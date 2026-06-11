# 1.5 Matn bilan ishlash (string)

[⬅️ Oldingi: 1.4 Amallar (operatorlar)](./07-amallar.md) · [🏠 README](./README.md) · [Keyingi: 1.6 Shartlar (if/else) ➡️](./09-shartlar.md)

---

Matn (string) — dasturlashda eng ko'p ishlatiladigan ma'lumot turlaridan biri: ismlar, manzillar, xabarlar, sarlavhalar. PHP'da matn ustida turli amallar bajarish uchun maxsus **funksiyalar** bor. Funksiya — bu "tayyor vosita": unga biror narsa berasiz, u natija qaytaradi. (Funksiyalarni o'zingiz yozishni 1.9'da o'rganamiz; hozircha PHP bergan tayyor funksiyalardan foydalanamiz.)

Funksiya shunday ishlatiladi: `funksiya_nomi(nimadir)`. Qavs ichiga "nima ustida ishlashini" yozasiz.

### Matn uzunligini topish — `strlen`

`strlen` matndagi belgilar sonini qaytaradi:

```php
<?php
$ism = "Ali";
echo strlen($ism);   // 3  (3 ta harf)

$parol = "12345";
echo strlen($parol); // 5
```

Bu, masalan, "parol kamida 8 ta belgidan iborat bo'lsin" degan tekshiruvda kerak bo'ladi.

### Katta/kichik harfga o'tkazish — `strtoupper`, `strtolower`

```php
<?php
$ism = "ali";
echo strtoupper($ism);   // ALI   (hammasi katta harf)
echo "<br>";
echo strtolower("SALOM"); // salom (hammasi kichik harf)
```

### Birinchi harfni katta qilish — `ucfirst`

```php
<?php
echo ucfirst("ali");        // Ali
echo "<br>";
echo ucwords("ali valiyev"); // Ali Valiyev  (har so'zning birinchi harfi)
```

### Matnni almashtirish — `str_replace`

Matndagi biror so'zni boshqasiga almashtiradi. Uch narsa beriladi: nimani, nimaga, qayerda:

```php
<?php
$gap = "Men olma yaxshi ko'raman";
echo str_replace("olma", "anor", $gap);   // Men anor yaxshi ko'raman
```

Bu yerda: `"olma"`ni topib, `"anor"`ga almashtir, `$gap` ichida.

### Matnning bir qismini olish — `substr`

Matnning ma'lum qismini kesib oladi. **Diqqat:** dasturlashda sanash **0 dan** boshlanadi (1 dan emas!). Ya'ni birinchi harf — 0-o'rinda, ikkinchisi — 1-o'rinda.

```php
<?php
$soz = "Dasturlash";
echo substr($soz, 0, 4);   // Dast  (0-o'rindan boshlab, 4 ta belgi)
echo "<br>";
echo substr($soz, 4);      // urlash (4-o'rindan oxirigacha)
```

> **Nega 0 dan?** Bu dasturlashda umumiy qoida — deyarli barcha tillarda sanoq 0 dan boshlanadi. Avvaliga g'alati tuyuladi, lekin tez ko'nikasiz. Massivlar (1.8) mavzusida buni yana ko'ramiz.

### Ortiqcha bo'sh joylarni olib tashlash — `trim`

Foydalanuvchi matn kiritganda, ba'zan boshida yoki oxirida keraksiz bo'sh joy qoladi. `trim` ularni tozalaydi:

```php
<?php
$kiritilgan = "   Ali   ";
echo trim($kiritilgan);   // "Ali"  (atrofdagi bo'sh joylar ketdi)
```

### Matnni qidirish — `str_contains`

Matn ichida biror so'z bor-yo'qligini tekshiradi. Natija `true` yoki `false` bo'ladi:

```php
<?php
$gap = "Bugun havo issiq";
var_dump(str_contains($gap, "havo"));   // true  (bor)
var_dump(str_contains($gap, "sovuq"));  // false (yo'q)
```

### Matnni bo'laklarga ajratish va birlashtirish — `explode`, `implode`

