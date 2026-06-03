---
name: luoboa-illustrate
description: Generate illustrations for WeChat public account articles (公众号配图) using image generation APIs or Dreamina CLI, then insert them into the article markdown file. Use this skill whenever the user wants to create illustrations, images, or cover art for their articles, or mentions 配图/插图/封面/快文配图/快文/视频素材 for articles. Also trigger when the user asks to "给文章配图", "生成插图", "做封面", "快文配图", "按句配图".
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
3. **Brand (optional)** — Ask: "Want to add brand watermark?" If yes, collect: name, tagline, logo URL, website
4. Save to `config.yaml`

### Config schema

```yaml
backend: api              # api (default) / dreamina

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

dreamina:
  enabled: true
  cli_path: ""            # auto-detected from PATH if empty
  ratio_cover: "21:9"
  ratio_section: "1:1"
  resolution: "2k"
  poll_timeout: 60
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
| 1 | 🖥️ 科技风 | 暗色手绘图解 + Excalidraw手绘草稿 |
| 2 | 💕 柔情风 | 温暖治愈莫兰迪 + 人物一致性 |
| 3 | 📷 怀旧照片风 | 90年代写实胶片质感 + 夕阳光/暖黄灯光 + 温暖泛黄 |
| 4 | 🍜 美食风 | 暖光食物特写 + 蒸汽/拉丝/俯拍构图 |
| 5 | 🗺️ 旅行城市风 | 现代写实风景 + 城市夜景/航拍/季节感 |
| 6 | 🐾 萌宠Q版风 | 拟人/治愈/Q版宠物插画 |
| 7 | 🏠 家居生活风 | 样板间/MUJI/北欧/户型图 |
| 8 | 💄 时尚美妆风 | 产品摄影 + 人物一致性 + 妆容/服装特写 |
| 9 | 🎮 ACG二次元风 | 日式赛璐璐/原神风/Q版角色 |
| 10 | 📊 测评信息图 | 结构化信息图 + 评分卡 + 对比图 |
| 11 | 🏃 运动健身风 | 动态/汗水/球场跑道 |
| 12 | 🎨 更多风格... | 查看额外扩展风格（Blueprint/Cyberpunk/Pixel Art/Sketch Notes/Vintage/Kawaii/Watercolor/Screen Print/Zen Minimal） |
| 13 | ⚡ 快文配图 | 按句生成9:16竖图，即梦渲染文字，视频素材 |
| 14 | 📰 头条配图 | 每条新闻生成9:16钢笔速写图，纪实风新闻合集 |

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
If user picks 12 → show extended catalog from `references/style-guide.md`
If user picks 13 → Workflow D (快文配图)
If user picks 14 → Workflow N (头条配图)

Also trigger Workflow D directly when user says "快文配图"/"快文"/"视频素材"/"按句配图".
Also trigger Workflow D when user mentions "横屏"/"竖屏"/"16:9"/"9:16"/"封面"/"banner" etc. — these are common video/post requirements that aren't always vertical.
Also trigger Workflow E directly when user says "怀旧照片"/"怀旧风"/"老照片"/"90年代照片"/"胶片风".
Also trigger Workflow N directly when user says "头条配图"/"新闻配图"/"资讯配图"/"AI快讯配图".

### Step 3: Generate Images

**API 优先（出图质量更好），Dreamina CLI 作为备选。** 根据 `config.yaml` 中 `backend` 字段决定。当 API 返回过载或连续错误时，自动降级到 Dreamina CLI。

#### 方案一：API（默认，推荐）

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

| 维度 | 封面 | 插图 | 说明 |
|------|------|------|------|
| Type（构图类型） | ✅ | ❌ | 插图无大字排版 |
| **Palette（色板）** | ✅ | ✅ **必须继承** | 同一套hex色值 |
| **Rendering（渲染方式）** | ✅ | ✅ **必须继承** | painterly就全painterly，digital就全digital，film grain就全film grain |
| Font（字体） | ✅ | ❌ | 插图无文字 |
| **Mood（情绪对比度）** | ✅ | ✅ **必须继承** | subtle就全subtle，bold就全bold |

**执行方式：** 生成封面后，将封面prompt中的 Palette/Rendering/Mood 三个维度参数原样写入每张插图的prompt。不允许封面painterly+插图photography，或封面duotone+插图全彩。

**具体例子：**
- 封面选了 A 日系电影感（painterly/warm/subtle）→ 插图prompt必须包含 "soft watercolor wash textures, visible brush strokes" + "cream #FFFAF0, golden yellow #F6AD55" + "low contrast, muted desaturated"
- 封面选了 G 王家卫式（digital/duotone/bold）→ 插图prompt必须包含 "clean precise edges, frosted glass effects" + "crimson #DC143C and navy #0D1B2A" + "high contrast, vivid saturated"
- 封面选了 H 拍立得底栏（hand-drawn/warm/subtle）→ 插图prompt必须包含 "sketchy organic strokes, variable marker line weight" + "cream #FFFAF0, golden yellow #F6AD55" + "low contrast, muted warm tones"

**同样适用于 Workflow F-M（美食/旅行/萌宠/家居/时尚/ACG/测评/运动）**：每种风格的 5 维默认参数已在各自 Workflow 章节明确定义，插图 prompt 必须以 `"Consistent with cover: [palette], [rendering], [mood]"` 开头。涉及真人/角色的风格（Workflow H/J/K）从第 2 张插图起必须传 `--ref-url` 保持一致性。

---

## Workflow A: 科技类

- Cover: dark-background hand-drawn diagram style (Excalidraw dark mode) with brand logo (if enabled). Prompt template in `references/style-guide.md`.
- Sections: Excalidraw hand-drawn sketch style. Prompt template in `references/style-guide.md`.
- **风格一致性**：封面和插图同属Excalidraw手绘风格，天然一致。

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
2. **英文 Prompt** — grsai 等国内 API 中文 prompt 易触发内容审核，统一使用英文
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
- 12种风格：A日系电影感 / B复古杂志风 / C自然呼吸感 / D信笺与手写 / E光影重叠 / F极简新中式 / G王家卫式 / H拍立得底栏 / I唱片封面风 / J旧报纸头条 / K诗歌散排 / L古书扉页
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

| 情绪 | 色调关键词 | 色相范围 |
|------|-----------|---------|
| 温暖/回忆/日常 | `warm golden tones, Kodak Gold film, soft amber glow, faded yellowish edges, gentle vignette, dust motes in sunbeam` | 蜂蜜金 #F6AD55 / 奶油 #FFFAF0 / 暖米 #F5E6D3 |
| 失去/空荡（仍暖） | `low saturation warm beige, faded honey tones, soft golden haze, very gentle vignette, no cold colors, warm light still present` | 沙米 #E8DCC4 / 暖灰 #C9B89C / 淡金 #D4A574 |
| 克制/隐忍 | `soft warm diffused light, muted amber, no harsh shadows, quiet warm tones, golden hour lingering` | 暖白 #FFF4E6 / 浅金 #FFE5B4 / 米色 #F5DEB3 |
| 夜晚室内（仍暖） | `warm tungsten lamp light, amber interior glow, cream walls, cozy living room, NO cold blue night` | 钨丝灯 #FFB347 / 暖琥珀 #DAA520 / 深米 #DEB887 |

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

| 维度 | 控制 | Banner 必选 | 插图继承 |
|------|------|-----------|---------|
| **Type** | 构图类型（hero/typography/scene/...） | ✅ | ❌ |
| **Palette** | 色板（hex 值） | ✅ | ✅ **必须继承** |
| **Rendering** | 渲染方式 | ✅ | ✅ **必须继承** |
| **Font** | 字体（clean/handwritten/serif/display） | ✅ | ❌（插图无文字） |
| **Mood** | 情绪对比度（subtle/balanced/bold） | ✅ | ✅ **必须继承** |

### Banner 设计规则（参考 baoyu-cover-image）

封面图不是"插图加大字"，是**用文字设计主导画面的视觉作品**：

1. **文字占画面 50-70% 视觉权重**。不是角落小字，是 Banner 级大字
2. **字体 × 风格匹配表**（参考 baoyu font.md）——**每张 banner 的 prompt 必须显式写 `Font Application` 段**，否则模型会渲染成默认宋体：

| Font | 视觉特征 | 适配场景 |
|------|---------|---------|
| `clean` | 几何无衬线，锐利均匀 | 科技/职业/家居/现代都市/测评 |
| `handwritten` | 手写/毛笔，有机变化 | 美食/萌宠/情感治愈/旅行随笔 |
| `serif` | 经典衬线，编辑感强 | 怀旧/时尚杂志/家居/品牌 |
| `display` | 粗体装饰，强表达 | 美食招牌/ACG标题/运动爆发/二次元 |

3. **花字技法（参考 baoyu typography.md）**——Banner 至少用一种：

| 技法 | 视觉 | 适用 |
|------|------|------|
| `gradient` | 渐变色填充 | 美食、时尚、ACG、潮酷 |
| `stroke-text` | 描边文字 | 旅行、街头、运动、户外 |
| `shadow-3d` | 立体投影 | 美食招牌、ACG、3D 风格 |
| `highlight` | 高亮笔 | 测评卡、对比、关键数据 |
| `neon` | 霓虹辉光 | 旅行夜景、ACG、赛博感 |
| `handwritten` | 手写效果 | 美食、萌宠、情感 |
| `bubble` | 圆润气泡 | 萌宠、ACG、亲子 |
| `brush` | 毛笔质感 | 美食、旅行、中式家居 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `hero` | 主图放大特写 |
| Palette | `warm` (#FFECD2 底, #ED8936 橙, #C05621 赤陶, #F6AD55 金, #A0522D 焦糖) | 暖色食物色调 |
| Rendering | `photography` | 写实美食摄影，浅景深 |
| Font | `handwritten` | 手写 + 毛笔感，符合食物温度 |
| Mood | `bold` | 食欲感需要高饱和高对比 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `hero` | 城市地标或风景大场景 |
| Palette | `cinematic` (#1E3A5F 深蓝, #F4A261 暖橙, #E76F51 珊瑚, #2A9D8F 蓝绿) | 电影感城市色调 |
| Rendering | `photography` | 现代写实摄影（与怀旧照片的"老"区分） |
| Font | `display` | 粗体装饰，做"目的地"标题 |
| Mood | `balanced` | 平衡写实和戏剧感 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `character` | 角色为主（写实宠物 / Q版拟人） |
| Palette | `pastel` (#FFE5E5 粉, #E5F5FF 蓝, #FFF4D6 黄, #D4F4DD 绿, #B5E5CF 薄荷) | 马卡龙/奶油色 |
| Rendering | `painterly`（写实萌宠） / `flat-vector`（Q版） | 二选一 |
| Font | `display` | 圆润装饰字体 |
| Mood | `balanced` | 暖但不刺眼 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `hero` | 房间全景或单品陈设 |
| Palette | `earth` (#F5F0E8 米白, #D4B896 沙色, #8B7355 木色, #2F4F4F 深绿, #C19A6B 焦糖) | 自然/木质/大地色 |
| Rendering | `photography` | 室内写实摄影，柔光 |
| Font | `serif` | 衬线字体，编辑感强 |
| Mood | `subtle` | 低饱和，安静感 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `hero` | 全身或半身人物 |
| Palette | `elegant` (#FAFAFA 白, #1A1A1A 黑, #C9A96E 金, #8B4513 棕, #D4A09A 玫瑰) | 高级简约 |
| Rendering | `photography` | 时尚杂志摄影 |
| Font | `serif`（高端） / `display`（街头潮流） | 二选一 |
| Mood | `bold` | 高对比，强视觉 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `character` | 角色为主 |
| Palette | `vivid` (#FF6B9D 樱粉, #6BCB77 草绿, #4D96FF 群青, #FFD93D 金, #C780FA 紫) | 高饱和动漫色 |
| Rendering | `flat-vector` | 赛璐璐/原神风（手绘赛璐璐上色） |
| Font | `display` | 粗体装饰，漫画/标题感 |
| Mood | `bold` | 高饱和高对比 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `infographic` | 信息结构主导（不是插图） |
| Palette | `mono`（黑白灰） / `macaron`（彩卡） | 二选一 |
| Rendering | `flat-vector` | 矢量/几何分块 |
| Font | `clean` | 几何无衬线，最强可读性 |
| Mood | `balanced` | 数据需要清晰可读，不抢戏 |

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

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `hero` | 人物动态为主 |
| Palette | `vivid` (#FF4500 橙红, #1E1E1E 黑, #00C9A7 青绿, #FFD700 金, #2C3E50 深蓝) | 力量感强对比 |
| Rendering | `photography` | 运动摄影（高速快门凝固动作） |
| Font | `display` | 粗体爆发感 |
| Mood | `bold` | 高对比，高能量 |

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

## Workflow D: 快文配图（按句生成人物+场景草图）

适合短平快的文章、**每句一图**的批量配图需求（公众号内文、视频脚本、PPT 配图、新闻合集、卡片卡片集等）。**不是 PPT/文字海报——重点是"人物+场景"的手绘草图，每张图是一个有画面感的瞬间**。

**核心特点**：
- **每句一图，不限制数量**（100+ 句也要全跑）
- **必须有"人物 + 场景表现"**（不是文字大字海报，不是抽象装饰）
- 风格：彩色手绘草图（colored pencil / hand-drawn sketch）—— 可见笔触、有墨水轮廓、人物表情和动作清晰
- 走 dreamina CLI（文字不需要渲染成图，文字只作 prompt 输入参考，**图里可以加少量文字标签但不是主元素**）

### Step 1: 读取文章并拆分句子

Read the target `.md` file. Then:

1. 去掉图片行 `![](...)`
2. 去掉空行和 markdown 格式标记（**、#、- 等等）
3. 按句号/问号/感叹号/换行拆分：`re.split(r'[。！？\n]+', text)`
4. 过滤短于 3 字的片段
5. 超过 50 字的句子**智能截断**（到上一个逗号，否则直接截断加省略号）—— **不截断优先**：长句可分两图，第一句完结，第二句接续
6. **不合并句子**——每句独立配图，**不要合并"一句话生成 1 张"以外的逻辑**
7. 展示拆分结果 + 每张图的具体画面构思，让用户确认（可增删改句子）

### Step 2: 选择画面比例（**必做！**）

快文配图**不是必须竖屏**——用户可能想出横屏给视频号横屏/小红书横屏/公众号封面/朋友圈/微博头图。**必须问用户比例**，不要默认 9:16。

| 选项 | 比例 | 描述 |
|------|------|------|
| 📱 **9:16 竖屏** | `9:16` | 竖版——抖音、快手、视频号、朋友圈、小红书、微博头条 |
| 🖥️ **16:9 横屏** | `16:9` | 横版——B站、YouTube、横屏视频号、电脑端展示 |
| ⬜ **1:1 方形** | `1:1` | 正方形——公众号次条、小红书贴纸、微信图片消息 |
| 🎬 **21:9 宽幅 banner** | `21:9` | 超宽 banner——公众号头条封面、网页 banner |
| 📷 **4:3 经典** | `4:3` | 经典 4:3——演示文稿、传统相机比例 |
| 📖 **3:4 杂志竖版** | `3:4` | 杂志风竖版——小红书贴纸长图、杂志内文 |

**判断用户已暗示的比例**：
- 用户说"竖屏"/"抖音/快手/视频号/朋友圈" → 默认 9:16
- 用户说"横屏"/"B 站/YouTube" → 默认 16:9
- 用户说"封面/banner" → 默认 21:9
- 其他情况一律询问，让用户选

**所有 6 个比例都支持 dreamina CLI**（dreamina 支持 `21:9 16:9 1:1 9:16 4:3 3:4` 等）。

### Step 3: 选择手绘草图风格（**核心：人物+场景**）

Show 6 个手绘草图风格（from `references/quick-styles.md`）：

| # | 风格 | 一句话描述 |
|---|------|-----------|
| 1 | 🎨 彩色铅笔草图 | baoyu sketch-notes 风。可见笔触、墨水轮廓、macaron 色 |
| 2 | 🖋️ 钢笔淡彩 | 钢笔线条 + 淡彩水洗、像笔记本插画 |
| 3 | 🖍️ 蜡笔速写 | 蜡笔质感、温暖厚重、童书插画感 |
| 4 | 📸 漫画分镜 | 日式漫画分镜式、人物表情夸张、动感强 |
| 5 | 🌊 水墨淡彩 | 水墨淡彩、清雅留白、东方美学 |
| 6 | 📓 速写本+便签 | 像打开的速写本、有便签、印章装饰 |

Default: 1 (彩色铅笔草图) for 一般快文.

**关键渲染提示词**（每张图必加）：
```
Hand-drawn illustration, visible brush strokes, ink outline, 
soft watercolor wash, colored pencil texture, macaron palette, 
NOT photorealistic, NOT 3D, NOT anime, NOT digital render
```

### Step 4: 确认 Dreamina CLI 环境可用

**快文配图固定使用 dreamina，模型锁定 `4.7`**——4.7 在 Q 版卡通、马克笔手绘、文字+图标组合场景下表现最好。

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

### Step 5: 批量生成图片（dreamina 4.7）

**重要：每张图都是一个独立的"Q 版马克笔 + 大量手写体 + 背景小图标"组合**。每张图的 prompt 必须明确：

```
Q版二头身卡通人物 with 大头小身体, exaggerated expression, sweat drops or 
emotion symbols (sweat drops 汗珠 / exclamation marks 感叹号 / stars 星星). 
黑色手绘线条 (marker / tablet brush feel), 低饱和度水彩或 marker 平涂上色, 
块状色感. NOT photorealistic, NOT polished, NOT refined, NOT digital 
gradient, NOT 3D.

