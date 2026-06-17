# 15 — Prompt caching

[⬅️ Oldingi: 14 — Token, narx va limitlar](./14-token-narx-limit.md) · [🏠 README](./README.md) · [Keyingi: 16 — Xatolar, retry va ishonchlilik ➡️](./16-xatolar-retry.md)

---

> **Bu bobda:** o'tgan bobda tokenni va narxni o'rgandingiz. Endi narxni keskin tushiradigan eng kuchli dastagimizni ko'ramiz — **prompt caching** (prompt keshlash). Agar siz bir xil **katta kontekst**ni qayta-qayta yuborsangiz (katta system prompt, uzun hujjat, few-shot misollar), har safar uning to'liq narxini to'laysiz. Prompt caching o'sha o'zgarmas qismni Anthropic serverida saqlab qo'yadi — keyingi so'rovlar uni ~0.1× narxda (90% gacha arzon) va tezroq qayta ishlatadi. Biz **bitta qoidani** — prefiks moslik — chuqur tushunamiz, `cache_control` ni qanday qo'yishni, keshni `usage` orqali tekshirishni, va eng muhimi — keshni **jim** buzadigan tuzoqlarni (Date.now(), UUID, tartibsiz JSON) topib tuzatishni o'rganamiz. Yakunda "katta hujjat bilan suhbat" quramiz: hujjat bir marta keshlanadi, o'nlab savol arzon qayta ishlatadi.

