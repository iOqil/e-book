# 2.10 Xatolarni boshqarish (try / catch)

[⬅️ Oldingi: 2.9 Enum — cheklangan tanlovlar](./22-enum-cheklangan-tanlovlar.md) · [🏠 README](./README.md) · [Keyingi: 2.11 Magic metodlar ➡️](./magic-metodlar.md)

---

### Muammo: xatolar dasturni "o'ldiradi"

Ba'zan kodda xato yuz beradi: foydalanuvchi noto'g'ri ma'lumot kiritadi, fayl topilmaydi, nolga bo'lish sodir bo'ladi. Agar buni boshqarmasangiz, dastur to'satdan to'xtaydi va foydalanuvchi xunuk xato xabarini ko'radi. Bizga xatolarni **chiroyli boshqarish** kerak.

### `try` / `catch` — xatoni "ushlash"

Asosiy g'oya: xato bo'lishi mumkin bo'lgan kodni `try` ("urinib ko'r") blokiga yozasiz. Agar xato yuz bersa, `catch` ("ushla") bloki uni ushlaydi va dastur to'xtamaydi:

```php
<?php
try {
    // Xato bo'lishi mumkin bo'lgan kod
    $natija = 10 / 0;   // nolga bo'lish — xato!
    echo $natija;
} catch (DivisionByZeroError $e) {
    // Xato yuz bersa — bu yer ishlaydi
    echo "Xato: nolga bo'lib bo'lmaydi!";
}

echo "<br>Dastur davom etmoqda...";   // dastur to'xtamadi
```

