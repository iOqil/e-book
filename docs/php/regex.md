# 1.11 Muntazam ifodalar (regex)

[⬅️ Oldingi: 1.10 Anonim funksiyalar va massiv vositalari (map / filter / reduce)](./13-anonim-funksiyalar-va-massiv-vosital.md) · [🏠 README](./README.md) · [Keyingi: 1.12 Sana va vaqt ➡️](./sana-vaqt.md)

---

Tasavvur qiling: ro'yxatdan o'tish formangiz bor va foydalanuvchi email kiritdi. Bu haqiqiy emailmi? Telefon raqami `+998` bilan boshlanyaptimi va to'g'ri uzunlikdami? Parol yetarlicha kuchlimi? Katta matn ichidan barcha hashtag'larni ajratib olish kerakmi? Bularning hammasini oddiy `str_contains` yoki `substr` bilan qilish — azob: har bir holatni qo'lda tekshirish kerak bo'ladi.

Mana shu yerda **regex** (regular expression — muntazam ifoda) yordamga keladi. Regex — bu matn **naqshini** (qolipini) tasvirlaydigan maxsus til. Siz "menga shunaqa ko'rinishdagi matn kerak" deysiz, regex esa matn shu naqshga mos keladimi-yo'qmi aytadi yoki mos kelgan qismlarini topib beradi.

Analogiya: regex — bu "qidiruvning superkuchli versiyasi". Oddiy qidiruvda aniq so'zni qidirasiz (`"olma"`). Regex'da esa qoidani qidirasiz: "uchta raqam, keyin chiziqcha, keyin yana ikkita raqam". Bitta naqsh minglab turli matnlarga mos kelishi mumkin.

PHP'da regex bilan ishlash uchun **PCRE** (Perl Compatible Regular Expressions — Perl tiliga mos muntazam ifodalar) deb ataladigan funksiyalar to'plami bor. Ularning nomi `preg_` bilan boshlanadi: `preg_match`, `preg_match_all`, `preg_replace`, `preg_split`. Shu bobda ularni chuqur o'rganamiz.

> **Ogohlantirish:** regex kuchli, lekin har doim ham kerak emas. Email yoki URL tekshirish uchun PHP'da tayyor `filter_var` vositasi bor (bob oxirida ko'ramiz) — u regex'dan ko'ra ishonchliroq. Regex'ni o'z naqshlaringiz uchun (telefon formati, mahsulot kodi, sana) ishlating.

### Birinchi tekshiruv — `preg_match`

