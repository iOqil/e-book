# 19 — Custom utility va variant yaratish

[⬅️ Oldingi: 18 — @theme bilan dizayn tizimi](./18-theme-dizayn-tizimi.md) · [🏠 README](./README.md) · [Keyingi: 20 — Direktiva va funksiyalar ➡️](./20-direktiva-funksiyalar.md)

> **Bu bobda:** Tailwind'ni shunchaki ishlatishdan to'xtab, uni **kengaytirishni** o'rganamiz. v4 ning CSS-birinchi (CSS-first) yo'li bilan: `@utility` orqali Tailwind bermaydigan **yangi utility** yasash (statik `content-auto` dan tortib, `--value()` bilan ishlaydigan funksional `tab-*` gacha), `--value()` qiymatni qaysi to'rt manbadan olishi, `--modifier()` bilan `/qiymat` qismini hal qilish, manfiy funksional utility'lar, va `@custom-variant` orqali o'zingizning **shartlaringiz** uchun variant prefiksi (`pointer-coarse:`, `theme-midnight:`) qurish. Nihoyat, qachon CSS-birinchi yetadi-yu, qachon to'liq JS plagin kerakligini ajratasiz.

---

## 19.1 Avval nega? — token yetmaganda

[Oldingi bobda](./18-theme-dizayn-tizimi.md) tokenlar bilan butun dizayn tilini boshqarishni o'rgandingiz. Lekin token faqat **mavjud** utility oilalarini oziqlantiradi: rang, spacing, radius, soya. Token sizga `bg-brand-500` beradi — chunki `bg-*` allaqachon bor. Ammo Tailwind **umuman qamrab olmagan** xususiyat kerak bo'lsa-chi?

Masalan, `content-visibility` (sahifa unumdorligini oshiruvchi zamonaviy CSS xususiyati) uchun tayyor utility yo'q. Yoki `tab-size` (matndagi tab kengligi). Yoki "sensorli ekranda kattaroq tugma" degan **shart** — bu na rang, na o'lcham, balki bir holat.

Ikkita ehtiyoj, ikkita vosita:

- **Yangi utility kerak** (Tailwind qamramagan xususiyat yoki loyihaga xos naqsh) → **`@utility`**.
- **Yangi shart kerak** (maxsus `data-` atribut, media-feature, holat) → **`@custom-variant`**.

