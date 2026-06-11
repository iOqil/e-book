# 19 — Funksional dasturlash (`functools`, `itertools`)

Ma'lumotni qayta ishlashning ikki yo'li bor. Birinchisi — **imperativ** uslub: "avval bo'sh ro'yxat och, keyin sikl bilan aylanib, har bir elementga shu amalni bajar, natijani qo'sh". Ikkinchisi — **funksional** (deklarativ) uslub: "menga shu ro'yxatning har bir elementining kvadratini ber". Birinchisida sen *qanday* qilishni qadam-baqadam aytasan, ikkinchisida *nima* kerakligini aytasan-u, mexanikani Python'ga qoldirasan.

Funksional uslub Python'da ikki kuchli modul orqali ochiladi: **`functools`** (funksiyalar ustida ishlovchi vositalar — keshlash, argumentni qotirish, dekorator yordamchilari) va **`itertools`** (iteratorlar ustida ishlovchi "lego" bloklari — ulash, kesish, kombinatorika, guruhlash). Bu ikkalasi to'g'ri ishlatilganda kod qisqaroq, tezroq va o'qishga osonroq bo'ladi. Bu bobda ularni chuqur, real misollar bilan o'rganamiz.

> **Bu modulda:** funksiya — birinchi sinf obyekt, `lambda`, `map`/`filter` (va comprehension afzalligi); `functools` (`reduce`, `partial`, `wraps`, `cache`/`lru_cache`, `cached_property`, `total_ordering`, `singledispatch`); `itertools` (cheksiz iteratorlar, `chain`, `islice`, kombinatorika, `groupby`, `accumulate`, `pairwise`/`batched` va boshqalar); `operator` moduli; hamda lazy (dangasa) pipeline.

---

## 19.1 Funksiya — birinchi sinf obyekt (eslatma)

Python'da funksiya — oddiy qiymat, xuddi son yoki string kabi. Uni o'zgaruvchiga berib bo'ladi, ro'yxatga solib bo'ladi, boshqa funksiyaga argument sifatida uzatib bo'ladi va funksiyadan qaytarib bo'ladi. Buni **"birinchi sinf obyekt"** deyiladi. Funksional dasturlashning butun asosi shu tushunchada yotadi.

Tasavvur qil: funksiya — bu "asbob". Asbobni qutiga solib, boshqa ustaga uzatib, kerak bo'lganda ishga solishing mumkin. Funksiyani **chaqirmasdan** (qavssiz) yozsang — uni shunchaki uzatasan; qavs (`()`) qo'ysang — ishga tushirasan.

```python
def kvadrat(x):
    return x * x

amal = kvadrat          # qavssiz — funksiyaning o'zini berdik, chaqirmadik
print(amal(5))          # 25  — endi amal orqali chaqiramiz

# Funksiyani boshqa funksiyaga uzatish
def qolla(f, qiymat):
    return f(qiymat)    # f — funksiya, uni ishlatamiz

print(qolla(kvadrat, 9))    # 81
```

Funksiyalarni ro'yxatga solib, ketma-ket ishlatish ham mumkin:

```python
amallar = [str.upper, str.strip, str.title]
matn = "  salom dunyo  "
for a in amallar:
    matn = a(matn)
print(repr(matn))       # 'Salom Dunyo'
```

> **Diqqat:** `kvadrat` — funksiya obyekti, `kvadrat()` — uni chaqirish (natija). Bu ikkalasini chalkashtirma. `map`, `filter`, `sorted(key=...)` kabilarga doim **qavssiz** funksiya beriladi — ular o'zlari ichida chaqiradi.

---

## 19.2 `lambda` — bir qatorlik nomsiz funksiya

Ba'zan funksiya shunchalik kichkina va bir martalik bo'ladiki, unga alohida `def` yozib nom o'ylab topish ortiqcha. Shunda **`lambda`** ishlatasan — bu "yo'l-yo'lakay" yaratiladigan nomsiz funksiya.

Sintaksis: `lambda parametrlar: ifoda`. U faqat **bitta ifoda**dan iborat bo'ladi (sikl, `if` bloki, bir nechta qator yozib bo'lmaydi) va o'sha ifodaning qiymatini avtomatik qaytaradi.

```python
qosh = lambda a, b: a + b
print(qosh(2, 3))       # 5
```

Bu `def qosh(a, b): return a + b` bilan teng. Lekin `lambda`ni o'zgaruvchiga berish odatda yaxshi uslub emas — agar nom kerak bo'lsa, `def` yoz. `lambda`ning haqiqiy kuchi — uni boshqa funksiyaga **joyida** uzatishda. Eng keng tarqalgan misol — `sorted` uchun saralash kaliti:

```python
sonlar = [(1, "b"), (3, "a"), (2, "c")]
sonlar.sort(key=lambda t: t[1])     # ikkinchi element (harf) bo'yicha sarala
print(sonlar)           # [(3, 'a'), (1, 'b'), (2, 'c')]
```

Bu yerda `lambda t: t[1]` har bir tuple uchun "saralashda nimaga qarab solishtiramiz" degan savolga javob beradi — ikkinchi elementga.

> **Qoida:** `lambda` qisqa va aniq bo'lsa ishlat. Agar ichida murakkab mantiq paydo bo'lsa — bu `def` yozish vaqti kelganini bildiradi. O'qiluvchanlik tezlikdan muhim.

---

## 19.3 `map` va `filter` — va nega comprehension afzal

**`map(funksiya, ketma-ketlik)`** — har bir elementga funksiyani qo'llab, yangi qiymatlar oqimini beradi. **`filter(funksiya, ketma-ketlik)`** — faqat funksiya `True` qaytargan elementlarni qoldiradi. Ikkalasi ham **iterator** qaytaradi (lazy — dangasa), shuning uchun natijani ko'rish uchun ko'pincha `list()` ga o'rab olamiz.

