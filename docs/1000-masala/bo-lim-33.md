<a id="b33"></a>
# 33-bo'lim: Funksional dasturlash

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Funksional dasturlash (functional programming) — funksiyalarni qiymat sifatida uzatish, ularni
> birlashtirish va o'zgarmas (immutable) ma'lumotlar ustida ishlashga asoslangan uslub. Bu bo'limda
> compose/pipe, curry, memoize kabi yuqori tartibli (higher-order) funksiyalar va map/filter/reduce
> kabi klassik kombinatorlar qo'lda yoziladi. Maqsad — kutubxonadan foydalanish emas, balki bu
> abstraksiyalar ichkaridan qanday ishlashini tushunish. Kod JS, PHP va Python tillarida idiomatik
> ko'rinishda beriladi; generator/lazy mavzularida JS va Python yetarli.

<a id="m697"></a>
### 697. compose (funksiyalarni o'ngdan birlashtirish)
Bir nechta funksiyani birlashtiradi: oxirgisi birinchi ishlaydi, natijasi keyingisiga uzatiladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const compose = (...fns) => (x) =>
  fns.reduceRight((acc, f) => f(acc), x);
// compose(x => x + 1, x => x * 2)(5) // 11
```
**PHP**
```php
function compose(callable ...$fns): callable {
    return fn($x) => array_reduce(
        array_reverse($fns),
        fn($acc, $f) => $f($acc),
        $x
    );
}
// compose(fn($x) => $x + 1, fn($x) => $x * 2)(5) // 11
```
**Python**
```python
from functools import reduce

def compose(*fns):
    return lambda x: reduce(lambda acc, f: f(acc), reversed(fns), x)
# compose(lambda x: x + 1, lambda x: x * 2)(5)  # 11
```

<a id="m698"></a>
### 698. pipe (funksiyalarni chapdan birlashtirish)
compose'ning teskarisi: funksiyalar yozilgan tartibda chapdan o'ngga qo'llanadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const pipe = (...fns) => (x) =>
  fns.reduce((acc, f) => f(acc), x);
// pipe(x => x + 1, x => x * 2)(5) // 12
```
**PHP**
```php
function pipe(callable ...$fns): callable {
    return fn($x) => array_reduce($fns, fn($acc, $f) => $f($acc), $x);
}
// pipe(fn($x) => $x + 1, fn($x) => $x * 2)(5) // 12
```
**Python**
```python
from functools import reduce

def pipe(*fns):
    return lambda x: reduce(lambda acc, f: f(acc), fns, x)
# pipe(lambda x: x + 1, lambda x: x * 2)(5)  # 12
```

<a id="m699"></a>
### 699. curry (argumentlarni bo'lib uzatish)
Ko'p argumentli funksiyani har biri bitta argument oluvchi funksiyalar zanjiriga aylantiradi.

**JS**
```js
const curry = (fn) => {
  const helper = (...args) =>
    args.length >= fn.length
      ? fn(...args)
      : (...more) => helper(...args, ...more);
  return helper;
};
const add = curry((a, b, c) => a + b + c);
// add(1)(2)(3) // 6 ; add(1, 2)(3) // 6
```
**PHP**
```php
function curry(callable $fn, int $arity): callable {
    $helper = function (array $args) use (&$helper, $fn, $arity) {
        if (count($args) >= $arity) {
            return $fn(...$args);
        }
        return fn(...$more) => $helper([...$args, ...$more]);
    };
    return fn(...$args) => $helper($args);
}
$add = curry(fn($a, $b, $c) => $a + $b + $c, 3);
// $add(1)(2)(3) // 6
```
**Python**
```python
def curry(fn, arity):
    def helper(args):
        if len(args) >= arity:
            return fn(*args)
        return lambda *more: helper(args + list(more))
    return lambda *args: helper(list(args))

add = curry(lambda a, b, c: a + b + c, 3)
# add(1)(2)(3)  # 6
```

