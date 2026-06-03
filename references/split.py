import re

with open(r'H:\iCloudDrive\myvault\media\answer\2606\0603\AI 会走蒸汽机革命先野蛮生长，再瓦特改效率，最后卡诺建理论的老路吗？.md', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
text = re.sub(r'[#*`>|_\-\[\]\(\)!]', '', text)
text = re.sub(r'📌.*?\n', '', text)
text = re.sub(r'确认问题：.*?\n', '', text)

sents = re.split(r'[。！？\n]+', text)
sents = [s.strip() for s in sents if s.strip() and len(s.strip()) >= 3]

result = []
for s in sents:
    if len(s) <= 50:
        result.append(s)
    else:
        cut = s[:50]
        last_comma = cut.rfind('，')
        if last_comma > 20:
            result.append(s[:last_comma])
            rest = s[last_comma + 1:].strip()
            if len(rest) >= 3:
                result.append(rest)
        else:
            result.append(cut + '...')

print(f'Total: {len(result)} sentences')
for i, s in enumerate(result, 1):
    print(f'{i:02d} [{len(s):2d}] {s}')
