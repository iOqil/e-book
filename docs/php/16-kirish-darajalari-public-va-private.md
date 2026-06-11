# 2.3 Kirish darajalari: public va private

[⬅️ Oldingi: 2.2 Konstruktor](./15-konstruktor.md) · [🏠 README](./README.md) · [Keyingi: 2.4 Meros (inheritance) ➡️](./17-meros.md)

---

Hozirgacha har bir xususiyat va metod oldiga `public` yozdik, lekin nima ekanini tushuntirmadik. Endi vaqti keldi.

### Muammo: hamma narsani tashqaridan o'zgartirish mumkin

`public` xususiyatni tashqaridan **istalgancha** o'zgartirish mumkin. Bu ba'zan xavfli. Bank hisobi misolini ko'raylik:

```php
<?php
class Hisob {
    public $balans = 0;
}

$h = new Hisob();
$h->balans = -50000;   // muammo! Balansni to'g'ridan-to'g'ri manfiy qildik
```

Bu noto'g'ri — bank hisobida balans manfiy bo'lmasligi kerak (yoki faqat ma'lum qoidalar bilan). Lekin `public` bo'lgani uchun, hech qanday tekshiruvsiz, istalgan qiymat berildi. Demak, ma'lumotni **himoyalash** kerak.

### Yechim: `private` — "faqat ichkaridan"

PHP'da xususiyat va metodlarga **kirish darajasi** belgilash mumkin:

- **`public`** — "ochiq". Tashqaridan ham, ichkaridan ham murojaat qilish mumkin.
- **`private`** — "yopiq". Faqat **shu class ichidan** murojaat qilish mumkin. Tashqaridan — mumkin emas.

```php
<?php
class Hisob {
    private $balans = 0;   // endi yopiq

    public function pulQoshish($summa) {
        if ($summa > 0) {              // tekshiruv!
            $this->balans += $summa;
        }
    }

    public function balansniKorish() {
        return $this->balans;
    }
}

$h = new Hisob();
$h->pulQoshish(100000);        // to'g'ri yo'l — metod orqali
echo $h->balansniKorish();     // 100000

// $h->balans = -50000;        // XATO! balans private, tashqaridan tegib bo'lmaydi
```

Endi `balans`ga tashqaridan **to'g'ridan-to'g'ri** tegib bo'lmaydi. Uni o'zgartirishning yagona yo'li — `pulQoshish` metodi orqali, u esa **tekshiruv** qiladi (manfiy summani qabul qilmaydi). Bu — ma'lumotni himoyalash.

### Bu g'oya: "inkapsulyatsiya" (encapsulation)

Bu yondashuvning nomi bor — **inkapsulyatsiya**. Ma'nosi: ma'lumotni (xususiyatni) yopib, unga faqat nazorat ostidagi metodlar orqali ruxsat berish.

Buni dori qutisiga o'xshatish mumkin: dorini to'g'ridan-to'g'ri olib bo'lmaydi, "bolalarga qarshi" qopqoq bor — uni faqat to'g'ri usulda ochasiz. Yoki bankomat: pulga to'g'ridan-to'g'ri qo'l yetkazmaysiz, faqat tugmalar (metodlar) orqali olasiz, ular esa qoidalarni tekshiradi (balans yetarlimi va h.k.).

### Getter va setter — o'qish va yozish metodlari

Yopiq xususiyatni o'qish va yozish uchun maxsus metodlar yoziladi. Ularni odatda **getter** (o'qish) va **setter** (yozish) deb atashadi:

```php
<?php
class Talaba {
    private $ism;

    public function __construct($ism) {
        $this->ism = $ism;
    }

    // getter — qiymatni o'qish
    public function getIsm() {
        return $this->ism;
    }

    // setter — qiymatni o'zgartirish (tekshiruv bilan)
    public function setIsm($yangiIsm) {
        if (strlen($yangiIsm) > 0) {     // bo'sh ism qabul qilinmaydi
            $this->ism = $yangiIsm;
        }
    }
}

$t = new Talaba("Ali");
echo $t->getIsm();        // Ali  (o'qidik)
$t->setIsm("Vali");       // o'zgartirdik
echo $t->getIsm();        // Vali
```

Getter/setter orqali siz **nazoratni** qo'lda ushlaysiz: setter ichida tekshiruv qo'yib, noto'g'ri qiymatni rad eta olasiz.

