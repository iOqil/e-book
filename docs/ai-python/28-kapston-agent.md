# 28 — Kapston II: agent-asoslangan avtomatlashtirish

[⬅️ Oldingi: 27 — Kapston I: RAG chatbot](./27-kapston-rag-chatbot.md) · [🏠 Kitob boshi](./README.md)

> **Bu bobda:** butun kitob bilimini bitta loyihaga jamlaymiz — **ko'p tool ishlatadigan, ko'p qadamda real vazifani hal qiladigan agent**. 18–19-boblardagi yadroni olib, uni production darajasiga ko'taramiz: loyihani uchta faylga ajratamiz (`tools.py`, `agent.py`, `main.py`), to'rt-besh ta **real tool** yozamiz (xavfsiz kalkulyator, web qidiruv, fayl yozish va 27-bobning RAG bazasiga ulanadigan qidiruv), agent loopni xotira va aniq to'xtash sharti bilan quramiz, **har qadamni kuzatuv (logging)** bilan kuzatamiz, xato va xarajatni boshqaramiz va nihoyat uni CLI hamda FastAPI orqali ishga tushiramiz. Oxirida sizning qo'lingizda "tadqiqot yordamchisi" — savolni olib, kerakli toollarni o'zi tanlab, qadam-baqadam hisobot tayyorlaydigan ishlaydigan agent bo'ladi. **Bu — butun kitobning yakuniy bobi.**

---

## Muammodan boshlaymiz: bitta funksiya yetmaydi

27-bobda biz RAG chatbot qurdik — u savolni oladi, hujjatlardan kerakli qismni topadi va javob beradi. Bu **workflow** edi: qadamlar oldindan ma'lum (qidir -> kontekst qo'sh -> javob ber). Lekin endi quyidagi topshiriqni tasavvur qiling:

> "Bizning narx ro'yxatimizdan eng qimmat uchta mahsulot summasini hisobla, ularning o'rtacha narxini chiqar va natijani `hisobot.txt` faylga yoz."

Bu **bitta** so'rov, lekin uni hal qilish uchun bir nechta turli xil qadam kerak: ichki hujjatdan ma'lumot topish (RAG), arifmetik hisob (kalkulyator), faylga yozish (fayl tool). Va eng muhimi — **necha qadam va qaysi tartibda kerakligini oldindan bilmaysiz**: savol o'zgarsa, yo'l ham o'zgaradi. Mana shu yerda **workflow yetmaydi** — bizga **agent** kerak: vazifaga qarab toollarni o'zi tanlab, o'zi to'xtaydigan tizim (18-bob).

> **Hayotiy o'xshatish.** RAG chatbot — bitta savolga bitta sahifa topib beradigan **kutubxonachi**. Agent esa — **tadqiqotchi yordamchi**: unga umumiy vazifa berasiz, u o'zi kerakli manbalarni qidiradi, hisob-kitob qiladi, qoralama yozadi, oraliq natijaga qarab yo'lini tuzatadi va tugagach sizga tayyor hisobot keltiradi. Siz har qadamni aytib turmaysiz.

