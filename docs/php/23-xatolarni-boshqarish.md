# 2.10 Xatolarni boshqarish (try / catch)

[⬅️ Oldingi: 2.9 Enum — cheklangan tanlovlar](./22-enum-cheklangan-tanlovlar.md) · [🏠 README](./README.md) · [Keyingi: 3.1 Ma'lumotlar bazasi nima va nega kerak? ➡️](./24-malumotlar-bazasi-nima-va-nega-kerak.md)

---

### Muammo: xatolar dasturni "o'ldiradi"

Ba'zan kodda xato yuz beradi: foydalanuvchi noto'g'ri ma'lumot kiritadi, fayl topilmaydi, nolga bo'lish sodir bo'ladi. Agar buni boshqarmasangiz, dastur to'satdan to'xtaydi va foydalanuvchi xunuk xato xabarini ko'radi. Bizga xatolarni **chiroyli boshqarish** kerak.

### `try` / `catch` — xatoni "ushlash"

Asosiy g'oya: xato bo'lishi mumkin bo'lgan kodni `try` ("urinib ko'r") blokiga yozasiz. Agar xato yuz bersa, `catch` ("ushla") bloki uni ushlaydi va dastur to'xtamaydi:

```php
<?php
try {
    // Xato bo'lishi mumkin bo'lgan kod
    $natija = 10 / 0;   // nolga bo'lish — xato!
    echo $natija;
} catch (DivisionByZeroError $e) {
    // Xato yuz bersa — bu yer ishlaydi
    echo "Xato: nolga bo'lib bo'lmaydi!";
}

echo "<br>Dastur davom etmoqda...";   // dastur to'xtamadi
```

Nima sodir bo'ldi:
- **`try { ... }`** — "shu kodni bajarishga urinib ko'r".
- Ichida xato yuz berdi (nolga bo'lish).
- **`catch (...) { ... }`** — xato yuz berganda darrov bu yerga "sakraydi" va xato xabarini chiqaradi.
- Eng muhimi: dastur **to'xtamadi** — keyingi kod ("Dastur davom etmoqda...") ham ishladi.

`$e` — bu "xato haqidagi ma'lumot" (error obyekti). Undan xato haqida ma'lumot olish mumkin: `$e->getMessage()` xato matnini qaytaradi.

### O'zingiz xato "tashlash" — `throw`

Ba'zan o'zingiz xato signalini berishingiz kerak. Masalan, "yosh manfiy bo'lmasligi kerak". Buning uchun `throw` ("tashla") ishlatiladi:

```php
<?php
function yoshTekshir($yosh) {
    if ($yosh < 0) {
        throw new Exception("Yosh manfiy bo'lishi mumkin emas");
    }
    return "Yosh: " . $yosh;
}

try {
    echo yoshTekshir(-5);   // bu xato tashlaydi
} catch (Exception $e) {
    echo "Xatolik: " . $e->getMessage();   // Xatolik: Yosh manfiy bo'lishi mumkin emas
}
```

Tushuntiramiz:
- **`throw new Exception("...")`** — "xato signalini tashla, shu matn bilan". `throw` bajarilishi bilan funksiya darrov to'xtaydi va xato "yuqoriga" — uni chaqirgan `try` ga uchadi.
- `catch` uni ushlaydi va `$e->getMessage()` orqali xato matnini oladi.

Bu — ma'lumotni tekshirishning toza usuli: funksiya "men bu ma'lumot bilan ishlay olmayman" deb signal beradi, chaqiruvchi esa uni `try/catch` bilan boshqaradi.

### `finally` — har doim bajariladigan qism

Ba'zan, xato bo'ladimi-yo'qmi, biror ish **albatta** bajarilishi kerak (masalan, faylni yopish). Buning uchun `finally` bor:

```php
<?php
try {
    echo "Ish boshlandi<br>";
    throw new Exception("Biror xato");
} catch (Exception $e) {
    echo "Xato ushlandi<br>";
} finally {
    echo "Bu qism HAR DOIM bajariladi";   // xato bo'lsa ham, bo'lmasa ham
}
```

Quyidagi diagramma `try / catch / finally` oqimini ko'rsatadi: `try` ichida xato bo'lsa `catch` ushlaydi, bo'lmasa `catch` o'tkazib yuboriladi — `finally` esa har ikki holatda ham bajariladi va dastur to'xtamaydi:

![try / catch / finally oqimi: xato ushlash va finally har doim bajarilishi](rasmlar/phb-try-catch.svg)

### Nega foydali?

1. **Dastur qulamaydi:** xato bo'lsa ham, foydalanuvchiga chiroyli xabar berasiz.
2. **Nazorat:** xatolarni bir joyda, tartibli boshqarasiz.
3. **Ishonch:** "nima noto'g'ri ketishi mumkin"ni oldindan o'ylab, tayyor turasiz.

### Mashqlar

**Oson**
1. `try/catch` bilan nolga bo'lishni ushlang va chiroyli xabar chiqaring.
2. `throw new Exception(...)` bilan o'z xatongizni tashlang va ushlang.
3. Xato xabarini `$e->getMessage()` orqali chiqaring.
4. `finally` blokini qo'shing va u har doim ishlashini ko'ring.
5. `try` ichida xato bo'lmasa, `catch` ishlamasligini (faqat `try` ishlashini) ko'ring.

**O'rta**
6. `yoshTekshir($yosh)` funksiyasi: yosh manfiy yoki 150 dan katta bo'lsa xato tashlasin.
7. `bol($a, $b)` funksiyasi: `$b` nol bo'lsa xato tashlasin, aks holda bo'linmani qaytarsin.
8. `parolTekshir($parol)` funksiyasi: parol 8 belgidan qisqa bo'lsa xato tashlasin.
9. Bir nechta `throw` holatini bitta funksiyada qo'llang (turli noto'g'ri inputlar uchun turli xato xabarlari).

**Qiyin**
10. `Hisob` class'ining `pulYechish` metodini xato bilan ishlang: pul yetarli bo'lmasa `throw new Exception("Mablag' yetarli emas")`. Chaqirilganda `try/catch` bilan ushlang.
11. Foydalanuvchi ro'yxatdan o'tishini tekshiruvchi funksiya yozing: bo'sh ism, noto'g'ri email (`@` yo'q), qisqa parol — har biri uchun alohida xato tashlasin. `try/catch` bilan har bir holatni sinab ko'ring.
12. `finally` ning amaliy foydasini ko'rsating: "ulanish ochildi" → ish (xato bo'lishi mumkin) → `finally` da "ulanish yopildi" har doim chiqsin.

