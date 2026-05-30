---
name: luoboa-illustrate
description: Generate illustrations for WeChat public account articles (公众号配图) using image generation APIs or Dreamina CLI, then insert them into the article markdown file. Use this skill whenever the user wants to create illustrations, images, or cover art for their articles, or mentions 配图/插图/封面 for articles. Also trigger when the user asks to "给文章配图", "生成插图", "做封面".
---

# WeChat Article Illustrator

This skill generates illustrations for WeChat public account articles. It creates one illustration per section heading (`# ` and `## ` levels), not just a cover.

---

## ⚙️ First-Time Setup (Required)

**Before any image generation**, check if the config file exists:

```
~/.claude/skills/luoboa-illustrate/config.json
```

If the file **does not exist** → run the Setup Wizard below.
If the file **exists** → load config and skip to Style Selection.

### Setup Wizard

**Step 1: Auto-detect Dreamina CLI**

Run:
```bash
dreamina --version 2>/dev/null || echo "NOT_FOUND"
```

- If `NOT_FOUND` → Dreamina CLI not available
- If version string returned → Dreamina CLI is installed

**Step 2: Ask the user**

Based on detection result, ask:

> 🎨 首次使用，需要配置出图方式：
>
> | # | 方式 | 说明 |
> |---|------|------|
> | 1 | 🌐 API 出图 | 支持 OpenAI / GRS AI / 兼容接口 / 本地服务 |
> | 2 | 🎬 即梦 CLI | 本地安装的即梦命令行工具{detected_status} |
>
> 选哪种？（输入编号）

Where `{detected_status}` is:
- `"✅ 已检测到"` if Dreamina was found
- `"（未检测到，需自行安装）"` if not found

**Step 3a: If user picks "API 出图"**

> 请选择 API 服务商：
>
> | # | 服务商 | 说明 | Base URL 示例 |
> |---|--------|------|--------------|
> | 1 | GRS AI | 国内 GPT-image-2 节点 | `https://grsai.dakka.com.cn` |
> | 2 | OpenAI | 官方 OpenAI API | `https://api.openai.com` |
> | 3 | 兼容接口 | OpenAI 兼容的第三方/代理 | 用户自定义 |
> | 4 | 本地服务 | 本地部署的图像生成服务 | `http://localhost:8000` |
>
> 选哪个？（输入编号）

Then ask:
- **"请输入 API Key："** → (user inputs their key, e.g. `sk-xxxx`)
- **"请输入 Base URL："** → (auto-fill based on selection, allow user to modify)
- **"使用的模型名称："** → (default: `gpt-image-2`, allow user to change)

**Step 3b: If user picks "即梦 CLI"**

If Dreamina was not detected:
- **"⚠️ 未检测到即梦 CLI，请先安装后再使用此方式。是否改用 API 出图？"**
- If yes → go to Step 3a
- If no → stop, tell user to install Dreamina

If Dreamina was detected:
- Confirm and continue (no further config needed for Dreamina)

**Step 4: Brand configuration (optional)**

> 🏷️ 是否配置品牌标识？（会显示在部分风格的封面上）
>
> | # | 选项 |
> |---|------|
> | 1 | 不需要品牌标识 |
> | 2 | 配置我的品牌 |
>
> 选哪个？

If "配置我的品牌":
- **"品牌名称："** → e.g. `萝卜啊`
- **"品牌标语："** → e.g. `AI落地实践者`
- **"品牌 Logo URL（可选）："** → e.g. `https://www.luoboa.com/image/luoboa.png`
- **"品牌网址："** → e.g. `luoboa.com`

**Step 5: Save config**

Write the config to `~/.claude/skills/luoboa-illustrate/config.json`:

```json
{
  "backend": "api",
  "api": {
    "provider": "grsai",
    "base_url": "https://grsai.dakka.com.cn",
    "api_key": "sk-xxxx",
    "model": "gpt-image-2"
  },
  "brand": {
    "enabled": true,
    "name": "萝卜啊",
    "tagline": "AI落地实践者",
    "logo_url": "https://www.luoboa.com/image/luoboa.png",
    "website": "luoboa.com"
  }
}
```

For Dreamina backend:
```json
{
  "backend": "dreamina",
  "brand": {
    "enabled": false
  }
}
```

Provider values: `"grsai"`, `"openai"`, `"openai-compatible"`, `"local"`

**After saving → "✅ 配置已保存！开始使用吧。"** → proceed to Style Selection.

### Re-configure

If the user wants to change config later (e.g. "重新配置", "换key", "切换出图方式"):
- Delete the config file and re-run the Setup Wizard
- Or edit the config file directly

---

## Config Reference

The config file `~/.claude/skills/luoboa-illustrate/config.json` controls all API behavior:

