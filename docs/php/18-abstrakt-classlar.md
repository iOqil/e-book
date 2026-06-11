# 2.5 Abstrakt class'lar

[⬅️ Oldingi: 2.4 Meros (inheritance)](./17-meros.md) · [🏠 README](./README.md) · [Keyingi: 2.6 Interfeys (interface) ➡️](./19-interfeys.md)

---

Bu va keyingi bo'lim (interfeys) — biroz mavhumroq tushunchalar. Sabrli bo'ling: misollar bilan oydinlashadi.

### Muammo

`Shakl` degan class bo'lsin. Har bir shaklning yuzasi bor (`yuza()`). Lekin "umuman shakl"ning yuzasini hisoblab bo'lmaydi — yuza shaklga bog'liq: kvadratniki bir xil formula, aylananiki boshqa. Ya'ni:
- "Har bir shaklda yuza **bo'lishi shart**" — buni ayta olamiz.
- Lekin "umumiy shakl yuzasi" — ma'noga ega emas. Faqat aniq shakl (kvadrat, aylana) yuzasini hisoblay olamiz.
- Va "umuman shakl" obyektini yaratish ham mantiqsiz — "qanaqa shakl?" degan savol qoladi.

**Abstrakt class** ana shuni ifodalaydi: u "tugallanmagan andoza" — qoidalarni belgilaydi, lekin to'liq emas; undan to'g'ridan-to'g'ri obyekt yaratib bo'lmaydi.

### Abstrakt class

`abstract` so'zi bilan e'lon qilinadi. Ichida **abstrakt metod** bo'lishi mumkin — bu metodning faqat nomi e'lon qilinadi, ichi (kodi) yozilmaydi. Ichini meros oluvchi bola class to'ldirishi **shart**:

```php
<?php
abstract class Shakl {
    // Abstrakt metod — faqat e'lon, ichi yo'q.
    // "Har bir shaklda yuza() bo'lishi SHART" degani.
    abstract public function yuza();

    // Oddiy metod ham bo'lishi mumkin (umumiy, ichi bor)
    public function tasvirla() {
        echo "Bu shaklning yuzasi: " . $this->yuza();
    }
}

class Kvadrat extends Shakl {
    private $tomon;

    public function __construct($tomon) {
        $this->tomon = $tomon;
    }

    // Abstrakt metodni TO'LDIRISH shart:
    public function yuza() {
        return $this->tomon * $this->tomon;
    }
}

class Aylana extends Shakl {
    private $radius;

    public function __construct($radius) {
        $this->radius = $radius;
    }

    public function yuza() {
        return 3.14 * $this->radius * $this->radius;
    }
}

$k = new Kvadrat(5);
$k->tasvirla();   // Bu shaklning yuzasi: 25

$a = new Aylana(3);
$a->tasvirla();   // Bu shaklning yuzasi: 28.26

// $s = new Shakl();   // XATO! Abstrakt class'dan obyekt yaratib bo'lmaydi
```

Nima sodir bo'ldi:
- **`abstract class Shakl`** — bu "to'liq bo'lmagan" class. Undan to'g'ridan-to'g'ri obyekt (`new Shakl()`) yaratib bo'lmaydi.
- **`abstract public function yuza();`** — abstrakt metod. Faqat nomi bor, `{ }` ichi yo'q (oxirida `;` bilan tugaydi). Bu "qoida": "mendan meros oladigan har bir class `yuza()` metodini **albatta** yozishi kerak".
- `Kvadrat` va `Aylana` — `Shakl`dan meros oladi va `yuza()` ni **o'ziga moslab** to'ldiradi.
- `tasvirla()` — umumiy metod, ota class'da to'liq yozilgan, hamma bolalar uni meros oladi.

### Nega foydali?

Abstrakt class **majburlaydi**: "mendan meros olsang, `yuza()` ni yozishing shart". Agar bola class `yuza()` ni yozmasa — PHP xato beradi. Bu — "esdan chiqib qolishi"ning oldini oladi. Demak abstrakt class umumiy qoidalarni o'rnatadi va bola class'larni to'ldirilishga majbur qiladi.

> **Oddiy class va abstrakt class farqi:** oddiy class'dan obyekt yaratish mumkin va u to'liq. Abstrakt class — "yarim tayyor andoza", undan obyekt yaratib bo'lmaydi, u faqat meros olish uchun mavjud va bola class'larni biror metodni yozishga majbur qiladi.

### Mashqlar

**Oson**
1. `Shakl` abstrakt class'ini yarating (abstrakt `yuza()` metodi bilan). Undan obyekt yaratishga urinib ko'ring — xatoni ko'ring.
2. `Kvadrat` class'ini `Shakl`dan meros qildiring va `yuza()` ni to'ldiring.
3. `Aylana` class'ini ham yarating va `yuza()` ni to'ldiring.
4. Abstrakt class'ga oddiy (ichi bor) metod ham qo'shing va bola class'da ishlating.
5. `Hayvon` abstrakt class'i (abstrakt `ovoz()` bilan) → `It` va `Mushuk` uni to'ldirsin.

