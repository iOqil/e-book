# 5.2 MVC — loyihani tartibga solish

[⬅️ Oldingi: 5.1 Toza kod prinsiplari](./36-toza-kod-prinsiplari.md) · [🏠 README](./README.md) · [Keyingi: 5.3 Foydali dizayn andozalari ➡️](./38-foydali-dizayn-andozalari.md)

---

### Muammo: hamma narsa bir faylda aralash

4.2'dagi mini-loyihada PHP mantiq, SQL so'rovlar va HTML — hammasi bitta faylda aralash edi. Kichik loyihada bu yetadi. Lekin loyiha kattalashganda, bunday "aralash" kod tartibsiz va boshqarib bo'lmas holga keladi. Yechim — kodni **vazifalariga ko'ra ajratish**.

### MVC nima?

**MVC** — kodni uchta qismga ajratuvchi mashhur tashkil qilish usuli. Har bir qism bitta vazifaga javob beradi:

- **Model** — **ma'lumot** bilan ishlaydi (ma'lumotlar bazasi: o'qish, yozish). "Ma'lumot qayerda va qanday saqlanadi" — shu qism biladi.
- **View** — **ko'rinish** (HTML). Foydalanuvchi ko'radigan narsa. "Ma'lumot qanday ko'rsatiladi" — shu qism biladi.
- **Controller** — **boshqaruvchi**. So'rovni qabul qiladi, Model'dan ma'lumot oladi, View'ga uzatadi. "Nima qilinishi kerak" — shu qism muvofiqlashtiradi.

Buni restoranga o'xshatish mumkin: **Controller** — ofitsiant (buyurtmani oladi, oshxonaga uzatadi, taomni stolga keltiradi). **Model** — oshpaz (taomni tayyorlaydi, ovqat qayerdaligini biladi). **View** — chiroyli tovoq (taom mijozga qanday ko'rinishi). Har biri o'z ishini qiladi, bir-biriga aralashmaydi.

### Nega bu foydali?

