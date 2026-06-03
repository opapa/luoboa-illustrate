# 科技风 (Tech)

## 封面 Prompt 模板

```
极具视觉张力的科技手绘风格公众号封面。背景是深蓝到深紫的微妙渐变。画面主体是Excalidraw风格的手绘架构图/概念图，使用白色和浅蓝色手绘线条绘制，线条带有手绘草稿的随性质感和微微的抖动感。图中包含方框、圆角矩形、箭头、连线等手绘元素，展示核心概念之间的逻辑关系，内容横向铺满画面。标题文字采用粗体手写风格，巨大醒目，占据画面上方或中心显著位置，带有微弱的发光效果确保在深色背景上清晰可读，确保在手机缩略图上也能清晰阅读。少量手绘图标(灯泡、齿轮、电路等)作为装饰点缀。整体风格是「暗色模式下的白板草稿」——既有科技感，又有手绘的亲切感和知识感。品牌标识：左上角显示「{brand.name} | {brand.website} | {brand.tagline}」，左下角显示网址「{brand.website}」。内容文字：<提炼的标题短句，2-3行中文>
```

## 插图 Prompt 模板

```
我在给我的公众号配图，请使用Excalidraw，其带有手绘、草稿的视觉风格，内容如下，你需要做删减，取核心内容：<原文段落内容>
```

- 封面尺寸：1920x832
- 插图尺寸：1024x1024
- 封面包含品牌标识（logo 参考图）
- 插图不含品牌标识

---

# 柔情风 (Emotional)

适合情感治愈类文章（小说/故事体裁）。

## 核心原则

1. 人物统一 — 用之前生成返回的URL作为参考图
2. 情节还原 — 把小说原文完整发给模型
3. **封面必须用5维艺术大字排版** — 标题是画面视觉主角，占中心40-70%，不是角落小字

## 封面设计

柔情风封面采用**5维艺术大字排版**设计（与怀旧照片风共用同一套 A-L 排版体系）。底图渲染方式根据正文风格选择：

| 底图渲染 | 适合什么 | 关键词 |
|----------|---------|--------|
| **painterly 水彩插画** | 莫兰迪色系正文插画 | soft watercolor wash, Morandi colors, visible brush strokes |
| **photography 写实摄影** | 实景照片正文 | natural light photography, high key low saturation |

### 封面构建流程

1. 用户选择5维排版风格（A-L，见下方速查表或怀旧照片风完整模板）
2. 用户选择底图渲染（painterly 或 photography）
3. 将选定的5维排版Prompt模板中的 RENDERING 替换为选定底图渲染的关键词
4. 替换 `<SCENE>` / `<MOOD>` / `<TITLE>` 占位符

### 5维排版风格速查（与怀旧照片风共用）

| # | 风格 | 适合情绪 | 5维映射 | 与柔情风契合度 |
|---|------|---------|---------|----------------|
| A | 🎬 日系电影感 | 温柔、回忆、和解 | typography/warm/painterly/serif/subtle | ⭐⭐⭐⭐⭐ |
| B | 📖 复古杂志风 | 文艺、深度、美学 | typography/retro/painterly/serif/subtle | ⭐⭐⭐⭐ |
| C | 🌿 自然呼吸感 | 安抚、冥想、静谧 | minimal/earth/painterly/clean/subtle | ⭐⭐⭐⭐ |
| D | ✉️ 信笺与手写 | 私密、倾诉、深夜 | metaphor/warm/hand-drawn/handwritten/subtle | ⭐⭐⭐⭐⭐ |
| E | 🌈 光影重叠 | 释怀、梦境、疗愈 | metaphor/duotone/digital/serif/balanced | ⭐⭐⭐⭐ |
| F | 🏮 极简新中式 | 禅意、松弛、断舍离 | minimal/mono/painterly/serif/subtle | ⭐⭐⭐⭐⭐ |
| G | 🎬 王家卫式 | 暧昧、孤独、浓烈 | typography/duotone/digital/serif/bold | ⭐⭐⭐⭐ |
| H | 📷 拍立得底栏 | 日常、亲情、手作 | scene/warm/hand-drawn/handwritten/subtle | ⭐⭐⭐⭐⭐ |
| K | 🌫️ 诗歌散排 | 释怀、独白、空灵 | minimal/mono/painterly/clean/subtle | ⭐⭐⭐⭐ |
| L | 📜 古书扉页 | 传承、故土、宗族 | typography/elegant/painterly/serif/subtle | ⭐⭐⭐⭐⭐ |

完整 Prompt 模板见本文件"怀旧照片风"章节的 A-L 模板。替换 RENDERING 部分即可适配柔情风底图。

### 柔情风默认推荐

- 排版风格：**A 日系电影感**（温柔+回忆+和解，最贴合情感治愈）
- 底图渲染：**painterly**（水彩插画，和正文莫兰迪插画统一）

### 封面核心原则

