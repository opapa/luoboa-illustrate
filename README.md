# luoboa-illustrate

**[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)**

AI-powered illustration generator for WeChat public account articles (公众号). Give it a Markdown article, pick a style, and it generates a cover + per-section illustrations, then inserts them back into the article automatically.

**Works with [Claude Code](https://claude.ai/code)** as a custom skill.

---

## Features

- 🎨 **12 visual styles** — from dark-tech to watercolor, pixel art to zen minimal
- 🖼️ **Cover + section illustrations** — one image per `##` heading, not just a cover
- 🔌 **Multiple backends** — OpenAI API, GRS AI, compatible endpoints, local services, or Dreamina CLI
- 🏷️ **Optional brand watermark** — configure once, appears on appropriate style covers
- 📝 **Auto-insert into Markdown** — illustrations are placed under the corresponding headings
- 👤 **Character consistency** — Emotional-Healing style passes reference images to keep characters consistent across sections

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

| # | Style | Description | Best For |
|---|-------|-------------|----------|
| 1 | 🖥️ Tech | Dark split-composition + Excalidraw sketches | AI, engineering, deep tech |
| 2 | 💕 Emotional-Healing | Warm Morandi tones + character consistency | Stories, essays, lifestyle |

### Extended Styles (click "更多")

| # | Style | ID | Keywords | Best For |
|---|-------|----|----------|----------|
| 3 | 📐 Blueprint | `blueprint` | Blue grid, technical schematics | System architecture, engineering |
| 4 | ✏️ Sketch Notes | `sketch-notes` | Macaron colors, hand-drawn, warm | Tutorials, notes, concepts |
| 5 | 📜 Vintage | `vintage` | Aged parchment, sepia, classical | History, heritage, brand stories |
| 6 | 🌸 Kawaii | `kawaii` | Pastel pink, round shapes, thick outlines | Lifestyle, pets, casual |
| 7 | 🌆 Cyberpunk Neon | `cyberpunk-neon` | Deep purple, neon glow, glitch | Future tech, gaming, sci-fi |
| 8 | 💼 Corporate | `corporate` | White + grey + gold, geometric | Business, strategy, analysis |
| 9 | 🍃 Watercolor | `watercolor` | Earth tones, organic brush | Travel, wellness, nature |
| 10 | 🕹️ Pixel Art | `pixel-art` | 8-bit, retro gaming, mosaic | Gaming culture, retro tech |
| 11 | 🎭 Screen Print | `screen-print` | Bold blocks, halftone, limited palette | Op-eds, cultural critique |
| 12 | 🧘 Zen Minimal | `zen-minimal` | Vast whitespace, single ink line | Philosophy, minimalism, zen |

---

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
    ├── Pick style (12 options)
    │
    ├── Generate cover (1920×832)
    │
    ├── Generate section illustrations (1024×1024)
    │       │
    │       └── Emotional-Healing: pass reference image
    │           for character consistency
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

Brand info only appears on covers of "professional" styles (Tech, Blueprint, Cyberpunk, Corporate, Pixel Art). Emotional and artistic styles keep a clean canvas.

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

---

## License

MIT
