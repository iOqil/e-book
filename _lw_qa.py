#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Livewire kitobi markaziy QA: kirill, BOM, font<13, cross-link, SVG XML, rasm havolalari."""
import os, re, glob
import xml.etree.ElementTree as ET

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/livewire"
RASM = os.path.join(BOOK, "rasmlar")

# Kirill diapazoni U+0400..U+04FF (lekin o' g' uchun ishlatiladigan ' apostroflar lotin)
CYR = re.compile(r"[Ѐ-ӿ]")

issues = {"cyrillic": [], "bom": [], "font": [], "img_missing": [], "xlink_missing": [],
          "xml": [], "svg_header": [], "raw_lt": []}

EXPECTED_CH = [f"{n:02d}" for n in range(1, 27)]

def check_cyrillic(path, text):
    for i, line in enumerate(text.splitlines(), 1):
        for m in CYR.finditer(line):
            ch = m.group()
            issues["cyrillic"].append(f"{os.path.basename(path)}:{i}  '{ch}' (U+{ord(ch):04X})  ...{line[max(0,m.start()-15):m.start()+15]}...")

# --- Markdown fayllar ---
md_files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
md_names = {os.path.basename(p) for p in md_files}
for md in md_files:
    raw = open(md, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        issues["bom"].append(os.path.basename(md))
    text = raw.decode("utf-8", "replace")
    check_cyrillic(md, text)
    # rasm havolalari ](rasmlar/xxx.svg)
    for m in re.finditer(r"\]\((rasmlar/[^)]+\.svg)\)", text):
        rel = m.group(1)
        if not os.path.exists(os.path.join(BOOK, rel)):
            issues["img_missing"].append(f"{os.path.basename(md)} -> {rel}")
    # cross-link ](./NN-xxx.md) yoki (./README.md)
    for m in re.finditer(r"\]\((\./[^)]+\.md)\)", text):
        rel = m.group(1)[2:]
        if not os.path.exists(os.path.join(BOOK, rel)):
            issues["xlink_missing"].append(f"{os.path.basename(md)} -> {m.group(1)}")
    # boshqa kitobga (../xxx/README.md)
    for m in re.finditer(r"\]\((\.\./[^)]+\.md)\)", text):
        rel = m.group(1)
        if not os.path.exists(os.path.join(BOOK, rel)):
            issues["xlink_missing"].append(f"{os.path.basename(md)} -> {rel} (tashqi)")

# Barcha boblar bormi?
for ch in EXPECTED_CH:
    if not any(n.startswith(ch + "-") for n in md_names):
        issues["xlink_missing"].append(f"BOB YO'Q: {ch}")

# --- SVG fayllar ---
svg_files = sorted(glob.glob(os.path.join(RASM, "*.svg")))
font_re = re.compile(r'font-size="([0-9.]+)"')
for svg in svg_files:
    raw = open(svg, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        issues["bom"].append(os.path.basename(svg))
    text = raw.decode("utf-8", "replace")
    check_cyrillic(svg, text)
    # header tekshiruvi
    if not text.lstrip().startswith("<svg"):
        issues["svg_header"].append(os.path.basename(svg) + " (svg bilan boshlanmaydi)")
    if "xmlns" not in text[:200]:
        issues["svg_header"].append(os.path.basename(svg) + " (xmlns yo'q)")
    # font-size < 13
    mins = [float(x) for x in font_re.findall(text)]
    small = [x for x in mins if x < 13]
    if small:
        issues["font"].append(f"{os.path.basename(svg)}: {sorted(set(small))} (min={min(mins) if mins else '-'})")
    # XML well-formed
    try:
        ET.fromstring(text)
    except ET.ParseError as e:
        issues["xml"].append(f"{os.path.basename(svg)}: {e}")

# --- Hisobot ---
print("="*70)
print(f"MARKDOWN: {len(md_files)} ta | SVG: {len(svg_files)} ta")
print("="*70)
total = 0
labels = {
    "cyrillic": "KIRILL HARFLAR (tuzatish shart)",
    "bom": "BOM (tuzatish shart)",
    "font": "FONT < 13 (tuzatish shart)",
    "img_missing": "RASM HAVOLASI YO'Q",
    "xlink_missing": "CROSS-LINK / BOB YO'Q",
    "xml": "SVG XML XATO",
    "svg_header": "SVG HEADER XATO",
    "raw_lt": "EKRANLANMAGAN <",
}
for k, label in labels.items():
    items = issues[k]
    total += len(items)
    print(f"\n### {label}: {len(items)} ta")
    for it in items[:60]:
        print("   -", it)
    if len(items) > 60:
        print(f"   ... va yana {len(items)-60} ta")
print("\n" + "="*70)
print(f"JAMI MUAMMO: {total}")
print("="*70)
