# API dizayni — 0 dan Expertgacha

Bu kitob sizni **API (Application Programming Interface) dizayni** bo'yicha noldan — "API nima va nega muhim?" degan savoldan — ekspert darajasiga olib chiqadi. HTTP protokolini chuqur o'rganib, REST tamoyillari (resurs modellashtirish, URI dizayni, status kodlari, xato dizayni, versiyalash), so'ng API'ning **sifati va ishonchliligi** (autentifikatsiya, avtorizatsiya, OWASP xavfsizligi, rate limiting, idempotentlik, keshlash), boshqa paradigmalar (**GraphQL, gRPC, asinxron/webhook, real-time**), hujjatlash va developer experience (**OpenAPI, API gateway, contract testing**), va nihoyat API **hayot sikli, dizayn naqshlari** hamda yakuniy **kapston** — to'liq API'ni noldan loyihalashga yetadi.

> 🧭 **Til-mustaqil kitob.** Yaxshi API — bu sintaksis emas, **shartnoma** (contract). Shuning uchun bu kitob biror dasturlash tili yoki freymvorkka bog'lanmaydi: asosiy yuk **HTTP so'rov/javoblar**, **JSON** payloadlar, **OpenAPI** spetsifikatsiyasi va **diagrammalar**da. Tamoyillar Node, Python, PHP, Go, Java — har qanday tilda bir xil qo'llaniladi. Aniq freymvork implementatsiyasini [Node.js](../nodejs/README.md), [Laravel](../laravel/README.md) yoki [Django](../django/README.md) kitoblarida ko'rishingiz mumkin; bu kitob esa **dizayn qarorini** o'rgatadi.

> ⚖️ **HALOL eslatma.** Bu kitob amaliy va **standartlarga asoslangan**: HTTP semantikasi (RFC 9110), xato formati (RFC 9457 Problem Details), OpenAPI 3.1+/3.2, OAuth 2.0/2.1, OWASP API Security Top 10 (2023) kabi obro'li manbalarga tayanadi. Standartlar va versiyalar **vaqt bilan o'zgaradi** (masalan OAuth 2.1 hali IETF draft) — kitob buni har joyda halol belgilaydi va rasmiy manbaga ishora qiladi. JSON va OpenAPI namunalari **haqiqatan tekshirilgan** (valid sintaksis); dizayn qarorlari esa kontekstga bog'liq **trade-off** sifatida taqdim etiladi, "har doim shunday qil" deb emas.

