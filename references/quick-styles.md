# 快文配图风格模板（Workflow D）

每句生成一张 **8-bit 像素海报**，参考**极客公园 萝卜啊** 的复古游戏机像素海报风格——**纯黑白 + 橙色关键词高亮 + 半色调网点阴影 + 复古游戏 UI 底栏**。每张图对应文章的一句话，每张图都是一个独立的"标题 + 8-bit 角色 + 复古 UI"组合。

**风格定位关键词：** Game Boy / NES 像素美学 + 1-bit 单色 + halftone 点阵阴影 + 锐利像素边缘（不要抗锯齿）+ 复古游戏机 UI（萝卜啊 logo + 计时器 + 弹"弹"字）。

## 通用 Prompt 结构

```
8-bit pixel art illustration in retro game console aesthetic (Game Boy / NES era).
LAYOUT (top to bottom):
1. TOP 35% — bold chunky 8-bit Chinese title rendering the sentence verbatim.
   KEYWORD(s) in bright orange #FF6B35 (default) or red #E8453C (alt).
   Other text in pure black #1A1A1A.
2. MIDDLE 50% — pixel-art 8-bit subject (角色/物件/场景), with sharp black
   outlines + halftone dot pattern for shading.
3. BOTTOM 15% — minimal UI bar: 萝卜啊-style logo on left
   (in orange #FF6B35), and a chunky 8-bit progress label in middle
   showing the current image number out of total, e.g. "1/2" or "3/12",
   in bright orange #FF6B35 pixel font.

Pure 1-bit monochrome (black on white) + 1-2 spot colors only.
Halftone dot pattern for shading. Sharp 1-px pixel edges (NOT anti-aliased).
Blocky chunky 8-bit sprite characters. No curves, only right angles and
stepped diagonals. Chunky 8-bit typography for any text.

NOT photorealistic, NOT 3D, NOT anime, NOT watercolor, NOT sketch,
NOT hand-drawn brush strokes, NOT smooth gradients, NOT vector art.

Subject: <句子核心意象 — 一个 8-bit 像素角色/物件 in 场景>.
关键词高亮: <关键词 1-2 个，会被染成橙/红色>.
```

**关键规则：**
- **每张图必须渲染中文标题**（关键词橙色高亮是核心特色，不是装饰）
- 每张图必须有 **主体角色/物件 + 复古 UI 底栏**——不能只画大字
- 颜色严格控制：**纯黑 + 纯白 + 1-2 个高亮色（默认黄 #FF6B35）**，不要让模型自由加第 3 种颜色
- 文字必须能被中文像素字渲染，dreamina v50 对中文支持较稳
- 模型用 `high_aes_general_v50`（**不用 4.7**——4.7 偏 Q 版马克笔，跟像素艺术冲突）

---

## 1. 🎮 8-bit 极客黑白 (8bit-geek-bw) — **DEFAULT**

**风格关键词：** 1-bit 单色、纯黑白 + 橙色高亮、半色调网点阴影、GameBoy sprite、关键词黄色像素字

**色板：**
- 纯黑 `#1A1A1A`（线条 + 主体）
- 纯白 `#FFFFFF`（底色 + 留白）
- 黄色 `#FF6B35`（关键词高亮，默认唯一高亮色）
- 半色调网点灰 `#CCCCCC`（阴影过渡）

**核心要素（每张图必含）：**
1. **顶部 35%**：粗黑体 8-bit 中文标题，**关键词用纯橙像素字**，其他字纯黑
2. **中部 50%**：1 个 8-bit 像素角色或物件，黑色硬轮廓 + 半色调网点阴影
3. **底部 15%**：复古游戏 UI 底栏 ——
   - 左：`萝卜啊` logo（黑底白字或纯白底黑字）
   - 中：进度标签 `1/N` 格式（橙色 #FF6B35）
   - 右：（无）
   - 角落小字 "弹" 装饰

**Prompt 模板：**
```
8-bit pixel art illustration in retro Game Boy aesthetic.
Pure 1-bit monochrome (black on white) with bright orange #FF6B35 as the
single spot color for keyword highlighting.

LAYOUT (top to bottom):
1. TOP 35% — bold chunky 8-bit Chinese title "<完整句子>" rendered in 
   sharp pixel font. KEYWORDS highlighted in bright orange #FF6B35:
   "<关键词 1>"/"<关键词 2>". Other text in pure black.
2. MIDDLE 50% — pixel-art 8-bit sprite of <角色/物件> doing <动作>,
   in sharp black outlines with halftone dot pattern for shading.
3. BOTTOM 15% — minimal UI bar: 萝卜啊 logo on left,
   progress label in middle (e.g. "1/2"), in orange.

Pure 1-bit monochrome + single spot color orange only. Halftone dot
pattern. Sharp 1-px pixel edges (NOT anti-aliased). Blocky 8-bit
sprite characters. No curves, only right angles and stepped diagonals.
Chunky 8-bit pixel typography.

NOT photorealistic, NOT 3D, NOT anime, NOT watercolor, NOT sketch,
NOT hand-drawn brush strokes, NOT smooth gradients, NOT vector art.
```

