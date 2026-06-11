# 5.5 Testing (PHPUnit)

[⬅️ Oldingi: 5.4 Composer — tashqi kutubxonalar](./39-composer-tashqi-kutubxonalar.md) · [🏠 README](./README.md) · [Keyingi: 6-QISM — Keyingi qadamlar ➡️](./40-keyingi-qadamlar.md)

---

Tasavvur qiling: siz katta loyiha yozdingiz — yuzlab funksiya, o'nlab class. Bugun bitta funksiyaga kichik o'zgartirish kiritdingiz. Savol: shu o'zgartirish loyihaning **boshqa joyini buzib qo'ymadimi**? Buni qanday bilasiz?

Eng oddiy yo'l — qo'lda tekshirish: brauzerni ochib, har bir sahifani bosib, har bir holatni sinab ko'rish. Loyiha kichik bo'lsa, mayli. Lekin loyiha o'sgani sayin bu **azobga** aylanadi: har bir o'zgarishdan keyin 50 ta narsani qo'lda qayta tekshirish — soatlab vaqt va baribir biror narsani o'tkazib yuborasiz.

Yechim — **avtomatik test** (automated test, ya'ni kodni tekshiradigan kod). Bir marta yozasiz, keyin bitta buyruq bilan butun loyihani soniyalar ichida tekshirasiz. Bu bobda PHP olamining standart test vositasi — **PHPUnit** bilan tanishamiz.

### Nega test yozish kerak?

Test yozish — ortiqcha ish emas, balki **vaqtni tejaydigan sarmoya**. Asosiy foydalari:

- **Refactoring (qayta tuzish) xavfsizligi.** Kodni yaxshilamoqchisiz, lekin "buzib qo'ysamchi" degan qo'rquv to'sqinlik qiladi. Testlar bo'lsa — bemalol o'zgartirasiz: agar biror narsa buzilsa, test darrov "qizil" bo'lib aytib beradi.
- **Tirik hujjat.** Yaxshi yozilgan test funksiya **qanday ishlashi kerakligini** ko'rsatadi. Kodni o'qigan odam testga qarab "aha, bu funksiya shunaqa ishlar ekan" deb tushunadi.
- **Ishonch.** "Mening kodim ishlaydi" deyish — yaxshi. "Mening kodim ishlaydi, mana 50 ta test buni isbotlaydi" deyish — professional.
- **Xatoni erta topish.** Test xatoni siz emas, kompyuter topadi — foydalanuvchidan oldin.

> Tajribali jamoalarda qoida oddiy: yangi funksiya yozsang — testi ham bo'lsin. Xato topilsa — avval shu xatoni ushlaydigan test yoz, keyin tuzat. Shunda xato **ikkinchi marta qaytmaydi**.

### PHPUnit'ni o'rnatish

PHPUnit — tashqi kutubxona, uni Composer (5.4) bilan o'rnatamiz. U faqat ishlab chiqish (development) paytida kerak, foydalanuvchiga ketadigan kodda emas. Shuning uchun `--dev` bayrog'i bilan o'rnatamiz:

```bash
composer require --dev phpunit/phpunit
```

Bu buyruq PHPUnit'ni `vendor/` papkaga yuklaydi va `composer.json` faylida shunday yozadi:

```json
{
    "require-dev": {
        "phpunit/phpunit": "^12.5"
    }
}
```

`require-dev` — "bu kutubxona faqat ishlab chiqishda kerak" degani (test vositasini serverda ishga tushirmaysiz). O'rnatilgandan keyin PHPUnit buyrug'i `vendor/bin/phpunit` da turadi.

### Birinchi test: sinaladigan class

Test yozish uchun avval **sinaladigan kod** kerak. Oddiy `Kalkulyator` class'ini olaylik (`src/Kalkulyator.php`):

```php
<?php

class Kalkulyator
{
    public function qosh(int $a, int $b): int
    {
        return $a + $b;
    }

    public function ayir(int $a, int $b): int
    {
        return $a - $b;
    }

    public function bol(int $a, int $b): float
    {
        if ($b === 0) {
            throw new InvalidArgumentException("Nolga bo'lib bo'lmaydi");
        }

        return $a / $b;
    }
}
```

E'tibor bering: parametrlar va qaytaruv qiymati **tiplangan** (`int $a`, `: int`) — zamonaviy PHP uslubi. Endi shu class uchun test yozamiz.

### Test class va test metodi

Test odatda alohida papkada (`tests/`) turadi. Har bir sinaladigan class uchun bitta test class yoziladi. Qoidalar oddiy:

1. Test class `PHPUnit\Framework\TestCase` dan **voris** (1.16) bo'ladi.
2. Test metodlari `public` bo'ladi va nomi `test` bilan boshlanadi (yoki `#[Test]` atributi bilan belgilanadi — pastda ko'ramiz).
3. Metod ichida **assert** (tasdiqlash) funksiyasi bilan natijani tekshirasiz.

