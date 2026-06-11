# 3.4 Filtrlash va saralash (WHERE, ORDER BY, LIMIT)

[⬅️ Oldingi: 3.3 SQL asoslari — ma'lumot bilan ishlash](./26-sql-asoslari-malumot-bilan-ishlash.md) · [🏠 README](./README.md) · [Keyingi: 3.5 Jadvallarni bog'lash (JOIN) ➡️](./28-jadvallarni-boglash.md)

---

Oldingi bo'limda `SELECT * FROM talabalar` barcha qatorlarni olardi. Lekin ko'pincha bizga **hammasi emas, ma'lum qatorlar** kerak bo'ladi: "faqat Toshkentdagilar", "eng yoshlari", "birinchi 10 tasi". SQL buni juda qulay qiladi.

### Filtrlash — `WHERE`

`WHERE` (3.3'da ko'rgan) faqat shartga mos qatorlarni qaytaradi:

```sql
-- Faqat 20 yoshdan kattalarni olish
SELECT * FROM talabalar WHERE yosh > 20;

-- Faqat Toshkentdagilarni olish
SELECT * FROM talabalar WHERE shahar = 'Toshkent';
```

`WHERE`da 1.4'da o'rgangan taqqoslash amallari ishlaydi: `>`, `<`, `>=`, `<=`, `=` (SQL'da tenglik **bitta** `=` bilan!), `!=`.

Bir nechta shartni birlashtirish (`AND`, `OR` — bular `&&`, `||` ning SQL versiyasi):

```sql
-- 18 dan katta VA Toshkentdagilar
SELECT * FROM talabalar WHERE yosh > 18 AND shahar = 'Toshkent';

-- Toshkent YOKI Samarqanddagilar
SELECT * FROM talabalar WHERE shahar = 'Toshkent' OR shahar = 'Samarqand';
```

Quyidagi diagramma `WHERE` qanday ishlashini ko'rsatadi: har bir qator shart bilan tekshiriladi, faqat shartga mos (rost) qatorlar natijaga kiradi:

![SELECT ... WHERE so'rov oqimi: qaysi qatorlar tanlanadi](rasmlar/phc-select-where-oqim.svg)

> **Diqqat:** SQL'da tenglikni tekshirish **bitta** `=` bilan (`WHERE yosh = 20`). PHP'da `==` edi. SQL'da `=` ham saqlash, ham taqqoslash uchun — chunki kontekst aniq. Buni aralashtirmang.

### Qidiruv — `LIKE`

Matn ichida qidirish uchun `LIKE` ishlatiladi. `%` belgisi "istalgan narsa" degani:

```sql
-- Ismi 'Ali' bilan boshlanadiganlar
SELECT * FROM talabalar WHERE ism LIKE 'Ali%';

-- Ismida 'val' bo'lganlar (qayerda bo'lsa ham)
SELECT * FROM talabalar WHERE ism LIKE '%val%';
```

`'Ali%'` — "Ali bilan boshlanadigan"; `'%val%'` — "ichida val bo'lgan". `%` — joker belgi (o'rnida istalgancha belgi bo'lishi mumkin).

### Saralash — `ORDER BY`

Natijani tartiblaydi:

```sql
-- Yosh bo'yicha o'sish tartibida (kichikdan kattaga)
SELECT * FROM talabalar ORDER BY yosh ASC;

-- Yosh bo'yicha kamayish tartibida (kattadan kichikka)
SELECT * FROM talabalar ORDER BY yosh DESC;

-- Ism bo'yicha alifbo tartibida
SELECT * FROM talabalar ORDER BY ism ASC;
```

- **`ORDER BY yosh`** — "yosh bo'yicha tartibla".
- **`ASC`** — o'sish (ascending, kichikdan kattaga). Standart — agar yozmasangiz, ASC bo'ladi.
- **`DESC`** — kamayish (descending, kattadan kichikka).

### Cheklash — `LIMIT`

Faqat ma'lum sondagi qatorni qaytaradi:

```sql
-- Faqat birinchi 5 ta qator
SELECT * FROM talabalar LIMIT 5;

-- Eng yosh 3 talaba (saralab, keyin cheklash)
SELECT * FROM talabalar ORDER BY yosh ASC LIMIT 3;
```

`LIMIT` ayniqsa katta jadvallarda foydali — "barcha 10000 qatorni emas, faqat birinchi 20 tasini ko'rsat" (masalan, saytda sahifalash uchun).

### Hammasini birga ishlatish

SQL'ning kuchi — bularni birlashtirish mumkin:

```sql
-- Toshkentdagi talabalarni, yoshi bo'yicha kamayish tartibida, eng katta 5 tasi
SELECT ism, yosh
FROM talabalar
WHERE shahar = 'Toshkent'
ORDER BY yosh DESC
LIMIT 5;
```

Tartib muhim: avval `SELECT ... FROM`, keyin `WHERE`, keyin `ORDER BY`, oxirida `LIMIT`.

### Mashqlar

**Oson**
1. `WHERE` bilan 20 yoshdan kattalarni tanlang.
2. `WHERE` bilan ma'lum shahardagilarni tanlang.
3. `ORDER BY` bilan talabalarni yosh bo'yicha saralang.
4. `LIMIT` bilan faqat birinchi 3 qatorni oling.
5. `ORDER BY ism` bilan alifbo tartibida saralang.

**O'rta**
6. `AND` bilan ikki shartni birlashtiring (yosh > 18 va shahar = 'Toshkent').
7. `OR` bilan ikki shahardan birini tanlang.
8. `LIKE 'A%'` bilan ismi A bilan boshlanadiganlarni toping.
9. Eng yosh 3 talabani toping (`ORDER BY yosh ASC LIMIT 3`).
10. `mahsulotlar` dan narxi 50000 dan arzonlarini, narx bo'yicha o'sish tartibida tanlang.

**Qiyin**
11. Toshkentdagi, 20 yoshdan katta talabalarni, ism bo'yicha alifbo tartibida, eng ko'pi 10 ta qilib tanlang (barcha qismlarni birga: `WHERE ... AND ... ORDER BY ... LIMIT ...`).
12. `mahsulotlar` dan: nomida "telefon" so'zi bo'lgan (`LIKE '%telefon%'`), narxi bo'yicha eng qimmat 5 tasini toping.
13. `BETWEEN` ni o'rganing (internetdan): 18 dan 25 gacha bo'lgan talabalarni `WHERE yosh BETWEEN 18 AND 25` bilan toping. Bu `yosh >= 18 AND yosh <= 25` bilan bir xil.

<details markdown="1">
<summary>Yechim — 11</summary>

```sql
SELECT *
FROM talabalar
WHERE shahar = 'Toshkent' AND yosh > 20
ORDER BY ism ASC
LIMIT 10;
```
Diqqat: qismlar aniq tartibda — `WHERE` (filtr), `ORDER BY` (saralash), `LIMIT` (cheklash). Bu tartibni SQL talab qiladi.
</details>

<details markdown="1">
<summary>Yechim — 12 (LIKE va eng qimmat 5 ta)</summary>

```sql
SELECT * FROM mahsulotlar
WHERE nom LIKE '%telefon%'
ORDER BY narx DESC
LIMIT 5;
```
`LIKE '%telefon%'` — nomida "telefon" so'zi bo'lgan (boshida, o'rtasida yoki oxirida) mahsulotlarni topadi. `ORDER BY narx DESC` ularni narx bo'yicha kamayish (qimmatdan arzonga) tartiblaydi, `LIMIT 5` esa eng qimmat 5 tasini qoldiradi.
</details>

<details markdown="1">
<summary>Yechim — 13 (BETWEEN bilan oraliq)</summary>

```sql
SELECT * FROM talabalar WHERE yosh BETWEEN 18 AND 25;

-- Bu quyidagi bilan bir xil:
SELECT * FROM talabalar WHERE yosh >= 18 AND yosh <= 25;
```
`BETWEEN 18 AND 25` — 18 dan 25 gacha (chegaralar **ham kiradi**). Bu `yosh >= 18 AND yosh <= 25` ning qisqa, o'qishli ko'rinishi. Oraliq bo'yicha qidirishda qulay.
</details>
