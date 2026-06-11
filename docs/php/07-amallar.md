# 1.4 Amallar (operatorlar)

[⬅️ Oldingi: 1.3 Ma'lumot turlari](./06-malumot-turlari.md) · [🏠 README](./README.md) · [Keyingi: 1.5 Matn bilan ishlash (string) ➡️](./08-matn-bilan-ishlash.md)

---

**Operator** — bu ma'lumot ustida biror amal bajaradigan belgi. Masalan, `+` qo'shadi, `-` ayiradi. Keling, eng kerakli amallarni ko'rib chiqamiz.

### Matematik amallar

```php
<?php
$a = 10;
$b = 3;

echo $a + $b;   // 13  (qo'shish)
echo "<br>";
echo $a - $b;   // 7   (ayirish)
echo "<br>";
echo $a * $b;   // 30  (ko'paytirish)
echo "<br>";
echo $a / $b;   // 3.333...  (bo'lish)
echo "<br>";
echo $a % $b;   // 1   (qoldiq: 10 ni 3 ga bo'lganda qoldiq)
```

Ko'pchiligi maktab matematikasiga o'xshaydi. Faqat ikkitasiga e'tibor bering:
- **`*`** — ko'paytirish (× emas, yulduzcha).
- **`%`** — bu **qoldiq** topadi. `10 % 3` degani: "10 ni 3 ga bo'lganda nechta qoldiq qoladi?" → 3×3=9, qoldiq 1. Bu amal keyinroq (masalan, juft/toq son aniqlashda) juda foydali bo'ladi.

### Daraja (`**`) — sonni darajaga ko'tarish

Sonni o'z-o'ziga necha marta ko'paytirishni qisqa yozish uchun **`**`** (ikkita yulduzcha) ishlatiladi. Maktabda buni "daraja" deb o'rgangansiz: 2⁵ degani 2 ni 5 marta ko'paytirish.

```php
<?php
echo 2 ** 10;   // 1024  (2 ni 10 marta ko'paytirish: 2*2*2*...)
echo "<br>";
echo 5 ** 2;    // 25    (5 ning kvadrati)
echo "<br>";
echo 10 ** 3;   // 1000  (1 va uchta nol)
echo "<br>";
echo 2 ** 0.5;  // 1.4142...  (yarim daraja = kvadrat ildiz)
```

`2 ** 10` ni qo'lda yozsangiz: `2*2*2*2*2*2*2*2*2*2` — uzun va xato qilish oson. `**` bilan bir belgida tayyor.

> **Diqqat — `**` o'ngdan chapga ishlaydi.** Boshqa amallar (`+`, `*`) chapdan o'ngga hisoblanadi, lekin daraja teskari:
>
> ```php
> <?php
> echo 3 ** 3 ** 2;   // 19683, NE 729
> // PHP buni 3 ** (3 ** 2) = 3 ** 9 = 19683 deb o'qiydi
> ```
>
> Agar chapdan boshlanishini xohlasangiz, qavs qo'ying: `(3 ** 3) ** 2`.

### Amallar tartibi

Maktabdagidek: avval ko'paytirish/bo'lish, keyin qo'shish/ayirish. Tartibni o'zgartirish uchun qavs ishlating:

```php
<?php
echo 2 + 3 * 4;     // 14  (avval 3*4=12, keyin +2)
echo "<br>";
echo (2 + 3) * 4;   // 20  (avval qavs ichi 2+3=5, keyin *4)
```

> **Maslahat:** tartibni eslab o'tirmang — shubha bo'lsa, **qavs qo'ying**. Qavs kodni boshqalarga ham, kelajakdagi o'zingizga ham aniqroq qiladi.

### Butun bo'lish — `intdiv()` va qoldiq `%`

`/` amali har doim aniq (kasrli) natija beradi: `10 / 3` → `3.333...`. Lekin ba'zan faqat **butun qism** kerak bo'ladi — masalan, "137 daqiqada nechta to'liq soat bor?". Buning uchun **`intdiv()`** funksiyasi bor:

```php
<?php
echo 10 / 3;          // 3.3333333333333  (kasrli)
echo "<br>";
echo intdiv(10, 3);   // 3   (faqat butun qism)
echo "<br>";
echo intdiv(17, 5);   // 3   (17 ichida 5 ta to'liq beshlik bor)
```

`intdiv()` va `%` ko'pincha **birga** ishlaydi — biri butun qismni, ikkinchisi qoldiqni beradi:

```php
<?php
$daqiqa = 137;
$soat   = intdiv($daqiqa, 60);   // 2   (nechta to'liq soat)
$qolgan = $daqiqa % 60;          // 17  (qolgan daqiqa)
echo "$soat soat $qolgan daqiqa";   // 2 soat 17 daqiqa
```

Tasavvur qiling: 137 ta tangani 60 talik uyumchalarga ajratyapsiz. `intdiv` — nechta to'liq uyum chiqdi (2 ta), `%` — uyumga sig'may qolgan tangalar (17 ta). Ikkalasi birgalikda butun manzarani beradi.

### O'zgaruvchini o'zgartirish (qisqa yozuv)

Ko'pincha o'zgaruvchining qiymatini oshirish kerak bo'ladi:

```php
<?php
$ball = 10;
$ball = $ball + 5;   // $ball endi 15
echo $ball;
```

`$ball = $ball + 5` — "ballning hozirgi qiymatiga 5 qo'shib, qayta ballga sol" degani. Buni qisqaroq yozish mumkin:

```php
<?php
$ball = 10;
$ball += 5;   // yuqoridagining qisqasi: $ball = $ball + 5
echo $ball;   // 15
```

Shunga o'xshash qisqa yozuvlar:
- `$x += 5;` → `$x = $x + 5`
- `$x -= 5;` → `$x = $x - 5`
- `$x *= 2;` → `$x = $x * 2`
- `$x **= 2;` → `$x = $x ** 2` (daraja)
- `$x++;` → `$x ni 1 ga oshir` (`$x = $x + 1`)
- `$x--;` → `$x ni 1 ga kamaytir`

`$x++` ayniqsa sikllar mavzusida (1.7) doim ishlatiladi.

### Matnlarni ulash

Sonlarda `+` qo'shish edi. Matnlarni esa ulash uchun `.` (nuqta) ishlatiladi (buni 1.2'da ko'rgan edik):

```php
<?php
$ism = "Ali";
$salom = "Salom, " . $ism;   // Salom, Ali
echo $salom;
```

> **Muhim farq:** sonlarni qo'shganda `+`, matnlarni ulaganda `.`. Buni aralashtirib yubormang.

### Matnga qo'shib borish — `.=`

`+=` son uchun bo'lgani kabi, matn uchun ham qisqa yozuv bor: **`.=`**. U "hozirgi matnning oxiriga yana matn ulab qo'y" degani — xuddi qatorga so'z qo'shib borgandek.

```php
<?php
$natija = "Salom";
$natija .= ", ";        // $natija = $natija . ", "  qisqasi
$natija .= "dunyo!";
echo $natija;           // Salom, dunyo!
```

Bu, ayniqsa, biror matnni bo'lak-bo'lak yig'ib borishda asqotadi:

```php
<?php
$royxat = "";
$royxat .= "Olma\n";
$royxat .= "Anor\n";
$royxat .= "Uzum\n";
echo $royxat;
// Olma
// Anor
// Uzum
```

Bo'sh `""` dan boshlab, har qatorda yana bir parcha qo'shib boryapmiz. Sikllar mavzusida (1.7) `.=` bilan ro'yxatlar, jadvallar va HTML sahifalarni yig'ish juda ko'p uchraydi.

### Taqqoslash amallari

Ikki narsani solishtirish uchun. Bu amallar natijasi doim `true` (rost) yoki `false` (yolg'on) bo'ladi. Ular asosan "shartlar" (1.6) bilan birga ishlatiladi:

```php
<?php
$a = 10;
$b = 5;

var_dump($a > $b);    // true   (a, b dan katta?)
var_dump($a < $b);    // false  (a, b dan kichik?)
var_dump($a == $b);   // false  (a, b ga teng?)
var_dump($a != $b);   // true   (a, b ga teng emas?)
var_dump($a >= 10);   // true   (a, 10 dan katta yoki teng?)
var_dump($a <= 9);    // false  (a, 9 dan kichik yoki teng?)
```

E'tibor bering:
- Tenglikni tekshirishda **ikkita** teng belgisi (`==`) ishlatiladi. Bitta `=` — bu "saqlash" edi (1.2). Buni aralashtirib yuborish — boshlovchilarda eng ko'p uchraydigan xato!
  - `$a = 5` → "5 ni a ga sol"
  - `$a == 5` → "a, 5 ga tengmi?"
- `!=` — "teng emas".

### Qat'iy tenglik — `===` va `!==` (eng muhim mavzu!)

Yuqorida `==` ni ko'rdik. Lekin PHP da `==` ning bir **xavfli odati** bor: u taqqoslashdan oldin ikki qiymatni "bir turga keltirishga" urinadi. Natijada, ko'rinishidan turlicha qiymatlar `==` ga ko'ra teng chiqib qolishi mumkin:

```php
<?php
var_dump(5 == "5");      // true   (sonni va matnni teng deb hisobladi!)
var_dump("1" == "01");   // true   (ikkalasini son deb o'qidi: 1 == 1)
var_dump(null == false); // true
```

Bunday "yumshoq" taqqoslash boshlovchilarni juda ko'p chalg'itadi va yashirin xatolarga olib keladi. Yechim — **`===`** (uchta teng belgisi), ya'ni **qat'iy tenglik**. U ikki narsa **ham qiymati, ham turi** bilan bir xil bo'lsagina `true` qaytaradi:

```php
<?php
var_dump(5 === "5");     // false  (biri son, biri matn — tur boshqa)
var_dump(5 === 5);       // true   (ikkalasi ham son 5)
var_dump("1" === "01");  // false  (matn sifatida ular har xil)
var_dump(null === false);// false  (null va false — boshqa turlar)
```

Xuddi shunday, "teng emas" uchun ham qat'iy variant bor: **`!==`** ("ham qiymati, ham turi bilan teng emasmi?").

```php
<?php
var_dump(5 !== "5");     // true   (ha, har xil — tur boshqa)
var_dump(5 !== 5);       // false  (yo'q, aynan bir xil)
```

**`==` ning klassik tuzog'i** — matnni songa solishtirish:

```php
<?php
$kiritilgan = "0";              // foydalanuvchi "0" kiritdi (matn)

var_dump($kiritilgan == 0);     // true   ❌ kutilmagan! "0" ni 0 deb o'qidi
var_dump($kiritilgan === 0);    // false  ✅ to'g'ri: "0" (matn) ≠ 0 (son)
```

> **PHP 8 dagi muhim o'zgarish.** PHP 7 va undan oldin `0 == "salom"` ifodasi `true` qaytarardi (matnni `0` deb o'qib). Bu juda ko'p xatolarning sababi edi. PHP 8 dan boshlab bu tuzatildi:
>
> ```php
> <?php
> var_dump(0 == "salom");   // PHP 8: false  (ilgari true edi!)
> var_dump(0 === "salom");  // false (har doim — turlar boshqa)
> ```
>
> Shunday bo'lsa-da, eski tuzoqlardan butunlay xalos bo'lish uchun bitta oddiy qoidaga amal qiling.

> **Oltin qoida:** shubha bo'lsa, har doim **`===`** va **`!==`** ishlating. `==` ni faqat ataylab "yumshoq" taqqoslash kerak bo'lgan kam holatlardagina qo'llang. Zamonaviy PHP kodida `===` standart hisoblanadi.

### Mantiqiy amallar — `&&`, `||`, `!`

Ko'pincha bitta emas, bir nechta shartni **birga** tekshirish kerak bo'ladi. Masalan: "yoshi 18 dan katta **VA** chiptasi bor". Buning uchun mantiqiy amallar bor:

- **`&&`** — "VA" (and). Ikkala tomon ham `true` bo'lsagina, natija `true`.
- **`||`** — "YOKI" (or). Kamida bittasi `true` bo'lsa, natija `true`.
- **`!`** — "EMAS" (not). `true` ni `false` ga, `false` ni `true` ga aylantiradi.

```php
<?php
$yosh = 20;
$pul  = 5000;

// && — ikkala shart ham bajarilsa
var_dump($yosh >= 18 && $pul >= 3000);   // true  (20>=18 VA 5000>=3000)

// || — kamida bittasi bajarilsa
var_dump($yosh < 12 || $yosh > 65);      // false (20 na 12dan kichik, na 65dan katta)

// ! — natijani teskari qiladi
var_dump(!($yosh >= 18));                // false (yoshi 18+, demak "emas" -> false)
```

Hayotiy misol — shartlar (1.6) bilan birga:

```php
<?php
$yosh = 20;
$chipta_bor = true;

if ($yosh >= 18 && $chipta_bor) {
    echo "Konsertga kirishingiz mumkin";
}
```

Buni o'qish oson: "agar yoshi 18+ **va** chiptasi bor bo'lsa". Mantiqiy amallarni xohlagancha zanjirlash mumkin: `$a > 0 && $b > 0 && $c > 0`.

> **`&&` ning aqlli odati (qisqa hisoblash).** `&&` da chap tomon `false` bo'lsa, o'ng tomon umuman tekshirilmaydi (chunki natija baribir `false`). Xuddi shunday `||` da chap tomon `true` bo'lsa, o'ng tomonga qaralmaydi. Bu "qisqa tutashuv" (short-circuit) deyiladi va keyinroq tekshiruvlarni xavfsiz yozishda foydali bo'ladi.

### Tuzoq: `&&`/`||` va `and`/`or` farqi

PHP da mantiqiy "va/yoki" uchun **ikki xil** yozuv bor: `&&`/`||` va so'z bilan `and`/`or`. Ko'rinishidan bir xil ishlaydi:

```php
<?php
var_dump(true && false);   // false
var_dump(true and false);  // false  (xuddi shunday)
```

Lekin ular orasida **prioritet (ustunlik)** farqi bor va bu yashirin tuzoq tug'diradi. `=` (saqlash) amali `and`/`or` dan **kuchliroq**, lekin `&&`/`||` dan **kuchsizroq**:

```php
<?php
// && ni ishlatsak — kutilganidek
$x = true && false;
var_dump($x);   // false  ✅

// and ni ishlatsak — TUZOQ!
$y = true and false;   // ❌ aslida bu: ($y = true) and false
var_dump($y);   // true  (!) — chunki avval $y = true bajarildi
```

Ikkinchi holatda PHP buni `($y = true) and false` deb o'qiydi: avval `$y` ga `true` saqlanadi, keyin `and false` ortiqcha bo'lib qoladi. Natijada `$y` `false` emas, `true` bo'lib chiqadi — ajablanarli xato!

> **Oddiy qoida:** har doim **`&&`** va **`||`** ishlating. `and`/`or` ni esa unutib qo'yganingiz ma'qul — ular faqat eski yoki o'ziga xos kodlarda uchraydi va yangi kodda kerak emas.

### Shartli amallar — `?:` (ternary) va `??` (null-coalescing)

Ba'zan "agar shunday bo'lsa — buni, aks holda — buni" degan tanlovni **bitta qatorda** yozish kerak bo'ladi. Buning uchun qisqa amallar bor.

**Uchlik (ternary) amal `? :`** — bu qisqa `if/else`:

```php
<?php
$yosh = 20;

// shart ? rost-bo'lsa : yolg'on-bo'lsa
$holat = ($yosh >= 18) ? "Voyaga yetgan" : "Voyaga yetmagan";
echo $holat;   // Voyaga yetgan
```

O'qilishi: "yoshi 18+ mi? Ha bo'lsa — 'Voyaga yetgan', yo'q bo'lsa — 'Voyaga yetmagan'". Buni to'liq `if/else` bilan yozsa 5 qator bo'lardi; ternary bilan — bir qator.

**Qisqa ternary `?:`** (Elvis amali deb ham ataladi) — agar qiymatning o'zi "bor/rost" bo'lsa o'zini, bo'lmasa muqobilni beradi:

```php
<?php
$ism = "";
$korinish = $ism ?: "Mehmon";   // $ism bo'sh -> "Mehmon"
echo $korinish;                 // Mehmon

$ism2 = "Ali";
echo $ism2 ?: "Mehmon";         // Ali ($ism2 to'la -> o'zini beradi)
```

**Null-birlashtiruvchi amal `??`** — bu eng ko'p ishlatiladigan zamonaviy amallardan biri. U "agar qiymat **yo'q** (`null`) bo'lsa, o'rniga shuni ber" degani. Eng muhimi: agar o'zgaruvchi yoki massiv kaliti **umuman mavjud bo'lmasa ham**, `??` xato (warning) bermaydi:

```php
<?php
$sozlama = null;
$qiymat = $sozlama ?? "standart";
echo $qiymat;   // standart

// Massivda bo'lmagan kalit — xato emas, muqobil qiymat:
$data = ["ism" => "Ali"];
echo $data["familiya"] ?? "Noma'lum";   // Noma'lum (warning yo'q!)
```

Bu, ayniqsa, foydalanuvchidan kelgan ma'lumotlarda (forma, URL) juda asqotadi:

```php
<?php
// Agar URL da ?sahifa=... berilmagan bo'lsa, 1 dan boshlaymiz:
$sahifa = $_GET["sahifa"] ?? 1;
echo "Sahifa: $sahifa";
```

**`??=` amali** — `??` ning qisqa yozuvi: "agar o'zgaruvchi `null` bo'lsa, unga shu qiymatni sol":

```php
<?php
$til = null;
$til ??= "uz";   // $til null edi -> "uz" bo'ldi
echo $til;       // uz

$til2 = "en";
$til2 ??= "uz";  // $til2 null emas -> o'zgarmaydi
echo $til2;      // en
```

> **`?:` va `??` farqi.** Qisqa `?:` qiymat "bo'sh/yolg'on" bo'lsa (masalan `0`, `""`, `false`) ham muqobilga o'tadi. `??` esa **faqat `null`** bo'lganda o'tadi. Shuning uchun "yo'qmi?" degan ma'no kerak bo'lsa — `??`, "bo'shmi?" degan ma'no kerak bo'lsa — `?:` ishlating.

### Taqqoslash amali — `<=>` (kosmik kema) va saralash

`<=>` (uchta belgi: kichik-teng-katta, "kosmik kema" deb ataladi) — bu ikki qiymatni solishtirib, **uchta natijadan birini** qaytaradi:

- chap kichik bo'lsa → `-1`
- teng bo'lsa → `0`
- chap katta bo'lsa → `1`

```php
<?php
var_dump(1 <=> 2);   // -1  (chap kichik)
var_dump(2 <=> 2);   //  0  (teng)
var_dump(3 <=> 2);   //  1  (chap katta)
```

Bir o'zida "kichikmi, tengmi, kattami" degan uchala savolga javob beradi. Uning asosiy foydasi — **saralash (sort)**. PHP ning `usort()` funksiyasi ro'yxatni tartiblaganda, har juft elementni qanday joylashni `<=>` orqali biladi:

```php
<?php
$sonlar = [5, 2, 8, 1, 9, 3];

// O'sish tartibi (kichikdan kattaga):
usort($sonlar, fn($a, $b) => $a <=> $b);
print_r($sonlar);   // [1, 2, 3, 5, 8, 9]

// Kamayish tartibi (kattadan kichikka) — $a va $b o'rnini almashtiramiz:
usort($sonlar, fn($a, $b) => $b <=> $a);
print_r($sonlar);   // [9, 8, 5, 3, 2, 1]
```

Bu yerda `fn($a, $b) => ...` — qisqa funksiya (bu mavzuni keyinroq, funksiyalar bo'limida batafsil ko'ramiz). Hozircha shuni eslab qoling: **`$a <=> $b` o'sish tartibi, `$b <=> $a` kamayish tartibi** beradi. Aniq kodni hozir tushunmasangiz ham, `<=>` ning vazifasi — "ikkitasidan qaysi biri oldinroq turishi kerak" degan savolga javob berish.

### Asosiy matematik funksiyalar

Amallardan tashqari, PHP da tayyor matematik **funksiyalar** ham bor. Ular son ustida amal bajarib, natijani qaytaradi. Eng kerakliylari:

```php
<?php
echo abs(-7);            // 7      modul: manfiyni musbatga aylantiradi
echo "<br>";
echo round(3.7);         // 4      yaqin butun songa yaxlitlash
echo "<br>";
echo round(3.14159, 2);  // 3.14   2 xona aniqlikda yaxlitlash
echo "<br>";
echo ceil(3.2);          // 4      doim YUQORIga yaxlitlash (shift)
echo "<br>";
echo floor(3.9);         // 3      doim PASTga yaxlitlash (pol)
echo "<br>";
echo pow(2, 8);          // 256    daraja (2 ** 8 bilan bir xil)
echo "<br>";
echo sqrt(144);          // 12     kvadrat ildiz
echo "<br>";
echo max(3, 7, 2);       // 7      eng kattasi
echo "<br>";
echo min(3, 7, 2);       // 2      eng kichigi
echo "<br>";
echo max([4, 1, 9, 6]);  // 9      massivdan ham topadi
```

Qisqacha:
- **`abs($x)`** — sonning moduli (ishorasiz kattaligi). Ikki son orasidagi farqni topishda qulay: `abs($a - $b)` — qaysi biri katta bo'lishidan qat'i nazar, har doim musbat farq.
- **`round($x)`** — eng yaqin butun songa yaxlitlaydi (`3.5` → `4`). Ikkinchi argument — necha xonagacha (pul hisobida `round($narx, 2)` juda asqotadi).
- **`ceil($x)`** — har doim **yuqoriga** (`3.1` ham `4`). "Kerakli qutilar soni" kabi hisoblarda kerak.
- **`floor($x)`** — har doim **pastga** (`3.9` ham `3`).
- **`pow($a, $b)`** — daraja, `**` amali bilan teng.
- **`sqrt($x)`** — kvadrat ildiz.
- **`max(...)`** / **`min(...)`** — bir nechta sondan (yoki massivdan) eng katta/kichigini topadi.

Hayotiy misollar:

```php
<?php
// Doira yuzasi: S = pi * r^2  (M_PI — tayyor pi qiymati)
$radius = 5;
$yuza = M_PI * $radius ** 2;
echo round($yuza, 2);            // 78.54
echo "<br>";

// Ikki harorat orasidagi farq (qaysi kattaligidan qat'i nazar):
$temp1 = -10;
$temp2 = 25;
echo "Farq: " . abs($temp1 - $temp2) . " daraja";   // Farq: 35 daraja
```

### Mashqlar

**Oson**
1. Ikkita son yarating va ularning yig'indisi, ayirmasi, ko'paytmasini chiqaring.
2. `17 % 5` ni hisoblang va natijani ko'ring (qoldiq necha?).
3. `$ball = 100;` yarating, `$ball += 50;` qiling va chiqaring.
4. `$soni = 5;` yarating, `$soni++;` qiling va chiqaring (necha bo'ldi?).
5. `2 + 3 * 4` va `(2 + 3) * 4` natijalarini solishtiring.
6. `2 ** 8` (ikkining sakkizinchi darajasi) ni hisoblang va chiqaring.
7. `$xabar = "Salom";` yarating, `.=` bilan unga `", dunyo!"` ni qo'shib, chiqaring.

**O'rta**
8. Do'kon hisobi: `$narx = 5000;` va `$soni = 3;` — umumiy summani (`narx * soni`) hisoblang.
9. Ikkita son teng yoki teng emasligini `==` va `!=` bilan tekshiring (`var_dump` orqali).
10. `$a = 10; $b = 20;` — `$a > $b` va `$a < $b` natijalarini chiqaring.
11. Bir o'zgaruvchining qiymatini avval `*= 2`, keyin `+= 10` qilib o'zgartiring, har bosqichda chiqaring.
12. `5 == "5"` va `5 === "5"` natijalarini `var_dump` bilan solishtiring va farqini izohlang.
13. Foydalanuvchining yoshi (`$yosh`) va haydovchilik guvohnomasi bor-yo'qligini (`$guvohnoma = true;`) tekshirib, `&&` orqali "Mashina haydashi mumkin/mumkin emas" degan natijani chiqaring.
14. `$til = null;` yarating, `??` bilan unga muqobil `"uz"` qiymatini bering va chiqaring.
15. Ternary `?:` bilan `$ball` 60 dan katta yoki tengmi — "O'tdi"/"Yiqildi" deb chiqaring.

**Qiyin**
16. To'liq xarid hisobi: 3 ta mahsulot (har birining narxi va soni), umumiy summani hisoblang va chiqaring.
17. Ikki xonali sonning birliklar xonasini toping. Maslahat: `% 10` (10 ga bo'lgandagi qoldiq) birliklar xonasini beradi. Masalan, `47 % 10 = 7`.
18. Daqiqani soat va daqiqaga ajrating: `$daqiqa = 200;` ni `intdiv` va `%` yordamida `"X soat Y daqiqa"` ko'rinishida chiqaring.
19. Ballar ro'yxatini (`[88, 42, 95, 67, 73]`) `usort` va `<=>` bilan kattadan kichikka saralang, so'ng `max`/`min` bilan eng yuqori va eng past ballni chiqaring.
20. Doira yuzasi va aylana uzunligini hisoblang: `$r = 7;` uchun `S = pi * r^2` va `L = 2 * pi * r`, natijalarni `round` bilan 2 xonagacha yaxlitlab chiqaring.

<details markdown="1">
<summary>Yechim — 7</summary>

```php
<?php
$xabar = "Salom";
$xabar .= ", dunyo!";   // $xabar = $xabar . ", dunyo!"
echo $xabar;            // Salom, dunyo!
```
`.=` matnning oxiriga yangi parchani ulab qo'yadi. `+=` son uchun nima qilsa, `.=` matn uchun shuni qiladi.
</details>

<details markdown="1">
<summary>Yechim — 8</summary>

```php
<?php
$narx = 5000;
$soni = 3;
$umumiy = $narx * $soni;
echo "Umumiy summa: " . $umumiy . " so'm";   // Umumiy summa: 15000 so'm
```
</details>

<details markdown="1">
<summary>Yechim — 12</summary>

```php
<?php
var_dump(5 == "5");    // true  — == tipni o'zgartiradi: "5" ni 5 deb o'qidi
var_dump(5 === "5");   // false — === tipni ham tekshiradi: son ≠ matn
```
`==` faqat qiymatga qaraydi va ularni "bir turga keltirishga" urinadi, shuning uchun son `5` va matn `"5"` teng chiqadi. `===` esa ham qiymat, ham turni tekshiradi — biri son, biri matn bo'lgani uchun `false`. Zamonaviy kodda har doim `===` ni afzal bilng.
</details>

<details markdown="1">
<summary>Yechim — 13</summary>

```php
<?php
$yosh = 19;
$guvohnoma = true;

$natija = ($yosh >= 18 && $guvohnoma) ? "Mashina haydashi mumkin" : "Mumkin emas";
echo $natija;   // Mashina haydashi mumkin
```
`&&` ikkala shart ham bajarilishini talab qiladi: yoshi 18+ **va** guvohnomasi bor. Bittasi yetishmasa — "Mumkin emas".
</details>

<details markdown="1">
<summary>Yechim — 14</summary>

```php
<?php
$til = null;
$natijaviy_til = $til ?? "uz";   // null bo'lgani uchun -> "uz"
echo $natijaviy_til;             // uz
```
`??` faqat qiymat `null` bo'lganda muqobilga o'tadi. Agar `$til = "en"` bo'lganida, natija `"en"` bo'lardi.
</details>

<details markdown="1">
<summary>Yechim — 15</summary>

```php
<?php
$ball = 75;
$natija = ($ball >= 60) ? "O'tdi" : "Yiqildi";
echo $natija;   // O'tdi
```
Ternary `shart ? rost : yolg'on` — qisqa `if/else`. Bir qatorda butun tanlovni yozadi.
</details>

<details markdown="1">
<summary>Yechim — 16 (to'liq xarid hisobi)</summary>

```php
<?php
$jami = 0;

$jami += 5000 * 3;     // 1-mahsulot: narx 5000, 3 dona = 15000
$jami += 12000 * 2;    // 2-mahsulot: 24000
$jami += 800 * 10;     // 3-mahsulot: 8000

echo "Umumiy summa: " . $jami . " so'm";   // 47000 so'm
```
Har bir mahsulot uchun `narx * soni` ni `$jami`ga qo'shamiz (`+=`). Oxirida `$jami` — butun xarid summasi. (Keyinroq, massiv va sikllar bilan, buni yanada chiroyli yozish mumkin bo'ladi.)
</details>

<details markdown="1">
<summary>Yechim — 17</summary>

```php
<?php
$son = 47;
$birliklar = $son % 10;   // 47 ni 10 ga bo'lganda qoldiq = 7
echo "Birliklar xonasi: " . $birliklar;   // 7
```

`% 10` har doim oxirgi raqamni beradi: `123 % 10 = 3`, `90 % 10 = 0`. Bu kichik hiyla turli joyda asqotadi.
</details>

<details markdown="1">
<summary>Yechim — 18</summary>

```php
<?php
$daqiqa = 200;
$soat   = intdiv($daqiqa, 60);   // 3   (nechta to'liq soat)
$qolgan = $daqiqa % 60;          // 20  (qolgan daqiqa)
echo "$soat soat $qolgan daqiqa";   // 3 soat 20 daqiqa
```
`intdiv` butun qismni (to'liq soatlar), `%` esa qoldiqni (sig'may qolgan daqiqalar) beradi. Ikkalasi birga butun manzarani ko'rsatadi.
</details>

<details markdown="1">
<summary>Yechim — 19</summary>

```php
<?php
$ballar = [88, 42, 95, 67, 73];

usort($ballar, fn($a, $b) => $b <=> $a);   // kattadan kichikka
print_r($ballar);   // [95, 88, 73, 67, 42]

echo "Eng yuqori ball: " . max($ballar);   // 95
echo "<br>";
echo "Eng past ball: " . min($ballar);     // 42
```
`$b <=> $a` kamayish tartibi beradi. `max`/`min` esa ro'yxatdagi eng katta/kichik qiymatni topadi (saralanganmi yoki yo'qmi — farqi yo'q).
</details>

<details markdown="1">
<summary>Yechim — 20</summary>

```php
<?php
$r = 7;

$yuza   = M_PI * $r ** 2;    // S = pi * r^2
$uzunlik = 2 * M_PI * $r;    // L = 2 * pi * r

echo "Yuza: " . round($yuza, 2);       // Yuza: 153.94
echo "<br>";
echo "Aylana: " . round($uzunlik, 2);  // Aylana: 43.98
```
`M_PI` — PHP da tayyor pi (≈3.14159) qiymati. `**` daraja, `round($x, 2)` esa natijani 2 xonagacha yaxlitlaydi (pul yoki o'lchovlarda doim qulay).
</details>
