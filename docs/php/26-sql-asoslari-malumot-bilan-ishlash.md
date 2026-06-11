# 3.3 SQL asoslari — ma'lumot bilan ishlash

[⬅️ Oldingi: 3.2 phpMyAdmin va birinchi jadval](./25-phpmyadmin-va-birinchi-jadval.md) · [🏠 README](./README.md) · [Keyingi: 3.4 Filtrlash va saralash (WHERE, ORDER BY, LIMIT) ➡️](./27-filtrlash-va-saralash.md)

---

**SQL (Structured Query Language)** — ma'lumotlar bazasi bilan "gaplashish" tili. Bazadan ma'lumot olish, qo'shish, o'zgartirish, o'chirish — hammasi SQL buyruqlari orqali bajariladi. SQL — alohida til (PHP emas), lekin uni o'rganish oson, chunki u deyarli oddiy inglizchaga o'xshaydi.

> **SQL'ni qayerda sinab ko'rish mumkin?** phpMyAdmin'da bazani ochib, yuqoridagi **"SQL"** bo'limiga o'ting — u yerga SQL buyruqlarini yozib, "Go" bosib, natijani ko'rish mumkin. Bu — SQL'ni mashq qilishning eng oson yo'li. Quyidagi barcha buyruqlarni shu yerda sinab ko'ring.

