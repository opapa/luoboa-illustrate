#!/usr/bin/env python
"""News headline illustrator — generate 9:16 pen-and-ink sketch images for each news item using dreamina CLI.

Usage:
  python news_generate.py \
    --input article.md \
    --data /path/to/news_data.json \
    --output article/2606/0603/news/

The news_data.json file should contain pre-extracted short_title and scene_en for each news item.
The AI (Claude) is responsible for parsing the .md file and generating the JSON; this script only handles image generation.

Output:
  {output}/01-{slug}.png
  {output}/02-{slug}.png
  ...
  {output}/manifest.txt
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import ssl

# Force UTF-8 stdout on Windows (avoid GBK codec errors with emoji)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --- Minimal YAML parser (same as quick_generate.py) ---

def parse_yaml(text):
    result = {}
    stack = [(0, result)]
    for line in text.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        content = stripped.strip()
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        if ":" not in content:
            continue
        key, _, value = content.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            new_dict = {}
            stack[-1][1][key] = new_dict
            stack.append((indent, new_dict))
        else:
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.lower() == "null":
                value = None
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
            stack[-1][1][key] = value
    return result


def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    config_path = os.path.join(skill_root, "config.yaml")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return parse_yaml(f.read())


CONFIG = load_config()

# --- News config ---

news_config = CONFIG.get("news", {})
DEFAULT_RATIO = news_config.get("ratio", "9:16")
DEFAULT_RESOLUTION = news_config.get("resolution", "2k")
DEFAULT_POLL_TIMEOUT = int(news_config.get("poll_timeout", 120))
DEFAULT_MODEL = news_config.get("model", "high_aes_general_v50")
USE_REF_URL = news_config.get("ref_url_from_previous", False)  # default off; dreamina text2image doesn't support ref-url


# --- Prompt template ---

# Category color scheme (macaron palette, baoyu-style)
CATEGORY_COLORS = {
    "AI大模型":     {"fill": "#A8D8EA", "ink": "#4A90A4"},  # macaron blue
    "AI Agent":     {"fill": "#D5C6E0", "ink": "#7B6B8C"},  # lavender
    "AI工具":       {"fill": "#B5E5CF", "ink": "#5A9078"},  # mint
    "AI行业动态":   {"fill": "#F8D5C4", "ink": "#B06850"},  # peach
}

# ⚠️ Dreamina 5.0 内容风控会拒掉同时含 "每日AI快讯" + 具体日期的 prompt
# （`generation failed: final generation failed`），所以"每日AI快讯 X月X日"
# 这一行小灰字 **不能** 写进 prompt——出图后用 overlay_timestamp() 用 PIL 叠。
# 其他元素（"AI大模型"chip、品牌词如腾讯云/DeepSeek、百分比、bullets、彩色高亮、
# 5 个手绘装饰图标）实测都能直接塞进 prompt，dreamina 5.0 都能渲染清楚。
# —— 摸顺时间 2026-06-04，详见 references/news-styles.md "dreamina 风控触发词"
PROMPT_TEMPLATE = (
    'Q版二头身手绘水彩马克笔风格，奶油色背景。'
    '右半边：{scene_zh}。'
    '左半边大字写「{short_title}」，上方小{category_color_name}标签写 {category}。'
    '标题下三行小手写要点：{bullets_formatted}。'
    '其中 {hl1} 用紫色，{hl2} 用红色，{hl3} 用橙色。'
    '右侧散落手绘小图标：灯泡、齿轮、问号、闪电、爱心。'
    '黑色墨水手绘线条，水彩块状上色，低饱和马卡龙色调，绘本插画风。'
    '每个汉字必须完整清晰可读，不要乱码不要缺字。'
)

# Category chip color names (Chinese, for dreamina prompt)
CATEGORY_COLOR_NAMES = {
    "AI大模型":   "蓝色",
    "AI Agent":   "淡紫色",
    "AI工具":     "薄荷绿",
    "AI行业动态": "蜜桃色",
}


def format_bullets(bullets):
    """Format bullet list as Chinese semicolon-separated points."""
    if not bullets:
        return ""
    return " ；".join(bullets)


def derive_highlights(bullets):
    """Fallback: extract 3 highlight terms from bullets when item didn't provide them.

    Picks: (1) first percentage / number, (2) second percentage / number,
    (3) a short standout phrase from the last bullet.
    """
    import re as _re
    nums = []
    for b in bullets or []:
        # 抓 75% / 97.5% / 150亿 / 一万亿 这种数字/数量词
        for m in _re.finditer(r"\d+(?:\.\d+)?\s*[%％万亿千百]?", b):
            tok = m.group().strip()
            if tok and tok not in nums:
                nums.append(tok)
    hl1 = nums[0] if len(nums) > 0 else (bullets[0].split()[-1] if bullets else "重点")
    hl2 = nums[1] if len(nums) > 1 else (bullets[1].split()[-1] if len(bullets or []) > 1 else "亮点")
    # 第 3 个：找含中文短词（取最后一条的前 4 字）
    hl3 = (bullets[2][:4] if len(bullets or []) > 2 else "趋势")
    return hl1, hl2, hl3


def build_prompt(date, short_title, scene_en, category="AI大模型", num=1,
                 bullets=None, scene_zh=None, highlights=None):
    """Build the full prompt for one news item.

    New (v3, 2026-06-04): 中文海报 prompt，绕开 dreamina 风控触发词。

    Args:
        date: e.g. "6月4日" — used by overlay_timestamp(), NOT in prompt
        short_title: title text (e.g. "腾讯云DeepSeek-V4大降价")
        scene_en: legacy English scene description (used as fallback when scene_zh absent)
        scene_zh: NEW preferred — Chinese 1-line scene (e.g. "一个吃惊的小程序员卡通，怀里抱着一摞云服务器")
        category: one of CATEGORY_COLORS keys
        bullets: list of 3 short Chinese strings
        highlights: optional [hl1, hl2, hl3] — 3 keyword strings to color-highlight.
                    If omitted, derived from bullets via derive_highlights().
    """
    color_name = CATEGORY_COLOR_NAMES.get(category, "蓝色")
    bullets = bullets or []
    scene = scene_zh or scene_en  # 没给中文 scene 就用英文 scene 兜底

    if highlights and len(highlights) >= 3:
        hl1, hl2, hl3 = highlights[0], highlights[1], highlights[2]
    else:
        hl1, hl2, hl3 = derive_highlights(bullets)

    return PROMPT_TEMPLATE.format(
        short_title=short_title,
        scene_zh=scene,
        category=category,
        category_color_name=color_name,
        bullets_formatted=format_bullets(bullets),
        hl1=hl1, hl2=hl2, hl3=hl3,
    )


# --- Dreamina CLI ---

def run_dreamina_text2image(prompt, ratio=DEFAULT_RATIO, resolution=DEFAULT_RESOLUTION,
                            model=DEFAULT_MODEL, poll=DEFAULT_POLL_TIMEOUT):
    """Call dreamina text2image and return (submit_id, gen_status) or (None, error_msg)."""
    cmd = [
        "dreamina", "text2image",
        "--prompt", prompt,
        "--ratio", ratio,
        "--resolution_type", resolution,
        "--model_version", model,
        "--poll", str(poll),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=poll + 30,
        )

        if result.returncode != 0:
            return None, f"CLI error: {result.stderr[:200] or result.stdout[:200]}"

        # Parse the JSON output (may be one or more JSON objects)
        output = result.stdout.strip()
        # Try the last JSON object (in case multiple were printed)
        json_objects = []
        decoder_pos = 0
        while decoder_pos < len(output):
            try:
                obj, idx = json.JSONDecoder().raw_decode(output[decoder_pos:])
                json_objects.append(obj)
                decoder_pos += idx
                # Skip whitespace
                while decoder_pos < len(output) and output[decoder_pos] in ' \t\r\n':
                    decoder_pos += 1
            except json.JSONDecodeError:
                break

        if not json_objects:
            return None, "No JSON in output"

        # Take the last object (most recent status)
        last = json_objects[-1]
        return last.get("submit_id"), last.get("gen_status", "unknown")

    except subprocess.TimeoutExpired:
        return None, "CLI timeout"
    except Exception as e:
        return None, f"CLI exception: {e}"


def run_dreamina_query_result(submit_id):
    """Call dreamina query_result and return (gen_status, image_url_or_None)."""
    cmd = ["dreamina", "query_result", "--submit_id", submit_id]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            return "error", None

        try:
            obj = json.loads(result.stdout)
        except json.JSONDecodeError:
            return "error", None

        status = obj.get("gen_status", "unknown")

        if status == "success":
            images = obj.get("result_json", {}).get("images", [])
            if images and len(images) > 0:
                return status, images[0].get("image_url")
            return status, None

        return status, None

    except subprocess.TimeoutExpired:
        return "timeout", None
    except Exception as e:
        return "error", None


def generate_image(prompt, item, max_wait=300):
    """Generate one image. Returns image_url or None.

    Flow:
      1. Submit with text2image --poll=N (N=120 by default)
      2. If status is 'querying' after poll, use query_result to wait
      3. If status is 'success', return image_url
      4. If status is 'failed' or other, return None
    """
    submit_id, status = run_dreamina_text2image(prompt)

    if not submit_id:
        print(f"  [{item['num']:02d}] ❌ Submit failed: {status}")
        return None

    if status == "success":
        # Got it on the first poll; re-query to get image_url
        status, url = run_dreamina_query_result(submit_id)
        if status == "success" and url:
            return url
        print(f"  [{item['num']:02d}] ⚠️ Submit returned success but no URL (status={status})")
        return None

    if status == "querying":
        # Poll with query_result
        start = time.time()
        while time.time() - start < max_wait:
            time.sleep(5)
            status, url = run_dreamina_query_result(submit_id)
            if status == "success" and url:
                return url
            if status in ("failed", "error"):
                print(f"  [{item['num']:02d}] ❌ Generation failed: {status}")
                return None
            # Still querying; continue waiting
        print(f"  [{item['num']:02d}] ⏱️ Timeout after {max_wait}s")
        return None

    print(f"  [{item['num']:02d}] ❌ Unexpected status: {status}")
    return None


def download_image(url, output_path, timeout=60):
    """Download image from URL to local path."""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            with open(output_path, "wb") as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download error: {e}")
        return False


# --- Timestamp overlay (post-processing) ---
#
# Dreamina 5.0 拒掉同时含 "每日AI快讯" + 日期 的 prompt（v3 风控触发词），
# 所以日期戳必须出图后用 PIL 叠。叠在顶部居中偏右，灰色，仿 API 原版位置。
#
# 字体优先级：用户自配 > 微软雅黑 > 楷体 > PIL 默认
_TIMESTAMP_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simkai.ttf",
    r"C:\Windows\Fonts\simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",  # macOS
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # linux
]


def _resolve_font(size):
    """Find a usable Chinese font; return PIL ImageFont or None."""
    try:
        from PIL import ImageFont
    except ImportError:
        return None
    for path in _TIMESTAMP_FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def overlay_timestamp(img_path, date_text, label="每日AI快讯"):
    """Stamp "每日AI快讯 X月X日" small gray text on top of the image (in-place).

    Skipped silently when PIL isn't installed or when date_text is empty —
    image is still usable, just without the timestamp.
    """
    if not date_text:
        return False
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print(f"  ⚠️ PIL not installed; skipping timestamp overlay")
        return False
    try:
        img = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print(f"  ⚠️ Can't open image for overlay: {e}")
        return False

    W, H = img.size
    size = max(int(W * 0.032), 18)
    font = _resolve_font(size)
    if font is None:
        return False

    text = f"{label}  {date_text}"
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        tw, th = size * len(text) // 2, size  # rough fallback

    x = W - tw - int(W * 0.06)
    y = int(H * 0.022)
    draw.text((x, y), text, font=font, fill=(80, 80, 80, 230))

    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(img_path, "PNG")
    return True


# --- Slug generation ---

def slugify(text, max_len=20):
    """Convert text to a filename-safe slug."""
    # Keep ASCII letters, digits, hyphen, underscore
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[-\s_]+", "-", slug).strip("-")
    if not slug:
        slug = "untitled"
    return slug[:max_len]


# --- Manifest ---

def write_manifest(output_dir, items, results):
    """Write manifest.txt with one line per news item.

    New format (since v2 ink+watercolor design):
      | 序号 | 分类 | 精简标题 | bullet1 | bullet2 | bullet3 | 状态 |
    """
    manifest_path = os.path.join(output_dir, "manifest.txt")
    with open(manifest_path, "w", encoding="utf-8") as f:
        for item, result in zip(items, results):
            num = f"{item['num']:02d}"
            category = item.get("category", "")
            short = item.get("short_title", "")
            bullets = item.get("bullets", [])
            b1 = bullets[0] if len(bullets) > 0 else ""
            b2 = bullets[1] if len(bullets) > 1 else ""
            b3 = bullets[2] if len(bullets) > 2 else ""
            status = "✅" if result else "❌"
            f.write(f"{num}|{category}|{short}|{b1}|{b2}|{b3}|{status}\n")
    return manifest_path


# --- Main ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Parse arguments
    args = {}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                args[key] = sys.argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1

    input_file = args.get("input", "")
    data_file = args.get("data", "")
    output_dir = args.get("output", "")

    if not input_file or not data_file or not output_dir:
        print("ERROR: --input, --data, and --output are all required")
        print(__doc__)
        sys.exit(1)

    # Load news data JSON
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    date = data.get("date", "")
    items = data.get("items", [])

    if not items:
        print("ERROR: No items in data file")
        sys.exit(1)

    if not date:
        # Try to derive from filename
        base = os.path.basename(input_file)
        m = re.search(r"(\d{2})(\d{2})", base)
        if m:
            date = f"{int(m.group(1))}月{int(m.group(2))}日"
        else:
            date = "今日"

    print(f"📰 Date: {date}")
    print(f"📄 Input: {input_file}")
    print(f"📦 Data: {data_file} ({len(items)} items)")
    print(f"📁 Output: {output_dir}")
    print(f"🎨 Style: pen-and-ink documentary sketch (9:16)")
    print(f"🔧 Model: {DEFAULT_MODEL}, ratio: {DEFAULT_RATIO}")
    print()

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate images sequentially
    results = []
    success_count = 0
    fail_count = 0

    for item in items:
        num = item["num"]
        short_title = item["short_title"]
        scene_en = item["scene_en"]
        category = item.get("category", "AI大模型")
        bullets = item.get("bullets", [])

        print(f"  [{num:02d}] {short_title}")
        print(f"        category: {category}")
        print(f"        bullets: {len(bullets)}")
        print(f"        scene: {scene_en[:60]}...")

        prompt = build_prompt(date, short_title, scene_en,
                              category=category, num=num, bullets=bullets)

        # First attempt
        url = generate_image(prompt, item)

        if not url:
            # Retry：稍微加强风格关键词；新模板对 dreamina 5.0 通常一发就过
            print(f"  [{num:02d}] 🔄 Retrying with stronger style emphasis...")
            emphasized_prompt = prompt.replace(
                "Q版二头身手绘水彩马克笔风格",
                "Q版二头身手绘水彩马克笔风格，绘本插画，细致清晰"
            )
            url = generate_image(emphasized_prompt, item)

        if url:
            slug = slugify(short_title)
            target_path = os.path.join(output_dir, f"{num:02d}-{slug}.png")
            if download_image(url, target_path):
                # 补上被 dreamina 风控拒掉的 "每日AI快讯 X月X日" 小灰字
                if overlay_timestamp(target_path, date):
                    print(f"  [{num:02d}] ✅ Saved + timestamp: {target_path}")
                else:
                    print(f"  [{num:02d}] ✅ Saved (no timestamp): {target_path}")
                results.append(target_path)
                success_count += 1
            else:
                print(f"  [{num:02d}] ❌ Download failed")
                results.append(None)
                fail_count += 1
        else:
            print(f"  [{num:02d}] ❌ Generation failed after retry")
            results.append(None)
            fail_count += 1

    # Write manifest
    manifest_path = write_manifest(output_dir, items, results)

    print()
    print(f"{'='*50}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed:  {fail_count}")
    print(f"📊 Total:   {len(items)}")
    print(f"📝 Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
