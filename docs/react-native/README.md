# React Native — 0 dan ekspertgacha

**React Native** bilan bitta kod bazasidan **iOS va Android** (hatto web) uchun **haqiqiy native** mobil ilovalar yaratishni **noldan** o'rgatadigan to'liq qo'llanma. Tugmadan tortib kamera, GPS, push-bildirishnoma, animatsiya va App Store/Google Play'ga chiqarishgacha. Kitob **Expo** (React Native jamoasi rasman tavsiya etgan zamonaviy framework) asosida, **Expo SDK 56 / React Native 0.85 / React 19** va **New Architecture** bilan yozilgan.

> 🎯 **Nega React Native?** JavaScript/React bilsangiz — Android va iOS uchun alohida til (Kotlin, Swift) o'rganmasdan, **bitta kod bilan** ikkala platformaga ilova chiqarasiz. Instagram, Discord, Shopify kabi ilovalar shu texnologiyada. Bu kitob sizni "Salom dunyo" dan to App Store'ga ilova joylashtirishgacha olib boradi.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan (jami 85): komponent daraxti, Flexbox layout, navigatsiya oqimi, hook hayot sikli, New Architecture (Fabric/JSI), EAS build quvuri va telefon mokaplari ko'z bilan ko'rib o'rganiladi.

> 💻 **Hamma kod ishlatiladi.** Kitobdagi TypeScript kod jonli **Expo SDK 56 + React Native 0.85** loyihada `tsc` bilan tip-tekshiruvidan o'tkazilgan; komponentlar va loyiha tuzilishi `create-expo-app` orqali tasdiqlangan.

---

## Bu kitob kim uchun?

