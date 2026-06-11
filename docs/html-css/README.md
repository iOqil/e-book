# HTML & CSS — 0 dan Expertgacha (o'zbek tilida)

Bu qo'llanma **HTML va CSS** ni mutlaqo noldan professional darajagacha o'rgatadi. Hech qanday oldingi tajriba shart emas — birinchi bob "internet qanday ishlaydi?" dan boshlanadi, oxirgi bob esa to'liq responsive sayt quradi.

> 🎨 Har bob **SVG diagramlar** bilan boyitilgan — box model, flexbox, grid, specificity, positioning kabi tushunchalar ko'z bilan ko'rib o'rganiladi. Jami 22 bob, 86+ diagramma.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'q (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. Kod misollarini **o'zing yozib ko'r** — faqat o'qib ketma. Bitta `.html` fayl yarat, brauzerда och.
3. Har bob oxiridagi **Mashqlar**ni o'zing yech, keyin `<details markdown="1">` ichidagi yechimga qara.
4. Diagrammalar tushunchani tezroq singdiradi — ularga e'tibor ber.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter va brauzer (Chrome/Firefox/Edge) | Shart |
| Matn muharriri (VS Code tavsiya etiladi) | Shart |
| Oldingi dasturlash tajribasi | **Shart emas** |

---

## I qism — HTML (struktura)

| # | Bob | Nima o'rganasan |
|---|---|---|
| 01 | [01 — Web va HTML asoslari](./01-web-html-asoslari.md) | internet va web qanday ishlashini (klient-server, brauzer, HTTP so'rov-javob, DNS, URL), HTML nimaligini va nima uchun kerakligini, brauzer sahifani qanday chizishini o'rganamiz, birinchi HTML faylimizni yaratib brauzerda ochamiz, hujjat strukturasini (doctype, html, head, body), element/teg/atribut anatomiyasini, bo'sh joy va izohlarni ko'rib chiqamiz, oxirida DevTools bilan tanishamiz. |
| 02 | [02 — Matn elementlari](./02-matn-elementlari.md) | sarlavhalar, paragraflar, ro'yxatlar va matnni belgilash elementlari yordamida matnga tuzilma va ma'no berishni o'rganamiz. |
| 03 | [03 — Havolalar va media](./03-havolalar-media.md) | havolalar (`a`) yordamida sahifalarni bog'lashni, rasmlarni (`img`) to'g'ri va tez ko'rsatishni, responsive (moslashuvchan) rasm texnikalarini, hamda audio, video, `figure` va `iframe` elementlarini noldan ekspert darajagacha o'rganamiz. |
| 04 | [04 — Jadvallar](./04-jadvallar.md) | ma'lumot jadvallari: `table`, qator, ustun va birlashtirish. |
| 05 | [05 — Formalar](./05-formalar.md) | foydalanuvchidan ma'lumot olishni o'rganamiz — `form` elementi, barcha `input` turlari va brauzer ichidagi validatsiya (tekshiruv). |
| 06 | [06 — Semantik HTML va accessibility](./06-semantik-accessibility.md) | ma'noli teglar (`header`/`nav`/`main`/`article`) bilan sahifa qurish va uni hamma — shu jumladan ko'zi ojiz, klaviatura bilan ishlovchi — odam uchun hammabop (a11y) qilish. |
| 07 | [07 — Head, meta va SEO](./07-head-meta-seo.md) | sahifaning ko'rinmas qismi — `<head>` ichidagi meta teglar, viewport, favicon, CSS/JS ulash, hamda saytni Google va ijtimoiy tarmoqlar uchun tayyorlaydigan SEO va ulashish sozlamalari. |

## II qism — CSS (ko'rinish va layout)

| # | Bob | Nima o'rganasan |
|---|---|---|
| 08 | [08 — CSS asoslari](./08-css-asoslari.md) | CSS nima ekanini, uning sintaksisi (selector, e'lon, property, value) hamda CSS ni HTMLga ulashning uch usulini (inline, internal, external) o'rganib, birinchi sahifangizni o'z qo'lingiz bilan bezaysiz. |
| 09 | [09 — Selektorlar](./09-selektorlar.md) | elementlarni aniq tanlash: tur, klass, id, kombinatorlar va psevdolar. |
| 10 | [10 — Cascade, specificity va inheritance](./10-cascade-specificity-inheritance.md) | bir nechta CSS qoidasi bitta elementga teginganda qaysi qoida g'olib chiqishini hal qiladigan uchta mexanizm — kaskad (cascade), aniqlik (specificity) va meros (inheritance) — to'liq o'rganamiz. |
| 11 | [11 — Box model](./11-box-model.md) | har bir HTML element aslida to'rt qatlamli quti ekanini (content, padding, border, margin) o'rganib, ularning o'lchami qanday hisoblanishini (`box-sizing`), `margin`/`padding`/`border` qisqa yozuvlarini, margin'lar birlashishini (margin collapse), `display` turlarini (block/inline/inline-block) va `overflow` ni to'liq tushunib olasiz. |
| 12 | [12 — O'lchovlar, tipografiya va ranglar](./12-oolchovlar-tipografiya-ranglar.md) | CSS o'lchov birliklari (px, em, rem, %, vw/vh va boshqalar), rang modellari (nomli, hex, rgb, hsl, oklch) va matnni boshqaradigan tipografiya xossalari hamda web shriftlarni to'liq, "nega"si bilan o'rganamiz. |
| 13 | [13 — Fon, chegara va soyalar](./13-fon-chegara-soyalar.md) | elementlarni jonlantiramiz — `background` (fon rangi, rasm, gradient), `border` va `border-radius` (chegara va yumaloq burchaklar), `box-shadow` (chuqurlik beruvchi soyalar), `outline` hamda `filter` bilan vizual effektlar yaratamiz. |
| 14 | [14 — Positioning va z-index](./14-positioning.md) | elementlarni joylashtirish — `static`, `relative`, `absolute`, `fixed`, `sticky` — hamda qatlamlarni boshqaruvchi `z-index` va stacking context. |
| 15 | [15 — Flexbox](./15-flexbox.md) | bir o'lchovli layout vositasi Flexbox bilan tanishamiz — flex konteyner, ikki o'q (main va cross) va elementlarni shu o'qlar bo'ylab tekislash hamda taqsimlashni 0 dan o'rganamiz. |
| 16 | [16 — CSS Grid](./16-grid.md) | sahifani ikki o'lchovda — ustun va qator panjarasi sifatida — qurishni o'rganamiz: `grid-template-columns/rows`, `fr` birligi, `repeat()`, `gap`, chiziqlarga joylashtirish, nomli sohalar (`grid-template-areas`), tekislash va `auto-fill`/`auto-fit` bilan moslashuvchan layout. |
| 17 | [17 — Responsive dizayn](./17-responsive.md) | bitta sahifani har qanday ekranga — telefon, planshet, desktop — moslashtirishni o'rganamiz: media query, mobile-first yondashuv, fluid layout va `clamp()` bilan moslashuvchan tipografiya. |
| 18 | [18 — Transitions, transforms va animatsiyalar](./18-transitions-transforms-animations.md) | harakat va o'zgarishlar — `transform` bilan elementni siljitish/aylantirish/kattalashtirish, `transition` bilan o'zgarishlarni silliq qilish va `@keyframes` bilan to'liq animatsiyalar yaratishni 0 dan o'rganamiz. |
| 19 | [19 — Zamonaviy CSS](./19-zamonaviy-css.md) | custom properties (CSS o'zgaruvchilar), `calc()`/`clamp()`, CSS nesting, `:has()` "ota" selektor, `@layer` kaskad qatlamlari va logical properties kabi zamonaviy CSS imkoniyatlarini 0 dan o'rganib, kodimizni qisqa, moslashuvchan va boshqarsa oson qilamiz. |
| 20 | [20 — CSS arxitekturasi va uslublar](./20-arxitektura-uslublar.md) | katta loyihada CSS'ni tartibli, boshqarib bo'ladigan qilib yozish — global scope va specificity muammolari nega kelib chiqishi, BEM kabi nomlash konventsiyalari, reset va normalize, fayllarni komponentlarga bo'lish, DRY, design tokens hamda utility-first (Tailwind) yondashuvini semantik usul bilan taqqoslash. |
| 21 | [21 — Formalar, UI holatlari va kirish imkoniyati](./21-amaliy-forma-ui-states.md) | formalarni chiroyli bezashni, interaktiv holatlarni (`:hover`, `:focus-visible`, `:checked` va boshqalar), dark mode'ni va kirish imkoniyatini (accessibility) o'rganamiz — sayt nafaqat ko'rkam, balki har bir foydalanuvchi uchun qulay bo'lishi uchun. |
| 22 | [22 — Yakuniy loyiha — responsive landing page](./22-capstone-loyiha.md) | shu paytgacha o'rgangan hamma narsani — semantik HTML, custom properties bilan dizayn tizimi, Grid va Flexbox, responsive, dark mode, hover/focus va animatsiya — birlashtirib, noldan to'liq ishlaydigan, ko'chirib qo'yib ishlatsa bo'ladigan responsive landing page quramiz. |

---

## HTML va CSS — bir og'iz (kontekst uchun)

- **HTML** — sahifaning **skeleti** (sarlavha, paragraf, rasm, forma). "Nima?" degan savolga javob beradi.
- **CSS** — sahifaning **ko'rinishi** (rang, joylashuv, masofa, animatsiya). "Qanday ko'rinadi?" degan savolga javob beradi.

Analogiya: HTML — uyning g'ishtlari va xonalari; CSS — bo'yoq, mebel va dizayn. Avval struktura (01–07), keyin ko'rinish (08–22).

Tayyor bo'lsang — [`01-web-html-asoslari.md`](./01-web-html-asoslari.md) dan boshla.
