# 1.5 Matn bilan ishlash (string)

[⬅️ Oldingi: 1.4 Amallar (operatorlar)](./07-amallar.md) · [🏠 README](./README.md) · [Keyingi: 1.6 Shartlar (if/else) ➡️](./09-shartlar.md)

---

Matn (string) — dasturlashda eng ko'p ishlatiladigan ma'lumot turlaridan biri: ismlar, manzillar, xabarlar, sarlavhalar. PHP'da matn ustida turli amallar bajarish uchun maxsus **funksiyalar** bor. Funksiya — bu "tayyor vosita": unga biror narsa berasiz, u natija qaytaradi. (Funksiyalarni o'zingiz yozishni 1.9'da o'rganamiz; hozircha PHP bergan tayyor funksiyalardan foydalanamiz.)

Funksiya shunday ishlatiladi: `funksiya_nomi(nimadir)`. Qavs ichiga "nima ustida ishlashini" yozasiz.

### Matn uzunligini topish — `strlen`

`strlen` matndagi belgilar sonini qaytaradi:

```php
<?php
$ism = "Ali";
echo strlen($ism);   // 3  (3 ta harf)

$parol = "12345";
echo strlen($parol); // 5
```

Bu, masalan, "parol kamida 8 ta belgidan iborat bo'lsin" degan tekshiruvda kerak bo'ladi.

### O'zbekcha matn uchun KRITIK: `mb_strlen` (multibayt)

Yuqoridagi `strlen` lotin harflari (`Ali`, `12345`) bilan to'g'ri ishlaydi. Lekin **bir nozik muammo bor**: `strlen` belgilar sonini emas, **baytlar (byte)** sonini sanaydi. Lotin harflari (ASCII) da har bir harf — aniq 1 bayt, shuning uchun farqi sezilmaydi. Ammo maxsus belgilar (masalan `é`, `ñ`, kirill, emoji) UTF-8 kodlashda **2 yoki undan ko'p bayt** egallaydi. Shunda `strlen` xato (kattaroq) son beradi:

```php
<?php
$matn = "Café";        // 'é' harfi UTF-8 da 2 bayt
echo strlen($matn);    // 5  ❌ (bayt soni, harf soni emas!)
echo "\n";
echo mb_strlen($matn); // 4  ✅ (haqiqiy harflar soni)
```

