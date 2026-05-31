# luoboa-illustrate

**[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)**

AI 驱动的微信公众号文章配图生成器。给它一篇 Markdown 文章，选一个风格，它就会自动生成封面 + 每个章节的插图，并插入回文章中。

**作为 [Claude Code](https://claude.ai/code) 自定义技能使用。**

---

## 功能特性

- 🎨 **12 种视觉风格** — 从暗黑科技风到水彩风，像素风到禅意极简
- 🖼️ **封面 + 章节插图** — 每个 `##` 标题生成一张配图，不只是封面
- 🔌 **多种后端** — OpenAI API、GRS AI、兼容端点、本地服务或 Dreamina CLI
- 🏷️ **可选品牌水印** — 一次配置，自动出现在合适的风格封面上
- 📝 **自动插入 Markdown** — 插图放置在对应标题下方
- 👤 **人物一致性** — 情感治愈风格通过传递参考图片，保持章节间人物一致

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

# 或开发模式使用符号链接
ln -s "$(pwd)/luoboa-illustrate" ~/.claude/skills/luoboa-illustrate
```

**卸载：**

```bash
npx skills remove luoboa-illustrate
```

</details>

### 2. 首次运行设置

首次触发技能时，设置向导会引导你完成：

1. **选择后端** — API 或 Dreamina CLI
2. **配置 API** — 选择提供商、输入密钥和地址
3. **品牌（可选）** — 名称、标语、logo URL、网站

配置保存在 `~/.claude/skills/luoboa-illustrate/config.yaml`。

### 3. 生成配图

在 Claude Code 中打开一篇 Markdown 文章，说：

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

| # | 风格 | 描述 | 适合场景 |
|---|------|------|---------|
| 1 | 🖥️ 科技风 | 暗黑对立构图 + Excalidraw 手绘草稿 | AI、工程、深度技术 |
| 2 | 💕 情感治愈风 | 温暖莫兰迪色调 + 人物一致性 | 故事、散文、生活方式 |

### 扩展风格（点击"更多"）

| # | 风格 | ID | 关键词 | 适合场景 |
|---|------|----|--------|---------|
| 3 | 📐 蓝图风 | `blueprint` | 蓝色网格、技术图纸 | 系统架构、工程 |
| 4 | ✏️ 手绘笔记风 | `sketch-notes` | 马卡龙色、手绘、温暖 | 教程、笔记、概念 |
| 5 | 📜 复古风 | `vintage` | 旧羊皮纸、棕褐色、古典 | 历史、传承、品牌故事 |
| 6 | 🌸 可爱风 | `kawaii` | 粉色系、圆润造型、粗线条 | 生活方式、宠物、休闲 |
| 7 | 🌆 赛博朋克风 | `cyberpunk-neon` | 深紫、霓虹光、故障感 | 未来科技、游戏、科幻 |
| 8 | 💼 商务风 | `corporate` | 白 + 灰 + 金、几何图形 | 商业、战略、分析 |
| 9 | 🍃 水彩风 | `watercolor` | 大地色系、有机笔触 | 旅行、养生、自然 |
| 10 | 🕹️ 像素风 | `pixel-art` | 8-bit、复古游戏、马赛克 | 游戏文化、复古科技 |
| 11 | 🎭 丝网印刷风 | `screen-print` | 大色块、网点、限色 | 时评、文化评论 |
| 12 | 🧘 禅意极简风 | `zen-minimal` | 大量留白、单条墨线 | 哲学、极简主义、禅意 |

---

## 配置

### 配置文件位置

```
~/.claude/skills/luoboa-illustrate/config.yaml
```

### 完整格式

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

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `backend` | `"api"` \| `"dreamina"` | 图片生成后端 |
| `api.provider` | 字符串 | `"grsai"` / `"openai"` / `"openai-compatible"` / `"local"` |
| `api.base_url` | 字符串 | API 基础地址（不带末尾斜杠） |
| `api.api_key` | 字符串 | API 认证密钥 |
| `api.model` | 字符串 | 模型名称（默认：`gpt-image-2`） |
| `brand.enabled` | 布尔值 | 是否在封面上显示品牌水印 |
| `brand.name` | 字符串 | 品牌显示名称 |
| `brand.tagline` | 字符串 | 品牌标语/口号 |
| `brand.logo_url` | 字符串\|空 | 品牌 logo 图片 URL |
| `brand.website` | 字符串 | 品牌网站 URL |

### 支持的 API 提供商

| 提供商 | ID | 基础地址 | 备注 |
|--------|-----|---------|------|
| GRS AI | `grsai` | `https://grsai.dakka.com.cn` | 国内 GPT-image-2 节点；插图使用 SSE |
| OpenAI | `openai` | `https://api.openai.com` | OpenAI 官方 API |
| 兼容端点 | `openai-compatible` | 用户自定义 | 任何 OpenAI 兼容端点（代理、第三方） |
| 本地服务 | `local` | `http://localhost:xxxx` | 自托管图片生成服务 |

### 重新配置

删除配置文件，下次使用时设置向导会重新运行：

```bash
rm ~/.claude/skills/luoboa-illustrate/config.yaml
```

或直接编辑该文件。

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
    │       └── 情感治愈风：传递参考图片
    │           保持人物一致性
    │
    └── 在每个 ## 标题下插入 ![](images/xx.png)
```

### 输出结构

```
article/0531/MyArticle/
├── MyArticle.md
└── images/
    ├── 00-cover.png          (封面，不插入文章)
    ├── 01-first-section.png  (插入到 ## 第一个章节 下方)
    ├── 02-second-section.png
    └── ...
```

### 图片尺寸

| 类型 | 尺寸 | 用途 |
|------|------|------|
| 封面 | 1920×832 (21:9) | 微信文章封面缩略图 |
| 章节插图 | 1024×1024 (1:1) | 文章正文配图 |

### 品牌水印

品牌信息仅出现在"专业"风格（科技风、蓝图风、赛博朋克、商务风、像素风）的封面上。情感和艺术风格保持纯净画面。

当 `brand.enabled` 为 `false`（默认）时，所有风格均不添加水印。

---

## API 提供商差异

| 特性 | `grsai` | `openai` / `openai-compatible` / `local` |
|------|---------|------------------------------------------|
| 封面端点 | `/v1/images/generations` | `/v1/images/generations` |
| 插图端点 | `/v1/draw/completions`（SSE） | `/v1/images/generations` |
| 插图请求 | `aspectRatio` + `replyType: "async"` | `size: "1024x1024"` |
| 插图响应 | SSE 流 | 标准 JSON |

---

## 触发方式

以下任意说法均可激活技能：

- `给文章配图` / `配图` / `插图` / `封面`
- `生成插图` / `做封面`
- `/luoboa-illustrate`

---

## 系统要求

- **Claude Code**（CLI 或桌面版）
- **以下之一**：图片生成 API 密钥 或 本地安装的 Dreamina CLI
- **Python 3**（用于 API 调用 — 仅使用标准库，无需 pip install）

---

## 👤 关于作者

**萝卜啊** — AI 实践派，只写亲身验证过的内容。

🌐 **个人博客**：[www.luoboa.com](https://www.luoboa.com)

最新的 AI 技术文章、工具推荐、Skill 和 MCP 精选，每日更新。

📱 **微信公众号**：关注获取独家资料

![公众号二维码](assets/qrcode.jpg)

公众号内容：

- ✅ 亲身验证过的 **AI 用法**，不是搬运
- ✅ **Agent 面试题思路**，来自真实面试场景
- ✅ **公司 AI 落地**的实在经验，不画饼

📌 回复关键词直接领取资料（无转发套路）：

| 关键词 | 资料内容 |
|--------|---------|
| **技巧** | AI 提升效率实战技巧 |
| **Agent** | Agent 面试备战指南 |
| **转型** | 公司 AI 落地转型方案 |

📅 **更新节奏**：

| 日期 | 内容 |
|------|------|
| 周一至周五 | Claude Code 最佳实践一篇 + AI 最佳开源 Agent/Skill 一篇 |
| 周六 | 本周 AI 快讯 + GitHub 最佳榜单 |
| 周日 | AI Agent 领域最佳实践 |

### 🔗 社交平台

| 平台 | 链接 |
|------|------|
| 🐙 GitHub | [github.com/opapa](https://github.com/opapa) |
| 📘 知乎 | [zhihu.com/people/opapar](https://www.zhihu.com/people/opapar) |
| 📺 B站 | [space.bilibili.com/316828422](https://space.bilibili.com/316828422) |
| ▶️ YouTube | [youtube.com/@ailuoboa](https://www.youtube.com/@ailuoboa) |

---

## 许可证

MIT
