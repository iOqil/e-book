# 1.7 Takrorlash (sikllar)

[⬅️ Oldingi: 1.6 Shartlar (if/else)](./09-shartlar.md) · [🏠 README](./README.md) · [Keyingi: 1.8 Ro'yxatlar (massivlar) ➡️](./11-royxatlar.md)

---

Tasavvur qiling, 1 dan 100 gacha sonlarni ekranga chiqarish kerak. Har birini alohida `echo` bilan yozsangiz — 100 ta qator! Bu juda noqulay. Kompyuterning eng kuchli tomoni — **bir ishni ko'p marta takrorlash**. Buni **sikllar** (loops) yordamida qilamiz: bir kod blokini kerakli marta qaytaramiz.

### `while` sikli — "shart bajarilguncha takrorla"

`while` so'zi "...gacha" degani. Shart rost bo'lib turguncha, kod takrorlanaveradi:

```php
<?php
$son = 1;

while ($son <= 5) {
    echo $son . "<br>";
    $son++;            // har takrorda sonni 1 ga oshiramiz
}
```

Bu kod 1, 2, 3, 4, 5 ni chiqaradi. Qanday ishlaydi:
1. `$son = 1` — boshlang'ich qiymat.
2. `while` shartni tekshiradi: `1 <= 5`? Ha → ichidagi kod ishlaydi (1 chiqadi), keyin `$son` 2 bo'ladi.
3. Yana tekshiradi: `2 <= 5`? Ha → 2 chiqadi, `$son` 3 bo'ladi.
4. ...shu tarzda davom etadi, `$son` 6 bo'lganda: `6 <= 5`? Yo'q → sikl to'xtaydi.

> **JUDA MUHIM:** sikl ichida `$son++` (qiymatni o'zgartirish) bo'lishi shart. Agar uni unutsangiz, shart hech qachon yolg'on bo'lmaydi va sikl **abadiy** takrorlanadi (dastur "osilib qoladi"). Bu — boshlovchilarda ko'p uchraydigan xato. Agar dasturingiz qotib qolsa, brauzer oynasini yopib, shuni tekshiring.

### `do-while` sikli — "avval bajar, keyin tekshir"

`while`da shart **boshida** tekshiriladi: agar shart darrov yolg'on bo'lsa, sikl ichidagi kod **bironta ham marta** ishlamaydi. Ba'zan esa bizga "kamida bir marta bajar, keyin takrorlash kerakmi-yo'qmi deb qara" kerak bo'ladi. Ana shu uchun `do-while` bor: u avval kodni bajaradi, **keyin** shartni tekshiradi.

```php
<?php
$son = 1;

do {
    echo $son . "<br>";
    $son++;
} while ($son <= 5);
```

Bu ham 1, 2, 3, 4, 5 ni chiqaradi. E'tibor bering: shart oxirida, `}` dan keyin yoziladi va orqasiga `;` (nuqta-vergul) qo'yiladi — buni unutmang.

**`while` va `do-while` farqi — bir misolda ko'ring.** Shartni ataylab darrov yolg'on qilamiz (`$son` 10, lekin shart `<= 5`):

```php
<?php
// while: shart boshidan yolg'on - hech narsa chiqmaydi
$son = 10;
echo "while natijasi: ";
while ($son <= 5) {
    echo $son . " ";
    $son++;
}
echo "(bo'sh)<br>";

// do-while: kamida bir marta bajariladi
$son = 10;
echo "do-while natijasi: ";
do {
    echo $son . " ";
    $son++;
} while ($son <= 5);
echo "(10 chiqdi)";
```

Natija:
```
while natijasi: (bo'sh)
do-while natijasi: 10 (10 chiqdi)
```

`while` boshidayoq `10 <= 5`? Yo'q → ichiga kirmadi ham. `do-while` esa avval ichiga kirib `10` ni chiqardi, **keyin** `11 <= 5`? Yo'q → to'xtadi. Mana shu — asosiy farq: `do-while` **doim kamida bir marta** ishlaydi.

> **Qachon `do-while` kerak?** Ko'pincha foydalanuvchidan biror narsa so'rayotganda. Masalan, "menyudan 1–5 oralig'ida raqam tanlang" deganda — avval bir marta so'rashimiz shart, keyin "noto'g'ri kiritibdi, yana so'rayman" deb takrorlaymiz. Quyidagi misolda foydalanuvchi kiritmalarini massiv bilan taqlid qilamiz (real loyihada `readline()` bo'lardi):

```php
<?php
// Foydalanuvchidan to'g'ri qiymat kelguncha so'rashni simulyatsiya qilamiz.
$kiritmalar = [0, 9, 3];   // 0 va 9 noto'g'ri, 3 to'g'ri
$indeks = 0;

do {
    $tanlov = $kiritmalar[$indeks];
    $indeks++;
    echo "Kiritildi: {$tanlov}<br>";
} while ($tanlov < 1 || $tanlov > 5);

echo "Qabul qilindi: {$tanlov}";
```

Natija:
```
Kiritildi: 0
Kiritildi: 9
Kiritildi: 3
Qabul qilindi: 3
```

Avval 0 so'raldi (noto'g'ri), keyin 9 (noto'g'ri), keyin 3 (to'g'ri → sikl to'xtadi). `do-while` aynan shunday "kamida bir marta so'rash" mantiqi uchun yaratilgan.

### `for` sikli — "ma'lum marta takrorla"

`for` — sanab takrorlash uchun eng qulay sikl. U `while`ning ixchamroq ko'rinishi: boshlang'ich qiymat, shart va o'zgartirish — hammasi bir qatorda:

```php
<?php
for ($i = 1; $i <= 5; $i++) {
    echo $i . "<br>";
}
```

Bu ham 1 dan 5 gacha chiqaradi. Qavs ichida uch qism, `;` bilan ajratilgan:
1. **`$i = 1`** — boshlang'ich qiymat (sikl boshida bir marta bajariladi).
2. **`$i <= 5`** — shart (har takror oldidan tekshiriladi).
3. **`$i++`** — o'zgartirish (har takror oxirida bajariladi).

> `$i` — bu "hisoblagich" (counter). An'anaga ko'ra ko'pincha `$i` deb nomlanadi (`index` so'zidan). 0 yoki 1 dan boshlanishi vazifaga bog'liq.

