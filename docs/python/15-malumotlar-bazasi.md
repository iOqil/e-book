# 15 — Ma'lumotlar bazasi va SQL

Oldingi modulda ma'lumotni oddiy lug'atda saqladik — lekin dastur o'chsa, hammasi yo'qoldi. **Ma'lumotlar bazasi** ma'lumotni doimiy, tartibli va tez qidiriladigan ko'rinishda saqlaydi. Bu yakuniy modulda **SQL** tilining asoslarini va Python'ning o'rnatilgan **`sqlite3`** modulini o'rganasan — qo'shimcha hech narsa o'rnatmasdan ishlaydigan, to'liq baza.

> **Bu modulda:** ma'lumotlar bazasi nima, `sqlite3` bilan jadval yaratish, ma'lumot qo'shish/o'qish/yangilash/o'chirish (SQL), va xavfsiz so'rovlar (parametrlash).

---

## 15.1 Ma'lumotlar bazasi nima?

Ma'lumotlar bazasi — ma'lumotni **jadval**lar ko'rinishida saqlaydi (Excel jadvaliga o'xshash, lekin ancha kuchli). Jadval **ustun**lar (maydonlar) va **qator**lardan (yozuvlar) iborat.

Misol — `talabalar` jadvali:

| id | ism | yosh | ball |
|----|-----|------|------|
| 1 | Aziz | 20 | 85 |
| 2 | Malika | 22 | 90 |

Jadvalning ustun (maydon), qator (yozuv) va birlamchi kalit (`id`) qismlarini quyidagicha tasavvur qil:

![Jadval anatomiyasi: ustun, qator va birlamchi kalit](rasmlar/py15-jadval-anatomiyasi.svg)

Baza bilan **SQL** (Structured Query Language) tilida "gaplashasan". `sqlite3` Python bilan birga keladi — o'rnatish shart emas, va butun baza bitta faylda saqlanadi. Boshlash uchun ideal.

---

## 15.2 Bazaga ulanish va jadval yaratish

```python
import sqlite3

# Bazaga ulanish (fayl yo'q bo'lsa, yaratiladi):
conn = sqlite3.connect("maktab.db")
cursor = conn.cursor()

# Jadval yaratish (SQL):
cursor.execute("""
    CREATE TABLE IF NOT EXISTS talabalar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism TEXT NOT NULL,
        yosh INTEGER,
        ball REAL
    )
""")

conn.commit()      # o'zgarishlarni saqlash
conn.close()       # ulanishni yopish
```

