# 24 — Batch API va optimizatsiya

[⬅️ Oldingi: 23 — Observability va evals](./23-observability-evals.md) · [🏠 README](./README.md) · [Keyingi: 25 — Deploy: serverless va edge ➡️](./25-deploy.md)

---

> **Bu bobda:** sizda **ko'p** so'rov bor, lekin ularning birortasi ham "darhol javob ber" demaydi — 10 000 ta sharhni tasniflash, butun datasetga xulosa/embedding generatsiya qilish, tungi ishlov. Mana shunday ish uchun **Message Batches API** bor: hammasini fonda **asinxron** ishlaydi va buning evaziga **narxning yarmini** (50% off) oladi. Avval *nega* batch — jonli chaqiruvdan farqi nimada, qachon to'g'ri, qachon noto'g'ri — keyin uni JavaScript'da qanday ishlatish: `create` → `custom_id` → `processing_status` ni poll qilish → natijalarni o'qib chiqish (har element xatosini alohida). So'ng kitob bo'ylab tarqalgan **barcha** narx/kechikish dastaklarini bitta to'plamga jamlaymiz — qaysi qachon, qaysi qaysi bobda — va ularni bitta bulk pipeline'da **birlashtirib** ~10× tejovni ko'ramiz. Yakunda: 1000 ta sharhni Batch + Haiku bilan, yarim narxda tasniflaydigan klassifikator + sample pipeline'ga qo'llangan "optimizatsiya nazorat ro'yxati".

> **Halollik eslatmasi:** bu bobdagi API shakllari — `client.messages.batches.create({ requests: [...] })`, `requests` ichidagi `custom_id` va `params`, `batches.retrieve(id)` qaytaradigan `processing_status` (`"ended"` bo'lguncha poll), `batches.results(id)` async-iterator va undagi `result.custom_id` / `result.result.type` (`"succeeded"` / `"errored"` / ...) / `result.result.message` — `@anthropic-ai/sdk` **0.104** va Anthropic hujjatiga muvofiq yozilgan. Cheklovlar: bitta batchda **100 000 gacha** so'rov yoki **256 MB**, natijalar **29 kun** saqlanadi, odatda **1 soat** ichida (maks 24 soat) tayyor. Narx ~50% — lekin aniq raqamlar va break-even sizning hajmingizga bog'liq, shuning uchun har doim haqiqiy `usage` bilan o'lchang (14/23-bob).

---

## Nega kerak? — "darhol kerak emas" ishning yarim narxi

Tasavvur qiling, sizda 10 000 ta mahsulot sharhi bor va har birini "ijobiy / salbiy / neytral" deb tasniflashingiz kerak. Buni hisobot uchun **bugun kechqurun** qilsangiz kifoya — hech kim ekran oldida javob kutib turgani yo'q. Agar siz buni 10 000 ta alohida jonli `messages.create()` chaqiruvi bilan qilsangiz, ikki narsani to'lasiz: **to'liq narx** va **rate limit bilan kurash** (16-bob). Holbuki ishning o'zi shoshilinch emas.

Mana shu yerda **Message Batches API** keladi. *Batch* (to'plam, partiya) — bu ko'p so'rovni bitta yumaloqqa yig'ib, Anthropic'ga "buni fonda, navbatda ishlab, tayyor bo'lganda ber" deyish. Buning evaziga siz **narxning 50% ini** (yarmini) to'laysiz. Almashinuv aniq: javob **darhol emas** — odatda 1 soat ichida (kafolatli yuqori chegara 24 soat). Demak batch fon/bulk ish uchun mukammal, lekin jonli chat uchun **noto'g'ri** — u yerda foydalanuvchi kutib turadi.

Analogiya: jonli chaqiruv — bu taksi. Darhol keladi, lekin har safar to'liq haq to'laysiz. Batch — bu avtobus. Ketishini biroz kutasiz, lekin chiptasi yarim narx. Yo'lovchilaringiz ko'p va shoshilmasa — avtobus aqlli tanlov.

Batch qachon **to'g'ri** (kechikishga sezgir EMAS, ko'p so'rov):

- **Bulk tasniflash** — minglab sharh/tiket/xabarni teglash (bu bobning kapstoni).
- **Dataset bo'yicha generatsiya** — har bir hujjatga xulosa, tarjima yoki qayta yozish.
- **Tungi/rejali ishlov** — har kuni yangi ma'lumotni qayta hisoblash.
- **Eval'larni ishga tushirish** — yuzlab test holatini bir batchda baholash ([23 — Observability va evals](./23-observability-evals.md)).

Batch qachon **noto'g'ri** (javob darhol kerak):

- Jonli chatbot, foydalanuvchi yozib kutadi — bu yerda **streaming** (04-bob) kerak, batch emas.
- Tugmaga bosgandan keyingi darhol javob, real-vaqt vositalar.

![Batch API oqimi: N so'rovni custom_id bilan create qiladi, asinxron fonda 50% narxda ishlanadi (1 soatgacha), processing_status poll qilinadi, ended bo'lganda natijalar custom_id bo'yicha moslab o'qiladi. Pastda batch (50% narx, asinxron) va N ta jonli chaqiruv (to'liq narx, darhol) solishtiriladi](rasmlar/ai24-batch-oqim.svg)

---

## Batch'ni JavaScript'da ishlatish

Batch oqimi to'rt qadamdan iborat: **yarat** → **poll qil** → **tugadi** → **natijalarni o'qib chiq**. Har birini ko'rib chiqamiz.

### 1) Batchni yaratish — `custom_id` muhim

Har bir so'rov bitta obyekt: `custom_id` (siz beradigan noyob nom) va `params` (xuddi `messages.create()` ga beradigan narsangiz — `model`, `max_tokens`, `messages`, hatto `tools`, `system`, caching). `custom_id` — eng muhim qism: natijalar **tartibsiz** qaytishi mumkin, shuning uchun har natijani qaysi so'rovga tegishli ekanini aynan `custom_id` orqali topasiz.

```js
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // ANTHROPIC_API_KEY .env dan (02-bob)

const sharhlar = [
  "Mahsulot zo'r, tez yetkazishdi!",
  "Sifati past, pulim afsus.",
  "Yaxshi, lekin qadoq buzilgan edi.",
  // ... 1000 ta sharh
];

const batch = await client.messages.batches.create({
  requests: sharhlar.map((sharh, i) => ({
    custom_id: `sharh-${i}`, // <- natijani shu so'rovga moslash uchun NOYOB id
    params: {
      model: "claude-haiku-4-5", // oddiy ish -> arzon model (14-bob)
      max_tokens: 16,            // javob qisqa -> kichik max_tokens (arzon)
      messages: [
        {
          role: "user",
          content: `Quyidagi sharhni faqat bitta so'z bilan tasnifla: `
            + `"ijobiy", "salbiy" yoki "neytral".\n\nSharh: ${sharh}`,
        },
      ],
    },
  })),
});