Nima sodir bo'ldi:
- **`try { ... }`** — "shu kodni bajarishga urinib ko'r".
- Ichida xato yuz berdi (nolga bo'lish).
- **`catch (...) { ... }`** — xato yuz berganda darrov bu yerga "sakraydi" va xato xabarini chiqaradi.
- Eng muhimi: dastur **to'xtamadi** — keyingi kod ("Dastur davom etmoqda...") ham ishladi.

`$e` — bu "xato haqidagi ma'lumot" (error obyekti). Undan xato haqida ma'lumot olish mumkin: `$e->getMessage()` xato matnini qaytaradi.

### Exception iyerarxiyasi — `Throwable`, `Error`, `Exception`

Bir savol tug'iladi: yuqorida biz `DivisionByZeroError` ni, boshqa joyda esa `Exception` ni ushladik. Ular qayerdan keladi? PHP'da barcha "tashlanadigan" (ushlash mumkin bo'lgan) xatolar bitta umumiy oilaga tegishli. Eng tepada — `Throwable` (so'zma-so'z: "tashlanadigan") interfeysi turadi. Undan ikkita katta tarmoq chiqadi:

- **`Error`** — bu **dasturiy yoki tizim xatosi**. Ya'ni dasturchi xato qilgan yoki tizimda jiddiy muammo bor. Masalan: `TypeError` (noto'g'ri tipdagi argument berildi), `DivisionByZeroError` (nolga bo'lish), `ParseError` (kod sintaksisi buzilgan). Bularni odatda **tuzatish** kerak, ushlab "yashirish" emas.
- **`Exception`** — bu **boshqariladigan xato**. Ya'ni "kutilgan", normal hayotiy holat: foydalanuvchi noto'g'ri yosh kiritdi, fayl topilmadi, balans yetarli emas. Bularni `try/catch` bilan ushlab, chiroyli boshqarish — odatiy holat.

Quyidagi sxema oilani ko'rsatadi:

```
        Throwable  (interfeys — hammasining boshi)
        /        \
     Error       Exception
       |             |
  TypeError     RuntimeException
  ValueError    InvalidArgumentException
  DivisionBy...  LogicException
  ...           (va siz yozgan o'z exception'laringiz)
```

Keling, farqni amalda ko'ramiz:

```php
<?php
// Error — tizim/dasturiy xato (TypeError)
function kvadrat(int $son): int {
    return $son * $son;
}

try {
    echo kvadrat("salom");   // ❌ int kutilyapti, lekin matn berildi
} catch (TypeError $e) {
    echo "TypeError ushlandi: " . $e->getMessage() . "\n";
}

// Exception — boshqariladigan xato
try {
    throw new Exception("Bu boshqariladigan xato");
} catch (Exception $e) {
    echo "Exception ushlandi: " . $e->getMessage() . "\n";
}

// Throwable — ikkalasini ham ushlaydi
try {
    throw new TypeError("Tip xatosi");
} catch (Throwable $e) {
    echo "Throwable ushladi: " . $e->getMessage() . "\n";
}
```

Natija:

```
TypeError ushlandi: kvadrat(): Argument #1 ($son) must be of type int, string given, ...
Exception ushlandi: Bu boshqariladigan xato
Throwable ushladi: Tip xatosi
```

Asosiy xulosa:
- `catch (Exception $e)` — faqat `Exception` va undan meros olganlarni ushlaydi. `TypeError` (u `Error` oilasidan) bu yerga **tushmaydi**.
- `catch (Throwable $e)` — hamma narsani ushlaydi: ham `Error`, ham `Exception`. Buni ehtiyotkorlik bilan ishlatish kerak: ba'zan `Error` ni ushlamaslik to'g'riroq, chunki u dasturdagi haqiqiy xatoni ko'rsatadi va uni tuzatish kerak (yashirish emas).

Amaliy qoida: kundalik kodda odatda `Exception` (yoki uning aniq turlari) ni ushlaysiz. `Error` ni faqat juda kerak bo'lganda (masalan, butun ilovani qulashdan saqlovchi eng tashqi "himoya devori"da) ushlaysiz.

### O'zingiz xato "tashlash" — `throw`

Ba'zan o'zingiz xato signalini berishingiz kerak. Masalan, "yosh manfiy bo'lmasligi kerak". Buning uchun `throw` ("tashla") ishlatiladi:

```php
<?php
function yoshTekshir($yosh) {
    if ($yosh < 0) {
        throw new Exception("Yosh manfiy bo'lishi mumkin emas");
    }
    return "Yosh: " . $yosh;
}

try {
    echo yoshTekshir(-5);   // bu xato tashlaydi
} catch (Exception $e) {
    echo "Xatolik: " . $e->getMessage();   // Xatolik: Yosh manfiy bo'lishi mumkin emas
}
```

Tushuntiramiz:
- **`throw new Exception("...")`** — "xato signalini tashla, shu matn bilan". `throw` bajarilishi bilan funksiya darrov to'xtaydi va xato "yuqoriga" — uni chaqirgan `try` ga uchadi.
- `catch` uni ushlaydi va `$e->getMessage()` orqali xato matnini oladi.

Bu — ma'lumotni tekshirishning toza usuli: funksiya "men bu ma'lumot bilan ishlay olmayman" deb signal beradi, chaqiruvchi esa uni `try/catch` bilan boshqaradi.

### Qachon `throw` qilish, qachon qaytarish (return)

Yangi boshlovchilar ko'p beradigan savol: "Xatoda har doim `throw` qilaymi, yoki ba'zan oddiy `null`/`false` qaytarsam bo'ladimi?" Javob — **vaziyatga bog'liq**, va to'g'ri tanlash kodingizni ancha toza qiladi.

Oddiy qoida:
- **`null` (yoki `false`) qaytaring** — agar "natija yo'qligi" **normal, kutilgan** holat bo'lsa. Masalan, ro'yxatdan foydalanuvchini qidirdingiz va topilmadi. Bu xato emas — shunchaki "yo'q".
- **`throw` qiling** — agar **qoida buzilgan** bo'lsa, ya'ni funksiya o'z ishini umuman bajara olmaydigan, "bunday bo'lmasligi kerak" degan holat yuz bersa. Masalan, yoshga `200` berildi, yoki summa manfiy.

```php
<?php
// 1-usul: oddiy "topilmadi" — qaytarish (null) yetarli
function foydalanuvchiTop(array $royxat, int $id): ?string {
    return $royxat[$id] ?? null;   // topilmasa null
}

// 2-usul: qoida buzilishi — exception tashlash kerak
function yoshTekshir(int $yosh): int {
    if ($yosh < 0 || $yosh > 150) {
        throw new RangeException("Yosh 0..150 oralig'ida bo'lishi kerak");
    }
    return $yosh;
}

$royxat = [1 => "Ali", 2 => "Vali"];
echo (foydalanuvchiTop($royxat, 5) ?? "topilmadi") . "\n";   // topilmadi
echo foydalanuvchiTop($royxat, 1) . "\n";                    // Ali

try {
    echo yoshTekshir(200) . "\n";
} catch (RangeException $e) {
    echo "Xato: " . $e->getMessage() . "\n";   // Xato: Yosh 0..150 oralig'ida bo'lishi kerak
}
```

Nega bu muhim? Agar siz **har bir** "yo'q" holatga exception tashlasangiz, kod `try/catch` larga to'lib ketadi va o'qish qiyinlashadi. Aksincha, **haqiqiy** qoidabuzarlikda `null` qaytarsangiz, chaqiruvchi uni e'tiborsiz qoldirib, keyinroq tushunarsiz xatoga duch keladi. To'g'ri tanlov — kodni ham toza, ham ishonchli qiladi.

Bitta `RangeException`, `InvalidArgumentException` kabi nomlarni ishlatganimizga e'tibor bering — bular PHP'da tayyor turgan, `Exception` dan meros olgan **maxsus turlar**. Ular xatoning "ma'nosini" aniqroq bildiradi. Keyingi bo'limda o'zimiznikini ham yozamiz.

### O'z exception klassingiz — `extends Exception`

Tayyor `Exception` yetarli bo'lmasa, o'zingizning **maxsus xato turingizni** yaratishingiz mumkin. Bu juda foydali: aynan shu turdagi xatoni `catch` qilib, boshqalardan ajratib ushlay olasiz. Buning uchun `Exception` dan meros olamiz (`extends`):

```php
<?php
// O'z exception turimiz — bo'sh klass yetarli (faqat nom kerak)
class MablagYetarliEmasException extends Exception {}

class Hisob {
    public function __construct(private int $balans) {}

    public function pulYechish(int $summa): int {
        if ($summa > $this->balans) {
            throw new MablagYetarliEmasException(
                "Mablag' yetarli emas. Balans: {$this->balans}, so'ralgan: {$summa}"
            );
        }
        $this->balans -= $summa;
        return $this->balans;
    }
}

$hisob = new Hisob(100000);

try {
    $hisob->pulYechish(150000);
} catch (MablagYetarliEmasException $e) {
    // AYNAN shu turdagi xatoni ushlaymiz
    echo "Maxsus xato ushlandi: " . $e->getMessage() . "\n";
} catch (Exception $e) {
    // Boshqa har qanday xato bu yerga tushadi
    echo "Umumiy xato: " . $e->getMessage() . "\n";
}
```

Natija:

```
Maxsus xato ushlandi: Mablag' yetarli emas. Balans: 100000, so'ralgan: 150000
```

Nimaga e'tibor berish kerak:
- **`class MablagYetarliEmasException extends Exception {}`** — ichi bo'sh bo'lsa ham, bu to'liq ishlaydigan exception. U `Exception` ning hamma imkoniyatini (xabar, kod, `getMessage()` va h.k.) meros qilib oladi. Bizga faqat **alohida nom** kerak edi.
- Endi `catch (MablagYetarliEmasException $e)` deb **aynan shu** xatoni ushlay olamiz va boshqa xatolardan ajratamiz.
- `catch` larni **tartib** bilan yozish muhim: aniqrog'i (`MablagYetarliEmasException`) yuqorida, umumiyrog'i (`Exception`) pastda turishi kerak. PHP yuqoridan pastga qarab birinchi mos kelganini ishlatadi.

Real loyihalarda bu juda keng tarqalgan: `ValidatsiyaException`, `TolovException`, `FaylTopilmadiException` kabi o'z turlaringizni yaratib, har xil xato turlarini aniq boshqarasiz.

### Bir nechta turni birga ushlash — multi-catch (`|`)

Ba'zan bir nechta **har xil turdagi** xato uchun **bir xil** ish qilmoqchisiz. Har biriga alohida `catch` yozish — takror kod. PHP'da ularni `|` ("yoki") belgisi bilan **bitta** `catch` da birlashtirish mumkin:

```php
<?php
function yoshniOl(mixed $qiymat): int {
    $yosh = (int) $qiymat;
    if ($yosh < 0) {
        throw new ValueError("Yosh manfiy bo'lishi mumkin emas");
    }
    return $yosh;
}

function sinab(mixed $qiymat): void {
    try {
        if (is_array($qiymat)) {
            throw new TypeError("Massiv emas, son kerak");
        }
        echo "Yosh: " . yoshniOl($qiymat) . "\n";
    } catch (TypeError | ValueError $e) {
        // Ikkala xato turini ham BITTA blok ushlaydi
        echo get_class($e) . ": " . $e->getMessage() . "\n";
    }
}

sinab(25);            // Yosh: 25
sinab(-3);            // ValueError: Yosh manfiy bo'lishi mumkin emas
sinab([1, 2, 3]);     // TypeError: Massiv emas, son kerak
```

Tushuntiramiz:
- **`catch (TypeError | ValueError $e)`** — "agar `TypeError` YOKI `ValueError` bo'lsa, shu blokni ishlat". Ikkalasiga ham bir xil javob beramiz.
- `get_class($e)` — ushlangan obyekt qaysi turdan ekanini ko'rsatadi (xatoni log qilishda foydali).

Bu — kodni qisqartirishning chiroyli usuli: takrorlanadigan ikki `catch` o'rniga bitta yozasiz. Agar har bir tur uchun **boshqacha** javob kerak bo'lsa — o'shanda alohida `catch` lar yozasiz.

### `finally` — har doim bajariladigan qism

Ba'zan, xato bo'ladimi-yo'qmi, biror ish **albatta** bajarilishi kerak (masalan, faylni yopish). Buning uchun `finally` bor:

```php
<?php
try {
    echo "Ish boshlandi<br>";
    throw new Exception("Biror xato");
} catch (Exception $e) {
    echo "Xato ushlandi<br>";
} finally {
    echo "Bu qism HAR DOIM bajariladi";   // xato bo'lsa ham, bo'lmasa ham
}
```

Quyidagi diagramma `try / catch / finally` oqimini ko'rsatadi: `try` ichida xato bo'lsa `catch` ushlaydi, bo'lmasa `catch` o'tkazib yuboriladi — `finally` esa har ikki holatda ham bajariladi va dastur to'xtamaydi:

![try / catch / finally oqimi: xato ushlash va finally har doim bajarilishi](rasmlar/phb-try-catch.svg)

### `finally` bilan resursni xavfsiz yopish

`finally` ning eng kuchli amaliy foydasi — **resursni tozalash**. Fayl, ma'lumotlar bazasi ulanishi, tarmoq soketi — bularni ochgandan keyin **albatta yopish** kerak, hatto o'rtada xato chiqib ketsa ham. `finally` aynan shuni kafolatlaydi: u ichidagi kod **har qanday** holatda ishlaydi — xato bo'lsa ham, hatto `try` ichida `return` bo'lsa ham.

```php
<?php
function faylgaYoz(string $yol, string $matn, bool $xatoBoladimi): void {
    $fayl = fopen($yol, "w");   // resurs ochildi
    echo "Fayl ochildi\n";
    try {
        if ($xatoBoladimi) {
            throw new RuntimeException("Yozishda muammo");
        }
        fwrite($fayl, $matn);
        echo "Matn yozildi\n";
    } finally {
        fclose($fayl);          // HAR DOIM yopiladi — xato bo'lsa ham
        echo "Fayl yopildi\n";
    }
}

$yol = sys_get_temp_dir() . "/test_ch23.txt";

faylgaYoz($yol, "Salom", false);
echo "---\n";
try {
    faylgaYoz($yol, "Salom", true);   // bu safar xato bo'ladi
} catch (RuntimeException $e) {
    echo "Tashqarida ushlandi: " . $e->getMessage() . "\n";
}
```

Natija:

```
Fayl ochildi
Matn yozildi
Fayl yopildi
---
Fayl ochildi
Fayl yopildi
Tashqarida ushlandi: Yozishda muammo
```

Diqqat qiling: ikkinchi chaqiruvda xato bo'lsa **ham**, "Fayl yopildi" baribir chiqdi — `finally` ishladi. Bu yerda `catch` ham yo'q (faqat `try/finally`): xato `finally` dan keyin "yuqoriga" uchib ketdi va uni tashqaridagi `try/catch` ushladi. Ya'ni `finally` xatoni "yutib yubormaydi" — u faqat tozalashni kafolatlaydi, xato esa o'z yo'lida davom etadi. Bu — fayl ochiq qolib, resurs "oqib ketishi"ning (resource leak) oldini oladi.

### Exception zanjiri — `previous` (asl sababni saqlash)

Katta dasturlarda xato ko'pincha "qatlamlardan" o'tadi: past daraja (ma'lumotlar bazasi) bir xato beradi, yuqori daraja (xizmat) uni o'rab, tushunarliroq xato tashlaydi. Lekin **asl sababni** yo'qotmaslik kerak — debugging uchun u juda muhim. Buning uchun exception'larni **zanjir** qilib bog'laymiz: yangi xatoni tashlaganda, eski xatoni `previous` ("oldingi") argument sifatida beramiz.

```php
<?php
class BazaException extends Exception {}
class XizmatException extends Exception {}

function bazadanOl(): never {
    throw new BazaException("Ulanish uzildi (port 3306)");
}

function foydalanuvchiOl(): void {
    try {
        bazadanOl();
    } catch (BazaException $past) {
        // Past darajadagi xatoni "o'rab", yangi, tushunarli xato tashlaymiz
        throw new XizmatException(
            "Foydalanuvchini olib bo'lmadi",
            previous: $past
        );
    }
}

try {
    foydalanuvchiOl();
} catch (XizmatException $e) {
    echo "Yuqori xato: " . $e->getMessage() . "\n";
    $sabab = $e->getPrevious();   // asl sababni olamiz
    if ($sabab !== null) {
        echo "Asl sabab: " . $sabab->getMessage() . "\n";
    }
}
```

Natija:

```
Yuqori xato: Foydalanuvchini olib bo'lmadi
Asl sabab: Ulanish uzildi (port 3306)
```

Tushuntiramiz:
- **`new XizmatException("...", previous: $past)`** — `Exception` konstruktorining uchinchi argumenti `previous`. Biz unga eski xatoni (`$past`) beramiz. (`previous:` — bu **nomli argument**, 8.x uslubi; xohlasangiz `new XizmatException("...", 0, $past)` ham yozsa bo'ladi.)
- **`$e->getPrevious()`** — zanjirning oldingi halqasini, ya'ni asl sababni qaytaradi. Agar yo'q bo'lsa `null`.
- `bazadanOl()` ning qaytish tipi **`never`** — bu "bu funksiya hech qachon normal qaytmaydi (har doim xato tashlaydi)" degani. Bu 8.1+ dagi foydali belgi.

Nega bu foydali? Foydalanuvchiga "Foydalanuvchini olib bo'lmadi" degan tushunarli xabarni ko'rsatasiz, lekin dasturchi sifatida log'da **asl** sababni ("Ulanish uzildi (port 3306)") ko'rasiz. Ikki dunyoning yaxshisi.

### Xato haqida ma'lumot olish — `getMessage`, `getCode`, `getLine`, `getTrace`

Ushlangan `$e` obyektida faqat `getMessage()` emas, balki yana bir nechta foydali metod bor. Ular xatoni **log qilish** va **debugging** uchun zarur:

```php
<?php
function bol(int $a, int $b): float {
    if ($b === 0) {
        throw new InvalidArgumentException("Nolga bo'lib bo'lmaydi", 422);
    }
    return $a / $b;
}

try {
    echo bol(10, 0);
} catch (InvalidArgumentException $e) {
    echo "Xabar (getMessage): " . $e->getMessage() . "\n";
    echo "Kod (getCode): " . $e->getCode() . "\n";
    echo "Qator (getLine): " . $e->getLine() . "\n";
    echo "Fayl (getFile): " . basename($e->getFile()) . "\n";
    echo "Iz (getTraceAsString) birinchi qatori:\n";
    $iz = explode("\n", $e->getTraceAsString());
    echo "  " . $iz[0] . "\n";
}
```

Natija (taxminan):

```
Xabar (getMessage): Nolga bo'lib bo'lmaydi
Kod (getCode): 422
Qator (getLine): 4
Fayl (getFile): t6-methods.php
Iz (getTraceAsString) birinchi qatori:
  #0 .../t6-methods.php(10): bol(10, 0)
```

Har bir metod nima beradi:
- **`getMessage()`** — xato matni (`throw` da yozganingiz).
- **`getCode()`** — xato kodi (raqam). `throw new ...("xabar", 422)` — ikkinchi argument kod. Ko'pincha HTTP holat kodi (404, 422, 500) yoki o'z raqamli belgilaringiz uchun ishlatiladi.
- **`getLine()`** — xato **qaysi qatorda** tashlangani.
- **`getFile()`** — xato **qaysi faylda** tashlangani.
- **`getTraceAsString()`** — to'liq "iz" (stack trace): qaysi funksiya qaysi funksiyani chaqirib, qayerda xatoga kelganini ko'rsatadigan zanjir. Debugging'da eng qimmatli ma'lumot.

Amaliyotda foydalanuvchiga faqat chiroyli `getMessage()` ni ko'rsatasiz, log faylga esa hammasini (`getFile`, `getLine`, `getTraceAsString`) yozasiz — keyin muammoni aniq topish uchun.

### `set_error_handler` — eski "warning"larni ham ushlash (qisqacha)

`try/catch` faqat **exception**'larni ushlaydi. Lekin PHP'ning ba'zi eski funksiyalari (masalan `file_get_contents`) xato bo'lganda exception **tashlamaydi** — ular shunchaki **"warning"** (ogohlantirish) chiqarib, ishni davom ettiradi. Buni ham boshqarish uchun PHP'da `set_error_handler` bor: u barcha warning/notice'larni biz beradigan funksiyaga yo'naltiradi, biz esa ularni exception'ga aylantira olamiz:

```php
<?php
// PHP "ogohlantirish" (warning) larini exception'ga aylantiramiz
set_error_handler(function (int $tur, string $xabar, string $fayl, int $qator) {
    throw new ErrorException($xabar, 0, $tur, $fayl, $qator);
});

try {
    // Mavjud bo'lmagan faylni ochish odatda Warning beradi (dasturni to'xtatmaydi)
    $matn = file_get_contents("yoq_bunday_fayl.txt");   // ❌ Warning
    echo $matn;
} catch (ErrorException $e) {
    echo "Ogohlantirish exception'ga aylandi: " . $e->getMessage() . "\n";
}

restore_error_handler();   // odatdagi holatga qaytaramiz
echo "Handler tiklandi, dastur davom etmoqda\n";
```

Natija (taxminan):

```
Ogohlantirish exception'ga aylandi: file_get_contents(yoq_bunday_fayl.txt): Failed to open stream: No such file or directory
Handler tiklandi, dastur davom etmoqda
```

Tushuntiramiz:
- **`set_error_handler(fn)`** — "bundan keyin PHP warning/notice chiqarsa, o'rniga shu funksiyani chaqir". Bizning funksiyamiz `ErrorException` tashlaydi — endi uni odatdagi `try/catch` bilan ushlash mumkin.
- **`restore_error_handler()`** — handler'ni avvalgi holatiga qaytaradi (ish tugagach yaxshi odat).

Buni har joyda ishlatish shart emas — bu ko'proq "ilg'or" texnika. Lekin eski funksiyalar bilan ishlaganda warning'larni ham toza, yagona usulda boshqarishga yordam beradi. Hozircha shuni bilsangiz yetarli: `try/catch` — exception uchun, `set_error_handler` — eski warning'larni exception'ga aylantirish uchun.

### Nega foydali?

1. **Dastur qulamaydi:** xato bo'lsa ham, foydalanuvchiga chiroyli xabar berasiz.
2. **Nazorat:** xatolarni bir joyda, tartibli boshqarasiz.
3. **Ishonch:** "nima noto'g'ri ketishi mumkin"ni oldindan o'ylab, tayyor turasiz.
4. **Aniqlik:** o'z exception turlaringiz va `previous` zanjiri bilan xatoning **aynan nima** ekanini va **asl sababini** aniq bilasiz.

### Mashqlar

**Oson**
1. `try/catch` bilan nolga bo'lishni ushlang va chiroyli xabar chiqaring.
2. `throw new Exception(...)` bilan o'z xatongizni tashlang va ushlang.
3. Xato xabarini `$e->getMessage()` orqali chiqaring.
4. `finally` blokini qo'shing va u har doim ishlashini ko'ring.
5. `try` ichida xato bo'lmasa, `catch` ishlamasligini (faqat `try` ishlashini) ko'ring.
6. `int` tip e'lon qilingan funksiyaga matn bering va chiqqan `TypeError` ni `catch (TypeError $e)` bilan ushlang.
7. Bitta xatoni avval `catch (Exception $e)`, keyin `catch (Throwable $e)` bilan ushlab ko'ring — qaysi biri `TypeError` ni ham ushlaydi?

**O'rta**
8. `yoshTekshir($yosh)` funksiyasi: yosh manfiy yoki 150 dan katta bo'lsa xato tashlasin.
9. `bol($a, $b)` funksiyasi: `$b` nol bo'lsa xato tashlasin, aks holda bo'linmani qaytarsin.
10. `parolTekshir($parol)` funksiyasi: parol 8 belgidan qisqa bo'lsa xato tashlasin.
11. Bir nechta `throw` holatini bitta funksiyada qo'llang (turli noto'g'ri inputlar uchun turli xato xabarlari).
12. O'z exception turingizni yarating: `class BoshXatoException extends Exception {}`. Bo'sh matn berilganda aynan shu turni tashlang va `catch (BoshXatoException $e)` bilan ushlang.
13. `catch (TypeError | ValueError $e)` (multi-catch) yozing va ikkala xato turini ham bitta blok ushlashini ko'ring.
14. `getCode()` va `getLine()` dan foydalaning: `throw new Exception("Xato", 500)` tashlang va kod hamda qatorni chiqaring.

**Qiyin**
15. `Hisob` class'ining `pulYechish` metodini xato bilan ishlang: pul yetarli bo'lmasa `throw new Exception("Mablag' yetarli emas")`. Chaqirilganda `try/catch` bilan ushlang.
16. Foydalanuvchi ro'yxatdan o'tishini tekshiruvchi funksiya yozing: bo'sh ism, noto'g'ri email (`@` yo'q), qisqa parol — har biri uchun alohida xato tashlasin. `try/catch` bilan har bir holatni sinab ko'ring.
17. `finally` ning amaliy foydasini ko'rsating: "ulanish ochildi" → ish (xato bo'lishi mumkin) → `finally` da "ulanish yopildi" har doim chiqsin.
18. Exception zanjiri yozing: past funksiya `BazaException` tashlasin, yuqori funksiya uni ushlab `XizmatException` tashlasin (`previous` orqali asl xatoni saqlab). Tashqarida `getPrevious()` bilan asl sababni chiqaring.
19. Resursni `finally` bilan xavfsiz yoping: `fopen` bilan fayl oching, `try` ichida xato tashlang, `finally` da `fclose` qiling. Fayl xato bo'lganda ham yopilishini ko'ring.

<details markdown="1">
<summary>Yechim — 12 (o'z exception turi)</summary>

```php
<?php
class BoshXatoException extends Exception {}

function ismTekshir(string $ism): string {
    if (trim($ism) === "") {
        throw new BoshXatoException("Ism bo'sh bo'lmasligi kerak");
    }
    return "Salom, " . $ism;
}

try {
    echo ismTekshir("");   // bo'sh — maxsus xato tashlaydi
} catch (BoshXatoException $e) {
    echo "Maxsus xato: " . $e->getMessage() . "\n";   // Maxsus xato: Ism bo'sh bo'lmasligi kerak
} catch (Exception $e) {
    echo "Boshqa xato: " . $e->getMessage() . "\n";
}
```
`class BoshXatoException extends Exception {}` — ichi bo'sh bo'lsa ham to'liq ishlaydigan xato turi. Endi uni boshqa xatolardan ajratib, `catch (BoshXatoException $e)` bilan **aynan** ushlay olamiz. `catch` larni tartib bilan yozdik: aniqrog'i (maxsus tur) yuqorida, umumiyrog'i (`Exception`) pastda.
</details>

<details markdown="1">
<summary>Yechim — 15 (xavfsiz pul yechish, xato bilan)</summary>

```php
<?php
class Hisob {
    public function __construct(private int $balans) {}

    public function pulYechish(int $summa): int {
        if ($summa > $this->balans) {
            throw new Exception("Mablag' yetarli emas. Balans: " . $this->balans);
        }
        $this->balans -= $summa;
        return $this->balans;
    }
}

$hisob = new Hisob(100000);

try {
    $hisob->pulYechish(150000);   // xato tashlaydi
} catch (Exception $e) {
    echo "Amal bajarilmadi: " . $e->getMessage();
    // Amal bajarilmadi: Mablag' yetarli emas. Balans: 100000
}
```
2.3'da `pulYechish` `false` qaytarardi. Bu yerda esa `throw` bilan **aniq xato** beramiz — chaqiruvchi nima uchun amal bajarilmaganini aniq biladi. Ikkala usul ham to'g'ri; `throw` murakkabroq holatlarda foydaliroq, chunki xato sababini aniq yetkazadi. E'tibor bering: `private int $balans` ni **konstruktor promotion** (`public function __construct(private int $balans)`) bilan yozdik — bu 8.x uslubi, qisqa va tiplangan.
</details>

<details markdown="1">
<summary>Yechim — 16 (ro'yxatdan o'tishni tekshirish)</summary>

```php
<?php
function royxatdanOtkaz(string $ism, string $email, string $parol): string {
    if (empty($ism)) {
        throw new Exception("Ism bo'sh bo'lmasligi kerak");
    }
    if (!str_contains($email, "@")) {
        throw new Exception("Email noto'g'ri (@ yo'q)");
    }
    if (strlen($parol) < 8) {
        throw new Exception("Parol kamida 8 belgidan iborat bo'lsin");
    }
    return "Ro'yxatdan o'tdingiz: " . $ism;
}

// Har xil holatlarni sinab ko'ramiz:
$testlar = [
    ["",      "a@b.uz", "12345678"],   // ism bo'sh
    ["Ali",   "xato",   "12345678"],   // email noto'g'ri
    ["Vali",  "v@b.uz", "123"],        // parol qisqa
    ["Guli",  "g@b.uz", "maxfiy123"],  // hammasi to'g'ri
];

foreach ($testlar as $t) {
    try {
        echo royxatdanOtkaz($t[0], $t[1], $t[2]) . "<br>";
    } catch (Exception $e) {
        echo "Xato: " . $e->getMessage() . "<br>";
    }
}
// Xato: Ism bo'sh bo'lmasligi kerak
// Xato: Email noto'g'ri (@ yo'q)
// Xato: Parol kamida 8 belgidan iborat bo'lsin
// Ro'yxatdan o'tdingiz: Guli
```
Funksiya har bir noto'g'ri holat uchun alohida, aniq xato tashlaydi. `try/catch` har birini ushlab, tegishli xabarni ko'rsatadi. Bu — formani tekshirishning toza usuli: funksiya "qoidani" biladi, chaqiruvchi "javobni" boshqaradi. (Argumentlarga `string` tiplari qo'shildi — 8.x uslubi, xato erta ushlanadi.)
</details>

<details markdown="1">
<summary>Yechim — 17 (finally bilan ulanishni yopish)</summary>

```php
<?php
function malumotOqi(bool $xatoBoladimi): void {
    echo "Ulanish ochildi<br>";
    try {
        if ($xatoBoladimi) {
            throw new Exception("O'qishda xato yuz berdi");
        }
        echo "Ma'lumot o'qildi<br>";
    } catch (Exception $e) {
        echo "Xato: " . $e->getMessage() . "<br>";
    } finally {
        echo "Ulanish yopildi<br>";   // HAR DOIM bajariladi
    }
}

malumotOqi(false);
echo "---<br>";
malumotOqi(true);
// Ulanish ochildi / Ma'lumot o'qildi / Ulanish yopildi
// ---
// Ulanish ochildi / Xato: O'qishda xato yuz berdi / Ulanish yopildi
```
`finally` ning amaliy foydasi shu: xato bo'ladimi yoki yo'qmi, "ulanishni yopish" kabi tozalash ishi **har doim** bajariladi. Real kodda bu — fayl, baza ulanishi yoki boshqa resursni xato bo'lganda ham to'g'ri yopish uchun ishlatiladi. (`$xatoBoladimi` ga `bool` tipi qo'shildi.)
</details>

