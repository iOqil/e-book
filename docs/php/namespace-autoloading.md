# 2.12 Namespace va autoloading

[⬅️ Oldingi: 2.11 Magic metodlar](./magic-metodlar.md) · [🏠 README](./README.md) · [Keyingi: 3.1 Ma'lumotlar bazasi nima va nega kerak? ➡️](./24-malumotlar-bazasi-nima-va-nega-kerak.md)

---

Loyihangiz o'sib boradi: bugun 5 ta class, ertaga 50 ta, keyin 500 ta. Va shu yerda ikkita og'riq paydo bo'ladi.

**Birinchisi — nomlar to'qnashuvi.** Siz `User` degan class yozdingiz. Tashqi kutubxonada ham `User` bor. Ikkalasini bitta loyihada ishlatmoqchisiz — PHP "Cannot redeclare class User" deb baqiradi. Bitta loyihada bir xil nomli ikkita class yashay olmaydi.

**Ikkinchisi — qo'lda yuklash azobi.** Har bir class alohida faylda. Har birini ishlatishdan oldin `require 'fayl.php'` yozish kerak. 50 ta class — index.php boshida 50 qator `require`. Bittasini unutsangiz — "Class not found" xatosi. Birini ko'chirsangiz — barcha yo'llarni qayta yozasiz.

**Namespace** birinchi muammoni hal qiladi — class'larni "papkalarga" ajratib, bir xil nomlilar yonma-yon yashashiga imkon beradi. **Autoloading** ikkinchisini hal qiladi — class kerak bo'lganda PHP uni avtomatik topib yuklaydi, siz `require` yozmaysiz. Ushbu bobda ikkalasini ham, va ularni birlashtirgan zamonaviy standart — **PSR-4** ni o'rganamiz.

### Muammoni ko'ramiz: nomlar to'qnashuvi

Tasavvur qiling, loyihangizda foydalanuvchini bildiradigan `User` class bor. Bir vaqtning o'zida to'lov kutubxonasida ham `User` bor (ularning "user" tushunchasi — boshqacha). Ikkalasini bitta faylga qo'shsangiz:

```php
<?php
class User {            // sizniki
    public string $ism = "Ali";
}

class User {            // ❌ Fatal error: Cannot redeclare class User
    public string $karta = "1234";
}
```

PHP ishga tushmaydi. Sabab oddiy: global "maydonda" `User` degan nom faqat bittaga tegishli bo'la oladi. Ikkita kishi bir uyda bir xil ismda yashayolmaydi — kimligini ajratib bo'lmaydi.

Yechim — har bir `User` ni o'z "papkasi"ga joylash. Aynan shuni **namespace** qiladi.

### Namespace e'lon qilish — `namespace`

**Namespace (nom fazosi) — class, funksiya va konstantalarni mantiqiy guruhlarga ajratuvchi "nomli konteyner".** Uni faylning eng boshida, `namespace` kalit so'zi bilan e'lon qilasiz:

```php
<?php
namespace App\Models;

class User {
    public function __construct(
        public string $ism
    ) {}
}
```

Endi bu `User` ning "to'liq nomi" — `App\Models\User`. U boshqa namespace'dagi `User` bilan to'qnashmaydi, chunki ular boshqa-boshqa "papkalarda".

Muhim qoidalar:

- `namespace` e'loni faylning **eng birinchi** kod qatori bo'lishi shart (`<?php` dan keyin, har qanday boshqa koddan oldin).
- `\` (backslash) — namespace bo'laklarini ajratuvchi belgi. `App\Models` — "App ichidagi Models".
- Odatda **bir faylga bitta** namespace va bitta class joylanadi (bu PSR-4 standarti talabi — pastda ko'ramiz).

### To'liq malakali nom (Fully Qualified Name)

Namespace'dagi class'ni boshqa joydan ishlatish uchun uning **to'liq nomini** yozasiz — `\` bilan boshlab, butun yo'lni:

```php
<?php
// 1-fayl: User class App\Models namespace'ida e'lon qilingan deb hisoblaymiz

$u = new \App\Models\User("Ali");
echo $u->ism;   // Ali
```

`\App\Models\User` — bu **to'liq malakali nom** (fully qualified name, FQN). Boshidagi `\` "global ildizdan boshla" degani — xuddi fayl tizimidagi `/home/user` kabi mutlaq yo'l. Bu nom aniq, lekin uzun. Har safar to'liq yozish charchatadi. Shu sababli **`use`** bor.

### Import qilish — `use`

`use` — namespace'dan biror class'ni joriy faylga "olib kirish" (import). Shundan keyin uni qisqa nomi bilan ishlatasiz:

```php
<?php
namespace App\Controllers;

use App\Models\User;   // App\Models\User ni import qildik

class UserController {
    public function yarat(): User {       // endi qisqa "User" yetarli
        return new User("Ali");
    }
}
```

`use App\Models\User;` dan keyin shu faylda har qanday `User` — aynan `App\Models\User` ni bildiradi. To'liq yo'lni qayta-qayta yozish shart emas.

> **Diqqat:** `use` da nom boshida `\` **yozilmaydi** (`use App\Models\User`, `use \App\Models\User` emas). `use` doim global ildizdan boshlaydi, shuning uchun boshlang'ich `\` ortiqcha.

### Alias berish — `use ... as`

Ikki xil namespace'dan bir xil nomli class'larni import qilsangiz, baribir to'qnashuv bo'ladi. **`as`** — import qilingan nomga taxallus (alias) berib, shu muammoni hal qiladi:

```php
<?php
namespace App\Services;

use App\Models\User;            // bizning User
use Payment\Models\User as PaymentUser;   // to'lov kutubxonasi User'i — boshqa nom bilan

class CheckoutService {
    public function ishla(): string {
        $bizniki = new User("Ali");
        $tolov   = new PaymentUser("1234-5678");
        return $bizniki->ism;
    }
}
```

Endi `User` — bizning class, `PaymentUser` — kutubxonaniki. Ikkalasi yonma-yon, hech qanday to'qnashuvsiz. `as` ayniqsa uzun yoki noqulay class nomini qisqartirishda ham foydali: `use Some\Very\Long\Namespace\ReportGenerator as Report;`.

### Global namespace — boshidagi `\`

Siz namespace ichida bo'lganingizda, PHP'ning o'rnatilgan class va funksiyalari (`Exception`, `DateTime`, `strlen` ...) "global namespace"da turadi. Namespace ichidan ularga murojaat qilganda boshiga `\` qo'yiladi:

```php
<?php
namespace App\Services;

class DateService {
    public function hozir(): string {
        // \DateTime — global namespace'dagi PHP class'i.
        // Agar \ qo'ymasak, PHP App\Services\DateTime ni qidiradi va topmaydi!
        $sana = new \DateTime();
        return $sana->format("Y-m-d");
    }
}

$s = new DateService();
echo $s->hozir();   // masalan: 2026-06-11
```

Sabab: namespace ichida `new DateTime()` deyilsa, PHP avval **joriy namespace'da** (`App\Services\DateTime`) qidiradi, topmasa xato beradi. Boshiga `\` qo'yib (`new \DateTime()`), "global ildizdan ol" deysiz.

> **Maslahat:** Funksiyalar uchun (`strlen`, `count` ...) PHP avtomatik global'ga "tushib" qidiradi, shuning uchun ularda `\` ko'pincha shart emas. Lekin **class'larda** har doim `\` kerak yoki yuqorida `use \DateTime;` qiling.

### Bir faylda bir nechta namespace (va nega bunday qilinmaydi)

Texnik jihatdan bitta faylda bir nechta namespace e'lon qilish mumkin, lekin buning uchun jingalak qavs `{ }` sintaksisi ishlatiladi:

```php
<?php
namespace App\Models {
    class Product {
        public function __construct(public string $nom) {}
    }
}

namespace App\Services {
    class Cart {
        public function qosh(\App\Models\Product $p): string {
            return $p->nom;
        }
    }
}

namespace {   // nomsiz blok — global namespace
    $p = new \App\Models\Product("Kitob");
    $c = new \App\Services\Cart();
    echo $c->qosh($p);   // Kitob
}
```

**Lekin amalda bunday qilinmaydi.** Standart (va PSR-4) qoidasi: **bir fayl — bitta namespace, bitta class.** Yuqoridagi shakl faqat texnik imkoniyatni ko'rsatish uchun. Haqiqiy loyihada har bir class o'z faylida, fayl boshida bitta `namespace` bilan turadi.

### Endi ikkinchi muammo: qo'lda `require` azobi

Namespace nomlar muammosini hal qildi. Lekin class'lar baribir alohida fayllarda, va har birini ishlatishdan oldin yuklash kerak. Hozircha buni `require` bilan qilamiz:

```php
<?php
require 'src/Models/User.php';
require 'src/Models/Product.php';
require 'src/Services/Cart.php';
require 'src/Services/Checkout.php';
// ... yana 40 ta require ...

use App\Models\User;

$u = new User("Ali");
```

Loyiha kattalashgani sayin bu ro'yxat cheksiz o'sadi. Birini unutsangiz — "Class not found". Faylni boshqa papkaga ko'chirsangiz — yo'lni hamma joyda tuzatasiz. **Autoloading** ana shu azobni butunlay yo'q qiladi.

### Autoloading nima?

**Autoloading (avtomatik yuklash) — class birinchi marta ishlatilganda PHP uni o'zi topib, faylini yuklash mexanizmi.** Ya'ni siz `new User()` deysiz, PHP "User class hali yuklanmagan-ku" deb sezadi va sahna ortida kerakli faylni topib ulaydi. Sizning `require` yozishingiz shart emas.

Buning siri — **`spl_autoload_register`** funksiyasi. Unga "qaysidir class kerak bo'lganda nima qilish kerakligini" tushuntiruvchi funksiya berasiz, PHP esa har "topilmagan class" holatida o'sha funksiyani chaqiradi.

### Qo'lda autoloader yozish — `spl_autoload_register`

Eng oddiy autoloader — class nomini fayl yo'liga aylantiradigan funksiya:

```php
<?php
spl_autoload_register(function (string $class): void {
    // $class — to'liq class nomi, masalan "Models\User"
    $fayl = __DIR__ . "/" . $class . ".php";

    if (file_exists($fayl)) {
        require $fayl;
        echo "[autoload] yuklandi: {$fayl}\n";
    }
});

// Bu nuqtada hech narsa require qilinmagan.
// Quyida class'ga murojaat qilamiz — PHP avtomatik yuklaydi:
$u = new \Models\User("Ali");
echo $u->ism;
```

Mexanizm:

1. PHP `\Models\User` ga duch keladi, lekin u hali yuklanmagan.
2. PHP ro'yxatdan o'tgan autoloader funksiyani chaqiradi va unga `"Models\User"` nomini beradi.
3. Funksiya bu nomdan fayl yo'lini yasaydi (`__DIR__/Models\User.php`) va `require` qiladi.
4. Class endi mavjud — PHP ishni davom ettiradi.

`__DIR__` — joriy fayl turgan papkaning to'liq yo'li (sehrli konstanta, 2.11-bobda ko'rgansiz). Bir vaqtda **bir nechta** autoloader ro'yxatga olish ham mumkin — PHP ularni navbat bilan sinab ko'radi.

> **`\` va papka belgisi:** namespace'da ajratgich `\`, fayl yo'lida esa `/`. Shu sababli real autoloaderda `\` ni `/` ga almashtirish kerak bo'ladi — buni quyidagi PSR-4 misolda ko'ramiz.

### PSR-4 standarti — namespace va papka tuzilishi mosligi

Har kim o'z autoloaderini o'zicha yozsa, har loyiha boshqacha bo'lardi. Shu sababli PHP hamjamiyati **PSR-4** degan standartni kelishib oldi. (PSR — "PHP Standard Recommendation", PHP standart tavsiyasi.)

**PSR-4 ning asosiy g'oyasi: namespace tuzilishi papka tuzilishini aks ettiradi.** Ya'ni:

- `App\Models\User` class → `src/Models/User.php` faylida
- `App\Services\Cart` class → `src/Services/Cart.php` faylida
- namespace'dagi `\` → papkadagi `/`
- class nomi → fayl nomi (`.php` bilan)

Bu yerda `App\` "namespace prefiksi" `src/` "asosiy papka"ga bog'langan. Prefiksdan keyingi qism aynan papka yo'liga aylanadi. Mana PSR-4 ga mos autoloader:

```php
<?php
spl_autoload_register(function (string $class): void {
    $prefiks   = "App\\";        // shu prefiks bilan boshlanadigan class'lar
    $asosiyDir = __DIR__ . "/src/";  // shu papkada turadi

    // class shu prefiks bilan boshlanmasa — bu autoloaderga tegishli emas
    if (!str_starts_with($class, $prefiks)) {
        return;
    }

    // Prefiksni olib tashlaymiz: "App\Models\User" -> "Models\User"
    $nisbiy = substr($class, strlen($prefiks));

    // \ -> / ga almashtirib, fayl yo'lini yasaymiz
    $fayl = $asosiyDir . str_replace("\\", "/", $nisbiy) . ".php";

    if (file_exists($fayl)) {
        require $fayl;
    }
});
```

Endi `new App\Models\User()` deganda autoloader avtomatik `src/Models/User.php` ni topib yuklaydi. Class qaysi papkada ekanini uning nomidan **aniq bilib olish mumkin** — bu loyihada yo'l topishni ulkan darajada osonlashtiradi.

### Composer autoload — standartni avtomatlashtirish

Yaxshi xabar: PSR-4 autoloaderni qo'lda yozish ham shart emas. **Composer** (5.4-bobda ko'rgansiz — PHP kutubxonalar menejeri) buni siz uchun avtomatik yasaydi. Sizga faqat `composer.json` da qaysi prefiks qaysi papkaga mosligini aytish kifoya:

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

Bu sozlama: "`App\` bilan boshlanadigan har qanday class `src/` papkada". So'ng terminalda:

```bash
composer dump-autoload
```

Bu buyruq `vendor/autoload.php` faylini (yoki yangilab) yasaydi — ichida tayyor, optimallashtirilgan PSR-4 autoloader. Endi loyihangizning kirish faylida faqat bitta qator:

```php
<?php
require 'vendor/autoload.php';   // bitta qator — barcha class'lar avtomatik yuklanadi

use App\Models\User;

$u = new User("Ali");   // src/Models/User.php avtomatik yuklandi
```

`composer require` bilan tashqi kutubxona o'rnatganingizda ham aynan shu `vendor/autoload.php` o'sha kutubxona class'larini ham yuklaydi. Ya'ni bitta `require` — ham sizning, ham tashqi kod uchun. Bu — Laravel, Symfony va deyarli barcha zamonaviy PHP loyihalarining poydevori.

> **Eslatma:** `composer dump-autoload` ni faqat yangi class/papka qo'shganda yoki `composer.json` ning `autoload` qismini o'zgartirganda qayta ishga tushirasiz. Composer mavjud bo'lganda bu — PSR-4 ni qo'lda yozishdan ko'ra ishonchli va tezroq yo'l.

### Real misol: kichik loyiha tuzilishi (App\ + PSR-4 + Composer)

Endi hamma narsani birlashtiramiz. Mana kichik "do'kon" loyihasining tuzilishi:

```
dokon/
├── composer.json
├── index.php
└── src/
    ├── Models/
    │   ├── Product.php
    │   └── User.php
    └── Services/
        └── Cart.php
```

**composer.json** — autoload sozlamasi:

```json
{
    "name": "men/dokon",
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

**src/Models/Product.php** — `App\Models\Product`:

```php
<?php
namespace App\Models;

class Product {
    public function __construct(
        public readonly string $nom,
        public readonly float $narx,
    ) {}
}
```

**src/Models/User.php** — `App\Models\User`:

```php
<?php
namespace App\Models;

class User {
    public function __construct(
        public readonly string $ism,
    ) {}
}
```

**src/Services/Cart.php** — `App\Services\Cart` (e'tibor bering: u `Product` ni `use` bilan import qiladi):

```php
<?php
namespace App\Services;

use App\Models\Product;

class Cart {
    /** @var Product[] */
    private array $mahsulotlar = [];

    public function qosh(Product $p): void {
        $this->mahsulotlar[] = $p;
    }

    public function jami(): float {
        $summa = 0.0;
        foreach ($this->mahsulotlar as $p) {
            $summa += $p->narx;
        }
        return $summa;
    }
}
```

**index.php** — hammasini ulaydi, lekin bironta ham qo'lda `require` yo'q:

```php
<?php
require 'vendor/autoload.php';   // yagona require — autoload hammasini hal qiladi

use App\Models\User;
use App\Models\Product;
use App\Services\Cart;

$xaridor = new User("Ali");

$savat = new Cart();
$savat->qosh(new Product("Kitob", 50000));
$savat->qosh(new Product("Ruchka", 5000));

echo "Xaridor: {$xaridor->ism}\n";
echo "Jami: " . number_format($savat->jami(), 0, ".", " ") . " so'm\n";
```

Loyihani ishga tushirish uchun bir marta `composer dump-autoload`, so'ng `php index.php`. Natija:

```
Xaridor: Ali
Jami: 55 000 so'm
```

E'tibor bering: `index.php` da na `Product.php`, na `User.php`, na `Cart.php` qo'lda yuklandi. Har bir class birinchi ishlatilganda PSR-4 autoloader uni o'z papkasidan avtomatik topdi. 3 ta class ham, 300 ta class ham — kirish fayli baribir bitta `require 'vendor/autoload.php'` bilan cheklanadi. Aynan shu — professional PHP loyihasining tuzilishi.

> Bu tuzilish to'g'ridan-to'g'ri 5.4 (Composer) boboga ulanadi: o'sha yerda tashqi kutubxonalarni `composer require` bilan o'rnatishni ko'rasiz — ular ham aynan shu `vendor/autoload.php` orqali yuklanadi. Namespace + PSR-4 + Composer — uchligi zamonaviy PHP ning poydevori.

### Mashqlar

**Oson**

1. `App\Models` namespace'ida `Book` degan class e'lon qiling (bitta `nom` xususiyati bilan). Uning to'liq malakali nomi qanday bo'ladi?
2. Boshqa faylda `App\Models\Book` ni `use` bilan import qiling va obyekt yarating.
3. Namespace ichida PHP'ning `\DateTime` class'idan obyekt yarating. Nega boshiga `\` qo'yish kerakligini izohlang.
4. `use App\Models\Book;` da `Book` ning oldiga `\` qo'yiladimi? Javobingizni asoslang.

**O'rta**

5. Ikkita turli namespace'dan (`App\Models\User` va `Auth\User`) bir xil nomli class'ni bitta faylda ishlatishingiz kerak. `as` bilan to'qnashuvni hal qiling.
6. `App\Services\Mailer` class'i ichida `App\Models\User` ni `use` qilib, konstruktorda uni parametr sifatida qabul qiling (`function __construct(User $u)`).
7. `spl_autoload_register` bilan oddiy autoloader yozing: class nomini olib, shu nomdagi `.php` faylni joriy papkadan `require` qilsin.
8. 7-mashqdagi autoloaderni PSR-4 uslubiga o'tkazing: faqat `App\` prefiksli class'larni `src/` papkadan yuklasin, `\` ni `/` ga almashtirsin.

**Qiyin**

9. PSR-4 ga mos papka tuzilishi tuzing: `App\Models\Order` class `qaysi faylda` turishi kerak? `App\Services\Payment\Stripe` esa? (Faqat yo'llarni yozing.)
10. Quyidagi `composer.json` ni to'ldiring: `Shop\` prefiksi `app/` papkaga mos kelsin. Keyin qaysi terminal buyrug'i autoloaderni yangilashini ayting.
11. Kichik mini-loyiha tuzing: `src/Models/Task.php` (`App\Models\Task`, `nom` va `bajarildi` xususiyatlari) va `src/Services/TaskList.php` (`App\Services\TaskList`, vazifa qo'shish va sanash metodlari). `index.php` da faqat bitta `require 'vendor/autoload.php'` bilan ikkalasini ham ishlating.
12. Tasavvur qiling, Composer yo'q (uni o'rnatib bo'lmaydi). 11-mashqdagi loyihani **qo'lda yozilgan** PSR-4 autoloader (`spl_autoload_register`) bilan ishga tushiring — `vendor/autoload.php` o'rniga o'z autoloader faylingizni ulang.

<details markdown="1">
<summary>Yechim — 5 (alias bilan to'qnashuvni hal qilish)</summary>

```php
<?php
namespace App\Controllers;

use App\Models\User;          // bizning User
use Auth\User as AuthUser;    // tashqi User — boshqa nom bilan

class LoginController {
    public function ishla(): string {
        $foydalanuvchi = new User("Ali");        // App\Models\User
        $autentifikator = new AuthUser("token"); // Auth\User
        return $foydalanuvchi->ism ?? "?";
    }
}
```

`as` bo'lmaganda PHP "Cannot use Auth\User as User because the name is already in use" deb xato berardi. `as AuthUser` ikkinchi class'ga shu faylda boshqa nom berdi — endi ikkalasi tinch yashaydi.
</details>

<details markdown="1">
<summary>Yechim — 7 (oddiy spl_autoload_register)</summary>

```php
<?php
spl_autoload_register(function (string $class): void {
    $fayl = __DIR__ . "/" . $class . ".php";
    if (file_exists($fayl)) {
        require $fayl;
    }
});

// Endi qo'lda require'siz:
$obj = new Hisoblagich();   // Hisoblagich.php avtomatik yuklanadi
```

PHP `Hisoblagich` ni topa olmaganda, ro'yxatdagi funksiyani chaqiradi, u esa `Hisoblagich.php` ni topib `require` qiladi. Namespace ishlatilsa, `$class` ichida `\` bo'ladi — buni keyingi mashqda hal qilamiz.
</details>

<details markdown="1">
<summary>Yechim — 8 (PSR-4 autoloader)</summary>

```php
<?php
spl_autoload_register(function (string $class): void {
    $prefiks   = "App\\";
    $asosiyDir = __DIR__ . "/src/";

    if (!str_starts_with($class, $prefiks)) {
        return;   // bizning prefiksimiz emas — boshqa autoloaderga qoldiramiz
    }

    $nisbiy = substr($class, strlen($prefiks));          // "Models\User"
    $fayl   = $asosiyDir . str_replace("\\", "/", $nisbiy) . ".php";

    if (file_exists($fayl)) {
        require $fayl;
    }
});

$u = new App\Models\User("Ali");   // src/Models/User.php avtomatik yuklanadi
```

Uchta qadam: (1) prefiksni tekshir, (2) prefiksdan keyingi qismni `substr` bilan ol, (3) `\` ni `/` ga almashtirib fayl yo'lini yasab `require` qil. Composer ham aynan shu mantiqni ishlatadi — faqat optimallashtirilgan.
</details>

<details markdown="1">
<summary>Yechim — 9 (PSR-4 yo'llari)</summary>

`App\` prefiksi `src/` ga mos deb hisoblasak:

- `App\Models\Order` → `src/Models/Order.php`
- `App\Services\Payment\Stripe` → `src/Services/Payment/Stripe.php`

Qoida: prefiksdan keyingi har bir `\` — papka, oxirgi bo'lak — fayl nomi (`.php` bilan). Namespace tuzilishini ko'rib, class qaysi faylda ekanini darrov bilib olasiz.
</details>

<details markdown="1">
<summary>Yechim — 10 (composer.json)</summary>

```json
{
    "autoload": {
        "psr-4": {
            "Shop\\": "app/"
        }
    }
}
```

JSON ichida `\` ni ikki marta yozish kerak (`Shop\\`), chunki JSON'da `\` — maxsus belgi. So'ng autoloaderni yangilash buyrug'i:

```bash
composer dump-autoload
```

Bu `vendor/autoload.php` ni `Shop\` → `app/` mosligi bilan qayta yasaydi.
</details>

<details markdown="1">
<summary>Yechim — 11 (Composer bilan mini-loyiha)</summary>

**composer.json:**
```json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

**src/Models/Task.php:**
```php
<?php
namespace App\Models;

class Task {
    public function __construct(
        public string $nom,
        public bool $bajarildi = false,
    ) {}
}
```

**src/Services/TaskList.php:**
```php
<?php
namespace App\Services;

use App\Models\Task;

class TaskList {
    /** @var Task[] */
    private array $vazifalar = [];

    public function qosh(Task $t): void {
        $this->vazifalar[] = $t;
    }

    public function soni(): int {
        return count($this->vazifalar);
    }
}
```

**index.php:**
```php
<?php
require 'vendor/autoload.php';

use App\Models\Task;
use App\Services\TaskList;

$royxat = new TaskList();
$royxat->qosh(new Task("PHP o'rganish"));
$royxat->qosh(new Task("Mashq qilish", bajarildi: true));

echo "Vazifalar soni: " . $royxat->soni();   // Vazifalar soni: 2
```

Ishga tushirish: `composer dump-autoload`, so'ng `php index.php`. Bironta qo'lda `require` yo'q — PSR-4 autoloader ikkala class'ni ham o'z papkasidan topadi.
</details>

<details markdown="1">
<summary>Yechim — 12 (Composer'siz, qo'lda PSR-4 autoloader)</summary>

Composer bo'lmasa, `vendor/autoload.php` o'rniga o'z autoloaderimizni yozamiz. Class fayllari (Task, TaskList) 11-mashqdagidek qoladi — faqat `index.php` o'zgaradi:

**autoload.php** (o'zimizning):
```php
<?php
spl_autoload_register(function (string $class): void {
    $prefiks   = "App\\";
    $asosiyDir = __DIR__ . "/src/";

    if (!str_starts_with($class, $prefiks)) {
        return;
    }

    $fayl = $asosiyDir
          . str_replace("\\", "/", substr($class, strlen($prefiks)))
          . ".php";

    if (file_exists($fayl)) {
        require $fayl;
    }
});
```

**index.php:**
```php
<?php
require 'autoload.php';   // Composer o'rniga o'z autoloaderimiz

use App\Models\Task;
use App\Services\TaskList;

$royxat = new TaskList();
$royxat->qosh(new Task("Composer'siz ishladi"));
echo "Soni: " . $royxat->soni();   // Soni: 1
```

Natija aynan bir xil. Bu shuni ko'rsatadi: Composer'ning `vendor/autoload.php` — sehr emas, balki aynan shunday PSR-4 autoloaderning optimallashtirilgan ko'rinishi. Composer bor joyda uni ishlatasiz; bo'lmaganda — bu 15 qatorlik funksiya ham yetarli.
</details>