`for` sikli "aniq necha marta takrorlanishini bilganda" qulay (masalan, 1 dan 100 gacha). `while` esa "qachongacha ekani noaniq bo'lganda" qulay.

### Misol: 1 dan 10 gacha sonlar yig'indisi

```php
<?php
$yigindi = 0;

for ($i = 1; $i <= 10; $i++) {
    $yigindi += $i;   // har takrorda joriy sonni yig'indiga qo'shamiz
}

echo "Yig'indi: " . $yigindi;   // 55
```

Sikl `$yigindi`ga 1, keyin 2, keyin 3... qo'shib boradi. Oxirida 1+2+...+10 = 55.

### Sikl ichida massiv yig'ish naqshlari

Sikllar ko'pincha **natijani bitta o'zgaruvchiga yig'ish** uchun ishlatiladi (yuqorida yig'indini bir songa yig'dik). Ammo ko'pincha natijani **massivga** yig'ish kerak bo'ladi: har takrorda bittadan element qo'shib boramiz. Buning bir nechta keng tarqalgan naqshi bor.

**Naqsh 1 — bo'sh massivdan boshlab, `[]` bilan qo'shish.** Bo'sh massivdan (`[]`) boshlaymiz, keyin `$massiv[] = ...` bilan oxiriga element qo'shamiz:

```php
<?php
$kvadratlar = [];
for ($i = 1; $i <= 5; $i++) {
    $kvadratlar[] = $i * $i;   // massiv oxiriga qo'shadi
}
print_r($kvadratlar);          // [1, 4, 9, 16, 25]
```

`$kvadratlar[]` — kvadrat qavs ichi bo'sh — "massivning eng oxiriga yangi element qo'sh" degani. Har takrorda massiv bittaga uzayadi.

**Naqsh 2 — mavjud massivni filtrlab, yangisini yig'ish.** Bir massivni aylanib chiqib, faqat kerakli elementlarni yangi massivga to'playmiz:

```php
<?php
$sonlar = [4, 7, 10, 13, 16, 21];
$juftlar = [];
foreach ($sonlar as $son) {
    if ($son % 2 === 0) {
        $juftlar[] = $son;     // faqat juft bo'lsa qo'shamiz
    }
}
print_r($juftlar);             // [4, 10, 16]
```

Bu — juda ko'p uchraydigan naqsh: "katta ro'yxatdan shartga mos elementlarni ajratib olish".

**Naqsh 3 — kalit => qiymat juftlarini yig'ish.** Massivga oddiy elementlar emas, balki kalit-qiymat juftlarini qo'yamiz. Bu yerda ikki ro'yxatni bittaga bog'laymiz:

```php
<?php
$narxlar = [];
$mahsulotlar = ['Olma', 'Banan', 'Uzum'];
$qiymatlar = [3000, 5000, 12000];

for ($i = 0; $i < count($mahsulotlar); $i++) {
    $narxlar[$mahsulotlar[$i]] = $qiymatlar[$i];
}
print_r($narxlar);             // ['Olma' => 3000, 'Banan' => 5000, 'Uzum' => 12000]
```

Endi `$narxlar['Olma']` → `3000`. `count()` — massivdagi elementlar sonini qaytaradi, shuning uchun `$i < count(...)` "massiv oxirigacha yur" degani. (Massivlar haqida keyingi bobda batafsil o'rganamiz — hozir shuncha bilish yetarli.)

### Siklni to'xtatish va o'tkazib yuborish

- **`break`** — siklni butunlay to'xtatadi (undan chiqib ketadi).
- **`continue`** — joriy takrorni o'tkazib yuboradi, keyingisiga o'tadi.

```php
<?php
// break: 5 ga yetganda to'xta
for ($i = 1; $i <= 10; $i++) {
    if ($i === 5) {
        break;        // 5 da sikl tugaydi
    }
    echo $i . " ";    // 1 2 3 4
}

echo "<br>";

// continue: juft sonlarni o'tkazib yubor (faqat toq sonlar chiqsin)
for ($i = 1; $i <= 10; $i++) {
    if ($i % 2 === 0) {
        continue;     // juft bo'lsa, qolganini o'tkazib yubor
    }
    echo $i . " ";    // 1 3 5 7 9
}
```

> **Eslatma:** bu yerda `$i === 5` va `$i % 2 === 0` da uch belgi `===` ishlatildi (oddiy `==` emas). `===` — "aynan teng" (ham qiymat, ham tur bir xil) degani; sonlar bilan ishlaganda har doim `===` ishlatish odat bo'lsin — bu kelajakdagi noxush xatolardan saqlaydi.

### `break N` va `continue N` — bir necha darajaga chiqish

Oddiy `break` faqat **eng ichki** sikldan chiqadi. Ammo sikl ichida sikl bo'lganda (ichma-ich), ba'zan bitta `break` bilan **bir nechta darajadan birdan** chiqib ketish kerak bo'ladi. Shu uchun PHPda `break` va `continue` orqasiga raqam yozish mumkin: `break 2` — ikki darajadan chiq, `continue 2` — ikki darajaga ta'sir qil.

**`break 2` — ichki va tashqi sikldan birdan chiqish.** Quyida ko'paytma 6 dan oshganda ikkala sikldan ham chiqamiz:

```php
<?php
for ($qator = 1; $qator <= 5; $qator++) {
    for ($ustun = 1; $ustun <= 5; $ustun++) {
        if ($qator * $ustun > 6) {
            echo "To'xtadi: {$qator} x {$ustun}<br>";
            break 2;          // ham ichki, ham tashqi siklni tugatadi
        }
        echo ($qator * $ustun) . " ";
    }
}
echo "Sikllardan butunlay chiqdik";
```

Natija:
```
1 2 3 4 5 2 4 6 To'xtadi: 2 x 4
Sikllardan butunlay chiqdik
```

Agar oddiy `break` (yoki `break 1`) yozganimizda, faqat ichki sikl tugardi va tashqi sikl `$qator = 3, 4, 5` bilan davom etardi. `break 2` esa **ikkalasini ham** to'xtatdi — natijada darrov "Sikllardan butunlay chiqdik" ga o'tdik. Bu, masalan, jadvaldan biror qiymatni qidirib topganda — "topdim, boshqa qidirish shart emas" degan holatda juda qulay.

**`continue 2` — tashqi siklning keyingi takroriga sakrash.** Bu esa ichki siklni tugatib, tashqi siklning **keyingi** aylanishiga o'tkazadi:

```php
<?php
for ($qator = 1; $qator <= 3; $qator++) {
    for ($ustun = 1; $ustun <= 3; $ustun++) {
        if ($ustun === 2) {
            continue 2;       // tashqi siklning keyingi takroriga o't
        }
        echo "{$qator}-{$ustun} ";
    }
    echo "(bu yozuv hech qachon chiqmaydi) ";
}
```

Natija:
```
1-1 2-1 3-1
```

Har bir qatorda `$ustun = 1` chiqadi, keyin `$ustun = 2` bo'lganda `continue 2` ishga tushadi — bu nafaqat ichki siklni tugatadi, balki **tashqi siklning oxiridagi `echo`ni ham o'tkazib yuboradi** va to'g'ridan-to'g'ri keyingi qatorga sakraydi. Shuning uchun "bu yozuv hech qachon chiqmaydi" haqiqatan ham chiqmaydi.

> **Maslahat:** `break 2` / `continue 2` qulay, lekin haddan tashqari chuqur (`break 3`, `break 4`...) ishlatish kodni o'qishni qiyinlashtiradi. Odatda 2 daraja yetarli; undan chuqurroq kerak bo'lsa, kodni alohida funksiyaga ajratib, `return` bilan chiqish toza yechim bo'ladi.

### Alternativ sintaksis — HTML shablon ichida qulay

Hozirgacha sikllarni `{ }` (figurali qavs) bilan yozdik. PHPda yana bir yozilishi bor: `{` o'rniga `:` (ikki nuqta), `}` o'rniga esa `endfor;`, `endforeach;`, `endwhile;`, `endif;` yoziladi. Bu — **alternativ sintaksis**.

Nima farqi bor? Mantiqan hech qanaqa — natija aynan bir xil. Lekin **HTML orasida PHP yozganda** alternativ sintaksis ancha o'qishli bo'ladi: chunki ko'p `}` qavslar HTML teglar bilan aralashib ketganda, qaysi `}` qaysi siklga tegishli ekanini topish qiyin. `endforeach;` esa darrov ko'rinadi.

Solishtiring. **Figurali qavs bilan** (HTML ichida chalkash):

```php
<ul>
    <?php foreach (['Olma', 'Banan', 'Uzum'] as $meva) { ?>
        <li><?= $meva ?></li>
    <?php } ?>
</ul>
```

**Alternativ sintaksis bilan** (ancha aniq):

```php
<?php $mahsulotlar = ['Olma', 'Banan', 'Uzum']; ?>
<ul>
    <?php foreach ($mahsulotlar as $mahsulot): ?>
        <li><?= $mahsulot ?></li>
    <?php endforeach; ?>
</ul>
```

Natija (HTML):
```html
<ul>
    <li>Olma</li>
    <li>Banan</li>
    <li>Uzum</li>
</ul>
```

E'tibor bering: `<?= $mahsulot ?>` — bu `<?php echo $mahsulot; ?>` ning qisqa shakli (HTML ichida qiymat chiqarish uchun juda qulay).

Xuddi shu uslub `for`, `while`, `if` uchun ham ishlaydi:

```php
<table>
    <?php for ($i = 1; $i <= 3; $i++): ?>
        <tr><td>Qator <?= $i ?></td></tr>
    <?php endfor; ?>
</table>

<?php $soat = 14; ?>
<?php if ($soat < 12): ?>
    <p>Xayrli tong!</p>
<?php else: ?>
    <p>Xayrli kun!</p>
<?php endif; ?>
```

Natija:
```html
<table>
    <tr><td>Qator 1</td></tr>
    <tr><td>Qator 2</td></tr>
    <tr><td>Qator 3</td></tr>
</table>

    <p>Xayrli kun!</p>
```

> **Qoida:** sof PHP fayllarda (HTML aralashmagan) odatda figurali qavs `{ }` ishlatiladi. HTML shablonlarda esa alternativ sintaksis (`:` ... `endforeach;`) o'qishni osonlashtiradi. Ikkalasi ham to'g'ri — vaziyatga qarab tanlang.

### Mashqlar

**Oson**
1. `for` sikli bilan 1 dan 10 gacha sonlarni chiqaring.
2. `while` sikli bilan 1 dan 5 gacha sonlarni chiqaring.
3. 1 dan 20 gacha **faqat juft** sonlarni chiqaring (`% 2 === 0` bilan).
4. 10 dan 1 gacha **teskari** sanang (`$i--` ishlatib).
5. "Salom" so'zini 5 marta chiqaring (sikl bilan).
6. `do-while` bilan 1 dan 5 gacha sonlarni chiqaring (`while` o'rniga `do-while`).

**O'rta**
7. 1 dan 100 gacha sonlar yig'indisini hisoblang.
8. 5 ning ko'paytuv jadvalini chiqaring: `5 x 1 = 5`, `5 x 2 = 10`, ... `5 x 10 = 50`.
9. 1 dan 50 gacha 3 ga bo'linadigan sonlarni chiqaring.
10. `break` bilan: 1 dan boshlab sanang, lekin son 7 ga yetganda to'xtang.
11. `continue` bilan: 1 dan 20 gacha sonlardan faqat toqlarini chiqaring.
12. Sikl ichida massiv yig'ish: 1 dan 10 gacha sonlarning kvadratlarini `$kvadratlar` massiviga to'plang va `print_r` bilan chiqaring.
13. `[12, 7, 30, 5, 18, 9]` massivdan faqat 10 dan kattalarini yangi massivga ajratib oling.

**Qiyin**
14. Berilgan sonning faktorialini hisoblang (faktorial: `5! = 1×2×3×4×5 = 120`). Maslahat: yig'indi o'rniga ko'paytma to'plang, boshlang'ich qiymat 1 bo'lsin.
15. Berilgan son tub (prime) sonmi, tekshiring. Tub son — faqat 1 ga va o'ziga bo'linadigan son (2, 3, 5, 7, 11...). Maslahat: sonni 2 dan boshlab o'zidan kichik sonlarga bo'lib ko'ring; agar birortasiga teng bo'linsa — tub emas.
16. To'liq ko'paytuv jadvali (1 dan 9 gacha) — bunda sikl **ichida sikl** kerak bo'ladi (tashqi sikl — qatorlar, ichki sikl — ustunlar).
17. `break 2` bilan: 3×3 jadvalda (ikki o'lchovli massiv) berilgan qiymatni qidiring; topilgan zahoti ikkala sikldan ham chiqing va o'rnini (qator-ustun) chiqaring.
18. `do-while` bilan oddiy parol tekshiruvi: to'g'ri parol kelguncha (yoki urinishlar tugaguncha) "so'rashni" davom ettiring. Kiritmalarni massiv bilan taqlid qiling.
19. Alternativ sintaksisdan foydalanib, vazifalar ro'yxatini (`['Kod yozish', 'Test qilish', 'Deploy']`) HTML `<ol>` ichida raqamlangan ro'yxat sifatida chiqaring.

<details markdown="1">
<summary>Yechim — 6 (do-while)</summary>

```php
<?php
$son = 1;

do {
    echo $son . "<br>";
    $son++;
} while ($son <= 5);
```
Natijasi `while` bilan bir xil (1, 2, 3, 4, 5). Farqi shundaki — bu yerda kod avval bajarilib, keyin shart tekshiriladi. Shart oxirida `;` bilan tugashini unutmang.
</details>

<details markdown="1">
<summary>Yechim — 8 (ko'paytuv jadvali)</summary>

```php
<?php
$son = 5;

for ($i = 1; $i <= 10; $i++) {
    echo $son . " x " . $i . " = " . ($son * $i) . "<br>";
}
```
Chiqadi: `5 x 1 = 5`, `5 x 2 = 10`, ... `5 x 10 = 50`.
Diqqat: `($son * $i)` qavs ichida — chunki avval ko'paytirib, keyin matnga ulashimiz kerak.
</details>

<details markdown="1">
<summary>Yechim — 12 (kvadratlarni massivga yig'ish)</summary>

```php
<?php
$kvadratlar = [];
for ($i = 1; $i <= 10; $i++) {
    $kvadratlar[] = $i * $i;   // massiv oxiriga qo'shamiz
}
print_r($kvadratlar);          // [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```
Bo'sh massivdan (`[]`) boshlaymiz, har takrorda `$kvadratlar[]` orqali oxiriga bitta element qo'shamiz.
</details>

<details markdown="1">
<summary>Yechim — 13 (filtrlab yig'ish)</summary>

```php
<?php
$sonlar = [12, 7, 30, 5, 18, 9];
$kattalar = [];
foreach ($sonlar as $son) {
    if ($son > 10) {
        $kattalar[] = $son;    // faqat 10 dan katta bo'lsa qo'shamiz
    }
}
print_r($kattalar);            // [12, 30, 18]
```
Bu — eng ko'p uchraydigan naqshlardan biri: massivni aylanib, shartga mos elementlarni yangi massivga ajratib olish.
</details>

<details markdown="1">
<summary>Yechim — 14 (faktorial)</summary>

```php
<?php
$son = 5;
$faktorial = 1;        // ko'paytma uchun boshlang'ich 1 (0 emas!)

for ($i = 1; $i <= $son; $i++) {
    $faktorial *= $i;  // 1*1, keyin *2, *3, *4, *5
}

echo $son . "! = " . $faktorial;   // 5! = 120
```
Nega boshlang'ich 1? Chunki ko'paytmada 0 dan boshlasak, hamma narsa 0 bo'lib qoladi. Yig'indida 0 dan, ko'paytmada 1 dan boshlanadi.
</details>

<details markdown="1">
<summary>Yechim — 15 (tub son tekshiruvi)</summary>

```php
<?php
$son = 7;
$tub = true;          // hozircha "tub" deb hisoblaymiz

if ($son < 2) {
    $tub = false;     // 0 va 1 tub emas
} else {
    // 2 dan boshlab, sonning kvadrat ildizigacha bo'lib ko'ramiz
    for ($i = 2; $i * $i <= $son; $i++) {
        if ($son % $i === 0) {
            $tub = false;   // biror songa bo'lindi → tub emas
            break;          // davom etish shart emas
        }
    }
}

echo $son . ($tub ? " — tub son" : " — tub son emas");
```
Mantiq: agar son 2 dan kichik bo'lsa — tub emas. Aks holda 2 dan boshlab `$i * $i <= $son` gacha bo'lib ko'ramiz; birortasiga butun bo'linsa — tub emas, `break` bilan to'xtaymiz. Nega `$i * $i <= $son` (ya'ni $i ildizgacha)? Chunki sonning bo'luvchilari ildizidan keyin takrorlanadi — bu hisobni tezlashtiradi.
</details>

<details markdown="1">
<summary>Yechim — 16 (ichma-ich sikl)</summary>

```php
<?php
for ($qator = 1; $qator <= 9; $qator++) {      // tashqi sikl
    for ($ustun = 1; $ustun <= 9; $ustun++) {  // ichki sikl
        echo ($qator * $ustun) . "\t";          // \t — bo'sh joy (tab)
    }
    echo "<br>";   // har qatordan keyin yangi qatorga o't
}
```
Tashqi sikl har bir qator uchun bir marta, ichki sikl esa har qatorda 9 marta ishlaydi. Natijada 9×9 jadval hosil bo'ladi.
</details>

<details markdown="1">
<summary>Yechim — 17 (break 2 bilan jadvalda qidirish)</summary>

```php
<?php
$jadval = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
];
$qidirilayotgan = 5;
$topildi = false;

for ($q = 0; $q < count($jadval); $q++) {
    for ($u = 0; $u < count($jadval[$q]); $u++) {
        if ($jadval[$q][$u] === $qidirilayotgan) {
            echo "Topildi: [{$q}][{$u}]<br>";
            $topildi = true;
            break 2;          // ikkala sikldan ham chiqamiz
        }
    }
}

echo $topildi ? "Qidiruv tugadi" : "Topilmadi";
```
`break 2` — qiymat topilgach, ichki va tashqi siklni birdan to'xtatadi: chunki topilgandan keyin qidirishni davom ettirish ortiqcha. 5 — `[1][1]` o'rnida (ikkinchi qatorning ikkinchi ustuni; sanoq 0 dan boshlanadi).
</details>

<details markdown="1">
<summary>Yechim — 18 (do-while bilan parol)</summary>

```php
<?php
$togriParol = "secret";
$urinishlar = ["123", "qwerty", "secret"];   // foydalanuvchi kiritmalari
$indeks = 0;
$kiritildi = "";

do {
    $kiritildi = $urinishlar[$indeks];
    $indeks++;
    echo "Urinish {$indeks}: {$kiritildi}<br>";
} while ($kiritildi !== $togriParol && $indeks < count($urinishlar));

echo ($kiritildi === $togriParol) ? "Kirildi!" : "Bloklandi!";
```
`do-while` tanlandi, chunki parolni **kamida bir marta** so'rashimiz shart. Shart ikki qismdan: parol noto'g'ri (`!==`) **va** urinishlar tugamagan bo'lsa — yana so'raymiz.
</details>

<details markdown="1">
<summary>Yechim — 19 (alternativ sintaksis bilan ro'yxat)</summary>

```php
<?php $vazifalar = ['Kod yozish', 'Test qilish', 'Deploy']; ?>
<ol>
    <?php foreach ($vazifalar as $vazifa): ?>
        <li><?= $vazifa ?></li>
    <?php endforeach; ?>
</ol>
```
HTML ichida `foreach (...): ... endforeach;` shakli figurali qavsga qaraganda o'qishli. `<?= $vazifa ?>` — `echo` ning qisqa yozilishi. Natija — raqamlangan ro'yxat (`<ol>`): 1. Kod yozish, 2. Test qilish, 3. Deploy.
</details>
