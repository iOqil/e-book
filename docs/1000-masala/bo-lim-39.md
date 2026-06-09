<a id="b39"></a>
# 39-bo'lim: Amaliy va kundalik masalalar

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Bu bo'limda har kuni kod yozishda kerak bo'ladigan obyekt va string yordamchilari
> to'plangan: chuqur nusxa va tenglik, obyektni tekislash va qayta qurish, kalitlar
> bo'yicha tanlash/chiqarib tashlash, query string qurish, matnni niqoblash, to'ldirish
> va o'rash, HTML bilan ishlash, ko'plik va tartib sonlar, ismdan bosh harflar, sonni
> qisqartirish va fayl nomini tozalash. Bular kichik, lekin loyihalarda doimiy ishlatiladigan
> "utility" funksiyalar — lodash, Str va shunga o'xshash kutubxonalarning yuragi.

<a id="m871"></a>
### 871. Chuqur nusxa (deep clone)
Obyekt va massivni ichki qatlamlari bilan to'liq, mustaqil nusxasini yaratadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const deepClone = (v) => {
  if (v === null || typeof v !== "object") return v;
  if (v instanceof Date) return new Date(v.getTime());
  if (Array.isArray(v)) return v.map(deepClone);
  const out = {};
  for (const k of Object.keys(v)) out[k] = deepClone(v[k]);
  return out;
};
```
**PHP**
```php
function deepClone($v) {
    if (is_array($v)) {
        $out = [];
        foreach ($v as $k => $x) $out[$k] = deepClone($x);
        return $out;
    }
    return is_object($v) ? clone $v : $v;
}
```
**Python**
```python
def deep_clone(v):
    if isinstance(v, dict):
        return {k: deep_clone(x) for k, x in v.items()}
    if isinstance(v, list):
        return [deep_clone(x) for x in v]
    return v