> **Halollik eslatmasi:** bu bobdagi API shakllari — `cache_control: { type: "ephemeral" }` (system bloki, tool ta'rifi yoki xabar blokida), top-level `cache_control` bilan avtomatik keshlash, `ttl: "1h"`, va `msg.usage.cache_creation_input_tokens` / `cache_read_input_tokens` maydonlari — `@anthropic-ai/sdk` **0.104** va Anthropic hujjatiga muvofiq yozilgan. Keshning haqiqiy ishlashini ko'rish uchun bir xil prefiks bilan kamida ikki marta API ga so'rov yuborish kerak (kalit + tarmoq), shuning uchun quyidagi misollar to'g'ri tuzilgan, biroq raqamli natijalar sizning prompt o'lchamingizga bog'liq. Minimal keshlanadigan prefiks model'ga bog'liq (Opus 4.8 da ≈ 4096 token) — bundan kichigi **jim** keshlanmaydi (xato bermaydi, shunchaki ishlamaydi).

---

## Nega kerak? — "hujjatni qadab qo'yish"

Tasavvur qiling, sizda 30 sahifalik mahsulot qo'llanmasi bor va foydalanuvchilar shu qo'llanma bo'yicha kuniga yuzlab savol berishadi. Har bir savolda siz Claude'ga butun qo'llanmani (aytaylik, 20 000 token) qaytadan yuborasiz. 20 000 token har safar — har savolda to'liq **input** narxi. Savol bir jumla bo'lsa ham, narxning 99% i o'sha o'zgarmas qo'llanmaga ketadi. Bu isrof.

Mana shu yerda yechim — **prompt caching**. *Caching* (keshlash) — bu hisoblangan natijani saqlab qo'yib, keyin uni qaytadan hisoblamasdan ishlatish. Prompt caching'da Claude promptingizning katta, **o'zgarmas oldingi qismini** (prefiksini) server tomonida saqlab qo'yadi. Keyingi so'rovlar o'sha qismni qaytadan "o'qimaydi" — keshdan oladi. Natija: keshlangan qism ~0.1× narxda (90% gacha arzon) va tezroq ishlanadi.

Analogiya: katta hujjatni har savolda qaytadan **yuklash** (upload) o'rniga, uni bir marta yuklab **qadab** (pin) qo'yasiz. Endi har savol shunchaki "o'sha qadalgan hujjatga" murojaat qiladi — yuklash takrorlanmaydi.

Asosiy use case'lar:

- **Hujjat bo'yicha savol-javob** — katta hujjatni keshlab, o'nlab savol bering (bu bobning kapston ilovasi; [09 — Vision va hujjatlar](./09-vision-fayllar.md) dagi "PDF bilan suhbat"ning narx tomoni).
- **Katta system prompt'li chatbot** — har turda yuboriladigan barqaror yo'riqnomani keshlang.
- **Few-shot pipeline'lar** — bir xil misollar to'plamini keshlang.
- **Ko'p turdagi suhbat (multi-turn)** — o'sib boruvchi tarixni keshlang ([03 — Messages API](./03-messages-api.md) da ko'rganimizdek, har so'rovda butun tarix yuboriladi — keshlash uni arzonlashtiradi).

---

## Bitta qoida — prefiks moslik

Keshlash haqida faqat **bitta narsani** chuqur tushunsangiz, qolgani o'z-o'zidan kelib chiqadi:

> **Keshlash — bu PREFIKS moslik. Prefiksning istalgan joyida BIR bayt o'zgarsa, undan keyingi hamma narsa keshni yo'qotadi.**

Kesh kaliti — promptning breakpoint'gacha bo'lgan **aniq baytlari**dan hosil bo'ladi. N-pozitsiyadagi bitta bayt farq qilsa, N va undan keyingi barcha breakpoint'lar uchun kesh bekor bo'ladi.

Buni to'g'ri ishlatish uchun **render tartibini** bilish shart. So'rov shu tartibda quriladi:

```
tools  →  system  →  messages
```

Demak: **BARQAROR** (o'zgarmas) narsani oldinga qo'ying, **O'ZGARUVCHAN** narsani oxiriga. Muzlatilgan system prompt, qotirilgan hujjat — boshida. Foydalanuvchining har safar o'zgaradigan savoli, timestamp'lar — oxirida, breakpoint'dan keyin.

![Prefiks kesh: so'rov tartibi tools, keyin system (katta barqaror hujjat), keyin messages. cache_control breakpoint barqaror qismdan keyin qo'yiladi. Birinchi chaqiruv keshni yozadi (1.25x narx), keyingi chaqiruvlar keshni o'qiydi (0.1x), faqat yangi savol uchun to'liq narx](rasmlar/ai15-prefix-cache.svg)

Mana shu rasm butun bobni o'zida jamlaydi: barqaror prefiks oldinda, breakpoint o'rtada, o'zgaruvchan savol oxirida. Birinchi chaqiruv keshni **yozadi**, qolganlar **o'qiydi**.

---

## API: `cache_control` ni qanday qo'yamiz

Keshlashni yoqish uchun siz biror content blokiga `cache_control: { type: "ephemeral" }` qo'shasiz. *ephemeral* — "vaqtinchalik" degani: kesh standart holatda 5 daqiqa yashaydi (har o'qishda muddat yangilanadi).

Eng keng tarqalgan holat — katta hujjatni `system` ichida bir blok sifatida keshlash:

```js
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // ANTHROPIC_API_KEY .env dan (02-bob)

const katta_hujjat = "..."; // 20 000+ token: qo'llanma, kodbaza, kitob bobi...

const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: katta_hujjat,
      cache_control: { type: "ephemeral" }, // <- shu blok va undan oldingisi keshlanadi
    },
  ],
  messages: [
    { role: "user", content: "Hujjatning asosiy fikrlarini sana." }, // <- o'zgaruvchan, keshsiz
  ],
});
```

E'tibor bering: `system` endi **satr emas, bloklar massivi** — chunki bizga `cache_control` ni aniq bir blokga qo'yish kerak. Hujjat — keshlanadi; oxirdagi savol — yo'q.

### Yana soddaroq: top-level `cache_control` (avto-keshlash)

Agar breakpointni qo'lda qaerga qo'yishni o'ylab o'tirmoqchi bo'lmasangiz, `messages.create()` ga **top-level** `cache_control` bering — SDK oxirgi keshlanadigan blokni avtomatik keshlaydi:

```js
const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  cache_control: { type: "ephemeral" }, // <- oxirgi keshlanadigan blok avto-keshlanadi
  system: katta_hujjat, // bu yerda oddiy satr ham bo'ladi
  messages: [{ role: "user", content: "Asosiy fikrlarni sana." }],
});
```

Ikki muhim chegara:

- **Eng ko'pi 4 ta breakpoint** bitta so'rovda.
- Uzunroq saqlash uchun `ttl: "1h"` (1 soat): `cache_control: { type: "ephemeral", ttl: "1h" }`. Buning narxi yuqoriroq (pastda "Iqtisod" qismida ko'ramiz).

### Bir hujjat — uch savol, arzon

Endi haqiqiy foydani ko'rsataylik: hujjatni bir marta keshlab, unga uch xil savol beramiz. Birinchi savol keshni yozadi; qolganlari keshdan o'qiydi.

```js
const katta_hujjat = "..."; // 20 000+ token barqaror kontekst

// Hujjat har so'rovda BIR XIL — shuning uchun keshlanadi.
// Faqat savol o'zgaradi — u keshsiz, har safar to'liq narxda.
async function sora(savol) {
  const msg = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    system: [
      { type: "text", text: katta_hujjat, cache_control: { type: "ephemeral" } },
    ],
    messages: [{ role: "user", content: savol }],
  });
  // keshni tekshiramiz (pastda batafsil)
  console.log("yozildi:", msg.usage.cache_creation_input_tokens,
              "o'qildi:", msg.usage.cache_read_input_tokens);
  return msg.content[0].text;
}

console.log(await sora("Qaytarish siyosati qanday?")); // 1: keshni YOZADI
console.log(await sora("Yetkazib berish necha kun?")); // 2: keshdan O'QIYDI
console.log(await sora("Kafolat muddati qancha?"));     // 3: keshdan O'QIYDI
```

Birinchi `sora()` da `cache_creation_input_tokens` katta son bo'ladi (hujjat keshga yozildi). Keyingilarida `cache_read_input_tokens` katta bo'ladi (hujjat keshdan o'qildi, ~0.1× narx), `cache_creation` esa 0 — chunki qayta yozish kerak emas edi.

---

## Kesh ishladimi? — `usage` orqali tekshirish

Keshlashni qo'shdingiz, lekin u **haqiqatan ishlayaptimi**? Buni taxmin qilmang — `msg.usage` da uchta maydon aniq aytib beradi:

| Maydon | Ma'nosi |
|---|---|
| `cache_creation_input_tokens` | Shu so'rovda keshga **yozilgan** token (siz ~1.25× yozish narxini to'ladingiz) |
| `cache_read_input_tokens` | Shu so'rovda keshdan **o'qilgan** token (siz ~0.1× to'ladingiz — arzon) |
| `input_tokens` | To'liq narxda ishlangan token (keshlanmagan qoldiq) |

![Keshni usage orqali tekshirish: birinchi chaqiruvda cache_creation_input_tokens noldan katta (yozildi); keyingi chaqiruvlarda cache_read_input_tokens noldan katta (arzon o'qish, ishladi); agar takror so'rovlarda cache_read 0 bo'lib qolsa, prefiksda jim keshbuzar bor degani](rasmlar/ai15-usage-tekshir.svg)

Buni har so'rovda log qiling:

```js
const msg = await client.messages.create({ /* ... yuqoridagidek ... */ });

console.log("Keshga yozildi  :", msg.usage.cache_creation_input_tokens);
console.log("Keshdan o'qildi :", msg.usage.cache_read_input_tokens);
console.log("Keshsiz (to'liq):", msg.usage.input_tokens);
```

**O'qish qoidasi:**

- **1-so'rov:** `cache_creation_input_tokens > 0` (yozildi), `cache_read_input_tokens = 0` (hali kesh yo'q edi).
- **2, 3, ... so'rov (bir xil prefiks):** `cache_read_input_tokens > 0` (o'qildi — ✅ kesh ishlayapti), `cache_creation = 0`.
- **Agar takror so'rovlarda ham `cache_read_input_tokens` 0 bo'lib qolsa** — ⚠️ prefiksda **jim keshbuzar** bor. Hech narsa keshlanmayapti.

> **Diqqat — `input_tokens` faqat keshlanmagan qoldiq.** To'liq prompt o'lchami = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. Agar ilovangiz katta kontekst yuborsa, lekin `input_tokens` kichik chiqsa — bu xato emas; qolgani keshdan kelgan. Yig'indini hisoblang, bitta maydonni emas.

---

## Jim keshbuzarlar — eng ko'p uchraydigan xato

Bu bobning eng muhim qismi. Ko'pchilik `cache_control` ni qo'yadi, lekin `cache_read_input_tokens` har safar 0 chiqadi va sababini topolmaydi. Sabab deyarli har doim bitta: **prefiksning boshida har so'rovda o'zgaradigan biror narsa bor.** U bitta bayt o'zgartiradi, shu bilan undan keyingi hamma narsa keshni yo'qotadi.

![Jim keshbuzar: prompt boshida Date.now() yoki UUID har so'rovda prefiks baytlarini o'zgartiradi va kesh promah bo'ladi (cache_read 0). Yechim: o'zgaruvchan qismni prompt oxiriga ko'chiring; barqaror prefiks o'zgarmasa kesh ishlaydi. Oldin va keyin solishtirma](rasmlar/ai15-invalidator.svg)

Eng keng tarqalgan jim keshbuzarlar:

```js
// ❌ 1) system prompt'da Date.now() / new Date()
const system = `Joriy vaqt: ${Date.now()}. Sen yordamchisan...`;
// -> har so'rovda boshqa son -> prefiks o'zgaradi -> kesh promah

// ❌ 2) UUID yoki so'rov ID si oldinda
const system = `So'rov ID: ${crypto.randomUUID()}. Sen yordamchisan...`;
// -> har so'rov noyob -> hech qachon keshlanmaydi

// ❌ 3) tartibsiz JSON.stringify (kalit tartibi har xil bo'lishi mumkin)
const system = `Sozlamalar: ${JSON.stringify(sozlamalar)}`;
// -> obyekt kalitlari tartibi farq qilsa -> baytlar farq qiladi -> kesh promah

// ❌ 4) foydalanuvchi ID si prefiks boshida
const system = `Foydalanuvchi ${userId}. Sen yordamchisan...`;
// -> har foydalanuvchi alohida prefiks -> foydalanuvchilar orasida kesh ulashilmaydi
```

Har biri prefiks baytlarini o'zgartiradi → kesh promah (cache miss).

**Qanday tuzatamiz?** Uch qoida:

1. **O'zgaruvchan baytlarni oxiriga ko'chiring** — breakpoint'dan keyingi qismga, ya'ni `messages` ichidagi oxirgi xabarga. 5-turdagi xabar undan oldingi 4 turni bekor qilmaydi.
2. **JSON kalitlarini barqaror tartibda bering** — `JSON.stringify` ni tartiblang.
3. **System promptni muzlating** — vaqt/rejim/ism kabi dinamik narsalarni system prompt'ga qo'shmang.

```js
// ✅ To'g'ri: barqaror prefiks oldinda, dinamik narsa oxirida
const BARQAROR_SYSTEM = "Sen do'kon yordamchisan. Quyidagi qoidalarga amal qil: ..."; // hech qachon o'zgarmaydi

const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: [
    { type: "text", text: BARQAROR_SYSTEM, cache_control: { type: "ephemeral" } },
  ],
  messages: [
    {
      role: "user",
      // vaqt va savol — OXIRDA, breakpoint'dan keyin. Keshni buzmaydi.
      content: `Joriy vaqt: ${new Date().toISOString()}.\nSavol: Kafolat qancha?`,
    },
  ],
});

// JSON ni barqaror tartibda bersangiz:
const barqaror_json = JSON.stringify(sozlamalar, Object.keys(sozlamalar).sort());
```

> **Yodda tuting.** Tool to'plamini va modelni suhbat o'rtasida o'zgartirmang. `tools` 0-pozitsiyada renderlanadi — bitta tool qo'shsangiz/olib tashlasangiz/tartibini o'zgartirsangiz, butun kesh bekor bo'ladi. Model almashtirsangiz ham (kesh model'ga bog'langan) — xuddi shu. "Rejim" kerak bo'lsa, tool to'plamini almashtirmang; rejimni xabar mazmuni sifatida bering.

---

## Iqtisod: qachon foyda beradi?

Keshlash **bepul emas** — yozish biroz qimmatroq. Lekin o'qish juda arzon. Raqamlar (asosiy input narxiga nisbatan):

| Amal | Narx |
|---|---|
| Kesh **o'qish** (cache read) | ~0.1× (90% arzon) |
| Kesh **yozish**, 5 daqiqa TTL | ~1.25× |
| Kesh **yozish**, 1 soat TTL (`ttl: "1h"`) | ~2× |
| Keshsiz oddiy input | 1× |

**Break-even (foyda chegarasi):** 5 daqiqalik TTL bilan ikki so'rov foyda chegarasiga yetadi — `1.25× + 0.1× = 1.35×`, keshsiz `2×` o'rniga. Ya'ni agar bir xil prefiksni **kamida 2 marta** ishlatsangiz, allaqachon yutdingiz. 1 soatlik TTL bilan kamida 3 so'rov kerak (`2× + 0.2× = 2.2×`, keshsiz `3×` o'rniga) — lekin u keshni 1 soat tirik tutadi, gaplari ko'p, lekin siyrak (bursty) trafik uchun.

**Minimal prefiks.** Eng muhimi: prefiks juda qisqa bo'lsa, **umuman keshlanmaydi** — xato bermaydi, shunchaki `cache_creation_input_tokens: 0` qaytaradi. Minimal o'lcham model'ga bog'liq:

| Model | Minimal keshlanadigan prefiks |
|---|---|
| Opus 4.8, Opus 4.7, Haiku 4.5 | ≈ 4096 token |
| Sonnet 4.6 | ≈ 2048 token |

Demak 3000 tokenli prompt Sonnet 4.6 da keshlanadi, lekin Opus 4.8 da **jim** keshlanmaydi. Agar kesh "ishlamayapti"dek tuyulsa, prefiks o'lchamini ham tekshiring.

> **Qachon keshlamaslik kerak?** Agar promptingiz **har so'rovda boshidanoq** farq qilsa (qayta ishlatiladigan barqaror prefiks yo'q), keshlash faqat yozish narxini behuda to'lashga olib keladi, o'qish esa hech qachon bo'lmaydi. Bunday holda `cache_control` ni qo'shmang.

---

## Kapston: katta hujjat bilan suhbat

Endi hammasini birlashtiramiz — kichik "hujjat bilan suhbat" ilovasi. Hujjat **bir marta** keshlanadi, foydalanuvchi xohlagancha savol beradi, va biz har savolda kesh tejovini log qilamiz.

```js
import Anthropic from "@anthropic-ai/sdk";
import fs from "node:fs";

const client = new Anthropic();

// 1) Katta hujjatni o'qiymiz (matn — kodbaza, qo'llanma, kitob...).
//    Bu BARQAROR prefiks: har so'rovda bir xil -> keshlanadi.
const hujjat = fs.readFileSync("qollanma.txt", "utf8");

const SYSTEM = "Sen quyidagi hujjat bo'yicha aniq, qisqa javob beradigan yordamchisan. "
  + "Faqat hujjatdagi ma'lumotga tayan. Bilmasang, 'hujjatda yo'q' deb ayt.";

async function sora(savol) {
  const msg = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    // BARQAROR prefiks: system yo'riqnoma + katta hujjat. Breakpoint hujjatdan keyin.
    system: [
      { type: "text", text: SYSTEM },
      { type: "text", text: hujjat, cache_control: { type: "ephemeral" } },
    ],
    // O'ZGARUVCHAN: faqat savol, oxirda. Keshni buzmaydi.
    messages: [{ role: "user", content: savol }],
  });

  const u = msg.usage;
  const tejov = u.cache_read_input_tokens > 0 ? "✅ keshdan o'qildi" : "yangi / keshsiz";
  console.log(`[${tejov}] yozildi=${u.cache_creation_input_tokens} `
    + `o'qildi=${u.cache_read_input_tokens} keshsiz=${u.input_tokens}`);
  return msg.content[0].text;
}