console.log("Batch yaratildi:", batch.id);             // msgbatch_...
console.log("Holat:", batch.processing_status);        // "in_progress"
```

E'tibor bering: `params` ichida `model`, `max_tokens`, `messages` — bular oddiy `messages.create()` dagi bilan **bir xil**. Batch shunchaki ularni o'rab, "fonda, yarim narxda ishla" deydi. `custom_id` esa `params` dan **tashqarida** — u sizning ichki yorlig'ingiz, modelga ko'rinmaydi.

### 2) Holatni poll qilish — `processing_status`

Batch yaratilgandan keyin u darhol tayyor emas. Siz vaqti-vaqti bilan `retrieve(id)` chaqirib, `processing_status` ni tekshirasiz. U `"ended"` bo'lganda hamma so'rov ishlangan (muvaffaqiyatli yoki xato — har biri alohida).

```js
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let b;
do {
  b = await client.messages.batches.retrieve(batch.id);
  console.log("Holat:", b.processing_status,
    "| tugadi:", b.request_counts.succeeded,
    "| xato:", b.request_counts.errored);
  if (b.processing_status !== "ended") await sleep(10_000); // 10 soniyada bir tekshir
} while (b.processing_status !== "ended");

console.log("Batch tugadi! Natijalar tayyor.");
```

Bu yerda biz har 10 soniyada bir poll qilamiz. **Tez-tez poll qilmang** — batch baribir asinxron, soniyada o'nlab tekshirish foydasiz va rate limit yeydi. Real ishlab chiqarishda buni ko'pincha alohida ishchi/cron qiladi: batchni yaratasiz, `batch.id` ni bazaga yozasiz, va keyinroq (masalan, har 5 daqiqada) yagona joyda tekshirasiz. `request_counts` esa progressni ko'rsatadi — necha so'rov bitdi, nechtasi xato.

### 3 va 4) Natijalarni o'qib chiqish — `custom_id` bo'yicha moslab

`"ended"` dan keyin `batches.results(id)` async-iterator qaytaradi. Har bir natijada `custom_id` (qaysi so'rov) va `result.type` (`"succeeded"` / `"errored"` / `"canceled"` / `"expired"`) bor. **Har elementning xatosini alohida boshqaring** — batch'da bir element xato bo'lsa, qolganlari baribir muvaffaqiyatli bo'lishi mumkin.

```js
const natijalar = {}; // custom_id -> javob

for await (const r of await client.messages.batches.results(batch.id)) {
  if (r.result.type === "succeeded") {
    // r.result.message — xuddi messages.create() qaytaradigan Message
    const javob = r.result.message.content[0].text.trim();
    natijalar[r.custom_id] = javob;
  } else {
    // har element xatosi ALOHIDA — bittasi yiqilsa, batch yiqilmaydi
    console.warn(`${r.custom_id}: ${r.result.type}`,
      r.result.error?.error?.message ?? "");
    natijalar[r.custom_id] = null;
  }
}