**适合：** 科技/职场/观点类快文 — 任何需要"硬核感 + 关键词突出 + 复古游戏机氛围"的内容（最像 萝卜啊 原版）

---

## 2. 🤖 机器人像素彩 (robot-pixel-color)

**风格关键词：** 黑白 + 红色高亮、硬核科技、机械感

**色板：**
- 纯黑 `#1A1A1A`
- 纯白 `#FFFFFF`
- 红色 `#E8453C`（高亮色 — 关键词/危险/数据）
- 半色调灰 `#BBBBBB`

**核心要素：**
- 主体偏机械感/电路/机器人
- 关键词用红色（"危险""警告""卡住""失败"等负面词特别合适）
- 整体比风格 1 更"硬"

**Prompt 模板：**
```
8-bit pixel art illustration in retro game console aesthetic.
Pure 1-bit monochrome (black on white) with bright red #E8453C as the
single spot color for warning / data / negative keyword highlighting.

LAYOUT (top to bottom):
1. TOP 35% — bold chunky 8-bit Chinese title "<完整句子>". 
   KEYWORDS highlighted in bright red #E8453C: "<关键词>".
2. MIDDLE 50% — pixel-art 8-bit 机械感 sprite (robot / circuit / 
   machine / tool), sharp black outlines + halftone dot shading.
3. BOTTOM 15% — retro game UI bar: same as 风格1 (萝卜啊 + progress label).

Pure 1-bit monochrome + single spot color red only.
```

**适合：** 警示类、AI 翻车类、技术故障类快文

---

## 3. 💚 GameBoy 绿屏 (gameboy-green)

**风格关键词：** 4 级绿阶 + 黄色高亮、极致 80s 复古、原版 GameBoy 屏幕

**色板：**
- 最深绿 `#0F380F`
- 深绿 `#306230`
- 浅绿 `#8BAC0F`
- 最浅绿 `#9BBC0F`（屏幕背景）
- 黄色 `#FF6B35`（高亮 — 在绿色屏幕上读最舒服的对比色）

**核心要素：**
- 整体限定在 4 级绿阶（不要中间色，**硬像素块**）
- 黄色在绿色屏幕上特别醒目（仿 GameBoy 实际配色）
- 营造"在看旧 GameBoy"的怀旧感

**Prompt 模板：**
```
8-bit pixel art illustration rendered as if displayed on an original 
Nintendo Game Boy LCD screen. STRICT 4-tone green palette only:
darkest green #0F380F, dark green #306230, light green #8BAC0F,
lightest green #9BBC0F (background). Yellow #FF6B35 is the single
spot color for keyword highlighting (yellow is highly readable on
green LCD).

LAYOUT (top to bottom):
1. TOP 35% — bold chunky 8-bit Chinese title "<完整句子>" in 
   darkest green #0F380F on lightest green #9BBC0F background.
   KEYWORDS in bright orange #FF6B35.
2. MIDDLE 50% — pixel-art 8-bit sprite of <角色/物件>, rendered in 
   4-tone green only with strict 1-px pixel boundaries.
3. BOTTOM 15% — retro game UI bar in green palette with yellow
   energy indicators.

STRICT 4-tone green palette. No greyscale, no anti-aliasing, no
smooth gradients. Halftone dithering for shading (the classic Game Boy
"checkerboard" pattern).
```

**适合：** 怀旧主题、游戏/电竞向、童年回忆、复古数码风快文

---

## 4. 📺 16-bit 街机 (16bit-arcade)

**风格关键词：** 像素密度更高（像 SNES/世嘉 MD 时代）、色彩更丰富、但仍纯像素

**色板：**
- 16-bit 时代典型调色板（最多 4-5 种主色 + 半色调阴影）
- 默认：纯黑 + 纯白 + 黄 + 蓝 + 灰 5 种
- 关键词高亮用红 `#E8453C`

**核心要素：**
- 比 8-bit 更细腻（角色细节更多）
- 但仍是纯像素（不是 32-bit 拟真）
- 适合复杂场景（多人物/多物件）

