# 26 — Deploy: FastAPI bilan LLM xizmati

[⬅️ Oldingi: 25 — Kuzatuv, logging va baholash (eval)](./25-kuzatuv-baholash.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 27 — Kapston I: RAG chatbot ➡️](./27-kapston-rag-chatbot.md)

> **Bu bobda:** terminalda ishlaydigan LLM **skriptini** boshqa ilovalar (web, mobil, boshqa xizmatlar) ishlatadigan **REST API xizmatiga** aylantiramiz. **FastAPI**ning eng zarur asoslarini — `app = FastAPI()`, `@app.post`, Pydantic so'rov/javob modellari, `uvicorn` bilan ishga tushirish — qisqa va amaliy ko'ramiz. To'liq `/chat` endpoint quramiz; sozlamalarni xavfsiz boshqaramiz; **`async def` + `AsyncOpenAI`** bilan ko'p so'rovni parallel bardosh qilamiz; **streaming endpoint**ni (`StreamingResponse`/SSE) yozamiz; xatolarni **HTTP statusga** to'g'ri map qilamiz; va nihoyat — kalit xavfsizligi, CORS, rate limit, `Dockerfile` va masshtab kabi **production eslatmalari** bilan yakunlaymiz. Bu bob — keyingi kapstonlarni "joylashtirish" poydevori.

---

## Muammodan boshlaymiz: skript bitta odam uchun, xizmat hamma uchun

Hozirgacha biz yozgan kodlar — **skript**lar edi: terminalda `python birinchi.py` deysiz, savol yuborasiz, javobni ekranda ko'rasiz. Bu o'rganish uchun ajoyib. Lekin haqiqiy mahsulotda LLM logikasi yolg'iz sizning terminalingizda emas, **boshqalar** uchun ishlashi kerak:

- **Veb-sayt** foydalanuvchisi sahifadagi chat oynasiga yozadi.
- **Mobil ilova** foydalanuvchi savolini yuboradi.
- **Boshqa backend xizmat** sizning "AI qismingiz"ni chaqiradi.

Bularning hammasi bitta umumiy ehtiyojni ko'rsatadi: LLM logikangiz **tarmoq orqali chaqirsa bo'ladigan** joyda turishi kerak. Yechim — uni **REST API** ortiga qo'yish: mijoz JSON so'rov yuboradi, sizning xizmatingiz LLM'ni chaqiradi va JSON javob qaytaradi.

![LLM xizmati arxitekturasi: chap tomonda mijozlar (web sayt, mobil ilova, boshqa xizmat), markazda FastAPI xizmati (POST /chat, Pydantic tekshiruv, .env kalit, xato->HTTP, logging), o'ng tomonda LLM provayderi; mijoz va xizmat orasida JSON so'rov/javob, xizmat va provayder orasida LLM chaqiruvi](rasmlar/aip26-arxitektura.svg)

> **Hayotiy o'xshatish.** Skript — uyingizdagi **shaxsiy oshxona**: faqat o'zingiz ovqatlanasiz. Xizmat (API) — **restoran**: ofitsiant (endpoint) buyurtmani oladi, oshxona (LLM logika) tayyorlaydi, taom qaytadi — va bu bir vaqtda **o'nlab mehmonga** xizmat qiladi. Eng muhimi: mehmonlar oshxonaga kirmaydi — ya'ni mijoz sizning API kalitingizni va ichki logikangizni ko'rmaydi.

!!! note "REST API nima — bir og'iz"
    **REST API** — ilovalar bir-biri bilan HTTP orqali gaplashuvi uchun kelishilgan usul. Mijoz ma'lum **manzilga** (masalan, `POST /chat`) **JSON** yuboradi, server **JSON** qaytaradi va **HTTP status kod** (200 = OK, 400 = xato so'rov, 500 = server xatosi) bilan natijani bildiradi. Til muhim emas: JavaScript frontend, Swift mobil ilova, boshqa Python xizmat — hammasi bir xil endpoint'ni chaqira oladi.

---

## FastAPI asoslari (eng zarur minimum)