```python
narxlar = [100, 250, 75]
soliqli = list(map(lambda n: n + n // 10, narxlar))
print(soliqli)          # [110, 275, 82]

juftlar = list(filter(lambda n: n % 2 == 0, range(10)))
print(juftlar)          # [0, 2, 4, 6, 8]
```

Bu ishlaydi, lekin zamonaviy Python'da ko'pincha **list comprehension** aniqroq va tezroq. Yuqoridagi ikkala satr comprehension bilan shunday yoziladi:

```python
soliqli = [n + n // 10 for n in narxlar]                 # map o'rniga
juftlar = [n for n in range(10) if n % 2 == 0]           # filter o'rniga
print(soliqli, juftlar)     # [110, 275, 82] [0, 2, 4, 6, 8]
```

Comprehension `lambda` yozishni talab qilmaydi, o'qishga ravon va Python jamoasi tomonidan tavsiya etiladi. `map`/`filter` esa ikki holatda hali ham qulay: (1) qo'llaniladigan funksiya **allaqachon mavjud** bo'lsa (yangi `lambda` yozish shart emas), (2) lazy oqim kerak bo'lsa.

```python
print(list(map(str.upper, ["a", "b", "c"])))   # ['A', 'B', 'C'] — tayyor funksiya
```

> **Qoida:** yangi `lambda` yozayotgan bo'lsang — comprehension afzal. Tayyor funksiyani (`str.upper`, `int`, `len`...) qo'llayotgan bo'lsang — `map` toza ko'rinadi.

---

## 19.4 `functools.reduce` — ketma-ketlikni bitta qiymatga yig'ish

`map` va `filter` ketma-ketlikdan ketma-ketlik yasaydi. **`reduce`** esa boshqacha — u butun ketma-ketlikni **bitta qiymatga** "yig'adi" (siqib chiqaradi). U elementlarni ikkitadan olib, oraliq natijani to'plab boradi.

`reduce(funksiya, ketma-ketlik, boshlang'ich)` — `funksiya(akkumulyator, element)` ni har element uchun chaqiradi. Tasavvur qil: qor to'pini dumalatasan — har bir qadamda u kattalashib boradi.

```python
from functools import reduce

# Yig'indi: (((0+1)+2)+3)+4 = 10
print(reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0))      # 10

# Ko'paytma (faktorial): 1*2*3*4*5 = 120
print(reduce(lambda acc, x: acc * x, range(1, 6)))          # 120
```

Bu yerda `acc` — to'plangan natija (akkumulyator), `x` — joriy element. Uchinchi argument (`0`) — boshlang'ich qiymat; berilmasa, birinchi element boshlang'ich bo'lib olinadi.

`reduce` faqat sonlar uchun emas — istalgan "yig'ish" mantiqi uchun ishlaydi:

```python
sozlar = ["Olma", "Banan", "Anor"]
eng_uzun = reduce(lambda a, b: a if len(a) >= len(b) else b, sozlar)
print(eng_uzun)         # Banan
```

> **Muhim:** oddiy yig'indi yoki ko'paytma uchun `sum()`, `max()`, `min()` tayyor funksiyalardan foydalan — ular `reduce`dan tushunarliroq. `reduce`ni faqat tayyor funksiya yo'q bo'lgan maxsus yig'ish holatlarida ishlat.

---

## 19.5 `functools.partial` — argumentni oldindan qotirish

Ba'zan funksiya bor, lekin uning ba'zi argumentlari **doim bir xil** bo'ladi. Har safar o'sha argumentni yozish zerikarli. **`partial`** funksiyaning bir qism argumentlarini "qotirib", yangi, soddalashtirilgan funksiya yasaydi.

Tasavvur qil: kofe mashinasida har safar "shakar 2, sut bor" deb tanlash o'rniga, "mening odatiy kofem" tugmasini yasaysan — qolgan sozlamalar oldindan qotirilgan.

```python
from functools import partial

def kuchaytir(asos, daraja):
    return asos ** daraja

kvadratga = partial(kuchaytir, daraja=2)    # daraja=2 ni qotirdik
kubga = partial(kuchaytir, daraja=3)        # daraja=3 ni qotirdik

print(kvadratga(5))     # 25  — kuchaytir(5, daraja=2)
print(kubga(2))         # 8   — kuchaytir(2, daraja=3)
```

Real misol — `int()` funksiyasi ikkilik (binary) sanoq tizimini o'qishga sozlash:

```python
from functools import partial

ikkilik = partial(int, base=2)
print(ikkilik("1010"))      # 10  — int("1010", base=2)
print(ikkilik("1111"))      # 15
```

`print` kabi funksiyaning birinchi argumentini ham qotirib, maxsus "log" funksiyasi yasash mumkin:

```python
from functools import partial

log_xato = partial(print, "[XATO]")
log_xato("fayl topilmadi")      # [XATO] fayl topilmadi
log_xato("ruxsat yo'q")         # [XATO] ruxsat yo'q
```

> **Foyda:** `partial` `lambda x: kuchaytir(x, 2)` yozishga o'xshaydi, lekin u funksiyaning nomi va metadata'sini saqlaydi va `map`/`callback`'larga uzatishga juda qulay.

---

## 19.6 `@functools.wraps` — dekoratorda metadata saqlash (MUHIM)

Dekorator yozganda (9-bobda ko'rganmiz) bir nozik muammo bor: dekorator ichki funksiya bilan o'rab qaytaradi, va shu sababli **asl funksiyaning nomi, hujjati (`__doc__`) yo'qoladi**. Bu xato izlashda va hujjat yaratishda jiddiy muammo. **`@functools.wraps`** ana shu metadata'ni asl funksiyadan nusxalab, o'rovchiga ko'chiradi.

Avval muammosini ko'raylik (`wraps`'siz):

```python
def jurnal(func):
    def ichki(*args, **kwargs):
        print(f"-> {func.__name__} chaqirildi")
        return func(*args, **kwargs)
    return ichki

@jurnal
def qoshish(a, b):
    "Ikki sonni qo'shadi"
    return a + b

print(qoshish.__name__)     # ichki   — XATO! nom yo'qoldi
print(qoshish.__doc__)      # None     — hujjat ham yo'qoldi
```