```

<a id="m872"></a>
### 872. Chuqur tenglik (deep equal)
Ikki tuzilmani ichki qiymatlarigacha qiyoslab, mazmunan teng-tengligini tekshiradi.
`⏱ O(n) · 💾 O(d)`

**JS**
```js
const deepEqual = (a, b) => {
  if (a === b) return true;
  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null)
    return false;
  const ka = Object.keys(a), kb = Object.keys(b);
  if (ka.length !== kb.length) return false;
  return ka.every(
    (k) => Object.prototype.hasOwnProperty.call(b, k) && deepEqual(a[k], b[k])
  );
};
```
**PHP**
```php
function deepEqual($a, $b): bool {
    if (is_array($a) && is_array($b)) {
        if (count($a) !== count($b)) return false;
        foreach ($a as $k => $v) {
            if (!array_key_exists($k, $b) || !deepEqual($v, $b[$k])) return false;
        }
        return true;
    }
    return $a === $b;
}
```
**Python**
```python
def deep_equal(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(deep_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(deep_equal(x, y) for x, y in zip(a, b))
    return a == b and type(a) == type(b)
```

<a id="m873"></a>
### 873. Chuqur birlashtirish (deep merge)
Ikki obyektni rekursiv birlashtiradi; ichki obyektlar qo'shiladi, oddiy qiymatlar ustiga yoziladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const isObj = (v) => v && typeof v === "object" && !Array.isArray(v);
const deepMerge = (a, b) => {
  const out = { ...a };
  for (const k of Object.keys(b))
    out[k] = isObj(a[k]) && isObj(b[k]) ? deepMerge(a[k], b[k]) : b[k];
  return out;
};
```
**PHP**
```php
function deepMerge(array $a, array $b): array {
    foreach ($b as $k => $v) {
        if (isset($a[$k]) && is_array($a[$k]) && is_array($v)
            && !array_is_list($a[$k]) && !array_is_list($v))
            $a[$k] = deepMerge($a[$k], $v);
        else
            $a[$k] = $v;
    }
    return $a;
}
```
**Python**
```python
def deep_merge(a, b):
    out = dict(a)
    for k, v in b.items():
        if isinstance(out.get(k), dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out
```

<a id="m874"></a>
### 874. Obyektni tekislash (flatten — dot kalitlar)
Ichma-ich joylashgan obyektni `"a.b.c"` ko'rinishidagi bir qatlamli kalitlarga aylantiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const flatten = (obj, prefix = "", out = {}) => {
  for (const k of Object.keys(obj)) {
    const key = prefix ? `${prefix}.${k}` : k;
    if (isObj(obj[k])) flatten(obj[k], key, out);
    else out[key] = obj[k];
  }
  return out;
};
```
**PHP**
```php
function flatten(array $obj, string $prefix = ''): array {
    $out = [];
    foreach ($obj as $k => $v) {
        $key = $prefix === '' ? (string)$k : "$prefix.$k";
        if (is_array($v) && !array_is_list($v) && $v !== [])
            $out += flatten($v, $key);
        else
            $out[$key] = $v;
    }
    return $out;
}
```
**Python**
```python
def flatten(obj, prefix=""):
    out = {}
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else str(k)
        if isinstance(v, dict) and v:
            out.update(flatten(v, key))
        else:
            out[key] = v
    return out
```

<a id="m875"></a>
### 875. Dot kalitlardan obyekt qurish (unflatten)
`"a.b.c"` ko'rinishidagi yassi kalitlarni qaytadan ichma-ich obyektga yig'adi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const unflatten = (flat) => {
  const out = {};
  for (const path of Object.keys(flat)) {
    const keys = path.split(".");
    let cur = out;
    keys.forEach((k, i) => {
      if (i === keys.length - 1) cur[k] = flat[path];
      else cur = cur[k] = cur[k] || {};
    });
  }
  return out;
};
```
**PHP**
```php
function unflatten(array $flat): array {
    $out = [];
    foreach ($flat as $path => $value) {
        $keys = explode('.', (string)$path);
        $cur = &$out;
        foreach ($keys as $i => $k) {
            if ($i === count($keys) - 1) $cur[$k] = $value;
            else {
                if (!isset($cur[$k]) || !is_array($cur[$k])) $cur[$k] = [];
                $cur = &$cur[$k];
            }
        }
        unset($cur);
    }
    return $out;
}
```
**Python**
```python
def unflatten(flat):
    out = {}
    for path, value in flat.items():
        keys = path.split(".")
        cur = out
        for i, k in enumerate(keys):
            if i == len(keys) - 1:
                cur[k] = value
            else:
                cur = cur.setdefault(k, {})
    return out
```

<a id="m876"></a>
### 876. Yo'l bo'yicha olish (get by path)
`"a.b.c"` yo'li bilan chuqurdagi qiymatni xavfsiz oladi; topilmasa standart qiymat.
`⏱ O(d) · 💾 O(1)`

**JS**
```js
const getByPath = (obj, path, def = undefined) => {
  const keys = Array.isArray(path) ? path : path.split(".");
  let cur = obj;
  for (const k of keys) {
    if (cur == null || !(k in cur)) return def;
    cur = cur[k];
  }
  return cur;
};
```
**PHP**
```php
function getByPath(array $obj, string $path, $def = null) {
    $cur = $obj;
    foreach (explode('.', $path) as $k) {
        if (!is_array($cur) || !array_key_exists($k, $cur)) return $def;
        $cur = $cur[$k];
    }
    return $cur;
}
```
**Python**
```python
def get_by_path(obj, path, default=None):
    keys = path.split(".") if isinstance(path, str) else path
    cur = obj
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur
```

<a id="m877"></a>
### 877. Yo'l bo'yicha o'rnatish (set by path)
`"a.b.c"` yo'li bo'yicha qiymat yozadi; oraliq obyektlar yo'q bo'lsa yaratiladi.
`⏱ O(d) · 💾 O(d)`

**JS**
```js
const setByPath = (obj, path, value) => {
  const keys = Array.isArray(path) ? path : path.split(".");
  let cur = obj;
  keys.forEach((k, i) => {
    if (i === keys.length - 1) cur[k] = value;
    else cur = cur[k] = isObj(cur[k]) ? cur[k] : {};
  });
  return obj;
};
```
**PHP**
```php
function setByPath(array $obj, string $path, $value): array {
    $keys = explode('.', $path);
    $cur = &$obj;
    foreach ($keys as $i => $k) {
        if ($i === count($keys) - 1) $cur[$k] = $value;
        else {
            if (!isset($cur[$k]) || !is_array($cur[$k])) $cur[$k] = [];
            $cur = &$cur[$k];
        }
    }
    unset($cur);
    return $obj;
}
```
**Python**
```python
def set_by_path(obj, path, value):
    keys = path.split(".") if isinstance(path, str) else path
    cur = obj
    for i, k in enumerate(keys):
        if i == len(keys) - 1:
            cur[k] = value
        else:
            if not isinstance(cur.get(k), dict):
                cur[k] = {}
            cur = cur[k]
    return obj
```

<a id="m878"></a>
### 878. Kalitlarni tanlash (pick)
Berilgan kalitlar to'plamiga mos qiymatlardan yangi obyekt yig'adi.
`⏱ O(k) · 💾 O(k)`

**JS**
```js
const pick = (obj, keys) => {
  const out = {};
  for (const k of keys) if (k in obj) out[k] = obj[k];
  return out;
};
```
**PHP**
```php
function pick(array $obj, array $keys): array {
    $out = [];
    foreach ($keys as $k) if (array_key_exists($k, $obj)) $out[$k] = $obj[$k];
    return $out;
}
```
**Python**
```python
def pick(obj, keys):
    return {k: obj[k] for k in keys if k in obj}
```

<a id="m879"></a>
### 879. Kalitlarni chiqarib tashlash (omit)
Berilgan kalitlardan tashqari barcha juftliklarni saqlab qoladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const omit = (obj, keys) => {
  const drop = new Set(keys);
  const out = {};
  for (const k of Object.keys(obj)) if (!drop.has(k)) out[k] = obj[k];
  return out;
};
```
**PHP**
```php
function omit(array $obj, array $keys): array {
    return array_diff_key($obj, array_flip($keys));
}
```
**Python**
```python
def omit(obj, keys):
    drop = set(keys)
    return {k: v for k, v in obj.items() if k not in drop}
```

<a id="m880"></a>
### 880. Obyekt kalitlarini camelCase qilish
`first_name`, `last-name` kabi kalitlarni `firstName`, `lastName` ko'rinishiga keltiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const toCamel = (s) => s.replace(/[_-]([a-z0-9])/g, (_, c) => c.toUpperCase());
const camelKeys = (obj) => {
  const out = {};
  for (const k of Object.keys(obj)) out[toCamel(k)] = obj[k];
  return out;
};
```
**PHP**
```php
function toCamel(string $s): string {
    return preg_replace_callback('/[_-]([a-z0-9])/', fn($m) => strtoupper($m[1]), $s);
}
function camelKeys(array $obj): array {
    $out = [];
    foreach ($obj as $k => $v) $out[toCamel((string)$k)] = $v;
    return $out;
}
```
**Python**
```python
def to_camel(s):
    return re.sub(r"[_-]([a-z0-9])", lambda m: m.group(1).upper(), s)

def camel_keys(obj):
    return {to_camel(k): v for k, v in obj.items()}
```

<a id="m881"></a>
### 881. Obyekt kalitlarini snake_case qilish
`firstName` kabi kalitlarni `first_name` ko'rinishiga keltiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const toSnake = (s) =>
  s.replace(/([A-Z])/g, "_$1").replace(/[-\s]+/g, "_").toLowerCase().replace(/^_/, "");
const snakeKeys = (obj) => {
  const out = {};
  for (const k of Object.keys(obj)) out[toSnake(k)] = obj[k];
  return out;
};
```
**PHP**
```php
function toSnake(string $s): string {
    $s = preg_replace('/([A-Z])/', '_$1', $s);
    $s = preg_replace('/[-\s]+/', '_', $s);
    return ltrim(strtolower($s), '_');
}
function snakeKeys(array $obj): array {
    $out = [];
    foreach ($obj as $k => $v) $out[toSnake((string)$k)] = $v;
    return $out;
}
```
**Python**
```python
def to_snake(s):
    s = re.sub(r"([A-Z])", r"_\1", s)
    s = re.sub(r"[-\s]+", "_", s)
    return s.lower().lstrip("_")

def snake_keys(obj):
    return {to_snake(k): v for k, v in obj.items()}
```

<a id="m882"></a>
### 882. Obyektni teskari aylantirish (invert)
Kalit va qiymatlarning o'rnini almashtiradi: `{a:"x"}` -> `{x:"a"}`.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const invert = (obj) => {
  const out = {};
  for (const k of Object.keys(obj)) out[obj[k]] = k;
  return out;
};
```
**PHP**
```php
function invert(array $obj): array {
    return array_flip($obj);
}
```
**Python**
```python
def invert(obj):
    return {v: k for k, v in obj.items()}
```

<a id="m883"></a>
### 883. JSON stringify (oddiy)
Obyekt, massiv, son, satr va boolean qiymatlarni JSON matniga aylantiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const jsonStringify = (v) => {
  if (v === null) return "null";
  const t = typeof v;
  if (t === "number" || t === "boolean") return String(v);
  if (t === "string") return '"' + v.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"';
  if (Array.isArray(v)) return "[" + v.map(jsonStringify).join(",") + "]";
  return "{" + Object.keys(v).map((k) => jsonStringify(k) + ":" + jsonStringify(v[k])).join(",") + "}";
};
```
**PHP**
```php
function jsonStringifySimple($v): string {
    if ($v === null) return 'null';
    if (is_bool($v)) return $v ? 'true' : 'false';
    if (is_int($v) || is_float($v)) return (string)$v;
    if (is_string($v)) return '"' . str_replace(['\\', '"'], ['\\\\', '\\"'], $v) . '"';
    if (array_is_list($v))
        return '[' . implode(',', array_map('jsonStringifySimple', $v)) . ']';
    $parts = [];
    foreach ($v as $k => $x) $parts[] = jsonStringifySimple((string)$k) . ':' . jsonStringifySimple($x);
    return '{' . implode(',', $parts) . '}';
}
```
**Python**
```python
def json_stringify(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(v, list):
        return "[" + ",".join(json_stringify(x) for x in v) + "]"
    return "{" + ",".join(json_stringify(str(k)) + ":" + json_stringify(x)
                          for k, x in v.items()) + "}"
```

<a id="m884"></a>
### 884. JSON parse (oddiy)
JSON matnini tilning nativ tuzilmasiga (obyekt/massiv) o'giradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const jsonParse = (s) => JSON.parse(s);
```
**PHP**
```php
function jsonParseSimple(string $s) {
    return json_decode($s, true);
}
```
**Python**
```python
import json

def json_parse(s):
    return json.loads(s)
```

<a id="m885"></a>
### 885. Query string qurish (build)
Obyektdan `key=value&key=value` ko'rinishidagi URL so'rovi matnini yasaydi; null qiymatlarni tashlaydi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const buildQuery = (params) =>
  Object.keys(params)
    .filter((k) => params[k] !== undefined && params[k] !== null)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(params[k]))
    .join("&");
```
**PHP**
```php
function buildQuery(array $params): string {
    $parts = [];
    foreach ($params as $k => $v) {
        if ($v === null) continue;
        $parts[] = rawurlencode((string)$k) . '=' . rawurlencode((string)$v);
    }
    return implode('&', $parts);
}
```
**Python**
```python
from urllib.parse import quote

def build_query(params):
    return "&".join(
        quote(str(k)) + "=" + quote(str(v))
        for k, v in params.items()
        if v is not None
    )
```

<a id="m886"></a>
### 886. Satrni niqoblash (mask — karta raqami)
Karta raqamining oxirgi bir necha belgisidan boshqasini `*` bilan yashiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const maskCard = (s, visible = 4, ch = "*") => {
  const digits = String(s).replace(/\s/g, "");
  if (digits.length <= visible) return digits;
  return ch.repeat(digits.length - visible) + digits.slice(-visible);
};
```
**PHP**
```php
function maskCard(string $s, int $visible = 4, string $ch = '*'): string {
    $digits = preg_replace('/\s/', '', $s);
    $len = strlen($digits);
    if ($len <= $visible) return $digits;
    return str_repeat($ch, $len - $visible) . substr($digits, -$visible);
}
```
**Python**
```python
def mask_card(s, visible=4, ch="*"):
    digits = re.sub(r"\s", "", str(s))
    if len(digits) <= visible:
        return digits
    return ch * (len(digits) - visible) + digits[-visible:]
```

<a id="m887"></a>
### 887. Satrni to'ldirish (pad left/right)
Satrni berilgan uzunlikkacha chap yoki o'ng tomondan belgilar bilan to'ldiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const padLeft = (s, len, ch = " ") => String(s).padStart(len, ch);
const padRight = (s, len, ch = " ") => String(s).padEnd(len, ch);
```
**PHP**
```php
function padLeft(string $s, int $len, string $ch = ' '): string {
    return str_pad($s, $len, $ch, STR_PAD_LEFT);
}
function padRight(string $s, int $len, string $ch = ' '): string {
    return str_pad($s, $len, $ch, STR_PAD_RIGHT);
}
```
**Python**
```python
def pad_left(s, length, ch=" "):
    return str(s).rjust(length, ch)

def pad_right(s, length, ch=" "):
    return str(s).ljust(length, ch)
```

<a id="m888"></a>
### 888. Word wrap (matnni o'rash)
Matnni so'zlarni buzmasdan berilgan kenglikdagi qatorlarga bo'ladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const wordWrap = (text, width) => {
  const words = text.split(/\s+/);
  const lines = [];
  let line = "";
  for (const w of words) {
    if (!line) line = w;
    else if (line.length + 1 + w.length <= width) line += " " + w;
    else { lines.push(line); line = w; }
  }
  if (line) lines.push(line);
  return lines.join("\n");
};
```
**PHP**
```php
function wordWrapText(string $text, int $width): string {
    $words = preg_split('/\s+/', trim($text));
    $lines = [];
    $line = '';
    foreach ($words as $w) {
        if ($line === '') $line = $w;
        elseif (strlen($line) + 1 + strlen($w) <= $width) $line .= ' ' . $w;
        else { $lines[] = $line; $line = $w; }
    }
    if ($line !== '') $lines[] = $line;
    return implode("\n", $lines);
}
```
**Python**
```python
def word_wrap(text, width):
    words = text.split()
    lines, line = [], ""
    for w in words:
        if not line:
            line = w
        elif len(line) + 1 + len(w) <= width:
            line += " " + w
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return "\n".join(lines)
```

<a id="m889"></a>
### 889. HTML escape
Matndagi `<`, `>`, `&`, qo'shtirnoq va apostrofni xavfsiz HTML entitilariga aylantiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const htmlEscape = (s) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
   .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
```
**PHP**
```php
function htmlEscapeStr(string $s): string {
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}
```
**Python**
```python
def html_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))
```

<a id="m890"></a>
### 890. HTML unescape
HTML entitilarni (`&lt;`, `&amp;` ...) qaytadan oddiy belgilarga o'giradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const htmlUnescape = (s) =>
  s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"')
   .replace(/&#39;/g, "'").replace(/&amp;/g, "&");
```
**PHP**
```php
function htmlUnescapeStr(string $s): string {
    return htmlspecialchars_decode($s, ENT_QUOTES);
}
```
**Python**
```python
def html_unescape(s):
    return (s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
             .replace("&#39;", "'").replace("&amp;", "&"))
```

