# 3.7 PostgreSQL va MySQL'dan farqlari

[⬅️ Oldingi: 3.6 PHP'dan bazaga ulanish (PDO)](./29-phpdan-bazaga-ulanish.md) · [🏠 README](./README.md) · [Keyingi: 4.1 Formalar va foydalanuvchi ma'lumoti ➡️](./31-formalar-va-foydalanuvchi-malumoti.md)

---

Hozirgacha MySQL bilan ishladik (XAMPP'da bor). Lekin boshqa baza tizimlari ham mavjud. Eng kuchlilaridan biri — **PostgreSQL** (qisqacha "Postgres"). Uni bilish foydali, chunki ko'p loyihalarda ishlatiladi.

Yaxshi xabar: **siz o'rgangan SQL'ning deyarli hammasi PostgreSQL'da ham bir xil ishlaydi.** `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`, `JOIN` — barchasi o'sha-o'sha. Faqat ba'zi kichik farqlar bor.

### Asosiy farqlar

| Mavzu | MySQL | PostgreSQL |
|---|---|---|
| Avtomatik ID | `INT AUTO_INCREMENT` | `SERIAL` |
| Matn turi | `VARCHAR`, `TEXT` | `VARCHAR`, `TEXT` (bir xil) |
| Katta/kichik harf (matn qidirishda) | farq qilmaydi (`=`) | farq qiladi |
| Qidiruvda harf sezmaslik | `LIKE` | `ILIKE` (harf sezmaydigan) |
| Standart o'rnatish | XAMPP'da bor | alohida o'rnatiladi |

Masalan, jadval yaratishda farq faqat ID turida:

```sql
-- MySQL:
CREATE TABLE talabalar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ism VARCHAR(100),
    yosh INT
);

-- PostgreSQL — deyarli bir xil, faqat id boshqacha:
CREATE TABLE talabalar (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(100),
    yosh INT
);
```

Ko'ryapsizmi — farq juda kichik. SQL bilimingiz ikkala bazaga ham yaraydi.

### PHP'dan PostgreSQL'ga ulanish

Eng yoqimli tomoni: PDO ikkala baza bilan ham deyarli bir xil ishlaydi. Faqat **ulanish satrida** `mysql` o'rniga `pgsql` yoziladi:

```php
<?php
// MySQL:
$pdo = new PDO("mysql:host=localhost;dbname=maktab", "root", "");

// PostgreSQL — faqat boshi o'zgaradi:
$pdo = new PDO("pgsql:host=localhost;dbname=maktab", "postgres", "parol");
```

Ulangandan keyin — `query`, `prepare`, `execute`, `fetch` — hammasi bir xil. PDO'ning kuchi shu: bir marta o'rgansangiz, turli bazalar bilan ishlay olasiz.

### Qaysi birini tanlash?

- **MySQL** — keng tarqalgan, o'rganish oson, ko'p hosting qo'llab-quvvatlaydi. Boshlovchi uchun ideal va XAMPP'da tayyor. Hozircha shuni ishlatavering.
- **PostgreSQL** — murakkabroq loyihalar, qat'iyroq qoidalar va kuchli imkoniyatlar kerak bo'lganda yaxshi tanlov.

> **Boshlovchi uchun maslahat:** hozircha MySQL'ga e'tibor bering — u sizda bor va hamma narsani o'rganish uchun yetarli. PostgreSQL borligini va SQL bilimingiz unga ham yarashini bilib qo'ying; kelajakda kerak bo'lganda, uni alohida o'rnatib (rasmiy saytidan), o'sha bilim bilan ishlatasiz.

### Mashqlar

**Oson**
1. MySQL va PostgreSQL'da `CREATE TABLE` ning farqini (faqat ID qismi) yozing.
2. PostgreSQL uchun `talabalar` jadvalini yaratish SQL'ini yozing (`SERIAL` bilan).
3. PDO ulanish satrini MySQL va PostgreSQL uchun yonma-yon yozing.

**O'rta**
4. O'rgangan biror `SELECT ... WHERE ... ORDER BY` so'rovingizni oling — u ikkala bazada ham bir xil ishlashiga ishonch hosil qiling (o'zgartirish kerakmas).
5. `LIKE` (MySQL) va `ILIKE` (PostgreSQL) farqini izohlang — qaysi biri harf katta-kichikligini sezmaydi?

**Qiyin**
6. Agar imkoningiz bo'lsa, PostgreSQL'ni o'rnatib ko'ring (rasmiy saytdan), bitta jadval yarating va MySQL'dagi bilimlaringizni unda sinab ko'ring. (Ixtiyoriy — hozir shart emas.)

<details markdown="1">
<summary>Yechim — 6 (PostgreSQL'da sinash — yo'riqnoma)</summary>

Bu — amaliy, ixtiyoriy mashq. Qadamlar:

1. `postgresql.org/download` dan o'rnating (Windows uchun o'rnatuvchi bor; u bilan birga `pgAdmin` ham keladi — bu PostgreSQL'ning phpMyAdmin'iga o'xshash vositasi).
2. `pgAdmin`da baza yarating (masalan, `maktab`).
3. Jadval yarating — MySQL'dan farqi faqat `id`da:

```sql
CREATE TABLE talabalar (
    id SERIAL PRIMARY KEY,    -- MySQL'dagi AUTO_INCREMENT o'rniga SERIAL
    ism VARCHAR(100),
    yosh INT
);

INSERT INTO talabalar (ism, yosh) VALUES ('Ali', 19);
SELECT * FROM talabalar WHERE yosh > 18 ORDER BY ism;
```

Ko'rasizki, `SELECT`, `INSERT`, `WHERE`, `ORDER BY` — hammasi MySQL'dagidek. Bilimingiz to'liq ishlaydi, faqat `SERIAL` va ulanish qatori (`pgsql:...`) farq qiladi. Maqsad — "SQL bilimi bazadan bazaga ko'chadi" degan ishonchni amalda his qilish.
</details>

---

> **3-QISM yakunlandi!** Endi siz ma'lumotni **doimiy saqlay olasiz** — bu haqiqiy dasturlar yo'lidagi katta qadam. Siz: ma'lumotlar bazasi nima ekanini, phpMyAdmin'da jadval yaratishni, SQL bilan ma'lumot qo'shish/o'qish/o'zgartirish/o'chirishni, filtrlash va saralashni, jadvallarni JOIN bilan bog'lashni, PHP'dan PDO orqali xavfsiz ulanishni (SQL injection'dan himoya bilan) va PostgreSQL farqlarini bilasiz.
>
> Endi sizda haqiqiy dastur yozish uchun barcha asosiy qismlar bor: PHP mantiq (1-QISM), tartibli kod (2-QISM, OOP) va doimiy ma'lumot (3-QISM, baza). Keyingi qismlarda bularni birlashtirib, kodni **professional** darajada tashkil qilishni va ilg'or mavzularni — har birini batafsil tushuntirish bilan — ko'rib chiqamiz.