**Prompt 模板：**
```
16-bit pixel art illustration in retro SNES / Sega Genesis console aesthetic.
Limited palette of 4-5 main colors: black #1A1A1A, white #FFFFFF, 
orange #FF6B35, blue #4A7BC8, gray #888888. Halftone dot pattern for
shading. Sharp 2-px pixel edges (less chunky than 8-bit).
Bright red #E8453C as spot color for keyword highlighting.

LAYOUT (top to bottom):
1. TOP 35% — bold chunky 16-bit Chinese title.
2. MIDDLE 50% — more detailed 16-bit sprite scene (up to 2-3 characters).
3. BOTTOM 15% — retro arcade UI bar with score counter.
```

**适合：** 复杂场景、多人物互动的快文

---

## 5. 🎰 街机红黄 (arcade-red-yellow)

**风格关键词：** 黑白 + 红 + 黄双高亮、复古街机 UI（Pac-Man / Galaga 风）

**色板：**
- 纯黑 `#1A1A1A`
- 纯白 `#FFFFFF`
- 红色 `#E8453C`（高亮 1 — 重要名词/数字）
- 黄色 `#FF6B35`（高亮 2 — 行动/状态）

**核心要素：**
- 双高亮色，关键词可分两类（"重要名词"用红，"动作"用黄）
- 复古街机风格比 萝卜啊 更"游戏化"（pac-man 风格 UI）

**Prompt 模板：**
```
8-bit pixel art illustration in retro arcade (Pac-Man / Galaga) aesthetic.
Pure 1-bit monochrome + TWO spot colors: red #E8453C (for important
nouns/numbers) and orange #FF6B35 (for actions/states). Halftone dot
shading. Sharp 1-px pixel edges.

LAYOUT (top to bottom):
1. TOP 35% — bold chunky 8-bit Chinese title.
   Important NOUNS in red #E8453C, ACTION VERBS in orange #FF6B35,
   other text in black.
2. MIDDLE 50% — pixel-art 8-bit sprite in classic arcade style.
3. BOTTOM 15% — arcade UI bar: SCORE counter, lives indicator 
   (3 ship icons), level number.
```

**适合：** 行动/事件向快文（多个关键概念需要用不同颜色区分）

---

## 6. 💾 磁带/磁盘像素 (tape-disk-pixel)

**风格关键词：** 8-bit 灰阶 + 黄色高亮、80s 科技风、Apple II 时代

**色板：**
- 5 级灰阶 `#0A0A0A` `#3A3A3A` `#6A6A6A` `#9A9A9A` `#CACACA`
- 黄色 `#FF6B35`（高亮 — 跟旧 CRT 显示器配色一致）

**核心要素：**
- 纯灰阶（黑白之间 5 个灰阶）
- 像早期 Mac/Apple II 屏幕
- 适合科技史/复古计算/老硬件主题

**Prompt 模板：**
```
8-bit pixel art illustration in retro 1980s computer aesthetic
(Apple II / early Mac / Commodore 64). 5-tone grayscale palette only:
black, dark gray, mid gray, light gray, off-white. Yellow #FF6B35
as the single spot color for keyword highlighting (matches the
amber/yellow phosphor of old CRT monitors).

LAYOUT (top to bottom):
1. TOP 35% — bold chunky 8-bit Chinese title in black/dark gray.
   KEYWORDS in bright orange #FF6B35.
2. MIDDLE 50% — pixel-art 8-bit sprite of <角色/物件>, in
   grayscale with halftone dot shading.
3. BOTTOM 15% — retro computer UI bar: floppy disk icon, 
   "C:>" prompt, blinking cursor.
```

**适合：** 科技史、复古计算、程序员怀旧主题

---

## ⚠️ 最关键的硬规则

**每张图必须包含：**
1. **顶部 35%**：粗黑体 8-bit 中文标题（**关键词橙色高亮**——这是 萝卜啊 风格的核心标志）
2. **中部 50%**：1 个 8-bit 像素角色/物件，黑色硬轮廓 + 半色调网点阴影
3. **底部 15%**：极简 UI 底栏（萝卜啊 logo 左 + 1/N 进度标签中）

**反例（不要的）：**
- ❌ 写实摄影 / 水彩 / 3D 渲染
- ❌ 抗锯齿平滑矢量
- ❌ 彩色渐变（颜色必须用 1-2 种 spot color + 半色调网点）
- ❌ 没有 8-bit 像素角色（只剩大字文字）
- ❌ 没有复古游戏 UI 底栏
- ❌ 颜色超过 3 种（默认纯黑 + 纯白 + 黄）
- ❌ 中文不渲染（dreamina v50 对中文支持稳，必须渲染）

**模型：** `high_aes_general_v50`（**不用 4.7**——4.7 偏 Q 版马克笔，跟像素艺术冲突，v50 才是像素友好）
