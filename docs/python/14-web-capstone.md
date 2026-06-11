# 14 — FastAPI bilan veb API

Hozirgacha yozgan dasturlarimiz faqat o'z kompyuteringda, terminalda ishladi. Lekin haqiqiy ilovalar (mobil ilova, sayt) ko'pincha **internet orqali** ma'lumot almashadi — buning uchun **veb API** kerak. Bu modulda **FastAPI** bilan oddiy, lekin ishlaydigan API yasashni o'rganasan. Bu — kursning kichik yakuniy loyihasi: oldingi modullardagi bilim (funksiyalar, lug'atlar, tip ko'rsatmalari) shu yerda birlashadi.

> **Bu modulda:** veb API nima, FastAPI'da birinchi API, parametrlar (path va query), Pydantic bilan ma'lumotni qabul qilish, oddiy CRUD (qo'shish/o'qish/o'zgartirish/o'chirish), `async`/`await`, Dependency Injection (`Depends`), `response_model` va status kodlar, `Annotated` bilan validatsiya, `APIRouter` va middleware (CORS), oddiy autentifikatsiya (JWT), `TestClient` bilan test va `uvicorn` bilan deploy.

---

## 14.1 Veb API nima?

API — bu dasturlar bir-biri bilan "gaplashadigan" til. Veb API esa internet orqali ishlaydi: mijoz (brauzer, mobil ilova) **so'rov** (request) yuboradi, server **javob** (response) qaytaradi.

Quyidagi diagramma bu aylanishni ko'rsatadi: klient so'rov yuboradi, FastAPI mos funksiyani ishlatib JSON javob qaytaradi.

