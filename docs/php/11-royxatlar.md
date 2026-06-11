# 1.8 Ro'yxatlar (massivlar)

[⬅️ Oldingi: 1.7 Takrorlash (sikllar)](./10-takrorlash.md) · [🏠 README](./README.md) · [Keyingi: 1.9 Funksiyalar ➡️](./12-funksiyalar.md)

---

Hozirgacha bitta o'zgaruvchiga bitta qiymat saqlardik. Lekin ko'pincha **ro'yxat** kerak bo'ladi: 30 ta talaba ismi, 10 ta mahsulot narxi. Har biriga alohida o'zgaruvchi yaratish (`$talaba1`, `$talaba2`, ...) juda noqulay. Yechim — **massiv** (array): bitta o'zgaruvchiga **ko'p qiymat** saqlash.

Massivni "bo'limli quti" deb tasavvur qiling: bitta quti, lekin ichida ko'p bo'lim, har bir bo'limda alohida narsa.

### Oddiy (tartibli) massiv

Qiymatlar `[ ]` ichida, vergul bilan ajratib yoziladi:

```php
<?php
$mevalar = ["olma", "anor", "uzum"];
```

Bu massivda 3 ta qiymat bor. Har biriga **tartib raqami** (indeks) orqali murojaat qilamiz. **Diqqat: sanoq 0 dan boshlanadi** (1.5'da aytib o'tgandek):

```php
<?php
$mevalar = ["olma", "anor", "uzum"];

echo $mevalar[0];   // olma   (birinchi element — 0-indeks)
echo $mevalar[1];   // anor   (ikkinchi — 1-indeks)
echo $mevalar[2];   // uzum   (uchinchi — 2-indeks)
```

`$mevalar[0]` — "mevalar massivining 0-elementi" degani. Kvadrat qavs ichida indeks turadi.

### Massivga element qo'shish

```php
<?php
$mevalar = ["olma", "anor"];
$mevalar[] = "uzum";       // oxiriga qo'shadi
$mevalar[] = "shaftoli";

echo $mevalar[2];   // uzum
echo $mevalar[3];   // shaftoli
```

Bo'sh `[]` — "oxiriga yangi element qo'sh" degani.

### Massivdagi elementlar sonini bilish — `count`

```php
<?php
$mevalar = ["olma", "anor", "uzum"];
echo count($mevalar);   // 3
```

### Massivni ko'rish — `print_r`

Massiv ichida nima borligini ko'rish uchun `echo` ishlamaydi (massivni butunligicha chiqarib bo'lmaydi). Buning uchun `print_r` ishlatamiz:

```php
<?php
$mevalar = ["olma", "anor", "uzum"];
print_r($mevalar);
// Array ( [0] => olma [1] => anor [2] => uzum )
```

`print_r` har bir indeks va uning qiymatini ko'rsatadi. Bu tekshirish uchun foydali.

### `foreach` — massivni aylanib chiqish

Massivdagi **har bir** element ustida amal bajarish kerak bo'lsa, `foreach` sikli ishlatiladi. Bu — massivlar uchun maxsus, eng qulay sikl:

```php
<?php
$mevalar = ["olma", "anor", "uzum"];

foreach ($mevalar as $meva) {
    echo $meva . "<br>";
}
// olma
// anor
// uzum
```

`foreach ($mevalar as $meva)` shunday o'qiladi: "`$mevalar` massividagi **har bir** elementni navbat bilan `$meva`ga sol va ichidagi kodni bajar". Sikl avtomatik ravishda har bir element bo'ylab yuradi — indeks bilan ovora bo'lishingiz shart emas.

> `for` sikli bilan ham massivni aylanib chiqsa bo'ladi (`for ($i = 0; $i < count($mevalar); $i++)`), lekin `foreach` ancha sodda va xavfsiz. Massivlar uchun `foreach`ni afzal ko'ring.

### Kalitli massiv (associative array)

Ba'zan tartib raqami emas, **nom** bo'yicha murojaat qilish qulayroq. Masalan, bir talaba haqida ma'lumot: ismi, yoshi, shahri. Bunda har bir qiymatga **kalit** (nom) beramiz:

```php
<?php
$talaba = [
    "ism" => "Ali",
    "yosh" => 19,
    "shahar" => "Toshkent",
];

echo $talaba["ism"];     // Ali
echo $talaba["yosh"];    // 19
echo $talaba["shahar"];  // Toshkent
```

Bu yerda `=>` belgisi "kalit va qiymat" juftligini bog'laydi: `"ism" => "Ali"` degani "ism kaliti ostida Ali turibdi". Endi `$talaba["ism"]` deb nom orqali murojaat qilamiz (raqam orqali emas). Bu — bir narsa haqida bog'liq ma'lumotlarni birga saqlashning qulay yo'li.

Quyidagi sxema ikki turning farqini ko'rsatadi: indeksli massivda raqamli tartib, kalitli massivda esa har bir qiymat o'z nomi (kaliti) bilan turadi.

![Indeksli massiv (raqam orqali) va kalitli massiv (kalit -> qiymat) farqi](rasmlar/pha-massiv-turlari.svg)

Kalitli massivni ham `foreach` bilan aylanib chiqish mumkin — bunda kalitni ham olamiz:

```php
<?php
$talaba = ["ism" => "Ali", "yosh" => 19, "shahar" => "Toshkent"];

foreach ($talaba as $kalit => $qiymat) {
    echo $kalit . ": " . $qiymat . "<br>";
}
// ism: Ali
// yosh: 19
// shahar: Toshkent
```

