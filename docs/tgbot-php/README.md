# Telegram bot (PHP / Nutgram) — 0 dan Expertgacha

Bu kitob **PHP biladigan** dasturchini Telegram bot yozish bo'yicha noldan ekspert darajaga olib chiqadi. Oddiy echo botdan boshlab — handler va routing, filtrlar, klaviaturalar, callback, **conversations (suhbat / FSM)**, middleware, ma'lumotlar bazasi, to'lovlar, webhook va deploy orqali — to'liq botgacha; so'ng **real amaliyot**: guruh/kanal boshqaruvi, **majburiy obuna**, Telegram **Mini App** integratsiyasi va **Hamster uslubidagi clicker o'yin** kapstoni. Hamma kod **Nutgram 4.x** freymvorki bilan yoziladi.

> 🤖 **Nutgram.** Bu kitob [Nutgram](https://nutgram.dev) (zamonaviy PHP 8 Telegram bot freymvorki) dan foydalanadi: fluent handlerlar, conversations, middleware, klaviatura quruvchilar va **`FakeNutgram`** — tokensiz, tarmoqsiz test vositasi.

> ⚠️ **HALOL eslatma.** Botning **mantig'i** — handlerlar, conversations, middleware, klaviaturalar, callback va ma'lumotlar bazasi — **offline ishga tushirib tekshirilgan** (`Nutgram::fake()` + PHPUnit, mock update'lar bilan). Ammo **jonli ishlash** — Telegram'ga polling/xabar yuborish, webhook, to'lovlar, guruhda ban — `@BotFather` dan olingan **token** va **internet** (Mini App uchun HTTPS hosting) talab qiladi; bu bloklar to'g'ri, lekin matnda "illustrativ" deb belgilangan.

> ℹ️ Bu kitob siz **PHP asoslarini** (sinf, namespace, composer, closure, type hints, PDO) bilasiz deb hisoblaydi. PHP yangi bo'lsa, avval [PHP qo'llanmasi](../php/README.md)ni o'qing. Chuqurroq mavzular uchun [PHP Expert](../php-expert/README.md) treki bor.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. `@BotFather` dan token oling (`/newbot`) va uni `.env` da saqlang — hech qachon kodga yozmang.
3. Har bir misolni o'zingiz tering. Bot o'qib emas, **yozib** o'rganiladi.
4. `FakeNutgram` bilan testlarni o'zingiz ishga tushiring — botni Telegram'siz sinash ekspert ko'nikmasi.

## Talab

| Kerak | Daraja |
|---|---|
| PHP asoslari (sinf, composer, closure) | **Shart** |
| PHP 8.2+ va Composer | Shart |
| Telegram hisobi va `@BotFather` token | Shart (jonli sinov uchun) |
| Terminal bilan tanishlik | Foydali |
| SQL/ma'lumotlar bazasi asoslari | Foydali |

---

## Mundarija

### I qism — Asoslar

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Telegram bot va Nutgram bilan tanishuv](./01-nutgram-tanishuv.md) | Bot API, `@BotFather` token, Nutgram nega, `composer require`, polling vs webhook. |
| 02 | [Birinchi bot: /start va echo](./02-birinchi-bot.md) | `new Nutgram($token)`, `onCommand`, `sendMessage`, echo, `$bot->run()`, token `.env`. |
| 03 | [Handlerlar va routing](./03-handlerlar-routing.md) | `onMessage`/`onCommand`/`onText`/`onCallbackQuery`, handler tartibi, `fallback`, accessorlar. |
| 04 | [Filtrlar va buyruqlar](./04-filtrlar-buyruqlar.md) | Parametrli buyruqlar, deep-link, `onText` regex, constraints, `setMyCommands`. |

### II qism — Foydalanuvchi bilan muloqot

| # | Bob | Mavzu |
|---|---|---|
| 05 | [Xabar yuborish, formatlash va media](./05-xabar-formatlash-media.md) | `parse_mode` (HTML/MarkdownV2), escape, `sendPhoto`/`sendDocument`, media-group. |
| 06 | [Klaviaturalar: reply va inline](./06-klaviaturalar.md) | `ReplyKeyboardMarkup`, `InlineKeyboardMarkup`, builder, `InlineMenu`. |
| 07 | [Callback query va inline rejim](./07-callback-inline.md) | `onCallbackQueryData`, `answerCallbackQuery`, `editMessageText`, pagination, inline mode. |
| 08 | [Conversations (suhbat / FSM)](./08-conversations.md) | `Conversation` klassi, `next`/`end`, ko'p qadamli forma, holatni saqlash, `/cancel`. |