| Field | Type | Description |
|-------|------|-------------|
| `backend` | `"api"` \| `"dreamina"` | Image generation backend |
| `api.provider` | string | `"grsai"` / `"openai"` / `"openai-compatible"` / `"local"` |
| `api.base_url` | string | API base URL (no trailing slash) |
| `api.api_key` | string | API key for authentication |
| `api.model` | string | Model name for image generation |
| `brand.enabled` | boolean | Whether to show brand on covers |
| `brand.name` | string | Brand display name |
| `brand.tagline` | string | Brand tagline / slogan |
| `brand.logo_url` | string\|null | Brand logo image URL (optional) |
| `brand.website` | string | Brand website URL |

---

## Style Selection

Before generating, **ask the user what style to use**. Show the primary choices first:

**"这篇文章选什么风格？"**

| # | 风格 | 一句话描述 |
|---|------|-----------|
| 1 | 🖥️ 科技风 | 暗黑对立构图 + Excalidraw手绘草稿 |
| 2 | 💕 柔情风 | 温暖治愈莫兰迪 + 人物一致性 |
| 3 | 🎨 更多风格... | 查看10种扩展风格 |

If the user picks **1** → use Workflow A (科技类)
If the user picks **2** → use Workflow B (情感治愈类)
If the user picks **3** or says "更多" → show the extended style catalog below

### Extended Style Catalog

**"以下是10种扩展风格，选一个（输入编号或名称）："**

| # | 风格 | 英文ID | 适合场景 | 视觉关键词 |
|---|------|--------|---------|-----------|
| 3 | 📐 学术蓝图风 | `blueprint` | 系统架构、工程设计、深度技术文 | 蓝色网格、技术蓝图、工程制图 |
| 4 | ✏️ 手绘笔记风 | `sketch-notes` | 知识教程、读书笔记、概念解析 | 马卡龙色、手绘线条、奶白底、温暖涂鸦 |
| 5 | 📜 复古文艺风 | `vintage` | 历史人文、怀旧散文、品牌故事 | 做旧羊皮纸、褐色调、古典装饰 |
| 6 | 🌸 可爱萌系风 | `kawaii` | 生活分享、萌宠、轻松日常 | 粉嫩色、圆滚滚、粗描边、贴纸感 |
| 7 | 🌆 赛博霓虹风 | `cyberpunk-neon` | 未来科技、游戏、AI科幻 | 深紫黑底、霓虹发光、故障艺术 |
| 8 | 💼 极简商务风 | `corporate` | 行业分析、商业策略、投资人视角 | 克制配色、几何图形、高级质感 |
| 9 | 🍃 自然水彩风 | `watercolor` | 旅行、养生、自然、慢生活 | 水彩晕染、大地色系、有机笔触 |
| 10 | 🕹️ 像素游戏风 | `pixel-art` | 游戏文化、复古科技、极客趣味 | 8-bit像素、复古游戏机、色块马赛克 |
| 11 | 🎭 海报丝印风 | `screen-print` | 观点评论、文化分析、深度社论 | 大色块、半调网点、丝网印刷、强视觉冲击 |
| 12 | 🧘 禅意留白风 | `zen-minimal` | 哲学思辨、极简生活、禅意随笔 | 大面积留白、单色线描、呼吸感 |

After user selects a style → use **Workflow C** (通用风格)

---

## Image Generation Backends

The backend is determined by the config file. Do NOT ask the user to choose each time — use whatever is configured.

| Backend | When | Notes |
|---------|------|-------|
| **API** (`api`) | `config.backend == "api"` | Supports GRS AI / OpenAI / compatible / local |
| **Dreamina** (`dreamina`) | `config.backend == "dreamina"` | Local CLI, requires login |

---

## API Call Templates

All API calls in this skill use the config values. **Never hardcode URLs or keys.** The templates below show the pattern for each provider type.

### Provider Differences

| Feature | `grsai` | `openai` / `openai-compatible` / `local` |
|---------|---------|------------------------------------------|
| Cover endpoint | `POST {base_url}/v1/images/generations` | `POST {base_url}/v1/images/generations` |
| Illustration endpoint | `POST {base_url}/v1/draw/completions` (SSE) | `POST {base_url}/v1/images/generations` |
| Cover request | `{"model","prompt","size","image?","response_format"}` | `{"model","prompt","size","image?"}` |
| Illustration request | `{"model","prompt","aspectRatio","replyType":"async"}` | `{"model","prompt","size":"1024x1024"}` |
| Cover response | `result["data"][0]["url"]` | `result["data"][0]["url"]` |
| Illustration response | SSE stream, `obj["results"][0]["url"]` | `result["data"][0]["url"]` |
| Auth header | `Bearer {api_key}` | `Bearer {api_key}` |

