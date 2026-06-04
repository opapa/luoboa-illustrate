# 微头条配图风格模板（Workflow N）

针对「每日AI快讯」类资讯合集文章，每条新闻生成 1 张 9:16 竖版配图。

风格定位：**🖍️ 马克笔 Q 版卡通**（marker-q-chibi）—— 二头身大头小身体 + 夸张表情 + 汗珠等情绪符号 + 黑色手绘马克笔/平板笔刷线条 + 低饱和度色块平涂 + 大量手写体文字 + 颜色高亮 + 手绘小图标散落。

**后端：用户选（API / CLI）**（用 `scripts/generate.py section --aspect-ratio 1024x1792` 或 `dreamina text2image`，见 Step 1.5）。

**默认提示词语言：中文。** scene_zh 字段是中文场景描述（grsai/dreamina 都支持中文 prompt）。

---

## ⚠️ Dreamina 风控触发词（2026-06-04 摸出来的坑）

**「每日AI快讯」+ 具体日期** 这两个串同时出现在 prompt 里，dreamina 5.0 一定 `final generation failed` 拒图。摸边界结论：

| Prompt 含 | 结果 |
|---|---|
| `腾讯云`、`DeepSeek-V4`、`大降价` | ✅ 不触发 |
| `75%`、`97.5%`、`几分钱` | ✅ 不触发 |
| `AI大模型` 这种 chip 词 | ✅ 不触发 |
| 多个独立中文文字区域（chip + 标题 + 3 bullets） | ✅ 不触发 |
| **`每日AI快讯 6月4日`**（"每日AI快讯" + 日期组合） | ❌ 必拒 |

**解法**：scripts/news_generate.py 的 `PROMPT_TEMPLATE` 不写这一行；出图后调 `overlay_timestamp(img_path, date)` 用 PIL 把"每日AI快讯 X月X日"小灰字叠在顶部右侧（位置仿 API 原版）。

API（grsai/gpt-image-2）则没这个限制——同一段 prompt 写"每日AI快讯 6月4日"能正常出。所以这条规则只针对 dreamina CLI 路径。

---

## 1. 通用 Prompt 结构（**默认中文 prompt**）

```
9:16 竖版手绘新闻卡，Q版二头身卡通人物 (big head small body, chibi style)。

主体：<具体人物>在<具体场景>，表情<夸张表情>，头上/周围有<汗珠/感叹号/星星/问号 等情绪符号>。

风格：黑色手绘马克笔/平板笔刷线条，低饱和度水彩或马克笔平涂上色，块状色感。NOT photorealistic, NOT polished, NOT refined, NOT digital gradient, NOT 3D, NOT anime。

背景：奶油色 (#F5E6D3) 背景，暖色调马卡龙色板。手绘小图标（灯泡💡、问号❓、月亮🌙、爱心❤️、大脑🧠、齿轮⚙️、警告⚠️）散落在画面周围，与主文字/人物不重叠。

中文文字占画面左半边或右半边，巨型粗体手写体风格，清晰锐利，不乱码。重点词用不同颜色高亮：
- 技术名词（如 "AI"、"MoE"、"transformer"）→ 紫色 #8B5CF6
- 情绪/难懂词（如 "不懂"、"难"、"卡住"）→ 橙色 #F97316
- 数字/关键数据 → 红色 #EF4444
- 否定/转折词（如 "但是"、"不是"、"没有"）→ 蓝色 #3B82F6

⚠️ CLI（dreamina）路径：**不要在 prompt 里写 "每日AI快讯 {date}"**——会触发风控拒图。
用 scripts/news_generate.py 的 overlay_timestamp() 出图后 PIL 叠。
API（grsai）路径：可以直接写进 prompt，没限制。

左上角分类 chip：{category_color_fill} 填充色 + Chinese text "【{category}】"。
标题（大字）：「{short_title}」
Bullet 区（3 个珊瑚红点）：
  • {bullet_1}
  • {bullet_2}
  • {bullet_3}
Footer：底部小字 "# {num:02d} | {date}"

每个中文字必须完整且可读，不乱码、不缺字、不多字。文字要保留草图手写感，不是宋体或印刷体。
```

---

## 2. 4 个分类的 macaron 配色（保留）

| 分类         | 填充色 (#hex) | 墨色 (#hex) | 配色名       |
| ------------ | ------------- | ----------- | ------------ |
| `AI大模型`   | `#A8D8EA` 蓝  | `#4A90A4`   | macaron blue |
| `AI Agent`   | `#D5C6E0` 紫  | `#7B6B8C`   | lavender     |
| `AI工具`     | `#B5E5CF` 绿  | `#5A9078`   | mint         |
| `AI行业动态` | `#F8D5C4` 桃  | `#B06850`   | peach        |

**全局通用色**（不变）：

- 背景 cream: `#F5F0E8`
- 标题深灰: `#1A1A1A`

---

## 3. 命令模板

```bash
# 单条新闻 9:16 竖版
# 默认 grsai API
python scripts/generate.py section \
  --prompt="<中文 Q版马克笔 prompt>" \
  --output "news/<MMDD>/<ArticleName>/<NN>.png" \
  --aspect-ratio 1024x1792

# 或 Dreamina CLI
dreamina text2image \
  --prompt="<中文 Q版马克笔 prompt>" \
  --ratio=9:16 \
  --model_version=4.7 \
  --resolution_type=2k \
  --poll=60
```

**注意**：

- grsai API 接受 `aspectRatio` 参数：1024x1024（1:1）/ 1024x1792（9:16）/ 1792x1024（16:9） 等
- 调用方式：`python scripts/generate.py section --prompt "..." --output "..." --aspect-ratio 1024x1792`
- grsai API 对中文文字渲染偶发乱码（4 次跑 1 次成功），如乱码可改用 dreamina
- 每张图必须有人物+场景+1-3 个情绪符号
- 重点词必须按颜色高亮规则使用

---

## 4. 与快文配图（Workflow D）的差异

| 维度 | Workflow D（快文）      | Workflow N（微头条）            |
| ---- | ----------------------- | ------------------------------- |
| 后端 | Dreamina CLI（4.7）     | **用户选（API / CLI）**         |
| 模型 | 4.7                     | gpt-image-2（API）/ 4.7（CLI）  |
| 比例 | 用户选（16:9/9:16/1:1） | **9:16** 固定                   |
| 场景 | 文章每句配 1 张         | 每条新闻配 1 张                 |
| 风格 | 马克笔 Q 版             | **马克笔 Q 版**（同快文，统一） |
| 文字 | 巨型手写体              | 巨型手写体（+ 颜色高亮）        |
