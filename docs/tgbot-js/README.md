# Telegram bot (JavaScript / grammY) — 0 dan Expertgacha

Bu kitob **JavaScript va Node.js asoslarini biladigan** o'quvchini Telegram bot yozish bo'yicha noldan ishonchli darajaga olib chiqadi. Oddiy echo botdan boshlab — handler va Composer, filtrlar (filter queries), klaviaturalar, callback, **conversations (suhbatlar)**, middleware, sessiya va ma'lumotlar bazasi, to'lovlar, webhook va deploy orqali — yakuniy to'liq botgacha; so'ng **real amaliyot**: guruh/kanal boshqaruvi, **majburiy obuna**, Telegram **Mini App** integratsiyasi va **Hamster uslubidagi clicker o'yin** kapstoni. Hamma kod **grammY 1.x** (zamonaviy, ESM, `async/await`) bilan yoziladi.

> 🤖 **grammY 1.x.** Bu kitob faqat **grammY** idiomidan foydalanadi (`Bot`, `bot.command`, `bot.on("message:text")` filter query, `Composer`, `InlineKeyboard`/`Keyboard` quruvchilari, `@grammyjs/conversations` v2 plugini). Internetdagi **Telegraf** (`ctx.scene`, `bot.on("text")`) yoki **node-telegram-bot-api** misollari bu yerda **ishlamaydi** — grammY API'si boshqacha, ehtiyot bo'ling.

> ⚠️ **HALOL eslatma.** Botning **mantig'i** — handlerlar, Composer, filter query'lar, conversations, klaviaturalar, callback, middleware va sessiya — **offline ishga tushirib tekshirilgan** (soxta `Update` ni `bot.handleUpdate` ga uzatib va API chaqiruvlarini transformer bilan ushlab). Ammo **jonli ishlash** — Telegram'ga polling/xabar yuborish, webhook qabul qilish, to'lovlar — `@BotFather` dan olingan **token** va **internet** talab qiladi; bu bloklar to'g'ri, lekin matnda "illustrativ" deb belgilangan. Botingizni o'z tokeningiz bilan ishga tushiring.

> ℹ️ Bu kitob siz **JavaScript va Node.js asoslarini** (`async/await`, `Promise`, ESM `import`, `npm`, obyekt/massiv) bilasiz deb hisoblaydi. JS/Node yangi bo'lsa, avval [JavaScript — 0 dan Expertgacha](../js/README.md) va [Node.js — 0 dan Expertgacha](../nodejs/README.md) kitoblarini o'qing.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. `@BotFather` dan token oling (`/newbot`) va uni `.env` (`BOT_TOKEN`) da saqlang — hech qachon kodga yozmang.
3. Har bir misolni o'zingiz tering va o'z botingizda sinab ko'ring — bot o'qib emas, **yozib** o'rganiladi.
4. conversations, middleware va DB kabi mavzular amaliyotsiz mavhum tuyuladi — har bir handlerni o'zingiz ishga tushiring.

## Talab

| Kerak | Daraja |
|---|---|
| JavaScript asoslari (`async/await`, `Promise`, ESM) | **Shart** |
| Node.js 18+ va `npm` | Shart |
| Telegram hisobi va `@BotFather` token | Shart (jonli sinov uchun) |
| Terminal bilan tanishlik | Foydali |
| SQL/ma'lumotlar bazasi asoslari | Foydali |

---

## Mundarija