Subject: <Q版人物 + 动作 + 夸张表情 + 汗珠等情绪符号>. 关键元素：<1-3 个具体物件>.

Chinese handwritten text occupying the left/right half of the frame, 
GIANT bold handwritten style, sharp legible characters. 重点词高亮用不同颜色：
- 技术名词（如 "AI"、"MoE"、"transformer"）用紫色 #8B5CF6
- 情绪/难懂词（如 "不懂"、"难"、"卡住"）用橙色 #F97316
- 数字/关键数据用红色 #EF4444
- 否定/转折词（如 "但是"、"不是"、"没有"）用蓝色 #3B82F6

Background: small hand-drawn icons (lightbulb 💡, question mark ❓, 
moon 🌙, heart ❤️, brain 🧠, gear ⚙️, warning ⚠️) scattered around the 
frame, NOT overlapping with main text or character.
```

**单次命令**（模型锁定 4.7）：
```bash
dreamina text2image \
  --prompt="<每句独立的 Q版马克笔 prompt>" \
  --ratio=<用户选的比例> \
  --model_version=4.7 \
  --resolution_type=2k \
  --poll=180
```

**批量策略**（按句子数量分批）：

| 句子数量 | 策略 |
|---------|------|
| ≤10 句 | 全部并发（每 3 个一组），失败重试 1 次 |
| 11-30 句 | 分 3-5 批并发，每批 3-5 个 |
| 31-100 句 | 分 5-10 批，每批 3-5 个 |
| 100+ 句 | **必分批**（每批 ≤5 个），不要一次性并发，会触发速率限制 |

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

⚠️ **快文不是 PPT/文字海报**：
- ❌ 文字占 1/3 区域
- ❌ 大字标题 + 装饰元素
- ❌ 抽象图案
- ✅ **有人物在场景中**（人在做事、表情、动作）
- ✅ 场景表现（环境 + 人物 + 物件）
- ✅ 文字只作"小标签/便签"出现在角落
- ✅ 30+ 句话/100+ 句话全跑完

### dreamina 注意事项

- 末尾加 "colored pencil texture, visible brush strokes, ink outline"
- 强调 `hand-drawn, sketch, watercolor, storybook illustration`
- 排除 `photorealistic, 3D, anime, digital render`
- 每张图必须有"主体人物 + 动作 + 场景"三要素
- **不强制文字渲染**——文字只是参考，模型爱渲不渲

## Workflow N: 头条配图（彩色铅笔速写）

适合「每日AI快讯」类多新闻合集文章（如 `news/2606/0603.md`）。每条新闻生成 1 张 9:16 竖版**彩色铅笔速写**配图，参考 baoyu `sketch-notes` 风格 + 童书编辑插图感 + macaron 配色。

**风格定位：** colored pencil drawing（彩色铅笔画）—— 可见笔触、软蜡质感、多色叠加、暖系 macaron 配色。像一本写满彩色铅笔速写的笔记本。

**与 Workflow D（快文配图）的核心差异：**
- 快文是"句子+装饰元素"（6 种预制风格）；头条是"6 区多文字 + 真实场景速写"（统一墨水淡彩风）
- 快文每张独立；头条 10 张需保持"同一画家"笔触
- 快文文字是新闻句子全文；头条文字 = 报头 + 分类 + 标题 + 3 个 bullet + footer（多层级）
- 快文后端可选；头条**强制 Dreamina CLI**

### Step 1: 读取并解析新闻文件

读取目标 `.md` 文件，提取：
- **报头日期**：从文件名（如 `0603.md` → `6月3日`）或文档首行（如 "📰 每日AI快讯 | 6月3日"）解析
- **分类标签**：解析 `【🔥 AI大模型】` 等分类段（保留供 chip 配色）
- **新闻条目**：每条 `**{N}. {标题}** {描述}` 拆为 1 个 dict

### Step 2: AI 提炼每条新闻（关键步骤）

对每条新闻，AI 生成 4 个字段：

1. **`short_title`（精简标题）**：≤ 22 字（推荐 18 字内），保留核心主体+事件
2. **`bullets`（3 条关键事实）**：每条 ≤ 18 字，必须有数字/专有名词/关键动作
3. **`category`（分类）**：从 4 个分类中选一：`AI大模型` / `AI Agent` / `AI工具` / `AI行业动态`
4. **`scene_en`（英文场景描述）**：1-2 句英文，描述该新闻对应的**视觉化可画场景**（人物+动作+环境）

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

头条配图和快文配图一样，**不修改原文章**。封面/配图作为独立素材使用。

### 5 维默认值

| 维度 | 默认值 | 说明 |
|------|--------|------|
| Type | `infographic-sketch` | 教育信息图速写 |
| Palette | `macaron`（cream + 4 色 chip + 珊瑚红）| 有色彩的暖系 |
| Rendering | `colored-pencil` | 彩色铅笔（可见笔触 + 多色叠加）|
| Font | `handwritten` | 手写字体（带轻微 wobble）|
| Mood | `balanced` | 平衡戏剧性与可读性 |

### 4 个分类的配色

| 分类 | 填充色 | 配色名 |
|------|--------|--------|
| `AI大模型` | `#A8D8EA` 蓝 | macaron blue |
| `AI Agent` | `#D5C6E0` 紫 | lavender |
| `AI工具` | `#B5E5CF` 绿 | mint |
| `AI行业动态` | `#F8D5C4` 桃 | peach |

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