**O'rta**
6. `Shakl` abstrakt class'iga `tasvirla()` umumiy metodini qo'shing (yuzani chiqaradi). `Kvadrat`, `Aylana`, `Tortburchak` bola class'larini yarating.
7. `Tolov` abstrakt class'i (abstrakt `tasdiqla()` bilan) → `NaqdTolov`, `KartaTolov` har biri o'z tasdiqlashini yozsin.
8. `Xodim` abstrakt class'i (abstrakt `maoshHisobla()`, oddiy `malumot()`) → `Soatbay` va `Oylikli` xodimlar har xil maosh hisoblasin.
9. Bola class abstrakt metodni yozmasa nima bo'lishini sinab ko'ring (xatoni o'qing va tushuning).

**Qiyin**
10. To'liq shakllar tizimi: `Shakl` abstrakt (`yuza()`, `perimetr()` abstrakt; `hisobot()` umumiy — ikkalasini chiqaradi). `Kvadrat`, `Togriburchak`, `Aylana` bolalarini yarating. Bir nechta shakl yaratib, hisobotini chiqaring.
11. `Transport` abstrakt class'i (`tezlik()` abstrakt) → `Mashina`, `Velosiped`, `Samolyot` — har biri o'z taxminiy tezligini qaytarsin. Massiv ichida har xil transportni saqlab, hammasining tezligini `foreach` bilan chiqaring.

<details markdown="1">
<summary>Yechim — 8 (turli xodim turlari)</summary>

```php
<?php
abstract class Xodim {
    protected $ism;

    public function __construct($ism) {
        $this->ism = $ism;
    }

    // Har bir xodim turi maoshni o'zicha hisoblaydi:
    abstract public function maoshHisobla();

    // Umumiy metod:
    public function malumot() {
        echo $this->ism . " maoshi: " . $this->maoshHisobla() . " so'm";
    }
}

class Oylikli extends Xodim {
    private $oylik;

    public function __construct($ism, $oylik) {
        parent::__construct($ism);
        $this->oylik = $oylik;
    }

    public function maoshHisobla() {
        return $this->oylik;   // oddiy: belgilangan oylik
    }
}

class Soatbay extends Xodim {
    private $soatlar;
    private $stavka;

    public function __construct($ism, $soatlar, $stavka) {
        parent::__construct($ism);
        $this->soatlar = $soatlar;
        $this->stavka = $stavka;
    }

    public function maoshHisobla() {
        return $this->soatlar * $this->stavka;   // soat × stavka
    }
}

$a = new Oylikli("Ali", 6000000);
$a->malumot();   // Ali maoshi: 6000000 so'm

$v = new Soatbay("Vali", 160, 50000);
echo "<br>";
$v->malumot();   // Vali maoshi: 8000000 so'm
```
`malumot()` umumiy (ota class'da), lekin u `maoshHisobla()` ni chaqiradi — har bir bola class uni o'zicha hisoblaydi. Bu — abstrakt class'ning kuchi: umumiy mantiq bir joyda, o'ziga xos qism bolalarda.
</details>

<details markdown="1">
<summary>Yechim — 10 (to'liq shakllar tizimi)</summary>

```php
<?php
abstract class Shakl {
    abstract public function yuza();
    abstract public function perimetr();

    // Umumiy metod — ikkalasini chiqaradi:
    public function hisobot() {
        echo "Yuza: " . $this->yuza() . ", Perimetr: " . $this->perimetr() . "<br>";
    }
}

class Kvadrat extends Shakl {
    private $tomon;
    public function __construct($tomon) { $this->tomon = $tomon; }
    public function yuza()     { return $this->tomon * $this->tomon; }
    public function perimetr() { return $this->tomon * 4; }
}

class Togriburchak extends Shakl {
    private $eni;
    private $boyi;
    public function __construct($eni, $boyi) {
        $this->eni = $eni;
        $this->boyi = $boyi;
    }
    public function yuza()     { return $this->eni * $this->boyi; }
    public function perimetr() { return 2 * ($this->eni + $this->boyi); }
}

$shakllar = [new Kvadrat(5), new Togriburchak(4, 6)];
foreach ($shakllar as $shakl) {
    $shakl->hisobot();
}
// Yuza: 25, Perimetr: 20
// Yuza: 24, Perimetr: 20
```
`yuza()` va `perimetr()` abstrakt (har shakl o'zicha hisoblaydi), `hisobot()` esa umumiy — u ikkalasini chaqiradi. Bir massivda turli shakllarni saqlab, bittagina sikl bilan hammasining hisobotini chiqardik.
</details>

<details markdown="1">
<summary>Yechim — 11 (Transport tezligi)</summary>

```php
<?php
abstract class Transport {
    abstract public function tezlik();   // har transport o'zicha
}

class Mashina extends Transport {
    public function tezlik() { return 120; }
}
class Velosiped extends Transport {
    public function tezlik() { return 25; }
}
class Samolyot extends Transport {
    public function tezlik() { return 900; }
}

$transportlar = [new Mashina(), new Velosiped(), new Samolyot()];
foreach ($transportlar as $t) {
    echo get_class($t) . ": " . $t->tezlik() . " km/soat<br>";
}
// Mashina: 120 km/soat
// Velosiped: 25 km/soat
// Samolyot: 900 km/soat
```
`get_class($t)` obyektning class nomini qaytaradi. Abstrakt `Transport` "har bir transportda `tezlik()` bo'lishi shart" deb majburlaydi — har biri o'z qiymatini beradi.
</details>
