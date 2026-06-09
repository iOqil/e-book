<a id="b27"></a>
# 27-bo'lim: Matematika va sonlar nazariyasi

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Bu bo'lim raqobat dasturlashda eng ko'p uchraydigan matematik vositalarni qamrab oladi:
> tez daraja va modul arifmetikasi, Evklid algoritmining kengaytmasi, tub sonlar elaklari,
> Euler funksiyasi, kombinatorika (nCr, Katalan), Fibonacci ni matritsa va fast doubling bilan
> hisoblash, Xitoy qoldiqlar teoremasi hamda ko'plab klassik raqamli masalalar. Asosiy GCD/LCM,
> oddiy tublik tekshiruvi va faktorial avvalgi bo'limlarda berilgani uchun bu yerda ularning
> ILG'OR variantlari beriladi. Modul sifatida ko'pincha 1e9+7 (tub son) ishlatiladi.

<a id="m457"></a>
### 457. Tez daraja — modular exponentiation
`(base^exp) mod m` ni log(exp) qadamda hisoblash (binary exponentiation).
`⏱ O(log exp) · 💾 O(1)`

**JS**
```js
const powMod = (base, exp, mod) => {
  base %= mod;
  let result = 1n;
  let b = BigInt(base), e = BigInt(exp), m = BigInt(mod);
  while (e > 0n) {
    if (e & 1n) result = (result * b) % m;
    b = (b * b) % m;
    e >>= 1n;
  }
  return Number(result);
};
```
**PHP**
```php
function powMod(int $base, int $exp, int $mod): int {
    $result = 1; $base %= $mod;
    while ($exp > 0) {
        if ($exp & 1) $result = (int)(($result * $base) % $mod);
        $base = (int)(($base * $base) % $mod);
        $exp >>= 1;
    }
    return $result;
}
```
**Python**
```python
def pow_mod(base, exp, mod):
    return pow(base, exp, mod)  # o'rnatilgan; qo'lda: pastdagi varianti
def pow_mod_manual(base, exp, mod):
    result, base = 1, base % mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result
```

<a id="m458"></a>
### 458. Modular invers — Fermat kichik teoremasi
Tub modul p uchun a^(-1) ≡ a^(p-2) (mod p). a va p o'zaro tub bo'lishi shart.
`⏱ O(log p) · 💾 O(1)`

**JS**
```js
const modInverseFermat = (a, p) => {
  // p tub bo'lishi shart; a^(p-2) mod p
  let result = 1n, b = BigInt(((a % p) + p) % p), e = BigInt(p - 2), m = BigInt(p);
  while (e > 0n) {
    if (e & 1n) result = (result * b) % m;
    b = (b * b) % m;
    e >>= 1n;
  }
  return Number(result);
};
```
**PHP**
```php
function modInverseFermat(int $a, int $p): int {
    // p tub; a^(p-2) mod p
    $a = (($a % $p) + $p) % $p;
    $result = 1; $exp = $p - 2;
    while ($exp > 0) {
        if ($exp & 1) $result = (int)(($result * $a) % $p);
        $a = (int)(($a * $a) % $p);
        $exp >>= 1;
    }
    return $result;
}
```
**Python**
```python
def mod_inverse_fermat(a, p):
    return pow(a % p, p - 2, p)
```

<a id="m459"></a>
### 459. Kengaytirilgan Evklid (extended GCD)
gcd(a, b) bilan birga ax + by = gcd(a, b) tenglamaning (x, y) yechimini topadi.
`⏱ O(log min(a,b)) · 💾 O(log min(a,b))`

**JS**
```js
const extGcd = (a, b) => {
  if (b === 0) return [a, 1, 0];
  const [g, x1, y1] = extGcd(b, a % b);
  return [g, y1, x1 - Math.floor(a / b) * y1];
};
```
**PHP**
```php
function extGcd(int $a, int $b): array {
    if ($b === 0) return [$a, 1, 0];
    [$g, $x1, $y1] = extGcd($b, $a % $b);
    return [$g, $y1, $x1 - intdiv($a, $b) * $y1];
}
```
**Python**
```python
def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1
```

<a id="m460"></a>
### 460. Modular invers — kengaytirilgan Evklid orqali
Modul tub bo'lmasa ham ishlaydi; a va m o'zaro tub bo'lishi yetarli.
`⏱ O(log m) · 💾 O(log m)`

**JS**
```js
const modInverse = (a, m) => {
  const ext = (a, b) => b === 0 ? [a, 1, 0]
    : (([g, x1, y1]) => [g, y1, x1 - Math.floor(a / b) * y1])(ext(b, a % b));
  const [g, x] = ext(((a % m) + m) % m, m);
  if (g !== 1) return null; // invers mavjud emas
  return ((x % m) + m) % m;
};
```
**PHP**
```php
function modInverse(int $a, int $m): ?int {
    $ext = function ($a, $b) use (&$ext) {
        if ($b === 0) return [$a, 1, 0];
        [$g, $x1, $y1] = $ext($b, $a % $b);
        return [$g, $y1, $x1 - intdiv($a, $b) * $y1];
    };
    [$g, $x] = $ext((($a % $m) + $m) % $m, $m);
    if ($g !== 1) return null;
    return (($x % $m) + $m) % $m;
}
```
**Python**
```python
def mod_inverse(a, m):
    def ext(a, b):
        if b == 0:
            return a, 1, 0
        g, x1, y1 = ext(b, a % b)
        return g, y1, x1 - (a // b) * y1
    g, x, _ = ext(a % m, m)
    if g != 1:
        return None
    return x % m
```

<a id="m461"></a>
### 461. Eratosfen elagi (sieve of Eratosthenes)
n gacha barcha tub sonlarni topadi.
`⏱ O(n log log n) · 💾 O(n)`

