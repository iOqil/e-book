# 1.1 Kod qanday yoziladi (sintaksis)

[⬅️ Oldingi: 0.3 Birinchi dasturingiz](./03-birinchi-dasturingiz.md) · [🏠 README](./README.md) · [Keyingi: 1.2 O'zgaruvchilar (variables) ➡️](./05-ozgaruvchilar.md)

---

Har bir tilning o'z qoidalari bor: o'zbek tilida gap bosh harf bilan boshlanib, nuqta bilan tugaydi. Dasturlash tillarining ham shunday qoidalari bor — bularga **sintaksis** deyiladi. Keling, PHP'ning asosiy qoidalarini ko'rib chiqamiz.

### Har bir buyruq nuqtali vergul bilan tugaydi

PHP'da har bir buyruq (amal) `;` bilan tugaydi:

```php
<?php
echo "Birinchi buyruq";
echo "Ikkinchi buyruq";
```

Buni gap oxiridagi nuqta deb tasavvur qiling. Agar `;` qo'ymasangiz, PHP buyruq qayerda tugaganini bilmaydi va xato beradi.

### Yangi qatorga o'tkazish

Yuqoridagi misolda ikkala matn brauzerda yonma-yon chiqadi. Sababi: brauzer "yangi qator"ni maxsus belgi orqali tushunadi. Bu belgi — `<br>`:

```php
<?php
echo "Birinchi qator";
echo "<br>";
echo "Ikkinchi qator";
```

Endi ular ikki qatorda chiqadi. `<br>` — bu brauzerga "shu yerda yangi qatorga o't" degan ishora (bu aslida HTML belgisi, lekin hozir tafsilotga kirmaymiz — shunchaki yangi qator uchun ishlatamiz).

### Izohlar (comments) — kompyuter o'qimaydigan yozuvlar

Ba'zan kodga o'zingiz uchun eslatma yozib qo'yishni xohlaysiz: "bu qator nima qilishini" tushuntirish uchun. Bunday yozuvlar **izoh** deyiladi. Kompyuter izohlarni e'tiborsiz qoldiradi — ular faqat odam o'qishi uchun.

```php
<?php
// Bu bir qatorlik izoh. Kompyuter buni o'qimaydi.
echo "Salom";   // Izohni qator oxiriga ham yozish mumkin

/*
  Bu ko'p qatorlik izoh.
  Bir nechta qatorga cho'zilishi mumkin.
*/
echo "Xayr";
```

- `//` — shu belgidan keyingi matn (o'sha qatorda) izoh hisoblanadi.
- `/* ... */` — bir nechta qatorga cho'zilgan izoh shu ichiga yoziladi.

Izohlar juda foydali: keyinroq kodingizga qaytganingizda, "bu yerda nima qilgan ekanman" deb o'ylamaslik uchun izoh yozib qo'yish odat bo'lishi kerak.

### Katta-kichik harf farqi bor

PHP ba'zi joyda katta-kichik harfni farqlaydi, ba'zi joyda yo'q. Hozircha shuni eslang: **buyruqlarni doim kichik harf bilan yozish odat** — `echo` deb yozing, `ECHO` yoki `Echo` emas. Garchi `ECHO` ham ishlasa-da, kichik harf — qabul qilingan to'g'ri uslub.

### Bo'sh joylar muhim emas (deyarli)

Quyidagi ikkala kod bir xil ishlaydi:

```php
<?php
echo "Salom";
```

```php
<?php
echo     "Salom"     ;
```

Ortiqcha bo'sh joylar (probel) kodning ishlashiga ta'sir qilmaydi. Lekin kodni **toza va o'qiladigan** qilib yozish muhim — keraksiz bo'sh joylarni qoldirmang, har buyruqni alohida qatorga yozing.

### Mashqlar

**Oson**
1. Uchta `echo` yozing va orasiga `<br>` qo'yib, uch qatorda matn chiqaring.
2. Kodingizga `//` bilan bitta izoh qo'shing.
3. `/* ... */` bilan ko'p qatorlik izoh yozing va dasturni ishga tushiring — izoh ekranda chiqmasligini ko'ring.
4. `echo` so'zini `ECHO` deb yozib ko'ring — ishlashini tekshiring (ishlaydi, lekin kichik harf to'g'ri uslub).

**O'rta**
5. O'zingiz haqingizda 3 ta gapni 3 ta alohida qatorda chiqaring (ism, yosh, shahar), orasida `<br>` bilan.
6. Bir nechta `echo` orasiga izohlar yozib, har bir qator nima qilishini tushuntiring.

**Qiyin**
7. Bir necha qatorli "tashrifnoma" (vizitka) yarating: ism, kasb, telefon, har biri yangi qatorda. Izohlar bilan kodni tushuntiring.

<details markdown="1">
<summary>Yechim — 5</summary>

```php
<?php
echo "Ism: Ali";
echo "<br>";
echo "Yosh: 19";
echo "<br>";
echo "Shahar: Toshkent";
```

Brauzerda:
```
Ism: Ali
Yosh: 19
Shahar: Toshkent
```
</details>

<details markdown="1">
<summary>Yechim — 7 (izohli tashrifnoma)</summary>

```php
<?php
// Tashrifnoma — har bir qator alohida ma'lumot
echo "Ism: Ali Valiyev";   // to'liq ism
echo "<br>";
echo "Kasb: Dasturchi";    // kasb
echo "<br>";
echo "Telefon: +998 90 123 45 67";
```
Izohlar (`//`) har bir qator nimani chiqarishini tushuntiradi — kompyuter ularni o'qimaydi, faqat siz uchun. `<br>` esa har bir ma'lumotni yangi qatorga tushiradi.
</details>