Tushuntirish:
- `connect("maktab.db")` — baza fayliga ulanadi (yo'q bo'lsa yaratadi).
- `cursor` — buyruqlarni bajaruvchi "kursor".
- `CREATE TABLE IF NOT EXISTS` — jadval yo'q bo'lsa yaratadi (bor bo'lsa xato bermaydi).
- `INTEGER PRIMARY KEY AUTOINCREMENT` — har yozuvga avtomatik o'sib boruvchi `id`.
- `TEXT`, `INTEGER`, `REAL` — ustun turlari (matn, butun son, kasr).
- `conn.commit()` — o'zgarishlarni faylga **yozadi** (busiz saqlanmaydi!).

---

## 15.3 Ma'lumot qo'shish (INSERT)

```python
import sqlite3
conn = sqlite3.connect("maktab.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO talabalar (ism, yosh, ball) VALUES (?, ?, ?)",
    ("Aziz", 20, 85.5)
)
conn.commit()
conn.close()
```

> **`?` belgilari — JUDA muhim (xavfsizlik!):** qiymatlarni SQL matniga to'g'ridan-to'g'ri yozma, doim `?` ishlatib, qiymatlarni alohida uzat. Aks holda **SQL injection** degan jiddiy xavfsizlik zaifligi paydo bo'ladi. Bu eng muhim qoidalardan biri.
>
> ```python
> # ❌ HECH QACHON BUNDAY QILMA:
> cursor.execute(f"INSERT INTO talabalar (ism) VALUES ('{ism}')")
> # ✅ DOIM BUNDAY:
> cursor.execute("INSERT INTO talabalar (ism) VALUES (?)", (ism,))
> ```

Ko'p yozuvni birdan qo'shish (`executemany`):

```python
talabalar = [("Malika", 22, 90), ("Bobur", 21, 78)]
cursor.executemany(
    "INSERT INTO talabalar (ism, yosh, ball) VALUES (?, ?, ?)",
    talabalar
)
conn.commit()
```

Yozish (`INSERT` + `commit`) va o'qish (`SELECT` + `fetchall`) dastur bilan baza fayli orasida shunday aylanadi:

![Dastur va baza orasidagi yozish/o'qish sikli](rasmlar/py15-insert-select-sikli.svg)

---

## 15.4 Ma'lumot o'qish (SELECT)

```python
import sqlite3
conn = sqlite3.connect("maktab.db")
cursor = conn.cursor()

# Barcha yozuvlar:
cursor.execute("SELECT * FROM talabalar")
qatorlar = cursor.fetchall()       # barcha natijalar ro'yxati
for qator in qatorlar:
    print(qator)                   # (1, 'Aziz', 20, 85.5)

# Bitta yozuv:
cursor.execute("SELECT * FROM talabalar WHERE id = ?", (1,))
print(cursor.fetchone())           # bitta qator yoki None

conn.close()
```

Foydali SQL so'rovlari:

```python
# Shart bilan:
cursor.execute("SELECT * FROM talabalar WHERE yosh > ?", (20,))

# Tartiblash:
cursor.execute("SELECT * FROM talabalar ORDER BY ball DESC")

# Faqat kerakli ustunlar:
cursor.execute("SELECT ism, ball FROM talabalar")

# Sanash:
cursor.execute("SELECT COUNT(*) FROM talabalar")
print(cursor.fetchone()[0])        # nechta talaba bor
```

> **SQL kalit so'zlari:** `SELECT` (tanlash) ... `FROM` (qaysi jadval) ... `WHERE` (shart) ... `ORDER BY` (tartiblash) ... `DESC`/`ASC` (kamayish/o'sish). Bular barcha SQL bazalarda deyarli bir xil.

So'rovning uch qismi — `SELECT` (qaysi ustunlar), `FROM` (qaysi jadval), `WHERE` (qaysi qatorlar) — qanday ishlashini quyidagi oqim ko'rsatadi:

![SELECT ... FROM ... WHERE so'rov oqimi](rasmlar/py15-select-where-oqimi.svg)

---

## 15.5 Yangilash (UPDATE) va o'chirish (DELETE)

```python
# Yangilash:
cursor.execute(
    "UPDATE talabalar SET ball = ? WHERE id = ?",
    (95, 1)
)
conn.commit()

# O'chirish:
cursor.execute("DELETE FROM talabalar WHERE id = ?", (2,))
conn.commit()
```

> **Diqqat — `WHERE`ni unutma!** `UPDATE` yoki `DELETE` da `WHERE` yozmasang, **butun jadval**ga ta'sir qiladi (hamma yozuv o'chadi/o'zgaradi). Bu juda keng tarqalgan, achchiq xato. Doim `WHERE` borligini tekshir.

---

## 15.6 `with` bilan toza ishlash

8-moduldagi `with` bu yerda ham ishlaydi — ulanishni avtomatik boshqaradi:

```python
import sqlite3

with sqlite3.connect("maktab.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM talabalar")
    for qator in cursor.fetchall():
        print(qator)
    # with bloki commit'ni avtomatik bajaradi
```

---

## 15.7 Keyingi qadam: katta loyihalar uchun

`sqlite3` o'rganish va kichik loyihalar uchun ajoyib. Loyihalaring kattalashganda quyidagilarni o'rganasan (ular ilg'orroq, hozir shart emas):
- **PostgreSQL / MySQL** — ko'p foydalanuvchili, katta loyihalar uchun kuchli bazalar (alohida server sifatida ishlaydi). Python'da ularga ulanish uchun maxsus kutubxonalar bor.
- **ORM** (masalan SQLAlchemy) — SQL yozmasdan, baza bilan Python obyektlari orqali ishlash usuli. Klasslar jadvalga, obyektlar qatorlarga mos keladi.

Bularning hammasi shu modulda o'rgangan asoslarga (jadval, qator, SELECT/INSERT/UPDATE/DELETE) tayanadi — shuning uchun bu poydevor muhim.

---

## ✍️ Masalalar (20 ta)

> Bu masalalar `sqlite3` bilan ishlaydi — har birini ishga tushirib, yaratilgan `.db` faylni sina.

**Oson (1–7):**

1. `test.db` bazasiga ulanib, `talabalar` jadvalini yarat (`id`, `ism`, `yosh`).
2. Jadvalga bitta talaba qo'sh (`INSERT` + `?` parametrlar bilan).
3. `SELECT * FROM talabalar` bilan barcha yozuvlarni o'qib chiqar.
4. `executemany` bilan 3 ta talabani birdan qo'sh.
5. `WHERE` bilan id'si 1 bo'lgan talabani top.
6. `COUNT(*)` bilan jadvaldagi yozuvlar sonini chiqar.
7. `ORDER BY` bilan talabalarni yoshi bo'yicha tartiblab chiqar.

**O'rta (8–14):**

8. `UPDATE` bilan bitta talabaning yoshini o'zgartir (`WHERE` bilan).
9. `DELETE` bilan bitta talabani o'chir (`WHERE` bilan).
10. `WHERE yosh > ?` bilan yoshi 20 dan katta talabalarni top.
11. Foydalanuvchidan ism va yosh so'rab (`input`), bazaga qo'sh (`?` parametrlar bilan).
12. `SELECT ism, yosh` bilan faqat kerakli ustunlarni o'qi.
13. `mahsulotlar` jadvali yarat (`nom`, `narx`), bir nechta mahsulot qo'sh, narxi bo'yicha kamayish tartibida chiqar.
14. `with sqlite3.connect(...)` ishlatib, jadvalni o'qib chiqar.

**Murakkab (15–20):**

15. To'liq CRUD funksiyalari yoz: `qosh(ism, yosh)`, `royxat()`, `yangila(id, yosh)`, `ochir(id)` — har biri bazaga ulanib ishlasin.
16. Oddiy "telefon kitobchasi" dasturi: menyu (qo'shish/ko'rish/o'chirish) bilan, ma'lumot `sqlite3` bazada saqlansin.
17. `WHERE ism LIKE ?` bilan qidiruv: ismida berilgan harf(lar) bor talabalarni top (`LIKE '%a%'`).
18. Ballar jadvali yaratib, `SELECT AVG(ball), MAX(ball), MIN(ball)` bilan statistika chiqar.
19. Oddiy "vazifalar" (todo) dasturi: vazifa qo'shish, bajarildi deb belgilash (`UPDATE`), o'chirish — bazada saqlansin.
20. Mini inventarizatsiya: `mahsulotlar` jadvali (`nom`, `soni`, `narx`); qo'shish, sotish (sonni kamaytirish, `UPDATE`), umumiy qiymatni hisoblash (`SELECT SUM(soni * narx)`) funksiyalari bilan to'liq dastur yoz.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
import sqlite3

# 1
conn = sqlite3.connect("test.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS talabalar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ism TEXT NOT NULL,
    yosh INTEGER
)""")
conn.commit()

# 2
cur.execute("INSERT INTO talabalar (ism, yosh) VALUES (?, ?)", ("Aziz", 20))
conn.commit()

# 3
cur.execute("SELECT * FROM talabalar")
for q in cur.fetchall():
    print(q)

# 4
cur.executemany(
    "INSERT INTO talabalar (ism, yosh) VALUES (?, ?)",
    [("Malika", 22), ("Bobur", 21), ("Gul", 19)]
)
conn.commit()

# 5
cur.execute("SELECT * FROM talabalar WHERE id = ?", (1,))
print(cur.fetchone())

# 6
cur.execute("SELECT COUNT(*) FROM talabalar")
print("Jami:", cur.fetchone()[0])

# 7
cur.execute("SELECT * FROM talabalar ORDER BY yosh")
for q in cur.fetchall():
    print(q)

# 8
cur.execute("UPDATE talabalar SET yosh = ? WHERE id = ?", (25, 1))
conn.commit()

# 9
cur.execute("DELETE FROM talabalar WHERE id = ?", (4,))
conn.commit()

# 10
cur.execute("SELECT * FROM talabalar WHERE yosh > ?", (20,))
print(cur.fetchall())

# 11
ism = input("Ism: ")
yosh = int(input("Yosh: "))
cur.execute("INSERT INTO talabalar (ism, yosh) VALUES (?, ?)", (ism, yosh))
conn.commit()

# 12
cur.execute("SELECT ism, yosh FROM talabalar")
for q in cur.fetchall():
    print(q)

# 13
cur.execute("""CREATE TABLE IF NOT EXISTS mahsulotlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, narx REAL
)""")
cur.executemany("INSERT INTO mahsulotlar (nom, narx) VALUES (?, ?)",
                [("Olma", 12000), ("Non", 4000), ("Go'sht", 90000)])
conn.commit()
cur.execute("SELECT * FROM mahsulotlar ORDER BY narx DESC")
print(cur.fetchall())
conn.close()

# 14
with sqlite3.connect("test.db") as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM talabalar")
    for q in cur.fetchall():
        print(q)

# 15
def ulanish():
    return sqlite3.connect("test.db")
def qosh(ism, yosh):
    with ulanish() as c:
        c.execute("INSERT INTO talabalar (ism, yosh) VALUES (?, ?)", (ism, yosh))
def royxat():
    with ulanish() as c:
        return c.execute("SELECT * FROM talabalar").fetchall()
def yangila(id, yosh):
    with ulanish() as c:
        c.execute("UPDATE talabalar SET yosh = ? WHERE id = ?", (yosh, id))
def ochir(id):
    with ulanish() as c:
        c.execute("DELETE FROM talabalar WHERE id = ?", (id,))
qosh("Kamol", 23)
print(royxat())

# 16
def init():
    with sqlite3.connect("tel.db") as c:
        c.execute("""CREATE TABLE IF NOT EXISTS kontaktlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ism TEXT, raqam TEXT)""")
init()
while True:
    amal = input("qosh / korish / ochirish / chiqish: ")
    if amal == "chiqish":
        break
    with sqlite3.connect("tel.db") as c:
        if amal == "qosh":
            ism = input("Ism: "); raqam = input("Raqam: ")
            c.execute("INSERT INTO kontaktlar (ism, raqam) VALUES (?, ?)", (ism, raqam))
        elif amal == "korish":
            for q in c.execute("SELECT * FROM kontaktlar").fetchall():
                print(q)
        elif amal == "ochirish":
            id = int(input("id: "))
            c.execute("DELETE FROM kontaktlar WHERE id = ?", (id,))

# 17
with sqlite3.connect("test.db") as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM talabalar WHERE ism LIKE ?", ("%a%",))
    print(cur.fetchall())

# 18
with sqlite3.connect("ball.db") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS b (id INTEGER PRIMARY KEY, ball REAL)")
    cur.executemany("INSERT INTO b (ball) VALUES (?)", [(85,), (90,), (78,), (92,)])
    cur.execute("SELECT AVG(ball), MAX(ball), MIN(ball) FROM b")
    print(cur.fetchone())     # (86.25, 92.0, 78.0)

# 19
def todo_init():
    with sqlite3.connect("todo.db") as c:
        c.execute("""CREATE TABLE IF NOT EXISTS vazifalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, matn TEXT, bajarildi INTEGER DEFAULT 0)""")
todo_init()
def vazifa_qosh(matn):
    with sqlite3.connect("todo.db") as c:
        c.execute("INSERT INTO vazifalar (matn) VALUES (?)", (matn,))
def vazifa_belgila(id):
    with sqlite3.connect("todo.db") as c:
        c.execute("UPDATE vazifalar SET bajarildi = 1 WHERE id = ?", (id,))
def vazifa_ochir(id):
    with sqlite3.connect("todo.db") as c:
        c.execute("DELETE FROM vazifalar WHERE id = ?", (id,))
vazifa_qosh("Python o'rganish")
vazifa_belgila(1)

# 20
def inv_init():
    with sqlite3.connect("inv.db") as c:
        c.execute("""CREATE TABLE IF NOT EXISTS mahsulotlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, soni INTEGER, narx REAL)""")
inv_init()
def mahsulot_qosh(nom, soni, narx):
    with sqlite3.connect("inv.db") as c:
        c.execute("INSERT INTO mahsulotlar (nom, soni, narx) VALUES (?, ?, ?)", (nom, soni, narx))
def sotish(id, miqdor):
    with sqlite3.connect("inv.db") as c:
        c.execute("UPDATE mahsulotlar SET soni = soni - ? WHERE id = ?", (miqdor, id))
def umumiy_qiymat():
    with sqlite3.connect("inv.db") as c:
        return c.execute("SELECT SUM(soni * narx) FROM mahsulotlar").fetchone()[0]
mahsulot_qosh("Olma", 100, 12000)
mahsulot_qosh("Non", 50, 4000)
sotish(1, 10)
print("Umumiy qiymat:", umumiy_qiymat())
```

</details>

---

---

## 🎉 Tabriklayman — kursni tugatding!

Bu — boshlovchilar yo'nalishining **oxirgi moduli**. Noldan boshlab, sen quyidagilarni o'rganding:

- **Asoslar:** o'zgaruvchilar, tiplar, shartlar, sikllar, funksiyalar (01–02)
- **Ma'lumot:** ro'yxat, lug'at, to'plam, stringlar (03–04)
- **OOP:** klasslar, obyektlar, meros (05)
- **Tashkil etish:** modullar, virtual muhit, xatolarni boshqarish (06–07)
- **Ma'lumot bilan ishlash:** fayllar, JSON, CSV (08)
- **Ilg'or vositalar:** generatorlar, dekoratorlar, tip ko'rsatmalari, standart kutubxona (09–11)
- **Professional ko'nikmalar:** parallel ishlash, test yozish, veb API, ma'lumotlar bazasi (12–15)

**Endi nima qilish kerak?**
1. **Loyiha yoz.** Eng yaxshi o'rganish — amaliyot. Kichik bir narsa qil: CLI dastur, telegram bot, yoki kichik veb API (14 + 15 modullarni birlashtirib).
2. **Rasmiy hujjatni o'qi.** [docs.python.org](https://docs.python.org/3/) — eng ishonchli manba. Endi uni o'qiy oladigan darajadasan.
3. **Mashq qil.** Har modulning 20 ta masalasini yechib chiqqaningga ishonch hosil qil.

Omad! 🚀

[← FastAPI veb API](./14-web-capstone.md) | [Boshlovchilar README ↑](./README.md)
