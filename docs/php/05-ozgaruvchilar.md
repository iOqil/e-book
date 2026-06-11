# 1.2 O'zgaruvchilar (variables)

[⬅️ Oldingi: 1.1 Kod qanday yoziladi (sintaksis)](./04-kod-qanday-yoziladi.md) · [🏠 README](./README.md) · [Keyingi: 1.3 Ma'lumot turlari ➡️](./06-malumot-turlari.md)

---

### O'zgaruvchi nima?

Tasavvur qiling, sizda bir nechta **qutilar** bor va har biriga nom yozib qo'ygansiz: "ism", "yosh", "narx". Har bir qutiga biror narsa solib qo'yasiz, keyin kerak bo'lganda qutining nomini aytib, ichidagini olasiz.

**O'zgaruvchi — aynan shunday "nomlangan quti".** Ichiga biror ma'lumot (matn, son) saqlaysiz, keyin nomi orqali ishlatasiz.

PHP'da o'zgaruvchi `$` belgisi bilan boshlanadi:

```php
<?php
$ism = "Ali";
$yosh = 19;

echo $ism;
echo "<br>";
echo $yosh;
```

Bu kod ekranga `Ali` va `19` chiqaradi.

Tushuntiramiz:
- **`$ism`** — bu o'zgaruvchi. `$` belgisidan keyin nom keladi (`ism`).
- **`=`** — bu "tenglik" emas, balki "**saqlash**" belgisi. `$ism = "Ali"` degani: "`Ali` degan matnni `ism` qutisiga sol".
- Keyin `echo $ism` deganimizda — quti ichidagi narsa (`Ali`) ekranga chiqadi.

> **Muhim:** `$ism = "Ali"` — bu "ism Ali'ga teng" degani EMAS. Bu "Ali'ni ism qutisiga joyla" degani. Chapdagi quti, o'ngdagi unga solinadigan narsa. Yo'nalish — o'ngdan chapga.

### Nega "o'zgaruvchi" deyiladi?

Chunki ichidagi narsani **o'zgartirish** mumkin:

```php
<?php
$narx = 1000;
echo $narx;        // 1000 chiqadi
echo "<br>";

$narx = 5000;      // endi qutiga yangi qiymat solindi
echo $narx;        // 5000 chiqadi
```

Quti bitta, lekin ichidagi narsa o'zgardi. Oxirgi solingan qiymat saqlanadi.

### Konstanta — o'zgarmas "quti"

Ba'zan qutiga biror narsa solib qo'yib, uni **butun dastur davomida o'zgartirmaslik** kerak bo'ladi. Masalan, PI soni (3.14159), soliq foizi, sayt nomi yoki admin elektron pochtasi — bular dastur boshidan oxirigacha bir xil bo'lib qoladi. Bunday "o'zgarmas qiymat" uchun **konstanta** (constant) ishlatiladi.

Konstanta — bu "muhrlangan quti": ichiga bir marta qiymat solasiz, keyin uni **hech qachon** o'zgartira olmaysiz. Agar adashib o'zgartirishga urinsangiz, PHP xato beradi. Bu — siz uchun himoya: muhim qiymatni xatolik bilan buzib qo'ymaysiz.

Konstanta yaratishning eng zamonaviy va sodda yo'li — `const` so'zi:

```php
<?php
const PI = 3.14159;
const SAYT_NOMI = "MeningSaytim";

echo PI;          // 3.14159
echo "\n";
echo SAYT_NOMI;   // MeningSaytim
```

> **Diqqat:** konstanta nomi oldida `$` belgisi **YO'Q**. `$narx` — o'zgaruvchi; `PI` — konstanta. Va konstantani chaqirganda ham `$` qo'yilmaydi: `echo PI;` (`echo $PI;` emas).

Endi uni o'zgartirib ko'raylik — bu **ishlamaydi**:

```php
<?php
const PI = 3.14;
// PI = 3.15;   // ❌ XATO — konstanta o'zgarmas

echo PI;   // 3.14
```

Mana shu "o'zgartirib bo'lmaslik" — konstantaning butun mohiyati. O'zgaruvchidan farqi shu: o'zgaruvchiga istalgancha yangi qiymat solib turish mumkin, konstantaga esa — faqat bir marta.

### `const` va `define` — ikkita yo'l

Konstanta yaratishning **ikki** yo'li bor: yangi `const` va eski `define()`.

`define()` — funksiya ko'rinishidagi usul. Birinchi qavsga konstanta nomini **matn** (qo'shtirnoq ichida) sifatida, ikkinchisiga qiymatini berasiz:

```php
<?php
define('SOLIQ', 12);
define('VALYUTA', "so'm");

$narx = 5000;
$soliqMiqdori = $narx * SOLIQ / 100;

echo "Soliq: " . $soliqMiqdori . " " . VALYUTA;   // Soliq: 600 so'm
```

Ikkalasi ham bir xil natija beradi. Farqi nimada?

| | `const PI = 3.14` | `define('PI', 3.14)` |
|---|---|---|
| Qachon yaratiladi | **kompilyatsiya** paytida (dastur o'qilayotganda) | **ish vaqtida** (kod shu qatorga yetganda) |
| Class ichida ishlatish | **mumkin** | mumkin emas |
| `if` ichida shartli yaratish | mumkin emas | **mumkin** |
| Tezligi | biroz tezroq | biroz sekinroq |
| Yozilishi | qisqaroq, toza | uzunroq |

Sodda qoida: **odatda `const` ishlating** — u qisqaroq, tezroq va zamonaviyroq. `define()` esa faqat alohida holatlarda kerak bo'ladi — masalan, konstantani biror shartga qarab (`if` ichida) yaratmoqchi bo'lsangiz. `const` buni qila olmaydi, `define()` esa qiladi.

### Konstanta nomlash konvensiyasi

O'zgaruvchilarni `$talabaIsmi` ko'rinishida yozgan edik. Konstantalar uchun esa boshqa, **maxsus** uslub bor: butun nom **KATTA HARF** bilan, so'zlar orasida `_` (pastki chiziq):

```php
<?php
const MAX_URINISH = 3;
const MIN_PAROL_UZUNLIGI = 8;
const ADMIN_EMAIL = "admin@sayt.uz";

echo MAX_URINISH . "\n";          // 3
echo MIN_PAROL_UZUNLIGI . "\n";   // 8
echo ADMIN_EMAIL;                 // admin@sayt.uz
```

Bu shunchaki "go'zallik" uchun emas — bu **kelishuv** (konvensiya). Kodni o'qiyotgan har qanday dasturchi `MAX_URINISH` ni ko'rib, darrov "bu konstanta, o'zgarmas qiymat" deb tushunadi. `$maxUrinish` ko'rsa esa "bu o'zgaruvchi, o'zgarishi mumkin" deb biladi. KATTA HARF — konstanta uchun butun dunyo dasturchilari uchun "imzo".

> **Foydasi:** "sehrli sonlar"ni konstantaga aylantiring. Kodingizda `12` (soliq foizi) bir necha joyda uchrasa, ertaga foiz o'zgarganda hamma joyni qidirib yurmaysiz — faqat `const SOLIQ = 12;` ni bir joyda o'zgartirasiz, qolgani avtomatik yangilanadi.

### Class konstantasi — qisqa eslatma

Konstantani **class** (sinf) ichida ham e'lon qilish mumkin. Class va obyektlarni keyinroq (1.14) chuqur o'rganamiz, hozircha shunchaki ko'rib qo'ying — class ichida `const` o'sha classga "tegishli" o'zgarmas qiymatni bildiradi:

```php
<?php
class Aylana
{
    const PI = 3.14159;

    public function yuza(float $radius): float
    {
        return self::PI * $radius * $radius;
    }
}

$a = new Aylana();
echo $a->yuza(5);          // 78.53975
echo "\n";
echo Aylana::PI;           // 3.14159  (tashqaridan ham)
```

Bu yerda ikki yangilik bor: class ichida `self::PI` orqali, tashqarida esa `Aylana::PI` (class nomi + `::` + konstanta nomi) orqali murojaat qilinadi. Hozircha tafsilotga kirmaymiz — shuni eslab qoling: konstantalar nafaqat "yalang'och" kodda, balki classlar ichida ham yashashi mumkin.

### O'zgaruvchini matn bilan birga chiqarish

Ko'pincha o'zgaruvchini matn bilan aralashtirib chiqarish kerak bo'ladi. Buning ikki yo'li bor.

**1-yo'l: nuqta bilan ulash.** PHP'da `.` (nuqta) ikkita narsani bir-biriga ulaydi:

```php
<?php
$ism = "Ali";
echo "Salom, " . $ism . "!";   // Salom, Ali!
```

**2-yo'l: o'zgaruvchini to'g'ridan-to'g'ri qo'shtirnoq ichiga yozish:**

```php
<?php
$ism = "Ali";
echo "Salom, $ism!";   // Salom, Ali!
```

Ikkala usul ham `Salom, Ali!` chiqaradi. Boshida sizga qulayrog'ini tanlang.

> **Diqqat:** o'zgaruvchini qo'shtirnoq (`" "`) ichida yozsangiz, uning qiymati chiqadi. Lekin **bittalik tirnoq** (`' '`) ichida yozsangiz, o'zgaruvchi qiymati EMAS, balki nomi xuddi o'zidek chiqadi:
> ```php
> $ism = "Ali";
> echo "Salom $ism";   // Salom Ali
> echo 'Salom $ism';   // Salom $ism  (qiymat chiqmadi!)
> ```
> Shuning uchun o'zgaruvchini chiqarganda **qo'shtirnoq** ishlating.

### Jingalak qavsli interpolatsiya — `{$massiv['kalit']}`

Oddiy `"$ism"` usuli oddiy o'zgaruvchilar uchun ajoyib ishlaydi. Lekin ba'zan o'zgaruvchi "murakkabroq" bo'ladi — masalan, massivning bir elementi (`$massiv['kalit']`) yoki obyektning xususiyati (`$obj->ism`). Bunday paytda PHP qayerda o'zgaruvchi tugaganini aniq bilolmay qoladi. Yechim — o'zgaruvchini **jingalak qavs** `{ }` ichiga olish.

(Massivlar 1.8'da, obyektlar 1.14'da batafsil; hozircha sintaksisni ko'rib qo'ying — keyin ko'p kerak bo'ladi.)

Massiv elementi bilan:

```php
<?php
$foydalanuvchi = [
    'ism' => "Ali",
    'shahar' => "Toshkent",
];

// Jingalak qavs PHP'ga "mana shu yer bitta o'zgaruvchi" deb aniq ko'rsatadi:
echo "Salom, {$foydalanuvchi['ism']}! Siz {$foydalanuvchi['shahar']}danmisiz?";
// Salom, Ali! Siz Toshkentdanmisiz?
```

Nega aynan jingalak qavs kerak? Quyidagiga qarang — qavssiz yozish chalkashlik (yoki xato) keltirib chiqaradi:

```php
<?php
$narxlar = ['olma' => 5000, 'anor' => 12000];

// Jingalak qavssiz — PHP tirnoq ichidagi 'olma' ni tushunolmaydi:
// echo "Olma narxi: $narxlar['olma']";   // ❌ Parse error

// Jingalak qavs bilan — to'g'ri ishlaydi:
echo "Olma narxi: {$narxlar['olma']} so'm";   // Olma narxi: 5000 so'm
```

Obyekt xususiyati bilan ham xuddi shunday — `{$obj->xususiyat}`:

```php
<?php
class Talaba
{
    public function __construct(
        public string $ism,
        public int $yosh,
    ) {}
}

$talaba = new Talaba("Ali", 19);

echo "Talaba: {$talaba->ism}, yoshi: {$talaba->yosh}";
// Talaba: Ali, yoshi: 19
```

> **Oddiy qoida:** o'zgaruvchi "yalang'och" bo'lsa (`$ism`), oddiy `"$ism"` yetadi. O'zgaruvchida qavs (`[...]`) yoki o'q (`->`) bo'lsa — jingalak qavs `{...}` ichiga oling. Ko'p tajribali dasturchilar **doim** `{$...}` yozadi — chunki u har doim ishlaydi va kod tozaroq ko'rinadi.

### O'zgaruvchiga nom berish qoidalari

- `$` bilan boshlanadi: `$ism`, `$narx`.
- Faqat harf, raqam va `_` (pastki chiziq) ishlatiladi. Bo'sh joy bo'lmaydi.
- Nom raqam bilan boshlanmaydi: `$1ism` — xato; `$ism1` — to'g'ri.
- **Mazmunli nom bering:** `$narx` deb yozing, `$n` yoki `$x` emas. Keyinroq kodni o'qiganingizda nima saqlanganini darrov tushunasiz.
- Bir nechta so'zli nomda odatda shunday yoziladi: `$talabaIsmi` yoki `$talaba_ismi`.

### O'zgaruvchi qamrovi (scope) — boshlovchi tuzog'i

Endi muhim bir narsani aytamiz — bu boshlovchilar ko'p "kaltaklanadigan" mavzu. (Funksiyalarni 1.9'da batafsil o'rganasiz; hozircha shu qoidani bilib qo'ying, keyin ishingizni osonlashtiradi.)

