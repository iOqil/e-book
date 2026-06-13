# NativePHP — PHP bilan Desktop va Mobil ilovalar

Bu kitob **Laravel biladigan** PHP dasturchini NativePHP bo'yicha desktop va mobil ilova yozadigan darajaga olib chiqadi. NativePHP — Laravel asosida qurilgan freymvork: bitta PHP/Laravel kod bazasidan **desktop** (Windows/macOS/Linux, Electron orqali) va **mobil** (iOS/Android) ilovalar yasaladi. Asosiy g'oya — ilova ichida **webview** ishlaydi, unga PHP runtime'i **bundled** (desktop) yoki **on-device** (mobil) tarzda biriktiriladi; siz odatdagidek Blade/Livewire bilan UI yozasiz, NativePHP esa oynalar, menyu, bildirishnoma, kamera, GPS, biometrika kabi **native** imkoniyatlarni PHP fasadlari orqali ochib beradi.

> 🏗️ Arxitektura: **webview + bundled/on-device PHP**. Desktop'da Electron oynasi Laravel ilovangizni mahalliy server orqali ko'rsatadi va PHP binari ilova ichiga joylanadi; mobil'da PHP qurilmaning o'zida ishlaydi. Natijada — bitta kod bazasi, ko'p platforma.

> ℹ️ Bu kitob siz **Laravel asoslarini** (routing, Blade, Eloquent, fasadlar, service container, Artisan) bilasiz deb hisoblaydi. Laravel yangi bo'lsa, avval [Laravel kitobini](../laravel/README.md) o'qing.

> ⚠️ **HALOL eslatma.** Kitobdagi **Laravel/PHP kodi tekshirilgan** va ishonchli. Ammo **GUI, qurilma (kamera/GPS/biometrika) va build/packaging bloklari illustrativ** — ularni real ishga tushirish uchun haqiqiy muhit kerak: desktop uchun **Node.js + Electron**, iOS uchun **macOS + Xcode**, Android uchun **Android SDK**. NativePHP versiyalari tez o'zgaradi, shuning uchun har doim rasmiy hujjat bilan solishtirib boring. Bu yerdagi maqsad — tushuncha va PHP tarafdagi to'g'ri yondashuvni berish.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. Avval **Asoslar** (I qism) va **Desktop** (II qism) ni puxta o'zlashtiring — mobil qism shu poydevorga quriladi.
3. PHP/Laravel kodini o'z muhitingizda yozing; native va build bloklarini esa rasmiy NativePHP hujjati bilan birga ko'ring.
4. Kamida bitta loyihani (kapston, 18-bob) boshidan oxirigacha o'zingiz yig'ing.

## Talab

| Kerak | Daraja |
|---|---|
| Laravel asoslari (Blade, Eloquent, fasad, Artisan) | **Shart** |
| PHP 8.2+ va Composer | Shart |
| Kompyuter (Windows / macOS / Linux) | Shart |
| Node.js + Electron (desktop build uchun) | Desktop bobiga |
| macOS + Xcode (iOS) / Android SDK (Android) | Mobil bobiga |
| Terminal bilan tanishlik | Foydali |

---

## Mundarija

### I qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [NativePHP nima](./01-nativephp-nima.md) | NativePHP falsafasi — bitta Laravel kod bazasidan desktop va mobil ilova; webview + bundled/on-device PHP arxitekturasi; Electron tarafi va mobil tarafi farqi; nima uchun va qachon ishlatish kerak. |
| 02 | [Muhit va Laravel asos](./02-muhit-laravel-asos.md) | Loyiha muhitini tayyorlash: PHP/Composer/Laravel, NativePHP paketini o'rnatish; desktop uchun Node/Electron, mobil uchun talablar; toza Laravel skeletini NativePHP uchun moslash. |
| 03 | [Birinchi desktop ilova](./03-birinchi-desktop-ilova.md) | "Salom dunyo" desktop ilovasi: NativePHP service provider, ilovani ishga tushirish, birinchi oynani ochish; dev oqimi (`native:run` / `composer native:dev`) va ilova hayot tsikli. |

