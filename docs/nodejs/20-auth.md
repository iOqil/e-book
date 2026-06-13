# 20 — Autentifikatsiya va avtorizatsiya

[⬅️ Oldingi: 19 — MongoDB va Mongoose](./19-mongodb.md) · [🏠 README](./README.md) · [Keyingi: 21 — Fayl yuklash, config va xavfsizlik ➡️](./21-xavfsizlik-config.md)

> **Bu bobda:** Backend ilovasining eng nozik qismi — kim kirayotganini bilish va u nimaga ruxsatli ekanini hal qilishni o'rganamiz. Avval **autentifikatsiya** ("kimsan?") va **avtorizatsiya** ("nima qila olasan?") farqini aniq ajratamiz. So'ng **parol xavfsizligi** — nega parolni hech qachon ochiq saqlamaslik kerakligi, **bcrypt** bilan hash + salt, `compare`, va **cost factor** ni o'lchab ko'ramiz. Ro'yxatdan o'tish/kirish oqimini (register -> hash -> saqlash; login -> compare -> token) quramiz, **sessiya-asosli** (cookie) va **JWT-asosli stateless** auth ni solishtiramiz. `jsonwebtoken` bilan token **imzolash/tekshirish**, token tuzilishi (`header.payload.signature`), `Authorization: Bearer`, **access + refresh** tokenlar; **auth middleware** orqali `req.user` ni to'ldirish; **RBAC** (admin/user), `requireRole`/`requireAuth`, va **resurs egaligi** (IDOR oldini olish). Oxirida xavfsizlik (token qayerda saqlash, secret env'da, refresh rotation, qattiq algoritm). REAL KEYS: bcrypt + Prisma/SQLite + JWT bilan to'liq auth tizimini quramiz va `fetch` bilan **haqiqatan** sinaymiz. Hamma kod Node 24.12 da ishga tushirib tasdiqlangan.

---

## Autentifikatsiya va avtorizatsiya: ikki xil savol

Backend xavfsizligi ikkita alohida savolga javob beradi. Ularni adashtirish — xatolarning eng ko'p tarqalgan manbai, shuning uchun avvalo aniq ajratib olaylik:

| | **Autentifikatsiya** (authentication) | **Avtorizatsiya** (authorization) |
|---|---|---|
| Savol | **Kimsan?** | **Nima qila olasan?** |
| Maqsad | Foydalanuvchini tanish | Ruxsatni tekshirish |
| Misol | Email + parol bilan kirish | "Bu vazifa meniki, o'chira olamanmi?" |
| Natija (xatosi) | `401 Unauthorized` | `403 Forbidden` |
| Bizdagi qadam | `requireAuth` middleware | `requireRole`, egalik tekshiruvi |

Sodda taqqoslash: **autentifikatsiya** — bu binoga kirishda pasportingizni ko'rsatish ("siz haqiqatan Olimsiz"). **Avtorizatsiya** — bu pasportingiz to'g'ri bo'lsa ham, server xonasiga kirish kartangiz bor-yo'qligi ("Olim siz, lekin bu xonaga ruxsatingiz yo'q").

Diqqat qiling: avtorizatsiyadan **oldin** har doim autentifikatsiya keladi. Kim ekaningni bilmasdan turib, nima qila olishingni hal qilib bo'lmaydi. Shuning uchun route'larda tartib doimo: avval `requireAuth`, keyin `requireRole`.

HTTP holat kodlarining farqi ham shu ikki tushunchadan kelib chiqadi:

- **401 Unauthorized** — "men seni **tanimadim**" (token yo'q yoki yaroqsiz). Nomi chalkash, aslida "unauthenticated" degani.
- **403 Forbidden** — "men seni **taniyman**, lekin bu amalga **ruxsating yo'q**".

13-bobda ([middleware](./13-middleware.md)) biz `req.user` ni o'rnatuvchi va rolni tekshiruvchi middleware'larni soxta ma'lumot bilan yozgan edik. Endi shu sxemani haqiqiy parol heshlash va JWT bilan to'liq, ishlaydigan tizimga aylantiramiz.

---

## Parol xavfsizligi: nega ochiq saqlamaymiz

Tasavvur qiling, foydalanuvchilar jadvalini shunday yaratdingiz:

```js
// XATO — parol ochiq (plaintext) saqlanmoqda
await prisma.user.create({
  data: { email: "olim@x.uz", password: "qwerty123" }
});
```

Bu **falokat**. Sababini tushunaylik:

1. **Bazaga kim kirsa, hammaning paroli qo'lida.** Hacker bazani o'g'irlasa yoki ichkaridagi xodim ko'rsa — barcha parollar ochiq.
2. **Foydalanuvchilar parolni qayta ishlatadi.** Ko'pchilik bir xil parolni email, bank, ijtimoiy tarmoqda ishlatadi. Sizning bazangizdan chiqqan parol — ularning butun hayotiga kalit.
3. **Siz parolni bilishingiz shart emas.** Login uchun foydalanuvchi kiritgan parolni saqlangan bilan **solishtirish** kifoya — asl parolni qayta tiklash kerak emas.

Yechim: parolni **bir tomonlama** (one-way) funksiya orqali o'tkazib, natijasini saqlaymiz. Bu funksiya — **hash**. Hashdan asl parolni qaytarib bo'lmaydi (matematik jihatdan amalda imkonsiz).

### Salt nima va nega kerak

Oddiy hash (masalan, SHA-256) ham yetarli emas, chunki:

- Bir xil parol — bir xil hash. Demak ikki foydalanuvchining hashlari bir xil bo'lsa, parollari ham bir xil ekani ko'rinib turadi.
- Hujumchilar oldindan hisoblangan **rainbow table** (mashhur parollar va ularning hashlari ro'yxati) bilan tez topadi.

**Salt** — har bir parolga qo'shiladigan tasodifiy, noyob qator. U parol bilan birga hashlanadi va hash natijasi ichida saqlanadi. Natijada:

- Bir xil parol ham har xil salt tufayli **har xil hash** beradi.
- Rainbow table ishlamaydi — har bir parol uchun alohida hisoblash kerak.

### bcrypt: hash + salt + cost factor

**bcrypt** — parollar uchun maxsus yaratilgan, salt va sekinlikni o'ziga jamlagan algoritm. Uning kuchi — **ataylab sekin** ishlashida. Oddiy hash mikrosoniyada ishlaydi, demak hujumchi sekundiga milliardlab parolni sinab ko'ra oladi. bcrypt esa har bir hashni yuzlab millisoniyaga cho'zadi — bu odatiy login uchun sezilmaydi, lekin brute-force hujumni amalda imkonsiz qiladi.

Sekinlikni **cost factor** (yoki "rounds") boshqaradi: bu sonni 1 ga oshirish hisob-kitobni **2 baravar** ko'paytiradi. Mana shu mashinada (`node cost-demo.mjs`) o'lchangan haqiqiy vaqtlar:

```
cost 8:  16 ms
cost 10: 56 ms
cost 12: 224 ms
cost 14: 895 ms
```

> **Cost factor tanlovi:** Bugungi standart — **12**. Login ~200 ms davom etadi (foydalanuvchi sezmaydi), lekin hujumchi uchun bu juda qimmat. Apparat tezlashgani sayin (yillar o'tib) bu sonni oshirib borasiz. 8 — juda past, 14+ — sek, faqat alohida holatlar uchun.

Endi bcrypt'ni amalda ko'raylik (`node test-bcrypt.mjs` bilan ishga tushirildi):

```js
import bcrypt from "bcrypt";

const COST = 12;
const parol = "sirli-parol-123";

// Hash yaratish: salt avtomatik generatsiya qilinadi va natijaga kiritiladi
const hash = await bcrypt.hash(parol, COST);
console.log("hash:", hash);
console.log("uzunligi:", hash.length);

// Tekshirish: kiritilgan parolni saqlangan hash bilan solishtiramiz
console.log("to'g'ri parol:", await bcrypt.compare(parol, hash));
console.log("xato parol:  ", await bcrypt.compare("boshqa", hash));

// Bir xil parol -> har safar boshqa hash (salt har xil)
const hash2 = await bcrypt.hash(parol, COST);
console.log("ikki hash farqli:", hash !== hash2);
console.log("lekin ikkalasi ham mos:", await bcrypt.compare(parol, hash2));
```

Haqiqiy chiqish:

```
hash: $2b$12$09cfDRcRT6/0d59lBHixSei5XZ8kg5JJVPve9EiW4lpYWPA4S.xMi
uzunligi: 60
to'g'ri parol: true
xato parol:   false
ikki hash farqli: true
lekin ikkalasi ham mos: true
```

bcrypt hashning **tuzilishini** o'qib chiqaylik — `$2b$12$09cfDRcRT6/0d59lBHixSe...`:

| Qism | Qiymat | Ma'no |
|---|---|---|
| `$2b$` | algoritm versiyasi | bcrypt 2b |
| `12` | cost factor | siz bergan COST |
| `09cfDRcRT6/0d59lBHixSe` (22 belgi) | **salt** | tasodifiy, hash ichida |
| qolgani | hash natijasi | parolning shifri |

E'tibor bering: salt **hash ichida** saqlanadi. Demak `compare` paytida bazada alohida salt ustun saqlash shart emas — bcrypt hashning o'zidan salt va costni o'qib oladi, kiritilgan parolni xuddi shu salt bilan qayta hashlaydi va solishtiradi.

> **Eslatma — `compare` ni qo'lda yozmang.** Hech qachon `bcrypt.hash(kiritilgan) === saqlangan` deb solishtirmang — bu salt har xilligi sabab hech qachon teng chiqmaydi va string tenglik **timing attack** ga ochiq. Doimo `bcrypt.compare(...)` ishlating: u to'g'ri salt bilan hashlaydi va vaqt bo'yicha barqaror (constant-time) solishtiradi.

---

## Ro'yxatdan o'tish va kirish oqimi

Endi ikkita asosiy oqimni tushunaylik. Ular bir-birining oynadagi aksi kabi:

**Register (ro'yxatdan o'tish):**

```
email + parol keladi  ->  bcrypt.hash(parol)  ->  bazaga {email, hash} saqlanadi
```

**Login (kirish):**

```
email + parol keladi  ->  bazadan user topiladi  ->  bcrypt.compare(parol, user.hash)
                                                      mos bo'lsa -> TOKEN beriladi
```

Diqqat: register'da **hash qilamiz va saqlaymiz**, login'da **compare qilamiz va token beramiz**. Login muvaffaqiyatli bo'lgach foydalanuvchiga "kalit" — token beriladi, keyingi so'rovlarda u shu kalit bilan o'zini tanitadi. Token nima ekanini hozir ko'ramiz.

> **Bir muhim xavfsizlik nuancesi:** Login muvaffaqiyatsiz bo'lganda — foydalanuvchi yo'qmi yoki parol xatomi — **bir xil** javob qaytaring ("Email yoki parol noto'g'ri"). Agar "bunday email yo'q" va "parol xato" deb alohida aytsangiz, hujumchi qaysi emaillar ro'yxatdan o'tganini aniqlay oladi (user enumeration).

---

## Sessiya-asosli auth: qisqacha solishtirish

Token'larga o'tishdan oldin, an'anaviy yondashuvni — **sessiya-asosli** auth'ni bir ko'rib chiqaylik, chunki farqni bilish JWT tanlovini tushunarli qiladi.

Sessiyada login muvaffaqiyatli bo'lgach, **server** xotirasida (yoki Redis/bazada) bir yozuv yaratadi va unga noyob **session ID** beradi. Bu ID foydalanuvchiga **cookie** orqali yuboriladi. Keyingi so'rovlarda brauzer cookie'ni avtomatik jo'natadi, server esa ID bo'yicha o'z xotirasidan "bu kim" ekanini topadi.

```js
// Sessiya-asosli auth (express-session) — soddalashtirilgan ko'rinish
import session from "express-session";

app.use(session({
  secret: process.env.SESSION_SECRET, // cookie'ni imzolash uchun
  resave: false,
  saveUninitialized: false,
  cookie: { httpOnly: true, secure: true, maxAge: 1000 * 60 * 60 }, // 1 soat
}));

app.post("/login", async (req, res) => {
  // ... bcrypt.compare ...
  req.session.userId = user.id; // server sessiyaga yozadi
  res.json({ ok: true });        // session ID cookie sifatida ketadi
});

app.get("/me", (req, res) => {
  if (!req.session.userId) return res.status(401).json({ xato: "Kiring" });
  res.json({ userId: req.session.userId });
});
```

**Sessiya (stateful)** va **JWT (stateless)** ni solishtiraylik:

| | Sessiya (cookie + server xotira) | JWT (stateless token) |
|---|---|---|
| Holat qayerda | **Serverda** (har sessiya yozuvi) | **Tokenda** (server hech narsa saqlamaydi) |
| Logout | Oson — sessiyani o'chirasiz | Qiyin — token amal qilavradi (qora ro'yxat kerak) |
| Masshtablash | Bir nechta serverda umumiy do'kon (Redis) kerak | Har qanday server tokenni o'zi tekshiradi |
| Mobil/API uchun | Noqulay (cookie boshqaruvi) | Qulay (`Authorization` header) |
| Bekor qilish | Bir zumda | Token muddati tugaguncha amalda |

Qisqasi: **sessiya** an'anaviy server-rendered veb-saytlar uchun ajoyib, **JWT** esa zamonaviy API'lar, mobil ilovalar va mikroservislar uchun qulay. Bu bobda asosiy e'tiborni JWT'ga qaratamiz, lekin ikkalasi ham to'g'ri tanlov bo'lishi mumkin — kontekstga bog'liq.

---

## JWT: stateless auth

**JWT** (JSON Web Token) — imzolangan, o'zini-o'zi ifodalovchi token. "Stateless" (holatsiz) deyilishining sababi: server token ichidagi ma'lumotga **ishonadi**, chunki u imzolangan — bazaga murojaat qilmasdan "bu kim" ekanini biladi.

### Token tuzilishi: header.payload.signature

JWT — nuqta bilan ajratilgan uch qismdan iborat string. Buni amalda ochib ko'raylik (`node jwt-demo.mjs`):

```js
import jwt from "jsonwebtoken";

const secret = "mening-sirim";
const token = jwt.sign({ sub: 42, role: "admin" }, secret, { expiresIn: "1h" });
console.log("Token:\n" + token);

const [h, p, s] = token.split(".");
console.log("Qismlar soni:", token.split(".").length);
console.log("header :", Buffer.from(h, "base64url").toString());
console.log("payload:", Buffer.from(p, "base64url").toString());
console.log("verify:", jwt.verify(token, secret));
```

Haqiqiy chiqish:

```
Token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQyLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3ODEyNTE0MjksImV4cCI6MTc4MTI1NTAyOX0.mHWFT_ugbjlAUxUVFUFfewOlodzsIUdQEv87Nn8Ai_8

Qismlar soni: 3
header : {"alg":"HS256","typ":"JWT"}
payload: {"sub":42,"role":"admin","iat":1781251429,"exp":1781255029}
verify: { sub: 42, role: 'admin', iat: 1781251429, exp: 1781255029 }
```

Uch qismni tushunaylik:

1. **Header** — `{"alg":"HS256","typ":"JWT"}` — qaysi algoritm bilan imzolanganini aytadi.
2. **Payload** — `{"sub":42,"role":"admin","iat":...,"exp":...}` — foydali ma'lumot ("claims"). `sub` = foydalanuvchi ID, `iat` = berilgan vaqt, `exp` = tugash vaqti. Bu yerga rol kabi kerakli ma'lumotni qo'yamiz.
3. **Signature** — secret yordamida header va payloaddan hisoblangan imzo.

> **JUDA MUHIM:** Header va payload shunchaki **base64url** bilan kodlangan — ular **shifrlanmagan**. Yuqorida ularni oddiy `Buffer.from(...).toString()` bilan o'qib oldik! Demak JWT ichiga **hech qachon parol, kredit karta yoki maxfiy ma'lumot qo'ymang** — har kim o'qiy oladi. JWT'ning kuchi maxfiylikda emas, **buzilmaslikda**: payloadni o'zgartirsangiz, imzo mos kelmaydi va `verify` rad etadi.

### Imzo nima uchun kerak: buzib ko'ramiz

Imzo — JWT'ning butun himoyasi. Uni sinab ko'raylik (xuddi shu `jwt-demo.mjs` chiqishi):

```js
// Buzilgan token — bitta belgi qo'shsak ham verify rad etadi
try {
  jwt.verify(token + "x", secret);
} catch (e) {
  console.log("buzilgan token:", e.name);
}

// Boshqa secret bilan tekshirish — rad etadi
try {
  jwt.verify(token, "boshqa-sir");
} catch (e) {
  console.log("xato secret:", e.name);
}
```

Chiqish:

```
buzilgan token: JsonWebTokenError
xato secret: JsonWebTokenError
```

Demak: faqat **secret**'ni biladigan server to'g'ri imzo yarata oladi. Hujumchi payloadni o'zgartirsa (masalan, `role: "user"` ni `role: "admin"` ga), imzo eski qoladi va `verify` xato beradi. Shuning uchun **secret** — butun tizimning kaliti, uni hech qachon kodga yozmang, faqat `.env`'da saqlang (bu haqda oxirida).

### Access va refresh token

Bitta muammo bor: token muddatini qancha qilamiz?

- **Qisqa** (masalan 15 daqiqa) — o'g'irlansa, tezda yaroqsiz bo'ladi. Lekin foydalanuvchi har 15 daqiqada qayta login qilishi noqulay.
- **Uzoq** (masalan 7 kun) — qulay, lekin o'g'irlangan token uzoq vaqt xavfli.

Yechim — **ikkita** token:

- **Access token** — qisqa muddatli (~15 daqiqa). Har bir so'rovda yuboriladi, himoyalangan endpoint'larga kirish uchun.
- **Refresh token** — uzoq muddatli (~7 kun). Faqat yangi access token olish uchun ishlatiladi. Access token muddati tugagach, klient refresh token bilan `/refresh` ga murojaat qilib, yangi access oladi — qayta login qilmasdan.

Shunday qilib qisqa muddatning xavfsizligi va uzoq sessiyaning qulayligi birlashadi.

![Auth oqimi](rasmlar/20-auth-oqim.svg)

---

## Auth middleware: tokenni tekshirib `req.user` ga

Endi eng muhim ulanish nuqtasi — **auth middleware**. U har bir himoyalangan so'rovda:

1. `Authorization: Bearer <token>` headerdan tokenni ajratadi,
2. `jwt.verify` bilan imzo va muddatni tekshiradi,
3. payloaddan `req.user` ni to'ldiradi (keyingi handler'lar foydalanishi uchun),
4. xato bo'lsa — `401` qaytaradi.

```js
function requireAuth(req, res, next) {
  const header = req.headers.authorization ?? "";
  const [scheme, token] = header.split(" "); // "Bearer eyJ..." -> ["Bearer", "eyJ..."]
  if (scheme !== "Bearer" || !token) {
    return res.status(401).json({ xato: "Token yo'q" });
  }
  try {
    const payload = jwt.verify(token, ACCESS_SECRET);
    req.user = { id: payload.sub, role: payload.role }; // keyingilar uchun
    next();
  } catch {
    return res.status(401).json({ xato: "Token yaroqsiz yoki muddati o'tgan" });
  }
}
```

`Authorization: Bearer <token>` — bu standart konventsiya. "Bearer" so'zi "egasi" degani: "bu tokenni kim ko'tarib yursa (bearer), o'sha kirishga haqli". Shuning uchun token — naqd pul kabi: kim ushlasa, o'sha foydalanadi. Demak uni himoya qilish juda muhim (bu haqda oxirida).

Bu middleware'ni route'ga ulaganimizda, handler ichida `req.user` tayyor bo'ladi — xuddi 13-bobdagi ([middleware](./13-middleware.md)) "ma'lumotni boyitish" qolipi kabi, lekin endi haqiqiy token bilan.

---

## Avtorizatsiya: RBAC va resurs egaligi

Auth middleware "kimsan?" ga javob berdi. Endi "nima qila olasan?" — avtorizatsiyaga o'tamiz. Ikki xil tekshiruv kerak bo'ladi.

### 1. RBAC — rolga asoslangan ruxsat

**RBAC** (Role-Based Access Control) — foydalanuvchiga **rol** beriladi (`user`, `admin`), va har bir endpoint ma'lum rollarni talab qiladi. Buni middleware **factory** sifatida yozamiz:

```js
function requireRole(...rollar) {
  return (req, res, next) => {
    if (!rollar.includes(req.user.role)) {
      return res.status(403).json({ xato: "Ruxsat yetarli emas" });
    }
    next();
  };
}
```

`requireRole("admin")` — sozlangan tekshiruvchini **qaytaradi**. Uni route'da `requireAuth` dan **keyin** ulaymiz (avval kim ekanini bilish kerak):

```js
// Faqat admin: avval requireAuth (req.user to'ldiriladi), keyin requireRole
app.get("/admin/users", requireAuth, requireRole("admin"), handler);
```

![RBAC: rol -> ruxsat](rasmlar/20-rbac.svg)

### 2. Resurs egaligi — IDOR oldini olish

RBAC yetarli emas. Tasavvur qiling, `user` rolidagi Olim `GET /tasks/5` ga murojaat qiladi. RBAC bo'yicha "har qanday `user` vazifani o'qiy oladi" — to'g'ri. Lekin **5-vazifa Olimniki emas, balki Anorniki** bo'lsa-chi?

Bu **IDOR** (Insecure Direct Object Reference) — eng keng tarqalgan va xavfli zaifliklardan biri. Hujumchi shunchaki URL'dagi ID'ni `/tasks/5`, `/tasks/6`, `/tasks/7` deb o'zgartirib, **boshqalarning** ma'lumotini o'qib chiqishi mumkin. Rol to'g'ri, lekin **egalik** tekshirilmagan.

Yechim: resurs olgandan keyin, uning egasi joriy foydalanuvchi ekanini tekshiramiz:

```js
app.get("/tasks/:id", requireAuth, async (req, res) => {
  const task = await prisma.task.findUnique({
    where: { id: Number(req.params.id) },
  });
  if (!task) return res.status(404).json({ xato: "Topilmadi" });

  // EGALIK tekshiruvi — IDOR oldini olish
  if (task.ownerId !== req.user.id) {
    return res.status(403).json({ xato: "Bu sizning vazifangiz emas" });
  }
  res.json(task);
});
```

Qoida: **har qanday "men/o'zimniki" resursida** egalikni doimo serverda tekshiring. Klientga ishonmang — URL'ni o'zgartirish bir soniyalik ish.

> **Maslahat:** Yaxshiroq usul — so'rovning o'zida egalikni filtrlash: `prisma.task.findFirst({ where: { id, ownerId: req.user.id } })`. Topilmasa `null` keladi va siz `404` qaytarasiz — bu hatto vazifa **mavjudligini** ham oshkor qilmaydi.

---

## REAL KEYS: to'liq auth tizimi (bcrypt + Prisma + JWT)

Endi hammasini birlashtirib, haqiqiy, ishlaydigan auth tizimini quramiz: register/login (bcrypt + SQLite orqali Prisma), JWT (access + refresh), himoyalangan endpoint, admin-only endpoint va faqat-egasi tekshiruvi. So'ng `fetch` bilan **haqiqatan** sinaymiz.

### O'rnatish va sxema

```bash
npm install express bcrypt jsonwebtoken @prisma/client
npm install -D prisma
npx prisma migrate dev --name init
```

`prisma/schema.prisma` — foydalanuvchi va vazifa modellari (19-bob, [MongoDB](./19-mongodb.md), o'rniga bu yerda SQLite ishlatamiz — server kerakmas, oson RUN):

```prisma
datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}
generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  password  String                      // bcrypt HASH saqlanadi, hech qachon ochiq parol emas
  role      String   @default("user")   // "user" yoki "admin"
  createdAt DateTime @default(now())
  tasks     Task[]
}

model Task {
  id      Int     @id @default(autoincrement())
  title   String
  done    Boolean @default(false)
  ownerId Int
  owner   User    @relation(fields: [ownerId], references: [id])
}
```

`.env` — secret'lar va baza yo'li **kodda emas**, shu yerda:

```bash
DATABASE_URL="file:./dev.db"
JWT_ACCESS_SECRET="dev-access-secret-almashtiring"
JWT_REFRESH_SECRET="dev-refresh-secret-almashtiring"
```

### Server (server.mjs)

`package.json`'da `"type": "module"` — zamonaviy ESM ishlatamiz.

```js
import express from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const app = express();
app.use(express.json());

const ACCESS_SECRET = process.env.JWT_ACCESS_SECRET;
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;
const COST = 12;

// --- Tokenlar ---
function accessToken(user) {
  return jwt.sign({ sub: user.id, role: user.role }, ACCESS_SECRET, {
    expiresIn: "15m",
  });
}
function refreshToken(user) {
  return jwt.sign({ sub: user.id }, REFRESH_SECRET, { expiresIn: "7d" });
}

// --- Auth middleware: tokenni tekshirib req.user ga ---
function requireAuth(req, res, next) {
  const header = req.headers.authorization ?? "";
  const [scheme, token] = header.split(" ");
  if (scheme !== "Bearer" || !token) {
    return res.status(401).json({ xato: "Token yo'q" });
  }
  try {
    const payload = jwt.verify(token, ACCESS_SECRET);
    req.user = { id: payload.sub, role: payload.role };
    next();
  } catch {
    return res.status(401).json({ xato: "Token yaroqsiz yoki muddati o'tgan" });
  }
}

// --- Avtorizatsiya: rol talab (factory) ---
function requireRole(...rollar) {
  return (req, res, next) => {
    if (!rollar.includes(req.user.role)) {
      return res.status(403).json({ xato: "Ruxsat yetarli emas" });
    }
    next();
  };
}

// --- Register: hash -> saqlash ---
app.post("/register", async (req, res, next) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ xato: "email va password kerak" });
    }
    const hash = await bcrypt.hash(password, COST);
    const user = await prisma.user.create({ data: { email, password: hash } });
    res.status(201).json({ id: user.id, email: user.email, role: user.role });
  } catch (err) {
    if (err.code === "P2002") return res.status(409).json({ xato: "Bu email band" });
    next(err);
  }
});

// --- Login: compare -> token ---
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = await prisma.user.findUnique({ where: { email } });
  // Bir xil javob: user yo'qmi yoki parol xatomi - sirni ochmaymiz
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ xato: "Email yoki parol noto'g'ri" });
  }
  res.json({ accessToken: accessToken(user), refreshToken: refreshToken(user) });
});

// --- Refresh: yangi access token ---
app.post("/refresh", async (req, res) => {
  try {
    const payload = jwt.verify(req.body.refreshToken, REFRESH_SECRET);
    const user = await prisma.user.findUnique({ where: { id: payload.sub } });
    if (!user) return res.status(401).json({ xato: "Foydalanuvchi yo'q" });
    res.json({ accessToken: accessToken(user) });
  } catch {
    return res.status(401).json({ xato: "Refresh token yaroqsiz" });
  }
});

// --- Himoyalangan: o'z profilim ---
app.get("/me", requireAuth, async (req, res) => {
  const user = await prisma.user.findUnique({ where: { id: req.user.id } });
  res.json({ id: user.id, email: user.email, role: user.role });
});

// --- Vazifa yaratish (egasi = joriy user) ---
app.post("/tasks", requireAuth, async (req, res) => {
  const task = await prisma.task.create({
    data: { title: req.body.title, ownerId: req.user.id },
  });
  res.status(201).json(task);
});

// --- RESURS EGALIGI: faqat egasi o'qiy oladi (IDOR oldini olish) ---
app.get("/tasks/:id", requireAuth, async (req, res) => {
  const task = await prisma.task.findUnique({ where: { id: Number(req.params.id) } });
  if (!task) return res.status(404).json({ xato: "Topilmadi" });
  if (task.ownerId !== req.user.id) {
    return res.status(403).json({ xato: "Bu sizning vazifangiz emas" });
  }
  res.json(task);
});

// --- Admin-only endpoint ---
app.get("/admin/users", requireAuth, requireRole("admin"), async (req, res) => {
  const users = await prisma.user.findMany({
    select: { id: true, email: true, role: true },
  });
  res.json(users);
});

// --- Markaziy error handler (13-bob) ---
app.use((err, req, res, next) => {
  console.error(err.message);
  res.status(500).json({ xato: "Server xatosi" });
});

app.listen(3000, () => console.log("Server: http://localhost:3000"));
```

### Haqiqiy sinov (fetch bilan)

Serverni `node --env-file=.env server.mjs` bilan ishga tushirib, boshqa fayldan butun oqimni `fetch` bilan sinaymiz: register -> login -> tokensiz/tokenli `/me` -> vazifa yaratish -> **IDOR test** (begona vazifa) -> **admin test** (rol bilan/rolsiz) -> refresh. Mana shu mashinada olingan **haqiqiy chiqish**:

```
register: 201 { id: 1, email: 'olma@x.uz', role: 'user' }
login: 200 access uzunligi: 157
login(xato): 401 { xato: "Email yoki parol noto'g'ri" }
/me (tokensiz): 401 { xato: "Token yo'q" }
/me: 200 { id: 1, email: 'olma@x.uz', role: 'user' }
task yaratildi: 201 { id: 1, title: 'Sut olish', done: false, ownerId: 1 }
o'z taskini o'qish: 200 { id: 1, title: 'Sut olish', done: false, ownerId: 1 }
begona taskini o'qish: 403 { xato: 'Bu sizning vazifangiz emas' }
/admin (user): 403 { xato: 'Ruxsat yetarli emas' }
/admin (admin): 200 [
  { id: 1, email: 'olma@x.uz', role: 'admin' },
  { id: 2, email: 'anor@x.uz', role: 'user' }
]
refresh: 200 yangi access: eyJhbGciOi...
```

Har bir qator nimani isbotlaydi:

- `register: 201` — parol bcrypt bilan hashlanib bazaga yozildi (ochiq emas).
- `login(xato): 401` — noto'g'ri parol `bcrypt.compare` dan o'tmadi, **bir xil** xato xabari.
- `/me (tokensiz): 401` — auth middleware tokensiz so'rovni to'sdi (**autentifikatsiya**).
- `begona taskini o'qish: 403` — **IDOR oldini olindi**: Anor Olimning vazifasini o'qiy olmadi.
- `/admin (user): 403` vs `/admin (admin): 200` — **RBAC** ishladi: oddiy userga taqiqlandi, admin rolidagi userga ruxsat berildi.
- `refresh: 200` — refresh token bilan yangi access token olindi, qayta login qilmasdan.

Tizimning to'rt qatlami ham haqiqatan ishlayapti: **parol xavfsizligi** (bcrypt), **autentifikatsiya** (JWT + middleware), **RBAC** (rol), **resurs egaligi** (IDOR). Aynan shu sxema ishlab chiqarish (production) API'larining poydevoridir.

---

## Xavfsizlik bo'yicha muhim qoidalar

Auth ishlayapti — lekin "ishlash" va "xavfsiz" bir narsa emas. Quyidagi qoidalar tizimingizni haqiqiy hujumlardan himoya qiladi:

**1. Tokenni qayerda saqlash (klient tomonida).** Bu — eng ko'p adashtiriladigan masala:

| Joy | Xavf | Tavsiya |
|---|---|---|
| `localStorage` | **XSS** ga ochiq — sahifaga kirgan har qanday JS uni o'qiy oladi | Tavsiya etilmaydi (ayniqsa refresh uchun) |
| **httpOnly cookie** | JS o'qiy olmaydi -> XSS himoyalangan | Refresh token uchun afzal |

`httpOnly` cookie — JavaScript'dan **ko'rinmaydi**, faqat brauzer uni server'ga avtomatik jo'natadi. Demak sahifaga zararli skript kirsa ham (XSS), tokenni o'qiy olmaydi. Buning evaziga **CSRF** xavfi paydo bo'ladi — uni `SameSite=Strict` (yoki `Lax`) va CSRF-token bilan yopasiz. Amaliyotda ko'p ilovalar: access tokenni xotirada (RAM, JS o'zgaruvchisida), refresh tokenni httpOnly cookie'da saqlaydi.

**2. Secret — faqat `.env`'da, hech qachon kodda emas.** Yuqorida ko'rganimizdek, secret'ni biladigan har kim **istalgan** token yarata oladi (admin bo'lib ko'rinishi mumkin). Shuning uchun:
   - `.env` faylni `.gitignore`'ga qo'ying — git'ga **hech qachon** tushmasin.
   - Kuchli, tasodifiy secret ishlating: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`.
   - Access va refresh uchun **alohida** secret'lar (biri sizib chiqsa, ikkinchisi himoyada).

**3. Refresh token rotation.** Har safar refresh ishlatilganda **yangi** refresh token ham bering va eskisini bekor qiling (bazada saqlangan refresh tokenlar ro'yxati orqali). Agar eski (allaqachon ishlatilgan) refresh token qayta kelsa — bu o'g'irlik belgisi, foydalanuvchining barcha sessiyalarini bekor qiling.

**4. Algoritmni qattiq belgilang.** Bu — mashhur JWT zaifligi. Tekshirishda algoritmni majburiy ko'rsating:

```js
// Algoritmni qattiq belgilash - "alg: none" yoki algoritm almashtirish hujumini to'sadi
jwt.verify(token, ACCESS_SECRET, { algorithms: ["HS256"] });
```

Aks holda hujumchi token header'idagi `alg`ni `none` ga o'zgartirib, imzosiz token o'tkazishga urinishi mumkin. `algorithms` ro'yxatini berib, faqat ruxsat etilgan algoritmni qabul qilasiz.

**5. Qo'shimcha qatlamlar.** To'liq xavfsiz auth uchun (21-bobda, [xavfsizlik](./21-xavfsizlik-config.md), davom etamiz):
   - Login'ga **rate limiting** (`express-rate-limit`) — brute-force'ni sekinlashtiradi.
   - Kirish ma'lumotlarini **validatsiya** (`zod`) — ifloslangan kirishni to'sadi.
   - **HTTPS** — token tarmoqda ochiq ketmasligi uchun (`secure` cookie shart qiladi).
   - **helmet** — xavfsizlik header'larini avtomatik qo'shadi.

> **Oltin qoida:** Auth — o'zingiz "o'ylab topadigan" joy emas. Standart, sinab ko'rilgan kutubxonalar (bcrypt, jsonwebtoken) va standart oqimlarni ishlating. "Soddaroq qilaman" deb XOR yoki o'z hash funksiyangizni yozish — falokatga olib boradi.

---

## Mashqlar

### Oson

**1.** `bcrypt` bilan "salom123" parolini cost `10` bilan hashlang va `compare` orqali (a) to'g'ri parol, (b) "salom124" xato parol uchun natijani chop eting.

**2.** `jwt.sign` bilan `{ sub: 7, role: "user" }` payloadli, `30s` muddatli token yarating. Tokenni `.split(".")` qilib, **payload** qismini base64url'dan dekodlang va chop eting.

**3.** `requireAuth` middleware'ida `Authorization` header `"Token abc"` (Bearer emas) bo'lsa, qaysi holat kodi qaytadi? Sababini bir jumlada yozing.

### O'rta

**4.** Login endpoint'ini shunday o'zgartiringki, foydalanuvchi topilmasa ham, parol xato bo'lsa ham **aynan bir xil** xabar va holat kodi qaytsin. Nega bu muhimligini izohlang.

**5.** `requireRole` ni `requireRole("admin", "moderator")` kabi **bir nechta** rol qabul qiladigan qilib yozing va `user` rolidagi foydalanuvchi `403` olishini tekshiring.

**6.** `GET /tasks/:id` endpoint'iga egalik tekshiruvini `findFirst({ where: { id, ownerId } })` usuli bilan qayta yozing. Begona vazifaga murojaatda nima uchun `404` (`403` emas) qaytarish ma'qulroq ekanini tushuntiring.

### Qiyin

**7.** `/refresh` endpoint'iga **rotation** qo'shing: yangi access token bilan birga **yangi refresh token** ham bering. (Maslahat: bazada `validRefreshTokens` jadvali yoki user yozuvida joriy refresh token saqlang; eski token kelsa rad eting.)

**8.** `jwt.verify` ga `{ algorithms: ["HS256"] }` qo'shing. So'ng token header'ini qo'lda `alg: "none"` ga o'zgartirib, imzosiz token yasashga urinib ko'ring — server uni rad etishini ko'rsating.

**9.** Access tokenni javob tanasida emas, **httpOnly cookie**'da jo'natadigan qilib login'ni o'zgartiring (`res.cookie("access", token, { httpOnly: true, sameSite: "strict", secure: true })`). `requireAuth`'ni cookie'dan token o'qiydigan qiling. localStorage'ga nisbatan qanday xavf kamayganini yozing.

---

<details>
<summary>Yechimlar</summary>

**1.**

```js
import bcrypt from "bcrypt";
const hash = await bcrypt.hash("salom123", 10);
console.log("to'g'ri:", await bcrypt.compare("salom123", hash)); // true
console.log("xato:  ", await bcrypt.compare("salom124", hash)); // false
```

**2.**

```js
import jwt from "jsonwebtoken";
const token = jwt.sign({ sub: 7, role: "user" }, "sir", { expiresIn: "30s" });
const [, payload] = token.split(".");
console.log(JSON.parse(Buffer.from(payload, "base64url").toString()));
// { sub: 7, role: 'user', iat: ..., exp: ... }
```

Diqqat: payload ochiq o'qildi — JWT shifrlanmagan, faqat imzolangan.

**3.** `401` qaytadi. Sababi: `requireAuth`'da `scheme !== "Bearer"` sharti bajariladi (`"Token"` !== `"Bearer"`), demak token yo'q deb hisoblanadi — bu **autentifikatsiya** muvaffaqiyatsizligi.

**4.**

```js
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = await prisma.user.findUnique({ where: { email } });
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ xato: "Email yoki parol noto'g'ri" });
  }
  res.json({ accessToken: accessToken(user), refreshToken: refreshToken(user) });
});
```

Muhimligi: agar "bunday email yo'q" deb alohida xabar bersangiz, hujumchi qaysi emaillar ro'yxatdan o'tganini aniqlay oladi (**user enumeration**). Bir xil javob bu sirni yopadi.

**5.**

```js
function requireRole(...rollar) {
  return (req, res, next) => {
    if (!rollar.includes(req.user.role)) {
      return res.status(403).json({ xato: "Ruxsat yetarli emas" });
    }
    next();
  };
}
app.get("/panel", requireAuth, requireRole("admin", "moderator"), (req, res) =>
  res.json({ panel: true })
);
// user roli -> 403, admin yoki moderator -> 200
```

**6.**

```js
app.get("/tasks/:id", requireAuth, async (req, res) => {
  const task = await prisma.task.findFirst({
    where: { id: Number(req.params.id), ownerId: req.user.id },
  });
  if (!task) return res.status(404).json({ xato: "Topilmadi" });
  res.json(task);
});
```

`404` afzalligi: begona vazifaga `403` bersangiz, hujumchiga "bu ID **mavjud**, lekin seniki emas" degan ma'lumotni berasiz (resurs borligini oshkor qilasiz). `404` esa "bunday narsa yo'q" deydi — mavjudligini ham yashiradi.

**7.**

```js
// Soddalashtirilgan: user yozuvida joriy refresh tokenni saqlaymiz
app.post("/refresh", async (req, res) => {
  try {
    const payload = jwt.verify(req.body.refreshToken, REFRESH_SECRET);
    const user = await prisma.user.findUnique({ where: { id: payload.sub } });
    // Rotation: faqat oxirgi berilgan refresh token amal qiladi
    if (!user || user.currentRefresh !== req.body.refreshToken) {
      return res.status(401).json({ xato: "Refresh token yaroqsiz" });
    }
    const newRefresh = refreshToken(user);
    await prisma.user.update({
      where: { id: user.id },
      data: { currentRefresh: newRefresh },
    });
    res.json({ accessToken: accessToken(user), refreshToken: newRefresh });
  } catch {
    return res.status(401).json({ xato: "Refresh token yaroqsiz" });
  }
});
```

(`User` modeliga `currentRefresh String?` ustuni qo'shiladi va login'da to'ldiriladi.) Eski refresh token qayta ishlatilsa, `currentRefresh` bilan mos kelmaydi — o'g'irlik aniqlanadi.

**8.**

```js
// verify'da algoritmni qattiq belgilash
const payload = jwt.verify(token, ACCESS_SECRET, { algorithms: ["HS256"] });
```

Agar hujumchi header'ni `{"alg":"none"}` ga o'zgartirib, imzosiz token yuborsa, `jwt.verify` `algorithms` ro'yxatida `none` yo'qligi sabab `JsonWebTokenError` tashlaydi — token rad etiladi. `algorithms` ni ko'rsatmaslik ba'zi eski sozlamalarda `alg: none` ni qabul qilish xavfini tug'diradi.

**9.**

```js
import cookieParser from "cookie-parser";
app.use(cookieParser());

