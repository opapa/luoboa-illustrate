---
name: luoboa-illustrate
description: Generate illustrations for WeChat public account articles (公众号配图) using image generation APIs or Dreamina CLI, then insert them into the article markdown file. Use this skill whenever the user wants to create illustrations, images, or cover art for their articles, or mentions 配图/插图/封面 for articles. Also trigger when the user asks to "给文章配图", "生成插图", "做封面".
---

# WeChat Article Illustrator

Generate cover and section illustrations for WeChat public account (公众号) articles. One image per `##` heading, plus a cover.

## First-Run Setup

On first use, check if `config.yaml` exists in the skill directory. If not, run a setup wizard:

1. **Choose backend** — API or Dreamina CLI
2. **Configure API** (if API chosen):
   - Ask: "Which provider?" Show options: GRS AI / OpenAI / OpenAI-Compatible / Local
   - Collect: base URL (pre-fill default per provider), API key, model name
3. **Brand (optional)** — Ask: "Want to add brand watermark?" If yes, collect: name, tagline, logo URL, website
4. Save to `config.yaml`

### Config schema

```yaml
backend: api

api:
  provider: openai        # grsai / openai / openai-compatible / local
  base_url: https://api.openai.com
  api_key: sk-xxxx
  model: gpt-image-2

brand:
  enabled: false
  name: ""
  tagline: ""
  logo_url: null
  website: ""
```

### Provider defaults

| Provider | base_url default | Notes |
|----------|-----------------|-------|
| `grsai` | `https://grsai.dakka.com.cn` | China node, SSE for illustrations |
| `openai` | `https://api.openai.com` | Official OpenAI |
| `openai-compatible` | (user must provide) | Proxies, third-party |
| `local` | (user must provide) | Self-hosted, e.g. `http://localhost:8080` |

### Re-configure

Tell user: "Delete config.yaml and the wizard runs again next time, or edit it directly."
```bash
rm ~/.claude/skills/luoboa-illustrate/config.yaml
```

## Workflow

### Step 1: Read Article Structure

Read the target `.md` file. Extract:
- Article title (the `# ` heading, or filename)
- All section headings (every `## ` subheading, in order)
- Full content of each section (for generating relevant prompts)

### Step 2: Style Selection

Ask the user to pick a style. Show primary choices first:

| # | 风格 | 一句话描述 |
|---|------|-----------|
| 1 | 🖥️ 科技风 | 暗黑对立构图 + Excalidraw手绘草稿 |
| 2 | 💕 柔情风 | 温暖治愈莫兰迪 + 人物一致性 |
| 3 | 🎨 更多风格... | 查看10种扩展风格 |

If user picks 1 → Workflow A (科技类)
If user picks 2 → Workflow B (情感治愈类)
If user picks 3 → show extended catalog from `references/style-guide.md`

### Step 3: Generate Images

Use the `scripts/generate.py` script. It reads config from `config.yaml`.

**Cover image:**
```bash
python scripts/generate.py cover \
  --prompt "<cover prompt>" \
  --output "images/00-cover.png"
```
Brand logo is automatically included if `brand.enabled` is true and the style requires it.

**Section illustration:**
```bash
python scripts/generate.py section \
  --prompt "<section prompt>" \
  --output "images/01-section-name.png"
```
For emotional style (Workflow B), add `--ref-url` starting from the 2nd illustration:
```bash
python scripts/generate.py section \
  --prompt "<section prompt>" \
  --output "images/02-section-name.png" \
  --ref-url "<URL returned from previous generation>"
```

### Step 4: Insert Images into Article

After all images are generated, insert them into the `.md` file:
- Each illustration goes **right below its `##` heading**
- Cover image is NOT inserted (it's used separately by the WeChat platform)
- Use relative path: `![](images/<filename>.png)`

Format:
```markdown
## Section Title

![](images/01-section-title.png)

Section content...
```

## Prompt Templates

All prompt templates are in `references/style-guide.md` and `references/style-templates.md`.

**Brand variables**: Templates use `{brand.name}`, `{brand.tagline}`, `{brand.website}` placeholders. Read `config.yaml` brand section and replace these before sending prompts. Only apply brand when `brand.enabled` is true AND the style supports watermark.

### Key rules for building prompts:

- **Send original section content** — do NOT summarize. The model needs full text.
- For sections over 2000 characters, trim to 1000-1500 essential characters.
- Strip markdown formatting (`**`, `[]()`, `|---|`) before sending.
- If API returns `failed`/`output_moderation`: rephrase prompt and retry once.

## Directory Structure

```
article/<MMDD>/<ArticleName>/
├── 00-封面.png          (cover, NOT inserted into md)
├── 01-<section>.png     (first ## heading)
├── 02-<section>.png     (second ## heading)
└── ...
```

Image sizes:
| Type | Size | Notes |
|------|------|-------|
| Cover | 1920x832 (21:9) | Landscape, WeChat cover |
| Section | 1024x1024 (1:1) | Square, body illustration |

## Workflow A: 科技类

- Cover: dark-tech split composition with brand logo (if enabled). Prompt template in `references/style-guide.md`.
- Sections: Excalidraw hand-drawn sketch style. Prompt template in `references/style-guide.md`.

## Workflow B: 情感治愈类

- Ask user for cover sub-style (A/B/C/D). Default to B.
- Cover: emotional photography or illustration style, NO brand logo even if enabled.
- Sections: warm healing style with Morandi colors.
- **Critical**: from 2nd section onward, pass previous generation's URL as `--ref-url` to maintain character consistency.
- **Critical**: send full novel/story text, not summaries.

## Workflow C: 通用风格

When user picks from extended catalog, use corresponding prompt templates from `references/style-templates.md`.

## Brand Watermark Rules

Brand info only appears on covers of "professional" styles:
- ✅ Tech, Blueprint, Cyberpunk, Corporate, Pixel Art
- ❌ Emotional, Sketch Notes, Vintage, Kawaii, Watercolor, Screen Print, Zen Minimal

When `brand.enabled` is false, no watermark on any style.

## API Provider Differences

| Feature | `grsai` | `openai` / `openai-compatible` / `local` |
|---------|---------|------------------------------------------|
| Cover endpoint | `/v1/images/generations` | `/v1/images/generations` |
| Illustration endpoint | `/v1/draw/completions` (SSE) | `/v1/images/generations` |
| Illustration request | `aspectRatio` + `replyType: "async"` | `size: "1024x1024"` |
| Illustration response | SSE stream | Standard JSON |

## Edge Cases

- No `##` headings → generate only cover
- No `#` heading → use filename as title
- API returns `violation` → rephrase and retry
- API returns `failed` → retry once, then report error and continue
- User only wants cover → skip section images and insertion