直接说"头条配图"/"新闻配图"/"资讯配图"/"AI快讯配图"也能触发本 Workflow。

---

## Workflow O: 数字插画 / Painterly 风格（独处/夜听/卧室场景专用）

适合**当代数字插画风**——不是水彩、不是胶片照片、不是 Excalidraw 手绘。笔触是**厚涂油画笔感**（thick visible oil paint brush strokes, dry brush texture），低饱和暖色，主角是数字绘画中的人物（不露脸）+ 卧室/书桌/窗户/城市夜景。

### 5 维默认

| 维度 | 默认值 |
|------|--------|
| **Type** | `illustration` 数字插画 |
| **Palette** | 暖色低饱和：cream #F5E0C8 / peach pink #F2C6B5 / muted gold #E8B57A / dusty blue #8B9DC3 / lavender shadow #C9B8D4 |
| **Rendering** | **数字插画 + 厚涂 painterly brush strokes + dry brush texture**（不是 watercolor 不是 ink wash 不是 photograph） |
| **Font** | serif + handwritten（封面标题用细手写/serif，截图清晰不乱码） |
| **Mood** | subtle，低对比，温暖中带安静 |

### 必含正向关键词（每张图都要有）

```
Digital painting, illustrated style, thick visible oil paint brush strokes, 
dry brush texture, soft warm muted palette (cream, peach pink, soft gold, 
dusty blue, lavender), low saturation, warm and cool color contrast, 
contemplative solitary mood
```

