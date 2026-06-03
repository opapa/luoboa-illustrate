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

PROMPT_TEMPLATE = (
    '9:16 vertical hand-drawn news card. '
    'Top 5% is a black header bar with white text "每日AI快讯 {date}" (crystal clear, no garbling). '
    'Below header on the left, a macaron {category_color_fill} category chip with Chinese text "【{category}】". '
    'Title: 「{short_title}」 in dark gray, hand-lettered style with rough wobble. '
    'Bullet block in cream (#F5F0E8) with 3 hand-drawn points in coral red dots:\n'
    '{bullets_formatted}\n'
    'Lower 50% scene: colored pencil illustration (彩色铅笔 画) with visible pencil strokes, soft waxy texture, multiple colors used, cream paper background, illustrating: {scene_en}. Visible colored pencil strokes in every shape, soft layering of pigments, slight grain texture, hand-drawn feel, no flat color fills. '
    'Footer: "# {num:02d} | {date}". '
    'Style: colored pencil drawing with visible strokes and soft layering, NOT digital art NOT watercolor wash NOT pure ink NOT oil painting, hand-drawn texture, warm friendly illustrative feel, like a childrens book editorial illustration in colored pencil. macaron palette cream background pastel chip coral red accent. '
    'Text rendered cleanly without garbled characters. '
    'NO flat color, NO vector, NO anime, NO photographic, NO digital gradients, NO smooth shading.'
)


def format_bullets(bullets):
    """Format bullet list for the prompt."""
    if not bullets:
        return ""
    return "\n".join(f"  • {b}" for b in bullets)


def build_prompt(date, short_title, scene_en, category="AI大模型", num=1, bullets=None):
    """Build the full prompt for one news item."""
    cat = CATEGORY_COLORS.get(category, CATEGORY_COLORS["AI大模型"])
    return PROMPT_TEMPLATE.format(
        date=date,
        short_title=short_title,
        scene_en=scene_en,
        category=category,
        category_color_fill=cat["fill"],
        category_color_ink=cat["ink"],
        bullets_formatted=format_bullets(bullets or []),
        num=num,
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
            # Retry with emphasized style keywords
            print(f"  [{num:02d}] 🔄 Retrying with emphasized style...")
            emphasized_prompt = prompt.replace(
                "fine line weight 1-2pt",
                "EXTRABOLD fine line weight 1-2pt, absolutely strict pen-and-ink style"
            )
            url = generate_image(emphasized_prompt, item)

        if url:
            slug = slugify(short_title)
            target_path = os.path.join(output_dir, f"{num:02d}-{slug}.png")
            if download_image(url, target_path):
                print(f"  [{num:02d}] ✅ Saved: {target_path}")
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
