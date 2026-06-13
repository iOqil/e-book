# Telegram bot (Python aiogram) — 0 dan Expertgacha

Bu kitob **Python asoslarini biladigan** o'quvchini Telegram bot yozish bo'yicha noldan ishonchli darajaga olib chiqadi. Oddiy echo botdan boshlab — handler va Router, filtrlar, klaviaturalar, callback, **FSM (holatlar mashinasi)**, middleware, ma'lumotlar bazasi, to'lovlar, webhook va deploy orqali — yakuniy to'liq botgacha; so'ng **real amaliyot**: guruh/kanal boshqaruvi, **majburiy obuna**, Telegram **Mini App** integratsiyasi va **Hamster uslubidagi clicker o'yin** kapstoni. Hamma kod **aiogram 3.x** (zamonaviy, async) bilan yoziladi.

> 🤖 **aiogram 3.x.** Bu kitob faqat **aiogram 3.x** idiomidan foydalanadi (`Router`, `@router.message`, `Dispatcher`, `F` magic-filtr, `DefaultBotProperties`). Internetdagi eski 2.x misollar (`@dp.message_handler`, `executor.start_polling`) bu yerda **ishlamaydi** — ehtiyot bo'ling.

> ⚠️ **HALOL eslatma.** Botning **mantig'i** — handlerlar, Router, filtrlar, FSM, klaviaturalar, callback, middleware va ma'lumotlar bazasi — **offline ishga tushirib tekshirilgan** (mock `Update` ni dispatcher'ga uzatib). Ammo **jonli ishlash** — Telegram'ga polling/xabar yuborish, webhook qabul qilish, to'lovlar — `@BotFather` dan olingan **token** va **internet** talab qiladi; bu bloklar to'g'ri, lekin matnda "illustrativ" deb belgilangan. Botingizni o'z tokeningiz bilan ishga tushiring.

> ℹ️ Bu kitob siz **Python asoslarini** (async/await, dekorator, sinf, virtual muhit, `pip`, type hints) bilasiz deb hisoblaydi. Python yangi bo'lsa, avval [Python — 0 dan Expertgacha](../python/README.md) kitobini o'qing.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. `@BotFather` dan token oling (`/newbot`) va uni `.env` (`BOT_TOKEN`) da saqlang — hech qachon kodga yozmang.
3. Har bir misolni o'zingiz tering va o'z botingizda sinab ko'ring — bot o'qib emas, **yozib** o'rganiladi.
4. FSM, middleware va DB kabi mavzular amaliyotsiz mavhum tuyuladi — har bir handlerni o'zingiz ishga tushiring.

## Talab

| Kerak | Daraja |
|---|---|
| Python asoslari (async/await, sinf, dekorator) | **Shart** |
| Python 3.11+ va `pip` | Shart |
| Telegram hisobi va `@BotFather` token | Shart (jonli sinov uchun) |
| Terminal va virtual muhit bilan tanishlik | Foydali |
| SQL/ma'lumotlar bazasi asoslari | Foydali |

---

## Mundarija

### I qism — Asoslar

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Telegram botlar va aiogram bilan tanishuv](./01-telegram-aiogram-tanishuv.md) | Bot nima, Bot API qanday ishlaydi, `@BotFather` token, polling vs webhook, aiogram nega va 3.x. |
| 02 | [Birinchi bot: echo va /start](./02-birinchi-bot.md) | Minimal bot: Bot + Dispatcher + Router, `/start`, echo, `start_polling`, token `.env` da. |
| 03 | [Handlerlar va Router](./03-handlerlar-router.md) | Message handler, `Router` bilan modullash, `include_router`, update turlari, handler tartibi. |
| 04 | [Filtrlar va buyruqlar](./04-filtrlar-buyruqlar.md) | `Command`/`CommandStart`, deep-link, `F` magic-filtr, maxsus filtr, content_type. |

### II qism — Foydalanuvchi bilan muloqot

| # | Bob | Mavzu |
|---|---|---|
| 05 | [Xabar yuborish, formatlash va media](./05-xabar-formatlash-media.md) | `answer`/`reply`, parse_mode (HTML/MarkdownV2), media (rasm/hujjat/audio), albom. |
| 06 | [Klaviaturalar: reply va inline](./06-klaviaturalar.md) | `ReplyKeyboardBuilder`, `InlineKeyboardBuilder`, callback tugmalar, `adjust`, klaviaturani o'chirish. |
| 07 | [Callback query va inline rejim](./07-callback-inline.md) | `callback_query`, `CallbackData` factory, xabarni tahrirlash, pagination, inline mode. |
| 08 | [FSM — holatlar mashinasi](./08-fsm-holatlar.md) | `StatesGroup`/`State`, `FSMContext`, `MemoryStorage`, ko'p qadamli forma, holatdan chiqish. |