**FastAPI** — Python'da REST API yozishning eng mashhur va tez yo'li. Nega aynan u? Chunki: (a) **Pydantic** bilan so'rov/javobni avtomatik tekshiradi (5-bobdagi `BaseModel` allaqachon tanish); (b) `async` ni tabiiy qo'llab-quvvatlaydi — bu LLM kabi **sekin I/O** ish uchun aynan kerak; (c) avtomatik hujjat (`/docs`) yaratadi.

Avval o'rnatamiz:

```bash
pip install fastapi "uvicorn[standard]" openai python-dotenv pydantic-settings
```

Eng kichik FastAPI ilovasi atigi shu:

```python
from fastapi import FastAPI

app = FastAPI()                 # ilova obyekti

@app.get("/")                   # GET so'rov / manzilida
def root():
    return {"holat": "ishlayapti"}   # dict avtomatik JSON bo'lib qaytadi
```

`uvicorn` — bu **ASGI server**, ilovani ishga tushiradi. Faylni `main.py` deb saqlasangiz:

```bash
uvicorn main:app --reload
# main = fayl nomi, app = FastAPI obyekti, --reload = kod o'zgarsa qayta yuklash (faqat dev)
```

Endi brauzerda `http://127.0.0.1:8000` — JSON javobni, `http://127.0.0.1:8000/docs` — avtomatik interaktiv hujjatni ko'rasiz.

!!! tip "`/docs` — bepul sovg'a"
    FastAPI har bir endpoint uchun **Swagger UI** hujjatini avtomatik yaratadi (`/docs` manzilida). U yerda endpointni brauzerdan to'g'ridan-to'g'ri sinab ko'rsa bo'ladi — alohida Postman shart emas. Pydantic modellaringiz shu hujjatda sxema bo'lib ko'rinadi.

### Pydantic bilan so'rov va javob modeli

Mijoz nima yuborishi va biz nima qaytarishimizni **aniq shakl** (model) bilan belgilaymiz. Bu — xizmatning "shartnomasi". FastAPI bu modellarni avtomatik tekshiradi: agar mijoz noto'g'ri ma'lumot yuborsa, **422** xato qaytaradi — bizning kodimizgacha yetib ham kelmaydi.

```python
from pydantic import BaseModel

class ChatSorov(BaseModel):
    xabar: str                       # majburiy maydon
    tizim: str = "Sen foydali yordamchisan."   # ixtiyoriy, standart qiymatli

class ChatJavob(BaseModel):
    javob: str
    tokenlar: int
```

> **Hayotiy o'xshatish.** Pydantic modeli — restoran **menyusi va buyurtma blankasi**. Mijoz blankada nimani to'ldirishini (xabar — majburiy, tizim — ixtiyoriy) aniq biladi; ofitsiant esa blankani avtomatik tekshiradi — bo'sh yoki noto'g'ri to'ldirilsa, oshxonaga (kodga) yubormay, "blankani to'g'ri to'ldiring" deydi.

---

## To'liq `/chat` endpoint

Endi barchasini birlashtiramiz: so'rovni qabul qilamiz, LLM'ni chaqiramiz, javobni qaytaramiz. Avval sozlamalarni xavfsiz boshqaraylik.

### Sozlamalar: `.env` va `pydantic-settings`

24-bobda o'rgandik — kalit **faqat serverda**, kodda emas. `.env` faylini ishlatamiz, lekin endi uni `BaseSettings` orqali tartibli o'qiymiz (oddiy `os.environ` ham ishlaydi, lekin `Settings` validatsiya va standart qiymat beradi):

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str               # .env dagi OPENAI_API_KEY ga moslanadi
    model: str = "gpt-5.4-mini"       # nomlar o'zgaradi — provayder ro'yxatini tekshiring
    max_tokens: int = 500

    class Config:
        env_file = ".env"

settings = Settings()                 # ishga tushganda .env dan o'qiydi
```

```text
# .env  (bu fayl HECH QACHON Git'ga tushmaydi — .gitignore ga qo'shing)
OPENAI_API_KEY=sk-...
MODEL=gpt-5.4-mini
```

### Endpoint

```python
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI(title="LLM xizmati")
client = OpenAI(api_key=settings.openai_api_key)

