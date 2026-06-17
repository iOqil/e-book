#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Algoritmlar kitobi uchun markaziy QA: kirill, BOM, CRLF, SVG font, cross-link, nav."""
import os, re, glob

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/algoritmlar"
RAS = os.path.join(BOOK, "rasmlar")
CYR = re.compile(r"[Ѐ-ӿԀ-ԯ]")
FONT = re.compile(r'font-size\s*=\s*"([\d.]+)"')
MDLINK = re.compile(r"\]\(\./([0-9][^)#]+\.md)")          # ./NN-...md
SVGLINK = re.compile(r"\]\(rasmlar/([^)]+\.svg)\)")        # rasmlar/...svg

EXPECTED = [
 "01-algoritm-nima","02-tasvirlash-blok-sxema-psevdokod","03-chiziqli-algoritmlar",
 "04-tarmoqlanuvchi-algoritmlar","05-takrorlanuvchi-algoritmlar","06-rekursiya-asoslari",
 "07-samaradorlik-hisoblash-modeli","08-asimptotik-notatsiya","09-murakkablikni-hisoblash",
 "10-rekurrent-master-teorema","11-amortizatsiyalangan-tahlil","12-massiv-dinamik-massiv",
 "13-boglangan-royxatlar","14-stack-queue-deque","15-hash-jadval","16-daraxtlar-traversal",
 "17-binar-qidiruv-daraxti","18-balanslangan-daraxtlar","19-heap-priority-queue",
 "20-trie-string-strukturalari","21-graflar-union-find","22-brute-force","23-divide-and-conquer",
 "24-greedy","25-dinamik-dasturlash","26-backtracking","27-saralash-algoritmlari",
 "28-qidiruv-algoritmlari","29-graf-algoritmlari-1","30-graf-algoritmlari-2","31-string-algoritmlari",
 "32-p-np-murakkablik-nazariyasi","33-kapston-algoritm-dizayni",
]

problems = []
def P(msg): problems.append(msg)

# 0) mavjudlik
for slug in EXPECTED:
    if not os.path.exists(os.path.join(BOOK, slug + ".md")):
        P(f"YETISHMAYDI: {slug}.md")

allfiles = sorted(glob.glob(os.path.join(BOOK, "*.md")) + glob.glob(os.path.join(RAS, "*.svg")))
for path in allfiles:
    raw = open(path, "rb").read()
    name = os.path.relpath(path, BOOK)
    if raw[:3] == b"\xef\xbb\xbf": P(f"BOM: {name}")
    if b"\r\n" in raw: P(f"CRLF: {name}")
    text = raw.decode("utf-8", "replace")
    cyr = CYR.findall(text)
    if cyr: P(f"KIRILL ({len(cyr)}x {sorted(set(cyr))}): {name}")

# 1) SVG font-size >= 13
for path in glob.glob(os.path.join(RAS, "*.svg")):
    text = open(path, encoding="utf-8").read()
    bad = [f for f in FONT.findall(text) if float(f) < 13]
    if bad: P(f"FONT<13 {sorted(set(bad))}: rasmlar/{os.path.basename(path)}")
    if "<title" not in text: P(f"TITLE yo'q: rasmlar/{os.path.basename(path)}")

# 2) cross-link integrity
known = set(EXPECTED) | {"README"}
for path in glob.glob(os.path.join(BOOK, "*.md")):
    text = open(path, encoding="utf-8").read()
    name = os.path.basename(path)
    for tgt in MDLINK.findall(text):
        slug = tgt[:-3]
        if slug not in known:
            P(f"NOTO'G'RI LINK -> {tgt} ({name})")
    for svg in SVGLINK.findall(text):
        if not os.path.exists(os.path.join(RAS, svg)):
            P(f"YETISHMAYDIGAN SVG -> {svg} ({name})")

# 3) nav + skeleton sanity (chapters only)
for slug in EXPECTED:
    p = os.path.join(BOOK, slug + ".md")
    if not os.path.exists(p): continue
    t = open(p, encoding="utf-8").read()
    if "[🏠 README](./README.md)" not in t: P(f"NAV yo'q: {slug}")
    if "## Mashqlar" not in t: P(f"Mashqlar yo'q: {slug}")
    if "<details" not in t or "</details>" not in t: P(f"details yopilmagan/yo'q: {slug}")
    if "## Asosiy g'oyalar" not in t: P(f"Asosiy g'oyalar yo'q: {slug}")

print(f"Tekshirilgan fayllar: {len(allfiles)} (md+svg)")
if problems:
    print(f"\n=== {len(problems)} MUAMMO ===")
    for m in problems: print(" -", m)
else:
    print("\nHAMMASI TOZA — 0 muammo.")