**Funksiya ichida yaratilgan o'zgaruvchi — faqat o'sha funksiya ichida yashaydi.** Funksiya tugashi bilan, u o'zgaruvchi ham "yo'qoladi". Tashqaridan unga murojaat qilolmaysiz:

```php
<?php
function salomBer(): void
{
    $xabar = "Salom!";   // bu o'zgaruvchi faqat funksiya ICHIDA yashaydi
    echo $xabar;
}

salomBer();   // Salom!

// echo $xabar;   // ❌ XATO — $xabar bu yerda mavjud emas (Undefined variable)
```

Buni "har bir funksiya — alohida xona" deb tasavvur qiling. Xona ichida yaratgan narsangiz tashqariga chiqmaydi. Va aksincha ham to'g'ri — **tashqaridagi o'zgaruvchi funksiya ichida ham ko'rinmaydi**:

```php
<?php
$soni = 10;   // tashqaridagi o'zgaruvchi

function korsat(): void
{
    // echo $soni;   // ❌ XATO — funksiya tashqaridagi $soni ni KO'RMAYDI
    echo "Funksiya ichidaman";
}

korsat();      // Funksiya ichidaman
echo "\n";
echo $soni;    // 10  (bu yerda esa ko'rinadi)
```

Bu xatolik emas, balki **maxsus qulaylik**. Tasavvur qiling, katta dasturda 100 ta funksiya bor, har birida `$i` degan o'zgaruvchi bor. Agar ular bir-biriga aralashib ketsa — tartibsizlik bo'lardi. "Har bir funksiya alohida xona" qoidasi tufayli ular bir-biriga xalal bermaydi.