### Cover API Call (all providers)

```python
import json, urllib.request, ssl

# --- Load config ---
import os
with open(os.path.expanduser("~/.claude/skills/luoboa-illustrate/config.json")) as f:
    cfg = json.load(f)

API_URL = cfg["api"]["base_url"] + "/v1/images/generations"
API_KEY = cfg["api"]["api_key"]
MODEL = cfg["api"]["model"]
BRAND = cfg.get("brand", {})
LOGO_URL = BRAND.get("logo_url") if BRAND.get("enabled") and BRAND.get("logo_url") else None

# --- Build request ---
prompt = "..."  # style-specific prompt
outpath = "..."

req_data = {
    "model": MODEL,
    "prompt": prompt,
    "size": "1920x832",
}
if LOGO_URL:
    req_data["image"] = [LOGO_URL]
# GRS AI needs response_format
if cfg["api"]["provider"] == "grsai":
    req_data["response_format"] = "url"

data = json.dumps(req_data, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    API_URL, data=data,
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
)
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    urllib.request.urlretrieve(result["data"][0]["url"], outpath)
print("OK")
```

### Illustration API Call — GRS AI (async SSE)

```python
import json, urllib.request, ssl, os

with open(os.path.expanduser("~/.claude/skills/luoboa-illustrate/config.json")) as f:
    cfg = json.load(f)

API_URL = cfg["api"]["base_url"] + "/v1/draw/completions"
API_KEY = cfg["api"]["api_key"]
MODEL = cfg["api"]["model"]

prompt = "..."
outpath = "..."
ref_url = None  # Set to previous illustration URL for reference (Workflow B only)

req_data = {
    "model": MODEL,
    "prompt": prompt,
    "aspectRatio": "1024x1024",
    "replyType": "async"
}
if ref_url:
    req_data["image"] = [ref_url]

data_bytes = json.dumps(req_data, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    API_URL, data=data_bytes,
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
)
ctx = ssl.create_default_context()
returned_url = None
with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
    result = resp.read().decode("utf-8")
    for line in result.strip().split("\n"):
        if line.startswith("data: "):
            obj = json.loads(line[6:])
            if obj.get("status") == "succeeded":
                returned_url = obj["results"][0]["url"]
                urllib.request.urlretrieve(returned_url, outpath)
                print("OK")
                print("REF_URL: " + returned_url)
            elif obj.get("status") == "failed":
                print("FAIL: " + obj.get("failure_reason", "unknown"))
                # Retry without reference if ref_url caused the failure
                if ref_url:
                    req_data_no_ref = {
                        "model": MODEL,
                        "prompt": prompt,
                        "aspectRatio": "1024x1024",
                        "replyType": "async"
                    }
                    data_bytes2 = json.dumps(req_data_no_ref, ensure_ascii=False).encode("utf-8")
                    req2 = urllib.request.Request(
                        API_URL, data=data_bytes2,
                        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(req2, timeout=180, context=ctx) as resp2:
                        result2 = resp2.read().decode("utf-8")
                        for line2 in result2.strip().split("\n"):
                            if line2.startswith("data: "):
                                obj2 = json.loads(line2[6:])
                                if obj2.get("status") == "succeeded":
                                    returned_url = obj2["results"][0]["url"]
                                    urllib.request.urlretrieve(returned_url, outpath)
                                    print("OK (retry)")
                                    print("REF_URL: " + returned_url)
```

### Illustration API Call — OpenAI / Compatible / Local

```python
import json, urllib.request, ssl, os

with open(os.path.expanduser("~/.claude/skills/luoboa-illustrate/config.json")) as f:
    cfg = json.load(f)

API_URL = cfg["api"]["base_url"] + "/v1/images/generations"
API_KEY = cfg["api"]["api_key"]
MODEL = cfg["api"]["model"]

prompt = "..."
outpath = "..."
ref_url = None  # Set to previous illustration URL for reference (Workflow B only)

req_data = {
    "model": MODEL,
    "prompt": prompt,
    "size": "1024x1024"
}
if ref_url:
    req_data["image"] = [ref_url]

data_bytes = json.dumps(req_data, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    API_URL, data=data_bytes,
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
)
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    img_url = result["data"][0]["url"]
    urllib.request.urlretrieve(img_url, outpath)
print("OK")
print("REF_URL: " + img_url)  # Save for reference in subsequent illustrations
```

### Dreamina CLI Call

```bash
dreamina text2image --prompt "<prompt>" --output "<outpath>" --size "<size>"
```

- Cover: `--size "1920x832"`
- Illustration: `--size "1024x1024"`
- If not logged in → tell user to run `dreamina login`

---

## Workflow A: 科技类文章

