# 1.6 Shartlar (if/else)

[⬅️ Oldingi: 1.5 Matn bilan ishlash (string)](./08-matn-bilan-ishlash.md) · [🏠 README](./README.md) · [Keyingi: 1.7 Takrorlash (sikllar) ➡️](./10-takrorlash.md)

---

Hozirgacha dasturimiz har doim bir xil ishni bajarardi. Lekin haqiqiy dasturlar **qaror qabul qilishi** kerak: "agar foydalanuvchi katta bo'lsa — ruxsat ber, aks holda — berma", "agar narx yetarli bo'lsa — sotib ol". Ana shu "agar..." mantig'i — **shartlar** orqali yoziladi. Bu — dasturlashning eng muhim tushunchalaridan biri.

### Oddiy `if`

`if` so'zi "agar" degani. Qavs ichiga shart yoziladi; agar shart **rost** (`true`) bo'lsa, `{ }` ichidagi kod ishlaydi:

```php
<?php
$yosh = 20;

if ($yosh >= 18) {
    echo "Siz katta yoshdasiz";
}
```

Bu yerda: "agar yosh 18 dan katta yoki teng bo'lsa, xabarni chiqar". Yosh 20 bo'lgani uchun shart rost — xabar chiqadi.

Tuzilishini ko'ring:
- **`if`** — "agar".
- **`( )`** ichida — tekshiriladigan shart (1.4'da ko'rgan taqqoslash amallari shu yerda ishlatiladi).
- **`{ }`** ichida — shart rost bo'lsa bajariladigan kod.

### `if ... else` — "aks holda"

`else` so'zi "aks holda" degani: agar shart yolg'on bo'lsa, `else` ichidagi kod ishlaydi:

```php
<?php
$yosh = 15;

if ($yosh >= 18) {
    echo "Ruxsat berildi";
} else {
    echo "Ruxsat berilmadi";   // yosh 15, shart yolg'on → shu chiqadi
}
```

Faqat ikkitadan bittasi ishlaydi: yoki `if` ichidagi, yoki `else` ichidagi.

### `if ... elseif ... else` — bir nechta holat

Ko'pincha ikkitadan ko'p holat bo'ladi. `elseif` ("aks holda agar") qo'shimcha shartlarni tekshiradi:

```php
<?php
$ball = 75;

if ($ball >= 90) {
    echo "A baho";
} elseif ($ball >= 80) {
    echo "B baho";
} elseif ($ball >= 70) {
    echo "C baho";   // 75 bu yerga to'g'ri keladi
} else {
    echo "Yiqildi";
}
```

PHP shartlarni **yuqoridan pastga** tekshiradi va birinchi rost bo'lganida to'xtaydi. `$ball = 75` uchun: 90 dan katta emas, 80 dan katta emas, 70 dan katta — ha! "C baho" chiqadi va qolgani tekshirilmaydi.

Quyidagi blok-sxema shu oqimni ko'rsatadi: har shart navbat bilan tekshiriladi, birinchi rost tarmoq bajariladi.

![if / elseif / else qaror oqimi: shartlar yuqoridan pastga tekshiriladi](rasmlar/pha-if-elseif-else.svg)

### Mantiqiy amallar — bir nechta shartni birlashtirish

Ba'zan bir vaqtda bir nechta shart tekshirilishi kerak. Buning uchun:

- **`&&`** — "va" (ikkala shart ham rost bo'lishi kerak)
- **`||`** — "yoki" (kamida bittasi rost bo'lsa yetarli)
- **`!`** — "emas" (rostni yolg'onga, yolg'onni rostga aylantiradi)

```php
<?php
$yosh = 25;
$pul = 100000;

// "va" — ikkala shart ham rost bo'lishi kerak
if ($yosh >= 18 && $pul >= 50000) {
    echo "Sotib olishingiz mumkin";
}

// "yoki" — bittasi rost bo'lsa yetarli
$kun = "shanba";
if ($kun == "shanba" || $kun == "yakshanba") {
    echo "Bugun dam olish kuni";
}
```

`&&` ni "ham...ham" deb, `||` ni "yo...yo" deb o'qing.

### Misol: juft yoki toq sonni aniqlash

1.4'da o'rgangan `%` (qoldiq) amalini eslang. Agar son 2 ga bo'linganda qoldiq 0 bo'lsa — u juft son:

```php
<?php
$son = 7;

if ($son % 2 == 0) {
    echo "Juft son";
} else {
    echo "Toq son";   // 7 % 2 = 1, qoldiq 0 emas → toq
}
```

### `switch` — bitta qiymatni ko'p variant bilan solishtirish

Ba'zan bitta o'zgaruvchini ko'p qiymatlardan biriga teng-emasligini tekshiramiz. `if/elseif` bilan bu uzun chiqadi. `switch` shu holat uchun toza ko'rinish beradi:

```php
<?php
$kun = "seshanba";

switch ($kun) {
    case "shanba":
    case "yakshanba":
        echo "Dam olish kuni";
        break;                  // bu variant tugadi — chiqib ket
    default:
        echo "Ish kuni";        // hech qaysi case mos kelmasa
}
```

- **`switch ($kun)`** — qaysi o'zgaruvchini tekshirayotganimiz.
- **`case "shanba":`** — "agar `$kun` `"shanba"` ga teng bo'lsa". Ikki `case` ketma-ket yozilsa (yuqorida shanba/yakshanba) — ikkalasi uchun bir xil kod ishlaydi.
- **`break;`** — JUDA muhim: variant tugaganini bildiradi. Unutsangiz, PHP keyingi `case`ga ham "tushib" ketadi (fall-through) — ko'p uchraydigan xato.
- **`default:`** — hech qaysi variant mos kelmaganda (xuddi `else` kabi).

> **Qachon `switch`, qachon `if`?** Bitta qiymatni aniq variantlarga solishtirsangiz (`$kun` "shanba"mi, "yakshanba"mi...) — `switch` toza. Oraliq/murakkab shartlar bo'lsa (`yosh >= 18 && pul > 0`) — `if/elseif`.

### `match` — `switch`'ning zamonaviy, ixcham ko'rinishi (PHP 8+)

`match` — `switch`'ning yangi, qulayroq versiyasi. Farqi: u **qiymat qaytaradi**, `break` shart emas, va qat'iy (`===` — ham qiymat, ham tur) solishtiradi:

```php
<?php
$baho = 85;

$harf = match(true) {
    $baho >= 90 => "A",
    $baho >= 80 => "B",      // 85 shu yerga to'g'ri keladi
    $baho >= 70 => "C",
    default     => "F",
};

echo $harf;   // B
```

- Har bir variant `shart => natija` ko'rinishida, vergul bilan ajratiladi.
- Natija to'g'ridan-to'g'ri `$harf`ga saqlanadi — `echo` yoki `break` yozish shart emas.
- `match(true)` — "qaysi shart `true` bo'lsa" degani (oraliqlarni tekshirishda qulay). Aniq qiymatlarni solishtirsangiz, `match($kun)` deb yozasiz:

```php
<?php
$kun = "seshanba";
echo match($kun) {
    "shanba", "yakshanba" => "Dam olish kuni",
    default               => "Ish kuni",
};
```

> **Why:** `match` `if/elseif`ning eng toza ko'rinishi — "bir qiymatga qarab turli natija" kerak bo'lganda ishlating. Bir necha variantni bitta natijaga ulash uchun ularni vergul bilan sanang. (2.9 — Enum bo'limida `match`ni yana ko'ramiz.)

### Qisqa shartli yozuvlar: ternary (`?:`) va `??`

Kichik shartlarni bitta qatorda yozishning qisqa yo'llari bor.

**Ternary (`?:`)** — "agar... bo'lsa buni, aks holda buni":

```php
<?php
$yosh = 20;

// To'liq if/else o'rniga:
$holat = ($yosh >= 18) ? "katta" : "kichik";
echo $holat;   // katta
```

`shart ? rost_bo'lsa : yolg'on_bo'lsa` — bu kichik tanlovlar uchun qulay. Lekin uni murakkablashtirib yubormang (ichma-ich ternary o'qishni qiyinlashtiradi) — murakkab bo'lsa, oddiy `if`ga qayting.

**Null-coalescing (`??`)** — "agar bor va `null` bo'lmasa o'shani, aks holda zaxira qiymatni":

```php
<?php
// $_GET['ism'] bor bo'lsa o'shani, bo'lmasa "Mehmon"
$ism = $_GET['ism'] ?? "Mehmon";

$sozlama = [];
$til = $sozlama['til'] ?? "uz";   // 'til' kaliti yo'q → "uz"
echo $til;   // uz
```

`??` ayniqsa foydalanuvchi ma'lumoti bilan ishlaganda (`$_GET`, `$_POST`, massiv kalitlari) juda ko'p kerak bo'ladi: "kalit bormi? bo'lsa qiymatini ol, bo'lmasa standart qiymat ber" — bularning hammasi bitta `??` bilan, xatosiz.

> **Diqqat:** `??` faqat `null` (yoki "umuman yo'q") holatini tekshiradi. `?:` esa har qanday "falsy" (bo'sh, 0) qiymatda zaxiraga o'tadi. Foydalanuvchi ma'lumotini olishda odatda `??` to'g'riroq.

### Mashqlar

**Oson**
1. Bir yosh o'zgaruvchisi yarating. Agar 18 dan katta bo'lsa, "Voyaga yetgan" deb chiqaring.
2. Bir songa `if/else` yozing: agar 100 dan katta bo'lsa "katta son", aks holda "kichik son".
3. Bir sonning juft yoki toqligini aniqlang (`% 2` bilan).
4. Bir baho (0-100) o'zgaruvchisi: agar 60 dan katta yoki teng bo'lsa "O'tdi", aks holda "Yiqildi".
5. Bir ob-havo o'zgaruvchisi (`$harorat`): agar 0 dan kichik bo'lsa "Sovuq" deb chiqaring.

**O'rta**
6. Baho tizimini `elseif` bilan yozing: A (90+), B (80+), C (70+), D (60+), F (qolgani).
7. Foydalanuvchi yoshi 18-65 oralig'idami, tekshiring (`&&` bilan: `>= 18` va `<= 65`).
8. Kun nomini tekshiring: shanba yoki yakshanba bo'lsa "dam olish", aks holda "ish kuni" (`||` bilan).
9. Login tekshiruvi: `$ism == "admin"` **va** `$parol == "12345"` bo'lsa "Xush kelibsiz", aks holda "Xato".
10. Bir son musbat, manfiy yoki nolligini aniqlang (uchta holat: `> 0`, `< 0`, `== 0`).

**Qiyin**
11. Oddiy "chegirma" mantig'i: agar xarid summasi 100000 dan katta bo'lsa, 10% chegirma hisoblang va yakuniy narxni chiqaring; aks holda to'liq narxni chiqaring.
12. Yil kabisa (visokosniy) yilmi? Maslahat: yil 4 ga bo'linsa kabisa, lekin 100 ga bo'linsa kabisa emas, agar 400 ga bo'linsa yana kabisa. (Bu — `%` va mantiqiy amallarning yaxshi mashqi. Avval soddaroq: faqat "4 ga bo'linadimi" bilan boshlang.)
13. Eng katta sonni topish: uchta son berilgan, ularning eng kattasini aniqlang va chiqaring (`if/elseif` yoki `&&` bilan).
14. `switch` bilan: hafta kuni raqami (1–7) berilganda, uning nomini chiqaring (1 → "Dushanba" ... 7 → "Yakshanba"); noto'g'ri raqam uchun `default`da "Noma'lum kun".
15. `match` bilan: baho (0–100) berilganda harf bahosini qaytaring (A/B/C/D/F) va chiqaring.
16. Ternary va `??` bilan: `$_GET['ism']` bo'lsa undan, bo'lmasa "Mehmon" oling (`??`), keyin ternary bilan "Salom, &lt;ism&gt;" yoki uzunligi 3 dan kichik bo'lsa "Ism juda qisqa" chiqaring.

<details markdown="1">
<summary>Yechim — 9</summary>

```php
<?php
$ism = "admin";
$parol = "12345";

if ($ism == "admin" && $parol == "12345") {
    echo "Xush kelibsiz!";
} else {
    echo "Login yoki parol xato";
}
```
`&&` tufayli **ikkala** shart ham to'g'ri bo'lsagina "Xush kelibsiz" chiqadi. Birortasi xato bo'lsa — `else` ishlaydi.
</details>

<details markdown="1">
<summary>Yechim — 11</summary>

```php
<?php
$summa = 150000;

if ($summa > 100000) {
    $chegirma = $summa * 0.10;        // 10% = summaning 0.10 qismi
    $yakuniy = $summa - $chegirma;
    echo "Chegirma: " . $chegirma . " so'm<br>";
    echo "To'lov: " . $yakuniy . " so'm";   // 135000
} else {
    echo "To'lov: " . $summa . " so'm";
}
```
</details>

<details markdown="1">
<summary>Yechim — 12 (kabisa yil)</summary>

```php
<?php
$yil = 2024;

// Kabisa: 4 ga bo'linsa, LEKIN 100 ga bo'linmasa; YOKI 400 ga bo'linsa
$kabisa = ($yil % 4 == 0 && $yil % 100 != 0) || ($yil % 400 == 0);

if ($kabisa) {
    echo "$yil — kabisa yil";
} else {
    echo "$yil — oddiy yil";
}
```

Tekshirib ko'ring: `2000` → kabisa (400 ga bo'linadi), `1900` → oddiy (100 ga bo'linadi, lekin 400 ga emas), `2024` → kabisa (4 ga bo'linadi, 100 ga emas). Mantiq murakkab ko'rinsa ham, uni so'z bilan o'qing: *"4 ga bo'linadi **va** 100 ga bo'linmaydi — **yoki** 400 ga bo'linadi"*. `&&` va `||` ni qavslar bilan to'g'ri guruhlash bu yerda kalit.
</details>

<details markdown="1">
<summary>Yechim — 13 (eng katta son)</summary>

```php
<?php
$a = 12;
$b = 45;
$c = 23;

if ($a >= $b && $a >= $c) {
    echo "Eng katta: " . $a;
} elseif ($b >= $a && $b >= $c) {
    echo "Eng katta: " . $b;
} else {
    echo "Eng katta: " . $c;   // bu holatda 45
}
```
Mantiq: `$a` eng katta bo'lishi uchun u **ham** `$b` dan, **ham** `$c` dan katta (yoki teng) bo'lishi kerak — shuning uchun `&&`.
</details>

<details markdown="1">
<summary>Yechim — 14 (switch bilan hafta kuni)</summary>

```php
<?php
$raqam = 3;

switch ($raqam) {
    case 1: echo "Dushanba";  break;
    case 2: echo "Seshanba";  break;
    case 3: echo "Chorshanba"; break;   // 3 → shu yer ishlaydi
    case 4: echo "Payshanba"; break;
    case 5: echo "Juma";      break;
    case 6: echo "Shanba";    break;
    case 7: echo "Yakshanba"; break;
    default: echo "Noma'lum kun";
}
```
Har bir `case`dan keyin `break` borligiga e'tibor bering — usiz keyingi kunlar ham "tushib" chiqib ketardi.
</details>

<details markdown="1">
<summary>Yechim — 15 (match bilan harf bahosi)</summary>

```php
<?php
$baho = 73;

$harf = match(true) {
    $baho >= 90 => "A",
    $baho >= 80 => "B",
    $baho >= 70 => "C",   // 73 → shu yer
    $baho >= 60 => "D",
    default     => "F",
};

echo $harf;   // C
```
`match(true)` oraliqlarni tekshirish uchun ideal: yuqoridan pastga, birinchi `true` bo'lgan shartning natijasini qaytaradi. 1.6'dagi `if/elseif`li baho tizimi bilan solishtiring — `match` ancha ixcham.
</details>

<details markdown="1">
<summary>Yechim — 16 (ternary va ??)</summary>

```php
<?php
$ism = $_GET['ism'] ?? "Mehmon";   // 'ism' kelmasa — "Mehmon"

echo (strlen($ism) < 3)
    ? "Ism juda qisqa"
    : "Salom, $ism";
```
`??` "yo'q bo'lsa zaxira" ni, ternary esa "shartga qarab ikki javobdan biri"ni beradi. Ikkalasi birga — qisqa, o'qiladigan kod.
</details>