@app.post("/chat", response_model=ChatJavob)   # javob shaklini ham e'lon qilamiz
def chat(sorov: ChatSorov):
    resp = client.chat.completions.create(
        model=settings.model,
        messages=[
            {"role": "system", "content": sorov.tizim},
            {"role": "user", "content": sorov.xabar},
        ],
        max_tokens=settings.max_tokens,
    )
    return ChatJavob(
        javob=resp.choices[0].message.content,
        tokenlar=resp.usage.total_tokens,
    )
```

Tekshiramiz (`uvicorn main:app --reload` ishlab turganda, boshqa terminalda):

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"xabar": "Salom, o'\''zingni bir jumlada tanishtir."}'
# -> {"javob":"Men sun'iy intellekt yordamchisiman...","tokenlar":42}
```

Tabriklaymiz — endi LLM logikangiz **tarmoqdagi xizmat**. Har qanday frontend yoki mobil ilova shu `/chat` ni chaqira oladi va sizning kalitingizni umuman ko'rmaydi.

!!! note "Kalit endi mijozda emas"
    Diqqat qiling: API kalit **serverdagi `.env`da** yashaydi va `client` shu yerda yaratiladi. Mijoz faqat `xabar` yuboradi — kalitni hech qachon ko'rmaydi va jo'natmaydi. Bu — frontend'dan to'g'ridan-to'g'ri LLM chaqirishga nisbatan asosiy xavfsizlik yutug'i (24-bob).

---

## Async: nega `async def` + `AsyncOpenAI`?

Yuqoridagi endpoint **oddiy** (`def`). Bitta foydalanuvchi uchun yaxshi. Lekin tasavvur qiling, bir vaqtda **20 ta** foydalanuvchi yozdi. LLM so'rovi **sekin** — 2-10 soniya kutiladi, va bu kutish **tarmoq (I/O)** kutishidir, protsessor ishi emas.

Oddiy `def` endpointda worker bitta so'rovning LLM javobini kutib turganda **boshqa hech nima qila olmaydi** — qolgan 19 foydalanuvchi navbatda turadi. `async def` bilan esa worker LLM javobini kutayotgan vaqtda **boshqa so'rovlarni** parallel boshqaradi. Bitta jarayon yuzlab parallel so'rovni "kutish" rejimida ushlab tura oladi.

> **Hayotiy o'xshatish.** Oddiy `def` — bitta ofitsiant har bir mijoz oldida **taom pishguncha qotib turadi**, hech kimga xizmat qilolmaydi. `async` — ofitsiant buyurtmani oshxonaga beradi-yu, taom pishguncha **boshqa stollarga** xizmat qiladi; taom tayyor bo'lganda esa olib keladi. Bitta ofitsiant ko'p stolni eplaydi — chunki vaqtning ko'pi **kutish**.

Buning uchun ikki o'zgartirish: `AsyncOpenAI` mijozi va `async def` + `await`:

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=settings.openai_api_key)   # async mijoz

@app.post("/chat", response_model=ChatJavob)
async def chat(sorov: ChatSorov):                       # async def
    resp = await client.chat.completions.create(        # await — natijani kutadi, lekin bloklamaydi
        model=settings.model,
        messages=[
            {"role": "system", "content": sorov.tizim},
            {"role": "user", "content": sorov.xabar},
        ],
        max_tokens=settings.max_tokens,
    )
    return ChatJavob(
        javob=resp.choices[0].message.content,
        tokenlar=resp.usage.total_tokens,
    )
