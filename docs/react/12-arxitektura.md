# Daraja 12 — Expert: Arxitektura va scaling

[⬅️ Oldingi: Daraja 11 — Production va ekotizim](./11-production.md) · [🏠 README](./README.md)

---

Bu darajada siz endi sintaksis emas, **qarorlar** haqida o'ylaysiz. Expert React dasturchisini ajratib turadigan narsa — kod yozish emas, *to'g'ri arxitektura tanlash*.

## 12.1. Loyiha strukturasi — feature-based

Kichik loyihalar `components/`, `hooks/`, `utils/` bilan boshlanadi. Lekin o'sganda **xususiyat (feature) bo'yicha** tashkil qiling:

```
src/
├── app/                    ← routing, providerlar
├── shared/                 ← umumiy (ui, lib, hooks, api)
│   ├── ui/                 ← Button, Input, Modal (dizayn tizimi)
│   ├── lib/                ← yordamchilar
│   └── api/                ← API mijoz (axios/fetch wrapper)
├── features/               ← biznes xususiyatlari
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── model/          ← state, tiplar
│   ├── students/
│   └── payments/
└── pages/                  ← sahifalar (feature'larni birlashtiradi)
```

> **DDD bilan bog'liqlik:** Bu **Feature-Sliced Design (FSD)** — frontend'ning DDD'siga eng yaqin metodologiya. Sizning backend tajribangiz (bounded context, domain ajratish) bu yerda to'g'ridan-to'g'ri qo'l keladi. Har bir `feature` — bu o'z domeniga ega modul. Qatlamlar orasida qat'iy bog'liqlik qoidalari (yuqori qatlam pastni biladi, aksincha emas).

## 12.2. Komponentlarni tashkil etish prinsiplari

- **Container vs Presentational** — mantiq (data fetching, state) va ko'rinish (sof UI)ni ajrating. Presentational komponentlar testlash va qayta ishlatish oson.
- **Single Responsibility** — bitta komponent bitta ishni qilsin. 200+ qatorli komponent — refactoring signali.
- **Composition over configuration** — 20 ta props o'rniga `children` va compound pattern.
- **Colocation** — bog'liq fayllarni yonma-yon saqlang (komponent + test + style + hook).

## 12.3. Dizayn tizimi (Design System)

Production ilova izchil UI talab qiladi. **shadcn/ui** (Radix asosida) — 2026'ning standarti: komponentlarni *loyihangizga ko'chirib olasiz* (kutubxona emas, kod), to'liq nazorat.

- Design tokens (rang, masofa, shrift) — markazlashtirilgan.
- Accessible by default (Radix primitivlar).
- Tailwind bilan birga.

## 12.4. Ilg'or React 19 imkoniyatlari

- **`use` hook** — Promise yoki Context'ni "ochish" (Suspense bilan).
  ```tsx
  import { use } from "react";
  function Comments({ commentsPromise }) {
    const comments = use(commentsPromise);  // Suspense bilan kutadi
    return <ul>{comments.map(...)}</ul>;
  }
  ```
- **`useEffectEvent`** (19.2) — effect ichidagi "reaktiv bo'lmagan" mantiqni ajratish (dependency muammosini hal qiladi).
- **Activity API** (19.2) — ko'rinmas qismlarni "to'xtatib qo'yish" (state'ni saqlab, renderni pauza qilish).
- **Partial Pre-rendering** — statik qismni CDN'dan, dinamikni keyin.

## 12.5. Scaling muammolari va yechimlari

| Muammo | Yechim |
|--------|--------|
| Katta bundle | Route splitting, tree shaking, dynamic import |
| Sekin ro'yxatlar | Virtualizatsiya (`react-virtual`) |
| Re-render shovqini | React Compiler, profiling, state'ni pastga |
| Prop drilling | Context (DI), Zustand |
| Server-client state chalkashligi | TanStack Query + Zustand ajratish |
| Izchilliksiz UI | Dizayn tizimi |
| Sekin birinchi yuklanish | SSR/RSC, streaming, code splitting |
| Murakkab forma logikasi | React Hook Form + Zod |

## 12.6. Monorepo va katta jamoa