Endi `@functools.wraps` qo'shamiz — faqat bitta qator:

```python
import functools

def jurnal(func):
    @functools.wraps(func)          # asl func metadata'sini ko'chiradi
    def ichki(*args, **kwargs):
        print(f"-> {func.__name__} chaqirildi")
        return func(*args, **kwargs)
    return ichki

@jurnal
def qoshish(a, b):
    "Ikki sonni qo'shadi"
    return a + b

print(qoshish(2, 3))        # -> qoshish chaqirildi / 5
print(qoshish.__name__)     # qoshish            — to'g'ri!
print(qoshish.__doc__)      # Ikki sonni qo'shadi — saqlandi!
```

> **Qoida:** dekorator yozsang, ichki funksiyaning ustiga **doim** `@functools.wraps(func)` qo'y. Bu professional kodning belgisi — usiz dekorator funksiya "kim ekanini" yashiradi.

---

## 19.7 `@functools.cache` / `@lru_cache` — memoizatsiya (natijani eslab qolish)

Agar funksiya bir xil argument bilan qayta-qayta chaqirilsa va har safar uzoq hisoblasa — bu isrof. **Memoizatsiya** — natijani birinchi marta hisoblab, eslab qolish; keyingi safar shu argument kelsa, qaytadan hisoblamay, eslab qolingan javobni berish.

**`@functools.cache`** (3.9+) — cheksiz kesh; **`@functools.lru_cache(maxsize=N)`** — eng kam ishlatilganlarni unutadigan (LRU — Least Recently Used) cheklangan kesh.

Klassik misol — Fibonachchi. Keshsiz u eksponensial sekin, kesh bilan — bir zumda:

```python
import functools

@functools.cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))          # 832040  — keshsiz bu juda sekin bo'lar edi
print(fib.cache_info()) # CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
```

`cache_info()` keshning samarasini ko'rsatadi: `hits` — kesh yordam bergan martalar, `misses` — yangi hisoblashlar. Kesh qancha ko'p "hit" bersa, shuncha tejaladi.

