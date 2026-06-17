# 02 — O'rnatish va birinchi chaqiruv

[⬅️ Oldingi: 01 — LLM nima va qanday ishlaydi](./01-llm-nima.md) · [🏠 README](./README.md) · [Keyingi: 03 — Messages API chuqur ➡️](./03-messages-api.md)

> **Bu bobda:** Endi nazariyadan amaliyotga o'tamiz. Birinchi bobda LLM "keyingi token"ni bashorat qiluvchi model ekanini ko'rdik; bu bobda esa shu modelga **JavaScript'dan haqiqiy so'rov yuborib, javob olamiz**. Avval kichik Node loyihasini tayyorlaymiz (`npm init`, ESM yoqamiz), keyin Anthropic konsolidan **API kalit** olamiz va — eng muhimi — uni xavfsiz saqlashni o'rganamiz: nega kalitni hech qachon kodga yozmaslik va Git'ga yubormaslik kerakligini. So'ng `@anthropic-ai/sdk` paketini o'rnatib, birinchi `messages.create` chaqiruvini yozamiz va har bir qatorini tushuntiramiz. Javob obyektini ochib ko'ramiz — nega `content` satr emas, balki **massiv** ekanini, `stop_reason` va `usage` nima berishini. Oxirida birinchi xatolarni (401, 404, 400) o'qishni o'rganamiz va arzon eksperiment qilishni — chunki har chaqiruv haqiqiy pul turadi.

---

## Avval — nima kerak?

Bu kitobning JavaScript nashri bo'lgani uchun, sizda JavaScript va Node.js asoslari bor deb hisoblaymiz: `async`/`await`, modullar (`import`/`export`), `npm`. Agar bular hali tanish bo'lmasa, avval [Node.js kitobini](../nodejs/README.md) ko'rib chiqing — bu yerda ularni qaytadan tushuntirmaymiz.

Texnik talab juda yengil:

- **Node.js 18 yoki undan yuqori.** Terminalda tekshiring:

```bash
node -v
```

