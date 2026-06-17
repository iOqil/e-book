# 05 — REST tamoyillari va Richardson Maturity Model

[⬅️ Oldingi: 04 — API uslublari: REST, RPC, GraphQL, gRPC](./04-api-uslublari.md) · [🏠 README](./README.md) · [Keyingi: 06 — Resurs modellashtirish va URI dizayni ➡️](./06-resurs-uri-dizayni.md)

---

> **Bu bobda:** REST aslida nima ekanini — protokol emas, arxitektura uslubi ekanini — manbasidan, ya'ni Roy Fielding dissertatsiyasidan boshlab tushuntiramiz. Oltita arxitektura cheklovini (constraints) ko'rib chiqib, ulardan ikkitasini — `stateless` va `uniform interface` ni — chuqur ochamiz. So'ng amaliyotda eng foydali asbob bo'lgan Richardson Maturity Model (RMM) ning to'rt darajasini misollar bilan o'rganamiz va "RESTful" degan da'voga halol qaraymiz.
>
> **Halollik / Eslatma:** HTTP metodlari, status kodlari va `stateless` ta'rifi RFC 9110 (2022) ga, keshlash xossalari RFC 9111 ga asoslangan. RMM — bu Leonard Richardson kiritib, Martin Fowler ommalashtirgan tahlil asbobi, RFC emas. HATEOAS nazariy jihatdan REST ning to'liq shakli, ammo amalda kam qo'llaniladi — buni biz ochiq aytamiz. Barcha JSON namunalari valid.

---

## REST qayerdan keladi: Fielding dissertatsiyasi