<a id="m891"></a>
### 891. Regex escape
Satrdagi maxsus regex belgilarini ekranlab, uni xavfsiz literal namuna sifatida ishlatadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const escapeRegExp = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
```
**PHP**
```php
function escapeRegExp(string $s): string {
    return preg_quote($s, '/');
}
```
**Python**
```python
def escape_regexp(s):
    return re.escape(s)
```

<a id="m892"></a>
### 892. HTML teglarni olib tashlash (strip tags)
Matndan barcha `<...>` teglarni olib tashlab, faqat sof matnni qoldiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const stripTags = (html) => html.replace(/<[^>]*>/g, "");
```
**PHP**
```php
function stripTagsStr(string $html): string {
    return preg_replace('/<[^>]*>/', '', $html);
}
```
**Python**
```python
def strip_tags(html):
    return re.sub(r"<[^>]*>", "", html)
```

<a id="m893"></a>
### 893. Pluralize (ko'plik)
Inglizcha so'zni son bo'yicha birlik yoki ko'plik shaklga keltiradi (oddiy qoidalar bilan).
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const pluralize = (word, count) => {
  if (count === 1) return word;
  if (/(s|x|z|ch|sh)$/i.test(word)) return word + "es";
  if (/[^aeiou]y$/i.test(word)) return word.slice(0, -1) + "ies";
  return word + "s";
};
```
**PHP**
```php
function pluralize(string $word, int $count): string {
    if ($count === 1) return $word;
    if (preg_match('/(s|x|z|ch|sh)$/i', $word)) return $word . 'es';
    if (preg_match('/[^aeiou]y$/i', $word)) return substr($word, 0, -1) . 'ies';
    return $word . 's';
}
```
**Python**
```python
def pluralize(word, count):
    if count == 1:
        return word
    if re.search(r"(s|x|z|ch|sh)$", word, re.I):
        return word + "es"
    if re.search(r"[^aeiou]y$", word, re.I):
        return word[:-1] + "ies"
    return word + "s"
