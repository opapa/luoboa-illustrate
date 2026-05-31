---
name: luoboa-illustrate
description: Generate illustrations for WeChat public account articles (公众号配图) using image generation APIs or Dreamina CLI, then insert them into the article markdown file. Use this skill whenever the user wants to create illustrations, images, or cover art for their articles, or mentions 配图/插图/封面/快文配图/快文/视频素材 for articles. Also trigger when the user asks to "给文章配图", "生成插图", "做封面", "快文配图", "按句配图".
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
| 4 | ⚡ 快文配图 | 按句生成9:16竖图，即梦渲染文字，视频素材 |

If user picks 1 → Workflow A (科技类)
If user picks 2 → Workflow B (情感治愈类)
If user picks 3 → show extended catalog from `references/style-guide.md`
If user picks 4 → Workflow D (快文配图)

Also trigger Workflow D directly when user says "快文配图"/"快文"/"视频素材"/"按句配图".

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

## Workflow D: 快文配图（按句生成视频素材）

适合短平快的AI前沿资讯文章。按句子拆分，每句生成一张9:16竖版图片（即梦渲染文字），用于视频素材。

### Step 1: 读取文章并拆分句子

Read the target `.md` file. Then:

1. 去掉图片行 `![](...)`
2. 去掉空行和markdown格式标记
3. 按句号/问号/感叹号/换行拆分：`re.split(r'[。！？\n]+', text)`
4. 过滤短于3字的片段
5. 超过50字的句子智能截断（到上一个逗号，否则直接截断加省略号）
6. 展示拆分结果，让用户确认（可增删改句子）

### Step 2: 选择快文风格

Show 6 quick-styles (from `references/quick-styles.md`):

| # | 风格 | 一句话描述 |
|---|------|-----------|
| 1 | 🖥️ 科技蓝 | 深蓝渐变 + 白色发光文字 + 电路装饰 |
| 2 | 🔥 热点红 | 暗红渐变 + 金色文字 + 火焰脉冲 |
| 3 | 🌊 清新绿 | 浅绿白底 + 深色文字 + 简约线条 |
| 4 | 🎯 极简黑 | 纯黑背景 + 白色大字 + 最少装饰 |
| 5 | 🌙 暗夜紫 | 深紫渐变 + 浅紫白文字 + 星光 |
| 6 | 📰 资讯风 | 报纸排版 + 宋体文字 + 简洁边框 |

Default: 1 (科技蓝) for AI/科技类文章.

### Step 3: 确保即梦CLI环境可用

Check jimeng CLI is available. If not found, tell user to install jimeng-cli-free:

```bash
git clone https://github.com/leigegehaha/jimeng-cli-free.git
cd jimeng-cli-free
bash bin/jimeng-cli-free ensure
# Then load browser extension and login to jimeng.jianying.com
```

If jimeng is found, run ensure to verify:
```bash
bash <jimeng-path>/scripts/ensure_opencli_and_jimeng.sh
```

### Step 4: 批量生成图片

Use `scripts/quick_generate.py`:

```bash
python scripts/quick_generate.py \
  --input "article.md" \
  --output "article/<MMDD>/<ArticleName>/quick/" \
  --style <style-id> \
  --concurrency 2
```

Key behaviors:
- Calls `bash <jimeng-path>/bin/jimeng-cli-free generate "<prompt>" --model high_aes_general_v50 --aspect 9:16`
- Each generation produces 4 images; picks 0001.png
- Copies to output as `01.png`, `02.png`, etc.
- Failed generations retry once with adjusted font, then skip
- Writes `sentences.txt` with sentence-to-image mapping

### Step 5: 输出

Directory structure:
```
article/<MMDD>/<ArticleName>/quick/
├── 01.png          (第1句的9:16图)
├── 02.png          (第2句的9:16图)
├── ...
└── sentences.txt   (序号|原文|状态 对照表)
```

`sentences.txt` format:
```
01|人类本质是上下文窗口只有7的大模型|✅
02|幻觉比GPT还严重|✅
03|OpenAI发布o1模型的时候|❌
```

**Does NOT modify the original markdown file.**

### 即梦文字渲染注意事项

- 文字用「」包裹，让即梦识别为文字渲染区域
- 每句不超过50字（超过则截断）
- 末尾加"文字渲染清晰不乱码"
- 默认模型 `high_aes_general_v50`（5.0 Lite 文字渲染最好）
- 如果文字乱码，重试时换字体描述（详见 `references/quick-styles.md` 重试策略）

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
- Jimeng CLI not found → tell user to install jimeng-cli-free and load browser extension
- Jimeng text garbled → retry with adjusted font description (see `references/quick-styles.md`)
- Article too long (>80 sentences) → warn user about credit consumption, confirm before proceeding