### III qism — Arxitektura va ma'lumot

| # | Bob | Mavzu |
|---|---|---|
| 09 | [Middleware](./09-middleware.md) | Onion modeli, global/guruh/handler darajasi, throttling, ma'lumot ulashish. |
| 10 | [Ma'lumotlar bazasi bilan ishlash](./10-malumotlar-bazasi.md) | PDO (SQLite/MySQL), repository, foydalanuvchini upsert, DI orqali ulash. |
| 11 | [Loyiha tuzilishi va konfiguratsiya](./11-loyiha-tuzilishi.md) | Modullash, PSR-4 autoload, `.env`, DI-konteyner, bootstrap. |
| 12 | [Maxsus xususiyatlar](./12-maxsus-xususiyatlar.md) | Fayl yuklab olish, media group, lokatsiya/kontakt, buyruqlar menyusi. |

### IV qism — Ilg'or

| # | Bob | Mavzu |
|---|---|---|
| 13 | [Webhook va running mode](./13-webhook-deploy.md) | Polling vs webhook, running mode'lar, `setWebhook`, `secret_token`, nginx+php-fpm. |
| 14 | [To'lovlar va Telegram Stars](./14-tolovlar-stars.md) | `sendInvoice`, `onPreCheckoutQuery`, `onSuccessfulPayment`, Telegram Stars (XTR). |
| 15 | [Rejalashtirilgan vazifalar va broadcast](./15-rejalashtirilgan-broadcast.md) | Cron, broadcast, `BulkMessenger`, flood-control (429 retry), bloklangan foydalanuvchi. |

### V qism — Sifat va deploy

| # | Bob | Mavzu |
|---|---|---|
| 16 | [Testlash (FakeNutgram)](./16-testlash.md) | `Nutgram::fake()`, `hearText->reply`, `assertReplyText`/`assertSequence`, PHPUnit/Pest. |
| 17 | [Production va deploy](./17-production-deploy.md) | Supervisor/systemd (polling), nginx+php-fpm (webhook), Docker, `onException`, monitoring. |
| 18 | [Yakuniy kapston: to'liq bot](./18-kapston.md) | Vazifa-menejer bot: conversation, DB, klaviatura, middleware, admin, testlar, deploy. |

### VI qism — Guruh, kanal va Mini App (real amaliyot)

| # | Bob | Mavzu |
|---|---|---|
| 19 | [Guruhlarda ishlash](./19-guruhlar.md) | Guruh turlari, privacy mode, `getChatMember` a'zo/admin, `onMyChatMember`. |
| 20 | [Guruh moderatsiyasi](./20-guruh-moderatsiya.md) | Welcome (`onChatMember`), ban/mute (`restrictChatMember` + `ChatPermissions`), captcha. |
| 21 | [Kanallar bilan ishlash](./21-kanallar.md) | Kanalga post, `onChannelPost`, linked discussion group, `forward`/`copy`, reaksiyalar. |
| 22 | [Majburiy obuna](./22-majburiy-obuna.md) | Obuna middleware, gate klaviatura, bir nechta kanal, yopiq kanal (`onChatJoinRequest`). |
| 23 | [Telegram Web App (Mini App) asoslari](./23-webapp-asoslari.md) | `WebAppInfo`, 3 tugma turi, `telegram-web-app.js` SDK, `sendData` → `onWebAppData`. |
| 24 | [Web App xavfsizligi: initData](./24-webapp-xavfsizlik.md) | initData HMAC validatsiya, `validateWebAppData`, replay himoyasi, serverda tekshirish. |
| 25 | [Mini App backend](./25-miniapp-backend.md) | PHP backend (router/Slim), har so'rovda initData auth, DB holat, bot↔WebApp↔backend uchburchagi. |
| 26 | [Kapston: Hamster uslubidagi clicker Mini App](./26-kapston-clicker.md) | Tap-to-earn: balans/energiya/upgrade, anti-cheat (serverda hisoblanadi), to'liq loyiha. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
