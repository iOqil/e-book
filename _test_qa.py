#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testing kitobi uchun markaziy QA: kirill, BOM, CRLF, SVG font/title, cross-link, nav, skelet."""
import os, re, glob

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/testing"
RAS = os.path.join(BOOK, "rasmlar")
CYR = re.compile(r"[Ѐ-ӿԀ-ԯ]")          # kirill + qo'shimcha kirill
FONT = re.compile(r'font-size\s*=\s*"([\d.]+)"')
MDLINK = re.compile(r"\]\(\./([0-9][^)#]+\.md)")            # ./NN-...md
SVGLINK = re.compile(r"\]\(\./rasmlar/([^)]+\.svg)\)")      # ./rasmlar/...svg

EXPECTED = [
 "01-nega-test-yozamiz","02-birinchi-test-aaa","03-test-turlari-piramida",
 "04-yaxshi-test-xossalari","05-assertionlar-test-holatlari","06-fixture-parametrize",
 "07-test-dublyorlari-nazariya","08-test-dublyorlari-amaliyot","09-bogliqliklarni-izolyatsiya",
 "10-testlanadigan-dizayn","11-tdd-red-green-refactor","12-tdd-amaliyot-kata",
 "13-refactoring-va-testlar","14-bdd-spetsifikatsiya","15-integratsiya-testlari",
 "16-malumotlar-bazasi-testlash","17-api-http-testlash","18-kontrakt-testlar",
 "19-e2e-ui-testlar","20-code-coverage","21-property-based-testing","22-mutation-testing",
 "23-snapshot-approval-testing","24-flaky-testlar","25-performance-yuk-testlari",
 "26-xavfsizlik-testlash","27-ci-cd-avtomatlashtirish","28-test-strategiyasi-quadrants",
 "29-legacy-kodni-testlash","30-kapston",
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

# 1) SVG font-size >= 13 + <title>
for path in glob.glob(os.path.join(RAS, "*.svg")):
    text = open(path, encoding="utf-8").read()
    bad = [f for f in FONT.findall(text) if float(f) < 13]
    if bad: P(f"FONT<13 {sorted(set(bad))}: rasmlar/{os.path.basename(path)}")
    if "<title" not in text: P(f"TITLE yo'q: rasmlar/{os.path.basename(path)}")

# 2) cross-link integrity (md + svg)
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

# 3) skelet sanity (boblar)
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