### Foydali tayyor massiv funksiyalari

PHP massivlar bilan ishlash uchun ko'p tayyor funksiya beradi. Eng keraklilari:

```php
<?php
$mevalar = ["olma", "anor", "uzum"];

// Element bormi? — in_array
var_dump(in_array("anor", $mevalar));    // true
var_dump(in_array("banan", $mevalar));   // false

// Saralash (massivning o'zini o'zgartiradi)
$sonlar = [3, 1, 4, 1, 5];
sort($sonlar);     // o'sish:   [1, 1, 3, 4, 5]
rsort($sonlar);    // kamayish: [5, 4, 3, 1, 1]

// Hisob-kitob
echo array_sum([10, 20, 30]);   // 60
echo max([10, 20, 30]);         // 30
echo min([10, 20, 30]);         // 10
echo count($mevalar);           // 3  (1.8 boshida ko'rgan)
```

Kalitli massivlar uchun:

```php
<?php
$talaba = ["ism" => "Ali", "yosh" => 19, "shahar" => "Toshkent"];

print_r(array_keys($talaba));     // ["ism", "yosh", "shahar"]  — faqat kalitlar
print_r(array_values($talaba));   // ["Ali", 19, "Toshkent"]    — faqat qiymatlar
```

- **`in_array($qiymat, $massiv)`** — qiymat massivda bormi (`true`/`false`).
- **`sort` / `rsort`** — o'sish / kamayish tartibida saralaydi. Diqqat: ular massivning **o'zini** o'zgartiradi (yangi massiv qaytarmaydi).
- **`array_sum`, `max`, `min`, `count`** — yig'indi, eng katta, eng kichik, soni.
- **`array_keys` / `array_values`** — kalitli massivdan faqat kalitlarni yoki faqat qiymatlarni ajratib oladi.

