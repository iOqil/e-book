<a id="b26"></a>
# 26-bo'lim: Ilg'or dinamik dasturlash (DP)

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Dinamik dasturlash (dynamic programming) — katta masalani o'zaro bog'liq kichik
> kichik masalalarga bo'lib, ularning natijalarini bir marta hisoblab saqlab qo'yish
> (memoizatsiya yoki pastdan-yuqoriga jadval) orqali yechish usuli. Bu bo'limda asosiy
> DP (Fibonacci, coin change, knapsack, LCS, LIS) dan keyingi ilg'or mavzular jamlangan:
> ikki o'lchovli grid DP, satrlar ustida DP (word break, regex/wildcard matching,
> interleaving), intervalli DP (matrix chain, burst balloons, MCM), o'yin nazariyasi
> (stone game, predict the winner), aksiyalar oilasi, hamda klassik LeetCode masalalari.
> Har bir yechim odatda 3 tilda (JS / PHP / Python) berilgan.

<a id="m407"></a>
### 407. Cheksiz ryukzak (unbounded knapsack)
Har bir buyumni cheksiz marta olish mumkin; sig'im W uchun maksimal qiymat.
`⏱ O(n × W) · 💾 O(W)`

**JS**
```js
const unboundedKnapsack = (weights, values, W) => {
  const dp = Array(W + 1).fill(0);
  for (let c = 1; c <= W; c++)
    for (let i = 0; i < weights.length; i++)
      if (weights[i] <= c)
        dp[c] = Math.max(dp[c], dp[c - weights[i]] + values[i]);
  return dp[W];
};
```
**PHP**
```php
function unboundedKnapsack(array $weights, array $values, int $W): int {
    $dp = array_fill(0, $W + 1, 0);
    for ($c = 1; $c <= $W; $c++)
        for ($i = 0; $i < count($weights); $i++)
            if ($weights[$i] <= $c)
                $dp[$c] = max($dp[$c], $dp[$c - $weights[$i]] + $values[$i]);
    return $dp[$W];
}
```
**Python**
```python
def unbounded_knapsack(weights, values, W):
    dp = [0] * (W + 1)
    for c in range(1, W + 1):
        for w, v in zip(weights, values):
            if w <= c:
                dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]
```

<a id="m408"></a>
### 408. Tayoqni kesish (rod cutting)
Uzunligi n bo'lgan tayoqni kesib, narxlar bo'yicha maksimal daromad.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const rodCutting = (price, n) => {
  const dp = Array(n + 1).fill(0);
  for (let len = 1; len <= n; len++)
    for (let cut = 1; cut <= len; cut++)
      dp[len] = Math.max(dp[len], price[cut - 1] + dp[len - cut]);
  return dp[n];
};
```
**PHP**
```php
function rodCutting(array $price, int $n): int {
    $dp = array_fill(0, $n + 1, 0);
    for ($len = 1; $len <= $n; $len++)
        for ($cut = 1; $cut <= $len; $cut++)
            $dp[$len] = max($dp[$len], $price[$cut - 1] + $dp[$len - $cut]);
    return $dp[$n];
}
```
**Python**
```python
def rod_cutting(price, n):
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            dp[length] = max(dp[length], price[cut - 1] + dp[length - cut])
    return dp[n]
```

<a id="m409"></a>
### 409. Matritsalar ko'paytmasi tartibi (matrix chain multiplication)
Matritsalarni ko'paytirish uchun minimal skalyar ko'paytirishlar soni.
`⏱ O(n³) · 💾 O(n²)`

**JS**
```js
const matrixChain = (dims) => {
  const n = dims.length - 1;
  const dp = Array.from({ length: n }, () => Array(n).fill(0));
  for (let len = 2; len <= n; len++)
    for (let i = 0; i + len - 1 < n; i++) {
      const j = i + len - 1;
      dp[i][j] = Infinity;
      for (let k = i; k < j; k++)
        dp[i][j] = Math.min(dp[i][j],
          dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]);
    }
  return dp[0][n - 1];
};
```
**PHP**
```php
function matrixChain(array $dims): int {
    $n = count($dims) - 1;
    $dp = array_fill(0, $n, array_fill(0, $n, 0));
    for ($len = 2; $len <= $n; $len++)
        for ($i = 0; $i + $len - 1 < $n; $i++) {
            $j = $i + $len - 1;
            $dp[$i][$j] = PHP_INT_MAX;
            for ($k = $i; $k < $j; $k++)
                $dp[$i][$j] = min($dp[$i][$j],
                    $dp[$i][$k] + $dp[$k + 1][$j] + $dims[$i] * $dims[$k + 1] * $dims[$j + 1]);
        }
    return $dp[0][$n - 1];
}
```
**Python**
```python
def matrix_chain(dims):
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                dp[i][j] = min(dp[i][j],
                               dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1])
    return dp[0][n - 1]
```

<a id="m410"></a>
### 410. Palindrom bo'laklash II — minimal kesishlar (palindrome partitioning II)
Satrni palindromlarga bo'lish uchun kerakli minimal kesishlar soni.
`⏱ O(n²) · 💾 O(n²)`

**JS**
```js
const minCut = (s) => {
  const n = s.length;
  const pal = Array.from({ length: n }, () => Array(n).fill(false));
  const dp = Array(n).fill(0);
  for (let i = 0; i < n; i++) {
    let best = i;
    for (let j = 0; j <= i; j++)
      if (s[j] === s[i] && (i - j < 2 || pal[j + 1][i - 1])) {
        pal[j][i] = true;
        best = j === 0 ? 0 : Math.min(best, dp[j - 1] + 1);
      }
    dp[i] = best;
  }
  return dp[n - 1];
};
```
**PHP**
```php
function minCut(string $s): int {
    $n = strlen($s);
    if ($n === 0) return 0;
    $pal = array_fill(0, $n, array_fill(0, $n, false));
    $dp = array_fill(0, $n, 0);
    for ($i = 0; $i < $n; $i++) {
        $best = $i;
        for ($j = 0; $j <= $i; $j++)
            if ($s[$j] === $s[$i] && ($i - $j < 2 || $pal[$j + 1][$i - 1])) {
                $pal[$j][$i] = true;
                $best = $j === 0 ? 0 : min($best, $dp[$j - 1] + 1);
            }
        $dp[$i] = $best;
    }
    return $dp[$n - 1];
}
```
**Python**
```python
def min_cut(s):
    n = len(s)
    if n == 0:
        return 0
    pal = [[False] * n for _ in range(n)]
    dp = [0] * n
    for i in range(n):
        best = i
        for j in range(i + 1):
            if s[j] == s[i] and (i - j < 2 or pal[j + 1][i - 1]):
                pal[j][i] = True
                best = 0 if j == 0 else min(best, dp[j - 1] + 1)
        dp[i] = best
    return dp[n - 1]
```

<a id="m411"></a>
### 411. So'zga bo'lish (word break)
Satrni lug'atdagi so'zlarga bo'lish mumkinligini aniqlash.
`⏱ O(n² ) · 💾 O(n)`

**JS**
```js
const wordBreak = (s, words) => {
  const dict = new Set(words);
  const n = s.length;
  const dp = Array(n + 1).fill(false);
  dp[0] = true;
  for (let i = 1; i <= n; i++)
    for (let j = 0; j < i; j++)
      if (dp[j] && dict.has(s.slice(j, i))) { dp[i] = true; break; }
  return dp[n];
};
```
**PHP**
```php
function wordBreak(string $s, array $words): bool {
    $dict = array_flip($words);
    $n = strlen($s);
    $dp = array_fill(0, $n + 1, false);
    $dp[0] = true;
    for ($i = 1; $i <= $n; $i++)
        for ($j = 0; $j < $i; $j++)
            if ($dp[$j] && isset($dict[substr($s, $j, $i - $j)])) { $dp[$i] = true; break; }
    return $dp[$n];
}
```
**Python**
```python
def word_break(s, words):
    dict_ = set(words)
    n = len(s)
    dp = [True] + [False] * n
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in dict_:
                dp[i] = True
                break
    return dp[n]
```

<a id="m412"></a>
### 412. Eng uzun palindrom ketma-ketlik (longest palindromic subsequence)
Satr ichidan eng uzun palindrom bo'la oladigan ketma-ketlik uzunligi.
`⏱ O(n²) · 💾 O(n²)`

**JS**
```js
const longestPalindromeSubseq = (s) => {
  const n = s.length;
  const dp = Array.from({ length: n }, () => Array(n).fill(0));
  for (let i = n - 1; i >= 0; i--) {
    dp[i][i] = 1;
    for (let j = i + 1; j < n; j++)
      dp[i][j] = s[i] === s[j]
        ? dp[i + 1][j - 1] + 2
        : Math.max(dp[i + 1][j], dp[i][j - 1]);
  }
  return dp[0][n - 1];
};
```
**PHP**
```php
function longestPalindromeSubseq(string $s): int {
    $n = strlen($s);
    $dp = array_fill(0, $n, array_fill(0, $n, 0));
    for ($i = $n - 1; $i >= 0; $i--) {
        $dp[$i][$i] = 1;
        for ($j = $i + 1; $j < $n; $j++)
            $dp[$i][$j] = $s[$i] === $s[$j]
                ? $dp[$i + 1][$j - 1] + 2
                : max($dp[$i + 1][$j], $dp[$i][$j - 1]);
    }
    return $dp[0][$n - 1];
}
```
**Python**
```python
def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            dp[i][j] = (dp[i + 1][j - 1] + 2 if s[i] == s[j]
                        else max(dp[i + 1][j], dp[i][j - 1]))
    return dp[0][n - 1]
