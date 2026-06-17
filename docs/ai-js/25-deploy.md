# 25 — Deploy: serverless va edge

[⬅️ Oldingi: 24 — Batch API va optimizatsiya](./24-batch-optimizatsiya.md) · [🏠 README](./README.md) · [Keyingi: 26 — Yakuniy loyiha: to'liq AI ilova ➡️](./26-kapston-loyiha.md)

---

> **Bu bobda:** lokal mashinangizda ishlayotgan AI ilovani **real foydalanuvchilarga** chiqaramiz. Avval **nega** bu alohida mavzu ekanini his qilamiz: lokalda ishlatish bir narsa, ishlab chiqarishda (production) **ishonchli va arzon** ishlatish — butunlay boshqa narsa. Server kodingiz **qayerda** ishlaydi, kalit **qanday** xavfsiz qoladi, oqim (streaming) **ishlaydimi** va xarajat **nazoratda**mi? So'ng eng muhim arxitektura chegarasini takrorlaymiz (13- va 22-bob): klient → **sizning serveringiz** (kalit shu yerda) → Anthropic — bu chegara qaysi platformaga deploy qilsangiz ham o'zgarmaydi. Keyin deploy variantlarini ko'ramiz: **Vercel** (Next.js + AI SDK uchun eng oson yo'l), **Cloudflare Workers** (edge, global), **Node server** (uzoq agentlar uchun) va qisqacha **AWS Lambda**. Muhit o'zgaruvchilari va maxfiylar (secrets), production'da streaming va to'g'ri runtime, hamda agentning eng katta tuzog'i — **serverless funksiya vaqt chegarasi** — ni o'rganamiz. Yakunda 13-bobdagi chatbotni Vercel'ga qadam-baqadam deploy qilamiz va Express muqobilini quramiz.
>
> **Halollik eslatmasi:** Vercel, Cloudflare Workers va AWS ning aniq sozlama oynalari, funksiya vaqt chegaralari va runtime nomlari versiyadan versiyaga, reja (plan)dan rejaga o'zgaradi. Bu yerda **g'oyani va arxitekturani** o'rgating — aniq raqamlar (timeout soniyalari, runtime kalit so'zlari) uchun har doim o'sha platformaning joriy hujjatini oching. Model — `claude-opus-4-8`.

---

## 1. Nega bu bob muhim? — lokal ≠ production

Shu paytgacha biz kodni o'z mashinangizda ishlatdik: `node script.js` yoki `npm run dev`, kalit `.env` faylida, hamma narsa bitta kompyuterda. Bu o'rganish uchun ajoyib. Lekin ilovani **internetga**, real foydalanuvchilarga ochmoqchi bo'lsangiz, bir nechta yangi savol paydo bo'ladi — va ularning har birida xato qilish oson:

- **Kod qayerda ishlaydi?** Sizning noutbukingiz doim yoqiq turolmaydi. Server kerak — lekin qanday server? Doimo-yoqiq mashina? Serverless funksiya? Edge?
- **Kalit qayerda yashaydi?** Lokalda `.env` faylida. Lekin `.env` ni hech qachon git'ga qo'ymaysiz — unda production'da kalit qayerdan keladi?
- **Oqim ishlaydimi?** Lokalda streaming yaxshi ishladi. Lekin serverless yoki edge muhitda ham xuddi shunday ishlaydimi?
- **Uzoq ishlar nima bo'ladi?** Bitta chat chaqiruvi bir necha soniya. Lekin 10 qadamli agent (7-bob) yoki katta hujjatni qayta ishlash — bir necha daqiqa olishi mumkin. Serverless funksiya buni ko'taradimi?
- **Xarajat nazoratdami?** Real foydalanuvchilar real token sarflaydi. Kim biror narsani noto'g'ri ishlatib, hisobingizni puch qilib qo'ymasligini qanday ta'minlaysiz?

> **Analogiya.** Oshxonangizda mazali taom pishirdingiz — bu **lokal**. Endi uni restoran qilib ochmoqchisiz — bu **production**. Restoranda yangi savollar paydo bo'ladi: oshxona qancha mehmonni bir vaqtda ko'taradi? Buyurtma juda murakkab bo'lsa (uzoq pishadigan taom) navbatni qanday boshqarasiz? Pul qutisi (kalit) qayerda — ko'rinadigan joydami yoki seyfdami? Bu bob — sizning taomingizni restoranga, ishonchli xizmatga aylantirish haqida.

Bu bob shu savollarning **deploy** tomonini hal qiladi. Xavfsizlikning to'liq tafsiloti — [22-bobda](./22-xavfsizlik.md), ishonchlilik — [16-bobda](./16-xatolar-retry.md), kuzatuv va xarajat — 23-bobda. Bu bob ularni production muhitiga bog'laydi.

---

## 2. Arxitektura — kalit har doim serverda (deploy ham buni buzmaydi)

13-bobda biz eng muhim qoidani o'rnatgan edik, va u **deploy paytida ham aynan o'sha** bo'lib qoladi. Aslida, deploy — aynan shu chegara haqiqatan saqlanishini tekshiradigan joy.

