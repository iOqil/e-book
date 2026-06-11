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

if ($holat == Holat::Yetkazildi) {
    echo "Buyurtma yetkazildi";
}
```

Tushuntiramiz:
- **`enum Holat { ... }`** — Holat degan enum yaratamiz.
- **`case Yangi;`** — har bir mumkin bo'lgan qiymat `case` bilan e'lon qilinadi.
- **`Holat::Yetkazildi`** — qiymatga shunday murojaat qilamiz (class'dagi static kabi, `::` bilan).

Endi `Holat::Yetkzildi` (xato yozsangiz) — PHP **darrov xato beradi**, chunki bunday `case` yo'q. Bu matnda mumkin emas edi. Enum sizni xatolardan himoyalaydi.

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

### Foydasi

1. **Xatosizlik:** faqat ruxsat etilgan qiymatlar. Xato matn yozib bo'lmaydi.
2. **Aniqlik:** kod o'qiganda `Holat::Yetkazildi` — `"yetkazildi"` matnidan ravshanroq.
3. **Bir joyda:** barcha mumkin bo'lgan holatlar bir joyda ro'yxatlangan.

Enum, masalan, holat (buyurtma holati), rol (foydalanuvchi roli: admin/oddiy), kun (hafta kunlari) kabi "cheklangan variantlar" uchun ideal.

### Mashqlar

**Oson**
1. `Holat` enum'ini yarating (`Yangi`, `Yolda`, `Yetkazildi`). Bir o'zgaruvchiga qiymat bering va `if` bilan tekshiring.
2. `Kun` enum'ini yarating (hafta kunlari) va bittasini tanlang.
3. `Rol` enum'ini yarating (`Admin`, `Oddiy`, `Mehmon`).
4. Qiymatli enum yarating (`Holat: string`) va `->value` ni chiqaring.
5. `Yonalish` enum'i (`Shimol`, `Janub`, `Sharq`, `Garb`) yarating.

**O'rta**
6. `Rol` enum'i bilan: foydalanuvchi roli `Admin` bo'lsa "Boshqaruv paneli", aks holda "Oddiy sahifa" chiqaring.
7. `Holat: string` enum'ining qiymatini bazaga saqlanadigandek `->value` orqali chiqaring.
8. Buyurtma class'i yarating, uning `holat` xususiyati enum turida bo'lsin (konstruktorda qabul qilsin).
9. `Baho` enum'i (`A`, `B`, `C`, `D`, `F`) yarating va bir nechta talaba bahosini saqlang.

**Qiyin**
10. `Buyurtma` class'i: konstruktor `holat`ni `Holat` enum sifatida olsin. `holatniOzgartir($yangiHolat)` metodi holatni yangilasin. `holatMatn()` metodi joriy holatni o'qiladigan matn ko'rinishida qaytarsin (`match` bilan).
11. Enum'ga metod qo'shish (PHP enum'larida metod bo'lishi mumkin!): `Holat` enum'iga `tavsif()` metodi qo'shing — har bir holat uchun o'zbekcha izoh qaytarsin (`match($this)` ishlatib).

<details markdown="1">
<summary>Yechim — 10 (Buyurtma holati)</summary>

```php
<?php
enum Holat {
    case Yangi;
    case Yolda;
    case Yetkazildi;
}

class Buyurtma {
    public $holat;

    public function __construct(Holat $holat) {   // tip — enum!
        $this->holat = $holat;
    }

    public function holatniOzgartir(Holat $yangiHolat) {
        $this->holat = $yangiHolat;
    }

    public function holatMatn(): string {
        return match($this->holat) {
            Holat::Yangi      => "Buyurtma qabul qilindi",
            Holat::Yolda      => "Buyurtma yo'lda",
            Holat::Yetkazildi => "Buyurtma yetkazildi",
        };
    }
}

$b = new Buyurtma(Holat::Yangi);
echo $b->holatMatn();              // Buyurtma qabul qilindi

$b->holatniOzgartir(Holat::Yolda);
echo "<br>" . $b->holatMatn();     // Buyurtma yo'lda
```
E'tibor bering: konstruktor va metod parametri tipi `Holat` (enum). Shuning uchun `holat`ga faqat haqiqiy `Holat` qiymati tushadi — xato matn ("yetkzildi") berib bo'lmaydi. `holatMatn()` esa `match` bilan har bir holatga o'qiladigan izoh beradi. Enum + tip e'loni + `match` — birgalikda juda ishonchli.
</details>

<details markdown="1">
<summary>Yechim — 11 (metodli enum)</summary>

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