<a id="m700"></a>
### 700. partial application (qisman qo'llash)
Funksiyaning ba'zi argumentlarini oldindan biriktirib, qolganini keyin qabul qiluvchi yangi funksiya yaratadi.

**JS**
```js
const partial = (fn, ...preset) =>
  (...rest) => fn(...preset, ...rest);
const greet = (greeting, name) => `${greeting}, ${name}!`;
const hello = partial(greet, "Salom");
// hello("Olim") // "Salom, Olim!"
```
**PHP**
```php
function partial(callable $fn, ...$preset): callable {
    return fn(...$rest) => $fn(...$preset, ...$rest);
}
$greet = fn($g, $name) => "$g, $name!";
$hello = partial($greet, "Salom");
// $hello("Olim") // "Salom, Olim!"
```
**Python**
```python
def partial(fn, *preset):
    return lambda *rest: fn(*preset, *rest)

greet = lambda g, name: f"{g}, {name}!"
hello = partial(greet, "Salom")
# hello("Olim")  # "Salom, Olim!"
```

<a id="m701"></a>
### 701. memoize (natijalarni keshlash)
Funksiya natijalarini argumentlar bo'yicha keshda saqlaydi; takror chaqiruvda hisoblamay keshdan qaytaradi.
`⏱ chaqiruv O(1) (keshda) · 💾 O(noyob argumentlar)`

**JS**
```js
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};
// const slow = memoize(n => n * n); slow(4) // 16 (ikkinchi chaqiruv keshdan)
```
**PHP**
```php
function memoize(callable $fn): callable {
    $cache = [];
    return function (...$args) use (&$cache, $fn) {
        $key = serialize($args);
        if (!array_key_exists($key, $cache)) {
            $cache[$key] = $fn(...$args);
        }
        return $cache[$key];
    };
}
// $slow = memoize(fn($n) => $n * $n); $slow(4) // 16
```
**Python**
```python
def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper
# slow = memoize(lambda n: n * n); slow(4)  # 16
```

<a id="m702"></a>
### 702. once (faqat bir marta ishlaydigan funksiya)
Funksiyani faqat birinchi chaqiruvda bajaradi; keyingi chaqiruvlarda saqlangan natijani qaytaradi.

**JS**
```js
const once = (fn) => {
  let called = false, result;
  return (...args) => {
    if (!called) { called = true; result = fn(...args); }
    return result;
  };
};
// const init = once(() => Math.random()); init() === init() // true
```
**PHP**
```php
function once(callable $fn): callable {
    $called = false;
    $result = null;
    return function (...$args) use (&$called, &$result, $fn) {
        if (!$called) { $called = true; $result = $fn(...$args); }
        return $result;
    };
}
// $init = once(fn() => mt_rand()); $init() === $init() // true
```
**Python**
```python
def once(fn):
    state = {"called": False, "result": None}
    def wrapper(*args):
        if not state["called"]:
            state["called"] = True
            state["result"] = fn(*args)
        return state["result"]
    return wrapper
# init = once(lambda: __import__("random").random()); init() == init()  # True
```

<a id="m703"></a>
### 703. map (qo'lda)
Har bir elementga funksiyani qo'llab, yangi ro'yxat yasaydi (kutubxonasiz).
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const map = (fn, arr) => {
  const out = [];
  for (const v of arr) out.push(fn(v));
  return out;
};
// map(x => x * 2, [1, 2, 3]) // [2, 4, 6]
```
**PHP**
```php
function mymap(callable $fn, array $arr): array {
    $out = [];
    foreach ($arr as $v) $out[] = $fn($v);
    return $out;
}
// mymap(fn($x) => $x * 2, [1, 2, 3]) // [2, 4, 6]
```
**Python**
```python
def my_map(fn, arr):
    out = []
    for v in arr:
        out.append(fn(v))
    return out