```

<a id="m894"></a>
### 894. Ordinal (1st/2nd/3rd)
Sonni tartib son qo'shimchasi bilan qaytaradi; 11–13 maxsus holatlar `th` bo'ladi.
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const ordinal = (n) => {
  const s = ["th", "st", "nd", "rd"], v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
};
```
**PHP**
```php
function ordinal(int $n): string {
    $v = $n % 100;
    $suf = ($v >= 11 && $v <= 13) ? 'th' : (['st', 'nd', 'rd'][($n % 10) - 1] ?? 'th');
    return $n . $suf;
}
```
**Python**
```python
def ordinal(n):
    v = n % 100
    if 11 <= v <= 13:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"
```

<a id="m895"></a>
### 895. Ismdan bosh harflar (initials)
Ism-familiyadan birinchi harflarni olib, bosh harfli qisqartma yasaydi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const initials = (name, max = 2) =>
  name.trim().split(/\s+/).filter(Boolean).slice(0, max)
      .map((w) => w[0].toUpperCase()).join("");
```
**PHP**
```php
function initials(string $name, int $max = 2): string {
    $parts = preg_split('/\s+/', trim($name), -1, PREG_SPLIT_NO_EMPTY);
    $parts = array_slice($parts, 0, $max);
    return implode('', array_map(fn($w) => strtoupper(mb_substr($w, 0, 1)), $parts));
}
```
**Python**
```python
def initials(name, max_n=2):
    parts = name.split()[:max_n]
    return "".join(w[0].upper() for w in parts)
```

<a id="m896"></a>
### 896. Sonni qisqartirish (1200 -> 1.2k)
Katta sonni `k`, `M`, `B` kabi qisqa shaklga aylantiradi.
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const abbreviateNumber = (n) => {
  const units = ["", "k", "M", "B", "T"];
  if (Math.abs(n) < 1000) return String(n);
  const i = Math.min(units.length - 1, Math.floor(Math.log10(Math.abs(n)) / 3));
  const val = n / 1000 ** i;
  return (Math.round(val * 10) / 10) + units[i];
};
```
**PHP**
```php
function abbreviateNumber($n): string {
    $units = ['', 'k', 'M', 'B', 'T'];
    if (abs($n) < 1000) return (string)$n;
    $i = min(count($units) - 1, (int)floor(log10(abs($n)) / 3));
    $val = $n / (1000 ** $i);
    return rtrim(rtrim(number_format(round($val, 1), 1, '.', ''), '0'), '.') . $units[$i];
}
```
**Python**
```python
def abbreviate_number(n):
    units = ["", "k", "M", "B", "T"]
    if abs(n) < 1000:
        return str(n)
    i = min(len(units) - 1, int(math.log10(abs(n)) // 3))
    val = round(n / 1000 ** i, 1)
    return f"{val:g}" + units[i]
```

<a id="m897"></a>
### 897. Qidiruv so'zini ajratib ko'rsatish (highlight)
Matndagi qidiruv so'zining barcha (registrga befarq) uchrashlarini belgilar bilan o'raydi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const highlight = (text, term, [a, b] = ["[", "]"]) => {
  if (!term) return text;
  const re = new RegExp(escapeRegExp(term), "gi");
  return text.replace(re, (m) => a + m + b);
};
```
**PHP**
```php
function highlight(string $text, string $term, string $a = '[', string $b = ']'): string {
    if ($term === '') return $text;
    return preg_replace('/' . escapeRegExp($term) . '/i', $a . '$0' . $b, $text);
}
```
**Python**
```python
def highlight(text, term, wrap=("[", "]")):
    if not term:
        return text
    a, b = wrap
    return re.sub(escape_regexp(term), lambda m: a + m.group(0) + b, text, flags=re.I)
```

<a id="m898"></a>
### 898. Sentence case
Matnni jumla boshlari bosh harf bo'ladigan ko'rinishga keltiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const sentenceCase = (s) =>
  s.toLowerCase().replace(/(^\s*\w|[.!?]\s+\w)/g, (c) => c.toUpperCase());
```
**PHP**
```php
function sentenceCase(string $s): string {
    $s = strtolower($s);
    return preg_replace_callback('/(^\s*\w|[.!?]\s+\w)/', fn($m) => strtoupper($m[0]), $s);
}
```
**Python**
```python
def sentence_case(s):
    s = s.lower()
    return re.sub(r"(^\s*\w|[.!?]\s+\w)", lambda m: m.group(0).upper(), s)
```

