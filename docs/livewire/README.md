# Laravel Livewire — 0 dan ekspertgacha

Laravel uchun **Livewire** bilan zamonaviy, dinamik (reaktiv) veb-interfeyslarni **deyarli JavaScript yozmasdan**, faqat PHP bilan qurishni **noldan** o'rgatadigan to'liq qo'llanma. Tugmani bosganda sahifa yangilanishi, jonli qidiruv, formalar, modal oynalar, real-vaqt yangilanishlar — bularning hammasini siz Blade va PHP bilan yasaysiz. Kitob **Livewire 4** (2026-yil yanvarda chiqqan eng so'nggi versiya) asosida, lekin **Livewire 3** farqlari ham har joyda ko'rsatib boriladi.

> 🎯 **Nega Livewire?** React yoki Vue o'rganmasdan ham zamonaviy, "jonli" sayt qurish mumkin. Livewire — Laravel dasturchisining super-kuchi: backend bilimingiz bilanoq frontend "sehrini" yaratasiz. Bu kitob sizni hisoblagichdan (counter) boshlab to'liq real-vaqt ilovagacha olib boradi.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan (jami 78 ta): so'rov-javob oqimi, wire:model bog'lanishi, komponent hayot sikli, event tarqalishi, Alpine.js ko'prigi va boshqalar ko'z bilan ko'rib o'rganiladi.

> 💻 **Hamma kod ishlatiladi.** Kitobdagi PHP `php -l` bilan sintaksis tekshiruvidan o'tgan, komponentlar esa jonli **Laravel 12 + Livewire 4** loyihada `php artisan` bilan yaratilib, brauzerda render qilinib tasdiqlangan.

---

## Bu kitob kim uchun?

Bu kitob shunday yozilganki, **maktab o'quvchisi ham tushuna oladi** — har tushuncha hayotiy o'xshatish bilan, sodda tildan boshlanadi. Lekin oxiriga borib siz **ekspert darajadagi** mavzularni (xavfsizlik, testlash, tezlik optimizatsiyasi, real-vaqt ilovalar) ham egallaysiz.

## Talab