**JS**
```js
const sieve = (n) => {
  const isPrime = new Array(n + 1).fill(true);
  isPrime[0] = isPrime[1] = false;
  for (let i = 2; i * i <= n; i++)
    if (isPrime[i])
      for (let j = i * i; j <= n; j += i) isPrime[j] = false;
  const primes = [];
  for (let i = 2; i <= n; i++) if (isPrime[i]) primes.push(i);
  return primes;
};
```
**PHP**
```php
function sieve(int $n): array {
    $isPrime = array_fill(0, $n + 1, true);
    $isPrime[0] = $isPrime[1] = false;
    for ($i = 2; $i * $i <= $n; $i++)
        if ($isPrime[$i])
            for ($j = $i * $i; $j <= $n; $j += $i) $isPrime[$j] = false;
    $primes = [];
    for ($i = 2; $i <= $n; $i++) if ($isPrime[$i]) $primes[] = $i;
    return $primes;
}
```
**Python**
```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]
```

<a id="m462"></a>
### 462. Segmentli elak (segmented sieve)
[lo, hi] oralig'idagi tublarni kichik xotira bilan topadi (hi katta bo'lsa ham).
`⏱ O((hi-lo) log log hi + √hi) · 💾 O(√hi + (hi-lo))`

**JS**
```js
const segmentedSieve = (lo, hi) => {
  const limit = Math.floor(Math.sqrt(hi)) + 1;
  const base = new Array(limit + 1).fill(true);
  const basePrimes = [];
  for (let i = 2; i <= limit; i++) {
    if (base[i]) {
      basePrimes.push(i);
      for (let j = i * i; j <= limit; j += i) base[j] = false;
    }
  }
  const isPrime = new Array(hi - lo + 1).fill(true);
  if (lo === 0) { isPrime[0] = false; if (hi >= 1) isPrime[1 - lo] = false; }
  else if (lo === 1) isPrime[0] = false;
  for (const p of basePrimes) {
    let start = Math.max(p * p, Math.ceil(lo / p) * p);
    for (let j = start; j <= hi; j += p) isPrime[j - lo] = false;
  }
  const res = [];
  for (let i = 0; i < isPrime.length; i++) if (isPrime[i]) res.push(i + lo);
  return res;
};
```
**Python**
```python
def segmented_sieve(lo, hi):
    limit = int(hi ** 0.5) + 1
    base = [True] * (limit + 1)
    base_primes = []
    for i in range(2, limit + 1):
        if base[i]:
            base_primes.append(i)
            for j in range(i * i, limit + 1, i):
                base[j] = False
    is_prime = [True] * (hi - lo + 1)
    for x in (0, 1):
        if lo <= x <= hi:
            is_prime[x - lo] = False
    for p in base_primes:
        start = max(p * p, (lo + p - 1) // p * p)
        for j in range(start, hi + 1, p):
            is_prime[j - lo] = False
    return [i + lo for i in range(hi - lo + 1) if is_prime[i]]
```

<a id="m463"></a>
### 463. Eng kichik tub bo'luvchi elagi (smallest prime factor)
Har bir son uchun eng kichik tub bo'luvchini oldindan hisoblaydi; faktorizatsiyani O(log n) qiladi.
`⏱ O(n log log n) · 💾 O(n)`

**JS**
```js
const spfSieve = (n) => {
  const spf = new Array(n + 1).fill(0);
  for (let i = 2; i <= n; i++) {
    if (spf[i] === 0)
      for (let j = i; j <= n; j += i)
        if (spf[j] === 0) spf[j] = i;
  }
  return spf;
};
const factorize = (x, spf) => {
  const f = {};
  while (x > 1) { const p = spf[x]; f[p] = (f[p] || 0) + 1; x = Math.floor(x / p); }
  return f;
};
```
**Python**
```python
def spf_sieve(n):
    spf = [0] * (n + 1)
    for i in range(2, n + 1):
        if spf[i] == 0:
            for j in range(i, n + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    return spf

def factorize(x, spf):
    f = {}
    while x > 1:
        p = spf[x]
        f[p] = f.get(p, 0) + 1
        x //= p
    return f
```

<a id="m464"></a>
### 464. Euler funksiyasi φ(n)
n dan kichik va u bilan o'zaro tub bo'lgan sonlar miqdori. Tub bo'luvchilar orqali hisoblanadi.
`⏱ O(√n) · 💾 O(1)`

**JS**
```js
const eulerPhi = (n) => {
  let result = n;
  for (let p = 2; p * p <= n; p++) {
    if (n % p === 0) {
      while (n % p === 0) n = Math.floor(n / p);
      result -= Math.floor(result / p);
    }
  }
  if (n > 1) result -= Math.floor(result / n);
  return result;
};
```
**PHP**
```php
function eulerPhi(int $n): int {
    $result = $n;
    for ($p = 2; $p * $p <= $n; $p++) {
        if ($n % $p === 0) {
            while ($n % $p === 0) $n = intdiv($n, $p);
            $result -= intdiv($result, $p);
        }
    }
    if ($n > 1) $result -= intdiv($result, $n);
    return $result;
}
```
**Python**
```python
def euler_phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result
```

<a id="m465"></a>
### 465. Euler funksiyasi — elak bilan (1..n hammasi)
1 dan n gacha barcha φ qiymatlarini elak usulida hisoblaydi.
`⏱ O(n log log n) · 💾 O(n)`

**JS**
```js
const phiSieve = (n) => {
  const phi = Array.from({ length: n + 1 }, (_, i) => i);
  for (let i = 2; i <= n; i++) {
    if (phi[i] === i) // i tub
      for (let j = i; j <= n; j += i)
        phi[j] -= Math.floor(phi[j] / i);
  }
  return phi;
};
```
**Python**
```python
def phi_sieve(n):
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:  # i tub
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi
```

<a id="m466"></a>
### 466. nCr — Paskal uchburchagi
Binomial koeffitsientni dinamik dastur orqali (modulsiz) hisoblaydi.
`⏱ O(n·r) · 💾 O(r)`