# my_map(lambda x: x * 2, [1, 2, 3])  # [2, 4, 6]
```

<a id="m704"></a>
### 704. filter (qo'lda)
Shartni (predikatni) qanoatlantiruvchi elementlarni saqlab qoladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const filter = (pred, arr) => {
  const out = [];
  for (const v of arr) if (pred(v)) out.push(v);
  return out;
};
// filter(x => x % 2 === 0, [1, 2, 3, 4]) // [2, 4]
```
**PHP**
```php
function myfilter(callable $pred, array $arr): array {
    $out = [];
    foreach ($arr as $v) if ($pred($v)) $out[] = $v;
    return $out;
}
// myfilter(fn($x) => $x % 2 === 0, [1, 2, 3, 4]) // [2, 4]
```
**Python**
```python
def my_filter(pred, arr):
    out = []
    for v in arr:
        if pred(v):
            out.append(v)
    return out
# my_filter(lambda x: x % 2 == 0, [1, 2, 3, 4])  # [2, 4]
```

<a id="m705"></a>
### 705. reduce (qo'lda)
Ro'yxatni boshlang'ich qiymatdan boshlab bitta natijaga yig'adi (fold).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const reduce = (fn, init, arr) => {
  let acc = init;
  for (const v of arr) acc = fn(acc, v);
  return acc;
};
// reduce((a, b) => a + b, 0, [1, 2, 3, 4]) // 10
```
**PHP**
```php
function myreduce(callable $fn, $init, array $arr) {
    $acc = $init;
    foreach ($arr as $v) $acc = $fn($acc, $v);
    return $acc;
}
// myreduce(fn($a, $b) => $a + $b, 0, [1, 2, 3, 4]) // 10
```
**Python**
```python
def my_reduce(fn, init, arr):
    acc = init
    for v in arr:
        acc = fn(acc, v)
    return acc
# my_reduce(lambda a, b: a + b, 0, [1, 2, 3, 4])  # 10
```

<a id="m706"></a>
### 706. flatMap (map + bitta darajaga yassilash)
Har bir elementga funksiyani qo'llaydi, natija ro'yxatlarini bitta tekis ro'yxatga qo'shadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const flatMap = (fn, arr) =>
  arr.reduce((acc, v) => acc.concat(fn(v)), []);
// flatMap(x => [x, x * 10], [1, 2]) // [1, 10, 2, 20]
```
**PHP**
```php
function flatMap(callable $fn, array $arr): array {
    $out = [];
    foreach ($arr as $v) {
        foreach ((array) $fn($v) as $u) $out[] = $u;
    }
    return $out;
}
// flatMap(fn($x) => [$x, $x * 10], [1, 2]) // [1, 10, 2, 20]
```
**Python**
```python
def flat_map(fn, arr):
    out = []
    for v in arr:
        out.extend(fn(v))
    return out
# flat_map(lambda x: [x, x * 10], [1, 2])  # [1, 10, 2, 20]
```

<a id="m707"></a>
### 707. zip (ikki ro'yxatni juftlash)
Ikki (yoki undan ko'p) ro'yxatni element-element juftlab, juftliklar ro'yxatini qaytaradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const zip = (a, b) => {
  const n = Math.min(a.length, b.length);
  const out = [];
  for (let i = 0; i < n; i++) out.push([a[i], b[i]]);
  return out;
};
// zip([1, 2, 3], ["a", "b"]) // [[1,"a"],[2,"b"]]
```
**PHP**
```php
function zip(array $a, array $b): array {
    $n = min(count($a), count($b));
    $out = [];
    for ($i = 0; $i < $n; $i++) $out[] = [$a[$i], $b[$i]];
    return $out;
}
// zip([1, 2, 3], ["a", "b"]) // [[1,"a"],[2,"b"]]
```
**Python**
```python
def my_zip(a, b):
    return [(a[i], b[i]) for i in range(min(len(a), len(b)))]
