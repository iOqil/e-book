# 19 — 0 dan agent qurish

[⬅️ Oldingi: 18 — Agentlar va ReAct sikli](./18-agentlar-react.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 20 — Agent freymvorklari va MCP ➡️](./20-agent-freymvork-mcp.md)

> **Bu bobda:** hech qanday freymvorksiz, sof Python va OpenAI-mos tool calling bilan **boshidan oxirigacha ishlaydigan agent** quramiz. 11-bobdagi tool loopni olib, uni to'liq agentga aylantiramiz: **tool registry** (nom -> funksiya + ta'rif), **agent loop** (`while` — model chaqir, `tool_calls` bo'lsa bajar, takror, yakuniy javob bo'lsa to'xta), **xotira** (`messages` tarixi), aniq **to'xtash sharti** (yakuniy javob yoki `maks_qadam`) va **xavfsizlik chegaralari** (qadam limiti, xavfli tool uchun inson tasdig'i, argument validatsiya). Oxirida 3 ta tool (kalkulyator + soxta qidiruv + joriy vaqt) bilan **har qadamini chop etadigan** to'liq `Agent` klassni yozamiz va ishga tushiramiz.

---

## Muammodan boshlaymiz: loop bormi — agent bormi?

11-bobda biz juda kichik bir narsa yozdik — model tool chaqiradi, biz bajaramiz, natijani qaytaramiz, model davom etadi. 18-bobda buni **ReAct** (Reasoning + Acting) nuqtai nazaridan ko'rdik: agent o'ylaydi, harakat qiladi, kuzatadi va yana o'ylaydi. Endi savol: **shularning hammasini bitta toza, kengaytiriladigan kod**ga qanday jamlash mumkin?

Tasavvur qiling, sizdan "ishlaydigan agent ko'rsat" deyishdi. Siz LangChain yoki boshqa freymvork ochasizmi? Yo'q — avval **agent aslida nima ekanini** o'z qo'lingiz bilan qurib ko'rish kerak. Chunki freymvork ichida aynan shu loop ishlaydi; uni tushunmasangiz, biror narsa buzilganda nima qilishni bilmaysiz.

Yaxshi xabar: to'liq ishlaydigan agent — bu **sehr emas**, balki bir nechta oddiy qismdan iborat:

1. **Tool registry** — agent ishlatadigan funksiyalar va ularning ta'riflari.
2. **Xotira** — suhbat va tool natijalari tarixi (`messages`).
3. **Loop** — model chaqir, tool bajar, takror; yakuniy javobda to'xta.
4. **To'xtash sharti** — yakuniy javob yoki qadam limiti.
5. **Xavfsizlik chegaralari** — limit, tasdiq, validatsiya.

> **Hayotiy o'xshatish.** Agent — bu **yangi xodim** kabi: unga vazifa (savol) berasiz, qo'lida asboblar (tool) bor, daftari (xotira) bor; u o'zicha "shuni qilsam, keyin buni" deb ishlaydi va tugaganda hisobot beradi. Sizning ishingiz — unga to'g'ri asboblar berish, daftarini yuritish va **chegaralar qo'yish** (cheksiz ishlamasin, xavfli ishni so'ramay qilmasin).

!!! note "Freymvork keyin, asos avval"
    Bu bobda **maxsus kutubxona ishlatmaymiz** — faqat `openai` (yoki OpenAI-mos provayder) va Python standart kutubxonasi. Maqsad — agent yadrosini "ko'rinmas qutim" emas, o'zingiz tushunadigan 80 qatorlik kod qilish. 20-bobda tayyor freymvork va MCP'ni ko'rganda, ular aynan shu g'oyani qadoqlanganini anglaysiz.

---

## Agent loop: butun g'oyaning yuragi

Agentning yuragi — bir nechta qadam bo'lishi mumkin bo'lgan **`while` loop**. Har qadamda: modelni xotira (`messages`) va tool ro'yxati bilan chaqiramiz. Model ikki narsadan birini qaytaradi — **`tool_calls`** (men shu toolni ishlatmoqchiman) yoki **oddiy matn** (mana yakuniy javob).

- `tool_calls` bo'lsa: hammasini bajaramiz, natijalarni xotiraga qo'shamiz va **takror** loopga kiramiz — model endi natijalarni ko'rib davom etadi.
- Oddiy matn bo'lsa: bu **yakuniy javob**, loopni to'xtatamiz.

![Agent loopining blok-sxemasi: savol messages xotiraga qo'shiladi, model chaqiriladi, tool_calls bormi degan tekshiruv; ha bo'lsa toollar registry orqali bajarilib natija xotiraga qo'shiladi va sikl takrorlanadi, yo'q bo'lsa yakuniy javob qaytadi; qadam limiti cheksiz siklning oldini oladi va o'ng tomonda messages ro'yxati agent xotirasi sifatida o'sib boradi](rasmlar/aip19-loop.svg)

Diagrammadagi eng muhim ikki narsaga e'tibor bering: (1) **xotira** (`messages`) — har qadamda o'sadi, chunki yangi `assistant` va `tool` xabarlari qo'shiladi; (2) **qadam limiti** — model behad tool chaqiraversa ham loop cheksiz aylanmasligi uchun.

> **Hayotiy o'xshatish.** Loop — oshpaz bilan suhbat: siz "palov qil" deysiz; u "guruch bormi?" (tool) so'raydi, javob olasiz; u "go'sht qancha?" (yana tool) so'raydi; nihoyat "tayyor!" (yakuniy javob) deydi. Har savol oldingi javobga tayanadi — shuning uchun **qat'iy ikki qadam emas, sikl** kerak.

!!! warning "Cheksiz loop = bo'sh hisob"
    Limitsiz agent — eng qimmat xato. Model (yoki tool xatosi tufayli) doimo tool chaqiraversa, loop cheksiz ishlaydi va har aylanish — pulli API so'rovi. Doim `maks_qadam` qo'ying (odatda 6-10 yetarli) va limitga yetganda chiroyli to'xtang.

---

## Xotira: `messages` — agentning daftari

Agent "esini yo'qotmasligi" uchun butun suhbat va tool natijalari bitta ro'yxatda — `messages`da — saqlanadi. Har qadamda bu ro'yxat o'sadi:

- `system` — agentga "kimligini" va tool ishlatish qoidasini aytadi (boshda bir marta).
- `user` — foydalanuvchi savoli.
- `assistant` (`tool_calls` bilan) — model qaysi toolni so'raganini ko'rsatadi.
- `tool` — har bir tool natijasi (o'z `tool_call_id` bilan bog'langan).
- `assistant` (matn) — yakuniy javob.

Muhim: model **holatsiz** (stateless) — u oldingi qadamni faqat siz `messages`da qaytarib yuborganingiz uchun "eslaydi". Demak, xotirani **siz yuritasiz**. Tool chaqirilganda `assistant` xabarini (tool_calls bilan) va har bir `tool` natijasini ro'yxatga qo'shishni unutmang — aks holda model "javobsiz qoldi" deb xato beradi.

> **Hayotiy o'xshatish.** `messages` — agentning **daftari**. Model har gal daftarni boshidan o'qiydi (chunki o'zida hech narsa eslab qolmaydi), so'ng keyingi qatorni yozadi. Daftarga yozishni to'xtatsangiz — agent xotirasini yo'qotadi.

---

## Tool registry: nom -> funksiya + ta'rif

Modelga toollarni **ikki shaklda** taqdim etamiz, va bu farqni aniq tushunish kerak:

1. **Ta'riflar (`tools` ro'yxati)** — modelga *yuboriladi*. Model faqat shu ta'rifni (nom, `description`, `parameters` sxemasi) ko'radi — funksiya kodini ko'rmaydi.
2. **Registry (`{"nom": funksiya}` lug'ati)** — *sizda* qoladi. Model `"kalkulyator"` degan **matnli nom** qaytarganda, siz uni shu lug'atdan haqiqiy Python funksiyaga bog'laysiz.

![Tool registry diagrammasi: chap tomonda toollarning ta'riflari (name, description, parameters) modelga yuboriladi va model faqat shuni ko'radi; model matnli nom qaytaradi (kalkulyator); markazda agent REGISTRY lug'atidan o'sha nomni haqiqiy funksiyaga bog'laydi va funksiyani argumentlar bilan chaqiradi; natija JSON bo'lib xotiraga qaytadi; o'ng tomonda REGISTRY lug'ati nom dan funksiyaga moslik sifatida ko'rsatilgan](rasmlar/aip19-registry.svg)

Bu ajratish nima beradi? **Kengaytiriluvchanlik.** Yangi tool qo'shish = (a) bitta funksiya yozish, (b) `tools`ga bitta ta'rif qo'shish, (c) `REGISTRY`ga bitta yozuv qo'shish. Agent loopining **kodi hech qachon o'zgarmaydi** — u shunchaki "nomni registry'dan topib chaqir" deydi.

```python
import json
import datetime

# --- Tool funksiyalari (har biri DICT qaytaradi, xatoni ham natija sifatida) ---
def kalkulyator(ifoda: str) -> dict:
    """'2 + 3 * 4' kabi matematik ifodani XAVFSIZ hisoblaydi (ast, eval EMAS)."""
    import ast, operator
    amallar = {ast.Add: operator.add, ast.Sub: operator.sub,
               ast.Mult: operator.mul, ast.Div: operator.truediv,
               ast.Pow: operator.pow, ast.USub: operator.neg}

    def bahola(t):
        if isinstance(t, ast.Constant) and isinstance(t.value, (int, float)):
            return t.value
        if isinstance(t, ast.BinOp):
            return amallar[type(t.op)](bahola(t.left), bahola(t.right))
        if isinstance(t, ast.UnaryOp):
            return amallar[type(t.op)](bahola(t.operand))
        raise ValueError("ruxsat etilmagan ifoda")

    try:
        return {"natija": bahola(ast.parse(ifoda, mode="eval").body)}
    except Exception as e:
        return {"xato": f"hisoblab bo'lmadi: {e}"}

def qidir(sorov: str) -> dict:
    """Internetdan qidiruv (DEMO: soxta natija; real loyihada qidiruv API'si)."""
    soxta_baza = {
        "o'zbekiston poytaxti": "O'zbekiston poytaxti — Toshkent shahri.",
        "python yili": "Python birinchi marta 1991-yilda chiqarilgan.",
    }
    matn = soxta_baza.get(sorov.lower().strip(),
                          f"'{sorov}' bo'yicha aniq natija topilmadi.")
    return {"sorov": sorov, "natija": matn}

def joriy_vaqt() -> dict:
    """Hozirgi sana va vaqtni qaytaradi."""
    return {"vaqt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}

# --- REGISTRY: model qaytaradigan NOM -> haqiqiy funksiya ---
REGISTRY = {
    "kalkulyator": kalkulyator,
    "qidir": qidir,
    "joriy_vaqt": joriy_vaqt,
}
```

Endi modelga yuboriladigan **ta'riflar** ro'yxati. Har bir `description`ni aniq yozing — bu modelning "ko'zi", u qachon qaysi toolni ishlatishni shundan biladi:

```python
TOOLS = [
    {"type": "function", "function": {
        "name": "kalkulyator",
        "description": "Matematik ifodani aniq hisoblaydi. Hisob-kitob kerak bo'lganda ishlat.",
        "parameters": {"type": "object",
            "properties": {"ifoda": {"type": "string",
                "description": "Hisoblanadigan ifoda, masalan '125 * 8 + 7'"}},
            "required": ["ifoda"]}}},
    {"type": "function", "function": {
        "name": "qidir",
        "description": "Fakt yoki yangi ma'lumotni qidiradi. Modelda bilim yetmasa ishlat.",
        "parameters": {"type": "object",
            "properties": {"sorov": {"type": "string", "description": "Qidiruv so'rovi"}},
            "required": ["sorov"]}}},
    {"type": "function", "function": {
        "name": "joriy_vaqt",
        "description": "Hozirgi sana va vaqtni qaytaradi. Vaqt/sana so'ralganda ishlat.",
        "parameters": {"type": "object", "properties": {}}}},
]
```

> **Hayotiy o'xshatish.** Ta'riflar (`TOOLS`) — modelga berilgan **menyu**, registry — oshxonadagi **retseptlar**. Mijoz (model) menyudan taom nomini aytadi; oshxona (siz) shu nomga mos retseptni topib pishiradi. Mijoz oshxonaga kirmaydi — faqat nom aytadi.

!!! tip "Ikki ro'yxatni sinxron tut"
    `TOOLS` ta'rifidagi `name` va `REGISTRY` kalitlari **bir xil** yozilishi shart. `"kalkulyator"` vs `"kalkulator"` kabi imlo farqi — model toolni chaqiradi-yu, registry topa olmaydi. Kichik loyihada bitta joyda saqlash yoki test bilan tekshirish foydali.

---

## To'liq agent: `Agent` klass (boshidan oxirigacha)

Endi hamma qismni bitta klassga jamlaymiz. Bu klass: xotirani yuritadi, loopni aylantiradi, har qadamni **chop etadi** (trace), qadam limitini hisoblaydi va xavfli toolda **tasdiq so'raydi**. Bu — to'liq ishlaydigan, freymvorksiz agent.

```python
import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()             # OpenAI-mos: base_url + kalitni almashtirsangiz boshqa provayder
MODEL = "gpt-5.4-mini"        # Eslatma: model nomlari o'zgaradi — provayder ro'yxatini tekshiring

# Inson tasdig'i talab qiladigan "xavfli" toollar (bizning demoda yo'q, lekin namuna)
XAVFLI_TOOLLAR = {"fayl_ochir", "tolov_yubor", "email_yubor"}


class Agent:
    def __init__(self, registry, tools, model=MODEL, maks_qadam=8):
        self.registry = registry
        self.tools = tools
        self.model = model
        self.maks_qadam = maks_qadam      # XAVFSIZLIK: qadam limiti

    def _tool_bajar(self, tool_call) -> str:
        """Bitta tool_call'ni xavfsiz bajaradi, natijani JSON-matn qaytaradi."""
        nom = tool_call.function.name
        try:
            args = json.loads(tool_call.function.arguments or "{}")
        except json.JSONDecodeError:
            return json.dumps({"xato": "argumentlar JSON emas"}, ensure_ascii=False)

        funksiya = self.registry.get(nom)
        if funksiya is None:
            return json.dumps({"xato": f"noma'lum tool: {nom}"}, ensure_ascii=False)

        # XAVFSIZLIK: xavfli tool uchun inson tasdig'i (human-in-the-loop)
        if nom in XAVFLI_TOOLLAR:
            javob = input(f"  [tasdiq] '{nom}' ni {args} bilan bajaraymi? (ha/yo'q): ")
            if javob.strip().lower() not in {"ha", "h", "y", "yes"}:
                return json.dumps({"xato": "foydalanuvchi rad etdi"}, ensure_ascii=False)

        try:
            natija = funksiya(**args)            # XAVFSIZLIK: **args — validatsiya tool ichida
        except TypeError as e:
            natija = {"xato": f"noto'g'ri argumentlar: {e}"}
        except Exception as e:
            natija = {"xato": str(e)}            # exception emas, NATIJA qaytaramiz
        return json.dumps(natija, ensure_ascii=False)

    def ishlat(self, savol: str) -> str:
        # XOTIRA: butun suhbat va tool natijalari shu ro'yxatda
        messages = [
            {"role": "system", "content":
                "Sen foydali yordamchisan. Kerak bo'lganda toollardan foydalan. "
                "Hisob-kitobni kalkulyatorga, faktni qidiruvga topshir."},
            {"role": "user", "content": savol},
        ]

        for qadam in range(1, self.maks_qadam + 1):     # TO'XTASH: qadam limiti
            print(f"\n--- {qadam}-qadam ---")
            resp = client.chat.completions.create(
                model=self.model, messages=messages, tools=self.tools,
            )
            msg = resp.choices[0].message

            # TO'XTASH SHARTI 1: tool chaqirilmadi -> yakuniy javob
            if not msg.tool_calls:
                print("  [yakun] model matn qaytardi")
                return msg.content

            # Aks holda: barcha tool_call'larni bajaramiz (parallel bo'lishi mumkin)
            messages.append(msg)                         # assistant navbati (tool_calls bilan)
            for tc in msg.tool_calls:
                print(f"  [tool] {tc.function.name}({tc.function.arguments})")
                natija = self._tool_bajar(tc)
                print(f"  [natija] {natija}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,               # qaysi chaqiruvga javob ekanini bog'laydi
                    "content": natija,
                })
            # Sikl boshiga qaytadi -> model natijalarni ko'rib davom etadi

        # TO'XTASH SHARTI 2: qadam limiti tugadi
        return "Kechirasiz, qadam limiti tugadi — vazifani yakunlay olmadim."
```

Mana shu — to'liq agent. E'tibor bering: bu kod **11-bobdagi loopning aniq davomi**, lekin endi (a) klass ichida tartibli, (b) har qadamni chop etadi (trace), (c) xavfli tool uchun tasdiq so'raydi, (d) argument xatosini ham natija sifatida qaytaradi.

> **Hayotiy o'xshatish.** `Agent` klass — yangi xodimning **ish tartibi qog'ozi**: "savolni oling, kerakli asbobni tanlang, ishni bajaring, hisobotni daftarga yozing, takrorlang; xavfli ishdan oldin so'rang; sakkiz qadamdan oshmang". Qog'oz bir marta yoziladi, har vazifaga ishlaydi.

---

## Ishga tushirish va trace

Endi agentni jonlantiramiz. `ishlat` har qadamni chop etgani uchun, agent qanday "fikrlayotganini" o'z ko'zingiz bilan ko'rasiz:

```python
if __name__ == "__main__":
    agent = Agent(REGISTRY, TOOLS, maks_qadam=8)
    javob = agent.ishlat(
        "Hozir soat necha, va 125 * 8 + 17 necha bo'ladi? O'zbekiston poytaxti qaysi shahar?"
    )
    print("\n=== YAKUNIY JAVOB ===")
    print(javob)
```

Taxminiy chiqish (trace) shunday ko'rinadi — model bir qadamda **uchta** toolni parallel chaqiradi, natijalarni oladi va keyingi qadamda hammasini matnga jamlaydi:

```text
--- 1-qadam ---
  [tool] joriy_vaqt({})
  [natija] {"vaqt": "2026-06-15 14:30"}
  [tool] kalkulyator({"ifoda": "125 * 8 + 17"})
  [natija] {"natija": 1017}
  [tool] qidir({"sorov": "O'zbekiston poytaxti"})
  [natija] {"sorov": "O'zbekiston poytaxti", "natija": "O'zbekiston poytaxti — Toshkent shahri."}

--- 2-qadam ---
  [yakun] model matn qaytardi

=== YAKUNIY JAVOB ===
Hozir soat 14:30. 125 * 8 + 17 = 1017. O'zbekiston poytaxti — Toshkent shahri.
```

Mana sehrning butun siri: model **o'zi** qaysi toolni, qaysi argument bilan chaqirishni hal qildi; biz faqat toollarni berdik va loopni aylantirdik. Trace tufayli har qadam ko'rinib turibdi — bu **debug** (xatoni topish) uchun bebaho.

!!! tip "Trace — agentni tushunishning kaliti"
    Agent "g'alati" javob berganda, birinchi qaraydigan joy — trace. Model qaysi toolni chaqirdi? Argumentlar to'g'rimi? Tool nima qaytardi? Ko'pincha muammo — yomon `description` (model noto'g'ri tool tanlaydi) yoki tool natijasi (xato qaytaradi). Trace bularning hammasini ko'rsatadi. Production'da `print` o'rniga `logging` ishlating (25-bobda kuzatuvni ko'ramiz).

---

## To'xtash sharti: agent qachon to'xtaydi

Agentning eng nozik qismi — **qachon to'xtash**. Ikki yo'l bor va ikkalasi ham kerak:

1. **Yakuniy javob (normal to'xtash).** Model `tool_calls` qaytarmasa — demak, u tugatdi va matn javob berdi. Bu — kutilgan, sog'lom yakun. Kodda: `if not msg.tool_calls: return msg.content`.
2. **Qadam limiti (himoya to'xtash).** Model behad tool chaqiraversa (masalan, tool doimo xato qaytarsa va model qayta-qayta urinaversa), `maks_qadam`ga yetganda **majburan** to'xtaymiz. Kodda: `for qadam in range(1, self.maks_qadam + 1)` tugagach, "limit tugadi" deb qaytaramiz.

> **Hayotiy o'xshatish.** Yakuniy javob — xodim "ish tayyor" deyishi; qadam limiti — "soat 18:00 bo'ldi, uyga ketamiz" qoidasi. Birinchisi — ideal, lekin ish cho'zilib ketsa, ikkinchisi (qattiq chegara) sizni cheksiz mehnat (va xarajat)dan saqlaydi.

!!! warning "Limitsiz agent — vaqt bombasi"
    Hech qachon `while True:` bilan limitsiz agent yozmang. Bitta noto'g'ri tool (har safar `{"xato": ...}` qaytaradigan) modelni cheksiz qayta urinishga undashi mumkin. `maks_qadam` — sizning "to'xta!" tugmangiz. Limitga yetilganda foydalanuvchiga ochiq xabar bering, jim qotib qolmang.

---

## Xavfsizlik chegaralari: agentni jilovlash

Agent — **harakat qiladigan** dastur: u sizning kodingizni (toollarni) ishga tushiradi va argumentlarni **model to'qiydi**. Bu kuchli, lekin xavfli. Uchta chegara har bir jiddiy agentda bo'lishi shart:

![Agent xavfsizlik chegaralarining diagrammasi: yuqorida uch quti — qadam limiti (cheksiz loopdan himoya), inson tasdig'i (xavfli tool oldidan ha yo'q so'raydi), argument validatsiya (model argumentlari ishonchsiz kirish, turini va chegarani tekshir); pastda oqim: tool_call darvozaga keladi, xavfsizmi degan tekshiruvdan o'tsa bajariladi va natija xotiraga qaytadi, rad etilsa yoki tasdiq bo'lmasa xato natija qaytadi](rasmlar/aip19-limit.svg)

**1. Qadam limiti** — yuqorida ko'rdik: `maks_qadam` cheksiz loopni to'xtatadi.

**2. Inson tasdig'i (human-in-the-loop)** — xavfli, qaytarib bo'lmaydigan amallar uchun. Faylni o'chirish, pul o'tkazish, email yuborish kabi toollarni model **so'ramay** bajarmasin. Bizning kodda `XAVFLI_TOOLLAR` to'plamiga kirgan tool oldidan `input()` bilan tasdiq so'raladi:

```python
if nom in XAVFLI_TOOLLAR:
    javob = input(f"  [tasdiq] '{nom}' ni {args} bilan bajaraymi? (ha/yo'q): ")
    if javob.strip().lower() not in {"ha", "h", "y", "yes"}:
        return json.dumps({"xato": "foydalanuvchi rad etdi"}, ensure_ascii=False)
```

Tasdiq berilmasa, tool **bajarilmaydi** va modelga `{"xato": "foydalanuvchi rad etdi"}` qaytadi — model buni ko'rib, boshqa yo'l tutadi yoki foydalanuvchiga tushuntiradi.

**3. Argument validatsiya** — model `arguments`ni o'zi yozadi, demak ular **ishonchsiz kirish** (untrusted input), xuddi foydalanuvchi formasidek. Bajarishdan oldin tekshiring: turi to'g'rimi, chegarada-mi, ruxsat etilgan qiymatmi. Validatsiyaning bir qismi `_tool_bajar` ichida (`TypeError`ni ushlash), bir qismi tool ichida (masalan, `kalkulyator` faqat oq ro'yxatdagi amallarni bajaradi):

```python
def tolov_yubor(summa: float, qabul_qiluvchi: str) -> dict:
    if not isinstance(summa, (int, float)) or summa <= 0:
        return {"xato": "summa musbat son bo'lishi kerak"}
    if summa > 1_000_000:                       # chegara: katta to'lovni rad et
        return {"xato": "summa chegaradan oshdi (inson nazorati kerak)"}
    # ... haqiqiy to'lov mantig'i
    return {"holat": "yuborildi", "summa": summa}
```

> **Hayotiy o'xshatish.** Bu uch chegara — yangi xodimga beriladigan **ruxsat darajalari** kabi: u o'zi ko'p ishni qila oladi (qadam limiti ichida), lekin katta pul o'tkazishdan oldin rahbardan so'raydi (tasdiq), va har qog'ozni imzolashdan oldin tekshiradi (validatsiya). Ishonch — nazorat bilan birga keladi.

!!! warning "eval / exec / os.system — tool ichida HECH QACHON"
    Model to'qigan matnni `eval()`, `exec()` yoki `os.system()`ga to'g'ridan-to'g'ri uzatish — eng xavfli xato. Shuning uchun `kalkulyator` `eval` emas, `ast` + oq ro'yxat ishlatadi (11-bob). Fayl toolida — yo'lni tekshiring (path traversal), DB toolida — parametrli so'rov (SQL injection). Xavfsizlikni 24-bobda chuqur ko'ramiz.

---

## Boshqa provayder: bir xil agent

Butun bu kod **OpenAI-mos** — ya'ni faqat `client`ni almashtirib, agentni Groq, DeepSeek yoki lokal Ollama'da ishlatasiz. Loop, registry, xotira — hammasi o'zgarmaydi:

```python
# Groq (bepul, tez) — qolgan barcha kod (Agent klass, REGISTRY, TOOLS) AYNI
client = OpenAI(base_url="https://api.groq.com/openai/v1",
                api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"
```

**Claude** va **Gemini**ning tool formati biroz farq qiladi (Claude'da natija `user` navbatida `tool_result` blok bilan qaytadi), lekin **g'oya bir xil**: ta'rif ber, model tool so'raydi, bajar, qaytar, loopda davom et. Agentning butun arxitekturasi — provayderdan mustaqil.

!!! note "Model nomlari o'zgaradi"
    Bu bobdagi `gpt-5.4-mini`, `llama-3.3-70b-versatile` kabi nomlar — yozilish paytidagi holat. Nomlar tez yangilanadi; loyiha boshlashdan oldin **provayderning joriy model ro'yxatini** tekshiring. Agent g'oyasi esa o'zgarmaydi.

---

## Xulosa

- **Agent = loop + xotira + tool registry + to'xtash sharti + chegaralar.** Bu sehr emas — freymvorksiz, ~80 qatorda quriladi.
- **Agent loop** — `while`/`for`: modelni xotira va toollar bilan chaqir; `tool_calls` bo'lsa hammasini bajarib natijani xotiraga qo'sh va **takror**; oddiy matn bo'lsa — bu yakuniy javob, to'xta.
- **Xotira** (`messages`) — agentning daftari. Model holatsiz, shuning uchun butun tarixni (`system`, `user`, `assistant` tool_calls bilan, `tool` natijalari) **siz yuritasiz**.
- **Tool registry** ikki qismdan: modelga yuboriladigan **ta'riflar** (`TOOLS`) va sizda qoladigan **funksiya lug'ati** (`REGISTRY`). Nomlar bir xil bo'lsin. Yangi tool = funksiya + ta'rif + registry yozuvi; loop kodi o'zgarmaydi.
- **To'xtash sharti** ikkita: yakuniy javob (`tool_calls` yo'q — normal) va **qadam limiti** (`maks_qadam` — himoya). Ikkalasi ham kerak.
- **Trace** (har qadamni chop etish) — agentni tushunish va debug qilishning kaliti: qaysi tool, qaysi argument, qanday natija ko'rinadi.
- **Xavfsizlik chegaralari** uchta: (1) qadam limiti — cheksiz loopdan; (2) inson tasdig'i — xavfli/qaytarilmas toollar uchun; (3) argument validatsiya — model argumentlari ishonchsiz kirish, doim tekshir. `eval`/`exec`/`os.system` — tool ichida hech qachon.
- Agent **OpenAI-mos** — `client`ni almashtirib boshqa provayderda ishlatasiz; Claude/Gemini formati farq qiladi, g'oya bir xil.

## Amaliy mashqlar

1. **(Oson)** Bobdagi `Agent` klassni, 3 ta tool va `REGISTRY`/`TOOLS`ni tering. "Soat necha?" deb so'rang va trace'da faqat `joriy_vaqt` chaqirilganini, keyingi qadamda yakuniy matn kelganini kuzating.

2. **(Oson)** Yangi tool qo'shing: `harf_sanagich(matn)` — matndagi harflar sonini qaytarsin. Uni `REGISTRY` va `TOOLS`ga qo'shing (loop kodiga **tegmang**) va "'salom dunyo' so'zida nechta harf bor?" deb so'rang. Agent uni o'zi chaqirganini ko'ring.

3. **(O'rtacha)** `maks_qadam=1` qilib agentni ishga tushiring va modeldan tool talab qiladigan murakkab savol bering ("Toshkent va Samarqand aholisini qo'shsang qancha?"). Limit tugaganda agent qaysi xabarni qaytarganini va nega bir qadamda yakunlay olmaganini tushuntiring.

4. **(O'rtacha)** `XAVFLI_TOOLLAR`ga `fayl_ochir` toolini qo'shing (faqat fayl nomini chop etadigan demo funksiya yozing). Agentdan shu toolni chaqirtiring va `input()` so'rovida bir marta "yo'q", bir marta "ha" javob bering. Har ikki holatda modelga qanday natija qaytganini va u keyin nima qilganini kuzating.

5. **(Qiyin)** Argument validatsiyani sinab ko'ring: `kalkulyator`ga atayin xavfli ifoda (`__import__('os').system('echo x')`) yuboradigan savol bering. Tool uni rad etganini (`{"xato": ...}`) va agent buni qanday tushuntirganini trace'da ko'ring. So'ng `_tool_bajar`ga **umumiy** vaqt o'lchagich (`time.perf_counter`) qo'shib, har tool necha soniya ishlaganini trace'ga chiqaring.

---

[⬅️ Oldingi: 18 — Agentlar va ReAct sikli](./18-agentlar-react.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 20 — Agent freymvorklari va MCP ➡️](./20-agent-freymvork-mcp.md)