Tasavvur qiling, kimdir sizdan "uy qurish uslubi" ni so'raydi. Siz unga g'isht yoki beton (ya'ni material) haqida emas, balki **tamoyillar** haqida gapirasiz: qanday qilib derazalar yorug'lik beradi, qanday qilib xonalar bir-biriga ulanadi, devorlar yukni qanday taqsimlaydi. Material — bu vosita; uslub — bu g'oyalar to'plami. REST ham aynan shunday: u protokol emas, **arxitektura uslubi** (architectural style).

REST 2000-yilda Roy Fieldingning doktorlik dissertatsiyasida tavsiflangan. Fielding — HTTP/1.1 va URI standartlarining mualliflaridan biri. U Web nega shunchalik muvaffaqiyatli, masshtablanuvchan va chidamli ekanini tushuntirishga harakat qildi va Web ortidagi arxitektura tamoyillarini umumlashtirdi. Natija — **REST** (REpresentational State Transfer).

Nomning o'zi g'oyani yashiradi:

- **Resource (resurs):** server boshqaradigan har qanday "narsa" — buyurtma, foydalanuvchi, hisob-kitob. Resurs — bu abstrakt tushuncha (masalan "42-buyurtma").
- **Representation (tasvir):** resursning ma'lum bir formatdagi nusxasi. Server sizga 42-buyurtmaning o'zini emas, balki uning **tasvirini** — masalan JSON hujjat sifatida — yuboradi. Bir xil resursning bir nechta tasviri bo'lishi mumkin (JSON, XML, HTML).
- **State Transfer (holatni uzatish):** mijoz va server o'rtasida ana shu tasvirlar uzatiladi. Mijoz tasvirni oladi, o'zgartiradi va serverga qaytaradi — shu tariqa ilova holati ko'chadi.

> **Eslatma:** Resurs bilan uning tasvirini ajratish muhim. `/orders/42` — resurs identifikatori. Server JSON yuborsa, bu uning bitta tasviri. Ertaga server XML tasviri qo'shsa ham, resurs o'zi o'zgarmaydi.

Demak REST "JSON qaytaradigan HTTP API" degani emas. REST — bu Web ishlash usulini umumlashtiradigan cheklovlar to'plami. Endi shu cheklovlarni ko'ramiz.

## Oltita cheklov (constraints)

Fielding REST ni oltita cheklov orqali ta'rifladi. "Cheklov" so'zi salbiy eshitiladi, lekin bu yerda u **ataylab qabul qilingan qoida** degani — har bir qoida nimanidir cheklab, evaziga muhim foyda beradi (masshtablanuvchanlik, soddalik, mustaqil rivojlanish). Agar tizim shu oltitasiga (oxirgisi ixtiyoriy) amal qilsa, u RESTful hisoblanadi.

| # | Cheklov | Bir jumlada | API uchun ma'nosi |
|---|---------|-------------|-------------------|
| 1 | **Client-Server** | Mijoz (UI) va server (ma'lumot/mantiq) ajratilgan | Ikki tomon mustaqil rivojlanadi; bitta API ni veb, mobil, IoT ishlatadi |
| 2 | **Stateless** | Server mijoz sessiyasini saqlamaydi | Har so'rov o'zini-o'zi yetarli; oson masshtablash |
| 3 | **Cacheable** | Javoblar keshlanadigan/keshlanmaydigan deb belgilanadi | Takroriy so'rovlarni kesh qaytaradi; tezlik va yuk kamayishi |
| 4 | **Uniform Interface** | Barcha resurslar bir xil, standart interfeys orqali | Bashorat qilinadigan API; mijoz bir marta o'rganadi |
| 5 | **Layered System** | Mijoz to'g'ridan-to'g'ri serverga yoki oraliq qatlamga ulanganini bilmaydi | Gateway, kesh, balanslagich qo'shish mumkin |
| 6 | **Code-on-Demand** *(ixtiyoriy)* | Server mijozga kod (masalan JS) yubora oladi | Kamdan-kam; brauzer JS bunga misol |

Qisqacha har biri:

1. **Client-Server.** Mas'uliyatlarni ajratish. Mijoz foydalanuvchi interfeysi va tajriba bilan shug'ullanadi; server ma'lumotni saqlash va biznes-mantiq bilan. Ikkisi shartnoma (API kontrakti) orqali kelishadi, qolgani mustaqil. Bu — eng asosiy ajratish.
2. **Stateless.** Server hech qanday mijoz sessiyasini eslamaydi. Pastda chuqur ko'ramiz.
3. **Cacheable.** Har javob o'zini "keshlasa bo'ladimi yoki yo'qmi" deb belgilashi kerak. Bu Web tezligining poydevori — bu mavzu [keshlash bobida](./16-keshlash.md) batafsil.
4. **Uniform Interface.** REST ni boshqa uslublardan ajratib turadigan markaziy cheklov. Pastda chuqur ko'ramiz.
5. **Layered System.** Mijoz faqat eng yaqin qatlam bilan gaplashadi va u ortida nima borligini (haqiqiy server, kesh, gateway) bilmaydi. Bu oraliq qatlamlar — kesh, xavfsizlik filtrlari, yuk balanslagichlar — qo'shishni osonlashtiradi. [API gateway/BFF bobi](./23-api-gateway-bff.md) shu cheklovning amaliy mevasi.
6. **Code-on-Demand (ixtiyoriy).** Server mijozga bajariladigan kod yuborib, uning imkoniyatlarini vaqtincha kengaytirishi mumkin. Bu yagona ixtiyoriy cheklov; ko'p API unsiz ham RESTful bo'la oladi.

> **Trade-off:** Har bir cheklov nimanidir qurbon qiladi. `Stateless` har so'rovda ko'proq ma'lumot yuborishni talab qiladi. `Uniform interface` esa "har holat uchun maxsus, optimal interfeys" ni cheklaydi. Foyda — masshtab va soddalik — odatda bu narxdan ustun keladi, lekin bu kontekstga bog'liq.

Endi ikkita eng muhim cheklovni chuqurroq ochamiz.

## Stateless — chuqur

![Stateless va stateful: holat qayerda saqlanishini taqqoslash](rasmlar/api05-stateless.svg)

**Intuitsiya.** Tasavvur qiling, kassirga borasiz. **Stateful** kassir sizni eslaydi: "Ha, siz oldin ikkita non olgansiz, savatingiz menda". Agar siz boshqa kassaga o'tsangiz, yangi kassir hech narsa bilmaydi. **Stateless** kassir esa hech kimni eslamaydi — siz har safar to'liq aytasiz: "Men Aliman, kartam shu, ikki non olmoqchiman". Sekinroq tuyuladi, lekin har qanday kassa sizga xizmat qila oladi — navbat tez tarqaydi.

**Aniq ta'rif.** REST da server mijozning **sessiya holatini** (session state) saqlamasligi kerak. Har bir so'rov uni qayta ishlash uchun zarur bo'lgan **barcha** ma'lumotni o'zida olib kelishi shart — kim so'rayapti (autentifikatsiya), nima kerak (parametrlar), qanday kontekstda. Server ikki so'rov o'rtasida hech narsani "eslab qolmaydi".

Quyidagi ikki so'rovni solishtiring. **Stateful** yondashuv (REST emas):

```http
POST /login HTTP/1.1
Host: api.example.com
Content-Type: application/json

{"username": "ali", "password": "..."}

HTTP/1.1 200 OK
Set-Cookie: SESSIONID=abc123; HttpOnly

```

So'ng keyingi so'rov serverning xotirasidagi `SESSIONID=abc123` yozuviga tayanadi — kim ekaningiz server xotirasida saqlangan.

**Stateless** yondashuv (REST): har so'rov o'zini-o'zi tasdiqlaydi va tegishli kontekstni olib keladi:

```http
GET /orders?status=pending HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{"items": [{"id": 42, "status": "pending"}], "total": 1}
```

Bu yerda `Authorization` sarlavhasi har so'rovda kim ekaningizni isbotlaydi — server uni alohida eslab turmaydi. Token o'zida kerakli identifikatsiyani olib yuradi (yoki serverda tez tekshiriladi). Autentifikatsiya tokenlari bilan bog'liqlik [autentifikatsiya bobida](./11-autentifikatsiya.md) batafsil.

> **Eslatma:** "Stateless" — bu server umuman holat saqlamaydi degani emas. Buyurtmalar, foydalanuvchilar bazada (ma'lumot holati / resource state) saqlanadi va saqlanishi shart. Cheklanadigan narsa — **mijoz sessiyasi holati**: "bu ulanish hozir login qilgan, savatida shu narsalar bor" kabi vaqtinchalik, so'rovlararo eslab qolinadigan kontekst.

**Stateless nima beradi?**

- **Masshtablash (eng katta foyda).** Server xotirasida sessiya bo'lmagani uchun, **istalgan** server **istalgan** so'rovni qayta ishlay oladi. Yuk balanslagich so'rovni xohlagan instansiyaga yo'naltira oladi. Yangi server qo'shish — shunchaki pulga ulab qo'yish. Bu — gorizontal masshtablashning poydevori.
- **Ishonchlilik (resilience).** Bitta server qulasa, uning so'rovlari boshqasiga o'tadi va mijoz hech narsa yo'qotmaydi — chunki yo'qotadigan sessiya yo'q.
- **Soddalik.** Server "kim qayerda turibdi" ni boshqarishi shart emas; har so'rov mustaqil tushuniladi, bu nosozlikni tuzatishni ham osonlashtiradi.

**Narxi (trade-off):**

- Har so'rov ko'proq ma'lumot olib yuradi (token, kontekst), ya'ni biroz ko'proq trafik va qayta-tekshirish.
- Ba'zi holatlarda (masalan ko'p qadamli jarayon) holatni qayerda saqlash kerakligi savol bo'ladi — javob: yo mijozda, yo umumiy ombor (Redis/DB) da, lekin alohida ilova serverining lokal xotirasida emas.

> **Trade-off:** Agar haqiqatan sessiya kerak bo'lsa (masalan ko'p qadamli buyurtma jarayoni), uni **tashqi umumiy ombor** (Redis, DB) ga qo'ying, alohida server xotirasiga emas. Shunda serverlar baribir o'zaro almashtiriladigan (stateless) bo'lib qoladi, faqat holat markazlashtirilgan. Bu — REST ruhini buzmaydigan amaliy yechim.

## Uniform Interface — chuqur

![Uniform interface: bir resurs ustida turli metodlar bir xil ma'noda](rasmlar/api05-uniform-interface.svg)

Bu — REST ni boshqa har qanday uslubdan ajratib turadigan markaziy cheklov. **Intuitsiya:** dunyodagi har bir eshik dastagi bir xil ishlaydi — bossang ochiladi, tortsang yopiladi. Yangi binoga kirganingizda eshikni qanday ochishni qayta o'rganmaysiz. Uniform interface ham xuddi shu: barcha resurslar **bir xil, standart, bashorat qilinadigan** tarzda ishlatiladi, shuning uchun bitta resursni ishlatishni o'rgansangiz, hammasini bilasiz.

Uniform interface to'rtta ichki tamoyildan iborat:

**(a) Resurslarni identifikatsiyalash (identification of resources).** Har bir resurs barqaror identifikator — URI orqali nomlanadi. `/orders/42` har doim aynan o'sha buyurtmani bildiradi. URI resursni ko'rsatadi, uning tasvirini emas.

**(b) Tasvir orqali manipulyatsiya (manipulation through representations).** Mijoz resursni to'g'ridan-to'g'ri o'zgartira olmaydi; u resursning **tasvirini** (masalan JSON hujjat) oladi, o'zgartiradi va serverga qaytaradi. Server tasvirni qabul qilib, haqiqiy holatni yangilaydi.

```http
PUT /orders/42 HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{"id": 42, "status": "shipped", "address": "Toshkent, ..."}

HTTP/1.1 200 OK
Content-Type: application/json

{"id": 42, "status": "shipped", "address": "Toshkent, ..."}
```

**(c) O'zini-o'zi tavsiflovchi xabarlar (self-descriptive messages).** Har bir so'rov va javob o'zini qanday qayta ishlashni o'zida tushuntiradi. `Content-Type: application/json` tananing formatini, status kodi natijani, `Cache-Control` keshlash qoidasini aytadi. Xabarni tushunish uchun tashqi, yashirin kontekst kerak emas — hammasi xabarning o'zida.

**(d) HATEOAS** — gipermedia ilova holatining dvigateli sifatida. Bu shunchalik muhim (va ko'p chalkashtiriladi) ki, alohida bo'limda ko'ramiz.

Uniform interface ning amaliy mevasi diagrammada ko'rinadi: bitta `/orders/42` resursi ustida `GET`, `PUT`, `PATCH`, `DELETE` metodlari **standart, oldindan ma'lum** ma'noga ega. Mijoz `/users/7` yoki `/products/9` ni ham xuddi shu qoidalar bilan ishlata oladi — har resurs uchun yangi qoida o'rganmaydi.

| Metod | Ma'nosi | Safe? | Idempotent? | Tipik javob |
|-------|---------|-------|-------------|-------------|
| `GET /orders/42` | Resursni o'qish | Ha | Ha | `200 OK` |
| `PUT /orders/42` | To'liq almashtirish | Yo'q | Ha | `200 OK` / `204 No Content` |
| `PATCH /orders/42` | Qisman o'zgartirish | Yo'q | Yo'q* | `200 OK` |
| `DELETE /orders/42` | O'chirish | Yo'q | Ha | `204 No Content` |

\* `PATCH` (RFC 5789) o'z-o'zidan idempotent emas, ammo patch tanasini idempotent qilib yozish mumkin. Metodlarning bu xossalari RFC 9110 da belgilangan; ular [HTTP chuqur bobida](./02-http-chuqur.md) batafsil.

> **Standart:** "Safe" = resursni o'zgartirmaydi (faqat o'qiydi). "Idempotent" = bir so'rovni bir necha marta yuborish bir martagidek natija beradi. Bu xossalar — uniform interface ning "bashorat qilinadigan" bo'lishining asosiy sababi: mijoz `GET` xavfsiz, `DELETE` ni qayta yuborsa ham zararsiz ekanini oldindan biladi.

## HATEOAS — gipermedia dvigateli

**HATEOAS** = *Hypermedia As The Engine Of Application State*. Intuitsiya: yaxshi tuzilgan veb-sahifani ochsangiz, keyin nima qilishni bilasiz — chunki sahifada **havolalar va tugmalar** bor ("Keyingi", "Bekor qilish", "To'lov"). Siz URL'larni yoddan bilishingiz shart emas; sahifa sizni yetaklaydi. HATEOAS — API javobi ham xuddi shunday bo'lishi g'oyasi: javob ichida **keyingi mumkin amallarning havolalari** bo'ladi.

HATEOAS'siz javob (faqat ma'lumot):

```json
{
  "id": 42,
  "status": "pending",
  "total": 150000
}
```

HATEOAS bilan javob — mijozga "endi nima qila olasan" ni ham aytadi:

```json
{
  "id": 42,
  "status": "pending",
  "total": 150000,
  "_links": {
    "self": { "href": "/orders/42" },
    "cancel": { "href": "/orders/42/cancel", "method": "POST" },
    "pay": { "href": "/orders/42/pay", "method": "POST" }
  }
}
```

Endi mijoz "bu buyurtmani bekor qilsa bo'ladimi?" deb biznes-qoidalarni o'zida takrorlamaydi — agar `cancel` havolasi javobda bo'lsa, demak amal mumkin. Buyurtma `shipped` holatiga o'tsa, server `cancel` havolasini olib tashlaydi va mijozga "endi bekor qilib bo'lmaydi" ni shu tarzda bildiradi. Ilova holati (qaysi amallar mavjud) serverdan kelgan havolalar orqali boshqariladi — nomning ma'nosi shu.

> **Halollik / Trade-off:** HATEOAS nazariy jihatdan kuchli — u mijozni serverdagi URL tuzilishi va biznes-qoidalardan ajratadi, server URL'larni o'zgartirsa ham mijoz buzilmaydi. **Ammo amalda u kam qo'llaniladi.** Sabablari: mijozlar ko'pincha URL'larni baribir qattiq kodlaydi (havoladan to'liq foydalanmaydi); javoblar kattalashadi; vositalar (SDK, generator) HATEOAS'siz ham yaxshi ishlaydi; va to'liq gipermedia-yetaklanadigan mijoz yozish murakkab. Shuning uchun ko'p muvaffaqiyatli "REST" API HATEOAS'siz qoladi va bu **normal**. HATEOAS — foydali, lekin har joyda majburiy emas: moslashuvchanlik evaziga murakkablik qabul qilasiz.