### Read article structure
Read the entire `.md` file. Extract:
- **Article title** — the `# ` heading (or filename if none)
- **All section headings** — every `## ` subheading, in order
- **Full content of each section** — read ALL paragraphs under each heading

### Build prompts

**Cover prompt (dark-tech):**
```
极具视觉张力的商业科技海报，采用对立式构图。画面被中间一个巨大的、带有抽象笔触感的分割线一分为二。左半部分风格：极简主义，高调摄影风格（High-key），大面积留白，冷淡的工业美学。右半部分风格：华丽的赛博空间，低调摄影风格（Low-key），深色调，充满动态的粒子感或发光元素。视觉特征：强烈的明暗对比，电影级布光，超广角透视，孤独的人物剪影，现代主义排版风格。核心设计要求：主标题文字必须巨大、醒目、占据画面显著位置，字体要粗重有力，确保在手机缩略图上也能清晰阅读。{brand_text}内容文字：<提炼的标题短句，2-3行中文>
```

Where `{brand_text}` is generated from config:
- If `brand.enabled == true`: `品牌标识：左上角显示「{brand.name} | {brand.website} | {brand.tagline}」，左下角显示网址「{brand.website}」。`
- If `brand.enabled == false`: empty string

**Section illustration prompt (Excalidraw):**
```
我在给我的公众号配图，请使用Excalidraw，其带有手绘、草稿的视觉风格，内容如下，你需要做删减，取核心内容：<原文段落内容>
```

---

## Workflow B: 情感治愈类文章（小说/故事体裁）

### 核心原则：人物统一 + 情节还原

情感治愈类很多是**小说/故事体裁**，插图要画的是**小说里的具体情节场景**，不是泛泛的生活元素。两个最关键要求：

1. **把小说原文完整发给模型** — 包含人物描写、对话、场景细节
2. **用之前生成返回的URL作为参考图** — 保证同一篇文章里角色外观一致

### Read article structure
Read the entire `.md` file. Extract:
- **Article title** — the `# ` heading (or filename if none)
- **All section headings** — every `## ` subheading, in order
- **Full content of each section** — read ALL paragraphs, including dialogue, character descriptions, scene details

### Check for existing reference URL

**Before generating each section illustration**, check if this article's folder already has images:
```bash
ls "article/<MMDD>/<ArticleName>/"
```

- If images exist → use the **URL returned from the most recent generation** as `image` reference URL for the next illustration
- If no images yet → generate without reference

**CRITICAL: Always save the returned URL when an image is generated successfully.** The URL is publicly accessible and can be used directly as the reference for subsequent illustrations. Store the latest URL in your working memory for this article.

### Choose sub-style for cover
**Ask the user: "封面风格选哪种？"**
- **A: 治愈系手绘/插画风** — 莫兰迪色/奶油色/水彩淡彩，线条简洁，毛绒质感或水彩晕染。
- **B: 极简清新摄影风** — 高光低饱和度，自然光捕捉生活微小美好。
- **C: 文艺留白排版风** — 大面积纯色或低饱和风景，角落留大片空白，手写体文字。
- **D: 电影胶片/温暖光影风** — 淡淡颗粒感，暗角、暖黄色调，黄昏夕阳，逆光剪影。

If the user says nothing, default to **B（极简清新摄影风）**.

### Cover prompt (情感治愈类 — 小说封面)

封面是故事的第一印象，需要从小说内容中提炼**核心场景或人物形象**融入画面。情感治愈类封面不包含品牌标识，保持画面纯净。

**A — 治愈系手绘插画风：**
```
治愈系公众号封面插画，奶油色和莫兰迪色系，水彩晕染边缘，柔和的笔触。<从小说内容提炼的核心场景人物>。整体氛围温暖、治愈、放松。画面上方留白区域放置标题文字，字号为中粗圆形字体，奶白色。背景为淡奶油色渐变到浅燕麦色。整个画面留白充足，没有任何视觉压迫感。内容文字：<标题短句>
```

**B — 极简清新摄影风：**
```
极简清新风格的公众号封面，自然光摄影，高光低饱和度。<从小说内容提炼的核心场景人物>。背景是柔和的雾霾蓝渐变，桌面是浅木色。整个画面安静、岁月静好，上方或角落留出空白用于放置文字。字体建议选择圆体或宋体，奶白色。内容文字：<标题短句>
```

**C — 文艺留白排版风：**
```
文艺风格的公众号封面，大面积低饱和度暖色背景（如浅燕麦色或淡奶咖色）。<从小说内容提炼的核心场景人物>。画面右侧或底部留出超过50%的纯色空间。标题文字使用手写体或宋体，浅灰色，字号中等。整个画面风格克制、高级、有呼吸感。内容文字：<标题短句>
```