// Foydalanuvchi ketma-ket savol beradi — hujjat faqat 1-savolda keshga yoziladi.
console.log(await sora("Qaytarish siyosati qanday?")); // keshni yozadi
console.log(await sora("Yetkazib berish necha kun?")); // keshdan o'qiydi (arzon)
console.log(await sora("Kafolat muddati qancha?"));     // keshdan o'qiydi (arzon)
console.log(await sora("To'lov usullari qaysilar?"));   // keshdan o'qiydi (arzon)
```

Birinchi savol katta hujjatni keshga yozadi (`cache_creation` katta). Qolgan uch savol o'sha keshni o'qiydi (`cache_read` katta, narx ~0.1×). Agar hujjat 20 000 token bo'lsa, 4 savoldan keyin siz uni 1.25× + 3×0.1× = ~1.55× narxda ishlatdingiz — keshsiz 4× o'rniga. Bu ~60% tejov, faqat to'rt savolda.

E'tibor bering: `SYSTEM` yo'riqnoma ham, `hujjat` ham barqaror, ikkalasi ham breakpoint'dan oldin. Faqat `savol` o'zgaradi va u `messages` ichida, oxirda.

---

## Tuzoqlar va ehtiyotkorlik

| Muammo | Sabab | Yechim |
|---|---|---|
| `cache_read_input_tokens` doim 0 | Prefiksda jim keshbuzar (Date.now, UUID, ID, tartibsiz JSON) | O'zgaruvchanni oxiriga ko'chiring, JSON ni tartiblang, system'ni muzlating |
| `cache_creation_input_tokens` ham 0 | Prefiks minimal'dan qisqa (Opus 4.8 da < 4096 token) | Prefiks o'lchamini oshiring yoki keshlashdan voz keching |
| Kesh kutilmaganda buzildi | Tool to'plami yoki model suhbat o'rtasida o'zgardi | Tool va modelni barqaror saqlang; "rejim"ni xabar mazmuni qiling |
| Faqat yozish bor, o'qish yo'q | Har so'rov noyob prefiks; qayta ishlatiladigan prefiks yo'q | Bu holatda keshlash foydasiz — `cache_control` ni olib tashlang |
| Breakpoint butun promptdan keyin qo'yilgan | Har so'rov alohida kesh yozadi, o'qish yo'q | Breakpointni **barqaror** qism oxiriga qo'ying, o'zgaruvchandan oldin |
| 5+ breakpoint qo'yildi | Eng ko'pi 4 ta breakpoint | 4 ta bilan cheklang |
| Kesh tez "o'lib" qolyapti | 5 daqiqalik TTL trafik tanaffusidan qisqa | `ttl: "1h"` ishlating yoki keshni qayta-isiting |

> **Diqqat — narxni o'lchang, taxmin qilmang.** Keshlash foydasini ko'rish uchun haqiqiy `usage` raqamlarini log qiling va bir necha so'rovda kuzating. "Keshlash qo'shdim, demak arzon bo'ldi" — bu xato xulosa: agar `cache_read_input_tokens` 0 bo'lsa, siz aslida 1.25× to'lab, hech narsa tejamayapsiz. Token narxini hisoblash [14 — Token, narx va limitlar](./14-token-narx-limit.md) bobida; ishonchlilik va xatolar — keyingi [16 — Xatolar, retry va ishonchlilik](./16-xatolar-retry.md) bobida.

---

## Mashqlar

Quyidagi mashqlarning ko'pi haqiqiy `ANTHROPIC_API_KEY` va tarmoq talab qiladi — chunki keshni faqat bir necha so'rovdan keyin `usage` orqali ko'rish mumkin. `client` — `new Anthropic()` (02-bob).

### Oson

1. **Birinchi keshlash.** Kamida ~5000 tokenli katta matnni `system` ichida `cache_control: { type: "ephemeral" }` bilan yuboring, bir savol bering. `msg.usage.cache_creation_input_tokens` noldan katta ekanini ko'ring (kesh yozildi).
2. **Top-level avto-keshlash.** Xuddi shu matnni `system` oddiy satr sifatida + top-level `cache_control: { type: "ephemeral" }` bilan yuboring. Natija 1-mashqdagidek bo'lganini tekshiring.
3. **O'qishni ko'rish.** 1-mashqdagi so'rovni **ikki marta** (bir xil prefiks bilan) yuboring. Ikkinchisida `cache_read_input_tokens` noldan katta ekanini ko'ring.

### O'rta

4. **Jim keshbuzarni topish.** `system` prompt boshiga `${Date.now()}` qo'shing va ikki marta yuboring. `cache_read_input_tokens` 0 bo'lib qolganini ko'ring. Keyin `Date.now()` ni `messages` dagi oxirgi xabarga ko'chiring — endi `cache_read` noldan katta bo'lishini tasdiqlang.
5. **JSON tartibini barqarorlashtirish.** Sozlamalar obyektini `JSON.stringify(obj)` bilan system'ga qo'shib ikki marta yuboring (orada obyekt kalitlari tartibini o'zgartiring). Kesh buzilishini ko'ring, so'ng `JSON.stringify(obj, Object.keys(obj).sort())` bilan tuzating.
6. **Break-even hisobi.** 20 000 tokenli prefiksni 5 savolda ishlatsangiz, keshli va keshsiz narxni `usage` raqamlari asosida solishtiring (yozish ~1.25×, o'qish ~0.1×, keshsiz 1×). Necha foiz tejadingiz?

### Qiyin

7. **Hujjat bilan suhbat.** Kapstondagi ilovani quring: katta matnni bir marta keshlang, unga 4 ta turli savol bering. Har savolda kesh holatini (`yozildi` / `o'qildi`) log qiling. Faqat 1-savol keshni yozganini ko'rsating.
8. **Minimal prefiks chegarasi.** Atayin ~1000 tokenli kichik prefiksni Opus 4.8 da `cache_control` bilan yuboring. `cache_creation_input_tokens` 0 bo'lib qolishini (jim keshlanmaslik) ko'ring. Keyin prefiksni ~5000 tokenga oshirib, kesh ishga tushishini tasdiqlang.
9. **Foydalanuvchilar orasida ulashish.** Bir xil katta system promptni **ikki xil** foydalanuvchi savoli bilan yuboring (savol — `messages` da, oxirda; foydalanuvchi ID si prefiksda EMAS). Ikkinchi so'rovda `cache_read` noldan katta ekanini — ya'ni prefiks foydalanuvchilar orasida ulashilganini — ko'ring.

