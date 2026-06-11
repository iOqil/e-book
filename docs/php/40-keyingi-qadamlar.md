# 6-QISM — Keyingi qadamlar

[⬅️ Oldingi: 5.4 Composer — tashqi kutubxonalar](./39-composer-tashqi-kutubxonalar.md) · [🏠 README](./README.md)

---

Tabriklaymiz — siz katta yo'lni bosib o'tdingiz! Noldan boshlab, endi haqiqiy, xavfsiz, professional tashkil etilgan veb-dasturlar yoza olasiz. Bu — jiddiy yutuq. Endi qayerga borish kerakligini ko'rsatamiz.

### Avvalo: mustahkamlang

Yangi mavzularga shoshilmang. Eng muhimi — **o'rganganlaringizni amalda mustahkamlash.** Buning eng yaxshi yo'li — **o'z loyihangizni qurish.** Masalan:
- Shaxsiy "vazifalar ro'yxati" (to-do) dasturi.
- Oddiy blog (maqola qo'shish, ko'rish, izoh qoldirish).
- Mini onlayn do'kon (mahsulotlar, savat).
- Kontaktlar yoki xarajatlar daftari.

Loyiha qurganda muqarrar muammolarga duch kelasiz — ularni yechish jarayonida haqiqiy o'rganish sodir bo'ladi. Kitob o'qish — bilim; loyiha qurish — mahorat.

### Keyingi texnik mavzular

Tayyor bo'lganingizda, quyidagilarni o'rganing (taxminan shu tartibda):

**1) Git va GitHub** — kodingiz tarixini saqlash va boshqarish vositasi. Har bir dasturchi buni biladi. "O'zgarishlarni saqlash, eski holatga qaytish, boshqalar bilan birga ishlash" — Git shuni qiladi. Bu — keyingi eng muhim ko'nikma.

**2) Framework (eng katta keyingi qadam)** — siz 5-QISMda MVC'ni "qo'lda" yozdingiz. Haqiqiy loyihalarda esa **framework** ("ish qurilmasi") ishlatiladi — bu tayyor, kuchli tuzilma bo'lib, MVC, xavfsizlik, baza bilan ishlash va boshqa ko'p narsalarni avtomatik beradi. PHP'da eng mashhurlari: **Laravel** va **Symfony**. Framework o'rganish — siz uchun katta tezlanish bo'ladi, lekin **faqat asoslarni (bu qo'llanmadagini) yaxshi tushungandan keyin.** Asossiz frameworkga o'tish — "sehr"ni ko'r-ko'rona ishlatishga olib keladi.

**3) Yanada chuqur SQL va ma'lumotlar bazasi** — murakkabroq so'rovlar, indekslar (bazani tezlashtirish), ma'lumotlar bazasini to'g'ri loyihalash.

**4) API va frontend bilan ishlash** — zamonaviy saytlarda backend (PHP) ma'lumotni "API" orqali beradi, frontend (JavaScript) uni ko'rsatadi. JSON formati, REST API tushunchalari.

**5) Deploy (saytni internetga chiqarish)** — loyihangizni o'z kompyuteringizdan haqiqiy serverga (internetga) joylash. Hosting, domen, server sozlamalari.

### Awareness uchun: kattaroq loyihalar mavzulari

Bular hozir shart emas, lekin borligini bilib qo'ying — kattaroq, yuklamasi yuqori loyihalarda kerak bo'ladi:
- **Kesh (caching)** — tez-tez kerak bo'ladigan ma'lumotni "tezkor xotirada" saqlab, bazaga har safar murojaat qilmaslik (saytni tezlashtiradi). Buning uchun **Redis** kabi vositalar ishlatiladi.
- **Navbat (queue)** — sekin ishlarni (masalan, minglab email yuborish) "fonda", foydalanuvchini kuttirmasdan bajarish.
- **Testlar** — kodingiz to'g'ri ishlashini avtomatik tekshiradigan kod (katta loyihalarda muhim).

Bularning hammasi — siz bugun qo'ygan poydevor ustiga quriladi. Ularni o'z vaqtida, kerak bo'lganda o'rganasiz.

### Yaxshi dasturchi bo'lish sirlari

1. **Har kuni oz bo'lsa ham kod yozing.** Muntazamlik — iqtidordan muhimroq.
2. **Xatolardan qo'rqmang.** Har bir xato — o'rganish imkoni. Xato xabarini diqqat bilan o'qing — u ko'pincha muammoni aniq aytadi.
3. **Hujjat (documentation) o'qishni o'rganing.** PHP'ning rasmiy hujjati (`php.net`) — eng ishonchli manba.
4. **Boshqalarning kodini o'qing.** GitHub'da ochiq loyihalarni ko'ring — qanday yozilganini o'rganing.
5. **Sabrli bo'ling.** Dasturlash — bir kunda emas, oylar va yillar davomida o'rganiladigan mahorat. Hamma boshlovchi bo'lgan.
6. **Savol berishdan uyalmang.** Hamjamiyatlar (forumlar, Telegram guruhlari) — yordam manbai.

### Yakuniy so'z

Bu qo'llanma sizga PHP'ning poydevorini berdi: o'zgaruvchilardan to to'liq, xavfsiz veb-dasturlargacha. Lekin dasturlashda o'rganish hech qachon to'xtamaydi — eng tajribali dasturchilar ham har kuni yangi narsa o'rganadi. Bu — chiroyli tomoni.

Eng muhimi: **qurishda davom eting.** Har bir yozgan dasturingiz sizni kuchliroq qiladi. Bugun "Salom, dunyo!" yozgan bo'lsangiz, ertaga butun bir tizim quryapsiz. Yo'lda omad!

---

*Qo'llanma tugadi. Har bir mavzuni amalda — kod yozib — mustahkamlang. Tushunmagan joy bo'lsa, o'sha bo'limga qaytib, misolni qayta yozib ko'ring. Dasturlash — mashq bilan o'rganiladi.*
