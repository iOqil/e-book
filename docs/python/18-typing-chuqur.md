# 18 — Type hints — chuqur (`Protocol`, `Generic`, `mypy`)

10-bobda tip ko'rsatmalarining asosini ko'rdik: `ism: str`, `def qosh(a: int) -> int`, `int | None`. Bu kundalik ish uchun yetarli edi. Lekin haqiqiy loyihalarda (Django, FastAPI, kutubxona yozish) kod murakkablashadi: bitta funksiya turli tiplar bilan ishlaydi, lug'at aniq "shaklga" ega bo'ladi, parametr faqat ma'lum qiymatlarni qabul qiladi. Mana shu yerda **ilg'or tip tizimi** ishga tushadi — u kodingni hujjatlaydi, muharrir (IDE) to'liq yordam beradi, va eng muhimi: xatoni **dasturni ishga tushirmasdan**, hali yozayotganingdayoq tutadi.

Tasavvur qil: 50 ming qatorli loyihada bir funksiyaning parametrini o'zgartirding. Uni 30 joyda chaqirishgan. Qaysi biri endi buzildi? `mypy` (statik tekshiruvchi) bir soniyada barchasini topib beradi — qo'lda izlash o'rniga. Bu bob aynan shu kuchni beradi.

> **Bu modulda:** zamonaviy generic sintaksis (`list[int]`, `X | None`), `Callable`, `Any` va undan qochish, `TypeVar`/`Generic` va PEP 695 (`class Box[T]`), `Protocol` (strukturaviy tip), `TypedDict`, `Literal`, `Final`, `Self`, `@overload`, `cast`, `TYPE_CHECKING`, va `mypy`/`pyright` bilan statik tekshiruv.

---

## 18.1 Nega umuman tip yozamiz? (4 sabab)

Python tipni majburlamaydi — kod tipsiz ham ishlaydi. Unda nega bezovta bo'lamiz? To'rtta aniq sabab:

1. **Xatoni erta tutish.** `mypy` kabi vosita kodni ishga tushirmasdan xatoni topadi. `None` ga `.upper()` chaqirsang — ish vaqtida `AttributeError` o'rniga, hali yozayotganingda ogohlantiradi.
2. **IDE yordami.** Muharrir tipni bilsa, avtomatik to'ldirish (autocomplete) aniq ishlaydi: `talaba.` deganda faqat `Talaba`ning metodlari chiqadi.
3. **Hujjat.** Tip o'zi hujjat. `def jonat(xabar: Xabar, urinishlar: int = 3) -> bool` — izohsiz ham hammasi tushunarli.
4. **Xavfsiz refaktoring.** Funksiya tipini o'zgartirsang, mos kelmagan barcha chaqiruvlar yonib qoladi.

```python
def yosh_kategoriya(yosh: int) -> str:
    if yosh < 18:
        return "voyaga yetmagan"
    return "kattalar"

print(yosh_kategoriya(25))     # kattalar
```

Tip yozish — qo'shimcha mehnat, lekin u o'zini bir necha barobar qaytaradi. Quyida buni isbotlaymiz.

---

## 18.2 Zamonaviy generic sintaksis: `list[int]`, `dict[str, int]`, `tuple`

To'plamlarning **ichidagi** tipni ko'rsatish — eng ko'p ishlatiladigan narsa. Python 3.9+ da to'g'ridan-to'g'ri o'rnatilgan tiplarni ishlatasan (eski `typing.List` kerak emas):

```python
ismlar: list[str] = ["Ali", "Vali"]
narxlar: dict[str, float] = {"olma": 1.5, "non": 3.0}
juftlik: tuple[int, str] = (1, "birinchi")        # aniq 2 element, har xil tip
sonlar: set[int] = {1, 2, 3}

def umumiy_narx(savat: dict[str, float]) -> float:
    return sum(savat.values())

print(umumiy_narx(narxlar))      # 4.5
```

`tuple` ikki xil ishlatiladi:

```python
# 1) Aniq uzunlik, har pozitsiya o'z tipi:
koordinata: tuple[int, int] = (10, 20)
yozuv: tuple[str, int, bool] = ("Ali", 25, True)

# 2) Noma'lum uzunlik, bir xil tip — `...` (ellipsis):
ballar: tuple[int, ...] = (90, 85, 100, 70)   # har qancha int
```

> **Eslatma:** `list[str]` "str'lardan iborat ro'yxat" degani. Bu Python'ni o'zgartirmaydi — ish vaqtida hech narsa tekshirilmaydi. Faqat `mypy` va IDE buni o'qiydi.

---

## 18.3 `X | None` va `X | Y` — union (birlashma) tiplar

Bir o'zgaruvchi bir nechta tipdan biri bo'lishi mumkin bo'lsa, `|` (union) ishlatasan. Python 3.10 dan bu sintaksis ishlaydi:

```python
def topish(ismlar: list[str], qidiruv: str) -> int | None:
    for i, ism in enumerate(ismlar):
        if ism == qidiruv:
            return i
    return None                      # topilmasa None

natija = topish(["a", "b"], "b")
print(natija)                        # 1
```

`int | None` — "int **yoki** None". Bu eng ko'p uchraydigan union. Boshqa union'lar ham bo'ladi:

```python
def uzunlik(qiymat: str | list[int]) -> int:
    return len(qiymat)               # ikkalasida ham len() ishlaydi

print(uzunlik("salom"))              # 5
print(uzunlik([1, 2, 3]))            # 3
```

> **`Optional[int]` vs `int | None`:** ikkalasi bir xil ma'no — "int yoki None". `Optional` eski uslub (`from typing import Optional`). Zamonaviy kodda `int | None` yoz — qisqaroq va aniq. `Optional` ni faqat eski kodda ko'rasan.

**Union'ni "toraytirish" (narrowing).** Union bilan ishlaganda Python (va mypy) `if` tekshiruvi ichida tipni aniqlashtiradi:

```python
def qayta_ishla(x: int | str) -> str:
    if isinstance(x, int):
        return str(x * 2)            # bu yerda x — aniq int
    return x.upper()                 # bu yerda x — aniq str

print(qayta_ishla(5))                # 10
print(qayta_ishla("ha"))             # HA
```

---

## 18.4 `Callable` — funksiyani parametr sifatida

Funksiya boshqa funksiyani qabul qilsa (callback, dekorator, `sorted`ning `key`i), uning tipini `Callable[[argumentlar], qaytish]` bilan yozasan:

```python
from collections.abc import Callable

def ikki_marta_qolla(f: Callable[[int], int], x: int) -> int:
    return f(f(x))                   # f ni ikki marta qo'llaydi

def qoshuv(n: int) -> int:
    return n + 3

print(ikki_marta_qolla(qoshuv, 10))  # 16  (10+3=13, 13+3=16)
```

`Callable[[int], int]` — "bitta int qabul qilib, int qaytaruvchi funksiya". Bir nechta argument:

```python
from collections.abc import Callable

def hisobla(amal: Callable[[int, int], int], a: int, b: int) -> int:
    return amal(a, b)

print(hisobla(lambda x, y: x + y, 4, 5))    # 9
print(hisobla(lambda x, y: x * y, 4, 5))    # 20
```

> **Qayerdan import?** Zamonaviy kodda `from collections.abc import Callable` ishlat (`typing.Callable` ham bor, lekin eskirgan uslub). Argument soni noma'lum bo'lsa: `Callable[..., int]` (har qanday argument, int qaytaradi).

---

## 18.5 `Any` — va undan nega qochish kerak

`Any` — "har qanday tip, tekshirmaslik". U tip tizimini **o'chiradi**:

```python
from typing import Any

def ishla(x: Any) -> Any:
    return x.istalgan_metod()        # mypy hech narsa demaydi — xavfli!
```

`Any` bilan mypy tekshiruvni to'xtatadi: `x` ga istalgan amalni qilsang ham shikoyat qilmaydi. Bu — tip yozishdan voz kechish bilan teng. Shuning uchun **iloji boricha qochish kerak**.

Ko'pincha `Any` o'rniga aniqroq variant bor:

```python
from typing import Any

# YOMON — Any:
def birinchi_any(royxat: list[Any]) -> Any: ...

# YAXSHI — object (eng umumiy, lekin xavfsiz tip):
def chiqar(qiymat: object) -> None:
    print(qiymat)                    # object'da print ishlaydi

# YANA YAXSHI — generic (keyingi bo'limda):
def birinchi[T](royxat: list[T]) -> T:
    return royxat[0]
```

> **`object` vs `Any` farqi:** `object` — "har qanday qiymat, lekin men uni ehtiyot ishlataman" (faqat barcha obyektlarda bor amallar mumkin). `Any` — "tekshirishni butunlay o'chir". `object` xavfsiz, `Any` xavfli. Tashqi (JSON, kutubxona) ma'lumot uchun ba'zan `Any` zarur, lekin imkon qadar tezroq aniq tipga o'tkaz.

---

## 18.6 `TypeVar` — generic funksiya (klassik usul)

Yuqorida `birinchi` funksiyasini ko'rdik: u ro'yxatning birinchi elementini qaytaradi. U `list[int]` uchun ham, `list[str]` uchun ham ishlashi kerak — va qaytgan tip **kiruvchi tipga mos** bo'lsin. Buni `TypeVar` (tip o'zgaruvchisi) hal qiladi:

```python
from typing import TypeVar

T = TypeVar("T")                     # "qandaydir tip" — nomi T

def birinchi(royxat: list[T]) -> T:  # kirsa list[T], chiqsa T
    return royxat[0]

s = birinchi(["a", "b", "c"])        # mypy biladi: s — str
n = birinchi([10, 20, 30])           # mypy biladi: n — int
print(s, n)                          # a 10
```

Sehr shunda: `T` — "joker tip". `list[int]` kirsa, `T` = `int` bo'ladi va funksiya `int` qaytaradi. `list[str]` kirsa — `str`. Bitta funksiya, har tip uchun **to'g'ri** natija tipi. `Any` bo'lganda bunday aniqlik yo'qolardi.

`TypeVar`ni cheklash ham mumkin (`bound` — faqat shu tip yoki uning avlodlari):

```python
from typing import TypeVar

Son = TypeVar("Son", int, float)     # faqat int yoki float

def qoshish(a: Son, b: Son) -> Son:
    return a + b

print(qoshish(3, 4))                 # 7    (int)
print(qoshish(1.5, 2.5))             # 4.0  (float)
```

