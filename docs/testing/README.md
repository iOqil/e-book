# Dasturiy ta'minotni testlash — 0 dan Expertgacha

Bu kitob sizni **dasturiy ta'minotni testlash** bo'yicha mutlaqo noldan — "nega test yozamiz?"
degan savoldan — ekspert darajasiga olib chiqadi. Birinchi `assert`dan boshlab, **test piramidasi**,
**unit / integratsiya / E2E** testlar, **test dublyorlari** (mock, stub, fake, spy), **TDD**
(Red-Green-Refactor), **BDD**, ma'lumotlar bazasi va **API testlash**, **kontrakt testlar**,
**code coverage**, **property-based** va **mutation testing**, **flaky** testlar, **performance**
va **xavfsizlik** testlari, **CI/CD**, **test strategiyasi** va eski (**legacy**) kodni testlashgacha —
nihoyat real loyihani noldan test bilan qoplaydigan **kapston**ga yetadi.

> 🧭 **Til-mustaqil kitob.** Test yozish — bu sintaksis emas, **fikrlash tarzi**. Shuning uchun bu
> kitob biror tilga bog'lanmaydi: asosiy yuk **tamoyillar, diagramma va psevdokod**da. Lekin har bir
> texnika yonida **ishlaydigan Python + `pytest`** namunasi beriladi (Python o'qishga eng oson va
> psevdokodga yaqin til). G'oyalar har qanday tilda bir xil: JavaScript'da `Jest`/`Vitest`,
> PHP'da `PHPUnit`/`Pest`, Java'da `JUnit`, Go'da `testing` — atamalar va naqshlar deyarli aynan.

> ⚖️ **HALOL eslatma.** Bu kitob testlashni *yodlatmaydi*, balki **qachon, nimani va qanchalik**
> test qilishni — va eng muhimi, **nega** — o'rgatadi. "100% coverage = xatosiz kod", "test yozish
> vaqtni behuda sarflaydi", "mock'lab hammasini testlash mumkin" kabi keng tarqalgan **afsonalarni**
> ataylab buzamiz. Barcha Python namunalari **haqiqatan ishga tushirib, chiqishi tekshirilgan**.

> ℹ️ Bu kitob siz **kamida bitta tilda asosiy kod yoza olasiz** deb hisoblaydi (o'zgaruvchi, funksiya,
> shart, sikl, klass tushunchasi). Agar yangi bo'lsangiz, avval [Python](../python/README.md) yoki
> [JavaScript](../js/README.md) kitobini ko'rib chiqing. Testlash uchun maxsus matematika kerak emas.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har qism oldingisiga tayanadi: asoslar →
   unit testing → TDD → integratsiya → sifat o'lchovlari → funksional bo'lmagan testlar → jarayon va kapston.
2. Har bobdagi **diagramma** va **kod namunalarini** diqqat bilan kuzating, kodni **o'zingiz ishlatib ko'ring**.
3. Eng muhimi — **o'z loyihangizda test yozib ko'ring**. Testlash faqat amaliyot bilan o'rganiladi.
4. Har bobning **"Mashqlar"** bo'limini ishlang: avval o'zingiz urinib, keyin yechimni oching.

## Talab