```

<a id="m413"></a>
### 413. Palindrom qism-satrlar soni (palindromic substrings count)
Satrdagi barcha palindrom qism-satrlar (substring) sonini sanash.
`⏱ O(n²) · 💾 O(1)`

**JS**
```js
const countSubstrings = (s) => {
  const n = s.length;
  let count = 0;
  const expand = (l, r) => {
    while (l >= 0 && r < n && s[l] === s[r]) { count++; l--; r++; }
  };
  for (let i = 0; i < n; i++) { expand(i, i); expand(i, i + 1); }
  return count;
};
```
**PHP**
```php
function countSubstrings(string $s): int {
    $n = strlen($s);
    $count = 0;
    $expand = function ($l, $r) use ($s, $n, &$count) {
        while ($l >= 0 && $r < $n && $s[$l] === $s[$r]) { $count++; $l--; $r++; }
    };
    for ($i = 0; $i < $n; $i++) { $expand($i, $i); $expand($i, $i + 1); }
    return $count;
}
```
**Python**
```python
def count_substrings(s):
    n = len(s)
    count = 0

    def expand(l, r):
        nonlocal count
        while l >= 0 and r < n and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1

    for i in range(n):
        expand(i, i)
        expand(i, i + 1)
    return count
```

<a id="m414"></a>
### 414. Turli ketma-ketliklar soni (distinct subsequences)
s satrida t qism-ketma-ketligi necha xil usulda uchrashini sanash.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const numDistinct = (s, t) => {
  const n = t.length;
  const dp = Array(n + 1).fill(0);
  dp[0] = 1;
  for (const ch of s)
    for (let j = n; j >= 1; j--)
      if (ch === t[j - 1]) dp[j] += dp[j - 1];
  return dp[n];
};
```
**PHP**
```php
function numDistinct(string $s, string $t): int {
    $n = strlen($t);
    $dp = array_fill(0, $n + 1, 0);
    $dp[0] = 1;
    for ($k = 0; $k < strlen($s); $k++)
        for ($j = $n; $j >= 1; $j--)
            if ($s[$k] === $t[$j - 1]) $dp[$j] += $dp[$j - 1];
    return $dp[$n];
}
```
**Python**
```python
def num_distinct(s, t):
    n = len(t)
    dp = [1] + [0] * n
    for ch in s:
        for j in range(n, 0, -1):
            if ch == t[j - 1]:
                dp[j] += dp[j - 1]
    return dp[n]
```

<a id="m415"></a>
### 415. Muntazam ifoda moslashtirish (regular expression matching)
`.` (istalgan belgi) va `*` (oldingi belgi 0+ marta) bilan to'liq moslikni tekshirish.
`⏱ O(m × n) · 💾 O(m × n)`

**JS**
```js
const isMatch = (s, p) => {
  const m = s.length, n = p.length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(false));
  dp[0][0] = true;
  for (let j = 1; j <= n; j++)
    if (p[j - 1] === '*') dp[0][j] = dp[0][j - 2];
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++) {
      if (p[j - 1] === '*') {
        dp[i][j] = dp[i][j - 2] ||
          ((p[j - 2] === '.' || p[j - 2] === s[i - 1]) && dp[i - 1][j]);
      } else {
        dp[i][j] = (p[j - 1] === '.' || p[j - 1] === s[i - 1]) && dp[i - 1][j - 1];
      }
    }
  return dp[m][n];
};
```
**PHP**
```php
function isMatchRegex(string $s, string $p): bool {
    $m = strlen($s); $n = strlen($p);
    $dp = array_fill(0, $m + 1, array_fill(0, $n + 1, false));
    $dp[0][0] = true;
    for ($j = 1; $j <= $n; $j++)
        if ($p[$j - 1] === '*') $dp[0][$j] = $dp[0][$j - 2];
    for ($i = 1; $i <= $m; $i++)
        for ($j = 1; $j <= $n; $j++) {
            if ($p[$j - 1] === '*') {
                $dp[$i][$j] = $dp[$i][$j - 2] ||
                    (($p[$j - 2] === '.' || $p[$j - 2] === $s[$i - 1]) && $dp[$i - 1][$j]);
            } else {
                $dp[$i][$j] = ($p[$j - 1] === '.' || $p[$j - 1] === $s[$i - 1]) && $dp[$i - 1][$j - 1];
            }
        }
    return $dp[$m][$n];
}
```
**Python**
```python
def is_match_regex(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2] or (
                    p[j - 2] in (".", s[i - 1]) and dp[i - 1][j])
            else:
                dp[i][j] = p[j - 1] in (".", s[i - 1]) and dp[i - 1][j - 1]
    return dp[m][n]
```

<a id="m416"></a>
### 416. Wildcard moslashtirish (wildcard matching)
`?` (bitta belgi) va `*` (istalgan ketma-ketlik) bilan to'liq moslikni tekshirish.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const wildcardMatch = (s, p) => {
  const m = s.length, n = p.length;
  let dp = Array(n + 1).fill(false);
  dp[0] = true;
  for (let j = 1; j <= n; j++) dp[j] = dp[j - 1] && p[j - 1] === '*';
  for (let i = 1; i <= m; i++) {
    const ndp = Array(n + 1).fill(false);
    for (let j = 1; j <= n; j++) {
      if (p[j - 1] === '*') ndp[j] = ndp[j - 1] || dp[j];
      else if (p[j - 1] === '?' || p[j - 1] === s[i - 1]) ndp[j] = dp[j - 1];
    }
    dp = ndp;
  }
  return dp[n];
};
```
**PHP**
```php
function wildcardMatch(string $s, string $p): bool {
    $m = strlen($s); $n = strlen($p);
    $dp = array_fill(0, $n + 1, false);
    $dp[0] = true;
    for ($j = 1; $j <= $n; $j++) $dp[$j] = $dp[$j - 1] && $p[$j - 1] === '*';
    for ($i = 1; $i <= $m; $i++) {
        $ndp = array_fill(0, $n + 1, false);
        for ($j = 1; $j <= $n; $j++) {
            if ($p[$j - 1] === '*') $ndp[$j] = $ndp[$j - 1] || $dp[$j];
            elseif ($p[$j - 1] === '?' || $p[$j - 1] === $s[$i - 1]) $ndp[$j] = $dp[$j - 1];
        }
        $dp = $ndp;
    }
    return $dp[$n];
}
```
**Python**
```python
def wildcard_match(s, p):
    m, n = len(s), len(p)
    dp = [True] + [False] * n
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and p[j - 1] == "*"
    for i in range(1, m + 1):
        ndp = [False] * (n + 1)
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                ndp[j] = ndp[j - 1] or dp[j]
            elif p[j - 1] in ("?", s[i - 1]):
                ndp[j] = dp[j - 1]
        dp = ndp
    return dp[n]
```

<a id="m417"></a>
### 417. Aralashtirilgan satr (interleaving string)
s3 satri s1 va s2 ni tartibni saqlagan holda aralashtirishdan hosil bo'lganmi.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const isInterleave = (s1, s2, s3) => {
  const m = s1.length, n = s2.length;
  if (m + n !== s3.length) return false;
  const dp = Array(n + 1).fill(false);
  dp[0] = true;
  for (let j = 1; j <= n; j++) dp[j] = dp[j - 1] && s2[j - 1] === s3[j - 1];
  for (let i = 1; i <= m; i++) {
    dp[0] = dp[0] && s1[i - 1] === s3[i - 1];
    for (let j = 1; j <= n; j++)
      dp[j] = (dp[j] && s1[i - 1] === s3[i + j - 1]) ||
              (dp[j - 1] && s2[j - 1] === s3[i + j - 1]);
  }
  return dp[n];
};
```
**PHP**
```php
function isInterleave(string $s1, string $s2, string $s3): bool {
    $m = strlen($s1); $n = strlen($s2);
    if ($m + $n !== strlen($s3)) return false;
    $dp = array_fill(0, $n + 1, false);
    $dp[0] = true;
    for ($j = 1; $j <= $n; $j++) $dp[$j] = $dp[$j - 1] && $s2[$j - 1] === $s3[$j - 1];
    for ($i = 1; $i <= $m; $i++) {
        $dp[0] = $dp[0] && $s1[$i - 1] === $s3[$i - 1];
        for ($j = 1; $j <= $n; $j++)
            $dp[$j] = ($dp[$j] && $s1[$i - 1] === $s3[$i + $j - 1]) ||
                      ($dp[$j - 1] && $s2[$j - 1] === $s3[$i + $j - 1]);
    }
    return $dp[$n];
}
```
**Python**
```python
def is_interleave(s1, s2, s3):
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [True] + [False] * n
    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, n + 1):
            dp[j] = (dp[j] and s1[i - 1] == s3[i + j - 1]) or \
                    (dp[j - 1] and s2[j - 1] == s3[i + j - 1])
    return dp[n]
```

<a id="m418"></a>
### 418. Grid bo'ylab minimal yo'l (minimum path sum)
Faqat o'ng/past yurib chap-yuqoridan o'ng-pastga eng kichik yig'indi.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const minPathSum = (grid) => {
  const m = grid.length, n = grid[0].length;
  const dp = Array(n).fill(Infinity);
  dp[0] = 0;
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++) {
      if (j > 0) dp[j] = Math.min(dp[j], dp[j - 1]);
      dp[j] += grid[i][j];
    }
  return dp[n - 1];
};
```
**PHP**
```php
function minPathSum(array $grid): int {
    $m = count($grid); $n = count($grid[0]);
    $dp = array_fill(0, $n, PHP_INT_MAX);
    $dp[0] = 0;
    for ($i = 0; $i < $m; $i++)
        for ($j = 0; $j < $n; $j++) {
            if ($j > 0) $dp[$j] = min($dp[$j], $dp[$j - 1]);
            $dp[$j] += $grid[$i][$j];
        }
    return $dp[$n - 1];
}
```
**Python**
```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [float("inf")] * n
    dp[0] = 0
    for i in range(m):
        for j in range(n):
            if j > 0:
                dp[j] = min(dp[j], dp[j - 1])
            dp[j] += grid[i][j]
    return dp[n - 1]
