<a id="b2"></a>
# 2-bo'lim: Sikllar

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

<a id="m16"></a>
### 16. 1 dan N gacha yig'indi

**JS**
```js
const sumTo = n => n * (n + 1) / 2;
```
**PHP**
```php
function sumTo($n) {
    return $n * ($n + 1) / 2;
}
```
**Python**
```python
def sum_to(n):
    return n * (n + 1) // 2
```

<a id="m17"></a>
### 17. N tagacha juft sonlar
Juft sonlar ro'yxati.

**JS**
```js
const evens = n => Array.from({ length: n }, (_, i) => i + 1).filter(x => x % 2 === 0);
```
**PHP**
```php
function evens($n) {
    return array_values(array_filter(range(1, $n), fn($x) => $x % 2 === 0));
}
```
**Python**
```python
def evens(n):
    return [x for x in range(1, n + 1) if x % 2 == 0]
```

<a id="m18"></a>
### 18. Ko'paytirish jadvali (n × 1..10)

**JS**
```js
const table = n => Array.from({ length: 10 }, (_, i) => `${n} x ${i + 1} = ${n * (i + 1)}`);
```
**PHP**
```php
function table($n) {
    $out = [];
    for ($i = 1; $i <= 10; $i++) {
        $out[] = "$n x $i = " . ($n * $i);
    }
    return $out;
}
```
**Python**
```python
def table(n):
    return [f"{n} x {i} = {n * i}" for i in range(1, 11)]
```

<a id="m19"></a>
### 19. Faktorial

**JS**
```js
const fact = n => n <= 1 ? 1 : n * fact(n - 1);
```
**PHP**
```php
function fact($n) {
    return $n <= 1 ? 1 : $n * fact($n - 1);
}
```
**Python**
```python
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)
```

<a id="m20"></a>
### 20. Raqamlar yig'indisi
Masalan: 1234 → 1+2+3+4 = 10.

**JS**
```js
const digitSum = n => String(Math.abs(n)).split("").reduce((s, d) => s + +d, 0);
```
**PHP**
```php
function digitSum($n) {
    return array_sum(str_split((string) abs($n)));
}
```
**Python**
```python
def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))
```

<a id="m21"></a>
### 21. Raqamlar soni

**JS**
```js
const digitCount = n => String(Math.abs(n)).length;
```
**PHP**
```php
function digitCount($n) {
    return strlen((string) abs($n));
}
```
**Python**
```python
def digit_count(n):
    return len(str(abs(n)))
```

<a id="m22"></a>
### 22. Sonni teskari ag'darish
123 → 321 (musbat butun sonlar).

**JS**
```js
const reverseNum = n => Number(String(n).split("").reverse().join(""));
```
**PHP**
```php
function reverseNum($n) {
    return (int) strrev((string) $n);
}
```
**Python**
```python
def reverse_num(n):
    return int(str(n)[::-1])
```

<a id="m23"></a>
### 23. Daraja (qo'lda hisoblash)
base^exp.

**JS**
```js
const power = (b, e) => {
  let r = 1;
  for (let i = 0; i < e; i++) r *= b;
  return r;
};
```
**PHP**
```php
function power($b, $e) {
    $r = 1;
    for ($i = 0; $i < $e; $i++) $r *= $b;
    return $r;
}
```
**Python**
```python
def power(b, e):
    r = 1
    for _ in range(e):
        r *= b
    return r
```

<a id="m24"></a>
### 24. To'g'ri burchakli uchburchak (yulduzcha)

**JS**
```js
const triangle = n => Array.from({ length: n }, (_, i) => "*".repeat(i + 1)).join("\n");
```
**PHP**
```php
function triangle($n) {
    $out = [];
    for ($i = 1; $i <= $n; $i++) $out[] = str_repeat("*", $i);
    return implode("\n", $out);
}
```
**Python**
```python
def triangle(n):
    return "\n".join("*" * i for i in range(1, n + 1))
```

<a id="m25"></a>
### 25. Fibonachchi (birinchi n ta)

**JS**
```js
const fib = n => {
  const r = [0, 1];
  for (let i = 2; i < n; i++) r.push(r[i - 1] + r[i - 2]);
  return r.slice(0, n);
};
```
**PHP**
```php
function fib($n) {
    $r = [0, 1];
    for ($i = 2; $i < $n; $i++) $r[] = $r[$i - 1] + $r[$i - 2];
    return array_slice($r, 0, $n);
}
```
**Python**
```python
def fib(n):
    r = [0, 1]
    for i in range(2, n):
        r.append(r[i - 1] + r[i - 2])
    return r[:n]
```

---
