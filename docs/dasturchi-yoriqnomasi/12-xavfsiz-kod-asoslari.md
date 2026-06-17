# 12 — Xavfsiz kod yozish asoslari

[⬅️ Oldingi: 11 — Testlash madaniyati](./11-testlash-madaniyati.md) · [🏠 README](./README.md) · [Keyingi: 13 — Code review — berish va olish ➡️](./13-code-review.md)

---

> **Bu bobda:** xavfsizlik — alohida jamoaning ishi emas, **har bir dasturchining mas'uliyati**. Bu bob sizni pentester (pentest mutaxassis) qilmaydi; uning maqsadi — har kuni kod yozadigan dasturchida bo'lishi shart bo'lgan **xavfsizlik ongini** uyg'otish. Eng muhim qoidadan boshlaymiz ("kirishga hech qachon ishonma"), keyin eng ko'p uchraydigan xatolar oilasini — injection (SQL/komanda/XSS), maxfiy ma'lumotning oqishi, parolni noto'g'ri saqlash — ko'rib chiqamiz. Autentifikatsiya bilan avtorizatsiya farqi, bog'liqliklar xavfi, transport va xato xabarida ma'lumot oshkor qilmaslik ham bor. Hammasining ostida bitta tafakkur: **kim, nima, nega menga zarar yetkazishi mumkin**.
>
> **Halollik / Eslatma:** bu yerdagi narsalar *amaliy yo'l-yo'riq va sezgi*, to'liq xavfsizlik darsligi emas. Hech bir kod 100% xavfsiz emas — maqsad mukammallik emas, **hujum xarajatini oshirish va oson xatolarni yo'q qilish**. Xavfsizlik — bu *holat* emas, *jarayon*: bugun xavfsiz kod ertaga yangi zaiflik topilganda zaif bo'lishi mumkin. Misollar Python/JavaScript va psevdokodda; g'oyalar har qanday tilda bir xil. Qayerda fikr/tajriba borligini ochiq aytaman.

---

## Xavfsizlik — har dasturchining ishi ("shift left")

Ko'p yangi dasturchi xavfsizlikni shunday tasavvur qiladi: "men kodni yozaman, oxirida 'xavfsizlik jamoasi' tekshiradi". Bu eski va xavfli model. Real loyihalarda xavfsizlik **chapga suriladi** (shift left) — ya'ni jarayonning oxirida emas, **boshida, har bir dasturchining stoli ustida** boshlanadi. Sababi oddiy: xato qanchalik erta topilsa, tuzatish shuncha arzon — bu [11-bob](./11-testlash-madaniyati.md)dagi test piramidasi mantig'ining aynan o'zi.

Buning uchun rasmiy pentester bo'lish shart emas. Sizga kerak bo'lgan narsa — **tahdid modeli sezgisi**. Har bir funksiya yozayotganda uchta savolni o'zingizga bering:

- **Kim?** Bu kodga kim ta'sir qila oladi? Faqat ishonchli foydalanuvchimi, yoki internetdagi har qanday anonim odammi?
- **Nima?** U nimani qila oladi? Ma'lumot o'qish, o'zgartirish, o'chirish, boshqa foydalanuvchi nomidan ish qilish?
- **Nega?** Unga nima qiziq? Pul, shaxsiy ma'lumot, boshqalarning hisobi, shunchaki vayronagarchilik?

Bu uch savol — butun bobning yuragi. "Mening kichik loyihamga kim hujum qiladi?" degan o'y — eng keng tarqalgan xato. Internetdagi botlar inson emas: ular minglab saytlarni avtomatik ravishda, farqsiz skanerlaydi. Sizning "kichik" loyihangiz ham ro'yxatda.

