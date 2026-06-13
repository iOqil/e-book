# 19 — MongoDB va Mongoose

[⬅️ Oldingi: 18 — Prisma ORM](./18-prisma.md) · [🏠 README](./README.md) · [Keyingi: 20 — Autentifikatsiya va avtorizatsiya ➡️](./20-auth.md)

> **Bu bobda:** Relyatsion bo'lmagan dunyoga — **NoSQL** va **document** ma'lumotlar bazasiga kiramiz. Avval NoSQL nima ekanini, **MongoDB** hujjat (document) modelini (JSON-ga o'xshash, BSON, moslashuvchan sxema) va **SQL vs NoSQL ni qachon** tanlashni tushunamiz. So'ng MongoDB tushunchalari (database -> collection -> document, `_id` va `ObjectId`) bilan tanishib, **Mongoose** ODM ni o'rnatamiz, `mongoose.connect` bilan ulanamiz. **Schema** va **Model** yasaymiz (tiplar, `required`/`default`/`unique`/`enum`/`validate`), to'liq **CRUD** ni (`create`/`find`/`findById`/`findOne`/`updateOne`/`findByIdAndUpdate`/`deleteOne`) va **query** ni (`filter`, `sort`/`limit`/`select`/`skip`, `$gt`/`$in`/`$regex` operatorlari) o'rganamiz. **Aloqalar** — `ref` + `populate` (referenced 1:N) va **embedded** hujjat (qachon embed, qachon ref); `pre('save')` **hook** (parol heshlash — 20-bobga ko'prik), **virtual** maydonlar, indekslar va `lean()` ham bor. REAL KEYS: to'liq **blog API** ma'lumot qatlami — post + muallif (`ref`) + izohlar (`embedded`). Hamma kod Node 24.12 + Mongoose 9.7 da **`mongodb-memory-server`** orqali haqiqatan ishga tushirib tekshirilgan.

---

## NoSQL nima va document DB

Shu paytgacha (16–18-boblar) biz **relyatsion** bazalar bilan ishladik: MySQL/SQLite, ularda ma'lumot **jadval**larga (qator + ustun) joylanadi va `JOIN` orqali bog'lanadi. Bu — ulkan, sinovdan o'tgan model. Lekin u yagona model emas.

**NoSQL** ("Not Only SQL") — relyatsion jadval modelidan voz kechgan bazalar oilasiga umumiy nom. Bir nechta turi bor: key-value (Redis), ustun (Cassandra), graf (Neo4j) va — bizni qiziqtirayotgani — **document** (hujjat) bazalar, ularning eng mashhuri **MongoDB**.

**Document DB** da ma'lumot jadval qatori sifatida emas, balki **hujjat** (document) sifatida saqlanadi. Hujjat — bu deyarli **JSON obyektining o'zi**: maydonlar (key) va qiymatlar, ichida boshqa obyektlar va massivlar bo'lishi mumkin. Masalan, foydalanuvchi:

```json
{
  "_id": "6a2bbcf48e747e9789e0bc2a",
  "ism": "Ali",
  "yosh": 30,
  "manzil": { "shahar": "Toshkent", "tuman": "Chilonzor" },
  "teglar": ["node", "mongo"]
}
```

E'tibor bering: `manzil` — ichma-ich obyekt, `teglar` — massiv. SQL da bularni alohida jadvallarga bo'lib, `JOIN` qilish kerak bo'lardi. Document DB da esa **bitta hujjat** bularning hammasini o'z ichiga oladi.

Texnik jihatdan MongoDB hujjatlarni **BSON** (Binary JSON) formatida saqlaydi — bu JSON'ning ikkilik (binar) ko'rinishi. BSON qo'shimcha tiplar beradi: `Date`, `ObjectId`, `Binary`, aniq butun/o'nlik sonlar. Lekin tashqaridan biz u bilan oddiy JSON kabi ishlaymiz.

Eng muhim farq — **sxema (schema)**. SQL jadvalda sxema **qat'iy**: ustunlar oldindan e'lon qilinadi, har qator aynan shu ustunlarga ega bo'lishi shart. MongoDB da esa **moslashuvchan (schema-flexible)**: bir collection ichidagi turli hujjatlar turli maydonlarga ega bo'lishi mumkin. Bir hujjatda `manzil` bor, boshqasida yo'q — baza buni qabul qiladi. Bu — tez prototiplash uchun katta ozodlik, lekin tartibsizlik xavfi ham. Aynan shu xavfni jilovlash uchun keyinroq **Mongoose** keladi.

![SQL jadval va MongoDB hujjat strukturasi farqi](rasmlar/19-sql-vs-document.svg)

---

## SQL vs NoSQL — qachon qaysi?

Bu — boshlovchilar eng ko'p adashadigan savol. To'g'ri javob: **"eng yaxshisi yo'q, mosi bor"**. Loyiha tabiatiga qarab tanlanadi.

**SQL (relyatsion: MySQL, PostgreSQL) ni tanlang, agar:**

- Ma'lumot **qat'iy va aniq aloqali** bo'lsa (foydalanuvchi -> buyurtma -> mahsulot, hammasi qoidaga bo'ysunadi).
- **Tranzaksiya** muhim bo'lsa — pul o'tkazmasi, hisob qoldig'i: "hammasi yoki hech narsa" kafolati kerak (16-bobdagi `BEGIN/COMMIT/ROLLBACK`).
- Murakkab **hisobotlar**, ko'p jadvalli `JOIN` va agregatlar talab qilinsa.
- Sxema **barqaror**, kamdan-kam o'zgaradi.

**NoSQL (MongoDB) ni tanlang, agar:**

