# Laravel — 0 dan Expertgacha (o'zbek tilida)

Bu kitob **PHP'ni biladigan** o'quvchini **Laravel 13** (PHP 8.4) bo'yicha 0 dan ekspert darajasiga olib chiqadi. Har bobda: sodda nazariya → `php artisan` bilan ishlaydigan kod misollari → **20 ta mashq** (o'zingiz bajarasiz). Jami 24 bob, 480 mashq.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan — MVC oqimi, request quvuri, Eloquent munosabatlari, N+1 muammosi, queue va deploy kabi tushunchalar ko'z bilan ko'rib o'rganiladi.

> **Qoida:** Laravel o'qib emas — **qilib** o'rganiladi. Har bir artisan buyrug'ini o'z kompyuteringizda tering, har misolni ishga tushiring. Bu kitob **zamonaviy slim struktura** (Laravel 11+) konvensiyasiga mos — eski `Kernel.php`'li darsliklardan farqli.

> ℹ️ Bu kitob siz PHP asoslarini (OOP, klasslar, composer) bilasiz deb hisoblaydi. PHP yangi bo'lsa, avval [PHP — Mutlaqo Noldan Boshlovchilar Uchun](../php/README.md) kitobini o'qing.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. 2-bobda muhitni (PHP 8.4, Composer, baza) o'rnatib, har misolni o'z loyihangizda sinang.
3. Har bob oxiridagi **20 ta mashqni** o'zingiz bajaring — kodni ko'chirib qo'yish bilan Laravel o'rganilmaydi.
4. Diagrammalar arxitekturani tezroq singdiradi — ularga e'tibor bering.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter (Windows / macOS / Linux) | Shart |
| PHP 8.4 + Composer (2-bobda o'rnatamiz) | Shart |
| Baza (MySQL yoki SQLite) | Shart |
| PHP asoslari (OOP, composer) | **Shart** |
| Oldingi Laravel tajribasi | Shart emas |

---

## I qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Laravel nima va nega kerak?](./01-laravel-nima.md) | Framework nima va nega kerakligini, Laravel'ning afzalliklarini, MVC arxitekturasini (route → controller → model/view → javob), Laravel beradigan tayyor vositalarni hamda ekosistemani o'rganasiz. |
| 02 | [O'rnatish va muhit](./02-ornatish-muhit.md) | Laravel muhitini (PHP 8.4, Composer, baza) tayyorlash, loyiha yaratish, `artisan serve`, slim 11+ struktura va `.env` sozlamalarini o'rganasiz. |
| 03 | [Routing — marshrutlash](./03-routing.md) | URL'ni kodga ulashni: `routes/web.php`, GET/POST/PUT/PATCH/DELETE, closure va controller, route parametrlari, named route va `route()` helper, prefix/middleware guruhlari, `route:list` va fallback'ni o'rganasiz. |
| 04 | [Controllers (kontrollerlar)](./04-controllers.md) | Mantiqni route faylidan ajratib, controller klasslarga ko'chirishni; `make:controller`, `Route::resource` (7 CRUD metod), invokable, dependency injection va route model binding'ni o'rganasiz. |
| 05 | [Blade shablonlari](./05-blade.md) | Blade shablon tizimida HTML'ni xavfsiz, tartibli va takrorsiz yozishni — `{{ }}` avtomatik escape, `@if`/`@foreach`/`@forelse`, `$loop`, layout komponenti (`x-layout` + slot + `@props`) va `@csrf`/`@auth`/`@can` direktivalarini o'rganasiz. |
| 06 | [Request va Response](./06-request-response.md) | Foydalanuvchi yuborgan ma'lumotni Request obyekti orqali xavfsiz olish va to'g'ri Response (view, JSON, redirect) qaytarishni: `@csrf`, `old()` bilan formani qayta to'ldirish, flash xabar va status kodlarni o'rganasiz. |

## II qism — Ma'lumotlar bazasi va Eloquent

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 07 | [Database va migratsiyalar](./07-database-migratsiya.md) | Baza strukturasini kod bilan boshqarishni: `.env` sozlash, migration ("baza versiya nazorati"), schema builder, ustun turlari, foreign key (constrained + cascade), `migrate`/`rollback`/`fresh` va indekslarni o'rganasiz. |
| 08 | [Eloquent ORM — asoslar](./08-eloquent-asos.md) | Eloquent ORM bilan baza ustida qo'lda SQL yozmasdan ishlash: model yasash, CRUD (create/find/where/update/delete), mass assignment xavfsizligi (`$fillable`), timestamps, casts, Tinker va soft deletes. |
| 09 | [Eloquent munosabatlari](./09-eloquent-munosabat.md) | Eloquent munosabatlarini: `hasOne`, `hasMany`, `belongsTo`, `belongsToMany` (pivot jadval, attach/detach/sync, withPivot), `hasManyThrough` va polimorf (morphMany/morphTo) bog'lanishlarni hamda N+1 muammosiga kirishni o'rganasiz. |
| 10 | [Query Builder va ilg'or Eloquent](./10-query-builder-ilgor-eloquent.md) | Query Builder, N+1 muammosi va eager loading (`with`/`load`), scope'lar, accessor/mutator va casts, `withCount`/`whereHas` hamda katta ma'lumotni `chunk`/`cursor` bilan qayta ishlashni o'rganasiz. |
| 11 | [Seeder, Factory va Tinker](./11-seeder-factory-tinker.md) | Namuna ma'lumotni qo'lda emas, kod bilan to'ldirish: Factory bilan soxta-real qatorlar yasash (Faker, state, relation), Seeder bilan bazani ekish va Tinker'da jonli sinashni o'rganasiz. |

## III qism — Forma, auth va xavfsizlik

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 12 | [Validatsiya](./12-validatsiya.md) | Foydalanuvchi ma'lumotini xavfsiz tekshirishni: `validate()` qoidalari, xatoni `@error`/`old()` bilan ko'rsatish, Form Request, custom rule va massiv/nested validatsiyani o'rganasiz. |
| 13 | [Autentifikatsiya](./13-autentifikatsiya.md) | Login/register tizimini xavfsiz qurish: starter kit/Fortify/Breeze tanlash, parol hash (bcrypt), Auth facade, `auth()->user()`, `Auth::attempt`/`login`/`logout`, `auth` middleware va `@auth`/`@guest` direktivalarini o'rganasiz. |
| 14 | [Avtorizatsiya (Gates va Policies)](./14-avtorizatsiya.md) | Tizimga kirgan foydalanuvchi har amalni qila olmasligini ta'minlash: Gates va Policies, `Gate::authorize()`, owner-based ruxsat, `@can` blade, `before()` hook, `can` middleware va rollarni o'rganasiz. |
| 15 | [Middleware](./15-middleware.md) | Middleware — so'rov controllerga yetmasdan o'tadigan "qatlamlar": tayyor (auth/throttle/CSRF), `make:middleware` bilan o'zingizniki, before/after mantiq va Laravel 11+ da `bootstrap/app.php` da ro'yxatga olishni o'rganasiz. |

## IV qism — API va kuchli imkoniyatlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 16 | [Eloquent API Resources va JSON](./16-api-resources.md) | Modelni xavfsiz, nazorat ostidagi JSON ga aylantirish: API Resource bilan maydon tanlash/qayta nomlash, Resource Collection, `paginate` (meta/links), `when`/`whenLoaded`, nested relation va data wrapping. |
| 17 | [RESTful API va Sanctum](./17-rest-api-sanctum.md) | Mobil ilova va SPA uchun token bilan himoyalangan RESTful API qurish: `install:api`, Sanctum tokenlari (`createToken`, `auth:sanctum`), versiyalash, throttle, CORS va JSON xato javoblarini o'rganasiz. |
| 18 | [File storage va upload](./18-file-storage.md) | Foydalanuvchi yuklagan fayllarni (rasm, hujjat) xavfsiz saqlash: disklar tizimi (local/public/s3), upload validatsiyasi, Storage facade, `storage:link`, private/public fayl farqi va S3-mos object storage sozlashni o'rganasiz. |
| 19 | [Mail va Notifications](./19-mail-notifications.md) | Foydalanuvchiga email va bildirishnoma yuborishni: Mailable klass, Markdown mail shablon, mail driver (log/Mailtrap/SMTP), Notification kanallari (mail/database/broadcast), o'qilmagan xabarlar va queue bilan yuborishni o'rganasiz. |
| 20 | [Queues va Jobs](./20-queues-jobs.md) | Og'ir va sekin ishlarni (email, rasm, hisobot) foydalanuvchini kutdirmasdan orqa fonda bajarishni — queue va job'larni: `make:job`, `ShouldQueue`, `dispatch`, `queue:work`, failed jobs va retry'ni o'rganasiz. |
| 21 | [Events, Listeners va Scheduling](./21-events-scheduling.md) | Hodisaga avtomatik reaksiya (Event/Listener, model Observer) va vaqt bo'yicha avtomatik ishlar (Task Scheduling) — serverda bitta cron bilan ko'plab vazifani boshqarishni o'rganasiz. |

## V qism — Professional daraja

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 22 | [Testing (Pest va PHPUnit)](./22-testing.md) | Kod ishlashiga ishonch hosil qilish va xavfsiz refactoring uchun avtomatik test yozishni: Pest va PHPUnit, feature/unit farqi, HTTP testlar, `RefreshDatabase`, factory, `actingAs` auth va TDD g'oyasini o'rganasiz. |
| 23 | [Caching va performance](./23-caching-performance.md) | Ilovani tezlashtirishni: `Cache::remember`, N+1 ni eager loading va `preventLazyLoading` bilan yo'qotish, database indeks, `select`/`chunk`/pagination, `php artisan optimize`, Redis va Telescope bilan profil qilishni o'rganasiz. |
| 24 | [Deploy va yakuniy loyiha](./24-deploy-yakuniy.md) | Laravel ilovani internetga chiqarish (deploy) va o'rgangan hamma narsani bitta to'liq loyihada jamlash: production `.env` xavfsizligi, deploy buyruqlari, Nginx, HTTPS va vazifa-menejerini noldan deploy'gacha qurishni o'rganasiz. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
