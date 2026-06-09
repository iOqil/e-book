# 09 — Generatorlar va dekoratorlar

Bu modul Python'ning kuchliroq vositalariga kirish. **Generatorlar** — katta yoki cheksiz ketma-ketliklarni xotirani tejab ishlatish usuli. **Dekoratorlar** — funksiyaning xulqini o'zgartirmasdan unga qo'shimcha imkoniyat qo'shish vositasi. Bular boshida biroz murakkab tuyuladi — sekin, misol bilan o'rganamiz.

> **Bu modulda:** generatorlar (`yield`), generator ifodalari, closure (yopilma), va dekoratorlar.

---

## 9.1 Generator nima? `yield`

Oddiy funksiya `return` bilan **bitta** qiymat qaytaradi va tugaydi. **Generator** esa `yield` bilan qiymatlarni **birma-bir**, kerak bo'lganda beradi — hammasini birdaniga xotiraga olmaydi.

```python
def sanagich(n):
    for i in range(n):
        yield i              # return emas — yield: qiymatni "berib", to'xtab turadi

for son in sanagich(5):
    print(son)               # 0, 1, 2, 3, 4
```

**Nega foydali?** Tasavvur qil, 1 milliard sonni qayta ishlash kerak. Oddiy ro'yxat hammasini xotiraga oladi (juda ko'p joy egallaydi). Generator esa har safar bittasini beradi — xotira deyarli ishlatilmaydi:

```python
# Ro'yxat — hammasini xotiraga oladi:
sonlar = [i * i for i in range(1000000)]   # ko'p xotira

# Generator — bittadan beradi, xotira tejaladi:
sonlar = (i * i for i in range(1000000))   # ( ) — generator ifodasi
for s in sonlar:
    ...                                     # har safar bittasi
```

> **Eslab qol:** generator "dangasa" (lazy) — qiymatni faqat **so'ralganda** hisoblaydi. Cheksiz ketma-ketliklar bilan ham ishlay oladi (chunki hammasini bir vaqtda yaratmaydi).

Quyidagi diagrammada ro'yxat (hammasini birdaniga xotiraga oladi) va generator (`yield` bilan to'xtab-to'xtab, bittadan beradi) yonma-yon taqqoslangan:

![Generator (lazy, bittadan beradi) va ro'yxat (eager, hammasi xotirada) taqqosi](rasmlar/py09-generator-vs-list.svg)

Generator ifodasi — list comprehension'ga o'xshaydi, lekin `[ ]` o'rniga `( )`:

```python
kvadratlar = (x * x for x in range(5))     # generator
print(sum(kvadratlar))                      # 30  — yig'indi, oraliq ro'yxatsiz
```

---

## 9.2 Closure (yopilma) — funksiya qaytaruvchi funksiya

Funksiya ichida boshqa funksiya yaratib, uni qaytarish mumkin. Ichki funksiya tashqi funksiyaning o'zgaruvchilarini "eslab qoladi" — bu **closure**:

```python
def kopaytiruvchi(n):
    def kopaytir(x):
        return x * n         # tashqi 'n' ni eslab qoladi
    return kopaytir          # funksiyaning O'ZINI qaytaramiz (chaqirmasdan)

ikki = kopaytiruvchi(2)      # n=2 bo'lgan funksiya
uch = kopaytiruvchi(3)       # n=3 bo'lgan funksiya

print(ikki(10))              # 20
print(uch(10))              # 30
```

> Bu boshida g'alati tuyuladi: funksiya **qiymat** emas, **boshqa funksiya** qaytaradi. Closure dekoratorlarni tushunish uchun zarur — keyingi bo'limga poydevor.

Quyidagi diagrammada ichki funksiya tashqi `n` ni qanday "eslab qolishi" va har bir chaqiruv o'z `n` ini olib yurishi ko'rsatilgan:

![Closure: ichki funksiya tashqi o'zgaruvchini eslab qoladi](rasmlar/py09-closure.svg)

---

## 9.3 Dekoratorlar — funksiyaga qo'shimcha imkoniyat qo'shish

Dekorator — bir funksiyani "o'rab", unga qo'shimcha xulq qo'shadigan funksiya. Masalan, funksiya ishlashidan oldin/keyin biror narsa qilish (log yozish, vaqt o'lchash) — asl funksiyani o'zgartirmasdan.

Avval dekoratorning "ichini" ko'ramiz:

```python
def log_qiluvchi(funk):
    def ichki(*args, **kwargs):
        print(f"{funk.__name__} chaqirilmoqda...")
        natija = funk(*args, **kwargs)       # asl funksiyani chaqiramiz
        print(f"{funk.__name__} tugadi")
        return natija
    return ichki

def salomla(ism):
    print(f"Salom, {ism}!")

salomla = log_qiluvchi(salomla)      # funksiyani "o'radik"
salomla("Aziz")
# Chiqish:
#   salomla chaqirilmoqda...
#   Salom, Aziz!
#   salomla tugadi
```

`@` belgisi — xuddi shu ishning qisqa yozuvi:

```python
def log_qiluvchi(funk):
    def ichki(*args, **kwargs):
        print(f"{funk.__name__} chaqirilmoqda...")
        natija = funk(*args, **kwargs)
        print(f"{funk.__name__} tugadi")
        return natija
    return ichki

@log_qiluvchi                  # = salomla = log_qiluvchi(salomla)
def salomla(ism):
    print(f"Salom, {ism}!")

salomla("Aziz")                # avtomatik o'ralgan holda ishlaydi
```

Quyidagi diagrammada dekorator asl funksiyani qanday o'rab, wrapper (ichki funksiya) orqali unga qo'shimcha xulq qo'shishi bosqichma-bosqich ko'rsatilgan:

![Dekorator: funksiya -> wrapper -> qo'shimcha xulq qo'shilgan funksiya](rasmlar/py09-decorator.svg)

> **`*args, **kwargs` nima?** Bular dekorator har qanday funksiyani (qanday argument olsa ham) o'rashi uchun. `*args` — barcha oddiy argumentlar, `**kwargs` — barcha nomli argumentlar. Hozircha "har qanday argumentni qabul qiladi" deb tushun.

Amaliy misol — vaqt o'lchovchi dekorator:

```python
import time

def vaqt_olchash(funk):
    def ichki(*args, **kwargs):
        boshlanish = time.perf_counter()
        natija = funk(*args, **kwargs)
        davomiylik = time.perf_counter() - boshlanish
        print(f"{funk.__name__}: {davomiylik:.4f} soniya")
        return natija
    return ichki

@vaqt_olchash
def sekin_ish():
    time.sleep(1)

sekin_ish()      # sekin_ish: 1.0001 soniya
```

---

## 9.4 Tayyor foydali dekoratorlar

Python o'zida foydali dekoratorlar bilan keladi. Eng mashhuri — `lru_cache` (natijani eslab qolib, takror hisoblamaydi):

```python
from functools import lru_cache

@lru_cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))       # tez ishlaydi — keshlangani uchun
# lru_cache'siz fib(50) juda sekin bo'lardi (bir xil hisob takrorlanardi)
```

> Hozircha dekoratorlarni faqat "ishlatish" darajasida bilsang yetadi (`@lru_cache` kabi tayyorlarni). O'z dekoratoringni yozish — yuqorida ko'rgan namuna bo'yicha, vaqt o'tib mashq qilasan.

---

## ✍️ Masalalar (20 ta)

> Bu masalalar oldingi modullarga (ayniqsa funksiyalar va sikllarga) tayanadi.

**Oson (1–7):**

1. `sanagich(n)` generatorini yoz: 0 dan n gacha sonlarni `yield` qilsin. `for` bilan chiqar.
2. `list()` bilan generator natijasini ro'yxatga aylantir: `list(sanagich(5))`.
3. Generator ifodasi `(x*2 for x in range(5))` yarat va `for` bilan chiqar.
4. `sum()` ni generator ifodasi bilan ishlat: 1 dan 100 gacha sonlar yig'indisi.
5. `kvadratlar(n)` generatorini yoz: 0 dan n gacha sonlarning kvadratlarini bersin.
6. `kopaytiruvchi(n)` closure yoz (n ga ko'paytiruvchi funksiya qaytarsin). `ikki = kopaytiruvchi(2)` qilib ishlat.
7. `@lru_cache` ishlatib rekursiv funksiya yoz (masalan faktorial yoki Fibonachchi).

**O'rta (8–14):**

8. Juft sonlarni beruvchi generator yoz: `juftlar(n)` — 0 dan n gacha faqat juftlarni `yield` qilsin.
9. Closure yoz: `qoshuvchi(n)` — `n` ni qo'shuvchi funksiya qaytarsin (`besh = qoshuvchi(5)`, `besh(10)` → 15).
10. Oddiy dekorator yoz: `@salom` — funksiya chaqirilishidan oldin "Salom!" deb chiqarsin.
11. Funksiya nomini chop etuvchi dekorator yoz (`funk.__name__` ishlat).
12. Vaqt o'lchovchi dekorator yoz (`time.perf_counter`), uni biror funksiyaga qo'lla.
13. Generator yoz: berilgan ro'yxatdan faqat musbat sonlarni `yield` qilsin.
14. `@lru_cache` bilan va usiz Fibonachchi yozib, tezligini taqqosla (`time` bilan).

**Murakkab (15–20):**

15. Cheksiz generator yoz: `sanoq(boshlanish)` — to'xtamasdan sonlarni `yield` qilsin. `for` + `break` bilan birinchi 5 tasini ol.
16. Dekorator yoz: funksiya nechi marta chaqirilganini sanasin va har chaqiruvda chop etsin.
17. Natijani 2 ga ko'paytiruvchi dekorator yoz: o'ralgan funksiya nima qaytarsa, uni 2 ga ko'paytirib qaytarsin.
18. Generator yoz: matndagi har bir so'zni bittadan `yield` qilsin (`split` + `yield`).
19. Dekorator yoz: funksiya xato bersa, uni ushlab "Xato yuz berdi" deb chiqarsin (funksiya qulamasin) — `try/except` ni dekorator ichida ishlat.
20. "Faqat musbat" dekoratori yoz: funksiyaga uzatilgan barcha sonlar musbat bo'lishini tekshirsin; biror salbiy bo'lsa `ValueError` chaqirsin, aks holda funksiyani normal ishlatsin.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
def sanagich(n):
    for i in range(n):
        yield i
for s in sanagich(5):
    print(s)                  # 0,1,2,3,4

# 2
print(list(sanagich(5)))      # [0, 1, 2, 3, 4]

# 3
for x in (x * 2 for x in range(5)):
    print(x)                  # 0,2,4,6,8

# 4
print(sum(x for x in range(1, 101)))    # 5050

# 5
def kvadratlar(n):
    for i in range(n):
        yield i * i
print(list(kvadratlar(5)))    # [0, 1, 4, 9, 16]

# 6
def kopaytiruvchi(n):
    def kopaytir(x):
        return x * n
    return kopaytir
ikki = kopaytiruvchi(2)
print(ikki(10))               # 20

# 7
from functools import lru_cache
@lru_cache
def fakt(n):
    return 1 if n <= 1 else n * fakt(n - 1)
print(fakt(10))               # 3628800

# 8
def juftlar(n):
    for i in range(n):
        if i % 2 == 0:
            yield i
print(list(juftlar(10)))      # [0, 2, 4, 6, 8]

# 9
def qoshuvchi(n):
    def qosh(x):
        return x + n
    return qosh
besh = qoshuvchi(5)
print(besh(10))               # 15

# 10
def salom(funk):
    def ichki(*args, **kwargs):
        print("Salom!")
        return funk(*args, **kwargs)
    return ichki
@salom
def ish():
    print("Ish bajarildi")
ish()                         # Salom! / Ish bajarildi

# 11
def nom_chop(funk):
    def ichki(*args, **kwargs):
        print(f"Chaqirilmoqda: {funk.__name__}")
        return funk(*args, **kwargs)
    return ichki
@nom_chop
def hisob():
    return 42
print(hisob())

# 12
import time
def vaqt_olchash(funk):
    def ichki(*args, **kwargs):
        b = time.perf_counter()
        n = funk(*args, **kwargs)
        print(f"{funk.__name__}: {time.perf_counter() - b:.4f}s")
        return n
    return ichki
@vaqt_olchash
def sekin():
    time.sleep(0.5)
sekin()

# 13
def musbatlar(royxat):
    for s in royxat:
        if s > 0:
            yield s
print(list(musbatlar([-2, 3, -1, 5, 0, 8])))   # [3, 5, 8]

# 14
import time
from functools import lru_cache
def fib1(n):
    return n if n < 2 else fib1(n - 1) + fib1(n - 2)
@lru_cache
def fib2(n):
    return n if n < 2 else fib2(n - 1) + fib2(n - 2)
b = time.perf_counter(); fib1(30); print("keshsiz:", round(time.perf_counter() - b, 3))
b = time.perf_counter(); fib2(30); print("keshli:", round(time.perf_counter() - b, 6))

# 15
def sanoq(boshlanish):
    son = boshlanish
    while True:
        yield son
        son += 1
natija = []
for s in sanoq(10):
    if len(natija) >= 5:
        break
    natija.append(s)
print(natija)                 # [10, 11, 12, 13, 14]

# 16
def sanagich_dek(funk):
    funk.soni = 0
    def ichki(*args, **kwargs):
        funk.soni += 1
        print(f"{funk.soni}-marta chaqirildi")
        return funk(*args, **kwargs)
    return ichki
@sanagich_dek
def salom():
    pass
salom(); salom()              # 1-marta / 2-marta

# 17
def ikki_barobar(funk):
    def ichki(*args, **kwargs):
        return funk(*args, **kwargs) * 2
    return ichki
@ikki_barobar
def qosh(a, b):
    return a + b
print(qosh(3, 4))             # 14  ((3+4)*2)

# 18
def sozlar(matn):
    for soz in matn.split():
        yield soz
print(list(sozlar("Python juda zor")))   # ['Python', 'juda', 'zor']

# 19
def xatoni_ushla(funk):
    def ichki(*args, **kwargs):
        try:
            return funk(*args, **kwargs)
        except Exception:
            print("Xato yuz berdi")
    return ichki
@xatoni_ushla
def bol(a, b):
    return a / b
print(bol(10, 2))             # 5.0
bol(10, 0)                    # Xato yuz berdi

# 20
def faqat_musbat(funk):
    def ichki(*args, **kwargs):
        for a in args:
            if isinstance(a, (int, float)) and a < 0:
                raise ValueError("Faqat musbat sonlar")
        return funk(*args, **kwargs)
    return ichki
@faqat_musbat
def qosh(a, b):
    return a + b
print(qosh(2, 3))             # 5
try:
    qosh(2, -1)
except ValueError as e:
    print(e)                  # Faqat musbat sonlar
```

</details>

---

[← Fayllar, JSON, CSV](./08-fayl-malumot.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Tip ko'rsatmalari →](./10-typing-functional.md)