**D — 电影胶片温暖光影风：**
```
电影胶片质感的公众号封面，暖黄色调，带有淡淡的颗粒感和暗角。<从小说内容提炼的核心场景人物>。整体氛围安静、怀旧、有故事感。标题文字使用宋体或细圆体，暖白色，放在画面上方留白区域。内容文字：<标题短句>
```

### Section illustration prompt (情感治愈类 — 小说情节插图)

**CRITICAL: 必须把小说原文完整传入，不要删减场景描写和人物细节。**

**Without reference (first illustration):**
```
我在给我的公众号小说配插画，需要温暖治愈风格的插画。请使用柔和的莫兰迪色系，线条简洁，整体氛围安静、温暖、放松。画面要有足够的留白。小说原文情节如下，请画出这一幕的核心场景，注意人物外观请自行设计但要符合故事设定：
<本章节完整原文内容，包含人物描写、对话、场景细节>
```

**With reference URL (from previous illustration):**
```
我在给我的公众号小说配插画，需要温暖治愈风格的插画。请参考附件中已生成的角色形象图，保持人物外观一致（发型、服装，五官特征），仅改变场景和动作。请使用柔和的莫兰迪色系，线条简洁，整体氛围安静、温暖、放松。画面要有足够的留白。小说原文情节如下，请画出这一幕：
<本章节完整原文内容，包含人物描写、对话、场景细节>
```

---

## Workflow C: 通用风格（10种扩展风格）

当用户从"更多风格"中选择时，使用此工作流。每种风格有独立的封面prompt和插图prompt模板。

### Read article structure
Read the entire `.md` file. Extract:
- **Article title** — the `# ` heading (or filename if none)
- **All section headings** — every `## ` subheading, in order
- **Full content of each section** — read ALL paragraphs under each heading

### Build prompts by style

Each style's prompt template may include `{brand_text}` for brand identifier insertion (same logic as Workflow A).

#### 📐 3: 学术蓝图风 (`blueprint`)

**适合：** 系统架构、工程设计、深度技术文

**封面 prompt：**
```
学术蓝图风格的公众号封面，深蓝色网格背景，白色技术线条和标注，工程制图质感。画面中央是抽象的系统架构示意，带有标注线和尺寸标记。整体氛围专业、精密、有深度。标题文字使用等宽字体或技术字体，白色或亮蓝色，放在画面上方。背景为深蓝色带细微网格纹理。{brand_text}内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号技术文章配图，请使用技术蓝图/工程制图风格。深蓝色背景，白色线条和标注，带有网格底纹和尺寸标记。请将以下内容提炼为简洁的技术示意图：<原文段落内容>
```

**配色：** 深蓝底 + 白色线条 + 亮蓝标注
**元素：** 网格、标注线、尺寸标记、方框图、箭头流程
**含品牌标识：** 是
**字体建议：** 等宽字体 / 技术字体

---

#### ✏️ 4: 手绘笔记风 (`sketch-notes`)

**适合：** 知识教程、读书笔记、概念解析

**封面 prompt：**
```
手绘笔记风格的公众号封面，温暖奶白色背景（#F5F0E8），马卡龙色系点缀（淡蓝、薄荷绿、薰衣草紫、蜜桃粉）。画面中有手绘风格的关键词气泡、箭头连接、涂鸦装饰元素。整体氛围轻松、友好、有学习感。标题文字使用手写体，珊瑚色（#E8655A）强调。背景有轻微的手绘纸张质感。内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号知识文章配图，请使用手绘笔记/涂鸦笔记风格。温暖奶白色背景，马卡龙色系点缀，手绘线条带有微微的抖动感，关键词用气泡框和箭头连接。请将以下内容提炼为可视化的笔记构图：<原文段落内容>
```

**配色：** 奶白底 + 马卡龙点缀（淡蓝/薄荷/薰衣草/蜜桃）+ 珊瑚强调
**元素：** 手绘气泡框、箭头连接、涂鸦装饰、便签贴纸、荧光笔标记
**含品牌标识：** 否
**字体建议：** 手写体 / 圆体

---

#### 📜 5: 复古文艺风 (`vintage`)

**适合：** 历史人文、怀旧散文、品牌故事

**封面 prompt：**
```
复古文艺风格的公众号封面，做旧羊皮纸质感背景，泛黄褐色调，带有岁月痕迹的斑驳纹理。画面中有古典装饰元素如花纹边框、火漆印章、羽毛笔。整体氛围怀旧、优雅、有文化底蕴。标题文字使用宋体或仿宋体，深褐色或暗金色，放在画面中央。内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号文章配图，请使用复古文艺风格。做旧纸张背景，泛黄褐色调，古典装饰边框，带有岁月质感的纹理。请为以下内容创作复古风格的插图：<原文段落内容>
```

