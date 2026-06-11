# 3.6 PHP'dan bazaga ulanish (PDO)

[⬅️ Oldingi: 3.5 Jadvallarni bog'lash (JOIN)](./28-jadvallarni-boglash.md) · [🏠 README](./README.md) · [Keyingi: 3.7 PostgreSQL va MySQL'dan farqlari ➡️](./30-postgresql-va-mysqldan-farqlari.md)

---

Hozirgacha SQL'ni phpMyAdmin'da qo'lda yozdik. Lekin haqiqiy dasturda **PHP kodi** bazaga ulanib, SQL buyruqlarini yuborishi kerak. Mana shu — PHP va ma'lumotlar bazasini birlashtiradigan eng muhim qadam. Buning uchun **PDO** degan vositadan foydalanamiz.

**PDO (PHP Data Objects)** — PHP'ni ma'lumotlar bazasiga ulaydigan standart, xavfsiz vosita.

### Bazaga ulanish

```php
<?php
$pdo = new PDO(
    "mysql:host=localhost;dbname=maktab;charset=utf8mb4",
    "root",   // foydalanuvchi nomi (XAMPP'da odatda "root")
    ""        // parol (XAMPP'da odatda bo'sh)
);
```

Tushuntiramiz:
- **`new PDO(...)`** — bazaga ulanish obyektini yaratamiz (PDO — class, biz undan obyekt yaratamiz).
- **`"mysql:host=localhost;dbname=maktab;..."`** — ulanish ma'lumotlari: `mysql` turi, `localhost` (shu kompyuter), `dbname=maktab` (qaysi baza). Bu satr **DSN** (Data Source Name — "ma'lumot manbasi nomi") deb ataladi.
- **`"root"`** va **`""`** — foydalanuvchi va parol. XAMPP'da standart sozlama: foydalanuvchi `root`, parol bo'sh.

> Agar ulanish xato bersa, MySQL XAMPP'da ishlab turganini tekshiring va baza nomi to'g'riligiga ishonch hosil qiling.

### Xato rejimini yoqing — `ERRMODE_EXCEPTION` (eng muhim!)

Yuqoridagi ulanish ishlaydi, lekin **bitta jiddiy kamchiligi** bor: agar so'rovda xato bo'lsa (ustun nomi noto'g'ri, jadval yo'q, baza o'chgan) — PDO standart holatda **jim turadi**. Hech narsa demaydi, faqat `false` qaytaradi. Natijada dasturingiz "sababsiz" ishlamay qoladi, siz esa nima xato bo'lganini bilmaysiz. Bu — boshlovchilarni eng ko'p aldaydigan tuzoq.

Yechim: PDO'ga **"xato bo'lsa, baqir!"** deb buyuramiz. Buni `setAttribute` bilan qilamiz:

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=maktab;charset=utf8mb4", "root", "");

// Xato bo'lsa — PDO "exception" (istisno) tashlaydi, jim turmaydi
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
```

Endi xato bo'lsa, PDO **`PDOException`** degan istisno tashlaydi (istisnolarni 2.10 — "Xatolarni boshqarish" bobida o'rgangansiz). Uni **`try/catch`** bilan ushlaymiz:

```php
<?php
try {
    $pdo = new PDO("mysql:host=localhost;dbname=maktab;charset=utf8mb4", "root", "");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Ataylab noto'g'ri jadval nomi — xato chiqishini ko'rish uchun
    $pdo->query("SELECT * FROM mavjud_emas_jadval");  // ❌ bunday jadval yo'q

} catch (PDOException $e) {
    echo "Baza bilan muammo: " . $e->getMessage();
}
```

Nima sodir bo'ldi:
- **`try { ... }`** ichida — bazaga oid kod. Agar xato bo'lsa, PHP darhol `catch`ga "sakraydi".
- **`catch (PDOException $e)`** — bazadan kelgan xatoni ushlaydi. `$e->getMessage()` — xatoning aniq matni (masalan, "Table 'maktab.mavjud_emas_jadval' doesn't exist").
- Endi siz **aniq nima xato bo'lganini** ko'rasiz. Bu — debug (xato topish)ni yuz barobar osonlashtiradi.

> **Oltin qoida:** har bir PDO ulanishida darhol `setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION)` yozing. Busiz xatolar yashirin qoladi va sizni ovora qiladi. Bu — professional PHP kodining birinchi belgisi.

> **Diqqat:** `$e->getMessage()` ichida ba'zan baza tuzilishi haqida ma'lumot bo'ladi. Tayyor (production) saytda bu matnni foydalanuvchiga to'g'ridan-to'g'ri ko'rsatmang — uni log faylga yozing, foydalanuvchiga esa oddiy "Xatolik yuz berdi" xabarini chiqaring (Xavfsizlik bobida batafsil).

### Ulanishni BITTA joyda saqlash — `db.php`

Diqqat qilgan bo'lsangiz, har bir misolda ulanish satrini (`new PDO(...)` + `setAttribute`) qayta-qayta yozyapmiz. Bu — yomon odat: parol o'zgarsa, **hamma fayllarni** tahrirlash kerak bo'ladi. To'g'ri yo'l — ulanishni **bitta joyda**, alohida faylda yozish va kerak bo'lganda chaqirish.

`db.php` degan fayl yarating:

```php
<?php
// db.php — bazaga ulanishni bir joyda saqlaydigan fayl