// custom_id orqali asl tartibga qaytaramiz
sharhlar.forEach((sharh, i) => {
  console.log(`[${natijalar[`sharh-${i}`] ?? "XATO"}] ${sharh}`);
});
```

Asosiy g'oya: `for await ... of` orqali natijalarni oqim sifatida o'qiysiz (10 000 ta natijani xotiraga birdan yuklamaslik uchun), har birini `custom_id` orqali asl so'rovga bog'laysiz, va `result.type` bo'yicha muvaffaqiyat/xatoni ajratasiz. `succeeded` bo'lsa `r.result.message` — bu siz tanigan oddiy `Message` obyekti (xuddi jonli chaqiruvdagidek `content`, `usage` bilan).

---

## To'liq optimizatsiya to'plami — qaysi dastak, qachon

Batch — narxni tushiradigan dastaklardan **bittasi**. Endi kitob bo'ylab tarqalgan barcha narx va kechikish dastaklarini bitta joyga jamlaymiz, toki keyingi loyihangizda "qayerda tejasam bo'ladi?" deganda butun ro'yxat ko'z oldingizda bo'lsin.

![Optimizatsiya vositalari to'plami: chap panelda NARX dastaklari (to'g'ri model 14-bob, prompt caching 15-bob, batch 50% shu bob, kichik max_tokens, qisqa prompt va past effort 10-bob, routing 21-bob), o'ng panelda KECHIKISH dastaklari (streaming 04-bob, Promise.all parallel 21-bob, kichikroq model 14-bob, keshlash 15-bob); ba'zi dastaklar ham arzon ham tez](rasmlar/ai24-optimizatsiya-vositalari.svg)

### Narxni kamaytirish

| Dastak | Nima qiladi | Qachon | Bob |
|---|---|---|---|
| **To'g'ri model** | Oddiy ish uchun Haiku, qiyin ish uchun Opus | Vazifa oddiy bo'lsa (tasniflash, marshrutlash) | [14](./14-token-narx-limit.md) |
| **Prompt caching** | Takror prefiksni ~0.1× narxda qayta ishlatish | Bir xil katta kontekst qayta yuborilsa | [15](./15-prompt-caching.md) |
| **Batch API** | Asinxron bulk = **50%** (yarmi) | Ko'p so'rov, kechikish muhim emas | shu bob |
| **Kichik `max_tokens`** | Chiqishni cheklash — chiqish narxi qimmatroq | Javob qisqa bo'lishi kerak bo'lsa | [14](./14-token-narx-limit.md) |
| **Qisqa/aniq prompt** | Kamroq kirish tokeni | Prompt shishib ketgan bo'lsa | har doim |
| **Past `effort`** | Kamroq fikrlash (thinking) tokeni | Vazifa chuqur fikrlashni talab qilmasa | 10-bob |
| **Routing arzon→qimmat** | Avval Haiku, faqat kerak bo'lsa Opus | Aralash qiyinlikdagi oqim | [21](./21-multi-agent.md) |

### Kechikishni (latency) kamaytirish

| Dastak | Nima qiladi | Qachon | Bob |
|---|---|---|---|
| **Streaming** | Token-token oqim — *his etilgan* tezlik | Foydalanuvchi javobni ko'rib turadi | 04-bob |
| **`Promise.all` parallel** | Mustaqil so'rovlarni bir vaqtda | Bir nechta so'rov bir-biriga bog'liq emas | [21](./21-multi-agent.md) |
| **Kichikroq model** | Haiku Opus'dan tez javob qaytaradi | Tezlik va narx ikkalasi muhim | [14](./14-token-narx-limit.md) |
| **Keshlash (kesh hit)** | Kesh natijasi qaytsa, API ga umuman bormaysiz | Bir xil so'rov takrorlansa | [15](./15-prompt-caching.md) |

> **Diqqat — ba'zi dastaklar ikkala tomonni ham yutadi.** Kichikroq model ham arzon, ham tez. Prompt caching ham narxni tushiradi (o'qish ~0.1×), ham ishlanish vaqtini qisqartiradi (model keshlangan prefiksni qayta o'qimaydi). Shu sababli bu ikkitasi — eng "tekin" optimizatsiyalar: ko'pincha xarajat almashinuvisiz ikkala foydani ham beradi.

> **Eslatma — batch parallel EMAS.** [21 — Multi-agent](./21-multi-agent.md) dagi `Promise.all` ham "ko'p so'rovni birga" qiladi, lekin maqsadi boshqa: u **kechikishni** kamaytiradi (javoblar darhol, parallel keladi), narxni emas. Batch esa **narxni** yarmiga tushiradi, lekin kechikishni oshiradi (asinxron). Ko'p so'rov darhol kerak bo'lsa — `Promise.all`. Ko'p so'rov shoshilmasa va arzon kerak bo'lsa — batch.

---

## Dastaklarni birlashtirish — tejov ustma-ust

Eng katta kuch — dastaklarni **birlashtirganda** kelib chiqadi. Ular jamlanmaydi, **ko'paytma** bo'lib ishlaydi: har biri qolgan narxni yana bo'ladi.

Misol: 10 000 ta sharhni tasniflash uchun bulk pipeline quramiz va uchta dastakni ustma-ust qo'yamiz:

1. **To'g'ri model** — bu oddiy ish, Opus shart emas. Haiku Opus'dan ~5× arzon → narx ~25% ga tushadi.
2. **Keshlangan system prompt** — har sharhda bir xil yo'riqnoma (tasniflash qoidalari, misollar) takrorlanadi. Uni keshlasak, o'sha umumiy prefiks ~0.1× bo'ladi → narx yana tushadi.
3. **Batch API** — hammasi shoshilinch emas, bulk. Batch qolgan narxni yana **yarmiga** bo'ladi (50%).

![Dastaklarni birlashtirish: sodda Opus-per-call-jonli 100% taglik; to'g'ri model (Haiku) qo'shilganda ~25%; keshlangan system prompt qo'shilganda ~14%; Batch API qo'shilganda ~7% — yakuniy narx taglikning ~10 dan 1 qismi. Dastaklar ko'paytma bo'lib ishlaydi, jamlama emas](rasmlar/ai24-birlashtirilgan.svg)

Yakuniy natija: sodda "Opus, jonli, har so'rov alohida" yondashuviga nisbatan taxminan **10× arzonroq**. Va bu taxminiy raqamlar — sizning aniq tejouingiz prompt o'lchamiga, model tanloviga va keshlanadigan prefiks ulushiga bog'liq. **Shuning uchun har doim o'lchang.**

> **Halollik — raqamlar taxminiy.** Yuqoridagi ~25% / ~14% / ~7% — dastaklar qanday **ko'payishini** ko'rsatish uchun illustratsiya, kafolatli aniq qiymat emas. Haqiqiy tejov sizning ish yukingizga bog'liq: agar keshlanadigan prefiks kichik bo'lsa, caching foydasi kam; agar sharhlar juda qisqa bo'lsa, model tanlovi foydasi katta. Doim haqiqiy `usage` bilan tasdiqlang.

### Kapston: bulk klassifikator (Batch + Haiku + kesh) + nazorat ro'yxati

Hammasini birlashtiramiz — 1000 ta sharhni Batch API bilan, Haiku'da, umumiy yo'riqnomani keshlab tasniflaydigan pipeline. So'ng pastda uni "optimizatsiya nazorat ro'yxati" bilan tekshiramiz.

```js
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Har sharhda BIR XIL yo'riqnoma — keshlash uchun nomzod (15-bob).
const YORIQNOMA =
  "Sen sharhlarni tasniflovchisan. Sharhni faqat bitta so'z bilan tasnifla: "
  + "'ijobiy', 'salbiy' yoki 'neytral'. Boshqa hech narsa yozma.\n"
  + "Misollar:\n"
  + "Sharh: 'Zo'r mahsulot!' -> ijobiy\n"
  + "Sharh: 'Umuman yoqmadi.' -> salbiy\n"
  + "Sharh: 'O'rtacha, shunchaki.' -> neytral\n"; // ... real holatda uzunroq