> **Qachon `public`, qachon `private`?** Umumiy qoida: **xususiyatlarni `private` qiling**, ularga metodlar (`public`) orqali ruxsat bering. Bu ma'lumotni himoyalaydi va keyinroq qoidalarni o'zgartirishni osonlashtiradi. Metodlarning ko'pi `public` bo'ladi (chunki ular class "interfeysi" — tashqaridan ishlatiladi), lekin faqat ichki yordamchi metodlarni `private` qilish mumkin.

### Tiplangan xususiyatlar (typed properties) — zamonaviy uslub

Yuqoridagi misollarda xususiyatlarni shunchaki `private $balans` deb e'lon qildik — bu yerda xususiyat **qanday tipdagi** ma'lumot saqlashi ko'rsatilmagan. Eski PHP (5/7) da boshqa imkon yo'q edi, lekin **PHP 7.4 dan boshlab** xususiyat oldiga uning **tipini** yozish mumkin — xuddi metod parametrlaridagidek (`int`, `string`, `float`, `bool`...). Buni **tiplangan xususiyat** (typed property) deyiladi.

```php
<?php
class Hisob {
    private int $balans = 0;   // tip: faqat butun son saqlanadi

    public function pulQoshish(int $summa): void {
        if ($summa > 0) {
            $this->balans += $summa;
        }
    }

    public function balansniKorish(): int {
        return $this->balans;
    }
}

$h = new Hisob();
$h->pulQoshish(100000);
echo $h->balansniKorish();     // 100000
```

E'tibor bering: `private int $balans` — endi `balans` faqat butun son (`int`) bo'lishi mumkin. Agar kimdir unga matn yoki kasr son tiqishga harakat qilsa, PHP **darrov xato** beradi — ma'lumot buzilib ulgurmaydi. Metod imzosida ham `pulQoshish(int $summa)` (kiruvchi tip) va `: int` / `: void` (qaytuvchi tip) yozildi.

Nima uchun bu yaxshi?

- **Xato erta topiladi.** `balans`ga noto'g'ri turdagi qiymat tushsa, dastur o'sha joyda to'xtaydi — keyinroq sirli xatoni qidirib yurmaysiz.
- **Kod o'zini o'zi hujjatlaydi.** `private int $balans` deganda, har kim bu xususiyat son ekanini darrov ko'radi. Izoh yozish shart emas.
- **Tahrirlagich (IDE) yordam beradi.** Tip ma'lum bo'lgani uchun, muharrir avtomatik to'ldirish va ogohlantirishlarni aniqroq beradi.

Shu sababli **bundan keyin xususiyatlarni doim tiplab yozamiz**. Yuqoridagi `Talaba`ni ham shu uslubga keltiraylik:

```php
<?php
class Talaba {
    private string $ism;     // tiplangan: faqat matn

    public function __construct(string $ism) {
        $this->ism = $ism;
    }

    public function getIsm(): string {
        return $this->ism;
    }

    public function setIsm(string $yangiIsm): void {
        if (strlen($yangiIsm) > 0) {
            $this->ism = $yangiIsm;
        }
    }
}

$t = new Talaba("Ali");
echo $t->getIsm();        // Ali
$t->setIsm("Vali");
echo $t->getIsm();        // Vali
```