```

<a id="m419"></a>
### 419. Uchburchakda minimal yo'l (triangle minimum path)
Uchburchak ustidan pastga tushib eng kichik yig'indini topish.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const minimumTotal = (triangle) => {
  const dp = [...triangle[triangle.length - 1]];
  for (let i = triangle.length - 2; i >= 0; i--)
    for (let j = 0; j <= i; j++)
      dp[j] = triangle[i][j] + Math.min(dp[j], dp[j + 1]);
  return dp[0];
};
```
**PHP**
```php
function minimumTotal(array $triangle): int {
    $dp = $triangle[count($triangle) - 1];
    for ($i = count($triangle) - 2; $i >= 0; $i--)
        for ($j = 0; $j <= $i; $j++)
            $dp[$j] = $triangle[$i][$j] + min($dp[$j], $dp[$j + 1]);
    return $dp[0];
}
```
**Python**
```python
def minimum_total(triangle):
    dp = list(triangle[-1])
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(i + 1):
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
    return dp[0]
```

<a id="m420"></a>
### 420. Eng katta kvadrat (maximal square)
0/1 matritsada faqat 1 lardan iborat eng katta kvadrat yuzasi.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const maximalSquare = (matrix) => {
  const m = matrix.length, n = matrix[0].length;
  const dp = Array(n + 1).fill(0);
  let best = 0, prev = 0;
  for (let i = 1; i <= m; i++) {
    prev = 0;
    for (let j = 1; j <= n; j++) {
      const tmp = dp[j];
      if (matrix[i - 1][j - 1] === '1' || matrix[i - 1][j - 1] === 1) {
        dp[j] = Math.min(dp[j], dp[j - 1], prev) + 1;
        best = Math.max(best, dp[j]);
      } else dp[j] = 0;
      prev = tmp;
    }
  }
  return best * best;
};
```
**PHP**
```php
function maximalSquare(array $matrix): int {
    $m = count($matrix); $n = count($matrix[0]);
    $dp = array_fill(0, $n + 1, 0);
    $best = 0;
    for ($i = 1; $i <= $m; $i++) {
        $prev = 0;
        for ($j = 1; $j <= $n; $j++) {
            $tmp = $dp[$j];
            if ((string)$matrix[$i - 1][$j - 1] === '1') {
                $dp[$j] = min($dp[$j], $dp[$j - 1], $prev) + 1;
                $best = max($best, $dp[$j]);
            } else $dp[$j] = 0;
            $prev = $tmp;
        }
    }
    return $best * $best;
}
```
**Python**
```python
def maximal_square(matrix):
    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    best = 0
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            tmp = dp[j]
            if str(matrix[i - 1][j - 1]) == "1":
                dp[j] = min(dp[j], dp[j - 1], prev) + 1
                best = max(best, dp[j])
            else:
                dp[j] = 0
            prev = tmp
    return best * best
```

<a id="m421"></a>
### 421. Eng katta to'rtburchak (maximal rectangle)
0/1 matritsada faqat 1 lardan iborat eng katta to'rtburchak yuzasi (histogram usuli).
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const maximalRectangle = (matrix) => {
  if (!matrix.length) return 0;
  const n = matrix[0].length;
  const heights = Array(n).fill(0);
  let best = 0;
  const largestInHist = (h) => {
    const stack = []; let area = 0;
    for (let i = 0; i <= h.length; i++) {
      const cur = i === h.length ? 0 : h[i];
      while (stack.length && h[stack[stack.length - 1]] >= cur) {
        const height = h[stack.pop()];
        const width = stack.length ? i - stack[stack.length - 1] - 1 : i;
        area = Math.max(area, height * width);
      }
      stack.push(i);
    }
    return area;
  };
  for (const row of matrix) {
    for (let j = 0; j < n; j++)
      heights[j] = (row[j] === '1' || row[j] === 1) ? heights[j] + 1 : 0;
    best = Math.max(best, largestInHist(heights));
  }
  return best;
};
```
**PHP**
```php
function maximalRectangle(array $matrix): int {
    if (!count($matrix)) return 0;
    $n = count($matrix[0]);
    $heights = array_fill(0, $n, 0);
    $best = 0;
    $largest = function (array $h): int {
        $stack = []; $area = 0; $len = count($h);
        for ($i = 0; $i <= $len; $i++) {
            $cur = $i === $len ? 0 : $h[$i];
            while ($stack && $h[end($stack)] >= $cur) {
                $height = $h[array_pop($stack)];
                $width = $stack ? $i - end($stack) - 1 : $i;
                $area = max($area, $height * $width);
            }
            $stack[] = $i;
        }
        return $area;
    };
    foreach ($matrix as $row) {
        for ($j = 0; $j < $n; $j++)
            $heights[$j] = ((string)$row[$j] === '1') ? $heights[$j] + 1 : 0;
        $best = max($best, $largest($heights));
    }
    return $best;
}
```
**Python**
```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0
    n = len(matrix[0])
    heights = [0] * n
    best = 0

    def largest(h):
        stack, area = [], 0
        for i in range(len(h) + 1):
            cur = 0 if i == len(h) else h[i]
            while stack and h[stack[-1]] >= cur:
                height = h[stack.pop()]
                width = i - stack[-1] - 1 if stack else i
                area = max(area, height * width)
            stack.append(i)
        return area

    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if str(row[j]) == "1" else 0
        best = max(best, largest(heights))
    return best
```

<a id="m422"></a>
### 422. Zindon o'yini (dungeon game)
Ritsar chap-yuqoridan o'ng-pastga yetib borishi uchun zarur minimal boshlang'ich jon.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const calculateMinimumHP = (dungeon) => {
  const m = dungeon.length, n = dungeon[0].length;
  const dp = Array(n + 1).fill(Infinity);
  dp[n - 1] = 1;
  for (let i = m - 1; i >= 0; i--)
    for (let j = n - 1; j >= 0; j--) {
      const need = Math.min(dp[j], dp[j + 1]) - dungeon[i][j];
      dp[j] = need <= 0 ? 1 : need;
    }
  return dp[0];
};
```
**PHP**
```php
function calculateMinimumHP(array $dungeon): int {
    $m = count($dungeon); $n = count($dungeon[0]);
    $dp = array_fill(0, $n + 1, PHP_INT_MAX);
    $dp[$n - 1] = 1;
    for ($i = $m - 1; $i >= 0; $i--)
        for ($j = $n - 1; $j >= 0; $j--) {
            $need = min($dp[$j], $dp[$j + 1]) - $dungeon[$i][$j];
            $dp[$j] = $need <= 0 ? 1 : $need;
        }
    return $dp[0];
}
```
**Python**
```python
def calculate_minimum_hp(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [float("inf")] * (n + 1)
    dp[n - 1] = 1
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            need = min(dp[j], dp[j + 1]) - dungeon[i][j]
            dp[j] = 1 if need <= 0 else need
    return dp[0]
```

<a id="m423"></a>
### 423. Aksiya — sovish davri bilan (stock with cooldown)
Sotgandan keyin 1 kun dam olish sharti bilan maksimal foyda.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const maxProfitCooldown = (prices) => {
  let hold = -Infinity, sold = 0, rest = 0;
  for (const p of prices) {
    const prevSold = sold;
    sold = hold + p;
    hold = Math.max(hold, rest - p);
    rest = Math.max(rest, prevSold);
  }
  return Math.max(sold, rest);
};
```
**PHP**
```php
function maxProfitCooldown(array $prices): int {
    $hold = PHP_INT_MIN; $sold = 0; $rest = 0;
    foreach ($prices as $p) {
        $prevSold = $sold;
        $sold = $hold + $p;
        $hold = max($hold, $rest - $p);
        $rest = max($rest, $prevSold);
    }
    return max($sold, $rest);
}
```
**Python**
```python
def max_profit_cooldown(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
    return max(sold, rest)
```

<a id="m424"></a>
### 424. Aksiya — tranzaksiya haqi bilan (stock with transaction fee)
Har bir savdoda fee to'lab maksimal foyda.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const maxProfitFee = (prices, fee) => {
  let cash = 0, hold = -prices[0];
  for (let i = 1; i < prices.length; i++) {
    cash = Math.max(cash, hold + prices[i] - fee);
    hold = Math.max(hold, cash - prices[i]);
  }
  return cash;
};
```
**PHP**
```php
function maxProfitFee(array $prices, int $fee): int {
    $cash = 0; $hold = -$prices[0];
    for ($i = 1; $i < count($prices); $i++) {
        $cash = max($cash, $hold + $prices[$i] - $fee);
        $hold = max($hold, $cash - $prices[$i]);
    }
    return $cash;
}
```
**Python**
```python
def max_profit_fee(prices, fee):
    cash, hold = 0, -prices[0]
    for p in prices[1:]:
        cash = max(cash, hold + p - fee)
        hold = max(hold, cash - p)
    return cash
```

<a id="m425"></a>
### 425. Aksiya — ko'pi bilan k tranzaksiya (stock at most k transactions)
Eng ko'pi bilan k marta savdo qilib maksimal foyda.
`⏱ O(n × k) · 💾 O(k)`

**JS**
```js
const maxProfitK = (k, prices) => {
  const n = prices.length;
  if (n === 0) return 0;
  if (k >= n / 2) {
    let profit = 0;
    for (let i = 1; i < n; i++)
      if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];
    return profit;
  }
  const buy = Array(k + 1).fill(-Infinity), sell = Array(k + 1).fill(0);
  for (const p of prices)
    for (let j = 1; j <= k; j++) {
      buy[j] = Math.max(buy[j], sell[j - 1] - p);
      sell[j] = Math.max(sell[j], buy[j] + p);
    }
  return sell[k];
};
```
**PHP**
```php
function maxProfitK(int $k, array $prices): int {
    $n = count($prices);
    if ($n === 0) return 0;
    if ($k >= $n / 2) {
        $profit = 0;
        for ($i = 1; $i < $n; $i++)
            if ($prices[$i] > $prices[$i - 1]) $profit += $prices[$i] - $prices[$i - 1];
        return $profit;
    }
    $buy = array_fill(0, $k + 1, PHP_INT_MIN);
    $sell = array_fill(0, $k + 1, 0);
    foreach ($prices as $p)
        for ($j = 1; $j <= $k; $j++) {
            $buy[$j] = max($buy[$j], $sell[$j - 1] - $p);
            $sell[$j] = max($sell[$j], $buy[$j] + $p);
        }
    return $sell[$k];
}
```
**Python**
```python
def max_profit_k(k, prices):
    n = len(prices)
    if n == 0:
        return 0
    if k >= n // 2:
        return sum(max(prices[i] - prices[i - 1], 0) for i in range(1, n))
    buy = [float("-inf")] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
