# 扩展风格详细 Prompt 模板

## 📷 3: 怀旧照片风 (nostalgic-photo)

### 封面 — 5维艺术大字排版（12种风格 A-L）

怀旧照片风封面采用**5维艺术大字排版**设计（基于 baoyu-cover-image 设计体系）。完整 Prompt 模板见 `style-guide.md` 中"12种封面文字排版风格"章节。

**快速构建公式：**
```
[选定风格的Prompt模板]
替换: <SCENE> → 核心场景英文描述
替换: <MOOD>  → 氛围关键词（从 style-guide.md 色调对照表选）
替换: <TITLE> → 文章标题中文原文
```

**12种封面文字排版风格速查：**

| # | 风格 | 5维映射 |
|---|------|---------|
| A | 🎬 日系电影感 | typography/warm/painterly/serif/subtle |
| B | 📖 复古杂志风 | typography/retro/painterly/serif/subtle |
| C | 🌿 自然呼吸感 | minimal/earth/painterly/clean/subtle |
| D | ✉️ 信笺与手写 | metaphor/warm/hand-drawn/handwritten/subtle |
| E | 🌈 光影重叠 | metaphor/duotone/digital/serif/balanced |
| F | 🏮 极简新中式 | minimal/mono/painterly/serif/subtle |
| G | 🎬 王家卫式 | typography/duotone/digital/serif/bold |
| H | 📷 拍立得底栏 | scene/warm/hand-drawn/handwritten/subtle |
| I | 🎵 唱片封面风 | hero/vivid/screen-print/display/bold |
| J | 📰 旧报纸头条 | typography/retro/digital/display/balanced |
| K | 🌫️ 诗歌散排 | minimal/mono/painterly/clean/subtle |
| L | 📜 古书扉页 | typography/elegant/painterly/serif/subtle |

### 插图

**插图（暖调）：**
```
Nostalgic 1990s photograph. <场景英文描述>. Faded yellowish film grain texture, vignette, warm golden tones, like a photograph kept in a drawer for thirty years.
```

**插图（冷调）：**
```
Nostalgic 1990s photograph. <场景英文描述>. Faded film grain texture, cool gray-blue tones, muted, vignette, desaturated, like a photograph kept in a drawer for thirty years. The scene feels lonely and empty.
```

**插图（克制/隐忍）：**
```
Nostalgic 1990s photograph. <场景英文描述>. Soft muted light, faded film grain texture, vignette, muted warm tones, quiet atmosphere, like a photograph kept in a drawer for thirty years.
```

**设计要点：**
- 封面文字是视觉主角，占中心40-70%，Banner级大字，5维艺术化处理
- 封面无人物或背影/侧影，留想象空间
- 统一使用英文 prompt（国内 API 中文易触发审核）
- 不需要 ref-url（场景独立，非人物连续性）
- 不含品牌标识
- 插图至少一张暖调+一张冷调，对比出情绪弧线

---

## 📐 4: 学术蓝图风 (blueprint)

5维：conceptual / cool / digital / clean / balanced

**封面：**
```
Conceptual cover art (21:9 landscape). PALETTE: cool — deep blue #1E3A5F background, steel blue #4A90D9 primary, ice white #E8F4FD highlights, slate gray #6B7B8D accents, electric cyan #00D4FF for data flow lines. RENDERING: digital — clean precise edges, smooth surfaces with subtle gradients, frosted glass panels, consistent stroke weights, anti-aliased rendering. FONT: clean — geometric monospace letterforms, sharp uniform line weight, ice white #E8F4FD text with electric cyan #00D4FF glow on key strokes, technical precision feel. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous clean technical characters occupying the central 40-50% of the frame, abstract system architecture diagram with grid lines, dimension markers, and annotation arrows surrounding the text, the text reads like a blueprint specification label. MOOD: balanced — medium contrast, precise and professional, clear hierarchy. Background has subtle fine grid texture #1E3A5F to #2A4A6F, brand watermark at top-left if enabled. 4k technical quality
```

**插图：**
```
我在给我的公众号技术文章配图，请使用技术蓝图/工程制图风格。深蓝色背景，白色线条和标注，带有网格底纹和尺寸标记。请将以下内容提炼为简洁的技术示意图：<原文段落内容>
```