> **Diqqat — boshlang'ich qiymatsiz tiplangan xususiyat.** `private string $ism;` deb e'lon qilib, unga hech qachon qiymat bermasangiz (na e'londa, na konstruktorda), uni o'qishga urinish xato beradi: "Typed property must not be accessed before initialization". Bu aslida **foydali** — "to'ldirilmagan" xususiyatni tasodifan o'qishdan saqlaydi. Shuning uchun tiplangan xususiyatlarni odatda konstruktorda to'ldiramiz.

### `readonly` — "faqat bir marta yoziladi" xususiyat

Ba'zan xususiyat shunday bo'lishi kerakki: u obyekt yaratilganda **bir marta** o'rnatiladi, keyin **hech qachon o'zgarmaydi**. Masalan: pasport raqami, tug'ilgan sana, buyurtma ID'si — bular yaratilgach o'zgarmasligi kerak.

Buni `private` + getter (setter'siz) bilan ham qilsa bo'ladi, lekin **PHP 8.1 dan boshlab** maxsus va aniqroq yo'l bor — `readonly` ("faqat o'qish") xususiyati:

```php
<?php
class Pasport {
    public readonly string $raqam;

    public function __construct(string $raqam) {
        $this->raqam = $raqam;   // faqat shu yerda — konstruktorda o'rnatiladi
    }
}

$p = new Pasport("AA1234567");
echo $p->raqam;        // AA1234567 — o'qish bemalol

// $p->raqam = "BB7654321";   // ❌ Xato! readonly — o'rnatilgach o'zgartirib bo'lmaydi
```

Agar oxirgi qatordagi izohni ochsangiz, PHP shunday xato beradi:

```
Fatal error: Cannot modify readonly property Pasport::$raqam
```

`readonly`ning ajoyib tomoni: xususiyat `public` bo'lsa ham, uni **tashqaridan o'qish** mumkin (getter yozish shart emas), lekin **o'zgartirib bo'lmaydi**. Ya'ni siz "ochiq o'qish, yopiq yozish" effektiga erishasiz — getter/setterning yarmini bepul olasiz.

Qoidalar oddiy:

- `readonly` xususiyatga qiymat **faqat class ichidan** (odatda konstruktorda) **bir marta** beriladi.
- Bir marta o'rnatilgach, na tashqaridan, na ichkaridan o'zgartirib bo'lmaydi.
- `readonly` xususiyatga albatta **tip** kerak (`public readonly string $raqam` — tipsiz bo'lmaydi).

Bu yondashuvni **o'zgarmas (immutable)** obyekt deyiladi: yaratilgach, ichi qotib qoladi. Bunaqa obyektlar xavfsizroq — uni dasturning bir qismiga uzatsangiz, hech kim sizdan bexabar ichini o'zgartira olmaydi.

### `readonly` + promotion birga — DTO uchun ideal

[Konstruktor bobida](./15-konstruktor.md) xususiyatni qo'lda `$this->ism = $ism;` deb to'ldirardik. PHP 8.0 da bu ishni qisqartiruvchi qulaylik bor — **konstruktor promotion** (ko'tarish): xususiyatni alohida e'lon qilib, keyin to'ldirish o'rniga, konstruktor parametrining oldiga `public`/`private`/`readonly` yozsangiz — PHP o'zi xususiyat yaratadi va to'ldiradi.

`readonly` aynan shu yerda juda qulay tushadi:

```php
<?php
class Nuqta {
    public function __construct(
        public readonly int $x,
        public readonly int $y,
    ) {}   // tana bo'sh — PHP o'zi $this->x = $x, $this->y = $y qiladi
}

$n = new Nuqta(3, 5);
echo "x = {$n->x}, y = {$n->y}";   // x = 3, y = 5

// $n->x = 10;   // ❌ readonly — o'zgartirib bo'lmaydi
```

Solishtiring — promotion'siz aynan shu class **uch baravar uzun** bo'lardi (xususiyat e'loni + parametr + qo'lda to'ldirish). Promotion + `readonly` bilan esa hammasi bitta joyda, qisqa va aniq.

Bunday "faqat ma'lumot tashuvchi, o'zgarmas" obyektlarni **DTO** (Data Transfer Object — ma'lumot tashuvchi obyekt) deb atashadi. Ular dasturda ma'lumotni bir joydan boshqasiga **xavfsiz** olib o'tish uchun ishlatiladi:

```php
<?php
final class PulOtkazma {
    public function __construct(
        public readonly string $kimdan,
        public readonly string $kimga,
        public readonly int $summa,
    ) {}
}

$otkazma = new PulOtkazma("Ali", "Vali", 50000);
echo "{$otkazma->kimdan} -> {$otkazma->kimga}: {$otkazma->summa} so'm";
// Ali -> Vali: 50000 so'm
```

Bu `PulOtkazma` yaratilgach, uning hech bir maydoni o'zgarmaydi — pul o'tkazmasining "kim, kimga, qancha" ma'lumoti soxtalashtirilolmaydi. Aynan shunaqa kafolat kerak bo'lganda `readonly` + promotion eng qulay vositadir.

> **Eslatma — `final`.** Yuqorida `final class` yozdik — bu "bu class'dan meros olib bo'lmaydi" degani (meros bilan keyingi bobda tanishasiz). DTO'lar uchun bu odatiy: o'zgarmas obyektni kimdir meros orqali kengaytirib, qoidasini buzmasligi uchun.

### Asimmetrik ko'rinish (asymmetric visibility) — PHP 8.4

Ko'pincha bizga shunaqa xususiyat kerak bo'ladi: uni **tashqaridan o'qish mumkin**, lekin **o'zgartirish faqat ichkaridan**. Hozirgacha buni getter bilan hal qilardik (xususiyat `private`, alohida `getBalans()` metodi). Bu ishlaydi, lekin har bir xususiyat uchun getter yozish — zerikarli.

**PHP 8.4 dan boshlab** buni to'g'ridan-to'g'ri xususiyat e'lonida aytib qo'yish mumkin — **asimmetrik ko'rinish**. "Asimmetrik" degani: o'qish va yozish uchun **alohida** kirish darajasi:

```php
<?php
class Hisob {
    // o'qish — public (hamma ko'radi), yozish — private (faqat ichkaridan)
    public private(set) int $balans = 0;

    public function pulQoshish(int $summa): void {
        if ($summa > 0) {
            $this->balans += $summa;     // ichkaridan yozish — mumkin
        }
    }
}

$h = new Hisob();
$h->pulQoshish(100000);
echo $h->balans;        // 100000 — to'g'ridan-to'g'ri o'qildi, getter shart emas!

// $h->balans = -50000;   // ❌ Xato! yozish private — tashqaridan tegib bo'lmaydi
```

`public private(set) int $balans` ni shunday o'qing: "`balans` — `int`, **o'qish** uchun `public`, lekin **yozish** (`set`) uchun `private`". Natijada:

- `echo $h->balans;` — ishlaydi (o'qish ochiq), getter yozmadik.
- `$h->balans = -50000;` — xato beradi (yozish yopiq), ma'lumot himoyalangan.

Bu — getter/setter qoliplarining ko'p qismini olib tashlaydi. Faqat o'qish kerak bo'lsa, asimmetrik ko'rinish ko'pincha alohida getter metoddan ko'ra qisqaroq va aniqroq. `protected(set)` ham bor — u meros olgan bola class'larga yozishga ruxsat beradi (`protected` bilan quyida tanishasiz).

> **Qaysi birini tanlash?** Agar xususiyat **umuman o'zgarmasa** — `readonly`. Agar tashqaridan **o'qilsa, lekin faqat ichkaridan o'zgartirilsa** — `public private(set)` (asimmetrik). Agar o'zgartirishda **murakkab tekshiruv** kerak bo'lsa — eski usul: `private` + setter ichida `if`. Uchalasi ham bir maqsadga xizmat qiladi — ma'lumotni nazoratsiz o'zgarishdan saqlash.

### `private` va `protected` farqi — meros bilan aniqlashtirib

Yuqoridagi diagrammada uchinchi daraja — **`protected`** ham bor edi. `public` (hammaga ochiq) va `private` (faqat shu class) orasida turadi:

- **`private`** — faqat **aynan shu class** ichidan ko'rinadi. Undan meros olgan **bola class ham ko'rmaydi**.
- **`protected`** — shu class ichidan **va** undan meros olgan **bola class'lar** ichidan ko'rinadi. Lekin **tashqaridan** — yo'q.

Farqni meros bilan ko'rsak aniq bo'ladi (`extends` — keyingi bob, lekin g'oya oddiy: `It` class'i `Hayvon`dan meros oladi, uning xususiyatlarini "ichiga oladi"):

```php
<?php
class Hayvon {
    protected string $nom;       // protected — bola class ham ko'radi
    private int $maxfiyId;       // private — faqat Hayvon ko'radi

    public function __construct(string $nom, int $maxfiyId) {
        $this->nom = $nom;
        $this->maxfiyId = $maxfiyId;
    }
}

class It extends Hayvon {
    public function tanishtir(): string {
        // $this->nom — protected, shuning uchun bola class'da ishlaydi
        return "Mening ismim " . $this->nom;
        // $this->maxfiyId — private bo'lgani uchun bu yerda XATO bo'lardi
    }
}

$it = new It("Bobik", 777);
echo $it->tanishtir();   // Mening ismim Bobik
```

Bu yerda `It` (bola class) `$this->nom`ni bemalol ishlatdi — chunki u `protected`. Ammo agar `tanishtir()` ichida `$this->maxfiyId`ga (u `private`) murojaat qilsak, PHP uni **ko'rmaydi** — `maxfiyId` faqat `Hayvon`ning o'ziga tegishli, bolaga "meros" bo'lib o'tmaydi.

Demak, oddiy qoida:

- Xususiyatni **bola class'lar ishlatishi kerakmi?** → `protected`.
- Xususiyat **faqat shu class'ning ichki ishi**, hatto bolasiga ham bermaysizmi? → `private`.
- **Hammaga ochiqmi?** → `public` (lekin xususiyatlar uchun buni kamroq ishlating).

Amaliyotda ko'pchilik xususiyatni `private` qiladi (eng qattiq himoya), faqat bola class aniq ishlatishi kerak bo'lsa `protected`ga ko'taradi. "Avval eng yopiq, kerak bo'lsa ochasan" — yaxshi odat. `protected` bilan to'liqroq keyingi — **meros** — bobida ishlaymiz.

Quyidagi diagramma har bir kirish darajasi qayerdan ko'rinishini taqqoslaydi (`protected` bilan keyingi bo'limda — meros — tanishasiz, lekin u shu yerda umumiy manzarada ko'rsatilgan):

![public, protected va private kirish darajalari qayerdan ko'rinishi](rasmlar/phb-kirish-darajalari.svg)

### Mashqlar

**Oson**
1. `Hisob` classida `balans`ni `private` qiling. `pulQoshish` metodi orqali to'ldiring va `balansniKorish` orqali o'qing.
2. Tashqaridan `private` xususiyatga to'g'ridan-to'g'ri tegishga urinib ko'ring (`$h->balans = 100;`) — xatoni ko'ring.
3. `Talaba` classida `ism`ni private qiling, `getIsm()` getterini yozing.
4. `Talaba`ga `setIsm()` setterini qo'shing va ismni o'zgartiring.
5. `Mahsulot` classida `narx`ni private qiling, getter va setter yozing.
6. Yuqoridagi `Hisob` classida `balans`ni `private int $balans = 0;` deb **tiplab** yozing. So'ng `pulQoshish(int $summa): void` va `balansniKorish(): int` metodlariga ham tip qo'shing.

**O'rta**
7. `Hisob`ning `pulYechish` metodini yozing — balansdan ko'p pul yechishga ruxsat bermasin (`if ($summa <= $this->balans)`).
8. `Talaba`ning `setBall` setterida ball 0-100 oralig'ida ekanini tekshiring; tashqaridagi qiymat noto'g'ri bo'lsa, qabul qilmasin.
9. `Mahsulot`ning `setNarx` setterida narx manfiy bo'lmasligini ta'minlang.
10. `Foydalanuvchi` classi: `parol` private bo'lsin; `parolniOzgartir($eski, $yangi)` metodi faqat eski parol to'g'ri bo'lsa o'zgartirsin.
11. `Sana` classini yarating: `kun`, `oy`, `yil` maydonlari `public readonly int` bo'lsin va konstruktorda **promotion** orqali to'ldirilsin. `chiqar()` metodi sanani `11.06.2026` ko'rinishida qaytarsin. Obyekt yaratilgach maydonni o'zgartirishga urinib ko'ring — xatoni kuzating.
12. `Mahsulot` classida `narx`ni `public private(set) float` (asimmetrik ko'rinish, 8.4) qiling. `narxOrnat(float $narx)` metodi faqat manfiy bo'lmagan narxni o'rnatsin. Narxni tashqaridan **o'qib** ko'ring (ishlaydi), so'ng tashqaridan **yozib** ko'ring (xato).

**Qiyin**
13. To'liq `Hisob` classi: `balans` private, `pulQoshish` (musbat tekshiruvi bilan), `pulYechish` (yetarlilik tekshiruvi bilan), `balansniKorish`. Bir nechta amal bajarib sinab ko'ring.
14. `Mahsulot` classida `narx` va `chegirma` (foiz) private bo'lsin. `yakuniyNarx()` metodi chegirmani hisobga olib yakuniy narxni qaytarsin. `setChegirma` 0-100 oralig'ini tekshirsin.
15. `Termometr` classi: `harorat` private. `setHarorat` -50 dan +50 gacha oraliqni tekshirsin. `holat()` metodi haroratga qarab "sovuq/normal/issiq" qaytarsin.
16. O'zgarmas (immutable) `PulOtkazma` DTO'sini yarating: `kimdan`, `kimga`, `summa` — barchasi `public readonly`, promotion bilan. Class'ni `final` qiling. Bir nechta o'tkazma yarating va ularning maydonlarini o'qing; maydonni o'zgartirib bo'lmasligini tekshiring.

<details markdown="1">
<summary>Yechim — 7 (xavfsiz pul yechish)</summary>

```php
<?php
class Hisob {
    private int $balans = 0;

    public function pulQoshish(int $summa): void {
        if ($summa > 0) {
            $this->balans += $summa;
        }
    }

    public function pulYechish(int $summa): bool {
        if ($summa > 0 && $summa <= $this->balans) {   // yetarli pul bormi?
            $this->balans -= $summa;
            return true;    // muvaffaqiyatli
        }
        return false;       // yechib bo'lmadi
    }

    public function balansniKorish(): int {
        return $this->balans;
    }
}

$h = new Hisob();
$h->pulQoshish(100000);
$h->pulYechish(150000);   // false — pul yetarli emas, balans o'zgarmaydi
echo $h->balansniKorish(); // 100000
$h->pulYechish(30000);    // true
echo "<br>" . $h->balansniKorish(); // 70000
```
Mana inkapsulyatsiyaning kuchi: `balans` himoyalangani uchun, undan ko'p pul yechib bo'lmaydi — qoida class ichida kafolatlangan. E'tibor bering: xususiyat va metodlar **tiplangan** (`private int`, `: bool`, `: int`) — zamonaviy PHP uslubi.
</details>

<details markdown="1">
<summary>Yechim — 11 (readonly Sana, promotion bilan)</summary>

```php
<?php
final class Sana {
    public function __construct(
        public readonly int $kun,
        public readonly int $oy,
        public readonly int $yil,
    ) {}

    public function chiqar(): string {
        return sprintf("%02d.%02d.%d", $this->kun, $this->oy, $this->yil);
    }
}

$s = new Sana(11, 6, 2026);
echo $s->chiqar();      // 11.06.2026

// $s->kun = 25;        // ❌ Xato! Cannot modify readonly property Sana::$kun
```
`kun`, `oy`, `yil` — `public readonly`, shuning uchun ularni tashqaridan **o'qish** mumkin (`$s->kun`), lekin **o'zgartirib bo'lmaydi**. Konstruktor promotion tufayli butun class qisqa: xususiyatlarni alohida e'lon qilib, qo'lda to'ldirish shart emas. Bu — o'zgarmas (immutable) obyektga klassik misol.
</details>

<details markdown="1">
<summary>Yechim — 12 (asimmetrik ko'rinish, PHP 8.4)</summary>

```php
<?php
class Mahsulot {
    public private(set) float $narx = 0;   // o'qish public, yozish private

    public function __construct(float $narx) {
        $this->narxOrnat($narx);
    }

    public function narxOrnat(float $narx): void {
        if ($narx >= 0) {                  // faqat manfiy bo'lmagan narx
            $this->narx = $narx;
        }
    }
}

$m = new Mahsulot(1500);
echo $m->narx;           // 1500 — tashqaridan o'qish ishlaydi (getter yo'q!)
$m->narxOrnat(2000);     // ichkaridan o'zgartirish — mumkin
echo "<br>" . $m->narx;  // 2000

// $m->narx = -99;       // ❌ Xato! Cannot modify private(set) property
```
`public private(set)` tufayli `narx`ni tashqaridan **o'qish** mumkin, lekin **yozish** faqat class ichidan (`narxOrnat` orqali, u esa manfiy narxni rad etadi). Alohida getter yozish shart bo'lmadi — bu asimmetrik ko'rinishning asosiy qulayligi.
</details>

<details markdown="1">
<summary>Yechim — 13 (to'liq, himoyalangan Hisob)</summary>

Bu — 7-mashqdagi `Hisob` class'ining to'liq ko'rinishi. Endi uni amalda sinab ko'ramiz:

```php
<?php
class Hisob {
    private int $balans = 0;

    public function pulQoshish(int $summa): void {
        if ($summa > 0) {                  // faqat musbat summa
            $this->balans += $summa;
        }
    }

    public function pulYechish(int $summa): bool {
        if ($summa > 0 && $summa <= $this->balans) {
            $this->balans -= $summa;
            return true;
        }
        return false;
    }

    public function balansniKorish(): int {
        return $this->balans;
    }
}

$h = new Hisob();
$h->pulQoshish(200000);
$h->pulQoshish(-5000);     // e'tiborsiz qoldiriladi (musbat emas)
$h->pulYechish(50000);     // true
$h->pulYechish(999999);    // false (yetarli emas)

echo $h->balansniKorish();   // 150000
```
`balans` `private int` — unga faqat class metodlari orqali tegish mumkin. Shuning uchun "manfiy pul qo'shish" yoki "yo'q pulni yechish" kabi noto'g'ri holatlar oldindan to'siladi. Ma'lumotni himoyalashning butun maqsadi shu.
</details>

<details markdown="1">
<summary>Yechim — 14 (Mahsulot: narx va chegirma)</summary>

```php
<?php
class Mahsulot {
    private int $chegirma = 0;   // foizda, standart 0

    public function __construct(
        private float $narx,     // konstruktor promotion + tip
    ) {}

    public function setChegirma(int $foiz): void {
        if ($foiz >= 0 && $foiz <= 100) {   // faqat 0-100 oralig'i
            $this->chegirma = $foiz;
        }
    }

    public function yakuniyNarx(): float {
        return $this->narx - ($this->narx * $this->chegirma / 100);
    }
}

$p = new Mahsulot(1000);
$p->setChegirma(25);
echo $p->yakuniyNarx();   // 750

$p->setChegirma(150);     // noto'g'ri — e'tiborsiz qoldiriladi, chegirma 25 qoladi
echo "<br>" . $p->yakuniyNarx();   // 750
```
`setChegirma` setteri chegirma 0-100 oralig'ida ekanini kafolatlaydi — noto'g'ri qiymat (150%) qabul qilinmaydi. Bu — setterning asosiy foydasi: o'zgaruvchiga noto'g'ri ma'lumot tushishini oldini oladi. `narx` esa konstruktor promotion bilan (`private float $narx`) qisqa e'lon qilindi.
</details>

<details markdown="1">
<summary>Yechim — 15 (Termometr)</summary>

```php
<?php
class Termometr {
    private int $harorat = 0;

    public function setHarorat(int $qiymat): void {
        if ($qiymat >= -50 && $qiymat <= 50) {
            $this->harorat = $qiymat;
        }
    }

    public function holat(): string {
        return match(true) {
            $this->harorat < 10  => "sovuq",
            $this->harorat <= 25 => "normal",
            default              => "issiq",
        };
    }
}

$t = new Termometr();
$t->setHarorat(30);
echo $t->holat();   // issiq

$t->setHarorat(15);
echo "<br>" . $t->holat();   // normal
```
`setHarorat` qiymatni mantiqiy oraliqda (-50..+50) ushlaydi, `holat()` esa `match` bilan haroratga qarab so'z qaytaradi (1.6'dagi `match`ni eslang). Xususiyat va metodlar tiplangan (`private int`, `: void`, `: string`).
</details>

<details markdown="1">
<summary>Yechim — 16 (o'zgarmas PulOtkazma DTO)</summary>

```php
<?php
final class PulOtkazma {
    public function __construct(
        public readonly string $kimdan,
        public readonly string $kimga,
        public readonly int $summa,
    ) {}

    public function chiqar(): string {
        return "{$this->kimdan} -> {$this->kimga}: {$this->summa} so'm";
    }
}

$a = new PulOtkazma("Ali", "Vali", 50000);
$b = new PulOtkazma("Hasan", "Husan", 120000);

echo $a->chiqar();           // Ali -> Vali: 50000 so'm
echo "<br>" . $b->chiqar();  // Hasan -> Husan: 120000 so'm

// $a->summa = 999999;       // ❌ Xato! Cannot modify readonly property
```
Har bir `PulOtkazma` yaratilgach, uning maydonlari **qotib qoladi** — `kimdan`, `kimga`, `summa` na tashqaridan, na ichkaridan o'zgaradi. Bu o'tkazma ma'lumoti soxtalashtirilmasligini kafolatlaydi. `final` esa class'dan meros olib qoidani buzishni to'sadi. Mana shu — `readonly` + promotion bilan tuzilgan o'zgarmas (immutable) DTO.
</details>
