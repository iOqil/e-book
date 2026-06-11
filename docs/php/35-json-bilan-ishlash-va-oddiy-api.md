# 4.5 JSON bilan ishlash va oddiy API

[⬅️ Oldingi: 4.4 Xavfsizlik asoslari](./34-xavfsizlik-asoslari.md) · [🏠 README](./README.md) · [Keyingi: 4.6 Fayl bilan ishlash va fayl yuklash ➡️](./fayl-yuklash.md)

---

### JSON nima va nega kerak?

Zamonaviy saytlarda backend (PHP) va frontend (JavaScript), yoki bir dastur va boshqasi, ma'lumot almashadi. Lekin ular bir-biriga PHP massivini "to'g'ridan-to'g'ri" jo'nata olmaydi. Kerak — barcha tillar tushunadigan **umumiy matn formati**. Ana shu — **JSON** (JavaScript Object Notation).

JSON oddiy matn ko'rinishida, lekin tuzilmali. Bizning kalitli massivga juda o'xshaydi:

```json
{
  "ism": "Ali",
  "yosh": 19,
  "faol": true
}
```

> JSON 1.8'dagi kalitli massivga o'xshashi bejiz emas — u aynan shunday "kalit: qiymat" tuzilmasini matn ko'rinishida ifodalaydi. Shuning uchun PHP massivini JSON'ga (va aksincha) aylantirish juda oson.

### PHP massivini JSON'ga — `json_encode`

```php
<?php
$talaba = ["ism" => "Ali", "yosh" => 19, "faol" => true];

$json = json_encode($talaba);
echo $json;   // {"ism":"Ali","yosh":19,"faol":true}
```

O'zbekcha (va boshqa) harflar to'g'ri chiqishi va chiroyli ko'rinish uchun ikkita "flag" qo'shamiz:

```php
<?php
$talaba = ["ism" => "Ali", "shahar" => "Toshkent"];

echo json_encode($talaba, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
// {
//     "ism": "Ali",
//     "shahar": "Toshkent"
// }
```

- **`JSON_UNESCAPED_UNICODE`** — o'zbekcha/kirill harflarni `\u...` ko'rinishida emas, o'zidek chiqaradi.
- **`JSON_PRETTY_PRINT`** — chiroyli, qatorlarga bo'lib (o'qishga qulay). Ikkalasini `|` bilan birga beramiz.

### JSON'ni PHP massiviga — `json_decode`

Aksincha, kelgan JSON matnni PHP massiviga aylantiramiz:

```php
<?php
$matn = '{"ism":"Vali","yosh":21}';

$data = json_decode($matn, true);   // true → kalitli massiv qaytaradi

echo $data["ism"];    // Vali
echo $data["yosh"];   // 21
```

> **Diqqat: ikkinchi parametr `true`.** Usiz `json_decode` obyekt qaytaradi (`$data->ism`). `true` bersangiz — bizga tanish kalitli massiv (`$data["ism"]`). Boshlanishida `true` bilan ishlash osonroq.

### Oddiy API — PHP ma'lumotni JSON sifatida qaytaradi

"API" — bu sahifa HTML emas, **JSON qaytaradigan** manzil. Frontend (JavaScript) shu manzilga murojaat qilib, ma'lumotni oladi. Mana bazadan o'qib, JSON beradigan oddiy API:

```php
<?php
// api_talabalar.php
require 'ulanish.php';

header('Content-Type: application/json; charset=utf-8');   // "men JSON qaytaraman"

$talabalar = $pdo->query("SELECT id, ism, yosh FROM talabalar")->fetchAll(PDO::FETCH_ASSOC);

echo json_encode($talabalar, JSON_UNESCAPED_UNICODE);
// [{"id":1,"ism":"Ali","yosh":19}, {"id":2,"ism":"Vali","yosh":21}]
```

- **`header('Content-Type: application/json...')`** — brauzerga "bu HTML emas, JSON" deb aytadi. Bu qator har qanday `echo`'dan **oldin** turishi kerak.
- Bazadan kelgan qatorlar (massivlar massivi) `json_encode` bilan to'g'ridan-to'g'ri JSON'ga aylanadi.

Bu — zamonaviy veb-ning asosi: PHP ma'lumotni JSON sifatida beradi, JavaScript uni olib, sahifada ko'rsatadi (sahifani qayta yuklamasdan). 6-QISMda bu yo'nalishni ("API va frontend") yana ko'rasiz.

### Mashqlar

