# JavaScript — 0 dan Expertgacha (O'zbek tilida)

Bu — JavaScript'ni **mutlaqo noldan professional darajagacha** o'rgatadigan to'liq qo'llanma. Hech qanday oldingi dasturlash tajribasi talab qilinmaydi: birinchi `console.log`dan tortib closure, `this`, async, prototiplar, design pattern va TypeScript ko'prigigacha.

Har bir modul: **nazariya + `Why` (nega shunday) + 20 ta masala (yechimi bilan)**.

---

## Qanday ishlatish kerak

1. Modullarni **tartib bilan** o'qing (0 → 30). Har biri oldingisiga tayanadi, sakramang.
2. Har modul oxiridagi **20 ta masalani avval o'zingiz yeching**, keyin yashirin "► Yechimlar" bo'limiga qarang. Faqat o'qib ketsangiz — bilim o'rnashmaydi.
3. Kodni **brauzer konsolida** (`F12` → Console) yoki **Node.js**da yozib sinab ko'ring. Dasturlash — yozish bilan o'rganiladi.
4. "Keng tarqalgan xatolar" va `Why` bloklarini e'tibordan qochirmang — ko'pchilik aynan shu joylarda qoqiladi.

---

## Talablar (prerequisites)

| Kerak | Daraja |
|---|---|
| Kompyuter, brauzer (Chrome/Firefox) | Asoslar |
| HTML/CSS | Shart emas (3-qism — DOM uchun ozgina foydali) |
| Matn muharriri (VS Code tavsiya etiladi) | Asoslar |
| Oldingi dasturlash tajribasi | **Shart emas** — noldan boshlaymiz |

---

## To'liq yo'l xaritasi (roadmap)

### I bosqich — Asoslar
| Qism | Modullar | Mavzular |
|---|---|---|
| [1-QISM — Asoslar](./javascript-qollanma-1-qism.md) | 0–4 | Kirish, o'zgaruvchilar va turlar, operatorlar, shartlar (`if`/`switch`), sikllar |
| [2-QISM — Strukturalar](./javascript-qollanma-2-qism.md) | 5–8 | Funksiyalar, massivlar va metodlar, obyektlar, String/Number metodlari |

### II bosqich — Brauzer va asinxronlik
| Qism | Modullar | Mavzular |
|---|---|---|
| [3-QISM — Brauzer (DOM)](./javascript-qollanma-3-qism.md) | 9–12 | DOM, events, forms va validation, localStorage |
| [4-QISM — Asinxron JS](./javascript-qollanma-4-qism.md) | 13–16 | Callbacks va Event Loop, Promises, `async`/`await`, Fetch API va REST |

### III bosqich — Chuqur JS
| Qism | Modullar | Mavzular |
|---|---|---|
| [5-QISM (1-bo'lim) — OOP yadrosi](./javascript-qollanma-5-qism-1.md) | 17–20 | Scope/closure/hoisting, `this`/`call`/`apply`/`bind`, prototiplar, classlar |
| [5-QISM (2-bo'lim)](./javascript-qollanma-5-qism-2.md) | 21–23 | ES6+ va modullar, error handling, regular expressions |

### IV bosqich — Expert
| Qism | Modullar | Mavzular |
|---|---|---|
| [6-QISM (1-bo'lim) — Expert](./javascript-qollanma-6-qism-1.md) | 24–27 | Functional programming, iterators/generators/Symbols, Proxy/Reflect, performance va memory |
| [6-QISM (2-bo'lim) — Yakun](./javascript-qollanma-6-qism-2.md) | 28–30 | Design patterns, bundlers va build tools, TypeScript'ga ko'prik |

> Jami: **31 modul**, har birida **20 masala** — ~620 amaliy mashq.

---

## Boshlashdan oldin

Kodni ishga tushirishning ikki oson yo'li:

1. **Brauzer konsoli (eng tez):** brauzerni och → `F12` → **Console** bo'limi → kod yoz, Enter bos.
   ```js
   console.log("Salom, dunyo!");
   ```
2. **Node.js (terminal):** [nodejs.org](https://nodejs.org) dan o'rnat, `dastur.js` fayl yarat, `node dastur.js` bilan ishga tushir.

Tayyor bo'lsang — **[1-QISM: Asoslar →](./javascript-qollanma-1-qism.md)** dan boshla.