# my_zip([1, 2, 3], ["a", "b"])  # [(1,"a"),(2,"b")]
```

<a id="m708"></a>
### 708. unzip (juftliklarni ikki ro'yxatga ajratish)
zip'ning teskarisi: juftliklar ro'yxatini ikkita alohida ro'yxatga ajratadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const unzip = (pairs) => {
  const a = [], b = [];
  for (const [x, y] of pairs) { a.push(x); b.push(y); }
  return [a, b];
};
// unzip([[1,"a"],[2,"b"]]) // [[1,2],["a","b"]]
```
**PHP**
```php
function unzip(array $pairs): array {
    $a = []; $b = [];
    foreach ($pairs as [$x, $y]) { $a[] = $x; $b[] = $y; }
    return [$a, $b];
}
// unzip([[1,"a"],[2,"b"]]) // [[1,2],["a","b"]]
```
**Python**
```python
def unzip(pairs):
    a, b = [], []
    for x, y in pairs:
        a.append(x)
        b.append(y)
    return a, b
# unzip([(1,"a"),(2,"b")])  # ([1,2],["a","b"])
```

<a id="m709"></a>
### 709. groupBy (kalit bo'yicha guruhlash)
Har bir elementdan kalit hisoblab, shu kalit ostidagi ro'yxatlarga to'playdi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const groupBy = (keyFn, arr) => {
  const out = {};
  for (const v of arr) {
    const k = keyFn(v);
    (out[k] ??= []).push(v);
  }
  return out;
};
// groupBy(x => x % 2, [1, 2, 3, 4]) // {1:[1,3], 0:[2,4]}
```
**PHP**
```php
function groupBy(callable $keyFn, array $arr): array {
    $out = [];
    foreach ($arr as $v) $out[$keyFn($v)][] = $v;
    return $out;
}
// groupBy(fn($x) => $x % 2, [1, 2, 3, 4]) // [1=>[1,3], 0=>[2,4]]
```
**Python**
```python
def group_by(key_fn, arr):
    out = {}
    for v in arr:
        out.setdefault(key_fn(v), []).append(v)
    return out
# group_by(lambda x: x % 2, [1, 2, 3, 4])  # {1:[1,3], 0:[2,4]}
```

<a id="m710"></a>
### 710. partition (shartga ko'ra ikkiga bo'lish)
Ro'yxatni predikat bo'yicha ikkiga ajratadi: rost va yolg'on bo'lganlar.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const partition = (pred, arr) => {
  const yes = [], no = [];
  for (const v of arr) (pred(v) ? yes : no).push(v);
  return [yes, no];
};
// partition(x => x > 2, [1, 2, 3, 4]) // [[3,4],[1,2]]
```
**PHP**
```php
function partition(callable $pred, array $arr): array {
    $yes = []; $no = [];
    foreach ($arr as $v) {
        if ($pred($v)) $yes[] = $v; else $no[] = $v;
    }
    return [$yes, $no];
}
// partition(fn($x) => $x > 2, [1, 2, 3, 4]) // [[3,4],[1,2]]
```
**Python**
```python
def partition(pred, arr):
    yes, no = [], []
    for v in arr:
        (yes if pred(v) else no).append(v)
    return yes, no
# partition(lambda x: x > 2, [1, 2, 3, 4])  # ([3,4],[1,2])
```

<a id="m711"></a>
### 711. chunk (bo'laklarga bo'lish)
Ro'yxatni belgilangan o'lchamli ketma-ket bo'laklarga ajratadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const chunk = (size, arr) => {
  const out = [];
  for (let i = 0; i < arr.length; i += size)
    out.push(arr.slice(i, i + size));
  return out;
};
// chunk(2, [1, 2, 3, 4, 5]) // [[1,2],[3,4],[5]]
```
**PHP**
```php
function chunk(int $size, array $arr): array {
    $out = [];
    for ($i = 0; $i < count($arr); $i += $size)
        $out[] = array_slice($arr, $i, $size);
    return $out;
}
// chunk(2, [1, 2, 3, 4, 5]) // [[1,2],[3,4],[5]]
```
**Python**
```python
def chunk(size, arr):
    return [arr[i:i + size] for i in range(0, len(arr), size)]