`maxsize` bilan kesh hajmini cheklash (xotira muhim bo'lsa):

```python
import functools

@functools.lru_cache(maxsize=2)
def kvadrat(n):
    print(f"  hisoblanyapti {n}")
    return n * n

print(kvadrat(4))       # hisoblanyapti 4 / 16
print(kvadrat(4))       # 16  — "hisoblanyapti" CHIQMAYDI, kesh ishladi
```

> **Diqqat:** kesh faqat **toza** funksiyalar uchun (bir xil kirish — doim bir xil chiqish). Tashqi holatga bog'liq (vaqt, fayl, tasodif) funksiyalarni keshlama. Argumentlar **hashlanuvchi** bo'lishi shart (list emas, tuple bo'lsin).

---

## 19.8 `@functools.cached_property` — bir marta hisoblanuvchi atribut

Klassda shunday atribut bo'ladiki, uni hisoblash qimmat, lekin obyekt umri davomida o'zgarmaydi. Har murojaatda qayta hisoblash isrof. **`@cached_property`** — birinchi o'qishda hisoblab, natijani obyektga saqlaydi; keyingi o'qishlar tayyor qiymatni qaytaradi.

`@property`'dan farqi: `property` har murojaatda qayta hisoblaydi, `cached_property` faqat bir marta.

```python
from functools import cached_property

class Hisobot:
    def __init__(self, sonlar):
        self.sonlar = sonlar

    @cached_property
    def ortacha(self):
        print("  hisoblanyapti...")
        return sum(self.sonlar) / len(self.sonlar)

h = Hisobot([10, 20, 30])
print(h.ortacha)        # hisoblanyapti... / 20.0
print(h.ortacha)        # 20.0  — "hisoblanyapti" CHIQMAYDI, saqlangan qiymat
```

E'tibor ber: `ortacha`ni qavssiz, oddiy atribut kabi o'qiymiz (`h.ortacha`, `h.ortacha()` emas) — bu `property`ning xususiyati.

> **Diqqat:** `cached_property` ma'lumot o'zgarmaydigan holatlar uchun. Agar `self.sonlar` keyin o'zgarsa, `ortacha` eski qiymatda qoladi (qayta hisoblanmaydi). O'zgaruvchan ma'lumotga ishlatma.

---

## 19.9 `@functools.total_ordering` — taqqoslash metodlarini avtomatik to'ldirish

Obyektlarni `<`, `<=`, `>`, `>=` bilan taqqoslamoqchi bo'lsang, odatda to'rtta maxsus metodni yozish kerak (`__lt__`, `__le__`, `__gt__`, `__ge__`). Bu zerikarli va xatoga moyil. **`@total_ordering`** — sen faqat `__eq__` va bittagina taqqoslash (`__lt__`) yozasan, qolganini Python **o'zi to'ldiradi**.

```python
from functools import total_ordering

@total_ordering
class Pul:
    def __init__(self, miqdor):
        self.miqdor = miqdor

    def __eq__(self, other):
        return self.miqdor == other.miqdor

    def __lt__(self, other):
        return self.miqdor < other.miqdor

    def __repr__(self):
        return f"Pul({self.miqdor})"

print(Pul(10) < Pul(20))    # True
print(Pul(30) >= Pul(20))   # True  — biz __ge__ yozmadik, avtomatik keldi
print(sorted([Pul(30), Pul(10), Pul(20)]))   # [Pul(10), Pul(20), Pul(30)]
```

Faqat `__eq__` va `__lt__` yozdik, ammo `>=`, `>`, `<=` ham ishlayapti va `sorted` ham. Bu — `total_ordering`ning sehri.

> **Foyda:** kamroq kod, kamroq xato. Mayda tezlik kerak bo'lsa to'rtta metodni qo'lda yozasan, ammo aksariyat hollarda `total_ordering` yetarli va toza.

---

## 19.10 `@functools.singledispatch` — tip bo'yicha "overload"

Ba'zi tillarda bir funksiyaning bir nechta versiyasi bo'ladi — argument turiga qarab mosi tanlanadi (overloading). Python'da `if isinstance(...)` zanjiri yozish o'rniga **`@singledispatch`** ishlatasan: bitta umumiy funksiya yozasan, keyin har bir tur uchun alohida versiyani ro'yxatdan o'tkazasan. Python **birinchi argument turiga** qarab mosini tanlaydi.

```python
from functools import singledispatch

@singledispatch
def tavsifla(arg):
    return f"Noma'lum tur: {arg!r}"     # standart (default) holat

@tavsifla.register
def _(arg: int):
    return f"Butun son: {arg}"

@tavsifla.register
def _(arg: str):
    return f"Matn, {len(arg)} ta belgi"

@tavsifla.register
def _(arg: list):
    return f"Ro'yxat, {len(arg)} ta element"

print(tavsifla(42))         # Butun son: 42
print(tavsifla("salom"))    # Matn, 5 ta belgi
print(tavsifla([1, 2, 3]))  # Ro'yxat, 3 ta element
print(tavsifla(3.14))       # Noma'lum tur: 3.14  — standart versiya
```

Har bir versiyaning nomi `_` (chunki nomi ahamiyatsiz — Python ularni tur bo'yicha topadi). Tur annotatsiyasi (`arg: int`) qaysi versiya qaysi turga mosligini belgilaydi. Mos versiya topilmasa — eng birinchi (default) ishlaydi.

> **Qachon kerak?** Bir amalni turli ma'lumot turlariga turlicha bajarganda (masalan, JSON serializatsiya, formatlash, chizish). `isinstance` zanjiridan tozaroq va kengaytirishga oson — yangi tur uchun shunchaki yangi `register` qo'shasan.

---

## 19.11 `itertools`: cheksiz iteratorlar — `count`, `cycle`, `repeat`

Endi **`itertools`** moduliga o'tamiz. U iteratorlarni yasash va ulardan "lego" kabi murakkab oqimlar qurish uchun. Birinchi guruh — **cheksiz** iteratorlar. Ular cheksiz qiymat berishi mumkin, shuning uchun ularni doim **cheklab** ishlatamiz (`islice`, `next`, yoki shartli `break` bilan) — aks holda dastur to'xtamaydi.

- **`count(boshlanish, qadam)`** — cheksiz sanaydi: `boshlanish, +qadam, +qadam, ...`
- **`cycle(ketma-ketlik)`** — ketma-ketlikni cheksiz aylantiradi.
- **`repeat(qiymat, marta)`** — qiymatni takrorlaydi (`marta` berilmasa cheksiz).

```python
from itertools import count, cycle, repeat, islice

hisoblagich = count(10, 2)          # 10, 12, 14, ...
print([next(hisoblagich) for _ in range(4)])    # [10, 12, 14, 16]

ranglar = cycle(["qizil", "yashil"])            # qizil, yashil, qizil, ...
print([next(ranglar) for _ in range(5)])
# ['qizil', 'yashil', 'qizil', 'yashil', 'qizil']

print(list(repeat("x", 3)))         # ['x', 'x', 'x']
print(list(islice(count(), 5)))     # [0, 1, 2, 3, 4]  — cheksizdan 5 ta
```

`count` ko'pincha `enumerate` o'rnini bosadi yoki `zip` bilan birga "raqamli yorliq" qo'shish uchun ishlatiladi. `cycle` esa navbatlash (masalan, jadval qatorlariga galma-gal rang berish) uchun ajoyib.

> **Eslatma:** cheksiz iteratorni hech qachon `list()` ga to'g'ridan-to'g'ri o'rama — dastur xotirani to'ldirib qotib qoladi. Doim `islice` yoki shart bilan cheklab ol.

---

## 19.12 `chain` — bir nechta ketma-ketlikni ulash

**`chain`** bir nechta ketma-ketlikni **ketma-ket ulab**, bitta uzluksiz oqimga aylantiradi. `+` operatori bilan ro'yxatlarni qo'shishga o'xshaydi, lekin `chain` lazy (yangi katta ro'yxat yasamaydi) va istalgan iteratsiyalanuvchi bilan ishlaydi.

```python
from itertools import chain

a = [1, 2]
b = [3, 4]
c = [5]
print(list(chain(a, b, c)))     # [1, 2, 3, 4, 5]
```

Ichma-ich ro'yxatni (matrisani) bitta tekis oqimga "yoyish" uchun **`chain.from_iterable`** juda qulay:

```python
from itertools import chain

matrisa = [[1, 2], [3, 4], [5]]
print(list(chain.from_iterable(matrisa)))    # [1, 2, 3, 4, 5]
```

> **Foyda:** `chain` katta ma'lumotlarni xotirada nusxalamasdan ketma-ket qayta ishlashga imkon beradi — masalan, bir nechta faylning satrlarini bittadek aylanish.

---

## 19.13 `islice` — iteratorni kesish (lazy slicing)

Ro'yxatni `[2:5]` bilan kesamiz, lekin bu iterator yoki generatorda ishlamaydi. **`islice`** ana shu uchun — istalgan iteratorni kesadi, lazy holda. `islice(iterator, stop)` yoki `islice(iterator, start, stop, step)`.

```python
from itertools import islice, count

katta = range(100)
print(list(islice(katta, 5)))           # [0, 1, 2, 3, 4]  — birinchi 5 ta
print(list(islice(katta, 5, 10)))       # [5, 6, 7, 8, 9]  — 5..9
print(list(islice(katta, 0, 20, 5)))    # [0, 5, 10, 15]   — har 5-chi

# Cheksiz iteratordan ham kesib olish mumkin:
print(list(islice(count(), 3)))         # [0, 1, 2]
```

`islice` manfiy indekslarni (`-1`) qo'llab-quvvatlamaydi — chunki u oxirini oldindan bilmaydi (iterator cheksiz bo'lishi mumkin). Bu — lazy ishlashning tabiiy cheklovi.

> **Foyda:** generatordan "birinchi N ta natija" olish, yoki katta fayldan faqat ma'lum oraliqdagi satrlarni o'qish uchun ideal — hammasini xotiraga yuklamasdan.

---

## 19.14 Kombinatorika: `product`, `permutations`, `combinations`

Bu uchlik — sanash (kombinatorika) masalalari uchun. Ular ichma-ich sikllar yozishni keskin qisqartiradi.

- **`product(A, B)`** — Dekart ko'paytmasi: A va B ning barcha juftliklari (ichma-ich sikl).
- **`permutations(A, n)`** — n ta elementdan tartibga sezgir terishlar (o'rin almashtirish muhim).
- **`combinations(A, n)`** — n ta elementdan tartibga befarq terishlar (tanlash, tartib muhim emas).
- **`combinations_with_replacement(A, n)`** — element takrorlanishiga ruxsat berilgan terishlar.

```python
from itertools import product, permutations, combinations, combinations_with_replacement

print(list(product([1, 2], ["a", "b"])))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

print(list(permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]  — (1,2) va (2,1) HAR IKKALASI

print(list(combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]  — (1,2) bor, (2,1) YO'Q (tartib muhim emas)

print(list(combinations_with_replacement([1, 2], 2)))
# [(1, 1), (1, 2), (2, 2)]  — takror ruxsat: (1,1) ham bor
```

Real misol: ikkita zarning barcha mumkin natijalari — `product`:

```python
from itertools import product

zarlar = list(product(range(1, 7), repeat=2))
print(len(zarlar))      # 36  — barcha juftliklar
print(zarlar[:3])       # [(1, 1), (1, 2), (1, 3)]
```

> **Eslatma:** `repeat=n` argumenti `product`ni "o'zini o'ziga ko'paytirish"ga aytadi — masalan barcha 4 xonali PIN kodlar: `product(range(10), repeat=4)`.

---

## 19.15 `groupby` — ketma-ket elementlarni guruhlash

**`groupby`** ketma-ketlikni guruhlarga ajratadi — bir xil kalitga ega **qo'shni** elementlarni birlashtiradi. Eng muhim nozik nuqta: u faqat **yonma-yon** turgan elementlarni guruhlaydi, shuning uchun deyarli doim avval **shu kalit bo'yicha saralash** kerak.

```python
from itertools import groupby
from operator import itemgetter

data = [
    {"shahar": "Toshkent", "ism": "Ali"},
    {"shahar": "Toshkent", "ism": "Vali"},
    {"shahar": "Samarqand", "ism": "Guli"},
]

data.sort(key=itemgetter("shahar"))     # MUHIM: avval saralaymiz!
for shahar, guruh in groupby(data, key=itemgetter("shahar")):
    ismlar = [d["ism"] for d in guruh]
    print(shahar, ismlar)
# Samarqand ['Guli']
# Toshkent ['Ali', 'Vali']
```

`groupby` har bir guruh uchun `(kalit, guruh_iteratori)` juftligini beradi. `guruh` — bir martalik iterator: uni o'qib bo'lgach yana o'qib bo'lmaydi, shuning uchun darhol `list()` ga yig'amiz.

> **Eng tez-tez qilinadigan xato:** saralamasdan `groupby` ishlatish. Agar ma'lumot saralanmagan bo'lsa, bir xil kalit bir nechta alohida guruhga bo'linib ketadi. Doim `sort(key=...)` ni `groupby(..., key=...)` bilan bir xil kalitda qil.

---

## 19.16 `zip_longest` — turli uzunlikdagi ketma-ketliklarni ulash

Oddiy `zip` eng qisqa ketma-ketlikda to'xtaydi — ortiqcha elementlar yo'qoladi. **`zip_longest`** esa eng uzuniga qarab ishlaydi, yetishmagan joylarni `fillvalue` bilan to'ldiradi.

```python
from itertools import zip_longest

ismlar = ["Ali", "Vali", "Guli"]
ballar = [90, 85]               # bittasi kam!

print(list(zip(ismlar, ballar)))
# [('Ali', 90), ('Vali', 85)]   — Guli yo'qoldi!

print(list(zip_longest(ismlar, ballar, fillvalue=0)))
# [('Ali', 90), ('Vali', 85), ('Guli', 0)]  — Guli saqlandi, bali 0
```

> **Foyda:** ma'lumot to'liq emasligini bilgan holatlarda (masalan, ustunlar uzunligi har xil jadval) hech narsani yo'qotmasdan ishlash uchun.

---

## 19.17 `accumulate` — to'planib boruvchi natijalar

`reduce` faqat **oxirgi** yig'ilgan qiymatni qaytaradi. **`accumulate`** esa **har bir qadamdagi** oraliq natijani ham beradi — "running total" (yugurib boruvchi yig'indi). Standart amal — qo'shish, lekin istalgan ikki argumentli funksiyani berish mumkin.

```python
from itertools import accumulate
import operator

print(list(accumulate([1, 2, 3, 4])))
# [1, 3, 6, 10]  — 1, 1+2, 1+2+3, 1+2+3+4

print(list(accumulate([1, 2, 3, 4], operator.mul)))
# [1, 2, 6, 24]  — running ko'paytma (faktoriallar)

print(list(accumulate([3, 1, 4, 1, 5], max)))
# [3, 3, 4, 4, 5]  — shu paytgacha ko'rilgan eng katta (running max)
```

> **Real foyda:** bank hisobidagi har kunlik balans tarixi, savatdagi narxlarning to'planib borishi, yoki grafik chizish uchun kumulativ ma'lumot — bularning barchasi `accumulate` bilan bir qatorda.

---

## 19.18 `pairwise` (3.10) va `batched` (3.12) — yangi va foydali

Bu ikki vosita yangi Python'da qo'shilgan va kundalik ishda juda asqotadi.

**`pairwise`** — ketma-ketlikdan ketma-ket **qo'shni juftliklarni** beradi. Ayirma, o'sish, masofa hisoblashda ideal:

```python
from itertools import pairwise

print(list(pairwise([1, 2, 3, 4])))
# [(1, 2), (2, 3), (3, 4)]

# Misol: kunlar orasidagi harorat o'zgarishi
haror = [20, 23, 19, 25]
ozgarish = [b - a for a, b in pairwise(haror)]
print(ozgarish)         # [3, -4, 6]
```

**`batched`** — ketma-ketlikni teng o'lchamli **bo'laklarga** (batch) ajratadi. Oxirgi bo'lak to'liq bo'lmasligi mumkin:

```python
from itertools import batched

print(list(batched([1, 2, 3, 4, 5], 2)))
# [(1, 2), (3, 4), (5,)]  — oxirgisi bittagina

# Misol: 7 ta elementni 3 talik sahifalarga bo'lish
elementlar = list(range(1, 8))
for sahifa in batched(elementlar, 3):
    print(sahifa)
# (1, 2, 3) / (4, 5, 6) / (7,)
```

> **Foyda:** `batched` API'ga ma'lumotni partiyalab yuborish, sahifalash, yoki katta vazifani bo'laklarga bo'lishda ajoyib — ilgari buni qo'lda sikl bilan yozish kerak edi.

---

## 19.19 `takewhile`, `dropwhile`, `filterfalse` — shartli kesish

Bu uchlik shart asosida ketma-ketlikni filtrlaydi, lekin `filter`dan farqli mantiq bilan:

- **`takewhile(shart, ketma-ketlik)`** — shart `True` bo'lguncha elementlarni **oladi**, birinchi `False`'da to'xtaydi.
- **`dropwhile(shart, ketma-ketlik)`** — shart `True` bo'lgan boshlang'ich elementlarni **tashlaydi**, birinchi `False`'dan keyin hammasini oladi.
- **`filterfalse(shart, ketma-ketlik)`** — `filter`ning teskarisi: shart `False` bo'lganlarni qoldiradi.

```python
from itertools import takewhile, dropwhile, filterfalse

sonlar = [1, 3, 5, 8, 9, 2]

print(list(takewhile(lambda x: x % 2 == 1, sonlar)))
# [1, 3, 5]  — toqlar tugaguncha oladi, 8'da to'xtaydi

print(list(dropwhile(lambda x: x % 2 == 1, sonlar)))
# [8, 9, 2]  — boshidagi toqlarni tashlaydi, 8'dan boshlab hammasi

print(list(filterfalse(lambda x: x % 2 == 0, range(10))))
# [1, 3, 5, 7, 9]  — juft EMASlar, ya'ni toqlar
```

`takewhile`/`dropwhile`ning `filter`'dan farqi: ular **birinchi shart buzilishida** mantiqni o'zgartiradi (oladi/tashlaydi), `filter` esa har elementni alohida tekshiradi.

> **Real misol:** saralangan ma'lumotda "ma'lum chegaragacha bo'lganlarni ol" (`takewhile`) — bu butun ro'yxatni aylanishdan tezroq, chunki chegarada to'xtaydi.

---

## 19.20 `operator` moduli — `itemgetter` va `attrgetter`

Saralashda `key=lambda x: x[1]` yoki `key=lambda o: o.yosh` ko'p yoziladi. **`operator`** moduli shu uchun tayyor, tezroq va o'qishga toza funksiyalar beradi: **`itemgetter`** (indeks/kalit bo'yicha) va **`attrgetter`** (atribut bo'yicha).

```python
from operator import itemgetter, attrgetter

odamlar = [("Ali", 30), ("Vali", 25), ("Guli", 35)]
print(sorted(odamlar, key=itemgetter(1)))       # yosh (1-indeks) bo'yicha
# [('Vali', 25), ('Ali', 30), ('Guli', 35)]
```

`attrgetter` — obyekt atributi bo'yicha:

```python
from operator import attrgetter

class Inson:
    def __init__(self, ism, yosh):
        self.ism = ism
        self.yosh = yosh
    def __repr__(self):
        return self.ism

insonlar = [Inson("Ali", 30), Inson("Vali", 25)]
print(sorted(insonlar, key=attrgetter("yosh")))     # [Vali, Ali]
```

`itemgetter` bir nechta indeks ham olishi mumkin — natija tuple bo'ladi (ko'p mezonli saralashda zo'r):

```python
from operator import itemgetter

ikki = itemgetter(0, 2)
print(ikki(["a", "b", "c", "d"]))   # ('a', 'c')

# Ko'p mezon: avval shahar, keyin yosh bo'yicha
xodimlar = [("Toshkent", 30), ("Andijon", 25), ("Toshkent", 22)]
print(sorted(xodimlar, key=itemgetter(0, 1)))
# [('Andijon', 25), ('Toshkent', 22), ('Toshkent', 30)]
```

> **Foyda:** `itemgetter`/`attrgetter` `lambda`'dan tezroq (C'da yozilgan) va niyatni aniqroq bildiradi. `groupby` va `sorted` bilan birga doimiy hamroh.