async function bulkTasnifla(sharhlar) {
  // 1) Batch yaratamiz: Haiku + kichik max_tokens + keshlangan system
  const batch = await client.messages.batches.create({
    requests: sharhlar.map((sharh, i) => ({
      custom_id: `sharh-${i}`,
      params: {
        model: "claude-haiku-4-5",          // arzon model (14-bob)
        max_tokens: 16,                       // qisqa javob (14-bob)
        system: [
          { type: "text", text: YORIQNOMA,
            cache_control: { type: "ephemeral" } }, // keshlangan prefiks (15-bob)
        ],
        messages: [{ role: "user", content: `Sharh: ${sharh}` }],
      },
    })),
  });
  console.log("Batch:", batch.id, "| so'rovlar:", sharhlar.length);

  // 2) Tugaguncha poll qilamiz
  let b;
  do {
    b = await client.messages.batches.retrieve(batch.id);
    if (b.processing_status !== "ended") await sleep(10_000);
  } while (b.processing_status !== "ended");

  // 3) Natijalarni custom_id bo'yicha yig'amiz + xatolarni alohida hisoblaymiz
  const tasnif = {};
  let xato = 0, kesh_oqildi = 0;
  for await (const r of await client.messages.batches.results(batch.id)) {
    if (r.result.type === "succeeded") {
      tasnif[r.custom_id] = r.result.message.content[0].text.trim().toLowerCase();
      kesh_oqildi += r.result.message.usage.cache_read_input_tokens ?? 0;
    } else {
      xato++;
      tasnif[r.custom_id] = null;
    }
  }

  console.log(`Tugadi. Xato: ${xato}. Keshdan o'qilgan token: ${kesh_oqildi}`);
  return sharhlar.map((_, i) => tasnif[`sharh-${i}`]);
}