---

## ✏️ 5: 手绘笔记风 (sketch-notes)

5维：conceptual / macaron / hand-drawn / handwritten / balanced

**封面：**
```
Conceptual cover art (21:9 landscape). PALETTE: macaron — warm cream #F5F0E8 background, soft lavender #B8A9C9, mint green #A8D8B9, peach pink #F4B8C1, butter yellow #F9E5A0, warm coral #E8655A for emphasis. RENDERING: hand-drawn — sketchy organic strokes with visible imperfections, variable line weight, pencil/marker texture, paper grain surface, natural hand tremor visible, wavy connectors and arrows. FONT: handwritten — warm hand-lettered typography with organic brush strokes, bouncy baselines, natural variation in stroke weight, warm coral #E8655A text color on cream background. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous hand-lettered characters occupying the central 50-60% of the frame, surrounded by hand-drawn keyword bubbles, doodle arrows, and sketchy decorative elements in macaron colors, the text reads like a giant handwritten note on a notebook page. MOOD: balanced — medium contrast, warm and friendly, approachable and inviting. Playful learning vibe, casual sketchbook feel, 4k
```

**插图：**
```
我在给我的公众号知识文章配图，请使用手绘笔记/涂鸦笔记风格。温暖奶白色背景，马卡龙色系点缀，手绘线条带有微微的抖动感，关键词用气泡框和箭头连接。请将以下内容提炼为可视化的笔记构图：<原文段落内容>
```

---

## 📜 6: 复古文艺风 (vintage)

5维：metaphor / retro / hand-drawn / serif / subtle

**封面：**
```
Metaphor-driven cover art (21:9 landscape). PALETTE: retro — aged paper #F5E6D3 background, coral red #E07A5F, mint green #81B29A, mustard yellow #F2CC8F, dark maroon #5D3A3A, vintage gold #C9A227. RENDERING: hand-drawn — sketchy organic strokes with visible imperfections, variable line weight, pencil/pen texture, aged paper grain surface with speckled foxing marks, natural hand tremor. FONT: serif — elegant refined letterforms with structured proportional spacing, editorial authority, dark maroon #5D3A3A text with vintage gold #C9A227 ornamental flourishes, classical decorative quality. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous elegant serif characters occupying the central 50-60% of the frame, classical decorative borders with filigree patterns, wax seal stamp element, quill pen motif, the text reads like a vintage book title page or old manuscript heading. MOOD: subtle — low contrast, muted desaturated palette, warm aged tones, light visual weight, nostalgic refined aesthetic. Timeless cultural depth, 4k
```

**插图：**
```
我在给我的公众号文章配图，请使用复古文艺风格。做旧纸张背景，泛黄褐色调，古典装饰边框，带有岁月质感的纹理。请为以下内容创作复古风格的插图：<原文段落内容>
```

---

## 🌸 7: 可爱萌系风 (kawaii)

5维：hero / pastel / flat-vector / display / balanced

**封面：**
```
Hero composition cover art (21:9 landscape). PALETTE: pastel — soft pink #FFB6C1, cream yellow #FFFACD, mint green #B8F0C8, lavender #E6E6FA, warm white #FFFAF0 background, bubblegum pink #FF69B4 for text emphasis. RENDERING: flat-vector — bold flat color fills, no gradients, thick consistent outlines #4A4A4A, rounded corners on all shapes, clean sharp edges, cartoon simplification. FONT: display — bold rounded decorative display typography, heavy expressive letterforms, thick bubbly strokes, warm white #FFFAF0 text with thick #4A4A4A outline, playful and cute. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous bold bubbly display characters occupying the central 50-60% of the frame, surrounded by cute kawaii elements: stars ★, hearts ♥, clouds ☁, sparkles ✦ in pastel colors, the text looks like it's made of soft marshmallow. MOOD: balanced — medium contrast, soft and sweet, lively and joyful. Kawaii aesthetic, adorable and playful, 4k
```

**插图：**
```
我在给我的公众号生活类文章配图，请使用可爱萌系/卡哇伊风格。粉嫩配色，粗描边，圆滚滚的造型，可爱的装饰元素（星星、爱心、云朵）。请为以下内容创作萌系插图：<原文段落内容>
```

