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

### Tiplangan parametrlar (zamonaviy uslub)

Yuqoridagi konstruktorda `$ism` va `$yosh`ga hech qanday "tip" ko'rsatmadik — ya'ni ularga istalgan narsa (matn, son, hatto massiv) berib yuborish mumkin edi. Zamonaviy PHP'da parametr oldidan uning **tipini** yozib qo'yamiz: `string`, `int`, `float`, `bool`, `array`. Bu — obyektga noto'g'ri ma'lumot kirib qolishining oldini oluvchi "qo'riqchi":

```php
<?php
class Talaba {
    public string $ism;   // xususiyat ham tiplangan
    public int $yosh;

    public function __construct(string $ism, int $yosh) {
        $this->ism = $ism;
        $this->yosh = $yosh;
    }
}

$t = new Talaba("Ali", 19);
echo $t->ism . " - " . $t->yosh;   // Ali - 19

// Endi noto'g'ri tip bersak, PHP darrov xato beradi:
$x = new Talaba("Vali", "o'n to'qqiz");   // ❌ yosh int bo'lishi kerak, string berildi → TypeError
```

`yosh` ga matn ("o'n to'qqiz") berishga urinsak — PHP `TypeError` chiqarib, dasturni shu yerda to'xtatadi. Bu yaxshi: xato keyinroq sirli ko'rinishda chiqib, soatlab qidirishdan ko'ra — aynan yaratilgan joyda, aniq xabar bilan chiqqani ming marta afzal. Tip — bu hujjat ham: kod o'qiyotgan odam `string $ism` deb ko'rib, bu yerda matn kelishini darrov tushunadi.

### Constructor property promotion — uzun yozuvni qisqartirish (PHP 8.0)

Yuqoridagi kodga diqqat qiling. Har bir xususiyat **uch marta** yozildi:
1. class boshida e'lon: `public string $ism;`
2. konstruktor parametri: `string $ism`
3. tayinlash: `$this->ism = $ism;`

Ikki-uchta xususiyatda bu chidasa bo'ladi, ammo 6-7 ta xususiyatli classda bu juda zerikarli takrordir. PHP 8.0 buni hal qildi: **constructor property promotion** ("konstruktorda xususiyatni ko'tarish"). G'oya oddiy — parametr oldiga `public`/`private`/`protected` so'zini qo'ysangiz, PHP **avtomatik** o'sha nomdagi xususiyat yaratadi va kelgan qiymatni unga saqlaydi. Uchta ish bitta yozuvga jamlanadi.

Quyida bir xil natija beradigan **eski** va **yangi** yozuvni yonma-yon ko'rsatamiz:

```php
<?php
// ESKI uslub (PHP 5/7) — uzun, takror
class TalabaEski {
    public string $ism;            // 1) e'lon
    public int $yosh;

    public function __construct(string $ism, int $yosh) {
        $this->ism = $ism;         // 3) tayinlash
        $this->yosh = $yosh;
    }
}

// YANGI uslub (PHP 8.0+) — qisqa, takrorsiz
class TalabaYangi {
    public function __construct(
        public string $ism,        // bitta yozuv = e'lon + parametr + tayinlash
        public int $yosh,
    ) {}                           // konstruktor tanasi bo'sh!
}

$a = new TalabaEski("Ali", 19);
$b = new TalabaYangi("Ali", 19);

echo $a->ism . " / " . $a->yosh;   // Ali / 19
echo "<br>";
echo $b->ism . " / " . $b->yosh;   // Ali / 19 — aynan bir xil natija
```

`TalabaYangi` ichida `public string $ism` deb yozdik — bu bitta qatorda:
- xususiyatni e'lon qiladi,
- konstruktor parametri bo'ladi,
- kelgan qiymatni o'sha xususiyatga saqlaydi.

Konstruktor tanasi (`{}`) bo'm-bo'sh qoldi, chunki `$this->ism = $ism` kabi qatorlar endi kerak emas — PHP ularni o'zi bajaradi. Natija aynan bir xil, lekin yozuv qariyb yarmiga qisqardi. Bu — bugungi PHP'da konstruktor yozishning **standart, tavsiya etilgan** usuli.

