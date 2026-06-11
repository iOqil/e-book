# 03 — Ma'lumot tuzilmalari

Hozirgacha bitta o'zgaruvchida bitta qiymat saqladik. Lekin ko'pincha **bir nechta qiymatni birga** saqlash kerak bo'ladi — masalan, o'quvchilar ro'yxati yoki mahsulot narxlari. Buning uchun Python'da maxsus tuzilmalar bor: **ro'yxat**, **lug'at**, **to'plam** va **tuple**.

> **Bu modulda:** ro'yxat (list) va uning metodlari, slicing, lug'at (dict), to'plam (set), tuple, va list comprehension.

---

## 3.1 Ro'yxat (list) — eng ko'p ishlatiladigan tuzilma

Ro'yxat — tartiblangan qiymatlar to'plami. Kvadrat qavs `[ ]` ichida, vergul bilan ajratiladi:

```python
mevalar = ["olma", "banan", "uzum"]
sonlar = [10, 20, 30, 40]
aralash = [1, "salom", 3.14, True]    # turli tiplar ham bo'lishi mumkin
bosh = []                              # bo'sh ro'yxat
```

**Elementga murojaat** — har bir element o'z **indeksi** (raqami) bilan. Diqqat: indeks **0 dan** boshlanadi:

```python
mevalar = ["olma", "banan", "uzum"]
print(mevalar[0])     # olma    (birinchi element)
print(mevalar[1])     # banan
print(mevalar[2])     # uzum
print(mevalar[-1])    # uzum    (oxirgisi — manfiy indeks oxiridan sanaydi)
print(mevalar[-2])    # banan
```

Ro'yxat ichida har bir element o'z indeksiga bog'langan; quyidagi diagramma musbat va manfiy indekslarning bir xil katakka qanday ishora qilishini ko'rsatadi:

![list ichki ko'rinishi: indeks va element bog'lanishi](rasmlar/py03-list-indeks.svg)

**Elementni o'zgartirish:**

```python
mevalar[0] = "anor"
print(mevalar)        # ['anor', 'banan', 'uzum']
```

**Uzunligini bilish** — `len()`:

```python
print(len(mevalar))   # 3
```