# chunk(2, [1, 2, 3, 4, 5])  # [[1,2],[3,4],[5]]
```

<a id="m712"></a>
### 712. deep flatten (chuqur yassilash)
Ixtiyoriy chuqurlikdagi ichma-ich ro'yxatlarni bitta tekis ro'yxatga aylantiradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const deepFlatten = (arr) =>
  arr.reduce(
    (acc, v) => acc.concat(Array.isArray(v) ? deepFlatten(v) : v),
    []
  );
// deepFlatten([1, [2, [3, [4]]], 5]) // [1, 2, 3, 4, 5]
```
**PHP**
```php
function deepFlatten(array $arr): array {
    $out = [];
    foreach ($arr as $v) {
        if (is_array($v)) {
            foreach (deepFlatten($v) as $u) $out[] = $u;
        } else {
            $out[] = $v;
        }
    }
    return $out;
}
// deepFlatten([1, [2, [3, [4]]], 5]) // [1, 2, 3, 4, 5]
```
**Python**
```python
def deep_flatten(arr):
    out = []
    for v in arr:
        if isinstance(v, list):
            out.extend(deep_flatten(v))
        else:
            out.append(v)
    return out
# deep_flatten([1, [2, [3, [4]]], 5])  # [1, 2, 3, 4, 5]
```

<a id="m713"></a>
### 713. pluck (xossani ajratish)
Obyektlar ro'yxatidan berilgan xossa (key) qiymatlarini yig'ib oladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const pluck = (key, arr) => arr.map((o) => o[key]);
// pluck("name", [{name: "Olim"}, {name: "Vali"}]) // ["Olim", "Vali"]
```
**PHP**
```php
function pluck(string $key, array $arr): array {
    return array_map(fn($o) => $o[$key], $arr);
}
// pluck("name", [["name" => "Olim"], ["name" => "Vali"]]) // ["Olim", "Vali"]
```
**Python**
```python
def pluck(key, arr):
    return [o[key] for o in arr]
# pluck("name", [{"name": "Olim"}, {"name": "Vali"}])  # ["Olim", "Vali"]
```

<a id="m714"></a>
### 714. path getter (yo'l bo'yicha qiymat olish)
Ichma-ich strukturadan kalitlar yo'li bo'yicha qiymatni oladi; topilmasa standart qiymat qaytaradi.
`⏱ O(k) · 💾 O(1)`

**JS**
```js
const getPath = (obj, path, def = undefined) => {
  let cur = obj;
  for (const key of path) {
    if (cur == null || !(key in cur)) return def;
    cur = cur[key];
  }
  return cur;
};
// getPath({a: {b: {c: 7}}}, ["a", "b", "c"]) // 7
```
**PHP**
```php
function getPath(array $obj, array $path, $def = null) {
    $cur = $obj;
    foreach ($path as $key) {
        if (!is_array($cur) || !array_key_exists($key, $cur)) return $def;
        $cur = $cur[$key];
    }
    return $cur;
}
// getPath(["a" => ["b" => ["c" => 7]]], ["a", "b", "c"]) // 7
```
**Python**
```python
def get_path(obj, path, default=None):
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur
# get_path({"a": {"b": {"c": 7}}}, ["a", "b", "c"])  # 7
```

<a id="m715"></a>
### 715. negate / complement (predikatni teskarilash)
Predikatni qabul qilib, uning natijasini teskari qiluvchi yangi predikat qaytaradi.

**JS**
```js
const negate = (pred) => (...args) => !pred(...args);
const isEven = (n) => n % 2 === 0;
const isOdd = negate(isEven);
// isOdd(3) // true
```
**PHP**
```php
function negate(callable $pred): callable {
    return fn(...$args) => !$pred(...$args);
}
$isEven = fn($n) => $n % 2 === 0;
$isOdd = negate($isEven);
// $isOdd(3) // true
```
**Python**
```python
def negate(pred):
    return lambda *args: not pred(*args)

