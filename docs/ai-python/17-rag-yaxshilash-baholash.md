# 17 — RAG'ni yaxshilash va baholash

[⬅️ Oldingi: 16 — RAG: retrieval va generatsiya](./16-rag-retrieval-generatsiya.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 18 — Agentlar va ReAct sikli ➡️](./18-agentlar-react.md)

> **Bu bobda:** 16-bobdagi oddiy (naive) RAG nega ko'pincha yetarli emasligini ko'ramiz — noto'g'ri chunk topiladi, ko'p shovqin keladi, savol so'zlari hujjat so'zlariga mos kelmaydi. So'ng RAG sifatini oshiruvchi to'rt asosiy texnikani o'rganamiz: **re-ranking** (ko'p nomzod olib, eng tegishlilarini qayta tartiblash), **hybrid search** (kalit so'z + vektor qidiruvni birlashtirish), **query expansion/rewriting** (savolni LLM bilan yaxshilash, multi-query) va **metadata filtering** (qidiruvni sana/bo'lim bilan toraytirish). Oxirida eng muhim ko'nikma — **baholash (evaluation)**: retrieval sifatini (kerakli chunk topildimi) va javob sifatini o'lchash, **LLM-as-judge** bilan avtomatik baholash, kichik test to'plami tuzish va `chunk` o'lchami/`top_k`ni shu o'lchov asosida sozlash.

---

## Muammodan boshlaymiz: naive RAG ko'pincha "deyarli to'g'ri"

16-bobda ishlaydigan RAG qurdik: savolni embeddingga aylantirdik, vektor bazadan eng yaqin `top_k` chunkni oldik, ularni modelga kontekst qilib berdik. Demoda ajoyib ishladi. Lekin haqiqiy, kattaroq bazada uni ishga tushirsangiz, tez-tez shunday holatlar ko'rasiz:

- Foydalanuvchi **"504 xato"** deb so'raydi, lekin hujjatda u **"gateway timeout"** deb yozilgan — semantik o'xshashlik past chiqib, kerakli chunk topilmaydi.
- `top_k=3` olganingizda kerakli javob aslida **5-o'rinda** edi — modelga yetib bormadi.
- Topilgan 3 chunkdan faqat bittasi tegishli, qolgan ikkitasi **shovqin** — model shovqindan chalg'ib, noaniq javob beradi.
- Savol bir nechta mavzuga tegishli ("narx **va** yetkazib berish"), lekin yagona qidiruv ikkalasini ham qamrab ololmaydi.

Mana shu — naive RAG'ning "shisha shipi": yarmi ishlaydi, lekin ishonchli production tizim uchun yetmaydi.

![Oddiy RAG va yaxshilangan RAG taqqoslashi: chap tomonda naive RAG shovqin va noto'g'ri chunklar bilan noaniq javob beradi; o'ng tomonda hybrid + re-rank ishlatgan RAG aniq, manbaga asoslangan javob beradi; bir xil model va baza, farq faqat kontekst sifatida](rasmlar/aip17-naive-vs-yaxshi.svg)

> **Hayotiy o'xshatish.** Naive RAG — kutubxonaga kirib, javonlardan tasodifan uchta kitob olib chiqishdek. Ba'zan kerakli kitob tushadi, ba'zan yo'q. Yaxshilangan RAG esa — avval ko'proq kitob (top-20) tortib olib, keyin ularni varaqlab eng mosini tanlaydigan tajribali kutubxonachidek: ko'p oladi, lekin aniq beradi.

!!! note "Asosiy haqiqat: yaxshi javob = yaxshi retrieval"
    RAG javobi qanchalik yaxshi bo'lsa, modelga **berilgan kontekst** shunchalik yaxshi. Agar kerakli chunk umuman topilmasa, dunyodagi eng kuchli model ham to'g'ri javob bera olmaydi — chunki javob unga **berilmagan**. Shuning uchun bu bobning aksariyati "modelni emas, **retrieval**ni yaxshilash" haqida.

---

## Re-ranking: ko'p ol, keyin aniq tanla

Birinchi va eng samarali yaxshilanish — **re-ranking**. G'oya juda sodda:

1. Vektor qidiruvdan **ko'proq** nomzod oling — `top_k=3` o'rniga, masalan, `top_k=20`.
2. So'ng **re-ranker** bilan bu 20 ta nomzodni savolga tegishliligi bo'yicha **qayta tartiblang** va eng yaxshi 3-5 tasini oling.

Nega bu ishlaydi? Vektor qidiruv **tez** lekin **taxminiy** — u savol va chunkni alohida-alohida vektorga aylantirib, masofani o'lchaydi. **Re-ranker** esa savol va chunkni **birga** o'qib, "bu chunk shu savolga qanchalik javob beradi?" degan aniqroq baho beradi. U sekinroq, shuning uchun butun bazaga emas, faqat 20 ta nomzodga qo'llanadi.

![Re-ranking jarayoni: avval vektor qidiruv tez ravishda 20 ta nomzod chunk qaytaradi (aralash sifat), keyin cross-encoder re-ranker har bir nomzodni savol bilan birga o'qib tegishlilik bahosi beradi va qayta tartiblaydi, natijada eng yaxshi top-3 modelga uzatiladi](rasmlar/aip17-rerank.svg)

> **Hayotiy o'xshatish.** Vektor qidiruv — tez ishlaydigan **elak**: u ko'p arizadan tezda 20 tasini saralab oladi, lekin chuqur o'qimaydi. Re-ranker — bu 20 ta arizani **diqqat bilan o'qiydigan komissiya**: u sekinroq, ammo ancha aniq. Butun bazani (minglab ariza) komissiyaga o'tkazib bo'lmaydi — shuning uchun avval elak, keyin komissiya.

Eng oson re-ranker — **cross-encoder** modeli (lokal, bepul). `sentence-transformers` orqali:

```python
from sentence_transformers import CrossEncoder

# Re-ranker modeli (lokal yuklanadi, internet faqat birinchi marta kerak)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def qayta_tartibla(savol: str, chunklar: list[str], top: int = 3) -> list[str]:
    """Nomzod chunklarni savolga tegishliligi bo'yicha qayta tartiblaydi."""
    # Re-ranker (savol, chunk) juftliklariga ball beradi
    juftlar = [(savol, ch) for ch in chunklar]
    ballar = reranker.predict(juftlar)            # har chunk uchun tegishlilik bali
    # Balga qarab kamayuvchi tartibda saralaymiz
    tartibli = sorted(zip(chunklar, ballar), key=lambda x: x[1], reverse=True)
    return [ch for ch, ball in tartibli[:top]]    # eng yaxshi `top` tasi
```

Endi RAG oqimini yangilaymiz: ko'p ol -> qayta tartibla -> kontekst qil:

```python
# 1) Vektor qidiruvdan KO'P nomzod (16-bobdagi qidiruv funksiyasi)
nomzodlar = vektor_qidiruv(savol, top_k=20)        # 3 emas, 20

# 2) Re-ranker bilan eng yaxshi 3 tasini tanlaymiz
eng_yaxshi = qayta_tartibla(savol, nomzodlar, top=3)

# 3) Faqat shu 3 ta toza chunkni modelga kontekst qilamiz
kontekst = "\n\n".join(eng_yaxshi)
```

Agar lokal model o'rnatishni xohlamasangiz, **LLM-reranker** ham bor: LLM'dan har bir chunkka 0-10 ball berishni yoki nomzodlarni tartiblashni so'raysiz. U kuchli, lekin sekinroq va pulli (har chunk uchun so'rov). Cross-encoder odatda yaxshiroq narx/sifat beradi.

!!! tip "Re-ranking — eng katta foyda/mehnat nisbati"
    Agar RAG'ingizda bitta narsani yaxshilashga vaqtingiz bo'lsa — **re-ranking** qiling. U odatda eng katta sifat sakrashini beradi: `top_k`ni 20 ga ko'tarib (recall oshadi), keyin re-ranker bilan 3 ga qisqartirasiz (precision oshadi). Ikkala metrik ham yuqori bo'ladi.

---

## Hybrid search: kalit so'z + semantikni birlashtirish

Vektor qidiruv **ma'noni** tushunadi, lekin **aniq so'z**larda zaif. "iPhone 15 Pro" yoki "ERR_504" yoki mahsulot artikuli kabi aniq atamalarni qidirganda, kichik harf farqi yoki noyob so'z semantik o'xshashlikda yo'qolib ketishi mumkin. Bunday holatda eski, sinovdan o'tgan **kalit so'z (keyword) qidiruvi** — **BM25** — kuchliroq.

Yechim — ikkalasini **birlashtirish**, ya'ni **hybrid search**:

- **BM25 (kalit so'z)** — aniq so'z mosligi. Kod, ID, nom, noyob atama uchun zo'r; sinonim/ma'noda zaif.
- **Vektor (semantik)** — ma'no yaqinligi. Sinonim, qayta ifodalash uchun zo'r; aniq kod/ID'da zaif.

Har biri ikkinchisining zaif tomonini qoplaydi.

![Hybrid search diagrammasi: foydalanuvchi savoli ham kalit so'z (BM25) qidiruviga, ham vektor (semantik) qidiruviga yuboriladi; BM25 aniq so'z mosligida kuchli lekin sinonimda zaif, vektor ma'noda kuchli lekin aniq kodda zaif; ikki natija ro'yxati RRF yoki ball bilan birlashtirilib bitta yaxshi top-k hosil qilinadi](rasmlar/aip17-hybrid.svg)

> **Hayotiy o'xshatish.** BM25 — so'zma-so'z eshitadigan kotib: "504 deysizmi? Mana 504 yozilgan hujjatlar." Vektor qidiruv — ma'noni tushunadigan maslahatchi: "504 — bu timeout, mana 'sahifa ochilmayapti' haqidagi hujjatlar." Ishonchli javob uchun ikkalasiga ham quloq solasiz.

Ikki ro'yxatni qanday birlashtirish kerak? Eng oddiy va mustahkam usul — **Reciprocal Rank Fusion (RRF)**: har bir hujjat uchun har ro'yxatdagi **o'rni** (rank) bo'yicha ball beriladi va qo'shiladi. Bu ballarni normallashtirish bilan ovora bo'lmaydi — faqat tartibga tayanadi.

```python
def rrf_birlashtir(rolxatlar: list[list[str]], k: int = 60, top: int = 5) -> list[str]:
    """Bir nechta tartiblangan ro'yxatni RRF bilan bitta ro'yxatga birlashtiradi.
    rolxatlar — har biri eng yaxshidan eng yomonga tartiblangan chunk-id ro'yxati."""
    ball = {}
    for rolxat in rolxatlar:
        for orin, hujjat in enumerate(rolxat):       # orin: 0, 1, 2, ...
            # Yuqori o'rin -> katta ball (1/(k+orin)); k tekislaydi
            ball[hujjat] = ball.get(hujjat, 0) + 1 / (k + orin)
    # Umumiy ball bo'yicha kamayuvchi tartib
    tartibli = sorted(ball.items(), key=lambda x: x[1], reverse=True)
    return [hujjat for hujjat, b in tartibli[:top]]

# Ishlatish: BM25 va vektor natijalarini birlashtiramiz
bm25_natija = bm25_qidiruv(savol, top_k=20)       # kalit so'z ro'yxati
vektor_natija = vektor_qidiruv(savol, top_k=20)   # semantik ro'yxati
birlashgan = rrf_birlashtir([bm25_natija, vektor_natija], top=5)
```

BM25 uchun Python'da `rank_bm25` kutubxonasi eng oddiy yo'l:

```python
from rank_bm25 import BM25Okapi

# Korpus — har chunk so'zlarga ajratilgan (oddiy tokenizatsiya)
korpus = [chunk.lower().split() for chunk in barcha_chunklar]
bm25 = BM25Okapi(korpus)

def bm25_qidiruv(savol: str, top_k: int = 20) -> list[str]:
    ballar = bm25.get_scores(savol.lower().split())
    # Eng yuqori balli `top_k` chunk indekslarini olamiz
    indekslar = sorted(range(len(ballar)), key=lambda i: ballar[i], reverse=True)[:top_k]
    return [barcha_chunklar[i] for i in indekslar]
```

!!! note "Hybrid ko'pincha bazaning o'zida bor"
    Ko'p vektor bazalar (Qdrant, Weaviate, pgvector + Postgres FTS, Elasticsearch) **hybrid qidiruvni o'zi** qo'llab-quvvatlaydi — siz faqat parametrni yoqasiz. Qo'lda BM25 + vektor + RRF yozish — g'oyani tushunish va kichik loyihalar uchun; production'da bazaning tayyor hybrid imkonidan foydalaning.

!!! tip "Hybrid + re-rank = kuchli juftlik"
    Eng yaxshi natija odatda ikkisini birga ishlatishdan keladi: **hybrid** bilan keng (BM25 + vektor) nomzod yig'ing, keyin **re-ranker** bilan eng yaxshilarini tanlang. Hybrid — qamrovni (recall), re-rank — aniqlikni (precision) ko'taradi.

---

## Query expansion va rewriting: savolni yaxshilash

Ba'zan muammo retrieval'da emas, **savolning o'zida**. Foydalanuvchi qisqa, noaniq yoki suhbat kontekstiga bog'liq yozadi:

- "U qancha turadi?" — "u" nima? Oldingi xabarga bog'liq.
- "telfon urishmiyapti" — imlo xato, qisqa.
- "narx" — bitta so'z, juda umumiy.

Bunday savolni to'g'ridan-to'g'ri qidirsa, natija yomon bo'ladi. **Query rewriting** — savolni qidiruvdan **oldin** LLM bilan to'liq, aniq shaklga keltirish:

```python
def savolni_qayta_yoz(savol: str, suhbat_tarixi: str = "") -> str:
    """Foydalanuvchi savolini qidiruv uchun aniq, mustaqil shaklga keltiradi."""
    yoriqnoma = (
        "Quyidagi foydalanuvchi savolini hujjat bazasidan qidirish uchun "
        "aniq, mustaqil (kontekstsiz tushunarli) savolga aylantir. "
        "Olmoshlarni (u, bu, o'sha) suhbat tarixiga qarab aniq nom bilan almashtir. "
        "Faqat qayta yozilgan savolni qaytar, boshqa hech narsa yozma."
    )
    javob = client.chat.completions.create(
        model="gpt-5.4-mini",                       # nomlar o'zgaradi — ro'yxatni tekshiring
        messages=[
            {"role": "system", "content": yoriqnoma},
            {"role": "user", "content": f"Suhbat:\n{suhbat_tarixi}\n\nSavol: {savol}"},
        ],
    )
    return javob.choices[0].message.content.strip()

# "U qancha turadi?" + tarix -> "iPhone 15 Pro narxi qancha?"
toza_savol = savolni_qayta_yoz(savol, suhbat_tarixi)
chunklar = vektor_qidiruv(toza_savol, top_k=20)
```

**Query expansion / multi-query** — bir savoldan **bir nechta** variant yaratib, har biri bilan alohida qidirish va natijalarni birlashtirish. Bu turli so'z tanloviga ega chunklarni ham qamrab oladi:

```python
def kop_savol_yarat(savol: str, n: int = 3) -> list[str]:
    """Bitta savoldan n ta turli ifodalangan variant yaratadi (multi-query)."""
    yoriqnoma = (
        f"Quyidagi savolni qidiruv uchun {n} xil so'z bilan qayta ifodala. "
        "Har birini yangi qatorda, raqamsiz yoz."
    )
    javob = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": yoriqnoma},
            {"role": "user", "content": savol},
        ],
    )
    variantlar = [s.strip() for s in javob.choices[0].message.content.split("\n") if s.strip()]
    return [savol] + variantlar                     # asl savol ham qoladi

# Har variant bilan qidirib, natijalarni RRF bilan birlashtiramiz
rolxatlar = [vektor_qidiruv(v, top_k=10) for v in kop_savol_yarat(savol)]
birlashgan = rrf_birlashtir(rolxatlar, top=5)
```

> **Hayotiy o'xshatish.** Multi-query — bir savolni uch xil qilib so'rashdek: "narxi qancha?", "qancha turadi?", "qiymati nima?". Kimdir hujjatda biror ifodani ishlatgan bo'lsa, uchta variantdan biri unga tegadi. Bitta savol — bitta urinish; uch savol — uch baravar ko'p imkon.

!!! warning "Har qo'shimcha LLM chaqiruvi — narx va kechikish"
    Query rewriting va multi-query har savol uchun **qo'shimcha LLM so'rovi** qiladi — bu pul va kechikish (latency) qo'shadi. Ularni hamma joyda emas, **kerak bo'lganda** ishlating: rewriting — suhbatli chatbotda (olmoshlar ko'p), multi-query — qidiruv sifati past bo'lgan murakkab savollarda. Oddiy, aniq savollarga ortiqcha.

---

## Metadata filtering: qidiruvni toraytirish

Ko'pincha chunkda nafaqat matn, balki **metadata** ham bo'ladi: sana, bo'lim, til, manba fayl, muallif, kategoriya. Agar savol "shu yilgi narx siyosati" haqida bo'lsa, butun tarixiy hujjatlardan emas, faqat **2026-yilgi** chunklardan qidirish mantiqiy. Bu **metadata filtering** — semantik qidiruvni **oldindan** toraytirish.

16-bobda chunklarga metadata qo'shgan edingiz; endi qidiruvda undan foydalanamiz. Vektor bazalar buni `filter`/`where` parametri orqali beradi (misol Chroma uslubida):

```python
# Faqat 2026-yilgi, "narx" bo'limidagi chunklar ichidan qidiramiz
natija = kolleksiya.query(
    query_texts=[savol],
    n_results=20,
    where={                                   # metadata filtri
        "$and": [
            {"yil": {"$eq": 2026}},
            {"bolim": {"$eq": "narx"}},
        ]
    },
)
```

Filtr **qidiruv maydonini kichraytiradi** — bu ham aniqlikni (tegishsiz davr/bo'lim chiqib ketadi), ham tezlikni oshiradi. Filtrlash uchun metadatani chunk yaratishda **to'g'ri va izchil** yozish kerak (`yil: 2026`, `"2026"` emas — tip mosligiga e'tibor bering).

> **Hayotiy o'xshatish.** Metadata filtri — kutubxonada "faqat 2026-yil, iqtisod bo'limi" deb javonni oldindan chegaralashdek. Kutubxonachi (qidiruv) endi butun binoni emas, bitta javonni ko'zdan kechiradi — tez va aniq.

!!! tip "Filtr + semantik — qattiq va yumshoq mezon birga"
    Metadata filtri — **qattiq** (mantiqiy: shu sana, shu bo'lim — yoki ha, yoki yo'q). Semantik qidiruv — **yumshoq** (o'xshashlik darajasi). Ikkalasini birga ishlating: filtr keraksiz hududni kesadi, semantik qolgan ichidan eng mosini topadi. "Manbasi rasmiy hujjat bo'lgan, 2026-yilgi, savolga eng yaqin chunk" — kuchli kombinatsiya.

---

## Baholash (evaluation): "yaxshilandimi?"ni o'lchash

Yuqorida to'rt texnikani ko'rdik. Lekin **qaysi biri sizning bazangizda chindan yordam berdi?** "Menimcha yaxshilandi" — yetarli emas. Professional RAG'ning belgisi — **o'lchash**. Baholashsiz har o'zgartirish — qorong'uda otish.

Baholashning **ikki qatlami** bor:

1. **Retrieval sifati** — kerakli chunk **topildimi**? (Model javobidan oldingi qadam.)
2. **Javob sifati** — yakuniy javob **to'g'ri va to'liqmi**?

### 1-qatlam: retrieval baholash (recall)

Avval kichik **test to'plami** tuzing: 20-50 ta savol va har biri uchun qaysi chunk(lar) javobni o'z ichiga olishini **qo'lda** belgilang. So'ng eng muhim metrika — **recall@k**: kerakli chunk top-`k` ichida bormi?

```python
# Test to'plami: savol -> javobni o'z ichiga olgan chunk ID(lari)
TEST = [
    {"savol": "Qaytarish muddati qancha?", "kerakli": {"c12"}},
    {"savol": "Yetkazib berish narxi?", "kerakli": {"c07", "c08"}},
    # ... 20-50 ta
]

def recall_baho(qidiruv_fn, k: int = 5) -> float:
    """top-k ichida kerakli chunk topilgan savollar ulushi (recall@k)."""
    topildi = 0
    for t in TEST:
        topilgan_idlar = set(qidiruv_fn(t["savol"], top_k=k))
        # Kerakli chunklardan KAMIDA bittasi top-k ichida bo'lsa — hisobladik
        if topilgan_idlar & t["kerakli"]:
            topildi += 1
    return topildi / len(TEST)

print("Naive:", recall_baho(vektor_qidiruv, k=5))
print("Hybrid:", recall_baho(lambda s, top_k: rrf_birlashtir(
    [bm25_qidiruv(s, top_k), vektor_qidiruv(s, top_k)], top=top_k)))
```

Endi siz **raqam** bilan ayta olasiz: "naive recall@5 = 0.68, hybrid = 0.84". Bu — taraqqiyot.

> **Hayotiy o'xshatish.** Test to'plamisiz RAG'ni sozlash — termometrsiz isitmani davolashdek. "Yaxshi bo'ldiganga o'xshaydi" emas, "harorat 39 dan 37 ga tushdi" deyish kerak. Kichik test to'plami — sizning termometringiz.

### 2-qatlam: javob sifati va LLM-as-judge

Retrieval to'g'ri ishlagach, **yakuniy javob** sifatini baholaymiz. Javobni qo'lda o'qib baholash aniq, lekin sekin va miqyoslanmaydi. Yechim — **LLM-as-judge**: **boshqa** LLM chaqiruvi javobni belgilangan mezon bo'yicha baholaydi.

```python
def llm_baho(savol: str, kontekst: str, javob: str) -> dict:
    """Boshqa LLM chaqiruvi javobni sodiqlik va tegishlilik bo'yicha baholaydi."""
    yoriqnoma = (
        "Sen qat'iy baholovchisan. Berilgan KONTEKST asosida JAVOBni 1-5 ball bilan bahola:\n"
        "- sodiqlik (faithfulness): javob faqat kontekstga tayanganmi, to'qimaganmi?\n"
        "- tegishlilik (relevance): javob savolga to'g'ri javob beradimi?\n"
        "Faqat JSON qaytar: {\"sodiqlik\": int, \"tegishlilik\": int, \"izoh\": str}"
    )
    natija = client.chat.completions.create(
        model="gpt-5.5",                            # baholashga kuchliroq model yaxshi
        messages=[
            {"role": "system", "content": yoriqnoma},
            {"role": "user", "content": f"SAVOL:\n{savol}\n\nKONTEKST:\n{kontekst}\n\nJAVOB:\n{javob}"},
        ],
        response_format={"type": "json_object"},    # qat'iy JSON (9-bob)
    )
    import json
    return json.loads(natija.choices[0].message.content)

baho = llm_baho(savol, kontekst, javob)
print(baho)   # {"sodiqlik": 5, "tegishlilik": 4, "izoh": "..."}
```

Eng muhim mezon — **sodiqlik (faithfulness)**: javob **faqat berilgan kontekstga** tayanganmi yoki model o'zidan **to'qib chiqarganmi** (hallucination — 1-bob). RAG'ning butun maqsadi — javobni haqiqiy manbaga bog'lash; sodiqlikni o'lchash shu maqsadning bajarilganini tekshiradi.

> **Hayotiy o'xshatish.** LLM-as-judge — imtihon ishini boshqa, tajribali o'qituvchi tekshirishidek. Talabaning o'zi "men 5 oldim" deyishi ishonchsiz; mustaqil baholovchi esa har ishni bir xil mezon bilan, tez va miqyosda tekshira oladi. Mukammal emas, lekin minglab javobni qo'lda o'qishdan ko'ra amaliy.

!!! warning "LLM-as-judge — foydali, lekin mutlaq emas"
    LLM-baholovchi ham LLM — u ham xato qiladi, uzun yoki ishonchli ko'ringan javobga yuqori ball berishga moyil bo'lishi mumkin. Shuning uchun: (1) baholashga **kuchliroq** model ishlating; (2) mezonni **aniq** yozing (1-5 nimani anglatadi); (3) vaqti-vaqti bilan baholovchining bahosini **qo'lda tekshiring** (kalibrlash). Uni avtomatlashtirilgan birinchi filtr deb biling, yakuniy hakam emas.

---

## Sozlash: chunk o'lchami va top_k

Endi sizda **o'lchov** (recall + LLM-baho) va kichik **test to'plami** bor. Demak, ilgari "tuyg'u bilan" tanlagan parametrlarni endi **raqamga tayanib** sozlay olasiz. Eng ta'sirli ikki parametr:

- **`chunk` o'lchami** — juda kichik bo'lsa, kontekst bo'linib ma'no yo'qoladi; juda katta bo'lsa, bitta chunkda ko'p shovqin va kam aniqlik. Odatda 300-800 token oralig'i va **chunklar orasida overlap** (16-bobda ko'rgansiz) yaxshi ishlaydi.
- **`top_k`** — kam bo'lsa, kerakli chunk tushib qolishi mumkin (recall past); ko'p bo'lsa, shovqin oshadi va kontekst uzayadi (narx + chalg'itish). Re-rank bilan: olishda `top_k=20`, modelga berishda 3-5.

To'g'ri yo'l — **bir necha qiymatni sinab, test to'plamida o'lchash**:

```python
for olcham in (256, 512, 768):
    for k in (3, 5, 8):
        baza = bazani_qur(chunk_olcham=olcham)        # shu o'lchamda qayta indekslash
        r = recall_baho(lambda s, top_k=k: qidir(baza, s, top_k), k=k)
        print(f"chunk={olcham}, top_k={k} -> recall@{k}={r:.2f}")
# Eng yuqori recall (va kerakli narx/tezlik) bergan kombinatsiyani tanlaysiz
```

!!! note "Bittadan o'zgartiring"
    Bir vaqtda bitta narsani o'zgartiring va o'lchang: avval re-rank qo'shing va o'lchang, keyin hybrid, keyin chunk o'lchamini sozlang. Hammasini birdan o'zgartirsangiz — qaysi biri yordam berganini bilmaysiz. Bu — eksperiment intizomi; RAG'ni "his bilan" emas, **ma'lumot bilan** yaxshilashning yagona yo'li.

---

## Hammasini birlashtirgan oqim

Yaxshilangan RAG retrieval bosqichi quyidagicha ko'rinadi (generatsiya 16-bobdagidek):

```python
def yaxshilangan_retrieval(savol: str, suhbat_tarixi: str = "") -> list[str]:
    # 1) Savolni tozalaymiz (suhbat olmoshlarini ochamiz)
    toza = savolni_qayta_yoz(savol, suhbat_tarixi)

    # 2) Hybrid: kalit so'z + semantik, har biri KO'P nomzod
    bm25_n = bm25_qidiruv(toza, top_k=20)
    vektor_n = vektor_qidiruv(toza, top_k=20)        # kerak bo'lsa metadata filtri bilan
    nomzodlar = rrf_birlashtir([bm25_n, vektor_n], top=15)

    # 3) Re-rank: 15 nomzoddan eng yaxshi 4 tasi
    return qayta_tartibla(toza, nomzodlar, top=4)
```

Diqqat: bu — **to'liq to'plam emas, asboblar to'plami**. Hech kim hamma texnikani birdan qo'shmaydi. Naive RAG'dan boshlang, **o'lchang**, eng zaif joyni toping (recall pastmi -> hybrid/multi-query; precision pastmi -> re-rank; noto'g'ri davr chiqyaptimi -> metadata filtri), **bitta** yaxshilanish qo'shing va yana o'lchang. Bu sikl — professional RAG ishlab chiqishning yuragi.

---

## Xulosa

- **Naive RAG ko'pincha yetmaydi**: noto'g'ri chunk topiladi, shovqin keladi, savol so'zlari hujjatga mos kelmaydi. Asosiy haqiqat: **yaxshi javob = yaxshi retrieval** — kerakli chunk topilmasa, eng kuchli model ham to'g'ri javob bera olmaydi.
- **Re-ranking** — ko'p nomzod oling (`top_k=20`), keyin re-ranker (cross-encoder yoki LLM) bilan eng tegishli 3-5 tasini qayta tartiblang. Recall va precisionni birga ko'taradi; odatda eng katta foyda/mehnat nisbati.
- **Hybrid search** — kalit so'z (**BM25**, aniq termin) + vektor (semantik, ma'no) natijalarini **RRF** kabi usul bilan birlashtiring; har biri ikkinchisining zaifligini qoplaydi. Ko'p baza buni o'zi qo'llab-quvvatlaydi.
- **Query rewriting/expansion** — savolni qidiruvdan oldin LLM bilan aniq, mustaqil shaklga keltiring (olmoshlarni oching) yoki **multi-query** bilan bir nechta variant qidiring. Har qo'shimcha chaqiruv — narx; kerak bo'lganda ishlating.
- **Metadata filtering** — qidiruvni sana/bo'lim/manba bilan oldindan toraytiring (qattiq mezon) va semantik bilan birlashtiring (yumshoq mezon). Aniqlik va tezlikni oshiradi.
- **Baholash — eng muhim ko'nikma**: kichik **test to'plami** tuzing; **retrieval**ni `recall@k` bilan, **javob**ni qo'lda yoki **LLM-as-judge** (ayniqsa **sodiqlik**) bilan o'lchang.
- **Sozlash o'lchovga tayansin**: `chunk` o'lchami va `top_k`ni test to'plamida sinab tanlang; har safar **bitta** narsani o'zgartirib o'lchang.
- Yondashuv — to'plam emas, **asboblar to'plami**: naive'dan boshlang, o'lchang, eng zaif joyni toping, bitta yaxshilanish qo'shing, yana o'lchang.

## Amaliy mashqlar

1. **(Oson)** 16-bobdagi RAG'ingizda `top_k`ni 3 dan 20 ga ko'tarib, qaytgan chunklarni chop eting. Kerakli javob 3-o'rindan keyin (4-20 oralig'ida) bormi? Bu — re-ranking nega kerakligini ko'rsatadi.

2. **(Oson)** Bitta savolni `savolni_qayta_yoz` (yoki `kop_savol_yarat`) funksiyasidan o'tkazing va asl hamda yaxshilangan variant(lar)ni solishtiring. Qaysi biri ko'proq qidiruv so'zi beradi?

3. **(O'rtacha)** `rank_bm25` o'rnatib, `bm25_qidiruv` yozing. Aniq atama (masalan mahsulot artikuli yoki "ERR_504") bilan BM25 va vektor qidiruv natijalarini solishtiring — qaysi biri aniq so'zda yutadi? So'ng `rrf_birlashtir` bilan ikkalasini birlashtiring.

4. **(O'rtacha)** `cross-encoder/ms-marco-MiniLM-L-6-v2` re-rankerini o'rnatib, `qayta_tartibla` yozing. 16-bobdagi qidiruvga ulang (ol-20 -> re-rank-3) va re-rank'dan oldingi/keyingi top-3 ni yonma-yon chop eting. Tartib o'zgardimi?

5. **(Qiyin)** 15-20 ta savol va ularning kerakli chunk ID'laridan iborat test to'plami tuzing. `recall_baho` bilan **naive** va **hybrid+re-rank** uchun `recall@5` ni o'lchang va raqamlarni solishtiring. So'ng `llm_baho` (LLM-as-judge) yozib, bir nechta javobning **sodiqlik** balini oling. Qaysi yaxshilanish eng katta farq berdi?

---

[⬅️ Oldingi: 16 — RAG: retrieval va generatsiya](./16-rag-retrieval-generatsiya.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 18 — Agentlar va ReAct sikli ➡️](./18-agentlar-react.md)
