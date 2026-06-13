# Node.js — 0 dan Backend dasturchigacha (o'zbek tilida)

Bu kitob **JavaScript asoslarini biladigan** o'quvchini Node.js bo'yicha noldan ishonchli backend dasturchi darajasiga olib chiqadi. Brauzerdan tashqarida JavaScript ishga tushirishdan boshlab — modullar, npm, asinxronlik, event loop, fayl tizimi, streamlar, Express, **to'rt xil ma'lumotlar bazasi** (SQLite, MySQL, Prisma, MongoDB), autentifikatsiya, real-time, testlash, production va TypeScript orqali — to'liq production-darajali REST API kapstongacha. Har bir mavzu sodda tushuntirish, **Node 24 da haqiqiy ishga tushirib tekshirilgan** kod va amaliy "REAL KEYS" loyihalari bilan ochib beriladi.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan — Node arxitekturasi, event loop fazalari, microtask/macrotask navbati, stream pipe, Express oqimi, connection pool, JWT auth kabi tushunchalar ko'z bilan ko'rib o'rganiladi.

> **Qoida:** Node.js o'qib emas — **YOZIB** o'rganiladi. Har bir misolni o'zingiz tering va `node` bilan ishga tushiring. Xato chiqsa — aynan shu yerda haqiqiy o'rganish boshlanadi.

