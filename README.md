<p align="center">
  <a href="#english">🇺🇸 English</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="#中文">🇨🇳 中文</a>
</p>

---

<a id="english"></a>

# luoboa-illustrate

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

Config is saved to `~/.claude/skills/luoboa-illustrate/config.json`.

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
~/.claude/skills/luoboa-illustrate/config.json
```

### Full schema

```json
{
  "backend": "api",
  "api": {
    "provider": "openai",
    "base_url": "https://api.openai.com",
    "api_key": "sk-xxxx",
    "model": "gpt-image-2"
  },
  "brand": {
    "enabled": false,
    "name": "",
    "tagline": "",
    "logo_url": null,
    "website": ""
  }
}
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
rm ~/.claude/skills/luoboa-illustrate/config.json
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

---
---

<a id="中文"></a>

# luoboa-illustrate

AI 驱动的微信公众号文章配图工具。给它一篇 Markdown 文章，选择风格，自动生成封面和章节插图，并插入回文章中。

**作为 [Claude Code](https://claude.ai/code) 自定义 Skill 使用。**

---

## 功能特性

- 🎨 **12 种视觉风格** — 从暗色科技到水彩、像素风到禅意极简
- 🖼️ **封面 + 章节插图** — 每个 `##` 标题生成一张配图，不止封面
- 🔌 **多种后端** — OpenAI API、GRS AI、兼容接口、本地服务或 Dreamina CLI
- 🏷️ **可选品牌水印** — 一次配置，自动出现在合适风格的封面上
- 📝 **自动插入 Markdown** — 插图放置在对应标题下方
- 👤 **角色一致性** — 情感治愈风格通过参考图保持角色在各章节中一致

---

## 快速开始

### 1. 安装 Skill

```bash
npx skills add opapa/luoboa-illustrate
```

<details>
<summary>其他安装方式</summary>

```bash
# 全局安装
npx skills add opapa/luoboa-illustrate -g

# 克隆并手动复制
git clone https://github.com/opapa/luoboa-illustrate.git
cp -r luoboa-illustrate ~/.claude/skills/

# 或创建符号链接（适合开发）
ln -s "$(pwd)/luoboa-illustrate" ~/.claude/skills/luoboa-illustrate
```

**卸载：**

```bash
npx skills remove luoboa-illustrate
```

</details>

### 2. 首次运行配置

首次触发 skill 时，设置向导会引导你完成：

1. **选择后端** — API 或 Dreamina CLI
2. **配置 API** — 选择提供商、输入密钥和 URL
3. **品牌（可选）** — 名称、标语、Logo URL、网站

配置保存至 `~/.claude/skills/luoboa-illustrate/config.json`。

### 3. 生成配图

在 Claude Code 中打开一篇 Markdown 文章，输入：

```
给这篇文章配图
```

或

```
/luoboa-illustrate
```

---

## 视觉风格

### 主要风格

| # | 风格 | 描述 | 适用场景 |
|---|------|------|----------|
| 1 | 🖥️ 科技风 | 暗色分割构图 + Excalidraw 草图 | AI、工程、深度技术 |
| 2 | 💕 情感治愈 | 暖莫兰迪色调 + 角色一致性 | 故事、随笔、生活 |

### 扩展风格（点击「更多」）

| # | 风格 | ID | 关键词 | 适用场景 |
|---|------|----|--------|----------|
| 3 | 📐 蓝图纸 | `blueprint` | 蓝色网格、技术示意图 | 系统架构、工程设计 |
| 4 | ✏️ 手绘笔记 | `sketch-notes` | 马卡龙色、手绘、温暖 | 教程、笔记、概念 |
| 5 | 📜 复古风 | `vintage` | 旧羊皮纸、棕色、古典 | 历史、传承、品牌故事 |
| 6 | 🌸 卡哇伊 | `kawaii` | 粉彩、圆润造型、粗描边 | 生活、宠物、休闲 |
| 7 | 🌆 赛博霓虹 | `cyberpunk-neon` | 深紫、霓虹光、故障风 | 未来科技、游戏、科幻 |
| 8 | 💼 商务风 | `corporate` | 白灰金、几何图形 | 商业、战略、分析 |
| 9 | 🍃 水彩风 | `watercolor` | 大地色系、有机笔触 | 旅行、养生、自然 |
| 10 | 🕹️ 像素风 | `pixel-art` | 8-bit、复古游戏、马赛克 | 游戏文化、复古科技 |
| 11 | 🎭 丝网印刷 | `screen-print` | 大色块、半调、限色 | 评论、文化批评 |
| 12 | 🧘 禅意极简 | `zen-minimal` | 大留白、单墨线 | 哲学、极简、禅意 |

---

## 配置

### 配置文件位置

```
~/.claude/skills/luoboa-illustrate/config.json
```

### 完整配置格式

```json
{
  "backend": "api",
  "api": {
    "provider": "openai",
    "base_url": "https://api.openai.com",
    "api_key": "sk-xxxx",
    "model": "gpt-image-2"
  },
  "brand": {
    "enabled": false,
    "name": "",
    "tagline": "",
    "logo_url": null,
    "website": ""
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `backend` | `"api"` \| `"dreamina"` | 图片生成后端 |
| `api.provider` | string | `"grsai"` / `"openai"` / `"openai-compatible"` / `"local"` |
| `api.base_url` | string | API 基础 URL（不含末尾斜杠） |
| `api.api_key` | string | API 密钥 |
| `api.model` | string | 模型名称（默认：`gpt-image-2`） |
| `brand.enabled` | boolean | 在封面上显示品牌水印 |
| `brand.name` | string | 品牌展示名称 |
| `brand.tagline` | string | 品牌标语 |
| `brand.logo_url` | string\|null | 品牌 Logo 图片 URL |
| `brand.website` | string | 品牌网站 URL |

### 支持的 API 提供商

| 提供商 | ID | Base URL | 说明 |
|--------|-----|----------|------|
| GRS AI | `grsai` | `https://grsai.dakka.com.cn` | 国内 GPT-image-2 节点；插图使用 SSE |
| OpenAI | `openai` | `https://api.openai.com` | OpenAI 官方 API |
| 兼容接口 | `openai-compatible` | 用户自定义 | 任何 OpenAI 兼容接口（代理、第三方） |
| 本地服务 | `local` | `http://localhost:xxxx` | 自建图片生成服务 |

### 重新配置

删除配置文件后，下次使用时会重新运行设置向导：

```bash
rm ~/.claude/skills/luoboa-illustrate/config.json
```

也可以直接编辑配置文件。

---

## 工作原理

### 工作流程

```
Markdown 文章
    │
    ├── 解析标题（# 和 ##）
    │
    ├── 选择风格（12 种）
    │
    ├── 生成封面（1920×832）
    │
    ├── 生成章节插图（1024×1024）
    │       │
    │       └── 情感治愈风格：传递参考图
    │           保持角色一致性
    │
    └── 在每个 ## 标题下插入 ![](images/xx.png)
```

### 输出结构

```
article/0531/MyArticle/
├── MyArticle.md
└── images/
    ├── 00-cover.png          （封面，不插入文章）
    ├── 01-first-section.png  （插入到 ## 第一章节 下方）
    ├── 02-second-section.png
    └── ...
```

### 图片尺寸

| 类型 | 尺寸 | 用途 |
|------|------|------|
| 封面 | 1920×832 (21:9) | 公众号文章封面缩略图 |
| 章节插图 | 1024×1024 (1:1) | 文章内配图 |

### 品牌水印

品牌信息仅出现在「专业」风格（科技、蓝图纸、赛博、商务、像素风）的封面上。情感和艺术风格保持画面干净。

当 `brand.enabled` 为 `false`（默认）时，所有风格均不添加水印。

---

## API 提供商差异

| 特性 | `grsai` | `openai` / `openai-compatible` / `local` |
|------|---------|------------------------------------------|
| 封面接口 | `/v1/images/generations` | `/v1/images/generations` |
| 插图接口 | `/v1/draw/completions`（SSE） | `/v1/images/generations` |
| 插图请求 | `aspectRatio` + `replyType: "async"` | `size: "1024x1024"` |
| 插图响应 | SSE 流 | 标准 JSON |

---

## 触发词

说出以下任意指令即可激活 Skill：

- `给文章配图` / `配图` / `插图` / `封面`
- `生成插图` / `做封面`
- `/luoboa-illustrate`

---

## 环境要求

- **Claude Code**（CLI 或桌面版）
- **以下任一**：图片生成 API 密钥 或 本地安装 Dreamina CLI
- **Python 3**（用于 API 调用 — 仅使用标准库，无需 pip install）

---

## 许可证

MIT
