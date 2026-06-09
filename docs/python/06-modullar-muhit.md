# 06 — Modullar va muhit

Dasturlaring kattalashganda, butun kodni bitta faylga yozish noqulay bo'lib qoladi. Python kodni **modullar**ga (alohida fayllarga) bo'lish va boshqalar yozgan tayyor kutubxonalardan foydalanish imkonini beradi. Bu modulda kodni qanday bo'lish, tashqi kutubxonalarni o'rnatish va loyihalarni toza saqlashni o'rganasan.

> **Bu modulda:** `import`, standart kutubxonadan foydalanish, o'z modulingni yozish, `if __name__ == "__main__"`, `pip` bilan kutubxona o'rnatish, va virtual muhit (venv).

---

## 6.1 Modul nima? `import`

Modul — bu Python kodi bo'lgan `.py` fayl. Boshqa fayldagi kodni `import` orqali olib ishlatasan. Python o'zida ko'plab tayyor modullar bilan keladi (standart kutubxona).

`import` qilganingda Python modulni qator joylardan ma'lum tartib bilan qidiradi — quyidagi diagramma shu jarayonni ko'rsatadi:

![import qanday topadi: Python sys.modules keshini, so'ng sys.path papkalarini tartib bilan qidiradi](rasmlar/py06-import-qidiruv.svg)

```python
import math                  # butun modulni import qilish

print(math.sqrt(16))         # 4.0    — modul nomi.funksiya
print(math.pi)               # 3.14159...
```

Faqat kerakli qismini olish (`from`):

```python
from math import sqrt, pi    # faqat sqrt va pi

print(sqrt(25))              # 5.0   — endi math. yozish shart emas
print(pi)
```

Modulga qisqa nom berish (`as`):

```python
import random as r           # random ni r deb chaqiramiz

print(r.randint(1, 6))       # 1..6 oralig'ida tasodifiy son
```

Bir nechta foydali standart modul:

```python
import math       # matematik funksiyalar (sqrt, ceil, floor, pi...)
import random     # tasodifiy sonlar va tanlovlar
import datetime    # sana va vaqt
```

```python
import random
print(random.choice(["olma", "banan", "uzum"]))   # tasodifiy bittasi
print(random.randint(1, 100))                       # 1..100 tasodifiy
```

---

## 6.2 O'z modulingni yozish

Har qanday `.py` fayl — modul. Masalan `hisob.py` faylini yarat:

```python
# hisob.py
def qosh(a, b):
    return a + b

def kop(a, b):
    return a * b

PI = 3.14159
```

Boshqa fayldan (masalan `main.py`) uni import qilasan:

```python
# main.py  (hisob.py bilan bir papkada)
import hisob

print(hisob.qosh(3, 5))      # 8
print(hisob.PI)              # 3.14159

# yoki:
from hisob import qosh
print(qosh(10, 20))          # 30
```

> Bu kodni tartibli saqlashning asosiy yo'li: bog'liq funksiyalarni alohida modullarga ajratasan (masalan `hisob.py`, `fayllar.py`, `foydalanuvchi.py`), keyin `main.py` da birlashtirasan.

Loyiha o'sganda bog'liq modullarni bitta papkaga — **paket**ga — guruhlaysan. Papka `__init__.py` faylini olganida paketga aylanadi va ichidagi modullarga nuqta bilan murojaat qilasan:

![Paket strukturasi: papka __init__.py fayli orqali paketga aylanadi, modullarga paket.modul nuqta sintaksisi bilan murojaat qilinadi](rasmlar/py06-paket-struktura.svg)

---

## 6.3 `if __name__ == "__main__":`

Bu satrni Python fayllarida tez-tez ko'rasan. Uning ma'nosi: **"agar bu fayl to'g'ridan-to'g'ri ishga tushirilsa"** (import qilinmasa).

```python
# hisob.py
def qosh(a, b):
    return a + b

if __name__ == "__main__":
    # bu blok faqat 'python hisob.py' deganda ishlaydi,
    # 'import hisob' qilinganda ishlamaydi
    print("Test:", qosh(2, 3))
```

> **Nega kerak?** Modulingni boshqa joydan import qilganda, undagi test/namoyish kodi avtomatik ishlab ketmasligi uchun. Funksiyalar import qilinadi, lekin `if __name__ == "__main__":` ichidagi kod faqat fayl o'zi ishga tushirilganda bajariladi. Hozircha "fayl bevosita ishga tushganda ishlaydigan kod" deb tushun.

---

## 6.4 `pip` — tashqi kutubxonalarni o'rnatish

Standart kutubxonadan tashqari, jamoa yozgan minglab kutubxonalar bor (internetda, PyPI omborida). Ularni `pip` bilan o'rnatasan (terminalda):

```bash
pip install requests       # 'requests' kutubxonasini o'rnatadi (internet so'rovlari uchun)
pip install rich           # chiroyli terminal chiqishi uchun
```

O'rnatilgandan keyin koddan ishlatasan:

```python
import requests            # endi import qilish mumkin
```

Foydali buyruqlar:

```bash
pip list                   # o'rnatilgan kutubxonalar ro'yxati
pip install --upgrade requests   # yangilash
pip uninstall requests     # o'chirish
```

---

## 6.5 Virtual muhit (venv) — loyihalarni ajratish

Har loyihaning o'z kutubxonalar to'plami bo'lishi kerak. Aks holda turli loyihalar bir-biriga xalaqit beradi (biriga kerakli versiya boshqasini buzishi mumkin). **Virtual muhit (venv)** — har loyiha uchun alohida, izolyatsiyalangan Python muhiti.

```bash
# 1. Virtual muhit yaratish (loyiha papkasida):
python -m venv venv

# 2. Uni faollashtirish:
#    Linux / macOS:
source venv/bin/activate
#    Windows:
venv\Scripts\activate

# 3. Endi pip install shu muhitga o'rnatadi (tizimga emas):
pip install requests

# 4. Ishni tugatib, chiqish:
deactivate
```

Faollashtirilganda terminalda `(venv)` belgisi paydo bo'ladi — demak izolyatsiyalangan muhitdasan.

> **Nega muhim?** Tasavvur qil: A loyihaga kutubxonaning 1-versiyasi, B loyihaga 2-versiyasi kerak. Virtual muhitsiz ular to'qnashadi. Har loyihaga alohida venv — har birida kerakli versiya. Bu professional amaliyot, har doim ishlat.

Quyidagi diagramma venv'siz to'qnashuv va venv bilan izolyatsiya o'rtasidagi farqni ko'rsatadi:

![venv izolatsiyasi: venv'siz loyihalar bitta umumiy kutubxonani baham ko'rib to'qnashadi, venv bilan har loyiha o'z muhitida alohida versiyani saqlaydi](rasmlar/py06-venv-izolatsiya.svg)

---

## 6.6 `requirements.txt` — loyiha bog'liqliklari

Loyihangda qaysi kutubxonalar kerakligini bitta faylda saqlaysan — `requirements.txt`. Shunda boshqa odam (yoki sen boshqa kompyuterda) hammasini bir buyruq bilan o'rnatadi:

```bash
# Joriy kutubxonalarni faylga yozish:
pip freeze > requirements.txt

# Boshqa joyda hammasini o'rnatish:
pip install -r requirements.txt
```

`requirements.txt` taxminan shunday ko'rinadi:

```
requests==2.31.0
rich==13.7.0
```

> Loyihangni GitHub'ga qo'yganingda `requirements.txt` ni ham qo'sh — shunda boshqalar loyihangni oson ishga tushiradi. `venv/` papkasini esa qo'shma (u katta va har kompyuterda qayta yaratiladi).

---

## ✍️ Masalalar (20 ta)

> Ba'zi masalalar terminalda buyruq bajarishni talab qiladi. Modul yozish masalalarida ikkita fayl yaratib sina.

**Oson (1–7):**

1. `math` modulini import qilib, 144 ning kvadrat ildizini chiqar.
2. `random` modulidan `randint` bilan 1–6 oralig'ida tasodifiy son chiqar (zar tashlash).
3. `from math import pi` qilib, radiusi 5 bo'lgan doira yuzasini hisobla.
4. `random.choice` bilan ro'yxatdan tasodifiy element tanla.
5. `import random as r` qilib, `r.randint` bilan 3 ta tasodifiy son chiqar.
6. Terminalda `pip list` ni ishga tushirib, o'rnatilgan kutubxonalarni ko'r (kod emas, terminal).
7. `math.ceil` va `math.floor` bilan `4.3` ni yuqoriga va pastga yaxlitla.

**O'rta (8–14):**

8. `hisob.py` moduli yarat (`qosh`, `ayir` funksiyalari bilan), uni `main.py` dan import qilib ishlat.
9. `salom.py` modul yarat (`salomlash(ism)` funksiyasi), boshqa fayldan `from salom import salomlash` qilib chaqir.
10. `hisob.py` ga `if __name__ == "__main__":` qo'shib, ichida test kodi yoz. Faylni to'g'ridan-to'g'ri ishga tushirib tekshir.
11. `random.shuffle` bilan `[1,2,3,4,5]` ro'yxatini aralashtir.
12. `datetime` modulidan foydalanib, bugungi sanani chiqar (`datetime.date.today()`).
13. Terminalda virtual muhit yarat (`python -m venv venv`) va faollashtir.
14. Virtual muhitda biror kutubxona o'rnat (`pip install rich`) va `pip list` bilan tekshir.

**Murakkab (15–20):**

15. Ikkita modul yarat: `geometriya.py` (`doira_yuza`, `tortburchak_yuza`) va `main.py` (ularni import qilib ishlatadi).
16. `random` bilan oddiy "son top" o'yini: kompyuter 1–100 oralig'ida son o'ylasin, foydalanuvchi topguncha "katta"/"kichik" deb yo'naltir.
17. `utils.py` moduli yarat: kamida 3 ta foydali funksiya (masalan `katta_harf`, `teskari`, `unli_sanash`), `main.py` dan hammasini ishlat.
18. Loyiha yarat: virtual muhit, `requirements.txt`, va `pip freeze` bilan uni to'ldir.
19. `random` va `math` ni birga ishlatib: 5 ta tasodifiy sonning kvadrat ildizlari yig'indisini hisobla.
20. Ikki moduldan iborat kichik loyiha: `bank.py` (`Hisob` klassi — 5-moduldan) va `main.py` (hisob yaratib, amallar bajaradi). Klassni modulga joylashtirib, import qilib ishlat.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
import math
print(math.sqrt(144))         # 12.0

# 2
import random
print(random.randint(1, 6))

# 3
from math import pi
print(pi * 5 ** 2)            # 78.539...

# 4
import random
print(random.choice(["olma", "banan", "uzum"]))

# 5
import random as r
print(r.randint(1, 100), r.randint(1, 100), r.randint(1, 100))

# 6
# Terminalda:  pip list

# 7
import math
print(math.ceil(4.3), math.floor(4.3))    # 5 4

# 8
# hisob.py:
#   def qosh(a, b): return a + b
#   def ayir(a, b): return a - b
# main.py:
import hisob
print(hisob.qosh(3, 5))       # 8
print(hisob.ayir(10, 4))      # 6

# 9
# salom.py:
#   def salomlash(ism): print(f"Salom, {ism}!")
# main.py:
from salom import salomlash
salomlash("Aziz")             # Salom, Aziz!

# 10
# hisob.py:
def qosh(a, b):
    return a + b
if __name__ == "__main__":
    print("Test:", qosh(2, 3))    # faqat 'python hisob.py' deganda chiqadi

# 11
import random
sonlar = [1, 2, 3, 4, 5]
random.shuffle(sonlar)
print(sonlar)                 # masalan [3, 1, 5, 2, 4]

# 12
import datetime
print(datetime.date.today())  # masalan 2026-06-09

# 13
# Terminalda:
#   python -m venv venv
#   source venv/bin/activate     (Windows: venv\Scripts\activate)

# 14
# Terminalda (venv faol):
#   pip install rich
#   pip list

# 15
# geometriya.py:
#   def doira_yuza(r): return 3.14159 * r * r
#   def tortburchak_yuza(a, b): return a * b
# main.py:
import geometriya
print(geometriya.doira_yuza(5))
print(geometriya.tortburchak_yuza(4, 6))

# 16
import random
maxfiy = random.randint(1, 100)
while True:
    taxmin = int(input("Taxminingiz (1-100): "))
    if taxmin == maxfiy:
        print("Topdingiz!")
        break
    elif taxmin < maxfiy:
        print("Kattaroq son")
    else:
        print("Kichikroq son")

# 17
# utils.py:
#   def katta_harf(s): return s.upper()
#   def teskari(s): return s[::-1]
#   def unli_sanash(s): return sum(1 for h in s.lower() if h in "aeiou")
# main.py:
from utils import katta_harf, teskari, unli_sanash
print(katta_harf("salom"))    # SALOM
print(teskari("salom"))       # molas
print(unli_sanash("salom"))   # 2

# 18
# Terminalda:
#   python -m venv venv
#   source venv/bin/activate
#   pip install requests
#   pip freeze > requirements.txt

# 19
import random, math
sonlar = [random.randint(1, 100) for _ in range(5)]
print(sum(math.sqrt(s) for s in sonlar))

# 20
# bank.py:
#   class Hisob:
#       def __init__(self, balans=0): self.balans = balans
#       def qoy(self, s): self.balans += s
#       def yech(self, s): self.balans -= s
# main.py:
from bank import Hisob
h = Hisob(1000)
h.qoy(500)
h.yech(200)
print(h.balans)               # 1300
```

</details>

---

[← OOP](./05-oop.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Xatolarni boshqarish →](./07-xatolar-context.md)