is_even = lambda n: n % 2 == 0
is_odd = negate(is_even)
# is_odd(3)  # True
```

<a id="m716"></a>
### 716. tap (oraliq nazorat)
Qiymatni o'zgartirmasdan unga funksiyani (masalan, log) qo'llaydi va qiymatni qaytaradi; zanjirlarda foydali.

**JS**
```js
const tap = (fn) => (x) => { fn(x); return x; };
// [1, 2, 3].map(x => x * 2).map(tap(console.log)) // log qiladi, [2,4,6] qaytaradi
```
**PHP**
```php
function tap(callable $fn): callable {
    return function ($x) use ($fn) { $fn($x); return $x; };
}
// $log = tap(fn($x) => fwrite(STDERR, $x . "\n")); $log(5) // 5
```
**Python**
```python
def tap(fn):
    def wrapper(x):
        fn(x)
        return x
    return wrapper
# tap(print)(5)  # 5 (va ekranga 5 chiqadi)
```

<a id="m717"></a>
### 717. identity / constant
identity argumentni o'zini qaytaradi; constant esa har doim bitta o'zgarmas qiymatni qaytaruvchi funksiya yasaydi.

**JS**
```js
const identity = (x) => x;
const constant = (x) => () => x;
// identity(5) // 5 ; constant(7)() // 7
```
**PHP**
```php
function identity($x) { return $x; }
function constant_fn($x): callable { return fn() => $x; }
// identity(5) // 5 ; constant_fn(7)() // 7
```
**Python**
```python
def identity(x):
    return x

def constant(x):
    return lambda: x
# identity(5)  # 5 ; constant(7)()  # 7
```

<a id="m718"></a>
### 718. take / drop (boshidan olish / tashlash)
take birinchi n ta elementni oladi; drop birinchi n tasini tashlab, qolganini qaytaradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const take = (n, arr) => arr.slice(0, n);
const drop = (n, arr) => arr.slice(n);
// take(2, [1, 2, 3, 4]) // [1, 2] ; drop(2, [1, 2, 3, 4]) // [3, 4]
```
**PHP**
```php
function take(int $n, array $arr): array {
    return array_slice($arr, 0, $n);
}
function drop(int $n, array $arr): array {
    return array_slice($arr, $n);
}
// take(2, [1, 2, 3, 4]) // [1, 2] ; drop(2, [1, 2, 3, 4]) // [3, 4]
```
**Python**
```python
def take(n, arr):
    return arr[:n]

def drop(n, arr):
    return arr[n:]
# take(2, [1, 2, 3, 4])  # [1, 2] ; drop(2, [1, 2, 3, 4])  # [3, 4]
```

<a id="m719"></a>
### 719. range (sonlar ketma-ketligi)
start dan stop gacha (stop kirmaydi) step qadam bilan sonlar ro'yxatini yasaydi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const range = (start, stop, step = 1) => {
  const out = [];
  for (let i = start; step > 0 ? i < stop : i > stop; i += step)
    out.push(i);
  return out;
};
// range(0, 10, 2) // [0, 2, 4, 6, 8]
```
**PHP**
```php
function myrange(int $start, int $stop, int $step = 1): array {
    $out = [];
    for ($i = $start; $step > 0 ? $i < $stop : $i > $stop; $i += $step)
        $out[] = $i;
    return $out;
}
// myrange(0, 10, 2) // [0, 2, 4, 6, 8]
```
**Python**
```python
def my_range(start, stop, step=1):
    out = []
    i = start
    while (i < stop) if step > 0 else (i > stop):
        out.append(i)
        i += step
    return out
