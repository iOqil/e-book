#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API-dizayni kitobi uchun markaziy QA: kirill, BOM, CRLF, SVG font, cross-link, nav, +JSON/YAML fence validatsiya."""
import os, re, glob, json

try:
    import yaml
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/api-dizayni"
RAS = os.path.join(BOOK, "rasmlar")
CYR = re.compile(r"[Ѐ-ӿԀ-ԯ]")
FONT = re.compile(r'font-size\s*=\s*"([\d.]+)"')
MDLINK = re.compile(r"\]\(\./([0-9][^)#]+\.md)")
SVGLINK = re.compile(r"\]\(rasmlar/([^)]+\.svg)\)")
FENCE = re.compile(r"```(json|yaml)\n(.*?)```", re.DOTALL)

EXPECTED = [
 "01-api-nima","02-http-chuqur","03-http-status-kodlari","04-api-uslublari",
 "05-rest-tamoyillari","06-resurs-uri-dizayni","07-sorov-javob-payload","08-sahifalash-filtrlash",
 "09-xato-dizayni","10-versiyalash","11-autentifikatsiya","12-avtorizatsiya","13-api-xavfsizligi",
 "14-rate-limiting","15-idempotentlik-parallellik","16-keshlash","17-graphql","18-grpc",
 "19-asinxron-webhook","20-realtime-websocket-sse","21-openapi","22-hujjatlash-dx",
 "23-api-gateway-bff","24-testlash-contract","25-observability","26-hayot-sikli-governance",
 "27-naqshlar-antinaqshlar","28-kapston",
]

problems = []
notes = []
def P(m): problems.append(m)

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

# SVG font>=13 + title
for path in glob.glob(os.path.join(RAS, "*.svg")):
    text = open(path, encoding="utf-8").read()
    bad = [f for f in FONT.findall(text) if float(f) < 13]
    if bad: P(f"FONT<13 {sorted(set(bad))}: rasmlar/{os.path.basename(path)}")
    if "<title" not in text: P(f"TITLE yo'q: rasmlar/{os.path.basename(path)}")

# cross-links + nav + skeleton + fenced JSON/YAML
known = set(EXPECTED) | {"README"}
for path in glob.glob(os.path.join(BOOK, "*.md")):
    text = open(path, encoding="utf-8").read()
    base = os.path.basename(path); slug = base[:-3]
    for tgt in MDLINK.findall(text):
        if tgt[:-3] not in known: P(f"NOTO'G'RI LINK -> {tgt} ({base})")
    for svg in SVGLINK.findall(text):
        if not os.path.exists(os.path.join(RAS, svg)): P(f"YETISHMAYDIGAN SVG -> {svg} ({base})")
    if slug in EXPECTED:
        if "[🏠 README](./README.md)" not in text: P(f"NAV yo'q: {slug}")
        if "## Mashqlar" not in text: P(f"Mashqlar yo'q: {slug}")
        if "<details" not in text or "</details>" not in text: P(f"details muammo: {slug}")
        if "## Asosiy g'oyalar" not in text: P(f"Asosiy g'oyalar yo'q: {slug}")
    # fenced JSON/YAML validatsiya (deliberately-bad '...' anti-misollarni o'tkazib yubor)
    for lang, body in FENCE.findall(text):
        if "..." in body or "<" in body and lang == "json":  # placeholder/anti-misol
            continue
        try:
            if lang == "json": json.loads(body)
            elif lang == "yaml" and HAVE_YAML: yaml.safe_load(body)
        except Exception as e:
            notes.append(f"{lang.upper()} fence shubhali ({base}): {str(e)[:60]}")

print(f"Tekshirilgan fayllar: {len(allfiles)} (md+svg); yaml={'bor' if HAVE_YAML else 'yoq'}")
if problems:
    print(f"\n=== {len(problems)} MUAMMO ===")
    for m in problems: print(" -", m)
else:
    print("\nHAMMASI TOZA — 0 muammo.")
if notes:
    print(f"\n--- {len(notes)} eslatma (qo'lda ko'rib chiqing, ataylab-bad bo'lishi mumkin) ---")
    for n in notes[:40]: print(" ~", n)