`preg_match` — eng asosiy funksiya. U "matn ushbu naqshga mos keladimi?" degan savolga javob beradi. Mos kelsa `1`, kelmasa `0` qaytaradi (xatolik bo'lsa `false`).

```php
<?php
$matn = "Salom dunyo";

// Matn ichida "dunyo" so'zi bormi?
$natija = preg_match('/dunyo/', $matn);

var_dump($natija);   // int(1)  — topildi
```

Birinchi argument — **naqsh** (pattern), ikkinchisi — tekshiriladigan **matn**. Naqsh ikki tomonidan `/` belgisi bilan o'ralgan — bu **delimiter** (ajratgich, naqshning chegarasi). Delimiter haqida birozdan keyin batafsil gaplashamiz.

Odatda `preg_match` ni `if` ichida ishlatamiz, chunki `1` — `true`, `0` — `false` deb qabul qilinadi:

```php
<?php
$matn = "Salom dunyo";

if (preg_match('/dunyo/', $matn)) {
    echo "Topildi!";
} else {
    echo "Topilmadi.";
}
// Natija: Topildi!
```

> **Muhim farq:** `str_contains($matn, "dunyo")` ham xuddi shu ishni qiladi va tezroq. Oddiy so'zni qidirayotgan bo'lsangiz, `str_contains` ishlating. Regex'ning kuchi — naqsh (raqamlar, harflar, formatlar) qidirishda namoyon bo'ladi.

### Naqsh chegarasi — delimiter `/.../`

Har bir regex naqshi ikki tomonidan bir xil belgi bilan o'ralishi shart. Eng ko'p ishlatiladigani — `/`:

```php
<?php
preg_match('/abc/', $matn);   // /.../ — eng keng tarqalgan delimiter
```

Lekin agar naqsh ichida `/` belgisi ko'p bo'lsa (masalan, sana `2026/06/11` yoki URL), uni har safar ekranlash (`\/`) noqulay. Shunda boshqa delimiter tanlash mumkin — masalan `#` yoki `~`:

```php
<?php
$sana = "2026/06/11";

// / o'rniga # delimiter ishlatamiz — endi naqsh ichidagi / ni ekranlash shart emas
if (preg_match('#\d{4}/\d{2}/\d{2}#', $sana)) {
    echo "Sana formati to'g'ri";
}
// Natija: Sana formati to'g'ri
```

Delimiter sifatida harf, raqam yoki bo'sh joydan tashqari deyarli har qanday belgi ishlatish mumkin (`/`, `#`, `~`, `!`, `@`). Kitobning qolgan qismida asosan `/` ishlatamiz, lekin `/` ko'p bo'lganda `#` ga o'tishni eslab qoling.

### Bog'lagichlar (anchor) — `^` va `$`

Hozircha naqshlarimiz matnning **istalgan qismida** moslik qidirardi. Ko'pincha esa biz "matn to'liq shu naqshga mos kelsinmi?" deb tekshirmoqchi bo'lamiz. Buning uchun ikki **anchor** (bog'lagich) bor:

- `^` — matnning **boshi**
- `$` — matnning **oxiri**

```php
<?php
// "salom" SO'ZI bormi (istalgan joyda)?
var_dump(preg_match('/salom/', "men salom dedim"));   // int(1)

// Matn AYNAN "salom" dan boshlanyaptimi?
var_dump(preg_match('/^salom/', "salom dunyo"));      // int(1)
var_dump(preg_match('/^salom/', "men salom dedim"));  // int(0) — boshida emas

// Matn AYNAN "salom" bilan tugayaptimi?
var_dump(preg_match('/salom$/', "men salom"));        // int(1)
```

Eng muhimi — `^` va `$` ni birga ishlatib, **butun matnni** tekshirish. Bu validatsiyada doimo kerak bo'ladi:

```php
<?php
// Matn FAQAT "ha" yoki boshqa hech narsa bo'lmagan holdami?
var_dump(preg_match('/^ha$/', "ha"));          // int(1) — aynan "ha"
var_dump(preg_match('/^ha$/', "ha mayli"));    // int(0) — ortiqcha matn bor
```

> **Qoida:** validatsiyada (email, telefon to'g'rimi) deyarli har doim `^...$` ishlating. Aks holda foydalanuvchi `ali@mail.com BLA BLA` deb yozsa ham "to'g'ri" deb o'tib ketadi.

### Belgi sinflari — `[...]`

`[...]` — **belgi sinfi** (character class). U "shu belgilardan **bittasi**" degani. Masalan, `[abc]` — a yoki b yoki c.

```php
<?php
// "kat" yoki "kot" yoki "kit" — ikkinchi harf a, o yoki i bo'lsin
var_dump(preg_match('/^k[aoi]t$/', "kot"));   // int(1)
var_dump(preg_match('/^k[aoi]t$/', "ket"));   // int(0) — e yo'q ro'yxatda
```

Belgilar **oralig'ini** `-` bilan beramiz — bu juda foydali:

```php
<?php
// [a-z] — kichik lotin harflari
// [A-Z] — katta lotin harflari
// [0-9] — raqamlar
var_dump(preg_match('/^[a-z]$/', "g"));   // int(1)
var_dump(preg_match('/^[0-9]$/', "7"));   // int(1)
var_dump(preg_match('/^[0-9]$/', "x"));   // int(0)
```

Oraliqlarni birlashtirish ham mumkin: `[a-zA-Z0-9]` — istalgan harf yoki raqam.

### Sinfni inkor qilish — `[^...]`

Belgi sinfi ichida birinchi belgi `^` bo'lsa, ma'no **teskari**ga aylanadi: "shu belgilardan tashqari istalgan biri".

```php
<?php
// [^0-9] — raqam BO'LMAGAN istalgan belgi
var_dump(preg_match('/[^0-9]/', "12345"));   // int(0) — hammasi raqam, raqammas belgi yo'q
var_dump(preg_match('/[^0-9]/', "123a45"));  // int(1) — 'a' raqammas, topildi
```

> **Diqqat:** `^` belgisi ikki xil ma'noga ega! Sinf **ichida** birinchi o'rinda (`[^...]`) — inkor. Sinfdan **tashqarida** (`^salom`) — matn boshi. Joylashuviga qarab farqlang.

### Tayyor qisqartmalar — `\d \w \s`

Eng ko'p ishlatiladigan belgi sinflari uchun qisqa yozuvlar mavjud. Ularni eslab qolish kerak:

| Qisqartma | Ma'nosi | Teng | 
|-----------|---------|------|
| `\d` | raqam (digit) | `[0-9]` |
| `\w` | so'z belgisi (word): harf, raqam, pastki chiziq | `[a-zA-Z0-9_]` |
| `\s` | bo'sh joy (space): probel, tab, yangi qator | `[ \t\n\r]` |

Ularning **katta harfli** versiyasi — teskari ma'no:

| Qisqartma | Ma'nosi |
|-----------|---------|
| `\D` | raqam BO'LMAGAN |
| `\W` | so'z belgisi BO'LMAGAN |
| `\S` | bo'sh joy BO'LMAGAN |

```php
<?php
var_dump(preg_match('/^\d$/', "5"));    // int(1) — bitta raqam
var_dump(preg_match('/^\w$/', "_"));    // int(1) — pastki chiziq so'z belgisi
var_dump(preg_match('/^\s$/', " "));    // int(1) — bitta probel
var_dump(preg_match('/^\D$/', "a"));    // int(1) — raqammas belgi
```

### Miqdor belgilari — `* + ? {n} {n,m}`

Hozirgacha bitta belgi bittaga mos kelardi. **Miqdor belgilari** (quantifier) o'zidan oldingi element **necha marta** takrorlanishini bildiradi:

| Belgi | Ma'nosi |
|-------|---------|
| `*` | 0 yoki undan ko'p marta |
| `+` | 1 yoki undan ko'p marta (kamida bitta) |
| `?` | 0 yoki 1 marta (ixtiyoriy) |
| `{n}` | aynan n marta |
| `{n,m}` | n dan m gacha marta |
| `{n,}` | kamida n marta |

```php
<?php
// \d+ — bir yoki undan ko'p raqam (kamida bitta)
var_dump(preg_match('/^\d+$/', "12345"));   // int(1) — faqat raqamlardan iborat
var_dump(preg_match('/^\d+$/', "123a"));    // int(0) — 'a' bor
var_dump(preg_match('/^\d+$/', ""));        // int(0) — bo'sh, kamida bitta kerak

// \d{4} — aynan 4 ta raqam (masalan, yil)
var_dump(preg_match('/^\d{4}$/', "2026"));  // int(1)
var_dump(preg_match('/^\d{4}$/', "202"));   // int(0) — 3 ta

// \d{2,4} — 2 dan 4 gacha raqam
var_dump(preg_match('/^\d{2,4}$/', "999")); // int(1) — 3 ta, oraliqda
```

`?` — biror narsani **ixtiyoriy** qilish uchun juda foydali:

```php
<?php
// "colour" va "color" — ikkalasi ham mos (u bo'lishi ham, bo'lmasligi ham mumkin)
var_dump(preg_match('/^colou?r$/', "color"));   // int(1)
var_dump(preg_match('/^colou?r$/', "colour"));  // int(1)
```

### Guruhlash — `(...)`

Qavslar `(...)` bir nechta belgini **bitta guruhga** birlashtiradi. Endi miqdor belgisini butun guruhga qo'llash mumkin:

```php
<?php
// (ha)+ — "ha" so'zi bir yoki ko'p marta: "ha", "haha", "hahaha"...
var_dump(preg_match('/^(ha)+$/', "hahaha"));   // int(1)
var_dump(preg_match('/^(ha)+$/', "haa"));      // int(0) — "ha" + "a", guruh buzildi

// (\d{3}-)+ — "123-456-789-" kabi takrorlanuvchi bloklar
var_dump(preg_match('/^(\d{3}-)+\d{3}$/', "111-222-333"));   // int(1)
```

Guruhlar yana **capture group** (ushlab qolish guruhi) vazifasini bajaradi — naqshning mos kelgan qismini ajratib olishga imkon beradi. Buni keyinroq batafsil ko'ramiz.

### Tanlov — `|`

`|` belgisi "yoki" degani. `kun|tun` — "kun" yoki "tun".

```php
<?php
// "ha" yoki "yoq" yoki "mayli"
$naqsh = '/^(ha|yoq|mayli)$/';

var_dump(preg_match($naqsh, "ha"));     // int(1)
var_dump(preg_match($naqsh, "yoq"));    // int(1)
var_dump(preg_match($naqsh, "balki"));  // int(0)
```

Tanlovni guruh ichiga olish odatda zarur — aks holda `|` butun naqshga taalluqli bo'lib qoladi. `^ha|yoq$` — "ha bilan boshlanadi YOKI yoq bilan tugaydi" degan ma'noni beradi (xato!), `^(ha|yoq)$` esa — "aynan ha yoki aynan yoq".

### Maxsus belgilarni ekranlash — `\`

`. * + ? ( ) [ ] { } ^ $ | \ /` — bular regex'da **maxsus ma'noga** ega. Agar ularning o'zini (oddiy belgi sifatida) qidirmoqchi bo'lsangiz, oldiga `\` (teskari chiziq) qo'yib **ekranlash** (escape) kerak.

Eng ko'p uchraydigan misol — nuqta `.`. Regex'da `.` "istalgan bitta belgi" degani:

```php
<?php
// . ekranlanmagan — "istalgan belgi" degani
var_dump(preg_match('/^a.c$/', "axc"));   // int(1) — x ham mos
var_dump(preg_match('/^a.c$/', "a c"));   // int(1) — probel ham mos

// \. ekranlangan — endi AYNAN nuqta belgisi
var_dump(preg_match('/^a\.c$/', "a.c"));  // int(1)
var_dump(preg_match('/^a\.c$/', "axc"));  // int(0) — x nuqta emas
```

Bu, masalan, fayl kengaytmasini yoki email'dagi nuqtani tekshirishda muhim:

```php
<?php
// Fayl .txt bilan tugayaptimi? Nuqtani ekranlaymiz
var_dump(preg_match('/\.txt$/', "hisobot.txt"));   // int(1)
var_dump(preg_match('/\.txt$/', "hisobotXtxt"));   // int(0) — nuqta yo'q
```

### Bayroqlar — `i` (registr) va `m` (ko'p qator)

Naqshning yopuvchi delimiter'idan **keyin** harflar qo'shib, uning xulqini o'zgartirish mumkin. Bularni **bayroq** (flag, modifier) deyiladi.

`i` bayrog'i — registr (katta/kichik harf) farqini **e'tiborsiz** qoldiradi:

```php
<?php
// i bayrog'isiz — registr muhim
var_dump(preg_match('/salom/', "SALOM"));    // int(0)

// i bayrog'i bilan — SALOM, Salom, salom — barchasi mos
var_dump(preg_match('/salom/i', "SALOM"));   // int(1)
var_dump(preg_match('/salom/i', "Salom"));   // int(1)
```

`m` bayrog'i — **ko'p qatorli** rejim. Bunda `^` va `$` butun matnning emas, **har bir qatorning** boshi va oxiriga mos keladi:

```php
<?php
$matn = "birinchi\nikkinchi\nuchinchi";

// m'siz: ^\w+ butun matn boshidan faqat 1 ta moslik
preg_match_all('/^\w+/', $matn, $m1);
var_dump($m1[0]);   // array(1) { [0]=> "birinchi" }

// m bilan: har bir qator boshidan moslik
preg_match_all('/^\w+/m', $matn, $m2);
var_dump($m2[0]);   // array(3) { "birinchi", "ikkinchi", "uchinchi" }
```

Bayroqlarni birlashtirish mumkin: `/naqsh/im` — ham registrga befarq, ham ko'p qatorli.

### Mosliklarni ushlab olish — capture group

`preg_match` ning uchinchi argumenti — **o'zgaruvchi**. Unga moslik natijalari massiv bo'lib joylanadi. `&$matches` orqali (havola bilan) PHP shu o'zgaruvchini to'ldiradi:

```php
<?php
$matn = "Buyurtma raqami: 12345";

preg_match('/\d+/', $matn, $natija);

var_dump($natija);
// array(1) { [0]=> string(5) "12345" }

echo $natija[0];   // 12345 — topilgan butun moslik
```

Endi eng kuchli imkoniyat — qavs `(...)` orqali naqshning **alohida qismlarini** ajratib olish. `$matches[0]` — butun moslik, `$matches[1]` — birinchi qavs, `$matches[2]` — ikkinchi qavs:

```php
<?php
$sana = "2026-06-11";

// Uchta guruh: yil, oy, kun
preg_match('/^(\d{4})-(\d{2})-(\d{2})$/', $sana, $m);

echo "Yil: {$m[1]}\n";   // Yil: 2026
echo "Oy:  {$m[2]}\n";   // Oy:  06
echo "Kun: {$m[3]}\n";   // Kun: 11
// $m[0] esa butun moslik: "2026-06-11"
```

Bu — regex'ning eng amaliy qismi: matndan kerakli ma'lumotni **bo'laklab** olish.

### Hammasini topish — `preg_match_all`

`preg_match` faqat **birinchi** moslikni topadi. Agar matndan **barcha** mosliklarni topish kerak bo'lsa — `preg_match_all` ishlating. U ham xuddi shunday ishlaydi, lekin natija massivga barcha mosliklarni yig'adi:

```php
<?php
$matn = "Narxlar: 100, 250 va 999 so'm";

preg_match_all('/\d+/', $matn, $natija);

var_dump($natija[0]);
// array(3) { [0]=> "100", [1]=> "250", [2]=> "999" }

// Endi ular ustida ishlash mumkin — masalan yig'indi
$jami = array_sum($natija[0]);
echo "Jami: {$jami}";   // Jami: 1349
```

Capture group bilan birga ishlatganda yanada kuchli. Masalan, matndan barcha hashtag'larni ajratib olish:

```php
<?php
$post = "Bugun #php va #dasturlash o'rganyapman. #kod hayot!";

preg_match_all('/#(\w+)/', $post, $m);

var_dump($m[0]);   // ["#php", "#dasturlash", "#kod"]  — # bilan
var_dump($m[1]);   // ["php", "dasturlash", "kod"]     — #'siz (1-guruh)
```

`$m[0]` — to'liq mosliklar, `$m[1]` — har bir moslikdagi birinchi guruh qiymatlari.

### Almashtirish — `preg_replace`

`preg_replace` naqshga mos kelgan barcha qismlarni boshqasiga **almashtiradi**. `str_replace` ga o'xshaydi, lekin aniq so'z emas, **naqsh** bo'yicha ishlaydi:

```php
<?php
$matn = "Mening raqamim 901234567";

// Barcha raqamlarni * bilan yashirish (raqam maxfiyligi)
$yashirin = preg_replace('/\d/', '*', $matn);
echo $yashirin;   // Mening raqamim *********
```

Matnni tozalashda juda qo'l keladi. Masalan, ortiqcha bo'sh joylarni bittaga keltirish:

```php
<?php
$xom = "Ali     Valiyev      keldi";

// Bir yoki ko'p bo'sh joyni bitta probelga almashtirish
$toza = preg_replace('/\s+/', ' ', $xom);
echo $toza;   // Ali Valiyev keldi
```

Yoki faqat raqamlarni qoldirish (telefon raqamini tozalash):

```php
<?php
$kiritilgan = "+998 (90) 123-45-67";

// Raqam BO'LMAGAN hamma narsani o'chirish (bo'sh matnga almashtirish)
$faqat_raqam = preg_replace('/\D/', '', $kiritilgan);
echo $faqat_raqam;   // 998901234567
```

**Almashtirishda guruhni ishlatish** — `preg_replace`'ning yana bir kuchi. Almashtirish matnida `$1`, `$2` orqali ushlab qolingan guruhlarga murojaat qilish mumkin. Masalan, sana formatini o'zgartirish:

```php
<?php
$sana = "2026-06-11";

// YYYY-MM-DD ni DD.MM.YYYY ga aylantirish
$yangi = preg_replace('/(\d{4})-(\d{2})-(\d{2})/', '$3.$2.$1', $sana);
echo $yangi;   // 11.06.2026
```

### Ajratish — `preg_split`

`preg_split` — `explode`ning regex versiyasi. Matnni naqsh bo'yicha bo'laklarga ajratadi. `explode` faqat aniq belgi bilan ajratsa, `preg_split` murakkab ajratgichlar bilan ishlaydi:

```php
<?php
$matn = "olma, anor;uzum,  banan";

// Ajratgich: vergul YOKI nuqta-vergul, atrofida bo'sh joy bo'lishi ham mumkin
$mevalar = preg_split('/\s*[,;]\s*/', $matn);

var_dump($mevalar);
// array(4) { "olma", "anor", "uzum", "banan" }
```

`explode(",", ...)` bu ishni eplay olmasdi, chunki ajratgich har xil (`,` va `;`) va atrofida turli bo'sh joylar bor. Yana bir misol — gapni so'zlarga ajratish:

```php
<?php
$gap = "Bir   ikki\tuch\nto'rt";

// Istalgan bo'sh joy (probel, tab, yangi qator) bo'yicha ajratish
$sozlar = preg_split('/\s+/', $gap);

var_dump($sozlar);
// array(4) { "Bir", "ikki", "uch", "to'rt" }
```

### Real misol — email validatsiya

Endi o'rganganlarimizni real masalalarga qo'llaymiz. Eng mashhuri — email tekshirish. Soddalashtirilgan naqsh:

```php
<?php
function emailToghrimi(string $email): bool
{
    // ^...$ — butun matn tekshiriladi
    // [\w.+-]+  — foydalanuvchi nomi: harf, raqam, _, ., +, -
    // @         — majburiy @ belgisi
    // [\w-]+    — domen nomi
    // (\.[\w-]+)+ — kamida bitta ".uz" yoki ".com" qismi
    $naqsh = '/^[\w.+-]+@[\w-]+(\.[\w-]+)+$/';

    return preg_match($naqsh, $email) === 1;
}

var_dump(emailToghrimi("ali@mail.com"));        // bool(true)
var_dump(emailToghrimi("oqil.dev@gmail.uz"));   // bool(true)
var_dump(emailToghrimi("xato@mail"));           // bool(false) — nuqta yo'q
var_dump(emailToghrimi("@mail.com"));           // bool(false) — nom yo'q
var_dump(emailToghrimi("ali mail.com"));        // bool(false) — @ yo'q
```

> **Eslatma:** real loyihada email uchun regex emas, `filter_var` ishlating (bob oxirida). Bu yerda regex'ni o'rganish maqsadida ko'rsatdik. Lekin telefon yoki o'z formatlaringiz uchun regex aynan kerak bo'ladi.

### Real misol — O'zbekiston telefon raqami

O'zbekiston mobil raqami `+998` bilan boshlanib, jami 9 ta raqamdan iborat bo'ladi: `+998901234567`. Foydalanuvchilar uni turlicha yozadi — bo'sh joy, qavs, chiziqcha bilan. Avval tozalab, keyin tekshiramiz:

```php
<?php
function telefonToghrimi(string $raqam): bool
{
    // 1-qadam: raqam va + dan boshqa hamma narsani olib tashlash
    $toza = preg_replace('/[^\d+]/', '', $raqam);

    // 2-qadam: +998 dan keyin aynan 9 ta raqam bormi?
    return preg_match('/^\+998\d{9}$/', $toza) === 1;
}

var_dump(telefonToghrimi("+998901234567"));        // bool(true)
var_dump(telefonToghrimi("+998 90 123 45 67"));    // bool(true) — tozalandi
var_dump(telefonToghrimi("+998 (90) 123-45-67"));  // bool(true) — tozalandi
var_dump(telefonToghrimi("998901234567"));         // bool(false) — + yo'q
var_dump(telefonToghrimi("+99890123456"));         // bool(false) — raqam kam
```

Bu yerda ikki regex'ni birga ishlatdik: avval `preg_replace` bilan tozaladik, keyin `preg_match` bilan tekshirdik. Bu — amalda juda keng tarqalgan usul.

### Real misol — kuchli parol tekshiruvi

"Kuchli parol" odatda bir nechta shartga javob berishi kerak: kamida 8 belgi, katta harf, kichik harf, raqam. Buni bitta murakkab regex bilan ham qilish mumkin (lookahead orqali), lekin **o'qishliroq** yo'l — har shartni alohida tekshirish:

```php
<?php
function parolKuchlimi(string $parol): bool
{
    // Har bir shart — alohida kichik regex
    $uzunlik = strlen($parol) >= 8;
    $kattaHarf = preg_match('/[A-Z]/', $parol) === 1;
    $kichikHarf = preg_match('/[a-z]/', $parol) === 1;
    $raqam = preg_match('/\d/', $parol) === 1;

    // Hammasi true bo'lsagina parol kuchli
    return $uzunlik && $kattaHarf && $kichikHarf && $raqam;
}

var_dump(parolKuchlimi("Parol123"));    // bool(true) — barcha shart bajarildi
var_dump(parolKuchlimi("parol123"));    // bool(false) — katta harf yo'q
var_dump(parolKuchlimi("Parol"));       // bool(false) — raqam yo'q va qisqa
var_dump(parolKuchlimi("PAROL123"));    // bool(false) — kichik harf yo'q
```

> **Maslahat:** bitta ulkan regex yozishdan ko'ra, bir nechta sodda regex'ni mantiqiy `&&` bilan birlashtirish — ko'pincha to'g'riroq tanlov. Kod o'qishli bo'ladi va xatoni topish oson.

### Foydali alternativa — `filter_var`

Regex'ni yakunlashdan oldin muhim narsani aytib o'tamiz. Ba'zi keng tarqalgan tekshiruvlar uchun PHP'da tayyor, sinovdan o'tgan vosita bor — `filter_var`. U email, URL, IP, butun son kabilarni regex'siz tekshiradi:

```php
<?php
// Email — regex emas, filter_var
$email = "ali@mail.com";
if (filter_var($email, FILTER_VALIDATE_EMAIL) !== false) {
    echo "Email to'g'ri\n";
}

// URL
$url = "https://ioqil.uz";
if (filter_var($url, FILTER_VALIDATE_URL) !== false) {
    echo "URL to'g'ri\n";
}

// Butun son
var_dump(filter_var("42", FILTER_VALIDATE_INT));   // int(42)
var_dump(filter_var("abc", FILTER_VALIDATE_INT));  // bool(false)
```

**Qoida:** agar tekshiruvingiz uchun tayyor `FILTER_VALIDATE_*` bo'lsa — uni ishlating, u ishonchliroq. Regex'ni esa o'zingizning maxsus formatlaringiz uchun (telefon, mahsulot kodi, sana shabloni, hashtag ajratish) qoldiring. Ko'p hollarda eng yaxshi yechim — ikkalasini birga ishlatish.

### Qisqacha xulosa

- `preg_match($naqsh, $matn, &$m)` — birinchi moslik bormi (`1`/`0`); `$m` ga ushlab oladi.
- `preg_match_all(...)` — barcha mosliklar.
- `preg_replace($naqsh, $almash, $matn)` — naqsh bo'yicha almashtirish (`$1` orqali guruhlar).
- `preg_split($naqsh, $matn)` — naqsh bo'yicha bo'laklarga ajratish.
- Naqsh qismlari: delimiter `/.../`, anchor `^ $`, sinf `[a-z]` `[^...]`, qisqartma `\d \w \s`, miqdor `* + ? {n} {n,m}`, guruh `(...)`, tanlov `|`, ekranlash `\.`, bayroq `i m`.
- Murakkab tekshiruvni bitta ulkan regex'ga tiqishtirmang — sodda bo'laklarga bo'ling.
- Tayyor narsa bo'lsa (`filter_var`) — regex o'rniga uni ishlating.

### Mashqlar

**Oson**
1. `preg_match` bilan tekshiring: `"abc123"` matnida raqam bormi (`/\d/`)?
2. `"Salom"` matni katta harf bilan boshlanyaptimi tekshiring (`/^[A-Z]/`).
3. `preg_match` bilan tekshiring: matn faqat raqamlardan iboratmi (`/^\d+$/`). `"12345"` va `"12a45"` ga sinab ko'ring.
4. `preg_match` bilan `"fayl.txt"` `.txt` bilan tugaganini tekshiring (nuqtani ekranlashni unutmang).
5. `preg_replace` bilan `"a1b2c3"` matnidagi barcha raqamlarni `#` belgisiga almashtiring.

**O'rta**
6. `emailToghrimi` funksiyasini yozing: email `^[\w.+-]+@[\w-]+\.[\w-]+$` naqshiga mos kelsa `true` qaytarsin. 3 ta to'g'ri va 2 ta noto'g'ri email bilan sinang.
7. `preg_replace` bilan telefon raqamidan (`"+998 90 123 45 67"`) faqat raqamlarni qoldiring (`/\D/` ni bo'sh matnga almashtiring).
8. `preg_match` va capture group bilan `"2026-06-11"` sanasidan yil, oy, kunni alohida o'zgaruvchilarga ajrating va chiqaring.
9. `preg_match_all` bilan `"Narx: 100, 250, 999"` matnidan barcha sonlarni toping va yig'indisini hisoblang.
10. `preg_split` bilan `"olma, anor;uzum"` matnini vergul yoki nuqta-vergul bo'yicha ajrating.

**Qiyin**
11. `telefonToghrimi` funksiyasini yozing: avval `preg_replace` bilan tozalang, keyin `^\+998\d{9}$` bilan tekshiring. Turli formatdagi 4 ta raqamga sinang.
12. `parolKuchlimi` funksiyasini yozing: kamida 8 belgi, katta harf, kichik harf va raqam bo'lsin (har shartni alohida regex bilan).
13. `preg_match_all` va capture group bilan matndan barcha email'larni ajrating: `"Murojaat: ali@mail.com yoki vali@gmail.uz"`.
14. `preg_match_all` bilan post matnidan barcha hashtag'larni (`#so'z`) `#` belgisisiz ajrating.
15. Bitta funksiya yozing: `sanaToghrimi(string $s): bool` — `YYYY-MM-DD` formatini tekshirsin (oy 01-12, kun 01-31 oralig'ida, soddalashtirilgan holda).

<details markdown="1">
<summary>Yechim — 6 (email validatsiya)</summary>

```php
<?php
function emailToghrimi(string $email): bool
{
    return preg_match('/^[\w.+-]+@[\w-]+\.[\w-]+$/', $email) === 1;
}

var_dump(emailToghrimi("ali@mail.com"));     // true
var_dump(emailToghrimi("oqil@ioqil.uz"));    // true
var_dump(emailToghrimi("a.b@c.co"));         // true
var_dump(emailToghrimi("xato@mail"));        // false — nuqtali qism yo'q
var_dump(emailToghrimi("@mail.com"));        // false — nom yo'q
```

`=== 1` ishlatdik, chunki `preg_match` `1` (topildi), `0` (yo'q) yoki `false` (xato) qaytaradi. `=== 1` aniq "topildi"ni bildiradi.
</details>

<details markdown="1">
<summary>Yechim — 8 (sanadan qismlarni ajratish)</summary>

```php
<?php
$sana = "2026-06-11";

if (preg_match('/^(\d{4})-(\d{2})-(\d{2})$/', $sana, $m)) {
    $yil = $m[1];
    $oy  = $m[2];
    $kun = $m[3];
    echo "Yil: {$yil}, Oy: {$oy}, Kun: {$kun}";
    // Yil: 2026, Oy: 06, Kun: 11
} else {
    echo "Sana formati noto'g'ri";
}
```

Har bir `(...)` qavs `$m` massivida alohida o'rin egallaydi: `$m[1]`, `$m[2]`, `$m[3]`. `$m[0]` esa butun moslik.
</details>

<details markdown="1">
<summary>Yechim — 9 (sonlar yig'indisi)</summary>

```php
<?php
$matn = "Narx: 100, 250, 999";

preg_match_all('/\d+/', $matn, $m);

var_dump($m[0]);            // ["100", "250", "999"]
echo array_sum($m[0]);     // 1349
```

`preg_match_all` barcha sonlarni `$m[0]` ga to'pladi, `array_sum` ularni qo'shdi (matn raqamlar avtomatik songa aylanadi).
</details>

<details markdown="1">
<summary>Yechim — 11 (telefon validatsiya)</summary>

```php
<?php
function telefonToghrimi(string $raqam): bool
{
    // Raqam va + dan boshqa hamma narsani tozalash
    $toza = preg_replace('/[^\d+]/', '', $raqam);

    // +998 + aynan 9 raqam
    return preg_match('/^\+998\d{9}$/', $toza) === 1;
}

var_dump(telefonToghrimi("+998901234567"));       // true
var_dump(telefonToghrimi("+998 90 123 45 67"));   // true
var_dump(telefonToghrimi("+998-90-1234567"));     // true
var_dump(telefonToghrimi("998901234567"));        // false — + yo'q
```

Avval `preg_replace` bilan barcha bo'sh joy, qavs, chiziqchani tozaladik, keyin qat'iy naqsh bilan tekshirdik. Bu — validatsiyada eng ishonchli yondashuv.
</details>

<details markdown="1">
<summary>Yechim — 12 (kuchli parol)</summary>

```php
<?php
function parolKuchlimi(string $parol): bool
{
    return strlen($parol) >= 8
        && preg_match('/[A-Z]/', $parol) === 1   // katta harf
        && preg_match('/[a-z]/', $parol) === 1   // kichik harf
        && preg_match('/\d/', $parol) === 1;     // raqam
}

var_dump(parolKuchlimi("Parol123"));   // true
var_dump(parolKuchlimi("parol123"));   // false — katta harf yo'q
var_dump(parolKuchlimi("Parol"));      // false — qisqa va raqam yo'q
```

Har bir shart — alohida kichik regex. `&&` bilan bog'langan: bittasi `false` bo'lsa, butun natija `false`.
</details>

<details markdown="1">
<summary>Yechim — 13 (matndan email'larni ajratish)</summary>

```php
<?php
$matn = "Murojaat: ali@mail.com yoki vali@gmail.uz";

preg_match_all('/[\w.+-]+@[\w-]+\.[\w-]+/', $matn, $m);

var_dump($m[0]);
// ["ali@mail.com", "vali@gmail.uz"]
```

`preg_match_all` matn ichidagi naqshga mos **barcha** qismlarni `$m[0]` ga yig'di. Anchor (`^ $`) ishlatmadik — chunki email matn o'rtasida, boshi/oxirida emas.
</details>

<details markdown="1">
<summary>Yechim — 14 (hashtag ajratish)</summary>

```php
<?php
$post = "Bugun #php va #dasturlash, ayniqsa #regex zo'r!";

preg_match_all('/#(\w+)/', $post, $m);

var_dump($m[1]);
// ["php", "dasturlash", "regex"]  — # belgisisiz
```

`#(\w+)` — `#` belgisi va undan keyingi so'z. Qavs `(\w+)` so'zning o'zini (# siz) ushlab qoladi — shuning uchun `$m[1]` dan olamiz. `$m[0]` da esa `#` bilan bo'lardi.
</details>

<details markdown="1">
<summary>Yechim — 15 (sana formati)</summary>

```php
<?php
function sanaToghrimi(string $s): bool
{
    // Yil: 4 raqam
    // Oy: 01-12 (0 dan keyin 1-9, yoki 1 dan keyin 0-2)
    // Kun: 01-31
    $naqsh = '/^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/';

    return preg_match($naqsh, $s) === 1;
}

var_dump(sanaToghrimi("2026-06-11"));   // true
var_dump(sanaToghrimi("2026-13-01"));   // false — 13-oy yo'q
var_dump(sanaToghrimi("2026-06-32"));   // false — 32-kun yo'q
var_dump(sanaToghrimi("2026-6-11"));    // false — oy 2 xonali emas
```

Bu yerda tanlov `|` va guruh `(...)` birgalikda ishladi:
- Oy: `0[1-9]` (01-09) yoki `1[0-2]` (10-12).
- Kun: `0[1-9]` (01-09) yoki `[12]\d` (10-29) yoki `3[01]` (30-31).

Bu soddalashtirilgan tekshiruv — masalan fevralda 30-kunni rad etmaydi. To'liq tekshiruv uchun `checkdate()` yoki `DateTime` ishlatiladi (keyingi bobda).
</details>
</content>
</invoke>
