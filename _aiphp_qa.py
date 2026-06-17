#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI/LLM-PHP kitobi markaziy QA: kirill, BOM, font<13, cross-link, SVG XML, rasm, nav."""
import os, re, glob
import xml.etree.ElementTree as ET

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/ai-llm-php"
RASM = os.path.join(BOOK, "rasmlar")
CYR = re.compile(r"[Ѐ-ӿ]")
EXPECTED_CH = [f"{n:02d}" for n in range(1, 25)]

issues = {"cyrillic": [], "bom": [], "font": [], "img_missing": [], "xlink_missing": [],
          "xml": [], "svg_header": [], "nav": []}

def check_cyr(path, text):
    for i, line in enumerate(text.splitlines(), 1):
        for m in CYR.finditer(line):
            ch = m.group()
            issues["cyrillic"].append(f"{os.path.basename(path)}:{i} '{ch}'(U+{ord(ch):04X}) ...{line[max(0,m.start()-12):m.start()+12]}...")

md_files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
md_names = {os.path.basename(p) for p in md_files}
ch_files = sorted(glob.glob(os.path.join(BOOK, "[0-9][0-9]-*.md")))
order = [os.path.basename(f) for f in ch_files]
idx = {n: i for i, n in enumerate(order)}

for md in md_files:
    raw = open(md, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"): issues["bom"].append(os.path.basename(md))
    text = raw.decode("utf-8", "replace")
    check_cyr(md, text)
    for m in re.finditer(r"\]\((rasmlar/[^)]+\.svg)\)", text):
        if not os.path.exists(os.path.join(BOOK, m.group(1))):
            issues["img_missing"].append(f"{os.path.basename(md)} -> {m.group(1)}")
    for m in re.finditer(r"\]\((\./[^)]+\.md)\)", text):
        if not os.path.exists(os.path.join(BOOK, m.group(1)[2:])):
            issues["xlink_missing"].append(f"{os.path.basename(md)} -> {m.group(1)}")
    for m in re.finditer(r"\]\((\.\./[^)]+\.md)\)", text):
        if not os.path.exists(os.path.join(BOOK, m.group(1))):
            issues["xlink_missing"].append(f"{os.path.basename(md)} -> {m.group(1)} (tashqi)")

for ch in EXPECTED_CH:
    if not any(n.startswith(ch + "-") for n in md_names):
        issues["xlink_missing"].append(f"BOB YO'Q: {ch}")

for f in ch_files:
    name = os.path.basename(f); i = idx[name]
    text = open(f, encoding="utf-8").read()
    prev_exp = order[i-1] if i > 0 else None
    next_exp = order[i+1] if i < len(order)-1 else None
    old = re.findall(r"Oldingi:[^\]]*\]\(\.\/([0-9]{2}-[^)]+\.md)\)", text)
    nxt = re.findall(r"Keyingi:[^\]]*\]\(\.\/([0-9]{2}-[^)]+\.md)\)", text)
    if prev_exp and (not old or old[0] != prev_exp):
        issues["nav"].append(f"{name}: OLDINGI '{old[0] if old else 'YO`Q'}' != '{prev_exp}'")
    if not prev_exp and old:
        issues["nav"].append(f"{name}: birinchi bobda Oldingi bo'lmasligi kerak ({old})")
    if next_exp and (not nxt or nxt[0] != next_exp):
        issues["nav"].append(f"{name}: KEYINGI '{nxt[0] if nxt else 'YO`Q'}' != '{next_exp}'")
    if not next_exp and nxt:
        issues["nav"].append(f"{name}: oxirgi bobda Keyingi bo'lmasligi kerak ({nxt})")

svg_files = sorted(glob.glob(os.path.join(RASM, "*.svg")))
font_re = re.compile(r'font-size="([0-9.]+)"')
for svg in svg_files:
    raw = open(svg, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"): issues["bom"].append(os.path.basename(svg))
    text = raw.decode("utf-8", "replace")
    check_cyr(svg, text)
    if not text.lstrip().startswith("<svg"): issues["svg_header"].append(os.path.basename(svg)+" (svg yo'q)")
    small = [float(x) for x in font_re.findall(text) if float(x) < 13]
    if small: issues["font"].append(f"{os.path.basename(svg)}: {sorted(set(small))}")
    try: ET.fromstring(text)
    except ET.ParseError as e: issues["xml"].append(f"{os.path.basename(svg)}: {e}")

print("="*68)
print(f"MARKDOWN: {len(md_files)} | SVG: {len(svg_files)}")
print("="*68)
total = 0
labels = {"cyrillic":"KIRILL","bom":"BOM","font":"FONT<13","img_missing":"RASM YO'Q",
          "xlink_missing":"CROSS-LINK/BOB","xml":"SVG XML","svg_header":"SVG HEADER","nav":"NAVIGATSIYA"}
for k,label in labels.items():
    items = issues[k]; total += len(items)
    print(f"\n### {label}: {len(items)}")
    for it in items[:60]: print("  -", it)
    if len(items) > 60: print(f"  ... +{len(items)-60}")
print("\n" + "="*68); print(f"JAMI MUAMMO: {total}"); print("="*68)
