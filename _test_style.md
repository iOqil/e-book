# Testing kitobi — yagona uslub va format yo'riqnomasi (AGENTLAR UCHUN)

Bu fayl — "Dasturiy ta'minotni testlash — 0 dan Expertgacha" kitobining HAR bir bobini
yozadigan agent uchun **majburiy** spetsifikatsiya. Boshqa boblar bilan **bir xil ko'rinish**
va sifatni ta'minlash uchun shu yerdagi qoidalarga **so'zma-so'z** amal qiling.

Kitob **til-mustaqil** (algoritmlar/arxitektura kabi): asosiy yuk — **tushuncha, diagramma,
psevdokod va tamoyillar**. Lekin har bir texnika yonida **ishlaydigan Python + pytest** namunasi
beriladi (Python o'qishga oson va psevdokodga yaqin). G'oyalar har qanday tilda (JS+Jest/Vitest,
PHP+PHPUnit/Pest, Java+JUnit, Go+testing) bir xil qo'llaniladi — buni matnda zarur joyda eslatib o'ting.

---

## 0. ENG MUHIM QOIDALAR (buzilmasin)

1. **FAQAT lotin o'zbek alifbosi.** Kirill harf (а, е, о, с, р, х, и...) MUTLAQO bo'lmasin —
   na matnda, na kodda, na SVG'da. Bu eng tez-tez uchraydigan xato (homoglif): lotincha
   "o", "a", "e", "c", "p", "x", "y" bilan kirillchani aralashtirmang. Yozgandan keyin o'zingiz tekshiring.
2. **Hech qanday BOM, hech qanday CRLF.** Fayllarni toza UTF-8, LF satr-oxiri bilan yozing.
3. **Har bir Python namunasi HAQIQATAN ishga tushirilsin.** Kodni o'zingiz `python`/`pytest`
   bilan ishlatib, chiqishini tekshiring. `# ->` izohidagi chiqish/natija aniq mos kelsin.
   Test "o'tdi/yiqildi" (PASS/FAIL) holatini ham haqiqiy pytest chiqishidan oling — to'qib chiqarmang.
4. **SVG `font-size` har doim ≥ 13.** Hech qachon 12 yoki kichik bo'lmasin (QA yiqitadi).
5. **Har SVG'da `<title>` element bor.** Aks holda QA yiqitadi.
6. **Hammasi o'zbek tilida** (kod identifikatorlari ham iloji boricha o'zbekcha: `savat`, `foydalanuvchi`,
   `narx_hisobla`), ammo standart texnik atamalar (unit test, mock, fixture, coverage, CI) — asl
   shaklida, qavs ichida o'zbekcha izoh bilan birinchi marta tushuntiriladi.

---

## 1. FAYL JOYLASHUVI

- Bob fayli: `docs/testing/NN-slug.md` (masalan `docs/testing/03-test-turlari-piramida.md`).
- SVG rasmlar: `docs/testing/rasmlar/tstNN-qisqa-nom.svg` (prefiks **`tst`** + bob raqami).
  Masalan: `docs/testing/rasmlar/tst03-piramida.svg`.
- Har bobda **3 ta SVG** (ba'zi murakkab bobda 2–4 bo'lishi mumkin, lekin standart = 3).
- Matnda rasm shunday joylashtiriladi: `![Tavsif matni](./rasmlar/tst03-piramida.svg)`

---

## 2. BOB FAYLINING ANIQ STRUKTURASI

Quyidagi tartibni **aynan** takrorlang (algoritmlar kitobidagidek):

```markdown
# NN — Bob sarlavhasi

[🏠 README](./README.md) · [⬅️ Oldingi: PREV](./PREV-slug.md) · [Keyingi: NEXT ➡️](./NEXT-slug.md)

---

> **Bu bobda:** 2–4 jumlada bobda nimani o'rganishini ayting (aniq, qiziqarli).
>
> **Halollik / Eslatma:** bobning chegarasi, soddalashtirishlar, qaysi narsa keyingi bobga
> qoldirilgani, va "barcha kod namunalari haqiqatan ishga tushirib tekshirilgan" eslatmasi.

---

## Birinchi mavzu sarlavhasi

Matn... (iliq, tushuntiruvchi ohang; "siz"ga murojaat; real hayotiy analogiya bilan boshlang).

![Rasm tavsifi](./rasmlar/tstNN-nom.svg)

### Kichik sarlavha

...

## Keyingi mavzu

...

---

## Asosiy g'oyalar (bobni qisqacha)

- **Qalin tezis** — qisqa tushuntirish.
- ... (5–8 ta asosiy xulosa)

---

## Mashqlar

### Oson

**1-mashq.** ...
**2-mashq.** ...
**3-mashq.** ...

### O'rta

**4-mashq.** ...
**5-mashq.** ...
**6-mashq.** ...

### Qiyin

**7-mashq.** ...
**8-mashq.** ...

<details markdown="1">
<summary>Yechimlar</summary>

### 1-mashq yechimi
...

### 2-mashq yechimi
...

(har mashq uchun yechim)

</details>

---

[🏠 README](./README.md) · [⬅️ Oldingi: PREV](./PREV-slug.md) · [Keyingi: NEXT ➡️](./NEXT-slug.md)
```

