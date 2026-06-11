# Daraja 8 — Advanced patterns

[⬅️ Oldingi: Daraja 7 — Performance optimizatsiya](./07-performance.md) · [🏠 README](./README.md) · [Keyingi: Daraja 9 — TypeScript bilan React ➡️](./09-typescript.md)

---

Bu darajada professional kutubxonalar (Radix, shadcn/ui) ichida ishlatiladigan patternlarni o'rganasiz.

## 8.1. Compound components

Bir-biriga bog'liq komponentlar guruhi (masalan `<Select>`, `<Select.Option>`). HTML'dagi `<select>`/`<option>` kabi.

```jsx
import { createContext, useContext, useState } from "react";

const TabsContext = createContext();

function Tabs({ children, defaultValue }) {
  const [active, setActive] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ value, children }) {
  const { active, setActive } = useContext(TabsContext);
  return (
    <button
      className={active === value ? "active" : ""}
      onClick={() => setActive(value)}
    >
      {children}
    </button>
  );
}

function TabPanel({ value, children }) {
  const { active } = useContext(TabsContext);
  return active === value ? <div>{children}</div> : null;
}

// Birikma
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Ishlatish — chiroyli, deklarativ API
<Tabs defaultValue="1">
  <Tabs.List>
    <Tabs.Tab value="1">Birinchi</Tabs.Tab>
    <Tabs.Tab value="2">Ikkinchi</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="1">Birinchi kontent</Tabs.Panel>
  <Tabs.Panel value="2">Ikkinchi kontent</Tabs.Panel>
</Tabs>
```

## 8.2. Render props

Komponent o'z renderini funksiya orqali tashqariga beradi.

```jsx
function MouseTracker({ render }) {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  return (
    <div onMouseMove={(e) => setPos({ x: e.clientX, y: e.clientY })}>
      {render(pos)}
    </div>
  );
}

// Ishlatish
<MouseTracker render={({ x, y }) => <p>{x}, {y}</p>} />
```

> **Eslatma:** Render props'ning ko'p holatlarini hozir **custom hooks** soddaroq hal qiladi. Lekin ba'zi kutubxonalar (masalan eski form liblari) buni ishlatadi — tanib olishingiz kerak.

## 8.3. Higher-Order Components (HOC)

Komponentni qabul qilib, kuchaytirilgan komponent qaytaruvchi funksiya.

```jsx
function withLoading(Component) {
  return function WithLoading({ isLoading, ...props }) {
    if (isLoading) return <p>Yuklanmoqda...</p>;
    return <Component {...props} />;
  };
}

const UserListWithLoading = withLoading(UserList);
```

