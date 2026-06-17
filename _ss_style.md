# Soft & Hard skills kitobi — yagona uslub va format (HAR BIR AGENT O'QIYDI)

Bu fayl — kitobning **yagona shartnomasi**. Har bir bob aynan shu formatda, shu ohangda, shu sifatda yoziladi. Maqsad: 30 bob bir muallif yozganday izchil chiqsin.

Kitob joylashuvi: `docs/soft-hard-skills/`. Rasmlar: `docs/soft-hard-skills/rasmlar/`.

---

## 0) Kitob haqida (kontekst)

- **Mavzu:** dasturchining professional ko'nikmalari — soft skill (muloqot, jamoa, vaqt, mentalitet) va til-mustaqil hard skill (debugging, muammo yechish, kod o'qish, baholash, hujjat) hamda karyera (CV, intervyu, o'sish).
- **Til-mustaqil:** hech qanday dasturlash tili o'rgatilmaydi. Misollar dasturchi hayotidan: code review, sprint, stand-up, PR, intervyu, daily, retro.
- **Auditoriya:** dasturlashni o'rganayotgan yoki junior–mid darajadagi, o'zbek tilida o'qiydigan kishi. Texnik chuqurlik shart emas; inson tomoni markazda.
- **Ohang:** samimiy, "katta aka maslahat berayotganday", lekin jiddiy va aniq. Voiz emas — amaliy. O'quvchini "siz" deb chaqir.

---

## 1) Fayl skeleti (AYNAN shu tartib)

Har bob `.md` fayli quyidagi tuzilishga **qat'iy** amal qiladi:

```
# NN — Bob sarlavhasi

<NAV QATORI — pastga qarang>

---

> **Bu bobda:** 2–4 jumlada bobda nimani o'rganishini ayt (qaysi ramkalar, qaysi ko'nikma).
>
> **Halollik / Eslatma:** 1–2 jumla — bu ko'nikma faqat amaliyotda o'sishini yoki ramka cheklovini halol ayt.

---

## <Birinchi bo'lim>
... matn, misollar, SVG, jadval ...

## <Keyingi bo'limlar>
...

## Asosiy g'oyalar (bobni qisqacha)

- 5–7 ta bullet — bobning eng muhim xulosalari, qalin (**bold**) kalit so'zlar bilan.

## Mashqlar

### Oson
**1-mashq.** ...
**2-mashq.** ...

### O'rta
**3-mashq.** ...
**4-mashq.** ...

### Qiyin
**5-mashq.** ...
**6-mashq.** ...

<details markdown="1">
<summary>Yechimlar / Namunaviy yondashuvlar</summary>

### 1-mashq yechimi
...
（har mashq uchun)
</details>

---

<NAV QATORI — pastda takror>
```

### NAV qatori

- **Birinchi bob (01):**
  `[🏠 README](./README.md) · [Keyingi: 02 — O'sish mentaliteti va imposter sindromi ➡️](./02-osish-mentaliteti.md)`
- **Oraliq boblar (02–29):**
  `[⬅️ Oldingi: NN — ...](./NN-oldingi.md) · [🏠 README](./README.md) · [Keyingi: NN — ... ➡️](./NN-keyingi.md)`
- **Oxirgi bob (30):**
  `[⬅️ Oldingi: 29 — Networking, shaxsiy brend va jamoa](./29-networking-shaxsiy-brend.md) · [🏠 README](./README.md)`

NAV qatori **yuqorida** (sarlavhadan keyin) **va pastda** (fayl oxirida) — ikki marta. `[🏠 README](./README.md)` matni AYNAN shu ko'rinishda bo'lsin (QA shuni qidiradi).

---

## 2) Mazmun talablari (har bob)

- **Uzunlik:** ~2200–3200 so'z (jiddiy, to'liq bob; yuza emas).
- **Tuzilish:** 4–7 ta `##` bo'lim. Har biri `###` kichik bo'limlarga bo'linishi mumkin.
- **Ramka (framework) markazda:** har bob kamida 1–2 ta nomlangan, tan olingan ramka/model atrofida qurilsin (masalan: Eisenhower matritsasi, SBI, STAR, Tuckman, Dreyfus, NVC, OKR). Ramkani **kim** yaratganini va **qachon/qayerdan** ekanini to'g'ri ayt (3-bo'lim — grounding).
- **Misol + anti-misol:** abstrakt gapni har doim aniq, dasturchi hayotidan misol bilan tasdiqla. Imkon bo'lsa "yomon yondashuv vs yaxshi yondashuv" qarama-qarshiligini ko'rsat (✅/❌).
- **Suhbat namunalari:** muloqot boblarida (09–17, 27, 28) haqiqiy dialog namunalarini ber — "Xodim: ...", "Lead: ..." ko'rinishida (code blok yoki blockquote ichida). Bu kitobning "kodi" — aynan shu dialoglar.
- **Jadval:** taqqoslash, ramka qadamlari yoki "buzilsa nima bo'ladi" uchun kamida 1 jadval ko'p boblarda foydali.
- **Admonition (ixtiyoriy, lekin tavsiya):** `> **Diqqat:**`, `> **Trade-off:**`, `> **Eslatma:**` blockquote'lar bilan muhim nuqtalarni ajrat. MkDocs `!!! tip` bloklaridan ham foydalanish mumkin, lekin oddiy `>` blockquote yetarli.
- **Mashqlar:** 6 ta (2 oson / 2 o'rta / 2 qiyin). Soft skill mashqlari ko'pincha **reflektiv** ("o'tgan haftadagi bir nizoni eslang va NVC tilida qayta yozing") yoki **rol-o'ynash** ("quyidagi feedback'ni SBI bo'yicha qayta ifodalang"). "To'g'ri javob" bo'lmasa, "Namunaviy yondashuv" ber — bo'sh qoldirma.
- **Asosiy g'oyalar:** 5–7 bullet, qalin kalit so'zlar bilan.

> ⚠️ **Sifat darajasi:** Bu "0 dan Expertgacha" seriyasi. Bob chinakam foydali, chuqur va o'ziga yetarli bo'lsin — Vikipediya konspekti emas, balki amaliyotga tayyor maslahat. Har bobni o'qigan odam ertaga ishda biror narsani boshqacha qilishi kerak.

---

## 3) Grounding — aniqlik SHART

Soft skill kitobida eng katta xavf — **ramkani noto'g'ri odamga nisbat berish** yoki **soxta statistika**. Qoidalar:

- Mashhur ramka/g'oya muallifini **to'g'ri** ayt. Masalan:
  - Growth mindset → **Carol Dweck**
  - Deliberate practice → **K. Anders Ericsson** ("10 000 soat" ni Malcolm Gladwell ommalashtirgan — buni aralashtirma)
  - Deep Work / kontekst → **Cal Newport**
  - Atomic Habits → **James Clear**
  - SBI feedback → **Center for Creative Leadership (CCL)**
  - Radical Candor → **Kim Scott**
  - Nonviolent Communication (NVC) → **Marshall Rosenberg**
  - Psixologik xavfsizlik → **Amy Edmondson**; Google **Project Aristotle** topilmasi
  - Tuckman bosqichlari (forming/storming/norming/performing) → **Bruce Tuckman**
  - Dreyfus skill modeli → **Dreyfus aka-uka**
  - Eisenhower matritsasi → Dwight Eisenhower'ga nisbat beriladi, Stephen Covey ommalashtirgan
  - Imposter sindromi → **Pauline Clance & Suzanne Imes**
  - Dunning–Kruger effekti → **David Dunning & Justin Kruger**
  - "Besh nega" (5 Whys) → **Toyota / Taiichi Ohno**
  - Polya muammo yechish 4 qadami → **George Pólya** ("How to Solve It")
  - SMART maqsad → odatda **George Doran** (1981)
  - Conway qonuni → **Melvin Conway**
- **Aniq bilmasangiz** kim aytganini — "ko'pincha ... ga nisbat beriladi" yoki "keng tarqalgan ramka" deb yumshat, NOTO'G'RI ism qo'yma. Shubha bo'lsa `WebSearch`/`WebFetch` bilan tekshir.
- **Soxta raqam yozma.** "Tadqiqotlar ko'rsatadiki 70%..." kabi aniq statistikani faqat ishonchli bo'lsang yoz; aks holda "ko'p tadqiqotlar shuni ko'rsatadi" deb sifat jihatdan ayt.
- Ortiqcha va'da berma ("bu sizni 1 oyda senior qiladi" — YO'Q). Halol, real ohang.

---

## 4) Imlo va til (KRITIK — QA shuni tekshiradi)

- **FAQAT lotin o'zbek alifbosi.** Matnда birorта **kirill** harf bo'lmasin (о, а, е, с, р, х, у, к, н, м, т, в, и... — bular kirill homoglif, lotin emas!). QA `[Ѐ-ӿ Ԁ-ԯ]` diapazonini qidiradi va topsa — XATO. Klaviaturadan faqat lotin yoz.
- **Apostrof:** `o'`, `g'`, va tutuq belgisi uchun oddiy ASCII apostrof `'` (U+0027) ishlat. Maxsus unicode apostroflar (`ʻ` `'` `'`) ISHLATMA — izchillik uchun faqat `'`.
- **CRLF emas, LF.** Fayllar `\n` bilan tugasin (Write tool buni ta'minlaydi). BOM yo'q.
- O'zbekcha texnik atama: inglizcha so'zni birinchi marta keltirsang qavs ichida asl shaklini ber — masalan "fikr-mulohaza (feedback)", "chuqur ish (deep work)". Keyin o'zbekchasini yoki keng tarqalgan inglizchasini ishlataver.
- Sana/raqamlarni o'zbekcha yoz: "IX asr", "2016-yil".

---

## 5) SVG diagrammalar (KRITIK format)

Har bobda **3 ta** SVG diagramma (ba'zida 2–4). Bu kitob vizual — ramkalar (matritsa, sikl, bosqichlar, model) diagrammada eng yaxshi tushuniladi.

**Joylashuv:** `docs/soft-hard-skills/rasmlar/ssNN-qisqa-nom.svg` (NN = bob raqami). Masalan: `ss05-eisenhower-matritsa.svg`.

**Markdown'da chaqirish:** `![Tavsifiy alt matn](./rasmlar/ssNN-nom.svg)`

**Majburiy SVG qoidalari:**
1. `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H">` — `width`/`height` atributsiz, faqat `viewBox` (responsive). Tipik o'lcham: `820x520` atrofida.
2. Birinchi element — `<title>Diagramma nomi</title>` (SHART — QA tekshiradi, accessibility uchun).
3. **Barcha `font-size` >= 13.** 13 dan kichik matn YO'Q (QA `font-size < 13` ni xato deb biladi). Sarlavha 20–22, kichik izoh 13–14.
4. Shrift: `font-family="Segoe UI"` (yoki `Segoe UI, sans-serif`).
5. **Faqat lotin matn** SVG ichida ham — kirill homoglif yo'q.
6. Fayl BOM'siz, LF bilan.
7. Rang palitrasi (kitob bilan izchil — indigo asos):
   - Fon: `#f8fafc`; sarlavha matni: `#1e293b`; kichik izoh: `#64748b` / `#334155`
   - Asosiy (ko'k): `#2563eb`, fon `#eff6ff`
   - Yashil (ijobiy/✅): `#16a34a`, fon `#f0fdf4`
   - Qizil (xavf/❌): `#dc2626`, fon `#fef2f2`
   - Siyohrang: `#7c3aed`; sariq/kashshof: `#f59e0b`
   - Quti: `fill="#ffffff" stroke="<rang>" stroke-width="2" rx="10"`
8. Diagramma **mazmunli** bo'lsin — shunchaki bezak emas. Matndagi ramkani aks ettirsin (masalan, Eisenhower 2x2 kvadrat, STAR 4 qadam, feedback sikli, Tuckman 4 bosqich grafigi).
9. Matn qutidan toshmasin: qisqa yorliq, kerak bo'lsa `<text>` ni bir nechta qatorga bo'l (alohida `<text>` elementlar bilan).

**Namunaviy SVG (nusxa olib moslang):**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 520">
  <title>Eisenhower matritsasi: shoshilinch va muhim</title>
  <rect x="0" y="0" width="820" height="520" fill="#f8fafc"/>
  <text x="410" y="40" text-anchor="middle" font-family="Segoe UI" font-size="22" font-weight="bold" fill="#1e293b">Eisenhower matritsasi</text>
  <text x="410" y="66" text-anchor="middle" font-family="Segoe UI" font-size="14" fill="#64748b">Vazifani 2 o'lchov bo'yicha ajrating</text>
  <rect x="150" y="110" width="250" height="160" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="275" y="150" text-anchor="middle" font-family="Segoe UI" font-size="16" font-weight="bold" fill="#16a34a">Muhim + Shoshilinch</text>
  <text x="275" y="178" text-anchor="middle" font-family="Segoe UI" font-size="14" fill="#334155">DARHOL BAJAR</text>
  <text x="275" y="202" text-anchor="middle" font-family="Segoe UI" font-size="13" fill="#64748b">Production bug, deadline</text>
  <rect x="420" y="110" width="250" height="160" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="545" y="150" text-anchor="middle" font-family="Segoe UI" font-size="16" font-weight="bold" fill="#2563eb">Muhim + Shoshilinch emas</text>
  <text x="545" y="178" text-anchor="middle" font-family="Segoe UI" font-size="14" fill="#334155">REJALASHTIR</text>
  <text x="545" y="202" text-anchor="middle" font-family="Segoe UI" font-size="13" fill="#64748b">O'rganish, test, refactor</text>
</svg>
```

---

## 6) Cross-link qoidalari (QA tekshiradi)

- Boshqa bobga `[matn](./NN-slug.md)` ko'rinishida havola ber. **Faqat mavjud slug'larga** havola qil (ro'yxat pastda). Noto'g'ri slug → QA xato beradi.
- README'ga: `[README](./README.md)`.
- Boshqa **kitobga** havola (masalan algoritmlar) faqat README'da; bob ichida kerak bo'lsa `../algoritmlar/README.md` ko'rinishida (lekin QA bob-ichi `./NN.md` havolalarni tekshiradi, `../` ni tekshirmaydi — shunisi bilan ehtiyot bo'l, faqat haqiqiy mavjud yo'lga havola qil).
- Tabiiy joyda 2–4 ta cross-link ber ("buni 13-bobda chuqurroq ko'ramiz"). Ortiqcha emas.

### To'liq slug ro'yxati (faqat shularga havola)

```
01-skills-nima-t-shaped
02-osish-mentaliteti
03-organishni-organish
04-bilim-boshqaruvi-eslab-qolish
05-vaqtni-boshqarish
06-diqqat-chuqur-ish
07-maqsad-odatlar
08-stress-burnout-muvozanat
09-texnik-muloqot-asoslari
10-yozma-asinxron-muloqot
11-ogzaki-taqdimot-public-speaking
12-tinglash-savol-berish
13-feedback-berish-qabul
14-jamoada-ishlash-xavfsizlik
15-code-review-inson-tomoni
16-nizolarni-hal-qilish
17-masofaviy-ish-jamoa
18-agile-scrum-jarayonlar
19-muammoni-hal-qilish
20-debugging-tizimli
21-begona-kodni-oqish
22-baholash-rejalashtirish
23-texnik-qaror-tradeoff
24-hujjatlashtirish
25-cv-portfolio-github
26-texnik-intervyu
27-behavioral-intervyu-star
28-maosh-muzokara
29-networking-shaxsiy-brend
30-junior-senior-lead-mentorlik
```

---

## 7) Yakuniy tekshiruv (agent o'zini tekshiradi)

Bobni topshirishdan oldin:
- [ ] Sarlavha `# NN — ...`, yuqori va past NAV qatori bor, `[🏠 README](./README.md)` aynan shu ko'rinishda.
- [ ] `> **Bu bobda:**` intro bor.
- [ ] `## Asosiy g'oyalar` bor (5–7 bullet).
- [ ] `## Mashqlar` (Oson/O'rta/Qiyin) + `<details markdown="1">...</details>` yopiq Yechimlar bilan.
- [ ] 3 ta SVG yaratildi, har biri `<title>` bilan, barcha `font-size >= 13`, faqat lotin, viewBox bor.
- [ ] Matnда va SVG'da **birorта kirill harf yo'q**.
- [ ] Ramka muallifi/manbasi to'g'ri (grounding).
- [ ] Cross-link'lar faqat mavjud slug'larga.