- **5维设计体系** — Type/Palette/Rendering/Font/Mood 五维度精确定义
- **文字即画面** — 标题是视觉主体，占画面中心40-70%
- **手机可读** — 缩略图上也能清楚辨认标题
- **无品牌标识** — 保持画面纯净
- **封面与正文风格统一** — painterly底图配莫兰迪插画正文，photography底图配实景正文

## 插图 Prompt 模板

**风格一致性要求**：插图必须继承封面5维参数中的 Palette + Rendering + Mood。根据封面选定的底图渲染方式，插图的视觉语言必须匹配：

**painterly底图（莫兰迪水彩插画）的插图模板：**

首次生成（无参考图）：
```
我在给我的公众号小说配插画，需要温暖治愈风格的插画。请使用柔和的莫兰迪色系水彩渲染，visible brush strokes, organic flowing edges, paper texture showing through transparent washes。色板：cream #FFFAF0, sage green #6B8F71, dusty rose #C4A882, warm brown #8B6F47。整体氛围 low contrast, muted desaturated, calm。画面要有足够的留白。小说原文情节如下，请画出这一幕的核心场景，注意人物外观请自行设计但要符合故事设定：
<本章节完整原文内容>
```

带参考图生成：
```
我在给我的公众号小说配插画，需要温暖治愈风格的插画。请参考附件中已生成的角色形象图，保持人物外观一致（发型、服装，五官特征），仅改变场景和动作。请使用柔和的莫兰迪色系水彩渲染，visible brush strokes, organic flowing edges, paper texture showing through transparent washes。色板：cream #FFFAF0, sage green #6B8F71, dusty rose #C4A882, warm brown #8B6F47。整体氛围 low contrast, muted desaturated, calm。画面要有足够的留白。小说原文情节如下，请画出这一幕：
<本章节完整原文内容>
```

**photography底图（实景摄影）的插图模板：**

首次生成（无参考图）：
```
我在给我的公众号小说配插画，需要温暖治愈风格的自然光摄影。高光低饱和度，soft natural light, shallow depth of field, clean precise edges。色板：haze blue #B8C9D9, soft white #F5F5F0, warm wood #C4A882。整体氛围 low contrast, muted desaturated, calm。画面要有足够的留白。小说原文情节如下，请画出这一幕的核心场景，注意人物外观请自行设计但要符合故事设定：
<本章节完整原文内容>
```

带参考图生成：
```
我在给我的公众号小说配插画，需要温暖治愈风格的自然光摄影。请参考附件中已生成的角色形象图，保持人物外观一致（发型、服装，五官特征），仅改变场景和动作。高光低饱和度，soft natural light, shallow depth of field, clean precise edges。色板：haze blue #B8C9D9, soft white #F5F5F0, warm wood #C4A882。整体氛围 low contrast, muted desaturated, calm。画面要有足够的留白。小说原文情节如下，请画出这一幕：
<本章节完整原文内容>
```

**如果封面选了特定的5维排版风格（A-L），插图的 Palette/Rendering/Mood 必须从该风格模板中提取对应参数，不能用默认值。**

- 封面不含品牌标识，保持画面纯净
- 第二张起必须传上一张返回的URL作为参考图

---

# 怀旧照片风 (Nostalgic Photo)

适合情感治愈、回忆、亲情、乡愁类文章。90年代写实照片风格。

## 核心原则

1. **英文 Prompt** — 国内 API（grsai 等）中文 prompt 易触发内容审核失败，统一使用英文写 prompt
2. **场景驱动** — 根据文章关键场景设计画面，不依赖 `##` 小标题
3. **色调叙事** — 温暖场景用暖黄暗角，失去/空荡场景切冷灰色调，用色调传达情绪变化
4. **无品牌标识** — 保持画面纯净
5. **不需要 ref-url** — 场景为主非人物连续性，每张图独立生成

## 封面 Prompt 模板

怀旧照片风的封面采用**5维艺术大字排版**设计（基于 baoyu-cover-image 设计体系）。照片作为底图，文章标题是画面的视觉主角，占据中心40-70%区域，通过艺术手法与照片交融。**不是宋体小字，是Banner级大字**。

用户选择文字排版风格（见下方12种 A-L），每种风格有独立的英文 Prompt 模板。默认推荐 G（王家卫式字幕）。

### 封面设计核心原则

- **5维设计体系** — 每种风格由 Type/Palette/Rendering/Font/Mood 五个维度精确定义，prompt中必须体现全部5个维度的特征
- **色值精确** — 使用hex色值而非模糊描述（"暖黄色"→"#F2CC8F mustard yellow"）
- **渲染可感** — 每种rendering有明确的线条/纹理/深度/元素特征，prompt必须描述
- **字体可辨** — font不写"宋体"，写具体视觉特征（"refined serif letterforms, structured strokes, editorial authority"）
- **文字即画面** — 标题不是配角，是视觉主体，占据画面中心40-70%区域
- **手机可读** — 在手机缩略图上也能清楚辨认标题内容
- **无品牌标识** — 保持画面纯净
- **无人物或背影/侧影为主** — 留想象空间
- **抓文章最有画面感的物件/场景做底图** — 比如灶台+腊肉、院子里修东西的背影、桌上打开的包裹

