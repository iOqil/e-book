# Daraja 6 — State management

[⬅️ Oldingi: Daraja 5 — Routing (React Router v7)](./05-routing.md) · [🏠 README](./README.md) · [Keyingi: Daraja 7 — Performance optimizatsiya ➡️](./07-performance.md)

---

Ilova kattalashganda state'ni boshqarish murakkablashadi. **2026-yilning eng muhim qoidasi:** server state va client state'ni *ajrating*.

| Tur | Nima | Yechim |
|-----|------|--------|
| **Server state** | API'dan kelgan ma'lumot (cache, sync kerak) | **TanStack Query** |
| **Client state** | UI holati (modal, theme, forma) | **Zustand** / `useState` / Context |
| **Katta enterprise** | Murakkab global state | **Redux Toolkit** |

> ⚠️ **Eng keng tarqalgan xato:** API javobini Redux/Zustand'ga saqlash. Buni qilmang — server state uchun TanStack Query bor. Bu ikkisini aralashtirmaslik kod sifatini keskin oshiradi.

Quyidagi diagramma bu ikki turning farqini va TanStack Query keshi qanday yashashini (fetch → cache → stale → refetch) ko'rsatadi:

![Server state va client state farqi; TanStack Query kesh hayoti](rasmlar/rec-server-vs-client-state.svg)

## 6.1. TanStack Query (server state uchun)

API ma'lumotini boshqarishning eng yaxshi yo'li. Caching, background refetch, loading/error — hammasi avtomatik.

```bash
npm install @tanstack/react-query
```

```jsx
import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Users />
    </QueryClientProvider>
  );
}

function Users() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["users"],
    queryFn: () =>
      fetch("https://jsonplaceholder.typicode.com/users").then((r) => r.json()),
  });

  if (isLoading) return <p>Yuklanmoqda...</p>;
  if (error) return <p>Xato!</p>;

  return <ul>{data.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

> **Solishtiring:** Daraja 4'dagi `useEffect` versiyasi 25 qator edi. Bu yerda 5 qator — va ustiga caching, refetch, deduplication bepul keladi. Aynan shu — to'g'ri yo'l.

Mutation (ma'lumot o'zgartirish):

```jsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function AddUser() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newUser) =>
      fetch("/api/users", { method: "POST", body: JSON.stringify(newUser) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });  // qayta yuklash
    },
  });

  return <button onClick={() => mutation.mutate({ name: "Ali" })}>Qo'shish</button>;
}
```

## 6.2. Zustand (client state uchun)

Eng yengil va sodda global state. Redux'siz boilerplate.

```bash
npm install zustand
```

```jsx
import { create } from "zustand";

// Store yaratish
const useCartStore = create((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) =>
    set((state) => ({ items: state.items.filter((i) => i.id !== id) })),
  clear: () => set({ items: [] }),
}));

// Istalgan komponentda — Provider kerak emas!
function Cart() {
  const { items, removeItem } = useCartStore();
  return (
    <ul>
      {items.map((i) => (
        <li key={i.id}>
          {i.name} <button onClick={() => removeItem(i.id)}>x</button>
        </li>
      ))}
    </ul>
  );
}

function AddButton() {
  const addItem = useCartStore((s) => s.addItem);  // faqat kerakli qismni oling
  return <button onClick={() => addItem({ id: 1, name: "Kitob" })}>Qo'shish</button>;
}
```

> **Zustand'ning afzalligi:** `<Provider>` o'rash shart emas, selector (`(s) => s.addItem`) bilan faqat kerakli qismga obuna bo'lasiz → kamroq re-render. Auth, theme, savatcha — shular uchun ideal.

## 6.3. Redux Toolkit (katta loyihalar uchun)

Murakkab, ko'p jamoali enterprise loyihalarda. Strukturali, DevTools kuchli.

```jsx
import { createSlice, configureStore } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },  // Immer ichida — mutatsiya OK
    decrement: (state) => { state.value -= 1; },
  },
});

