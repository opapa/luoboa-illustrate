#!/usr/bin/env python3
"""Batch generate images via dreamina CLI. Concurrency=4 to avoid rate limit."""
import subprocess, sys, os, re, json, time, concurrent.futures, urllib.request

IMGDIR = r"H:/iCloudDrive/myvault/media/article/2606/0605/images"
os.makedirs(IMGDIR, exist_ok=True)

def gen(name, prompt, ratio):
    out = os.path.join(IMGDIR, name)
    if os.path.exists(out) and os.path.getsize(out) > 100000:
        return f"SKIP {name}"
    for attempt in range(2):
        try:
            r = subprocess.run(
                ["dreamina", "text2image",
                 "--prompt=" + prompt,
                 f"--ratio={ratio}",
                 "--resolution_type=2k",
                 "--model_version=high_aes_general_v50",
                 "--poll=120"],
                capture_output=True, text=True, timeout=300
            )
            out_text = r.stdout + r.stderr
            m = re.search(r'"image_url":\s*"(https://[^"]+)"', out_text)
            if not m:
                print(f"[{name}] attempt {attempt+1}: no url, first 200 chars: {out_text[:200]}", file=sys.stderr)
                continue
            url = m.group(1)
            urllib.request.urlretrieve(url, out)
            sz = os.path.getsize(out)
            if sz < 50000:
                print(f"[{name}] too small {sz}, retry", file=sys.stderr)
                continue
            return f"OK {name} {sz} bytes"
        except Exception as e:
            print(f"[{name}] attempt {attempt+1}: {e}", file=sys.stderr)
            time.sleep(3)
    return f"FAIL {name}"

