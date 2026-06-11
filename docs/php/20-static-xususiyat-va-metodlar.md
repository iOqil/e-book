# 2.7 Static xususiyat va metodlar

[⬅️ Oldingi: 2.6 Interfeys (interface)](./19-interfeys.md) · [🏠 README](./README.md) · [Keyingi: 2.8 Trait — metodlarni ulashish ➡️](./21-trait-metodlarni-ulashish.md)

---

### Obyektga emas, class'ning o'ziga tegishli

Hozirgacha xususiyat va metodlar **har bir obyektga** tegishli edi: `$mashina1->rang`, `$mashina2->rang` — har birida alohida. Lekin ba'zan ma'lumot yoki amal **butun class'ga** tegishli bo'ladi, alohida obyektga emas. Ana shunda **static** ishlatiladi.

Misol: nechta obyekt yaratilganini sanash. Bu son birorta obyektga emas, butun class'ga tegishli.

```php
<?php
class Talaba {
    public static int $soni = 0;   // static — butun class'ga tegishli (PHP 8.4: tiplangan)

    public function __construct() {
        self::$soni++;   // har obyekt yaratilganda umumiy hisobni oshiramiz
    }
}

new Talaba();
new Talaba();
new Talaba();

echo Talaba::$soni;   // 3
```

Diqqat qiling:
- **`public static int $soni = 0;`** — `static` so'zi: bu xususiyat obyektlarga emas, **class'ning o'ziga** tegishli. U bitta, hamma obyektlar uchun umumiy. Zamonaviy PHP'da static xususiyatlarni ham **tiplaymiz** (`int`) — bu xatolardan saqlaydi.
- **`self::$soni`** — static xususiyatga class **ichidan** murojaat. `self` — "shu class" degani (`$this` "shu obyekt" edi; `self` "shu class").
- **`Talaba::$soni`** — static xususiyatga **tashqaridan** murojaat. Obyekt orqali emas (`$t->soni` emas), balki **class nomi** orqali (`Talaba::$soni`). `::` belgisi static narsalar uchun ishlatiladi.

Uchta obyekt yaratdik, har biri konstruktorda `self::$soni++` qildi — natijada umumiy hisob 3 bo'ldi.

> **Eslatma (zamonaviy uslub):** eski PHP 5/7 kodida ko'pincha tipsiz `public static $soni = 0;` yoziladi. PHP 7.4 dan boshlab xususiyatlarga tip qo'yish mumkin — `public static int $soni = 0;`. Tip qo'ysangiz, noto'g'ri qiymat berilsa PHP darrov ogohlantiradi. Shu kitobda biz hamma joyda tiplangan uslubni ishlatamiz.

### Static metodlar

Metod ham static bo'lishi mumkin — bunda uni obyekt yaratmasdan, to'g'ridan-to'g'ri class orqali chaqirasiz. Bu odatda "yordamchi" (utility) funksiyalar uchun ishlatiladi:

```php
<?php
class Matematika {
    public static function kvadrat(int|float $son): int|float {
        return $son * $son;
    }

    public static function kub(int|float $son): int|float {
        return $son * $son * $son;
    }
}

// Obyekt yaratish SHART EMAS — to'g'ridan-to'g'ri class orqali:
echo Matematika::kvadrat(5);   // 25
echo "<br>";
echo Matematika::kub(3);       // 27
```