```

<a id="m426"></a>
### 426. Uylarni bo'yash (paint house)
Har uyni 3 rangdan biriga, qo'shni uylar har xil rangda — minimal narx.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const minCostPaintHouse = (costs) => {
  let [a, b, c] = [0, 0, 0];
  for (const [r, g, bl] of costs) {
    [a, b, c] = [
      r + Math.min(b, c),
      g + Math.min(a, c),
      bl + Math.min(a, b),
    ];
  }
  return Math.min(a, b, c);
};
```
**PHP**
```php
function minCostPaintHouse(array $costs): int {
    $a = 0; $b = 0; $c = 0;
    foreach ($costs as [$r, $g, $bl]) {
        [$a, $b, $c] = [
            $r + min($b, $c),
            $g + min($a, $c),
            $bl + min($a, $b),
        ];
    }
    return min($a, $b, $c);
}
```
**Python**
```python
def min_cost_paint_house(costs):
    a = b = c = 0
    for r, g, bl in costs:
        a, b, c = r + min(b, c), g + min(a, c), bl + min(a, b)
    return min(a, b, c)
```

<a id="m427"></a>
### 427. Panjarani bo'yash (paint fence)
n panjarani k rangda bo'yash; uchtadan ko'pi ketma-ket bir xil bo'lmasin.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const numWaysPaintFence = (n, k) => {
  if (n === 0) return 0;
  if (n === 1) return k;
  let same = k, diff = k * (k - 1);
  for (let i = 3; i <= n; i++) {
    const newDiff = (same + diff) * (k - 1);
    same = diff;
    diff = newDiff;
  }
  return same + diff;
};
```
**PHP**
```php
function numWaysPaintFence(int $n, int $k): int {
    if ($n === 0) return 0;
    if ($n === 1) return $k;
    $same = $k; $diff = $k * ($k - 1);
    for ($i = 3; $i <= $n; $i++) {
        $newDiff = ($same + $diff) * ($k - 1);
        $same = $diff;
        $diff = $newDiff;
    }
    return $same + $diff;
}
```
**Python**
```python
def num_ways_paint_fence(n, k):
    if n == 0:
        return 0
    if n == 1:
        return k
    same, diff = k, k * (k - 1)
    for _ in range(3, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff
```

<a id="m428"></a>
### 428. Xabarni dekodlash II (decode ways II)
`*` joker belgisi (1–9) bilan A–Z kodlangan satrni dekodlash usullari soni (mod 1e9+7).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const numDecodingsII = (s) => {
  const MOD = 1000000007n;
  let prev = 1n, cur = s[0] === '*' ? 9n : (s[0] === '0' ? 0n : 1n);
  const oneWays = (c) => c === '*' ? 9n : (c === '0' ? 0n : 1n);
  const twoWays = (a, b) => {
    if (a === '*' && b === '*') return 15n;
    if (a === '*') return +b <= 6 ? 2n : 1n;
    if (b === '*') return a === '1' ? 9n : (a === '2' ? 6n : 0n);
    const v = +(a + b);
    return v >= 10 && v <= 26 ? 1n : 0n;
  };
  for (let i = 1; i < s.length; i++) {
    const nxt = (oneWays(s[i]) * cur + twoWays(s[i - 1], s[i]) * prev) % MOD;
    prev = cur; cur = nxt;
  }
  return Number(cur);
};
```
**PHP**
```php
function numDecodingsII(string $s): int {
    $MOD = 1000000007;
    $oneWays = fn($c) => $c === '*' ? 9 : ($c === '0' ? 0 : 1);
    $twoWays = function ($a, $b) {
        if ($a === '*' && $b === '*') return 15;
        if ($a === '*') return (int)$b <= 6 ? 2 : 1;
        if ($b === '*') return $a === '1' ? 9 : ($a === '2' ? 6 : 0);
        $v = (int)($a . $b);
        return $v >= 10 && $v <= 26 ? 1 : 0;
    };
    $prev = 1; $cur = $oneWays($s[0]);
    for ($i = 1; $i < strlen($s); $i++) {
        $nxt = ($oneWays($s[$i]) * $cur + $twoWays($s[$i - 1], $s[$i]) * $prev) % $MOD;
        $prev = $cur; $cur = $nxt;
    }
    return $cur % $MOD;
}
```
**Python**
```python
def num_decodings_ii(s):
    MOD = 1000000007

    def one_ways(c):
        return 9 if c == "*" else (0 if c == "0" else 1)

    def two_ways(a, b):
        if a == "*" and b == "*":
            return 15
        if a == "*":
            return 2 if int(b) <= 6 else 1
        if b == "*":
            return 9 if a == "1" else (6 if a == "2" else 0)
        v = int(a + b)
        return 1 if 10 <= v <= 26 else 0

    prev, cur = 1, one_ways(s[0])
    for i in range(1, len(s)):
        prev, cur = cur, (one_ways(s[i]) * cur + two_ways(s[i - 1], s[i]) * prev) % MOD
    return cur % MOD
```

<a id="m429"></a>
### 429. Eng uzun arifmetik ketma-ketlik (longest arithmetic subsequence)
Massivdan farqi bir xil bo'lgan eng uzun qism-ketma-ketlik uzunligi.
`⏱ O(n²) · 💾 O(n²)`

**JS**
```js
const longestArithSeqLength = (nums) => {
  const dp = nums.map(() => new Map());
  let best = 1;
  for (let i = 0; i < nums.length; i++)
    for (let j = 0; j < i; j++) {
      const d = nums[i] - nums[j];
      const len = (dp[j].get(d) || 1) + 1;
      dp[i].set(d, len);
      best = Math.max(best, len);
    }
  return best;
};
```
**PHP**
```php
function longestArithSeqLength(array $nums): int {
    $n = count($nums);
    $dp = array_fill(0, $n, []);
    $best = 1;
    for ($i = 0; $i < $n; $i++)
        for ($j = 0; $j < $i; $j++) {
            $d = $nums[$i] - $nums[$j];
            $len = ($dp[$j][$d] ?? 1) + 1;
            $dp[$i][$d] = $len;
            $best = max($best, $len);
        }
    return $best;
}
```
**Python**
```python
def longest_arith_seq_length(nums):
    dp = [dict() for _ in nums]
    best = 1
    for i in range(len(nums)):
        for j in range(i):
            d = nums[i] - nums[j]
            dp[i][d] = dp[j].get(d, 1) + 1
            best = max(best, dp[i][d])
    return best
```

<a id="m430"></a>
### 430. Eng uzun so'z zanjiri (longest string chain)
Har qadamda bitta harf qo'shib so'zlardan tuzilgan eng uzun zanjir uzunligi.
`⏱ O(n × L²) · 💾 O(n)`

**JS**
```js
const longestStrChain = (words) => {
  words.sort((a, b) => a.length - b.length);
  const dp = new Map();
  let best = 0;
  for (const w of words) {
    let cur = 1;
    for (let i = 0; i < w.length; i++) {
      const pred = w.slice(0, i) + w.slice(i + 1);
      if (dp.has(pred)) cur = Math.max(cur, dp.get(pred) + 1);
    }
    dp.set(w, cur);
    best = Math.max(best, cur);
  }
  return best;
};
```
**PHP**
```php
function longestStrChain(array $words): int {
    usort($words, fn($a, $b) => strlen($a) - strlen($b));
    $dp = []; $best = 0;
    foreach ($words as $w) {
        $cur = 1;
        $len = strlen($w);
        for ($i = 0; $i < $len; $i++) {
            $pred = substr($w, 0, $i) . substr($w, $i + 1);
            if (isset($dp[$pred])) $cur = max($cur, $dp[$pred] + 1);
        }
        $dp[$w] = $cur;
        $best = max($best, $cur);
    }
    return $best;
}
```
**Python**
```python
def longest_str_chain(words):
    words.sort(key=len)
    dp = {}
    best = 0
    for w in words:
        cur = 1
        for i in range(len(w)):
            pred = w[:i] + w[i + 1:]
            if pred in dp:
                cur = max(cur, dp[pred] + 1)
        dp[w] = cur
        best = max(best, cur)
    return best
```

<a id="m431"></a>
### 431. Birlar va nollar (ones and zeroes)
Eng ko'pi bilan m ta 0 va n ta 1 bilan tuzish mumkin bo'lgan satrlar soni.
`⏱ O(L × m × n) · 💾 O(m × n)`

**JS**
```js
const findMaxForm = (strs, m, n) => {
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (const s of strs) {
    const zeros = [...s].filter((c) => c === '0').length;
    const ones = s.length - zeros;
    for (let i = m; i >= zeros; i--)
      for (let j = n; j >= ones; j--)
        dp[i][j] = Math.max(dp[i][j], dp[i - zeros][j - ones] + 1);
  }
  return dp[m][n];
};
```
**PHP**
```php
function findMaxForm(array $strs, int $m, int $n): int {
    $dp = array_fill(0, $m + 1, array_fill(0, $n + 1, 0));
    foreach ($strs as $s) {
        $zeros = substr_count($s, '0');
        $ones = strlen($s) - $zeros;
        for ($i = $m; $i >= $zeros; $i--)
            for ($j = $n; $j >= $ones; $j--)
                $dp[$i][$j] = max($dp[$i][$j], $dp[$i - $zeros][$j - $ones] + 1);
    }
    return $dp[$m][$n];
}
```
**Python**
```python
def find_max_form(strs, m, n):
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count("0")
        ones = len(s) - zeros
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
    return dp[m][n]
```

<a id="m432"></a>
### 432. Kombinatsiyalar yig'indisi IV (combination sum IV)
Tartibli kombinatsiyalar (permutatsiyalar) soni target summa uchun.
`⏱ O(target × n) · 💾 O(target)`

**JS**
```js
const combinationSum4 = (nums, target) => {
  const dp = Array(target + 1).fill(0);
  dp[0] = 1;
  for (let t = 1; t <= target; t++)
    for (const num of nums)
      if (num <= t) dp[t] += dp[t - num];
  return dp[target];
};
```
**PHP**
```php
function combinationSum4(array $nums, int $target): int {
    $dp = array_fill(0, $target + 1, 0);
    $dp[0] = 1;
    for ($t = 1; $t <= $target; $t++)
        foreach ($nums as $num)
            if ($num <= $t) $dp[$t] += $dp[$t - $num];
    return $dp[$target];
}
```
**Python**
```python
def combination_sum4(nums, target):
    dp = [1] + [0] * target
    for t in range(1, target + 1):
        for num in nums:
            if num <= t:
                dp[t] += dp[t - num]
    return dp[target]
```

<a id="m433"></a>
### 433. Mukammal kvadratlar (perfect squares)
n ni mukammal kvadratlar yig'indisi sifatida eng kam son bilan ifodalash.
`⏱ O(n√n) · 💾 O(n)`

**JS**
```js
const numSquares = (n) => {
  const dp = Array(n + 1).fill(Infinity);
  dp[0] = 0;
  for (let i = 1; i <= n; i++)
    for (let j = 1; j * j <= i; j++)
      dp[i] = Math.min(dp[i], dp[i - j * j] + 1);
  return dp[n];
};
```
**PHP**
```php
function numSquares(int $n): int {
    $dp = array_fill(0, $n + 1, PHP_INT_MAX);
    $dp[0] = 0;
    for ($i = 1; $i <= $n; $i++)
        for ($j = 1; $j * $j <= $i; $j++)
            $dp[$i] = min($dp[$i], $dp[$i - $j * $j] + 1);
    return $dp[$n];
}
```
**Python**
```python
def num_squares(n):
    dp = [0] + [float("inf")] * n
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1
    return dp[n]
```

<a id="m434"></a>
### 434. Sonni bo'lish (integer break)
n ni kamida ikkita musbat butun songa bo'lib, ko'paytmasini maksimallashtirish.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const integerBreak = (n) => {
  const dp = Array(n + 1).fill(0);
  dp[1] = 1;
  for (let i = 2; i <= n; i++)
    for (let j = 1; j < i; j++)
      dp[i] = Math.max(dp[i], j * Math.max(i - j, dp[i - j]));
  return dp[n];
};
```
**PHP**
```php
function integerBreak(int $n): int {
    $dp = array_fill(0, $n + 1, 0);
    $dp[1] = 1;
    for ($i = 2; $i <= $n; $i++)
        for ($j = 1; $j < $i; $j++)
            $dp[$i] = max($dp[$i], $j * max($i - $j, $dp[$i - $j]));
    return $dp[$n];
}
```
**Python**
```python
def integer_break(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        for j in range(1, i):
            dp[i] = max(dp[i], j * max(i - j, dp[i - j]))
    return dp[n]
```

<a id="m435"></a>
### 435. Maqsadli yig'indili soqqa tashlashlar (dice rolls with target sum)
n ta k-yoqli soqqada target summani hosil qilish usullari soni (mod 1e9+7).
`⏱ O(n × target × k) · 💾 O(target)`

**JS**
```js
const numRollsToTarget = (n, k, target) => {
  const MOD = 1000000007;
  let dp = Array(target + 1).fill(0);
  dp[0] = 1;
  for (let d = 0; d < n; d++) {
    const ndp = Array(target + 1).fill(0);
    for (let t = 1; t <= target; t++)
      for (let f = 1; f <= k && f <= t; f++)
        ndp[t] = (ndp[t] + dp[t - f]) % MOD;
    dp = ndp;
  }
  return dp[target];
};
```
**PHP**
```php
function numRollsToTarget(int $n, int $k, int $target): int {
    $MOD = 1000000007;
    $dp = array_fill(0, $target + 1, 0);
    $dp[0] = 1;
    for ($d = 0; $d < $n; $d++) {
        $ndp = array_fill(0, $target + 1, 0);
        for ($t = 1; $t <= $target; $t++)
            for ($f = 1; $f <= $k && $f <= $t; $f++)
                $ndp[$t] = ($ndp[$t] + $dp[$t - $f]) % $MOD;
        $dp = $ndp;
    }
    return $dp[$target];
}
```
**Python**
```python
def num_rolls_to_target(n, k, target):
    MOD = 1000000007
    dp = [1] + [0] * target
    for _ in range(n):
        ndp = [0] * (target + 1)
        for t in range(1, target + 1):
            for f in range(1, min(k, t) + 1):
                ndp[t] = (ndp[t] + dp[t - f]) % MOD
        dp = ndp
    return dp[target]
```

<a id="m436"></a>
### 436. Otning ehtimoli shaxmat taxtasida (knight probability on chessboard)
Ot k qadamdan keyin n×n taxtada qolish ehtimoli.
`⏱ O(k × n²) · 💾 O(n²)`

**JS**
```js
const knightProbability = (n, k, row, col) => {
  const moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]];
  let dp = Array.from({ length: n }, () => Array(n).fill(0));
  dp[row][col] = 1;
  for (let s = 0; s < k; s++) {
    const ndp = Array.from({ length: n }, () => Array(n).fill(0));
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++)
        if (dp[r][c] > 0)
          for (const [dr, dc] of moves) {
            const nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < n && nc >= 0 && nc < n)
              ndp[nr][nc] += dp[r][c] / 8;
          }
    dp = ndp;
  }
  let total = 0;
  for (const r of dp) for (const v of r) total += v;
  return total;
};
```
**PHP**
```php
function knightProbability(int $n, int $k, int $row, int $col): float {
    $moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]];
    $dp = array_fill(0, $n, array_fill(0, $n, 0.0));
    $dp[$row][$col] = 1.0;
    for ($s = 0; $s < $k; $s++) {
        $ndp = array_fill(0, $n, array_fill(0, $n, 0.0));
        for ($r = 0; $r < $n; $r++)
            for ($c = 0; $c < $n; $c++)
                if ($dp[$r][$c] > 0)
                    foreach ($moves as [$dr, $dc]) {
                        $nr = $r + $dr; $nc = $c + $dc;
                        if ($nr >= 0 && $nr < $n && $nc >= 0 && $nc < $n)
                            $ndp[$nr][$nc] += $dp[$r][$c] / 8;
                    }
        $dp = $ndp;
    }
    $total = 0.0;
    foreach ($dp as $r) foreach ($r as $v) $total += $v;
    return $total;
}
```
**Python**
```python
def knight_probability(n, k, row, col):
    moves = [(1, 2), (2, 1), (2, -1), (1, -2),
             (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    dp = [[0.0] * n for _ in range(n)]
    dp[row][col] = 1.0
    for _ in range(k):
        ndp = [[0.0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                if dp[r][c]:
                    for dr, dc in moves:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n:
                            ndp[nr][nc] += dp[r][c] / 8
        dp = ndp
    return sum(v for r in dp for v in r)
```

<a id="m437"></a>
### 437. Chegaradan chiqish yo'llari (out of boundary paths)
To'p eng ko'pi bilan N qadamda grid chegarasidan chiqishi usullari soni (mod 1e9+7).
`⏱ O(N × m × n) · 💾 O(m × n)`

**JS**
```js
const findPaths = (m, n, N, sr, sc) => {
  const MOD = 1000000007;
  let dp = Array.from({ length: m }, () => Array(n).fill(0));
  dp[sr][sc] = 1;
  let count = 0;
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  for (let step = 0; step < N; step++) {
    const ndp = Array.from({ length: m }, () => Array(n).fill(0));
    for (let r = 0; r < m; r++)
      for (let c = 0; c < n; c++)
        if (dp[r][c] > 0)
          for (const [dr, dc] of dirs) {
            const nr = r + dr, nc = c + dc;
            if (nr < 0 || nr >= m || nc < 0 || nc >= n) count = (count + dp[r][c]) % MOD;
            else ndp[nr][nc] = (ndp[nr][nc] + dp[r][c]) % MOD;
          }
    dp = ndp;
  }
  return count;
};
```
**PHP**
```php
function findPaths(int $m, int $n, int $N, int $sr, int $sc): int {
    $MOD = 1000000007;
    $dp = array_fill(0, $m, array_fill(0, $n, 0));
    $dp[$sr][$sc] = 1;
    $count = 0;
    $dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    for ($step = 0; $step < $N; $step++) {
        $ndp = array_fill(0, $m, array_fill(0, $n, 0));
        for ($r = 0; $r < $m; $r++)
            for ($c = 0; $c < $n; $c++)
                if ($dp[$r][$c] > 0)
                    foreach ($dirs as [$dr, $dc]) {
                        $nr = $r + $dr; $nc = $c + $dc;
                        if ($nr < 0 || $nr >= $m || $nc < 0 || $nc >= $n)
                            $count = ($count + $dp[$r][$c]) % $MOD;
                        else $ndp[$nr][$nc] = ($ndp[$nr][$nc] + $dp[$r][$c]) % $MOD;
                    }
        $dp = $ndp;
    }
    return $count;
}
```
**Python**
```python
def find_paths(m, n, N, sr, sc):
    MOD = 1000000007
    dp = [[0] * n for _ in range(m)]
    dp[sr][sc] = 1
    count = 0
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for _ in range(N):
        ndp = [[0] * n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                if dp[r][c]:
                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        if not (0 <= nr < m and 0 <= nc < n):
                            count = (count + dp[r][c]) % MOD
                        else:
                            ndp[nr][nc] = (ndp[nr][nc] + dp[r][c]) % MOD
        dp = ndp
    return count
```

<a id="m438"></a>
### 438. Yagona yo'llar II — to'siqlar bilan (unique paths II)
To'siqli gridda chap-yuqoridan o'ng-pastga necha xil yo'l bor.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const uniquePathsWithObstacles = (grid) => {
  const n = grid[0].length;
  const dp = Array(n).fill(0);
  dp[0] = 1;
  for (const row of grid)
    for (let j = 0; j < n; j++) {
      if (row[j] === 1) dp[j] = 0;
      else if (j > 0) dp[j] += dp[j - 1];
    }
  return dp[n - 1];
};
```
**PHP**
```php
function uniquePathsWithObstacles(array $grid): int {
    $n = count($grid[0]);
    $dp = array_fill(0, $n, 0);
    $dp[0] = 1;
    foreach ($grid as $row)
        for ($j = 0; $j < $n; $j++) {
            if ($row[$j] === 1) $dp[$j] = 0;
            elseif ($j > 0) $dp[$j] += $dp[$j - 1];
        }
    return $dp[$n - 1];
}
```
**Python**
```python
def unique_paths_with_obstacles(grid):
    n = len(grid[0])
    dp = [1] + [0] * (n - 1)
    for row in grid:
        for j in range(n):
            if row[j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[n - 1]
```

<a id="m439"></a>
### 439. Minimal tushuvchi yo'l yig'indisi (minimum falling path sum)
Matritsada yuqoridan pastga (qo'shni ustunlarga) tushib eng kichik yig'indi.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const minFallingPathSum = (matrix) => {
  const n = matrix.length;
  let dp = [...matrix[0]];
  for (let i = 1; i < n; i++) {
    const ndp = Array(n).fill(0);
    for (let j = 0; j < n; j++) {
      let best = dp[j];
      if (j > 0) best = Math.min(best, dp[j - 1]);
      if (j < n - 1) best = Math.min(best, dp[j + 1]);
      ndp[j] = matrix[i][j] + best;
    }
    dp = ndp;
  }
  return Math.min(...dp);
};
```
**PHP**
```php
function minFallingPathSum(array $matrix): int {
    $n = count($matrix);
    $dp = $matrix[0];
    for ($i = 1; $i < $n; $i++) {
        $ndp = array_fill(0, $n, 0);
        for ($j = 0; $j < $n; $j++) {
            $best = $dp[$j];
            if ($j > 0) $best = min($best, $dp[$j - 1]);
            if ($j < $n - 1) $best = min($best, $dp[$j + 1]);
            $ndp[$j] = $matrix[$i][$j] + $best;
        }
        $dp = $ndp;
    }
    return min($dp);
}
```
**Python**
```python
def min_falling_path_sum(matrix):
    n = len(matrix)
    dp = list(matrix[0])
    for i in range(1, n):
        ndp = [0] * n
        for j in range(n):
            best = dp[j]
            if j > 0:
                best = min(best, dp[j - 1])
            if j < n - 1:
                best = min(best, dp[j + 1])
            ndp[j] = matrix[i][j] + best
        dp = ndp
    return min(dp)
```

<a id="m440"></a>
### 440. Unli tovushli satrlar soni (count vowels permutation)
n uzunlikdagi, unlilar ketma-ketligi qoidalariga mos satrlar soni (mod 1e9+7).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const countVowelPermutation = (n) => {
  const MOD = 1000000007n;
  let [a, e, i, o, u] = [1n, 1n, 1n, 1n, 1n];
  for (let k = 1; k < n; k++) {
    [a, e, i, o, u] = [
      (e + i + u) % MOD,
      (a + i) % MOD,
      (e + o) % MOD,
      i % MOD,
      (i + o) % MOD,
    ];
  }
  return Number((a + e + i + o + u) % MOD);
};
```
**PHP**
```php
function countVowelPermutation(int $n): int {
    $MOD = 1000000007;
    $a = 1; $e = 1; $i = 1; $o = 1; $u = 1;
    for ($k = 1; $k < $n; $k++) {
        [$a, $e, $i, $o, $u] = [
            ($e + $i + $u) % $MOD,
            ($a + $i) % $MOD,
            ($e + $o) % $MOD,
            $i % $MOD,
            ($i + $o) % $MOD,
        ];
    }
    return ($a + $e + $i + $o + $u) % $MOD;
}
```
**Python**
```python
def count_vowel_permutation(n):
    MOD = 1000000007
    a = e = i = o = u = 1
    for _ in range(n - 1):
        a, e, i, o, u = (e + i + u) % MOD, (a + i) % MOD, \
            (e + o) % MOD, i % MOD, (i + o) % MOD
    return (a + e + i + o + u) % MOD
```

<a id="m441"></a>
### 441. Domino va tromino qoplash (domino and tromino tiling)
2×n maydonni domino va L-tromino bilan qoplash usullari soni (mod 1e9+7).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const numTilings = (n) => {
  const MOD = 1000000007n;
  if (n <= 2) return n;
  let a = 1n, b = 1n, c = 2n; // dp[0], dp[1], dp[2]
  for (let i = 3; i <= n; i++) {
    const d = (2n * c + a) % MOD;
    a = b; b = c; c = d;
  }
  return Number(c);
};
```
**PHP**
```php
function numTilings(int $n): int {
    $MOD = 1000000007;
    if ($n <= 2) return $n;
    $a = 1; $b = 1; $c = 2;
    for ($i = 3; $i <= $n; $i++) {
        $d = (2 * $c + $a) % $MOD;
        $a = $b; $b = $c; $c = $d;
    }
    return $c;
}
```
**Python**
```python
def num_tilings(n):
    MOD = 1000000007
    if n <= 2:
        return n
    a, b, c = 1, 1, 2
    for _ in range(3, n + 1):
        a, b, c = b, c, (2 * c + a) % MOD
    return c
```

<a id="m442"></a>
### 442. Tosh o'yini (stone game)
Ikki o'yinchi navbatma-navbat chetdan tosh oladi; Alice yutadimi (DP yechim).
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const stoneGame = (piles) => {
  const n = piles.length;
  const dp = [...piles];
  for (let len = 2; len <= n; len++)
    for (let i = 0; i + len - 1 < n; i++) {
      const j = i + len - 1;
      dp[i] = Math.max(piles[i] - dp[i + 1], piles[j] - dp[i]);
    }
  return dp[0] > 0;
};
```
**PHP**
```php
function stoneGame(array $piles): bool {
    $n = count($piles);
    $dp = $piles;
    for ($len = 2; $len <= $n; $len++)
        for ($i = 0; $i + $len - 1 < $n; $i++) {
            $j = $i + $len - 1;
            $dp[$i] = max($piles[$i] - $dp[$i + 1], $piles[$j] - $dp[$i]);
        }
    return $dp[0] > 0;
}
```
**Python**
```python
def stone_game(piles):
    n = len(piles)
    dp = list(piles)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i] = max(piles[i] - dp[i + 1], piles[j] - dp[i])
    return dp[0] > 0
```

<a id="m443"></a>
### 443. G'olibni bashorat qilish (predict the winner)
Chetdan son olib, 1-o'yinchi yutishi yoki durang qilishi mumkinmi.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const predictTheWinner = (nums) => {
  const n = nums.length;
  const dp = [...nums];
  for (let len = 2; len <= n; len++)
    for (let i = 0; i + len - 1 < n; i++) {
      const j = i + len - 1;
      dp[i] = Math.max(nums[i] - dp[i + 1], nums[j] - dp[i]);
    }
  return dp[0] >= 0;
};
```
**PHP**
```php
function predictTheWinner(array $nums): bool {
    $n = count($nums);
    $dp = $nums;
    for ($len = 2; $len <= $n; $len++)
        for ($i = 0; $i + $len - 1 < $n; $i++) {
            $j = $i + $len - 1;
            $dp[$i] = max($nums[$i] - $dp[$i + 1], $nums[$j] - $dp[$i]);
        }
    return $dp[0] >= 0;
}
```
**Python**
```python
def predict_the_winner(nums):
    n = len(nums)
    dp = list(nums)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i] = max(nums[i] - dp[i + 1], nums[j] - dp[i])
    return dp[0] >= 0
```

<a id="m444"></a>
### 444. Sharlarni yorish (burst balloons)
Sharlarni yorib maksimal tanga yig'ish (intervalli DP).
`⏱ O(n³) · 💾 O(n²)`

**JS**
```js
const maxCoins = (nums) => {
  const a = [1, ...nums, 1];
  const n = a.length;
  const dp = Array.from({ length: n }, () => Array(n).fill(0));
  for (let len = 2; len < n; len++)
    for (let l = 0; l + len < n; l++) {
      const r = l + len;
      for (let k = l + 1; k < r; k++)
        dp[l][r] = Math.max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]);
    }
  return dp[0][n - 1];
};
```
**PHP**
```php
function maxCoins(array $nums): int {
    $a = array_merge([1], $nums, [1]);
    $n = count($a);
    $dp = array_fill(0, $n, array_fill(0, $n, 0));
    for ($len = 2; $len < $n; $len++)
        for ($l = 0; $l + $len < $n; $l++) {
            $r = $l + $len;
            for ($k = $l + 1; $k < $r; $k++)
                $dp[$l][$r] = max($dp[$l][$r], $dp[$l][$k] + $dp[$k][$r] + $a[$l] * $a[$k] * $a[$r]);
        }
    return $dp[0][$n - 1];
}
```
**Python**
```python
def max_coins(nums):
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(n - length):
            r = l + length
            for k in range(l + 1, r):
                dp[l][r] = max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r])
    return dp[0][n - 1]