const sharhlar = [/* ... 1000 ta sharh ... */];
const teglar = await bulkTasnifla(sharhlar);
console.log(teglar.slice(0, 5)); // ["ijobiy", "salbiy", "neytral", ...]
```

Bu pipeline uchta dastakni birga ishlatadi: **Batch** (50% narx), **Haiku** (arzon model), **kesh** (umumiy yo'riqnoma ~0.1×). Va `cache_read_input_tokens` ni o'qib, keshning haqiqatan ishlayotganini tekshiramiz (15-bob).

**Optimizatsiya nazorat ro'yxati** — har bulk/AI pipeline uchun bosib o'ting:

- [ ] **Vazifa darhol javob talab qiladimi?** Yo'q → Batch API (50%). Ha → batch emas.
- [ ] **Eng oddiy model yetadimi?** Tasniflash/marshrutlash → Haiku (14-bob).
- [ ] **Bir xil katta kontekst takrorlanadimi?** Ha → prompt caching (15-bob), `cache_read` ni tekshir.
- [ ] **`max_tokens` haqiqiy ehtiyojga moslangmi?** Qisqa javob → kichik limit.
- [ ] **Prompt shishib ketmaganmi?** Keraksiz so'zlarni olib tashla; `effort` ni pasaytir (10-bob).
- [ ] **So'rovlar bir-biriga bog'liq emasmi?** (jonli oqimda) → `Promise.all` parallel (21-bob).
- [ ] **Har optimizatsiyani `cost()`/`usage` bilan O'LCHADINGMI?** (14/23-bob) — taxmin qilma.

---

## O'lchamasdan optimallashtirmang

Bu butun bobning eng muhim qoidasi. Har bir optimizatsiya bir taxminga asoslanadi ("Haiku yetadi", "kesh ishlayapti", "batch arzonroq"). Taxmin **noto'g'ri** bo'lishi mumkin: ehtimol Haiku sifat berolmay, siz uni Opus bilan ikki marta chaqirib, qimmatroq qilib qo'ygansiz; ehtimol keshingiz har so'rovda buzilib, faqat yozish narxini behuda to'layapsiz (15-bob). Buni **bilishning** yagona yo'li — o'lchash.

[14 — Token, narx va limitlar](./14-token-narx-limit.md) dagi `cost(usage, model)` va [23 — Observability va evals](./23-observability-evals.md) dagi logging'ni ishlating: optimizatsiyadan **oldin** va **keyin** narx/kechikishni yozib oling va solishtiring. Raqam tushdimi — yutdingiz. Tushmadi yoki sifat yomonlashdi — orqaga qayting.

```js
import { cost } from "./narx.js"; // 14-bobdagi cost() funksiyasi

// Optimizatsiyadan OLDIN: Opus, jonli, keshsiz
const oldin = await client.messages.create({
  model: "claude-opus-4-8", max_tokens: 16,
  messages: [{ role: "user", content: `Sharhni tasnifla: ${sharh}` }],
});
console.log("Oldin (1 so'rov):", cost(oldin.usage, "claude-opus-4-8").toFixed(6), "$");