> **Zamonaviy holat:** HOC ham asosan custom hooks bilan almashtirildi. Lekin legacy kodda (`connect` Redux'da, `withRouter`) uchraydi. Bilib qo'ying, lekin yangi kodda hook'larni afzal ko'ring.

Quyidagi diagramma ikki patternni solishtiradi: compound components (qismlar Context bilan bog'lanadi) va HOC (komponentni o'rab funksiya qo'shadi):

![Compound components va HOC: komponentni o'rab kuchaytirish](rasmlar/rec-compound-hoc.svg)

## 8.4. Portals

Komponentni DOM daraxtining boshqa joyiga "uchirish" (modal, tooltip uchun — `overflow: hidden`dan qutulish).

```jsx
import { createPortal } from "react-dom";

function Modal({ children, onClose }) {
  return createPortal(
    <div className="overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.body  // <body> ga chiqariladi
  );
}
```

## 8.5. Error Boundaries

JavaScript xatosi butun ilovani buzmasligi uchun "qo'riqchi" komponent.

```jsx
import { Component } from "react";

class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    // log servisiga yuborish (Sentry kabi)
    console.error(error, info);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Nimadir xato ketdi 😢</h1>;
    }
    return this.props.children;
  }
}

// Ishlatish
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

> Error Boundary — hozircha **faqat class component** sifatida yoziladi (yoki `react-error-boundary` kutubxonasi bilan). Bu React'da class kerak bo'ladigan kam joylardan biri.

Quyidagi diagramma Error Boundary ishini ko'rsatadi: bola komponentda xato bo'lsa, fallback UI ko'rsatiladi va butun ilova qulamaydi:

![Error Boundary: bola'da xato bo'lsa fallback UI ko'rsatiladi](rasmlar/rec-error-boundary.svg)

## 8.6. Boshqa muhim patternlar

- **Controlled vs Uncontrolled komponentlar** — komponentingiz har ikki rejimni qo'llab-quvvatlashi mumkin.
- **Slot pattern** — `header`, `footer`ni prop sifatida (`children`dan tashqari).
- **Provider pattern** — Context bilan global servis berish.
- **State reducer pattern** — foydalanuvchiga state mantig'ini override qilish imkonini berish.

## 8.7. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| Hamma joyda HOC/render props | Avval custom hook'ni o'ylang |
| Modal'ni portal'siz chizish | `createPortal` + `document.body` |
| Error boundary'siz ilova | Ildizga (va kalit joylarga) qo'ying |
| Compound'da Context'ni unutish | Holatni Context orqali ulang |
| Portal'da event bubbling'ni e'tibordan qoldirish | `stopPropagation` kerak bo'lishi mumkin |

## +20 Masala — Daraja 8

**Oson:**
1. `createPortal` bilan oddiy modal yarating.
2. Modal'ni overlay bosilganda yopiladigan qiling.
3. `withLoading` HOC yozing va ro'yxatda ishlating.
4. Render props bilan sichqoncha pozitsiyasini ko'rsating.
5. Tooltip komponentini portal bilan yarating.
6. Error Boundary yozing va atayin xato chiqarib sinab ko'ring.
7. `children` + slot pattern bilan `Layout` yarating.
8. Toast notification'ni portal bilan ko'rsating.

**O'rta:**
9. Compound component: `<Tabs>` to'liq tizimini yarating.
10. Compound: `<Accordion>` bir nechta paneli bilan.
11. `withAuth` HOC: login bo'lmasa boshqa narsa ko'rsatsin.
12. Render props bilan `<DataFetcher>` (loading/error/data).
13. Confirmation modal: "Ishonchingiz komilmi?" + portal.
14. Error Boundary'ni `react-error-boundary` bilan + "Qayta urinish" tugmasi.
15. Controlled + uncontrolled ikkalasini qo'llab-quvvatlovchi `<Input>`.

**Qiyin:**
16. To'liq `<Select>` compound komponenti (klaviatura navigatsiyasi bilan).
17. `<Modal>` tizimi: stack (bir nechta modal), focus trap.
18. Compound `<Form>`: `<Form.Field>`, `<Form.Error>`, Context bilan.
19. Plugin tizimi: Provider pattern bilan kengaytiriladigan komponent.
20. Dropdown menyu: portal + click-outside + klaviatura + a11y (accessibility).

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**16 — Compound `<Select>`** (Context bilan qismlar bog'lanadi):
```jsx
const SelectCtx = createContext(null);

function Select({ value, onChange, children }) {
  const [open, setOpen] = useState(false);
  return (
    <SelectCtx.Provider value={{ value, onChange, open, setOpen }}>
      <div className="select">{children}</div>
    </SelectCtx.Provider>
  );
}
Select.Trigger = function () {
  const { value, open, setOpen } = useContext(SelectCtx);
  return <button onClick={() => setOpen(!open)}>{value ?? "Tanlang"}</button>;
};
Select.Option = function ({ value: v, children }) {
  const { onChange, setOpen } = useContext(SelectCtx);
  return <div onClick={() => { onChange(v); setOpen(false); }}>{children}</div>;
};
// <Select value={v} onChange={setV}><Select.Trigger/><Select.Option value="a">A</Select.Option></Select>
```
Qismlar (`Trigger`, `Option`) Context orqali bog'lanadi — foydalanuvchi ularni erkin joylashtiradi.

**18 — Compound `<Form>`** (`Form.Field`, `Form.Error`):
```jsx
const FormCtx = createContext(null);

function Form({ children, onSubmit }) {
  const [errors, setErrors] = useState({});
  return (
    <FormCtx.Provider value={{ errors, setErrors }}>
      <form onSubmit={onSubmit}>{children}</form>
    </FormCtx.Provider>
  );
}
Form.Field = ({ name, children }) => <div data-name={name}>{children}</div>;
Form.Error = ({ name }) => {
  const { errors } = useContext(FormCtx);
  return errors[name] ? <span className="error">{errors[name]}</span> : null;
};
```

**20 — Dropdown** (portal + click-outside):
```jsx
function Dropdown({ trigger, children }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function onClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    if (open) document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, [open]);

  return (
    <div ref={ref} style={{ position: "relative" }}>
      <button onClick={() => setOpen((o) => !o)} aria-haspopup="menu" aria-expanded={open}>
        {trigger}
      </button>
      {open && createPortal(
        <div className="menu" role="menu">{children}</div>,
        document.body
      )}
    </div>
  );
}
```
`createPortal` menyuni `document.body`ga chiqaradi (`overflow:hidden` ota element kesib qo'ymaydi); click-outside `mousedown` listener bilan; `aria-*` — a11y. Klaviatura uchun (↑/↓/Esc) `onKeyDown` qo'shiladi.

> **Maslahat:** real loyihada bularning hammasini noldan yozish o'rniga **Radix UI** / **shadcn/ui** ishlating — a11y va klaviatura tayyor. Lekin "ostida qanday ishlashini" bilish uchun bir marta o'zing yozib ko'r.
</details>
