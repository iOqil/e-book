# 3.5 Jadvallarni bog'lash (JOIN)

[⬅️ Oldingi: 3.4 Filtrlash va saralash (WHERE, ORDER BY, LIMIT)](./27-filtrlash-va-saralash.md) · [🏠 README](./README.md) · [Keyingi: 3.6 PHP'dan bazaga ulanish (PDO) ➡️](./29-phpdan-bazaga-ulanish.md)

---

### Muammo: takrorlanuvchi ma'lumot

Tasavvur qiling, kitoblar jadvalini yaratyapmiz. Har bir kitobning muallifi bor. Eng oddiy yo'l — muallif ismini to'g'ridan-to'g'ri kitoblar jadvaliga yozish:

```
kitoblar:
+----+------------------+------------------+
| id | nom              | muallif          |
+----+------------------+------------------+
| 1  | O'tkan kunlar    | Abdulla Qodiriy  |
| 2  | Mehrobdan chayon | Abdulla Qodiriy  |
| 3  | Sarob            | Abdulla Qahhor   |
+----+------------------+------------------+
```

Muammo ko'rinyaptimi? "Abdulla Qodiriy" ikki marta yozilgan. Agar uning 50 ta kitobi bo'lsa — ism 50 marta takrorlanadi. Va agar ismda xato topilsa (yoki o'zgartirish kerak bo'lsa) — 50 joyni tuzatish kerak. Bu — isrof va xatolar manbai.

### Yechim: ma'lumotni ajratish va bog'lash

To'g'ri yondashuv: mualliflarni **alohida jadvalga** chiqaramiz, kitoblarda esa faqat muallifning **id**'sini saqlaymiz:

```
mualliflar:                      kitoblar:
+----+------------------+        +----+------------------+-----------+
| id | ism              |        | id | nom              | muallif_id|
+----+------------------+        +----+------------------+-----------+
| 1  | Abdulla Qodiriy  |        | 1  | O'tkan kunlar    | 1         |
| 2  | Abdulla Qahhor   |        | 2  | Mehrobdan chayon | 1         |
+----+------------------+        | 3  | Sarob            | 2         |
                                 +----+------------------+-----------+
```

Endi har bir muallif **bir marta** yoziladi. Kitoblar jadvalidagi `muallif_id` ustuni mualliflar jadvalidagi `id` ga ishora qiladi. Masalan, "O'tkan kunlar"ning `muallif_id` = 1, demak uning muallifi — mualliflar jadvalidagi id'si 1 bo'lgan inson (Abdulla Qodiriy).

Bu — **bog'liq jadvallar** (relational database) g'oyasi. `muallif_id` kabi, boshqa jadvalga ishora qiluvchi ustun **tashqi kalit** (foreign key) deb ataladi.

### JOIN — bog'langan ma'lumotni birlashtirish

Endi muammo: kitob nomini **va** muallif ismini birga ko'rsatmoqchimiz. Lekin ular ikki alohida jadvalda. **JOIN** ana shu ikki jadvalni `id` orqali "bir-biriga ulaydi":

```sql
SELECT kitoblar.nom, mualliflar.ism
FROM kitoblar
JOIN mualliflar ON kitoblar.muallif_id = mualliflar.id;
```

Natija:
```
+------------------+------------------+
| nom              | ism              |
+------------------+------------------+
| O'tkan kunlar    | Abdulla Qodiriy  |
| Mehrobdan chayon | Abdulla Qodiriy  |
| Sarob            | Abdulla Qahhor   |
+------------------+------------------+
```

Tushuntiramiz:
- **`SELECT kitoblar.nom, mualliflar.ism`** — ikki jadvaldan ustun olamiz. `jadval.ustun` ko'rinishida yozamiz, chunki ikki jadval bor (qaysi jadvalning ustuni ekanini aniqlash uchun).
- **`FROM kitoblar`** — asosiy jadval.
- **`JOIN mualliflar ON kitoblar.muallif_id = mualliflar.id`** — "mualliflar jadvalini ham qo'sh, ularni shu shart bo'yicha bog'la: kitobning `muallif_id`'si muallifning `id`'siga teng bo'lganda".

`ON` qismi — eng muhimi: u ikki jadvalni qanday bog'lashni aytadi. Bu yerda: "har bir kitobni, uning `muallif_id`'siga mos keladigan muallif bilan birlashtir".

Quyidagi diagramma `JOIN` jarayonini ko'rsatadi: kitoblar jadvalidagi `muallif_id` mualliflar jadvalidagi `id` ga bog'lanadi va ikki jadval bitta natijaga birlashadi:

![JOIN: ikki jadval id orqali bog'lanib birlashadi](rasmlar/phc-join-birlashtirish.svg)

### Nega foydali?

1. **Takrorlanmaslik:** har ma'lumot bir marta saqlanadi (muallif ismi bir joyda).
2. **Oson o'zgartirish:** muallif ismi o'zgarsa — bir joyni tuzatasiz, hamma kitoblarga ta'sir qiladi.
3. **Tartib:** ma'lumot mantiqiy bo'linadi (mualliflar alohida, kitoblar alohida), keyin kerak bo'lganda birlashtiriladi.

> Bu — boshlovchilar uchun biroz murakkab mavzu. Asosiy g'oyani tushunsangiz yetarli: **bog'liq ma'lumotni alohida jadvallarga ajratamiz, keyin JOIN bilan birlashtiramiz.** Amalda ko'p mashq qilsangiz, oydinlashadi.

### Mashqlar

> Avval `mualliflar` va `kitoblar` jadvallarini yarating (phpMyAdmin'da), ma'lumot bilan to'ldiring.

**Oson**
1. `mualliflar` (id, ism) va `kitoblar` (id, nom, muallif_id) jadvallarini yarating.
2. 2 ta muallif va 4 ta kitob qo'shing (kitoblarning `muallif_id`'sini to'g'ri bog'lang).
3. Oddiy `JOIN` bilan kitob nomi va muallif ismini birga chiqaring.

**O'rta**
4. JOIN natijasini muallif ismi bo'yicha saralang (`ORDER BY mualliflar.ism`).
5. Faqat ma'lum bir muallifning kitoblarini JOIN + WHERE bilan toping.
6. `talabalar` va `baholar` (id, talaba_id, fan, ball) jadvallarini yarating, JOIN bilan har bir talabaning bahosini ism bilan chiqaring.

**Qiyin**
7. `talabalar`, `kurslar` (id, nom) va `yozilishlar` (id, talaba_id, kurs_id) jadvallarini yarating. Bu — "ko'pga-ko'p" bog'lanish (bir talaba ko'p kursga, bir kursga ko'p talaba). Ikki JOIN bilan: qaysi talaba qaysi kursga yozilganini ism va kurs nomi bilan chiqaring.
8. JOIN + WHERE + ORDER BY ni birga ishlating: ma'lum bir kursga yozilgan talabalarni, ism bo'yicha tartiblab chiqaring.

<details markdown="1">
<summary>Yechim — 6 (talaba baholari)</summary>

```sql
-- Jadvallar:
-- talabalar (id, ism)
-- baholar (id, talaba_id, fan, ball)

SELECT talabalar.ism, baholar.fan, baholar.ball
FROM baholar
JOIN talabalar ON baholar.talaba_id = talabalar.id
ORDER BY talabalar.ism;
```
Natija har bir bahoni talaba ismi bilan ko'rsatadi, masalan: `Ali | Matematika | 90`. JOIN `baholar.talaba_id` ni `talabalar.id` ga bog'lab, qaysi baho qaysi talabaga tegishli ekanini aniqlaydi.
</details>

<details markdown="1">
<summary>Yechim — 7 (ko'pga-ko'p bog'lanish: ikki JOIN)</summary>

```sql
-- Jadvallar:
-- talabalar (id, ism)
-- kurslar (id, nom)
-- yozilishlar (id, talaba_id, kurs_id)   -- "bog'lovchi" jadval

SELECT talabalar.ism, kurslar.nom
FROM yozilishlar
JOIN talabalar ON yozilishlar.talaba_id = talabalar.id
JOIN kurslar   ON yozilishlar.kurs_id   = kurslar.id;
```
"Ko'pga-ko'p" (bir talaba ko'p kursga, bir kursga ko'p talaba) bog'lanish uchun **oraliq (bog'lovchi) jadval** — `yozilishlar` — ishlatiladi. U faqat ikkita `id`ni (talaba va kurs) bog'laydi. So'rovda **ikkita JOIN**: biri talaba ismini, ikkinchisi kurs nomini olib keladi. Natija: `Ali | Matematika`, `Ali | Fizika`, `Vali | Matematika` ...
</details>

<details markdown="1">
<summary>Yechim — 8 (JOIN + WHERE + ORDER BY)</summary>

```sql
SELECT talabalar.ism
FROM yozilishlar
JOIN talabalar ON yozilishlar.talaba_id = talabalar.id
JOIN kurslar   ON yozilishlar.kurs_id   = kurslar.id
WHERE kurslar.nom = 'Matematika'
ORDER BY talabalar.ism;
```
Bu — "Matematika" kursiga yozilgan talabalarni, ism bo'yicha alifbo tartibida beradi. `JOIN` jadvallarni bog'laydi, `WHERE` kurs bo'yicha filtrlaydi, `ORDER BY` saralaydi — uchalasi birga ishlaydi.
</details>
