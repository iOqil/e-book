# -*- coding: utf-8 -*-
"""DevOps kitobi markaziy QA. Faqat docs/devops ni tekshiradi. UTF-8 hisobot faylga yoziladi."""
import os, re, glob, unicodedata
from xml.dom import minidom

BASE = os.path.join('docs', 'devops')
RAS = os.path.join(BASE, 'rasmlar')
REPORT = '_devops_qa_report.txt'

CHAPTERS = [
    ('01', '01-devops-nima.md'), ('02', '02-linux-server-asoslari.md'),
    ('03', '03-bash-skripting.md'), ('04', '04-tarmoq-xavfsizlik.md'),
    ('05', '05-qolda-deploy.md'), ('06', '06-docker-nima.md'),
    ('07', '07-konteyner-ishlash.md'), ('08', '08-dockerfile.md'),
    ('09', '09-image-optimizatsiya.md'), ('10', '10-volume-network.md'),
    ('11', '11-docker-compose.md'), ('12', '12-cicd-github-actions.md'),
    ('13', '13-pipeline-test-build.md'), ('14', '14-docker-ci-ghcr.md'),
    ('15', '15-avtomatik-deploy.md'), ('16', '16-nginx-asoslari.md'),
    ('17', '17-reverse-proxy-load-balancing.md'), ('18', '18-https-domen.md'),
    ('19', '19-systemd-process.md'), ('20', '20-toliq-deploy.md'),
    ('21', '21-kubernetes-nima.md'), ('22', '22-pod-deployment-service.md'),
    ('23', '23-production-k8s.md'), ('24', '24-ingress-helm-gitops.md'),
    ('25', '25-monitoring-prometheus-grafana.md'), ('26', '26-logging-alerting-backup.md'),
    ('27', '27-iac-ansible-terraform.md'), ('28', '28-kapston.md'),
]

# Latin-but-non-Uzbek letters that must NOT appear (the category-L+not-LATIN check misses these)
BAD_LATIN = {
    0x0131: 'ı dotless-i', 0x0130: 'İ dotted-I', 0x011F: 'ğ', 0x011E: 'Ğ',
    0x015F: 'ş', 0x015E: 'Ş', 0x0259: 'ə', 0x0258: 'ɘ', 0x0069 - 0: '', # noop
}
BAD_LATIN.pop(0x0069, None)
# Fancy apostrophes / quotes that must NOT appear (only ASCII ' U+0027 allowed)
BAD_APOS = {0x2018: 'LEFT SINGLE QUOTE', 0x2019: 'RIGHT SINGLE QUOTE',
            0x02BB: 'MODIFIER TURNED COMMA', 0x02BC: 'MODIFIER APOSTROPHE',
            0x02B9: 'MODIFIER PRIME', 0x00B4: 'ACUTE ACCENT', 0x2032: 'PRIME'}

lines_out = []
def log(s=''):
    lines_out.append(s)

# Symbol chars that Unicode mislabels as letters but are legit (emoji/info). Memory: U+2139 false-positive.
ALLOW = {0x2139}

def classify_char(ch):
    cp = ord(ch)
    if cp in ALLOW:
        return None
    if cp in BAD_APOS:
        return ('APOS', BAD_APOS[cp])
    if cp in BAD_LATIN:
        return ('BADLAT', BAD_LATIN[cp])
    cat = unicodedata.category(ch)
    if cat.startswith('L'):
        try:
            name = unicodedata.name(ch)
        except ValueError:
            name = ''
        if 'LATIN' not in name and 'CJK' not in name and 'HANGUL' not in name:
            # Cyrillic/Greek/Armenian/Georgian/etc letter
            return ('NONLAT', name or hex(cp))
    return None

def context(text, idx, w=25):
    a = max(0, idx - w); b = min(len(text), idx + w)
    return text[a:b].replace('\n', ' ')

total_problems = 0