Eng yaxshi yangilik: v4 da bularning **ikkalasi ham CSS ichida** yoziladi. v3 da bu uchun JavaScript bilan plagin yozish kerak edi; v4 da ko'p hollarda bir-ikki qator CSS kifoya. JS plagin esa endi faqat dinamik, dasturiy generatsiya kerak bo'lgan kam holatlar uchun ([21-bobda](./21-plaginlar.md) ko'rasiz).

> 📌 **Atamalar.** **Utility** — bitta-yarim xususiyatni o'rnatuvchi klass (`p-4`, `text-center`). **Variant** — utility oldidagi shart prefiksi (`hover:`, `md:`) — u utility'ni "qachon" qo'llanishini boshqaradi ([15-bob](./15-holat-variantlari.md)). Bu bobda ikkalasini ham **o'zimiz** yasaymiz.

---

## 19.2 Statik `@utility` — bitta yangi klass

Eng oddiy holat: bitta qat'iy xususiyatga klass berish. Sintaksis xuddi oddiy CSS qoidasiga o'xshaydi, faqat selektor o'rnida **klass nomi** turadi:

```css
@import "tailwindcss";

@utility content-auto {
  content-visibility: auto;
}
```

Tamom. Endi `content-auto` butun loyihada ishlaydi:

```html
<section class="content-auto">...</section>
```

### Nega oddiy `.class` emas?

"Shunchaki `.content-auto { ... }` yozsam bo'lmaydimi?" — yaxshi savol. Bo'ladi, **lekin** u holda klass **variantlarni qo'llab-quvvatlamaydi**. `@utility` orqali e'lon qilingan klass esa Tailwind'ning butun variant tizimiga ulanadi — `hover:`, `lg:`, `dark:`, hamma narsa avtomatik ishlaydi:

```html
<section class="content-auto lg:content-auto hover:content-auto">
  Variantlar avtomatik ishlaydi — oddiy .class buni bermaydi.
</section>
```

Mana shu farq — `@utility` ni oddiy CSS klassidan ajratuvchi asosiy sabab.

![Statik @utility content-auto bitta klass beradi va lg:/hover: variantlari avtomatik ishlaydi; funksional @utility tab-* esa * o'rnini --value(integer) bilan to'ldirib tab-2, tab-4, tab-[13] kabi cheksiz klasslar yaratadi](rasmlar/tw19-utility-statik-funksional.svg)

### Yana ikki amaliy misol

Brauzer scrollbar'ini yashirish — bu uchun standart utility yo'q, lekin tez-tez kerak bo'ladi:

```css
@utility scrollbar-none {
  scrollbar-width: none;            /* Firefox */
  &::-webkit-scrollbar {            /* Chrome/Safari */
    display: none;
  }
}
```

E'tibor bering — `@utility` ichida `&` bilan ichki selektor (`&::-webkit-scrollbar`) yozsangiz bo'ladi; bu oddiy CSS ichma-ichligi (nesting) kabi ishlaydi.

Diagonal chiziqli fon naqshi — sof dekorativ, lekin loyihada qayta-qayta kerak bo'ladigan narsa:

```css
@utility bg-stripes {
  background-image: repeating-linear-gradient(
    45deg,
    #e0e7ff 0 10px,
    #ffffff 10px 20px
  );
}
```

Endi `class="bg-stripes hover:bg-stripes"` — utility ham, variant ham tayyor.

---

## 19.3 Funksional `@utility name-*` — qiymat qabul qiluvchi utility

Hozirgacha klasslar **qat'iy** edi. Endi kuchli qismga o'tamiz: **qiymat qabul qiluvchi** utility. `tab-2`, `tab-4`, `tab-8` — bularning hammasi bitta ta'rifdan kelib chiqsin, deylik.

Buning siri — nom oxiridagi **`*`** (yulduzcha) va **`--value()`** funksiyasi:

```css
@utility tab-* {
  tab-size: --value(integer);
}
```

`*` — bu **qiymat o'rni** (placeholder). U klassda `-` dan keyingi qismni ifodalaydi. `--value(integer)` esa o'sha qismni olib, butun son sifatida hal qiladi:

```html
<pre class="tab-2">...</pre>   <!-- tab-size: 2 -->
<pre class="tab-4">...</pre>   <!-- tab-size: 4 -->
<pre class="tab-[13]">...</pre> <!-- tab-size: 13 (arbitrary) -->
```

Bitta ta'rif → cheksiz klasslar oilasi. Aynan Tailwind'ning o'z `p-*`, `text-*` utility'lari ham xuddi shu mexanizm bilan qurilgan.

> ⚠️ **Eng ko'p uchraydigan xato — `*` ni unutish.** `@utility tab { ... }` (yulduzchasiz) — bu **statik** utility bo'lib, faqat `tab` klassini yaratadi; `tab-4` ishlamaydi. Qiymat qabul qilmoqchi bo'lsangiz, nom oxirida `*` **shart**: `@utility tab-*`.

---

## 19.4 `--value()` qiymatni qayerdan oladi?

`--value()` — bu funksional utility'ning yuragi. U `*` o'rnidagi matnni olib, uni **qaysidir manbaga** moslab hal qiladi. To'rtta asosiy manba bor:

| Manba turi | Sintaksis | Nimani qabul qiladi | Misol klass |
|---|---|---|---|
| **Bare (yalang'och)** | `--value(integer)`, `--value(number)`, `--value(percentage)` | To'g'ridan-to'g'ri son: `2`, `1.5`, `50%` | `tab-2`, `scale-150` |
| **Arbitrary** | `--value([length])`, `--value([integer])`, `--value([*])` | Kvadrat qavsdagi ixtiyoriy qiymat | `tab-[13]`, `w-[37px]` |
| **Literal kalit so'z** | `--value('auto')`, `--value('full')` | Aniq matnga moslaydi | `size-auto`, `size-full` |
| **Tema namespace** | `--value(--spacing-*)`, `--value(--color-*)` | `@theme` tokenini o'qiydi | `gap-md`, `glow-brand` |

![--value() funksiyasi qiymatni to'rt manbadan oladi: bare integer/number, arbitrary [length]/[integer], literal kalit so'z 'auto'/'full', va tema namespace --spacing-* / --color-* — barchasi bitta funksional utility'ni oziqlantiradi](rasmlar/tw19-value-manbalar.svg)

### Bir nechta manbani birlashtirish

Eng kuchli tomoni — bitta `--value()` ichida **bir nechta** manbani vergul bilan sanab, Tailwind'ga "qaysi mos kelsa o'shani ol" deyish mumkin:

```css
@utility tab-* {
  /* tab-2 (bare), tab-[13] (arbitrary), tab-full (kalit so'z) — uchchalasi ham ishlaydi */
  tab-size: --value(integer, [integer], 'auto');
}
```

### Tema tokenidan o'qiydigan misol

Bu — eng professional naqsh: utility o'z qiymatlarini [18-bobdagi](./18-theme-dizayn-tizimi.md) `@theme` tokenlaridan oladi. Masalan, "yorug'lik" soyasini turli o'lchamlarda beruvchi `glow-*` utility:

```css
@import "tailwindcss";

@theme {
  --glow-sm: 0 0 8px;
  --glow-md: 0 0 18px;
  --glow-lg: 0 0 32px;
}

@utility glow-* {
  box-shadow: --value(--glow-*) var(--color-indigo-500);
}
```

`--value(--glow-*)` — Tailwind'ga "qiymatni `--glow-` namespace'idan qidir" deydi. Endi `glow-sm`, `glow-md`, `glow-lg` — uchchalasi ham `@theme` tokenidan oziqlanadi:

```html
<button class="glow-md hover:glow-lg">Yorug' tugma</button>
```

Token o'zgarsa — utility ham birga o'zgaradi. Manba bitta.

> 💡 **Arbitrary qiymatlar bilan bog'lanish.** `tab-[13]` dagi `[13]` — bu [3-bobda](./03-utility-first-ish-jarayoni.md) ko'rgan **arbitrary value** (ixtiyoriy qiymat) sintaksisining aynan o'zi. `--value([integer])` shu qavs ichidagi qiymatni qabul qiladi. Ya'ni siz funksional utility yaratganingizda, foydalanuvchi avtomatik ravishda arbitrary qiymat ham yoza oladi — buni alohida sozlamaysiz.

---

## 19.5 `--modifier()` — `/qiymat` qismini hal qilish

Tailwind klasslarida ba'zan `/` (slash) orqali **modifikator** bo'ladi: `bg-black/50` (50% shaffoflik), `text-lg/7` (qator balandligi). Bu `/` dan keyingi qism — **modifier**.

O'z utility'ingizda ham shuni qabul qilmoqchi bo'lsangiz, `--modifier()` ishlatasiz — u `/` dan keyingi qismni hal qiladi, xuddi `--value()` `-` dan keyingisini hal qilgani kabi:

```css
@utility glow-* {
  box-shadow: 0 0 --value([length]) var(--color-indigo-500);
  opacity: --modifier([percentage]);
}
```

```html
<div class="glow-[20px]/75">...</div>
<!-- --value()  → 20px (length)
     --modifier() → 75% (percentage) -->
```

Qisqacha: **`--value()` `-` dan keyingisini**, **`--modifier()` `/` dan keyingisini** oladi. Aksariyat utility'lar faqat `--value()` bilan ishlaydi; `--modifier()` shaffoflik kabi "ikkinchi o'lcham" kerak bo'lganda qo'shiladi.

---

## 19.6 Manfiy funksional utility'lar

Tailwind'da `-mt-4` (manfiy margin) kabi **manfiy** utility'lar bor. O'z funksional utility'ingizning manfiy variantini berish uchun alohida `-` bilan boshlanuvchi ta'rif yozasiz:

```css
@utility top-* {
  top: --value(--spacing-*);
}

@utility -top-* {
  top: calc(--value(--spacing-*) * -1);
}
```

Endi `top-4` musbat, `-top-4` esa manfiy qiymat beradi. Naqsh sodda: manfiy variant uchun **alohida `@utility -name-*`** e'lon qiling va qiymatni `calc(... * -1)` bilan teskari qiling.

---

## 19.7 Custom variant — o'zingizning shartingiz

Endi ikkinchi vositaga o'tamiz. Variant — bu utility oldidagi **shart prefiksi**. `hover:`, `md:`, `dark:` — bularning bari shartlar. `@custom-variant` esa sizga **yangi shart** e'lon qilish imkonini beradi.

![@custom-variant shart bilan variant prefiksini bog'laydi: media-feature (@media pointer:coarse) → pointer-coarse: prefiks; selektor &:where([data-theme=midnight] *) → theme-midnight: prefiks; har bir variant istalgan utility oldiga qo'yiladi](rasmlar/tw19-custom-variant.svg)

### Media-feature varianti

"Sensorli (touch) ekranda tugmalar kattaroq bo'lsin" — buni `@media (pointer: coarse)` aniqlaydi. Shu shartga nom beramiz:

```css
@custom-variant pointer-coarse (@media (pointer: coarse));
```

Endi `pointer-coarse:` istalgan utility oldiga qo'yiladi:

```html
<button class="p-2 pointer-coarse:p-4">
  Sichqonchada kichik, barmoq bilan kattaroq tugma
</button>
```

Sintaksis sodda: `@custom-variant <nom> (<shart>);`. Bu — **qisqa forma** (shorthand), bitta media so'rovi yoki selektor uchun.

### Selektor / atribut varianti

Endi maxsus tema. Saytda `data-theme="midnight"` atributi bo'lganda ishlovchi `theme-midnight:` varianti yasaymiz:

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

```html
<html data-theme="midnight">
  <body>
    <div class="bg-white theme-midnight:bg-black theme-midnight:text-white">
      Midnight temada qora fon, oq matn
    </div>
  </body>
</html>
```

Bu yerdagi sintaksis muhim. `&` — utility qo'llanayotgan elementning o'rnini bildiradi. `:where(...)` esa selektorni o'rab, uning **specificity'sini 0 ga** tushiradi — shunda variant boshqa utility'lar bilan tortishmaydi.

> ⚠️ **Selektorli variantda `&` va `:where()` deyarli har doim kerak.** `&` bo'lmasa, Tailwind variantni qaysi elementga qo'llashni bilmaydi. `:where()` bo'lmasa, variant specificity'si oshib, oddiy utility'larni bosib ketishi mumkin. Naqsh: `&:where([shart] *)`.

### Ko'p qatorli forma va `@slot`

Ba'zan variant bir qatorga sig'maydi — masalan, media so'rovi **ichida** holat selektori kerak bo'lsa. U holda jingalak qavsli forma va `@slot` ishlatiladi. `@slot` — "utility shu yerga joylashadi" degan o'rin:

```css
@custom-variant any-hover {
  @media (any-hover: hover) {
    &:hover {
      @slot;
    }
  }
}
```

Bu `any-hover:bg-indigo-500` ni "agar qurilma hover'ni qo'llab-quvvatlasa **va** element hover holatida bo'lsa" degan murakkab shartga aylantiradi. `@slot` o'rnida utility'ning haqiqiy CSS'i joylashadi.

### `dark` ham aslida custom variant

Qiziq haqiqat: [16-bobda](./16-dark-mode.md) ko'p ishlatgan `dark:` varianti — bu Tailwind'ning ichki **custom variant**i, xolos. Va u **ustiga-yoziladi**. Standart dark'ni `class` strategiyasiga o'tkazmoqchi bo'lsangiz:

```css
@custom-variant dark (&:where(.dark, .dark *));
```

Ya'ni siz bobning birinchi yarmida o'rgangan mexanizm — Tailwind'ning o'zi `dark` ni qanday quradigani bilan **aynan bir xil**. Sehr yo'q, hammasi shu bitta direktiva.

---

## 19.8 `@variant` — Tailwind variantini qo'lda yozilgan CSS ichida ishlatish

Ba'zan oddiy CSS qoidasi yozasiz (utility emas), lekin uning ichida Tailwind variantini qo'llashni xohlaysiz — masalan, komponent stilining dark-mode versiyasini. Buning uchun **`@variant`** direktivasi bor (e'tibor bering: `@custom-variant` variant **yaratadi**, `@variant` esa mavjud variantni **qo'llaydi**):

```css
@layer components {
  .btn {
    background: var(--color-indigo-600);
    color: white;

    @variant dark {
      background: var(--color-indigo-400);
      color: black;
    }
  }
}
```

Kompilyatsiyadan keyin `.btn` yorug' rejimda indigo-600, dark rejimda esa indigo-400 bo'ladi — `dark:` ni HTML'da yozmasdan, to'g'ridan-to'g'ri CSS ichida. `@variant` o'zingiz yaratgan custom variantlar bilan ham ishlaydi: `@variant pointer-coarse { ... }`.

---

## 19.9 Qachon `@utility`/`@custom-variant`, qachon JS plagin?

Endi tabiiy savol: "Bularning hammasini CSS'da qila olsam, JS plagin nimaga kerak?"

| Vaziyat | Vosita |
|---|---|
| Bitta yangi xususiyat klassi | `@utility` (statik) |
| Qiymat qabul qiluvchi utility oilasi | `@utility name-*` + `--value()` |
| Yangi shart / media-feature / atribut | `@custom-variant` |
| Qo'lda CSS ichida variant qo'llash | `@variant` |
| **Yuzlab klassni dasturiy generatsiya** (masalan, ikon to'plamidan, sozlama obyektidan tsikl bilan) | **JS plagin** (`@plugin`) |
| **Boshqa plaginga (npm paket) ulanish** | **JS plagin** |

Qoida sodda: **CSS-birinchi yo'l aksariyat ehtiyojlarni qoplaydi.** JS plagin faqat dasturiy mantiq (tsikl, shart, tashqi ma'lumotdan generatsiya) kerak bo'lgandagina ustun keladi. Bu mavzuni — plaginlarni paketlangan utility sifatida — [21-bobda](./21-plaginlar.md) batafsil ko'ramiz.

---

## 19.10 Amaliy misol — barchasini birga

Kichik, lekin to'liq kengaytma to'plamini quramiz: funksional `tab-*`, statik `scrollbar-none`, sensorli `pointer-coarse:` varianti, `theme-midnight:` atribut varianti va komponent ichida `@variant dark`:

```css
@import "tailwindcss";

/* 1. Funksional utility — tema namespace'idan ham, bare/arbitrary'dan ham */
@utility tab-* {
  tab-size: --value(integer, [integer]);
}

/* 2. Statik utility — ichki selektor bilan */
@utility scrollbar-none {
  scrollbar-width: none;
  &::-webkit-scrollbar { display: none; }
}

/* 3. Media-feature varianti — sensorli ekran */
@custom-variant pointer-coarse (@media (pointer: coarse));

/* 4. Atribut varianti — maxsus tema */
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));

/* 5. Qo'lda komponent + @variant dark */
@layer components {
  .kod-panel {
    background: var(--color-slate-100);
    @variant dark {
      background: var(--color-slate-800);
    }
  }
}
```

```html
<html data-theme="midnight">
  <pre class="kod-panel tab-4 scrollbar-none p-3
              theme-midnight:bg-black
              pointer-coarse:p-5">
    function salom() {
        console.log("Tab kengligi 4, scrollbar yashirin");
    }
  </pre>
</html>
```

Bitta `<pre>` da: funksional utility (`tab-4`), statik utility (`scrollbar-none`), atribut varianti (`theme-midnight:`) va sensorli variant (`pointer-coarse:`) — barchasi siz o'zingiz CSS'da yaratdingiz, hech qanday JS plaginsiz.

---

## 19.11 Tez-tez uchraydigan xatolar

- **Funksional utility'da `*` ni unutish.** `@utility tab { ... }` faqat `tab` klassini beradi; `tab-4` uchun `@utility tab-*` kerak.
- **Noto'g'ri `--value()` manba turi.** `tab-4` da `--value(integer)` ishlaydi, lekin `tab-[13px]` uchun `--value([length])` kerak. Klass qabul qilishi kerak bo'lgan har bir shaklni `--value()` ichida sanang: `--value(integer, [integer], 'auto')`.
- **Oddiy `.class` dan variant kutish.** `.content-auto { ... }` ga `hover:` ishlamaydi. Variant kerak bo'lsa — `@utility content-auto` ishlating.
- **Selektorli variantda `&`/`:where()` ni tashlab ketish.** `@custom-variant theme-x ([data-x] &)` ko'pincha kutilmagan natija beradi. Ishonchli naqsh: `&:where([data-x] *)`.
- **`@custom-variant` va `@variant` ni chalkashtirish.** `@custom-variant` — variant **yaratadi** (bir marta, e'lon). `@variant` — mavjud variantni qo'lda yozilgan CSS **ichida qo'llaydi**.
- **CSS yetarli bo'lsa ham JS plaginga yugurish.** Statik yoki qiymatli utility, oddiy shart — bularning bari CSS-birinchi. JS plaginni faqat dasturiy generatsiya kerak bo'lganda oching.

> 🔭 **Oldinga qarash.** Endi Tailwind'ni token darajasida (18-bob) ham, utility/variant darajasida (shu bob) ham kengaytira olasiz. [Keyingi bobda](./20-direktiva-funksiyalar.md) bu direktivalar oilasini to'liq ko'rib chiqamiz — `@apply`, `@layer`, `@reference`, `theme()` funksiyasi va boshqalar — ya'ni Tailwind'ning butun CSS "lug'ati". Undan keyin esa [21-bobda](./21-plaginlar.md) JS plaginlar bilan tanishasiz.

---

## Mashqlar

**1-mashq.** Loyihangizda `text-wrap: balance` (sarlavhalarni chiroyli o'raydigan zamonaviy CSS) kerak, lekin tayyor utility yo'q. `text-balance` nomli statik utility yarating va u `hover:` bilan ham ishlasin.

<details markdown="1"><summary>Yechim</summary>

```css
@utility text-balance {
  text-wrap: balance;
}
```

```html
<h1 class="text-balance hover:text-balance">Chiroyli o'raladigan sarlavha</h1>
```

`@utility` orqali e'lon qilingani uchun `text-balance` Tailwind'ning variant tizimiga ulanadi — `hover:`, `lg:` va boshqalar avtomatik ishlaydi. Oddiy `.text-balance { ... }` bo'lsa, variantlar ishlamasdi.

</details>

**2-mashq.** `tab-2`, `tab-4`, `tab-8` va shuningdek `tab-[13]` ishlaydigan funksional utility yozing. `tab-size` xususiyatini sozlasin.

<details markdown="1"><summary>Yechim</summary>

```css
@utility tab-* {
  tab-size: --value(integer, [integer]);
}
```

Nom oxiridagi `*` — qiymat o'rni. `--value(integer)` `tab-2`/`tab-4`/`tab-8` (bare son) ni, `--value([integer])` esa `tab-[13]` (arbitrary) ni hal qiladi. Ikkalasini bitta `--value()` ichida vergul bilan sanaymiz.

</details>

**3-mashq.** Bir hamkasbingiz `@utility shadow-soft { ... }` deb yozdi va `shadow-soft-lg` ishlamasligidan hayron. U xohlagani — `shadow-soft-sm`, `shadow-soft-md`, `shadow-soft-lg`. Xatosi nimada, qanday tuzatadi?

<details markdown="1"><summary>Yechim</summary>

Nom oxirida **`*`** yo'q — shuning uchun bu **statik** utility bo'lib qoldi va faqat `shadow-soft` klassini yaratdi. Qiymat (`sm`/`md`/`lg`) qabul qilishi uchun funksional shaklga o'tkazish kerak:

```css
@theme {
  --shadow-soft-sm: 0 1px 4px;
  --shadow-soft-md: 0 4px 12px;
  --shadow-soft-lg: 0 10px 28px;
}

@utility shadow-soft-* {
  box-shadow: --value(--shadow-soft-*) var(--color-slate-400);
}
```

`*` qo'shilgach `shadow-soft-sm`/`-md`/`-lg` ishlaydi, qiymatlar `@theme` tokenidan o'qiladi.

</details>

**4-mashq.** Saytingizda sensorli qurilmalarda tugmalar kattaroq bo'lishi kerak. `pointer-coarse:` variantini yarating va bitta tugmada `p-2` (sichqoncha) → `p-4` (barmoq) qiling.

<details markdown="1"><summary>Yechim</summary>

```css
@custom-variant pointer-coarse (@media (pointer: coarse));
```

```html
<button class="p-2 pointer-coarse:p-4 bg-indigo-600 text-white rounded-lg">
  Boshlash
</button>
```

`@media (pointer: coarse)` qo'pol ko'rsatuvchi (barmoq) ishlatilayotganini aniqlaydi. Variant qisqa formada: `@custom-variant <nom> (<shart>);`.

</details>

**5-mashq.** `data-theme="midnight"` atributi bo'lganda ishlovchi `theme-midnight:` variantini yarating. Specificity muammosi chiqmasligi uchun to'g'ri sintaksisni ishlating va bitta blokda `bg-white` → `bg-black` qiling.

<details markdown="1"><summary>Yechim</summary>

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

```html
<html data-theme="midnight">
  <div class="bg-white theme-midnight:bg-black">...</div>
</html>
```

`&` — utility qo'llanayotgan elementning o'rni, `:where(...)` esa specificity'ni 0 ga tushiradi, shunda variant boshqa utility'larni bosib ketmaydi. Bu — [16-bobdagi](./16-dark-mode.md) `dark` variant qurilishining aynan o'zi.

</details>

**6-mashq (debugging).** Quyidagi kod ishlamayapti — `card-glow:` degan variant kutilgan edi, lekin u utility'ga aylanmagandek. Sababini toping va to'g'rilang.

```css
@variant card-glow (&:hover);

.karta {
  border-radius: 1rem;
}
```

<details markdown="1"><summary>Yechim</summary>

Variant **yaratish** uchun `@variant` emas, `@custom-variant` ishlatilishi kerak. `@variant` — mavjud variantni qo'lda yozilgan CSS **ichida qo'llash** uchun. Ikkisi almashib qolgan:

```css
/* Variant YARATISH → @custom-variant */
@custom-variant card-glow (&:hover);

/* Variantni CSS ichida QO'LLASH → @variant */
.karta {
  border-radius: 1rem;
  @variant card-glow {
    box-shadow: 0 0 18px var(--color-indigo-500);
  }
}
```

Eslang: `@custom-variant` — variant **e'lon qiladi** (bir marta); `@variant` — uni **ishlatadi**.

</details>

---

[⬅️ Oldingi: 18 — @theme bilan dizayn tizimi](./18-theme-dizayn-tizimi.md) · [🏠 README](./README.md) · [Keyingi: 20 — Direktiva va funksiyalar ➡️](./20-direktiva-funksiyalar.md)
