# Vue 3 + Nuxt — Zero to Hero (o'zbek tilida)

Bu qo'llanma **Vue 3 (Composition API)** va **Nuxt 3/4** ni noldan professional darajagacha o'rgatish uchun yozilgan. Har bir modul nazariya + `why` (nega shunday) + **kamida 20 ta masala** dan iborat.

> Sen backend (Laravel/DDD) tajribasi bor odamsan, shuning uchun ba'zi joylarda **Laravel/PHP analogiyalari** beriladi — yangi tushunchani eski bilim ustiga "ulash" eng tez o'rganish usuli.

---

## Qanday ishlatish kerak

1. Modullarni **tartib bilan** o'q (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. Har modul oxiridagi masalalarni **o'zing yoz**, keyin yechimga qara. Faqat o'qib ketsang — 2 haftada unutasan.
3. Har modul uchun alohida `playground` papka ochib, kod yozib ko'r:
   ```bash
   npm create vue@latest playground
   ```
4. Masalalarning ✅ belgisi bor yechimi shu faylning oxirida yoki keyingi qatorda beriladi. Belgisiz masalalar — mustaqil mashq (yechimi yo'q, ataylab).

---

## Talablar (prerequisites)

| Kerak | Daraja |
|---|---|
| JavaScript (ES6+): `let/const`, arrow fn, destructuring, modules, Promise/async-await, array methods (`map/filter/reduce`) | Yaxshi bilish shart |
| HTML/CSS | O'rta |
| Terminal, npm | Asoslar |
| TypeScript | Shart emas, lekin foydali — yo'l-yo'lakay o'rganamiz |

Agar JS'ning yuqoridagilarini yaxshi bilmasang — avval o'shani mustahkamla, aks holda Vue'da qiynalasan. Vue qiyin emas, JS zaif bo'lsa qiyin tuyuladi.

---

## To'liq dastur (roadmap)

### I qism — Vue 3 yadrosi

| № | Modul | Nima o'rganasan |
|---|---|---|
| 01 | [Vue asoslari va template syntax](./01-vue-asoslari.md) | Vue nima, SFC, Vite, direktivalar, `v-bind/v-if/v-for/v-on` |
| 02 | [Reactivity](./02-reactivity.md) | `ref`, `reactive`, `computed`, `watch`, `watchEffect`, reaktivlik ichki mexanizmi |
| 03 | [Komponentlar](./03-komponentlar.md) | `props`, `emits`, `slots`, `v-model`, `provide/inject` |
| 04 | [Composition API & Composables](./04-composition-api.md) | Lifecycle, composable yozish, advanced reactivity, `<script setup>` chuqur |
| 05 | [Vue Router](./05-vue-router.md) | Routing, nested routes, guards, lazy loading |
| 06 | [Pinia (state management)](./06-pinia.md) | Store, actions, getters, plugins, persist |

### II qism — Nuxt

| № | Modul | Nima o'rganasan |
|---|---|---|
| 07 | [Nuxt asoslari](./07-nuxt-asoslari.md) | Setup, file-based routing, layouts, auto-imports, `app.vue` |
| 08 | [Data fetching & Server (Nitro)](./08-nuxt-data-server.md) | `useFetch`, `useAsyncData`, `$fetch`, server API, middleware, `useState` |

### III qism — Nuxt UI (komponentlar kutubxonasi)

| № | Modul | Nima o'rganasan |
|---|---|---|
| 09 | [Nuxt UI: asoslar va theming](./09-nuxt-ui-asoslar.md) | O'rnatish, `UApp`, design system (color/variant/size), 3 qatlamli theming, `:ui` prop |
| 10 | [Nuxt UI komponentlari (to'liq)](./10-nuxt-ui-komponentlar.md) | 125+ komponent kategoriya bo'yicha: form (Zod), table (TanStack), overlay (`useOverlay`), dashboard |

> Nuxt UI **v4** — Nuxt UI va Pro birlashgan, butunlay bepul (`@nuxt/ui`), Reka UI + Tailwind v4 asosida. 09 — tizimni tushunish, 10 — har bir komponent.

---

> Yadro to'plam (Vue 100% + Nuxt'ning eng muhim ~70% + Nuxt UI). Hali yozilmagan, so'rasang qo'shiladigan mavzular: rendering modes (SSR/SSG/ISR/hybrid), SEO/meta chuqur, Nitro chuqur (storage/caching), modules ecosystem, testing (Vitest), deployment (VPS/Nginx/Docker), TypeScript chuqur, performance — barchasi shu modullar uslubida.

---

## Vue vs React — bir og'iz (kontekst uchun)

Vue va React bir muammoni hal qiladi: **UI = f(state)**. Farqi:

- **React** — "hammasi JavaScript". JSX, manual re-render optimizatsiya (`useMemo`, `useCallback`).
- **Vue** — template + **avtomatik reaktivlik** (Proxy asosida). Ko'p narsa "o'zi" optimallashadi. Kamroq boilerplate.

Laravel termini bilan: React — "hamma narsani qo'lda yig'asan", Vue — "framework ko'p ishni convention bilan o'zi qiladi" (Laravel'ning "convention over configuration" falsafasiga yaqin).

---

## Vue ekotizimi xaritasi

```
Vue 3 (core)
 ├── Vue Router      → sahifalar orasida navigatsiya (SPA)
 ├── Pinia           → global state (Vuex'ning vorisi)
 ├── Vite            → build tool / dev server (Webpack vorisi, juda tez)
 └── Nuxt            → "Vue uchun Laravel" — fullstack meta-framework
                       (SSR, routing, server API, auto-import hammasi tayyor)
```

Tayyor bo'lsang — `01-vue-asoslari.md` dan boshla.