<details markdown="1">
<summary>Yechimlar</summary>

> Yechimlar `ANTHROPIC_API_KEY` (.env) talab qiladi. `client` — `new Anthropic()` (02-bob). Katta matnni o'zingiznikiga moslang (kamida ~5000 token, Opus 4.8 uchun yaxshisi ~5000+).

### 1-mashq yechimi

```js
const matn = "..."; // ~5000+ token barqaror matn
const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 256,
  system: [
    { type: "text", text: matn, cache_control: { type: "ephemeral" } },
  ],
  messages: [{ role: "user", content: "Bu matn nima haqida? Bir jumlada ayt." }],
});
console.log("yozildi:", msg.usage.cache_creation_input_tokens); // > 0 bo'lishi kerak
```

Birinchi so'rovda kesh **yoziladi**, shuning uchun `cache_creation_input_tokens` noldan katta. `cache_read` esa hali 0 (kesh endigina paydo bo'ldi).

### 2-mashq yechimi

```js
const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 256,
  cache_control: { type: "ephemeral" }, // oxirgi keshlanadigan blokni avto-keshlaydi
  system: matn, // oddiy satr ham bo'ladi
  messages: [{ role: "user", content: "Bu matn nima haqida?" }],
});
console.log("yozildi:", msg.usage.cache_creation_input_tokens);
```