- Sxema **moslashuvchan/o'zgaruvchan** bo'lsa — har xil shakldagi hujjatlar, tez-tez yangi maydon qo'shiladi.
- **Tez prototip / MVP** kerak bo'lsa — sxema migratsiyalari bilan ovora bo'lmasdan kodni yozib ketasiz.
- Ma'lumot tabiatan **iyerarxik / ichma-ich** bo'lsa (mahsulot va uning variantlari, post va izohlari) — bularni bitta hujjatda saqlash tabiiy.
- Juda katta hajm va **gorizontal scaling** (ko'p serverga taqsimlash) kerak bo'lsa.

Amaliyotda ko'p loyihalar **ikkalasini** ham ishlatadi (polyglot persistence): asosiy ma'lumot SQL da, sessiya/kesh Redis da, log/analitika MongoDB da. Shuning uchun ikkalasini ham bilish — backend dasturchi uchun shart. SQL ni chuqurroq o'rganmoqchi bo'lsangiz, [SQL kitobi](../sql/README.md) ga qarang.

> **Tez prototip tuzog'i:** "sxema yo'q" degani "tartib yo'q" degani emas. Mongoose'siz xom MongoDB da bir hujjatda `email`, boshqasida `e_mail`, uchinchisida `mail` yozib qo'yish oson — keyin so'rov yozib bo'lmaydi. Aynan shuning uchun Mongoose ishlatamiz: u moslashuvchanlikni saqlab, ustiga **tartib** qo'yadi.

---

## MongoDB tushunchalari: database -> collection -> document

MongoDB iyerarxiyasi SQL'ga o'xshaydi, lekin nomlari boshqacha:

| SQL | MongoDB | Izoh |
|---|---|---|
| Database | **Database** | bir loyiha bazasi (masalan `blog`) |
| Table (jadval) | **Collection** | bir turdagi hujjatlar to'plami (masalan `posts`) |
| Row (qator) | **Document** | bitta yozuv (bitta post) |
| Column (ustun) | **Field** (maydon) | hujjatdagi key (`sarlavha`) |
| Primary key (id) | **`_id`** | har hujjatda majburiy, avtomatik |

Ya'ni: bitta **database** ichida bir nechta **collection**, har collectionda ko'p **document**, har documentda **field**lar.

**`_id` va `ObjectId`.** Har bir hujjatda `_id` maydoni bo'ladi — bu uning yagona kaliti (SQL'dagi primary key kabi). Agar siz `_id` bermasangiz, MongoDB avtomatik **`ObjectId`** yaratadi — bu 12 baytli (24 ta hex belgi) maxsus qiymat, masalan `6a2bbcf48e747e9789e0bc2a`. ObjectId ichida yaratilgan vaqt ham kodlangan, shuning uchun u **deyarli** vaqt bo'yicha tartiblangan va global yagona. SQL'dagi auto-increment `1, 2, 3` o'rniga MongoDB shu ObjectId ni ishlatadi (bu taqsimlangan tizimda to'qnashuvsiz ishlash uchun qulay).

---

## Mongoose — nega ODM kerak?

MongoDB bilan ishlash uchun rasmiy `mongodb` drayveri bor. Lekin u "xom": sxema yo'q, validatsiya yo'q, aloqalar uchun yordam yo'q. Real loyihada bu xavfli.

**Mongoose** — bu **ODM** (Object Document Mapper). Prisma SQL uchun ORM bo'lgani kabi (18-bob), Mongoose MongoDB uchun ODM: u hujjatlarga **sxema** beradi, **validatsiya** qiladi, JS modellariga bog'laydi, aloqalar (`populate`), hooklar va virtual maydonlarni qo'shadi. Qisqasi — moslashuvchan MongoDB ustiga **tartib va xavfsizlik** qatlami.

O'rnatamiz:

```bash
npm install mongoose
```

> **Bu bobda baza qayerdan?** MongoDB — alohida **server**: odatda uni lokal o'rnatasiz yoki bepul **MongoDB Atlas** (bulutli) bazasidan foydalanasiz. Ushbu bob misollarini **haqiqatan ishga tushirib** tekshirish uchun biz `mongodb-memory-server` paketidan foydalandik — u test paytida **xotirada** vaqtinchalik mongod ishga tushiradi (real server o'rnatmasdan). Quyidagi natijalar aynan shu orqali olingan. **Sizning loyihangizda esa ulanish satri (connection string) Atlas yoki lokal serverga ishora qiladi.**

---

## Ulanish — `mongoose.connect`

Mongoose'da har narsadan oldin bazaga ulanasiz. Buning uchun **connection string** (ulanish satri) kerak:

```js
import mongoose from "mongoose";

// Lokal MongoDB:
// mongodb://127.0.0.1:27017/blog
// Atlas (bulut):
// mongodb+srv://user:parol@cluster0.xxxxx.mongodb.net/blog

await mongoose.connect("mongodb://127.0.0.1:27017/blog");
console.log("MongoDB ga ulandik");
```

Connection string tuzilishi: `mongodb://<host>:<port>/<database-nomi>`. Oxiridagi `blog` — database nomi; agar u mavjud bo'lmasa, MongoDB birinchi yozuvda **avtomatik yaratadi** (collectionlar ham shunday — birinchi hujjat yozilganda paydo bo'ladi).

Connection string ni **hech qachon kodga yozib qoldirmang** — u parol saqlaydi. `.env` faylga qo'ying (10-bobdagi `process.env` ni eslang):

```js
import "dotenv/config";
import mongoose from "mongoose";

await mongoose.connect(process.env.MONGO_URI);
```

Ulanish holatini kuzatish uchun `mongoose.connection` hodisalarini tinglash mumkin — bu ishlab chiqarish (production) da foydali:

```js
mongoose.connection.on("connected", () => console.log("[mongo] ulandi"));
mongoose.connection.on("error", (err) => console.error("[mongo] xato:", err.message));
mongoose.connection.on("disconnected", () => console.log("[mongo] uzildi"));
```

**Tekshirilgan natija** (`mongodb-memory-server` orqali real ulanish):

```
[event] connected
...
[event] disconnected
```

> **Ulanish bir marta.** `mongoose.connect` ni butun ilova bo'yicha **bir marta** (server ko'tarilishida) chaqirasiz, har so'rovda emas. Mongoose ichida ulanish hovuzini (connection pool) o'zi boshqaradi. Express server bilan birga ishlatishni REAL KEYS bo'limida ko'ramiz.

---

## Schema va Model

Mongoose'ning yuragi — **Schema**. U hujjat **shaklini** (qaysi maydonlar, qaysi tipda, qanday qoidalar bilan) ta'riflaydi. Schema'dan **Model** yasaladi — model orqali esa CRUD bajariladi.