```

<a id="m445"></a>
### 445. Tuxum tashlash (super egg drop)
k tuxum va n qavat bilan kritik qavatni topishga kerakli minimal urinishlar soni.
`⏱ O(k × n) · 💾 O(k)`

**JS**
```js
const superEggDrop = (k, n) => {
  const dp = Array(k + 1).fill(0);
  let moves = 0;
  while (dp[k] < n) {
    moves++;
    for (let i = k; i >= 1; i--)
      dp[i] = dp[i] + dp[i - 1] + 1;
  }
  return moves;
};
```
**PHP**
```php
function superEggDrop(int $k, int $n): int {
    $dp = array_fill(0, $k + 1, 0);
    $moves = 0;
    while ($dp[$k] < $n) {
        $moves++;
        for ($i = $k; $i >= 1; $i--)
            $dp[$i] = $dp[$i] + $dp[$i - 1] + 1;
    }
    return $moves;
}
```
**Python**
```python
def super_egg_drop(k, n):
    dp = [0] * (k + 1)
    moves = 0
    while dp[k] < n:
        moves += 1
        for i in range(k, 0, -1):
            dp[i] = dp[i] + dp[i - 1] + 1
    return moves
```

<a id="m446"></a>
### 446. Qurbaqa sakrashi (frog jump)
Toshlar bo'ylab sakrab (oldingi sakrash ±1) oxirgi toshga yetib bo'ladimi.
`⏱ O(n²) · 💾 O(n²)`

**JS**
```js
const canCross = (stones) => {
  const n = stones.length;
  const idx = new Map(stones.map((s, i) => [s, i]));
  const dp = stones.map(() => new Set());
  dp[0].add(0);
  for (let i = 0; i < n; i++)
    for (const k of dp[i])
      for (const step of [k - 1, k, k + 1])
        if (step > 0 && idx.has(stones[i] + step))
          dp[idx.get(stones[i] + step)].add(step);
  return dp[n - 1].size > 0;
};
```
**PHP**
```php
function canCross(array $stones): bool {
    $n = count($stones);
    $idx = array_flip($stones);
    $dp = array_fill(0, $n, []);
    $dp[0][0] = true;
    for ($i = 0; $i < $n; $i++)
        foreach (array_keys($dp[$i]) as $k)
            foreach ([$k - 1, $k, $k + 1] as $step)
                if ($step > 0 && isset($idx[$stones[$i] + $step]))
                    $dp[$idx[$stones[$i] + $step]][$step] = true;
    return count($dp[$n - 1]) > 0;
}
```
**Python**
```python
def can_cross(stones):
    n = len(stones)
    idx = {s: i for i, s in enumerate(stones)}
    dp = [set() for _ in stones]
    dp[0].add(0)
    for i in range(n):
        for k in dp[i]:
            for step in (k - 1, k, k + 1):
                if step > 0 and stones[i] + step in idx:
                    dp[idx[stones[i] + step]].add(step)
    return len(dp[n - 1]) > 0