Mana shu yerda Richardson Maturity Model yordamga keladi — u "qancha REST?" degan savolga aniq til beradi.

## Richardson Maturity Model (RMM)

![Richardson Maturity Model: L0 dan L3 gacha yetuklik zinapoyasi](rasmlar/api05-rmm.svg)

Leonard Richardson API'ning "REST'ga qanchalik yaqinligini" o'lchaydigan to'rt darajali model taklif qildi; Martin Fowler uni "Glory of REST" maqolasida ommalashtirdi. Bu — RFC emas, balki **tahlil va o'qitish asbobi**: u REST'ni alohida bosqichlarga ajratib, har birining qiymatini ko'rsatadi. Diagrammadagi zinapoyani pastdan yuqoriga ko'ramiz.

### L0 — Botqoq (The Swamp of POX)

Bitta endpoint, **hamma narsa POST**. HTTP shunchaki "tunnel" sifatida ishlatiladi — metodlar va URI'larning ma'nosidan foydalanilmaydi. Bu — RPC-over-HTTP; klassik misol — SOAP yoki eski XML-RPC.

```http
POST /api HTTP/1.1
Host: api.example.com
Content-Type: application/json

{"method": "getOrder", "params": {"id": 42}}
```

Buyurtma yaratish, o'chirish, qidirish — hammasi shu bitta `POST /api` ga turli `method` qiymati bilan boradi. URI bitta, metod bitta; ma'no faqat tana ichida.