# my_range(0, 10, 2)  # [0, 2, 4, 6, 8]
```

<a id="m720"></a>
### 720. repeat (qiymatni takrorlash)
Berilgan qiymatdan n ta nusxadan iborat ro'yxat yasaydi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const repeat = (value, n) => Array.from({ length: n }, () => value);
// repeat("x", 3) // ["x", "x", "x"]
```
**PHP**
```php
function repeat($value, int $n): array {
    return array_fill(0, $n, $value);
}
// repeat("x", 3) // ["x", "x", "x"]
```
**Python**
```python
def repeat(value, n):
    return [value for _ in range(n)]
# repeat("x", 3)  # ["x", "x", "x"]
```

<a id="m721"></a>
### 721. uniqBy (kalit bo'yicha noyoblash)
Har bir elementdan kalit hisoblab, shu kalit birinchi marta uchragan elementlarni saqlaydi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const uniqBy = (keyFn, arr) => {
  const seen = new Set();
  const out = [];
  for (const v of arr) {
    const k = keyFn(v);
    if (!seen.has(k)) { seen.add(k); out.push(v); }
  }
  return out;
};
// uniqBy(x => x % 3, [1, 2, 3, 4, 5]) // [1, 2, 3]
```
**PHP**
```php
function uniqBy(callable $keyFn, array $arr): array {
    $seen = [];
    $out = [];
    foreach ($arr as $v) {
        $k = $keyFn($v);
        if (!isset($seen[$k])) { $seen[$k] = true; $out[] = $v; }
    }
    return $out;
}
// uniqBy(fn($x) => $x % 3, [1, 2, 3, 4, 5]) // [1, 2, 3]
```
**Python**
```python
def uniq_by(key_fn, arr):
    seen = set()
    out = []
    for v in arr:
        k = key_fn(v)
        if k not in seen:
            seen.add(k)
            out.append(v)
    return out
# uniq_by(lambda x: x % 3, [1, 2, 3, 4, 5])  # [1, 2, 3]
```

<a id="m722"></a>
### 722. sortBy (kalit bo'yicha saralash)
Har bir elementdan hisoblangan kalit (yoki kalitlar) bo'yicha barqaror saralaydi.
`⏱ O(n log n) · 💾 O(n)`

**JS**
```js
const sortBy = (keyFn, arr) =>
  [...arr].sort((a, b) => {
    const ka = keyFn(a), kb = keyFn(b);
    return ka < kb ? -1 : ka > kb ? 1 : 0;
  });
// sortBy(s => s.length, ["bbb", "a", "cc"]) // ["a", "cc", "bbb"]
```
**PHP**
```php
function sortBy(callable $keyFn, array $arr): array {
    usort($arr, fn($a, $b) => $keyFn($a) <=> $keyFn($b));
    return $arr;
}
// sortBy(fn($s) => strlen($s), ["bbb", "a", "cc"]) // ["a", "cc", "bbb"]
```
**Python**
```python
def sort_by(key_fn, arr):
    return sorted(arr, key=key_fn)
# sort_by(len, ["bbb", "a", "cc"])  # ["a", "cc", "bbb"]
```

<a id="m723"></a>
### 723. maxBy / minBy (kalit bo'yicha eng katta/kichik)
Kalit funksiyasi bo'yicha eng katta yoki eng kichik elementni topadi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const maxBy = (keyFn, arr) =>
  arr.reduce((best, v) => (keyFn(v) > keyFn(best) ? v : best));
const minBy = (keyFn, arr) =>
  arr.reduce((best, v) => (keyFn(v) < keyFn(best) ? v : best));
// maxBy(s => s.length, ["a", "ccc", "bb"]) // "ccc"
```
**PHP**
```php
function maxBy(callable $keyFn, array $arr) {
    return array_reduce(
        $arr,
        fn($best, $v) => ($best === null || $keyFn($v) > $keyFn($best)) ? $v : $best,
        null
    );
}
function minBy(callable $keyFn, array $arr) {
    return array_reduce(
        $arr,
        fn($best, $v) => ($best === null || $keyFn($v) < $keyFn($best)) ? $v : $best,
        null
    );
}
// maxBy(fn($s) => strlen($s), ["a", "ccc", "bb"]) // "ccc"
```
**Python**
```python
def max_by(key_fn, arr):
    return max(arr, key=key_fn)

def min_by(key_fn, arr):
    return min(arr, key=key_fn)
# max_by(len, ["a", "ccc", "bb"])  # "ccc"
```