```js
import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  ism: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  yosh: { type: Number, min: 0, default: 18 },
  rol: { type: String, enum: ["admin", "muallif", "oquvchi"], default: "oquvchi" },
  faol: { type: Boolean, default: true },
}, { timestamps: true });

// Modeldan model yasaymiz: "User" -> collection avtomatik "users" (kichik, ko'plik)
const User = mongoose.model("User", userSchema);
```

Diqqat qiling: `mongoose.model("User", ...)` ni chaqirganda Mongoose collection nomini **avtomatik** `users` qiladi — kichik harf va ko'plikka aylantiradi. Bu — kelishuv (convention).

**Maydon tiplari (SchemaTypes).** Asosiylar: `String`, `Number`, `Boolean`, `Date`, `mongoose.Schema.Types.ObjectId` (havola uchun), massiv `[String]`, ichma-ich obyekt.

**Maydon opsiyalari (validatsiya va sozlash):**

| Opsiya | Vazifasi |
|---|---|
| `required: true` | maydon majburiy; yo'q bo'lsa — validatsiya xatosi |
| `default: X` | berilmaganda standart qiymat |
| `unique: true` | takrorlanmas (indeks orqali; pastda izoh bor) |
| `enum: [...]` | faqat ro'yxatdagi qiymatlardan biri |
| `min` / `max` | son uchun chegaralar |
| `minlength` / `maxlength` | satr uzunligi chegaralari |
| `trim: true` | satr atrofidagi bo'shliqni olib tashlaydi |
| `lowercase` / `uppercase` | satrni kichik/katta harfga keltiradi |
| `validate` | maxsus tekshiruv funksiyasi |

`{ timestamps: true }` — schema darajasidagi qulaylik: Mongoose har hujjatga `createdAt` va `updatedAt` maydonlarini avtomatik qo'shadi va boshqaradi.

**Maxsus validatsiya** (`validate`) — masalan email shaklini tekshirish:

```js
const schema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    validate: {
      validator: (v) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v),
      message: (props) => `${props.value} — yaroqli email emas`,
    },
  },
});
```

**Validatsiya haqiqatan ishlaydimi?** Sinab ko'ramiz (tekshirilgan natija):

```js
const User = mongoose.model("User", userSchema);

// 1) lowercase + default ishlaydi
const ali = await User.create({ ism: "Ali", email: "ALI@example.com", yosh: 30, rol: "muallif" });
const vali = await User.create({ ism: "Vali", email: "vali@example.com" });
console.log(ali.email, "| default yosh:", vali.yosh, "| default rol:", vali.rol);

// 2) required tutadi
try {
  await User.create({ ism: "X" });           // email yo'q
} catch (e) {
  console.log("Validatsiya tutdi:", e.errors.email.message);
}

// 3) enum tutadi
try {
  await User.create({ ism: "Y", email: "y@e.com", rol: "xakker" }); // ruxsatsiz rol
} catch (e) {
  console.log("Enum tutdi:", !!e.errors.rol);
}
```

Chiqish:

```
ali@example.com | default yosh: 18 | default rol: oquvchi
Validatsiya tutdi: Path `email` is required.
Enum tutdi: true
```

Ko'rdingizmi: `ALI@example.com` avtomatik `ali@example.com` ga aylandi (`lowercase`), `yosh` va `rol` standart qiymatga to'ldi, email yo'qligida va noto'g'ri rolda esa Mongoose `create` ni **rad etdi**. Bu — moslashuvchan MongoDB ustidagi qat'iylik qatlami.

> **`unique` — validator emas, indeks!** `unique: true` aslida validatsiya emas — u MongoDB'da **unique index** yaratadi. Takror qiymat kelganda xato bazadan keladi (kod `E11000 duplicate key`), Mongoose validatsiyasidan emas. Indeks tayyor bo'lishi uchun ulanishdan keyin biroz vaqt ketishi mumkin; production'da `Model.syncIndexes()` ishlatiladi.

---

## CRUD — Create, Read, Update, Delete

Model tayyor bo'lgach, hamma amal model metodlari orqali bajariladi. Hammasi **Promise** qaytaradi, demak `await` bilan ishlaymiz.

### Create — yaratish

```js
// Variant 1: create (eng keng tarqalgan)
const post = await Post.create({ sarlavha: "Salom", matn: "Birinchi post" });

// Variant 2: new + save (hujjatni o'zgartirib keyin saqlash kerak bo'lsa)
const post2 = new Post({ sarlavha: "Ikkinchi" });
post2.matn = "qo'shildi";
await post2.save();

// Ko'p hujjat birdaniga
await Post.insertMany([{ sarlavha: "A" }, { sarlavha: "B" }]);
```

`create` qaytargan hujjatda `_id` (ObjectId) avtomatik to'lgan bo'ladi.

### Read — o'qish

```js
const hammasi = await Post.find();                       // hammasi (massiv)
const bittasi = await Post.findById(post._id);           // _id bo'yicha bitta
const birinchi = await Post.findOne({ sarlavha: "Salom" }); // shartga mos birinchisi
const sanaboq = await Post.countDocuments({ faol: true });   // soni
```

- `find(filter)` — shartga mos **hamma** hujjat (massiv; topilmasa bo'sh massiv `[]`).
- `findById(id)` — `_id` bo'yicha bitta (topilmasa `null`).
- `findOne(filter)` — shartga mos **birinchi** (topilmasa `null`).

### Update — yangilash

```js
// updateOne — natija statistikasi qaytaradi (hujjatni emas)
const r = await Post.updateOne({ _id: post._id }, { $set: { sarlavha: "Yangi" } });
console.log(r.modifiedCount);   // 1

// $inc — sonni oshirish (atomik)
await Post.updateOne({ _id: post._id }, { $inc: { korishlar: 1 } });

// findByIdAndUpdate — yangilab, YANGILANGAN hujjatni qaytaradi
const yangi = await Post.findByIdAndUpdate(
  post._id,
  { sarlavha: "Tahrirlandi" },
  { returnDocument: "after" }   // standart: eski hujjatni qaytaradi! "after" -> yangisini
);
console.log(yangi.sarlavha);    // Tahrirlandi
```

> **`returnDocument: "after"` ni unutmang.** `findByIdAndUpdate` standart holatda yangilangan emas, **eski** hujjatni qaytaradi. Yangilangan versiya kerak bo'lsa, `{ returnDocument: "after" }` bering. (Eski darsliklarda `{ new: true }` ko'rasiz — Mongoose 9 da u eskirgan deb belgilandi, `returnDocument: "after"` ishlating.)