### Nav qatori qoidalari (juda muhim — cross-link QA tekshiradi)
- **Birinchi bob (01):** oldingi yo'q → `[🏠 README](./README.md) · [Keyingi: 02 — ... ➡️](./02-slug.md)`
- **Oxirgi bob (30):** keyingi yo'q → `[🏠 README](./README.md) · [⬅️ Oldingi: 29 — ...](./29-slug.md)`
- **O'rta boblar:** README + Oldingi + Keyingi (yuqoridagidek).
- Slug'larni **aniq** yozing (quyidagi 4-bo'limdagi ro'yxatdan). Noto'g'ri slug = buzilgan havola.

---

## 3. MAZMUN VA OHANG

- **Mutlaqo boshlovchidan ekspertgacha.** Hech narsani "ma'lum" deb hisoblamang; har atamani
  birinchi ishlatishda tushuntiring.
- **Real hayotiy analogiya** bilan boshlang (masalan: test = mashinani sotishdan oldin tekshirish).
- **Misol VA anti-misol.** Yaxshi test va yomon testni yonma-yon ko'rsating (✅ / ❌ belgilar bilan).
- **Trade-off'larni ochiq ayting.** `> **Trade-off:**` blokida. Testing — muvozanat san'ati
  (tezlik vs ishonch, izolyatsiya vs realistiklik, coverage vs vaqt).
- **Halol bo'ling.** `> **Eslatma:**` / `> **Diqqat:**` bloklarida soddalashtirishlar, cheklovlar,
  "bu yondashuv qachon noto'g'ri" holatlarini ayting. Testing'da "100% coverage = xatosiz" kabi
  afsonalarni ataylab buzing.
- **Jadval**lardan foydalaning (taqqoslash uchun juda mos: unit vs integration, mock vs stub, ...).
- Boshqa boblarga **ichki havola** bering (`[07-bob](./07-test-dublyorlari-nazariya.md)`) — lekin
  faqat ro'yxatdagi mavjud slug'larga.
- Tegishli joyda boshqa kitoblarga havola: arxitektura (`../arxitektura/README.md`),
  algoritmlar (`../algoritmlar/README.md`), DevOps (`../devops/README.md`). Slug aniq bo'lmasa,
  faqat README'ga havola qiling (taxmin qilmang).

### Python + pytest namunalari uchun
- **Sinaladigan kod** va **test kod**ini aniq ajrating (ikki alohida blok yoki izoh bilan).
- Test funksiyalari `test_` bilan boshlanadi; AAA (Arrange-Act-Assert) tuzilishini ko'rsating.
- pytest chiqishini ko'rsatganda haqiqiy formatga yaqin bo'ling, masalan:
  ```text
  ======== 3 passed in 0.02s ========
  ```
  yoki yiqilgan testda `assert 5 == 6` kabi. Lekin asosiy e'tibor — **g'oya**, log'ni
  uzun-uzun ko'chirmang.
- Har kod blokida `# ->` bilan kutilgan natijani ko'rsating (haqiqatan tekshirilgan).
- Kerakli kutubxonalar: `pytest` (asosiy), `unittest.mock` (standart), `hypothesis`
  (property-based, 21-bob), `coverage`/`pytest-cov` (20-bob), `mutmut` (mutation, 22-bob),
  `requests`/`httpx` + `respx`/`responses` (API, 17-bob), `freezegun` (vaqt, 09-bob).
  Tashqi kutubxona ishlatganda `pip install ...` ni eslatib o'ting.
- Til-mustaqillikni eslatish: kerakli joyda "JS'da bu `jest.fn()`, PHP'da `Mockery`" kabi
  qisqa ko'prik bering — lekin chuqurlashmang.

