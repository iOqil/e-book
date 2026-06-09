# 11 — Standart kutubxona ("hammasi ichida")

Python "hammasi ichida" (batteries included) tamoyili bilan keladi: ko'p foydali vositalar o'rnatmasdan, til bilan birga keladi. Bu modulda eng ko'p ishlatiladigan standart modullar bilan tanishasan — ular kundalik ishingni ancha osonlashtiradi.

> **Bu modulda:** `collections` (Counter, defaultdict), `datetime` (sana/vaqt), `random` (tasodif), va `math` (matematika).

---

## 11.1 `collections` — qulay to'plamlar

**`Counter`** — narsalarni sanash uchun (3-moduldagi qo'lda sanashning tayyor varianti):

```python
from collections import Counter

ovozlar = ["ha", "yo'q", "ha", "ha", "yo'q"]
hisob = Counter(ovozlar)
print(hisob)                  # Counter({'ha': 3, "yo'q": 2})
print(hisob["ha"])            # 3
print(hisob.most_common(1))   # [('ha', 3)]  — eng ko'p uchragani

# Matndagi harflarni sanash:
print(Counter("mississippi"))  # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
```

`Counter` ro'yxat bo'ylab yurib, har bir elementni avtomatik sanaydi va natijani "element → nechta marta" lug'ati ko'rinishida qaytaradi:

![Counter ro'yxatdagi har elementni sanab chastota lug'atini yasaydi](rasmlar/py11-counter.svg)

**`defaultdict`** — yo'q kalitga avtomatik standart qiymat beradi (`KeyError` bo'lmaydi):

```python
from collections import defaultdict

guruh = defaultdict(list)     # yo'q kalit avtomatik bo'sh ro'yxat bo'ladi
for ism, sinf in [("Ali", "A"), ("Vali", "B"), ("Gul", "A")]:
    guruh[sinf].append(ism)   # KeyError yo'q — kalit avtomatik yaratiladi

print(dict(guruh))            # {'A': ['Ali', 'Gul'], 'B': ['Vali']}
```

> Oddiy `dict` bilan buni `if kalit not in lugat: lugat[kalit] = []` qilib yozarding — `defaultdict` shuni avtomatlashtiradi.

---

## 11.2 `datetime` — sana va vaqt

```python
from datetime import datetime, date, timedelta

hozir = datetime.now()        # hozirgi sana va vaqt
bugun = date.today()          # bugungi sana

print(hozir.year, hozir.month, hozir.day)   # 2026 6 9
print(bugun)                  # 2026-06-09

# Chiroyli formatlash (strftime):
print(hozir.strftime("%d.%m.%Y"))           # 09.06.2026
print(hozir.strftime("%H:%M"))              # 14:30

# Matndan sana o'qish (strptime):
sana = datetime.strptime("2026-01-15", "%Y-%m-%d")

# timedelta — vaqt qo'shish/ayirish:
keyingi_hafta = bugun + timedelta(days=7)
print(keyingi_hafta)          # 7 kun keyin

farq = date(2026, 12, 31) - bugun
print(farq.days, "kun qoldi")
```

Sana — bu vaqt o'qidagi nuqta, `timedelta` esa ikki nuqta orasidagi oraliq: sanaga `timedelta` qo'shsang yangi sana chiqadi, ikki sanani ayirsang `timedelta` (farq) chiqadi:

![datetime sana nuqtasi, timedelta esa oraliq: qo'shish va ayirish vaqt o'qida](rasmlar/py11-datetime-timedelta.svg)

> `strftime` (sanani matnga) va `strptime` (matnni sanaga) — kodlar: `%Y`=yil, `%m`=oy, `%d`=kun, `%H`=soat, `%M`=daqiqa. Hammasini yodlash shart emas, kerak bo'lganda qaraysan.

---

## 11.3 `random` — tasodifiy sonlar