```

!!! warning "`async def` ichida bloklovchi kod yozmang"
    `async` ning kuchi — hech narsani **bloklamaslik**da. `async def` ichida sinxron `time.sleep()`, og'ir CPU sikli yoki **sinxron** `OpenAI()` mijozini chaqirsangiz — butun event loop qotadi va async afzalligi yo'qoladi. Async endpointda har doim `await` bilan **async** mijoz (`AsyncOpenAI`) ishlating; uxlash kerak bo'lsa `await asyncio.sleep(...)`.

---

## Streaming endpoint: token-token javob (SSE)

7-bobda streamingni ko'rdik — model javobni token-token jo'natadi, foydalanuvchi birinchi belgini deyarli darrov ko'radi. Endi shu g'oyani **API ustidan** quramiz: server LLM'dan kelgan har bo'lakni **kelishi bilanoq** mijozga uzatadi. Buning uchun FastAPI'da `StreamingResponse` va **SSE** (Server-Sent Events) ishlatamiz.

![Streaming endpoint oqimi: brauzer bitta ulanish ochadi, FastAPI StreamingResponse (media_type text/event-stream) async generator orqali "data: ..." satrlarini yield qiladi; FastAPI LLM'ni stream=True bilan chaqiradi, har chunk delta'sini SSE token bo'lib brauzerga oqim sifatida jo'natadi](rasmlar/aip26-streaming-sse.svg)

```python
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
async def chat_stream(sorov: ChatSorov):
    async def token_generator():
        stream = await client.chat.completions.create(
            model=settings.model,
            messages=[
                {"role": "system", "content": sorov.tizim},
                {"role": "user", "content": sorov.xabar},
            ],
            stream=True,
        )
        async for chunk in stream:                 # async for — async oqim
            delta = chunk.choices[0].delta.content
            if delta:                              # delta None bo'lishi mumkin (7-bob)
                yield f"data: {delta}\n\n"         # SSE formati: "data: <matn>\n\n"
        yield "data: [DONE]\n\n"                    # oqim tugaganini bildiramiz

    return StreamingResponse(token_generator(), media_type="text/event-stream")
```

E'tibor bering: oddiy `async def` o'rniga **async generator** (`yield`li funksiya) ishlatdik. Har `yield` — mijozga darrov jo'natiladigan bitta bo'lak. SSE formati oddiy: har xabar `data: ` bilan boshlanadi va `\n\n` bilan tugaydi.

> **Hayotiy o'xshatish.** Oddiy endpoint — butun xatni yozib, **konvertga solib** jo'natish: mijoz hammasi tayyor bo'lguncha kutadi. SSE streaming — **ochiq telefon liniyasi**: gapni so'z-so'z aytasiz, narigi tomon darrov eshitadi. Liniya bitta, lekin ma'lumot uzluksiz oqib turadi.

!!! tip "Frontend SSE'ni qanday o'qiydi?"
    Brauzerda JavaScript `fetch(...)` javobini `response.body.getReader()` bilan o'qiydi yoki `EventSource` ishlatadi va har kelgan `data:` bo'lagini chat oynasiga qo'shib boradi — natijada ChatGPT'dagidek "jonli yozish" effekti chiqadi. Server tomoni esa — yuqoridagi 15 qator.

---

## Xatolarni HTTP statusga map qilish

23-bobda LLM SDK'ning **tipli xatolarini** ko'rdik (`RateLimitError`, `AuthenticationError`, ...). API xizmatda bu xatolarni "yalang'och" qoldirsangiz, FastAPI har birini **500 Internal Server Error** qilib qaytaradi — mijoz nima bo'lganini tushunmaydi. To'g'ri yo'l: har xato turini **mos HTTP statusga** map qilish.

- Mijoz juda ko'p so'rasa yoki provayder limiti urilsa -> **429 Too Many Requests**.
- Mijoz noto'g'ri ma'lumot yuborsa -> **400 Bad Request** (Pydantic buni 422 bilan o'zi qiladi).
- Provayder yoki bizning tarafda nosozlik -> **500/502**.

FastAPI'da buni `HTTPException` bilan qilamiz:

```python
import openai
from fastapi import HTTPException

@app.post("/chat", response_model=ChatJavob)
async def chat(sorov: ChatSorov):
    try:
        resp = await client.chat.completions.create(
            model=settings.model,
            messages=[
                {"role": "system", "content": sorov.tizim},
                {"role": "user", "content": sorov.xabar},
            ],
            max_tokens=settings.max_tokens,
        )
    except openai.RateLimitError:
        # provayder limiti urildi — mijozga "keyinroq uring" deymiz
        raise HTTPException(status_code=429, detail="Hozir band, biroz keyin urinib ko'ring.")
    except openai.AuthenticationError:
        # kalit muammosi — bu BIZNING xatomiz, mijozga tafsilot bermaymiz
        raise HTTPException(status_code=500, detail="Server konfiguratsiya xatosi.")
    except openai.APIError:
        raise HTTPException(status_code=502, detail="LLM provayderi javob bermadi.")

    return ChatJavob(javob=resp.choices[0].message.content, tokenlar=resp.usage.total_tokens)