**JS**
```js
const nCr = (n, r) => {
  if (r < 0 || r > n) return 0;
  r = Math.min(r, n - r);
  const dp = new Array(r + 1).fill(0);
  dp[0] = 1;
  for (let i = 1; i <= n; i++)
    for (let j = Math.min(i, r); j > 0; j--)
      dp[j] += dp[j - 1];
  return dp[r];
};
```
**Python**
```python
def n_cr(n, r):
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    dp = [0] * (r + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, r), 0, -1):
            dp[j] += dp[j - 1]
    return dp[r]
```

<a id="m467"></a>
### 467. nCr mod p — faktorial va invers
Tub p uchun nCr ni faktorial va modular invers orqali tez hisoblaydi.
`⏱ O(n) tayyorlash, O(1) so'rov · 💾 O(n)`

**Python**
```python
def n_cr_mod_p(n, r, p):
    if r < 0 or r > n:
        return 0
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % p
    inv = pow(fact[r] * fact[n - r] % p, p - 2, p)
    return fact[n] * inv % p
```
**JS**
```js
const nCrModP = (n, r, p) => {
  if (r < 0 || r > n) return 0;
  const P = BigInt(p);
  const fact = [1n];
  for (let i = 1; i <= n; i++) fact[i] = (fact[i - 1] * BigInt(i)) % P;
  const powMod = (b, e) => {
    let res = 1n; b %= P;
    while (e > 0n) { if (e & 1n) res = (res * b) % P; b = (b * b) % P; e >>= 1n; }
    return res;
  };
  const inv = powMod((fact[r] * fact[n - r]) % P, P - 2n);
  return Number((fact[n] * inv) % P);
};
```

<a id="m468"></a>
### 468. Katalan sonlari
n-chi Katalan soni Cn = C(2n, n)/(n+1). To'g'ri qavslar, BST tuzilmalari soni.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const catalan = (n) => {
  let c = 1n;
  for (let i = 0; i < n; i++)
    c = (c * BigInt(2 * (2 * i + 1))) / BigInt(i + 2);
  return c; // BigInt (katta o'sadi)
};
```
**Python**
```python
def catalan(n):
    c = 1
    for i in range(n):
        c = c * 2 * (2 * i + 1) // (i + 2)
    return c
```

<a id="m469"></a>
### 469. Fibonacci — matritsa darajasi orqali
[[1,1],[1,0]]^n matritsasi orqali F(n) ni O(log n) da hisoblaydi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const fibMatrix = (n) => {
  const mul = (A, B) => [
    [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
    [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
  ];
  let result = [[1n, 0n], [0n, 1n]];        // birlik matritsa
  let m = [[1n, 1n], [1n, 0n]];
  let e = n;
  while (e > 0) {
    if (e & 1) result = mul(result, m);
    m = mul(m, m);
    e = Math.floor(e / 2);
  }
  return result[0][1]; // F(n)
};
```
**Python**
```python
def fib_matrix(n):
    def mul(a, b):
        return [
            [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
            [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]],
        ]
    result = [[1, 0], [0, 1]]
    m = [[1, 1], [1, 0]]
    while n > 0:
        if n & 1:
            result = mul(result, m)
        m = mul(m, m)
        n >>= 1
    return result[0][1]
```

<a id="m470"></a>
### 470. Fibonacci — fast doubling
F(2k) va F(2k+1) ni rekursiv ikkilantirib O(log n) da hisoblaydi (matritsadan tez).
`⏱ O(log n) · 💾 O(log n)`

**JS**
```js
const fibFastDoubling = (n) => {
  const rec = (n) => {
    if (n === 0n) return [0n, 1n]; // [F(n), F(n+1)]
    const [a, b] = rec(n >> 1n);
    const c = a * (2n * b - a);
    const d = a * a + b * b;
    return (n & 1n) ? [d, c + d] : [c, d];
  };
  return rec(BigInt(n))[0];
};
```
**Python**
```python
def fib_fast_doubling(n):
    def rec(n):
        if n == 0:
            return 0, 1  # F(n), F(n+1)
        a, b = rec(n >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if n & 1:
            return d, c + d
        return c, d
    return rec(n)[0]
```

<a id="m471"></a>
### 471. Xitoy qoldiqlar teoremasi (CRT)
x ≡ r[i] (mod m[i]) tizimini o'zaro tub modullar uchun yechadi.
`⏱ O(k log M) · 💾 O(1)`

**Python**
```python
def crt(remainders, moduli):
    def ext(a, b):
        if b == 0:
            return a, 1, 0
        g, x, y = ext(b, a % b)
        return g, y, x - (a // b) * y
    prod = 1
    for m in moduli:
        prod *= m
    result = 0
    for r, m in zip(remainders, moduli):
        pp = prod // m
        _, inv, _ = ext(pp % m, m)
        result = (result + r * pp * inv) % prod
    return result % prod
```
**JS**
```js
const crt = (remainders, moduli) => {
  const ext = (a, b) => b === 0n ? [a, 1n, 0n]
    : (([g, x, y]) => [g, y, x - (a / b) * y])(ext(b, a % b));
  let prod = 1n;
  for (const m of moduli) prod *= BigInt(m);
  let result = 0n;
  for (let i = 0; i < moduli.length; i++) {
    const m = BigInt(moduli[i]), r = BigInt(remainders[i]);
    const pp = prod / m;
    let [, inv] = ext(((pp % m) + m) % m, m);
    result = (result + r * pp * inv) % prod;
  }
  return Number(((result % prod) + prod) % prod);
};
```

<a id="m472"></a>
### 472. Butun kvadrat ildiz (Nyuton usuli)
⌊√x⌋ ni butun sonlarda, Nyuton iteratsiyasi bilan topadi.
`⏱ O(log x) · 💾 O(1)`

**JS**
```js
const isqrt = (x) => {
  if (x < 2) return x;
  let g = Math.floor(Math.sqrt(x)); // boshlang'ich taxmin
  while (g * g > x) g--;
  while ((g + 1) * (g + 1) <= x) g++;
  return g;
};
```
**PHP**
```php
function isqrt(int $x): int {
    if ($x < 2) return $x;
    $g = (int)sqrt($x);
    while ($g * $g > $x) $g--;
    while (($g + 1) * ($g + 1) <= $x) $g++;
    return $g;
}
```
**Python**
```python
import math
def isqrt(x):
    return math.isqrt(x)
```