1. **Tartib:** har narsa o'z joyida — ma'lumot mantiqi alohida, ko'rinish alohida.
2. **O'zgartirish oson:** dizaynni (View) o'zgartirsangiz, ma'lumot mantig'iga (Model) tegmaysiz, aksincha ham.
3. **Jamoa ishi:** bir kishi View (dizayn), boshqasi Model (ma'lumot) ustida ishlay oladi.

### Oddiy misol

4.2'dagi talabalar ro'yxatini MVC ruhida ajratamiz. Murakkab freymvork shart emas — shunchaki kodni mantiqiy bo'lamiz:

**Model** (`TalabaModel.php`) — faqat ma'lumot bilan ishlaydi:

```php
<?php
// TalabaModel.php — faqat baza bilan ishlaydi, HTML yo'q
class TalabaModel {
    private $pdo;

    public function __construct($pdo) {
        $this->pdo = $pdo;
    }

    public function hammasi() {
        return $this->pdo->query("SELECT * FROM talabalar ORDER BY id DESC")->fetchAll();
    }

    public function qoshish($ism, $yosh, $shahar) {
        $stmt = $this->pdo->prepare("INSERT INTO talabalar (ism, yosh, shahar) VALUES (?, ?, ?)");
        $stmt->execute([$ism, $yosh, $shahar]);
    }

    public function ochirish($id) {
        $stmt = $this->pdo->prepare("DELETE FROM talabalar WHERE id = ?");
        $stmt->execute([$id]);
    }
}
```

**Controller** (`royxat.php`) — so'rovni boshqaradi, Model'ni ishlatadi:

```php
<?php
// royxat.php — boshqaruvchi
require 'ulanish.php';
require 'TalabaModel.php';

$model = new TalabaModel($pdo);

// Agar forma yuborilgan bo'lsa — qo'shamiz (Model orqali)
if (!empty($_POST['ism'])) {
    $model->qoshish(trim($_POST['ism']), (int)$_POST['yosh'], trim($_POST['shahar']));
    header("Location: royxat.php");
    exit;
}

// Ma'lumotni Model'dan olamiz
$talabalar = $model->hammasi();

// View'ni ko'rsatamiz (ma'lumotni unga uzatib)
require 'talabalar_view.php';
```

**View** (`talabalar_view.php`) — faqat ko'rinish (HTML):

```php
<?php // talabalar_view.php — faqat HTML/ko'rinish ?>
<h1>Talabalar</h1>
<form method="post">
    <input name="ism" placeholder="Ism" required>
    <input name="yosh" type="number" placeholder="Yosh" required>
    <input name="shahar" placeholder="Shahar" required>
    <button>Qo'shish</button>
</form>

<table border="1" cellpadding="8">
    <?php foreach ($talabalar as $t): ?>
        <tr>
            <td><?= htmlspecialchars($t['ism']) ?></td>
            <td><?= $t['yosh'] ?></td>
            <td><?= htmlspecialchars($t['shahar']) ?></td>
        </tr>
    <?php endforeach; ?>
</table>
```

Endi har bir qism aniq: **Model** baza bilan ishlaydi (SQL shu yerda), **View** faqat ko'rinish (HTML shu yerda), **Controller** ularni bog'laydi. Dizaynni o'zgartirmoqchi bo'lsangiz — faqat View'ga tegasiz. SQL so'rovni o'zgartirmoqchi bo'lsangiz — faqat Model'ga.

Quyidagi diagramma so'rov MVC qismlari orasidan qanday oqishini ko'rsatadi:

![MVC arxitekturasi: so'rov Controller'ga, Controller Model/baza bilan ishlaydi, View javob qaytaradi](rasmlar/phd-mvc-arxitektura.svg)

> **Muhim:** bu — MVC'ning **soddalashtirilgan**, "qo'lda" ko'rinishi. Haqiqiy katta loyihalarda MVC'ni tayyor freymvorklar (maxsus vositalar) yordamida qo'llashadi — ular bu tuzilmani avtomatik va kuchli tarzda beradi. Lekin g'oya bir xil: **ma'lumot, ko'rinish va boshqaruvni ajratish.** Freymvorklarni keyingi qadam sifatida (6-QISM) o'rganasiz; hozir g'oyani tushunish muhim.

### Mashqlar

**Oson**
1. MVC'ning uch qismini (Model, View, Controller) o'z so'zingiz bilan tushuntiring.
2. Restoran analogiyasida har bir qism nimaga to'g'ri kelishini ayting.
3. Quyidagi kodlarning qaysi biri Model, qaysi biri View ekanini ayting (SQL bormi yoki HTML bormi).

**O'rta**
4. 4.2'dagi mini-loyihangizni yuqoridagidek uch qismga (Model, Controller, View) ajrating.
5. `TalabaModel`ga `bittasi($id)` metodini qo'shing (bitta talabani id bo'yicha qaytarsin).
6. View'ni o'zgartiring (ranglar, dizayn qo'shing) — Model va Controller'ga tegmasdan. Bu — ajratishning foydasini ko'rsatadi.

**Qiyin**
7. `mahsulotlar` uchun to'liq MVC tuzilmasini yarating: `MahsulotModel` (baza), controller (`mahsulotlar.php`) va view (`mahsulotlar_view.php`). To'liq CRUD (qo'shish, ko'rish, o'chirish) Model metodlari orqali ishlasin.
8. Ikkita Model (`TalabaModel`, `MahsulotModel`) bo'lgan loyihada umumiy ulanish kodini bir joyda ushlang, har bir Model'ni alohida faylda saqlang — toza tashkil etishni mashq qiling.

<details markdown="1">
<summary>Yechim — 3 (Model vs View ni ajratish)</summary>

Qoidani eslang:
- **Model** — ichida **SQL** va baza bilan ishlash bor, HTML yo'q. Masalan, `$pdo->query("SELECT ...")` bor kod — bu Model.
- **View** — ichida **HTML** bor (`<table>`, `<form>`, `<?= ... ?>`), SQL yo'q. Faqat ma'lumotni ko'rsatadi.
- **Controller** — Model'ni chaqiradi va View'ni yuklaydi, lekin o'zida na SQL, na ko'p HTML bo'ladi — u faqat "ulab beradi".

Sinov: kodda `SELECT`/`INSERT` ko'rsangiz → Model. `<table>`/`<form>` ko'rsangiz → View. `require Model` + `require View` ko'rsangiz → Controller.
</details>

<details markdown="1">
<summary>Yechim — 7 (mahsulotlar uchun to'liq MVC)</summary>

```php
<?php
// MahsulotModel.php — faqat baza (SQL shu yerda)
class MahsulotModel {
    private $pdo;
    public function __construct($pdo) { $this->pdo = $pdo; }

    public function hammasi() {
        return $this->pdo->query("SELECT * FROM mahsulotlar ORDER BY id DESC")->fetchAll();
    }
    public function qoshish($nom, $narx) {
        $stmt = $this->pdo->prepare("INSERT INTO mahsulotlar (nom, narx) VALUES (?, ?)");
        $stmt->execute([$nom, $narx]);
    }
    public function ochirish($id) {
        $stmt = $this->pdo->prepare("DELETE FROM mahsulotlar WHERE id = ?");
        $stmt->execute([$id]);
    }
}
```
```php
<?php
// mahsulotlar.php — Controller (boshqaruvchi)
require 'ulanish.php';
require 'MahsulotModel.php';

$model = new MahsulotModel($pdo);

if (!empty($_POST['nom'])) {
    $model->qoshish(trim($_POST['nom']), (int) $_POST['narx']);
    header("Location: mahsulotlar.php");
    exit;
}

$mahsulotlar = $model->hammasi();   // Model'dan ma'lumot
require 'mahsulotlar_view.php';     // View'ga uzatamiz
```
```php
<?php // mahsulotlar_view.php — faqat ko'rinish (HTML) ?>
<form method="post">
    <input name="nom" placeholder="Nom" required>
    <input name="narx" type="number" placeholder="Narx" required>
    <button>Qo'shish</button>
</form>
<table border="1" cellpadding="8">
    <?php foreach ($mahsulotlar as $m): ?>
        <tr><td><?= htmlspecialchars($m['nom']) ?></td><td><?= number_format($m['narx']) ?> so'm</td></tr>
    <?php endforeach; ?>
</table>
```
Talabalar MVC'si bilan tuzilma bir xil: **Model** (SQL), **Controller** (boshqaruv), **View** (HTML) — faqat jadval/maydonlar mahsulotlarga moslangan. Har bir qism o'z ishini qiladi.
</details>

<details markdown="1">
<summary>Yechim — 8 (ikkita Model, umumiy ulanish)</summary>

Fayl tuzilmasi:
```
ulanish.php          → faqat $pdo ni yaratadi (umumiy, bir joyda)
TalabaModel.php      → class TalabaModel  (talabalar bilan ishlaydi)
MahsulotModel.php    → class MahsulotModel (mahsulotlar bilan ishlaydi)
index.php            → controller: ulanishni va kerakli Model(lar)ni yuklaydi
```
```php
<?php
// index.php
require 'ulanish.php';          // $pdo bir marta yaratiladi
require 'TalabaModel.php';
require 'MahsulotModel.php';

$talabaModel   = new TalabaModel($pdo);     // bitta ulanish...
$mahsulotModel = new MahsulotModel($pdo);   // ...ikkala Model'ga beriladi (DI)

$talabalar   = $talabaModel->hammasi();
$mahsulotlar = $mahsulotModel->hammasi();
```
Asosiy g'oya: ulanish (`$pdo`) **bir joyda** yaratiladi va kerakli har bir Model'ga **konstruktor orqali** beriladi (bu — Dependency Injection, 5.3'da ko'ramiz). Har bir Model alohida faylda, faqat o'z jadvali bilan ishlaydi. Bu — toza, kengaytiriladigan tuzilma.
</details>