JOBS = [
    # Article 2 - OpenWolf
    ("00-cover-openwolf.png", "21:9", "Excalidraw dark mode hand-drawn diagram on dark charcoal background. 6 colorful hooks/fishhooks connecting to a giant brain-shape memory network above a Claude Code terminal window, dollar signs and tokens floating around getting absorbed by the network. Show data flow: arrows pointing INTO the brain, smaller Chinese text 'anatomy.md cerebrum.md buglog.json token-ledger.json'. Hand-drawn wobbly lines, neon accent colors (cyan, magenta, yellow, lime green), whiteboard marker strokes. 21:9 aspect ratio. NOT photorealistic, NOT 3D."),
    # Article 3 - GLM/DS4/M3
    ("00-cover-glm.png", "21:9", "Excalidraw dark mode hand-drawn diagram on dark charcoal background. Three labeled rectangular cards in a row representing three Chinese AI models: GLM-5.1 (left), DeepSeek V4 (center with token fire burning), MiniMax M3 (right with phone+voice+image icons). Arrows between them showing the 'main model' choice shift. Big red Chinese text '2亿 tokens' with fire in center. Hand-drawn wobbly lines, neon accent colors (cyan, magenta, yellow, orange), whiteboard marker strokes. 21:9 aspect ratio. NOT photorealistic, NOT 3D."),

    # Article 1 sections
    ("01-mcp-问题从哪来的.png", "1:1", "Excalidraw dark mode hand-drawn diagram. Four columns labeled in Chinese (搜索类 / 爬取类 / 浏览器类 / 专用类), each with 4 small icons (magnifying glass, robot, globe, code brackets) representing MCP tools. Total 16 icons in a grid. A big red X over the grid, with caption '4 大类 16 个 MCP 工具'. Dark charcoal background, neon accent colors, hand-drawn wobbly lines. 1:1 square aspect ratio. NOT photorealistic, NOT 3D."),
    ("02-mcp-202K怎么吃光的.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A horizontal bar chart showing token consumption growing across 5 rounds: round 1 80K, round 2 130K, round 3 155K, round 4 180K, round 5 EXPLOSION with red star. Arrow showing fixed cost 80K plus growing dynamic cost each round. Caption '5 轮就炸'. Dark charcoal background, neon cyan and red accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("03-mcp-真正烧context的.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A large browser window showing raw markdown content filling 60% of the screen, with red 'PERMANENT' stamp and a ghost icon showing the content cannot be deleted. Side note '爬一个 20K 爬两个 40K 爬三个 60K'. Dark charcoal background, neon red and cyan accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("04-mcp-改法.png", "1:1", "Excalidraw dark mode hand-drawn diagram. Two boxes side by side: LEFT labeled '改之前 主对话直接吃' with mountain of content, RIGHT labeled '改之后 子代理隔离' with small clean summary flowing into a smaller main context. Arrow showing '子代理用完即释放'. Dark charcoal background, neon green and cyan accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("05-mcp-几个教训.png", "1:1", "Excalidraw dark mode hand-drawn diagram. Three short checklist items in Chinese with red warning icons: 'MCP 工具不是越多越好' / '爬取结果必须隔离子代理' / '写 Skill 之前先算 token 账'. Each as a hand-drawn sticky note with a red exclamation mark. Dark charcoal background, neon yellow and red accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),

    # Article 2 - OpenWolf sections
    ("01-openwolf-它怎么工作的.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A timeline showing Claude Code work flow with 6 hook points marked as colored hooks/clips at different stages (pre, during, post). Arrows showing data flow into a '.wolf/' folder box containing 4 file cards: 'anatomy.md', 'cerebrum.md', 'buglog.json', 'token-ledger.json'. Hand-drawn wobbly lines, dark charcoal background, neon cyan/magenta accents. 1:1 square. NOT photorealistic."),
    ("02-openwolf-效果实测.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A two-column comparison: LEFT column labeled '裸 Claude CLI' with bars showing 250万 tokens and $1.25 cost, RIGHT column labeled 'OpenWolf + Claude' with shorter bars showing 42.5万 tokens and $0.43 cost. Big green downward arrow between them labeled '省 65%'. Dark charcoal background, neon red on left and neon green on right, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("03-openwolf-优点和坑.png", "1:1", "Excalidraw dark mode hand-drawn diagram. Split layout: LEFT side '优点' (Pros) with 3 green checkmark sticky notes (省钱, 省心, 省力). RIGHT side '坑' (Cons) with 3 red warning sticky notes (工具还年轻, 估算有偏差, 依赖 Claude 生态). Each sticky note has a hand-drawn icon. Dark charcoal background, neon green/red accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("04-openwolf-安装.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A terminal window showing 3 commands: 'npm install -g openwolf' / 'openwolf init' / 'claude'. Below the terminal, a folder icon labeled '.wolf/' with a small 'memory' badge. Hand-drawn wobbly lines, dark charcoal background, neon green accent for terminal text, white/cyan accents. 1:1 square. NOT photorealistic."),
    ("05-openwolf-用下来.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A simple conclusion visual: a hand-drawn brain/lightbulb icon with speech bubble saying '会话变短 + 账单变好看'. Arrow pointing right to text '值得装一下'. Dark charcoal background, neon yellow and cyan accents, hand-drawn wobbly lines, simple and clean. 1:1 square. NOT photorealistic."),

    # Article 3 - GLM/DS4/M3 sections
    ("01-glm-DeepSeekV4.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A long horizontal scroll/banner showing 'DeepSeek V4 半天烧了 2 亿 token'. A flame icon with a counter showing '2亿'. A thinking bubble with chain-of-thought text being amplified many times. Small footnote '$1,066,426 YC-Bench extreme case'. Dark charcoal background, neon orange/red fire accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("02-glm-GLM5.1.png", "1:1", "Excalidraw dark mode hand-drawn diagram. Three tiered boxes labeled 'Lite' (80 prompts), 'Pro' (400 prompts), 'Max' (1600 prompts), with a red '3x peak hours' multiplier stamp. Below: a hand with '抢不到' speech bubble. Right side: 100% completion bar labeled '编码完成度 100%'. Dark charcoal background, neon red/yellow/cyan accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("03-glm-MiniMaxM3.png", "1:1", "Excalidraw dark mode hand-drawn diagram. Center: a 1M context window with MSA sparse pattern (gaps in the matrix). Around it: 4 small icon cards (text, image, voice, video) feeding into the window, labeled '多模态'. Bottom: a code review stamp labeled '每改必看' (must check every change). Dark charcoal background, neon cyan/magenta/green accents, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("04-glm-三个模型怎么排.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A 2x2 matrix/quadrant chart. Top-left '纯编码': GLM 5.1 > V4 > M3. Bottom-right '多模态+长上下文': M3 > V4 > GLM 5.1. Each cell has a small model icon and ranking arrows. Dark charcoal background, neon 4 different colors per quadrant, hand-drawn wobbly lines. 1:1 square. NOT photorealistic."),
    ("05-glm-接下来Kimi.png", "1:1", "Excalidraw dark mode hand-drawn diagram. A 'next experiment' themed visual: a magnifying glass over a 'Kimi K2.6' card with 'Agent Swarm 300 agents' badge. Arrows pointing to a '?' mark with a hopeful '?' speech bubble. Dark charcoal background, neon purple and yellow accents, hand-drawn wobbly lines, exploration theme. 1:1 square. NOT photorealistic."),
]

print(f"Total jobs: {len(JOBS)}")
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futures = {ex.submit(gen, name, p, r): name for (name, r, p) in JOBS}
    for fut in concurrent.futures.as_completed(futures):
        print(fut.result())

print("DONE")
