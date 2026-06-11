# 5.3 Foydali dizayn andozalari

[⬅️ Oldingi: 5.2 MVC — loyihani tartibga solish](./37-mvc-loyihani-tartibga-solish.md) · [🏠 README](./README.md) · [Keyingi: 5.4 Composer — tashqi kutubxonalar ➡️](./39-composer-tashqi-kutubxonalar.md)

---

**Dizayn andozasi (design pattern)** — tez-tez uchraydigan muammolar uchun tayyor, sinovdan o'tgan yechim usuli. Ularni yoddan o'rganish shart emas — aksincha, ko'pini siz allaqachon (bilmasdan) ishlatdingiz! Bu bo'limda eng oddiy va foydalilarini, tanish misollar bilan ko'rsatamiz.

### 1) Bog'liqlikni uzatish (Dependency Injection)

Buni 5.2'da allaqachon ishlatdingiz! `TalabaModel`ga `$pdo`ni **konstruktor orqali berdik**:

```php
<?php
class TalabaModel {
    private $pdo;

    public function __construct($pdo) {   // bog'liqlikni tashqaridan olamiz
        $this->pdo = $pdo;
    }
}

$model = new TalabaModel($pdo);   // kerakli narsani uzatamiz
```

Bunga **Dependency Injection** ("bog'liqlikni uzatish") deyiladi: class o'ziga kerakli narsani (bu yerda — bazaga ulanish) **ichida yaratmaydi**, balki **tashqaridan oladi**.

Nega yaxshi? Agar `TalabaModel` ichida o'zi `new PDO(...)` qilsa, uni sinash yoki o'zgartirish qiyin bo'lardi. Tashqaridan berganimizda — moslashuvchan: turli ulanishlar berishimiz mumkin (masalan, sinov uchun boshqasini). Oddiy qoida: **class'ga kerakli narsalarni konstruktor orqali bering.**

### 2) Almashtiriladigan xulq (Strategy)

Buni ham ko'rgansiz — 2.6'dagi interfeyslar! Esingizdami, `Tolov` interfeysi bo'lib, `NaqdTolov` va `KartaTolov` uni har xil amalga oshirardi, va ularni bir-biriga almashtirsa bo'lardi:

```php
<?php
interface Tolov {
    public function tasdiqla($summa);
}

class NaqdTolov implements Tolov { /* ... */ }
class KartaTolov implements Tolov { /* ... */ }

// To'lov turini istalgan vaqtda almashtirsa bo'ladi:
function buyurtmaTola(Tolov $tolov, $summa) {
    $tolov->tasdiqla($summa);
}
```

Bu — **Strategy** andozasi: bir vazifani bajarishning turli usullarini (strategiyalarini) interfeys orqali almashtiriladigan qilish. Yangi usul qo'shsangiz (masalan, `OnlaynTolov`) — mavjud kodni o'zgartirmaysiz, faqat yangi class yozasiz.

### 3) Yaratishni bir joyga jamlash (Factory)

Ba'zan obyekt yaratish mantig'i murakkab yoki bir necha joyda kerak bo'ladi. Uni bitta funksiya/class'ga jamlaymiz — bu **Factory** ("fabrika"):

```php
<?php
class TolovFactory {
    public static function yarat($tur) {
        return match($tur) {
            'naqd'  => new NaqdTolov(),
            'karta' => new KartaTolov(),
            default => throw new Exception("Noma'lum to'lov turi"),
        };
    }
}

// Endi obyekt yaratish bir joyda, oddiy:
$tolov = TolovFactory::yarat('karta');
```

Foydasi: obyekt yaratish mantig'i bir joyda. Yangi tur qo'shsangiz — faqat bu yerni yangilaysiz, butun loyiha bo'ylab emas.

### Muhim ogohlantirish: andozani majburlamang