---

## 19.21 Funksional vs imperativ uslub

Bir vazifani ikki uslubda yozib, farqni ko'raylik: "uzunligi 3 dan katta so'zlarni olib, uzunligi bo'yicha sarala".

**Imperativ** (qadam-baqadam, qanday qilishni aytadi):

```python
words = ["apple", "fig", "banana", "kiwi"]
natija = []
for w in words:
    if len(w) > 3:
        natija.append(w)
natija.sort(key=len)
print(natija)           # ['kiwi', 'apple', 'banana']
```

**Funksional** (nima kerakligini aytadi):

```python
words = ["apple", "fig", "banana", "kiwi"]
natija = sorted(filter(lambda w: len(w) > 3, words), key=len)
print(natija)           # ['kiwi', 'apple', 'banana']
```

Funksional uslub qisqaroq va "yon ta'sir"siz (oraliq o'zgaruvchilarni o'zgartirmaydi). Lekin har doim ham yaxshiroq emas: agar mantiq murakkablashsa, imperativ (yoki comprehension) o'qishga osonroq bo'lishi mumkin. **Eng yaxshi kod — eng o'qiluvchan kod.**

> **Tavsiya:** comprehension — Python'da "oltin o'rta": funksional uslubning tozaligini imperativning o'qiluvchanligi bilan birlashtiradi. `[w for w in words if len(w) > 3]` ko'pincha eng yaxshi tanlov.