function ulan(): PDO
{
    static $pdo = null;   // bir marta ulanadi, keyin eslab qoladi

    if ($pdo === null) {
        $pdo = new PDO(
            "mysql:host=localhost;dbname=maktab;charset=utf8mb4",
            "root",
            ""
        );
        // Har doim shu uchta sozlama:
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    }

    return $pdo;
}
```

Endi istalgan faylda shunchaki chaqiramiz:

```php
<?php
require 'db.php';        // ulanish funksiyasini ulaymiz

$pdo = ulan();           // ulanishni olamiz

$natija = $pdo->query("SELECT * FROM talabalar");
foreach ($natija as $qator) {
    echo $qator['ism'] . "<br>";
}
```

Tushuntiramiz:
- **`function ulan(): PDO`** — funksiya PDO obyekti qaytaradi (`: PDO` — qaytish turi, 1.9'da o'rgangansiz).
- **`static $pdo = null`** — `static` o'zgaruvchi funksiya chaqiruvlari orasida **qiymatini eslab qoladi**. Shuning uchun `ulan()` ni 10 marta chaqirsangiz ham, baza **bir marta** ulanadi (har safar yangi ulanish ochish — sekin va isrofgarchilik).
- **Uchta sozlama** har doim birga yuradi:
  - `ATTR_ERRMODE` — xatoni istisno qilib tashlaydi (yuqorida ko'rdik).
  - `ATTR_DEFAULT_FETCH_MODE` — natijani standart holatda kalitli massiv qiladi (pastda batafsil).
  - `ATTR_EMULATE_PREPARES => false` — prepared statement'ni **haqiqiy** (baza darajasida) ishlatadi, soxta emas. Bu xavfsizroq.

Bu naqsh — boshqa har bir misolda ham ishlatiladi. Endilikda "`require 'db.php'; $pdo = ulan();`" degan kod — bazaga ulanishning standart usuli.

### Ma'lumot o'qish — `query`

Oddiy o'qish so'rovini `query` bilan yuboramiz va natijani `foreach` bilan aylanib chiqamiz:

```php
<?php
require 'db.php';
$pdo = ulan();

$natija = $pdo->query("SELECT * FROM talabalar");

foreach ($natija as $qator) {
    echo $qator['ism'] . " - " . $qator['yosh'] . " yosh<br>";
}
```

Nima sodir bo'ldi:
- `$pdo->query("SELECT ...")` — bazaga so'rov yuboradi va natijani qaytaradi.
- Natija — qatorlar to'plami. Har bir qator — **kalitli massiv** (1.8'da o'rgangan!), kalitlari ustun nomlari (`ism`, `yosh`).
- `foreach` bilan har bir qatorni olamiz, `$qator['ism']` orqali ustun qiymatini o'qiymiz.

Ko'ryapsizmi — bu yerda hamma narsa birlashdi: PHP (`foreach`, massiv) + SQL (`SELECT`) + baza. Bazadagi ma'lumot endi PHP kodingizga keldi.

> **Eslatma:** `query()` faqat **foydalanuvchi ma'lumoti yo'q** sof so'rovlar uchun (masalan "barcha talabalarni ber"). Agar so'rovga tashqaridan kelgan qiymat qo'shadigan bo'lsangiz — pastda ko'radiganimizdek `prepare`/`execute` ishlating.

### Bir qatorni o'qish usullari — `fetch`, `fetchAll`, `fetchColumn`

`foreach` — qatorlarni aylanishning bir yo'li. Lekin PDO bizga natijani olishning bir nechta qulay usulini beradi. Eng muhim uchtasi:

**1) `fetch()` — bitta qator oladi.** Keyingi chaqiruvda — keyingi qator. Qator qolmasa `false` qaytaradi. `while` bilan juda qulay:

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->query("SELECT ism, yosh FROM talabalar");

while ($qator = $stmt->fetch()) {
    echo $qator['ism'] . " - " . $qator['yosh'] . "<br>";
}
```

**2) `fetchAll()` — barcha qatorlarni bitta massivga oladi.** Natija — massivlar massivi. Bu sonni `count()` bilan bilish yoki butun ro'yxatni saqlash uchun qulay:

```php
<?php
require 'db.php';
$pdo = ulan();

$talabalar = $pdo->query("SELECT * FROM talabalar")->fetchAll();

echo "Jami: " . count($talabalar) . " ta talaba<br>";

foreach ($talabalar as $t) {
    echo $t['ism'] . "<br>";
}
```