---

## 18.7 PEP 695 — yangi sintaksis (`def f[T]`, `class Box[T]`, `type`)

Python 3.12 dan generic yozishning **ancha qisqa** yo'li bor — `TypeVar`ni alohida e'lon qilish kerak emas. To'g'ridan-to'g'ri kvadrat qavsda yozasan:

```python
# Eski (3.11 va oldin):
from typing import TypeVar
T = TypeVar("T")
def birinchi_eski(royxat: list[T]) -> T:
    return royxat[0]

# Yangi (3.12+) — TypeVar e'loni kerak emas:
def birinchi[T](royxat: list[T]) -> T:
    return royxat[0]

print(birinchi([1, 2, 3]))           # 1
print(birinchi(["x", "y"]))          # x
```

`type` kalit so'zi bilan **tip taxallusi** (alias — uzun tipga qisqa nom) yaratasan:

```python
type Vektor = list[float]            # endi Vektor = list[float]
type Jadval = dict[str, list[int]]

def uzunlik(v: Vektor) -> float:
    return sum(x * x for x in v) ** 0.5

print(round(uzunlik([3.0, 4.0]), 1))   # 5.0
```

Bu boblar oxirida generic klassni ham yangi sintaksisda yozamiz. Yangi sintaksis — zamonaviy kodda afzal.

---

## 18.8 `Generic` — o'z generic klassing

Funksiyagina emas, **klass** ham generic bo'lishi mumkin. Masalan, "qutiga istalgan tipdagi qiymat solib, keyin xuddi shu tipda olib chiqaman". Avval klassik usul (`Generic` bilan):

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Quti(Generic[T]):              # T parametrli generic klass
    def __init__(self, qiymat: T) -> None:
        self._qiymat = qiymat

    def ol(self) -> T:
        return self._qiymat

    def almashtir(self, yangi: T) -> None:
        self._qiymat = yangi

q_int = Quti(42)                     # mypy: Quti[int]
print(q_int.ol())                    # 42
q_str = Quti("salom")                # mypy: Quti[str]
print(q_str.ol().upper())            # SALOM
```

Endi **yangi sintaksis (3.12+)** bilan — `Generic` va `TypeVar` kerak emas:

```python
class Quti[T]:                       # to'g'ridan-to'g'ri [T]
    def __init__(self, qiymat: T) -> None:
        self._qiymat = qiymat

    def ol(self) -> T:
        return self._qiymat

q = Quti([1, 2, 3])                  # Quti[list[int]]
print(q.ol())                        # [1, 2, 3]
```

Real misol — generic "stek" (ikkala tip xavfsiz):

```python
class Stek[T]:
    def __init__(self) -> None:
        self._elementlar: list[T] = []

    def qosh(self, x: T) -> None:
        self._elementlar.append(x)

    def ol(self) -> T:
        return self._elementlar.pop()

    def bosh(self) -> bool:
        return len(self._elementlar) == 0

s: Stek[int] = Stek()
s.qosh(1)
s.qosh(2)
print(s.ol())                        # 2
print(s.bosh())                      # False
```

---

## 18.9 `Protocol` — strukturaviy tiplilik (duck typing'ning tipi)

Bu — bobning eng muhim qismi. Odatda tip "merosga" asoslanadi: `It` — `Hayvon` avlodi bo'lsa, `Hayvon` o'rniga ishlatish mumkin. Lekin ko'pincha bizga **meros emas, shakl** kerak: "menga `.maydon()` metodi bor istalgan obyekt bo'ladi — u kim avlodi ekani muhim emas". Bu — **strukturaviy tiplilik** (duck typing: "agar o'rdakdek qaqillasa, u o'rdak").

`Protocol` aynan shuni beradi: "shu metod/atributlar bor bo'lsa, mos keladi":

```python
from typing import Protocol

class Maydonli(Protocol):            # "shartnoma": maydon() metodi bor
    def maydon(self) -> float: ...

class Doira:                         # Maydonli'dan MEROS OLMAYDI!
    def __init__(self, r: float) -> None:
        self.r = r
    def maydon(self) -> float:
        return 3.14159 * self.r ** 2

class Kvadrat:                       # bu ham meros olmaydi
    def __init__(self, tomon: float) -> None:
        self.tomon = tomon
    def maydon(self) -> float:
        return self.tomon ** 2

def umumiy_maydon(shakllar: list[Maydonli]) -> float:
    return sum(sh.maydon() for sh in shakllar)

# Doira ham, Kvadrat ham `maydon()` ga ega — shuning uchun mos keladi:
print(umumiy_maydon([Doira(2), Kvadrat(3)]))    # 21.56636
```

Diqqat: `Doira` va `Kvadrat` `Maydonli`dan **meros olmadi**. Ular shunchaki `maydon()` metodiga ega — shu yetarli. `mypy` buni tekshiradi: agar biror shaklda `maydon()` bo'lmasa, xato beradi.

Bu FastAPI, dependency injection va "plug-in" arxitekturasida juda muhim — sen interfeysga emas, **shaklga** bog'lanasan. Real misol — "yozish mumkin bo'lgan" har qanday obyekt:

```python
from typing import Protocol