---

## 19.22 Lazy pipeline — generator va `itertools` birga

`itertools`ning eng kuchli tomoni — vositalarni **quvur (pipeline)** kabi ulab, **lazy** (dangasa) ishlatish. Har bir bosqich faqat keyingisi so'raganda hisoblaydi — shuning uchun **cheksiz** yoki **juda katta** ma'lumotni ham xotirani to'ldirmasdan qayta ishlash mumkin.

Misol: 1, 2, 3, ... cheksiz oqimdan **juft sonlarning kvadratlari**ni olib, birinchi 5 tasini chiqaramiz:

```python
from itertools import islice

def sonlar_oqimi():         # cheksiz generator
    n = 1
    while True:
        yield n
        n += 1

# Pipeline: oqim -> faqat juftlar -> kvadrat
quvur = (x * x for x in sonlar_oqimi() if x % 2 == 0)

print(list(islice(quvur, 5)))   # [4, 16, 36, 64, 100]
```

Bu yerda hech narsa oldindan to'liq hisoblanmaydi: `islice` faqat 5 ta natija so'raydi, shuning uchun `sonlar_oqimi` ham faqat kerakligicha ishlaydi. Cheksiz oqim bo'lsa-da, dastur darhol javob beradi.

Yana bir ko'p bosqichli misol — katta ma'lumotni bosqichma-bosqich qayta ishlash:

```python
from itertools import islice, count

# count'dan -> 3 ga bo'linadiganlar -> +1 -> birinchi 4 ta
quvur = (n + 1 for n in count(1) if n % 3 == 0)
print(list(islice(quvur, 4)))   # [4, 7, 10, 13]
```

> **Asosiy g'oya:** generator ifodalari + `itertools` = xotira-tejamkor, cheksiz oqim bilan ishlay oladigan ma'lumot quvuri. Katta fayllar, oqim (stream) ma'lumotlar, yoki cheksiz ketma-ketliklar bilan ishlashning eng to'g'ri yo'li.

---

## ✍️ Masalalar (20 ta)

> Bu masalalar shu modul mavzulariga asoslangan: `map`/`filter`/`reduce`, `partial`, `itertools`, `operator`, `singledispatch`, `groupby` va lazy pipeline.

**Oson (1–7):**

1. `map` ishlatib, `[1, 2, 3, 4]` ro'yxatining har bir sonining kvadratini hisoblab, ro'yxat qaytar.
2. `filter` ishlatib, `[-2, 3, -1, 5, 0]` dan faqat musbat sonlarni ajrat.
3. `functools.reduce` ishlatib, `[1, 2, 3, 4, 5]` sonlarning ko'paytmasini topib (`operator.mul` bilan).
4. `functools.partial` ishlatib, "har doim 10 ga ko'paytiruvchi" funksiya yasab, uni `5` ga qo'lla.
5. `map` va `filter` ni birga ishlatib, 1 dan 10 gacha sonlardan **juftlarning kvadratlarini** ol.
6. `reduce` ishlatib, `[3, 7, 2, 9, 4]` dan eng katta sonni top (`max`siz, `lambda` bilan).
7. `partial` ishlatib, `print`ning birinchi argumentini `"[XATO]"` ga qotirgan `xato` funksiyasi yasab, biror xabar chiqar.

**O'rta (8–14):**

8. `itertools.chain` ishlatib, uchta ro'yxatni (`[1,2]`, `[3,4]`, `[5,6]`) bitta ro'yxatga ula.
9. `itertools.islice` va `itertools.count` ishlatib, 1 dan boshlanuvchi cheksiz oqimdan birinchi 5 sonni ol.
10. `itertools.product` ishlatib, `"AB"` harflaridan 2 belgili barcha kombinatsiyalarni (takror bilan) yasa (`repeat=2`).
11. `operator.itemgetter` ishlatib, `[("olma", 3000), ("non", 1500), ("sut", 8000)]` ro'yxatini **narx** bo'yicha sarala.
12. `itertools.combinations` ishlatib, `["a", "b", "c"]` dan barcha 2 elementli terishlarni chiqar.
13. `itertools.accumulate` ishlatib, `[10, 20, 30, 40]` uchun to'planib boruvchi yig'indini chiqar.
14. `itertools.zip_longest` ishlatib, `[1, 2, 3]` va `["a", "b"]` ni ula, yetishmaganini `"?"` bilan to'ldir.

**Murakkab (15–20):**

15. `itertools.takewhile` va `dropwhile` ishlatib, `[2, 4, 6, 7, 8]` dan boshidagi juftlarni alohida, qolganini alohida ol.
16. `functools.singledispatch` ishlatib, `hajm(x)` funksiyasi yas: `int` uchun sonning o'zini, `str` va `list` uchun uzunligini qaytarsin.
17. `itertools.groupby` ishlatib, `["it", "uy", "olma", "non", "anor"]` so'zlarini **uzunligi** bo'yicha guruhla (avval saralashni unutma).
18. `functools.cache` ishlatib, rekursiv Fibonachchi funksiyasini yoz va `fib(40)` ni hisobla.
19. Cheksiz generator va `islice` ishlatib, 3 ga bo'linadigan sonlarning kvadratlaridan birinchi 4 tasini ol (lazy pipeline).
20. To'liq pipeline: sotuvlar ro'yxati (`[{"kategoriya": ..., "summa": ...}, ...]`) berilgan. `itemgetter` bilan saralab, `groupby` bilan kategoriyaga guruhlab, har guruh uchun `reduce` bilan umumiy summani hisobla.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Masala 1</summary>