<a id="m473"></a>
### 473. n-darajali butun ildiz
⌊x^(1/k)⌋ ni butun sonlarda binary search bilan topadi.
`⏱ O(log x · k) · 💾 O(1)`

**Python**
```python
def integer_nth_root(x, k):
    if x < 0:
        raise ValueError("manfiy son")
    lo, hi = 0, max(1, x)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo
```
**JS**
```js
const integerNthRoot = (x, k) => {
  let lo = 0n, hi = BigInt(Math.max(1, x)), X = BigInt(x), K = BigInt(k);
  while (lo < hi) {
    const mid = (lo + hi + 1n) / 2n;
    if (mid ** K <= X) lo = mid; else hi = mid - 1n;
  }
  return Number(lo);
};
```

<a id="m474"></a>
### 474. Ixtiyoriy asosga o'tkazish (base conversion)
10 lik sonni 2..16 asosdagi satrga aylantiradi.
`⏱ O(log_base n) · 💾 O(log_base n)`

**JS**
```js
const toBase = (n, base) => {
  if (n === 0) return "0";
  const digits = "0123456789ABCDEF";
  let neg = n < 0; n = Math.abs(n);
  let s = "";
  while (n > 0) { s = digits[n % base] + s; n = Math.floor(n / base); }
  return neg ? "-" + s : s;
};
```
**PHP**
```php
function toBase(int $n, int $base): string {
    if ($n === 0) return "0";
    $digits = "0123456789ABCDEF";
    $neg = $n < 0; $n = abs($n);
    $s = "";
    while ($n > 0) { $s = $digits[$n % $base] . $s; $n = intdiv($n, $base); }
    return $neg ? "-" . $s : $s;
}
```
**Python**
```python
def to_base(n, base):
    if n == 0:
        return "0"
    digits = "0123456789ABCDEF"
    neg, n = n < 0, abs(n)
    s = ""
    while n > 0:
        s = digits[n % base] + s
        n //= base
    return "-" + s if neg else s
```

<a id="m475"></a>
### 475. Rim raqamidan butunga (roman to integer)
Rim raqami satrini butun songa aylantiradi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const romanToInt = (s) => {
  const m = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };
  let total = 0;
  for (let i = 0; i < s.length; i++) {
    if (i + 1 < s.length && m[s[i]] < m[s[i + 1]]) total -= m[s[i]];
    else total += m[s[i]];
  }
  return total;
};
```
**PHP**
```php
function romanToInt(string $s): int {
    $m = ['I'=>1,'V'=>5,'X'=>10,'L'=>50,'C'=>100,'D'=>500,'M'=>1000];
    $total = 0; $n = strlen($s);
    for ($i = 0; $i < $n; $i++) {
        if ($i + 1 < $n && $m[$s[$i]] < $m[$s[$i + 1]]) $total -= $m[$s[$i]];
        else $total += $m[$s[$i]];
    }
    return $total;
}
```
**Python**
```python
def roman_to_int(s):
    m = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and m[ch] < m[s[i + 1]]:
            total -= m[ch]
        else:
            total += m[ch]
    return total
```

<a id="m476"></a>
### 476. Excel ustun raqami ↔ harf
Sonni Excel ustun harfiga (1→A, 27→AA) va aksincha aylantiradi (1 dan boshlangan asos-26).
`⏱ O(log n) · 💾 O(log n)`

**JS**
```js
const toColumnTitle = (n) => {
  let s = "";
  while (n > 0) { n--; s = String.fromCharCode(65 + (n % 26)) + s; n = Math.floor(n / 26); }
  return s;
};
const titleToNumber = (s) => {
  let n = 0;
  for (const ch of s) n = n * 26 + (ch.charCodeAt(0) - 64);
  return n;
};
```
**Python**
```python
def to_column_title(n):
    s = ""
    while n > 0:
        n -= 1
        s = chr(65 + n % 26) + s
        n //= 26
    return s

def title_to_number(s):
    n = 0
    for ch in s:
        n = n * 26 + (ord(ch) - 64)
    return n
```

<a id="m477"></a>
### 477. Baxtli son (happy number)
Raqamlari kvadratlari yig'indisini takrorlab 1 ga kelsa baxtli; sikl bo'lsa yo'q.
`⏱ O(log n) iteratsiya · 💾 O(log n)`

**JS**
```js
const isHappy = (n) => {
  const seen = new Set();
  const next = (x) => {
    let s = 0;
    while (x > 0) { const d = x % 10; s += d * d; x = Math.floor(x / 10); }
    return s;
  };
  while (n !== 1 && !seen.has(n)) { seen.add(n); n = next(n); }
  return n === 1;
};
```
**PHP**
```php
function isHappy(int $n): bool {
    $seen = [];
    $next = function ($x) {
        $s = 0;
        while ($x > 0) { $d = $x % 10; $s += $d * $d; $x = intdiv($x, 10); }
        return $s;
    };
    while ($n !== 1 && !isset($seen[$n])) { $seen[$n] = true; $n = $next($n); }
    return $n === 1;
}
```
**Python**
```python
def is_happy(n):
    seen = set()
    def nxt(x):
        return sum(int(d) ** 2 for d in str(x))
    while n != 1 and n not in seen:
        seen.add(n)
        n = nxt(n)
    return n == 1
```

<a id="m478"></a>
### 478. Uch yoki to'rt darajasimi (power of three / four)
Sonning aniq 3 yoki 4 darajasi ekanini tekshiradi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const isPowerOfThree = (n) => {
  if (n < 1) return false;
  while (n % 3 === 0) n = Math.floor(n / 3);
  return n === 1;
};
const isPowerOfFour = (n) => {
  if (n < 1) return false;
  while (n % 4 === 0) n = Math.floor(n / 4);
  return n === 1;
};
```
**Python**
```python
def is_power_of_three(n):
    if n < 1:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1

def is_power_of_four(n):
    if n < 1:
        return False
    while n % 4 == 0:
        n //= 4
    return n == 1
```