```

<a id="m447"></a>
### 447. Sakrash o'yini II — minimal sakrashlar (jump game II)
Har katakda maksimal sakrash uzunligi berilgan; oxiriga minimal sakrashda yetish.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const jump = (nums) => {
  let jumps = 0, curEnd = 0, farthest = 0;
  for (let i = 0; i < nums.length - 1; i++) {
    farthest = Math.max(farthest, i + nums[i]);
    if (i === curEnd) { jumps++; curEnd = farthest; }
  }
  return jumps;
};
```
**PHP**
```php
function jump(array $nums): int {
    $jumps = 0; $curEnd = 0; $farthest = 0;
    for ($i = 0; $i < count($nums) - 1; $i++) {
        $farthest = max($farthest, $i + $nums[$i]);
        if ($i === $curEnd) { $jumps++; $curEnd = $farthest; }
    }
    return $jumps;
}
```
**Python**
```python
def jump(nums):
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

<a id="m448"></a>
### 448. Rus matryoshka konvertlari (russian doll envelopes)
Bir-biriga (kengligi va balandligi qat'iy katta) joylashadigan eng ko'p konvertlar.
`⏱ O(n log n) · 💾 O(n)`

**JS**
```js
const maxEnvelopes = (envelopes) => {
  envelopes.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
  const tails = [];
  for (const [, h] of envelopes) {
    let lo = 0, hi = tails.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (tails[mid] < h) lo = mid + 1; else hi = mid;
    }
    tails[lo] = h;
  }
  return tails.length;
};
```
**PHP**
```php
function maxEnvelopes(array $envelopes): int {
    usort($envelopes, fn($a, $b) => $a[0] === $b[0] ? $b[1] - $a[1] : $a[0] - $b[0]);
    $tails = [];
    foreach ($envelopes as [$w, $h]) {
        $lo = 0; $hi = count($tails);
        while ($lo < $hi) {
            $mid = intdiv($lo + $hi, 2);
            if ($tails[$mid] < $h) $lo = $mid + 1; else $hi = $mid;
        }
        $tails[$lo] = $h;
    }
    return count($tails);
}
```
**Python**
```python
import bisect