Unda funksiyaga tashqaridan ma'lumot qanday beriladi? **Parametr** orqali — qiymatni "xonaning eshigidan" uzatasiz, funksiya esa natijani `return` bilan "qaytarib beradi":

```php
<?php
$soni = 10;

function ikkilantir(int $qiymat): int
{
    return $qiymat * 2;   // tashqaridan PARAMETR sifatida olamiz
}

echo ikkilantir($soni);   // 20
```

Bu yerda `$soni` ni to'g'ridan-to'g'ri funksiya ichida ishlatmadik — uni `ikkilantir($soni)` orqali **parametr** sifatida uzatdik. Funksiya esa natijani `return` bilan tashqariga qaytardi. Bu — "toza" usul. Parametr va `return` haqida 1.9'da to'liq gaplashamiz; hozircha shu tuzoqni bilib qo'ying: funksiya ichi va tashqarisi — ikki alohida dunyo.

### Mashqlar

**Oson**
1. `$ism` o'zgaruvchisiga o'z ismingizni saqlang va ekranga chiqaring.
2. `$shahar` o'zgaruvchisiga shaharingizni saqlang va `"Men ... da yashayman"` shaklida chiqaring.
3. `$narx` o'zgaruvchisiga `2000` saqlang, chiqaring, keyin `3500` saqlab qayta chiqaring.
4. Ikkita o'zgaruvchi (`$ism`, `$yosh`) yarating va ikkalasini bitta gap ichida chiqaring.
5. `const PI = 3.14159;` konstantasini yarating va ekranga chiqaring (`echo PI;`). Konstanta nomi oldida `$` yo'qligiga e'tibor bering.

