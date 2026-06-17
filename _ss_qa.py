#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soft & Hard skills kitobi uchun markaziy QA: kirill, BOM, CRLF, SVG font, cross-link, nav."""
import os, re, glob

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/soft-hard-skills"
RAS = os.path.join(BOOK, "rasmlar")
CYR = re.compile(r"[Ѐ-ӿԀ-ԯ]")
FONT = re.compile(r'font-size\s*=\s*"([\d.]+)"')
MDLINK = re.compile(r"\]\(\./([0-9][^)#]+\.md)")          # ./NN-...md
SVGLINK = re.compile(r"\]\(\./rasmlar/([^)]+\.svg)\)")     # ./rasmlar/...svg

EXPECTED = [
 "01-skills-nima-t-shaped","02-osish-mentaliteti","03-organishni-organish",
 "04-bilim-boshqaruvi-eslab-qolish","05-vaqtni-boshqarish","06-diqqat-chuqur-ish",
 "07-maqsad-odatlar","08-stress-burnout-muvozanat","09-texnik-muloqot-asoslari",
 "10-yozma-asinxron-muloqot","11-ogzaki-taqdimot-public-speaking","12-tinglash-savol-berish",
 "13-feedback-berish-qabul","14-jamoada-ishlash-xavfsizlik","15-code-review-inson-tomoni",
 "16-nizolarni-hal-qilish","17-masofaviy-ish-jamoa","18-agile-scrum-jarayonlar",
 "19-muammoni-hal-qilish","20-debugging-tizimli","21-begona-kodni-oqish",
 "22-baholash-rejalashtirish","23-texnik-qaror-tradeoff","24-hujjatlashtirish",
 "25-cv-portfolio-github","26-texnik-intervyu","27-behavioral-intervyu-star",
 "28-maosh-muzokara","29-networking-shaxsiy-brend","30-junior-senior-lead-mentorlik",
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

# 1) SVG font-size >= 13 va <title>
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
    if "> **Bu bobda:**" not in t: P(f"intro 'Bu bobda' yo'q: {slug}")
    # SVG soni: kamida 2 ta rasm havolasi
    nsvg = len(SVGLINK.findall(t))
    if nsvg < 2: P(f"SVG < 2 ({nsvg} ta): {slug}")

print(f"Tekshirilgan fayllar: {len(allfiles)} (md+svg)")
if problems:
    print(f"\n=== {len(problems)} MUAMMO ===")
    for m in problems: print(" -", m)
else:
    print("\nHAMMASI TOZA — 0 muammo.")