**Ro'yxat bo'ylab aylanish** (`for` bilan, 2-modulda ko'rgan edik):

```python
for meva in mevalar:
    print(meva)
```

---

## 3.2 Ro'yxat metodlari

Ro'yxatga amal qilish uchun tayyor metodlar bor. Metod — `royxat.metod()` ko'rinishida chaqiriladi:

```python
sonlar = [3, 1, 2]

sonlar.append(4)        # oxiriga qo'shadi → [3, 1, 2, 4]
sonlar.insert(0, 9)     # 0-indeksga qo'yadi → [9, 3, 1, 2, 4]
sonlar.remove(1)        # qiymat 1 ni o'chiradi → [9, 3, 2, 4]
oxirgi = sonlar.pop()   # oxirgini olib tashlaydi va qaytaradi → oxirgi=4
sonlar.sort()           # tartiblaydi → [2, 3, 9]
sonlar.reverse()        # teskari qiladi → [9, 3, 2]

print(len(sonlar))      # nechta element
print(3 in sonlar)      # True  — 3 ro'yxatda bormi?
print(sonlar.count(3))  # 3 nechta marta uchraydi
```

> **Eng ko'p ishlatiladigani — `append()`.** Ko'pincha bo'sh ro'yxatdan boshlab, sikl ichida `append` bilan to'ldirasan:
> ```python
> kvadratlar = []
> for i in range(1, 6):
>     kvadratlar.append(i * i)
> print(kvadratlar)      # [1, 4, 9, 16, 25]
> ```

---

## 3.3 Slicing — ro'yxatning bir qismini olish

Slicing (kesib olish) — ro'yxatdan bir qismini ajratib olish. `[boshlanish:tugash]` ko'rinishida (tugash indeksi **kirmaydi**):

```python
sonlar = [0, 1, 2, 3, 4, 5]

print(sonlar[1:4])     # [1, 2, 3]      (1-indeksdan 4 gacha, 4 kirmaydi)
print(sonlar[:3])      # [0, 1, 2]      (boshidan 3 gacha)
print(sonlar[3:])      # [3, 4, 5]      (3-indeksdan oxirigacha)
print(sonlar[-2:])     # [4, 5]         (oxirgi 2 ta)
print(sonlar[::2])     # [0, 2, 4]      (har 2-element)
```

Quyidagi diagramma `[start:stop:step]` qanday ishlashini ko'rsatadi — `start` kiradi, `stop` esa kirmaydi:

![slicing [start:stop:step] qanday ishlaydi](rasmlar/py03-slicing.svg)

> Slicing matnlarda ham xuddi shunday ishlaydi (4-modulda ko'rasan). U **yangi** ro'yxat qaytaradi, aslini o'zgartirmaydi.

---

## 3.4 Lug'at (dict) — kalit–qiymat juftliklari

Lug'at — har bir qiymat **nom** (kalit) bilan saqlanadigan tuzilma. Ro'yxatda elementlar raqam (indeks) bilan, lug'atda esa **kalit** bilan topiladi. Jingalak qavs `{ }` ichida `kalit: qiymat` ko'rinishida:

```python
talaba = {
    "ism": "Aziz",
    "yosh": 20,
    "shahar": "Toshkent",
}
```

**Qiymatga murojaat** — kalit orqali:

```python
print(talaba["ism"])      # Aziz
print(talaba["yosh"])     # 20
```

Lug'at qiymatni shu qadar tez topishining sababi — kalit ichkarida **hash** qiymatiga aylantiriladi va shu orqali saqlangan joy (bucket) aniqlanadi:

![dict ichki ishlashi: kalit, hash va bucket bog'lanishi](rasmlar/py03-dict-hashing.svg)

**Qo'shish va o'zgartirish:**

```python
talaba["telefon"] = "998901234567"   # yangi kalit qo'shadi
talaba["yosh"] = 21                  # mavjud kalitni o'zgartiradi
```

**Xavfsiz murojaat** — `get()` (kalit yo'q bo'lsa xato bermaydi):

```python
print(talaba.get("email"))            # None  (kalit yo'q, lekin xato yo'q)
print(talaba.get("email", "yo'q"))    # yo'q  (standart qiymat berish mumkin)
# Solishtirish uchun: talaba["email"] — KeyError xatosi berardi
```

**Lug'at bo'ylab aylanish:**

```python
for kalit in talaba:
    print(kalit, "=", talaba[kalit])

# yoki kalit va qiymatni birga:
for kalit, qiymat in talaba.items():
    print(f"{kalit}: {qiymat}")
```

> **Qachon ro'yxat, qachon lug'at?** Tartibli, bir xil turdagi narsalar uchun (mevalar, ballar) — ro'yxat. Har bir narsaning "nomi"/xususiyati bo'lsa (ism, yosh, shahar) — lug'at.

---

## 3.5 To'plam (set) — takrorlanmas qiymatlar

To'plam — takrorlanmaydigan qiymatlar to'plami. Tartib yo'q, takror yo'q. Jingalak qavs `{ }` (lekin kalit-qiymat emas, faqat qiymatlar):

```python
ranglar = {"qizil", "yashil", "qizil", "ko'k"}
print(ranglar)        # {'qizil', 'yashil', 'ko'k'}  — takror avtomatik o'chdi
```

Eng foydali ishlatilishi — **takrorlarni olib tashlash**:

```python
sonlar = [1, 2, 2, 3, 3, 3, 4]
noyob = set(sonlar)
print(noyob)          # {1, 2, 3, 4}
print(len(noyob))     # 4  — nechta xil son bor
```

To'plam amallari:

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)          # {2, 3}      — umumiy (kesishma)
print(a | b)          # {1, 2, 3, 4}  — birlashma
print(a - b)          # {1}         — a da bor, b da yo'q
```

---

## 3.6 Tuple — o'zgarmas ro'yxat

Tuple — ro'yxatga o'xshaydi, lekin **o'zgartirib bo'lmaydi** (qiymat berib qo'yilgandan keyin qo'shish/o'chirish/o'zgartirish mumkin emas). Oddiy qavs `( )` ichida:

```python
koordinata = (41.31, 69.28)
print(koordinata[0])      # 41.31
# koordinata[0] = 50      # XATO — tuple o'zgarmas
```

> **Qachon tuple?** O'zgarmasligi kerak bo'lgan ma'lumotlar uchun — masalan koordinata, RGB rang, yoki bir nechta qiymatni birga qaytarish. Tasodifan o'zgartirib qo'yishdan himoya qiladi.

Endi to'rttala tuzilmani bir joyda taqqoslab ko'ramiz — qaysi biri o'zgaruvchan, tartibli yoki takrorga ruxsat berishini quyidagi jadval umumlashtiradi:

![list, dict, set, tuple taqqoslash jadvali](rasmlar/py03-tuzilmalar-taqqoslash.svg)

Funksiyadan bir nechta qiymat qaytarishda tuple qulay:

```python
def min_max(sonlar: list[int]) -> tuple[int, int]:
    return min(sonlar), max(sonlar)   # tuple qaytaradi

eng_kichik, eng_katta = min_max([5, 2, 8, 1])
print(eng_kichik, eng_katta)          # 1 8
```

> Type hint'lar (`list[int]`, `-> tuple[int, int]`) — kodni o'qishni osonlashtiradi va muharrir xatolarni oldindan ko'rsatishga yordam beradi. Python 3.9 dan beri `list`, `tuple`, `dict` ni to'g'ridan-to'g'ri qavs bilan yozish mumkin (eski `List`, `Tuple` import qilish shart emas). 10-modulda bu mavzuga chuqurroq kiramiz.

---

## 3.7 List comprehension — ro'yxatni qisqa yo'l bilan yaratish

Ko'pincha bir ro'yxatdan boshqasini yasaymiz. Buni `for` bilan ham qilsa bo'ladi, lekin **list comprehension** qisqaroq:

```python
# Oddiy usul (for bilan):
kvadratlar = []
for i in range(1, 6):
    kvadratlar.append(i * i)

# List comprehension bilan — bir qatorda:
kvadratlar = [i * i for i in range(1, 6)]
print(kvadratlar)         # [1, 4, 9, 16, 25]
```

Shart qo'shish ham mumkin (`if` bilan):

```python
juftlar = [i for i in range(1, 11) if i % 2 == 0]
print(juftlar)            # [2, 4, 6, 8, 10]
```

> Boshida `for` bilan yozaver — comprehension ko'zga o'rganib qolgach, qisqaroq variantga o'tasan. Ikkalasi bir xil natija beradi.

---

## 3.8 Dict va set comprehension, generator ifoda

List comprehension yolg'iz emas — xuddi shu g'oya **lug'at** va **to'plam** uchun ham ishlaydi. Faqat kvadrat qavs o'rniga jingalak qavs ishlatiladi.

**Dict comprehension** — `{kalit: qiymat for ...}` ko'rinishida. Ikki ro'yxatdan lug'at yasash uchun ayniqsa qulay:

```python
nomlar = ["olma", "banan", "uzum"]
narxlar = [12000, 9000, 15000]

katalog = {nom: narx for nom, narx in zip(nomlar, narxlar)}
print(katalog)        # {'olma': 12000, 'banan': 9000, 'uzum': 15000}

# Son -> uning kvadrati lug'ati:
kvadrat_lugat = {i: i * i for i in range(1, 6)}
print(kvadrat_lugat)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

`if` shartini ham qo'shsa bo'ladi — faqat shartni qondiradigan juftliklar qoladi:

```python
arzonlar = {nom: narx for nom, narx in katalog.items() if narx < 13000}
print(arzonlar)       # {'olma': 12000, 'banan': 9000}
```

**Set comprehension** — `{ifoda for ...}` (kalit-qiymat emas, faqat qiymat). Natijada takror avtomatik tushib qoladi:

```python
sozlar = ["olma", "banan", "olma", "uzum", "banan"]

noyob_uzunliklar = {len(s) for s in sozlar}
print(noyob_uzunliklar)   # {4, 5}  -- takrorlanmagan uzunliklar

birinchi_harflar = {s[0] for s in sozlar}
print(birinchi_harflar)   # {'o', 'b', 'u'}  -- noyob bosh harflar
```

**Generator ifoda** — `(ifoda for ...)` (oddiy qavs). U list comprehension'ga o'xshaydi, lekin **butun ro'yxatni xotirada yasamaydi** — elementlarni bittalab, kerak bo'lganda ishlab beradi. Shuning uchun katta hajmlarda xotirani tejaydi:

```python
# List comprehension butun ro'yxatni yasaydi (xotirada saqlanadi):
royxat = [i * i for i in range(1, 6)]
print(royxat)             # [1, 4, 9, 16, 25]

# Generator ifoda esa "retsept" qaytaradi, qiymatlarni darrov yasamaydi:
gen = (i * i for i in range(1, 6))
print(gen)                # <generator object <genexpr> at 0x...>  (manzil har xil)

# U bilan ham aylanish mumkin (bir martalik):
for q in gen:
    print(q, end=" ")     # 1 4 9 16 25
print()
```

Eng tez-tez ishlatilishi — `sum()`, `max()`, `min()` kabi funksiyalarga to'g'ridan-to'g'ri uzatish. Bunda oraliq ro'yxat umuman yasalmaydi:

```python
# 1 dan 1000 gacha kvadratlar yig'indisi -- ro'yxat yasamasdan:
jami = sum(i * i for i in range(1, 1001))
print(jami)               # 333833500
```

> **Qaysi qavs nima yasaydi?** `[...]` -> list, `{...}` (kalit:qiymat bilan) -> dict, `{...}` (faqat qiymat) -> set, `(...)` -> generator. Bitta g'oya, to'rtta tuzilma.

---

## 3.9 Shartli va ichma-ich (nested) comprehension

Comprehension ichida shart ikki xil joyda turishi mumkin — va ular **butunlay boshqa** ma'no beradi.

**1) Oxirida `if` — filtrlash** (elementni o'tkazadi yoki tashlaydi):

```python
sonlar = [-3, 5, -1, 8, -7]
musbatlar = [s for s in sonlar if s > 0]
print(musbatlar)          # [5, 8]
```

**2) Boshida `if/else` — har bir element uchun tanlash** (`[a if shart else b for ...]`). Bu yerda hamma element qoladi, lekin qiymati shartga qarab o'zgaradi:

```python
sonlar = [-3, 5, -1, 8, -7]
belgilar = ["musbat" if s > 0 else "manfiy" for s in sonlar]
print(belgilar)           # ['manfiy', 'musbat', 'manfiy', 'musbat', 'manfiy']
```

> **Tuzoq:** `[x for x in ... if shart]` (filtr) va `[x if shart else y for x in ...]` (tanlash) — `if` ning joyiga qarab butunlay boshqa narsa. Filtrda `else` yo'q; tanlashda `else` shart.

**Ichma-ich (nested) comprehension** — ikkita `for` bilan. Masalan, matritsani (ro'yxatlar ro'yxatini) bitta tekis ro'yxatga aylantirish:

```python
matritsa = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
tekis = [son for qator in matritsa for son in qator]
print(tekis)              # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

> O'qish tartibi chapdan o'ngga: avval `for qator in matritsa`, keyin `for son in qator` — xuddi ikki ichma-ich `for` siklidek.

Comprehension ichida yana comprehension qo'yib, jadval (ro'yxatlar ro'yxati) yasash ham mumkin:

```python
jadval = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(jadval)             # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

---

## 3.10 Ro'yxat metodlari — yana ko'proq

3.2 da `append`, `insert`, `remove`, `pop`, `sort`, `reverse` bilan tanishding. Endi qolgan muhimlarini ko'ramiz.

**`extend()` va `append()` farqi** — bu eng ko'p adashtiradigan juftlik:

```python
a = [1, 2, 3]
a.append([4, 5])
print(a)              # [1, 2, 3, [4, 5]]  -- ro'yxatni bitta element qilib qo'shdi

b = [1, 2, 3]
b.extend([4, 5])
print(b)              # [1, 2, 3, 4, 5]    -- elementlarni birma-bir qo'shdi
```

**`index()`** — qiymat qaysi indeksda turganini topadi (birinchi uchraganini):

```python
mevalar = ["olma", "banan", "uzum", "banan"]
print(mevalar.index("banan"))   # 1
print("uzum" in mevalar)        # True  -- avval mavjudligini tekshirgan ma'qul
```

**`sorted()` va `.sort()` farqi** — ikkalasi ham tartiblaydi, lekin:

- `lst.sort()` — ro'yxatning **o'zini** o'zgartiradi, `None` qaytaradi.
- `sorted(lst)` — **yangi** ro'yxat qaytaradi, aslini o'zgartirmaydi.

```python
asl = [3, 1, 2]
yangi = sorted(asl)
print(yangi)          # [1, 2, 3]  -- yangi ro'yxat
print(asl)            # [3, 1, 2]  -- asl o'zgarmadi
```

Ikkalasi ham `key=` va `reverse=` qabul qiladi. `key=` — har bir elementni nima bo'yicha solishtirishni belgilaydi (funksiya beradi):

```python
sozlar = ["olma", "non", "banan", "uzum"]
print(sorted(sozlar, key=len))          # ['non', 'olma', 'uzum', 'banan']  -- uzunligi bo'yicha
print(sorted(sozlar, reverse=True))     # ['uzum', 'olma', 'non', 'banan']  -- teskari alifbo

# Lug'atlar ro'yxatini biror maydon bo'yicha tartiblash -- juda ko'p ishlatiladi:
talabalar = [
    {"ism": "Aziz", "ball": 85},
    {"ism": "Malika", "ball": 92},
    {"ism": "Bobur", "ball": 78},
]
eng_yaxshilar = sorted(talabalar, key=lambda t: t["ball"], reverse=True)
print(eng_yaxshilar[0]["ism"])          # Malika
```

**`copy()`** — ro'yxatning nusxasini oladi (buni 3.13 da chuqur tushuntiramiz):

```python
asl = [1, 2, 3]
nusxa = asl.copy()
nusxa.append(4)
print(asl, nusxa)     # [1, 2, 3] [1, 2, 3, 4]  -- mustaqil
```

**`del` va slice'ga qiymat berish** — `del` indeks yoki slice bo'yicha o'chiradi; slice'ga ro'yxat tenglab, bir qismni butunlay almashtirish mumkin:

```python
sonlar = [0, 1, 2, 3, 4, 5]
del sonlar[0]
print(sonlar)         # [1, 2, 3, 4, 5]
del sonlar[1:3]
print(sonlar)         # [1, 4, 5]

# Slice'ga qiymat berish -- o'lchami har xil bo'lsa ham bo'ladi:
sonlar = [0, 1, 2, 3, 4]
sonlar[1:3] = [10, 20, 30]
print(sonlar)         # [0, 10, 20, 30, 3, 4]
```

---

## 3.11 Lug'at metodlari — yana ko'proq

3.4 da `get`, `items` bilan tanishding. Endi kundalik ishda kerak bo'ladiganlarini ko'ramiz.

**`update()`** — bir lug'atga boshqa lug'at (yoki juftliklar)ni qo'shadi/yangilaydi:

```python
talaba = {"ism": "Aziz", "yosh": 20}
talaba.update({"yosh": 21, "shahar": "Toshkent"})
print(talaba)         # {'ism': 'Aziz', 'yosh': 21, 'shahar': 'Toshkent'}
```

**`setdefault()`** — kalit bo'lmasa qo'shadi va qiymatini qaytaradi; bo'lsa mavjudini qaytaradi (tegmaydi):

```python
talaba.setdefault("email", "yo'q")   # email yo'q edi -> qo'shildi
talaba.setdefault("ism", "X")        # ism bor edi -> tegmadi
print(talaba["email"])               # yo'q
print(talaba["ism"])                 # Aziz
```

**`keys()`, `values()`, `items()`** — mos ravishda kalitlar, qiymatlar va juftliklar ustidan aylanish imkonini beradi:

```python
narxlar = {"olma": 12000, "non": 4000}
print(list(narxlar.keys()))     # ['olma', 'non']
print(list(narxlar.values()))   # [12000, 4000]
print(list(narxlar.items()))    # [('olma', 12000), ('non', 4000)]
print(sum(narxlar.values()))    # 16000  -- qiymatlar yig'indisi
```

**`pop()`** — kalitni o'chiradi va qiymatini qaytaradi. Standart qiymat bersang, yo'q kalitda ham xato bermaydi:

```python
yosh = talaba.pop("yosh")
print(yosh)                      # 21
print(talaba.pop("telefon", "yo'q"))   # yo'q  -- kalit yo'q, standart qaytdi
```

**`dict.fromkeys()`** — bir xil boshlang'ich qiymat bilan lug'at yasaydi:

```python
hisob = dict.fromkeys(["a", "b", "c"], 0)
print(hisob)          # {'a': 0, 'b': 0, 'c': 0}
```

**Tartib kafolati (3.7+):** Python 3.7 dan boshlab lug'at kalitlarni **qo'shilish tartibida** saqlaydi — aylanishda ular qaysi tartibda qo'shilgan bo'lsa, shu tartibda chiqadi:

```python
d = {}
d["z"] = 1
d["a"] = 2
d["m"] = 3
print(list(d))        # ['z', 'a', 'm']  -- alifbo emas, qo'shilish tartibi
```

**`|` bilan birlashtirish (3.9+):** Ikki lug'atni `|` bilan qo'shib, yangi lug'at olish mumkin. Bir xil kalitda **o'ngdagi** g'olib:

```python
x = {"a": 1, "b": 2}
y = {"b": 20, "c": 3}
print(x | y)          # {'a': 1, 'b': 20, 'c': 3}

x |= y                # x ni o'rnida yangilaydi (update kabi)
print(x)              # {'a': 1, 'b': 20, 'c': 3}
```

---

## 3.12 To'plam metodlari va frozenset

3.5 da `&`, `|`, `-` operatorlarini ko'rgan eding. Ularning **metod** ko'rinishi ham bor, ustiga `^` (symmetric difference) qo'shiladi.

**Element qo'shish/o'chirish:**

```python
ranglar = {"qizil", "yashil"}
ranglar.add("ko'k")        # qo'shadi
ranglar.discard("sariq")   # yo'q bo'lsa ham XATO BERMAYDI
ranglar.remove("qizil")    # bor elementni o'chiradi
# ranglar.remove("sariq")  # KeyError -- remove yo'q elementda xato beradi
print(ranglar)             # {"ko'k", 'yashil'}
```

> `discard` vs `remove`: ikkalasi ham o'chiradi, lekin `discard` yo'q elementda jim turadi, `remove` esa xato beradi. Ishonchsiz bo'lsang — `discard`.

**To'plam amallari — operator va metod (bir xil natija):**

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b,  a.union(b))                  # {1,2,3,4}  birlashma
print(a & b,  a.intersection(b))           # {2,3}      kesishma
print(a - b,  a.difference(b))             # {1}        a da bor, b da yo'q
print(a ^ b,  a.symmetric_difference(b))   # {1,4}      faqat bittasida bor
```

`^` (symmetric difference) — "ikkalasida ham emas, faqat bittasida" degani: birlashmadan kesishmani ayirgancha.

**Qism-to'plam tekshiruvi:**

```python
print({1, 2}.issubset({1, 2, 3}))      # True  -- {1,2} ichida-mi?
print({1, 2, 3}.issuperset({1, 2}))    # True  -- {1,2} ni qamrab oladimi?
```

**`frozenset` — o'zgarmas to'plam.** Oddiy `set` o'zgaruvchan (`add`/`remove` bo'ladi), shuning uchun uni lug'at kaliti yoki boshqa set elementi qilib bo'lmaydi. `frozenset` esa o'zgarmas — shuning uchun kalit bo'la oladi:

```python
muzlatilgan = frozenset([1, 2, 3])
print(muzlatilgan)         # frozenset({1, 2, 3})
# muzlatilgan.add(4)       # XATO -- frozenset o'zgartirib bo'lmaydi

