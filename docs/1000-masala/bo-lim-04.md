<a id="b4"></a>
# 4-bo'lim: Satrlar

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

<a id="m41"></a>
### 41. Satrni teskari ag'darish

**JS**
```js
const reverse = s => s.split("").reverse().join("");
```
**PHP**
```php
function reverse($s) {
    return strrev($s);
}
```
**Python**
```python
def reverse(s):
    return s[::-1]
```

<a id="m42"></a>
### 42. Palindrom satr

**JS**
```js
const isPalindrome = s => s === s.split("").reverse().join("");
```
**PHP**
```php
function isPalindrome($s) {
    return $s === strrev($s);
}
```
**Python**
```python
def is_palindrome(s):
    return s == s[::-1]
```

<a id="m43"></a>
### 43. Unli harflar soni (vowels)

**JS**
```js
const vowels = s => (s.match(/[aeiou]/gi) || []).length;
```
**PHP**
```php
function vowels($s) {
    return preg_match_all('/[aeiou]/i', $s);
}
```
**Python**
```python
def vowels(s):
    return sum(c.lower() in "aeiou" for c in s)
```

<a id="m44"></a>
### 44. So'zlar soni

**JS**
```js
const wordCount = s => s.trim().split(/\s+/).filter(Boolean).length;
```
**PHP**
```php
function wordCount($s) {
    return count(preg_split('/\s+/', trim($s), -1, PREG_SPLIT_NO_EMPTY));
}
```
**Python**
```python
def word_count(s):
    return len(s.split())
```

<a id="m45"></a>
### 45. Katta-kichik harf almashtirish (swapcase)

**JS**
```js
const swapCase = s => s.replace(/[a-z]/gi, c =>
  c === c.toLowerCase() ? c.toUpperCase() : c.toLowerCase());
```
**PHP**
```php
function swapCase($s) {
    $out = "";
    foreach (str_split($s) as $c) {
        $out .= ctype_upper($c) ? strtolower($c) : strtoupper($c);
    }
    return $out;
}
```
**Python**
```python
def swap_case(s):
    return s.swapcase()
```

<a id="m46"></a>
### 46. Belgi chastotasi (character frequency)

**JS**
```js
const charFreq = s => {
  const f = {};
  for (const c of s) f[c] = (f[c] || 0) + 1;
  return f;
};
```
**PHP**
```php
function charFreq($s) {
    return array_count_values(str_split($s));
}
```
**Python**
```python
from collections import Counter

def char_freq(s):
    return dict(Counter(s))
```

<a id="m47"></a>
### 47. Anagramma tekshirish

**JS**
```js
const isAnagram = (a, b) => {
  const norm = s => s.replace(/\s/g, "").toLowerCase().split("").sort().join("");
  return norm(a) === norm(b);
};
```
**PHP**
```php
function isAnagram($a, $b) {
    $norm = function ($s) {
        $arr = str_split(strtolower(str_replace(" ", "", $s)));
        sort($arr);
        return implode("", $arr);
    };
    return $norm($a) === $norm($b);
}
```
**Python**
```python
def is_anagram(a, b):
    norm = lambda s: sorted(s.replace(" ", "").lower())
    return norm(a) == norm(b)
```

<a id="m48"></a>
### 48. Eng uzun so'z

**JS**
```js
const longestWord = s => s.trim().split(/\s+/).reduce((a, b) => b.length > a.length ? b : a, "");
```
**PHP**
```php
function longestWord($s) {
    $words = preg_split('/\s+/', trim($s));
    usort($words, fn($a, $b) => strlen($b) - strlen($a));
    return $words[0];
}
```
**Python**
```python
def longest_word(s):
    return max(s.split(), key=len)
```

<a id="m49"></a>
### 49. Barcha bo'sh joylarni olib tashlash

**JS**
```js
const stripSpaces = s => s.replace(/\s+/g, "");
```
**PHP**
```php
function stripSpaces($s) {
    return preg_replace('/\s+/', '', $s);
}
```
**Python**
```python
def strip_spaces(s):
    return "".join(s.split())
```

<a id="m50"></a>
### 50. Birinchi takrorlanmas belgi

**JS**
```js
const firstUnique = s => {
  for (const c of s) if (s.indexOf(c) === s.lastIndexOf(c)) return c;
  return null;
};
```
**PHP**
```php
function firstUnique($s) {
    $counts = array_count_values(str_split($s));
    foreach (str_split($s) as $c) if ($counts[$c] === 1) return $c;
    return null;
}
```
**Python**
```python
from collections import Counter

def first_unique(s):
    counts = Counter(s)
    for c in s:
        if counts[c] == 1:
            return c
    return None
```

<a id="m51"></a>
### 51. Qism-satr indeksini topish
Topilmasa: JS/Python −1, PHP false.

**JS**
```js
const indexOf = (s, sub) => s.indexOf(sub);
```
**PHP**
```php
function indexOf($s, $sub) {
    return strpos($s, $sub);
}
```
**Python**
```python
def index_of(s, sub):
    return s.find(sub)
```

<a id="m52"></a>
### 52. Akronim (bosh harflar)
"laravel domain driven" → "LDD".

**JS**
```js
const acronym = s => s.trim().split(/\s+/).map(w => w[0].toUpperCase()).join("");
```
**PHP**
```php
function acronym($s) {
    $words = preg_split('/\s+/', trim($s));
    return implode("", array_map(fn($w) => strtoupper($w[0]), $words));
}
```
**Python**
```python
def acronym(s):
    return "".join(w[0].upper() for w in s.split())
```

<a id="m53"></a>
### 53. Faqat harflarni qoldirish

**JS**
```js
const lettersOnly = s => s.replace(/[^a-z]/gi, "");
```
**PHP**
```php
function lettersOnly($s) {
    return preg_replace('/[^a-z]/i', '', $s);
}
```
**Python**
```python
def letters_only(s):
    return "".join(c for c in s if c.isalpha())
```

<a id="m54"></a>
### 54. Har bir so'zni teskari ag'darish
"abc def" → "cba fed".

**JS**
```js
const reverseWords = s => s.split(" ").map(w => w.split("").reverse().join("")).join(" ");
```
**PHP**
```php
function reverseWords($s) {
    return implode(" ", array_map('strrev', explode(" ", $s)));
}
```
**Python**
```python
def reverse_words(s):
    return " ".join(w[::-1] for w in s.split(" "))
```

<a id="m55"></a>
### 55. camelCase → snake_case
"helloWorld" → "hello_world".

**JS**
```js
const toSnake = s => s.replace(/[A-Z]/g, c => "_" + c.toLowerCase());
```
**PHP**
```php
function toSnake($s) {
    return strtolower(preg_replace('/([A-Z])/', '_$1', $s));
}
```
**Python**
```python
import re

def to_snake(s):
    return re.sub(r"[A-Z]", lambda m: "_" + m.group().lower(), s)
```

---