<details markdown="1">
<summary>Yechim — 18 (exception zanjiri, previous bilan)</summary>

```php
<?php
class BazaException extends Exception {}
class XizmatException extends Exception {}

function bazadanOl(): never {
    throw new BazaException("Ulanish uzildi (port 3306)");
}

function foydalanuvchiOl(): void {
    try {
        bazadanOl();
    } catch (BazaException $past) {
        // Asl xatoni previous orqali saqlab, yangi xato tashlaymiz
        throw new XizmatException("Foydalanuvchini olib bo'lmadi", previous: $past);
    }
}

try {
    foydalanuvchiOl();
} catch (XizmatException $e) {
    echo "Yuqori xato: " . $e->getMessage() . "\n";
    $sabab = $e->getPrevious();
    if ($sabab !== null) {
        echo "Asl sabab: " . $sabab->getMessage() . "\n";
    }
}
// Yuqori xato: Foydalanuvchini olib bo'lmadi
// Asl sabab: Ulanish uzildi (port 3306)
```
Past daraja (`bazadanOl`) texnik xato beradi. Yuqori daraja (`foydalanuvchiOl`) uni ushlab, foydalanuvchiga tushunarli `XizmatException` tashlaydi — lekin `previous: $past` orqali **asl sababni** yo'qotmaydi. Tashqarida `getPrevious()` bilan ikkalasini ham olamiz: foydalanuvchiga chiroyli xabar, log'ga esa texnik sabab.
</details>

