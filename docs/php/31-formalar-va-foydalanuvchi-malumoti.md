# 4.1 Formalar va foydalanuvchi ma'lumoti

[⬅️ Oldingi: 3.7 PostgreSQL va MySQL'dan farqlari](./30-postgresql-va-mysqldan-farqlari.md) · [🏠 README](./README.md) · [Keyingi: 4.2 To'liq mini-loyiha: talabalar ro'yxati (CRUD) ➡️](./32-toliq-mini-loyiha-talabalar-royxati.md)

---

Hozirgacha ma'lumotni kod ichida o'zimiz yozardik (`$ism = "Ali"`). Lekin haqiqiy saytda ma'lumotni **foydalanuvchi** kiritadi: ro'yxatdan o'tish formasi, qidiruv maydoni, izoh yozish. Bu bo'limda foydalanuvchidan ma'lumot olishni o'rganamiz — bu PHP'ning asosiy vazifalaridan biri.

### Forma — ma'lumot kiritish oynasi

**Forma (form)** — bu sahifadagi maydonlar (matn katakchasi, tugma va h.k.) orqali foydalanuvchidan ma'lumot oladigan qism. Forma HTML bilan yoziladi:

```html
<form method="post" action="natija.php">
    Ismingiz: <input type="text" name="ism">
    <br>
    Yoshingiz: <input type="number" name="yosh">
    <br>
    <button type="submit">Yuborish</button>
</form>
```

Tushuntiramiz:
- **`<form>`** — forma boshlanishi.
- **`method="post"`** — ma'lumot qanday yuborilishi (pastda tushuntiramiz).
- **`action="natija.php"`** — ma'lumot **qaysi faylga** yuboriladi. "Yuborish" bosilganda, forma `natija.php` ga ma'lumotni jo'natadi.
- **`<input type="text" name="ism">`** — matn kiritish maydoni. **`name="ism"`** juda muhim: bu maydonning "nomi", PHP'da shu nom orqali qiymatni olamiz.
- **`<button type="submit">`** — yuborish tugmasi.

### Ma'lumotni PHP'da olish — `$_POST`

Forma yuborilganda, ma'lumot `action`dagi faylga keladi. PHP uni **`$_POST`** degan maxsus massivdan oladi (`method="post"` bo'lsa):

```php
<?php
// natija.php fayli
$ism = $_POST['ism'];     // formadagi name="ism" maydonidan
$yosh = $_POST['yosh'];   // name="yosh" maydonidan

echo "Salom, " . $ism . "! Siz " . $yosh . " yoshdasiz.";
```

`$_POST` — bu PHP avtomatik to'ldiradigan **kalitli massiv** (1.8'da o'rgangan!). Kalitlari — formadagi maydon nomlari (`name`). `$_POST['ism']` — "formadagi ism maydonining qiymati".

> **Ikki fayl ishtirok etadi:** biri forma (HTML) — uni brauzerda ochib to'ldirasiz; ikkinchisi natija fayli (PHP) — forma yuborilganda ishlaydi va ma'lumotni qabul qiladi. `action` ularni bog'laydi.

### `$_GET` va `$_POST` farqi

Ma'lumot yuborishning ikki usuli bor:

- **POST** (`$_POST`) — ma'lumot "yashirin" yuboriladi (manzilda ko'rinmaydi). Parol, shaxsiy ma'lumot, ma'lumot saqlash uchun ishlatiladi.
- **GET** (`$_GET`) — ma'lumot **manzil qatorida** yuboriladi (`sayt.php?ism=Ali&yosh=19` ko'rinishida). Qidiruv, filtrlash, havola orqali ma'lumot uzatish uchun.

```php
<?php
// Manzil: natija.php?ism=Ali
echo $_GET['ism'];   // Ali
```

Oddiy qoida: **ma'lumotni o'zgartirish/saqlash** (forma yuborish, ro'yxatdan o'tish) → POST. **Ma'lumot olish/qidirish** → GET.

Quyidagi diagramma formadan ma'lumot serverga qanday borishini va POST hamda GET farqini ko'rsatadi:

![Forma serverga: $_POST/$_GET orqali PHP'ga ma'lumot uzatish, POST va GET farqi](rasmlar/phd-forma-server.svg)

### Ma'lumotni tekshirish (juda muhim!)

Foydalanuvchi ma'lumotiga **hech qachon ishonmang** — u bo'sh, noto'g'ri yoki zararli bo'lishi mumkin. Doim tekshiring:

```php
<?php
// Maydon to'ldirilganmi, tekshiramiz
if (empty($_POST['ism'])) {
    echo "Iltimos, ismingizni kiriting!";
} else {
    $ism = trim($_POST['ism']);   // ortiqcha bo'sh joyni tozalaymiz (1.5)
    echo "Salom, " . htmlspecialchars($ism);
}
```