Mana `tests/KalkulyatorTest.php`:

```php
<?php

use PHPUnit\Framework\TestCase;

require_once __DIR__ . '/../src/Kalkulyator.php';

class KalkulyatorTest extends TestCase
{
    public function testQoshIkkitaSonniQoshadi(): void
    {
        $kalkulyator = new Kalkulyator();

        $natija = $kalkulyator->qosh(2, 3);

        $this->assertEquals(5, $natija);
    }
}
```

Nima bo'lyapti:
- `KalkulyatorTest extends TestCase` — test class TestCase'dan voris bo'lib, barcha assert metodlarini meros qilib oladi.
- `testQoshIkkitaSonniQoshadi` — metod nomi `test` bilan boshlangani uchun PHPUnit uni **test** deb taniydi.
- `$this->assertEquals(5, $natija)` — "kutgan natijam 5, haqiqiy natija `$natija` bo'lsin; agar teng bo'lmasa — test yiqiladi".

### Testni ishga tushirish — `vendor/bin/phpunit`

Test yozildi, endi ishga tushiramiz. Terminalda loyiha papkasida:

```bash
vendor/bin/phpunit tests
```

(Windows'da `vendor\bin\phpunit tests`.) Hammasi joyida bo'lsa, natija yashil bo'ladi:

```
PHPUnit 12.5.29 by Sebastian Bergmann and contributors.

Runtime:       PHP 8.4.0

.                                                                   1 / 1 (100%)

Time: 00:00.008, Memory: 6.00 MB

OK (1 test, 1 assertion)
```

Har bir nuqta (`.`) — bitta o'tgan test. `OK (1 test, 1 assertion)` — hammasi yashil. Agar test yiqilsa, nuqta o'rniga `F` (Failure) chiqadi va xato batafsil ko'rsatiladi (buni keyinroq ko'ramiz).

### AAA naqsh — Arrange, Act, Assert

Yuqoridagi testga qaytsak, u uch qismdan iborat edi. Bu — testlarning standart tuzilishi, **AAA naqsh** deyiladi:

```php
public function testQoshIkkitaSonniQoshadi(): void
{
    // 1. Arrange (tayyorla) — kerakli obyekt va ma'lumotlarni tayyorla
    $kalkulyator = new Kalkulyator();
    $a = 2;
    $b = 3;

    // 2. Act (bajar) — sinaladigan amalni bajar
    $natija = $kalkulyator->qosh($a, $b);

    // 3. Assert (tasdiqla) — natija kutilganday ekanini tekshir
    $this->assertEquals(5, $natija);
}
```

- **Arrange** — sahnani tayyorlash (obyekt yarat, ma'lumot ber).
- **Act** — bitta amalni bajarish (tekshirilayotgan metod).
- **Assert** — natijani tekshirish.

Bu tartib testni o'qishli qiladi: kim o'qisa ham "nima tayyorlandi, nima qilindi, nima kutilyapti" ni darrov ko'radi. Har bir test odatda **bitta narsani** tekshiradi.

### `#[Test]` atributi — `test` prefiksisiz

Metod nomini har safar `test...` bilan boshlash shart emas. Zamonaviy PHP'da **atribut** (attribute — kod ustidagi maxsus belgi, `#[...]` ko'rinishida) ishlatiladi. `#[Test]` atributi metodni test deb belgilaydi, nomi esa ixtiyoriy bo'ladi:

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Kalkulyator.php';

