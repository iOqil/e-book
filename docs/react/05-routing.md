# Daraja 5 — Routing (React Router v7)

[⬅️ Oldingi: Daraja 4 — Formalar va ma'lumotlar](./04-formalar.md) · [🏠 README](./README.md) · [Keyingi: Daraja 6 — State management ➡️](./06-state-management.md)

---

SPA'da sahifalar orasida URL bilan harakatlanish uchun **React Router** kerak (React'da o'z ichida yo'q).

```bash
npm install react-router-dom
```

## 5.1. Asosiy sozlash

```jsx
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Bosh sahifa</Link>
        <Link to="/about">Biz haqimizda</Link>
        <Link to="/users">Foydalanuvchilar</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<Users />} />
        <Route path="*" element={<NotFound />} />  {/* 404 */}
      </Routes>
    </BrowserRouter>
  );
}
```

> **`<Link>` ishlating, `<a href>` emas** — `<a>` butun sahifani qayta yuklaydi, `<Link>` esa SPA tezligini saqlaydi.

Quyidagi diagramma routing mexanizmini ko'rsatadi: URL o'zgarganda Router mos `path`ni topib, tegishli komponentni chizadi (`:id` dinamik segment bilan):

![Routing: URL mos komponentga moslab chiziladi](rasmlar/reb-routing-url-component.svg)

## 5.2. Dinamik route va parametrlar

```jsx
// Route
<Route path="/users/:id" element={<UserDetail />} />

// Komponent ichida parametrni o'qish
import { useParams } from "react-router-dom";

function UserDetail() {
  const { id } = useParams();
  return <h1>Foydalanuvchi #{id}</h1>;
}
```

## 5.3. Programmatik navigatsiya

```jsx
import { useNavigate } from "react-router-dom";

function LoginForm() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // ... login mantiq
    navigate("/dashboard");  // boshqa sahifaga o'tkazish
  };
}
```

## 5.4. Nested routes va Layout

```jsx
import { Outlet } from "react-router-dom";

function DashboardLayout() {
  return (
    <div>
      <Sidebar />
      <main>
        <Outlet />  {/* bu yerda child route chiqadi */}
      </main>
    </div>
  );
}

// Routes
<Route path="/dashboard" element={<DashboardLayout />}>
  <Route index element={<Overview />} />
  <Route path="settings" element={<Settings />} />
  <Route path="profile" element={<Profile />} />
</Route>
```

Quyidagi diagramma nested route ishlashini ko'rsatadi: layout (Sidebar) doimiy qoladi, faqat `<Outlet />` ichidagi qism URL'ga qarab almashadi:

![Nested route + layout: Outlet ichida child route chiziladi](rasmlar/reb-nested-routes-layout.svg)

## 5.5. Himoyalangan route (Protected route)

