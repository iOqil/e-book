# 2.4 Meros (inheritance)

[⬅️ Oldingi: 2.3 Kirish darajalari: public va private](./16-kirish-darajalari-public-va-private.md) · [🏠 README](./README.md) · [Keyingi: 2.5 Abstrakt class'lar ➡️](./18-abstrakt-classlar.md)

---

### Muammo: takrorlanuvchi class'lar

Tasavvur qiling, sizda ikkita class bor: `It` va `Mushuk`. Ikkalasida ham `nom` xususiyati va `ovqatlan()` metodi bor — bir xil. Faqat ovoz chiqarishi farq qiladi (it huradi, mushuk miyovlaydi). Bir xil kodni ikki marta yozish — yomon (xato topilsa, ikki joyni tuzatasiz).

**Meros** ana shuni hal qiladi: umumiy narsalarni bitta "ota class"ga yozasiz, qolgan class'lar undan **meros olib**, faqat o'ziga xos qismni qo'shadi.

### Meros qanday ishlaydi

Bir nechta class uchun umumiy narsalarni **ota class** (parent) ga yozamiz. Boshqa class'lar undan `extends` so'zi bilan meros oladi:

```php
<?php
// Ota class — umumiy narsalar
class Hayvon {
    public $nom;

    public function __construct($nom) {
        $this->nom = $nom;
    }

    public function ovqatlan() {
        echo $this->nom . " ovqatlanyapti";
    }
}

// Bola class — Hayvondan meros oladi
class It extends Hayvon {
    public function ovoz() {
        echo $this->nom . ": Vov-vov!";
    }
}

class Mushuk extends Hayvon {
    public function ovoz() {
        echo $this->nom . ": Miyov!";
    }
}

$it = new It("Bobik");
$it->ovqatlan();   // Bobik ovqatlanyapti   ← Hayvondan meros olingan!
echo "<br>";
$it->ovoz();       // Bobik: Vov-vov!        ← It'ning o'ziniki

$mushuk = new Mushuk("Mosya");
$mushuk->ovqatlan(); // Mosya ovqatlanyapti  ← yana meros
$mushuk->ovoz();     // Mosya: Miyov!
```

Nima sodir bo'ldi:
- **`class It extends Hayvon`** — "It class'i Hayvon'dan meros oladi". `extends` — "kengaytiradi/meros oladi" degani.
- `It` o'zida `nom` va `ovqatlan()` ni yozmadi, lekin ularga **ega** — chunki `Hayvon`dan meros oldi.
- `It` faqat o'ziga xos `ovoz()` metodini qo'shdi.

Demak: **bola class ota class'dagi hamma narsaga ega bo'ladi, ustiga o'ziniki qo'shadi.** Umumiy kod bir joyda (ota class'da) — takrorlanish yo'q.

### Metodni qayta yozish (override)

Bola class ota class'dagi metodni "o'ziga moslab" qayta yozishi mumkin. Bu — **override** (qayta belgilash):

```php
<?php
class Hayvon {
    public $nom;

    public function __construct($nom) {
        $this->nom = $nom;
    }

    public function ovoz() {
        echo $this->nom . ": (umumiy ovoz)";
    }
}

class It extends Hayvon {
    // Hayvon'dagi ovoz() ni o'zgartiramiz (override)
    public function ovoz() {
        echo $this->nom . ": Vov-vov!";
    }
}

$it = new It("Bobik");
$it->ovoz();   // Bobik: Vov-vov!   ← bola class versiyasi ishladi
```

Bola class'da bir xil nomli metod yozsangiz, u ota class'nikini "ustini bosadi" — bola class obyektida bola versiyasi ishlaydi.

Quyidagi diagramma meros daraxtini ko'rsatadi: ota `Hayvon`dagi `$nom` va `ovqatlan()` bolalarga meros bo'ladi, har bir bola esa `ovoz()` ni o'ziga moslab override qiladi:

![Meros daraxti: ota class metod va xususiyatlari bolalarga o'tadi, ovoz() override qilinadi](rasmlar/phb-meros-daraxti.svg)

### `parent::` — ota class'ga murojaat

Ba'zan bola class ota class'ning metodini chaqirib, **ustiga** o'ziniki qo'shmoqchi bo'ladi. Buning uchun `parent::` ishlatiladi ("ota" degani):

```php
<?php
class Hayvon {
    public $nom;

    public function __construct($nom) {
        $this->nom = $nom;
    }
}

class It extends Hayvon {
    public $zot;

    public function __construct($nom, $zot) {
        parent::__construct($nom);   // ota class konstruktorini chaqiramiz
        $this->zot = $zot;           // keyin o'zimiznikini qo'shamiz
    }
}

$it = new It("Bobik", "Labrador");
echo $it->nom;   // Bobik   (ota class konstruktori to'ldirdi)
echo "<br>";
echo $it->zot;   // Labrador (bola class konstruktori to'ldirdi)
```

`parent::__construct($nom)` — "ota class'ning konstruktorini ishga tushir va `$nom`ni unga ber". Shunday qilib, ota class o'z ishini qiladi (nomni saqlaydi), bola class qolganini qo'shadi (zotni saqlaydi). Bu — takrorlamaslikning yaxshi usuli.

### Nega meros foydali?

1. **Takrorlanmaslik:** umumiy kod bir joyda.
2. **Tartib:** o'xshash narsalar bir "oila"ga birlashtiriladi (`Hayvon` → `It`, `Mushuk`).
3. **Kengaytirish:** yangi tur qo'shish oson — yangi bola class yozasiz, umumiy qismni qayta yozmaysiz.

> **Diqqat:** merosni haddan tashqari ishlatmang. U faqat haqiqiy "...bu ham bir turdagi..." munosabati bo'lganda mantiqiy: "It — bu bir Hayvon", "Yuk mashinasi — bu bir Mashina". Agar shunday munosabat bo'lmasa, meros o'rniga boshqa usul (masalan, oddiy xususiyat) to'g'riroq bo'ladi.

### Mashqlar

**Oson**
1. `Hayvon` (ota, `nom` bilan) va `It` (bola) class'larini yarating. It Hayvon'dan meros olsin.
2. `It`ga o'ziga xos `ovoz()` metodini qo'shing va ota class'dan kelgan `ovqatlan()` ni ham ishlating.
3. `Mushuk` class'ini ham `Hayvon`dan meros qildiring.
4. `Mashina` (ota) va `YukMashinasi` (bola) class'larini yarating.
5. `Foydalanuvchi` (ota) va `Admin` (bola) class'larini yarating.

**O'rta**
6. `Hayvon`dagi `ovoz()` ni `It`da override qiling (it uchun "Vov-vov").
7. `Shakl` (ota, `yuza()` umumiy) → `Kvadrat` va `Aylana` (bolalar, har biri o'z `yuza()` siga ega) — override bilan.
8. `Mashina` (ota, konstruktor `rang`) → `ElektrMashina` (bola, qo'shimcha `batareya`). `parent::__construct` ishlating.
9. `Xodim` (ota, `ism`, `maosh`) → `Menejer` (bola, qo'shimcha `bonus`). `parent::__construct` bilan.

**Qiyin**
10. `Hayvon` ota class: `nom`, `ovqatlan()`, `ovoz()` (umumiy). `It`, `Mushuk`, `Sigir` bolalar — har biri `ovoz()` ni override qilsin. Hammasini yaratib, ovozlarini chiqaring.
11. `Xodim` (ota, `maoshHisobla()` umumiy maosh qaytaradi) → `Menejer` (bola, `maoshHisobla()` ni override qilib, maosh + bonus qaytaradi; `parent::maoshHisobla()` dan foydalaning).
12. `Tolov` (ota, `summa`, `tasdiqla()`) → `NaqdTolov` va `KartaTolov` (bolalar, har biri `tasdiqla()` ni o'ziga xos qilib override qiladi).

<details markdown="1">
<summary>Yechim — 8 (parent::__construct)</summary>

```php
<?php
class Mashina {
    public $rang;

    public function __construct($rang) {
        $this->rang = $rang;
    }

    public function malumot() {
        echo "Rang: " . $this->rang;
    }
}

class ElektrMashina extends Mashina {
    public $batareya;

    public function __construct($rang, $batareya) {
        parent::__construct($rang);   // ota class rangni saqlaydi
        $this->batareya = $batareya;  // bola batareyani qo'shadi
    }

    public function malumot() {
        parent::malumot();            // ota class malumotini chiqaradi
        echo ", Batareya: " . $this->batareya . "%";  // ustiga qo'shadi
    }
}

$e = new ElektrMashina("oq", 80);
$e->malumot();   // Rang: oq, Batareya: 80%
```
Bu yerda `parent::` ni ikki joyda ishlatdik: konstruktorda (rangni saqlash) va `malumot`da (umumiy ma'lumotni chiqarish). Bola class faqat o'ziga xos qismni qo'shadi — qolgani ota class'da.
</details>

<details markdown="1">
<summary>Yechim — 10 (Hayvon va bolalari)</summary>

```php
<?php
class Hayvon {
    public $nom;

    public function __construct($nom) {
        $this->nom = $nom;
    }

    public function ovqatlan() {
        echo $this->nom . " ovqatlanyapti<br>";
    }

    public function ovoz() {
        echo "...";   // umumiy (bolalar override qiladi)
    }
}

class It extends Hayvon {
    public function ovoz() { echo "Vov-vov"; }
}
class Mushuk extends Hayvon {
    public function ovoz() { echo "Miyov"; }
}
class Sigir extends Hayvon {
    public function ovoz() { echo "Mooo"; }
}

$hayvonlar = [new It("Bobik"), new Mushuk("Pishi"), new Sigir("Zumrad")];
foreach ($hayvonlar as $h) {
    echo $h->nom . ": ";
    $h->ovoz();
    echo "<br>";
}
// Bobik: Vov-vov
// Pishi: Miyov
// Zumrad: Mooo
```
Har bir bola `ovoz()` ni o'zicha **override** qiladi (qayta yozadi). Bir massivda turli hayvonlarni saqlab, bittagina `foreach` bilan hammasini "gapirtirdik" — har biri o'z ovozini chiqaradi. Bu — polimorfizm: "bir buyruq, har xil natija".
</details>

<details markdown="1">
<summary>Yechim — 11 (maosh + bonus)</summary>

```php
<?php
class Xodim {
    protected $maosh;   // protected — pastda izoh

    public function __construct($maosh) {
        $this->maosh = $maosh;
    }

    public function maoshHisobla() {
        return $this->maosh;
    }
}

class Menejer extends Xodim {
    private $bonus;

    public function __construct($maosh, $bonus) {
        parent::__construct($maosh);
        $this->bonus = $bonus;
    }

    public function maoshHisobla() {
        return parent::maoshHisobla() + $this->bonus;   // asosiy maosh + bonus
    }
}

$x = new Xodim(5000000);
echo $x->maoshHisobla();      // 5000000

$m = new Menejer(5000000, 2000000);
echo "<br>" . $m->maoshHisobla();  // 7000000
```

> **Yangi so'z: `protected`.** Bu — `public` va `private` orasidagi uchinchi daraja. `private` faqat shu class ichida ishlaydi; `protected` esa shu class **va undan meros olgan bola class'lar** ichida ishlaydi (lekin tashqaridan emas). Bu yerda `$maosh` ni `protected` qildik, shunda `Menejer` (bola) unga murojaat qila olsin. Agar `private` bo'lsa, bola class undan foydalana olmasdi.
</details>

<details markdown="1">
<summary>Yechim — 12 (Tolov turlari)</summary>

```php
<?php
class Tolov {
    protected $summa;

    public function __construct($summa) {
        $this->summa = $summa;
    }

    public function tasdiqla() {
        echo "To'lov: " . $this->summa . " so'm";
    }
}

class NaqdTolov extends Tolov {
    public function tasdiqla() {
        echo "Naqd: " . $this->summa . " so'm qabul qilindi";
    }
}

class KartaTolov extends Tolov {
    public function tasdiqla() {
        echo "Karta: " . $this->summa . " so'm yechildi";
    }
}

(new NaqdTolov(5000))->tasdiqla();    // Naqd: 5000 so'm qabul qilindi
echo "<br>";
(new KartaTolov(12000))->tasdiqla();  // Karta: 12000 so'm yechildi
```
Ota `Tolov` `summa`ni saqlaydi va umumiy `tasdiqla()` beradi; har bir bola uni o'z usulida override qiladi. (Keyingi bo'limda — interfeys — bu g'oyani yanada qat'iyroq ko'rinishda ko'ramiz.)
</details>