<a id="m724"></a>
### 724. fold / scan (yig'ish va oraliq natijalar)
fold reduce kabi bitta natija beradi; scan esa har bir qadamdagi oraliq yig'indilar ro'yxatini qaytaradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const scan = (fn, init, arr) => {
  const out = [init];
  let acc = init;
  for (const v of arr) { acc = fn(acc, v); out.push(acc); }
  return out;
};
// scan((a, b) => a + b, 0, [1, 2, 3, 4]) // [0, 1, 3, 6, 10]
```
**PHP**
```php
function scan(callable $fn, $init, array $arr): array {
    $out = [$init];
    $acc = $init;
    foreach ($arr as $v) { $acc = $fn($acc, $v); $out[] = $acc; }
    return $out;
}
// scan(fn($a, $b) => $a + $b, 0, [1, 2, 3, 4]) // [0, 1, 3, 6, 10]
```
**Python**
```python
def scan(fn, init, arr):
    out = [init]
    acc = init
    for v in arr:
        acc = fn(acc, v)
        out.append(acc)
    return out
# scan(lambda a, b: a + b, 0, [1, 2, 3, 4])  # [0, 1, 3, 6, 10]
```

<a id="m725"></a>
### 725. lazy sequence (generator orqali dangasa ketma-ketlik)
Generator yordamida cheksiz yoki katta ketma-ketlikni xotirada to'liq saqlamasdan, talab bo'yicha element-element beradi.

**JS**
```js
function* naturals() {
  let n = 1;
  while (true) yield n++;
}
function* take(n, gen) {
  let i = 0;
  for (const v of gen) {
    if (i++ >= n) return;
    yield v;
  }
}
// [...take(5, naturals())] // [1, 2, 3, 4, 5]
```
**Python**
```python
def naturals():
    n = 1
    while True:
        yield n
        n += 1

def take(n, gen):
    out = []
    for v in gen:
        if len(out) >= n:
            break
        out.append(v)
    return out
# take(5, naturals())  # [1, 2, 3, 4, 5]
```

<a id="m726"></a>
### 726. frequency / countBy (chastotani sanash)
Har bir element (yoki kalit) necha marta uchraganini sanab, kalit-son lug'atini qaytaradi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const countBy = (keyFn, arr) => {
  const out = {};
  for (const v of arr) {
    const k = keyFn(v);
    out[k] = (out[k] ?? 0) + 1;
  }
  return out;
};
// countBy(x => x % 2, [1, 2, 3, 4, 5]) // {1: 3, 0: 2}
```
**PHP**
```php
function countBy(callable $keyFn, array $arr): array {
    $out = [];
    foreach ($arr as $v) {
        $k = $keyFn($v);
        $out[$k] = ($out[$k] ?? 0) + 1;
    }
    return $out;
}
// countBy(fn($x) => $x % 2, [1, 2, 3, 4, 5]) // [1 => 3, 0 => 2]
```
**Python**
```python
def count_by(key_fn, arr):
    out = {}
    for v in arr:
        k = key_fn(v)
        out[k] = out.get(k, 0) + 1
    return out
# count_by(lambda x: x % 2, [1, 2, 3, 4, 5])  # {1: 3, 0: 2}
```