Top-level `cache_control` qo'lda blok ajratmasdan oxirgi keshlanadigan blokni keshlaydi. Natija 1-mashqdagidek: `cache_creation` noldan katta.

### 3-mashq yechimi

```js
async function bir_marta() {
  return client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 256,
    system: [{ type: "text", text: matn, cache_control: { type: "ephemeral" } }],
    messages: [{ role: "user", content: "Bu matn nima haqida?" }],
  });
}

const a = await bir_marta();
console.log("1:", a.usage.cache_creation_input_tokens, a.usage.cache_read_input_tokens);
const b = await bir_marta(); // BIR XIL prefiks
console.log("2:", b.usage.cache_creation_input_tokens, b.usage.cache_read_input_tokens);
// 1: katta, 0   (yozildi)
// 2: 0, katta   (o'qildi — kesh ishladi!)
```

Ikkinchi so'rovda prefiks bir xil bo'lgani uchun `cache_read_input_tokens` noldan katta — kesh o'qildi. Bu keshlash haqiqatan ishlayotganining isboti.

### 4-mashq yechimi

```js
// ❌ Jim keshbuzar: Date.now() prefiks BOSHIDA
async function buzuq() {
  return client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 256,
    system: [
      // har so'rovda boshqa son -> prefiks o'zgaradi -> kesh promah
      { type: "text", text: `Vaqt: ${Date.now()}\n${matn}`, cache_control: { type: "ephemeral" } },
    ],
    messages: [{ role: "user", content: "Bu nima haqida?" }],
  });
}
console.log((await buzuq()).usage.cache_read_input_tokens); // 0
console.log((await buzuq()).usage.cache_read_input_tokens); // 0 — hech qachon o'qilmaydi

// ✅ Tuzatilgan: vaqt OXIRGA, messages ichiga ko'chdi
async function togri() {
  return client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 256,
    system: [{ type: "text", text: matn, cache_control: { type: "ephemeral" } }], // barqaror
    messages: [{ role: "user", content: `Vaqt: ${Date.now()}\nBu nima haqida?` }], // o'zgaruvchan, oxirda
  });
}
await togri(); // yozadi
console.log((await togri()).usage.cache_read_input_tokens); // > 0 — endi o'qiladi
```

