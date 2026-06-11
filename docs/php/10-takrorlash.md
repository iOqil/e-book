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

### Siklni to'xtatish va o'tkazib yuborish

- **`break`** — siklni butunlay to'xtatadi (undan chiqib ketadi).
- **`continue`** — joriy takrorni o'tkazib yuboradi, keyingisiga o'tadi.

```php
<?php
// break: 5 ga yetganda to'xta
for ($i = 1; $i <= 10; $i++) {
    if ($i == 5) {
        break;        // 5 da sikl tugaydi
    }
    echo $i . " ";    // 1 2 3 4
}

echo "<br>";

// continue: juft sonlarni o'tkazib yubor (faqat toq sonlar chiqsin)
for ($i = 1; $i <= 10; $i++) {
    if ($i % 2 == 0) {
        continue;     // juft bo'lsa, qolganini o'tkazib yubor
    }
    echo $i . " ";    // 1 3 5 7 9
}
```

### Mashqlar

**Oson**
1. `for` sikli bilan 1 dan 10 gacha sonlarni chiqaring.
2. `while` sikli bilan 1 dan 5 gacha sonlarni chiqaring.
3. 1 dan 20 gacha **faqat juft** sonlarni chiqaring (`% 2 == 0` bilan).
4. 10 dan 1 gacha **teskari** sanang (`$i--` ishlatib).
5. "Salom" so'zini 5 marta chiqaring (sikl bilan).

**O'rta**
6. 1 dan 100 gacha sonlar yig'indisini hisoblang.
7. 5 ning ko'paytuv jadvalini chiqaring: `5 x 1 = 5`, `5 x 2 = 10`, ... `5 x 10 = 50`.
8. 1 dan 50 gacha 3 ga bo'linadigan sonlarni chiqaring.
9. `break` bilan: 1 dan boshlab sanang, lekin son 7 ga yetganda to'xtang.
10. `continue` bilan: 1 dan 20 gacha sonlardan faqat toqlarini chiqaring.

**Qiyin**
11. Berilgan sonning faktorialini hisoblang (faktorial: `5! = 1×2×3×4×5 = 120`). Maslahat: yig'indi o'rniga ko'paytma to'plang, boshlang'ich qiymat 1 bo'lsin.
12. Berilgan son tub (prime) sonmi, tekshiring. Tub son — faqat 1 ga va o'ziga bo'linadigan son (2, 3, 5, 7, 11...). Maslahat: sonni 2 dan boshlab o'zidan kichik sonlarga bo'lib ko'ring; agar birortasiga teng bo'linsa — tub emas.
13. To'liq ko'paytuv jadvali (1 dan 9 gacha) — bunda sikl **ichida sikl** kerak bo'ladi (tashqi sikl — qatorlar, ichki sikl — ustunlar).

<details markdown="1">
<summary>Yechim — 7 (ko'paytuv jadvali)</summary>

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
<summary>Yechim — 11 (faktorial)</summary>

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
<summary>Yechim — 12 (tub son tekshiruvi)</summary>

```php
<?php
$son = 7;
$tub = true;          // hozircha "tub" deb hisoblaymiz

if ($son < 2) {
    $tub = false;     // 0 va 1 tub emas
} else {
    // 2 dan boshlab, sonning kvadrat ildizigacha bo'lib ko'ramiz
    for ($i = 2; $i * $i <= $son; $i++) {
        if ($son % $i == 0) {
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
<summary>Yechim — 13 (ichma-ich sikl)</summary>

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