class Yozuvchi(Protocol):
    def write(self, matn: str) -> int: ...   # write metodi bor

def hisobot_yoz(chiqish: Yozuvchi, qatorlar: list[str]) -> None:
    for q in qatorlar:
        chiqish.write(q + "\n")

import sys, io
hisobot_yoz(sys.stdout, ["birinchi", "ikkinchi"])   # ekranga yozadi
bufer = io.StringIO()
hisobot_yoz(bufer, ["a", "b"])       # xotiraga yozadi — ikkalasida write bor
print(repr(bufer.getvalue()))        # 'a\nb\n'
```

> **`@runtime_checkable`:** odatda `Protocol` faqat statik tekshiriladi. `isinstance(x, Maydonli)` ishlatmoqchi bo'lsang, protokolga `@runtime_checkable` dekoratorini qo'sh (lekin u faqat metod **borligini** tekshiradi, imzosini emas).

---

## 18.10 `TypedDict` — lug'atning aniq shakli (JSON/API uchun)

Oddiy `dict[str, ...]` lug'atning ichida qaysi kalitlar borligini bilmaydi. Lekin JSON/API bilan ishlaganda lug'at **aniq shaklga** ega bo'ladi: `{"ism": str, "yosh": int}`. `TypedDict` shu shaklni e'lon qiladi:

```python
from typing import TypedDict

class Foydalanuvchi(TypedDict):
    ism: str
    yosh: int
    faolmi: bool

u: Foydalanuvchi = {"ism": "Ali", "yosh": 25, "faolmi": True}
print(u["ism"])                      # Ali

def tavsif(f: Foydalanuvchi) -> str:
    holat = "faol" if f["faolmi"] else "nofaol"
    return f"{f['ism']}, {f['yosh']} yosh ({holat})"

print(tavsif(u))                     # Ali, 25 yosh (faol)
```

`mypy` endi biladi: `u["ism"]` — `str`, `u["yosh"]` — `int`. Agar `u["isim"]` (xato kalit) yozsang yoki `yosh`ga string bersang — ogohlantiradi. Bu API javoblarini ishonchli qiladi.

Ixtiyoriy kalitlar uchun `total=False` yoki `NotRequired`:

```python
from typing import TypedDict, NotRequired

class Sozlama(TypedDict):
    til: str                         # majburiy
    mavzu: NotRequired[str]          # ixtiyoriy — bo'lmasligi mumkin

s1: Sozlama = {"til": "uz"}                      # OK — mavzu yo'q
s2: Sozlama = {"til": "uz", "mavzu": "tungi"}    # OK
print(s1, s2)
```

> **`TypedDict` vs `dataclass`:** `TypedDict` — oddiy **lug'at** (JSON'dan to'g'ridan-to'g'ri keladi, `["kalit"]` bilan murojaat). `dataclass` — to'liq **obyekt** (`.atribut` bilan murojaat, metodlar bo'lishi mumkin). API javoblari uchun `TypedDict`, ichki model uchun `dataclass` qulay.

---

## 18.11 `Literal` — faqat aniq qiymatlar

Ba'zan parametr **faqat sanab o'tilgan qiymatlarni** qabul qilishi kerak: rang faqat `"qizil"`, `"yashil"`, `"ko'k"` bo'lsin. `Literal` aynan shuni cheklaydi:

```python
from typing import Literal

def buyur(yon: Literal["chap", "ong"], qadam: int) -> str:
    return f"{qadam} qadam {yon}ga"

print(buyur("chap", 3))              # 3 qadam chapga
# buyur("yuqori", 2)  -> mypy XATO: "yuqori" ruxsat etilmagan
```

`mypy` `buyur("yuqori", ...)` ni xato deb belgilaydi — chunki `"yuqori"` ro'yxatda yo'q. Bu xatolarni yozayotgan paytda tutadi. Real misol — HTTP metodi:

```python
from typing import Literal

Metod = Literal["GET", "POST", "PUT", "DELETE"]

def sorov(metod: Metod, url: str) -> str:
    return f"{metod} {url}"

print(sorov("GET", "/api/users"))    # GET /api/users
print(sorov("POST", "/api/users"))   # POST /api/users
```

> **`Literal` vs `Enum`:** ikkalasi ham "aniq qiymatlar to'plami" beradi. `Literal` — yengil, string/int bilan ishlaydi, JSON'ga mos. `Enum` — to'liq obyekt (`Rang.QIZIL`), boyroq lekin og'irroq. API/sozlama uchun ko'pincha `Literal` yetarli.

---

## 18.12 `Final` — o'zgarmas qiymat

`Final` — "bu o'zgaruvchini qayta o'zgartirma" deb belgilaydi. Konstantalar uchun:

```python
from typing import Final

PI: Final = 3.14159
MAKS_URINISH: Final[int] = 3

print(PI * 2)                        # 6.28318
# PI = 3.14   -> mypy XATO: Final qiymatni qayta yozib bo'lmaydi
```

Bu Python'da qiymatni haqiqatan qulflamaydi (ish vaqtida o'zgartirish mumkin), lekin `mypy` qayta o'zlashtirishni xato deb belgilaydi. Klass atributlari uchun ham ishlaydi — meros vaqtida ustiga yozishni taqiqlaydi.

---

## 18.13 `Self` — o'zini qaytaruvchi metodlar

Metod "o'zini" qaytarganda (zanjirli chaqiruv — method chaining), qaytish tipini `Self` bilan yozasan. Python 3.11 dan:

```python
from typing import Self