<a id="m479"></a>
### 479. Faktorialdagi nollar soni (trailing zeroes)
n! oxiridagi nollar soni — bu n ichidagi 5 ko'paytuvchilari soni.
`⏱ O(log_5 n) · 💾 O(1)`

**JS**
```js
const trailingZeroes = (n) => {
  let count = 0;
  for (let p = 5; p <= n; p *= 5) count += Math.floor(n / p);
  return count;
};
```
**PHP**
```php
function trailingZeroes(int $n): int {
    $count = 0;
    for ($p = 5; $p <= $n; $p *= 5) $count += intdiv($n, $p);
    return $count;
}
```
**Python**
```python
def trailing_zeroes(n):
    count = 0
    p = 5
    while p <= n:
        count += n // p
        p *= 5
    return count
```

<a id="m480"></a>
### 480. Faktorialdagi raqamlar soni
n! da nechta o'nlik raqam borligini Stirling/logarifm formulasi bilan topadi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const factorialDigits = (n) => {
  if (n <= 1) return 1;
  let sum = 0;
  for (let i = 2; i <= n; i++) sum += Math.log10(i);
  return Math.floor(sum) + 1;
};
```
**Python**
```python
import math
def factorial_digits(n):
    if n <= 1:
        return 1
    s = sum(math.log10(i) for i in range(2, n + 1))
    return int(s) + 1
```

<a id="m481"></a>
### 481. Bo'luvchilar yig'indisi (sum of divisors)
n ning barcha musbat bo'luvchilari yig'indisi σ(n).
`⏱ O(√n) · 💾 O(1)`

**JS**
```js
const sumDivisors = (n) => {
  let sum = 0;
  for (let i = 1; i * i <= n; i++) {
    if (n % i === 0) {
      sum += i;
      if (i !== Math.floor(n / i)) sum += Math.floor(n / i);
    }
  }
  return sum;
};
```
**PHP**
```php
function sumDivisors(int $n): int {
    $sum = 0;
    for ($i = 1; $i * $i <= $n; $i++) {
        if ($n % $i === 0) {
            $sum += $i;
            if ($i !== intdiv($n, $i)) $sum += intdiv($n, $i);
        }
    }
    return $sum;
}
```
**Python**
```python
def sum_divisors(n):
    total = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        i += 1
    return total
```

<a id="m482"></a>
### 482. Bo'luvchilar soni (count of divisors)
n ning musbat bo'luvchilari miqdori d(n).
`⏱ O(√n) · 💾 O(1)`

**JS**
```js
const countDivisors = (n) => {
  let count = 0;
  for (let i = 1; i * i <= n; i++) {
    if (n % i === 0) {
      count += (i === Math.floor(n / i)) ? 1 : 2;
    }
  }
  return count;
};
```
**Python**
```python
def count_divisors(n):
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1 if i == n // i else 2
        i += 1
    return count
```

<a id="m483"></a>
### 483. Kaprekar soni (Kaprekar number)
Kvadrati ikki qismga bo'linib qo'shilganda asl sonni beradigan son (masalan 45²=2025, 20+25=45).
`⏱ O(log n) · 💾 O(log n)`

**JS**
```js
const isKaprekar = (n) => {
  if (n === 1) return true;
  const sq = (n * n).toString();
  const len = sq.length;
  for (let i = 1; i < len; i++) {
    const left = parseInt(sq.slice(0, i) || "0", 10);
    const right = parseInt(sq.slice(i), 10);
    if (right > 0 && left + right === n) return true;
  }
  return false;
};
```
**Python**
```python
def is_kaprekar(n):
    if n == 1:
        return True
    sq = str(n * n)
    for i in range(1, len(sq)):
        left = int(sq[:i] or "0")
        right = int(sq[i:])
        if right > 0 and left + right == n:
            return True
    return False
```

<a id="m484"></a>
### 484. Avtomorf son (automorphic number)
Kvadrati shu son bilan tugaydigan son (masalan 25²=625, 76²=5776).
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const isAutomorphic = (n) => {
  const sq = n * n;
  const s = n.toString();
  return sq.toString().endsWith(s);
};
```
**PHP**
```php
function isAutomorphic(int $n): bool {
    $sq = (string)($n * $n);
    $s = (string)$n;
    return substr($sq, -strlen($s)) === $s;
}
```
**Python**
```python
def is_automorphic(n):
    return str(n * n).endswith(str(n))
```

<a id="m485"></a>
### 485. Harshad (Niven) soni
Raqamlari yig'indisiga butun bo'linadigan son (masalan 18 → 1+8=9, 18%9=0).
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const isHarshad = (n) => {
  let s = 0, x = n;
  while (x > 0) { s += x % 10; x = Math.floor(x / 10); }
  return s > 0 && n % s === 0;
};
```
**Python**
```python
def is_harshad(n):
    s = sum(int(d) for d in str(n))
    return s > 0 and n % s == 0
```

<a id="m486"></a>
### 486. Collatz qadamlari
n dan 1 ga yetguncha (juft→/2, toq→3n+1) qadamlar sonini sanaydi.
`⏱ noma'lum (amalda log) · 💾 O(1)`

**JS**
```js
const collatzSteps = (n) => {
  let steps = 0;
  while (n !== 1) {
    n = (n % 2 === 0) ? n / 2 : 3 * n + 1;
    steps++;
  }
  return steps;
};
```
**PHP**
```php
function collatzSteps(int $n): int {
    $steps = 0;
    while ($n !== 1) {
        $n = ($n % 2 === 0) ? intdiv($n, 2) : 3 * $n + 1;
        $steps++;
    }
    return $steps;
}
```
**Python**
```python
def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps
```

