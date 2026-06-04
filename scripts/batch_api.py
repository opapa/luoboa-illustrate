#!/usr/bin/env python3
"""Batch generate via API (grsai gpt-image-2) with brand watermark."""
import subprocess, sys, os, concurrent.futures, time

SKILL_DIR = r"C:/Users/opapa/.claude/skills/luoboa-illustrate"
IMGDIR = r"H:/iCloudDrive/myvault/media/article/2606/0605/images"
GEN = os.path.join(SKILL_DIR, "scripts", "generate.py")

def gen(name, prompt, mode, ratio):
    out = os.path.join(IMGDIR, name)
    if os.path.exists(out) and os.path.getsize(out) > 100000:
        return f"SKIP {name}"
    size = "1920x832" if ratio == "21:9" else "1024x1024"
    for attempt in range(2):
        try:
            cmd = ["python", GEN, mode,
                   "--style", "tech",
                   "--prompt", prompt,
                   "--output", out]
            if mode == "section":
                cmd.extend(["--size", size])
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 100000:
                return f"OK {name}"
            print(f"[{name}] attempt {attempt+1}: rc={r.returncode} stderr={r.stderr[:200]}", file=sys.stderr)
            time.sleep(3)
        except Exception as e:
            print(f"[{name}] {e}", file=sys.stderr)
            time.sleep(3)
    return f"FAIL {name}"