**3) `fetchColumn()` — bitta qiymat (bitta ustun) oladi.** `COUNT(*)`, `MAX(...)`, yoki bitta ustun kerak bo'lganda eng qulay:

```php
<?php
require 'db.php';
$pdo = ulan();

// Talabalar soni — bitta son
$soni = $pdo->query("SELECT COUNT(*) FROM talabalar")->fetchColumn();
echo "Talabalar soni: $soni<br>";

// Eng katta yosh
$kattaYosh = $pdo->query("SELECT MAX(yosh) FROM talabalar")->fetchColumn();
echo "Eng katta yosh: $kattaYosh";
```

> **Qachon qaysi biri?** Bitta qiymat kerak (son, summa) → `fetchColumn()`. Bitta qator kerak (bitta talaba) → `fetch()`. Hamma qatorlar kerak (ro'yxat) → `fetchAll()` yoki `foreach`. Katta jadvalda `fetchAll` butun jadvalni xotiraga yuklaydi — juda katta ma'lumotda `while ($stmt->fetch())` tejamliroq.

### Natija ko'rinishi — FETCH rejimlari (`ASSOC`, `OBJ`, `CLASS`)

PDO natijani **uch xil ko'rinishda** bera oladi. Buni "fetch rejimi" deb ataymiz. `db.php`'da standart qilib `FETCH_ASSOC` ni qo'ydik, lekin har bir chaqiruvda boshqasini tanlash mumkin.

**1) `PDO::FETCH_ASSOC` — kalitli massiv** (eng ko'p ishlatiladi). Ustunga `$qator['ism']` bilan murojaat qilamiz:

```php
<?php
require 'db.php';
$pdo = ulan();

$qator = $pdo->query("SELECT * FROM talabalar LIMIT 1")
             ->fetch(PDO::FETCH_ASSOC);

echo $qator['ism'];     // massiv: kvadrat qavs bilan
```

**2) `PDO::FETCH_OBJ` — obyekt.** Ustunlarga `$qator->ism` (strelka) bilan murojaat qilamiz — ba'zilarga bu chiroyliroq tuyuladi:

```php
<?php
require 'db.php';
$pdo = ulan();

$qator = $pdo->query("SELECT * FROM talabalar LIMIT 1")
             ->fetch(PDO::FETCH_OBJ);

echo $qator->ism;       // obyekt: strelka bilan
echo " - ";
echo $qator->yosh;
```

**3) `PDO::FETCH_CLASS` — o'zingiz yozgan class obyektiga.** Bu — eng kuchlisi. Bazadagi qatorni **to'g'ridan-to'g'ri** o'z class obyektingizga aylantiradi. Ustun nomlari class xususiyatlariga mos kelishi kerak:

```php
<?php
require 'db.php';
$pdo = ulan();

// Avval class yozamiz (zamonaviy, tiplangan uslubda)
class Talaba
{
    public int $id = 0;
    public string $ism = '';
    public int $yosh = 0;
    public string $shahar = '';

    public function tanishtir(): string
    {
        return "{$this->ism}, {$this->yosh} yosh, {$this->shahar}dan";
    }
}

// Bazadagi qatorni Talaba obyektiga aylantiramiz
$stmt = $pdo->query("SELECT * FROM talabalar LIMIT 1");
$talaba = $stmt->fetchObject(Talaba::class);

echo $talaba->ism;             // Ali
echo "<br>";
echo $talaba->tanishtir();     // Ali, 18 yosh, Toshkentdan
```

Tushuntiramiz:
- `fetchObject(Talaba::class)` — qatorni `Talaba` class obyekti qilib qaytaradi.
- Endi `$talaba` — oddiy massiv emas, **to'liq obyekt**: undan `tanishtir()` kabi metodlarni chaqira olasiz. Bu — bazani obyektga bog'laydigan kuchli usul (kelajakda "ORM" deb ataladigan kutubxonalar shu asosda ishlaydi).

Hammasini bittada — barcha talabalarni `Talaba` obyektlari sifatida olish:

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->query("SELECT * FROM talabalar");
$talabalar = $stmt->fetchAll(PDO::FETCH_CLASS, Talaba::class);

