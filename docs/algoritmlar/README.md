# Algoritmlar va ma'lumotlar strukturalari — 0 dan Expertgacha

Bu kitob sizni **algoritmik fikrlash** bo'yicha mutlaqo noldan — "algoritm nima?" degan savoldan — ekspert darajasiga olib chiqadi. Eng oddiy **chiziqli algoritm** tuzishdan boshlab (ketma-ket qadamlar), **tarmoqlanuvchi** va **takrorlanuvchi** algoritmlar, **rekursiya**, so'ng algoritmlarni **tahlil qilish** (Big-O, murakkablik), barcha asosiy **ma'lumotlar strukturalari** (massiv, ro'yxat, stack, queue, hash, daraxt, heap, graf), **algoritm paradigmalari** (divide & conquer, greedy, dinamik dasturlash, backtracking), **klassik algoritmlar** (saralash, qidiruv, graf, string) va nihoyat **hisoblash murakkabligi nazariyasi** (P, NP, NP-to'liqlik) hamda yakuniy **kapston**ga yetadi.

> 🧭 **Til-mustaqil kitob.** Algoritm — bu sintaksis emas, **fikr**. Shuning uchun bu kitob biror dasturlash tiliga bog'lanmaydi: asosiy yuk **diagrammalar** (blok-sxema, struktura tasviri), **psevdokod** va **matematik tahlil**da. Lekin har bir algoritm yonida **ishlaydigan Python** namunasi beriladi, chunki Python psevdokodga eng yaqin va o'qishga qulay til. G'oyalar har qanday tilda (C, Java, JS, Go...) bir xil qo'llaniladi.

> ⚖️ **HALOL eslatma.** Bu kitob **nazariy**: u sizga algoritmlarni *yodlatmaydi*, balki ularni **qanday o'ylab topishni**, **nega ishlashini** (to'g'rilik isboti) va **qancha tez ishlashini** (murakkablik tahlili) o'rgatadi. Murakkablik baholari (Big-O) — matematik aniq; Python namunalari **haqiqatan ishga tushirib tekshirilgan**. Amaliy masalalar to'plamini esa [1000 masala](../1000-masala/README.md) kitobida topasiz — bu ikki kitob bir-birini to'ldiradi: bu yerda **nazariya va tushuncha**, u yerda **mashq va intervyu masalalari**.

> ℹ️ Bu kitob siz **kamida bitta dasturlash tilida** asosiy kod yoza olasiz deb hisoblaydi (o'zgaruvchi, shart, sikl, funksiya, massiv). Agar yangi bo'lsangiz, avval [Python](../python/README.md) yoki [JavaScript](../js/README.md) kitobidan birini ko'rib chiqing. Matematikadan faqat maktab darajasi (daraja, logarifm tushunchasi) yetarli — kerakli matematikani kitobning o'zi tushuntiradi.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har qism oldingisiga tayanadi: fikrlash asoslari → tahlil → strukturalar → paradigmalar → klassik algoritmlar → nazariya.
2. Har bobdagi **diagramma** va **trassirovka jadvallarini** diqqat bilan kuzating — algoritm ko'p jihatdan vizual va qadamba-qadam fikrlash.
3. Kodni faqat o'qib qo'ymang — **qog'ozda yoki kompyuterda o'zingiz ishlatib ko'ring**, kichik kirishlarda qadamlarni qo'lda kuzating.
4. Har bobning **"Mashqlar"** bo'limini albatta ishlang: algoritmika faqat amaliyot bilan o'rganiladi. Avval o'zingiz urinib, keyin yechimni oching.

## Talab

| Kerak | Daraja |
|---|---|
| Kamida bitta tilda asosiy dasturlash (o'zgaruvchi, sikl, funksiya, massiv) | **Shart** |
| Funksiya va rekursiya tushunchasi | Foydali (kitob ham tushuntiradi) |
| Maktab matematikasi (daraja, logarifm, oddiy yig'indi) | Foydali |
| Big-O va murakkablik | **Shart emas** — kitob noldan o'rgatadi |

---

## Mundarija

### I qism — Algoritmik fikrlash asoslari

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Algoritm nima va uning xossalari](./01-algoritm-nima.md) | Algoritm ta'rifi, al-Xorazmiy, 5 ta xossa (aniqlik, cheklilik, kirish/chiqish, samaradorlik), kundalik va kompyuter algoritmlari. |
| 02 | [Algoritmni tasvirlash: blok-sxema, psevdokod, trassirovka](./02-tasvirlash-blok-sxema-psevdokod.md) | Blok-sxema belgilari, psevdokod yozish, qadamba-qadam trassirovka (qo'lda ishlatish), o'zgaruvchi va qiymat. |
| 03 | [Chiziqli (ketma-ket) algoritmlar](./03-chiziqli-algoritmlar.md) | Sequential bajarilish, kirish→qayta ishlash→chiqish, almashtirish, oddiy hisob-kitob algoritmlari. |
| 04 | [Tarmoqlanuvchi algoritmlar (shartlar)](./04-tarmoqlanuvchi-algoritmlar.md) | Shart, if/else, tanlash (switch), murakkab shartlar (AND/OR/NOT), ichma-ich shartlar, qaror daraxti. |
| 05 | [Takrorlanuvchi algoritmlar va sikl invarianti](./05-takrorlanuvchi-algoritmlar.md) | Sikl (for/while), sanagich, akkumulyator, sikl invarianti, to'g'rilik, cheksiz sikldan saqlanish. |
| 06 | [Rekursiya asoslari](./06-rekursiya-asoslari.md) | Rekursiya, baza va qadam, chaqiruvlar steki, rekursiya vs iteratsiya, klassik misollar (faktorial, Fibonachchi, Hanoy). |

### II qism — Algoritm tahlili (murakkablik)

| # | Bob | Mavzu |
|---|---|---|
| 07 | [Algoritm samaradorligi va hisoblash modeli](./07-samaradorlik-hisoblash-modeli.md) | Nega tezlikni o'lchaymiz, RAM modeli, asosiy amallarni sanash, vaqtni o'lchashning muammosi. |
| 08 | [Asimptotik notatsiya: Big-O, Ω, Θ](./08-asimptotik-notatsiya.md) | O, Omega, Theta matematik ta'rifi, o'sish tartiblari, eng keng tarqalgan murakkabliklar ierarxiyasi. |
| 09 | [Murakkablikni hisoblash: vaqt va xotira](./09-murakkablikni-hisoblash.md) | Sikllarni sanash, ichma-ich sikllar, eng yomon/o'rta/eng yaxshi holat, xotira (space) murakkabligi. |
| 10 | [Rekurrent munosabatlar va Master teorema](./10-rekurrent-master-teorema.md) | Rekursiv algoritm murakkabligi, rekursiya daraxti, almashtirish usuli, Master teorema. |
| 11 | [Amortizatsiyalangan tahlil](./11-amortizatsiyalangan-tahlil.md) | Amortized cost, aggregate / accounting / potensial usul, dinamik massiv misoli. |

### III qism — Ma'lumotlar strukturalari

| # | Bob | Mavzu |
|---|---|---|
| 12 | [Massiv va dinamik massiv](./12-massiv-dinamik-massiv.md) | Statik massiv, xotira modeli (uzluksiz), indeks, dinamik massiv, ikkilantirish strategiyasi, amortized append. |
| 13 | [Bog'langan ro'yxatlar (linked list)](./13-boglangan-royxatlar.md) | Bir/ikki tomonlama, doiraviy, tugun, qo'shish/o'chirish, massiv vs ro'yxat trade-off. |
| 14 | [Stack, Queue va Deque](./14-stack-queue-deque.md) | LIFO/FIFO, stack/queue amallari, deque, doiraviy bufer, qo'llanmalar (undo, BFS, ifoda hisoblash). |
| 15 | [Hash jadval (hash table)](./15-hash-jadval.md) | Hash funksiya, kolliziya, zanjir (chaining) va ochiq adreslash, load factor, rehashing, O(1) o'rtacha. |
| 16 | [Daraxtlar va traversal](./16-daraxtlar-traversal.md) | Terminologiya (ildiz, barg, balandlik), binar daraxt, traversal (pre/in/post-order, BFS), tasvirlash. |
| 17 | [Binar qidiruv daraxti (BST)](./17-binar-qidiruv-daraxti.md) | BST xossasi, qidiruv/qo'shish/o'chirish, in-order = saralangan, balanslanmaganlik muammosi. |
| 18 | [Balanslangan daraxtlar (AVL, Red-Black, B-tree)](./18-balanslangan-daraxtlar.md) | Balans nega kerak, aylanish (rotation), AVL, Red-Black tamoyili, B-tree va disk. |
| 19 | [Heap va Priority Queue](./19-heap-priority-queue.md) | Binar heap (min/max), massivda tasvirlash, heapify, push/pop, heapsort, priority queue qo'llanmalari. |
| 20 | [Trie va string strukturalari](./20-trie-string-strukturalari.md) | Prefiks daraxti (trie), qo'shish/qidiruv, avtoto'ldirish, xotira trade-off, suffix tushunchasi (qisqa). |
| 21 | [Graflar: tasvirlash va Union-Find](./21-graflar-union-find.md) | Graf turlari (yo'naltirilgan/vaznli), qo'shnilik matritsasi vs ro'yxati, Union-Find (disjoint set). |

### IV qism — Algoritm paradigmalari

| # | Bob | Mavzu |
|---|---|---|
| 22 | [Brute force va to'liq qidiruv](./22-brute-force.md) | Barcha variantlarni sinash, qachon yetarli, kombinatorik portlash, optimallashtirish kirish. |
| 23 | [Divide and Conquer (bo'lib hal qil)](./23-divide-and-conquer.md) | Bo'lish→hal qilish→birlashtirish, merge sort, binar qidiruv, tez ko'paytirish, murakkablik. |
| 24 | [Greedy (ochko'z) algoritmlar](./24-greedy.md) | Lokal optimal tanlov, qachon to'g'ri ishlaydi, almashtirish argumenti, klassik misollar, qachon noto'g'ri. |
| 25 | [Dinamik dasturlash (DP)](./25-dinamik-dasturlash.md) | Optimal substructure, qayta ishlatiluvchi qism-masala, memoizatsiya vs tabulatsiya, klassik DP masalalar. |
| 26 | [Backtracking (orqaga qaytish)](./26-backtracking.md) | Qaror daraxti, kesib tashlash (pruning), N-vazir, permutatsiya, Sudoku, backtracking vs brute force. |

### V qism — Klassik algoritmlar

| # | Bob | Mavzu |
|---|---|---|
| 27 | [Saralash algoritmlari](./27-saralash-algoritmlari.md) | Bubble/selection/insertion, merge/quick/heap sort, counting/radix, barqarorlik, taqqoslash chegarasi O(n log n). |
| 28 | [Qidiruv algoritmlari](./28-qidiruv-algoritmlari.md) | Chiziqli vs binar qidiruv, binar qidiruvning to'g'ri yozilishi, chap/o'ng chegara, interpolyatsion qidiruv. |
| 29 | [Graf algoritmlari I: BFS, DFS va qo'llanmalar](./29-graf-algoritmlari-1.md) | BFS (qatlamli), DFS (chuqur), topologik saralash, bog'langan komponentlar, sikl aniqlash. |
| 30 | [Graf algoritmlari II: eng qisqa yo'l va MST](./30-graf-algoritmlari-2.md) | Dijkstra, Bellman-Ford, Floyd-Warshall, minimal qoplovchi daraxt (Kruskal, Prim). |
| 31 | [String algoritmlari](./31-string-algoritmlari.md) | Pattern matching: sodda (naive), KMP, Rabin-Karp, Boyer-Moore g'oyasi, qo'llanmalar. |

### VI qism — Murakkablik nazariyasi va kapston

| # | Bob | Mavzu |
|---|---|---|
| 32 | [Hisoblash murakkabligi: P, NP va NP-to'liqlik](./32-p-np-murakkablik-nazariyasi.md) | Qaror muammolari, P vs NP, NP-to'liqlik, reduksiya, qiyin muammolar bilan ishlash (approksimatsiya, heuristika). |
| 33 | [Kapston: muammodan yechimgacha — algoritm dizayni amaliyoti](./33-kapston-algoritm-dizayni.md) | Muammoga yondashish strategiyasi, struktura va paradigma tanlash, to'liq misol, intervyu va keyingi qadamlar. |

---

## Bu kitob va boshqa kitoblar

- **Amaliyot va masalalar:** [1000 amaliy masala](../1000-masala/README.md) — bu yerdagi nazariyani mustahkamlash uchun yuzlab yechilgan masala (saralash, daraxt, graf, DP...).
- **Til asoslari:** [Python](../python/README.md) yoki [JavaScript](../js/README.md) — agar dasturlash sintaksisi yangi bo'lsa.
- **Tizim darajasidagi dizayn:** [Dasturiy arxitektura](../arxitektura/README.md) — algoritm *ichidagi* emas, butun *tizim* darajasidagi qarorlar (masshtab, kesh, mikroservis).
- **Ma'lumotlar bazasi tomoni:** [Ma'lumotlar bazasi dizayni](../db-dizayni/README.md) — indeks (B-tree), saralash va graf strukturalari bazada qanday ishlatiladi.

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
