# 2.9 Enum — cheklangan tanlovlar

[⬅️ Oldingi: 2.8 Trait — metodlarni ulashish](./21-trait-metodlarni-ulashish.md) · [🏠 README](./README.md) · [Keyingi: 2.10 Xatolarni boshqarish (try / catch) ➡️](./23-xatolarni-boshqarish.md)

---

### Muammo: "sehrli matnlar"

Tasavvur qiling, buyurtmaning holatini saqlaymiz. Holat faqat ma'lum qiymatlardan biri bo'lishi mumkin: "yangi", "yo'lda", "yetkazildi", "bekor qilindi". Buni oddiy matn bilan saqlasak:

```php
<?php
$holat = "yetkazildi";
```

Muammo: bu yerda matnni xato yozish oson. `"yetkzildi"` (harf tushib qolgan) deb yozsangiz, PHP buni xato deb aytmaydi — shunchaki noto'g'ri ishlaydi. Yoki `"Yetkazildi"` (katta harf bilan) — boshqa qiymat hisoblanadi. Bunday "sehrli matnlar" (magic strings) — xatolar manbai.

**Enum** ana shuni hal qiladi: faqat **oldindan belgilangan** qiymatlar ro'yxatini yaratadi, boshqasiga ruxsat bermaydi.

### Enum nima?

**Enum (enumeration) — cheklangan, nomlangan qiymatlar to'plami.** "Faqat shu variantlardan biri bo'lishi mumkin" degani:

```php
<?php
enum Holat {
    case Yangi;
    case Yolda;
    case Yetkazildi;
    case BekorQilindi;
}

// Endi holat faqat shu to'rttadan biri bo'lishi mumkin:
$holat = Holat::Yetkazildi;

if ($holat === Holat::Yetkazildi) {
    echo "Buyurtma yetkazildi";
}
```