foreach ($talabalar as $t) {        // har bir $t — Talaba obyekti
    echo $t->tanishtir() . "<br>";
}
```

> **Qaysi birini tanlash?** Oddiy sahifalar uchun `FETCH_ASSOC` (massiv) yetarli va eng ko'p ishlatiladi. Class va metodlar bilan ishlasangiz — `FETCH_CLASS` toza, obyektga yo'naltirilgan kod beradi.

### Foydalanuvchi ma'lumoti bilan ishlash — XAVFSIZLIK

Endi eng muhim mavzu. Ko'pincha so'rovga **foydalanuvchidan kelgan** ma'lumot qo'shamiz. Masalan, "id'si shu bo'lgan talabani top". Buni **noto'g'ri** qilish — jiddiy xavfsizlik teshigiga olib keladi.

**❌ XAVFLI usul — hech qachon bunday qilmang:**

```php
<?php
$id = $_GET['id'];   // foydalanuvchidan kelgan ma'lumot
// ❌ XAVFLI: foydalanuvchi ma'lumotini to'g'ridan-to'g'ri so'rovga qo'shish
$natija = $pdo->query("SELECT * FROM talabalar WHERE id = $id");
```

Nega xavfli? Chunki foydalanuvchi `$id` o'rniga zararli SQL kodini kiritishi mumkin. Bu — **SQL injection** degan hujum. Yomon niyatli odam shu orqali butun bazangizni o'qishi yoki o'chirishi mumkin. Bu — eng keng tarqalgan va xavfli xatolardan biri.

**✅ TO'G'RI usul — "prepared statement" (tayyorlangan so'rov):**

```php
<?php
$id = $_GET['id'];

// 1) So'rovni "tayyorlaymiz" — qiymat o'rniga ? belgisi qo'yamiz
$stmt = $pdo->prepare("SELECT * FROM talabalar WHERE id = ?");

// 2) Qiymatni alohida, xavfsiz tarzda beramiz
$stmt->execute([$id]);

// 3) Natijani olamiz
$talaba = $stmt->fetch();

echo $talaba['ism'];
```

Tushuntiramiz:
- **`prepare("... WHERE id = ?")`** — so'rovni tayyorlaymiz, qiymat o'rniga **`?`** (savol belgisi) qo'yamiz.
- **`execute([$id])`** — qiymatni alohida beramiz. PHP uni xavfsiz tarzda joylaydi — endi zararli kod ishlamaydi.
- **`fetch()`** — bitta qatorni oladi (`fetchAll()` — barcha qatorlarni).

**Asosiy qoida:** foydalanuvchidan kelgan har qanday ma'lumot so'rovga `?` orqali, `prepare`/`execute` bilan qo'shilishi shart. Hech qachon to'g'ridan-to'g'ri so'rov ichiga yozmang. Bu — sizning bazangizni himoyalaydi.

Quyidagi diagramma butun oqimni ko'rsatadi: PHP qiymatni PDO'ga beradi, PDO uni prepared statement bilan bazaga xavfsiz yuboradi va natijani PHP'ga qaytaradi:

![PDO ulanish oqimi: PHP, PDO, baza va prepared statement](rasmlar/phc-pdo-ulanish-oqimi.svg)

### Nomli parametrlar — `:ism` va `bindValue`

`?` belgisi yaxshi, lekin so'rovda **ko'p qiymat** bo'lsa, qaysi `?` qaysi qiymatga tegishli ekanini chalkashtirish oson (tartibni aniq saqlash kerak). Bunday holatda **nomli parametrlar** ancha o'qilishli: `?` o'rniga `:ism`, `:yosh` kabi nom qo'yamiz.

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->prepare(
    "SELECT * FROM talabalar WHERE shahar = :shahar AND yosh > :yosh"
);

// Qiymatlarni nom bo'yicha beramiz — tartibi muhim emas
$stmt->execute([
    ':shahar' => 'Toshkent',
    ':yosh'   => 18,
]);

foreach ($stmt->fetchAll() as $t) {
    echo $t['ism'] . "<br>";
}
```

Tushuntiramiz:
- So'rovda `?` o'rniga **`:shahar`**, **`:yosh`** (ikki nuqta bilan boshlanadigan nom) qo'ydik.
- `execute([...])` ga **kalitli massiv** beramiz: kalit — parametr nomi, qiymat — uning qiymati. Tartib emas, **nom** muhim.

**`bindValue` — qiymatni alohida bog'lash.** `execute([...])` ichida hammasini bittada berish o'rniga, har bir qiymatni alohida bog'lash ham mumkin. Bu, ayniqsa, **qiymat turini** aniq aytmoqchi bo'lganda foydali:

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->prepare("SELECT * FROM talabalar WHERE id = :id");

// Qiymatni nomga bog'laymiz, turini ham aytamiz (butun son)
$stmt->bindValue(':id', $_GET['id'], PDO::PARAM_INT);

$stmt->execute();
$talaba = $stmt->fetch();
print_r($talaba);
```

Tushuntiramiz:
- **`bindValue(':id', $qiymat, PDO::PARAM_INT)`** — `:id` parametriga qiymatni bog'laydi va "bu — butun son" deb belgilaydi.
- `PDO::PARAM_INT` — butun son, `PDO::PARAM_STR` — matn, `PDO::PARAM_BOOL` — mantiqiy. Ko'pincha bularsiz ham ishlaydi, lekin turni aniq berish toza va xavfsiz.
- `bindValue` dan keyin `execute()` ni **qiymatsiz** chaqiramiz (qiymatlar allaqachon bog'langan).

> **Xulosa:** kam qiymat → `?` qulay. Ko'p qiymat → `:nom` o'qilishliroq. Tur muhim → `bindValue(..., PDO::PARAM_INT)`. Hammasi bir xil darajada xavfsiz — muhimi, qiymatni hech qachon so'rov matniga to'g'ridan-to'g'ri yozmaslik.

### Ma'lumot qo'shish (xavfsiz)

```php
<?php
require 'db.php';
$pdo = ulan();

