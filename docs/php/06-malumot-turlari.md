# 1.3 Ma'lumot turlari

[⬅️ Oldingi: 1.2 O'zgaruvchilar (variables)](./05-ozgaruvchilar.md) · [🏠 README](./README.md) · [Keyingi: 1.4 Amallar (operatorlar) ➡️](./07-amallar.md)

---

O'zgaruvchi ichiga turli xil ma'lumot saqlash mumkin: matn, son, "ha/yo'q" qiymati va boshqalar. Bularning har biri — alohida **tur** (type). PHP'ning asosiy turlarini ko'rib chiqamiz. Buni bilish muhim, chunki turli turdagi ma'lumotlar turlicha ishlaydi.

### 1) Matn (string) — harflar, so'zlar, gaplar

Matn doim **qo'shtirnoq** (yoki bittalik tirnoq) ichida yoziladi:

```php
<?php
$ism = "Ali";
$gap = "Bugun havo issiq";
$telefon = "998901234567";   // bu ham matn (raqam ko'rinishida bo'lsa ham)
```

> Diqqat: `"998901234567"` — bu matn, son emas, chunki tirnoq ichida. Telefon raqami, pasport raqami kabilarni matn sifatida saqlash to'g'ri — chunki ular bilan hisob-kitob qilmaymiz.

### 2) Butun son (integer) — kasrsiz sonlar

Tirnoqsiz yozilgan, nuqtasiz sonlar:

```php
<?php
$yosh = 19;
$narx = 5000;
$temperatura = -10;   // manfiy son ham bo'ladi
```

Bular bilan matematik amallar bajarish mumkin (qo'shish, ayirish va h.k.).

### 3) Kasr son (float) — nuqtali sonlar

Kasr qism bo'lgan sonlar. Kasr **nuqta** bilan yoziladi (vergul emas!):

```php
<?php
$narx = 19.99;
$ball = 4.5;
$pi = 3.14;
```

> Eslatma: o'zbekchada "uch butun o'n to'rt" deb vergul ishlatamiz, lekin dasturlashda **nuqta** ishlatiladi: `3.14`.

### 4) Mantiqiy qiymat (boolean) — faqat "ha" yoki "yo'q"

Ba'zan bizga faqat ikki holatdan biri kerak bo'ladi: rost yoki yolg'on, ha yoki yo'q, yoniq yoki o'chiq. Buni `true` (rost) yoki `false` (yolg'on) bilan ifodalaymiz:

```php
<?php
$tizimga_kirgan = true;    // ha, kirgan
$xat_yuborilgan = false;   // yo'q, yuborilmagan
```

Bu tur ayniqsa "shartlar" mavzusida (1.6) juda kerak bo'ladi. Hozircha shuni bilsangiz yetarli: `true` — rost, `false` — yolg'on.

### 5) Bo'shliq (null) — "hech narsa"

`null` — "bu qutida hozircha hech narsa yo'q" degani:

```php
<?php
$tanlangan_mahsulot = null;   // hali hech narsa tanlanmagan
```

Buni keyinroq ko'proq ishlatamiz. Hozircha shunchaki "bo'sh, hech narsa yo'q" deb eslang.

### Raqamli ajratgich — katta sonlarni o'qiy oladigan qilish

Bir million — `1000000`. Bir qarashda nechta nol borligini sanash qiyin. PHP'da (7.4 versiyadan beri) sonlar ichida **pastki chiziq** `_` qo'yib, raqamlarni guruhlash mumkin. Bu faqat **odam o'qishi uchun** — kompyuter `_` belgisini umuman e'tiborga olmaydi:

```php
<?php
$aholi = 1_000_000;       // bir million — endi nollarni sanash oson
$narx  = 1_500_000;       // bir yarim million
$pi    = 3.141_592_653;   // kasr sonlarda ham mumkin

var_dump($aholi);          // int(1000000) — _ belgisi yo'qoladi
echo $aholi + $narx, "\n"; // 2500000 — oddiy son kabi ishlaydi
```

> Bu o'zgaruvchining turini o'zgartirmaydi: `1_000_000` ham, `1000000` ham bir xil `int`. `_` — bu shunchaki "qulflik belgi" bo'lib, biz uchun sonni o'qishni osonlashtiradi, xolos. `1_00_00` kabi notekis qo'ysangiz ham ishlaydi (lekin har 3 raqamda qo'ygan mantiqiyroq).

