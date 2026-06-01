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

## 封面子风格选择

| 编号 | 子风格 | 描述 |
|------|--------|------|
| A | 治愈系手绘/插画风 | 莫兰迪色/奶油色/水彩淡彩，线条简洁，毛绒质感或水彩晕染 |
| B | 极简清新摄影风 | 高光低饱和度，自然光捕捉生活微小美好 |
| C | 文艺留白排版风 | 大面积纯色或低饱和风景，角落留大片空白，手写体文字 |
| D | 电影胶片/温暖光影风 | 淡淡颗粒感，暗角、暖黄色调，黄昏夕阳，逆光剪影 |

## 封面 Prompt 模板 (B - 默认)

```
极简清新风格的公众号封面，自然光摄影，高光低饱和度。<从小说内容提炼的核心场景人物>。背景是柔和的雾霾蓝渐变，桌面是浅木色。整个画面安静、岁月静好，上方或角落留出空白用于放置文字。字体建议选择圆体或宋体，奶白色。内容文字：<标题短句>
```

## 插图 Prompt 模板

首次生成（无参考图）：
```
我在给我的公众号小说配插画，需要温暖治愈风格的插画。请使用柔和的莫兰迪色系，线条简洁，整体氛围安静、温暖、放松。画面要有足够的留白。小说原文情节如下，请画出这一幕的核心场景，注意人物外观请自行设计但要符合故事设定：
<本章节完整原文内容>
```

带参考图生成：
```
我在给我的公众号小说配插画，需要温暖治愈风格的插画。请参考附件中已生成的角色形象图，保持人物外观一致（发型、服装，五官特征），仅改变场景和动作。请使用柔和的莫兰迪色系，线条简洁，整体氛围安静、温暖、放松。画面要有足够的留白。小说原文情节如下，请画出这一幕：
<本章节完整原文内容>
```

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

### 封面 Prompt 快速构建公式

```
[选定风格的Prompt模板]
替换: <SCENE> → 核心场景英文描述
替换: <MOOD>  → 氛围关键词（从色调对照表选）
替换: <TITLE> → 文章标题中文原文
```