> **Vergulga e'tibor bering.** Promotion'da parametrlarni odatda har birini alohida qatorga yozamiz va oxiriga vergul (`,`) qo'yamiz — hatto oxirgisiga ham (buni "trailing comma" deyiladi, PHP 8.0'dan ruxsat). Bu keyinroq yangi parametr qo'shishni osonlashtiradi va `git`da o'zgarish tozaroq ko'rinadi.

### Default qiymat va nullable promotion bilan

Promotion'da ham 1.9'dagi **standart qiymat** (`= "..."`) va matn yoki son "bo'lmasligi mumkin" degan **nullable** tip (`?string`) bemalol ishlaydi. `?string` — "string yoki `null`" degani; ya'ni bu xususiyat to'ldirilmasligi ham mumkin:

```php
<?php
class Foydalanuvchi {
    public function __construct(
        public string $ism,
        public ?string $telefon = null,   // nullable: bo'lmasligi mumkin
        public int $yosh = 0,             // tiplangan + standart qiymat
    ) {}
}

$u1 = new Foydalanuvchi("Ali", "+998901234567", 25);
$u2 = new Foydalanuvchi("Vali");          // telefon va yosh berilmadi

echo $u1->ism . " - " . $u1->telefon . " - " . $u1->yosh;
echo "<br>";
echo $u2->ism . " - " . ($u2->telefon ?? "telefon yo'q") . " - " . $u2->yosh;
```

Natija:

```
Ali - +998901234567 - 25
Vali - telefon yo'q - 0
```

`$u2`da `telefon` berilmadi — u `null` bo'lib qoldi, `?string` shunga ruxsat berdi. `?? "telefon yo'q"` esa "agar `null` bo'lsa, o'rniga shu matnni ko'rsat" degani (1.x'da o'rgangan null-coalescing operatori). `yosh` ham berilmadi — standart `0` ni oldi.

> **Qachon `?` (nullable), qachon default?** Ular har xil narsa: `= 0` — "berilmasa, o'rniga 0 ishlat"; `?int` — "qiymat `null` bo'lishi ham mumkin". Ko'pincha ikkalasi birga ishlatiladi: `public ?string $telefon = null` — "telefon ixtiyoriy, berilmasa null bo'lib qoladi".

### Named arguments — parametrlarni nomi bilan berish (PHP 8.0)

Parametrlar ko'payganda yana bir muammo chiqadi. Mana shunga qarang:

```php
$u = new Foydalanuvchi("Ali", null, 25);
```

Bu yerda `null` nima? `25` qaysi parametr? Kodni o'qiyotgan odam class e'loniga qaytib qarashga majbur. PHP 8.0'dagi **named arguments** ("nomlangan argumentlar") buni hal qiladi — har bir qiymatni **qaysi parametrga** tegishliligini nomi bilan ko'rsatamiz, `nom: qiymat` shaklida:

```php
<?php
class Foydalanuvchi {
    public function __construct(
        public string $ism,
        public int $yosh = 0,
        public string $shahar = "Toshkent",
    ) {}
}

// Qaysi qiymat qaysi parametr ekani — o'qishda darrov ravshan:
$u = new Foydalanuvchi(ism: "Ali", yosh: 25);
echo $u->ism . ", " . $u->yosh . ", " . $u->shahar;   // Ali, 25, Toshkent

echo "<br>";

// Named arguments bilan tartibni ham o'zgartirsa bo'ladi:
$u2 = new Foydalanuvchi(shahar: "Samarqand", ism: "Vali");
echo $u2->ism . ", " . $u2->yosh . ", " . $u2->shahar;   // Vali, 0, Samarqand
```

