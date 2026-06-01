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

```
Nostalgic 1990s photograph. <核心场景英文描述>. Faded yellowish film grain texture, vignette, warm golden tones, like a photograph kept in a drawer for thirty years. <画面氛围：quiet and solitary / warm and peaceful / lonely and empty>
```

**封面设计要点：**
- 无人物或背影/侧影为主，留想象空间
- 抓文章最有画面感的一个物件/场景做封面
- 比如灶台+腊肉、院子里修东西的背影、桌上打开的包裹

## 场景插图 Prompt 模板

场景插图不需要 `##` 小标题，AI 阅读全文后选择 2-3 个关键场景。

**温暖场景（暖调）：**
```
Nostalgic 1990s photograph. <场景英文描述>. Faded yellowish film grain texture, vignette, warm golden tones, like a photograph kept in a drawer for thirty years.
```

**冷清/失去场景（冷调）：**
```
Nostalgic 1990s photograph. <场景英文描述>. Faded film grain texture, cool gray-blue tones, muted, vignette, desaturated, like a photograph kept in a drawer for thirty years. The scene feels lonely and empty.
```

**克制/隐忍场景（柔暖）：**
```
Nostalgic 1990s photograph. <场景英文描述>. Soft muted light, faded film grain texture, vignette, muted warm tones, quiet atmosphere, like a photograph kept in a drawer for thirty years.
```

## 选场景规则

| 规则 | 说明 |
|------|------|
| 画面感优先 | 选有具体物件/动作/空间的段落，不选心理描写 |
| 情绪递进 | 场景之间有情绪变化：温暖→失去→余韵 |
| 一张一冷一热 | 至少有一张暖调+一张冷调，对比出情绪弧线 |
| 插图位置 | 紧接场景描写之后、情绪转折之前 |

## 色调对照表

| 情绪 | 英文关键词 | 示例 |
|------|-----------|------|
| 温暖回忆 | warm golden tones, faded yellowish | 阿婆添柴、母亲寄包裹 |
| 失去空荡 | cool gray-blue tones, muted, desaturated | 空灶台、没人的院子 |
| 克制隐忍 | soft muted light, muted warm tones | 父亲修门锁、木箱子 |
| 安静日常 | warm golden tones, quiet | 腊肉挂梁、翻盖手机亮屏 |

## 常见场景 Prompt 示例

**灶台/厨房类：**
- `A traditional Chinese rural kitchen interior with a large brick stove at center, warm firelight glowing from the stove opening, strips of cured meat hanging from a smoke-blackened wooden beam above`
- `A small elderly woman bending over to add pine branches to a traditional brick stove, one hand resting on the stove edge for support, firelight reflecting on her weathered face`
- `A cold brick stove with no fire, only gray ashes in the stove opening, the wooden beam above is empty`（冷调）

**父亲/修理类：**
- `Back view of a middle-aged man sitting on a small stool in a Chinese courtyard, hunched over fixing something with a wrench, a flip phone on a low table nearby with screen faintly glowing`
- `An old unpainted pine wood box sitting beside a bed, rough wood grain visible, mortise and tenon joints at the corners fitting tightly`

**包裹/寄送类：**
- `A cardboard package opened on a small apartment table, three layers of tape cut open, inside: two glass jars, a bag, a pair of thick socks, and at the bottom a small handwritten note`

- 封面不含品牌标识
- 不需要 ref-url（场景独立）

---

# 扩展风格目录

| # | 风格 | 英文ID | 适合场景 | 视觉关键词 |
|---|------|--------|---------|-----------|
| 3 | 怀旧照片风 | nostalgic-photo | 情感治愈、回忆、亲情、乡愁 | 90年代胶片、泛黄暗角、颗粒感、写实照片 |
| 4 | 学术蓝图风 | blueprint | 系统架构、工程设计、深度技术文 | 蓝色网格、技术蓝图、工程制图 |
| 4 | 手绘笔记风 | sketch-notes | 知识教程、读书笔记、概念解析 | 马卡龙色、手绘线条、奶白底、温暖涂鸦 |
| 5 | 复古文艺风 | vintage | 历史人文、怀旧散文、品牌故事 | 做旧羊皮纸、褐色调、古典装饰 |
| 6 | 可爱萌系风 | kawaii | 生活分享、萌宠、轻松日常 | 粉嫩色、圆滚滚、粗描边、贴纸感 |
| 7 | 赛博霓虹风 | cyberpunk-neon | 未来科技、游戏、AI科幻 | 深紫黑底、霓虹发光、故障艺术 |
| 8 | 极简商务风 | corporate | 行业分析、商业策略、投资人视角 | 克制配色、几何图形、高级质感 |
| 9 | 自然水彩风 | watercolor | 旅行、养生、自然、慢生活 | 水彩晕染、大地色系、有机笔触 |
| 10 | 像素游戏风 | pixel-art | 游戏文化、复古科技、极客趣味 | 8-bit像素、复古游戏机、色块马赛克 |
| 11 | 海报丝印风 | screen-print | 观点评论、文化分析、深度社论 | 大色块、半调网点、丝网印刷、强视觉冲击 |
| 12 | 禅意留白风 | zen-minimal | 哲学思辨、极简生活、禅意随笔 | 大面积留白、单色线描、呼吸感 |

各风格的详细 Prompt 模板见同目录下的 `style-templates.md`。

## 品牌标识规则

| 风格 | 品牌标识 |
|------|---------|
| 科技风 | 封面必须含品牌标识 |
| 柔情风 | 不含，保持画面纯净 |
| 怀旧照片风 | 不含，保持画面纯净 |
| 学术蓝图风 | 封面含，蓝色调 |
| 赛博霓虹风 | 封面含，霓虹风格 |
| 极简商务风 | 封面含，灰色调 |
| 像素游戏风 | 封面含，像素风格 |
| 其余风格 | 不含品牌标识 |

含品牌标识的封面提示词中须包含：
- 左上角：{brand.name} | {brand.website} | {brand.tagline}
- 左下角：{brand.website}
