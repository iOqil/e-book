# Python: Noldan boshlab — Boshlovchilar uchun

Bu — Python'ni **mutlaqo noldan** o'rgatadigan qo'llanma. Hech qanday oldingi dasturlash tajribasi talab qilinmaydi. Bu yerda:

- Boshqa tillar bilan solishtirish **yo'q** — faqat sof Python. Boshqa til bilmasang ham hammasi tushunarli.
- Har bir tushuncha sodda tilda, kundalik hayotdan misollar bilan tushuntiriladi.
- Sekin-asta, qadam-baqadam — har modul oldingisiga tayanadi.
- Har modulda 20 ta masala va to'liq yechimlar bor.

---

## Yo'l xaritasi

| # | Modul | Mavzu | Holat |
|---|-------|-------|-------|
| 01 | [`01-asoslar.md`](./01-asoslar.md) | print, o'zgaruvchilar, tiplar, input, f-string | ✅ Tayyor |
| 02 | [`02-boshqaruv-funksiyalar.md`](./02-boshqaruv-funksiyalar.md) | if/elif/else, for, while, funksiyalar | ✅ Tayyor |
| 03 | [`03-malumot-tuzilmalari.md`](./03-malumot-tuzilmalari.md) | ro'yxat, lug'at, to'plam, tuple | ✅ Tayyor |
| 04 | [`04-stringlar.md`](./04-stringlar.md) | matn metodlari, slicing, qidiruv | ✅ Tayyor |
| 05 | [`05-oop.md`](./05-oop.md) | klasslar va obyektlar | ✅ Tayyor |
| 06 | [`06-modullar-muhit.md`](./06-modullar-muhit.md) | modullar, `pip`, virtual muhit | ✅ Tayyor |
| 07 | [`07-xatolar-context.md`](./07-xatolar-context.md) | xatolarni boshqarish (`try/except`) | ✅ Tayyor |
| 08 | [`08-fayl-malumot.md`](./08-fayl-malumot.md) | fayllar, JSON, CSV | ✅ Tayyor |
| 09 | [`09-iterator-generator-decorator.md`](./09-iterator-generator-decorator.md) | generator va dekoratorlar | ✅ Tayyor |
| 10 | [`10-typing-functional.md`](./10-typing-functional.md) | tip ko'rsatmalari, `map/filter` | ✅ Tayyor |
| 11 | [`11-standart-kutubxona.md`](./11-standart-kutubxona.md) | tayyor kutubxonalar | ✅ Tayyor |
| 12 | [`12-concurrency-async.md`](./12-concurrency-async.md) | parallel ishlash, `asyncio` | ✅ Tayyor |
| 13 | [`13-testlash.md`](./13-testlash.md) | dasturni test qilish | ✅ Tayyor |
| 14 | [`14-web-capstone.md`](./14-web-capstone.md) | FastAPI bilan veb API | ✅ Tayyor |
| 15 | [`15-malumotlar-bazasi.md`](./15-malumotlar-bazasi.md) | ma'lumotlar bazasi, SQL | ✅ Tayyor |

---

## Boshlashdan oldin

Python o'rnatilganini tekshir (terminalda):

```bash
python --version
```

Agar `Python 3.x.x` chiqsa — tayyor. Chiqmasa, [python.org](https://www.python.org/downloads/) dan yuklab o'rnat.

Kodni ishga tushirishning ikki yo'li:
1. **Interaktiv (REPL)** — terminalda `python` deb yoz, `>>>` belgisiga buyruq yozib darhol natija ko'r.
2. **Fayl** — `dastur.py` fayl yarat, kod yoz, `python dastur.py` bilan ishga tushir.

Birinchi moduldan boshla: [01 — Asoslar →](./01-asoslar.md)