### III qism — Arxitektura va ma'lumot

| # | Bob | Mavzu |
|---|---|---|
| 09 | [Middleware](./09-middleware.md) | Outer vs inner middleware, `BaseMiddleware`, ma'lumot in'ektsiyasi, throttling, logging. |
| 10 | [Ma'lumotlar bazasi bilan ishlash](./10-malumotlar-bazasi.md) | aiosqlite / SQLAlchemy 2.0 (async), foydalanuvchilarni saqlash, repository, DB middleware. |
| 11 | [Loyiha tuzilishi va konfiguratsiya](./11-loyiha-tuzilishi.md) | Katta botni modullash (handlers/keyboards/states/services), `.env` config, DI. |
| 12 | [Maxsus xususiyatlar](./12-maxsus-xususiyatlar.md) | Fayl yuklab olish, media guruh, lokatsiya/kontakt, buyruqlar menyusi, WebApp tugma. |

### IV qism — Ilg'or

| # | Bob | Mavzu |
|---|---|---|
| 13 | [Webhook va aiohttp server](./13-webhook-deploy.md) | Polling vs webhook chuqur, aiohttp webhook server, `set_webhook`, nginx, qachon qaysi. |
| 14 | [To'lovlar va Telegram Stars](./14-tolovlar-stars.md) | `send_invoice`, `pre_checkout_query`, `successful_payment`, provider token, Telegram Stars (XTR). |
| 15 | [Rejalashtirilgan vazifalar va broadcast](./15-rejalashtirilgan-broadcast.md) | APScheduler/asyncio bilan rejali xabar, ommaviy tarqatish, flood-control, `TelegramRetryAfter`. |

### V qism — Sifat va deploy

| # | Bob | Mavzu |
|---|---|---|
| 16 | [Testlash va xatolarni boshqarish](./16-testlash-xatolar.md) | Handlerlarni offline test (pytest-asyncio + `feed_update`), error handler, logging, debug. |
| 17 | [Production va deploy](./17-production-deploy.md) | VPS, Docker, systemd/supervisor, `.env`/sirlar, polling vs webhook prod, graceful shutdown. |
| 18 | [Yakuniy kapston: to'liq bot](./18-kapston.md) | Boshidan oxirigacha to'liq bot: FSM forma, DB, klaviatura, middleware, admin, deploy. Yo'l yakuni. |

### VI qism — Guruh, kanal va Mini App (real amaliyot)

| # | Bob | Mavzu |
|---|---|---|
| 19 | [Guruhlarda ishlash](./19-guruhlar.md) | Guruh turlari, privacy mode, `get_chat_member` bilan a'zo/admin tekshirish, `my_chat_member`. |
| 20 | [Guruh moderatsiyasi](./20-guruh-moderatsiya.md) | Welcome (`chat_member` JOIN), ban/kick/mute (`restrict_chat_member` + `ChatPermissions`), admin-filtr, captcha. |
| 21 | [Kanallar bilan ishlash](./21-kanallar.md) | Kanalga post, `channel_post`, linked discussion group, `forward`/`copy`, reaksiyalar. |
| 22 | [Majburiy obuna](./22-majburiy-obuna.md) | Obuna middleware, gate klaviatura, bir nechta kanal, private kanal (`chat_join_request`), kesh. |
| 23 | [Telegram Web App (Mini App) asoslari](./23-webapp-asoslari.md) | `WebAppInfo`, 3 tugma turi, `telegram-web-app.js` SDK, `sendData` → `F.web_app_data`. |
| 24 | [Web App xavfsizligi: initData](./24-webapp-xavfsizlik.md) | initData HMAC validatsiya, `check_webapp_signature`, replay himoyasi, serverda tekshirish. |
| 25 | [Mini App backend](./25-miniapp-backend.md) | aiohttp backend, har so'rovda initData auth, DB holat, bot↔WebApp↔backend uchburchagi. |
| 26 | [Kapston: Hamster uslubidagi clicker Mini App](./26-kapston-clicker.md) | Tap-to-earn: balans/energiya/upgrade, anti-cheat (serverda hisoblanadi), to'liq loyiha. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
