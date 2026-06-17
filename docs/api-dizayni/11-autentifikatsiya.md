# 11 — Autentifikatsiya

[⬅️ Oldingi: 10 — API versiyalash va evolyutsiya](./10-versiyalash.md) · [🏠 README](./README.md) · [Keyingi: 12 — Avtorizatsiya va ruxsatlar ➡️](./12-avtorizatsiya.md)

---

> **Bu bobda:** API'ga so'rov yuborgan tomon **kim ekanini** qanday tasdiqlaymiz? Bu bob autentifikatsiyaning (authn) avtorizatsiyadan (authz) farqini aniq ajratadi, asosiy usullarni (API key, Basic, Bearer token / JWT, OAuth 2.0 / OIDC) trade-off bilan ko'rib chiqadi, JWT tuzilishi va uning bekor qilish (revocation) muammosini ochib beradi, hamda OAuth 2.0 (RFC 6749) delegatsiyasini va Authorization Code + PKCE oqimini tushuntiradi.
>
> **Halollik / Eslatma:** Aniq standartlarga tayanamiz: **OAuth 2.0 = RFC 6749** (joriy, yakuniy RFC), **OAuth 2.1 = IETF DRAFT** (hali yakuniy RFC EMAS) — eng yaxshi amaliyotlarni jamlaydi; **JWT = RFC 7519**; **Bearer token = RFC 6750**; **PKCE = RFC 7636**; status kodlari (`401`, `403`) = **RFC 9110**. Qaysi usulni tanlash esa ko'pincha kontekstga-bog'liq **trade-off** — mutlaq qoida emas. JSON namunalari valid. Standartlar va versiyalar vaqt bilan o'zgaradi.

---

## Autentifikatsiya nima — va u avtorizatsiya emas

Tasavvur qiling, ofis binosiga kirayapsiz. Eshik oldida ikki alohida tekshiruv bor:

1. **Qo'riqchi pasportingizni ko'radi:** "Bu odam rostdan ham aytgani — Ali Valiyevmi?" Bu — **autentifikatsiya** (authentication, qisqasi *authn*): "**KIM** ekaningni tasdiqlash".
2. **Keyin propuskingizni tekshiradi:** "Ali Valiyev 5-qavatdagi serverxonaga kira oladimi?" Bu — **avtorizatsiya** (authorization, *authz*): "**NIMAGA** ruxsating bor".

Bular ikki **alohida** savol va ularni aralashtirib yuborish — API dizaynidagi eng keng tarqalgan chalkashlik. Avval kimligingni bilamiz, *keyin* nimaga ruxsating borligini hal qilamiz.

| | Autentifikatsiya (authn) | Avtorizatsiya (authz) |
|---|---|---|
| Savol | "Kim sen?" | "Senga nimaga ruxsat?" |
| Tekshiradi | Shaxsni (token, parol, kalit) | Ruxsatni (rol, scope, egalik) |
| Tartib | Avval | Keyin (authn'dan so'ng) |
| Muvaffaqiyatsizlikda | **401 Unauthorized** | **403 Forbidden** |
| Misol | "Bu token haqiqiymi?" | "Bu foydalanuvchi shu buyurtmani o'qiy oladimi?" |

> **Diqqat:** Status kodlarining nomlari chalg'ituvchi. **401 Unauthorized** aslida "**unauthenticated**" (kim ekaning noma'lum yoki token noto'g'ri) degani — bu **authn** xatosi. **403 Forbidden** esa "kim ekaning ma'lum, lekin bu amalga ruxsating yo'q" — bu **authz** xatosi (RFC 9110). Demak `401` = "o'zingni tanitib kel"; `403` = "tanidim, lekin senga yo'q". Bu farq [03-bobda](./03-http-status-kodlari.md) batafsil ko'rilgan.

