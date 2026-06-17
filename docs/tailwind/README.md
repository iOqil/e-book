# Tailwind CSS — 0 dan Expertgacha (o'zbek tilida)

Bu qo'llanma **Tailwind CSS** ni mutlaqo noldan professional darajagacha o'rgatadi. Birinchi bob "utility-first nima va nega?" degan savoldan boshlanadi, oxirgi bob esa to'liq responsive, dark-mode'li, hammabop (accessible) ilovani noldan quradi.

> 🎨 Kitob butunlay **Tailwind CSS v4** (2026, eng so'nggi turg'un versiya — `v4.3`) asosida yozilgan. Bu juda muhim: v4 — CSS-first sozlash (`@theme`), `@import "tailwindcss"`, Oxide dvigateli va avtomatik content-detection bilan v3 dan **butunlay farq qiladi**. Internetdagi eski darslarning aksariyati hali v3 (JS config) haqida — bu kitob esa zamonaviy yo'lni o'rgatadi.

> 📐 Har bob **SVG diagramlar** bilan boyitilgan — utility-first oqimi, spacing scale, flex/grid o'qlari, variant zanjiri, `@theme` token tizimi, dark-mode strategiyasi kabi tushunchalar ko'z bilan ko'rib o'rganiladi. Jami **26 bob, 78+ diagramma**.

> ✅ Kitobdagi har bir muhim da'vo **jonli Tailwind v4.3.1** bilan kompilyatsiya qilib tekshirilgan — yozilgan utility'lar haqiqatan ham ko'rsatilgan CSS'ni chiqaradi.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. Kod misollarini **o'zingiz yozib ko'ring** — faqat o'qib ketmang. 02-bobda bitta loyiha o'rnatamiz, qolgan boblarda shu loyihada tajriba qilasiz.
3. Har bob oxiridagi **Mashqlar**ni o'zingiz yeching, keyin `<details>` ichidagi yechimga qarang.
4. Diagrammalar tushunchani tezroq singdiradi — ularga e'tibor bering.

## Talab

| Kerak | Daraja |
|---|---|
| **HTML va CSS asoslari** (box model, flex/grid, selektor, specificity) | **Shart** |
| Kompyuter, brauzer (Chrome/Firefox/Edge) va matn muharriri (VS Code tavsiya) | Shart |
| Node.js va `npm` (terminalda ishlash) | Shart |
| JavaScript / React / Vue tajribasi | Foydali, lekin shart emas |

> ⚠️ **Tailwind — CSS o'rnini bosmaydi, CSS ustiga yoziladi.** Agar `padding`, `flexbox`, `position: absolute` yoki specificity nima ekanini bilmasangiz, avval [HTML & CSS kitobini](../html-css/README.md) o'qing. Tailwind faqat CSS yozishni **tezlashtiradi** — CSS o'rnini bosmaydi. Bu kitob siz CSS tushunchalarini bilasiz deb hisoblaydi va ularni Tailwind tilida qayta ifodalaydi.

---

