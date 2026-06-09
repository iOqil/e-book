<a id="b1"></a>
# 1-bo'lim: Asoslar

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

<a id="m1"></a>
### 1. Hello World
Ekranga matn chiqarish.

**JS**
```js
console.log("Hello, World!");
```
**PHP**
```php
echo "Hello, World!";
```
**Python**
```python
print("Hello, World!")
```

<a id="m2"></a>
### 2. Ikki sonni qo'shish
Ikki sonni qabul qilib, yig'indisini qaytaradi.

**JS**
```js
const add = (a, b) => a + b;
```
**PHP**
```php
function add($a, $b) {
    return $a + $b;
}
```
**Python**
```python
def add(a, b):
    return a + b
```

<a id="m3"></a>
### 3. O'zgaruvchilarni almashtirish (swap)
Ikki o'zgaruvchi qiymatini almashtirish.

**JS**
```js
[a, b] = [b, a];
```
**PHP**
```php
[$a, $b] = [$b, $a];
```
**Python**
```python
a, b = b, a
```

<a id="m4"></a>
### 4. Aylana yuzasi
Radius bo'yicha aylana yuzasi (πr²).

**JS**
```js
const circleArea = r => Math.PI * r ** 2;
```
**PHP**
```php
function circleArea($r) {
    return M_PI * $r ** 2;
}
```
**Python**
```python
import math

def circle_area(r):
    return math.pi * r ** 2
```

<a id="m5"></a>
### 5. Salomlashish
Ismni qabul qilib, salomlashish matnini qaytaradi.

**JS**
```js
const greet = name => `Salom, ${name}!`;
```
**PHP**
```php
function greet($name) {
    return "Salom, $name!";
}
```
**Python**
```python
def greet(name):
    return f"Salom, {name}!"
```

<a id="m6"></a>
### 6. Selsiy → Farengeyt
Haroratni Selsiydan Farengeytga aylantirish.

**JS**
```js
const cToF = c => c * 9 / 5 + 32;
```
**PHP**
```php
function cToF($c) {
    return $c * 9 / 5 + 32;
}
```
**Python**
```python
def c_to_f(c):
    return c * 9 / 5 + 32
```

<a id="m7"></a>
### 7. Juft yoki toq
Son juftligini tekshirish.

**JS**
```js
const isEven = n => n % 2 === 0;
```
**PHP**
```php
function isEven($n) {
    return $n % 2 === 0;
}
```
**Python**
```python
def is_even(n):
    return n % 2 == 0
```

<a id="m8"></a>
### 8. Ikki sondan kattasi

**JS**
```js
const max2 = (a, b) => a > b ? a : b;
```
**PHP**
```php
function max2($a, $b) {
    return $a > $b ? $a : $b;
}
```
**Python**
```python
def max2(a, b):
    return a if a > b else b
```

<a id="m9"></a>
### 9. Uch sondan kattasi

**JS**
```js
const max3 = (a, b, c) => Math.max(a, b, c);
```
**PHP**
```php
function max3($a, $b, $c) {
    return max($a, $b, $c);
}
```
**Python**
```python
def max3(a, b, c):
    return max(a, b, c)
```

<a id="m10"></a>
### 10. Sonning ishorasi
Musbat / manfiy / nol ekanini aniqlash.

**JS**
```js
const sign = n => n > 0 ? "musbat" : n < 0 ? "manfiy" : "nol";
```
**PHP**
```php
function sign($n) {
    return $n > 0 ? "musbat" : ($n < 0 ? "manfiy" : "nol");
}
```
**Python**
```python
def sign(n):
    return "musbat" if n > 0 else "manfiy" if n < 0 else "nol"
```

<a id="m11"></a>
### 11. Kabisa yil (leap year)

**JS**
```js
const isLeap = y => (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
```
**PHP**
```php
function isLeap($y) {
    return ($y % 4 === 0 && $y % 100 !== 0) || $y % 400 === 0;
}
```
**Python**
```python
def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
```

<a id="m12"></a>
### 12. Sekundlarni HH:MM:SS formatiga

**JS**
```js
const fmtTime = s => {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return [h, m, sec].map(x => String(x).padStart(2, "0")).join(":");
};
```
**PHP**
```php
function fmtTime($s) {
    return sprintf("%02d:%02d:%02d", intdiv($s, 3600), intdiv($s % 3600, 60), $s % 60);
}
```
**Python**
```python
def fmt_time(s):
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"
```

<a id="m13"></a>
### 13. Oddiy kalkulyator
Ikki son va amal bo'yicha natija.

**JS**
```js
const calc = (a, op, b) => {
  switch (op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "/": return b !== 0 ? a / b : "0 ga bo'lib bo'lmaydi";
  }
};
```
**PHP**
```php
function calc($a, $op, $b) {
    return match ($op) {
        "+" => $a + $b,
        "-" => $a - $b,
        "*" => $a * $b,
        "/" => $b != 0 ? $a / $b : "0 ga bo'lib bo'lmaydi",
    };
}
```
**Python**
```python
def calc(a, op, b):
    table = {
        "+": a + b,
        "-": a - b,
        "*": a * b,
        "/": a / b if b != 0 else "0 ga bo'lib bo'lmaydi",
    }
    return table[op]
```

<a id="m14"></a>
### 14. BMI (tana massasi indeksi)
kg / m².

**JS**
```js
const bmi = (kg, m) => +(kg / m ** 2).toFixed(1);
```
**PHP**
```php
function bmi($kg, $m) {
    return round($kg / $m ** 2, 1);
}
```
**Python**
```python
def bmi(kg, m):
    return round(kg / m ** 2, 1)
```

<a id="m15"></a>
### 15. Chegirma narxi
Narx va chegirma foizi bo'yicha yakuniy narx.

**JS**
```js
const discount = (price, pct) => price - price * pct / 100;
```
**PHP**
```php
function discount($price, $pct) {
    return $price - $price * $pct / 100;
}
```
**Python**
```python
def discount(price, pct):
    return price - price * pct / 100
```

---
