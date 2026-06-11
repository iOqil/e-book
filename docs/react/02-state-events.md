# Daraja 2 — Interaktivlik: State va Events

[⬅️ Oldingi: Daraja 1 — React asoslari](./01-asoslar.md) · [🏠 README](./README.md) · [Keyingi: Daraja 3 — Hooks olami ➡️](./03-hooks.md)

---

Hozirgacha komponentlarimiz "o'lik" edi. Endi ularni **jonlantiramiz**.

## 2.1. `useState` — komponent xotirasi

State — komponent "eslab qoladigan" va o'zgarganda UI'ni qayta chizdiradigan ma'lumot.

`setState` chaqirilganda React komponentni qayta render qiladi va yangi UI hosil bo'ladi — bu siklni quyida ko'rasiz:

![useState sikli: setState dan qayta render orqali yangi UI](rasmlar/rea-usestate-rerender.svg)

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  //     ↑       ↑              ↑
  //  qiymat  yangilovchi    boshlang'ich qiymat

  return (
    <div>
      <p>Hisob: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(count - 1)}>-1</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

### Muhim qoidalar

1. **State'ni to'g'ridan-to'g'ri o'zgartirmang:**
   ```jsx
   count = count + 1;        // ❌ ISHLAMAYDI — UI yangilanmaydi
   setCount(count + 1);      // ✅ to'g'ri
   ```

2. **Avvalgi qiymatga tayanganda funksiya bering:**
   ```jsx
   setCount(prev => prev + 1);   // ✅ ishonchli (ayniqsa ketma-ket yangilashda)
   ```

3. **Obyekt/massiv state'ni yangi nusxa bilan yangilang:**
   ```jsx
   const [user, setUser] = useState({ name: "Ali", age: 25 });

   setUser({ ...user, age: 26 });   // ✅ spread bilan yangi obyekt
   user.age = 26;                    // ❌ React buni "sezmaydi"
   ```

## 2.2. Event handling

```jsx
function Form() {
  const [text, setText] = useState("");

  const handleClick = () => {
    alert("Bosildi: " + text);
  };

  return (
    <div>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Yozing..."
      />
      <button onClick={handleClick}>Yuborish</button>
    </div>
  );
}
```

Asosiy eventlar: `onClick`, `onChange`, `onSubmit`, `onMouseEnter`, `onKeyDown`, `onFocus`, `onBlur`.

> **Diqqat:** `onClick={handleClick}` — funksiyani *uzatamiz*. `onClick={handleClick()}` — funksiyani *chaqiramiz* (xato! u darhol ishlab ketadi).

## 2.3. Conditional rendering (shartli ko'rsatish)

```jsx
function Status({ isLoading, error, data }) {
  if (isLoading) return <p>Yuklanmoqda...</p>;
  if (error) return <p>Xatolik: {error}</p>;

  return (
    <div>
      {data.length > 0 ? (
        <ul>{/* ... */}</ul>
      ) : (
        <p>Ma'lumot yo'q</p>
      )}
    </div>
  );
}
```

Uchta usul: `if` (early return), ternary (`? :`), `&&`.

## 2.4. Lists va keys

Ro'yxat chizish — `map` bilan. **Har bir elementga `key` shart.**