$ism = "Yangi Talaba";
$yosh = 18;
$shahar = "Toshkent";

$stmt = $pdo->prepare("INSERT INTO talabalar (ism, yosh, shahar) VALUES (?, ?, ?)");
$stmt->execute([$ism, $yosh, $shahar]);

echo "Talaba qo'shildi!";
```

Bir nechta qiymat bo'lsa, har biriga bitta `?` qo'yamiz va `execute`ga massiv sifatida (tartibda) beramiz.

### Yangi qator id'sini olish — `lastInsertId()`

`INSERT` qilganingizda baza yangi qatorga avtomatik `id` beradi (`AUTO_INCREMENT`). Ko'pincha shu yangi `id` darhol kerak bo'ladi — masalan, "talaba qo'shildi, endi uning sahifasiga yo'naltir". `lastInsertId()` aynan shuni beradi:

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->prepare("INSERT INTO talabalar (ism, yosh, shahar) VALUES (?, ?, ?)");
$stmt->execute(["Bekzod", 19, "Andijon"]);

$yangiId = $pdo->lastInsertId();    // yangi qo'shilgan qatorning id'si
echo "Yangi talaba qo'shildi, id = $yangiId";
```

`lastInsertId()` — **oxirgi** `INSERT`'da berilgan id'ni qaytaradi. Shuning uchun uni `execute()` dan **darhol keyin** chaqiring.

### Nechta qator o'zgardi — `rowCount()`

`UPDATE` yoki `DELETE` qilganingizda, "nechta qatorga ta'sir qildi?" degan savol tug'iladi. `rowCount()` shu sonni beradi:

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->prepare("UPDATE talabalar SET shahar = ? WHERE shahar = ?");
$stmt->execute(["Toshkent shahri", "Toshkent"]);

echo $stmt->rowCount() . " ta qator yangilandi";
```

`DELETE` da ham xuddi shunday:

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->prepare("DELETE FROM talabalar WHERE yosh < ?");
$stmt->execute([10]);

if ($stmt->rowCount() === 0) {
    echo "Hech qaysi qator o'chmadi.";
} else {
    echo $stmt->rowCount() . " ta talaba o'chirildi.";
}
```

> **Diqqat:** `rowCount()` `UPDATE`/`DELETE`/`INSERT` uchun ishonchli. `SELECT` da qatorlar sonini bilish uchun `fetchAll()` qilib `count()` ishlatgan yaxshi (ba'zi bazalarda `SELECT`'da `rowCount` to'g'ri ishlamaydi).

### Transaksiyalar — "yo hammasi, yo hech narsa"

Ba'zan **bir nechta so'rov** birga bajarilishi shart — biri bo'lib, ikkinchisi bo'lmasa, ma'lumot buziladi. Eng klassik misol — **pul o'tkazish**: bir hisobdan pul yechish va boshqasiga qo'shish. Tasavvur qiling:

1. Ali hisobidan 300 so'm yechildi. ✅
2. ...keyin to'satdan tok o'chdi / xato chiqdi. ❌
3. Vali hisobiga 300 so'm qo'shilmadi.

Natija: 300 so'm **havoga uchdi**! Ali pulni yo'qotdi, Vali olmadi. Bu — falokat.

**Transaksiya** shu muammoni hal qiladi: bir nechta so'rovni **bitta bo'lak** qilib bog'laydi. Qoida — **"yo hammasi bajariladi, yo hech narsa"**. Birortasi xato bo'lsa — hammasi bekor qilinadi (orqaga qaytariladi), baza o'zgarmaydi.