# Lug'at kaliti sifatida ishlatish mumkin:
xarita = {frozenset([1, 2]): "juftlik", frozenset([3]): "yakka"}
print(xarita[frozenset([1, 2])])   # juftlik
```

> **Tuple list'ga nima bo'lsa, frozenset set'ga ham shu:** o'zgarmas variant. O'zgarmaslik kalit bo'la olish va tasodifiy o'zgartirishdan himoya beradi.

---

## 3.13 Yuza (shallow) va chuqur (deep) nusxalash

01-modulda ko'rgan eding: o'zgaruvchi obyektni **o'z ichida saqlamaydi**, balki unga ishora qiladigan nom (reference model). Shu sabab `b = a` obyektni nusxalamaydi — bitta obyektga ikkinchi nom beradi, xolos:

```python
a = [1, 2, 3]
b = a               # nusxa EMAS -- bitta obyekt, ikki nom
b.append(4)
print(a)            # [1, 2, 3, 4]  -- a ham "o'zgardi", chunki a va b bir narsa
print(a is b)       # True
```

Haqiqiy nusxa kerak bo'lsa, `a.copy()` (yoki `list(a)`, yoki `a[:]`) ishlatiladi. Bu **yuza (shallow) nusxa** — yuqori darajadagi ro'yxat ko'chiriladi:

```python
asl = [1, 2, 3]
yuza = asl.copy()
yuza.append(4)
print(asl, yuza)    # [1, 2, 3] [1, 2, 3, 4]  -- mustaqil
print(asl is yuza)  # False  -- alohida obyektlar
```

**Lekin tuzoq bor:** yuza nusxa faqat eng tashqi ro'yxatni ko'chiradi. Ichidagi ro'yxatlar (yoki boshqa o'zgaruvchan obyektlar) **baribir baham ko'riladi** — ikkala nusxa ham o'sha bitta ichki obyektga ishora qiladi:

```python
asl = [[1, 2], [3, 4]]
yuza = asl.copy()
yuza[0].append(99)
print(asl)          # [[1, 2, 99], [3, 4]]  -- asl ham o'zgardi!
print(yuza)         # [[1, 2, 99], [3, 4]]
```

Bunday "ichma-ich" tuzilmalarni to'liq mustaqil nusxalash uchun `copy.deepcopy()` kerak — u **har bir darajani** rekursiv nusxalaydi:

```python
import copy

