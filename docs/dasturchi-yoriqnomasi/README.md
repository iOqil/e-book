# Dasturchi yo'riqnomasi — kod yozuvchidan professional muhandisgacha

Bu kitob sizga **kod yozishni** o'rgatmaydi — buni boshqa kitoblar qiladi. Bu kitob sizga *professional dasturchi BO'LISHni* o'rgatadi. "Men kod yoza olaman" bilan "men muhandisman" o'rtasida katta jarlik bor, va aynan shu jarlikni bu kitob to'ldiradi: **dasturchi tafakkuri** (muammoni yechish, begona kodni o'qish, debugging), **toza kod hunari** (nomlash, modullik, xatolarni boshqarish, refactoring, texnik qarz), **sifat** (testlash madaniyati, code review, xavfsiz kod), **jamoada ishlash** (Agile, baholash, kommunikatsiya, hujjatlash, fikr-mulohaza), **unumdorlik** (vositalar, vaqt, o'rganishni o'rganish) va **karyera** (junior'dan senior'gacha, ish topish, intervyu, frilans, etika, barqarorlik).

> 🧭 **Til-mustaqil kitob.** Bu yerda gap sintaksisda emas, **kasbiy ko'nikmada**. Shuning uchun kitob biror dasturlash tiliga bog'lanmaydi: kod kerak bo'lganda psevdokod yoki qisqa, aniq misol (Python/JavaScript) beriladi, lekin g'oyalar har qanday tilda — siz PHP, Go, Java yoki Rust yozasizmi — bir xil amal qiladi.

> ⚖️ **HALOL eslatma.** Bu kitobdagi maslahatlar — **qonun emas, amaliy yo'l-yo'riq**. Dasturlash hunari ko'p jihatdan *kontekstga bog'liq*: bir jamoada to'g'ri narsa boshqasida noto'g'ri bo'lishi mumkin. Shuning uchun har bobda nafaqat "qanday qilish kerak", balki **qachon va nega** (hamda qachon *aks*ini qilish kerakligi) ham aytiladi. Bu yerda muhandislik tajribasi va keng qabul qilingan amaliyot bor — lekin yakuniy qaror har doim sizniki va kontekstingizniki.

