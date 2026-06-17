# WordPress plugin yozish — 0 dan Expertgacha (o'zbek tilida)

Bu kitob **PHP asoslarini biladigan** dasturchini WordPress uchun **professional, xavfsiz va kengaytiriladigan plugin** yozadigan darajaga olib chiqadi. Eng oddiy "Hello World" plugindan boshlab — hooks (action/filter), Settings API, Custom Post Type'lar, ma'lumotlar bazasi, REST API, **Gutenberg blok muharriri (React/JSX bilan)**, WooCommerce kengaytmasi, testlash va xavfsizlik auditidan — yakuniy **distribution-ready professional plugin** kapstonigacha. Hammasi **WordPress 7.0** va **PHP 8.3+** ning zamonaviy idiomida.

> 🧩 **Zamonaviy stek (2026).** Kitob faqat **joriy** idiomdan foydalanadi: WordPress **7.0**, PHP **8.3/8.4** (namespace, `match`, enum, `readonly`, tiplar), PSR-4 autoloading, blok muharriri uchun **`@wordpress/create-block`** + **`@wordpress/scripts`** (`block.json` **apiVersion 3**, JSX) va **`render.php`** (server-side render), hatto **PHP-only blok ro'yxatdan o'tkazish** (2026 yangi). Eskirgan amaliyotlar (core fayllarni tahrirlash, `mysql_*`, global funksiyalarni prefiks'siz e'lon qilish, `wp_localize_script` ni ma'lumot uchun ishlatish) faqat ❌ "shunday qilmang" sifatida ko'rsatiladi.

> ⚠️ **HALOL eslatma.** Kitobdagi **PHP kod** `php -l` (PHP 8.4) bilan sintaktik tekshirilgan, **Gutenberg blok kodi** esa `@wordpress/create-block` bilan yaratilib `npm run build` (`@wordpress/scripts`, Node 24) bilan **haqiqatan qurilgan**; `block.json`/JSON va JS `node --check` bilan tasdiqlangan. Ammo plugin **mantig'i** WordPress yadrosining funksiyalariga (`add_action`, `register_post_type`, `$wpdb` ...) tayanadi — bu funksiyalar faqat **ishlab turgan WordPress** ichida mavjud. Shuning uchun plugin'ni haqiqatan **aktivatsiya qilish, wp-admin'da ko'rish, jonli REST javoblari va WooCommerce** kabi natijalar **ishlaydigan WP saytini** talab qiladi; bu bloklar to'g'ri, lekin matnda **"o'z saytingizda sinab ko'ring"** ohangida. Lokal WordPress'ni `wp-env` yoki Docker bilan oson ko'tarasiz (02-bob).

> ℹ️ Bu kitob siz **PHP'ni** (funksiya, sinf, namespace, massiv, OOP asoslari) bilasiz deb hisoblaydi. PHP yangi bo'lsa, avval [PHP — Mutlaqo Noldan](../php/README.md), so'ng ilg'or mavzular uchun [PHP — Ekspert Darajasi](../php-expert/README.md) kitoblarini o'qing. Gutenberg boblari uchun JavaScript/JSX bilan tanishlik foydali ([JavaScript](../js/README.md)).

---

## Bu kitob nimaga o'rgatadi?

WordPress dunyodagi saytlarning katta qismini quvvatlaydi va uning kuchi — **plugin'lar**. Plugin yozishni bilsangiz, mijoz uchun istalgan funksiyani qo'sha olasiz, o'z mahsulotingizni sotishingiz yoki ochiq kodga hissa qo'shishingiz mumkin. Bu kitob sizni "tema `functions.php`'ga kod tashlaydigan" havaskordan **toza, xavfsiz, yangilanishga chidamli plugin** yozadigan muhandisga aylantiradi.

Kitob oxirida siz: o'z **Custom Post Type**'ingiz va sozlamalar sahifangizni yaratasiz, **REST API** endpoint'lari qo'shasiz, **Gutenberg blok**'larini React bilan yozasiz, **WooCommerce**'ni kengaytirasiz, plugin'ingizni **test** qilasiz, **lokalizatsiya** qilasiz va **wordpress.org**'ga tayyorlaysiz.

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. **Lokal WordPress** o'rnating (02-bob: `wp-env` yoki Docker) va `WP_DEBUG` ni yoqing — har bir misolni o'z saytingizda sinab ko'ring.
3. Har bir plugin'ni **o'zingiz tering va aktivatsiya qiling** — plugin o'qib emas, **yozib** o'rganiladi.
4. Rasmiy [Plugin Handbook](https://developer.wordpress.org/plugins/) va [Block Editor Handbook](https://developer.wordpress.org/block-editor/) — eng ishonchli ma'lumotnoma; shubha bo'lsa shularni oching.

## Talab

| Kerak | Daraja |
|---|---|
| PHP asoslari (funksiya, sinf, namespace, massiv) | **Shart** |
| WordPress'dan foydalanuvchi sifatida tanishlik | Shart |
| Lokal muhit: PHP 8.3+, MySQL/MariaDB yoki Docker | Shart (02-bobda) |
| Terminal, Composer va Node/npm | Foydali (blok va test uchun) |
| JavaScript/JSX asoslari | Foydali (Gutenberg boblari uchun) |

---

## Mundarija

### I qism — Asoslar va muhit

| # | Bob | Mavzu |
|---|---|---|
| 01 | [WordPress arxitekturasi va plugin falsafasi](./01-arxitektura-falsafa.md) | Core/tema/plugin ajratimi, so'rov hayot sikli, "yadroni o'zgartirma — hook ishlat" falsafasi, plugin nima qila oladi. |
| 02 | [Lokal muhit va asboblar](./02-lokal-muhit.md) | `wp-env` (Docker), Local/MAMP muqobillari, `WP_DEBUG`/`debug.log`, WP-CLI, IDE va Xdebug, plugin papkasi. |
| 03 | [Birinchi plugin: tuzilish va hayot sikli](./03-birinchi-plugin.md) | Plugin header, fayl tuzilishi, activation/deactivation hook, `uninstall.php`, `register_activation_hook`. |
| 04 | [Hooks: action va filter (chuqur)](./04-hooks-action-filter.md) | `add_action`/`add_filter`, prioritet va argumentlar soni, hook'ni topish, o'z `do_action`/`apply_filters` hook'laringiz. |
| 05 | [Zamonaviy PHP: namespace, autoload, OOP](./05-namespace-oop-autoload.md) | Namespace va prefiks, PSR-4 + Composer autoload, OOP boilerplate (singleton/DI konteyner), konstantalar, fayl tashkili. |

### II qism — Ma'lumot va admin

| # | Bob | Mavzu |
|---|---|---|
| 06 | [Settings API va admin sahifalar](./06-settings-api-admin.md) | `add_menu_page`/`add_options_page`, `register_setting`, sections/fields, `sanitize_callback`, settings'ni saqlash va ko'rsatish. |
| 07 | [Custom Post Type'lar](./07-custom-post-types.md) | `register_post_type`, labels, `supports`, `rewrite`/slug, `show_in_rest`, capabilities, admin ustunlar. |
| 08 | [Taxonomiyalar](./08-taxonomiyalar.md) | `register_taxonomy`, ierarxik vs teg, terms bilan ishlash, CPT bilan bog'lash, admin filtr. |
| 09 | [Meta box va custom fields](./09-meta-box-custom-fields.md) | `add_meta_box`, post meta, `save_post`, nonce, sanitize/escape, `register_post_meta` (REST + blok uchun). |
| 10 | [Ma'lumotlar bazasi: $wpdb, options, transients](./10-malumotlar-bazasi.md) | `$wpdb` (`prepare`!), `dbDelta` bilan o'z jadvaling, Options API, Transients API (keshlash), autoload nuanslari. |
| 11 | [Foydalanuvchi, rol va capabilities](./11-rollar-capabilities.md) | Rollar va capabilities, `current_user_can`, custom rol/cap, `map_meta_cap`, ko'p saytli (multisite) qisqa. |
| 12 | [Xavfsizlik asoslari: nonce, sanitize, escape](./12-xavfsizlik-asoslari.md) | Nonce (CSRF), input sanitizatsiya, output escaping (kontekst!), `$wpdb->prepare` (SQLi), XSS, capability tekshiruvi. |

### III qism — Frontend va integratsiya

| # | Bob | Mavzu |
|---|---|---|
| 13 | [Shortcode'lar](./13-shortcode.md) | `add_shortcode`, atributlar (`shortcode_atts`), ichki kontent, xavfsiz chiqish, `do_shortcode`, blok bilan taqqoslash. |
| 14 | [Skript va stillarni ulash (enqueue)](./14-enqueue-assets.md) | `wp_enqueue_script`/`style`, bog'liqliklar va versiyalash, `wp_localize_script` vs `wp_add_inline_script`, shartli ulash, `@wordpress/scripts` asset fayli. |
| 15 | [AJAX (admin-ajax va zamonaviy)](./15-ajax.md) | `wp_ajax_`/`wp_ajax_nopriv_`, nonce, `admin-ajax.php`, `fetch`, va nega zamonaviy yo'l — REST API. |
| 16 | [REST API: o'z endpoint'laringiz](./16-rest-api.md) | `register_rest_route`, `permission_callback`, argument `validate`/`sanitize`, schema, autentifikatsiya (cookie+nonce, Application Passwords). |
| 17 | [WP-Cron va fon vazifalari](./17-wp-cron.md) | `wp_schedule_event`, custom interval, `wp-cron` cheklovlari, real cron, Action Scheduler kirish, bir martalik vazifa. |
| 18 | [Email, HTTP API va keshlash](./18-email-http-cache.md) | `wp_mail` (+ HTML), HTTP API (`wp_remote_get`/`post`), tashqi API'ni keshlash (transients), `WP_Error` bilan ishlash. |

### IV qism — Blok muharriri (Gutenberg), chuqur

| # | Bob | Mavzu |
|---|---|---|
| 19 | [Blok muharririga kirish va create-block](./19-blok-kirish-create-block.md) | Blok muharriri arxitekturasi, `@wordpress/create-block`, `block.json` (apiVersion 3), `@wordpress/scripts` build, `register_block_type`. |
| 20 | [Static blok: edit, save, attributes](./20-static-blok.md) | `edit`/`save`, JSX, `attributes`, `RichText`, `useBlockProps`, `InspectorControls`, `BlockControls`, `supports`. |
| 21 | [Dynamic blok va PHP-only registratsiya](./21-dynamic-blok.md) | `render.php` (server-side render), `render_callback`, dinamik ma'lumot, PHP-only blok ro'yxatdan o'tkazish (2026). |
| 22 | [Blok variations, styles, InnerBlocks, patterns](./22-blok-kengaytmalar.md) | Block variations, block styles, `InnerBlocks`, block patterns, mavjud bloklarni filter bilan kengaytirish. |
| 23 | [Sidebar plugin, SlotFill va @wordpress/data](./23-sidebar-slotfill-data.md) | `PluginSidebar`/`registerPlugin`, SlotFill, `@wordpress/data` store, blok'dan tashqari editor UI, meta bilan bog'lash. |

### V qism — Ilg'or va sifat

| # | Bob | Mavzu |
|---|---|---|
| 24 | [i18n va lokalizatsiya](./24-i18n-lokalizatsiya.md) | Text domain, `__()`/`_e()`/`esc_html__()`, `_n()` ko'plik, `.pot`/`.po`/`.mo`, JS i18n (`wp i18n`), tarjimaga tayyorlash. |
| 25 | [Testlash: PHPUnit, wp-env, PHPCS/WPCS](./25-testlash.md) | `wp-env` test muhiti, WP PHPUnit (integration), `WP_UnitTestCase`, JS testlar, PHPCS + WordPress Coding Standards, CI. |
| 26 | [Performance va keshlash](./26-performance.md) | So'rov optimizatsiya (`WP_Query`, `meta_query` xavfi), object cache, transients, autoload tozalash, profiling (Query Monitor). |
| 27 | [WooCommerce kengaytirish (HPOS)](./27-woocommerce.md) | WooCommerce hooks, custom product data/type, checkout/email kengaytmasi, HPOS (High-Performance Order Storage) muvofiqligi. |
| 28 | [Distribution: readme.txt, SVN, yangilanish](./28-distribution.md) | `readme.txt` formati, wordpress.org SVN (assets/tags/trunk), versiyalash, plugin yangilanishi, litsenziya (GPL), xavfsizlik e'loni. |

### VI qism — Kapston

| # | Bob | Mavzu |
|---|---|---|
| 29 | [Xavfsizlik auditi (chuqur)](./29-xavfsizlik-audit.md) | Nonce hayot sikli, escaping konteksti chuqur, `prepare` naqshlari, fayl yuklash xavfsizligi, REST auth, real zaiflik naqshlari va tuzatish. |
| 30 | [Yakuniy kapston: to'liq professional plugin](./30-kapston.md) | Boshidan oxirigacha: CPT + Settings + REST + Gutenberg blok + WooCommerce hook + test + i18n + distribution-ready paket. Yo'l yakuni. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