asl = [[1, 2], [3, 4]]
chuqur = copy.deepcopy(asl)
chuqur[0].append(99)
print(asl)          # [[1, 2], [3, 4]]      -- asl butunlay himoyalangan
print(chuqur)       # [[1, 2, 99], [3, 4]]
```

> **Uchta darajani ajrat:**
> - `b = a` — nusxa yo'q, bitta obyekt ikki nom (`is` -> `True`).
> - `b = a.copy()` — yuza nusxa: tashqisi alohida, ichkisi baham ko'riladi.
> - `b = copy.deepcopy(a)` — chuqur nusxa: har bir daraja alohida, butunlay mustaqil.
>
> Oddiy (ichma-ich bo'lmagan) ro'yxat uchun `copy()` yetarli; ichida ro'yxat/lug'at bo'lsa — `deepcopy` o'yla.

---

## ✍️ Masalalar (26 ta)

> Bu masalalar 1–3 modullar mavzulariga asoslangan.

**Oson (1–7):**

1. `["olma", "banan", "uzum"]` ro'yxatini yarat. Birinchi va oxirgi elementini chiqar.
2. Bo'sh ro'yxat yarat, unga `append` bilan 3 ta son qo'sh, keyin ro'yxatni chiqar.
3. `[5, 2, 8, 1, 9]` ro'yxatini `sort` bilan tartibla va chiqar. Keyin `len` bilan uzunligini chiqar.
4. `[10, 20, 30, 40, 50]` ro'yxatidan slicing bilan o'rtadagi 3 tasini (`[20, 30, 40]`) ol.
5. `talaba` lug'atini yarat (`ism`, `yosh`, `shahar`). Har bir kalitning qiymatini chiqar.
6. `[1, 1, 2, 3, 3, 3, 4]` ro'yxatidan `set` bilan takrorlarni olib tashla va nechta xil son borligini chiqar.
7. Bir lug'atga yangi kalit qo'sh va mavjud kalitning qiymatini o'zgartir.

**O'rta (8–14):**

8. Sonlar ro'yxatining yig'indisini va o'rtachasini hisobla (`sum()` va `len()` ishlat).
9. Ro'yxatdagi eng katta va eng kichik sonni top (`max()`, `min()`).
10. Foydalanuvchidan 5 ta son so'rab (sikl bilan), ularni ro'yxatga `append` qil, keyin ro'yxatni tartiblab chiqar.
11. Lug'at bo'ylab `items()` bilan aylanib, har bir juftlikni `kalit: qiymat` ko'rinishida chiqar.
12. List comprehension bilan 1 dan 20 gacha sonlarning kvadratlari ro'yxatini yasa.
13. List comprehension va `if` bilan 1 dan 30 gacha 3 ga bo'linadigan sonlar ro'yxatini yasa.
14. Ikkita ro'yxatning umumiy elementlarini top (`set` va `&` ishlat): `[1,2,3,4]` va `[3,4,5,6]`.

**Murakkab (15–20):**

15. So'zlar ro'yxati berilgan. Har bir so'z necha marta uchraganini sanab, lug'atga yoz (maslahat: lug'at + `get`). Masalan `["a","b","a","c","a"]` → `{"a":3, "b":1, "c":1}`.
16. Talabalar ro'yxati (har biri lug'at: `ism`, `ball`). Ballari 60 dan yuqorilarning ismlarini chiqar.
17. Sonlar ro'yxatidan faqat juftlarini yangi ro'yxatga ajrat (ham `for` bilan, ham list comprehension bilan — ikki usulda).
18. Foydalanuvchidan so'zlar kiritishini so'ra ("stop" deguncha), ularni ro'yxatga yig'. Oxirida nechta so'z kiritilganini va ularni alifbo tartibida chiqar.
19. Bir lug'atda mahsulot nomi → narxi saqlangan. Barcha narxlar yig'indisini hisobla va eng qimmat mahsulot nomini top.
20. Telefon kitobchasi: foydalanuvchi "qo'shish", "qidirish" yoki "chiqish" tanlasin. Qo'shishda ism va raqamni lug'atga saqla, qidirishda ism bo'yicha raqamni chiqar (`while` sikli bilan davomli ishlasin).

**Qo'shimcha (21–26) — comprehension, yangi metodlar va nusxalash:**

21. Dict comprehension bilan `["olma", "non", "banan"]` so'zlaridan `{so'z: uzunligi}` lug'atini yasa.
22. `zip` bilan ikkita ro'yxatdan (`nomlar`, `narxlar`) lug'at tuz, keyin set comprehension bilan narxi 10000 dan yuqori mahsulot **nomlari to'plamini** ajrat.
23. Talabalar ro'yxati berilgan (har biri `ism`, `ball` lug'at). `sorted(key=...)` bilan ularni ball bo'yicha kamayish tartibida tartibla va eng yuqori 3 tasini chiqar.
24. `[[1, 2], [3, 4]]` ichma-ich ro'yxat uchun `copy()` (yuza) va `copy.deepcopy()` (chuqur) farqini ko'rsat: ichki ro'yxatni o'zgartirib, qaysi holatda asl o'zgarishini namoyish qil.
25. Ikki guruh (to'plam): `{"Aziz","Malika","Bobur"}` va `{"Malika","Sardor"}`. Birlashma, kesishma, ayirma va symmetric difference (`^`) ni chiqar.
26. Generator ifoda bilan 1 dan 1000 gacha sonlarning kvadratlari yig'indisini hisobla (oraliq ro'yxat yasamasdan).

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
mevalar = ["olma", "banan", "uzum"]
print(mevalar[0], mevalar[-1])     # olma uzum