**Qoida shu:**

> **Klient (brauzer/mobil) → sizning serveringiz → Anthropic.** Klient hech qachon Anthropic bilan to'g'ridan-to'g'ri gaplashmaydi. `ANTHROPIC_API_KEY` faqat **server tomonida** yashaydi.

Lokalda bu chegara aniq edi: kalit `.env` faylida, faqat Node jarayoni uni o'qidi. Production'da xuddi shu g'oya, lekin endi kalit **platformaning maxfiy do'koniga** (secrets store) joylashadi — Vercel/Cloudflare dashboard'idagi "Environment Variables" bo'limiga. Kod uni xuddi avvalgidek `process.env.ANTHROPIC_API_KEY` orqali o'qiydi, lekin u **git'da emas**, **klientda emas** — faqat server funksiyangiz ishga tushganda muhitga yuklanadi.

![Production deploy arxitekturasi: foydalanuvchilar (brauzer/mobil) CDN/edge orqali sizning serverless yoki edge route'ingizga ulanadi; route ANTHROPIC_API_KEY ni platforma maxfiylaridan (secrets) o'qib Anthropic'ni chaqiradi; oqimli javob xuddi shu yo'l bilan qaytadi. Kalit har doim server maxfiylarida, hech qachon klientga chiqmaydi.](rasmlar/ai25-deploy-arxitektura.svg)

Diagrammada uchta qatlam:

1. **Foydalanuvchilar** — brauzer yoki mobil ilova. Ular faqat **sizning** URL'ingiz bilan gaplashadi (`/api/chat`).
2. **Sizning deploy'ingiz** — CDN/edge tarmoq orqali kelgan so'rov sizning route'ingizga yetadi. Shu yerda `streamText(...)` ishlaydi va shu yerda kalit `process.env` orqali o'qiladi. Bu Vercel funksiyasi, Cloudflare Worker yoki Node server bo'lishi mumkin — qatlam bir xil.
3. **Anthropic** — model. U faqat sizning serveringizdan so'rov oladi, klientdan emas.

Javob (oqim) xuddi shu yo'ldan teskari qaytadi: Anthropic → sizning route → foydalanuvchi. **Qaysi platformani tanlasangiz ham, bu chegara o'zgarmaydi** — faqat o'rtadagi "sizning deploy'ingiz" qutisi turli texnologiyalarda bo'ladi. Endi shu qutining variantlarini ko'ramiz.

---

## 3. Deploy variantlari — qachon qaysi?

To'rtta asosiy variant bor. Ularni "qaysi biri yaxshi?" deb emas, "**mening ishimga qaysi biri to'g'ri keladi?**" deb tanlaysiz. Asosiy ajratuvchi savol: ishim **qisqami** (chat, bitta chaqiruv) yoki **uzoqmi** (ko'p qadamli agent, ommaviy ishlash)?

