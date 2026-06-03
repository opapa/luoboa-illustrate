# luoboa-illustrate

**[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)**

AI-powered illustration generator for WeChat public account articles (公众号). Give it a Markdown article, pick a style, and it generates a cover + per-section illustrations, then inserts them back into the article automatically.

**Works with [Claude Code](https://claude.ai/code)** as a custom skill.

---

## Features

- 🎨 **23 visual styles** — 11 primary styles + 10 extended + 6 quick-styles, covering all major public-account verticals
- 🖼️ **Cover + section illustrations** — one image per `##` heading, not just a cover
- 🔌 **Multiple backends** — OpenAI API, GRS AI, compatible endpoints, local services, or Dreamina CLI
- 🏷️ **Optional brand watermark** — configure once, appears on appropriate style covers
- 📝 **Auto-insert into Markdown** — illustrations are placed under the corresponding headings
- 🎯 **5-dimension consistency system** — Type × Palette × Rendering × Font × Mood; cover and illustrations share the same visual vocabulary
- 👤 **Character consistency** — styles with characters (Pet, Fashion, ACG) pass reference images across sections

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
| 3 | 📷 Nostalgic Photo | 1990s film stock + golden hour / warm tungsten lighting | Memories, family, nostalgia |
| 4 | 🍜 Food | Warm food photography, steam, sauce highlights | Recipes, restaurant reviews, snacks |
| 5 | 🗺️ Travel / City | Modern landscape photography, cinematic, cityscape | Travel guides, city walks, scenery |
| 6 | 🐾 Pet / Q-version | Q-version character illustration, pastel palette | Pet accounts, parenting, healing |
| 7 | 🏠 Home / Lifestyle | Interior photography, MUJI / Nordic, natural light | Home decor, lifestyle, minimalism |
| 8 | 💄 Fashion / Beauty | High-fashion editorial, character consistency | Lookbook, makeup tutorials, reviews |
| 9 | 🎮 ACG / Anime | Cel-shaded illustration, vivid colors, character consistency | Anime, games, light novels |
| 10 | 📊 Review / Infographic | Structured infographic, scorecards, comparison charts | Product reviews, rankings, data |
| 11 | 🏃 Sports / Fitness | Action photography, high shutter speed, dynamic | Fitness, sports, marathon |
| 12 | ⚡ Quick-style | 9:16 vertical, sentence-by-sentence text rendering | Short video material, quick reads |

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
