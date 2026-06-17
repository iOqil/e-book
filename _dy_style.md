# Dasturchi yo'riqnomasi — yagona uslub va skelet (agentlar uchun)

Bu fayl **«Dasturchi yo'riqnomasi»** kitobining barcha boblari uchun majburiy uslub qo'llanmasi.
Har bir bob yozuvchi agent buni o'qiydi va AYNAN shunga amal qiladi. Maqsad — boblararo to'liq izchillik.

Kitob: **Dasturchi yo'riqnomasi — kod yozuvchidan professional muhandisgacha**
Papka: `docs/dasturchi-yoriqnomasi/`  ·  Rasmlar: `docs/dasturchi-yoriqnomasi/rasmlar/`
Til: **o'zbekcha (lotin)**, "siz" murojaati, iliq, amaliy, ortiqcha akademik emas.

## 0) Kitobning mohiyati (har agent yodida tutsin)

Bu kitob **kod yozishni o'rgatmaydi**. U *professional dasturchi BO'LISH* haqida — kod yozuvchini muhandisga aylantiradigan "yumshoq" va kasbiy ko'nikmalar: tafakkur, toza kod hunari, jamoada ishlash, kommunikatsiya, unumdorlik va karyera. Boshqa kitoblar (Git, DevOps, Arxitektura, Algoritmlar, til kitoblari) o'rgatmaydigan "hamma narsa".

**Til-mustaqil.** Kod misollari kerak bo'lganda — psevdokod yoki qisqa, aniq belgilangan snippet (Python yoki JavaScript, qaysi biri tabiiy bo'lsa). Hech qachon biror tilga "bog'lanib qolmang": g'oya tildan muhim. Misol tilini izohda ayting (` ```python `, ` ```js `, ` ```text ` psevdokod uchun).

## 1) Fayl skeleti (HAR bob shu tartibda)

````markdown
# NN — Bob sarlavhasi

[⬅️ Oldingi: NN — ...](./OLDIN-slug.md) · [🏠 README](./README.md) · [Keyingi: NN — ... ➡️](./KEYIN-slug.md)

---