`mb_` — bu **"multibyte"** (ko'p baytli) degani. `mb_` bilan boshlanadigan funksiyalar har bir belgini **bayt sifatida emas, belgi sifatida** to'g'ri sanaydi. O'zbek tilida lotin alifbosi (`o'`, `g'`, `sh`, `ch`) asosan ASCII bo'lsa-da, foydalanuvchilar kirilcha yozishi, ismlarda maxsus harflar bo'lishi mumkin. Shuning uchun **qoida**: matn bilan ishlashda har doim `mb_` variantini tanlang — u har qanday holatda to'g'ri ishlaydi.

> **Qisqacha:** `strlen` — baytlar, `mb_strlen` — belgilar. Lotincha matn uchun ikkisi bir xil, lekin maxsus belgilar bo'lsa faqat `mb_strlen` to'g'ri. Shubha bo'lsa — `mb_` ishlating.

### Katta/kichik harfga o'tkazish — `strtoupper`, `strtolower`

```php
<?php
$ism = "ali";
echo strtoupper($ism);   // ALI   (hammasi katta harf)
echo "<br>";
echo strtolower("SALOM"); // salom (hammasi kichik harf)
```

### Multibayt versiyalari — `mb_strtoupper`, `mb_strtolower`, `mb_substr`, `mb_str_split`

Xuddi `strlen` kabi, `strtoupper`/`strtolower`/`substr` ham maxsus belgilarda chalkashishi mumkin. Ularning **multibayt** versiyalari — `mb_strtoupper`, `mb_strtolower`, `mb_substr` — har qanday belgi bilan to'g'ri ishlaydi:

```php
<?php
echo mb_strtoupper("ozodbek");      // OZODBEK
echo "\n";
echo mb_strtolower("SALOM DUNYO");   // salom dunyo
echo "\n";
echo mb_substr("Dasturlash", 0, 4);  // Dast  (0-belgidan 4 ta belgi)
```

Yana bir foydali funksiya — `mb_str_split`: matnni **har bir belgisiga** ajratib, massivga aylantiradi (massivlarni 1.8'da ko'ramiz):

```php
<?php
$harflar = mb_str_split("salom");
print_r($harflar);
// Array ( [0] => s  [1] => a  [2] => l  [3] => o  [4] => m )
```

`mb_str_split` bilan har bir harfni alohida olib, ular ustida amal bajarish mumkin — masalan parolni belgi-belgi tekshirish yoki harflar sonini sanash.

> **Eslab qoling:** matn uzunligi, kesish, registr (katta/kichik) — bularning hammasi uchun `mb_` versiyasi bor. Real loyihada (ayniqsa foydalanuvchi kiritgan matnda) `mb_` ishlatish — ishonchli odat.

### Birinchi harfni katta qilish — `ucfirst`

```php
<?php
echo ucfirst("ali");        // Ali
echo "<br>";
echo ucwords("ali valiyev"); // Ali Valiyev  (har so'zning birinchi harfi)
```

### Matnni almashtirish — `str_replace`

Matndagi biror so'zni boshqasiga almashtiradi. Uch narsa beriladi: nimani, nimaga, qayerda:

```php
<?php
$gap = "Men olma yaxshi ko'raman";
echo str_replace("olma", "anor", $gap);   // Men anor yaxshi ko'raman
```

Bu yerda: `"olma"`ni topib, `"anor"`ga almashtir, `$gap` ichida.

### Matnning bir qismini olish — `substr`

Matnning ma'lum qismini kesib oladi. **Diqqat:** dasturlashda sanash **0 dan** boshlanadi (1 dan emas!). Ya'ni birinchi harf — 0-o'rinda, ikkinchisi — 1-o'rinda.

```php
<?php
$soz = "Dasturlash";
echo substr($soz, 0, 4);   // Dast  (0-o'rindan boshlab, 4 ta belgi)
echo "<br>";
echo substr($soz, 4);      // urlash (4-o'rindan oxirigacha)
```

> **Nega 0 dan?** Bu dasturlashda umumiy qoida — deyarli barcha tillarda sanoq 0 dan boshlanadi. Avvaliga g'alati tuyuladi, lekin tez ko'nikasiz. Massivlar (1.8) mavzusida buni yana ko'ramiz.

### Belgi pozitsiyasini topish — `strpos`, `stripos`, `strrpos`

Ba'zan matn ichida biror so'z **qaysi o'rinda** turishini bilish kerak bo'ladi. `strpos` matn ichida qidirilayotgan bo'lakning **birinchi pozitsiyasini** (0 dan boshlab) qaytaradi. Topilmasa — `false` qaytaradi:

```php
<?php
$gap = "Bugun havo issiq";
echo strpos($gap, "havo");        // 6  (6-o'rindan boshlanadi)
echo "\n";
var_dump(strpos($gap, "sovuq"));  // bool(false)  (yo'q)
```

`stripos` — xuddi `strpos`, lekin **katta-kichik harfga befarq** (case-insensitive):

```php
<?php
$email = "Ali@Mail.com";
var_dump(stripos($email, "mail"));  // int(4)  — "Mail" ni topdi, registrga qaramay
```

`strrpos` — bo'lakning **oxirgi** pozitsiyasini topadi (r — "right", o'ngdan qidiradi). Fayl kengaytmasini ajratishda foydali:

```php
<?php
$yol = "rasm.png.png";
echo strrpos($yol, ".png");   // 8  (oxirgi ".png" ning o'rni)
```