**O'rta**
6. `$ism` va `$familiya` o'zgaruvchilarini yarating, ularni bo'sh joy bilan ulab, to'liq ismni chiqaring.
7. Bir o'zgaruvchini qo'shtirnoq ichida (`"$ism"`) va bittalik tirnoq ichida (`'$ism'`) chiqaring — farqini ko'ring.
8. `$mahsulot` va `$narx` o'zgaruvchilari bilan: `"Olma narxi: 5000 so'm"` shaklida chiqaring.
9. `const PI = 3.14159;` dan foydalanib, radiusi `5` bo'lgan aylananing uzunligi (`2 * PI * radius`) va yuzasini (`PI * radius * radius`) hisoblab chiqaring.
10. `define('SOLIQ', 12)` konstantasini yarating. Narxi `50000` bo'lgan mahsulotning 12% solig'ini va soliq bilan jami narxini hisoblang.
11. Massiv yarating: `$mahsulot = ['nom' => "Olma", 'narx' => 5000, 'soni' => 3];`. So'ng jingalak qavsli interpolatsiya (`{$mahsulot['nom']}`) bilan ma'lumotlarni chiroyli chiqaring va jami narxni hisoblang.

**Qiyin**
12. To'liq tashrifnoma yarating: `$ism`, `$kasb`, `$telefon`, `$shahar` o'zgaruvchilari bilan, har birini alohida qatorda (`<br>` bilan) chiroyli chiqaring.
13. Ikkita o'zgaruvchi qiymatini bir-biriga almashtiring (`$a` da turgan narsa `$b` ga, `$b` dagi `$a` ga o'tsin). Buning uchun uchinchi vaqtinchalik o'zgaruvchi kerak bo'lishi mumkin — o'ylab ko'ring.
14. `class Doira` yarating: ichida `const PI` konstantasi, `$radius` xususiyati va `yuza()` metodi bo'lsin. Radiusi `10` bo'lgan doira yaratib, yuzasini hisoblang (`PI * radius * radius`). Natijani interpolatsiya bilan chiqaring.

<details markdown="1">
<summary>Yechim — 6</summary>

```php
<?php
$ism = "Ali";
$familiya = "Valiyev";
echo $ism . " " . $familiya;   // Ali Valiyev
```
Bu yerda `.` belgisi ism, bo'sh joy (`" "`) va familiyani birlashtiradi.
</details>

<details markdown="1">
<summary>Yechim — 9 (PI bilan aylana)</summary>

```php
<?php
const PI = 3.14159;

$radius = 5;
$aylanaUzunligi = 2 * PI * $radius;
$yuza = PI * $radius * $radius;

echo "Aylana uzunligi: $aylanaUzunligi\n";   // 31.4159
echo "Yuza: $yuza";                           // 78.53975
```
Konstanta `PI` ni o'zgaruvchi kabi `$` siz ishlatishga e'tibor bering. Uni butun dastur davomida xavfsiz qayta ishlatamiz — o'zgartirib qo'yish xavfi yo'q.
</details>