// KEYIN: Haiku, keshlangan system — bir so'rovning narxini solishtiring
const keyin = await client.messages.create({
  model: "claude-haiku-4-5", max_tokens: 16,
  system: [{ type: "text", text: YORIQNOMA, cache_control: { type: "ephemeral" } }],
  messages: [{ role: "user", content: `Sharh: ${sharh}` }],
});
console.log("Keyin (1 so'rov):", cost(keyin.usage, "claude-haiku-4-5").toFixed(6), "$");
// + batchda yana 50% — lekin uni batch usage'ida ko'rasiz
```

### Qachon umuman optimallashtirmaslik kerak

**Erta optimizatsiya** (premature optimization) — bu o'zining tuzog'i. Agar siz kuniga atigi 50 ta so'rov yuborsangiz, batch sozlash, caching breakpoint'lari va router ustida bosh qotirish — vaqt isrofi. Shunchaki Opus'ni jonli ishlating va ishingizni davom ettiring; oydagi farq bir piyola qahvadan kam bo'lishi mumkin.

Optimizatsiya **og'rigan joyda** ma'noli bo'ladi: hisob-faktura sezilarli, yoki kechikish foydalanuvchini bezovta qiladi. Avval **o'lchang** (qayerga pul/vaqt ketyapti?), keyin eng katta ulushni oling. "Hammasini optimallashtir" emas, "eng katta xarajatni optimallashtir".

> **Diqqat — sifatni qurbon qilmang.** Eng arzon model va eng past effort doim "yaxshi" emas. Agar Haiku tasnifni xato qilsa va siz noto'g'ri hisobot bersangiz, bu sizga arzon modeldan ko'ra qimmatga tushadi. Har optimizatsiyadan keyin **sifatni** ham tekshiring — eval'lar bilan (23-bob). Narx va sifat orasidagi muvozanat — sizniki, modelniki emas.

---

## Mashqlar

Quyidagi mashqlarning ko'pi haqiqiy `ANTHROPIC_API_KEY` va tarmoq talab qiladi (batch jonli ishlanadi). `client` — `new Anthropic()` (02-bob). Katta hajm uchun avval kichik (5–10 ta) so'rovli batch bilan sinab ko'ring.

### Oson

1. **Birinchi batch.** 5 ta qisqa so'rovni (masalan, "1+1 nechchi?", "Parij qaysi davlatda?" ...) `batches.create()` bilan yuboring, har biriga `custom_id: "q-0"`, `"q-1"`, ... bering. `batch.id` va `batch.processing_status` ni log qiling.
2. **Poll qilish.** 1-mashqdagi batchni `retrieve(id)` bilan 10 soniyada bir tekshiring, `processing_status` `"ended"` bo'lguncha. Har tekshirishda `request_counts` ni log qiling.
3. **Natijalarni o'qish.** `batches.results(id)` orqali natijalarni oqim sifatida o'qing. Har birida `r.custom_id` va `r.result.type` ni log qiling; `succeeded` bo'lsa javob matnini ko'rsating.

### O'rta

4. **Custom_id moslash.** 1-mashqdagi natijalarni `custom_id` orqali asl savollar bilan **moslab** chiqaring (`natijalar[custom_id]` lug'ati quring, keyin asl tartibda chop eting). Natijalar tartibsiz kelishi mumkinligini eslab, faqat `custom_id` ga tayaning.
5. **Element xatosini boshqarish.** Bitta so'rovni atayin buzuq qiling (masalan, `max_tokens: 0` yoki noto'g'ri model), batchni yuboring. Natijalarda o'sha element `result.type !== "succeeded"` ekanini, lekin **qolganlari** `"succeeded"` bo'lganini ko'ring. Xato elementni alohida hisoblang.
6. **Batch vs jonli narx.** 10 ta bir xil so'rovni (a) 10 ta alohida jonli `messages.create()` va (b) bitta batch bilan yuboring. `cost()` (14-bob) bilan jonli to'liq narxni hisoblang; batch ~50% ekanini eslatib, qancha tejaganingizni taxmin qiling.

### Qiyin

7. **Bulk klassifikator.** Kapstondagi pipeline'ni quring: 50 ta sharhni Haiku + keshlangan yo'riqnoma + batch bilan tasniflang. `cache_read_input_tokens` (natija `usage`'ida) noldan katta ekanini — ya'ni kesh ishlaganini — tasdiqlang.
8. **Optimizatsiya nazorat ro'yxati.** O'zingizning biror AI pipeline'ingizni (yoki kitobdagi biror kapstonni) oling va bobdagi nazorat ro'yxatining har bandidan o'tkazing. Har band uchun: qo'llasa bo'ladimi? Qo'llasangiz, `cost()`/`usage` bilan narx tushganini o'lchang.
9. **Birlashtirilgan tejovni o'lchash.** Bir vazifani to'rt usulda baholang va `cost()`/`usage` bilan haqiqiy narxni solishtiring: (a) Opus jonli keshsiz, (b) Haiku jonli keshsiz, (c) Haiku jonli keshli, (d) Haiku batch keshli. Har qadamda narx necha barobar tushganini jadval qiling. Diagrammadagi ~10× ga yaqinlashdimi?

<details markdown="1">
<summary>Yechimlar</summary>

> Yechimlar `ANTHROPIC_API_KEY` (.env) talab qiladi. `client` — `new Anthropic()` (02-bob), `cost()` — 14-bobdagi funksiya. `sleep = (ms) => new Promise(r => setTimeout(r, ms))`.

### 1-mashq yechimi

```js
const savollar = ["1+1 nechchi?", "Parij qaysi davlatda?", "Suvning formulasi?",
                  "Yer Quyoshni necha kunda aylanadi?", "Eng katta okean?"];
