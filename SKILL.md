---
name: luoboa-illustrate
description: Generate illustrations for WeChat public account articles (公众号配图) using image generation APIs or Dreamina CLI, then insert them into the article markdown file. 17 styles available: 科技风 (Excalidraw) / 柔情风 / 怀旧照片 / 美食 / 旅行 / 萌宠Q版 / 家居 / 时尚 / ACG二次元 / 测评信息图 / 运动 / 快文 / 微头条 / 知乎文配图 (白底黑字流程图统计图) / 小黑科普 (Ian 怪诞手绘+小黑 IP, 默认 API 出图) / **轻量涂鸦Q版 (#17, 草根手绘+Q版角色+涂鸦,非日漫/非韩漫/非萌系,委派 baoyu-article-illustrator)** / 额外扩展. Use this skill whenever the user wants to create illustrations, images, or cover art for their articles, or mentions 配图/插图/封面/快文配图/快文/视频素材/知乎/白底黑字/流程图/统计图/涂鸦/手绘Q版/轻量涂鸦 for articles. Also trigger when the user asks to "给文章配图", "生成插图", "做封面", "快文配图", "按句配图", "配个知乎风的图", "做白底黑字流程图", "做个涂鸦Q版".
---

# WeChat Article Illustrator

Generate cover and section illustrations for WeChat public account (公众号) articles. One image per `##` heading, plus a cover.

## First-Run Setup

On first use, check if `config.yaml` exists in the skill directory. If not, run a setup wizard:

1. **Choose backend** — API (default, 出图质量更好) or Dreamina CLI (API不可用时的备选)
2. **Configure API** (if API chosen, 默认):
   - Ask: "Which provider?" Show options: GRS AI / OpenAI / OpenAI-Compatible / Local
   - Collect: base URL (pre-fill default per provider), API key, model name
3. **Configure Dreamina** (if Dreamina chosen):
   - Check if `dreamina` CLI is in PATH (`which dreamina`)
   - If not found, tell user: "Install dreamina CLI and run `dreamina login` first"
   - Verify login: `dreamina user_credit`
4. **Brand (optional)** — Ask: "Want to add brand watermark?" If yes, collect: name, tagline, logo URL, website
5. Save to `config.yaml`

### Config schema

```yaml
backend: api # api (default) / dreamina

api:
  provider: openai # grsai / openai / openai-compatible / local
  base_url: https://api.openai.com
  api_key: sk-xxxx
  model: gpt-image-2

brand:
  enabled: false
  name: ""
  tagline: ""
  logo_url: null
  website: ""

dreamina:
  enabled: true
  cli_path: "" # auto-detected from PATH if empty
  ratio_cover: "21:9"
  ratio_section: "1:1"
  resolution: "2k"
  poll_timeout: 60
```

### Provider defaults

| Provider            | base_url default             | Notes                                     |
| ------------------- | ---------------------------- | ----------------------------------------- |
| `grsai`             | `https://grsai.dakka.com.cn` | China node, SSE for illustrations         |
| `openai`            | `https://api.openai.com`     | Official OpenAI                           |
| `openai-compatible` | (user must provide)          | Proxies, third-party                      |
| `local`             | (user must provide)          | Self-hosted, e.g. `http://localhost:8080` |

### Re-configure

Tell user: "Delete config.yaml and the wizard runs again next time, or edit it directly."

```bash
rm ~/.claude/skills/luoboa-illustrate/config.yaml
```

## 🎨 风格速查（Style Cheat Sheet）— 解决"风格太多乱"的问题

**整个 skill 有 18 个风格 + 4 个科技子风格（TA-X）+ 7 个科技 section 变体（TS-X）**。直接看下面 3 张表，再翻详细章节。

### 表 1：18 个一级风格（按 Workflow 字母排序）

| # | 风格 | 一句话定位 | 触发关键词 |
|---|------|----------|----------|
| 1 | 🖥️ **科技风** (Workflow A) | 工程师白板 Excalidraw 手绘 | 科技、Claude Code、Agent、Vibe Coding、教程、面试 |
| 2 | 💕 **柔情风** (Workflow B) | 莫兰迪温暖治愈 | 情感、晚安、爱情、亲情 |
| 3 | 📷 **怀旧照片风** (Workflow E) | 90 年代胶片暖调 | 回忆、奶奶、童年、乡愁 |
| 4 | 🍜 **美食风** (Workflow F) | 暖光食物特写 | 探店、食谱、咖啡、烘焙 |
| 5 | 🗺️ **旅行城市风** (Workflow G) | 现代写实风景 | 旅行、citywalk、城市攻略 |
| 6 | 🐾 **萌宠Q版风** (Workflow H) | 拟人宠物 | 萌宠、亲子、表情包 |
| 7 | 🏠 **家居生活风** (Workflow I) | MUJI/北欧样板间 | 装修、家居、好物 |
| 8 | 💄 **时尚美妆风** (Workflow J) | 时尚杂志摄影 | 穿搭、lookbook、护肤 |
| 9 | 🎮 **ACG 二次元** (Workflow K) | 日式赛璐璐/原神风 | 番剧、手游、cosplay |
| 10 | 📊 **测评信息图** (Workflow L) | 评分卡/对比/雷达图 | 横评、3C、榜单 |
| 11 | 🏃 **运动健身风** (Workflow M) | 高速运动摄影 | 健身、马拉松、装备 |
| 12 | 🎨 **通用风格** (Workflow C) | 12 种扩展风格 | Blueprint/Cyberpunk/Pixel/... |
| 13 | ⚡ **快文配图** (Workflow D) | 8-bit 极客像素黑白 | 每句一图、抖音、卡片 |
| 14 | 📰 **微头条配图** (Workflow N) | 马克笔 Q 版卡通 | AI 快讯、新闻、资讯 |
| 15 | 📐 **知乎文配图** (Workflow Z) | 白底黑字 + 流程图/统计图 | 知乎、白底黑字、数据驱动、流程图 |
| 16 | 🐾 **小黑科普** (Workflow X) | Ian 怪诞手绘 + 小黑 IP | 概念、机制、隐喻、判断 |
| 17 | ✏️ **涂鸦Q版** (Workflow Q) | 草根手绘 Q 版 | 手绘 Q 版、不要日漫 |

**怎么选**：先用 `触发关键词` 匹配到 1-3 个候选 workflow → 然后翻该 workflow 的详细章节看 prompt 模板。

### 表 2：科技类 4 个 Banner 风格（TA-X）— **容易乱的根源**

科技文封面有 4 个备选，**TA-D 是 default**：

| 维度 | TA-A 数字终端 | TA-B 电路图腾 | TA-C 数据看板 | **TA-D 白底 Excalidraw** ⭐ |
|---|---|---|---|---|
| **看图想象** | 黑客帝国暗色终端 | 硬件工程师 PCB 蓝图 | 麦肯锡咨询报告 | 工程师在白板上随手画 |
| **背景色** | 深 navy `#0D1B2A` | 米白 `#F0F4F8` | 纯白 `#FFFFFF` | **纯白 `#FFFFFF`** |
| **主色** | cyan `#4D96FF` | 炭黑 + cyan | 知乎蓝 `#056DE8` | **深灰 + 蓝 + 黄 Excalidraw** |
| **渲染** | clean-digital（锐利矢量） | hand-drawn（草根手绘） | flat-vector（咨询风） | **hand-drawn（白板手绘）** |
| **字体** | display 粗体 | clean 衬线 | clean 衬线 | **display 粗体装饰** |
| **情绪** | bold（高对比） | balanced | subtle | **balanced** |
| **跟插图共享 3 维？** | ❌ 完全不共享 | ⚠️ 共享 rendering | ⚠️ 共享 palette | ✅ **完全共享** |
| **适合** | 工具/教程 | 硬件/电路 | 咨询/数据 | **99% 科技文** |

**核心规则（口诀）**：

> **封面必须跟正文插图共享 Palette + Rendering + Mood 3 维**（5 维一致性）。
> 正文插图 7 个变体（TS-A~TS-G）**全部是白底 Excalidraw**。
> 所以 **只有 TA-D 跟它们共享 3 维** → **TA-D 是 default**。
> TA-A/B/C 是"特殊备选"——只有当你**整篇文章所有图**（封面 + 每张插图）都统一走对应风格时才能用。

**决策树**：

```
问：科技文要出 banner，选哪个 TA-X？
├─ 99% 情况 → TA-D（白底 Excalidraw，最稳）
├─ 整篇都走暗色 cyberpunk 风 → TA-A
├─ 整篇都走 PCB 硬件风 → TA-B
└─ 整篇都走咨询报告风 → TA-C
```

### 表 3：科技类 7 个 Section 变体（TS-X）— 给 subagent 选哪种可视化

| # | 变体 | 适用场景 | 必含具象元素 | 跟 TA-D 共享？ |
|---|------|---------|---------|---------|
| **TS-A** | 流程图 | 步骤、流程、因果链 | 1 人物 + 1 工具/文件 | ✅ |
| **TS-B** | 概念关系图 | 影响因素、节点连接 | 1 拟人化动物 + 节点 | ✅ |
| **TS-C** | 系统架构图 | 模块依赖、技术栈分层 | 1 服务器/电脑/数据库 | ✅ |
| **TS-D** | 线框图 | UI 界面、产品流程 | 1 工程师用 UI + 设备 | ✅ |
| **TS-E** | 时间线/里程碑 | 版本演进、关键事件 | 1 人物 + 1 关键物件 | ✅ |
| **TS-F** | 决策树/分支图 | 条件分支、trade-off | 1 思考中人物 + 问号/灯泡 | ✅ |
| **TS-G** | 🆕 人物场景图 | 故事开头、概念具象化、对话 | 1 人物 + 1 巨型概念物 + 1 场景物（3 件套）| ✅ |

**决策树**：

```
问：科技文某段要配图，选哪个 TS-X？
├─ 故事开头 / 人物对话 / 场景描述 → TS-G
├─ 纯步骤 / 流程拆解 → TS-A
├─ 概念关系 / 影响因素 → TS-B
├─ 系统架构 / 模块依赖 → TS-C
├─ UI 草图 / 产品界面 → TS-D
├─ 版本演进 / 时间阶段 → TS-E
└─ 决策 / 分支 / trade-off → TS-F
```

### 表 4：18 风格 → 推荐后端（API vs Dreamina CLI）

| 风格 | 默认后端 | 备注 |
|------|---------|------|
| 科技 (Workflow A) | API（grsai）| 5 维一致 + 中文手写稳 |
| 情感 (Workflow B) | API | 人物一致性要 ref-url |
| 怀旧 (Workflow E) | Dreamina CLI | 写实风 + 暖调 v50 稳 |
| 美食/旅行/萌宠/家居/时尚/ACG/测评/运动 (F-M) | API | 写实摄影 gresai 强 |
| 通用 (C) | API | 看具体风格 |
| **快文 (D)** | **Dreamina CLI v50** | 8-bit 像素 v50 专用，4.7 偏 Q 版冲突 |
| **微头条 (N)** | **Dreamina CLI v50** | Q 版马克笔 v50 专用 |
| **知乎 (Z)** | **API** (🆕 2026-06-08 改) | 白底矢量信息图 API 稳 |
| **小黑科普 (X)** | **API** | 小黑 IP 一致性 API 强 |
| 涂鸦Q版 (Q) | API（grsai） | 委派给 baoyu-article-illustrator |

### 表 5：风格选择的"反向避坑"清单

- ❌ 科技文 + 怀旧照片风（= 工程师故事用 90 年代胶片，错位）
- ❌ 情感文 + 知乎文配图（= 莫兰迪用流程图，错位）
- ❌ 美食文 + 8-bit 像素（= 暖光食物用黑白像素，错位）
- ❌ 科技文 + TA-A 暗色 banner + 白底 Excalidraw 插图（= 调色板不共享，破坏 5 维一致性）
- ❌ 二次元 + 写实摄影（= 番剧推荐用真人照，错位）

---

## Workflow

### Step 1: Read Article Structure

Read the target `.md` file. Extract:

- Article title (the `# ` heading, or filename)
- All section headings (every `## ` subheading, in order)
- Full content of each section (for generating relevant prompts)

### Step 2: Style Selection

Ask the user to pick a style. Show primary choices first:

| #   | 风格           | 一句话描述                                                                                                        |
| --- | -------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1   | 🖥️ 科技风      | 白底 Excalidraw 手绘草稿 + 不规则手绘线条 + 技术人气质                                                              |
| 2   | 💕 柔情风      | 温暖治愈莫兰迪 + 人物一致性                                                                                       |
| 3   | 📷 怀旧照片风  | 90年代写实胶片质感 + 夕阳光/暖黄灯光 + 温暖泛黄                                                                   |
| 4   | 🍜 美食风      | 暖光食物特写 + 蒸汽/拉丝/俯拍构图                                                                                 |
| 5   | 🗺️ 旅行城市风  | 现代写实风景 + 城市夜景/航拍/季节感                                                                               |
| 6   | 🐾 萌宠Q版风   | 拟人/治愈/Q版宠物插画                                                                                             |
| 7   | 🏠 家居生活风  | 样板间/MUJI/北欧/户型图                                                                                           |
| 8   | 💄 时尚美妆风  | 产品摄影 + 人物一致性 + 妆容/服装特写                                                                             |
| 9   | 🎮 ACG二次元风 | 日式赛璐璐/原神风/Q版角色                                                                                         |
| 10  | 📊 测评信息图  | 结构化信息图 + 评分卡 + 对比图                                                                                    |
| 11  | 🏃 运动健身风  | 动态/汗水/球场跑道                                                                                                |
| 12  | 🎨 更多风格... | 查看额外扩展风格（Blueprint/Cyberpunk/Pixel Art/Sketch Notes/Vintage/Kawaii/Watercolor/Screen Print/Zen Minimal） |
| 13  | ⚡ 快文配图    | 按句生成9:16竖图，即梦渲染文字，视频素材                                                                          |
| 14  | 📰 微头条配图  | 每条新闻生成9:16马克笔 Q 版卡通                                                                                   |
| 15  | 📐 知乎文配图  | 白底黑字 + 极少量蓝/橙强调 + 流程图/统计图/知识图谱/线框图 + Tufte 高 data-ink ratio，专业数据驱动风格        |
| 16  | 🐾 小黑科普   | Ian 怪诞手绘 + 小黑 IP + 纯白底 + 少量红/橙/蓝批注 + 全新原创隐喻，适合技术/概念/科普文；**默认 API 出图**（不走 Dreamina CLI）|
| 17  | ✏️ 轻量涂鸦Q版 | 草根手绘 + 圆润Q版角色 + 涂鸦风格（**非日漫、非韩漫、非萌系**）。区别于 #6 萌宠Q版（限定宠物主体）、#9 ACG二次元（日式赛璐璐/原神风）、#5 sketch-notes（笔记本 Macaron 风）。定位：**非亚洲漫感的"草根 Q版"**——给人物/概念/品牌，**出图时委派给 `baoyu-article-illustrator`**。 |

If user picks 1 → Workflow A (科技类)
If user picks 2 → Workflow B (情感治愈类)
If user picks 3 → Workflow E (怀旧照片类)
If user picks 4 → Workflow F (美食类)
If user picks 5 → Workflow G (旅行城市类)
If user picks 6 → Workflow H (萌宠Q版类)
If user picks 7 → Workflow I (家居生活类)
If user picks 8 → Workflow J (时尚美妆类)
If user picks 9 → Workflow K (ACG二次元类)
If user picks 10 → Workflow L (测评信息图类)
If user picks 11 → Workflow M (运动健身类)
If user picks 17 → **Workflow Q (轻量涂鸦Q版类)** — 草根手绘 + 圆润Q版角色 + 涂鸦风格。**委派到 `/baoyu-skills/baoyu-article-illustrator`** sub-skill 完成（同 Workflow A 的"强制委派 banner"模式）。**非日漫/非韩漫/非萌系**——避免和 #6/9 撞。
If user picks 12 → show extended catalog from `references/style-guide.md`
If user picks 13 → Workflow D (快文配图)
If user picks 14 → Workflow N (微头条配图)
If user picks 15 → **Workflow Z (知乎文配图)** — see "Workflow Z: 知乎文配图" section below
If user picks 16 → **Workflow X (小黑科普 / Ian 怪诞手绘)** — see "Workflow X: 小黑科普" section below

Also trigger Workflow D directly when user says "快文配图"/"快文"/"视频素材"/"按句配图".
Also trigger Workflow D when user mentions "横屏"/"竖屏"/"16:9"/"9:16"/"封面"/"banner" etc. — these are common video/post requirements that aren't always vertical.
Also trigger Workflow E directly when user says "怀旧照片"/"怀旧风"/"老照片"/"90年代照片"/"胶片风".
Also trigger Workflow N directly when user says "微头条配图"/"新闻配图"/"资讯配图"/"AI快讯配图".
Also trigger **Workflow Z (知乎文配图)** directly when user says: `知乎`/`知乎文`/`知乎风格`/`Zhihu`/`白底黑字`/`白底`/`极简`/`专业`/`数据驱动`/`学术风`/`咨询风`/`流程图`/`flowchart`/`统计图`/`柱状图`/`折线图`/`chart`/`信息图`/`infographic`/`线框图`/`wireframe`/`知识图谱`/`技术文`/`科普文`/`分析报告`/`数据可视化`. Cover + 6 变体插图（流程图/柱状图/折线图/知识图谱/对比表/线框图）的完整 prompt 模板见 `references/style-guide.md` 末节 "知乎文配图风格"。

> 🆕 **冲突触发时的二选一询问**（2026-06 加）：当用户同时说 `技术文`/`科普文`/`分析报告`/`知乎` **和** `概念/机制/隐喻/对比/判断/收束` 这类关键词，**先 AskUserQuestion 问选 Workflow Z 还是 Workflow X**（详见 Workflow X 段）。默认推荐：数字/统计/流程 → Z；概念/隐喻/判断 → X。

Also trigger **Workflow X (小黑科普 / Ian 怪诞手绘)** directly when user says: `小黑`/`小黑科普`/`Ian`/`怪诞手绘`/`小黑插图`/`小黑配图`/`Ian 风格`/`小黑图`/文章里有"机制/概念/隐喻"等需要翻译的判断. 走 API 出图（`scripts/generate.py`），委派到 `~/.claude/skills/ian-xiaohei-illustrations/`.

### Step 3: Generate Images

**默认提示词语言：中文。** 如果用户没特别强调，**所有 prompt 都用中文写**（grsai/dreamina 都能识别中文 prompt）。如果用户写了"用英文 prompt"或"英文"才用英文。

**⚠️ 中文 prompt + 中文文字渲染（硬性要求，覆盖全 skill）：**
- **prompt 主体用中文写**——场景、风格、画面元素、人物动作、情绪描述全部用中文
- **技术约束可以英文**——比如 "NOT oil paint, NOT 3D" 这类风格负面词用英文
- **所有图中的中文文字必须清晰渲染**（标题、副标、品牌、关键词高亮）——在 prompt 里用 `'文字内容'` 明确写出要渲染的中文 + `Chinese text 'X' must be sharp legible` 强化
- **特别强调科技类（Workflow A）**：公众号 banner 一定要渲染中文标题（公众号编辑器不会帮你叠层），不能等用户后期 PS

**后端选择：必须问用户。** 不再默认走 API。Step 3 之前要先问："用 **API**（grsai，质量好）还是 **Dreamina CLI**（快+中文稳）？"

#### 方案一：API（grsai）

Use the `scripts/generate.py` script. It reads config from `config.yaml`.

**Cover image:**

```bash
python scripts/generate.py cover \
  --prompt "<中文 cover prompt>" \
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

**API 故障降级：** 如果 API 返回 `excessive system load` 或连续 400 错误，自动切换到 Dreamina CLI 方案重试。

#### 方案二：Dreamina CLI（API不可用时的备选）

检查 `dreamina` 是否可用：

```bash
which dreamina   # 或 where dreamina (Windows)
```

**Cover image (21:9):**

```bash
dreamina text2image \
  --prompt="<cover prompt>" \
  --ratio=21:9 \
  --resolution_type=2k \
  --poll=60
```

返回 JSON 中 `result_json.images[0].image_url` 即为图片 URL，用 `curl -sL "<url>" -o "images/00-cover.png"` 下载保存。

**Section illustration (1:1):**

```bash
dreamina text2image \
  --prompt="<section prompt>" \
  --ratio=1:1 \
  --resolution_type=2k \
  --poll=60
```

**批量生成技巧：**

- 多个 section 可以并行提交（多个 `dreamina text2image` 同时跑），然后用 `dreamina query_result --submit_id=<id>` 逐个获取结果
- 生成失败时：调整 prompt 重试一次，如果仍然失败跳过该 section 继续下一个

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

## ⛔ 全局硬约束：Banner 比例 + 艺术性验收（2026-06-06 起）

**所有 banner（cover）必须满足以下 3 条，缺一不可**：

1. **比例 = 21:9**（即 1920x832 / 3024x1296 / 2560x1080）
   - API 调用显式传 `--ratio "21:9"` 或 `--aspect-ratio "1920x832"`
   - 生成后用 PIL.Image 校验 `width/height ∈ [2.2, 2.45]`
   - 比例不合格 → 重试到合格为止，**禁止静默接受 1:1 / 1.5:1 / 3:4 等任何非 21:9 比例**

2. **艺术大字排版（typography-dominant）**
   - 标题占画面 40-70% 视觉权重
   - 标题字号 220-340px 视觉高度
   - 字体必须显式指定（display/serif/clean/handwritten），并在 prompt 末尾加 `Font Application` 段
   - **不接受的素面**：纯色背景+小标题、纯渐变+角落文字、单图+小字水印

3. **艺术性视觉锚点**
   - 至少有 1 个明显的视觉符号 / 元素组合（终端光晕、电路图腾、数据看板、墨迹笔触、夕阳光斑、麦穗剪影、窗棂投影等）
   - **不接受纯色填充 + 文字 + 装饰条**——必须有"画面感"

### 🆕 强制委派：Banner 必须先调 `/baoyu-skills` 里的 `/baoyu-cover-image` 做设计分析（2026-06-06 加）

> **`/baoyu-cover-image` 是 `/baoyu-skills` 仓库里专门做封面/banner 的子 skill**（仓库地址 https://github.com/JimLiu/baoyu-skills），包含 5 维排版、4 种字体、8 种花字技法、Type × Style × Palette 三维体系，是目前中文封面/banner 出图质量天花板的方法论。**任何 banner / cover 在落 prompt 之前，必须先委派给它做完整的设计分析**，不要自己拍脑袋写 prompt。

**触发条件**（满足任一即触发）：

- Workflow 包含 21:9 banner / cover（公众号、知乎专栏、网页 banner、播客封面）
- 文章类型为 公众号深度文 / 36kr / 钛媒体 / 知乎专栏 / 技术博客（这些都需要封面图）
- 用户提到「封面」「banner」「cover」「公众号头图」

**委派步骤**（按顺序执行，不可跳）：

1. **调用 `/baoyu-cover-image` 分析文章主题**
   - 让它读文章 + 输出 `Type × Style × Palette` 三维推荐
   - 拿到推荐后**不要照搬**，而是融合到本 skill 的 `5 维一致性体系`（Type × Palette × Rendering × Font × Mood）

2. **调 `/baoyu-cover-image` 的字体表和花字技法表**
   - 让它根据文章类型推荐具体字体（clean/handwritten/serif/display）
   - 让它根据风格推荐 1-2 种花字技法（gradient/stroke-text/shadow-3d/highlight/neon/handwritten/bubble/brush）
   - 把这两个推荐直接写进本 skill 的 banner prompt 末尾 `Font Application` 段

3. **复用 `/baoyu-cover-image` 的"5 维默认参数"**
   - 它输出的 `Palette` 配色 + `Style` 渲染风格 = 本 skill 的 `Palette × Rendering` 两维
   - 直接拷过去，不要自己重选

4. **设计分析完成后再进入本 skill 的 Step 3 出图**
   - 用 `python scripts/generate.py cover --prompt=... --ratio=21:9`（API）
   - 或 `dreamina text2image --ratio=21:9 --model_version=4.6`（Dreamina CLI）
   - 出图后用 ⛔ 三条硬约束校验（21:9 比例、artistic typography、视觉锚点）

**伪代码**：

```text
if workflow needs banner/cover:
    analysis = invoke_skill("/baoyu-cover-image", args={  # 来自 baoyu-skills
        "article": article_text,
        "article_type": "公众号深度文" / "知乎专栏" / "36kr" / ...,
        "output": "5维推荐 + 字体推荐 + 花字推荐 + Palette"
    })
    banner_prompt = build_with_5dims(article, analysis)  # 本 skill 的 5 维
    banner_prompt += build_font_application(analysis.font, analysis.typography)  # 来自 baoyu
    image = generate(banner_prompt, ratio="21:9")
    assert(image.width / image.height in [2.2, 2.45])  # 比例硬约束
    assert(has_visual_anchor(image))  # 视觉锚点硬约束
```

**关于 `/baoyu-skills` 仓库**（外部依赖）：

- 仓库地址：https://github.com/JimLiu/baoyu-skills
- **是一个大型 multi-skill 项目**，包含非常多子 skill（十几个，按图片处理 / 文档转换 / 内容发布 / 平台对接等不同场景组织）。**`baoyu-*` 名字会随时间增长**——任何时候都可以用"ls `~/.claude/skills/baoyu-skills/`"扫一下，看看新增了什么。
- 本 skill **不硬编码"只用这 N 个"**，而是**按 workflow 需求动态委派**：扫一下 `~/.claude/skills/baoyu-skills/` 下装了什么，再按"需求 → 候选 sub-skill"的映射挑最合适的。

**动态委派矩阵**（按"workflow 需要什么 → 哪些 baoyu-* sub-skill 能提供"列出）：

| Workflow 需要 | 候选 sub-skill（按优先级） |
|---------------|--------------------------|
| 21:9 banner / 封面设计分析（5 维排版 + 字体 + 花字） | **`/baoyu-cover-image`** （强制）→ 没有则用本 skill 内置 12 种 A-L 排版 |
| Balanced 多区布局（小红书 / 信息图 / 微信图文） | `/baoyu-xhs-images` |
| 高密度信息大图（21 布局 × 22 风格） | `/baoyu-infographic` |
| 知识漫画 / 人物传记漫画 | `/baoyu-comic` |
| 文章长图（杂志风） | `/baoyu-article-illustrator` |
| Markdown → 公众号兼容 HTML | `/baoyu-markdown-to-html` |
| 文章转视频 | `/baoyu-article-to-video`（如有） |
| Slide / PPT 出图 | `/baoyu-slide-deck` |
| 后端 API 出图（grsai/openai/...） | `/baoyu-image-gen`（可替本 skill 的 `scripts/generate.py`）|
| Diagram / 流程图 SVG | `/baoyu-diagram` |
| 翻译 | `/baoyu-translate` |
| 发布到微信 / 微博 / X | `/baoyu-post-to-wechat` / `/baoyu-post-to-weibo` / `/baoyu-post-to-x` |
| 微信群聊摘要 | `/baoyu-wechat-summary` |
| 压缩图片 | `/baoyu-compress-image` |

**执行规则**：

1. **每次触发本 skill**，先扫 `~/.claude/skills/baoyu-skills/`（用 `ls` 或 `Glob`），得到当前实际可用的 sub-skill 列表
2. 按"workflow 需要"匹配候选 sub-skill，**只对匹配到的做委派**（不浪费 token 调无关 skill）
3. 匹配不到的 sub-skill → 跳过委派，走本 skill 内置 fallback（`references/style-guide.md` + `references/quick-styles.md` + `references/news-styles.md`）
4. 委派时**只传"需要它做什么"，不要让 sub-skill 抢本 skill 的整体 workflow 控制权**——它应该是"被叫来帮忙的专家"，不是"接管者"
5. 委派完成后，把 sub-skill 的输出**融合到本 skill 的 5 维一致性体系**（Type × Palette × Rendering × Font × Mood），不要让两套体系打架

**安装方式**（覆盖全 sub-skill）：

```bash
git clone https://github.com/JimLiu/baoyu-skills ~/.claude/skills/baoyu-skills
```

也可以只 clone 单个 sub-skill 子目录（如果只想用一两个）。子 skill 目录名直接作为 `Skill` 工具的 `skill` 参数（如 `skill: "baoyu-cover-image"`）。

**Fallback 行为**：如果 `/baoyu-skills` 整个未安装，使用本 skill 内置的 `references/style-guide.md` 中"封面排版"章节的 12 种排版风格 A-L + `references/quick-styles.md` + `references/news-styles.md` 兜底。在 setup wizard 中检查依赖时，主动提示用户安装 `/baoyu-skills` 以获得最佳封面/布局/漫画/翻译等能力。

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

## 全局规则：风格一致性

**同一篇文章的所有图片（封面 + 插图）必须共享相同的视觉词汇。**

5维体系定义了 Type/Palette/Rendering/Font/Mood 五个维度。封面用全部5维，插图继承其中3维：

| 维度                      | 封面 | 插图            | 说明                                                                 |
| ------------------------- | ---- | --------------- | -------------------------------------------------------------------- |
| Type（构图类型）          | ✅   | ❌              | 插图无大字排版                                                       |
| **Palette（色板）**       | ✅   | ✅ **必须继承** | 同一套hex色值                                                        |
| **Rendering（渲染方式）** | ✅   | ✅ **必须继承** | painterly就全painterly，digital就全digital，film grain就全film grain |
| Font（字体）              | ✅   | ❌              | 插图无文字                                                           |
| **Mood（情绪对比度）**    | ✅   | ✅ **必须继承** | subtle就全subtle，bold就全bold                                       |

**执行方式：** 生成封面后，将封面prompt中的 Palette/Rendering/Mood 三个维度参数原样写入每张插图的prompt。不允许封面painterly+插图photography，或封面duotone+插图全彩。

**具体例子：**

- 封面选了 A 日系电影感（painterly/warm/subtle）→ 插图prompt必须包含 "soft watercolor wash textures, visible brush strokes" + "cream #FFFAF0, golden yellow #F6AD55" + "low contrast, muted desaturated"
- 封面选了 G 王家卫式（digital/duotone/bold）→ 插图prompt必须包含 "clean precise edges, frosted glass effects" + "crimson #DC143C and navy #0D1B2A" + "high contrast, vivid saturated"
- 封面选了 H 拍立得底栏（hand-drawn/warm/subtle）→ 插图prompt必须包含 "sketchy organic strokes, variable marker line weight" + "cream #FFFAF0, golden yellow #F6AD55" + "low contrast, muted warm tones"

**同样适用于 Workflow F-M（美食/旅行/萌宠/家居/时尚/ACG/测评/运动）**：每种风格的 5 维默认参数已在各自 Workflow 章节明确定义，插图 prompt 必须以 `"Consistent with cover: [palette], [rendering], [mood]"` 开头。涉及真人/角色的风格（Workflow H/J/K）从第 2 张插图起必须传 `--ref-url` 保持一致性。

---

## Workflow A: 科技类

- Cover: **5维艺术大字排版**（参考 baoyu-cover-image 体系）—— 标题是画面视觉主角，占 40-70% 区域，**不是角落小字**。**🆕 2026-06-08 起 4 种风格：TA-D 白底 Excalidraw（default）** + TA-A/B/C 3 种特殊场景备选（见下方）。prompt 模板完整版见 `references/style-guide.md` "科技公众号 banner" 章节。
- Sections: **白底 Excalidraw 手绘草稿（whiteboard excalidraw sketch）** —— 2026-06-06 用户确认改为手绘草稿风（之前是"白底信息图"那种麦肯锡/TED-Ed 报告感）。现在要求"技术人气质"：白纸感 + 不规则手绘线条 + 轻微 jitter/wobble + 偶发擦除/重叠痕迹，像开发者在白板/Miro 上随手画的草图。6 种变体见下方"科技插图 6 变体"章节。完整 prompt 模板见 `references/style-guide.md` "科技插图 - 白底 Excalidraw 手绘" 章节。
- **风格一致性**：封面 typography-dominant（4 选 1，**TA-D 白底 Excalidraw default**）+ 插图 6 变体（6 选 1）共享 Palette（excalidraw 调色板）+ 手绘渲染方式。
- **⚠️ 科技类必出中文标题**：banner 一定要把中文标题直接渲染在画面里（不是后期叠层），公众号编辑器不会帮你加字。在 prompt 里写：`Chinese title '【公众号】[标题]' must be sharp legible`
- **⚠️ 配色硬性约束（白底 Excalidraw 调色板，2026-06-06 起）**：
  - **白底纯白 `#FFFFFF`** 为主，禁止暗色/灰底/渐变/纹理
  - **主线条深灰 `#2D2D2D`** 或近黑 `#1A1A1A`（Excalidraw 默认主色）
  - **高亮 Excalidraw 蓝 `#4D96FF`** 或 `#056DE8` 知乎蓝（强调当前节点/主线）
  - **黄色填充 `#FFD93D` 透明度 40%** 用于高亮某个 box
  - **极少量暖橙 `#F4A261` / 紫红 `#9B59B6`** 用于"另一种"高亮(避免抢主蓝)
  - **不出现纯红 `#FF0000`** —— Excalidraw 风本身不用红警示,改用主蓝/黄代替

### 科技插图 6 变体（白底 Excalidraw 手绘草稿，2026-06-06 起强制 default）

**风格定位（用户 2026-06-06 确认）**：

- ❌ **不用"白底信息图"那种麦肯锡/TED-Ed 报告感** —— 太规整、缺技术人气质
- ❌ **不用"暗色 Excalidraw"白板感** —— 太素、配色死板
- ✅ **用"白底 Excalidraw 手绘草稿"** —— 想象一个工程师在白板/Miro 上随手画的草图:白纸、黑色手绘线条、轻微 wobble、圆角矩形略带不齐、箭头有手抖感、关键 box 用半透明黄/蓝高亮。**重点是"像人手画的",不是"AI 矢量画的"**

**跟 Workflow Z 知乎白底信息图的关键区别**：

| 维度 | WF-A 科技 Excalidraw | WF-Z 知乎白底信息图 |
|---|---|---|
| 目标 | 公众号科技文内文配图 | 知乎高赞回答内文配图 |
| 气质 | 工程师随手画的草图,白板/Miro 感 | 麦肯锡/TED-Ed 报告,Tufte data-ink |
| 渲染 | hand-drawn sketch + 轻微 wobble | clean-digital 矢量 + 锐利描边 |
| 元素 | 手绘 box、圆圈、连接线,允许不齐 | 精确对齐的 box、轴、刻度 |
| 6 变体 | 流程/概念/架构/线框/时间线/分支 | 流程/柱状/折线/图谱/对比表/线框 |

| # | 变体 | 适用场景 | 5维映射 | 必含具象元素（≥1） |
|---|------|---------|---------|------------------|
| **TS-A** | 流程图（default） | 步骤说明、流程拆解、因果链 | whiteboard/hand-drawn/excalidraw/wobbly/balanced | 1 人物 + 1 工具/文件 |
| **TS-B** | 概念关系图 / 节点网络 | 影响因素、概念关系、节点连接 | whiteboard/hand-drawn/excalidraw/wobbly/balanced | 1 拟人化动物 + 节点 |
| **TS-C** | 系统架构图 / 分层图 | 系统组件、模块依赖、技术栈分层 | whiteboard/hand-drawn/excalidraw/wobbly/balanced | 1 服务器/电脑/数据库实物 |
| **TS-D** | 线框图 / UI 草图 | 产品界面、UI 流程、组件关系 | whiteboard/hand-drawn/excalidraw/wobbly/balanced | 1 工程师用 UI + 设备 |
| **TS-E** | 时间线 / 里程碑 | 版本演进、阶段划分、关键事件 | whiteboard/hand-drawn/excalidraw/wobbly/balanced | 1 人物 + 1 关键物件（沿途） |
| **TS-F** | 决策树 / 分支图 | 条件分支、判断逻辑、if-else 流程 | whiteboard/hand-drawn/excalidraw/wobbly/balanced | 1 思考中人物 + 问号/灯泡 |
| **TS-G** | 🆕 人物场景图（具象版） | 故事开头、概念具象化、对话场景 | whiteboard/hand-drawn/excalidraw/wobbly/balanced | 1 人物 + 1 巨型概念物 + 1 场景物件（3 件套是核心）|

### 6 变体共同要求：具象元素点缀（手稿气质，2026-06-08 加）

**问题诊断**：早期 6 变体（TS-A~TS-F）全部是"结构图"（流程/概念/架构/线框/时间线/分支）——画面里只有 box + arrow + 高亮，**没有人物、没有动物、没有真实物件**。结果是"工程师风"但"无人气"，用户原话反馈："太单调了、都是流程图、太无聊了、应该像手稿、还会画些人物动物之类的物品"。

**目标**：让每张科技插图都"像真人画的白板草图"——既保留结构信息（流程/概念/时间线），又有手稿气质的具象锚点（人/动物/物品）。避免变成"AI 矢量"或"PPT 框架图"。

**12 类具象元素库**（按"科技公众号文"常用度排序，每张图从中选 1-3 个）：

| 大类 | 元素 | 适用场景 | 视觉示例 |
|------|------|---------|---------|
| **A 人物**（最常用） | 工程师/程序员 | 几乎所有科技文 | 3-4 头身 + 圆头 + 戴方框眼镜 + 头发几笔（不是光头）+ 穿格子衬衫 + 抱笔记本电脑 + 手握键盘/鼠标 + 略带思考表情 |
| | 面试官/老板 | 职场、面试、P8 故事 | 3-4 头身 + 戴细框眼镜 + 穿西装 + 领带 + 手持简历/指向 + 严肃抿嘴 + 头发梳整齐 |
| | 实习生/新人 | 入职、教学、踩坑 | 3-4 头身 + 头发乱 + 头上一根呆毛 + 挠头 + 拿便签本 + 头顶汗珠符号 💧 |
| | 用户/读者 | 产品、C 端 | 3-4 头身 + 看手机/看电脑 + 头顶问号 ❓ + 手指摸下巴 |
| | 2 个小人对话 | 对比、争论、教学 | 2 人各 3-4 头身 + 相对而立 + 中间对话气泡（≤6 字/气泡）+ 动作手势明显（指点/摊手/竖大拇指）|
| **B 动物**（拟人化概念用） | 猫 | 产品/客户/黑盒 | 坐姿 + 圆眼 + 卷尾 |
| | 狗 | 团队、忠诚 | 坐姿 + 摇尾巴 |
| | 大象 | "房间里的大象"、大模型 | 笨重 + 占空间 |
| | 乌龟/兔子 | 速度对比、A/B 测试 | 一前一后 |
| | 鸟/鸽子 | 消息传递、飞书、轻量 | 飞翔 + 翅膀 |
| | 鱼 | 摸鱼、鱼骨图 | 鱼缸 + 摆尾 |
| **C 工具/办公** | 笔记本电脑、显示器 | 开发、AI、屏幕场景 | 屏幕发光 + 键盘 |
| | 文件夹、纸张、便签 | 文档、Skill、prompt | 堆叠 + 标签 |
| | 咖啡杯、马克杯 | 程序员燃料、深夜 | 蒸汽 + 把手 |
| | 铅笔、钢笔、橡皮 | 创作、草稿、迭代 | 写 + 擦痕迹 |
| | 灯泡 | 灵感、洞察、Idea | 发光 + 底座 |
| | 锤子/扳手 | 工具调用、工程化 | 木柄 + 金属头 |
| | 计算器、尺子 | 数据、测量 | 数字按键 |
| **D 食物/饮料** | 咖啡、奶茶、外卖盒 | 加班、996、副业 | 杯装 + 商标 |
| | 披萨、汉堡 | 摸鱼、午餐、加班 | 三角形切片 |
| | 苹果 | Apple、诱惑、知识点 | 红色 + 叶子 |
| **E 家具/场景** | 椅子、沙发、床 | 加班、家、休息 | 简约轮廓 |
| | 门、窗、楼梯 | 阶段、关卡、出口 | 透视感 |
| | 房间、办公室 | 面试、开会、独处 | 室内 + 桌椅 |
| **F 抽象物**（拟物化概念） | 巨型书本 | "217 页 SKILL.md"、知识量 | 立体书 + 页码 |
| | 巨型问号 | "为什么挂了？"、疑问 | 大 ? + 黄底 |
| | 巨型对勾/叉 | 答对/答错、对比 | ✓ / ✗ 大图标 |
| | 巨型齿轮 | 工具、机制、工程 | 互相啮合 |
| | 巨型公式 | Token 算式、参数 | 数字 + 符号 |
| | 巨型文件柜/档案盒 | 历史、归档、笔记 | 多层抽屉 |

**选 1-3 个的硬约束**：

1. **每个 TS-A/B/C/D/E/F 变体必含 ≥2 个具象元素**（1 人物 + 1 工具/物品/动物）
2. **总具象元素 ≤ 3 个**（避免喧宾夺主，保留信息密度）
3. **占画面 15-25% 视觉权重**（不是装饰，是"概念锚点"）
4. **1-2 个具象元素用 Excalidraw 高亮**（半透明黄 #FFD93D 40% 填充 OR 蓝色 #4D96FF 描边）
5. **必须为概念服务**（不是装饰）—— 例：画"217 页书"是表达"SKill 太多"，不是随便一本书

**反 AI slop 注意事项**（避免跑偏到"装饰画"）：

- ❌ **不要火柴人（stick figure）** —— 圆头 + 单线条身体 + 1-2 头身比 + 4 笔成型 = 火柴人。**这是用户 2026-06-08 明确禁止的最差造型**。
- ❌ **不要"圆头 + 2 个点眼睛 + 单线条身体"** 这种最简化造型 → 模型会把"Excalidraw 简笔" 理解成火柴人
- ❌ 不要写实摄影风格（手绘简笔即可，Excalidraw 风）
- ❌ 不要日漫/Kawaii 人物（圆眼 + 桃心 + 猫耳 = 走错片场）
- ❌ 不要拟人化卡通动物（迪士尼/皮克斯风，不是科技公众号气质）
- ❌ 不要"全家福"—— 1-3 个就够，4+ 个就成装饰画
- ❌ 不要不相关的物件（与文章概念无关的"白噪声装饰"）
- ✅ 工程师气质 = **3-4 头身比 + 圆头 + 戴方框/圆框眼镜 + 头发几笔（不是光头）+ 穿格子衬衫/T 恤/西装（有袖子和领口）+ 抱笔记本电脑 / 手握键盘 / 手托下巴思考 / 食指指向某物 + 略带焦虑或专注表情（嘴角/眉毛/汗珠 💧 / 问号 ❓）**
- ✅ 颜色仍用 Excalidraw 调色板（深灰 + 蓝/黄高亮），不引入新色

**🆕 "Excalidraw 工程师小人"标准参考（2026-06-08 加，subagent 必抄）：**

每次提到"画 1 个工程师小人/程序员/面试官/用户"时，**必须**用下面这组视觉特征（**禁止简化成"圆头 + 单线条身体"**）：

```
- 头身比 3-4 头身（明确，不是火柴人的 1-2 头身）
- 圆头 + 戴眼镜框（圆框或方框，2-3 笔勾出，不是光秃秃的圆）
- 头发几笔（不是光头）：3-5 根线条表发型 / 一根呆毛 / 戴帽子
- 具体躯干轮廓（不是单线条身体）：穿格子衬衫 / T 恤 / 西装，**有袖子和领口**，
  衣领用 2 笔 V 形表示，袖子用 1-2 笔弧线
- 明确手部动作（关键！）：手握键盘 / 托下巴思考 / 抱笔记本电脑 / 举咖啡杯 /
  食指指向某物 / 双手比 OK 手势 / 双手抱胸 / 双手举起欢呼
- 明确配饰：笔记本电脑 / 咖啡杯 / 文件夹 / 耳机 / 工牌 / 鼠标 / 笔
- 1 个小表情：嘴角上扬 / 抿嘴 / 皱眉 / 汗珠 💧 / 问号 ❓ / 灯泡 💡 / 闪电 ⚡
- 线条 2-3px 炭黑 #2D2D2D，保留手绘 wobble（"手稿"感不能丢）
- 可有黄色 #FFD93D 40% 高亮（衣服某块 / 工具 / 配饰）
```

**反向词必加**（每个提到人物的 prompt 都加这一行）：

```
NOT stick figure, NOT 火柴人, NOT 1-2 head body ratio, NOT 圆圈头 + 单线条身体,
NOT 光头, NOT 圆圈+4 笔火柴人, NOT 单线条身体, NOT 简笔到认不出职业,
NOT 抽象无五官圆形, NOT emoji 风格, NOT 表情符号圆形头
```

**subagent 选变体决策树**（5 维 + 具象元素综合判断）：

```
if 故事开头 / 人物对话 / 场景描述:
    pick TS-G (人物场景图)
elif 纯步骤 / 流程拆解:
    pick TS-A + 加 1 工程师小人在流程起点 + 1 文件/工具在终点
elif 概念关系 / 影响因素:
    pick TS-B + 加 1 拟人动物（"大象"代表大模型）
elif 系统架构 / 模块依赖:
    pick TS-C + 画真实服务器/电脑/数据库（不画 box）
elif 产品 UI / 界面流程:
    pick TS-D + 画 1 工程师用 UI + 1 设备
elif 版本演进 / 阶段:
    pick TS-E + 在关键里程碑画 1 人物 + 1 物件
elif 决策 / 分支 / trade-off:
    pick TS-F + 画 1 思考中人物 + 1 巨型问号
```

**TS-A 流程图（default，强制白底 Excalidraw 手绘）prompt 模板：**

**TS-A 流程图（default，强制白底 Excalidraw 手绘）prompt 模板：**

```
Consistent with cover: hand-drawn excalidraw sketch rendering, excalidraw palette (white #FFFFFF / charcoal #2D2D2D / blue #4D96FF / yellow #FFD93D), balanced-technical mood.
Square 1:1 white-background excalidraw-style hand-drawn sketch for Chinese tech blog.
White paper background #FFFFFF (NO gradients, NO textures, NO patterns, looks like clean paper).

A hand-drawn process flowchart like an engineer sketched on a whiteboard or Miro board. 4-6 boxes connected by directional arrows. The whole drawing has a sketchy, slightly imperfect feel — lines are not perfectly straight, boxes are not perfectly rectangular, the artist made it by hand. Think Excalidraw / tldraw / Figma "draw" tool output, not Illustrator.

Boxes (hand-drawn look):
- White fill (or semi-transparent yellow #FFD93D at 40% opacity for the KEY 1-2 boxes)
- 2-3px charcoal #2D2D2D border, **slightly wobbly** with visible hand-drawn imperfections
- Rounded corners but NOT perfect — corners are slightly off, edges are slightly wavy
- Each box contains a SHORT Chinese label (1-2 lines, hand-written feel):
  - Main concept in bold dark gray #2D2D2D
  - Optional sub-text in lighter gray #6B7280
- 1-2 KEY boxes highlighted with semi-transparent yellow #FFD93D fill (Excalidraw highlight style)

Arrows (hand-drawn):
- 2-3px charcoal #2D2D2D lines with arrowheads, **slightly wobbly** like a hand drew them
- 1 KEY transition arrow highlighted in Excalidraw blue #4D96FF (slightly thicker 3px)
- Other transitions stay charcoal

Visual character:
- Lines have **slight imperfection** — not laser-straight, not anti-aliased to perfection
- Boxes have **slight wobble** in edges
- Some boxes slightly overlap arrows (hand-drawn feel)
- Optional: 1-2 small annotations like "←这里" or "✓" or "✗" written in handwriting
- A small excalidraw-style **red dot/circle** (in blue #4D96FF not red) at one or two key points to draw attention

🆕 具象元素点缀（2026-06-08 用户反馈：纯流程图太单调，要"像手稿"）：
- 至少画 1 个**手绘工程师小人**（3-4 头身 + 圆头 + 戴方框眼镜 + 头发几笔 + 穿格子衬衫 / T 恤 / 西装 + 手握键盘 / 抱笔记本电脑 / 食指指向流程起点 + 略带思考或专注表情）
  - **必抄 "Excalidraw 工程师小人标准参考" 段（见上方反 AI slop 注意事项后）**
  - **反向词必加**：NOT stick figure, NOT 火柴人, NOT 1-2 head body ratio, NOT 圆圈头 + 单线条身体, NOT 光头, NOT 简笔到认不出职业
- 至少 1 个**具象物件**点缀（咖啡杯/笔记本电脑/文件夹/灯泡/问号/巨型书本/对勾/叉/齿轮/计算器/便签）
- 1-2 个具象元素用 Excalidraw 高亮（半透明黄 #FFD93D 40% 填充 OR 蓝色 #4D96FF 描边）
- 具象元素占画面 15-25% 视觉权重（不喧宾夺主，保留流程图信息密度）
- 完整 12 类具象元素设计原则见下方"### 6 变体共同要求：具象元素点缀（手稿气质）"章节

CRITICAL: All Chinese text must look HAND-WRITTEN, not typeset. Use 思源黑体 or handwriting-style font, 14-18pt. Chinese text '清晰可识别' — must be sharp and legible (don't sacrifice readability for sketchiness).

Title above chart: <章节标题> in bold hand-written style at top, 22-28pt dark gray #2D2D2D.
Subtle 'luoboa.com 萝卜啊' brand in light gray #B0B0B0 bottom-right 8pt, handwriting font.

Content (节选原文核心流程):
<节选 200-400 字原文>

Square 1:1 format. The aesthetic is '工程师白板随手画' — NOT McKinsey/TED-Ed polished, NOT dark Excalidraw white-board, but specifically WHITE PAPER + hand-drawn lines + slight wobble + Excalidraw highlight.
NOT photorealistic, NOT 3D, NOT painterly, NOT watercolor, NOT flat vector (with laser-straight lines).
```

**TS-B / TS-C / TS-D / TS-E / TS-F 模板**：同 TS-A 骨架,把"flowchart"换成"concept relationship graph" / "system architecture" / "wireframe UI sketch" / "timeline milestone" / "decision tree" 即可,所有 hand-drawn 关键词、Excalidraw 调色板、wobble 风格通用。完整 6 变体 prompt 见 `references/style-guide.md` 末节"科技插图 - 白底 Excalidraw 手绘"章节(待补充)。

**🆕 TS-G 人物场景图（具象版，2026-06-08 加）prompt 模板：**

```
Consistent with cover: hand-drawn excalidraw sketch rendering, excalidraw palette (white #FFFFFF / charcoal #2D2D2D / blue #4D96FF / yellow #FFD93D), balanced-technical mood.

Square 1:1 white-background excalidraw-style hand-drawn sketch for Chinese tech blog.
White paper background #FFFFFF (NO gradients, NO textures, NO patterns, looks like clean paper).

A hand-drawn SCENE WITH CHARACTER — 1 small hand-drawn engineer/character figure in the foreground, doing a specific action related to the article topic. Around the character: 1 hand-drawn SCENE OBJECT (oversized for the concept) and 1 hand-drawn ENVIRONMENT prop. Optional: 1-2 small EMPTY thought bubbles or speech bubbles near the character (NO text inside — or with 1-3 short hand-written Chinese words like "怎么选?" / "塞哪?" / "挂了").

CHARACTER (1 small figure, ≤ 20% of frame, 🆕 2026-06-08 强化"Excalidraw 工程师小人"标准):
- 3-4 head body ratio (NOT stick figure, NOT 1-2 头身的火柴人)
- 圆头 + 戴方框/圆框眼镜（2-3 笔勾出，不是光秃秃的圆）+ 头发几笔（3-5 根线条 / 一根呆毛 / 戴帽子，不是光头）
- 具体躯干轮廓（不是单线条身体）：穿格子衬衫 / T 恤 / 西装，**有袖子和领口**，衣领用 V 形 2 笔表示
- 明确手部动作（关键！至少 1 个具体动作）：
  - 手握键盘 / 手托下巴思考 / 抱笔记本电脑 / 举咖啡杯 / 食指指向 SCENE OBJECT
  - 双手比 OK 手势 / 双手抱胸 / 双手举起欢呼
- 明确配饰（至少 1 个）：笔记本电脑 / 咖啡杯 / 文件夹 / 耳机 / 工牌 / 鼠标 / 笔
- 1 个小表情：嘴角上扬 / 抿嘴 / 皱眉 / 汗珠 💧 / 问号 ❓ / 灯泡 💡 / 闪电 ⚡
- Charcoal #2D2D2D outline, 2-3px wobbly stroke（保留手绘 wobble）
- 1 KEY character only (no crowd)
- Position: foreground left/right/center, NOT floating in the middle
- 视觉参考：见上方"反 AI slop 注意事项"后的"Excalidraw 工程师小人标准参考"段（subagent 必抄）
- 反向词必加：NOT stick figure, NOT 火柴人, NOT 1-2 head body ratio, NOT 圆圈头 + 单线条身体, NOT 光头, NOT 圆圈+4 笔火柴人, NOT 简笔到认不出职业, NOT 抽象无五官圆形, NOT emoji 风格, NOT anime, NOT kawaii, NOT realistic, NOT Disney/Pixar

SCENE OBJECT (1 oversized prop, 20-30% of frame):
- Hand-drawn: 文件夹 / 笔记本电脑 / 大书 (217 pages stack) / 巨型问号 / 咖啡杯 / 灯泡 / 巨型公式 / 文件柜 / 巨型对勾 / 巨型叉
- Semi-transparent yellow #FFD93D 40% fill for the KEY object (the one that carries the article concept)
- 2-3px charcoal #2D2D2D wobbly outline
- Position: behind or beside the character, oversized to convey "this is the main concept"

ENVIRONMENT PROP (1 smaller, 5-10% of frame):
- Hand-drawn: 椅子 / 桌子 / 门 / 窗 / 楼梯 / 房间一角 / 楼梯 / 楼梯 / 笔记本电脑屏幕
- 2-3px charcoal #2D2D2D wobbly outline, white fill
- Position: around the character, gives context

Visual character:
- Lines have slight imperfection — not laser-straight
- The character + 1-2 props should feel like a real engineer sketched them
- Optional: 1-2 small hand-written Chinese labels (≤6字) like "面试" / "挂了" / "塞不进" near the scene

CRITICAL: All Chinese text (if any) must look HAND-WRITTEN. Chinese text '清晰可识别' — must be sharp and legible.

Title above chart: <章节标题> in bold hand-written style at top, 22-28pt dark gray #2D2D2D.
Subtle 'luoboa.com 萝卜啊' brand in light gray #B0B0B0 bottom-right 8pt, handwriting font.

Content (节选原文核心场景):
<节选 100-300 字原文，描述人物+动作+场景>

Square 1:1 format. The aesthetic is '工程师白板随手画 — 带人物的 1 场景' — whiteboard + hand-drawn lines + slight wobble + Excalidraw highlight + 1 small character + 1 oversized prop.
NOT photorealistic, NOT 3D, NOT painterly, NOT watercolor, NOT flat vector.
NOT anime, NOT kawaii, NOT realistic figure, NOT Disney/Pixar style.
```

**🆕 6 变体共同硬要求（2026-06-08 加）**：每个 TS-A/B/C/D/E/F 变体**必含 ≥2 个具象元素**（1 个人物 + 1 个工具/物品/动物，详见下方"### 6 变体共同要求：具象元素点缀"）。仅当文章是"纯概念解释 / 无场景"时可省略人物，但**仍需画 1 个具象物件**（如巨型问号、灯泡、对勾）作视觉锚点。

**TS-B 柱状图 prompt 模板：**

```
Consistent with cover: clean-digital rendering, zhihu-mono palette, subtle-professional mood.
White background #FFFFFF. A horizontal or vertical bar chart in clean
minimal style, 5-8 data categories.

Bars:
- Solid #056DE8 zhihu blue for the highlighted/most-important data point
- Solid #D9E2EC light gray for comparison bars
- NO 3D, NO gradients, NO shadows

Axes:
- Thin 1px black #1A1A1A lines
- Tick labels in 10-12pt sans-serif Chinese (思源黑体), black #1A1A1A
- Data labels above each bar in same font, #1A1A1A black, bold for
  the highlighted bar

Title above chart: <标题> in bold 思源黑体 24-32pt black, sharp.
Legend (if needed): small Chinese label with 2px color swatch.

CRITICAL: Chinese labels '清晰锐利', anti-aliased.

Data (节选原文中的数据):
- 类别 1: 数值
- 类别 2: 数值 (高亮)
- ...

Square 1:1 format. The aesthetic is '专业研究报告图表' — Tufte data-ink ratio.
```

**TS-D 知识图谱 prompt 模板：**

```
Consistent with cover: clean-digital rendering, zhihu-mono palette, subtle-professional mood.
White background #FFFFFF. A force-directed knowledge graph showing
relationships between 6-10 concepts.

Nodes:
- White circles with 2px #1A1A1A black border
- 40-80px diameter (size = importance)
- The 2-3 most important nodes: filled with #056DE8 blue
- Other nodes: white fill
- One main node: 80px diameter, #056DE8 blue

Edges:
- 1-2px #1A1A1A thin lines connecting related nodes
- One KEY relationship edge: 2.5px #F4A261 orange to highlight the
  most important connection

Each node has ONE Chinese label in clean sans-serif (思源黑体), 12-14pt,
sharp, #1A1A1A black. Labels positioned next to nodes (not inside).

NO curved lines, NO clusters, NO force-field visualization artifacts.

Title: <标题> in bold 思源黑体 24-32pt at top.

Square 1:1 format. Tufte data-ink ratio.
```

**TS-E 对比表 prompt 模板：**

```
Consistent with cover: clean-digital rendering, zhihu-mono palette, subtle-professional mood.
White background #FFFFFF. A clean comparison table with 3-4 columns and
4-7 rows.

Header row: #F0F2F7 light gray background, bold black Chinese text 16-20pt.
Data rows: white background, regular black text 14-16pt,
alternating subtle zebra striping (white / #FAFAFA) for readability.
Cell borders: thin 1px #D9E2EC light gray lines.
Column widths: 严格对齐，第一列 (选项) 较窄，结论列较宽.

Key recommendation in the conclusion column: highlighted with #056DE8
blue background and white text. Other key cells: subtle #F4A261
orange marker (small dot or arrow).

CRITICAL: Chinese text '清晰锐利', no wrapping, well-aligned, 思源黑体.

Title: <标题> in bold 思源黑体 24-32pt at top.

Square 1:1 format. The aesthetic is '专业决策矩阵'.
```

**通用底栏：每张科技插图右下角都加 `luoboa.com 萝卜啊` 浅灰色水印（8px / 60% opacity）。**

### ⚠️ 白底 Excalidraw 手绘插图硬约束（2026-06-06 起，2026-06-08 加第 7 条）

1. **背景必须纯白 `#FFFFFF`**，禁止暗色、灰底、渐变、纹理 —— 想象白纸
2. **元素必须丰富**——禁止只有 2-3 个 icon。必须包含至少：
   - 1 个手写风格主标题（手写体或思源黑体 22-28pt 深灰 #2D2D2D, NOT 思源宋体）
   - 1 个核心手绘可视化（流程/概念/架构/线框/时间线/分支，6 选 1；或 TS-G 人物场景图）
   - 2-3 个手写风格文字标签或注解（≤ 8 字/标签,不能长篇大论）
   - 1 个 Excalidraw 高亮（半透明黄 #FFD93D 40% 填充 OR 蓝色 #4D96FF 描边 1 个关键 box/箭头）
3. **🆕 ≥2 个具象元素（2026-06-08 加，2026-06-08 二次加固化 "NOT 火柴人" 硬约束）**——禁止纯几何（box + arrow）就让图"看起来太单调"。每张图必含：
   - 至少 **1 个 Excalidraw 工程师小人**（3-4 头身 + 圆头 + 戴方框眼镜 + 头发几笔 + 穿格子衬衫/T 恤/西装 + 手握键盘/抱电脑/指向某物 + 明确配饰 + 1 个小表情；**完整视觉参考见上方"反 AI slop 注意事项"后的标准段，subagent 必抄**）
   - 至少 **1 个具象物件**点缀（人物/动物/工具/食物/家具/抽象物 6 大类 30+ 元素中选）
   - 总具象元素 ≤ 3 个（不喧宾夺主，保留信息密度）
   - 仅当文章是"纯概念解释 / 无场景"时可省略人物，但仍需画 1 个具象物件作视觉锚点
   - **人物反向词必加**（每个 prompt 都加这一行）：`NOT stick figure, NOT 火柴人, NOT 1-2 head body ratio, NOT 圆圈头 + 单线条身体, NOT 光头, NOT 圆圈+4 笔火柴人, NOT 简笔到认不出职业, NOT 抽象无五官圆形, NOT emoji 风格, NOT anime, NOT kawaii, NOT realistic`
4. **中文必须清晰渲染**（不要因为"手绘风"就牺牲可读性），字号 ≥ 12pt
5. **必须保留手绘痕迹** —— 线条轻微 wobble、box 边缘不齐、箭头手抖感（这是"技术人气质"的核心,不能去掉）
6. **内容必须来自原文**，不能瞎编
7. **色彩 ≤ 4 个**：白 + 深灰主线条 + 蓝高亮 + 黄高亮（+ 极少量橙/紫红）

### 科技 Banner 排版风格（4 种 TA- 风格）

**🆕 2026-06-08 起 banner default 改为 TA-D 白底 Excalidraw 风格**——因为 5 维一致性原则（memory `luoboa-illustrate-cover-section-consistency`）要求"封面跟插图共享 Palette + Rendering + Mood 3 维"，而 6 变体（TS-A/B/C/D/E/F）插图都是白底 Excalidraw 手绘，**只有 TA-D 跟插图共享调色板**。TA-A/B/C 3 种保留为"特殊场景备选"——仅当文章内所有图（封面+全部插图）都统一走对应风格的暗色/PCB/数据看板时才能用，**不能混搭**。

每期 subagent 自动选 1 种。**默认 TA-D**：

| # | 风格 | 状态 | 5维映射 | 跟插图共享 3 维？ | 适合 |
|---|------|------|---------|----------------|------|
| **TA-D** | ✏️ **白底 Excalidraw 手绘**（**default**）| 🆕 2026-06-08 新增 | typography/excalidraw/**hand-drawn**/clean/balanced | ✅ **完全共享**（白底 + 手绘 + balanced）| 绝大多数科技公众号文（默认走这个）|
| **TA-A** | 🔵 数字终端风 | ⚠️ 特殊场景备选 | typography/tech-blue/clean-digital/display/bold | ❌ 暗色 + clean-digital + bold — **不能跟白底 Excalidraw 插图混搭** | 工具类/教程类，但**整篇文章所有图都需统一走暗色** |
| **TA-B** | ⚡ 电路图腾风 | ⚠️ 特殊场景备选 | typography/tech-mono/hand-drawn/clean/balanced | ⚠️ 共享 Rendering（hand-drawn）+ Mood（balanced），但 Palette 米白 PCB **不是白底** | 整篇文章走米白 PCB 风格时 |
| **TA-C** | 📊 数据看板风 | ⚠️ 特殊场景备选 | typography/dataviz/flat-vector/clean/subtle | ⚠️ Palette 白底但 Rendering flat-vector 不是手绘，**不能跟手绘 Excalidraw 插图混搭** | 整篇文章走咨询报告风时 |

**TA-A 数字终端风 prompt 模板（⚠️ 特殊场景备选）：**

```
Typography-dominant tech cover (21:9 landscape, exactly 1920x832, NOT square NOT portrait).
A late-night dev workstation scene: matte dark-navy gradient background
(#0D1B2A → #1E3A5F), soft cyan glow from a monitor on the right side,
scattered thin grid lines and tiny data points in #4D96FF suggesting code
flowing. Foreground has subtle code snippets / terminal output in soft
#B5C5D3 (highly blurred so not legible as text).
🆕 具象元素点缀（2026-06-08 用户反馈 "太单调"，banner 也要"像手稿"）：
- 1 个**手绘工程师剪影**（暗色背景里的坐姿剪影，低头看屏幕，戴耳机，背光勾勒出 #4D96FF cyan 边光；或站姿面对巨型终端）
- 1-2 个**具象大物件**（笔记本电脑剪影 / 巨型终端 prompt 框 / 巨型 `< / >` 符号 / 巨型 `{ }` / 巨型 `{;}` 字符 / 巨型 `;exit` 命令）
- 1 个**场景物件**（咖啡杯剪影 / 鼠标 / 键盘一角 / 桌子边缘 / 显示器支架 / 数据线）
- 具象元素占 banner 画面 15-25% 视觉权重（不喧宾夺主，保留文字 + 终端骨架）
- 颜色仍用 tech-blue 调色板（白 + cyan + 极少量橙，**不引入新色**）
- 反 AI slop：NOT 写实照片、NOT 日漫、NOT Kawaii；剪影要"工程感"不要"光鲜亮丽"
- 完整 12 类具象元素设计原则见上方 "### 6 变体共同要求：具象元素点缀" 章节
PALETTE: tech-blue — primary background #1E3A5F / #0D1B2A, text white #FFFFFF
and #B5C5D3, accent #4D96FF cyan, highlight #F4A261 orange (≤10% area).
RENDERING: clean-digital — sharp 1-2px strokes, no painterly, no film grain.
FONT: display — bold geometric display typography, heavy expressive
letterforms, strong visual impact.
The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous display
characters occupying the central 50-60% of the frame, white #FFFFFF text
with a 2-3px cyan #4D96FF outline / inner glow, positioned in the
left 60% of the frame. The right 40% holds a single iconic data motif
(a 1-0-1 binary, a glowing </> bracket, or a terminal cursor block) in
#4D96FF cyan. Below the title, a small sans-serif Chinese subtitle
「<SUBTITLE>」in #B5C5D3 (60% of title size), positioned directly
under the title.
A tiny 8px high brand 'luoboa.com 萝卜啊' in #B5C5D3 bottom-right.
MOOD: bold — high contrast, vivid cyan against deep navy, dramatic
tech-noir energy. Cinematic 4k quality, modern dev aesthetic.

CRITICAL: All Chinese characters must be SHARP and LEGIBLE, no garbling.
Render 「<TITLE>」 exactly as written, 220-340px visual height.
NOT minimalist (NOT plain blue background with small title — that is
boring and NOT a banner).
```

**TA-B 电路图腾风 prompt 模板（⚠️ 特殊场景备选）：**

```
Typography-dominant tech cover (21:9 landscape, exactly 1920x832, NOT square NOT portrait).
A printed-circuit-board inspired composition: cream-white #F0F4F8 base
with thin charcoal #2D2D2D hand-drawn circuit traces (PCB lines, chip
rectangles, resistor zigzag patterns, signal arrows) drifting
diagonally across the entire frame, like a system architecture diagram
deconstructed into cover art. Empty negative space concentrated in the
right 50% for text.
🆕 具象元素点缀（2026-06-08 用户反馈 "太单调"，banner 也要"像手稿"）：
- 1 个**手绘工程师半身像或手部特写**（手握烙铁 / 手握示波器探头 / 戴护目镜的工程师半身 / 戴手套正在焊接）
- 1-2 个**具象 PCB 元件**（电容器 / 电阻器 / 二极管 / 芯片（标 `SKILL` / `Claude` 字样的微芯片）/ 巨型 USB 接口 / 巨型 HDMI 接口 / 巨型 LED 灯）
- 1 个**场景物件**（烙铁 / 万用表 / 螺丝刀 / 散热风扇 / PCB 板边角 / 测试夹具 / 工作台桌面）
- 具象元素占 banner 画面 15-25% 视觉权重（不喧宾夺主，保留文字 + 电路骨架）
- 颜色仍用 tech-mono 调色板（米白 + 炭黑 + cyan + 极少量橙，**不引入新色**）
- 反 AI slop：NOT 写实 PCB 照片、NOT 日漫工程师、NOT 假芯片（保持"草根手绘"感）
- 完整 12 类具象元素设计原则见上方 "### 6 变体共同要求：具象元素点缀" 章节
PALETTE: tech-mono — primary cream #F0F4F8 / paper white, ink #1A1A1A
for circuit lines, accent #4D96FF cyan for highlighted signal paths,
highlight #F4A261 orange (≤10% area).
RENDERING: hand-drawn — sketchy organic strokes with visible imperfections,
variable line weight, marker/pen texture, paper grain surface.
FONT: clean — clean geometric sans-serif, sharp uniform line weight,
modern minimal letterforms.
The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous clean
sans-serif Chinese characters occupying the central 50-60% of the frame,
ink #1A1A1A color, positioned in the right 50% of the frame, with one
or two circuit traces actually overlapping THROUGH the text (signal
lines piercing characters). Title size 220-340px.
A small subtitle '「<SUBTITLE>」' in #4A6FA5 below the title (60% of
title size).
Tiny 8px high brand 'luoboa.com 萝卜啊' in #8C8C8C bottom-left.
MOOD: balanced — medium contrast, paper-print feel, blueprint poster
energy, the cover reads like a developer conference keynote visual.

CRITICAL: All Chinese characters must be SHARP and LEGIBLE.
NOT minimalist.
```

**TA-C 数据看板风 prompt 模板（⚠️ 特殊场景备选）：**

```
Typography-dominant tech cover (21:9 landscape, exactly 1920x832, NOT square NOT portrait).
A data dashboard composition: pure white #FFFFFF base (NOT gray, NOT off-white),
with a sparse grid of pale gray #F0F2F7 8x8 cells filling the background.
Foreground features 1-2 large data visualization motifs in the LEFT 30% of
the frame: a big bar chart or a percentage number 「<KEY_METRIC>%」 in
#056DE8 zhihu blue, plus 1-2 small KPI cards with sample metrics in
#1A1A1A. The right 65% is reserved for the title.
🆕 具象元素点缀（2026-06-08 用户反馈 "太单调"，banner 也要"像手稿"）：
- 1 个**手绘数据分析师小人**（西装或商务休闲装，指着图表 / 拿平板 / 戴眼镜看数据 / 站姿分析报告前）
- 1-2 个**具象大物件**（巨型百分号 % / 巨型数字 `<KEY_METRIC>` / 巨型箭头 ↗ / 巨型饼图一角 / 巨型折线图标 / 巨型 K 线图 / 巨型趋势线 / 巨型对勾或叉）
- 1 个**场景物件**（办公桌一角 / 笔记本电脑 / 咖啡杯 / 数据报表纸张 / 铅笔 / 计算器 / iPad / 趋势线图钉）
- 具象元素占 banner 画面 15-25% 视觉权重（不喧宾夺主，保留文字 + 看板骨架）
- 颜色仍用 dataviz 调色板（白 + 黑 + zhihu 蓝 + 极少量橙，**不引入新色**）
- 反 AI slop：NOT 写实人像、NOT 日漫、NOT Kawaii；分析师要"专业朴素"不要"CEO 派头"
- 完整 12 类具象元素设计原则见上方 "### 6 变体共同要求：具象元素点缀" 章节
PALETTE: dataviz — pure white #FFFFFF base, ink #1A1A1A text,
zhihu blue #056DE8 accent, light gray #F0F2F7 for grid, tiny orange
#F4A261 highlight (≤5% area).
RENDERING: flat-vector — clean precise edges, anti-aliased Chinese text,
no painterly, no film grain, no sketch.
FONT: clean — clean geometric sans-serif (思源黑体 / Inter),
sharp uniform line weight, modern minimal letterforms.
The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous clean
sans-serif Chinese characters occupying the central 50-60% of the frame,
ink #1A1A1A, positioned in the right 65% of the frame, 220-340px visual
height. ONE KEY WORD inside the title highlighted in #056DE8 zhihu blue
(the headline verb or core number, e.g. 「70% 节省」or 「5 个技巧」).
A small subtitle '「<SUBTITLE>」' in #4A6FA5 below the title.
Tiny 8px high brand 'luoboa.com 萝卜啊' in #8C8C8C bottom-right.
MOOD: subtle — high data-ink ratio, professional consulting-report
aesthetic, Tufte-style, the cover reads like a McKinsey / 36kr cover.

CRITICAL: All Chinese characters must be SHARP and LEGIBLE.
NOT minimalist.
```

**TA-D 白底 Excalidraw 手绘风 prompt 模板（default，2026-06-08 新增）：**

```
Typography-dominant tech cover (21:9 landscape, exactly 1920x832, NOT square NOT portrait).
A whiteboard / Miro style cover DENSELY covered in hand-drawn Excalidraw
sketches — NOT a white background with sparse corner labels. The whole
frame is filled with hand-drawn elements: large process flows, decision
trees, node networks, system architecture sketches, file stacks,
data callouts, token counters, error icons, checkmarks/crosses, arrows
connecting everything. Imagine an engineer furiously sketching on a
whiteboard with multiple intertwined diagrams + annotations, not a
single clean illustration with a title on top.

Background base: pure white #FFFFFF paper (just the substrate — most
of it should be covered with hand-drawn elements, not empty white space).

Hand-drawn elements composition (must fill 50-70% of the frame, BUT
be SHAPES ONLY — **NO text labels inside any shape**, no words
anywhere in the background; only hand-drawn shapes/icons/arrows/
connectors/highlights):
- A large central process flow / decision tree / node network occupying
  40-50% of the frame (boxes/diamonds/circles must be EMPTY)
- Surrounding details: connecting arrows, decision diamonds, status
  indicators, file/folder icons, terminal/box shapes, equation
  operator symbols (+, =, ×, ÷, ✓, ✗, ? , !), lightbulb/battery/
  starburst/explosion shapes
- 🆕 **3-5 个手绘具象元素点缀**（2026-06-08 用户反馈"太单调"，banner 也要"像手稿"）：
  - 1-2 个 **Excalidraw 工程师小人**（3-4 头身 + 圆头 + 戴方框眼镜 + 头发几笔 + 穿格子衬衫 / T 恤 / 西装 + 手握键盘 / 抱笔记本电脑 / 食指指向某物 + 明确配饰 + 1 个小表情；**完整视觉参考见上方"反 AI slop 注意事项"后的标准段，subagent 必抄**）
  - 1-2 个具象大物件（巨型书本/巨型问号/巨型公式/巨型电脑/巨型文件柜/巨型对勾或叉）
  - 1 个场景物件（咖啡杯/铅笔/灯泡/椅子/笔记本电脑/文件夹/便签）
  - 具象元素占 banner 画面 15-25% 视觉权重（不喧宾夺主，保留 banner 文字 + 流程骨架）
  - **人物反向词必加**：`NOT stick figure, NOT 火柴人, NOT 1-2 head body ratio, NOT 圆圈头 + 单线条身体, NOT 光头, NOT 圆圈+4 笔火柴人, NOT 简笔到认不出职业, NOT 抽象无五官圆形, NOT emoji 风格, NOT anime, NOT kawaii, NOT realistic`
  - 完整 12 类具象元素设计原则见上方"### 6 变体共同要求：具象元素点缀"章节
- Multiple visual layers overlapping and connected, like a real
  whiteboard with several intertwined shapes
- **❌ NO hand-written text annotations in the background** (no
  "←这里" / "8 秒" / "217 页" / "context 200K" / etc. — the
  background is SHAPES ONLY)
- 1-2 KEY boxes highlighted with semi-transparent yellow #FFD93D
  fill (Excalidraw highlight style, EMPTY inside)
- 1-2 KEY transition arrows in Excalidraw blue #4D96FF (slightly
  thicker 3px)
- 1-2 KEY 具象元素用 Excalidraw 高亮（半透明黄 #FFD93D 40% 填充 OR 蓝色 #4D96FF 描边）
- Background elements must be VISUALLY RECESSED — slightly
  desaturated or smaller in scale — so the title clearly dominates

PALETTE: excalidraw — pure white #FFFFFF base, primary ink #2D2D2D
(charcoal), accent #4D96FF cyan for highlighted paths, highlight
#FFD93D yellow 40% opacity for key boxes, tiny orange #F4A261 / purple-red
#9B59B6 accents (≤5% area each). NO red, NO crimson, NO scarlet.

RENDERING: hand-drawn — sketchy organic strokes with visible
imperfections, slight wobble, variable line weight, marker/pen texture.
Lines are NOT laser-straight, NOT anti-aliased to perfection. Boxes
have slightly off-rounded corners, edges slightly wavy.

FONT APPLICATION (CRITICAL — 来自 baoyu-cover-image, 必加段):
Use bold decorative display typography with strong visual impact.
Heavy expressive letterforms with thick-thin contrast. The title
characters must feel like art-poster display, not plain sans-serif,
not Song-style typeface. Each character should have weight variation,
slight ink bleed, and decorative impact. Use thick-thin contrast
visible in the strokes.

The LARGE TITLE TEXT「<TITLE>」is the visual hero — embedded INTO the
hand-drawn background (not floating in empty space). Enormous display
characters occupying the central 50-60% of the frame, ink #2D2D2D color,
220-340px visual height, with hand-drawn elements connecting/pointing
to/passing through the title. ONE KEY PHRASE inside the title
highlighted with #FFD93D yellow background (e.g. 「5 个 SKILL.md」 or
「11 条爆款」), another key phrase with #4D96FF blue wobbly underline.
A small subtitle '「<SUBTITLE>」' in #4A6FA5 below the title (60% of
title size).
Tiny 8px high brand 'luoboa.com 萝卜啊' in #B0B0B0 bottom-right.

MOOD: balanced-technical — medium contrast, paper-print feel, the
cover reads like a senior engineer's whiteboard sketch with a strong
art-poster title slapped on top.

CRITICAL: All Chinese characters must be SHARP and LEGIBLE, no garbling.
Render 「<TITLE>」 exactly as written with sharp legibility for the
main title and the subtitle.
NOT minimalist (NOT sparse white background with small title — that's
a failed banner). NOT dark navy (NOT TA-A). NOT clean-digital vector
(NOT TA-C). The cover should feel ALIVE and CROWDED with hand-drawn
SHAPES (boxes, arrows, icons, diamonds, circles) but NOT labeled
diagrams — the background is shapes only, NO text labels.

🆕 **CRITICAL CONSTRAINT — BACKGROUND MUST HAVE NO TEXT (2026-06-08
用户反馈: "banner 太密密麻麻了，分不清主次了。手绘是背景与附图，
可以多，但不可以出现文字"):** The hand-drawn Excalidraw background
contains ONLY shapes, icons, arrows, and graphic symbols. NO Chinese
characters, NO English words, NO numbers, NO text labels anywhere in
the background. The only text in the entire image is the MAIN TITLE
and SUBTITLE (plus the tiny corner watermark). Every box/diamond/
circle in the background is EMPTY — they are pure visual shapes
representing process flow / decision tree / comparison, not labeled
diagrams. Title font-size 350-400px (not 280-320px), title occupies
70-80% visual weight (not 60-70%) — the title is the absolute visual
hero.
```

### ⚠️ Banner 比例硬约束（2026-06-06 起）

**所有 banner（cover）出图比例必须 21:9**（即 1920x832 / 3024x1296 / 2560x1080），**禁止出现 1:1 / 3:4 / 4:3 / 9:16 / 1.5:1 等任何非 21:9 比例**。这是公众号/微信生态对 banner 的硬性要求。

**生成后必须做比例校验**：
```python
from PIL import Image
im = Image.open("images/00-cover-banner.png")
w, h = im.size
ratio = w / h
assert 2.2 <= ratio <= 2.45, f"❌ Banner 比例不合格: {ratio:.2f} (must be 2.33 ± 0.1)，请重新出图并显式指定 21:9"
print(f"✅ Banner 比例合格: {ratio:.2f}")
```

**API 调用强制指定**：
- grsai: `--ratio "21:9"` 或 `--aspect-ratio "1920x832"`
- dreamina: `--ratio "21:9"`

如果后端不支持 21:9，**用最接近的 16:9 fallback 并在文件名后加 `.16x9` 提示**，绝不静默接受 1.5:1 / 1:1 等错误比例。

### 科技 Banner 失败重试规则

如果生成出来的 banner 出现以下问题，按优先级重试：

1. **比例错（不是 21:9）** → 检查 prompt 里有没有写 `(21:9 landscape, exactly 1920x832)` + 调用参数
2. **中文字渲染乱码** → 在 prompt 末尾加 `Chinese text 「<TITLE>」 must be SHARP and LEGIBLE, render as the exact characters written, no garbling no missing characters`
3. **标题太小、缺乏 banner 感** → 在 prompt 里显式写 `enormous display characters occupying the central 50-60% of the frame, 220-340px visual height, NOT small corner label`
4. **画面太素 / 白底占太多** → 必须用 **TA-D**（白底 Excalidraw 共享插图调色板，**default**）。TA-A / TA-B / TA-C 仅在整篇文章所有图都统一走对应风格时才能用，**不能跟白底 Excalidraw 插图混搭**。TA-D 模板里有"DENSELY covered"和"60-80% of the frame"硬约束，确保背景铺满手绘元素
5. **背景元素密度不够（手绘元素只占 4 个 corner 而非铺满）** → 用 TA-D 模板，**别用 corner 标注代替背景**。整体画面应该是"工程师疯狂画的白板"，不是"4 个标签 + 1 个标题"
6. **字体太素（默认思源黑体粗体）** → 必加 **Font Application 段**（baoyu 句式）：`Use bold decorative display typography with strong visual impact, heavy expressive letterforms, thick-thin contrast, ink bleed, NOT plain sans-serif, NOT Song-style typeface`。Font 必须是 **display 粗体装饰**（不是 SKILL.md 默认科技类 `clean`）
7. **配色出现红色** → 在 prompt 末尾追加 `NO red, NO crimson, NO scarlet — replace any red with #4D96FF cyan or #F4A261 orange`
8. **🆕 背景出现文字标签（手绘区域带字导致分不清主次）** → 删掉 prompt 里的"hand-written annotations"和"comment boxes with hand-written text"段；改用"EMPTY boxes / decision diamonds"等纯形状。**整个画面唯一的文字是主标题 + 副标题 + 角部小水印**——背景只能画形状/icon/箭头，不带任何字。这是 2026-06-08 用户反馈的硬约束。
9. **🆕 画面"太单调"/"都是流程图"/"没有人物"（2026-06-08 用户原话）** → 必加**具象元素点缀**。每张 banner 必含 ≥3 个具象元素（1 人物 + 1 大物件 + 1 场景物）。具体指引：
   - TA-D 白底 Excalidraw：1 工程师/面试官/对话 2 人 + 1 巨型书本/巨型问号/巨型公式/巨型电脑/巨型文件柜 + 1 咖啡杯/铅笔/灯泡/椅子/笔记本电脑
   - TA-A 数字终端：1 工程师剪影（背光 cyan 边光） + 1 巨型终端 prompt 框 / 巨型 `</>` `{}` `{;}` 字符 + 1 咖啡杯剪影 / 鼠标 / 键盘一角
   - TA-B 电路图腾：1 工程师半身或手部特写（手握烙铁/戴护目镜） + 1 电容/电阻/芯片（标 `SKILL`/`Claude` 字样） + 1 烙铁/万用表/散热风扇
   - TA-C 数据看板：1 数据分析师小人（西装/戴眼镜/拿平板） + 1 巨型 `%` / 巨型数字 / 巨型饼图 / 巨型 K 线 / 巨型箭头 ↗ + 1 办公桌/计算器/iPad
   - 完整 12 类具象元素设计原则见上方 "### 6 变体共同要求：具象元素点缀" 章节
   - 修复 prompt 必加段：`<TA-X 模板> + 🆕 3-5 个手绘具象元素点缀（1 人物 + 1 大物件 + 1 场景物，NOT 日漫/Kawaii/写实/迪士尼，仍用 <调色板名> 调色板）`

## Workflow B: 情感治愈类

- Cover: **5维艺术大字排版**（与怀旧照片风共用 A-L 排版体系）。用户选择排版风格 + 底图渲染方式（painterly水彩插画 / photography写实摄影）。标题占画面中心40-70%，不是角落小字。NO brand logo even if enabled.
- Sections: warm healing style with Morandi colors.
- **Critical**: from 2nd section onward, pass previous generation's URL as `--ref-url` to maintain character consistency.
- **Critical**: send full novel/story text, not summaries.
- **Critical**: 封面底图渲染必须和正文风格统一——莫兰迪插画正文用painterly底图，实景正文用photography底图。完整封面模板见 `references/style-guide.md` 柔情风章节。
- **风格一致性**：插图prompt必须继承封面5维参数中的 Palette + Rendering + Mood。例：封面A日系电影感→插图必须含"soft watercolor wash" + "cream #FFFAF0, golden yellow #F6AD55" + "low contrast, muted desaturated"。不允许封面painterly+插图无渲染约束。

## Workflow E: 怀旧照片类

适合情感治愈、回忆、亲情、乡愁类文章。90年代写实照片风格，胶片颗粒感，但**基调是温馨的，不是阴郁的**——想象夏末傍晚、奶奶家客厅那种夕阳光和暖黄灯光照着旧家具、泛黄照片墙的感觉。

### 核心原则

1. **场景驱动** — 根据文章关键场景（不是标题）设计画面，2-3张场景插图 + 1张封面
2. **中文 Prompt（图片风格描述）+ 英文约束（技术参数）** — 主体描述用中文，技术负面词用英文
3. **无品牌标识** — 保持画面纯净，不加任何品牌水印
4. **不需要 ref-url** — 场景为主，非人物连续性，每张图独立生成
5. **统一暖调，不走冷灰** — 整篇文章**所有场景都用暖色调**，通过饱和度和明度变化（而非色相冷暖切换）传达情绪。失去/空荡场景用"低饱和的暖米色"而不是"冷灰蓝"，避免阴郁感
6. **风格一致性** — 插图必须继承封面5维参数中的 Palette + Rendering + Mood。封面选了A日系电影感(painterly/subtle)→插图不能出现digital或high contrast；封面选了G王家卫(digital/bold)→插图不能出现soft watercolor wash。**色调在饱和度上有差异（高饱和/低饱和），但色相始终保持在暖色系（黄/橙/暖红/米色）**

### 氛围基线（必须出现在每个 prompt）

**这是这个风格最关键的一组关键词——没有它们，模型会默认生成"老旧泛阴"的照片。** 每张图（封面 + 插图）的 prompt 开头都包含：

```
Warm nostalgic 1990s photograph, bathed in golden hour sunlight
or warm tungsten indoor lighting, soft amber glow,
gentle warm color cast, no harsh shadows,
Kodak Gold / Fujifilm Superia film stock aesthetic,
slight light leak on edges, soft halation around highlights,
NOT cold NOT gloomy NOT desaturated-blue NOT horror
```

**正向关键词（必须用）：**

- `golden hour sunlight streaming through window`
- `warm tungsten lamp light`
- `soft amber glow, honey-colored light`
- `dust motes floating in warm sunbeam`
- `cream white walls, beige wooden furniture, warm beige palette`
- `Kodak Gold 200 film stock`（暖偏黄）
- `Fujifilm Superia 400 film stock`（暖偏橙）
- `soft warm halation, light bloom around highlights`
- `gentle vignette, faded yellowish edges`

**反向关键词（禁止出现）：**

- `cold, gloomy, eerie, horror, abandoned, decayed, decayed paint, peeling wall, dark room, dim, shadowy, harsh contrast, blue tint, desaturated, desaturated-blue, cold gray, overcast`

### 封面

- 尺寸：1920x832
- 无人物或背影/侧影为主，留想象空间
- **艺术大字排版设计**：文章标题是画面的视觉主角，占据中心50-70%区域，通过艺术手法与照片交融。**不是宋体小字，是Banner级大字**
- 用户从12种文字排版风格（A-L）中选择，默认推荐 G（王家卫式字幕）— 但即使 G 王家卫，**底图也必须是暖调**，不是他电影里那种冷绿冷蓝
- 12种风格：A日系电影感 / B复古杂志风 / C自然呼吸感 / D信笺与手写 / E光影重叠 / F极简新中式 / G王家卫式 / H拍立得底栏 / I唱片封面风 / J旧报纸微头条 / K诗歌散排 / L古书扉页
- Prompt 模板见 `references/style-guide.md` 中"12种封面文字排版风格"章节

### 场景插图（无 `##` 小标题的文章）

情感文通常不加 `##` 小标题，需要 AI 阅读全文后选择 2-3 个关键场景生成插图。

**选场景规则：**

- 选画面感最强的段落，不选心理描写/议论段落
- 场景之间有情绪递进：温暖→留白→余韵，或日常→转折→回望。**不要选"失去/冷清/空荡"场景作为主插图**——这种场景可以选，但要选**有夕阳光照进来**的空荡房间，不要选阴暗房间
- 插图插入位置：紧接场景描写之后、情绪转折之前

**插图尺寸：** 1024x1024

### Prompt 模板

封面和插图模板见 `references/style-guide.md`。

**色调指南（统一暖调，通过饱和度+明度区分情绪）：**

| 情绪              | 色调关键词                                                                                                                       | 色相范围                                       |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 温暖/回忆/日常    | `warm golden tones, Kodak Gold film, soft amber glow, faded yellowish edges, gentle vignette, dust motes in sunbeam`             | 蜂蜜金 #F6AD55 / 奶油 #FFFAF0 / 暖米 #F5E6D3   |
| 失去/空荡（仍暖） | `low saturation warm beige, faded honey tones, soft golden haze, very gentle vignette, no cold colors, warm light still present` | 沙米 #E8DCC4 / 暖灰 #C9B89C / 淡金 #D4A574     |
| 克制/隐忍         | `soft warm diffused light, muted amber, no harsh shadows, quiet warm tones, golden hour lingering`                               | 暖白 #FFF4E6 / 浅金 #FFE5B4 / 米色 #F5DEB3     |
| 夜晚室内（仍暖）  | `warm tungsten lamp light, amber interior glow, cream walls, cozy living room, NO cold blue night`                               | 钨丝灯 #FFB347 / 暖琥珀 #DAA520 / 深米 #DEB887 |

**冷色禁用清单（任何场景都禁止出现）：**

- 冷蓝灰 / blue-gray / cold tint / desaturated-blue
- 月光冷感 / moonlight cold
- 阴雨 / overcast / rainy day
- 雪景冷感（除非配暖色窗光）

### 典型场景示例

下面 4 个场景示范"如何用暖调表达不同情绪"，覆盖最常见的情感治愈/怀旧文章场景：

**场景 1：童年客厅日常（最温暖）**

```
Warm nostalgic 1990s family photograph,
golden hour sunlight streaming through lace curtains into living room,
dust motes floating in amber sunbeam,
beige sofa, wooden coffee table with glass cups,
old TV in background, warm cream walls,
Kodak Gold 200 film stock, soft warm halation,
gentle vignette, faded yellowish edges,
NOT cold NOT gloomy
```

**场景 2：奶奶厨房做饭（人文烟火气）**

```
Warm nostalgic 1990s kitchen photograph,
warm tungsten overhead lamp light,
grandmother cooking at stove, steam rising in warm light,
tiled countertop, hanging utensils, ceramic bowls,
amber glow on wooden cabinets,
Fujifilm Superia 400 film stock,
cozy domestic atmosphere, no harsh shadows,
NOT cold NOT dim
```

**场景 3：放学回家路上夕阳（青春回忆）**

```
Warm nostalgic 1990s photograph of school girl walking home at sunset,
golden hour backlight, long warm shadow on asphalt road,
bicycle beside her, schoolbag on rear rack,
honey-colored sky with soft amber clouds,
cypress trees in silhouette against golden sky,
Kodak Gold 200 film stock, warm halation around sun,
nostalgic coming-of-age mood, gentle vignette
```

**场景 4：空荡房间留白（仍暖不冷）**

```
Warm nostalgic 1990s photograph of empty living room at dusk,
late afternoon golden hour light coming through window,
abandoned rocking chair with knitted throw,
dust motes in soft amber sunbeam,
unmade bed in background, warm cream walls,
low saturation warm beige palette (NOT cold gray),
gentle golden haze, Kodak Gold film stock,
quiet contemplative mood, warm NOT melancholic-cold
```

### 插入文章

封面不插入 md。场景插图插入对应场景描写之后，用 `![](images/<filename>.png)` 格式。

## Workflow C: 通用风格

When user picks from extended catalog, use corresponding prompt templates from `references/style-templates.md`.

- **风格一致性**：12种扩展风格的封面和插图模板已配对设计，但执行时必须确保插图prompt包含封面同款的 Palette + Rendering + Mood 参数。不允许封面painterly+插图digital等渲染断裂。

---

## 通用约束：Banner 设计 × 插图一致性

**适用于下面所有 Workflow F-M（新加的 8 种）。** Banner（封面）和插图不是两张图，是**同一套视觉系统的两张输出**。所有新风格都按以下规则设计：

### 5 维体系（与现有体系对齐）

| 维度          | 控制                                    | Banner 必选 | 插图继承         |
| ------------- | --------------------------------------- | ----------- | ---------------- |
| **Type**      | 构图类型（hero/typography/scene/...）   | ✅          | ❌               |
| **Palette**   | 色板（hex 值）                          | ✅          | ✅ **必须继承**  |
| **Rendering** | 渲染方式                                | ✅          | ✅ **必须继承**  |
| **Font**      | 字体（clean/handwritten/serif/display） | ✅          | ❌（插图无文字） |
| **Mood**      | 情绪对比度（subtle/balanced/bold）      | ✅          | ✅ **必须继承**  |

### Banner 设计规则（参考 baoyu-cover-image）

封面图不是"插图加大字"，是**用文字设计主导画面的视觉作品**：

1. **文字占画面 50-70% 视觉权重**。不是角落小字，是 Banner 级大字
2. **字体 × 风格匹配表**（参考 baoyu font.md）——**每张 banner 的 prompt 必须显式写 `Font Application` 段**，否则模型会渲染成默认宋体：

| Font          | 视觉特征             | 适配场景                         |
| ------------- | -------------------- | -------------------------------- |
| `clean`       | 几何无衬线，锐利均匀 | 科技/职业/家居/现代都市/测评     |
| `handwritten` | 手写/毛笔，有机变化  | 美食/萌宠/情感治愈/旅行随笔      |
| `serif`       | 经典衬线，编辑感强   | 怀旧/时尚杂志/家居/品牌          |
| `display`     | 粗体装饰，强表达     | 美食招牌/ACG标题/运动爆发/二次元 |

3. **花字技法（参考 baoyu typography.md）**——Banner 至少用一种：

| 技法          | 视觉       | 适用                   |
| ------------- | ---------- | ---------------------- |
| `gradient`    | 渐变色填充 | 美食、时尚、ACG、潮酷  |
| `stroke-text` | 描边文字   | 旅行、街头、运动、户外 |
| `shadow-3d`   | 立体投影   | 美食招牌、ACG、3D 风格 |
| `highlight`   | 高亮笔     | 测评卡、对比、关键数据 |
| `neon`        | 霓虹辉光   | 旅行夜景、ACG、赛博感  |
| `handwritten` | 手写效果   | 美食、萌宠、情感       |
| `bubble`      | 圆润气泡   | 萌宠、ACG、亲子        |
| `brush`       | 毛笔质感   | 美食、旅行、中式家居   |

4. **封面构图三件套**：
   - **视觉锚点**：主元素居中或偏左 1/3
   - **呼吸感**：40-60% 留白（背景、模糊、纯色块）
   - **文字层级**：H1 标题 100% + H2 副标题 60-70% + 标签 30%

5. **标题字体尺寸**：
   - 1920×832 banner：标题主字 220-340px 视觉高度
   - 占画面高度 30-50% 区域
   - 一行最多 8-10 个汉字（中文）或 16-20 个字符（英文）

### 插图与 Banner 的一致性约束

**生成 Banner 后，将 Banner 的 3 个继承参数原样写入每张插图 prompt：**

```
# Banner Prompt 末尾
palette: [#hex1, #hex2, #hex3]
rendering: painterly/photography/digital/...
mood: subtle/balanced/bold

# 每张插图 Prompt 开头必含
"Consistent with cover: [palette 描述], [rendering 描述], [mood 描述]"
```

**反例（不允许）：**

- Banner 写实摄影 + 插图手绘插画
- Banner 高对比 bold + 插图低饱和 subtle
- Banner 暖色调 + 插图冷色调（除非情绪递进需要，且显式声明）

### 人物一致性规则

涉及真人（时尚美妆、家居生活、ACG 角色）的插图，从第 2 张起必须传 `--ref-url`（同柔情风规则）。

---

## Workflow F: 美食类

适合探店、食谱、零食测评、地域美食、咖啡奶茶、烘焙等内容。

### 5 维默认

| 维度      | 默认值                                                                  | 说明                        |
| --------- | ----------------------------------------------------------------------- | --------------------------- |
| Type      | `hero`                                                                  | 主图放大特写                |
| Palette   | `warm` (#FFECD2 底, #ED8936 橙, #C05621 赤陶, #F6AD55 金, #A0522D 焦糖) | 暖色食物色调                |
| Rendering | `photography`                                                           | 写实美食摄影，浅景深        |
| Font      | `handwritten`                                                           | 手写 + 毛笔感，符合食物温度 |
| Mood      | `bold`                                                                  | 食欲感需要高饱和高对比      |

### Banner 设计要点

- **构图**：食物居中或偏右下 1/3，背景虚化（bokeh），45° 俯拍或正面特写
- **文字**：用 `brush` 毛笔字或 `handwritten` 手写体做主标题，加 `gradient` 渐变（橙→金）
- **关键元素**：蒸汽、拉丝、汤汁、油光、食材纹理——视觉化"温度"和"鲜"
- **示例 prompt 片段**：
  ```
  Hero food photography, 45° angle close-up of steaming [dish],
  shallow depth of field, warm golden lighting (#F6AD55, #ED8936),
  visible steam rising, glossy sauce highlights, wooden table background,
  Chinese handwritten brush calligraphy title "【主标题】" with
  orange-to-gold gradient fill (#ED8936 → #F6AD55), 220px height,
  text bottom-right with subtle drop shadow, rustic cozy atmosphere
  ```

### 插图（1:1）

继承 palette + rendering + mood，构图变化：

- 食材平铺（flat lay）俯拍
- 单品特写（macro shot）焦点在食物表面纹理
- 制作过程（手部入镜）半虚化背景
- 成品的桌面全景（lifestyle shot）

**示例 prompt 片段**：

```
Consistent with cover (warm palette, food photography, bold mood):
Overhead flat-lay of [ingredients] on parchment paper,
natural daylight, soft shadows, 50mm lens,
warm wood grain background, [accent color: #C05621] props
```

### Brand 水印：❌ 不加（食物图加水印=广告感）

---

## Workflow G: 旅行/城市类

适合旅行攻略、城市探店、风光摄影、季节游记、citywalk。

### 5 维默认

| 维度      | 默认值                                                               | 说明                                 |
| --------- | -------------------------------------------------------------------- | ------------------------------------ |
| Type      | `hero`                                                               | 城市地标或风景大场景                 |
| Palette   | `cinematic` (#1E3A5F 深蓝, #F4A261 暖橙, #E76F51 珊瑚, #2A9D8F 蓝绿) | 电影感城市色调                       |
| Rendering | `photography`                                                        | 现代写实摄影（与怀旧照片的"老"区分） |
| Font      | `display`                                                            | 粗体装饰，做"目的地"标题             |
| Mood      | `balanced`                                                           | 平衡写实和戏剧感                     |

### Banner 设计要点

- **构图**：地标建筑居中，天空占 40-50%，用引导线（街道、河流）引向主元素
- **时间感**：黄昏（golden hour）/ 蓝调时刻（blue hour）/ 城市夜景三种主调任选
- **文字**：用 `stroke-text` 描边字（白字黑边）或 `neon` 霓虹（夜景主题），副标题用 `clean` 衬线小字
- **季节元素**：樱花/红叶/雪/雨/雾——一个就够了
- **示例 prompt 片段**：
  ```
  Hero landscape photography, [city] skyline at blue hour,
  cinematic color grading, deep navy sky (#1E3A5F) with coral sunset (#E76F51),
  iconic [landmark] centered, leading lines of [street/river],
  bold display typography title "【城市名】" 280px white stroke-text
  with navy outline (#0D1B2A), positioned top-center,
  clean sans-serif subtitle "【副标题】" 60% size below,
  subtle film grain, balanced contrast
  ```

### 插图（1:1）

继承 palette + rendering + mood，构图变化：

- 街角特写（人文细节）
- 食物/咖啡（场景里的）
- 当地人物背影（不露脸）
- 小巷/屋顶/窗户（氛围细节）

### Brand 水印：✅ 可加（专业旅行内容合适）

---

## Workflow H: 萌宠/Q版类

适合萌宠号、亲子号、治愈系内容、表情包、Q版头像。

### 5 维默认

| 维度      | 默认值                                                                  | 说明                           |
| --------- | ----------------------------------------------------------------------- | ------------------------------ |
| Type      | `character`                                                             | 角色为主（写实宠物 / Q版拟人） |
| Palette   | `pastel` (#FFE5E5 粉, #E5F5FF 蓝, #FFF4D6 黄, #D4F4DD 绿, #B5E5CF 薄荷) | 马卡龙/奶油色                  |
| Rendering | `painterly`（写实萌宠） / `flat-vector`（Q版）                          | 二选一                         |
| Font      | `display`                                                               | 圆润装饰字体                   |
| Mood      | `balanced`                                                              | 暖但不刺眼                     |

### Banner 设计要点

- **构图**：单一萌宠/角色居中，留 40% 留白做"互动感"
- **文字**：用 `bubble` 气泡字或 `handwritten` 手写体，加 `bubble` 圆角
- **细节**：拟人化元素（小帽子、蝴蝶结、表情气泡）一个就够
- **示例 prompt 片段（Q版）**：
  ```
  Q-version pet illustration, [animal] character with [accessory],
  pastel color palette (#FFE5E5 cream pink, #E5F5FF baby blue),
  flat-vector rendering, soft rounded shapes, no outlines,
  centered composition, 40% breathing room,
  bubble-style display typography title "【主标题】" 240px
  with cream fill and coral stroke (#E8655A),
  gentle smile expression, storybook illustration style
  ```

### 插图（1:1）

继承 palette + rendering + mood：

- 不同动作/姿态（同角色）→ 必须传 `--ref-url` 保持角色一致性
- 不同场景（家、户外、医院、节日）
- 对话气泡（漫画式分镜）

### Brand 水印：❌ 不加

---

## Workflow I: 家居/生活类

适合家装、装修、好物、生活方式、MUJI/北欧/中式风格展示。

### 5 维默认

| 维度      | 默认值                                                                         | 说明               |
| --------- | ------------------------------------------------------------------------------ | ------------------ |
| Type      | `hero`                                                                         | 房间全景或单品陈设 |
| Palette   | `earth` (#F5F0E8 米白, #D4B896 沙色, #8B7355 木色, #2F4F4F 深绿, #C19A6B 焦糖) | 自然/木质/大地色   |
| Rendering | `photography`                                                                  | 室内写实摄影，柔光 |
| Font      | `serif`                                                                        | 衬线字体，编辑感强 |
| Mood      | `subtle`                                                                       | 低饱和，安静感     |

### Banner 设计要点

- **构图**：45° 视角房间全景，窗户自然光从左/右上射入
- **文字**：用 `serif` 衬线主标题，干净不抢戏
- **细节**：植物、木质、棉麻、陶瓷——传递"质感"而非"贵"
- **示例 prompt 片段**：
  ```
  Interior design photography, [style: MUJI/Nordic/Japanese] living room,
  45-degree angle, soft natural window light from upper right,
  earth palette (#F5F0E8 cream walls, #D4B896 wooden floor,
  #8B7355 walnut furniture), shallow depth of field,
  serif typography title "【主标题】" 200px deep forest green (#2F4F4F),
  positioned upper-left, plenty of negative space,
  minimalist composition, subtle contrast, lifestyle magazine aesthetic
  ```

### 插图（1:1）

继承 palette + rendering + mood：

- 单品特写（家具、器皿、绿植）
- 局部细节（窗帘褶皱、木纹、陶土质感）
- 平面俯拍（flat lay）
- 户型图/平面图（用 infographic 替代）→ 见 Workflow L

### Brand 水印：✅ 可加

---

## Workflow J: 时尚/美妆类

适合穿搭、美妆教程、产品测评、lookbook、护肤成分党。

### 5 维默认

| 维度      | 默认值                                                                   | 说明           |
| --------- | ------------------------------------------------------------------------ | -------------- |
| Type      | `hero`                                                                   | 全身或半身人物 |
| Palette   | `elegant` (#FAFAFA 白, #1A1A1A 黑, #C9A96E 金, #8B4513 棕, #D4A09A 玫瑰) | 高级简约       |
| Rendering | `photography`                                                            | 时尚杂志摄影   |
| Font      | `serif`（高端） / `display`（街头潮流）                                  | 二选一         |
| Mood      | `bold`                                                                   | 高对比，强视觉 |

### Banner 设计要点

- **构图**：人物偏左/右 1/3，背景纯色或城市模糊
- **文字**：用 `gradient` 渐变金（#C9A96E → #E6D5A8）或 `display` 粗体装饰字
- **关键元素**：妆容特写、服饰质感、配饰、姿势——杂志级pose
- **示例 prompt 片段**：
  ```
  High-fashion editorial photography, full-body portrait of [subject description],
  elegant palette (#FAFAFA ivory background, #1A1A1A black accents,
  #C9A96E gold jewelry), studio lighting with single key light from upper left,
  magazine cover composition, subject offset to right third,
  bold serif display typography title "【主标题】" 260px
  with gold gradient fill (#C9A96E → #F4E4BC),
  positioned left side, sharp focus, bold contrast,
  fashion week aesthetic
  ```

### 插图（1:1）

继承 palette + rendering + mood，**人物必须传 `--ref-url` 保持一致性**：

- 妆容步骤分解（before / after / step 1-3）
- 单品陈设（包、鞋、配饰平铺）
- 街拍/生活场景
- 成分/配方信息图（用 Workflow L 风格叠加）

### Brand 水印：✅ 可加（时尚品牌合适）

---

## Workflow K: ACG/二次元类

适合番剧推荐、cosplay、二次元资讯、手游（抽卡/角色/皮肤）、轻小说。

### 5 维默认

| 维度      | 默认值                                                                     | 说明                            |
| --------- | -------------------------------------------------------------------------- | ------------------------------- |
| Type      | `character`                                                                | 角色为主                        |
| Palette   | `vivid` (#FF6B9D 樱粉, #6BCB77 草绿, #4D96FF 群青, #FFD93D 金, #C780FA 紫) | 高饱和动漫色                    |
| Rendering | `flat-vector`                                                              | 赛璐璐/原神风（手绘赛璐璐上色） |
| Font      | `display`                                                                  | 粗体装饰，漫画/标题感           |
| Mood      | `bold`                                                                     | 高饱和高对比                    |

### Banner 设计要点

- **构图**：角色立绘居中或偏左 1/3，背景加战斗/光效元素
- **文字**：用 `shadow-3d` 立体投影字（漫画标题感）或 `neon` 霓虹（赛博风）
- **细节**：眼睛要大、头发要飘、武器/魔法光效——视觉化"力量"
- **示例 prompt 片段**：
  ```
  Anime cel-shaded illustration, original character [description],
  vivid color palette (#FF6B9D sakura, #4D96FF cobalt, #FFD93D gold),
  flat-vector rendering with hard cel-shading and minimal gradients,
  centered character composition with magical particle effects,
  40% breathing space upper area,
  bold display typography title "【主标题】" 280px
  with 3D shadow extrusion (front color #FFD93D, shadow #1A1A1A),
  positioned top, anime key visual style, dynamic pose,
  high contrast, Genshin Impact aesthetic
  ```

### 插图（1:1）

继承 palette + rendering + mood，**角色必须传 `--ref-url`**：

- 不同动作/表情
- 战斗/技能释放场面
- 角色与场景互动
- Q版头像（4 头身简化版）—— 切换到 `flat-vector` 简化版

### Brand 水印：❌ 不加（二次元同人/商业敏感）

---

## Workflow L: 测评/信息图类

适合产品横评、App 测评、3C 数码、成分党、榜单排行、数据新闻。

### 5 维默认

| 维度      | 默认值                               | 说明                     |
| --------- | ------------------------------------ | ------------------------ |
| Type      | `infographic`                        | 信息结构主导（不是插图） |
| Palette   | `mono`（黑白灰） / `macaron`（彩卡） | 二选一                   |
| Rendering | `flat-vector`                        | 矢量/几何分块            |
| Font      | `clean`                              | 几何无衬线，最强可读性   |
| Mood      | `balanced`                           | 数据需要清晰可读，不抢戏 |

### Banner 设计要点

- **构图**：上半部分大标题 + 评分/价格数字，下半部分产品图/对比图
- **文字**：用 `highlight` 高亮笔标关键数据（"省 30%""9.5 分"），用 `clean` 几何字做主标题
- **关键元素**：评分卡、对比表、雷达图、icon 矩阵——视觉化数据
- **示例 prompt 片段**：
  ```
  Modern infographic layout, product comparison visual,
  mono palette with accent (#FAFAFA background, #1A1A1A black,
  #E8655A coral accent for highlights),
  flat-vector rendering, geometric grid system,
  upper area: bold clean sans-serif title "【主标题】" 240px black,
  with yellow highlighter mark behind key word,
  lower area: 3-column product cards with score badges (★★★★★),
  clean icon system, data-forward design, Apple keynote aesthetic
  ```

### 插图（1:1）

继承 palette + rendering + mood：

- **测评卡**：单品评分（5 维雷达图、星级、价格、推荐指数）
- **对比图**：2-4 个产品 A/B 横评
- **流程图**：从购买到使用的步骤
- **排行榜**：TOP 10 列表
- **数据可视化**：饼图、柱状图、地图热力

插图 prompt 不需要文字，**数据和文字用 prompt 中明确写出，模型直接渲染**。

### Brand 水印：✅ 可加（专业测评合适）

---

## Workflow M: 运动/健身类

适合健身教程、运动品牌、跑步/瑜伽/球类、马拉松、减肥。

### 5 维默认

| 维度      | 默认值                                                                     | 说明                         |
| --------- | -------------------------------------------------------------------------- | ---------------------------- |
| Type      | `hero`                                                                     | 人物动态为主                 |
| Palette   | `vivid` (#FF4500 橙红, #1E1E1E 黑, #00C9A7 青绿, #FF6B35 金, #2C3E50 深蓝) | 力量感强对比                 |
| Rendering | `photography`                                                              | 运动摄影（高速快门凝固动作） |
| Font      | `display`                                                                  | 粗体爆发感                   |
| Mood      | `bold`                                                                     | 高对比，高能量               |

### Banner 设计要点

- **构图**：人物动态瞬间，斜对角构图（45° 倾斜线）
- **文字**：用 `stroke-text` 描边（白字+黑边/橙边）或 `shadow-3d` 立体投影
- **关键元素**：汗水、肌肉线条、运动模糊、装备特写——传递"力量"
- **示例 prompt 片段**：
  ```
  Sports action photography, [sport: running/weightlifting/yoga] athlete
  in dynamic motion, frozen mid-action with high shutter speed (1/1000s),
  vivid palette (#FF4500 energy orange, #1E1E1E charcoal,
  #00C9A7 vitality teal), dramatic side lighting,
  diagonal composition with strong leading lines,
  bold display typography title "【主标题】" 260px
  white with orange stroke (#FF4500 4px), positioned top-left,
  motion blur on limbs, sweat droplet details, bold contrast,
  Nike ad campaign aesthetic
  ```

### 插图（1:1）

继承 palette + rendering + mood：

- **动作分解**：连续动作序列（4 宫格分解图）
- **装备特写**：球鞋、运动服、器材
- **对比图**：训练前/后
- **数据展示**：心率、卡路里、训练量
- **场景**：球场、跑道、健身房、户外

### Brand 水印：✅ 可加（运动品牌常见）

---

## Workflow Q: 轻量涂鸦Q版（草根手绘 + 圆润Q版角色 + 涂鸦风，#17，2026-06-07 加）

**定位**：给人物/概念/品牌的"草根 Q版"风格。**非日漫、非韩漫、非萌系**——明确不与 Workflow H 萌宠Q版（限定宠物主体）、Workflow K ACG二次元（日式赛璐璐/原神风）撞。

**5 维**：
- **Type**: `character`（Q版人物为主，不是"宠物拟人"也不是"日漫角色"）
- **Palette**: `warm-pastel` + `cream` 暖底（**非 Kawaii 的马卡龙/粉系**，**非 ACG 的冷色赛璐璐**）—— 偏暖米白 + 焦糖棕 + 1 个柠檬黄高亮
- **Rendering**: `hand-drawn` + `doodle`（**手绘线条 + 涂鸦抖动**——不是 ACG 那种"勾线笔"赛璐璐，也不是 Excalidraw 那种工程师白板草稿；是介于两者之间的"草根随笔"涂鸦）
- **Font**: `handwritten`（中文用思源黑体/手写体；英文字体 casual marker）
- **Mood**: `balanced`（不极端萌也不冷）

**差异化锚点**（避免 3 个现有风格撞）：

| 区别于 | 关键差异 |
|---|---|
| **#6 萌宠Q版** | 萌宠Q版限定"动物主体"；Q版是"草根人物/概念"，可以给任何题材 |
| **#9 ACG二次元** | ACG 是"日式赛璐璐/原神风"（日漫感强）；Q版是"草根手绘"（无日漫感，线条更简单更圆润）|
| **#5 sketch-notes** | sketch-notes 是"笔记本 Macaron 暖色 + 学习/笔记场景"；Q版是"草根人物角色 + 通用"（有具体 Q版人物/概念主体）|
| **#1 科技 Excalidraw** | Excalidraw 是"工程师白板草稿"（极简线条/无人物）；Q版有具体 Q版人物角色 |
| **#7 Kawaii（扩展）** | Kawaii 是"粉色/糖果色日式可爱"（马卡龙/糖果/星星/桃心）；Q版是"焦糖暖棕 + 草根"（更朴实不"少女") |

**出图时强制委派**（同 Workflow A banner 委派模式）：

```python
# 在 /luoboa-illustrate 调 baoyu-article-illustrator
# 关键：让 baoyu-article-illustrator 知道是 "草根Q版" 不是 "Kawaii日漫"
invoke_skill("/baoyu-article-illustrator", args={
  "style": "hand-drawn-q-version",  # 不是 kawaii / acg / anime
  "subject": "<人物/概念/品牌名>",
  "audience": "<读者画像>",
  "mood": "warm, casual, doodle, grassroot, NOT anime, NOT kawaii",
  "constraints": [
    "rendering: hand-drawn doodle, NOT excalidraw whiteboard, NOT anime cel-shaded",
    "subject must be a Q-version character (大头大身比, 2-3 heads tall, 圆润线条)",
    "no Japanese manga visual cues (no big sparkly eyes, no anime hair spikes)",
    "no Kawaii pastel pink overload (no hearts, no stars, no macaron colors)",
    "palette: warm cream #FAF0E6 + 焦糖棕 #8B5A3C + 1 lemon yellow #F4D03F highlight",
    "中文 must be handwritten-style font, 14-18pt, 清晰可读"
  ]
})
```

**触发关键词**：`涂鸦Q版` / `手绘Q版` / `轻量涂鸦` / `草根Q版` / `Q版手绘` / `doodle Q` / `hand-drawn Q` / `grassroot Q` / `casual Q版` —— 任何明确说"我要 Q版 + 手绘 + 不要日漫感"的请求。

**完整 prompt 模板**见 `references/style-templates.md` 行 ~228+（"## ✏️ 14: 轻量涂鸦Q版" 章节）。

### Brand 水印：✅ 可加（草根品牌/IP 类常见）

---

## Workflow D: 快文配图（按句生成 8-bit 极客像素风复古游戏机配图）

适合短平快的文章、**每句一图**的批量配图需求（公众号内文、视频脚本、PPT 配图、新闻合集、卡片集等）。**风格参考极客公园 萝卜啊 的复古游戏机像素海报**——黑白主导 + 黄色高亮 + 复古游戏 UI + 关键词橙色高亮 + 8-bit 像素角色。

**核心特点**：

- **每句一图，不限制数量**（100+ 句也要全跑）
- **8-bit 像素艺术风格**（不是写实照片、不是 3D、不是手绘水彩）—— 黑白主导 + 1-2 个高亮色（黄/红/橙）
- **关键词橙色高亮**是核心特色：句子里的关键名词/动词/数据用纯橙色 (#FF6B35) 像素字呈现，其他文字纯黑
- **极简底栏**：底部居中显示 "luoboa.com 萝卜啊"（用 chunky 8-bit 像素字，橙 #FF6B35）—— 去掉进度、1/N 标签、时间、血条、能量条、左右布局
- 走 dreamina CLI（**像素艺术必须用 `--model_version=high_aes_general_v50` 或类似，不锁 4.7**——4.7 偏 Q 版马克笔）

### Step 1: 读取文章并拆分句子

Read the target `.md` file. Then:

1. 去掉图片行 `![](...)`
2. 去掉空行和 markdown 格式标记（\*\*、#、- 等等）
3. 按句号/问号/感叹号/换行拆分：`re.split(r'[。！？\n]+', text)`
4. 过滤短于 3 字的片段
5. 超过 50 字的句子**智能截断**（到上一个逗号，否则直接截断加省略号）—— **不截断优先**：长句可分两图，第一句完结，第二句接续
6. **不合并句子**——每句独立配图，**不要合并"一句话生成 1 张"以外的逻辑**
7. 展示拆分结果 + 每张图的具体画面构思，让用户确认（可增删改句子）

### Step 2: 选择画面比例（**必做！**）

快文配图**不是必须竖屏**——用户可能想出横屏给视频号横屏/小红书横屏/公众号封面/朋友圈/微博头图。**必须问用户比例**，不要默认 9:16。

| 选项                    | 比例   | 描述                                                 |
| ----------------------- | ------ | ---------------------------------------------------- |
| 📱 **9:16 竖屏**        | `9:16` | 竖版——抖音、快手、视频号、朋友圈、小红书、微博微头条 |
| 🖥️ **16:9 横屏**        | `16:9` | 横版——B站、YouTube、横屏视频号、电脑端展示           |
| ⬜ **1:1 方形**         | `1:1`  | 正方形——公众号次条、小红书贴纸、微信图片消息         |
| 🎬 **21:9 宽幅 banner** | `21:9` | 超宽 banner——公众号封面、网页 banner                 |
| 📷 **4:3 经典**         | `4:3`  | 经典 4:3——演示文稿、传统相机比例                     |
| 📖 **3:4 杂志竖版**     | `3:4`  | 杂志风竖版——小红书贴纸长图、杂志内文                 |

**判断用户已暗示的比例**：

- 用户说"竖屏"/"抖音/快手/视频号/朋友圈" → 默认 9:16
- 用户说"横屏"/"B 站/YouTube" → 默认 16:9
- 用户说"封面/banner" → 默认 21:9
- 其他情况一律询问，让用户选

**所有 6 个比例都支持 dreamina CLI**（dreamina 支持 `21:9 16:9 1:1 9:16 4:3 3:4` 等）。

### Step 3: 选择像素风格（**核心：8-bit 复古游戏机美学**）

Show 6 个像素风格（from `references/quick-styles.md`）：

| #   | 风格 | 一句话描述 |
| --- | --- | --- |
| 1   | 🎮 **8-bit 极客黑白** (default) | 纯黑白 + 橙色高亮，萝卜啊 同款，半色调网点 |
| 2   | 🤖 机器人像素彩 | 黑白 + 红色高亮，硬核科技感 |
| 3   | 💚 GameBoy 绿屏 | 4 级绿阶 + 黄色高亮，极致 80s 复古 |
| 4   | 📺 16-bit 街机 | 像素密度 2x，色彩更丰富 |
| 5   | 🎰 街机红黄 | 黑白 + 红+黄双高亮，复古街机 UI |
| 6   | 💾 磁带/磁盘像素 | 8-bit 灰阶 + 黄色高亮，80s 科技风 |

Default: 1 (8-bit 极客黑白) for 一般快文（最接近 萝卜啊 原版）。

**关键渲染提示词**（每张图必加）：

```
Pure 8-bit pixel art, retro game console aesthetic (Game Boy era),
1-bit monochrome (pure black on pure white) with 1-2 spot colors only,
halftone dot pattern for shading, sharp pixel edges (NOT anti-aliased),
blocky pixel characters (Game Boy sprite style, 1px stroke width),
chunky 8-bit typography for any text,
NOT photorealistic, NOT 3D, NOT anime, NOT smooth vector art,
NOT watercolor, NOT sketch, NOT hand-drawn brush strokes
```

### Step 4: 确认 Dreamina CLI 环境可用

**快文配图固定使用 dreamina，模型用 `high_aes_general_v50`**（不用 4.7——4.7 偏 Q 版马克笔，跟像素艺术冲突）。v50 在 8-bit 像素、复古 UI、GameBoy 风格上更稳。

```bash
which dreamina   # 检查是否在 PATH 中
dreamina user_credit   # 验证登录状态和余额
```

如果未安装，告诉用户：

```
请先安装 Dreamina CLI 并完成登录：
1. 从官方渠道获取 dreamina CLI
2. 运行 dreamina login 完成 OAuth 登录
3. 运行 dreamina user_credit 确认可用
```

### Step 5: 批量生成图片（dreamina v50）

**重要：每张图都是一个独立的"8-bit 像素角色 + 中文粗体标题（关键词橙高亮）+ 复古游戏 UI 底栏"组合**。每张图的 prompt 必须明确：

```
8-bit pixel art illustration in retro Game Boy / NES console aesthetic.
Pure monochrome (black on white) with ONE spot color (bright orange #FF6B35
or red #E8453C). Halftone dot pattern for shading. Sharp 1-px pixel edges
(NOT anti-aliased, NOT smooth vector). Blocky chunky 8-bit sprite
characters. No curves, only right angles and stepped diagonals.

LAYOUT (top to bottom):
1. TOP 35% — large bold chunky 8-bit Chinese title (黑色 32pt+ 像素字), 
   with KEYWORD(s) highlighted in bright orange #FF6B35 or red #E8453C.
   The title renders the article sentence verbatim, but only the
   important noun/verb/data is orange, the rest is black.
2. MIDDLE 50% — pixel-art 8-bit subject (角色/物件/场景), 
   with sharp black outlines + halftone dot shading.
3. BOTTOM 15% — minimal UI bar: centered text "luoboa.com 萝卜啊"
   in chunky 8-bit pixel font, bright orange #FF6B35. No progress,
   no 1/N labels, no time, no health bars, no left/right split — purely
   centered single line.

Subject: <句子核心意象 — 一个 8-bit 像素角色/物件 in 场景>.
Key elements: <1-3 个具体物件>, 关键高亮词: <关键词 1-2 个>.

Pure 1-bit monochrome + 1-2 spot colors only. NOT photorealistic,
NOT 3D rendering, NOT anime, NOT watercolor, NOT sketch,
NOT hand-drawn brush strokes, NOT smooth gradients.
```

**单次命令**（模型 v50，像素艺术专用）：

```bash
dreamina text2image \
  --prompt="<每句独立的 8-bit 像素 prompt>" \
  --ratio=<用户选的比例> \
  --model_version=high_aes_general_v50 \
  --resolution_type=2k \
  --poll=180
```

**批量策略**（按句子数量分批）：

| 句子数量  | 策略                                                     |
| --------- | -------------------------------------------------------- |
| ≤10 句    | 全部并发（每 3 个一组），失败重试 1 次                   |
| 11-30 句  | 分 3-5 批并发，每批 3-5 个                               |
| 31-100 句 | 分 5-10 批，每批 3-5 个                                  |
| 100+ 句   | **必分批**（每批 ≤5 个），不要一次性并发，会触发速率限制 |

**每一批的并发数不超过 5 个**（dreamina 速率限制经验值）。

**流程**：

1. 遍历拆分好的句子列表
2. 每句构建 prompt（含具体场景描述 + 人物 + 动作 + 环境）
3. 启动 dreamina text2image（每批 3-5 个并发）
4. 等待一批完成 → 下载到 `quick/NN.png` → 启动下一批
5. 失败的重试 1 次，仍然失败则跳过并标记 ❌
6. 全部完成 → 写入 `sentences.txt`

### Step 6: 输出

Directory structure:

```
article/<MMDD>/<ArticleName>/quick/
├── 01.png          (第1句的图，按用户选的比例)
├── 02.png          (第2句的图)
├── ...
├── NN.png          (最后一句的图)
└── sentences.txt   (序号|原文|状态 对照表)
```

`sentences.txt` format:

```
01|人类本质是上下文窗口只有7的大模型|✅
02|幻觉比GPT还严重|✅
03|OpenAI发布o1模型的时候|❌
```

**Does NOT modify the original markdown file.**

### 关键规则（**重要！**）

⚠️ **快文是 8-bit 像素海报，不是 PPT/水彩/3D**：

- ❌ 不要写实摄影、水彩、油画、3D 渲染
- ❌ 不要抗锯齿（要锐利像素边缘）
- ❌ 不要彩色水彩渐变
- ✅ **纯黑白 + 1-2 个高亮色**（默认橙 #FF6B35 萝卜啊频道色，可换红 #E8453C）
- ✅ **关键词橙色高亮**——句子里的关键名词/数据/动词用纯橙像素字
- ✅ **粗黑体中文标题**（像素字，≥32pt 视觉尺寸）
- ✅ **半色调网点**（dithering/halftone）做阴影
- ✅ **极简底栏**：居中 "luoboa.com 萝卜啊"（chunky 8-bit 像素字，橙 #FF6B35）
  - ❌ **不要计时器/00:00**（不是关卡截图）
  - ❌ **不要弹"弹"字/子弹/能量条**（不是游戏 UI）
- ✅ 30+ 句话/100+ 句话全跑完
- ✅ **必须渲染文字**（关键词橙色高亮是核心特色，模型必须能渲染中文）

### dreamina 注意事项

- 末尾必含 `8-bit pixel art, halftone dot pattern, sharp pixel edges`
- 强调 `pure 1-bit monochrome, spot color orange #FF6B35, Game Boy aesthetic, retro game console UI`
- 排除 `photorealistic, 3D, anime, watercolor, sketch, hand-drawn brush, anti-aliased, smooth gradients, vector art`
- 模型用 `high_aes_general_v50`（**不要用 4.7**——4.7 偏 Q 版马克笔，跟像素艺术冲突）
- 文字必须渲染（这是 萝卜啊 风格的核心标志），dreamina v50 对中文像素字渲染较稳
- 颜色严格控制：纯黑 + 纯白 + 1-2 个高亮色（黄/红），**不要让模型自由加第 3、第 4 种颜色**

## Workflow N: 微头条配图（马克笔 Q 版卡通）

适合「每日AI快讯」类多新闻合集文章（如 `news/2606/0603.md`）。每条新闻生成 1 张 9:16 竖版**马克笔 Q 版卡通**配图——**风格独立于 Workflow D**（D 现在用 8-bit 像素，N 保持 Q 版马克笔，因为新闻合集更适合 Q 版）。

**风格定位：** 🖍️ 马克笔 Q 版卡通（marker-q-chibi）—— 二头身大头小身体 + 夸张表情 + 汗珠等情绪符号 + 黑色手绘马克笔/平板笔刷线条 + 低饱和度色块平涂 + 大量手写体文字 + 颜色高亮 + 手绘小图标散落。

**默认提示词语言：中文。** scene_zh 字段是中文场景描述（grsai/dreamina 都支持中文 prompt）。

**与 Workflow D（快文配图）的核心差异：**

| 维度 | Workflow D（快文）      | Workflow N（微头条）          |
| ---- | ----------------------- | ----------------------------- |
| 后端 | Dreamina CLI（4.7）     | **用户选（API / CLI）**       |
| 比例 | 用户选（16:9/9:16/1:1） | **9:16** 固定                |
| 场景 | 文章每句配 1 张         | 每条新闻配 1 张               |
| 风格 | 马克笔 Q 版             | 马克笔 Q 版（**完全同快文**） |
| 文字 | 巨型手写体              | 巨型手写体 + 颜色高亮         |

### Step 1: 读取并解析新闻文件

读取目标 `.md` 文件，提取：

- **报头日期**：从文件名（如 `0603.md` → `6月3日`）或文档首行（如 "📰 每日AI快讯 | 6月3日"）解析
- **分类标签**：解析 `【🔥 AI大模型】` 等分类段（保留供 chip 配色）
- **新闻条目**：每条 `**{N}. {标题}** {描述}` 拆为 1 个 dict

### Step 1.5: 选择后端（**必做！不要默认**）

微头条生图**不默认走 API**。必须问用户：

| 选项 | 优点 | 缺点 | 适合 |
|------|------|------|------|
| **🟢 grsai API**（推荐） | 出图质量好、Q 版稳定 | 中文字偶发乱码 | 重要封面/视觉优先 |
| **🔵 Dreamina CLI** | 中文稳、文字渲染强 | Q 版效果略弱、模型只到 5.0 | 文字密集、需快速出 |

用户默认选 API（质量优先），但**必须显式问**而不是直接选。

### Step 2: AI 提炼每条新闻（关键步骤）

对每条新闻，AI 生成 4 个字段：

1. **`short_title`（精简标题）**：≤ 22 字（推荐 18 字内），保留核心主体+事件
2. **`bullets`（3 条关键事实）**：每条 ≤ 18 字，必须有数字/专有名词/关键动作
3. **`category`（分类）**：从 4 个分类中选一：`AI大模型` / `AI Agent` / `AI工具` / `AI行业动态`
4. **`scene_zh`（中文场景描述）**：1-2 句中文，描述该新闻对应的**视觉化可画场景**（人物+动作+环境）

**Bullet 提炼规则：**

- 保留：具体数字、专有名词、关键动作
- 删除：修饰语、连接词、模糊表达
- 3 条要有递进或并列关系，不能重复

**用户确认环节**：展示 `原标题 → 精简标题 / 3 bullets / 分类 / 场景描述` 对照表，让用户增删改后再出图。

完整 10 个场景示例见 `references/news-styles.md` 第 5 节。

### Step 3: 构建 Prompt 模板（6 区布局）

每张图采用 **balanced 多区布局**（参考 baoyu-xhs-images 布局）：

```
[报头区 5%]       黑色横条 + 白字 "每日AI快讯 6月3日"
[分类 chip 6%]    左上角 macaron 色彩徽章 "【AI大模型】"
[标题区 12%]      大字手绘标题 "「xxx」"
[Bullet 区 18%]   奶油色块 + 3 个珊瑚红点 bullet
[插图区 50%]      墨水速写 + 淡彩水洗场景
[Footer 3%]       底部小字 "# 01 | 6月3日"
```

**完整 prompt 模板：**

```
9:16 vertical hand-drawn news card.
Top 5% is a black header bar with white text "每日AI快讯 {date}" (crystal clear, no garbling).
Below header on the left, a macaron {category_color_fill} category chip with Chinese text "【{category}】".
Title: 「{short_title}」 in dark gray, handwritten style with slight wobble.
Bullet block in cream (#F5F0E8) with 3 hand-drawn points in coral red dots:
  • {bullet_1}
  • {bullet_2}
  • {bullet_3}
Lower 50% scene: pen-and-ink sketch with light watercolor wash in macaron accent color, cream paper background, illustrating: {scene_en}.
Footer: "# {num:02d} | {date}".
Style: hand-drawn ink with intentional wobble, light watercolor wash NOT full color NOT black and white, macaron palette cream background pastel zones coral red accent, educational infographic sketch aesthetic, New York Times op-ed meets hand-drawn study card. Text rendered cleanly without garbled characters. NO photographic, NO digital gradients, NO anime, NO realistic shading, NO 3D rendering.
```

### Step 4: 批量出图（强制 Dreamina CLI）

```bash
dreamina text2image \
  --prompt="<完整 prompt>" \
  --ratio=9:16 \
  --resolution_type=2k \
  --model_version=high_aes_general_v50 \
  --poll=120
```

**注意：dreamina `text2image` 不支持 `--ref-url`**，无法像 API 那样传参考图保持人物一致性。10 张图的画风一致性**完全靠 prompt 关键词约束**（一致性块 + 冗余关键词）。

**串行生成**：默认单次串行 10 次（避免触发速率限制）。失败重试 1 次（强化风格关键词），第二次仍失败则跳过并标记 `❌`。

### Step 5: 下载并归档

每张图从 `dreamina query_result` 返回的 JSON 中提取 `result_json.images[0].image_url`，用 `urllib.request.urlretrieve` 下载。

输出目录：

```
article/0603/0603-AI快讯/
└── news/
    ├── 01-anthropic-ipo.png
    ├── 02-gpt56-release.png
    ├── ...
    ├── 10-unitree-ipo.png
    └── manifest.txt
```

**manifest.txt 格式**（pipe-separated）：

```
01|AI大模型|Anthropic冲史上最大 IPO|已提交上市招股书|冲击AI行业最大规模IPO|教皇预警2030年AGI|✅
02|AI大模型|GPT-5.6 今晚杀到|OpenAI 即将发布 GPT-5.6|奥特曼亲自预告|基准测试刷新纪录|✅
...
```

字段顺序：`| 序号 | 分类 | 精简标题 | bullet1 | bullet2 | bullet3 | 状态(✅/❌) |`

### Step 6: 不修改原 .md

微头条配图和快文配图一样，**不修改原文章**。封面/配图作为独立素材使用。

### 5 维默认值

| 维度      | 默认值                                  | 说明                            |
| --------- | --------------------------------------- | ------------------------------- |
| Type      | `infographic-sketch`                    | 教育信息图速写                  |
| Palette   | `macaron`（cream + 4 色 chip + 珊瑚红） | 有色彩的暖系                    |
| Rendering | `colored-pencil`                        | 彩色铅笔（可见笔触 + 多色叠加） |
| Font      | `handwritten`                           | 手写字体（带轻微 wobble）       |
| Mood      | `balanced`                              | 平衡戏剧性与可读性              |

### 4 个分类的配色

| 分类         | 填充色       | 配色名       |
| ------------ | ------------ | ------------ |
| `AI大模型`   | `#A8D8EA` 蓝 | macaron blue |
| `AI Agent`   | `#D5C6E0` 紫 | lavender     |
| `AI工具`     | `#B5E5CF` 绿 | mint         |
| `AI行业动态` | `#F8D5C4` 桃 | peach        |

### 文字渲染注意事项

- **6 个文字区**都需要清晰渲染
- 顶部报头：固定 5% 画面高度
- 标题：占 12%，字号最大
- Bullets：占 18%，每条 4-6% 高度，珊瑚红点
- 场景：占 50% 主体
- Footer：占 3% 小字
- 末尾必须加 `Text rendered cleanly without garbled characters`

### 失败重试策略

如果生成的图片文字乱码或风格跑偏：

1. 第一次重试：强化 `EXTRABOLD` 字体描述 + 加大字号
2. 第二次重试：去掉 chip 颜色描述对文字的影响
3. 第三次重试：拆分长文字为 2 行
4. 如果整张图明显跑偏（变成照片/纯黑白/卡通），整个 prompt 重新生成

### 触发关键词

直接说"微头条配图"/"新闻配图"/"资讯配图"/"AI快讯配图"也能触发本 Workflow。

---

## Workflow Z: 知乎文配图（白底黑字 + 流程图/统计图/知识图谱）

适合**知乎高赞回答、36kr/钛媒体深度文章、技术博客教程、产品分析类公众号**。
整体气质：**「让数据和逻辑自己说话」**——白底黑字、极少量彩色标记、专业感强、像一份精修过的咨询报告或学术图解。

> ⚡ **执行规则（覆盖全局 Step 3 的"后端选择:必须问用户"）**
> **🆕 2026-06-08 修订：知乎文配图默认改走 API**（`scripts/generate.py`，provider 走 config.yaml 默认），不调用 Dreamina CLI。
> 原因：实测中 Dreamina CLI 在知乎文配图上 3 类问题集中爆发——① 多 subagent 并行时 dreamina 队列阻塞（`querying` 卡 5+ 分钟无响应）② 即使出图也常跑出 macaron 插画风（猪猪银行/计算器/笔记本）而不是白底矢量信息图 ③ 中文 prompt 在 dreamina 上 v42/v50 模型创造力盖过指令，可控性差。API（grsai gpt-image-2 / openai）出白底矢量信息图稳定，中文渲染清晰。
> 仅在用户**明确说"用 Dreamina / 即梦 / CLI"**时才切到 Dreamina CLI，并提示有上述失败风险。
> API 模板见下面"知乎专用规则"。

### 5 维默认

| 维度 | 默认值 |
|------|--------|
| Type | dataviz (cover) / dataflow (插图) |
| Palette | zhihu-mono: 纯白底 / 纯黑字 / 知乎蓝（深一点的群青蓝） / 浅灰（方框/连线/行底） / 极少量暖橙（高亮强调） |
| Rendering | clean-digital（矢量、锐利 1-2px 描边、无 painterly/film grain/sketch 杂色） |
| Font | clean-sans（思源黑体 / Inter / 苹方 / 微软雅黑 — 中文必须清晰锐利） |
| Mood | subtle-professional（高对比数据、低装饰、专业克制） |

### 设计原则（学术依据）

| 原则 | 出处 | 实操含义 |
|---|---|---|
| **白底黑字，高 data-ink ratio** | Tufte 1990; McGurgan 2021 VISIGRAPP; Hill 2018 JISAR | 纯白底，纯黑字，**无装饰背景/渐变/纹理/边框** |
| **配色 ≤ 3 个颜色** | Graze & Schwabish 2024 JAMIA; Midway 2020 Patterns | 纯黑 + 知乎蓝 + 极少暖橙，其他全灰阶 |
| **白底是科普图解的最优解** | Boy 2020 Frontiers Comm; Schorn 2022 | TED-Ed / Kurzgesagt 风格的白底图解 |
| **关系图用 force-directed 布局** | Zhou 2024 DKGV; Ortega Mattsson 2020 | 节点+边的力导向，节点大小=重要程度 |

**禁用色**：纯红、纯黄、纯绿、纯紫。彩色只能服务于"区分/强调"，不能装饰。

### 6 种插图变体（自动根据章节内容选最合适的 1 种）

| # | 变体 | 适用场景 |
|---|------|---------|
| A | **流程图** | 步骤说明、流程拆解、因果链 |
| B | **柱状图** | 类别对比、排名、规模差异 |
| C | **折线图** | 趋势、随时间变化、增长曲线 |
| D | **知识图谱** | 概念关系、影响因素、节点图 |
| E | **对比表** | 多维度对比、优缺点、推荐 |
| F | **线框图** | 系统架构、UI 流程、组件关系 |

**完整 6 种变体的 prompt 模板**见 `references/style-guide.md` 末节 "知乎文配图风格"。

### 封面 vs 插图差异

- **封面（21:9）**：5 维全开 + typography-dominant data infographic + 大标题 + 1 个核心数据可视化
- **插图（1:1）**：继承 3 维（Palette + Rendering + Mood），无大标题，**根据章节内容自动选最合适的变体**（A-F 中 1 种）
- **风格一致性**：同篇文章所有插图必须是同一种变体风格或同一调色板家族，不允许混搭

### 触发关键词

直接说：`知乎`/`知乎文`/`知乎风格`/`Zhihu`/`白底黑字`/`白底`/`极简`/`专业`/`数据驱动`/`学术风`/`咨询风`/`流程图`/`flowchart`/`统计图`/`柱状图`/`折线图`/`chart`/`信息图`/`infographic`/`线框图`/`wireframe`/`知识图谱`/`技术文`/`科普文`/`分析报告`/`数据可视化` 都会触发本 Workflow。

### 平台部署约定（重要！）

| 平台 | 封面 | 内容图 | 比例 | 数量 | Brand 水印 |
|------|------|-------|------|------|----------|
| **知乎回答 / Zhihu** | ❌ **不要封面**（知乎有自带的问题封面） | ✅ 3 张内容图 | **全部 16:9 横屏**（如 1792x1024）| **恰好 3 张**（再多会拖慢阅读） | ❌ **不要品牌水印**（个人回答）|
| 36kr / 钛媒体 | ✅ 封面 | ✅ per-section | 21:9 封面 / 1:1 内容 | 不限 | ✅ 视情况 |
| 公众号深度文 | ✅ 封面 | ✅ per-section | 21:9 封面 / 1:1 内容 | 不限 | ✅ 视情况 |
| 技术博客教程 | ✅ 封面 | ✅ per-section | 16:9 封面 / 1:1 内容 | 不限 | ✅ 视情况 |

**知乎专用规则**（用户 2026-06 确认，**2026-06-08 修订后端默认走 API**）：
- **不要封面** —— 知乎回答的封面由知乎系统从问题标题自动生成，不需要我们自己出
- **恰好 3 张内容图** —— 知乎排版对超过 3 张图的容忍度低，3 张是最佳实践
- **全部 16:9 横屏（landscape）** —— 知乎移动端 + PC 端展示时横屏图占满栏宽，视觉冲击力最强
- **无品牌水印** —— 个人回答 ≠ 公众号文章，不该带商业水印
- **🆕 后端默认走 API（2026-06-08 修订）** —— 知乎文配图默认走 `scripts/generate.py` + `grsai`/`openai`（config.yaml 默认 provider），中文 prompt + 矢量白底信息图稳定可控。命令：`python scripts/generate.py section --prompt=... --aspect-ratio="1792x1024" --style="zhihu" --article-type="zhihu"`（`--style zhihu --article-type zhihu` 是 API 标志）。仅在用户明确说"用 Dreamina / 即梦 / CLI"时切到 `dreamina text2image --prompt=... --ratio=16:9 --resolution_type=2k --model_version=4.6 --poll=120`，并提示有失败风险

**3 张图的默认锚点（按文章结构）**：
1. **戳破幻觉段**（前 1/4）—— 柱状图，对比"X 年前 vs 现在的履历价值"或"裁员数据"
2. **核心论证段**（中间 1/2）—— 知识图谱 / 公式 viz / 流程图，呈现文章最核心的论证（"议价能力 = ..."）
3. **具体建议段**（后 1/4）—— 流程图 / 对比表，把 3 条建议可视化

**插入位置规范**：在 markdown 中用 `![](images/02-议价能力公式.png)` 紧贴对应段落之后，**不要用 `## ` 标题把段落切碎**（知乎原版没标题）。

### 🔴 中文 prompt 默认规则（用户 2026-06 确认，2026-06-08 修订通用化）

**知乎文章是中文内容，所以配图 prompt 必须是中文**。所有后端（API / Dreamina CLI）对英文 prompt 渲染中文标签都经常失败（出现乱码、拼音替代、或被替换成英文），**所有知乎/公众号/中文场景的 Workflow Z prompt 必须用中文写**。

**中文 prompt 模板**（所有变体通用，6 种变体都按这个改写）：

```
纯白底色（不允许任何纹理/渐变/底纹/底色叠加），专业知乎风格[变体类型：流程图/柱状图/折线图/知识图谱/对比表/线框图]，
黑色文字，蓝色柱子/节点（知乎蓝，深一点的群青蓝），浅灰色辅助元素（方框/连接线/行底），
极少量暖橙色用于高亮强调（≤5% 画面面积）。

[具体场景中文描述，包括节点/列名/数值/标签]。

矢量干净风格，无装饰无边框，1-2px 描边，思源黑体或苹方字体，16:9 横屏。

所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文替代。
颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符。
```

**中文 prompt 的硬性要求**（所有后端通用）：

1. **必含"纯白底色"** —— 多个模型默认会加纹理或渐变，必须在 prompt 显式压回去
2. **必含"黑色文字"** —— 默认是灰色，文字不锐利
3. **必含"思源黑体"或"苹方"字体关键词** —— 默认宋体，需要指定无衬线中文字体
4. **必含"所有中文文字必须清晰锐利可识别，不能渲染成乱码或英文"** —— 长中文容易截断/换字体/拼音替代，必须强约束
5. **节点/列名/数值要写在 prompt 里** —— 不能让模型自己猜
6. **不要写英文 prompt 然后期待模型加中文** —— 必失败
7. **不要在 prompt 写 hex 色值（如 #FFFFFF / #1A1A1A / #056DE8）** —— Dreamina v42 会把 hex 字符串当成可见文字打印在画面上（实测：柱状图柱顶出现 #056DE8 字样）；API 也可能误读 hex 为字面字符串。**改用中文色名**："纯白"/"纯黑"/"知乎蓝"/"浅灰"/"暖橙"，并显式加一句"颜色仅作为风格约束描述，不允许在画面中打印任何颜色名称、颜色代码或 hex 字符"

**英文 prompt 残留的常见症状**（必须避免）：
- ❌ "Knowledge graph" 标签下显示 "Knowledge" 而不是"知识"
- ❌ 中文标签渲染成 "Zhi Shi" 拼音
- ❌ 数字 70% 渲染成 "70%" 但中文描述"成功率"消失
- ❌ 长中文（"工程师角色转变"）被截断成"工程师角色"

**改写检查清单**（生成前必查）：
- [ ] prompt 主体语言是中文
- [ ] 含"纯白底色"和"黑色文字"（用中文色名，**不要写 hex**）
- [ ] 含字体关键词（思源黑体/苹方）
- [ ] 含"中文文字必须清晰锐利可识别"强约束
- [ ] 含"颜色仅作为风格约束描述，不允许打印任何颜色名称/hex 字符"反渲染约束
- [ ] 关键节点/列名用中文明确写出
- [ ] 🆕 **默认走 API（2026-06-08 修订）**：`python scripts/generate.py section --prompt=... --aspect-ratio="1792x1024" --style="zhihu" --article-type="zhihu"`
- [ ] 仅在用户明确要 Dreamina / 即梦 / CLI 时才用 `dreamina text2image --prompt=... --ratio=16:9 --resolution_type=2k --model_version=4.6 --poll=120`

### 与"测评信息图" (Workflow L) 的关键区别

| 维度 | 测评信息图 (L) | 知乎文配图 (本 Workflow Z) |
|---|---|---|
| 背景 | 浅色 (浅灰/浅米) | **纯白** |
| 主色 | 多色（蓝/橙/绿/红） | **单色强调 (蓝)** |
| 装饰 | 允许小图标点缀 | **完全无装饰** |
| 气质 | "测评报告 + 评分卡" | "学术图解 / 知乎高赞回答" |
| 适用 | 产品横评、工具对比 | 数据论证、概念解释、流程拆解 |

---

## Workflow X: 小黑科普（Ian 怪诞手绘 + 小黑 IP）

适合**科技公众号深度文、知乎技术文/科普文、AI 概念解释、机制/原理/对比类文章**——只要文章里有 1-3 个"核心判断/认知锚点/结构/状态/隐喻"需要被解释清楚，就适合这套。

整体气质：**「让一个黑色小怪物在白纸上认真做一件怪事，把抽象概念翻译成一个奇怪但成立的画面」**——纯白手绘、小黑 IP、少量红/橙/蓝批注、极简、留白、怪诞但可读。

> ⚡ **执行规则（覆盖全局 Step 3 的"后端选择"）**
> **小黑科普默认走 API 出图**（`scripts/generate.py`，provider 走 config.yaml），**不走 Dreamina CLI**。
> 原因：小黑科普依赖 IP 形象一致性 + 中文手写批注 + 怪诞隐喻，对模型可控性要求高；Dreamina CLI 在 2026-06 实测中曾 3 次出现"final generation failed"（见本次会话日志），不可靠。
> 仅在用户**明确说"用 Dreamina / 即梦 / CLI"**时才切到 Dreamina CLI，并提示用户有失败风险。
> API prompt 模板见 `references/style-guide.md` 末节"小黑科普风格"。

### 触发关键词

直接说：`小黑`/`小黑科普`/`Ian`/`怪诞手绘`/`小黑插图`/`小黑配图`/`Ian 风格`/`小黑图` 都能触发本 Workflow。

### 风格 vs Workflow Z 的关键区别（用户经常要选）

| 维度 | 知乎文配图 (Workflow Z) | 小黑科普 (本 Workflow X) |
|---|---|---|
| 气质 | 学术图解 / 咨询报告 / Tufte 风 | 怪诞手绘 / 产品草图 / 冷幽默 |
| 主体 | 数据 + 节点 + 边 | **小黑 IP**（黑色实心、白点眼、细腿、空表情） |
| 背景 | 纯白、矢量、锐利 1-2px | 纯白、**手绘抖动线**、有手感 |
| 颜色 | 蓝 + 极少量橙，单色强调 | **红/橙/蓝三色少量批注**（不混搭）|
| 装饰 | 完全无装饰 | 少量手写中文批注（5-8 处）|
| 适用 | 数据论证、统计图、流程图、对比表 | 概念隐喻、状态对比、机制解释、判断收束 |
| 后端 | Dreamina CLI 4.6 | **API（grsai/openai/local）** |
| 失败率 | 较低 | API 较低；Dreamina CLI 较高（2026-06 实测 3/3 失败）|

**当用户触发条件同时命中两个 Workflow 时**（如 `技术文`/`科普文`/`分析报告`/`知乎` + 包含"对比/机制/隐喻"等关键词），**必须先用 AskUserQuestion 询问选哪个 Workflow**：
- 选项 A：Workflow Z（白底黑字信息图，学术风）
- 选项 B：Workflow X（小黑科普，怪诞手绘风）
- 默认推荐按"内容性质"判断：
  - 数字、统计、流程、对比表 → 倾向 Z
  - 概念、机制、判断、隐喻、收束 → 倾向 X

### 5 维默认

| 维度 | 默认值 |
|---|---|
| 比例 | **16:9 横屏**（知乎/公众号正文同款）|
| 数量 | **3-4 张**（文章短 1-3 张；长文不要超 8 张，够用就好）|
| 后端 | **API**（config.yaml 里的 default provider）|
| 主体 | **小黑 IP**（每张必出现，承担核心动作）|
| 留白 | 主体占画面 40-60%，至少 35% 空白 |

### 工作流（必走 5 步）

1. **消化正文** — 读文章，提炼核心观点、认知转折点、可图解段落
2. **出 shot list** — 写 1-3 段话说明每张图的位置、主题、隐喻、小黑动作（先给用户看，不直接生图）
3. **逐张生图** — 调 `python scripts/generate.py section --prompt=...`（API），**每张单独生成**，不复用旧案例构图
4. **QA 检查** — 5 项硬约束：①白底 ②小黑承担动作 ③全新隐喻（不复刻传送带/漏斗/切鱼/拉线/盖章/拉三层） ④不留左上角标题 ⑤无 PPT/课程课件感
5. **保存 + 插入** — `images/NN-topic-name.png` 命名，紧跟对应段落后用 `![](images/NN-...)` 插入

### 调用 `/ian-xiaohei-illustrations` 的方式

本 Workflow 是**轻委托**——生图相关的细节（风格 DNA、IP 形象、构图模式、QA 清单、提示词模板）全部来自 `~/.claude/skills/ian-xiaohei-illustrations/`。本 Workflow 只决定：

- **何时**触发（科技/科普/知乎/技术文场景）
- **选哪个 Workflow**（用 AskUserQuestion 问用户）
- **插入到文章的哪里**（用 `![](images/...)` 语法）
- **多少张**（默认 3-4 张，按文章长度）
- **后端选 API**（强制）

具体的"小黑动作 / 隐喻 / 标注词 / 颜色"全部由 `ian-xiaohei-illustrations` 自己决定。

**执行伪代码**：

```text
if user triggers 知乎/科技/科普/技术文/分析报告:
    ask_user = AskUserQuestion(
        question="要哪种风格？",
        options=[
            {label: "📐 知乎文配图 (Workflow Z)", description: "白底黑字学术风, API 出图 (🆕 2026-06-08 修订后端默认), 流程图/统计图/知识图谱"},
            {label: "🐾 小黑科普 (Workflow X)", description: "Ian 怪诞手绘, API 出图, 小黑 IP + 全新原创隐喻"},
        ]
    )
    if ask_user == "Z": run Workflow Z
    if ask_user == "X": delegate to /ian-xiaohei-illustrations
```

---

## Workflow O: 水彩淡墨 / 清新淡雅风格（独处/夜听/卧室场景专用）

适合**清新淡雅水彩插画风**——不是厚涂油画、不是胶片照片、不是 Excalidraw 手绘。笔触是**淡彩水洗**（light watercolor wash, soft ink wash texture, 留白多），**极简、留白、轻盈**。低饱和柔色，主角是数字绘画中的人物（不露脸）+ 卧室/书桌/窗户/城市夜景。

### 📦 生图数量硬约束（2026-06 用户确认）

**每期日听 / 夜听文章固定生成 4 张图**（不再多也不再少，按这个数量跑）：

| # | 类型 | 比例 | 用途 | 是否插入文章 |
|---|------|------|------|------|
| 1 | **1:1 插图** | 1:1 (1024×1024) | 文章内文配图 — 选文中 3 个关键画面 | ✅ **插入文章** |
| 2 | **1:1 插图** | 1:1 (1024×1024) | 文章内文配图 | ✅ **插入文章** |
| 3 | **1:1 插图** | 1:1 (1024×1024) | 文章内文配图 | ✅ **插入文章** |
| 4 | **21:9 banner** | 21:9 (1920×832) | 公众号 / 网页 banner | ❌ **不插入**（仅保存到 images/） |
| 5 | **1:1 播客封面** | 1:1 (1024×1024) | 喜马拉雅 / Apple Podcasts 单期封面 | ❌ **不插入**（仅保存到 images/） |

**执行规则**：

- **3 张 1:1 插图**——按 Workflow O 的"1:1 场景插图模板"批量出，每张选文章里一个关键画面（早期 / 中段 / 收尾），**全部插入文章正文中**（参考插入位置由 sub-agent 按内容节奏决定）
- **1 张 21:9 banner**——按 Workflow O 的"封面 Banner 模板"出，比例硬约束 21:9（参考下方 ⚠️ 比例硬约束段），**不插入文章**，仅保存到 `images/0x-{日听/夜听}-banner.png`
- **1 张 1:1 播客封面**——按 Workflow P 的"单期封面 prompt 模板"出，**不插入文章**，仅保存到 `images/0x-{日听/夜听}-播客.png`
- **3 张插图插入位置**：用 `![](images/01-xxx.png)` 紧跟对应段落后，**不拆原文的 `##` 标题**（日听/夜听通常无章节标题，按画面节奏自然插入）
- **后端默认走 API（GPT-Image-2 / grsai）**——日听/夜听是**风格化强 + 中文文字密集**的场景（暖光卧室+抱膝人物+水彩淡墨+中文长段诗），GPT-Image-2 在写实/插画风 + 文字渲染上比即梦更稳。仅在用户明确说"用 Dreamina/即梦/CLI"时才切到 Dreamina CLI

**输出文件命名**（建议规范，可改）：

```
images/
├── 01-{日听/夜听}-插图-{画面1}.png        # 1:1 插图，插入文章
├── 02-{日听/夜听}-插图-{画面2}.png        # 1:1 插图，插入文章
├── 03-{日听/夜听}-插图-{画面3}.png        # 1:1 插图，插入文章
├── 04-{日听/夜听}-banner.png              # 21:9 banner，**不插入**
└── 05-{日听/夜听}-播客.png                # 1:1 播客封面，**不插入**
```

### ⚠️ "图+长诗"组合硬约束（2026-06 验证）

**日听/夜听的核心需求 = "水彩淡墨画面 + 中文长段诗(10+ 行)同图渲染"。这个组合有明确的硬约束**：

| 后端 | 是否支持"图+长诗同图" | 证据 |
|---|---|---|
| **API (GPT-Image-2 / grsai)** | ✅ **支持** | 实测 14 行中文长诗完整清晰渲染（见 `yeting-01.png`）|
| **Dreamina CLI (v42 / v50)** | ❌ **不支持** | 100% 触发 `api error: ret=1046, message=InvalidNode`（即梦 parser 拒收中文长段诗）|

**Sub-agent 执行规则**：

- 当用户需求是"图+中文长诗同图"时，**必须用 API (GPT-Image-2)**，**不能切到 Dreamina CLI** — 这不是风格偏好问题，是**技术硬约束**
- 当用户**明确**说"用 Dreamina/即梦/CLI 跑日听/夜听"时，正确做法是 **fallback 方案**：
  1. 用 CLI 跑**无诗**的水彩淡墨画面（`yeting-01-cli-nopoem.png` 风格）
  2. 诗**后期手工加**到画面上（用 Figma/Canva/PS 等加字）
  3. 在文件命名上区分：`xxx-cli-nopoem.png` vs `xxx-api-with-poem.png`
- CLI 的优势场景是**无文字密集**的画面（白底信息图、流程图、马克笔 Q 版、8-bit 像素、白底 Excalidraw），**不是"诗配图"**

**踩坑记录**（避免重复踩）：
- CLI 短 prompt（"a cat portrait"）→ ✅ 正常
- CLI 简化版夜听 prompt（诗短 + 描述少）→ ✅ 正常（但**只适配 CLI 自己的画风，跟 API 风格不一致，没法对比**）
- CLI 完整夜听 prompt（诗 14 行 + 画面 + 反向词）→ ❌ InvalidNode
- 删 3 个反向词重试 → ❌ 还是 InvalidNode
- 删全部诗重试 → ✅ 正常
- 结论：**触发 `InvalidNode` 的就是 prompt 里的中文长段诗**（不是反向词数量、不是总长度，是 parser 对"长段诗"格式敏感）

### 5 维默认

| 维度          | 默认值                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Type**      | `illustration` 数字插画（水彩淡墨感）                                                                                |
| **Palette**   | 柔色低饱和：cream #FAF4E8 / soft peach #F0DCC4 / pale gold #E8C9A0 / dusty blue #B5C5D3 / misty lavender #D5C9DC |
| **Rendering** | **数字水彩 + 淡彩笔触 + 留白多**（light watercolor wash, sparse brush, ample negative space, NOT thick impasto / NOT heavy painterly）|
| **Font**      | 细笔手写 + 衬线（封面标题用细手写/serif，留白环境清晰可读）                                                       |
| **Mood**      | subtle，极低对比，清淡中带安静                                                                                     |

### 必含正向关键词（每张图都要有，中英混用 prompt）

中文：
- 清新淡雅的水彩风格
- 淡彩水洗笔触，留白多
- 低饱和柔色，奶油、淡桃、雾蓝、淡紫
- 安静、克制、独处、陪伴

English (技术约束)：
```
Light watercolor wash illustration, sparse delicate brush strokes,
ample negative space, soft muted palette (cream, soft peach, pale gold,
dusty blue, misty lavender), low saturation, low contrast,
contemplative solitary mood, gentle color bleeds
```

### 必含反向关键词（**关键！这是避免跑偏的核心**）

中文：
- ❌ 不是厚涂油画
- ❌ 不是高饱和
- ❌ 不是浓墨重彩
- ❌ 不是写实摄影
- ❌ 不是 3D 渲染
- ❌ 不是二次元/卡通

English (反向)：
```
NOT thick impasto, NOT heavy painterly, NOT oil paint texture,
NOT photograph, NOT photorealistic, NOT anime, NOT 3D rendering,
NOT line art, NOT dark/moody, NOT high contrast, NOT high saturation
```

### 典型画面元素（独处/夜听/卧室场景）

- **人物**：年轻女性独处（不露脸），抱膝、看手机、坐窗边、看书
- **服装**：宽松的白衬衫/米色/淡粉睡袍
- **场景**：卧室（床、枕头、毯子）+ 床头小台灯（暖光）+ 窗外深蓝城市夜景
- **物件**：手机（屏幕冷光）、咖啡杯、书、便签、墙上的照片
- **氛围**：暖色台灯 + 窗外冷光 = 暖冷对比，安静独处

### 封面 Banner 模板（21:9）

```
[场景描述...]

# ⚠️ 比例硬约束：必须 21:9 (1920x832 / 3024x1296)
# NOT 1:1, NOT 3:4, NOT 4:3, NOT 9:16, NOT 1.5:1
# API 调用必须显式指定 --ratio "21:9" 或 --aspect-ratio "1920x832"
# 生成后用 PIL.Image 校验 width/height 在 [2.2, 2.45] 区间内

# Font Application (CRITICAL — 来自 baoyu-cover-image)
Use warm hand-lettered typography with organic brush strokes. Friendly,
personal feel. The title MUST be in artistic hand-drawn style with slightly
wobbly, organic strokes — NOT plain sans-serif, NOT Song-style typeface,
NOT uniform printed type. Each character must feel hand-painted with
visible brush variation (thick-thin contrast, slight ink bleed,
occasional dry-brush edges). The text style must harmonize with the
gouache/painterly rendering of the scene.

Include the following Chinese text rendered clearly with sharp legible
characters, no garbled strokes, no missing characters:
- Large title at center-bottom: '【夜听】[标题]' (handwritten brush
  calligraphy, dark warm brown, 30-40% of image height)
- Small subtitle at bottom right: '——木棉书笺 记' (smaller handwritten
  brush style, subtle dark warm brown)
```

### ⚠️ 21:9 比例硬约束（2026-06-06 起，所有 banner 通用）

**日听/夜听 banner 同样必须 21:9**。`novel/2606/0606/【日听】xxx-banner.png` 当初出成 1536x1024 (1.5:1) 是不合格的。

生成后**必须**做比例校验（参考 Workflow A 末节的比例校验脚本）。如果后端只支持 1:1 / 9:16，先尝试显式传 `--ratio "21:9"` / `--aspect-ratio "1920x832"`，**不要默认接受任何非 21:9 的比例**。

### 字体选择（baoyu 标准 4 种）

| 风格       | 英文 keyword  | 描述                                                                                 | 适合                          |
| ---------- | ------------- | ------------------------------------------------------------------------------------ | ----------------------------- |
| 手写毛笔   | `handwritten` | warm hand-lettered with organic brush strokes, thick-thin contrast, slight ink bleed | 夜听 / 情感治愈 / 美食 / 萌宠 |
| 衬线经典   | `serif`       | elegant serif with refined letterforms, classic editorial character                  | 怀旧 / 时尚 / 家居            |
| 极简无衬线 | `clean`       | clean geometric sans-serif, modern minimal letterforms                               | 科技 / 测评 / 都市            |
| 装饰粗体   | `display`     | bold decorative display, heavy expressive headlines                                  | ACG / 运动 / 招牌             |

⚠️ **关键警告**：不在 prompt 里加 `Font:` / `Font Application` 段，grsai 会渲染成默认宋体。必须用 baoyu 的 `Use ... typography with ...` 句式写**具体视觉特征**（hand-drawn、wobbly、brush variation、ink bleed），模型才会按设计意图出字。

### 字体模板（每个绘画风格都必加）

每个 Workflow 的封面/插图 prompt 模板，**必须**包含下面这段（或选对应 font）：

```
# Font Application (CRITICAL)
- handwritten: Use warm hand-lettered typography with organic brush
  strokes. Friendly, personal feel. Title MUST be in artistic hand-drawn
  style with slightly wobbly, organic strokes — NOT plain sans-serif,
  NOT Song-style typeface.
- serif: Use elegant serif typography with refined letterforms.
  Classic, editorial character.
- clean: Use clean geometric sans-serif typography. Modern, minimal
  letterforms.
- display: Use bold decorative display typography. Heavy, expressive
  headlines.
```

### 1:1 场景插图模板（芒种系列实战 prompt）

```
[中文主体描述]：清新淡雅的水彩插画风格，淡彩水洗笔触，留白多，极简。
低饱和柔色调：奶油色 #FAF4E8、淡桃 #F0DCC4、淡金 #E8C9A0、雾蓝 #B5C5D3、淡紫 #D5C9DC。
安静、克制、独处、陪伴的氛围。
数字水彩感、留白轻盈、淡彩水洗笔触。

[具体场景中文描述，例如]
"清晨卧室场景：床上躺着的女性背影（不露脸），窗帘透进第一缕光，
床头放着复古闹钟（5:55），床头柜上一杯咖啡冒着热气，
窗外有麦穗剪影，淡彩水洗笔触，极简留白。"

Light watercolor wash illustration, sparse delicate brush strokes,
ample negative space, soft muted palette, low saturation, low contrast,
contemplative solitary mood, gentle color bleeds.

Chinese text '【日听】芒种——先给自己五分钟' must be sharp legible,
rendered in delicate brush calligraphy, light brown or dark warm color.
Brand text '木棉书笺' in small, light warm color at bottom right.

NOT thick impasto, NOT heavy painterly, NOT oil paint texture,
NOT photograph, NOT photorealistic, NOT anime, NOT 3D rendering,
NOT line art, NOT dark/moody, NOT high contrast, NOT high saturation.

1:1 square format.
```

### ⚠️ 即梦中文渲染注意

即梦对通讯录里的"Chinese name"理解弱，可能渲染成 Mom/Dad/Lila/Tom 等英文。如需中文，**必须在 prompt 里直接写**具体要渲染的字（如 "render the Chinese characters 老王 clearly"），并加 `Chinese text '老王' must be sharp legible` 强约束。

### 参考图（芒种系列是这个风格的成功案例）

- `novel/2606/0605/images/日听-芒种-先给自己五分钟-banner.png`（21:9 日听 banner，水彩淡墨 + 中文标题清晰 + 麦穗+晨光+咖啡+钟）
- `novel/2606/0605/images/夜听-芒种-别忘了你在等什么-banner.png`（21:9 夜听 banner，水彩淡墨 + 月光+暖灯+书桌+窗外麦田+窗棂）
- `novel/2606/0605/images/日听-芒种-先给自己五分钟-喜马拉雅.png`（1:1 喜马拉雅 banner）
- `novel/2606/0605/images/夜听-芒种-别忘了你在等什么-喜马拉雅.png`（1:1 喜马拉雅 banner）

### 触发关键词

- 独处型夜听 / 日听朝露
- 深夜翻手机 / 晨光
- 水彩淡墨 / 清新淡雅
- 淡彩水洗 / 留白极简
- 卧室场景插画
- 情感治愈 / 电台散文诗

---

## Workflow P: 1:1 音频封面（喜马拉雅/播客/单集/专辑）

适合音频内容（播客、电台、专辑、单集）的**1:1 方形封面图**。常见用途：

- 喜马拉雅专辑封面（1000x1000）
- 喜马拉雅单集封面
- Apple Podcasts 专辑封面（1:1，最大 3000x3000）
- 小宇宙、网易云音乐等播客平台
- 公众号音频栏目头图

**与 Workflow O（水彩淡墨 / 清新淡雅）的关系：**

- 风格一致（**水彩淡墨 / 淡彩水洗 / 留白极简** / 低饱和柔色）
- **区别是比例 1:1**（不是 21:9 banner）
- **包含品牌文字 + 大字标题**（Ximalaya 等平台要求标题清晰可见）
- 适用于日听朝露 / 夜听寄语 等中文电台散文诗类型

> 芒种系列（2026/06/05 出图）是这个风格的成功标准实现，参考图详见 Workflow O 参考图章节。

### 5 维默认

| 维度          | 默认值                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Type**      | `cover-square` 1:1 方形封面                                                                                          |
| **Palette**   | 柔色低饱和：cream #FAF4E8 / soft peach #F0DCC4 / pale gold #E8C9A0 / dusty blue #B5C5D3 / misty lavender #D5C9DC    |
| **Rendering** | **数字水彩 + 淡彩笔触 + 留白多**（light watercolor wash, sparse brush, ample negative space）                                                                                          |
| **Font**      | `handwritten`（细笔手写 / 留白环境清晰可读）                                                                                                                                          |
| **Mood**      | `subtle`（极低对比，清淡安静）                                                                                                                                                       |

### 触发关键词

- 1:1 封面 / 1:1 生图 / square cover
- 喜马拉雅封面 / 喜马拉雅专辑图
- 播客封面 / podcast cover
- 单集封面 / 专辑封面
- 方形封面 / 1:1 banner

### 两种用途的文字差异

| 用途         | 文字层级                                                | 视觉重心                |
| ------------ | ------------------------------------------------------- | ----------------------- |
| **单期封面** | 标题大字（25-30% 画面高度）+ 品牌（小）                 | 标题占视觉中心          |
| **专辑封面** | 专辑名大字（30-35% 画面高度）+ 副标题（中）+ 品牌（小） | 专辑名 + 一句副标题     |

### 单期封面 prompt 模板

**日听（晨间）单期：**

```
Square 1:1 digital painting cover for Chinese morning radio podcast.
Hand-painted style with thick visible oil paint brush strokes,
dry brush texture. NOT watercolor, NOT photograph, NOT anime,
NOT 3D rendering, NOT line art.

Visual scene: [本期主题画面]. [具体元素 / 光线 / 物件 / 人物动作].

Chinese text to render clearly with sharp legible characters,
no garbling, no missing characters:
- Large title (centered, mid-image): '【日听】[本期标题]'
  (handwritten brush calligraphy style, dark warm brown #5C3A21,
  25-30% of image height)
- Small brand at bottom right: '木棉书笺 · 日听朝露'
  (smaller handwritten brush style)

Color palette: cream #F5E0C8, peach pink #F2C6B5, muted gold #E8B57A,
dusty blue #8B9DC3. Low saturation, warm tones with cool accents.
Square 1:1 format. Contemplative morning mood.
```

**夜听（深夜）单期：**

```
Square 1:1 digital painting cover for Chinese late-night radio podcast.
Hand-painted style with thick visible oil paint brush strokes,
dry brush texture. NOT watercolor, NOT photograph, NOT anime,
NOT 3D rendering, NOT line art.

Visual scene: [本期主题画面]. [具体元素 / 光线 / 物件 / 深夜氛围].

Chinese text to render clearly with sharp legible characters,
no garbling, no missing characters:
- Large title (centered, mid-image): '【夜听】[本期标题]'
  (handwritten brush calligraphy style, dark warm brown #5C3A21,
  25-30% of image height)
- Small brand at bottom right: '木棉书笺 · 夜听寄语'
  (smaller handwritten brush style)

Color palette: cream #F5E0C8, peach pink #F2C6B5, muted gold #E8B57A,
deep navy #1E3A5F, lavender shadow #C9B8D4. Low saturation,
warm-cool contrast. Square 1:1 format.
Quiet, intimate, late-night mood.
```

### 专辑封面 prompt 模板

**日听朝露 专辑（早晨方向感）：**

```
Square 1:1 digital painting cover for Chinese morning radio podcast
album 'Morning Dew'. Hand-painted style with thick visible oil paint
brush strokes, dry brush texture. NOT watercolor, NOT photograph,
NOT anime, NOT 3D rendering, NOT line art.

Visual scene: A window sill at dawn. A small glass cup with morning
dew drops on it, catching the first sunlight. A small white magnolia
flower or a single branch with fresh leaves beside. The first light
of dawn - golden hour, with dewdrops on green leaves just visible at
the edges. Soft and fresh. A cup of warm drink with soft steam rising.

Chinese text to render clearly with sharp legible characters,
no garbling, no missing characters:
- Large album title (centered, mid-image): '日听朝露'
  (handwritten brush calligraphy style, dark warm brown #5C3A21,
  30-35% of image height)
- Subtitle below title: '每天清晨 给你一个行动的方向'
  (smaller handwritten brush style)
- Small brand at bottom right: '木棉书笺' (smaller handwritten)

Color palette: cream #F5E0C8, peach pink #F2C6B5, muted gold #E8B57A,
fresh mint #B5E5CF, soft sky #A8D8EA. Low saturation, fresh and bright.
Square 1:1 format. Fresh morning album cover mood.
```

**夜听寄语 专辑（深夜陪伴感）：**

```
Square 1:1 digital painting cover for Chinese late-night radio podcast
album 'Night Whispers'. Hand-painted style with thick visible oil
paint brush strokes, dry brush texture. NOT watercolor, NOT photograph,
NOT anime, NOT 3D rendering, NOT line art.

Visual scene: A cozy late-night room corner. A warm lamp with amber
glow on a wooden nightstand, the lamp is the only light source.
Through a half-open window, the moon and a few stars in deep blue
night sky. A ceramic cup of warm drink with gentle steam rising.
A small stack of old books beside the lamp. The whole scene wrapped
in soft darkness, with the lamp creating a small pool of warm light.

Chinese text to render clearly with sharp legible characters,
no garbling, no missing characters:
- Large album title (centered, mid-image): '夜听寄语'
  (handwritten brush calligraphy style, dark warm brown #5C3A21,
  30-35% of image height)
- Subtitle below title: '每个深夜 给你一点温柔的允许'
  (smaller handwritten brush style)
- Small brand at bottom right: '木棉书笺' (smaller handwritten)

Color palette: cream #F5E0C8, peach pink #F2C6B5, muted gold #E8B57A,
deep navy #1E3A5F, lavender shadow #C9B8D4. Low saturation,
warm-cool contrast. Square 1:1 format.
Quiet, intimate, contemplative album mood.
```

### 命令调用

用 `generate.py section` 模式 + `--aspect-ratio 1024x1024`：

```bash
python scripts/generate.py section \
  --prompt "<上面模板填充后>" \
  --output "images/01-日听-单期-[标题].png" \
  --aspect-ratio "1024x1024" \
  --style "painterly" \
  --article-type "riting"
```

**article-type 路由（自动选品牌）：**

- `riting` → 木棉书笺（mumian）品牌
- `yeting` → 木棉书笺（mumian）品牌

**文件命名规范：**

```
images/
├── 01-{riting/yeting}-单期-{标题}.png   # 单期封面
├── 02-{riting/yeting}-单期-{标题}.png
├── 03-{riting/yeting}-专辑-{专辑名}.png  # 专辑封面
└── 04-{riting/yeting}-专辑-{专辑名}.png
```

### 与 21:9 banner 的关系

Ximalaya 专辑封面**必须 1:1**，不能用 21:9 banner（21:9 是公众号封面比例）。但同一系列可以出两版：

- **1:1 专辑封面**（Ximalaya / Apple Podcasts）→ 用本 Workflow P
- **21:9 banner**（公众号 / 网页）→ 用 Workflow A 或 O

保持色板和渲染风格一致即可。

### 失败重试

如果中文标题渲染乱码：

1. 强化 `Chinese text to render clearly with sharp legible characters, no garbling`
2. 标题字符过长时拆成两行（用 `\\n`）
3. 重试 1 次，仍然失败则跳过该图并标记 `❌`

### 参考图

- `novel/2606/0605/images/01-日听-单期-困住你的不是时间.png`（本期生成）
- `novel/2606/0605/images/02-夜听-单期-今天这样就够了.png`（本期生成）
- `novel/2606/0605/images/03-日听朝露-专辑封面.png`（本期生成）
- `novel/2606/0605/images/04-夜听寄语-专辑封面.png`（本期生成）

---

## Brand Watermark Rules

Brand info only appears on covers of "professional" styles:

- ✅ Tech, Blueprint, Cyberpunk, Corporate, Pixel Art, Travel/City, Home/Lifestyle, Fashion/Beauty, ACG/Anime, Review/Infographic, Sports/Fitness
- ❌ Emotional, Nostalgic Photo, Sketch Notes, Vintage, Kawaii, Watercolor, Screen Print, Zen Minimal, Food, Pet/Q-version, Digital Illustration / Painterly

When `brand.enabled` is false, no watermark on any style.

## API Provider Differences

| Feature               | `grsai`                              | `openai` / `openai-compatible` / `local` |
| --------------------- | ------------------------------------ | ---------------------------------------- |
| Cover endpoint        | `/v1/images/generations`             | `/v1/images/generations`                 |
| Illustration endpoint | `/v1/draw/completions` (SSE)         | `/v1/images/generations`                 |
| Illustration request  | `aspectRatio` + `replyType: "async"` | `size: "1024x1024"`                      |
| Illustration response | SSE stream                           | Standard JSON                            |

## Edge Cases

- No `##` headings → Workflow E (怀旧照片): generate cover + 2-3 scene illustrations; other workflows: generate only cover
- No `#` heading → use filename as title
- API returns `violation` → rephrase and retry
- API returns `failed` → retry once, then report error and continue
- API returns `excessive system load` (grsai) → wait 30s and retry, or switch to Dreamina CLI
- Dreamina CLI not found → tell user to install dreamina CLI and run `dreamina login`
- Dreamina generation failed → retry once with adjusted prompt, then skip and continue
- User only wants cover → skip section images and insertion
- Jimeng text garbled → retry with adjusted font description (see `references/quick-styles.md`)
- Article too long (>80 sentences) → warn user about credit consumption, confirm before proceeding
