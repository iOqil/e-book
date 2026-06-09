# 01 — Asoslar: sintaksis, tiplar, "Pythonic" tafakkur

[← README](./README.md) | [Keyingi: Boshqaruv va funksiyalar →](./02-boshqaruv-funksiyalar.md)

---

## 1.1 Chekinish (indentation) = sintaksis

Python'da kod bloklari **chekinish** (qatorni bo'sh joy bilan ichkariga surish) orqali aniqlanadi. Qavslar (`{ }`) ishlatilmaydi — qaysi qatorlar blok ichida ekanini aynan chekinish belgilaydi.

```python
if x > 0:
    print("musbat")      # 4 probel — bu blokni bildiradi
    print("hali ham ichida")
print("blokdan tashqarida")
```

Qoidalar:
- Standart — **4 probel** (tab emas; aralashtirib bo'lmaydi).
- `:` blok ochilishini bildiradi (`if`, `for`, `def`, `class` va h.k.).
- Noto'g'ri chekinish → `IndentationError`.

> **Why:** Bu "kosmetik" emas — Python sintaksisni vizual tuzilmaga bog'laydi, shuning uchun "format urushlari" bo'lmaydi va kod doim bir xil ko'rinadi.

---

## 1.2 O'zgaruvchilar va dinamik tiplash

```python
x = 5            # int
x = "salom"      # endi str — muammo yo'q
name = "Oqil"
PI = 3.14159     # konstanta: katta harf bilan yozish — kelishuv, til majburlamaydi
```

- O'zgaruvchini oldindan e'lon qilish (`declare`) shart emas — nom yozib, `=` bilan qiymat berasan, tamom. Nom oldiga maxsus belgi qo'yilmaydi, qator oxiriga `;` ham qo'yilmaydi.
- Python **dinamik tiplangan** (o'zgaruvchining turi qiymatga qarab avtomatik aniqlanadi), lekin ayni paytda **kuchli tiplangan** (strongly typed): `"3" + 5` xato beradi, turlar avtomatik aralashtirilmaydi.

Python'da o'zgaruvchi qiymatni o'z ichida saqlamaydi — u obyektga **ishora qiluvchi nom**dir (reference model). Shuning uchun `b = a` obyektni nusxalamaydi, balki bitta obyektga ikkinchi nom beradi:

![Nom obyektga ishora qiladi: reference model va bir obyektga ikki nom](rasmlar/py01-reference-model.svg)

Tur nomda emas, **obyektda** turgani uchun bir nomni ketma-ket har xil turdagi obyektlarga bog'lash mumkin — dinamik tiplash aynan shu:

![Dinamik tiplash: bitta nom har xil turdagi obyektlarga qayta bog'lanadi](rasmlar/py01-dinamik-tiplash.svg)

```python
"3" + 5     # TypeError! Python matn va sonni avtomatik qo'shmaydi
"3" + str(5)   # "35"  ✅
int("3") + 5   # 8     ✅
```

### Type hints (tip ko'rsatmalari)

Python'da tiplar majburiy emas, lekin **type hints** yozish — professional standart. Bu funksiya qanday turdagi ma'lumot kutishini va nima qaytarishini ochiq ko'rsatadi:

```python
age: int = 25
name: str = "Oqil"

def greet(name: str) -> str:
    return f"Salom, {name}"
```

> Type hints dastur ishlayotganda (runtime'da) **majburlanmaydi** — ular `mypy`/Pylance kabi statik tekshiruvchilar uchun. Lekin baribir doim yoz — kod o'qilishi osonlashadi va xatolar oldindan topiladi.

---

## 1.3 Raqamli tiplar

```python
a = 10           # int — CHEKSIZ aniqlik (big integer muammosi yo'q!)
b = 3.14         # float (64-bit)
c = 2 + 3j       # complex (kamdan-kam kerak)

2 ** 100         # 1267650600228229401496703205376 — muammosiz, overflow yo'q
```

> **Diqqat:** Python'da butun son (`int`) **cheksiz aniqlikka** ega — son qanchalik katta bo'lmasin, "overflow" (to'lib ketish) muammosi yo'q. Bu katta hisob-kitoblarda juda qulay.

### Bo'lish — eng ko'p chalkashtiriladigan joy

```python
7 / 2      # 3.5   — `/` har doim float (kasr son) qaytaradi
7 // 2     # 3     — butun bo'lish (floor division)
7 % 2      # 1     — qoldiq
-7 // 2    # -4    — pastga yaxlitlaydi, 0 tomon emas!
divmod(7, 2)  # (3, 1) — butun va qoldiq birga
```

---

## 1.4 Boolean va "truthiness"

```python
True, False          # bosh harf bilan!
None                 # "hech narsa" / bo'sh qiymat

# Mantiqiy operatorlar — so'z bilan:
x and y              # &&
x or y               # ||
not x                # !
```

**Truthiness** — bo'sh yoki nol qiymatlar `if` ichida `False` deb baholanadi (aniq qoidalar bilan):

```python
# False deb baholanadi:
bool(0), bool(0.0), bool(""), bool([]), bool({}), bool(None), bool(set())
# True deb baholanadi: deyarli hamma narsa, jumladan "0" (string!), [0], " "
```

Quyidagi diagramma qaysi qiymatlar `False`, qaysilari `True` deb baholanishini aniq ko'rsatadi (diqqat: `"0"` va `[0]` bo'sh emas, demak `True`):

![Truthiness: qaysi qiymatlar False, qaysilari True deb baholanadi](rasmlar/py01-truthiness.svg)

> **Idioma:** `if len(items) > 0:` o'rniga `if items:` yoz. Bo'sh list `False`. Bu Pythonic.

`and`/`or` qiymat qaytaradi (short-circuit), faqat bool emas:

```python
name = user_input or "Mehmon"   # bo'sh bo'lsa "Mehmon" (qisqa, qulay yozuv)
```

---

## 1.5 `None`, `==` va `is`

```python
x = None
x == None      # ishlaydi, lekin...
x is None      # ✅ to'g'ri uslub — identite (xotira) tekshiruvi
```

- `==` — **qiymat** tengligi (qiymatlarni solishtiradi va turni ham hisobga oladi: `1 == "1"` → `False`).
- `is` — **bir xil obyektmi** (xotirada bir joymi). `None`, `True`, `False` bilan doim `is` ishlat.

```python
a = [1, 2]
b = [1, 2]
a == b     # True  — qiymatlar teng
a is b     # False — alohida obyektlar
```

Bu farqni vizual ko'rinishda: `a` va `b` qiymati bir xil, ammo xotirada ikki **alohida obyekt** — shuning uchun `==` `True`, `is` esa `False` qaytaradi:

![== qiymat tengligi va is ayniyat (bir xil obyektmi) farqi](rasmlar/py01-eq-vs-is.svg)

---

## 1.6 Tip konvertatsiyasi

```python
int("42")        # 42
int("42", 16)    # 66  — 16-lik sanoq sistemasidan
float("3.14")    # 3.14
str(42)          # "42"
bool(0)          # False
list("abc")      # ['a', 'b', 'c']

# Xavfsiz konvertatsiya:
int("abc")       # ValueError — try/except kerak (07-modulda)
```

---

## 1.7 Kiritish/chiqarish (I/O)

```python
print("Salom", "dunyo")              # Salom dunyo  (probel bilan ajraladi)
print("a", "b", sep="-")             # a-b
print("yangi qatorsiz", end="")      # \n qo'shmaydi
print(f"{name} — {age} yosh")        # f-string (eng muhim!)

ism = input("Isming: ")              # har doim STRING qaytaradi
yosh = int(input("Yoshing: "))       # raqam kerak bo'lsa konvertatsiya qil
```

> `input()` **har doim string qaytaradi** — foydalanuvchi raqam yozsa ham, u matn bo'lib keladi. Raqam kerak bo'lsa `int()`/`float()` bilan o'ra.

---

## 1.8 f-string — formatlashning to'g'ri yo'li

```python
name = "Oqil"
age = 25
price = 1234567.891

f"{name} {age} yoshda"               # Oqil 25 yoshda
f"{price:,.2f}"                      # 1,234,567.89  — minglik ajratgich + 2 kasr
f"{age:03d}"                         # 025           — 3 xonali, nol bilan
f"{0.1234:.1%}"                      # 12.3%
f"{name=}"                           # name='Oqil'   — debug uchun (3.8+)
f"{2 + 2}"                           # 4 — ichida ifoda yozish mumkin
```

> f-string — matn ichiga to'g'ridan-to'g'ri o'zgaruvchi va ifoda joylashning eng toza yo'li: `f"..."` ichida `{...}` qavslar orasiga istalgan ifoda va formatlashni yozasan. **Eski usullar (`.format()`, `%`) ni unut — f-string ishlat.**

---

## 1.9 Bir nechta qiymat berish (multiple assignment)

```python
a, b, c = 1, 2, 3            # bir vaqtda
a, b = b, a                  # almashtirish — vaqtinchalik o'zgaruvchisiz!
x = y = z = 0                # hammasi 0

first, *rest = [1, 2, 3, 4]  # first=1, rest=[2,3,4]  (unpacking)
```

> `a, b = b, a` — ikki o'zgaruvchini almashtirishning eng nafis yo'li. Ko'p tillarda buning uchun vaqtinchalik uchinchi o'zgaruvchi kerak; Python'da bitta qator yetadi.

---

## 1.10 Walrus operatori `:=` (3.8+)

Ifoda ichida o'zgaruvchiga qiymat berish:

```python
# Oddiy:
data = input()
while data != "quit":
    print(data)
    data = input()

# Walrus bilan:
while (data := input()) != "quit":
    print(data)
```

> Kerak bo'lgandagina ishlat — o'qilishini buzmasin.

---

## 1.11 Izohlar va docstring

```python
# Bir qatorli izoh

"""
Ko'p qatorli — texnik jihatdan string,
lekin izoh sifatida ishlatiladi.
"""

def hisobla(x: int) -> int:
    """Funksiya docstring'i — help() shuni ko'rsatadi."""
    return x * 2

help(hisobla)   # docstring'ni chiqaradi
```

---

## ✍️ Masalalar (20 ta)

> Yechimga qaramasdan ishla. REPL'da sina. Yechimlar fayl oxirida.

**Oson (1–7):**

1. Foydalanuvchidan ism va yoshni so'ra, `"<ism> <yosh> yoshda"` ko'rinishida chiqar (f-string bilan).
2. Ikkita raqamni foydalanuvchidan ol, ularning yig'indisi, ayirmasi, ko'paytmasi, bo'linmasi (`/`), butun bo'linmasi (`//`) va qoldig'ini chiqar.
3. `a = 5`, `b = 10` — vaqtinchalik o'zgaruvchisiz ularni almashtir va natijani chiqar.
4. Sekunddagi vaqtni (masalan 3725) soat, daqiqa, sekundga aylantir: `1:02:05`.
5. Berilgan narx (`1234567.5`) ni minglik ajratgich va 2 kasr bilan chiqar: `1,234,567.50`.
6. `"3"` va `5` ni qo'shib `8` chiqar (tip muammosini hal qilib).
7. Doira radiusini ol, yuzasi va perimetrini hisobla (`PI = 3.14159`).

**O'rta (8–14):**

8. Foydalanuvchidan haroratni Selsiyda ol, Farengeytga aylantir: `F = C * 9/5 + 32`.
9. Ikki xonali sonni ol, uning raqamlari yig'indisini hisobla (masalan `47 → 11`). *(Bo'lish/qoldiq bilan, stringsiz.)*
10. `bool()` ni quyidagilarga qo'llab, qaysi biri `True`/`False` ekanini bashorat qil, keyin tekshir: `0`, `""`, `"0"`, `[]`, `[0]`, `None`, `" "`, `0.0`.
11. `x = 0`, `y = "default"` — `x or y` va `x and y` nima qaytaradi? Bashorat qilib tekshir va sababini tushuntir.
12. Foydalanuvchidan 3 ta baho ol (`input`), o'rtachasini 2 kasr bilan chiqar.
13. `a = [1,2]`, `b = [1,2]`, `c = a` bo'lsa: `a == b`, `a is b`, `a is c` — har birini bashorat qilib tekshir.
14. Bir qatorli kodda 5 ta o'zgaruvchiga (`a,b,c,d,e`) `[10,20,30,40,50]` listidan qiymat ber (unpacking).

**Murakkab (15–20):**

15. `first, *middle, last = [1,2,3,4,5]` — har biri nimaga teng? Yozib tekshir, keyin `*middle` ning tipi nima ekanini ayt.
16. Foydalanuvchidan summa (so'm) va valyuta kursini ol, dollarga aylantirib `$<qiymat>` ko'rinishida 2 kasr bilan chiqar.
17. Walrus operatori bilan: foydalanuvchidan son so'rab, "quit" deguncha har sonning kvadratini chiqaruvchi sikl yoz.
18. `2 ** 1000` ni hisobla — natija nechta xonali ekanini top. *(Maslahat: stringga aylantirib uzunligini ol.)*
19. Bir xonali son `n` (1–9) berilganda, uning quyidagi jadvalini chiqar: `n x 1 = n` dan `n x 9 = 9n` gacha (f-string, hozircha `for` ishlatmasdan 9 ta `print` bilan ham bo'ladi — yoki `for` bilsang, ishlat).
20. `divmod()` dan foydalanib, 1000 daqiqani kun:soat:daqiqaga aylantir (masalan `1500 → 1 kun 1 soat 0 daqiqa`).

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
ism = input("Isming: ")
yosh = input("Yoshing: ")
print(f"{ism} {yosh} yoshda")

# 2
a = int(input())
b = int(input())
print(a + b, a - b, a * b, a / b, a // b, a % b)

# 3
a, b = 5, 10
a, b = b, a
print(a, b)        # 10 5

# 4
t = 3725
soat = t // 3600
daqiqa = (t % 3600) // 60
sekund = t % 60
print(f"{soat}:{daqiqa:02d}:{sekund:02d}")   # 1:02:05

# 5
narx = 1234567.5
print(f"{narx:,.2f}")        # 1,234,567.50

# 6
print(int("3") + 5)          # 8

# 7
PI = 3.14159
r = float(input("Radius: "))
print(f"Yuza: {PI * r ** 2:.2f}, Perimetr: {2 * PI * r:.2f}")

# 8
c = float(input("Selsiy: "))
print(f"{c * 9/5 + 32:.1f} F")

# 9
n = 47
print(n // 10 + n % 10)      # 11

# 10
for v in (0, "", "0", [], [0], None, " ", 0.0):
    print(repr(v), "->", bool(v))
# 0->False, ''->False, '0'->True, []->False, [0]->True, None->False, ' '->True, 0.0->False

# 11
x, y = 0, "default"
print(x or y)     # "default"  (x falsy bo'lgani uchun y qaytadi)
print(x and y)    # 0          (x falsy bo'lsa and to'xtaydi, x ni qaytaradi)

# 12
a, b, c = int(input()), int(input()), int(input())
print(f"{(a + b + c) / 3:.2f}")

# 13
a, b = [1, 2], [1, 2]
c = a
print(a == b)     # True   qiymat teng
print(a is b)     # False  alohida obyekt
print(a is c)     # True   c — a ning o'zi

# 14
a, b, c, d, e = [10, 20, 30, 40, 50]
print(a, b, c, d, e)

# 15
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)   # 1 [2, 3, 4] 5
print(type(middle))          # <class 'list'>  — har doim list

# 16
summa = float(input("So'm: "))
kurs = float(input("Kurs: "))
print(f"${summa / kurs:.2f}")

# 17
while (son := input("Son ('quit' to'xtatadi): ")) != "quit":
    print(int(son) ** 2)

# 18
print(len(str(2 ** 1000)))   # 302

# 19
n = int(input("Son (1-9): "))
for i in range(1, 10):
    print(f"{n} x {i} = {n * i}")

# 20
daqiqa = 1500
kun, qoldiq = divmod(daqiqa, 24 * 60)
soat, daq = divmod(qoldiq, 60)
print(f"{kun} kun {soat} soat {daq} daqiqa")   # 1 kun 1 soat 0 daqiqa
```

</details>

---

[← README](./README.md) | [Keyingi: Boshqaruv va funksiyalar →](./02-boshqaruv-funksiyalar.md)
