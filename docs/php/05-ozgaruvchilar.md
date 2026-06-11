# 1.2 O'zgaruvchilar (variables)

[⬅️ Oldingi: 1.1 Kod qanday yoziladi (sintaksis)](./04-kod-qanday-yoziladi.md) · [🏠 README](./README.md) · [Keyingi: 1.3 Ma'lumot turlari ➡️](./06-malumot-turlari.md)

---

### O'zgaruvchi nima?

Tasavvur qiling, sizda bir nechta **qutilar** bor va har biriga nom yozib qo'ygansiz: "ism", "yosh", "narx". Har bir qutiga biror narsa solib qo'yasiz, keyin kerak bo'lganda qutining nomini aytib, ichidagini olasiz.

**O'zgaruvchi — aynan shunday "nomlangan quti".** Ichiga biror ma'lumot (matn, son) saqlaysiz, keyin nomi orqali ishlatasiz.

PHP'da o'zgaruvchi `$` belgisi bilan boshlanadi:

```php
<?php
$ism = "Ali";
$yosh = 19;

echo $ism;
echo "<br>";
echo $yosh;
```

Bu kod ekranga `Ali` va `19` chiqaradi.

Tushuntiramiz:
- **`$ism`** — bu o'zgaruvchi. `$` belgisidan keyin nom keladi (`ism`).
- **`=`** — bu "tenglik" emas, balki "**saqlash**" belgisi. `$ism = "Ali"` degani: "`Ali` degan matnni `ism` qutisiga sol".
- Keyin `echo $ism` deganimizda — quti ichidagi narsa (`Ali`) ekranga chiqadi.

> **Muhim:** `$ism = "Ali"` — bu "ism Ali'ga teng" degani EMAS. Bu "Ali'ni ism qutisiga joyla" degani. Chapdagi quti, o'ngdagi unga solinadigan narsa. Yo'nalish — o'ngdan chapga.

### Nega "o'zgaruvchi" deyiladi?

Chunki ichidagi narsani **o'zgartirish** mumkin:

```php
<?php
$narx = 1000;
echo $narx;        // 1000 chiqadi
echo "<br>";

$narx = 5000;      // endi qutiga yangi qiymat solindi
echo $narx;        // 5000 chiqadi
```

Quti bitta, lekin ichidagi narsa o'zgardi. Oxirgi solingan qiymat saqlanadi.

### O'zgaruvchini matn bilan birga chiqarish

Ko'pincha o'zgaruvchini matn bilan aralashtirib chiqarish kerak bo'ladi. Buning ikki yo'li bor.

**1-yo'l: nuqta bilan ulash.** PHP'da `.` (nuqta) ikkita narsani bir-biriga ulaydi:

```php
<?php
$ism = "Ali";
echo "Salom, " . $ism . "!";   // Salom, Ali!
```

**2-yo'l: o'zgaruvchini to'g'ridan-to'g'ri qo'shtirnoq ichiga yozish:**

```php
<?php
$ism = "Ali";
echo "Salom, $ism!";   // Salom, Ali!
```

Ikkala usul ham `Salom, Ali!` chiqaradi. Boshida sizga qulayrog'ini tanlang.

> **Diqqat:** o'zgaruvchini qo'shtirnoq (`" "`) ichida yozsangiz, uning qiymati chiqadi. Lekin **bittalik tirnoq** (`' '`) ichida yozsangiz, o'zgaruvchi qiymati EMAS, balki nomi xuddi o'zidek chiqadi:
> ```php
> $ism = "Ali";
> echo "Salom $ism";   // Salom Ali
> echo 'Salom $ism';   // Salom $ism  (qiymat chiqmadi!)
> ```
> Shuning uchun o'zgaruvchini chiqarganda **qo'shtirnoq** ishlating.

### O'zgaruvchiga nom berish qoidalari

- `$` bilan boshlanadi: `$ism`, `$narx`.
- Faqat harf, raqam va `_` (pastki chiziq) ishlatiladi. Bo'sh joy bo'lmaydi.
- Nom raqam bilan boshlanmaydi: `$1ism` — xato; `$ism1` — to'g'ri.
- **Mazmunli nom bering:** `$narx` deb yozing, `$n` yoki `$x` emas. Keyinroq kodni o'qiganingizda nima saqlanganini darrov tushunasiz.
- Bir nechta so'zli nomda odatda shunday yoziladi: `$talabaIsmi` yoki `$talaba_ismi`.

### Mashqlar

**Oson**
1. `$ism` o'zgaruvchisiga o'z ismingizni saqlang va ekranga chiqaring.
2. `$shahar` o'zgaruvchisiga shaharingizni saqlang va `"Men ... da yashayman"` shaklida chiqaring.
3. `$narx` o'zgaruvchisiga `2000` saqlang, chiqaring, keyin `3500` saqlab qayta chiqaring.
4. Ikkita o'zgaruvchi (`$ism`, `$yosh`) yarating va ikkalasini bitta gap ichida chiqaring.

**O'rta**
5. `$ism` va `$familiya` o'zgaruvchilarini yarating, ularni bo'sh joy bilan ulab, to'liq ismni chiqaring.
6. Bir o'zgaruvchini qo'shtirnoq ichida (`"$ism"`) va bittalik tirnoq ichida (`'$ism'`) chiqaring — farqini ko'ring.
7. `$mahsulot` va `$narx` o'zgaruvchilari bilan: `"Olma narxi: 5000 so'm"` shaklida chiqaring.

**Qiyin**
8. To'liq tashrifnoma yarating: `$ism`, `$kasb`, `$telefon`, `$shahar` o'zgaruvchilari bilan, har birini alohida qatorda (`<br>` bilan) chiroyli chiqaring.
9. Ikkita o'zgaruvchi qiymatini bir-biriga almashtiring (`$a` da turgan narsa `$b` ga, `$b` dagi `$a` ga o'tsin). Buning uchun uchinchi vaqtinchalik o'zgaruvchi kerak bo'lishi mumkin — o'ylab ko'ring.

