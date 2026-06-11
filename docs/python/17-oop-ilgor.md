# 17 — OOP — ilg'or (property, dunder, dataclass)

05-bobda klass, `__init__`, metod va merosni ko'rdik — bu OOP'ning poydevori. Lekin professional kodda klasslar shunchaki "ma'lumot qutisi" emas: ular o'zini xuddi Python'ning tug'ma turlari (`int`, `list`, `dict`) kabi tutadi. Sening obyekting ham `+` bilan qo'shilsin, `==` bilan solishtirilsin, `len()` ishlasin, `for` bilan aylansin, atributga noto'g'ri qiymat berilsa esa shartta xato qaytarsin. Bu bobda obyektni "tirik" qiladigan vositalarni — `@property`, dunder (sehrli) metodlar, `@dataclass`, `Enum`, ABC va merosning chuqur qoidalarini — to'liq o'rganamiz.

> **Bu modulda:** `@property`/setter/deleter bilan boshqariladigan atribut va validatsiya; `@classmethod` (alternativ konstruktor) va `@staticmethod`; klass vs instance atributi; inkapsulyatsiya (`_himoyalangan`, `__mangling`); dunder metodlar chuqur (`__repr__`/`__str__`, `__eq__`/`__hash__`, taqqoslash + `@total_ordering`, `__len__`/`__getitem__`/`__contains__`/`__iter__`, `__call__`, operator overloading, `__enter__`/`__exit__`); `@dataclass` (`field`, `frozen`, `slots`, `kw_only`); `Enum`/`IntEnum`; `NamedTuple`; `ABC`/`@abstractmethod`; ko'p meros, MRO va mixin; `__slots__`; kompozitsiya vs meros; `match/case` bilan klass patterni.

---

## 17.1 `@property` — atributga o'xshagan metod

05-bobda atributga to'g'ridan-to'g'ri qiymat berardik: `t.yosh = 20`. Muammo shuki, hech kim `t.yosh = -5` deb yozishga to'sqinlik qilmaydi. Bizga **boshqariladigan atribut** kerak: tashqaridan oddiy atributga o'xshaydi, lekin ichida tekshiruv (validatsiya) bor.

`@property` aynan shu — metodni atribut kabi (qavssiz) o'qishga imkon beradi:

```python
class Doira:
    def __init__(self, radius: float):
        self.radius = radius

    @property
    def yuza(self) -> float:           # metod, lekin atribut kabi o'qiladi
        return 3.14159 * self.radius ** 2

d = Doira(5)
print(d.yuza)          # 78.53975   — qavssiz! d.yuza() emas
```

`yuza` har safar o'qilganda **qayta hisoblanadi** — `radius` o'zgarsa, `yuza` ham yangilanadi. Bu "hisoblanuvchi atribut" (computed property): tashqaridan oddiy ma'lumotga o'xshaydi, ichida esa hisob ketadi.

> **Qachon `@property`?** Atribut o'qilganda biror hisob/tekshiruv kerak bo'lsa. Avval oddiy atribut yoz; keyinroq nazorat kerak bo'lsa, kodni buzmasdan `@property` ga aylantirasan — chaqiruvchi `d.yuza` ni o'zgartirmasdan ishlayveradi.

---

## 17.2 setter — qiymat o'rnatishni nazorat qilish

Faqat o'qish kam — ko'pincha **yozishni** ham tekshirmoqchimiz. `@<nom>.setter` qiymat o'rnatilganda ishlaydigan metodni belgilaydi:

```python
class Harorat:
    def __init__(self, selsiy: float):
        self.selsiy = selsiy          # bu setter'ni chaqiradi (validatsiya bor)

    @property
    def selsiy(self) -> float:
        return self._selsiy           # haqiqiy qiymat _selsiy da saqlanadi

    @selsiy.setter
    def selsiy(self, qiymat: float) -> None:
        if qiymat < -273.15:
            raise ValueError("Mutlaq noldan past bo'lishi mumkin emas")
        self._selsiy = qiymat

h = Harorat(25)
print(h.selsiy)        # 25
h.selsiy = 30          # setter ishlaydi, tekshiruvdan o'tadi
print(h.selsiy)        # 30
```

Endi noto'g'ri qiymat berib bo'lmaydi:

```python
h.selsiy = -300        # ValueError: Mutlaq noldan past bo'lishi mumkin emas
```

> **Diqqat — nega `_selsiy`?** Tashqi nom `selsiy` (property), ichki saqlash joyi `_selsiy`. Agar setter ichida `self.selsiy = qiymat` deb yozsang, setter o'zini-o'zi cheksiz chaqiradi (rekursiya). Shuning uchun haqiqiy qiymatni boshqa nomli (`_selsiy`) "yashirin" atributda saqlaymiz.

Property orqali bog'liq qiymatlarni ham hisoblash mumkin — masalan Farengeyt selsiydan kelib chiqadi:

```python
class Harorat:
    def __init__(self, selsiy: float):
        self.selsiy = selsiy

    @property
    def selsiy(self) -> float:
        return self._selsiy

    @selsiy.setter
    def selsiy(self, qiymat: float) -> None:
        if qiymat < -273.15:
            raise ValueError("Mutlaq noldan past")
        self._selsiy = qiymat

    @property
    def farengeyt(self) -> float:
        return self._selsiy * 9 / 5 + 32

    @farengeyt.setter
    def farengeyt(self, f: float) -> None:
        self.selsiy = (f - 32) * 5 / 9     # selsiy setter'i orqali — validatsiya ham ishlaydi

h = Harorat(100)
print(h.farengeyt)     # 212.0
h.farengeyt = 32
print(h.selsiy)        # 0.0
```

---

## 17.3 deleter va to'liq property

`@<nom>.deleter` — `del obyekt.atribut` yozilganda ishlaydi. Kamroq kerak bo'ladi, lekin to'liqlik uchun:

```python
class Foydalanuvchi:
    def __init__(self, ism: str):
        self.ism = ism            # DIQQAT: public nom (self.ism) — setter ishlaydi!

    @property
    def ism(self) -> str:
        return self._ism

    @ism.setter
    def ism(self, qiymat: str) -> None:
        if not qiymat.strip():
            raise ValueError("Ism bo'sh bo'lmasin")
        self._ism = qiymat.strip()

    @ism.deleter
    def ism(self) -> None:
        print("Ism o'chirilmoqda")
        self._ism = "<noma'lum>"

f = Foydalanuvchi("  Aziz  ")
print(repr(f.ism))     # 'Aziz'   — __init__ setter orqali yozdi, strip ishladi
del f.ism              # Ism o'chirilmoqda
print(f.ism)           # <noma'lum>
```