### Hajm
- Har bob ~250–420 satr markdown (algoritmlar kitobidagi kabi to'liq, lekin suvsiz).
- 8 ta mashq (3 oson + 3 o'rta + 2 qiyin), har biriga `<details>` ichida yechim.

---

## 4. KITOB BOBLARI (slug ro'yxati — nav uchun)

```
01-nega-test-yozamiz
02-birinchi-test-aaa
03-test-turlari-piramida
04-yaxshi-test-xossalari
05-assertionlar-test-holatlari
06-fixture-parametrize
07-test-dublyorlari-nazariya
08-test-dublyorlari-amaliyot
09-bogliqliklarni-izolyatsiya
10-testlanadigan-dizayn
11-tdd-red-green-refactor
12-tdd-amaliyot-kata
13-refactoring-va-testlar
14-bdd-spetsifikatsiya
15-integratsiya-testlari
16-malumotlar-bazasi-testlash
17-api-http-testlash
18-kontrakt-testlar
19-e2e-ui-testlar
20-code-coverage
21-property-based-testing
22-mutation-testing
23-snapshot-approval-testing
24-flaky-testlar
25-performance-yuk-testlari
26-xavfsizlik-testlash
27-ci-cd-avtomatlashtirish
28-test-strategiyasi-quadrants
29-legacy-kodni-testlash
30-kapston
```

README slug = `README` (bosh harf).

---

## 5. SVG USLUBI (aniq)

Har SVG quyidagi qolipga mos kelsin:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 480">
  <title>Aniq, qisqa sarlavha (o'zbekcha)</title>
  <rect x="0" y="0" width="820" height="480" fill="#f8fafc"/>
  <text x="410" y="40" text-anchor="middle" font-family="Segoe UI" font-size="22" font-weight="bold" fill="#1e293b">Bosh sarlavha</text>
  <text x="410" y="66" text-anchor="middle" font-family="Segoe UI" font-size="14" fill="#64748b">Izoh / sub-sarlavha</text>
  <!-- ... shakllar ... -->
</svg>
```

Qoidalar:
- `xmlns` shart; `viewBox` shart (kenglik odatda 760–860, balandlik mazmunga qarab).
- **`<title>` shart** (QA tekshiradi). BOM/CRLF yo'q. Kirill yo'q.
- `font-family="Segoe UI"`, `font-size` HAR DOIM **≥ 13** (sarlavhalar 18–24, izohlar 13–15).
- Fon: `<rect ... fill="#f8fafc"/>` (yoki `#ffffff`).
- **Rang palitrasi** (boshqa boblar bilan bir xil bo'lsin):
  - Asosiy qora/dark: `#1e293b`, ikkilamchi matn: `#64748b`, och fon: `#f8fafc`/`#eff6ff`
  - Ko'k (asosiy): `#2563eb`  · Yashil (yaxshi/PASS): `#16a34a`  · Qizil (xato/FAIL): `#dc2626`
  - Binafsha: `#7c3aed`  · Amber/sariq (ogohlik): `#f59e0b`  · ramka kulrang: `#94a3b8`/`#cbd5e1`
- Kartochkalar: `rx="8"`–`rx="12"` yumaloq burchak, `stroke-width="2"`.
- Matn `text-anchor="middle"` markazlash uchun; o'qiladigan, ortiqcha tig'iz emas.
- **Testing'ga mos vizual g'oyalar:** test piramidasi (3 qatlam), Red→Green→Refactor sikli (3 doira),
  AAA bloklari, mock vs real diagramma, coverage o'lchagich, flaky test "goh o'tadi goh yiqiladi" oqimi,
  CI pipeline bosqichlari. Diagramma g'oyani **ko'rsatsin**, bezak bo'lmasin.

---

## 6. YAKUNIY TEKSHIRUV (agent o'zi qilsin, topshirishdan oldin)

- [ ] Kirill harf yo'q (matn + kod + SVG).
- [ ] BOM/CRLF yo'q.
- [ ] Har Python namunasi ishga tushirildi, `# ->` chiqishlari va PASS/FAIL haqiqiy.
- [ ] 3 ta SVG yaratildi, har birida `<title>`, font-size ≥ 13, kirill yo'q.
- [ ] Nav qatori (yuqori + past) to'g'ri slug'lar bilan.
- [ ] `## Asosiy g'oyalar`, `## Mashqlar`, `<details>...</details>` mavjud.
- [ ] Ichki havolalar mavjud slug'larga.
```