class Sorovchi:
    def __init__(self) -> None:
        self.qismlar: list[str] = []

    def tanla(self, nima: str) -> Self:      # o'zini qaytaradi
        self.qismlar.append(f"SELECT {nima}")
        return self

    def jadval(self, nom: str) -> Self:
        self.qismlar.append(f"FROM {nom}")
        return self

    def qur(self) -> str:
        return " ".join(self.qismlar)

natija = Sorovchi().tanla("*").jadval("users").qur()
print(natija)                        # SELECT * FROM users
```

`Self`ning kuchi: agar `Sorovchi`dan avlod klass yasasang, `tanla()` o'sha **avlod** tipini qaytaradi (`Sorovchi` emas). `def tanla(self) -> "Sorovchi"` yozganingda bu ishlamasdi. Method chaining (FastAPI, SQLAlchemy, ORM) uchun ideal.

---

## 18.14 `@overload` — bir funksiya, bir nechta imzo

Ba'zan funksiya **kiruvchi tipga qarab boshqacha tip qaytaradi**. Masalan: int bersang int qaytar, string bersang string. `@overload` har bir holatni alohida e'lon qiladi:

```python
from typing import overload

@overload
def ikki_marta(x: int) -> int: ...
@overload
def ikki_marta(x: str) -> str: ...

def ikki_marta(x: int | str) -> int | str:   # asl (yagona) amalga oshirish
    return x * 2

a = ikki_marta(5)                    # mypy biladi: a — int
b = ikki_marta("ab")                 # mypy biladi: b — str
print(a, b)                          # 10 abab
```

`@overload` bilan belgilangan ikkita versiya — faqat `mypy` uchun "xarita". Haqiqiy kod — pastdagi oddiy funksiya. `mypy` endi `ikki_marta(5)` ning int ekanini, `ikki_marta("ab")` ning str ekanini aniq biladi (oddiy `int | str` qaytsa, bu aniqlik yo'qolardi).

---

## 18.15 `cast` va `TYPE_CHECKING` — qiyin holatlar

**`cast`** — "men bu tipni `mypy`dan yaxshiroq bilaman, ishon" deb aytish. Ish vaqtida hech narsa qilmaydi, faqat `mypy`ga maslahat:

```python
from typing import cast

def json_ol() -> object:             # tashqi manba — aniq tip noma'lum
    return {"ism": "Ali", "yosh": 25}

malumot = json_ol()
# mypy malumot'ni object deb biladi — biz aniqlashtiramiz:
sozlangan = cast(dict[str, object], malumot)
print(sozlangan["ism"])              # Ali
```

> **`cast` ehtiyotkorlik talab qiladi:** u tekshirmaydi, faqat `mypy`ni jim qiladi. Noto'g'ri `cast` ish vaqtida xato keltirib chiqaradi. Faqat haqiqatan bilganingda ishlat.

**`TYPE_CHECKING`** — aylanma import (circular import) muammosini hal qiladi. Ba'zan ikki fayl bir-birini import qilishi kerak (faqat tip uchun). Bu ish vaqtida xatoga olib keladi. `TYPE_CHECKING` faqat `mypy` paytida `True` bo'ladi:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence    # faqat mypy ko'radi, ish vaqtida import bo'lmaydi

def jami(sonlar: Sequence[int]) -> int:      # tip annotatsiyasi string sifatida saqlanadi
    return sum(sonlar)

print(jami([1, 2, 3]))               # 6
```

`from __future__ import annotations` annotatsiyalarni "matn" sifatida saqlaydi — shuning uchun `Sequence` ish vaqtida kerak bo'lmaydi, faqat `mypy` uni tekshiradi. Aylanma importlarni shunday sindirasan.

---

## 18.16 `mypy` — statik tekshiruvni amalda ishlatish

`mypy` — eng mashhur statik tip tekshiruvchi. U kodingni **ishga tushirmasdan** o'qiydi va tip xatolarini topadi. O'rnatish:

```bash
pip install mypy
```

Faraz qilaylik, `dastur.py` faylimiz bor:

```python
def salomla(ism: str) -> str:
    return "Salom, " + ism

salomla(42)            # XATO: int berdik, str kutilgan
```

Terminalda tekshir:

```bash
mypy dastur.py
```

`mypy` shunday natija beradi:

```
dastur.py:4: error: Argument 1 to "salomla" has incompatible type "int"; expected "str"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

Dasturni umuman ishga tushirmasdan, mypy xatoni **4-qatorda** topdi. Yana bir tipik xato — `None`ga murojaat:

```python
def topish(ismlar: list[str], q: str) -> int | None:
    for i, ism in enumerate(ismlar):
        if ism == q:
            return i
    return None