```python
print(list(map(lambda x: x ** 2, [1, 2, 3, 4])))   # [1, 4, 9, 16]
```
</details>

<details markdown="1">
<summary>Masala 2</summary>

```python
print(list(filter(lambda x: x > 0, [-2, 3, -1, 5, 0])))   # [3, 5]
```
</details>

<details markdown="1">
<summary>Masala 3</summary>

```python
from functools import reduce
from operator import mul
print(reduce(mul, [1, 2, 3, 4, 5]))     # 120
```
</details>

<details markdown="1">
<summary>Masala 4</summary>

```python
from functools import partial
kopaytir = partial(lambda a, b: a * b, 10)   # birinchi argument 10 ga qotirildi
print(kopaytir(5))      # 50
```
</details>

<details markdown="1">
<summary>Masala 5</summary>

```python
sonlar = range(1, 11)
natija = map(lambda x: x * x, filter(lambda x: x % 2 == 0, sonlar))
print(list(natija))     # [4, 16, 36, 64, 100]
```
</details>

<details markdown="1">
<summary>Masala 6</summary>

```python
from functools import reduce
print(reduce(lambda a, b: a if a > b else b, [3, 7, 2, 9, 4]))   # 9
```
</details>

<details markdown="1">
<summary>Masala 7</summary>

```python
from functools import partial
xato = partial(print, "[XATO]")
xato("xabar")           # [XATO] xabar
```
</details>

<details markdown="1">
<summary>Masala 8</summary>

```python
from itertools import chain
print(list(chain([1, 2], [3, 4], [5, 6])))   # [1, 2, 3, 4, 5, 6]
```
</details>

<details markdown="1">
<summary>Masala 9</summary>

```python
from itertools import islice, count
print(list(islice(count(1), 5)))    # [1, 2, 3, 4, 5]
```
</details>

<details markdown="1">
<summary>Masala 10</summary>

```python
from itertools import product
print(list(product("AB", repeat=2)))
# [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]
```
</details>

<details markdown="1">
<summary>Masala 11</summary>

```python
from operator import itemgetter
mahsulot = [("olma", 3000), ("non", 1500), ("sut", 8000)]
print(sorted(mahsulot, key=itemgetter(1)))
# [('non', 1500), ('olma', 3000), ('sut', 8000)]
```
</details>

<details markdown="1">
<summary>Masala 12</summary>

```python
from itertools import combinations
print(list(combinations(["a", "b", "c"], 2)))
# [('a', 'b'), ('a', 'c'), ('b', 'c')]
```
</details>

<details markdown="1">
<summary>Masala 13</summary>

```python
from itertools import accumulate
print(list(accumulate([10, 20, 30, 40])))   # [10, 30, 60, 100]
```
</details>

<details markdown="1">
<summary>Masala 14</summary>

```python
from itertools import zip_longest
print(list(zip_longest([1, 2, 3], ["a", "b"], fillvalue="?")))
# [(1, 'a'), (2, 'b'), (3, '?')]
```
</details>

<details markdown="1">
<summary>Masala 15</summary>

```python
from itertools import takewhile, dropwhile
data = [2, 4, 6, 7, 8]
print(list(takewhile(lambda x: x % 2 == 0, data)))   # [2, 4, 6]
print(list(dropwhile(lambda x: x % 2 == 0, data)))   # [7, 8]
```
</details>

<details markdown="1">
<summary>Masala 16</summary>

```python
from functools import singledispatch

@singledispatch
def hajm(x):
    raise TypeError("qo'llab-quvvatlanmaydi")

@hajm.register
def _(x: int):
    return x

@hajm.register
def _(x: str):
    return len(x)

@hajm.register
def _(x: list):
    return len(x)

print(hajm(5), hajm("salom"), hajm([1, 2, 3]))   # 5 5 3
```
</details>

<details markdown="1">
<summary>Masala 17</summary>

```python
from itertools import groupby
sozlar = ["it", "uy", "olma", "non", "anor"]
sozlar.sort(key=len)        # MUHIM: avval uzunlik bo'yicha saralaymiz
for uzunlik, guruh in groupby(sozlar, key=len):
    print(uzunlik, list(guruh))
# 2 ['it', 'uy']
# 3 ['non']
# 4 ['olma', 'anor']
```
</details>

<details markdown="1">
<summary>Masala 18</summary>

```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(40))      # 102334155
```
</details>

<details markdown="1">
<summary>Masala 19</summary>

```python
from itertools import islice

def cheksiz():
    n = 1
    while True:
        yield n
        n += 1

quvur = (x ** 2 for x in cheksiz() if x % 3 == 0)
print(list(islice(quvur, 4)))   # [9, 36, 81, 144]
```
</details>

<details markdown="1">
<summary>Masala 20</summary>

```python
from functools import reduce
from itertools import groupby
from operator import itemgetter

sotuvlar = [
    {"kategoriya": "meva", "summa": 100},
    {"kategoriya": "ichimlik", "summa": 50},
    {"kategoriya": "meva", "summa": 200},
    {"kategoriya": "ichimlik", "summa": 30},
]

sotuvlar.sort(key=itemgetter("kategoriya"))     # groupby uchun saralash shart
for kat, guruh in groupby(sotuvlar, key=itemgetter("kategoriya")):
    jami = reduce(lambda acc, d: acc + d["summa"], guruh, 0)
    print(kat, jami)
# ichimlik 80
# meva 300
```
</details>

---

[← Type hints — chuqur](./18-typing-chuqur.md) | [Boshlovchilar README ↑](./README.md)