### I qism — Asoslar

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Telegram botlar va grammY bilan tanishuv](./01-telegram-grammy-tanishuv.md) | Bot nima, Bot API qanday ishlaydi, `@BotFather` token, polling vs webhook, grammY nega va Telegraf'dan farqi. |
| 02 | [Birinchi bot: echo va /start](./02-birinchi-bot.md) | Minimal bot: `new Bot`, `bot.command`, `bot.on`, `bot.start()`, token `.env` da, `ctx.reply`. |
| 03 | [Update'lar, handlerlar va Composer](./03-handlerlar-composer.md) | `ctx` obyekti, `bot.use`, `Composer` bilan modullash, `next()`, handler tartibi, middleware daraxti. |
| 04 | [Filtrlar va buyruqlar (filter queries)](./04-filtrlar-buyruqlar.md) | `bot.command`, deep-link payload, `bot.hears`, filter query (`message:text`, `:photo`), maxsus filtr (`bot.filter`). |

### II qism — Foydalanuvchi bilan muloqot

| # | Bob | Mavzu |
|---|---|---|
| 05 | [Xabar yuborish, formatlash va media](./05-xabar-formatlash-media.md) | `ctx.reply`/`reply_parameters`, parse_mode (HTML/MarkdownV2), `InputFile`, media (rasm/hujjat/audio), albom. |
| 06 | [Klaviaturalar: reply va inline](./06-klaviaturalar.md) | `Keyboard`, `InlineKeyboard` quruvchilari, callback tugmalar, `.resized()`/`.oneTime()`, klaviaturani olib tashlash. |
| 07 | [Callback query va inline rejim](./07-callback-inline.md) | `bot.callbackQuery`, `ctx.answerCallbackQuery`, xabarni tahrirlash, pagination, `bot.inlineQuery`. |
| 08 | [Conversations — suhbatlar (ko'p qadamli forma)](./08-conversations.md) | `@grammyjs/conversations` v2, `createConversation`, `conversation.wait`/`waitFor`, `conversation.external`, `conversation.form`. |

### III qism — Arxitektura va ma'lumot

| # | Bob | Mavzu |
|---|---|---|
| 09 | [Middleware va Composer daraxti](./09-middleware.md) | `bot.use`, `next()`, o'tish/to'xtatish, `Composer`, `bot.errorBoundary`, throttling, logging. |
| 10 | [Sessiya va ma'lumotlar bazasi](./10-sessiya-malumotlar-bazasi.md) | `session()` middleware, storage adapter (file/DB), `better-sqlite3`, foydalanuvchilarni saqlash, repository. |
| 11 | [Loyiha tuzilishi va konfiguratsiya](./11-loyiha-tuzilishi.md) | Katta botni modullash (handlers/keyboards/conversations/services), `.env` config, context flavor. |
| 12 | [Maxsus xususiyatlar va plaginlar](./12-maxsus-xususiyatlar.md) | Fayl yuklab olish (`getFile`/`download`), `@grammyjs/menu`, buyruqlar menyusi, `@grammyjs/hydrate`, WebApp tugma. |

### IV qism — Ilg'or

| # | Bob | Mavzu |
|---|---|---|
| 13 | [Webhook va deploy server](./13-webhook.md) | Polling vs webhook chuqur, `webhookCallback`, Express/Hono server, `bot.api.setWebhook`, qachon qaysi. |
| 14 | [To'lovlar va Telegram Stars](./14-tolovlar-stars.md) | `replyWithInvoice`, `pre_checkout_query`, `successful_payment`, provider token, Telegram Stars (XTR). |
| 15 | [Rejalashtirilgan vazifalar va broadcast](./15-rejalashtirilgan-broadcast.md) | `node-cron` bilan rejali xabar, `@grammyjs/runner` bilan konkurensiya, ommaviy tarqatish, flood-control, `@grammyjs/auto-retry`. |

### V qism — Sifat va deploy

| # | Bob | Mavzu |
|---|---|---|
| 16 | [Testlash va xatolarni boshqarish](./16-testlash-xatolar.md) | Handlerlarni offline test (`handleUpdate` + transformer mock), Vitest, `bot.catch`, `GrammyError`/`HttpError`. |
| 17 | [Production va deploy](./17-production-deploy.md) | VPS, Docker, pm2/systemd, `@grammyjs/runner`, sirlar/.env, polling vs webhook prod, graceful shutdown. |
| 18 | [Yakuniy kapston: to'liq bot](./18-kapston.md) | Boshidan oxirigacha to'liq bot: conversation forma, sessiya/DB, klaviatura, middleware, admin, deploy. Yo'l yakuni. |

### VI qism — Guruh, kanal va Mini App (real amaliyot)

| # | Bob | Mavzu |
|---|---|---|
| 19 | [Guruhlarda ishlash](./19-guruhlar.md) | Guruh turlari, privacy mode, `getChatMember` bilan a'zo/admin tekshirish, `my_chat_member`, `bot.chatType`. |
| 20 | [Guruh moderatsiyasi](./20-guruh-moderatsiya.md) | Welcome (`chat_member`), ban/kick/mute (`banChatMember`/`restrictChatMember` + `ChatPermissions`), admin-filtr, captcha. |
| 21 | [Kanallar bilan ishlash](./21-kanallar.md) | Kanalga post, `channel_post`, linked discussion group, `forwardMessage`/`copyMessage`, reaksiyalar (`bot.reaction`). |
| 22 | [Majburiy obuna](./22-majburiy-obuna.md) | Obuna middleware, gate klaviatura, bir nechta kanal, private kanal (`chat_join_request`), kesh. |
| 23 | [Telegram Web App (Mini App) asoslari](./23-webapp-asoslari.md) | `WebAppInfo`, 3 tugma turi, `telegram-web-app.js` SDK, `sendData` → `bot.on("message:web_app_data")`. |
| 24 | [Web App xavfsizligi: initData](./24-webapp-xavfsizlik.md) | initData HMAC validatsiya (Node `crypto`), `data_check_string`, replay himoyasi, serverda tekshirish. |
| 25 | [Mini App backend](./25-miniapp-backend.md) | Hono/Express backend, har so'rovda initData auth, DB holat, bot↔WebApp↔backend uchburchagi. |
| 26 | [Kapston: Hamster uslubidagi clicker Mini App](./26-kapston-clicker.md) | Tap-to-earn: balans/energiya/upgrade, anti-cheat (serverda hisoblanadi), to'liq loyiha. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