### 12种封面文字排版风格

每种风格标注5维映射（Type / Palette / Rendering / Font / Mood），prompt严格按5维构建。

| # | 风格 | 适合情绪 | 5维映射 | 与怀旧照片契合度 |
|---|------|---------|---------|----------------|
| A | 🎬 日系电影感 | 温柔、回忆、和解 | typography/warm/painterly/serif/subtle | ⭐⭐⭐⭐⭐ |
| B | 📖 复古杂志风 | 文艺、深度、美学 | typography/retro/painterly/serif/subtle | ⭐⭐⭐⭐ |
| C | 🌿 自然呼吸感 | 安抚、冥想、静谧 | minimal/earth/painterly/clean/subtle | ⭐⭐⭐⭐ |
| D | ✉️ 信笺与手写 | 私密、倾诉、深夜 | metaphor/warm/hand-drawn/handwritten/subtle | ⭐⭐⭐⭐⭐ |
| E | 🌈 光影重叠 | 释怀、梦境、疗愈 | metaphor/duotone/digital/serif/balanced | ⭐⭐⭐⭐ |
| F | 🏮 极简新中式 | 禅意、松弛、断舍离 | minimal/mono/painterly/serif/subtle | ⭐⭐⭐⭐⭐ |
| G | 🎬 王家卫式 | 暧昧、孤独、浓烈 | typography/duotone/digital/serif/bold | ⭐⭐⭐⭐ |
| H | 📷 拍立得底栏 | 日常、亲情、手作 | scene/warm/hand-drawn/handwritten/subtle | ⭐⭐⭐⭐⭐ |
| I | 🎵 唱片封面风 | 反叛、独立、态度 | hero/vivid/screen-print/display/bold | ⭐⭐⭐ |
| J | 📰 旧报纸头条 | 时代、变迁、历史 | typography/retro/digital/display/balanced | ⭐⭐⭐⭐⭐ |
| K | 🌫️ 诗歌散排 | 释怀、独白、空灵 | minimal/mono/painterly/clean/subtle | ⭐⭐⭐⭐ |
| L | 📜 古书扉页 | 传承、故土、宗族 | typography/elegant/painterly/serif/subtle | ⭐⭐⭐⭐⭐ |

### 各风格 Prompt 模板

> **模板中的占位符**：`<SCENE>` = 核心场景英文描述，`<MOOD>` = 画面氛围关键词，`<TITLE>` = 文章标题中文原文

---

**A：日系电影感（情绪叙事）**

5维：typography / warm / painterly / serif / subtle

适用场景：情感随笔、回忆、自我和解、温柔的小故事。

```
Typography-dominant cover art (21:9 landscape). <SCENE>. Soft focus vintage photography background, faded film grain, <MOOD>. PALETTE: warm — cream #FFFAF0 base, golden yellow #F6AD55 and warm orange #ED8936 soft glow, terracotta #C05621 accents, deep brown #744210 for text grounding. RENDERING: painterly — soft watercolor wash textures, visible brush strokes, organic flowing edges, paper texture showing through transparent washes. FONT: serif — elegant refined letterforms with structured proportional spacing, editorial authority, warm cream #F6AD55 text color with subtle warm glow. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous artistic characters occupying the central 50-60% of the frame, positioned in the lower-right area with generous negative space above (40%+ whitespace), like closing credits of an Ozu film. MOOD: subtle — low contrast, muted desaturated colors, light visual weight, calm refined aesthetic. Airy breathing room, poetic emotional healing vibe, subtle drop shadow on text, asymmetric layout, high design sense, 4k cinematic quality
```

---

**B：复古杂志风（文艺高级）**

5维：typography / retro / painterly / serif / subtle

适用场景：心理科普、深度好文、生活美学、治愈系书单推荐。

```
Typography-dominant cover art (21:9 landscape). <SCENE>. PALETTE: retro — cream off-white #F5F0E6 background, coral red #E07A5F and mustard yellow #F2CC8F accents, dark maroon #5D3A3A for text depth, faded teal #2F7373 subtle highlights. RENDERING: painterly — soft watercolor wash textures, visible brush strokes, color bleeds, organic flowing edges, aged paper texture showing through. FONT: serif — elegant refined letterforms with structured proportional spacing, editorial authority, dark maroon #5D3A3A text with coral red #E07A5F emphasis. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous artistic characters occupying the central 50-60% of the frame, some characters overlapping with translucent painted paper panels in retro colors, mixing elegant Chinese serif and retro modern sans-serif for visual rhythm. MOOD: subtle — low contrast, muted desaturated palette, light visual weight, calm refined aesthetic. Warm neutral tones, poetic and healing editorial style, highly artistic magazine cover, 4k
```

---

**C：自然呼吸感（静谧安抚）**

