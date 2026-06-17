# AI/LLM integratsiyasi — JavaScript bilan (0 dan Expertgacha)

Bu qo'llanma sizni **AI/LLM (sun'iy intellekt / katta til modellari) ni JavaScript ilovalariga ulashni** mutlaqo noldan professional darajagacha o'rgatadi. Birinchi bob "LLM nima va qanday ishlaydi?" dan boshlanadi, oxirgi bob esa to'liq, ishlab chiqarishga tayyor AI ilovasini — chat + RAG + vositalar (tools) + oqimli (streaming) UI — noldan quradi.

> 🤖 Kitob **Anthropic Claude** modellari va rasmiy **`@anthropic-ai/sdk`** (JavaScript/TypeScript) atrofida qurilgan, hamda zamonaviy **Vercel AI SDK** (`ai` + `@ai-sdk/anthropic`) bilan ilova qatlamini o'rgatadi. Standart model — **Claude Opus 4.8** (`claude-opus-4-8`), 1M tokenli kontekst.

> ✅ Kitobdagi barcha SDK chaqiruvlari **jonli o'rnatilgan paketlar** bilan tip-tekshiruvdan (`tsc`) o'tkazilgan: `@anthropic-ai/sdk` 0.104, `ai` (AI SDK v6) 6.0, `@ai-sdk/anthropic` 3.0, `zod` 4.4 — ya'ni misollardagi metod nomlari va parametrlar haqiqatan ham mavjud va to'g'ri.

> 🎨 Har bob **SVG diagramlar** bilan boyitilgan — tokenizatsiya, kontekst oynasi, streaming oqimi, tool-use sikli, RAG quvuri (pipeline), agent loop, prompt caching kabi tushunchalar ko'z bilan ko'rib o'rganiladi. Jami **26 bob, 78 diagramma**.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. Har bir kod misolini **o'zingiz yozib, ishga tushiring**. AI integratsiyasini faqat o'qib o'rganib bo'lmaydi.
3. Har bob oxiridagi **Mashqlar**ni o'zingiz yeching, keyin `<details>` ichidagi yechimga qarang.
4. **API kaliti pul turadi** — har bir chaqiruv tokenlar uchun haq oladi. Boshida arzon model (Haiku) va kichik `max_tokens` bilan tajriba qiling.

## Talab