**配色：** 泛黄褐色底 + 暗金装饰 + 深褐文字
**元素：** 羊皮纸纹理、古典花纹边框、火漆印章、羽毛笔、复古地图
**含品牌标识：** 否
**字体建议：** 宋体 / 仿宋 / 古典衬线体

---

#### 🌸 6: 可爱萌系风 (`kawaii`)

**适合：** 生活分享、萌宠、轻松日常

**封面 prompt：**
```
可爱萌系风格的公众号封面，粉嫩柔和的配色（蜜桃粉、奶黄、薄荷绿、淡紫），粗描边，圆滚滚的造型。画面中有可爱的卡通元素如星星、爱心、云朵。整体氛围甜美、活泼、让人会心一笑。标题文字使用圆体，白色带粗描边，放在画面中央偏上。背景为柔和的粉色到奶白渐变。内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号生活类文章配图，请使用可爱萌系/卡哇伊风格。粉嫩配色，粗描边，圆滚滚的造型，可爱的装饰元素（星星、爱心、云朵）。请为以下内容创作萌系插图：<原文段落内容>
```

**配色：** 蜜桃粉 + 奶黄 + 薄荷绿 + 淡紫 + 奶白底
**元素：** 粗描边、圆滚滚造型、星星、爱心、云朵、贴纸感
**含品牌标识：** 否
**字体建议：** 圆体 / 可爱手写体

---

#### 🌆 7: 赛博霓虹风 (`cyberpunk-neon`)

**适合：** 未来科技、游戏、AI科幻

**封面 prompt：**
```
赛博朋克霓虹风格的公众号封面，深紫黑底色，强烈的霓虹发光效果（电光蓝、霓虹粉、荧光绿）。画面中有故障艺术（glitch）效果、数字雨、全息投影元素。整体氛围前卫、未来感、视觉冲击力极强。标题文字使用未来感科技字体，霓虹发光效果，放在画面中央。{brand_text}内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号科技文章配图，请使用赛博朋克霓虹风格。深紫黑背景，霓虹发光线条，故障艺术效果，全息投影质感。请为以下内容创作赛博风格的插图：<原文段落内容>
```

**配色：** 深紫黑底 + 电光蓝 + 霓虹粉 + 荧光绿
**元素：** 霓虹发光、故障艺术、数字雨、全息投影、电路纹理
**含品牌标识：** 是
**字体建议：** 科技感字体 / 未来主义字体

---

#### 💼 8: 极简商务风 (`corporate`)

**适合：** 行业分析、商业策略、投资人视角

**封面 prompt：**
```
极简商务风格的公众号封面，克制的配色（深灰、白、金色点缀），干净的几何构图。画面中有简洁的图形元素如柱状图、上升箭头、抽象人物剪影。整体氛围专业、高端、有权威感。标题文字使用无衬线字体，深灰色或金色，放在画面左侧留白区域。背景为纯白或浅灰。{brand_text}内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号商业分析文章配图，请使用极简商务风格。克制配色，干净几何构图，简洁的图表和箭头，专业高端的视觉语言。请为以下内容创作商务风格的插图：<原文段落内容>
```

**配色：** 纯白/浅灰底 + 深灰 + 金色点缀
**元素：** 几何图形、柱状图、箭头、人物剪影、简洁图标
**含品牌标识：** 是
**字体建议：** 无衬线字体 / Helvetica风格

---

#### 🍃 9: 自然水彩风 (`watercolor`)

**适合：** 旅行、养生、自然、慢生活

**封面 prompt：**
```
自然水彩风格的公众号封面，柔和的大地色系（苔绿、赭石、暖棕、天蓝），水彩晕染边缘，有机的笔触感。画面中有自然元素如植物、远山、水面倒影。整体氛围宁静、治愈、有自然气息。标题文字使用手写体或宋体，深绿或深棕，放在画面留白处。背景为淡雅的水彩渐变。内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号自然生活类文章配图，请使用自然水彩风格。柔和大地色系，水彩晕染边缘，有机笔触，自然元素。请为以下内容创作水彩风格的插图：<原文段落内容>
```

**配色：** 淡雅水彩底 + 苔绿 + 赭石 + 暖棕 + 天蓝
**元素：** 水彩晕染、植物叶片、远山、水面、天空、花朵
**含品牌标识：** 否
**字体建议：** 手写体 / 宋体

---

#### 🕹️ 10: 像素游戏风 (`pixel-art`)

**适合：** 游戏文化、复古科技、极客趣味

