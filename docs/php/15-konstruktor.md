# 2.2 Konstruktor

[⬅️ Oldingi: 2.1 Class va obyekt — eng asosiy tushuncha](./14-class-va-obyekt-eng-asosiy-tushuncha.md) · [🏠 README](./README.md) · [Keyingi: 2.3 Kirish darajalari: public va private ➡️](./16-kirish-darajalari-public-va-private.md)

---

Oldingi bo'limda obyekt yaratib, keyin xususiyatlariga alohida qiymat berardik:

```php
<?php
$t = new Talaba();
$t->ism = "Ali";        // bir qator
$t->yosh = 19;          // yana bir qator
```

Bu uzun va noqulay. Agar har bir talabani yaratganda 5 ta xususiyatga qiymat berish kerak bo'lsa-chi? **Konstruktor** ana shuni hal qiladi: obyekt yaratilayotgan paytdayoq xususiyatlarni to'ldiradi.

### Konstruktor nima?

**Konstruktor — obyekt `new` bilan yaratilganda avtomatik ishga tushadigan maxsus metod.** Uning vazifasi — obyektni "boshlang'ich holatga keltirish" (xususiyatlarni to'ldirish). U `__construct` deb nomlanadi (boshida ikkita pastki chiziq):

```php
<?php
class Talaba {
    public $ism;
    public $yosh;

    // Konstruktor — obyekt yaratilganda avtomatik chaqiriladi
    public function __construct($ism, $yosh) {
        $this->ism = $ism;     // kelgan qiymatni xususiyatga saqlaymiz
        $this->yosh = $yosh;
    }
}

// Endi obyekt yaratganda darrov qiymat beramiz:
$t = new Talaba("Ali", 19);

echo $t->ism;    // Ali
echo "<br>";
echo $t->yosh;   // 19
```

Nima sodir bo'ldi:
- `new Talaba("Ali", 19)` deganimizda, `__construct` avtomatik ishga tushdi va `"Ali"`, `19` qiymatlarini qabul qildi.
- Konstruktor ichida `$this->ism = $ism` — kelgan qiymatni obyektning xususiyatiga saqladi.
- Natijada obyekt yaratilishi bilan to'liq tayyor bo'ldi — alohida qatorlar shart emas.

> **`$this->ism = $ism` chalkash tuyulishi mumkin.** Bu yerda ikki xil narsa bor:
> - `$this->ism` — obyektning **xususiyati** (class ichida e'lon qilingan).
> - `$ism` — konstruktorga **kelgan parametr** (tashqaridan berilgan qiymat).
>
> Ya'ni "tashqaridan kelgan `$ism`ni, obyektning `$this->ism` xususiyatiga saqla". Ular bir xil nomda bo'lsa ham — ikki alohida narsa.

### Nima uchun foydali?

1. **Qisqalik:** bir qatorda to'liq obyekt.
2. **Kafolat:** konstruktor talab qilgan ma'lumotsiz obyekt yaratib bo'lmaydi. Yuqoridagi misolda `new Talaba()` (ism va yoshsiz) — xato beradi. Demak, har bir talabada albatta ism va yosh bo'ladi — "yarim to'ldirilgan" obyekt bo'lmaydi.

### Konstruktorda boshlang'ich amal ham bajarish mumkin

Konstruktor faqat qiymat saqlash bilan cheklanmaydi — obyekt yaratilganda kerakli har qanday tayyorgarlikni qilishi mumkin:

```php
<?php
class Hisob {
    public $egasi;
    public $balans;

    public function __construct($egasi) {
        $this->egasi = $egasi;
        $this->balans = 0;        // har bir yangi hisob 0 balans bilan ochiladi
    }
}

$h = new Hisob("Ali");
echo $h->egasi;    // Ali
echo "<br>";
echo $h->balans;   // 0
```

### Standart qiymatli parametr (konstruktorda ham)

1.9'dagi standart qiymat konstruktorda ham ishlaydi:

```php
<?php
class Talaba {
    public $ism;
    public $shahar;

    public function __construct($ism, $shahar = "Toshkent") {
        $this->ism = $ism;
        $this->shahar = $shahar;
    }
}

$t1 = new Talaba("Ali");             // shahar berilmadi → "Toshkent"
$t2 = new Talaba("Vali", "Samarqand");

echo $t1->shahar;   // Toshkent
echo "<br>";
echo $t2->shahar;   // Samarqand
```

### Mashqlar

**Oson**
1. `Talaba` classiga konstruktor qo'shing (`ism`, `yosh`). Obyektni bir qatorda yarating.
2. `Mashina` classiga konstruktor qo'shing (`rang`, `tezlik`) va obyekt yarating.
3. `Mahsulot` classi: konstruktor `nom` va `narx` olsin. Obyekt yaratib, ma'lumotini chiqaring.
4. `Kitob` classi: konstruktor `nom`, `muallif`, `yil` olsin.
5. `Hisob` classi: konstruktor `egasi` olsin, `balans` esa konstruktor ichida 0 ga o'rnatilsin.

**O'rta**
6. `Talaba` classiga konstruktor (`ism`, `ball`) va `otdimi()` metodini qo'shing (ball 60+ bo'lsa "O'tdi").
7. `Aylana` classi: konstruktor `radius` olsin, `yuza()` metodi yuzani qaytarsin.
8. `Mahsulot` classiga standart qiymatli parametr qo'shing: `valyuta = "so'm"`.
9. `Foydalanuvchi` classi: konstruktor `ism`, `email` olsin, `parol` esa standart qiymatga ega bo'lsin.
10. `Tortburchak` classi: konstruktor `eni`, `boyi` olsin; `yuza()` va `perimetr()` metodlari bo'lsin.

**Qiyin**
11. `Hisob` classi: konstruktor `egasi` va ixtiyoriy `boshlangichBalans` (standart 0) olsin. `pulQoshish`, `pulYechish`, `korsat` metodlari bo'lsin.
12. `Talaba` classi: konstruktor `ism` va bir nechta `ball`larni massiv sifatida olsin; `ortacha()` metodi o'rtacha ballni hisoblab qaytarsin.
13. `Mashina` classi: konstruktor `rang` olsin, `tezlik` 0 dan boshlansin; `tezlash()` har chaqirilganda tezlikni 10 ga oshirsin, `tormoz()` 10 ga kamaytirsin (lekin 0 dan past bo'lmasin).

<details markdown="1">
<summary>Yechim — 7</summary>

```php
<?php
class Aylana {
    public $radius;

    public function __construct($radius) {
        $this->radius = $radius;
    }

    public function yuza() {
        return 3.14 * $this->radius * $this->radius;
    }
}

$a = new Aylana(5);
echo "Yuza: " . $a->yuza();   // Yuza: 78.5
```
Konstruktor radiusni saqlaydi, `yuza()` metodi esa `$this->radius` orqali o'sha radiusdan yuzani hisoblaydi.
</details>

<details markdown="1">
<summary>Yechim — 11 (Hisob: ixtiyoriy boshlang'ich balans)</summary>

```php
<?php
class Hisob {
    public $egasi;
    public $balans;

    public function __construct($egasi, $boshlangichBalans = 0) {
        $this->egasi = $egasi;
        $this->balans = $boshlangichBalans;   // berilmasa — 0
    }

    public function pulQoshish($summa) {
        $this->balans += $summa;
    }

    public function pulYechish($summa) {
        if ($summa <= $this->balans) {
            $this->balans -= $summa;
        }
    }

    public function korsat() {
        return $this->egasi . ": " . $this->balans . " so'm";
    }
}

$h = new Hisob("Ali", 100000);   // boshlang'ich balans bilan
$h->pulQoshish(50000);
$h->pulYechish(30000);
echo $h->korsat();   // Ali: 120000 so'm

$h2 = new Hisob("Vali");         // boshlang'ich balanssiz — 0 dan
echo "<br>" . $h2->korsat();     // Vali: 0 so'm
```
`$boshlangichBalans = 0` — standart qiymatli parametr: berilsa o'shani, berilmasa 0 ni oladi. Shu tufayli `new Hisob("Ali", 100000)` ham, `new Hisob("Vali")` ham ishlaydi.
</details>

<details markdown="1">
<summary>Yechim — 12 (o'rtacha ball)</summary>

```php
<?php
class Talaba {
    public $ism;
    public $ballar;

    public function __construct($ism, $ballar) {
        $this->ism = $ism;
        $this->ballar = $ballar;   // bu — massiv
    }

    public function ortacha() {
        $yigindi = 0;
        foreach ($this->ballar as $ball) {
            $yigindi += $ball;
        }
        return $yigindi / count($this->ballar);
    }
}

$t = new Talaba("Ali", [80, 90, 70]);
echo $t->ism . " o'rtacha bali: " . $t->ortacha();   // Ali o'rtacha bali: 80
```
Bu yerda xususiyat **massiv** bo'lishi mumkinligini ko'ramiz. `ortacha()` metodi 1.8'da o'rgangan "massiv yig'indisi" mantig'ini class ichida ishlatadi.
</details>

<details markdown="1">
<summary>Yechim — 13 (Mashina: tezlash va tormoz)</summary>

```php
<?php
class Mashina {
    public $rang;
    public $tezlik = 0;   // har doim 0 dan boshlanadi

    public function __construct($rang) {
        $this->rang = $rang;
    }

    public function tezlash() {
        $this->tezlik += 10;
    }

    public function tormoz() {
        $this->tezlik -= 10;
        if ($this->tezlik < 0) {
            $this->tezlik = 0;   // manfiy bo'lib ketmasin
        }
    }
}

$m = new Mashina("qizil");
$m->tezlash();   // 10
$m->tezlash();   // 20
$m->tormoz();    // 10
echo $m->tezlik; // 10

$m->tormoz();    // 0
$m->tormoz();    // hali ham 0 (manfiy emas)
echo "<br>" . $m->tezlik;   // 0
```
`tormoz()` da `if ($this->tezlik < 0)` tekshiruvi tezlikning manfiy bo'lib ketishini oldini oladi. (Buni `$this->tezlik = max(0, $this->tezlik - 10);` deb bitta qatorda ham yozsa bo'ladi.)
</details>
