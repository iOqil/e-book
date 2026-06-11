# 2.11 Magic metodlar

[⬅️ Oldingi: 2.10 Xatolarni boshqarish (try / catch)](./23-xatolarni-boshqarish.md) · [🏠 README](./README.md) · [Keyingi: 2.12 Namespace va autoloading ➡️](./namespace-autoloading.md)

---

Tasavvur qiling: Laravel'da `$user->name` deb yozasiz va ism o'z-o'zidan bazadan keladi — garchi `User` classida `public $name` umuman e'lon qilinmagan bo'lsa ham. Yoki `$collection->where(...)->map(...)->filter(...)` deb metodlarni zanjir qilib chaqirasiz, lekin classda bunday metodlarning ko'pi yo'q. Bu "sehr" qayerdan? Javob — **magic metodlar** (magic method — PHP avtomatik chaqiradigan maxsus metod).

**Magic metod** — nomi ikkita pastki chiziq bilan boshlanadigan (`__`) maxsus metod. Siz uni hech qachon `$obj->__get(...)` deb qo'lda chaqirmaysiz — PHP uni ma'lum bir vaziyat yuzaga kelganda **o'zi** chaqiradi. Masalan, mavjud bo'lmagan xususiyatga murojaat qilsangiz — `__get` ishga tushadi; obyektni `echo` qilsangiz — `__toString` ishga tushadi.

Bitta `__construct`ni siz allaqachon bilasiz (2.2): u obyekt `new` bilan yaratilganda avtomatik chaqiriladi. Aslida `__construct` ham magic metod — shunchaki eng ko'p ishlatiladigani. Bu bobda qolgan magic metodlarni o'rganamiz va ular bilan haqiqiy professional kutubxonalar (Laravel, Doctrine) qanday "sehr" yaratishini ko'ramiz.

> **Diqqat:** PHP'da `__` bilan boshlanadigan metod nomlari faqat PHP'ning o'zi uchun zahiralangan. Shuning uchun o'z metodlaringizni `__` bilan **boshlamang** — kelajakda PHP yangi magic metod qo'shsa, to'qnashuv bo'ladi.

### `__construct` va `__destruct` — boshlanish va tugash

`__construct`ni bilamiz: obyekt tug'ilganda chaqiriladi. Uning juftligi — `__destruct`: obyekt "o'lganda" (xotiradan o'chirilganda yoki skript tugaganda) chaqiriladi. Bu, masalan, ochilgan faylni yopish yoki ulanishni uzish uchun ishlatiladi:

```php
<?php
class FaylYozuvchi
{
    private $resurs;

    public function __construct(private readonly string $yol)
    {
        $this->resurs = fopen($this->yol, 'w');
        echo "Fayl ochildi: {$this->yol}\n";
    }

    public function yoz(string $matn): void
    {
        fwrite($this->resurs, $matn);
    }

    // Obyekt yo'q qilinganda avtomatik chaqiriladi
    public function __destruct()
    {
        fclose($this->resurs);
        echo "Fayl yopildi: {$this->yol}\n";
    }
}

$yozuvchi = new FaylYozuvchi('hisobot.txt');
$yozuvchi->yoz("Salom dunyo");
unset($yozuvchi);   // bu yerda __destruct ishga tushadi
echo "Dastur davom etmoqda...\n";
```

Natija:

```
Fayl ochildi: hisobot.txt
Fayl yopildi: hisobot.txt
Dastur davom etmoqda...
```

`__destruct`ni qo'lda yozish kamdan-kam kerak bo'ladi, lekin "resurs" (fayl, tarmoq ulanishi) bilan ishlaganda foydali. Diqqat: bu yerda `constructor property promotion` (2.2'da o'rgangan qisqa yozuv: `private readonly string $yol`) ishlatildi — bu zamonaviy PHP 8 uslubi.

### `__toString` — obyektni matnga aylantirish

Oddiy obyektni `echo` qilsangiz, xato chiqadi: PHP obyektni matnga qanday aylantirishni bilmaydi. `__toString` aynan shuni hal qiladi — u obyekt matn sifatida ishlatilganda (`echo`, satr ulash, `(string)`) chaqiriladi va matn qaytaradi:

```php
<?php
class Pul
{
    public function __construct(
        private readonly int $miqdor,
        private readonly string $valyuta = 'UZS'
    ) {}

    public function __toString(): string
    {
        return number_format($this->miqdor, 0, '.', ' ') . ' ' . $this->valyuta;
    }
}

$narx = new Pul(1500000);
echo $narx;                       // 1 500 000 UZS
echo "\n";
echo "Jami: " . $narx . "\n";     // Jami: 1 500 000 UZS
$matn = (string) $narx;           // matnga aylantirish
echo strlen($matn) . "\n";        // 13
```

`__toString` har doim `string` qaytarishi shart (PHP 8'da `: string` return-tipini yozsangiz, buni ta'minlaysiz). Bu metod log yozish, xabarlarni chiqarish, DTO'ni (Data Transfer Object — ma'lumot tashuvchi obyekt) ko'rsatishda juda qulay.

### `__get` va `__set` — mavjud bo'lmagan xususiyatga murojaat

Mana eng "sehrli" juftlik. `__get($nom)` — mavjud bo'lmagan (yoki `private`/`protected` bo'lib, tashqaridan ko'rinmaydigan) xususiyatni **o'qishga** urinilganda chaqiriladi. `__set($nom, $qiymat)` — bunday xususiyatga **yozishga** urinilganda chaqiriladi.

Bu Laravel modellaridagi (`$user->name`) "sehr"ning asosi. Quyida ichki massivda ma'lumot saqlaydigan, lekin tashqaridan oddiy xususiyat kabi ko'rinadigan class:

```php
<?php
class Sozlama
{
    private array $malumot = [];

    // $obj->nimadir = ... bo'lganda chaqiriladi
    public function __set(string $nom, mixed $qiymat): void
    {
        echo "[set] {$nom} = " . var_export($qiymat, true) . "\n";
        $this->malumot[$nom] = $qiymat;
    }

    // $obj->nimadir o'qilganda chaqiriladi
    public function __get(string $nom): mixed
    {
        echo "[get] {$nom}\n";
        return $this->malumot[$nom] ?? null;
    }
}

$s = new Sozlama();
$s->til = 'uz';          // __set chaqirildi
$s->mavzu = 'tungi';     // __set chaqirildi

echo $s->til . "\n";     // __get chaqirildi -> uz
echo $s->mavzu . "\n";   // __get chaqirildi -> tungi
```

Natija:

```
[set] til = 'uz'
[set] mavzu = 'tungi'
[get] til
uz
[get] mavzu
tungi
```

Diqqat qiling: `til` va `mavzu` degan xususiyatlar classda **umuman e'lon qilinmagan** — ular dinamik (dynamic — ish vaqtida hosil bo'ladigan) tarzda yaratildi. Bu — "dinamik xususiyat" (dynamic property) deb ataladi.