`Date.now()` prefiks boshida bo'lganda har so'rov noyob bo'ladi — kesh hech qachon o'qilmaydi. Uni breakpoint'dan keyingi `messages` ga ko'chirsangiz, prefiks barqarorlashadi va kesh ishlaydi.

### 5-mashq yechimi

```js
const sozlamalar = { til: "uz", rejim: "qisqa", daraja: 2 };

// ❌ Tartibsiz: kalitlar tartibi farq qilsa, baytlar farq qiladi
const buzuq = `Sozlamalar: ${JSON.stringify(sozlamalar)}\n${matn}`;

// ✅ Barqaror: kalitlar har doim bir xil tartibda
const togri = `Sozlamalar: ${JSON.stringify(sozlamalar, Object.keys(sozlamalar).sort())}\n${matn}`;

// `togri` ni ikki marta yuborsangiz, ikkinchisida cache_read > 0.
const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 256,
  system: [{ type: "text", text: togri, cache_control: { type: "ephemeral" } }],
  messages: [{ role: "user", content: "Davom et." }],
});
```

`JSON.stringify` ni `Object.keys(...).sort()` bilan tartiblang — shunda kalitlar tartibi qanday bo'lishidan qat'i nazar, chiqqan satr har safar bir xil baytlar bo'ladi va prefiks barqaror qoladi.