5维：minimal / earth / painterly / clean / subtle

适用场景：晚安心语、压力释放、冥想、亲近自然。

```
Minimal composition cover art (21:9 landscape). <SCENE>. Faint old photograph base with overlapping plant leaf shadows, <MOOD>. PALETTE: earth — sage green #6B8F71, warm brown #8B6F47, sky blue #87CEEB accents, cream #F5F0E6 base, moss #4A6741 for depth. RENDERING: painterly — soft watercolor wash textures, diluted color washes, organic flowing edges, paper texture visible through transparent areas. FONT: clean — geometric sans-serif letterforms, sharp uniform line weight, ultra-thin whisper-light weight, sage green #6B8F71 text color with slight transparency. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous ultra-thin elegant lettering occupying the central 50-60% of the frame, rendered with ultra-wide line spacing as if text is breathing on the image, text slightly transparent blending with plant shadows. MOOD: subtle — low contrast, muted desaturated earth tones, light visual weight, calm aesthetic, 60%+ whitespace. Healing calm vibes, ample negative space, modern fine-art aesthetic, 4k
```

---

**D：信笺与手写（情绪的私密倾诉）**

5维：metaphor / warm / hand-drawn / handwritten / subtle

适用场景：个人成长、树洞倾听、写给过去的自己、深夜疗愈。

```
Metaphor-driven cover art (21:9 landscape). <SCENE>. Old vintage photo background, <MOOD>. PALETTE: warm — cream #FFFAF0 base, warm orange #ED8936 soft glow, terracotta #C05621 ink tones, deep brown #744210 for ink depth. RENDERING: hand-drawn — sketchy organic strokes with visible imperfections, variable line weight, pencil/pen/marker texture, paper grain surface, natural hand tremor visible. FONT: handwritten — warm hand-lettered typography with organic brush strokes, friendly personal feel, natural variation in stroke weight, approachable human character, warm brown-black ink color #744210. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous warm fountain pen handwritten calligraphy occupying the central 50-60% of the frame, ink flow variations with slight tremor in strokes, torn kraft paper note fragments behind some characters, tactile scrapbook style, the photograph shows through translucent paper. MOOD: subtle — low contrast, muted warm tones, light visual weight, calm refined aesthetic. Nostalgic emotional healing, raw and authentic design, 4k
```

---

**E：光影重叠（虚实交织的梦境感）**

5维：metaphor / duotone / digital / serif / balanced

适用场景：走出阴霾、释怀、梦境解析、心理疗愈。

```
Metaphor-driven cover art (21:9 landscape). <SCENE>. <MOOD>. PALETTE: duotone — burnt orange #E8751A and deep teal #0A6E6E as the dominant pair (cinematic action feel), off-black #121212 background, warm cream #F5E6D0 for text highlights, amber #F4A623 accent. RENDERING: digital — clean precise edges, smooth surfaces with subtle gradients, frosted glass and blur effects, controlled soft shadows. FONT: serif — elegant refined letterforms with structured proportional spacing, warm cream #F5E6D0 text color with amber #F4A623 glow edges. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous semi-transparent characters occupying the central 60% of the frame, blending with the photograph through double exposure effect: some strokes dissolving into light, others catching rainbow prism flare, venetian blind shadows falling across the text, blurry ethereal text effect, text and image are one. MOOD: balanced — medium contrast, normal saturation, clear foreground/background separation. Stark two-color separation across composition, silhouettes in one color against the other, nostalgic yet modern, poetic healing atmosphere, fine art aesthetic, 4k
```

---

**F：极简新中式（中式美学的旷野感）**

5维：minimal / mono / painterly / serif / subtle

适用场景：中式生活美学、禅意、松弛感、断舍离。

```
Minimal composition cover art (21:9 landscape). <SCENE>. Wabi-sabi aged photo background, <MOOD>. PALETTE: mono — off-white #F5F0E6 background, charcoal #2D2D2D for primary text, warm gray #8C8C8C subtle elements, pure black #1A1A1A for emphasis, tiny vermilion red #C41E3A for seal stamp accent ONLY. RENDERING: painterly — soft diluted ink wash textures, organic flowing edges, rice paper texture visible through transparent areas, brush stroke patterns. FONT: serif — elegant refined letterforms with structured proportional spacing, editorial authority, charcoal #2D2D2D text color, thin weight. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous elegant thin serif characters occupying the central 50-60% of the frame, VERTICAL text alignment right-to-left, tiny vermilion red #C41E3A seal stamp accent in bottom corner ONLY. MOOD: subtle — low contrast, muted desaturated tones, light visual weight, calm aesthetic, 60%+ whitespace. Spacious zen healing vibe, high-end tranquility, characters floating in vast empty space, classical yet modern, 4k
```

---

**G：王家卫式字幕（情绪叙事）— 默认推荐**

5维：typography / duotone / digital / serif / bold

适用场景：暧昧、城市孤独、深夜、无法说出口的感情、一切情感类。