> **Muhim qoidalar:**
> - `__get`/`__set` faqat xususiyat **mavjud bo'lmaganda** yoki **ko'rinmas** (`private`/`protected`) bo'lganda ishlaydi. Agar `public $til` e'lon qilingan bo'lsa, PHP to'g'ridan-to'g'ri unga murojaat qiladi va `__get`ni **chaqirmaydi**.
> - Bu metodlar sekinroq ishlaydi (oddiy xususiyatga qaraganda) va IDE ularni "ko'rmaydi" (avto-to'ldirish ishlamaydi). Shuning uchun ortiqcha ishlatmang.

### `__isset` va `__unset` — `isset()` va `unset()` bilan ishlash

`__get`/`__set` bilan dinamik xususiyat yaratganda, bitta muammo chiqadi: `isset($obj->til)` to'g'ri ishlamaydi, chunki PHP haqiqiy xususiyatni ko'rmaydi. Buni `__isset` hal qiladi — u dinamik xususiyatga `isset()` yoki `empty()` qo'llanilganda chaqiriladi. `__unset` esa `unset()` qo'llanilganda:

```php
<?php
class Sozlama
{
    private array $malumot = [];

    public function __set(string $nom, mixed $qiymat): void
    {
        $this->malumot[$nom] = $qiymat;
    }

    public function __get(string $nom): mixed
    {
        return $this->malumot[$nom] ?? null;
    }

    // isset($obj->nom) / empty($obj->nom) bo'lganda
    public function __isset(string $nom): bool
    {
        return isset($this->malumot[$nom]);
    }

    // unset($obj->nom) bo'lganda
    public function __unset(string $nom): void
    {
        unset($this->malumot[$nom]);
    }
}

$s = new Sozlama();
$s->til = 'uz';

var_dump(isset($s->til));        // true   (__isset ishladi)
var_dump(isset($s->mavzu));      // false  (yo'q)

unset($s->til);                  // __unset ishladi
var_dump(isset($s->til));        // false
```

To'liq "dinamik xususiyatli" class qilish uchun bu to'rtlik (`__get`, `__set`, `__isset`, `__unset`) birga ishlatiladi — shunda obyekt har tomondan oddiy xususiyatli obyekt kabi tuyuladi.

### `__call` va `__callStatic` — mavjud bo'lmagan metod chaqirilganda

`__call($nom, $argumentlar)` — obyektda **mavjud bo'lmagan** metod chaqirilganda ishga tushadi. `$nom` — chaqirilgan metod nomi, `$argumentlar` — berilgan argumentlar massivi. `__callStatic` esa xuddi shu, lekin **static** metod uchun (`Class::metod()`).

Bu "proxy" (vositachi) va "fluent interface" (zanjirli, ravon interfeys) yaratishda asosiy vosita. Avval oddiy misol — har qanday metod chaqiruvini "ushlab qoladigan" class:

```php
<?php
class Logger
{
    // Mavjud bo'lmagan metod chaqirilganda
    public function __call(string $nom, array $argumentlar): void
    {
        $matn = $argumentlar[0] ?? '';
        echo "[" . strtoupper($nom) . "] {$matn}\n";
    }

    // Mavjud bo'lmagan STATIC metod chaqirilganda
    public static function __callStatic(string $nom, array $argumentlar): void
    {
        $matn = $argumentlar[0] ?? '';
        echo "[STATIC " . strtoupper($nom) . "] {$matn}\n";
    }
}

$log = new Logger();
$log->info("Foydalanuvchi kirdi");      // [INFO] Foydalanuvchi kirdi
$log->error("Baza ulanmadi");           // [ERROR] Baza ulanmadi
$log->debug("x = 42");                  // [DEBUG] x = 42

Logger::warning("Eski API");            // [STATIC WARNING] Eski API
```

`info`, `error`, `debug`, `warning` metodlari classda **yozilmagan** — lekin barchasi ishlaydi, chunki `__call`/`__callStatic` ularni ushlab qoladi. Aynan shu usul bilan Laravel'ning `Log::info(...)`, `Cache::get(...)` kabi "facade"lari (yuzaki interfeyslar) ishlaydi.

### `__invoke` — obyektni funksiya kabi chaqirish

`__invoke` eng qiziq magic metodlardan biri: u obyektni xuddi funksiya kabi `$obj(...)` ko'rinishida chaqirilganda ishga tushadi. Bunday obyekt "chaqiriladigan obyekt" (invokable object) deb ataladi — u holat (xususiyat) saqlaydigan funksiya kabi:

```php
<?php
class Kopaytiruvchi
{
    public function __construct(private readonly int $koeffitsient) {}

    // $obj(...) deb chaqirilganda ishlaydi
    public function __invoke(int $son): int
    {
        return $son * $this->koeffitsient;
    }
}

$ikkilantir = new Kopaytiruvchi(2);
$uchlantir = new Kopaytiruvchi(3);

echo $ikkilantir(10) . "\n";    // 20  ($ikkilantir obyektini funksiya kabi chaqirdik)
echo $uchlantir(10) . "\n";     // 30

// Eng foydali tomoni: array_map kabi funksiyalarga uzatish mumkin
$sonlar = [1, 2, 3, 4];
$natija = array_map($ikkilantir, $sonlar);
print_r($natija);               // [2, 4, 6, 8]
```

`__invoke`ning kuchi shundaki, oddiy funksiya holatni (bu yerda — `$koeffitsient`) saqlay olmaydi, ammo obyekt saqlaydi. Laravel'da "single action controller" (bitta vazifali kontroller) aynan shu prinsipga asoslangan.

### `__clone` — obyektni nusxalashda chuqur nusxa

PHP'da obyektni `clone` bilan nusxalasangiz, "yuza nusxa" (shallow copy) hosil bo'ladi: oddiy qiymatlar ko'chiriladi, lekin **ichki obyektlar** ikkala nusxada ham **bir xil** (umumiy) qoladi. Demak, nusxadagi ichki obyektni o'zgartirsangiz, asl obyektdagi ham o'zgaradi — bu ko'pincha xato keltiradi.

`__clone` — obyekt `clone` qilingandan keyin **yangi nusxada** avtomatik chaqiriladi. Uning vazifasi — ichki obyektlarni ham nusxalab, "chuqur nusxa" (deep copy) qilish:

```php
<?php
class Manzil
{
    public function __construct(public string $shahar) {}
}

class Foydalanuvchi
{
    public function __construct(
        public string $ism,
        public Manzil $manzil
    ) {}

    // clone qilinganda yangi nusxada chaqiriladi
    public function __clone(): void
    {
        // Ichki obyektni ham nusxalaymiz (aks holda umumiy bo'lib qoladi)
        $this->manzil = clone $this->manzil;
    }
}

$ali = new Foydalanuvchi('Ali', new Manzil('Toshkent'));
$vali = clone $ali;
$vali->ism = 'Vali';
$vali->manzil->shahar = 'Samarqand';   // faqat $vali ning manzilini o'zgartiramiz

echo $ali->manzil->shahar . "\n";       // Toshkent  (o'zgarmadi!)
echo $vali->manzil->shahar . "\n";      // Samarqand
```

`__clone` ichida `$this->manzil = clone $this->manzil;` qatorini olib tashlasangiz, ikkalasi ham `Samarqand` bo'lib qoladi — chunki ikkala obyekt bitta `Manzil`ni baham ko'radi. Mana shuning uchun ichki obyektli classlarda `__clone` deyarli har doim kerak.

### Real misol: dinamik query-builder

Endi bir nechta magic metodni birga ishlatib, haqiqiy kutubxonalardagidek "query builder" (so'rov quruvchi — SQL'ni metodlar bilan yig'adigan vosita) yasaymiz. Bu Laravel'ning `DB::table('users')->where('age', '>', 18)->orderBy('name')` uslubining soddalashtirilgan ko'rinishi:

```php
<?php
class QuerySorovi
{
    private array $shartlar = [];
    private array $tartib = [];

    public function __construct(private readonly string $jadval) {}

    // where(...), orWhere(...) kabi metodlar uchun
    public function where(string $maydon, string $amal, mixed $qiymat): static
    {
        $this->shartlar[] = "{$maydon} {$amal} '{$qiymat}'";
        return $this;   // zanjir uchun o'zini qaytaradi (fluent interface)
    }

    public function orderBy(string $maydon, string $yonalish = 'ASC'): static
    {
        $this->tartib[] = "{$maydon} {$yonalish}";
        return $this;
    }

    // Yakuniy SQL matnini yasash
    public function __toString(): string
    {
        $sql = "SELECT * FROM {$this->jadval}";

        if ($this->shartlar !== []) {
            $sql .= " WHERE " . implode(' AND ', $this->shartlar);
        }
        if ($this->tartib !== []) {
            $sql .= " ORDER BY " . implode(', ', $this->tartib);
        }

        return $sql . ";";
    }
}

$sorov = (new QuerySorovi('foydalanuvchilar'))
    ->where('yosh', '>', 18)
    ->where('shahar', '=', 'Toshkent')
    ->orderBy('ism');

echo $sorov . "\n";
// SELECT * FROM foydalanuvchilar WHERE yosh > '18' AND shahar = 'Toshkent' ORDER BY ism ASC;
```

Bu yerda ikkita g'oya birlashdi: har bir metod `return $this` qaytarib **zanjir** (fluent) imkonini berdi, `__toString` esa yig'ilgan so'rovni `echo` qilinganda SQL matniga aylantirdi.

### Real misol: tiplangan konteyner (ActiveRecord namunasi)

Endi `__get`/`__set`/`__isset` + `__call`ni birga ishlatib, soddalashtirilgan "ActiveRecord" (ma'lumotni obyekt kabi ifodalovchi andoza — Laravel Eloquent shunga asoslangan) yasaymiz. Bunda ma'lumotlar ichki massivda saqlanadi, lekin tashqaridan oddiy obyekt kabi ko'rinadi, ustiga `getIsm()` kabi metodlar ham "sehrli" ravishda ishlaydi:

```php
<?php
class Model
{
    public function __construct(private array $atributlar = []) {}

    public function __get(string $nom): mixed
    {
        return $this->atributlar[$nom] ?? null;
    }

    public function __set(string $nom, mixed $qiymat): void
    {
        $this->atributlar[$nom] = $qiymat;
    }

    public function __isset(string $nom): bool
    {
        return isset($this->atributlar[$nom]);
    }

    // getIsm(), getYosh() kabi chaqiruvlarni avtomatik hosil qilamiz
    public function __call(string $nom, array $argumentlar): mixed
    {
        if (str_starts_with($nom, 'get')) {
            // "getIsm" -> "ism"
            $maydon = strtolower(substr($nom, 3));
            return $this->atributlar[$maydon] ?? null;
        }

        throw new BadMethodCallException("Metod topilmadi: {$nom}");
    }

    public function toArray(): array
    {
        return $this->atributlar;
    }
}

$user = new Model(['ism' => 'Ali', 'yosh' => 25]);

// Dinamik xususiyat (__get / __set)
echo $user->ism . "\n";          // Ali
$user->shahar = 'Toshkent';      // __set
echo $user->shahar . "\n";       // Toshkent

// Sehrli getter (__call)
echo $user->getIsm() . "\n";     // Ali
echo $user->getYosh() . "\n";    // 25

// __isset
var_dump(isset($user->ism));     // true
var_dump(isset($user->yoq));     // false

print_r($user->toArray());
```

Natija:

```
Ali
Toshkent
Ali
25
bool(true)
bool(false)
Array
(
    [ism] => Ali
    [yosh] => 25
    [shahar] => Toshkent
)
```

Bu — Eloquent va Doctrine kabi ORM (Object-Relational Mapping — obyekt va baza jadvali orasidagi ko'prik) kutubxonalarining yuragida turgan g'oya. Albatta, haqiqiy ORM bundan ancha murakkab, lekin "sehr" aynan shu magic metodlardan boshlanadi.

### `__serialize` va `__unserialize` — obyektni saqlashga tayyorlash

Obyektni faylga saqlash, sessiyaga yozish yoki tarmoq orqali yuborish uchun uni **matn ko'rinishiga** o'tkazish kerak — bu **serializatsiya** (`serialize()`). Ba'zan saqlashdan oldin nimanidir tashlab yuborish kerak (masalan, parol yoki ulanish resursi). `__serialize` aynan **qaysi** ma'lumot saqlanishini, `__unserialize` esa tiklashda nima qilishni belgilaydi (PHP 7.4+; eski `__sleep`/`__wakeup` o'rnini bosadi):

```php
<?php
class Foydalanuvchi
{
    public ?string $parol = null;   // bu saqlanmasin

    public function __construct(public string $ism) {}

    public function __serialize(): array
    {
        return ['ism' => $this->ism];        // faqat ism saqlanadi
    }

    public function __unserialize(array $data): void
    {
        $this->ism = $data['ism'];
    }
}

$u = new Foydalanuvchi("Ali");
$u->parol = "maxfiy";

$saqlangan = serialize($u);              // parol ICHIDA yo'q
$tiklangan = unserialize($saqlangan);
echo $tiklangan->ism;                    // Ali
```

📌 Eski `__sleep()` (saqlanadigan xususiyat nomlarini qaytaradi) va `__wakeup()` (tiklashda chaqiriladi) ham mavjud, lekin zamonaviy kodda `__serialize`/`__unserialize` juftligi afzal.

### `__debugInfo` — `var_dump` nimani ko'rsatishini boshqarish

`var_dump($obj)` obyektning BARCHA xususiyatlarini chiqaradi — ba'zan bu ortiqcha yoki maxfiy (parol, PIN). `__debugInfo` `var_dump` nimani ko'rsatishini belgilaydi:

```php
<?php
class Hisob
{
    public function __construct(
        public string $egasi,
        private string $pinKod,
    ) {}

    public function __debugInfo(): array
    {
        return ['egasi' => $this->egasi, 'pinKod' => '***'];   // PIN yashirildi
    }
}

var_dump(new Hisob("Ali", "1234"));
// object(Hisob)#1 (2) { ["egasi"]=> string(3) "Ali" ["pinKod"]=> string(3) "***" }
```

### Magic metodlar — to'liq ro'yxat (eslatma jadvali)

| Metod | Qachon chaqiriladi |
|-------|--------------------|
| `__construct` | Obyekt `new` bilan yaratilganda |
| `__destruct` | Obyekt yo'q qilinganda / skript tugaganda |
| `__toString` | Obyekt matn sifatida ishlatilganda (`echo`, `(string)`) |
| `__get` | Mavjud/ko'rinmas xususiyat **o'qilganda** |
| `__set` | Mavjud/ko'rinmas xususiyatga **yozilganda** |
| `__isset` | `isset()`/`empty()` qo'llanilganda |
| `__unset` | `unset()` qo'llanilganda |
| `__call` | Mavjud bo'lmagan **obyekt** metodi chaqirilganda |
| `__callStatic` | Mavjud bo'lmagan **static** metod chaqirilganda |
| `__invoke` | Obyekt funksiya kabi `$obj(...)` chaqirilganda |
| `__clone` | Obyekt `clone` qilingandan keyin |
| `__serialize` | `serialize()` da — qaysi ma'lumot saqlanishi (PHP 7.4+) |
| `__unserialize` | `unserialize()` da — obyektni qayta tiklash (PHP 7.4+) |
| `__sleep` / `__wakeup` | Eski serializatsiya juftligi (`__serialize` afzal) |
| `__debugInfo` | `var_dump()` obyektni qanday ko'rsatishi |
| `__set_state` | `var_export()` chaqirilganda |

### Ehtiyot bo'ling: magic metodlarni ortiqcha ishlatmang

Magic metodlar kuchli, lekin "sehr" har doim yaxshi emas. Quyidagilarni yodda tuting:

- **IDE va avto-to'ldirish "ko'rmaydi".** `__get` orqali yaratilgan `$user->ism` xususiyatini muharrir tanimaydi — xato yozsangiz ham ogohlantirmaydi. Buni yumshatish uchun class ustiga `@property` izohi yoziladi (Laravel modellarida shuni ko'rasiz).
- **Sekinroq.** Magic metod chaqiruvi oddiy xususiyat/metoddan bir necha barobar sekin. Ko'p marta takrorlanadigan tsiklda buni sezasiz.
- **O'qishni qiyinlashtiradi.** Kodni o'qigan kishi `$user->getIsm()` qayerda yozilganini izlab topa olmaydi — chunki u `__call` ichida yashiringan.
- **Qachon ishlatish kerak?** Haqiqatan dinamik xulq kerak bo'lganda (ORM, konfiguratsiya konteyneri, proxy, DTO). Oddiy class uchun esa odatiy xususiyat va metodlardan foydalaning — ular aniqroq va tezroq.

Qoida sodda: **agar oddiy usul bilan yozish mumkin bo'lsa, magic metoddan foydalanmang.** Magic metod — maxsus vaziyatlar uchun maxsus vosita.

### Mashqlar

**Oson**

1. `Vaqt` nomli class yarating: u `$soat` va `$daqiqa` qabul qilsin, `__toString` orqali `"14:05"` ko'rinishida qaytarsin (bir xonali daqiqa oldiga nol qo'shing — maslahat: `sprintf("%02d", ...)`).
2. `Harorat` classini yozing: `$qiymat` (gradus) saqlasin, `echo` qilinganda `"23°C"` chiqarsin.
3. `Foydalanuvchi` classida `$ism` va `$familiya` bo'lsin; `__toString` to'liq ismni (`"Ali Valiyev"`) qaytarsin.
4. `Kvadrat` classini yozing: `__invoke($son)` orqali chaqirilganda sonning kvadratini (`$son * $son`) qaytarsin. `$k = new Kvadrat(); echo $k(5);` -> 25.

**O'rta**

5. `__get` va `__set` ishlatib, ichki massivda ma'lumot saqlaydigan `Konteyner` classini yozing. `$c->til = 'uz'` va `echo $c->til;` ishlasin. Mavjud bo'lmagan xususiyat o'qilsa `null` qaytsin.
6. `__isset` ham qo'shing (5-mashqdagi `Konteyner`ga): `isset($c->til)` to'g'ri ishlasin.
7. `Salomlovchi` classini yozing: `__invoke($ism)` orqali `"Salom, Ali!"` qaytarsin. Keyin uni `array_map` bilan `["Ali", "Vali"]` massiviga qo'llang.
8. `__set` ichida tekshiruv qo'shing: agar `$nom === 'yosh'` bo'lsa va qiymat manfiy bo'lsa, `InvalidArgumentException` tashlang (throw). Aks holda saqlang.

**Qiyin**

9. `Sozlama` classini yozing: `set('til', 'uz')` o'rniga `setTil('uz')`, `setMavzu('tungi')` kabi metodlar `__call` orqali ishlasin (fluent — har biri `$this` qaytarsin, zanjir qilinsin). `__toString` orqali barcha sozlamalarni `"til=uz; mavzu=tungi"` ko'rinishida chiqaring.
10. `Savatcha` classini `__clone` bilan yozing: ichida `Mahsulot` obyektlari massivi bo'lsin. Savatchani `clone` qilganda, ichidagi har bir `Mahsulot` ham yangidan nusxalansin (chuqur nusxa), shunda nusxadagi mahsulot narxini o'zgartirsangiz asl savatchaga ta'sir qilmasin.
11. Soddalashtirilgan `Record` (ActiveRecord) classini yozing: konstruktorda massiv qabul qilsin; `__get`/`__set` bilan maydonlarga murojaat; `__call` bilan `getX()` (o'qish) va `setX($q)` (yozish) metodlari ishlasin; `toArray()` barcha maydonlarni qaytarsin.

<details markdown="1">
<summary>Yechim — 5 (__get / __set)</summary>

```php
<?php
class Konteyner
{
    private array $malumot = [];

    public function __get(string $nom): mixed
    {
        return $this->malumot[$nom] ?? null;
    }

    public function __set(string $nom, mixed $qiymat): void
    {
        $this->malumot[$nom] = $qiymat;
    }
}

$c = new Konteyner();
$c->til = 'uz';
echo $c->til . "\n";       // uz
var_dump($c->mavzu);       // NULL (mavjud emas)
```
`?? null` — agar kalit massivda bo'lmasa, `null` qaytaradi (xato o'rniga).
</details>

<details markdown="1">
<summary>Yechim — 7 (__invoke + array_map)</summary>

```php
<?php
class Salomlovchi
{
    public function __invoke(string $ism): string
    {
        return "Salom, {$ism}!";
    }
}

$salom = new Salomlovchi();

echo $salom('Ali') . "\n";          // Salom, Ali!

$natija = array_map($salom, ['Ali', 'Vali']);
print_r($natija);
// Array ( [0] => Salom, Ali! [1] => Salom, Vali! )
```
Obyekt `__invoke` tufayli oddiy funksiya kabi ishlatildi va `array_map`ga uzatildi.
</details>

<details markdown="1">
<summary>Yechim — 9 (__call bilan fluent setter)</summary>

```php
<?php
class Sozlama
{
    private array $malumot = [];

    public function __call(string $nom, array $argumentlar): static
    {
        if (str_starts_with($nom, 'set')) {
            // "setTil" -> "til"
            $maydon = strtolower(substr($nom, 3));
            $this->malumot[$maydon] = $argumentlar[0] ?? null;
            return $this;   // zanjir uchun
        }

        throw new BadMethodCallException("Noma'lum metod: {$nom}");
    }

    public function __toString(): string
    {
        $juftliklar = [];
        foreach ($this->malumot as $kalit => $qiymat) {
            $juftliklar[] = "{$kalit}={$qiymat}";
        }
        return implode('; ', $juftliklar);
    }
}

$s = (new Sozlama())
    ->setTil('uz')
    ->setMavzu('tungi')
    ->setTil('en');   // qayta yozish ham ishlaydi

echo $s . "\n";       // til=en; mavzu=tungi
```
Har bir `setX` `__call` ichida ushlanib, `$this` qaytargani uchun zanjir hosil bo'ldi.
</details>

<details markdown="1">
<summary>Yechim — 10 (__clone chuqur nusxa)</summary>

```php
<?php
class Mahsulot
{
    public function __construct(
        public string $nom,
        public int $narx
    ) {}
}

class Savatcha
{
    /** @var Mahsulot[] */
    private array $mahsulotlar = [];

    public function qoshish(Mahsulot $m): void
    {
        $this->mahsulotlar[] = $m;
    }

    public function jami(): int
    {
        return array_sum(array_map(fn(Mahsulot $m) => $m->narx, $this->mahsulotlar));
    }

    // Har bir ichki Mahsulotni ham nusxalaymiz (chuqur nusxa)
    public function __clone(): void
    {
        $this->mahsulotlar = array_map(
            fn(Mahsulot $m) => clone $m,
            $this->mahsulotlar
        );
    }
}

$asl = new Savatcha();
$asl->qoshish(new Mahsulot('Kitob', 50000));
$asl->qoshish(new Mahsulot('Ruchka', 5000));

$nusxa = clone $asl;
// Nusxadagi birinchi mahsulot narxini o'zgartiramiz... lekin buning uchun
// ichki obyektga murojaat kerak, shuning uchun jamilarni solishtiramiz:

echo "Asl jami:   " . $asl->jami() . "\n";    // 55000
echo "Nusxa jami: " . $nusxa->jami() . "\n";  // 55000

// Endi nusxadagi ichki obyektni o'zgartirsak, __clone tufayli
// asl savatchaga ta'sir qilmaydi — chunki ular alohida obyektlar.
```
`__clone` ichida `array_map(fn($m) => clone $m, ...)` har bir mahsulotni yangidan nusxaladi. Bu qatorsiz, ikkala savatcha bir xil `Mahsulot` obyektlarini baham ko'rardi.
</details>

<details markdown="1">
<summary>Yechim — 11 (oddiy ActiveRecord)</summary>

```php
<?php
class Record
{
    public function __construct(private array $maydonlar = []) {}

    public function __get(string $nom): mixed
    {
        return $this->maydonlar[$nom] ?? null;
    }

    public function __set(string $nom, mixed $qiymat): void
    {
        $this->maydonlar[$nom] = $qiymat;
    }

    public function __call(string $nom, array $argumentlar): mixed
    {
        // getIsm() -> o'qish
        if (str_starts_with($nom, 'get')) {
            $maydon = strtolower(substr($nom, 3));
            return $this->maydonlar[$maydon] ?? null;
        }

        // setIsm('Ali') -> yozish
        if (str_starts_with($nom, 'set')) {
            $maydon = strtolower(substr($nom, 3));
            $this->maydonlar[$maydon] = $argumentlar[0] ?? null;
            return $this;   // fluent
        }

        throw new BadMethodCallException("Noma'lum metod: {$nom}");
    }

    public function toArray(): array
    {
        return $this->maydonlar;
    }
}

$u = new Record(['ism' => 'Ali']);

// __get / __set
$u->yosh = 25;
echo $u->ism . "\n";          // Ali

// __call: getter / setter
$u->setShahar('Toshkent');
echo $u->getShahar() . "\n";  // Toshkent
echo $u->getYosh() . "\n";    // 25

print_r($u->toArray());
// Array ( [ism] => Ali [yosh] => 25 [shahar] => Toshkent )
```
Bu — Laravel Eloquent va Doctrine kabi ORM'larning eng asosiy g'oyasi: ma'lumot massivda, murojaat esa "sehrli" magic metodlar orqali.
</details>
</content>
</invoke>