natija = topish(["a", "b"], "x")
print(natija + 1)      # XATO: natija None bo'lishi mumkin!
```

`mypy` aytadi:

```
dastur.py:8: error: Unsupported operand types for + ("None" and "int")  [operator]
```

Bu — eng qimmatli foyda: `None` xatolarini ish vaqtida emas, oldindan tutish. Tuzatish — avval `None`ni tekshirish:

```python
natija = topish(["a", "b"], "x")
if natija is not None:
    print(natija + 1)    # endi mypy xotirjam — bu yerda natija aniq int
```

**Foydali mypy bayroqlari:**

```bash
mypy --strict dastur.py        # eng qattiq rejim (yangi loyihalarga tavsiya)
mypy dastur.py --pretty        # chiroyli, rangli chiqish
```

> **`pyright`:** Microsoft'ning muqobil tekshiruvchisi (VS Code'dagi Pylance shunga asoslangan). Tezroq va ko'pincha aniqroq. `pip install pyright` yoki VS Code'da avtomatik. Ikkalasi bir xil tip tizimini tushunadi — bittasini tanla.

---

## 18.17 Hammasini birlashtirgan real misol

Quyida bu bobning ko'p tushunchasi bitta kichik "vazifa boshqaruvchi"da jamlangan — `TypedDict`, `Literal`, `Protocol`, generic, `Self`:

```python
from typing import TypedDict, Literal, Protocol, Self

Holat = Literal["yangi", "jarayonda", "tugadi"]

class Vazifa(TypedDict):
    id: int
    nom: str
    holat: Holat

class Saqlovchi(Protocol):           # qanday saqlanishi muhim emas — shakl muhim
    def saqla(self, v: Vazifa) -> None: ...
    def barchasi(self) -> list[Vazifa]: ...

class XotiraSaqlovchi:               # Saqlovchi'dan meros OLMAYDI, shaklga mos
    def __init__(self) -> None:
        self._db: list[Vazifa] = []
    def saqla(self, v: Vazifa) -> None:
        self._db.append(v)
    def barchasi(self) -> list[Vazifa]:
        return self._db

class Loyiha:
    def __init__(self, saqlovchi: Saqlovchi) -> None:
        self.saqlovchi = saqlovchi
        self._keyingi_id = 1
    def qosh(self, nom: str) -> Self:                # zanjir uchun Self
        v: Vazifa = {"id": self._keyingi_id, "nom": nom, "holat": "yangi"}
        self.saqlovchi.saqla(v)
        self._keyingi_id += 1
        return self
    def hisobot(self) -> str:
        return "\n".join(f"#{v['id']} {v['nom']} [{v['holat']}]"
                         for v in self.saqlovchi.barchasi())

loyiha = Loyiha(XotiraSaqlovchi())
loyiha.qosh("Dizayn").qosh("Kodlash").qosh("Test")
print(loyiha.hisobot())
# #1 Dizayn [yangi]
# #2 Kodlash [yangi]
# #3 Test [yangi]
```

Bu yerda `Loyiha` `XotiraSaqlovchi`ga emas, `Saqlovchi` **protokoliga** bog'langan. Ertaga `FaylSaqlovchi` yoki `BazaSaqlovchi` yozsang — `saqla()` va `barchasi()` metodlari bo'lsa — hech narsa o'zgartirmasdan ishlaydi. Bu — tip tizimining haqiqiy kuchi.

---

## ✍️ Masalalar (20 ta)

> Bu masalalar shu bob (18) va oldingi boblar mavzulariga asoslangan. Imkon bo'lsa, yechimni `mypy fayl.py` bilan tekshir.

**Oson (1–7):**

1. `kvadrat(n)` funksiyasini tipla: `int` qabul qilib `int` qaytarsin (`n * n`).
2. `bosh_harf(matn)` funksiyasini tipla: `str` qabul qilib `str` qaytarsin (birinchi harfni katta qiladi).
3. `ortacha(sonlar)` funksiyasini tipla: `list[float]` qabul qilib `float` qaytarsin.
4. `topish(royxat, qiymat)` ni tipla: `list[int]` va `int` qabul qilib, indeks yoki topilmasa `None` qaytarsin (`int | None`).
5. `narxlar` lug'atini tipla: kalit `str`, qiymat `float` (`dict[str, float]`).
6. `koordinata` o'zgaruvchisini tipla: ikkita `int`dan iborat tuple.
7. `birlash(a, b)` ni tipla: `str | int` ikkita qabul qilib, string qaytarsin.

**O'rta (8–14):**

8. `Quti[T]` generic klassini yangi sintaksisda (`class Quti[T]`) yoz: `qosh(x)` va `ol()` metodlari bilan.
9. `Nuqta` `TypedDict`ini yoz: `x: int`, `y: int`. Funksiya nuqtalar ro'yxatidan eng o'ngdagisini topsin.
10. `loglash(daraja, xabar)` ni `Literal`bilan tipla: `daraja` faqat `"info"`, `"warn"`, `"error"` bo'lsin.
11. `Mahsulot` `TypedDict`ini yoz (`nom: str`, `narx: float`). Savatdagi umumiy narxni hisoblovchi funksiya tiplab yoz.
12. Generic `oxirgi[T](royxat: list[T]) -> T` funksiyasini yoz — oxirgi elementni qaytarsin.
13. `Sozlama` `TypedDict`ini `NotRequired` bilan yoz: `til: str` majburiy, `mavzu: str` ixtiyoriy.
14. `Stek[T]` generic klassini yoz (`qosh`, `ol`, `bosh`). `Stek[str]` bilan sinab ko'r.

**Murakkab (15–20):**

15. `Maydonli` `Protocol`ini yoz (`maydon() -> float`). `Uchburchak` va `Doira` klasslarini meros **olmasdan** unga mos qilib yoz; ro'yxatdagi umumiy maydonni hisobla.
16. `Taqqoslovchi` protokolini yoz (`__lt__` metodi bor). Generic `eng_kichik` funksiyasini `TypeVar` bound bilan yoz.
17. `@overload` bilan `ol(manba)` funksiyasini yoz: `list` bersang oxirgi elementni, `str` bersang oxirgi harfni qaytarsin (mos tip bilan).
18. `Yozuvchi` protokolini yoz (`write(s: str) -> int`). Funksiya har qanday "yozuvchi"ga matn yozsin (`sys.stdout` ham, `io.StringIO()` ham mos kelsin).
19. `Sorovchi` klassini `Self` bilan yoz — `where(shart)` va `qur()` metodlari zanjir bilan ishlasin.
20. Quyidagi kodda `mypy` topadigan **2 ta** tip xatosini ayt va tuzat:
    ```python
    def salomla(ism: str) -> str:
        return "Salom " + ism
    def yosh_olish() -> int | None:
        return None
    natija = salomla(123)
    print(yosh_olish() + 5)
    ```

---

## ✅ Yechimlar

<details markdown="1">
<summary>Masala 1</summary>

```python
def kvadrat(n: int) -> int:
    return n * n

