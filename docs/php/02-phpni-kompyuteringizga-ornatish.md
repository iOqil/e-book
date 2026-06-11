# 0.2 PHP'ni kompyuteringizga o'rnatish

[⬅️ Oldingi: 0.1 Dasturlash nima va PHP nima?](./01-dasturlash-nima-va-php-nima.md) · [🏠 README](./README.md) · [Keyingi: 0.3 Birinchi dasturingiz ➡️](./03-birinchi-dasturingiz.md)

---

PHP kodini yozish uchun ikkita narsa kerak:
1. **PHP dasturi** — yozgan kodingizni "tushunadigan" va ishga tushiradigan vosita.
2. **Matn muharriri (kod yozadigan dastur)** — kodni yozadigan joy.

Buni eng oson yo'li — **XAMPP** degan dasturni o'rnatish. XAMPP bitta o'rnatishda PHP'ni va kerakli barcha narsalarni birdaniga o'rnatib beradi. (Keyinroq, ma'lumotlar bazasi mavzusiga kelganda, XAMPP'dagi boshqa qismlar ham asqotadi.)

> Eslatma: bu yerda **Windows** kompyuter uchun tushuntiriladi, chunki ko'pchilik shundan foydalanadi. Mac yoki Linux'da ham XAMPP bor, o'rnatish jarayoni shunga o'xshash.

### 1-qadam: XAMPP'ni o'rnatish (Windows)

1. Brauzerda `apachefriends.org` saytiga kiring (bu XAMPP'ning rasmiy sayti).
2. "XAMPP for Windows" tugmasini bosib, o'rnatish faylini yuklab oling.
3. Yuklangan faylni ishga tushiring. Ochilgan oynalarda "Next" tugmasini bosib ketavering (standart sozlamalar yetarli).
4. Odatda XAMPP `C:\xampp` papkasiga o'rnatiladi.

### 2-qadam: Kod muharririni o'rnatish

Kodni oddiy "Bloknot"da ham yozish mumkin, lekin maxsus muharrir ishni ancha osonlashtiradi (xatolarni ko'rsatadi, ranglar bilan ajratadi).

Eng ko'p ishlatiladigani — **Visual Studio Code** (qisqacha **VS Code**), bepul:
1. `code.visualstudio.com` saytiga kiring.
2. Windows uchun yuklab oling va o'rnating.

### 3-qadam: Kod yozadigan papkani tayyorlash

XAMPP o'rnatilgach, `C:\xampp\htdocs` degan papka paydo bo'ladi. **Bu — muhim papka:** veb-saytlaringiz aynan shu yerda turishi kerak.

- `htdocs` ichida yangi papka yarating, masalan: `darslar`.
- VS Code'ni oching → "File" → "Open Folder" → `C:\xampp\htdocs\darslar` papkasini tanlang.

Endi siz shu papka ichida fayllar yaratasiz.

### 4-qadam: XAMPP'ni ishga tushirish

1. Boshlash menyusidan **XAMPP Control Panel**ni oching.
2. "Apache" qatorining yonidagi **"Start"** tugmasini bosing. Yashil rang paydo bo'lsa — ishladi.

Apache — bu kompyuteringizni "kichik server"ga aylantiradigan dastur. U ishlayotgan bo'lsa, brauzerda `http://localhost` manzili orqali fayllaringizni ochish mumkin bo'ladi.

Hammasi tayyor! Keyingi bo'limda birinchi dasturimizni yozamiz.

> Agar "Start" bosganda xato chiqsa (ko'pincha "port band" degan xato), bu boshqa dastur 80-portni egallaganini bildiradi. Hozircha bu kam uchraydi; agar duch kelsangiz, internetda "XAMPP Apache port 80 band" deb qidiring — oddiy yechimi bor.