`$set`, `$inc` — bular MongoDB **update operatorlari**. `$set` maydonni o'rnatadi, `$inc` sonni oshiradi/kamaytiradi (atomik — bir vaqtning o'zida ikki so'rov kelsa ham to'g'ri ishlaydi).

### Delete — o'chirish

```js
const d = await Post.deleteOne({ _id: post._id });
console.log(d.deletedCount);                    // 1

await Post.deleteMany({ faol: false });         // shartga mos hammasini
await Post.findByIdAndDelete(post._id);         // o'chirib, o'chirilgan hujjatni qaytaradi
```

**To'liq CRUD — tekshirilgan natija** (`mongodb-memory-server`, Mongoose 9.7):

```
findById: Ali
findByIdAndUpdate: Mongoose asoslari (yangilangan) | korishlar: 1
deleteOne deletedCount: 1
Qolgan postlar: 2
```

---

## Query — filter, operatorlar va modifikatorlar

`find` ga berilgan **filter obyekti** — so'rovning shartini ifodalaydi. Oddiy holatda `{ maydon: qiymat }` — aniq moslik:

```js
await Post.find({ faol: true });                 // faol === true
await Post.find({ muallif: ali._id });           // muallif shu ID
```

**Solishtirish operatorlari** (`$` bilan boshlanadi):

```js
await Post.find({ korishlar: { $gt: 100 } });     // > 100
await Post.find({ korishlar: { $gte: 50 } });     // >= 50
await Post.find({ korishlar: { $lt: 10 } });      // < 10
await Post.find({ yosh: { $gte: 18, $lte: 65 } }); // 18..65 oralig'i
await Post.find({ rol: { $ne: "admin" } });        // teng EMAS
```

**Massiv / ro'yxat operatorlari:**

```js
await Post.find({ teglar: { $in: ["mongo", "node"] } }); // teglar ichida shulardan biri bor
await Post.find({ rol: { $nin: ["admin"] } });           // ro'yxatda YO'Q
```

**Matn bo'yicha qidirish — `$regex`:**

```js
await Post.find({ sarlavha: { $regex: /tez/i } });        // "tez" so'zi (i — registrga befarq)
await Post.find({ ism: { $regex: "^Al" } });              // "Al" bilan boshlanadigan
```

**Query modifikatorlari** (zanjir bilan ulanadi) — natijani tartiblash, cheklash, maydon tanlash, sahifalash:

```js
const royxat = await Post.find({ faol: true })
  .sort({ korishlar: -1 })   // korishlar bo'yicha kamayuvchi (-1: desc, 1: asc)
  .skip(20)                  // birinchi 20 tasini o'tkazib yubor (sahifalash)
  .limit(10)                 // 10 tasini ol
  .select("sarlavha korishlar"); // faqat shu maydonlar (+ _id) qaytsin
```

- `.sort({ maydon: 1 | -1 })` — tartiblash; `1` o'suvchi, `-1` kamayuvchi.
- `.limit(n)` — ko'pi bilan `n` ta.
- `.skip(n)` — boshidan `n` tasini o'tkazib yuborish. `skip` + `limit` = **sahifalash** (pagination).
- `.select("a b")` — faqat sanab o'tilgan maydonlar; `.select("-matn")` — `matn` dan tashqari hammasi.

**Tekshirilgan natija** (`$gte` + `sort`, `$in`, `$regex`, sahifalash):

```
$gte sort: [ 'NoSQL nima=120', 'Express tez=50' ]
$in teglar: 2
$regex: [ 'Express tez' ]
```

> **`select` bilan tarmoqni tejang.** Faqat kerakli maydonlarni so'rasangiz (`.select("sarlavha")`), bazadan kamroq ma'lumot keladi — bu, ayniqsa katta hujjatlarda, sezilarli tezlik beradi.

---

## Aloqalar: ref + populate (referenced)

Real ma'lumot bog'liq bo'ladi: postning **muallifi** bor, foydalanuvchining **postlari** bor. MongoDB'da bog'lashning ikki yo'li bor: **referenced** (havola) va **embedded** (joylash). Avval birinchisi.

**Referenced** yondashuvda bir hujjat ikkinchisining **`_id`** sini saqlaydi — xuddi SQL'dagi foreign key kabi. Postda `muallif` maydoni `User` ga havola qiladi:

```js
const postSchema = new mongoose.Schema({
  sarlavha: { type: String, required: true },
  matn: String,
  // ObjectId + ref: "User" -> bu maydon User hujjatiga havola
  muallif: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
});
const Post = mongoose.model("Post", postSchema);

// Yaratishda faqat ID beramiz:
const post = await Post.create({ sarlavha: "Salom", muallif: ali._id });
```

Endi postni o'qiganda `muallif` faqat ObjectId bo'ladi (`6a2b...`). To'liq muallif ma'lumotini olish uchun **`populate`** ishlatamiz — u ID o'rniga butun hujjatni qo'yib beradi (SQL `JOIN` ning Mongoose analogi):

```js
const post = await Post.findById(id).populate("muallif");
console.log(post.muallif.ism);   // endi to'liq User hujjati: "Ali"

// faqat kerakli maydonlarni tortish:
const p2 = await Post.findById(id).populate("muallif", "ism email");
```

![ref + populate va embedded hujjat farqi](rasmlar/19-ref-vs-embedded.svg)