export const { increment, decrement } = counterSlice.actions;
export const store = configureStore({ reducer: { counter: counterSlice.reducer } });
```

> **Qachon Redux?** Faqat haqiqatan murakkab, ko'p o'zaro bog'liq global state bo'lsa. Aks holda Zustand + TanStack Query yetadi. **Premature'ga Redux qo'shmang.**

## 6.4. Qanday tanlash kerak? (qaror jadvali)

- **Faqat bitta komponent ichida** → `useState`
- **Bir nechta komponent (kichik daraxt)** → lifting state up yoki Context
- **Tez-tez o'zgaradigan global UI state** → Zustand
- **API ma'lumoti** → TanStack Query (har doim!)
- **Juda katta, murakkab enterprise** → Redux Toolkit + TanStack Query

## 6.5. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| API javobini Redux/Zustand'ga saqlash | TanStack Query |
| Hamma narsani global state'ga tiqish | Avval local, keyin ko'taring |
| Context'ni tez-tez o'zgaruvchi state uchun ishlatish | Zustand (selectorlar bilan) |
| Boshlanishidayoq Redux qo'shish | Avval sodda yechim |
| `queryKey`ni noto'g'ri tuzish | Aniq, izchil kalitlar |

## +20 Masala — Daraja 6

**Oson (TanStack Query):**
1. `useQuery` bilan foydalanuvchilarni yuklang.
2. Loading va error holatlarini chiroyli ko'rsating.
3. "Refetch" tugmasi qo'shing.
4. `queryKey`ga parametr bering (`["user", id]`) va bitta foydalanuvchini oling.
5. `staleTime` sozlang va caching ishini kuzating.
6. Ikki xil API'dan ma'lumotni parallel yuklang.
7. `enabled` opsiyasi bilan shartli so'rov (faqat `id` bor bo'lsa).
8. DevTools'ni o'rnating va cache'ni kuzating.

**O'rta (Zustand + mutation):**
9. Zustand bilan savatcha: qo'shish/o'chirish/tozalash.
10. Zustand bilan dark mode toggle (butun ilovaga).
11. Auth store: `login`, `logout`, `user` (Zustand).
12. `useMutation` bilan yangi post qo'shish + `invalidateQueries`.
13. Optimistik mutation (TanStack Query): like'ni darhol ko'rsatish.
14. Selector bilan Zustand'dan faqat kerakli qismni olib re-render'ni kamaytiring.
15. Pagination: `page` state + `useQuery` (`keepPreviousData`).

**Qiyin:**
16. To'liq CRUD ilovasi: TanStack Query (read) + mutations (create/update/delete).
17. Infinite scroll: `useInfiniteQuery` bilan.
18. Server state (TanStack Query) + client state (Zustand)ni bitta ilovada to'g'ri ajrating.
19. Redux Toolkit bilan counter + todo slice yarating.
20. EduCore prototipi: tenant ma'lumotini TanStack Query bilan, UI holatini Zustand bilan boshqaring.

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**16 — TanStack Query CRUD** (read + mutation + invalidate):
```jsx
function useStudents() {
  return useQuery({
    queryKey: ["students"],
    queryFn: () => fetch("/api/students").then((r) => r.json()),
  });
}
function useAddStudent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (s) => fetch("/api/students", { method: "POST", body: JSON.stringify(s) }).then((r) => r.json()),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["students"] }), // ro'yxat avtomatik yangilanadi
  });
}
```

**18 — Server state vs client state ajratish:**
```jsx
// SERVER state → TanStack Query (backend'dan keladi, kesh, qayta yuklash)
const { data: students } = useStudents();

// CLIENT state → Zustand (faqat UI: modal ochiq/yopiq, sidebar)
const useUiStore = create((set) => ({
  sidebarOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));
```
**Qoida:** backend'dan kelgan narsa — Query; faqat brauzerdagi UI holati — Zustand. Ularni aralashtirma (server datani Zustand'da dublikat qilma).

**19 — Redux Toolkit** (counter + todo slice):
```jsx
const counterSlice = createSlice({
  name: "counter",
  initialState: { value: 0 },
  reducers: {
    increment: (s) => { s.value += 1; },   // Immer tufayli "mutatsiya" xavfsiz
    decrement: (s) => { s.value -= 1; },
  },
});
const todoSlice = createSlice({
  name: "todos",
  initialState: { items: [] },
  reducers: {
    add: (s, a) => { s.items.push({ id: Date.now(), text: a.payload }); },
    remove: (s, a) => { s.items = s.items.filter((t) => t.id !== a.payload); },
  },
});
const store = configureStore({
  reducer: { counter: counterSlice.reducer, todos: todoSlice.reducer },
});
```

> (20 — EduCore prototipi: `useQuery(["tenant", id])` bilan tenant ma'lumoti + Zustand'da UI holati — 16 va 18 ni birlashtirish.)
</details>