```python
import random

print(random.randint(1, 6))            # 1..6 oralig'ida (zar)
print(random.random())                 # 0.0–1.0 oralig'ida kasr
print(random.choice(["olma", "banan", "uzum"]))   # tasodifiy bittasi

karta = [1, 2, 3, 4, 5]
random.shuffle(karta)                   # ro'yxatni joyida aralashtiradi
print(karta)

# Ro'yxatdan bir nechta tasodifiy (takrorsiz):
print(random.sample(range(1, 50), 5))   # 5 ta tasodifiy son
```

> **Diqqat:** `random` o'yinlar va simulyatsiya uchun. Parol, token, xavfsizlik uchun **ishlatma** — uning natijasi bashorat qilinadi. Xavfsizlik kerak bo'lganda `secrets` moduli bor.

---

## 11.4 `math` — matematik funksiyalar

```python
import math

print(math.sqrt(16))          # 4.0    — kvadrat ildiz
print(math.ceil(4.1))         # 5      — yuqoriga yaxlitlash
print(math.floor(4.9))        # 4      — pastga yaxlitlash
print(math.pi)                # 3.14159...
print(math.factorial(5))      # 120    — faktorial
print(math.gcd(24, 36))       # 12     — eng katta umumiy bo'luvchi
print(round(3.14159, 2))      # 3.14   — yaxlitlash (math emas, lekin foydali)
```

---

## 11.5 Boshqa foydali modullar (qisqacha)

