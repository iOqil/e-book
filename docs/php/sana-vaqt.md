# 1.12 Sana va vaqt

[⬅️ Oldingi: 1.11 Muntazam ifodalar (regex)](./regex.md) · [🏠 README](./README.md) · [Keyingi: 1.13 Generatorlar va iteratorlar ➡️](./generatorlar.md)

---

Deyarli har bir ilovada sana va vaqt kerak bo'ladi: "ro'yxatdan o'tgan sana", "buyurtma qachon berilgan", "obunaga necha kun qoldi", "yosh nechada", "muddat o'tib ketdimi". Bularning hammasi — sana-vaqt bilan ishlash. Bir qarashda oson tuyuladi ("shunchaki sana-ku"), lekin amalda bu eng ko'p xato chiqadigan mavzulardan biri: oylar har xil uzunlikda, kabisa (leap) yillar bor, vaqt mintaqalari (timezone) bir-biridan farq qiladi, yoz/qish vaqti almashadi.

Yaxshiyamki PHP'da bu murakkablikni o'z bo'yniga oladigan kuchli vositalar bor. Bu bobda avval eski, soddagina `time()`/`date()` funksiyalarini ko'ramiz (ularni hamma joyda uchratasiz), keyin esa zamonaviy, ishonchli `DateTimeImmutable` obyektiga o'tamiz — bugungi kunda professional kodda aynan shu tavsiya etiladi. Oxirida real misollar: yosh hisoblash, "necha kun qoldi", muddat tekshirish, to'lov rejasi.

### Vaqtni belgi sifatida tasavvur qilish — `time()`

Kompyuter vaqtni qanday saqlaydi? U sanani "11-iyun 2026, soat 14:30" ko'rinishida emas, balki bitta katta son ko'rinishida saqlaydi: **1970-yil 1-yanvar 00:00:00 (UTC)** dan beri o'tgan **soniyalar** soni. Bu son — **Unix timestamp** (Unix vaqt belgisi) deb ataladi.

`time()` aynan shu sonni qaytaradi:

```php
<?php
$hozir = time();
echo $hozir;   // masalan: 1781532600 (ishga tushirgan paytingizga qarab)
```

Bu son odamga hech nima anglatmaydi, lekin kompyuter uchun juda qulay: ikki vaqtni taqqoslash — shunchaki ikki sonni solishtirish; "1 soatdan keyin" — songa `3600` qo'shish (1 soat = 3600 soniya). Sanalarni saqlash va hisoblash uchun ko'pincha aynan shu timestamp ishlatiladi.

### Timestamp'ni o'qishli ko'rinishga aylantirish — `date()`

`date()` esa timestamp (yoki standart holatda — hozirgi vaqt) ni odam o'qiy oladigan matnga aylantiradi. Birinchi parametr — **format** (qanday ko'rinishda chiqarish):

```php
<?php
echo date("Y-m-d");            // 2026-06-11   (yil-oy-kun)
echo "\n";
echo date("d.m.Y H:i:s");      // 11.06.2026 14:30:00
echo "\n";
echo date("H:i");              // 14:30        (faqat soat:daqiqa)
```

Format — bu maxsus harflardan tuzilgan andoza. Har bir harf sananing bir qismini bildiradi. Eng kerakliari:

| Harf | Ma'nosi | Misol |
|------|---------|-------|
| `Y` | yil, 4 xonali | `2026` |
| `y` | yil, 2 xonali | `26` |
| `m` | oy, nol bilan (01-12) | `06` |
| `n` | oy, nolsiz (1-12) | `6` |
| `d` | kun, nol bilan (01-31) | `09` |
| `j` | kun, nolsiz (1-31) | `9` |
| `H` | soat, 24-soatlik (00-23) | `14` |
| `i` | daqiqa (00-59) | `30` |
| `s` | soniya (00-59) | `05` |
| `D` | hafta kuni, qisqa | `Thu` |
| `l` | hafta kuni, to'liq | `Thursday` |
| `N` | hafta kuni raqami (1=dushanba ... 7=yakshanba) | `4` |