### 必含反向关键词（**关键！这是避免跑偏的核心**）

```
NOT watercolor, NOT ink wash, NOT wet on wet, NOT photograph, 
NOT photorealistic, NOT anime, NOT 3D rendering, NOT line art
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

### 字体选择（baoyu 标准 4 种）

| 风格 | 英文 keyword | 描述 | 适合 |
|------|-------------|------|------|
| 手写毛笔 | `handwritten` | warm hand-lettered with organic brush strokes, thick-thin contrast, slight ink bleed | 夜听 / 情感治愈 / 美食 / 萌宠 |
| 衬线经典 | `serif` | elegant serif with refined letterforms, classic editorial character | 怀旧 / 时尚 / 家居 |
| 极简无衬线 | `clean` | clean geometric sans-serif, modern minimal letterforms | 科技 / 测评 / 都市 |
| 装饰粗体 | `display` | bold decorative display, heavy expressive headlines | ACG / 运动 / 招牌 |

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

### 1:1 场景插图模板

```
Digital painting, illustrated style, thick visible oil paint brush strokes, 
dry brush texture. NOT watercolor, NOT ink wash, NOT photograph. 
[具体场景描述]. Soft warm muted palette (cream, peach pink, soft gold, 
dusty blue, lavender). Low saturation, warm and cool color contrast, 
contemplative mood. 1:1 square format.
```

### ⚠️ 即梦中文渲染注意

即梦对通讯录里的"Chinese name"理解弱，可能渲染成 Mom/Dad/Lila/Tom 等英文。如需中文，**必须在 prompt 里直接写**具体要渲染的字（如 "render the Chinese characters 老王 clearly"），并加 `Chinese text '老王' must be sharp legible` 强约束。

### 参考图

`novel/0602/沉默的时候/images/01-深夜翻手机.png`（确认是这种风格的"原型图"）

### 触发关键词

- 独处型夜听
- 深夜翻手机
- 数字插画 painterly
- 厚涂 brush strokes
- 卧室场景插画
- 暖色低饱和数字绘画

---

## Brand Watermark Rules

Brand info only appears on covers of "professional" styles:
- ✅ Tech, Blueprint, Cyberpunk, Corporate, Pixel Art, Travel/City, Home/Lifestyle, Fashion/Beauty, ACG/Anime, Review/Infographic, Sports/Fitness
- ❌ Emotional, Nostalgic Photo, Sketch Notes, Vintage, Kawaii, Watercolor, Screen Print, Zen Minimal, Food, Pet/Q-version, Digital Illustration / Painterly

When `brand.enabled` is false, no watermark on any style.

## API Provider Differences

| Feature | `grsai` | `openai` / `openai-compatible` / `local` |
|---------|---------|------------------------------------------|
| Cover endpoint | `/v1/images/generations` | `/v1/images/generations` |
| Illustration endpoint | `/v1/draw/completions` (SSE) | `/v1/images/generations` |
| Illustration request | `aspectRatio` + `replyType: "async"` | `size: "1024x1024"` |
| Illustration response | SSE stream | Standard JSON |

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
