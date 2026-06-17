# WordPress tema yaratish — 0 dan ekspertgacha

WordPress uchun professional tema (mavzu) yaratishni **noldan** o'rganadigan to'liq qo'llanma. Klassik PHP-shablon temalardan boshlab zamonaviy **block / Full Site Editing** temalar, **custom bloklar** (React/JSX), WooCommerce, xavfsizlik, i18n va tarqatishgacha. **WordPress 7.0** asosida.

> 🎯 **Klassik + zamonaviy birga.** 2026'da WordPress block/FSE standartiga o'tdi, lekin klassik temalar hali ham millionlab saytda ishlaydi. Bu kitob ikkalasini ham o'rgatadi: avval klassik poydevor (template hierarchy, The Loop, hooks), keyin block tema (theme.json, Site Editor) va o'z bloklaringiz.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan (jami 90 ta): template hierarchy daraxti, The Loop oqimi, hook tartibi, theme.json tuzilishi, block markup, custom blok edit/save va boshqalar ko'z bilan ko'rib o'rganiladi.

> 💻 **Hamma kod ishlatiladi.** Kitobdagi PHP kod `php -l` bilan, theme.json/block.json JSON-schema bilan, custom bloklar `@wordpress/scripts` build bilan, temalar esa jonli **WordPress 7.0** saytda render qilinib tekshirilgan.

---

## Talab