Python'da yana ko'p tayyor modul bor. Bilib qo'ysang foydali:
- `os` — operatsion tizim bilan ishlash (papkalar, muhit o'zgaruvchilari).
- `statistics` — o'rtacha, mediana, standart og'ish.
- `time` — vaqtni o'lchash (`time.perf_counter`), kutish (`time.sleep`).
- `logging` — `print` o'rniga professional log yozish.

```python
import statistics
baholar = [85, 90, 78, 92]
print(statistics.mean(baholar))     # o'rtacha: 86.25
print(statistics.median(baholar))   # mediana
```

---

## ✍️ Masalalar (20 ta)

> Bu masalalar oldingi modullarga tayanadi.

**Oson (1–7):**

1. `Counter` bilan `"banana"` so'zidagi har harf nechta ekanini sana.
2. `Counter.most_common(1)` bilan `[1,2,2,3,3,3]` dagi eng ko'p uchragan sonni top.
3. `datetime.now()` dan bugungi sanani `"DD.MM.YYYY"` formatida chiqar.
4. `random.randint` bilan 1–100 oralig'ida 5 ta tasodifiy son ro'yxatini yasa.
5. `math.sqrt` va `math.factorial` bilan 144 ning ildizini va 5! ni chiqar.
6. `random.choice` bilan ro'yxatdan tasodifiy element tanla.
7. `random.shuffle` bilan `[1,2,3,4,5]` ni aralashtir.

**O'rta (8–14):**

8. `defaultdict(int)` bilan so'zlar ro'yxatidagi har so'z chastotasini hisobla.
9. `defaultdict(list)` bilan talabalarni sinflar bo'yicha guruhla.
10. `timedelta` bilan bugundan 30 kun keyingi sanani hisobla.
11. `strptime` bilan `"2026-03-15"` matnini sanaga aylantirib, hafta kunini (`%A`) chiqar.
12. `statistics` bilan baholar ro'yxatining o'rtacha va medianasini chiqar.
13. `Counter` bilan matndagi eng ko'p uchragan 3 ta so'zni top.
14. `random.sample` bilan 1–49 dan 6 ta takrorlanmas tasodifiy son tanla (lotereya).

**Murakkab (15–20):**

15. `Counter` bilan ikki ro'yxatning umumiy elementlarini chastotasi bilan top (`&` ishlat).
16. Tug'ilgan kuninggacha necha kun qolganini hisobla (`date` va `timedelta`).
17. `defaultdict` bilan jumladagi har bir harf bilan boshlanadigan so'zlarni guruhla.
18. Oddiy "tanga tashlash" simulyatsiyasi: `random` bilan 1000 marta tashlab, "orol"/"yozuv" nisbatini chiqar.
19. `datetime` bilan ikki sana orasidagi farqni kun, hafta ko'rinishida chiqar.
20. So'zlar ro'yxatining chastota tahlili: `Counter` bilan hisobla, eng ko'p va eng kam uchraganini top, va natijani chiroyli jadval ko'rinishida chiqar.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
from collections import Counter
print(Counter("banana"))      # Counter({'a': 3, 'n': 2, 'b': 1})

# 2
print(Counter([1, 2, 2, 3, 3, 3]).most_common(1))   # [(3, 3)]

# 3
from datetime import datetime
print(datetime.now().strftime("%d.%m.%Y"))

# 4
import random
print([random.randint(1, 100) for _ in range(5)])

# 5
import math
print(math.sqrt(144), math.factorial(5))   # 12.0 120

# 6
import random
print(random.choice(["olma", "banan", "uzum"]))

# 7
import random
sonlar = [1, 2, 3, 4, 5]
random.shuffle(sonlar)
print(sonlar)

# 8
from collections import defaultdict
chastota = defaultdict(int)
for soz in ["non", "suv", "non", "non", "suv"]:
    chastota[soz] += 1
print(dict(chastota))         # {'non': 3, 'suv': 2}

# 9
from collections import defaultdict
guruh = defaultdict(list)
for ism, sinf in [("Ali", "A"), ("Vali", "B"), ("Gul", "A")]:
    guruh[sinf].append(ism)
print(dict(guruh))            # {'A': ['Ali', 'Gul'], 'B': ['Vali']}

# 10
from datetime import date, timedelta
print(date.today() + timedelta(days=30))

# 11
from datetime import datetime
d = datetime.strptime("2026-03-15", "%Y-%m-%d")
print(d.strftime("%A"))       # Sunday

# 12
import statistics
baholar = [85, 90, 78, 92, 88]
print(statistics.mean(baholar), statistics.median(baholar))

# 13
from collections import Counter
matn = "olma non olma suv non olma"
print(Counter(matn.split()).most_common(3))

# 14
import random
print(random.sample(range(1, 50), 6))

# 15
from collections import Counter
a = Counter([1, 2, 2, 3])
b = Counter([2, 3, 3, 4])
print(a & b)                  # Counter({2: 1, 3: 1})

# 16
from datetime import date
bugun = date.today()
tugilgan = date(bugun.year, 12, 31)   # masalan 31-dekabr
if tugilgan < bugun:
    tugilgan = date(bugun.year + 1, 12, 31)
print((tugilgan - bugun).days, "kun qoldi")

# 17
from collections import defaultdict
jumla = "olma anor banan behi olcha"
guruh = defaultdict(list)
for soz in jumla.split():
    guruh[soz[0]].append(soz)
print(dict(guruh))

# 18
import random
orol = 0
for _ in range(1000):
    if random.choice(["orol", "yozuv"]) == "orol":
        orol += 1
print(f"Orol: {orol}, Yozuv: {1000 - orol}")

# 19
from datetime import date
d1 = date(2026, 1, 1)
d2 = date(2026, 12, 31)
farq = (d2 - d1).days
print(f"{farq} kun = {farq // 7} hafta {farq % 7} kun")

# 20
from collections import Counter
sozlar = "olma non olma suv non olma choy".split()
hisob = Counter(sozlar)
print("Eng ko'p:", hisob.most_common(1)[0])
print("Eng kam:", hisob.most_common()[-1])
for soz, son in hisob.most_common():
    print(f"{soz:<6} {'*' * son}")
```

</details>

---

[← Tip ko'rsatmalari](./10-typing-functional.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Parallel ishlash →](./12-concurrency-async.md)
