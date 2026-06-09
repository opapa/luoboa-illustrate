#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate ReelClaw article 21:9 banner v2 — display font + dense Excalidraw background.

5-dim LOCKED (do NOT re-select):
- Type: typography-dominant
- Palette: excalidraw (white #FFFFFF + dark gray #2D2D2D + blue #4D96FF/#056DE8
  + yellow #FFD93D 40% + minimal orange #F4A261 + purple-red #9B59B6)
- Rendering: hand-drawn (wobble + uneven corners + shaky arrows)
- Font: display 粗体装饰 (NOT clean / 思源黑体)
- Mood: balanced-technical
- Aspect: 21:9 / 1920x832

Hua-zi techniques LOCKED:
- highlight: 黄色 #FFD93D 40% on 主标题「代价」二字
- stroke-text: 1.5-2px black #2D2D2D stroke on all title characters
"""
import os
import sys

SKILL_DIR = r"C:\Users\opapa\.claude\skills\luoboa-illustrate"
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from generate import generate_cover  # noqa: E402

OUTPUT_PATH = r"H:\iCloudDrive\myvault\media\article\2606\0608\images\00-banner.png"

# ===== Locked 5-dim prompt — display font + dense Excalidraw background =====
BANNER_PROMPT = """A 21:9 ultra-wide banner (3200x1370 px) on pure white #FFFFFF background,
densely filled with hand-drawn Excalidraw-style elements covering 60-80%
of the canvas. The whole image looks like an engineer's whiteboard filled
with sketches.

FONT APPLICATION (CRITICAL — must be rendered as bold decorative display,
NOT plain sans-serif, NOT Song-style):
Use bold decorative display typography with strong visual impact. Heavy
expressive letterforms with thick-thin contrast. The title characters
must feel like art-poster display, not plain sans-serif, not Song-style
typeface. Each character should have weight variation, slight ink bleed,
and decorative impact. Apply a 1.5-2px black stroke outline (#2D2D2D) to
all title characters for poster visibility. Highlight the key reversal
word「代价」with a yellow marker highlight (#FFD93D, 40% opacity)
covering 70-80% of the character area with irregular hand-drawn edges.

PALETTE: white #FFFFFF base, dark gray #2D2D2D main strokes, blue #4D96FF
and #056DE8 highlights, yellow #FFD93D 40% transparency highlights,
minimal warm orange #F4A261 and purple-red #9B59B6 accents. No dark
background.

RENDERING: hand-drawn Excalidraw. Wobbly lines, uneven box corner radii,
trembling arrows, sketchy connectors, slight ink bleed on strokes. NOT
clean-digital, NOT flat-vector, NOT photo, NOT 3D, NOT watercolor.

MOOD: balanced-technical, engineer's whiteboard aesthetic.

MAIN TITLE (Chinese, must be sharp and readable, font-size 280-320px,
embeds into the hand-drawn background, not floating on it):
「我把 ReelClaw 接进了视频号，第一周产 11 条爆款，第二周我才看清它要什么代价」

SUBTITLE (60% of main title size, font-size 170-190px):
「AI 视频 · 一键成片不是一键省钱」

EXCALIDRAW BACKGROUND ELEMENTS (must cover 60-80% of canvas):
- Left third: 6 hand-drawn boxes (uneven rounded corners) labeled
  "ReelClaw 输入：选题", "主 Agent 调度", "6 个子 Agent 并行", "重生成 30%",
  "成片", "真人审稿 ✗", connected with wobbly hand-drawn arrows
- Center: hand-written giant "1.7 亿 Token" with yellow starburst + ⚡
- Right third: hand-drawn decision tree
  "内容是剧本型？"→是→"ReelClaw 跑得动 ✓"
  →否→"Vlog/日常 ✗ 翻车"
- Top-left: explosion box "11 条爆款" with blue highlight
- Top-right: lightbulb "杠杆工具" with yellow highlight
- Bottom-left: equation "1.7亿 × 0.08元/1K = 2.4万" with red underline
- Bottom-right: battery icon "1880/月" with blue highlight
- Top: timeline "3.21 接 → 3.25 第一条 → 3.30 账单"
- Bottom: large red "1.8 万净亏 ✗"
- Scattered: hand-drawn circles around keywords (11, 1.7亿, 2.4万, 3 剪辑师),
  checkmarks ✓ and crosses ✗, question marks ?, exclamation marks !
- 3-4 comment boxes with hand-written text:
  "真实消耗是标称的 5-10 倍", "AI 跑了 3-5 遍才交出来", "裁 1 个剪辑师 ≠ 省 6000"

TITLE-BACKGROUND INTERACTION (NOT floating, MUST integrate):
- A wobbly hand-drawn connector line crosses through the title's "爆款"
  characters (visually "interrupting" 爆款 to introduce the reversal)
- Yellow marker highlight on "代价" extends to the right toward a
  hand-drawn circle around "看清它要什么"
- An arrow from "1.8 万净亏" points directly at the title's "代价"
- "1.7 亿" hand-written big text slightly overlaps with "11 条爆款"
  (suggesting 爆款 and 代价 coexist)
- Timeline at top extends through the bottom of the title across the canvas
- "ReelClaw" brand name appears in the title as hand-written large text
  with blue highlight

WATERMARK: "luoboa.com 萝卜啊" in 8pt light gray #B0B0B0 at bottom-right corner.

Layout: typography-dominant, title 60-70% visual weight, with hand-drawn
Excalidraw elements densely filling the background around and behind the title.

All Chinese characters must be SHARP and LEGIBLE, no garbling, no missing
characters. Display typography is bold decorative with thick-thin contrast,
NOT plain sans-serif, NOT Song-style typeface. 21:9 cinematic widescreen."""


def main():
    print(f"=== Generating ReelClaw banner v2 ===")
    print(f"Output: {OUTPUT_PATH}")
    print(f"5-dim LOCKED: typography-dominant / excalidraw / hand-drawn / display / balanced-technical")
    print(f"Backend: API (grsai) / article_type=tech / brand=luoboa (auto)")

    generate_cover(
        prompt=BANNER_PROMPT,
        output_path=OUTPUT_PATH,
        style="tech",
        article_type="tech",
    )
    print(f"\nOK: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
