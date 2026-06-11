# 3.2 phpMyAdmin va birinchi jadval

[⬅️ Oldingi: 3.1 Ma'lumotlar bazasi nima va nega kerak?](./24-malumotlar-bazasi-nima-va-nega-kerak.md) · [🏠 README](./README.md) · [Keyingi: 3.3 SQL asoslari — ma'lumot bilan ishlash ➡️](./26-sql-asoslari-malumot-bilan-ishlash.md)

---

**phpMyAdmin** — bu MySQL bazasini ko'rinadigan, sichqoncha bilan boshqariladigan vosita. U ham XAMPP bilan birga keladi. U yordamida baza va jadvallarni kod yozmasdan, vizual yaratish mumkin — bu boshlovchilar uchun ideal boshlanish.

### phpMyAdmin'ni ochish

1. XAMPP Control Panel'da **Apache** va **MySQL** ikkalasini ham ishga tushiring ("Start" tugmasi, ikkalasi ham yashil bo'lsin).
2. Brauzerda oching: **`http://localhost/phpmyadmin`**
3. phpMyAdmin sahifasi ochiladi — chap tomonda bazalar ro'yxati ko'rinadi.

### Baza yaratish

1. Yuqori menyudan **"Databases"** (Ma'lumotlar bazalari) bo'limiga o'ting.
2. "Create database" maydoniga baza nomini yozing, masalan: **`maktab`**.
3. Yonidagi tanlovni `utf8mb4_general_ci` qoldiring (bu o'zbekcha harflar va emoji to'g'ri saqlanishini ta'minlaydi).
4. **"Create"** tugmasini bosing.

Tabriklaymiz — `maktab` degan bo'sh bazangiz tayyor. Endi unga jadval qo'shamiz.

### Jadval yaratish

1. Chap tomondan yangi yaratgan `maktab` bazasini bosing.
2. "Create table" qismida jadval nomini yozing: **`talabalar`**, ustunlar soni (Number of columns): **4**, "Create" bosing.
3. Endi 4 ta ustunni belgilaymiz:

| Ustun nomi (Name) | Turi (Type) | Uzunlik/qiymat | Qo'shimcha |
|---|---|---|---|
| `id` | INT | — | "A_I" (Auto Increment) belgilang + Primary kalit |
| `ism` | VARCHAR | 100 | — |
| `yosh` | INT | — | — |
| `shahar` | VARCHAR | 50 | — |

4. **"Save"** tugmasini bosing.

Ustun turlari haqida qisqacha:
- **INT** — butun son (`id`, `yosh` kabi).
- **VARCHAR** — qisqa matn (ism, shahar). Yonidagi son (`100`) — eng ko'p necha belgi sig'ishini bildiradi.
- **TEXT** — uzun matn (maqola, izoh kabi). (Bu jadvalda ishlatmadik, lekin bilib qo'ying.)
- **DATE** — sana (`2024-05-20` ko'rinishida).

**`id` ustuni haqida muhim narsa:**
- **AUTO_INCREMENT (A_I)** — "avtomatik o'sish". Har yangi qator qo'shilganda `id` o'zi 1, 2, 3... deb ortadi. Siz `id` haqida o'ylashingiz shart emas — baza o'zi beradi.
- **Primary kalit (PRIMARY KEY)** — bu ustun har bir qatorni noyob qiladigan "asosiy kalit". `id` odatda primary kalit bo'ladi.

Quyidagi diagramma jadvalning asosiy qismlarini ko'rsatadi — ustun (vertikal), qator (gorizontal) va har qatorni noyob qiladigan primary kalit:

![Jadval anatomiyasi: ustun, qator va primary kalit](rasmlar/phc-jadval-anatomiyasi.svg)

### Ma'lumot qo'shish (vizual)

1. Jadval ochilgach, yuqoridan **"Insert"** bo'limiga o'ting.
2. `ism`, `yosh`, `shahar` maydonlarini to'ldiring (`id` ni bo'sh qoldiring — u avtomatik to'ladi).
3. **"Go"** bosing.
4. **"Browse"** bo'limiga o'tib, qo'shilgan qatorni ko'ring.

Bir nechta talaba qo'shing. Endi sizda haqiqiy, diskda saqlanadigan ma'lumot bor — sahifani yangilasangiz ham, kompyuterni o'chirsangiz ham, u joyida qoladi!

> phpMyAdmin — qulay boshlanish, lekin haqiqiy dasturlarda ma'lumotni **kod orqali** qo'shamiz va o'qiymiz. Buning uchun esa MySQL bilan "gaplashish tili" — **SQL** ni o'rganishimiz kerak. Keyingi bo'limda aynan shu.

### Mashqlar

**Oson**
1. phpMyAdmin'ni oching va `maktab` bazasini yarating.
2. `talabalar` jadvalini yuqoridagi 4 ustun bilan yarating.
3. "Insert" orqali 3 ta talaba qo'shing.
4. "Browse" orqali qatorlarni ko'ring.
5. Yangi `shahar` qatorli talaba qo'shib, `id` avtomatik ortishini kuzating.

**O'rta**
6. `mahsulotlar` degan yangi jadval yarating: `id`, `nom` (VARCHAR), `narx` (INT), `soni` (INT).
7. `mahsulotlar`ga 5 ta mahsulot qo'shing.
8. Bir qatorni "Edit" (tahrirlash) orqali o'zgartiring (masalan, narxini).
9. Bir qatorni "Delete" orqali o'chiring va natijani ko'ring.

**Qiyin**
10. `kitoblar` jadvali yarating: `id`, `nom`, `muallif`, `yil` (INT), `mavjud` (bu yerda turini `TINYINT` qiling — 1 yoki 0, ya'ni ha/yo'q). Bir nechta kitob qo'shing.
11. `talabalar` jadvaliga `email` (VARCHAR) ustunini keyinroq qo'shing ("Structure" bo'limidan), mavjud qatorlarga email kiriting.

<details markdown="1">
<summary>Yechim — 10 (kitoblar jadvali)</summary>

phpMyAdmin'da vizual yaratasiz, lekin "ortida" quyidagi SQL ishlaydi (uni "SQL" bo'limida ham bajarish mumkin):

```sql
CREATE TABLE kitoblar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150),
    muallif VARCHAR(100),
    yil INT,
    mavjud TINYINT      -- 1 = bor, 0 = yo'q
);

INSERT INTO kitoblar (nom, muallif, yil, mavjud) VALUES
('O''tkan kunlar', 'Abdulla Qodiriy', 1925, 1),
('Sarob', 'Abdulla Qahhor', 1943, 0);
```

> **`TINYINT` nega "ha/yo'q" uchun?** MySQL'da alohida "boolean" tur yo'q — odatda `TINYINT` ishlatiladi: `1` (ha/true) yoki `0` (yo'q/false). SQL ichida matnda `'` ni ikki marta (`''`) yozib "qochiramiz" (`O''tkan` → `O'tkan`).
</details>

<details markdown="1">
<summary>Yechim — 11 (ustun qo'shish — ALTER TABLE)</summary>

"Structure" bo'limidan vizual qo'shasiz; SQL ko'rinishi:

```sql
-- Yangi ustun qo'shish:
ALTER TABLE talabalar ADD email VARCHAR(150);

-- Mavjud qatorlarga email kiritish:
UPDATE talabalar SET email = 'ali@mail.uz'  WHERE id = 1;
UPDATE talabalar SET email = 'vali@mail.uz' WHERE id = 2;
```
`ALTER TABLE ... ADD` — mavjud jadvalga yangi ustun qo'shadi. Diqqat: yangi ustun avval bo'sh (`NULL`) bo'ladi — keyin `UPDATE` bilan (har doim `WHERE` bilan!) to'ldiramiz.
</details>