def max_envelopes(envelopes):
    envelopes.sort(key=lambda e: (e[0], -e[1]))
    tails = []
    for _, h in envelopes:
        i = bisect.bisect_left(tails, h)
        if i == len(tails):
            tails.append(h)
        else:
            tails[i] = h
    return len(tails)
```

<a id="m449"></a>
### 449. Juftliklar zanjirining maksimal uzunligi (maximum length of pair chain)
[a, b] juftliklardan b < c sharti bilan eng uzun zanjir (ochko'z + saralash).
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const findLongestChain = (pairs) => {
  pairs.sort((a, b) => a[1] - b[1]);
  let count = 0, cur = -Infinity;
  for (const [a, b] of pairs)
    if (a > cur) { count++; cur = b; }
  return count;
};
```
**PHP**
```php
function findLongestChain(array $pairs): int {
    usort($pairs, fn($a, $b) => $a[1] - $b[1]);
    $count = 0; $cur = PHP_INT_MIN;
    foreach ($pairs as [$a, $b])
        if ($a > $cur) { $count++; $cur = $b; }
    return $count;
}
```
**Python**
```python
def find_longest_chain(pairs):
    pairs.sort(key=lambda p: p[1])
    count, cur = 0, float("-inf")
    for a, b in pairs:
        if a > cur:
            count += 1
            cur = b
    return count
```

<a id="m450"></a>
### 450. Bog'ni sug'orish uchun minimal jo'mraklar (minimum taps to water garden)
[0, n] bog'ni qamrab oladigan minimal jo'mraklar soni (interval-qamrov DP).
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const minTaps = (n, ranges) => {
  const reach = Array(n + 1).fill(0);
  for (let i = 0; i <= n; i++) {
    const l = Math.max(0, i - ranges[i]);
    reach[l] = Math.max(reach[l], i + ranges[i]);
  }
  let taps = 0, end = 0, farthest = 0;
  for (let i = 0; i < n; i++) {
    farthest = Math.max(farthest, reach[i]);
    if (i === farthest) return -1;
    if (i === end) { taps++; end = farthest; }
  }
  return taps;
};
```
**PHP**
```php
function minTaps(int $n, array $ranges): int {
    $reach = array_fill(0, $n + 1, 0);
    for ($i = 0; $i <= $n; $i++) {
        $l = max(0, $i - $ranges[$i]);
        $reach[$l] = max($reach[$l], $i + $ranges[$i]);
    }
    $taps = 0; $end = 0; $farthest = 0;
    for ($i = 0; $i < $n; $i++) {
        $farthest = max($farthest, $reach[$i]);
        if ($i === $farthest) return -1;
        if ($i === $end) { $taps++; $end = $farthest; }
    }
    return $taps;
}
```
**Python**
```python
def min_taps(n, ranges):
    reach = [0] * (n + 1)
    for i in range(n + 1):
        l = max(0, i - ranges[i])
        reach[l] = max(reach[l], i + ranges[i])
    taps = end = farthest = 0
    for i in range(n):
        farthest = max(farthest, reach[i])
        if i == farthest:
            return -1
        if i == end:
            taps += 1
            end = farthest
    return taps
```

<a id="m451"></a>
### 451. Foydali rejalar (profitable schemes)
n a'zo va kamida minProfit foyda beruvchi guruh tanlovlari soni (mod 1e9+7).
`⏱ O(len × n × minProfit) · 💾 O(n × minProfit)`

**JS**
```js
const profitableSchemes = (n, minProfit, group, profit) => {
  const MOD = 1000000007;
  const dp = Array.from({ length: n + 1 }, () => Array(minProfit + 1).fill(0));
  for (let g = 0; g <= n; g++) dp[g][0] = 1;
  for (let k = 0; k < group.length; k++) {
    const g = group[k], p = profit[k];
    for (let i = n; i >= g; i--)
      for (let j = minProfit; j >= 0; j--) {
        const pj = Math.max(0, j - p);
        dp[i][j] = (dp[i][j] + dp[i - g][pj]) % MOD;
      }
  }
  return dp[n][minProfit];
};
```
**PHP**
```php
function profitableSchemes(int $n, int $minProfit, array $group, array $profit): int {
    $MOD = 1000000007;
    $dp = array_fill(0, $n + 1, array_fill(0, $minProfit + 1, 0));
    for ($g = 0; $g <= $n; $g++) $dp[$g][0] = 1;
    for ($k = 0; $k < count($group); $k++) {
        $g = $group[$k]; $p = $profit[$k];
        for ($i = $n; $i >= $g; $i--)
            for ($j = $minProfit; $j >= 0; $j--) {
                $pj = max(0, $j - $p);
                $dp[$i][$j] = ($dp[$i][$j] + $dp[$i - $g][$pj]) % $MOD;
            }
    }
    return $dp[$n][$minProfit];
}
```
**Python**
```python
def profitable_schemes(n, min_profit, group, profit):
    MOD = 1000000007
    dp = [[0] * (min_profit + 1) for _ in range(n + 1)]
    for g in range(n + 1):
        dp[g][0] = 1
    for gk, pk in zip(group, profit):
        for i in range(n, gk - 1, -1):
            for j in range(min_profit, -1, -1):
                pj = max(0, j - pk)
                dp[i][j] = (dp[i][j] + dp[i - gk][pj]) % MOD
    return dp[n][min_profit]