- **Turbopack / Turborepo / Nx** — bir nechta ilova/paket bitta repo'da (web + admin + mobil shared kod).
- **Storybook** — komponentlarni izolyatsiyada ishlab chiqish va hujjatlash.
- **CI/CD** — har PR'da test + lint + type-check + build.
- **Conventional commits + changesets** — versiyalash.

## 12.7. Expert'ning fikrlash tarzi

1. **YAGNI** — kelajakda kerak bo'lishi *mumkin* degan narsani qo'shmang.
2. **Premature abstraction'dan qoching** — 3 marta takrorlangach abstraksiya qiling (rule of three).
3. **Performance — o'lchovga asoslangan** — taxmin emas, profiling.
4. **Accessibility — ixtiyoriy emas** — semantik HTML, ARIA, klaviatura.
5. **Server-first fikrlash** — brauzerga iloji boricha kam ish va JS yuboring.
6. **Tip xavfsizligi uchtadan** — TypeScript + Zod (runtime) + test.
7. **Trade-off'larni ayting** — har qaror narxga ega; uni ochiq bayon qiling.

## 12.8. Keng tarqalgan xatolar (expert darajada)

| Xato | To'g'risi |
|------|-----------|
| Boshidanoq murakkab arxitektura | Sodda boshlang, o'sgani sayin bo'ling |
| Hamma narsani abstraksiya qilish | Rule of three |
| Texnologiya tanlovini "hype" bilan | Loyiha ehtiyojiga ko'ra |
| Accessibility'ni keyinga qoldirish | Boshidan rejalashtiring |
| Test'ni "vaqt yo'q" deb tashlab qo'yish | Sifat = tezlik (uzoq muddatda) |

## +20 Masala — Daraja 12

**Oson (struktura):**
1. Mavjud loyihani feature-based strukturaga qayta tashkil eting.
2. `shared/ui` papkasiga 5 ta qayta ishlatiladigan komponent ajrating.
3. API mijozini (axios wrapper) markazlashtiring.
4. Container va Presentational komponentlarni ajrating.
5. Bitta katta komponentni (200+ qator) kichiklarga bo'ling.
6. Dizayn tokenlarni (rang, masofa) markazlashtiring.
7. Colocation prinsipini qo'llang (komponent + test + style yonma-yon).
8. shadcn/ui'ni loyihaga o'rnating va Button'ni sozlang.

**O'rta:**
9. Feature-Sliced Design qoidalarini loyihada qo'llang (qatlam bog'liqliklari).
10. Storybook o'rnating va 5 komponentni hujjatlang.
11. `use` hook + Suspense bilan ma'lumot oling.
12. React Compiler'ni yoqib, eski memo'larni tozalang.
13. Murakkab formani RHF + Zod bilan refactor qiling.
14. CI pipeline yozing (lint + type-check + test + build).
15. Bundle analyzer bilan eng katta paketlarni toping va kamaytiring.

**Qiyin:**
16. EduCore'ning to'liq frontend arxitekturasini loyihalang (FSD, multi-tenant, dizayn tizimi).
17. Monorepo quring: web + admin + shared paket (Turborepo).
18. To'liq dizayn tizimi yarating (tokenlar, komponentlar, Storybook, hujjat).
19. SSR + streaming + RSC bilan optimal yuklanadigan dashboard quring.
20. **Capstone:** o'z stack'ingizda (Laravel API + Next.js) to'liq production ilova: auth, CRUD, RBAC, payments, test, deploy, monitoring.

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20) — yo'nalish va qarorlar</summary>

Bu daraja mashqlari — **kod parchasi emas, arxitektura qarorlari**. Yechim — to'g'ri tuzilma va prinsiplar:

**16 — Feature-Sliced Design (FSD) tuzilma:**
```
src/
├── app/          # provayderlar, router, global stillar
├── pages/        # sahifalar (route'lar yig'iladi)
├── widgets/      # mustaqil UI bloklar (Header, Sidebar)
├── features/     # foydalanuvchi amallari (auth, add-student)
├── entities/     # biznes obyektlar (student, payment, tenant)
└── shared/       # ui-kit, api, lib, config (hammaga umumiy)
```
Qoida: yuqori qatlam pastdagiga bog'lanadi, teskari emas (`features` → `entities` → `shared`). Multi-tenant: `shared/api`da tenant `baseURL`/header markazlashtiriladi.

