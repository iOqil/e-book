# SQL va MySQL — Noldan boshlovchilar uchun amaliy kitob

> 📄 **[Butun kitobni PDF formatda yuklab olish →](/pdf/sql.pdf)**

Bu kitob **hech qachon dasturlash qilmagan** odam ham tushunadigan tilda yozilgan. Har bir bobda: sodda nazariya → tayyor misollar → **20 ta masala** (o'zingiz yechasiz). Jami 25 bob, 500 masala.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan — JOIN, GROUP BY, indeks, tranzaksiya, normalizatsiya kabi tushunchalar ko'z bilan ko'rib o'rganiladi.

> **Qoida:** SQL o'qib o'rganilmaydi — **YOZIB** o'rganiladi. Har bir masalani kompyuterda o'zingiz tering. Xato chiqsa — bu yaxshi, xatodan o'rganasiz.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. 3-bobdagi **4 ta amaliyot bazasini** (kutubxona, do'kon, klinika, taksi) albatta o'rnating — butun kitob masalalari shularga asoslangan.
3. Har bob oxiridagi **20 ta masalani** o'zingiz yeching — kod misollarini ko'chirib qo'yish bilan SQL o'rganilmaydi.
4. Diagrammalar tushunchani tezroq singdiradi — ularga e'tibor bering.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter (Windows / macOS / Linux) | Shart |
| MySQL 8.0 (2-bobda o'rnatamiz) | Shart |
| Oldingi dasturlash tajribasi | **Shart emas** |

---

## I qism — Tanishuv

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Ma'lumotlar bazasi nima?](./01-malumotlar-bazasi-nima.md) | Ma'lumotlar bazasi nima va u daftar yoki Excel'dan nimasi bilan kuchli ekanini, jadval/qator/ustun/id tushunchalarini, SQL (til) bilan MySQL (dastur) farqini va klient-server modelini kutubxona misolida o'rganamiz. Bob oxirida kompyutersiz yechiladigan 20 ta qog'oz masalasi bor. |
| 02 | [MySQL'ni o'rnatish va ishga tushirish](./02-mysql-ornatish.md) | MySQL'ning server-klient arxitekturasini tushunib, uni Windows (Laragon), macOS (brew) va Linux (apt) tizimlariga o'rnatamiz, terminal hamda DBeaver orqali ulanib, birinchi SQL buyruqlarimizni bajarishni o'rganamiz. |
| 03 | [Amaliyot bazalarini tayyorlash (4 ta tizim)](./03-amaliyot-bazalari.md) | Butun kitob davomida ishlatiladigan 4 ta amaliyot bazasini (kutubxona, do'kon, klinika, taksi) yaratamiz, jadvallar orasidagi bog'lanishlarni ER-diagrammalarda ko'rib, skriptlarni bajarib tekshirishni o'rganamiz. |

## II qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 04 | [CREATE — baza va jadval yaratish](./04-create.md) | CREATE DATABASE, USE va CREATE TABLE bilan birinchi baza va jadvalimizni quramiz; PRIMARY KEY, AUTO_INCREMENT, NOT NULL, UNIQUE, DEFAULT qoidalarini hamda SHOW/DESCRIBE/DROP yordamchi buyruqlarini o'rganamiz. |
| 05 | [Ma'lumot turlari](./05-malumot-turlari.md) | Sonlar (INT, DECIMAL, FLOAT), matnlar (CHAR, VARCHAR, TEXT), sana-vaqt va maxsus turlar (ENUM, BOOLEAN, JSON) bilan tanishamiz; har bir ustunga to'g'ri tur tanlashni va pul nima uchun faqat DECIMAL'da saqlanishini o'rganamiz. |
| 06 | [INSERT — ma'lumot kiritish](./06-insert.md) | Jadvalga yangi qator qo'shishni o'rganamiz: INSERT INTO anatomiyasi, ko'p qatorli kiritish, AUTO_INCREMENT va DEFAULT qanday ishlashi, NOW() va LAST_INSERT_ID() hamda INSERT xatolarini o'qib tushunish. |
| 07 | [SELECT — ma'lumot o'qish](./07-select.md) | SQL'ning eng ko'p ishlatiladigan buyrug'i — SELECT bilan jadvaldan kerakli ustunlarni tanlab o'qishni, alias (AS) berishni, SELECT ichida hisob-kitob qilishni va DISTINCT bilan takrorlarni olib tashlashni o'rganamiz. |
| 08 | [WHERE — filtrlash](./08-where.md) | Qatorlarni shart bo'yicha filtrlashni o'rganamiz: taqqoslash operatorlari, AND/OR/NOT mantiqiy bog'lovchilari va qavslar, BETWEEN va IN, LIKE naqshlari hamda NULL bilan to'g'ri ishlash (IS NULL). |
| 09 | [ORDER BY, LIMIT, DISTINCT](./09-order-limit-distinct.md) | Natijani ORDER BY bilan saralashni, LIMIT/OFFSET bilan kesishni ("eng katta N ta" qolipi va sahifalash) hamda DISTINCT bilan takror qiymatlarni olib tashlashni o'rganamiz. |
| 10 | [Built-in funksiyalar (matn, son, sana)](./10-builtin-funksiyalar.md) | MySQL'ning tayyor funksiyalarini o'rganamiz: matn (UPPER, CONCAT, SUBSTRING), son (ROUND, CEIL, FLOOR), sana (NOW, DATEDIFF, DATE_FORMAT, TIMESTAMPDIFF), shartli qiymat (IF, CASE) va NULL bilan ishlash (IFNULL, COALESCE) — hammasi hayotiy misollarda. |

## III qism — Kuchli qurollar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 11 | [Aggregate funksiyalar va GROUP BY](./11-aggregate-group-by.md) | COUNT, SUM, AVG, MIN, MAX bilan ko'p qatordan bitta xulosa chiqarishni, "har bir ... bo'yicha" savollariga GROUP BY bilan javob berishni va guruhlarni HAVING bilan filtrlashni o'rganamiz. COUNT(*) va COUNT(ustun) orasidagi NULL farqi hamda query bajarilish tartibini ham ko'rib chiqamiz. |
| 12 | [JOIN — jadvallarni bog'lash](./12-join.md) | Bo'lingan ma'lumotni qaytadan yig'ishni — JOIN'ni o'rganamiz: ON sharti, INNER va LEFT JOIN farqi, anti-join qolipi, LEFT JOIN + WHERE tuzog'i, 3-4 jadvalli zanjirlar va JOIN + GROUP BY bilan real hisobotlar. |
| 13 | [UNION — natijalarni birlashtirish](./13-union.md) | Bir nechta SELECT natijasini bitta ro'yxatga "tagma-tag" ulaydigan UNION va UNION ALL'ni, ustun yetishmaganda NULL bilan to'ldirishni, UNION'da ORDER BY/LIMIT qoidalarini va JOIN bilan farqini o'rganamiz. |
| 14 | [Subquery — query ichida query](./14-subquery.md) | Query ichiga yana bitta query joylashni o'rganamiz: skalyar, IN-ro'yxat va correlated (EXISTS) subquery turlari, mashhur NOT IN + NULL tuzog'idan qochish hamda FROM ichidagi hosila jadval bilan ikki bosqichli hisob-kitoblar. |
| 15 | [CTE — WITH bilan ishlash](./15-cte.md) | WITH yordamida murakkab query'ni nomli, yuqoridan pastga o'qiladigan bosqichlarga bo'lishni, bir nechta CTE'ni zanjir qilishni va recursive CTE bilan jadvalsiz sonlar, kalendar hamda daraxt strukturalar hosil qilishni o'rganamiz. |
| 16 | [Window funksiyalar](./16-window-funksiyalar.md) | GROUP BY'dan farqli, qatorlarni yo'qotmasdan guruh statistikasini hisoblashni o'rganamiz: OVER va PARTITION BY, ROW_NUMBER/RANK/DENSE_RANK bilan raqamlash, LAG/LEAD, yig'ilib boruvchi summa va LAST_VALUE'dagi frame tuzog'i. |

## IV qism — Ma'lumotni boshqarish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 17 | [UPDATE va DELETE — chuqur](./17-update-delete.md) | Ma'lumotni o'zgartirish (UPDATE) va o'chirish (DELETE)ni xavfsiz ishlash odati bilan o'rganamiz: "avval SELECT" protokoli, SQL_SAFE_UPDATES kamari, NULL tuzog'i, soft delete yondashuvi va DELETE/TRUNCATE/DROP farqlari. |
| 18 | [ALTER, Constraint, Foreign Key](./18-alter-constraint-fk.md) | Tayyor jadvalni ALTER TABLE bilan buzmasdan o'zgartirishni, bazaning o'zi qo'riqlaydigan qoidalar — NOT NULL, UNIQUE, DEFAULT, CHECK constraint'larini va jadvallararo bog'lanish kafolati FOREIGN KEY'ni o'rganamiz; ota qator o'chirilganda nima bo'lishini ON DELETE (RESTRICT, CASCADE, SET NULL) bilan boshqaramiz. |
| 19 | [Tranzaksiyalar](./19-tranzaksiyalar.md) | Tranzaksiya — "yo hammasi, yo hech narsa" tamoyilini o'rganamiz: START TRANSACTION, COMMIT va ROLLBACK, autocommit rejimi, parallel ishlashda FOR UPDATE qulfi, deadlock holati va ACID xossalari. |
| 20 | [Normalizatsiya — to'g'ri schema](./20-normalizatsiya.md) | Bitta katta jadvalning kasalliklarini (takrorlash, yangilash/o'chirish/kiritish anomaliyalari), normalizatsiyaning 3 sodda qoidasini (1NF, 2NF, 3NF), bog'lanish turlarini (1:1, 1:N, N:M) va qachon ataylab takrorlash (snapshot, denormalizatsiya) to'g'ri ekanini o'rganamiz. |

## V qism — Professional daraja

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 21 | [Indekslar](./21-indekslar.md) | Indeksni kitob oxiridagi alfavit ko'rsatkich o'xshatishi bilan tushunamiz: 1 million qatorli jadvalda full scan va indeksli qidiruv farqini o'z qo'limiz bilan o'lchaymiz, B-tree daraxti, indeks ishlamaydigan tuzoqlar, kompozit indeks (chap prefiks qoidasi) va indeksning narxini o'rganamiz. |
| 22 | [VIEW, Stored Procedure, Trigger, Event](./22-view-procedure-trigger.md) | Takrorlanadigan query'larni VIEW qilib nomlab qo'yishni, parametr qabul qiladigan stored procedure yozish va CALL bilan chaqirishni, jadvaldagi o'zgarishlarga avtomatik javob beradigan trigger hamda jadval bo'yicha o'z-o'zidan ishlaydigan EVENT'larni o'rganamiz. |
| 23 | [EXPLAIN va optimizatsiya](./23-explain-optimizatsiya.md) | Sekin query'ning sababini EXPLAIN bilan ochishni o'rganamiz: type/rows/key ustunlarini o'qish, const'dan ALL'gacha shkala, va to'liq optimizatsiya sikli — sekin query → EXPLAIN → indeks → qayta o'lchash. |
| 24 | [Xavfsizlik va administratsiya](./24-xavfsizlik-admin.md) | Har ilovaga alohida foydalanuvchi yaratish va GRANT bilan minimal ruxsat berishni, SQL injection hujumi qanday ishlashini va prepared statement bilan himoyalanishni, mysqldump bilan backup/restore qilishni o'rganamiz. |
| 25 | [Yakuniy loyihalar](./25-yakuniy-loyihalar.md) | O'rganganlarimizni jamlab 3 ta to'liq tizimni noldan quramiz: talablar → schema → CREATE → ma'lumotlar → hisobot query'lari. Oxirida kitobdan keyingi yo'l xaritasi: PostgreSQL, ORM va backend tomon. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
