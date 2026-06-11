# 3.1 Ma'lumotlar bazasi nima va nega kerak?

[⬅️ Oldingi: 2.10 Xatolarni boshqarish (try / catch)](./23-xatolarni-boshqarish.md) · [🏠 README](./README.md) · [Keyingi: 3.2 phpMyAdmin va birinchi jadval ➡️](./25-phpmyadmin-va-birinchi-jadval.md)

---

### Muammo: ma'lumot yo'qolib ketadi

Hozirgacha barcha ma'lumotlarimiz o'zgaruvchilarda va massivlarda edi. Lekin bir narsani sezgan bo'lsangiz kerak: **dastur tugashi bilan hamma narsa yo'qoladi.** Sahifani yangilasangiz — massivdagi talabalar ro'yxati g'oyib bo'ladi. Chunki o'zgaruvchilar faqat dastur ishlayotgan paytda, kompyuter "tezkor xotirasi"da yashaydi.

Lekin haqiqiy dasturda ma'lumot **saqlanib qolishi** kerak. Onlayn do'kon mahsulotlarni, foydalanuvchilarni, buyurtmalarni eslab qolishi shart — sayt o'chib-yonsa ham. Ana shu — **doimiy saqlash** muammosi.

### Yechim: ma'lumotlar bazasi

**Ma'lumotlar bazasi (database) — ma'lumotni tartibli va doimiy saqlaydigan tizim.** U ma'lumotni diskka yozadi, shuning uchun dastur yopilsa ham, kompyuter o'chsa ham — ma'lumot saqlanib qoladi. Bundan tashqari, undan ma'lumotni tez topish, qidirish, saralash mumkin.

Ma'lumotni oddiy faylga ham yozish mumkin. Lekin baza ancha kuchli: u minglab yozuvni tez qidiradi, tartibga soladi, bog'laydi va bir vaqtning o'zida ko'p odam bilan ishlay oladi.

### Jadval — Excel jadvaliga o'xshaydi

Bazada ma'lumot **jadvallarda** (table) saqlanadi. Agar Excel yoki Google Sheets ko'rgan bo'lsangiz, jadvalni allaqachon tasavvur qilasiz: **qatorlar** (satrlar) va **ustunlar**.

Masalan, talabalar jadvali shunday ko'rinadi:

```
+----+-------------+------+----------+
| id | ism         | yosh | shahar   |
+----+-------------+------+----------+
| 1  | Ali Valiyev | 19   | Toshkent |
| 2  | Vali Aliyev | 21   | Samarqand|
| 3  | Guli Karim  | 20   | Buxoro   |
+----+-------------+------+----------+
```

- **Ustunlar** (`id`, `ism`, `yosh`, `shahar`) — har bir talaba haqida **qanday ma'lumot** saqlanishini bildiradi. Ular oldindan belgilanadi.
- **Qatorlar** — har bir alohida **yozuv** (bitta talaba). Yuqorida 3 ta talaba bor.
- **`id`** ustuni — har bir qatorning **noyob raqami**. Hech qachon takrorlanmaydi. Bu — har bir yozuvni aniq ajratib olish uchun (xuddi pasport raqami kabi). Deyarli har bir jadvalda `id` bo'ladi.

> Bu — 1.8'da ko'rgan "massiv ichida massiv" tuzilmasiga juda o'xshaydi: ro'yxatdagi har bir element — kalitli ma'lumotlar to'plami. Baza shu g'oyani diskda, tartibli va kuchli tarzda amalga oshiradi.

### MySQL — biz ishlatadigan baza

Ma'lumotlar bazasining turli xil tizimlari bor. Eng mashhurlaridan biri — **MySQL**. Yaxshi xabar: siz uni allaqachon o'rnatgansiz! **XAMPP MySQL'ni ham o'z ichiga oladi.** Shuning uchun alohida hech narsa o'rnatishingiz shart emas.

> MySQL — bu baza **tizimi** (ma'lumotni saqlaydigan dastur). Biz u bilan **SQL** degan til orqali "gaplashamiz" (3.3'da o'rganamiz). Hozircha shuni eslang: MySQL — ombor, SQL — u bilan gaplashish tili.

Keyingi bo'limda XAMPP orqali birinchi bazamizni va jadvalimizni yaratamiz — buni ko'rinadigan, qulay vosita (phpMyAdmin) orqali qilamiz.