Bu bob faqat **birinchi** savolga — autentifikatsiyaga — bag'ishlangan. Ikkinchi savol, ya'ni ruxsatlar, rollar, scope va egalik tekshiruvi, keyingi [12-bob — Avtorizatsiya](./12-avtorizatsiya.md) mavzusi. Ko'pincha amalda token bir vaqtning o'zida ikkalasini ham olib yuradi (kim ekaning + qanday scope'laring bor) — lekin tushunchaviy jihatdan ularni alohida ko'rish muhim.

---

## Autentifikatsiya usullari: bir maqsad, to'rt yo'l

So'rov yuborgan tomon o'zini qanday tanitadi? Tarixan soddadan murakkabga qarab to'rtta asosiy usul shakllangan. Har biri boshqa muammoni yechadi va boshqa narxga ega.

![Autentifikatsiya usullari taqqoslash](rasmlar/api11-auth-usullari.svg)

### 1. API key — eng oddiy sir

API key — bu shunchaki uzun, taxmin qilib bo'lmaydigan **sir satr** (masalan `sk_live_a1b2c3...`). Mijoz uni har so'rovda yuboradi, server bazadan tekshiradi: "Bu kalit menda bormi va aktivmi?"

Kalit **sarlavhada** yuboriladi — odatda maxsus sarlavhada yoki `Authorization` sxemasi sifatida:

```http
GET /v1/weather?city=Tashkent HTTP/1.1
Host: api.example.com
X-API-Key: sk_live_a1b2c3d4e5f6

HTTP/1.1 200 OK
Content-Type: application/json

{"city": "Tashkent", "temp_c": 21}
```

- **Kuchli:** juda sodda — bir satr sir, hech qanday oqim yo'q. Server-to-server chaqiruvlar va ochiq (public) ma'lumotli API'lar uchun ideal. Berish/bekor qilish oddiy.
- **Zaif:** kalit **foydalanuvchini ifodalamaydi** — u "qaysi *ilova/hisob*" ekanini bildiradi, "qaysi *odam*" ekanini emas. Kalitni aylantirish (rotation) va scope'lash (har kalitga aniq ruxsatlar) qo'shimcha ish talab qiladi. Va sir bo'lgani uchun, sizib chiqsa — to'liq kirish beradi.

> **Xavfsizlik:** API key'ni **URL query'da YUBORMANG** (`?api_key=...`). URL'lar server loglariga, proxy loglariga, brauzer tarixiga, `Referer` sarlavhasiga tushadi — sir o'sha yerlarda ochiq qoladi. Kalitni **sarlavhada** yuboring (`X-API-Key` yoki `Authorization: ApiKey ...`). Bu OWASP API Security'ning "Security Misconfiguration" (API8, 2023) toifasiga tegishli keng tarqalgan xato.

### 2. Basic Auth — parol har so'rovda

HTTP Basic autentifikatsiya (RFC 9110 doirasida) — foydalanuvchi nomi va parolni `user:parol` ko'rinishida birlashtirib, **base64** bilan kodlab yuboradi:

```http
GET /v1/profile HTTP/1.1
Host: api.example.com
Authorization: Basic YWxpOnNlY3JldDEyMw==

HTTP/1.1 200 OK
Content-Type: application/json

{"id": 42, "name": "Ali"}
```

Bu yerda `YWxpOnNlY3JldDEyMw==` — bu `ali:secret123` ning base64 ko'rinishi.

- **Kuchli:** o'rnatilgan, qo'llab-quvvatlanadigan, juda oddiy. Ichki vositalar yoki tezkor prototip uchun mos.
- **Zaif:** base64 — bu **kodlash, shifrlash emas**; har kim uni qaytarib ochib parolni o'qiy oladi. Demak **faqat HTTPS** ustida ishlatish mumkin (aks holda parol ochiq uzatiladi). Va parol **har so'rovda** yuboriladi — bu uni ochib qo'yish ehtimolini oshiradi, hamda mijozda parolni saqlab turishni talab qiladi.

> **Xavfsizlik:** Basic Auth'da `Base64` — sir emas, shaffof. HTTPS bo'lmasa, bu deyarli "parolni ochiq matnda yuborish" bilan teng. Token-asosidagi usullar (pastda) parolni faqat bir marta ishlatib, keyin qisqa-muddatli token bilan almashtiradi — bu xavfni kamaytiradi.

### 3. Bearer token — eng keng tarqalgan zamonaviy usul

"Bearer" so'zi "egasiga tegishli" degani: tokenga **ega bo'lgan** har kim u bilan kirishi mumkin (xuddi naqd puldek — kim ushlasa, o'shaniki). Token `Authorization` sarlavhasida `Bearer` sxemasi bilan yuboriladi (RFC 6750):

```http
GET /v1/orders/1001 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiJ9.SflKxw

HTTP/1.1 200 OK
Content-Type: application/json

{"id": 1001, "status": "paid"}
```

Token ikki xil bo'lishi mumkin (buni pastda chuqurroq ko'ramiz):

- **Opaque token** — ma'nosi yo'q tasodifiy satr; server uni bazada qidirib "bu kimning tokeni?" deb topadi.
- **JWT** — o'zida ma'lumot olib yuradigan, imzolangan token; server bazaga bormay, imzoni tekshirib o'qiydi.

Bearer token bugun **eng keng tarqalgan** usul — chunki u parolni har so'rovda yuborishdan qutqaradi (bir marta login → token), qisqa muddatli bo'lishi mumkin, va foydalanuvchini ifodalaydi.

> **Xavfsizlik:** Bearer token "egasiga tegishli" bo'lgani uchun, uni o'g'irlagan har kim foydalana oladi. Demak: faqat HTTPS ustida yuboring; mijozda xavfsiz saqlang (pastga qarang); muddatini qisqa qiling. Bu yer OWASP API2:2023 "Broken Authentication" eng ko'p buziladigan nuqta.

### 4. OAuth 2.0 / OIDC — uchinchi tomonga delegatsiya

Yuqoridagi uchtasi — "men API egasiman, mijozim menga to'g'ridan-to'g'ri sir/parol/token beradi" holatlari. Lekin boshqa, murakkabroq stsenariy bor: **uchinchi tomonga foydalanuvchi nomidan ruxsat berish**.

Klassik misol: "Loyiha-Boshqaruv" ilovasi sizning Google Kalendaringizga *yozmoqchi*. Siz Google parolingizni shu ilovaga **bermasligingiz kerak** — bu xavfli (ilova parolni ko'radi, hammasiga kira oladi, parolni o'zgartirsangiz buziladi). Buning o'rniga **OAuth 2.0** (RFC 6749) ishlatiladi: foydalanuvchi to'g'ridan-to'g'ri Google'da login qiladi va ilovaga *cheklangan, bekor qilinadigan ruxsat* (faqat kalendar) beradi — parolni umuman ko'rsatmasdan.

OAuth — bu butun bir mexanizm; uni keyingi bo'limlarda alohida ochamiz. Hozircha asosiy g'oya: **delegatsiyalangan ruxsat** — parolni uzatmasdan, cheklangan kirish berish.

### Qaysi usul qachon — qaror jadvali

| Usul | Foydalanuvchini ifodalaydimi? | Qachon ishlatish | Asosiy ehtiyot |
|---|---|---|---|
| **API key** | Yo'q (ilova/hisob) | Server-to-server, ochiq ma'lumot, oddiy integratsiya | Query'da emas; aylantirish/scope qiyin |
| **Basic Auth** | Ha (user:parol) | Ichki vositalar, tezkor prototip | Faqat HTTPS; parol har so'rovda |
| **Bearer token** | Ha (token ichida) | Foydalanuvchili API: SPA, mobil, web | HTTPS; xavfsiz saqlash; qisqa muddat |
| **OAuth 2.0 / OIDC** | Ha (delegatsiya orqali) | Uchinchi tomon ruxsati, SSO, "X bilan kirish" | To'g'ri grant turini tanlash; PKCE |

> **Trade-off:** "Eng to'g'ri" usul yo'q — kontekst hal qiladi. Bitta ichki cron-skript ochiq ob-havo API'siga chaqirsa, **API key** yetarli — OAuth bu yerda ortiqcha murakkablik. Aksincha, millionlab foydalanuvchili mobil ilova uchun **OAuth + Bearer (JWT)** to'g'ri tanlov. Murakkablikni ehtiyojga moslang, "zamonaviy" deb emas.

---

## Token: opaque va JWT

Bearer token deganimizda eng muhim dizayn qarori — bu token **opaque** bo'ladimi yoki **self-contained (JWT)** bo'ladimi. Bu trade-off butun autentifikatsiya arxitekturangizni belgilaydi.

### Opaque token — ma'nosi serverda

Opaque token — bu shunchaki tasodifiy satr (masalan `a8f5f167f44f4964e6c998dee827110c`). Uning ichida hech qanday ma'lumot yo'q. Server uni qabul qilganda, **bazaga/keshga boradi** va qidiradi: "Bu token kimga tegishli, qachon tugaydi, qaysi scope'lari bor?"

- **Kuchli:** **bekor qilish (revocation) oson** — bazadan o'chirsangiz, token o'sha zahoti yaroqsiz. Token hech qanday foydalanuvchi ma'lumotini oshkor qilmaydi (faqat tasodifiy satr). Mijozda saqlanadigan ma'lumot minimal.
- **Zaif:** **har so'rov bazaga boradi** (yoki tez keshga) — bu qo'shimcha kechikish va serverdagi holat (state). Bu [05-bobdagi](./05-rest-tamoyillari.md) "stateless" idealiga biroz zid (server token holatini saqlaydi).

### JWT — ma'lumot tokenning o'zida

**JWT** (JSON Web Token, RFC 7519) — bu **o'zida ma'lumot olib yuradigan** (self-contained), **imzolangan** token. Uni ochib o'qiganda, ichidan foydalanuvchi ID'si, muddati va boshqa ma'lumotlar chiqadi — serverga bazaga borish shart emas.

![JWT tuzilishi](rasmlar/api11-jwt-tuzilishi.svg)

JWT uchta qismdan iborat, nuqta bilan ajratilgan, har biri **base64url** kodlangan: `header.payload.signature`.

**1. Header** — imzo algoritmi haqida:

```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

**2. Payload** — **claims** (da'volar), ya'ni token nimani aytadi:

```json
{
  "iss": "https://auth.example.com",
  "sub": "user_42",
  "aud": "https://api.example.com",
  "exp": 1735692600,
  "iat": 1735689000
}
```

Standart claim'lar (RFC 7519):

| Claim | Ma'nosi |
|---|---|
| `iss` (issuer) | Tokenni kim chiqargan (auth server) |
| `sub` (subject) | Token kim haqida (odatda foydalanuvchi ID) |
| `aud` (audience) | Token kim uchun mo'ljallangan (qaysi API) |
| `exp` (expiration) | Qachon tugaydi (Unix vaqti) |
| `iat` (issued at) | Qachon chiqarilgan |

**3. Signature** — header va payload'ni **sir/kalit bilan imzolab** olingan natija. Aynan shu imzo tokenni ishonchli qiladi.

### JWT'ni server qanday tekshiradi (stateless)

Server JWT'ni qabul qilganda:

1. Header va payload'ni o'qiydi.
2. **Imzoni qayta hisoblaydi** — o'zining sir/kalit'i bilan `header.payload` uchun imzo yasaydi.
3. Bu imzo tokendagi imzo bilan **mos kelsa** → token haqiqiy va **buzilmagan** (hech kim payload'ni o'zgartirmagan, chunki o'zgartirsa imzo mos kelmasdi).
4. Keyin `exp` (muddat o'tmaganmi?) va `aud` (bu token shu API uchunmi?) claim'larini ham tekshiradi.

Eng muhim jihat: **server bazaga bormaydi**. Imzo to'g'ri bo'lsa, server payload'dagi `sub` ni ishonib oladi — "bu user 42". Bu aynan **stateless** ([05-bobga](./05-rest-tamoyillari.md) qarang) — server token holatini saqlamaydi, har so'rov o'zini o'zi isbotlaydi. Shuning uchun JWT mikroservislar va masshtablanadigan tizimlarda mashhur.

> **Diqqat — JWT shifrlash EMAS.** Imzolangan JWT (JWS) **shifrlanmagan** — payload base64url, ya'ni har kim uni ochib o'qiy oladi. Imzo faqat **buzilmaslikni** (integrity) kafolatlaydi, **maxfiylikni** emas. Demak: **payload'ga sir/maxfiy ma'lumot QO'YMANG** (parol, karta raqami, shaxsiy ma'lumot). Faqat ID va kerakli, oshkor bo'lsa zarar qilmaydigan claim'lar.

### JWT'ning eng katta zaifligi: bekor qilish (revocation)

Mana JWT trade-off'ining yuragi. JWT stateless bo'lgani uchun — server uni *eslab qolmaydi*. Demak **chiqarilgan JWT'ni vaqtidan oldin bekor qilish qiyin**:

- Foydalanuvchi "logout" bosdi yoki tokeni o'g'irlandi → siz uni bloklamoqchisiz.
- Lekin server hech bazaga bormaydi — u faqat imzoni tekshiradi. Imzo hali ham to'g'ri va `exp` hali kelmagan, demak server tokenni **qabul qilaveradi**.

Bu opaque token'ning teskarisi: opaque'ni bazadan o'chirsangiz tamom; JWT'ni esa "unutib bo'lmaydi", chunki holat yo'q. Yechimlar:

1. **Qisqa muddat (short-lived) + refresh token.** Access token'ni qisqa qiling (masalan 5–15 daqiqa). Tokeni o'g'irlansa ham, tez tugaydi. Uzoq yashash uchun alohida **refresh token** ishlatiladi (pastda).
2. **Bekor qilish ro'yxati (denylist/blocklist).** Bekor qilingan token ID'larini (`jti` claim) keshda saqlash va har tekshiruvda solishtirish. Lekin diqqat: bu **statelilik qaytaradi** — JWT'ning bosh afzalligini qisman yo'qotadi.

> **Trade-off:** **opaque vs JWT** — bu "tezlik/masshtab vs nazorat" tanlovidir. **JWT:** stateless, tez, bazaga bormaydi, masshtablanadi — lekin bekor qilish qiyin. **Opaque:** bekor qilish oson, to'liq nazorat — lekin har so'rov bazaga/keshga boradi. Ko'p tizimlar ikkalasini **birga** ishlatadi: qisqa-muddatli JWT access token (tezlik) + opaque refresh token bazada (nazorat).

> **Xavfsizlik — `alg:none` va zaif imzo.** Tarixiy JWT zaifligi: ba'zi kutubxonalar `"alg": "none"` (imzosiz) tokenni qabul qilgan — buzg'unchi imzoni butunlay olib tashlab, istalgan payload yuborgan. Yana bir hujum: kalit turini almashtirish. Himoya: server **kutgan algoritmni qat'iy majburlasin** (masalan faqat `RS256`), `none` ni **hech qachon** qabul qilmasin, va imzoni har doim tekshirsin. Bu OWASP API2:2023 "Broken Authentication" ning klassik holati.

---

## OAuth 2.0: parolni bermasdan ruxsat berish

Endi OAuth'ga qaytamiz — uni alohida, chuqurroq ochamiz, chunki bu autentifikatsiya/ruxsat dunyosining eng muhim va eng ko'p chalkashtiriladigan mavzusi.

### Muammo: uchinchi tomonga ishonch

Yana o'sha misol: "Loyiha-Boshqaruv" ilovasi Google Kalendaringizga yozmoqchi. Eski (yomon) yo'l — ilovaga Google parolingizni berish. Buning oqibatlari:

- Ilova parolingizni ko'radi va saqlaydi (xavfli).
- Ilova *hamma narsangizga* kira oladi — faqat kalendar emas, Gmail, Drive, hammasi.
- Parolingizni o'zgartirsangiz — integratsiya buziladi.
- Ilovaga ishonchni bekor qilolmaysiz (faqat parolni o'zgartirish orqali, bu boshqa hamma narsani ham buzadi).

**OAuth 2.0** (RFC 6749) aynan shu muammoni yechadi: foydalanuvchi parolini uchinchi tomonga **bermasdan**, unga **cheklangan, bekor qilinadigan ruxsat** beradi.

### To'rt rol

OAuth'da to'rtta ishtirokchi bor:

| Rol | Kim | Bizning misolda |
|---|---|---|
| **Resource owner** | Resursga egalik qiluvchi foydalanuvchi | Siz (kalendar egasi) |
| **Client** | Ruxsat so'ragan ilova | "Loyiha-Boshqaruv" ilovasi |
| **Authorization server** | Ruxsat beruvchi va token chiqaruvchi | Google'ning auth serveri |
| **Resource server** | Himoyalangan API | Google Calendar API |

Asosiy g'oya: client foydalanuvchi parolini **hech qachon ko'rmaydi**. Buning o'rniga authorization server foydalanuvchini autentifikatsiya qiladi va client'ga **access token** beradi — bu token cheklangan scope'ga ega (faqat kalendar) va muddatli.

### Grant turlari: qaysi oqim qachon

OAuth'da access token olishning bir necha **grant** (ruxsat berish) turi bor. Bugun ikkitasi tavsiya etiladi:

#### Authorization Code + PKCE — foydalanuvchi-mijozlar uchun standart

Bu — SPA, mobil va web ilovalar uchun **standart** oqim. **PKCE** (Proof Key for Code Exchange, RFC 7636) qo'shimcha himoya beradi.

![OAuth Authorization Code + PKCE oqimi](rasmlar/api11-oauth-code-flow.svg)

Oqim ketma-ketligi:

1. **Tayyorgarlik (PKCE):** client tasodifiy sir `code_verifier` yasaydi va undan hash — `code_challenge` hisoblaydi.
2. **Authorize:** client foydalanuvchini auth serverga yo'naltiradi, `code_challenge` ni qo'shib.
3. **Login + rozilik:** foydalanuvchi *to'g'ridan-to'g'ri auth serverda* login qiladi va "bu ilovaga kalendarga ruxsat beraymi?" degan roziligini bildiradi. (Client parolni ko'rmaydi.)
4. **Authorization code:** auth server client'ga qisqa-muddatli **kod** (`code`) qaytaradi.
5. **Token almashtirish:** client bu kodni **va** `code_verifier` ni auth serverga yuboradi: "kodni token'ga almashtir".
6. **PKCE tekshiruvi:** auth server `hash(code_verifier) == code_challenge` ekanini tekshiradi. Mos kelsa — bu haqiqatan ham 1-qadamni boshlagan client.
7. **Token:** auth server **access token** (va ko'pincha **refresh token**) qaytaradi.
8. **API chaqiruv:** client access token'ni `Authorization: Bearer ...` da resource server (API)'ga yuboradi.

PKCE nima uchun kerak? **`code` o'g'irlanish himoyasi.** 4-qadamdagi kod (masalan brauzer redirect'i orqali) o'g'irlansa ham, buzg'unchida `code_verifier` yo'q — u faqat haqiqiy client'da. Verifiersiz kodni token'ga almashtirib bo'lmaydi. Avval PKCE faqat mobil/SPA uchun tavsiya etilardi; **endi barcha client'lar uchun** (OAuth 2.1 yo'nalishi).

Token javobi (5–7 qadamlar natijasi) odatda shunday:

```http
POST /oauth/token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&code=AUTH_CODE&code_verifier=VERIFIER&client_id=app123

HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0MiJ9.abc",
  "token_type": "Bearer",
  "expires_in": 900,
  "refresh_token": "v1.MnR0a2Vu",
  "scope": "calendar.read calendar.write"
}
```

#### Client Credentials — servis-to-servis

Foydalanuvchi umuman yo'q bo'lganda — bir backend boshqasiga to'g'ridan-to'g'ri chaqirsa — **Client Credentials** grant ishlatiladi. Bu yerda client o'zining `client_id` va `client_secret`'i bilan to'g'ridan-to'g'ri token oladi (hech qanday foydalanuvchi login'i yo'q):

```http
POST /oauth/token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=svc_billing&client_secret=SECRET&scope=invoices.read

HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJzdmNfYmlsbGluZyJ9.xyz",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "invoices.read"
}
```

### Eskirgan grant'lar — halol gap

Tarixan OAuth 2.0'da yana ikkita grant bo'lgan, lekin ular **endi tavsiya etilmaydi**:

- **Implicit grant** — access token'ni to'g'ridan-to'g'ri brauzer redirect URL'ida (fragment'da) qaytarar edi. Token URL'ga, brauzer tarixiga, loglarga tushib qolardi — xavfli. **Olib tashlandi.**
- **Password (ROPC — Resource Owner Password Credentials) grant** — client foydalanuvchi parolini *to'g'ridan-to'g'ri qabul qilib* tokenga almashtirardi. Bu OAuth'ning butun maqsadiga (parolni bermaslik) zid. **Olib tashlandi.**

> **Standart — OAuth 2.1 (DRAFT):** **OAuth 2.1 hali yakuniy RFC EMAS** — u IETF **draft**'i bo'lib, OAuth 2.0'ning eng yaxshi amaliyotlarini jamlaydi. Asosiy o'zgarishlar: (1) **Implicit grant olib tashlandi**, (2) **Password (ROPC) grant olib tashlandi**, (3) **PKCE barcha client'lar uchun majburiy**, (4) public client'lar uchun refresh token rotatsiyasi. Demak amaliy maslahat: yangi tizim qursangiz — **Authorization Code + PKCE** (foydalanuvchi uchun) yoki **Client Credentials** (servis uchun) ishlating; Implicit/Password'ni o'rganmang ham. Lekin halol bo'laylik: 2.1 hali draft, RFC 6749 esa joriy yakuniy standart.

### OIDC — autentifikatsiya qatlami

Diqqat qilingan bo'lsa: OAuth 2.0 aslida **avtorizatsiya** (ruxsat berish) protokoli — "bu ilovaga kalendarimga kirishga ruxsat". U sizning *kimligingizni* ilovaga aytishni maqsad qilmaydi.

**OpenID Connect (OIDC)** — bu OAuth 2.0 **ustiga qurilgan identifikatsiya (autentifikatsiya) qatlami**. U OAuth oqimiga **`id_token`** (JWT formatidagi shaxs token'i) qo'shadi — bu token "bu foydalanuvchi kim" (ismi, email, ID) deydi. Aynan OIDC "**Google bilan kirish**" / "**GitHub bilan kirish**" tugmalari ortida turadi: ilova sizning kimligingizni Google orqali bilib oladi, parolingizni ko'rmasdan.

> **Eslatma:** Sodda farq: **OAuth 2.0 = ruxsat** ("nimaga kirishi mumkin"), **OIDC = kimlik** ("bu kim"). OIDC OAuth'ni *almashtirmaydi*, balki uning ustiga `id_token` qo'shadi. "Login with X" kerak bo'lsa — OIDC.

---

## Access token va refresh token

Yuqorida ko'rdik: JWT access token'ni qisqa qilish kerak (bekor qilish muammosi). Lekin foydalanuvchini har 10 daqiqada qayta login qildirish — yomon tajriba. Yechim — **ikki token**:

| | Access token | Refresh token |
|---|---|---|
| Vazifasi | Har API chaqiruvda yuboriladi | Yangi access token olish uchun |
| Muddati | **Qisqa** (5–15 daqiqa) | **Uzoq** (kunlar/haftalar) |
| Qayerga yuboriladi | Resource server (API) | Faqat auth server |
| Tez-tez ishlatiladimi | Ha, har so'rovda | Yo'q, faqat access tugaganda |
| O'g'irlansa | Tez tugaydi (zarar cheklangan) | Xavfliroq → rotatsiya kerak |

Oqim: foydalanuvchi login qiladi → access + refresh token oladi. Access bilan API'ga chaqiradi. Access tugaganda, client **refresh token bilan jimgina yangi access token oladi** — foydalanuvchi qayta login qilmaydi:

```http
POST /oauth/token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token=v1.MnR0a2Vu&client_id=app123

HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0MiJ9.new",
  "token_type": "Bearer",
  "expires_in": 900,
  "refresh_token": "v1.bmV3UmVmcmVzaA"
}
```

Yuqorida diqqat qiling — javobda **yangi refresh token** ham qaytdi. Bu **refresh token rotatsiyasi**: har refresh'da eski refresh token bekor bo'ladi, yangisi beriladi. Agar o'g'irlangan eski refresh token ishlatishga urinilsa, server "bu allaqachon ishlatilgan" deb butun zanjirni bekor qiladi. Bu OAuth 2.1 yo'nalishidagi muhim himoya.

> **Diqqat — token tugaganda 401.** Access token muddati tugaganda yoki noto'g'ri bo'lganda, API **`401 Unauthorized`** qaytaradi (RFC 9110). Yaxshi mijoz buni ko'rib, **avtomatik refresh** qiladi va so'rovni qayta yuboradi — foydalanuvchi sezmaydi. `403` esa boshqa narsa: token to'g'ri, lekin ruxsat yetarli emas — bunda refresh yordam bermaydi.

### Token saqlash: mijozda xavfsizlik

Token — bu "egasiga tegishli" sir. Uni qayerda saqlash — muhim xavfsizlik qarori:

- **Server tomonidagi web ilova:** tokenni serverda saqlang; brauzerga faqat `HttpOnly`, `Secure`, `SameSite` cookie bering — JavaScript tokenni ko'rmasin (XSS himoyasi).
- **Mobil ilova:** platforma xavfsiz xotirasi (iOS Keychain, Android Keystore).
- **SPA (brauzer):** eng nozik holat. `localStorage` XSS'ga zaif (har qanday inject qilingan skript o'qiy oladi). Imkon qadar `HttpOnly` cookie + backend orqali ishlash xavfsizroq. Access token'ni xotirada (memory) saqlash ham keng tarqalgan.

> **Xavfsizlik:** Refresh token — uzoq yashaydi va eng qimmatli; uni alohida ehtiyot bilan saqlang (mobil xavfsiz xotira, yoki `HttpOnly` cookie). Token saqlash va umumiy API himoyasi (transport, XSS, CSRF, sir boshqaruvi) [13-bob — API xavfsizligi](./13-api-xavfsizligi.md) da chuqurroq ko'riladi.

---

## Session-cookie va token: qaysi biri?

Tarixan web ilovalar **session-cookie** autentifikatsiyasidan foydalangan: foydalanuvchi login qiladi, server `session_id` cookie beradi, server bazada session holatini saqlaydi. Zamonaviy API'lar esa ko'pincha **token** (Bearer) yo'lidan boradi.

| | Session-cookie | Token (Bearer) |
|---|---|---|
| Holat (state) | Server saqlaydi (stateful) | Stateless mumkin (JWT) |
| Saqlanishi | Brauzer cookie (avtomatik) | Mijoz qo'lda saqlaydi/yuboradi |
| Mobil/SPA mosligi | Noqulayroq | Tabiiy |
| CSRF | Zaif (cookie avtomatik ketadi) → himoya kerak | Kamroq (sarlavhada qo'lda yuboriladi) |
| Domenlararo / mikroservis | Qiyinroq | Oson |
| Bekor qilish | Oson (server session'ni o'chiradi) | JWT'da qiyin |

> **Trade-off:** **SPA, mobil va mikroservis** muhitida — odatda **token** afzal: stateless, domenlararo oson, mobil bilan tabiiy. **An'anaviy server-rendered web sayt** (faqat brauzer, bitta domen) uchun esa **session-cookie** hali ham sodda va ishonchli tanlov — `HttpOnly` cookie XSS'dan token'dagi `localStorage`'dan ko'ra xavfsizroq. Aralash yondashuvlar ham bor: SPA backend'i `HttpOnly` cookie bilan ishlaydi, ichida esa token saqlaydi (BFF naqshi, [23-bobda](./23-api-gateway-bff.md)).

---

## Asosiy g'oyalar (bobni qisqacha)

- **Autentifikatsiya (authn) = "kim ekaning"** ni tasdiqlash; **avtorizatsiya (authz) = "nimaga ruxsating"**. Bular ikki alohida savol. Muvaffaqiyatsizlikda: authn → **401**, authz → **403** (RFC 9110). Bu eng keng tarqalgan chalkashlik.
- **To'rt usul:** **API key** (oddiy sir, foydalanuvchini bilmaydi, query'da emas) → **Basic** (base64 parol, faqat HTTPS) → **Bearer token** (eng keng tarqalgan) → **OAuth 2.0/OIDC** (uchinchi tomon delegatsiyasi). Murakkablikni ehtiyojga moslang.
- **Token: opaque vs JWT.** Opaque = bazada tekshiriladi, bekor qilish oson, lekin har so'rov bazaga boradi. **JWT** (RFC 7519: `header.payload.signature`, claims `iss/sub/aud/exp/iat`) = imzolangan, self-contained, **stateless** (bazaga bormaydi), masshtablanadi — lekin **bekor qilish qiyin**. Yechim: qisqa muddat + refresh.
- **JWT ≠ shifrlash** — payload o'qiladi, sir saqlamang. `alg:none` va zaif imzodan saqlaning (kutilgan algoritmni majburlang).
- **OAuth 2.0 (RFC 6749)** = parolni uchinchi tomonga bermasdan, cheklangan ruxsat berish. To'rt rol: resource owner, client, auth server, resource server. Tavsiya etiladigan grant'lar: **Authorization Code + PKCE** (RFC 7636 — foydalanuvchi-mijozlar uchun standart) va **Client Credentials** (servis-to-servis).
- **OAuth 2.1 (DRAFT, hali RFC emas)**: Implicit va Password (ROPC) grant'lar **olib tashlandi**, PKCE **barcha client'lar uchun majburiy**. Implicit/Password'ni o'rganmang.
- **OIDC** = OAuth 2.0 ustiga **identifikatsiya qatlami** (`id_token`); "X bilan kirish" ortida.
- **Access token (qisqa) + refresh token (uzoq):** access tugaganda refresh bilan jimgina yangilanadi (rotatsiya bilan). Tokenni mijozda xavfsiz saqlang.

---

## Mashqlar

### Oson

**1-mashq.** Quyidagi har bir holatni **autentifikatsiya (authn)** yoki **avtorizatsiya (authz)** deb belgilang:
- (a) Server "bu token haqiqiymi?" deb tekshiradi.
- (b) Server "bu foydalanuvchi shu buyurtmani o'chira oladimi?" deb tekshiradi.
- (c) Token muddati tugaganligini aniqlash.
- (d) Foydalanuvchining "admin" roli borligini tekshirish.

**2-mashq.** Quyidagi har bir stsenariy uchun eng mos autentifikatsiya **usulini** tanlang (API key / Basic / Bearer token / OAuth 2.0) va bir jumlada sababini ayting:
- (a) Ichki cron-skript ochiq ob-havo API'siga chaqiradi.
- (b) Mobil ilova foydalanuvchi nomidan ishlaydi.
- (c) Uchinchi tomon ilovasi foydalanuvchining Google Drive'iga yozmoqchi.

**3-mashq.** JWT uch qismdan iborat. Ularning nomlarini ayting va har birida nima borligini bir jumlada tushuntiring. Nega payload'ga parol yoki karta raqamini qo'yish xavfli?

### O'rta

**4-mashq.** Yangi ko'p-platformali ilova (web SPA + iOS + Android) quryapsiz, foydalanuvchilar login qiladi. Qaysi autentifikatsiya usulini va token turini (opaque/JWT) tanlaysiz? Tanlovingizni masshtab, stateless va bekor qilish nuqtai nazaridan asoslang.

**5-mashq.** Quyidagi JWT payload'ini "o'qing": har bir claim nimani anglatadi va server ularni qanday ishlatadi (token to'g'riligini tekshirishda)?
```json
{"iss": "https://auth.shop.uz", "sub": "user_7781", "aud": "https://api.shop.uz", "exp": 1735692600, "iat": 1735689000, "scope": "orders.read"}
```

**6-mashq.** Mijoz API'ga so'rov yubordi va `401 Unauthorized` oldi. Bu nima degani? Yaxshi mijoz buni qanday hal qiladi (refresh token bilan)? Va nega `403 Forbidden` boshqa narsa — unda refresh yordam beradimi?

### Qiyin

**7-mashq.** OAuth Authorization Code + PKCE oqimini to'liq, ketma-ket bosqichlarda tushuntiring: to'rt rol, `code_verifier`/`code_challenge`, kod, token almashtirish. **PKCE aniq qaysi hujumdan himoya qiladi** va u bo'lmasa nima sodir bo'lardi?

**8-mashq.** JWT'ning **bekor qilish (revocation) muammosini** tushuntiring: nega chiqarilgan JWT'ni "logout"da darhol yaroqsiz qilish qiyin? Kamida ikkita yechim bering va har birining trade-off'ini (ayniqsa statelilik bilan bog'liq) ayting. Opaque token bu muammoni qanday yengadi?

**9-mashq.** OAuth'da **Implicit grant** va **Password (ROPC) grant** nega olib tashlandi (OAuth 2.1 yo'nalishida)? Har biri qanday xavfsizlik muammosini keltirib chiqargan? Ularning o'rniga bugun nima tavsiya etiladi va nega OAuth 2.1 hali "draft" ekanini halol aytish muhim?

<details markdown="1">
<summary>Yechimlar</summary>

### 1-mashq yechimi
- (a) **Authn** — token haqiqiyligini tekshirish "kim ekaning"ni tasdiqlash.
- (b) **Authz** — "shu buyurtmani o'chira oladimi" — bu ruxsat (egalik/rol) savoli.
- (c) **Authn** — muddat token haqiqiyligining bir qismi; tugagan token autentifikatsiya bermaydi (401).
- (d) **Authz** — rol — bu ruxsat darajasi, "nimaga ruxsating bor" savoli.

### 2-mashq yechimi
- (a) **API key** — foydalanuvchi yo'q, server-to-server, ochiq ma'lumot; oddiy sir yetarli, OAuth ortiqcha.
- (b) **Bearer token** (OAuth Authorization Code + PKCE orqali olingan) — foydalanuvchili mobil ilova uchun standart; parol har so'rovda emas, qisqa-muddatli token.
- (c) **OAuth 2.0** — uchinchi tomon foydalanuvchi nomidan, *parolni bermasdan*, cheklangan (faqat Drive) ruxsat oladi — bu aynan delegatsiya muammosi.

### 3-mashq yechimi
JWT = `header.payload.signature` (base64url, nuqta bilan ajratilgan):
- **Header** — imzo algoritmi (`alg`) va token turi (`typ`).
- **Payload** — claims: `iss` (kim chiqargan), `sub` (kim haqida), `aud` (kim uchun), `exp` (qachon tugaydi), `iat` (qachon chiqarilgan).
- **Signature** — header+payload'ning sir/kalit bilan imzolangan natijasi; buzilmaslikni kafolatlaydi.

Payload'ga parol/karta qo'yish xavfli, chunki imzolangan JWT **shifrlanmagan** — payload base64url, har kim ochib o'qiy oladi. Imzo faqat *buzilmaslikni* kafolatlaydi, *maxfiylikni* emas.

### 4-mashq yechimi
**Usul:** OAuth 2.0 Authorization Code + PKCE bilan login, so'ng **Bearer token** API chaqiruvlarda. Sabab: ko'p-platformali (web/iOS/Android) foydalanuvchili ilova uchun bu standart; PKCE barcha client turlarini (jumladan SPA va mobil) himoya qiladi.

**Token turi:** **qisqa-muddatli JWT access token** + **refresh token**. Sabab:
- **Masshtab/stateless:** JWT'ni har resource server bazaga bormay, imzo orqali tekshiradi — ko'p instansli, masshtablanadigan backend uchun ideal ([05-bob](./05-rest-tamoyillari.md) stateless).
- **Bekor qilish muammosini yengillashtirish:** access token'ni qisqa qilamiz (masalan 10 daqiqa), shunda o'g'irlansa ham tez tugaydi; uzoq sessiya uchun refresh token (rotatsiya bilan). Agar to'liq, darhol bekor qilish kritik bo'lsa — refresh token'ni opaque qilib bazada saqlash mumkin (gibrid yondashuv).

### 5-mashq yechimi
- `iss: https://auth.shop.uz` — tokenni **shu auth server** chiqargan; server ishonadigan issuer ro'yxatiga mosligini tekshiradi.
- `sub: user_7781` — token **user 7781 haqida**; server buni "kim chaqiryapti" deb oladi.
- `aud: https://api.shop.uz` — token **shu API uchun**; server `aud` o'ziga mosligini tekshiradi (boshqa API uchun token'ni rad etadi).
- `exp: 1735692600` — **tugash vaqti** (Unix); server joriy vaqt bundan kichikligini tekshiradi, aks holda `401`.
- `iat: 1735689000` — **chiqarilgan vaqt**; juda eski yoki kelajakdagi tokenni rad etishda yordam beradi.
- `scope: orders.read` — ruxsat doirasi; bu **avtorizatsiya** ([12-bob](./12-avtorizatsiya.md)) bosqichida ishlatiladi ("buyurtmalarni o'qishi mumkin").