!!! note "Bu bob nimaga tayanadi"
    Bu kapston — **18-bob** (agent nima, ReAct sikli) va ayniqsa **19-bob** (0 dan agent: registry + loop + xotira + to'xtash + xavfsizlik) ning to'g'ridan-to'g'ri davomi. Tool calling (10–11), kuzatuv (25), xarajat (22) va xato boshqaruvi (23) ham shu yerda birlashadi. Agar agent loop sizga notanish bo'lsa — avval 19-bobni qaytaring.

---

## Loyiha tuzilishi: uchta toza fayl

Bitta uzun skript o'rniga loyihani **mas'uliyatga ko'ra** uchga ajratamiz. Bu professional amaliyot: har fayl bitta ish qiladi, sinash va kengaytirish oson bo'ladi.

![Agent tizimi arxitekturasi: main.py interfeys (CLI yoki FastAPI) agent.py dagi Agent klassni chaqiradi; Agent loop ichida modelni chaqiradi, qaror qabul qiladi, tools.py dagi registry orqali toollarni bajaradi; messages xotira loop bilan birga o'sadi; kuzatuv (logging) har qadamni yon tomonda yozib boradi; toollar tashqi dunyoga (kalkulyator, web, fayl, RAG bazasi) ulanadi](rasmlar/aip28-arxitektura.svg)

```text
tadqiqot-agent/
├── tools.py    # tool funksiyalari + ta'riflar (sxema) + REGISTRY
├── agent.py    # Agent klass: loop, xotira, to'xtash, kuzatuv, xavfsizlik
├── main.py     # ishga tushirish: CLI yoki FastAPI
└── .env        # API kalit (GitHub'ga YUKLAMANG)
```

> **Hayotiy o'xshatish.** Bu uch fayl — ustaxonadagi **uch bo'lim**: `tools.py` — asboblar javoni (har asbob o'z yorlig'i bilan); `agent.py` — ustaning ish tartibi (qachon qaysi asbobni olish, qachon to'xtash); `main.py` — mijoz bilan gaplashadigan qabulxona. Bo'limlar aralashmaydi — shuning uchun bittasini o'zgartirsangiz, qolgani buzilmaydi.

!!! tip "Nega ajratish kerak?"
    Hamma narsa bitta faylda bo'lsa, 200 qatordan keyin uni tushunish qiyinlashadi va sinash deyarli imkonsiz. Ajratilgan loyihada `tools.py`ni alohida sinab ko'rasiz, `agent.py`ni soxta tool bilan tekshirasiz, `main.py`ni esa interfeys o'zgarsa ham (CLI'dan API'ga) qolgan kodga tegmasdan almashtirasiz.

---

## 1-qadam: `tools.py` — real toollar, sxema va registry

Toollar — agentning "qo'l-oyog'i". 19-bobdagi g'oyani eslang: har tool uchun (a) **funksiya** (haqiqiy ish), (b) modelga yuboriladigan **ta'rif/sxema**, (c) **registry** yozuvi (nom -> funksiya). Bu kapstonda **to'rtta real tool** yozamiz:

1. `kalkulyator` — `ast` bilan **xavfsiz** arifmetika (`eval` EMAS).
2. `web_qidir` — web qidiruv (demo: oddiy lug'at; real loyihada qidiruv API'si).
3. `fayl_yoz` — natijani faylga yozadi (yo'lni tekshiradi — path traversal'dan himoya).
4. `hujjat_qidir` — 27-bobning **RAG vektor bazasiga** ulanib, ichki hujjatlardan qidiradi.

```python
# tools.py — tool funksiyalari, ta'riflari va registry
import os
import ast
import json
import operator
from pathlib import Path

# === Tool 1: xavfsiz kalkulyator (ast, eval EMAS) =====================
_AMALLAR = {ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.Pow: operator.pow, ast.Mod: operator.mod,
            ast.USub: operator.neg}

def kalkulyator(ifoda: str) -> dict:
    """'125 * 8 + 17' kabi ifodani XAVFSIZ hisoblaydi (ast bilan, eval'siz)."""
    def bahola(t):
        if isinstance(t, ast.Constant) and isinstance(t.value, (int, float)):
            return t.value
        if isinstance(t, ast.BinOp):
            return _AMALLAR[type(t.op)](bahola(t.left), bahola(t.right))
        if isinstance(t, ast.UnaryOp):
            return _AMALLAR[type(t.op)](bahola(t.operand))
        raise ValueError("ruxsat etilmagan ifoda")
    try:
        return {"natija": bahola(ast.parse(ifoda, mode="eval").body)}
    except Exception as e:
        return {"xato": f"hisoblab bo'lmadi: {e}"}

# === Tool 2: web qidiruv (DEMO; real loyihada qidiruv API'si) =========
def web_qidir(sorov: str) -> dict:
    """Internetdan qidiradi (DEMO: soxta baza; real loyihada Tavily/SerpAPI)."""
    soxta_baza = {
        "python yili": "Python birinchi marta 1991-yilda chiqarilgan.",
        "llm nima": "LLM — katta matn ustida o'rgatilgan, matn generatsiya qiladigan AI modeli.",
    }
    matn = soxta_baza.get(sorov.lower().strip(),
                          f"'{sorov}' bo'yicha aniq natija topilmadi (demo baza).")
    return {"sorov": sorov, "natija": matn}

# === Tool 3: faylga yozish (yo'lni tekshiradi) ========================
ISH_PAPKA = Path("./agent_natijalar").resolve()   # faqat shu papkaga yozish mumkin

def fayl_yoz(fayl_nomi: str, matn: str) -> dict:
    """Matnni ISH_PAPKA ichidagi faylga yozadi. Tashqariga chiqishga ruxsat yo'q."""
    ISH_PAPKA.mkdir(exist_ok=True)
    yol = (ISH_PAPKA / fayl_nomi).resolve()
    # XAVFSIZLIK: path traversal'dan himoya — yo'l ISH_PAPKA ichida bo'lsin
    if not str(yol).startswith(str(ISH_PAPKA)):
        return {"xato": "ruxsat etilmagan yo'l (papkadan tashqariga chiqib bo'lmaydi)"}
    try:
        yol.write_text(matn, encoding="utf-8")
        return {"holat": "yozildi", "yol": str(yol), "belgilar": len(matn)}
    except Exception as e:
        return {"xato": f"yozib bo'lmadi: {e}"}

# === Tool 4: ichki hujjatlardan qidir (27-bobning RAG bazasi) =========
def hujjat_qidir(sorov: str, top_k: int = 3) -> dict:
    """27-bobda qurilgan Chroma vektor bazadan eng yaqin chunklarni topadi."""
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        client = chromadb.PersistentClient(path="./chroma_db")   # 27-bobdagi baza (config.DB_YOL)
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-3-small",
        )
        kol = client.get_collection("bilim_bazasi", embedding_function=ef)  # 27-bob: KOLLEKSIYA
        natija = kol.query(query_texts=[sorov], n_results=top_k)
        chunklar = natija["documents"][0]
        return {"sorov": sorov, "topildi": len(chunklar), "kontekst": chunklar}
    except Exception as e:
        # Baza hali yo'q bo'lsa ham agent yiqilmasin — xatoni natija qilamiz
        return {"xato": f"hujjat bazasiga ulanib bo'lmadi: {e}"}

# === REGISTRY: model qaytaradigan NOM -> haqiqiy funksiya =============
REGISTRY = {
    "kalkulyator": kalkulyator,
    "web_qidir": web_qidir,
    "fayl_yoz": fayl_yoz,
    "hujjat_qidir": hujjat_qidir,
}

# === Modelga yuboriladigan TA'RIFLAR (sxema) ==========================
# description — modelning "ko'zi": u qachon qaysi toolni ishlatishni shundan biladi.
TOOLS = [
    {"type": "function", "function": {
        "name": "kalkulyator",
        "description": "Matematik ifodani aniq hisoblaydi. Hisob-kitob kerak bo'lganda ishlat.",
        "parameters": {"type": "object",
            "properties": {"ifoda": {"type": "string",
                "description": "Hisoblanadigan ifoda, masalan '1200 + 850 + 990'"}},
            "required": ["ifoda"]}}},
    {"type": "function", "function": {
        "name": "web_qidir",
        "description": "Umumiy fakt yoki yangi ma'lumotni internetdan qidiradi. Modelda bilim yetmasa ishlat.",
        "parameters": {"type": "object",
            "properties": {"sorov": {"type": "string", "description": "Qidiruv so'rovi"}},
            "required": ["sorov"]}}},
    {"type": "function", "function": {
        "name": "hujjat_qidir",
        "description": "Bizning ICHKI hujjatlardan (narx ro'yxati, qo'llanma) ma'lumot qidiradi. "
                       "Foydalanuvchi 'bizning', 'narx ro'yxatimiz' kabi ichki ma'lumot so'rasa ishlat.",
        "parameters": {"type": "object",
            "properties": {"sorov": {"type": "string", "description": "Hujjatlardan qidiriladigan savol"}},
            "required": ["sorov"]}}},
    {"type": "function", "function": {
        "name": "fayl_yoz",
        "description": "Tayyor natija yoki hisobotni faylga yozadi. Foydalanuvchi 'faylga yoz', "
                       "'saqla' deganda ishlat.",
        "parameters": {"type": "object",
            "properties": {
                "fayl_nomi": {"type": "string", "description": "Fayl nomi, masalan 'hisobot.txt'"},
                "matn": {"type": "string", "description": "Faylga yoziladigan to'liq matn"}},
            "required": ["fayl_nomi", "matn"]}}},
]
```

E'tibor bering: har tool xatoni `raise` qilmaydi, balki **natija sifatida** (`{"xato": ...}`) qaytaradi. Bu — agent uchun muhim: xatoda butun loop yiqilmaydi, model xatoni "ko'radi" va boshqa yo'l tutadi.

> **Hayotiy o'xshatish.** `TOOLS` ta'riflari — modelga berilgan **menyu** (har taom nomi va tavsifi); `REGISTRY` — oshxonadagi **retseptlar**. Model menyudan nom tanlaydi, oshxona (sizning kodingiz) o'sha nomga mos retseptni pishiradi. Model oshxonaga kirmaydi — faqat nom aytadi.

!!! warning "Tool ichida eval/exec/os.system — HECH QACHON"
    Tool argumentlarini **model to'qiydi** — demak ular ishonchsiz kirish (19, 24-boblar). Shuning uchun `kalkulyator` `eval` emas, `ast` + oq ro'yxat; `fayl_yoz` esa yo'lni `resolve()` qilib, ish papkadan tashqariga chiqishni rad etadi. Modelga berilgan har bir tool — potensial xavf darvozasi; uni tor va tekshiruvchi qilib yozing.

---

## 2-qadam: `agent.py` — loop, xotira, to'xtash, kuzatuv

Endi yadroni quramiz. Bu — 19-bobdagi `Agent` klassning kengaytmasi: ustiga **kuzatuv (logging)**, **vaqt o'lchash** va **xarajat hisobi** qo'shamiz.

### Avval kuzatuvni sozlaymiz (25-bob)

`print` — debug uchun yaxshi, lekin production'da **`logging`** kerak: vaqt, daraja, faylga yozish imkoni. Har qadamni — qaysi tool, qancha vaqt, qancha token — yozib boramiz.

```python
# agent.py
import os, json, time, logging
from dotenv import load_dotenv
from openai import OpenAI
import tools as T   # bizning tools.py

load_dotenv()

# === Kuzatuv: har qadamni log qilamiz (25-bob) =======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(),                       # ekranga
              logging.FileHandler("agent.log", encoding="utf-8")],  # faylga
)
log = logging.getLogger("agent")

client = OpenAI()          # OpenAI-mos: base_url + kalitni almashtirsangiz boshqa provayder
MODEL = "gpt-5.4-mini"     # Eslatma: model nomlari o'zgaradi — provayder ro'yxatini tekshiring

# Inson tasdig'i talab qiladigan "xavfli" toollar (qaytarilmas amallar)
XAVFLI_TOOLLAR = {"fayl_yoz"}
```

> **Hayotiy o'xshatish.** Kuzatuv — agentning **qora qutisi** (samolyotdagi kabi): agent g'alati ish qilsa, log'ga qarab "qaysi qadamda, qaysi tool, qanday natija" — hammasini tiklaysiz. Logsiz agent — yo'lda nima bo'lganini hech kim bilmaydigan, faqat oxirgi natijani ko'rsatadigan qora quti emas, balki **butunlay ko'r quti**.

### Agent klass

```python
class TadqiqotAgent:
    def __init__(self, model=MODEL, maks_qadam=8):
        self.model = model
        self.maks_qadam = maks_qadam      # XAVFSIZLIK: cheksiz loopdan himoya (19-bob)
        self.jami_token = 0               # XARAJAT: token sarfini yig'amiz (22-bob)

    def _tool_bajar(self, tool_call) -> str:
        """Bitta tool_call'ni xavfsiz bajaradi, natijani JSON-matn qaytaradi."""
        nom = tool_call.function.name
        try:
            args = json.loads(tool_call.function.arguments or "{}")
        except json.JSONDecodeError:
            return json.dumps({"xato": "argumentlar JSON emas"}, ensure_ascii=False)

        funksiya = T.REGISTRY.get(nom)
        if funksiya is None:
            return json.dumps({"xato": f"noma'lum tool: {nom}"}, ensure_ascii=False)

        # XAVFSIZLIK: xavfli tool oldidan inson tasdig'i (human-in-the-loop)
        if nom in XAVFLI_TOOLLAR:
            javob = input(f"  [tasdiq] '{nom}' ni {args} bilan bajaraymi? (ha/yo'q): ")
            if javob.strip().lower() not in {"ha", "h", "y", "yes"}:
                return json.dumps({"xato": "foydalanuvchi rad etdi"}, ensure_ascii=False)

        # KUZATUV: har toolning vaqtini o'lchaymiz (25-bob)
        boshlandi = time.perf_counter()
        try:
            natija = funksiya(**args)         # XAVFSIZLIK: validatsiya tool ichida
        except TypeError as e:
            natija = {"xato": f"noto'g'ri argumentlar: {e}"}
        except Exception as e:
            natija = {"xato": str(e)}          # exception emas, NATIJA qaytaramiz
        vaqt = (time.perf_counter() - boshlandi) * 1000
        log.info("tool=%s args=%s vaqt=%.0fms", nom, args, vaqt)
        return json.dumps(natija, ensure_ascii=False)

    def ishlat(self, savol: str) -> str:
        # XOTIRA: butun suhbat va tool natijalari shu ro'yxatda (19-bob)
        messages = [
            {"role": "system", "content":
                "Sen tadqiqot yordamchisisan. Murakkab vazifani qadamlarga bo'l. "
                "Hisob-kitobni kalkulyatorga, ichki ma'lumotni hujjat_qidir'ga, "
                "umumiy faktni web_qidir'ga topshir. Faylga yozishni so'ralganda fayl_yoz ishlat. "
                "Yetarli ma'lumot yig'ilgach, aniq va qisqa yakuniy hisobot ber."},
            {"role": "user", "content": savol},
        ]

        for qadam in range(1, self.maks_qadam + 1):    # TO'XTASH: qadam limiti
            log.info("=== %d-qadam ===", qadam)
            try:
                resp = client.chat.completions.create(
                    model=self.model, messages=messages, tools=T.TOOLS,
                )
            except Exception as e:
                # XATO BOSHQARUVI (23-bob): API yiqilsa, agent ham yiqilmasin
                log.error("API xatosi: %s", e)
                return f"API bilan bog'lanishda xato: {e}"

            # XARAJAT (22-bob): token sarfini yig'amiz
            if resp.usage:
                self.jami_token += resp.usage.total_tokens

            msg = resp.choices[0].message

            # TO'XTASH SHARTI 1: tool chaqirilmadi -> yakuniy javob
            if not msg.tool_calls:
                log.info("yakun: model matn qaytardi | jami_token=%d", self.jami_token)
                return msg.content

            # Aks holda: barcha tool_call'larni bajaramiz
            messages.append(msg)                        # assistant navbati (tool_calls bilan)
            for tc in msg.tool_calls:
                natija = self._tool_bajar(tc)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,              # qaysi chaqiruvga javob ekanini bog'laydi
                    "content": natija,
                })
            # Sikl boshiga qaytadi -> model natijalarni ko'rib davom etadi

        # TO'XTASH SHARTI 2: qadam limiti tugadi
        log.warning("qadam limiti tugadi (maks=%d)", self.maks_qadam)
        return "Kechirasiz, qadam limiti tugadi — vazifani to'liq yakunlay olmadim."
```

Mana shu — to'liq agent. U 19-bobdagi yadroni saqlaydi, lekin endi: (a) har qadam va har tool **log**ga yoziladi, (b) tool **vaqti** o'lchanadi, (c) **token sarfi** yig'iladi, (d) API xatosi ushlanib, agent yiqilmaydi.

![Ko'p tool orkestratsiyasi: foydalanuvchi vazifasi modelga keladi; model har qadamda toollar menyusini ko'rib O'ZI qaysi toolni qaysi tartibda chaqirishni hal qiladi — hujjat_qidir bilan ichki ma'lumot, kalkulyator bilan hisob, fayl_yoz bilan saqlash; har tool natijasi xotiraga qaytib, model keyingi qarorini shunga qarab qiladi; yetarli bo'lganda yakuniy hisobot beradi](rasmlar/aip28-orkestratsiya.svg)

> **Hayotiy o'xshatish.** Model — **dirijyor**, toollar — **cholg'uchilar**. Dirijyor partiturani (vazifani) o'qib, har lahzada qaysi cholg'u qachon kirishini ko'rsatadi: avval skripka (hujjat_qidir), keyin pianino (kalkulyator), oxirida nog'ora (fayl_yoz). Hech bir cholg'u o'zicha chalmaydi — dirijyor (model) tartibni boshqaradi, lekin har lahza eshitilgan ovozga (tool natijasiga) qarab keyingi ishorani beradi.

!!! tip "Trace — agentni tushunishning kaliti"
    Agent g'alati ish qilsa, birinchi qaraydigan joy — `agent.log`. Qaysi tool chaqirildi? Argumentlar to'g'rimi? Tool nima qaytardi? Ko'pincha muammo — yomon `description` (model noto'g'ri tool tanlaydi) yoki tool natijasidagi xato. Log bularning hammasini ko'rsatadi.

---

## 3-qadam: xato va xarajat boshqaruvi (qisqacha)

Agent — **ko'p chaqiruvli** dastur, shuning uchun xato va xarajat oddiy chatdagidan jiddiyroq. Yuqoridagi kodda allaqachon to'rtta himoya bor — ularni nomlab o'tamiz:

- **Qadam limiti** (`maks_qadam`, 18–19-bob). Har aylanma — pulli API chaqiruvi; limitsiz agent — vaqt va pul bombasi. 6–10 odatda yetarli.
- **Token kuzatuvi** (`jami_token`, 22-bob). Har chaqiruvda butun `messages` qayta yuboriladi, shuning uchun **xotira o'sgani sayin har qadam qimmatlashadi**. Token sarfini yig'ib, log'ga chiqaramiz — keyin narxga aylantirish oson.
- **API xatosini ushlash** (`try/except`, 23-bob). Tarmoq uzilsa yoki rate limit chiqsa, butun loop yiqilmasin. Production'da bu yerga **exponential backoff bilan retry** qo'yiladi.
- **Xatoni natija qilish.** Tool xatosi `raise` emas, `{"xato": ...}` bo'lib modelga qaytadi — model uni ko'rib o'zini tuzatadi.

```python
# Narxga aylantirish (22-bob): 1M token uchun taxminiy narx (provayderdan tekshiring)
NARX_1M = 0.60        # USD / 1M token (misol; model va provayderga qarab o'zgaradi)
def taxminiy_narx(token: int) -> float:
    return token / 1_000_000 * NARX_1M
```

!!! warning "Xarajat agentda kuchayadi"
    8 qadamli agent — 8 ta oddiy so'rov emas, balki **8 ta tobora kattalashayotgan** so'rov (har safar butun tarix qayta yuboriladi). Shuning uchun: (a) arzon model tanlang (`gpt-5.4-mini`/`gemini-2.5-flash`), (b) qadam limitini joyida tuting, (c) kerak bo'lmaganda eski tool natijalarini qisqartiring (8-bob). Token kuzatuvi — birinchi himoya.

---

## 4-qadam: `main.py` — interfeys (CLI va FastAPI)

Yadro tayyor; endi unga "eshik" qo'shamiz. Avval eng oddiy — **CLI** (terminalda suhbat):

```python
# main.py — CLI varianti
from agent import TadqiqotAgent, taxminiy_narx

def cli():
    agent = TadqiqotAgent(maks_qadam=8)
    print("Tadqiqot yordamchisi. Vazifa yozing ('chiqish' — to'xtatish).")
    while True:
        savol = input("\nVazifa> ").strip()
        if savol.lower() in {"chiqish", "exit", "quit"}:
            break
        javob = agent.ishlat(savol)
        print("\n=== YAKUNIY HISOBOT ===")
        print(javob)
        print(f"\n[token: {agent.jami_token}, taxminiy narx: ${taxminiy_narx(agent.jami_token):.4f}]")

if __name__ == "__main__":
    cli()
```

Endi xuddi shu agentni **FastAPI** orqali HTTP xizmati qilamiz (26-bob) — boshqa ilovalar undan foydalansin:

```python
# main.py — FastAPI varianti (uvicorn main:app --reload)
from fastapi import FastAPI
from pydantic import BaseModel
from agent import TadqiqotAgent, taxminiy_narx

app = FastAPI(title="Tadqiqot agenti")

class Sorov(BaseModel):
    vazifa: str
    maks_qadam: int = 8

@app.post("/agent")
def agent_endpoint(s: Sorov):
    agent = TadqiqotAgent(maks_qadam=s.maks_qadam)   # har so'rovga toza xotira
    javob = agent.ishlat(s.vazifa)
    return {
        "hisobot": javob,
        "token": agent.jami_token,
        "taxminiy_narx_usd": round(taxminiy_narx(agent.jami_token), 4),
    }
```

Diqqat: **yadro (`agent.py`) o'zgarmadi** — faqat unga ulanish usulini almashtirdik. Mana shu — loyihani fayllarga ajratishning mevasi: bitta agent, ko'p interfeys.

> **Hayotiy o'xshatish.** `agent.py` — restoran **oshxonasi**; `main.py` — **zal**. CLI — bu kichik oilaviy kafe (mijoz to'g'ridan-to'g'ri oshxona oynasiga kelib buyuradi); FastAPI — bu yetkazib berish xizmati (buyurtma telefon/ilovadan keladi). Oshxona (mantiq) bir xil; faqat buyurtma qabul qilish usuli farq qiladi.

!!! note "Har so'rovga toza agent"
    FastAPI variantida har `/agent` so'rovi uchun **yangi** `TadqiqotAgent` yaratamiz. Sababi — `messages` xotirasi va `jami_token` har vazifaga **toza** boshlanishi kerak; aks holda bir foydalanuvchi suhbati boshqasiga aralashib ketadi. Production'da foydalanuvchi sessiyalarini alohida saqlash kerak (8-bob).

---

## Namuna ish: boshdan oxir

Endi hammasini birga ko'ramiz. Foydalanuvchi murakkab, ko'p qadamli vazifa beradi:

> "Bizning narx ro'yxatimizdagi eng qimmat uchta mahsulot 1200, 990 va 850 ekan. Ularning yig'indisini va o'rtachasini hisobla, qisqa xulosa yoz va `hisobot.txt`ga saqla."

Agent buni qanday hal qiladi — `agent.log`dagi trace:

```text
2026-06-15 14:30:01 | INFO | === 1-qadam ===
2026-06-15 14:30:02 | INFO | tool=kalkulyator args={'ifoda': '1200 + 990 + 850'} vaqt=1ms
2026-06-15 14:30:02 | INFO | tool=kalkulyator args={'ifoda': '(1200 + 990 + 850) / 3'} vaqt=0ms
2026-06-15 14:30:03 | INFO | === 2-qadam ===
  [tasdiq] 'fayl_yoz' ni {'fayl_nomi': 'hisobot.txt', ...} bilan bajaraymi? (ha/yo'q): ha
2026-06-15 14:30:05 | INFO | tool=fayl_yoz args={'fayl_nomi': 'hisobot.txt', ...} vaqt=2ms
2026-06-15 14:30:06 | INFO | === 3-qadam ===
2026-06-15 14:30:07 | INFO | yakun: model matn qaytardi | jami_token=1843

=== YAKUNIY HISOBOT ===
Hisob tayyor. Uch mahsulot yig'indisi: 3040, o'rtacha narx: 1013.33.
Xulosa hisobot.txt fayliga saqlandi.

[token: 1843, taxminiy narx: $0.0011]
```

Eng muhimini ko'ring: **biz "avval qo'sh, keyin o'rtachani hisobla, keyin faylga yoz" deb yozmadik.** Buni **model o'zi** rejalashtirdi — bir qadamda ikki marta kalkulyatorni chaqirdi, keyin `fayl_yoz`ni (tasdiq so'rab), so'ng yakuniy matnni berdi. Va `fayl_yoz` xavfli bo'lgani uchun agent bizdan **tasdiq so'radi**. Mana shu — agent: vazifaga qarab yo'lni o'zi tuzadi, xavfli qadamda esa nazoratni sizga qaytaradi.

![Boshdan oxir vazifa oqimi: foydalanuvchi maqsadi (eng qimmat 3 mahsulotni hisobla va faylga yoz) agentga keladi; agent qadamlarga bo'ladi — kalkulyator bilan yig'indi, kalkulyator bilan o'rtacha, fayl_yoz bilan saqlash (inson tasdig'i bilan); har qadam log'ga yoziladi; oxirida yakuniy hisobot va token/narx qaytadi](rasmlar/aip28-vazifa-oqimi.svg)

!!! question "Bu workflow bilan ham bo'lardimi?"
    Ha — agar vazifa **doim** aynan shu shaklda bo'lsa (3 son, qo'sh, o'rtacha, yoz), oddiy workflow yetardi va arzonroq bo'lardi (18-bob). Lekin agent kuchi — **vazifa o'zgarganda**: foydalanuvchi "eng qimmat 5 tasini ol, ichki bazadan top va o'rtachasini chiqar" desa, **kod o'zgarmaydi** — model yangi yo'lni o'zi tuzadi (`hujjat_qidir` -> `kalkulyator` -> ...). Agentni "yo'l oldindan noma'lum" bo'lgan joyda ishlating.

---

## Tabriklaymiz! Siz nimani o'rgandingiz

Bu — nafaqat bobning, balki **butun kitobning yakuni**. Bir lahza orqaga qarab, qancha yo'l bosib o'tganingizni ko'ring.

Siz **bir qatordan ham AI'siz** boshladingiz — "integratsiya nima" degan savol bilan (1-bob). Endi esa **o'zingiz tool ishlatadigan, ko'p qadamda fikrlaydigan agent** qurdingiz. Mana bosib o'tgan yo'lingiz:

- **Asoslar** (1–8): birinchi so'rovdan to chat formati, ko'p provayder, prompt muhandisligi, parametrlar, streaming va suhbat xotirasigacha. Siz LLM bilan ishonchli "gaplashish"ni o'rgandingiz.
- **Strukturali natija va tool** (9–12): JSON va Pydantic bilan modelni ilovangizga **ulash**, tool/function calling bilan modelga **tashqi dunyoga ta'sir qilish** kuchini berish, multimodal bilan rasm va ovozni qo'shish.
- **RAG** (13–17): embeddings va vektor bazasi bilan **o'z bilimingiz** ustida savol-javob — modelni sizning hujjatlaringizni "biladigan" qildingiz va hallucination'ni kamaytirdingiz.
- **Agentlar** (18–20): ReAct sikli, 0 dan agent, freymvork va MCP — modelga **mustaqil qaror** qilish va ketma-ket harakat qilish imkonini berdingiz.
- **Lokal va production** (21–26): Ollama bilan bepul/maxfiy ishlash, xarajat, ishonchlilik, xavfsizlik, kuzatuv va FastAPI bilan **deploy** — o'yinchoq skriptdan haqiqiy xizmatga o'tdingiz.
- **Kapston** (27–28): RAG chatbot va agent — hamma bilimni **bitta ishlaydigan tizimga** birlashtirdingiz.

> **Hayotiy o'xshatish.** Boshida siz "rozetkaga ulanish"ni o'rgandingiz (1-bob). Endi esa **butun bir uy elektr tarmog'ini** — xavfsizlik avtomatlari (limit, validatsiya), hisoblagich (token kuzatuvi), bir nechta xona (tool) va boshqaruv panel (agent loop) bilan — o'z qo'lingiz bilan yig'a olasiz. Rozetkadan tarmoqqacha bo'lgan yo'lni bosib o'tdingiz.

### Keyingi qadamlar: qayerga o'sish

Bu kitob — poydevor. Mana yo'nalishlar, qaysi biri qiziq bo'lsa, o'sha tomonga rivojlaning:

- **Ko'proq va kuchliroq tool.** Demo `web_qidir` o'rniga haqiqiy qidiruv API (Tavily, SerpAPI), DB so'rovi, kod ishga tushirish (sandbox'da), API integratsiyalari. Tool qancha ko'p va sifatli — agent shunchalik foydali.
- **MCP (Model Context Protocol).** Toollarni standart protokol orqali ulang (20-bob) — bir marta yozilgan tool ko'p agent va ilovaga ulanadi.
- **Kuzatuv platformalari.** `print`/`logging`dan keyingi qadam — LangSmith, Langfuse, OpenTelemetry kabi tracing platformalari: har qadamni, xarajatni, sifatni dashboard'da kuzatasiz (25-bob).
- **Baholash (eval).** Agent javoblarini avtomatik baholang — LLM-as-judge, regress sinovlar, A/B (25-bob). "Yaxshilash uchun avval o'lchash kerak."
- **Fine-tuning.** Maxsus vazifa uchun model sozlash (1-bobda aytganimizdek — kamdan-kam kerak, lekin ba'zan o'rinli).
- **Jamoa loyihasi.** Eng yaxshi o'rganish — **real loyiha** qurish: o'zingizning hujjatlaringiz ustida RAG yordamchi, ish jarayoningizni avtomatlashtiradigan agent. Bu kitobdagi hamma narsa shu yerga olib keladi.

Eng muhim maslahat — o'zgarmaydi: **o'qib emas, qilib o'rganiladi.** Endi bilimingiz bor; navbat — o'z g'oyangizni qurishda. Omad!

---

## Xulosa

- **Kapston agent** — butun kitob bilimini birlashtiradi: ko'p tool, ko'p qadam, real vazifa. U **workflow** emas — yo'lni model o'zi tuzadi (18-bob).
- Loyihani uchga ajrating: **`tools.py`** (funksiya + ta'rif + registry), **`agent.py`** (loop + xotira + to'xtash + kuzatuv + xavfsizlik), **`main.py`** (CLI yoki FastAPI). Har fayl bitta ish — sinash va kengaytirish oson.
- **Toollar** real va xavfsiz bo'lsin: `kalkulyator` (`ast`, `eval` emas), `web_qidir`, `fayl_yoz` (yo'lni tekshiradi), `hujjat_qidir` (27-bobning RAG bazasi). Har biri xatoni `{"xato": ...}` **natija sifatida** qaytaradi — loop yiqilmaydi.
- **Agent loop** (19-bob): `for qadam in range(maks_qadam)` — model chaqir; `tool_calls` bo'lsa bajarib natijani xotiraga qo'sh va takror; oddiy matn bo'lsa — yakuniy hisobot. **Xotira** (`messages`) har qadamda o'sadi.
- **Kuzatuv** (25-bob): `print` emas, `logging` — har qadam, har tool, vaqt va token log'ga yoziladi. Bu — agentning "qora qutisi", debug uchun bebaho.
- **Xato/xarajat** (22–23-bob): qadam limiti, token kuzatuvi, API xatosini ushlash, xatoni natija qilish — to'rtta himoya. Agentda xarajat kuchayadi (har qadam butun tarixni qayta yuboradi).
- **Interfeys**: bir xil yadro CLI va FastAPI orqali ishlaydi — yadroni fayllarga ajratganimiz uchun interfeysni almashtirish qolgan kodga tegmaydi.
- **Xavfsizlik**: qadam limiti, xavfli tool uchun **inson tasdig'i**, argument validatsiya, tor tool yo'llari — agentni hech qachon chegarasiz qo'ymang (18–19, 24-bob).
- **Yakun**: 1-bobdagi "rozetkaga ulanish"dan to to'liq agent tizimigacha keldingiz. Keyingi o'sish — ko'proq tool, MCP, kuzatuv platformalari, eval va, eng muhimi — **o'z real loyihangiz**.

## Amaliy mashqlar

1. **(Oson)** Bobdagi uch faylni (`tools.py`, `agent.py`, `main.py`) tering va CLI'ni ishga tushiring. "125 * 8 + 17 necha bo'ladi va natijani `javob.txt`ga yoz" deb so'rang. Trace'da qaysi toollar, qaysi tartibda chaqirilganini va `fayl_yoz` oldidan tasdiq so'ralganini kuzating.

2. **(Oson)** `tools.py`ga yangi tool qo'shing: `harf_sanagich(matn)` — matndagi harflar sonini qaytarsin. Uni `REGISTRY` va `TOOLS`ga qo'shing (`agent.py` loopiga **tegmang**) va "'salom dunyo' iborasida nechta harf bor?" deb so'rang. Agent uni o'zi tanlaganini ko'ring.

3. **(O'rtacha)** `maks_qadam=1` qilib, bir qadamda yakunlanmaydigan vazifa bering ("Toshkent va Samarqand aholisini hujjatdan topib, qo'shib, faylga yoz"). Limit tugaganda agent qaysi xabarni qaytarganini va `agent.log`da nima ko'rinishini tahlil qiling. Keyin `maks_qadam`ni oshirib, farqni ko'ring.

4. **(O'rtacha)** FastAPI variantini `uvicorn main:app`bilan ishga tushiring va `/agent` endpointiga `curl` yoki `/docs` orqali vazifa yuboring. Javobdagi `token` va `taxminiy_narx_usd`ni kuzating. Bir necha xil murakkablikdagi vazifa yuborib, qaysi biri ko'proq token sarflashini taqqoslang (xulosa: ko'p qadam = ko'p token).

5. **(Qiyin)** Agentni "ishonchli" qiling: (a) `client.chat.completions.create` atrofiga **exponential backoff bilan retry** qo'shing (23-bob: `RateLimitError`da 1s, 2s, 4s kutib qayta urinish); (b) `jami_token` ma'lum chegaradan (masalan 50 000) oshsa, agentni majburan to'xtatib, xarajat limiti haqida xabar bering; (c) `fayl_yoz`ni sinab ko'ring — `../boshqa.txt` kabi yo'l bilan papkadan tashqariga yozishga urinib, himoya ishlashini tasdiqlang.

---

[⬅️ Oldingi: 27 — Kapston I: RAG chatbot](./27-kapston-rag-chatbot.md) · [🏠 Kitob boshi](./README.md)