Format harflari orasiga istalgan belgini (`-`, `.`, `:`, `/`, bo'sh joy) qo'yishingiz mumkin — ular o'zgarmasdan chiqadi.

Agar aniq bir timestamp'ni formatlash kerak bo'lsa, uni ikkinchi parametr qilib beriladi:

```php
<?php
$timestamp = 1781532600;
echo date("d.m.Y H:i", $timestamp);   // 11.06.2026 14:30
```

> **Diqqat:** format harflari katta-kichikligiga sezgir. `m` (oy) va `M` (oy nomi), `d` (kun) va `D` (hafta kuni) — butunlay boshqa narsalar. Jadvalga qarab tekshirib turing.

### Matndan timestamp yasash — `strtotime()`

Ko'pincha sana matn ko'rinishida keladi (`"2026-06-11"`) yoki "1 hafta keyin" kabi nisbiy ifoda kerak bo'ladi. `strtotime()` — inglizcha yozilgan sana ifodasini timestamp'ga aylantiradigan ajoyib funksiya:

```php
<?php
echo date("d.m.Y", strtotime("2026-12-31"));        // 31.12.2026
echo "\n";
echo date("d.m.Y", strtotime("+1 day"));            // ertaga
echo "\n";
echo date("d.m.Y", strtotime("+1 week"));           // 1 haftadan keyin
echo "\n";
echo date("d.m.Y", strtotime("-3 months"));         // 3 oy oldin
echo "\n";
echo date("d.m.Y", strtotime("first day of next month"));  // keyingi oyning 1-kuni
echo "\n";
echo date("d.m.Y", strtotime("next monday"));       // keyingi dushanba
```

`strtotime` tushunadigan ifodalar (inglizcha): `+1 day`, `-2 weeks`, `+3 hours`, `tomorrow`, `yesterday`, `next friday`, `last day of this month`. Sodda hisob-kitoblar uchun juda qulay. Lekin murakkabroq, ishonchli ishlar uchun quyida ko'radigan `DateTimeImmutable` obyektidan foydalanish ma'qul.

> **Ogohlantirish:** `strtotime` xatoda `false` qaytaradi. Masalan, `strtotime("buncha-bemaza-matn")` natijasi `false` bo'ladi. Shuning uchun foydalanuvchi kiritgan sanaga ishonib bo'lmaydi — har doim natijani tekshiring (`if ($t === false) { ... }`).

### Zamonaviy yo'l — `DateTime` va `DateTimeImmutable`

`date()`/`strtotime()` — sodda, lekin cheklangan: ular shunchaki son va matn bilan ishlaydi. Murakkab hisoblar (sanalar farqi, oraliqlar, vaqt mintaqalari) uchun PHP **obyektga asoslangan** yondashuvni taklif qiladi — sana butun bir **obyekt** bo'lib, uning ichida metodlar bor.

Ikkita asosiy class bor:

- **`DateTime`** — o'zgaruvchan (mutable). Metodlari (`->add()`, `->modify()`) obyektning **o'zini o'zgartiradi**.
- **`DateTimeImmutable`** — o'zgarmas (immutable). Metodlari obyektni o'zgartirmaydi, balki **yangi obyekt qaytaradi**.

Bugungi tavsiya — **har doim `DateTimeImmutable`'dan foydalaning**. Nega — pastda "tuzoq" bo'limida ko'rasiz. Hozircha shuni bilib oling: ikkalasining ishlash usuli bir xil, faqat o'zgaruvchanligi farq qiladi.

Obyekt yaratish — `new`, qavs ichida sana matni (bo'sh qoldirilsa — hozirgi vaqt):

```php
<?php
$hozir = new DateTimeImmutable();              // hozirgi sana-vaqt
$sana = new DateTimeImmutable("2026-06-11");   // aniq sana
$toliq = new DateTimeImmutable("2026-06-11 14:30:00");

echo $sana->format("d.m.Y");        // 11.06.2026
echo "\n";
echo $hozir->format("Y-m-d H:i");   // hozirgi vaqt
```

E'tibor bering: obyektni chiroyli matnga aylantirish uchun yana o'sha format harflaridan foydalanamiz, faqat endi `->format()` **metodi** orqali. `date()` da o'rgangan barcha harflar (`Y`, `m`, `d`, `H`, `i`...) shu yerda ham ishlaydi.

### Vaqt mintaqasi — `DateTimeZone` (O'zbekiston uchun muhim!)

Server qaysi mamlakatda turgani bo'yicha vaqt har xil bo'ladi. Server London'da bo'lsa, `time()` London vaqtini, Toshkent'da bo'lsa — Toshkent vaqtini beradi. Buni aniq nazorat qilish uchun **vaqt mintaqasini** (timezone) o'zimiz belgilaymiz.

O'zbekiston uchun mintaqa nomi — **`Asia/Tashkent`** (UTC+5):

```php
<?php
$mintaqa = new DateTimeZone("Asia/Tashkent");
$hozir = new DateTimeImmutable("now", $mintaqa);

echo $hozir->format("d.m.Y H:i");   // Toshkent vaqti bilan hozir
echo "\n";
echo $hozir->format("P");           // +05:00  (UTC dan farqi)
```

Bitta vaqtni boshqa mintaqada ko'rsatish (masalan, Toshkent vaqtini London vaqtiga aylantirish):

```php
<?php
$toshkent = new DateTimeImmutable("2026-06-11 14:00", new DateTimeZone("Asia/Tashkent"));
$london = $toshkent->setTimezone(new DateTimeZone("Europe/London"));

echo $toshkent->format("H:i");   // 14:00
echo "\n";
echo $london->format("H:i");     // 10:00  (London 5 soat orqada)
```

Diqqat: bu yerda asl `$toshkent` obyekti **o'zgarmadi** — `setTimezone()` yangi obyekt qaytardi (chunki bu `Immutable`). Aynan shu xavfsizlik immutable'ning asosiy afzalligi.

> **Maslahat:** butun loyiha uchun standart mintaqani bir marta belgilash mumkin — fayl boshida `date_default_timezone_set("Asia/Tashkent");`. Shundan keyin `time()`, `date()` va obyektlar — hammasi Toshkent vaqtida ishlaydi.

### Vaqt oralig'i — `DateInterval`

"3 kun", "2 oy", "1 yil 6 oy", "45 daqiqa" kabi **muddatlar** alohida obyekt bilan ifodalanadi — `DateInterval`. Uni yaratish uchun maxsus matn beriladi, u **ISO 8601 davriy format** deb ataladi va qoidasi shunday:

- `P` harfi bilan boshlanadi (Period — davr).
- Sana qismi: `Y` (yil), `M` (oy), `D` (kun), `W` (hafta).
- Vaqt qismidan oldin `T` harfi (Time), keyin: `H` (soat), `M` (daqiqa), `S` (soniya).

```php
<?php
$uchKun = new DateInterval("P3D");        // 3 kun
$ikkiOy = new DateInterval("P2M");        // 2 oy
$murakkab = new DateInterval("P1Y2M10D"); // 1 yil 2 oy 10 kun
$birYarimSoat = new DateInterval("PT1H30M"); // 1 soat 30 daqiqa
```

> **Eslab qoling:** `M` ikki ma'noda keladi — `T` dan **oldin** bo'lsa oy (Month), `T` dan **keyin** bo'lsa daqiqa (Minute). Shuning uchun "30 daqiqa" — `PT30M`, "2 oy" esa — `P2M`. `T` chegarani belgilaydi.

Endi bu muddatni sanaga qo'shamiz yoki ayiramiz — `->add()` va `->sub()`:

```php
<?php
$sana = new DateTimeImmutable("2026-06-11");

$keyin = $sana->add(new DateInterval("P10D"));   // 10 kun keyin
$oldin = $sana->sub(new DateInterval("P1M"));    // 1 oy oldin

echo $keyin->format("d.m.Y");   // 21.06.2026
echo "\n";
echo $oldin->format("d.m.Y");   // 11.05.2026
echo "\n";
echo $sana->format("d.m.Y");    // 11.06.2026  (asl o'zgarmadi!)
```

E'tibor bering — `$sana` o'zgarmadi. `add` va `sub` yangi obyekt qaytardi. Bu — `Immutable`ning kuchi.

### Ikki sana orasidagi farq — `diff()`

Eng ko'p kerak bo'ladigan amal: ikki sana o'rtasida qancha vaqt bor? `diff()` metodi ikki sanani solishtirib, natijani `DateInterval` ko'rinishida qaytaradi:

```php
<?php
$boshlanish = new DateTimeImmutable("2026-01-01");
$tugash = new DateTimeImmutable("2026-06-11");

$farq = $boshlanish->diff($tugash);

echo $farq->y;      // 0   (yillar)
echo "\n";
echo $farq->m;      // 5   (oylar)
echo "\n";
echo $farq->d;      // 10  (kunlar)
echo "\n";
echo $farq->days;   // 161 (JAMI kunlar soni)
```

Bu yerda ikki xil narsa borligini yaxshi tushunib oling:

- `->y`, `->m`, `->d` — farqning **parchalangan** ko'rinishi: "0 yil, 5 oy, 10 kun".
- `->days` — farqning **jami kunlardagi** ko'rinishi: 161 kun. "Necha kun qoldi" kabi savollar uchun aynan shu kerak.

`DateInterval`ni chiroyli matnga aylantirish uchun `->format()` ham bor (lekin bu yerda format harflari `%` bilan yoziladi):

```php
<?php
$farq = (new DateTimeImmutable("2026-01-01"))->diff(new DateTimeImmutable("2026-06-11"));
echo $farq->format("%y yil, %m oy, %d kun");   // 0 yil, 5 oy, 10 kun
```

`diff` natijasida `->invert` xususiyati ham bor: agar ikkinchi sana birinchisidan oldin bo'lsa, `->invert` qiymati `1` bo'ladi (farq "manfiy", ya'ni o'tmishga qarab). Buni muddat o'tib ketganini aniqlashda ishlatamiz.

### Sanalarni taqqoslash

`DateTime` va `DateTimeImmutable` obyektlarini bevosita `<`, `>`, `==`, `>=` belgilari bilan taqqoslash mumkin — PHP ularni avtomatik to'g'ri solishtiradi:

```php
<?php
$muddat = new DateTimeImmutable("2026-12-31");
$hozir = new DateTimeImmutable();   // bugun

if ($hozir < $muddat) {
    echo "Muddat hali o'tmagan";
} elseif ($hozir > $muddat) {
    echo "Muddat o'tib ketgan";
} else {
    echo "Aynan bugun tugaydi";
}
```

Bu — sana tekshiruvining eng tabiiy yo'li. Timestamp solishtirishga qaraganda ancha o'qishli: `if ($hozir < $muddat)` o'zini o'zi tushuntiradi.

### Matndan aniq formatda o'qish — `createFromFormat()`

Foydalanuvchi sanani `"11/06/2026"` yoki `"11-06-2026"` ko'rinishida kiritsa-chi? Oddiy `new DateTimeImmutable("11/06/2026")` bunday formatlarda chalkashadi (kun-oymi yoki oy-kunmi — bilmaydi). Bunday holatda **aniq formatni o'zimiz aytib beramiz** — `createFromFormat()`:

```php
<?php
$sana = DateTimeImmutable::createFromFormat("d/m/Y", "11/06/2026");
echo $sana->format("Y-m-d");   // 2026-06-11

$boshqa = DateTimeImmutable::createFromFormat("d-m-Y H:i", "31-12-2026 23:59");
echo "\n";
echo $boshqa->format("d.m.Y H:i");   // 31.12.2026 23:59
```

Bu yerda birinchi parametr — kirayotgan matn **qanday formatda** ekani (o'sha tanish harflar), ikkinchisi — matnning o'zi. Bu usul foydalanuvchi kiritgan sanalarni xavfsiz o'qishning eng to'g'ri yo'li.

Agar matn formatga mos kelmasa, metod `false` qaytaradi — shuni tekshirish kerak:

```php
<?php
$natija = DateTimeImmutable::createFromFormat("d/m/Y", "bemaza");

if ($natija === false) {
    echo "Sana formati noto'g'ri!";
} else {
    echo $natija->format("Y-m-d");
}
```

### Tuzoq: mutable (`DateTime`) vs immutable (`DateTimeImmutable`)

Endi eng muhim amaliy maslahatga keldik. Quyidagi kodga qarang va natijani taxmin qiling:

```php
<?php
// ❌ XATO TUSHUNCHA: DateTime o'zgaruvchan!
$boshlanish = new DateTime("2026-06-11");
$tugash = $boshlanish->add(new DateInterval("P7D"));

echo "Boshlanish: " . $boshlanish->format("d.m.Y") . "\n";
echo "Tugash:     " . $tugash->format("d.m.Y") . "\n";
```

Ko'pchilik `$boshlanish` 11-iyun, `$tugash` esa 18-iyun bo'ladi deb o'ylaydi. Aslida natija:

```
Boshlanish: 18.06.2026
Tugash:     18.06.2026
```

Ikkalasi ham 18-iyun! Sababi: `DateTime`'da `add()` **asl obyektni o'zgartirib yuboradi** va o'sha o'zgargan obyektga havola qaytaradi. Ya'ni `$boshlanish` va `$tugash` — bitta obyektga ishora qiladi. Boshlanish sanasini yo'qotib qo'ydik.

Endi xuddi shu kod, lekin `DateTimeImmutable` bilan:

```php
<?php
// ✅ TO'G'RI: DateTimeImmutable o'zgarmaydi
$boshlanish = new DateTimeImmutable("2026-06-11");
$tugash = $boshlanish->add(new DateInterval("P7D"));

echo "Boshlanish: " . $boshlanish->format("d.m.Y") . "\n";   // 11.06.2026
echo "Tugash:     " . $tugash->format("d.m.Y") . "\n";       // 18.06.2026
```

Endi to'g'ri: boshlanish — 11-iyun, tugash — 18-iyun. `Immutable` obyekt o'zgarmadi, `add` esa yangi obyekt qaytardi.

> **Oltin qoida:** **har doim `DateTimeImmutable` ishlating.** Shunda "qayerdadir sanam o'zgarib ketibdi" degan, topilishi qiyin xatolardan butunlay xalos bo'lasiz. `DateTime`'ni faqat eski kodlarda uchratganingizda taniydigan darajada bilsangiz kifoya.

### Real misol — yosh hisoblash

Tug'ilgan sanadan to'liq yoshni (necha yil) hisoblash. `diff` natijasidagi `->y` aynan to'liq yillarni beradi (oy va kunni hisobga olib):

```php
<?php
function yoshHisobla(string $tugilganSana): int
{
    $tugilgan = new DateTimeImmutable($tugilganSana);
    $bugun = new DateTimeImmutable();

    return $tugilgan->diff($bugun)->y;
}

echo yoshHisobla("2000-01-15");   // masalan: 26
echo "\n";
echo yoshHisobla("2010-12-31");   // masalan: 15
```

`->y` to'liq yillarni beradi: agar tug'ilgan kun bu yil hali kelmagan bo'lsa, yosh avtomatik 1 ga kam bo'ladi — `diff` buni o'zi to'g'ri hisoblaydi. Shuning uchun yoshni "joriy yil minus tug'ilgan yil" deb hisoblash xato — `diff` aniq ishlaydi.

### Real misol — "necha kun qoldi"

Biror voqea (bayram, imtihon, muddat) gacha necha kun qolganini topish:

```php
<?php
function kunQoldi(string $maqsadSana): int
{
    $bugun = new DateTimeImmutable("today");   // bugun, soat 00:00
    $maqsad = new DateTimeImmutable($maqsadSana);

    return (int) $bugun->diff($maqsad)->format("%r%a");
}

echo kunQoldi("2026-12-31") . " kun qoldi\n";   // masalan: 203 kun qoldi
echo kunQoldi("2026-01-01") . " kun (manfiy = o'tib ketgan)\n";  // masalan: -161
```

Bu yerda kichik hiyla bor: `%a` — jami kunlar, `%r` esa — agar sana o'tmishda bo'lsa minus belgisi qo'yadi. Shu tufayli funksiya kelajakdagi sana uchun musbat, o'tib ketgan sana uchun manfiy son qaytaradi. `"today"` ishlatdik (`"now"` emas), chunki soat-daqiqa kunlar sanog'iga xalaqit bermasligi kerak.

### Real misol — muddat o'tganmi?

Obuna, parol amal qilish muddati, aksiya tugashi — ko'p joyda "muddat o'tdimi yoki yo'q" kerak. Bu — oddiy taqqoslash:

```php
<?php
function muddatOtganmi(string $tugashSana): bool
{
    $hozir = new DateTimeImmutable();
    $tugash = new DateTimeImmutable($tugashSana);

    return $hozir > $tugash;   // hozir tugash sanasidan keyinmi?
}

var_dump(muddatOtganmi("2020-01-01"));   // bool(true)  — o'tib ketgan
var_dump(muddatOtganmi("2030-01-01"));   // bool(false) — hali bor
```

### Real misol — sanani o'zbekcha formatlash

`date()`/`format()` oy nomlarini faqat inglizcha beradi (`June`, `December`). O'zbekcha chiqarish uchun oy raqamini o'zimiz nomga aylantiramiz:

```php
<?php
function ozbekchaSana(DateTimeImmutable $sana): string
{
    $oylar = [
        1 => "yanvar", 2 => "fevral", 3 => "mart", 4 => "aprel",
        5 => "may", 6 => "iyun", 7 => "iyul", 8 => "avgust",
        9 => "sentabr", 10 => "oktabr", 11 => "noyabr", 12 => "dekabr",
    ];

    $kun = (int) $sana->format("j");         // 11
    $oyRaqami = (int) $sana->format("n");    // 6
    $yil = $sana->format("Y");               // 2026

    return "{$kun}-{$oylar[$oyRaqami]} {$yil}-yil";
}

echo ozbekchaSana(new DateTimeImmutable("2026-06-11"));   // 11-iyun 2026-yil
echo "\n";
echo ozbekchaSana(new DateTimeImmutable("2026-12-31"));   // 31-dekabr 2026-yil
```

Oy raqamini massivdagi o'zbekcha nomga moslab, ismni o'zimiz quramiz. Hafta kunlarini ham xuddi shunday massiv bilan o'zbekchalashtirish mumkin (`N` formati 1-7 raqamni beradi).

### Real misol — ikki sana orasidagi barcha kunlar — `DatePeriod`

Ba'zan ikki sana **orasidagi har bir kunni** birma-bir aylanib chiqish kerak bo'ladi (masalan, taqvim chizish yoki har kunlik hisobot). `DatePeriod` — boshlanish, qadam (`DateInterval`) va tugash beriladi, u esa har bir nuqtani beradi:

```php
<?php
$boshlanish = new DateTimeImmutable("2026-06-11");
$tugash = new DateTimeImmutable("2026-06-15");
$birKun = new DateInterval("P1D");

// tugash sanasini ham qo'shish uchun unga 1 kun qo'shamiz
$davr = new DatePeriod($boshlanish, $birKun, $tugash->add($birKun));

foreach ($davr as $kun) {
    echo $kun->format("d.m.Y (l)") . "\n";
}
// 11.06.2026 (Thursday)
// 12.06.2026 (Friday)
// 13.06.2026 (Saturday)
// 14.06.2026 (Sunday)
// 15.06.2026 (Monday)
```

`DatePeriod` standart holatda tugash sanasini **o'z ichiga olmaydi** (oxirgi kunni chiqarmaydi), shuning uchun yuqorida tugash sanasiga bir kun qo'shdik. Bu — taqvim, band kunlar, kunlik statistika kabi vazifalarda juda foydali.

### Mashqlar

**Oson**

1. `date()` bilan bugungi sanani `kun.oy.yil` (`11.06.2026`) ko'rinishida chiqaring.
2. `date()` bilan hozirgi soat va daqiqani (`H:i`) chiqaring.
3. `time()` qiymatini chiqaring va u nima ekanini bir gapda izohlang (kommentariyada).
4. `strtotime("+1 week")` natijasini `date()` bilan o'qishli sanaga aylantirib chiqaring (1 haftadan keyingi sana).
5. `new DateTimeImmutable("2026-12-31")` obyektini yaratib, `->format()` bilan `31.12.2026` ko'rinishida chiqaring.

**O'rta**

6. Tug'ilgan sanangizni bering va `diff` yordamida to'liq yoshingizni (necha yil) hisoblang.
7. Ikki sana (`2026-01-01` va `2026-06-11`) orasidagi **jami kunlar** sonini (`->days`) chiqaring.
8. Bugundan boshlab `DateInterval("P100D")` qo'shib, "100 kundan keyin qaysi sana bo'ladi" ni toping.
9. `Asia/Tashkent` mintaqasida hozirgi vaqtni va uning UTC dan farqini (`P` formati) chiqaring.
10. `createFromFormat` bilan `"25/12/2026"` (kun/oy/yil) matnini o'qib, `Y-m-d` formatida chiqaring.

**Qiyin**

11. Funksiya yozing: `muddatHolati(string $tugash): string` — agar muddat o'tib ketgan bo'lsa `"O'tib ketgan"`, bugun bo'lsa `"Bugun tugaydi"`, kelajakda bo'lsa `"Yana N kun bor"` qaytarsin.
12. "Necha kun qoldi" funksiyasini yozing: yangi yilgacha (`keyingi yil 1-yanvar`) necha kun qolganini toping. (Maslahat: `strtotime("first day of january next year")` yoki `DateTimeImmutable` ishlating.)
13. `DateTimeImmutable` bilan to'lov rejasi tuzing: boshlanish sanasidan boshlab, har oyda bir martadan, 6 oylik to'lov sanalarini chiqaring (`->add(new DateInterval("P1M"))` ni takror ishlatib). Asl boshlanish sanasi o'zgarmasligiga e'tibor bering.
14. Funksiya yozing: berilgan sana **dam olish kuni** (shanba yoki yakshanba) ekanmi tekshirsin (`N` formati 6 yoki 7 bo'lsa — dam olish).
15. Berilgan ikki sana orasidagi **ish kunlari** (dushanba-juma) sonini hisoblang. `DatePeriod` bilan har kunni aylanib, dam olish kunlarini chiqarib tashlang.

<details markdown="1">
<summary>Yechim — 6 (yosh hisoblash)</summary>

```php
<?php
$tugilgan = new DateTimeImmutable("2000-01-15");
$bugun = new DateTimeImmutable();

$yosh = $tugilgan->diff($bugun)->y;
echo "Yosh: {$yosh}";
```

`diff` ikki sana farqini beradi, `->y` esa to'liq yillar sonini. Tug'ilgan kun bu yil hali kelmagan bo'lsa, `diff` yoshni avtomatik bittaga kam hisoblaydi — qo'lda tuzatish shart emas.
</details>

<details markdown="1">
<summary>Yechim — 8 (100 kundan keyin)</summary>

```php
<?php
$bugun = new DateTimeImmutable("today");
$keyin = $bugun->add(new DateInterval("P100D"));

echo "Bugun:        " . $bugun->format("d.m.Y") . "\n";
echo "100 kun keyin: " . $keyin->format("d.m.Y") . "\n";
```

`add` yangi obyekt qaytargani uchun `$bugun` o'zgarmadi — ikkala sanani ham bemalol chiqara olamiz.
</details>

<details markdown="1">
<summary>Yechim — 11 (muddat holati)</summary>

```php
<?php
function muddatHolati(string $tugash): string
{
    $bugun = new DateTimeImmutable("today");
    $sana = new DateTimeImmutable($tugash);

    if ($bugun > $sana) {
        return "O'tib ketgan";
    }

    if ($bugun == $sana) {
        return "Bugun tugaydi";
    }

    $qolgan = $bugun->diff($sana)->days;
    return "Yana {$qolgan} kun bor";
}

echo muddatHolati("2020-01-01") . "\n";   // O'tib ketgan
echo muddatHolati("2030-06-11") . "\n";   // Yana NNNN kun bor
```

Avval taqqoslash bilan uch holatni ajratdik (o'tgan / bugun / kelajak), keyin kelajak uchun `diff(...)->days` bilan qolgan kunlarni sanadik. `"today"` ishlatdik, chunki soat-daqiqa taqqoslashga xalaqit bermasligi kerak.
</details>

<details markdown="1">
<summary>Yechim — 12 (yangi yilgacha necha kun)</summary>

```php
<?php
$bugun = new DateTimeImmutable("today");
$yangiYil = new DateTimeImmutable("first day of january next year");

$kun = $bugun->diff($yangiYil)->days;
echo "Yangi yilgacha {$kun} kun qoldi";
```

`"first day of january next year"` — keyingi yilning 1-yanvariga to'g'ri keladi. `diff(...)->days` esa oradagi kunlarni sanaydi.
</details>

<details markdown="1">
<summary>Yechim — 13 (to'lov rejasi)</summary>

```php
<?php
function tolovRejasi(string $boshlanish, int $oylarSoni): array
{
    $sana = new DateTimeImmutable($boshlanish);
    $birOy = new DateInterval("P1M");
    $rejalar = [];

    for ($i = 0; $i < $oylarSoni; $i++) {
        $tolovSana = $sana->add(new DateInterval("P{$i}M"));
        $rejalar[] = $tolovSana->format("d.m.Y");
    }

    return $rejalar;
}

$reja = tolovRejasi("2026-06-11", 6);
foreach ($reja as $n => $sana) {
    echo ($n + 1) . "-to'lov: {$sana}\n";
}
// 1-to'lov: 11.06.2026
// 2-to'lov: 11.07.2026
// 3-to'lov: 11.08.2026
// 4-to'lov: 11.09.2026
// 5-to'lov: 11.10.2026
// 6-to'lov: 11.11.2026
```

Bu yerda `$sana` (asl boshlanish) hech qachon o'zgarmaydi — har safar undan **yangi** obyekt yasaymiz (`$sana->add(...)`). Aynan shu `Immutable`ning afzalligi: asl nuqtani yo'qotmaymiz. Agar `DateTime` ishlatganimizda, har bir `add` boshlanishni surib yuborib, hisob chalkashardi.

> **Diqqat — oylik qo'shishdagi nozik holat:** `P1M` "bir oy keyin" degani, lekin oylar har xil uzunlikda. Masalan, 31-yanvarga 1 oy qo'shsangiz, fevralda 31-kun yo'qligi sababli sana 3-martga "oshib" ketishi mumkin. Aniq sana muhim bo'lgan moliyaviy ilovalarda buni alohida tekshirish kerak. Bizning misolda boshlanish 11-kun bo'lgani uchun muammo chiqmaydi.
</details>

<details markdown="1">
<summary>Yechim — 14 (dam olish kunimi)</summary>

```php
<?php
function damOlishKunimi(string $sana): bool
{
    $kun = (int) (new DateTimeImmutable($sana))->format("N");
    // N: 1=dushanba ... 6=shanba, 7=yakshanba
    return $kun === 6 || $kun === 7;
}

var_dump(damOlishKunimi("2026-06-13"));   // bool(true)  — shanba
var_dump(damOlishKunimi("2026-06-11"));   // bool(false) — payshanba
```

`N` formati hafta kunini raqam qilib beradi (1—dushanba, 7—yakshanba). 6 yoki 7 bo'lsa — dam olish.
</details>

<details markdown="1">
<summary>Yechim — 15 (ish kunlari soni)</summary>

```php
<?php
function ishKunlari(string $boshlanish, string $tugash): int
{
    $b = new DateTimeImmutable($boshlanish);
    $t = new DateTimeImmutable($tugash);
    $birKun = new DateInterval("P1D");

    // tugash kunini ham hisobga olish uchun +1 kun
    $davr = new DatePeriod($b, $birKun, $t->add($birKun));

    $son = 0;
    foreach ($davr as $kun) {
        $hafta = (int) $kun->format("N");
        if ($hafta <= 5) {   // 1-5 = dushanba-juma
            $son++;
        }
    }

    return $son;
}

echo ishKunlari("2026-06-11", "2026-06-17") . " ta ish kuni\n";
// 11(pay) 12(jum) 15(dush) 16(sesh) 17(chor) = 5 ta (13-shan, 14-yak chiqdi)
```

`DatePeriod` bilan har bir kunni aylanib chiqdik; `N` formati 1-5 (dushanba-juma) bo'lganlarni sanadik, 6-7 (dam olish) larni tashlab ketdik. Tugash kunini ham qamrab olish uchun davr oxiriga bir kun qo'shdik.
</details>
