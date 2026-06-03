# 快文配图风格模板（Workflow D）

每句生成一张"人物+场景"手绘草图。**不是 PPT/文字海报——重点是"人在做事"的画面感**。每张图对应文章的一句话，prompt 必须明确写出**主体人物 + 动作 + 场景 + 关键物件**。

## 通用 Prompt 结构

```
A hand-drawn <风格名> illustration in <色板> palette. Scene: <具体描述人物+动作+环境>. Visible brush strokes, ink outline, soft watercolor wash, storybook illustration style. NOT photorealistic, NOT 3D rendering, NOT anime, NOT digital gradient. The Chinese text '{句子}' may appear as a small handwritten label/caption in a corner, NOT the main visual element.

Key elements:
- 主体人物: <具体人物、动作、表情>
- 场景环境: <具体环境>
- 物件细节: <1-3 个具体物件>
- 氛围: <温暖/孤独/紧张/温馨 等>
```

**关键规则：**
- **每张图必须有"主体人物 + 动作 + 场景"**——不能只画个物件
- 文字可以出现在画面里（如便签、报纸标题、书页），但**不是主元素**
- 每个 prompt 末尾加 `NOT photorealistic, NOT 3D rendering, NOT anime, NOT digital gradient`
- 模型默认用 `high_aes_general_v50`

---

## 1. 🖍️ 马克笔 Q 版卡通 (marker-q-chibi)

**风格关键词：** Q 版二头身、大头小身体、夸张表情、汗珠等情绪符号、黑色手绘马克笔/平板笔刷线条、低饱和度色块平涂

**色板：** cream #FAF3E7 / soft black #1A1A1A（线条）/ pastel red #FFB5B5（高光）/ pastel yellow #FFE9A8 / pastel blue #B5E0FF

**核心要素（每张图必含）：**
1. **人物**：Q 版二头身卡通，大头小身体（约头：身 = 1:1），夸张表情（紧张/惊讶/发愁/开心/恍然大悟 等）
2. **情绪符号**：汗珠、感叹号、星星、问号等小图标飘在人物头上/周围
3. **线条与色彩**：黑色手绘马克笔/平板笔刷线条 + 低饱和度马克笔平涂上色，块状色感
4. **背景小图标**：灯泡💡、问号❓、月亮🌙、爱心❤️、大脑🧠、齿轮⚙️、警告⚠️ 等手绘小元素散落

**Prompt 模板：**
```
Q版二头身卡通人物 (big head, small body, chibi style). 
<具体人物>在<具体场景>，表情<夸张表情>，头上/周围有<汗珠/感叹号/星星/问号 等情绪符号>.

黑色手绘线条 (marker / tablet brush feel), 低饱和度水彩或 marker 平涂上色, 
块状色感. NOT photorealistic, NOT polished, NOT refined, NOT digital 
gradient, NOT 3D, NOT anime.

Subject: <Q版人物 + 动作 + 夸张表情 + 1-3 个情绪符号>. 
关键元素：<1-3 个具体物件>.

Chinese handwritten text occupying the LEFT/RIGHT half of the frame, 
GIANT bold handwritten style, sharp legible characters. 重点词用不同颜色高亮：
- 技术名词（如 "AI"、"MoE"、"transformer"）→ 紫色 #8B5CF6
- 情绪/难懂词（如 "不懂"、"难"、"卡住"）→ 橙色 #F97316
- 数字/关键数据 → 红色 #EF4444
- 否定/转折词（如 "但是"、"不是"、"没有"）→ 蓝色 #3B82F6

Background: small hand-drawn icons (lightbulb, question mark, moon, 
heart, brain, gear, warning) scattered around the frame, NOT overlapping 
with main text or character.
```

**适合：** 科技/职场/生活/观点类快文 — 情绪化、有冲击力、易传播的速读场景

**模型：** `4.7`（dreamina 4.7 对 Q 版 + 马克笔 + 文字高亮表现最好）

---

## 2. 🖋️ 钢笔淡彩 (pen-watercolor)

**风格关键词：** 钢笔线条、淡彩水洗、笔记本插画感、有墨水轮廓

**色板：** muted teal #4A7C7E / cream #F4E8D0 / soft red #C16E70 / brown #6B4F3A

**Prompt 模板：**
```
A pen-and-ink and watercolor wash illustration in muted teal/cream/soft 
red palette. 

Scene: <人物>在<场景>做<具体动作>，表情<具体表情>。
Fine ink linework, soft watercolor washes, visible brush strokes, 
notebook sketch feel. NOT photorealistic, NOT 3D, NOT anime.

The Chinese text '{句子}' may appear as a small handwritten label in 
a corner.

Key elements:
- 主体人物: <具体人物、动作、表情>
- 场景环境: <具体环境>
- 物件细节: <1-3 个具体物件>
- 氛围: <温暖/孤独/紧张/温馨 等>
```