### II qism — Desktop chuqur

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 04 | [Window management](./04-window-management.md) | Oynalar bilan ishlash: `Window` fasadi, bir nechta oyna, o'lcham/joylashuv, modal va frameless oynalar, oyna hodisalari va oynalararo aloqa. |
| 05 | [Menyu, tray va shortcut](./05-menyu-tray-shortcut.md) | Ilova menyusi (menu bar), kontekst menyu, tizim tray ikonkasi va uning menyusi, global klaviatura shortcut'lari; native his beradigan desktop UX. |
| 06 | [Native UI: notification va dialog](./06-native-ui-notification-dialog.md) | Tizim bildirishnomalari (`Notification`), fayl tanlash/saqlash dialoglari, ogohlantirish/tasdiq oynalari, clipboard bilan ishlash — operatsion tizimning native elementlari. |
| 07 | [System, child process va fayl](./07-system-childprocess-fayl.md) | Tizim bilan ishlash: tashqi jarayonlarni ishga tushirish (child process), fon vazifalari, foydalanuvchi fayl tizimiga kirish, ilova ma'lumotlari uchun papkalar. |
| 08 | [Local data: SQLite va settings](./08-local-data-sqlite-settings.md) | Ilova ichida mahalliy ma'lumot saqlash: bundled SQLite bazasi va Eloquent, NativePHP `Settings` bilan sozlamalar, migratsiyalar va data joylashuvi. |
| 09 | [Desktop UI: Blade va Livewire](./09-desktop-ui-blade-livewire.md) | Desktop UI'ni Blade va Livewire bilan qurish; reaktiv komponentlar, native imkoniyatlarni UI bilan bog'lash, desktop'ga mos dizayn va navigatsiya. |

### III qism — Mobil

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 10 | [Mobil asoslari](./10-mobil-asoslari.md) | NativePHP mobil tomoni: on-device PHP runtime, iOS/Android farqi, mobil loyiha tuzilishi, emulyator/simulyatorda ishga tushirish va dev oqimi. |
| 11 | [Mobil UI va navigatsiya](./11-mobil-ui-navigatsiya.md) | Mobil UI: ekran o'lchamlariga moslash, sahifalararo navigatsiya, native his beradigan komponentlar, gesture va mobil UX pattern'lari. |
| 12 | [Qurilma: camera, geo, scanner](./12-qurilma-camera-geo-scanner.md) | Qurilma imkoniyatlari: kamera va galereya, geolokatsiya (GPS), QR/barcode skaner; ruxsatlar (permissions) bilan ishlash va ma'lumotni Laravel'ga uzatish. |
| 13 | [Qurilma: biometrics, secure storage, push](./13-qurilma-biometrics-securestorage-push.md) | Biometrik autentifikatsiya (Face ID / barmoq izi), maxfiy ma'lumotni xavfsiz saqlash (secure storage), push bildirishnomalar; mobil xavfsizlik asoslari. |
| 14 | [Mobil offline data](./14-mobil-offline-data.md) | Internetsiz ishlash: on-device SQLite, mahalliy keshlash, offline-first yondashuv, ulanish tiklanganda server bilan sinxronlash strategiyalari. |

### IV qism — Sifat, build va deploy

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 15 | [Testlash va debugging](./15-testlash-debugging.md) | NativePHP ilovani testlash: Laravel testlari (Pest/PHPUnit), native qatlamni mock qilish, desktop/mobil debug usullari, log va xatolarni kuzatish. |
| 16 | [Desktop build va packaging](./16-desktop-build-packaging.md) | Desktop ilovani yig'ish: `native:build`, Windows/macOS/Linux uchun paketlash, ikonka va metadata, kod imzolash (code signing) va distributsiya asoslari. |
| 17 | [Mobil build va deploy](./17-mobil-build-deploy.md) | Mobil ilovani yig'ish va tarqatish: iOS uchun Xcode/App Store, Android uchun APK/AAB va Play Store, imzolash sertifikatlari, versiyalash va relizga tayyorlash. |
| 18 | [Kapston loyiha](./18-kapston.md) | Butun kitobni bog'laydigan to'liq loyiha: bitta Laravel kod bazasidan desktop va mobil ilova — local data, native imkoniyatlar, offline, test va build — boshidan oxirigacha. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
