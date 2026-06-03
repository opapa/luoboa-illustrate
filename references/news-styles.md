# 头条配图风格模板（Workflow N）

针对「每日AI快讯」类资讯合集文章，每条新闻生成 1 张 9:16 竖版**彩色铅笔速写**配图。
风格定位：**colored pencil drawing**（彩色铅笔 / 彩铅画），可见笔触、软蜡质感、多色叠加、暖系 macaron 配色，参考 baoyu `sketch-notes` 风格 + 儿童书插图感。

---

## 1. 通用 Prompt 结构（6 区布局）

每张图采用 **balanced 多区布局**（参考 baoyu-xhs-images 布局）：

```
[报头区 5%]       黑色横条 + 白字 "每日AI快讯 6月3日"
[分类 chip 6%]    左上角 macaron 色彩徽章 "【AI大模型】"
[标题区 12%]      大字手绘标题 "「xxx」"
[Bullet 区 18%]   奶油色块 + 3 个珊瑚红点 bullet
[插图区 50%]      墨水速写 + 淡彩水洗场景
[Footer 3%]       底部小字 "# 01 | 6月3日"
```

**通用 prompt 模板：**

```
9:16 vertical hand-drawn news card.
Top 5% is a black header bar with white text "每日AI快讯 {date}" (crystal clear, no garbling).
Below header on the left, a macaron {category_color_fill} category chip with Chinese text "【{category}】".
Title: 「{short_title}」 in dark gray, hand-lettered style with rough wobble.
Bullet block in cream (#F5F0E8) with 3 hand-drawn points in coral red dots:
  • {bullet_1}
  • {bullet_2}
  • {bullet_3}
Lower 50% scene: colored pencil illustration (彩色铅笔 画) with visible pencil strokes, soft waxy texture, multiple colors used, cream paper background, illustrating: {scene_en}. Visible colored pencil strokes in every shape, soft layering of pigments, slight grain texture, hand-drawn feel, no flat color fills.
Footer: "# {num:02d} | {date}".
Style: colored pencil drawing with visible strokes and soft layering, NOT digital art NOT watercolor wash NOT pure ink NOT oil painting, hand-drawn texture, warm friendly illustrative feel, like a childrens book editorial illustration in colored pencil. macaron palette cream background pastel chip coral red accent. Text rendered cleanly without garbled characters. NO flat color, NO vector, NO anime, NO photographic, NO digital gradients, NO smooth shading.
```

**关键参数：**
- `{date}` — 从文件名或首行解析的日期
- `{short_title}` — 智能精简后的标题，≤ 22 字
- `{bullets}` — 3 条关键事实（AI 从新闻原文提取，每条 ≤ 18 字）
- `{scene_en}` — 视觉化英文场景描述
- `{category}` — 4 个分类之一
- `{category_color_fill}` — 分类对应的 macaron 填充色

---

## 2. 4 个分类的 macaron 配色