Named arguments'ning ikki katta foydasi:
1. **O'qiluvchanlik:** `new Foydalanuvchi(ism: "Ali", yosh: 25)` o'zini o'zi tushuntiradi — izoh shart emas.
2. **O'rtadagi parametrni o'tkazib yuborish:** standart qiymatli parametrlar ko'p bo'lsa, faqat kerakligini berib, qolganini standart qiymatda qoldirish mumkin. Yuqorida `yosh`ni berib, `shahar`ni teginmadik — u o'zining standart "Toshkent" qiymatida qoldi. Tartibni ham o'zgartirdik: `shahar`ni `ism`dan oldin yozdik, PHP nomi bo'yicha to'g'ri joyiga qo'ydi.

> **Eslatma:** named arguments faqat konstruktorga emas — har qanday funksiya/metodga ishlaydi. Lekin u eng ko'p aynan ko'p parametrli konstruktorlarda asqotadi.

### Readonly promotion — o'zgarmas xususiyat (PHP 8.1)

Ba'zi ma'lumotlar obyekt **yaratilgandan keyin hech qachon o'zgarmasligi** kerak. Masalan: hujjat raqami, tug'ilgan sana, buyurtma ID'si. Bularni xato bilan o'zgartirib qo'yish — jiddiy nuqson. PHP 8.1 buning uchun `readonly` ("faqat o'qish uchun") so'zini qo'shdi. Promotion bilan birga ishlatish juda qulay:

```php
<?php
class Hujjat {
    public function __construct(
        public readonly string $raqam,   // yaratilgandan keyin o'zgarmaydi
        public readonly string $sana,
    ) {}
}

$h = new Hujjat("A-2026-001", "2026-06-11");
echo $h->raqam . " (" . $h->sana . ")";   // A-2026-001 (2026-06-11)

// O'qish mumkin, ammo o'zgartirib bo'lmaydi:
$h->raqam = "B-999";   // ❌ Error: Cannot modify readonly property Hujjat::$raqam
```

`readonly` xususiyatga faqat **bir marta**, konstruktor ichida (promotion orqali) qiymat beriladi. Undan keyin uni o'zgartirishga urinish — `Error` bilan to'xtaydi. Bu sizning kodingizni xavfsizroq qiladi: "bu qiymat o'rnatilgandan keyin teginilmaydi" degan kafolatni PHP'ning o'zi ta'minlaydi.

> **Promotion bilan uyg'unligi.** Eski uslubda `readonly` ishlatish uchun xususiyatni alohida e'lon qilib, konstruktorda qo'lda tayinlash kerak edi. Promotion bilan esa hammasi bir qatorda: `public readonly string $raqam` — e'lon, tayinlash va o'zgarmaslik kafolati — birgalikda.

### Promotion va oddiy xususiyat aralash

Hamma xususiyat ham parametrdan kelmasligi mumkin — ba'zilari konstruktor **ichida** hisoblanadi yoki standart qiymat oladi. Bunday holatda promotion qilinadigan parametrlarni konstruktor sarlavhasiga, qolganini esa class boshida (oddiy usulda) yozamiz:

```php
<?php
class Hisob {
    public int $balans = 0;          // promotion EMAS — har doim 0 dan boshlanadi
    public string $ochilganSana;     // promotion EMAS — ichkarida hisoblanadi

    public function __construct(
        public string $egasi,        // promotion — bu parametrdan keladi
    ) {
        $this->ochilganSana = date("Y-m-d");   // konstruktor ichidagi tayyorgarlik
    }
}

$h = new Hisob("Ali");
echo $h->egasi;          // Ali
echo "<br>";
echo $h->balans;         // 0
echo "<br>";
echo $h->ochilganSana;   // bugungi sana, masalan 2026-06-11
```

Demak, promotion "hammasi yoki hech narsa" emas — kerakli parametrlarni ko'tarib, qolgan tayyorgarlikni konstruktor tanasida bemalol davom ettirasiz. Bu naqsh juda ko'p uchraydi: ID egadan keladi (promotion), ammo sana, status, bo'sh ro'yxat kabilar ichkarida o'rnatiladi.

### Konstruktorda boshlang'ich amal ham bajarish mumkin

