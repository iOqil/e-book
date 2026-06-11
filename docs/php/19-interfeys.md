# 2.6 Interfeys (interface)

[⬅️ Oldingi: 2.5 Abstrakt class'lar](./18-abstrakt-classlar.md) · [🏠 README](./README.md) · [Keyingi: 2.7 Static xususiyat va metodlar ➡️](./20-static-xususiyat-va-metodlar.md)

---

Interfeys — abstrakt class'ga o'xshash, lekin yanada "qat'iy" tushuncha. Keling, farqini tushunamiz.

### Interfeys — "shartnoma"

**Interfeys — bu shartnoma (ro'yxat):** "agar bu interfeysni qabul qilsang, ushbu metodlarni **albatta** yozishing kerak". Interfeys faqat metod **nomlari**ni belgilaydi — ichi (kodi) umuman bo'lmaydi. U "nima qilinishi kerakligini" aytadi, "qanday qilinishini" emas.

Buni elektr rozetkasiga o'xshatish mumkin: rozetka — "shartnoma". Unga ulanmoqchi bo'lgan har qanday qurilma (changyutgich, telefon zaryadlovchisi, choynak) bir xil vilka shakliga ega bo'lishi kerak. Qurilma ichida nima borligi muhim emas — faqat vilka mos kelsa, ulanadi.

```php
<?php
// Interfeys — "shartnoma". interface so'zi bilan, metodlar faqat nomlari bilan.
interface Tolov {
    public function tasdiqla($summa);
    public function bekorQil();
}

// "implements" — "men bu shartnomani bajaraman" degani
class NaqdTolov implements Tolov {
    public function tasdiqla($summa) {
        echo "Naqd to'lov tasdiqlandi: " . $summa . " so'm";
    }

    public function bekorQil() {
        echo "Naqd to'lov bekor qilindi";
    }
}

class KartaTolov implements Tolov {
    public function tasdiqla($summa) {
        echo "Kartadan yechildi: " . $summa . " so'm";
    }

    public function bekorQil() {
        echo "Kartaga qaytarildi";
    }
}

$t1 = new NaqdTolov();
$t1->tasdiqla(50000);   // Naqd to'lov tasdiqlandi: 50000 so'm

$t2 = new KartaTolov();
$t2->tasdiqla(50000);   // Kartadan yechildi: 50000 so'm
```

Tushuntiramiz:
- **`interface Tolov { ... }`** — interfeys e'lon qilinadi. Ichida metodlarning faqat nomlari bor (ichi yo'q, `;` bilan tugaydi).
- **`class NaqdTolov implements Tolov`** — "NaqdTolov class'i Tolov shartnomasini bajaradi". `implements` — "amalga oshiradi/bajaradi" degani.
- Shartnomani qabul qilgan class **barcha** metodlarni yozishi shart. Agar `bekorQil()` ni yozmasangiz — PHP xato beradi.

### Nega foydali? Almashtirib bo'ladigan qismlar

Interfeysning eng katta foydasi: bir xil shartnomaga ega obyektlarni **bir-biriga almashtirish** mumkin. Masalan, to'lov turini istalgan vaqtda o'zgartira olasiz, qolgan kod o'zgarmaydi:

```php
<?php
// Bu funksiya har qanday "Tolov" shartnomasini bajaradigan obyekt bilan ishlaydi
function tolovniBajar(Tolov $tolov, $summa) {
    $tolov->tasdiqla($summa);
}

tolovniBajar(new NaqdTolov(), 50000);   // Naqd to'lov tasdiqlandi: 50000 so'm
tolovniBajar(new KartaTolov(), 50000);  // Kartadan yechildi: 50000 so'm
```

`tolovniBajar` funksiyasi qanday to'lov ekanini bilmaydi — u faqat "Tolov shartnomasini bajaradigan biror narsa" kutadi. Naqd ham, karta ham bo'lishi mumkin. Ertaga "PaymeTolov" qo'shsangiz — bu funksiyani umuman o'zgartirmaysiz, faqat yangi class yozasiz. Bu — moslashuvchan, kengaytiriladigan kodning kaliti.

### Abstrakt class va interfeys farqi

Ikkalasi ham "majburlaydi", lekin farqlari bor:

| | Abstrakt class | Interfeys |
|---|---|---|
| Metod ichi (kod) | Ba'zilarida bo'lishi mumkin | Umuman bo'lmaydi (faqat nomlar) |
| Xususiyat | Bo'lishi mumkin | Bo'lmaydi |
| Nechtasini qabul qilish | Faqat bittadan meros | **Bir nechta** interfeysni qabul qilsa bo'ladi |
| Maqsad | Umumiy kod + qoidani birlashtirish | Faqat shartnoma (qoida) |

Oddiy qilib: **abstrakt class** "qisman tayyor andoza + qoidalar"; **interfeys** "faqat qoidalar ro'yxati". Bitta class bir nechta interfeysni bajarishi mumkin (`class X implements A, B`), lekin faqat bitta class'dan meros oladi.

Quyidagi diagramma bu farqni yonma-yon ko'rsatadi:

![Abstract class va interface farqi: tayyor kod va bittadan meros vs faqat nomlar va bir nechta interfeys](rasmlar/phb-abstrakt-vs-interfeys.svg)

> **Qachon qaysi biri?** Agar bola class'larga **umumiy tayyor kod** bermoqchi bo'lsangiz — abstrakt class. Agar faqat "shu metodlar bo'lsin" degan **qoida** o'rnatmoqchi bo'lsangiz — interfeys. Boshlanishida ko'p o'ylab o'tirmang; tajriba bilan qaysi biri qachon to'g'ri kelishini his qilasiz.

### Mashqlar

**Oson**
1. `Tolov` interfeysini yarating (`tasdiqla()`, `bekorQil()` bilan). `NaqdTolov` class'ida uni bajaring.
2. `KartaTolov` class'ini ham yarating va interfeysni bajaring.
3. Interfeys metodlaridan birini class'da yozishni unutib ko'ring — xatoni ko'ring.
4. `Ovoz` interfeysi (`chiqar()` bilan) → `It` va `Mushuk` uni bajarsin.
5. `Saqlanadigan` interfeysi (`saqla()` bilan) → `Fayl` class'ida bajaring.

**O'rta**
6. `Tolov` interfeysini bajaradigan obyektni parametr sifatida qabul qiluvchi funksiya yozing.
7. `Shakl` interfeysi (`yuza()`, `perimetr()`) → `Kvadrat`, `Aylana` uni bajarsin.
8. Ikki interfeysni bir class'da bajaring: `class Robot implements Yuruvchi, Gapiruvchi` (har birida bittadan metod).
9. `Bildirishnoma` interfeysi (`yubor($xabar)`) → `Email`, `SMS`, `Telegram` class'lari har biri o'z usulida yuborsin.

**Qiyin**
10. To'lov tizimi: `Tolov` interfeysi (`tasdiqla`, `bekorQil`). `NaqdTolov`, `KartaTolov`, `OnlaynTolov` class'lari. Bir massivga turli to'lovlarni solib, `foreach` bilan hammasini tasdiqlang.
11. `Bildirishnoma` interfeysini bajaradigan bir nechta class (`Email`, `SMS`) yarating. `hammaganYubor($kanallar, $xabar)` funksiyasi massivdagi har bir kanaldan xabar yuborsin — funksiya kanal turini bilmasin (faqat interfeysga tayansin).
12. `Saralanadigan` g'oyasini sinab ko'ring: `narx()` metodini talab qiladigan interfeys yarating, uni bir nechta mahsulot class'ida bajaring, keyin mahsulotlarni narxi bo'yicha solishtiruvchi oddiy kod yozing.

<details markdown="1">
<summary>Yechim — 10 (to'lov tizimi: turli to'lovlar bir massivda)</summary>

```php
<?php
interface Tolov {
    public function tasdiqla($summa);
}

class NaqdTolov implements Tolov {
    public function tasdiqla($summa) { echo "Naqd: $summa so'm<br>"; }
}
class KartaTolov implements Tolov {
    public function tasdiqla($summa) { echo "Karta: $summa so'm<br>"; }
}
class OnlaynTolov implements Tolov {
    public function tasdiqla($summa) { echo "Onlayn: $summa so'm<br>"; }
}

// Turli to'lovlar bir massivda — hammasi "Tolov" interfeysiga ega
$tolovlar = [new NaqdTolov(), new KartaTolov(), new OnlaynTolov()];
foreach ($tolovlar as $tolov) {
    $tolov->tasdiqla(1000);
}
// Naqd: 1000 so'm
// Karta: 1000 so'm
// Onlayn: 1000 so'm
```
`foreach` har bir to'lovning turini bilmaydi — faqat ularda `tasdiqla()` borligiga (interfeys kafolatlaydi) tayanadi. Yangi to'lov turi qo'shsangiz, bu sikl o'zgarmaydi. Bu — interfeyslarning kuchi.
</details>

<details markdown="1">
<summary>Yechim — 12 (narx interfeysi va solishtirish)</summary>

```php
<?php
interface Narxli {
    public function narx(): int;
}

class Kitob implements Narxli {
    private $narx;
    public function __construct($narx) { $this->narx = $narx; }
    public function narx(): int { return $this->narx; }
}

$mahsulotlar = [new Kitob(300), new Kitob(100), new Kitob(200)];

// Narx bo'yicha o'sish tartibida saralash (1.10'dagi usort):
usort($mahsulotlar, fn($a, $b) => $a->narx() <=> $b->narx());

foreach ($mahsulotlar as $m) {
    echo $m->narx() . "<br>";
}
// 100
// 200
// 300
```
`Narxli` interfeysi "narx() bo'lishi shart" deb kafolatlaydi — shuning uchun `usort` ichida xotirjam `$a->narx()` deymiz. Interfeys + 1.10'dagi `usort` birgalikda kuchli vosita.
</details>

<details markdown="1">
<summary>Yechim — 11 (universal bildirishnoma)</summary>

```php
<?php
interface Bildirishnoma {
    public function yubor($xabar);
}

class Email implements Bildirishnoma {
    public function yubor($xabar) {
        echo "Email yuborildi: " . $xabar . "<br>";
    }
}

class SMS implements Bildirishnoma {
    public function yubor($xabar) {
        echo "SMS yuborildi: " . $xabar . "<br>";
    }
}

// Bu funksiya kanal turini BILMAYDI — faqat "Bildirishnoma" ekanini biladi
function hammaganYubor($kanallar, $xabar) {
    foreach ($kanallar as $kanal) {
        $kanal->yubor($xabar);
    }
}

$kanallar = [new Email(), new SMS()];
hammaganYubor($kanallar, "Salom!");
// Email yuborildi: Salom!
// SMS yuborildi: Salom!
```
Diqqat: `hammaganYubor` faqat interfeysga (`yubor` metodi bor-yo'qligiga) tayanadi. Email, SMS, ertaga qo'shiladigan Telegram — hammasi ishlaydi, funksiyani o'zgartirmaymiz. Bu — interfeyslarning asosiy kuchi: "qism"larni almashtirsa bo'ladi.
</details>
