# Dasturiy ta'minot arxitekturasi — 0 dan Expertgacha

Bu kitob **dasturlashni biladigan** (kamida bitta tilda kod yoza oladigan) o'quvchini dasturiy ta'minot arxitekturasi bo'yicha noldan ishonchli darajaga olib chiqadi. Kod darajasidagi dizayndan — **coupling/cohesion, SOLID, design patternlar** — boshlab, ilova arxitekturasi (**qatlamli, hexagonal, clean, DDD, event-driven/CQRS**) orqali, tizim dizayniga (**monolit vs mikroservis, API dizayni, ma'lumotlar bazasi tanlovi, masshtablash, keshlash, navbatlar, CAP, ishonchlilik, observability**) o'tib, yakuniy **real tizimni noldan loyihalash** kapstoniga yetadi.

> 🧭 **Til-mustaqil kitob.** Arxitektura — bu sintaksis emas, **qaror**. Shuning uchun bu kitob biror tilga bog'lanmaydi: asosiy yuk **diagrammalar** (C4, ketma-ketlik, komponent) va **pseudokod**da, lekin kerakli joyda ishlaydigan **TypeScript** yoki **Python** namunalari beriladi. Patternlar va printsiplar har qanday tilda qo'llaniladi.

> ⚖️ **HALOL eslatma.** Arxitekturada "yagona to'g'ri javob" yo'q — har qaror **trade-off** (ayirboshlash). Bu kitob qoidalarni emas, **fikrlashni** o'rgatadi: qachon qaysi yondashuv, va nega. Kod namunalari (TypeScript/Python) **haqiqatan ishga tushirib tekshirilgan**; tizim dizayni qarorlari esa kontekstga bog'liq — kitob ularni **trade-off sifatida** taqdim etadi, "har doim shunday qil" deb emas.

> ℹ️ Bu kitob siz **kamida bitta dasturlash tilini** (funksiya, sinf/obyekt, interfeys, asosiy OOP) bilasiz deb hisoblaydi. Yangi bo'lsangiz, avval [TypeScript](../typescript/README.md), [Python](../python/README.md) yoki [PHP](../php/README.md) kitoblaridan birini o'qing. PHP'da arxitekturaning amaliy qo'llanilishini [PHP Expert](../php-expert/README.md) kitobida ham ko'rishingiz mumkin (bu kitob til-mustaqil va kengroq).

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har bir qism oldingisiga tayanadi: kod dizayni → ilova arxitekturasi → tizim dizayni.
2. Har bobdagi **diagrammani** diqqat bilan o'rganing — arxitektura ko'p jihatdan vizual fikrlash.
3. Kod namunalarini o'zingiz teribb ishga tushiring; "Mashqlar" da **o'zingiz loyihalashga** urinib ko'ring (arxitektura amaliyot bilan o'rganiladi).
4. Har bir "trade-off" da o'zingizdan so'rang: *bu yerda nimani nimaga almashtiryapman?*

## Talab

| Kerak | Daraja |
|---|---|
| Kamida bitta tilda dasturlash (funksiya, sinf, interfeys) | **Shart** |
| OOP asoslari (meros, polimorfizm, abstraksiya) | Shart |
| Ma'lumotlar bazasi asoslari (SQL, jadval, kalit) | Foydali |
| Veb/backend bilan tanishlik (HTTP, API) | Foydali |
| Git bilan tanishlik | Foydali |

---

## Mundarija

### I qism — Arxitektura asoslari

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Dasturiy arxitektura nima va nega muhim](./01-arxitektura-nima.md) | Arxitektura ta'rifi, me'mor roli, arxitektura vs dizayn, texnik qarz, nega muhim. |
| 02 | [Sifat atributlari va trade-off'lar](./02-sifat-atributlari-tradeoff.md) | "-ilities" (masshtablanuvchanlik, qo'llab-quvvatlanuvchanlik, ishonchlilik...), trade-off, "hammasi ayirboshlash". |
| 03 | [Arxitekturani hujjatlashtirish: C4, UML, ADR](./03-hujjatlash-c4-adr.md) | C4 model (Context/Container/Component/Code), UML asoslari, Architecture Decision Record (ADR). |

### II qism — Kod darajasidagi dizayn