### L1 — Resurslar

Endi tizimda **ko'p URI** bor — har bir ob'ekt o'z manziliga ega ("divide and conquer"). Lekin HTTP fe'llari hali to'g'ri ishlatilmaydi; ko'pincha hammasi baribir `POST`.

```http
POST /orders/42 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{"action": "cancel"}
```

`/orders/42`, `/orders/42/cancel`, `/users/7` kabi alohida manzillar paydo bo'ldi — bu yutuq. Ammo "o'qish" va "o'chirish" baribir `POST` orqali, amal nomi URI yoki tanada. Yarim yo'l.

### L2 — HTTP fe'llar + status kodlar

**Ko'pchilik "REST" API aynan shu yerda.** HTTP metodlari **semantik to'g'ri** ishlatiladi (`GET` o'qiydi, `POST` yaratadi, `PUT`/`PATCH` o'zgartiradi, `DELETE` o'chiradi) va status kodlari **mazmunli** qaytadi (`200`, `201 Created`, `404`, `409 Conflict`).

```http
GET /orders/42 HTTP/1.1
Host: api.example.com
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{"id": 42, "status": "pending", "total": 150000}
```

```http
DELETE /orders/42 HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>

HTTP/1.1 204 No Content
```

Bu darajada API butun HTTP infratuzilmasidan — keshlash, idempotentlik, status kodlarga asoslangan xatolar — to'liq foydalanadi. Status kodlari [03-bobda](./03-http-status-kodlari.md) batafsil. Amaliy nuqtai nazardan, L2 — "yaxshi, professional REST API" ning realistik chegarasi.