```
Typography-dominant cover art (21:9 landscape). <SCENE>. PALETTE: duotone — crimson #DC143C and navy #0D1B2A as the dominant pair (dramatic noir feel), off-black #121212 background, warm cream #F5E6D0 for text, amber #F4A623 inner glow. RENDERING: digital — clean precise edges, smooth surfaces, subtle controlled gradients, frosted glass effects, sharp shadows. FONT: serif — elegant refined letterforms with structured proportional spacing, warm cream #F5E6D0 text color with amber #F4A623 warm glow as if lit from within. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous artistic characters occupying the central 50-60% of the frame, centered lower area, the photograph bleeds through the semi-transparent text, like a line of dialogue frozen on screen in a Wong Kar-wai film. MOOD: bold — high contrast, vivid saturated colors (rich teal and warm amber grading), heavy visual weight, dynamic energy. One line of text carries the entire emotional weight, cinematic 4k quality
```

---

**H：拍立得底栏（日常手作感）**

5维：scene / warm / hand-drawn / handwritten / subtle

适用场景：亲情、日常、手作感、随拍记录、生活碎片。

```
Scene-driven cover art (21:9 landscape). <SCENE>. Nostalgic vintage photograph with warm tones, <MOOD>. PALETTE: warm — cream #FFFAF0 base, golden yellow #F6AD55 soft glow, warm orange #ED8936 for marker ink, terracotta #C05621 accents, deep brown #744210 for marker depth. RENDERING: hand-drawn — sketchy organic strokes with visible imperfections, variable marker line weight, casual fills with visible brush direction, paper grain surface. FONT: handwritten — warm hand-lettered typography with organic marker strokes, friendly personal feel, natural variation in stroke weight, warm orange #ED8936 marker ink color on white polaroid strip. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous handwritten marker-style characters occupying the central 50-60% of the frame, written on a white polaroid bottom strip that extends across the image, casual marker pen texture, slight tilt, authentic tactile feeling. MOOD: subtle — low contrast, muted warm tones, light visual weight, calm aesthetic. Personal memory keepsake, slight film grain, the text looks like someone grabbed a marker and wrote directly on the photo, 4k
```

---

**I：唱片封面风（独立精神）**

5维：hero / vivid / screen-print / display / bold

适用场景：青春、反叛、独立精神、城市漂泊、自我认同。

```
Hero composition cover art (21:9 landscape). <SCENE>. Vintage photograph background, <MOOD>. PALETTE: vivid — electric blue #3B82F6 and hot pink #EC4899 as dominant colors, deep purple #581C87 background, bright yellow #EAB308 accent, white #FFFFFF for text. RENDERING: screen-print — bold flat color blocks, visible halftone dot texture, limited color palette (3-4 colors), slight misregistration between color layers, strong graphic shapes. FONT: display — bold decorative display typography, heavy expressive letterforms, strong visual impact, attention-grabbing character, white #FFFFFF with hot pink #EC4899 offset shadow. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous bold display characters occupying the central 60% of the frame, centered or intentionally offset, geometric color blocks behind text. MOOD: bold — high contrast, vivid saturated colors, heavy visual weight, dynamic energy. Edgy and authentic, graphic overlay style, statement design, the text IS the cover art, 4k
```

---

**J：旧报纸头条（时代印记）**

5维：typography / retro / digital / display / balanced

适用场景：历史、社会变迁、回忆、时代感、家族往事。

```
Typography-dominant cover art (21:9 landscape). <SCENE>. PALETTE: retro — aged paper #F5E6D3 background, dark maroon #5D3A3A for headline text, coral red #E07A5F for emphasis, mustard yellow #F2CC8F for date line, rock blue #577590 for border lines. RENDERING: digital — clean precise edges, smooth surfaces, sharp corners, anti-aliased smooth rendering, consistent stroke weights. FONT: display — bold decorative display typography, heavy expressive letterforms, strong visual impact, dark maroon #5D3A3A text. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous bold display headline occupying the central 60% of the frame, vertical or horizontal text layout, thin border frame lines in rock blue #577590, date line in small mustard yellow #F2CC8F text, historical archive feeling. MOOD: balanced — medium contrast, normal saturation, clear hierarchy. Clipped newspaper cutting aesthetic, the headline dominates the page like a real newspaper front page, nostalgic and documentary, 4k
```

---

**K：诗歌散排（空灵释怀）**

5维：minimal / mono / painterly / clean / subtle

适用场景：释怀、告别、深夜独白、空灵、放下。