print(kvadrat(5))            # 25
```
</details>

<details markdown="1">
<summary>Masala 2</summary>

```python
def bosh_harf(matn: str) -> str:
    return matn.capitalize()

print(bosh_harf("salom"))    # Salom
```
</details>

<details markdown="1">
<summary>Masala 3</summary>

```python
def ortacha(sonlar: list[float]) -> float:
    return sum(sonlar) / len(sonlar)

print(ortacha([2.0, 4.0, 6.0]))   # 4.0
```
</details>

<details markdown="1">
<summary>Masala 4</summary>

```python
def topish(royxat: list[int], qiymat: int) -> int | None:
    for i, x in enumerate(royxat):
        if x == qiymat:
            return i
    return None

print(topish([10, 20, 30], 20))   # 1
print(topish([10, 20], 99))       # None
```
</details>

<details markdown="1">
<summary>Masala 5</summary>

```python
narxlar: dict[str, float] = {"olma": 1.5, "non": 3.0}
print(narxlar["olma"])       # 1.5
```
</details>

<details markdown="1">
<summary>Masala 6</summary>

```python
koordinata: tuple[int, int] = (10, 20)
print(koordinata)            # (10, 20)
```
</details>

<details markdown="1">
<summary>Masala 7</summary>

```python
def birlash(a: str | int, b: str | int) -> str:
    return f"{a}{b}"

print(birlash("son: ", 42))  # son: 42
print(birlash(1, 2))         # 12
```
</details>

<details markdown="1">
<summary>Masala 8</summary>

```python
class Quti[T]:
    def __init__(self) -> None:
        self._qiymat: T | None = None
    def qosh(self, x: T) -> None:
        self._qiymat = x
    def ol(self) -> T | None:
        return self._qiymat

q: Quti[int] = Quti()
q.qosh(42)
print(q.ol())                # 42
```
</details>

<details markdown="1">
<summary>Masala 9</summary>

```python
from typing import TypedDict

class Nuqta(TypedDict):
    x: int
    y: int

def eng_ongdagi(nuqtalar: list[Nuqta]) -> Nuqta:
    return max(nuqtalar, key=lambda n: n["x"])

nuqtalar: list[Nuqta] = [{"x": 1, "y": 2}, {"x": 5, "y": 0}, {"x": 3, "y": 9}]
print(eng_ongdagi(nuqtalar))      # {'x': 5, 'y': 0}
```
</details>

<details markdown="1">
<summary>Masala 10</summary>

```python
from typing import Literal

def loglash(daraja: Literal["info", "warn", "error"], xabar: str) -> str:
    return f"[{daraja.upper()}] {xabar}"

print(loglash("info", "ishga tushdi"))    # [INFO] ishga tushdi
print(loglash("error", "tarmoq uzildi"))  # [ERROR] tarmoq uzildi
# loglash("debug", "...")  -> mypy XATO: "debug" ruxsat etilmagan
```
</details>

<details markdown="1">
<summary>Masala 11</summary>

```python
from typing import TypedDict

class Mahsulot(TypedDict):
    nom: str
    narx: float

def jami_narx(savat: list[Mahsulot]) -> float:
    return sum(m["narx"] for m in savat)

savat: list[Mahsulot] = [{"nom": "olma", "narx": 1.5}, {"nom": "non", "narx": 3.0}]
print(jami_narx(savat))      # 4.5
```
</details>

<details markdown="1">
<summary>Masala 12</summary>

```python
def oxirgi[T](royxat: list[T]) -> T:
    return royxat[-1]

print(oxirgi([1, 2, 3]))     # 3
print(oxirgi(["a", "b"]))    # b
```
</details>

<details markdown="1">
<summary>Masala 13</summary>

```python
from typing import TypedDict, NotRequired

