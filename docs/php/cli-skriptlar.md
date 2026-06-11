# 1.14 CLI — terminal skriptlari

[⬅️ Oldingi: 1.13 Generatorlar va iteratorlar](./generatorlar.md) · [🏠 README](./README.md) · [Keyingi: 2.1 Class va obyekt — eng asosiy tushuncha ➡️](./14-class-va-obyekt-eng-asosiy-tushuncha.md)

---

Shu paytgacha yozgan PHP kodlaringizning aksariyati brauzer va veb-server (Apache yoki Nginx) bilan birga ishladi: foydalanuvchi saytga kiradi, server PHP'ni ishga tushiradi, natija HTML bo'lib brauzerga qaytadi. Lekin PHP'ning hayoti faqat brauzerdan iborat emas.

Tasavvur qiling: bazada 100 000 ta eski yozuvni yangi formatga ko'chirish kerak (migratsiya). Yoki har kechasi soat 3:00 da hisobot tayyorlab, uni emailga jo'natish kerak (cron vazifa). Yoki mijoz sizga 50 000 qatorli CSV fayl berdi — uni bazaga import qilish kerak. Bunaqa vazifalar uchun brauzer ham, foydalanuvchi ham kerak emas — kod terminalda (komanda qatorida) o'zi ishlashi kerak. Ana shunaqa skriptlarni **CLI** (Command-Line Interface — komanda qatori interfeysi) skriptlari deyiladi.

Bu bobda PHP'ni brauzersiz, to'g'ridan-to'g'ri terminalda ishlatishni o'rganamiz: parametr qabul qilish, foydalanuvchidan so'rash, fayllarni qayta ishlash va tayyor vositalar (tool) yozish. Bu — "haqiqiy" dasturchining kundalik ishi.

### CLI nima va nega kerak?

