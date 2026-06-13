# Ma'lumotlar bazasi dizayni — 0 dan ekspertgacha

Bu kitob ma'lumotlar bazasini **to'g'ri loyihalashni** o'rgatadi: talab tahlilidan ER-modellashtirish, normalizatsiya va fizik dizayndan tortib NoSQL, analitik ombor va taqsimlangan masshtablashgacha. Asosiy vosita — **PostgreSQL 18**, lekin tamoyillar har qanday bazaga tegishli; kerakli joyda MySQL farqlari ham izohlanadi.

> 🎯 **Bu kitob nimasi bilan SQL kitobidan farq qiladi?** [SQL va MySQL kitobi](../sql/README.md) bazadan *qanday so'rov yozishni* (SELECT, JOIN, GROUP BY) o'rgatadi. Bu kitob esa undan keyingi savolga javob beradi: **qanday sxema loyihalash kerak?** Qaysi jadval, qaysi kalit, qancha normalizatsiya, qaysi indeks, qaysi modellashtirish naqshi. Sintaksis emas — **qaror**.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan (jami 72 ta): ER-model, kardinallik, normalizatsiya qadamlari, indeks tuzilishi, star-schema, partition xaritasi va boshqalar ko'z bilan ko'rib o'rganiladi.

> 💻 **Hamma kod ishlatiladi.** Kitobdagi har bir DDL va so'rov PostgreSQL 18.4 da haqiqatan ishga tushirilib tekshirilgan. Siz ham har misolni o'zingiz tering — dizayn o'qib emas, **loyihalab** o'rganiladi.

---

## Talab