---

## 🌆 8: 赛博霓虹风 (cyberpunk-neon)

5维：hero / dark / digital / display / bold

**封面：**
```
Hero composition cover art (21:9 landscape). PALETTE: dark — deep purple-black #0D0221 background, electric blue #00F0FF, neon magenta #FF00FF, toxic green #39FF14, hot pink #FF1493, bright yellow #FFE600. RENDERING: digital — clean precise edges, smooth surfaces, strong neon glow effects, chromatic aberration on edges, scan-line interference, frosted glass panels with holographic reflection. FONT: display — bold futuristic display typography, heavy geometric letterforms with angular cuts, neon glow effect electric blue #00F0FF with magenta #FF00FF offset shadow, glitch distortion on select characters. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous bold futuristic display characters occupying the central 55-65% of the frame, digital rain and holographic projection elements behind text, glitch art artifacts, circuit board traces as decorative lines. MOOD: bold — maximum contrast, vivid saturated neon colors, heavy visual weight, intense dynamic energy. Cyberpunk dystopian atmosphere, 4k
```

**插图：**
```
我在给我的公众号科技文章配图，请使用赛博朋克霓虹风格。深紫黑背景，霓虹发光线条，故障艺术效果，全息投影质感。请为以下内容创作赛博风格的插图：<原文段落内容>
```

---

## 💼 9: 极简商务风 (corporate)

5维：conceptual / elegant / digital / clean / subtle

**封面：**
```
Conceptual cover art (21:9 landscape). PALETTE: elegant — pure white #FFFFFF background, charcoal gray #333333 primary, champagne gold #D4A843 accent, slate gray #6B7B8D secondary, warm gray #E8E8E8 subtle geometric shapes. RENDERING: digital — clean precise edges, smooth surfaces, minimal shadows with consistent direction, frosted glass card elements, anti-aliased rendering, material design elevation. FONT: clean — geometric sans-serif letterforms, sharp uniform line weight, charcoal gray #333333 text with champagne gold #D4A843 accent line underneath, modern professional clarity. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous clean geometric characters occupying the central 40-50% of the frame, positioned with generous whitespace (50%+), subtle geometric shapes (ascending bars, growth arrows, abstract silhouettes) in warm gray #E8E8E8 behind the text, minimal supporting elements. MOOD: subtle — low contrast, muted professional tones, light visual weight, calm authoritative aesthetic. Corporate premium quality, brand watermark if enabled, 4k
```

**插图：**
```
我在给我的公众号商业分析文章配图，请使用极简商务风格。克制配色，干净几何构图，简洁的图表和箭头，专业高端的视觉语言。请为以下内容创作商务风格的插图：<原文段落内容>
```

---

## 🍃 10: 自然水彩风 (watercolor)

5维：scene / earth / painterly / handwritten / subtle

**封面：**
```
Scene-driven cover art (21:9 landscape). PALETTE: earth — sage green #6B8F71, warm brown #8B6F47, sky blue #87CEEB, cream #F5F0E6, moss #4A6741, terracotta #C05621. RENDERING: painterly — soft watercolor wash textures, visible brush strokes, color bleeds and wet-on-wet effects, organic flowing edges, paper texture showing through transparent washes, splatter and drip accents. FONT: handwritten — warm hand-lettered typography with organic brush strokes, natural variation in stroke weight, friendly personal feel, deep moss green #4A6741 ink color, calligraphic brush quality. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous watercolor brush calligraphy characters occupying the central 50-60% of the frame, painted directly on the watercolor background with visible brush stroke texture, color bleeds at character edges, natural elements (leaves, distant mountains, water reflections) flowing around the text. MOOD: subtle — low contrast, muted desaturated earth tones, light visual weight, calm serene aesthetic. Healing natural atmosphere, 4k
```

**插图：**
```
我在给我的公众号自然生活类文章配图，请使用自然水彩风格。柔和大地色系，水彩晕染边缘，有机笔触，自然元素。请为以下内容创作水彩风格的插图：<原文段落内容>
```

---

