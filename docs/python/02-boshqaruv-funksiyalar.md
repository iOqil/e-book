# 02 — Boshqaruv va funksiyalar

Hozirgacha kod yuqoridan pastga, har bir qator ketma-ket bajarilardi. Endi dasturlashning yuragini o'rganamiz: **shartga qarab qaror qabul qilish** (`if`) va **takrorlash** (`for`, `while`). Shundan keyin o'z **funksiyalaring**ni yozasan.

> **Bu modulda:** if/elif/else bilan tanlash, for va while sikllari, break/continue, va funksiyalar yaratish.

---

## 2.1 Bloklar va bo'sh joy (indentatsiya)

1-modulda aytib o'tgandik: Python'da kod **bloklari** chap tomondagi bo'sh joy (indentatsiya) bilan ajraladi. Endi buni amalda ko'ramiz.

Blok — bir guruh qator bo'lib, ular birga bajariladi. Blok ochilishidan oldin `:` (ikki nuqta) qo'yiladi, blok ichidagi qatorlar esa **4 ta bo'sh joy** bilan suriladi:

```python
yosh = 20

if yosh >= 18:
    print("Voyaga yetgan")      # 4 ta bo'sh joy — bu qator if blokiga tegishli
    print("Ovoz berishi mumkin")  # bu ham if blokida
print("Bu qator har doim bajariladi")   # surilmagan — blokdan tashqarida
```

> **Qoidalar:**
> - Blok ichi aniq **4 ta bo'sh joy** bilan suriladi (Tab tugmasi emas — ko'pchilik muharrirlar Tab'ni 4 bo'sh joyga aylantiradi).
> - Noto'g'ri bo'sh joy → `IndentationError` xatosi.
> - Bu Python qoidasi, xohish emas. Lekin foydasi bor: kod doim toza va bir xil ko'rinadi.

---

## 2.2 `if` / `elif` / `else` — qaror qabul qilish

`if` — "agar" degani. Shart `True` bo'lsa, blok bajariladi:

```python
yosh = 20

if yosh >= 18:
    print("Kirishingiz mumkin")
```

`else` — "aks holda". Shart bajarilmasa, `else` bloki ishlaydi:

```python
yosh = 15

if yosh >= 18:
    print("Kirishingiz mumkin")
else:
    print("Kirish mumkin emas")     # shu chiqadi
```

`elif` ("aks holda agar") — bir nechta shartni ketma-ket tekshirish uchun:

```python
ball = 75

if ball >= 90:
    print("A'lo")
elif ball >= 70:
    print("Yaxshi")           # shu chiqadi (75 >= 70)
elif ball >= 60:
    print("Qoniqarli")
else:
    print("Qoniqarsiz")
```

> Python yuqoridan pastga tekshiradi va **birinchi to'g'ri** shartda to'xtaydi. Qolganlariga qaramaydi. Shuning uchun shartlar tartibi muhim.

Quyidagi blok-sxema shartlarning yuqoridan pastga qanday tekshirilishini ko'rsatadi:

![if/elif/else qaror oqimi blok-sxemasi](rasmlar/py02-if-elif-else.svg)