### L3 — HATEOAS (gipermedia)

Yuqori daraja: L2 ning hamma narsasi, ustiga javoblar **gipermedia havolalarini** o'z ichiga oladi (yuqorida ko'rgan `_links`). Mijoz keyingi amallarni javobdagi havolalardan o'rganadi, URL'larni qattiq kodlamaydi. Fielding talqinida faqat L3 "haqiqiy REST".

```json
{
  "id": 42,
  "status": "pending",
  "_links": {
    "self": { "href": "/orders/42" },
    "cancel": { "href": "/orders/42/cancel" }
  }
}
```

| Daraja | Nima qo'shiladi | Misol | Holat |
|--------|-----------------|-------|-------|
| **L0** | Yo'q (bitta endpoint, POST) | `POST /api` | RPC-over-HTTP (SOAP) |
| **L1** | Resurslar (ko'p URI) | `POST /orders/42` | Yarim yo'l |
| **L2** | HTTP fe'llar + status kodlar | `GET /orders/42 -> 200` | Ko'p "REST" API |
| **L3** | Gipermedia (HATEOAS) | `_links` javobda | "Haqiqiy REST", kam |

> **Eslatma:** RMM zinapoyasi — bu "yuqoriroq har doim yaxshiroq" degani emas. U "qaysi HTTP imkoniyatlaridan foydalanyapsiz?" degan savolga aniq til beradi. Ko'p loyiha uchun L2 — to'g'ri to'xtash nuqtasi; L3 ga o'tish foydasi ko'pincha qo'shilgan murakkablikni qoplamaydi.

## "RESTful" vs haqiqiy REST — halol gap

Endi muhim haqiqat. Fieldingning qat'iy talqinida API faqat **L3 (HATEOAS)** bo'lsagina "haqiqatan REST" hisoblanadi. Fielding hatto "agar gipermedia yo'q bo'lsa, bu REST emas" deb yozgan. Amaliyotda esa deyarli barcha mashhur "REST API"lar (jamoatchilik, ichki) **L2** da to'xtaydi va o'zini "REST" yoki "RESTful" deb ataydi.

Bu — **xato emas, balki amaliy norma**. Sanoatdagi "REST" so'zining ma'nosi vaqt o'tib akademik ta'rifdan biroz farq qila boshladi: ko'pchilik uchun "REST API" = "resurslarga URI bergan, HTTP fe'llari va status kodlaridan to'g'ri foydalanadigan, JSON qaytaradigan stateless API" (ya'ni L2). Buni bilib turish — chalkashlikning oldini oladi:

- Agar kimdir "bizning API to'liq RESTful" desa, deyarli har doim L2 nazarda tutiladi.
- Agar sizga "to'liq RESTful, HATEOAS bilan" kerak bo'lsa, buni **alohida talab qilib** aniqlashtiring — bu kamdan-kam standart.
- "REST emas, chunki HATEOAS yo'q" degan tanqid texnik jihatdan to'g'ri, ammo amaliy jihatdan ko'pincha ahamiyatsiz — muhimi API izchil, bashoratli va HTTP semantikasiga sodiqmi.

> **Trade-off:** "Toza" REST (L3) g'oyaviy jihatdan chiroyli, lekin uning to'liq foydasi (mijozni URL'lardan ajratish) faqat mijozlar haqiqatan gipermedia-yetaklanadigan bo'lsagina ro'yobga chiqadi — bu kam uchraydi. Shuning uchun ko'p jamoa ataylab L2 da to'xtaydi. Bu — dangasalik emas, balki ongli muhandislik tanlovi.

## Nega stateless va cacheable shunchalik kuchli

REST ning ikki cheklovi — `stateless` va `cacheable` — birgalikda Web ning **ulkan masshtabini** mumkin qiladi, va bu API dizayni uchun amaliy ahamiyatga ega:

- **Stateless** — har server o'zaro almashtiriladigan bo'lgani uchun, oldiga shunchaki **ko'proq server** qo'yib gorizontal masshtablash mumkin. Holat yo'qligi nosozlikka chidamlilikni ham oshiradi.
- **Cacheable** — javoblar keshlanadigan deb belgilansa, takroriy o'qishlar serverga umuman yetib bormaydi: ularni CDN, reverse-proxy yoki brauzer keshi qaytaradi. Bu serverdagi yukni keskin kamaytiradi. Bu mexanizm — `ETag`, `Cache-Control`, `304 Not Modified` — [keshlash bobida](./16-keshlash.md) batafsil ochiladi.

Ikkalasi `layered system` bilan birlashganda, API oldiga kesh, gateway, balanslagich qatlamlarini mijozga sezdirmasdan qo'yish mumkin bo'ladi. Bu — REST'ning eng katta amaliy yutug'i va u to'g'ridan-to'g'ri tizim arxitekturasi tamoyillari bilan bog'lanadi (gorizontal masshtablash, keshlash qatlamlari, stateless xizmatlar) — bu mavzular [Dasturiy arxitektura kitobida](../arxitektura/README.md) chuqurroq yoritilgan.

> **Eslatma:** Shu sababdan ham REST hali ham eng keng tarqalgan API uslubi: u qimmatga tushadigan murakkab protokol talab qilmasdan, mavjud Web infratuzilmasi (kesh, proksi, CDN) ustida bepul masshtablanadi. Boshqa uslublar bilan taqqoslash [04-bobda](./04-api-uslublari.md).

## Asosiy g'oyalar (bobni qisqacha)

- **REST — protokol emas, arxitektura uslubi.** Roy Fielding (2000) Web nega masshtablanuvchan ekanini umumlashtirgan. "REST" = REpresentational State Transfer: mijoz va server resursning **tasvirlarini** (JSON kabi) uzatadi.
- **Oltita cheklov:** client-server, stateless, cacheable, uniform interface, layered system, code-on-demand (ixtiyoriy). Har biri nimanidir cheklab, masshtab/soddalik/mustaqillik beradi.
- **Stateless** = server mijoz sessiyasini saqlamaydi; har so'rov o'zini-o'zi yetarli (auth + kontekst har safar). Foyda: oson masshtablash va ishonchlilik; narx: har so'rovda ko'proq ma'lumot.
- **Uniform interface** = resurs URI orqali identifikatsiya, tasvir orqali manipulyatsiya, o'zini-o'zi tavsiflovchi xabarlar, HATEOAS. Natija — bashorat qilinadigan, bir marta o'rganiladigan interfeys.
- **HATEOAS** javobga keyingi amallarning havolalarini qo'shadi — nazariy jihatdan kuchli, **amalda kam**.
- **RMM:** L0 (bitta endpoint/POST) → L1 (resurslar) → L2 (fe'llar + status kodlar, ko'p "REST" API shu yerda) → L3 (HATEOAS). Tahlil asbobi, RFC emas.
- **"RESTful" odatda L2 ni anglatadi** — bu xato emas, amaliy norma. "Haqiqiy REST" (L3) ni alohida talab qilib aniqlashtiring.

## Mashqlar

### Oson

**1-mashq.** REST ning oltita cheklovini nomlang va ulardan qaysi biri ixtiyoriy ekanini ayting.

**2-mashq.** Quyidagi API qaysi RMM darajasida? Sababini ayting:

```http
POST /api HTTP/1.1
Content-Type: application/json

{"method": "deleteUser", "id": 7}
```

**3-mashq.** Quyidagi ikki javobdan qaysi biri L3 (HATEOAS) ga mos? Nega?

```json
{"id": 42, "status": "pending"}
```

```json
{"id": 42, "status": "pending", "_links": {"cancel": {"href": "/orders/42/cancel"}}}
```

### O'rta

**4-mashq.** Quyidagi API'ni RMM darajasiga baholang va nega aynan shu daraja ekanini tushuntiring:

```http
GET /orders/42 HTTP/1.1
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{"id": 42, "status": "shipped"}
```

**5-mashq.** Quyidagi ikki dizayndan qaysi biri stateless, qaysi biri stateful? Har birini bir jumlada asoslang.

- (A) Mijoz `POST /login` qiladi, server `Set-Cookie: SESSIONID=...` qaytaradi va keyingi so'rovlar serverning xotirasidagi sessiyaga tayanadi.
- (B) Mijoz har so'rovda `Authorization: Bearer <token>` yuboradi va server tokenni o'sha so'rovda tekshiradi.

**6-mashq.** `GET /orders/42` javobiga HATEOAS havolalarini qo'shing. Buyurtma `pending` holatida — `cancel` va `pay` amallari mumkin; `self` havolasi ham bo'lsin. Valid JSON yozing.

### Qiyin

**7-mashq.** Stateless dizayn masshtablashga aniq qanday yordam berishini tushuntiring: nega 3 ta serverga ega stateless API ga yana 5 ta server qo'shish oson, stateful API ga esa qiyin? Yuk balanslagich roli haqida ham gapiring.

**8-mashq.** Bir jamoa o'zining L2 REST API'sini L3 (HATEOAS) ga ko'tarishni muhokama qilyapti. Bu o'tishning ikki foydasi va ikki narxini sanab bering va qaysi holatda o'tish oqlanishini, qaysida yo'qligini ayting.

**9-mashq.** Bir vendor "bizning API to'liq RESTful" deydi, lekin javoblarda hech qanday gipermedia havola yo'q va u faqat HTTP fe'llar + status kodlardan foydalanadi. Bu da'voni RMM va Fielding ta'rifi nuqtai nazaridan tanqid qiling — texnik jihatdan da'vo to'g'rimi, amaliy jihatdan muhimi?

<details markdown="1">
<summary>Yechimlar</summary>

### 1-mashq yechimi

Oltita cheklov: (1) **Client-Server** — mijoz va server ajratilgan; (2) **Stateless** — server sessiya saqlamaydi; (3) **Cacheable** — javoblar keshlanadigan deb belgilanadi; (4) **Uniform Interface** — barcha resurslar bir xil standart interfeys orqali; (5) **Layered System** — oraliq qatlamlar mijozga shaffof; (6) **Code-on-Demand** — server kod yubora oladi. Oxirgisi — **Code-on-Demand** — yagona **ixtiyoriy** cheklov.

### 2-mashq yechimi

**L0**. Bitta endpoint (`/api`), hamma narsa `POST` orqali, amal nomi (`deleteUser`) tana ichida. Bu — RPC-over-HTTP: HTTP faqat tunnel sifatida ishlatiladi, na URI'lar resursni ko'rsatadi, na metod semantik ma'no beradi.

### 3-mashq yechimi

Ikkinchi javob — `_links` maydoni bilan — L3 (HATEOAS) ga mos. U javob ichida keyingi mumkin amalning (`cancel`) havolasini olib yuradi, ya'ni gipermedia ilova holatini boshqaradi. Birinchi javob faqat ma'lumotdan iborat, havolasiz — bu L2 (yoki undan past) ga xos.

### 4-mashq yechimi

**L2**. Bu yerda `GET` metodi semantik to'g'ri ishlatilgan (o'qish uchun, safe metod) va `200 OK` mazmunli status kodi qaytarilgan. Resurs `/orders/42` o'z URI'siga ega (L1 belgisi) va HTTP fe'l + status kodi to'g'ri ishlatilmoqda (L2 belgisi). Javobda gipermedia havolalar (`_links`) yo'q, shuning uchun bu L3 emas. Bu — eng keng tarqalgan "REST API" darajasi.

### 5-mashq yechimi

- (A) — **stateful**. Server `SESSIONID` ga bog'liq sessiya kontekstini **o'z xotirasida** saqlaydi; keyingi so'rovlar shu eslab qolingan holatga tayanadi. Boshqa serverga o'tilsa, u sessiyani bilmaydi.
- (B) — **stateless**. Har so'rov `Authorization` tokeni orqali o'zini-o'zi tasdiqlaydi; server so'rovlararo hech narsani eslab qolmaydi, shuning uchun istalgan server uni qayta ishlay oladi.

### 6-mashq yechimi

```json
{
  "id": 42,
  "status": "pending",
  "total": 150000,
  "_links": {
    "self": { "href": "/orders/42" },
    "cancel": { "href": "/orders/42/cancel", "method": "POST" },
    "pay": { "href": "/orders/42/pay", "method": "POST" }
  }
}
```

`self` resursning o'z manzilini, `cancel` va `pay` esa `pending` holatda mumkin bo'lgan amallarni ko'rsatadi. Buyurtma `shipped` ga o'tsa, server `cancel` havolasini olib tashlab, amal endi mumkin emasligini bildiradi.

### 7-mashq yechimi

Stateless API da har bir server **o'zaro almashtiriladigan** (interchangeable) — chunki hech bir server biror so'rovga xos sessiya holatini saqlamaydi. Demak yuk balanslagich kelgan so'rovni **istalgan** serverga yo'naltira oladi va ular bir xil natija beradi (auth + kontekst har so'rovda kelgani uchun). 5 ta yangi server qo'shish — shunchaki ularni balanslagich hovuziga ulash; hech qanday holat ko'chirish, sessiyani moslashtirish kerak emas.

Stateful API da esa har bir foydalanuvchining sessiyasi **muayyan** server xotirasida yashaydi. Yuk balanslagich ularni o'sha serverga "yopishtirib" yuborishi (sticky session) kerak; yangi server qo'shilsa, mavjud sessiyalar avtomatik undan foydalana olmaydi, server qulasa sessiyalar yo'qoladi. Shuning uchun masshtablash murakkab: sessiyani tashqi umumiy omborga (Redis) ko'chirish kabi qo'shimcha mexanizm talab qilinadi. Stateless bu muammoni dizayn darajasida yo'q qiladi.

### 8-mashq yechimi

**Foydalari:** (1) Mijoz serverdagi URL tuzilishi va biznes-qoidalardan ajraladi — server URL'larni o'zgartirsa yoki amal qachon mumkinligini o'zgartirsa, mijoz kodi buzilmaydi (havolaning bor-yo'qligi yetaklaydi). (2) API o'zini-o'zi hujjatlaydigan va kashf qilinadigan (discoverable) bo'ladi — javob keyingi qadamlarni ko'rsatadi.

**Narxlari:** (1) Mijoz va server tomonida murakkablik ortadi — gipermedia-yetaklanadigan mijoz yozish va havolalar mantig'ini boshqarish qiyin. (2) Javoblar kattalashadi (har javobda havolalar to'plami), va aksar mijozlar baribir URL'larni qattiq kodlab, foydani ro'yobga chiqarmaydi.

**Qachon oqlanadi:** uzoq yashaydigan, ko'p turli mijozli, tez evolyutsiyalanadigan **jamoat API** — bu yerda mijozni URL'lardan ajratish real qiymat beradi. **Qachon yo'q:** ichki yoki bitta-mijozli API, barqaror URL'lar, oddiy CRUD — bu yerda qo'shilgan murakkablik foydani qoplamaydi va L2 da qolish to'g'riroq.

### 9-mashq yechimi

**Texnik jihatdan, qat'iy ta'rifda — da'vo to'liq to'g'ri emas.** Fielding talqinida va RMM bo'yicha "haqiqiy REST" faqat **L3** — gipermedia (HATEOAS) bilan. Gipermedia havolalari yo'q API **L2** da, demak "to'liq RESTful" deyish akademik jihatdan noaniq; aniqrog'i "L2 REST API" deyish kerak edi.

**Amaliy jihatdan — bu da'vo deyarli ahamiyatsiz va keng qabul qilingan.** Sanoatda "REST API" so'zi amalda L2 ni anglatadi: resurs-URI'lar, to'g'ri HTTP fe'llar, mazmunli status kodlar, stateless. Vendor aynan shularga amal qilsa, uning API'si professional va izchil. Shuning uchun tanqid "siz HATEOAS qo'shmagansiz" emas, balki "API izchilmi, hujjatli, bashoratli, HTTP semantikasiga sodiqmi?" degan amaliy savollarga qaratilishi kerak. Faqat agar mijozlarni URL'lardan ajratish real talab bo'lsa, HATEOAS yo'qligi haqiqiy kamchilik bo'ladi — aks holda L2 to'liq maqbul.

</details>

---

[⬅️ Oldingi: 04 — API uslublari: REST, RPC, GraphQL, gRPC](./04-api-uslublari.md) · [🏠 README](./README.md) · [Keyingi: 06 — Resurs modellashtirish va URI dizayni ➡️](./06-resurs-uri-dizayni.md)
