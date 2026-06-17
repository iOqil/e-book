# -*- coding: utf-8 -*-
"""WordPress plugin kitobi markaziy QA. Faqat docs/wp-plugin ni tekshiradi. UTF-8 hisobot faylga."""
import os, re, glob, unicodedata
from xml.dom import minidom

BASE = os.path.join('docs', 'wp-plugin')
RAS = os.path.join(BASE, 'rasmlar')
REPORT = '_wp_qa_report.txt'

CHAPTERS = [
    ('01','01-arxitektura-falsafa.md'),('02','02-lokal-muhit.md'),
    ('03','03-birinchi-plugin.md'),('04','04-hooks-action-filter.md'),
    ('05','05-namespace-oop-autoload.md'),('06','06-settings-api-admin.md'),
    ('07','07-custom-post-types.md'),('08','08-taxonomiyalar.md'),
    ('09','09-meta-box-custom-fields.md'),('10','10-malumotlar-bazasi.md'),
    ('11','11-rollar-capabilities.md'),('12','12-xavfsizlik-asoslari.md'),
    ('13','13-shortcode.md'),('14','14-enqueue-assets.md'),
    ('15','15-ajax.md'),('16','16-rest-api.md'),
    ('17','17-wp-cron.md'),('18','18-email-http-cache.md'),
    ('19','19-blok-kirish-create-block.md'),('20','20-static-blok.md'),
    ('21','21-dynamic-blok.md'),('22','22-blok-kengaytmalar.md'),
    ('23','23-sidebar-slotfill-data.md'),('24','24-i18n-lokalizatsiya.md'),
    ('25','25-testlash.md'),('26','26-performance.md'),
    ('27','27-woocommerce.md'),('28','28-distribution.md'),
    ('29','29-xavfsizlik-audit.md'),('30','30-kapston.md'),
]

BAD_LATIN = {0x0131:'ı dotless-i',0x0130:'İ',0x011F:'ğ',0x011E:'Ğ',0x015F:'ş',0x015E:'Ş',0x0259:'ə'}
BAD_APOS = {0x2018:'LEFT SINGLE QUOTE',0x2019:'RIGHT SINGLE QUOTE',0x02BB:'TURNED COMMA',
            0x02BC:'MODIFIER APOSTROPHE',0x02B9:'PRIME',0x00B4:'ACUTE',0x2032:'PRIME'}
ALLOW = {0x2139}  # ℹ info — Unicode mislabels as Ll

def classify_char(ch):
    cp = ord(ch)
    if cp in ALLOW: return None
    if cp in BAD_APOS: return ('APOS', BAD_APOS[cp])
    if cp in BAD_LATIN: return ('BADLAT', BAD_LATIN[cp])
    cat = unicodedata.category(ch)
    if cat.startswith('L'):
        try: name = unicodedata.name(ch)
        except ValueError: name = ''
        if 'LATIN' not in name and 'CJK' not in name and 'HANGUL' not in name:
            return ('NONLAT', name or hex(cp))
    return None

def context(text, idx, w=25):
    return text[max(0,idx-w):min(len(text),idx+w)].replace('\n',' ')

out=[]
def log(s=''): out.append(s)
total=0

# allowed cross-book links
ALLOWED_REL = ('../php','../php-expert','../js','../nodejs','../git-github','../laravel','../python')

log('=== BOB TEKSHIRUVI ===')
found=set()
for num,fn in CHAPTERS:
    path=os.path.join(BASE,fn)
    if not os.path.isfile(path):
        log(f"[YO'Q] {fn}"); total+=1; continue
    found.add(fn)
    text=open(path,encoding='utf-8').read()
    probs=[]
    bad={}
    for i,ch in enumerate(text):
        c=classify_char(ch)
        if c: bad.setdefault((c[0],ch,c[1]),[]).append(i)
    for (kind,ch,name),idxs in sorted(bad.items()):
        probs.append(f"  TIL[{kind}] {repr(ch)} ({name}) x{len(idxs)} | ...{context(text,idxs[0])}...")
    if not re.search(r'^#\s+'+num+r'\s+[—-]', text, re.M):
        probs.append(f'  FORMAT: H1 "# {num} —" topilmadi')
    if '> **Bu bobda:**' not in text: probs.append('  FORMAT: "> **Bu bobda:**" yo\'q')
    if not re.search(r'##\s+'+num+r'-bob mashqlari', text) and '## Mashqlar' not in text:
        probs.append('  FORMAT: "## NN-bob mashqlari" yo\'q')
    do=len(re.findall(r'<details',text)); dm=len(re.findall(r'<details markdown="1"',text)); dc=len(re.findall(r'</details>',text))
    if do!=dc: probs.append(f'  FORMAT: <details> balans (open={do} close={dc})')
    if do!=dm: probs.append(f'  FORMAT: {do-dm} ta <details> markdown="1" yo\'q')
    if './README.md' not in text: probs.append('  NAV: ./README.md yo\'q')
    if '../../' in text: probs.append('  NAV: ../../ taqiqlangan')
    for m in re.finditer(r'\]\((\.\./[^)]*)\)', text):
        if not m.group(1).startswith(ALLOWED_REL):
            probs.append(f'  NAV: shubhali tashqi havola {m.group(1)}')
    for m in re.finditer(r'!\[[^\]]*\]\((rasmlar/[^)]+\.svg)\)', text):
        if not os.path.isfile(os.path.join(BASE,m.group(1))):
            probs.append(f'  RASM: {m.group(1)} topilmadi')
    if len(text)<1500: probs.append(f"  TO'LIQSIZ? ({len(text)} bayt)")
    if probs:
        log(f'\n--- {fn} ({len(text)} bayt) ---'); [log(p) for p in probs]; total+=len(probs)
    else: log(f'[OK] {fn}')

log('\n=== SVG TEKSHIRUVI ===')
svgs=sorted(glob.glob(os.path.join(RAS,'wpp*.svg')))
log(f'Jami SVG: {len(svgs)}')
for sp in svgs:
    name=os.path.basename(sp); raw=open(sp,encoding='utf-8').read(); iss=[]
    try: minidom.parseString(raw)
    except Exception as e: log(f'[XML XATO] {name}: {e}'); total+=1; continue
    if '<title' not in raw: iss.append('<title> yo\'q')
    for m in re.finditer(r'font-size\s*=\s*"([\d.]+)"',raw):
        if float(m.group(1))<13: iss.append(f'font-size={m.group(1)}(<13)')
    for m in re.finditer(r'font-size:\s*([\d.]+)',raw):
        if float(m.group(1))<13: iss.append(f'font-size:{m.group(1)}(<13css)')
    for ch in raw:
        c=classify_char(ch)
        if c: iss.append(f'TIL {repr(ch)}({c[1]})'); break
    if iss: log(f'[!] {name}: '+'; '.join(sorted(set(iss)))); total+=len(set(iss))

log('\n=== BOB BOSHIGA SVG SONI ===')
for num,fn in CHAPTERS:
    cnt=len(glob.glob(os.path.join(RAS,f'wpp{num}-*.svg')))
    if cnt!=3: log(f'  wpp{num}: {cnt} SVG <-- 3 EMAS!'); total+=1

log('\n=== XULOSA ===')
log(f'Boblar: {len(found)}/30 | SVG: {len(svgs)} (kutilgan 90) | JAMI MUAMMO: {total}')
open(REPORT,'w',encoding='utf-8').write('\n'.join(out))
print(f'Hisobot: {REPORT} | boblar={len(found)}/30 svg={len(svgs)} muammo={total}')