E'tibor ber: `__init__` ichida `self.ism = ism` deb **public nomga** (property nomiga) yozdik, `self._ism = ism` deb backing maydonga emas. Aynan shu kichik farq tufayli konstruktorda berilgan `"  Aziz  "` setter'dan o'tib, `strip()` qilinadi — natija `'Aziz'`. Agar `__init__` da `self._ism = ism` deb yozganingda, setter **chetlab o'tilardi**: qiymat tozalanmasdan saqlanib, `repr(f.ism)` `'  Aziz  '` (bo'shliqlar bilan) chiqardi va konstruktorga bo'sh ism berib ham xato chiqmasdi.

Buni isbotlash uchun — setter validatsiyasi endi konstruktorda ham ishlaydi:

```python
# Foydalanuvchi("   ")   # ValueError: Ism bo'sh bo'lmasin — setter __init__ dan ishladi
```

> **Oltin qoida:** `@property` bilan ishlovchi atributni `__init__` da **public nom orqali** (`self.x = ...`) o'rnat, backing maydonga (`self._x = ...`) to'g'ridan yozma. Faqat shundagina normalizatsiya (strip) va validatsiya **obyekt yaratilayotgan paytdayoq** qo'llanadi. Bu — yangi boshlovchilar ko'p tushadigan tuzoq: setter yozasan-u, `__init__` uni chetlab o'tib backing maydonga yozadi, natijada "boshlang'ich qiymat tekshirilmaydi". (17.2-bo'limda `self.selsiy = selsiy` aynan shu sababdan to'g'ri yozilgan.)

> **Xulosa:** `@property` (o'qish) + `@x.setter` (yozish) + `@x.deleter` (o'chirish) — atributning uch amalini ham nazorat qilish. Ko'pincha faqat property va setter kerak bo'ladi.

---

## 17.4 `@classmethod` — alternativ konstruktor

Ba'zan obyektni turli yo'l bilan yaratmoqchimiz: ba'zan oddiy argumentlardan, ba'zan lug'atdan, ba'zan matndan. `@classmethod` — birinchi parametri `self` emas, **`cls`** (klassning o'zi) bo'lgan metod. U ko'pincha **alternativ konstruktor** sifatida ishlatiladi:

```python
class User:
    def __init__(self, ism: str, yosh: int):
        self.ism = ism
        self.yosh = yosh

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(data["ism"], data["yosh"])    # cls() == User() ni chaqiradi

    @classmethod
    def from_string(cls, satr: str) -> "User":
        ism, yosh = satr.split(",")
        return cls(ism.strip(), int(yosh))

    def __repr__(self) -> str:
        return f"User({self.ism!r}, {self.yosh})"

u1 = User("Aziz", 20)
u2 = User.from_dict({"ism": "Malika", "yosh": 22})
u3 = User.from_string("Bobur, 25")
print(u1)              # User('Aziz', 20)
print(u2)              # User('Malika', 22)
print(u3)              # User('Bobur', 25)
```

> **Nega `cls`, `User` emas?** `cls` — chaqirilgan klass. Agar `User` dan meros olgan `Admin` bo'lsa, `Admin.from_dict(...)` avtomatik `Admin` obyektini yasaydi (chunki `cls` == `Admin`). Klass nomini qattiq yozsang, bu ishlamasdi.

---

## 17.5 `@staticmethod` — klassga tegishli yordamchi

`@staticmethod` — na `self`, na `cls` oladi. Bu shunchaki klass ichida "yashayotgan" oddiy funksiya: mantiqan klassga tegishli, lekin obyekt holatiga muhtoj emas:

```python
class Matematika:
    @staticmethod
    def tub_mi(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

print(Matematika.tub_mi(7))     # True
print(Matematika.tub_mi(8))     # False
```

> **Farqni eslab qol:** `self`-metod — obyekt ma'lumotiga muhtoj; `@classmethod` (`cls`) — klassning o'ziga (masalan, yangi obyekt yasash); `@staticmethod` — ikkalasiga ham muhtoj emas, faqat guruhlash uchun klass ichida turadi.

---

## 17.6 Klass atributi vs instance atributi

`self.x = ...` — bu **instance** (obyekt) atributi: har obyektda alohida. Klass tanasida to'g'ridan yozilgan atribut esa **klass atributi**: barcha obyektlarga umumiy:

```python
class Hisob:
    foiz: float = 0.05          # klass atributi — hammaga umumiy
    soni: int = 0               # nechta hisob yaratilgan

    def __init__(self, balans: float):
        self.balans = balans     # instance atributi — har obyektda alohida
        Hisob.soni += 1          # klass atributini o'zgartiramiz

a = Hisob(1000)
b = Hisob(500)
print(Hisob.soni)      # 2   — umumiy hisoblagich
print(a.foiz, b.foiz)  # 0.05 0.05   — ikkalasi ham klass atributini ko'radi
```

Ehtiyot bo'l: o'zgaruvchan (mutable) klass atributi xavfli — barcha obyektlar **bitta** ro'yxatni baham ko'radi:

```python
class Xato:
    elementlar: list = []       # XATO: barcha obyektlarga umumiy ro'yxat!

a = Xato()
b = Xato()
a.elementlar.append(1)
print(b.elementlar)    # [1]   — b ham o'zgardi! Kutilmagan natija

class Togri:
    def __init__(self):
        self.elementlar: list = []   # TO'G'RI: har obyektda yangi ro'yxat

a = Togri()
b = Togri()
a.elementlar.append(1)
print(b.elementlar)    # []   — b alohida
```

> **Qoida:** o'zgaruvchan (list, dict, set) atributlarni **doim** `__init__` ichida yarat. Klass tanasida faqat o'zgarmas (int, str, doimiy sozlamalar) qiymatlarni qoldir.

---

## 17.7 Inkapsulyatsiya — `_himoyalangan` va `__mangling`

Python'da chinakam "private" yo'q, lekin **kelishuvlar** bor:

- `_nom` (bitta pastki chiziq) — "bu ichki narsa, tashqaridan tegma" degan **maslahat**. Texnik jihatdan o'qish mumkin, lekin kelishuvga ko'ra tegmaysan.
- `__nom` (ikkita pastki chiziq) — **name mangling**: Python uni avtomatik `_KlassNomi__nom` ga aylantiradi. Bu ayniqsa merosda nom to'qnashuvini oldini oladi.

```python
class Hisob:
    def __init__(self, balans: float):
        self._egasi = "maxfiy"        # himoyalangan: tegmaslik kelishildi
        self.__pin = 1234             # mangling: _Hisob__pin ga aylanadi

    def tekshir(self, pin: int) -> bool:
        return self.__pin == pin       # klass ichida __pin oddiy ishlaydi

h = Hisob(1000)
print(h._egasi)        # maxfiy   — texnik jihatdan o'qish mumkin
print(h.tekshir(1234)) # True

# print(h.__pin)       # AttributeError: 'Hisob' object has no attribute '__pin'
print(h._Hisob__pin)   # 1234   — mangling shunday ishlaydi (lekin bunday yozma!)
```

> **Amaliyot:** kundalik ishda `_nom` yetarli — "ichki, tashqaridan ishlatma" signali. `__nom` (mangling) faqat merosda nom to'qnashuvidan himoya kerak bo'lganda ishlatiladi. Hech qachon `_Klass__pin` deb tashqaridan kovlama — bu kelishuvni buzadi.

---

## 17.8 `__repr__` va `__str__` — ikki xil matn

05-bobda `__str__` ni ko'rdik. Aslida ikkita dunder bor va ular **boshqa-boshqa** maqsadga xizmat qiladi:

- `__repr__` — **dasturchi uchun**: aniq, ko'pincha obyektni qayta yasashga yetadigan matn. `repr(x)`, REPL'da va ro'yxat ichida ko'rinadi.
- `__str__` — **foydalanuvchi uchun**: chiroyli, o'qishbop matn. `print(x)`, `str(x)`.

```python
class Pul:
    def __init__(self, miqdor: int, valyuta: str = "UZS"):
        self.miqdor = miqdor
        self.valyuta = valyuta

    def __repr__(self) -> str:
        return f"Pul(miqdor={self.miqdor}, valyuta={self.valyuta!r})"

    def __str__(self) -> str:
        return f"{self.miqdor:,} {self.valyuta}"

p = Pul(1500000)
print(repr(p))     # Pul(miqdor=1500000, valyuta='UZS')   — dasturchi uchun
print(str(p))      # 1,500,000 UZS                          — chiroyli
print(p)           # 1,500,000 UZS   — print __str__ ni ishlatadi
print([p, p])      # [Pul(...), Pul(...)]   — ro'yxat __repr__ ni ishlatadi
```

> **Maslahat:** agar bittasini yozsang, **`__repr__`** ni yoz — `__str__` bo'lmasa, `print` avtomatik `__repr__` ga tushadi. `__repr__` ni shunday yozki, ko'rganda obyekt holatini darrov tushunasan.

---

## 17.9 `__eq__` va `__hash__` — birga yuradi

Standart holatda ikki obyekt faqat **bitta xil obyekt** bo'lsagina teng (`is` kabi). Ko'pincha bizga **qiymat bo'yicha** tenglik kerak: ikki nuqta koordinatalari bir xil bo'lsa — teng.

```python
class Nuqta:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Nuqta):
            return NotImplemented      # boshqa tur bilan solishtirishni Python'ga qoldiramiz
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))   # eq'da ishlatilgan maydonlardan

a = Nuqta(1, 2)
b = Nuqta(1, 2)
c = Nuqta(3, 4)
print(a == b)      # True    — qiymat bo'yicha teng
print(a == c)      # False
print({a, b, c})   # {Nuqta..., Nuqta...}   — a va b bitta sanaladi (2 element)
```

> **Muhim qoida:** agar `__eq__` yozsang, **`__hash__`** ni ham yoz. Sababi: Python `__eq__` ni belgilaganingda `__hash__` ni avtomatik `None` qiladi (obyekt `set`/`dict` kalitiga yaroqsiz bo'lib qoladi). Teng obyektlar **bir xil hash** ga ega bo'lishi shart — shuning uchun ikkalasini ham `eq`dagi maydonlardan yasaymiz.

`NotImplemented` qaytarsang, Python boshqa tomonning `__eq__` ini sinab ko'radi va oxir-oqibat `False` beradi — bu to'g'ri xulq.

---

## 17.10 Taqqoslash metodlari va `@total_ordering`

Saralash (`sorted`) va `<`, `>` uchun taqqoslash dunderlari kerak: `__lt__` (<), `__le__` (<=), `__gt__` (>), `__ge__` (>=). To'rttasini ham yozish zerikarli — `@functools.total_ordering` bittasi (`__lt__`) va `__eq__` dan qolganini avtomatik yasaydi:

```python
from functools import total_ordering

@total_ordering
class Versiya:
    def __init__(self, katta: int, kichik: int):
        self.katta = katta
        self.kichik = kichik

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Versiya):
            return NotImplemented
        return (self.katta, self.kichik) == (other.katta, other.kichik)

    def __lt__(self, other: "Versiya") -> bool:
        if not isinstance(other, Versiya):
            return NotImplemented
        return (self.katta, self.kichik) < (other.katta, other.kichik)

    def __repr__(self) -> str:
        return f"{self.katta}.{self.kichik}"

v = [Versiya(1, 5), Versiya(2, 0), Versiya(1, 2)]
print(sorted(v))            # [1.2, 1.5, 2.0]   — saralandi
print(Versiya(1, 5) > Versiya(1, 2))   # True   — __gt__ avtomatik yasaldi
print(Versiya(2, 0) >= Versiya(2, 0))  # True   — __ge__ ham
```

> **Foyda:** `@total_ordering` faqat `__eq__` + `__lt__` so'raydi, qolgan uchtasini o'zi qo'shadi. Kortej (tuple) bo'yicha solishtirish — bir necha maydonni tartiblashning eng oson yo'li.

---

## 17.11 O'z konteyneringni yasash: `__len__`, `__getitem__`, `__contains__`, `__iter__`

Obyektingni `list`/`dict` kabi tutadigan qilish mumkin. Bir nechta dunder klassingga indekslash, `len()`, `in` va `for` ni qo'shadi:

```python
class Jamoa:
    def __init__(self, nom: str):
        self.nom = nom
        self._azolar: list[str] = []

    def qosh(self, azo: str) -> None:
        self._azolar.append(azo)

    def __len__(self) -> int:                  # len(jamoa)
        return len(self._azolar)

    def __getitem__(self, i: int) -> str:      # jamoa[0]
        return self._azolar[i]

    def __contains__(self, azo: str) -> bool:  # "Aziz" in jamoa
        return azo in self._azolar

    def __iter__(self):                        # for x in jamoa
        return iter(self._azolar)

j = Jamoa("Yoshlar")
j.qosh("Aziz")
j.qosh("Malika")
j.qosh("Bobur")

print(len(j))            # 3
print(j[0])              # Aziz          — indekslash
print("Malika" in j)     # True          — in operatori
for a in j:              # for sikli
    print(a)             # Aziz, Malika, Bobur
```

> **Maroqli fakt:** agar `__iter__` bo'lmasa-yu, faqat `__getitem__` bo'lsa, Python baribir `for` ni ishga tushiradi — indeksni 0 dan oshirib `IndexError` chiqquncha so'raydi. Lekin aniqlik uchun `__iter__` yozish yaxshiroq.

---

## 17.12 `__call__` — obyektni funksiya kabi chaqirish

`__call__` qo'shilsa, obyektni xuddi funksiya kabi `obyekt(...)` deb chaqirish mumkin. Bu "holatni eslab qoluvchi funksiya" yasashga qulay (closure'ga muqobil, lekin obyektda):

```python
class Kopaytiruvchi:
    def __init__(self, koeffitsiyent: float):
        self.koeffitsiyent = koeffitsiyent

    def __call__(self, x: float) -> float:
        return x * self.koeffitsiyent

ikki_barobar = Kopaytiruvchi(2)
print(ikki_barobar(10))    # 20   — obyekt funksiya kabi chaqirildi
print(ikki_barobar(7))     # 14
print(callable(ikki_barobar))  # True
```

Holatni eslab qoluvchi hisoblagich:

```python
class Sanagich:
    def __init__(self):
        self.soni = 0

    def __call__(self) -> int:
        self.soni += 1
        return self.soni

s = Sanagich()
print(s(), s(), s())   # 1 2 3   — har chaqiriqda eslab qoladi
```

---

## 17.13 Operator overloading: `__add__`, `__mul__` va boshqalar

Dunderlar `+`, `-`, `*` kabi operatorlarni o'z klassingga moslashtirishga imkon beradi. Klassik misol — matematik vektor:

```python
from __future__ import annotations
import math

class Vektor:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vektor({self.x}, {self.y})"

    def __add__(self, other: Vektor) -> Vektor:        # v1 + v2
        return Vektor(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vektor) -> Vektor:        # v1 - v2
        return Vektor(self.x - other.x, self.y - other.y)

    def __mul__(self, skalyar: float) -> Vektor:       # v * 3
        return Vektor(self.x * skalyar, self.y * skalyar)

    def __rmul__(self, skalyar: float) -> Vektor:      # 3 * v (chap tomon int bo'lsa)
        return self * skalyar

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vektor):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __abs__(self) -> float:                        # abs(v) — uzunlik
        return math.hypot(self.x, self.y)

a = Vektor(1, 2)
b = Vektor(3, 4)
print(a + b)       # Vektor(4, 6)
print(b - a)       # Vektor(2, 2)
print(a * 3)       # Vektor(3, 6)
print(3 * a)       # Vektor(3, 6)   — __rmul__ ishladi
print(abs(b))      # 5.0            — Pifagor
print(a == Vektor(1, 2))   # True
```

> **`__rmul__` nima?** `3 * a` da chap tomon — `int`, u `Vektor` bilan nima qilishni bilmaydi va `NotImplemented` qaytaradi. Shunda Python o'ng tomonning `__rmul__` ini sinaydi. Shu sabab `5 * vektor` ham ishlaydi.

Boshqa foydali arifmetik dunderlar: `__truediv__` (`/`), `__floordiv__` (`//`), `__mod__` (`%`), `__pow__` (`**`), `__neg__` (`-v`).

---

## 17.14 Klass — context manager: `__enter__` va `__exit__`

`with` bloki resurslarni ochib-yopish (fayl, ulanish, qulf) uchun ishlatiladi. O'z klassingni `with` bilan ishlaydigan qilish uchun `__enter__` (kirishda) va `__exit__` (chiqishda, hatto xato bo'lsa ham) yoz:

```python
import time

class Taymer:
    def __enter__(self) -> "Taymer":
        self.boshlandi = time.perf_counter()
        return self                          # 'as t' ga shu qaytadi

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.davomiyligi = time.perf_counter() - self.boshlandi
        print(f"Vaqt: {self.davomiyligi:.4f} soniya")
        return False         # False — xato bo'lsa, uni yutmaymiz (yuqoriga uzatamiz)

with Taymer() as t:
    jami = sum(range(1_000_000))
# blok tugashi bilan __exit__ ishlaydi va vaqtni chiqaradi
```

`__exit__` ning uch parametri — blok ichida xato bo'lsa, uning turi/qiymati/izi. `True` qaytarsang, xatoni "yutasan" (yashirasan); `False` (yoki `None`) qaytarsang — xato yuqoriga ko'tariladi. Quyida qulf misoli xato bo'lsa ham resurs yopilishini ko'rsatadi:

```python
class Ulanish:
    def __init__(self, nom: str):
        self.nom = nom

    def __enter__(self) -> "Ulanish":
        print(f"{self.nom}: ochildi")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print(f"{self.nom}: yopildi")        # xato bo'lsa ham ishlaydi
        return False

try:
    with Ulanish("baza") as u:
        print("ish ketmoqda")
        raise ValueError("nimadir buzildi")
except ValueError as e:
    print(f"Ushlandi: {e}")
# Chiqish:
# baza: ochildi
# ish ketmoqda
# baza: yopildi      <- __exit__ xatodan oldin resursni yopdi
# Ushlandi: nimadir buzildi
```

---

## 17.15 `@dataclass` — qaytariluvchi kodni yo'qotish

Faqat ma'lumot saqlovchi klasslarda `__init__`, `__repr__`, `__eq__` ni qo'lda yozish zerikarli va xatoga moyil. `@dataclass` shularning hammasini **avtomatik** yasaydi — sen faqat maydonlarni tip bilan e'lon qilasan:

```python
from dataclasses import dataclass

@dataclass
class Mahsulot:
    nom: str
    narx: float
    soni: int = 1               # default qiymat

m1 = Mahsulot("Olma", 12000, 3)
m2 = Mahsulot("Olma", 12000, 3)
print(m1)              # Mahsulot(nom='Olma', narx=12000, soni=3)   — __repr__ tayyor
print(m1 == m2)        # True    — __eq__ tayyor (qiymat bo'yicha)
print(m1.narx)         # 12000
```

Bir necha qatorda biz qo'lda `__init__` + `__repr__` + `__eq__` yozishdan qutuldik. Dataclass'ga oddiy metodlar ham qo'shsa bo'ladi:

```python
@dataclass
class Tortburchak:
    eni: float
    boyi: float

    def yuza(self) -> float:
        return self.eni * self.boyi

t = Tortburchak(4, 6)
print(t.yuza())        # 24
print(t)               # Tortburchak(eni=4, boyi=6)
```

---

## 17.16 `field`, `default_factory` va `frozen`

Dataclass maydonida o'zgaruvchan default (list, dict) bersang, oddiy `= []` **xato** beradi (barcha obyektlar bitta ro'yxatni baham ko'rmasligi uchun Python buni taqiqlaydi). To'g'ri yo'l — `field(default_factory=...)`:

```python
from dataclasses import dataclass, field

@dataclass
class Talaba:
    ism: str
    ballar: list[int] = field(default_factory=list)   # har obyektda yangi ro'yxat

a = Talaba("Aziz")
b = Talaba("Malika")
a.ballar.append(90)
print(a.ballar)        # [90]
print(b.ballar)        # []    — alohida ro'yxat
```

`frozen=True` — obyektni **o'zgarmas** (immutable) qiladi: yaratilgandan keyin maydonni o'zgartirib bo'lmaydi. Bu obyektni `set`/`dict` kalitiga ham yaroqli qiladi (chunki `__hash__` avtomatik yasaladi):

```python
@dataclass(frozen=True)
class Nuqta:
    x: int
    y: int

p = Nuqta(1, 2)
print(p)               # Nuqta(x=1, y=2)
print({p: "boshlanish"})   # {Nuqta(x=1, y=2): 'boshlanish'}   — kalit bo'la oldi

# p.x = 5              # FrozenInstanceError: cannot assign to field 'x'
```

`field` ning yana foydali parametrlari: `field(compare=False)` (maydon `__eq__` da hisobga olinmasin), `field(repr=False)` (`__repr__` da ko'rinmasin).

---

## 17.17 `slots=True`, `kw_only` va tartib

`@dataclass(slots=True)` — obyekt uchun `__slots__` yasaydi: xotira kamroq, atribut o'qish tezroq, lekin yangi atribut qo'shib bo'lmaydi (keyingi bo'limda `__slots__` ni batafsil ko'ramiz):

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Pixel:
    x: int
    y: int
    rang: str = "qora"

p = Pixel(10, 20)
print(p)               # Pixel(x=10, y=20, rang='qora')
# p.alfa = 0.5         # AttributeError: 'Pixel' object has no attribute 'alfa'
```

`kw_only=True` — barcha maydonlarni **faqat nom bilan** uzatishga majbur qiladi (pozitsiya bo'yicha emas) — bu chalkashlikni kamaytiradi:

```python
@dataclass(kw_only=True)
class Sozlama:
    host: str
    port: int
    debug: bool = False

s = Sozlama(host="localhost", port=8080)   # nom bilan uzatish shart
print(s)               # Sozlama(host='localhost', port=8080, debug=False)
# Sozlama("localhost", 8080)   # TypeError — pozitsiya bilan bo'lmaydi
```

> **Default tartibi:** default'li maydonlardan keyin default'siz maydon kelolmaydi (oddiy funksiya argumentlari kabi). `kw_only=True` esa bu cheklovni olib tashlaydi — chunki tartib ahamiyatsiz bo'lib qoladi.

---

## 17.18 `Enum` — nomlangan doimiylar to'plami

Sehrli "magic" qiymatlar (`status == 1`, `rang == "qizil"`) kodni chigallashtiradi. `Enum` — bog'liq doimiylarning nomlangan, xavfsiz to'plami:

```python
from enum import Enum, auto

class Holat(Enum):
    KUTILMOQDA = auto()       # auto() — 1, 2, 3... avtomatik beradi
    JARAYONDA = auto()
    TUGALLANDI = auto()

print(Holat.JARAYONDA)         # Holat.JARAYONDA
print(Holat.JARAYONDA.name)    # JARAYONDA
print(Holat.JARAYONDA.value)   # 2
print(Holat.KUTILMOQDA == Holat.KUTILMOQDA)   # True

for h in Holat:                # Enum ustidan aylanish mumkin
    print(h.name, h.value)     # KUTILMOQDA 1, JARAYONDA 2, TUGALLANDI 3
```

Enum'ga metod ham qo'shsa bo'ladi:

```python
from enum import Enum

class Yonalish(Enum):
    SHIMOL = (0, 1)
    JANUB = (0, -1)
    SHARQ = (1, 0)
    GARB = (-1, 0)

    def teskari(self) -> "Yonalish":
        dx, dy = self.value
        return Yonalish((-dx, -dy))

print(Yonalish.SHIMOL.teskari())   # Yonalish.JANUB
print(Yonalish.SHARQ.value)        # (1, 0)
```

`IntEnum` — qiymatlari `int` bilan ham solishtiriladigan Enum:

```python
from enum import IntEnum

class Daraja(IntEnum):
    PAST = 1
    ORTA = 2
    YUQORI = 3

print(Daraja.YUQORI > Daraja.PAST)   # True   — son kabi solishtiriladi
print(Daraja.ORTA == 2)              # True   — int bilan ham teng
print(Daraja.ORTA + 1)               # 3      — arifmetika ishlaydi
```

> **Foyda:** Enum xatolardan saqlaydi. `Holat("nomalum")` darrov `ValueError` beradi, `status = "nomalum"` esa jimgina o'tib ketardi. IDE ham mavjud variantlarni ko'rsatadi.

---

## 17.19 `NamedTuple` — nomli maydonli kortej

`NamedTuple` — kortej (tuple) kabi o'zgarmas, lekin maydonlariga **nom** bilan murojaat qilinadigan tur. Yengil, faqat ma'lumot saqlovchi obyektga ideal:

```python
from typing import NamedTuple

class Koordinata(NamedTuple):
    lat: float
    lon: float
    nom: str = "noma'lum"     # default ham bo'ladi

k = Koordinata(41.31, 69.24, "Toshkent")
print(k.lat)           # 41.31     — nom bilan
print(k[0])            # 41.31     — indeks bilan ham (kortej-ku)
print(k.nom)           # Toshkent
lat, lon, nom = k      # ochib olish (unpacking) ishlaydi
print(lat, lon)        # 41.31 69.24

# k.lat = 0            # AttributeError — o'zgarmas (immutable)
```

> **`NamedTuple` vs `@dataclass(frozen=True)`:** ikkalasi ham o'zgarmas ma'lumot uchun. `NamedTuple` — kortej (indekslash, unpacking ishlaydi, yengilroq); `dataclass` — moslashuvchanroq (metodlar, `field`, meros qulayroq). Oddiy "qiymatlar uchligi" kerak bo'lsa — `NamedTuple`.

---

## 17.20 `ABC` va `@abstractmethod` — interfeys majburlash

Ba'zan "shartnoma" o'rnatmoqchimiz: har bir avlod klass aniq metodni **albatta** yozsin. `ABC` (Abstract Base Class) va `@abstractmethod` — bu interfeysni majburlaydi: abstrakt metodni amalga oshirmagan klassdan obyekt yasab bo'lmaydi:

```python
from abc import ABC, abstractmethod

class Shakl(ABC):
    @abstractmethod
    def yuza(self) -> float:
        ...                    # tanasi yo'q — avlod yozishi shart

    @abstractmethod
    def perimetr(self) -> float:
        ...

    def tavsif(self) -> str:                    # oddiy (umumiy) metod ham bo'ladi
        return f"Yuza={self.yuza():.2f}, perimetr={self.perimetr():.2f}"

class Doira(Shakl):
    def __init__(self, r: float):
        self.r = r

    def yuza(self) -> float:
        return 3.14159 * self.r ** 2

    def perimetr(self) -> float:
        return 2 * 3.14159 * self.r

d = Doira(5)
print(d.tavsif())      # Yuza=78.54, perimetr=31.42

# Shakl()             # TypeError — abstrakt klassdan obyekt yasab bo'lmaydi
```

Agar avlod abstrakt metodni yozmasa, obyekt yasashda darrov xato:

```python
class Yarim(Shakl):
    def yuza(self) -> float:
        return 0          # perimetr() yozilmadi!

# Yarim()             # TypeError: Can't instantiate abstract class Yarim
#                     # without an implementation for abstract method 'perimetr'
```

> **Foyda:** ABC "interfeys"ni hujjatlashtiradi va majburlaydi. Katta loyihada bir nechta dasturchi bir xil shartnomaga amal qilishini kafolatlaydi — metodni unutib qolsang, ishga tushirishdayoq xato chiqadi (ishlab chiqarishda emas).

---

## 17.21 Ko'p meros, MRO va `super()`

Python bir klassni bir nechta klassdan meros qildirishga ruxsat beradi (ko'p meros). Lekin "agar ikkala otada bir xil nomli metod bo'lsa, qaysi biri ishlaydi?" degan savol tug'iladi. Buni **MRO** (Method Resolution Order — metod izlash tartibi) hal qiladi. Python **C3 linearization** algoritmi bilan aniq, bashoratli tartib quradi:

```python
class A:
    def kim(self) -> str:
        return "A"

class B(A):
    def kim(self) -> str:
        return "B -> " + super().kim()

class C(A):
    def kim(self) -> str:
        return "C -> " + super().kim()

class D(B, C):                  # ham B, ham C dan meros
    def kim(self) -> str:
        return "D -> " + super().kim()

d = D()
print(d.kim())                 # D -> B -> C -> A
print([k.__name__ for k in D.__mro__])   # ['D', 'B', 'C', 'A', 'object']
```

E'tibor ber: `D` da `super()` to'g'ridan-to'g'ri `A` ga emas, **MRO bo'yicha keyingi**ga (`B`, keyin `C`) o'tadi. Shu sabab `super()` ko'p merosda ham har bir klassni **bir marta** to'g'ri tartibda chaqiradi — `B` ichidagi `super()` "A"ga emas, `C`ga boradi. Bu C3 ning kuchi.

> **MRO ni `Klass.__mro__` orqali ko'r.** Tartib: o'zi → ota klasslar (chapdan o'ngga, lekin har biri faqat bir marta, otadan oldin) → oxirida `object`. `super()` shu ro'yxat bo'ylab yuradi.

---

## 17.22 Mixin — kichik qobiliyat qo'shuvchi klass

**Mixin** — to'liq klass emas, balki boshqa klasslarga "qo'shimcha qobiliyat" beruvchi kichik klass. Odatda o'z `__init__` i bo'lmaydi, faqat metod(lar) beradi. Ko'p meros orqali aralashtiriladi:

```python
import json

class JSONMixin:
    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)

class TakrorMixin:
    def takrorla(self, n: int) -> None:
        for _ in range(n):
            print(self)

class Mahsulot(JSONMixin, TakrorMixin):
    def __init__(self, nom: str, narx: int):
        self.nom = nom
        self.narx = narx

    def __str__(self) -> str:
        return f"{self.nom}: {self.narx}"

m = Mahsulot("Olma", 12000)
print(m.to_json())     # {"nom": "Olma", "narx": 12000}   — JSONMixin'dan
m.takrorla(2)          # Olma: 12000 (ikki marta)         — TakrorMixin'dan
```

> **Mixin nomi odatda `...Mixin` bilan tugaydi** — bu "men mustaqil ishlamayman, faqat qo'shimcha beraman" signali. Mixin'lar takrorlovchi qobiliyatlarni (loglash, JSON, taqqoslash) bir joyga jamlab, ko'p klassga ulashga yordam beradi.

---

## 17.23 `__slots__` — xotirani tejash

Standart obyekt har bir atributni `__dict__` (lug'at) da saqlaydi — bu moslashuvchan, lekin xotira talab qiladi. `__slots__` lug'atni o'chiradi va atributlarni qat'iy ro'yxatda saqlaydi: **kam xotira, tezroq o'qish**, lekin yangi atribut qo'shib bo'lmaydi:

```python
class Oddiy:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Tejamkor:
    __slots__ = ("x", "y")          # faqat shu ikki atribut bo'ladi

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

a = Oddiy(1, 2)
a.z = 3                # OK — __dict__ borligi uchun yangi atribut qo'shildi
print(a.__dict__)      # {'x': 1, 'y': 2, 'z': 3}

b = Tejamkor(1, 2)
# b.z = 3              # AttributeError: 'Tejamkor' object has no attribute 'z'
# print(b.__dict__)   # AttributeError — __dict__ yo'q
print(b.x, b.y)        # 1 2
```

> **Qachon `__slots__`?** Bir xil tuzilmali obyektlardan **juda ko'p** (millionlab) yaratilganda — har biridan tejalgan xotira jamlanib katta farq beradi. Kichik dasturlarda kerak emas; "erta optimallashtirish" ga yo'l qo'yma. `@dataclass(slots=True)` shuni avtomatik beradi.

---

## 17.24 Kompozitsiya vs meros

Meros — "B **bu** A" (It bu Hayvon). Lekin ko'pincha "B **da** A bor" munosabati to'g'riroq — bu **kompozitsiya**: obyekt boshqa obyektni atribut sifatida saqlaydi.

```python
class Dvigatel:
    def __init__(self, ot_kuchi: int):
        self.ot_kuchi = ot_kuchi

    def ishga_tushir(self) -> str:
        return f"Dvigatel ({self.ot_kuchi} ot kuchi) ishga tushdi"

class Mashina:
    def __init__(self, marka: str, ot_kuchi: int):
        self.marka = marka
        self.dvigatel = Dvigatel(ot_kuchi)     # Mashina'DA Dvigatel BOR (meros emas)

    def hayda(self) -> None:
        print(f"{self.marka}: {self.dvigatel.ishga_tushir()}")

m = Mashina("Malibu", 250)
m.hayda()              # Malibu: Dvigatel (250 ot kuchi) ishga tushdi
```

> **Qoidaning oltin qoidasi:** "meroldan kompozitsiyani afzal ko'r." Meros qattiq bog'lanish yaratadi (ota o'zgarsa, avlod buziladi). Kompozitsiya esa moslashuvchan — qismlarni mustaqil almashtirish mumkin. "B bu A" desa bo'lsagina meros ishlat; aks holda kompozitsiya.

---

## 17.25 `match/case` bilan klass patterni

10-bobda `match/case` ni ko'rdik. U klasslar bilan ham ishlaydi — obyektni **strukturasi bo'yicha** ajratadi (atributlarini bevosita tekshirib, ochib oladi):

```python
from dataclasses import dataclass

@dataclass
class Nuqta:
    x: int
    y: int

def joylashuv(n: Nuqta) -> str:
    match n:
        case Nuqta(x=0, y=0):
            return "Markazda"
        case Nuqta(x=0, y=y):
            return f"Y o'qida, y={y}"
        case Nuqta(x=x, y=0):
            return f"X o'qida, x={x}"
        case Nuqta(x=x, y=y) if x == y:
            return f"Diagonalda ({x}, {y})"
        case Nuqta():
            return f"Boshqa joyda ({n.x}, {n.y})"

print(joylashuv(Nuqta(0, 0)))    # Markazda
print(joylashuv(Nuqta(0, 5)))    # Y o'qida, y=5
print(joylashuv(Nuqta(3, 0)))    # X o'qida, x=3
print(joylashuv(Nuqta(4, 4)))    # Diagonalda (4, 4)
print(joylashuv(Nuqta(2, 7)))    # Boshqa joyda (2, 7)
```

> **Diqqat:** `case Nuqta(x=0, y=y)` — `x` aniq 0 bo'lishini **tekshiradi**, `y` ni esa **ochib oladi** (o'zgaruvchiga bog'laydi). `if x == y` qo'shimcha shart (guard). Bu klass obyektlarini ajratishning juda o'qishbop usuli — uzun `if/elif` zanjiridan ancha toza.

---

## ✍️ Masalalar (20 ta)

> Bu masalalar 17-modul (ilg'or OOP) mavzulariga asoslangan. Yechishdan oldin tegishli bo'limga qayt.

**Oson (1–7):**

1. `To'rtburchak` klassini yarat: `eni`, `boyi`; `@property yuza` (eni*boyi) qaytarsin. `boyi` ni o'zgartirib, `yuza` yangilanganini ko'rsat.
2. `Yosh` klassiga `@property` + setter qo'sh: yosh 0 dan kichik bo'lsa `ValueError` ko'tarsin.
3. `Kitob` klassiga `__repr__` yoz: `Kitob(nom='...', muallif='...')` ko'rinishida.
4. `Harorat` klassi: `selsiy` saqlasin, `farengeyt` `@property` (faqat o'qiladigan) bo'lsin: `c*9/5+32`.
5. `User` klassiga `@classmethod from_dict` qo'sh: `{"ism": ..., "yosh": ...}` lug'atdan obyekt yasasin.
6. `Geometriya` klassiga `@staticmethod uchburchak_yuzasi(asos, balandlik)` qo'sh: `asos*balandlik/2`.
7. `Hisob` klassiga klass atributi `soni` qo'sh: har yangi obyekt yaratilganda 1 ga oshsin.

**O'rta (8–14):**

8. `Nuqta` klassiga `__eq__` va `__hash__` yoz (x, y bo'yicha). Ikki bir xil nuqtani `set` ga solib, bitta sanalishini ko'rsat.
9. `Mahsulot` ni `@dataclass` qil: `nom`, `narx`, `soni=1`. Ikki bir xil obyekt `==` ekanini tekshir.
10. `Talaba` ni `@dataclass` qil va `ballar` maydonini `field(default_factory=list)` bilan qo'sh. Ikki obyekt ro'yxatlari alohida ekanini ko'rsat.
11. `Hafta` `Enum` ini yarat (DUSHANBA...YAKSHANBA, `auto()`). Ustidan aylanib, har birining `name` va `value` ini chiqar.
12. `Jamoa` klassiga `__len__` va `__getitem__` qo'sh (ichida ro'yxat). `len()` va indekslashni ko'rsat.
13. `Daraja` `IntEnum` ini yarat (PAST=1, ORTA=2, YUQORI=3). `YUQORI > PAST` va `ORTA == 2` ni tekshir.
14. `Stack` klassiga `__contains__` va `__iter__` qo'sh: `x in stack` va `for` ishlasin.

**Murakkab (15–20):**

15. `Vektor` klassini yoz: `__add__`, `__sub__`, `__mul__` (skalyar), `__eq__`, `__repr__`. `v1 + v2`, `v * 3` ni sina.
16. `Shakl` ABC sini yarat (`@abstractmethod yuza`). `Doira` va `Kvadrat` avlodlarini yoz; abstrakt klassdan obyekt yasab bo'lmasligini tekshir.
17. `Fayl` klassini context manager qil: `__enter__` "ochildi", `__exit__` "yopildi" chiqarsin. Blok ichida xato bo'lsa ham `__exit__` ishlashini ko'rsat.
18. `Versiya` klassiga `@total_ordering` qo'llab `__eq__` + `__lt__` yoz. Versiyalar ro'yxatini `sorted` qil.
19. `Pul` klassini `@dataclass(frozen=True)` qil (`miqdor`, `valyuta`). Uni `dict` kalitiga ishlat va o'zgartirib bo'lmasligini ko'rsat.
20. `Kopaytiruvchi` klassiga `__call__` qo'sh: `Kopaytiruvchi(3)` obyektini funksiya kabi chaqirib `x*3` qaytarsin. `callable(obyekt)` `True` ekanini tekshir.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Masala 1</summary>

```python
class Tortburchak:
    def __init__(self, eni: float, boyi: float):
        self.eni = eni
        self.boyi = boyi

    @property
    def yuza(self) -> float:
        return self.eni * self.boyi

t = Tortburchak(4, 6)
print(t.yuza)          # 24
t.boyi = 10
print(t.yuza)          # 40   — qayta hisoblandi
```

</details>

<details markdown="1">
<summary>Masala 2</summary>

```python
class Odam:
    def __init__(self, yosh: int):
        self.yosh = yosh

    @property
    def yosh(self) -> int:
        return self._yosh

    @yosh.setter
    def yosh(self, qiymat: int) -> None:
        if qiymat < 0:
            raise ValueError("Yosh manfiy bo'lmasin")
        self._yosh = qiymat

o = Odam(20)
print(o.yosh)          # 20
try:
    o.yosh = -5
except ValueError as e:
    print(e)           # Yosh manfiy bo'lmasin
```

</details>

<details markdown="1">
<summary>Masala 3</summary>

```python
class Kitob:
    def __init__(self, nom: str, muallif: str):
        self.nom = nom
        self.muallif = muallif

    def __repr__(self) -> str:
        return f"Kitob(nom={self.nom!r}, muallif={self.muallif!r})"

k = Kitob("O'tkan kunlar", "A. Qodiriy")
print(repr(k))         # Kitob(nom="O'tkan kunlar", muallif='A. Qodiriy')
```

</details>

<details markdown="1">
<summary>Masala 4</summary>

```python
class Harorat:
    def __init__(self, selsiy: float):
        self.selsiy = selsiy

    @property
    def farengeyt(self) -> float:
        return self.selsiy * 9 / 5 + 32

h = Harorat(100)
print(h.farengeyt)     # 212.0
h.selsiy = 0
print(h.farengeyt)     # 32.0
```

</details>

<details markdown="1">
<summary>Masala 5</summary>

```python
class User:
    def __init__(self, ism: str, yosh: int):
        self.ism = ism
        self.yosh = yosh

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(data["ism"], data["yosh"])

    def __repr__(self) -> str:
        return f"User({self.ism!r}, {self.yosh})"

u = User.from_dict({"ism": "Malika", "yosh": 22})
print(u)               # User('Malika', 22)
```

</details>

<details markdown="1">
<summary>Masala 6</summary>

```python
class Geometriya:
    @staticmethod
    def uchburchak_yuzasi(asos: float, balandlik: float) -> float:
        return asos * balandlik / 2

print(Geometriya.uchburchak_yuzasi(10, 4))   # 20.0
```

</details>

<details markdown="1">
<summary>Masala 7</summary>

```python
class Hisob:
    soni: int = 0

    def __init__(self, balans: float):
        self.balans = balans
        Hisob.soni += 1

a = Hisob(100)
b = Hisob(200)
c = Hisob(300)
print(Hisob.soni)      # 3
```

</details>

<details markdown="1">
<summary>Masala 8</summary>

```python
class Nuqta:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Nuqta):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

a = Nuqta(1, 2)
b = Nuqta(1, 2)
print(a == b)          # True
print(len({a, b}))     # 1   — bitta sanaldi
```

</details>

<details markdown="1">
<summary>Masala 9</summary>

```python
from dataclasses import dataclass

@dataclass
class Mahsulot:
    nom: str
    narx: float
    soni: int = 1

m1 = Mahsulot("Olma", 12000, 3)
m2 = Mahsulot("Olma", 12000, 3)
print(m1 == m2)        # True
print(m1)              # Mahsulot(nom='Olma', narx=12000, soni=3)
```

</details>

<details markdown="1">
<summary>Masala 10</summary>

```python
from dataclasses import dataclass, field

@dataclass
class Talaba:
    ism: str
    ballar: list[int] = field(default_factory=list)

a = Talaba("Aziz")
b = Talaba("Malika")
a.ballar.append(90)
print(a.ballar)        # [90]
print(b.ballar)        # []   — alohida
```

</details>

<details markdown="1">
<summary>Masala 11</summary>

```python
from enum import Enum, auto

class Hafta(Enum):
    DUSHANBA = auto()
    SESHANBA = auto()
    CHORSHANBA = auto()
    PAYSHANBA = auto()
    JUMA = auto()
    SHANBA = auto()
    YAKSHANBA = auto()

for kun in Hafta:
    print(kun.name, kun.value)   # DUSHANBA 1, SESHANBA 2, ... YAKSHANBA 7
```

</details>

<details markdown="1">
<summary>Masala 12</summary>

```python
class Jamoa:
    def __init__(self):
        self._azolar: list[str] = []

    def qosh(self, azo: str) -> None:
        self._azolar.append(azo)

    def __len__(self) -> int:
        return len(self._azolar)

    def __getitem__(self, i: int) -> str:
        return self._azolar[i]

j = Jamoa()
j.qosh("Aziz")
j.qosh("Malika")
print(len(j))          # 2
print(j[0])            # Aziz
```

</details>

<details markdown="1">
<summary>Masala 13</summary>

```python
from enum import IntEnum

class Daraja(IntEnum):
    PAST = 1
    ORTA = 2
    YUQORI = 3

print(Daraja.YUQORI > Daraja.PAST)   # True
print(Daraja.ORTA == 2)              # True
```

</details>

<details markdown="1">
<summary>Masala 14</summary>

```python
class Stack:
    def __init__(self):
        self._items: list[int] = []

    def push(self, x: int) -> None:
        self._items.append(x)

    def __contains__(self, x: int) -> bool:
        return x in self._items

    def __iter__(self):
        return iter(self._items)

s = Stack()
s.push(1)
s.push(2)
print(2 in s)          # True
for x in s:
    print(x)           # 1, 2
```

</details>

<details markdown="1">
<summary>Masala 15</summary>

```python
from __future__ import annotations

class Vektor:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: Vektor) -> Vektor:
        return Vektor(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vektor) -> Vektor:
        return Vektor(self.x - other.x, self.y - other.y)

    def __mul__(self, k: float) -> Vektor:
        return Vektor(self.x * k, self.y * k)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vektor):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Vektor({self.x}, {self.y})"

a = Vektor(1, 2)
b = Vektor(3, 4)
print(a + b)           # Vektor(4, 6)
print(b - a)           # Vektor(2, 2)
print(a * 3)           # Vektor(3, 6)
```

</details>

<details markdown="1">
<summary>Masala 16</summary>

```python
from abc import ABC, abstractmethod

class Shakl(ABC):
    @abstractmethod
    def yuza(self) -> float:
        ...

class Doira(Shakl):
    def __init__(self, r: float):
        self.r = r

    def yuza(self) -> float:
        return 3.14159 * self.r ** 2

class Kvadrat(Shakl):
    def __init__(self, tomon: float):
        self.tomon = tomon

    def yuza(self) -> float:
        return self.tomon ** 2

print(Doira(5).yuza())     # 78.53975
print(Kvadrat(4).yuza())   # 16
try:
    Shakl()
except TypeError as e:
    print("Abstrakt klassdan obyekt bo'lmaydi")
```

</details>

<details markdown="1">
<summary>Masala 17</summary>

```python
class Fayl:
    def __enter__(self) -> "Fayl":
        print("ochildi")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print("yopildi")
        return False

try:
    with Fayl():
        print("ish ketmoqda")
        raise ValueError("xato")
except ValueError:
    print("xato ushlandi")
# Chiqish: ochildi / ish ketmoqda / yopildi / xato ushlandi
```

</details>

<details markdown="1">
<summary>Masala 18</summary>

```python
from functools import total_ordering

@total_ordering
class Versiya:
    def __init__(self, katta: int, kichik: int):
        self.katta = katta
        self.kichik = kichik

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Versiya):
            return NotImplemented
        return (self.katta, self.kichik) == (other.katta, other.kichik)

    def __lt__(self, other: "Versiya") -> bool:
        return (self.katta, self.kichik) < (other.katta, other.kichik)

    def __repr__(self) -> str:
        return f"{self.katta}.{self.kichik}"

v = [Versiya(1, 5), Versiya(2, 0), Versiya(1, 2)]
print(sorted(v))       # [1.2, 1.5, 2.0]
```

</details>

<details markdown="1">
<summary>Masala 19</summary>

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Pul:
    miqdor: int
    valyuta: str = "UZS"

p = Pul(1000)
xarita = {p: "asosiy"}     # dict kaliti bo'la oldi
print(xarita[Pul(1000)])   # asosiy
try:
    p.miqdor = 2000
except Exception as e:
    print(type(e).__name__)   # FrozenInstanceError
```

</details>

<details markdown="1">
<summary>Masala 20</summary>

```python
class Kopaytiruvchi:
    def __init__(self, k: float):
        self.k = k

    def __call__(self, x: float) -> float:
        return x * self.k

uch = Kopaytiruvchi(3)
print(uch(10))             # 30
print(callable(uch))       # True
```

</details>

---

[← Muntazam ifodalar (regex)](./16-regex.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Type hints — chuqur →](./18-typing-chuqur.md)