```

!!! warning "Ichki xatoni mijozga oqizmang"
    `AuthenticationError` — bu **sizning** kalit muammoyingiz, mijozga "kalit noto'g'ri" deb aytish ham foydasiz, ham xavfli (ichki tafsilot sizadi). Mijozga umumiy "server xatosi" bering, **batafsil sababni esa logingizga** yozing (25-bob). Qoida: mijoz uchun foydali, qisqa xabar; o'zingiz uchun to'liq log.

---

## Production eslatmalari

Endpoint ishlaydi — endi uni "internetga chiqarishdan" oldingi muhim nuqtalar.

### Kalit va sirlar

Kalit **faqat serverda** (24-bob). Lokal `.env`, production'da esa hosting platformasining **secret/environment** sozlamasi (Railway, Render, Fly.io, AWS va h.k.). Kalitni hech qachon konteyner image'iga "pishirib" yubormang — uni ish vaqtida environment orqali bering.

### CORS

Agar frontend boshqa domendan (masalan, `https://sayt.uz`) sizning API'ngizni chaqirsa, brauzer **CORS** siyosatini talab qiladi. FastAPI'da:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sayt.uz"],   # faqat ishonchli domenlar; "*" ni production'da ishlatmang
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

### Rate limit va concurrency

LLM so'rovi pul turadi (22-bob). Bitta foydalanuvchi (yoki bot) cheksiz so'rov yuborib **hisobingizni bo'shatmasligi** uchun **rate limit** qo'ying (masalan, `slowapi` kutubxonasi: IP bo'yicha daqiqada N so'rov). Bundan tashqari, bir vaqtdagi LLM chaqiruvlar sonini cheklash (semaphore) provayder limitini urmaslik uchun foydali.

### Logging va kuzatuv

25-bobdagi logging'ni shu yerga ulang: har so'rovni (model, token soni, davomiylik, status) yozing — lekin **maxfiy ma'lumot va to'liq kalitni logga yozmang**. Bu xarajatni kuzatish, sekin so'rovlarni topish va xatolarni tahlil qilish uchun zarur.

### `Dockerfile` (qisqa misol)

