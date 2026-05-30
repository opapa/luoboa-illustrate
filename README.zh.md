# luoboa-illustrate

AI 驱动的公众号文章配图生成器。给它一篇 Markdown 文章，选择风格，自动生成封面 + 每个章节的插图，并插入回文章中。

**作为 [Claude Code](https://claude.ai/code) 自定义技能使用。**

---

## 功能特色

- 🎨 **12 种视觉风格** — 从暗黑科技到水彩自然，从像素游戏到禅意留白
- 🖼️ **封面 + 章节插图** — 每个 `##` 标题生成一张插图，不只是封面
- 🔌 **多种出图后端** — OpenAI API、GRS AI、兼容接口、本地服务、即梦 CLI
- 🏷️ **可选品牌水印** — 一次配置，自动出现在适合的风格封面上
- 📝 **自动插入 Markdown** — 插图自动插入到对应标题下方
- 👤 **人物一致性** — 柔情风通过参考图保证同一篇文章中角色外观统一

---

## 快速开始

### 1. 安装技能

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

# 或创建软链接（适合开发）
ln -s "$(pwd)/luoboa-illustrate" ~/.claude/skills/luoboa-illustrate
```

**卸载：**

```bash
npx skills remove luoboa-illustrate
```

</details>

### 2. 首次配置

首次使用时，配置向导会引导你完成：

1. **选择出图方式** — API 或 即梦 CLI
2. **配置 API** — 选择服务商、输入 Key 和 URL
3. **品牌标识（可选）** — 名称、标语、Logo URL、网址

配置保存在 `~/.claude/skills/luoboa-illustrate/config.json`。

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

### 主打风格

| # | 风格 | 描述 | 适合场景 |
|---|------|------|---------|
| 1 | 🖥️ 科技风 | 暗黑对立构图 + Excalidraw 手绘草稿 | AI、工程、深度技术 |
| 2 | 💕 柔情风 | 温暖治愈莫兰迪 + 人物一致性 | 故事、散文、生活随笔 |

### 扩展风格（点击"更多"）

| # | 风格 | 英文ID | 视觉关键词 | 适合场景 |
|---|------|--------|-----------|---------|
| 3 | 📐 学术蓝图风 | `blueprint` | 蓝色网格、技术蓝图、工程制图 | 系统架构、工程设计、深度技术文 |
| 4 | ✏️ 手绘笔记风 | `sketch-notes` | 马卡龙色、手绘线条、奶白底、温暖涂鸦 | 知识教程、读书笔记、概念解析 |
| 5 | 📜 复古文艺风 | `vintage` | 做旧羊皮纸、褐色调、古典装饰 | 历史人文、怀旧散文、品牌故事 |
| 6 | 🌸 可爱萌系风 | `kawaii` | 粉嫩色、圆滚滚、粗描边、贴纸感 | 生活分享、萌宠、轻松日常 |
| 7 | 🌆 赛博霓虹风 | `cyberpunk-neon` | 深紫黑底、霓虹发光、故障艺术 | 未来科技、游戏、AI科幻 |
| 8 | 💼 极简商务风 | `corporate` | 克制配色、几何图形、高级质感 | 行业分析、商业策略、投资人视角 |
| 9 | 🍃 自然水彩风 | `watercolor` | 水彩晕染、大地色系、有机笔触 | 旅行、养生、自然、慢生活 |
| 10 | 🕹️ 像素游戏风 | `pixel-art` | 8-bit像素、复古游戏机、色块马赛克 | 游戏文化、复古科技、极客趣味 |
| 11 | 🎭 海报丝印风 | `screen-print` | 大色块、半调网点、丝网印刷、强视觉冲击 | 观点评论、文化分析、深度社论 |
| 12 | 🧘 禅意留白风 | `zen-minimal` | 大面积留白、单色线描、呼吸感 | 哲学思辨、极简生活、禅意随笔 |

---

## 配置说明

### 配置文件位置

```
~/.claude/skills/luoboa-illustrate/config.json
```

### 完整配置示例

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
| `backend` | `"api"` \| `"dreamina"` | 出图后端 |
| `api.provider` | string | `"grsai"` / `"openai"` / `"openai-compatible"` / `"local"` |
| `api.base_url` | string | API 基础 URL（末尾不带斜杠） |
| `api.api_key` | string | API 密钥 |
| `api.model` | string | 模型名称（默认 `gpt-image-2`） |
| `brand.enabled` | boolean | 是否在封面显示品牌水印 |
| `brand.name` | string | 品牌名称 |
| `brand.tagline` | string | 品牌标语 |
| `brand.logo_url` | string\|null | 品牌 Logo 图片 URL |
| `brand.website` | string | 品牌网址 |

### 支持的 API 服务商

| 服务商 | ID | Base URL 示例 | 说明 |
|--------|-----|--------------|------|
| GRS AI | `grsai` | `https://grsai.dakka.com.cn` | 国内 GPT-image-2 节点，插图用 SSE 流式 |
| OpenAI | `openai` | `https://api.openai.com` | 官方 OpenAI API |
| 兼容接口 | `openai-compatible` | 用户自定义 | 任何 OpenAI 兼容端点（代理、第三方） |
| 本地服务 | `local` | `http://localhost:xxxx` | 本地部署的图像生成服务 |

### 重新配置

删除配置文件，下次使用时会自动重新启动配置向导：

```bash
rm ~/.claude/skills/luoboa-illustrate/config.json
```

也可以直接编辑配置文件。

---

## 工作原理

### 流程

```
Markdown 文章
    │
    ├── 解析标题（# 和 ##）
    │
    ├── 选择风格（12 种可选）
    │
    ├── 生成封面（1920×832）
    │
    ├── 生成章节插图（1024×1024）
    │       │
    │       └── 柔情风：传入参考图，保证人物外观一致
    │
    └── 在每个 ## 标题下方插入 ![](images/xx.png)
```

### 输出目录结构

```
article/0531/某篇文章/
├── 某篇文章.md
└── images/
    ├── 00-封面.png          （封面，不插入文章）
    ├── 01-第一个章节.png     （插入到 ## 第一个章节 下方）
    ├── 02-第二个章节.png
    └── ...
```

### 图片尺寸

| 类型 | 尺寸 | 用途 |
|------|------|------|
| 封面 | 1920×832（21:9） | 公众号封面缩略图 |
| 章节插图 | 1024×1024（1:1） | 正文中配图 |

### 品牌水印

品牌信息仅出现在"专业向"风格的封面上（科技风、蓝图风、赛博风、商务风、像素风）。情感和艺术类风格保持画面纯净。

当 `brand.enabled` 为 `false`（默认）时，所有风格均不添加水印。

---

## 各服务商 API 差异

| 特性 | `grsai` | `openai` / `openai-compatible` / `local` |
|------|---------|------------------------------------------|
| 封面端点 | `/v1/images/generations` | `/v1/images/generations` |
| 插图端点 | `/v1/draw/completions`（SSE 流式） | `/v1/images/generations` |
| 插图请求 | `aspectRatio` + `replyType: "async"` | `size: "1024x1024"` |
| 插图响应 | SSE 流 | 标准 JSON |

---

## 触发方式

以下任一说法都会激活技能：

- `给文章配图` / `配图` / `插图` / `封面`
- `生成插图` / `做封面`
- `/luoboa-illustrate`

---

## 系统要求

- **Claude Code**（CLI 或桌面版）
- **出图后端**（以下任一）：图像生成 API 密钥 或 本地安装的即梦 CLI
- **Python 3**（用于 API 调用，仅使用标准库，无需 pip install）

---

## 许可证

MIT
