# 4.6 Fayl bilan ishlash va fayl yuklash

[⬅️ Oldingi: 4.5 JSON bilan ishlash va oddiy API](./35-json-bilan-ishlash-va-oddiy-api.md) · [🏠 README](./README.md) · [Keyingi: 5.1 Toza kod prinsiplari ➡️](./36-toza-kod-prinsiplari.md)

---

Har bir jiddiy ilovada fayllar bilan ishlash bor: foydalanuvchi avatar yoki hujjat yuklaydi, dastur xatolarni log faylga yozadi, hisobot CSV ko'rinishida eksport qilinadi, sozlamalar matnli faylda saqlanadi. Ma'lumotlar bazasi (3-qism) ko'p narsani saqlaydi, lekin **fayllar** hali ham zarur — chunki rasm, PDF, video kabi "katta" ma'lumotlarni bazaga emas, diskka saqlaymiz.

Bu bobda ikki katta mavzuni ko'ramiz: birinchisi — diskdagi fayllarni **o'qish va yozish** (log, CSV, sozlama); ikkinchisi va eng muhimi — foydalanuvchi brauzer orqali yuborgan faylni **xavfsiz qabul qilish** (file upload). Fayl yuklash — hujum nuqtalaridan biri, shuning uchun unga alohida e'tibor beramiz: yuza qilingan kod butun saytni xavf ostiga qo'yadi.

## Fayllarni o'qish va yozish

### Faylga oddiy yozish — `file_put_contents`