class KalkulyatorTest extends TestCase
{
    #[Test]
    public function ayirAyirmaniQaytaradi(): void
    {
        $kalkulyator = new Kalkulyator();

        $this->assertSame(4, $kalkulyator->ayir(10, 6));
    }
}
```

`use PHPUnit\Framework\Attributes\Test;` — atributni import qiladi (namespace, 2.12). Endi metod nomi mazmunli (`ayirAyirmaniQaytaradi`) bo'lib, `test` prefiksiga bog'lanmaydi. Bu — hozirgi tavsiya etiladigan uslub.

### Eng muhim assertlar

Assert — testning yuragi. PHPUnit'da o'nlab assert bor; quyida eng ko'p ishlatiladiganlari.

#### `assertEquals` va `assertSame` — eng muhim farq

Ikkalasi ham "tenglikni" tekshiradi, lekin farqi katta:

- **`assertEquals(kutilgan, haqiqiy)`** — qiymatlarni `==` kabi taqqoslaydi: **turini e'tiborga olmaydi**. `5` va `'5'` (matn) — teng deb hisoblanadi.
- **`assertSame(kutilgan, haqiqiy)`** — qiymatlarni `===` kabi taqqoslaydi: **turini ham tekshiradi**. `5` (son) va `'5'` (matn) — teng EMAS.

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

class TaqqoslashTest extends TestCase
{
    #[Test]
    public function equalsTuriEtiborgaOlmaydi(): void
    {
        // '5' (matn) va 5 (son) -- assertEquals uchun teng (== kabi)
        $this->assertEquals(5, '5');   // ✅ o'tadi
    }

    #[Test]
    public function sameTuriniHamTekshiradi(): void
    {
        // 5 (int) va 5 (int) -- assertSame uchun teng (=== kabi)
        $this->assertSame(5, 2 + 3);   // ✅ o'tadi
    }
}
```

> **Maslahat:** imkon bo'lsa `assertSame` ishlatiladi — u qattiqroq tekshiradi, ya'ni `'5'` o'rniga `5` qaytsa ham darrov sezadi. `assertEquals` esa ob'ektlarni yoki tur muhim bo'lmagan joylarda qulay.

#### `assertTrue` va `assertFalse` — mantiqiy qiymatlar

`true`/`false` qaytaradigan funksiyalar uchun:

```php
<?php
$this->assertTrue($validator->emailToghriMi('ali@mail.com'));   // true bo'lsin
$this->assertFalse($validator->emailToghriMi('salom'));         // false bo'lsin
```

#### `assertNull` — qiymat bo'sh (null) ekanini tekshirish

```php
<?php
$qiymat = null;
$this->assertNull($qiymat);   // null bo'lsin
```

#### `assertCount` — massivdagi elementlar soni

```php
<?php
$royxat = ['olma', 'anor', 'uzum'];
$this->assertCount(3, $royxat);   // aynan 3 ta element bo'lsin
```

#### `assertContains` — massivda element bor-yo'qligi

```php
<?php
$royxat = ['olma', 'anor', 'uzum'];
$this->assertContains('anor', $royxat);   // 'anor' massivda bo'lsin
```

#### `assertInstanceOf` — obyekt qaysi class'dan ekanini tekshirish

```php
<?php
$validator = new Validator();
$this->assertInstanceOf(Validator::class, $validator);   // Validator obyekti bo'lsin
```

Bularning hammasini bitta testda ko'rib chiqaylik. `Validator` class'i (`src/Validator.php`):

```php
<?php

class Validator
{
    public function emailToghriMi(string $email): bool
    {
        return str_contains($email, '@') && str_contains($email, '.');
    }

    public function parolKuchliMi(string $parol): bool
    {
        return strlen($parol) >= 8;
    }
}
```

Va uning testi:

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Validator.php';

