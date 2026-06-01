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
| 3 | 📷 怀旧照片风 | 90年代写实胶片质感 + 泛黄暗角颗粒感 |
| 4 | 🎨 更多风格... | 查看10种扩展风格 |
| 5 | ⚡ 快文配图 | 按句生成9:16竖图，即梦渲染文字，视频素材 |

If user picks 1 → Workflow A (科技类)
If user picks 2 → Workflow B (情感治愈类)
If user picks 3 → Workflow E (怀旧照片类)
If user picks 4 → show extended catalog from `references/style-guide.md`
If user picks 5 → Workflow D (快文配图)

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

## Workflow A: 科技类

- Cover: dark-background hand-drawn diagram style (Excalidraw dark mode) with brand logo (if enabled). Prompt template in `references/style-guide.md`.
- Sections: Excalidraw hand-drawn sketch style. Prompt template in `references/style-guide.md`.

## Workflow B: 情感治愈类

- Ask user for cover sub-style (A/B/C/D). Default to B.
- Cover: emotional photography or illustration style, NO brand logo even if enabled.
- Sections: warm healing style with Morandi colors.
- **Critical**: from 2nd section onward, pass previous generation's URL as `--ref-url` to maintain character consistency.
- **Critical**: send full novel/story text, not summaries.

## Workflow E: 怀旧照片类

适合情感治愈、回忆、亲情、乡愁类文章。90年代写实照片风格，胶片颗粒感，泛黄暗角，像压在抽屉底三十年的老照片。

### 核心原则

1. **场景驱动** — 根据文章关键场景（不是标题）设计画面，2-3张场景插图 + 1张封面
2. **英文 Prompt** — grsai 等国内 API 中文 prompt 易触发内容审核，统一使用英文
3. **无品牌标识** — 保持画面纯净，不加任何品牌水印
4. **不需要 ref-url** — 场景为主，非人物连续性，每张图独立生成
5. **冷热对比** — 温暖场景用暖黄暗角，失去/空荡场景切冷灰色调，用色调传达情绪

### 封面

- 尺寸：1920x832
- 无人物或背影/侧影为主，留想象空间
- **艺术大字排版设计**：文章标题是画面的视觉主角，占据中心50-70%区域，通过艺术手法与照片交融。**不是宋体小字，是Banner级大字**
- 用户从12种文字排版风格（A-L）中选择，默认推荐 G（王家卫式字幕）
- 12种风格：A日系电影感 / B复古杂志风 / C自然呼吸感 / D信笺与手写 / E光影重叠 / F极简新中式 / G王家卫式 / H拍立得底栏 / I唱片封面风 / J旧报纸头条 / K诗歌散排 / L古书扉页
- Prompt 模板见 `references/style-guide.md` 中"12种封面文字排版风格"章节

### 场景插图（无 `##` 小标题的文章）

情感文通常不加 `##` 小标题，需要 AI 阅读全文后选择 2-3 个关键场景生成插图。

**选场景规则：**
- 选画面感最强的段落，不选心理描写/议论段落
- 场景之间有情绪递进：温暖→失去→空荡，或日常→转折→余韵
- 插图插入位置：紧接场景描写之后、情绪转折之前

**插图尺寸：** 1024x1024

### Prompt 模板

封面和插图模板见 `references/style-guide.md`。

**色调指南：**

| 情绪 | 色调关键词 |
|------|-----------|
| 温暖/回忆/日常 | warm golden tones, faded yellowish film grain, vignette |
| 失去/冷清/空荡 | cool gray-blue tones, muted, vignette, desaturated |
| 克制/隐忍 | soft light, muted warm tones, quiet |

### 插入文章

封面不插入 md。场景插图插入对应场景描写之后，用 `![](images/<filename>.png)` 格式。

## Workflow C: 通用风格

When user picks from extended catalog, use corresponding prompt templates from `references/style-templates.md`.

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
- ✅ Tech, Blueprint, Cyberpunk, Corporate, Pixel Art
- ❌ Emotional, Nostalgic Photo, Sketch Notes, Vintage, Kawaii, Watercolor, Screen Print, Zen Minimal

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
