import subprocess, sys, os, re, concurrent.futures, urllib.request, time

IMGDIR = r"H:/iCloudDrive/myvault/media/article/2606/0605/images"

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
                # show first 100 chars to see why
                err = re.search(r'"fail_reason":\s*"([^"]+)"', out_text)
                print(f"[{name}] attempt {attempt+1}: {err.group(1) if err else 'no url'}", file=sys.stderr)
                time.sleep(2)
                continue
            urllib.request.urlretrieve(m.group(1), out)
            return f"OK {name}"
        except Exception as e:
            print(f"[{name}] {e}", file=sys.stderr)
            time.sleep(2)
    return f"FAIL {name}"

JOBS = [
    ("00-cover-openwolf.png", "21:9",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. 6 fishhooks pulling data into a brain memory network, dollar tokens flowing in, simple sketch. Neon colors. NOT photorealistic, NOT 3D."),
    ("00-cover-glm.png", "21:9",
     "Excalidraw hand-drawn dark mode diagram, dark charcoal background. 3 rectangular model cards side by side with arrows between them, central fire icon. Neon colors. NOT photorealistic, NOT 3D."),
    ("01-mcp-问题从哪来的.png", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark background. 4x4 grid of small icons (magnifying glass, robot, globe, code symbol) with a red X overlay. Neon colors. NOT photorealistic, NOT 3D."),
    ("01-glm-DeepSeekV4.png", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark background. A long scroll banner with chain of thought loops, flame icon, counter, dollar sign. Neon orange and red. NOT photorealistic, NOT 3D."),
    ("03-glm-MiniMaxM3.png", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark background. A central window with sparse matrix pattern, 4 small icon cards (text, image, voice, video) feeding in, a small stamp icon. Neon cyan and magenta. NOT photorealistic, NOT 3D."),
    ("04-openwolf-安装.png", "1:1",
     "Excalidraw hand-drawn dark mode diagram, dark background. A simple terminal window with 3 command lines, a folder icon below. Neon green text. NOT photorealistic, NOT 3D."),
]

print(f"Retry {len(JOBS)} jobs")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    futures = {ex.submit(gen, n, p, r): n for (n, r, p) in JOBS}
    for fut in concurrent.futures.as_completed(futures):
        print(fut.result())
print("DONE")