**适合：** 历史、游记、复古主题

---

## 3. 🖍️ 蜡笔速写 (crayon-sketch)

**风格关键词：** 蜡笔质感、温暖厚重、童书插画感

**色板：** warm yellow #F4D35E / coral #FF6B6B / sage #88D8B0 / cream #FFFAEB / navy #2C3E50

**Prompt 模板：**
```
A crayon-textured illustration in warm yellow/coral/sage/cream palette. 
Children's book art style, soft and warm.

Scene: <人物>在<场景>做<具体动作>，表情<具体表情>。
Crayon strokes, soft and warm, picture book illustration. NOT photorealistic, 
NOT 3D, NOT anime, NOT digital gradient.

The Chinese text '{句子}' may appear as a small handwritten label.

Key elements:
- 主体人物: <具体人物、动作、表情>
- 场景环境: <具体环境>
- 物件细节: <1-3 个具体物件>
- 氛围: <温暖/孤独/紧张/温馨 等>
```

**适合：** 童年、亲情、生活方式

---

## 4. 📸 漫画分镜 (manga-storyboard)

**风格关键词：** 日式漫画分镜、人物表情夸张、动感强、对话框

**色板：** black ink / cream / accent red / sky blue

**Prompt 模板：**
```
A Japanese manga storyboard style illustration in ink with cream/red/blue 
accents. Panel composition with strong dynamic lines.

Scene: <人物>在<场景>做<具体动作>，表情夸张<具体表情>。
Bold ink lines, dynamic motion lines, manga panel framing. NOT photorealistic, 
NOT watercolor, NOT 3D. Cel-shaded with minimal flat color.

The Chinese text '{句子}' may appear in a speech bubble or caption box.

Key elements:
- 主体人物: <具体人物、动作、表情>
- 场景环境: <具体环境>
- 物件细节: <1-3 个具体物件>
- 氛围: <紧张/激烈/搞笑/温馨 等>
```

**适合：** 观点、评论、争议话题

---

## 5. 🌊 水墨淡彩 (ink-wash)

**风格关键词：** 水墨淡彩、清雅留白、东方美学

**色板：** 淡墨 #2C2C2C / 米白 #F8F4EC / 桃粉 #E8B4A0 / 淡青 #A8C3B0

**Prompt 模板：**
```
A Chinese ink wash painting with light color accents (ink, cream, peach, 
sage). Generous empty space, minimal brushwork, East Asian aesthetic.

Scene: <人物>在<场景>做<具体动作>，表情<具体表情>。
Ink wash, light watercolor tint, generous negative space, contemplative 
mood. NOT photorealistic, NOT 3D, NOT anime, NOT heavy digital render.

The Chinese text '{句子}' may appear as a small vertical/horizontal 
calligraphy in a corner.

Key elements:
- 主体人物: <具体人物、动作、表情>
- 场景环境: <具体环境>
- 物件细节: <1-3 个具体物件>
- 氛围: <空灵/禅意/淡泊/宁静 等>
```

**适合：** 国风、哲思、抒情

---

## 6. 📓 速写本+便签 (sketchbook-sticky)

**风格关键词：** 速写本、有便签、印章装饰、像打开的笔记本

**色板：** cream paper #F4E9D6 / pencil gray #4A4A4A / accent red #C8443A / sage #7A8B6A

**Prompt 模板：**
```
An open sketchbook page illustration. Pencil sketches with watercolor 
touches, sticky notes, a small red seal stamp (yinzhang) in corner. 
Hand-drawn notebook feel.

Scene: <人物>在<场景>做<具体动作>，表情<具体表情>。
Pencil linework, watercolor washes, paper texture, mixed media sketchbook. 
NOT photorealistic, NOT 3D, NOT anime, NOT digital render.

The Chinese text '{句子}' may appear as if handwritten in the sketchbook 
margin or on a sticky note.

Key elements:
- 主体人物: <具体人物、动作、表情>
- 场景环境: <具体环境>
- 物件细节: <1-3 个具体物件>
- 氛围: <温暖/孤独/紧张/温馨 等>
```

**适合：** 笔记、随笔、文艺主题

---

## ⚠️ 最关键的硬规则

**每张图必须包含：**
1. **主体人物**（具体身份：男/女/老师/工人/小孩 + 动作 + 表情）
2. **场景环境**（具体地点：街角/办公室/教室/家里/路边 + 时间/光线）
3. **1-3 个关键物件**（让人物有事可做）
4. **氛围关键词**（温暖/孤独/紧张/温馨/怀念 等）

**反例（不要的）：**
- ❌ 只有文字 + 抽象图案
- ❌ 大字标题占满画面
- ❌ 没有人物
- ❌ 没有具体场景