Server avval **imzoni** tekshiradi (buzilmaganmi), keyin `exp` (tugamaganmi), `aud` (menga mo'ljallanganmi), `iss` (ishonchli chiqaruvchimi) claim'larini.

### 6-mashq yechimi
**`401 Unauthorized`** = autentifikatsiya muvaffaqiyatsiz: token yo'q, noto'g'ri yoki **muddati tugagan**. Yaxshi mijoz buni ko'rib:
1. Saqlangan **refresh token** bilan auth serverga boradi va **yangi access token** oladi (`grant_type=refresh_token`).
2. Asl so'rovni yangi access token bilan **qayta yuboradi** — foydalanuvchi hech narsa sezmaydi.

(Agar refresh ham ishlamasa — refresh tugagan/bekor — foydalanuvchi qayta login qilishi kerak.)

**`403 Forbidden`** boshqa narsa: token **to'g'ri va haqiqiy** (autentifikatsiya o'tdi), lekin foydalanuvchida bu amalga **ruxsat yo'q** (scope/rol yetarsiz). Bunda **refresh yordam bermaydi** — yangi access token ham xuddi shu yetarsiz ruxsatga ega bo'ladi. Yechim ruxsat darajasida ([12-bob](./12-avtorizatsiya.md)), token darajasida emas.

### 7-mashq yechimi
**To'rt rol:** resource owner (foydalanuvchi), client (ilova), authorization server (ruxsat beruvchi), resource server (API).

**Oqim:**
1. **PKCE tayyorgarligi:** client tasodifiy `code_verifier` yasaydi, undan `code_challenge = hash(code_verifier)` hisoblaydi.
2. **Authorize:** client foydalanuvchini auth serverga yo'naltiradi, `code_challenge` ni qo'shadi.
3. **Login + rozilik:** foydalanuvchi *auth serverda* login qiladi va ruxsatni tasdiqlaydi (client parolni ko'rmaydi).
4. **Code:** auth server client'ga qisqa-muddatli `code` qaytaradi (redirect orqali).
5. **Token almashtirish:** client `code` + `code_verifier` ni auth serverga yuboradi.
6. **PKCE tekshiruvi:** auth server `hash(code_verifier) == code_challenge` ekanini tekshiradi; mos kelsa — token (access + refresh) beradi.
7. Client access token'ni `Bearer` sifatida API'ga yuboradi.

**PKCE qaysi hujumdan himoya qiladi:** **authorization code o'g'irlash** (code interception). 4-qadamdagi `code` redirect orqali ketadi va o'g'irlanishi mumkin (masalan mobil/zararli ilova yoki tarmoq orqali). PKCE bo'lmasa — o'g'ri shunchaki kodni token'ga almashtirib, kirib oladi. PKCE bilan esa o'g'irlovchida `code_verifier` yo'q (u faqat asl client'da, hech qachon yuborilmagan), shuning uchun kod foydasiz. Demak PKCE kodni *faqat uni boshlagan client* ishlata olishini kafolatlaydi.

### 8-mashq yechimi
**Muammo:** JWT **stateless** va self-contained — server uni bazaga yozmaydi, faqat imzoni tekshiradi. "Logout"da foydalanuvchini bloklamoqchimiz, lekin server hech bazaga bormaydi: imzo hali to'g'ri va `exp` hali kelmagan bo'lsa, u tokenni **qabul qilaveradi**. JWT'ni "unutib" bo'lmaydi, chunki eslab qolinmagan.

**Yechimlar:**
1. **Qisqa muddat + refresh token.** Access token'ni juda qisqa qilamiz (5–15 daqiqa). Logout/o'g'irlikda zarar tez tugaydi. *Trade-off:* darhol emas — token tugagunga qadar amal qiladi; tez-tez refresh kerak.
2. **Denylist/blocklist (`jti` bo'yicha).** Bekor qilingan token ID'larini keshda saqlab, har tekshiruvda solishtiramiz. *Trade-off:* bu **statelilikni qaytaradi** — har so'rov keshga boradi, JWT'ning bosh afzalligi (bazaga bormaslik) qisman yo'qoladi.

**Opaque token** bu muammoni tabiiy yengadi: u har so'rovda baribir bazada qidiriladi, demak bazadan o'chirsangiz — **o'sha zahoti** yaroqsiz. Bekor qilish — oddiy `DELETE`. Narxi: har so'rov bazaga/keshga boradi (stateless emas). Ko'p tizimlar gibrid ishlatadi: qisqa JWT access + opaque refresh bazada.

### 9-mashq yechimi
**Implicit grant olib tashlandi:** u access token'ni to'g'ridan-to'g'ri brauzer redirect URL'ining fragment'ida qaytarardi. Token URL'ga, brauzer tarixiga, server/proxy loglariga, `Referer` sarlavhasiga tushib, oson o'g'irlanardi. Endi o'rniga — **Authorization Code + PKCE** (token URL'da emas, xavfsiz POST orqali olinadi).

**Password (ROPC) grant olib tashlandi:** client foydalanuvchi parolini *to'g'ridan-to'g'ri qabul qilib* tokenga almashtirardi. Bu OAuth'ning butun maqsadiga zid — OAuth aynan "parolni client'ga bermaslik" uchun yaratilgan. Parolni ko'rgan client uni saqlashi, suiiste'mol qilishi mumkin va delegatsiya/scope/bekor qilish afzalliklari yo'qoladi. O'rniga — **Authorization Code + PKCE** (foydalanuvchi auth serverda login qiladi, client parolni ko'rmaydi) yoki servis uchun **Client Credentials**.

**Nega "draft" ekanini halol aytish muhim:** OAuth 2.1 hali yakuniy IETF RFC emas — u 2.0 amaliyotlarini jamlagan **draft**. Joriy yakuniy standart hamon RFC 6749 (OAuth 2.0). Buni aniq aytmaslik — o'quvchini chalg'itish: 2.1 yo'nalishi (PKCE majburiy, Implicit/Password yo'q) eng yaxshi amaliyot, lekin uni "tasdiqlangan RFC" deb ko'rsatish noto'g'ri bo'lardi. Texnik halollik — yo'nalishni tavsiya etib, maqomini to'g'ri aytish.

</details>

---

[⬅️ Oldingi: 10 — API versiyalash va evolyutsiya](./10-versiyalash.md) · [🏠 README](./README.md) · [Keyingi: 12 — Avtorizatsiya va ruxsatlar ➡️](./12-avtorizatsiya.md)