```
Minimal composition cover art (21:9 landscape). <SCENE>. <MOOD>. PALETTE: mono — off-white #F5F0E6 base, charcoal #2D2D2D for primary text, warm gray #8C8C8C for fading edges, pure black #1A1A1A for emphasis points. RENDERING: painterly — soft diluted ink wash textures, organic flowing edges, rice paper texture visible, brush stroke patterns, splatter and drip effects as accents. FONT: clean — geometric sans-serif letterforms, sharp uniform line weight, charcoal #2D2D2D text with warm gray #8C8C8C fading at edges. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous semi-transparent characters occupying the central 50-60% of the frame, but scattered asymmetrically across the image like poetry lines falling on a photograph, ultra-wide line spacing, ghost-like fading words, text dissolves at edges into ink wash. MOOD: subtle — low contrast, muted desaturated tones, light visual weight, calm aesthetic, 60%+ whitespace. Ethereal and airy composition, quiet contemplative mood, negative space as emotion, minimalist poetic design, 4k
```

---

**L：古书扉页（传承故土）**

5维：typography / elegant / painterly / serif / subtle

适用场景：家族、传承、故土、宗族、老宅、仪式。

```
Typography-dominant cover art (21:9 landscape). <SCENE>. Wabi-sabi aged paper texture background, <MOOD>. PALETTE: elegant — champagne gold #D4A843 for text, deep burgundy #4A1A2E background tones, warm ivory #F5E6D0 paper base, antique bronze #8B7355 subtle borders, tiny vermilion red #C41E3A for seal stamp accent ONLY. RENDERING: painterly — soft ink wash textures, organic flowing edges, aged rice paper texture visible through transparent areas, brush stroke patterns, classical calligraphic quality. FONT: serif — elegant refined letterforms with structured proportional spacing, editorial authority, champagne gold #D4A843 text color, thin weight. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous elegant serif characters occupying the central 50-60% of the frame, VERTICAL text right-to-left alignment, thread-bound book layout style with antique bronze #8B7355 subtle border lines, small vermilion red #C41E3A seal stamp accent in bottom corner ONLY. MOOD: subtle — low contrast, muted desaturated tones, light visual weight, calm aesthetic. Ancestral record feeling, classical refined aesthetic, the text reads like an ancient book title page, 4k
```

---

# 扁平插画风 (Flat Illustration)

适合职场干货、个人成长、知乎回答、知识科普类文章。干净矢量色块 + 限定色板 + 几何人物，得到/极客时间/知乎盐选的标准视觉语言。

## 核心原则

1. **色板严格** — 限定4-6色，不允许渐变，flat color fills only
2. **几何简化** — 人物/物件用基本几何形拼合，圆角+粗描边
3. **5维继承** — 插图必须继承封面 Palette + Rendering + Mood
4. **品牌水印** — 允许（professional style）

## 封面 — 5维艺术大字排版

推荐排版风格（与怀旧照片风共用A-L体系，替换RENDERING为flat-vector）：

| # | 排版风格 | 5维映射 | 与扁平插画契合度 |
|---|---------|---------|----------------|
| A | 🎬 日系电影感 | typography/warm/flat-vector/serif/subtle | ⭐⭐⭐⭐⭐ |
| B | 📖 复古杂志风 | typography/retro/flat-vector/serif/subtle | ⭐⭐⭐⭐⭐ |
| C | 🌿 自然呼吸感 | minimal/earth/flat-vector/clean/subtle | ⭐⭐⭐⭐⭐ |
| G | 🎬 王家卫式 | typography/duotone/flat-vector/serif/bold | ⭐⭐⭐⭐ |
| J | 📰 旧报纸头条 | typography/retro/flat-vector/display/balanced | ⭐⭐⭐⭐ |

### 封面默认5维

```
Type: typography / Palette: warm-cool / Rendering: flat-vector / Font: clean / Mood: balanced
```

### 封面 Prompt 模板（默认 B复古杂志风）

```
Typography-dominant cover art (21:9 landscape). <SCENE>. Flat vector illustration background, geometric shapes and simplified figures, limited color palette. PALETTE: warm-cool — clean white #FFFFFF base, coral #FF6B6B and teal #4ECDC4 as primary pair, warm yellow #FFE66D accent, slate #2D3436 for text depth, soft gray #DFE6E9 secondary shapes. RENDERING: flat-vector — bold flat color fills, no gradients, clean sharp edges, geometric simplification, consistent line weight, minimal shading with single-color shadows. FONT: clean — geometric sans-serif letterforms, sharp uniform line weight, slate #2D3436 text with coral #FF6B6B emphasis on key characters, modern professional clarity. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous clean geometric characters occupying the central 50-60% of the frame, flat color blocks behind text in coral and teal, the text reads like a premium infographic headline. MOOD: balanced — medium contrast, clean and professional, clear hierarchy. Modern editorial quality, brand watermark if enabled, 4k
```

## 插图 Prompt 模板

**风格一致性要求**：插图必须继承封面5维参数中的 Palette + Rendering + Mood。

```
Flat vector illustration for WeChat article. <场景英文描述>. RENDERING: flat-vector — bold flat color fills, no gradients, clean sharp edges, geometric simplification, consistent line weight, minimal shading with single-color shadows. PALETTE: clean white #FFFFFF base, coral #FF6B6B and teal #4ECDC4 primary, warm yellow #FFE66D accent, slate #2D3436 depth, soft gray #DFE6E9 secondary. MOOD: balanced — medium contrast, clean and professional, clear hierarchy. Simplified geometric people and objects, limited 4-6 colors, 4k
```