### 6-mashq yechimi

```js
const matn = "..."; // ~20 000 token
const savollar = ["Q1?", "Q2?", "Q3?", "Q4?", "Q5?"];

let yozish = 0, oqish = 0, keshsiz = 0;
for (const s of savollar) {
  const msg = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 256,
    system: [{ type: "text", text: matn, cache_control: { type: "ephemeral" } }],
    messages: [{ role: "user", content: s }],
  });
  yozish  += msg.usage.cache_creation_input_tokens;
  oqish   += msg.usage.cache_read_input_tokens;
  keshsiz += msg.usage.input_tokens;
}

// Taxminiy narx birligi (input narxiga nisbatan koeffitsiyent):
const keshli   = yozish * 1.25 + oqish * 0.1 + keshsiz * 1;
const keshsizN = (yozish + oqish + keshsiz) * 1; // hammasi to'liq narxda bo'lsa edi
console.log("Keshli:", keshli, "Keshsiz:", keshsizN);
console.log("Tejov:", (100 * (1 - keshli / keshsizN)).toFixed(1), "%");
```

5 savolda hujjat 1 marta yoziladi (~1.25×) va 4 marta o'qiladi (4×0.1×). Katta prefiks uchun tejov 60% dan oshadi. Yig'indiga `input_tokens` (savollar) ham kiradi — ular keshlanmaydi.

### 7-mashq yechimi