`Matematika::kvadrat(5)` — obyekt yaratmadik (`new` yo'q), to'g'ridan-to'g'ri class orqali metodni chaqirdik. Bu mantiqiy: "kvadratni hisoblash" uchun "matematika obyekti" yaratish shart emas — funksiyaning o'zi yetarli. E'tibor bering: argumentni `int|float` (ikkala tip ham mumkin) deb tipladik va qaytarish tipini ham ko'rsatdik — bu xato kiritishdan himoya qiladi.

> **Qachon static?** Agar metod yoki ma'lumot **biror aniq obyektga bog'liq bo'lmasa** — static qiling. Masalan, "kvadratni hisoblash" hech qaysi obyektga bog'liq emas → static. Lekin "shu hisobning balansi" — aniq obyektga bog'liq → static EMAS. Boshlanishida static'ni kam ishlating; ko'pincha oddiy (obyektga tegishli) metodlar to'g'ri tanlov.

### `self` vs `static` — meros bilan eng muhim farq (Late Static Binding)

Endi static mavzusining **eng muhim** va eng ko'p chalkashtiradigan qismiga keldik. `self::` va `static::` — ikkalasi ham "class'ning static a'zosi" degani, lekin meros (`extends`) ishtirokida ular **boshqacha** ishlaydi:

- **`self::`** — har doim **e'lon qilingan** class'ni (kod yozilgan joyni) bildiradi. U meros bilan o'zgarmaydi.
- **`static::`** — **aktual** (haqiqatda chaqirilgan) class'ni bildiradi. U meros bilan o'zgaradi. Bu xatti-harakat **Late Static Binding** ("kech static bog'lanish") deb ataladi: PHP qaysi class'ni ishlatishni kompilyatsiya paytida emas, **chaqiruv paytida** hal qiladi.

Eng yaxshi tushuntiruvchi misol — bola class ota class'dagi metodni qayta yozsa:

```php
<?php
class Asosiy {
    public static function salom(): string {
        return "Asosiy class'dan salom";
    }

    public static function selfTest(): string {
        return self::salom();    // self:: — SHU class (Asosiy) ni qattiq bog'laydi
    }

    public static function staticTest(): string {
        return static::salom();  // static:: — AKTUAL (chaqirgan) class'ni ishlatadi
    }
}

class Bola extends Asosiy {
    public static function salom(): string {       // ota metodni qayta yozdik
        return "Bola class'dan salom";
    }
}

echo Bola::selfTest();    // "Asosiy class'dan salom"  — self qattiq Asosiy'ga bog'langan
echo "<br>";
echo Bola::staticTest();  // "Bola class'dan salom"    — static aktual class (Bola) ni topdi
```

Diqqat bilan kuzating:
- `Bola::selfTest()` ni chaqirdik. `selfTest()` ichida `self::salom()` bor. `self` "kod yozilgan joy" — ya'ni **Asosiy** class. Shuning uchun Bola'dagi qayta yozilgan `salom()` **e'tiborga olinmaydi**, Asosiy'niki ishlaydi.
- `Bola::staticTest()` ni chaqirdik. `staticTest()` ichida `static::salom()` bor. `static` "kim chaqirgan bo'lsa, o'sha" — ya'ni **Bola**. Shuning uchun Bola'dagi yangi `salom()` ishlaydi.

> **Oddiy qoida:** agar bola class metodni qayta yozishi mumkin bo'lsa va siz **eng so'nggi (bola) versiyani** ishlatmoqchi bo'lsangiz — `static::` ishlating. Agar **aniq shu yerda yozilgan** versiya kerak bo'lsa — `self::`. Amalda zamonaviy frameworklar (Laravel kabi) deyarli hamma joyda `static::` ishlatadi, chunki kengaytirish moslashuvchanligini beradi.

### `new static()` — meros bilan ishlaydigan factory metod

`static::` faqat metodlarda emas, **obyekt yaratishda** ham juda foydali. `new self()` doim aniq shu class obyektini yaratadi; `new static()` esa **aktual class** obyektini yaratadi. Bu farq **static factory metod** ("yasovchi metod") naqshida juda muhim.

Factory metod — bu obyektni `new` o'rniga **mazmunli nom** bilan yaratadigan static metod. `User::yarat(...)` `new User(...)` dan o'qishga qulayroq va ko'pincha qo'shimcha mantiq (validatsiya, standart qiymatlar) joylash uchun qulay:

```php
<?php
class Foydalanuvchi {
    // PHP 8.4: constructor promotion — qisqa, tiplangan konstruktor
    public function __construct(
        public string $ism,
        public string $email,
    ) {}

    // Static factory metod — obyekt yaratishning mazmunli yo'li
    public static function yarat(string $ism, string $email): static {
        return new static($ism, $email);   // new static -> aktual class obyekti
    }

    // Tayyor qiymatlar bilan "mehmon" yaratuvchi factory
    public static function mehmon(): static {
        return new static("Mehmon", "mehmon@example.com");
    }
}

class Admin extends Foydalanuvchi {
    public function rol(): string {
        return "administrator";
    }
}

$u = Foydalanuvchi::yarat("Ali", "ali@example.com");
echo $u->ism . " — " . $u->email;   // Ali — ali@example.com
echo "<br>";

// MUHIM: new static() tufayli Admin::yarat() Admin obyektini qaytaradi (Foydalanuvchi emas!)
$a = Admin::yarat("Vali", "vali@example.com");
echo get_class($a);    // Admin
echo "<br>";
echo $a->rol();        // administrator  — chunki bu haqiqatan Admin obyekti

$mehmon = Foydalanuvchi::mehmon();
echo "<br>";
echo $mehmon->ism;     // Mehmon
```

Bu yerda sehr `new static()` da:
- `Foydalanuvchi::yarat(...)` chaqirilsa, `new static()` `Foydalanuvchi` obyektini yaratadi.
- `Admin::yarat(...)` chaqirilsa, **xuddi shu `yarat()` metodi** (Admin uni meros oldi) endi `new static()` orqali **Admin** obyektini yaratadi.

Agar `new self()` yozganimizda, `Admin::yarat()` baribir `Foydalanuvchi` obyektini qaytarardi — chunki `self` qattiq `Foydalanuvchi`ga bog'langan bo'lardi. Demak, factory metodlarda **deyarli har doim `new static()`** ishlatiladi: shunda metod meros bilan to'g'ri ishlaydi.

> **Diqqat:** qaytarish tipi sifatida `: static` yozdik. Bu PHP 8.0 dan beri mavjud va "qaytariladigan obyekt aktual class'niki bo'ladi" deb va'da beradi — IDE va kelajakdagi o'zingiz uchun aniq hujjat.

### Static xususiyat meros bilan qanday ulashiladi

Static **xususiyat** (metod emas) meros qilinganda yana bir nozik holat bor: bola class otaning static xususiyatini **qayta e'lon qilmasa**, ular **bitta umumiy** xotirani bo'lishadi:

```php
<?php
class Ulagich {
    public static int $soni = 0;

    public function __construct() {
        static::$soni++;   // aktual class hisoblagichini oshiramiz
    }
}

class Bola extends Ulagich {}   // $soni ni qayta e'lon qilmadi -> umumiy

new Ulagich();   // soni -> 1
new Bola();      // umumiy bo'lgani uchun -> 2
new Bola();      // -> 3

echo "Ulagich: " . Ulagich::$soni;   // 3
echo "<br>";
echo "Bola: " . Bola::$soni;         // 3 — IKKALASI ham bitta xotirani ulashadi!
```

Bola `$soni`ni qayta e'lon qilmaganligi sababli, `Ulagich::$soni` va `Bola::$soni` **bir xil** o'zgaruvchi — ikkalasi ham 3. Agar har bir class'da **alohida** hisoblagich kerak bo'lsa, bola class xususiyatni **qayta e'lon qilishi** kerak:

```php
<?php
class Ulagich {
    public static int $soni = 0;
    public function __construct() {
        static::$soni++;   // static:: -> aktual class'ning o'z hisoblagichi
    }
}

class Bola extends Ulagich {
    public static int $soni = 0;   // O'ZINING alohida hisoblagichi
}

new Ulagich();
new Bola();
new Bola();

echo "Ulagich: " . Ulagich::$soni;   // 1
echo "<br>";
echo "Bola: " . Bola::$soni;         // 2 — endi alohida
```

E'tibor bering: bu yerda konstruktorda `self::$soni++` emas, **`static::$soni++`** yozdik. `static::` aktual class'ning xususiyatini topadi — shuning uchun Bola yaratilganda Bola'ning o'z `$soni`si oshadi. Agar `self::$soni++` yozganimizda, doim Ulagich'niki oshib qolardi. Bu yana bir misol: **meros bilan ishlaydigan static kod uchun `static::` tanlang.**

### Static hisoblagich — chuqurroq qarash

Yuqorida ko'rgan oddiy hisoblagichni "to'liq" qilamiz: hisobni o'qish va nollash metodlari bilan. Bu obyektga bog'liq bo'lmagan umumiy holatni boshqarishning klassik misoli:

```php
<?php
class Hisoblagich {
    public static int $soni = 0;

    public function __construct() {
        self::$soni++;
    }

    public static function qancha(): int {
        return self::$soni;     // joriy qiymatni o'qish
    }

    public static function nolla(): void {
        self::$soni = 0;        // qaytadan boshlash
    }
}

new Hisoblagich();
new Hisoblagich();
echo Hisoblagich::qancha();   // 2
echo "<br>";

Hisoblagich::nolla();
echo Hisoblagich::qancha();   // 0
echo "<br>";

new Hisoblagich();
echo Hisoblagich::qancha();   // 1
```

Static `$soni` dastur ishlayotgan vaqt davomida **bitta** va **saqlanib turadi** — har yangi obyekt uni oshiradi, `nolla()` esa qaytadan boshlaydi. Bu naqsh: faol foydalanuvchilarni sanash, bajarilgan so'rovlar sonini hisoblash, test paytida holatni tozalash kabi joylarda ishlatiladi.

> **Ogohlantirish:** static holat (umumiy o'zgaruvchi) qulay, lekin ko'p ishlatish kodni testlash va kuzatishni qiyinlashtiradi — chunki "kim qachon o'zgartirgani" yashirin bo'ladi. Shuning uchun static'ni faqat haqiqatan butun class'ga umumiy ma'lumot uchun ishlating, oddiy ma'lumotni esa obyekt ichida saqlang.

### Mashqlar

**Oson**
1. `Talaba` class'iga static `$soni` qo'shing. Bir nechta obyekt yarating va umumiy sonni chiqaring.
2. `Matematika` class'iga static `kvadrat($son)` metodini qo'shing, obyektsiz chaqiring.
3. `Matematika`ga static `kub()` va `ikkilantir()` metodlarini qo'shing.
4. Static xususiyatga obyekt orqali emas, class nomi (`::`) orqali murojaat qiling.
5. `Konvertor` class'i: static `kmdanMilga($km)` metodi (km × 0.621) qaytarsin.

**O'rta**
6. `Mahsulot` class'i: static `$umumiySoni` har obyekt yaratilganda oshsin. 5 ta mahsulot yaratib, sonini chiqaring.
7. `Yordamchi` class'i: static `formatNarx($son)` metodi sonni `"5 000 so'm"` ko'rinishida qaytarsin (`number_format` dan foydalaning).
8. `Hisoblagich` class'i: static `$qiymat`, static `oshir()` va `qiymatniOl()` metodlari bilan.
9. `Tasodif` class'i: static `tanga()` metodi tasodifiy "bosh" yoki "tail" qaytarsin (`rand(0, 1)` dan foydalaning).
10. (LSB) `Shakl` abstract class'ida static `yarat()` metodi `new static()` qaytarsin. `Doira` va `Kvadrat` bola class'larini yarating; har biri `nomi()` ni qaytarsin. `Doira::yarat()->nomi()` va `Kvadrat::yarat()->nomi()` ni chiqaring va natija farqini kuzating.

**Qiyin**
11. `IDgenerator` class'i: static `$oxirgiId = 0`. Static `yangiId()` metodi har chaqirilganda IDni 1 ga oshirib qaytarsin (1, 2, 3, ...). Bu — har bir yangi yozuvga noyob raqam berishning oddiy usuli.
12. `Foydalanuvchi` class'i: konstruktor `ism` olsin va static `$royxat` massiviga o'zini qo'shsin. Static `hammasi()` metodi barcha foydalanuvchilar ro'yxatini qaytarsin.
13. `Statistika` class'i: static metodlar bilan son massividan eng katta, eng kichik va o'rtacha qiymatni qaytaruvchi vositalar to'plamini yarating.
14. (Self vs static) `Asosiy` class'ida static `kim()` metodi `"Asosiy"` qaytarsin va `selfChaqir()`/`staticChaqir()` metodlari mos ravishda `self::kim()` va `static::kim()` ni qaytarsin. `Bola` class'ida `kim()` ni `"Bola"` ga qayta yozing. `Bola::selfChaqir()` va `Bola::staticChaqir()` natijalarini taqqoslab tushuntiring.
15. (Factory + LSB) `Model` class'i: konstruktor `int $id` olsin (constructor promotion). Static `topish(int $id): static` metodi `new static($id)` qaytarsin. `jadval()` metodi `static::class` asosida jadval nomini qaytarsin (masalan `Mahsulot` -> `"mahsulotlar"`). `Mahsulot` va `Buyurtma` bola class'larini yarating va `Mahsulot::topish(5)` qaysi class obyektini va qaysi jadval nomini berishini ko'rsating.

<details markdown="1">
<summary>Yechim — 10 (Shakl factory + new static)</summary>

```php
<?php
abstract class Shakl {
    public static function yarat(): static {
        return new static();      // aktual class obyektini yaratadi
    }
    abstract public function nomi(): string;
}

class Doira extends Shakl {
    public function nomi(): string { return "Doira"; }
}

class Kvadrat extends Shakl {
    public function nomi(): string { return "Kvadrat"; }
}

echo Doira::yarat()->nomi();     // Doira
echo "<br>";
echo Kvadrat::yarat()->nomi();   // Kvadrat
```
`yarat()` faqat bir marta (ota class'da) yozilgan, lekin `new static()` tufayli `Doira::yarat()` Doira obyektini, `Kvadrat::yarat()` Kvadrat obyektini qaytaradi. Agar `new self()` bo'lganida, abstract class'ni yaratishga urinib xato berardi. Bu — bitta factory metodni hamma bola class'lar uchun qayta ishlatishning kuchi.
</details>

<details markdown="1">
<summary>Yechim — 11 (ID generator)</summary>

```php
<?php
class IDgenerator {
    public static int $oxirgiId = 0;

    public static function yangiId(): int {
        self::$oxirgiId++;        // umumiy hisobni oshiramiz
        return self::$oxirgiId;
    }
}

echo IDgenerator::yangiId();   // 1
echo "<br>";
echo IDgenerator::yangiId();   // 2
echo "<br>";
echo IDgenerator::yangiId();   // 3
```
Static bo'lgani uchun `$oxirgiId` bitta va saqlanib turadi — har chaqiruvda davom etadi. Bu obyektga bog'liq bo'lmagan, "umumiy hisoblagich" uchun ajoyib misol. E'tibor bering: xususiyatni `int` deb, metodni `: int` deb tipladik — zamonaviy uslub.
</details>

<details markdown="1">
<summary>Yechim — 12 (Foydalanuvchilar ro'yxati)</summary>

```php
<?php
class Foydalanuvchi {
    public static array $royxat = [];   // barcha foydalanuvchilar — butun class'ga umumiy

    // PHP 8.4: constructor promotion — $ism ni darrov xususiyatga aylantiradi
    public function __construct(public string $ism) {
        self::$royxat[] = $ism;    // o'zini umumiy ro'yxatga qo'shadi
    }

    public static function hammasi(): array {
        return self::$royxat;
    }
}

new Foydalanuvchi("Ali");
new Foydalanuvchi("Vali");
new Foydalanuvchi("Guli");

print_r(Foydalanuvchi::hammasi());   // ["Ali", "Vali", "Guli"]
```
`$royxat` static — u bitta va barcha obyektlar uchun umumiy. Har bir yangi foydalanuvchi konstruktorda `self::$royxat`ga qo'shiladi, shuning uchun `hammasi()` to'liq ro'yxatni beradi. `self::` — "shu class'ning static a'zosi" (obyektda `$this`, static'da `self`). Konstruktorda `public string $ism` yozish (constructor promotion) `$this->ism = $ism;` qatorini avtomatik bajaradi — qisqa va aniq.
</details>

<details markdown="1">
<summary>Yechim — 13 (Statistika vositalari)</summary>

```php
<?php
class Statistika {
    public static function engKatta(array $sonlar): int|float {
        return max($sonlar);
    }
    public static function engKichik(array $sonlar): int|float {
        return min($sonlar);
    }
    public static function ortacha(array $sonlar): float {
        return array_sum($sonlar) / count($sonlar);
    }
}

$ballar = [85, 90, 70, 95, 60];

echo "Eng katta: "  . Statistika::engKatta($ballar)  . "<br>";   // 95
echo "Eng kichik: " . Statistika::engKichik($ballar) . "<br>";   // 60
echo "O'rtacha: "   . Statistika::ortacha($ballar);              // 80
```
Bu metodlar hech qaysi obyektga bog'liq emas — ular shunchaki "vosita". Shuning uchun static: obyekt yaratmasdan, `Statistika::ortacha(...)` deb to'g'ridan-to'g'ri ishlatamiz. Bu — "yordamchi funksiyalar to'plami" uchun mos naqsh. Argument va qaytarish tiplarini ko'rsatish kodni xatolardan himoya qiladi.
</details>

<details markdown="1">
<summary>Yechim — 14 (self vs static)</summary>

```php
<?php
class Asosiy {
    public static function kim(): string {
        return "Asosiy";
    }
    public static function selfChaqir(): string {
        return self::kim();      // qattiq Asosiy'ga bog'langan
    }
    public static function staticChaqir(): string {
        return static::kim();    // aktual class'ni topadi
    }
}

class Bola extends Asosiy {
    public static function kim(): string {
        return "Bola";           // ota metodni qayta yozdik
    }
}

echo Bola::selfChaqir();     // "Asosiy" — self e'lon qilingan joyni (Asosiy) oladi
echo "<br>";
echo Bola::staticChaqir();   // "Bola"   — static aktual class (Bola) ni oladi
```
`selfChaqir()` ichidagi `self::kim()` doim Asosiy'ning `kim()`ini chaqiradi, chunki `self` "kod yozilgan class"ga qattiq bog'langan. `staticChaqir()` ichidagi `static::kim()` esa "kim chaqirgan bo'lsa, o'shaning" `kim()`ini chaqiradi — biz `Bola::staticChaqir()` deganimiz uchun Bola'niki ishlaydi. Mana shu — Late Static Binding: bola class metodni qayta yozsa va siz eng so'nggi versiyani xohlasangiz, `static::` ishlatishingiz kerak.
</details>

<details markdown="1">
<summary>Yechim — 15 (Factory + LSB: Model)</summary>

```php
<?php
class Model {
    public function __construct(public int $id) {}   // constructor promotion

    public static function topish(int $id): static {
        return new static($id);          // aktual class obyekti
    }

    public function jadval(): string {
        return strtolower(static::class) . "lar";   // static::class -> aktual class nomi
    }
}

class Mahsulot extends Model {}
class Buyurtma extends Model {}

$p = Mahsulot::topish(5);
echo get_class($p) . " #" . $p->id . " -> " . $p->jadval() . "<br>";
// Mahsulot #5 -> mahsulotlar

$o = Buyurtma::topish(9);
echo get_class($o) . " #" . $o->id . " -> " . $o->jadval();
// Buyurtma #9 -> buyurtmalar
```
`topish()` faqat bir marta (Model'da) yozilgan, ammo `new static($id)` tufayli `Mahsulot::topish(5)` Mahsulot obyektini, `Buyurtma::topish(9)` Buyurtma obyektini beradi. `static::class` esa aktual class nomini matn sifatida qaytaradi — shuning uchun `jadval()` har bir class uchun to'g'ri nom (`mahsulotlar`, `buyurtmalar`) hosil qiladi. Mana shunday yondashuv haqiqiy ORM kutubxonalarida (masalan Laravel'ning Eloquent'ida) `User::find(1)` kabi metodlar ortida turadi.
</details>
