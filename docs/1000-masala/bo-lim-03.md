<a id="b3"></a>
# 3-bo'lim: Sonlar va matematika

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

<a id="m26"></a>
### 26. Tub son tekshirish

**JS**
```js
const isPrime = n => {
  if (n < 2) return false;
  for (let i = 2; i * i <= n; i++) if (n % i === 0) return false;
  return true;
};
```
**PHP**
```php
function isPrime($n) {
    if ($n < 2) return false;
    for ($i = 2; $i * $i <= $n; $i++) if ($n % $i === 0) return false;
    return true;
}
```
**Python**
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

<a id="m27"></a>
### 27. N tagacha tub sonlar

**JS**
```js
const primes = n => Array.from({ length: n - 1 }, (_, i) => i + 2).filter(isPrime);
```
**PHP**
```php
function primes($n) {
    return array_values(array_filter(range(2, $n), 'isPrime'));
}
```
**Python**
```python
def primes(n):
    return [x for x in range(2, n + 1) if is_prime(x)]
```

<a id="m28"></a>
### 28. EKUB — eng katta umumiy bo'luvchi (GCD)

**JS**
```js
const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
```
**PHP**
```php
function gcd($a, $b) {
    return $b === 0 ? $a : gcd($b, $a % $b);
}
```
**Python**
```python
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)
```

<a id="m29"></a>
### 29. EKUK — eng kichik umumiy karrali (LCM)

**JS**
```js
const lcm = (a, b) => a / gcd(a, b) * b;
```
**PHP**
```php
function lcm($a, $b) {
    return $a / gcd($a, $b) * $b;
}
```
**Python**
```python
def lcm(a, b):
    return a // gcd(a, b) * b
```

<a id="m30"></a>
### 30. Mukammal son (perfect number)
Bo'luvchilari yig'indisi o'ziga teng (mas: 6, 28).

**JS**
```js
const isPerfect = n => {
  let sum = 0;
  for (let i = 1; i < n; i++) if (n % i === 0) sum += i;
  return sum === n;
};
```
**PHP**
```php
function isPerfect($n) {
    $sum = 0;
    for ($i = 1; $i < $n; $i++) if ($n % $i === 0) $sum += $i;
    return $sum === $n;
}
```
**Python**
```python
def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n
```

<a id="m31"></a>
### 31. Armstrong soni
Har raqamning (raqamlar soni)-darajasi yig'indisi songa teng (mas: 153).

**JS**
```js
const isArmstrong = n => {
  const d = String(n).split("");
  const p = d.length;
  return d.reduce((s, x) => s + (+x) ** p, 0) === n;
};
```
**PHP**
```php
function isArmstrong($n) {
    $d = str_split((string) $n);
    $p = count($d);
    return array_sum(array_map(fn($x) => $x ** $p, $d)) === $n;
}
```
**Python**
```python
def is_armstrong(n):
    d = str(n)
    p = len(d)
    return sum(int(x) ** p for x in d) == n
```

<a id="m32"></a>
### 32. Palindrom son

**JS**
```js
const isPalindromeNum = n => String(n) === String(n).split("").reverse().join("");
```
**PHP**
```php
function isPalindromeNum($n) {
    return (string) $n === strrev((string) $n);
}
```
**Python**
```python
def is_palindrome_num(n):
    return str(n) == str(n)[::-1]
```

<a id="m33"></a>
### 33. O'nlikdan ikkilikka (decimal → binary)

**JS**
```js
const toBinary = n => n.toString(2);
```
**PHP**
```php
function toBinary($n) {
    return decbin($n);
}
```
**Python**
```python
def to_binary(n):
    return bin(n)[2:]
```

<a id="m34"></a>
### 34. Ikkilikdan o'nlikka (binary → decimal)

**JS**
```js
const fromBinary = s => parseInt(s, 2);
```
**PHP**
```php
function fromBinary($s) {
    return bindec($s);
}
```
**Python**
```python
def from_binary(s):
    return int(s, 2)
```

<a id="m35"></a>
### 35. O'rta arifmetik (average)

**JS**
```js
const avg = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
```
**PHP**
```php
function avg($arr) {
    return array_sum($arr) / count($arr);
}
```
**Python**
```python
def avg(arr):
    return sum(arr) / len(arr)
```

<a id="m36"></a>
### 36. Sonning bo'luvchilari (divisors)

**JS**
```js
const divisors = n => Array.from({ length: n }, (_, i) => i + 1).filter(i => n % i === 0);
```
**PHP**
```php
function divisors($n) {
    return array_values(array_filter(range(1, $n), fn($i) => $n % $i === 0));
}
```
**Python**
```python
def divisors(n):
    return [i for i in range(1, n + 1) if n % i == 0]
```

<a id="m37"></a>
### 37. Tub ko'paytuvchilarga ajratish (prime factorization)
60 → [2, 2, 3, 5].

**JS**
```js
const primeFactors = n => {
  const f = [];
  for (let d = 2; d * d <= n; d++) {
    while (n % d === 0) { f.push(d); n /= d; }
  }
  if (n > 1) f.push(n);
  return f;
};
```
**PHP**
```php
function primeFactors($n) {
    $f = [];
    for ($d = 2; $d * $d <= $n; $d++) {
        while ($n % $d === 0) { $f[] = $d; $n /= $d; }
    }
    if ($n > 1) $f[] = $n;
    return $f;
}
```
**Python**
```python
def prime_factors(n):
    f = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            f.append(d)
            n //= d
        d += 1
    if n > 1:
        f.append(n)
    return f
```

<a id="m38"></a>
### 38. Ikki son orasidagi tub sonlar

**JS**
```js
const primesBetween = (a, b) => {
  const r = [];
  for (let i = a; i <= b; i++) if (isPrime(i)) r.push(i);
  return r;
};
```
**PHP**
```php
function primesBetween($a, $b) {
    return array_values(array_filter(range($a, $b), 'isPrime'));
}
```
**Python**
```python
def primes_between(a, b):
    return [i for i in range(a, b + 1) if is_prime(i)]
```

<a id="m39"></a>
### 39. Kvadrat tenglama yechimi
ax² + bx + c = 0.

**JS**
```js
const quadratic = (a, b, c) => {
  const d = b * b - 4 * a * c;
  if (d < 0) return [];
  const sq = Math.sqrt(d);
  return d === 0 ? [-b / (2 * a)] : [(-b + sq) / (2 * a), (-b - sq) / (2 * a)];
};
```
**PHP**
```php
function quadratic($a, $b, $c) {
    $d = $b * $b - 4 * $a * $c;
    if ($d < 0) return [];
    $sq = sqrt($d);
    return $d == 0
        ? [-$b / (2 * $a)]
        : [(-$b + $sq) / (2 * $a), (-$b - $sq) / (2 * $a)];
}
```
**Python**
```python
import math

def quadratic(a, b, c):
    d = b * b - 4 * a * c
    if d < 0:
        return []
    sq = math.sqrt(d)
    if d == 0:
        return [-b / (2 * a)]
    return [(-b + sq) / (2 * a), (-b - sq) / (2 * a)]
```

<a id="m40"></a>
### 40. Foiz hisoblash
part dan whole gacha foiz.

**JS**
```js
const percent = (part, whole) => part / whole * 100;
```
**PHP**
```php
function percent($part, $whole) {
    return $part / $whole * 100;
}
```
**Python**
```python
def percent(part, whole):
    return part / whole * 100
```

---