```jsx
function TodoList() {
  const [todos, setTodos] = useState([
    { id: 1, text: "Kod yozish" },
    { id: 2, text: "Dam olish" },
  ]);

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

> **`key` nega kerak?** React qaysi element o'zgarganini, qaysisi qo'shilgan/o'chganini aniqlash uchun. **`key` sifatida `index` ishlatmang** (agar ro'yxat o'zgarsa bug chiqadi) — barqaror `id` ishlating.

Quyidagi diagramma reconciliation'da barqaror `id` bilan `index` farqini ko'rsatadi:

![Lists va keys: key reconciliation jarayonida elementni aniqlaydi](rasmlar/rea-lists-keys.svg)

### To'liq Todo misoli

```jsx
import { useState } from "react";

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState("");

  const addTodo = () => {
    if (input.trim() === "") return;
    setTodos([...todos, { id: Date.now(), text: input }]);
    setInput("");
  };

  const removeTodo = (id) => {
    setTodos(todos.filter((t) => t.id !== id));
  };

  return (
    <div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={addTodo}>Qo'shish</button>

      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            {todo.text}
            <button onClick={() => removeTodo(todo.id)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## 2.5. State'ni "ko'tarish" (Lifting state up)

Ikki komponent bitta ma'lumotni baham ko'rishi kerak bo'lsa, state'ni ularning umumiy ota-onasiga ko'taramiz.

Quyidagi diagramma state otaga ko'tarilganda ikki bola uni qanday ulashishini ko'rsatadi:

![Lifting state up: umumiy holatni ota komponentga ko'tarish](rasmlar/rea-lifting-state.svg)

```jsx
function Parent() {
  const [value, setValue] = useState("");

  return (
    <>
      <Input value={value} onChange={setValue} />
      <Display value={value} />
    </>
  );
}

function Input({ value, onChange }) {
  return <input value={value} onChange={(e) => onChange(e.target.value)} />;
}

function Display({ value }) {
  return <p>Siz yozdingiz: {value}</p>;
}
```

## 2.6. Keng tarqalgan xatolar

| Xato | To'g'risi |
|------|-----------|
| State'ni mutatsiya qilish (`arr.push()`) | Yangi massiv (`[...arr, item]`) |
| `key` sifatida `index` | Barqaror `id` |
| `onClick={fn()}` | `onClick={fn}` yoki `onClick={() => fn()}` |
| Bir nechta `setState`ni eski qiymatga tayanib chaqirish | `setX(prev => ...)` funksiya formasi |
| Renderda to'g'ridan-to'g'ri `setState` chaqirish | Faqat event yoki effect ichida |

## +20 Masala — Daraja 2

**Oson:**
1. Counter yarating: +1, -1, Reset tugmalari bilan.
2. Tugma bosilganda matn "Yoqildi"/"O'chirildi" ga almashsin (toggle).
3. Input'ga yozilganini real vaqtda pastda ko'rsating (mirror).
4. Tugma bosilgan sonini sanang.
5. Checkbox holatini state'da saqlang va matnda ko'rsating.
6. 3 ta tugma: bosilganiga qarab fon rangini o'zgartirsin.
7. Inputdagi matn uzunligini real vaqtda chiqaring.
8. "Like" tugmasi: bosilsa ❤️, yana bosilsa 🤍 bo'lsin.

**O'rta:**
9. To'liq Todo ilovasi: qo'shish, o'chirish, ro'yxat.
10. Todo'ga "bajarildi" holatini qo'shing (chizilgan matn — `line-through`).
11. Hisoblagich: faqat 0 dan katta bo'lsa "-" tugmasi ishlasin (`disabled`).
12. Forma: ism + email kiritib, "Yuborish"da pastda kartada ko'rsating.
13. Rang tanlovchi: 5 ta tugma, tanlangani fon bo'lib o'zgarsin.
14. Filtrlash: ro'yxatdan inputga yozilgan matnga mos elementlarni ko'rsating.
15. Savatcha: mahsulot qo'shish, sonini oshirish/kamaytirish, umumiy narx.

**Qiyin:**
16. Quiz ilovasi: 5 ta savol, javoblar, oxirida ball ko'rsatish.
17. Soatli yulduzcha baholash (interaktiv `Rating`): hover va click.
18. Akkordeon: bir nechta panel, faqat bittasi ochiq (lifting state up).
19. Stepper forma: 3 qadam, "Oldinga/Orqaga", har qadam state'ni saqlasin.
20. Tic-tac-toe (krestiki-noliki) o'yini: 2 o'yinchi, g'olibni aniqlash.

<details markdown="1">
<summary>✅ Qiyin masalalar yechimi (16–20)</summary>

**17 — Interaktiv Rating** (hover + click; `hover || value` hiylasi):
```jsx
function Rating() {
  const [value, setValue] = useState(0);
  const [hover, setHover] = useState(0);
  return (
    <div>
      {[1, 2, 3, 4, 5].map((n) => (
        <span
          key={n}
          onClick={() => setValue(n)}
          onMouseEnter={() => setHover(n)}
          onMouseLeave={() => setHover(0)}
        >
          {n <= (hover || value) ? "⭐" : "☆"}
        </span>
      ))}
    </div>
  );
}
```

**18 — Accordion** (faqat bittasi ochiq — `openIdx` bitta state):
```jsx
function Accordion({ items }) {
  const [openIdx, setOpenIdx] = useState(null);
  return (
    <div>
      {items.map((it, i) => (
        <div key={i}>
          <h3 onClick={() => setOpenIdx(openIdx === i ? null : i)}>{it.title}</h3>
          {openIdx === i && <p>{it.content}</p>}
        </div>
      ))}
    </div>
  );
}
```
"Qaysi panel ochiq" — bitta `openIdx`. Yangisini ochsa, eskisi avtomatik yopiladi.

**19 — Stepper forma** (`[name]` pattern bilan bitta state obyekti):
```jsx
function Stepper() {
  const [step, setStep] = useState(1);
  const [data, setData] = useState({ ism: "", email: "", manzil: "" });
  const set = (k) => (e) => setData({ ...data, [k]: e.target.value });
  return (
    <div>
      {step === 1 && <input value={data.ism} onChange={set("ism")} placeholder="Ism" />}
      {step === 2 && <input value={data.email} onChange={set("email")} placeholder="Email" />}
      {step === 3 && <input value={data.manzil} onChange={set("manzil")} placeholder="Manzil" />}
      <div>
        {step > 1 && <button onClick={() => setStep(step - 1)}>Orqaga</button>}
        {step < 3 && <button onClick={() => setStep(step + 1)}>Oldinga</button>}
      </div>
    </div>
  );
}
```

**20 — Tic-tac-toe:**
```jsx
function hisoblaGolib(k) {
  const yutuq = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  for (const [a, b, c] of yutuq)
    if (k[a] && k[a] === k[b] && k[a] === k[c]) return k[a];
  return null;
}
function TicTacToe() {
  const [kataklar, setKataklar] = useState(Array(9).fill(null));
  const [xNavbat, setXNavbat] = useState(true);
  const golib = hisoblaGolib(kataklar);

  function bos(i) {
    if (kataklar[i] || golib) return;          // band yoki o'yin tugagan
    const yangi = kataklar.slice();            // NUSXA (state'ni to'g'ridan o'zgartirma!)
    yangi[i] = xNavbat ? "X" : "O";
    setKataklar(yangi);
    setXNavbat(!xNavbat);
  }
  return (
    <div>
      <p>{golib ? `G'olib: ${golib}` : `Navbat: ${xNavbat ? "X" : "O"}`}</p>
      <div className="board">
        {kataklar.map((k, i) => <button key={i} onClick={() => bos(i)}>{k}</button>)}
      </div>
    </div>
  );
}
```
Asosiy saboq: state massivni **nusxalab** (`slice`) o'zgartiramiz, g'olibni har renderda hosilaviy (derived) qiymat sifatida hisoblaymiz — alohida state'da saqlamaymiz.

> (16 — Quiz va undan oldingilar shu naqshlarning kombinatsiyasi: savollar massivi + `idx`/`ball` state + tugma `onClick`.)
</details>