Andozalar — foydali, lekin ularni **kerak bo'lmagan joyda** ishlatmang. Oddiy ishga murakkab andoza qo'shish — kodni soddalashtirmaydi, balki chalkashtiradi. Andozani faqat u **haqiqiy muammoni** (masalan, almashtirib bo'ladigan xulq kerakligini) hal qilganda qo'llang. Boshlovchi sifatida: avval oddiy yozing; muammo paydo bo'lganda, mos andozani qo'llang. Tajriba bilan qaysi andoza qachon kerakligini his qilasiz.

### Mashqlar

**Oson**
1. Dependency Injection: bir class'ga bog'liqlikni (masalan, `$pdo` yoki boshqa obyekt) konstruktor orqali bering.
2. 2.6'dagi `Tolov` interfeysi misolini Strategy andozasi sifatida qayta ko'rib chiqing — nega bu "almashtiriladigan xulq"?
3. Oddiy Factory yozing: tur nomiga qarab mos obyekt qaytaruvchi `yarat($tur)` metodi.

**O'rta**
4. `Bildirishnoma` Factory'si: `'email'`, `'sms'` turlariga qarab mos class obyektini qaytarsin.
5. Strategy bilan: turli "chegirma" usullarini (`OddiyChegirma`, `VIPChegirma`) interfeys orqali almashtiriladigan qiling.
6. Dependency Injection foydasini ko'rsating: ichida `new` qiladigan class va konstruktor orqali oladigan class'ni yonma-yon yozing, farqini izohlang.

**Qiyin**
7. To'lov tizimini uchala andoza bilan birlashtiring: `TolovFactory` (yaratish) + `Tolov` interfeysi (Strategy, almashtirish) + Dependency Injection (kerakli obyektlarni uzatish). Qaysi andoza qaysi muammoni hal qilishini izohlang.

<details markdown="1">
<summary>Yechim — 6 (DI farqi)</summary>

```php
<?php
// ❌ Bog'liqlikni ichida yaratish — moslashuvchan emas:
class HisobotYomon {
    private $pdo;
    public function __construct() {
        // ulanish ma'lumoti shu yerga "qotirilgan" — o'zgartirish/sinash qiyin
        $this->pdo = new PDO("mysql:host=localhost;dbname=maktab", "root", "");
    }
}

// ✅ Bog'liqlikni tashqaridan olish (DI) — moslashuvchan:
class HisobotYaxshi {
    private $pdo;
    public function __construct($pdo) {   // ulanish tashqaridan keladi
        $this->pdo = $pdo;
    }
}

// Yaxshi versiyada turli ulanish bera olamiz (masalan, sinov uchun boshqasini):
$pdo = new PDO("mysql:host=localhost;dbname=maktab", "root", "");
$hisobot = new HisobotYaxshi($pdo);
```
Farq: yomon versiyada ulanish class ichiga "qotirilgan" — uni o'zgartirib yoki sinab bo'lmaydi. Yaxshi versiyada tashqaridan beramiz — moslashuvchan va sinash oson. Shuning uchun kerakli narsalarni konstruktor orqali uzating.
</details>

<details markdown="1">
<summary>Yechim — 7 (uchala andozani birlashtirish)</summary>

```php
<?php
// 1) Tolov — interfeys (Strategy: almashtiriladigan xulq)
interface Tolov {
    public function tasdiqla($summa);
}

class NaqdTolov implements Tolov {
    public function tasdiqla($summa) { return "Naqd: $summa so'm qabul qilindi"; }
}
class KartaTolov implements Tolov {
    public function tasdiqla($summa) { return "Karta: $summa so'm yechildi"; }
}

// 2) TolovFactory — yaratishni bir joyga jamlaydi (Factory)
class TolovFactory {
    public static function yarat($tur): Tolov {
        return match($tur) {
            'naqd'  => new NaqdTolov(),
            'karta' => new KartaTolov(),
            default => throw new Exception("Noma'lum to'lov turi"),
        };
    }
}

// 3) Buyurtma — to'lovni TASHQARIDAN oladi (Dependency Injection)
class Buyurtma {
    private $tolov;
    public function __construct(Tolov $tolov) {   // har qanday Tolov bo'lishi mumkin
        $this->tolov = $tolov;
    }
    public function tola($summa) {
        return $this->tolov->tasdiqla($summa);
    }
}

// Ishlatish:
$tolov = TolovFactory::yarat('karta');   // Factory yaratadi
$buyurtma = new Buyurtma($tolov);        // DI orqali beramiz
echo $buyurtma->tola(50000);             // Karta: 50000 so'm yechildi
```

Har bir andoza o'z muammosini hal qiladi:
- **Interfeys (Strategy):** `Buyurtma` to'lov turini bilmaydi — har qanday `Tolov`ni qabul qiladi. Yangi tur (`OnlaynTolov`) qo'shsangiz, `Buyurtma`ni o'zgartirmaysiz.
- **Factory:** obyekt yaratish mantig'i bir joyda (`TolovFactory`). Yangi tur qo'shsangiz — faqat shu yerni yangilaysiz.
- **Dependency Injection:** `Buyurtma` to'lovni o'zi yaratmaydi, **tashqaridan** oladi — moslashuvchan va sinash oson.

Uchovi birga — kengaytiriladigan, toza tizim. Lekin esda tuting (5.3 boshidagi ogohlantirish): andozalarni faqat **haqiqiy muammoni** hal qilganda qo'llang.
</details>
