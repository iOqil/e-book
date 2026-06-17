# AI / LLM integratsiyasi — PHP bilan (0 dan ekspertgacha)

PHP ilovangizga **sun'iy intellekt (AI)** va **katta til modellari (LLM)** ni ulashni **noldan** o'rgatadigan to'liq qo'llanma. Oddiy "salom" so'rovidan boshlab — jonli oqim (streaming), strukturali JSON chiqish, function calling (tool use), agentlar, RAG (o'z hujjatlaringiz bo'yicha savol-javob), vektor bazalar va to'liq AI ilovani productionga chiqarishgacha. Amaliy kod **Anthropic'ning rasmiy PHP SDK**'si (Claude) asosida, lekin tushunchalar har qanday provayderga (OpenAI, Gemini, lokal modellar) ko'chiriladi.

> 🎯 **Nega PHP'da AI?** Dunyo saytlarining katta qismi PHP'da. AI'ni o'rganish uchun Python'ga o'tish shart emas — o'z PHP/Laravel loyihangizga aqlli chatbot, hujjat-yordamchi, kontent generatori yoki avtomatlashtirish qo'sha olasiz. Bu kitob sizni "AI nima?" dan to real AI ilovani ishga tushirishgacha olib boradi.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan (jami 73 ta): LLM so'rov-javob oqimi, tool use sikli, agent loop, RAG quvuri, embedding va vektor qidiruv, prompt caching va boshqalar ko'z bilan ko'rib o'rganiladi.

> 💻 **Hamma kod ishlatiladi.** Kitobdagi PHP kod jonli **PHP 8.4 + `anthropic-ai/sdk`** muhitida `php -l` bilan sintaksis tekshiruvidan o'tgan; SDK klasslari va metod imzolari haqiqiy paketdan tasdiqlangan.

---

## Bu kitob kim uchun?

Kitob shunday yozilganki, **boshlovchi ham tushuna oladi** — har tushuncha hayotiy o'xshatish bilan sodda tildan boshlanadi. Oxiriga borib siz **ekspert darajadagi** mavzularni (agentlar, RAG, vektor bazalar, xavfsizlik, baholash, production) ham egallaysiz.

## Talab

| Kerak | Daraja |
|---|---|
| PHP asoslari (o'zgaruvchi, funksiya, massiv, OOP, Composer) | **Shart** — kerak bo'lsa [PHP kitobini](../php/README.md) o'qing |
| Laravel asoslari | Foydali (18-bob uchun) — [Laravel kitobi](../laravel/README.md) |
| Ma'lumotlar bazasi asoslari (PostgreSQL) | Foydali (vektor baza bo'limi uchun) |
| AI/LLM bo'yicha oldindan bilim | **Shart emas** — 0 dan boshlaymiz |
| Anthropic API kaliti (yoki boshqa provayder) | Amaliyot uchun — 2-bobda olamiz |

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing — har qism oldingisiga tayanadi (asoslar → strukturali chiqish → tool/agent → RAG → professional).
2. Har misolni o'z loyihangizda **terib, ishga tushirib ko'ring** — AI'ni "his qilish" uchun shart.
3. Bob oxiridagi **amaliy masalalarni** o'zingiz yeching.
4. Oxirgi bobda hamma bilimni birlashtirib **to'liq AI ilova** quramiz.

---

