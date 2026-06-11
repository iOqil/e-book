# TypeScript — 0 dan Expertgacha (o'zbek tilida)

Bu kitob **JavaScript'ni biladigan** o'quvchini TypeScript bo'yicha 0 dan ekspert darajasiga olib chiqadi. Har bobda: sodda nazariya → `tsc` bilan tekshirilgan kod misollari → **20 ta mashq** (o'zingiz bajarasiz). Jami 24 bob, 480 mashq.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan — union/narrowing, generics, mapped & conditional types, kompilyatsiya quvuri kabi tushunchalar ko'z bilan ko'rib o'rganiladi.

> **Qoida:** TypeScript o'qib emas — **YOZIB** o'rganiladi. Har bir misolni o'zingiz tering, `tsc`'ni ishlatib xatolarni o'z ko'zingiz bilan ko'ring. Xato chiqsa — bu yaxshi: aynan TypeScript shu xatolarni brauzergacha tutib beradi.

> ℹ️ Bu kitob siz JavaScript asoslarini (o'zgaruvchi, funksiya, obyekt, massiv, async) bilasiz deb hisoblaydi. JavaScript yangi bo'lsa, avval [JavaScript — 0 dan Expertgacha](../js/README.md) kitobini o'qing.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. 2-bobda TypeScript'ni o'rnatib, har misolni o'z kompyuteringizda `tsc` bilan sinang.
3. Har bob oxiridagi **20 ta mashqni** o'zingiz bajaring — kodni ko'chirib qo'yish bilan TypeScript o'rganilmaydi.
4. Diagrammalar tip tizimini tezroq singdiradi — ularga e'tibor bering.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter (Windows / macOS / Linux) | Shart |
| Node.js + TypeScript (2-bobda o'rnatamiz) | Shart |
| JavaScript asoslari | **Shart** |
| Oldingi TypeScript tajribasi | Shart emas |

---

## I qism — Kirish va asosiy tiplar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [TypeScript nima va nega kerak?](./01-typescript-nima.md) | TypeScript nima ekani, JavaScript'ning ustki to'plami (superset) sifatida xatoni kod yozilayotganda (compile-time) tutishi, JS'ga kompilyatsiya qilinib tiplar o'chishi (type erasure) va nega zamonaviy loyihalarda kerakligini o'rganasiz. |
| 02 | [O'rnatish va birinchi qadamlar](./02-ornatish-birinchi-qadam.md) | TypeScript'ni o'rnatib, birinchi `.ts` faylni yozasiz, uni `tsc` bilan JavaScript'ga compile qilib `node`'da ishga tushirasiz; `tsconfig.json`, `--watch`, `--noEmit`, `tsx` va Playground bilan tanishasiz. |
| 03 | [Asosiy tiplar va type inference](./03-asosiy-tiplar.md) | O'zgaruvchiga keladigan qiymat turini cheklashni — type annotation, asosiy tiplar va TypeScript turini o'zi topadigan type inference'ni, hamda `const`/`let` narrowing farqini o'rganasiz. |
| 04 | [Massivlar, tuple va enum](./04-massiv-tuple-enum.md) | Bir turdagi qiymatlar uchun massiv tiplari (`number[]`, `readonly`, ko'p o'lchovli) va aniq tartibli qiymatlar uchun tuple (optional/rest/named, destructuring), hamda nomli konstantalar uchun enum — va nega 2026-da ko'pincha enum o'rniga union literal afzal ekanini o'rganasiz. |
| 05 | [Object tiplari va interface](./05-object-interface.md) | Obyektning shaklini tip bilan belgilash: inline object type va interface, optional `?` hamda readonly maydonlar, index signature, `extends` bilan kengaytirish, interface va type farqi va strukturaviy tiplilik. |
| 06 | [Funksiya tiplari](./06-funksiya-tiplari.md) | Funksiyalarni tiplash: parametr va return annotation, `void`, optional/default/rest parametrlar, funksiya tipi va callback'lar, HOF, overload va `this` parametri. |

## II qism — Tip tizimini egallash

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 07 | [Union va literal tiplar](./07-union-literal.md) | "Yo bu, yo u" holatlarini union (`string \| number`) va literal tiplar (`"kichik" \| "orta" \| "katta"`) bilan ifodalashni, union'da nega faqat umumiy xossalar mavjudligini, `null \| T` qolipini va tag maydonli discriminated union'ni o'rganasiz. |
| 08 | [Type narrowing va type guard'lar](./08-narrowing-guard.md) | Union qiymatdan aniq tipga "toraytirish" (narrowing): `typeof`, `instanceof`, `in`, truthiness, discriminated union switch, `never` bilan exhaustiveness, custom type guard (`v is X`) va assertion function (`asserts`). |
| 09 | [any, unknown, never va void](./09-any-unknown-never.md) | `any` tip tekshiruvini o'chiradi (xavfli), `unknown` noma'lum lekin xavfsiz (narrowing majbur), `never` hech qachon bo'lmaydigan qiymat (exhaustiveness qo'riqchisi), `void` qaytarmaydigan funksiya — va `as` assertion xavfi. |
| 10 | [Type alias, intersection va kompozitsiya](./10-type-intersection.md) | Tiplarga nom berish (type alias) va kichik tiplardan kattasini qurish: intersection (`A & B`), interface `extends` vs type `&`, generic type alias va kompozitsiya. |
| 11 | [Generics — asoslar](./11-generics-asos.md) | Bir xil mantiqni turli tiplar uchun `any`'siz yozishni — generic tip parametri `<T>`, generic interface/type/klass, constraint (`extends`) va bir nechta tip parametrini o'rganasiz. |
| 12 | [Generics — ilg'or (keyof, indexed access)](./12-generics-ilgor.md) | `keyof T`, indexed access `T[K]` va `K extends keyof T` constraint'i bilan to'liq tiplangan get/set/pluck/pick yordamchilarini yozishni; default tip parametri, `typeof` va const tip parametrini o'rganasiz. |

## III qism — OOP va tip-darajali dasturlash

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 13 | [Klasslar TypeScript'da](./13-klasslar.md) | JS klasslariga TypeScript bilan tip xavfsizligi va inkapsulyatsiya qo'shishni: access modifier'lar (public/private/protected/`#private`), readonly, parameter properties, getter/setter, static, abstract class, implements, meros va generic klasslarni o'rganasiz. |
| 14 | [Utility types](./14-utility-types.md) | TypeScript'ning tayyor utility tiplarini (Partial, Required, Readonly, Pick, Omit, Record, Exclude/Extract, NonNullable, ReturnType, Parameters, Awaited) qachon va qanday ishlatishni, ularni zanjirlab real forma/API tiplarini yasashni o'rganasiz. |
| 15 | [Mapped va conditional types](./15-mapped-conditional.md) | Utility tiplarni o'zingiz yasaysiz: mapped type bilan har maydon ustidan o'tib (readonly/`?` modifikatorlar, `as` bilan qayta nomlash), conditional type va `infer` bilan tip darajasida "if" yozib, DeepReadonly kabi real tiplarni qurasiz. |
| 16 | [Template literal types](./16-template-literal-types.md) | String tiplarni shablon bilan birlashtirib aniq string shakllarini yasash: union ko'paytma, Uppercase/Capitalize utility'lari, mapped+template orqali event nomlari va getter'lar, `infer` bilan route param ajratish. |
| 17 | [Modullar va deklaratsiya fayllari (.d.ts)](./17-modullar-deklaratsiya.md) | Kodni modullarga bo'lib export/import bilan ulashish va tipsiz JavaScript kutubxonalarga `.d.ts` deklaratsiya fayllari orqali tip qatlamini kiyintirishni o'rganasiz. |
| 18 | [tsconfig.json chuqur](./18-tsconfig.md) | `tsconfig.json` kompilyatorni qanday boshqarishini: uch asosiy blok, `strict` oilasi, target/module ta'siri va har loyiha turi uchun tavsiya konfiguratsiyani o'rganasiz. |

## IV qism — Amaliy TypeScript

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 19 | [DOM va brauzer TypeScript bilan](./19-dom-brauzer.md) | Brauzer (DOM) kodida tip xavfsizligi: `querySelector` va `Element\|null`, aniq element tipini olish, event tiplari, `event.target` narrowing va type assertion (`as`) ni xavfsiz ishlatish. |
| 20 | [Async, Promise va tiplangan API](./20-async-promise.md) | Asinxron kodni xavfsiz tiplash: `Promise<T>`, async/await tiplari, `fetch` + `json()` ortidagi `any` xavfini interface va validatsiya bilan yengish, `Promise.all` tuple natijasi, `catch (e: unknown)` narrowing va generic tiplangan API klient qurish. |
| 21 | [Tashqi kutubxonalar va @types](./21-types-kutubxonalar.md) | Tashqi npm kutubxonalar bilan TypeScript tiplarini bog'lashni: built-in `.d.ts`, `@types` paketi va o'z deklaratsiyangizni yozishni o'rganasiz. |
| 22 | [React va Node bilan TypeScript](./22-react-node.md) | O'rgangan TypeScript tiplarini real freymvorklarda qo'llashni: React komponent props'ini interface bilan tiplash, `useState<T>`, event va children tiplari, hamda Node/Express'da tiplangan req/res va environment bilan ishlashni o'rganasiz. |
| 23 | [Migratsiya: JS'dan TypeScript'ga](./23-migratsiya-js-ts.md) | Mavjud JavaScript loyihasini noldan emas, bosqichma-bosqich TypeScript'ga ko'chirishni: `allowJs`/`checkJs` bilan aralash loyiha, fayllarni bittalab `.ts` qilish, `any` bilan boshlab aniqlashtirish, `@ts-expect-error` ko'prigi, JSDoc tiplari va `strict`'ni oxirida yoqishni o'rganasiz. |

## V qism — Yakun

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 24 | [Yakuniy loyiha, best practices va shpargalka](./24-yakuniy-loyiha.md) | Butun kitobni birlashtirib, noldan to'liq tiplangan mini-loyiha (vazifa-menejeri) qurasiz: domen tiplaridan generics, utility, narrowing va runtime validatsiyagacha; professional best practices va keng shpargalkani o'zlashtirasiz. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