Tushuntiramiz:
- **`enum Holat { ... }`** — Holat degan enum yaratamiz.
- **`case Yangi;`** — har bir mumkin bo'lgan qiymat `case` bilan e'lon qilinadi.
- **`Holat::Yetkazildi`** — qiymatga shunday murojaat qilamiz (class'dagi static kabi, `::` bilan).

Endi `Holat::Yetkzildi` (xato yozsangiz) — PHP **darrov xato beradi**, chunki bunday `case` yo'q. Bu matnda mumkin emas edi. Enum sizni xatolardan himoyalaydi.

> **Kichik modernizatsiya: `==` o'rniga `===`.** Yuqorida `if ($holat === Holat::Yetkazildi)` deb yozdik. Enum bilan ikkala variant ham ishlaydi, lekin zamonaviy PHP'da har doim `===` (qat'iy tenglik) ishlatish odat — u "qiymati ham, turi ham bir xilmi?" deb tekshiradi va kutilmagan o'zgarishlardan himoya qiladi. Enum'ning har bir `case`'i — yagona (singleton) obyekt, shuning uchun `Holat::Yangi === Holat::Yangi` har doim `true`.

### Qiymatli enum (backed enum)

Ko'pincha enumning har bir variantiga aniq qiymat (matn yoki son) biriktirish kerak bo'ladi — masalan, bazaga saqlash uchun:

```php
<?php
enum Holat: string {
    case Yangi = 'yangi';
    case Yolda = 'yolda';
    case Yetkazildi = 'yetkazildi';
}

$holat = Holat::Yetkazildi;
echo $holat->value;   // yetkazildi   (biriktirilgan qiymat)
```

`enum Holat: string` — "har bir variantning matn qiymati bor" degani. `$holat->value` orqali o'sha qiymatni olamiz. Bu, masalan, holatni bazaga `"yetkazildi"` deb saqlash uchun qulay.

### Backed enum — chuqurroq: nega "backed"?

"Backed" (ortida qiymati bor) enum — bu **har bir `case`'ga aniq qiymat biriktirilgan** enum. Yuqoridagi oddiy `enum Holat { case Yangi; ... }` da `case`'larning faqat nomi bor, ortida hech qanday matn/son yo'q. Bunday enum'ni bazaga to'g'ridan-to'g'ri saqlab bo'lmaydi — chunki "Yangi" obyektini matn yoki songa aylantirish kerak. Backed enum aynan shu muammoni hal qiladi.

Backed enum'ning ikki turi bor: **`string`** (matn ortida) yoki **`int`** (son ortida). Boshqa tip bo'lmaydi.

```php
<?php
// Matn ortidagi enum
enum Rol: string {
    case Admin  = 'admin';
    case Oddiy  = 'oddiy';
    case Mehmon = 'mehmon';
}

// Son ortidagi enum
enum Daraja: int {
    case Boshlangich = 1;
    case Orta        = 2;
    case Yuqori      = 3;
}

echo Rol::Admin->value;       // admin   (matn)
echo "\n";
echo Daraja::Orta->value;     // 2       (son)
```

Har bir backed enum obyektida **ikkita o'qish mumkin bo'lgan xususiyat** bor:

- **`->name`** — `case`'ning nomi (har doim matn): `Daraja::Orta->name` => `"Orta"`.
- **`->value`** — biriktirilgan qiymat: `Daraja::Orta->value` => `2`.

```php
<?php
enum Daraja: int {
    case Boshlangich = 1;
    case Orta        = 2;
    case Yuqori      = 3;
}

$d = Daraja::Orta;
echo $d->name . "\n";    // Orta   (kod ichidagi nom)
echo $d->value . "\n";   // 2      (bazaga saqlanadigan son)
```

Demak amaliy qoida: **kodda — `Daraja::Orta`** (o'qish oson, xatosiz), **bazada esa — `2`** (kompakt). Backed enum bu ikki olamni bir-biriga bog'laydi.

### `cases()` — barcha variantlar ro'yxati

Har bir enum'da avtomatik tayyor **`cases()`** metodi bor. U enum'ning **barcha variantlarini massiv** ko'rinishida qaytaradi — siz hech narsa yozmaysiz, PHP o'zi beradi. Bu, ayniqsa, formada **dropdown (select)** yasash yoki barcha variantlar ustidan aylanish uchun juda qulay:

```php
<?php
enum Holat: string {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';
}

// Barcha variantlar ustidan aylanamiz
foreach (Holat::cases() as $variant) {
    echo $variant->name . " => " . $variant->value . "\n";
}
// Yangi => yangi
// Yolda => yolda
// Yetkazildi => yetkazildi

echo count(Holat::cases());   // 3  (nechta variant borligi)
```

`Holat::cases()` — `[Holat::Yangi, Holat::Yolda, Holat::Yetkazildi]` massivini qaytaradi. Endi formaga `<select>` yasaymiz — barcha holatlarni qo'lda yozish shart emas, enum o'zi beradi:

```php
<?php
enum Holat: string {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';

    public function label(): string {
        return match($this) {
            Holat::Yangi      => "Yangi",
            Holat::Yolda      => "Yo'lda",
            Holat::Yetkazildi => "Yetkazildi",
        };
    }
}

echo "<select name=\"holat\">\n";
foreach (Holat::cases() as $variant) {
    echo "  <option value=\"{$variant->value}\">{$variant->label()}</option>\n";
}
echo "</select>\n";
```

Natija:

```html
<select name="holat">
  <option value="yangi">Yangi</option>
  <option value="yolda">Yo'lda</option>
  <option value="yetkazildi">Yetkazildi</option>
</select>
```

Eng katta foydasi: keyinroq enum'ga yangi `case` qo'shsangiz (masalan, `BekorQilindi`), dropdown'da u **avtomatik** paydo bo'ladi — bir joyni ham qo'lda tahrirlash kerak emas. Bu — "bir joyda ro'yxat" tamoyilining amaliy mevasi.

### `from()` va `tryFrom()` — qiymatdan enum yasash

Yuqorida `$holat->value` orqali enum'dan qiymatni oldik. Endi **teskari** vazifa: bazadan `"yolda"` degan matn keldi — uni qanday qilib `Holat::Yolda` obyektiga aylantiramiz? Buning uchun ikki tayyor metod bor: **`from()`** va **`tryFrom()`**. Ikkalasi ham faqat backed enum'da ishlaydi (chunki qiymatdan qidirish kerak).

**`from($qiymat)`** — qiymatga mos `case`'ni topadi. **Topa olmasa — xato (`ValueError`) tashlaydi** (dasturni to'xtatadi):

```php
<?php
enum Holat: string {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';
}

$holat = Holat::from('yolda');
echo $holat->name . "\n";    // Yolda

// Mavjud bo'lmagan qiymat — xato:
try {
    $x = Holat::from('mavjud-emas');
} catch (\ValueError $e) {
    echo "Xato: bunday holat yo'q\n";
}
```

**`tryFrom($qiymat)`** — xuddi shunday, lekin **topa olmasa xato tashlamaydi, `null` qaytaradi**:

```php
<?php
enum Holat: string {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';
}

$bor = Holat::tryFrom('yangi');
echo $bor->name . "\n";      // Yangi

$yoq = Holat::tryFrom('mavjud-emas');
var_dump($yoq);              // NULL  (xato emas, shunchaki null)
```

**Qaysi birini qachon ishlatish kerak?**

- **`from()`** — qiymat **albatta to'g'ri** bo'lishi kerak bo'lganda (masalan, o'zingiz yozgan kod ichidan). Xato bo'lsa — darrov bilib olish yaxshi.
- **`tryFrom()`** — qiymat **ishonchsiz manba**dan kelganda: **bazadan o'qishda**, formadan, API'dan. Bu yerda `tryFrom()` deyarli **majburiy**, chunki bazadagi qiymat eskirgan, buzilgan yoki kutilmagan bo'lishi mumkin — bunda butun dasturni qulatib qo'ymaslik kerak.

`tryFrom()` ni `??` (null-koalescing) bilan birga ishlatish — eng keng tarqalgan andoza. "Topilmasa, zaxira (default) qiymat ber":

```php
<?php
enum Rol: string {
    case Admin  = 'admin';
    case Oddiy  = 'oddiy';
    case Mehmon = 'mehmon';
}

// Bazadan kelgan qiymat — buzilgan/eski bo'lishi mumkin
$bazadan = 'super-admin';   // bunday rol yo'q

$rol = Rol::tryFrom($bazadan) ?? Rol::Mehmon;   // topilmasa — Mehmon
echo $rol->name . "\n";     // Mehmon (xavfsiz zaxira)
```

Bu yerda: agar `tryFrom()` `null` qaytarsa, `??` darrov `Rol::Mehmon`'ni beradi. Dastur qulamaydi, foydalanuvchi eng kam huquqli rolni oladi — bu xavfsizlik nuqtai nazaridan to'g'ri tanlov.

### Bazadan o'qishning to'liq misoli

Backed enum + `tryFrom()` + `value` — birgalikda baza bilan ishlashning klassik aylanasini tashkil qiladi. **Saqlashda** `->value` (enum -> matn), **o'qishda** `tryFrom()` (matn -> enum):

```php
<?php
enum Holat: string {
    case Yangi        = 'yangi';
    case Yolda        = 'yolda';
    case Yetkazildi   = 'yetkazildi';
    case BekorQilindi = 'bekor';

    public function label(): string {
        return match($this) {
            Holat::Yangi        => "Yangi buyurtma",
            Holat::Yolda        => "Yo'lda",
            Holat::Yetkazildi   => "Yetkazildi",
            Holat::BekorQilindi => "Bekor qilindi",
        };
    }
}

// 1) SAQLASH: enum -> matn (bazaga $b->holat->value yoziladi)
$saqlanadigan = Holat::Yolda->value;
echo "Bazaga yoziladi: $saqlanadigan\n";   // Bazaga yoziladi: yolda

// 2) O'QISH: bazadan kelgan qatorlar (biri buzilgan)
$qatorlar = ['yangi', 'yetkazildi', 'notogri-qiymat', 'bekor'];

foreach ($qatorlar as $q) {
    $holat = Holat::tryFrom($q);
    if ($holat === null) {
        echo "$q -> NOMA'LUM (e'tibordan chetda)\n";
        continue;
    }
    echo "$q -> {$holat->label()}\n";
}
// yangi -> Yangi buyurtma
// yetkazildi -> Yetkazildi
// notogri-qiymat -> NOMA'LUM (e'tibordan chetda)
// bekor -> Bekor qilindi
```

E'tibor bering: `'notogri-qiymat'` butun dasturni qulatmadi — `tryFrom()` `null` qaytardi, biz uni xushmuomalalik bilan o'tkazib yubordik. Bu — ishonchli (robust) kod belgisi.

### Enum metodlari — `match($this)`

Eng kuchli imkoniyatlardan biri: **enum ichida metod yozish mumkin** (xuddi class'dagidek). Bu, ayniqsa, har bir variantga "qo'shimcha ma'lumot" (o'qiladigan yorliq, rang, ball) biriktirishda foydali. Metod ichida joriy variantni `$this` orqali bilib olamiz va `match($this)` bilan mos natijani qaytaramiz:

```php
<?php
enum Holat: string {
    case Yangi        = 'yangi';
    case Yolda        = 'yolda';
    case Yetkazildi   = 'yetkazildi';
    case BekorQilindi = 'bekor';

    // Inson o'qiy oladigan yorliq
    public function label(): string {
        return match($this) {
            Holat::Yangi        => "Yangi buyurtma",
            Holat::Yolda        => "Yo'lda",
            Holat::Yetkazildi   => "Yetkazildi",
            Holat::BekorQilindi => "Bekor qilindi",
        };
    }

    // Interfeysda ko'rsatish uchun rang
    public function rang(): string {
        return match($this) {
            Holat::Yangi        => "kok",
            Holat::Yolda        => "sariq",
            Holat::Yetkazildi   => "yashil",
            Holat::BekorQilindi => "qizil",
        };
    }
}

$h = Holat::Yolda;
echo $h->label() . "\n";   // Yo'lda
echo $h->rang() . "\n";    // sariq
```

> **`match($this)` qanday ishlaydi?** `match` — `if/elseif` ning ixcham va toza ko'rinishi. `match($this)` joriy enum qiymatini olib, har bir `Holat::... => natija` qatorini tekshiradi va birinchi mos kelganini qaytaradi. `match` qat'iy (`===`) solishtiradi, shuning uchun enum bilan idealdir.

Bir nechta `case`'ni bitta natijaga ham bog'lash mumkin — vergul bilan ajratamiz. Masalan, "yakunlangan" holatlar (yetkazilgan yoki bekor qilingan):

```php
<?php
enum Holat: string {
    case Yangi        = 'yangi';
    case Yolda        = 'yolda';
    case Yetkazildi   = 'yetkazildi';
    case BekorQilindi = 'bekor';

    public function yakunlanganmi(): bool {
        return match($this) {
            Holat::Yetkazildi, Holat::BekorQilindi => true,   // ikkalasi ham
            default => false,
        };
    }
}

var_dump(Holat::Yetkazildi->yakunlanganmi());   // true
var_dump(Holat::Yangi->yakunlanganmi());        // false
```

`default` — "boshqa barcha holatlar uchun" degani (xuddi `switch`'dagi `default` kabi).

### Enum const — o'zgarmas qiymatlar

Enum ichida **const** (o'zgarmas qiymat) ham e'lon qilish mumkin — masalan, "asosiy" (default) variantni belgilash uchun. `self::` orqali enum'ning o'z `case`'iga murojaat qilamiz:

```php
<?php
enum Holat: string {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';

    // Yangi buyurtma uchun asosiy (default) holat
    const Boshlangich = self::Yangi;
}

echo Holat::Boshlangich->name . "\n";    // Yangi
echo Holat::Boshlangich->value . "\n";   // yangi
```

`const Boshlangich = self::Yangi;` — "Boshlangich nomli o'zgarmas, qiymati `Holat::Yangi`" degani. Endi kodning turli joyida `Holat::Yangi` deb takrorlash o'rniga `Holat::Boshlangich` deb mazmunli nom ishlatish mumkin.

### Enum interfeys (interface) qabul qilishi

Enum ham, class kabi, **interfeys** qabul qila oladi (`implements`). Bu shuni anglatadi: enum o'sha interfeysdagi metodlarni majburan yozadi va `instanceof` bilan tekshirilishi mumkin. Bu, masalan, turli enum'larni bir xil "qoidaga" bo'ysundirish kerak bo'lganda foydali (2.6-bobdagi interfeysni eslang):

```php
<?php
// Shartnoma: "rang qaytara olishing kerak"
interface Ranglangan {
    public function rang(): string;
}

enum Holat: string implements Ranglangan {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';

    const Boshlangich = self::Yangi;

    // Interfeys talab qilgan metod — majburan yozildi
    public function rang(): string {
        return match($this) {
            Holat::Yangi      => "kok",
            Holat::Yolda      => "sariq",
            Holat::Yetkazildi => "yashil",
        };
    }
}

$h = Holat::Yetkazildi;
echo ($h instanceof Ranglangan ? "ha" : "yoq") . "\n";  // ha
echo $h->rang() . "\n";                                 // yashil
echo Holat::Boshlangich->name . "\n";                   // Yangi
```

Bu yerda `enum Holat: string implements Ranglangan` — bir vaqtda **backed enum** (`: string`) va **interfeysni qabul qiladi** (`implements Ranglangan`). Endi `rang()` metodini yozmasangiz, PHP xato beradi — interfeys "shartnoma"ni majburlaydi.

### Foydasi

1. **Xatosizlik:** faqat ruxsat etilgan qiymatlar. Xato matn yozib bo'lmaydi.
2. **Aniqlik:** kod o'qiganda `Holat::Yetkazildi` — `"yetkazildi"` matnidan ravshanroq.
3. **Bir joyda:** barcha mumkin bo'lgan holatlar bir joyda ro'yxatlangan.
4. **Baza bilan moslik:** backed enum + `value` + `tryFrom()` — bazaga saqlash va o'qishni xavfsiz qiladi.
5. **Boyitilgan:** metod, const va interfeys orqali har bir variantga yorliq, rang, ball kabi ma'lumot biriktiriladi.

Enum, masalan, holat (buyurtma holati), rol (foydalanuvchi roli: admin/oddiy), kun (hafta kunlari) kabi "cheklangan variantlar" uchun ideal.

### Mashqlar

**Oson**
1. `Holat` enum'ini yarating (`Yangi`, `Yolda`, `Yetkazildi`). Bir o'zgaruvchiga qiymat bering va `if` bilan tekshiring.
2. `Kun` enum'ini yarating (hafta kunlari) va bittasini tanlang.
3. `Rol` enum'ini yarating (`Admin`, `Oddiy`, `Mehmon`).
4. Qiymatli enum yarating (`Holat: string`) va `->value` ni chiqaring.
5. `Yonalish` enum'i (`Shimol`, `Janub`, `Sharq`, `Garb`) yarating.
6. Backed enum `Rol: string` yarating, `Rol::Admin->name` va `Rol::Admin->value` ni chiqaring — farqini ko'ring.
7. Istalgan backed enum uchun `cases()` ni `foreach` bilan aylanib, har bir variantning nomini chiqaring.

**O'rta**
8. `Rol` enum'i bilan: foydalanuvchi roli `Admin` bo'lsa "Boshqaruv paneli", aks holda "Oddiy sahifa" chiqaring.
9. `Holat: string` enum'ining qiymatini bazaga saqlanadigandek `->value` orqali chiqaring.
10. Buyurtma class'i yarating, uning `holat` xususiyati enum turida bo'lsin (konstruktorda qabul qilsin).
11. `Baho` enum'i (`A`, `B`, `C`, `D`, `F`) yarating va bir nechta talaba bahosini saqlang.
12. `Holat: string` enum'idan `cases()` yordamida HTML `<select>` (dropdown) yasang — har bir variant `<option>` bo'lsin (`value` va o'qiladigan matn bilan).
13. `tryFrom()` ishlating: bir massivdagi matn qiymatlarini (`['yangi', 'xato', 'yolda']`) enum'ga aylantiring; topilmaganini "noma'lum" deb chiqaring.

**Qiyin**
14. `Buyurtma` class'i: konstruktor `holat`ni `Holat` enum sifatida olsin. `holatniOzgartir($yangiHolat)` metodi holatni yangilasin. `holatMatn()` metodi joriy holatni o'qiladigan matn ko'rinishida qaytarsin (`match` bilan).
15. Enum'ga metod qo'shish (PHP enum'larida metod bo'lishi mumkin!): `Holat` enum'iga `tavsif()` metodi qo'shing — har bir holat uchun o'zbekcha izoh qaytarsin (`match($this)` ishlatib).
16. `Baho: string` backed enum'iga `ball(): int` metodi qo'shing (A=5 ... F=1) va `otganmi(): bool` metodi (F bo'lmasa `true`). Bir nechta bahoni aylanib, ball va o'tdi/qoldi holatini chiqaring.
17. `Holat: string` enum'iga `Ranglangan` interfeysini qabul qildiring (`rang(): string`) va `const Boshlangich = self::Yangi;` qo'shing. `instanceof` bilan tekshiring.
18. Backed enum `tryFrom()` + `??` bilan "xavfsiz default" andozasini qo'llang: bazadan kelgan ishonchsiz rol matnini `Rol` enum'iga aylantiring; topilmasa `Rol::Mehmon` bo'lsin.

<details markdown="1">
<summary>Yechim — 12 (cases() bilan dropdown)</summary>

```php
<?php
enum Holat: string {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';

    public function label(): string {
        return match($this) {
            Holat::Yangi      => "Yangi",
            Holat::Yolda      => "Yo'lda",
            Holat::Yetkazildi => "Yetkazildi",
        };
    }
}

echo "<select name=\"holat\">\n";
foreach (Holat::cases() as $variant) {
    echo "  <option value=\"{$variant->value}\">{$variant->label()}</option>\n";
}
echo "</select>\n";
```

Natija:

```html
<select name="holat">
  <option value="yangi">Yangi</option>
  <option value="yolda">Yo'lda</option>
  <option value="yetkazildi">Yetkazildi</option>
</select>
```

`cases()` barcha variantlarni avtomatik beradi. Yangi `case` qo'shsangiz, dropdown'da o'zi paydo bo'ladi — qo'lda hech narsa qo'shish kerak emas.
</details>

<details markdown="1">
<summary>Yechim — 13 (tryFrom bilan matnlarni aylantirish)</summary>

```php
<?php
enum Holat: string {
    case Yangi       = 'yangi';
    case Yolda       = 'yolda';
    case Yetkazildi  = 'yetkazildi';
}

$matnlar = ['yangi', 'xato', 'yolda'];

foreach ($matnlar as $matn) {
    $holat = Holat::tryFrom($matn);
    if ($holat === null) {
        echo "$matn -> noma'lum\n";
    } else {
        echo "$matn -> {$holat->name}\n";
    }
}
// yangi -> Yangi
// xato -> noma'lum
// yolda -> Yolda
```

`tryFrom()` topa olmasa `null` qaytaradi — shuning uchun dastur qulamaydi. `from()` bo'lsa, `'xato'`da butun dastur to'xtardi. Ishonchsiz manbada (massiv, baza, forma) doim `tryFrom()`.
</details>

<details markdown="1">
<summary>Yechim — 14 (Buyurtma holati)</summary>

```php
<?php
enum Holat: string {
    case Yangi      = 'yangi';
    case Yolda      = 'yolda';
    case Yetkazildi = 'yetkazildi';

    // O'qiladigan matn — enum metodida
    public function label(): string {
        return match($this) {
            Holat::Yangi      => "Buyurtma qabul qilindi",
            Holat::Yolda      => "Buyurtma yo'lda",
            Holat::Yetkazildi => "Buyurtma yetkazildi",
        };
    }
}

class Buyurtma {
    // Constructor promotion + tiplangan xususiyat (zamonaviy PHP 8.4)
    public function __construct(
        public Holat $holat
    ) {}

    public function holatniOzgartir(Holat $yangiHolat): void {
        $this->holat = $yangiHolat;
    }

    public function holatMatn(): string {
        return $this->holat->label();
    }
}

$b = new Buyurtma(Holat::Yangi);
echo $b->holatMatn() . "\n";        // Buyurtma qabul qilindi

$b->holatniOzgartir(Holat::Yolda);
echo $b->holatMatn() . "\n";        // Buyurtma yo'lda

// Bazaga saqlash uchun matn:
echo "Bazaga: " . $b->holat->value . "\n";   // Bazaga: yolda
```

E'tibor bering: bu yangi (8.4) uslubda yozildi. Avval `public $holat;` ni alohida e'lon qilib, konstruktorda `$this->holat = $holat;` yozardik. Endi **constructor promotion** bilan `public Holat $holat` to'g'ridan-to'g'ri konstruktor qavsida — qisqaroq va xususiyatga **tip** (`Holat`) ham qo'yilgan. Shuning uchun `holat`ga faqat haqiqiy `Holat` qiymati tushadi — xato matn ("yetkzildi") berib bo'lmaydi. `holatMatn()` esa enum'ning o'z `label()` metodiga ishonadi. Enum + tip e'loni + `match` — birgalikda juda ishonchli.
</details>

<details markdown="1">
<summary>Yechim — 15 (metodli enum)</summary>

```php
<?php
enum Holat: string {
    case Yangi = 'yangi';
    case Yolda = 'yolda';
    case Yetkazildi = 'yetkazildi';

    // Enum ichida metod ham bo'lishi mumkin
    public function tavsif(): string {
        return match($this) {
            Holat::Yangi       => "Buyurtma qabul qilindi",
            Holat::Yolda       => "Buyurtma yo'lda",
            Holat::Yetkazildi  => "Buyurtma yetkazib berildi",
        };
    }
}

$holat = Holat::Yolda;
echo $holat->tavsif();   // Buyurtma yo'lda
```

> **Yangi narsa: `match`.** Bu — `if/elseif` ning ixcham ko'rinishi. `match($this)` joriy qiymatni tekshiradi va mos kelganini qaytaradi. `Holat::Yangi => "..."` degani: "agar joriy holat Yangi bo'lsa, shu matnni qaytar". `match` ayniqsa "bir qiymatga qarab turli natija" kerak bo'lganda qulay va `if/elseif`dan toza ko'rinadi.
</details>

<details markdown="1">
<summary>Yechim — 16 (Baho: ball va o'tdi/qoldi)</summary>

```php
<?php
enum Baho: string {
    case A = 'a';
    case B = 'b';
    case C = 'c';
    case D = 'd';
    case F = 'f';

    public function ball(): int {
        return match($this) {
            Baho::A => 5,
            Baho::B => 4,
            Baho::C => 3,
            Baho::D => 2,
            Baho::F => 1,
        };
    }

    public function otganmi(): bool {
        return $this !== Baho::F;   // F'dan boshqa hammasi — o'tgan
    }
}

$baholar = [Baho::A, Baho::C, Baho::F];
foreach ($baholar as $b) {
    $holat = $b->otganmi() ? "o'tdi" : "qoldi";
    echo $b->name . " = " . $b->ball() . " ball ($holat)\n";
}
// A = 5 ball (o'tdi)
// C = 3 ball (o'tdi)
// F = 1 ball (qoldi)
```

`ball()` har bahoga son biriktiradi (`match`), `otganmi()` esa oddiy `===`/`!==` solishtirish bilan mantiqiy javob beradi. Diqqat: enum `case`'lari yagona obyekt bo'lgani uchun `$this !== Baho::F` to'g'ri ishlaydi.
</details>

<details markdown="1">
<summary>Yechim — 17 (interfeys + const)</summary>

```php
<?php
interface Ranglangan {
    public function rang(): string;
}

enum Holat: string implements Ranglangan {
    case Yangi      = 'yangi';
    case Yolda      = 'yolda';
    case Yetkazildi = 'yetkazildi';

    const Boshlangich = self::Yangi;   // asosiy (default) holat

    public function rang(): string {
        return match($this) {
            Holat::Yangi      => "kok",
            Holat::Yolda      => "sariq",
            Holat::Yetkazildi => "yashil",
        };
    }
}

$h = Holat::Yolda;
echo ($h instanceof Ranglangan ? "ha" : "yoq") . "\n";   // ha
echo $h->rang() . "\n";                                  // sariq
echo Holat::Boshlangich->name . "\n";                    // Yangi
```

Enum bir vaqtning o'zida **backed** (`: string`), **interfeys qabul qiladi** (`implements Ranglangan`) va **const**ga ega. Interfeys `rang()` metodini majburlaydi — yozmasangiz, PHP xato beradi. `const Boshlangich` esa mazmunli "default" nomini beradi.
</details>

<details markdown="1">
<summary>Yechim — 18 (tryFrom + ?? xavfsiz default)</summary>

```php
<?php
enum Rol: string {
    case Admin  = 'admin';
    case Oddiy  = 'oddiy';
    case Mehmon = 'mehmon';
}

// Bazadan kelgan ishonchsiz qiymatlar
$bazadan = ['admin', 'super-user', 'oddiy', ''];

foreach ($bazadan as $matn) {
    // topilmasa — eng kam huquqli rol (Mehmon)
    $rol = Rol::tryFrom($matn) ?? Rol::Mehmon;
    echo "'$matn' -> {$rol->name}\n";
}
// 'admin' -> Admin
// 'super-user' -> Mehmon
// 'oddiy' -> Oddiy
// '' -> Mehmon
```

`tryFrom()` topa olmasa `null`, `??` esa darrov `Rol::Mehmon`'ni beradi. Natijada noto'g'ri yoki bo'sh qiymat hech qachon dasturni qulatmaydi — har doim xavfsiz, eng kam huquqli rol bilan davom etadi. Bu xavfsizlik uchun to'g'ri yondashuv: shubhali bo'lsa — eng kam ruxsat.
</details>