# 2
sonlar = []
sonlar.append(10)
sonlar.append(20)
sonlar.append(30)
print(sonlar)                      # [10, 20, 30]

# 3
sonlar = [5, 2, 8, 1, 9]
sonlar.sort()
print(sonlar)                      # [1, 2, 5, 8, 9]
print(len(sonlar))                 # 5

# 4
sonlar = [10, 20, 30, 40, 50]
print(sonlar[1:4])                 # [20, 30, 40]

# 5
talaba = {"ism": "Aziz", "yosh": 20, "shahar": "Toshkent"}
print(talaba["ism"])
print(talaba["yosh"])
print(talaba["shahar"])

# 6
sonlar = [1, 1, 2, 3, 3, 3, 4]
print(len(set(sonlar)))            # 4

# 7
talaba = {"ism": "Aziz", "yosh": 20}
talaba["shahar"] = "Toshkent"      # qo'shish
talaba["yosh"] = 21                # o'zgartirish
print(talaba)

# 8
sonlar = [10, 20, 30, 40]
print(sum(sonlar))                 # 100
print(sum(sonlar) / len(sonlar))   # 25.0

# 9
sonlar = [5, 2, 8, 1, 9]
print(max(sonlar), min(sonlar))    # 9 1

# 10
sonlar = []
for i in range(5):
    sonlar.append(int(input(f"{i+1}-son: ")))
