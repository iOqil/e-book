# Next.js — 0 dan Expert darajagacha (o'zbek tilida)

Bu qo'llanma **Next.js 16** (App Router) va **React 19** ni **mutlaqo noldan** professional darajagacha o'rgatadi. Hech qanday oldingi tajriba — JavaScript ham, React ham — talab qilinmaydi: birinchi qism ularni ham noldan tushuntiradi.

> **Versiya:** Next.js **16**, React **19**, Node.js **20.9+**. Kod misollari shu versiyalarga moslangan (async `params`, `"use cache"`, sukut bo'yicha keshlanmaydigan `fetch`/GET va h.k.).

---

## Qanday ishlatish kerak

1. Qismlarni va boblarni **tartib bilan** o'qing (0-BOB → 19-BOB). Har biri oldingisiga tayanadi.
2. Har bobdagi kodni **o'z kompyuteringizda yozib, ishga tushiring**. Faqat o'qib ketsangiz — bilim o'rnashmaydi.
3. Bob oxiridagi **mashqlar (challenge)** ni mustaqil bajaring.
4. "⚠️ Next.js 16" va "Keng tarqalgan xatolar" bloklarini e'tibordan qochirmang — ular real loyihada vaqtingizni tejaydi.

---

## Talablar

| Kerak | Daraja |
|---|---|
| Kompyuter, terminal, brauzer | Asoslar |
| Node.js 20.9+ | O'rnatiladi (0-bobda) |
| Oldingi dasturlash tajribasi | **Shart emas** — JS va React noldan o'rgatiladi |

---

## To'liq yo'l xaritasi (roadmap)

### [1-QISM — Asoslar](./Nextjs-0-dan-Expert-1-qism.md)
| Bob | Mavzu |
|---|---|
| 0 | Boshlashdan oldin (muhit sozlash, Node.js) |
| 1 | JavaScript asoslari |
| 2 | React asoslari |
| 3 | Next.js bilan birinchi qadamlar |
| 4 | Routing — sahifalar tizimi |

### [2-QISM — Server, ma'lumot va Actions](./Nextjs-0-dan-Expert-2-qism.md)
| Bob | Mavzu |
|---|---|
| 5 | Server Components va Client Components |
| 6 | Ma'lumot olish (Data Fetching) |
| 7 | Server Actions — ma'lumot yuborish va saqlash |
| 8 | Keshlash (Caching) va `"use cache"` |

### [3-QISM — Full-stack: API, baza, auth](./Nextjs-0-dan-Expert-3-qism.md)
| Bob | Mavzu |
|---|---|
| 9 | Route Handlers — o'z API'ngiz |
| 10 | Ma'lumotlar bazasi (Prisma) |
| 11 | Validatsiya (Zod) |
| 12 | Autentifikatsiya (Better Auth) va xavfsizlik |

### [4-QISM — Production (yakuniy)](./Nextjs-0-dan-Expert-4-qism.md)
| Bob | Mavzu |
|---|---|
| 13 | Performance (tezlik) |
| 14 | Test yozish |
| 15 | Deployment — saytni internetga chiqarish |
| 16 | Monitoring, ilg'or patternlar va yakuniy loyiha |

### [BONUS — Ilg'or mavzular](./Nextjs-0-dan-Expert-Bonus-i18n-Stripe-Realtime.md)
| Bob | Mavzu |
|---|---|
| 17 | Ko'p tillik (i18n) |
| 18 | To'lov qabul qilish (Stripe va mahalliy provayderlar) |
| 19 | Real-time (jonli yangilanish / WebSocket) |

> Jami: **20 bob**, 4 asosiy qism + bonus. 0 dan to'liq full-stack production ilovagacha.

---

## Boshlashdan oldin

[nodejs.org](https://nodejs.org) dan **Node.js 20.9+** ni o'rnating, keyin:

```bash
npx create-next-app@latest
```

Tayyor bo'lsang — **[1-QISM: Asoslar →](./Nextjs-0-dan-Expert-1-qism.md)** dan boshla.
