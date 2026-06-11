# Daraja 0 — Tayyorgarlik

[🏠 README](./README.md) · [Keyingi: Daraja 1 — React asoslari ➡️](./01-asoslar.md)

---

React'ni o'rganishdan oldin **JavaScript'ni bilish shart**. Ko'p odam "React qiyin" deydi, aslida ularning muammosi JavaScript bilan. React — bu shunchaki JavaScript kutubxonasi.

## 0.1. Kerakli JavaScript (ES6+)

Quyidagilarni **erkin** ishlata olishingiz kerak. Agar bittasi notanish bo'lsa, avval shuni o'rganing.

### `let` va `const` (`var` emas)

```js
const PI = 3.14;      // qiymati o'zgarmaydi
let count = 0;        // qiymati o'zgaradi
count = count + 1;
```

### Arrow functions

```js
// Oddiy funksiya
function add(a, b) {
  return a + b;
}

// Arrow ko'rinishi
const add = (a, b) => a + b;

// React'da doimo shunaqa ko'rasiz:
const greet = (name) => `Salom, ${name}!`;
```

### Destructuring (eng ko'p ishlatiladi)

```js
const user = { name: "Ali", age: 25 };
const { name, age } = user;   // user.name, user.age o'rniga

const colors = ["qizil", "yashil"];
const [first, second] = colors;
```

### Spread / Rest

```js
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4];   // [1, 2, 3, 4] — nusxa olish

const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 };  // { a: 1, b: 2 }
```

> **Muhim:** React'da state'ni *hech qachon* to'g'ridan-to'g'ri o'zgartirmaymiz, balki spread bilan **yangi nusxa** yasaymiz. Bu pattern'ni hozir o'zlashtiring.

### Array metodlari: `map`, `filter`, `reduce`

```js
const nums = [1, 2, 3, 4];

const doubled = nums.map(n => n * 2);        // [2, 4, 6, 8]
const evens   = nums.filter(n => n % 2 === 0); // [2, 4]
const sum     = nums.reduce((acc, n) => acc + n, 0); // 10
```

> `map` — React'da ro'yxat chizishning asosi. Yoddan biling.

### Ternary va `&&`

```js
const status = isLoggedIn ? "Kirgan" : "Mehmon";
const greeting = isLoggedIn && "Xush kelibsiz!";
```

### Modules (import / export)

```js
// math.js
export const add = (a, b) => a + b;
export default function multiply(a, b) { return a * b; }

// app.js
import multiply, { add } from "./math.js";
```

### Promise / async-await

```js
async function getUser() {
  const res = await fetch("https://api.example.com/user");
  const data = await res.json();
  return data;
}
```

## 0.2. Muhit sozlash

1. **Node.js** o'rnating (LTS versiya, 20+). Tekshirish:
   ```bash
   node -v
   npm -v
   ```
2. **Code muharriri** — VS Code. Quyidagi extension'larni o'rnating:
   - ES7+ React/Redux/React-Native snippets
   - Prettier (kod formatlash)
   - ESLint
3. **Brauzer** — Chrome + **React Developer Tools** extension.

## 0.3. Birinchi loyiha (Vite bilan)

> ⚠️ **Create React App (CRA) o'lgan** — 2025-yilda rasman deprecated qilingan. Yangi SPA loyihalar uchun **Vite** ishlatamiz (tez, yengil, zamonaviy). Katta production ilovalar uchun keyinroq **Next.js**'ni ko'ramiz.

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

Brauzerda `http://localhost:5173` ochiladi. Tabriklaymiz — bu sizning birinchi React ilovangiz.

### Loyiha tuzilishi

```
my-app/
├── index.html        ← yagona HTML fayl (SPA)
├── package.json      ← bog'liqliklar (dependencies)
├── vite.config.js    ← Vite sozlamalari
└── src/
    ├── main.jsx       ← kirish nuqtasi (entry point)
    ├── App.jsx        ← ildiz komponent
    └── index.css
```

`src/main.jsx` — bu yerda React DOM'ga ulanadi:

```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

> `StrictMode` — development'da xatolarni topishga yordam beradi (ba'zi narsalarni 2 marta chaqiradi — bu normal, qo'rqmang).

## +20 Masala — Daraja 0

**Oson (JavaScript mashqi):**
1. `[5, 12, 8, 130, 44]` massividan 10 dan katta sonlarni `filter` bilan ajrating.
2. Ismlar massivini (`["ali", "vali"]`) `map` bilan bosh harfi kattaga aylantiring (`["Ali", "Vali"]`).
3. `reduce` bilan `[10, 20, 30]` massivining yig'indisini toping.
4. Obyektdan destructuring bilan `name` va `email`ni ajratib chiqaring.
5. Ikki massivni spread operatori bilan birlashtiring va dublikatlarni `Set` bilan olib tashlang.
6. Arrow function yozing: ikki sonni qabul qilib, kattasini qaytaradi (ternary bilan).
7. `const`, `let`, `var` farqini 3 ta misol bilan tushuntiring (kommentariy yozing).
8. Obyekt massivini (`[{id:1,name:"a"}]`) faqat `name`lar massiviga `map` bilan aylantiring.

**O'rta:**
9. `async/await` bilan `https://jsonplaceholder.typicode.com/users` dan ma'lumot oling va konsol'ga chiqaring.
10. Funksiya yozing: massiv qabul qilib, eng katta va eng kichik elementni `{min, max}` obyekt sifatida qaytarsin.
11. `map` + `filter`ni zanjir qiling: sonlar massividan juftlarini ikki barobar oshiring.
12. Obyektni spread bilan "yangilang" (bittasini o'zgartirib, qolganini saqlab) — immutable update.
13. `Promise.all` bilan 3 ta API'dan parallel ma'lumot oling.
14. `reduce` bilan obyektlar massivini ID bo'yicha guruhlang (group by).
15. Optional chaining (`?.`) va nullish coalescing (`??`) bilan xavfsiz qiymat o'qing.

**Qiyin:**
16. Vite bilan yangi loyiha yarating va `App.jsx`'da o'z ismingizni chiqaring.
17. `package.json`'dagi `dependencies` va `devDependencies` farqini yozib tushuntiring.
18. Sof JavaScript bilan kichik "todo" mantiqini yozing (qo'shish/o'chirish funksiyalari, hali UI yo'q).
19. `debounce` funksiyasini noldan yozing (keyin React'da kerak bo'ladi).
20. Closure tushunchasini misol bilan tushuntiring: counter funksiyasi yarating.

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**16 — Vite loyiha + ism:**
```jsx
// src/App.jsx
export default function App() {
  const ism = "Oqil";
  return <h1>Salom, mening ismim {ism}</h1>;
}
```
`npm create vite@latest` → React tanlang → `npm install` → `npm run dev`.

**17 — `dependencies` vs `devDependencies`:**
- **`dependencies`** — ilova ishlashi uchun kerak bo'lgan paketlar (`react`, `react-dom`). Production build'ga kiradi.
- **`devDependencies`** — faqat ishlab chiqishda kerak (`vite`, `eslint`, `vitest`). Tayyor mahsulotga kirmaydi.
- O'rnatish: `npm i react` (dependencies) vs `npm i -D vite` (devDependencies).

**18 — Todo mantiqi (sof JS, UI'siz):**
```js
let todos = [];
let nextId = 1;

function addTodo(text) {
  todos.push({ id: nextId++, text, done: false });
}
function removeTodo(id) {
  todos = todos.filter((t) => t.id !== id);
}
function toggleTodo(id) {
  todos = todos.map((t) => (t.id === id ? { ...t, done: !t.done } : t));
}
```
Diqqat: o'zgartirishda **yangi massiv/obyekt** yasaymiz (`filter`, `map`, `{...t}`) — bu React'da state yangilashning asosiy qoidasi (keyingi darajada ko'ramiz).

**19 — `debounce` noldan:**
```js
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
// Har chaqirilganda oldingi taymerni bekor qiladi — faqat "tinchlik"dan keyin ishlaydi.
// Qidiruv input'ida har harfda emas, yozib bo'lgach API chaqirish uchun ishlatamiz.
```

**20 — Closure bilan counter:**
```js
function createCounter() {
  let count = 0; // closure ichida "yashiringan", tashqaridan to'g'ridan kirib bo'lmaydi
  return {
    increment: () => ++count,
    decrement: () => --count,
    value: () => count,
  };
}
const c = createCounter();
c.increment(); c.increment();
console.log(c.value()); // 2
```
`count` faqat qaytarilgan funksiyalar orqali o'zgaradi — bu **closure**. `useState` ham xuddi shu g'oyaga asoslanadi: holat funksiya "ichida" saqlanadi.
</details>
