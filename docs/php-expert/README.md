# PHP — Ekspert Darajasi (REST API, autentifikatsiya, xavfsizlik)

> **Kimga mo'ljallangan:** PHP asoslarini ([boshlovchi kitob](../php/README.md)) o'zlashtirgan — sintaksis, OOP, PDO, formalar va sessiyalar bilan tanish — va endi **ishlab chiqarish darajasidagi** (production) backend qurishni o'rganmoqchi bo'lganlarga.
>
> **Qanday o'qiladi:** har bob bitta katta mavzuni chuqur ochadi. Avval **nazariya va sabab** (nega aynan shunday), so'ng **tekshirilgan kod** (har bir blok `php -l` va haqiqiy `curl` so'rovlari bilan sinaldi), keyin **mashqlar** (Oson / O'rta / Qiyin — ko'pchiligining yechimi bilan). Bu yerda kod shunchaki "ishlaydi" emas, balki **to'g'ri** bo'lishi muhim: status kodlar ma'noli, xato formati standart, xavfsizlik o'ylab qo'yilgan.
>
> **Eng muhim qoida:** har bir misolni o'z kompyuteringizda ishga tushiring. API ni `curl` yoki Postman bilan o'zingiz sinab ko'ring — javob status kodlarini va sarlavhalarni kuzating.

---

## Mundarija

- [01 — REST API (ekspert)](./01-rest-api.md) — REST tamoyillari, HTTP verblar va status kodlar semantikasi, front-controller marshrutlash, `php://input`, validatsiya qatlami, RFC 7807 Problem Details va to'liq CRUD REST API.
- [02 — HTTP klient: cURL va Guzzle](./02-http-client.md) — tashqi API chaqirish: native cURL (`setopt`/`exec`/`getinfo`), Guzzle (PSR-18), timeout, qayta urinish (retry) + eksponensial backoff, circuit breaker va webhook imzosini tekshirish (HMAC).
- [03 — Authorization va RBAC](./03-authorization-rbac.md) — autentifikatsiya vs avtorizatsiya, rol/ruxsat modeli (RBAC), policy/gate naqshi, guard middleware, ABAC va IDOR (broken access control) oldini olish.
- [04 — JWT va stateless auth](./04-jwt-auth.md) — stateful vs stateless autentifikatsiya, JWT tuzilishi (`header.payload.signature`), HS256 imzosini qo'lda yozish, `firebase/php-jwt`, access/refresh token tsikli va xavfsizlik tuzoqlari.
- [05 — Qat'iy tiplash va PHP 8.4 tip tizimi](./05-tip-tizimi.md) — `declare(strict_types=1)` va nega, strict vs coercive, skalyar/`?T`/union/intersection/DNF turlar, `never`/`void`/`mixed`, `false`/`true` literal turlar, `self` vs `static`, type narrowing (`instanceof`/`match (true)`/`array_is_list`) va `==` vs `===` tuzoqlari.
- [06 — readonly, Value Object va variance](./06-value-object.md) — `readonly` property/class, immutable Value Object (Money/Email/Uuid), `bcmath` bilan pul aniqligi, "withX" immutable yangilash (`__clone`), kovariantlik/kontravariantlik (Liskov) va `#[\Override]`.
- [07 — Property hooks va asymmetric visibility (8.4)](./07-property-hooks.md) — PHP 8.4 ning eng yangi imkoniyatlari: `get`/`set` property hooks, virtual property, `public private(set)` asymmetric visibility, hooks vs magic `__get` va getter/setter boilerplate'ni o'ldirish.
- [08 — Reflection, attributes va FFI](./08-reflection-attributes.md) — `ReflectionClass`/`Method`/`Property`, `#[Attribute]` bilan o'z atributingni yozish va o'qish (router/validator/DI "sehri"), Reflection cache hamda FFI bilan C kutubxonaga ulanish.
- [09 — WeakMap, SPL va reference semantikasi](./09-weakmap-spl.md) — `WeakReference`/`WeakMap` (memory-leak'siz cache), SPL interfeyslar (`ArrayAccess`/`Countable`/`Iterator`/`JsonSerializable`), SPL data strukturalar va reference/COW/GC semantikasi.
- [10 — PSR standartlari va PHP-FIG](./10-psr-standartlar.md) — PHP-FIG va interoperability, PSR-1/12 + PHP-CS-Fixer, PSR-4 autoload, PSR-3 Logger, PSR-7/17 HTTP, PSR-11 Container — paketlar almashinuvining "umumiy tili".
- [11 — HTTP xabarlari: PSR-7 va PSR-17](./11-psr7-http.md) — HTTP so'rov/javobni immutable obyekt sifatida: `ServerRequest`/`Response`/`Uri`/`Stream`, `withX` (yangi nusxa) va nega bu middleware uchun xavfsiz.
- [12 — PSR-15 middleware pipeline](./12-middleware.md) — "piyoz" (onion) modeli, `MiddlewareInterface`/`RequestHandlerInterface`, pipeline/dispatcher qurish va short-circuit (auth 401).
- [13 — PSR-11 DI konteyner qurish](./13-di-konteyner.md) — Reflection bilan autowiring, binding (interfeys→implementatsiya), singleton vs factory, aylanma bog'liqlik aniqlash va compiled konteyner.
- [14 — Routing va front controller](./14-routing.md) — front controller (bitta `index.php`), route table, parametrli path, `#[Route]` atribut-asosli routing, dispatch va 404/405.
- [15 — O'z mini-frameworkingizni yig'ish](./15-mini-framework.md) — kernel = konteyner + router + middleware + PSR-7 birga; to'liq ishlaydigan mini-app; Slim/Symfony/Laravel internals bilan solishtirish.
- [16 — Twig va xavfsiz shablon](./16-twig-shablon.md) — avtomatik escaping (XSS template-darajada), shablon merosi (`extends`/`block`), escaping konteksti (`html`/`js`/`url`) va `|raw` xavfi.
- [17 — Fayllar, oqimlar va katta ma'lumot](./17-fayllar-oqimlar.md) — stream wrappers/filters, `SplFileObject`, generator bilan katta fayl (xotira tejash), `flock`/atomik yozish, `RecursiveDirectoryIterator`, `ZipArchive`, finfo MIME va path-traversal xavfsizligi.
- [18 — Fayl formatlari, rasm va bulutli saqlash](./18-fayl-formatlari.md) — CSV chuqur, Excel (**PhpSpreadsheet**), PDF (**Dompdf**), rasm (**GD** — resize/thumbnail/optimize) va **league/flysystem** bilan bulutli saqlash (lokal + S3-mos object storage).

> **Eslatma:** bu trek bosqichma-bosqich kengaymoqda. Hozircha tayyor: **birinchi** (01-04 — REST API, HTTP klient, avtorizatsiya, JWT), **ikkinchi** (05-10 — zamonaviy PHP 8.4 tip tizimi va meta-dasturlash), **uchinchi** (11-16 — framework internals: o'z mini-frameworkingizni noldan qurish) va **amaliy I/O** (17-18 — fayllar, oqimlar, formatlar va bulutli saqlash). Keyingi to'plamlarda: sifat va testlash (PHPStan/Infection/CI), performance (OPcache/JIT/Redis) va async. Boblar mustaqil o'qilishi mumkin, lekin tartib bilan o'qish tavsiya etiladi.

---

## Talab qilinadigan tayyorgarlik

Bu kitobni boshlashdan oldin boshlovchi kitobning quyidagi boblari o'zlashtirilgan bo'lishi kerak:

- [PDO bilan bazaga ulanish](../php/29-phpdan-bazaga-ulanish.md) — prepared statement, `ERRMODE_EXCEPTION`.
- [JSON bilan ishlash va oddiy API](../php/35-json-bilan-ishlash-va-oddiy-api.md) — `json_encode` / `json_decode` asoslari.
- [Sessiyalar va login](../php/33-sessiyalar-va-login.md) — stateful autentifikatsiya modeli.
- [Xavfsizlik asoslari](../php/34-xavfsizlik-asoslari.md) — SQL injeksiya, XSS, parol hashlash.
- [Toza kod prinsiplari](../php/36-toza-kod-prinsiplari.md) — qatlamlarga ajratish, mas'uliyatlarni bo'lish.

---

[🏠 Bosh sahifa](../index.md) · [⬅️ Boshlovchi PHP kitobi](../php/README.md)