class ValidatorTest extends TestCase
{
    #[Test]
    public function turliAssertlar(): void
    {
        $validator = new Validator();

        $this->assertTrue($validator->emailToghriMi('ali@mail.com'));
        $this->assertFalse($validator->emailToghriMi('salom'));

        $natija = $validator->parolKuchliMi('parol');   // 5 ta belgi
        $this->assertFalse($natija);

        $royxat = ['olma', 'anor', 'uzum'];
        $this->assertCount(3, $royxat);
        $this->assertContains('anor', $royxat);

        $this->assertInstanceOf(Validator::class, $validator);
    }
}
```

### Xatoni kutish — `expectException`

Ba'zan funksiya **xato tashlashi** (throw, 2.10) kerak. Masalan, nolga bo'lganda `Kalkulyator::bol` xato tashlaydi. Buni qanday testlaymiz? `expectException` bilan: "shu kod ishga tushganda, men aynan shu xatoni kutaman" deymiz.

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Kalkulyator.php';

class KalkulyatorXatoTest extends TestCase
{
    #[Test]
    public function nolgaBolishXatoTashlaydi(): void
    {
        $kalkulyator = new Kalkulyator();

        // Avval xatoni "kutamiz" deb e'lon qilamiz
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage("Nolga bo'lib bo'lmaydi");

        // Endi xato tashlashi kerak bo'lgan kodni ishga tushiramiz
        $kalkulyator->bol(10, 0);
    }
}
```

Muhim nuqta: `expectException` ni xato tashlaydigan koddan **oldin** yozasiz. Agar `bol(10, 0)` haqiqatan ham `InvalidArgumentException` tashlasa — test o'tadi. Agar **xato tashlamasa** (xatolik kutilgan, lekin kelmadi) — test yiqiladi. `expectExceptionMessage` esa xato matnini ham tekshiradi (ixtiyoriy, lekin foydali).

### `setUp` va `tearDown` — takrorlanishni kamaytirish

Yuqoridagi har bir testda `$kalkulyator = new Kalkulyator();` ni qayta-qayta yozdik. Bu zerikarli. **`setUp`** metodi — har bir test metodidan **oldin** avtomatik ishga tushadigan tayyorgarlik joyi:

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Kalkulyator.php';

class KalkulyatorTest extends TestCase
{
    private Kalkulyator $kalkulyator;

    protected function setUp(): void
    {
        // Har bir test metodidan OLDIN ishga tushadi
        $this->kalkulyator = new Kalkulyator();
    }

    #[Test]
    public function qoshIshlaydi(): void
    {
        $this->assertSame(5, $this->kalkulyator->qosh(2, 3));
    }

    #[Test]
    public function ayirIshlaydi(): void
    {
        $this->assertSame(4, $this->kalkulyator->ayir(10, 6));
    }
}
```

Endi `$this->kalkulyator` har bir testda **yangidan** tayyorlanadi (testlar bir-biriga ta'sir qilmasligi uchun har biriga toza obyekt beriladi).

Juftligi — **`tearDown`** metodi: har bir testdan **keyin** ishga tushadi. Vaqtinchalik faylni o'chirish, ulanishni yopish kabi "tozalash" ishlari uchun:

```php
protected function tearDown(): void
{
    // Har bir testdan KEYIN ishga tushadi (tozalash uchun)
    // masalan: vaqtinchalik faylni o'chirish
}
```

### Data provider — bir test, ko'p ma'lumot

`qosh` funksiyasini ko'p holatda sinab ko'rmoqchimiz: `2+3=5`, `0+7=7`, `-4+1=-3` va h.k. Har biriga alohida test yozish — takror. **Data provider** (ma'lumot ta'minlovchi) bitta testni **ko'p ma'lumot to'plami** bilan ishga tushiradi.

Buning uchun:
1. Ma'lumotlarni qaytaradigan `static` (2.7) metod yozasiz — har bir element `[kirish1, kirish2, kutilgan_natija]` ko'rinishida.
2. Test metodiga `#[DataProvider('metodNomi')]` atributini qo'shasiz.
3. Test metodi parametrlar qabul qiladi — ular ma'lumotdan keladi.

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\DataProvider;

require_once __DIR__ . '/../src/Kalkulyator.php';

