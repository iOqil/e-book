# Saytni `e-book.oqil.uz` ga chiqarish — yo'riqnoma

Sayt **MkDocs Material** bilan qurilgan. Manba — `docs/` ichidagi markdown kitoblar.
Build natijasi — `site/` papkasi (statik HTML, hech qanday server kerak emas).

---

## Lokal (kompyuterda) ishlatish

```bash
# 1. Kutubxonalarni o'rnatish (bir marta)
pip install -r requirements.txt

# 2. Jonli ko'rish (o'zgartirsang avtomatik yangilanadi)
mkdocs serve
# brauzerda: http://127.0.0.1:8000

# 3. Sayt yasash (deploy uchun)
mkdocs build
# natija: site/ papkasi
```

> Navigatsiyani (sidebar) yangilash uchun yangi bob qo'shsang: `python _genmkdocs.py` ni qaytadan ishga tushir, keyin `mkdocs build`.

---

## Variant A — Cloudflare Pages + Git (tavsiya etiladi)

Eng oson va bepul. Har push'da avtomatik qayta quriladi.

1. **GitHub'ga yukla:** loyihani GitHub repozitoriysiga push qil (`docs/`, `mkdocs.yml`, `requirements.txt` bilan birga). `site/` va `node_modules/` `.gitignore`'da — yuborilmaydi.
2. **Cloudflare Pages:** [dash.cloudflare.com](https://dash.cloudflare.com) → Workers & Pages → Create → Pages → Connect to Git → repozitoriyni tanla.
3. **Build sozlamalari:**
   - Framework preset: **None**
   - Build command: `pip install -r requirements.txt && mkdocs build`
   - Build output directory: `site`
   - Environment variable: `PYTHON_VERSION` = `3.12`
4. **Deploy** — bir necha daqiqada `<loyiha>.pages.dev` da chiqadi.
5. **Domen:** Pages loyihasi → Custom domains → `e-book.oqil.uz` qo'sh.
   - `oqil.uz` Cloudflare DNS'da bo'lsa — avtomatik ulanadi.
   - Bo'lmasa: DNS'da `e-book` uchun **CNAME** yozuvi → `<loyiha>.pages.dev`.

> PDF'lar `docs/pdf/` da repozitoriyga kiritilgan, shuning uchun `mkdocs build` ularni `site/pdf/` ga ko'chiradi — Playwright CI'da kerak emas.

---

## Variant B — To'g'ridan-to'g'ri yuklash (Wrangler, Git'siz)

```bash
mkdocs build                       # site/ yasaydi
npx wrangler pages deploy site --project-name=oqil-ebooklar
```
Keyin Cloudflare panelida `e-book.oqil.uz` domenini ulang (yuqoridagi 5-qadam).

---

## Variant C — GitHub Pages

`.github/workflows/deploy.yml` yarat:

```yaml
name: deploy
on: { push: { branches: [main] } }
permissions: { contents: read, pages: write, id-token: write }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@v3
        with: { path: site }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages }
    steps:
      - uses: actions/deploy-pages@v4
```
So'ng repo Settings → Pages → Custom domain: `e-book.oqil.uz` (DNS'da CNAME).

---

## Maslahat
- **Cloudflare Pages** — eng tez va sodda (ayniqsa `oqil.uz` allaqachon Cloudflare'da bo'lsa).
- Kitobni yangilash = `docs/` dagi `.md` ni tahrirlash → push → sayt o'zi yangilanadi.
- PDF'larni yangilash uchun: `mkdocs build` → `python _genpdf.py` (lokal, Playwright bilan) → yangi PDF'larni commit qil.