> ⚠️ **Eng ko'p uchraydigan xato — 0 va `false`.** `strpos` agar bo'lak matn **boshida** tursa, `0` qaytaradi. Lekin shartlarda `0` ham, `false` ham "yolg'on" deb baholanadi! Shuning uchun natijani **`=== false`** yoki **`!== false`** bilan solishtirish kerak:

```php
<?php
$gap = "Olma shirin";

// ❌ NOTO'G'RI: "Olma" 0-o'rinda, lekin 0 ni "topilmadi" deb o'ylaydi
if (strpos($gap, "Olma")) {
    echo "topildi";
} else {
    echo "topilmadi";   // ❌ XATO natija — aslida bor!
}

// ✅ TO'G'RI: aniq === false bilan tekshirish
if (strpos($gap, "Olma") !== false) {
    echo "topildi";     // ✅ to'g'ri
}
```

Faqat "bor-yo'qligini" bilish kerak bo'lsa, eng oson yo'l — quyida ko'radigan `str_contains` (uni alohida pozitsiya bilan boshi og'rimaydi).

### Matnni qidirish — `str_contains`

Matn ichida biror so'z bor-yo'qligini tekshiradi. Natija `true` yoki `false` bo'ladi:

```php
<?php
$gap = "Bugun havo issiq";
var_dump(str_contains($gap, "havo"));   // true  (bor)
var_dump(str_contains($gap, "sovuq"));  // false (yo'q)
```

`str_contains` — PHP 8 da qo'shilgan. U `strpos(...) !== false` ning sodda va xatosiz o'rnini bosadi: faqat "bormi?" deb so'rasangiz, mana shuni ishlating.

### Matn boshi/oxirini tekshirish — `str_starts_with`, `str_ends_with`

PHP 8 da yana ikkita juda qulay funksiya keldi. `str_starts_with` — matn berilgan bo'lak bilan **boshlanadimi**, `str_ends_with` — **tugaydimi** degan savolga `true`/`false` javob beradi:

```php
<?php
$fayl = "hisobot.pdf";

var_dump(str_starts_with($fayl, "hisobot"));  // true
var_dump(str_ends_with($fayl, ".pdf"));        // true
var_dump(str_ends_with($fayl, ".jpg"));        // false
```

Bular juda hayotiy: fayl kengaytmasini tekshirish (`.pdf`, `.png`), URL `https://` bilan boshlanishini bilish, telefon raqami `+998` bilan boshlanishini tekshirish va h.k.:

```php
<?php
$url = "https://ioqil.uz";
if (str_starts_with($url, "https://")) {
    echo "Xavfsiz ulanish (HTTPS)";
}
```

> **Avval qanday edi?** PHP 8 dan oldin buni qilish uchun `substr` yoki `strpos` bilan murakkab shartlar yozish kerak edi. Endi bitta o'qishli funksiya bor — ishonch bilan ishlating.

### Matnni bo'sh joy bilan to'ldirish — `str_pad`, `str_repeat`

`str_pad` matnni berilgan **uzunlikkacha** to'ldiradi (yetmagan joyni biror belgi bilan to'ldiradi). Chek, jadval, raqamlarni tekislashda foydali:

```php
<?php
echo str_pad("7", 3, "0", STR_PAD_LEFT);    // 007   (chapdan nol bilan)
echo "\n";
echo str_pad("Ali", 10, ".", STR_PAD_RIGHT); // Ali.......  (o'ngdan nuqta)
echo "\n";
echo str_pad("menu", 10, "-", STR_PAD_BOTH);  // ---menu---  (ikki tomondan)
```

`str_pad(matn, umumiy_uzunlik, belgi, yo'nalish)`. Yo'nalish: `STR_PAD_LEFT` (chapdan), `STR_PAD_RIGHT` (o'ngdan, standart), `STR_PAD_BOTH` (ikki tomondan).

`str_repeat` — bitta matnni **N marta takrorlaydi**. Ajratuvchi chiziq yoki naqsh chizishda qulay:

```php
<?php
echo str_repeat("=", 20);   // ====================
echo "\n";
echo str_repeat("ab", 3);   // ababab
```