## I qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [LLM nima va AI integratsiyasi nima](./01-llm-nima.md) | LLM nima, token, kontekst oynasi, qanday "o'ylaydi", API orqali integratsiya, provayderlar manzarasi. |
| 02 | [Muhit va birinchi so'rov](./02-muhit-birinchi-sorov.md) | PHP 8.4 + Composer, Anthropic SDK + Guzzle o'rnatish, API kalit (.env), birinchi `messages->create`. |
| 03 | [Prompt muhandisligi asoslari](./03-prompt-muhandisligi.md) | System vs user, aniq ko'rsatma, few-shot, rol berish, format so'rash, harorat/effort tushunchasi. |
| 04 | [Suhbat va kontekst](./04-suhbat-kontekst.md) | Ko'p-burilishli suhbat, messages massivi, API stateless, kontekst oynasi, token sanash. |
| 05 | [Streaming — jonli javob](./05-streaming.md) | `createStream`, SSE, foydalanuvchiga oqim ko'rsatish, PHP'da SSE endpoint. |

## II qism — Strukturali va ishonchli chiqish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 06 | [Strukturali chiqish (JSON)](./06-strukturali-chiqish.md) | `outputConfig` format, `StructuredOutputModel`, ma'lumot ajratish, klassifikatsiya, validatsiya. |
| 07 | [Vision va hujjatlar](./07-vision-hujjatlar.md) | Rasm tahlili, PDF/hujjat, multimodal — rasm yuborish (base64/URL), hujjatdan ma'lumot olish. |
| 08 | [Xatolar, qayta urinish va ishonchlilik](./08-xatolar-ishonchlilik.md) | Xato turlari, rate limit, retry/backoff, timeout, fallback model, idempotentlik. |

## III qism — Tool use va agentlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 09 | [Function calling (tool use) asoslari](./09-function-calling.md) | Tool nima, ta'rif, model tool so'raydi — siz bajarib qaytarasiz, manual loop. |
| 10 | [Tool runner va ko'p tool](./10-tool-runner.md) | `BetaRunnableTool` + `toolRunner`, avtomatik loop, bir nechta tool, real misol. |
| 11 | [Agentlar qurish](./11-agentlar.md) | Agent nima, agent loop, rejalashtirish, qachon agent kerak, xavfsizlik, inson-tasdiqlash. |
| 12 | [MCP (Model Context Protocol)](./12-mcp.md) | MCP nima, server/tool, PHP'da MCP, mavjud MCP serverlar — AI'ni tashqi tizimlarga ulash standarti. |

## IV qism — RAG va bilim

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 13 | [Embedding va semantik qidiruv](./13-embedding-semantik-qidiruv.md) | Embedding nima, vektor, o'xshashlik, embedding olish, semantik qidiruv g'oyasi. |
| 14 | [Vektor bazalar](./14-vektor-bazalar.md) | pgvector (PostgreSQL), vektor saqlash/qidirish, indeks, qachon vektor baza kerak. |
| 15 | [RAG (Retrieval-Augmented Generation)](./15-rag.md) | Hujjat → chunk → embed → saqlash → qidirish → prompt; to'liq RAG quvuri PHP'da. |
| 16 | [Kesh va xarajat optimizatsiyasi](./16-kesh-xarajat.md) | Prompt caching, token tejash, model tanlash (Opus/Sonnet/Haiku), Batch API, monitoring. |

## V qism — Frameworklar va arxitektura

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 17 | [PHP GenAI frameworklari](./17-frameworklar.md) | LLPhant va Neuron AI — multi-provider abstraktsiya, qachon framework, qachon to'g'ridan SDK. |
| 18 | [Laravel'ga integratsiya](./18-laravel-integratsiya.md) | AI xizmati, queue bilan asinxron, real misol (chatbot/yordamchi), Livewire/Blade bilan UI. |
| 19 | [Boshqa provayderlar (OpenAI/Gemini/Ollama)](./19-boshqa-provayderlar.md) | Provayder-agnostik kod, `openai-php/client`, Gemini, lokal Ollama, OpenAI-mos API, qachon qaysi. |

## VI qism — Professional daraja

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 20 | [Xavfsizlik](./20-xavfsizlik.md) | Prompt injection, ma'lumot sizishi, API kalit himoyasi, kiritmaga ishonmaslik, PII, jailbreak. |
| 21 | [Testlash va baholash](./21-testlash-baholash.md) | LLM kodini test qilish, mock, eval/baholash, LLM-as-judge, regress, sifat o'lchash. |
| 22 | [Production va kuzatuv](./22-production-kuzatuv.md) | Deploy, rate limit boshqaruvi, logging/observability, xarajat kuzatuvi, fallback, versiya. |
| 23 | [Promptlarni boshqarish va ilg'or naqshlar](./23-promptlarni-boshqarish.md) | Prompt versiyalash, shablon, chain/pipeline, router, guardrails, structured workflow. |

## VII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 24 | [Yakuniy loyiha: to'liq AI ilova](./24-kapston-loyiha.md) | Real ilova 0 dan: hujjat-yordamchi (RAG) + tool + streaming + UI + xavfsizlik + deploy. |

---

## Versiya va texnologiyalar

Bu kitob **PHP 8.4** va **Anthropic rasmiy PHP SDK** (`anthropic-ai/sdk`) asosida yozilgan; modellar — **Claude Opus 4.8 / Sonnet 4.6 / Haiku 4.5** (2026). Tushunchalar provayderga bog'liq emas: 19-bobda OpenAI, Gemini, Ollama (lokal) va PHP GenAI frameworklari (LLPhant, Neuron AI) ko'rsatiladi.

```text
$ composer require anthropic-ai/sdk guzzlehttp/guzzle
$ php -v
PHP 8.4.0
```

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
