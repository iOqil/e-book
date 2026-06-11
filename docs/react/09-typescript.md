# Daraja 9 — TypeScript bilan React

[⬅️ Oldingi: Daraja 8 — Advanced patterns](./08-advanced-patterns.md) · [🏠 README](./README.md) · [Keyingi: Daraja 10 — Testing ➡️](./10-testing.md)

---

TypeScript — JavaScript'ga tip qo'shadi. Xatolarni *yozish paytida* topadi, refactoring'ni xavfsiz qiladi. **2026'da professional React = TypeScript.**

```bash
npm create vite@latest my-app -- --template react-ts
```

## 9.1. Props'ni tiplash

```tsx
type ButtonProps = {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";  // ixtiyoriy
  disabled?: boolean;
};

function Button({ label, onClick, variant = "primary", disabled }: ButtonProps) {
  return (
    <button className={variant} onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

`children` bilan:

```tsx
type CardProps = {
  title: string;
  children: React.ReactNode;  // har qanday JSX
};

function Card({ title, children }: CardProps) {
  return <div><h2>{title}</h2>{children}</div>;
}
```

## 9.2. Hook'larni tiplash

```tsx
// useState — odatda tip o'zi aniqlanadi (inference)
const [count, setCount] = useState(0);          // number
const [name, setName] = useState("");           // string

// Murakkab tip bo'lsa — aniq belgilang
const [user, setUser] = useState<User | null>(null);

type User = { id: number; name: string };

// useRef
const inputRef = useRef<HTMLInputElement>(null);

// useReducer
type State = { count: number };
type Action = { type: "inc" } | { type: "dec" } | { type: "set"; payload: number };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "inc": return { count: state.count + 1 };
    case "dec": return { count: state.count - 1 };
    case "set": return { count: action.payload };
  }
}
```

## 9.3. Event'larni tiplash

```tsx
function Form() {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  };

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {};
}
```

## 9.4. Generic komponentlar

```tsx
type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
};

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map((item, i) => <li key={i}>{renderItem(item)}</li>)}</ul>;
}

// Ishlatish — tip avtomatik aniqlanadi
<List items={users} renderItem={(u) => u.name} />
```

## 9.5. Custom hook'ni tiplash

```tsx
function useToggle(initial = false): [boolean, () => void] {
  const [value, setValue] = useState(initial);
  const toggle = () => setValue((v) => !v);
  return [value, toggle];
}
```

## 9.6. Foydali utility tiplar

- `React.ReactNode` — har qanday renderlanadigan narsa
- `React.FC<Props>` — function component (lekin hozir to'g'ridan-to'g'ri annotatsiya afzal)
- `Partial<T>`, `Pick<T>`, `Omit<T>` — tiplarni qayta shakllantirish
- `ComponentProps<"button">` — HTML element propslarini olish

```tsx
// Native button propslarini meros qilib olish
type Props = React.ComponentProps<"button"> & { variant: "primary" };
```

## 9.7. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| `any` ishlatish | Aniq tip bering yoki `unknown` |
| `React.FC`ni majburlash | To'g'ridan-to'g'ri props annotatsiyasi |
| Event tipini noto'g'ri tanlash | `ChangeEvent`, `MouseEvent`, `FormEvent` |
| `useState`ga tip bermaslik (null bo'lsa) | `useState<T \| null>(null)` |
| API javobini tiplab olmaslik | Zod bilan runtime validatsiya + tip |

## +20 Masala — Daraja 9

**Oson:**
1. `Button` komponentini TypeScript bilan tiplang.
2. `Card` (children bilan) tiplang.
3. `useState`ni `User \| null` bilan ishlating.
4. `onChange` event'ini to'g'ri tiplang.
5. Ixtiyoriy (`?`) va union tip (`"a" \| "b"`) propslar yozing.
6. `useRef<HTMLInputElement>` bilan input fokus qiling.
7. `Props` tipini `type` orqali eksport qiling.
8. Mavjud JS komponentni TS'ga ko'chiring.

**O'rta:**
9. Generic `List<T>` komponenti yozing.
10. `useReducer`ni to'liq tiplang (State + Action union).
11. `useToggle` custom hook'ini tiplang (tuple qaytarsin).
12. API javobini interface bilan tiplab, `useQuery`da ishlating.
13. `Omit`/`Pick` bilan tiplarni qayta ishlating.
14. `ComponentProps<"input">` bilan native propslarni meros qiling.
15. Discriminated union bilan turli holatlarni tiplang (loading/success/error).

**Qiyin:**
16. To'liq todo ilovasini TypeScript bilan qayta yozing.
17. Generic `useFetch<T>` hook'i yozing.
18. Zod schema + TypeScript bilan type-safe forma.
19. Polymorphic komponent (`as` prop bilan har xil HTML element).
20. EduCore bir modulini (masalan, student ro'yxati) to'liq type-safe qiling.

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**16 — Typed todo** (asosiy tip + state):
```tsx
type Todo = { id: number; text: string; done: boolean };

function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const add = (text: string) =>
    setTodos((p) => [...p, { id: Date.now(), text, done: false }]);
  // ...
}
```

**17 — Generic `useFetch<T>`** (ignore bilan race'dan himoya):
```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    let ignore = false;
    fetch(url)
      .then((r) => r.json())
      .then((d: T) => { if (!ignore) setData(d); })
      .catch((e) => { if (!ignore) setError(e); })
      .finally(() => { if (!ignore) setLoading(false); });
    return () => { ignore = true; };  // race condition'dan himoya
  }, [url]);
  return { data, loading, error };
}
// const { data } = useFetch<Student[]>("/api/students");  // data: Student[] | null
```

**19 — Polymorphic komponent** (`as` prop):
```tsx
import type { ElementType, ComponentPropsWithoutRef } from "react";

type TextProps<T extends ElementType> = {
  as?: T;
  children: React.ReactNode;
} & ComponentPropsWithoutRef<T>;

function Text<T extends ElementType = "span">({ as, children, ...rest }: TextProps<T>) {
  const Component = as || "span";
  return <Component {...rest}>{children}</Component>;
}
// <Text as="h1">Sarlavha</Text>   yoki   <Text as="a" href="/">Havola</Text>  — props tipi `as`ga moslashadi
```

> (18 — Zod + TS: `z.infer<typeof schema>` bilan tipni schema'dan avtomatik olasan; 20 — EduCore moduli: `Student` tipi + `useFetch<Student[]>` + typed props birlashtirib.)
</details>