class Sozlama(TypedDict):
    til: str
    mavzu: NotRequired[str]

s1: Sozlama = {"til": "uz"}
s2: Sozlama = {"til": "en", "mavzu": "tungi"}
print(s1, s2)
```
</details>

<details markdown="1">
<summary>Masala 14</summary>

```python
class Stek[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def qosh(self, x: T) -> None:
        self._items.append(x)
    def ol(self) -> T:
        return self._items.pop()
    def bosh(self) -> bool:
        return len(self._items) == 0

s: Stek[str] = Stek()
s.qosh("a")
s.qosh("b")
print(s.ol())                # b
print(s.bosh())              # False
```
</details>

<details markdown="1">
<summary>Masala 15</summary>

```python
from typing import Protocol

class Maydonli(Protocol):
    def maydon(self) -> float: ...

class Uchburchak:            # meros OLMAYDI
    def __init__(self, asos: float, balandlik: float) -> None:
        self.asos = asos
        self.balandlik = balandlik
    def maydon(self) -> float:
        return 0.5 * self.asos * self.balandlik

class Doira:                # bu ham meros olmaydi
    def __init__(self, r: float) -> None:
        self.r = r
    def maydon(self) -> float:
        return 3.14159 * self.r ** 2

def umumiy(shakllar: list[Maydonli]) -> float:
    return sum(sh.maydon() for sh in shakllar)

print(round(umumiy([Uchburchak(4, 3), Doira(2)]), 2))   # 18.57
```
</details>

<details markdown="1">
<summary>Masala 16</summary>

```python
from typing import Protocol, TypeVar, Any

class Taqqoslovchi(Protocol):
    def __lt__(self, boshqa: Any, /) -> bool: ...   # "<" amali bor

T = TypeVar("T", bound=Taqqoslovchi)

def eng_kichik(royxat: list[T]) -> T:
    natija = royxat[0]
    for x in royxat[1:]:
        if x < natija:
            natija = x
    return natija

print(eng_kichik([5, 2, 8, 1]))        # 1
print(eng_kichik(["banan", "olma"]))   # banan  (alifbo bo'yicha)
```

> **Eslatma:** `__lt__` parametrini `Any` qildik — chunki `int` va `str`ning `__lt__` imzosi har xil. `object` qo'ysak, `mypy` ularni mos kelmaydi deb hisoblaydi. Bu — strukturaviy tipning nozik joyi.
</details>

<details markdown="1">
<summary>Masala 17</summary>

```python
from typing import overload, Any

@overload
def ol(manba: list[Any]) -> Any: ...
@overload
def ol(manba: str) -> str: ...

def ol(manba: list[Any] | str) -> Any:
    return manba[-1]

print(ol([1, 2, 3]))         # 3
print(ol("salom"))           # m
```
</details>

<details markdown="1">
<summary>Masala 18</summary>

```python
from typing import Protocol
import sys, io

class Yozuvchi(Protocol):
    def write(self, s: str) -> int: ...

def yoz(chiqish: Yozuvchi, matn: str) -> None:
    chiqish.write(matn)

yoz(sys.stdout, "ekranga\n")     # ekranga yozadi
bufer = io.StringIO()
yoz(bufer, "xotiraga")
print(repr(bufer.getvalue()))    # 'xotiraga'
```
</details>

<details markdown="1">
<summary>Masala 19</summary>

```python
from typing import Self

class Sorovchi:
    def __init__(self, jadval: str) -> None:
        self.jadval = jadval
        self.shartlar: list[str] = []
    def where(self, shart: str) -> Self:
        self.shartlar.append(shart)
        return self
    def qur(self) -> str:
        sorov = f"SELECT * FROM {self.jadval}"
        if self.shartlar:
            sorov += " WHERE " + " AND ".join(self.shartlar)
        return sorov

natija = Sorovchi("users").where("yosh > 18").where("faol = 1").qur()
print(natija)
# SELECT * FROM users WHERE yosh > 18 AND faol = 1
```
</details>

<details markdown="1">
<summary>Masala 20</summary>

`mypy` ikkita xato beradi:
```
xato.py:5: error: Argument 1 to "salomla" has incompatible type "int"; expected "str"  [arg-type]
xato.py:6: error: Unsupported operand types for + ("None" and "int")  [operator]
```
1. `salomla(123)` — `123` `int`, lekin `str` kutilgan (`arg-type`).
2. `yosh_olish() + 5` — funksiya `None` qaytarishi mumkin, `None + int` ishlamaydi (`operator`). Tuzatish uchun natijani `None` ga tekshirish kerak.

Tuzatilgan kod:

```python
def salomla(ism: str) -> str:
    return "Salom " + ism

def yosh_olish() -> int | None:
    return None

natija = salomla("Ali")          # str berdik
print(natija)                    # Salom Ali

yosh = yosh_olish()
if yosh is not None:             # None tekshiruvi
    print(yosh + 5)
else:
    print("yosh noma'lum")       # yosh noma'lum
```

`mypy fayl.py` endi: `Success: no issues found in 1 source file`.
</details>

---

[← OOP — ilg'or](./17-oop-ilgor.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Funksional dasturlash →](./19-funksional.md)
