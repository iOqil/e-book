# 12 — Parallel ishlash va `asyncio`

Hozirgacha dasturlarimiz **ketma-ket** ishladi: bir ish tugaguncha keyingisi kutadi. Lekin ba'zan bir nechta ishni **bir vaqtda** qilish kerak — masalan, 100 ta internet sahifani yuklab olishda har birini navbatma-navbat kutish sekin. Bu modulda bir vaqtda bir nechta ishni boshqarishni o'rganasan. Bu mavzu biroz murakkab — tushunchalar darajasida, sodda misollar bilan ko'ramiz.

> **Bu modulda:** parallel ishlash nima, threadlar (I/O kutish uchun), GIL tushunchasi, va `asyncio` (`async`/`await`) asoslari.

---

## 12.1 Nega parallel ishlash kerak?

Ishlar ikki xil bo'ladi:

- **Kutish ishi (I/O)** — internet so'rovi, fayl o'qish, baza so'rovi. Dastur ko'p vaqtni shunchaki **kutib** o'tkazadi.
- **Hisob ishi (CPU)** — og'ir matematik hisob-kitob. Protsessor band bo'ladi.

Kutish ishida parallellik juda foydali: bitta so'rovni kutib turganda, boshqasini boshlash mumkin. Misol uchun, 3 ta sahifani har biri 2 soniyada yuklasa — ketma-ket 6 soniya, parallel esa ~2 soniya.

---

## 12.2 Threadlar — bir vaqtda bir nechta ish

`threading` moduli bir nechta ishni "bir vaqtda" boshqarish imkonini beradi (ayniqsa kutish ishlarida foydali):

```python
import threading
import time

def yuklab_ol(nom):
    print(f"{nom} boshlandi")
    time.sleep(2)             # kutishni taqlid qiladi (masalan internet)
    print(f"{nom} tugadi")

# Uchta ishni parallel boshlash:
threadlar = []
for nom in ["A", "B", "C"]:
    t = threading.Thread(target=yuklab_ol, args=(nom,))
    threadlar.append(t)
    t.start()                 # boshlanadi

for t in threadlar:
    t.join()                  # hammasi tugashini kutamiz

# Ketma-ket bo'lsa 6 soniya, threadlar bilan ~2 soniya
```

---

## 12.3 GIL — Python'ning muhim xususiyati

Python'da bir muhim qoida bor: **GIL** (Global Interpreter Lock). Soddaroq aytganda — Python'da bir vaqtda faqat **bitta** thread haqiqiy hisob-kitob qiladi.

Bundan kelib chiqadigan oddiy qoida:

| Ish turi | Misol | Threadlar yordam beradimi? |
|----------|-------|----------------------------|
| **Kutish (I/O)** | internet, fayl, baza | ✅ Ha — kutishda boshqa thread ishlaydi |
| **Hisob (CPU)** | og'ir matematika | ❌ Yo'q — GIL tufayli navbatga turadi |

> Ya'ni: agar dasturing ko'p **kutsa** (internet/fayl) — threadlar tezlashtiradi. Agar ko'p **hisoblasa** (matematika) — threadlar yordam bermaydi (buning uchun alohida usul, `multiprocessing`, bor, lekin u ilg'orroq mavzu). Hozircha shu qoidani bilib qo'y.

Quyidagi diagramma GIL qulfi qanday ishlashini ko'rsatadi — bir vaqtda faqat bitta thread Python bytecode bajaradi:

![GIL: bir vaqtda faqat bitta thread Python bytecode bajaradi](rasmlar/py12-gil.svg)

---

## 12.4 `asyncio` — minglab kutish ishini boshqarish

`asyncio` — ayniqsa ko'p sonli kutish ishlari (masalan minglab internet so'rovi) uchun zamonaviy usul. `async def` bilan maxsus funksiya yozasan, `await` bilan "kutilayotgan" joyda boshqarivni bo'shatasan:

```python
import asyncio

async def yuklab_ol(nom):
    print(f"{nom} boshlandi")
    await asyncio.sleep(2)        # NOMBLOCKING kutish (time.sleep emas!)
    print(f"{nom} tugadi")
    return f"{nom} natijasi"

async def main():
    # gather — bir nechta ishni BIR VAQTDA boshlaydi:
    natijalar = await asyncio.gather(
        yuklab_ol("A"),
        yuklab_ol("B"),
        yuklab_ol("C"),
    )
    print(natijalar)              # ~2 soniyada hammasi (6 emas)

asyncio.run(main())               # async dasturni shunday ishga tushirasan
```

> **Eng ko'p uchraydigan xato:** `async` funksiya ichida oddiy `time.sleep()` ishlatish — u hammasini bloklaydi. `asyncio.sleep()` ishlat. Async kodda kutish uchun maxsus, "nomblocking" funksiyalar bo'ladi.

