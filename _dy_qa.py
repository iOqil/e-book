#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dasturchi yo'riqnomasi kitobi uchun markaziy QA: kirill, BOM, CRLF, SVG font/title, cross-link, nav, skelet."""
import os, re, glob

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/dasturchi-yoriqnomasi"
RAS = os.path.join(BOOK, "rasmlar")
CYR = re.compile(r"[Ѐ-ӿԀ-ԯ]")
FONT = re.compile(r'font-size\s*=\s*"([\d.]+)"')
MDLINK = re.compile(r"\]\(\./([0-9][^)#]+\.md)")            # ./NN-...md
SVGLINK = re.compile(r"\]\(\.?/?rasmlar/([^)]+\.svg)\)")    # (./)rasmlar/...svg

EXPECTED = [
 "01-kod-yozuvchidan-muhandisgacha","02-muammoni-yechish-sanati","03-begona-kodni-oqish",
 "04-debugging-tizimli-ovlash","05-nomlash-sanati","06-funksiyalar-modullik",
 "07-izoh-ozini-hujjatlovchi-kod","08-xatolarni-boshqarish","09-refactoring-kod-hidlari",
 "10-texnik-qarz","11-testlash-madaniyati","12-xavfsiz-kod-asoslari","13-code-review",
 "14-jamoaviy-kod-oqimi","15-agile-scrum-kanban","16-baholash-rejalashtirish",
 "17-texnik-kommunikatsiya","18-hujjatlash","19-fikr-mulohaza-mentorlik",
 "20-ish-muhiti-vositalar","21-vaqt-diqqat-chuqur-ish","22-organishni-organish",
 "23-karyera-narvoni","24-ish-topish-rezyume-portfolio","25-texnik-intervyu",
 "26-frilans-masofaviy-ish","27-etika-masuliyat","28-barqaror-karyera-burnout",
 "29-kapston-90-kun-osish-rejasi",
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

# 2) cross-link integrity (ichki .md va svg)
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

# 3) skelet sanity (faqat boblar)
for slug in EXPECTED:
    p = os.path.join(BOOK, slug + ".md")
    if not os.path.exists(p): continue
    t = open(p, encoding="utf-8").read()
    if "[🏠 README](./README.md)" not in t: P(f"NAV yo'q: {slug}")
    if "## Mashqlar" not in t: P(f"Mashqlar yo'q: {slug}")
    if "<details" not in t or "</details>" not in t: P(f"details yopilmagan/yo'q: {slug}")
    if "## Asosiy g'oyalar" not in t: P(f"Asosiy g'oyalar yo'q: {slug}")
    n_svg = len(set(SVGLINK.findall(t)))
    if n_svg < 3: P(f"SVG havola < 3 ({n_svg}): {slug}")

print(f"Tekshirilgan fayllar: {len(allfiles)} (md+svg)")
if problems:
    print(f"\n=== {len(problems)} MUAMMO ===")
    for m in problems: print(" -", m)
else:
    print("\nHAMMASI TOZA — 0 muammo.")