```jsx
import { Navigate } from "react-router-dom";

function ProtectedRoute({ children }) {
  const { user } = useAuth();  // o'z auth hook'ingiz
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

// Ishlatish:
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

> **EduCore uchun muhim:** subdomain-based multi-tenant routing'da har tenant uchun alohida route logikasini shu yerda quryapsiz. Role-based middleware'ni `ProtectedRoute` ichida `user.role` bilan kengaytirasiz.

## 5.6. Zamonaviy eslatma

> **2026:** React Router **v7** "framework mode"da Remix bilan birlashdi — data loading (`loader`), action'lar, SSR'ni qo'llab-quvvatlaydi. Type-safety juda muhim bo'lsa **TanStack Router**'ni ham ko'rib chiqing (compile-time type-safe routing). Boshlovchi uchun esa yuqoridagi "declarative mode" yetarli.

## 5.7. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| `<a href>` ishlatish | `<Link to>` |
| `BrowserRouter`siz `Routes` ishlatish | Ildizda o'rang |
| 404 (`path="*"`) ni unutish | Har doim qo'shing |
| Nested'da `<Outlet />`ni unutish | Layout'ga qo'ying |
| Auth tekshiruvini `useEffect`+`navigate` bilan | `<Navigate>` deklarativ |

## +20 Masala — Daraja 5

**Oson:**
1. 3 sahifali sayt: Home, About, Contact + navigatsiya.
2. 404 sahifasini qo'shing.
3. `<Link>` bilan menyu yarating, aktiv link'ni ajrating (`NavLink`).
4. Tugma bosilganda `useNavigate` bilan boshqa sahifaga o'ting.
5. "Orqaga" tugmasi yarating (`navigate(-1)`).
6. Logo'ga bosilganda bosh sahifaga o'tsin.
7. Footer'ni barcha sahifalarda ko'rsating (umumiy layout).
8. Tashqi havola (`<a>`) va ichki havola (`<Link>`) farqini ko'rsatuvchi sahifa.

**O'rta:**
9. Bloglar ro'yxati + `/blog/:id` dinamik detail sahifa.
10. Query parametrlar bilan ishlash: `/search?q=react` (`useSearchParams`).
11. Nested routes: `/dashboard` ichida `overview`, `settings`, `profile`.
12. Login → dashboard redirect (`useNavigate`).
13. `ProtectedRoute` yarating, login bo'lmasa `/login`ga yuborsin.
14. Mahsulotlar katalogi: ro'yxat → detail → orqaga.
15. Breadcrumb (non zarralari) navigatsiyasini yarating.

**Qiyin:**
16. To'liq mini-blog: ro'yxat, detail, qo'shish, tahrirlash, o'chirish + routing.
17. Role-based routing: admin va user uchun turli sahifalar.
18. `loader` (React Router v7 framework mode) bilan ma'lumot oldindan yuklang.
19. Lazy loading: har bir route'ni `lazy` + `Suspense` bilan yuklang.
20. Multi-tenant routing prototipi: `/:tenant/dashboard` strukturasi (EduCore uslubida).

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**17 — Role-based routing:**
```jsx
function RoleRoute({ allow, role, children }) {
  return allow.includes(role)
    ? children
    : <Navigate to="/forbidden" replace />;
}

<Routes>
  <Route path="/dashboard" element={
    <RoleRoute allow={["user", "admin"]} role={role}><Dashboard /></RoleRoute>
  } />
  <Route path="/admin" element={
    <RoleRoute allow={["admin"]} role={role}><AdminPanel /></RoleRoute>
  } />
</Routes>
```

**18 — `loader` (React Router v7 framework mode)** — route ma'lumotni *render'dan oldin* yuklaydi:
```jsx
// routes.ts
export const usersLoader = async () => {
  const res = await fetch("/api/users");
  return res.json();
};
// komponentda
import { useLoaderData } from "react-router";
function Users() {
  const users = useLoaderData(); // yuklangan, kutish shart emas
  return <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```
`useEffect` + `useState`siz — ma'lumot route bilan birga keladi (waterfall yo'q).

**19 — Lazy loading** (`lazy` + `Suspense`):
```jsx
import { lazy, Suspense } from "react";
const Dashboard = lazy(() => import("./Dashboard.jsx"));

<Suspense fallback={<p>Yuklanmoqda...</p>}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
  </Routes>
</Suspense>
```
Har route alohida bundle bo'lib, faqat kerak bo'lganda yuklanadi (kichikroq boshlang'ich yuk).

**20 — Multi-tenant routing** (`/:tenant/...`, EduCore uslubida):
```jsx
function TenantLayout() {
  const { tenant } = useParams();
  return (
    <div>
      <header>Tenant: {tenant}</header>
      <Outlet />   {/* ichki route shu yerga chiziladi */}
    </div>
  );
}

<Routes>
  <Route path="/:tenant" element={<TenantLayout />}>
    <Route path="dashboard" element={<Dashboard />} />
    <Route path="students" element={<Students />} />
  </Route>
</Routes>
```
`useParams().tenant` orqali joriy markaz aniqlanadi — keyin uni context yoki store'ga (Zustand) qo'yib, butun ilova shu tenant bilan ishlaydi.

> (16 — mini-blog: yuqoridagi nested route + `useParams` (detail) + forma (qo'shish/tahrir) kombinatsiyasi.)
</details>