**Tekshirilgan natija** (`populate` ID o'rniga to'liq hujjat qo'ydi):

```
populate muallif: Ali ali@example.com
```

Bu — klassik **1:N** aloqa: bitta `User` -> ko'p `Post`, har `Post` -> bitta `User`.

---

## Aloqalar: embedded hujjat

Ikkinchi yo'l — **embedded** (joylangan): bog'liq ma'lumotni alohida collectionda emas, **asosiy hujjat ichida** saqlash. Klassik misol — postga **izohlar**. Izoh postsiz yashamaydi va doim post bilan birga o'qiladi, demak uni post ichiga joylash mantiqiy:

```js
const postSchema = new mongoose.Schema({
  sarlavha: { type: String, required: true },
  matn: String,
  // izohlar massivi — har biri kichik sub-schema
  izohlar: [{
    muallifIsmi: { type: String, required: true },
    matn: { type: String, required: true },
    sana: { type: Date, default: Date.now },
  }],
});
```

Izoh qo'shish — massivga `push` qilib, postni `save` qilish:

```js
const post = await Post.findById(id);
post.izohlar.push({ muallifIsmi: "Vali", matn: "Zo'r maqola!" });
post.izohlar.push({ muallifIsmi: "Ali", matn: "Rahmat" });
await post.save();
```

Endi postni bitta so'rovda o'qisangiz, izohlar **ichida** keladi — `populate` umuman kerak emas, qo'shimcha so'rov yo'q:

```js
const post = await Post.findById(id);
console.log(post.izohlar.length);          // 2
console.log(post.izohlar[0].muallifIsmi);  // "Vali"
```

**Tekshirilgan natija:**

```
Izohlar soni: 2 | birinchi izoh sana bormi: true
```

### Qachon embed, qachon ref?

Bu — MongoDB dizaynidagi eng muhim qaror. Oddiy qoida:

| Embed (joylash) qiling, agar... | Ref (havola) qiling, agar... |
|---|---|
| ma'lumot egasiz yashamaydi (izoh -> post) | ma'lumot mustaqil (foydalanuvchi) |
| doim birga o'qiladi | alohida ham kerak bo'ladi |
| soni cheklangan (o'nlab) | soni cheksiz o'sishi mumkin |
| kamdan-kam o'zgaradi | ko'p joyda ishlatiladi, markazlashgan yangilanish kerak |

**Sezgi:** "izoh" — embed (postga tegishli, soni cheklangan). "Muallif" — ref (mustaqil, ko'p postda takrorlanadi, profili bitta joyda yangilanishi kerak). Agar embedlangan massiv **cheksiz** o'sadigan bo'lsa (masalan mashhur postda million izoh), uni ref ga o'tkazing — chunki MongoDB hujjat hajmi 16 MB bilan cheklangan.

---

## Middleware (hooks): `pre('save')` — parolga ko'prik

Mongoose **middleware** (hooks) — ma'lum amal **oldidan** (`pre`) yoki **keyin** (`post`) avtomatik ishlaydigan funksiyalar. Express middleware (13-bob) g'oyasiga o'xshaydi, lekin bu yerda bazaviy amallar ushlab olinadi.

Eng mashhur misol — `pre('save')` bilan **parolni heshlash**. Foydalanuvchi parolini hech qachon ochiq saqlamaymiz; saqlashdan **oldin** uni heshga aylantiramiz. Bu — to'g'ridan-to'g'ri 20-bobga (autentifikatsiya) ko'prik:

```js
import { createHash } from "node:crypto";

const userSchema = new mongoose.Schema({
  email: String,
  parol: String,
});

// save() dan OLDIN ishlaydi. Mongoose 9 da hook async funksiya
userSchema.pre("save", async function () {
  // faqat parol o'zgargan bo'lsa qayta heshlaymiz (aks holda har save da qayta-qayta heshlanadi)
  if (!this.isModified("parol")) return;
  this.parol = createHash("sha256").update(this.parol).digest("hex");
});

const User = mongoose.model("User", userSchema);

const u = new User({ email: "a@b.com", parol: "123456" });
await u.save();
console.log(u.parol);   // 8d969eef6eca... (xom "123456" emas!)
```

`this` — saqlanayotgan hujjat. `this.isModified("parol")` tekshiruvi muhim: u faqat **o'zgargan** parolni qayta heshlaydi — aks holda foydalanuvchi emailini yangilaganda parol qayta heshlanib, eski parol ishlamay qoladi.

**Tekshirilgan natija:**

```
Hash bo'ldimi: true 8d969eef6eca...
Parol o'zgarmadi (qayta hash yo'q): true
```

> **Diqqat — bu DEMO!** Bu yerda biz oddiy `sha256` ishlatdik, faqat hook tushunchasini ko'rsatish uchun. **Haqiqiy parol uchun sha256 YETARLI EMAS** — u juda tez, brute-force ga ojiz. Real loyihada **bcrypt** (sekin, "salt" bilan) ishlatiladi. To'liq parol heshlash, `bcrypt`, JWT token va login/registratsiya tizimini keyingi — **[20-bob (Autentifikatsiya)](./20-auth.md)** da to'liq quramiz. Bu yerda siz hook **qayerga ulanishini** ko'rib qo'ying.

---

## Virtual maydonlar

**Virtual** — bazada **saqlanmaydigan**, lekin o'qiganda hisoblanadigan maydon. Masalan, izohlar sonini yoki to'liq ismni har safar hisoblamasdan, virtual sifatida e'lon qilish mumkin:

```js
postSchema.virtual("izohSoni").get(function () {
  return this.izohlar.length;
});

userSchema.virtual("taqdimot").get(function () {
  return `${this.ism} <${this.email}>`;
});

const ali = await User.create({ ism: "Ali", email: "ali@example.com" });
console.log(ali.taqdimot);   // "Ali <ali@example.com>"
```

**Tekshirilgan natija:**

```
Virtual: Ali <ali@example.com>
```

Virtuallar bazada joy egallamaydi — ular faqat JS tomonida hisoblanadi. (Eslatma: virtual maydonlar `JSON.stringify` / `res.json` ga avtomatik kirmaydi; kerak bo'lsa schema'ga `{ toJSON: { virtuals: true } }` opsiyasini qo'shing.)

---

## Indekslar va `lean()` — qisqacha samaradorlik

**Indeks.** Ko'p qidiriladigan maydonga **indeks** qo'ysangiz, MongoDB so'rovni keskin tezlashtiradi (kitobning alifbo ko'rsatkichi kabi — har safar boshidan o'qimaydi). `unique: true` ham aslida indeks edi. Schema darajasida:

```js
postSchema.index({ sarlavha: "text" });   // matn qidiruvi uchun
postSchema.index({ muallif: 1, createdAt: -1 }); // murakkab (compound) indeks
```

Qoida: tez-tez `find`/`sort` qilinadigan maydonlarga indeks qo'ying. Ortiqcha indeks esa yozishni sekinlashtiradi — me'yorni saqlang.

**`lean()`.** Standart holatda `find` to'liq Mongoose hujjatlarini qaytaradi — ularda `save()`, virtuallar, getterlar bor, lekin "og'ir". Agar siz ma'lumotni faqat **o'qib, JSON qaytarmoqchi** bo'lsangiz (o'zgartirmasangiz), `.lean()` qo'shing — u oddiy JS obyektini qaytaradi, ancha **tez va yengil**:

```js
const royxat = await Post.find().lean();   // oddiy obyektlar (Mongoose hujjati emas)
```

**Tekshirilgan natija:**

```
lean() oddiy obyekt: true
```

Read-only ro'yxat sahifalari (masalan blog postlar ro'yxati) uchun `lean()` — bepul tezlik.

---

## REAL KEYS — blog API ma'lumot qatlami

Endi hammasini birlashtirib, real **blog API** ning ma'lumot qatlamini quramiz: foydalanuvchi (`User`), post (`Post`) — muallif **ref** bilan, izohlar **embedded**. Bu — 12–13-bobdagi Express bilan ulanadigan, hayotiy backend tuzilishi. Real loyihada modellarni alohida fayllarga (`models/User.js`, `models/Post.js`) bo'lamiz; quyida g'oyani ko'rsatish uchun bitta faylda yig'amiz.

```js
// blog.js — to'liq ishlaydigan misol (Mongoose 9.7 da tekshirilgan)
import mongoose from "mongoose";

// 1) Ulanish (real loyihada process.env.MONGO_URI)
await mongoose.connect("mongodb://127.0.0.1:27017/blog");

// 2) Model: User
const User = mongoose.model("User", new mongoose.Schema({
  ism: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
}, { timestamps: true }));

// 3) Model: Post (muallif = ref, izohlar = embedded)
const postSchema = new mongoose.Schema({
  sarlavha: { type: String, required: true, trim: true },
  matn: { type: String, required: true },
  muallif: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  teglar: { type: [String], default: [] },
  korishlar: { type: Number, default: 0, min: 0 },
  izohlar: [new mongoose.Schema({
    muallifIsmi: { type: String, required: true },
    matn: { type: String, required: true },
  }, { timestamps: true })],
}, { timestamps: true });

postSchema.virtual("izohSoni").get(function () {
  return this.izohlar.length;
});

const Post = mongoose.model("Post", postSchema);

// 4) Servis funksiyalari (Express controller ichidan chaqiriladi)
async function postYarat({ sarlavha, matn, muallifId, teglar }) {
  return Post.create({ sarlavha, matn, muallif: muallifId, teglar });
}

async function izohQosh(postId, { muallifIsmi, matn }) {
  const post = await Post.findById(postId);
  if (!post) return null;
  post.izohlar.push({ muallifIsmi, matn });
  await post.save();
  return post;
}

async function postlarRoyxati({ teg, sahifa = 1, soni = 10 } = {}) {
  const filter = teg ? { teglar: teg } : {};
  return Post.find(filter)
    .sort({ createdAt: -1 })          // yangilari birinchi
    .skip((sahifa - 1) * soni)        // sahifalash
    .limit(soni)
    .populate("muallif", "ism")       // muallif ismini tortamiz
    .select("sarlavha teglar korishlar muallif")
    .lean();                          // read-only -> yengil
}

// 5) Seed + sinov
const ali = await User.create({ ism: "Ali", email: "ali@example.com" });
const vali = await User.create({ ism: "Vali", email: "vali@example.com" });

const p1 = await postYarat({ sarlavha: "MongoDB asoslari", matn: "Hujjat DB...", muallifId: ali._id, teglar: ["mongo", "db"] });
await postYarat({ sarlavha: "Express bilan API", matn: "REST...", muallifId: vali._id, teglar: ["node", "web"] });
await postYarat({ sarlavha: "Mongoose ODM", matn: "Schema...", muallifId: ali._id, teglar: ["mongo", "node"] });

await izohQosh(p1._id, { muallifIsmi: "Vali", matn: "Foydali!" });
await izohQosh(p1._id, { muallifIsmi: "Hasan", matn: "Davom eting" });

// 6) "mongo" tegli postlar ro'yxati (populate qilingan)
const royxat = await postlarRoyxati({ teg: "mongo" });
console.log("mongo tegli postlar:");
for (const p of royxat) {
  console.log(` - "${p.sarlavha}" | muallif: ${p.muallif.ism} | korishlar: ${p.korishlar}`);
}

// 7) Bitta postni to'liq (muallif + embedded izohlar bilan)
const toliq = await Post.findById(p1._id).populate("muallif", "ism email");
console.log(`\n"${toliq.sarlavha}" muallifi: ${toliq.muallif.ism} <${toliq.muallif.email}>`);
console.log(`Izohlar (${toliq.izohSoni}):`);
for (const iz of toliq.izohlar) {
  console.log(`   ${iz.muallifIsmi}: ${iz.matn}`);
}

await mongoose.disconnect();
```

**Tekshirilgan chiqish** (`mongodb-memory-server`, Node 24.12 + Mongoose 9.7 — real run):

```
mongo tegli postlar:
 - "Mongoose ODM" | muallif: Ali | korishlar: 0
 - "MongoDB asoslari" | muallif: Ali | korishlar: 0

"MongoDB asoslari" muallifi: Ali <ali@example.com>
Izohlar (2):
   Vali: Foydali!
   Hasan: Davom eting
```

E'tibor bering, bu kichik misolda nimalar birlashdi:

- **ref + populate**: post ro'yxatida `muallif` faqat ID edi, `populate("muallif", "ism")` uni to'liq ismga aylantirdi.
- **embedded**: izohlar post ichida — bitta `findById` ularning hammasini olib keldi, alohida so'rov yo'q.
- **query**: `teg` bo'yicha `filter`, `sort` (yangilari birinchi), `skip`/`limit` bilan sahifalash, `select` bilan kerakli maydonlar.
- **virtual**: `izohSoni` bazada yo'q — o'qiganda hisoblandi.
- **lean()**: ro'yxat read-only, shuning uchun yengil obyektlar qaytdi.

### Express bilan ulash (eskiz)

Bu servis funksiyalarini 12–13-bobdagi Express'ga ulash juda tabiiy. Ulanishni server boshida bir marta qilamiz:

```js
// server.js (eskiz)
import express from "express";
import mongoose from "mongoose";
// import { Post, User } from "./models/index.js"; // real loyihada

const app = express();
app.use(express.json());

app.get("/posts", async (req, res, next) => {
  try {
    const { teg, sahifa } = req.query;
    const royxat = await postlarRoyxati({ teg, sahifa: Number(sahifa) || 1 });
    res.json(royxat);
  } catch (err) {
    next(err); // markaziy error handler ga (13-bob)
  }
});

app.post("/posts/:id/izoh", async (req, res, next) => {
  try {
    const post = await izohQosh(req.params.id, req.body);
    if (!post) return res.status(404).json({ xato: "Post topilmadi" });
    res.status(201).json({ izohSoni: post.izohlar.length });
  } catch (err) {
    next(err);
  }
});

// MUHIM: avval bazaga ulanib, KEYIN serverni ishga tushiramiz
await mongoose.connect(process.env.MONGO_URI);
app.listen(3000, () => console.log("Server tayyor, MongoDB ulangan"));
```

Bu — to'liq blog API ning skeleti: ma'lumot qatlami (Mongoose) + HTTP qatlami (Express) + 13-bobdagi markaziy error handler. 20-bobda buning ustiga autentifikatsiya qo'shamiz.

---

## Mashqlar

> Misollarni haqiqatan ishga tushirib ko'ring. MongoDB serveringiz bo'lmasa, `npm install mongoose mongodb-memory-server` qilib, fayl boshida quyidagini qo'shing va `mongoose.connect(mem.getUri())` ishlating:
> ```js
> import { MongoMemoryServer } from "mongodb-memory-server";
> const mem = await MongoMemoryServer.create();
> ```

### Oson

1. `Kitob` schema yarating: `nom` (String, required), `narx` (Number, min 0), `mavjud` (Boolean, default true), `janr` (enum: "ilmiy", "badiiy", "darslik"). Model yasab, ikkita kitob `create` qiling va `find` bilan o'qing.
2. Yuqoridagi `Kitob` modelida `janr: "kompyuter"` (enum'da yo'q) bilan kitob yaratishga urinib, validatsiya xatosini `try/catch` da tutib, xato xabarini chop eting.
3. Kitoblardan `narx` 50 000 dan yuqorilarini, narx bo'yicha **kamayuvchi** tartibda, faqat `nom` va `narx` maydonlari bilan toping (`$gt` + `sort` + `select`).

### O'rta

4. `Muallif` (`ism`, `email` unique) va `Kitob` (`nom`, `muallif` -> `ref: "Muallif"`) modellarini yarating. Bitta muallif va unga tegishli ikkita kitob yarating, so'ng kitoblarni `populate("muallif")` bilan o'qing.
5. `Kitob` ga **embedded** `sharhlar` massivini qo'shing (`muallifIsmi`, `matn`, `ball` 1–5). Bitta kitobga ikkita sharh `push` qilib saqlang, keyin o'qib, sharhlar sonini va o'rtacha ballni (virtual maydon `ortachaBall` orqali) chiqaring.
6. `Muallif` schema'siga `pre('save')` hook qo'shing: `email` har doim kichik harfga aylansin (`this.email = this.email.toLowerCase()`). `ALI@MAIL.COM` bilan muallif yaratib, bazada `ali@mail.com` saqlanganini tekshiring. (Maslahat: `lowercase: true` opsiyasi ham mavjud — ammo bu mashqda hook bilan qiling.)

### Qiyin

7. **Sahifalash funksiyasi.** `kitoblarRoyxati({ sahifa, soni })` funksiyasini yozing: u `sort({ createdAt: -1 })`, `skip`, `limit`, `lean()` ishlatib, berilgan sahifani qaytarsin. 7 ta kitob `insertMany` qilib, 1- va 2-sahifani (har biri 3 tadan) so'rab, to'g'ri bo'linishini tekshiring.
8. **REAL KEYS kengaytmasi.** Blog modeliga `like` funksiyasini qo'shing: `likeBos(postId)` `$inc` bilan `korishlar` ni emas, yangi `yoqtirishlar` maydonini atomik oshirsin. So'ng eng ko'p yoqtirilgan 3 postni (`sort({ yoqtirishlar: -1 }).limit(3)`) muallif ismi bilan (`populate`) chiqaring.

<details markdown="1"><summary>Yechimlar</summary>

**1 — Kitob modeli va CRUD**

```js
import mongoose from "mongoose";
import { MongoMemoryServer } from "mongodb-memory-server";

const mem = await MongoMemoryServer.create();
await mongoose.connect(mem.getUri());

const Kitob = mongoose.model("Kitob", new mongoose.Schema({
  nom: { type: String, required: true },
  narx: { type: Number, min: 0 },
  mavjud: { type: Boolean, default: true },
  janr: { type: String, enum: ["ilmiy", "badiiy", "darslik"] },
}));

await Kitob.create({ nom: "Node.js", narx: 80000, janr: "darslik" });
await Kitob.create({ nom: "1984", narx: 45000, janr: "badiiy" });

const hammasi = await Kitob.find();
console.log(hammasi.map((k) => `${k.nom} (${k.narx}, mavjud: ${k.mavjud})`));
// [ 'Node.js (80000, mavjud: true)', '1984 (45000, mavjud: true)' ]

await mongoose.disconnect();
await mem.stop();
```

**2 — Enum validatsiyasini tutish**

```js
try {
  await Kitob.create({ nom: "C++", janr: "kompyuter" }); // enum'da yo'q
} catch (e) {
  console.log("Xato:", e.errors.janr.message);
  // Xato: `kompyuter` is not a valid enum value for path `janr`.
}
```

`enum` ro'yxatda bo'lmagan qiymatni rad etadi; xato `e.errors.<maydon>.message` da bo'ladi.

**3 — `$gt` + `sort` + `select`**

```js
const qimmat = await Kitob.find({ narx: { $gt: 50000 } })
  .sort({ narx: -1 })
  .select("nom narx");
console.log(qimmat.map((k) => `${k.nom}=${k.narx}`));
// [ 'Node.js=80000' ]
```

**4 — ref + populate**

```js
const Muallif = mongoose.model("Muallif", new mongoose.Schema({
  ism: String,
  email: { type: String, unique: true },
}));
const Kitob = mongoose.model("Kitob", new mongoose.Schema({
  nom: String,
  muallif: { type: mongoose.Schema.Types.ObjectId, ref: "Muallif" },
}));

const ali = await Muallif.create({ ism: "Ali", email: "ali@e.com" });
await Kitob.create({ nom: "Birinchi", muallif: ali._id });
await Kitob.create({ nom: "Ikkinchi", muallif: ali._id });

const kitoblar = await Kitob.find().populate("muallif", "ism");
for (const k of kitoblar) console.log(`${k.nom} — ${k.muallif.ism}`);
// Birinchi — Ali
// Ikkinchi — Ali
```

**5 — Embedded sharhlar + virtual o'rtacha ball**

```js
const kitobSchema = new mongoose.Schema({
  nom: String,
  sharhlar: [{
    muallifIsmi: String,
    matn: String,
    ball: { type: Number, min: 1, max: 5 },
  }],
});
kitobSchema.virtual("ortachaBall").get(function () {
  if (this.sharhlar.length === 0) return 0;
  const yigindi = this.sharhlar.reduce((s, sh) => s + sh.ball, 0);
  return yigindi / this.sharhlar.length;
});
const Kitob = mongoose.model("Kitob", kitobSchema);

const k = await Kitob.create({ nom: "Node.js" });
k.sharhlar.push({ muallifIsmi: "Ali", matn: "Zo'r", ball: 5 });
k.sharhlar.push({ muallifIsmi: "Vali", matn: "Yaxshi", ball: 4 });
await k.save();

const olingan = await Kitob.findById(k._id);
console.log("Sharhlar:", olingan.sharhlar.length, "| o'rtacha:", olingan.ortachaBall);
// Sharhlar: 2 | o'rtacha: 4.5
```

Virtual `ortachaBall` bazada saqlanmaydi — o'qiganda hisoblanadi.

**6 — `pre('save')` hook bilan email kichik harf**

```js
const muallifSchema = new mongoose.Schema({ ism: String, email: String });
muallifSchema.pre("save", async function () {
  if (this.email) this.email = this.email.toLowerCase();
});
const Muallif = mongoose.model("Muallif", muallifSchema);

const m = await Muallif.create({ ism: "Ali", email: "ALI@MAIL.COM" });
console.log(m.email);   // ali@mail.com
```

`pre('save')` hujjat saqlanishidan oldin `this` ni o'zgartiradi. Mongoose 9 da hook **async funksiya** (eski `function(next)` shakli emas).

**7 — Sahifalash funksiyasi**

```js
// barqaror tartib uchun `tartib` maydoni bo'yicha saralaymiz
const Kitob = mongoose.model("Kitob", new mongoose.Schema({ nom: String, tartib: Number }));

async function kitoblarRoyxati({ sahifa = 1, soni = 3 } = {}) {
  return Kitob.find()
    .sort({ tartib: 1 })
    .skip((sahifa - 1) * soni)
    .limit(soni)
    .lean();
}

await Kitob.insertMany(
  Array.from({ length: 7 }, (_, i) => ({ nom: `Kitob ${i + 1}`, tartib: i + 1 }))
);

const s1 = await kitoblarRoyxati({ sahifa: 1, soni: 3 });
const s2 = await kitoblarRoyxati({ sahifa: 2, soni: 3 });
console.log("1-sahifa:", s1.map((k) => k.nom)); // ['Kitob 1','Kitob 2','Kitob 3']
console.log("2-sahifa:", s2.map((k) => k.nom)); // ['Kitob 4','Kitob 5','Kitob 6']
```

`skip((sahifa - 1) * soni)` — sahifalashning kaliti. `lean()` — read-only ro'yxat uchun. E'tibor bering: bir vaqtda `insertMany` qilingan hujjatlar `createdAt` bir xil bo'lib qolishi mumkin, shuning uchun barqaror sahifalash uchun alohida `tartib` (yoki `_id`) bo'yicha saralash ishonchliroq.

**8 — REAL KEYS: like va top-3 postlar**

```js
const Post = mongoose.model("Post", new mongoose.Schema({
  sarlavha: String,
  muallif: { type: mongoose.Schema.Types.ObjectId, ref: "Muallif" },
  yoqtirishlar: { type: Number, default: 0 },
}));

async function likeBos(postId) {
  // $inc — atomik oshirish (parallel so'rovlarda ham to'g'ri)
  await Post.updateOne({ _id: postId }, { $inc: { yoqtirishlar: 1 } });
}

const ali = await Muallif.create({ ism: "Ali" });
const a = await Post.create({ sarlavha: "A", muallif: ali._id });
const b = await Post.create({ sarlavha: "B", muallif: ali._id });
const c = await Post.create({ sarlavha: "C", muallif: ali._id });

// turli marta like bosamiz
for (let i = 0; i < 5; i++) await likeBos(a._id);
for (let i = 0; i < 9; i++) await likeBos(b._id);
for (let i = 0; i < 2; i++) await likeBos(c._id);

const top = await Post.find()
  .sort({ yoqtirishlar: -1 })
  .limit(3)
  .populate("muallif", "ism")
  .lean();

console.log("Top postlar:");
for (const p of top) console.log(` ${p.sarlavha}: ${p.yoqtirishlar} (${p.muallif.ism})`);
// B: 9 (Ali)
// A: 5 (Ali)
// C: 2 (Ali)
```

`$inc` — **atomik** operator: ko'p foydalanuvchi bir vaqtda like bossa ham, hisob to'g'ri qoladi (oddiy `oqi -> +1 -> yoz` ketma-ketligi esa poyga (race condition) ga olib kelardi).

</details>

---

Endi sizda backend dasturchining ikkita asosiy ma'lumot bazasi tajribasi bor: relyatsion (SQL/Prisma, 16–18-bob) va document (MongoDB/Mongoose). Keyingi bobda ma'lumotni saqlashdan **himoyalashga** o'tamiz: bu yerda ko'rgan `pre('save')` parol heshlash ko'prigini to'liq **autentifikatsiya va avtorizatsiya** tizimiga — `bcrypt`, JWT token, login/registratsiya va himoyalangan route'larga aylantiramiz.

---

[⬅️ Oldingi: 18 — Prisma ORM](./18-prisma.md) · [🏠 README](./README.md) · [Keyingi: 20 — Autentifikatsiya va avtorizatsiya ➡️](./20-auth.md)