Konstruktor faqat qiymat saqlash bilan cheklanmaydi — obyekt yaratilganda kerakli har qanday tayyorgarlikni qilishi mumkin. Quyida xususiyatni **promotion** bilan oldik, `balans`ni esa ichkarida 0 ga o'rnatdik:

```php
<?php
class Hisob {
    public int $balans = 0;   // har bir yangi hisob 0 balans bilan ochiladi

    public function __construct(
        public string $egasi,
    ) {}
}

$h = new Hisob("Ali");
echo $h->egasi;    // Ali
echo "<br>";
echo $h->balans;   // 0
```

(Avval bu kodda `$egasi` ham, `$balans` ham alohida e'lon qilinib, konstruktorda qo'lda tayinlanardi. Promotion bilan `$egasi` bitta qatorga jamlandi, `$balans` esa parametrdan kelmagani uchun oddiy xususiyat sifatida `= 0` standart qiymat bilan qoldi.)

### Standart qiymatli parametr (konstruktorda ham)

1.9'dagi standart qiymat konstruktorda ham ishlaydi. Quyida promotion bilan, tiplangan ko'rinishda:

```php
<?php
class Talaba {
    public function __construct(
        public string $ism,
        public string $shahar = "Toshkent",
    ) {}
}

$t1 = new Talaba("Ali");             // shahar berilmadi → "Toshkent"
$t2 = new Talaba("Vali", "Samarqand");

echo $t1->shahar;   // Toshkent
echo "<br>";
echo $t2->shahar;   // Samarqand
```

`public string $shahar = "Toshkent"` — promotion, tip va standart qiymat bir qatorda. Berilmasa "Toshkent", berilsa kelgan qiymat. Xohlasangiz `new Talaba(ism: "Ali")` deb named argument bilan ham chaqirishingiz mumkin.

### Mashqlar

**Oson**
1. `Talaba` classiga konstruktor qo'shing (`ism`, `yosh`). Obyektni bir qatorda yarating.
2. `Mashina` classiga konstruktor qo'shing (`rang`, `tezlik`) va obyekt yarating.
3. `Mahsulot` classi: konstruktor `nom` va `narx` olsin. Obyekt yaratib, ma'lumotini chiqaring.
4. `Kitob` classi: konstruktor `nom`, `muallif`, `yil` olsin.
5. `Hisob` classi: konstruktor `egasi` olsin, `balans` esa konstruktor ichida 0 ga o'rnatilsin.
6. (Yangi) `Talaba` classini **constructor property promotion** bilan qaytadan yozing: `public function __construct(public string $ism, public int $yosh) {}`. Eski (uzun) yozuv bilan solishtiring — natija bir xil ekanini ko'ring.
7. (Yangi) `Mahsulot` classini **tiplangan** promotion bilan yozing (`public string $nom, public float $narx`). So'ng `new Mahsulot(nom: "Non", narx: 4000)` deb **named arguments** bilan obyekt yarating.

**O'rta**
8. `Talaba` classiga konstruktor (`ism`, `ball`) va `otdimi()` metodini qo'shing (ball 60+ bo'lsa "O'tdi").
9. `Aylana` classi: konstruktor `radius` olsin, `yuza()` metodi yuzani qaytarsin.
10. `Mahsulot` classiga standart qiymatli parametr qo'shing: `valyuta = "so'm"`.
11. `Foydalanuvchi` classi: konstruktor `ism`, `email` olsin, `parol` esa standart qiymatga ega bo'lsin.
12. `Tortburchak` classi: konstruktor `eni`, `boyi` olsin; `yuza()` va `perimetr()` metodlari bo'lsin.
13. (Yangi) `Foydalanuvchi` classini promotion bilan yozing: `ism`, `email` (majburiy), `rol = "user"` va `faol = true` (standart qiymatli). So'ng faqat `ism`, `email` va `rol`ni **named arguments** bilan berib, admin yarating.