```

<a id="m452"></a>
### 452. Maksimal yig'indi uchun massivni bo'lish (partition array for maximum sum)
Massivni eng ko'pi bilan k uzunlikdagi bo'laklarga bo'lib (har bo'lak = max × uzunlik) maksimal yig'indi.
`⏱ O(n × k) · 💾 O(n)`

**JS**
```js
const maxSumAfterPartitioning = (arr, k) => {
  const n = arr.length;
  const dp = Array(n + 1).fill(0);
  for (let i = 1; i <= n; i++) {
    let curMax = 0;
    for (let j = 1; j <= k && j <= i; j++) {
      curMax = Math.max(curMax, arr[i - j]);
      dp[i] = Math.max(dp[i], dp[i - j] + curMax * j);
    }
  }
  return dp[n];
};
```
**PHP**
```php
function maxSumAfterPartitioning(array $arr, int $k): int {
    $n = count($arr);
    $dp = array_fill(0, $n + 1, 0);
    for ($i = 1; $i <= $n; $i++) {
        $curMax = 0;
        for ($j = 1; $j <= $k && $j <= $i; $j++) {
            $curMax = max($curMax, $arr[$i - $j]);
            $dp[$i] = max($dp[$i], $dp[$i - $j] + $curMax * $j);
        }
    }
    return $dp[$n];
}
```
**Python**
```python
def max_sum_after_partitioning(arr, k):
    n = len(arr)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        cur_max = 0
        for j in range(1, min(k, i) + 1):
            cur_max = max(cur_max, arr[i - j])
            dp[i] = max(dp[i], dp[i - j] + cur_max * j)
    return dp[n]
```

<a id="m453"></a>
### 453. Javon tokchalarini to'ldirish (filling bookcase shelves)
Kitoblarni tartibni saqlab javonga joylashtirib, javonning minimal umumiy balandligi.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const minHeightShelves = (books, shelfWidth) => {
  const n = books.length;
  const dp = Array(n + 1).fill(Infinity);
  dp[0] = 0;
  for (let i = 1; i <= n; i++) {
    let width = 0, height = 0;
    for (let j = i; j >= 1; j--) {
      width += books[j - 1][0];
      if (width > shelfWidth) break;
      height = Math.max(height, books[j - 1][1]);
      dp[i] = Math.min(dp[i], dp[j - 1] + height);
    }
  }
  return dp[n];
};
```
**PHP**
```php
function minHeightShelves(array $books, int $shelfWidth): int {
    $n = count($books);
    $dp = array_fill(0, $n + 1, PHP_INT_MAX);
    $dp[0] = 0;
    for ($i = 1; $i <= $n; $i++) {
        $width = 0; $height = 0;
        for ($j = $i; $j >= 1; $j--) {
            $width += $books[$j - 1][0];
            if ($width > $shelfWidth) break;
            $height = max($height, $books[$j - 1][1]);
            $dp[$i] = min($dp[$i], $dp[$j - 1] + $height);
        }
    }
    return $dp[$n];
}
```
**Python**
```python
def min_height_shelves(books, shelf_width):
    n = len(books)
    dp = [0] + [float("inf")] * n
    for i in range(1, n + 1):
        width = height = 0
        for j in range(i, 0, -1):
            width += books[j - 1][0]
            if width > shelf_width:
                break
            height = max(height, books[j - 1][1])
            dp[i] = min(dp[i], dp[j - 1] + height)
    return dp[n]
```

<a id="m454"></a>
### 454. Barg qiymatlaridan minimal narxli daraxt (minimum cost tree from leaf values)
Barglardan binar daraxt qurishda ichki tugunlar (chap×o'ng max ko'paytma) yig'indisi minimal.
`⏱ O(n²) · 💾 O(n²)`

**JS**
```js
const mctFromLeafValues = (arr) => {
  const n = arr.length;
  const maxv = Array.from({ length: n }, () => Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    let m = 0;
    for (let j = i; j < n; j++) { m = Math.max(m, arr[j]); maxv[i][j] = m; }
  }
  const dp = Array.from({ length: n }, () => Array(n).fill(0));
  for (let len = 2; len <= n; len++)
    for (let i = 0; i + len - 1 < n; i++) {
      const j = i + len - 1;
      dp[i][j] = Infinity;
      for (let k = i; k < j; k++)
        dp[i][j] = Math.min(dp[i][j],
          dp[i][k] + dp[k + 1][j] + maxv[i][k] * maxv[k + 1][j]);
    }
  return dp[0][n - 1];
};
```
**PHP**
```php
function mctFromLeafValues(array $arr): int {
    $n = count($arr);
    $maxv = array_fill(0, $n, array_fill(0, $n, 0));
    for ($i = 0; $i < $n; $i++) {
        $m = 0;
        for ($j = $i; $j < $n; $j++) { $m = max($m, $arr[$j]); $maxv[$i][$j] = $m; }
    }
    $dp = array_fill(0, $n, array_fill(0, $n, 0));
    for ($len = 2; $len <= $n; $len++)
        for ($i = 0; $i + $len - 1 < $n; $i++) {
            $j = $i + $len - 1;
            $dp[$i][$j] = PHP_INT_MAX;
            for ($k = $i; $k < $j; $k++)
                $dp[$i][$j] = min($dp[$i][$j],
                    $dp[$i][$k] + $dp[$k + 1][$j] + $maxv[$i][$k] * $maxv[$k + 1][$j]);
        }
    return $dp[0][$n - 1];
}
```
**Python**
```python
def mct_from_leaf_values(arr):
    n = len(arr)
    maxv = [[0] * n for _ in range(n)]
    for i in range(n):
        m = 0
        for j in range(i, n):
            m = max(m, arr[j])
            maxv[i][j] = m
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                dp[i][j] = min(dp[i][j],
                               dp[i][k] + dp[k + 1][j] + maxv[i][k] * maxv[k + 1][j])
    return dp[0][n - 1]
```

<a id="m455"></a>
### 455. Eng uzun umumiy qism-satr (longest common substring)
Ikki satrning uzluksiz eng uzun umumiy qism-satri (substring) uzunligi.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const longestCommonSubstr = (a, b) => {
  const m = a.length, n = b.length;
  let dp = Array(n + 1).fill(0), best = 0;
  for (let i = 1; i <= m; i++) {
    const ndp = Array(n + 1).fill(0);
    for (let j = 1; j <= n; j++)
      if (a[i - 1] === b[j - 1]) {
        ndp[j] = dp[j - 1] + 1;
        best = Math.max(best, ndp[j]);
      }
    dp = ndp;
  }
  return best;
};
```
**PHP**
```php
function longestCommonSubstr(string $a, string $b): int {
    $m = strlen($a); $n = strlen($b);
    $dp = array_fill(0, $n + 1, 0); $best = 0;
    for ($i = 1; $i <= $m; $i++) {
        $ndp = array_fill(0, $n + 1, 0);
        for ($j = 1; $j <= $n; $j++)
            if ($a[$i - 1] === $b[$j - 1]) {
                $ndp[$j] = $dp[$j - 1] + 1;
                $best = max($best, $ndp[$j]);
            }
        $dp = $ndp;
    }
    return $best;
}
```
**Python**
```python
def longest_common_substr(a, b):
    m, n = len(a), len(b)
    dp = [0] * (n + 1)
    best = 0
    for i in range(1, m + 1):
        ndp = [0] * (n + 1)
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                ndp[j] = dp[j - 1] + 1
                best = max(best, ndp[j])
        dp = ndp
    return best
```

<a id="m456"></a>
### 456. Kvadrat qism-matritsalar soni (count square submatrices)
0/1 matritsada faqat 1 lardan iborat barcha kvadrat qism-matritsalar soni.
`⏱ O(m × n) · 💾 O(n)`

**JS**
```js
const countSquares = (matrix) => {
  const m = matrix.length, n = matrix[0].length;
  const dp = Array(n + 1).fill(0);
  let total = 0, prev = 0;
  for (let i = 1; i <= m; i++) {
    prev = 0;
    for (let j = 1; j <= n; j++) {
      const tmp = dp[j];
      if (matrix[i - 1][j - 1] === 1) {
        dp[j] = Math.min(dp[j], dp[j - 1], prev) + 1;
        total += dp[j];
      } else dp[j] = 0;
      prev = tmp;
    }
  }
  return total;
};
```
**PHP**
```php
function countSquares(array $matrix): int {
    $m = count($matrix); $n = count($matrix[0]);
    $dp = array_fill(0, $n + 1, 0);
    $total = 0;
    for ($i = 1; $i <= $m; $i++) {
        $prev = 0;
        for ($j = 1; $j <= $n; $j++) {
            $tmp = $dp[$j];
            if ($matrix[$i - 1][$j - 1] === 1) {
                $dp[$j] = min($dp[$j], $dp[$j - 1], $prev) + 1;
                $total += $dp[$j];
            } else $dp[$j] = 0;
            $prev = $tmp;
        }
    }
    return $total;
}
```
**Python**
```python
def count_squares(matrix):
    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    total = 0
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            tmp = dp[j]
            if matrix[i - 1][j - 1] == 1:
                dp[j] = min(dp[j], dp[j - 1], prev) + 1
                total += dp[j]
            else:
                dp[j] = 0
            prev = tmp
    return total
```