<a id="m487"></a>
### 487. Butun sonni teskari (reverse integer, overflow xavfsiz)
Belgili 32-bitli sonni teskari aylantiradi; chegaradan oshsa 0 qaytaradi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const reverseInt = (x) => {
  const sign = Math.sign(x);
  let r = parseInt(Math.abs(x).toString().split("").reverse().join(""), 10) * sign;
  if (r < -(2 ** 31) || r > 2 ** 31 - 1) return 0;
  return r;
};
```
**Python**
```python
def reverse_int(x):
    sign = -1 if x < 0 else 1
    r = sign * int(str(abs(x))[::-1])
    if r < -2**31 or r > 2**31 - 1:
        return 0
    return r
```

<a id="m488"></a>
### 488. Katta sonlarni qo'shish (string sifatida)
Ixtiyoriy uzunlikdagi ikki musbat butun sonni satr ko'rinishida qo'shadi.
`⏱ O(max(n,m)) · 💾 O(max(n,m))`

**JS**
```js
const addStrings = (a, b) => {
  let i = a.length - 1, j = b.length - 1, carry = 0, res = "";
  while (i >= 0 || j >= 0 || carry) {
    const da = i >= 0 ? +a[i--] : 0;
    const db = j >= 0 ? +b[j--] : 0;
    const sum = da + db + carry;
    res = (sum % 10) + res;
    carry = Math.floor(sum / 10);
  }
  return res;
};
```
**PHP**
```php
function addStrings(string $a, string $b): string {
    $i = strlen($a) - 1; $j = strlen($b) - 1; $carry = 0; $res = "";
    while ($i >= 0 || $j >= 0 || $carry) {
        $da = $i >= 0 ? (int)$a[$i--] : 0;
        $db = $j >= 0 ? (int)$b[$j--] : 0;
        $sum = $da + $db + $carry;
        $res = ($sum % 10) . $res;
        $carry = intdiv($sum, 10);
    }
    return $res;
}
```
**Python**
```python
def add_strings(a, b):
    i, j, carry, res = len(a) - 1, len(b) - 1, 0, []
    while i >= 0 or j >= 0 or carry:
        da = int(a[i]) if i >= 0 else 0
        db = int(b[j]) if j >= 0 else 0
        s = da + db + carry
        res.append(str(s % 10))
        carry = s // 10
        i -= 1
        j -= 1
    return "".join(reversed(res))
```

<a id="m489"></a>
### 489. Katta sonlarni ko'paytirish (string sifatida)
Ikki musbat butun sonni satrda, ustun ko'paytirish usulida ko'paytiradi.
`⏱ O(n·m) · 💾 O(n+m)`

**JS**
```js
const multiplyStrings = (a, b) => {
  if (a === "0" || b === "0") return "0";
  const n = a.length, m = b.length;
  const pos = new Array(n + m).fill(0);
  for (let i = n - 1; i >= 0; i--)
    for (let j = m - 1; j >= 0; j--) {
      const mul = (+a[i]) * (+b[j]);
      const p1 = i + j, p2 = i + j + 1;
      const sum = mul + pos[p2];
      pos[p2] = sum % 10;
      pos[p1] += Math.floor(sum / 10);
    }
  return pos.join("").replace(/^0+/, "") || "0";
};
```
**Python**
```python
def multiply_strings(a, b):
    if a == "0" or b == "0":
        return "0"
    n, m = len(a), len(b)
    pos = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            mul = int(a[i]) * int(b[j])
            p1, p2 = i + j, i + j + 1
            s = mul + pos[p2]
            pos[p2] = s % 10
            pos[p1] += s // 10
    return "".join(map(str, pos)).lstrip("0") or "0"
```

<a id="m490"></a>
### 490. Satrlarning GCD si (greatest common divisor of strings)
Ikki satr uchun shunday eng uzun t topadiki, ikkalasi ham t ning takrori bo'lsin.
`⏱ O(n+m) · 💾 O(n+m)`

**JS**
```js
const gcdOfStrings = (s1, s2) => {
  if (s1 + s2 !== s2 + s1) return "";
  const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
  const g = gcd(s1.length, s2.length);
  return s1.slice(0, g);
};
```
**Python**
```python
def gcd_of_strings(s1, s2):
    if s1 + s2 != s2 + s1:
        return ""
    from math import gcd
    return s1[:gcd(len(s1), len(s2))]