app.post("/login", async (req, res) => {
  // ... bcrypt.compare ...
  res.cookie("access", accessToken(user), {
    httpOnly: true,   // JS o'qiy olmaydi -> XSS himoya
    sameSite: "strict", // CSRF himoya
    secure: true,      // faqat HTTPS
    maxAge: 15 * 60 * 1000,
  });
  res.json({ ok: true });
});

function requireAuth(req, res, next) {
  const token = req.cookies.access; // header o'rniga cookie'dan
  if (!token) return res.status(401).json({ xato: "Token yo'q" });
  try {
    const payload = jwt.verify(token, ACCESS_SECRET, { algorithms: ["HS256"] });
    req.user = { id: payload.sub, role: payload.role };
    next();
  } catch {
    return res.status(401).json({ xato: "Token yaroqsiz" });
  }
}
```

Xavf kamayishi: `httpOnly` cookie'ni **JavaScript o'qiy olmaydi**, shuning uchun sahifaga zararli skript kirsa ham (XSS) tokenni o'g'irlay olmaydi. `localStorage`'dagi token esa har qanday JS'ga ochiq. Evaziga CSRF xavfi paydo bo'ladi, uni `sameSite: "strict"` yopadi.

</details>

---

[⬅️ Oldingi: 19 — MongoDB va Mongoose](./19-mongodb.md) · [🏠 README](./README.md) · [Keyingi: 21 — Fayl yuklash, config va xavfsizlik ➡️](./21-xavfsizlik-config.md)
