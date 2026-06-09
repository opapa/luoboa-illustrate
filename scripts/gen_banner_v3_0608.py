#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate 0608 SKILL.md article 21:9 banner v3.

v2 失败的根因：手绘区域画了大量文字标签（"SKILL.md #1-#5"、"217 页"等 20+ 个文字），跟主标题抢戏。
v3 核心修复：
  1. 手绘元素只画形状，不带任何文字标签 — box/icon/arrow/连接线都不带字
  2. 主标题字号 350-400px（v2 是 280-320px）— 显著加大
  3. 标题视觉占比 70-80%（v2 是 60-70%）— 标题是绝对主角
  4. 整体"标题为主 + 手绘为辅" — 多形状 OK，但形状里不带字
  5. 关键词高亮保留：黄底「5 个 SKILL.md」、红/橙底「8 秒就崩了」、蓝 wobbly underline on 标题词

5-dim LOCKED（不重新选型）:
- Type: typography-dominant
- Palette: excalidraw (白 + 深灰 + 蓝/黄高亮 + 极少量橙/紫红)
- Rendering: hand-drawn (wobble + 不齐圆角 + 手抖箭头)
- Font: display 粗体装饰
- Mood: balanced-technical
- Aspect: 21:9 / 1920x832
"""
import os
import sys

SKILL_DIR = r"C:\Users\opapa\.claude\skills\luoboa-illustrate"
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from generate import generate_cover  # noqa: E402

OUTPUT_PATH = r"H:\iCloudDrive\myvault\media\article\2606\0608\我把 SKILL.md 全塞进 context 了，面试官看了直摇头\images\00-banner.png"

# ===== v3 Prompt: 标题大 70-80% 视觉占比 + 手绘无字 =====
BANNER_PROMPT = """A 21:9 ultra-wide banner (3200x1370 px) on pure white #FFFFFF background.
The title is the absolute visual hero — typography-dominant 70-80% of
visual weight, huge 350-400px bold decorative display Chinese
characters, occupying the central 60-70% of the frame. The title
is embedded INTO a hand-drawn Excalidraw background.

FONT APPLICATION (CRITICAL — must be rendered as bold decorative display,
NOT plain sans-serif, NOT Song-style):
Use bold decorative display typography with strong visual impact.
Heavy expressive letterforms with thick-thin contrast. The title
characters must feel like art-poster display, not plain sans-serif,
not Song-style typeface. Each character should have weight variation,
slight ink bleed, and decorative impact. Apply a 1.5-2px black stroke
outline (#2D2D2D) to all title characters for poster visibility.
Highlight「5 个 SKILL.md」with a yellow marker highlight (#FFD93D,
40% opacity) covering 70-80% of the character area with irregular
hand-drawn edges. Highlight「8 秒就崩了」with a red/orange marker
highlight (#F4A261 + red, 40% opacity).

PALETTE: white #FFFFFF base, dark gray #2D2D2D main strokes, blue
#4D96FF and #056DE8 highlights, yellow #FFD93D 40% transparency
highlights, minimal warm orange #F4A261 and purple-red #9B59B6 accents
(<=5% area each). No dark background.

RENDERING: hand-drawn Excalidraw. Wobbly lines, uneven box corner
radii, trembling arrows, sketchy connectors, slight ink bleed on
strokes. NOT clean-digital, NOT flat-vector, NOT photo, NOT 3D,
NOT watercolor.

MOOD: balanced-technical, engineer's whiteboard aesthetic.

MAIN TITLE (Chinese, font-size 350-400px, very large, occupies central
60-70% of the frame, embedded into the hand-drawn background, NOT
floating on it, must be the absolute visual hero):
「我把 5 个 SKILL.md 全塞进 Claude Code 的 context，AI 跑了 8 秒就崩了」

SUBTITLE (60% of main title size, font-size 210-240px):
「5 个 Skill × 217 页 markdown × 95K token / 8 秒崩溃」

EXCALIDRAW BACKGROUND (must fill 50-70% of canvas BUT be SHAPES ONLY —
NO text labels inside any shape, no words anywhere in the background,
only hand-drawn shapes/icons/arrows/connectors/highlights):
- Left third: 5 hand-drawn empty document/file icon shapes (small
  rectangles representing files, with NO text inside or labels),
  stacked or scattered, with wobbly arrows connecting them
  (representing "5 SKILL files being loaded")
- Center-left: hand-drawn empty giant rectangular "context window"
  shape (representing context overflow, NO text inside, just an
  empty rectangle with a smaller filled section representing
  "effective attention")
- Center: hand-drawn empty comparison — 2 small empty shapes with
  a wobbly downward arrow between them (representing "95K to 11K
  decrease", NO numbers/text on the shapes)
- Right third: hand-drawn empty comparison split —
  TOP: empty shape with red X mark (representing "full load bad")
  BOTTOM: empty shape with green check (representing "lazy load good")
  NO text in any shape
- Corners: hand-drawn empty shapes — Claude Code terminal box
  (top-left, with X inside but NO text label), ruler/scale shape
  (top-right, with tick marks but NO numbers), empty comparison
  bar pair (bottom-left, 2 empty bars one tall one short),
  question/lightbulb shape (bottom-right)
- Scattered throughout: empty yellow highlight boxes (rounded
  rectangles with NO text), empty blue circle highlights, hand-drawn
  check cross question exclamation icons, hand-drawn starbursts,
  hand-drawn small arrows connecting things
- Multiple visual layers overlapping and connected, like a real
  whiteboard with several intertwined shapes
- Background elements must be VISUALLY RECESSED — slightly
  desaturated or smaller in scale — so the title clearly
  dominates

TITLE-BACKGROUND INTERACTION (NOT floating, MUST integrate):
- A wobbly hand-drawn arrow crosses through the title's "context"
  characters pointing to the empty context window box (visually
  illustrating context overflow)
- Yellow marker highlight on "5 个 SKILL.md" extends to the left
  toward the 5 empty file icon shapes
- Red marker highlight on "8 秒就崩了" connects to the top-left
  empty Claude Code terminal shape (with X inside)
- "context" word's blue wobbly underline connects to the empty
  context window shape

WATERMARK: "luoboa.com 萝卜啊" in 8pt light gray #B0B0B0 at
bottom-right corner.

CRITICAL CONSTRAINT — BACKGROUND MUST HAVE NO TEXT:
The hand-drawn Excalidraw background contains ONLY shapes, icons,
arrows, and graphic symbols. NO Chinese characters, NO English
words, NO numbers, NO text labels anywhere in the background.
The only text in the entire image is the MAIN TITLE and SUBTITLE
(plus the tiny corner watermark). Every box/diamond/circle in the
background is EMPTY — they are pure visual shapes representing
files / context window / comparison / process flow, not labeled
diagrams.

Layout: typography-dominant, title 70-80% visual weight, with
hand-drawn Excalidraw SHAPES (NOT labeled diagrams) filling the
background around and behind the title. The title is the clear
visual hero; the background recedes visually."""


def main():
    print(f"=== Generating 0608 SKILL.md banner v3 ===")
    print(f"Output: {OUTPUT_PATH}")
    print(f"5-dim LOCKED: typography-dominant / excalidraw / hand-drawn / display / balanced-technical")
    print(f"Backend: API (grsai) / article_type=tech / brand=luoboa (auto)")
    print(f"v3 关键修复: 手绘无字 + 标题字号 350-400px + 视觉占比 70-80%")

    generate_cover(
        prompt=BANNER_PROMPT,
        output_path=OUTPUT_PATH,
        style="tech",
        article_type="tech",
    )
    print(f"\nOK: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