| 分类 | 填充色 (#hex) | 墨色 (#hex) | 配色名 |
|------|--------------|-------------|--------|
| `AI大模型` | `#A8D8EA` 蓝 | `#4A90A4` | macaron blue |
| `AI Agent` | `#D5C6E0` 紫 | `#7B6B8C` | lavender |
| `AI工具` | `#B5E5CF` 绿 | `#5A9078` | mint |
| `AI行业动态` | `#F8D5C4` 桃 | `#B06850` | peach |

**全局通用色**（不变）：
- 背景 cream: `#F5F0E8`
- Bullet 强调色 coral red: `#E8655A`
- 标题深灰: `#1A1A1A`
- Footer 紫: `#D5C6E0`

---

## 3. 风格修饰词清单

### 主调：彩色铅笔
- `colored pencil drawing` / `colored pencil illustration` — 彩色铅笔
- `彩色铅笔 画` — 中文关键词（让即梦精确识别）
- `visible pencil strokes` — 可见笔触
- `soft waxy texture` — 软蜡质感
- `soft layering of pigments` — 颜料叠加
- `slight grain texture` — 颗粒感
- `no flat color fills` — 不要平涂
- `hand-drawn texture` — 手绘质感

### 风格定位
- `like a childrens book editorial illustration in colored pencil` — 童书编辑插图感
- `warm friendly illustrative feel` — 温暖友好
- `macaron palette` — 配色体系

### 排除（重要）
- `NOT digital art`
- `NOT watercolor wash`
- `NOT pure ink`
- `NOT oil painting`
- `NO flat color`
- `NO vector`
- `NO anime`
- `NO photographic`
- `NO digital gradients`
- `NO smooth shading`

### 文字渲染
- `crystal clear, no garbling` — 顶部报头
- `Text rendered cleanly without garbled characters` — 末尾防乱码

---

## 4. Bullet 提炼规则

AI 从每条新闻原文中提炼 **3 个关键事实**（`bullets` 字段）：

**规则：**
1. 每条 ≤ 18 字（一行能装下）
2. 保留：具体数字、专有名词、关键动作
3. 删除：修饰语、连接词、模糊表达
4. 3 条要有递进或并列关系，不能重复

**示例**（Anthropic IPO 原文："Anthropic已提交上市招股书，冲击AI行业最大规模IPO。同期教皇与Anthropic联合发布报告，警告2030年AGI可能降临"）：
```
• 已提交上市招股书
• 冲击AI行业最大规模IPO
• 教皇预警2030年AGI来临
```

---

## 5. 10 条新闻场景示例（基于 0603.md）

> 这 10 个场景是纪实速写的"主图"内容。完整的 6 区布局（报头+chip+标题+bullets+场景+footer）由 prompt 模板自动生成。

### 01. Anthropic 冲击最大 IPO
**精简标题：** Anthropic 冲史上最大 IPO
**分类：** AI大模型（macaron 蓝）
**Bullets：** 已提交上市招股书 / 冲击AI行业最大规模IPO / 教皇预警2030年AGI来临
**场景：** A classical Renaissance hall with marble columns, a giant unfurled S-1 prospectus scroll on a stone pedestal, stock ticker numbers carved into the architecture, AI chip motifs integrated into the column capitals

### 02. GPT-5.6 官宣
**精简标题：** GPT-5.6 今晚杀到
**分类：** AI大模型（macaron 蓝）
**Bullets：** OpenAI 即将发布 GPT-5.6 / 奥特曼亲自预告 / 基准测试刷新纪录
**场景：** An OpenAI keynote stage with an executive figure at the podium pointing to a massive glowing screen, audience silhouettes with raised phones, spotlight beams cutting through stage haze

### 03. Opus 4.8 破 AI 考试
**精简标题：** Opus 4.8 破 AI 最难考试
**分类：** AI大模型（macaron 蓝）
**Bullets：** 烧掉 1 万美元算力 / AI 最难基准测试夺冠 / 领先 GPT-5.5 近 4 倍
**场景：** A grand examination hall with empty wooden desks and one glowing terminal at the center, stacks of GPU cards burning like incense at the corner, a giant scoreboard on the wall showing 4x lead over competitors

### 04. 豆包收费 5088 元/年
**精简标题：** 豆包收费 5088 元/年
**分类：** AI大模型（macaron 蓝）
**Bullets：** 6 月下旬上线付费订阅 / 最高年费 5088 元 / 国产 AI 免费时代或终结
**场景：** A tech company office pantry with a giant price tag hanging from the ceiling showing 5088 yuan per year, employees walking past with coffee cups, a free-trial banner being torn down

### 05. ChatGPT + Codex 合体
**精简标题：** ChatGPT 联手 Codex
**分类：** AI Agent（lavender）
**Bullets：** ChatGPT 与编程工具 Codex 合体 / 10 亿用户获「超级 Agent」 / 编程/办公/创作全面自动化
**场景：** Two figures merging into one - a friendly chatbot avatar on the left and a glowing terminal window on the right clasping hands, surrounded by orbiting code symbols and productivity icons

### 06. 字节 AI 大将离职
**精简标题：** 字节 AI 大将离职
**分类：** AI Agent（lavender）
**Bullets：** 字节 AI 业务核心人物离职 / AI 行业人才战持续升温 / 大厂核心人员流动频繁
**场景：** A corporate office at dusk, silhouette of a person carrying a cardboard box of personal belongings walking toward the elevator, empty desk with a single wilted succulent plant

### 07. 微软量子芯片
**精简标题：** 微软量子芯片发布
**分类：** AI工具（mint）
**Bullets：** 微软发布新一代量子芯片 / 瞄准 AI 算力瓶颈 / 或重塑 AI 芯片竞争格局
**场景：** A scientist in a lab coat leaning over a glowing quantum chip suspended in a cryogenic chamber, control monitors showing waveforms, cables snaking across the laboratory floor

### 08. Tesla FSD 争议
**精简标题：** Tesla FSD 安全争议
**分类：** AI工具（mint）
**Bullets：** 前员工公开不信任 FSD / 坦言「给钱也不坐」 / Robotaxi 计划或受打击
**场景：** A driver gripping a steering wheel with knuckles white, eyes narrowed with distrust, autonomous driving interface glowing on the dashboard, road motion blur through the windshield

### 09. 微信 AI 战略
**精简标题：** 微信 AI 战略加码
**分类：** AI行业动态（peach）
**Bullets：** 腾讯 AI 战略全面加码 / 微信加速 AI 功能落地 / 巨头 AI 争夺战升级
**场景：** A modern corporate strategy meeting room with a large projection screen showing neural network patterns, executives seated around a polished table with laptops and coffee cups, strategic charts on the walls

### 10. 宇树 IPO + 人形机器人
**精简标题：** 宇树人形机器人 IPO
**分类：** AI行业动态（peach）
**Bullets：** 宇树科创板 IPO 过会 / 人形机器人首家上市公司 / 机器人+AI 投资主题火热
**场景：** A humanoid robot standing at a stock exchange podium, one mechanical hand raised in an IPO bell-ringing gesture, factory assembly line of smaller robots marching in the background

---

## 6. 文字渲染注意事项

### 6 个文字区
1. **顶部报头**：「"每日AI快讯 6月3日"」+ `crystal clear, no garbling`
2. **分类 chip**：「"【AI大模型】"」+ macaron 填色
3. **大标题**：「{short_title}」+ 暗灰手写 display 字体
4. **3 个 Bullets**：「• 已提交...」+ 珊瑚红圆点
5. **场景描述**：英文，仅在 prompt 引导模型，不直接渲染
6. **Footer**：「"# 01 | 6月3日"」+ 紫色小字

### 防乱码关键词
末尾必须加 `Text rendered cleanly without garbled characters`

### 字号策略
- 报头：固定 5% 画面高度
- 标题：占 12%，字号最大
- Bullets：占 18%，每条 4-6% 高度
- 插图：占 50% 主体
- Footer：占 3% 小字

---

## 7. 文字乱码重试策略

如果生成的图片文字乱码，按以下顺序调整重试：

1. **第一次重试**：强化字体描述
   - 添加 `EXTRABOLD` 到标题描述
   - 改为 `extra large bold handwritten`

2. **第二次重试**：简化文字位置
   - 把"top 5%"改为"top of the image"
   - 去掉 chip 颜色描述对文字的影响

3. **第三次重试**：拆分长文字
   - 标题超过 15 字拆 2 行
   - Bullet 超过 20 字截断

---

## 8. 内容审核风险词

实测发现以下关键词会触发即梦 `gen_status: fail`（final generation failed）：

| 类别 | 触发词 | 替代方案 |
|------|--------|---------|
| 模板陷阱 | `the remaining` （实测会触发 fail） | 用 `Lower 50%` 或 `Main scene below` |
| 模板陷阱 | `Top X% of the canvas` 重复使用 | 改用更口语化的位置描述 |
| 宗教人物 | `pope`, `papal`, `Vatican`, `priest`, `bishop` | 用 `classical figure`, `silhouette in robes` |
| 政治敏感 | `Trump`, `Biden`, `习近平`, `Putin` | 用 `political leader silhouette`, `dignitary` |
| 暴力血腥 | `blood`, `gun`, `shooting`, `war` | 用 `intense scene`, `dramatic confrontation` |
| 公司名/CEO | `OpenAI`, `奥特曼`, `Sam Altman`, `马斯克`, `Elon Musk` | 用 `founder` / `创始人` / `CEO silhouette` |
| 真实人物 | 知名在世 CEO 可能触发 | 用 `executive silhouette`, `founder figure` |

**应对策略：**
1. 模板用 `Lower 50%` 替代 `The remaining 70%`（**已修复**）
2. 模板用简短位置描述，避免 `Top X% of the canvas` 重复
3. scene_en 避免上述风险词
4. 失败时脚本自动重试一次（强化风格关键词）
5. 重试仍失败则该条标记 ❌，跳过继续

---

## 9. 一致性维护规则

**重要约束：** `dreamina text2image` 不支持 `--ref-url`。10 张图的画风一致性**完全靠 prompt 关键词约束**。

### 强约束手段

1. **固定风格块**：每个 prompt 末尾必须包含风格描述段
2. **5 维参数同步**：所有 prompt 共享 5 维默认值：
   - Type: `infographic-sketch`（教育信息图速写）
   - Palette: `macaron`（暖米 + 4 色 chip + 珊瑚红强调）
   - Rendering: `hand-drawn-ink + watercolor-wash`（手绘墨水 + 淡彩）
   - Font: `handwritten`（手写字体）
   - Mood: `balanced`（平衡戏剧性与可读性）
3. **关键词冗余**：相同的风格关键词在 prompt 中出现 2-3 次

### 一致性预期
- ✅ 色调：100% 一致（macaron 配色）
- ✅ 渲染方式：90% 一致（手绘墨水 + 淡彩）
- ⚠️ 笔触粗细：约 80% 一致
- ⚠️ 场景人物比例：约 70% 一致