**封面 prompt：**
```
像素游戏风格的公众号封面，8-bit复古像素画，鲜明的色块，马赛克质感。画面中有复古游戏机、像素角色、游戏界面元素（血条、金币、对话框）。整体氛围怀旧、有趣、极客味十足。标题文字使用像素字体，白色或亮黄色，放在画面上方。背景为深色像素渐变。{brand_text}内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号极客趣味文章配图，请使用8-bit像素游戏风格。复古像素画，鲜明色块，马赛克质感，游戏界面元素。请为以下内容创作像素风格的插图：<原文段落内容>
```

**配色：** 深色底 + 鲜明色块（红/蓝/黄/绿像素色）
**元素：** 像素格子、游戏界面、血条、金币、对话框、复古游戏机
**含品牌标识：** 是
**字体建议：** 像素字体 / Press Start风格

---

#### 🎭 11: 海报丝印风 (`screen-print`)

**适合：** 观点评论、文化分析、深度社论

**封面 prompt：**
```
丝网印刷海报风格的公众号封面，大色块对比，半调网点纹理，有限的套色（3-4色）。画面中有强烈的视觉隐喻符号，粗犷有力的构图。整体氛围大胆、有态度、视觉冲击力强。标题文字使用粗体无衬线或特粗宋体，白色或亮色，占据画面核心位置。背景为深色块面。内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号深度评论文章配图，请使用丝网印刷海报风格。大色块对比，半调网点纹理，有限套色，强烈视觉符号。请为以下内容创作海报风格的插图：<原文段落内容>
```

**配色：** 深色块面 + 3-4色套色（如深红+米白+黑）
**元素：** 大色块、半调网点、视觉隐喻符号、粗犷线条
**含品牌标识：** 否
**字体建议：** 特粗无衬线 / 海报标题字体

---

#### 🧘 12: 禅意留白风 (`zen-minimal`)

**适合：** 哲学思辨、极简生活、禅意随笔

**封面 prompt：**
```
禅意留白风格的公众号封面，大面积纯净留白（超过60%），单色极简线描，呼吸感十足。画面中只有一个核心元素，用最少的笔墨表达。整体氛围宁静、深邃、有禅意。标题文字使用极细的宋体或手写体，浅灰色，放在画面大片留白区域。背景为纯白或极淡的暖灰。内容文字：<标题短句>
```

**插图 prompt：**
```
我在给我的公众号哲学/极简类文章配图，请使用禅意留白风格。大面积留白，单色极简线描，最少的元素表达核心概念。请为以下内容创作极简禅意插图：<原文段落内容>
```

**配色：** 纯白/极淡暖灰底 + 单色墨线（黑或深灰）
**元素：** 极简线描、大面积留白、单一核心元素、墨点
**含品牌标识：** 否
**字体建议：** 极细宋体 / 手写体 / 浅灰色

---

## {brand_text} Generation Rule

When a prompt template contains `{brand_text}`, replace it with:

**If `brand.enabled == true`:**
```
品牌标识：左上角显示「{brand.name} | {brand.website} | {brand.tagline}」，左下角显示网址「{brand.website}」。
```

**If `brand.enabled == false`:**
```
(空字符串，不插入任何内容)
```

### Which styles include brand on cover?

| 含品牌标识 | 不含品牌标识 |
|-----------|------------|
| 🖥️ 科技风 | 💕 柔情风 |
| 📐 学术蓝图风 | ✏️ 手绘笔记风 |
| 🌆 赛博霓虹风 | 📜 复古文艺风 |
| 💼 极简商务风 | 🌸 可爱萌系风 |
| 🕹️ 像素游戏风 | 🍃 自然水彩风 |
| | 🎭 海报丝印风 |
| | 🧘 禅意留白风 |

**When `brand.enabled == false`**, all styles render without brand — this is the default for open-source users.

---

## 风格配色与元素速查表

| 风格 | 色彩基调 | 核心元素 | 品牌标识 | 字体建议 |
|------|---------|---------|---------|---------|
| 🖥️ 科技风 | 深海蓝+深黑，强对比 | 粒子光效、科技线条、数据图表、人物剪影 | ✅ | 粗体无衬线 |
| 💕 柔情风 | 低饱和暖色、莫兰迪 | 自然光影、猫咪、花草、书籍 | ❌ | 圆体/宋体 |
| 📐 学术蓝图风 | 深蓝底+白线+亮蓝标注 | 网格、标注线、方框图、箭头 | ✅ | 等宽/技术字体 |
| ✏️ 手绘笔记风 | 奶白底+马卡龙点缀 | 手绘气泡框、箭头、涂鸦、便签 | ❌ | 手写体/圆体 |
| 📜 复古文艺风 | 泛黄褐+暗金 | 羊皮纸、花纹边框、火漆印章 | ❌ | 宋体/仿宋 |
| 🌸 可爱萌系风 | 蜜桃粉+奶黄+薄荷绿 | 粗描边、圆滚滚、星星爱心 | ❌ | 圆体/可爱手写 |
| 🌆 赛博霓虹风 | 深紫黑+霓虹发光 | 故障艺术、数字雨、全息投影 | ✅ | 未来主义字体 |
| 💼 极简商务风 | 纯白/浅灰+深灰+金 | 几何图形、图表、箭头、剪影 | ✅ | 无衬线/Helvetica |
| 🍃 自然水彩风 | 苔绿+赭石+天蓝 | 水彩晕染、植物、远山、水面 | ❌ | 手写体/宋体 |
| 🕹️ 像素游戏风 | 深色底+鲜明色块 | 像素格子、游戏界面、复古机 | ✅ | 像素字体 |
| 🎭 海报丝印风 | 深色块+3-4色套色 | 大色块、半调网点、视觉隐喻 | ❌ | 特粗无衬线 |
| 🧘 禅意留白风 | 纯白+单色墨线 | 极简线描、大面积留白、墨点 | ❌ | 极细宋体 |

