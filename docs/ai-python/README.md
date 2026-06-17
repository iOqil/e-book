# AI / LLM integratsiyasi (Python) — 0 dan ekspertgacha

**Python** bilan ilovalaringizga **sun'iy intellekt (AI)** va **katta til modellarini (LLM)** ulashni **noldan** o'rgatadigan to'liq qo'llanma. Birinchi API so'rovidan tortib **RAG** (o'z hujjatlaringiz ustida savol-javob), **agentlar**, **tool calling**, **lokal modellar** va **production**gacha (xarajat, xavfsizlik, deploy). Kitob **ko'p provayderli** yondashuvga asoslangan: bitta kod — **OpenAI, Claude (Anthropic), Gemini (Google), Groq, OpenRouter, DeepSeek** va hatto **lokal Ollama**.

> 🎯 **Nega bu kitob?** LLM'lar dasturlashni tubdan o'zgartirdi. Endi "aqlli" ilova qurish uchun mashina o'rganishni noldan o'rganish shart emas — siz tayyor modelni **API orqali chaqirasiz**. Bu kitob sizga aynan shuni: LLM'ni Python ilovaga **professional, ishonchli va arzon** ulashni o'rgatadi. Chatbot, hujjat-tahlilchi, agent, RAG-tizim — hammasini o'zingiz qurasiz.

> 🌐 **Ko'p provayderli — O'zbek o'quvchi uchun amaliy.** Asosiy o'q sifatida **OpenAI-mos API** (Chat Completions) ishlatiladi — bu de-fakto standart bo'lib, faqat `base_url` va kalitni o'zgartirib, o'nlab provayderga (jumladan **bepul** Groq, **arzon** DeepSeek, **lokal/bepul** Ollama) ulanasiz. Alohida boblarda Claude va Gemini'ning native SDK'lari ham chuqur ko'riladi.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan (jami ~84): so'rov anatomiyasi, token oqimi, tool-calling sikli, RAG quvuri, embedding fazosi, agent ReAct sikli, xarajat tahlili va arxitektura sxemalari ko'z bilan ko'rib o'rganiladi.

> 💻 **Kod ishlatiladigan.** Misollar **Python 3.11+** uchun yozilgan va sintaktik tekshiruvdan (`py_compile`) o'tkazilgan; API chaqiruvlari joriy (2026) rasmiy SDK hujjatlariga asoslangan. **Eslatma:** model nomlari va narxlar tez o'zgaradi — kitob har doim provayderning model ro'yxatini tekshirishni o'rgatadi.

---

## Bu kitob kim uchun?

Python'ni **biladigan** (o'zgaruvchi, funksiya, `dict`/`list`, `try/except`, virtual muhit, `pip`) har bir dasturchi uchun. AI yoki matematika bo'yicha oldingi bilim **shart emas** — har tushuncha sodda tildan, hayotiy o'xshatish bilan boshlanadi. Oxiriga borib siz **ekspert darajadagi** mavzularni (RAG, agentlar, MCP, production xavfsizligi, evaluatsiya) ham egallaysiz.

## Talab

| Kerak | Daraja |
|---|---|
| Python asoslari (funksiya, `dict`/`list`, `try/except`, `async` haqida tushuncha) | **Shart** — kerak bo'lsa [Python kitobini](../python/README.md) o'qing |
| Virtual muhit va `pip` | **Shart** — 2-bobda qaytariladi |
| JSON va HTTP haqida umumiy tushuncha | Foydali — kitobda qaytariladi |
| Bitta provayder kaliti (yoki bepul Ollama) | 2-bobda olishni ko'rsatamiz; ko'p misol bepul tier'da ishlaydi |

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing — har qism oldingisiga tayanadi.
2. Har misolni o'zingiz **terib, ishga tushiring** — AI integratsiyasini faqat qilib o'rganasiz.
3. Bob oxiridagi **amaliy masalalarni** yeching.
4. So'nggi ikki bobda hamma bilimni birlashtirib **to'liq AI ilova** quramiz (RAG chatbot + agent).

---