**Qiyin**
14. `Hisob` classi: konstruktor `egasi` va ixtiyoriy `boshlangichBalans` (standart 0) olsin. `pulQoshish`, `pulYechish`, `korsat` metodlari bo'lsin.
15. `Talaba` classi: konstruktor `ism` va bir nechta `ball`larni massiv sifatida olsin; `ortacha()` metodi o'rtacha ballni hisoblab qaytarsin.
16. `Mashina` classi: konstruktor `rang` olsin, `tezlik` 0 dan boshlansin; `tezlash()` har chaqirilganda tezlikni 10 ga oshirsin, `tormoz()` 10 ga kamaytirsin (lekin 0 dan past bo'lmasin).
17. (Yangi) `Nuqta` classi: konstruktor `x` va `y` koordinatalarini **`readonly` promotion** bilan olsin (yaratilgandan keyin o'zgarmasin). `masofa(Nuqta $boshqa)` metodi ikki nuqta orasidagi masofani qaytarsin. So'ng `$nuqta->x = 10` deb o'zgartirishga urinib, xatoni ko'ring.

<details markdown="1">
<summary>Yechim — 6 (constructor property promotion)</summary>

```php
<?php
// ESKI (uzun) yozuv
class TalabaEski {
    public string $ism;
    public int $yosh;

    public function __construct(string $ism, int $yosh) {
        $this->ism = $ism;
        $this->yosh = $yosh;
    }
}

// YANGI (promotion) yozuv — bir xil natija
class Talaba {
    public function __construct(
        public string $ism,
        public int $yosh,
    ) {}
}

$t = new Talaba("Ali", 19);
echo $t->ism . " / " . $t->yosh;   // Ali / 19
```
`public string $ism` bitta qatorda xususiyatni e'lon qiladi, parametr qiladi va qiymatini saqlaydi. Konstruktor tanasi bo'sh qoladi — `$this->ism = $ism` kabi qatorlar endi kerak emas. Natija eski yozuv bilan aynan bir xil.
</details>

<details markdown="1">
<summary>Yechim — 7 (tiplangan promotion + named arguments)</summary>

```php
<?php
class Mahsulot {
    public function __construct(
        public string $nom,
        public float $narx,
    ) {}

    public function korsat(): string {
        return $this->nom . " — " . $this->narx . " so'm";
    }
}

// Named arguments: qaysi qiymat qaysi parametr ekani ravshan
$m = new Mahsulot(nom: "Non", narx: 4000);
echo $m->korsat();   // Non — 4000 so'm
```
`public string $nom, public float $narx` — promotion bilan ikki xususiyat ham tiplangan holda bir qatordan e'lon qilindi. `new Mahsulot(nom: "Non", narx: 4000)` esa named arguments: kod o'qiganda qaysi qiymat narx, qaysisi nom ekani izohsiz tushunarli.
</details>

<details markdown="1">
<summary>Yechim — 9</summary>

```php
<?php
class Aylana {
    public function __construct(
        public float $radius,
    ) {}

    public function yuza(): float {
        return 3.14 * $this->radius * $this->radius;
    }
}

$a = new Aylana(5);
echo "Yuza: " . $a->yuza();   // Yuza: 78.5
```
Konstruktor radiusni promotion bilan saqlaydi (bitta qatorda e'lon + tayinlash), `yuza()` metodi esa `$this->radius` orqali o'sha radiusdan yuzani hisoblaydi.
</details>

<details markdown="1">
<summary>Yechim — 13 (Foydalanuvchi: promotion + standart qiymat + named arguments)</summary>

```php
<?php
class Foydalanuvchi {
    public function __construct(
        public string $ism,
        public string $email,
        public string $rol = "user",   // standart qiymat
        public bool $faol = true,
    ) {}
}

// Faqat kerakli parametrlarni nomi bilan beramiz, faol — standart (true)
$admin = new Foydalanuvchi(
    ism: "Oqil",
    email: "oqil@example.com",
    rol: "admin",
);
echo "{$admin->ism} ({$admin->rol}) - faol: " . ($admin->faol ? "ha" : "yo'q");
// Oqil (admin) - faol: ha
```
`rol` va `faol` standart qiymatli. Named arguments tufayli `faol`ni teginmasdan (u standart `true` qoldi) faqat kerakli uchta qiymatni berdik. Bu — ko'p parametrli konstruktorlarda eng qulay chaqirish usuli.
</details>

<details markdown="1">
<summary>Yechim — 14 (Hisob: ixtiyoriy boshlang'ich balans)</summary>

```php
<?php
class Hisob {
    public function __construct(
        public string $egasi,
        public int $balans = 0,   // berilmasa — 0
    ) {}

    public function pulQoshish(int $summa): void {
        $this->balans += $summa;
    }

    public function pulYechish(int $summa): void {
        if ($summa <= $this->balans) {
            $this->balans -= $summa;
        }
    }

    public function korsat(): string {
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
`public int $balans = 0` — promotion, tip va standart qiymat bir qatorda. Berilsa o'shani, berilmasa 0 ni oladi. Shu tufayli `new Hisob("Ali", 100000)` ham, `new Hisob("Vali")` ham ishlaydi. Metodlarning qaytish tipi ham yozildi: `: void` (hech narsa qaytarmaydi), `: string` (matn qaytaradi).
</details>

<details markdown="1">
<summary>Yechim — 15 (o'rtacha ball)</summary>

```php
<?php
class Talaba {
    public function __construct(
        public string $ism,
        public array $ballar,   // bu — massiv
    ) {}

    public function ortacha(): float {
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
Bu yerda xususiyat **massiv** (`array`) bo'lishi mumkinligini ko'ramiz — promotion'da tip sifatida `array` yozildi. `ortacha()` metodi 1.8'da o'rgangan "massiv yig'indisi" mantig'ini class ichida ishlatadi.
</details>

<details markdown="1">
<summary>Yechim — 16 (Mashina: tezlash va tormoz)</summary>

```php
<?php
class Mashina {
    public int $tezlik = 0;   // promotion EMAS — har doim 0 dan boshlanadi

    public function __construct(
        public string $rang,
    ) {}

    public function tezlash(): void {
        $this->tezlik += 10;
    }

    public function tormoz(): void {
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
`rang` parametrdan keladi — uni promotion bilan oldik. `tezlik` esa parametrdan emas, har doim 0 dan boshlanadi — shuning uchun uni promotion qilmasdan, oddiy xususiyat sifatida `= 0` standart qiymat bilan e'lon qildik. `tormoz()` da `if ($this->tezlik < 0)` tekshiruvi tezlikning manfiy bo'lib ketishini oldini oladi. (Buni `$this->tezlik = max(0, $this->tezlik - 10);` deb bitta qatorda ham yozsa bo'ladi.)
</details>

<details markdown="1">
<summary>Yechim — 17 (Nuqta: readonly promotion)</summary>

```php
<?php
class Nuqta {
    public function __construct(
        public readonly int $x,   // yaratilgandan keyin o'zgarmaydi
        public readonly int $y,
    ) {}

    public function masofa(Nuqta $boshqa): float {
        $dx = $this->x - $boshqa->x;
        $dy = $this->y - $boshqa->y;
        return sqrt($dx * $dx + $dy * $dy);
    }
}

$a = new Nuqta(0, 0);
$b = new Nuqta(3, 4);
echo "Masofa: " . $a->masofa($b);   // Masofa: 5

// O'zgartirishga urinsak — xato:
$a->x = 10;   // ❌ Error: Cannot modify readonly property Nuqta::$x
```
`public readonly int $x` — promotion va `readonly` birga. `x` va `y` faqat konstruktorda bir marta o'rnatiladi, keyin o'zgarmaydi. Bu mantiqan to'g'ri: nuqtaning koordinatasi o'zgarsa, u boshqa nuqta bo'lib qoladi. `masofa()` metodi parametr sifatida boshqa `Nuqta` obyektini oladi (`Nuqta $boshqa`) va ikkisi orasidagi masofani Pifagor teoremasi bilan hisoblaydi. `$a->x = 10` esa `Error` chiqaradi — `readonly` o'zgartirishga yo'l qo'ymaydi.
</details>