Xizmatni har joyda bir xil ishlatish uchun uni konteynerga joylaymiz:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# 4 worker bilan ishga tushiramiz (gunicorn + uvicorn worker)
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "4", "-b", "0.0.0.0:8000"]
```

```bash
docker build -t llm-xizmat .
docker run -p 8000:8000 --env-file .env llm-xizmat   # kalitni env orqali beramiz, image'ga emas
```

![Deploy topologiyasi: internetdagi mijozlar Docker konteyneriga ulanadi; konteyner ichida uvicorn/gunicorn master so'rovlarni bir nechta async worker'ga taqsimlaydi, sirlar (OPENAI_API_KEY) env/secret manager orqali beriladi (kodda emas); konteyner LLM provayder API'siga chiqadi; masshtab ko'proq worker yoki konteyner qo'shish bilan, og'ir ish esa queue orqali](rasmlar/aip26-deploy.svg)

### Masshtab: worker, konteyner, queue

- **Worker'lar.** Bitta jarayon yetmasa, `gunicorn -w N` bilan bir nechta worker ishga tushiring (odatda CPU yadrosiga bog'liq). Har biri async bo'lgani uchun ko'p parallel so'rovni eplaydi.
- **Gorizontal masshtab.** Yuk oshsa — bir nechta **konteyner** ishlatib, oldiga **load balancer** qo'yasiz. FastAPI xizmatingiz **stateless** bo'lsa (holatni o'zida saqlamasa, suhbat tarixini tashqi bazada saqlasa) — bu oson kengayadi.
- **Queue (navbat).** Juda uzun yoki og'ir ishlar (masalan, 100 hujjatni RAG uchun indekslash) HTTP so'rovni bloklamasin — ularni **fon navbatiga** (Celery/RQ kabi) yuboring va mijozga "tayyor bo'lganda xabar beramiz" deb javob qaytaring.

!!! note "Bu bob — keyingi kapstonlar poydevori"
    27 va 28-boblarda RAG chatbot va agent quramiz. Ularning "miyasi" — shu kitobda o'rgangan logikamiz; "tanasi" esa — aynan shu bobdagi FastAPI xizmati. Ya'ni har qanday AI loyihangiz pirovardida shunday endpoint ortida yashaydi va dunyoga shu eshik orqali "gapiradi".

---

## Xulosa

- **Skript** bitta odam uchun, **xizmat (API)** hamma uchun: LLM logikani **REST API** ortiga qo'yib, web/mobil/boshqa xizmatlar uni tarmoq orqali chaqiradi va kalitni hech qachon ko'rmaydi.
- **FastAPI** asoslari: `app = FastAPI()`, `@app.post("/chat")`, **Pydantic** so'rov/javob modeli (avtomatik validatsiya, `/docs`), `uvicorn main:app` bilan ishga tushirish.
- To'liq `/chat`: so'rov qabul -> LLM chaqir -> javob qaytar. Sozlamalarni `.env` + `pydantic-settings` (yoki `os.environ`) bilan boshqar, kalit **faqat serverda**.
- **Async muhim**, chunki LLM so'rovi sekin va **I/O-bound**: `async def` + `AsyncOpenAI` + `await` bitta jarayonda ko'p so'rovni parallel kutadi. Async ichida bloklovchi kod yozmang.
- **Streaming endpoint**: `StreamingResponse` + **async generator** + SSE (`yield f"data: {delta}\n\n"`) bilan token-token javob — ChatGPT'dagidek jonli (7-bobga tayanadi).
- Xatolarni **HTTP statusga map** qiling (23-bob): `RateLimitError`->429, noto'g'ri so'rov->400/422, provayder/ichki nosozlik->500/502; ichki tafsilotni mijozga oqizmang, **logga** yozing.
- Production: kalit serverda (24-bob), **CORS** faqat ishonchli domenlar, **rate limit**/concurrency, **logging** (25-bob), qisqa **`Dockerfile`**, masshtab = ko'proq worker/konteyner, og'ir ish -> **queue**.
- Bu bob — 27/28-kapstonlar uchun "joylashtirish" poydevori: AI logikangiz pirovardida shunday endpoint ortida yashaydi.

## Amaliy mashqlar

1. **(Oson)** FastAPI'ni o'rnating va eng kichik ilovani (`GET /` "ishlayapti" qaytaradigan) yozib, `uvicorn main:app --reload` bilan ishga tushiring. `http://127.0.0.1:8000/docs` ni brauzerda oching va endpointni shu yerdan sinab ko'ring.

2. **(Oson)** `ChatSorov` va `ChatJavob` Pydantic modellarini yozing va sinxron (`def`) `/chat` endpointini quring. `curl` yoki `/docs` orqali bitta savol yuborib, JSON javob va token sonini oling.

3. **(O'rtacha)** Endpointni `async def` + `AsyncOpenAI` ga o'tkazing. So'ng `httpx` yoki oddiy skript bilan **5 ta** so'rovni bir vaqtda (`asyncio.gather`) yuboring va sinxron versiyaga nisbatan umumiy vaqt qanchalik qisqarganini o'lchang.

4. **(O'rtacha)** `/chat/stream` streaming endpointini `StreamingResponse` va async generator bilan yozing. `curl -N http://127.0.0.1:8000/chat/stream ...` bilan javob token-token kelishini kuzating.

5. **(Qiyin)** Endpointga to'liq production qatlamini qo'shing: `try/except` bilan LLM xatolarini mos `HTTPException` (429/500/502) ga map qiling, CORS middleware va oddiy rate limit (masalan `slowapi`) o'rnating, har so'rovni (model, token, davomiylik, status) logga yozing va loyiha uchun `Dockerfile` yozib, `docker run --env-file .env` bilan ishga tushiring.

---

[⬅️ Oldingi: 25 — Kuzatuv, logging va baholash (eval)](./25-kuzatuv-baholash.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 27 — Kapston I: RAG chatbot ➡️](./27-kapston-rag-chatbot.md)