| Kerak | Daraja |
|---|---|
| Kamida bitta tilda asosiy dasturlash (funksiya, shart, sikl, klass) | **Shart** |
| Python sintaksisi bilan tanishlik | Foydali (kitob namunalari Python'da) |
| Buyruq qatori (terminal) bilan ishlash | Foydali (kitob asosini o'rgatadi) |
| Avvalgi test yozish tajribasi | **Shart emas** — kitob noldan o'rgatadi |

---

## Mundarija

### I qism — Testlash asoslari

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Nega test yozamiz?](./01-nega-test-yozamiz.md) | Xatoning narxi, ishonch va regressiya, qo'lda vs avtomat testlash, test nima emas, testlash madaniyati. |
| 02 | [Birinchi testingiz: AAA va test anatomiyasi](./02-birinchi-test-aaa.md) | Test runner, assertion, Arrange-Act-Assert, birinchi `pytest` testi, test nomlash va ishga tushirish. |
| 03 | [Test turlari va test piramidasi](./03-test-turlari-piramida.md) | Unit / integratsiya / E2E, test piramidasi vs "trophy", qamrov-tezlik-narx muvozanati. |
| 04 | [Yaxshi test xossalari: FIRST va izolyatsiya](./04-yaxshi-test-xossalari.md) | FIRST tamoyillari, determinizm, mustaqillik, o'qilishi, "bitta yiqilish sababi", test smell'lari. |

### II qism — Unit testing chuqur

| # | Bob | Mavzu |
|---|---|---|
| 05 | [Assertion'lar va test holatlarini tanlash](./05-assertionlar-test-holatlari.md) | Assertion turlari, istisnolarni testlash, chegara qiymatlari, ekvivalentlik sinflari, hodisa tanlash. |
| 06 | [Test ma'lumotlari: fixture, parametrize, builder](./06-fixture-parametrize.md) | `pytest` fixture, scope, `conftest.py`, parametrlangan testlar, test data builder / object mother. |
| 07 | [Test dublyorlari I: taksonomiya](./07-test-dublyorlari-nazariya.md) | Dummy, stub, fake, spy, mock — Meszaros taksonomiyasi; har biri qachon kerak; "klassik vs london". |
| 08 | [Test dublyorlari II: amaliyot va tuzoqlar](./08-test-dublyorlari-amaliyot.md) | `unittest.mock`, `patch`, side effect, qachon mock qilmaslik, ortiqcha mock (over-mocking) tuzog'i. |
| 09 | [Vaqt, tasodif, I/O: bog'liqliklarni izolyatsiya](./09-bogliqliklarni-izolyatsiya.md) | Vaqt/tasodif/fayl/tarmoqni boshqarish, seam, testlash uchun dependency injection. |
| 10 | [Testlanadigan dizayn](./10-testlanadigan-dizayn.md) | DI, sof funksiya, humble object, portlar/adapterlar, testlash dizaynga qanday bosim beradi. |

### III qism — TDD va dizayn

| # | Bob | Mavzu |
|---|---|---|
| 11 | [TDD: Red-Green-Refactor](./11-tdd-red-green-refactor.md) | Test-driven development sikli, kichik qadamlar, "transformation priority", TDD foydasi va tanqidi. |
| 12 | [TDD amaliyotda: to'liq misol (kata)](./12-tdd-amaliyot-kata.md) | To'liq TDD kata: bosqichma-bosqich real masalani test bilan haydab yechish. |
| 13 | [Refactoring va testlar](./13-refactoring-va-testlar.md) | Test soyabonida xavfsiz refactoring, characterization test, test koddagi smell'lar, DRY vs DAMP. |
| 14 | [BDD va spetsifikatsiya](./14-bdd-spetsifikatsiya.md) | Given-When-Then, Gherkin, jonli hujjat, "specification by example", umumiy til (DDD bilan ko'prik). |

### IV qism — Integratsiya va yuqori darajadagi testlar

| # | Bob | Mavzu |
|---|---|---|
| 15 | [Integratsiya testlari](./15-integratsiya-testlari.md) | Integratsiya chegaralari, in-memory vs real, Testcontainers g'oyasi, qachon integratsiya afzal. |
| 16 | [Ma'lumotlar bazasi va tashqi servislarni testlash](./16-malumotlar-bazasi-testlash.md) | Tranzaksiya/rollback, migratsiya, seed, fixture vs factory, tashqi servislarni izolyatsiya. |
| 17 | [API va HTTP testlash](./17-api-http-testlash.md) | So'rov/javob, status kod, sxema validatsiyasi, autentifikatsiya, HTTP'ni soxtalashtirish (mock server). |
| 18 | [Kontrakt testlar](./18-kontrakt-testlar.md) | Consumer-driven contract, Pact g'oyasi, sxema/API kontrakti, mikroservislararo moslik. |
| 19 | [End-to-end va UI testlar](./19-e2e-ui-testlar.md) | E2E qachon arziydi, brauzer avtomatizatsiyasi (Playwright/Selenium g'oyasi), Page Object, barqarorlik. |

### V qism — Sifatni o'lchash va kengaytirilgan texnikalar

| # | Bob | Mavzu |
|---|---|---|
| 20 | [Code coverage: foyda va xavf](./20-code-coverage.md) | Qamrov turlari (qator/shox/yo'l), maqsadli foiz, Goodhart qonuni, coverage nimani ko'rsatmaydi. |
| 21 | [Property-based testing](./21-property-based-testing.md) | Generativ testlash, invariant, `Hypothesis`, shrinking, misol-asosli vs xossa-asosli. |
| 22 | [Mutation testing](./22-mutation-testing.md) | Mutant, mutation score, "testlaringizni testlash", `mutmut` g'oyasi, coverage'dan kuchliroq signal. |
| 23 | [Snapshot va approval testing](./23-snapshot-approval-testing.md) | Snapshot/golden master, approval test, characterization, qachon foydali va qachon xavfli. |
| 24 | [Flaky testlar va barqarorlik](./24-flaky-testlar.md) | Sabablar (async/vaqt/tartib/umumiy holat), karantin, retry, flaky'ni topish va tuzatish. |

### VI qism — Funksional bo'lmagan testlar

| # | Bob | Mavzu |
|---|---|---|
| 25 | [Performance, yuk va stress testlar](./25-performance-yuk-testlari.md) | Latency vs throughput, persentil (p95/p99), load/stress/soak, tooling g'oyasi (k6/Locust). |
| 26 | [Xavfsizlik testlash asoslari](./26-xavfsizlik-testlash.md) | SAST/DAST, OWASP, fuzzing, bog'liqliklarni skanerlash, testlarda xavfsizlik holatlari. |

### VII qism — Jarayon, strategiya va kapston

| # | Bob | Mavzu |
|---|---|---|
| 27 | [Test avtomatlashtirish va CI/CD](./27-ci-cd-avtomatlashtirish.md) | CI'da testlar, pipeline bosqichlari, tez fikr-mulohaza, parallellashtirish, test tanlash. |
| 28 | [Test strategiyasi va testing quadrants](./28-test-strategiyasi-quadrants.md) | Agile testing quadrants, risk-asosli testlash, nimani qancha testlash, ROI, test rejasi. |
| 29 | [Eski (legacy) kodni testlash](./29-legacy-kodni-testlash.md) | Seam, characterization test, "test yo'q koddan" boshlash, Michael Feathers, strangler yondashuv. |
| 30 | [Kapston: loyihani noldan test bilan qoplash](./30-kapston.md) | Hammasini birlashtirish: strategiya → unit → integratsiya → E2E → CI → coverage/mutation. |

---

## Bu kitob va boshqa kitoblar

- **Arxitektura:** [Dasturiy arxitektura](../arxitektura/README.md) — testlanadigan dizayn, portlar/adapterlar, qatlamlar.
- **Algoritmlar:** [Algoritmlar va ma'lumotlar strukturalari](../algoritmlar/README.md) — to'g'rilik isboti va test bir-birini to'ldiradi.
- **DevOps:** [DevOps & Deployment](../devops/README.md) — CI/CD pipeline'da testlarni ishga tushirish.
- **Til asoslari:** [Python](../python/README.md) — namunalardagi sintaksis yangi bo'lsa.

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
