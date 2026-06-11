# 1.13 Generatorlar va iteratorlar

[⬅️ Oldingi: 1.12 Sana va vaqt](./sana-vaqt.md) · [🏠 README](./README.md) · [Keyingi: 1.14 CLI — terminal skriptlari ➡️](./cli-skriptlar.md)

---

Tasavvur qiling: sizda 1 million qatorli log fayl bor va siz har bir qatorni o'qib chiqishingiz kerak. Birinchi xayolga keladigan yechim — butun faylni massivga yuklab, keyin uni `foreach` bilan aylanib chiqish. Lekin bu million qatorni **bir vaqtda** xotiraga yuklaydi — natijada dasturingiz yuzlab megabayt RAM yeydi yoki umuman "Out of memory" xatosi bilan o'ladi.

Aslida sizga bir vaqtning o'zida faqat **bitta** qator kerak: o'qiysiz, ishlatasiz, tashlaysiz, keyingisiga o'tasiz. Aynan shu g'oyani **generator** amalga oshiradi. Generator — qiymatlarni oldindan hammasini hisoblab xotiraga to'ldirmaydigan, balki **kerak bo'lganda, bittadan hosil qiladigan** maxsus funksiya. Bu uslub "lazy" (dangasa) hisoblash deyiladi: ish faqat zarur paytda bajariladi.

