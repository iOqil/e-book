# Flutter & Dart — 0 dan Expertgacha (o'zbek tilida)

Bu qo'llanma sizni **mutlaqo noldan** — hech qachon kod yozmagan bo'lsangiz ham — professional mobil dasturchi darajasiga olib chiqadi. Birinchi qism **Dart** dasturlash tilini asoslaridan o'rgatadi, keyin **Flutter** bilan haqiqiy, do'konga joylasa bo'ladigan ilovalar quramiz.

> 📱 Kitob butunlay **Flutter 3.44** va **Dart 3.12** (2026, eng so'nggi turg'un versiyalar) asosida. Bu juda muhim: Dart 3 (records, pattern matching, sealed klasslar, sound null safety) va Flutter 3.44 (Material 3 standart, Impeller dvigateli) zamonaviy kodni eski darslardan butunlay farqli qiladi.

> 🎨 Har bob **SVG diagramlar** bilan boyitilgan — widget daraxti, layout cheklovlari (constraints), event loop, state oqimi, navigatsiya steki, Riverpod/Bloc ma'lumot oqimi kabi tushunchalar ko'z bilan ko'rib o'rganiladi. Jami **30 bob, 90 diagramma**.

> ✅ Kitobdagi kod **jonli Flutter 3.44.1 / Dart 3.12.1** bilan tekshirilgan — misollar `flutter analyze` va `dart run` dan toza o'tadi.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Bu kitob bir-biriga zanjir bo'lib bog'langan — Dart'ni o'rganmasdan Flutter'ga o'tib bo'lmaydi.
2. Har bir kod misolini **o'zingiz yozib, ishga tushiring**. Mobil dasturlashni faqat o'qib o'rganib bo'lmaydi — qo'l bilan yoziladi.
3. Har bob oxiridagi **Mashqlar**ni o'zingiz yeching, keyin `<details>` ichidagi yechimga qarang.
4. **Hot reload** — sizning eng yaqin do'stingiz. O'zgartiring, saqlang, natijani darhol ko'ring.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter (Windows / macOS / Linux) | Shart |
| **Oldingi dasturlash tajribasi** | **Shart emas** — 0 dan boshlaymiz |
| Flutter SDK + editor (VS Code yoki Android Studio) | Shart (01-bobda o'rnatamiz) |
| Emulyator yoki haqiqiy telefon (Android/iOS) | Shart (01-bobda sozlaymiz) |

> 💡 iOS ilovasini qurish va do'konga joylash uchun **Mac** kerak. Lekin Dart'ni va Flutter'ni o'rganish hamda Android'ga qurish uchun istalgan OS yetarli.

---

## I qism — Dart tili (0 dan)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Kirish va muhitni o'rnatish](./01-kirish-muhit.md) | mobil dasturlash nima, Flutter va Dart bilan tanishuv, SDK o'rnatish, editor, emulyator va birinchi `dart run`. |
| 02 | [Dart asoslari: o'zgaruvchi va tiplar](./02-dart-asoslari.md) | `var`/`final`/`const`, asosiy tiplar (int, double, String, bool), operatorlar, string interpolation, `print`. |
| 03 | [Boshqaruv oqimi](./03-boshqaruv-oqimi.md) | `if/else`, `switch` (expression va patternlarga kirish), `for`/`while`/`for-in` sikllari, `break`/`continue`. |
| 04 | [Funksiyalar](./04-funksiyalar.md) | parametrlar (positional, named, optional, default), arrow, anonim funksiyalar, closure, yuqori-tartibli funksiyalar. |
| 05 | [To'plamlar: List, Set, Map](./05-toplamlar.md) | ro'yxatlar, to'plamlar, lug'atlar, spread `...`, collection-if/for, iterable metodlari (`map`/`where`/`fold`). |
| 06 | [Null safety](./06-null-safety.md) | sound null safety (Dart 3 standart), nullable `?`, `!`, `??`/`??=`, `?.`, `late` — "null xatosi"ni butunlay yo'qotish. |
| 07 | [OOP — obyektga yo'naltirilgan dasturlash](./07-oop-asoslari.md) | klass, konstruktor (named/factory), getter/setter, inheritance, `abstract`, interface, `mixin`, enhanced `enum`. |
| 08 | [Dart 3 zamonaviy imkoniyatlari](./08-dart3-zamonaviy.md) | records, pattern matching va destructuring, sealed klasslar, class modifiers (`base`/`interface`/`final`/`sealed`), exhaustive switch, generics, exceptions. |
| 09 | [Asinxron Dart](./09-asinxron-dart.md) | `Future`, `async`/`await`, `Stream`, xatolarni boshqarish, `isolate` (kirish) — Flutter'dan oldin **shart**. |

## II qism — Flutter UI asoslari

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 10 | [Flutter bilan tanishuv](./10-flutter-kirish.md) | Flutter qanday ishlaydi (widget daraxti, deklarativ UI, hot reload), birinchi ilova anatomiyasi (`runApp`, `MaterialApp`, `Scaffold`). |
| 11 | [Hamma narsa widget](./11-widgetlar-stateless.md) | `StatelessWidget`, `build`, `BuildContext`, `Text`/`Icon`/`Image`/`Container` va asosiy ko'rinish widgetlari. |
| 12 | [Layout I: Row, Column, Flex](./12-layout-row-column.md) | `Row`/`Column`, main/cross o'qlar, `MainAxisAlignment`, `Expanded`/`Flexible`/`Spacer`, `SizedBox`. |
| 13 | [Layout II: Stack va Constraints](./13-layout-stack-constraints.md) | `Stack`/`Positioned`, `Align`/`Center`/`Padding`, Flutter layout qoidalari (constraints), `Wrap`, responsive'ga kirish. |
| 14 | [Material 3, Cupertino va theming](./14-material-cupertino-theming.md) | Material 3 (standart), `ThemeData`/`ColorScheme.fromSeed`, dark mode, tipografiya, Cupertino (iOS uslubi) widgetlari. |
| 15 | [Asosiy UI widgetlar](./15-ui-widgetlar.md) | tugmalar (`ElevatedButton`/`FilledButton`/...), `TextField`, `Checkbox`/`Switch`/`Slider`, `Card`, `ListTile`. |

## III qism — Interaktivlik va holat (state)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 16 | [StatefulWidget va setState](./16-statefulwidget-setstate.md) | holat (state) nima, `StatefulWidget`, `setState`, lifecycle (`initState`/`dispose`/`didUpdateWidget`). |
| 17 | [Formalar va foydalanuvchi kiritmasi](./17-formalar-kiritma.md) | `Form`/`TextFormField`, validatsiya, `TextEditingController`, `FocusNode`, klaviatura va kiritma turlari. |
| 18 | [Ro'yxatlar va scroll](./18-royxatlar-scroll.md) | `ListView` (`builder`/`separated`), `GridView`, `SingleChildScrollView`, sliver'larga kirish, pull-to-refresh. |

## IV qism — Navigatsiya

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 19 | [Navigatsiya: Navigator 1.0](./19-navigatsiya-navigator.md) | `Navigator.push`/`pop`, ekranlar orasida o'tish, argument uzatish, dialog/bottom sheet/snackbar. |
| 20 | [go_router bilan deklarativ navigatsiya](./20-go-router.md) | marshrutlar, path/query parametrlar, `redirect`, nested/shell routes, deep linking — zamonaviy yondashuv. |

## V qism — Ma'lumotlar va tarmoq

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 21 | [Tarmoq (networking) va API](./21-networking-http.md) | `http`/`dio`, REST API chaqiruvi, JSON serializatsiya (qo'lda + `json_serializable`), `FutureBuilder`. |
| 22 | [Mahalliy ma'lumotlarni saqlash](./22-mahalliy-saqlash.md) | `shared_preferences`, `sqflite`/`drift` (mahalliy baza), fayl tizimi, `path_provider`. |
| 23 | [Stream va reaktiv UI](./23-stream-reaktiv.md) | `StreamBuilder`, real-vaqt ma'lumot, Firebase'ga qisqa kirish (Firestore/Auth tushunchasi). |

## VI qism — State management (professional)

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 24 | [Provider va InheritedWidget](./24-provider.md) | nega global state kerak, `InheritedWidget`, `Provider`/`ChangeNotifier`, `Consumer`/`context.watch`. |
| 25 | [Riverpod (3.x)](./25-riverpod.md) | providerlar, `Notifier`/`AsyncNotifier`, codegen (`riverpod_generator`), dependency injection va test. |
| 26 | [Bloc va Cubit](./26-bloc-cubit.md) | hodisa→holat oqimi, `flutter_bloc`, `Cubit`, `BlocProvider`/`BlocBuilder` — va qaysi yondashuvni tanlash. |

## VII qism — Pro daraja va ishlab chiqarish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 27 | [Animatsiya](./27-animatsiya.md) | implicit (`AnimatedContainer`/`Hero`), explicit (`AnimationController`/`Tween`), curve'lar, `Lottie`/`Rive` (qisqa). |
| 28 | [Platforma, paketlar va moslashuv](./28-platforma-paketlar.md) | pub.dev, platform channels (kirish), kamera/joylashuv/ruxsatlar, responsive/adaptive (`LayoutBuilder`/`MediaQuery`), i18n, accessibility. |
| 29 | [Testing, debugging va ishlab chiqarish](./29-testing-performance.md) | unit/widget/integration test, DevTools, performance (Impeller, rebuild profiling), build/release (APK/AAB/iOS), signing, do'konga joylash. |

## VIII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 30 | [Yakuniy loyiha: to'liq ilova](./30-kapston-loyiha.md) | o'rgangan hammasini birlashtirib — navigatsiya + state management (Riverpod) + REST API + mahalliy baza + test — noldan to'liq, professional mobil ilova quramiz. |

---

## Flutter va Dart — bir og'iz (kontekst uchun)

**Dart** — Google yaratgan, mijozga (client) yo'naltirilgan zamonaviy dasturlash tili. U tez (AOT kompilyatsiya), xavfsiz (sound null safety) va o'rganish oson. **Flutter** — shu Dart tilida yozilgan UI freymvorki: **bitta kod bazasidan** Android, iOS, web va desktop uchun ilova quradi. Flutter'ning yuragida bitta g'oya yotadi: *"hamma narsa — widget"*. Tugma ham, oraliq ham, butun ekran ham — hammasi widget, va siz ularni Lego kabi birlashtirib interfeys quryapsiz.

Nega Flutter? Chunki bitta jamoa, bitta til, bitta kod — va u **haqiqiy native tezlikda** ishlaydi (Impeller dvigateli to'g'ridan-to'g'ri GPU bilan chizadi). Bugun Flutter mobil bozorda eng tez o'sayotgan texnologiyalardan biri.

> Bu kitob Flutter'ni "tayyor kod ko'chirish" sifatida emas, balki **har bir widget nega shunday ishlashini tushunib** quradigan dasturchi sifatida o'rgatadi.

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