### Turni tekshirish

O'zgaruvchining turi nima ekanini bilish uchun `var_dump()` ishlatiladi. Bu — kodni tekshirishda juda foydali vosita:

```php
<?php
$ism = "Ali";
$yosh = 19;
$narx = 19.99;
$kirgan = true;

var_dump($ism);    // string(3) "Ali"  → matn, 3 ta harf
var_dump($yosh);   // int(19)           → butun son
var_dump($narx);   // float(19.99)      → kasr son
var_dump($kirgan); // bool(true)        → mantiqiy
```

`var_dump` o'zgaruvchining ham turini, ham qiymatini ko'rsatadi. Kod kutilganidek ishlamayotganda, "o'zgaruvchida nima turibdi ekan?" deb tekshirish uchun ishlatiladi.

### `gettype()` va `settype()` — turni nomini olish va o'zgartirish

`var_dump` qulay, lekin ba'zan bizga faqat **tur nomi** matn ko'rinishida kerak bo'ladi (masalan, shart yozish uchun). Buning uchun `gettype()` bor:

```php
<?php
$x = 19;
echo gettype($x), "\n";    // integer
$x = "salom";
echo gettype($x), "\n";    // string
$x = 3.14;
echo gettype($x), "\n";    // double  (diqqat: float uchun "double" deyiladi!)
$x = true;
echo gettype($x), "\n";    // boolean
$x = null;
echo gettype($x), "\n";    // NULL
```

> Bir hiyla-nuqta: float turi `gettype()` da `"double"` deb chiqadi (tarixiy sabab bilan). Bu odamni adashtirishi mumkin — esda tuting: `"double"` = `float`.

`settype()` esa o'zgaruvchining turini **joyida o'zgartiradi** (cast'dan farqi: yangi o'zgaruvchi yaratmaydi, eskisining turini almashtiradi):

```php
<?php
$son = "100";
echo gettype($son), "\n";  // string
settype($son, "integer");  // turni o'zgartiramiz
echo gettype($son), "\n";  // integer
var_dump($son);            // int(100)
```

Amaliyotda `settype()` kamroq ishlatiladi — pastda ko'radigan aniq cast (`(int)`, `(float)`...) ko'proq o'qiladigan va xavfsizroq. Lekin `gettype()` xatolarni tekshirishda asqotadi.

### Type juggling — avtomatik tur o'girilishi

PHP — "yumshoq turli" (loosely typed) til. Bu degani: agar siz har xil turdagi qiymatlarni bir amalda aralashtirsangiz, PHP ularni **o'zi avtomatik** mos turga o'giradi. Bu hodisa **type juggling** ("tur jonglyorligi") deb ataladi.

Eng klassik misol — son ko'rinishidagi matnni songa qo'shish:

```php
<?php
$natija = "5" + 3;
var_dump($natija);     // int(8)  → "5" avtomatik 5 soniga o'girildi
echo $natija, "\n";    // 8

$narx = "100";
$jami = $narx * 2;
var_dump($jami);       // int(200)  → "100" matni 100 soniga aylandi
```

Bu qulay tuyuladi, lekin **xatarli**. Agar matn toza son bo'lmasa nima bo'ladi? PHP boshidagi sonni oladi-yu, **ogohlantirish** (Warning) chiqaradi:

```php
<?php
$natija = "5 ta" + 3;
var_dump($natija);
// Warning: A non-numeric value encountered ...
// int(8)  → "5 ta" dan faqat 5 olindi
```