| # | Bob | Mavzu |
|---|---|---|
| 04 | [Coupling va cohesion (bog'liqlik va jipslik)](./04-coupling-cohesion.md) | Tight/loose coupling, high/low cohesion, coupling turlari, connascence — dizaynning poydevori. |
| 05 | [SOLID printsiplari](./05-solid.md) | SRP, OCP, LSP, ISP, DIP — misol va anti-misol bilan (TS/Python). |
| 06 | [Boshqa printsiplar: DRY, KISS, YAGNI, SoC](./06-dry-kiss-yagni.md) | DRY, KISS, YAGNI, separation of concerns, Demeter qonuni, meros o'rniga kompozitsiya. |
| 07 | [Yaratuvchi patternlar (creational)](./07-creational-patterns.md) | Factory Method, Abstract Factory, Builder, Prototype, Singleton (+ anti-pattern). |
| 08 | [Strukturaviy patternlar (structural)](./08-structural-patterns.md) | Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight. |
| 09 | [Xulq-atvor patternlari (behavioral)](./09-behavioral-patterns.md) | Strategy, Observer, Command, State, Template Method, Iterator, Mediator, Chain of Responsibility. |

### III qism — Ilova arxitekturasi

| # | Bob | Mavzu |
|---|---|---|
| 10 | [Modullik, komponentlar va chegaralar](./10-modullik-komponentlar.md) | Modullik, komponentlar, paketlar, chegaralar, modulli monolit, package-by-feature. |
| 11 | [Qatlamli arxitektura (layered / n-tier)](./11-qatlamli-arxitektura.md) | Presentation/business/data qatlamlari, n-tier, sinkhole anti-pattern, qachon kerak. |
| 12 | [Hexagonal: portlar va adapterlar](./12-hexagonal-portlar-adapterlar.md) | Ports & adapters, biznes mantiqni infratuzilmadan ajratish, dependency inversion miqyosda. |
| 13 | [Onion va Clean Architecture](./13-onion-clean-architecture.md) | Onion, Clean Architecture, dependency rule, use case, entity, chegaralar. |
| 14 | [Domain-Driven Design (DDD) asoslari](./14-ddd-asoslari.md) | Ubiquitous language, bounded context, entity/VO/aggregate, domain event, strategik vs taktik. |
| 15 | [Event-driven arxitektura va CQRS](./15-event-driven-cqrs.md) | Event-driven, pub/sub, event sourcing, CQRS, eventual consistency kirish. |

### IV qism — Tizim dizayni asoslari

| # | Bob | Mavzu |
|---|---|---|
| 16 | [Monolit, modulli monolit va mikroservislar](./16-monolit-mikroservis.md) | Monolit vs mikroservis vs modulli monolit, qachon bo'lish, distributed monolit anti-pattern. |
| 17 | [Servislararo aloqa va API dizayni](./17-api-dizayni-aloqa.md) | REST, gRPC, GraphQL, sinxron vs asinxron, API gateway, BFF, versiyalash, idempotentlik. |
| 18 | [Ma'lumotlar bazasi: SQL vs NoSQL, modellashtirish](./18-malumotlar-bazasi-tanlovi.md) | Relyatsion vs document/key-value/column/graph, qachon qaysi, polyglot persistence, ACID vs BASE. |
| 19 | [Masshtablash va load balancing](./19-masshtablash-load-balancing.md) | Vertikal/gorizontal masshtab, load balancer, stateless servis, sharding, replikatsiya kirish. |
| 20 | [Keshlash strategiyalari](./20-keshlash.md) | Cache-aside, write-through/behind, CDN, Redis, kesh-invalidatsiya, stampede, TTL. |
| 21 | [Message queue va asinxron aloqa](./21-message-queue-async.md) | Navbatlar, broker (Kafka/RabbitMQ), async ishlov, backpressure, idempotentlik, outbox. |

### V qism — Ishonchli distributed tizimlar

| # | Bob | Mavzu |
|---|---|---|
| 22 | [CAP, consistency va replikatsiya](./22-cap-consistency-replikatsiya.md) | CAP teoremasi (aniq), PACELC, consistency modellari, replikatsiya, partitsiyalash, consensus kirish. |
| 23 | [Ishonchlilik: fault tolerance va resilience](./23-fault-tolerance-resilience.md) | Retry, circuit breaker, bulkhead, timeout, graceful degradation, SPOF, distributed computing fallacy'lari. |
| 24 | [Observability va operatsiya](./24-observability.md) | Logging, metrics, tracing (3 ustun), monitoring, SLA/SLO/SLI, alerting. |

### VI qism — Amaliyot va kapston

| # | Bob | Mavzu |
|---|---|---|
| 25 | [Evolyutsion arxitektura, anti-patternlar va xavfsizlik](./25-evolyutsion-antipatternlar.md) | Evolyutsion arxitektura, fitness function, anti-patternlar (big ball of mud...), Conway qonuni, security by design. |
| 26 | [Kapston: real tizimni noldan loyihalash](./26-kapston-tizim-dizayni.md) | To'liq tizim dizayni: talablar → C4 diagrammalar → ADR → komponentlar → ma'lumot modeli → masshtab rejasi → trade-off'lar. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
