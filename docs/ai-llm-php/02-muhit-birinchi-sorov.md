# 02 — Muhit va birinchi so'rov

[⬅️ Oldingi: 01 — LLM nima](./01-llm-nima.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 03 — Prompt muhandisligi ➡️](./03-prompt-muhandisligi.md)

> **Bu bobda:** kompyuteringizni AI bilan ishlashga tayyorlaymiz — PHP va Composer borligini tekshiramiz, Anthropic'ning rasmiy PHP SDK'sini (va u talab qiladigan Guzzle'ni) o'rnatamiz, API kalitini xavfsiz saqlaymiz, so'ng birinchi marta o'z PHP kodimizdan Claude'ga savol yuborib, javobini ekranga chiqaramiz. Bob oxirida sizning kompyuteringizdan haqiqiy AI bilan "salomlashgan" to'liq ishlaydigan skript bo'ladi.

---

## Kirish: nazariyadan amaliyotga

Oldingi bobda LLM (katta til modeli) nima ekanligini, token va kontekst oynasi qanday ishlashini o'rgandik. Endi gapdan ishga o'tamiz: **o'z PHP kodimizdan turib Claude'ga birinchi savolimizni yuboramiz** va uning javobini ekranda ko'ramiz.

> **Hayotiy o'xshatish.** Tasavvur qiling, chet ellik juda bilimdon maslahatchi bilan ishlamoqchisiz. U siz bilan bir xonada o'tirmaydi — boshqa shaharda. Siz unga **xat** (so'rov) yozasiz, **pochta xizmati** (internet va API) xatni yetkazadi, u o'qib **javob xati** qaytaradi. Bu bobda biz aynan shu "pochta liniyasi"ni o'rnatamiz: konvertni qanday yozish, manzilni (model nomini), parolni (API kalitni) qayerga qo'yish va javobni qanday o'qishni o'rganamiz.

Hamma narsa bitta maqsadga xizmat qiladi — **kompyuteringizdan Anthropic serverlariga** internet orqali so'rov ketsin va javob qaytsin. Bu yo'lni bir marta to'g'ri qursangiz, kitobning qolgan barcha boblari (streaming, JSON chiqish, tool use, agentlar, RAG) xuddi shu poydevor ustiga quriladi.

!!! info "Provayder haqida"
    Bu kitobda amaliy kod uchun **Claude (Anthropic)** ning rasmiy PHP SDK'sidan foydalanamiz. Lekin g'oya — "API kaliti olish, kutubxona o'rnatish, so'rov yuborish, javobni o'qish" — har qanday provayder (OpenAI, Gemini, lokal modellar) uchun bir xil. 19-bobda boshqa provayderlarga ko'chirishni ko'ramiz.

---

## 1. Talablarni tekshirish: PHP va Composer

AI bilan ishlash uchun maxsus, kuchli kompyuter **kerak emas**. Og'ir hisob-kitobni Anthropic serverlari bajaradi — sizning kompyuteringiz faqat so'rov yuboradi va javobni qabul qiladi. Bizga atigi ikki narsa kerak:

| Kerak | Versiya | Nima uchun |
|---|---|---|
| **PHP** | 8.1+ (8.4 tavsiya) | Kodimiz PHP'da yoziladi; SDK zamonaviy PHP imkoniyatlaridan (nomli argument, enum) foydalanadi |
| **Composer** | 2.x | PHP kutubxonalarini (SDK, Guzzle) o'rnatadigan menejer |

> **Hayotiy o'xshatish — Composer.** Composer — bu PHP dunyosining "ilova do'koni". Telefoningizga App Store'dan dastur o'rnatganingizdek, Composer ham boshqalar yozgan tayyor kutubxonalarni bir buyruq bilan loyihangizga yuklab oladi va versiyalarini boshqaradi. Anthropic SDK'sini ham aynan shu orqali o'rnatamiz.

### Tekshirish

Terminal (Windows'da PowerShell yoki Terminal, Mac/Linux'da Terminal) oching va quyidagilarni tering:

```bash
php -v
```

Taxminan shunday natija chiqishi kerak (versiya raqami sizda boshqacha bo'lishi mumkin):

```text
PHP 8.4.0 (cli) (built: Nov 21 2024) ( NTS Visual C++ 2019 x64 )
Copyright (c) The PHP Group
Zend Engine v4.4.0
```

Endi Composer'ni tekshiramiz:

```bash
composer --version
```

```text
Composer version 2.9.3 2025-12-30
```

Agar ikkala buyruq ham versiya raqamini ko'rsatsa — tayyorsiz, keyingi bo'limga o'ting.

!!! warning "Buyruq topilmasa"
    Agar `php` yoki `composer` "command not found" / "buyruq topilmadi" desa, demak ular o'rnatilmagan yoki tizim ularni topa olmayapti (PATH'da yo'q). Bu holda avval PHP'ni o'rnating. Eng oson yo'l — **Laragon** (Windows), **Herd** (Mac/Windows) yoki **DDEV/Docker** kabi tayyor to'plamlar; ular PHP, Composer va boshqalarini birga o'rnatadi. PHP asoslari va o'rnatish bo'yicha [PHP kitobiga](../php/README.md) qarang.

!!! note "Nega PHP 8.1+ ?"
    Anthropic'ning rasmiy SDK'si zamonaviy PHP imkoniyatlaridan (jumladan **nomli argumentlar** — `model:`, `maxTokens:`) foydalanadi. Bular PHP 8.0+ da paydo bo'lgan, lekin SDK 8.1+ ni talab qiladi. 8.4 — eng yangi va tavsiya etiladigan versiya; biz shu bilan ishlaymiz.

---

## 2. API kaliti olish

Claude'ga so'rov yuborish uchun **API kaliti** kerak. API kaliti — bu sizning shaxsiy maxfiy parolingiz; u orqali Anthropic "bu so'rov aynan sizning hisobingizdan kelyapti" deb biladi va xarajatni sizning hisobingizga yozadi.

> **Hayotiy o'xshatish — API kaliti.** API kaliti — uy kalitiga o'xshaydi. U bilan eshikni (API'ni) ochish mumkin. Kalitni begonaga bermaysiz, ko'cha o'rtasiga tashlab ketmaysiz. Agar kimdir kalitingizni topib olsa, sizning hisobingizdan so'rov yuborib, **sizning hisobingizga pul yozdirishi** mumkin. Shuning uchun kalit doim maxfiy turishi kerak.

### Qadamlar

1. Brauzerda **`console.anthropic.com`** saytiga kiring.
2. Hisob yarating (email bilan ro'yxatdan o'ting) yoki mavjud hisobingizga kiring.
3. Menyudan **API Keys** bo'limini toping va **Create Key** (yangi kalit yaratish) tugmasini bosing.
4. Kalitga nom bering (masalan, `php-kitob-test`) va yarating.
5. Chiqqan kalitni **darhol nusxalab oling** — u `sk-ant-...` bilan boshlanadi va **faqat bir marta** to'liq ko'rsatiladi. Yopilgandan keyin uni qayta ko'ra olmaysiz (faqat yangisini yaratish mumkin).

!!! danger "Kalitni HECH QACHON kodga yozmang"
    Bu — eng muhim xavfsizlik qoidasi. Kalitni `$client = new Client(apiKey: 'sk-ant-abc123...')` deb to'g'ridan kodga yozmang. Sababi: kodni GitHub'ga yuklasangiz yoki birovga bersangiz, kalit **butun dunyoga ochiq** bo'ladi. Botlar GitHub'dagi ochiq kalitlarni soniyalar ichida topib, sizning hisobingizdan minglab so'rov yuborishi mumkin. Kalitni **muhit o'zgaruvchisi** yoki **`.env` fayl** orqali beramiz (5-bo'limda ko'ramiz).

!!! tip "To'lov haqida"
    Anthropic'da odatda boshlang'ich bepul kredit beriladi, keyin esa "qancha ishlatsang, shuncha to'laysan" tartibi. Bitta savol-javob arzon (tokenlar haqida 16-bobda batafsil). O'rganish jarayonida xarajat juda kichik bo'ladi — qo'rqmang.

---

## 3. Loyiha yaratish

Endi AI loyihamiz uchun alohida papka yaratamiz. Papka — barcha fayllarimiz (kod, sozlamalar, kutubxonalar) bir joyda turishi uchun.

Terminalda:

```bash
mkdir ai-test
cd ai-test
```

Bu `ai-test` nomli papka yaratib, ichiga kiradi. Endi shu papkada loyihani sozlaymiz.

Composer loyihasini boshlashning ikki yo'li bor:

**1-yo'l — `composer init` (interaktiv, savol-javob bilan):**

```bash
composer init
```

Bu sizdan loyiha nomi, tavsifi va boshqalarni so'raydi. Boshlovchi uchun har bir savolda **Enter** bosib (standart qiymatni qoldirib) o'tib ketsangiz ham bo'ladi.

**2-yo'l — to'g'ridan o'rnatish (eng oddiy):**

Aslida `composer init` shart emas. Quyidagi bo'limda `composer require` buyrug'ini ishlatsak, Composer o'zi `composer.json` faylini yaratadi. Boshlovchi uchun **shuni tavsiya qilamiz** — keling, to'g'ridan kutubxonani o'rnatishga o'tamiz.

> **Hayotiy o'xshatish — `composer.json`.** `composer.json` — loyihangizning "xarid ro'yxati"ga o'xshaydi: unda loyihangizga qaysi kutubxonalar va qaysi versiyada kerakligi yozib qo'yiladi. Composer shu ro'yxatga qarab hammasini `vendor/` papkasiga yuklab oladi.

---

## 4. SDK o'rnatish — Anthropic SDK + Guzzle (MUHIM)

Bu — bobning eng muhim bo'limi. Ko'p boshlovchilar aynan shu yerda qoqiladi.

Anthropic'ning rasmiy PHP kutubxonasini o'rnatamiz:

```bash
composer require anthropic-ai/sdk
```

Endi **juda muhim** ikkinchi qadam — **Guzzle** ni ham o'rnatamiz:

```bash
composer require guzzlehttp/guzzle
```

Yoki ikkalasini birga:

```bash
composer require anthropic-ai/sdk guzzlehttp/guzzle
```

### Nega Guzzle SHART?

Bu savol juda muhim, chunki Guzzle'ni o'rnatishni unutsangiz, kodingiz ishlamaydi va tushunarsiz xato beradi.

> **Hayotiy o'xshatish — SDK va Guzzle.** SDK — bu "xat yozuvchi kotib": u sizning so'rovingizni Anthropic tushunadigan to'g'ri shaklga (HTTP so'rovga) keltiradi va javobni qayta sizga tushunarli obyektga aylantiradi. Lekin kotib **xatni o'zi pochtaga eltmaydi** — buning uchun "kuryer" kerak. **Guzzle** — aynan o'sha kuryer: u tayyor HTTP so'rovni internet orqali Anthropic serveriga olib boradi va javobni qaytaradi.

Texnik tilda: Anthropic SDK'si HTTP so'rovni o'zi yubormaydi. U **PSR-18** standartiga mos har qanday "HTTP mijoz"ni ishlatishga moslangan. PSR-18 — PHP hamjamiyati kelishgan umumiy standart bo'lib, "HTTP mijoz qanday ko'rinishda bo'lishi kerak"ligini belgilaydi. SDK ishga tushganda, o'rnatilgan kutubxonalar orasidan PSR-18'ga mos mijozni avtomatik izlab topadi. **Guzzle** — eng mashhur PSR-18 HTTP mijozi.

> Qisqasi: **SDK = miya (so'rovni tuzadi), Guzzle = qo'l-oyoq (so'rovni internetga yuboradi).** Ikkalasi birga kerak.

!!! danger "Guzzle bo'lmasa qanday xato chiqadi"
    Agar faqat SDK'ni o'rnatib, Guzzle'ni unutsangiz, birinchi so'rovda taxminan shunday xato olasiz:

    ```text
    No PSR-17 url factory found
    ```
    yoki
    ```text
    Could not find resource using any discovery strategy
    ```

    Bu — "men so'rovni yuboradigan kuryerni topa olmadim" degani. Yechimi bitta: `composer require guzzlehttp/guzzle`.

!!! note "Guzzle o'rniga boshqa narsa bo'ladimi?"
    Ha. Guzzle yagona variant emas — masalan `nyholm/psr7` + `symfony/http-client` juftligi ham ishlaydi. Lekin boshlovchi uchun eng oson va keng tarqalgani — **Guzzle**. Shubha bo'lsa, Guzzle'ni tanlang.

O'rnatish tugagach, papkangizda `vendor/` nomli papka va `composer.json`, `composer.lock` fayllari paydo bo'ladi. `vendor/` — barcha yuklab olingan kutubxonalar shu yerda turadi.

---

## 5. API kalitini xavfsiz saqlash (.env)

Endi 2-bo'limda olgan kalitimizni **xavfsiz** joyga qo'yamiz — kodga emas. Eng keng tarqalgan usul — **`.env` fayl**.

> **Hayotiy o'xshatish — `.env` fayl.** `.env` fayl — uy kalitini saqlaydigan **shaxsiy seyf**ga o'xshaydi. Maxfiy ma'lumotlar (API kalitlar, parollar, baza ulanishlari) shu faylda turadi. Kodingizda esa "seyfdan kalitni ol" deyiladi, kalitning o'zi kodda ko'rinmaydi. Seyfning o'zini esa hech qachon GitHub'ga yuklamaysiz.

### 5.1 `phpdotenv` kutubxonasini o'rnatish

`.env` faylni o'qish uchun mashhur `vlucas/phpdotenv` kutubxonasidan foydalanamiz:

```bash
composer require vlucas/phpdotenv
```

### 5.2 `.env` faylni yaratish

Loyiha papkasida `.env` nomli fayl yarating va ichiga kalitingizni yozing:

```text
ANTHROPIC_API_KEY=sk-ant-bu-yerga-haqiqiy-kalitingiz
```

(`sk-ant-...` o'rniga 2-bo'limda nusxalagan haqiqiy kalitingizni qo'ying. Atrofiga tirnoq qo'yish shart emas.)

### 5.3 `.gitignore` ga `.env` qo'shish (juda muhim)

Agar loyihangizni Git bilan boshqarsangiz (GitHub'ga yuklasangiz), `.env` fayl **hech qachon** repozitoriyga tushmasligi kerak. Buning uchun loyiha papkasida `.gitignore` faylini yarating (yoki mavjudiga qatorni qo'shing):

```text
/vendor/
.env
```

Bu Git'ga "`vendor/` papkani va `.env` faylni kuzatma, GitHub'ga yuklama" deydi.

!!! danger "Eng ko'p uchraydigan xavfsizlik xatosi"
    Dunyo bo'ylab dasturchilar `.env` faylni xatoan GitHub'ga yuklab, API kalitlarini oshkor qilib qo'yishadi. Botlar buni daqiqalar ichida topadi. **Doim** `.env` ni `.gitignore` ga qo'shing — bu birinchi ish bo'lsin.

!!! tip "Namuna fayl — `.env.example`"
    Odat shuki, `.env` ni yashirib, uning yonida `.env.example` nomli **kalitsiz namuna** qoldiriladi:
    ```text
    ANTHROPIC_API_KEY=
    ```
    Bu boshqalarga "bu yerda shunday o'zgaruvchi kerak" deb ko'rsatadi, lekin haqiqiy kalitni oshkor qilmaydi. `.env.example` ni `.gitignore` ga qo'shmang — u GitHub'da bo'lishi kerak.

### 5.4 `.env` siz: to'g'ridan muhit o'zgaruvchisi

`.env` fayl yagona yo'l emas. Kalitni **operatsion tizimning muhit o'zgaruvchisi** sifatida ham berish mumkin (productionda ko'pincha shunday qilinadi):

```bash
# Mac / Linux:
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows PowerShell:
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

Yoki PHP kodi ichidan `putenv('ANTHROPIC_API_KEY=...')` bilan ham o'rnatish mumkin (lekin bu holda ham kalitni kodga yozmang — masalan boshqa maxfiy manbadan o'qing).

Ikkala usulda ham kodimiz kalitni bir xil yo'l bilan o'qiydi — **`getenv('ANTHROPIC_API_KEY')`**. Bu funksiya muhit o'zgaruvchisini qaytaradi; `.env` faylni `phpdotenv` o'qib, qiymatlarni aynan muhit o'zgaruvchilariga joylaydi.

![O'rnatish oqimi: PHP+Composer dan birinchi so'rovgacha bo'lgan qadamlar](rasmlar/ai02-ornatish-oqimi.svg)

---

## 6. Birinchi so'rov — to'liq ishlaydigan skript

Hammasi tayyor. Endi **birinchi marta** Claude'ga savol yuboramiz. Loyiha papkasida `birinchi.php` nomli fayl yarating:

```php
<?php
// 1) Composer yuklagan barcha kutubxonalarni ulaymiz
require __DIR__ . '/vendor/autoload.php';

use Anthropic\Client;
use Dotenv\Dotenv;

// 2) .env fayldagi maxfiy o'zgaruvchilarni yuklaymiz
//    (endi getenv('ANTHROPIC_API_KEY') ishlaydi)
$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

// 3) Klient yaratamiz — kalitni .env dan olamiz, kodga YOZMAYMIZ
$client = new Client(apiKey: getenv('ANTHROPIC_API_KEY'));

// 4) So'rov yuboramiz: model, maksimal token, xabarlar
$message = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Salom, Claude! O\'zbek tilida bir jumlada o\'zingni tanishtir.'],
    ],
);

// 5) Javobni o'qiymiz va ekranga chiqaramiz
echo $message->content[0]->text . "\n";
```

Skriptni terminalda ishga tushiring:

```bash
php birinchi.php
```

Agar hammasi to'g'ri bo'lsa, taxminan shunday javob ko'rasiz:

```text
Salom! Men Claude — Anthropic kompaniyasi yaratgan sun'iy intellekt yordamchisiman, sizga turli savollarda yordam berishga tayyorman.
```

**Tabriklaymiz — siz o'z PHP kodingizdan birinchi marta haqiqiy AI bilan gaplashdingiz!** Endi kodning har bir qatorini tushunamiz.

### Kodni qator-qator tushunamiz

- **`require __DIR__ . '/vendor/autoload.php';`** — Composer barcha o'rnatilgan kutubxonalarni avtomatik ulaydigan "ulagich" fayl. Har bir PHP skriptimiz shu qatordan boshlanadi. `__DIR__` — joriy fayl turgan papka manzili.
- **`Dotenv::createImmutable(__DIR__)->load();`** — `.env` faylni o'qib, ichidagi o'zgaruvchilarni muhitga yuklaydi. Shundan keyin `getenv()` ular qiymatini qaytaradi. (Agar muhit o'zgaruvchisini boshqa yo'l bilan bergan bo'lsangiz, bu qatorlar shart emas.)
- **`new Client(apiKey: getenv('ANTHROPIC_API_KEY'))`** — SDK klientini yaratamiz. `apiKey:` — bu **nomli argument** (PHP 8.0+ imkoniyati: argument tartibini emas, nomini yozamiz). Kalit `.env` dan keladi.
- **`$client->messages->create(...)`** — bu asosiy buyruq: Claude'ga xabar yuboradi. Uchta majburiy narsa: `model` (qaysi model), `maxTokens` (javob eng ko'pi bilan necha tokendan iborat bo'lsin), `messages` (xabarlar ro'yxati).
- **`messages: [['role' => 'user', 'content' => '...']]`** — xabarlar massivi. Har xabarda `role` (kim gapiryapti — `user` siz, `assistant` model) va `content` (matn) bo'ladi. Birinchi xabar **doim `user`** bo'lishi kerak.
- **`$message->content[0]->text`** — javobning matni. Nega `[0]` va `->text`? Buni keyingi bo'limda batafsil ko'ramiz.

![So'rov-javob oqimi: Client dan messages->create orqali API ga, javob matnigacha](rasmlar/ai02-sorov-javob.svg)

!!! note "Nomli argument (`maxTokens:`) — camelCase"
    Diqqat qiling: SDK'da parametr nomi **`maxTokens`** (katta `T` bilan, camelCase), `max_tokens` emas. Bu — PHP SDK'sining uslubi. Anthropic'ning to'g'ridan HTTP API'sida `max_tokens` bo'ladi, lekin biz SDK ishlatganimiz uchun `maxTokens:` yozamiz. SDK bu kabi nomlarni o'zi to'g'ri shaklga o'giradi.

---

## 7. Javob strukturasini tushunish

Yuqorida `$message->content[0]->text` yozdik. Endi `$message` aslida nima ekanligini ochib beramiz — bu kitobning qolgan qismida juda ko'p kerak bo'ladi.

`$message` — oddiy matn **emas**, balki **boy obyekt**. U javob matnidan tashqari ko'p foydali ma'lumotni o'z ichiga oladi:

```php
$message->content      // javob bloklari massivi (eng muhim qism)
$message->stopReason   // model nega to'xtadi (masalan "end_turn")
$message->usage        // sarflangan tokenlar (xarajatni hisoblash uchun)
$message->model        // qaysi model javob berdi
$message->role         // har doim "assistant"
$message->id           // bu javobning noyob raqami
```

### Nega `content` — massiv?

Eng muhim tushuncha shu: **`$message->content` bitta matn emas, balki "bloklar" massivi.** Nega?

> **Hayotiy o'xshatish — bloklar.** Claude'ning javobini gazeta sahifasiga o'xshating. Sahifada faqat matn bo'lmasligi mumkin: bir blok — matn, boshqasi — rasm, yana biri — jadval. Claude ham javobni bloklarga bo'lib qaytaradi. Oddiy savol-javobda odatda **bitta** matn bloki bo'ladi — shuning uchun `content[0]` (birinchi blok) yozamiz. Lekin keyinroq (tool use, fikrlash bloklari) bir nechta turli blok bo'lishi mumkin.

Har blokda `type` (turi) bo'ladi. Matn bloki uchun `type === 'text'`, va matn `->text` ichida turadi. Shuning uchun ishonchli yozuvi — bloklarni aylanib chiqib, faqat matn bloklarini olish:

```php
// Barcha matn bloklarini xavfsiz o'qish
foreach ($message->content as $block) {
    if ($block->type === 'text') {
        echo $block->text;
    }
}
echo "\n";
```

Oddiy holatlarda `$message->content[0]->text` ham yetarli (birinchi blok matn bo'lganligiga ishonchingiz komil bo'lsa). Lekin `foreach` bilan yozish — har doim xavfsizroq odat.

### `stopReason` — model nega to'xtadi?

`$message->stopReason` modelning javobni nega yakunlaganini aytadi. Eng ko'p uchraydigani:

| `stopReason` | Ma'nosi |
|---|---|
| `end_turn` | Model fikrini tabiiy yakunladi (normal holat) |
| `max_tokens` | `maxTokens` chegarasiga yetdi — javob **yarmida uzilgan** bo'lishi mumkin |
| `tool_use` | Model tooldan foydalanmoqchi (9-bobda ko'ramiz) |
| `stop_sequence` | Siz belgilagan to'xtash so'ziga yetdi |

!!! tip "`max_tokens` bo'lsa — chegarani oshiring"
    Agar `stopReason === 'max_tokens'` bo'lsa, javob to'liq tugamagan, ya'ni `maxTokens` qiymati kichik bo'lgan. Uni oshiring (masalan `maxTokens: 4096`). Lekin esda tuting — `maxTokens` faqat **chegara**; model undan kamroq ishlatishi mumkin va siz faqat haqiqatda ishlatilgan token uchun to'laysiz.

### `usage` — tokenlar va xarajat

`$message->usage` shu so'rovda nechta token sarflanganini ko'rsatadi:

```php
echo "Kirish tokenlari: "  . $message->usage->inputTokens  . "\n";
echo "Chiqish tokenlari: " . $message->usage->outputTokens . "\n";
```

- **`inputTokens`** — siz yuborgan so'rov (savol + system prompt) necha token edi.
- **`outputTokens`** — model qaytargan javob necha token.

Bu raqamlar muhim, chunki **xarajat shularga bog'liq**. Token va narx haqida 16-bobda batafsil to'xtalamiz; hozircha shuni biling: chiqish tokenlari kirishga qaraganda qimmatroq turadi.

![Message obyekti tuzilishi: content bloklari, stopReason va usage](rasmlar/ai02-javob-struktura.svg)

---

## 8. System prompt qo'shish — modelga rol berish

Hozircha biz faqat **savol** (`user` xabari) yubordik. Lekin ko'pincha modelga "qanday yordamchi bo'lishi"ni oldindan aytib qo'yish kerak. Buning uchun **system prompt** ishlatiladi.

> **Hayotiy o'xshatish — system prompt.** Yangi ishchini ishga olganingizni tasavvur qiling. Unga birinchi kuni **lavozim yo'riqnomasi** berasiz: "Sen mijozlarga yordam beradigan operator'san. Doim xushmuomala bo'l, qisqa javob ber, o'zbek tilida gaplash." Bu yo'riqnoma har bir mijoz savolidan oldin emas, bir marta beriladi va u butun ish davomida amal qiladi. **System prompt** — aynan shu yo'riqnoma: u modelga rolini, qoidalarini va uslubini belgilaydi.

System prompt — `messages` ichidagi alohida rol **emas**, balki `create()` ning alohida `system:` parametri:

```php
<?php
require __DIR__ . '/vendor/autoload.php';

use Anthropic\Client;
use Dotenv\Dotenv;

Dotenv::createImmutable(__DIR__)->load();
$client = new Client(apiKey: getenv('ANTHROPIC_API_KEY'));

$message = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    // Modelga rol va qoidalar beramiz:
    system: 'Sen foydali PHP yordamchisisan. Doim o\'zbek tilida, qisqa va aniq javob ber. Iloji bo\'lsa kod misol keltir.',
    messages: [
        ['role' => 'user', 'content' => 'PDO nima?'],
    ],
);

echo $message->content[0]->text . "\n";
```

`system:` qo'shilganda, model PDO haqida aynan siz so'ragan uslubda — o'zbekcha, qisqa, kod misolli — javob beradi. System prompt'ni o'zgartirib, modelni mutlaqo boshqacha "shaxs"ga (matematika o'qituvchisi, SQL eksperti, til tarjimoni) aylantirishingiz mumkin.

!!! note "System prompt vs user xabar"
    - **System** = "kim bo'l va qanday gaplash" (rol, qoida, uslub) — bir marta beriladi.
    - **User** = aniq savol/topshiriq — har gal o'zgaradi.

    System prompt'ni mohirona yozish — alohida san'at. Buni keyingi bobda ([03 — Prompt muhandisligi](./03-prompt-muhandisligi.md)) chuqur o'rganamiz.

---

## 9. Model tanlash — Opus, Sonnet, Haiku

Yuqorida hamma misollarda `model: 'claude-opus-4-8'` yozdik. Lekin Claude'ning bir nechta modeli bor va ular tezlik, aql va narx bo'yicha farq qiladi:

| Model | ID | Kontekst | Qachon ishlatish |
|---|---|---|---|
| **Claude Opus 4.8** (eng kuchli) | `claude-opus-4-8` | 1M token | Murakkab masala, chuqur fikrlash, eng yuqori sifat |
| **Claude Sonnet 4.6** (balans) | `claude-sonnet-4-6` | 1M token | Tezlik va aql balansi — ko'p vazifaga eng yaxshi tanlov |
| **Claude Haiku 4.5** (eng tez) | `claude-haiku-4-5` | 200K token | Oddiy, ko'p sonli, tez/arzon vazifalar |

> **Hayotiy o'xshatish — modellar.** Modellarni transport turlariga o'xshating. **Opus** — kuchli, qimmat, eng murakkab yo'lni bosib o'tadigan yuk mashinasi. **Sonnet** — kundalik ishga juda mos yengil avtomobil. **Haiku** — tez va arzon mototsikl, kichik topshiriqlar uchun. Vazifa qanchalik murakkab bo'lsa, shunchalik kuchli modelni tanlaysiz; oddiy ishga kuchli (va qimmat) modelni sarflash shart emas.

Modelni almashtirish juda oson — faqat `model:` qiymatini o'zgartiring:

```php
$message = $client->messages->create(
    model: 'claude-haiku-4-5',   // tez va arzon variantga o'tdik
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Bugun kayfiyat qanday ekanini qisqa so\'ra']],
);
```

!!! warning "Model ID'siga sana qo'shmang"
    Model ID aynan jadvaldagidek bo'lishi kerak: `claude-opus-4-8` — to'g'ri. `claude-opus-4-8-2026-01-15` kabi sana qo'shilgan ko'rinish bu kitobda **noto'g'ri** va `404` (model topilmadi) xatosiga olib keladi. Sana qo'shmang.

---

## 10. Keng tarqalgan xatolar va ularni hal qilish

Birinchi so'rovda ko'pincha shu xatolar uchraydi. Quyidagi jadval sizni vaqt yo'qotishdan saqlaydi:

| Xato | Sabab | Yechim |
|---|---|---|
| `No PSR-17 url factory found` / `Could not find resource using any discovery strategy` | **Guzzle o'rnatilmagan** | `composer require guzzlehttp/guzzle` |
| `401 Unauthorized` / `authentication_error` | API kaliti yo'q, noto'g'ri yoki bo'sh | `.env` da kalit borligini, `getenv()` qiymat qaytarayotganini tekshiring |
| `404` / `model: ... not found` | Model nomi noto'g'ri (masalan sana qo'shilgan) | Aniq ID: `claude-opus-4-8` (sanasiz) |
| `Class "Anthropic\Client" not found` | `vendor/autoload.php` ulanmagan yoki SDK o'rnatilmagan | Skript boshida `require __DIR__ . '/vendor/autoload.php';` borligini va `composer require anthropic-ai/sdk` bajarilganini tekshiring |
| `getenv()` `false` qaytaryapti | `.env` yuklanmagan | `Dotenv::createImmutable(__DIR__)->load();` chaqirilganini, `.env` to'g'ri papkada ekanini tekshiring |

> **Kalit yo'qligini oldindan tekshirish.** Skript boshida kalit borligini tekshirib, foydalanuvchiga aniq xabar berish — yaxshi odat:

```php
$kalit = getenv('ANTHROPIC_API_KEY');
if (!$kalit) {
    exit("Xato: ANTHROPIC_API_KEY topilmadi. .env faylni tekshiring.\n");
}
$client = new Client(apiKey: $kalit);
```

!!! tip "Xatolarni yashirmang, o'qing"
    Boshlovchilar ko'pincha xatoni ko'rib qo'rqib ketadi. Aslida xato matni — sizning **eng yaxshi do'stingiz**: u muammoni aniq aytadi. "401" ko'rsangiz — kalit muammosi; "PSR" yoki "discovery" so'zini ko'rsangiz — Guzzle muammosi; "404" — model nomi. Xatoni o'qishni o'rganish — eng muhim dasturchilik ko'nikmasi. Xatolarni professional boshqarish (try/catch, retry) haqida [08-bobda](./08-xatolar-ishonchlilik.md) batafsil ko'ramiz.

---

## 11. To'liq misol: AI yordamchidan savol so'rash (CLI)

Endi o'rganganlarimizni birlashtiramiz: terminaldan savol qabul qilib, Claude'ga yuboradigan va javobni chiroyli ko'rsatadigan **to'liq CLI skripti**. `sora.php` nomli fayl yarating:

```php
<?php
require __DIR__ . '/vendor/autoload.php';

use Anthropic\Client;
use Dotenv\Dotenv;

// 1) .env yuklaymiz
Dotenv::createImmutable(__DIR__)->load();

// 2) Kalit borligini tekshiramiz
$kalit = getenv('ANTHROPIC_API_KEY');
if (!$kalit) {
    exit("Xato: ANTHROPIC_API_KEY topilmadi. .env faylni tekshiring.\n");
}

// 3) Savolni terminal argumentidan yoki standart savol
//    Ishlatish: php sora.php "Sizning savolingiz"
$savol = $argv[1] ?? 'PHP nima ekanini bir jumlada tushuntir.';

// 4) Klient yaratamiz
$client = new Client(apiKey: $kalit);

echo "Savol: {$savol}\n";
echo "O'ylanmoqda...\n\n";

// 5) So'rov yuboramiz (system prompt bilan rol beramiz)
$message = $client->messages->create(
    model: 'claude-opus-4-8',
    maxTokens: 1024,
    system: 'Sen o\'zbek tilida javob beradigan foydali yordamchisan. '
          . 'Aniq, tushunarli va do\'stona bo\'l.',
    messages: [
        ['role' => 'user', 'content' => $savol],
    ],
);

// 6) Barcha matn bloklarini xavfsiz chiqaramiz
echo "Javob:\n";
foreach ($message->content as $block) {
    if ($block->type === 'text') {
        echo $block->text;
    }
}
echo "\n\n";

// 7) Sarflangan tokenlarni ko'rsatamiz
echo "---\n";
echo "Kirish: {$message->usage->inputTokens} token · "
   . "Chiqish: {$message->usage->outputTokens} token · "
   . "To'xtash sababi: {$message->stopReason}\n";
```

Ishga tushirish:

```bash
php sora.php "Composer nima va nima uchun kerak?"
```

Natija taxminan shunday ko'rinadi:

```text
Savol: Composer nima va nima uchun kerak?
O'ylanmoqda...

Javob:
Composer — PHP uchun bog'liqliklar (kutubxonalar) menejeri. U boshqalar
yozgan tayyor kodni bir buyruq bilan loyihangizga o'rnatadi va versiyalarini
boshqaradi, shunda hamma narsani qo'lda yuklab o'tirmaysiz.

---
Kirish: 38 token · Chiqish: 52 token · To'xtash sababi: end_turn
```

Bu skript — kitobning qolgan boblari uchun **poydevor**. Unga keyinroq streaming, suhbat tarixi, tool use va boshqalarni qo'shib boramiz. Hozir esa siz uni ishlatib, har xil savollar bilan o'ynab ko'ring — bu AI'ni "his qilish"ning eng yaxshi yo'li.

!!! example "Sinab ko'ring"
    `sora.php` ni ishga tushirib, bir necha xil savol bering: oddiy fakt savoli, kod yozishni so'rash, biror narsani tushuntirishni so'rash. `system:` matnini o'zgartiring (masalan, "Sen quvnoq matematika o'qituvchisisan") va javob uslubi qanday o'zgarishini kuzating. `model:` ni `claude-haiku-4-5` ga almashtirib, tezlik farqini sezing.

---

## Xulosa

- AI bilan ishlash uchun kuchli kompyuter **kerak emas** — og'ir ish serverda bajariladi; sizga **PHP 8.1+ (8.4 tavsiya)** va **Composer** yetarli (`php -v`, `composer --version` bilan tekshiring).
- Anthropic'ning rasmiy SDK'sini o'rnatishda **Guzzle SHART**: `composer require anthropic-ai/sdk guzzlehttp/guzzle`. SDK so'rovni tuzadi (miya), Guzzle uni internetga yuboradi (kuryer — PSR-18 HTTP mijoz). Guzzle bo'lmasa "discovery" / "PSR-17 url factory" xatosi chiqadi.
- API kaliti `console.anthropic.com` dan olinadi va **hech qachon kodga yozilmaydi** — `.env` fayl (`vlucas/phpdotenv`) yoki muhit o'zgaruvchisi orqali beriladi, `.env` esa `.gitignore` ga qo'shiladi.
- Birinchi so'rov: `new Client(apiKey: getenv(...))` → `$client->messages->create(model:, maxTokens:, messages:)`. Parametrlar **nomli va camelCase** (`maxTokens`, `max_tokens` emas).
- Javob `$message` — boy obyekt: `content` (bloklar **massivi**, matn bloki `type === 'text'` da `->text`), `stopReason` (nega to'xtadi), `usage->inputTokens`/`outputTokens` (xarajat).
- `system:` parametri modelga **rol va qoida** beradi (alohida message roli emas, top-level parametr).
- Uchta model: `claude-opus-4-8` (kuchli, default), `claude-sonnet-4-6` (balans), `claude-haiku-4-5` (tez/arzon). ID'ga **sana qo'shilmaydi**.
- Eng ko'p xatolar: Guzzle yo'q (discovery xatosi), kalit yo'q/noto'g'ri (401), model nomi xato (404) — har birining aniq yechimi bor.

## Amaliy mashqlar

1. **Muhitni tayyorlash.** Yangi `ai-test` papkasi yarating, `composer require anthropic-ai/sdk guzzlehttp/guzzle vlucas/phpdotenv` bajaring, `.env` ga kalitingizni qo'ying va `.gitignore` ga `.env` ni qo'shing. So'ng `php -v` va `composer show` bilan hammasi joyida ekanini tasdiqlang.
2. **Birinchi so'rov.** `birinchi.php` skriptini yozib, Claude'dan o'zini o'zbek tilida tanishtirishini so'rang. Javob bilan birga `inputTokens` va `outputTokens` sonlarini ham ekranga chiqaring.
3. **System prompt bilan rol.** Bitta savolni (masalan, "Massiv nima?") ikki marta yuboring: birinchisida `system:` siz, ikkinchisida `system: 'Sen 10 yoshli bolaga tushuntiradigan o\'qituvchisan'` bilan. Javoblar qanday farq qilganini yozma ravishda taqqoslang.
4. **Model almashtirish.** Bitta murakkabroq savolni (masalan, qisqa funksiya yozishni so'rash) `claude-opus-4-8`, `claude-sonnet-4-6` va `claude-haiku-4-5` modellarida navbat bilan yuboring. Javob sifati, tezligi va `usage` token sonidagi farqni kuzating.
5. **Xatoni ataylab chiqaring.** `.env` dagi kalitni vaqtincha noto'g'ri qiymatga o'zgartiring va skriptni ishga tushiring — qanday xato (status kodi) chiqishini ko'ring. So'ng kalitni to'g'rilab, `getenv()` `false` qaytarsa aniq xabar beradigan tekshiruvni skriptingizga qo'shing.

---

[⬅️ Oldingi: 01 — LLM nima](./01-llm-nima.md) · [🏠 Kitob boshi](./README.md) · [Keyingi: 03 — Prompt muhandisligi ➡️](./03-prompt-muhandisligi.md)