## I qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Tailwind nima va nega?](./01-tailwind-nima.md) | utility-first falsafa, semantik CSS va Bootstrap bilan farqi, "uzun klass qatori" muammosiga javob, v1→v4 qisqa tarix. |
| 02 | [O'rnatish va birinchi qadamlar](./02-ornatish-birinchi-qadam.md) | Vite plugin, CLI, PostCSS va Play CDN — to'rt yo'l; `@import "tailwindcss"`; birinchi build; VS Code IntelliSense. |
| 03 | [Utility-first ish jarayoni](./03-utility-first-ish-jarayoni.md) | utility klasslar bilan "o'ylash", brauzerda tez iteratsiya, arbitrary qiymatlar `[...]`, takrorlanishni boshqarish. |
| 04 | [Spacing, sizing va o'lcham tizimi](./04-spacing-sizing.md) | `--spacing` scale, `p-*`/`m-*`/`w-*`/`h-*`/`gap-*`, dinamik qiymatlar (`mt-17`), `size-*`, manfiy qiymatlar. |

## II qism — Layout

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 05 | [Display va box model utility'lari](./05-box-model-display.md) | `block`/`inline`/`hidden`, `box-border`, border/padding/margin, `space-*`, `divide-*`. |
| 06 | [Flexbox Tailwind bilan](./06-flexbox.md) | `flex`, `flex-row/col`, `justify-*`, `items-*`, `flex-1`/`grow`/`shrink`, `gap-*`, `order-*`. |
| 07 | [CSS Grid Tailwind bilan](./07-grid.md) | `grid-cols-*`, `col-span-*`, `grid-rows-*`, `gap`, `auto-cols`, `grid-flow`, subgrid. |
| 08 | [Positioning, z-index va overflow](./08-positioning-overflow.md) | `static`/`relative`/`absolute`/`fixed`/`sticky`, `inset-*`, `z-*`, `overflow-*`, stacking. |
| 09 | [Responsive dizayn](./09-responsive-dizayn.md) | breakpoint variantlar (`sm:`/`md:`/...), mobile-first, `max-*` va range, custom breakpoint. |
| 10 | [Container queries (`@container`)](./10-container-queries.md) | v4 yadrosi: `@container`, `@sm:`/`@lg:`, `@max-*`, nomli konteynerlar — komponent o'z o'lchamiga moslashadi. |

## III qism — Ko'rinish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 11 | [Ranglar va rang tizimi](./11-ranglar.md) | OKLCH palette, `text-*`/`bg-*`/`border-*`, opacity (`/50`), `color-mix`, gradientga kirish. |
| 12 | [Tipografiya](./12-tipografiya.md) | `font-*`, `text-*` (size), `font-weight`, `leading`, `tracking`, `text-align`, `@tailwindcss/typography` (`prose`). |
| 13 | [Fon, gradient va chegara](./13-fon-gradient-border.md) | `bg-*` rasm/gradient (`bg-linear`/`radial`/`conic`), `border`, `rounded-*`, `ring-*`, `outline-*`. |
| 14 | [Soya, filter va mask](./14-soya-filter-mask.md) | `shadow-*`, `inset-shadow`, `opacity`, `blur`/`brightness` filter, `backdrop-*`, `mask-*` va `text-shadow-*` (v4.1). |

## IV qism — Interaktivlik va holatlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 15 | [Holat variantlari](./15-holat-variantlari.md) | `hover:`/`focus:`/`active:`/`disabled:`, `focus-visible`, `group`/`peer`, `data-*`/`aria-*`, `has-*`, `not-*`. |
| 16 | [Dark mode](./16-dark-mode.md) | `dark:` variant, `media` vs `class`/`selector` strategiya, `@custom-variant dark`, theme toggle (JS). |
| 17 | [Transition, transform va animatsiya](./17-transition-transform-animatsiya.md) | `transition`, `duration`/`ease`, `transform` (2D/3D: `rotate-x`, `translate-z`), `animate-*`, `@starting-style`. |

## V qism — Sozlash va kengaytirish (v4 CSS-first)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 18 | [`@theme` bilan dizayn tizimi](./18-theme-dizayn-tizimi.md) | design tokenlar, custom rang/spacing/shrift/breakpoint, `--*` o'zgaruvchilar, `@theme inline`, namespace'lar. |
| 19 | [Custom utility va variant yaratish](./19-custom-utility-variant.md) | `@utility` (statik va `*-` funksional), `--value()`/`--modifier()`, `@custom-variant`, `@variant`. |
| 20 | [Direktiva va funksiyalar](./20-direktiva-funksiyalar.md) | `@apply`, `@reference`, `--alpha()`/`--spacing()`, `@layer`, `@source`, `@import`, eski `theme()`. |
| 21 | [Plaginlar ekotizimi](./21-plaginlar.md) | rasmiy plaginlar (`typography`, `forms`), `@plugin` (eski JS plaginlar), daisyUI va boshqa komponent kutubxonalari. |

## VI qism — Komponentlar va amaliyot

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 22 | [Komponentlar va framework integratsiyasi](./22-komponentlar-framework.md) | takrorlanishni boshqarish (komponent vs `@apply`), React/Vue, `clsx`+`tailwind-merge`, `cva`, conditional klasslar. |
| 23 | [Forma va UI komponentlari amaliy](./23-forma-ui-komponentlar.md) | tugma, karta, modal, navbar, forma, badge — noldan; `@tailwindcss/forms`; holatlar va accessibility. |
| 24 | [Production: optimizatsiya va asboblar](./24-production-optimizatsiya.md) | build va minifikatsiya, content scanning, `@source`, IntelliSense, Prettier plugin, ESLint, performance. |
| 25 | [Best practices, arxitektura va migratsiya](./25-best-practices-migratsiya.md) | qachon Tailwind (qachon yo'q), jamoa konventsiyalari, tez-tez xatolar, v3 → v4 migratsiya (`@config`, upgrade tool). |

## VII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 26 | [Yakuniy loyiha: to'liq dashboard/landing](./26-capstone-loyiha.md) | o'rgangan hammasini birlashtirib — `@theme` dizayn tizimi, responsive + container queries, dark mode, animatsiya, accessible komponentlar — noldan to'liq ilova. |

---

## Tailwind — bir og'iz (kontekst uchun)

**Tailwind CSS** — bu *utility-first* CSS freymvorki. Oddiy CSS'da siz `.card { padding: 1rem; border-radius: 0.5rem; }` deb yozasiz; Tailwind'da esa to'g'ridan-to'g'ri HTML'da `class="p-4 rounded-lg"` deb yozasiz. Har bir klass — bitta kichik, o'zgarmas (atomic) CSS qoidasi.

Bu nimaga arziydi? Chunki siz **nom o'ylab topmaysiz** (`.card-inner-wrapper-left` muammosi yo'qoladi), **fayl orasida sakramaysiz** (HTML va uslub bir joyda), va dizayn **bir xil tizim** ichida qoladi (ixtiyoriy `19px` emas, `--spacing` scale'idan). Tailwind v4 esa bularning hammasini **CSS'ning o'zida** (`@theme`, `@utility`) sozlanadigan, OKLCH ranglar va container queries kabi zamonaviy platformaga tayangan dvigatel bilan beradi.

> Bu kitob Tailwind'ni "sehrli klasslar to'plami" sifatida emas, balki **siz boshqaradigan dizayn tizimi** sifatida o'rgatadi — har bir klass ortida qaysi CSS turishini bilib ishlaysiz.

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