> ℹ️ Bu kitob siz **kamida bitta tilda kod yoza olasiz** deb hisoblaydi (o'zgaruvchi, funksiya, sikl, oddiy dastur). Agar siz bunday loyihada hali ishlamagan bo'lsangiz ham, kitobni o'qishingiz mumkin — lekin eng katta foydani **birinchi real loyihangiz** yoki **birinchi ishingiz** atrofida olasiz, chunki bu yerdagi ko'p narsa amaliyotda "tushadi".

---

## Bu kitob kim uchun

- **Yangi dasturchi** — kod yozishni o'rgandingiz, endi *qanday qilib jamoada, real loyihada professional ishlashni* bilmoqchisiz.
- **Birinchi ishini izlayotgan** — rezyume, portfolio, intervyu va birinchi 90 kunga tayyorlanmoqchisiz.
- **O'sishni xohlovchi junior/mid** — senior darajaga nima yetishmayotganini aniq bilmoqchisiz.
- **Frilanser** — mijoz topish, baholash, kommunikatsiya va barqaror ishlashni o'rganmoqchisiz.
- **O'zini "yetarli emas" his qilayotgan** (impostor sindromi) — siz yolg'iz emassiz; oxirgi qism aynan shu haqida.

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qish shart emas, lekin tavsiya etiladi: kitob tafakkur → hunar → sifat → jamoa → unumdorlik → karyera tartibida quriladi. Agar aniq ehtiyojingiz bo'lsa (mas. intervyu), to'g'ridan-to'g'ri shu bobga o'ting.
2. Har bobning **"Mashqlar"** bo'limini ishlang — bu kitobda mashqlar ko'pincha amaliy/refleksiv (real kod refactor qilish, commit xabari yozish, vazifa baholash, o'z holatingizni tahlil qilish). Yagona "to'g'ri javob" bo'lmasligi mumkin — yechimlar namuna sifatida berilgan.
3. **O'qib qo'ymang — qo'llang.** Har bobdan keyin bitta narsani o'z loyihangizda yoki ishingizda sinab ko'ring. Bu kitobning butun qiymati amaliyotda.
4. Bu kitobni **boshqa kitoblar bilan birga** ishlating: bu yerda *kasb*, ularda *texnologiya*. Cross-link'lar orqali kerakli chuqurlikka o'ting.

---

## Mundarija

### I qism — Dasturchi tafakkuri va muammo yechish

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Kod yozuvchidan muhandisgacha](./01-kod-yozuvchidan-muhandisgacha.md) | "Kod yoza olish" vs "muhandis bo'lish" jarligi, professionalizm nimasi, bu kitob nima haqida, dasturchi mas'uliyati. |
| 02 | [Muammoni yechish san'ati](./02-muammoni-yechish-sanati.md) | Muammoni tushunish, bo'laklash, gipoteza, "rubber duck", qotib qolganda nima qilish, yechimga yondashuv. |
| 03 | [Begona kodni o'qish va tushunish](./03-begona-kodni-oqish.md) | Kod ko'proq o'qiladi, kamroq yoziladi; katta kod bazasiga kirish, navigatsiya, "qaysi ipni tortish", mental model qurish. |
| 04 | [Debugging: xatoni tizimli ovlash](./04-debugging-tizimli-ovlash.md) | Ilmiy debugging (takrorla→izolatsiya→tuzat), xato xabari va stack-trace o'qish, bisection, log, debugger, "ishlamayapti" ni aniqlashtirish. |

### II qism — Toza kod hunari

| # | Bob | Mavzu |
|---|---|---|
| 05 | [Nomlash — eng qiyin oson ish](./05-nomlash-sanati.md) | Yaxshi nom = yarim hujjat; o'zgaruvchi/funksiya/klass nomlash, niyatni ochish, qisqartma, izchillik, ✅/❌ misollar. |
| 06 | [Funksiyalar, modullik va kod tuzilishi](./06-funksiyalar-modullik.md) | Kichik funksiya, bitta mas'uliyat (kod darajasida), abstraksiya darajasi, yon ta'sir, fayl/modul tuzilishi. |
| 07 | [Izoh va o'z-o'zini hujjatlovchi kod](./07-izoh-ozini-hujjatlovchi-kod.md) | Qachon izoh kerak/keraksiz, "nega" vs "nima", eskirgan izoh xavfi, docstring/API izohi, kod o'zi gapirsin. |
| 08 | [Xatolarni boshqarish va mudofaaviy dasturlash](./08-xatolarni-boshqarish.md) | Xato vs istisno, "fail loud", chegaraviy holatlar, null/bo'sh, validatsiya, qayta urinish, xatoni yutib yubormaslik. |
| 09 | [Refactoring va kod hidlari](./09-refactoring-kod-hidlari.md) | Kod hidlari (code smells), xavfsiz qadamlar bilan refactoring, test bilan himoya, "boy skaut qoidasi", qachon to'xtash. |

### III qism — Sifat, test va xavfsizlik

| # | Bob | Mavzu |
|---|---|---|
| 10 | [Texnik qarz: tushunish va boshqarish](./10-texnik-qarz.md) | Texnik qarz nima, ataylab vs tasodifiy, foiz (interest), qachon "qarz olish" oqilona, jamoaga tushuntirish. |
| 11 | [Testlash madaniyati](./11-testlash-madaniyati.md) | Nega test, test piramidasi (unit/integ/e2e), TDD kirish, nimani test qilish, "ishonch" sifatida test, mind-set. |
| 12 | [Xavfsiz kod yozish asoslari](./12-xavfsiz-kod-asoslari.md) | Dasturchi uchun xavfsizlik ongi: kirishga ishonmaslik, injection, maxfiy ma'lumot (secrets), parol/hash, OWASP sezgisi. |

### IV qism — Jamoada ishlash

| # | Bob | Mavzu |
|---|---|---|
| 13 | [Code review — berish va olish](./13-code-review.md) | Sharhdan maqsad, qanday sharh yozish (mehribon + aniq), sharhni qabul qilish, pair programming, ego'siz muhandislik. |
| 14 | [Jamoaviy kod oqimi: commit, branch, PR madaniyati](./14-jamoaviy-kod-oqimi.md) | Atomik commit, yaxshi commit xabari, branch strategiyasi (trunk vs git-flow) jamoa qarori sifatida, PR odob-axloqi. |
| 15 | [Agile amalda: Scrum, Kanban va sprintlar](./15-agile-scrum-kanban.md) | Agile manifest, Scrum rollari/marosimlari, Kanban oqimi, standup/retro, jarayonning maqsadi, anti-patternlar. |
| 16 | [Baholash va rejalashtirish](./16-baholash-rejalashtirish.md) | Nega baholash qiyin, story point vs vaqt, noaniqlik konusi, buffer, kechikishni aytish, "tez/arzon/sifatli" uchburchagi. |
| 17 | [Texnik kommunikatsiya: yaxshi savol va yozma muloqot](./17-texnik-kommunikatsiya.md) | Yaxshi savol berish (XY muammosi), asinxron yozma muloqot, RFC/ADR, taqdimot, non-tech bilan gaplashish. |
| 18 | [Hujjatlash: README'dan runbook'gacha](./18-hujjatlash.md) | Nega hujjat, README anatomiyasi, onboarding, runbook, ADR, "hujjat ham kod", qachon yetarli. |
| 19 | [Fikr-mulohaza, mentorlik va mojaro](./19-fikr-mulohaza-mentorlik.md) | Feedback berish/olish, mentor va mentee bo'lish, kelishmovchilikni boshqarish, psixologik xavfsizlik, jamoa madaniyati. |

### V qism — Unumdorlik va o'sish

| # | Bob | Mavzu |
|---|---|---|
| 20 | [Ish muhiti va vositalar ustaligi](./20-ish-muhiti-vositalar.md) | IDE'ni qurol qilish, terminal/shell ustaligi, klaviatura, avtomatlashtirish, dotfiles, takrorlanuvchini yo'q qilish. |
| 21 | [Vaqt, diqqat va chuqur ish](./21-vaqt-diqqat-chuqur-ish.md) | Chuqur ish (deep work), kontekst almashinuvi narxi, yig'ilishlar, uzilishlar, fokus, ko'p ish bir vaqtda afsonasi. |
| 22 | [O'rganishni o'rganish va dolzarb qolish](./22-organishni-organish.md) | "Tutorial do'zaxi"dan chiqish, T-shaklli mutaxassis, fundamental vs trend, qanday samarali o'rganish, charchamasdan kuzatish. |

### VI qism — Karyera va kasb

| # | Bob | Mavzu |
|---|---|---|
| 23 | [Dasturchi karyera narvoni: junior'dan senior'gacha](./23-karyera-narvoni.md) | Junior/mid/senior/lead/staff nima anglatadi, darajalar orasidagi farq ko'lamda emas, "senior" = mas'uliyat va ta'sir. |
| 24 | [Ishni topish: rezyume, portfolio va tarmoq](./24-ish-topish-rezyume-portfolio.md) | Rezyume (CV) yozish, portfolio/GitHub, LinkedIn, tarmoq qurish, ariza strategiyasi, soxta talablar afsonasi. |
| 25 | [Texnik intervyuga tayyorgarlik](./25-texnik-intervyu.md) | Coding intervyu, tizim dizayni, behavioral (STAR), take-home, jonli kodlash, savol berish, ish haqi muzokarasi. |
| 26 | [Frilans va masofaviy ish](./26-frilans-masofaviy-ish.md) | Mijoz topish, narx belgilash, shartnoma/TZ, masofaviy disiplin, vaqt zonasi, O'zbekistondan global bozorga chiqish. |
| 27 | [Professional etika, mas'uliyat va huquq](./27-etika-masuliyat.md) | Kasbiy etika, litsenziya/IP, maxfiylik, "men yozgan kod zarar keltirsa", AI yordamida kod yozish etikasi, ochiq kod. |
| 28 | [Barqaror karyera: burnout, impostor va salomatlik](./28-barqaror-karyera-burnout.md) | Charchash (burnout) belgilari va oldini olish, impostor sindromi, ish-hayot muvozanati, jismoniy/ruhiy salomatlik. |

### Kapston

| # | Bob | Mavzu |
|---|---|---|
| 29 | [Kapston: birinchi 90 kun va shaxsiy o'sish rejasi](./29-kapston-90-kun-osish-rejasi.md) | Hammasini birlashtirish: yangi ishda birinchi 90 kun rejasi + shaxsiy o'sish yo'l xaritasi va keyingi qadamlar. |

---

## Bu kitob va boshqa kitoblar

Bu kitob **kasb** haqida; texnologiyani chuqur o'rganish uchun quyidagilarga o'ting:

- **Versiya nazorati mexanikasi:** [Git & GitHub](../git-github/README.md) — bu kitobda commit/PR *madaniyati* bor; u yerda to'liq mexanika.
- **Tizim darajasidagi dizayn:** [Dasturlash arxitekturasi](../arxitektura/README.md) — kod *ichidagi* emas, tizim *darajasidagi* qarorlar (SOLID, pattern, mikroservis).
- **Algoritmik fikrlash:** [Algoritmlar](../algoritmlar/README.md) + [1000 masala](../1000-masala/README.md) — intervyu va muammo yechish poydevori.
- **Deploy va operatsiya:** [DevOps & Deployment](../devops/README.md) — kodni serverga chiqarish, CI/CD, monitoring.
- **Til asoslari:** [Python](../python/README.md), [JavaScript](../js/README.md), [PHP](../php/README.md) — agar sintaksis hali yangi bo'lsa.
- **Qayerdan boshlash:** [Yo'l xaritasi](../roadmap.md) — qaysi kitobni qaysi tartibda.

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
