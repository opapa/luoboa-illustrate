#!/usr/bin/env python
"""Fix image anchor placement in all 9 zhihu answer articles.

For each article:
- Find body lines (skip H1 title, skip signoff, skip ## 参考 section)
- Insert 3 images at 30%, 55%, 80% positions of body content
- Remove any existing image references before re-inserting
"""
import os

ART_DIR = r"H:\iCloudDrive\myvault\media\answer\2606\0609"

ARTICLES = [
    ("q1-anthropic", "Anthropic 呼吁全球暂缓前沿 AI 研发，这反映了人工智能领域怎样的担忧？-知乎回答.md"),
    ("q2-pricing", "GPT-5.5 涨价，而DeepSeek 再次降价？为什么会同时出现「涨价」和「降价」共存的情况？-知乎回答.md"),
    ("q3-weird-images", "GPT为什么会生成这么诡异的图片？有没有研究者能解释为什么会出现这一现象？-知乎回答.md"),
    ("q4-skills-mcp", "为什么 skills 优于 mcp-知乎回答.md"),
    ("q5-opc", "你看好超级个体，一人公司（OPC）吗？为什么？-知乎回答.md"),
    ("q6-agent-workflow", "大模型 Agent 和 workflow 的区别在哪里？-知乎回答.md"),
    ("q7-tool-use", "大模型为什么可以调用工具？-知乎回答.md"),
    ("q8-tech-leader", "搞技术的人员为什么通常当不了领导？-知乎回答.md"),
    ("q9-gaokao", "有哪些当年只道寻常，现在却再也回不去的全民高考记忆？-知乎回答.md"),
]


def fix_article(article_key, file_name):
    path = os.path.join(ART_DIR, file_name)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")

    # Find signoff marker (---) line
    signoff_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            signoff_idx = i
            break

    # Find "## 参考" heading
    ref_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## 参考") or line.strip().startswith("##参考"):
            ref_idx = i
            break

    # Body content cutoff: earliest of signoff or ref_idx
    cutoff = signoff_idx if signoff_idx is not None else len(lines)
    if ref_idx is not None and ref_idx < cutoff:
        cutoff = ref_idx

    # Build content indices (real content lines in body)
    content_indices = []
    for idx, line in enumerate(lines):
        if idx >= cutoff:
            break
        s = line.strip()
        if not s:
            continue
        if s.startswith("![") and "images/" in s:
            continue
        if s.startswith("#"):
            continue
        if s == "---":
            continue
        content_indices.append((idx, line))

    n = len(content_indices)
    if n < 3:
        print(f"  SKIP {article_key}: only {n} content lines")
        return False

    # Anchor positions: 30%, 55%, 80% of body content
    anchor_indices = []
    for frac in [0.30, 0.55, 0.80]:
        target = int(n * frac)
        target = max(0, min(n - 1, target))
        anchor_line_idx = content_indices[target][0]
        anchor_indices.append(anchor_line_idx)

    # Remove all existing image lines
    new_lines = []
    for line in lines:
        s = line.strip()
        if s.startswith("![") and "images/" in s:
            continue
        new_lines.append(line)

    # Build orig_idx -> new_idx map
    orig_to_new = {}
    new_idx = 0
    for orig_idx, line in enumerate(lines):
        s = line.strip()
        if s.startswith("![") and "images/" in s:
            continue
        orig_to_new[orig_idx] = new_idx
        new_idx += 1

    # Build insertions list (descending by position to keep indices valid)
    insertions = []
    for k, anchor_orig_idx in enumerate(anchor_indices):
        if anchor_orig_idx in orig_to_new:
            new_pos = orig_to_new[anchor_orig_idx] + 1  # insert AFTER
        else:
            # pick nearest forward
            new_pos = None
            for cand in sorted(orig_to_new.keys()):
                if cand >= anchor_orig_idx:
                    new_pos = orig_to_new[cand] + 1
                    break
            if new_pos is None:
                new_pos = len(new_lines)  # fallback
        img_rel = f"images/{article_key}-{k+1:02d}.png"
        insertions.append((new_pos, img_rel))

    insertions.sort(key=lambda x: x[0], reverse=True)
    for pos, img in insertions:
        new_lines.insert(pos, f"![]({img})")
        new_lines.insert(pos, "")

    # Collapse 3+ consecutive blank lines
    cleaned = []
    blank_run = 0
    for line in new_lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 2:
                cleaned.append(line)
        else:
            blank_run = 0
            cleaned.append(line)

    new_text = "\n".join(cleaned)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"  OK {article_key}: anchors at lines {anchor_indices} (of {n} body lines)")
    return True


if __name__ == "__main__":
    for key, fn in ARTICLES:
        fix_article(key, fn)