# ---- Chapter checks ----
log('=== BOB TEKSHIRUVI ===')
existing = set()
for num, fn in CHAPTERS:
    path = os.path.join(BASE, fn)
    if not os.path.isfile(path):
        log(f'[YO\'Q] {fn} mavjud emas!'); total_problems += 1; continue
    existing.add(fn)
    text = open(path, encoding='utf-8').read()
    probs = []
    # language scan
    badchars = {}
    for i, ch in enumerate(text):
        c = classify_char(ch)
        if c:
            key = (c[0], ch, c[1])
            badchars.setdefault(key, []).append(i)
    for (kind, ch, name), idxs in sorted(badchars.items()):
        ex = context(text, idxs[0])
        probs.append(f'  TIL[{kind}] {repr(ch)} ({name}) x{len(idxs)} | ...{ex}...')
    # structure
    if not re.search(r'^#\s+' + num + r'\s+[—-]', text, re.M):
        probs.append(f'  FORMAT: H1 "# {num} —" topilmadi')
    if '> **Bu bobda:**' not in text:
        probs.append('  FORMAT: "> **Bu bobda:**" yo\'q')
    if not re.search(r'##\s+' + num + r'-bob mashqlari', text) and '## Mashqlar' not in text:
        probs.append('  FORMAT: "## NN-bob mashqlari" yo\'q')
    # details balance + markdown=1
    d_open = len(re.findall(r'<details', text))
    d_open_md = len(re.findall(r'<details markdown="1"', text))
    d_close = len(re.findall(r'</details>', text))
    if d_open != d_close:
        probs.append(f'  FORMAT: <details> balans buzuq (open={d_open} close={d_close})')
    if d_open != d_open_md:
        probs.append(f'  FORMAT: {d_open - d_open_md} ta <details> da markdown="1" yo\'q')
    # nav
    if './README.md' not in text:
        probs.append('  NAV: ./README.md havola yo\'q')
    if '../../' in text:
        probs.append('  NAV: ../../ ishlatilgan (taqiqlangan)')
    for m in re.finditer(r'\]\((\.\./[^)]*)\)', text):
        ln = m.group(1)
        if not ln.startswith('../git-github') and not ln.startswith('../python') \
           and not ln.startswith('../nodejs') and not ln.startswith('../django') \
           and not ln.startswith('../php') and not ln.startswith('../laravel'):
            probs.append(f'  NAV: shubhali tashqi havola {ln}')
    # svg refs resolve
    for m in re.finditer(r'!\[[^\]]*\]\((rasmlar/[^)]+\.svg)\)', text):
        rel = m.group(1)
        if not os.path.isfile(os.path.join(BASE, rel)):
            probs.append(f'  RASM: {rel} havola fayli topilmadi')
    # truncation sanity
    if len(text) < 1500:
        probs.append(f'  TO\'LIQSIZ?: bob juda qisqa ({len(text)} bayt)')
    if not text.rstrip().endswith(')') and 'README' not in text.splitlines()[-1]:
        pass
    if probs:
        log(f'\n--- {fn} ({len(text)} bayt) ---')
        for p in probs:
            log(p)
        total_problems += len(probs)
    else:
        log(f'[OK] {fn}')

# ---- SVG checks ----
log('\n=== SVG TEKSHIRUVI ===')
svgs = sorted(glob.glob(os.path.join(RAS, 'dvo*.svg')))
log(f'Jami SVG: {len(svgs)}')
svg_probs = 0
for sp in svgs:
    name = os.path.basename(sp)
    raw = open(sp, encoding='utf-8').read()
    issues = []
    try:
        dom = minidom.parseString(raw)
    except Exception as e:
        log(f'[XML XATO] {name}: {e}'); total_problems += 1; svg_probs += 1; continue
    if '<title' not in raw:
        issues.append('<title> yo\'q')
    # font-size >= 13
    for m in re.finditer(r'font-size\s*=\s*"([\d.]+)"', raw):
        try:
            v = float(m.group(1))
            if v < 13:
                issues.append(f'font-size={v} (<13)')
        except ValueError:
            pass
    for m in re.finditer(r'font-size:\s*([\d.]+)', raw):
        try:
            v = float(m.group(1))
            if v < 13:
                issues.append(f'font-size:{v} (<13, css)')
        except ValueError:
            pass
    # language in svg
    for i, ch in enumerate(raw):
        c = classify_char(ch)
        if c:
            issues.append(f'TIL {repr(ch)} ({c[1]})')
            break
    if issues:
        log(f'[!] {name}: ' + '; '.join(sorted(set(issues))))
        total_problems += len(set(issues)); svg_probs += len(set(issues))

# per-chapter svg count
log('\n=== BOB BOShIGA SVG SONI ===')
for num, fn in CHAPTERS:
    cnt = len(glob.glob(os.path.join(RAS, f'dvo{num}-*.svg')))
    mark = '' if cnt == 3 else '  <-- 3 EMAS!'
    if cnt != 3:
        log(f'  dvo{num}: {cnt} SVG{mark}')
        total_problems += 1

log('\n=== XULOSA ===')
log(f'Boblar topildi: {len(existing)}/28')
log(f'SVG jami: {len(svgs)} (kutilgan 84)')
log(f'JAMI MUAMMO: {total_problems}')

with open(REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print(f'Hisobot yozildi: {REPORT} | boblar={len(existing)}/28 svg={len(svgs)} muammo={total_problems}')