> ℹ️ Bu kitob siz **HTTP va veb bilan asosiy tanishlik** (so'rov-javob, brauzer-server, JSON) borligini hisoblaydi. Agar yangi bo'lsangiz, avval [HTML & CSS](../html-css/README.md) va biror backend kitobini ([Node.js](../nodejs/README.md) / [PHP](../php/README.md) / [Python](../python/README.md)) ko'rib chiqing. Tizim darajasidagi kengroq dizayn uchun [Dasturiy arxitektura](../arxitektura/README.md) kitobiga qarang — bu kitob uning **API qatlamini** chuqurlashtiradi.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har qism oldingisiga tayanadi: HTTP asoslari → REST dizayni → sifat/xavfsizlik → paradigmalar → hujjatlash → hayot sikli.
2. Har bobdagi **so'rov/javob namunalari** va **diagrammalarni** diqqat bilan o'rganing — API dizayni ko'p jihatdan shartnoma va aloqa oqimini tasavvur qilish.
3. Har bir dizayn qarorida o'zingizdan so'rang: *bu shartnoma mijoz uchun qulaymi? o'zgarganda nima sinadi? — bu yerda nimani nimaga almashtiryapman (trade-off)?*
4. Har bobning **"Mashqlar"** bo'limini ishlang: API dizayni amaliyot va real misollar bilan o'rganiladi. Avval o'zingiz loyihalashga urinib, keyin yechimni oching.

## Talab

| Kerak | Daraja |
|---|---|
| HTTP va veb asoslari (so'rov-javob, status, JSON) | **Shart** |
| Kamida bitta backend tili bilan tanishlik | Foydali |
| Ma'lumotlar bazasi va resurs tushunchasi | Foydali |
| REST/API tajribasi | **Shart emas** — kitob noldan o'rgatadi |

---

## Mundarija

### I qism — Asoslar

| # | Bob | Mavzu |
|---|---|---|
| 01 | [API nima va nega muhim](./01-api-nima.md) | API ta'rifi, API = shartnoma va mahsulot, API-first dizayn, API turlari (web/library/OS), public/private/partner. |
| 02 | [HTTP protokoli chuqur](./02-http-chuqur.md) | So'rov/javob anatomiyasi, metodlar (GET/POST/PUT/PATCH/DELETE...), sarlavhalar, content negotiation, RFC 9110. |
| 03 | [HTTP status kodlari](./03-http-status-kodlari.md) | 1xx–5xx, qachon qaysi (2xx/3xx/4xx/5xx), keng tarqalgan xatolar, semantikani to'g'ri qo'llash. |
| 04 | [API uslublari: REST, RPC, GraphQL, gRPC](./04-api-uslublari.md) | Paradigmalar taqqoslashi (request-response/RPC/query/streaming), qachon qaysi, trade-off. |

### II qism — REST dizayni

| # | Bob | Mavzu |
|---|---|---|
| 05 | [REST tamoyillari va Richardson Maturity Model](./05-rest-tamoyillari.md) | Resurslar, statelessness, uniform interface, HATEOAS, RMM (0–3 daraja). |
| 06 | [Resurs modellashtirish va URI dizayni](./06-resurs-uri-dizayni.md) | Resurs nomi (ot, ko'plik), kolleksiya/element, ichma-ich, URI konvensiyalari, anti-naqshlar. |
| 07 | [So'rov va javob dizayni (payload)](./07-sorov-javob-payload.md) | Request/response body, JSON konvensiyalari, envelope, maydon nomlari, null/optional, data turlari. |
| 08 | [Sahifalash, filtrlash, saralash, qidiruv](./08-sahifalash-filtrlash.md) | Offset vs cursor pagination, filtrlash, saralash, qidiruv, sparse fieldsets, RFC 8288 Link. |
| 09 | [Xatolarni dizayn qilish](./09-xato-dizayni.md) | Xato modeli, Problem Details (RFC 9457), validatsiya xatolari, status mosligi, mijoz uchun foydali xabar. |
| 10 | [API versiyalash va evolyutsiya](./10-versiyalash.md) | URI/header/media-type versiyalash, breaking vs non-breaking, evolyutsion API, deprecation kirish. |

### III qism — Xavfsizlik va ishonchlilik

| # | Bob | Mavzu |
|---|---|---|
| 11 | [Autentifikatsiya](./11-autentifikatsiya.md) | API key, Basic, Bearer/JWT, OAuth 2.0/2.1, OIDC, sessiya vs token, qaysi qachon. |
| 12 | [Avtorizatsiya va ruxsatlar](./12-avtorizatsiya.md) | Scopes, RBAC/ABAC, token dizayni, eng kam imtiyoz, BOLA/BFLA dan saqlanish. |
| 13 | [API xavfsizligi (OWASP API Top 10)](./13-api-xavfsizligi.md) | OWASP API Security Top 10 (2023), input validatsiya, injection, CORS, TLS, sirlar. |
| 14 | [Rate limiting, throttling, kvotalar](./14-rate-limiting.md) | Token bucket va boshqa algoritmlar, 429, Retry-After, RateLimit sarlavhalari, kvota dizayni. |
| 15 | [Idempotentlik va parallellik](./15-idempotentlik-parallellik.md) | Idempotent metodlar, Idempotency-Key, ETag, optimistik parallellik, If-Match/If-None-Match. |
| 16 | [Keshlash (HTTP caching)](./16-keshlash.md) | Cache-Control, ETag, conditional so'rovlar, freshness/validation, CDN, RFC 9111. |

### IV qism — Boshqa paradigmalar

| # | Bob | Mavzu |
|---|---|---|
| 17 | [GraphQL dizayni](./17-graphql.md) | Schema, query/mutation/subscription, tip tizimi, N+1 muammosi, REST bilan trade-off, qachon. |
| 18 | [gRPC va Protocol Buffers](./18-grpc.md) | RPC, protobuf (proto3), 4 streaming turi, contract-first, HTTP/2, qachon gRPC. |
| 19 | [Asinxron API va webhooklar](./19-asinxron-webhook.md) | Webhook dizayni, imzo/xavfsizlik, retry, async naqshlar, event-driven, AsyncAPI. |
| 20 | [Real-time API: WebSocket va SSE](./20-realtime-websocket-sse.md) | WebSocket, Server-Sent Events, long-polling, qaysi qachon, real-time dizayn. |

### V qism — Hujjatlash, tajriba, infratuzilma

| # | Bob | Mavzu |
|---|---|---|
| 21 | [OpenAPI spetsifikatsiyasi](./21-openapi.md) | OpenAPI 3.1/3.2, design-first, schema, components, kod/hujjat generatsiyasi. |
| 22 | [Hujjatlash va Developer Experience](./22-hujjatlash-dx.md) | DX, yaxshi hujjat, misol va onboarding, SDK, changelog, developer portal. |
| 23 | [API gateway, BFF va kompozitsiya](./23-api-gateway-bff.md) | Gateway vazifalari, BFF naqshi, aggregation, edge concerns, mikroservis API kompozitsiyasi. |
| 24 | [API testlash va contract testing](./24-testlash-contract.md) | Test piramidasi API'da, contract/consumer-driven testing, mocking, schema validatsiya. |

### VI qism — Hayot sikli va kapston

| # | Bob | Mavzu |
|---|---|---|
| 25 | [Observability va ishlash](./25-observability.md) | Logging/metrics/tracing API'da, SLA/SLO/SLI, performance (payload/compression/batching). |
| 26 | [API hayot sikli va boshqaruv](./26-hayot-sikli-governance.md) | Lifecycle, governance, dizayn standartlari, deprecation/sunset (RFC 8594), migratsiya. |
| 27 | [Dizayn naqshlari va anti-naqshlari](./27-naqshlar-antinaqshlar.md) | Eng yaxshi amaliyotlar, keng tarqalgan anti-naqshlar, API dizayn checklist (jamlovchi). |
| 28 | [Kapston: to'liq API'ni noldan loyihalash](./28-kapston.md) | Talabdan to'liq dizayngacha: resurslar → OpenAPI → auth → xato → versiyalash → trade-off'lar. |

---

## Bu kitob va boshqa kitoblar

- **Tizim darajasidagi dizayn:** [Dasturiy arxitektura](../arxitektura/README.md) — API faqat bitta qatlam; bu kitob mikroservis, masshtab, CAP, kesh kabi kengroq qarorlarni qamraydi.
- **Amaliy implementatsiya:** [Node.js](../nodejs/README.md), [Laravel](../laravel/README.md), [Django](../django/README.md) — bu yerdagi dizaynni aniq freymvorkda qanday qurish.
- **Ma'lumotlar tomoni:** [Ma'lumotlar bazasi dizayni](../db-dizayni/README.md) — API ortidagi sxema va modellashtirish.
- **Xavfsizlik asboblari:** [Git & GitHub](../git-github/README.md) va [DevOps](../devops/README.md) — API'ni deploy, CI/CD va sirlarni boshqarish.

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