Bazada to'rtta asosiy amal bor. Ularni ko'pincha **CRUD** deb atashadi:
- **C**reate (qo'shish) — `INSERT`
- **R**ead (o'qish) — `SELECT`
- **U**pdate (o'zgartirish) — `UPDATE`
- **D**elete (o'chirish) — `DELETE`

### O'qish — `SELECT`

Eng ko'p ishlatiladigan buyruq. Jadvaldan ma'lumot oladi:

```sql
-- Barcha talabalarning hamma ma'lumotini olish
SELECT * FROM talabalar;
```

- **`SELECT`** — "tanla/ol".
- **`*`** — "hamma ustunlar" degani (yulduzcha).
- **`FROM talabalar`** — "talabalar jadvalidan".

Faqat kerakli ustunlarni olish ham mumkin:

```sql
-- Faqat ism va shaharni olish
SELECT ism, shahar FROM talabalar;
```

> SQL buyruqlari ham `;` (nuqtali vergul) bilan tugaydi — PHP'dagidek. SQL kalit so'zlari (`SELECT`, `FROM`) odatda KATTA harfda yoziladi — bu majburiy emas, lekin o'qishni osonlashtiradigan an'ana.

### Qo'shish — `INSERT`

Jadvalga yangi qator qo'shadi:

```sql
INSERT INTO talabalar (ism, yosh, shahar)
VALUES ('Ali Valiyev', 19, 'Toshkent');
```

- **`INSERT INTO talabalar (...)`** — "talabalar jadvaliga qo'sh, mana shu ustunlarga".
- **`VALUES (...)`** — "mana shu qiymatlarni".
- Ustunlar tartibi va qiymatlar tartibi mos kelishi kerak: `ism` → `'Ali Valiyev'`, `yosh` → `19`, `shahar` → `'Toshkent'`.
- `id` ni yozmadik — chunki u AUTO_INCREMENT, baza o'zi beradi.

> **Diqqat:** SQL'da matn **bittalik tirnoq** (`' '`) ichida yoziladi (`'Ali Valiyev'`), sonlar tirnoqsiz (`19`). Bu PHP'dan biroz farq qiladi (PHP'da qo'shtirnoq ham ishlardi); SQL'da bittalik tirnoq odat.

### O'zgartirish — `UPDATE`

Mavjud qatorni o'zgartiradi:

```sql
UPDATE talabalar
SET shahar = 'Samarqand'
WHERE id = 1;
```

- **`UPDATE talabalar`** — "talabalar jadvalini o'zgartir".
- **`SET shahar = 'Samarqand'`** — "shahar ustunini Samarqandga o'zgartir".
- **`WHERE id = 1`** — "faqat id'si 1 bo'lgan qatorda".

> **JUDA MUHIM:** `UPDATE`da `WHERE` ni **unutmang!** Agar `WHERE` yozmasangiz, **barcha** qatorlar o'zgaradi! Ya'ni `UPDATE talabalar SET shahar = 'Samarqand'` — hamma talabaning shahrini Samarqand qilib qo'yadi. Bu — xavfli xato. Doim `WHERE` bilan qaysi qatorni o'zgartirayotganingizni aniq belgilang.

### O'chirish — `DELETE`

Qatorni o'chiradi:

```sql
DELETE FROM talabalar WHERE id = 3;
```

- **`DELETE FROM talabalar`** — "talabalar jadvalidan o'chir".
- **`WHERE id = 3`** — "id'si 3 bo'lgan qatorni".

> **`DELETE`da ham `WHERE` shart!** `WHERE`siz `DELETE FROM talabalar` — **butun jadvalni** bo'shatadi! Ehtiyot bo'ling.

### Mashqlar

> Quyidagilarni phpMyAdmin'ning "SQL" bo'limida bajaring (avval `talabalar` jadvali to'ldirilgan bo'lsin).

**Oson**
1. `SELECT * FROM talabalar` bilan barcha talabalarni ko'ring.
2. Faqat `ism` ustunini tanlang.
3. `INSERT` bilan yangi talaba qo'shing.
4. `UPDATE` bilan bitta talabaning yoshini o'zgartiring (`WHERE id = ...` bilan).
5. `DELETE` bilan bitta talabani o'chiring.

**O'rta**
6. `ism` va `yosh` ustunlarini birga tanlang.
7. `mahsulotlar` jadvaliga 3 ta yangi mahsulot qo'shing (`INSERT`).
8. Bir mahsulotning narxini `UPDATE` bilan o'zgartiring.
9. Bir talabaning ham yoshini, ham shahrini bir `UPDATE` buyrug'ida o'zgartiring (`SET yosh = ..., shahar = ...`).

**Qiyin**
10. `WHERE`siz `UPDATE` bajarsangiz nima bo'lishini (avval bitta sinov jadvalida) tushuntiring — nega bu xavfli? (Sinab ko'rmang, faqat tushuntiring yoki ehtiyot bo'lib alohida jadvalda sinang.)
11. `kitoblar` jadvalida: barcha 2020-yildan keyin chiqqan kitoblarni tanlash buyrug'ini yozing (`WHERE yil > 2020`). Bu — keyingi bo'lim (filtrlash) ga ko'prik.

<details markdown="1">
<summary>Yechim — 9</summary>

```sql
UPDATE talabalar
SET yosh = 22, shahar = 'Buxoro'
WHERE id = 2;
```
Bir vaqtda bir nechta ustunni o'zgartirish uchun `SET` dan keyin ularni vergul bilan ajratamiz. `WHERE id = 2` esa faqat 2-talabaga ta'sir qilishini kafolatlaydi.
</details>

<details markdown="1">
<summary>Yechim — 10 (WHERE'siz UPDATE nega xavfli)</summary>

```sql
-- ❌ XAVFLI: WHERE yo'q — BARCHA qatorlar o'zgaradi!
UPDATE talabalar SET shahar = 'Toshkent';
-- Endi har bir talabaning shahri "Toshkent" bo'lib qoldi.

-- ✅ TO'G'RI: WHERE bilan aniq qator(lar)ni belgilash
UPDATE talabalar SET shahar = 'Toshkent' WHERE id = 1;
```
`WHERE` yozilmasa, `UPDATE` (va `DELETE`) **butun jadvalga** ta'sir qiladi — bu real loyihada falokat (masalan, hamma foydalanuvchining parolini bittaga aylantirib qo'yish). Shuning uchun `UPDATE`/`DELETE` yozganda **birinchi navbatda `WHERE` haqida o'ylang**. Sinab ko'rmoqchi bo'lsangiz — alohida sinov jadvalida qiling.
</details>

<details markdown="1">
<summary>Yechim — 11 (2020-yildan keyingi kitoblar)</summary>

```sql
SELECT * FROM kitoblar WHERE yil > 2020;
```
`WHERE yil > 2020` faqat `yil` ustuni 2020 dan katta bo'lgan qatorlarni qaytaradi. Bu — keyingi bo'limdagi filtrlashning oddiy ko'rinishi.
</details>
