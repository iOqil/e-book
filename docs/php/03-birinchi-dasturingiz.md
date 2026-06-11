# 0.3 Birinchi dasturingiz

[⬅️ Oldingi: 0.2 PHP'ni kompyuteringizga o'rnatish](./02-phpni-kompyuteringizga-ornatish.md) · [🏠 README](./README.md) · [Keyingi: 1.1 Kod qanday yoziladi (sintaksis) ➡️](./04-kod-qanday-yoziladi.md)

---

An'anaga ko'ra, dasturlashda birinchi dastur — ekranga "Salom" deb yozish. Keling, shuni qilamiz.

### Faylni yaratish

1. VS Code'da, ochilgan `darslar` papkasida yangi fayl yarating: "File" → "New File".
2. Faylga nom bering: **`salom.php`**

> **Diqqat:** fayl nomi `.php` bilan tugashi shart. Bu — "bu PHP fayli" degani. Aynan shu kengaytma orqali kompyuter faylni PHP sifatida tushunadi.

### Kodni yozish

Faylga quyidagini yozing:

```php
<?php
echo "Salom, dunyo!";
```

Endi har bir qatorni tushuntiramiz:

- **`<?php`** — bu "PHP kodi shu yerdan boshlanadi" degan belgi. Har bir PHP fayli shu bilan ochiladi. Esda tuting: u `<?php` shaklida yoziladi (oxirida `php` so'zi bilan).
- **`echo`** — bu so'z "ekranga chiqar" degani. PHP'da biror narsani ko'rsatmoqchi bo'lsangiz, `echo` ishlatasiz.
- **`"Salom, dunyo!"`** — bu ekranga chiqadigan matn. Matn doim **qo'shtirnoq** (`" "`) ichida yoziladi.
- **`;`** (nuqtali vergul) — har bir buyruq oxirida qo'yiladi. Bu "buyruq tugadi" degani, xuddi gap oxiridagi nuqta kabi. **Uni unutmaslik muhim** — ko'p boshlovchilar shu sababli xatoga duch keladi.

### Dasturni ishga tushirish

1. XAMPP Control Panel'da Apache ishlab turganiga ishonch hosil qiling (yashil bo'lsin).
2. Brauzerni oching.
3. Manzil qatoriga yozing: **`http://localhost/darslar/salom.php`**
4. Enter bosing.

Ekranda **Salom, dunyo!** degan yozuv chiqishi kerak. Tabriklaymiz — siz birinchi dasturingizni yozdingiz va ishga tushirdingiz!

> **Manzil qanday tuziladi?** `http://localhost/` — bu sizning kompyuteringizdagi server. Undan keyin `htdocs` ichidagi yo'l yoziladi: `darslar/salom.php` — ya'ni `darslar` papkasidagi `salom.php` fayli.

Bu jarayonni sxemada ko'ramiz: brauzer serverga so'rov yuboradi, server PHP kodni bajaradi va tayyor natijani (HTML) qaytaradi.

![PHP qanday ishlaydi: brauzer so'rov yuboradi, server kodni bajaradi, javob qaytadi](rasmlar/pha-php-qanday-ishlaydi.svg)

### Agar ishlamasa?

Boshlovchilarda ko'p uchraydigan xatolar:
- **Bo'sh sahifa yoki xato:** `;` (nuqtali vergul) qo'yishni unutgandirsiz, yoki qo'shtirnoqni yopmagandirsiz.
- **Fayl topilmadi (404):** manzilni xato yozgandirsiz yoki fayl boshqa papkada. Fayl `htdocs/darslar` ichidaligiga ishonch hosil qiling.
- **Kod o'zi matn ko'rinishida chiqyapti:** Apache ishlamayapti yoki faylni `localhost` orqali emas, to'g'ridan-to'g'ri ochgansiz. Doim `http://localhost/...` orqali oching.

### Mashqlar

**Oson**
1. Yuqoridagi dasturni ishga tushiring va ekranda matnni ko'ring.
2. Matnni o'zgartiring: `"Salom, dunyo!"` o'rniga o'z ismingizni yozing (masalan, `"Mening ismim Ali"`).
3. `echo`dan keyingi matnni qo'shtirnoqsiz yozib ko'ring (`echo Salom;`) — xato chiqishini ko'ring va nega xato bo'lganini o'ylab ko'ring (matn doim qo'shtirnoq ichida bo'lishi kerak edi).
4. Oxiridagi `;` (nuqtali vergul)ni o'chirib, dasturni ishga tushiring — qanday xato chiqadi? Keyin uni qaytaring.

**O'rta**
5. Ikkita `echo` qatorini ketma-ket yozing (har birining oxirida `;` bo'lsin) va ikkita matn ham chiqishini ko'ring.
6. Bitta `echo` bilan o'zingiz haqingizda bir gap yozing (masalan: `"Men PHP o'rganyapman"`).

**Qiyin**
7. Uchta alohida fayl yarating (`birinchi.php`, `ikkinchi.php`, `uchinchi.php`), har birida boshqacha matn chiqsin. Har birini brauzerda alohida manzil bilan oching.

<details markdown="1">
<summary>Yechim — 5</summary>

```php
<?php
echo "Birinchi qator.";
echo "Ikkinchi qator.";
```

Brauzerda ikkala matn yonma-yon chiqadi: `Birinchi qator.Ikkinchi qator.`
Hozircha ular bir qatorda chiqadi — keyingi mavzularda matnni yangi qatorga tushirishni ham o'rganamiz.
</details>

<details markdown="1">
<summary>Yechim — 7 (uchta fayl)</summary>

Har bir faylni alohida yarating va ichiga boshqacha matn yozing:

```php
<?php
// birinchi.php
echo "Bu — birinchi fayl";
```
```php
<?php
// ikkinchi.php
echo "Bu — ikkinchi fayl";
```
```php
<?php
// uchinchi.php
echo "Bu — uchinchi fayl";
```
Keyin har birini brauzerda alohida oching: `http://localhost/darslar/birinchi.php`, `.../ikkinchi.php`, `.../uchinchi.php`. Maqsad — har bir `.php` fayl mustaqil sahifa ekanini his qilish.
</details>
