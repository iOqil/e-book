# 2.7 Static xususiyat va metodlar

[⬅️ Oldingi: 2.6 Interfeys (interface)](./19-interfeys.md) · [🏠 README](./README.md) · [Keyingi: 2.8 Trait — metodlarni ulashish ➡️](./21-trait-metodlarni-ulashish.md)

---

### Obyektga emas, class'ning o'ziga tegishli

Hozirgacha xususiyat va metodlar **har bir obyektga** tegishli edi: `$mashina1->rang`, `$mashina2->rang` — har birida alohida. Lekin ba'zan ma'lumot yoki amal **butun class'ga** tegishli bo'ladi, alohida obyektga emas. Ana shunda **static** ishlatiladi.

Misol: nechta obyekt yaratilganini sanash. Bu son birorta obyektga emas, butun class'ga tegishli.

```php
<?php
class Talaba {
    public static $soni = 0;   // static — butun class'ga tegishli

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
- **`public static $soni = 0;`** — `static` so'zi: bu xususiyat obyektlarga emas, **class'ning o'ziga** tegishli. U bitta, hamma obyektlar uchun umumiy.
- **`self::$soni`** — static xususiyatga class **ichidan** murojaat. `self` — "shu class" degani (`$this` "shu obyekt" edi; `self` "shu class").
- **`Talaba::$soni`** — static xususiyatga **tashqaridan** murojaat. Obyekt orqali emas (`$t->soni` emas), balki **class nomi** orqali (`Talaba::$soni`). `::` belgisi static narsalar uchun ishlatiladi.

Uchta obyekt yaratdik, har biri konstruktorda `self::$soni++` qildi — natijada umumiy hisob 3 bo'ldi.

### Static metodlar

Metod ham static bo'lishi mumkin — bunda uni obyekt yaratmasdan, to'g'ridan-to'g'ri class orqali chaqirasiz. Bu odatda "yordamchi" (utility) funksiyalar uchun ishlatiladi:

```php
<?php
class Matematika {
    public static function kvadrat($son) {
        return $son * $son;
    }

    public static function kub($son) {
        return $son * $son * $son;
    }
}

// Obyekt yaratish SHART EMAS — to'g'ridan-to'g'ri class orqali:
echo Matematika::kvadrat(5);   // 25
echo "<br>";
echo Matematika::kub(3);       // 27
```

`Matematika::kvadrat(5)` — obyekt yaratmadik (`new` yo'q), to'g'ridan-to'g'ri class orqali metodni chaqirdik. Bu mantiqiy: "kvadratni hisoblash" uchun "matematika obyekti" yaratish shart emas — funksiyaning o'zi yetarli.

> **Qachon static?** Agar metod yoki ma'lumot **biror aniq obyektga bog'liq bo'lmasa** — static qiling. Masalan, "kvadratni hisoblash" hech qaysi obyektga bog'liq emas → static. Lekin "shu hisobning balansi" — aniq obyektga bog'liq → static EMAS. Boshlanishida static'ni kam ishlating; ko'pincha oddiy (obyektga tegishli) metodlar to'g'ri tanlov.

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

**Qiyin**
10. `IDgenerator` class'i: static `$oxirgiId = 0`. Static `yangiId()` metodi har chaqirilganda IDni 1 ga oshirib qaytarsin (1, 2, 3, ...). Bu — har bir yangi yozuvga noyob raqam berishning oddiy usuli.
11. `Foydalanuvchi` class'i: konstruktor `ism` olsin va static `$royxat` massiviga o'zini qo'shsin. Static `hammasi()` metodi barcha foydalanuvchilar ro'yxatini qaytarsin.
12. `Statistika` class'i: static metodlar bilan son massividan eng katta, eng kichik va o'rtacha qiymatni qaytaruvchi vositalar to'plamini yarating.

<details markdown="1">
<summary>Yechim — 10 (ID generator)</summary>

```php
<?php
class IDgenerator {
    public static $oxirgiId = 0;

    public static function yangiId() {
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
Static bo'lgani uchun `$oxirgiId` bitta va saqlanib turadi — har chaqiruvda davom etadi. Bu obyektga bog'liq bo'lmagan, "umumiy hisoblagich" uchun ajoyib misol.
</details>

<details markdown="1">
<summary>Yechim — 11 (Foydalanuvchilar ro'yxati)</summary>

```php
<?php
class Foydalanuvchi {
    public static $royxat = [];   // barcha foydalanuvchilar — butun class'ga umumiy
    public $ism;

    public function __construct($ism) {
        $this->ism = $ism;
        self::$royxat[] = $ism;    // o'zini umumiy ro'yxatga qo'shadi
    }

    public static function hammasi() {
        return self::$royxat;
    }
}

new Foydalanuvchi("Ali");
new Foydalanuvchi("Vali");
new Foydalanuvchi("Guli");

print_r(Foydalanuvchi::hammasi());   // ["Ali", "Vali", "Guli"]
```
`$royxat` static — u bitta va barcha obyektlar uchun umumiy. Har bir yangi foydalanuvchi konstruktorda `self::$royxat`ga qo'shiladi, shuning uchun `hammasi()` to'liq ro'yxatni beradi. `self::` — "shu class'ning static a'zosi" (obyektda `$this`, static'da `self`).
</details>

<details markdown="1">
<summary>Yechim — 12 (Statistika vositalari)</summary>

```php
<?php
class Statistika {
    public static function engKatta(array $sonlar) {
        return max($sonlar);
    }
    public static function engKichik(array $sonlar) {
        return min($sonlar);
    }
    public static function ortacha(array $sonlar) {
        return array_sum($sonlar) / count($sonlar);
    }
}

$ballar = [85, 90, 70, 95, 60];

echo "Eng katta: "  . Statistika::engKatta($ballar)  . "<br>";   // 95
echo "Eng kichik: " . Statistika::engKichik($ballar) . "<br>";   // 60
echo "O'rtacha: "   . Statistika::ortacha($ballar);              // 80
```
Bu metodlar hech qaysi obyektga bog'liq emas — ular shunchaki "vosita". Shuning uchun static: obyekt yaratmasdan, `Statistika::ortacha(...)` deb to'g'ridan-to'g'ri ishlatamiz. Bu — "yordamchi funksiyalar to'plami" uchun mos naqsh.
</details>