> **Eslatma:** xavfsizlik mukammal qulf qurish haqida emas. Eshigingizga qulf qo'yganingizda maqsad — uni *buzib bo'lmaydigan* qilish emas (bunday qulf yo'q), balki o'g'rini qo'shni, qulfsiz uyga yo'naltirish: hujum xarajatini foydadan baland qilish. Kodda ham xuddi shunday.

---

## Eng muhim qoida: kirishga hech qachon ishonma

Agar bu bobdan faqat bitta narsani esda saqlasangiz, mana shu bo'lsin: **tashqaridan kelgan har qanday ma'lumot — dushman bo'lishi mumkin.** Foydalanuvchi formasi, tashqi API javobi, o'qiyotgan faylingiz, URL parametri, hatto sizning *o'z* bazangizdan kelgan ma'lumot ham (chunki uni kimdir buzgan bo'lishi mumkin) — hech biriga ko'r-ko'rona ishonmang.

![Ishonchsiz tashqi manbalar validatsiya darvozasidan o'tib ishonchli ichki zonaga kiradi](./rasmlar/dy12-kirishga-ishonma.svg)

Ishonchsizlik tashqi zona bilan ishonchli ichki zona o'rtasida **chegara** bor, va o'sha chegarada **validatsiya darvozasi** turadi. Bu yerda ikki ish bajariladi:

- **Validatsiya** — bu ma'lumot *yaroqlimi*? To'g'ri tip, format, oraliq, uzunlik? Yosh maydoni `-5` yoki `o'ttiz` emasligi; email haqiqatan email shaklida ekani. Yaroqsiz bo'lsa — **rad et**, "tuzatib qabul qil" emas.
- **Sanitizatsiya / kodlash** — ma'lumotni *qaerga ishlatilishiga* qarab xavfsiz ko'rinishga keltirish. Bu validatsiyadan farq qiladi: bir xil ma'lumot SQL'ga, HTML'ga va shell'ga turlicha tayyorlanadi.

> **Trade-off:** "allowlist" (faqat ruxsat berilganni qabul qil) deyarli har doim "blocklist" (faqat yomonni rad et)dan kuchli. Blocklist har doim to'liq emas — bir hujum usulini bloklayotganingizda hujumchi ikkinchisini topadi. Lekin allowlist qattiqroq va ba'zan haqiqiy foydalanuvchini ham rad etishi mumkin (mas. chinakam g'alati, lekin to'g'ri ism). Qoida: shubha bo'lsa — allowlist, lekin uni juda tor qilib qonuniy holatlarni bloklab qo'ymang.

Bu yerda bitta nozik nuqta bor: **mijoz (frontend) validatsiyasi xavfsizlik emas.** Brauzerdagi JavaScript tekshiruvi — bu foydalanuvchi qulayligi (darhol fikr-mulohaza). Lekin hujumchi brauzerni chetlab o'tib, to'g'ridan-to'g'ri serverga so'rov yuboradi. **Haqiqiy validatsiya har doim serverda** bo'lishi shart.

---

## Injection: ma'lumot va kod aralashuvi

Eng mashhur va eng halokatli zaiflik oilasi — **injection**. Uning ildizi bitta: **ma'lumotni kod sifatida talqin qilish.** Siz foydalanuvchi kiritmasini olib, uni satrga ulab, so'rov/komanda yasaysiz — va kiritmaning bir qismi *buyruqqa* aylanib ketadi.

Klassik misol — **SQL injection**:

```python
# ❌ XAVFLI: foydalanuvchi kiritmasi to'g'ridan-to'g'ri so'rovga ulanadi
ism = request.get("ism")          # foydalanuvchi: '  OR '1'='1
query = "SELECT * FROM users WHERE ism = '" + ism + "'"
db.execute(query)
# Natija: SELECT * FROM users WHERE ism = '' OR '1'='1'  -> butun jadval qaytadi
```

Bu yerda `' OR '1'='1` matn bo'lib qolmadi — u so'rovning **mantig'iga** aralashdi. Hujumchi `'; DROP TABLE users; --` yozsa, jadval o'chadi. Davo — ma'lumotni koddan **ajratish**: parametrlangan so'rov (prepared statement). Ma'lumot bazaga alohida kanal orqali, "qiymat" sifatida boradi va hech qachon kod sifatida talqin qilinmaydi.

```python
# ✅ XAVFSIZ: parametrlangan so'rov -- ma'lumot kod kanalidan ajratilgan
ism = request.get("ism")
db.execute("SELECT * FROM users WHERE ism = ?", [ism])
# ' OR '1'='1 endi shunchaki qidirilayotgan satr -- "bunday ismli odam yo'q"
```

![Ma'lumot va kod aralashuvi injection beradi, parametrlangan so'rov ularni ajratib xavfsiz qiladi](./rasmlar/dy12-injection.svg)

Xuddi shu g'oya bir nechta libosda keladi — diagrammada ko'rganingizdek, sabab ham, davo ham bir xil:

| Injection turi | Qaerda | Sabab | Davo |
|---|---|---|---|
| **SQL injection** | Ma'lumotlar bazasi so'rovi | Kiritma so'rovga ulanadi | Parametrlangan so'rov / ORM |
| **Command injection** | Shell / OS komandasi | Kiritma komanda satriga ulanadi | Argument massivi, shell'siz `exec` |
| **XSS** (cross-site scripting) | Brauzerdagi HTML/JS | Kiritma sahifaga xom chiqariladi | Kontekstga mos escaping / kodlash |
| **Path traversal** | Fayl tizimi | Kiritma fayl yo'liga ulanadi | Yo'lni normallashtir + allowlist |

`✅`/`❌` namuna — **command injection** uchun:

```python
# ❌ XAVFLI: foydalanuvchi nomi shell komandasiga ulanadi
fayl = request.get("fayl")        # foydalanuvchi: hisobot.pdf; rm -rf /
os.system("convert " + fayl + " out.png")   # ; rm -rf / ham bajariladi!

# ✅ XAVFSIZ: argumentlar massiv sifatida, shell yo'q -> aralashuv mumkin emas
subprocess.run(["convert", fayl, "out.png"], shell=False)
```

XSS uchun esa yodda tutilsin: HTML, atribut, URL va JavaScript konteksti — har biri **boshqacha** kodlashni talab qiladi. Shuning uchun "o'zim escaping qilaman" o'rniga deyarli har doim freymvork/shablon dvigatelining avtomatik kodlashiga (mas. React, Jinja2, Blade) tayanish to'g'ri.

> **Trade-off:** ba'zan ishlash tezligi yoki dinamik so'rov uchun "qo'lda satr yasash" vasvasasi paydo bo'ladi (mas. dinamik `ORDER BY` ustun nomi — uni parametr qilib bo'lmaydi). Bunday holatda yagona xavfsiz yo'l — **allowlist**: foydalanuvchi kiritgan ustun nomini ruxsat etilgan nomlar ro'yxati bilan solishtir, mos kelmasa rad et. Hech qachon foydalanuvchi matnini to'g'ridan-to'g'ri so'rov tuzilishiga qo'shmang.

---

## Maxfiy ma'lumot (secrets): parol, kalit, token

Ikkinchi eng keng tarqalgan xato — **maxfiy ma'lumotni kodga yoki git tarixiga joylash**. API kaliti, ma'lumotlar bazasi paroli, token, shifrlash kaliti — bularning hech biri **kodda yoki git repozitoriysida** bo'lmasligi kerak.

```python
# ❌ JIDDIY XATO: maxfiy ma'lumot kod ichida (va git tarixiga tushadi)
STRIPE_KEY = "sk_live_51H8xKf...real...key"
db = connect("postgres://admin:P@rol123@db.example.com/prod")
```

Nima uchun bu shunchalik xavfli? Chunki kod **ko'p joyga** ketadi: git tarixi (bir marta commit qilingan kalitni o'chirsangiz ham, tarixda qoladi), repozitoriy nusxalari, CI loglar, jamoa a'zolarining noutbuklari. Repozitoriy ochiq bo'lib qolsa yoki kimningdir noutbuki o'g'irlansa — kalitlaringiz ochiq.

To'g'ri yo'l — maxfiy ma'lumotni koddan **tashqarida** saqlash:

```python
# ✅ TO'G'RI: muhit o'zgaruvchisidan (env) yoki secret-manager'dan o'qish
import os
STRIPE_KEY = os.environ["STRIPE_KEY"]
db_url = os.environ["DATABASE_URL"]
```

| Yondashuv | Holati | Izoh |
|---|---|---|
| Kodda qattiq yozilgan | ❌ Hech qachon | Git tarixiga abadiy tushadi |
| `.env` fayl (git'da) | ❌ Xato | `.gitignore`siz commit'ga ketadi |
| `.env` fayl + `.gitignore` | ✅ Lokal/kichik | Fayl git'ga kirmaydi |
| Muhit o'zgaruvchisi (env) | ✅ Yaxshi | Server/CI darajasida beriladi |
| Secret-manager (Vault, AWS SM) | ✅ Eng yaxshi | Markazlashgan, rotatsiya, audit |

Amaliy minimal qadamlar har bir loyihada: (1) `.env` ni **`.gitignore`** ga qo'shing; (2) `.env.example` da faqat *kalit nomlarini* (qiymatsiz) saqlang; (3) agar maxfiy ma'lumot bir marta git'ga tushib ketsa — uni o'chirish yetarli emas, **darhol rotatsiya qiling** (kalitni bekor qilib, yangisini yarating). Tarixni tozalash uchun [Git & GitHub](../git-github/README.md) kitobidagi tarix qayta yozish (filter / BFG) usullariga qarang — lekin esda tuting: oqib ketgan kalitni *haqiqatan* xavfsiz qiladigan yagona narsa rotatsiya.

> **Trade-off:** kichik shaxsiy loyihada `.env` + `.gitignore` mutlaqo yetarli — Vault o'rnatib o'tirish ortiqcha murakkablik (over-engineering). Lekin jamoa o'sib, prod muhitlar ko'paygach, secret-manager'ning markazlashgan rotatsiyasi va auditi qimmatga arziydi. Kontekstga qarab tanlang.

---

## Parol va hash: parol shifrlanmaydi, hash qilinadi

Foydalanuvchi parollarini saqlash — yangi dasturchilar eng ko'p adashadigan joy. Eng katta tushunmovchilik: **parol shifrlanmaydi, u HASH qilinadi.** Farqi nimada?

- **Shifrlash** (encryption) — ikki tomonlama: kalit bilan shifrlangan narsani qaytarib ochish mumkin. Parol uchun bu yomon — agar siz parolni ochib olsangiz, demak baza buzilganda hujumchi ham ochadi.
- **Hash** — bir tomonlama: paroldan hash chiqaradi, lekin hashdan parolni qaytarib bo'lmaydi. Parolni hech qachon "ochish" kerak emas — faqat kelganini qayta hashlab, saqlangan hash bilan solishtirasiz.

![Parol salt bilan bir tomonlama hash qilib saqlanadi, tekshirishda qayta hashlash taqqoslanadi](./rasmlar/dy12-parol-hash.svg)

Diagrammadagi ikki bosqich muhim: **saqlashda** parol + tasodifiy **salt** bilan hashlanadi va faqat hash bazaga yoziladi (asl parol hech qaerda qolmaydi); **tekshirishda** kiritilgan parol o'sha salt bilan qayta hashlanadi va saqlangan hash bilan solishtiriladi.

```python
# ✅ TO'G'RI: bcrypt -- salt avtomatik, ataylab sekin
import bcrypt

# Ro'yxatdan o'tish (saqlash):
hash = bcrypt.hashpw(parol.encode(), bcrypt.gensalt())   # DB'ga shu hash yoziladi

# Kirish (tekshirish):
if bcrypt.checkpw(kiritilgan.encode(), hash):            # qayta-hash + taqqoslash
    kirishga_ruxsat()
```

Bu yerda ikkita nozik tushuncha bor. **Salt** — har bir parolga qo'shiladigan tasodifiy qiymat: u sababli ikki kishi bir xil parol qo'ysa ham, hashlari turlicha bo'ladi, va hujumchining oldindan tayyor "rainbow jadvallari" ishlamaydi. **Sekinlik** — bcrypt/argon2 *ataylab* sekin: bu odamga sezilmaydi (kirishda bir marta), lekin hujumchining sekundiga milliardlab parol sinash imkonini yo'q qiladi.

```python
# ❌ XATO: md5/sha256 parol uchun yetarli emas -- juda tez, saltsiz
hash = hashlib.md5(parol.encode()).hexdigest()   # brute-force soniyalar ichida
```

`md5`/`sha1`/`sha256` — umumiy maqsadli, tez xeshlar; aynan tezligi ularni parol uchun **yaroqsiz** qiladi. Parol uchun maxsus mo'ljallangan **bcrypt, argon2 yoki scrypt** ishlating.

> **Eslatma:** hashlarni taqqoslashda **teng-vaqt** (constant-time) taqqoslashdan foydalaning. Oddiy `==` ba'zan birinchi farqli baytdayoq to'xtaydi — bu mikro-vaqt farqi orqali ma'lumot sizdirishi mumkin (timing attack). bcrypt'ning `checkpw` kabi funksiyalari buni o'zi hal qiladi; token taqqoslashda esa `hmac.compare_digest` kabilarni ishlating. Bu ilg'or detal, lekin sezgi sifatida foydali.

---

## Autentifikatsiya, avtorizatsiya va eng kam imtiyoz

Ikki o'xshash so'z — tez-tez aralashtiriladi, lekin ular butunlay boshqa narsa:

- **Autentifikatsiya** (authentication, "authn") — **sen kimsan?** Parol, token, biometrika bilan kimligingni isbotlash.
- **Avtorizatsiya** (authorization, "authz") — **senga nima qilishga ruxsat bor?** Kim ekaning aniqlangach, qaysi amallarga huquqing borligi.

| | Autentifikatsiya | Avtorizatsiya |
|---|---|---|
| Savol | Sen kimsan? | Senga nimaga ruxsat bor? |
| Misol | Login + parol | "Bu hujjatni o'chira olasanmi?" |
| Qachon | Birinchi | Autentifikatsiyadan keyin |
| Tipik xato | Zaif parol siyosati | Boshqa foydalanuvchi ma'lumotiga kirish |

Eng ko'p uchraydigan avtorizatsiya xatosi — **kimligini tekshirib, huquqini tekshirmaslik**. Misol: foydalanuvchi tizimga kirgan (authn OK), lekin `/buyurtma/77` so'rovida 77-buyurtma *boshqa* odamniki ekani tekshirilmaydi — shunchaki `id`ni almashtirib begona ma'lumotni ko'radi. Buni **IDOR** (insecure direct object reference) deyishadi. Har bir resursga kirishda "*bu foydalanuvchi aynan shu resursga huquqlimi?*" deb so'rang.

Markaziy tamoyil — **eng kam imtiyoz** (least privilege): har bir foydalanuvchi, jarayon va xizmatga faqat **kerakli minimal** huquqni bering, ortiqchasini emas. Ma'lumotlar bazasiga ulanayotgan ilovaga `DROP TABLE` huquqi kerak emas. Buzilish yuz berganda zarar imtiyoz doirasi bilan cheklanadi.

> **Trade-off:** eng kam imtiyoz ba'zan noqulay — har yangi amal uchun yangi ruxsat sozlash kerak, "hammasiga ruxsat" tezroq tuyuladi. Lekin bu noqulaylik aynan himoya: keng ruxsat — keng hujum yuzasi. Junior bo'lganda "ishlatib ko'ray, keyin toraytaman" deb keng ruxsat berasiz va "keyin" hech qachon kelmaydi. Boshidan tor bering.

---

## Bog'liqliklar, transport va xato xabarlari

Uchta qisqaroq, lekin muhim mavzu — har biri kundalik ish ongida bo'lishi kerak.

**Bog'liqliklar (dependencies).** Zamonaviy loyiha o'nlab, ba'zan minglab tashqi paketga tayanadi. Sizning kodingiz mukammal bo'lsa ham, ulardagi **ma'lum zaiflik** sizniki bo'lib qoladi. Amaliy ong: paketlarni muntazam **yangilab turing**, `npm audit` / `pip-audit` kabi vositalarni CI'ga qo'ying, va **supply chain** xavfini his qiling — mashhur paketga o'xshatib qo'yilgan soxta nom (typosquatting) yoki buzib qo'yilgan paket sizning mashinangizda kod ishga tushiradi. CI'da xavfsizlik skanini avtomatlashtirish — bu [DevOps](../devops/README.md) kitobidagi pipeline madaniyatining bir qismi.

**Transport (HTTPS).** Ma'lumot tarmoq orqali yuborilganda **shifrlanmagan bo'lsa** — yo'ldagi har kim (ochiq Wi-Fi, oraliq server) uni o'qiy oladi. Qoida oddiy: **har doim HTTPS/TLS**, parol va token hech qachon ochiq HTTP orqali ketmasin. Bundan tashqari — **eng kam ma'lumot saqlash**: kerak bo'lmagan shaxsiy ma'lumotni yig'masangiz, oqib ketishi ham mumkin emas. Saqlamagan narsangiz o'g'irlanmaydi.

**Xato xabarlari — ma'lumot oshkor qilmang.** [08-bob](./08-xatolarni-boshqarish.md)da "fail loud" haqida gaplashdik — lekin "baland ovozda yiqilish" foydalanuvchiga emas, **logga** qaratilgan. Foydalanuvchi yuziga to'liq stack-trace, SQL so'rovi yoki fayl yo'lini chiqarish — hujumchiga tizim ichki tuzilishi haqida bepul xarita berish demak.

```text
❌ Foydalanuvchiga:  "SQLException: column 'parol_hash' ... at UserRepo.java:88
                      postgres://admin@10.0.0.5/prod"
✅ Foydalanuvchiga:  "Kutilmagan xatolik yuz berdi. (kod: REQ-4F2A)"
✅ Logga (ichki):    to'liq stack-trace + so'rov konteksti + REQ-4F2A
```

Foydalanuvchi tinch, umumiy xabar va kuzatuv kodi (REQ-4F2A) oladi; dasturchi esa o'sha kod bo'yicha logdan to'liq diagnostikani topadi. Bu — [08-bob](./08-xatolarni-boshqarish.md)dagi "xato xabari ikki auditoriyaga" qoidasining xavfsizlik tarafi.

---

## OWASP sezgisi va halol yakun

Xavfsizlik bo'yicha eng mashhur ma'lumotnoma — **OWASP Top 10**: veb-ilovalardagi eng keng tarqalgan zaifliklar ro'yxati. Buni yoddan bilish shart emas; muhimi — **uning ongi bilan yashash**. Bu bobda ko'rganlaringiz — injection, buzuq avtorizatsiya, maxfiy ma'lumot oqishi, eskirgan bog'liqlik — aynan o'sha ro'yxatning yuqori qatorlari. Vaqti-vaqti bilan OWASP Top 10 ga qarab chiqish — o'z kodingizga "hujumchi ko'zi" bilan boqishning yaxshi odati.

Va eng halol haqiqat: **hech bir kod 100% xavfsiz emas.** Mukammal qulf yo'q. Maqsad — hujumni *imkonsiz* qilish emas (bunga erishib bo'lmaydi), balki uni **qimmat** qilish: oson, avtomatik hujumlarni to'sib, hujumchini foyda-xarajat hisobiga majburlash. Aksariyat buzilishlar nozik kriptografik kamchiliklardan emas, **oddiy, oldini olsa bo'ladigan** xatolardan boshlanadi — kodga tashlangan parol, parametrlanmagan so'rov, tekshirilmagan huquq. Aynan shularni yo'q qilsangiz — siz mavjud kodlarning ko'pchiligidan xavfsizroq bo'lasiz.

Xavfsizlik — bu **jarayon, holat emas**: yangi zaifliklar topiladi, bog'liqliklar eskiradi, tahdidlar o'zgaradi. "Biz xavfsizmiz" degan yakuniy nuqta yo'q; bor narsa — har commit, har review, har deployda davom etadigan ongli e'tibor.

---

## Asosiy g'oyalar (bobni qisqacha)

- **Xavfsizlik har dasturchining ishi:** "shift left" — jarayon oxirida emas, boshida. Har funksiyada **kim/nima/nega** zarar yetkazishi mumkinligini so'rang (tahdid modeli sezgisi).
- **Kirishga hech qachon ishonma:** foydalanuvchi, API, fayl, URL — hammasi dushman bo'lishi mumkin. Chegarada **validatsiya + sanitizatsiya**; haqiqiy tekshiruv har doim **serverda**, mijozda emas.
- **Injection = ma'lumot va kod aralashuvi:** SQL/komanda/XSS — bitta ildiz. Davo — ajratish: **parametrlangan so'rov**, argument massivi, kontekstga mos **escaping**. Dinamik tuzilish kerak bo'lsa — **allowlist**.
- **Maxfiy ma'lumot koddan tashqarida:** parol/kalit/token kodda yoki git'da **bo'lmasin** — env yoki secret-manager, `.gitignore`. Oqib ketsa o'chirish yetarli emas — **rotatsiya**.
- **Parol hash qilinadi, shifrlanmaydi:** bir tomonlama **bcrypt/argon2** + salt; md5/sha tez bo'lgani uchun **yaroqsiz**; taqqoslash teng-vaqtli bo'lsin.
- **Authn ≠ authz va eng kam imtiyoz:** kimligini tekshirish (authn) huquqini tekshirish (authz)ni almashtirmaydi (IDOR xavfi). Har resursga **minimal kerakli** huquq bering.
- **Atrofga e'tibor:** bog'liqliklarni yangilab tur (supply chain), har doim **HTTPS**, eng kam ma'lumot saqla, xato xabarida ichki tuzilishni **oshkor qilma**. Maqsad — hujum xarajatini oshirish; xavfsizlik — **jarayon, holat emas**.

---

## Mashqlar

> Eslatma: bu mashqlarning ko'pi amaliy/refleksiv. "Yagona to'g'ri javob" har doim ham yo'q — yechimlar namuna va mezon sifatida berilgan. Bir nechta mashqda savol: "bu kodda qaysi zaiflik bor?"

### Oson

**1-mashq.** Quyidagi kodda **qaysi zaiflik bor**? Nomini ayting va bir qatorda davosini yozing.
```python
ism = request.get("ism")
db.execute("SELECT * FROM users WHERE ism = '" + ism + "'")
```

**2-mashq.** Quyidagi ikki saqlash usulidan qaysi biri xavfli va nega? Tuzating.
```python
API_KEY = "sk_live_9aF...real..."          # (a)
API_KEY = os.environ["API_KEY"]            # (b)
```

**3-mashq.** "Autentifikatsiya" va "avtorizatsiya" — har birini bitta jumlada o'z so'zingiz bilan ta'riflang va har biriga bittadan kundalik misol keltiring.

### O'rta

**4-mashq.** Quyidagi parol saqlash kodida **kamida ikkita** xavfsizlik xatosi bor. Toping va to'g'ri versiyasini yozing.
```python
import hashlib
def saqla(parol):
    h = hashlib.md5(parol.encode()).hexdigest()
    db.save(h)
```

**5-mashq.** Quyidagi kodda **qaysi zaiflik bor** (foydalanuvchi `fayl` maydoniga `hisobot.pdf; rm -rf /` yozsa nima bo'ladi)? Davosini yozing.
```python
fayl = request.get("fayl")
os.system("convert " + fayl + " natija.png")
```

**6-mashq.** Quyidagi xato xabari prod'da foydalanuvchiga ko'rsatiladi. Unda nima muammo bor (xavfsizlik nuqtai nazaridan) va uni qanday qayta yozasiz (foydalanuvchiga + logga ikki versiya)?
```text
Error: SQLException at OrderRepo.java:142
db=postgres://admin:Pr0d@10.0.2.5/orders, query=SELECT * FROM orders WHERE id=88
```

### Qiyin

**7-mashq.** Quyidagi endpoint'da **avtorizatsiya zaifligi** bor (foydalanuvchi autentifikatsiyadan o'tgan, lekin...). Zaiflik nomini ayting, hujum stsenariysini bir jumlada tasvirlang va kodni tuzating.
```python
@app.get("/buyurtma/<id>")
def buyurtma(id):
    foydalanuvchi = joriy_foydalanuvchi()   # kim ekani aniq (authn OK)
    return db.get_buyurtma(id)              # id bo'yicha qaytaradi
```

**8-mashq.** Sizga "kichik shaxsiy loyiha" deb topshiriq berildi: foydalanuvchilar ro'yxatdan o'tadigan, parol bilan kiradigan, profilini tahrirlaydigan veb-ilova. **Tahdid modeli sezgisi** bilan, bu loyihada e'tibor berishingiz kerak bo'lgan **kamida 5 ta** xavfsizlik nuqtasini sanang (har biriga "kim/nima/nega" yoki davosini qisqacha qo'shing). "Kichik loyihaga kim hujum qiladi" deb o'ylash nega xato ekanini ham ayting.

<details markdown="1">
<summary>Yechimlar</summary>

### 1-mashq yechimi
Zaiflik — **SQL injection**: `ism` to'g'ridan-to'g'ri so'rovga ulangan, foydalanuvchi `' OR '1'='1` yoki `'; DROP TABLE users; --` yozib so'rov mantig'iga aralasha oladi. Davo — **parametrlangan so'rov**:
```python
db.execute("SELECT * FROM users WHERE ism = ?", [ism])
```

### 2-mashq yechimi
**(a) xavfli** — API kaliti kodga qattiq yozilgan, demak git tarixiga tushadi, repozitoriy/CI loglar orqali oqib ketishi mumkin. **(b) to'g'ri** — kalit muhit o'zgaruvchisidan o'qiladi, koddan tashqarida. Tuzatish: `(a)`ni o'chirib, `(b)`ni qoldiring, `.env` ni `.gitignore`ga qo'shing. Agar `(a)` allaqachon commit qilingan bo'lsa — kalitni **rotatsiya qiling** (eskisini bekor qiling), shunchaki o'chirish yetarli emas.

### 3-mashq yechimi
- **Autentifikatsiya (authn):** "sen kimsan?" — kimligingni isbotlash. Misol: login + parol kiritib tizimga kirish.
- **Avtorizatsiya (authz):** "senga nimaga ruxsat bor?" — kimliging aniqlangach, qaysi amalga huquqing borligi. Misol: oddiy foydalanuvchi boshqa odamning hisobini **o'chira olmaydi**, admin esa o'chira oladi.
Asosiy nuqta: authn o'tgani authz'ni anglatmaydi — kirgan foydalanuvchi ham har amalga huquqli emas.

### 4-mashq yechimi
Xatolar: (1) **md5** parol uchun yaroqsiz — juda tez, brute-force oson; (2) **salt yo'q** — bir xil parollar bir xil hash beradi, rainbow jadvallar ishlaydi; (qo'shimcha) bcrypt'da salt avtomatik. To'g'ri versiya:
```python
import bcrypt
def saqla(parol):
    h = bcrypt.hashpw(parol.encode(), bcrypt.gensalt())   # salt avtomatik, ataylab sekin
    db.save(h)
# Tekshirish: bcrypt.checkpw(kiritilgan.encode(), saqlangan_hash)
```

### 5-mashq yechimi
Zaiflik — **command injection**: `os.system` satrni shell orqali bajaradi, `;` keyingi komandani ishga tushiradi. `hisobot.pdf; rm -rf /` butun diskni o'chirishga urinadi. Davo — shell'siz, argumentlar massivi bilan:
```python
import subprocess
subprocess.run(["convert", fayl, "natija.png"], shell=False)
# `fayl` endi alohida argument -- ; va boshqa shell belgilari kuch ishlatmaydi
```
(Qo'shimcha: `fayl`ni allowlist/normallashtirish bilan ham tekshirish kerak — path traversal uchun.)

### 6-mashq yechimi
Muammo: xato xabari **ichki tuzilishni oshkor qiladi** — baza turi, host IP, foydalanuvchi nomi, parol, jadval va so'rov tuzilishi. Bu hujumchiga bepul xarita. Foydalanuvchiga umumiy xabar, batafsil ma'lumot faqat logga:
- **Foydalanuvchiga:** `"Kutilmagan xatolik yuz berdi. Iltimos keyinroq urinib ko'ring. (kod: ERR-7B31)"`
- **Logga (ichki):** to'liq stack-trace + so'rov konteksti + `ERR-7B31` (lekin **parol logga ham yozilmasin** — ulanish satrini maskalang).

E'tibor bering: ulanish parolini *logga ham* xom yozish xato — sirlar logda qolmasin.

### 7-mashq yechimi
Zaiflik — **IDOR** (insecure direct object reference) / buzuq avtorizatsiya. **Hujum:** kirgan foydalanuvchi URL'dagi `id`ni almashtirib (`/buyurtma/77` → `/buyurtma/78`) **begona** buyurtmani ko'radi — kod faqat "kim ekani"ni tekshirib, "shu resursga huquqi bormi"ni tekshirmaydi. Tuzatish — egalikni tekshir:
```python
@app.get("/buyurtma/<id>")
def buyurtma(id):
    foydalanuvchi = joriy_foydalanuvchi()
    b = db.get_buyurtma(id)
    if b is None or b.egasi_id != foydalanuvchi.id:
        abort(404)            # 403 emas, 404 -- mavjudligini ham oshkor qilma
    return b
```
(Trade-off: 403 "ruxsat yo'q" o'rniga 404 qaytarish resurs *mavjudligini* ham yashiradi — ko'pincha afzal.)

### 8-mashq yechimi
Namuna ro'yxat (kamida 5 ta — sizniki boshqacha bo'lishi mumkin):
1. **Parol saqlash** — bcrypt/argon2 + salt; md5/ochiq matn emas. (*kim:* baza buzilsa hujumchi; *nega:* parollarni o'g'irlash.)
2. **Injection** — barcha so'rovlar parametrlangan; profil maydonlari xom HTML chiqarilmaydi (XSS). (*kim:* har anonim so'rov yuboruvchi.)
3. **Avtorizatsiya** — foydalanuvchi faqat *o'z* profilini tahrirlay olsin (IDOR'dan saqlanish).
4. **Maxfiy ma'lumot** — DB paroli, sessiya kaliti env'da, kodda emas; `.gitignore`.
5. **Transport** — HTTPS majburiy; parol/sessiya ochiq HTTP'da ketmasin.
6. (qo'shimcha) **Sessiya/token** — xavfsiz cookie, chiqishda bekor qilish; **bog'liqliklar** yangilanib tursin.

"Kichik loyihaga kim hujum qiladi" xato, chunki hujumlarning aksariyati **maqsadli emas** — botlar internetni farqsiz, avtomatik skanerlaydi va har qanday zaif saytni topadi. Loyiha "kichik" bo'lishi uni ko'rinmas qilmaydi.

</details>

---

[⬅️ Oldingi: 11 — Testlash madaniyati](./11-testlash-madaniyati.md) · [🏠 README](./README.md) · [Keyingi: 13 — Code review — berish va olish ➡️](./13-code-review.md)
