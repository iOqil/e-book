import re, glob, os, xml.dom.minidom
files = glob.glob(r'C:\Users\imomn\Desktop\e-books\docs\api-dizayni\rasmlar\api16-*.svg')
for f in sorted(files):
    raw = open(f, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    crlf = b'\r\n' in raw
    s = raw.decode('utf-8')
    cyr = re.findall(r'[Ѐ-ӿ]', s)
    fonts = [int(x) for x in re.findall(r'font-size="(\d+)"', s)]
    bad = [x for x in fonts if x < 13]
    try:
        xml.dom.minidom.parseString(raw)
        xmlok = "OK"
    except Exception as e:
        xmlok = "ERR: " + str(e)
    has_title = '<title>' in s
    print(os.path.basename(f))
    print('  BOM=%s CRLF=%s cyr=%s min_font=%s bad=%s xml=%s title=%s' % (
        bom, crlf, cyr, min(fonts) if fonts else None, bad, xmlok, has_title))