| Kerak | Daraja |
|---|---|
| PHP asoslari (o'zgaruvchi, funksiya, massiv, OOP) | **Shart** — avval [PHP kitobini](../php/README.md) o'qing |
| Lokal WordPress (LocalWP / Studio / XAMPP / wp-env) | Shart — 2-bobda o'rnatamiz |
| HTML/CSS asoslari | Tavsiya etiladi |
| Node.js (custom blok bo'limi uchun) | V qismda kerak bo'ladi |

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing — har qism oldingisiga tayanadi (asoslar → klassik → block/FSE → custom blok → professional).
2. Har misolni o'z lokal WordPress'ingizda **terib, aktivlashtirib ko'ring** — temani his qilish uchun.
3. Bob oxiridagi **amaliy masalalarni** o'zingiz yeching: shablon yozing, hook qo'llang, theme.json sozlang, blok yarating.
4. V qism (custom blok) uchun Node.js o'rnating va `npx @wordpress/create-block` bilan mashq qiling.

---

## I qism — Asoslar va WordPress arxitekturasi

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [WordPress va tema nima](./01-wordpress-tema-nima.md) | WordPress (CMS), tema vs plagin vs yadro farqi, tema = ko'rinish qatlami, klassik vs block tema umumiy ko'rinishi. |
| 02 | [Lokal muhit va birinchi minimal tema](./02-lokal-muhit-birinchi-tema.md) | Lokal WP o'rnatish, eng minimal tema (style.css + index.php), aktivlashtirish va birinchi render. |
| 03 | [So'rov hayoti va template hierarchy](./03-sorov-hayoti-template-hierarchy.md) | WordPress so'rovni qanday qabul qiladi va qaysi shablon faylni tanlaydi — klassik temaning yadrosi. |
| 04 | [Tema anatomiyasi va standartlar](./04-tema-anatomiyasi-standartlar.md) | style.css header, tema fayl strukturasi, Coding Standards, get_template vs get_stylesheet. |

## II qism — Klassik tema: The Loop va shablonlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 05 | [The Loop va WP_Query](./05-the-loop-wp-query.md) | Main query, The Loop, post ma'lumotlari, ikkilamchi WP_Query, pre_get_posts. |
| 06 | [Template teglar va shartli teglar](./06-template-shartli-teglar.md) | the_* vs get_the_*, is_home/is_single/is_archive, get_template_part. |
| 07 | [Shablon iyerarxiyasi amalda](./07-shablon-iyerarxiyasi.md) | index/single/page/archive/search/404 shablonlarini yozish, maxsus va custom page template. |
| 08 | [header, footer, sidebar va get_template_part](./08-header-footer-sidebar.md) | get_header/footer/sidebar, wp_head/wp_footer (majburiy), modulli bo'laklar. |
| 09 | [functions.php, hooks va theme setup](./09-functions-php-hooks.md) | Hook tizimi (action vs filter), add_theme_support, eng muhim hooklar. |

## III qism — Klassik tema: dinamik imkoniyatlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 10 | [Skript va uslublarni ulash (enqueue)](./10-asset-enqueue.md) | wp_enqueue_style/script, dependency, versiya, strategy (defer/async), localize. |
| 11 | [Navigatsiya menyulari (Walker)](./11-menyular.md) | register_nav_menus, wp_nav_menu, Walker_Nav_Menu bilan maxsus HTML. |
| 12 | [Widget'lar va dinamik sidebar](./12-widget-sidebar.md) | register_sidebar, dynamic_sidebar, klassik vs block widget, custom WP_Widget. |
| 13 | [Custom Post Type va Taxonomy](./13-custom-post-type-taxonomy.md) | register_post_type/taxonomy, show_in_rest, CPT shablonlari, tema vs plagin. |
| 14 | [Custom Fields, meta va Customizer](./14-custom-fields-customizer.md) | Post meta, register_post_meta, block bindings API, Customizer vs Site Editor. |

## IV qism — Zamonaviy Block tema (FSE)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 15 | [Block temaga kirish](./15-block-temaga-kirish.md) | Block tema NIMA va NEGA (FSE), fayl strukturasi, minimal block tema. |
| 16 | [theme.json I: settings](./16-theme-json-settings.md) | version 3, color/typography/spacing/layout settings, global vs per-block. |
| 17 | [theme.json II: styles](./17-theme-json-styles.md) | styles root/elements/blocks, preset reference, custom CSS — theme.json CSS generatsiyasi. |
| 18 | [Block templates va template parts](./18-block-templates-parts.md) | templates/ va parts/ block markup, template-part bloki, query loop. |
| 19 | [Global styles va style variations](./19-global-styles-variations.md) | Site Editor styles, styles/ variations, section/color/typography variations. |
| 20 | [Block patterns](./20-patterns.md) | patterns/ papka, register_block_pattern, synced/unsynced, pattern overrides. |
| 21 | [Site Editor va hybrid temalar](./21-site-editor-hybrid.md) | Site Editor workflow, navigation bloki, klassik→block bosqichma-bosqich ko'chish. |

## V qism — Custom bloklar (React/JSX)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 22 | [Custom blok yaratish asoslari](./22-block-dev-asoslari.md) | @wordpress/scripts, block.json, register_block_type, build jarayoni. |
| 23 | [Edit/Save, attributes va InspectorControls](./23-edit-save-attributes.md) | edit/save (JSX), attributes, RichText, InspectorControls, block supports. |
| 24 | [Dinamik bloklar (render_callback)](./24-dinamik-bloklar.md) | save=null, render.php, get_block_wrapper_attributes, ServerSideRender. |
| 25 | [InnerBlocks, variations va Interactivity API](./25-innerblocks-interactivity.md) | InnerBlocks, block variations/styles, Interactivity API (data-wp-*). |

## VI qism — Professional

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 26 | [WooCommerce tema integratsiyasi](./26-woocommerce-tema.md) | add_theme_support, template override, WC hooks, block-based store. |
| 27 | [Xavfsizlik: escaping, sanitization, nonce](./27-xavfsizlik.md) | esc_*/wp_kses, sanitize_*, nonce (CSRF), $wpdb->prepare, capability. |
| 28 | [i18n/l10n va accessibility](./28-i18n-accessibility.md) | __()/_e()/_n(), text domain, .pot/.po/.mo, semantik HTML, ARIA, WCAG. |
| 29 | [Performans va tarqatish](./29-performans-tarqatish.md) | Shartli enqueue, transient kesh, child tema, Theme Check, wordpress.org/GPL. |

## VII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 30 | [Yakuniy loyiha: to'liq professional tema](./30-yakuniy-loyiha.md) | Hybrid block tema 0 dan: theme.json + templates + patterns + custom blok + i18n + xavfsizlik. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