const batch = await client.messages.batches.create({
  requests: savollar.map((s, i) => ({
    custom_id: `q-${i}`,
    params: {
      model: "claude-haiku-4-5",
      max_tokens: 64,
      messages: [{ role: "user", content: s }],
    },
  })),
});
console.log("Batch id:", batch.id);
console.log("Holat:", batch.processing_status); // "in_progress"
```

`custom_id` har so'rov uchun noyob (`q-0` ... `q-4`). `batch.id` ni saqlang — keyingi qadamlar shunga tayanadi.

### 2-mashq yechimi

```js
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let b;
do {
  b = await client.messages.batches.retrieve(batch.id);
  console.log(b.processing_status, b.request_counts); // { processing, succeeded, errored, ... }
  if (b.processing_status !== "ended") await sleep(10_000);
} while (b.processing_status !== "ended");
console.log("Tayyor!");
```

`request_counts` progressni ko'rsatadi: nechtasi ishlanmoqda, nechtasi tugadi, nechtasi xato. `"ended"` — hammasi (xato bo'lsa ham) yakunlangani.

### 3-mashq yechimi

```js
for await (const r of await client.messages.batches.results(batch.id)) {
  console.log(r.custom_id, "->", r.result.type);
  if (r.result.type === "succeeded") {
    console.log("  javob:", r.result.message.content[0].text.trim());
  }
}
```

`results()` async-iterator — `for await ... of` bilan o'qiladi. `r.result.message` — oddiy `Message` obyekti (jonli chaqiruvdagidek).

### 4-mashq yechimi

```js
const natijalar = {};
for await (const r of await client.messages.batches.results(batch.id)) {
  natijalar[r.custom_id] =
    r.result.type === "succeeded" ? r.result.message.content[0].text.trim() : null;
}
// Asl tartibda, custom_id orqali moslab
savollar.forEach((s, i) => {
  console.log(`Q: ${s}\nA: ${natijalar[`q-${i}`] ?? "XATO"}\n`);
});
```

Natijalar **tartibsiz** kelishi mumkin, shuning uchun massiv indeksiga emas, `custom_id` ga (`q-${i}`) tayanamiz. Lug'at quramiz, keyin asl tartibda chop etamiz.

### 5-mashq yechimi

```js
const batch = await client.messages.batches.create({
  requests: [
    { custom_id: "ok-0", params: {
        model: "claude-haiku-4-5", max_tokens: 32,
        messages: [{ role: "user", content: "Salom de" }] } },
    { custom_id: "buzuq-1", params: {
        model: "yoq-bunday-model", max_tokens: 32, // <- atayin xato model
        messages: [{ role: "user", content: "Salom de" }] } },
  ],
});
// ... poll qilib "ended" kut ...
let xato = 0, ok = 0;
for await (const r of await client.messages.batches.results(batch.id)) {
  if (r.result.type === "succeeded") { ok++; }
  else { xato++; console.warn(r.custom_id, r.result.type, r.result.error?.error?.message); }
}
console.log("OK:", ok, "Xato:", xato); // OK: 1, Xato: 1
```

Muhim saboq: batch'da bir element yiqilsa, **butun batch yiqilmaydi**. Har element `result.type` ni alohida tekshiring va xatolarni alohida hisoblang/qayta yuboring.

### 6-mashq yechimi

```js
import { cost } from "./narx.js";
const sorov = { model: "claude-haiku-4-5", max_tokens: 32,
  messages: [{ role: "user", content: "Bu sharh ijobiymi? 'Zo'r mahsulot'" }] };

// (a) 10 ta jonli chaqiruv — to'liq narx
let jonliNarx = 0;
for (let i = 0; i < 10; i++) {
  const m = await client.messages.create(sorov);
  jonliNarx += cost(m.usage, "claude-haiku-4-5");
}
console.log("Jonli (10x, to'liq narx):", jonliNarx.toFixed(6), "$");

// (b) Batch — xuddi shu 10 so'rov, ~50%
const batch = await client.messages.batches.create({
  requests: Array.from({ length: 10 }, (_, i) => ({ custom_id: `r-${i}`, params: sorov })),
});
// ... poll + results ...
console.log("Batch ~", (jonliNarx * 0.5).toFixed(6), "$ atrofida (50% off)");
```

Batch narxni ~yarmiga tushiradi. Aniq raqamni batch natijalarining `usage` yig'indisidan oling — taxmin emas, o'lchang.

### 7-mashq yechimi

```js
const YORIQNOMA = "Sharhni faqat bitta so'z bilan tasnifla: 'ijobiy', 'salbiy', 'neytral'. "
  + "/* ... uzun, keshlanadigan yo'riqnoma + misollar ... */";
const sharhlar = [/* 50 ta sharh */];

