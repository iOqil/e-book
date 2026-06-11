# Daraja 7 — Performance optimizatsiya

[⬅️ Oldingi: Daraja 6 — State management](./06-state-management.md) · [🏠 README](./README.md) · [Keyingi: Daraja 8 — Advanced patterns ➡️](./08-advanced-patterns.md)

---

> **Oltin qoida:** Avval o'lchang (profiling), keyin optimallashtiring. Premature optimization — yovuzlik.

## 7.1. Re-render qachon bo'ladi?

Komponent qayta render bo'ladi agar: (1) uning state'i o'zgarsa, (2) props'i o'zgarsa, (3) ota-onasi re-render bo'lsa.

Render o'zi ikki fazaga bo'linadi — quyidagi diagramma Render fazasi (virtual DOM diff/reconciliation) va Commit fazasini (DOM yangilash) ko'rsatadi:

![React render fazalari: Render fazasi, reconciliation, Commit fazasi, DOM](rasmlar/rec-render-fazalari.svg)

## 7.2. `React.memo` — keraksiz re-render'ni to'xtatish

```jsx
import { memo } from "react";

// Props o'zgarmasa, qayta render bo'lmaydi
const ExpensiveChild = memo(function ExpensiveChild({ data }) {
  console.log("render!");
  return <div>{data}</div>;
});
```

`memo` + `useCallback`/`useMemo` birgalikda ishlaydi (props referencelari barqaror bo'lishi uchun).

Quyidagi diagramma re-render kaskadini (ota re-render bo'lsa bolalar ham) va `React.memo` keraksiz re-render'ni qanday to'sishini ko'rsatadi:

![Re-render kaskadi va React.memo keraksiz re-render'ni to'sishi](rasmlar/rec-rerender-cascade-memo.svg)

## 7.3. React Compiler (2026 yangiligi)

> **Eng muhim yangilik:** React 19 bilan kelgan **React Compiler** memoizatsiyani **avtomatik** qiladi. Kelajakda `React.memo`, `useMemo`, `useCallback`ni qo'lda yozish deyarli kerak emas — compiler buni o'zi optimallashtiradi. Yangi loyihalarda compiler'ni yoqing va manual memoizatsiyani minimal qiling.

```js
// vite.config.js (React Compiler yoqish)
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [
    react({
      babel: { plugins: [["babel-plugin-react-compiler"]] },
    }),
  ],
});
```

## 7.4. Code splitting va lazy loading

Boshida butun ilovani yuklamasdan, kerak bo'lganda yuklang.

```jsx
import { lazy, Suspense } from "react";

const Dashboard = lazy(() => import("./Dashboard"));

function App() {
  return (
    <Suspense fallback={<p>Yuklanmoqda...</p>}>
      <Dashboard />
    </Suspense>
  );
}
```

Route darajasida code splitting — eng samarali (har sahifa alohida bundle).

## 7.5. Ro'yxatlarni virtualizatsiya

10000 element bo'lsa, hammasini chizmang — faqat ekrandagisini. **`@tanstack/react-virtual`** ishlatiladi.

## 7.6. Boshqa texnikalar

- **Lift content up / push state down** — state'ni iloji boricha pastga tushiring (kichikroq daraxt re-render bo'ladi).
- **`children` prop** — o'zgarmaydigan qismni `children` qilib uzating (re-render'dan saqlanadi).
- **Debounce/throttle** — tez-tez ishlaydigan eventlar (scroll, qidiruv) uchun.
- **Image lazy loading** — `<img loading="lazy" />`.

## 7.7. Profiling (o'lchash)

React DevTools'da **Profiler** tab'i — qaysi komponent qancha render bo'lganini ko'rsatadi. React 19.2'da Chrome DevTools'ga **Performance Tracks** qo'shildi.

## 7.8. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| Profiling'siz optimallashtirishga urinish | Avval o'lchang |
| Hamma joyga `memo`/`useMemo` | Faqat kerakli joyda |
| `memo` + har render'da yangi funksiya/obyekt props | `useCallback`/`useMemo` bilan barqarorlash |
| Katta ro'yxatni virtualizatsiyasiz chizish | `react-virtual` |
| Butun ilovani bitta bundle qilish | Route-level code splitting |