Shartlarni `and`, `or`, `not` bilan birlashtirish (1-modulda ko'rgan edik):

```python
yosh = 25
chipta = True

if yosh >= 18 and chipta:
    print("Konsertga kirishingiz mumkin")
```

---

## 2.3 `for` sikli — ketma-ketlik bo'ylab takrorlash

`for` sikli biror ketma-ketlik (sonlar, ro'yxat, matn...) bo'ylab harakatlanib, har bir element uchun blokni bajaradi.

**`range()` bilan sonlar bo'ylab:**

```python
for i in range(5):       # 0, 1, 2, 3, 4  (5 ning O'ZI kirmaydi!)
    print(i)
```

`range()` ning shakllari:

```python
range(5)         # 0, 1, 2, 3, 4
range(1, 6)      # 1, 2, 3, 4, 5     (1 dan boshlab, 6 gacha lekin 6 kirmaydi)
range(0, 10, 2)  # 0, 2, 4, 6, 8     (2 qadam bilan)
```

**Matn yoki ro'yxat bo'ylab** (ro'yxatni 3-modulda batafsil ko'rasan):

```python
for harf in "salom":
    print(harf)          # s, a, l, o, m  — har harf alohida qatorda

mevalar = ["olma", "banan", "uzum"]
for meva in mevalar:
    print(meva)
```

> `for i in range(n)` — "n marta takrorla" degani. `i` har aylanishda navbatdagi qiymatni oladi. O'zgaruvchi nomini ixtiyoriy tanlaysan (`i`, `son`, `harf`...).

---

## 2.4 `while` sikli — shart bajarilguncha takrorlash

`while` — shart `True` bo'lib turguncha takrorlaydi:

```python
son = 1
while son <= 5:
    print(son)
    son = son + 1        # MUHIM: shartni o'zgartirmasang, sikl cheksiz bo'ladi!
```

> **Diqqat — cheksiz sikl:** agar shart hech qachon `False` bo'lmasa, dastur to'xtamay qoladi. Yuqoridagi misolda `son = son + 1` bo'lmasa, `son` doim 1 bo'lib qoladi va sikl tugamaydi. Har `while` da shartni o'zgartirayotganingni tekshir.

`for` qancha marta takrorlashni oldindan bilganda, `while` esa "qachongacha"ni bilmaganda qulay (masalan, foydalanuvchi to'g'ri javob berguncha).

Quyidagi sxema ikki siklning oqimini yonma-yon solishtiradi:

![for va while sikllarining oqimi](rasmlar/py02-for-vs-while.svg)

---

## 2.5 `break` va `continue`

Sikl ichida oqimni boshqarish:

```python
# break — siklni butunlay to'xtatadi
for i in range(10):
    if i == 5:
        break            # 5 ga yetganda chiqadi
    print(i)             # 0, 1, 2, 3, 4

# continue — shu aylanishni o'tkazib, keyingisiga o'tadi
for i in range(5):
    if i == 2:
        continue         # 2 ni o'tkazib yuboradi
    print(i)             # 0, 1, 3, 4
```

---

## 2.6 Funksiyalar — kodni qayta ishlatish

Funksiya — bir vazifani bajaradigan, nom berilgan kod bo'lagi. Bir marta yozasan, keyin xohlagancha chaqirasan. Bu takrorni kamaytiradi va kodni tartibli qiladi.

```python
def salomlash():               # def bilan e'lon qilinadi
    print("Salom!")
    print("Xush kelibsiz!")

salomlash()                    # funksiyani chaqirish — kod shu yerda bajariladi
salomlash()                    # yana bir marta
```

**Parametrlar** — funksiyaga ma'lumot uzatish:

```python
def salomlash(ism):            # ism — parametr
    print(f"Salom, {ism}!")

salomlash("Aziz")              # Salom, Aziz!
salomlash("Malika")            # Salom, Malika!
```

**`return`** — funksiyadan natija qaytarish:

```python
def qosh(a: int, b: int) -> int:   # type hint: a, b — int, natija ham int
    return a + b               # natijani qaytaradi

natija = qosh(3, 5)            # natija = 8
print(natija)                  # 8
print(qosh(10, 20))            # 30
```

> **Type hint (tur ko'rsatkichi)** — `a: int`, `-> int` kabi belgilar. Bular Python'ni majburlamaydi (xato bermaydi), lekin kodni o'qiganga "bu yerga int kutilyapti" deb aytadi va muharrirlar yordamida xatolarni oldindan tutadi. Zamonaviy Python kodida ular standart hisoblanadi — shu kitobda ham asta-sekin ko'proq ishlatamiz.

> **`print` va `return` farqi** — yangi boshlovchilar buni tez chalkashtiradi:
> - `print` — qiymatni **ekranga ko'rsatadi**, lekin qaytarmaydi.
> - `return` — qiymatni **qaytaradi**, uni o'zgaruvchiga saqlab, keyin ishlatish mumkin.
>
> Hisob-kitob qiluvchi funksiyalar odatda `return` ishlatadi, shunda natijani keyinroq foydalanasan.

Quyidagi sxema argument parametrga qanday kirib, `return` natijani qanday qaytarishini, hamda ko'p argument uchun `*args`/`**kwargs`ni ko'rsatadi:

![Funksiya chaqiruvi: argument kiradi, return chiqadi, *args/**kwargs](rasmlar/py02-funksiya-chaqiruvi.svg)

Funksiya ichida biror nomni ishlatganingda, Python uni qaysi tartibda qidiradi? Quyidagi sxema **LEGB** qoidasini ko'rsatadi — Python nomni Local -> Enclosing -> Global -> Built-in tartibida, ichkaridan tashqariga qarab qidiradi va birinchi topilgan joyda to'xtaydi:

![LEGB scope: Local, Enclosing, Global, Built-in qidirish tartibi](rasmlar/py02-legb-scope.svg)

---

## 2.7 Standart parametr qiymatlari

Parametrga oldindan qiymat berib qo'yish mumkin — chaqirilganda berilmasa, shu ishlatiladi:

```python
def salomlash(ism, salom="Salom"):
    print(f"{salom}, {ism}!")

salomlash("Aziz")                  # Salom, Aziz!     (standart ishlatildi)
salomlash("Aziz", "Assalomu alaykum")   # Assalomu alaykum, Aziz!
```

> Standart qiymatli parametrlar funksiyani moslashuvchan qiladi: ko'p hollarda standart yetadi, kerak bo'lganda boshqasini berasan.

---

## 2.8 `*args` — ixtiyoriy ko'p pozitsion argument

Ba'zan funksiya nechta argument olishini oldindan bilmaymiz. Masalan, "bir nechta sonni qo'sh" funksiyasi 2 ta ham, 5 ta ham son qabul qilishi kerak. Mana shu yerda `*args` yordamga keladi.

Parametr nomi oldiga `*` qo'ysang, Python berilgan barcha qolgan **pozitsion argumentlarni** bitta `tuple`ga (to'plamga) yig'adi:

```python
def yigindi(*sonlar: int) -> int:
    jami = 0
    for s in sonlar:        # sonlar — tuple, ustidan aylanamiz
        jami += s
    return jami

print(yigindi(1, 2, 3))            # 6
print(yigindi(10, 20, 30, 40))     # 100
print(yigindi())                   # 0  — hech narsa berilmasa, bo'sh tuple
```

> `args` shunchaki kelishilgan nom (arguments — argumentlar). Asosiy "sehr" — `*` belgisi. Istasang `*sonlar`, `*qiymatlar` deb ham nomlashing mumkin, lekin an'anaviy nom — `*args`.

Funksiya ichida `args` oddiy `tuple` bo'ladi, demak uzunligini `len()` bilan, elementlarini indeks bilan olasan:

```python
def ortacha(*sonlar: float) -> float:
    if not sonlar:               # bo'sh bo'lsa, nolga bo'lishdan saqlanamiz
        return 0.0
    return sum(sonlar) / len(sonlar)

print(ortacha(10, 20, 30))       # 20.0
print(ortacha(5))                # 5.0
print(ortacha())                 # 0.0
```

---

## 2.9 `**kwargs` — ixtiyoriy ko'p nomli argument

`*args` pozitsion (nomsiz) argumentlarni yig'sa, `**kwargs` esa **nom=qiymat** ko'rinishidagi argumentlarni bitta `dict`ga (lug'atga) yig'adi. Ikkita yulduzcha (`**`) ishlatiladi:

```python
def malumot(**maydonlar) -> None:
    for kalit, qiymat in maydonlar.items():    # maydonlar — dict
        print(f"{kalit} = {qiymat}")

malumot(ism="Aziz", yosh=25, shahar="Toshkent")
# ism = Aziz
# yosh = 25
# shahar = Toshkent
```

`kwargs` ham kelishilgan nom (keyword arguments). Asosiysi — `**`.

`*args` va `**kwargs`ni birga ishlatish mumkin. **Tartib qat'iy**: avval oddiy parametrlar, keyin `*args`, oxirida `**kwargs`:

```python
def hodisa(nom: str, *qatnashchilar, **tafsilotlar) -> None:
    print(f"Hodisa: {nom}")
    print("Qatnashchilar:", qatnashchilar)   # tuple
    print("Tafsilotlar:", tafsilotlar)       # dict

hodisa("Tug'ilgan kun", "Aziz", "Malika", joy="Park", soat=18)
# Hodisa: Tug'ilgan kun
# Qatnashchilar: ('Aziz', 'Malika')
# Tafsilotlar: {'joy': 'Park', 'soat': 18}
```

---

## 2.10 Paketlash va yoyish (`*` va `**` chaqiruvda)

Yuqorida `*` va `**` ni **funksiya ta'rifida** ko'rdik — u yerda ular argumentlarni **paketlaydi** (yig'adi). Endi **chaqiruvda** ishlatsak, aksincha — tayyor ro'yxat yoki lug'atni **yoyadi** (ochib yuboradi):

```python
def yigindi(*sonlar: int) -> int:
    return sum(sonlar)

raqamlar = [1, 2, 3, 4]
print(yigindi(*raqamlar))      # yigindi(1, 2, 3, 4) bilan bir xil → 10
```

Bu yerda `*raqamlar` ro'yxatni alohida argumentlarga **yoyib** beradi. Xuddi shunday, `**` lug'atni `nom=qiymat` argumentlariga yoyadi:

```python
def profil(ism: str, yosh: int, shahar: str) -> None:
    print(f"{ism}, {yosh} yosh, {shahar}")

malumotlar = {"ism": "Olim", "yosh": 30, "shahar": "Samarqand"}
profil(**malumotlar)           # profil(ism="Olim", yosh=30, shahar="Samarqand")
# Olim, 30 yosh, Samarqand
```

> Eslab qol: `*`/`**` **ta'rifda** — paketlash (ko'p argumentni bitta to'plamga yig'ish), **chaqiruvda** — yoyish (bitta to'plamni alohida argumentlarga ochish). Bir xil belgi, joyiga qarab teskari ish bajaradi.

---

## 2.11 Pozitsion-only (`/`) va keyword-only (`*`) parametrlar

Python parametrlarni **qanday uzatish mumkinligini** boshqarish imkonini beradi. Buning uchun parametrlar ro'yxatida maxsus belgilar ishlatamiz.

**Keyword-only (`*` dan keyingilar)** — `*` belgisidan keyingi parametrlarni faqat `nom=qiymat` ko'rinishida uzatish mumkin, pozitsion (tartib bo'yicha) emas. Bu chaqiruvni o'qiluvchan qiladi:

```python
def hisob(narx: float, *, soliq: float = 0.12, chegirma: float = 0.0) -> float:
    return narx * (1 + soliq) * (1 - chegirma)

print(hisob(100))                            # 112.00000000000001 (float aniqligi — 1-bobni eslang; round() kerak)
print(hisob(100, soliq=0.20, chegirma=0.1))  # 108.0 (bu yerda aniq chiqdi)
# hisob(100, 0.20)  -> XATO! soliq pozitsion uzatib bo'lmaydi
```

Bu yerda `*` o'zi parametr emas — u shunchaki "bundan keyingilari faqat nom bilan" degan chegara. Foydasi: `hisob(100, 0.20, 0.1)` kabi tushunarsiz chaqiruvni taqiqlaydi — har bir qiymat nima ekani aniq bo'ladi.

**Pozitsion-only (`/` dan oldingilar)** — `/` belgisidan oldingi parametrlarni faqat tartib bo'yicha uzatish mumkin, `nom=` bilan emas:

```python
def bolish(a: float, b: float, /) -> float:
    return a / b

print(bolish(10, 2))      # 5.0
# bolish(a=10, b=2)  -> XATO! a va b pozitsion-only
```

Ikkalasini bitta funksiyada birlashtirish ham mumkin — bu Python'ning o'rnatilgan funksiyalarida (masalan `len`, `range`) ham qo'llaniladi:

```python
def royxat_yasa(element, /, royxat: list, *, takror: int = 1) -> list:
    # element — faqat pozitsion, takror — faqat keyword, royxat — ikkalasi ham
    return royxat + [element] * takror

print(royxat_yasa(5, [1, 2], takror=3))   # [1, 2, 5, 5, 5]
```

> Boshlovchi sifatida bularni har doim ishlatishing shart emas, lekin kutubxonalarda tez-tez uchraydi — bilib qo'ygan foydali.

---

## 2.12 `for-else` va `while-else` — sikl `break`'siz tugaganda

Python'da sikllarga ham `else` qo'shish mumkin — bu boshqa tillarda kam uchraydigan, ammo juda qulay imkoniyat. `else` bloki sikl **`break`'siz, oxirigacha tugaganda** bajariladi. Agar sikl `break` bilan to'xtatilsa, `else` **bajarilmaydi**.

Buni "izlash" masalalarida o'qib qarash kerak: "agar hech nima topilmasa (break bo'lmasa)...":

```python
son = 13
for i in range(2, son):
    if son % i == 0:                          # bo'luvchi topildi
        print(f"{son} tub emas ({i} ga bo'linadi)")
        break
else:                                          # break bo'lmadi = bo'luvchi yo'q
    print(f"{son} — tub son")
# 13 — tub son
```

Bu aynan **tub son** tekshiruvi uchun ideal. Yuqorida `15` bersak:

```python
son = 15
for i in range(2, son):
    if son % i == 0:
        print(f"{son} tub emas ({i} ga bo'linadi)")
        break
else:
    print(f"{son} — tub son")
# 15 tub emas (3 ga bo'linadi)
```

Endi bu naqshni funksiyaga solib, berilgan chegaragacha barcha tub sonlarni topamiz:

```python
def tub_sonlar(chegara: int) -> list[int]:
    natija: list[int] = []
    for son in range(2, chegara + 1):
        for bolovchi in range(2, int(son ** 0.5) + 1):
            if son % bolovchi == 0:
                break
        else:                       # ichki sikl break'siz tugadi → tub
            natija.append(son)
    return natija

print(tub_sonlar(30))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

`while-else` ham xuddi shunday ishlaydi — `else` shart `False` bo'lib sikl o'z-o'zidan tugaganda bajariladi, `break` bilan emas:

```python
urinish = 0
while urinish < 3:
    parol = input("Parol: ")
    urinish += 1
    if parol == "python123":
        print("Kirildi")
        break
else:
    print("Urinishlar tugadi, hisob bloklandi")
```

> Yodda tut: sikl `else`si "**break bo'lmadi**" degani, "shart noto'g'ri bo'ldi" degani EMAS. Aynan break bilan bog'lab o'yla.

---

## 2.13 `match` / `case` — strukturaviy moslik

`if/elif/else` zanjiri uzayib ketganda, Python 3.10 dan boshlab `match`/`case` (PEP 634) ko'proq o'qiluvchan muqobil beradi. U bir qiymatni bir nechta **naqsh (pattern)** bilan solishtiradi va birinchi mosini bajaradi.

**Eng oddiy shakl — literal moslik.** Bu kalkulyator masalasining (16-masala) zamonaviy ko'rinishi:

```python
def kalkulyator(a: float, b: float, amal: str) -> float | str:
    match amal:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            if b == 0:
                return "Nolga bo'lib bo'lmaydi"
            return a / b
        case _:                       # _ — "boshqa har qanday holat" (default)
            return "Noma'lum amal"

print(kalkulyator(10, 3, "+"))    # 13
print(kalkulyator(10, 0, "/"))    # Nolga bo'lib bo'lmaydi
print(kalkulyator(10, 3, "%"))    # Noma'lum amal
```

`_` (pastki chiziq) — maxsus naqsh: u **hamma narsaga** mos keladi va `else` vazifasini bajaradi. Doim oxiriga qo'yiladi.

**Bir nechta variant — `|` bilan:**

```python
def javob(buyruq: str) -> str:
    match buyruq:
        case "salom" | "hi" | "hello":    # uchtasidan biri bo'lsa
            return "Salom!"
        case "xayr" | "bye":
            return "Ko'rishguncha!"
        case _:
            return "Tushunmadim"

print(javob("hi"))      # Salom!
print(javob("bye"))     # Ko'rishguncha!
```

**Sequence (ketma-ketlik) naqshi** — `match` tuple/ro'yxatni "ochib", qismlarini o'zgaruvchilarga ajratib oladi:

```python
def nuqta_tahlil(nuqta: tuple[int, int]) -> str:
    match nuqta:
        case (0, 0):
            return "Markaz (boshlanish nuqtasi)"
        case (0, y):                      # birinchisi 0, ikkinchisini y ga ol
            return f"Y o'qida, y={y}"
        case (x, 0):
            return f"X o'qida, x={x}"
        case (x, y):
            return f"Nuqta ({x}, {y})"
        case _:
            return "Noma'lum"

print(nuqta_tahlil((0, 0)))   # Markaz (boshlanish nuqtasi)
print(nuqta_tahlil((0, 5)))   # Y o'qida, y=5
print(nuqta_tahlil((3, 4)))   # Nuqta (3, 4)
```

**Dict (lug'at) naqshi** — kerakli kalitlar borligini tekshirib, qiymatlarini ajratadi:

```python
def buyurtma(data: dict) -> str:
    match data:
        case {"tur": "pizza", "olcham": olcham}:
            return f"Pizza, o'lchami: {olcham}"
        case {"tur": "ichimlik"}:
            return "Ichimlik"
        case _:
            return "Noma'lum buyurtma"

print(buyurtma({"tur": "pizza", "olcham": "katta"}))   # Pizza, o'lchami: katta
print(buyurtma({"tur": "ichimlik", "hajm": "0.5l"}))   # Ichimlik
```

**Guard (qo'shimcha shart) — `if` bilan.** Naqshdan keyin `if` qo'yib, qo'shimcha shart qo'shasan:

```python
def yosh_guruh(yosh: int) -> str:
    match yosh:
        case n if n < 0:
            return "Xato: manfiy yosh"
        case n if n < 13:
            return "Bola"
        case n if n < 18:
            return "O'smir"
        case _:
            return "Katta yoshli"

print(yosh_guruh(10))   # Bola
print(yosh_guruh(16))   # O'smir
print(yosh_guruh(25))   # Katta yoshli
```

> `match`/`case` `if/elif` o'rnini bosish uchun **majburiy** emas. Lekin ko'p variantli tanlovda, ayniqsa tuple/dict/obyekt ichini "ochib" ko'rganda — kod ancha tiniq bo'ladi.

---

## 2.14 O'zgaruvchi ko'rinish doirasi: `global` va `nonlocal`

2.6-bo'limdagi **LEGB** sxemasini eslaylik: Python nomni Local → Enclosing → Global → Built-in tartibida qidiradi. Odatda funksiya ichida tashqi o'zgaruvchini **o'qish** mumkin, lekin **o'zgartirish** uchun maxsus kalit so'z kerak.

**`global`** — funksiya ichidan **global** (modul darajasidagi) o'zgaruvchini o'zgartirish uchun:

```python
hisoblagich = 0

def oshir() -> None:
    global hisoblagich        # tashqi global o'zgaruvchiga ishora
    hisoblagich += 1

oshir()
oshir()
print(hisoblagich)            # 2
```

`global hisoblagich` bo'lmasa, `hisoblagich += 1` qatori `UnboundLocalError` xatosini bergan bo'lardi — Python uni yangi lokal o'zgaruvchi deb o'ylaydi.

**`nonlocal`** — ichki (uyalangan) funksiyadan **tashqaridagi funksiya** o'zgaruvchisini o'zgartirish uchun. Bu **closure** (yopilma) — ichki funksiya tashqi muhitni "eslab qoladi":

```python
def sanagich_yasa():
    son = 0                   # tashqi funksiya o'zgaruvchisi
    def ichki() -> int:
        nonlocal son          # son — yangi lokal emas, tashqaridagi
        son += 1
        return son
    return ichki              # funksiyaning O'ZINI qaytaramiz

sanagich = sanagich_yasa()
print(sanagich())             # 1
print(sanagich())             # 2
print(sanagich())             # 3  — har chaqiruvda holatini eslab qoladi
```

> Maslahat: `global`ni imkon qadar kam ishlat — u kodni murakkablashtiradi. Ko'pincha qiymatni `return` qilib, natijani qabul qilish toza yechim. `nonlocal` esa closure naqshida o'rinli.

---

## 2.15 Tuzoq: o'zgaruvchan standart argument (mutable default)

Bu — Python'dagi eng mashhur "tuzoq" (gotcha). Standart qiymat sifatida `[]` yoki `{}` kabi **o'zgaruvchan** (mutable) obyekt ishlatsang, kutilmagan xatti-harakat olasan.

Sababi: standart qiymat funksiya **e'lon qilinganda bir marta** yaratiladi, har chaqiruvda emas. Demak barcha chaqiruvlar **bir xil ro'yxatni** baham ko'radi:

```python
def qoshish_xato(element, royxat=[]):    # XATO: standart [] bir marta yaraladi
    royxat.append(element)
    return royxat

print(qoshish_xato(1))    # [1]
print(qoshish_xato(2))    # [1, 2]      — kutilmagan! oldingisi qoldi
print(qoshish_xato(3))    # [1, 2, 3]   — ro'yxat to'planib boryapti
```

**To'g'ri yechim** — standart qiymat `None` qil, funksiya ichida tekshirib, yangi ro'yxat yarat:

```python
def qoshish_togri(element, royxat: list | None = None) -> list:
    if royxat is None:
        royxat = []           # har chaqiruvda YANGI ro'yxat
    royxat.append(element)
    return royxat

print(qoshish_togri(1))   # [1]
print(qoshish_togri(2))   # [2]    — endi har safar toza boshlaydi
print(qoshish_togri(3))   # [3]
```

> Qoida: standart argument sifatida **hech qachon** o'zgaruvchan obyekt (`list`, `dict`, `set`) ishlatma. `None` ishlat, ichida tekshirib yarat. Bu professional Python kodida qat'iy amal qilinadigan qoida.

---

## 2.16 `return`'siz funksiya `None` qaytaradi

Agar funksiyada `return` bo'lmasa yoki `return` qiymatsiz yozilsa, funksiya avtomatik ravishda `None` qaytaradi. `None` — Python'da "hech narsa / qiymat yo'q" degani:

```python
def salomlash(ism: str) -> None:     # -> None: ataylab hech narsa qaytarmaydi
    print(f"Salom, {ism}!")

natija = salomlash("Aziz")     # Salom, Aziz!  (print ishladi)
print(natija)                  # None
print(type(natija))            # <class 'NoneType'>
```

Bu juda muhim, chunki ko'p boshlovchi `print` qilgan funksiyani `return` qilgan deb o'ylab, natijasini ishlatmoqchi bo'ladi va `None` bilan xatoga uchraydi.

Yana bir nozik holat: agar `return` faqat `if` ichida bo'lsa, shart bajarilmaganda funksiya `None` qaytaradi:

```python
def juft_qaytar(n: int) -> bool | None:
    if n % 2 == 0:
        return True
    # toq son uchun return yo'q → None qaytadi

print(juft_qaytar(4))    # True
print(juft_qaytar(3))    # None  — toq son, return ishlamadi
```

> `-> None` type hint funksiya ataylab qiymat qaytarmasligini bildiradi (masalan, faqat ekranga chiqaradi yoki obyektni o'zgartiradi). Bu kodni o'qiyotgan odamga niyatingni aniq ko'rsatadi.

---

## ✍️ Masalalar (26 ta)

> Bu masalalar shu modul va 1-modul mavzulariga asoslangan. Yechimga qaramasdan ishlashga harakat qil.

**Oson (1–7):**

1. Foydalanuvchidan son so'ra. Agar musbat bo'lsa "musbat", aks holda "musbat emas" deb chiqar.
2. Foydalanuvchidan yoshini so'ra. 18 dan katta yoki teng bo'lsa "voyaga yetgan", aks holda "voyaga yetmagan" deb yoz.
3. `for` sikli bilan 1 dan 10 gacha sonlarni chiqar.
4. `for` va `range` bilan 1 dan 10 gacha **juft** sonlarni chiqar (maslahat: `range(2, 11, 2)`).
5. `while` sikli bilan 5 dan 1 gacha teskari sanab chiqar.
6. `salom()` nomli funksiya yoz — chaqirilganda "Salom, dunyo!" chiqarsin. Uni 3 marta chaqir.
7. Ikkita sonni qabul qilib, ularning ko'paytmasini **qaytaradigan** (`return`) funksiya yoz.

**O'rta (8–14):**

8. Foydalanuvchidan ball so'ra (0–100). `if/elif/else` bilan baho qo'y: 90+ → "A'lo", 70+ → "Yaxshi", 60+ → "Qoniqarli", aks holda "Qoniqarsiz".
9. `for` sikli bilan 1 dan 100 gacha sonlarning yig'indisini hisobla va chiqar.
10. Foydalanuvchidan son so'ra, uning ko'paytuv jadvalini (1 dan 9 gacha) chiqar (`for` bilan, masalan `7 x 1 = 7`).
11. `while` sikli bilan foydalanuvchi "stop" deb yozguncha har safar undan biror so'z so'rab, uni qaytarib chiqar.
12. Sonni qabul qilib, juft yoki toq ekanini **qaytaradigan** funksiya yoz (maslahat: `%` ishlat, natija matn bo'lsin).
13. `for` va `break` bilan 1 dan boshlab sonlarni chiqar, lekin son 7 ga yetganda to'xta.
14. `for` va `continue` bilan 1 dan 10 gacha sonlarni chiqar, lekin 5 ni o'tkazib yubor.

**Murakkab (15–20):**

15. Foydalanuvchidan son so'rab, u **tub son** (faqat 1 va o'ziga bo'linadigan) ekanini tekshiruvchi dastur yoz (maslahat: `for` bilan 2 dan son-1 gacha bo'linishini tekshir).
16. Ikkita sonni va amalni (`+`, `-`, `*`, `/`) qabul qiladigan oddiy kalkulyator funksiya yoz (`if/elif` bilan amalni tanla, natijani `return` qil).
17. `for` sikli bilan 1 dan 50 gacha sonlardan faqat 3 ga **ham**, 5 ga **ham** bo'linadiganlarini chiqar.
18. Foydalanuvchidan parol so'ra. To'g'ri parol (`"python123"`) kiritilmaguncha `while` bilan qayta-qayta so'ra. To'g'ri bo'lganda "Kirish muvaffaqiyatli" deb yoz.
19. Berilgan son uchun **faktorial** hisoblaydigan funksiya yoz (`n!` = 1×2×...×n; masalan `5! = 120`). `for` yoki `while` bilan.
20. 1 dan 100 gacha "FizzBuzz" o'yini: 3 ga bo'linsa "Fizz", 5 ga bo'linsa "Buzz", ikkalasiga bo'linsa "FizzBuzz", aks holda sonning o'zini chiqar.

**Qo'shimcha — yangi mavzular (21–26):**

21. `*args` ishlatib, ixtiyoriy sondagi sonlarning **o'rtacha** qiymatini qaytaradigan funksiya yoz. Hech narsa berilmasa `0.0` qaytarsin.
22. 16-masaladagi kalkulyatorni `match`/`case` bilan qayta yoz. `/` da nolga bo'linishni va noma'lum amalni alohida ushlab, mos matn qaytar.
23. Tub son tekshiruvini `for-else` bilan yoz: ichki sikl `break`'siz tugasa son tub, `else` blokida `True` qaytar (maslahat: `range(2, int(n**0.5)+1)`).
24. `hisobvaraq(ism, *, balans=0.0, valyuta="USD")` funksiyasini yoz — `balans` va `valyuta` faqat `nom=qiymat` bilan uzatiladigan (keyword-only) bo'lsin. Ikki xil chaqiruv bilan sina.
25. "Tuzoqli" funksiyani tuzat: `def savatga_qosh(mahsulot, savat=[])` o'rniga `None` standartli to'g'ri versiyani yoz, ketma-ket chaqirganda ro'yxat to'planib qolmasligini ko'rsat.
26. `match`/`case` va `dataclass` bilan: `Doira(radius)` va `Tortburchak(eni, boyi)` shakllarining **yuza**sini hisoblaydigan funksiya yoz (class pattern ishlat).

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
son = int(input("Son: "))
if son > 0:
    print("musbat")
else:
    print("musbat emas")

# 2
yosh = int(input("Yosh: "))
if yosh >= 18:
    print("voyaga yetgan")
else:
    print("voyaga yetmagan")

# 3
for i in range(1, 11):
    print(i)

# 4
for i in range(2, 11, 2):
    print(i)

# 5
son = 5
while son >= 1:
    print(son)
    son = son - 1

# 6
def salom():
    print("Salom, dunyo!")
salom()
salom()
salom()

# 7
def kopaytir(a, b):
    return a * b
print(kopaytir(4, 5))     # 20

# 8
ball = int(input("Ball: "))
if ball >= 90:
    print("A'lo")
elif ball >= 70:
    print("Yaxshi")
elif ball >= 60:
    print("Qoniqarli")
else:
    print("Qoniqarsiz")

# 9
yigindi = 0
for i in range(1, 101):
    yigindi = yigindi + i
print(yigindi)            # 5050

# 10
n = int(input("Son: "))
for i in range(1, 10):
    print(f"{n} x {i} = {n * i}")

# 11
while True:
    soz = input("So'z ('stop' to'xtatadi): ")
    if soz == "stop":
        break
    print(soz)

# 12
def juft_toq(n):
    if n % 2 == 0:
        return "juft"
    else:
        return "toq"
print(juft_toq(10))       # juft

# 13
for i in range(1, 20):
    if i == 7:
        break
    print(i)              # 1..6

# 14
for i in range(1, 11):
    if i == 5:
        continue
    print(i)              # 5 dan tashqari hammasi

# 15
son = int(input("Son: "))
tubmi = True
if son < 2:
    tubmi = False
for i in range(2, son):
    if son % i == 0:
        tubmi = False
        break
print("tub son" if tubmi else "tub son emas")

# 16
def kalkulyator(a, b, amal):
    if amal == "+":
        return a + b
    elif amal == "-":
        return a - b
    elif amal == "*":
        return a * b
    elif amal == "/":
        return a / b
print(kalkulyator(10, 3, "*"))   # 30

# 17
for i in range(1, 51):
    if i % 3 == 0 and i % 5 == 0:
        print(i)          # 15, 30, 45

# 18
while True:
    parol = input("Parol: ")
    if parol == "python123":
        print("Kirish muvaffaqiyatli")
        break

# 19
def faktorial(n):
    natija = 1
    for i in range(1, n + 1):
        natija = natija * i
    return natija
print(faktorial(5))       # 120

# 20
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

</details>

**Qo'shimcha masalalar yechimi (21–26):**

<details markdown="1">
<summary>Masala 21 — *args bilan o'rtacha</summary>

```python
def ortacha(*sonlar: float) -> float:
    if not sonlar:                 # bo'sh bo'lsa, nolga bo'lishdan saqlanamiz
        return 0.0
    return sum(sonlar) / len(sonlar)

print(ortacha(10, 20, 30))     # 20.0
print(ortacha(5))              # 5.0
print(ortacha())               # 0.0
```

</details>

<details markdown="1">
<summary>Masala 22 — match/case kalkulyator</summary>

```python
def kalkulyator(a: float, b: float, amal: str) -> float | str:
    match amal:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            return a / b if b != 0 else "Nolga bo'lib bo'lmaydi"
        case _:
            return "Noma'lum amal"

print(kalkulyator(8, 2, "/"))   # 4.0
print(kalkulyator(8, 0, "/"))   # Nolga bo'lib bo'lmaydi
print(kalkulyator(8, 2, "^"))   # Noma'lum amal
```

</details>

<details markdown="1">
<summary>Masala 23 — for-else tub son</summary>

```python
def tubmi(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False           # bo'luvchi topildi → tub emas
    else:
        return True                # break bo'lmadi → tub

print(tubmi(7))    # True
print(tubmi(9))    # False
print(tubmi(13))   # True
```

</details>

<details markdown="1">
<summary>Masala 24 — keyword-only parametrlar</summary>

```python
def hisobvaraq(ism: str, *, balans: float = 0.0, valyuta: str = "USD") -> str:
    return f"{ism}: {balans} {valyuta}"

print(hisobvaraq("Aziz"))                              # Aziz: 0.0 USD
print(hisobvaraq("Malika", balans=500, valyuta="UZS")) # Malika: 500 UZS
# hisobvaraq("Olim", 100)  -> XATO: balans pozitsion uzatib bo'lmaydi
```

</details>

<details markdown="1">
<summary>Masala 25 — mutable default tuzatish</summary>

```python
def savatga_qosh(mahsulot: str, savat: list[str] | None = None) -> list[str]:
    if savat is None:
        savat = []             # har chaqiruvda yangi ro'yxat
    savat.append(mahsulot)
    return savat

print(savatga_qosh("non"))     # ['non']
print(savatga_qosh("sut"))     # ['sut']   — to'planib qolmadi
```

</details>

<details markdown="1">
<summary>Masala 26 — match + dataclass yuza</summary>

```python
from dataclasses import dataclass

@dataclass
class Doira:
    radius: float

@dataclass
class Tortburchak:
    eni: float
    boyi: float

def yuza(shakl: Doira | Tortburchak) -> float:
    match shakl:
        case Doira(radius=r):
            return 3.14159 * r * r
        case Tortburchak(eni=e, boyi=b):
            return e * b
        case _:
            return 0.0

print(round(yuza(Doira(2)), 2))   # 12.57
print(yuza(Tortburchak(3, 4)))    # 12
```

</details>

---

[← Asoslar](./01-asoslar.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Ma'lumot tuzilmalari →](./03-malumot-tuzilmalari.md)