| Kerak | Daraja |
|---|---|
| Laravel asoslari (routing, Blade, Eloquent, controller) | **Shart** — avval [Laravel kitobini](../laravel/README.md) o'qing |
| PHP asoslari (o'zgaruvchi, funksiya, massiv, OOP) | **Shart** — kerak bo'lsa [PHP kitobini](../php/README.md) ko'ring |
| HTML/CSS asoslari | Tavsiya etiladi — [HTML & CSS kitobi](../html-css/README.md) |
| JavaScript asoslari | Foydali, lekin shart emas (Alpine.js bobida o'rganamiz) |

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing — har qism oldingisiga tayanadi (asoslar → formalar → CRUD → aloqalar → tezlik → professional).
2. Har misolni o'z Laravel loyihangizda **terib, brauzerda ochib ko'ring** — Livewire'ni "his qilish" uchun shart.
3. Bob oxiridagi **amaliy masalalarni** o'zingiz yeching.
4. Oxirgi bobda hamma bilimni birlashtirib **to'liq real-vaqt ilova** quramiz.

---

## I qism — Kirish va asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Livewire nima va nega kerak](./01-livewire-nima.md) | An'anaviy web vs SPA muammosi, Livewire falsafasi (PHP bilan reaktivlik), Livewire qanday ishlaydi, v3 va v4 farqi. |
| 02 | [O'rnatish va birinchi komponent](./02-ornatish-muhit.md) | Laravel 12 + Livewire 4 o'rnatish, layout, `make:livewire`, Single-File Component (SFC). |
| 03 | [Birinchi komponent: hisoblagich](./03-birinchi-komponent.md) | Property, action, `wire:click`, `wire:model` — reaktivlikning birinchi "sehri". |
| 04 | [Komponent anatomiyasi](./04-komponent-anatomiyasi.md) | SFC vs ko'p-fayl (MFC) vs klass, fayl tuzilishi (⚡), `render()`, ildiz element, komponentni joylash, props. |

## II qism — Holat, bog'lanish va amallar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 05 | [Properties — komponent holati](./05-properties-holat.md) | Public xususiyatlar, ruxsat etilgan turlar, boshlang'ich holat, `mount()`, xavf-xatarlar. |
| 06 | [Data binding: wire:model](./06-data-binding.md) | `.live`/`.blur`/`.change` (v4 yangi semantikasi), `.debounce`/`.throttle`/`.number`/`.lazy`/`.deep`. |
| 07 | [Actions — amallar va hodisalar](./07-actions.md) | `wire:click`, parametrlar, `wire:submit`, klaviatura/hodisa modifikatorlari, magic actions. |
| 08 | [Lifecycle hooks — hayot sikli](./08-lifecycle.md) | `mount`, `boot`, `hydrate`/`dehydrate`, `updating`/`updated`, xususiyatga xos hooklar. |

## III qism — Formalar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 09 | [Formalar bilan ishlash](./09-formalar.md) | Input turlari, select/checkbox/radio/textarea, submit, reset, ko'p maydonli forma. |
| 10 | [Validatsiya](./10-validatsiya.md) | `#[Validate]`, `rules()`, real-vaqt validatsiya, xato xabarlari, custom xabar va nom. |
| 11 | [Form Objects](./11-form-objects.md) | `Livewire\Form` klassi, qayta ishlatish, validatsiyani formaga ko'chirish, `fill`/`reset`. |
| 12 | [Fayl yuklash](./12-fayl-yuklash.md) | Fayl yuklash, vaqtinchalik URL, preview, validatsiya, ko'p fayl, S3'ga saqlash. |

## IV qism — Ro'yxatlar va CRUD

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 13 | [Ma'lumot ko'rsatish va ro'yxatlar](./13-royxatlar.md) | Eloquent bilan ro'yxat, `@foreach`, `wire:key`, shartli ko'rsatish, bo'sh holat. |
| 14 | [Pagination, qidiruv va filtr](./14-pagination-qidiruv.md) | `WithPagination`, jonli qidiruv, filtr, saralash, `#[Url]` bilan holatni saqlash. |
| 15 | [Computed properties](./15-computed-properties.md) | `#[Computed]`, keshlash, `unset()`/`->forget()`, ro'yxatlarda samarali ishlatish. |
| 16 | [To'liq CRUD ilova](./16-toliq-crud.md) | Create/Read/Update/Delete, modal oyna, o'chirishni tasdiqlash, flash xabar. |

## V qism — Komponentlar o'zaro aloqasi

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 17 | [Nested (ichma-ich) komponentlar](./17-nested-komponentlar.md) | Ota-bola komponentlar, props uzatish, `#[Reactive]`, `#[Modelable]`, `wire:key`. |
| 18 | [Events — hodisalar bilan aloqa](./18-events.md) | `dispatch`, `#[On]`, brauzer hodisalari, `self`/`to`, komponentlar orasida muloqot. |
| 19 | [URL va query string](./19-url-query-string.md) | `#[Url]`, query string'da holat, `history`/`keep`, sahifalararo holat ulashish. |

## VI qism — Dinamik UI va tezlik

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 20 | [Loading va progress holatlari](./20-loading-holatlar.md) | `wire:loading`, `wire:target`, `wire:dirty`, `wire:offline`, skeleton ekranlar. |
| 21 | [Lazy, polling va SPA navigatsiya](./21-lazy-poll-navigate.md) | `#[Lazy]` + placeholder, `wire:poll` (real-vaqt), `wire:navigate` (SPA tezligi), prefetch. |
| 22 | [Alpine.js integratsiyasi](./22-alpine-js.md) | `x-data`, `$wire`, `@entangle`, `$dispatch`, JS hooklar, `@script`/`@assets`. |

## VII qism — Professional daraja

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 23 | [Xavfsizlik](./23-xavfsizlik.md) | Public xususiyat xavfi, `#[Locked]`, avtorizatsiya/policy, mass-assignment, validatsiya xavfsizligi. |
| 24 | [Testlash](./24-testing.md) | Livewire test API (`Livewire::test`, `set`/`call`/`assertSee`/`assertDispatched`), Pest bilan. |
| 25 | [Tezlik (performance) va deploy](./25-performance-deploy.md) | Optimizatsiya, kesh, lazy, asset birlashtirish, production sozlash, keng tarqalgan xatolar. |

## VIII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 26 | [Yakuniy loyiha: real-vaqt vazifa boshqaruvchi](./26-kapston-loyiha.md) | To'liq ilova 0 dan: CRUD + events + auth + qidiruv + real-vaqt yangilanish + tezlik. |

---

## Versiya haqida

Bu kitob **Livewire 4.x** (2026-yil 14-yanvarda chiqqan) va **Laravel 12 / PHP 8.4** asosida yozilgan. Livewire 4 eng katta yangiligi — **Single-File Component** (bitta faylda PHP + Blade). Livewire 3 hali ham millionlab loyihada ishlaydi, shuning uchun muhim farqlar bobma-bob `Livewire 3` eslatmalarida ko'rsatib boriladi.

```text
$ php artisan --version
Laravel Framework 12.x

$ composer show livewire/livewire | grep versions
versions : * v4.x

$ php -v
PHP 8.4.0
```

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