Agar `v18.0.0` yoki kattaroq raqam chiqsa — yetarli. Bu kitobda biz **Node 20.6+** ning bir qulay imkoniyatidan (`--env-file`) foydalanamiz, shuning uchun iloji bo'lsa Node 20+ o'rnating. `node -v` umuman ishlamasa, [nodejs.org](https://nodejs.org) dan LTS versiyasini o'rnating.

- **npm** — Node bilan birga keladi (`npm -v` bilan tekshiring). Boshqa hech narsa kerak emas: AI bilan ishlash uchun maxsus "kuchli kompyuter" yoki GPU shart emas. Sizning ilovangiz shunchaki **Anthropic serveriga so'rov yuboradi** — og'ir hisob-kitob ularning tomonida bo'ladi.

## Loyihani tayyorlash

Yangi papka ochib, uni Node loyihasiga aylantiramiz:

```bash
mkdir ai-birinchi
cd ai-birinchi
npm init -y
```

`npm init -y` buyrug'i loyiha papkasida `package.json` faylini yaratadi — bu loyihangizning "pasporti": nomi, versiyasi, bog'liqliklar (dependencies) ro'yxati shu yerda turadi. `-y` ("yes") esa barcha savollarga sukut bo'yicha javob beradi, vaqt tejaydi.

Endi **bitta muhim qadam**: loyihani **ESM** (ES Modules — zamonaviy `import`/`export` sintaksisi) rejimiga o'tkazamiz. Buning uchun `package.json` ichiga `"type": "module"` qatorini qo'shing:

```json
{
  "name": "ai-birinchi",
  "version": "1.0.0",
  "type": "module"
}
```

Nega? Chunki `@anthropic-ai/sdk` va bu kitobdagi barcha misollar `import Anthropic from "..."` ko'rinishidagi ESM sintaksisidan foydalanadi. `"type": "module"` qo'shmasangiz, Node fayllarni eski CommonJS (`require`) rejimida o'qishga urinadi va `import` so'zida xato beradi. Bu qatorni hozir qo'shib qo'ysangiz — keyin hech bir misolda muammo bo'lmaydi.

## API kalit olish

Claude'ga so'rov yuborish uchun sizga **API kalit** kerak — bu Anthropic serveriga "men kim ekanimni va kim hisob to'lashini" bildiradigan maxfiy parol. Olish tartibi:

1. [console.anthropic.com](https://console.anthropic.com) saytiga kiring va ro'yxatdan o'ting.
2. **Billing** (to'lov) bo'limida hisobingizga biroz kredit qo'shing. Anthropic API **har token uchun pul** oladi (bu haqda quyida va batafsil [14-bobda](./14-token-narx-limit.md)) — bepul cheksiz emas.
3. **API Keys** bo'limiga o'tib, **Create Key** tugmasini bosing. Sizga `sk-ant-...` bilan boshlanadigan uzun satr beriladi.

> ⚠️ **Kalit faqat bir marta to'liq ko'rsatiladi.** Konsol oynasini yopsangiz, kalitni qaytadan ko'ra olmaysiz (faqat yangisini yaratasiz). Shuning uchun darrov nusxalab, xavfsiz joyga (quyidagi `.env` faylga) qo'ying.

> 💡 **Sarf chegarasini belgilang.** Konsolning Billing bo'limida oylik **spending limit** (sarf chegarasi) qo'yib qo'ying — masalan, 5$. Shunda o'rganish jarayonida xato bilan ko'p so'rov yuborib qo'ysangiz ham, hisobingiz himoyalangan bo'ladi. Boshlovchi uchun bu juda foydali tinchlik.

## ENG MUHIM: kalitni xavfsiz saqlash

Bu bobning eng muhim qismi shu — kodga yoki diqqatga oid bir necha satrdan ham muhimroq. **API kalit — bu sizning pulingiz.** U o'g'irlansa, begona odam sizning hisobingizdan minglab so'rov yuborib, pulingizni sarflashi mumkin.

Eng keng tarqalgan halokatli xato — kalitni to'g'ridan-to'g'ri kod ichiga yozib qo'yish va keyin loyihani GitHub'ga yuklash:

```js
// ❌ HECH QACHON BUNDAY QILMANG
const client = new Anthropic({ apiKey: "sk-ant-abc123..." });
```

Nega bu xavfli? GitHub'ga (yoki har qanday ochiq joyga) yuklangan zahoti, kalit **butun internetga ko'rinadi**. Bundan ham yomoni: maxsus **botlar** doimo yangi repozitoriylarni skanlab, `sk-ant-...` ko'rinishidagi kalitlarni qidiradi. Kalit bir necha daqiqada topiladi va ishlatib yuboriladi. Bu — afsona emas, kundalik haqiqat.

To'g'ri yo'l — kalitni koddan **tashqarida**, `.env` faylida saqlash.

![API kalitni saqlash: to'g'ri yo'l (.env + gitignore) va noto'g'ri yo'l (kodga yozib GitHub'ga yuklash, natijada o'g'irlanadi)](rasmlar/ai02-env-xavfsizlik.svg)

Loyiha papkasida `.env` nomli fayl yarating (e'tibor bering — nomi nuqta bilan boshlanadi, kengaytmasi yo'q):

```text
ANTHROPIC_API_KEY=sk-ant-bu-yerga-haqiqiy-kalitingizni-qoying
```

Endi — **muhim** — `.gitignore` faylini yaratib (yoki mavjudiga qo'shib), `.env` ni va `node_modules` ni Git e'tiboridan tashqariga chiqaramiz:

```text
.env
node_modules/
```

`.gitignore` — Git'ga "bu fayllarni kuzatma, commit qilma" deb aytadigan ro'yxat. Shu ikki qator bilan kalitingiz hech qachon repozitoriyga tushmaydi. Endi kalit faqat sizning mashinangizdagi `.env` faylida yashaydi, kod esa uni **ish vaqtida** (runtime) o'qiydi.

> 🔑 **Oltin qoida:** kalit hech qachon kod fayliga (`.js`) yozilmaydi, hech qachon Git'ga tushmaydi. Agar adashib kalitni biror joyga qo'yib yuborsangiz — konsolda darhol o'sha kalitni **bekor qiling** (revoke) va yangisini yarating. Bekor qilingan kalit endi ishlamaydi, demak o'g'riga foydasiz.

## SDK ni o'rnatish

Endi Anthropic'ning rasmiy JavaScript paketini o'rnatamiz:

```bash
npm i @anthropic-ai/sdk
```

`npm i` (`npm install`ning qisqasi) paketni internetdan yuklab, loyihangizning `node_modules` papkasiga qo'yadi va `package.json` ga bog'liqlik sifatida yozib qo'yadi. Bu paket — Claude API bilan ishlashning eng qulay yo'li: HTTP so'rovlarini, autentifikatsiyani, xatolarni — hammasini siz uchun o'zi boshqaradi. Siz shunchaki JavaScript funksiyasini chaqirasiz.

> Bu kitob jonli o'rnatilgan **`@anthropic-ai/sdk` 0.104** versiyasi bilan tekshirilgan. Sizda biroz yangiroq versiya bo'lsa ham, bu yerdagi metodlar (`messages.create` va boshqalar) aynan ishlaydi.

## Birinchi chaqiruv

Mana — kutilgan lahza. Loyiha papkasida `app.js` faylini yarating va shuni yozing:

```js
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // ANTHROPIC_API_KEY ni env'dan avtomatik o'qiydi

const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "JavaScript nima ekanini bir jumlada tushuntir." },
  ],
});

console.log(msg.content[0].text);
```

Ishga tushiring — Node 20.6+ ning o'rnatilgan `.env` o'quvchisi bilan:

```bash
node --env-file=.env app.js
```

`--env-file=.env` — Node'ga "ishga tushishdan oldin `.env` faylidagi o'zgaruvchilarni o'qib ol" deydi. Shu tufayli `ANTHROPIC_API_KEY` muhit o'zgaruvchisi (environment variable) sifatida mavjud bo'ladi, va SDK uni avtomatik topadi.

Bir necha soniyadan keyin terminalda Claude'ning javobini ko'rasiz, masalan:

```text
JavaScript — bu veb-sahifalarni interaktiv qiladigan, brauzerda ham serverda
ham ishlay oladigan dasturlash tili.
```

Tabriklaymiz — siz hozirgina JavaScript'dan birinchi AI so'rovingizni yubordingiz va javob oldingiz! Endi har bir qatorni ochib tushunaylik.

### Har bir qator nima qiladi

- `import Anthropic from "@anthropic-ai/sdk";` — paketdan asosiy `Anthropic` klassini chaqirib olamiz (ESM `import`, shuning uchun `"type": "module"` kerak edi).
- `const client = new Anthropic();` — **klient** obyektini yaratamiz. Bu — API bilan gaplashadigan "telefon". Hech qanday kalit bermadik, chunki klient `ANTHROPIC_API_KEY` muhit o'zgaruvchisini o'zi qidirib topadi. Mana shuning uchun kalitni koddan tashqarida, `.env` da saqlash ham xavfsiz, ham qulay.
- `await client.messages.create({ ... })` — bu **asosiy chaqiruv**: Claude'ga xabar yuborib, javob so'raymiz. `await` ishlatamiz, chunki bu tarmoq so'rovi — javob kelguncha vaqt ketadi. (`await` top-level'da, ya'ni funksiya ichida bo'lmasdan ishlayapti — bu ESM modulida mumkin.)

Chaqiruvdagi uchta parametrni alohida ko'ramiz:

- `model: "claude-opus-4-8"` — qaysi modelga murojaat qilishimiz. `claude-opus-4-8` — eng kuchli model. Eksperiment uchun arzonroq modellar ham bor (quyida ko'ramiz).
- `max_tokens: 1024` — javobning **eng ko'p uzunligi** (tokenlarda). Bu ikki vazifani bajaradi: (1) juda uzun javobni cheklaydi, (2) **narx tomini** ushlab turadi — model bundan ko'p token chiqara olmaydi, demak xarajat ham cheklangan. Diqqat: bu parametr nomi **snake_case** (`max_tokens`), `maxTokens` emas — bu API'ning qoidasi.
- `messages: [...]` — suhbat **xabarlari massivi**. Hozir bitta xabar bor: `{ role: "user", content: "..." }`. `role: "user"` — "bu men, foydalanuvchi, gapiryapman" degani; `content` — aytayotgan matnimiz. (Rollar va ko'p bosqichli suhbat haqida [03-bobda](./03-messages-api.md) batafsil to'xtalamiz.)

So'ng `console.log(msg.content[0].text)` bilan javobni chop etamiz. Ana shu qatorda eng ko'p chalkashlik bo'ladi — keling, javob obyektini chuqur ochaylik.

![So'rov-javob oqimi: Node ilovangiz client.messages.create yuboradi, Anthropic API javob obyektini qaytaradi, ilovangiz content[0].text ni o'qiydi](rasmlar/ai02-sorov-javob.svg)

## Javobni o'qish — `content` bu MASSIV

Yangi boshlovchilar eng ko'p qiladigan xato: `msg` ni satr (string) deb o'ylash va to'g'ridan-to'g'ri `console.log(msg)` qilish. Aslida `msg` — boy **obyekt**, undagi matn esa ichkarida, bir necha qatlam pastda turadi.

![Javob obyektining anatomiyasi: content massiv (ichida text bloki), stop_reason va usage.input_tokens/output_tokens belgilangan](rasmlar/ai02-javob-struktura.svg)

Eng muhim tushuncha: **`msg.content` — bu massiv**, satr emas. Nega massiv? Chunki Claude javobi bir nechta "blok"dan iborat bo'lishi mumkin — matn bloki, vosita chaqiruvi bloki (keyingi boblarda) va hokazo. Hozir bizda bitta matn bloki bor, u massivning birinchi elementi:

```js
console.log(msg.content);
// [ { type: "text", text: "JavaScript — bu ..." } ]
```

Shuning uchun matnga yetib borish uchun: `msg.content[0].text` — "birinchi blok, uning `text` maydoni". Bu ishladi, lekin **professional usul** — blok turini tekshirib, barcha matn bloklarini yig'ish:

```js
for (const block of msg.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

Bu yondashuv kelajakda javob bir nechta blokli bo'lganda ham, matn bo'lmagan blok aralashganda ham (`block.type === "tool_use"` kabi) buzilmaydi. `block.type === "text"` tekshiruvi — "bu blok haqiqatan matnmi?" degan savol.

Obyektda yana ikki foydali maydon bor:

```js
console.log(msg.stop_reason); // "end_turn"
console.log(msg.usage);       // { input_tokens: 14, output_tokens: 31, ... }
```

- `msg.stop_reason` — model **nega to'xtaganini** aytadi. `"end_turn"` — Claude o'z javobini tabiiy ravishda yakunladi (eng yaxshi holat). `"max_tokens"` — javob `max_tokens` chegarasiga yetib, **o'rtada kesilib qoldi** degani; bunda `max_tokens` ni oshirish kerak bo'lishi mumkin.
- `msg.usage` — **nechta token sarflanganini** ko'rsatadi: `input_tokens` (siz yuborgan matn) va `output_tokens` (Claude qaytargan matn). **Mana shu — sizning narxingiz.** Har bir chaqiruvdan keyin shu raqamlarga qarab, qancha sarflayotganingizni his qilib borasiz. Tokenlar va narx haqida to'liq hisob-kitobni [14-bobda](./14-token-narx-limit.md) ko'ramiz.

## Birinchi xatolar va ularni o'qish

Birinchi chaqiruvda xato chiqsa — xavotir olmang, bu odatiy. SDK xatolarni HTTP **status kod** bilan beradi; eng ko'p uchraydigan uchtasini tanib oling:

- **401 (Authentication / `AuthenticationError`)** — kalit noto'g'ri yoki umuman topilmadi. Sabablari: `.env` fayl noto'g'ri joyda yoki nomi xato; `--env-file=.env` ni unutgansiz; kalitda ortiqcha bo'shliq/tirnoq bor; yoki kalit bekor qilingan. Tekshiruv: `console.log(process.env.ANTHROPIC_API_KEY)` qatorini vaqtincha qo'shib, kalit haqiqatan yuklanganini ko'ring (keyin bu qatorni o'chiring — kalitni terminalga chiqarish ham yaxshi odat emas).
- **404 (`NotFoundError`)** — odatda **model nomida xato**. `claude-opus-4-8` ni xato yozgansiz (masalan `claude-opus-4.8` yoki `claude-opus-4-08`). Imloni diqqat bilan solishtiring.
- **400 (`BadRequestError`)** — so'rov noto'g'ri tuzilgan. Masalan, `max_tokens` ni umuman bermagansiz (u **majburiy**), yoki `messages` massivi bo'sh, yoki maydon nomini `camelCase` qilib yozgansiz (`maxTokens`).

Xato xabarini **to'liq o'qing** — SDK odatda muammoni aniq aytadi (masalan, "`max_tokens: Field required`"). Xatoni dasturda chiroyli tutish uchun `try/catch` ishlatamiz (xatolarni, retry va timeout'ni keyingi qismlarda chuqur ko'ramiz); hozircha shuni biling: xato — dushman emas, yo'l ko'rsatkichi.

## Ikkinchi misol — o'zgartirib ko'ring

Eng yaxshi o'rganish — **o'ynab ko'rish**. `app.js` ni biroz o'zgartiramiz: boshqa so'rov va kichikroq `max_tokens`:

```js
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 60, // ataylab kichik — javob qisqaroq bo'ladi yoki kesilishi mumkin
  messages: [
    { role: "user", content: "Node.js'da fayl o'qishni 3 ta qadamda ayt." },
  ],
});

console.log(msg.content[0].text);
console.log("---");
console.log("To'xtash sababi:", msg.stop_reason);
console.log("Tokenlar:", msg.usage.input_tokens, "kirish /", msg.usage.output_tokens, "chiqish");
```

`max_tokens: 60` ni qo'yganimiz uchun javob qisqa bo'ladi, hatto `stop_reason` `"max_tokens"` chiqib, o'rtada kesilishi mumkin. `max_tokens` ni `1024` ga oshirib, qaytadan ishga tushiring — farqni o'z ko'zingiz bilan ko'rasiz. So'rov matnini ham erkin o'zgartiring: undan she'r so'rang, kod yozdiring, savol bering.

> 💡 **Arzon eksperiment qiling.** O'rganish bosqichida har bir mayda o'zgarishni Opus bilan sinash shart emas — bu nisbatan qimmat model. Tezkor, arzon sinov uchun modelni vaqtincha **`claude-haiku-4-5`** ga almashtiring: `model: "claude-haiku-4-5"`. Haiku tezroq va sezilarli arzonroq; sintaksis va oqim to'g'riligini tekshirish uchun ideal. Mantiq ishlaganiga ishonch hosil qilgach, kerak bo'lsa Opus'ga qaytasiz. (Model tanlash va narxlarni [14-bobda](./14-token-narx-limit.md) solishtiramiz.)

## Ishchi sikl (dev loop)

Endi sizda AI bilan ishlashning asosiy **takrorlanuvchi sikli** bor — uni butun kitob davomida ishlatasiz:

1. **Tahrirlash** — `app.js` da so'rov, model yoki parametrlarni o'zgartirasiz.
2. **Ishga tushirish** — `node --env-file=.env app.js`.
3. **O'qish** — javobni, `stop_reason` ni va `usage` ni ko'rasiz.
4. **Takrorlash** — natijaga qarab so'rovni yaxshilaysiz va yana ishga tushirasiz.

Aynan shu "tahrirla → ishga tushir → o'qi → yaxshilash" aylanasi — AI integratsiyasini o'rganishning yuragi. Ko'proq aylantirsangiz — model bilan qanday "gaplashishni" shunchalik yaxshi his qilasiz.

## Xulosa

- **Talab yengil:** Node 18+ (afzal 20.6+, `--env-file` uchun), npm. Maxsus apparat shart emas — og'ir ish Anthropic serverida bo'ladi.
- **Loyiha:** `npm init -y`, so'ng `package.json` ga `"type": "module"` (ESM uchun), keyin `npm i @anthropic-ai/sdk`.
- **API kalit** console.anthropic.com dan olinadi, sarf chegarasi qo'yiladi. Kalit **faqat bir marta** to'liq ko'rsatiladi.
- **Xavfsizlik (eng muhim):** kalit `.env` da saqlanadi, `.env` va `node_modules/` `.gitignore` ga qo'shiladi. Kalit **hech qachon** kodga yozilmaydi yoki Git'ga tushmaydi. Sizib chiqsa — darhol bekor qiling.
- **Birinchi chaqiruv:** `new Anthropic()` (kalitni env'dan o'qiydi) → `await client.messages.create({ model, max_tokens, messages })`. Ishga tushirish: `node --env-file=.env app.js`.
- **Javob — obyekt, satr emas:** `msg.content` bu **massiv**; matn `msg.content[0].text` da yoki bloklar bo'ylab `block.type === "text"` ni tekshirib olinadi. Yana `msg.stop_reason` ("end_turn"/"max_tokens") va `msg.usage` (token soni = narx).
- **Xatolar:** 401 = kalit, 404 = model nomi, 400 = noto'g'ri so'rov. Xato xabarini to'liq o'qing.
- **Arzon sinang:** o'rganishda `claude-haiku-4-5` bilan tajriba qiling, sikl — tahrirla → ishga tushir → o'qi → yaxshilash.

Keyingi bobda **Messages API**ni chuqurroq ochamiz: `user` va `assistant` rollari, `system` prompt, ko'p bosqichli suhbat (va nega API "holatsiz" — oldingi xabarlarni o'zi eslamaydi), `stop_reason` va content bloklarining to'liq manzarasi.

---

## Mashqlar

### Oson

1. O'z so'zlaringiz bilan tushuntiring: nega API kalitni `.env` faylida saqlash, kod ichiga yozishdan ko'ra xavfsizroq? Kalit GitHub'ga tushib qolsa nima bo'ladi?
2. Yangi loyiha yarating va uni ESM rejimiga o'tkazing. Qaysi faylga nima qo'shasiz? Nega bu qadam `@anthropic-ai/sdk` uchun zarur?
3. `msg.content` haqida quyidagi gaplardan qaysilari to'g'ri: (a) bu satr (string), (b) bu massiv, (c) birinchi matn `msg.content[0].text` da, (d) `msg.text` to'g'ridan-to'g'ri matnni beradi. To'g'rilarini tanlang.
4. `node --env-file=.env app.js` buyrug'idagi `--env-file=.env` qismi nima vazifani bajaradi? Uni tushirib qoldirsangiz, qaysi xato (status kod) chiqishi ehtimoli yuqori?
5. Quyidagi xato kodlarini sabablari bilan moslang: `401`, `404`, `400` ↔ "model nomida xato", "kalit yo'q/noto'g'ri", "so'rov noto'g'ri tuzilgan (masalan `max_tokens` yo'q)".

### O'rta

6. Birinchi chaqiruv kodini yozing va ishga tushiring. So'rov sifatida o'zingizning savolingizni bering. Javobni, `msg.stop_reason` ni va `msg.usage` ni konsolga chiqaring.
7. Kodingizni shunday o'zgartiring: `msg.content[0].text` o'rniga bloklar bo'ylab `for` bilan yurib, faqat `block.type === "text"` bo'lganlarini chop etsin. Nega bu usul ishonchliroq?
8. `max_tokens` ni `30` ga tushirib, uzun javob talab qiladigan so'rov bering (masalan "Node.js tarixini batafsil yoz"). `msg.stop_reason` qanday qiymat oladi va bu nimani anglatadi? Keyin uni `1024` ga oshirib, farqni tasvirlang.

### Qiyin

9. Kichik "savol-javob" skripti yozing: u so'rov matnini `process.argv` (buyruq qatori argumenti) dan olsin, masalan `node --env-file=.env soroq.js "Promise nima?"`. Javobni va sarflangan jami tokenlar sonini (`input_tokens + output_tokens`) chiqarsin. Argument berilmasa, foydalanish yo'riqnomasini ko'rsatsin.
10. Chaqiruvni `try/catch` ga o'rab, xato yuz berganda dastur yiqilmasin, balki tushunarli xabar chiqarsin (masalan, status kodni va qisqa tavsifni). Maslahat: SDK xatosida `err.status` (HTTP kod) bo'ladi. So'ng kalitni ataylab xato qilib, 401 ni tutib ko'ring.

<details markdown="1"><summary>Yechim — 1</summary>

Kalitni `.env` da saqlash xavfsizroq, chunki `.env` faylini `.gitignore` orqali Git e'tiboridan chiqaramiz — demak u repozitoriyga **hech qachon tushmaydi** va ochiq joyga (GitHub) chiqib ketmaydi. Kalit faqat sizning mashinangizda qoladi, kod esa uni ish vaqtida muhit o'zgaruvchisidan o'qiydi.

Kalitni kod ichiga yozsangiz, u kod bilan birga commit bo'lib, GitHub'ga chiqadi. Kalit GitHub'ga (yoki har qanday ochiq joyga) tushsa — **butun internetga ko'rinadi**. Maxsus botlar repozitoriylarni doimo skanlab, `sk-ant-...` kalitlarini bir necha daqiqada topadi va ishlatib yuboradi — hisobingizdan begona pul sarflanadi. Kalit sizib chiqqanini bilsangiz, uni darhol konsolda **bekor qilib** (revoke), yangisini yaratish kerak.

</details>

<details markdown="1"><summary>Yechim — 2</summary>

```bash
mkdir ai-loyiha
cd ai-loyiha
npm init -y
```

So'ng `package.json` faylini ochib, `"type": "module"` qatorini qo'shaman:

```json
{
  "name": "ai-loyiha",
  "version": "1.0.0",
  "type": "module"
}
```

Bu qadam zarur, chunki `@anthropic-ai/sdk` va kitobdagi barcha misollar ESM sintaksisidan (`import Anthropic from "..."`) foydalanadi. `"type": "module"` bo'lmasa, Node faylni eski CommonJS rejimida o'qishga urinadi va `import` so'zida xato beradi.

</details>

<details markdown="1"><summary>Yechim — 3</summary>

To'g'rilari: **(b)** va **(c)**.

- (a) noto'g'ri — `msg.content` satr emas, **massiv** (bloklar ro'yxati).
- (b) to'g'ri — bu massiv, chunki javob bir nechta blokli (matn, vosita chaqiruvi va h.k.) bo'lishi mumkin.
- (c) to'g'ri — bitta matn blokli javobda matn `msg.content[0].text` da turadi.
- (d) noto'g'ri — `msg.text` degan maydon yo'q; matnga `content` massivi orqali yetib borasiz.

Ishonchliroq usul — bloklar bo'ylab yurib, `block.type === "text"` ni tekshirish.

</details>

<details markdown="1"><summary>Yechim — 4</summary>

`--env-file=.env` — Node'ga (20.6-versiyadan boshlab) "dasturni ishga tushirishdan oldin `.env` faylidagi o'zgaruvchilarni o'qib, muhit o'zgaruvchilariga yuklab qo'y" deydi. Shu tufayli `process.env.ANTHROPIC_API_KEY` mavjud bo'ladi va `new Anthropic()` uni avtomatik topadi.

Bu qismni tushirib qoldirsangiz, `ANTHROPIC_API_KEY` yuklanmaydi, SDK kalit topa olmaydi va ehtimol **401** (Authentication) xatosi chiqadi. (Eski Node versiyalarida `--env-file` qo'llab-quvvatlanmaydi — u holda `npm i dotenv` o'rnatib, kodning eng boshiga `import "dotenv/config";` qo'shiladi.)

</details>

<details markdown="1"><summary>Yechim — 5</summary>

- **401** ↔ "kalit yo'q/noto'g'ri" — autentifikatsiya muvaffaqiyatsiz. Kalit yuklanmagan, xato yozilgan yoki bekor qilingan.
- **404** ↔ "model nomida xato" — so'ralgan resurs topilmadi; odatda `model` qiymati noto'g'ri yozilgan (`claude-opus-4-8` ni tekshiring).
- **400** ↔ "so'rov noto'g'ri tuzilgan" — masalan, majburiy `max_tokens` berilmagan, `messages` bo'sh, yoki maydon nomi `camelCase` (`maxTokens`) yozilgan.

</details>

<details markdown="1"><summary>Yechim — 6</summary>

```js
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Node.js va brauzer JavaScript'i o'rtasidagi asosiy farq nima?" },
  ],
});

console.log("Javob:", msg.content[0].text);
console.log("To'xtash sababi:", msg.stop_reason);
console.log("Token sarfi:", msg.usage);
```

```bash
node --env-file=.env app.js
```

```text
Javob: Node.js — brauzerdan tashqarida (server/terminal) ishlaydi va ...
To'xtash sababi: end_turn
Token sarfi: { input_tokens: 20, output_tokens: 88, ... }
```

`stop_reason: "end_turn"` — Claude javobini tabiiy yakunladi. `usage` esa bu chaqiruv qancha tokenga tushganini ko'rsatadi.

</details>

<details markdown="1"><summary>Yechim — 7</summary>

```js
for (const block of msg.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

Bu usul ishonchliroq, chunki `msg.content` — **massiv**, va u kelajakda bir nechta blokli bo'lishi mumkin: matn bloklari, vosita chaqiruvi (`tool_use`) bloklari va boshqalar. `msg.content[0].text` faqat birinchi element matn bo'lganda ishlaydi; agar birinchi blok matn bo'lmasa (masalan vosita chaqiruvi), `content[0].text` `undefined` bo'lib qoladi. Bloklar bo'ylab yurib, `block.type === "text"` ni tekshirsangiz — faqat haqiqiy matn bloklarini olasiz va kod hech qachon adashmaydi.

</details>

<details markdown="1"><summary>Yechim — 8</summary>

```js
const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 30,
  messages: [{ role: "user", content: "Node.js tarixini batafsil yoz." }],
});
console.log(msg.content[0].text);
console.log("Sabab:", msg.stop_reason);
```

`max_tokens: 30` bo'lgani uchun javob 30 token chiqarilgach **majburan to'xtaydi**, va `msg.stop_reason` qiymati **`"max_tokens"`** bo'ladi. Bu — "javob tugamadi, men chegaraga yetib kesib qo'ydim" degani; matn jumla o'rtasida uzilib qolishi mumkin.

`max_tokens` ni `1024` ga oshirsangiz, model fikrini to'liq aytishga ulguradi va `stop_reason` odatda **`"end_turn"`** ga aylanadi — javob tabiiy yakunlangan. Demak `max_tokens` — javob uzunligi (va narx) tomi; uni mavzuga yetarli darajada qo'yish kerak.

</details>

<details markdown="1"><summary>Yechim — 9</summary>

```js
// soroq.js
import Anthropic from "@anthropic-ai/sdk";

const soroq = process.argv.slice(2).join(" ");

if (!soroq) {
  console.log('Foydalanish: node --env-file=.env soroq.js "savolingiz"');
  process.exit(1);
}

const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  messages: [{ role: "user", content: soroq }],
});

console.log(msg.content[0].text);

const jami = msg.usage.input_tokens + msg.usage.output_tokens;
console.log(`\n[Jami ${jami} token: ${msg.usage.input_tokens} kirish + ${msg.usage.output_tokens} chiqish]`);
```

```bash
node --env-file=.env soroq.js "Promise nima?"
# Promise — JavaScript'da kelajakda bajariladigan ...
# [Jami 95 token: 12 kirish + 83 chiqish]

node --env-file=.env soroq.js
# Foydalanish: node --env-file=.env soroq.js "savolingiz"
```

`process.argv.slice(2)` bilan buyruq qatori argumentlarini olamiz (`slice(2)` — Node va skript yo'lini kesib tashlaydi), `join(" ")` bilan bitta matnga birlashtiramiz. Argument bo'sh bo'lsa, yo'riqnoma ko'rsatib `process.exit(1)` bilan chiqamiz. Jami tokenni `input_tokens + output_tokens` dan hisoblaymiz — bu chaqiruv narxiga to'g'ridan-to'g'ri bog'liq.

</details>

<details markdown="1"><summary>Yechim — 10</summary>

```js
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

try {
  const msg = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Salom!" }],
  });
  console.log(msg.content[0].text);
} catch (err) {
  if (err.status === 401) {
    console.error("Xato 401: kalit noto'g'ri yoki topilmadi. .env va --env-file ni tekshiring.");
  } else if (err.status === 404) {
    console.error("Xato 404: model nomi noto'g'ri bo'lishi mumkin.");
  } else if (err.status === 400) {
    console.error("Xato 400: so'rov noto'g'ri tuzilgan.", err.message);
  } else {
    console.error("Kutilmagan xato:", err.status ?? "", err.message);
  }
}
```

`try/catch` xatoni tutadi — endi dastur yiqilmaydi, balki tushunarli xabar chiqaradi. SDK xatosida `err.status` HTTP status kodini, `err.message` esa tafsilotni beradi. Kalitni `.env` da ataylab buzib (yoki `--env-file` ni tushirib) ishga tushiring — `Xato 401: ...` xabarini ko'rasiz. Bu — ishonchli ilovaning birinchi qadami; retry, timeout va tipli xatolarni keyingi qismlarda to'liq ochamiz.

</details>

---

[⬅️ Oldingi: 01 — LLM nima va qanday ishlaydi](./01-llm-nima.md) · [🏠 README](./README.md) · [Keyingi: 03 — Messages API chuqur ➡️](./03-messages-api.md)