## +20 Masala — Daraja 7

**Oson:**
1. `console.log` bilan komponent necha marta render bo'lganini kuzating.
2. `React.memo` qo'shib, keraksiz re-render'ni to'xtating.
3. Profiler bilan eng ko'p render bo'lgan komponentni toping.
4. `<img loading="lazy" />` bilan rasmlarni kechiktirib yuklang.
5. Tugmaning funksiyasini `useCallback`ga o'rang.
6. Qimmat hisobni `useMemo`ga o'rang.
7. State'ni pastroqqa tushirib (push state down) re-render hududini kichraytiring.
8. `children` prop bilan o'zgarmas qismni re-render'dan saqlang.

**O'rta:**
9. `lazy` + `Suspense` bilan komponentni kechiktirib yuklang.
10. Har bir route'ni code splitting qiling.
11. Qidiruvni debounce bilan optimallashtiring.
12. 1000 elementli ro'yxatda `memo`'siz va `memo` bilan farqni o'lchang.
13. `useMemo` bilan og'ir filtrlash/saralashni optimallashtiring.
14. React Compiler'ni Vite loyihasiga yoqing.
15. Scroll eventini throttle bilan optimallashtiring.

**Qiyin:**
16. `react-virtual` bilan 10000 qatorli jadvalni virtualizatsiya qiling.
17. Lighthouse/DevTools bilan bundle hajmini kamaytiring.
18. Murakkab dashboard'ni profiling qilib, render shovqinlarini tozalang.
19. Image lazy loading + blur placeholder (progressive yuklash).
20. Katta forma performance'ini optimallashtiring (har keystroke'da butun forma re-render bo'lmasin).

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**16 — Virtualizatsiya** (`@tanstack/react-virtual`):
```jsx
import { useVirtualizer } from "@tanstack/react-virtual";

function VirtualList({ rows }) {
  const parentRef = useRef(null);
  const v = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 35,
  });
  return (
    <div ref={parentRef} style={{ height: 400, overflow: "auto" }}>
      <div style={{ height: v.getTotalSize(), position: "relative" }}>
        {v.getVirtualItems().map((item) => (
          <div key={item.key} style={{ position: "absolute", transform: `translateY(${item.start}px)` }}>
            {rows[item.index]}
          </div>
        ))}
      </div>
    </div>
  );
}
```
10000 qatordan faqat ko'rinadigan ~15 tasi DOM'da bo'ladi — qolgani "virtual".

**20 — Katta forma perf** (har maydonni `memo` bilan ajratish):
```jsx
const Field = memo(function Field({ label, value, onChange }) {
  return <label>{label}<input value={value} onChange={onChange} /></label>;
});

function FastForm() {
  const [form, setForm] = useState({ ism: "", email: "" });
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  return (
    <>
      <Field label="Ism" value={form.ism} onChange={set("ism")} />
      <Field label="Email" value={form.email} onChange={set("email")} />
    </>
  );
}
```
`memo` tufayli faqat o'zgargan maydon qayta render bo'ladi. (Yoki React Hook Form — u uncontrolled bo'lib, keystroke'da re-render qilmaydi.)

**17–19 — jarayon (kod emas, texnika):**
- **17 (bundle):** `npm run build` → bundle analizatori (`rollup-plugin-visualizer`); katta paketlarni `lazy` import qiling, ishlatilmaganini olib tashlang.
- **18 (profiling):** React DevTools → **Profiler** tab → yozib oling, qaysi komponent ko'p/keraksiz render bo'layotganini toping → `memo`/`useMemo`/`useCallback` qo'llang.
- **19 (image):** `loading="lazy"` atributi + kichik blur rasm (`placeholder`) → asl rasm yuklangach almashtirish.

> **Eslatma:** React Compiler (2026) `memo`/`useMemo`/`useCallback` ehtiyojini ko'p holatda avtomatik bartaraf etadi — avval profiling qiling, keyin kerak bo'lsa qo'lda optimallashtiring.
</details>