**如果封面选了特定A-L排版风格，插图的 Palette/Rendering/Mood 必须从该风格模板中提取对应参数。** 例：封面选G王家卫→插图用"crimson #DC143C and navy #0D1B2A" + "clean precise edges" + "high contrast, vivid saturated"。

## 色调指南

| 情绪 | 色调关键词 |
|------|-----------|
| 专业/职场 | clean white base, teal #4ECDC4, slate #2D3436, balanced |
| 温暖/成长 | warm yellow #FFE66D, coral #FF6B6B, cream #FFF8E7, subtle |
| 冷峻/锐评 | navy #0D1B2A, crimson #DC143C, stark contrast, bold |

---

# 杂志大片风 (Magazine Editorial)

适合人物故事、观点评论、深度报道类文章。高对比人像摄影 + 杂志封面排版 + 电影级光影，把人物推到视觉中心。

## 核心原则

1. **人物即画面** — 人是视觉主体，不是背景。背影/侧影/剪影为主，留想象空间
2. **电影级光影** — 明暗对比（chiaroscuro），浅景深，戏剧性布光
3. **5维继承** — 插图必须继承封面 Palette + Rendering + Mood
4. **品牌水印** — 允许（professional style）
5. **不需要 ref-url** — 场景为主，每张图独立生成

## 封面 — 5维艺术大字排版

推荐排版风格（与怀旧照片风共用A-L体系，替换RENDERING为photography）：

| # | 排版风格 | 5维映射 | 与杂志大片契合度 |
|---|---------|---------|----------------|
| A | 🎬 日系电影感 | typography/warm/photography/serif/subtle | ⭐⭐⭐⭐⭐ |
| B | 📖 复古杂志风 | typography/retro/photography/serif/subtle | ⭐⭐⭐⭐⭐ |
| D | ✉️ 信笺与手写 | metaphor/warm/photography/handwritten/subtle | ⭐⭐⭐⭐ |
| G | 🎬 王家卫式 | typography/duotone/photography/serif/bold | ⭐⭐⭐⭐⭐ |
| J | 📰 旧报纸头条 | typography/retro/photography/display/balanced | ⭐⭐⭐⭐⭐ |

### 封面默认5维

```
Type: typography / Palette: elegant / Rendering: photography / Font: serif / Mood: bold
```

### 封面 Prompt 模板（默认 G王家卫式）

```
Typography-dominant cover art (21:9 landscape). <SCENE>. High-contrast cinematic portrait photography, dramatic chiaroscuro lighting, shallow depth of field, film-quality bokeh. PALETTE: elegant — deep charcoal #1A1A1A shadows, warm ivory #F5E6D0 highlights, champagne gold #D4A843 accent, burgundy #6B2D3E midtones, pure white #FFFFFF catch light. RENDERING: photography — natural light photography, cinematic color grading, shallow depth of field, dramatic chiaroscuro lighting, film-quality bokeh, editorial retouching quality. FONT: serif — elegant refined letterforms with structured proportional spacing, editorial authority, warm ivory #F5E6D0 text with champagne gold #D4A843 subtle glow, magazine cover headline weight. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous editorial serif characters occupying the central 50-60% of the frame, positioned like a magazine cover headline, the photograph bleeds through semi-transparent text, editorial fashion quality. MOOD: bold — high contrast, rich saturated tones, heavy visual weight, dramatic energy. Magazine editorial cover quality, cinematic 4k
```

## 插图 Prompt 模板

**风格一致性要求**：插图必须继承封面5维参数中的 Palette + Rendering + Mood。

```
Cinematic editorial photograph for WeChat article. <场景英文描述>. RENDERING: photography — natural light photography, cinematic color grading, shallow depth of field, dramatic chiaroscuro lighting, film-quality bokeh, editorial retouching quality. PALETTE: deep charcoal #1A1A1A shadows, warm ivory #F5E6D0 highlights, champagne gold #D4A843 accent, burgundy #6B2D3E midtones. MOOD: bold — high contrast, rich saturated tones, heavy visual weight, dramatic energy. Magazine editorial photography quality, cinematic 4k
```

**如果封面选了特定A-L排版风格，插图的 Palette/Rendering/Mood 必须从该风格模板中提取对应参数。** 例：封面选A日系电影感→插图用"cream #FFFAF0, golden yellow #F6AD55" + "soft focus" + "low contrast, muted desaturated"。

## 色调指南

| 情绪 | 色调关键词 |
|------|-----------|
| 人物/故事 | warm ivory highlights, champagne gold accent, dramatic shadows, bold |
| 观点/锐评 | deep charcoal, stark contrast, crimson accents, bold |
| 回忆/温暖 | golden hour lighting, soft vignette, warm tones, balanced |

---

# 国潮新风 (Guochao / Neo-Chinese)

