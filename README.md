# luoboa-illustrate

**[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)**

AI-powered illustration generator for WeChat public account articles (公众号). Give it a Markdown article, pick a style, and it generates a cover + per-section illustrations, then inserts them back into the article automatically.

**Works with [Claude Code](https://claude.ai/code)** as a custom skill.

---

## Features

- 🎨 **26+ visual styles** — 11 primary + 4 special (快文/微头条/知乎/小黑科普) + 10 extended + 6 quick-styles, covering all major public-account verticals
- 🖼️ **Cover + section illustrations** — one image per `##` heading, not just a cover
- 🔌 **Multiple backends** — OpenAI API, GRS AI, compatible endpoints, local services, or Dreamina CLI (per-style default)
- 🏷️ **Optional brand watermark** — configure once, appears on appropriate style covers
- 📝 **Auto-insert into Markdown** — illustrations are placed under the corresponding headings
- 🎯 **5-dimension consistency system** — Type × Palette × Rendering × Font × Mood; cover and illustrations share the same visual vocabulary
- 👤 **Character consistency** — styles with characters (Pet, Fashion, ACG) pass reference images across sections
- 🐾 **Optional 小黑科普 mode** — delegates to `/ian-xiaohei-illustrations` for Ian-style absurd hand-drawn + 小黑 IP illustrations on 科技/科普/知乎/技术文 contexts (default backend: API, not Dreamina CLI)
- 🎨 **Banner design system** — inherits the mature 4-font × 8-typography framework from `/baoyu-cover-image`, with explicit `Font Application` section in every prompt

---

## Quick Start

### 1. Install the skill

```bash
npx skills add opapa/luoboa-illustrate
```

<details>
<summary>Other install methods</summary>

```bash
# Install globally
npx skills add opapa/luoboa-illustrate -g

# Clone & copy manually
git clone https://github.com/opapa/luoboa-illustrate.git
cp -r luoboa-illustrate ~/.claude/skills/

# Or symlink for development
ln -s "$(pwd)/luoboa-illustrate" ~/.claude/skills/luoboa-illustrate
```

**Uninstall:**

```bash
npx skills remove luoboa-illustrate
```

</details>

### 2. First-run setup

When you trigger the skill for the first time, a setup wizard will walk you through:

1. **Choose backend** — API or Dreamina CLI
2. **Configure API** — select provider, enter key & URL
3. **Brand (optional)** — name, tagline, logo URL, website

Config is saved to `~/.claude/skills/luoboa-illustrate/config.yaml`.

### 3. Generate illustrations

In Claude Code, open a Markdown article and say:

```
给这篇文章配图
```

or

```
/luoboa-illustrate
```

---

## Visual Styles

### Primary Styles

| # | Style | Description | Best For | Default Backend |
|---|-------|-------------|----------|-----------------|
| 1 | 🖥️ Tech | **White-background Excalidraw hand-drawn sketches** (engineer-on-whiteboard vibe, slightly wobbly lines) | AI, engineering, deep tech | API |
| 2 | 💕 Emotional-Healing | Warm Morandi tones + character consistency | Stories, essays, lifestyle | API |
| 3 | 📷 Nostalgic Photo | 1990s film stock + golden hour / warm tungsten lighting | Memories, family, nostalgia | API |
| 4 | 🍜 Food | Warm food photography, steam, sauce highlights | Recipes, restaurant reviews, snacks | API |
| 5 | 🗺️ Travel / City | Modern landscape photography, cinematic, cityscape | Travel guides, city walks, scenery | API |
| 6 | 🐾 Pet / Q-version | Q-version character illustration, pastel palette | Pet accounts, parenting, healing | API |
| 7 | 🏠 Home / Lifestyle | Interior photography, MUJI / Nordic, natural light | Home decor, lifestyle, minimalism | API |
| 8 | 💄 Fashion / Beauty | High-fashion editorial, character consistency | Lookbook, makeup tutorials, reviews | API |
| 9 | 🎮 ACG / Anime | Cel-shaded illustration, vivid colors, character consistency | Anime, games, light novels | API |
| 10 | 📊 Review / Infographic | Structured infographic, scorecards, comparison charts | Product reviews, rankings, data | API |
| 11 | 🏃 Sports / Fitness | Action photography, high shutter speed, dynamic | Fitness, sports, marathon | API |
| 12 | ⚡ Quick-style | 9:16 vertical, sentence-by-sentence text rendering | Short video material, quick reads | Dreamina CLI |
| 13 | 📰 Weibo Toutiao | Per-news 9:16 marker-pen Q-version cartoon | News, quick updates | Dreamina CLI |
| 14 | 📐 Zhihu Article | **White background + black text** + minimum blue/orange + flowchart/stats/knowledge graph/wireframe (Tufte high data-ink ratio, professional data-driven) | Zhihu, technical blogs, deep analysis | **Dreamina CLI 4.6/5.0** |
| 15 | 🐾 小黑科普 | **Ian absurd hand-drawn + 小黑 IP** + pure white background + sparse red/orange/blue annotations + fresh original metaphor; delegates to `/ian-xiaohei-illustrations` | 科技/科普/知乎/技术文 contexts, 概念隐喻/机制解释/状态对比/判断收束 | **API** (grsai/openai/compatible/local) |

### Choosing between Zhihu (14) and 小黑科普 (15)

When 知乎/科技/科普/技术文/分析报告 triggers fire **and** the article has 概念/机制/隐喻/对比/收束 content, the skill will **ask you to pick** via `AskUserQuestion`:

- **Pick 14 (Workflow Z) if** your content is dominated by **numbers, statistics, flowcharts, data tables** — academic/Tufte style, default to Dreamina CLI 4.6
- **Pick 15 (Workflow X) if** your content is dominated by **concept metaphors, mechanism explanations, judgments** — Ian-style absurd hand-drawn, default to API, delegates to `/ian-xiaohei-illustrations`

### Extended Styles (click "更多")

| # | Style | ID | Keywords | Best For |
|---|-------|----|----------|----------|
| 13 | 📐 Blueprint | `blueprint` | Blue grid, technical schematics | System architecture, engineering |
| 14 | ✏️ Sketch Notes | `sketch-notes` | Macaron colors, hand-drawn, warm | Tutorials, notes, concepts |
| 15 | 📜 Vintage | `vintage` | Aged parchment, sepia, classical | History, heritage, brand stories |
| 16 | 🌸 Kawaii | `kawaii` | Pastel pink, round shapes, thick outlines | Lifestyle, pets, casual |
| 17 | 🌆 Cyberpunk Neon | `cyberpunk-neon` | Deep purple, neon glow, glitch | Future tech, gaming, sci-fi |
| 18 | 💼 Corporate | `corporate` | White + grey + gold, geometric | Business, strategy, analysis |
| 19 | 🍃 Watercolor | `watercolor` | Earth tones, organic brush | Travel, wellness, nature |
| 20 | 🕹️ Pixel Art | `pixel-art` | 8-bit, retro gaming, mosaic | Gaming culture, retro tech |
| 21 | 🎭 Screen Print | `screen-print` | Bold blocks, halftone, limited palette | Op-eds, cultural critique |
| 22 | 🧘 Zen Minimal | `zen-minimal` | Vast whitespace, single ink line | Philosophy, minimalism, zen |

### Cover Typography (Emotional-Healing & Nostalgic Photo only)

12 cover typography options A–L pair with the photo-based styles: A Japanese-cinema / B Vintage-magazine / C Natural-breath / D Letter-handwritten / E Light-overlay / F Minimal-Chinese / G Wong-Kar-wai / H Polaroid-caption / I Record-cover / J Newspaper-headline / K Poetry-scatter / L Classical-frontispiece.

---

## ✨ Highlights of This Version

### 🏆 11 Primary Styles Cover Every Major Vertical

From the first release's 2 styles to **11 primary + 10 extended + 6 quick** in the current version, the library now covers all top public-account verticals: AI/tech, emotion/healing, food, travel, pets, home, fashion, anime, reviews, sports — plus nostalgia as a base photo style.

### 📐 5-Dimension Consistency System

Every style is defined across 5 dimensions: **Type × Palette × Rendering × Font × Mood**. The cover sets all 5; section illustrations inherit 3 (Palette, Rendering, Mood) so every image in the article looks like part of the same set — no painterly-cover + digital-illustration mismatches.

### 🎨 Reference-Backed Banner Design

Cover banners are not "illustration with small text in the corner" — they are **type-design-driven visual works** with title taking 50–70% of visual weight. The library provides font prompts (clean / handwritten / serif / display) and 8 text-effect techniques (gradient / stroke-text / shadow-3d / highlight / neon / handwritten / bubble / brush) inspired by the `baoyu-cover-image` skill.

### 🌅 Nostalgic Photo: Warm, Not Gloomy

The 1990s film-stock style was rewritten to fix a common failure mode — the model would default to "decayed, dim, blue-tinted" photos. Every Nostalgic Photo prompt now starts with an explicit **warm-tone baseline** (Kodak Gold / Fujifilm Superia, golden hour / warm tungsten) and a **forbidden-words list** (no cold, no gloomy, no desaturated-blue, no horror). Even "empty room" scenes stay warm and contemplative, never melancholic.

### 👤 Character Consistency for Pet / Fashion / ACG

Three character-heavy styles (Pet / Q-version, Fashion / Beauty, ACG / Anime) automatically pass the previous illustration as `--ref-url` to the next, so the same character stays recognizable across all section images.

---

## 🆕 2026-06 Update Log

### 🐾 Style #15 — 小黑科普 (Workflow X) — New, API-only, delegates to `/ian-xiaohei-illustrations`

A new style for 科技公众号深度文 + 知乎技术/科普文 + AI 概念解释 + 机制/原理/对比类文章. When the trigger words `技术文`/`科普文`/`分析报告`/`知乎` fire **and** the content has `概念`/`机制`/`隐喻`/`对比`/`收束` keywords, the skill now **asks the user** to pick between Workflow Z (academic infographic) and Workflow X (Ian absurd hand-drawn).

Concrete additions:

- **Style #15 added** to the primary table (16 styles total: 11 main + 4 special + 1 ×iaohhei)
- **Backend locked to API** (`scripts/generate.py section --prompt=... --aspect-ratio=16:9`), **NOT Dreamina CLI**. Empirically verified on 2026-06-06: Dreamina 5.0 failed 3/3 attempts at 小黑科普 ("final generation failed"), grsai GPT-Image-2 succeeded on the first try. The 小黑 style depends on IP consistency + Chinese hand-written annotations + absurd metaphors, which Dreamina CLI cannot reliably deliver.
- **New AskUserQuestion step** in the trigger flow: when 知乎/科技/科普/技术文/分析报告 trigger fires, the skill now prompts the user to pick Z vs X (default recommendation: numbers/flowchart → Z; concept/metaphor/judgment → X)
- **Dependencies bumped from 1 to 3 external skills**: now requires `/ian-xiaohei-illustrations` (for X) in addition to existing `/baoyu-cover-image` (for banner typography) and `/baoyu-xhs-images` (for balanced multi-zone layouts)
- **Reference doc added**: `references/style-guide.md` end-of-file section "小黑科普风格" with backend rule, prompt template source, naming, decision tree

Verified sample output (2026-06-06, 知乎答 "Agent Skill 为何没有像 MCP 那样火爆？"):

- 3 illustrations, 16:9, white background, 小黑 IP central in every frame
- Original metaphors: 歪秤对比声量 vs 用户量 / 协议门 vs 产品按钮门 / USB-C 洞 vs App Store 金库
- All passed 5-item QA: ①白底 ②小黑承担动作 ③全新隐喻 ④不留标题 ⑤无 PPT 感

### ✏️ Tech Style (Workflow A) — White-Background Excalidraw Sketch

Tech-style section illustrations switched from "white-background data infographic" (McKinsey/TED-Ed feel) to **"white-background Excalidraw hand-drawn sketch"** (engineer-on-whiteboard vibe). Concretely:

- Sections now render as **hand-drawn** boxes/arrows on white paper, with **slight wobble** in lines and box edges (this wobble is the "engineer vibe" core, do not remove)
- New Excalidraw palette: white + charcoal main lines + Excalidraw blue highlight + semi-transparent yellow box fill + tiny orange/purple accents (no pure red)
- 6 variants re-mapped for sketch-friendliness: flowchart / concept graph / system architecture / wireframe / timeline / decision tree (replaced the old bar/line/scatter/table/line-chart set that didn't fit hand-drawn aesthetic)
- Use case: AI / engineering / Claude Code / vibe-coding / tool-tutorial public-account articles where readers expect "tech-person draws on a whiteboard" feel, not "consulting firm report" feel

### 🚀 Zhihu Style (Workflow Z) — Defaults to Dreamina CLI

Zhihu-article illustrations now **default to Dreamina CLI** (即梦/剪映) instead of going through the API path. Rationale:

- Zhihu content is Chinese; Jimeng/Dreamina renders Chinese text and vector white-background info-graphics more reliably than GPT-image-2
- Model `4.6` + `2k` resolution + `16:9` ratio is the verified production combo
- Override path: if user explicitly says "用 API", switch to `scripts/generate.py` (not the default)

### 🛡️ Color Names Instead of Hex in Prompts

Found a real-world bug: when prompts contained `#FFFFFF` / `#1A1A1A` / `#056DE8`, the Dreamina v42 visualizer treated hex strings as **visible text** and printed them on the image (e.g. bar chart column tops showed literal `#056DE8` text). Fixed by:

- Replacing all hex codes in Workflow Z templates with **Chinese color names** (纯白 / 纯黑 / 知乎蓝 / 浅灰 / 暖橙)
- Adding a hard prompt constraint: *"颜色仅作为风格约束描述,不允许在画面中打印任何颜色名称、颜色代码或 hex 字符"*
- Verified by side-by-side: original (hex in prompt) → columns showed `#056DE8`; fixed (Chinese name + constraint) → clean `70%` / `25%` / `10%` / `60%` labels

## Configuration

### Config file location

```
~/.claude/skills/luoboa-illustrate/config.yaml
```

### Full schema

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

### Field reference

| Field | Type | Description |
|-------|------|-------------|
| `backend` | `"api"` \| `"dreamina"` | Image generation backend |
| `api.provider` | string | `"grsai"` / `"openai"` / `"openai-compatible"` / `"local"` |
| `api.base_url` | string | API base URL (no trailing slash) |
| `api.api_key` | string | API key for authentication |
| `api.model` | string | Model name (default: `gpt-image-2`) |
| `brand.enabled` | boolean | Show brand watermark on covers |
| `brand.name` | string | Brand display name |
| `brand.tagline` | string | Brand tagline / slogan |
| `brand.logo_url` | string\|null | Brand logo image URL |
| `brand.website` | string | Brand website URL |

### Supported API providers

| Provider | ID | Base URL | Notes |
|----------|-----|----------|-------|
| GRS AI | `grsai` | `https://grsai.dakka.com.cn` | China-based GPT-image-2 node; uses SSE for illustrations |
| OpenAI | `openai` | `https://api.openai.com` | Official OpenAI API |
| Compatible | `openai-compatible` | User-defined | Any OpenAI-compatible endpoint (proxies, third-party) |
| Local | `local` | `http://localhost:xxxx` | Self-hosted image generation service |

### Re-configure

Delete the config file and the setup wizard will run again on next use:

```bash
rm ~/.claude/skills/luoboa-illustrate/config.yaml
```

Or edit it directly.

---

## How It Works

### Workflow

```
Markdown article
    │
    ├── Parse headings (# and ##)
    │
    ├── Pick style (11 primary + 10 extended + 6 quick)
    │
    ├── Generate cover (1920×832) using 5-dim style profile
    │
    ├── Generate section illustrations (1024×1024)
    │       │
    │       └── Inherit Palette + Rendering + Mood from cover
    │           for visual consistency
    │       │
    │       └── Pet / Fashion / ACG: pass previous image
    │           as --ref-url for character consistency
    │
    └── Insert ![](images/xx.png) under each ## heading
```

### Output structure

```
article/0531/MyArticle/
├── MyArticle.md
└── images/
    ├── 00-cover.png          (cover, not inserted into article)
    ├── 01-first-section.png  (inserted under ## First Section)
    ├── 02-second-section.png
    └── ...
```

### Image sizes

| Type | Size | Usage |
|------|------|-------|
| Cover | 1920×832 (21:9) | WeChat article cover thumbnail |
| Section illustration | 1024×1024 (1:1) | In-article images |

### Brand watermark

Brand info only appears on covers of "professional" styles: **Tech, Blueprint, Cyberpunk, Corporate, Pixel Art, Travel/City, Home/Lifestyle, Fashion/Beauty, ACG/Anime, Review/Infographic, Sports/Fitness**.

**No-watermark styles** (kept clean): Emotional, Nostalgic Photo, Sketch Notes, Vintage, Kawaii, Watercolor, Screen Print, Zen Minimal, Food, Pet/Q-version.

When `brand.enabled` is `false` (default), no watermark is added to any style.

---

## API Differences by Provider

| Feature | `grsai` | `openai` / `openai-compatible` / `local` |
|---------|---------|------------------------------------------|
| Cover endpoint | `/v1/images/generations` | `/v1/images/generations` |
| Illustration endpoint | `/v1/draw/completions` (SSE) | `/v1/images/generations` |
| Illustration request | `aspectRatio` + `replyType: "async"` | `size: "1024x1024"` |
| Illustration response | SSE stream | Standard JSON |

---

## Trigger Phrases

The skill activates when you say any of:

- `给文章配图` / `配图` / `插图` / `封面`
- `生成插图` / `做封面`
- `/luoboa-illustrate`

---

## Requirements

- **Claude Code** (CLI or desktop)
- **One of**: an image generation API key OR Dreamina CLI installed locally
- **Python 3** (for API calls — uses only stdlib, no pip install needed)

### External Skill Dependencies

This skill optionally delegates to **two** external Claude Code skills / skill collections. They are not required for primary styles 1-11, but heavily used by the special workflows and significantly improve quality:

| Dependency | Purpose |
|------------|---------|
| **`/baoyu-skills`** ([github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)) | A **large multi-skill project** containing many sub-skills (baoyu-cover-image / baoyu-image-gen / baoyu-xhs-images / baoyu-infographic / baoyu-comic / baoyu-article-illustrator / baoyu-translate / baoyu-markdown-to-html / baoyu-slide-deck / baoyu-post-to-wechat / baoyu-post-to-weibo / baoyu-post-to-x / baoyu-wechat-summary / baoyu-compress-image / baoyu-diagram / ...). **Not a hard-coded list** — this skill dynamically scans `~/.claude/skills/baoyu-skills/` and delegates to whichever sub-skill fits the current workflow need. Current known candidates: `/baoyu-cover-image` (banner design), `/baoyu-xhs-images` (multi-zone layout), `/baoyu-infographic` (high-density info-graphics), `/baoyu-comic` (comic / narrative), `/baoyu-image-gen` (API backend), `/baoyu-article-illustrator` (article long-image), `/baoyu-markdown-to-html` (HTML conversion), `/baoyu-translate` (translation), `/baoyu-slide-deck` (PPT), `/baoyu-post-to-*` (publishing), `/baoyu-wechat-summary` (group digest), `/baoyu-compress-image` (compression), `/baoyu-diagram` (SVG diagrams). Install: `git clone https://github.com/JimLiu/baoyu-skills ~/.claude/skills/baoyu-skills` |
| **`/ian-xiaohei-illustrations`** (`~/.claude/skills/ian-xiaohei-illustrations/`) | Provides 小黑 IP character design, style DNA (white background, hand-drawn wobble, red/orange/blue sparse annotations), composition patterns, QA checklist, and the prompt template. **Required for 科技/科普/知乎/技术文 contexts** when you pick style #15. |

**Dynamic delegation rule**: this skill does **not** hardcode "use these 4 sub-skills." At runtime it scans what's available in `~/.claude/skills/baoyu-skills/` and matches workflow needs → best sub-skill. The mapping table (workflow need → candidate sub-skill) is in `SKILL.md` "External Dependency → Dynamic Delegation Matrix."

If either dependency is missing, the relevant workflow degrades gracefully (skip the delegation, log a warning) — but cover typography quality, multi-zone layout options, and 小黑科普 availability will drop. The setup wizard should prompt to install both on first use.

---

---

## 👤 About the Author

**Luoboa (萝卜啊)** — AI practitioner, only writes about what's been personally verified.

🌐 **Blog**: [www.luoboa.com](https://www.luoboa.com)

Latest AI tech articles, tool recommendations, curated Skills & MCPs — updated daily.

📱 **WeChat Public Account**: Follow for exclusive resources

![QR Code](assets/qrcode.jpg)

What you'll find:

- ✅ **AI workflows** that are personally tested — not just reshared
- ✅ **Agent interview insights** from real interview scenarios
- ✅ **Practical AI adoption** experience for companies — no vaporware

📌 Reply with keywords to get resources instantly (no forwarding gimmicks):

| Keyword | Resource |
|---------|----------|
| **技巧** (Tips) | Practical AI efficiency tips |
| **Agent** | Agent interview prep guide |
| **转型** (Transform) | Company AI adoption playbook |

📅 **Content Schedule**:

| Day | Content |
|-----|---------|
| Mon–Fri | One Claude Code best practice + one best open-source AI Agent/Skill |
| Saturday | Weekly AI news roundup + GitHub top list |
| Sunday | Best practices in the AI Agent space |

### 🔗 Social Links

| Platform | Link |
|----------|------|
| 🐙 GitHub | [github.com/opapa](https://github.com/opapa) |
| 📘 Zhihu | [zhihu.com/people/opapar](https://www.zhihu.com/people/opapar) |
| 📺 Bilibili | [space.bilibili.com/316828422](https://space.bilibili.com/316828422) |
| ▶️ YouTube | [youtube.com/@ailuoboa](https://www.youtube.com/@ailuoboa) |

---

## License

MIT