**CLI** — bu grafik interfeyssiz (tugma, oyna yo'q), faqat matn orqali ishlaydigan dastur. Siz terminalga buyruq yozasiz, dastur matn bilan javob beradi.

Nega CLI skriptlar kerak? Bir nechta sabab:

- **Tezlik:** brauzer va HTML ortiqcha yuk. Faqat ish bajarish kerak bo'lsa, CLI tezroq.
- **Avtomatlashtirish:** cron (jadval bo'yicha ishga tushiruvchi) faqat terminal buyruqlarini biladi, brauzerni ocha olmaydi.
- **Vaqt cheklovi yo'q:** veb-so'rovda PHP odatda 30 soniyada to'xtaydi. CLI'da bu cheklov yo'q — soatlab ishlashi mumkin (katta migratsiya).
- **Bir martalik vazifalar:** seed (bazaga test ma'lumot to'ldirish), import/export, tozalash skriptlari.

Qisqasi: foydalanuvchi ko'rmaydigan, "orqa tomonda" bajariladigan har qanday ish CLI uchun.

### Birinchi CLI skript — `php fayl.php`

Brauzer kerak emas. Oddiy `.php` fayl yozasiz va uni terminalda `php` buyrug'i bilan ishga tushirasiz.

`salom.php` faylini yarating:

```php
<?php

echo "Salom, terminal!\n";
echo "Bugun ajoyib kun.\n";
```

Endi terminalda (papkada turib) ishga tushiring:

```
php salom.php
```

Natija:

```
Salom, terminal!
Bugun ajoyib kun.
```

Hammasi shu. `<?php` ochiladi, `echo` to'g'ridan-to'g'ri terminal ekraniga yozadi. Bu yerda HTML ham, `<br>` ham yo'q — chunki terminal HTML tushunmaydi. Yangi qatorga o'tish uchun `\n` ishlatiladi (`<br>` emas!).

PHP qaysi versiyada ekanini ko'rish uchun:

```
php -v
```

Natija (taxminan):

```
PHP 8.4.0 (cli) (built: ...)
```

Mana shu **(cli)** so'zi muhim — u PHP'ning terminal (CLI) rejimida ishlayotganini bildiradi.

### CLI va veb farqi — SAPI

PHP bir xil til, lekin u **qayerda** ishga tushganiga qarab biroz boshqacha tutadi. PHP'ning shu "ishlash muhiti" — **SAPI** (Server API) deyiladi. Eng ko'p uchraydigani ikkitasi:

- **`cli`** — terminalda (`php fayl.php`).
- **`apache2handler`** yoki **`fpm-fcgi`** — veb-serverda (brauzer orqali).

Kod ichida o'zingiz qaysi muhitda ekaningizni bilib olish mumkin — `PHP_SAPI` konstantasi orqali:

```php
<?php

if (PHP_SAPI === 'cli') {
    echo "Bu terminalda ishlayapti.\n";
} else {
    echo "Bu brauzerda (veb-serverda) ishlayapti.<br>";
}
```

Terminalda ishga tushirsangiz — birinchi xabar chiqadi. Bu, masalan, bitta faylni ham brauzerda, ham terminalda ishlatib, joyiga qarab boshqacha javob berish kerak bo'lganda asqotadi.

CLI rejimida yana bir muhim farq: `\n` chinakam yangi qator beradi (HTML'dagi `<br>` ishlamaydi), va chiqish darhol ekranga boradi — buferlanmaydi.

### Komanda qatori parametrlari — `$argv` va `$argc`

Skriptga tashqaridan ma'lumot berishning eng oddiy yo'li — uni ishga tushirayotganda yoniga so'z (argument) qo'shish:

```
php salom.php Ali Vali
```

Bu so'zlar (`Ali`, `Vali`) skript ichida ikkita maxsus o'zgaruvchida bo'ladi:

- **`$argv`** (argument vector) — barcha argumentlar massivi.
- **`$argc`** (argument count) — argumentlar soni.

```php
<?php

echo "Argumentlar soni: $argc\n";

foreach ($argv as $indeks => $qiymat) {
    echo "$indeks => $qiymat\n";
}
```

`php salom.php Ali Vali` bilan ishga tushirsangiz:

```
Argumentlar soni: 3
0 => salom.php
1 => Ali
2 => Vali
```

**Diqqat:** `$argv[0]` — bu doim **fayl nomining o'zi** (`salom.php`). Sizning haqiqiy argumentlaringiz `$argv[1]` dan boshlanadi. Shuning uchun `$argc` ham 3 chiqdi: fayl nomi + 2 ta so'z.

Real foydalanish — birinchi argumentni ism sifatida olamiz:

```php
<?php

$ism = $argv[1] ?? 'mehmon';   // agar argument berilmasa, "mehmon"

echo "Salom, $ism!\n";
```

`$argv[1] ?? 'mehmon'` — bu **null coalescing** (`??`) operatori: agar `$argv[1]` mavjud bo'lsa — uni ol, bo'lmasa — `'mehmon'`. Bu argument berilmagan holatni chiroyli hal qiladi (xato chiqmaydi).

```
php salom.php Olim     →  Salom, Olim!
php salom.php          →  Salom, mehmon!
```

### Argumentdan sonni olish — tip masalasi

Muhim nozik nuqta: `$argv` ichidagi **hamma narsa matn** (string). `php hisobla.php 5 3` desangiz, `$argv[1]` — bu `"5"` (matn), `5` (son) emas. Matematik amal qilishdan oldin songa aylantirish kerak:

```php
<?php

$a = (int) ($argv[1] ?? 0);   // matnni butun songa aylantiramiz
$b = (int) ($argv[2] ?? 0);

echo $a + $b . "\n";
```

```
php hisobla.php 5 3     →  8
```

Agar `(int)` qo'ymasangiz, `"5" + "3"` PHP'da baribir 8 chiqadi (PHP matnni avtomatik songa aylantiradi), lekin `"5" . "3"` (nuqta — ulash) `"53"` beradi. Shuning uchun aniqlik kerak bo'lsa, tipni o'zingiz boshqaring — `(int)` yoki `(float)` bilan.

### Nomli flaglar — `getopt`

`$argv` oddiy, lekin chalkash: `php tool.php Ali 25 erkak` — bu sonlar nimani anglatadi? Yoshi? Tartibi? Esda tutish qiyin. Shuning uchun professional CLI vositalar **nomli flag** (belgili parametr) ishlatadi: `--name=Ali --age=25`. Mana shu nomli flaglarni o'qish uchun PHP'da tayyor funksiya bor — **`getopt`**.

`getopt` ikki xil flagni tushunadi:

- **qisqa** flag: bitta harf, bitta chiziq — `-n Ali`
- **uzun** flag: to'liq so'z, ikkita chiziq — `--name=Ali`

```php
<?php

// "n:" -> -n flagi qiymat oladi (: belgisi "qiymat kerak" demak)
// ["name:"] -> --name flagi qiymat oladi
$flaglar = getopt('n:', ['name:']);

var_dump($flaglar);
```

```
php tool.php -n Ali
```

natija:

```
array(1) {
  ["n"]=>
  string(3) "Ali"
}
```

Ikki tomonlama — qisqa **yoki** uzun nom bilan ishlaydigan vosita:

```php
<?php

$flaglar = getopt('n:', ['name:']);

// -n yoki --name dan qaysi berilgan bo'lsa, o'shani olamiz
$ism = $flaglar['n'] ?? $flaglar['name'] ?? null;

if ($ism === null) {
    echo "Xato: ismni bering. Masalan: --name=Ali\n";
    exit(1);   // 1 — xato bilan tugadi (pastda tushuntiramiz)
}

echo "Salom, $ism!\n";
```

```
php tool.php --name=Olim   →  Salom, Olim!
php tool.php -n Olim        →  Salom, Olim!
php tool.php                →  Xato: ismni bering...
```

`getopt('n:', ['name:'])` ichidagi belgilarni eslab qoling:

- `'n:'` — `n` qisqa flag, oxiridagi `:` — "qiymat kerak" (`-n Ali`).
- `'n'` (ikki nuqtasiz) — qiymat kerak emas, faqat bor/yo'q flag (`-v` kabi).
- `['name:']` — uzun flaglar massivda yoziladi, `:` yana "qiymat kerak" degani.

Qiymatsiz (toggle) flag — masalan `--verbose` (batafsil chiqarish rejimi):

```php
<?php

// "v" oxirida : yo'q -> qiymatsiz flag (bor yoki yo'q)
$flaglar = getopt('v', ['verbose']);

$batafsil = isset($flaglar['v']) || isset($flaglar['verbose']);

if ($batafsil) {
    echo "Batafsil rejim yoqildi.\n";
} else {
    echo "Oddiy rejim.\n";
}
```

```
php tool.php -v          →  Batafsil rejim yoqildi.
php tool.php --verbose   →  Batafsil rejim yoqildi.
php tool.php             →  Oddiy rejim.
```

### Foydalanuvchidan so'rash — `fgets(STDIN)`

Ba'zan skript ishlash payti foydalanuvchidan biror narsa **so'rashi** kerak: "Ismingiz?", "Rostdan o'chirilsinmi? (ha/yo'q)". Buning uchun PHP'da **`STDIN`** ("standard input" — standart kirish kanali, ya'ni klaviatura) bor. Undan o'qish uchun `fgets` funksiyasidan foydalanamiz:

```php
<?php

echo "Ismingiz nima? ";
$javob = fgets(STDIN);   // foydalanuvchi yozguncha kutadi

$ism = trim($javob);     // oxiridagi "\n" (Enter) ni olib tashlaymiz

echo "Tanishganimdan xursandman, $ism!\n";
```

Ishga tushirilganda:

```
Ismingiz nima? Olim
Tanishganimdan xursandman, Olim!
```

**Muhim nuqta:** `fgets(STDIN)` foydalanuvchi bosgan **Enter** (`\n`) belgisini ham qaytaradi. Shuning uchun deyarli har doim `trim()` bilan tozalash kerak — aks holda `$ism` ichida yashirin `\n` qoladi va keyingi taqqoslashlar buziladi.

Ha/yo'q tasdiq so'rash — ko'p uchraydigan naqsh:

```php
<?php

echo "Hamma ma'lumot o'chirilsinmi? (ha/yo'q): ";
$javob = trim(fgets(STDIN));

if (strtolower($javob) === 'ha') {
    echo "O'chirildi.\n";
} else {
    echo "Bekor qilindi.\n";
}
```

`strtolower` bilan kichik harfga o'tkazamiz — shunda `Ha`, `HA`, `ha` — hammasi bir xil qabul qilinadi.

### `readline` — qulayroq so'rash

`echo` + `fgets(STDIN)` juftligini bitta funksiyaga jamlash mumkin — **`readline`**. U savolni chiqaradi va javobni qaytaradi (oxirida `\n` ham bo'lmaydi — o'zi tozalaydi):

```php
<?php

$ism = readline("Ismingiz: ");
$shahar = readline("Shahringiz: ");

echo "Siz — $ism, $shahar shahridan.\n";
```

```
Ismingiz: Olim
Shahringiz: Toshkent
Siz — Olim, Toshkent shahridan.
```

`readline` qulayroq, lekin **muhim ogohlantirish:** u hamma joyda ishlamaydi. `readline` alohida kengaytmaga (extension) bog'liq va Windows'dagi standart PHP'da odatda **yo'q** — u yerda `readline()` ni chaqirsangiz "undefined function" xatosi chiqadi. `fgets(STDIN)` esa **doim, hamma tizimda** ishlaydi.

Shuning uchun ko'chma (portable — har tizimda ishlaydigan) kod yozish uchun o'zimizning kichik so'rash yordamchimizni yozamiz — u `readline` bor bo'lsa undan, bo'lmasa `fgets(STDIN)` dan foydalanadi:

```php
<?php

function sora(string $savol): string
{
    // readline bor bo'lsa — undan (qulayroq), aks holda fgets(STDIN)
    if (function_exists('readline')) {
        return trim((string) readline($savol));
    }

    echo $savol;
    return trim((string) fgets(STDIN));
}

$ism = sora("Ismingiz: ");
echo "Salom, $ism!\n";
```

Bu `sora` funksiyasi — universal yechim. Quyidagi real misollarda aynan shuni ishlatamiz.

### To'g'ri yangi qator — `PHP_EOL`

Biz `\n` ishlatdik. Bu Linux va macOS'da to'g'ri ishlaydi. Lekin Windows'da yangi qator boshqacha — `\r\n`. Har xil tizimda bir xil to'g'ri ishlashi uchun PHP'da maxsus konstanta bor — **`PHP_EOL`** (End Of Line — qator oxiri). U qaysi tizimda ekaningizga qarab to'g'ri belgini beradi:

```php
<?php

echo "Birinchi qator" . PHP_EOL;
echo "Ikkinchi qator" . PHP_EOL;
```

Ko'p hollarda oddiy skriptlarda `\n` ham yetarli (zamonaviy terminallar `\n` ni tushunadi). Lekin fayl yozayotganda yoki har xil tizimda ishlaydigan jiddiy vosita yozayotganda — **`PHP_EOL`** ni ishlatish to'g'riroq. Bu — "har tizimda bir xil ishlasin" degan kafolat.

### Skript natijasi — `exit` va chiqish kodlari

Terminal dasturi tugaganda **chiqish kodi** (exit code) qaytaradi — bu butun son boshqa dasturlarga "ish qanday tugadi?" deb xabar beradi:

- **`0`** — hammasi muvaffaqiyatli (kelishuv: nol = yaxshi).
- **`0` dan boshqa** (1, 2, ...) — xato bo'ldi.

Bu cron va boshqa skriptlar uchun juda muhim: ular sizning skriptingiz **0** qaytarsa — "ish bitdi", boshqa son qaytarsa — "xato bor, ogohlantir" deb tushunadi.

`exit()` skriptni darhol to'xtatadi va kod qaytaradi:

```php
<?php

$fayl = $argv[1] ?? null;

if ($fayl === null) {
    echo "Xato: fayl nomini bering.\n";
    exit(1);   // xato kodi bilan to'xtatamiz
}

if (!file_exists($fayl)) {
    echo "Xato: '$fayl' fayli topilmadi.\n";
    exit(1);
}

echo "Fayl topildi, ishni boshlaymiz...\n";
// ... asosiy ish ...

exit(0);   // muvaffaqiyatli tugadi (yoki shunchaki skript oxiriga yetsa ham 0)
```

`exit` ga matn ham berish mumkin — u ekranga chiqadi va kod **0** bo'ladi:

```php
<?php
exit("Tugadi.\n");   // matnni chiqaradi, kod = 0
```

Lekin xato uchun `exit(1)` (son bilan) ishlatish to'g'riroq — chunki bu yerda kod muhim.

Oxirgi skriptning chiqish kodini terminalda tekshirish mumkin (Windows PowerShell'da `$LASTEXITCODE`, Linux/macOS'da `echo $?`). Bu — skriptlarni zanjirlab bog'lashning asosi.

### O'rnatilgan dev-server — `php -S`

PHP'da kichik bir mo'jiza bor: alohida Apache yoki Nginx o'rnatmasdan, bitta buyruq bilan vaqtinchalik veb-server ishga tushirish mumkin. Bu — o'rganish va tez sinash uchun ideal:

```
php -S localhost:8000
```

Bu buyruq joriy papkani veb-sayt sifatida `http://localhost:8000` manzilida ochadi. Endi brauzerda shu manzilga kirsangiz, papkadagi `.php` fayllar ishlaydi.

Masalan, papkada `index.php` bo'lsa:

```php
<?php

echo "<h1>Salom, dev-server!</h1>";
echo "<p>Vaqt: " . date('H:i:s') . "</p>";
```

`php -S localhost:8000` deb, brauzerda `http://localhost:8000` ni ochsangiz — sahifani ko'rasiz. To'xtatish uchun terminalda **Ctrl + C**.

Boshqa papkani server qilish uchun `-t` (target) flagi:

```
php -S localhost:8000 -t public
```

Bu — `public` papkasini ildiz qiladi (zamonaviy loyihalarda `index.php` aynan `public` da turadi).

**Eslatma:** `php -S` faqat o'rganish va lokal sinash uchun. Haqiqiy serverda (productionda) Nginx yoki Apache ishlatiladi — chunki `php -S` bir vaqtda ko'p so'rovni ko'tara olmaydi.

### Rangli chiqish — ANSI ranglari

Professional CLI vositalar xatoni qizil, muvaffaqiyatni yashil rangda ko'rsatadi — bu o'qishni osonlashtiradi. Terminalda rang **ANSI escape** (maxsus boshqaruv belgilari) kodlari bilan beriladi. Ko'rinishi g'alati, lekin sodda: rang kodini matn oldiga, "reset" (rangni qaytarish) kodini oxiriga qo'yasiz.

```php
<?php

$qizil = "\033[31m";
$yashil = "\033[32m";
$sariq = "\033[33m";
$reset = "\033[0m";   // rangni odatdagiga qaytaradi

echo $yashil . "OK: hammasi joyida" . $reset . "\n";
echo $qizil . "XATO: fayl topilmadi" . $reset . "\n";
echo $sariq . "OGOHLANTIRISH: bo'sh qiymat" . $reset . "\n";
```

Terminalda birinchi qator yashil, ikkinchisi qizil, uchinchisi sariq bo'lib chiqadi.

`\033[32m` — bu yashil rang kodi (`\033` — escape belgisi, `[32m` — "yashil matn"). `\033[0m` — "rangni qaytar". Reset'ni qo'yishni unutmang, aks holda undan keyingi hamma matn rangli bo'lib qoladi.

Buni qayta-qayta ishlatish uchun kichik yordamchi funksiya yozish qulay:

```php
<?php

function rangli(string $matn, string $rang): string
{
    $ranglar = [
        'qizil'  => "\033[31m",
        'yashil' => "\033[32m",
        'sariq'  => "\033[33m",
    ];
    $reset = "\033[0m";

    return ($ranglar[$rang] ?? '') . $matn . $reset;
}

echo rangli("Muvaffaqiyatli!", 'yashil') . "\n";
echo rangli("Xatolik yuz berdi", 'qizil') . "\n";
```

Endi rangli matn yozish bitta funksiya chaqiruviga aylandi — kod toza bo'ladi.

### Real misol 1 — interaktiv kalkulyator

Endi o'rganganlarimizni birlashtiramiz. Foydalanuvchidan ikkita son va amalni so'rab, natijani chiqaradigan kichik kalkulyator:

```php
<?php

// yuqorida yozgan universal so'rash yordamchimiz
function sora(string $savol): string
{
    if (function_exists('readline')) {
        return trim((string) readline($savol));
    }
    echo $savol;
    return trim((string) fgets(STDIN));
}

echo "=== CLI Kalkulyator ===\n";

$a = (float) sora("Birinchi son: ");
$amal = sora("Amal (+ - * /): ");
$b = (float) sora("Ikkinchi son: ");

$natija = match ($amal) {
    '+' => $a + $b,
    '-' => $a - $b,
    '*' => $a * $b,
    '/' => $b !== 0.0 ? $a / $b : null,
    default => null,
};

if ($natija === null) {
    echo "\033[31mXato: noto'g'ri amal yoki nolga bo'lish.\033[0m\n";
    exit(1);
}

echo "\033[32mNatija: $a $amal $b = $natija\033[0m\n";
exit(0);
```

Ishlashi:

```
=== CLI Kalkulyator ===
Birinchi son: 10
Amal (+ - * /): *
Ikkinchi son: 4
Natija: 10 * 4 = 40
```

Bu yerda `match` (1.7 da ko'rgan) amalni tanlash uchun ideal: har bir belgi uchun bitta natija. Nolga bo'lish va noto'g'ri amal `null` bo'lib, qizil xato beradi va `exit(1)` bilan tugaydi. So'rashni `sora` orqali qildik — shuning uchun bu kalkulyator Windows'da ham, Linux'da ham bir xil ishlaydi.

### Real misol 2 — fayl generator

Ko'pincha test uchun bir nechta bir xil ko'rinishdagi fayl kerak bo'ladi (masalan, 5 ta bo'sh shablon). Buni qo'lda yaratish zerikarli — skript yozamiz. Nechta fayl yaratishni `getopt` flagi orqali olamiz:

```php
<?php

// --count=5 --prefix=test  ko'rinishida chaqiriladi
$flaglar = getopt('', ['count:', 'prefix:']);

$soni = (int) ($flaglar['count'] ?? 3);
$prefiks = $flaglar['prefix'] ?? 'fayl';

if ($soni < 1) {
    echo "\033[31mXato: --count musbat son bo'lishi kerak.\033[0m\n";
    exit(1);
}

for ($i = 1; $i <= $soni; $i++) {
    $nom = "{$prefiks}_{$i}.txt";
    $matn = "Bu {$i}-fayl. Yaratilgan: " . date('Y-m-d H:i:s') . PHP_EOL;

    file_put_contents($nom, $matn);
    echo "\033[32m+\033[0m Yaratildi: $nom\n";
}

echo "\nJami $soni ta fayl yaratildi.\n";
exit(0);
```

```
php generator.php --count=3 --prefix=hujjat
```

natija:

```
+ Yaratildi: hujjat_1.txt
+ Yaratildi: hujjat_2.txt
+ Yaratildi: hujjat_3.txt

Jami 3 ta fayl yaratildi.
```

`file_put_contents` — fayl yozadigan tayyor funksiya (faylga matn yozish). `--count` berilmasa, `?? 3` bilan standart 3 ta yaratiladi. Mana shunaqa kichik vositalar real ishda kuningizni tejaydi.

### Real misol 3 — CSV import vositasi

Eng amaliy misol. Mijoz sizga `foydalanuvchilar.csv` fayl berdi va "buni qayta ishlab ber" dedi. CSV (Comma-Separated Values — vergul bilan ajratilgan qiymatlar) — Excel'dan eksport qilinadigan oddiy jadval formati. Fayl nomini argument orqali olib, har qatorni o'qiymiz.

Avval namuna CSV fayl ko'rinishi (`foydalanuvchilar.csv`):

```
ism,email,yosh
Ali,ali@mail.com,25
Vali,vali@mail.com,30
Guli,guli@mail.com,invalid
```

Endi import skripti:

```php
<?php

// Foydalanish: php import.php foydalanuvchilar.csv
$fayl = $argv[1] ?? null;

if ($fayl === null) {
    echo "\033[31mFoydalanish: php import.php <fayl.csv>\033[0m\n";
    exit(1);
}

if (!file_exists($fayl)) {
    echo "\033[31mXato: '$fayl' topilmadi.\033[0m\n";
    exit(1);
}

$qator = 0;
$muvaffaqiyatli = 0;
$xato = 0;

$ochildi = fopen($fayl, 'r');   // faylni o'qish uchun ochamiz

// PHP 8.4'da fgetcsv'ga escape: '' berish tavsiya etiladi (ortiqcha "qochirish"siz)
while (($maydonlar = fgetcsv($ochildi, escape: '')) !== false) {
    $qator++;

    // Birinchi qator — sarlavha (ism,email,yosh), uni o'tkazib yuboramiz
    if ($qator === 1) {
        continue;
    }

    [$ism, $email, $yosh] = $maydonlar;

    // Oddiy tekshiruv: email ichida @ va yosh — son bo'lsin
    if (!str_contains($email, '@') || !is_numeric($yosh)) {
        echo "\033[31m  Qator $qator: noto'g'ri ma'lumot ($ism)\033[0m\n";
        $xato++;
        continue;
    }

    // Haqiqiy loyihada bu yerda bazaga INSERT bo'lardi
    echo "\033[32m  + $ism ($email), $yosh yosh\033[0m\n";
    $muvaffaqiyatli++;
}

fclose($ochildi);   // faylni yopamiz

echo "\n=== Yakun ===\n";
echo "Muvaffaqiyatli: $muvaffaqiyatli\n";
echo "Xato: $xato\n";

exit($xato > 0 ? 1 : 0);   // xato bo'lsa, kod 1
```

Ishlashi:

```
php import.php foydalanuvchilar.csv
```

natija:

```
  + Ali (ali@mail.com), 25 yosh
  + Vali (vali@mail.com), 30 yosh
  Qator 4: noto'g'ri ma'lumot (Guli)

=== Yakun ===
Muvaffaqiyatli: 2
Xato: 1
```

Bu yerda yangi funksiyalar:

- **`fopen($fayl, 'r')`** — faylni o'qish (`'r'` = read) uchun ochadi.
- **`fgetcsv($ochildi, escape: '')`** — CSV'ning bitta qatorini o'qib, qiymatlarni avtomatik massivga ajratadi (vergulni o'zi tushunadi). Fayl tugasa `false` qaytaradi. PHP 8.4'da `escape: ''` ni aniq berish tavsiya etiladi (`escape` — bu **named argument**, ya'ni nomi bilan beriladigan parametr; aks holda PHP eskirish ogohlantirishini chiqaradi).
- **`fclose($ochildi)`** — faylni yopadi (yaxshi odat — resursni bo'shatadi).
- **`[$ism, $email, $yosh] = $maydonlar`** — bu **destructuring** (massivni o'zgaruvchilarga "yoyish"): massivning 0,1,2-elementlarini uchta o'zgaruvchiga bir vaqtda joylash.

Bu skript — haqiqiy import vositalarining kichraytirilgan, lekin to'liq ishlaydigan namunasi. Bazaga ulanishni (1.10, ma'lumotlar bazasi qismi) qo'shsangiz — tayyor migratsiya/import vositasiga aylanadi.

### Mashqlar

**Oson**

1. `salom.php` faylini yarating: terminalda "Salom, dunyo!" deb chiqarsin (`\n` bilan). `php salom.php` orqali ishga tushiring.
2. Skript barcha `$argv` argumentlarini va ularning sonini (`$argc`) chiqarsin.
3. `php -v` buyrug'ini ishga tushiring va PHP versiyangizni aniqlang. Keyin kod ichida `PHP_SAPI` ni `echo` qilib, "cli" chiqishiga ishonch hosil qiling.
4. `PHP_EOL` yordamida uchta qatorni har xil qatorlarda chiqaring.
5. Foydalanuvchidan ismini so'rang (`readline` bo'lmasa `fgets(STDIN)`) va "Salom, <ism>!" deb javob bering. Javobni `trim` qiling.

**O'rta**

6. Skript ikkita argument (`$argv[1]`, `$argv[2]`) ni son sifatida olib, ularning yig'indisini chiqarsin. Argument yetmasa, ogohlantirib `exit(1)` bilan to'xtasin.
7. Foydalanuvchidan "Davom etilsinmi? (ha/yo'q)" deb so'rang (`fgets(STDIN)` + `trim`). "ha" bo'lsa — "Davom etamiz", aks holda — "To'xtatildi".
8. `$argv[1]` orqali olingan amal va ikki songa (`$argv[2]`, `$argv[3]`) qarab `+` yoki `-` natijasini `match` bilan chiqaring.
9. Muvaffaqiyat xabarini yashil (`\033[32m`), xato xabarini qizil (`\033[31m`) rangda chiqaradigan ikkita qatorli skript yozing. Reset (`\033[0m`) ni unutmang.

**Qiyin**

10. `getopt` bilan `--name` va `--age` flaglarini o'qiydigan skript yozing. Ikkalasi ham berilsa — "Ali, 25 yosh" deb chiqarsin; biri yetmasa — qizil xato va `exit(1)`.
11. Interaktiv kalkulyator yozing: universal `sora` yordamchisi (`readline` yoki `fgets(STDIN)`) bilan ikki son va amal (`+ - * /`) so'rang, `match` bilan natijani hisoblang, nolga bo'lishni ushlang.
12. Fayl generator yozing: `--count=N` flagi bo'yicha N ta `.txt` fayl yaratsin (ichida tartib raqami va sana bo'lsin). `--count` berilmasa — standart 3 ta.
13. Sodda CSV import skripti yozing: fayl nomini `$argv[1]` dan oling, har qatorni `fgetcsv` bilan o'qing, sarlavhani o'tkazib yuboring, har bir qator ma'lumotini chiqaring va oxirida nechta qator qayta ishlanganini ayting.

<details markdown="1">
<summary>Yechim — 6</summary>

```php
<?php

$a = $argv[1] ?? null;
$b = $argv[2] ?? null;

if ($a === null || $b === null) {
    echo "Xato: ikkita son bering. Masalan: php yigindi.php 5 3\n";
    exit(1);
}

$natija = (int) $a + (int) $b;
echo "Yig'indi: $natija\n";
exit(0);
```

`(int)` bilan matnni songa aylantirdik, chunki `$argv` ichidagi hamma narsa — string. Argument yetmasa, `exit(1)` xato kodi bilan to'xtatdik.
</details>

<details markdown="1">
<summary>Yechim — 9 (rangli chiqish)</summary>

```php
<?php

$yashil = "\033[32m";
$qizil  = "\033[31m";
$reset  = "\033[0m";

echo $yashil . "OK: amal bajarildi" . $reset . "\n";
echo $qizil  . "XATO: nimadir noto'g'ri" . $reset . "\n";
```

Rang kodini matn oldiga, `\033[0m` (reset) ni oxiriga qo'yamiz. Reset bo'lmasa, undan keyingi butun matn rangli bo'lib qoladi.
</details>

<details markdown="1">
<summary>Yechim — 10 (getopt bilan CLI vosita)</summary>

```php
<?php

$flaglar = getopt('', ['name:', 'age:']);

$ism = $flaglar['name'] ?? null;
$yosh = $flaglar['age'] ?? null;

if ($ism === null || $yosh === null) {
    echo "\033[31mXato: --name va --age ikkalasi ham kerak.\033[0m\n";
    echo "Masalan: php tool.php --name=Ali --age=25\n";
    exit(1);
}

echo "\033[32m$ism, $yosh yosh\033[0m\n";
exit(0);
```

`getopt('', ['name:', 'age:'])` — qisqa flag yo'q (`''`), faqat uzun flaglar. Har ikkala `:` — "qiymat kerak" degani. `?? null` bilan yetishmaganini aniqlab, qizil xato beramiz.
</details>

<details markdown="1">
<summary>Yechim — 11 (interaktiv kalkulyator)</summary>

```php
<?php

function sora(string $savol): string
{
    if (function_exists('readline')) {
        return trim((string) readline($savol));
    }
    echo $savol;
    return trim((string) fgets(STDIN));
}

$a = (float) sora("Birinchi son: ");
$amal = sora("Amal (+ - * /): ");
$b = (float) sora("Ikkinchi son: ");

$natija = match ($amal) {
    '+' => $a + $b,
    '-' => $a - $b,
    '*' => $a * $b,
    '/' => $b !== 0.0 ? $a / $b : null,
    default => null,
};

if ($natija === null) {
    echo "\033[31mXato: noto'g'ri amal yoki nolga bo'lish.\033[0m\n";
    exit(1);
}

echo "\033[32mNatija: $natija\033[0m\n";
```

`match` har bir amal uchun bitta natija beradi. Nolga bo'lish va noto'g'ri amal `null` bo'lib, qizil xato chiqaradi. `(float)` bilan kiritilgan matnni songa aylantiramiz. So'rashni `sora` orqali qilganimiz uchun kod Windows'da ham ishlaydi.
</details>

<details markdown="1">
<summary>Yechim — 13 (CSV import)</summary>

```php
<?php

$fayl = $argv[1] ?? null;

if ($fayl === null || !file_exists($fayl)) {
    echo "\033[31mFoydalanish: php import.php <mavjud-fayl.csv>\033[0m\n";
    exit(1);
}

$ochildi = fopen($fayl, 'r');
$qator = 0;
$qayta_ishlangan = 0;

while (($maydonlar = fgetcsv($ochildi, escape: '')) !== false) {
    $qator++;

    if ($qator === 1) {
        continue;   // sarlavhani o'tkazamiz
    }

    echo "  " . implode(' | ', $maydonlar) . "\n";
    $qayta_ishlangan++;
}

fclose($ochildi);

echo "\nJami $qayta_ishlangan ta qator qayta ishlandi.\n";
exit(0);
```

`fgetcsv` har qatorni avtomatik massivga ajratadi. Birinchi qator (sarlavha) `continue` bilan o'tkazib yuboriladi. `implode(' | ', ...)` bilan maydonlarni chiroyli chiqaramiz. Fayl tugagach `fclose` bilan yopamiz.
</details>
