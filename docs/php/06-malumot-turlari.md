# 1.3 Ma'lumot turlari

[⬅️ Oldingi: 1.2 O'zgaruvchilar (variables)](./05-ozgaruvchilar.md) · [🏠 README](./README.md) · [Keyingi: 1.4 Amallar (operatorlar) ➡️](./07-amallar.md)

---

O'zgaruvchi ichiga turli xil ma'lumot saqlash mumkin: matn, son, "ha/yo'q" qiymati va boshqalar. Bularning har biri — alohida **tur** (type). PHP'ning asosiy turlarini ko'rib chiqamiz. Buni bilish muhim, chunki turli turdagi ma'lumotlar turlicha ishlaydi.

### 1) Matn (string) — harflar, so'zlar, gaplar

Matn doim **qo'shtirnoq** (yoki bittalik tirnoq) ichida yoziladi:

```php
<?php
$ism = "Ali";
$gap = "Bugun havo issiq";
$telefon = "998901234567";   // bu ham matn (raqam ko'rinishida bo'lsa ham)
```

> Diqqat: `"998901234567"` — bu matn, son emas, chunki tirnoq ichida. Telefon raqami, pasport raqami kabilarni matn sifatida saqlash to'g'ri — chunki ular bilan hisob-kitob qilmaymiz.

### 2) Butun son (integer) — kasrsiz sonlar

Tirnoqsiz yozilgan, nuqtasiz sonlar:

```php
<?php
$yosh = 19;
$narx = 5000;
$temperatura = -10;   // manfiy son ham bo'ladi
```

Bular bilan matematik amallar bajarish mumkin (qo'shish, ayirish va h.k.).

### 3) Kasr son (float) — nuqtali sonlar

Kasr qism bo'lgan sonlar. Kasr **nuqta** bilan yoziladi (vergul emas!):

```php
<?php
$narx = 19.99;
$ball = 4.5;
$pi = 3.14;
```

> Eslatma: o'zbekchada "uch butun o'n to'rt" deb vergul ishlatamiz, lekin dasturlashda **nuqta** ishlatiladi: `3.14`.

### 4) Mantiqiy qiymat (boolean) — faqat "ha" yoki "yo'q"

Ba'zan bizga faqat ikki holatdan biri kerak bo'ladi: rost yoki yolg'on, ha yoki yo'q, yoniq yoki o'chiq. Buni `true` (rost) yoki `false` (yolg'on) bilan ifodalaymiz:

```php
<?php
$tizimga_kirgan = true;    // ha, kirgan
$xat_yuborilgan = false;   // yo'q, yuborilmagan
```

Bu tur ayniqsa "shartlar" mavzusida (1.6) juda kerak bo'ladi. Hozircha shuni bilsangiz yetarli: `true` — rost, `false` — yolg'on.

### 5) Bo'shliq (null) — "hech narsa"

`null` — "bu qutida hozircha hech narsa yo'q" degani:

```php
<?php
$tanlangan_mahsulot = null;   // hali hech narsa tanlanmagan
```

Buni keyinroq ko'proq ishlatamiz. Hozircha shunchaki "bo'sh, hech narsa yo'q" deb eslang.

### Turni tekshirish

O'zgaruvchining turi nima ekanini bilish uchun `var_dump()` ishlatiladi. Bu — kodni tekshirishda juda foydali vosita:

```php
<?php
$ism = "Ali";
$yosh = 19;
$narx = 19.99;
$kirgan = true;

var_dump($ism);    // string(3) "Ali"  → matn, 3 ta harf
var_dump($yosh);   // int(19)           → butun son
var_dump($narx);   // float(19.99)      → kasr son
var_dump($kirgan); // bool(true)        → mantiqiy
```

`var_dump` o'zgaruvchining ham turini, ham qiymatini ko'rsatadi. Kod kutilganidek ishlamayotganda, "o'zgaruvchida nima turibdi ekan?" deb tekshirish uchun ishlatiladi.

### Nima uchun tur muhim?

Chunki turli turdagi ma'lumotlar turlicha "muomala qiladi". Masalan, ikkita sonni qo'shsangiz — ular matematik qo'shiladi. Ikkita matnni esa "qo'shsangiz" — boshqacha natija bo'ladi:

```php
<?php
$a = 5;
$b = 3;
echo $a + $b;     // 8  (sonlar matematik qo'shildi)
```

Buni keyingi bo'limda — amallar mavzusida — batafsil ko'ramiz.

### Mashqlar

**Oson**
1. Har bir turga bittadan o'zgaruvchi yarating: matn, butun son, kasr son, mantiqiy qiymat.
2. Ularning har birini `var_dump` bilan tekshiring va natijani ko'ring.
3. `19` (son) va `"19"` (matn) ni alohida `var_dump` qiling — natijadagi farqni ko'ring.
4. Kasr sonni vergul bilan yozib ko'ring (`$x = 3,14;`) — xato chiqishini ko'ring, keyin nuqta bilan tuzating.

**O'rta**
5. Telefon raqamini saqlash uchun qaysi tur to'g'ri — matnmi yoki sonmi? O'z fikringizni izoh bilan yozing va shunday saqlang.
6. `$kirgan = true;` va `$kirgan = false;` larni alohida `var_dump` qiling.
7. Bitta o'zgaruvchiga avval matn, keyin son saqlang (`$x = "salom";` keyin `$x = 100;`), har safar `var_dump` qiling — turning o'zgarishini kuzating.

**Qiyin**
8. Mahsulot haqida ma'lumotni turli o'zgaruvchilarda saqlang: nomi (matn), narxi (kasr son), soni (butun son), mavjudligi (mantiqiy). Hammasini chiqaring va `var_dump` bilan tekshiring.

<details markdown="1">
<summary>Yechim — 3</summary>

```php
<?php
var_dump(19);     // int(19)        → bu butun son
var_dump("19");   // string(2) "19" → bu matn, 2 ta belgidan iborat
```

Ko'rib turganingizdek, ekranda `19` bir xil ko'rinsa ham, kompyuter uchun ular **ikki xil narsa**: biri son (u bilan hisob qilish mumkin), ikkinchisi matn (ikkita belgi: "1" va "9"). Bu farqni tushunish keyinroq juda asqotadi.
</details>

<details markdown="1">
<summary>Yechim — 8 (mahsulot ma'lumoti, har xil turlar)</summary>

```php
<?php
$nom = "Noutbuk";       // matn (string)
$narx = 7499.99;        // kasr son (float)
$soni = 3;              // butun son (int)
$mavjud = true;         // mantiqiy (bool)

echo "$nom — $narx so'm, $soni dona<br>";

var_dump($nom);     // string(7) "Noutbuk"
var_dump($narx);    // float(7499.99)
var_dump($soni);    // int(3)
var_dump($mavjud);  // bool(true)
```
Bitta mahsulot — to'rtta har xil turdagi ma'lumot. `var_dump` har birining turini aniq ko'rsatadi. E'tibor bering: `$narx` kasr bo'lgani uchun `float`, `$soni` butun bo'lgani uchun `int`.
</details>