const batch = await client.messages.batches.create({
  requests: sharhlar.map((sh, i) => ({
    custom_id: `sh-${i}`,
    params: {
      model: "claude-haiku-4-5", max_tokens: 16,
      system: [{ type: "text", text: YORIQNOMA, cache_control: { type: "ephemeral" } }],
      messages: [{ role: "user", content: `Sharh: ${sh}` }],
    },
  })),
});
// ... poll ...
let kesh = 0;
for await (const r of await client.messages.batches.results(batch.id)) {
  if (r.result.type === "succeeded") kesh += r.result.message.usage.cache_read_input_tokens ?? 0;
}
console.log("Keshdan o'qilgan token (jami):", kesh); // > 0 bo'lsa kesh ishladi
```

Birinchi so'rov yo'riqnomani keshga yozadi, qolganlari o'qiydi — shuning uchun jami `cache_read_input_tokens` noldan katta. Eslatma: keshlash ishlashi uchun yo'riqnoma minimal prefiks o'lchamidan katta bo'lishi kerak (Haiku 4.5 da ≈ 4096 token, 15-bob), aks holda **jim** keshlanmaydi.

### 8-mashq yechimi

Nazorat ro'yxatini pipeline'ga qo'llash — masalan, 18-bobdagi RAG javob generatori uchun:

```
[x] Darhol kerakmi? — RAG javobi foydalanuvchiga jonli -> batch EMAS, streaming (04-bob).
[x] Eng oddiy model? — javob sifatli bo'lishi kerak -> Opus qoldiramiz, lekin retrieval tasnifini Haiku ga (router, 21-bob).
[x] Takror kontekst? — system prompt + retrieval shabloni har so'rovda bir xil -> caching (15-bob).
[x] max_tokens? — javob 1-2 abzats -> max_tokens: 512 ga cheklaymiz.
[x] Prompt shishganmi? — retrieval'da top-3 -> top-8 emas, kamroq kontekst.
[x] Parallel? — bir foydalanuvchi bir savol -> parallel kerak emas; lekin embeddings'ni Promise.all bilan.
[x] O'lchadingmi? — har so'rovda cost(usage) log -> caching narxni 40% tushirdi (o'lchandi).
```

Asosiy g'oya: har bandni "ha/yo'q" bilan ko'rib chiqing va qo'llaganingizni **o'lchang** — taxmin emas.

### 9-mashq yechimi

```js
import { cost } from "./narx.js";
const sh = "Mahsulot zo'r, lekin yetkazish sekin edi.";
const Y = "Sharhni bir so'z bilan tasnifla: ijobiy/salbiy/neytral. /* ... uzun yo'riqnoma ... */";

// (a) Opus jonli, keshsiz
const a = await client.messages.create({ model: "claude-opus-4-8", max_tokens: 16,
  messages: [{ role: "user", content: `${Y}\nSharh: ${sh}` }] });
// (b) Haiku jonli, keshsiz
const b = await client.messages.create({ model: "claude-haiku-4-5", max_tokens: 16,
  messages: [{ role: "user", content: `${Y}\nSharh: ${sh}` }] });
// (c) Haiku jonli, keshli (ikki marta yuborib o'qishni ko'ring)
const c = await client.messages.create({ model: "claude-haiku-4-5", max_tokens: 16,
  system: [{ type: "text", text: Y, cache_control: { type: "ephemeral" } }],
  messages: [{ role: "user", content: `Sharh: ${sh}` }] });
// (d) Haiku batch keshli -> batch usage'idan narx, keyin ~50% qo'llang

console.log("a Opus jonli :", cost(a.usage, "claude-opus-4-8").toFixed(6));
console.log("b Haiku jonli:", cost(b.usage, "claude-haiku-4-5").toFixed(6));
console.log("c Haiku kesh :", cost(c.usage, "claude-haiku-4-5").toFixed(6), "(2-so'rovda kesh o'qiladi)");
// d: c ning narxini batchda ~0.5x deb hisoblang -> jadval qiling
```

Har qadamda narx tushadi: Opus→Haiku (~5×), keshli (umumiy prefiks ~0.1×), batch (yana ~2×). Birlashtirilganda diagrammadagi ~10× ga yaqinlashadi — lekin aniq qiymat sizning prompt o'lchamingiz va keshlanadigan ulushga bog'liq, shuning uchun **o'lchang**, taxmin qilmang.

</details>

---

> **Keyingi qadam.** Endi sizda to'liq optimizatsiya to'plami bor. Eng muhim ikki saboqni yodda tuting: (1) **Batch API** kechikishga sezgir bo'lmagan ko'p so'rov uchun narxni yarmiga tushiradi — `custom_id` bilan yuborib, `processing_status` ni poll qilib, natijalarni `custom_id` orqali moslab o'qiysiz; (2) dastaklar (to'g'ri model, caching, batch, kichik `max_tokens`, past effort, routing, streaming, parallel) **birlashganda** ko'paytma bo'lib ishlaydi — bulk pipeline'da ~10× tejovga olib keladi. Va oltin qoida: **o'lchamasdan optimallashtirmang** — har o'zgarishni `cost()`/`usage` (14/23-bob) bilan tasdiqlang, va sifatni ham (23-bob) tekshiring. Keyingi bobda ilovangizni dunyoga chiqaramiz: serverless va edge muhitlarida AI ilovasini **deploy** qilishni — sovuq start, environment maxfiylari, streaming'ni edge'da uzatishni — o'rganamiz.

---

[⬅️ Oldingi: 23 — Observability va evals](./23-observability-evals.md) · [🏠 README](./README.md) · [Keyingi: 25 — Deploy: serverless va edge ➡️](./25-deploy.md)
