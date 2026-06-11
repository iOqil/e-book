# 1.4 Amallar (operatorlar)

[⬅️ Oldingi: 1.3 Ma'lumot turlari](./06-malumot-turlari.md) · [🏠 README](./README.md) · [Keyingi: 1.5 Matn bilan ishlash (string) ➡️](./08-matn-bilan-ishlash.md)

---

**Operator** — bu ma'lumot ustida biror amal bajaradigan belgi. Masalan, `+` qo'shadi, `-` ayiradi. Keling, eng kerakli amallarni ko'rib chiqamiz.

### Matematik amallar

```php
<?php
$a = 10;
$b = 3;

echo $a + $b;   // 13  (qo'shish)
echo "<br>";
echo $a - $b;   // 7   (ayirish)
echo "<br>";
echo $a * $b;   // 30  (ko'paytirish)
echo "<br>";
echo $a / $b;   // 3.333...  (bo'lish)
echo "<br>";
echo $a % $b;   // 1   (qoldiq: 10 ni 3 ga bo'lganda qoldiq)
```

Ko'pchiligi maktab matematikasiga o'xshaydi. Faqat ikkitasiga e'tibor bering:
- **`*`** — ko'paytirish (× emas, yulduzcha).
- **`%`** — bu **qoldiq** topadi. `10 % 3` degani: "10 ni 3 ga bo'lganda nechta qoldiq qoladi?" → 3×3=9, qoldiq 1. Bu amal keyinroq (masalan, juft/toq son aniqlashda) juda foydali bo'ladi.

### Amallar tartibi

Maktabdagidek: avval ko'paytirish/bo'lish, keyin qo'shish/ayirish. Tartibni o'zgartirish uchun qavs ishlating:

```php
<?php
echo 2 + 3 * 4;     // 14  (avval 3*4=12, keyin +2)
echo "<br>";
echo (2 + 3) * 4;   // 20  (avval qavs ichi 2+3=5, keyin *4)
```

### O'zgaruvchini o'zgartirish (qisqa yozuv)

Ko'pincha o'zgaruvchining qiymatini oshirish kerak bo'ladi:

```php
<?php
$ball = 10;
$ball = $ball + 5;   // $ball endi 15
echo $ball;
```

`$ball = $ball + 5` — "ballning hozirgi qiymatiga 5 qo'shib, qayta ballga sol" degani. Buni qisqaroq yozish mumkin:

```php
<?php
$ball = 10;
$ball += 5;   // yuqoridagining qisqasi: $ball = $ball + 5
echo $ball;   // 15
```

Shunga o'xshash qisqa yozuvlar:
- `$x += 5;` → `$x = $x + 5`
- `$x -= 5;` → `$x = $x - 5`
- `$x *= 2;` → `$x = $x * 2`
- `$x++;` → `$x ni 1 ga oshir` (`$x = $x + 1`)
- `$x--;` → `$x ni 1 ga kamaytir`

`$x++` ayniqsa sikllar mavzusida (1.7) doim ishlatiladi.

### Matnlarni ulash

Sonlarda `+` qo'shish edi. Matnlarni esa ulash uchun `.` (nuqta) ishlatiladi (buni 1.2'da ko'rgan edik):

```php
<?php
$ism = "Ali";
$salom = "Salom, " . $ism;   // Salom, Ali
echo $salom;
```

> **Muhim farq:** sonlarni qo'shganda `+`, matnlarni ulaganda `.`. Buni aralashtirib yubormang.

### Taqqoslash amallari

Ikki narsani solishtirish uchun. Bu amallar natijasi doim `true` (rost) yoki `false` (yolg'on) bo'ladi. Ular asosan "shartlar" (1.6) bilan birga ishlatiladi:

```php
<?php
$a = 10;
$b = 5;

var_dump($a > $b);    // true   (a, b dan katta?)
var_dump($a < $b);    // false  (a, b dan kichik?)
var_dump($a == $b);   // false  (a, b ga teng?)
var_dump($a != $b);   // true   (a, b ga teng emas?)
var_dump($a >= 10);   // true   (a, 10 dan katta yoki teng?)
var_dump($a <= 9);    // false  (a, 9 dan kichik yoki teng?)
```

E'tibor bering:
- Tenglikni tekshirishda **ikkita** teng belgisi (`==`) ishlatiladi. Bitta `=` — bu "saqlash" edi (1.2). Buni aralashtirib yuborish — boshlovchilarda eng ko'p uchraydigan xato!
  - `$a = 5` → "5 ni a ga sol"
  - `$a == 5` → "a, 5 ga tengmi?"
- `!=` — "teng emas".

### Mashqlar

**Oson**
1. Ikkita son yarating va ularning yig'indisi, ayirmasi, ko'paytmasini chiqaring.
2. `17 % 5` ni hisoblang va natijani ko'ring (qoldiq necha?).
3. `$ball = 100;` yarating, `$ball += 50;` qiling va chiqaring.
4. `$soni = 5;` yarating, `$soni++;` qiling va chiqaring (necha bo'ldi?).
5. `2 + 3 * 4` va `(2 + 3) * 4` natijalarini solishtiring.

**O'rta**
6. Do'kon hisobi: `$narx = 5000;` va `$soni = 3;` — umumiy summani (`narx * soni`) hisoblang.
7. Ikkita son teng yoki teng emasligini `==` va `!=` bilan tekshiring (`var_dump` orqali).
8. `$a = 10; $b = 20;` — `$a > $b` va `$a < $b` natijalarini chiqaring.
9. Bir o'zgaruvchining qiymatini avval `*= 2`, keyin `+= 10` qilib o'zgartiring, har bosqichda chiqaring.

**Qiyin**
10. To'liq xarid hisobi: 3 ta mahsulot (har birining narxi va soni), umumiy summani hisoblang va chiqaring.
11. Ikki xonali sonning birliklar xonasini toping. Maslahat: `% 10` (10 ga bo'lgandagi qoldiq) birliklar xonasini beradi. Masalan, `47 % 10 = 7`.

<details markdown="1">
<summary>Yechim — 6</summary>

```php
<?php
$narx = 5000;
$soni = 3;
$umumiy = $narx * $soni;
echo "Umumiy summa: " . $umumiy . " so'm";   // Umumiy summa: 15000 so'm
```
</details>

<details markdown="1">
<summary>Yechim — 10 (to'liq xarid hisobi)</summary>

```php
<?php
$jami = 0;

$jami += 5000 * 3;     // 1-mahsulot: narx 5000, 3 dona = 15000
$jami += 12000 * 2;    // 2-mahsulot: 24000
$jami += 800 * 10;     // 3-mahsulot: 8000

echo "Umumiy summa: " . $jami . " so'm";   // 47000 so'm
```
Har bir mahsulot uchun `narx * soni` ni `$jami`ga qo'shamiz (`+=`). Oxirida `$jami` — butun xarid summasi. (Keyinroq, massiv va sikllar bilan, buni yanada chiroyli yozish mumkin bo'ladi.)
</details>

<details markdown="1">
<summary>Yechim — 11</summary>

```php
<?php
$son = 47;
$birliklar = $son % 10;   // 47 ni 10 ga bo'lganda qoldiq = 7
echo "Birliklar xonasi: " . $birliklar;   // 7
```

`% 10` har doim oxirgi raqamni beradi: `123 % 10 = 3`, `90 % 10 = 0`. Bu kichik hiyla turli joyda asqotadi.
</details>
