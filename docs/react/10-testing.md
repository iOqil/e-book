# Daraja 10 — Testing

[⬅️ Oldingi: Daraja 9 — TypeScript bilan React](./09-typescript.md) · [🏠 README](./README.md) · [Keyingi: Daraja 11 — Production va ekotizim ➡️](./11-production.md)

---

Sifatli kod = testlangan kod. **Vitest** (Vite'ga tabiiy) + **React Testing Library** standart.

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

## 10.1. Test falsafasi

> **RTL qoidasi:** "Foydalanuvchi qanday ishlatsa, shunday test qiling." Implementatsiya detallarini emas (state, ichki funksiya), **xulq-atvorni** (ekranda nima ko'rinadi, nima bosiladi) tekshiring.

## 10.2. Birinchi test

```jsx
// Button.jsx
export function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

// Button.test.jsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi } from "vitest";
import { Button } from "./Button";

test("tugma bosilganda funksiya chaqiriladi", async () => {
  const handleClick = vi.fn();   // mock funksiya
  render(<Button onClick={handleClick}>Bosing</Button>);

  await userEvent.click(screen.getByText("Bosing"));

  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

Har bir RTL testi bir xil to'rt bosqichli oqimni bosib o'tadi — komponentni chizish, elementni topish, u bilan ishlash va natijani tekshirish:

![RTL oqimi: render, query, interact, assert](rasmlar/red-rtl-oqimi.svg)

## 10.3. Element topish (queries)

```jsx
screen.getByRole("button", { name: "Yuborish" });  // afzal — a11y
screen.getByLabelText("Email");
screen.getByPlaceholderText("Yozing...");
screen.getByText("Salom");
screen.getByTestId("user-card");  // oxirgi chora

// findBy — async (kutadi)
await screen.findByText("Yuklandi");

// queryBy — yo'qligini tekshirish uchun (null qaytaradi, xato bermaydi)
expect(screen.queryByText("Xato")).not.toBeInTheDocument();
```

## 10.4. State va interaktivlikni test qilish

```jsx
test("counter oshadi", async () => {
  render(<Counter />);

  expect(screen.getByText("0")).toBeInTheDocument();
  await userEvent.click(screen.getByRole("button", { name: "+1" }));
  expect(screen.getByText("1")).toBeInTheDocument();
});
```

## 10.5. Async va API mock

```jsx
test("foydalanuvchilar yuklanadi", async () => {
  // fetch'ni mock qilamiz
  global.fetch = vi.fn(() =>
    Promise.resolve({ json: () => Promise.resolve([{ id: 1, name: "Ali" }]) })
  );

  render(<Users />);

  expect(screen.getByText("Yuklanmoqda...")).toBeInTheDocument();
  expect(await screen.findByText("Ali")).toBeInTheDocument();
});
```

> Real loyihada `fetch`ni qo'lda mock qilish o'rniga **MSW (Mock Service Worker)** ishlatiladi — tarmoq darajasida mock, eng ishonchli yondashuv.

## 10.6. Custom hook'ni test qilish

```jsx
import { renderHook, act } from "@testing-library/react";

test("useToggle ishlaydi", () => {
  const { result } = renderHook(() => useToggle());

  expect(result.current[0]).toBe(false);
  act(() => result.current[1]());  // toggle
  expect(result.current[0]).toBe(true);
});
```

## 10.7. Testlar turlari

- **Unit** — bitta funksiya/komponent (eng ko'p).
- **Integration** — bir nechta komponent birga (eng qimmatli).
- **E2E** — butun ilova brauzerda (**Playwright** / Cypress).

Bu uch turning nisbati piramida shaklida bo'ladi: tagida ko'p tez unit test, yuqorida esa kam, sekin E2E test:

![Test piramidasi: unit, integration va e2e nisbati](rasmlar/red-test-piramidasi.svg)

## 10.8. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| Implementatsiya detalini test qilish (state) | Xulq-atvorni test qiling |
| `getByTestId`ni asosiy usul qilish | `getByRole`/`getByText` afzal |
| Async'da `getBy` ishlatish | `findBy` (kutadi) |
| `userEvent`'ni `await`siz ishlatish | Har doim `await` |
| `fetch`ni qo'lda mock qilish | MSW |

## +20 Masala — Daraja 10

**Oson:**
1. `Button` bosilganda mock funksiya chaqirilishini test qiling.
2. Komponent matnni to'g'ri ko'rsatishini tekshiring.
3. `getByRole` bilan tugma toping.
4. Props o'tkazib, to'g'ri render bo'lishini test qiling.
5. `disabled` tugma bosilmasligini tekshiring.
6. Conditional rendering'ni test qiling (`queryBy` bilan yo'qligi).
7. Input'ga yozilganini `userEvent.type` bilan test qiling.
8. Snapshot test yozing.

**O'rta:**
9. Counter komponentini to'liq test qiling (+/-/reset).
10. Forma submit'ini test qiling (mock onSubmit).
11. Validatsiya xatosi ko'rinishini test qiling.
12. Todo qo'shish/o'chirishni test qiling.
13. `findBy` bilan async yuklanishni test qiling.
14. `useToggle` custom hook'ini `renderHook` bilan test qiling.
15. Mock fetch bilan API komponentini test qiling.

**Qiyin:**
16. MSW bilan API'ni mock qilib, integration test yozing.
17. TanStack Query komponentini test qiling (QueryClient wrapper bilan).
18. `useReducer`'li murakkab hook'ni to'liq test qiling.
19. Modal/portal komponentini test qiling.
20. Playwright bilan login → dashboard E2E test stsenariysi yozing.

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**17 — TanStack Query komponentini test qilish** (QueryClient wrapper):
```tsx
function renderWithClient(ui: React.ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>);
}

it("o'quvchilarni ko'rsatadi", async () => {
  renderWithClient(<StudentList />);
  await waitFor(() => expect(screen.getByText("Ali Valiyev")).toBeInTheDocument());
});
```
Test uchun `retry: false` — xato bo'lsa darrov ko'rsin, qayta urinmasin.

**16 — MSW bilan API mock** (integration test):
```tsx
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

const server = setupServer(
  http.get("/api/students", () =>
    HttpResponse.json([{ id: 1, name: "Ali Valiyev" }])
  )
);
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```
MSW tarmoq so'rovini ushlab, soxta javob beradi — real backend kerak emas, lekin komponent "haqiqiy" fetch qilayotgandek ishlaydi.

**20 — Playwright E2E** (login → dashboard):
```ts
import { test, expect } from "@playwright/test";

test("login -> dashboard", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("ali@mail.uz");
  await page.getByLabel("Parol").fill("12345678");
  await page.getByRole("button", { name: "Kirish" }).click();
  await expect(page).toHaveURL("/dashboard");
});
```
E2E test — real brauzerda, foydalanuvchi kabi: bosadi, yozadi, natijani tekshiradi.

> **Tamoyil:** `getByRole`/`getByLabel` bilan qidir (foydalanuvchi ko'rganidek), `getByTestId` ni kamroq ishlat. Test *foydalanuvchi xulqini* tekshirsin, *implementatsiyani* emas.
> (18 — `useReducer` hook'i: `renderHook` + `act` bilan; 19 — Modal/portal: `getByRole("dialog")` bilan tekshiriladi.)
</details>