适合情感治愈（文化向）、人物故事（传统行业）、夜听（节日向）类文章。新中式纹样 + 书法笔触 + 朱砂墨色 + 留白，公众号情感文的流量密码。

## 核心原则

1. **古今融合** — 传统纹样（云纹/水纹/缠枝莲）用现代几何简化，不是纯古风临摹
2. **朱砂点睛** — vermilion red #C41E3A 只做印鉴/点缀，不做主色
3. **5维继承** — 插图必须继承封面 Palette + Rendering + Mood
4. **品牌水印** — 不允许（保持画面纯净）
5. **不需要 ref-url** — 场景为主，每张图独立生成

## 封面 — 5维艺术大字排版

推荐排版风格（与怀旧照片风共用A-L体系，替换RENDERING为国潮painterly）：

| # | 排版风格 | 5维映射 | 与国潮新风契合度 |
|---|---------|---------|----------------|
| A | 🎬 日系电影感 | typography/warm/guochao-painterly/serif/subtle | ⭐⭐⭐⭐ |
| C | 🌿 自然呼吸感 | minimal/earth/guochao-painterly/clean/subtle | ⭐⭐⭐⭐ |
| D | ✉️ 信笺与手写 | metaphor/warm/guochao-painterly/handwritten/subtle | ⭐⭐⭐⭐⭐ |
| F | 🏮 极简新中式 | minimal/mono/guochao-painterly/serif/subtle | ⭐⭐⭐⭐⭐ |
| K | 🌫️ 诗歌散排 | minimal/mono/guochao-painterly/clean/subtle | ⭐⭐⭐⭐⭐ |
| L | 📜 古书扉页 | typography/elegant/guochao-painterly/serif/subtle | ⭐⭐⭐⭐⭐ |

### 封面默认5维

```
Type: typography / Palette: elegant / Rendering: guochao-painterly / Font: serif / Mood: balanced
```

### 封面 Prompt 模板（默认 L古书扉页）

```
Typography-dominant cover art (21:9 landscape). <SCENE>. Ink wash and traditional Chinese pattern background with modern design sensibility, cloud and wave motifs in geometric simplification. PALETTE: elegant — ink black #1A1A1A primary, vermillion red #C41E3A accent ONLY for seal stamp, rice paper white #F5F0E6 base, antique gold #C9A227 secondary, jade green #2E8B57 subtle highlights. RENDERING: guochao-painterly — Chinese ink wash textures with visible brush strokes, calligraphic quality, rice paper texture visible through transparent washes, traditional pattern overlays (cloud motifs, wave patterns, floral scrolls) with modern geometric simplification, gold leaf accents. FONT: serif — elegant refined letterforms with calligraphic influence, structured proportional spacing with traditional stroke quality, ink black #1A1A1A text, thin weight, some strokes echoing brush calligraphy. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous elegant characters occupying the central 50-60% of the frame, accompanied by subtle traditional cloud or wave motifs in antique gold #C9A227, a small vermillion red #C41E3A seal stamp accent in bottom corner ONLY, the text reads like a modern reinterpretation of classical Chinese book art. MOOD: balanced — medium contrast, rich cultural tones, balanced visual weight, modern-traditional fusion aesthetic. Neo-Chinese high design sense, 4k
```

## 插图 Prompt 模板

**风格一致性要求**：插图必须继承封面5维参数中的 Palette + Rendering + Mood。

```
Neo-Chinese style illustration for WeChat article. <场景英文描述>. RENDERING: guochao-painterly — Chinese ink wash textures with visible brush strokes, calligraphic quality, rice paper texture visible through transparent washes, traditional pattern overlays (cloud motifs, wave patterns, floral scrolls) with modern geometric simplification, gold leaf accents. PALETTE: ink black #1A1A1A primary, vermillion red #C41E3A accent ONLY, rice paper white #F5F0E6 base, antique gold #C9A227 secondary, jade green #2E8B57 subtle. MOOD: balanced — medium contrast, rich cultural tones, modern-traditional fusion aesthetic. Neo-Chinese high design sense, 4k
```

**如果封面选了特定A-L排版风格，插图的 Palette/Rendering/Mood 必须从该风格模板中提取对应参数。** 例：封面选F极简新中式→插图用"charcoal #2D2D2D, off-white #F5F0E6" + "diluted ink wash" + "lowest contrast, muted desaturated"。

## 色调指南

| 情绪 | 色调关键词 |
|------|-----------|
| 节庆/团圆 | antique gold #C9A227, vermillion #C41E3A accent, warm ivory #F5F0E6, balanced |
| 思乡/离别 | ink black washes, rice paper white, muted jade green, subtle |
| 传承/故土 | deep ink textures, vermillion seal stamp, antique gold borders, balanced |

---

### 封面 Prompt 快速构建公式

```
[选定风格的Prompt模板]
替换: <SCENE> → 核心场景英文描述
替换: <MOOD>  → 氛围关键词（从色调对照表选）
替换: <TITLE> → 文章标题中文原文
```