<details markdown="1">
<summary>Yechim — 10 (xavfsiz pul yechish, xato bilan)</summary>

```php
<?php
class Hisob {
    private $balans;

    public function __construct($balans) {
        $this->balans = $balans;
    }

    public function pulYechish($summa) {
        if ($summa > $this->balans) {
            throw new Exception("Mablag' yetarli emas. Balans: " . $this->balans);
        }
        $this->balans -= $summa;
        return $this->balans;
    }
}

$hisob = new Hisob(100000);

try {
    $hisob->pulYechish(150000);   // xato tashlaydi
} catch (Exception $e) {
    echo "Amal bajarilmadi: " . $e->getMessage();
    // Amal bajarilmadi: Mablag' yetarli emas. Balans: 100000
}
```
2.3'da `pulYechish` `false` qaytarardi. Bu yerda esa `throw` bilan **aniq xato** beramiz — chaqiruvchi nima uchun amal bajarilmaganini aniq biladi. Ikkala usul ham to'g'ri; `throw` murakkabroq holatlarda foydaliroq, chunki xato sababini aniq yetkazadi.
</details>

<details markdown="1">
<summary>Yechim — 11 (ro'yxatdan o'tishni tekshirish)</summary>

```php
<?php
function royxatdanOtkaz($ism, $email, $parol) {
    if (empty($ism)) {
        throw new Exception("Ism bo'sh bo'lmasligi kerak");
    }
    if (!str_contains($email, "@")) {
        throw new Exception("Email noto'g'ri (@ yo'q)");
    }
    if (strlen($parol) < 8) {
        throw new Exception("Parol kamida 8 belgidan iborat bo'lsin");
    }
    return "Ro'yxatdan o'tdingiz: " . $ism;
}

// Har xil holatlarni sinab ko'ramiz:
$testlar = [
    ["",      "a@b.uz", "12345678"],   // ism bo'sh
    ["Ali",   "xato",   "12345678"],   // email noto'g'ri
    ["Vali",  "v@b.uz", "123"],        // parol qisqa
    ["Guli",  "g@b.uz", "maxfiy123"],  // hammasi to'g'ri
];

foreach ($testlar as $t) {
    try {
        echo royxatdanOtkaz($t[0], $t[1], $t[2]) . "<br>";
    } catch (Exception $e) {
        echo "Xato: " . $e->getMessage() . "<br>";
    }
}
// Xato: Ism bo'sh bo'lmasligi kerak
// Xato: Email noto'g'ri (@ yo'q)
// Xato: Parol kamida 8 belgidan iborat bo'lsin
// Ro'yxatdan o'tdingiz: Guli
```
Funksiya har bir noto'g'ri holat uchun alohida, aniq xato tashlaydi. `try/catch` har birini ushlab, tegishli xabarni ko'rsatadi. Bu — formani tekshirishning toza usuli: funksiya "qoidani" biladi, chaqiruvchi "javobni" boshqaradi.
</details>

<details markdown="1">
<summary>Yechim — 12 (finally bilan ulanishni yopish)</summary>

```php
<?php
function malumotOqi($xatoBoladimi) {
    echo "Ulanish ochildi<br>";
    try {
        if ($xatoBoladimi) {
            throw new Exception("O'qishda xato yuz berdi");
        }
        echo "Ma'lumot o'qildi<br>";
    } catch (Exception $e) {
        echo "Xato: " . $e->getMessage() . "<br>";
    } finally {
        echo "Ulanish yopildi<br>";   // HAR DOIM bajariladi
    }
}

malumotOqi(false);
echo "---<br>";
malumotOqi(true);
// Ulanish ochildi / Ma'lumot o'qildi / Ulanish yopildi
// ---
// Ulanish ochildi / Xato: O'qishda xato yuz berdi / Ulanish yopildi
```
`finally` ning amaliy foydasi shu: xato bo'ladimi yoki yo'qmi, "ulanishni yopish" kabi tozalash ishi **har doim** bajariladi. Real kodda bu — fayl, baza ulanishi yoki boshqa resursni xato bo'lganda ham to'g'ri yopish uchun ishlatiladi.
</details>

---

> **2-QISM yakunlandi!** Bu — qo'llanmaning eng murakkab qismlaridan biri edi. Endi siz: class va obyekt, konstruktor, inkapsulyatsiya (public/private), meros, abstrakt class, interfeys, static, trait, enum va xatolarni boshqarishni bilasiz. Bu — katta, tartibli dasturlar yozishning asosi.
>
> Agar hammasi hali to'liq "o'tirmagan" bo'lsa — tabiiy. OOP'ni tushunish vaqt va mashq talab qiladi. Misollarni qayta yozib, o'zgartirib ko'ring. Keyingi qism — **ma'lumotlar bazasi:** ma'lumotni doimiy (dastur yopilgandan keyin ham) saqlash. Bu — haqiqiy, foydali dasturlar yozishning keyingi katta qadami.
