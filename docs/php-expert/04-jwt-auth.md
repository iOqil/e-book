# 04 — JWT va stateless auth

[⬅️ Oldingi: 03 — Authorization va RBAC](./03-authorization-rbac.md) · [🏠 README](./README.md) · [Keyingi: 05 — Qat'iy tiplash va PHP 8.4 tip tizimi ➡️](./05-tip-tizimi.md)

> **Bu bobda:** sessiyaga asoslangan (stateful) va tokenga asoslangan (stateless) autentifikatsiya orasidagi tub farqni, JWT ning aniq tuzilishini (`header.payload.signature`), HS256 imzosini PHP da QO'LDA yozish va xavfsiz tekshirishni, `firebase/php-jwt` kutubxonasi bilan amaliy ishlashni, access/refresh token hayot tsiklini hamda eng ko'p uchraydigan xavfsizlik tuzoqlarini (`alg:none`, zaif kalit, `exp` ni tekshirmaslik, tokenni noto'g'ri saqlash) o'rganamiz. Oxirida login -> token -> himoyalangan endpoint oqimini to'liq quramiz. Bu bob [03 — Authorization va RBAC](./03-authorization-rbac.md) hamda boshlovchi kitobdagi [sessiyalar va login](../php/33-sessiyalar-va-login.md) va [xavfsizlik asoslari](../php/34-xavfsizlik-asoslari.md) boblariga tayanadi.

---

## Stateful sessiya va stateless token: nima farqi bor?

Boshlovchi kitobda [sessiyalar va login](../php/33-sessiyalar-va-login.md) bilan tanishgansiz: foydalanuvchi login qilganda PHP serverda `$_SESSION` massivini saqlaydi, brauzerga esa faqat `PHPSESSID` nomli cookie beradi. Keyingi har bir so'rovda brauzer shu cookie ni yuboradi, server uni diskdagi (yoki Redis dagi) sessiya yozuviga bog'laydi. Bu **stateful** yondashuv — holat (kim login qilgan) **serverda** yashaydi.

JWT (JSON Web Token) butunlay boshqa falsafaga asoslanadi. Login muvaffaqiyatli bo'lganda server **imzolangan token** beradi, ichida foydalanuvchi haqidagi ma'lumot (`sub`, `role`, `exp`) joylashgan. Keyingi so'rovlarda mijoz shu tokenni yuboradi, server esa **hech qanday yozuvga qaramay**, faqat imzoni qayta hisoblab tokenning haqiqiyligini tekshiradi. Bu **stateless** yondashuv — holat **mijozda** yashaydi.

| Mezon | Sessiya (stateful) | JWT (stateless) |
|---|---|---|
| Holat qayerda | Serverda (`$_SESSION`, Redis) | Tokenning o'zida (mijozda) |
| Tekshirish | Sessiya yozuvini topish (I/O) | Imzoni qayta hisoblash (CPU) |
| Gorizontal masshtab | Sessiyani umumlashtirish kerak (sticky session yoki umumiy Redis) | Tabiiy: har bir server o'zi tekshiradi |
| Darhol bekor qilish | Oson: yozuvni o'chirasiz | Qiyin: token `exp` gacha amal qiladi (blacklist kerak) |
| Hajmi | Cookie kichik (faqat ID) | Token kattaroq (har so'rovda yuboriladi) |
| Mobil / mikroservis | Noqulay | Tabiiy |

**Qachon qaysi?**

- **Sessiya** — klassik monolit web-ilova, server-side render (Blade, Twig), bitta domen. Darhol logout va sodda bekor qilish muhim bo'lsa.
- **JWT** — SPA (React/Vue) backend i, **mobil ilova**lar (cookie noqulay), **mikroservislar** (har bir servis tokenni mustaqil tekshiradi), uchinchi tomon **API** lari, servislararo aloqa.

> **Muhim tushuncha:** stateless ning "narxi" — darhol bekor qilishning qiyinligi. Agar token o'g'irlansa, u `exp` gacha ishlaydi. Shu sababli access tokenni **qisqa muddatli** qilamiz (masalan 15 daqiqa) va refresh token mexanizmi qo'shamiz — bularni quyida ko'ramiz.

---

## JWT tuzilishi: header.payload.signature

JWT — bu uchta qismdan iborat, nuqta bilan ajratilgan satr:

![JWT 3 qismli anatomiya](rasmlar/04-jwt-anatomiya.svg)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsInJvbGUiOiJhZG1pbiJ9.HA4pMlSge_h7JZgOoNILvjXp7v6AsuRFJoBzVmKySuw
└────────────── header ──────────────┘ └──────────── payload ───────────┘ └────────────── signature ──────────────┘
```

Har bir qism — bu JSON ning **base64url** kodlangan ko'rinishi (signature esa baytlarning base64url i).

### 1. Header (sarlavha)

Algoritm va token turini bildiradi:

```json
{ "alg": "HS256", "typ": "JWT" }
```

### 2. Payload (yuk) va claimlar

Bu yerda foydalanuvchi haqidagi ma'lumot — **claim**lar joylashadi. RFC 7519 standart (registered) claimlarni belgilaydi:

| Claim | To'liq nomi | Mazmuni |
|---|---|---|
| `iss` | issuer | Tokenni kim bergan (masalan `auth.misol.uz`) |
| `sub` | subject | Token kim haqida (odatda foydalanuvchi ID si) |
| `aud` | audience | Token kim uchun mo'ljallangan |
| `exp` | expiration time | Muddat tugash vaqti (Unix timestamp) — undan keyin token YAROQSIZ |
| `nbf` | not before | Shu vaqtdan oldin token faol EMAS |
| `iat` | issued at | Token qachon berilgan |
| `jti` | JWT ID | Tokenning noyob identifikatori (bekor qilish/blacklist uchun) |

Bularga o'zingizning **maxsus (private) claim**laringizni qo'shasiz: `role`, `email`, `tenant_id` va h.k.

```json
{
  "iss": "auth.misol.uz",
  "sub": "42",
  "role": "admin",
  "iat": 1781195842,
  "exp": 1781199442,
  "jti": "9f3c1a2b"
}
```

> **❗ Eng muhim ogohlantirish:** payload **shifrlanmagan**, faqat base64url kodlangan. Uni har kim ochib o'qiy oladi (`jwt.io` ga joylashtiring — hamma ko'rinadi). JWT ning kuchi **maxfiylikda emas, butunlikda** (integrity): imzo tufayli ma'lumotni o'zgartirib bo'lmaydi, lekin ko'rib bo'ladi. **Hech qachon parol, karta raqami yoki sirli ma'lumotni payloadga solmang.**

### 3. Signature (imzo)

Imzo — `header` va `payload` ustidan hisoblangan kriptografik HMAC (HS256 da) yoki raqamli imzo (RS256/EdDSA da). Aynan shu qism tokenni "qalbakilashtirishdan" himoya qiladi.

### base64url — base64 ning URL-xavfsiz varianti

Oddiy base64 da `+`, `/`, `=` belgilari bor — ular URL va header larda muammo tug'diradi. base64url ularni almashtiradi:

- `+` -> `-`
- `/` -> `_`
- oxiridagi `=` to'ldiruvchilar **olib tashlanadi**

```php
<?php
declare(strict_types=1);

function base64url_encode(string $data): string {
    return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
}

function base64url_decode(string $data): string {
    // base64 4 ga bo'linadigan uzunlik talab qiladi — '=' ni qaytaramiz
    $remainder = strlen($data) % 4;
    if ($remainder) {
        $data .= str_repeat('=', 4 - $remainder);
    }
    // strict rejim (true): noto'g'ri belgi bo'lsa false qaytaradi
    return base64_decode(strtr($data, '-_', '+/'), true) ?: '';
}
```

---

## HS256 ni QO'LDA yozamiz: encode

HS256 — bu **HMAC-SHA256**. "Symmetric" (simmetrik): bitta **maxfiy kalit** ham imzolash, ham tekshirish uchun ishlatiladi. Kim kalitni bilsa — token yarata oladi va tekshira oladi.

Imzo formulasi:

```
signature = base64url( HMAC_SHA256( base64url(header) + "." + base64url(payload), secret ) )
```

PHP da HMAC ni `hash_hmac()` beradi. Uchinchi `binary` argumentini `true` qilamiz — bizga xom baytlar kerak, ularni keyin base64url qilamiz:

```php
<?php
declare(strict_types=1);

require 'base64url.php'; // yuqoridagi ikki funksiya

function jwt_encode(array $payload, string $secret, string $alg = 'HS256'): string
{
    if ($alg !== 'HS256') {
        throw new InvalidArgumentException("Bu misol faqat HS256 ni qo'llab-quvvatlaydi");
    }

    $header = ['alg' => $alg, 'typ' => 'JWT'];

    // JSON_THROW_ON_ERROR — kodlashda xato bo'lsa istisno chiqarsin
    $headerEncoded  = base64url_encode(json_encode($header, JSON_THROW_ON_ERROR));
    $payloadEncoded = base64url_encode(json_encode($payload, JSON_THROW_ON_ERROR));

    $signingInput = $headerEncoded . '.' . $payloadEncoded;

    // true => xom (binary) HMAC baytlari
    $signature = base64url_encode(hash_hmac('sha256', $signingInput, $secret, true));

    return $signingInput . '.' . $signature;
}
```

JSON bilan ishlash boshlovchi kitobda batafsil yoritilgan: [JSON bilan ishlash va oddiy API](../php/35-json-bilan-ishlash-va-oddiy-api.md).

---

## HS256 ni QO'LDA yozamiz: decode (xavfsiz tekshirish)

Decode — bu yerda **eng nozik joy**. Token kelganda quyidagilarni MAJBURIY tekshiramiz:

1. **Tuzilish** — aniq 3 qism bormi?
2. **Algoritm** — header dagi `alg` biz kutgan algoritmga (`HS256`) tengmi? (`alg:none` hujumini bloklash uchun — pastda batafsil)
3. **Imzo** — imzoni QAYTA hisoblab, kelgani bilan **timing-safe** solishtiramiz.
4. **Vaqt** — `exp` o'tmaganmi, `nbf` yetganmi?

```php
<?php
declare(strict_types=1);

require 'base64url.php';

/**
 * @return array{0: bool, 1: string, 2: ?array} [muvaffaqiyat, sabab, payload]
 */
function jwt_decode(string $token, string $secret): array
{
    $parts = explode('.', $token);
    if (count($parts) !== 3) {
        return [false, 'tuzilish_xato', null];
    }
    [$headerB64, $payloadB64, $signatureB64] = $parts;

    // 2-qadam: algoritmni QATTIQ belgilaymiz — header dagi 'alg' ga ISHONMAYMIZ
    $header = json_decode(base64url_decode($headerB64), true);
    if (!is_array($header) || ($header['alg'] ?? null) !== 'HS256') {
        return [false, 'algoritm_qabul_qilinmadi', null];
    }

    // 3-qadam: imzoni qayta hisoblaymiz
    $signingInput = $headerB64 . '.' . $payloadB64;
    $expected = base64url_encode(hash_hmac('sha256', $signingInput, $secret, true));

    // hash_equals — TIMING-SAFE solishtirish (pastda nega kerakligi tushuntirilgan)
    if (!hash_equals($expected, $signatureB64)) {
        return [false, 'imzo_xato', null];
    }

    $payload = json_decode(base64url_decode($payloadB64), true);
    if (!is_array($payload)) {
        return [false, 'payload_xato', null];
    }

    // 4-qadam: vaqt claimlari
    $now = time();
    $leeway = 0; // soat farqi uchun kichik tolerantlik qo'shsa bo'ladi (masalan 60s)

    if (isset($payload['exp']) && $now >= ((int) $payload['exp'] + $leeway)) {
        return [false, 'muddati_otgan', null];
    }
    if (isset($payload['nbf']) && $now < ((int) $payload['nbf'] - $leeway)) {
        return [false, 'hali_faol_emas', null];
    }

    return [true, 'ok', $payload];
}
```

### Nega `hash_equals`, oddiy `===` emas?

`===` operatori ikki satrni belgilab-belgilab solishtiradi va **birinchi farqda darhol to'xtaydi**. Bu vaqt farqini yuzaga keltiradi: noto'g'ri imzo birinchi belgida farq qilsa, tekshiruv tez tugaydi; agar dastlabki 10 belgi to'g'ri bo'lsa — sekinroq. Hujumchi shu mikro-vaqt farqlarini o'lchab, imzoni belgilab-belgilab "topib" olishi mumkin (**timing attack**). `hash_equals()` esa **doimo bir xil vaqtda** ishlaydi (constant-time), shuning uchun maxfiy qiymatlarni solishtirishda doim shuni ishlating.

### To'liq encode/decode aylanmasini ishga tushiramiz

Quyidagi misol PHP 8.4 bilan **haqiqatan ishga tushirildi** va natijasi tasdiqlangan:

```php
<?php
declare(strict_types=1);

require 'base64url.php';
require 'jwt_lib.php'; // jwt_encode + jwt_decode

$secret = 'juda-uzun-va-tasodifiy-maxfiy-kalit-32bayt+';

$token = jwt_encode([
    'iss'  => 'auth.misol.uz',
    'sub'  => '42',
    'role' => 'admin',
    'iat'  => time(),
    'exp'  => time() + 3600,
], $secret);

echo "TOKEN: $token\n";

[$ok, $reason, $payload] = jwt_decode($token, $secret);
echo "DECODE ok=" . var_export($ok, true) . " reason=$reason role={$payload['role']}\n";

// Buzilgan imzo
$tampered = substr($token, 0, -3) . 'AAA';
[$ok2, $reason2] = jwt_decode($tampered, $secret);
echo "TAMPER ok=" . var_export($ok2, true) . " reason=$reason2\n";

// Muddati o'tgan token
$expired = jwt_encode(['sub' => '1', 'exp' => time() - 10], $secret);
[$ok3, $reason3] = jwt_decode($expired, $secret);
echo "EXPIRED ok=" . var_export($ok3, true) . " reason=$reason3\n";
```

Haqiqiy natija (terminaldan):

```
TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhdXRoLm1pc29sLnV6Iiwic3ViIjoiNDIiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3ODExOTU4NDIsImV4cCI6MTc4MTE5OTQ0Mn0.-Z_SV79-vBgnWNCu3pzHw4_kSyr4PN7xf3HUxY8XY3w
DECODE ok=true reason=ok role=admin
TAMPER ok=false reason=imzo_xato
EXPIRED ok=false reason=muddati_otgan
```

Ko'ryapsizmi — imzodagi 3 ta belgi o'zgarganda ham token darhol rad etildi. Bu JWT ning butun mohiyati.

---

## RS256 va EdDSA: assimetrik imzolar (qisqacha)

HS256 simmetrik — bitta kalit. Bu **bitta tomon** ham imzolab, ham tekshirsa yaxshi. Lekin **mikroservis** muhitda muammo: agar 10 ta servis tokenni tekshirsa, hammasiga maxfiy kalit kerak bo'ladi — ulardan biri buzilsa, butun tizim xavf ostida (chunki kalitni bilgan token **yaratishi** ham mumkin).

**RS256** (RSA-SHA256) va **EdDSA** (Ed25519) — assimetrik. Ikkita kalit bo'ladi:

- **Yopiq (private) kalit** — faqat auth-server da. U bilan token IMZOLANADI.
- **Ochiq (public) kalit** — hamma servisga tarqatiladi. U bilan faqat TEKSHIRISH mumkin, lekin imzolash MUMKIN EMAS.

Shunday qilib, tekshiruvchi servislar token yarata olmaydi — bu tafovut mikroservis arxitekturasi uchun ideal.

```php
<?php
declare(strict_types=1);

// Kalit juftligini generatsiya qilish (bir marta, auth-server da)
$res = openssl_pkey_new([
    'private_key_bits' => 2048,
    'private_key_type' => OPENSSL_KEYTYPE_RSA,
]);
openssl_pkey_export($res, $privateKey);                       // yopiq kalit (PEM)
$publicKey = openssl_pkey_get_details($res)['key'];           // ochiq kalit (PEM)

// Imzolash (yopiq kalit bilan)
$signingInput = $headerB64 . '.' . $payloadB64;
openssl_sign($signingInput, $rawSignature, $privateKey, OPENSSL_ALGO_SHA256);

// Tekshirish (ochiq kalit bilan) — 1 = to'g'ri, 0 = noto'g'ri
$valid = openssl_verify($signingInput, $rawSignature, $publicKey, OPENSSL_ALGO_SHA256);
```

> **Eslatma:** RS256 imzosi HS256 ga qaraganda ancha katta (RSA-2048 da ~256 bayt), token hajmi oshadi. **EdDSA** (Ed25519) zamonaviyroq: imzo kichik, hisoblash tez, xavfsizlik yuqori. Amalda bularni qo'lda emas, kutubxona orqali ishlatamiz — quyida.

---

## Amaliyot: `firebase/php-jwt` kutubxonasi

Ishlab chiqarishda (production) JWT ni **qo'lda yozmang** — sinovdan o'tgan kutubxonadan foydalaning. Eng keng tarqalgani — `firebase/php-jwt`.

```bash
composer require firebase/php-jwt
```

```php
<?php
declare(strict_types=1);

require 'vendor/autoload.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Firebase\JWT\ExpiredException;
use Firebase\JWT\SignatureInvalidException;

// DIQQAT: firebase/php-jwt 6.x HS256 uchun kamida 256-bit (32 bayt) kalit talab qiladi
$secret = 'maxfiy-kalit-kamida-256-bit-uzunlikda-bolsin!!';

$payload = [
    'iss'  => 'auth.misol.uz',
    'sub'  => '42',
    'role' => 'admin',
    'iat'  => time(),
    'exp'  => time() + 3600,
];

// IMZOLASH
$jwt = JWT::encode($payload, $secret, 'HS256');

// TEKSHIRISH — algoritm ikkinchi argumentda QATTIQ belgilanadi (Key obyekti)
$decoded = JWT::decode($jwt, new Key($secret, 'HS256'));
echo $decoded->role; // "admin"  — stdClass obyekt qaytadi
```

`Key($secret, 'HS256')` — bu kutubxona dizaynidagi muhim xavfsizlik qarori: algoritm **siz tomonidan** belgilanadi, header dan emas. Bu `alg:none` va algoritm chalkashtirish (algorithm confusion) hujumlarini ildizdan kesadi.

### Istisnolar bilan ishlash

```php
<?php
declare(strict_types=1);

use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Firebase\JWT\ExpiredException;
use Firebase\JWT\SignatureInvalidException;
use Firebase\JWT\BeforeValidException;

try {
    $decoded = JWT::decode($jwt, new Key($secret, 'HS256'));
} catch (ExpiredException $e) {
    http_response_code(401);
    exit(json_encode(['error' => 'token_muddati_otgan']));
} catch (SignatureInvalidException $e) {
    http_response_code(401);
    exit(json_encode(['error' => 'imzo_notogri']));
} catch (BeforeValidException $e) {
    http_response_code(401);
    exit(json_encode(['error' => 'token_hali_faol_emas']));
} catch (\UnexpectedValueException $e) {
    // tuzilish buzilgan, yaroqsiz token
    http_response_code(401);
    exit(json_encode(['error' => 'yaroqsiz_token']));
}
```

Quyidagi sinov **haqiqatan ishga tushirildi** (`composer require firebase/php-jwt`, PHP 8.4) va natija:

```
ENCODED len=192
DECODED role=admin sub=42
TUTILDI: SignatureInvalidException   (noto'g'ri kalit bilan)
TUTILDI: ExpiredException            (exp o'tgan token bilan)
RS256 sub=7                          (assimetrik kalit bilan)
```

> **Amaliy tuzoq (sinovda topildi):** `firebase/php-jwt` ning yangi versiyalari HS256 uchun **32 baytdan qisqa** kalitni rad etib `DomainException("Provided key is too short")` chiqaradi. Bu — bilib qo'yilgan himoya: zaif kalit JWT ning eng katta xavfsizlik teshigi. Kalitingiz har doim uzun va tasodifiy bo'lsin: `bin2hex(random_bytes(32))`.

---

## Token hayot tsikli: access + refresh

Stateless ning eng katta zaifligi — **darhol bekor qila olmaslik**. Buni quyidagi naqsh bilan yumshatamiz:

![Login -> token -> himoyalangan so'rov oqimi](rasmlar/04-login-token-oqim.svg)

- **Access token** — qisqa muddatli (5–15 daqiqa). Har bir API so'rovida yuboriladi. O'g'irlansa ham tezda yaroqsiz bo'ladi.
- **Refresh token** — uzoq muddatli (kunlar/haftalar). FAQAT yangi access token olish uchun ishlatiladi, oddiy endpointlarga emas. Xavfsizroq joyda saqlanadi (httpOnly cookie).

Oqim:

1. Login -> server **ham** access, **ham** refresh token beradi.
2. Mijoz access token bilan API ga so'rov yuboradi.
3. Access token tugagach (401) -> mijoz refresh token bilan `/refresh` ga murojaat qiladi -> yangi access (va ko'pincha yangi refresh) oladi. Bu — **rotation** (aylanish).
4. Logout -> refresh tokenni bekor qilamiz (serverda jti ni blacklist ga qo'shamiz).

### Bekor qilish (revocation) strategiyalari

Stateless da tokenni "o'chirib" bo'lmaydi, lekin uni **rad etish** mumkin:

- **`jti` blacklist** — har tokenga noyob `jti` beramiz. Logout/o'g'irlikda `jti` ni Redis/DB ga qo'shamiz (TTL = token `exp` gacha). Decode da `jti` ro'yxatda bo'lsa rad etamiz. Bu yana qisman stateful, lekin faqat **bekor qilingan** tokenlar saqlanadi — barchasi emas.
- **`token_version`** — foydalanuvchi yozuvida raqam. Tokenga `ver` claim solamiz. "Hamma qurilmalardan chiqish" kerak bo'lsa, DB dagi raqamni oshiramiz — eski barcha tokenlar bir zumda yaroqsiz.
- **Qisqa `exp` + refresh** — eng amaliyi: access tokenni shunchalik qisqa qilingki, blacklist deyarli kerak emas; faqat refresh tokenlarni boshqaramiz.

> RBAC bilan bog'liqlik: tokendagi `role`/`scope` claimi [03 — Authorization va RBAC](./03-authorization-rbac.md) dagi ruxsat tekshiruvi uchun manba bo'ladi. Lekin diqqat: agar foydalanuvchi roli o'zgarsa, eski tokenda **eski rol** qoladi `exp` gacha. Shuning uchun rolni juda qisqa muddatli access tokenga solish yoki kritik amallarda DB dan tekshirish kerak.

---

## Xavfsizlik tuzoqlari

### 1. `alg:none` hujumi

JWT standartida `"alg": "none"` (imzosiz) variant bor. Sodda dizaynda decoder header dagi `alg` ga ishonib, "none bo'lsa imzoni tekshirmaymiz" deydi. Hujumchi shuni suiiste'mol qiladi: header ni `{"alg":"none"}` ga, payload ni `{"role":"admin"}` ga o'zgartirib, imzosiz token yuboradi.

```php
<?php
// ❌ XAVFLI: header dagi alg ga ishonish
$header = json_decode(base64url_decode($headerB64), true);
$alg = $header['alg']; // hujumchi buni "none" qila oladi!
if ($alg === 'none') {
    return $payload; // ❌ imzo umuman tekshirilmadi — TIZIM BUZILDI
}
```

**Yechim** — algoritmni **server tomonida QATTIQ belgilash**, header dagiga hech qachon ishonmaslik. Bizning qo'lda yozgan `jwt_decode` aynan shuni qiladi:

```php
<?php
// ✅ TO'G'RI: kutilgan algoritmni biz belgilaymiz
if (($header['alg'] ?? null) !== 'HS256') {
    return [false, 'algoritm_qabul_qilinmadi', null];
}
```

Sinovda `{"alg":"none"}` li token yuborilganda natija: `ALG_NONE ok=false reason=algoritm_qabul_qilinmadi` — to'g'ri rad etildi. `firebase/php-jwt` da esa `new Key($secret, 'HS256')` shuni majburlaydi.

### 2. Zaif maxfiy kalit

`"secret"`, `"123456"` kabi kalitlar bilan HS256 imzosini **brute-force** bilan ochish mumkin (hashcat). Kalit kamida 256-bit (32 bayt) tasodifiy bo'lsin va `.env` da saqlansin, kodda emas:

```php
<?php
// Kalit generatsiya (bir marta): bin2hex(random_bytes(32))
$secret = $_ENV['JWT_SECRET'] ?? throw new RuntimeException('JWT_SECRET sozlanmagan');
```

### 3. `exp` ni tekshirmaslik

Eng keng tarqalgan xato — imzoni tekshiramiz, lekin `exp` ni unutamiz. Natijada token **abadiy** yashaydi. Har doim `exp` ni tekshiring (bizning decoder buni qiladi, `firebase/php-jwt` ham avtomatik). Token bergan vaqtda `exp` ni MAJBURIY qo'ying.

### 4. Tokenni qayerda saqlash: httpOnly cookie vs localStorage

| Joy | Afzallik | Xavf |
|---|---|---|
| `localStorage` | Sodda, JS dan oson o'qiladi | **XSS** ga ochiq — zararli skript tokenni o'g'irlaydi |
| `httpOnly` cookie | JS o'qiy olmaydi (XSS dan himoya) | **CSRF** xavfi — `SameSite=Strict/Lax` bilan yopiladi |

Tavsiya: refresh tokenni **`httpOnly; Secure; SameSite=Strict` cookie** da saqlang, access tokenni esa xotirada (JS o'zgaruvchisida) ushlang. Bu XSS va CSRF ni bir vaqtda kamaytiradi.

```php
<?php
declare(strict_types=1);

setcookie('refresh_token', $refreshToken, [
    'expires'  => time() + 60 * 60 * 24 * 14,
    'path'     => '/auth/refresh',
    'httponly' => true,   // JS o'qiy olmaydi
    'secure'   => true,   // faqat HTTPS
    'samesite' => 'Strict',
]);
```

XSS, CSRF va boshqa hujumlar boshlovchi kitobda yoritilgan: [xavfsizlik asoslari](../php/34-xavfsizlik-asoslari.md).

### 5. Kalit aylanishi (key rotation)

Bir kunmas-bir kun kalitni almashtirish kerak bo'ladi (yoki sizib chiqsa). Agar darhol almashtirsangiz, hamma joriy tokenlar buziladi. Yechim — header dagi **`kid`** (key ID) claimi: bir nechta kalitni saqlaysiz, token qaysi kalit bilan imzolanganini `kid` aytadi. Eski kalitni qisqa muddat (eng uzun `exp` gacha) qabul qilib, keyin o'chirasiz.

---

## To'liq amaliyot: login -> token -> himoyalangan endpoint

Endi hammasini birlashtiramiz. Quyidagi kod **haqiqatan PHP 8.4 da ishga tushirildi** va har bir holat tasdiqlandi.

```php
<?php
declare(strict_types=1);

require 'jwt_lib.php'; // base64url_* + jwt_encode + jwt_decode

// --- Soxta foydalanuvchilar bazasi (amalda DB: ../php/29-phpdan-bazaga-ulanish.md) ---
$users = [
    'oqil@misol.uz' => [
        'id'   => 42,
        'role' => 'admin',
        'hash' => password_hash('parol1234', PASSWORD_BCRYPT), // parolni HECH QACHON ochiq saqlamang
    ],
];

$revokedJti = []; // bekor qilingan jti'lar (amalda Redis/DB)

// --- LOGIN: parolni tekshirib, access + refresh token beradi ---
function login(array $users, string $email, string $password, string $secret): ?array
{
    $u = $users[$email] ?? null;
    if ($u === null || !password_verify($password, $u['hash'])) {
        return null; // -> 401 Unauthorized
    }
    $now = time();
    return [
        'access' => jwt_encode([
            'iss' => 'auth.misol.uz', 'sub' => (string) $u['id'], 'role' => $u['role'],
            'iat' => $now, 'exp' => $now + 900, // 15 daqiqa
            'jti' => bin2hex(random_bytes(8)), 'type' => 'access',
        ], $secret),
        'refresh' => jwt_encode([
            'iss' => 'auth.misol.uz', 'sub' => (string) $u['id'],
            'iat' => $now, 'exp' => $now + 60 * 60 * 24 * 14, // 14 kun
            'jti' => bin2hex(random_bytes(8)), 'type' => 'refresh',
        ], $secret),
    ];
}

// --- HIMOYALANGAN ENDPOINT GUARD: Authorization: Bearer <token> ni tekshiradi ---
function authGuard(?string $authHeader, string $secret, array $revokedJti): array
{
    if ($authHeader === null || !preg_match('/^Bearer\s+(.+)$/i', $authHeader, $m)) {
        return [401, 'token_yoq', null];
    }
    [$ok, $reason, $payload] = jwt_decode($m[1], $secret);
    if (!$ok) {
        return [401, $reason, null];
    }
    // refresh tokenni oddiy endpointda ishlatib bo'lmaydi
    if (($payload['type'] ?? null) !== 'access') {
        return [401, 'notogri_token_turi', null];
    }
    // bekor qilingan jti?
    if (in_array($payload['jti'] ?? '', $revokedJti, true)) {
        return [401, 'bekor_qilingan', null];
    }
    return [200, 'ok', $payload];
}

$secret = 'juda-uzun-tasodifiy-maxfiy-kalit-kamida-32-bayt!!';

// 1) Noto'g'ri parol -> null (401)
var_dump(login($users, 'oqil@misol.uz', 'xato', $secret)); // NULL

// 2) To'g'ri login
$tokens = login($users, 'oqil@misol.uz', 'parol1234', $secret);

// 3) Himoyalangan endpointga to'g'ri so'rov
[$code, $reason, $payload] = authGuard('Bearer ' . $tokens['access'], $secret, $revokedJti);
echo "GET /profile: $code $reason role={$payload['role']}\n"; // 200 ok role=admin

// 4) Tokensiz so'rov
[$code2] = authGuard(null, $secret, $revokedJti);
echo "tokensiz: $code2\n"; // 401

// 5) Refresh tokenni endpointda ishlatishga urinish
[$code3, $reason3] = authGuard('Bearer ' . $tokens['refresh'], $secret, $revokedJti);
echo "refresh bilan: $code3 $reason3\n"; // 401 notogri_token_turi

// 6) jti bekor qilingach
$revokedJti[] = jwt_decode($tokens['access'], $secret)[2]['jti'];
[$code4, $reason4] = authGuard('Bearer ' . $tokens['access'], $secret, $revokedJti);
echo "bekor qilingach: $code4 $reason4\n"; // 401 bekor_qilingan
```

Haqiqiy chiqish (terminaldan):

```
NULL
GET /profile: 200 ok role=admin
tokensiz: 401
refresh bilan: 401 notogri_token_turi
bekor qilingach: 401 bekor_qilingan
```

Har bir holat aynan kutilgandek ishladi: noto'g'ri parol rad etildi, to'g'ri token 200 berdi, tokensiz va refresh-as-access 401, bekor qilingan jti esa 401. Bu — to'liq stateless auth oqimining ishlaydigan skeleti.

Status kodlar (401 vs 403) haqida [03 — Authorization va RBAC](./03-authorization-rbac.md) da batafsil: **401** — "kim ekanligingni isbotlamading" (autentifikatsiya), **403** — "kimligingni bilaman, lekin ruxsating yo'q" (avtorizatsiya). Token yaroqsiz/yo'q bo'lsa 401, token yaroqli lekin rol yetmasa 403.

---

## Mashqlar

### Oson

1. `base64url_encode("Salom, JWT!")` natijasini qo'lda chiqarib, keyin `base64url_decode` bilan teskari tiklang. Oddiy `base64_encode` dan farqini ko'rsating.
2. Berilgan JWT ning faqat payload qismini decode qilib, `sub` va `role` claimlarini chiqaruvchi funksiya yozing (imzoni tekshirmasdan — faqat o'qish uchun).
3. `jwt_encode` bilan token yarating, undan keyin `jwt.io` ga (yoki qo'lda) header ni ochib o'qing. Payload shifrlanmaganini o'z ko'zingiz bilan tasdiqlang.

### O'rta

4. `jwt_decode` ga `leeway` (soat farqi tolerantligi) parametrini to'liq qo'shing: `exp` va `nbf` tekshiruvida `±leeway` soniya joiz bo'lsin. 60 soniyalik leeway bilan sinab ko'ring.
5. `firebase/php-jwt` ni o'rnatib, HS256 bilan token yarating, so'ng **noto'g'ri (lekin yetarlicha uzun)** kalit bilan decode qilishga urinib, qaysi istisno (`SignatureInvalidException`) chiqishini terminalda tasdiqlang.
6. `authGuard` ga rol tekshiruvini qo'shing: faqat `role === 'admin'` bo'lsa 200, aks holda **403** qaytarsin. 401 va 403 farqini izohlang.

### Qiyin

7. To'liq **refresh oqimini** yozing: `refreshAccessToken(string $refreshToken, string $secret, array &$revokedJti): ?array` funksiyasi refresh tokenni tekshirib (`type === 'refresh'`, jti bekor qilinmagan), **yangi access + yangi refresh** qaytarsin va **eski refresh jti ni blacklist ga qo'shsin** (rotation). O'g'irlangan eski refresh tokenni qayta ishlatishga urinish 401 berishini sinov bilan isbotlang.
8. `jti` blacklist ni in-memory massiv o'rniga **fayl yoki SQLite** da, har yozuvga TTL (token `exp`) bilan saqlovchi `Revocation` klassini yozing. TTL o'tgan yozuvlarni avtomatik tozalasin.

---

<details markdown="1"><summary>Yechim — 1</summary>

```php
<?php
declare(strict_types=1);

require 'base64url.php';

$matn = 'Salom, JWT!';
$url   = base64url_encode($matn);
$plain = base64_encode($matn);

echo "base64url: $url\n";    // belgilar -, _ va '=' siz
echo "base64:    $plain\n";  // +, / va '=' bo'lishi mumkin
echo "teskari:   " . base64url_decode($url) . "\n"; // Salom, JWT!
```

Farq: `base64url` da `+`/`/` -> `-`/`_` ga almashadi va oxiridagi `=` to'ldiruvchilar olib tashlanadi. Shu sababli u URL va HTTP header larda xavfsiz ishlaydi.

</details>

<details markdown="1"><summary>Yechim — 2</summary>

```php
<?php
declare(strict_types=1);

require 'base64url.php';

function jwt_peek(string $token): ?array
{
    $parts = explode('.', $token);
    if (count($parts) !== 3) {
        return null;
    }
    $payload = json_decode(base64url_decode($parts[1]), true);
    return is_array($payload) ? $payload : null;
}

$p = jwt_peek($token);
echo "sub={$p['sub']} role={$p['role']}\n";
```

Diqqat: bu funksiya imzoni TEKSHIRMAYDI — faqat o'qish (debug, log) uchun. Ishonch talab qiladigan qarorni hech qachon tekshirilmagan payloadga asoslamang.

</details>

<details markdown="1"><summary>Yechim — 4</summary>

```php
<?php
declare(strict_types=1);

function jwt_decode(string $token, string $secret, int $leeway = 0): array
{
    // ... tuzilish, alg, imzo tekshiruvi avvalgidek ...
    $now = time();

    if (isset($payload['exp']) && $now >= ((int) $payload['exp'] + $leeway)) {
        return [false, 'muddati_otgan', null];
    }
    if (isset($payload['nbf']) && $now < ((int) $payload['nbf'] - $leeway)) {
        return [false, 'hali_faol_emas', null];
    }
    return [true, 'ok', $payload];
}

// Sinov: exp 30s oldin tugagan, lekin 60s leeway bilan hali joiz
$token = jwt_encode(['sub' => '1', 'exp' => time() - 30], $secret);
var_dump(jwt_decode($token, $secret, 60)[0]); // true  (leeway tufayli)
var_dump(jwt_decode($token, $secret, 0)[0]);  // false (leeway yo'q)
```

`leeway` distributed tizimda serverlar soati biroz farq qilganda foydali — odatda 30–60 soniya. Juda katta qilmang: u xavfsizlik oynasini kengaytiradi.

</details>

<details markdown="1"><summary>Yechim — 6</summary>

```php
<?php
declare(strict_types=1);

function authGuard(?string $authHeader, string $secret, string $requiredRole = 'user'): array
{
    if ($authHeader === null || !preg_match('/^Bearer\s+(.+)$/i', $authHeader, $m)) {
        return [401, 'token_yoq', null]; // autentifikatsiya yo'q
    }
    [$ok, $reason, $payload] = jwt_decode($m[1], $secret);
    if (!$ok) {
        return [401, $reason, null]; // token yaroqsiz -> autentifikatsiya muvaffaqiyatsiz
    }
    // bu yergacha kim ekanligi ANIQ. Endi RUXSAT tekshiruvi:
    if (($payload['role'] ?? 'user') !== $requiredRole) {
        return [403, 'ruxsat_yoq', $payload]; // kim ekanini bilamiz, lekin huquqi yo'q
    }
    return [200, 'ok', $payload];
}
```

**401 vs 403:** 401 — "kim ekanligingni isbotlay olmading" (token yo'q/yaroqsiz/muddati o'tgan). 403 — "kimligingni bilaman, lekin bu amalga huquqing yo'q". Bu farq [03 — Authorization va RBAC](./03-authorization-rbac.md) ning markaziy tushunchasi.

</details>

<details markdown="1"><summary>Yechim — 7 (to'liq refresh rotation)</summary>

```php
<?php
declare(strict_types=1);

require 'jwt_lib.php';

/**
 * Refresh tokenni tekshiradi va YANGI access + refresh juftligini qaytaradi.
 * Eski refresh jti ni blacklist ga qo'shadi (rotation) — bir martalik ishlatish.
 *
 * @param array<int,string> $revokedJti  havola bo'yicha (&) o'zgartiriladi
 * @return array{access:string,refresh:string}|null  null => 401
 */
function refreshAccessToken(string $refreshToken, string $secret, array &$revokedJti): ?array
{
    [$ok, $reason, $payload] = jwt_decode($refreshToken, $secret);
    if (!$ok) {
        return null; // imzo/exp xato
    }
    // FAQAT refresh turidagi token qabul qilinadi
    if (($payload['type'] ?? null) !== 'refresh') {
        return null;
    }
    // qayta ishlatilgan (rotation buzilgan) refresh token?
    $oldJti = $payload['jti'] ?? '';
    if (in_array($oldJti, $revokedJti, true)) {
        return null; // o'g'irlangan/qayta ishlatilgan -> rad etamiz
    }

    // eski refresh jti ni darhol bekor qilamiz (bir martalik)
    $revokedJti[] = $oldJti;

    $now = time();
    $sub = $payload['sub'];

    return [
        'access' => jwt_encode([
            'iss' => 'auth.misol.uz', 'sub' => $sub, 'role' => 'admin',
            'iat' => $now, 'exp' => $now + 900,
            'jti' => bin2hex(random_bytes(8)), 'type' => 'access',
        ], $secret),
        'refresh' => jwt_encode([
            'iss' => 'auth.misol.uz', 'sub' => $sub,
            'iat' => $now, 'exp' => $now + 60 * 60 * 24 * 14,
            'jti' => bin2hex(random_bytes(8)), 'type' => 'refresh',
        ], $secret),
    ];
}

// --- Sinov ---
$secret = 'juda-uzun-tasodifiy-maxfiy-kalit-kamida-32-bayt!!';
$revoked = [];

$now = time();
$oldRefresh = jwt_encode([
    'iss' => 'auth.misol.uz', 'sub' => '42',
    'iat' => $now, 'exp' => $now + 86400,
    'jti' => 'eski-jti-1', 'type' => 'refresh',
], $secret);

// 1) Birinchi refresh -> yangi juftlik beradi
$new = refreshAccessToken($oldRefresh, $secret, $revoked);
var_dump($new !== null);                 // true — yangi tokenlar berildi

// 2) ESKI refresh tokenni QAYTA ishlatishga urinish -> rad etiladi
$replay = refreshAccessToken($oldRefresh, $secret, $revoked);
var_dump($replay === null);              // true — jti blacklist da, 401
```

**Nega rotation muhim?** Agar refresh token o'g'irlansa, ham hujumchi, ham haqiqiy foydalanuvchi uni ishlatishga urinadi. Rotation tufayli birinchi ishlatgan eski jti ni bekor qiladi; ikkinchisi kelganda u allaqachon blacklist da — tizim aniqlaydiki, refresh token "ikki marta ishlatildi" (reuse), demak o'g'irlangan bo'lishi mumkin. Bunda butun foydalanuvchi seansini majburan tugatish (hamma tokenlarni bekor qilish) eng to'g'ri reaksiya.

</details>

<details markdown="1"><summary>Yechim — 8 (TTL li Revocation klassi)</summary>

```php
<?php
declare(strict_types=1);

final class Revocation
{
    private \PDO $db;

    public function __construct(string $sqlitePath = ':memory:')
    {
        $this->db = new \PDO('sqlite:' . $sqlitePath);
        $this->db->setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);
        $this->db->exec(
            'CREATE TABLE IF NOT EXISTS revoked (
                jti        TEXT PRIMARY KEY,
                expires_at INTEGER NOT NULL
            )'
        );
    }

    /** jti ni bekor qiladi; expiresAt = token exp (Unix ts) */
    public function revoke(string $jti, int $expiresAt): void
    {
        $stmt = $this->db->prepare(
            'INSERT OR REPLACE INTO revoked (jti, expires_at) VALUES (:jti, :exp)'
        );
        $stmt->execute([':jti' => $jti, ':exp' => $expiresAt]);
    }

    /** jti bekor qilinganmi? (muddati o'tmagan yozuvlar orasida) */
    public function isRevoked(string $jti): bool
    {
        $this->gc(); // avval eskirgan yozuvlarni tozalaymiz
        $stmt = $this->db->prepare(
            'SELECT 1 FROM revoked WHERE jti = :jti AND expires_at > :now'
        );
        $stmt->execute([':jti' => $jti, ':now' => time()]);
        return (bool) $stmt->fetchColumn();
    }

    /** TTL o'tgan yozuvlarni o'chiradi — ro'yxat cheksiz o'smaydi */
    public function gc(): int
    {
        $stmt = $this->db->prepare('DELETE FROM revoked WHERE expires_at <= :now');
        $stmt->execute([':now' => time()]);
        return $stmt->rowCount();
    }
}

// --- Sinov ---
$rev = new Revocation();              // xotirada SQLite
$rev->revoke('jti-aktiv', time() + 3600);
$rev->revoke('jti-eskirgan', time() - 10); // allaqachon eskirgan

var_dump($rev->isRevoked('jti-aktiv'));    // true  — hali amaldagi bekor qilish
var_dump($rev->isRevoked('jti-eskirgan')); // false — gc() uni tozaladi
var_dump($rev->isRevoked('jti-yoq'));      // false — umuman bekor qilinmagan
```

`PDO` bilan ishlash boshlovchi kitobda yoritilgan: [PHP dan bazaga ulanish](../php/29-phpdan-bazaga-ulanish.md). Bu yondashuvning kuchi: blacklist FAQAT bekor qilingan, hali amaldagi tokenlarni saqlaydi — `gc()` muddati o'tganlarini avtomatik o'chiradi, shuning uchun jadval cheksiz o'smaydi. Ishlab chiqarishda SQLite o'rniga Redis (`SET jti 1 EX <ttl>`) tabiiy TTL tufayli yanada qulay.

</details>

---

[⬅️ Oldingi: 03 — Authorization va RBAC](./03-authorization-rbac.md) · [🏠 README](./README.md) · [Keyingi: 05 — Qat'iy tiplash va PHP 8.4 tip tizimi ➡️](./05-tip-tizimi.md)