<details markdown="1">
<summary>Yechim — 10 (soliq hisoblash)</summary>

```php
<?php
define('SOLIQ', 12);

$narx = 50000;
$soliqMiqdori = $narx * SOLIQ / 100;
$jami = $narx + $soliqMiqdori;

echo "Narx: $narx so'm\n";                // Narx: 50000 so'm
echo "Soliq (12%): $soliqMiqdori so'm\n"; // Soliq (12%): 6000 so'm
echo "Jami: $jami so'm";                  // Jami: 56000 so'm
```
`SOLIQ` ni konstanta qildik, chunki soliq foizi dastur davomida o'zgarmaydi. Ertaga foiz o'zgarsa — faqat bir joyni (`define`) tahrirlaysiz.
</details>

<details markdown="1">
<summary>Yechim — 11 (jingalak qavsli interpolatsiya)</summary>

```php
<?php
$mahsulot = [
    'nom' => "Olma",
    'narx' => 5000,
    'soni' => 3,
];

echo "Mahsulot: {$mahsulot['nom']}\n";
echo "Narxi: {$mahsulot['narx']} so'm\n";
echo "Soni: {$mahsulot['soni']} dona\n";
echo "Jami: " . ($mahsulot['narx'] * $mahsulot['soni']) . " so'm";
```
Massiv elementini matn ichida chiqarish uchun **jingalak qavs** `{...}` shart. Qavssiz `"$mahsulot['nom']"` xato berardi.
</details>

<details markdown="1">
<summary>Yechim — 12 (to'liq tashrifnoma)</summary>

```php
<?php
$ism = "Ali Valiyev";
$kasb = "Dasturchi";
$telefon = "+998 90 123 45 67";
$shahar = "Toshkent";

echo "Ism: $ism<br>";
echo "Kasb: $kasb<br>";
echo "Telefon: $telefon<br>";
echo "Shahar: $shahar";
```
Bu yerda har bir ma'lumot o'zgaruvchida saqlanadi va qo'shtirnoq ichida `$ism` ko'rinishida chiqariladi (1.2'dagi interpolatsiya). Avvalgi mashqdagi "qotirilgan" matndan farqi — endi qiymatni bir joyda o'zgartirsak, hamma joyda yangilanadi.
</details>

<details markdown="1">
<summary>Yechim — 13 (qiymatlarni almashtirish)</summary>

```php
<?php
$a = "olma";
$b = "anor";

// To'g'ridan-to'g'ri $a = $b qilsak, $a dagi "olma" yo'qoladi.
// Shuning uchun avval vaqtinchalik qutiga saqlaymiz:
$vaqtinchalik = $a;   // "olma" ni saqlab qo'ydik
$a = $b;              // endi $a = "anor"
$b = $vaqtinchalik;   // $b = "olma"

echo $a;   // anor
echo "<br>";
echo $b;   // olma
```
Bu — boshlovchilar uchun klassik mashq. "Uchinchi quti" hiylasini tushunish muhim.
</details>

<details markdown="1">
<summary>Yechim — 14 (class konstantasi)</summary>

```php
<?php
class Doira
{
    const PI = 3.14159;

    public function __construct(
        public float $radius,
    ) {}

    public function yuza(): float
    {
        return self::PI * $this->radius ** 2;
    }
}

$d = new Doira(10);
echo "Radius: {$d->radius}\n";   // Radius: 10
echo "Yuza: {$d->yuza()}";       // Yuza: 314.159
```
Bu yerda uch yangilik bir joyda: class ichidagi konstanta (`self::PI`), zamonaviy konstruktor (`public float $radius`) va jingalak qavsli interpolatsiya (`{$d->radius}`). Class va konstruktor haqida 1.14–1.15'da batafsil o'rganasiz — hozircha shunchaki ishlatib ko'ring.
</details>