| Kerak | Daraja |
|---|---|
| SQL asoslari (SELECT, JOIN, CREATE) | **Shart** — avval [SQL va MySQL kitobini](../sql/README.md) o'qing |
| PostgreSQL 16+ (18 tavsiya etiladi) | Shart — misollarni sinash uchun |
| Oldingi dizayn tajribasi | Shart emas |

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing — har qism oldingisiga tayanadi (modellashtirish → normalizatsiya → fizik dizayn → ilg'or mavzular).
2. Har bobdagi DDL'ni o'z PostgreSQL'ingizda **terib ko'ring** — sxemani his qilish uchun.
3. Bob oxiridagi **dizayn masalalarini** o'zingiz yeching: berilgan talabni sxemaga aylantiring, anti-naqshni toping va tuzating.
4. Diagrammalarga e'tibor bering — ular dizayn qarorini tezroq singdiradi.

---

## I qism — Asoslar va konseptual modellashtirish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Ma'lumotlar bazasi dizayni nima va nega muhim](./01-dizayn-nima.md) | Yomon sxemaning narxi (anomaliya, sekinlik, bug), dizaynning uch bosqichi (konseptual → logik → fizik) va yaxshi sxema belgilari. |
| 02 | [Talab tahlili va domen modellashtirish](./02-talab-tahlili.md) | Biznes talabidan model elementlarini ajratish (ot → entity, sifat → atribut, fe'l → bog'lanish), biznes qoidalari va ko'lam. |
| 03 | [ER-diagramma: entity, atribut, bog'lanish](./03-er-diagramma.md) | Entity, atribut turlari, Crow's foot notatsiyasi va to'liq ER-diagramma o'qish hamda chizish. |
| 04 | [Bog'lanishlar va kardinallik (1:1, 1:N, N:M)](./04-boglanish-kardinallik.md) | Kardinallik, modallik (ixtiyoriy/majburiy), N:M ni junction jadvalga aylantirish va o'z-o'ziga bog'lanish. |

## II qism — Relyatsion model va normalizatsiya

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 05 | [Relyatsion model va kalit turlari](./05-relyatsion-model.md) | Relyatsion model qoidalari, kalit iyerarxiyasi (super/candidate/primary/foreign) va NULL ning xavfi (uch qiymatli mantiq). |
| 06 | [Kalit dizayni: natural, surrogate, UUID, kompozit](./06-kalit-dizayni.md) | Natural vs surrogate trade-off, IDENTITY, UUID v4 vs v7 (`uuidv7()`), kompozit va business kalit. |
| 07 | [Normalizatsiya I: 1NF, 2NF, 3NF va anomaliyalar](./07-normalizatsiya-asoslari.md) | Funksional bog'liqlik, uchta anomaliya va jadvalni 1NF → 2NF → 3NF bo'ylab qadam-baqadam parchalash. |
| 08 | [Normalizatsiya II: BCNF, 4NF, 5NF va denormalizatsiya](./08-normalizatsiya-ilgor.md) | BCNF, ko'p qiymatli bog'liqlik (4NF), 5NF va denormalizatsiya qachon ataylab to'g'ri ekani. |
| 09 | [Logik modeldan fizik sxemaga](./09-logik-fizik-sxema.md) | ER → jadval o'tkazish qoidalari, nomlash konvensiyalari va to'liq DDL skript tuzilishi. |

## III qism — Yaxlitlik, turlar va naqshlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 10 | [To'g'ri ma'lumot turini tanlash](./10-malumot-turlari.md) | PostgreSQL boy turlari: numeric vs float (pul!), timestamptz, enum, JSONB, array, range, generated column, domain. |
| 11 | [Yaxlitlik va constraint dizayni](./11-constraint-dizayni.md) | Yaxlitlikni bazada majburlash: CHECK, UNIQUE, EXCLUDE, FK ON DELETE strategiyasi va deferrable constraint. |
| 12 | [Keng tarqalgan dizayn naqshlari](./12-dizayn-naqshlari.md) | Soft delete, audit/tarix ustunlari, status modellashtirish, slug, polimorfik bog'lanish va pul+valyuta. |
| 13 | [Anti-naqshlar: nima qilmaslik kerak](./13-anti-naqshlar.md) | Jaywalking (CSV ustun), EAV, naive tree, god-table, float'da pul, indekssiz FK — alomat → nega yomon → tuzatish. |

## IV qism — Fizik dizayn va performans

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 14 | [Indeks strategiyasi](./14-indeks-strategiyasi.md) | B-tree/GIN/BRIN/GiST qachon, kompozit ustun tartibi, qisman/ifoda/covering indeks va indeks narxi. |
| 15 | [Sxema va so'rov performansi (EXPLAIN ANALYZE)](./15-performans.md) | EXPLAIN rejasini o'qish, N+1 muammosi, materialized view va keshlangan agregat — "avval o'lcha". |
| 16 | [Tranzaksiya, izolyatsiya va parallellik dizayni](./16-tranzaksiya-parallellik.md) | ACID, izolyatsiya darajalari, MVCC, lost update, optimistik vs pessimistik qulflash va deadlock. |

## V qism — Ilg'or modellashtirish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 17 | [Daraxt va graf strukturalarini modellashtirish](./17-daraxt-graf.md) | Adjacency list, materialized path, nested set, closure table trade-off va recursive CTE bilan aylanish. |
| 18 | [Vaqtinchalik va versiyalangan ma'lumot](./18-temporal-versiya.md) | Bitemporal model, tarix jadvali, audit log, event sourcing va PG18 temporal constraint (WITHOUT OVERLAPS). |
| 19 | [Multi-tenancy dizayni va RLS](./19-multi-tenancy.md) | Ko'p-ijarachi SaaS uchun 3 strategiya va PostgreSQL Row-Level Security bilan tenant izolyatsiyasi. |

## VI qism — NoSQL, analitik va masshtab

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 20 | [NoSQL ma'lumot modellashtirish](./20-nosql-modellashtirish.md) | Document/key-value/wide-column/graph qachon, embed vs reference (MongoDB), Redis dizayn va CAP/BASE. |
| 21 | [Analitik dizayn va ma'lumotlar ombori](./21-analitik-ombor.md) | OLTP vs OLAP, dimensional modeling, star vs snowflake schema, grain va slowly changing dimensions. |
| 22 | [Partitioning, sharding va masshtablash](./22-partitioning-masshtab.md) | PostgreSQL partitioning (RANGE/LIST/HASH) + pruning, sharding strategiyalari, replication va CAP teoremasi. |
| 23 | [Migratsiya va sxema evolyutsiyasi](./23-migratsiya-evolyutsiya.md) | Versiyalangan migratsiya, zero-downtime, expand-contract naqshi va xavfsiz vs lock-oluvchi ALTER. |

## VII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 24 | [Yakuniy loyiha: tizimni 0 dan loyihalash](./24-yakuniy-loyiha.md) | Real tizimni talabdan to'liq fizik sxemagacha loyihalash: ER → normalizatsiya → DDL → indeks → partition → migratsiya + ADR. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