---

## 通用规范

### 目录结构
```
article/<MMDD>/<ArticleName>/
├── 00-封面.png          (# 标题封面)
├── 01-<section>.png     (第一个 ## 标题)
├── 02-<section>.png     (第二个 ## 标题)
└── ...
```

### 图片尺寸
| 类型 | 尺寸 | 说明 |
|------|------|------|
| 封面 | `1920x832` (21:9) | 横屏，公众号封面必须 |
| 插图 | `1024x1024` (1:1) | 正方形，正文配图 |

### 关键规则
- **Send original section content directly** — do NOT summarize. The model needs the full text to generate relevant illustrations.
- For sections over 2000 characters, trim to 1000-1500 essential characters.
- Strip markdown formatting (`**`, `[]()`, `|---|`, etc.) before sending.
- For GPT-image-2 async responses (GRS AI): poll by reading SSE stream line by line until `"status":"succeeded"`.
- For OpenAI / compatible / local: standard REST response, parse `result["data"][0]["url"]`.
- If API returns `failed` status: retry once with rephrased prompt, or report error and continue.
- **Never hardcode API keys or URLs** — always read from config.

---

## 插入图片到文章

所有插图生成完毕后，必须把图片插入到文章的 `.md` 文件中。**封面不插入**，只插入 `##` 标题对应的插图。

### 插入规则

1. 每张插图插入到对应的 `##` 标题行的**正下方**
2. 图片上方空一行，图片下方空一行
3. 使用相对路径引用图片（相对于 md 文件的位置）
4. 封面图（`00-封面.png`）不插入文章

### 插入格式

在 `##` 标题行之后，插入如下内容：

```markdown
## 某某标题

![](images/01-某某标题.png)

正文内容...
```

注意三个关键空行：
- `##` 标题行和 `![](...)` 之间：**1个空行**
- `![](...)` 和正文之间：**1个空行**

### 实现步骤

1. 读取 md 文件全文
2. 找到所有 `## ` 开头的行，记录行号和标题内容
3. 按顺序匹配已生成的插图文件（`01-*.png`, `02-*.png`, ...）
4. **从后往前**插入（从最后一个 `##` 开始），这样前面的行号不会被影响
5. 每次插入的内容为：换行 + `![](images/<filename>)` + 换行
6. 写回文件

### 路径计算

插图文件在文章目录的 `images/` 子目录下。md 文件和 images 目录是平级的：

```
article/0531/某篇文章/
├── 某篇文章.md
└── images/
    ├── 00-封面.png
    ├── 01-四条规则.png
    ├── 02-160K星标.png
    └── ...
```

如果 md 文件直接在 `0531/` 下（和 `images/` 平级），引用路径就是 `images/01-xxx.png`。
如果 md 文件在 `0531/某篇文章/` 下，引用路径也是 `images/01-xxx.png`。

### 示例

插入前：
```markdown
## 一、四条规则，每一条都在堵一个AI的"坏习惯"

先说清楚这四条规则到底是什么。
```

插入后：
```markdown
## 一、四条规则，每一条都在堵一个AI的"坏习惯"

![](images/01-四条规则.png)

先说清楚这四条规则到底是什么。
```

---

## Edge Cases
- No config file → run Setup Wizard before proceeding
- No `## ` headings → generate only the cover, nothing to insert
- No `# ` heading → use filename as title
- API returns `violation` → rephrase prompt and retry
- API returns `failed` → report error and continue
- Dreamina not logged in → tell user to run `dreamina login`
- User only wants cover → generate only `00-封面.png`, no insertion needed
- Image file count doesn't match `##` heading count → insert what you have, skip missing
- User says "更多" but then picks 科技风 or 柔情风 → use Workflow A or B accordingly
- User wants to reconfigure → delete config file and re-run Setup Wizard