## 🕹️ 11: 像素游戏风 (pixel-art)

5维：hero / vivid / pixel / display / bold

**封面：**
```
Hero composition cover art (21:9 landscape). PALETTE: vivid — deep navy #1A1A2E background, bright yellow #FFE600 primary, pixel green #00FF41, hot pink #FF1493, electric blue #3B82F6, white #FFFFFF. RENDERING: pixel — 8-bit pixel art style, visible square pixels, hard edges with no anti-aliasing, limited color palette (6-8 colors), dithering patterns for gradients, retro game console aesthetic. FONT: display — bold pixel font typography, blocky square letterforms made of visible pixels, bright yellow #FFE600 text with white #FFFFFF pixel outline, 8-bit arcade game title screen feel. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous bold pixel characters occupying the central 55-65% of the frame, retro game UI elements around text: health bar, coin counter ★, dialog box border, pixel art characters, 8-bit star field background. MOOD: bold — high contrast, vivid saturated colors, heavy visual weight, nostalgic playful energy. Retro gaming culture, brand watermark in pixel style if enabled, 4k
```

**插图：**
```
我在给我的公众号极客趣味文章配图，请使用8-bit像素游戏风格。复古像素画，鲜明色块，马赛克质感，游戏界面元素。请为以下内容创作像素风格的插图：<原文段落内容>
```

---

## 🎭 12: 海报丝印风 (screen-print)

5维：typography / duotone / screen-print / display / bold

**封面：**
```
Typography-dominant cover art (21:9 landscape). PALETTE: duotone — choose ONE pair: orange #E8751A + teal #0A6E6E (cinematic), red #C0392B + cream #F5E6D0 (classic), blue #1A3A5C + gold #D4A843 (premium), crimson #DC143C + navy #0D1B2A (noir). Off-black #121212 background. RENDERING: screen-print — bold flat color blocks, visible halftone dot texture, limited color palette (2-3 colors only), slight misregistration between color layers for authentic print feel, strong graphic shapes with sharp edges, no gradients. FONT: display — bold decorative display typography, heavy expressive letterforms with maximum visual impact, cream #F5E6D0 or white text with slight offset shadow in second duotone color, mondo poster style. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous bold screen-printed display characters occupying the central 55-65% of the frame, strong visual metaphor symbol behind text, stark two-color separation across entire composition. MOOD: bold — maximum contrast, vivid saturated colors, heavy visual weight, bold provocative energy. Limited-edition poster art, brand watermark if enabled, 4k
```

**插图：**
```
我在给我的公众号深度评论文章配图，请使用丝网印刷海报风格。大色块对比，半调网点纹理，有限套色，强烈视觉符号。请为以下内容创作海报风格的插图：<原文段落内容>
```

---

## 🧘 13: 禅意留白风 (zen-minimal)

5维：minimal / mono / painterly / serif / subtle

**封面：**
```
Minimal composition cover art (21:9 landscape). PALETTE: mono — pure white #FFFFFF or warm ivory #F8F6F0 background, charcoal #2D2D2D for text, warm gray #C0C0C0 for the single element, pure black #1A1A1A for emphasis point, no other colors. RENDERING: painterly — single brush stroke in sumi-e ink wash style, diluted ink texture, organic flowing edges, rice paper texture visible, minimal brush strokes (3-5 strokes maximum). FONT: serif — elegant refined thin serif letterforms, structured proportional spacing, editorial authority, charcoal #2D2D2D text color, ultra-thin weight, ample breathing room between characters. The LARGE TITLE TEXT「<TITLE>」is the visual hero — enormous elegant thin serif characters occupying the central 40-50% of the frame, floating in vast empty space (60%+ whitespace), a single sumi-e brush stroke element as the only visual companion, the text breathes in the emptiness. MOOD: subtle — lowest contrast, muted desaturated tones, lightest visual weight, calm meditative aesthetic, maximum breathing room. Zen contemplation, wabi-sabi beauty, 4k
```

**插图：**
```
我在给我的公众号哲学/极简类文章配图，请使用禅意留白风格。大面积留白，单色极简线描，最少的元素表达核心概念。请为以下内容创作极简禅意插图：<原文段落内容>
```
