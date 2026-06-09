import os, re, glob

BOOKS = [
    ('html-css', 'HTML & CSS'),
    ('js', 'JavaScript'),
    ('python', 'Python'),
    ('vue', 'Vue & Nuxt'),
    ('react', 'React'),
    ('nextjs', 'Next.js'),
    ('php', 'PHP'),
    ('1000-masala', '1000 masala'),
]

def title(path):
    try:
        for line in open(path, encoding='utf-8'):
            m = re.match(r'^#\s+(.+)$', line)
            if m:
                return m.group(1).replace('`', '').strip()
    except Exception:
        pass
    return os.path.basename(path)

def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def yq(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def book_files(d):
    files = [os.path.basename(p) for p in glob.glob(f'docs/{d}/*.md')]
    files.sort(key=lambda f: (0 if f.lower() == 'readme.md' else 1, natkey(f)))
    return files

nav_lines = ['nav:', '  - Bosh sahifa: index.md']
for d, name in BOOKS:
    nav_lines.append(f'  - {yq(name)}:')
    for f in book_files(d):
        t = title(f'docs/{d}/{f}')
        nav_lines.append(f'      - {yq(t)}: {d}/{f}')
nav_lines.append('  - "Litsenziya va muallif": litsenziya.md')

config = f'''site_name: Oqil E-kitoblar
site_description: "Dasturlash bo'yicha o'zbekcha e-kitoblar — 0 dan expertgacha. 8 ta qo'llanma, 297 SVG diagramma."
copyright: '© 2026 <a href="/litsenziya/">Oqil Imomnazarov</a> · bepul · savdo taqiqlanadi · CC BY-NC-SA 4.0'
repo_url: https://github.com/iOqil/e-book
repo_name: iOqil/e-book
edit_uri: edit/main/docs/
docs_dir: docs
site_dir: site
use_directory_urls: true

extra_css:
  - assets/extra.css

theme:
  name: material
  language: uz
  logo: assets/logo.svg
  favicon: assets/logo.svg
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.instant
    - navigation.instant.progress
    - navigation.instant.prefetch
    - navigation.tabs.sticky
    - content.tooltips
    - search.share
    - navigation.tabs
    - navigation.top
    - navigation.tracking
    - navigation.indexes
    - navigation.footer
    - toc.follow
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.action.edit
    - content.action.view
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: "Qorong'i rejim"
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: "Yorug' rejim"

extra:
  social:
    - icon: material/web
      link: https://ioqil.uz
      name: ioqil.uz
    - icon: fontawesome/brands/telegram
      link: https://t.me/i_oqil
      name: Telegram
    - icon: fontawesome/brands/youtube
      link: https://www.youtube.com/@I_Oqil
      name: YouTube

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - footnotes
  - toc:
      permalink: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.superfences
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true

plugins:
  - search

{chr(10).join(nav_lines)}
'''

open('mkdocs.yml', 'w', encoding='utf-8', newline='\n').write(config)
total = sum(len(book_files(d)) for d, _ in BOOKS)
print(f'mkdocs.yml yozildi. {len(BOOKS)} kitob, {total} sahifa nav.')