sonlar.sort()
print(sonlar)

# 11
talaba = {"ism": "Aziz", "yosh": 20, "shahar": "Toshkent"}
for kalit, qiymat in talaba.items():
    print(f"{kalit}: {qiymat}")

# 12
kvadratlar = [i * i for i in range(1, 21)]
print(kvadratlar)

# 13
uchga = [i for i in range(1, 31) if i % 3 == 0]
print(uchga)                       # [3, 6, 9, ..., 30]

# 14
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
print(set(a) & set(b))             # {3, 4}

# 15
sozlar = ["a", "b", "a", "c", "a"]
hisob = {}
for soz in sozlar:
    hisob[soz] = hisob.get(soz, 0) + 1
print(hisob)                       # {'a': 3, 'b': 1, 'c': 1}

# 16
talabalar = [
    {"ism": "Aziz", "ball": 85},
    {"ism": "Malika", "ball": 55},
    {"ism": "Bobur", "ball": 72},
]
for t in talabalar:
    if t["ball"] > 60:
        print(t["ism"])            # Aziz, Bobur

# 17
sonlar = [1, 2, 3, 4, 5, 6]
# for bilan:
juftlar = []
for s in sonlar:
    if s % 2 == 0:
        juftlar.append(s)
print(juftlar)                     # [2, 4, 6]
# comprehension bilan:
juftlar2 = [s for s in sonlar if s % 2 == 0]
print(juftlar2)                    # [2, 4, 6]