<details markdown="1">
<summary>Yechim — 19 (finally bilan resursni yopish)</summary>

```php
<?php
function faylgaYoz(string $yol, bool $xatoBoladimi): void {
    $fayl = fopen($yol, "w");   // resurs ochildi
    echo "Fayl ochildi<br>";
    try {
        if ($xatoBoladimi) {
            throw new RuntimeException("Yozishda muammo");
        }
        fwrite($fayl, "Salom");
        echo "Matn yozildi<br>";
    } finally {
        fclose($fayl);          // HAR DOIM yopiladi
        echo "Fayl yopildi<br>";
    }
}

$yol = sys_get_temp_dir() . "/mashq19.txt";
try {
    faylgaYoz($yol, true);   // xato bo'ladi
} catch (RuntimeException $e) {
    echo "Tashqarida ushlandi: " . $e->getMessage() . "<br>";
}
unlink($yol);
// Fayl ochildi / Fayl yopildi / Tashqarida ushlandi: Yozishda muammo
```
Bu yerda `catch` ham yo'q (faqat `try/finally`): xato `finally` da fayl yopilgandan **keyin** "yuqoriga" uchadi va uni tashqaridagi `try/catch` ushlaydi. Natija: fayl xato bo'lganda ham yopildi (resurs "oqib ketmadi"), xato esa yo'qolmadi. Bu — ishonchli kodning asosiy odati.
</details>

---

> **2-QISM yakunlandi!** Bu — qo'llanmaning eng murakkab qismlaridan biri edi. Endi siz: class va obyekt, konstruktor, inkapsulyatsiya (public/private), meros, abstrakt class, interfeys, static, trait, enum va xatolarni boshqarishni (try/catch/finally, exception iyerarxiyasi, o'z exception turlaringiz, multi-catch va zanjir) bilasiz. Bu — katta, tartibli dasturlar yozishning asosi.
>
> Agar hammasi hali to'liq "o'tirmagan" bo'lsa — tabiiy. OOP'ni tushunish vaqt va mashq talab qiladi. Misollarni qayta yozib, o'zgartirib ko'ring. Keyingi qism — **ma'lumotlar bazasi:** ma'lumotni doimiy (dastur yopilgandan keyin ham) saqlash. Bu — haqiqiy, foydali dasturlar yozishning keyingi katta qadami.
