<a id="b19"></a>
# 19-bo'lim: Validatsiya (email, telefon, parol)

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> ✅ Validatsiya — regex va mantiq aralashmasi. Muhim qoida: **mavjud, sinovdan o'tgan vositalardan foydalaning** (email/URL/IP uchun) — o'z regex'ingiz ko'pincha chetki holatlarni o'tkazib yuboradi. Murakkablik odatda O(n) (satr uzunligi).

<a id="m202"></a>
### 202. Email validatsiya
`⏱ O(n)`
Sodda amaliy tekshiruv (to'liq RFC 5322 emas). PHP'da tayyor `filter_var(..., FILTER_VALIDATE_EMAIL)` ishonchliroq.

**JS**
```js
const isValidEmail = email => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
```
**PHP**
```php
function isValidEmail($email): bool {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}
```
**Python**
```python
import re

def is_valid_email(email):
    return re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) is not None
```

<a id="m203"></a>
### 203. Parol kuchi (kriteriylar)
`⏱ O(n)`
Min 8 belgi, kichik + katta harf, raqam, maxsus belgi.

**JS**
```js
const isStrongPassword = pw =>
  pw.length >= 8 &&
  /[a-z]/.test(pw) &&
  /[A-Z]/.test(pw) &&
  /\d/.test(pw) &&
  /[^A-Za-z0-9]/.test(pw);
```
**PHP**
```php
function isStrongPassword($pw): bool {
    return strlen($pw) >= 8
        && preg_match('/[a-z]/', $pw)
        && preg_match('/[A-Z]/', $pw)
        && preg_match('/\d/', $pw)
        && preg_match('/[^A-Za-z0-9]/', $pw);
}
```
**Python**
```python
import re

def is_strong_password(pw):
    return (
        len(pw) >= 8
        and bool(re.search(r"[a-z]", pw))
        and bool(re.search(r"[A-Z]", pw))
        and bool(re.search(r"\d", pw))
        and bool(re.search(r"[^A-Za-z0-9]", pw))
    )
```

<a id="m204"></a>
### 204. URL validatsiya
`⏱ O(n)`
Tayyor vositalar regex'dan ishonchliroq — JS `URL` konstruktori, PHP `FILTER_VALIDATE_URL`, Python `urlparse`.

**JS**
```js
const isValidUrl = url => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};
```
**PHP**
```php
function isValidUrl($url): bool {
    return filter_var($url, FILTER_VALIDATE_URL) !== false;
}
```
**Python**
```python
from urllib.parse import urlparse

def is_valid_url(url):
    result = urlparse(url)
    return all([result.scheme, result.netloc])
```

<a id="m205"></a>
### 205. Username validatsiya
`⏱ O(n)`
Harf bilan boshlanadi, 3–20 belgi, harf/raqam/pastki chiziq (`\w`).

**JS**
```js
const isValidUsername = name => /^[a-zA-Z]\w{2,19}$/.test(name);
```
**PHP**
```php
function isValidUsername($name): bool {
    return (bool) preg_match('/^[a-zA-Z]\w{2,19}$/', $name);
}
```
**Python**
```python
import re

def is_valid_username(name):
    return re.fullmatch(r"[a-zA-Z]\w{2,19}", name) is not None
```

<a id="m206"></a>
### 206. Telefon validatsiya
`⏱ O(n)`
Avval bo'shliq/tire/qavslarni tozalab, so'ng E.164-uslubdagi shaklni tekshiramiz (ixtiyoriy `+`, 7–15 raqam). Aniq davlat formati uchun (mas. `+998 9X XXX XX XX`) pattern moslashtiriladi.

**JS**
```js
const isValidPhone = phone => {
  const cleaned = phone.replace(/[\s\-()]/g, "");
  return /^\+?[1-9]\d{6,14}$/.test(cleaned);
};
```
**PHP**
```php
function isValidPhone($phone): bool {
    $cleaned = preg_replace('/[\s\-()]/', '', $phone);
    return (bool) preg_match('/^\+?[1-9]\d{6,14}$/', $cleaned);
}
```
**Python**
```python
import re

def is_valid_phone(phone):
    cleaned = re.sub(r"[\s\-()]", "", phone)
    return re.fullmatch(r"\+?[1-9]\d{6,14}", cleaned) is not None
```

<a id="m207"></a>
### 207. Luhn algoritmi (kredit karta checksum)
`⏱ O(n) · 💾 O(1)`
O'ngdan boshlab har ikkinchi raqamni 2 ga ko'paytirib (9 dan oshsa −9), yig'indi 10 ga bo'linsa — karta raqami to'g'ri tuzilgan. Bank kartalari shu bilan tekshiriladi.

**JS**
```js
const isValidLuhn = number => {
  const digits = number.replace(/\D/g, "");
  let sum = 0, alt = false;
  for (let i = digits.length - 1; i >= 0; i--) {
    let d = +digits[i];
    if (alt) {
      d *= 2;
      if (d > 9) d -= 9;
    }
    sum += d;
    alt = !alt;
  }
  return digits.length > 0 && sum % 10 === 0;
};
```
**PHP**
```php
function isValidLuhn($number): bool {
    $digits = preg_replace('/\D/', '', $number);
    $sum = 0;
    $alt = false;
    for ($i = strlen($digits) - 1; $i >= 0; $i--) {
        $d = (int) $digits[$i];
        if ($alt) {
            $d *= 2;
            if ($d > 9) $d -= 9;
        }
        $sum += $d;
        $alt = !$alt;
    }
    return strlen($digits) > 0 && $sum % 10 === 0;
}
```
**Python**
```python
import re

def is_valid_luhn(number):
    digits = re.sub(r"\D", "", number)
    total = 0
    alt = False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return len(digits) > 0 and total % 10 == 0
```

<a id="m208"></a>
### 208. IPv4 validatsiya
`⏱ O(n)`
4 ta oktet, har biri 0–255; boshida ortiqcha nol ("01") rad etiladi. PHP'da tayyor `FILTER_VALIDATE_IP`.

**JS**
```js
const isValidIPv4 = ip => {
  const parts = ip.split(".");
  if (parts.length !== 4) return false;
  return parts.every(p => /^\d{1,3}$/.test(p) && +p <= 255 && String(+p) === p);
};
```
**PHP**
```php
function isValidIPv4($ip): bool {
    return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4) !== false;
}
```
**Python**
```python
def is_valid_ipv4(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit() or not 0 <= int(p) <= 255:
            return False
        if len(p) > 1 and p[0] == "0":
            return False
    return True
```

---
