#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate 4 images for article 2606/0608 SKILL.md context article.
Workflow A (whiteboard/hand-drawn/excalidraw/wobbly/balanced).
Banner 21:9 + 3 content images 16:9.
"""
import sys
import os
import shutil

# Add skill scripts to path
SKILL_DIR = r"C:\Users\opapa\.claude\skills\luoboa-illustrate"
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from generate import generate_cover, generate_section, CONFIG  # noqa: E402

ARTICLE_DIR = r"H:\iCloudDrive\myvault\media\article\2606\0608\我把 SKILL.md 全塞进 context 了，面试官看了直摇头"
IMAGES_DIR = os.path.join(ARTICLE_DIR, "images")

# Common 5-dim preamble for consistency (TS-* style)
CONSISTENT = """Consistent with cover: hand-drawn excalidraw sketch rendering, excalidraw palette (white #FFFFFF / charcoal #2D2D2D / blue #4D96FF / yellow #FFD93D), balanced-technical mood. 16:9 landscape format.

White paper background #FFFFFF (NO gradients, NO textures, NO patterns, looks like clean paper).

Lines have slight imperfection — not laser-straight, slightly wobbly like a hand drew them. Boxes have slight wobble in edges. Use 思源黑体 or handwriting-style font for Chinese. Brand watermark at bottom-right: 'luoboa.com 萝卜啊' in light gray #B0B0B0, 8pt, handwriting font.

Chinese text must be SHARP and LEGIBLE, anti-aliased, 14-18pt. NOT photorealistic, NOT 3D, NOT painterly, NOT watercolor, NOT flat vector with laser-straight lines. Style: 工程师白板随手画 — whiteboard/Miro sketch."""

# ============================================================
# 1) 21:9 BANNER — TA-A 数字终端风
# ============================================================
BANNER_PROMPT = """Typography-dominant tech cover (21:9 landscape, exactly 1920x832, NOT square NOT portrait).

A late-night dev workstation scene: matte dark-navy gradient background (#0D1B2A → #1E3A5F), soft cyan glow from a monitor on the right side, scattered thin grid lines and tiny data points in #4D96FF suggesting code flowing. Foreground has subtle code snippets / terminal output in soft #B5C5D3 (highly blurred so not legible as text).

PALETTE: tech-blue — primary background #1E3A5F / #0D1B2A, text white #FFFFFF and #B5C5D3, accent #4D96FF cyan, highlight #F4A261 orange (≤10% area).

RENDERING: clean-digital — sharp 1-2px strokes, no painterly, no film grain.

FONT: display — bold geometric display typography, heavy expressive letterforms, strong visual impact.

The LARGE TITLE TEXT「我把 5 个 SKILL.md 全塞进 Claude Code 的 context，AI 跑了 8 秒就崩了」is the visual hero — enormous display characters occupying the central 50-60% of the frame, white #FFFFFF text with a 2-3px cyan #4D96FF outline / inner glow, positioned in the left 60% of the frame. Title may wrap to 2-3 lines. Title size 220-340px visual height.

The right 40% holds a single iconic data motif (a 1-0-1 binary, a glowing </> bracket, or a terminal cursor block) in #4D96FF cyan.

Below the title, a small sans-serif Chinese subtitle「5 个 Skill × 217 页 markdown × 95K token / 8 秒崩溃」 in #B5C5D3 (60% of title size), positioned directly under the title.

A tiny 8px high brand 'luoboa.com 萝卜啊' in #B5C5D3 bottom-right.

MOOD: bold — high contrast, vivid cyan against deep navy, dramatic tech-noir energy. Cinematic 4k quality, modern dev aesthetic.

CRITICAL: All Chinese characters must be SHARP and LEGIBLE, no garbling. Render the title exactly as written, every character must be readable. 220-340px visual height for the title.

NOT minimalist (NOT plain blue background with small title — that is boring and NOT a banner)."""


# ============================================================
# 2) 16:9 Content 01 — TS-B 概念关系图 — 3 个错
# ============================================================
CONTENT_01_PROMPT = CONSISTENT + """

A hand-drawn concept relationship graph showing 3 mistakes I made. 3 main mistake nodes (rounded rectangles) connected by directional arrows showing how they cascade / cause each other. Imagine an engineer sketching this on a whiteboard.

The 3 main nodes (hand-drawn boxes with charcoal #2D2D2D border, slight wobble):
- 错 1: 'context 越大 AI 越聪明' (highlighted with semi-transparent yellow #FFD93D 40% fill, the FIRST/ROOT mistake)
- 错 2: '把 Skill 当 README 写' (highlighted with semi-transparent yellow #FFD93D 40% fill, the SECOND mistake)
- 错 3: '没做 Skill 路由' (highlighted with semi-transparent yellow #FFD93D 40% fill, the THIRD mistake)

Arrows (hand-drawn charcoal #2D2D2D, slightly wobbly):
- 错 1 → 错 2 (transition arrow)
- 错 2 → 错 3 (transition arrow)
- ONE KEY transition arrow highlighted in Excalidraw blue #4D96FF (slightly thicker 3px) — the most important causal link

Below each mistake, a small 8-10pt charcoal #2D2D2D explanation in handwriting style:
- Under 错 1: '217 页 / 80% 在死亡区'
- Under 错 2: '写给人看 不是写给 AI'
- Under 错 3: 'AI 大海捞针'

A small X mark in Excalidraw blue #4D96FF at the right side of each box (indicating 'wrong'). A small text annotation near the top-right: '★ 3 个错' in handwritten Excalidraw blue.

Title at top: '我犯的 3 个错' in bold hand-written style, 22-28pt dark gray #2D2D2D.

NOT McKinsey/TED-Ed polished. NOT dark Excalidraw. Specifically: WHITE PAPER + hand-drawn lines + slight wobble + Excalidraw highlight (semi-transparent yellow #FFD93D 40% + Excalidraw blue #4D96FF)."""


# ============================================================
# 3) 16:9 Content 02 — TS-B 概念图 / 柱状图对比 — Token + 准确率
# ============================================================
CONTENT_02_PROMPT = CONSISTENT + """

A clean hand-drawn data comparison visualization showing BEFORE/AFTER Skill split. Two side-by-side horizontal bar charts drawn in a sketchy hand-drawn Excalidraw style.

LEFT side — '5 个 Skill 全在 context' (BEFORE, the BAD way):
- Big horizontal bar showing '95K Token / 217 页'
- Bar filled with light gray (representing waste)
- A small label in red/orange: 'AI 看不见 80%'
- Below: '准确率 71%' in small charcoal text

RIGHT side — '拆成 5 个独立 .md + 200 字目录' (AFTER, the GOOD way):
- Smaller horizontal bar showing '11K Token'
- Bar filled with Excalidraw blue #4D96FF (highlighting the improvement)
- A small label: '按需加载'
- Below: '准确率 88%' in small charcoal text with checkmark

A big downward arrow ↓ in the center between the two halves, in Excalidraw blue #4D96FF, with text 'Token 省 90%' / '准确率涨 30%' in handwritten style.

Title at top: '拆 vs 不拆' in bold hand-written style, 22-28pt dark gray #2D2D2D.

Subtitle below title: '面试官原话: context 能省 90%, AI 准确率能涨 30%' in 12-14pt charcoal #4A4A4A.

Two callout boxes with hand-drawn border:
- Top-left of LEFT side: '× 全量预载' in red-orange #F4A261
- Top-left of RIGHT side: '√ 按需加载' in Excalidraw blue #4D96FF

NOT McKinsey chart. NOT flat vector. Hand-drawn Excalidraw whiteboard sketch with slight wobble, semi-transparent yellow #FFD93D highlights on KEY data, charcoal #2D2D2D main lines, Excalidraw blue #4D96FF accent."""


# ============================================================
# 4) 16:9 Content 03 — TS-A 流程图 — 3 步方法
# ============================================================
CONTENT_03_PROMPT = CONSISTENT + """

A hand-drawn process flowchart showing 3 lessons I learned. 3 main step-boxes arranged top-to-bottom, connected by directional arrows. Imagine an engineer drawing this on a whiteboard to teach someone.

The 3 main step-boxes (hand-drawn rounded rectangles, slight wobble):
- Step 1 (top): '按需加载' (highlighted with semi-transparent yellow #FFD93D 40% fill — the FOUNDATION step)
  - Sub-text: 'CLAUDE.md 只留 200 字目录'
  - Sub-text: '用户输入 /skill-name 才加载'
- Step 2 (middle): 'Skill 当 AI 触发器' (highlighted with semi-transparent yellow #FFD93D 40% fill)
  - Sub-text: 'when_to_use / required_inputs'
  - Sub-text: 'expected_output / tool_chain'
- Step 3 (bottom): '别用工程量当借口' (highlighted with semi-transparent yellow #FFD93D 40% fill)
  - Sub-text: '拆 5 份 10 页 ≠ 1 份 50 页'
  - Sub-text: '后者维护难 10 倍'

Arrows (hand-drawn charcoal #2D2D2D, slightly wobbly, with arrowheads):
- Step 1 → Step 2 (one KEY transition arrow highlighted in Excalidraw blue #4D96FF, slightly thicker 3px)
- Step 2 → Step 3

A small left-side annotation in Excalidraw blue #4D96FF handwriting: '5 个 Skill 拆成 5 个 .md'

A small bottom annotation in handwriting: '实测: 95K → 11K / 71% → 88%'

Title at top: '做对 3 件事' in bold hand-written style, 22-28pt dark gray #2D2D2D.

Numbered circle (① ② ③) in Excalidraw blue #4D96FF to the left of each step box.

NOT McKinsey/TED-Ed polished flowchart. NOT dark Excalidraw. Specifically: WHITE PAPER + hand-drawn lines + slight wobble + Excalidraw highlight (semi-transparent yellow #FFD93D 40% fill on KEY boxes + Excalidraw blue #4D96FF on KEY transition arrow)."""


def main():
    # 1) Generate banner 21:9
    banner_path = os.path.join(IMAGES_DIR, "00-banner.png")
    print(f"=== Generating banner: {banner_path} ===")
    generate_cover(
        prompt=BANNER_PROMPT,
        output_path=banner_path,
        style="tech",
        article_type="tech",
    )
    print(f"OK banner: {banner_path}")

    # 2-4) Generate 3 content images 16:9
    items = [
        ("01-3个错.png", CONTENT_01_PROMPT, "01-3个错"),
        ("02-Token对比.png", CONTENT_02_PROMPT, "02-Token对比"),
        ("03-3步方法.png", CONTENT_03_PROMPT, "03-3步方法"),
    ]
    for fname, prompt, slug in items:
        out = os.path.join(IMAGES_DIR, fname)
        print(f"=== Generating {fname}: {out} ===")
        generate_section(
            prompt=prompt,
            output_path=out,
            style="tech",
            aspect_ratio="1792x1024",  # 16:9
            article_type="tech",
        )
        print(f"OK {fname}: {out}")


if __name__ == "__main__":
    main()