Ko'pincha matnni belgilangan ajratgich bo'yicha bo'laklarga ajratish kerak bo'ladi (masalan, vergul bilan yozilgan ro'yxatni). `explode` matnni **massivga** (1.8) aylantiradi:

```php
<?php
$gap = "olma,anor,uzum";
$mevalar = explode(",", $gap);   // ["olma", "anor", "uzum"]
echo $mevalar[1];                // anor
```

`implode` esa aksini qiladi — massivni bitta matnga **birlashtiradi**:

```php
<?php
$royxat = ["Ali", "Vali", "Guli"];
echo implode(", ", $royxat);   // Ali, Vali, Guli
```

`explode("ajratgich", $matn)` — "matnni shu belgi bo'yicha bo'l"; `implode("ulagich", $massiv)` — "massiv elementlarini shu belgi bilan ula". Bu ikkisi matn ↔ massiv o'rtasidagi ko'prik.

### Sonni chiroyli formatlash — `number_format`

Katta sonlarni o'qishli ko'rinishda chiqarish (minglik ajratgich, kasr):

```php
<?php
echo number_format(1234567.891, 2);            // 1,234,567.89
echo number_format(1234567, 0, ".", " ");      // 1 234 567  (o'zbekcha uslub)
```

`number_format(son, kasr_xona, kasr_belgisi, minglik_belgisi)`. Narxlarni ko'rsatishda juda ko'p kerak bo'ladi.

### Andoza bo'yicha matn yasash — `sprintf`

`sprintf` "andoza"ga qiymatlarni joylab, **yangi matn qaytaradi** (`echo` qilmaydi — natijani saqlash mumkin):

```php
<?php
$matn = sprintf("%s — %d yoshda", "Ali", 19);
echo $matn;                          // Ali — 19 yoshda

echo sprintf("Narx: %.2f so'm", 5000);   // Narx: 5000.00 so'm
echo sprintf("ID: %05d", 42);            // ID: 00042  (5 xona, nol bilan)
```

- **`%s`** — matn (string) o'rni, **`%d`** — butun son, **`%.2f`** — 2 kasrli son, **`%05d`** — 5 xonali, yetmasa nol bilan to'ldiriladi.
- Qiymatlar andozadan keyin, tartibda yoziladi.

> **`echo` bilan farqi:** `echo "Ali" . " — " . 19` ham ishlaydi, lekin ko'p qiymat bo'lsa `.` bilan ulash chalkash ko'rinadi. `sprintf` andozani aniq ko'rsatadi — ayniqsa formatlash (kasr, nol to'ldirish) kerak bo'lganda qulay.

### Mashqlar

**Oson**
1. Bir ismni `strlen` bilan o'lchang va uzunligini chiqaring.
2. O'z ismingizni `strtoupper` bilan katta harfda chiqaring.
3. `ucfirst` bilan kichik harfli so'zning birinchi harfini katta qiling.
4. Bir gapdagi so'zni `str_replace` bilan boshqasiga almashtiring.
5. "Dasturlash" so'zining birinchi 4 harfini `substr` bilan oling.

**O'rta**
6. Foydalanuvchi ismi `"  ali  "` shaklida (bo'sh joylar bilan) berilgan. `trim` bilan tozalang, keyin `ucfirst` bilan birinchi harfini katta qiling. Natija: `Ali`.
7. Bir gapda biror so'z bor-yo'qligini `str_contains` bilan tekshiring.
8. To'liq ism (`"ali valiyev"`) ning har bir so'zini `ucwords` bilan katta harf bilan boshlang.
9. Parol uzunligini `strlen` bilan o'lchang va `var_dump` orqali "8 dan katta yoki tengmi" (`>= 8`) ekanini tekshiring.

**Qiyin**
10. Bir ismni oling, uni katta harfga o'tkazing va uzunligini bitta gapda chiqaring: masalan, `"ALI - 3 ta harf"`. (Maslahat: `strtoupper`, `strlen` va `.` ulashdan foydalaning.)
11. Email manzil (`"ali@mail.com"`) ichida `"@"` belgisi bor-yo'qligini tekshiring (`str_contains`). Bu — oddiy email tekshiruvining boshlanishi.
12. `"olma,anor,uzum"` matnini `explode` bilan massivga aylantiring, sonini (`count`) chiqaring, keyin `implode` bilan `" | "` ajratgich bilan qayta birlashtiring.
13. Narx `1234567.5` ni `number_format` bilan minglik ajratgich va 2 kasr bilan chiqaring; keyin `sprintf` bilan `"Mahsulot: <nom>, narxi: <narx> so'm"` ko'rinishida bitta matn yasang.

<details markdown="1">
<summary>Yechim — 6</summary>

```php
<?php
$kiritilgan = "  ali  ";
$tozalangan = trim($kiritilgan);     // "ali"
$natija = ucfirst($tozalangan);      // "Ali"
echo $natija;
```

Yoki bitta qatorda (funksiyalarni "ichma-ich" ishlatib):
```php
<?php
echo ucfirst(trim("  ali  "));   // Ali
```
Bu yerda avval `trim` bo'sh joylarni oladi, keyin uning natijasini `ucfirst` katta harfga o'tkazadi. Funksiyalarni shunday birlashtirish mumkin.
</details>

<details markdown="1">
<summary>Yechim — 10</summary>

```php
<?php
$ism = "ali";
$katta = strtoupper($ism);       // "ALI"
$uzunlik = strlen($ism);         // 3
echo $katta . " - " . $uzunlik . " ta harf";   // ALI - 3 ta harf
```
</details>

<details markdown="1">
<summary>Yechim — 11 (email tekshiruvining boshlanishi)</summary>

```php
<?php
$email = "ali@mail.com";

if (str_contains($email, "@")) {
    echo "Email ko'rinishi to'g'ri (@ bor)";
} else {
    echo "Noto'g'ri email: @ yo'q";
}
```
Bu — eng oddiy tekshiruv: `@` belgisi bormi. Haqiqiy email tekshiruvi murakkabroq (PHP'da `filter_var($email, FILTER_VALIDATE_EMAIL)` tayyor vositasi bor), lekin `str_contains` bilan asosiy g'oyani tushunish — yaxshi boshlanish.
</details>

<details markdown="1">
<summary>Yechim — 12 (explode / implode)</summary>

```php
<?php
$matn = "olma,anor,uzum";
$mevalar = explode(",", $matn);     // ["olma", "anor", "uzum"]

echo count($mevalar);               // 3
echo "<br>";
echo implode(" | ", $mevalar);      // olma | anor | uzum
```
`explode` matnni massivga ajratdi, `implode` esa boshqa ajratgich bilan qayta birlashtirdi. Bu ikkisi — matn va massiv orasida o'tishning eng tez yo'li.
</details>

<details markdown="1">
<summary>Yechim — 13 (number_format va sprintf)</summary>

```php
<?php
$narx = 1234567.5;

echo number_format($narx, 2);   // 1,234,567.50

$satr = sprintf(
    "Mahsulot: %s, narxi: %s so'm",
    "Noutbuk",
    number_format($narx, 2)
);
echo "<br>" . $satr;            // Mahsulot: Noutbuk, narxi: 1,234,567.50 so'm
```
`number_format` sonni o'qishli qildi (minglik vergul + 2 kasr), `sprintf` esa uni andozaga joylab tayyor matn yasadi.
</details>
