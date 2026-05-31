#!/usr/bin/env python
"""Quick article illustrator — generate 9:16 images per sentence using jimeng CLI.

Usage:
  python quick_generate.py \
    --input article.md \
    --output article/2606/0601/ArticleName/quick/ \
    --style tech-blue \
    --concurrency 2

Reads config.yaml from the skill root for jimeng settings.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# --- Minimal YAML parser (same as generate.py) ---

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


# --- Jimeng CLI settings ---

def find_jimeng_cli():
    """Find jimeng-cli-free installation path."""
    # 1. From config
    jimeng_config = CONFIG.get("jimeng", {})
    cli_path = jimeng_config.get("cli_path", "")
    if cli_path and os.path.isfile(os.path.join(cli_path, "bin", "jimeng-cli-free")):
        return cli_path

    # 2. Search common locations
    home = os.path.expanduser("~")
    search_paths = [
        os.path.join(home, ".claude", "skills", "jimeng-cli-free"),
        os.path.join(home, ".agents", "skills", "jimeng-cli-free"),
    ]

    for p in search_paths:
        entry = os.path.join(p, "bin", "jimeng-cli-free")
        if os.path.isfile(entry):
            return p

    # 3. Search PATH
    result = shutil.which("jimeng-cli-free")
    if result:
        # Go up from bin/jimeng-cli-free to the repo root
        return os.path.dirname(os.path.dirname(result))

    return None


JIMENG_ROOT = find_jimeng_cli()
JIMENG_CONFIG = CONFIG.get("jimeng", {})
DEFAULT_MODEL = JIMENG_CONFIG.get("model", "high_aes_general_v50")
DEFAULT_ASPECT = JIMENG_CONFIG.get("aspect", "9:16")


# --- Style templates ---

STYLE_TEMPLATES = {
    "tech-blue": (
        '9:16竖版海报，深蓝色到靛蓝色渐变背景，带有微弱的电路板纹理和流动的数据光线。'
        '画面上方约三分之一区域显示文字：「{sentence}」，使用白色粗体无衬线字体，'
        '带有微弱的蓝色发光效果，清晰可读。下方为抽象的科技场景：发光的芯片线路、'
        '全息投影数据流、或神经网络节点连接图。边缘有细微的蓝色光晕装饰。'
        '文字渲染清晰不乱码，排版简洁大气。'
    ),
    "hot-red": (
        '9:16竖版海报，深红色到暗红棕色渐变背景，带有隐约的火焰纹理和热浪扭曲效果。'
        '画面上方约三分之一区域显示文字：「{sentence}」，使用金色粗体宋体字，'
        '带有微弱的暖光效果，清晰可读。下方为动态的热点场景：跳动的数据脉冲、'
        '上升的火焰粒子、或爆炸式扩散的光环。边缘有微弱的红色能量波纹。'
        '文字渲染清晰不乱码，排版简洁大气。'
    ),
    "fresh-green": (
        '9:16竖版海报，浅薄荷绿到白色渐变背景，干净清爽的质感。'
        '画面上方约三分之一区域显示文字：「{sentence}」，使用深灰绿色圆体字，'
        '笔画柔和，清晰可读。下方为清新的自然场景：简约的植物线条画、'
        '波浪形的绿色渐变、或几何化的叶片图案。装饰元素为细线条和圆形点缀。'
        '文字渲染清晰不乱码，排版简洁大气。'
    ),
    "minimal-black": (
        '9:16竖版海报，纯黑背景，无纹理无渐变。'
        '画面上方约三分之一区域显示文字：「{sentence}」，使用纯白色粗体黑体字，'
        '大号，无任何特效，清晰可读。下方为极简的白色线条画：一个简洁的图标、'
        '一条水平线、或一个几何形状。没有任何多余装饰元素。'
        '文字渲染清晰不乱码，排版简洁大气。'
    ),
    "night-purple": (
        '9:16竖版海报，深紫色到藏蓝色渐变背景，带有微弱的星空纹理。'
        '画面上方约三分之一区域显示文字：「{sentence}」，使用浅紫白色圆体字，'
        '带有柔和的发光效果，清晰可读。下方为梦幻的宇宙场景：闪烁的星光、'
        '漂浮的几何棱镜、或流动的紫色星云。边缘有细微的紫色光粒子装饰。'
        '文字渲染清晰不乱码，排版简洁大气。'
    ),
    "news-style": (
        '9:16竖版海报，浅灰白色背景，带有细微的新闻纸张纹理。'
        '画面上方约三分之一区域显示文字：「{sentence}」，使用深灰色宋体字，'
        '正式庄重，清晰可读。下方为简洁的信息图示意：数据图表轮廓、新闻剪影、'
        '或柱状图折线图等图表元素。画面四周有细灰色边框线装饰，角落有小圆点。'
        '文字渲染清晰不乱码，排版简洁大气。'
    ),
}

# Fallback prompts for retry when text is garbled
RETRY_FONT_SWAPS = {
    "tech-blue": "白色超大号粗体黑体字，无发光效果",
    "hot-red": "白色加粗加大圆体字，无特效",
    "fresh-green": "深灰色加粗黑体字，笔画粗壮",
    "minimal-black": "纯白色超大号粗体宋体字",
    "night-purple": "白色加粗黑体字，无发光效果",
    "news-style": "黑色加粗加大圆体字，笔画粗壮",
}


# --- Sentence splitting ---

def split_sentences(md_text):
    """Split markdown text into sentences by 。！？ and newlines."""
    # Remove image lines
    text = re.sub(r'!\[.*?\]\(.*?\)', '', md_text)
    # Remove markdown formatting
    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\|[-:]+\|', '', text)
    text = re.sub(r'^\s*\|', '', text, flags=re.MULTILINE)

    # Split by sentence-ending punctuation and newlines
    parts = re.split(r'([。！？\n])', text)

    sentences = []
    current = ""
    for part in parts:
        if part in ('。', '！', '？'):
            current += part
            stripped = current.strip()
            if stripped and len(stripped) > 2:
                sentences.append(stripped)
            current = ""
        elif part == '\n':
            stripped = current.strip()
            if stripped and len(stripped) > 2:
                sentences.append(stripped)
            current = ""
        else:
            current += part

    # Don't forget the last fragment
    stripped = current.strip()
    if stripped and len(stripped) > 2:
        sentences.append(stripped)

    return sentences


def truncate_sentence(sentence, max_len=50):
    """Truncate a sentence to max_len, preferring comma boundaries."""
    if len(sentence) <= max_len:
        return sentence

    # Try to cut at a comma
    truncated = sentence[:max_len]
    last_comma = truncated.rfind('，')
    if last_comma > max_len // 2:
        return truncated[:last_comma + 1]

    return truncated + '…'


# --- Image generation ---

def generate_with_jimeng(prompt, model=None, aspect=None, output_dir=None):
    """Call jimeng CLI to generate an image. Returns path to best result or None."""
    if not JIMENG_ROOT:
        print("ERROR: jimeng-cli-free not found. Install it first.")
        return None

    model = model or DEFAULT_MODEL
    aspect = aspect or DEFAULT_ASPECT

    cli_script = os.path.join(JIMENG_ROOT, "bin", "jimeng-cli-free")
    if not os.path.isfile(cli_script):
        print(f"ERROR: CLI script not found at {cli_script}")
        return None

    cmd = [
        "bash", cli_script, "generate", prompt,
        "--model", model,
        "--aspect", aspect,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=JIMENG_ROOT,
        )

        if result.returncode != 0:
            print(f"  CLI error: {result.stderr[:200]}")
            return None

        # Find the latest output directory
        output_base = os.path.join(JIMENG_ROOT, "output")
        if not os.path.isdir(output_base):
            return None

        subdirs = sorted([
            d for d in os.listdir(output_base)
            if os.path.isdir(os.path.join(output_base, d))
        ], reverse=True)

        if not subdirs:
            return None

        latest = os.path.join(output_base, subdirs[0])
        # Find the first png/jpg file (0001)
        for fname in sorted(os.listdir(latest)):
            if fname.startswith("0001") and (fname.endswith(".png") or fname.endswith(".jpg")):
                return os.path.join(latest, fname)

        # Fallback: any image file
        for fname in sorted(os.listdir(latest)):
            if fname.endswith((".png", ".jpg", ".webp")):
                return os.path.join(latest, fname)

        return None

    except subprocess.TimeoutExpired:
        print("  CLI timeout (120s)")
        return None
    except Exception as e:
        print(f"  CLI exception: {e}")
        return None


def process_sentence(idx, sentence, style, model, output_dir):
    """Generate one image for a sentence. Returns (idx, sentence, result_path_or_None)."""
    template = STYLE_TEMPLATES.get(style, STYLE_TEMPLATES["tech-blue"])
    prompt = template.format(sentence=sentence)

    num = f"{idx:02d}"
    target_path = os.path.join(output_dir, f"{num}.png")

    print(f"  [{num}] Generating: {sentence[:40]}...")

    # First attempt
    result = generate_with_jimeng(prompt, model=model)

    if result and os.path.isfile(result):
        shutil.copy2(result, target_path)
        print(f"  [{num}] ✅ Done")
        return (idx, sentence, target_path)

    # Retry with font swap
    retry_template = template
    font_swap = RETRY_FONT_SWAPS.get(style, "白色加粗加大黑体字")
    # Replace font description in prompt
    retry_prompt = prompt
    # Simple: rebuild with swapped font
    retry_prompt = retry_prompt.replace("白色粗体无衬线字体，带有微弱的蓝色发光效果", font_swap)
    retry_prompt = retry_prompt.replace("金色粗体宋体字，带有微弱的暖光效果", font_swap)
    retry_prompt = retry_prompt.replace("深灰绿色圆体字，笔画柔和", font_swap)
    retry_prompt = retry_prompt.replace("纯白色粗体黑体字，大号，无任何特效", font_swap)
    retry_prompt = retry_prompt.replace("浅紫白色圆体字，带有柔和的发光效果", font_swap)
    retry_prompt = retry_prompt.replace("深灰色宋体字，正式庄重", font_swap)

    print(f"  [{num}] 🔄 Retrying with adjusted font...")
    result = generate_with_jimeng(retry_prompt, model=model)

    if result and os.path.isfile(result):
        shutil.copy2(result, target_path)
        print(f"  [{num}] ✅ Done (retry)")
        return (idx, sentence, target_path)

    print(f"  [{num}] ❌ Failed after retry")
    return (idx, sentence, None)


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
    output_dir = args.get("output", "")
    style = args.get("style", "tech-blue")
    model = args.get("model", DEFAULT_MODEL)
    concurrency = int(args.get("concurrency", "2"))

    if not input_file or not output_dir:
        print("ERROR: --input and --output are required")
        sys.exit(1)

    if style not in STYLE_TEMPLATES:
        print(f"ERROR: Unknown style '{style}'. Available: {', '.join(STYLE_TEMPLATES.keys())}")
        sys.exit(1)

    if not JIMENG_ROOT:
        print("ERROR: jimeng-cli-free not found. Install it or set cli_path in config.yaml.")
        sys.exit(1)

    # Read and split
    with open(input_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    sentences = split_sentences(md_text)
    if not sentences:
        print("ERROR: No sentences found in the input file.")
        sys.exit(1)

    # Truncate long sentences
    sentences = [truncate_sentence(s) for s in sentences]

    print(f"📄 Found {len(sentences)} sentences")
    print(f"🎨 Style: {style}")
    print(f"🔧 Model: {model}")
    print(f"📁 Output: {output_dir}")
    print()

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate images
    results = []
    success_count = 0
    fail_count = 0

    if concurrency <= 1:
        # Sequential
        for idx, sentence in enumerate(sentences, 1):
            r = process_sentence(idx, sentence, style, model, output_dir)
            results.append(r)
            if r[2]:
                success_count += 1
            else:
                fail_count += 1
    else:
        # Parallel with limited concurrency
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = {}
            for idx, sentence in enumerate(sentences, 1):
                f = executor.submit(process_sentence, idx, sentence, style, model, output_dir)
                futures[f] = idx
                # Small stagger to avoid overwhelming jimeng
                time.sleep(0.5)

            for f in as_completed(futures):
                r = f.result()
                results.append(r)
                if r[2]:
                    success_count += 1
                else:
                    fail_count += 1

    # Sort results by index
    results.sort(key=lambda x: x[0])

    # Write sentences.txt
    sentences_path = os.path.join(output_dir, "sentences.txt")
    with open(sentences_path, "w", encoding="utf-8") as f:
        for idx, sentence, path in results:
            num = f"{idx:02d}"
            status = "✅" if path else "❌"
            f.write(f"{num}|{sentence}|{status}\n")

    print()
    print(f"{'='*50}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed:  {fail_count}")
    print(f"📊 Total:   {len(sentences)}")
    print(f"📝 Sentences list: {sentences_path}")


if __name__ == "__main__":
    main()