> **Why:** bu funksiyalarni o'zingiz `foreach` bilan yozish mumkin (1.8 mashqlarida shuni qildik), lekin tayyor funksiya — qisqaroq, tezroq va xatosizroq. "Eng katta sonni topish"ni qo'lda yozish — yaxshi mashq; real kodda esa `max()` ishlatiladi. Murakkabroq, "o'z qoidam bilan" saralashni (masalan, narx bo'yicha) keyingi bo'limda (`usort`) ko'ramiz.

### Element qo'shish va olib tashlash — `push`, `pop`, `shift`, `unshift`

`$massiv[] = ...` oxiriga element qo'shadi. Lekin ba'zan **boshidan** qo'shish yoki olib tashlash kerak bo'ladi. PHP buning uchun 4 ta funksiya beradi. Ularni "massiv-quti" ustida amal deb tasavvur qiling:

```php
<?php
$savat = ["olma", "anor"];

array_push($savat, "uzum");             // oxiriga qo'shadi
array_push($savat, "shaftoli", "behi"); // bir vaqtda bir nechta

echo implode(", ", $savat);   // olma, anor, uzum, shaftoli, behi

$oxirgi = array_pop($savat);  // oxirgini olib tashlaydi VA qaytaradi
echo $oxirgi;                 // behi

$birinchi = array_shift($savat);  // boshidan olib tashlaydi VA qaytaradi
echo $birinchi;                   // olma

array_unshift($savat, "nok");     // boshiga qo'shadi
echo implode(", ", $savat);       // nok, anor, uzum, shaftoli
```

Yodda saqlash uchun jadval:

| Funksiya | Nima qiladi | Qayer |
|----------|-------------|-------|
| `array_push($m, $x)` | qo'shadi | oxiriga |
| `array_pop($m)` | olib tashlaydi va qaytaradi | oxiridan |
| `array_unshift($m, $x)` | qo'shadi | boshiga |
| `array_shift($m)` | olib tashlaydi va qaytaradi | boshidan |

> `array_push($savat, "uzum")` bilan `$savat[] = "uzum"` bir xil ish qiladi — bittagina element qo'shsangiz, `[]` qisqaroq. `array_push` faqat bir vaqtda bir nechta qo'shganda foydaliroq. `pop` va `shift` esa olib tashlangan elementni **qaytaradi** — shuning uchun ularni o'zgaruvchiga olish mumkin.

### Indeks bo'yicha qidirish — `array_search`

`in_array` faqat "bormi?" (`true`/`false`) deydi. Agar elementning **qaysi indeksda** turganini bilmoqchi bo'lsangiz, `array_search` ishlating:

```php
<?php
$mevalar = ["olma", "anor", "uzum"];

var_dump(in_array("anor", $mevalar));   // bool(true)  — shunchaki bormi

$indeks = array_search("uzum", $mevalar);
var_dump($indeks);   // int(2)  — "uzum" 2-indeksda turibdi

$yoq = array_search("banan", $mevalar);
var_dump($yoq);      // bool(false)  — topilmadi
```

> **Diqqat — `0` tuzog'i:** birinchi element 0-indeksda turadi. Agar element topilsa-yu, u 0-indeksda bo'lsa, `array_search` `0` qaytaradi — bu esa `if` ichida `false` deb qabul qilinadi! Shuning uchun har doim `!== false` bilan tekshiring:

```php
<?php
$narxlar = [100, 200, 300];
$natija = array_search(100, $narxlar);   // int(0)

if ($natija !== false) {                 // === o'rniga !== false MUHIM
    echo "Topildi, indeks: " . $natija;  // Topildi, indeks: 0
}
```

### Kalitlarni qiymat bilan topish — `array_keys`

`array_keys` odatda barcha kalitlarni beradi (yuqorida ko'rdik). Lekin unga ikkinchi argument bersangiz — **shu qiymatga ega** barcha kalitlarni topadi:

```php
<?php
$ball = ["Ali" => 85, "Vali" => 72, "Guli" => 85];

print_r(array_keys($ball, 85));   // ["Ali", "Guli"]  — 85 ball olganlar
```

### Massivlarni birlashtirish — `array_merge`, `array_combine`

`array_merge` ikki (yoki undan ko'p) massivni **ketma-ket ulaydi**:

```php
<?php
$a = ["olma", "anor"];
$b = ["uzum", "behi"];

$hammasi = array_merge($a, $b);
print_r($hammasi);   // ["olma", "anor", "uzum", "behi"]
```

`array_combine` esa bitta massivni **kalit**, ikkinchisini **qiymat** qilib, kalitli massiv yasaydi (ikkalasi teng uzunlikda bo'lishi shart):

```php
<?php
$mahsulotlar = ["olma", "anor", "uzum"];
$narxlar     = [12000, 25000, 18000];

$narxnoma = array_combine($mahsulotlar, $narxlar);
print_r($narxnoma);
// ["olma" => 12000, "anor" => 25000, "uzum" => 18000]
```

Bu — ikki alohida ro'yxatni (masalan, ustun nomlari va qatordagi qiymatlar) bitta qulay kalitli massivga aylantirishning eng tez yo'li.

### Bir qismini olish/o'chirish — `array_slice`, `array_splice`

`array_slice` massivning **bir bo'lagini oladi** (asl massivga tegmaydi — yangisini qaytaradi):

```php
<?php
$harflar = ["a", "b", "c", "d", "e"];

print_r(array_slice($harflar, 1, 3));   // ["b", "c", "d"]  (1-indeksdan 3 ta)
print_r(array_slice($harflar, -2));     // ["d", "e"]       (oxirgi 2 ta)
print_r($harflar);                       // o'zgarmagan: a, b, c, d, e
```

`array_splice` esa massivni **o'zgartiradi**: bir qismini o'chiradi (xohlasangiz o'rniga yangisini qo'yadi):

```php
<?php
$ranglar = ["qizil", "yashil", "ko'k", "sariq"];

$olingan = array_splice($ranglar, 1, 2);  // 1-indeksdan 2 tasini o'chir
print_r($olingan);   // ["yashil", "ko'k"]  — o'chirilganlar
print_r($ranglar);   // ["qizil", "sariq"]  — qolgani

// O'rniga yangisini qo'yish (4-argument)
$sonlar = [1, 2, 3, 4, 5];
array_splice($sonlar, 1, 2, ["x", "y", "z"]);  // 2 tani 3 ta bilan almashtir
print_r($sonlar);   // [1, "x", "y", "z", 4, 5]
```

> **Esda tuting:** `slice` — *kesib oladi, lekin asliga tegmaydi*; `splice` — *kesib oladi va aslidan o'chiradi*. Nomi o'xshash, lekin biri xavfsiz (nusxa), biri o'zgartiruvchi.

### Massivlarni solishtirish — `array_diff`, `array_intersect`

`array_diff` — birinchi massivda bor, lekin ikkinchisida **yo'q** elementlarni qaytaradi (ayirma). `array_intersect` — **ikkalasida ham** bor elementlarni qaytaradi (umumiy):

```php
<?php
$kecha = ["olma", "anor", "uzum", "behi"];
$bugun = ["anor", "behi", "nok"];

print_r(array_diff($kecha, $bugun));        // ["olma", "uzum"]  — faqat kechagilardagisi
print_r(array_intersect($kecha, $bugun));   // ["anor", "behi"]  — ikkalasida ham bor
```

Bu juda amaliy: "omborda yo'q mahsulotlar", "ikkala ro'yxatda ham bor foydalanuvchilar" kabi savollarga bir qatorda javob beradi.

### Tozalash va aylantirish — `array_unique`, `array_reverse`, `array_flip`

```php
<?php
// array_unique — takrorlanganlarni olib tashlaydi
$sonlar = [1, 2, 2, 3, 3, 3, 4];
print_r(array_unique($sonlar));   // [1, 2, 3, 4]

// array_reverse — teskari tartibga keltiradi
$mevalar = ["olma", "anor", "uzum"];
print_r(array_reverse($mevalar));   // ["uzum", "anor", "olma"]

// array_flip — kalit va qiymatni almashtiradi
$rang = ["q" => "qizil", "k" => "ko'k"];
print_r(array_flip($rang));   // ["qizil" => "q", "ko'k" => "k"]
```

> `array_unique` indekslarni saqlaydi (1, 2, 4-indekslar tushib qolishi mumkin). Agar "toza" 0,1,2... indeks kerak bo'lsa, ustidan `array_values(...)` o'rab oling.

### Obyekt massividan ustun olish — `array_column`

Real dasturlarda massiv ichida kalitli massivlar bo'ladi (masalan, bazadan kelgan qatorlar). Ulardan bitta "ustun"ni ajratib olish uchun `array_column` ishlatiladi:

```php
<?php
$talabalar = [
    ["id" => 1, "ism" => "Ali",  "ball" => 85],
    ["id" => 2, "ism" => "Vali", "ball" => 72],
    ["id" => 3, "ism" => "Guli", "ball" => 95],
];

// Faqat "ism" ustunini ajratib olish
print_r(array_column($talabalar, "ism"));   // ["Ali", "Vali", "Guli"]

// Faqat ballarni olib, o'rtachasini hisoblash
$ballar = array_column($talabalar, "ball");
echo "O'rtacha: " . (array_sum($ballar) / count($ballar));   // 84

// 3-argument: qaysi maydon KALIT bo'lsin
print_r(array_column($talabalar, "ism", "id"));
// [1 => "Ali", 2 => "Vali", 3 => "Guli"]
```

`foreach` bilan ustunni qo'lda yig'ishingiz ham mumkin edi, lekin `array_column` buni bir qatorda qiladi — jadval ko'rinishidagi ma'lumotlar bilan ishlaganda eng ko'p ishlatiladigan funksiyalardan biri.

### Bo'laklarga bo'lish — `array_chunk`

`array_chunk` massivni teng **bo'laklarga** ajratadi. Sahifalashda (har sahifada N ta element) juda qo'l keladi:

```php
<?php
$sonlar = [1, 2, 3, 4, 5, 6, 7];

print_r(array_chunk($sonlar, 3));
// [ [1,2,3], [4,5,6], [7] ]   — oxirgi bo'lak to'liq bo'lmasligi mumkin

$sahifalar = array_chunk($sonlar, 3);
echo "Sahifalar soni: " . count($sahifalar);   // 3
echo "1-sahifa: " . implode(", ", $sahifalar[0]);   // 1, 2, 3
```

### Massiv yasash — `range`, `array_fill`

Qo'lda yozmasdan, tayyor massiv hosil qilish:

```php
<?php
// range — ketma-ket sonlar yoki harflar
print_r(range(1, 5));        // [1, 2, 3, 4, 5]
print_r(range(0, 10, 2));    // [0, 2, 4, 6, 8, 10]  (qadami 2)
print_r(range("a", "e"));    // ["a", "b", "c", "d", "e"]

// array_fill — bir xil qiymat bilan to'ldirish
print_r(array_fill(0, 3, "bo'sh"));   // ["bo'sh", "bo'sh", "bo'sh"]

// Foydali: 1 dan 100 gacha yig'indi — bir qatorda
echo array_sum(range(1, 100));   // 5050
```

> `range(1, 5)` — `for ($i = 1; $i <= 5; $i++)` o'rniga qisqa yo'l. `foreach (range(1, 5) as $i)` deb yozish mumkin, lekin katta diapazonlarda `for` tejamkorroq (`range` butun massivni xotirada yasaydi).

### Yig'indi va ko'paytma — `array_sum`, `array_product`

`array_sum`ni yuqorida ko'rdik. Uning juftligi — `array_product` (barcha elementlarni ko'paytiradi):

```php
<?php
$sonlar = [2, 3, 4];

echo array_sum($sonlar);       // 9   (2+3+4)
echo array_product($sonlar);   // 24  (2*3*4)
```

### Saralash oilasi — qaysi birini qachon?

`sort`/`rsort` qiymatlarni saralaydi, lekin **kalitlarni yo'qotadi** (qayta 0,1,2... qiladi). Kalitli massivlarda bu yomon — "Ali"ning balini saralagach, kim qaysi ball olganini bilmay qolamiz. Shuning uchun PHP'da butun bir saralash oilasi bor:

```php
<?php
// 1) sort / rsort — QIYMAT bo'yicha, kalitlar yo'qoladi
$sonlar = [3, 1, 4, 1, 5];
sort($sonlar);    // [1, 1, 3, 4, 5]  o'sish
rsort($sonlar);   // [5, 4, 3, 1, 1]  kamayish

// 2) asort / arsort — QIYMAT bo'yicha, lekin KALITLAR saqlanadi
$ball = ["Ali" => 85, "Vali" => 72, "Guli" => 95];
asort($ball);    // Vali=>72, Ali=>85, Guli=>95   (kim qancha — saqlanadi!)
arsort($ball);   // Guli=>95, Ali=>85, Vali=>72   (kamayish)

// 3) ksort / krsort — KALIT bo'yicha
$yosh = ["Guli" => 19, "Ali" => 21, "Vali" => 20];
ksort($yosh);    // Ali, Guli, Vali   (alifbo bo'yicha kalit)
krsort($yosh);   // Vali, Guli, Ali   (teskari)
```

Tanlash jadvali:

| Nimaga qarab? | O'sish | Kamayish | Kalit saqlanadimi? |
|---------------|--------|----------|--------------------|
| Qiymat (oddiy massiv) | `sort` | `rsort` | yo'q |
| Qiymat (kalitli massiv) | `asort` | `arsort` | ha |
| Kalit | `ksort` | `krsort` | ha |

> Oddiy `[10, 30, 20]` kabi massivni saralasangiz — `sort`. Kalitli `["Ali" => 85, ...]` massivni ball bo'yicha saralab, kalitni saqlamoqchi bo'lsangiz — `asort`. Kalit (ism, sana) bo'yicha tartiblamoqchi bo'lsangiz — `ksort`.

### O'z qoidam bilan saralash — `usort`, `uasort`

Yuqoridagilar oddiy qiymatlar uchun. Lekin massiv ichida **kalitli massivlar** bo'lsa (talabalar, mahsulotlar), "ball bo'yicha" yoki "narx bo'yicha" saralash kerak. Buning uchun `usort` — unga **o'z solishtirish qoidangizni** beramiz:

```php
<?php
$talabalar = [
    ["ism" => "Ali",  "ball" => 85],
    ["ism" => "Vali", "ball" => 72],
    ["ism" => "Guli", "ball" => 95],
];

// usort — ball bo'yicha kamayish tartibida
usort($talabalar, function ($a, $b) {
    return $b["ball"] - $a["ball"];   // katta ball oldinga
});

foreach ($talabalar as $t) {
    echo $t["ism"] . " - " . $t["ball"] . "\n";
}
// Guli - 95
// Ali - 85
// Vali - 72
```

Solishtirish funksiyasi ikki element (`$a` va `$b`) oladi va son qaytaradi: **manfiy** — `$a` oldinga, **musbat** — `$b` oldinga, **0** — teng. `$a - $b` o'sish, `$b - $a` kamayish beradi.

Zamonaviy PHP'da bu funksiyani **ko'rsatkichli funksiya** (arrow function, `fn`) bilan qisqaroq yozamiz:

```php
<?php
$talabalar = [
    ["ism" => "Ali",  "ball" => 85],
    ["ism" => "Vali", "ball" => 72],
    ["ism" => "Guli", "ball" => 95],
];

usort($talabalar, fn($a, $b) => $a["ball"] - $b["ball"]);   // o'sish

echo $talabalar[0]["ism"];   // Vali  (eng kichik ball birinchi)
```

`uasort` — xuddi `usort` kabi, lekin **kalitlarni saqlaydi**:

```php
<?php
$narx = ["olma" => 12000, "anor" => 25000, "uzum" => 18000];

uasort($narx, fn($a, $b) => $a - $b);   // narx o'sishi, lekin kalit (nom) qoladi
print_r($narx);
// ["olma" => 12000, "uzum" => 18000, "anor" => 25000]
```

> **Why:** `usort` — saralashning eng kuchli shakli. "Eng arzon mahsulot", "eng baland ballik talaba", "yangi sanadagi buyurtmalar" — bularning hammasi `usort` bilan bir qatorda hal bo'ladi. Funksiya/ko'rsatkichli funksiya (`fn`) keyingi bobda batafsil, hozircha shu shaklni "saralash retsepti" deb qabul qiling.

### Yoyish operatori `...` (spread)

`...` operatori massivni boshqa massiv ichiga **yoyadi** (ochib tashlaydi):

```php
<?php
$asosiy    = ["olma", "anor"];
$qoshimcha = ["uzum", "behi"];

$hammasi = [...$asosiy, ...$qoshimcha, "nok"];
print_r($hammasi);   // ["olma", "anor", "uzum", "behi", "nok"]
```

Bu `array_merge`ga o'xshaydi, lekin sintaksisi qisqaroq va massiv literalining istalgan joyiga qo'shimcha element qo'shsa bo'ladi. Kalitli massivlarni ham birlashtirish mumkin (PHP 8.1+), bunda keyingi qiymat oldingisini qayta yozadi:

```php
<?php
$standart = ["rang" => "qora", "olcham" => "M"];

$buyurtma = [...$standart, "olcham" => "L"];   // olcham qayta yoziladi
print_r($buyurtma);   // ["rang" => "qora", "olcham" => "L"]
```

> Bu "standart sozlamalar + foydalanuvchi o'zgartirgan qiymatlar" naqshida juda qulay: avval standartni yoyamiz, keyin ustidan o'zgartirishlarni qo'yamiz.

### Massivni o'zgaruvchilarga yoyish — destructuring `[$a, $b]`

Massiv elementlarini **bir nechta o'zgaruvchiga** bir qatorda taqsimlash mumkin:

```php
<?php
$koordinata = [41, 69];
[$x, $y] = $koordinata;       // $x = 41, $y = 69
echo "x=$x, y=$y";            // x=41, y=69

// Ba'zilarini tashlab ketish (bo'sh joy qoldirib)
$rgb = [255, 128, 0];
[, $yashil, ] = $rgb;         // faqat o'rtadagini olamiz
echo $yashil;                 // 128

// Kalitli massivni ham yoyish mumkin
$talaba = ["ism" => "Ali", "yosh" => 19];
["ism" => $ism, "yosh" => $yosh] = $talaba;
echo "$ism, $yosh yosh";      // Ali, 19 yosh
```

`foreach` ichida bu ayniqsa kuchli — har bir qatorni darhol nomli o'zgaruvchilarga ajratamiz:

```php
<?php
$juftliklar = [[1, "a"], [2, "b"], [3, "c"]];

foreach ($juftliklar as [$raqam, $harf]) {
    echo "$raqam => $harf\n";
}
// 1 => a
// 2 => b
// 3 => c
```

> `[$a, $b] = ...` — bu eski `list($a, $b) = ...` ning zamonaviy, qisqa shakli. Ikkalasi bir xil ishlaydi, lekin yangi kodda kvadrat qavs shakli afzal.

### O'zgaruvchi va massiv orasida — `compact`, `extract`

`compact` mavjud o'zgaruvchilardan kalitli massiv yasaydi (kalit — o'zgaruvchi nomi):

```php
<?php
$ism = "Ali";
$yosh = 19;
$shahar = "Toshkent";

$talaba = compact("ism", "yosh", "shahar");
print_r($talaba);
// ["ism" => "Ali", "yosh" => 19, "shahar" => "Toshkent"]
```

`extract` esa teskarisini qiladi — kalitli massivdan o'zgaruvchilar yasaydi:

```php
<?php
$mahsulot = ["nom" => "Olma", "narx" => 12000];

extract($mahsulot);          // $nom va $narx o'zgaruvchilari paydo bo'ladi
echo "$nom — $narx so'm";    // Olma — 12000 so'm
```

> `compact` shablonlarga ma'lumot uzatishda ko'p ishlatiladi. `extract`ni esa ehtiyot bo'lib ishlating — u mavjud o'zgaruvchilarni jimgina qayta yozib yuborishi mumkin; ishonchsiz (masalan, foydalanuvchidan kelgan) ma'lumotga hech qachon qo'llamang.

### Ko'p o'lchovli massiv — chuqurroq

Massiv ichida yana massiv bo'lishi mumkin — bu "ko'p o'lchovli massiv". Eng ko'p uchraydigani — **jadval** (qatorlar va ustunlar):

```php
<?php
$jadval = [
    ["Ali",  85, 90],
    ["Vali", 72, 68],
    ["Guli", 95, 88],
];

// Bitta katakka murojaat: [qator][ustun]
echo $jadval[0][0];   // Ali
echo $jadval[2][1];   // 95

// Ichma-ich foreach bilan butun jadvalni aylanish
foreach ($jadval as $qator) {
    echo implode(" | ", $qator) . "\n";
}
// Ali | 85 | 90
// Vali | 72 | 68
// Guli | 95 | 88
```

Kalitli ko'p o'lchovli massiv esa "bo'limlar ichida elementlar" tuzilmasini yaxshi ifodalaydi:

```php
<?php
$dokon = [
    "mevalar"  => ["olma", "anor"],
    "sabzavot" => ["sabzi", "kartoshka", "piyoz"],
];

foreach ($dokon as $bolim => $mahsulotlar) {
    echo strtoupper($bolim) . ":\n";
    foreach ($mahsulotlar as $m) {
        echo "  - $m\n";
    }
}
// MEVALAR:
//   - olma
//   - anor
// SABZAVOT:
//   - sabzi
//   - kartoshka
//   - piyoz
```

> Ko'p o'lchovli massiv real dasturlarda hamma joyda: bazadan kelgan qatorlar, JSON ma'lumotlari, sozlamalar fayllari — barchasi shunday tuzilgan. "Tashqi `foreach` — qatorlar, ichki `foreach` — ustunlar" naqshini yaxshi o'zlashtiring.

### Mashqlar

**Oson**
1. 5 ta shahar nomidan massiv yarating va birinchi hamda oxirgisini chiqaring.
2. Massivga `[]` bilan yangi element qo'shing.
3. `count` bilan massivdagi elementlar sonini chiqaring.
4. `foreach` bilan massivdagi barcha elementlarni chiqaring.
5. Kalitli massiv yarating (kitob haqida: nomi, muallifi, yili) va har birini nom orqali chiqaring.
6. `range(1, 10)` bilan massiv yarating va `array_sum` orqali yig'indisini chiqaring.
7. `["olma", "anor"]` massiviga `array_push` bilan ikkita meva qo'shing, keyin `array_shift` bilan birinchisini olib tashlang va chiqaring.
8. `array_search` bilan `["a", "b", "c"]` massivida `"c"` qaysi indeksda turganini toping.
9. Ikki massivni — `["a", "b"]` va `["c", "d"]` ni — `...` (spread) bilan birlashtirib chiqaring.
10. `array_reverse` bilan `[1, 2, 3, 4]` massivini teskari tartibda chiqaring.

**O'rta**
11. Sonlardan iborat massiv (`[10, 20, 30, 40]`) yarating va `foreach` bilan ularning yig'indisini hisoblang.
12. Mahsulotlar massivini `foreach` bilan chiqaring, har birining oldiga raqam qo'ying (1. olma, 2. anor...). Maslahat: sikl tashqarisida hisoblagich yarating.
13. Kalitli massiv (talaba ma'lumoti) ni `foreach` bilan kalit-qiymat ko'rinishida chiqaring.
14. Massivdagi eng katta sonni toping (`foreach` bilan har bir elementni joriy eng katta bilan solishtiring).
15. Ikki massivni — `$mahsulotlar = ["olma", "anor", "uzum"]` va `$narxlar = [12000, 25000, 18000]` ni — `array_combine` bilan kalitli massivga aylantiring va `foreach` bilan `nom — narx` ko'rinishida chiqaring.
16. `$harflar = ["a", "b", "c", "d", "e"]` massividan `array_slice` bilan o'rtadagi 3 tasini (`b, c, d`) ajratib oling.
17. Ikki ro'yxat — `["olma", "anor", "uzum", "behi"]` va `["anor", "behi"]` ni — `array_diff` bilan solishtiring va birinchisida bor, ikkinchisida yo'qlarini chiqaring.
18. `[1, 2, 2, 3, 3, 3]` massividan `array_unique` bilan takrorlanmas qiymatlarni oling va `array_values` bilan indekslarni tartiblang.

**Qiyin**
19. Talabalar ro'yxati — bu yerda massiv **ichida** kalitli massivlar bo'ladi: har bir talaba alohida kalitli massiv (ism, ball). Hammasini `foreach` bilan chiqaring (`Ali - 85 ball` ko'rinishida).
20. Sonlar massividagi qiymatlarning o'rtachasini hisoblang (yig'indini elementlar soniga bo'ling).
21. Bir massivdagi sonlardan faqat juftlarini yangi massivga yig'ing va chiqaring.
22. `[12, 45, 23, 8, 67]` massivida: `array_sum`, `max`, `min` bilan yig'indi, eng katta va eng kichikni chiqaring; `in_array` bilan `67` borligini tekshiring.
23. `$narxlar = [300, 100, 500, 200]` ni `sort` bilan o'sish, `rsort` bilan kamayish tartibida chiqaring (har birini `implode` bilan).
24. Kitoblar ro'yxatini (har biri `["nom" => ..., "narx" => ...]`) `usort` bilan narx bo'yicha arzondan qimmatga saralang va chiqaring.
25. Talabalar massividan (`["ism" => ..., "ball" => ...]`) `array_column` bilan faqat ballarni ajratib oling, eng yuqori (`max`) va o'rtacha ballni chiqaring.
26. `foreach`da destructuring (`[$a, $b]`) ishlatib, `[[1, "bir"], [2, "ikki"], [3, "uch"]]` massivini `1 = bir` ko'rinishida chiqaring.
27. `range(1, 12)` bilan massiv yasab, `array_chunk` bilan 4 tadan bo'lakka bo'ling va har bir bo'lakni alohida qatorga chiqaring (sahifalash).

<details markdown="1">
<summary>Yechim — 11</summary>

```php
<?php
$sonlar = [10, 20, 30, 40];
$yigindi = 0;

foreach ($sonlar as $son) {
    $yigindi += $son;   // har bir sonni yig'indiga qo'shamiz
}

echo "Yig'indi: " . $yigindi;   // 100
```
</details>

<details markdown="1">
<summary>Yechim — 14 (eng katta son)</summary>

```php
<?php
$sonlar = [12, 45, 23, 8, 67, 34];
$eng_katta = $sonlar[0];   // birinchisini "hozircha eng katta" deb olamiz

foreach ($sonlar as $son) {
    if ($son > $eng_katta) {
        $eng_katta = $son;   // kattaroq topilsa, yangilaymiz
    }
}

echo "Eng katta: " . $eng_katta;   // 67
```
Mantiq: birinchi elementni boshlang'ich "g'olib" deb olamiz, keyin har birini u bilan solishtiramiz; kattarog'i chiqsa — uni yangi g'olib qilamiz.
</details>

<details markdown="1">
<summary>Yechim — 19 (massiv ichida massiv)</summary>

```php
<?php
$talabalar = [
    ["ism" => "Ali", "ball" => 85],
    ["ism" => "Vali", "ball" => 72],
    ["ism" => "Guli", "ball" => 95],
];

foreach ($talabalar as $talaba) {
    echo $talaba["ism"] . " - " . $talaba["ball"] . " ball<br>";
}
// Ali - 85 ball
// Vali - 72 ball
// Guli - 95 ball
```
Bu yerda `$talabalar` — massiv, uning har bir elementi yana kalitli massiv. `foreach` har bir talabani oladi, keyin uning ichidagi `["ism"]` va `["ball"]` ga murojaat qilamiz. Bunday "massiv ichida massiv" tuzilmasi real dasturlarda juda ko'p uchraydi (masalan, bazadan kelgan ma'lumotlar shunday ko'rinadi).
</details>

<details markdown="1">
<summary>Yechim — 20 (o'rtacha qiymat)</summary>

```php
<?php
$sonlar = [10, 25, 30, 45];

$yigindi = 0;
foreach ($sonlar as $son) {
    $yigindi += $son;
}

$ortacha = $yigindi / count($sonlar);   // yig'indini elementlar soniga bo'lamiz
echo "O'rtacha: " . $ortacha;            // 27.5
```
O'rtacha = yig'indi ÷ elementlar soni. `count($sonlar)` elementlar sonini beradi. (Buni `array_sum($sonlar) / count($sonlar)` bilan bir qatorda ham yozish mumkin — 1.8'dagi tayyor funksiyalarni eslang.)
</details>

<details markdown="1">
<summary>Yechim — 21 (juft sonlarni yangi massivga yig'ish)</summary>

```php
<?php
$hammasi = [1, 2, 3, 4, 5, 6, 7, 8];
$juftlar = [];                    // bo'sh massiv

foreach ($hammasi as $son) {
    if ($son % 2 === 0) {
        $juftlar[] = $son;        // juft bo'lsa, yangi massivga qo'sh
    }
}

echo implode(", ", $juftlar);     // 2, 4, 6, 8
```
Bo'sh massivdan boshlaymiz, `foreach` bilan har bir sonni tekshiramiz, juft bo'lsa `$juftlar[]` bilan oxiriga qo'shamiz. (1.10'da buni `array_filter` bilan bitta qatorda qilishni ko'rasiz.)
</details>

<details markdown="1">
<summary>Yechim — 22 (tayyor funksiyalar bilan)</summary>

```php
<?php
$sonlar = [12, 45, 23, 8, 67];

echo "Yig'indi: " . array_sum($sonlar) . "<br>";   // 155
echo "Eng katta: " . max($sonlar) . "<br>";        // 67
echo "Eng kichik: " . min($sonlar) . "<br>";       // 8
var_dump(in_array(67, $sonlar));                    // true
```
9-mashqda eng katta sonni `foreach` bilan qo'lda topgandik. Bu yerda esa `max()` bir so'zda qiladi — tayyor funksiyalar shu uchun foydali.
</details>

<details markdown="1">
<summary>Yechim — 23 (sort / rsort)</summary>

```php
<?php
$narxlar = [300, 100, 500, 200];

sort($narxlar);                      // o'sish tartibida
echo implode(", ", $narxlar);        // 100, 200, 300, 500

echo "<br>";

rsort($narxlar);                     // kamayish tartibida
echo implode(", ", $narxlar);        // 500, 300, 200, 100
```
Diqqat: `sort`/`rsort` massivning **o'zini** o'zgartiradi — natijani alohida o'zgaruvchiga olish shart emas, `$narxlar`ning o'zi saralangan bo'ladi.
</details>

<details markdown="1">
<summary>Yechim — 15 (array_combine)</summary>

```php
<?php
$mahsulotlar = ["olma", "anor", "uzum"];
$narxlar     = [12000, 25000, 18000];

$narxnoma = array_combine($mahsulotlar, $narxlar);

foreach ($narxnoma as $nom => $narx) {
    echo "$nom — $narx so'm<br>";
}
echo "Jami: " . array_sum($narxnoma) . " so'm";
// olma — 12000 so'm
// anor — 25000 so'm
// uzum — 18000 so'm
// Jami: 55000 so'm
```
`array_combine` birinchi massivni kalit, ikkinchisini qiymat qiladi — ikki alohida ro'yxatni bitta kalitli massivga aylantirishning eng tez yo'li. Keyin `array_sum` to'g'ridan-to'g'ri kalitli massivning qiymatlarini qo'shadi.
</details>

<details markdown="1">
<summary>Yechim — 17 (array_diff)</summary>

```php
<?php
$buyurtma = ["olma", "anor", "uzum", "behi"];
$omborda  = ["anor", "behi"];

$yoq = array_diff($buyurtma, $omborda);   // omborda yo'qlari
echo "Yetishmaydi: " . implode(", ", $yoq);   // Yetishmaydi: olma, uzum
```
`array_diff` birinchi massivda bor, lekin ikkinchisida yo'q elementlarni qaytaradi. "Omborda nimalar yetishmayapti?" kabi savolga bir qatorda javob beradi.
</details>

<details markdown="1">
<summary>Yechim — 24 (usort — narx bo'yicha)</summary>

```php
<?php
$kitoblar = [
    ["nom" => "PHP", "narx" => 75000],
    ["nom" => "SQL", "narx" => 60000],
    ["nom" => "JS",  "narx" => 90000],
];

usort($kitoblar, fn($a, $b) => $a["narx"] - $b["narx"]);   // arzondan qimmatga

foreach ($kitoblar as $k) {
    echo $k["nom"] . " — " . $k["narx"] . " so'm<br>";
}
// SQL — 60000 so'm
// PHP — 75000 so'm
// JS — 90000 so'm
```
`usort`ga o'z solishtirish qoidamizni beramiz: `$a["narx"] - $b["narx"]` — manfiy chiqsa `$a` oldinga (arzon oldinga). Kamayish kerak bo'lsa `$b["narx"] - $a["narx"]` deb yozamiz. `fn(...)` — funksiyaning zamonaviy, qisqa ko'rsatkichli shakli.
</details>

<details markdown="1">
<summary>Yechim — 25 (array_column)</summary>

```php
<?php
$talabalar = [
    ["ism" => "Ali",  "ball" => 85],
    ["ism" => "Vali", "ball" => 72],
    ["ism" => "Guli", "ball" => 95],
];

$ballar = array_column($talabalar, "ball");   // [85, 72, 95]

echo "Eng yuqori: " . max($ballar) . "<br>";                       // 95
echo "O'rtacha: " . (array_sum($ballar) / count($ballar));          // 84
```
`array_column` massiv ichidagi kalitli massivlardan bitta "ustun"ni (`ball`) ajratib oladi. Keyin oddiy `max` va `array_sum` bilan ishlaymiz. 19-mashqdagi `foreach` o'rniga buni bir qatorda qiladi.
</details>

<details markdown="1">
<summary>Yechim — 26 (foreach + destructuring)</summary>

```php
<?php
$sonlar = [[1, "bir"], [2, "ikki"], [3, "uch"]];

foreach ($sonlar as [$raqam, $soz]) {
    echo "$raqam = $soz<br>";
}
// 1 = bir
// 2 = ikki
// 3 = uch
```
`foreach ($sonlar as [$raqam, $soz])` — har bir ichki massivni darhol ikki nomli o'zgaruvchiga yoyadi. `$qator[0]`, `$qator[1]` deb yozishdan ko'ra ancha o'qish oson.
</details>

<details markdown="1">
<summary>Yechim — 27 (array_chunk — sahifalash)</summary>

```php
<?php
$royxat = range(1, 12);                  // [1, 2, ..., 12]
$sahifalar = array_chunk($royxat, 4);    // har biri 4 tadan

foreach ($sahifalar as $nomer => $sahifa) {
    echo ($nomer + 1) . "-sahifa: " . implode(", ", $sahifa) . "<br>";
}
// 1-sahifa: 1, 2, 3, 4
// 2-sahifa: 5, 6, 7, 8
// 3-sahifa: 9, 10, 11, 12
```
`range(1, 12)` tayyor massiv yasaydi, `array_chunk(..., 4)` uni 4 tadan bo'laklarga bo'ladi. `$nomer` 0 dan boshlanadi, shuning uchun sahifa raqami uchun `+1` qo'shamiz. Bu — sahifalashning (pagination) eng oddiy ko'rinishi.
</details>