| Kerak | Daraja |
|---|---|
| **JavaScript / Node.js asoslari** (async/await, ESM, npm, `fetch`) | **Shart** |
| Node.js 18+ va terminal | Shart |
| **Anthropic API kaliti** (console.anthropic.com) | Shart (02-bobda olamiz) |
| TypeScript tajribasi | Foydali, lekin shart emas (kitob JS'da) |
| React / Next.js (UI boblari uchun) | Foydali |

> ⚠️ Bu kitob **dasturlashni emas, AI integratsiyasini** o'rgatadi. JavaScript'ni bilmasangiz, avval [JavaScript kitobini](../js/README.md) va kerak bo'lsa [Node.js kitobini](../nodejs/README.md) o'qing. Bu yerda `async`/`await`, modullar va `npm` siz uchun tanish deb hisoblanadi.

---

## I qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [LLM nima va qanday ishlaydi](./01-llm-nima.md) | til modeli (LLM) tushunchasi, tokenlar, kontekst oynasi, ehtimollik va "keyingi token", nega JavaScript bilan, Claude/Anthropic bilan tanishuv. |
| 02 | [O'rnatish va birinchi chaqiruv](./02-ornatish-birinchi-chaqiruv.md) | Node loyiha, `npm i @anthropic-ai/sdk`, API kaliti va `.env` xavfsizligi, birinchi `messages.create`, `claude-opus-4-8`. |
| 03 | [Messages API chuqur](./03-messages-api.md) | rollar (`user`/`assistant`), `system` prompt, ko'p bosqichli (multi-turn) suhbat (API holatsiz!), `max_tokens`, `stop_reason`, content bloklar. |
| 04 | [Streaming (oqimli javob)](./04-streaming.md) | nega streaming, `client.messages.stream()`, event'lar, `.finalMessage()`, oqimni UI va terminalga ulash. |
| 05 | [Prompt engineering](./05-prompt-engineering.md) | aniq ko'rsatma berish, rol berish, few-shot misollar, XML teglar, "ketma-ket o'ylash", Claude uchun eng yaxshi amaliyotlar. |

## II qism — Strukturali chiqish va vositalar (tools)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 06 | [Strukturali chiqish (JSON)](./06-structured-output.md) | `output_config.format` (`json_schema`), `messages.parse()`, Zod sxema bilan validatsiya — ishonchli JSON olish. |
| 07 | [Tool use (funksiya chaqirish)](./07-tool-use.md) | tool ta'rifi, `tool_use`/`tool_result` sikli, qo'lda agent loop, parallel vositalar, `tool_choice`. |
| 08 | [Tool runner va Zod](./08-tool-runner-zod.md) | SDK avtomatik tool runner (`betaZodTool`), Zod bilan tipli vositalar — qo'lda loop'siz. |
| 09 | [Vision va hujjatlar](./09-vision-fayllar.md) | rasm yuborish (base64/URL), PDF tahlili, Files API (beta) — bir faylni qayta-qayta ishlatish. |
| 10 | [Adaptiv thinking va effort](./10-thinking-effort.md) | Claude Opus 4.8 ning `thinking: {type:"adaptive"}` va `output_config.effort` (low→max) — chuqur o'ylashni boshqarish. |

## III qism — Vercel AI SDK (ilova qatlami)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 11 | [Vercel AI SDK bilan tanishuv](./11-vercel-ai-sdk-kirish.md) | `ai` + `@ai-sdk/anthropic`, `generateText`/`streamText`, nega abstraksiya qatlami foydali. |
| 12 | [AI SDK: strukturali chiqish va vositalar](./12-ai-sdk-structured-tools.md) | `generateObject`/`streamObject` (+ Zod), `tool({inputSchema, execute})`, agent loop (`stopWhen: stepCountIs`). |
| 13 | [AI SDK UI: chat interfeysi](./13-ai-sdk-ui.md) | React `useChat`, Next.js route handler, oqimli (streaming) chat UI'ni qurish. |

## IV qism — Token, narx va ishonchlilik

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 14 | [Token, narx va limitlar](./14-token-narx-limit.md) | tokenizatsiya, `countTokens` (tiktoken EMAS), modellar narxi, rate limit, to'g'ri model tanlash. |
| 15 | [Prompt caching](./15-prompt-caching.md) | `cache_control: {type:"ephemeral"}`, prefix-moslik, 90% gacha tejash, cache hit'larni tekshirish. |
| 16 | [Xatolar, retry va ishonchlilik](./16-xatolar-retry.md) | tipli xatolar (`RateLimitError` va b.), SDK avtomatik retry, timeout, oqimda xatolar, ishonchli klient. |

## V qism — RAG (bilimga asoslangan javob)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 17 | [Embeddings va semantik qidiruv](./17-embeddings.md) | embedding nima, semantik qidiruv, AI SDK `embed`/`embedMany`, embedding provayderi (Claude embedding bermaydi — Voyage AI v.b.). |
| 18 | [Vektor baza va RAG](./18-vector-db-rag.md) | bo'laklash (chunking), vektor saqlash (pgvector/lokal), o'xshashlik qidiruvi, to'liq RAG quvuri Claude bilan. |

## VI qism — Agentlar va MCP

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 19 | [Agentlar asoslari](./19-agentlar-asoslari.md) | agent loop nima, qachon agent qurish kerak (4 mezon), reasoning + tools, oddiy agentni noldan qurish. |
| 20 | [MCP — Model Context Protocol](./20-mcp.md) | MCP nima, `mcp_servers` parametri, JS'da MCP klient/server, tashqi vositalarni ulash. |
| 21 | [Ko'p bosqichli va ko'p agentli ish](./21-multi-agent.md) | orkestratsiya, subagentlar, parallel ishlash, murakkab oqimlarni qurish. |

## VII qism — Ishlab chiqarish (production)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 22 | [Xavfsizlik](./22-xavfsizlik.md) | API kalitini himoyalash, prompt injection, chiqishni validatsiya, kontent moderatsiyasi, PII. |
| 23 | [Observability va evals](./23-observability-evals.md) | log/trace, xarajat kuzatuvi, chiqish sifatini baholash (eval), LLM-as-judge. |
| 24 | [Batch API va optimizatsiya](./24-batch-optimizatsiya.md) | Batches API (50% arzon, ommaviy ishlash), kechikishni (latency) va xarajatni kamaytirish. |
| 25 | [Deploy: serverless va edge](./25-deploy.md) | Vercel/Cloudflare Workers'ga joylash, edge'da streaming, muhit o'zgaruvchilari, ishlab chiqarishga tayyorlik. |

## VIII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 26 | [Yakuniy loyiha: to'liq AI ilova](./26-kapston-loyiha.md) | o'rgangan hammasini birlashtirib — Claude chat + RAG + vositalar + oqimli UI + xavfsizlik — noldan to'liq AI ilova. |

---

## AI/LLM va JavaScript — bir og'iz (kontekst uchun)

**LLM** (Large Language Model — katta til modeli) — bu ulkan matn ustida o'rgatilgan, "keyingi so'zni (token)" bashorat qiluvchi neyron tarmoq. **Claude** — Anthropic kompaniyasining LLM oilasi; siz unga matn (prompt) yuborasiz, u javob qaytaradi. Sehr yo'q: bu HTTP API — siz so'rov jo'natasiz, javob olasiz, xuddi boshqa API kabi. JavaScript bu vazifa uchun ideal: `@anthropic-ai/sdk` rasmiy paketi va Vercel AI SDK bilan siz bir necha qatorda chat, agent yoki RAG tizimini qura olasiz, va uni veb (Next.js), serverless yoki edge'da ishlatasiz.

Bu kitob AI'ni "sehrli quti" sifatida emas, balki **siz boshqaradigan, narxini va sifatini tushunadigan vosita** sifatida o'rgatadi: nega tokenlar muhim, qachon tool kerak, qanday qilib ishonchli JSON olish, va ilovangizni ishlab chiqarishda xavfsiz hamda arzon tutish.

> Bu kitob **JavaScript** nashri. Xuddi shu mavzu PHP va Python uchun alohida kitoblarda beriladi.

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
