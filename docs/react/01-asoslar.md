# Daraja 1 — React asoslari

[⬅️ Oldingi: Daraja 0 — Tayyorgarlik](./00-tayyorgarlik.md) · [🏠 README](./README.md) · [Keyingi: Daraja 2 — Interaktivlik: State va Events ➡️](./02-state-events.md)

---

## 1.1. React nima va nega kerak?

React — foydalanuvchi interfeysi (UI) yasash uchun JavaScript kutubxonasi. Asosiy g'oyalari:

- **Komponentlar** — UI'ni mustaqil, qayta ishlatiladigan bo'laklarga bo'lamiz.
- **Deklarativ** — "qanday chizishni" emas, "nima ko'rinishi kerakligini" aytamiz. State o'zgarsa, React UI'ni o'zi yangilaydi.
- **Bir tomonlama ma'lumot oqimi** — ma'lumot yuqoridan pastga (parent → child) oqadi.

> **Backend analogiyasi (Laravel'dan):** Komponent — bu Blade component (`<x-card>`) kabi. Props — komponentga uzatilgan parametrlar. Lekin React'da hammasi brauzerda, real vaqtda yangilanadi.

## 1.2. JSX

JSX — JavaScript ichida HTML kabi yozish imkoniyati. Brauzer buni tushunmaydi, Vite uni oddiy JavaScript'ga aylantiradi.

Quyidagi diagramma JSX'ning brauzergacha bo'lgan yo'lini ko'rsatadi — u aslida `React.createElement` chaqiruviga, undan oddiy obyektga aylanadi:

![JSX qanday React element obyektiga aylanadi](rasmlar/rea-jsx-aylanish.svg)

```jsx
const element = <h1>Salom, dunyo!</h1>;
```

### JSX qoidalari

```jsx
function App() {
  const name = "Oqil";
  const isAdmin = true;

  return (
    // 1. Bitta ildiz element bo'lishi shart (yoki Fragment <>...</>)
    <div>
      {/* 2. JavaScript {} ichida yoziladi */}
      <h1>Salom, {name}!</h1>

      {/* 3. class emas, className */}
      <p className="text-lg">Matn</p>

      {/* 4. Shartli ko'rsatish */}
      {isAdmin && <button>Admin paneli</button>}

      {/* 5. Inline style — obyekt sifatida */}
      <span style={{ color: "red", fontSize: "20px" }}>Qizil</span>

      {/* 6. Teglar yopilishi shart: <img /> <br /> */}
      <img src="/logo.png" alt="Logo" />
    </div>
  );
}
```

> **Eslab qoling:** `class` → `className`, `for` → `htmlFor`, `onclick` → `onClick` (camelCase).

### Fragment

Ortiqcha `<div>` qo'shmaslik uchun:

```jsx
function List() {
  return (
    <>
      <li>Birinchi</li>
      <li>Ikkinchi</li>
    </>
  );
}
```

## 1.3. Komponentlar

Komponent — bu JSX qaytaradigan oddiy funksiya. **Nomi katta harf bilan boshlanishi shart.**

Komponentlar bir-birining ichiga joylashib, ildiz `App`'dan tarmoqlanuvchi daraxt hosil qiladi:

![Komponent daraxti: App ildizdan bola komponentlarga](rasmlar/rea-komponent-daraxti.svg)

```jsx
// Welcome.jsx
function Welcome() {
  return <h1>Xush kelibsiz!</h1>;
}

export default Welcome;
```

Ishlatish:

```jsx
import Welcome from "./Welcome.jsx";

function App() {
  return (
    <div>
      <Welcome />
      <Welcome />  {/* qayta ishlatish mumkin */}
    </div>
  );
}
```

## 1.4. Props

Props — komponentga ma'lumot uzatish usuli (HTML atributlari kabi). Props **faqat o'qish uchun** (read-only) — komponent ichida o'zgartirib bo'lmaydi.

Ma'lumot doimo ota'dan bola'ga, bir tomonlama oqadi — bola uni o'zgartira olmaydi:

![Props oqimi: otadan bolaga, bir tomonlama va faqat o'qish uchun](rasmlar/rea-props-oqimi.svg)

```jsx
// Card.jsx
function Card({ title, description }) {   // destructuring bilan
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}

// App.jsx
function App() {
  return (
    <div>
      <Card title="Birinchi" description="Tavsif 1" />
      <Card title="Ikkinchi" description="Tavsif 2" />
    </div>
  );
}
```

### `children` prop

Komponent teglari orasidagi narsa `children`ga tushadi:

```jsx
function Box({ children }) {
  return <div className="box">{children}</div>;
}

// Ishlatish:
<Box>
  <p>Bu matn children bo'lib uzatiladi</p>
</Box>
```

### Default qiymatlar

```jsx
function Button({ text = "Bosing", color = "blue" }) {
  return <button style={{ background: color }}>{text}</button>;
}
```

## 1.5. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| Komponent nomini kichik harf bilan boshlash (`card`) | Katta harf (`Card`) |
| `return` ichida bir nechta ildiz element | Fragment `<>` yoki `<div>` bilan o'rash |
| Props'ni komponent ichida o'zgartirish | Props read-only — o'zgartirmang |
| `class` ishlatish | `className` |
| Teglarni yopmaslik (`<img>`) | `<img />` |

## +20 Masala — Daraja 1

**Oson:**
1. `Greeting` komponentini yarating: "Assalomu alaykum" deb chiqarsin.
2. `Profile` komponenti yarating: `name`, `age` props'ini olib chiqarsin.
3. `Avatar` komponenti: `src` va `alt` props'ini olib `<img>` chizsin.
4. Bitta `App` ichida `Greeting`ni 3 marta chizing.
5. `Button` komponenti: `label` props'i bo'lmasa default "Bosing" chiqarsin.
6. JSX'da inline style bilan ko'k fonli quti chizing.
7. `Card` komponenti yarating va `children` orqali ichiga matn joylang.
8. Ternary bilan: `isOnline` props'iga qarab "🟢 Online" yoki "🔴 Offline" chiqarsin.

**O'rta:**
9. `UserCard`: `user` obyektini props sifatida oling (`{name, email, avatar}`) va chiroyli karta chizing.
10. `PriceTag`: `price` va `currency` props'ini olib `"$25"` formatida chiqarsin.
11. `List` komponenti yarating, ichida 5 ta `Card`ni turli props bilan chizing.
12. `Badge` komponenti: `type` props'iga (`success`/`error`/`warning`) qarab turli `className` bersin.
13. `Layout` komponenti: `header`, `footer` slot'larini props sifatida olsin (children pattern).
14. Komponentni alohida faylga ajrating va to'g'ri `import`/`export` qiling.
15. `&&` bilan: `isPremium` props bo'lsagina "⭐ Premium" belgisini ko'rsating.

**Qiyin:**
16. `Accordion` komponentining *statik* (hali interaktiv emas) versiyasini yarating — sarlavha + matn.
17. `Rating` komponenti: `value` (1-5) props'ini olib shuncha ⭐ chizsin (`Array.from` + `map`).
18. Komponentlar daraxtini quring: `App > Sidebar > MenuItem` (3 qatlam props uzatish).
19. `Table` komponenti: ustun nomlarini props sifatida olib statik jadval chizing.
20. Tashrif qog'ozi (business card) UI'sini faqat komponentlar va props bilan yarating (rasm, ism, lavozim, kontakt).

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**16 — Statik Accordion** (`children` orqali kontent):
```jsx
function Accordion({ title, children }) {
  return (
    <div className="accordion">
      <h3>{title}</h3>
      <div className="content">{children}</div>
    </div>
  );
}
// <Accordion title="Savol 1">Javob matni</Accordion>
```

**17 — Rating** (`Array.from` + `map`):
```jsx
function Rating({ value }) {
  return (
    <div>
      {Array.from({ length: value }, (_, i) => <span key={i}>⭐</span>)}
    </div>
  );
}
// <Rating value={4} />  →  ⭐⭐⭐⭐
```

**18 — Komponentlar daraxti** (3 qatlam props):
```jsx
function MenuItem({ label }) {
  return <li>{label}</li>;
}
function Sidebar({ items }) {
  return <ul>{items.map((it) => <MenuItem key={it} label={it} />)}</ul>;
}
function App() {
  return <Sidebar items={["Bosh", "Profil", "Chiqish"]} />;
}
```
Props yuqoridan pastga "oqadi": `App` → `Sidebar` (items) → `MenuItem` (label).

**19 — Statik Table** (ustunlar props):
```jsx
function Table({ columns, rows }) {
  return (
    <table>
      <thead>
        <tr>{columns.map((c) => <th key={c}>{c}</th>)}</tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr key={i}>{r.map((cell, j) => <td key={j}>{cell}</td>)}</tr>
        ))}
      </tbody>
    </table>
  );
}
```

**20 — Business card:**
```jsx
function BusinessCard({ avatar, name, role, contact }) {
  return (
    <div className="card">
      <img src={avatar} alt={name} />
      <h2>{name}</h2>
      <p>{role}</p>
      <small>{contact}</small>
    </div>
  );
}
```
Hammasini props bilan — bir komponent, har xil ma'lumot bilan qayta ishlatiladi.
</details>