**Oson**
1. Bir kalitli massiv (kitob: nom, muallif, yil) yarating va `json_encode` bilan JSON chiqaring.
2. `JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT` flaglari bilan o'zbekcha matnli massivni chiroyli JSON qiling.
3. Berilgan JSON matnni (`'{"nom":"Olma","narx":5000}'`) `json_decode` bilan massivga aylantiring va qiymatlarini chiqaring.

**O'rta**
4. Massivlar massivini (3 ta mahsulot) JSON'ga aylantiring.
5. JSON matndagi mahsulotlar ro'yxatini `json_decode` bilan o'qib, `foreach` bilan har birini chiqaring.
6. `json_encode` natijasini `json_decode` bilan qayta massivga aylantiring (aylanma yo'l) va asl bilan solishtiring.

**Qiyin**
7. Oddiy API yarating: `talabalar` jadvalidan o'qib, JSON qaytaring (`header` bilan, `JSON_UNESCAPED_UNICODE`). Brauzerda manzilni ochib, JSON natijani ko'ring.
8. JSON faylni (`malumot.json`) o'qib (`file_get_contents`), `json_decode` qilib, ichidagi ma'lumotni jadval ko'rinishida chiqaring.

<details markdown="1">
<summary>Yechim — 5 (JSON ro'yxatni o'qish)</summary>

```php
<?php
$matn = '[
    {"nom":"Olma","narx":5000},
    {"nom":"Anor","narx":12000},
    {"nom":"Uzum","narx":8000}
]';

$mahsulotlar = json_decode($matn, true);   // massivlar massivi

foreach ($mahsulotlar as $m) {
    echo $m["nom"] . " — " . number_format($m["narx"]) . " so'm<br>";
}
// Olma — 5,000 so'm
// Anor — 12,000 so'm
// Uzum — 8,000 so'm
```
`json_decode(..., true)` JSON ro'yxatni kalitli massivlar massiviga aylantirdi — keyin uni xuddi 1.8'dagidek `foreach` bilan aylanib chiqamiz.
</details>

<details markdown="1">
<summary>Yechim — 7 (oddiy JSON API)</summary>

```php
<?php
// api_talabalar.php
require 'ulanish.php';

header('Content-Type: application/json; charset=utf-8');

$talabalar = $pdo
    ->query("SELECT id, ism, yosh, shahar FROM talabalar ORDER BY id")
    ->fetchAll(PDO::FETCH_ASSOC);

echo json_encode($talabalar, JSON_UNESCAPED_UNICODE);
```
Brauzerda `http://localhost/darslar/api_talabalar.php` ni ochsangiz — HTML emas, sof JSON ko'rasiz. Bu — frontend (JavaScript) "iste'mol qiladigan" API. `header(...)` `echo`'dan oldin turishi shart.
</details>

<details markdown="1">
<summary>Yechim — 8 (JSON faylni o'qish)</summary>

`malumot.json` faylida:
```json
[
    {"nom": "Olma", "narx": 5000},
    {"nom": "Anor", "narx": 12000}
]
```

PHP uni o'qib, jadval qiladi:
```php
<?php
$matn = file_get_contents("malumot.json");   // faylni matn sifatida o'qiydi
$mahsulotlar = json_decode($matn, true);      // JSON → massiv
?>

<table border="1" cellpadding="8">
    <tr><th>Nom</th><th>Narx</th></tr>
    <?php foreach ($mahsulotlar as $m): ?>
        <tr>
            <td><?= htmlspecialchars($m['nom']) ?></td>
            <td><?= number_format($m['narx']) ?> so'm</td>
        </tr>
    <?php endforeach; ?>
</table>
```
`file_get_contents("fayl")` faylni butunligicha matn sifatida o'qiydi, `json_decode(..., true)` esa uni massivga aylantiradi. Keyin xuddi bazadan kelgandek `foreach` bilan jadval qilamiz. Ko'p tashqi xizmatlar (ob-havo, valyuta kurslari) ma'lumotni aynan JSON sifatida beradi — shuning uchun JSON o'qishni bilish muhim.
</details>

---

> **4-QISM yakunlandi!** Endi siz haqiqiy veb-dastur yoza olasiz: formalar orqali foydalanuvchi bilan muloqot, ma'lumotlar bazasi bilan to'liq CRUD, sessiyalar va login tizimi, asosiy xavfsizlik (parol hashlash, XSS, SQL injection himoyasi) va ma'lumotni JSON sifatida almashish (oddiy API). Bu — haqiqiy, foydalanuvchilar ishlatadigan dastur yozish darajasi.