# 18
sozlar = []
while True:
    soz = input("So'z ('stop' to'xtatadi): ")
    if soz == "stop":
        break
    sozlar.append(soz)
sozlar.sort()
print(f"{len(sozlar)} ta so'z:", sozlar)

# 19
mahsulotlar = {"olma": 12000, "non": 4000, "go'sht": 90000}
print("Jami:", sum(mahsulotlar.values()))
eng_qimmat = ""
eng_narx = 0
for nom, narx in mahsulotlar.items():
    if narx > eng_narx:
        eng_narx = narx
        eng_qimmat = nom
print("Eng qimmat:", eng_qimmat)   # go'sht

# 20
kitobcha = {}
while True:
    amal = input("qo'shish / qidirish / chiqish: ")
    if amal == "chiqish":
        break
    elif amal == "qo'shish":
        ism = input("Ism: ")
        raqam = input("Raqam: ")
        kitobcha[ism] = raqam
    elif amal == "qidirish":
        ism = input("Ism: ")
        print(kitobcha.get(ism, "topilmadi"))
```

</details>

<details markdown="1">
<summary>Masala 21</summary>

```python
sozlar = ["olma", "non", "banan"]
uzunliklar = {s: len(s) for s in sozlar}
print(uzunliklar)         # {'olma': 4, 'non': 3, 'banan': 5}
```

</details>

<details markdown="1">
<summary>Masala 22</summary>

```python
nomlar = ["olma", "non", "go'sht"]
narxlar = [12000, 4000, 90000]