### Ortiqcha bo'sh joylarni olib tashlash — `trim`

Foydalanuvchi matn kiritganda, ba'zan boshida yoki oxirida keraksiz bo'sh joy qoladi. `trim` ularni tozalaydi:

```php
<?php
$kiritilgan = "   Ali   ";
echo trim($kiritilgan);   // "Ali"  (atrofdagi bo'sh joylar ketdi)
```

### Faqat bir tomonni tozalash — `ltrim`, `rtrim`

`trim` ikkala tomondan tozalaydi. Ba'zan faqat **chap** yoki faqat **o'ng** tomonni tozalash kerak bo'ladi:

- `ltrim` — **l**eft (chap) tomonni tozalaydi,
- `rtrim` — **r**ight (o'ng) tomonni tozalaydi.

```php
<?php
$kiritilgan = "   Ali   ";
echo "[" . ltrim($kiritilgan) . "]";  // [Ali   ]  (faqat chap tozalandi)
echo "\n";
echo "[" . rtrim($kiritilgan) . "]";  // [   Ali]  (faqat o'ng tozalandi)
```

Ularning ikkinchi argumentiga **qaysi belgilarni** olib tashlashni ham aytish mumkin (faqat bo'sh joy emas):

```php
<?php
$narx = "***5000***";
echo ltrim($narx, "*");   // 5000***   (faqat chapdagi yulduzchalar)
echo "\n";
echo rtrim($narx, "*");   // ***5000   (faqat o'ngdagi yulduzchalar)
```

> **Hayotiy misol:** fayllardan o'qilgan har bir qator oxirida ko'rinmas `\n` (yangi qator belgisi) bo'ladi. `rtrim($qator)` uni olib tashlaydi — matn bilan ishlashda juda ko'p kerak bo'ladi.

### Matnni bo'laklarga ajratish va birlashtirish — `explode`, `implode`

Ko'pincha matnni belgilangan ajratgich bo'yicha bo'laklarga ajratish kerak bo'ladi (masalan, vergul bilan yozilgan ro'yxatni). `explode` matnni **massivga** (1.8) aylantiradi:

```php
<?php
$gap = "olma,anor,uzum";
$mevalar = explode(",", $gap);   // ["olma", "anor", "uzum"]
echo $mevalar[1];                // anor
```

`implode` esa aksini qiladi — massivni bitta matnga **birlashtiradi**:

```php
<?php
$royxat = ["Ali", "Vali", "Guli"];
echo implode(", ", $royxat);   // Ali, Vali, Guli
```

`explode("ajratgich", $matn)` — "matnni shu belgi bo'yicha bo'l"; `implode("ulagich", $massiv)` — "massiv elementlarini shu belgi bilan ula". Bu ikkisi matn ↔ massiv o'rtasidagi ko'prik.

### Har bir belgiga ajratish va teskari aylantirish — `str_split`, `strrev`

`str_split` matnni **belgi-belgi** (yoki belgilangan bo'lak uzunligi bo'yicha) massivga ajratadi:

```php
<?php
print_r(str_split("salom"));
// Array ( [0] => s  [1] => a  [2] => l  [3] => o  [4] => m )

print_r(str_split("123456", 2));
// Array ( [0] => 12  [1] => 34  [2] => 56 )  — 2 talab bo'lak
```

> **Eslatma:** `str_split` baytlar bilan ishlaydi. Maxsus belgilar (UTF-8) bo'lsa, yuqorida ko'rgan `mb_str_split` dan foydalaning — u har bir **belgini** to'g'ri ajratadi.

`strrev` — matnni **teskari** aylantiradi (oxiridan boshiga):

```php
<?php
echo strrev("salom");   // molas
echo "\n";
echo strrev("12345");   // 54321
```

Bu, masalan, "matn palindrommi?" (ikki tomondan bir xil o'qiladimi) degan klassik masalada ishlatiladi.

### Yangi qatorni `<br>` ga aylantirish — `nl2br`

HTML'da oddiy `\n` (yangi qator) ko'rinmaydi — brauzer uni e'tiborsiz qoldiradi. `nl2br` (new line to break) har bir `\n` oldiga `<br />` qo'yadi, shunda matn brauzerda ham qatorlarga bo'linib ko'rinadi:

```php
<?php
$izoh = "Birinchi qator\nIkkinchi qator";
echo nl2br($izoh);
// Birinchi qator<br />
// Ikkinchi qator
```

Foydalanuvchi `textarea` (ko'p qatorli maydon) ga yozgan izohni veb-sahifada ko'rsatishda juda kerak bo'ladi.

### Uzun matnni qatorlarga sig'dirish — `wordwrap`

`wordwrap` uzun matnni belgilangan **enga** (belgilar soniga) sig'dirib, so'zlarni buzmasdan qatorlarga bo'ladi:

```php
<?php
$uzun = "Bu juda uzun gap bo'lib uni belgilangan enga sig'dirish kerak";
echo wordwrap($uzun, 20, "\n", true);
// Bu juda uzun gap
// bo'lib uni
// belgilangan enga
// sig'dirish kerak
```

`wordwrap(matn, en, ulagich, qattiq_bo'lish)`. To'rtinchi argument `true` bo'lsa, juda uzun bitta so'z ham majburan bo'linadi. Bu — chek, SMS yoki tor ustunli matnlarni formatlashda asqotadi.

### Sonni chiroyli formatlash — `number_format`

Katta sonlarni o'qishli ko'rinishda chiqarish (minglik ajratgich, kasr):

```php
<?php
echo number_format(1234567.891, 2);            // 1,234,567.89
echo number_format(1234567, 0, ".", " ");      // 1 234 567  (o'zbekcha uslub)
```

`number_format(son, kasr_xona, kasr_belgisi, minglik_belgisi)`. Narxlarni ko'rsatishda juda ko'p kerak bo'ladi.

### Andoza bo'yicha matn yasash — `sprintf`

`sprintf` "andoza"ga qiymatlarni joylab, **yangi matn qaytaradi** (`echo` qilmaydi — natijani saqlash mumkin):

```php
<?php
$matn = sprintf("%s — %d yoshda", "Ali", 19);
echo $matn;                          // Ali — 19 yoshda

echo sprintf("Narx: %.2f so'm", 5000);   // Narx: 5000.00 so'm
echo sprintf("ID: %05d", 42);            // ID: 00042  (5 xona, nol bilan)
```

- **`%s`** — matn (string) o'rni, **`%d`** — butun son, **`%.2f`** — 2 kasrli son, **`%05d`** — 5 xonali, yetmasa nol bilan to'ldiriladi.
- Qiymatlar andozadan keyin, tartibda yoziladi.

> **`echo` bilan farqi:** `echo "Ali" . " — " . 19` ham ishlaydi, lekin ko'p qiymat bo'lsa `.` bilan ulash chalkash ko'rinadi. `sprintf` andozani aniq ko'rsatadi — ayniqsa formatlash (kasr, nol to'ldirish) kerak bo'lganda qulay.

### To'g'ridan-to'g'ri chiqarish va massivdan — `printf`, `vsprintf`

`sprintf` matn **qaytaradi**. Agar natijani saqlamasdan **darrov chiqarmoqchi** bo'lsangiz, `printf` ishlating — u xuddi `sprintf` kabi andoza bilan ishlaydi, lekin natijani to'g'ridan-to'g'ri ekranga chiqaradi (`echo sprintf(...)` ning qisqartmasi):

```php
<?php
printf("%s — %d yoshda\n", "Ali", 19);   // Ali — 19 yoshda
printf("Narx: %.2f so'm\n", 5000);        // Narx: 5000.00 so'm
```

`vsprintf` — "v" **vector** (massiv) degani. Qiymatlar bir-bir yozilmaydi, **massivdan** olinadi. Bu qiymatlar avvaldan massivda turganda juda qulay:

```php
<?php
$malumot = ["Vali", 25];
echo vsprintf("%s — %d yoshda", $malumot);   // Vali — 25 yoshda
```

Jadval ko'rinishida tekis ustunlar chizishda `vsprintf` va belgi-pozitsiya (`%-10s` chapga tekislash, `%5d` 5 xonaga o'ngga tekislash) yaxshi ishlaydi:

```php
<?php
echo vsprintf("%-10s | %5d", ["Olma", 50]);   // Olma       |    50
```

> **Qaysi birini tanlash?** `sprintf` — natijani saqlash kerak bo'lsa. `printf` — darrov chiqarish kerak bo'lsa. `vsprintf` — qiymatlar massivda turgan bo'lsa.

### Ko'p qatorli matn va shablon — HEREDOC va NOWDOC

Ko'p qatorli matn (xat, HTML shablon, SQL so'rov) yozishda har bir qatorni `"..."` bilan o'rab, `.` bilan ulash juda zerikarli. PHP'da bunga maxsus, qulay sintaksis bor — **HEREDOC**.

HEREDOC `<<<NOM` bilan boshlanadi, `NOM;` bilan tugaydi (NOM — siz tanlagan belgi, odatda katta harf). Ichida `"` ham, `'` ham erkin yozish mumkin, eng muhimi — **o'zgaruvchilar ishlaydi** (`"..."` kabi):

```php
<?php
$ism = "Ali";
$yosh = 19;

$xat = <<<XAT
Salom, $ism!
Sizning yoshingiz: $yosh.
Xush kelibsiz.
XAT;

echo $xat;
// Salom, Ali!
// Sizning yoshingiz: 19.
// Xush kelibsiz.
```

HEREDOC ayniqsa **HTML shablon** yozishda qulay — `echo` larni takrorlamaysiz, kod toza ko'rinadi. Murakkab ifodalarni `{$...}` ichida yozish tavsiya etiladi:

```php
<?php
$sarlavha = "Mahsulot";
$narx = 5000;

$html = <<<HTML
<div class="card">
    <h2>$sarlavha</h2>
    <p>Narxi: {$narx} so'm</p>
</div>
HTML;

echo $html;
```

**NOWDOC** — HEREDOC ning "xom" varianti. U `<<<'NOM'` (NOM **bir tirnoq ichida**) bilan boshlanadi. Farqi: NOWDOC ichida o'zgaruvchilar **ishlamaydi** — hamma narsa shundayligicha (xom matn sifatida) chiqadi. Bu kod namunasi yoki `$` belgisi bor matnni ko'rsatishda kerak bo'ladi:

```php
<?php
$kod = <<<'NAMUNA'
$ism o'zgaruvchisi shunchaki matn bo'lib chiqadi.
NAMUNA;

echo $kod;
// $ism o'zgaruvchisi shunchaki matn bo'lib chiqadi.
```

> ⚠️ **Diqqat:** yopuvchi belgi (`XAT;`, `HTML;`, `NAMUNA;`) **alohida qatorda** turishi kerak. PHP 7.3 dan boshlab uni chekka (bo'sh joy bilan) yozish ham mumkin, lekin eng ishonchlisi — boshqa matn bilan bir qatorga qo'shmaslik.

### Mashqlar

**Oson**
1. Bir ismni `strlen` bilan o'lchang va uzunligini chiqaring.
2. O'z ismingizni `strtoupper` bilan katta harfda chiqaring.
3. `ucfirst` bilan kichik harfli so'zning birinchi harfini katta qiling.
4. Bir gapdagi so'zni `str_replace` bilan boshqasiga almashtiring.
5. "Dasturlash" so'zining birinchi 4 harfini `substr` bilan oling.
6. `str_repeat` bilan `"-"` belgisidan 30 ta uzunlikdagi ajratuvchi chiziq chizing.
7. `"hisobot.pdf"` fayl nomi `.pdf` bilan tugaydimi — `str_ends_with` bilan tekshiring.

**O'rta**
8. Foydalanuvchi ismi `"  ali  "` shaklida (bo'sh joylar bilan) berilgan. `trim` bilan tozalang, keyin `ucfirst` bilan birinchi harfini katta qiling. Natija: `Ali`.
9. Bir gapda biror so'z bor-yo'qligini `str_contains` bilan tekshiring.
10. To'liq ism (`"ali valiyev"`) ning har bir so'zini `ucwords` bilan katta harf bilan boshlang.
11. Parol uzunligini `strlen` bilan o'lchang va `var_dump` orqali "8 dan katta yoki tengmi" (`>= 8`) ekanini tekshiring.
12. `"Café"` so'zi uchun `strlen` va `mb_strlen` natijalarini chiqaring va nima uchun farq qilishini tushuntiring (izoh sifatida).
13. Bir butun son ID ni (masalan `42`) `str_pad` bilan 6 xonali, chapdan nol bilan to'ldirilgan ko'rinishga keltiring: `000042`.
14. `"Bugun havo issiq"` gapida `"havo"` so'zi qaysi pozitsiyada turishini `strpos` bilan toping.

**Qiyin**
15. Bir ismni oling, uni katta harfga o'tkazing va uzunligini bitta gapda chiqaring: masalan, `"ALI - 3 ta harf"`. (Maslahat: `strtoupper`, `strlen` va `.` ulashdan foydalaning.)
16. Email manzil (`"ali@mail.com"`) ichida `"@"` belgisi bor-yo'qligini tekshiring (`str_contains`). Bu — oddiy email tekshiruvining boshlanishi.
17. `"olma,anor,uzum"` matnini `explode` bilan massivga aylantiring, sonini (`count`) chiqaring, keyin `implode` bilan `" | "` ajratgich bilan qayta birlashtiring.
18. Narx `1234567.5` ni `number_format` bilan minglik ajratgich va 2 kasr bilan chiqaring; keyin `sprintf` bilan `"Mahsulot: <nom>, narxi: <narx> so'm"` ko'rinishida bitta matn yasang.
19. HEREDOC dan foydalanib, `$nom` va `$narx` o'zgaruvchilari joylangan kichik HTML "karta" (`<div>` ichida sarlavha va narx) yasang va chiqaring.
20. Bir matnni `mb_str_split` bilan harflarga ajrating va `strrev` ishlatmasdan, harflar massivini teskari tartibda birlashtirib, matnni teskari ko'rinishda chiqaring. (Maslahat: `array_reverse` va `implode`.)

<details markdown="1">
<summary>Yechim — 8</summary>

```php
<?php
$kiritilgan = "  ali  ";
$tozalangan = trim($kiritilgan);     // "ali"
$natija = ucfirst($tozalangan);      // "Ali"
echo $natija;
```

Yoki bitta qatorda (funksiyalarni "ichma-ich" ishlatib):
```php
<?php
echo ucfirst(trim("  ali  "));   // Ali
```
Bu yerda avval `trim` bo'sh joylarni oladi, keyin uning natijasini `ucfirst` katta harfga o'tkazadi. Funksiyalarni shunday birlashtirish mumkin.
</details>

<details markdown="1">
<summary>Yechim — 12 (strlen va mb_strlen farqi)</summary>

```php
<?php
$soz = "Café";
echo "strlen: " . strlen($soz);       // strlen: 5  (bayt soni)
echo "\n";
echo "mb_strlen: " . mb_strlen($soz); // mb_strlen: 4  (belgi soni)

// 'é' harfi UTF-8 kodlashda 2 bayt egallaydi.
// strlen baytlarni sanaydi -> 5; mb_strlen belgilarni sanaydi -> 4.
// O'zbekcha/maxsus belgili matnda doim mb_strlen ishonchli.
```
</details>

<details markdown="1">
<summary>Yechim — 13 (str_pad bilan ID to'ldirish)</summary>

```php
<?php
$id = 42;
$tola = str_pad((string)$id, 6, "0", STR_PAD_LEFT);
echo $tola;   // 000042
```
`str_pad` matn bilan ishlaganligi uchun sonni avval `(string)` bilan matnga aylantirdik. `STR_PAD_LEFT` — bo'sh joyni chapdan to'ldiradi, shuning uchun nollar oldinga qo'shildi.
</details>

<details markdown="1">
<summary>Yechim — 15</summary>

```php
<?php
$ism = "ali";
$katta = strtoupper($ism);       // "ALI"
$uzunlik = strlen($ism);         // 3
echo $katta . " - " . $uzunlik . " ta harf";   // ALI - 3 ta harf
```
</details>

<details markdown="1">
<summary>Yechim — 16 (email tekshiruvining boshlanishi)</summary>

```php
<?php
$email = "ali@mail.com";

if (str_contains($email, "@")) {
    echo "Email ko'rinishi to'g'ri (@ bor)";
} else {
    echo "Noto'g'ri email: @ yo'q";
}
```
Bu — eng oddiy tekshiruv: `@` belgisi bormi. Haqiqiy email tekshiruvi murakkabroq (PHP'da `filter_var($email, FILTER_VALIDATE_EMAIL)` tayyor vositasi bor), lekin `str_contains` bilan asosiy g'oyani tushunish — yaxshi boshlanish.
</details>

<details markdown="1">
<summary>Yechim — 17 (explode / implode)</summary>

```php
<?php
$matn = "olma,anor,uzum";
$mevalar = explode(",", $matn);     // ["olma", "anor", "uzum"]

echo count($mevalar);               // 3
echo "<br>";
echo implode(" | ", $mevalar);      // olma | anor | uzum
```
`explode` matnni massivga ajratdi, `implode` esa boshqa ajratgich bilan qayta birlashtirdi. Bu ikkisi — matn va massiv orasida o'tishning eng tez yo'li.
</details>

<details markdown="1">
<summary>Yechim — 18 (number_format va sprintf)</summary>

```php
<?php
$narx = 1234567.5;

echo number_format($narx, 2);   // 1,234,567.50

$satr = sprintf(
    "Mahsulot: %s, narxi: %s so'm",
    "Noutbuk",
    number_format($narx, 2)
);
echo "<br>" . $satr;            // Mahsulot: Noutbuk, narxi: 1,234,567.50 so'm
```
`number_format` sonni o'qishli qildi (minglik vergul + 2 kasr), `sprintf` esa uni andozaga joylab tayyor matn yasadi.
</details>

<details markdown="1">
<summary>Yechim — 19 (HEREDOC bilan HTML karta)</summary>

```php
<?php
$nom = "Noutbuk";
$narx = 12500000;

$karta = <<<HTML
<div class="card">
    <h2>$nom</h2>
    <p>Narxi: {$narx} so'm</p>
</div>
HTML;

echo $karta;
// <div class="card">
//     <h2>Noutbuk</h2>
//     <p>Narxi: 12500000 so'm</p>
// </div>
```
HEREDOC ichida o'zgaruvchilar to'g'ridan-to'g'ri joylandi — `echo` larni takrorlash shart bo'lmadi. HTML shablon yozishning eng toza yo'li.
</details>

<details markdown="1">
<summary>Yechim — 20 (mb_str_split + array_reverse + implode)</summary>

```php
<?php
$matn = "salom";
$harflar = mb_str_split($matn);        // ["s","a","l","o","m"]
$teskari = array_reverse($harflar);    // ["m","o","l","a","s"]
echo implode("", $teskari);            // molas
```
`mb_str_split` matnni belgilarga ajratdi, `array_reverse` massivni teskari aylantirdi, `implode("", ...)` esa ularni ajratgichsiz qayta birlashtirdi. Natija — `strrev` bilan bir xil, lekin bu usul maxsus belgilarda ham to'g'ri ishlaydi.
</details>