```js
import fs from "node:fs";
const hujjat = fs.readFileSync("qollanma.txt", "utf8");
const SYSTEM = "Sen hujjat bo'yicha javob beradigan yordamchisan. Faqat hujjatga tayan.";

async function sora(savol) {
  const msg = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 512,
    system: [
      { type: "text", text: SYSTEM },
      { type: "text", text: hujjat, cache_control: { type: "ephemeral" } }, // barqaror prefiks oxiri
    ],
    messages: [{ role: "user", content: savol }], // o'zgaruvchan
  });
  const u = msg.usage;
  console.log(u.cache_read_input_tokens > 0 ? "✅ keshdan o'qildi" : "🟡 yangi/yozildi",
              `(yozildi=${u.cache_creation_input_tokens}, o'qildi=${u.cache_read_input_tokens})`);
  return msg.content[0].text;
}

await sora("Qaytarish siyosati?"); // 🟡 yozildi
await sora("Yetkazish muddati?");  // ✅ o'qildi
await sora("Kafolat?");            // ✅ o'qildi
await sora("To'lov usullari?");    // ✅ o'qildi
```

Faqat birinchi savol keshni yozadi (`cache_creation` katta). Qolgan uchtasi o'qiydi. Bu "hujjat bilan suhbat"ning narx poydevori: bir marta yukla/keshla, ko'p marta arzon so'ra.

### 8-mashq yechimi

```js
const kichik = "..."; // ~1000 token (Opus 4.8 minimal 4096 dan kichik)
const m1 = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 128,
  system: [{ type: "text", text: kichik, cache_control: { type: "ephemeral" } }],
  messages: [{ role: "user", content: "Salom" }],
});
console.log("kichik prefiks yozildi:", m1.usage.cache_creation_input_tokens); // 0 — jim keshlanmadi!

const katta = "..."; // ~5000 token (4096 dan katta)
const m2 = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 128,
  system: [{ type: "text", text: katta, cache_control: { type: "ephemeral" } }],
  messages: [{ role: "user", content: "Salom" }],
});
console.log("katta prefiks yozildi:", m2.usage.cache_creation_input_tokens); // > 0 — ishladi
```

Opus 4.8 da minimal keshlanadigan prefiks ≈ 4096 token. Undan kichigi xato bermaydi, lekin `cache_creation_input_tokens` 0 qaytaradi — kesh jim ishlamaydi. Prefiksni oshirsangiz, kesh ishga tushadi.

### 9-mashq yechimi

```js
const SYSTEM = "..."; // ~5000+ token barqaror system prompt (foydalanuvchi ID si YO'Q)

async function sora(savol) {
  return client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 256,
    system: [{ type: "text", text: SYSTEM, cache_control: { type: "ephemeral" } }],
    // foydalanuvchi ID si va savol — messages ichida, oxirda
    messages: [{ role: "user", content: savol }],
  });
}

const u1 = await sora("Foydalanuvchi A: narxlar qanday?"); // yozadi
const u2 = await sora("Foydalanuvchi B: ish vaqti qachon?"); // o'qiydi — boshqa savol, BIR XIL prefiks
console.log(u1.usage.cache_creation_input_tokens); // > 0
console.log(u2.usage.cache_read_input_tokens);     // > 0 — prefiks ulashildi!
```

System prompt barqaror va foydalanuvchiga bog'liq emas — shuning uchun u har xil foydalanuvchi so'rovlari orasida **ulashiladi**. Agar foydalanuvchi ID sini prefiks boshiga qo'yganingizda, har foydalanuvchi alohida kesh yozardi va bu ulashish yo'qolardi. Foydalanuvchiga oid narsani har doim `messages` ga, oxirga qo'ying.

</details>

---

> **Keyingi qadam.** Endi siz narxni keskin tushiradigan eng kuchli dastagni bilasiz: bir xil katta prefiksni qayta-qayta yuborsangiz, uni keshlang. Bitta qoidani yodda tuting — **keshlash prefiks moslik**: barqaror narsa oldinda, o'zgaruvchan narsa (vaqt, savol, ID) oxirda. `cache_control: { type: "ephemeral" }` ni katta barqaror blokga qo'ying, `msg.usage.cache_read_input_tokens` orqali ishlayotganini tekshiring, va jim keshbuzarlardan (Date.now, UUID, tartibsiz JSON) saqlaning. Keyingi bobda ilovangizni **ishonchli** qilamiz: API xatolari, qayta urinish (retry), eksponensial kechikish va `429`/`529` kabi holatlarni qanday to'g'ri boshqarishni o'rganamiz.

---

[⬅️ Oldingi: 14 — Token, narx va limitlar](./14-token-narx-limit.md) · [🏠 README](./README.md) · [Keyingi: 16 — Xatolar, retry va ishonchlilik ➡️](./16-xatolar-retry.md)
