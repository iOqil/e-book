import asyncio, os, re, glob, sys
from playwright.async_api import async_playwright
from pypdf import PdfWriter

BASE = 'http://127.0.0.1:8013'
BOOKS = [
    ('html-css', 'HTML & CSS'), ('js', 'JavaScript'), ('python', 'Python'),
    ('vue', 'Vue & Nuxt'), ('react', 'React'), ('nextjs', 'Next.js'),
    ('php', 'PHP'), ('sql', 'SQL & MySQL'), ('1000-masala', '1000 masala'),
    ('git-github', 'Git & GitHub'),
    ('typescript', 'TypeScript'),
    ('laravel', 'Laravel'),
    ('php-expert', 'PHP Expert'),
    ('nodejs', 'Node.js'),
    ('django', 'Django'),
    ('nativephp', 'NativePHP'),
    ('tgbot-python', 'Telegram bot (Python)'),
    ('tgbot-php', 'Telegram bot (PHP)'),
    ('tgbot-js', 'Telegram bot (JS)'),
]

def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def book_files(d):
    files = [os.path.basename(p) for p in glob.glob(f'docs/{d}/*.md')]
    files.sort(key=lambda f: (0 if f.lower() == 'readme.md' else 1, natkey(f)))
    return files

def url_for(d, f):
    name = f[:-3]
    return f'{BASE}/{d}/' if name.lower() == 'readme' else f'{BASE}/{d}/{name}/'

CSS = '''
.md-header,.md-tabs,.md-sidebar,.md-footer,.md-nav,.md-search,.md-content__button,[data-md-component=announce],[data-md-component=skip]{display:none!important}
.md-main__inner,.md-content{margin:0!important;max-width:100%!important}
.md-content__inner{padding:8px 10px!important}
.md-content__inner:before{display:none!important}
pre,code,.highlight pre,.md-typeset pre>code{white-space:pre-wrap!important;word-break:break-word!important;overflow-wrap:anywhere!important}
.md-typeset{font-size:.72rem;line-height:1.5}
img,svg{max-width:100%!important;height:auto!important}
.md-typeset table:not([class]){font-size:.62rem}
'''

async def main():
    os.makedirs('_paid-pdf', exist_ok=True)
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for d, name in BOOKS:
            files = book_files(d)
            writer = PdfWriter()
            for f in files:
                url = url_for(d, f)
                try:
                    await page.goto(url, wait_until='networkidle', timeout=90000)
                except Exception as e:
                    print(f'  WARN {url}: {e}');
                    await page.goto(url, wait_until='load', timeout=90000)
                await page.emulate_media(media='print')
                await page.add_style_tag(content=CSS)
                data = await page.pdf(format='A4', print_background=True,
                                      margin={'top':'12mm','bottom':'12mm','left':'10mm','right':'10mm'})
                tmp = '_paid-pdf/_t.pdf'
                open(tmp, 'wb').write(data)
                writer.append(tmp)
            out = f'_paid-pdf/{d}.pdf'
            with open(out, 'wb') as fo:
                writer.write(fo)
            writer.close()
            mb = os.path.getsize(out) / 1024 / 1024
            results.append((d, len(files), round(mb, 1)))
            print(f'{d}.pdf tayyor — {len(files)} sahifa, {mb:.1f} MB', flush=True)
        await browser.close()
    if os.path.exists('_paid-pdf/_t.pdf'):
        os.remove('_paid-pdf/_t.pdf')
    print('=== YAKUN ===')
    for d, n, mb in results:
        print(f'  {d}: {n} sahifa, {mb} MB')

asyncio.run(main())