katalog = {n: p for n, p in zip(nomlar, narxlar)}
qimmatlar = {n for n, p in katalog.items() if p > 10000}
print(katalog)            # {'olma': 12000, 'non': 4000, "go'sht": 90000}
print(qimmatlar)          # {'olma', "go'sht"}
```

</details>

<details markdown="1">
<summary>Masala 23</summary>

```python
talabalar = [
    {"ism": "Aziz", "ball": 85},
    {"ism": "Malika", "ball": 92},
    {"ism": "Bobur", "ball": 78},
]
tartibli = sorted(talabalar, key=lambda t: t["ball"], reverse=True)
for t in tartibli[:3]:
    print(t["ism"], t["ball"])
# Malika 92
# Aziz 85
# Bobur 78
```

</details>

<details markdown="1">
<summary>Masala 24</summary>

```python
import copy

asl = [[1, 2], [3, 4]]
yuza = asl.copy()
chuqur = copy.deepcopy(asl)

yuza[0].append(99)
print("yuza o'zgartirdi -> asl:", asl)   # [[1, 2, 99], [3, 4]]  -- asl ham o'zgardi!

chuqur[1].append(77)
print("chuqur o'zgartirdi -> asl:", asl) # [[1, 2, 99], [3, 4]]  -- asl tegmadi
print("chuqur:", chuqur)                 # [[1, 2, 99], [3, 4, 77]]
```

</details>

<details markdown="1">
<summary>Masala 25</summary>

```python
guruh_a = {"Aziz", "Malika", "Bobur"}
guruh_b = {"Malika", "Sardor"}

print(guruh_a | guruh_b)   # hamma: {'Aziz', 'Malika', 'Bobur', 'Sardor'}
print(guruh_a & guruh_b)   # ikkalasida: {'Malika'}
print(guruh_a - guruh_b)   # faqat A da: {'Aziz', 'Bobur'}
print(guruh_a ^ guruh_b)   # faqat bittasida: {'Aziz', 'Bobur', 'Sardor'}
```

</details>

<details markdown="1">
<summary>Masala 26</summary>

```python
jami = sum(i * i for i in range(1, 1001))
print(jami)               # 333833500
```

</details>

---

[← Boshqaruv va funksiyalar](./02-boshqaruv-funksiyalar.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Stringlar →](./04-stringlar.md)
