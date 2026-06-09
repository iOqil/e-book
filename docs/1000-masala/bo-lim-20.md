<a id="b20"></a>
# 20-bo'lim: Amaliy masalalar (parsing, formatting)

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> 🛠 Kundalik ishda uchraydigan utilita funksiyalar. Yana bir bor — tilning tayyor vositalari ko'pincha qo'lda yozishdan yaxshiroq va xavfsizroq.

<a id="m209"></a>
### 209. Minglik ajratuvchi bilan formatlash
`⏱ O(d)` — d: raqamlar soni.
Har tilda tayyor vosita: JS `toLocaleString`, PHP `number_format`, Python f-string `:,`.

**JS**
```js
const formatNumber = n => n.toLocaleString("en-US");
// qo'lda: String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ",")
```
**PHP**
```php
function formatNumber($n): string {
    return number_format($n);
}
```
**Python**
```python
def format_number(n):
    return f"{n:,}"
```

<a id="m210"></a>
### 210. Slugify (matn → URL slug)
`⏱ O(n)`
Kichik harf → maxsus belgilarni olib tashlash → bo'shliq/tirelarni bitta tirega → chetdagilarni kesish. (Lotin bo'lmagan harflar uchun transliteratsiya kerak.)

**JS**
```js
const slugify = text =>
  text.toLowerCase().trim()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/[\s-]+/g, "-")
    .replace(/^-+|-+$/g, "");
```
**PHP**
```php
function slugify($text): string {
    $text = strtolower(trim($text));
    $text = preg_replace('/[^a-z0-9\s-]/', '', $text);
    $text = preg_replace('/[\s-]+/', '-', $text);
    return trim($text, '-');
}
```
**Python**
```python
import re

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text.strip("-")
```

<a id="m211"></a>
### 211. Query string'ni parse qilish
`⏱ O(n)`
Tayyor vositalar — JS `URLSearchParams`, PHP `parse_str`, Python `parse_qs` (u har kalitga ro'yxat beradi, shuning uchun `[0]`).

**JS**
```js
const parseQuery = qs => Object.fromEntries(new URLSearchParams(qs));
```
**PHP**
```php
function parseQuery($qs): array {
    parse_str($qs, $result);
    return $result;
}
```
**Python**
```python
from urllib.parse import parse_qs

def parse_query(qs):
    return {k: v[0] for k, v in parse_qs(qs).items()}
```

<a id="m212"></a>
### 212. Baytlarni o'qishli formatga (human-readable)
`⏱ O(1)`
1024 asosli logarifm orqali mos birlikni tanlaymiz (1536 → "1.5 KB").

**JS**
```js
const formatBytes = bytes => {
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / 1024 ** i).toFixed(1) + " " + units[i];
};
```
**PHP**
```php
function formatBytes($bytes): string {
    if ($bytes === 0) return "0 B";
    $units = ["B", "KB", "MB", "GB", "TB"];
    $i = (int) floor(log($bytes) / log(1024));
    return round($bytes / (1024 ** $i), 1) . " " . $units[$i];
}
```
**Python**
```python
import math

def format_bytes(num_bytes):
    if num_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(num_bytes, 1024)))
    return f"{num_bytes / 1024 ** i:.1f} {units[i]}"
```

<a id="m213"></a>
### 213. Integer → Roman raqam
`⏱ O(1)` (cheklangan jadval)
Kattadan kichikka — har qiymatni imkon qadar ayirib, mos belgini qo'shamiz (greedy). 1994 → "MCMXCIV".

**JS**
```js
const toRoman = num => {
  const map = [
    [1000, "M"], [900, "CM"], [500, "D"], [400, "CD"],
    [100, "C"], [90, "XC"], [50, "L"], [40, "XL"],
    [10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"],
  ];
  let result = "";
  for (const [value, symbol] of map) {
    while (num >= value) { result += symbol; num -= value; }
  }
  return result;
};
```
**PHP**
```php
function toRoman($num): string {
    $map = [
        1000 => "M", 900 => "CM", 500 => "D", 400 => "CD",
        100 => "C", 90 => "XC", 50 => "L", 40 => "XL",
        10 => "X", 9 => "IX", 5 => "V", 4 => "IV", 1 => "I",
    ];
    $result = "";
    foreach ($map as $value => $symbol) {
        while ($num >= $value) { $result .= $symbol; $num -= $value; }
    }
    return $result;
}
```
**Python**
```python
def to_roman(num):
    mapping = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = []
    for value, symbol in mapping:
        while num >= value:
            result.append(symbol)
            num -= value
    return "".join(result)
```

<a id="m214"></a>
### 214. Title case (har so'z bosh harfi katta)
`⏱ O(n)`
Tayyor vositalar — PHP `ucwords`, Python `str.title()`; JS'da regex bilan har so'z boshini katta qilamiz.

**JS**
```js
const titleCase = s =>
  s.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
```
**PHP**
```php
function titleCase($s): string {
    return ucwords(strtolower($s));
}
```
**Python**
```python
def title_case(s):
    return s.title()
```

<a id="m215"></a>
### 215. Matnni qisqartirish (truncate + "…")
`⏱ O(n)`
PHP'da `mb_` funksiyalari UTF-8 (ko'p baytli) matn uchun zarur — oddiy `substr` o'zbekcha harflarni buzishi mumkin.

**JS**
```js
const truncate = (s, max) =>
  s.length <= max ? s : s.slice(0, max).trimEnd() + "…";
```
**PHP**
```php
function truncate($s, $max): string {
    return mb_strlen($s) <= $max ? $s : rtrim(mb_substr($s, 0, $max)) . "…";
}
```
**Python**
```python
def truncate(s, max_len):
    return s if len(s) <= max_len else s[:max_len].rstrip() + "…"
```

<a id="m216"></a>
### 216. Tasodifiy parol generatsiya
`⏱ O(n)`
⚠️ **Xavfsizlik:** PHP `random_int` va Python `secrets` kriptografik xavfsiz; JS `Math.random` esa **emas** — jiddiy holatlarda `crypto.getRandomValues` ishlating.

**JS**
```js
const randomPassword = (length = 12) => {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return result;
};
```
**PHP**
```php
function randomPassword(int $length = 12): string {
    $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%";
    $result = "";
    $max = strlen($chars) - 1;
    for ($i = 0; $i < $length; $i++) {
        $result .= $chars[random_int(0, $max)];
    }
    return $result;
}
```
**Python**
```python
import secrets

def random_password(length=12):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%"
    return "".join(secrets.choice(chars) for _ in range(length))
```

---