class KalkulyatorDataTest extends TestCase
{
    #[Test]
    #[DataProvider('qoshMisollari')]
    public function qoshTurliSonlarBilan(int $a, int $b, int $kutilgan): void
    {
        $kalkulyator = new Kalkulyator();

        $this->assertSame($kutilgan, $kalkulyator->qosh($a, $b));
    }

    public static function qoshMisollari(): array
    {
        return [
            'ikki musbat' => [2, 3, 5],
            'nol bilan'   => [0, 7, 7],
            'manfiy son'  => [-4, 1, -3],
            'ikki manfiy' => [-5, -5, -10],
        ];
    }
}
```

Endi PHPUnit testni **4 marta** — har bir ma'lumot to'plami bilan ishga tushiradi. `'ikki musbat'`, `'nol bilan'` kabi nomlar (kalitlar) — qaysi to'plam yiqilganini tezda topish uchun foydali. Agar `'manfiy son'` yiqilsa, PHPUnit aynan shuni aytadi. Bu — bir test bilan o'nlab holatni qoplashning eng tejamli yo'li.

### Mock va stub — bog'liqlikni almashtirish

Ba'zan sinalayotgan class boshqa narsaga **bog'liq** bo'ladi: tashqi API, ma'lumotlar bazasi, fayl tizimi. Testda haqiqiy API'ga murojaat qilish — sekin, ishonchsiz (internet o'chsa test yiqiladi). Yechim — bog'liqlikni **soxta** (yasama) versiya bilan almashtirish.

- **Stub** — "doim shu javobni qaytar" deydigan soxta obyekt (faqat ma'lumot beradi).
- **Mock** — undan ham ko'proq: chaqiruv **bo'lganini** ham tekshiradi (masalan, "bu metod aniq bir marta chaqirildimi?").

Misol: `NarxHisoblovchi` dollarni so'mga o'giradi, lekin kursni `KursManbasi` dan oladi (interfeys, 2.5). Testda haqiqiy kurs API'siga ulanmaymiz — uni **stub** bilan almashtiramiz:

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

interface KursManbasi
{
    public function dollarKursi(): float;
}

class NarxHisoblovchi
{
    public function __construct(private readonly KursManbasi $manba) {}

    public function somda(float $dollar): float
    {
        return $dollar * $this->manba->dollarKursi();
    }
}

class NarxHisoblovchiTest extends TestCase
{
    #[Test]
    public function dollarniSomgaOgiradi(): void
    {
        // Stub: KursManbasi'ni soxta obyekt bilan almashtiramiz
        $manba = $this->createStub(KursManbasi::class);
        $manba->method('dollarKursi')->willReturn(12500.0);   // doim 12500 qaytarsin

        $hisoblovchi = new NarxHisoblovchi($manba);

        $this->assertSame(125000.0, $hisoblovchi->somda(10));   // 10 * 12500
    }
}
```

`createStub(KursManbasi::class)` — interfeysga mos soxta obyekt yasaydi; `->method('dollarKursi')->willReturn(12500.0)` — "bu metod chaqirilsa, doim 12500 qaytar" deydi. Endi test internetga bog'liq emas, tez va barqaror.

Agar chaqiruv **bo'lganini** ham tekshirmoqchi bo'lsak — `createMock` va `expects` ishlatamiz:

```php
#[Test]
public function manbagaChaqiruvYuboriladi(): void
{
    $manba = $this->createMock(KursManbasi::class);
    $manba->expects($this->once())          // aniq bir marta chaqirilsin
          ->method('dollarKursi')
          ->willReturn(12500.0);

    $hisoblovchi = new NarxHisoblovchi($manba);
    $hisoblovchi->somda(10);
    // test oxirida PHPUnit "dollarKursi haqiqatan 1 marta chaqirildimi?" ni tekshiradi
}
```

> Qoida: javob **kerak bo'lsa** — stub; chaqiruvning o'zi **tekshirilsa** (chaqirildimi, necha marta) — mock. Boshlanishda stub ko'proq ishlatiladi.

### TDD g'oyasi — avval test, keyin kod

Hozirgacha avval kod yozib, keyin test yozdik. **TDD** (Test-Driven Development — test bilan boshqariladigan ishlab chiqish) buni teskari qiladi: **avval test**, keyin kod. Tsikl uchta qadamdan iborat:

1. **Qizil (Red)** — hali yozilmagan funksiya uchun test yozasiz. Test, tabiiyki, yiqiladi (funksiya yo'q yoki noto'g'ri) — natija qizil.
2. **Yashil (Green)** — testni o'tkazadigan **eng oddiy** kodni yozasiz. Natija yashil.
3. **Refactor (qayta tuzish)** — kodni tozalaysiz, yaxshilaysiz. Testlar yashil turibdi — demak buzmadingiz.

Keyin yana 1-qadamga qaytasiz. Bu — "avval nima kerakligini aniqlab ol, keyin yoz" degan intizom.

Misol: `chegirmaBilan(narx, foiz)` funksiyasi kerak. Avval testini yozamiz (`src/Narx.php` hali bo'sh, funksiya yo'q):

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Narx.php';

class NarxTest extends TestCase
{
    #[Test]
    public function chegirmaToghriHisoblanadi(): void
    {
        $narx = new Narx();

        // 1000 so'mdan 10% chegirma -> 900
        $this->assertSame(900.0, $narx->chegirmaBilan(1000.0, 10));
    }
}
```

Hozir ishga tushirsak — **qizil** (`Narx` class'i yoki metod yo'q). Endi testni o'tkazadigan eng oddiy kodni yozamiz (`src/Narx.php`):

```php
<?php

class Narx
{
    public function chegirmaBilan(float $narx, int $foiz): float
    {
        return $narx - ($narx * $foiz / 100);
    }
}
```

Endi test **yashil**. Keyingi talab: foiz 0..100 oralig'ida bo'lishi kerak. Avval shuni tekshiradigan test yozamiz:

```php
#[Test]
public function notoghriFoizXatoTashlaydi(): void
{
    $this->expectException(InvalidArgumentException::class);

    (new Narx())->chegirmaBilan(1000.0, 150);   // 150% -- noto'g'ri
}
```

Bu — yana **qizil** (hozir xato tashlanmaydi). Funksiyaga tekshiruv qo'shamiz — **yashil** qilamiz:

```php
<?php

class Narx
{
    public function chegirmaBilan(float $narx, int $foiz): float
    {
        if ($foiz < 0 || $foiz > 100) {
            throw new InvalidArgumentException("Foiz 0 va 100 orasida bo'lishi kerak");
        }

        return $narx - ($narx * $foiz / 100);
    }
}
```

Mana TDD tsikli: **qizil -> yashil -> refactor**. Kod talablar asosida, qadam-baqadam, har doim test himoyasida o'sib boradi.

### `phpunit.xml` — sozlamalarni bir joyga jamlash

Har safar `vendor/bin/phpunit tests` deb papkani ko'rsatish o'rniga, loyiha ildizida **`phpunit.xml`** sozlama fayli yaratiladi. PHPUnit uni avtomatik o'qiydi:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         bootstrap="vendor/autoload.php"
         colors="true">
    <testsuites>
        <testsuite name="Loyiha testlari">
            <directory>tests</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

- `bootstrap="vendor/autoload.php"` — har testdan oldin Composer autoload'ini (5.4) ulaydi, ya'ni `require_once` larni qo'lda yozish shart emas (class'laringiz autoload bilan yuklanadi).
- `<directory>tests</directory>` — testlar qayerda turishini ko'rsatadi.
- `colors="true"` — natijani rangli (yashil/qizil) chiqaradi.

Endi shunchaki:

```bash
vendor/bin/phpunit
```

PHPUnit `phpunit.xml` ni o'qib, `tests/` papkadagi hamma testni topib ishga tushiradi.

### Test yiqilganda nima bo'ladi?

Test "qizil" bo'lishi — yomon emas, balki **foyda**: u sizga muammoni aytib beradi. Aytaylik, funksiyada xato bor va `qosh(2, 2)` 99 emas, 4 qaytaradi. PHPUnit shuni ko'rsatadi:

```
There was 1 failure:

1) KalkulyatorTest::ataylabXato
Failed asserting that 4 is identical to 99.

/loyiha/tests/KalkulyatorTest.php:14

