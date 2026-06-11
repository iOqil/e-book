# 1.9 Funksiyalar

[⬅️ Oldingi: 1.8 Ro'yxatlar (massivlar)](./11-royxatlar.md) · [🏠 README](./README.md) · [Keyingi: 1.10 Anonim funksiyalar va massiv vositalari (map / filter / reduce) ➡️](./13-anonim-funksiyalar-va-massiv-vosital.md)

---

1.5'da PHP bergan tayyor funksiyalardan (`strlen`, `trim`) foydalangan edik. Endi **o'z funksiyalarimizni** yozishni o'rganamiz. Bu — kodni tartibga solishning eng muhim usuli.

### Funksiya nima va nega kerak?

**Funksiya — biror ishni bajaradigan, nom berilgan kod bo'lagi.** Bir marta yozasiz, keyin nomini chaqirib, istalgancha marta ishlatasiz.

Nega kerak? Tasavvur qiling, dasturingizning 5 ta joyida bir xil hisob-kitob bor. Funksiyasiz — o'sha kodni 5 marta nusxalaysiz. Agar xato topilsa — 5 joyni tuzatasiz. Funksiya bilan — bir joyda yozasiz, 5 joyda chaqirasiz, xatoni bir joyda tuzatasiz. Bu — "takrorlanishdan qoching" degan muhim qoidaning asosi.

### Oddiy funksiya

```php
<?php
function salomlash() {
    echo "Salom, xush kelibsiz!";
}

// Funksiyani chaqirish (ishga tushirish):
salomlash();   // Salom, xush kelibsiz!
salomlash();   // yana chaqirsak — yana ishlaydi
```

Tuzilishi:
- **`function`** — "funksiya yarataman" degan so'z.
- **`salomlash`** — funksiya nomi (o'zingiz tanlaysiz, mazmunli bo'lsin).
- **`( )`** — qavs (hozir bo'sh; keyinroq ichiga "kirish ma'lumotlari"ni yozamiz).
- **`{ }`** — funksiya bajaradigan kod shu ichida.

Funksiyani **yozish** — bu uni ishga tushirish emas. U faqat **chaqirilganda** (`salomlash();`) ishlaydi.

### Funksiyaga ma'lumot berish (parametrlar)

Ko'pincha funksiyaga "kirish ma'lumoti" berish kerak. Masalan, "kimni salomlashni" aytish. Bu ma'lumotlar qavs ichiga yoziladi va **parametr** deyiladi:

```php
<?php
function salomlash($ism) {
    echo "Salom, " . $ism . "!";
}

salomlash("Ali");    // Salom, Ali!
salomlash("Vali");   // Salom, Vali!
```

Bu yerda `$ism` — parametr. Funksiyani chaqirganda qavs ichiga bergan qiymat (`"Ali"`) `$ism`ga tushadi. Endi bitta funksiya har xil ism bilan ishlaydi.

Bir nechta parametr ham berish mumkin (vergul bilan):

```php
<?php
function tanishtir($ism, $yosh) {
    echo $ism . ", " . $yosh . " yosh";
}

tanishtir("Ali", 19);   // Ali, 19 yosh
```

### Natija qaytarish — `return`

Hozirgi funksiyalar ekranga chiqarardi (`echo`). Lekin ko'pincha funksiya biror **natijani hisoblab, qaytarishi** kerak — shunda natijani keyin ishlatamiz. Buning uchun `return` ishlatiladi:

```php
<?php
function yigindi($a, $b) {
    return $a + $b;   // natijani qaytaradi (ekranga chiqarmaydi)
}

$natija = yigindi(5, 3);   // funksiya 8 ni qaytaradi, $natija ga tushadi
echo $natija;              // 8

// To'g'ridan-to'g'ri ham ishlatish mumkin:
echo yigindi(10, 20);      // 30
```

**`echo` va `return` farqi — bu muhim:**
- **`echo`** — natijani **darrov ekranga** chiqaradi, lekin uni keyin ishlata olmaysiz.
- **`return`** — natijani **qaytaradi**, siz uni o'zgaruvchiga saqlab, keyin xohlagancha ishlatasiz (qo'shasiz, taqqoslaysiz, chiqarasiz).

Ko'pincha `return` to'g'ri tanlov, chunki u funksiyani moslashuvchanroq qiladi. `return` bajarilgach, funksiya darrov tugaydi (undan keyingi kod ishlamaydi).

Funksiya chaqiruvini sxemada ko'ramiz: argumentlar funksiyaga kiradi, ichida hisob bajariladi, `return` esa natijani tashqariga qaytaradi.

![Funksiya chaqiruvi: argumentlar kiradi, return natija qaytaradi](rasmlar/pha-funksiya-chaqiruvi.svg)

### Standart (default) qiymatli parametr

Parametrga oldindan qiymat berib qo'yish mumkin — agar chaqirganda qiymat berilmasa, shu ishlatiladi:

```php
<?php
function salomlash($ism = "mehmon") {
    echo "Salom, " . $ism;
}

salomlash("Ali");   // Salom, Ali
salomlash();        // Salom, mehmon   (qiymat berilmadi → standart ishlatildi)
```

### Funksiya ichidagi o'zgaruvchilar "tashqarida ko'rinmaydi"

Funksiya ichida yaratilgan o'zgaruvchi faqat o'sha funksiya ichida yashaydi. Tashqarida u mavjud emas:

```php
<?php
function hisobla() {
    $natija = 100;   // bu o'zgaruvchi faqat funksiya ichida
}

hisobla();
// echo $natija;   // XATO! $natija bu yerda mavjud emas
```

Bu — yaxshi narsa: har bir funksiya "o'z dunyosi"da ishlaydi, bir-biriga xalaqit bermaydi. Tashqaridan ma'lumot kerak bo'lsa — parametr orqali berasiz; natija kerak bo'lsa — `return` bilan qaytarasiz.

### Tip e'lonlari (type declarations) — funksiyani ishonchli qilish

Hozirgacha parametrlar tipsiz edi: `function yigindi($a, $b)`. Lekin PHP'da parametr va natija **tipini** ko'rsatish mumkin — bu professional standart. Funksiya qanday ma'lumot kutishini va nima qaytarishini aniq aytadi:

```php
<?php
function yigindi(int $a, int $b): int {
    return $a + $b;
}

echo yigindi(5, 3);   // 8
```

- **`int $a, int $b`** — "bu parametrlar butun son bo'lishi kerak".
- **`: int`** — "funksiya butun son qaytaradi" (qavsdan keyin, `{` dan oldin).

Asosiy tiplar: `int`, `float`, `string`, `bool`, `array`. Standart qiymat bilan birga ham ishlaydi:

```php
<?php
function chegirma(float $narx, float $foiz = 10.0): float {
    return $narx - ($narx * $foiz / 100);
}

echo chegirma(1000);   // 900
```

**`null` bo'lishi mumkin bo'lsa — `?` qo'yiladi**, qiymat qaytarmasa — `void`:

```php
<?php
function salomla(?string $ism): void {     // $ism string yoki null
    echo "Salom, " . ($ism ?? "mehmon");   // void — hech narsa qaytarmaydi
}

salomla(null);    // Salom, mehmon
salomla("Ali");   // Salom, Ali
```

### `strict_types` — qat'iy tip nazorati

Standart holatda PHP tiplarni "yumshoq" tekshiradi: `yigindi("5", 3)` da `"5"` ni avtomatik `5` ga aylantiradi. Bu xatolarni yashirishi mumkin. Buni oldini olish uchun fayl **eng boshiga** (`<?php` dan keyin, birinchi qator) shuni yozing:

```php
<?php
declare(strict_types=1);

function kvadrat(int $n): int {
    return $n * $n;
}

echo kvadrat(5);     // 25  — to'g'ri
echo kvadrat("5");   // ❌ TypeError: int kutilgan, string berildi
```

`strict_types=1` bilan PHP avtomatik aylantirmaydi — noto'g'ri tip berilsa, darrov **TypeError** beradi. Bu yaxshi: xato yashirinib qolmasdan, darrov ko'rinadi.

> **Why:** tip e'lonlari kodni **o'zini-o'zi hujjatlaydigan** va **ishonchli** qiladi. Funksiyani ko'rgan odam (yoki kelajakdagi siz) nima kutilishini darrov tushunadi, noto'g'ri ma'lumot esa yashirinmasdan xato beradi. Professional PHP kodida tiplar va `strict_types=1` — odat. Boshlanishida hamma funksiyaga tip yozishni mashq qiling.

### Mashqlar

**Oson**
1. `salom()` funksiyasini yozing — chaqirilganda "Assalomu alaykum" chiqarsin.
2. `kvadrat($son)` funksiyasini yozing — sonni o'ziga ko'paytirib **qaytarsin** (`return` bilan).
3. `kopaytir($a, $b)` funksiyasini yozing — ikki sonning ko'paytmasini qaytarsin.
4. `tanishtir($ism, $shahar)` funksiyasini yozing — "Men Ali, Toshkentdanman" shaklida chiqarsin.
5. Standart qiymatli funksiya yozing: `salomlash($ism = "do'st")`.

**O'rta**
6. `eng_katta($a, $b)` funksiyasini yozing — ikki sondan kattasini qaytarsin (`if` bilan).
7. `juftmi($son)` funksiyasini yozing — son juft bo'lsa `true`, toq bo'lsa `false` qaytarsin.
8. `salom_narx($narx)` funksiyasi: narxni olib, 12% QQS qo'shilgan yakuniy narxni qaytarsin.
9. `harf_sanash($matn)` funksiyasi: matndagi belgilar sonini qaytarsin (`strlen`dan foydalaning).
10. `chegirma($narx, $foiz)` funksiyasi: narx va chegirma foizini olib, chegirmadan keyingi narxni qaytarsin.

**Qiyin**
11. `massiv_yigindi($sonlar)` funksiyasi: son massivini parametr sifatida olib, ularning yig'indisini qaytarsin (`foreach` bilan).
12. `eng_katta_massivda($sonlar)` funksiyasi: massivdagi eng katta sonni qaytarsin.
13. `salomlash_royxat($ismlar)` funksiyasi: ismlar massivini olib, har birini "Salom, Ali" ko'rinishida chiqarsin.
14. `tubmi($son)` funksiyasi: son tub bo'lsa `true`, aks holda `false` qaytarsin (1.7'dagi tub son mantig'ini funksiyaga aylantiring).
15. Tip e'lonlari bilan: `kopaytir(int $a, int $b): int` funksiyasini yozing. Keyin `kopaytir("5", 2)` deb chaqiring va faylga `declare(strict_types=1)` qo'yib/olib, xulq farqini kuzating.
16. `formatNarx(float $narx, string $valyuta = "so'm"): string` funksiyasi: narxni `number_format` bilan formatlab, valyuta bilan qaytarsin (masalan, `1,500.00 so'm`).

<details markdown="1">
<summary>Yechim — 7</summary>

```php
<?php
function juftmi($son) {
    if ($son % 2 == 0) {
        return true;
    } else {
        return false;
    }
}

var_dump(juftmi(4));   // bool(true)
var_dump(juftmi(7));   // bool(false)
```

Aslida buni qisqaroq ham yozish mumkin, chunki `$son % 2 == 0` ning o'zi `true`/`false` qiymat beradi:
```php
<?php
function juftmi($son) {
    return $son % 2 == 0;   // to'g'ridan-to'g'ri natijani qaytaradi
}
```
Ikkala variant ham bir xil ishlaydi. Ikkinchisi tajribali dasturchilar yozadigan toza usul.
</details>

<details markdown="1">
<summary>Yechim — 11 (massiv yig'indisi funksiyada)</summary>

```php
<?php
function massiv_yigindi($sonlar) {
    $yigindi = 0;
    foreach ($sonlar as $son) {
        $yigindi += $son;
    }
    return $yigindi;
}

$mening_sonlarim = [10, 20, 30];
echo massiv_yigindi($mening_sonlarim);   // 60
```
E'tibor bering: parametr **massiv** ham bo'lishi mumkin. Funksiya massivni qabul qilib, ichidan o'tib, bitta natija qaytaradi. Bu — funksiyalarning kuchini ko'rsatadi: bir marta yozasiz, istalgan massiv bilan ishlaydi.
</details>

<details markdown="1">
<summary>Yechim — 12 (massivdagi eng katta son)</summary>

```php
<?php
function eng_katta_massivda(array $sonlar) {
    $eng_katta = $sonlar[0];          // birinchisini boshlang'ich deb olamiz
    foreach ($sonlar as $son) {
        if ($son > $eng_katta) {
            $eng_katta = $son;
        }
    }
    return $eng_katta;
}

echo eng_katta_massivda([3, 99, 12, 50]);   // 99
```
1.8'dagi "eng katta son" mantig'ini funksiyaga aylantirdik — endi uni istalgan massiv bilan chaqirish mumkin. (Albatta, tayyor `max($sonlar)` ham bor; bu yerda esa mantiqni o'zimiz yozib mashq qildik.)
</details>

<details markdown="1">
<summary>Yechim — 13 (ro'yxatni salomlash)</summary>

```php
<?php
function salomlash_royxat(array $ismlar): void {
    foreach ($ismlar as $ism) {
        echo "Salom, " . $ism . "<br>";
    }
}

salomlash_royxat(["Ali", "Vali", "Guli"]);
// Salom, Ali
// Salom, Vali
// Salom, Guli
```
Funksiya massivni oladi va har bir elementni `foreach` bilan chiqaradi. Hech narsa qaytarmagani uchun `: void`.
</details>

<details markdown="1">
<summary>Yechim — 14 (tubmi funksiyasi)</summary>

```php
<?php
function tubmi(int $son): bool {
    if ($son < 2) {
        return false;
    }
    for ($i = 2; $i * $i <= $son; $i++) {
        if ($son % $i == 0) {
            return false;     // bo'lindi → tub emas
        }
    }
    return true;              // hech narsaga bo'linmadi → tub
}

var_dump(tubmi(7));    // true
var_dump(tubmi(9));    // false
```
1.7'dagi tub son mantig'ini funksiyaga oldik. E'tibor bering: bu yerda `$tub` o'zgaruvchisi kerak emas — bo'linish topilishi bilan darrov `return false` qilamiz; sikl tugaguncha hech narsa topilmasa `return true`. Bu — funksiyada `return`ning qulayligi.
</details>

<details markdown="1">
<summary>Yechim — 15 (tip e'lonlari va strict_types)</summary>

```php
<?php
declare(strict_types=1);

function kopaytir(int $a, int $b): int {
    return $a * $b;
}

echo kopaytir(5, 2);     // 10  — to'g'ri
echo kopaytir("5", 2);   // ❌ TypeError (strict_types=1 tufayli)
```
`declare(strict_types=1)` ni o'chirsangiz, `kopaytir("5", 2)` `"5"` ni `5` ga aylantirib `10` beradi. Qat'iy rejimda esa darrov xato — bu xatolarni yashirinishdan saqlaydi. Shuning uchun professional kodda qat'iy rejim afzal.
</details>

<details markdown="1">
<summary>Yechim — 16 (formatlangan narx funksiyasi)</summary>

```php
<?php
declare(strict_types=1);

function formatNarx(float $narx, string $valyuta = "so'm"): string {
    return number_format($narx, 2) . " " . $valyuta;
}

echo formatNarx(1500);            // 1,500.00 so'm
echo "<br>";
echo formatNarx(2500.5, "USD");   // 2,500.50 USD
```
Funksiya tiplangan (`float`, `string`), standart qiymatli (`$valyuta = "so'm"`) va matn qaytaradi (`: string`). 1.5'da o'rgangan `number_format` shu yerda asqotdi.
</details>
