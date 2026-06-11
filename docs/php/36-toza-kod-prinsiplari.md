# 5.1 Toza kod prinsiplari

[⬅️ Oldingi: 4.6 Fayl bilan ishlash va fayl yuklash](./fayl-yuklash.md) · [🏠 README](./README.md) · [Keyingi: 5.2 MVC — loyihani tartibga solish ➡️](./37-mvc-loyihani-tartibga-solish.md)

---

Kod "ishlasa bo'ldi" emas. Yaxshi dasturchi **toza, o'qiladigan, oson o'zgartiriladigan** kod yozadi. Sababi: kodni bir marta yozasiz, lekin ko'p marta o'qiysiz va o'zgartirasiz (o'zingiz ham, boshqalar ham). Toza kod — vaqtingizni va asablaringizni tejaydi. Bu bo'limda asosiy odatlarni ko'ramiz.

### 1) Mazmunli nomlar

O'zgaruvchi, funksiya, class nomlari **nima ekanini** aytib turishi kerak:

```php
<?php
// ❌ Yomon — nima ekani noaniq
$x = 25;
$d = $x * 12;
function hsb($a, $b) { return $a * $b; }

// ✅ Yaxshi — nom o'zi tushuntiradi
$oylikMaosh = 25;
$yillikMaosh = $oylikMaosh * 12;
function maydonHisobla($eni, $boyi) { return $eni * $boyi; }
```

Yaxshi nom — eng yaxshi izoh. `$yillikMaosh` ni ko'rganda hech narsa tushuntirish shart emas. `$d` esa — jumboq.

### 2) Funksiya bitta ish qilsin

Bitta funksiya bitta aniq ishni bajarsin, juda uzun bo'lmasin. Agar funksiya "ham buni, ham buni, yana buni" qilayotgan bo'lsa — uni bo'ling:

```php
<?php
// ❌ Yomon — bitta funksiya hamma ishni qilyapti
function foydalanuvchiniQayta($data) {
    // tekshirish... bazaga yozish... email yuborish... hisobot... (50 qator)
}

// ✅ Yaxshi — har biri bitta ish, alohida funksiya
function malumotniTekshir($data) { /* faqat tekshiradi */ }
function bazagaSaqla($data) { /* faqat saqlaydi */ }
function emailYubor($email) { /* faqat email yuboradi */ }
```

Har bir funksiya kichik va bitta maqsadli bo'lsa: o'qish oson, sinash oson, xato topish oson, qayta ishlatish oson.

### 3) DRY — o'zingizni takrorlamang