JOBS = [
    # === Covers (21:9) ===
    ("00-cover-openwolf.png", "cover", "21:9",
     "Excalidraw hand-drawn dark mode diagram on dark charcoal background. 6 colorful hooks/fishhooks connecting to a giant brain-shape memory network above a Claude Code terminal window, dollar signs and tokens floating around being absorbed by the network. Show 4 file cards: anatomy.md, cerebrum.md, buglog.json, token-ledger.json. Hand-drawn wobbly lines, neon accent colors (cyan, magenta, yellow, lime green), whiteboard marker strokes. 21:9 widescreen. NOT photorealistic, NOT 3D."),
    ("00-cover-glm.png", "cover", "21:9",
     "Excalidraw hand-drawn dark mode diagram on dark charcoal background. 3 rectangular cards side by side representing three Chinese AI models: GLM-5.1 (left), DeepSeek V4 (center with token fire burning), MiniMax M3 (right with phone+voice+image icons). Arrows between them showing main-model shift. Big text 2 hundred million tokens with fire in center. Hand-drawn wobbly lines, neon accent colors (cyan, magenta, yellow, orange), whiteboard marker strokes. 21:9 widescreen. NOT photorealistic, NOT 3D."),

    # === Article 1 - MCP sections (1:1) ===
    ("01-mcp-问题从哪来的.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A 4x4 grid of small tool icons (magnifying glass, robot, globe, code brackets) labeled with 4 categories at top: Search / Crawl / Browser / Special. A big red X over the grid with caption '4 categories 16 MCP tools'. Hand-drawn wobbly lines, neon red and cyan accents. 1:1 square. NOT photorealistic, NOT 3D."),
    ("02-mcp-202K怎么吃光的.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A horizontal bar chart showing token consumption growing across 5 rounds: 80K, 130K, 155K, 180K, then EXPLOSION with red star at the end. Arrow showing fixed cost 80K plus growing dynamic cost each round. Caption 'BOOM at round 5'. Neon cyan and red accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("03-mcp-真正烧context的.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A large browser window showing raw markdown content filling 60% of the screen, with red PERMANENT stamp and a ghost icon showing the content cannot be deleted. Side note 'one page 20K two pages 40K three pages 60K'. Neon red and cyan accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("04-mcp-改法.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. Two boxes side by side: LEFT labeled 'Before main thread eats everything' with mountain of content, RIGHT labeled 'After sub-agent isolation' with small clean summary flowing into a smaller main context. Arrow showing 'sub-agent released after done'. Neon green and cyan accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("05-mcp-几个教训.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. 3 short checklist items as hand-drawn sticky notes with red warning icons: 'MCP tools: less is more' / 'Scrape results must be isolated to sub-agent' / 'Calculate token budget before writing Skill'. Each sticky note with red exclamation mark. Neon yellow and red accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),

    # === Article 2 - OpenWolf sections (1:1) ===
    ("01-openwolf-它怎么工作的.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A timeline showing Claude Code work flow with 6 hook points marked as colored hooks/clips at different stages (pre, during, post). Arrows showing data flow into a '.wolf/' folder box containing 4 file cards: anatomy.md, cerebrum.md, buglog.json, token-ledger.json. Neon cyan/magenta accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("02-openwolf-效果实测.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A two-column comparison: LEFT 'Plain Claude CLI' with bars showing 2.5M tokens and $1.25 cost, RIGHT 'OpenWolf + Claude' with shorter bars showing 425K tokens and $0.43 cost. Big green downward arrow between labeled 'save 65-80%'. Neon red on left, neon green on right, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("03-openwolf-优点和坑.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. Split layout: LEFT 'Pros' with 3 green checkmark sticky notes (save money, save effort, save time). RIGHT 'Cons' with 3 red warning sticky notes (tool still young, estimation off, dependent on Claude ecosystem). Hand-drawn icons, neon green/red accents, wobbly lines. 1:1 square. NOT photorealistic."),
    ("04-openwolf-安装.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A terminal window showing 3 commands: npm install / openwolf init / claude. Below the terminal, a folder icon labeled .wolf/ with a small memory badge. Neon green terminal text, cyan accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("05-openwolf-用下来.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A simple conclusion visual: a hand-drawn brain/lightbulb icon with speech bubble saying 'shorter sessions + lower bill'. Arrow pointing right to text 'worth installing'. Neon yellow and cyan accents, hand-drawn wobbly lines, clean and simple. 1:1 square. NOT photorealistic."),

    # === Article 3 - GLM/DS4/M3 sections (1:1) ===
    ("01-glm-DeepSeekV4.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A long horizontal scroll banner showing 'DeepSeek V4 burned 200 million tokens in half day'. A flame icon with a counter, chain-of-thought text being amplified many times. Small footnote 'extreme YC-Bench case 1 million dollars'. Neon orange/red fire accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("02-glm-GLM5.1.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. 3 tiered boxes labeled Lite (80 prompts), Pro (400 prompts), Max (1600 prompts), with a red '3x peak hours' multiplier stamp. Below: a hand with 'sold out' speech bubble. Right side: 100% completion bar labeled 'coding completion 100%'. Neon red/yellow/cyan accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("03-glm-MiniMaxM3.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. Center: a 1M context window with sparse matrix pattern (gaps). Around it: 4 small icon cards (text, image, voice, video) feeding in, labeled 'multimodal'. Bottom: a code review stamp labeled 'must check every change'. Neon cyan/magenta/green accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("04-glm-三个模型怎么排.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A 2x2 matrix quadrant chart. Top-left 'coding only': GLM 5.1 > V4 > M3. Bottom-right 'multimodal + long context': M3 > V4 > GLM 5.1. Each cell has a small model icon and ranking arrows. 4 different neon colors per quadrant, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("05-glm-接下来Kimi.png", "section", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. A next-experiment themed visual: a magnifying glass over a 'Kimi K2.6' card with 'Agent Swarm 300 agents' badge. Arrows pointing to a question mark with hopeful speech bubble. Neon purple and yellow accents, hand-drawn wobbly lines, exploration theme. 1:1 square. NOT photorealistic."),
]

print(f"Total jobs: {len(JOBS)}")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    futures = {ex.submit(gen, n, p, m, r): n for (n, m, r, p) in JOBS}
    for fut in concurrent.futures.as_completed(futures):
        print(fut.result())
print("DONE")