Buning uchun uchta buyruq bor:
- **`beginTransaction()`** — "transaksiyani boshla" (bu yerdan keyingi o'zgarishlar vaqtincha, tasdiqlanmagan).
- **`commit()`** — "hammasi joyida, o'zgarishlarni tasdiqla" (endi baza haqiqatan o'zgaradi).
- **`rollBack()`** — "xato bo'ldi, hammasini bekor qil" (baza boshlang'ich holatiga qaytadi).

```php
<?php
require 'db.php';
$pdo = ulan();

$jonatuvchiId   = 1;     // Ali
$qabulQiluvchiId = 2;    // Vali
$summa = 300;

try {
    $pdo->beginTransaction();   // transaksiya boshlandi

    // 1) Jo'natuvchidan pul yechamiz
    $yech = $pdo->prepare("UPDATE hisoblar SET balans = balans - :s WHERE id = :id");
    $yech->execute([':s' => $summa, ':id' => $jonatuvchiId]);

    // 2) Qabul qiluvchiga pul qo'shamiz
    $qosh = $pdo->prepare("UPDATE hisoblar SET balans = balans + :s WHERE id = :id");
    $qosh->execute([':s' => $summa, ':id' => $qabulQiluvchiId]);

    $pdo->commit();             // hammasi joyida — tasdiqlaymiz
    echo "Pul muvaffaqiyatli o'tkazildi!";

} catch (PDOException $e) {
    $pdo->rollBack();           // xato — hammasini bekor qilamiz
    echo "Xatolik: o'tkazma bekor qilindi. Pul joyida qoldi.";
}
```

Tushuntiramiz:
- Ikkala `UPDATE` **birga** bajarilishi shart. `beginTransaction()` ulanrni "bitta bo'lak"ka bog'laydi.
- Agar ikkinchi `UPDATE` (yoki oradagi biror narsa) xato bersa — `catch`ga sakraymiz, `rollBack()` **birinchi** `UPDATE`ni ham bekor qiladi. Ali pulini yo'qotmaydi.
- Faqat **ikkalasi ham** muvaffaqiyatli bo'lsa — `commit()` o'zgarishlarni tasdiqlaydi.

> **Hayotiy qoida:** bir-biriga bog'liq, "hammasi yoki hech narsa" bo'lishi kerak bo'lgan o'zgarishlar (pul, buyurtma + ombor, ko'p jadvalni birga yangilash) doim transaksiya ichida bo'lsin. `ATTR_ERRMODE => EXCEPTION` bu yerda **shart**, chunki xato bo'lganini bilmasak, `rollBack` ham qila olmaymiz.

### Mashqlar

> Bu mashqlar uchun `maktab` bazasi va `talabalar` jadvali tayyor bo'lsin. Fayllarni `htdocs/darslar` ichida yarating, `http://localhost/...` orqali oching. Yangi mashqlar uchun `db.php` faylini yaratib, `require 'db.php'; $pdo = ulan();` naqshidan foydalaning.

**Oson**
1. PDO bilan `maktab` bazasiga ulaning (xato bo'lmasligini tekshiring).
2. `query` bilan barcha talabalarni o'qing va `foreach` bilan ismlarini chiqaring.
3. Har bir talabaning ism va yoshini birga chiqaring.
4. `prepare`/`execute` bilan id'si 1 bo'lgan talabani toping va chiqaring.
5. `prepare`/`execute` bilan yangi talaba qo'shing.
6. Ulanishga `setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION)` qo'shing, keyin ataylab noto'g'ri jadval nomi bilan so'rov yuborib, `try/catch` orqali xato matnini chiqaring.
7. `fetchColumn()` bilan talabalar **sonini** (`SELECT COUNT(*)`) chiqaring.

**O'rta**
8. Faqat Toshkentdagi talabalarni o'qing (`WHERE shahar = ?` bilan, prepared).
9. `fetchAll()` bilan barcha talabalarni massivga oling va sonini (`count`) chiqaring.
10. `mahsulotlar` jadvalidagi barcha mahsulotlarni narxi bilan chiqaring.
11. Foydalanuvchidan kelgan `$_GET['id']` bo'yicha talabani xavfsiz (prepared) qidiring.
12. Bir talabaning yoshini `UPDATE` + prepared statement bilan o'zgartiring, keyin `rowCount()` bilan nechta qator yangilanganini chiqaring.
13. `db.php` faylini yarating: `ulan()` funksiyasi PDO obyekti qaytarsin (uch sozlama bilan). Boshqa faylda `require 'db.php'` qilib ishlating.
14. Yangi talaba qo'shing va `lastInsertId()` bilan unga berilgan yangi `id`'ni chiqaring.
15. `:shahar` va `:yosh` **nomli parametrlari** bilan "Toshkentdagi, yoshi 18 dan katta" talabalarni qidiring.

**Qiyin**
16. To'liq "talabalar ro'yxati" sahifasini yarating: bazadan barcha talabalarni o'qib, ularni HTML jadval (`<table>`) ko'rinishida chiqaring. (`<table>`, `<tr>`, `<td>` teglaridan foydalaning — internetdan ko'ring.)
17. SQL injection xavfini amalda tushuntiring: nima uchun `"WHERE id = $id"` xavfli va `"WHERE id = ?"` xavfsiz ekanini o'z so'zingiz bilan yozing.
18. JOIN'ni PHP'dan ishlating: `kitoblar` va `mualliflar` ni JOIN qilib, har bir kitob nomi va muallifini PHP bilan o'qib chiqaring.
19. `hisoblar` jadvalini yarating (`id`, `egasi`, `balans`) va **transaksiya** bilan bir hisobdan ikkinchisiga pul o'tkazing. Atayin xato qo'shib (masalan, ikkinchi `UPDATE`'da mavjud bo'lmagan ustun nomi), `rollBack` ishlaganini — pul joyida qolganini ko'rsating.
20. `Talaba` classi yozing (tiplangan xususiyatlar + `tanishtir()` metodi) va `FETCH_CLASS`/`fetchAll(PDO::FETCH_CLASS, ...)` bilan barcha talabalarni **obyektlar** sifatida olib, har biri uchun `tanishtir()` ni chaqiring.

<details markdown="1">
<summary>Yechim — 6 (xato rejimi va try/catch)</summary>

```php
<?php
try {
    $pdo = new PDO("mysql:host=localhost;dbname=maktab;charset=utf8mb4", "root", "");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Ataylab noto'g'ri jadval — xato chiqishini ko'ramiz
    $pdo->query("SELECT * FROM yoq_bunday_jadval");   // ❌

} catch (PDOException $e) {
    echo "Baza xatosi: " . $e->getMessage();
    // Masalan: Table 'maktab.yoq_bunday_jadval' doesn't exist
}
```

`ERRMODE_EXCEPTION` yoqilmaganda bu so'rov **jim** `false` qaytarardi va siz nima xato bo'lganini bilmasdingiz. Endi PDO aniq xabar beradi va siz uni `try/catch` bilan boshqarasiz. Bu — har bir loyihada birinchi qo'shadigan sozlama.
</details>

<details markdown="1">
<summary>Yechim — 13 (db.php — bir joyda ulanish)</summary>

`db.php`:

```php
<?php
function ulan(): PDO
{
    static $pdo = null;

    if ($pdo === null) {
        $pdo = new PDO(
            "mysql:host=localhost;dbname=maktab;charset=utf8mb4",
            "root",
            ""
        );
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    }

    return $pdo;
}
```

Ishlatish (`royxat.php`):

```php
<?php
require 'db.php';
$pdo = ulan();

foreach ($pdo->query("SELECT * FROM talabalar") as $t) {
    echo $t['ism'] . "<br>";
}
```

`static $pdo` tufayli `ulan()` ni necha marta chaqirsangiz ham baza **bir marta** ulanadi. Parol o'zgarsa — faqat `db.php` ni tahrirlaysiz, qolgan fayllar tegmaydi.
</details>

<details markdown="1">
<summary>Yechim — 14 (lastInsertId)</summary>

```php
<?php
require 'db.php';
$pdo = ulan();

$stmt = $pdo->prepare("INSERT INTO talabalar (ism, yosh, shahar) VALUES (?, ?, ?)");
$stmt->execute(["Dilnoza", 17, "Namangan"]);

$yangiId = $pdo->lastInsertId();
echo "Qo'shildi! Yangi id = $yangiId";
```

`lastInsertId()` ni `execute()` dan **darhol keyin** chaqiramiz — u oxirgi `INSERT`'da berilgan avtomatik `id`'ni qaytaradi. Bu, masalan, "yangi yozuv sahifasiga yo'naltir" yoki "bog'liq jadvalga shu id bilan yozuv qo'sh" uchun kerak.
</details>

<details markdown="1">
<summary>Yechim — 16 (talabalar ro'yxati sahifasi)</summary>

```php
<?php
require 'db.php';
$pdo = ulan();
$natija = $pdo->query("SELECT * FROM talabalar ORDER BY ism");
?>

<table border="1" cellpadding="8">
    <tr>
        <th>ID</th>
        <th>Ism</th>
        <th>Yosh</th>
        <th>Shahar</th>
    </tr>
    <?php foreach ($natija as $qator): ?>
        <tr>
            <td><?= $qator['id'] ?></td>
            <td><?= $qator['ism'] ?></td>
            <td><?= $qator['yosh'] ?></td>
            <td><?= $qator['shahar'] ?></td>
        </tr>
    <?php endforeach; ?>
</table>
```

> **Yangi narsa: `<?= ... ?>`**. Bu — `<?php echo ... ?>` ning qisqa shakli. HTML ichida PHP qiymatini chiqarish uchun qulay. `<?= $qator['ism'] ?>` degani — "shu yerga ismni chiqar".
>
> Bu misol PHP va HTML'ni birlashtiradi: PHP bazadan ma'lumot oladi, HTML uni chiroyli jadval qilib ko'rsatadi. Bu — haqiqiy veb-sahifaning oddiy ko'rinishi!
</details>

<details markdown="1">
<summary>Yechim — 17 (SQL injection nega xavfli)</summary>

`"WHERE id = $id"` xavfli, chunki foydalanuvchi `$id` o'rniga oddiy son emas, **zararli SQL** kiritishi mumkin. Masalan, manzilga `?id=0 OR 1=1` yozsa, so'rov shunday bo'ladi:

```sql
SELECT * FROM talabalar WHERE id = 0 OR 1=1
```

`1=1` har doim rost — natijada **barcha** talabalar qaytadi. Yomonroq holatda hujumchi `DROP TABLE`, parollarni o'qish kabi buyruqlar qo'shishi mumkin.

`"WHERE id = ?"` (prepared statement) xavfsiz, chunki:

```php
<?php
$stmt = $pdo->prepare("SELECT * FROM talabalar WHERE id = ?");
$stmt->execute([$id]);
```

Bu yerda `$id` **alohida**, "ma'lumot" sifatida yuboriladi — u hech qachon "buyruq" (SQL kod) sifatida bajarilmaydi. Foydalanuvchi `0 OR 1=1` yozsa ham, PHP uni butun matn sifatida `id` ga qo'yadi, kod sifatida emas. Shuning uchun **qoida:** foydalanuvchi ma'lumotini hech qachon so'rov matniga to'g'ridan-to'g'ri qo'shmang — doim `?` va `execute([...])` ishlating.
</details>

<details markdown="1">
<summary>Yechim — 18 (PHP'dan JOIN)</summary>

```php
<?php
require 'db.php';
$pdo = ulan();

$sql = "SELECT kitoblar.nom, mualliflar.ism
        FROM kitoblar
        JOIN mualliflar ON kitoblar.muallif_id = mualliflar.id";

$natija = $pdo->query($sql);

foreach ($natija as $qator) {
    echo $qator['nom'] . " — " . $qator['ism'] . "<br>";
}
// O'tkan kunlar — Abdulla Qodiriy
// Mehrobdan chayon — Abdulla Qodiriy
// Sarob — Abdulla Qahhor
```
JOIN'li so'rov PHP'da ham xuddi oddiy `SELECT` kabi ishlaydi: `query` bilan yuboramiz, `foreach` bilan aylanib chiqamiz. Har bir `$qator` ikkala jadvaldan kelgan ustunlarni (`nom`, `ism`) o'z ichiga oladi. (Bu so'rovda foydalanuvchi ma'lumoti yo'q, shuning uchun `query` yetadi; bo'lsa — `prepare`/`execute` ishlatardik.)
</details>

<details markdown="1">
<summary>Yechim — 19 (transaksiya bilan pul o'tkazish)</summary>

Avval jadval (phpMyAdmin'da bir marta):

```sql
CREATE TABLE hisoblar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    egasi VARCHAR(100),
    balans INT
);
INSERT INTO hisoblar (egasi, balans) VALUES ('Ali', 1000), ('Vali', 500);
```

PHP:

```php
<?php
require 'db.php';
$pdo = ulan();

$summa = 300;

try {
    $pdo->beginTransaction();

    // 1) Alidan yechamiz
    $pdo->prepare("UPDATE hisoblar SET balans = balans - ? WHERE id = ?")
        ->execute([$summa, 1]);

    // 2) Valiga qo'shamiz
    $pdo->prepare("UPDATE hisoblar SET balans = balans + ? WHERE id = ?")
        ->execute([$summa, 2]);

    $pdo->commit();
    echo "O'tkazildi!";

} catch (PDOException $e) {
    $pdo->rollBack();
    echo "Xato — bekor qilindi. Pul joyida.";
}
```

Agar ikkinchi `UPDATE`'da ataylab xato qilsangiz (masalan `balanss` deb noto'g'ri ustun yozsangiz), `ERRMODE_EXCEPTION` tufayli istisno tashlanadi, `catch`ga o'tadi va `rollBack()` **birinchi** `UPDATE`'ni ham bekor qiladi — Ali pulini yo'qotmaydi. Aynan shu — transaksiyaning kuchi: "yo hammasi, yo hech narsa".
</details>

<details markdown="1">
<summary>Yechim — 20 (FETCH_CLASS bilan obyektlar)</summary>

```php
<?php
require 'db.php';
$pdo = ulan();

class Talaba
{
    public int $id = 0;
    public string $ism = '';
    public int $yosh = 0;
    public string $shahar = '';

    public function tanishtir(): string
    {
        return "{$this->ism}, {$this->yosh} yosh, {$this->shahar}dan";
    }
}

$stmt = $pdo->query("SELECT * FROM talabalar");
$talabalar = $stmt->fetchAll(PDO::FETCH_CLASS, Talaba::class);

foreach ($talabalar as $t) {     // har bir $t — Talaba obyekti
    echo $t->tanishtir() . "<br>";
}
```

`fetchAll(PDO::FETCH_CLASS, Talaba::class)` — har bir qatorni `Talaba` obyektiga aylantiradi. Ustun nomlari (`ism`, `yosh`...) class xususiyatlariga mos kelishi kerak. Endi qatorlar oddiy massiv emas, **to'liq obyekt** — ulardan `tanishtir()` kabi metodlarni chaqira olasiz. Bu — bazani obyektga bog'laydigan zamonaviy, toza uslub.
</details>