**DRY = "Don't Repeat Yourself"** (o'zingizni takrorlamang). Agar bir xil kodni ikki-uch joyga nusxalayotgan bo'lsangiz — to'xtang. Uni funksiyaga oling:

```php
<?php
// ❌ Yomon — bir xil hisob 3 joyda takrorlangan
$narx1 = $asl1 + ($asl1 * 0.12);
$narx2 = $asl2 + ($asl2 * 0.12);
$narx3 = $asl3 + ($asl3 * 0.12);

// ✅ Yaxshi — bir marta funksiyada, qayta ishlatamiz
function qqsQoshib($narx) {
    return $narx + ($narx * 0.12);
}
$narx1 = qqsQoshib($asl1);
$narx2 = qqsQoshib($asl2);
$narx3 = qqsQoshib($asl3);
```

Foydasi: agar QQS 12% dan 15% ga o'zgarsa — bitta joyni (funksiyani) tuzatasiz, hamma joyga ta'sir qiladi. Takrorlangan kodda esa 3 joyni tuzatib, bittasini unutib qo'yish xavfi bor.

### 4) Foydali izohlar

Izoh (1.1) **nima** qilayotganini emas (kod buni o'zi ko'rsatadi), **nega** qilayotganingizni tushuntirsin:

```php
<?php
// ❌ Foydasiz izoh — kod allaqachon ko'rsatib turibdi
$yosh = $yosh + 1;   // yoshni bittaga oshiramiz

// ✅ Foydali izoh — NEGA shundayligini tushuntiradi
// Tug'ilgan kun o'tgani uchun yoshni yangilaymiz
$yosh = $yosh + 1;
```

Eng yaxshi kod — izohsiz ham tushunarli (mazmunli nomlar tufayli). Izohni faqat "nega" aniq bo'lmaganda qo'shing.

### 5) Bir xil uslub

Butun loyihada bir xil uslubda yozing: bir xil nomlash usuli (`$talabaIsmi` yoki `$talaba_ismi` — bittasini tanlang va doim shuni ishlating), bir xil joylashuv (chekinish/indentatsiya). Bir xil uslub — kodni o'qishni osonlashtiradi.

> **Asosiy g'oya:** kodni "6 oydan keyin bu yerga qaytib kelganimda o'zim tushunamanmi?" degan savol bilan yozing. Yoki "boshqa odam buni o'qiy oladimi?". Agar javob "ha" bo'lsa — toza kod yozyapsiz.

### Mashqlar

**Oson**
1. Yomon nomli o'zgaruvchilarni (`$x`, `$a`, `$temp`) mazmunli nomlarga o'zgartiring.
2. Bir xil takrorlangan kodni (masalan, 3 ta joyda narx hisobi) funksiyaga oling (DRY).
3. "Nima" qilayotganini takrorlaydigan foydasiz izohni "nega" tushuntiradigan izohga aylantiring.
4. Hamma ishni qiladigan uzun funksiyani 2-3 ta kichik funksiyaga bo'ling.

**O'rta**
5. Berilgan "iflos" kodni (yomon nomlar, takror, izohsiz) toza ko'rinishga keltiring.
6. O'zingizning oldingi mashqlaringizdan birini oling va toza kod prinsiplari bilan qayta yozing.
7. Bir nechta joyda ishlatiladigan mantiqni (masalan, sana formatlash) funksiyaga ajrating.

**Qiyin**
8. 4.2'dagi mini-loyihani toza kod nuqtai nazaridan ko'rib chiqing: takrorlangan kodni funksiyalarga oling, nomlarni yaxshilang. Masalan, har faylda ulanish kodini takrorlamaslik uchun (allaqachon `ulanish.php` da qildik), boshqa takrorlarni ham toping va bartaraf eting.

<details markdown="1">
<summary>Yechim — 5 (iflos kodni tozalash)</summary>

```php
<?php
// ❌ OLDIN — iflos:
$a = 50000;
$b = 3;
$c = $a * $b;
$d = $c + ($c * 0.12);
echo $d;

// ✅ KEYIN — toza:
function jamiNarxniHisobla($narx, $soni) {
    $oraliq = $narx * $soni;
    return $oraliq + ($oraliq * 0.12);   // QQS qo'shilgan yakuniy narx
}

$mahsulotNarxi = 50000;
$mahsulotSoni = 3;
$jamiNarx = jamiNarxniHisobla($mahsulotNarxi, $mahsulotSoni);
echo $jamiNarx;
```
Farqni ko'ring: nomlar o'zi tushuntiradi, mantiq funksiyada (qayta ishlatsa bo'ladi), kod o'qiladi. `$a`, `$b`, `$c`, `$d` jumboq edi; endi har bir narsa aniq.
</details>

<details markdown="1">
<summary>Yechim — 8 (mini-loyihani toza kod bilan ko'rib chiqish)</summary>

4.2'dagi mini-loyihani toza kod nuqtai nazaridan baholaymiz — qaysi prinsiplarni qo'llash kerak:

1. **DRY (ulanish):** bazaga ulanish allaqachon `ulanish.php` da, har faylda `require 'ulanish.php'` — ✅ to'g'ri (kod takrorlanmaydi).

2. **DRY (takroriy tekshiruv):** bir nechta faylda `htmlspecialchars(trim($_POST[...]))` takrorlanadi. Buni funksiyaga oling:

```php
<?php
// yordamchi.php
function inputOl($kalit) {
    return htmlspecialchars(trim($_POST[$kalit] ?? ""));
}
// Endi: $ism = inputOl('ism');  — bir joyda, hamma joyda ishlatiladi
```

3. **Mazmunli nomlar:** `$natija`, `$qator` o'rniga `$talabalar`, `$talaba` kabi aniq nomlar.

4. **Funksiya bitta ish qilsin:** `royxat.php` ham qo'shadi, ham ko'rsatadi — buni Model'ga (SQL) va View'ga (HTML) ajratish keyingi bo'lim (5.2 — MVC) vazifasi.

Asosiy g'oya: ishlaydigan kodni "tozalash" — takrorni funksiyaga olish, nomlarni aniqlash, vazifalarni ajratish. Bu kod hajmini emas, **tushunarliligini** oshiradi.
</details>
