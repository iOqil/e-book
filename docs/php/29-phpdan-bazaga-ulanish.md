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
- **`"mysql:host=localhost;dbname=maktab;..."`** — ulanish ma'lumotlari: `mysql` turi, `localhost` (shu kompyuter), `dbname=maktab` (qaysi baza).
- **`"root"`** va **`""`** — foydalanuvchi va parol. XAMPP'da standart sozlama: foydalanuvchi `root`, parol bo'sh.

> Agar ulanish xato bersa, MySQL XAMPP'da ishlab turganini tekshiring va baza nomi to'g'riligiga ishonch hosil qiling.

### Ma'lumot o'qish — `query`

Oddiy o'qish so'rovini `query` bilan yuboramiz va natijani `foreach` bilan aylanib chiqamiz:

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=maktab;charset=utf8mb4", "root", "");

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

### Foydalanuvchi ma'lumoti bilan ishlash — XAVFSIZLIK

Endi eng muhim mavzu. Ko'pincha so'rovga **foydalanuvchidan kelgan** ma'lumot qo'shamiz. Masalan, "id'si shu bo'lgan talabani top". Buni **noto'g'ri** qilish — jiddiy xavfsizlik teshigiga olib keladi.

**❌ XAVFLI usul — hech qachon bunday qilmang:**

```php
<?php
$id = $_GET['id'];   // foydalanuvchidan kelgan ma'lumot
// XAVFLI: foydalanuvchi ma'lumotini to'g'ridan-to'g'ri so'rovga qo'shish
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

### Ma'lumot qo'shish (xavfsiz)

```php
<?php
$ism = "Yangi Talaba";
$yosh = 18;
$shahar = "Toshkent";

$stmt = $pdo->prepare("INSERT INTO talabalar (ism, yosh, shahar) VALUES (?, ?, ?)");
$stmt->execute([$ism, $yosh, $shahar]);

echo "Talaba qo'shildi!";
```

Bir nechta qiymat bo'lsa, har biriga bitta `?` qo'yamiz va `execute`ga massiv sifatida (tartibda) beramiz.

### Mashqlar

> Bu mashqlar uchun `maktab` bazasi va `talabalar` jadvali tayyor bo'lsin. Fayllarni `htdocs/darslar` ichida yarating, `http://localhost/...` orqali oching.

**Oson**
1. PDO bilan `maktab` bazasiga ulaning (xato bo'lmasligini tekshiring).
2. `query` bilan barcha talabalarni o'qing va `foreach` bilan ismlarini chiqaring.
3. Har bir talabaning ism va yoshini birga chiqaring.
4. `prepare`/`execute` bilan id'si 1 bo'lgan talabani toping va chiqaring.
5. `prepare`/`execute` bilan yangi talaba qo'shing.

**O'rta**
6. Faqat Toshkentdagi talabalarni o'qing (`WHERE shahar = ?` bilan, prepared).
7. `fetchAll()` bilan barcha talabalarni massivga oling va sonini (`count`) chiqaring.
8. `mahsulotlar` jadvalidagi barcha mahsulotlarni narxi bilan chiqaring.
9. Foydalanuvchidan kelgan `$_GET['id']` bo'yicha talabani xavfsiz (prepared) qidiring.
10. Bir talabaning yoshini `UPDATE` + prepared statement bilan o'zgartiring.

**Qiyin**
11. To'liq "talabalar ro'yxati" sahifasini yarating: bazadan barcha talabalarni o'qib, ularni HTML jadval (`<table>`) ko'rinishida chiqaring. (`<table>`, `<tr>`, `<td>` teglaridan foydalaning — internetdan ko'ring.)
12. SQL injection xavfini amalda tushuntiring: nima uchun `"WHERE id = $id"` xavfli va `"WHERE id = ?"` xavfsiz ekanini o'z so'zingiz bilan yozing.
13. JOIN'ni PHP'dan ishlating: `kitoblar` va `mualliflar` ni JOIN qilib, har bir kitob nomi va muallifini PHP bilan o'qib chiqaring.

<details markdown="1">
<summary>Yechim — 11 (talabalar ro'yxati sahifasi)</summary>

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=maktab;charset=utf8mb4", "root", "");
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
<summary>Yechim — 12 (SQL injection nega xavfli)</summary>

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
<summary>Yechim — 13 (PHP'dan JOIN)</summary>

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=maktab;charset=utf8mb4", "root", "");

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