Kitob shunday yozilganki, **maktab o'quvchisi ham tushuna oladi** — har tushuncha hayotiy o'xshatish bilan, sodda tildan boshlanadi. Oxiriga borib siz **ekspert darajadagi** mavzularni (native modullar, animatsiya, autentifikatsiya, performance, EAS bilan do'konga chiqarish) ham egallaysiz.

## Talab

| Kerak | Daraja |
|---|---|
| JavaScript asoslari (o'zgaruvchi, funksiya, massiv, obyekt, async) | **Shart** — kerak bo'lsa [JavaScript kitobini](../js/README.md) o'qing |
| React asoslari (komponent, props, state, hook) | **Juda foydali** — [React kitobi](../react/README.md). Bu kitobda ham qaytariladi |
| TypeScript asoslari | Foydali — [TypeScript kitobi](../typescript/README.md). Kitob TS ishlatadi |
| Kompyuter (Windows/macOS/Linux) + Android/iOS telefon yoki emulator | Shart — 2-bobda sozlaymiz (Expo Go bilan oson) |

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing — har qism oldingisiga tayanadi.
2. Har misolni o'z loyihangizda **terib, telefoningizda (Expo Go) ochib ko'ring** — mobilni "his qilish" uchun shart.
3. Bob oxiridagi **amaliy masalalarni** o'zingiz yeching.
4. Oxirgi bobda hamma bilimni birlashtirib **to'liq mobil ilova** quramiz.

---

## I qism — Asoslar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [React Native nima va nega kerak](./01-react-native-nima.md) | Native vs web vs hibrid, RN qanday ishlaydi, New Architecture (Fabric/JSI/Hermes), Expo nima, RN vs Flutter. |
| 02 | [Muhit sozlash va birinchi ilova](./02-muhit-birinchi-ilova.md) | Node, Expo, `create-expo-app`, Expo Go, loyiha tuzilishi (`app/`, `src/app/`), telefon/emulatorda ishga tushirish. |
| 03 | [JSX va Core komponentlar](./03-jsx-core-komponentlar.md) | JSX, `View`/`Text`/`Image`, HTML'dan farq, funksional komponent, props bilan tanishuv. |
| 04 | [Stillar: StyleSheet](./04-stillar-stylesheet.md) | `StyleSheet.create`, style prop, rang/o'lcham/spacing, CSS'dan farqlar, NativeWind eslatma. |
| 05 | [Flexbox va layout](./05-flexbox-layout.md) | Flexbox (RN'da default `column`!), `justifyContent`/`alignItems`/`flex`/`gap`, responsive, `Dimensions`. |

## II qism — UI va o'zaro ta'sir

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 06 | [Input va tugmalar](./06-input-tugma.md) | `TextInput`, `Button`, `Pressable`, `TouchableOpacity`, controlled input, bosish hodisalari. |
| 07 | [ScrollView, SafeArea, StatusBar](./07-scrollview-safearea.md) | `ScrollView`, `SafeAreaView` (safe-area-context), `StatusBar`, `Image` chuqur, `KeyboardAvoidingView`. |
| 08 | [Ro'yxatlar: FlatList](./08-royxatlar-flatlist.md) | `FlatList`, `keyExtractor`, `renderItem`, `SectionList`, refresh, cheksiz skroll, performance. |
| 09 | [State va hodisalar](./09-state-hodisalar.md) | `useState`, hodisalar, controlled forma, holatni yangilash qoidalari, immutability. |

## III qism — React chuqur

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 10 | [Props va kompozitsiya](./10-props-kompozitsiya.md) | Props, `children`, qayta ishlatiladigan komponentlar, TypeScript bilan props tiplash. |
| 11 | [useEffect va yon ta'sirlar](./11-useeffect.md) | `useEffect`, bog'liqliklar massivi, cleanup, ma'lumot yuklash, obuna/tozalash. |
| 12 | [Hooks chuqur](./12-hooks-chuqur.md) | `useRef`, `useMemo`, `useCallback`, `useContext`, qachon qaysi, performance. |
| 13 | [Custom hooks va loyiha tuzilishi](./13-custom-hooks-tuzilish.md) | O'z hooklaringiz (`useXxx`), mantiqni ajratish, papka tuzilishi, kod tashkil etish. |

## IV qism — Navigatsiya

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 14 | [Expo Router asoslari](./14-expo-router-asoslari.md) | File-based routing, `app/`, `_layout.tsx`, `Stack`, `Link`, `useRouter`, sahifalar orasida o'tish. |
| 15 | [Tabs va Drawer navigatsiya](./15-tabs-drawer.md) | `Tabs` (pastki menyu), `Drawer` (yon menyu), route guruhlari `(tabs)`, ikonkalar, nested. |
| 16 | [Dinamik marshrut va parametrlar](./16-dinamik-marshrut.md) | `[id].tsx`, `useLocalSearchParams`, parametr uzatish, catch-all, deep linking. |

## V qism — Ma'lumot va backend

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 17 | [Tarmoq va API](./17-tarmoq-api.md) | `fetch`/`axios`, `async/await`, REST API, loading/error/data holatlari, ma'lumot ko'rsatish. |
| 18 | [Lokal saqlash](./18-lokal-saqlash.md) | `AsyncStorage`, `expo-secure-store` (maxfiy), `expo-sqlite`, holatni saqlash va o'qish. |
| 19 | [Global holat: Context va Zustand](./19-global-holat.md) | Context API, cheklovlari, Zustand (zamonaviy, sodda), qachon global holat kerak. |
| 20 | [Formalar va validatsiya](./20-formalar-validatsiya.md) | Controlled formalar, validatsiya, `react-hook-form`, klaviatura boshqaruvi, xato xabarlari. |

## VI qism — Native imkoniyatlar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 21 | [Kamera, rasm va galereya](./21-kamera-rasm.md) | `expo-camera`, `expo-image-picker`, ruxsatlar (permissions), rasm yuklash va ko'rsatish. |
| 22 | [Joylashuv va xarita](./22-joylashuv-xarita.md) | `expo-location` (GPS), `react-native-maps` (`MapView`/`Marker`), ruxsat, real-vaqt joylashuv. |
| 23 | [Bildirishnoma va sensorlar](./23-bildirishnoma-sensor.md) | `expo-notifications` (push), `expo-sensors`, `expo-haptics`, qurilma imkoniyatlari. |
| 24 | [Animatsiya va gestlar](./24-animatsiya-gest.md) | `Animated`, `Reanimated` (silliq), `Gesture Handler` (surish/cho'zish), o'tishlar. |

## VII qism — Professional daraja

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 25 | [Autentifikatsiya](./25-autentifikatsiya.md) | Login/signup, token, `expo-secure-store`, himoyalangan marshrutlar, auth holati, OAuth. |
| 26 | [Testlash va debugging](./26-testlash-debugging.md) | Jest + `@testing-library/react-native`, komponent testlari, React Native DevTools, xatolarni topish. |
| 27 | [Performance, New Architecture va deploy](./27-performance-build-deploy.md) | Optimizatsiya, Hermes, Fabric/JSI, EAS Build, App Store/Google Play, EAS Update (OTA). |

## VIII qism — Kapston

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 28 | [Yakuniy loyiha: to'liq mobil ilova](./28-kapston-loyiha.md) | To'liq ilova 0 dan: navigatsiya + API + saqlash + auth + native + animatsiya + build. |

---

## Versiya haqida

Bu kitob **Expo SDK 56**, **React Native 0.85**, **React 19** va **New Architecture** (Fabric + TurboModules + JSI + Hermes) asosida yozilgan. New Architecture 2026-yilda standart — eski "bridge" butunlay olib tashlangan. Expo — React Native jamoasi yangi loyihalar uchun rasman tavsiya etgan framework.

```text
$ npx create-expo-app@latest MyApp
$ cat package.json | grep -E "expo|react-native|react"
  "expo": "~56.0.x"
  "react": "19.2.x"
  "react-native": "0.85.x"
```

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