<details markdown="1">
<summary>Yechim — 5</summary>

```php
<?php
$ism = "Ali";
$familiya = "Valiyev";
echo $ism . " " . $familiya;   // Ali Valiyev
```
Bu yerda `.` belgisi ism, bo'sh joy (`" "`) va familiyani birlashtiradi.
</details>

<details markdown="1">
<summary>Yechim — 8 (to'liq tashrifnoma)</summary>

```php
<?php
$ism = "Ali Valiyev";
$kasb = "Dasturchi";
$telefon = "+998 90 123 45 67";
$shahar = "Toshkent";

echo "Ism: $ism<br>";
echo "Kasb: $kasb<br>";
echo "Telefon: $telefon<br>";
echo "Shahar: $shahar";
```
Bu yerda har bir ma'lumot o'zgaruvchida saqlanadi va qo'shtirnoq ichida `$ism` ko'rinishida chiqariladi (1.2'dagi interpolatsiya). Avvalgi mashqdagi "qotirilgan" matndan farqi — endi qiymatni bir joyda o'zgartirsak, hamma joyda yangilanadi.
</details>

<details markdown="1">
<summary>Yechim — 9 (qiymatlarni almashtirish)</summary>

```php
<?php
$a = "olma";
$b = "anor";

// To'g'ridan-to'g'ri $a = $b qilsak, $a dagi "olma" yo'qoladi.
// Shuning uchun avval vaqtinchalik qutiga saqlaymiz:
$vaqtinchalik = $a;   // "olma" ni saqlab qo'ydik
$a = $b;              // endi $a = "anor"
$b = $vaqtinchalik;   // $b = "olma"

echo $a;   // anor
echo "<br>";
echo $b;   // olma
```
Bu — boshlovchilar uchun klassik mashq. "Uchinchi quti" hiylasini tushunish muhim.
</details>