Bu bobda generatorlarni (`yield` kalit so'zi), ularning massivdan farqini (xotira solishtirish bilan), katta fayllarni qator-qator o'qishni, cheksiz ketma-ketliklarni va pastroq darajadagi `Iterator` interfeysini o'rganamiz. Bu mavzular sizning dasturlaringizni xotira-tejamkor va kuchli qiladi.

### Birinchi generator — `yield` kalit so'zi

Oddiy funksiya qiymat qaytarganda `return` ishlatadi va **bir marta** ishlab, **bitta** qiymat qaytaradi-da, tugaydi. Generator esa `yield` (o'qilishi: "yild", "hosil qil" degani) kalit so'zini ishlatadi va **bir necha marta** qiymat "uzatib turishi" mumkin — har safar to'xtab, keyingi safar **aynan o'sha joydan** davom etadi.

Funksiya ichida hech bo'lmasa bitta `yield` bo'lsa, PHP uni avtomatik ravishda **generator**ga aylantiradi:

```php
<?php
function sanaqlar(): Generator
{
    yield 1;
    yield 2;
    yield 3;
}

foreach (sanaqlar() as $son) {
    echo $son . "\n";
}
// 1
// 2
// 3
```

Diqqat qiling: `sanaqlar()` chaqirilganda funksiya **darrov ishlamaydi**. U `Generator` obyektini qaytaradi. Kod faqat siz `foreach` bilan aylanganda ishga tushadi — har bir `yield`gacha boradi, qiymatni beradi, **to'xtaydi** va keyingi takrorlashda davom etadi.

### Generator ish jarayonini ko'rish

Generatorning "to'xtab-davom etadigan" tabiatini ko'rish uchun `yield` orasiga `echo` qo'yamiz:

```php
<?php
function jarayon(): Generator
{
    echo "Boshlandi\n";
    yield "A";
    echo "A dan keyin\n";
    yield "B";
    echo "B dan keyin\n";
}

foreach (jarayon() as $qiymat) {
    echo "Olindi: {$qiymat}\n";
}
// Boshlandi
// Olindi: A
// A dan keyin
// Olindi: B
// B dan keyin
```

Natijaga e'tibor bering: kod "Boshlandi"ni faqat **birinchi** qiymat so'ralganda chiqaradi, "A dan keyin"ni esa **ikkinchi** qiymat so'ralganda. Ya'ni generator har `yield`da muzlaydi va keyingi takrorlash uni uyg'otadi. Bu — generatorning butun sehri.

### Generator vs array — xotira solishtirish

Endi generatorning asosiy ustunligini raqamlar bilan ko'ramiz. Bir million sonni avval **massiv** sifatida yasaymiz, keyin **generator** sifatida — va `memory_get_usage` (joriy band qilingan xotira baytlarda) bilan farqni o'lchaymiz.

Avval massiv yo'li:

```php
<?php
function massivYasa(int $n): array
{
    $natija = [];
    for ($i = 1; $i <= $n; $i++) {
        $natija[] = $i;
    }
    return $natija;   // hamma 1 mln son xotirada!
}

$oldin = memory_get_usage();
$sonlar = massivYasa(1_000_000);
$keyin = memory_get_usage();

$mb = ($keyin - $oldin) / 1024 / 1024;
echo "Massiv xotirasi: " . number_format($mb, 2) . " MB\n";
// Massiv xotirasi: ~18 MB (taxminan, PHP versiyasiga qarab)
```

Endi xuddi shu vazifa, lekin generator bilan:

```php
<?php
function generatorYasa(int $n): Generator
{
    for ($i = 1; $i <= $n; $i++) {
        yield $i;        // har safar bittasi hosil bo'ladi
    }
}

$oldin = memory_get_usage();
$gen = generatorYasa(1_000_000);
$keyin = memory_get_usage();

$kb = ($keyin - $oldin);
echo "Generator xotirasi: " . $kb . " bayt\n";
// Generator xotirasi: ~448 bayt (megabayt emas — deyarli hech narsa!)
```

Massiv 1 million sonni saqlash uchun **o'nlab megabayt** band qiladi. Generator esa deyarli **0 bayt** — chunki u sonlarni saqlamaydi, balki har safar `foreach` so'raganda bittadan hosil qiladi. Mana lazy hisoblashning kuchi: qiymatlar yashaydi va o'ladi, ular hech qachon birgalikda xotirada turmaydi.

> **Eslatma:** `1_000_000` — PHP 7.4+ da raqamlarni o'qilishli qilish uchun pastki chiziq ishlatish mumkin. `1_000_000` va `1000000` bir xil son.

### Kalit va qiymat — `yield key => value`

Massivlarda har element kalit (key) va qiymat (value) juftligidan iborat. Generatorlar ham xuddi shunday kalit berishi mumkin — `yield kalit => qiymat` shaklida:

```php
<?php
function foydalanuvchilar(): Generator
{
    yield "admin" => "Oqil";
    yield "mehmon" => "Vali";
    yield "moderator" => "Guli";
}

foreach (foydalanuvchilar() as $rol => $ism) {
    echo "{$rol}: {$ism}\n";
}
// admin: Oqil
// mehmon: Vali
// moderator: Guli
```

Agar kalit bermasangiz, PHP avtomatik 0, 1, 2, ... butun sonlarni kalit qiladi (xuddi oddiy massivdagidek). Kalit berish, masalan, CSV faylni o'qiyotganda "qator raqami => qator mazmuni" ko'rinishida juda foydali.

### Generatordan qiymat qaytarish — `return`

Generator ichida `yield` qiymatlar **uzatadi**, lekin generator tugaganda yana bitta yakuniy qiymatni `return` bilan qaytarishi mumkin. Bu yakuniy qiymat `foreach`da **ko'rinmaydi** — uni `getReturn()` metodi bilan, generator to'liq aylanib bo'lgandan keyin olasiz:

```php
<?php
function hisobla(): Generator
{
    $yigindi = 0;
    yield $qiymat = 10;
    $yigindi += $qiymat;
    yield $qiymat = 20;
    $yigindi += $qiymat;
    return $yigindi;        // yakuniy natija
}

$gen = hisobla();
foreach ($gen as $q) {
    echo "Qiymat: {$q}\n";
}
echo "Jami: " . $gen->getReturn() . "\n";
// Qiymat: 10
// Qiymat: 20
// Jami: 30
```

`return` generatorni tugatadi va yakuniy "xulosa"ni saqlaydi. Masalan, fayl o'qiyotganda har qatorni `yield` qilib, oxirida jami qatorlar sonini `return` qilishingiz mumkin.

### Boshqa generatorni ulash — `yield from`

Ko'pincha bitta generator ichidan boshqa generatorning (yoki massivning) hamma qiymatlarini "quyish" kerak bo'ladi. Buni qo'lda `foreach` bilan qilish o'rniga `yield from` ishlatiladi — u boshqa manbaning **barcha** qiymatlarini joriy generatorga uzatadi:

```php
<?php
function birinchiQism(): Generator
{
    yield 1;
    yield 2;
}

function ikkinchiQism(): Generator
{
    yield 3;
    yield 4;
}

function hammasi(): Generator
{
    yield from birinchiQism();    // 1, 2
    yield from ikkinchiQism();    // 3, 4
    yield from [5, 6];            // massivdan ham bo'ladi
}

foreach (hammasi() as $son) {
    echo $son . " ";
}
echo "\n";
// 1 2 3 4 5 6
```

`yield from` katta generatorni kichik, qayta ishlatiladigan bo'laklarga ajratishga yordam beradi. Bu — generatorlarni "bir-biriga ulash" usuli.

### Katta faylni qator-qator o'qish

Endi bobning boshidagi muammoga qaytamiz — katta faylni xotira-tejamkor o'qish. PHP'ning `fopen`/`fgets` funksiyalari faylni qator-qator o'qiydi; biz har qatorni `yield` qilamiz. Natijada fayl qanchalik katta bo'lmasin, xotirada **bir vaqtda faqat bitta qator** turadi.

Avval test uchun fayl yasaymiz, keyin uni generator bilan o'qiymiz:

```php
<?php
// 1) Test fayl yasaymiz (10 ta qator)
$fayl = sys_get_temp_dir() . "/log.txt";
$f = fopen($fayl, "w");
for ($i = 1; $i <= 10; $i++) {
    fwrite($f, "Qator raqami {$i}\n");
}
fclose($f);

// 2) Generator bilan qator-qator o'qiymiz
function qatorlarniOqi(string $yol): Generator
{
    $f = fopen($yol, "r");
    if ($f === false) {
        throw new RuntimeException("Fayl ochilmadi: {$yol}");
    }
    try {
        while (($qator = fgets($f)) !== false) {
            yield rtrim($qator, "\n");   // oxiridagi yangi qator belgisini olib tashlaymiz
        }
    } finally {
        fclose($f);     // generator tugaganda yoki uzilganda fayl yopiladi
    }
}

foreach (qatorlarniOqi($fayl) as $raqam => $qator) {
    echo "{$raqam}: {$qator}\n";
}
// 0: Qator raqami 1
// 1: Qator raqami 2
// ... 9: Qator raqami 10
```

Bu yondashuv 10 qatorlik faylda ham, 10 millionlik faylda ham bir xil — **doimiy** miqdorda xotira ishlatadi. `try/finally` bloki muhim: generator tugasa ham, yarim yo'lda to'xtatilsa ham, fayl albatta yopiladi.

### CSV faylni generator bilan o'qish

Amaliy misol: CSV (vergul bilan ajratilgan qiymatlar) faylni qator-qator o'qib, har qatorni massivga ajratish. `fgetcsv` faylning bir qatorini o'qib, uni darrov massivga aylantiradi — buni `yield` bilan birlashtiramiz:

```php
<?php
// Test CSV yasaymiz
$csv = sys_get_temp_dir() . "/mahsulotlar.csv";
file_put_contents($csv, "Noutbuk,1200\nSichqoncha,15\nKlaviatura,40\n");

function csvOqi(string $yol): Generator
{
    $f = fopen($yol, "r");
    try {
        while (($qator = fgetcsv($f, escape: "")) !== false) {
            yield $qator;       // ["Noutbuk", "1200"] ko'rinishida
        }
    } finally {
        fclose($f);
    }
}

$jamiNarx = 0;
foreach (csvOqi($csv) as [$nom, $narx]) {
    echo "{$nom}: {$narx}$\n";
    $jamiNarx += (int) $narx;
}
echo "Jami: {$jamiNarx}$\n";
// Noutbuk: 1200$
// Sichqoncha: 15$
// Klaviatura: 40$
// Jami: 1255$
```

Diqqat: `foreach (... as [$nom, $narx])` — bu massivni darrov ikki o'zgaruvchiga ajratish (destructuring). Million qatorli CSV ham shu usulda xotirani to'ldirmasdan o'qiladi.

> **Eslatma:** `fgetcsv`da `escape: ""` (named argument) PHP 8.4'da tavsiya etiladi — eski "escape" xulqi PHP 9'da olib tashlanadi, shuning uchun uni bo'sh qilib qo'yish kelajakka mos kod yozadi.

### Cheksiz ketma-ketlik

Massiv har doim cheklangan — uni xotiraga sig'dirish kerak. Generator esa **cheksiz** ketma-ketlik hosil qila oladi, chunki qiymatlar oldindan yasalmaydi. Quyidagi generator hech qachon tugamaydi — siz qachon to'xtashni o'zingiz hal qilasiz:

```php
<?php
function cheksizSonlar(int $boshlanish = 1): Generator
{
    $son = $boshlanish;
    while (true) {          // cheksiz tsikl!
        yield $son;
        $son++;
    }
}

$natija = [];
foreach (cheksizSonlar(100) as $son) {
    if ($son > 105) {
        break;              // biz o'zimiz to'xtatamiz
    }
    $natija[] = $son;
}
echo implode(", ", $natija) . "\n";
// 100, 101, 102, 103, 104, 105
```

`while (true)` oddiy funksiyada dasturni qotirib qo'yardi. Generatorda esa muammo yo'q: har qiymat so'ralgandagina bittasi hosil bo'ladi, qolgani "kelajakda" qoladi. To'xtashni `break` yoki shart bilan boshqarasiz.

### Amaliy cheksiz ketma-ketlik — Fibonachchi

Cheksiz generatorning klassik misoli — Fibonachchi sonlari (har son oldingi ikkitasining yig'indisi). Bunda generator "holatni eslab qoladi" degan g'oyani yaqqol ko'rasiz: o'zgaruvchilar `yield`lar orasida saqlanib qoladi.

```php
<?php
function fibonachchi(): Generator
{
    [$a, $b] = [0, 1];
    while (true) {
        yield $a;
        [$a, $b] = [$b, $a + $b];   // navbatdagi juftlikka o'tamiz
    }
}

$dastlabki10 = [];
foreach (fibonachchi() as $son) {
    if (count($dastlabki10) >= 10) {
        break;
    }
    $dastlabki10[] = $son;
}
echo implode(" ", $dastlabki10) . "\n";
// 0 1 1 2 3 5 8 13 21 34
```

`$a` va `$b` o'zgaruvchilari har `yield`da xotirada qoladi — generator to'xtaganda ham ularning qiymati yo'qolmaydi. Bu generatorlarning "holatni saqlash" qobiliyatini ko'rsatadi.

### Iterator interfeysi — o'z obyektingizni `foreach` qilish

Generatorlar — `Iterator` (takrorlanuvchi) interfeysining qulay, avtomatik ko'rinishi. Agar to'liq nazorat kerak bo'lsa, `Iterator` interfeysini o'zingiz amalga oshirishingiz mumkin. Bu interfeys 5 ta metodni talab qiladi:

- `current()` — joriy qiymat
- `key()` — joriy kalit
- `next()` — keyingisiga o'tish
- `rewind()` — boshiga qaytish (`foreach` boshida chaqiriladi)
- `valid()` — hali qiymat bormi (`false` bo'lsa `foreach` tugaydi)

Mana oddiy diapazon (range) iteratori:

```php
<?php
class Diapazon implements Iterator
{
    private int $joriy;

    public function __construct(
        private readonly int $boshlanish,
        private readonly int $tugash,
        private readonly int $qadam = 1,
    ) {
        $this->joriy = $boshlanish;
    }

    public function current(): int
    {
        return $this->joriy;
    }

    public function key(): int
    {
        return ($this->joriy - $this->boshlanish) / $this->qadam;
    }

    public function next(): void
    {
        $this->joriy += $this->qadam;
    }

    public function rewind(): void
    {
        $this->joriy = $this->boshlanish;
    }

    public function valid(): bool
    {
        return $this->joriy <= $this->tugash;
    }
}

foreach (new Diapazon(0, 10, 2) as $kalit => $son) {
    echo "{$kalit} => {$son}\n";
}
// 0 => 0
// 1 => 2
// 2 => 4
// 3 => 6
// 4 => 8
// 5 => 10
```

`foreach` ich-ichida shu 5 metodni chaqiradi: avval `rewind()`, keyin har takrorlashda `valid()` (davom etish kerakmi?), `current()` (qiymat), `key()` (kalit), so'ng `next()`. Generatorlar aslida xuddi shu ishni siz uchun avtomatik bajaradi — shuning uchun oddiy holatlarda generator ancha qulay.

### IteratorAggregate — soddaroq yo'l

`Iterator`ning 5 ta metodini yozish ko'p ish. Agar obyektingiz ichida allaqachon massiv yoki generator bo'lsa, `IteratorAggregate` interfeysidan foydalanish ancha oson — u faqat **bitta** metodni talab qiladi: `getIterator()`, u takrorlanuvchini qaytaradi.

```php
<?php
class Jamoa implements IteratorAggregate
{
    private array $azolar = [];

    public function qoshish(string $ism): void
    {
        $this->azolar[] = $ism;
    }

    public function getIterator(): Generator
    {
        foreach ($this->azolar as $tartib => $ism) {
            yield $tartib + 1 => $ism;   // 1 dan boshlab raqamlaymiz
        }
    }
}

$jamoa = new Jamoa();
$jamoa->qoshish("Oqil");
$jamoa->qoshish("Vali");
$jamoa->qoshish("Guli");

foreach ($jamoa as $raqam => $ism) {
    echo "{$raqam}. {$ism}\n";
}
// 1. Oqil
// 2. Vali
// 3. Guli
```

`getIterator()` ichida generator (`yield`) ishlatdik — bu eng qulay usul, chunki 5 ta metodni qo'lda yozish shart emas. Obyektingiz tashqaridan oddiy massivdek `foreach` qilinadi, lekin ichida xohlagan mantiqni (filtrlash, raqamlash, hisoblash) yashirishingiz mumkin.

### Generatorni massivga aylantirish — `iterator_to_array`

Ba'zan generator natijasini to'liq massiv sifatida kerak bo'ladi (masalan, `count` qilish yoki `sort`lash uchun). `iterator_to_array` generatorni aylanib chiqib, hamma qiymatni massivga yig'adi:

```php
<?php
function juftSonlar(int $chegara): Generator
{
    for ($i = 0; $i <= $chegara; $i += 2) {
        yield $i;
    }
}

$massiv = iterator_to_array(juftSonlar(10));
echo "Soni: " . count($massiv) . "\n";
echo "Qiymatlar: " . implode(", ", $massiv) . "\n";
// Soni: 6
// Qiymatlar: 0, 2, 4, 6, 8, 10
```

Diqqat: bu generatorning butun mazmunini xotiraga yuklaydi — ya'ni lazy afzalligini yo'qotadi. Faqat **cheklangan** va kichikroq generatorlar bilan ishlating; cheksiz generatorda `iterator_to_array` dasturni cheksiz qotirib qo'yadi.

### Qachon generator, qachon massiv?

Ikkalasi ham `foreach` qilinadi, lekin tanlash quyidagicha:

**Generator ishlating, agar:**
- Ma'lumotlar ko'p (katta fayl, ko'p qatorli natija) — xotirani tejaysiz.
- Qiymatlarni faqat **bir marta**, tartib bilan o'qishingiz kifoya.
- Ketma-ketlik cheksiz yoki noma'lum uzunlikda (oqim, real-time ma'lumot).
- Har qiymatni hisoblash "qimmat" — kerak bo'lmasa, umuman hisoblanmaydi.

**Massiv ishlating, agar:**
- Ma'lumotlar kichik va xotiraga bemalol sig'adi.
- Elementlarga **tasodifiy** kirish kerak (`$massiv[5]`, oxirgi element va h.k.).
- Bir nechta marta aylanishingiz kerak (generatorni qayta `foreach` qilib bo'lmaydi — u "bir martalik").
- `count`, `sort`, `array_map` kabi massiv funksiyalari kerak.

Eng muhim farq: **generator bir martalik**. Uni bir marta aylanib bo'lgach, qaytadan `foreach` qilsangiz, qiymat kelmaydi (yoki xato beradi). Massivni esa xohlagancha qayta aylanish mumkin. Shubha bo'lsa: katta yoki cheksiz ma'lumot — generator; kichik va qayta kerak bo'ladigan ma'lumot — massiv.

### Mashqlar

**Oson**

1. `salomlar()` nomli generator yozing: u `yield` bilan `"Salom"`, `"Hello"`, `"Hi"` so'zlarini bersin. Uni `foreach` bilan chiqaring.

2. `uchtaSon()` generatori 5, 10, 15 sonlarini `yield` qilsin. `foreach` bilan har birini yangi qatorda chiqaring.

3. Generator nima uchun massivdan ko'ra kamroq xotira ishlatishini bir-ikki jumlada o'z so'zingiz bilan tushuntiring.

4. `harflar()` generatori `yield key => value` bilan `"a" => 1`, `"b" => 2`, `"c" => 3` bersin. Kalit va qiymatni `foreach`da chiqaring.

**O'rta**

5. `diapazon(int $boshlanish, int $tugash)` generatori yozing: u `$boshlanish`dan `$tugash`gacha (shu sonlar ham kiradi) hamma butun sonni `yield` qilsin. `diapazon(3, 7)` -> 3 4 5 6 7.

6. `juftlar(int $n)` generatori 0 dan `$n` gacha bo'lgan faqat **juft** sonlarni bersin. `juftlar(10)` -> 0 2 4 6 8 10.

7. Avvalgi `diapazon` generatoriga `$qadam` (step) parametrini qo'shing: `diapazon(0, 10, 2)` -> 0 2 4 6 8 10.

8. `kvadratlar(int $n)` generatori 1 dan `$n` gacha sonlarning kvadratini `yield key => value` bilan bersin, kalit — son, qiymat — kvadrat. `kvadratlar(4)` -> `1=>1, 2=>4, 3=>9, 4=>16`.

9. `iterator_to_array` yordamida 1 dan 5 gacha sonlar generatorini massivga aylantiring va `array_sum` bilan yig'indisini toping (natija: 15).

**Qiyin**

10. `katta_fayl_oqi(string $yol)` generatori yozing: u faylni qator-qator `yield` qilsin (oxiridagi `\n`ni `rtrim` bilan olib tashlang). `try/finally` bilan faylni yoping. Avval test fayl yasab, keyin generator bilan o'qing.

11. `cheksiz_uchlar()` generatori 3 ning karralilarini cheksiz bersin (3, 6, 9, 12, ...). `foreach` va `break` bilan dastlabki 5 tasini chiqaring.

12. `Stack` (stek) klassi yozing — u `Iterator` interfeysini amalga oshirsin. `push(qiymat)` metodi element qo'shsin; `foreach` esa elementlarni **oxirgidan birinchisigacha** (LIFO — last in, first out) tartibida chiqarsin.

13. `Kutubxona` klassi yozing — u `IteratorAggregate` ni amalga oshirsin. Ichida kitoblar massivi bo'lsin; `getIterator()` faqat **mavjud** (`omborda => true`) kitoblarni `yield` qilsin (filtrlash).

14. `fibonachchigacha(int $chegara)` generatori Fibonachchi sonlarini `$chegara`dan oshmaguncha bersin. `fibonachchigacha(20)` -> 0 1 1 2 3 5 8 13.

<details markdown="1">
<summary>Yechim — 5 (diapazon)</summary>

```php
<?php
function diapazon(int $boshlanish, int $tugash): Generator
{
    for ($i = $boshlanish; $i <= $tugash; $i++) {
        yield $i;
    }
}

foreach (diapazon(3, 7) as $son) {
    echo $son . " ";
}
echo "\n";
// 3 4 5 6 7
```
</details>

<details markdown="1">
<summary>Yechim — 8 (kvadratlar, key => value)</summary>

```php
<?php
function kvadratlar(int $n): Generator
{
    for ($i = 1; $i <= $n; $i++) {
        yield $i => $i * $i;
    }
}

foreach (kvadratlar(4) as $son => $kvadrat) {
    echo "{$son} => {$kvadrat}\n";
}
// 1 => 1
// 2 => 4
// 3 => 9
// 4 => 16
```
Kalit sifatida sonning o'zini, qiymat sifatida kvadratini berdik.
</details>

<details markdown="1">
<summary>Yechim — 10 (katta faylni qator-qator o'qish)</summary>

```php
<?php
// Test fayl yasaymiz
$yol = sys_get_temp_dir() . "/test_log.txt";
file_put_contents($yol, "Birinchi qator\nIkkinchi qator\nUchinchi qator\n");

function katta_fayl_oqi(string $yol): Generator
{
    $f = fopen($yol, "r");
    if ($f === false) {
        throw new RuntimeException("Fayl ochilmadi: {$yol}");
    }
    try {
        while (($qator = fgets($f)) !== false) {
            yield rtrim($qator, "\n");
        }
    } finally {
        fclose($f);
    }
}

foreach (katta_fayl_oqi($yol) as $raqam => $qator) {
    echo "{$raqam}: {$qator}\n";
}
// 0: Birinchi qator
// 1: Ikkinchi qator
// 2: Uchinchi qator
```
`try/finally` fayl albatta yopilishini kafolatlaydi — generator yarim yo'lda to'xtasa ham. Fayl qancha katta bo'lsa ham, xotirada bir vaqtda faqat bitta qator turadi.
</details>

<details markdown="1">
<summary>Yechim — 12 (Stack — Iterator, LIFO)</summary>

```php
<?php
class Stack implements Iterator
{
    private array $elementlar = [];
    private int $pozitsiya = 0;

    public function push(mixed $qiymat): void
    {
        $this->elementlar[] = $qiymat;
    }

    public function rewind(): void
    {
        // oxirgi elementdan boshlaymiz (LIFO)
        $this->pozitsiya = count($this->elementlar) - 1;
    }

    public function valid(): bool
    {
        return $this->pozitsiya >= 0;
    }

    public function current(): mixed
    {
        return $this->elementlar[$this->pozitsiya];
    }

    public function key(): int
    {
        return $this->pozitsiya;
    }

    public function next(): void
    {
        $this->pozitsiya--;   // orqaga qarab yuramiz
    }
}

$stack = new Stack();
$stack->push("Birinchi");
$stack->push("Ikkinchi");
$stack->push("Uchinchi");

foreach ($stack as $element) {
    echo $element . "\n";
}
// Uchinchi
// Ikkinchi
// Birinchi
```
`rewind` oxirgi indeksdan boshlaydi, `next` indeksni kamaytiradi — shuning uchun elementlar teskari (LIFO) tartibda keladi.
</details>

<details markdown="1">
<summary>Yechim — 13 (Kutubxona — IteratorAggregate, filtrlash)</summary>

```php
<?php
class Kutubxona implements IteratorAggregate
{
    private array $kitoblar = [];

    public function qoshish(string $nom, bool $omborda): void
    {
        $this->kitoblar[] = ["nom" => $nom, "omborda" => $omborda];
    }

    public function getIterator(): Generator
    {
        foreach ($this->kitoblar as $kitob) {
            if ($kitob["omborda"]) {        // faqat mavjudlarini
                yield $kitob["nom"];
            }
        }
    }
}

$kutubxona = new Kutubxona();
$kutubxona->qoshish("PHP asoslari", true);
$kutubxona->qoshish("SQL qo'llanma", false);   // omborda yo'q
$kutubxona->qoshish("Algoritmlar", true);

foreach ($kutubxona as $nom) {
    echo "Mavjud: {$nom}\n";
}
// Mavjud: PHP asoslari
// Mavjud: Algoritmlar
```
`getIterator()` ichidagi `if` faqat omborda mavjud kitoblarni `yield` qiladi — filtrlash mantig'i obyekt ichida yashiringan.
</details>

<details markdown="1">
<summary>Yechim — 14 (Fibonachchi chegaragacha)</summary>

```php
<?php
function fibonachchigacha(int $chegara): Generator
{
    [$a, $b] = [0, 1];
    while ($a <= $chegara) {
        yield $a;
        [$a, $b] = [$b, $a + $b];
    }
}

foreach (fibonachchigacha(20) as $son) {
    echo $son . " ";
}
echo "\n";
// 0 1 1 2 3 5 8 13
```
`while ($a <= $chegara)` sharti generatorni 20 dan oshmaguncha to'xtatadi — cheksiz emas, lekin oldindan necha son bo'lishini bilmaymiz.
</details>