> **Bu bobda:** 2–4 jumlada bob nimani qamrashini ayting (qaysi tushunchalar, qanday ko'nikma).
>
> **Halollik / Eslatma:** halol ramka — bu boblardagi maslahatlar *qonun emas, amaliy yo'l-yo'riq*; kontekstga qarab o'zgaradi; bu yerda fikr/tajriba bor joyini ochiq ayting. Real misollar va kelishuvlar (trade-off) ko'rsatiladi.

---

## (bo'limlar — ## sarlavhalar bilan)

... matn, jadval, diagramma, ✅/❌ misollar, > **Eslatma:**, > **Trade-off:** ...

---

## Asosiy g'oyalar (bobni qisqacha)

- 5–7 ta eng muhim xulosa, qalin **kalit so'z** bilan.

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

(har mashq uchun yechim/namuna javob)

</details>

---

[⬅️ Oldingi: NN — ...](./OLDIN-slug.md) · [🏠 README](./README.md) · [Keyingi: NN — ... ➡️](./KEYIN-slug.md)
````

**Nav qoidalari:**
- Birinchi bob (01): `[🏠 README](./README.md) · [Keyingi: 02 — ... ➡️](./...)` (Oldingi yo'q).
- Oxirgi bob (29): `[⬅️ Oldingi: 28 — ...](./...) · [🏠 README](./README.md)` (Keyingi yo'q).
- Sarlavha/havola matnida apostrof (yo'riqnoma, g'oya) BO'LISHI mumkin; faqat **fayl yo'llarida** apostrof ishlatmang.

## 2) Mazmun sifati (eng muhim qism)

- **Hajm:** har bob to'liq, jiddiy — taxminan 250–420 qator. Yuzaki emas; misol, anti-misol, real vaziyat bilan.
- **Misol + anti-misol:** tushunchani ✅ yaxshi va ❌ yomon misol bilan ko'rsating. Bu kitobning asosiy uslubi.
- **Real hayot:** "real loyihada/jamoada bu shunday ko'rinadi" tipidagi konkret hikoyalar. O'zbekiston/freelance konteksti joiz va xush kelibdi.
- **Trade-off ongi:** har maslahatda "lekin bu har doim to'g'ri emas" — qachon mos, qachon mos emasligini ayting. `> **Trade-off:**` bloki ishlating.
- **Jadval:** taqqoslash (oldin/keyin, daraja, ✅/❌, ne/qachon) uchun markdown jadval — har bobda kamida 1 ta.
- **Kod bloklari:** kerakli joyda. Toza-kod boblarida "oldin (yomon) → keyin (yaxshi)" snippet juftligi juda yaxshi ishlaydi.
- **Cross-link:** boshqa boblarga `[NN-bob](./NN-slug.md)` va boshqa kitoblarga `[Nom](../papka/README.md)` bilan havola qiling (pastdagi ro'yxatga qarang). Slug'ni TAXMIN qilmang — README/ro'yxatdagi aniq slug'dan foydalaning.
- **Mavzuni bosib o'tmang:** o'z bobingiz doirasida qoling; qo'shni bobning materialini takrorlamang, balki unga havola qiling.

## 3) Mashqlar va yechimlar

- **Har bob:** 8 ta mashq (3 Oson + 3 O'rta + 2 Qiyin), `<details>` ichida yechimlar.
- Bu kitobda mashqlar ko'pincha **amaliy/refleksiv**: "bu kodni refactor qiling", "bu vazifani baholang", "bu PR'ga sharh yozing", "bu commit xabarini tuzating", "o'z holatingizni tahlil qiling". Yechimlar — **namuna javob** yoki **mezonlar ro'yxati** (yagona to'g'ri javob bo'lmasligi mumkin — buni ayting).
- Kod bor mashqlarda yechim kodini bering. Psevdokod/aniq til.

## 4) SVG diagrammalar (HAR bob uchun 3 ta)

Har bob **aniq 3 ta** SVG diagramma ishlatadi: `./rasmlar/dyNN-qisqa-nom.svg` (NN = bob raqami).
Matnda: `![Tavsifiy alt matn](./rasmlar/dyNN-nom.svg)`.

**Majburiy SVG qoidalari (QA tekshiradi):**
- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H">` bilan boshlanadi (W,H mos o'lcham, mas. 820×480).
- Birinchi element — `<title>...</title>` (qisqa tavsif). **Title shart.**
- **Hech qanday `font-size` 13 dan kichik bo'lmasin.** Eng kichik matn = `font-size="13"`. Sarlavhalar 18–24, oraliq 14–16, izoh 13.
- Shrift: `font-family="Segoe UI"`.
- Yorug' mavzu: fon `#f8fafc` yoki `#ffffff`. Matn `#1e293b`/`#334155`/`#64748b`. Ranglar: ko'k `#2563eb`, yashil `#16a34a`, qizil `#dc2626`, binafsha `#7c3aed`, sariq/zarhal `#f59e0b`, slate `#1e293b`/`#94a3b8`.
- BOM YO'Q, faqat LF (CRLF emas). Faqat ASCII + o'zbek lotin harflari; **kirill harf ishlatmang** (homoglif xato!). Masalan "с"(kirill) emas "s"(lotin).
- Diagramma mazmunli bo'lsin: konsepsiyani ko'rsatsin (oqim, taqqoslash, narvon, sikl, matritsa), shunchaki bezak emas.

## 5) Til va imlo (KRITIK — QA kirillni rad etadi)

- **Faqat o'zbek lotin alifbosi.** Hech qaerda (matn, kod izohi, SVG) **kirill** harf bo'lmasin. Homoglif xavfi: `o'`, `g'`, `'` (apostrof) to'g'ri yozing; "c/с", "o/о", "a/а", "e/е", "p/р", "x/х" — har doim LOTIN variantini ishlating.
- Apostrof uchun **to'g'ri belgi** `'` (U+02BB emas, oddiy `'` ASCII apostrof U+0027) — butun kitob bo'ylab bir xil: `o'`, `g'`, `bo'lsa`, `yo'q`.
- Texnik atamalar: birinchi marta o'zbekcha + qavsda inglizcha (mas. "texnik qarz (technical debt)"), keyin qisqasi.

## 6) Boshqa kitoblarga cross-link (aniq yo'llar)

- Git & GitHub: `../git-github/README.md`
- DevOps & Deployment: `../devops/README.md`
- Dasturlash arxitekturasi: `../arxitektura/README.md`
- Algoritmlar: `../algoritmlar/README.md`
- 1000 masala: `../1000-masala/README.md`
- Yo'l xaritasi (roadmap): `../roadmap.md`
- Til kitoblari: `../python/README.md`, `../js/README.md`, `../php/README.md`

## 7) Muallif bloki (faqat README oxirida)

```
## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
```

## 8) Tekshiruv (agent o'zini-o'zi nazorat qilsin)

Bobni topshirishdan oldin: (1) skelet to'liqmi (nav, Bu bobda, Halollik, Asosiy g'oyalar, Mashqlar, details, nav)? (2) 3 ta SVG yaratildimi va matnda havola qilindimi? (3) kirill harf yo'qmi? (4) SVG'da font<13 yo'qmi va har birida `<title>` bormi? (5) cross-link slug'lari to'g'rimi? (6) hajm va sifat yetarlimi (misol+anti-misol+trade-off)?