## I qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [AI/LLM integratsiyasi nima va nega kerak](./01-ai-llm-integratsiya-nima.md) | LLM nima, token va kontekst, "integratsiya = API chaqirish", modellar landshafti, bu kitob yo'l xaritasi. |
| 02 | [Muhitni sozlash va birinchi so'rov](./02-muhit-birinchi-sorov.md) | Python muhit, API kalit olish, `.env`, `openai` SDK, birinchi `chat.completions` chaqiruvi. |
| 03 | [Chat formati: messages, rollar, suhbat](./03-chat-formati-rollar.md) | `system`/`user`/`assistant` rollari, xabar tarixi, javobni o'qish, `usage`. |
| 04 | [Modellar va provayderlar: bitta SDK, ko'p provayder](./04-modellar-provayderlar.md) | `base_url` almashtirish (OpenAI/Groq/OpenRouter/DeepSeek/Ollama/Gemini), model tanlash, narx/tezlik/sifat. |

## II qism — Promptlar va matn generatsiyasi

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 05 | [Prompt muhandisligi](./05-prompt-muhandisligi.md) | System prompt, aniq ko'rsatma, few-shot, rol berish, format so'rash, keng tarqalgan xatolar. |
| 06 | [Generatsiya parametrlari](./06-parametrlar.md) | `temperature`, `top_p`, `max_tokens`, `stop`, `seed`; determinism va ijodiylik. |
| 07 | [Streaming: token-token javob](./07-streaming.md) | `stream=True`, real-vaqt UI, generatorlar, streamingda xatolar. |
| 08 | [Suhbat xotirasi va kontekst boshqaruvi](./08-suhbat-xotira-kontekst.md) | Multi-turn suhbat, tarixni saqlash, kontekst oynasi, qisqartirish va xulosalash. |

## III qism — Strukturali natija va tashqi dunyo

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 09 | [Strukturali natija (JSON + Pydantic)](./09-strukturali-natija-json.md) | JSON mode, structured outputs, `response_format`, Pydantic bilan validatsiya. |
| 10 | [Function/tool calling asoslari](./10-tool-calling-asoslari.md) | `tools` ta'rifi, model funksiyani chaqiradi, natijani qaytarish sikli. |
| 11 | [Tool calling chuqur va ko'p qadamli](./11-tool-calling-chuqur.md) | Parallel tool'lar, ko'p qadamli loop, real funksiyalar (API, DB, hisob-kitob). |
| 12 | [Multimodal: rasm va ovoz](./12-multimodal-rasm-ovoz.md) | Vision (rasmni tushunish), audio transkripsiya, rasm generatsiya, base64/URL. |

## IV qism — RAG (o'z bilimingiz ustida)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 13 | [Embeddings va semantik qidiruv](./13-embeddings-semantik-qidiruv.md) | Embedding nima, vektor fazosi, cosine o'xshashlik, semantik qidiruv. |
| 14 | [Vektor bazalari](./14-vektor-bazalari.md) | Chroma, pgvector, FAISS; vektorlarni saqlash, indeks va qidiruv. |
| 15 | [RAG: chunking va indekslash](./15-rag-chunking-indekslash.md) | Hujjatlarni bo'lish (chunk), metadata, indeks qurish, yuklash quvuri. |
| 16 | [RAG: retrieval va generatsiya](./16-rag-retrieval-generatsiya.md) | Qidiruv + kontekst + javob, manba ko'rsatish (citations), promptni yig'ish. |
| 17 | [RAG'ni yaxshilash va baholash](./17-rag-yaxshilash-baholash.md) | Re-ranking, hybrid search, query expansion, RAG sifatini o'lchash. |

## V qism — Agentlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 18 | [Agentlar va ReAct sikli](./18-agentlar-react.md) | Agent nima, reasoning + acting, tool loop, qachon agent kerak (va kerakmas). |
| 19 | [0 dan agent qurish](./19-agent-qurish.md) | Tool registry, agent sikli, xotira, to'xtash sharti, xavfsizlik chegaralari. |
| 20 | [Agent freymvorklari va MCP](./20-agent-freymvork-mcp.md) | LangChain/LlamaIndex umumiy ko'rinish, MCP (Model Context Protocol), qachon freymvork. |

## VI qism — Lokal modellar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 21 | [Lokal LLM: Ollama](./21-lokal-llm-ollama.md) | Ollama o'rnatish, model yuklash, OpenAI-mos endpoint, kvantizatsiya, lokal vs bulut. |

## VII qism — Production

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 22 | [Xarajat, token va keshlash](./22-xarajat-token-kesh.md) | Token sanash, narx hisobi, prompt caching, batch, model bilan tejash. |
| 23 | [Ishonchlilik: xato, retry, rate limit](./23-ishonchlilik-retry.md) | Xato turlari, exponential backoff, timeout, fallback provayder, idempotentlik. |
| 24 | [Xavfsizlik va prompt injection](./24-xavfsizlik-prompt-injection.md) | API kalitlarni saqlash, prompt injection, PII, output validatsiya, moderation. |
| 25 | [Kuzatuv, logging va baholash (eval)](./25-kuzatuv-baholash.md) | Logging, tracing, LLM-as-judge, evaluatsiya, regress sinov, A/B. |
| 26 | [Deploy: FastAPI bilan LLM xizmati](./26-deploy-fastapi.md) | REST API, streaming endpoint, async, konfiguratsiya, konteyner va masshtab. |

## VIII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 27 | [Kapston I: RAG chatbot](./27-kapston-rag-chatbot.md) | To'liq tizim: hujjat yuklash + RAG + suhbat + manba + FastAPI/CLI. |
| 28 | [Kapston II: agent-asoslangan avtomatlashtirish](./28-kapston-agent.md) | Tool + agent + xotira + ko'p qadamli real vazifa, 0 dan oxirigacha. |

---

## Versiya va provayderlar haqida

Kitob **Python 3.11+** va quyidagi rasmiy SDK'larga asoslangan: `openai` (OpenAI-mos API uchun universal), `anthropic` (Claude), `google-genai` (Gemini), `ollama` (lokal). RAG uchun `chromadb`, `pydantic`, `fastapi` ishlatiladi.

```text
$ pip install openai anthropic google-genai ollama chromadb pydantic fastapi
```

!!! warning "Model nomlari o'zgaradi"
    Bu kitobdagi model nomlari (`gpt-5.4-mini`, `claude-haiku-4-5`, `gemini-2.5-flash` va h.k.) — **yozilgan paytdagi misollar**. LLM provayderlari modellarni tez-tez yangilaydi. Har doim provayderning rasmiy **model ro'yxatini** tekshiring (`client.models.list()` yoki hujjat). Kitob aynan shu — "o'zgarishga chidamli" kod yozishni — o'rgatadi.

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