Mana `asyncio` qanday ishlaydi: `await` ga yetganda coroutine boshqaruvni **event loop**'ga qaytaradi, loop esa kutib turgan boshqa coroutine ishini boshlaydi (hammasi bitta thread'da):

![asyncio event loop: await boshqaruvni qaytaradi, loop boshqa ishni boshlaydi](rasmlar/py12-event-loop.svg)

---

## 12.5 Qaysi usulni qachon ishlataman?

Sodda yo'riqnoma:

```
Bitta ish, parallel kerak emas?
  → oddiy ketma-ket kod (murakkablashtirma!)

Bir nechta kutish ishi (internet/fayl)?
  → threading (oson) yoki asyncio (ko'p son uchun samarali)

Og'ir hisob-kitob?
  → multiprocessing (ilg'or mavzu, keyinroq)
```

`threading` va `asyncio` ikkalasi ham kutish (I/O) ishlari uchun, lekin ishlash modeli farq qiladi — threadlarda bir nechta OS thread bo'ladi, `asyncio`da esa bitta thread ichida event loop navbatlashtiradi:

![Threadlar va asyncio farqi: ko'p OS thread vs bitta threadda event loop](rasmlar/py12-thread-vs-async.svg)

> **Eng muhim maslahat:** parallellik kodni murakkablashtiradi va yangi xatolar (masalan bir vaqtda bir ma'lumotni o'zgartirish) keltiradi. Faqat **haqiqatan kerak bo'lganda** ishlat. Avvalo oddiy ketma-ket kod yoz — sekin bo'lsa, keyin optimallashtir.

---

## ✍️ Masalalar (20 ta)

> Bu mavzu murakkab — masalalar asosan tushunish va oddiy misollar uchun.

**Oson (1–7):**

1. Bitta `async def salom()` yoz: "salom" chop etsin. `asyncio.run` bilan ishga tushir.
2. `await asyncio.sleep(1)` bilan 1 soniya kutib, keyin xabar chiqaruvchi coroutine yoz.
3. `threading.Thread` bilan bitta funksiyani ishga tushir (ichida `time.sleep(1)`).
4. GIL nima ekanini o'z so'zlaring bilan (kod izohi sifatida) yoz.
5. Kutish ishi (I/O) va hisob ishi (CPU) farqini misol bilan izohda yoz.
6. `asyncio.gather` bilan ikkita oddiy coroutine'ni birga ishga tushir.
7. `threading.Thread` bilan ikkita funksiyani parallel boshla (`start` + `join`).

**O'rta (8–14):**

8. `asyncio.gather` bilan 3 ta coroutine'ni birga ishga tushir, har biri turli muddat uxlasin.
9. Async funksiya yoz: parametr sifatida nom va kutish vaqtini olsin, kutgach nomni qaytarsin.
10. 3 ta thread'ni ro'yxatda yaratib, hammasini `start` qil, keyin `join` bilan kut.
11. Async coroutine natijasini `await` bilan olib, o'zgaruvchiga saqlab chiqar.
12. `time.sleep` (oddiy) va `asyncio.sleep` (async) farqini izohda tushuntir.
13. `asyncio.gather` natijasini ro'yxatga olib, har birini chiqar.
14. Bir vaqtda 5 ta "yuklab olish"ni (har biri `asyncio.sleep`) ishga tushirib, umumiy vaqtni `time` bilan o'lcha.

**Murakkab (15–20):**

15. Ketma-ket va parallel (gather bilan) bajarishni taqqosla: 3 ta 1-soniyalik ishni ikki usulda bajarib, vaqtlarini chiqar.
16. Async funksiyalar zanjiri: bittasi natija qaytarsin, ikkinchisi shu natijani ishlatsin (`await` bilan).
17. `threading` bilan umumiy hisoblagichni bir nechta thread'dan oshir; natija to'g'ri chiqishini kuzat (bu yerda `Lock` kerakligini izohda ayt).
18. `asyncio.gather` bilan 10 ta ishni parallel bajar, har biri o'z nomini va natijasini qaytarsin.
19. Oddiy "yuklab oluvchi" simulyator: nomlar ro'yxatini async tarzda "yuklab ol" (har biri tasodifiy vaqt uxlasin, `asyncio.sleep` + `random`).
20. Threadli va asyncioli variantni yonma-yon yozib, qaysi qaysi holatda mosligini izohda tushuntir (kutish vs hisob).

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
import asyncio
import threading
import time

# 1
async def salom():
    print("salom")
asyncio.run(salom())

# 2
async def kut():
    await asyncio.sleep(1)
    print("1 soniya o'tdi")
asyncio.run(kut())

# 3
def ish():
    time.sleep(1)
    print("ish tugadi")
t = threading.Thread(target=ish)
t.start(); t.join()

# 4
# GIL: Python'da bir vaqtda faqat bitta thread haqiqiy hisob-kitob qiladi.
# Shuning uchun og'ir CPU ishida threadlar tezlashtirmaydi,
# lekin kutish (I/O) ishida foydali — kutishda boshqa thread ishlay oladi.

# 5
# I/O ishi: internet so'rovi, fayl o'qish — dastur ko'p kutadi.
# CPU ishi: katta matematik hisob — protsessor band bo'ladi.
# Parallellik I/O da ko'proq foyda beradi.

# 6
async def a():
    await asyncio.sleep(0.5); return "a"
async def b():
    await asyncio.sleep(0.5); return "b"
async def m6():
    print(await asyncio.gather(a(), b()))
asyncio.run(m6())

# 7
def ish2(nom):
    time.sleep(1)
    print(f"{nom} tugadi")
t1 = threading.Thread(target=ish2, args=("A",))
t2 = threading.Thread(target=ish2, args=("B",))
t1.start(); t2.start(); t1.join(); t2.join()

# 8
async def uxla(nom, sek):
    await asyncio.sleep(sek)
    return f"{nom}: {sek}s"
async def m8():
    print(await asyncio.gather(uxla("A", 1), uxla("B", 0.5), uxla("C", 0.2)))
asyncio.run(m8())

# 9
async def yuklab(nom, vaqt):
    await asyncio.sleep(vaqt)
    return nom
async def m9():
    print(await yuklab("Sahifa", 0.3))
asyncio.run(m9())

# 10
def ish3(nom):
    time.sleep(0.5)
    print(nom)
threadlar = [threading.Thread(target=ish3, args=(f"T{i}",)) for i in range(3)]
for t in threadlar: t.start()
for t in threadlar: t.join()

# 11
async def hisob():
    await asyncio.sleep(0.2)
    return 42
async def m11():
    natija = await hisob()
    print("Natija:", natija)
asyncio.run(m11())

# 12
# time.sleep — butun dasturni (yoki event loop'ni) bloklaydi.
# asyncio.sleep — faqat shu coroutine'ni "uxlatadi", boshqalar ishlay beradi.
# Async kodda DOIM asyncio.sleep ishlat.

# 13
async def m13():
    natijalar = await asyncio.gather(*[uxla(f"ish{i}", 0.1) for i in range(3)])
    for n in natijalar:
        print(n)
asyncio.run(m13())

# 14
async def m14():
    b = time.perf_counter()
    await asyncio.gather(*[asyncio.sleep(1) for _ in range(5)])
    print(f"5 ta ish: {time.perf_counter() - b:.2f}s")   # ~1s (parallel)
asyncio.run(m14())

# 15
async def bir_ish():
    await asyncio.sleep(1)
async def m15():
    # ketma-ket:
    b = time.perf_counter()
    for _ in range(3):
        await bir_ish()
    print(f"ketma-ket: {time.perf_counter() - b:.2f}s")   # ~3s
    # parallel:
    b = time.perf_counter()
    await asyncio.gather(bir_ish(), bir_ish(), bir_ish())
    print(f"parallel: {time.perf_counter() - b:.2f}s")     # ~1s
asyncio.run(m15())

# 16
async def birinchi():
    await asyncio.sleep(0.2)
    return 10
async def ikkinchi(x):
    await asyncio.sleep(0.2)
    return x * 2
async def m16():
    a = await birinchi()
    b = await ikkinchi(a)
    print(b)                  # 20
asyncio.run(m16())

# 17
hisoblagich = 0
lock = threading.Lock()
def oshir():
    global hisoblagich
    for _ in range(10000):
        with lock:            # Lock — bir vaqtda faqat bitta thread o'zgartirsin
            hisoblagich += 1
ts = [threading.Thread(target=oshir) for _ in range(3)]
for t in ts: t.start()
for t in ts: t.join()
print(hisoblagich)            # 30000  (Lock'siz kamroq chiqishi mumkin edi)

# 18
async def vazifa(i):
    await asyncio.sleep(0.1)
    return f"ish{i} tayyor"
async def m18():
    natijalar = await asyncio.gather(*[vazifa(i) for i in range(10)])
    print(natijalar)
asyncio.run(m18())

# 19
import random
async def yuklab_ol(nom):
    await asyncio.sleep(random.uniform(0.1, 0.5))
    return f"{nom} yuklandi"
async def m19():
    nomlar = ["sahifa1", "sahifa2", "sahifa3"]
    print(await asyncio.gather(*[yuklab_ol(n) for n in nomlar]))
asyncio.run(m19())

# 20
# threading — oddiy kod bilan, kam sonli kutish ishlari uchun qulay.
# asyncio — ko'p sonli kutish ishlari (minglab so'rov) uchun samarali.
# Ikkalasi ham KUTISH (I/O) uchun. Og'ir HISOB uchun multiprocessing kerak.
```

</details>

---

[← Standart kutubxona](./11-standart-kutubxona.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Testlash →](./13-testlash.md)
