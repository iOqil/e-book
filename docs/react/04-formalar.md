# Daraja 4 — Formalar va ma'lumotlar

[⬅️ Oldingi: Daraja 3 — Hooks olami](./03-hooks.md) · [🏠 README](./README.md) · [Keyingi: Daraja 5 — Routing (React Router v7) ➡️](./05-routing.md)

---

## 4.1. Controlled components

React'da forma maydonlarini state boshqaradi — bu "controlled" yondashuv.

Quyidagi diagramma state bilan input o'rtasidagi ikki tomonlama bog'lanishni ko'rsatadi: state input'ning `value`sini belgilaydi, `onChange` esa yozilgani state'ni yangilaydi:

![Controlled component: state va input value ikki tomonlama bog'lanish](rasmlar/reb-controlled-component.svg)

```jsx
import { useState } from "react";

function SignupForm() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));  // dinamik kalit
  };

  const handleSubmit = (e) => {
    e.preventDefault();  // sahifa yangilanishini to'xtatish
    console.log(form);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" value={form.name} onChange={handleChange} />
      <input name="email" type="email" value={form.email} onChange={handleChange} />
      <input name="password" type="password" value={form.password} onChange={handleChange} />
      <button type="submit">Ro'yxatdan o'tish</button>
    </form>
  );
}
```

> **`[name]: value`** — bitta `handleChange` bilan barcha maydonlarni boshqaramiz (computed property). Bu pattern'ni yodda tuting.

## 4.2. Validation (tekshiruv)

```jsx
function LoginForm() {
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState({});

  const validate = () => {
    const errs = {};
    if (!email) errs.email = "Email majburiy";
    else if (!/\S+@\S+\.\S+/.test(email)) errs.email = "Email noto'g'ri";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      console.log("Yuborildi!");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      {errors.email && <span style={{ color: "red" }}>{errors.email}</span>}
      <button>Kirish</button>
    </form>
  );
}
```

> **Real loyihada:** validatsiyani qo'lda yozish o'rniga **Zod** + **React Hook Form** ishlatiladi (kamroq kod, type-safe). Backend'dagi Form Request validation'ga o'xshash. Bularni o'rganib chiqing.

## 4.3. API'dan ma'lumot olish

### Eski usul (`useEffect` bilan) — tushunish uchun

```jsx
import { useState, useEffect } from "react";

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let ignore = false;  // race condition'dan himoya

    async function load() {
      try {
        setLoading(true);
        const res = await fetch("https://jsonplaceholder.typicode.com/users");
        if (!res.ok) throw new Error("Tarmoq xatosi");
        const data = await res.json();
        if (!ignore) setUsers(data);
      } catch (err) {
        if (!ignore) setError(err.message);
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    load();
    return () => { ignore = true; };  // cleanup
  }, []);

  if (loading) return <p>Yuklanmoqda...</p>;
  if (error) return <p>Xato: {error}</p>;

  return (
    <ul>
      {users.map((u) => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}
```

> Ko'rib turganingizdek — `loading`, `error`, `data`, race condition... juda ko'p boilerplate. **Aynan shu sababli** zamonaviy loyihalar **TanStack Query** ishlatadi (Daraja 6). Bu usulni biling, lekin real loyihada qo'llamang.

## 4.4. React 19 — Actions (zamonaviy formalar)

React 19 formalar bilan ishlashni sezilarli soddalashtirdi. `<form>`ga `action` funksiyasi, `useActionState` va `useFormStatus` hook'lari.

```jsx
import { useActionState } from "react";

function SubscribeForm() {
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData) => {
      const email = formData.get("email");
      // server'ga yuborish (yoki Server Action)
      await fakeApi(email);
      return { success: true, message: "Obuna bo'ldingiz!" };
    },
    { success: false, message: "" }
  );

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <button disabled={isPending}>
        {isPending ? "Yuborilmoqda..." : "Obuna"}
      </button>
      {state.message && <p>{state.message}</p>}
    </form>
  );
}
```

`useFormStatus` — ichki tugma forma holatini bilishi uchun:

```jsx
import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? "..." : "Yuborish"}</button>;
}
```

`useOptimistic` — optimistik yangilash (server javobini kutmasdan UI'ni darhol yangilash):

```jsx
import { useOptimistic } from "react";

function LikeButton({ likes, onLike }) {
  const [optimisticLikes, addOptimistic] = useOptimistic(likes);

  const handle = async () => {
    addOptimistic(optimisticLikes + 1);  // darhol ko'rsat
    await onLike();                        // keyin server'ga
  };

  return <button onClick={handle}>❤️ {optimisticLikes}</button>;
}
```

## 4.5. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| `e.preventDefault()`ni unutish | Forma'da har doim qo'ying |
| Uncontrolled + controlled aralashtirib yuborish | Bittasini tanlang (odatda controlled) |
| `useEffect`da cleanup/ignore'siz fetch | Race condition'dan himoya qiling |
| Validatsiyani faqat frontend'da qilish | Backend'da ham tekshiring (xavfsizlik) |
| Har bir maydonga alohida state | Bitta obyekt + `[name]` pattern |

## +20 Masala — Daraja 4

**Oson:**
1. Bitta input'li forma: submit'da qiymatni `alert` qiling.
2. Login forma (email + parol), `console.log`'ga obyekt chiqaring.
3. Bitta `handleChange` bilan 3 maydonli formani boshqaring.
4. Checkbox + radio + select bo'lgan forma yarating (controlled).
5. Textarea: belgilar sonini va qolgan limitni ko'rsating.
6. Forma'da "Tozalash" tugmasi: barcha maydonlarni bo'shatsin.
7. Email maydoni bo'sh bo'lsa qizil xato chiqarsin.
8. Parol va "parolni tasdiqlash" mosligini tekshiring.

**O'rta:**
9. To'liq ro'yxatdan o'tish formasi + validatsiya (ism, email, parol, yosh).
10. `jsonplaceholder` dan postlarni `useEffect` bilan yuklang (loading/error bilan).
11. Qidiruv: inputga yozilganda API'dan natija oling (debounce bilan).
12. Forma yuborilgach, ma'lumotni ro'yxatga qo'shing (POST simulyatsiyasi).
13. Multi-step ro'yxatdan o'tish (3 qadam, har biri validatsiyalansin).
14. React 19 `useActionState` bilan obuna formasi yarating.
15. Fayl yuklash inputi: tanlangan fayl nomini va o'lchamini ko'rsating.

**Qiyin:**
16. React Hook Form + Zod bilan type-safe forma yozing.
17. Dinamik forma: "Maydon qo'shish" tugmasi bilan input'lar massivi.
18. CRUD: foydalanuvchilarni qo'shish/tahrirlash/o'chirish (API bilan).
19. `useOptimistic` bilan like tugmasini optimistik yangilang.
20. Avtosaqlash forma: foydalanuvchi yozganda debounce bilan `localStorage`ga saqlasin.

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**16 — React Hook Form + Zod** (type-safe):
```jsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({ email: z.email(), parol: z.string().min(8) });

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({ resolver: zodResolver(schema) });
  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
      <input type="password" {...register("parol")} />
      {errors.parol && <span>{errors.parol.message}</span>}
      <button>Kirish</button>
    </form>
  );
}
```
`register` har bir input'ni ulaydi, `zodResolver` validatsiyani Zod schema'ga topshiradi.

**17 — Dinamik forma** (`useFieldArray`):
```jsx
import { useForm, useFieldArray } from "react-hook-form";

function DynamicForm() {
  const { register, control, handleSubmit } = useForm({ defaultValues: { items: [{ nom: "" }] } });
  const { fields, append, remove } = useFieldArray({ control, name: "items" });
  return (
    <form onSubmit={handleSubmit((d) => console.log(d))}>
      {fields.map((f, i) => (
        <div key={f.id}>
          <input {...register(`items.${i}.nom`)} />
          <button type="button" onClick={() => remove(i)}>O'chir</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ nom: "" })}>Maydon qo'shish</button>
      <button>Yuborish</button>
    </form>
  );
}
```

**19 — `useOptimistic` like:**
```jsx
import { useOptimistic } from "react";

function LikeButton({ likes, onLike }) {
  const [optimistic, addOptimistic] = useOptimistic(likes, (state, amount) => state + amount);
  async function handle() {
    addOptimistic(1);   // UI darhol +1
    await onLike();     // server javobini kutadi; xato bo'lsa avtomatik qaytadi
  }
  return <button onClick={handle}>❤️ {optimistic}</button>;
}
```

**20 — Avtosaqlash** (debounce + `localStorage`, custom hook):
```jsx
function useAutosave(value, key, delay = 500) {
  useEffect(() => {
    const t = setTimeout(() => localStorage.setItem(key, JSON.stringify(value)), delay);
    return () => clearTimeout(t);  // har o'zgarishda eski taymerni bekor qiladi
  }, [value, key, delay]);
}
// Forma state'i o'zgarganda, foydalanuvchi to'xtagach 500ms keyin saqlanadi.
```

> (18 — CRUD: `useState`/TanStack Query'da ro'yxat + `fetch` bilan POST/PUT/DELETE; 6-daraja TanStack Query bilan toza ko'rinishini beradi.)
</details>