> ℹ️ Bu kitob siz JavaScript asoslarini (o'zgaruvchi, funksiya, obyekt, massiv, `async/await`) bilasiz deb hisoblaydi. JavaScript yangi bo'lsa, avval [JavaScript — 0 dan Expertgacha](../js/README.md) kitobini o'qing.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi, sakramang.
2. 01-bobda Node.js'ni o'rnatib, har bir misolni o'z kompyuteringizda `node` bilan sinang.
3. Har bobdagi **REAL KEYS** amaliy loyihalarni o'zingiz qaytadan yozing — ko'chirib qo'yish bilan Node.js o'rganilmaydi.
4. Diagrammalarga e'tibor bering: event loop va streamlar kabi mavzular ularsiz mavhum tuyuladi.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter (Windows / macOS / Linux) | Shart |
| Node.js (01-bobda o'rnatamiz, LTS yoki 24+ tavsiya) | Shart |
| JavaScript asoslari | **Shart** |
| Terminal bilan asosiy tanishlik | Foydali |
| Oldingi backend tajribasi | Shart emas |

---

## Mundarija

### I qism — Node bilan tanishuv

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Node.js nima va o'rnatish](./01-nodejs-nima.md) | Node.js — brauzerdan tashqarida JavaScript ishga tushiruvchi muhit (V8, libuv); asinxron "bloklamaydigan" tabiati, brauzer JS'dan farqi; o'rnatish, REPL va birinchi CLI skript. |
| 02 | [Modullar: CommonJS va ESM](./02-modullar.md) | Kodni modullarga bo'lish; CommonJS (`require`/`module.exports`) va ESM (`import`/`export`); fayl scope, modul kesh, `__dirname` vs `import.meta`, top-level await, modul resolution. |
| 03 | [npm va package.json](./03-npm.md) | npm va `package.json`; `npm install`, `node_modules`, `package-lock.json`; SemVer va `^`/`~`; npm scripts va npx bilan amaliy mini-loyiha. |
| 04 | [Node uchun zamonaviy JavaScript va globallar](./04-zamonaviy-js.md) | Node kontekstidagi kerakli zamonaviy JS (destructuring, spread, `?.`/`??`, arrow); Node globallari — `process` (argv/env), `Buffer`, `globalThis`, timerlar (`setImmediate`/`nextTick`), `structuredClone`, global `fetch`. |

### II qism — Asinxron Node

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 05 | [Event loop va non-blocking I/O](./05-event-loop.md) | Node bitta thread'da minglab so'rovni qanday eplaydi; bloklovchi vs non-bloklovchi; call stack, event loop fazalari, microtask vs macrotask navbati, `process.nextTick`, libuv thread pool. |
| 06 | [Asinxronlik: callback, Promise, async/await](./06-asinxron.md) | Asinxron evolyutsiya: error-first callback, callback hell, Promise, `util.promisify`, `fs/promises`, `async/await`; ketma-ket vs parallel, `Promise.all/allSettled/race/any`, top-level await. |
| 07 | [EventEmitter va hodisa-asoslangan dasturlash](./07-eventemitter.md) | Event-driven pattern; `node:events` va `EventEmitter` (`on`/`emit`/`once`/`off`), meros, `error` hodisasining maxsusligi, `maxListeners` va xotira oqishi; real buyurtma tizimi misoli. |

### III qism — Fayllar, oqimlar va tizim

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 08 | [Fayl tizimi (fs) va path](./08-fayl-tizimi.md) | `node:fs` ning uch yuzi (sync/callback/promise); o'qish/yozish/o'chirish/ko'chirish, papkalar, `stat`; `existsSync` tuzog'i; `node:path` va `import.meta.dirname`. |
| 09 | [Streams va Buffers](./09-streams-buffers.md) | Katta ma'lumot bilan samarali ishlash; Buffer (binar bayt); Stream (Readable/Writable/Duplex/Transform), `pipe`/`pipeline()`, backpressure, `zlib` gzip, qatorma-qator filtr. |
| 10 | [process, os, CLI va child_process](./10-process-cli.md) | `process` (argv, env, signallar, graceful shutdown); `os` moduli; `readline` bilan CLI; `child_process` (`exec`/`execFile`/`spawn`/`fork`) va shell injection xavfi. |
| 11 | [HTTP moduli: native server (sehrsiz)](./11-http-modul.md) | `node:http` bilan paketsiz veb-server; `createServer`, `req`/`res`, qo'lda routing, query string, statik fayl; native REST API — keyin Express bilan solishtiriladi. |

### IV qism — Express bilan veb

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 12 | [Express asoslari](./12-express-asoslari.md) | Eng mashhur framework Express.js; routing, route parametrlari/query, `express.json()` va `req.body`, `res.json/status`, `express.Router()`, statik fayllar; native bilan solishtirish. |
| 13 | [Middleware](./13-middleware.md) | Express'ning yuragi — middleware (`(req, res, next)`); `next()`, zanjir va tartib, besh turi, `req` ni boyitish, error-handling middleware, 404; amaliy auth + logger + error handler. |
| 14 | [REST API qurish](./14-rest-api.md) | To'liq RESTful API: resurs/verb semantikasi, CRUD, to'g'ri status kodlar (200/201/204/400/404/409/422), izchil JSON javob, pagination/filtering/sorting, versiyalash va qatlamlash (routes→controllers→services). |
| 15 | [Validatsiya va xato boshqaruvi](./15-validatsiya-xato.md) | **Zod** bilan kiruvchi ma'lumot validatsiyasi (schema, safeParse); validatsiya middleware; markaziy xato boshqaruvi — custom Error sinflari, error middleware, RFC 7807 Problem Details, dev vs prod. |

### V qism — Ma'lumotlar bazasi

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 16 | [SQLite (better-sqlite3)](./16-sqlite.md) | Node'da DB asoslari; serversiz embedded SQLite; prepared statements (SQL injection himoyasi), to'liq CRUD, transaction; vazifa API'ni haqiqiy bazaga ko'chirish. |
| 17 | [MySQL: mysql2, pool, tranzaksiya](./17-mysql.md) | Real DB server; `mysql2/promise`, **connection pool**, prepared `execute`, CRUD, `beginTransaction`/`commit`/`rollback`, `.env` config; haqiqiy MySQL serverga ulanish. |
| 18 | [Prisma ORM](./18-prisma.md) | Zamonaviy **type-safe ORM**; `schema.prisma`, `migrate`/`generate`, type-safe CRUD, relations (`include`/nested), `$transaction`, seed; sxemadan DB'gacha bitta tiplangan zanjir. |
| 19 | [MongoDB va Mongoose](./19-mongodb.md) | NoSQL document DB; Mongoose schema/model, CRUD va query operatorlari, `ref`+`populate` vs embedded, hooks (`pre('save')`), virtuals; SQL vs NoSQL qachon. |

### VI qism — Auth, xavfsizlik, real-time

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 20 | [Autentifikatsiya va avtorizatsiya](./20-auth.md) | **bcrypt** parol hash, **JWT** stateless auth (sign/verify, Bearer, refresh token), auth middleware (`req.user`), RBAC (admin/user) va resurs egaligi (IDOR oldini olish). |
| 21 | [Fayl yuklash, config va xavfsizlik](./21-xavfsizlik-config.md) | **multer** fayl yuklash (MIME/hajm tekshirish); `.env`/dotenv config va validatsiya; **helmet**, **CORS**, **rate limiting**, injection/XSS himoya — OWASP asoslari. |
| 22 | [Real-time: WebSocket va Socket.io](./22-realtime.md) | Server→mijoz push; WebSocket protokoli, `ws` paketi; **Socket.io** (rooms, broadcast, namespace, auto-reconnect); Express bilan integratsiya; real-time chat. |

### VII qism — Sifat va production

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 23 | [Testlash (Vitest + supertest)](./23-testlash.md) | Test turlari va piramidasi; **Vitest** (describe/it/expect, async, mocking); **supertest** bilan API integratsiya testi; sqlite `:memory:` test bazasi, coverage, TDD. |
| 24 | [Production: logging, performance, deploy](./24-production.md) | **pino** strukturali logging; graceful shutdown; **cluster** va **worker_threads** (ko'p yadro/CPU-bound); PM2, health check; **Docker** (multi-stage Dockerfile, compose); deploy. |
| 25 | [TypeScript va Node](./25-typescript-node.md) | TS'ni Node bilan sozlash: `tsconfig.json` (`NodeNext`/`strict`), `tsx`/`tsc`/Node 24 strip-types; typed Express (`Request` generikasi, `req.user` kengaytma), typed ENV, Prisma + TS. |
| 26 | [Yakuniy kapston: to'liq REST API loyiha](./26-kapston.md) | Butun kitobni bog'laydigan production-darajali REST API: qatlamli struktura, DB + JWT/RBAC + Zod + markaziy xato + logging + supertest test + Docker. "0 dan expertgacha" yo'lining yakuni. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