FAILURES!
Tests: 1, Assertions: 1, Failures: 1.
```

PHPUnit aniq aytadi: qaysi test (`KalkulyatorTest::ataylabXato`), nima kutilgan-u nima kelgan (`4 is identical to 99` — ya'ni haqiqiy 4, kutilgan 99), va qaysi faylning qaysi qatorida (`:14`). Shu ma'lumot bilan xatoni tez topasiz. `.` — o'tgan test, `F` — yiqilgan test, `E` — testda kutilmagan xatolik (error).

### Mashqlar

**Oson**

1. `Kalkulyator` class'i uchun `ayir(10, 4)` metodini sinaydigan test yozing: natija `6` ekanini `assertSame` bilan tekshiring.
2. `assertTrue` va `assertFalse` ishlatib, `5 > 3` (true) va `2 > 10` (false) ifodalarini sinang.
3. `['a', 'b', 'c']` massivida aynan 3 ta element borligini `assertCount` bilan tekshiring.
4. Bir massivda `'olma'` borligini `assertContains` bilan tasdiqlang.
5. `assertEquals(10, '10')` va `assertSame(10, '10')` farqini tushuntiring: qaysi biri o'tadi, qaysi biri yiqiladi va nega?

**O'rta**

6. `Validator` class'iga `parolKuchliMi` metodini sinaydigan ikkita test yozing: `"parol"` (5 belgi, `false`) va `"parol12345"` (10 belgi, `true`). `setUp` da `Validator` obyektini bir marta tayyorlang.
7. `Kalkulyator::bol(10, 0)` `InvalidArgumentException` tashlashini `expectException` bilan sinang.
8. Bir test class'ga `setUp` qo'shing va ikkita test metodida shu tayyorlangan obyektni ishlating. `setUp` har test oldidan ishga tushishini izohlang.
9. `assertNull` ishlatib, qiymat berilmagan o'zgaruvchi yoki `null` qaytaradigan funksiya natijasini sinang.

**Qiyin**

10. `qosh` metodini **data provider** bilan kamida 4 ta turli ma'lumot to'plamida sinang (musbat, nol, manfiy, katta sonlar). Har bir to'plamga mazmunli nom bering.
11. **TDD** bilan `kvadrat(int $son): int` funksiyasini yozing: avval `kvadrat(5) === 25` testini yozing (qizil), keyin funksiyani yozing (yashil).
12. **TDD** bilan `Hisob` (bank hisobi) class'ini yozing: `yechib_olish(summa)` metodi, agar balansdan ko'p summa yechilsa, xato (`Exception`) tashlasin. Avval ikkita test yozing (oddiy yechib olish + balansdan ko'p yechishda xato), keyin class'ni yozing.
13. Data provider bilan `Validator::emailToghriMi` ni sinang: bir nechta to'g'ri (`ali@mail.com`) va noto'g'ri (`salom`, `ali.mail.com`) email'larni bitta data provider'da bering. Har biri uchun kutilgan natija (`true`/`false`) ni ham to'plamga qo'shing.

<details markdown="1">
<summary>Yechim — 6 (setUp bilan ikki test)</summary>

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Validator.php';

class ParolTest extends TestCase
{
    private Validator $validator;

    protected function setUp(): void
    {
        $this->validator = new Validator();   // har test oldidan yangidan
    }

    #[Test]
    public function qisqaParolKuchsiz(): void
    {
        $this->assertFalse($this->validator->parolKuchliMi('parol'));   // 5 belgi
    }

    #[Test]
    public function uzunParolKuchli(): void
    {
        $this->assertTrue($this->validator->parolKuchliMi('parol12345'));   // 10 belgi
    }
}
```

`setUp` har ikkala testdan oldin alohida ishga tushadi, shuning uchun har bir test toza `Validator` obyektini oladi va testlar bir-biriga ta'sir qilmaydi.
</details>

<details markdown="1">
<summary>Yechim — 7 (expectException)</summary>

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Kalkulyator.php';