- **`empty(...)`** — maydon bo'sh yoki to'ldirilmaganmi, tekshiradi.
- **`trim(...)`** — ortiqcha bo'sh joyni oladi.
- **`htmlspecialchars(...)`** — bu **muhim xavfsizlik vositasi**: foydalanuvchi kiritgan matnni "zararsizlantiradi". Buni 4.4'da (xavfsizlik) batafsil ko'ramiz — hozircha shuni eslang: foydalanuvchi matnini ekranga chiqarganda doim `htmlspecialchars` orqali chiqaring.

### Mashqlar

> Bu mashqlar uchun ikki fayl yarating: `forma.php` (HTML forma) va `natija.php` (qabul qiluvchi PHP). `forma.php` ni brauzerda oching.

**Oson**
1. Bitta matn maydonli forma yarating (ism uchun), yuborilganda ismni chiqaring.
2. Formaga yosh maydonini ham qo'shing, ikkalasini ham chiqaring.
3. `$_POST` o'rniga `$_GET` ishlatib ko'ring (`method="get"`), manzilda ma'lumot ko'rinishini kuzating.
4. Forma orqali kelgan ismni katta harfda (`strtoupper`) chiqaring.
5. `empty` bilan ism bo'sh yuborilsa "Ism kiriting" deb chiqaring.

**O'rta**
6. Ro'yxatdan o'tish formasi: ism, email, yosh. Hammasini olib, chiroyli chiqaring.
7. Forma orqali ikkita son olib, ularning yig'indisini chiqaring (kalkulyator).
8. Kelgan ismni `trim` va `htmlspecialchars` bilan tozalab chiqaring.
9. Forma maydonlarining hammasi to'ldirilganini tekshiring; biror bo'sh bo'lsa, qaysi biri ekanini ayting.
10. Yoshni tekshiring: agar 18 dan kichik bo'lsa "Voyaga yetmagan", aks holda "Voyaga yetgan".

**Qiyin**
11. To'liq kalkulyator formasi: ikki son va amal (qo'shish/ayirish/ko'paytirish — `<select>` orqali tanlash). Tanlangan amalni bajarib, natijani chiqaring (`if`/`match` bilan).
12. Bir faylda forma **va** uni qabul qilish (alohida fayl emas): forma `action` ni o'ziga (bo'sh `action` yoki o'sha fayl) yo'naltiring, PHP qismida `if ($_POST)` bilan ma'lumot kelgan-kelmaganini tekshiring.

<details markdown="1">
<summary>Yechim — 11 (to'liq kalkulyator)</summary>

```php
<?php
// kalkulyator.php — forma va hisob bir faylda
$natija = null;

if (!empty($_POST['a']) && !empty($_POST['b'])) {
    $a = (float) $_POST['a'];
    $b = (float) $_POST['b'];

    $natija = match($_POST['amal']) {
        'qoshish'     => $a + $b,
        'ayirish'     => $a - $b,
        'kopaytirish' => $a * $b,
        'bolish'      => $b != 0 ? $a / $b : "0 ga bo'lib bo'lmaydi",
        default       => "Noma'lum amal",
    };
}
?>

<form method="post">
    <input type="number" name="a" step="any" required>
    <select name="amal">
        <option value="qoshish">+</option>
        <option value="ayirish">−</option>
        <option value="kopaytirish">×</option>
        <option value="bolish">÷</option>
    </select>
    <input type="number" name="b" step="any" required>
    <button type="submit">=</button>
</form>

<?php if ($natija !== null): ?>
    <p>Natija: <strong><?= htmlspecialchars((string) $natija) ?></strong></p>
<?php endif; ?>
```
`<select>` dan tanlangan amal `$_POST['amal']` ga keladi; `match` uni tegishli hisobga yo'naltiradi. `(float)` — kelgan matnni songa aylantiradi (forma har doim matn yuboradi). Nolga bo'lishni alohida tekshirdik. Forma o'ziga yuboriladi (`action` yo'q), natija pastda chiqadi.
</details>

<details markdown="1">
<summary>Yechim — 12 (forma + qabul bir faylda)</summary>

```php
<?php
// salom.php — forma va qabul bir faylda
$xabar = "";

if (!empty($_POST['ism'])) {              // forma yuborilganmi?
    $ism = htmlspecialchars(trim($_POST['ism']));
    $xabar = "Salom, " . $ism . "!";
}
?>

<form method="post">
    Ismingiz: <input type="text" name="ism">
    <button type="submit">Yuborish</button>
</form>

<p><?= $xabar ?></p>
```
Bu — keng tarqalgan uslub: bitta fayl ham formani ko'rsatadi, ham yuborilganda qabul qiladi. `action` yozilmagani uchun, forma o'ziga yuboriladi. PHP avval ma'lumot kelgan-kelmaganini tekshiradi (`if (!empty(...))`), kelgan bo'lsa — javob tayyorlaydi.
</details>