**17 — Monorepo (Turborepo):**
```
apps/        web/ (mijoz), admin/ (boshqaruv)
packages/    ui/ (umumiy komponentlar), config/ (eslint/ts), types/ (umumiy tiplar)
```
`turbo.json` da build/lint pipeline; umumiy kod `packages/`da, ikki ilova ham ishlatadi.

**18 — Dizayn tizimi:** tokenlar (rang/spacing/typography CSS o'zgaruvchilar) → primitiv komponentlar (Button, Input) → **Storybook**da har birini hujjatlash + vizual test.

**19 — SSR + streaming + RSC:** Server Components'da ma'lumot oling, sekin qismlarni `<Suspense>`ga o'rab **stream** qiling (sahifa qism-qism keladi) — foydalanuvchi tez kontentni darrov ko'radi.

**20 — Capstone checklist** (production ilova):
- ✅ Auth (token/session) + **RBAC** (rol-asosli ruxsat, route + UI darajasida)
- ✅ CRUD (TanStack Query + optimistik yangilash)
- ✅ Validatsiya (Zod — client + server)
- ✅ Test (unit + integration + 1-2 E2E kritik yo'l uchun)
- ✅ Xato kuzatuvi (error boundary + Sentry kabi monitoring)
- ✅ CI/CD (lint + test + build → deploy)
- ✅ Performance (lazy, code splitting, profiling)

> **Expert sirri:** kod yozish emas — **to'g'ri qaror qabul qilish** muhim. "Bu yerda Context yetadimi yoki Zustand kerakmi?", "Bu komponentni bo'lish kerakmi?" — tajriba shu savollarga tez javob berishdir.
</details>

---

# Xulosa va keyingi qadamlar

Agar siz bu yo'lni oxirigacha bosib o'tib, har darajaning 20 masalasini yechgan bo'lsangiz — endi siz **junior emas, mustaqil React dasturchisi**siz. Eslab qoling:

- **Hujjatlar — eng yaxshi do'st:** [react.dev](https://react.dev) — rasmiy, eng sifatli manba. Yangi React 19 patternlari shu yerda.
- **O'qish ≠ bilish.** Faqat loyiha qurib o'rganasiz. Har darajadan keyin o'z loyihangizni qiling.
- **Ekotizim tez o'zgaradi, asoslar — yo'q.** Komponent, state, ma'lumot oqimi tushunchalari abadiy. Kutubxonalar almashadi.
- **2026 mentaliteti:** server-first, kam global state, `useEffect` — oxirgi chora, tip xavfsizligi standart.

## Tavsiya etilgan o'rganish tartibi (takror)

```
JavaScript (ES6+) → React asoslari → Hooks → Formalar/API
   → Routing → State management (Query + Zustand)
   → Performance → Patterns → TypeScript → Testing
   → Next.js/RSC → Arxitektura
```

## Foydali resurslar

- **Rasmiy:** react.dev, nextjs.org, tanstack.com/query
- **Kutubxonalar:** React Router, Zustand, React Hook Form, Zod, shadcn/ui, Radix UI
- **Testing:** Vitest, React Testing Library, Playwright, MSW
- **Amaliyot:** har darajada o'z mini-loyihangiz; oxirida bitta to'liq portfolio ilovasi

## Loyiha g'oyalari (portfolio uchun)

1. To'liq Todo/Notes ilovasi (CRUD + localStorage + filter)
2. Ob-havo ilovasi (API + qidiruv + favorites)
3. E-commerce mini-do'kon (savatcha + Zustand + checkout)
4. Blog platformasi (Next.js + RSC + Server Actions)
5. Dashboard (jadval + grafik + filter + virtualizatsiya)
6. EduCore moduli (sizning real loyihangiz — eng yaxshi mashq!)

---

> **Muallifga eslatma (juniorlarga o'rgatish uchun):** Bu qo'llanmani kurs sifatida ishlatsangiz, har darajani 1-2 hafta deb rejalashtiring (0-7 darajalar — asosiy kurs, 8-12 — ilg'or modul). Masalalarni uy vazifasi qiling, har darajada bitta kichik loyiha topshiring. Live coding'da "Keng tarqalgan xatolar" jadvallarini ko'rsatish juda samarali — talabalar aynan shu xatolarni qiladi.

**Omad! React — o'rganishga arziydigan, kuchli vosita. 🚀**