Eng oson yo'l — `file_put_contents`: faylga butun matnni bir urinishda yozadi. Fayl bo'lmasa — yaratadi, bo'lsa — **ustidan yozadi** (eski tarkib o'chadi). Funksiya nechta bayt yozilganini qaytaradi (xato bo'lsa `false`).

```php
<?php
$satr = file_put_contents("xabar.txt", "Salom, dunyo!");
echo $satr;   // 13  (yozilgan baytlar soni)
```

Bir necha qatorni yozish uchun matnga `\n` (yangi qator belgisi) qo'shamiz. Diqqat: `\n` ishlashi uchun qo'shtirnoq (`"..."`) kerak — bittatirnoq (`'...'`) ichida `\n` shunchaki ikki belgi bo'lib qoladi.

```php
<?php
$matn = "Birinchi qator\nIkkinchi qator\nUchinchi qator\n";
file_put_contents("royxat.txt", $matn);
```

### Faylga qo'shib yozish — `FILE_APPEND`

Log fayl uchun ustidan yozish yaramaydi — har safar eski yozuvlar o'chib ketadi. `FILE_APPEND` bayrog'i (flag) matnni fayl **oxiriga qo'shadi**:

```php
<?php
file_put_contents("amallar.log", "Foydalanuvchi kirdi\n", FILE_APPEND);
file_put_contents("amallar.log", "Hujjat yuklandi\n", FILE_APPEND);
// Fayl tarkibi:
// Foydalanuvchi kirdi
// Hujjat yuklandi
```

### Fayldan oddiy o'qish — `file_get_contents`

`file_get_contents` faylning **butun tarkibini** bitta matn (string) ko'rinishida qaytaradi. Kichik fayllar (sozlama, shablon, kichik JSON) uchun ideal:

```php
<?php
file_put_contents("salom.txt", "Assalomu alaykum");

$tarkib = file_get_contents("salom.txt");
echo $tarkib;   // Assalomu alaykum
echo strlen($tarkib);   // 16  (uzunligini ham bilamiz)
```

> **Diqqat — katta fayl:** `file_get_contents` butun faylni xotiraga (RAM) yuklaydi. 2 GB lik fayl bilan bu xotirani to'ldirib yuboradi. Katta fayllar uchun pastdagi `fgets` (qator-qator) usulini ishlating.

### Fayl satrlarini massivga olish — `file`

Ko'pincha faylni **qatorma-qator** ko'rib chiqish kerak. `file` funksiyasi har bir qatorni massivning bitta elementi qilib qaytaradi:

```php
<?php
file_put_contents("shahar.txt", "Toshkent\nSamarqand\nBuxoro\n");

$qatorlar = file("shahar.txt", FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
// ["Toshkent", "Samarqand", "Buxoro"]

foreach ($qatorlar as $nomer => $shahar) {
    echo ($nomer + 1) . ". " . $shahar . "\n";
}
// 1. Toshkent
// 2. Samarqand
// 3. Buxoro
```

Ikki foydali bayroq: `FILE_IGNORE_NEW_LINES` — har qator oxiridagi `\n` ni olib tashlaydi; `FILE_SKIP_EMPTY_LINES` — bo'sh qatorlarni o'tkazib yuboradi. Ularni `|` (yoki) bilan birlashtiramiz.

### Pastki sathda ishlash — `fopen`, `fwrite`, `fread`, `fclose`

`file_get_contents` va `file_put_contents` qulay, lekin ular faylni har safar to'liq ochib-yopadi. Agar faylni ochib **bir necha amal** bajarish (ko'p marta yozish, qism-qism o'qish) kerak bo'lsa, faylni qo'lda ochamiz: `fopen` faylni ochadi va **resurs** (handle — faylga "ishlov beruvchi") qaytaradi, oxirida `fclose` bilan yopamiz.

`fopen` ikkinchi argumenti — **rejim** (mode), faylni nima maqsadda ochayotganimizni bildiradi:

| Rejim | Ma'nosi |
|-------|---------|
| `"r"` | Faqat **o'qish**. Fayl bo'lishi shart. Kursor boshida. |
| `"w"` | **Yozish**. Faylni tozalaydi (yoki yaratadi). Eski tarkib yo'qoladi. |
| `"a"` | **Qo'shib yozish** (append). Kursor oxirida; eski tarkib saqlanadi. |
| `"r+"` | O'qish **va** yozish. Fayl bo'lishi shart. Kursor boshida. |
| `"x"` | Yozish, lekin faqat fayl **yo'q bo'lsa** (bor bo'lsa xato). |

```php
<?php
// Yozish uchun ochamiz ("w" — tozalaydi)
$fayl = fopen("hisobot.txt", "w");
fwrite($fayl, "Hisobot boshi\n");
fwrite($fayl, "Qator 2\n");
fwrite($fayl, "Qator 3\n");
fclose($fayl);   // har doim yopishni unutmang!

echo file_get_contents("hisobot.txt");
// Hisobot boshi
// Qator 2
// Qator 3
```

`fread` esa fayldan belgilangan miqdordagi baytni o'qiydi:

```php
<?php
file_put_contents("data.txt", "0123456789");

$fayl = fopen("data.txt", "r");
$qism = fread($fayl, 5);   // boshidan 5 bayt
fclose($fayl);

echo $qism;   // 01234
```

### Katta faylni qator-qator o'qish — `fgets` + `feof`

Katta log yoki CSV faylni butunlay xotiraga yuklamasdan, **bir qatordan** o'qiymiz. `fgets` keyingi qatorni qaytaradi, `feof` (end of file) fayl oxiriga yetganimizni bildiradi:

```php
<?php
file_put_contents("katta.log", "qator-1\nqator-2\nqator-3\n");

$fayl = fopen("katta.log", "r");
while (!feof($fayl)) {
    $qator = fgets($fayl);
    if ($qator === false) {
        break;   // o'qishda xato yoki oxir
    }
    echo "O'qildi: " . trim($qator) . "\n";
}
fclose($fayl);
// O'qildi: qator-1
// O'qildi: qator-2
// O'qildi: qator-3
```

Bu usul **xotira-tejamkor**: faylda million qator bo'lsa ham, har lahzada xotirada faqat bitta qator turadi. Gigabaytlik fayllarni shunday qayta ishlash mumkin.

### CSV faylni o'qish — `fgetcsv`

**CSV** (Comma-Separated Values — vergul bilan ajratilgan qiymatlar) — jadval ma'lumotini saqlovchi eng keng tarqalgan format. Excel, Google Sheets va deyarli barcha dasturlar CSV import/eksport qiladi. Bitta qator — bitta yozuv, ustunlar vergul (yoki nuqta-vergul) bilan ajratiladi.

CSV ni `explode(",", ...)` bilan o'qish — **xato**: chunki qiymat ichida vergul yoki qo'shtirnoq bo'lsa, bo'linish buziladi. To'g'ri yo'l — `fgetcsv`: u qoidalarni biladi (tirnoq ichidagi vergulni ajratmaydi):

```php
<?php
// Avval namuna CSV yaratamiz
$csv = "ism,yosh,shahar\nAli,25,Toshkent\nVali,30,Samarqand\n";
file_put_contents("odamlar.csv", $csv);

// Endi o'qiymiz
$fayl = fopen("odamlar.csv", "r");
$sarlavha = fgetcsv($fayl, escape: "");   // birinchi qator — ustun nomlari
echo "Ustunlar: " . implode(" | ", $sarlavha) . "\n";

while (($qator = fgetcsv($fayl, escape: "")) !== false) {
    // $qator — massiv: [ism, yosh, shahar]
    echo $qator[0] . " — " . $qator[1] . " yosh, " . $qator[2] . "\n";
}
fclose($fayl);
// Ustunlar: ism | yosh | shahar
// Ali — 25 yosh, Toshkent
// Vali — 30 yosh, Samarqand
```

`fgetcsv` har qatorni **massiv** qilib qaytaradi; fayl oxirida `false` qaytaradi, shuning uchun `while` shartida `!== false` ishlatamiz. `escape: ""` — **nomli argument** (1.x): PHP 8.4'da CSV'ning eskirgan "escape" qoidasini o'chiradi va PHP 9'ga tayyor, standart RFC 4180 xatti-harakatini beradi. Uni yozish — yaxshi odat (aks holda PHP 8.4 ogohlantirish chiqaradi).

### CSV faylga yozish — `fputcsv`

Aksincha — massivlardan CSV yasash uchun `fputcsv` ishlatamiz. U vergul va tirnoqlarni o'zi to'g'ri qo'yadi (qiymatda vergul bo'lsa, avtomatik tirnoqqa oladi):

```php
<?php
$mahsulotlar = [
    ["nomi", "narxi", "izoh"],
    ["Noutbuk", 7500000, "yangi, korobkada"],
    ["Sichqoncha", 120000, "simsiz"],
];

$fayl = fopen("mahsulotlar.csv", "w");
foreach ($mahsulotlar as $qator) {
    fputcsv($fayl, $qator, escape: "");
}
fclose($fayl);

echo file_get_contents("mahsulotlar.csv");
// nomi,narxi,izoh
// Noutbuk,7500000,"yangi, korobkada"
// Sichqoncha,120000,simsiz
```

E'tibor bering: `"yangi, korobkada"` ichida vergul borligi uchun `fputcsv` uni avtomatik qo'shtirnoqqa oldi. Mana shu — qo'lda `implode(",", ...)` qila olmaydigan narsa.

### Fayl va papka mavjudligini tekshirish

Faylga murojaat qilishdan oldin uning borligini tekshirish kerak — aks holda xato chiqadi. Bir nechta tekshiruvchi funksiya bor:

```php
<?php
file_put_contents("test.txt", "salom");

var_dump(file_exists("test.txt"));   // true   — fayl yoki papka bormi?
var_dump(is_file("test.txt"));       // true   — aynan faylmi?
var_dump(is_dir("test.txt"));        // false  — papkami?
var_dump(file_exists("yoq.txt"));    // false  — yo'q fayl
```

- **`file_exists`** — fayl yoki papka mavjudligini umumiy tekshiradi.
- **`is_file`** — aynan oddiy fayl ekanini.
- **`is_dir`** — papka (directory) ekanini.

### Papka yaratish va ichini ko'rish — `mkdir`, `scandir`

Yuklangan fayllarni saqlash uchun ko'pincha papka yaratish kerak. `mkdir` papka yaratadi; uchinchi argument `true` bo'lsa, **bir necha sath** papkani birato'la yaratadi (`yuklamalar/2026/iyun` kabi):

```php
<?php
if (!is_dir("yuklamalar")) {
    mkdir("yuklamalar", 0755, true);   // 0755 — ruxsatlar, true — rekursiv
}

// Ichiga ikkita fayl qo'yamiz
file_put_contents("yuklamalar/a.txt", "1");
file_put_contents("yuklamalar/b.txt", "2");

// Papka ichidagi fayllar ro'yxati
$fayllar = scandir("yuklamalar");
// scandir har doim "." va ".." ni ham qaytaradi — ularni ajratamiz
$haqiqiy = array_diff($fayllar, [".", ".."]);
print_r(array_values($haqiqiy));
// Array ( [0] => a.txt [1] => b.txt )
```

`scandir` natijasida `.` (joriy papka) va `..` (yuqori papka) doim bo'ladi — ularni `array_diff` bilan chiqarib tashlaymiz.

### Faylni o'chirish va nomini o'zgartirish — `unlink`, `rename`

```php
<?php
file_put_contents("eski.txt", "ma'lumot");

rename("eski.txt", "yangi.txt");   // nomini o'zgartirdi (yoki ko'chirdi)
var_dump(file_exists("yangi.txt"));   // true

unlink("yangi.txt");   // faylni o'chirdi
var_dump(file_exists("yangi.txt"));   // false
```

**`unlink`** faylni o'chiradi (PHP'da "delete" emas, aynan `unlink` deyiladi). **`rename`** nomini o'zgartiradi — bir papkadan boshqasiga ko'chirishda ham ishlatiladi.

## Fayl yuklash (file upload)

Endi bobning eng muhim qismiga keldik: foydalanuvchi brauzer orqali yuborgan faylni qabul qilish. Avatar, hujjat, rasm — bularning hammasi shu jarayon orqali serverga keladi.

### HTML forma — `multipart/form-data`

Oddiy forma faqat matn yuboradi. Fayl yuborish uchun formaga **ikkita** shart qo'yamiz: `method="post"` va `enctype="multipart/form-data"`. `enctype` — forma ma'lumotini qanday "o'rab" yuborilishini bildiradi; faylsiz formalar uchun bu shart emas, lekin **fayl** uchun majburiy. Maydon esa `<input type="file">` bo'ladi:

```html
<form method="post" action="yuklash.php" enctype="multipart/form-data">
    Rasm tanlang:
    <input type="file" name="rasm">
    <button type="submit">Yuklash</button>
</form>
```

> **Eng ko'p uchraydigan xato:** `enctype="multipart/form-data"` ni unutish. Usiz fayl serverga **kelmaydi** — `$_FILES` bo'sh bo'ladi va sababini topish qiyin bo'ladi. Fayl yuklash ishlamasa, birinchi navbatda shu satrni tekshiring.

### `$_FILES` strukturasi

Forma yuborilganda, fayl haqidagi ma'lumot `$_FILES` maxsus massiviga keladi (`$_POST` matn uchun, `$_FILES` fayllar uchun). `name="rasm"` maydoni uchun `$_FILES['rasm']` quyidagi kalitlarni saqlaydi:

```php
<?php
// Forma yuborilgandan keyin $_FILES['rasm'] taxminan shunday bo'ladi:
$_FILES['rasm'] = [
    "name"     => "mushuk.jpg",        // foydalanuvchi qurilmasidagi asl nom
    "type"     => "image/jpeg",        // brauzer aytgan MIME tur (ISHONCHSIZ!)
    "tmp_name" => "/tmp/phpA3f9.tmp",  // serverdagi vaqtinchalik manzil
    "error"    => 0,                   // xato kodi (0 = UPLOAD_ERR_OK = muvaffaqiyat)
    "size"     => 24576,               // hajmi (bayt)
];
```

Eng muhim kalitlar:
- **`tmp_name`** — fayl serverda **vaqtinchalik** shu yerga saqlanadi. Skript tugashi bilan o'chadi! Shuning uchun uni doimiy joyga **ko'chirishimiz** shart.
- **`error`** — yuklash holati. `0` (UPLOAD_ERR_OK) bo'lsagina hammasi joyida.
- **`size`** — hajm (bayt). O'lcham cheklash uchun kerak.
- **`name`** — faqat asl nomni bilish uchun. **Buni saqlash nomi sifatida ishonib ishlatmang** (pastda ko'ramiz).
- **`type`** — brauzer aytadi, foydalanuvchi yolg'on aytishi mumkin. **Bunga ishonmang** — haqiqiy turni `finfo` bilan tekshiramiz.

### Xato kodlari — `error`

`$_FILES['rasm']['error']` faqat `0` emas, turli holatlarni bildiruvchi kod qaytaradi. PHP ularga nom (konstanta) bergan. `match` (2-qism) bilan tushunarli xabarga aylantiramiz:

```php
<?php
function yuklashXatosi(int $kod): string
{
    return match ($kod) {
        UPLOAD_ERR_OK         => "Muvaffaqiyatli yuklandi",
        UPLOAD_ERR_INI_SIZE   => "Fayl server cheklovidan katta (php.ini)",
        UPLOAD_ERR_FORM_SIZE  => "Fayl forma cheklovidan katta",
        UPLOAD_ERR_PARTIAL    => "Fayl qisman yuklandi (ulanish uzildi)",
        UPLOAD_ERR_NO_FILE    => "Hech qanday fayl tanlanmadi",
        UPLOAD_ERR_NO_TMP_DIR => "Vaqtinchalik papka topilmadi",
        UPLOAD_ERR_CANT_WRITE => "Diskka yozib bo'lmadi",
        UPLOAD_ERR_EXTENSION  => "PHP kengaytmasi yuklashni to'xtatdi",
        default               => "Noma'lum xato (kod: $kod)",
    };
}

echo yuklashXatosi(0);   // Muvaffaqiyatli yuklandi
echo "\n";
echo yuklashXatosi(4);   // Hech qanday fayl tanlanmadi
echo "\n";
echo yuklashXatosi(1);   // Fayl server cheklovidan katta (php.ini)
```

Real kodda doim **birinchi navbatda** `error` ni tekshiramiz — agar `UPLOAD_ERR_OK` bo'lmasa, qolgan ishni davom ettirishdan ma'no yo'q.

### Faylni saqlash — `move_uploaded_file`

Vaqtinchalik fayl (`tmp_name`) skript tugashi bilan o'chadi. Uni doimiy saqlash uchun **`move_uploaded_file`** ishlatamiz — oddiy `rename` emas. Nega aynan u? Chunki `move_uploaded_file` qo'shimcha **xavfsizlik tekshiruvi** qiladi: fayl haqiqatan ham HTTP yuklash orqali kelganini tasdiqlaydi (hujumchi server ichidagi maxfiy faylni ko'rsatib qo'ya olmaydi).

```php
<?php
// Bu kod faqat haqiqiy forma yuborilganda ishlaydi (bu yerda namuna)
$manba = $_FILES['rasm']['tmp_name'];
$maqsad = __DIR__ . "/yuklamalar/rasm.jpg";

if (move_uploaded_file($manba, $maqsad)) {
    echo "Fayl saqlandi: " . $maqsad;
} else {
    echo "Saqlashda xato yuz berdi";
}
```

`__DIR__` — joriy fayl turgan papkaning to'liq manzili (sehrli konstanta). Maqsad manzilni shunday aniq belgilash kerak — nisbiy yo'lga (`yuklamalar/...`) ishonish chalkashlikka olib keladi.

## Validatsiya va xavfsizlik

Fayl yuklash — **hujumchilarning sevimli nuqtasi**. Tekshiruvsiz forma orqali kimdir `virus.php` yuklab, uni brauzerda ochib serveringizni egallashi mumkin. Quyidagi har bir tekshiruv — majburiy himoya qatlami.

### 1) O'lchamni cheklash

Cheksiz hajmni qabul qilmang — disk to'lib qolishi yoki server yuklanib qolishi mumkin. `size` ni belgilangan chegara bilan solishtiramiz:

```php
<?php
$maxHajm = 2 * 1024 * 1024;   // 2 MB (bayt hisobida)
$hajm = 1_500_000;            // namuna: $_FILES['rasm']['size'] o'rniga

if ($hajm > $maxHajm) {
    echo "Fayl juda katta! Eng ko'pi 2 MB.";
} else {
    echo "O'lcham joyida (" . round($hajm / 1024) . " KB)";
}
// O'lcham joyida (1465 KB)
```

> PHP'da raqamlarni o'qishli qilish uchun `_` ishlatish mumkin: `2_000_000` — ikki million. Bu faqat ko'rinish uchun, qiymatga ta'sir qilmaydi.

### 2) Haqiqiy turini tekshirish — `finfo` (faqat kengaytmaga ishonmang!)

Eng ko'p qilinadigan xato — fayl turini **kengaytma** (`.jpg`) yoki `$_FILES[...]['type']` bo'yicha tekshirish. Ikkalasini ham foydalanuvchi yolg'on ko'rsatishi mumkin: `virus.php` ni `rasm.jpg` deb nomlash yoki `type` ni qo'lda o'zgartirish oson.

To'g'ri yo'l — faylning **ichidagi haqiqiy mazmunini** o'qib turini aniqlash. PHP'da buni `finfo` (file info) qiladi — u faylning birinchi baytlariga ("sehrli raqamlar") qarab haqiqiy MIME turni topadi:

```php
<?php
// Namuna uchun haqiqiy kichik PNG fayl yaratamiz (1x1 piksel)
$pngBaytlar = base64_decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
);
file_put_contents("test.png", $pngBaytlar);

// Faylning HAQIQIY turini aniqlaymiz
$finfo = finfo_open(FILEINFO_MIME_TYPE);
$haqiqiyTur = finfo_file($finfo, "test.png");
finfo_close($finfo);

echo $haqiqiyTur;   // image/png

// Ruxsat etilgan turlar ro'yxati bilan solishtiramiz
$ruxsatEtilgan = ["image/jpeg", "image/png", "image/gif", "image/webp"];

if (in_array($haqiqiyTur, $ruxsatEtilgan, true)) {
    echo "\nFayl haqiqatan rasm — qabul qilamiz";
} else {
    echo "\nBu rasm emas! Rad etildi.";
}
```

Bu yondashuv — **oq ro'yxat** (whitelist): faqat aniq ruxsat etilgan turlarni o'tkazamiz, qolganlarini rad etamiz. Qora ro'yxat (".php ni taqiqlash") yomonroq — chunki xavfli kengaytmalar ko'p (`.php5`, `.phtml`, `.phar`) va birortasini unutish oson.

### 3) Xavfsiz noyob fayl nomi

Foydalanuvchi bergan nomni (`$_FILES[...]['name']`) saqlash nomi sifatida ishlatish **xavfli**:
- Ikki kishi `rasm.jpg` yuklasa — biri ikkinchisini o'chirib yuboradi.
- Nomda `../../../etc/passwd` kabi yo'l bo'lsa — boshqa papkaga yozib yuborishi mumkin (path traversal hujumi).
- Nomda `.php` bo'lsa — bajariladigan fayl yaratiladi.

Yechim — nomni **o'zimiz yasaymiz**: tasodifiy noyob nom + faqat ruxsat etilgan kengaytma. `uniqid` (unique id — noyob identifikator) takrorlanmas satr beradi:

```php
<?php
// Haqiqiy turdan kengaytmani o'zimiz tanlaymiz (foydalanuvchi nomidan EMAS)
$turKengaytma = [
    "image/jpeg" => "jpg",
    "image/png"  => "png",
    "image/gif"  => "gif",
    "image/webp" => "webp",
];

$haqiqiyTur = "image/png";   // namuna (finfo natijasi)
$kengaytma = $turKengaytma[$haqiqiyTur];

// Noyob, xavfsiz nom yasaymiz
$xavfsizNom = uniqid("rasm_", true) . "." . $kengaytma;
echo $xavfsizNom;   // masalan: rasm_6651a3b9c4d7e1.23456789.png
```

Bu nomda foydalanuvchi ma'lumotidan hech narsa qolmaydi — demak `../` ham, `.php` ham bo'lishi mumkin emas. Kengaytmani esa `finfo` topgan **haqiqiy turdan** olamiz, faylning asl nomidan emas.

### 4) Web-root tashqarisiga saqlash

Imkon bo'lsa, yuklangan fayllarni veb-saytning ochiq papkasidan (`public/`, `htdocs/`) **tashqarida** saqlang. Sababi: agar hujumchi nazoratdan o'tib `.php` fayl yuklasa ham, u brauzerda ochib ishga tushira olmaydi — chunki fayl veb orqali ko'rinmaydigan joyda. Foydalanuvchiga ko'rsatish kerak bo'lsa, faylni PHP skript orqali "uzatamiz" (readfile bilan), to'g'ridan-to'g'ri havola bermaymiz.

```php
<?php
// Yomon: web orqali to'g'ridan-to'g'ri ochiladigan papka
//   /var/www/html/uploads/   ← .php yuklansa, ishga tushadi!

// Yaxshi: web-root TASHQARISIDAGI papka
$saqlashPapka = __DIR__ . "/../storage/uploads/";
echo "Fayllar shu yerda saqlanadi: " . $saqlashPapka;
// Bu papka brauzerdan to'g'ridan-to'g'ri ochilmaydi
```

### To'liq misol — xavfsiz rasm yuklash

Endi barcha tekshiruvlarni bitta funksiyada birlashtiramiz. Bu — real loyihada ishlatsa bo'ladigan namuna: o'lcham, haqiqiy MIME tur, noyob nom va xavfsiz saqlash. Funksiya muvaffaqiyatda saqlangan fayl nomini, xatoda xato matnini qaytaradi:

```php
<?php

/**
 * Yuklangan rasmni tekshirib, xavfsiz saqlaydi.
 * Muvaffaqiyatda: ['ok' => true, 'fayl' => 'nom.jpg']
 * Xatoda:        ['ok' => false, 'xato' => 'sabab']
 */
function rasmYukla(array $fayl, string $saqlashPapka): array
{
    // 1) Yuklash xatosini tekshiramiz
    if ($fayl["error"] !== UPLOAD_ERR_OK) {
        return ["ok" => false, "xato" => "Yuklashda xato (kod: {$fayl['error']})"];
    }

    // 2) O'lcham cheklovi — 2 MB
    $maxHajm = 2 * 1024 * 1024;
    if ($fayl["size"] > $maxHajm) {
        return ["ok" => false, "xato" => "Fayl 2 MB dan katta"];
    }

    // 3) HAQIQIY MIME turini aniqlaymiz (kengaytmaga ishonmaymiz!)
    $ruxsat = [
        "image/jpeg" => "jpg",
        "image/png"  => "png",
        "image/gif"  => "gif",
        "image/webp" => "webp",
    ];

    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $tur = finfo_file($finfo, $fayl["tmp_name"]);
    finfo_close($finfo);

    if (!isset($ruxsat[$tur])) {
        return ["ok" => false, "xato" => "Faqat rasm fayllari (jpg, png, gif, webp)"];
    }

    // 4) Papka mavjudligini ta'minlaymiz
    if (!is_dir($saqlashPapka)) {
        mkdir($saqlashPapka, 0755, true);
    }

    // 5) Noyob xavfsiz nom + to'g'ri kengaytma
    $kengaytma = $ruxsat[$tur];
    $yangiNom = uniqid("img_", true) . "." . $kengaytma;
    $toliqYol = rtrim($saqlashPapka, "/") . "/" . $yangiNom;

    // 6) Vaqtinchalik fayldan doimiy joyga ko'chiramiz
    if (!move_uploaded_file($fayl["tmp_name"], $toliqYol)) {
        return ["ok" => false, "xato" => "Faylni saqlab bo'lmadi"];
    }

    return ["ok" => true, "fayl" => $yangiNom];
}

// Haqiqiy ishlatilishi (forma yuborilganda):
//
// if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES["rasm"])) {
//     $natija = rasmYukla($_FILES["rasm"], __DIR__ . "/../storage/uploads/");
//     if ($natija["ok"]) {
//         echo "Saqlandi: " . $natija["fayl"];
//     } else {
//         echo "Xato: " . $natija["xato"];
//     }
// }

echo "Funksiya tayyor (real forma bilan ishlaydi)";
```

Bu funksiyaning kuchi — **har bir bosqichda** to'xtab tekshirishida: xato bo'lsa, darrov tushunarli sabab bilan qaytadi va keyingi xavfli amalni bajarmaydi. Aynan shunday "darvoza"lar yuza kodni professional koddan ajratib turadi.

### Bonus — oddiy log yozuvchi

Bobni amaliy vosita bilan yakunlaymiz: ilovangizdagi muhim hodisalarni faylga yozuvchi kichik log funksiyasi. Sana-vaqt bilan, `FILE_APPEND` rejimida — xuddi real loyihalardagidek:

```php
<?php
function log_yoz(string $xabar, string $sath = "INFO"): void
{
    $vaqt = date("Y-m-d H:i:s");
    $qator = "[{$vaqt}] {$sath}: {$xabar}" . PHP_EOL;
    file_put_contents("ilova.log", $qator, FILE_APPEND);
}

log_yoz("Server ishga tushdi");
log_yoz("Foydalanuvchi #42 kirdi", "INFO");
log_yoz("Bazaga ulanib bo'lmadi", "ERROR");

echo file_get_contents("ilova.log");
// [2026-06-11 10:30:00] INFO: Server ishga tushdi
// [2026-06-11 10:30:00] INFO: Foydalanuvchi #42 kirdi
// [2026-06-11 10:30:00] ERROR: Bazaga ulanib bo'lmadi
```

`PHP_EOL` — operatsion tizimga mos yangi qator belgisi (Windows va Linux farq qiladi). `date("Y-m-d H:i:s")` — joriy sana va vaqtni o'qishli formatda beradi (sana-vaqt mavzusi alohida bobda batafsil).

### Mashqlar

**Oson**

1. `file_put_contents` bilan `ism.txt` fayliga o'z ismingizni yozing, keyin `file_get_contents` bilan o'qib ekranga chiqaring.
2. Bir matnni uch qatorga (`\n` bilan) `file_put_contents` orqali yozing, so'ng `file` funksiyasi bilan massivga o'qib, qatorlar sonini (`count`) chiqaring.
3. `fopen` ni `"w"` rejimida ishlatib, faylga `fwrite` bilan ikki qator yozing va `fclose` bilan yoping.
4. `file_exists` bilan biror fayl bor-yo'qligini tekshiring; bo'lmasa "fayl yo'q" deb chiqaring.
5. `FILE_APPEND` bayrog'idan foydalanib, bitta faylga uch marta uch xil qator qo'shing, keyin to'liq o'qib ko'ring.

**O'rta**

6. Quyidagi CSV ni faylga yozing va `fgetcsv` bilan qator-qator o'qib, har bir talabaning ismi va bahosini chiqaring:
   `ism,baho` / `Ali,90` / `Vali,75` / `Guli,85`.
7. Bir nechta mahsulot massivini (`[nomi, narxi]`) `fputcsv` bilan CSV faylga yozing.
8. `scandir` bilan bir papkadagi fayllar ro'yxatini oling va `.` hamda `..` ni chiqarib tashlab, qolganini ko'rsating.
9. Forma orqali kelgan faylning (`$_FILES['hujjat']`) `error` kodini olib, `match` bilan tushunarli xabarga aylantiruvchi funksiya yozing (`UPLOAD_ERR_OK`, `UPLOAD_ERR_NO_FILE`, `UPLOAD_ERR_INI_SIZE` ni qamrang).
10. Berilgan hajm (bayt) 2 MB dan katta yoki kichikligini tekshiruvchi funksiya yozing; natijani KB da ham ko'rsating.

**Qiyin**

11. `finfo` yordamida fayl haqiqiy MIME turini aniqlang va u `["image/jpeg", "image/png"]` ro'yxatida bor-yo'qligini tekshiring (oq ro'yxat). Test uchun kichik PNG fayl yarating.
12. Foydalanuvchi bergan fayl nomidan **mustaqil** ravishda, `uniqid` va haqiqiy MIME turdan olingan kengaytma bilan xavfsiz noyob nom yasovchi funksiya yozing.
13. To'liq xavfsiz rasm yuklash funksiyasini yozing: o'lcham (max 1 MB), `finfo` bilan MIME tekshiruvi, noyob nom va `move_uploaded_file`. Natijada `['ok' => bool, ...]` qaytsin.
14. Sana-vaqtli log funksiyasi yozing (`log_yoz($xabar, $sath)`), u har bir yozuvni `FILE_APPEND` bilan yangi qatorga qo'shsin; keyin uni 4-5 marta chaqirib, log faylni o'qib ko'rsating.
15. Kichik "sozlama" tizimi yozing: `key=value` ko'rinishidagi qatorlardan iborat faylni `file` bilan o'qib, massivga (`['kalit' => 'qiymat']`) aylantiruvchi funksiya tuzing.

<details markdown="1">
<summary>Yechim — 6 (CSV o'qish)</summary>

```php
<?php
$csv = "ism,baho\nAli,90\nVali,75\nGuli,85\n";
file_put_contents("baholar.csv", $csv);

$fayl = fopen("baholar.csv", "r");
$sarlavha = fgetcsv($fayl, escape: "");   // birinchi qatorni (ustun nomlarini) o'tkazib yuboramiz

while (($qator = fgetcsv($fayl, escape: "")) !== false) {
    echo $qator[0] . ": " . $qator[1] . " ball\n";
}
fclose($fayl);
// Ali: 90 ball
// Vali: 75 ball
// Guli: 85 ball
```

`fgetcsv` har qatorni massiv qilib qaytaradi; `$qator[0]` — ism, `$qator[1]` — baho. Fayl oxirida `false` qaytgani uchun `while` to'xtaydi.
</details>

<details markdown="1">
<summary>Yechim — 9 (xato kodlari)</summary>

```php
<?php
function yuklashHolati(int $kod): string
{
    return match ($kod) {
        UPLOAD_ERR_OK       => "Muvaffaqiyatli yuklandi",
        UPLOAD_ERR_NO_FILE  => "Fayl tanlanmadi",
        UPLOAD_ERR_INI_SIZE => "Fayl ruxsat etilgan hajmdan katta",
        default             => "Boshqa xato (kod: $kod)",
    };
}

echo yuklashHolati(UPLOAD_ERR_OK) . "\n";       // Muvaffaqiyatli yuklandi
echo yuklashHolati(UPLOAD_ERR_NO_FILE) . "\n";  // Fayl tanlanmadi
echo yuklashHolati(99);                         // Boshqa xato (kod: 99)
```

`match` — `switch` ning zamonaviy, qisqa varianti (2-qism). Har bir holatni aniq qiymatga moslaydi; mos kelmaganini `default` ushlaydi.
</details>

<details markdown="1">
<summary>Yechim — 12 (xavfsiz noyob nom)</summary>

```php
<?php
function xavfsizNom(string $haqiqiyTur, string $prefiks = "fayl_"): ?string
{
    $turlar = [
        "image/jpeg" => "jpg",
        "image/png"  => "png",
        "image/gif"  => "gif",
        "image/webp" => "webp",
    ];

    // Ruxsat etilmagan tur — null qaytaramiz
    if (!isset($turlar[$haqiqiyTur])) {
        return null;
    }

    $kengaytma = $turlar[$haqiqiyTur];
    return uniqid($prefiks, true) . "." . $kengaytma;
}

echo xavfsizNom("image/png") . "\n";    // masalan: fayl_6651...png
echo xavfsizNom("image/jpeg") . "\n";   // masalan: fayl_6651...jpg
var_dump(xavfsizNom("application/x-php"));   // NULL (ruxsat yo'q)
```

Diqqat: kengaytmani **faqat haqiqiy MIME turdan** olamiz, foydalanuvchi yuborgan fayl nomidan emas. Shu sabab `.php` yoki `../` umuman nomga tushmaydi.
</details>

<details markdown="1">
<summary>Yechim — 13 (to'liq xavfsiz yuklash)</summary>

```php
<?php
function rasmYukla(array $fayl, string $papka): array
{
    // 1) Yuklash xatosi
    if ($fayl["error"] !== UPLOAD_ERR_OK) {
        return ["ok" => false, "xato" => "Yuklash xatosi: {$fayl['error']}"];
    }

    // 2) O'lcham — max 1 MB
    if ($fayl["size"] > 1 * 1024 * 1024) {
        return ["ok" => false, "xato" => "Fayl 1 MB dan katta"];
    }

    // 3) Haqiqiy MIME tur (oq ro'yxat)
    $ruxsat = ["image/jpeg" => "jpg", "image/png" => "png"];
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $tur = finfo_file($finfo, $fayl["tmp_name"]);
    finfo_close($finfo);

    if (!isset($ruxsat[$tur])) {
        return ["ok" => false, "xato" => "Faqat JPG yoki PNG"];
    }

    // 4) Papka + noyob nom
    if (!is_dir($papka)) {
        mkdir($papka, 0755, true);
    }
    $nom = uniqid("img_", true) . "." . $ruxsat[$tur];
    $yol = rtrim($papka, "/") . "/" . $nom;

    // 5) Ko'chirish
    if (!move_uploaded_file($fayl["tmp_name"], $yol)) {
        return ["ok" => false, "xato" => "Saqlab bo'lmadi"];
    }

    return ["ok" => true, "fayl" => $nom];
}
```

Tartib muhim: avval **arzon** tekshiruvlar (xato kodi, o'lcham), keyin **qimmatroq** (`finfo` faylni o'qiydi), eng oxirida **ko'chirish**. Bironta tekshiruv o'tmasa, keyingi xavfli amal umuman bajarilmaydi.
</details>

<details markdown="1">
<summary>Yechim — 15 (sozlama o'qigich)</summary>

```php
<?php
// Namuna sozlama fayl yaratamiz
file_put_contents("sozlama.txt", "sayt=Mening Saytim\ntil=uz\ndebug=true\n");

function sozlamaOqi(string $fayl): array
{
    $natija = [];
    $qatorlar = file($fayl, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

    foreach ($qatorlar as $qator) {
        // "=" bo'yicha faqat BIRINCHI marta bo'lamiz (qiymatda = bo'lishi mumkin)
        if (!str_contains($qator, "=")) {
            continue;   // noto'g'ri qatorni o'tkazamiz
        }
        [$kalit, $qiymat] = explode("=", $qator, 2);
        $natija[trim($kalit)] = trim($qiymat);
    }

    return $natija;
}

$sozlama = sozlamaOqi("sozlama.txt");
print_r($sozlama);
// Array ( [sayt] => Mening Saytim [til] => uz [debug] => true )

echo $sozlama["til"];   // uz
```

Muhim nuqta: `explode("=", $qator, 2)` dagi `2` — eng ko'pi 2 bo'lakka bo'l, demak qiymat ichidagi `=` saqlanadi. Bu `.env` fayllari ishlatadigan haqiqiy usul.
</details>