```

<a id="m491"></a>
### 491. Kasrni davriy o'nlik kasrga (fraction to recurring decimal)
Ratsional kasrni o'nlik satrga aylantiradi, takrorlanuvchi qismni qavsga oladi.
`⏱ O(maxraj) · 💾 O(maxraj)`

**Python**
```python
def fraction_to_decimal(num, den):
    if num == 0:
        return "0"
    sign = "-" if (num < 0) ^ (den < 0) else ""
    num, den = abs(num), abs(den)
    res = [sign, str(num // den)]
    rem = num % den
    if rem == 0:
        return "".join(res)
    res.append(".")
    seen = {}
    while rem and rem not in seen:
        seen[rem] = len(res)
        rem *= 10
        res.append(str(rem // den))
        rem %= den
    if rem:
        idx = seen[rem]
        res.insert(idx, "(")
        res.append(")")
    return "".join(res)
```
**JS**
```js
const fractionToDecimal = (num, den) => {
  if (num === 0) return "0";
  let res = "";
  if ((num < 0) ^ (den < 0)) res += "-";
  let n = Math.abs(num), d = Math.abs(den);
  res += Math.floor(n / d);
  let rem = n % d;
  if (rem === 0) return res;
  res += ".";
  const seen = new Map();
  while (rem !== 0 && !seen.has(rem)) {
    seen.set(rem, res.length);
    rem *= 10;
    res += Math.floor(rem / d);
    rem %= d;
  }
  if (rem !== 0) {
    const idx = seen.get(rem);
    res = res.slice(0, idx) + "(" + res.slice(idx) + ")";
  }
  return res;
};
```

<a id="m492"></a>
### 492. Josephus muammosi
n kishi doirada, har k-chisini chiqarib boramiz; tirik qolgan o'rinni topamiz (0 dan).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const josephus = (n, k) => {
  let res = 0; // 1 kishi uchun pozitsiya 0
  for (let i = 2; i <= n; i++) res = (res + k) % i;
  return res;
};
```
**PHP**
```php
function josephus(int $n, int $k): int {
    $res = 0;
    for ($i = 2; $i <= $n; $i++) $res = ($res + $k) % $i;
    return $res;
}
```
**Python**
```python
def josephus(n, k):
    res = 0
    for i in range(2, n + 1):
        res = (res + k) % i
    return res
```

<a id="m493"></a>
### 493. Nim o'yini (Nim game)
Bir uyumli sodda Nim: birinchi o'yinchi 4 ga karrali bo'lmagan toshlarda yutadi.
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const canWinNim = (n) => n % 4 !== 0;
```
**PHP**
```php
function canWinNim(int $n): bool { return $n % 4 !== 0; }
```
**Python**
```python
def can_win_nim(n):
    return n % 4 != 0
```

<a id="m494"></a>
### 494. Lampochkalar (bulb switcher)
n ta lampochka, i-chi yurishda i ga karra holatlar almashtiriladi; yoniqlari soni = ⌊√n⌋.
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const bulbSwitch = (n) => Math.floor(Math.sqrt(n));
```
**Python**
```python
import math
def bulb_switch(n):
    return math.isqrt(n)
```

<a id="m495"></a>
### 495. Suv va idish muammosi (water and jug)
x va y litrli idishlar bilan aniq z litr o'lchash mumkinmi (z ≤ x+y va z gcd(x,y) ga karra).
`⏱ O(log min(x,y)) · 💾 O(1)`

**JS**
```js
const canMeasureWater = (x, y, z) => {
  if (z > x + y) return false;
  if (z === 0) return true;
  const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
  return z % gcd(x, y) === 0;
};
```
**Python**
```python
from math import gcd
def can_measure_water(x, y, z):
    if z > x + y:
        return False
    if z == 0:
        return True
    return z % gcd(x, y) == 0
```

<a id="m496"></a>
### 496. pow(x, n) — manfiy darajali
Haqiqiy x ni butun n (manfiy ham) darajaga ko'taradi, log n qadamda.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const myPow = (x, n) => {
  if (n < 0) { x = 1 / x; n = -n; }
  let result = 1;
  while (n > 0) {
    if (n & 1) result *= x;
    x *= x;
    n = Math.floor(n / 2);
  }
  return result;
};
```
**Python**
```python
def my_pow(x, n):
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n > 0:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result
```

<a id="m497"></a>
### 497. Ko'paytma massivi (o'zidan tashqari, bo'linishsiz)
res[i] = boshqa barcha elementlarning ko'paytmasi; bo'lish ishlatilmaydi.
`⏱ O(n) · 💾 O(1) (chiqishdan tashqari)`

**JS**
```js
const productExceptSelf = (nums) => {
  const n = nums.length, res = new Array(n).fill(1);
  let left = 1;
  for (let i = 0; i < n; i++) { res[i] = left; left *= nums[i]; }
  let right = 1;
  for (let i = n - 1; i >= 0; i--) { res[i] *= right; right *= nums[i]; }
  return res;
};
```
**Python**
```python
def product_except_self(nums):
    n = len(nums)
    res = [1] * n
    left = 1
    for i in range(n):
        res[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        res[i] *= right
        right *= nums[i]
    return res
```

<a id="m498"></a>
### 498. Maksimal ko'paytma uchligi (maximum product of three)
Massivda uchta sonning eng katta ko'paytmasini topadi (manfiylarni hisobga olib).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const maxProductThree = (nums) => {
  let max1 = -Infinity, max2 = -Infinity, max3 = -Infinity;
  let min1 = Infinity, min2 = Infinity;
  for (const x of nums) {
    if (x > max1) { max3 = max2; max2 = max1; max1 = x; }
    else if (x > max2) { max3 = max2; max2 = x; }
    else if (x > max3) max3 = x;
    if (x < min1) { min2 = min1; min1 = x; }
    else if (x < min2) min2 = x;
  }
  return Math.max(max1 * max2 * max3, max1 * min1 * min2);
};
```
**Python**
```python
def max_product_three(nums):
    nums.sort()
    return max(nums[-1] * nums[-2] * nums[-3],
               nums[0] * nums[1] * nums[-1])
```

<a id="m499"></a>
### 499. Ikkilik qo'shish (add binary strings)
Ikki ikkilik satrni qo'shib, ikkilik satr qaytaradi.
`⏱ O(max(n,m)) · 💾 O(max(n,m))`

**JS**
```js
const addBinary = (a, b) => {
  let i = a.length - 1, j = b.length - 1, carry = 0, res = "";
  while (i >= 0 || j >= 0 || carry) {
    let sum = carry;
    if (i >= 0) sum += +a[i--];
    if (j >= 0) sum += +b[j--];
    res = (sum % 2) + res;
    carry = sum >> 1;
  }
  return res;
};
```
**PHP**
```php
function addBinary(string $a, string $b): string {
    $i = strlen($a) - 1; $j = strlen($b) - 1; $carry = 0; $res = "";
    while ($i >= 0 || $j >= 0 || $carry) {
        $sum = $carry;
        if ($i >= 0) $sum += (int)$a[$i--];
        if ($j >= 0) $sum += (int)$b[$j--];
        $res = ($sum % 2) . $res;
        $carry = $sum >> 1;
    }
    return $res;
}
```
**Python**
```python
def add_binary(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]
```

<a id="m500"></a>
### 500. Ikki sonni qo'shish — bitlar bilan (sum without +)
Qo'shish operatorisiz, faqat bit amallari bilan ikki butun sonni qo'shadi.
`⏱ O(1) (32 bit) · 💾 O(1)`

**JS**
```js
const getSum = (a, b) => {
  while (b !== 0) {
    const carry = (a & b) << 1;
    a = (a ^ b) | 0;   // 32-bit ga keltirish
    b = carry | 0;
  }
  return a;
};
```
**Python**
```python
def get_sum(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    a &= mask
    # manfiy natijani belgili songa qaytarish
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)
```

<a id="m501"></a>
### 501. Ikki sonni bo'lish — bo'linishsiz (divide two integers)
Ko'paytirish/bo'lish operatorlarisiz, ayirish va siljitish bilan bo'linmani topadi (32-bit chegara).
`⏱ O(log² n) · 💾 O(1)`

**JS**
```js
const divide = (dividend, divisor) => {
  const INT_MAX = 2 ** 31 - 1, INT_MIN = -(2 ** 31);
  if (dividend === INT_MIN && divisor === -1) return INT_MAX;
  const neg = (dividend < 0) !== (divisor < 0);
  let a = Math.abs(dividend), b = Math.abs(divisor), result = 0;
  while (a >= b) {
    let temp = b, m = 1;
    while (a >= (temp << 1) && (temp << 1) > 0) { temp <<= 1; m <<= 1; }
    a -= temp;
    result += m;
  }
  result = neg ? -result : result;
  return Math.max(INT_MIN, Math.min(INT_MAX, result));
};
```
**Python**
```python
def divide(dividend, divisor):
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    if dividend == INT_MIN and divisor == -1:
        return INT_MAX
    neg = (dividend < 0) != (divisor < 0)
    a, b, result = abs(dividend), abs(divisor), 0
    while a >= b:
        temp, m = b, 1
        while a >= (temp << 1):
            temp <<= 1
            m <<= 1
        a -= temp
        result += m
    result = -result if neg else result
    return max(INT_MIN, min(INT_MAX, result))
```

<a id="m502"></a>
### 502. Mukammal son (perfect number)
O'zidan kichik bo'luvchilari yig'indisi o'ziga teng son (masalan 6, 28).
`⏱ O(√n) · 💾 O(1)`

**JS**
```js
const isPerfect = (n) => {
  if (n < 2) return false;
  let sum = 1;
  for (let i = 2; i * i <= n; i++) {
    if (n % i === 0) {
      sum += i;
      if (i !== Math.floor(n / i)) sum += Math.floor(n / i);
    }
  }
  return sum === n;
};
```
**PHP**
```php
function isPerfect(int $n): bool {
    if ($n < 2) return false;
    $sum = 1;
    for ($i = 2; $i * $i <= $n; $i++) {
        if ($n % $i === 0) {
            $sum += $i;
            if ($i !== intdiv($n, $i)) $sum += intdiv($n, $i);
        }
    }
    return $sum === $n;
}
```
**Python**
```python
def is_perfect(n):
    if n < 2:
        return False
    total = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        i += 1
    return total == n
```

<a id="m503"></a>
### 503. Xunuk son tekshiruvi (ugly number)
Faqat 2, 3, 5 tub ko'paytuvchilaridan iborat musbat son.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const isUgly = (n) => {
  if (n <= 0) return false;
  for (const f of [2, 3, 5])
    while (n % f === 0) n = Math.floor(n / f);
  return n === 1;
};
```
**Python**
```python
def is_ugly(n):
    if n <= 0:
        return False
    for f in (2, 3, 5):
        while n % f == 0:
            n //= f
    return n == 1
```

<a id="m504"></a>
### 504. Super daraja (super pow)
a^b mod 1337, bu yerda b juda katta va massiv (raqamlari) ko'rinishida berilgan.
`⏱ O(len(b) · log) · 💾 O(1)`

**Python**
```python
def super_pow(a, b):
    mod = 1337
    def pm(x, k):
        x %= mod
        res = 1
        for _ in range(k):
            res = res * x % mod
        return res
    result = 1
    for digit in b:
        result = pm(result, 10) * pm(a, digit) % mod
    return result
```
**JS**
```js
const superPow = (a, b) => {
  const mod = 1337;
  const pm = (x, k) => {
    x %= mod; let res = 1;
    for (let i = 0; i < k; i++) res = (res * x) % mod;
    return res;
  };
  let result = 1;
  for (const digit of b) result = (pm(result, 10) * pm(a, digit)) % mod;
  return result;
};
```

<a id="m505"></a>
### 505. Tublar sonini sanash (count primes, elak bilan)
n dan qat'iy kichik bo'lgan tub sonlar miqdorini Eratosfen elagi bilan sanaydi.
`⏱ O(n log log n) · 💾 O(n)`

**JS**
```js
const countPrimes = (n) => {
  if (n < 3) return 0;
  const isPrime = new Array(n).fill(true);
  isPrime[0] = isPrime[1] = false;
  for (let i = 2; i * i < n; i++)
    if (isPrime[i])
      for (let j = i * i; j < n; j += i) isPrime[j] = false;
  return isPrime.filter(Boolean).length;
};
```
**Python**
```python
def count_primes(n):
    if n < 3:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n, i):
                is_prime[j] = False
    return sum(is_prime)
```

<a id="m506"></a>
### 506. Tub son tekshiruvi — Miller–Rabin (deterministik 64-bit)
Katta sonlar uchun tezkor, 64-bit ichida deterministik tublik testi.
`⏱ O(k log³ n) · 💾 O(1)`

**Python**
```python
def is_prime_mr(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True
```
**JS**
```js
const isPrimeMR = (n) => {
  n = BigInt(n);
  if (n < 2n) return false;
  const small = [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n];
  for (const p of small) { if (n % p === 0n) return n === p; }
  let d = n - 1n, r = 0n;
  while (d % 2n === 0n) { d /= 2n; r++; }
  const powMod = (b, e, m) => {
    let res = 1n; b %= m;
    while (e > 0n) { if (e & 1n) res = (res * b) % m; b = (b * b) % m; e >>= 1n; }
    return res;
  };
  for (const a of small) {
    let x = powMod(a, d, n);
    if (x === 1n || x === n - 1n) continue;
    let composite = true;
    for (let i = 0n; i < r - 1n; i++) {
      x = (x * x) % n;
      if (x === n - 1n) { composite = false; break; }
    }
    if (composite) return false;
  }
  return true;
};
```
