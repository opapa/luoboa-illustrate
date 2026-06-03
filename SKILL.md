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

Also trigger Workflow D directly when user says "快文配图"/"快文"/"视频素材"/"按句配图".
Also trigger Workflow E directly when user says "怀旧照片"/"怀旧风"/"老照片"/"90年代照片"/"胶片风".

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
2. **字体 × 风格匹配表**（参考 baoyu font.md）：

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

### Step 3: 确保 Dreamina CLI 环境可用

检查 `dreamina` CLI 是否已安装并登录：

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

### Step 4: 批量生成图片

使用 `dreamina text2image` 逐句生成：

```bash
dreamina text2image \
  --prompt="<快文风格的prompt，含文字渲染>" \
  --ratio=9:16 \
  --resolution_type=2k \
  --poll=30
```

批量生成流程：
1. 遍历拆分好的句子列表
2. 每句构建 prompt（含风格模板 + 文字内容）
3. 调用 `dreamina text2image` 生成
4. 从返回 JSON 中提取 `image_url`，用 `curl` 下载保存为 `01.png`, `02.png` 等
5. 失败的重试一次，仍然失败则跳过并标记 ❌
6. 写入 `sentences.txt` 记录序号|原文|状态对照表

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
- Dreamina CLI 的 `text2image` 命令会自动处理模型选择和轮询，不需要手动指定模型
- 并发生成建议不超过 3 个，避免触发速率限制

## Brand Watermark Rules

Brand info only appears on covers of "professional" styles:
- ✅ Tech, Blueprint, Cyberpunk, Corporate, Pixel Art, Travel/City, Home/Lifestyle, Fashion/Beauty, ACG/Anime, Review/Infographic, Sports/Fitness
- ❌ Emotional, Nostalgic Photo, Sketch Notes, Vintage, Kawaii, Watercolor, Screen Print, Zen Minimal, Food, Pet/Q-version

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