![Deploy variantlari taqqoslangan: Vercel (Next.js + AI SDK, oson, serverless/edge — chat va oddiy chaqiruv uchun), Cloudflare Workers (edge, global, tez, lekin to'liq Node API yo'q — yengil proksi/chat), Node server Render/Railway/VPS (uzoq agentlar, to'liq Node API, fon ishlari), AWS Lambda (serverless funksiya). Qachon qaysi: chat vs uzoq agent vs ommaviy.](rasmlar/ai25-platformalar.svg)

### Vercel — eng oson yo'l (Next.js + AI SDK)

Agar ilovangiz Next.js + AI SDK (11–13-bob) da bo'lsa, **Vercel** eng silliq yo'l. AI SDK aynan shu muhit uchun ishlab chiqilgan.

- **git push → avtomatik deploy.** GitHub repozitoriyangizni Vercel'ga ulaysiz; har `git push` da Vercel ilovani qayta quradi va chiqaradi.
- **Route Handler'lar avtomatik funksiyaga aylanadi.** 13-bobdagi `app/api/chat/route.js` — Vercel'da serverless (yoki edge) funksiya bo'lib ishlaydi. Siz alohida server sozlamaysiz.
- **Streaming qutidan ishlaydi.** `toUIMessageStreamResponse()` Vercel'da to'g'ri oqim qaytaradi.
- **⚠️ Funksiyaga vaqt chegarasi bor.** Bu — keyingi bo'limdagi asosiy tuzoq. Chat va bitta chaqiruv uchun yetarli; juda uzun agentlar uchun emas.

**Qachon:** chat ilovasi, bitta chaqiruv, RAG so'rovi (18-bob), strukturali chiqish — qisqa, sekundlik ishlar.

### Cloudflare Workers — edge, global

**Cloudflare Workers** — kodingizni dunyo bo'ylab, foydalanuvchiga **eng yaqin** joyda ishlatadigan **edge** platforma.

- **Global va tez.** Kod foydalanuvchiga geografik yaqin nuqtada ishlaydi — past kechikish (latency).
- **⚠️ To'liq Node API yo'q.** Edge muhit Node'ning to'liq nusxasi emas: `fs` (fayl tizimi) kabi Node-ga xos API'lar, ba'zi paketlar bo'lmasligi yoki boshqacha ishlashi mumkin. Anthropic SDK va `fetch` ga asoslangan kod odatda ishlaydi, lekin og'irroq Node kutubxonalari ishlamasligi mumkin.

**Qachon:** yengil chat yoki proksi route, global tarqalish kerak bo'lganda, og'ir Node-ga-bog'liq kod yo'q bo'lsa.

### Node server — uzoq ishlar uchun (Express/Fastify)

Agar sizga **uzoq ishlaydigan** jarayon kerak bo'lsa — ko'p qadamli agent, fon ishi, navbat (queue) ishchisi — **doimo-yoqiq Node server** kerak. Uni Render, Railway, Fly.io yoki o'z VPS'ingizda ishlatasiz.

- **Vaqt chegarasi yo'q.** Server doimo ishlab turadi — agent 5 daqiqa ishlasa ham uni hech kim majburan to'xtatmaydi.
- **To'liq Node API.** `fs`, fon vazifalari, navbat ishchilari — hammasi ishlaydi.
- **⚠️ Siz boshqarasiz.** Server doim yoqiq (va doim pul yeyadi); masshtablash, monitoring — sizning zimmangizda.

**Qachon:** uzun agent siklilari, fon ishlari, navbat ishchilari, to'liq Node API kerak bo'lganda.

### AWS Lambda — serverless (qisqacha)

**AWS Lambda** — klassik "funksiya-as-service": so'rov kelganda funksiya ishga tushadi, tugagach o'chadi. Konseptual jihatdan Vercel funksiyasiga o'xshaydi (shu jumladan **vaqt chegarasi** ham bor), lekin AWS ekotizimiga chuqurroq bog'langan. Agar infratuzilmangiz allaqachon AWS'da bo'lsa mantiqiy. Uzun ish uchun AWS'da SQS (navbat) yoki Step Functions ishlatiladi — Node server'dagi navbat g'oyasining AWS varianti.

> **Asosiy fikr.** Hammasida kalit serverda, hammasida bir xil `route` mantig'i ishlaydi. Farq — **qulaylik** (Vercel eng oson), **yaqinlik** (Cloudflare edge eng tez), va **vaqt chegarasi** (serverless'da bor, doimo-yoqiq serverda yo'q). Tanlovni ishingiz qisqa yoki uzunligiga qarab qiling.

---

## 4. Muhit o'zgaruvchilari va maxfiylar (secrets)

Bu — deploy'da eng ko'p xato qilinadigan joy, va eng xavflisi. Qoidalar oddiy, lekin ularni qattiq tuting.

**1. Kalit platformaning maxfiy do'konidan keladi.** Har bir platformada "Environment Variables" yoki "Secrets" bo'limi bor (Vercel dashboard, Cloudflare dashboard, Render sozlamalari). `ANTHROPIC_API_KEY` ni o'sha yerga qo'shasiz. Kod uni xuddi lokaldagidek o'qiydi:

```js
// Server kodida — qaysi platformada bo'lsa ham bir xil
const apiKey = process.env.ANTHROPIC_API_KEY;
// @anthropic-ai/sdk va @ai-sdk/anthropic buni AVTOMATIK o'qiydi —
// new Anthropic() yoki anthropic("claude-opus-4-8") deb yozsangiz kifoya.
```

**2. Hech qachon git'ga qo'ymang.** `.env` (va `.env.local`) faylini `.gitignore` ga qo'ying. Kalit git tarixiga bir marta tushsa — uni o'chirgan bilan tarixdan ketmaydi, va repozitoriyani ko'rgan har kim uni topadi. (Bu xato shunchalik ko'p uchraydiki, GitHub o'zi kalitlarni avtomatik skanerlaydi.)

**3. Klientga sizdirib qo'ymang.** Next.js'da `NEXT_PUBLIC_` prefiksli o'zgaruvchi **brauzerga yuboriladi** — `NEXT_PUBLIC_ANTHROPIC_API_KEY` deb yozish kalitni butun internetga oshkor qilishdir. Kalit prefiksisiz, oddiy `ANTHROPIC_API_KEY` bo'lib qolsin.

**4. Muhitlar uchun alohida kalitlar.** Ishlab chiqish (dev) va production uchun **alohida** kalit yarating. Shunday qilsangiz: dev kaliti tasodifan sizib ketsa, production'ga ta'sir qilmaydi; har muhitning xarajatini alohida kuzatasiz; bittasini bekor qilish boshqasini buzmaydi.

**5. Xarajat chegarasini (spending limit) o'rnating.** Anthropic Console'da hisobingizga oylik xarajat chegarasini qo'ying. Bu — production'ning "xavfsizlik kamari": kodda xatolik (cheksiz sikl) yoki suiiste'mol bo'lsa, chegara hisobingizni himoya qiladi.

> **Konseptual eslatma.** Bu qoidalar — 22-bobdagi kalit xavfsizligi mavzusining deploy'dagi amaliy ko'rinishi. Bu yerda **g'oyani** yodda tuting: kalit kodda emas, git'da emas, klientda emas — faqat platformaning maxfiy do'konida. Har bir platformaning aniq oynasi va atamasi hujjatda; lekin qoida hamma joyda bir xil.

---

## 5. Production'da streaming va to'g'ri runtime

Yaxshi xabar: oqim (streaming) production'da ham ishlaydi — Vercel serverless va edge funksiyalarida, Cloudflare Workers'da, Node serverda. 13-bobdagi `toUIMessageStreamResponse()` o'sha-o'sha qoladi. Lekin bitta yangi qaror bor: **funksiya qaysi runtime'da ishlasin?**

Next.js Route Handler'da buni bitta qator bilan tanlaysiz:

```js
// app/api/chat/route.js
import { anthropic } from "@ai-sdk/anthropic";
import { streamText, convertToModelMessages } from "ai";

// Runtime tanlovi: "edge" (tez, global, cheklangan) yoki "nodejs" (to'liq API).
// Aniq qiymat va xulq Next.js/platforma versiyasiga bog'liq — hujjatdan tasdiqlang.
export const runtime = "edge";

export async function POST(req) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic("claude-opus-4-8"),
    messages: await convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

Ikki runtime o'rtasidagi farq:

- **`runtime = "edge"`** — funksiya edge'da, foydalanuvchiga yaqin ishlaydi. **Tez va global**, lekin **cheklangan**: to'liq Node API yo'q (ba'zi paketlar ishlamaydi), vaqt/xotira chegaralari qattiqroq. Oddiy chat va proksi route uchun ajoyib.
- **`runtime = "nodejs"`** — funksiya to'liq Node muhitda ishlaydi. Hamma Node API mavjud, og'irroq kutubxonalar ishlaydi; biroz sekinroq sovuq start, lekin moslashuvchanroq.

Qaysi birini tanlash kerak? Sodda qoida: agar kodingiz **faqat `fetch` va Anthropic SDK** ishlatsa va past kechikish kerak bo'lsa — `edge`. Agar Node-ga xos paket (fayl tizimi, ma'lum DB drayverlari, og'ir kutubxonalar) ishlatsangiz — `nodejs`. Shubha bo'lsa, `nodejs` dan boshlang: u eng mos keladi, keyin tezlik kerak bo'lsa `edge` ga o'tasiz.

> **Streaming nega muhim — UX uchun ham, timeout uchun ham.** Oqim foydalanuvchiga birinchi tokenni **tez** beradi — ekran bo'sh qolmaydi (13-bob). Bundan tashqari, oqim ulanishni "jonli" ushlab turadi: ma'lumot doimo oqib turgani uchun ulanish "jim" qolib timeout'ga uchramaydi (16-bob, timeout bo'limi). Demak production'da streaming — standart tanlovingiz bo'lsin.

---

## 6. Funksiya vaqt chegarasi — agentning eng katta tuzog'i

Mana deploy'dagi eng ko'p "nega ishlamayapti?" sababi. Serverless va edge funksiyalarining **maksimal ishlash vaqti** bor — platforma va rejaga qarab taxminan 10–60 soniya (aniq raqam hujjatga qarang). Funksiya shu vaqtdan oshib ketsa, platforma uni **majburan to'xtatadi** — ish yarmida uziladi.

Chat uchun bu muammo emas: bitta chaqiruv bir necha soniya, oqim birinchi tokenni darrov beradi. Lekin **ko'p qadamli agent** (7-bob) — Claude tool chaqiradi, natijani oladi, yana tool chaqiradi, yana... — bir necha daqiqaga cho'zilishi mumkin. Bu funksiya chegarasidan oshib ketadi.

![Serverless funksiya vaqt chegarasi muammosi: qisqa chat chaqiruvi funksiyaning vaqt chegarasiga sig'adi (yashil, OK); uzoq ko'p-qadamli agent ishi chegaradan oshib ketadi (qizil, funksiya uziladi). Yechim: ishni fon navbatiga (queue) yoki doimo ishlaydigan ishchiga (worker) o'tkazib, jarayonni oqim bilan ko'rsatish.](rasmlar/ai25-timeout-muammo.svg)

**Qachon serverless yetarli (chegara muammo emas):**

- Bitta chat chaqiruvi yoki qisqa suhbat.
- RAG so'rovi: qidiruv + bitta model chaqiruvi.
- Strukturali chiqish, klassifikatsiya, qisqa generatsiya.

**Qachon serverless yetmaydi (worker/navbat kerak):**

- Uzun ko'p qadamli agent (o'nlab tool chaqiruvlari).
- Katta hujjat to'plamini qayta ishlash.
- Daqiqalar davom etadigan har qanday ish.

**Yechim — uzoq ishni funksiyadan tashqariga chiqaring:**

1. **Ishni fon navbatiga (queue) qo'ying.** So'rov kelganda funksiya butun ishni o'zi bajarmaydi — ishni navbatga qo'shadi va darhol "qabul qilindi" (job id) deb javob beradi. Funksiya soniyalarda yopiladi, chegaraga urilmaydi.
2. **Doimo-yoqiq ishchi (worker) bajaradi.** Navbatdagi ishni Node server yoki fon ishchisi oladi va vaqt chegarasisiz bajaradi (3-bobdagi Node server varianti).
3. **Jarayonni foydalanuvchiga ko'rsating.** Ish davom etayotganini holat (status) so'rovi yoki oqim bilan bildiring: "tahlil qilinmoqda… 3/10 qadam". Tugagach natijani ko'rsatasiz.

> **Ommaviy ish bo'lsa — Batches API.** Agar minglab so'rovni **bir vaqtda** (real-time emas) qayta ishlamoqchi bo'lsangiz — bu aynan [Batches API](./24-batch-optimizatsiya.md) ning ishi: 50% arzon, va u uzoq ishni Anthropic tomonida bajaradi, sizning funksiyangizni band qilmaydi. Real-time uzoq agent uchun esa — worker/navbat. Ikki vositani aralashtirib yubormang: batch = ommaviy/kechiktirilgan, worker = jonli uzoq jarayon.

---

## 7. Production tayyorlik ro'yxati (checklist)

Ilovani internetga ochishdan oldin shu ro'yxatdan o'ting. Har bir band — bu kitobdagi bir bobning production'dagi aksi.

| # | Tekshiruv | Qayerda |
|---|---|---|
| 1 | Kalit platforma maxfiylarida, git'da/klientda emas | bu bob §4, [22-bob](./22-xavfsizlik.md) |
| 2 | Xarajat chegarasi (spending limit) o'rnatilgan | Anthropic Console |
| 3 | Tipli xato boshqaruvi + backoff/retry | [16-bob](./16-xatolar-retry.md) |
| 4 | Log/trace + xarajat kuzatuvi (monitoring) | 23-bob |
| 5 | Foydalanuvchi bo'yicha rate limiting | [22-bob](./22-xavfsizlik.md) |
| 6 | Streaming yoqilgan (UX + timeout uchun) | bu bob §5, [13-bob](./13-ai-sdk-ui.md) |
| 7 | To'g'ri runtime tanlangan (edge / nodejs) | bu bob §5 |
| 8 | Uzun ishlar worker/navbatga chiqarilgan | bu bob §6 |
| 9 | Prompt caching (takror kontekstda tejash) | 15-bob |
| 10 | Graceful degradation (fallback) | [16-bob](./16-xatolar-retry.md) |

Bu ro'yxat — sizning "deploy oldidan" odatingiz bo'lsin. Birinchi to'rttasi (kalit, xarajat chegarasi, xato boshqaruvi, monitoring) — **majburiy**; ularsiz production'ga chiqmang. Qolganlari ilovangiz turiga qarab.

---

## 8. Loyiha: 13-bobdagi chatbotni Vercel'ga deploy qilish

Hammasini amalda ko'ramiz. 13-bobdagi minimal streaming chatbotni Vercel'ga chiqaramiz — qadam-baqadam.

**1-qadam — loyiha tayyor bo'lsin.** 13-bobdagi ikki fayl joyida bo'lsin: `app/api/chat/route.js` (server route) va `app/page.jsx` (chat sahifasi). Lokalda `npm run dev` bilan ishlayotganiga ishonch hosil qiling.

**2-qadam — route'ga runtime qo'shing.** Oddiy chat uchun edge ajoyib:

```js
// app/api/chat/route.js
import { anthropic } from "@ai-sdk/anthropic";
import { streamText, convertToModelMessages } from "ai";

export const runtime = "edge"; // tez, global; Node-ga xos paket yo'q bo'lsa

export async function POST(req) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic("claude-opus-4-8"),
    system: "Sen foydali, qisqa javob beradigan o'zbek tilidagi yordamchisan.",
    messages: await convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

**3-qadam — `.env.local` ni git'dan himoyalang.** `.gitignore` da `.env*` borligini tekshiring. Kalit hech qachon git'ga tushmasin.

**4-qadam — git'ga push qiling va Vercel'ga ulang.** Loyihani GitHub'ga yuklang. Vercel'da "New Project" → repozitoriyangizni tanlang. Vercel Next.js'ni avtomatik aniqlaydi.

**5-qadam — kalitni Vercel'ga qo'shing.** Vercel loyiha sozlamalarida **Settings → Environment Variables** ga o'ting. `ANTHROPIC_API_KEY` nomini va kalit qiymatini qo'shing. Vercel uni faqat server funksiyalariga beradi — brauzerga emas. (Production va Preview muhitlari uchun alohida belgilashingiz mumkin.)

**6-qadam — deploy.** "Deploy" tugmasini bosing (yoki keyingi `git push` avtomatik deploy qiladi). Vercel ilovani quradi va sizga jonli URL beradi.

**7-qadam — oqimni tekshiring.** Jonli URL'ni oching, savol yuboring va javob **token-token** oqib kelishini kuzating — xuddi lokaldagidek. Endi brauzerda **DevTools → Network** ni oching, `/api/chat` so'rovini toping va so'rov/javobda `ANTHROPIC_API_KEY` **yo'qligiga** ishonch hosil qiling. Kalit serverda qoldi — bu sizning chegarangiz ishlayotganining isboti.

Tabriklaymiz — ilovangiz endi internetda, real foydalanuvchilar uchun, kalit esa xavfsiz.

### Vercel'siz muqobil: kichik Express streaming serveri

Hamma loyiha Next.js'da emas, va ba'zida sizga **doimo-yoqiq Node server** kerak (uzoq agentlar uchun, 6-bo'lim). Mana o'sha bir xil g'oyaning Express varianti — uni Render, Railway yoki VPS'ga deploy qilasiz:

```js
// server.js — doimo-yoqiq Node server (Express)
import express from "express";
import Anthropic from "@anthropic-ai/sdk";

const app = express();
app.use(express.json());

const client = new Anthropic(); // ANTHROPIC_API_KEY muhitdan (process.env)

app.post("/api/chat", async (req, res) => {
  const { messages } = req.body;

  // Oqimni SSE sifatida brauzerga yetkazamiz (04-bobdagi g'oya)
  res.setHeader("Content-Type", "text/plain; charset=utf-8");

  const stream = client.messages
    .stream({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages,
    })
    .on("text", (delta) => res.write(delta)) // har bo'lakni darhol yuboramiz
    .on("error", (err) => {
      console.error("Oqim xatosi:", err.message); // 16-bob: chiroyli boshqaruv
      res.end();
    });

  await stream.finalMessage();
  res.end();
});

// Platforma PORT ni muhit orqali beradi (Render/Railway shunday qiladi)
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server ${port}-portda ishlamoqda`));
```

Bu server **doimo ishlab turadi** — vaqt chegarasi yo'q, demak uzun agent siklilari bemalol ishlaydi. E'tibor bering: kalit baribir `process.env.ANTHROPIC_API_KEY` dan keladi (deploy platformasi maxfiylaridan), va `PORT` ni platforma beradi. Chegara bir xil: klient → bu server → Anthropic.

> **Tanlov xulosasi.** Next.js + chat → Vercel (eng oson). Global yengil route → Cloudflare edge. Uzun agent / fon ishi → doimo-yoqiq Node server (yuqoridagi Express). AWS'dasizmi → Lambda + (uzun ish uchun) SQS. Hammasida kalit serverda, hammasida shu bir xil arxitektura chegarasi.

---

## 9. Tez-tez uchraydigan xatolar

| Xato | Sabab | Yechim |
|---|---|---|
| Kalit production'da topilmadi | Vercel/CF env'iga qo'shilmagan | Platforma "Environment Variables" ga `ANTHROPIC_API_KEY` qo'shing |
| Kalit git tarixida ko'rinib qoldi | `.env` `.gitignore` da emas | `.env*` ni gitignore qiling, kalitni **bekor qilib** yangisini oling |
| Kalit brauzerga sizib ketdi | `NEXT_PUBLIC_` prefiks ishlatilgan | Prefiksisiz oddiy `ANTHROPIC_API_KEY` |
| Edge'da paket ishlamadi | To'liq Node API yo'q | `runtime = "nodejs"` ga o'ting yoki edge-mos paket |
| Uzun agent yarmida uzildi | Funksiya vaqt chegarasi | Worker/navbatga chiqaring; jarayonni oqim bilan ko'rsating |
| Oqim kelmadi, faqat to'liq javob | Route oqim qaytarmayapti | `streamText` + `toUIMessageStreamResponse` ni tekshiring |
| Kutilmagan katta hisob | Xarajat chegarasi + rate limit yo'q | Console'da limit; foydalanuvchi bo'yicha rate limiting (22-bob) |

---

## Xulosa

- Lokalda ishlatish ≠ production. Deploy'da to'rt savol hal qilinadi: kod qayerda ishlaydi, kalit qanday xavfsiz qoladi, oqim ishlaydimi, uzoq ishlar va xarajat nazoratdami.
- **Arxitektura chegarasi o'zgarmaydi:** klient → sizning serveringiz (kalit shu yerda) → Anthropic. Deploy faqat shu chegara haqiqatan saqlanishini tekshiradi.
- **Variantlar:** Vercel (Next.js+AI SDK, eng oson, serverless/edge) · Cloudflare Workers (edge, global, lekin to'liq Node API yo'q) · Node server (uzoq agentlar, to'liq Node API, vaqt chegarasiz) · AWS Lambda (serverless, AWS ekotizimi).
- **Maxfiylar:** kalit platforma secrets'ida, git'da emas, klientda emas, `NEXT_PUBLIC_` emas; dev/prod uchun alohida kalit; xarajat chegarasi.
- **Streaming production'da ishlaydi.** Runtime'ni to'g'ri tanlang: `edge` (tez/global/cheklangan) yoki `nodejs` (to'liq API). Streaming UX'ni ham, timeout'ni ham yaxshilaydi.
- **Eng katta tuzoq — funksiya vaqt chegarasi.** Chat sig'adi; uzun agent oshib ketadi → fon navbati + worker + jarayonni ko'rsatish. Ommaviy ish → Batches API ([24-bob](./24-batch-optimizatsiya.md)).
- **Production ro'yxati:** kalit secrets'da, xarajat chegarasi, xato/retry ([16-bob](./16-xatolar-retry.md)), monitoring (23-bob), rate limiting ([22-bob](./22-xavfsizlik.md)), streaming, to'g'ri runtime, caching (15-bob), fallback.

---

## Mashqlar

> Maslahat: bu mashqlar uchun 13-bobdagi chatbot loyihasi va Anthropic kaliti kerak bo'ladi. Aniq sozlama oynalari, funksiya vaqt chegaralari va runtime nomlari platforma versiyasiga bog'liq — ishlamasa, birinchi navbatda o'sha platformaning joriy hujjatini tekshiring.

### Oson

1. **`.gitignore` tekshiruvi.** Loyihangizdagi `.gitignore` da `.env*` borligini tekshiring. Yo'q bo'lsa qo'shing. Bir jumlada: nega kalit git tarixiga **bir marta** tushsa ham xavfli (oddiy o'chirish yetarli emas)?
2. **Runtime tanlovi.** Quyidagi ikki holatda `runtime = "edge"` yoki `"nodejs"` dan qaysisini tanlaysiz va nega: (a) faqat `fetch` + Anthropic SDK ishlatadigan oddiy chat route; (b) fayl tizimidan (`fs`) hujjat o'qiydigan route.
3. **`NEXT_PUBLIC_` tuzog'i.** Nega `NEXT_PUBLIC_ANTHROPIC_API_KEY` deb yozish **xavfli**? Kalit aynan qayerga sizib ketadi va uni kim ko'ra oladi?

### O'rta

4. **Vercel'ga deploy.** 13-bobdagi chatbotni Vercel'ga deploy qiling (8-bo'limdagi qadamlar bo'yicha). Jonli URL'da oqim ishlashini va DevTools → Network'da kalit **yo'qligini** tasdiqlang.
5. **Qisqa vs uzoq ish.** Quyidagilarning qaysisi serverless funksiyaga sig'adi, qaysisi worker/navbat talab qiladi va nega: (a) bitta chat javobi; (b) 30 ta tool chaqiruvi bo'lgan tadqiqot agenti; (c) RAG so'rovi (qidiruv + bitta chaqiruv); (d) 5000 ta mahsulot tavsifini generatsiya qilish.
6. **Production ro'yxati audi­ti.** 7-bo'limdagi ro'yxatni o'z ilovangizga qo'llang. 10 banddan nechtasi bajarilgan? Bajarilmaganlaridan qaysi to'rttasi **majburiy** ekanini ayting.

### Qiyin

7. **Express muqobili.** 8-bo'limdagi Express serverni lokalda ishga tushiring va unga oddiy HTML+JS klientdan `fetch` qiling (13-bobdagi React'siz klient g'oyasi). Kalit `process.env` dan kelishini va oqim ishlashini tasdiqlang.
8. **Uzoq agent rejasi (dizayn).** Tasavvur qiling: sizda 20 qadamli tadqiqot agenti bor va u Vercel funksiyasida timeout'ga uchrayapti. Kodsiz, faqat **arxitektura** sifatida tasvirlang: so'rov kelganda nima bo'ladi, ish qayerda bajariladi, foydalanuvchi jarayonni qanday ko'radi, natija unga qanday yetadi?

<details markdown="1">
<summary>Yechimlar</summary>

> Eslatma: platforma oynalari, vaqt chegaralari (soniyalar) va runtime nomlari versiyaga bog'liq — yechimlardagi aniq raqamlarni o'sha platformaning joriy hujjatidan tasdiqlang. G'oya o'zgarmaydi.

**1-mashq.** `.gitignore` da `.env*` (yoki hech bo'lmaganda `.env` va `.env.local`) bo'lishi shart. Nega bir marta tushsa ham xavfli: git **tarixni saqlaydi** — keyingi commit'da faylni o'chirsangiz ham, eski commit'da kalit qoladi va repozitoriyani klonlagan har kim uni `git log`/tarixdan topadi. Shuning uchun sizib ketgan kalitni **o'chirish emas, bekor qilish** (rotate) kerak: Console'da eski kalitni o'chirib, yangisini yarating.

**2-mashq.** (a) Faqat `fetch` + Anthropic SDK → `runtime = "edge"`: tez, global, va edge cheklovlariga urilmaydi (SDK `fetch` ga asoslangan). (b) `fs` bilan fayl o'qish → `runtime = "nodejs"`: fayl tizimi — Node-ga xos API, edge'da yo'q. Umumiy qoida: Node-ga xos narsa ishlatsangiz `nodejs`, aks holda `edge` (yoki shubhada `nodejs` dan boshlang).

**3-mashq.** `NEXT_PUBLIC_` prefiksli o'zgaruvchi Next.js tomonidan **brauzer JS bundle'iga** joylashtiriladi — ya'ni kalit sahifa ochilganda yuklangan JavaScript faylida ochiq matn bo'lib turadi. Sahifani ochgan **har bir odam** (DevTools → Sources/Network orqali) uni ko'radi va o'g'irlaydi, keyin sizning hisobingizdan cheksiz so'rov yuboradi. Kalit prefiksisiz, oddiy `ANTHROPIC_API_KEY` bo'lib, faqat serverda qolishi shart.

**4-mashq.** 8-bo'limdagi 7 qadam: route'ga `runtime` qo'shish → `.gitignore` da `.env*` → GitHub'ga push → Vercel'ga ulash → **Settings → Environment Variables** ga `ANTHROPIC_API_KEY` → Deploy → jonli URL'da oqimni tekshirish. Tekshiruv: DevTools → Network → `/api/chat` so'rovi — tanasida faqat `messages`, javobda Claude matni, kalit **hech qaerda yo'q**. Bu kalit serverda qolganini isbotlaydi.

**5-mashq.**
- (a) Bitta chat javobi → **serverless** (sekundlar, sig'adi).
- (b) 30 tool chaqiruvli agent → **worker/navbat** (daqiqalar, funksiya chegarasidan oshadi).
- (c) RAG so'rovi (qidiruv + bitta chaqiruv) → **serverless** (qisqa).
- (d) 5000 ta tavsif generatsiyasi → bu **ommaviy** ish; eng to'g'risi [Batches API](./24-batch-optimizatsiya.md) (24-bob) — 50% arzon va funksiyani band qilmaydi. Real-time talab qilinmaydigan katta hajm aynan batch uchun.

Asosiy ajratuvchi: ish **sekundlarda** tugaydimi (serverless) yoki **daqiqalar**ga cho'ziladimi (worker), va u **jonli** kerakmi yoki **kechiktirilgan ommaviy**mi (batch).

**6-mashq.** Ro'yxatni belgilab chiqing. Majburiy to'rttasi — bularsiz production'ga chiqmang:
1. Kalit secrets'da (git'da/klientda emas).
2. Xarajat chegarasi o'rnatilgan.
3. Tipli xato boshqaruvi + retry ([16-bob](./16-xatolar-retry.md)).
4. Monitoring + xarajat kuzatuvi (23-bob).

Qolganlari (rate limiting, streaming, runtime, worker, caching, fallback) — ilova turiga qarab muhim, lekin yuqoridagi to'rttasi poydevor.

**7-mashq.** 8-bo'limdagi `server.js` ni `node server.js` bilan ishga tushiring (`ANTHROPIC_API_KEY` muhitda bo'lsin). Keyin 13-bobdagi React'siz klient g'oyasi bilan oddiy `index.html` dan `fetch("/api/chat", { method: "POST", ... })` qiling va `response.body.getReader()` orqali kelgan oqimni `<div>` ga yozib boring. Kalit faqat serverda (`process.env`), klient kodida yo'q. (Lokalda CORS uchun klient va serverni bir xil portdan bering yoki Express'ga CORS qo'shing.)

**8-mashq (arxitektura).**

1. **So'rov kelganda:** Vercel funksiyasi (yoki API route) butun agentni o'zi bajarmaydi — u ishni **fon navbatiga** (queue) qo'shadi va darhol `{ jobId }` qaytaradi. Funksiya soniyalarda yopiladi, timeout'ga urilmaydi.
2. **Ish qayerda bajariladi:** **doimo-yoqiq worker** (Node server — Render/Railway/VPS) navbatdan ishni oladi va 20 qadamli agentni vaqt chegarasisiz bajaradi.
3. **Foydalanuvchi jarayonni qanday ko'radi:** klient `jobId` bo'yicha holatni so'rab turadi (polling) yoki oqim/WebSocket orqali jonli yangilanish oladi: "3/20 qadam… 11/20 qadam…".
4. **Natija qanday yetadi:** worker tugagach natijani saqlaydi (DB/kesh); keyingi holat so'rovi tayyor natijani qaytaradi (yoki worker oqim orqali yakuniy javobni yuboradi).

Kalit g'oya: **serverless funksiya ishni qabul qiladi, worker bajaradi, foydalanuvchi jarayonni kuzatadi.** Funksiya hech qachon uzoq ushlanmaydi — shuning uchun timeout muammosi yo'qoladi.

</details>

---

[⬅️ Oldingi: 24 — Batch API va optimizatsiya](./24-batch-optimizatsiya.md) · [🏠 README](./README.md) · [Keyingi: 26 — Yakuniy loyiha: to'liq AI ilova ➡️](./26-kapston-loyiha.md)