> Bu ogohlantirish bejiz emas: "Sen menga aralash narsa berding, men taxmin qildim — lekin bu xato bo'lishi mumkin" degani. Forma orqali kelgan ma'lumotlarni shu tarzda qo'shmang — avval `is_numeric` bilan tekshirib, keyin aniq cast qiling (pastda ko'ramiz).

Matnlarni **ulash** uchun esa `+` emas, **nuqta** `.` ishlatiladi — u har doim matn natija beradi (type juggling'siz, xavfsiz):

```php
<?php
echo "salom" . 5;   // "salom5"  → nuqta hamma narsani matnga aylantirib ulaydi
echo 7 . 8;         // "78"      → ikki son ham matn bo'lib qo'shildi (yondi)
```

#### Mantiqiy (bool) kontekst — qaysi qiymatlar "yolg'on" hisoblanadi?

`if`, `while` kabi joylarda PHP qiymatni avtomatik `bool` ga o'giradi. Ko'pchilik qiymat `true`, lekin bir nechtasi `false` hisoblanadi. **Yodda tuting** — bu ro'yxat juda muhim:

```php
<?php
// Bularning hammasi FALSE ga o'giriladi:
var_dump((bool) 0);        // false  → noldan iborat son
var_dump((bool) 0.0);      // false  → nol kasr
var_dump((bool) "");       // false  → bo'sh matn
var_dump((bool) "0");      // false  → "0" matni ham false! (tuzoq)
var_dump((bool) []);       // false  → bo'sh massiv
var_dump((bool) null);     // false  → null

echo "---\n";

// Qolgan hamma narsa TRUE:
var_dump((bool) 1);        // true
var_dump((bool) -5);       // true  → manfiy son ham true (0 emas-ku)
var_dump((bool) "salom");  // true
var_dump((bool) "0.0");    // true  → "0.0" matni TRUE! (faqat "0" false)
var_dump((bool) "false");  // true  → bu matn, bo'sh emas → true (tuzoq!)
var_dump((bool) [0]);      // true  → ichida element bor (qiymat 0 bo'lsa ham)
```

> Ikkita asosiy tuzoq: (1) `"0"` matni `false` ga o'giriladi — bu sizni adashtirishi mumkin. (2) `"false"` matni esa `true` — chunki u bo'sh emas, oddiy 5 harfli matn. `true`/`false` so'zlari faqat tirnoqsiz yozilganda mantiqiy qiymat bo'ladi.

#### Loose (`==`) va Strict (`===`) solishtirish — eng muhim farq

PHP'da ikki xil "tenglik" bor:

- `==` (loose / yumshoq) — **faqat qiymatni** solishtiradi, kerak bo'lsa turlarni avtomatik o'giradi.
- `===` (strict / qat'iy) — **ham qiymat, ham turni** solishtiradi. Tur har xil bo'lsa, darrov `false`.

```php
<?php
var_dump("1" == 1);     // true   → qiymatlar teng (matn songa o'girildi)
var_dump("1" === 1);    // false  → biri matn, biri son — turlar har xil!

var_dump(0 == "0");     // true
var_dump(0 === "0");    // false

var_dump("10" == "1e1"); // true  → ikkalasi ham 10 soni (e1 = ilmiy yozuv)
var_dump(100 == "1e2");  // true  → "1e2" = 1 * 10^2 = 100
```

**Maslahat:** shubha bo'lsa — har doim `===` ishlating. U "sehrli" o'girishlarsiz, aniq solishtiradi va kutilmagan xatolardan saqlaydi.

#### PHP 8 da o'zgargan xulq — `0 == "abc"` endi `false`!

Bu juda muhim tarixiy o'zgarish. **Eski PHP (7 va undan oldin)** da `0 == "abc"` natijasi `true` edi — chunki PHP `"abc"` ni songa o'girishga urinib, uni `0` deb hisoblardi va `0 == 0` → `true` chiqardi. Bu son-sanoqsiz xavfsizlik teshigi va xatolarning manbai bo'lgan.

**PHP 8** dan boshlab mantiq teskari o'zgartirildi: agar matn **toza son emas** bo'lsa, son matnga o'giriladi (matn songa emas). Natijada:

```php
<?php
var_dump(0 == "abc");   // PHP 8: false   (eski PHP 7 da bu true edi!)
var_dump(0 == "");      // PHP 8: false   (eski PHP 7 da true edi!)
var_dump(0 == "0");     // true   → "0" toza son, shuning uchun hali ham true
var_dump(42 == "42");   // true   → toza son, songa o'giriladi
var_dump(42 == "42abc"); // false → toza son emas
```

> Nima uchun bu muhim? Tasavvur qiling, eski kodda `if ($parol == 0)` deb yozilgan va foydalanuvchi `"abc"` kiritgan. PHP 7 da bu `true` chiqib, xavfsizlik buzilardi. PHP 8 bu xatoni tuzatdi. Agar siz eski qo'llanmalardan o'rgansangiz, bu farqni bilib qo'ying.

### Aniq tur o'girish (type casting) — o'zingiz boshqaring

Type juggling avtomatik va ba'zan xatarli. Yaxshi dasturchi turni **o'zi aniq** o'giradi. Buning uchun qiymat oldiga qavs ichida tur nomi yoziladi — bu **cast** deyiladi:

```php
<?php
var_dump((int) "42");       // int(42)   → matn butun songa
var_dump((int) "42 yosh");  // int(42)   → boshidagi son olinadi
var_dump((int) "yosh 42");  // int(0)    → boshida son yo'q → 0
var_dump((int) 19.99);      // int(19)   → kasr qismi TASHLANADI (yaxlitlanmaydi!)

var_dump((float) "3.14");   // float(3.14)
var_dump((float) "3.14 kg"); // float(3.14) → boshidagi kasr son

var_dump((string) 100);     // string(3) "100"  → son matnga
var_dump((string) true);    // string(1) "1"    → true → "1"
var_dump((string) false);   // string(0) ""     → false → bo'sh matn! (tuzoq)

var_dump((bool) "0");       // false
```

> Eng tez-tez adashtiradigan joy: `(int) 19.99` natijasi **19**, ya'ni 20 emas! Cast kasr qismni shunchaki **kesib tashlaydi**, yaxlitlamaydi. Agar yaxlitlash kerak bo'lsa, `round()` ishlating: `(int) round(19.99)` → 20.

`intval()` va `floatval()` funksiyalari ham xuddi shunday ishlaydi (cast'ning funksiya ko'rinishi). `intval()` ning qo'shimcha imkoni bor — ikkinchi argument bilan **sanoq sistemasini** ko'rsatish mumkin:

```php
<?php
var_dump(intval("250 so'm"));  // int(250)
var_dump(floatval("19.99$"));  // float(19.99)

var_dump(intval("FF", 16));    // int(255)  → 16 lik (hex) sanoqdagi FF = 255
var_dump(intval("101", 2));    // int(5)    → 2 lik (binary) 101 = 5
```

### `is_*` oilasi — turni xavfsiz tekshirish

Cast qilishdan oldin "bu qiymat aslida nima turida?" deb tekshirish kerak bo'ladi. Buning uchun `is_` bilan boshlanadigan funksiyalar bor. Ular har doim `true` yoki `false` qaytaradi:

```php
<?php
$yosh   = 19;
$ism    = "Ali";
$narx   = 19.99;
$kirgan = true;
$bosh   = null;
$royxat = [1, 2, 3];

var_dump(is_int($yosh));      // true
var_dump(is_string($ism));    // true
var_dump(is_float($narx));    // true
var_dump(is_bool($kirgan));   // true
var_dump(is_null($bosh));     // true
var_dump(is_array($royxat));  // true
```

Alohida bitta funksiya — `is_numeric()` — juda foydali. U "bu qiymat son **yoki son ko'rinishidagi matnmi**?" degan savolga javob beradi. Forma orqali kelgan ma'lumotni tekshirishda ayni muddao:

```php
<?php
var_dump(is_numeric("123"));    // true   → son ko'rinishidagi matn
var_dump(is_numeric("19.99"));  // true   → kasr son ko'rinishi
var_dump(is_numeric(42));       // true   → oddiy son
var_dump(is_numeric("12abc"));  // false  → aralash, toza son emas

var_dump(is_int("19"));         // false  → diqqat: bu MATN, int emas!
```

> Farqni sezing: `is_int("19")` → `false`, chunki `"19"` matn turida (`is_int` faqat haqiqiy `int` turini tekshiradi). Lekin `is_numeric("19")` → `true`, chunki u "songa o'girilishi mumkinmi?" deb qaraydi. Foydalanuvchi kiritgan ma'lumot deyarli har doim **matn** bo'lib keladi, shuning uchun `is_numeric` ko'proq asqotadi.

Mana xavfsiz uslub — avval `is_numeric` bilan tekshir, keyin aniq cast qil:

```php
<?php
$kiritilgan = "25";   // forma orqali kelgan, deylik (matn)

if (is_numeric($kiritilgan)) {
    $yosh = (int) $kiritilgan;   // endi xavfsiz songa o'giramiz
    echo "Yosh: $yosh\n";        // Yosh: 25
} else {
    echo "Xato: son kiriting!\n";
}
```

### Float (kasr son) aniqligi — `0.1 + 0.2` muammosi

Bu — har bir dasturchi bir marta hayron bo'ladigan klassik "tuzoq". Kompyuter kasr sonlarni ikkilik (binary) tizimda saqlaydi va `0.1`, `0.2` kabi sonlar u yerda **aniq** ifodalanmaydi (xuddi `1/3` ni o'nlik kasrda aniq yoza olmaganimiz kabi: 0.333...). Natijada:

```php
<?php
$natija = 0.1 + 0.2;
var_dump($natija);          // float(0.30000000000000004)  → 0.3 emas!
var_dump($natija == 0.3);   // false   (!!! kutilmagan natija)
var_dump($natija === 0.3);  // false
```

Ko'p odam buni ko'rib "PHP buzuq" deb o'ylaydi. Yo'q — bu **barcha** tillarda (Python, JavaScript, C...) shunday, chunki bu protsessorning kasr son saqlash usuli (IEEE 754 standarti).

**Qoida:** kasr sonlarni hech qachon `==` yoki `===` bilan to'g'ridan-to'g'ri solishtirmang. To'g'ri yo'l — `round()` bilan kerakli aniqlikka yaxlitlab solishtirish:

```php
<?php
$natija = 0.1 + 0.2;

// ✅ round bilan ma'lum xona aniqlikda solishtirish
var_dump(round($natija, 2) == 0.3);   // true
echo round($natija, 2), "\n";          // 0.3

// ✅ yoki ayirma juda kichik ekanini tekshirish
$farq = abs($natija - 0.3);
var_dump($farq < 0.00001);             // true  → "deyarli teng"
```

> Pul-mablag' bilan ishlaganda bu ayniqsa muhim. Ko'p loyihalarda narxlar **tiyin/sent** sifatida butun sonda saqlanadi (masalan, 19.99 so'm o'rniga 1999 tiyin), shunda kasr aniqligi muammosi umuman bo'lmaydi.

### `declare(strict_types=1)` — turlarni qat'iy talab qilish

PHP avtomatik type juggling qiladi, dedik. Lekin yirik loyihalarda bu "yumshoqlik" xatolarni yashiradi. Shuning uchun zamonaviy PHP'da funksiya argumentlariga **tur belgilash** va faylning **eng tepasiga** maxsus qator qo'yish odat bo'ldi:

```php
<?php
declare(strict_types=1);   // FAYLNING ENG BIRINCHI qatori bo'lishi shart!

function kvadrat(int $son): int {   // int kiradi, int qaytadi
    return $son * $son;
}

echo kvadrat(5), "\n";   // 25  → to'g'ri
echo kvadrat(9), "\n";   // 81
```

`strict_types=1` bo'lganda PHP turni **avtomatik o'girmaydi** — agar funksiya `int` kutsa-yu, siz matn bersangiz, darrov **xato** (TypeError) chiqaradi:

```php
<?php
declare(strict_types=1);

function kvadrat(int $son): int {
    return $son * $son;
}

echo kvadrat("5");
// ❌ Fatal error: Uncaught TypeError: kvadrat(): Argument #1 ($son)
//    must be of type int, string given
```

Agar `declare(strict_types=1)` bo'lmaganida, PHP `"5"` ni jimgina `5` ga o'girib, `25` chiqarardi. Strict rejim esa: "Yo'q, men aniq int kutdim, matn bermang!" deydi — bu xatolarni erta tutib oladi.

> Maslahat: yangi loyihalarda har bir `.php` faylni `declare(strict_types=1);` bilan boshlash — professional standart. U sizni "type juggling tuzoqlari"dan himoya qiladi. Buni hozir to'liq tushunmasangiz ham xafa bo'lmang — funksiyalar mavzusiga (1.x) yetganda qaytamiz; hozircha "turlarni qat'iy qilish degan imkoniyat bor ekan" deb eslab qo'ying.

### Nima uchun tur muhim?

Chunki turli turdagi ma'lumotlar turlicha "muomala qiladi". Masalan, ikkita sonni qo'shsangiz — ular matematik qo'shiladi. Ikkita matnni esa "qo'shsangiz" — boshqacha natija bo'ladi:

```php
<?php
$a = 5;
$b = 3;
echo $a + $b;     // 8  (sonlar matematik qo'shildi)
```

Buni keyingi bo'limda — amallar mavzusida — batafsil ko'ramiz.

### Mashqlar

**Oson**
1. Har bir turga bittadan o'zgaruvchi yarating: matn, butun son, kasr son, mantiqiy qiymat.
2. Ularning har birini `var_dump` bilan tekshiring va natijani ko'ring.
3. `19` (son) va `"19"` (matn) ni alohida `var_dump` qiling — natijadagi farqni ko'ring.
4. Kasr sonni vergul bilan yozib ko'ring (`$x = 3,14;`) — xato chiqishini ko'ring, keyin nuqta bilan tuzating.
5. `1_000_000` raqamli ajratgich bilan bir o'zgaruvchi yarating va `var_dump` qiling — natijada `_` belgisi yo'qolganini ko'ring.

**O'rta**
6. Telefon raqamini saqlash uchun qaysi tur to'g'ri — matnmi yoki sonmi? O'z fikringizni izoh bilan yozing va shunday saqlang.
7. `$kirgan = true;` va `$kirgan = false;` larni alohida `var_dump` qiling.
8. Bitta o'zgaruvchiga avval matn, keyin son saqlang (`$x = "salom";` keyin `$x = 100;`), har safar `var_dump` qiling — turning o'zgarishini kuzating.
9. `"7" + 3` va `"7 ta" + 3` ni alohida `var_dump` qiling. Birinchisida natija nima, ikkinchisida qanday ogohlantirish chiqdi? Izohlang.
10. `0 == "abc"` va `0 === "abc"` natijalarini `var_dump` qiling. PHP 8 da birinchisi nima beradi? (Maslahat: bo'limdagi "PHP 8 da o'zgargan xulq" qismiga qarang.)
11. `(int) 19.99`, `(int) "42 yosh"`, `(string) false` larni `var_dump` qiling. Har birining natijasini oldindan taxmin qiling, keyin tekshiring.

**Qiyin**
12. Mahsulot haqida ma'lumotni turli o'zgaruvchilarda saqlang: nomi (matn), narxi (kasr son), soni (butun son), mavjudligi (mantiqiy). Hammasini chiqaring va `var_dump` bilan tekshiring.
13. Foydalanuvchi forma orqali `"25"` deb kiritdi (matn), deylik. Avval `is_numeric` bilan tekshiring, agar son bo'lsa — `(int)` ga o'giring va "Yosh: 25" deb chiqaring, aks holda "Xato" deb yozing.
14. `0.1 + 0.2` ni `0.3` bilan avval `==` orqali solishtiring (natija nima?), keyin `round(..., 2)` orqali to'g'ri solishtiring.
15. Quyidagi qiymatlarning **bool kontekstda** `true` mi yoki `false` ekanini oldindan taxmin qiling, keyin `(bool)` cast bilan tekshiring: `0`, `"0"`, `"0.0"`, `""`, `"false"`, `[]`, `[0]`.

<details markdown="1">
<summary>Yechim — 3</summary>

```php
<?php
var_dump(19);     // int(19)        → bu butun son
var_dump("19");   // string(2) "19" → bu matn, 2 ta belgidan iborat
```

Ko'rib turganingizdek, ekranda `19` bir xil ko'rinsa ham, kompyuter uchun ular **ikki xil narsa**: biri son (u bilan hisob qilish mumkin), ikkinchisi matn (ikkita belgi: "1" va "9"). Bu farqni tushunish keyinroq juda asqotadi.
</details>

<details markdown="1">
<summary>Yechim — 9 (type juggling va ogohlantirish)</summary>

```php
<?php
$a = "7" + 3;
var_dump($a);        // int(10)  → "7" avtomatik 7 soniga o'girildi

$b = "7 ta" + 3;
var_dump($b);
// Warning: A non-numeric value encountered ...
// int(10)  → "7 ta" dan faqat boshidagi 7 olindi
```

Birinchisida `"7"` toza son ko'rinishida bo'lgani uchun PHP uni jimgina 7 ga o'giradi — natija `10`. Ikkinchisida `"7 ta"` aralash matn, shuning uchun PHP boshidagi 7 ni oladi-yu, **ogohlantirish** chiqaradi: "men toza son kutgandim". Shuning uchun forma ma'lumotini qo'shishdan oldin `is_numeric` bilan tekshirish kerak.
</details>

<details markdown="1">
<summary>Yechim — 10 (PHP 8 da loose comparison)</summary>

```php
<?php
var_dump(0 == "abc");    // PHP 8: false  (eski PHP 7 da true edi!)
var_dump(0 === "abc");   // false  → turlar ham har xil
```

PHP 8 dan boshlab `0 == "abc"` natijasi `false`. Sababi: `"abc"` toza son emas, shuning uchun PHP endi **sonni matnga** o'giradi (`"0" == "abc"` → false), eski PHP 7 dagidek matnni 0 ga o'girmaydi. `===` esa har doim turni ham tekshirgani uchun `false` — bir tomon son, ikkinchisi matn.
</details>

<details markdown="1">
<summary>Yechim — 11 (aniq cast natijalari)</summary>

```php
<?php
var_dump((int) 19.99);      // int(19)    → kasr qismi KESILADI (20 emas!)
var_dump((int) "42 yosh");  // int(42)    → boshidagi son olinadi
var_dump((string) false);   // string(0) "" → bo'sh matn (false → "")
```

Uchta tez-tez adashtiradigan joy: (1) `(int)` yaxlitlamaydi, kasrni kesadi — `19.99` → `19`. Yaxlitlash kerak bo'lsa `round()`. (2) `(int) "42 yosh"` boshidagi raqamlarni oladi → `42`. (3) `(string) false` natijasi **bo'sh matn**, `"false"` degan so'z emas; `(string) true` esa `"1"`.
</details>

<details markdown="1">
<summary>Yechim — 12 (mahsulot ma'lumoti, har xil turlar)</summary>

```php
<?php
$nom = "Noutbuk";       // matn (string)
$narx = 7499.99;        // kasr son (float)
$soni = 3;              // butun son (int)
$mavjud = true;         // mantiqiy (bool)

echo "$nom — $narx so'm, $soni dona<br>";

var_dump($nom);     // string(7) "Noutbuk"
var_dump($narx);    // float(7499.99)
var_dump($soni);    // int(3)
var_dump($mavjud);  // bool(true)
```
Bitta mahsulot — to'rtta har xil turdagi ma'lumot. `var_dump` har birining turini aniq ko'rsatadi. E'tibor bering: `$narx` kasr bo'lgani uchun `float`, `$soni` butun bo'lgani uchun `int`.
</details>

<details markdown="1">
<summary>Yechim — 13 (forma ma'lumotini xavfsiz songa o'girish)</summary>

```php
<?php
$kiritilgan = "25";   // forma orqali kelgan, deylik (matn)

if (is_numeric($kiritilgan)) {
    $yosh = (int) $kiritilgan;   // endi xavfsiz songa o'giramiz
    echo "Yosh: $yosh\n";        // Yosh: 25
} else {
    echo "Xato: son kiriting!\n";
}
```

Forma orqali kelgan ma'lumot deyarli har doim **matn** bo'ladi. `is_numeric` bilan "bu songa o'girilishi mumkinmi?" deb tekshiramiz; faqat shundan keyin `(int)` ga o'giramiz. Bu type juggling tuzoqlaridan (masalan, "25 yosh" kabi aralash matn) himoya qiladi.
</details>

<details markdown="1">
<summary>Yechim — 14 (float aniqligi)</summary>

```php
<?php
$natija = 0.1 + 0.2;

// ❌ Noto'g'ri: to'g'ridan-to'g'ri solishtirish
var_dump($natija == 0.3);             // false (0.30000000000000004 != 0.3)

// ✅ To'g'ri: round bilan ma'lum aniqlikda solishtirish
var_dump(round($natija, 2) == 0.3);   // true
```

`0.1 + 0.2` aslida `0.30000000000000004` bo'ladi — bu kompyuterning kasr son saqlash usuli (hamma tillarda shunday). Shuning uchun kasrlarni `==` bilan solishtirmang; `round()` bilan kerakli xona aniqlikka yaxlitlab solishtiring.
</details>

<details markdown="1">
<summary>Yechim — 15 (bool kontekst)</summary>

```php
<?php
var_dump((bool) 0);        // false  → nol son
var_dump((bool) "0");      // false  → "0" matni (tuzoq!)
var_dump((bool) "0.0");    // true   → "0.0" matni bo'sh emas → true
var_dump((bool) "");       // false  → bo'sh matn
var_dump((bool) "false");  // true   → bu oddiy matn, bo'sh emas → true (tuzoq!)
var_dump((bool) []);       // false  → bo'sh massiv
var_dump((bool) [0]);      // true   → ichida 1 ta element bor
```

`false` ga o'giriladiganlar: `0`, `0.0`, `""`, `"0"`, `[]`, `null`. Diqqat: faqat `"0"` matni `false`; `"0.0"` va `"false"` esa `true`, chunki ular bo'sh emas. Massivda esa muhimi — **ichida element bormi yo'qmi**: `[0]` da bitta element bor, shuning uchun `true`.
</details>