<a id="m899"></a>
### 899. Fayl nomini tozalash (sanitize filename)
Fayl nomidan xavfli belgilarni (`/ \ : * ? " < >`) olib tashlab, xavfsiz nomga aylantiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const sanitizeFilename = (name) =>
  name.replace(/[/\\?%*:|"<>]/g, "_")
      .replace(/\s+/g, "_")
      .replace(/_+/g, "_")
      .replace(/^[_.]+|[_.]+$/g, "")
      .slice(0, 255) || "file";
```
**PHP**
```php
function sanitizeFilename(string $name): string {
    $name = preg_replace('/[\/\\\\?%*:|"<>]/', '_', $name);
    $name = preg_replace('/\s+/', '_', $name);
    $name = preg_replace('/_+/', '_', $name);
    $name = trim($name, '_.');
    $name = substr($name, 0, 255);
    return $name === '' ? 'file' : $name;
}
```
**Python**
```python
def sanitize_filename(name):
    name = re.sub(r'[/\\?%*:|"<>]', "_", name)
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_.")[:255]
    return name or "file"
```

<a id="m900"></a>
### 900. Parse boolean ("true"/"1"/"yes")
Matnli qiymatni boolean'ga aylantiradi: `true`, `1`, `yes`, `y`, `on` -> true.
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const parseBoolean = (v) => {
  if (typeof v === "boolean") return v;
  return /^(true|1|yes|y|on)$/i.test(String(v).trim());
};
```
**PHP**
```php
function parseBoolean($v): bool {
    if (is_bool($v)) return $v;
    return (bool)preg_match('/^(true|1|yes|y|on)$/i', trim((string)$v));
}
```
**Python**
```python
def parse_boolean(v):
    if isinstance(v, bool):
        return v
    return bool(re.match(r"^(true|1|yes|y|on)$", str(v).strip(), re.I))
```

<a id="m901"></a>
### 901. Sana farqini "insoniy" ko'rsatish (date diff humanize)
Ikki sana orasidagi farqni "3 kun oldin", "2 soat oldin" ko'rinishida qaytaradi.

**JS**
```js
const humanizeDiff = (from, to = new Date()) => {
  const sec = Math.round((to - from) / 1000);
  const past = sec >= 0;
  const s = Math.abs(sec);
  const units = [[31536000, "yil"], [2592000, "oy"], [86400, "kun"],
    [3600, "soat"], [60, "daqiqa"], [1, "soniya"]];
  for (const [secs, name] of units) {
    if (s >= secs) {
      const n = Math.floor(s / secs);
      return past ? `${n} ${name} oldin` : `${n} ${name}dan keyin`;
    }
  }
  return "hozir";
};
```
**PHP**
```php
function humanizeDiff(int $fromTs, ?int $toTs = null): string {
    $toTs ??= time();
    $sec = $toTs - $fromTs;
    $past = $sec >= 0;
    $s = abs($sec);
    $units = [31536000 => "yil", 2592000 => "oy", 86400 => "kun",
        3600 => "soat", 60 => "daqiqa", 1 => "soniya"];
    foreach ($units as $secs => $name) {
        if ($s >= $secs) {
            $n = intdiv($s, $secs);
            return $past ? "$n $name oldin" : "$n {$name}dan keyin";
        }
    }
    return "hozir";
}
```
**Python**
```python
import time

def humanize_diff(from_ts, to_ts=None):
    to_ts = time.time() if to_ts is None else to_ts
    sec = to_ts - from_ts
    past = sec >= 0
    s = abs(sec)
    units = [(31536000, "yil"), (2592000, "oy"), (86400, "kun"),
             (3600, "soat"), (60, "daqiqa"), (1, "soniya")]
    for secs, name in units:
        if s >= secs:
            n = int(s // secs)
            return f"{n} {name} oldin" if past else f"{n} {name}dan keyin"
    return "hozir"
```

<a id="m902"></a>
### 902. Nisbiy vaqt formati (relative time format)
Berilgan sekundlik farqni qisqa nisbiy yorliqqa aylantiradi ("just now", "5m", "2h", "3d").

**JS**
```js
const relativeTime = (diffSec) => {
  const s = Math.abs(diffSec);
  if (s < 60) return "hozirgina";
  const table = [[86400, "k"], [3600, "s"], [60, "d"]];
  for (const [secs, suf] of table)
    if (s >= secs) return `${Math.floor(s / secs)}${suf}`;
  return "hozirgina";
};
```
**Python**
```python
def relative_time(diff_sec):
    s = abs(diff_sec)
    if s < 60:
        return "hozirgina"
    for secs, suf in ((86400, "k"), (3600, "s"), (60, "d")):
        if s >= secs:
            return f"{s // secs}{suf}"
    return "hozirgina"
```

<a id="m903"></a>
### 903. Davomiylikni parse qilish ("1h30m" -> sekund)
"1h30m", "45s", "2d12h" kabi qatorni umumiy sekundga aylantiradi.

**JS**
```js
const parseDuration = (str) => {
  const mult = { d: 86400, h: 3600, m: 60, s: 1 };
  let total = 0;
  const re = /(\d+)([dhms])/g;
  let m;
  while ((m = re.exec(str)) !== null) total += Number(m[1]) * mult[m[2]];
  return total;
};
```
**PHP**
```php
function parseDuration(string $str): int {
    $mult = ["d" => 86400, "h" => 3600, "m" => 60, "s" => 1];
    $total = 0;
    preg_match_all('/(\d+)([dhms])/', $str, $matches, PREG_SET_ORDER);
    foreach ($matches as $m) $total += (int)$m[1] * $mult[$m[2]];
    return $total;
}
```
**Python**
```python
import re

def parse_duration(s):
    mult = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    return sum(int(n) * mult[u] for n, u in re.findall(r"(\d+)([dhms])", s))
```

<a id="m904"></a>
### 904. Davomiylikni formatlash (sekund -> "1s 30d")
Umumiy sekundni o'qiladigan "1s 30d 15soniya" ko'rinishidagi qatorga aylantiradi.

**JS**
```js
const formatDuration = (sec) => {
  const units = [[86400, "kun"], [3600, "s"], [60, "d"], [1, "soniya"]];
  const parts = [];
  let rem = sec;
  for (const [secs, name] of units) {
    const n = Math.floor(rem / secs);
    if (n > 0) { parts.push(`${n}${name}`); rem -= n * secs; }
  }
  return parts.length ? parts.join(" ") : "0soniya";
};
```
**PHP**
```php
function formatDuration(int $sec): string {
    $units = [86400 => "kun", 3600 => "s", 60 => "d", 1 => "soniya"];
    $parts = [];
    $rem = $sec;
    foreach ($units as $secs => $name) {
        $n = intdiv($rem, $secs);
        if ($n > 0) { $parts[] = "$n$name"; $rem -= $n * $secs; }
    }
    return $parts ? implode(" ", $parts) : "0soniya";
}
```
**Python**
```python
def format_duration(sec):
    units = [(86400, "kun"), (3600, "s"), (60, "d"), (1, "soniya")]
    parts, rem = [], sec
    for secs, name in units:
        n, rem = divmod(rem, secs) if False else (rem // secs, rem - (rem // secs) * secs)
        if n > 0:
            parts.append(f"{n}{name}")
    return " ".join(parts) if parts else "0soniya"
```

<a id="m905"></a>
### 905. Ikki sana orasidagi ish kunlari soni (business days)
Dam olish kunlarini (shanba, yakshanba) chiqarib tashlab, ish kunlarini sanaydi.
`⏱ O(kunlar) · 💾 O(1)`

**JS**
```js
const businessDays = (start, end) => {
  let count = 0;
  const d = new Date(start);
  while (d <= end) {
    const wd = d.getDay();
    if (wd !== 0 && wd !== 6) count++;
    d.setDate(d.getDate() + 1);
  }
  return count;
};
```
**Python**
```python
from datetime import date, timedelta

def business_days(start, end):
    count, d = 0, start
    while d <= end:
        if d.weekday() < 5:
            count += 1
        d += timedelta(days=1)
    return count
```

<a id="m906"></a>
### 906. Ish kunlarini qo'shish (add business days)
Sanaga berilgan miqdordagi ish kunini qo'shadi, dam olish kunlarini o'tkazib yuboradi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const addBusinessDays = (start, n) => {
  const d = new Date(start);
  let added = 0;
  while (added < n) {
    d.setDate(d.getDate() + 1);
    const wd = d.getDay();
    if (wd !== 0 && wd !== 6) added++;
  }
  return d;
};
```
**Python**
```python
from datetime import timedelta

def add_business_days(start, n):
    d, added = start, 0
    while added < n:
        d += timedelta(days=1)
        if d.weekday() < 5:
            added += 1
    return d
```

<a id="m907"></a>
### 907. Dam olish kunimi (is weekend)
Sana shanba yoki yakshanbaga to'g'ri kelsa rost qaytaradi.

**JS**
```js
const isWeekend = (date) => {
  const wd = date.getDay();
  return wd === 0 || wd === 6;
};
```
**PHP**
```php
function isWeekend(int $ts): bool {
    $wd = (int)date("N", $ts); // 6=shanba, 7=yakshanba
    return $wd >= 6;
}
```
**Python**
```python
def is_weekend(d):
    return d.weekday() >= 5  # 5=shanba, 6=yakshanba
```

<a id="m908"></a>
### 908. ISO hafta raqami (ISO week number)
Sananing ISO-8601 bo'yicha yil ichidagi hafta raqamini hisoblaydi.

**JS**
```js
const isoWeek = (date) => {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil(((d - yearStart) / 86400000 + 1) / 7);
};
```
**Python**
```python
def iso_week(d):
    return d.isocalendar()[1]
```

<a id="m909"></a>
### 909. Sananing choragi (quarter)
Sana yilning nechanchi choragiga (1-4) tegishli ekanini qaytaradi.

**JS**
```js
const quarterOf = (date) => Math.floor(date.getMonth() / 3) + 1;
```
**PHP**
```php
function quarterOf(int $ts): int {
    return intdiv((int)date("n", $ts) - 1, 3) + 1;
}
```
**Python**
```python
def quarter_of(d):
    return (d.month - 1) // 3 + 1
```

<a id="m910"></a>
### 910. Yildagi kunlar soni (days in year)
Yil kabisa yili bo'lsa 366, aks holda 365 qaytaradi.

**JS**
```js
const daysInYear = (year) => {
  const leap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  return leap ? 366 : 365;
};
```
**PHP**
```php
function daysInYear(int $year): int {
    $leap = ($year % 4 === 0 && $year % 100 !== 0) || $year % 400 === 0;
    return $leap ? 366 : 365;
}
```
**Python**
```python
import calendar

def days_in_year(year):
    return 366 if calendar.isleap(year) else 365
```

<a id="m911"></a>
### 911. HEX rangni RGB ga aylantirish (hex -> rgb)
"#ff8800" yoki "f80" qatorini [r, g, b] uchligiga aylantiradi.

**JS**
```js
const hexToRgb = (hex) => {
  let h = hex.replace(/^#/, "");
  if (h.length === 3) h = h.split("").map((c) => c + c).join("");
  const num = parseInt(h, 16);
  return [(num >> 16) & 255, (num >> 8) & 255, num & 255];
};
```
**PHP**
```php
function hexToRgb(string $hex): array {
    $h = ltrim($hex, "#");
    if (strlen($h) === 3) $h = $h[0].$h[0].$h[1].$h[1].$h[2].$h[2];
    $num = hexdec($h);
    return [($num >> 16) & 255, ($num >> 8) & 255, $num & 255];
}
```
**Python**
```python
def hex_to_rgb(hex_str):
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
```

<a id="m912"></a>
### 912. RGB rangni HEX ga aylantirish (rgb -> hex)
[r, g, b] qiymatlarini "#rrggbb" qatoriga aylantiradi.

**JS**
```js
const rgbToHex = (r, g, b) =>
  "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");
```
**PHP**
```php
function rgbToHex(int $r, int $g, int $b): string {
    return sprintf("#%02x%02x%02x", $r, $g, $b);
}
```
**Python**
```python
def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"
```

<a id="m913"></a>
### 913. RGB rangni HSL ga aylantirish (rgb -> hsl)
RGB ranglarini ottenok (H), to'yinganlik (S) va yorqinlik (L) qiymatlariga aylantiradi.

**JS**
```js
const rgbToHsl = (r, g, b) => {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  const l = (max + min) / 2;
  let h = 0, s = 0;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    if (max === r) h = ((g - b) / d + (g < b ? 6 : 0));
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h /= 6;
  }
  return [Math.round(h * 360), Math.round(s * 100), Math.round(l * 100)];
};
```
**Python**
```python
def rgb_to_hsl(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    h = s = 0.0
    if mx != mn:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6
    return [round(h * 360), round(s * 100), round(l * 100)]
```

<a id="m914"></a>
### 914. HSL rangni RGB ga aylantirish (hsl -> rgb)
H (0-360), S va L (0-100) qiymatlaridan [r, g, b] hosil qiladi.

**JS**
```js
const hslToRgb = (h, s, l) => {
  h /= 360; s /= 100; l /= 100;
  const hue = (p, q, t) => {
    if (t < 0) t += 1;
    if (t > 1) t -= 1;
    if (t < 1 / 6) return p + (q - p) * 6 * t;
    if (t < 1 / 2) return q;
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  };
  if (s === 0) { const v = Math.round(l * 255); return [v, v, v]; }
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;
  return [hue(p, q, h + 1 / 3), hue(p, q, h), hue(p, q, h - 1 / 3)]
    .map((v) => Math.round(v * 255));
};
```
**Python**
```python
def hsl_to_rgb(h, s, l):
    h, s, l = h / 360, s / 100, l / 100

    def hue(p, q, t):
        t %= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    if s == 0:
        v = round(l * 255)
        return [v, v, v]
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    return [round(hue(p, q, h + 1 / 3) * 255),
            round(hue(p, q, h) * 255),
            round(hue(p, q, h - 1 / 3) * 255)]
```

<a id="m915"></a>
### 915. Valyutani formatlash (1234.5 -> "$1,234.50")
Sonni minglik ajratgich va ikki kasrli pul ko'rinishida formatlaydi.

**JS**
```js
const formatCurrency = (amount, symbol = "$") => {
  const fixed = amount.toFixed(2);
  const [int, dec] = fixed.split(".");
  const grouped = int.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return `${symbol}${grouped}.${dec}`;
};
```
**PHP**
```php
function formatCurrency(float $amount, string $symbol = "$"): string {
    return $symbol . number_format($amount, 2, ".", ",");
}
```
**Python**
```python
def format_currency(amount, symbol="$"):
    return f"{symbol}{amount:,.2f}"
```

<a id="m916"></a>
### 916. Valyutani parse qilish ("$1,234.50" -> 1234.5)
Pul qatoridan belgilar va ajratgichlarni olib tashlab, son qaytaradi.

**JS**
```js
const parseCurrency = (str) => parseFloat(str.replace(/[^0-9.-]/g, ""));
```
**PHP**
```php
function parseCurrency(string $str): float {
    return (float)preg_replace('/[^0-9.\-]/', "", $str);
}
```
**Python**
```python
import re

def parse_currency(s):
    return float(re.sub(r"[^0-9.\-]", "", s))
```

<a id="m917"></a>
### 917. Harorat konvertori (C / F / K)
Haroratni bir o'lchov birligidan boshqasiga aylantiradi.

**JS**
```js
const convertTemp = (value, from, to) => {
  const toC = { C: (v) => v, F: (v) => (v - 32) * 5 / 9, K: (v) => v - 273.15 };
  const fromC = { C: (v) => v, F: (v) => v * 9 / 5 + 32, K: (v) => v + 273.15 };
  return fromC[to](toC[from](value));
};
```
**Python**
```python
def convert_temp(value, src, dst):
    to_c = {"C": lambda v: v, "F": lambda v: (v - 32) * 5 / 9, "K": lambda v: v - 273.15}
    from_c = {"C": lambda v: v, "F": lambda v: v * 9 / 5 + 32, "K": lambda v: v + 273.15}
    return from_c[dst](to_c[src](value))
```

<a id="m918"></a>
### 918. Uzunlik o'lchov konvertori (m / km / mile)
Uzunlikni metr orqali har qanday ikki birlik orasida aylantiradi.

**JS**
```js
const convertLength = (value, from, to) => {
  const toM = { m: 1, km: 1000, mile: 1609.344, ft: 0.3048 };
  return (value * toM[from]) / toM[to];
};
```
**Python**
```python
def convert_length(value, src, dst):
    to_m = {"m": 1, "km": 1000, "mile": 1609.344, "ft": 0.3048}
    return value * to_m[src] / to_m[dst]
```

<a id="m919"></a>
### 919. Og'irlik konvertori (kg / lb / oz)
Og'irlikni kilogramm orqali turli birliklar orasida aylantiradi.

**JS**
```js
const convertWeight = (value, from, to) => {
  const toKg = { kg: 1, g: 0.001, lb: 0.45359237, oz: 0.028349523 };
  return (value * toKg[from]) / toKg[to];
};
```
**Python**
```python
def convert_weight(value, src, dst):
    to_kg = {"kg": 1, "g": 0.001, "lb": 0.45359237, "oz": 0.028349523}
    return value * to_kg[src] / to_kg[dst]
```

<a id="m920"></a>
### 920. Sonni tartib so'zga aylantirish (ordinal)
Sonni "birinchi"/"first" kabi tartib so'ziga aylantiradi (inglizcha suffiks bilan).

**JS**
```js
const ordinalEn = (n) => {
  const s = ["th", "st", "nd", "rd"];
  const v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
};
```
**PHP**
```php
function ordinalEn(int $n): string {
    $s = ["th", "st", "nd", "rd"];
    $v = $n % 100;
    $suf = $s[($v - 20) % 10] ?? $s[$v] ?? $s[0];
    return $n . $suf;
}
```
**Python**
```python
def ordinal_en(n):
    suffixes = ["th", "st", "nd", "rd"]
    v = n % 100
    if 11 <= v <= 13:
        suf = "th"
    else:
        suf = suffixes[v % 10] if v % 10 < 4 else "th"
    return f"{n}{suf}"
```

<a id="m921"></a>
### 921. Nisbatni soddalashtirish (simplify ratio, gcd bilan)
Ikki sonni eng katta umumiy bo'luvchiga (gcd) bo'lib, nisbatni soddalashtiradi.
`⏱ O(log min(a,b)) · 💾 O(1)`

**JS**
```js
const simplifyRatio = (a, b) => {
  const gcd = (x, y) => (y === 0 ? x : gcd(y, x % y));
  const g = gcd(Math.abs(a), Math.abs(b)) || 1;
  return [a / g, b / g];
};
```
**PHP**
```php
function simplifyRatio(int $a, int $b): array {
    $gcd = function ($x, $y) use (&$gcd) {
        return $y === 0 ? $x : $gcd($y, $x % $y);
    };
    $g = $gcd(abs($a), abs($b)) ?: 1;
    return [intdiv($a, $g), intdiv($b, $g)];
}
```
**Python**
```python
from math import gcd

def simplify_ratio(a, b):
    g = gcd(a, b) or 1
    return (a // g, b // g)
```

<a id="m922"></a>
### 922. Chegaralash (clamp)
Qiymatni berilgan [min, max] oralig'iga "qisib" qaytaradi.

**JS**
```js
const clamp = (value, lo, hi) => Math.max(lo, Math.min(hi, value));
```
**PHP**
```php
function clamp(float $value, float $lo, float $hi): float {
    return max($lo, min($hi, $value));
}
```
**Python**
```python
def clamp(value, lo, hi):
    return max(lo, min(hi, value))
```

<a id="m923"></a>
### 923. O'nlik kasrgacha yaxlitlash (round to decimals)
Sonni berilgan o'nlik xona soniga to'g'ri yaxlitlaydi.

**JS**
```js
const roundTo = (value, decimals = 2) => {
  const f = 10 ** decimals;
  return Math.round((value + Number.EPSILON) * f) / f;
};
```
**PHP**
```php
function roundTo(float $value, int $decimals = 2): float {
    return round($value, $decimals);
}
```
**Python**
```python
def round_to(value, decimals=2):
    return round(value, decimals)
```

<a id="m924"></a>
### 924. Diapazonda tasodifiy butun son (random int)
[min, max] (ikkalasi ham kiritilgan) oralig'ida tasodifiy butun son qaytaradi.

**JS**
```js
const randomInt = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;
```
**PHP**
```php
function randomInt2(int $min, int $max): int {
    return random_int($min, $max);
}
```
**Python**
```python
import random

def random_int(lo, hi):
    return random.randint(lo, hi)
```

<a id="m925"></a>
### 925. Og'irlikli tasodifiy tanlov (weighted random)
Har bir elementning vazniga mutanosib ehtimollik bilan bittasini tanlaydi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const weightedChoice = (items, weights) => {
  const total = weights.reduce((a, b) => a + b, 0);
  let r = Math.random() * total;
  for (let i = 0; i < items.length; i++) {
    r -= weights[i];
    if (r < 0) return items[i];
  }
  return items[items.length - 1];
};
```
**Python**
```python
import random

def weighted_choice(items, weights):
    return random.choices(items, weights=weights, k=1)[0]
```

<a id="m926"></a>
### 926. OTP generatsiya (6 raqamli)
Bir martalik 6 raqamli kodni (kerak bo'lsa boshida nol bilan) generatsiya qiladi.

**JS**
```js
const generateOtp = (digits = 6) => {
  const max = 10 ** digits;
  return Math.floor(Math.random() * max).toString().padStart(digits, "0");
};
```
**PHP**
```php
function generateOtp(int $digits = 6): string {
    $max = (10 ** $digits) - 1;
    return str_pad((string)random_int(0, $max), $digits, "0", STR_PAD_LEFT);
}
```
**Python**
```python
import random

def generate_otp(digits=6):
    return str(random.randint(0, 10 ** digits - 1)).zfill(digits)
```

<a id="m927"></a>
### 927. Fayl hajmini formatlash (human-readable bytes)
Baytlar sonini "1.5 KB", "3.2 MB" ko'rinishidagi o'qiladigan qatorga aylantiradi.

**JS**
```js
const formatBytes = (bytes, decimals = 1) => {
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB", "TB", "PB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  const value = bytes / 1024 ** i;
  return `${value.toFixed(i === 0 ? 0 : decimals)} ${units[i]}`;
};
```
**PHP**
```php
function formatBytes(int $bytes, int $decimals = 1): string {
    if ($bytes === 0) return "0 B";
    $units = ["B", "KB", "MB", "GB", "TB", "PB"];
    $i = (int)floor(log($bytes) / log(1024));
    $value = $bytes / (1024 ** $i);
    return number_format($value, $i === 0 ? 0 : $decimals) . " " . $units[$i];
}
```
**Python**
```python
import math

def format_bytes(num_bytes, decimals=1):
    if num_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = int(math.floor(math.log(num_bytes, 1024)))
    value = num_bytes / 1024 ** i
    return f"{value:.{0 if i == 0 else decimals}f} {units[i]}"
```

<a id="m928"></a>
### 928. Fayl kengaytmasini ajratish (file extension)
Fayl nomidan kengaytmani (nuqtadan keyingi qismni) kichik harfda ajratadi.

**JS**
```js
const fileExtension = (name) => {
  const i = name.lastIndexOf(".");
  return i > 0 ? name.slice(i + 1).toLowerCase() : "";
};
```
**PHP**
```php
function fileExtension(string $name): string {
    return strtolower(pathinfo($name, PATHINFO_EXTENSION));
}
```
**Python**
```python
import os

def file_extension(name):
    return os.path.splitext(name)[1].lstrip(".").lower()
```

<a id="m929"></a>
### 929. Kengaytmadan MIME turi (mime from extension)
Fayl kengaytmasiga qarab tegishli MIME turini qaytaradi.

**JS**
```js
const mimeType = (ext) => {
  const map = {
    txt: "text/plain", html: "text/html", json: "application/json",
    png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg",
    pdf: "application/pdf", csv: "text/csv",
  };
  return map[ext.toLowerCase()] || "application/octet-stream";
};
```
**PHP**
```php
function mimeType(string $ext): string {
    $map = [
        "txt" => "text/plain", "html" => "text/html", "json" => "application/json",
        "png" => "image/png", "jpg" => "image/jpeg", "jpeg" => "image/jpeg",
        "pdf" => "application/pdf", "csv" => "text/csv",
    ];
    return $map[strtolower($ext)] ?? "application/octet-stream";
}
```
**Python**
```python
def mime_type(ext):
    table = {
        "txt": "text/plain", "html": "text/html", "json": "application/json",
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "pdf": "application/pdf", "csv": "text/csv",
    }
    return table.get(ext.lower(), "application/octet-stream")
```

<a id="m930"></a>
### 930. O'qish vaqtini baholash (reading time)
Matndagi so'zlar soniga qarab o'qish uchun ketadigan daqiqalarni baholaydi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const readingTime = (text, wpm = 200) => {
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.ceil(words / wpm));
};
```
**PHP**
```php
function readingTime(string $text, int $wpm = 200): int {
    $words = count(preg_split('/\s+/', trim($text), -1, PREG_SPLIT_NO_EMPTY));
    return max(1, (int)ceil($words / $wpm));
}
```
**Python**
```python
import math

def reading_time(text, wpm=200):
    words = len(text.split())
    return max(1, math.ceil(words / wpm))
```