![Klient va FastAPI server orasidagi so'rov/javob aylanishi](rasmlar/py14-sorov-javob.svg)

So'rovlarning asosiy turlari (HTTP metodlari):

| Metod | Ma'nosi | Misol |
|-------|---------|-------|
| `GET` | ma'lumot **olish** | talabalar ro'yxatini ko'rish |
| `POST` | yangi ma'lumot **qo'shish** | yangi talaba qo'shish |
| `PUT` | mavjudni **yangilash** | talaba ma'lumotini o'zgartirish |
| `DELETE` | **o'chirish** | talabani o'chirish |

Javob odatda **JSON** ko'rinishida bo'ladi (8-moduldan tanish).

---

## 14.2 O'rnatish va birinchi API

```bash
pip install "fastapi[standard]"
```

> `[standard]` qism `uvicorn` (server), `python-multipart` (forma ma'lumotlari) va boshqa foydali kutubxonalarni ham o'rnatadi — keyinroq autentifikatsiyada ular kerak bo'ladi.

Eng oddiy API — `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def bosh_sahifa():
    return {"xabar": "Salom, dunyo!"}
```

Ishga tushirish (terminalda):

```bash
fastapi dev main.py
```

Brauzerda `http://127.0.0.1:8000` ni och — `{"xabar": "Salom, dunyo!"}` chiqadi.

> **Bonus:** `http://127.0.0.1:8000/docs` manzilini och — FastAPI **avtomatik** interaktiv hujjat yaratadi! U yerda API'ngni brauzerdan sinab ko'rishing mumkin. Bu FastAPI'ning eng yoqimli xususiyatlaridan biri.

`@app.get("/")` ni shunday o'qi: "kimdir `/` manziliga `GET` so'rov yuborsa, shu funksiyani ishlatib, natijasini qaytar". Funksiya lug'at qaytarsa, FastAPI uni avtomatik JSON ga aylantiradi.

---

## 14.3 Path parametrlari — manzildagi qiymat

Manzilning bir qismini o'zgaruvchi qilish mumkin:

```python
@app.get("/salom/{ism}")
def salomla(ism: str):
    return {"xabar": f"Salom, {ism}!"}

# /salom/Aziz  ->  {"xabar": "Salom, Aziz!"}
```

Tip ko'rsatmasi (`ism: str`, `id: int`) bu yerda **haqiqatan tekshiriladi** — FastAPI uni avtomatik tekshiradi va aylantiradi:

```python
@app.get("/talaba/{id}")
def talaba_olish(id: int):           # id avtomatik int ga aylanadi
    return {"id": id, "tur": str(type(id))}

# /talaba/5     ->  {"id": 5, ...}       (int)
# /talaba/abc   ->  XATO (422): int kutilgan edi  — FastAPI o'zi tekshiradi!
```

> 10-modulda "tip ko'rsatmalari tekshirilmaydi" degandik — bu sof Python'da. FastAPI esa ularni **ishlatadi**: so'rovdagi ma'lumotni tekshirish va aylantirish uchun. Bu juda qulay.

---

## 14.4 Query parametrlari — `?kalit=qiymat`

Manzil oxiridagi `?` dan keyingi qiymatlar — query parametrlari. Funksiya parametri sifatida olasan (standart qiymat bilan — ixtiyoriy bo'ladi):

```python
@app.get("/qidiruv")
def qidiruv(q: str, limit: int = 10):
    return {"qidiruv": q, "limit": limit}

# /qidiruv?q=python            ->  {"qidiruv": "python", "limit": 10}
# /qidiruv?q=python&limit=5    ->  {"qidiruv": "python", "limit": 5}
```

Endi ikkala turdagi parametrni yonma-yon solishtiramiz: path parametr manzilning bir qismi (`{}` ichida), query parametr esa `?` dan keyin `kalit=qiymat` ko'rinishida keladi.

![Path parametr va query parametr o'rtasidagi farq](rasmlar/py14-path-vs-query.svg)

---

## 14.5 Pydantic — ma'lumotni qabul qilish (POST)

Yangi ma'lumot qabul qilishda (POST), kelgan JSON qanday ko'rinishda bo'lishini **model** orqali belgilaysan. Buning uchun Pydantic ishlatasan:

```python
from pydantic import BaseModel

class Talaba(BaseModel):           # ma'lumot "shakli"
    ism: str
    yosh: int
    ball: float = 0                # standart qiymatli — ixtiyoriy

@app.post("/talabalar")
def qoshish(talaba: Talaba):       # kelgan JSON avtomatik Talaba'ga aylanadi
    return {"qoshildi": talaba}
```

Endi `{"ism": "Aziz", "yosh": 20}` JSON yuborsang, FastAPI uni avtomatik tekshiradi:
- Maydon yetishmasa yoki tur noto'g'ri bo'lsa — o'zi xato (422) qaytaradi.
- Hammasi to'g'ri bo'lsa — funksiyaga tayyor `Talaba` obyekti keladi.

> Pydantic 5-moduldagi klasslarga o'xshaydi, lekin u qo'shimcha ravishda **kelgan ma'lumotni avtomatik tekshiradi**. Bu xavfsiz API yozishni juda osonlashtiradi — kirish ma'lumotini o'zing tekshirib o'tirishing shart emas.

---

## 14.6 To'liq misol — oddiy CRUD

Talabalarni xotirada (oddiy lug'atda) saqlovchi to'liq API. Bu — barcha asoslarni birlashtiradi:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Talaba(BaseModel):
    ism: str
    yosh: int

# Xotirada saqlash (oddiy lug'at — dastur o'chsa yo'qoladi):
talabalar: dict[int, dict] = {}
keyingi_id = 1

@app.get("/talabalar")                       # HAMMASINI o'qish
def royxat():
    return talabalar

@app.get("/talabalar/{id}")                  # BITTASINI o'qish
def bittasi(id: int):
    if id not in talabalar:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")
    return talabalar[id]

@app.post("/talabalar")                      # QO'SHISH
def qoshish(talaba: Talaba):
    global keyingi_id
    talabalar[keyingi_id] = talaba.model_dump()
    keyingi_id += 1
    return {"id": keyingi_id - 1, **talaba.model_dump()}

@app.put("/talabalar/{id}")                  # YANGILASH
def yangilash(id: int, talaba: Talaba):
    if id not in talabalar:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")
    talabalar[id] = talaba.model_dump()
    return talabalar[id]

@app.delete("/talabalar/{id}")               # O'CHIRISH
def ochirish(id: int):
    if id not in talabalar:
        raise HTTPException(status_code=404, detail="Talaba topilmadi")
    del talabalar[id]
    return {"ochirildi": id}
```

Quyidagi xaritada yuqoridagi endpointlar jamlangan: e'tibor ber — bir xil manzil (`/talabalar/{id}`) turli HTTP metod bilan turli amalni bajaradi.

![CRUD endpointlarining metod va manzil bo'yicha xaritasi](rasmlar/py14-rest-endpoint-xarita.svg)

> **`HTTPException`** — ma'lumot topilmasa, mijozga to'g'ri xato (404 "topilmadi") qaytarish uchun. `model_dump()` — Pydantic obyektini oddiy lug'atga aylantiradi.
>
> **Eslatma:** bu yerda ma'lumot oddiy lug'atda — dastur o'chsa yo'qoladi. Keyingi modulda ma'lumotni **bazaga** (doimiy) saqlashni ko'rasan.

Bu misol asoslar uchun zo'r, lekin unda ikkita yashirin muammo bor: (1) `global keyingi_id` bilan ID berish ko'p so'rov bir vaqtda kelganda **xato ID** berishi mumkin (buni 14.12 da tuzatamiz); (2) endpointlar `def` — ya'ni **sinxron**, holbuki FastAPI'ning kuchi `async` da (buni darhol, 14.7 da ko'ramiz). Quyidagi bo'limlar shu kamchiliklarni bitta-bittadan yopib, kodni zamonaviy, professional darajaga olib chiqadi.

---

## 14.7 `async def` / `await` — FastAPI'ning kuchi

FastAPI nomidagi "Fast" (tez) — bu so'z behuda emas. Uning asosiy sehri **async** (asinxron) ishlashda. Tasavvur qil: kafeda bitta ofitsiant bor. **Sinxron** ofitsiant bir mijozga qahva tayyorlanayotganda **qimir etmay kutadi** — boshqa mijozlarga xizmat qilolmaydi. **Async** ofitsiant esa qahva tayyorlanayotganda **boshqa mijozlardan buyurtma oladi** — kutish vaqtini behuda sarflamaydi.

Veb serverda "kutish" — bu ko'pincha ma'lumotlar bazasi javobini yoki tashqi API javobini kutish. `async def` endpoint shu kutish paytida serverni **boshqa so'rovlarga** xizmat qilish uchun bo'shatadi.

`async` funksiya ichida "kut, lekin serverni bloklama" demoqchi bo'lsang — `await` ishlatasan:

```python
import asyncio

async def malumot_ol(soniya: float) -> dict[str, str]:
    await asyncio.sleep(soniya)          # "tashqi xizmatni" taqlid qilamiz
    return {"holat": "tayyor"}
```

`asyncio.sleep` — oddiy `time.sleep` ning async ukasi: u kutadi, lekin serverni bloklamaydi. Endi endpointni `async def` qilamiz:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/yangiliklar")
async def yangiliklar():
    # haqiqiy hayotda bu yerda async DB yoki async HTTP so'rov bo'lardi:
    natija = await malumot_ol(0.1)
    return {"yangiliklar": ["FastAPI o'rgandik"], "holat": natija["holat"]}
```

> **Qachon `async`, qachon `def`?** Oddiy qoida:
> - Endpoint ichida `await` ishlatadigan **async kutubxona** (async DB drayveri, `httpx`) bo'lsa — `async def`.
> - Faqat oddiy, "bloklaydigan" kod bo'lsa (`time.sleep`, oddiy `requests`) — `def` yoz. FastAPI bunday `def` endpointni avtomatik **alohida ip**da ishlatadi, shunda u boshqa so'rovlarni bloklamaydi.
> - **Eng yomon variant:** `async def` ichida `time.sleep(5)` yoki oddiy bloklaydigan kod yozish — bu butun serverni muzlatadi! Async ichida faqat `await` ladigan narsalar bo'lishi kerak.

Tashqi API ga async so'rov yuborishning amaliy ko'rinishi (`httpx` kutubxonasi bilan, u `fastapi[standard]` ichida keladi):

```python
import httpx

@app.get("/valyuta")
async def valyuta():
    async with httpx.AsyncClient() as client:
        javob = await client.get("https://api.example.com/usd")
        return javob.json()
```

---

## 14.8 `Depends` — Dependency Injection (qaramlikni in'ektsiya qilish)

Bu — FastAPI'ning eng markaziy va eng kuchli konsepsiyalaridan biri. Nomi qo'rqinchli, lekin g'oyasi oddiy: ba'zi narsalar **ko'p endpointga kerak bo'ladi** (masalan: ma'lumotlar bazasi ulanishi, joriy foydalanuvchi, umumiy parametrlar). Har bir endpointda ularni qaytadan yozish o'rniga, ularni **bir marta** funksiya qilib yozasan va FastAPI uni kerakli joyga o'zi "olib kelib beradi" (inject qiladi).

Eng oddiy misol — bir nechta endpointda takrorlanadigan query parametrlar:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

# Umumiy parametrlarni bitta funksiyaga jamlaymiz:
def sahifalash(skip: int = 0, limit: int = 10) -> dict[str, int]:
    return {"skip": skip, "limit": limit}

@app.get("/talabalar")
def talabalar(p: Annotated[dict, Depends(sahifalash)]):
    return {"parametrlar": p}

@app.get("/kitoblar")
def kitoblar(p: Annotated[dict, Depends(sahifalash)]):   # o'sha funksiyani qayta ishlatamiz
    return {"parametrlar": p}
```

`Depends(sahifalash)` ni shunday o'qi: "bu joyga `sahifalash()` funksiyasini ishlatib, natijasini qo'y". FastAPI `skip` va `limit` ni so'rovdan o'zi oladi, `sahifalash` ni chaqiradi, natijani `p` ga beradi.

Eng ko'p uchraydigan amaliy ishlatilishi — **ma'lumot omborini** (DB) berish. Shunda endpoint o'zi global o'zgaruvchiga bog'lanib qolmaydi, balki omborni "tashqaridan" oladi — bu test yozishni ham osonlashtiradi:

```python
class Ombor:
    def __init__(self) -> None:
        self.talabalar: dict[int, dict] = {}

ombor = Ombor()

def ombor_ber() -> Ombor:
    return ombor

@app.get("/soni")
def soni(db: Annotated[Ombor, Depends(ombor_ber)]):
    return {"soni": len(db.talabalar)}
```

> **Nega bu yaxshi?** Endi `soni` endpoint qaysi ombor kelishini bilmaydi — unga shunchaki "biror ombor" keladi. Test paytida `ombor_ber` ni soxta (yengil, xotiradagi) ombor bilan **almashtirib qo'yish** mumkin (`app.dependency_overrides`). Bu — professional kodning belgisi. `Depends` zanjir bo'lishi ham mumkin: bir `Depends` ichida boshqa `Depends` chaqirilishi mumkin (masalan: "joriy foydalanuvchi" -> "token tekshiruvchi" -> "DB").

---

## 14.9 `response_model`, status kodlar va `Annotated` validatsiya

Hozirgacha endpointlar nima qaytarsa, shu chiqib ketardi. Lekin professional API'da chiqadigan ma'lumotning **shaklini** ham aniq belgilash kerak — masalan, foydalanuvchining parolini hech qachon javobga qo'shmaslik uchun.

### `response_model` — javobning shakli

```python
from pydantic import BaseModel

class TalabaIn(BaseModel):          # KIRADIGAN ma'lumot (parol bilan)
    ism: str
    parol: str

class TalabaOut(BaseModel):         # CHIQADIGAN ma'lumot (parolsiz!)
    id: int
    ism: str

@app.post("/royxatdan", response_model=TalabaOut)
def royxatdan_otish(talaba: TalabaIn) -> TalabaOut:
    # parol saqlanadi, lekin javobga TUSHMAYDI — response_model filtrlaydi
    return TalabaOut(id=1, ism=talaba.ism)
```

`response_model=TalabaOut` FastAPI'ga: "nima qaytsa ham, faqat `TalabaOut` maydonlarini chiqar" deydi. Parol javobga tushmaydi — **xavfsizlik**.

### `status_code` — to'g'ri HTTP holat kodi

Yangi narsa yaratilganda standart `200 OK` emas, `201 Created` qaytarish to'g'riroq. O'chirishda esa `204 No Content`:

```python
from fastapi import status

@app.post("/talabalar", status_code=status.HTTP_201_CREATED)
def qoshish(talaba: TalabaIn):
    return {"natija": "qo'shildi"}

@app.delete("/talabalar/{id}", status_code=status.HTTP_204_NO_CONTENT)
def ochirish(id: int):
    ...   # 204 — "muvaffaqiyatli, qaytariladigan tana yo'q"
```

> `status.HTTP_201_CREATED` shunchaki `201` raqamining tushunarli nomi. Kodni o'qiganda `201` nimani anglatishini eslab o'tirmaysan.

### `Annotated[..., Query()/Path()/Body()]` — chuqur validatsiya

`Annotated` bilan parametrga **qoidalar** osib qo'yish mumkin: minimal/maksimal qiymat, uzunlik, tavsif. FastAPI buni `/docs` hujjatiga ham yozib qo'yadi.

```python
from typing import Annotated
from fastapi import Path, Query, Body

@app.get("/qidiruv")
def qidiruv(
    q: Annotated[str, Query(min_length=2, max_length=50, description="Qidiruv so'zi")],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return {"q": q, "limit": limit}

@app.get("/talabalar/{id}")
def bittasi(id: Annotated[int, Path(ge=1)]):    # id 1 dan kichik bo'lmasin
    return {"id": id}

@app.post("/baho")
def baho(ball: Annotated[int, Body(ge=0, le=100, embed=True)]):
    return {"ball": ball}
```

Ma'nosi:
- `ge=1` — "greater than or equal" (>= 1),  `le=100` — "less than or equal" (<= 100).
- `min_length` / `max_length` — matn uzunligi chegarasi.
- Qoida buzilsa — FastAPI **o'zi** 422 xato qaytaradi, sen hech narsa tekshirmaysan.

> **`Annotated` nega kerak?** Eski uslubda `limit: int = Query(10, ge=1)` deb yozilardi (standart qiymat va validatsiya aralash). Zamonaviy (Python 3.13) uslub — `Annotated[int, Query(ge=1)] = 10`: tur, qoida va standart qiymat **alohida**, tozaroq. FastAPI hujjatlari endi shu uslubni tavsiya qiladi.

---

## 14.10 `APIRouter` — kodni guruhlarga ajratish

Loyiha o'sgan sari hamma endpointni bitta `main.py` ga tiqish noqulay bo'ladi. `APIRouter` — endpointlarni mavzu bo'yicha alohida fayllarga ajratib, keyin bitta ilovaga ulash imkonini beradi. Bu — kichik ilovani **katta loyiha** strukturasiga o'tkazishning birinchi qadami.

`talabalar.py` faylida:

```python
from fastapi import APIRouter
from pydantic import BaseModel

# prefix — barcha manzil oldiga qo'shiladi;  tags — /docs da guruhlaydi
router = APIRouter(prefix="/talabalar", tags=["talabalar"])

class Talaba(BaseModel):
    ism: str
    yosh: int

@router.get("")                 # -> GET /talabalar
def royxat():
    return {"talabalar": []}

@router.get("/{id}")            # -> GET /talabalar/{id}
def bittasi(id: int):
    return {"id": id}
```

Asosiy `main.py` da ularni ulaymiz:

```python
from fastapi import FastAPI
from talabalar import router as talaba_router
# from kitoblar import router as kitob_router   # boshqa modul

app = FastAPI()
app.include_router(talaba_router)
# app.include_router(kitob_router)
```

> **Nima yutdik?** Har bir mavzu (talabalar, kitoblar, foydalanuvchilar) o'z faylida. `prefix="/talabalar"` tufayli router ichida manzilni qisqa (`""`, `"/{id}"`) yozasan. `tags=["talabalar"]` esa `/docs` sahifasida endpointlarni chiroyli guruhlaydi. Katta loyihalarda `app/routers/` papkasida o'nlab router fayllari bo'ladi.

---

## 14.11 Middleware va CORS — so'rovlar oralig'idagi qatlam

**Middleware** — har bir so'rov endpointga **yetib borishidan oldin** va javob qaytishidan **oldin** ishlaydigan "oraliq qatlam". U barcha so'rovlar uchun umumiy ish bajaradi: vaqtni o'lchash, log yozish, sarlavha (header) qo'shish.

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def vaqt_olchovchi(request: Request, call_next):
    boshlanish = time.perf_counter()
    javob = await call_next(request)          # endpointni ishga tushiramiz
    sarflandi = time.perf_counter() - boshlanish
    javob.headers["X-Sarflangan-Vaqt"] = f"{sarflandi:.4f}"
    return javob
```

Bu middleware har bir javobga "qancha vaqt ketdi" degan sarlavha qo'shadi — barcha endpointga, qo'lda yozmasdan.

### CORS — brauzerdan API ga murojaat

Agar API'ngga **boshqa domendagi** veb-sayt (masalan, React frontend `https://mensayt.uz`) murojaat qilsa, brauzer xavfsizlik uchun buni **bloklaydi** — bu CORS qoidasi. Yechim — ruxsat berilgan domenlarni ko'rsatish:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mensayt.uz"],   # ruxsat berilgan domenlar
    allow_credentials=True,
    allow_methods=["*"],                    # barcha metodlar (GET, POST...)
    allow_headers=["*"],                    # barcha sarlavhalar
)
```

> **Eslatma:** ishlab chiqish paytida `allow_origins=["*"]` (hammaga ruxsat) qulay, lekin **ishchi (production) serverda** faqat o'z frontend domeningni yozish kerak — aks holda istalgan sayt API'ngdan foydalanishi mumkin.

---

## 14.12 Race condition — global `dict` + `keyingi_id` muammosi

14.6 dagi `global keyingi_id` ni eslaysanmi? Unda yashirin xato bor. Tasavvur qil: ikkita foydalanuvchi **bir vaqtda** talaba qo'shmoqda. `keyingi_id += 1` aslida uch amaldan iborat: (1) o'qish, (2) bittaga oshirish, (3) qayta yozish. Ikki so'rov bu amallar orasiga "kirib qolsa", **ikkalasi ham bir xil ID** olishi mumkin — biri ikkinchisining ustiga yozadi. Bu — **race condition** ("poyga holati").

Buni sun'iy ravishda ko'rsatamiz (`itertools.count` ni qulfsiz ishlatib):

```python
from threading import Thread

keyingi_id = 1
yigilgan: list[int] = []

def ishchi():
    global keyingi_id
    for _ in range(10000):
        joriy = keyingi_id          # 1) o'qish
        keyingi_id = joriy + 1      # 2,3) oshirish + yozish
        yigilgan.append(joriy)

iplar = [Thread(target=ishchi) for _ in range(5)]
for i in iplar: i.start()
for i in iplar: i.join()

print("Kutilgan:", 5 * 10000)
print("Haqiqiy (takrorlanmas):", len(set(yigilgan)))   # KAMROQ chiqadi — ID'lar takrorlangan!
```

### Yechim — `Lock` (qulf) yoki atomik hisoblagich

To'g'ri yo'l — ID berishni **qulf** (`Lock`) bilan himoyalash: bir vaqtda faqat bitta ip ID olabilsin. Eng toza yechim — `itertools.count` ni `Lock` bilan o'rab, butun omborni klassga jamlash:

```python
from itertools import count
from threading import Lock

class TalabalarOmbori:
    def __init__(self) -> None:
        self._data: dict[int, dict] = {}
        self._id_gen = count(1)        # 1, 2, 3, ... beradigan generator
        self._lock = Lock()

    def qosh(self, talaba: dict) -> int:
        with self._lock:               # bir vaqtda faqat bitta ip kiradi
            yangi_id = next(self._id_gen)
            self._data[yangi_id] = talaba
        return yangi_id
```

`with self._lock:` bloki ichidagi kod **atomik** bo'ladi — uni ikki ip bir vaqtda bajara olmaydi, demak ID'lar hech qachon takrorlanmaydi.

> **Yana yaxshiroq yechim:** real loyihada ID berishni umuman **ma'lumotlar bazasiga** topshirasan (`AUTOINCREMENT` yoki `SERIAL`) — baza buni o'zi, xavfsiz qiladi. Global `dict` faqat o'rganish va demo uchun. Keyingi modulda buni ko'rasan.
>
> Yana bir nozik holat: agar serverni bir nechta **ishchi jarayon** (`uvicorn --workers 4`) bilan ishlatsang, har bir jarayonning **alohida** `dict` va `Lock` i bo'ladi — `Lock` jarayonlar orasida ishlamaydi. Shuning uchun ham doimiy ma'lumot uchun yagona umumiy baza kerak.

---

## 14.13 Pydantic v2 chuqurroq — `Field`, `field_validator`, `model_config`

Pydantic — FastAPI'ning yuragi. v2 versiyasi juda tez va kuchli. Modelni shunchaki maydonlar ro'yxati emas, balki **aqlli validator** qilib yasash mumkin.

### `Field()` — maydonga qoida va metama'lumot

```python
from pydantic import BaseModel, Field

class Mahsulot(BaseModel):
    nom: str = Field(min_length=2, max_length=100, description="Mahsulot nomi")
    narx: float = Field(gt=0, description="Narx (musbat bo'lishi shart)")
    soni: int = Field(default=0, ge=0)
    teglar: list[str] = Field(default_factory=list)   # standart bo'sh ro'yxat
```

> **Diqqat:** o'zgaruvchan standart qiymat (ro'yxat, lug'at) uchun `default_factory=list` ishlat, `default=[]` emas — aks holda barcha obyektlar **bitta** ro'yxatni baham ko'radi (klassik Python tuzog'i).

### `field_validator` — maxsus tekshiruv mantiqiy

`Field` yetmasa, o'z mantiqingni yozasan:

```python
from pydantic import BaseModel, field_validator

class Foydalanuvchi(BaseModel):
    login: str
    parol: str

    @field_validator("login")
    @classmethod
    def login_kichik_harf(cls, v: str) -> str:
        return v.strip().lower()        # bo'sh joyni olib, kichik harfga o'tkazamiz

    @field_validator("parol")
    @classmethod
    def parol_kuchli(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("parol kamida 8 belgi bo'lsin")
        if not any(c.isdigit() for c in v):
            raise ValueError("parolda kamida bitta raqam bo'lsin")
        return v
```

Validator `ValueError` otsa — FastAPI buni avtomatik chiroyli **422** xatoga aylantiradi.

### `model_config` — modelning umumiy sozlamalari

```python
from pydantic import BaseModel, ConfigDict

class Sozlama(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,   # barcha matn maydonlarda bo'sh joyni avtomatik tozalaydi
        extra="forbid",              # modelda yo'q maydon yuborilsa — XATO beradi
        frozen=False,                # True bo'lsa — obyekt o'zgarmas bo'ladi
    )

    ism: str
    yosh: int
```

> `extra="forbid"` — xavfsizlik uchun foydali: foydalanuvchi kutilmagan (`admin: true` kabi) maydon "tiqishtirib" yuborolmaydi. v2 da `model_config` lug'at yoki `ConfigDict(...)` bo'lishi mumkin; `ConfigDict` IDE'da avtomatik to'ldirishni beradi.

---

## 14.14 `TestClient` bilan test yozish

13-modulda `pytest` bilan funksiyalarni test qildik. API'ni ham aynan shunday **avtomatik** test qilish mumkin — serverni qo'lda ishga tushirmasdan! FastAPI shu uchun `TestClient` beradi. U serverni **xotirada** ishga tushiradi va unga "soxta" so'rovlar yuboradi.

`test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app           # main.py dagi FastAPI ilovamiz

client = TestClient(app)

def test_bosh_sahifa():
    javob = client.get("/")
    assert javob.status_code == 200
    assert javob.json() == {"xabar": "Salom, dunyo!"}

def test_talaba_qoshish():
    javob = client.post("/talabalar", json={"ism": "Aziz", "yosh": 20})
    assert javob.status_code == 201
    assert javob.json()["ism"] == "Aziz"

def test_xato_malumot_422():
    javob = client.post("/talabalar", json={"ism": "A"})   # yosh yo'q
    assert javob.status_code == 422

def test_topilmadi_404():
    javob = client.get("/talabalar/999999")
    assert javob.status_code == 404
```

Ishga tushirish: `pytest`. Har bir test soniyaning ulushida o'tadi.

> **Nega bu kuchli?** Har safar kod o'zgartirganda, qo'lda brauzerdan barcha endpointni tekshirish — uzoq va zerikarli. Avtomatik testlar bilan `pytest` ni bir marta ishlatib, **hammasini** bir zumda tekshirasan. 14.8 dagi `Depends` bilan yozilgan kod bu yerda ayniqsa qulay: testda haqiqiy DB o'rniga soxta omborni `app.dependency_overrides[ombor_ber] = soxta_ombor` orqali ulab qo'yasan.

---

## 14.15 Oddiy autentifikatsiya — token va JWT

Hozirgacha API'mizga **istalgan kishi** murojaat qila olardi. Ko'p ilovalarda esa ba'zi amallar (o'chirish, o'zgartirish) faqat **tizimga kirgan** foydalanuvchiga ruxsat etilishi kerak. Bu — autentifikatsiya.

Eng keng tarqalgan usul — **token**: foydalanuvchi bir marta login/parol bilan kiradi, server unga **imzolangan token** beradi. Keyingi har bir so'rovda foydalanuvchi shu tokenni yuboradi, server uni tekshiradi. Haqiqiy loyihada bu token **JWT** (JSON Web Token) bo'ladi — odatda `pyjwt` kutubxonasi bilan (`pip install pyjwt`).

Quyida JWT'ning ishlash g'oyasini **tashqi kutubxonasiz** (faqat standart kutubxona bilan) ko'rsatamiz, shunda "imzolangan token" nima ekanini chuqur tushunasan. FastAPI'ning `OAuth2PasswordBearer` yordamchisi `Authorization: Bearer <token>` sarlavhasini o'qishni avtomatlashtiradi:

```python
import base64, hashlib, hmac, json, time
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SIR = "juda-maxfiy-kalit"          # real loyihada: muhit o'zgaruvchisidan o'qiladi!

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="/token")
foydalanuvchilar = {"aziz": "12345"}   # demo: login -> parol (real: hash saqlanadi!)

def token_yasa(login: str) -> str:
    yuk = {"login": login, "exp": time.time() + 3600}      # 1 soat amal qiladi
    yuk_b = base64.urlsafe_b64encode(json.dumps(yuk).encode()).decode()
    imzo = hmac.new(SIR.encode(), yuk_b.encode(), hashlib.sha256).hexdigest()
    return f"{yuk_b}.{imzo}"        # JWT ham aynan shunday: yuk + imzo

def token_tekshir(token: Annotated[str, Depends(oauth2)]) -> str:
    try:
        yuk_b, imzo = token.split(".")
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token buzuq")
    kutilgan = hmac.new(SIR.encode(), yuk_b.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(imzo, kutilgan):            # imzoni tekshiramiz
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Imzo noto'g'ri")
    yuk = json.loads(base64.urlsafe_b64decode(yuk_b))
    if yuk["exp"] < time.time():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token muddati o'tgan")
    return yuk["login"]

@app.post("/token")          # 1) LOGIN: token olish
def kirish(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    parol = foydalanuvchilar.get(form.username)
    if parol is None or parol != form.password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Login yoki parol xato")
    return {"access_token": token_yasa(form.username), "token_type": "bearer"}

@app.get("/men")             # 2) HIMOYALANGAN: token kerak
def men(login: Annotated[str, Depends(token_tekshir)]) -> dict[str, str]:
    return {"login": login}   # token to'g'ri bo'lsagina shu yergacha yetib keladi
```

Ishlatish:
1. `POST /token` ga `username=aziz&password=12345` yuborasan -> `access_token` olasan.
2. `GET /men` ga `Authorization: Bearer <token>` sarlavhasi bilan murojaat qilasan.
3. Token yo'q/buzuq/eskirgan bo'lsa -> 401.

> **Real loyiha uchun muhim ogohlantirishlar:**
> - Parollarni **hech qachon ochiq** saqlama — `bcrypt`/`argon2` bilan **hash** qil.
> - `SIR` kalitni kodga yozma — **muhit o'zgaruvchisidan** (`os.environ`) o'qi.
> - Haqiqiy JWT uchun `pyjwt` ishlat: `jwt.encode(yuk, SIR, algorithm="HS256")` va `jwt.decode(...)`. Yuqoridagi qo'lbola variant faqat **g'oyani tushuntirish** uchun.

---

## 14.16 Ishga tushirish va deploy — `uvicorn`

Ishlab chiqish paytida `fastapi dev main.py` qulay — u kod o'zgarsa serverni **avtomatik qayta yuklaydi**. Lekin u sahnaning ortida **uvicorn** degan serverni ishga tushiradi. Ishchi (production) serverda uvicorn'ni to'g'ridan-to'g'ri chaqirasan:

```bash
# Ishlab chiqish (avtomatik qayta yuklash bilan):
fastapi dev main.py
# yoki:
uvicorn main:app --reload

# Ishchi server (production):
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

`main:app` ni shunday o'qi: "`main.py` faylidagi `app` nomli FastAPI ilovasini ishga tushir".
- `--host 0.0.0.0` — serverni tashqi ulanishlarga ham ochadi (faqat o'zingda emas).
- `--workers 4` — 4 ta ishchi jarayon, ko'p so'rovni parallel bajarish uchun.
- `--reload` — faqat ishlab chiqishda! Production'da o'chir.

Deploy uchun odatda **Docker** ishlatiladi. Eng oddiy `Dockerfile`:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> **Lifespan — ishga tushish/to'xtash hodisalari.** Server ishga tushganda (bazaga ulanish) yoki to'xtaganda (ulanishni yopish) biror ish qilish kerak bo'lsa, `lifespan` ishlatasan:
>
> ```python
> from contextlib import asynccontextmanager
> from fastapi import FastAPI
>
> @asynccontextmanager
> async def umr(app: FastAPI):
>     print("Server ishga tushdi — bazaga ulandik")   # yield dan OLDIN: start
>     yield
>     print("Server to'xtadi — ulanishni yopdik")       # yield dan KEYIN: stop
>
> app = FastAPI(lifespan=umr)
> ```

---

## 14.17 Zamonaviy to'liq misol — qayta yozilgan CRUD

Endi 14.6 dagi misolni o'rgangan barcha narsalarimiz bilan **professional** ko'rinishga keltiramiz: `async`, `Depends` bilan ombor, `response_model`, `Annotated` validatsiya, status kodlar va race-condition'siz xavfsiz ID. Bu — yuqoridagi bo'limlarning hammasi bitta joyda.

```python
from itertools import count
from threading import Lock
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field

# ---- Modellar: kiruvchi va chiquvchi alohida ----
class Talaba(BaseModel):
    ism: str = Field(min_length=2, max_length=50)
    yosh: int = Field(ge=0, le=150)

class TalabaJavob(Talaba):       # kiruvchi maydonlar + id
    id: int

# ---- Xavfsiz ombor (Lock bilan, race-condition'siz) ----
class TalabalarOmbori:
    def __init__(self) -> None:
        self._data: dict[int, Talaba] = {}
        self._id = count(1)
        self._lock = Lock()

    def qosh(self, t: Talaba) -> TalabaJavob:
        with self._lock:
            yangi = next(self._id)
            self._data[yangi] = t
        return TalabaJavob(id=yangi, **t.model_dump())

    def hammasi(self) -> list[TalabaJavob]:
        return [TalabaJavob(id=i, **t.model_dump()) for i, t in self._data.items()]

    def bittasi(self, talaba_id: int) -> TalabaJavob:
        t = self._data.get(talaba_id)
        if t is None:
            raise HTTPException(404, "Talaba topilmadi")
        return TalabaJavob(id=talaba_id, **t.model_dump())

    def yangila(self, talaba_id: int, t: Talaba) -> TalabaJavob:
        if talaba_id not in self._data:
            raise HTTPException(404, "Talaba topilmadi")
        self._data[talaba_id] = t
        return TalabaJavob(id=talaba_id, **t.model_dump())

    def ochir(self, talaba_id: int) -> None:
        if self._data.pop(talaba_id, None) is None:
            raise HTTPException(404, "Talaba topilmadi")

ombor = TalabalarOmbori()
def db() -> TalabalarOmbori:
    return ombor

# ---- Qulay qisqartmalar (Annotated turlarini qayta ishlatamiz) ----
Db = Annotated[TalabalarOmbori, Depends(db)]
TalabaId = Annotated[int, Path(ge=1)]

# ---- Router ----
app = FastAPI(title="Talabalar API", version="2.0")
router = APIRouter(prefix="/talabalar", tags=["talabalar"])

@router.get("", response_model=list[TalabaJavob])
async def royxat(d: Db, limit: Annotated[int, Query(ge=1, le=100)] = 10):
    return d.hammasi()[:limit]

@router.get("/{talaba_id}", response_model=TalabaJavob)
async def bittasi(talaba_id: TalabaId, d: Db):
    return d.bittasi(talaba_id)

@router.post("", response_model=TalabaJavob, status_code=status.HTTP_201_CREATED)
async def qoshish(talaba: Talaba, d: Db):
    return d.qosh(talaba)

@router.put("/{talaba_id}", response_model=TalabaJavob)
async def yangilash(talaba_id: TalabaId, talaba: Talaba, d: Db):
    return d.yangila(talaba_id, talaba)

@router.delete("/{talaba_id}", status_code=status.HTTP_204_NO_CONTENT)
async def ochirish(talaba_id: TalabaId, d: Db):
    d.ochir(talaba_id)

app.include_router(router)
```

> **Solishtir:** 14.6 dagi misol bilan yonma-yon qo'ysang, farqni ko'rasan — kiruvchi/chiquvchi modellar ajratilgan, ombor qulflangan (xavfsiz), validatsiya `Annotated` da, status kodlar to'g'ri, endpointlar `async`, va kod router'da guruhlangan. Bu — kichik o'quv API'dan **ishlatsa bo'ladigan** API ga o'tishning to'liq yo'li.

---

## ✍️ Masalalar (26 ta)

> Bu masalalar uchun `fastapi dev main.py` bilan serverni ishga tushirib, `/docs` orqali sina.

**Oson (1–7):**

1. `/` manzilida `{"xabar": "Salom"}` qaytaruvchi API yoz.
2. `/salom/{ism}` yoz: "Salom, {ism}!" qaytarsin.
3. `/kvadrat/{son}` yoz: sonning kvadratini qaytarsin (`son: int`).
4. `/qoshish?a=2&b=3` ko'rinishida ikki sonni qo'shadigan endpoint yoz (query params).
5. `/vaqt` yoz: hozirgi sanani qaytarsin (`datetime` ishlat).
6. `/docs` ni ochib, yozgan endpointlaringni brauzerdan sina.
7. `/salom` endpointiga ixtiyoriy `til` query parametrini qo'sh (standart "uz").

**O'rta (8–14):**

8. `Mahsulot` Pydantic modeli yoz (`nom: str`, `narx: float`), `POST /mahsulotlar` bilan qabul qilib qaytar.
9. `GET /talabalar` yoz: oldindan to'ldirilgan ro'yxatni (lug'atlar) qaytarsin.
10. `GET /talabalar/{id}` yoz: berilgan id'li talabani qaytarsin, topilmasa 404.
11. Query parametrli qidiruv: `GET /qidiruv?q=...` — mahsulotlardan nomida `q` bo'lganlarni qaytarsin.
12. `POST` bilan kelgan Pydantic modelni tekshir: noto'g'ri ma'lumot yuborib, 422 xatosini ko'r.
13. `limit` va `skip` query parametrlari bilan ro'yxatni "sahifalash" (qism qaytarish).
14. `HTTPException` bilan: id topilmasa 404, manfiy id berilsa 400 qaytar.

**Murakkab (15–20):**

15. To'liq CRUD yoz: `Kitob` (`nom`, `muallif`) uchun GET (hammasi), GET (bittasi), POST, DELETE.
16. PUT qo'sh: mavjud kitobni yangilash, topilmasa 404.
17. Avtomatik `id` berish: yangi yozuvga ketma-ket id ber (yuqoridagi `keyingi_id` namunasiday).
18. Validatsiya qo'sh: Pydantic modelda `yosh` manfiy bo'lmasligini ta'minla (`field_validator` yoki shartli tekshiruv bilan).
19. Statistika endpointi: `GET /statistika` — talabalar soni va o'rtacha yoshni qaytarsin.
20. Mini "vazifa boshqaruvchi" (todo) API: vazifa qo'shish, ro'yxatni ko'rish, bajarildi deb belgilash (PUT), o'chirish — to'liq CRUD bilan.

**Zamonaviy / ilg'or (21–26):**

21. `async def` endpoint yoz: `GET /kechikkan` — `asyncio.sleep(1)` bilan kutib, keyin javob qaytarsin. `async`/`await` ishlat.
22. `Depends` bilan umumiy `sahifalash(skip, limit)` funksiyasini yoz va uni kamida ikkita endpointda qayta ishlat.
23. `response_model` va `status_code=201`: `MahsulotIn` (parol bilan) qabul qilib, `MahsulotOut` (parolsiz) qaytaruvchi `POST /mahsulotlar` yoz — parol javobga tushmasin.
24. `Annotated` validatsiya: `GET /talabalar/{id}` da `id` ni `Path(ge=1)` bilan, `limit` ni `Query(ge=1, le=100)` bilan cheklab qo'y.
25. `Lock` bilan xavfsiz ombor: 14.12 dagiday `TalabalarOmbori` klassini `itertools.count` + `Lock` bilan yoz, ID hech qachon takrorlanmasin.
26. `TestClient` bilan test: yozgan CRUD API'ng uchun kamida 3 ta test yoz — qo'shish (201), o'qish (200), topilmagan holat (404).

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish (1–20)</summary>

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI()

# 1
@app.get("/")
def bosh():
    return {"xabar": "Salom"}

# 2
@app.get("/salom/{ism}")
def salom(ism: str):
    return {"xabar": f"Salom, {ism}!"}

# 3
@app.get("/kvadrat/{son}")
def kvadrat(son: int):
    return {"natija": son ** 2}

# 4
@app.get("/qoshish")
def qoshish(a: int, b: int):
    return {"natija": a + b}

# 5
@app.get("/vaqt")
def vaqt():
    return {"sana": str(date.today())}

# 7
@app.get("/salom2")
def salom2(ism: str = "dunyo", til: str = "uz"):
    matnlar = {"uz": "Salom", "en": "Hello", "ru": "Privet"}
    return {"xabar": f"{matnlar.get(til, 'Salom')}, {ism}!"}

# 8
class Mahsulot(BaseModel):
    nom: str
    narx: float
@app.post("/mahsulotlar")
def mahsulot_qosh(m: Mahsulot):
    return {"qoshildi": m}

# 9, 10, 11, 13 — namuna ma'lumot bilan:
talabalar_db = {
    1: {"ism": "Aziz", "yosh": 20},
    2: {"ism": "Malika", "yosh": 22},
}

@app.get("/talabalar")
def talabalar_royxat(skip: int = 0, limit: int = 10):
    qiymatlar = list(talabalar_db.values())
    return qiymatlar[skip: skip + limit]

@app.get("/talabalar/{id}")
def talaba_bittasi(id: int):
    if id < 0:
        raise HTTPException(status_code=400, detail="id manfiy bo'lmaydi")
    if id not in talabalar_db:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return talabalar_db[id]

mahsulotlar_db = [{"nom": "Olma", "narx": 12000}, {"nom": "Non", "narx": 4000}]
@app.get("/qidiruv")
def qidiruv(q: str):
    return [m for m in mahsulotlar_db if q.lower() in m["nom"].lower()]

# 15, 16, 17 — Kitob uchun to'liq CRUD:
class Kitob(BaseModel):
    nom: str
    muallif: str

kitoblar: dict[int, dict] = {}
kitob_id = 1

@app.get("/kitoblar")
def kitoblar_royxat():
    return kitoblar

@app.get("/kitoblar/{id}")
def kitob_bittasi(id: int):
    if id not in kitoblar:
        raise HTTPException(status_code=404, detail="Topilmadi")
    return kitoblar[id]

@app.post("/kitoblar")
def kitob_qosh(k: Kitob):
    global kitob_id
    kitoblar[kitob_id] = k.model_dump()
    kitob_id += 1
    return {"id": kitob_id - 1, **k.model_dump()}

@app.put("/kitoblar/{id}")
def kitob_yangila(id: int, k: Kitob):
    if id not in kitoblar:
        raise HTTPException(status_code=404, detail="Topilmadi")
    kitoblar[id] = k.model_dump()
    return kitoblar[id]

@app.delete("/kitoblar/{id}")
def kitob_ochir(id: int):
    if id not in kitoblar:
        raise HTTPException(status_code=404, detail="Topilmadi")
    del kitoblar[id]
    return {"ochirildi": id}

# 18 — validatsiyali model:
from pydantic import field_validator
class TalabaV(BaseModel):
    ism: str
    yosh: int
    @field_validator("yosh")
    @classmethod
    def yosh_musbat(cls, v):
        if v < 0:
            raise ValueError("yosh manfiy bo'lmaydi")
        return v

# 19
@app.get("/statistika")
def statistika():
    yoshlar = [t["yosh"] for t in talabalar_db.values()]
    return {
        "soni": len(yoshlar),
        "ortacha_yosh": sum(yoshlar) / len(yoshlar) if yoshlar else 0,
    }

# 20 — todo API:
class Vazifa(BaseModel):
    matn: str
    bajarildi: bool = False

vazifalar: dict[int, dict] = {}
vazifa_id = 1

@app.get("/vazifalar")
def vazifalar_royxat():
    return vazifalar

@app.post("/vazifalar")
def vazifa_qosh(v: Vazifa):
    global vazifa_id
    vazifalar[vazifa_id] = v.model_dump()
    vazifa_id += 1
    return {"id": vazifa_id - 1, **v.model_dump()}

@app.put("/vazifalar/{id}/bajarildi")
def vazifa_belgila(id: int):
    if id not in vazifalar:
        raise HTTPException(status_code=404, detail="Topilmadi")
    vazifalar[id]["bajarildi"] = True
    return vazifalar[id]

@app.delete("/vazifalar/{id}")
def vazifa_ochir(id: int):
    if id not in vazifalar:
        raise HTTPException(status_code=404, detail="Topilmadi")
    del vazifalar[id]
    return {"ochirildi": id}
```

</details>

<details markdown="1">
<summary>Masala 21 (async endpoint)</summary>

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/kechikkan")
async def kechikkan():
    await asyncio.sleep(1)        # serverni bloklamasdan 1 soniya kutadi
    return {"xabar": "1 soniyadan keyin javob"}
```

`asyncio.sleep` (oddiy `time.sleep` emas!) bilan kutamiz — shu paytda server boshqa so'rovlarga xizmat qila oladi.

</details>

<details markdown="1">
<summary>Masala 22 (Depends bilan qayta ishlatish)</summary>

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def sahifalash(skip: int = 0, limit: int = 10) -> dict[str, int]:
    return {"skip": skip, "limit": limit}

Sahifa = Annotated[dict, Depends(sahifalash)]   # qisqartma — qayta ishlatamiz

@app.get("/talabalar")
def talabalar(p: Sahifa):
    return {"resurs": "talabalar", **p}

@app.get("/kitoblar")
def kitoblar(p: Sahifa):
    return {"resurs": "kitoblar", **p}
```

`sahifalash` mantiqiy bir joyda — ikkala endpoint uni qayta ishlatadi. Bir joyda o'zgartirsang, ikkalasiga ham ta'sir qiladi.

</details>

<details markdown="1">
<summary>Masala 23 (response_model + status_code=201)</summary>

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class MahsulotIn(BaseModel):       # kiruvchi (maxfiy maydon bilan)
    nom: str
    narx: float
    maxfiy_kod: str

class MahsulotOut(BaseModel):      # chiquvchi (maxfiy maydonsiz)
    id: int
    nom: str
    narx: float

@app.post("/mahsulotlar", response_model=MahsulotOut, status_code=status.HTTP_201_CREATED)
def qoshish(m: MahsulotIn):
    # maxfiy_kod saqlanadi (haqiqiy hayotda), lekin javobga TUSHMAYDI:
    return MahsulotOut(id=1, nom=m.nom, narx=m.narx)
```

`response_model=MahsulotOut` tufayli `maxfiy_kod` javobga hech qachon chiqmaydi. `201` — yangi resurs yaratilganini bildiradi.

</details>

<details markdown="1">
<summary>Masala 24 (Annotated bilan Path/Query validatsiya)</summary>

```python
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()
talabalar_db = {1: {"ism": "Aziz"}, 2: {"ism": "Malika"}}

@app.get("/talabalar")
def royxat(limit: Annotated[int, Query(ge=1, le=100)] = 10):
    return list(talabalar_db.values())[:limit]

@app.get("/talabalar/{id}")
def bittasi(id: Annotated[int, Path(ge=1)]):    # id < 1 bo'lsa — avtomatik 422
    if id not in talabalar_db:
        raise HTTPException(404, "Topilmadi")
    return talabalar_db[id]

# /talabalar/0      -> 422 (id >= 1 bo'lsin)
# /talabalar?limit=0 -> 422 (limit >= 1 bo'lsin)
```

Endi noto'g'ri `id` yoki `limit` kelsa, FastAPI o'zi 422 qaytaradi — qo'lda tekshirish shart emas.

</details>

<details markdown="1">
<summary>Masala 25 (Lock bilan xavfsiz ombor)</summary>

```python
from itertools import count
from threading import Lock

class TalabalarOmbori:
    def __init__(self) -> None:
        self._data: dict[int, dict] = {}
        self._id_gen = count(1)
        self._lock = Lock()

    def qosh(self, talaba: dict) -> int:
        with self._lock:                 # atomik: bir vaqtda bitta ip
            yangi_id = next(self._id_gen)
            self._data[yangi_id] = talaba
        return yangi_id

    def olish(self, talaba_id: int) -> dict | None:
        return self._data.get(talaba_id)

# Sinab ko'rish: ko'p ip bir vaqtda qo'shsa ham, ID'lar takrorlanmaydi
if __name__ == "__main__":
    from threading import Thread
    ombor = TalabalarOmbori()
    idlar: list[int] = []
    def ishchi():
        for _ in range(1000):
            idlar.append(ombor.qosh({"ism": "X"}))
    iplar = [Thread(target=ishchi) for _ in range(5)]
    for i in iplar: i.start()
    for i in iplar: i.join()
    print("Takrorlanmas:", len(set(idlar)) == len(idlar))   # True
```

`with self._lock:` ID berishni atomik qiladi — 14.12 dagi race condition yo'qoladi.

</details>

<details markdown="1">
<summary>Masala 26 (TestClient bilan test)</summary>

`main.py`:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Kitob(BaseModel):
    nom: str
    muallif: str

kitoblar: dict[int, dict] = {}
keyingi = 1

@app.post("/kitoblar", status_code=status.HTTP_201_CREATED)
def qoshish(k: Kitob):
    global keyingi
    kitoblar[keyingi] = k.model_dump()
    keyingi += 1
    return {"id": keyingi - 1, **k.model_dump()}

@app.get("/kitoblar/{id}")
def bittasi(id: int):
    if id not in kitoblar:
        raise HTTPException(404, "Topilmadi")
    return kitoblar[id]
```

`test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_qoshish_201():
    javob = client.post("/kitoblar", json={"nom": "Python", "muallif": "Oqil"})
    assert javob.status_code == 201
    assert javob.json()["nom"] == "Python"

def test_oqish_200():
    yangi = client.post("/kitoblar", json={"nom": "SQL", "muallif": "Oqil"}).json()
    javob = client.get(f"/kitoblar/{yangi['id']}")
    assert javob.status_code == 200
    assert javob.json()["nom"] == "SQL"

def test_topilmadi_404():
    assert client.get("/kitoblar/999999").status_code == 404
```

Ishga tushirish: `pytest`. Uchala test ham bir zumda o'tadi — serverni qo'lda ishga tushirish shart emas.

</details>

---

[← Dasturni test qilish](./13-testlash.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Ma'lumotlar bazasi →](./15-malumotlar-bazasi.md)