class BolTest extends TestCase
{
    #[Test]
    public function nolgaBolishXatoTashlaydi(): void
    {
        $kalkulyator = new Kalkulyator();

        $this->expectException(InvalidArgumentException::class);

        $kalkulyator->bol(10, 0);   // xato tashlashi kerak
    }
}
```

`expectException` ni xato tashlaydigan koddan **oldin** yozish muhim. Agar `bol(10, 0)` xato tashlamasa — test yiqiladi.
</details>

<details markdown="1">
<summary>Yechim — 10 (data provider bilan qosh)</summary>

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\DataProvider;

require_once __DIR__ . '/../src/Kalkulyator.php';

class QoshDataTest extends TestCase
{
    #[Test]
    #[DataProvider('sonlar')]
    public function qoshToghriHisoblanadi(int $a, int $b, int $kutilgan): void
    {
        $kalkulyator = new Kalkulyator();

        $this->assertSame($kutilgan, $kalkulyator->qosh($a, $b));
    }

    public static function sonlar(): array
    {
        return [
            'ikki musbat' => [2, 3, 5],
            'nol bilan'   => [0, 7, 7],
            'manfiy son'  => [-4, 1, -3],
            'katta sonlar' => [1000, 2500, 3500],
        ];
    }
}
```

Bitta test 4 marta — har bir to'plam bilan ishga tushadi. Mazmunli nomlar (`'manfiy son'`) yiqilgan holatni darrov topishga yordam beradi.
</details>

<details markdown="1">
<summary>Yechim — 12 (TDD bilan Hisob class'i)</summary>

**1-qadam — testlar (qizil).** Avval `tests/HisobTest.php`:

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;

require_once __DIR__ . '/../src/Hisob.php';

class HisobTest extends TestCase
{
    #[Test]
    public function pulYechibOlinadi(): void
    {
        $hisob = new Hisob(1000);

        $hisob->yechibOlish(300);

        $this->assertSame(700, $hisob->balans());
    }

    #[Test]
    public function balansdanKopYechishXatoTashlaydi(): void
    {
        $hisob = new Hisob(1000);

        $this->expectException(Exception::class);

        $hisob->yechibOlish(5000);   // balansdan ko'p
    }
}
```

**2-qadam — class (yashil).** Endi `src/Hisob.php`:

```php
<?php

class Hisob
{
    public function __construct(private int $balans) {}

    public function yechibOlish(int $summa): void
    {
        if ($summa > $this->balans) {
            throw new Exception("Balansda yetarli mablag' yo'q");
        }

        $this->balans -= $summa;
    }

    public function balans(): int
    {
        return $this->balans;
    }
}
```

Endi ikkala test ham **yashil**. Avval testni yozib, keyin uni o'tkazadigan kodni yozish — TDD'ning asosi: kod talab (test) asosida o'sib boradi.
</details>

<details markdown="1">
<summary>Yechim — 13 (data provider bilan email)</summary>

```php
<?php

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\DataProvider;

require_once __DIR__ . '/../src/Validator.php';

class EmailTest extends TestCase
{
    #[Test]
    #[DataProvider('emailMisollari')]
    public function emailToghriTekshiriladi(string $email, bool $kutilgan): void
    {
        $validator = new Validator();

        $this->assertSame($kutilgan, $validator->emailToghriMi($email));
    }

    public static function emailMisollari(): array
    {
        return [
            'toza email'    => ['ali@mail.com', true],
            'pochta yoq'    => ['ali.mail.com', false],   // @ yo'q
            'shunchaki soz' => ['salom', false],
            'boshqa toza'   => ['vali@gmail.com', true],
        ];
    }
}
```

Har bir to'plamda email **va** kutilgan natija (`true`/`false`) birga turibdi. Shunday qilib bitta test to'g'ri va noto'g'ri holatlarni birga qoplaydi.
</details>

> **5-QISM yakunlandi!** Endi siz toza kod yozib (5.1), uni MVC bilan tartibga solib (5.2), dizayn andozalaridan foydalanib (5.3), tashqi kutubxonalarni Composer bilan boshqarib (5.4) va kodingizni avtomatik testlar bilan himoyalab (5.5) bilasiz. Test yozish — havaskorni professionaldan ajratuvchi muhim ko'nikma: u kodingizga ishonch, refactoring'ga erkinlik va loyihaga barqarorlik beradi.
