<a id="b38"></a>
# 38-bo'lim: Bit operatsiyalari (ilg'or)

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Bu bo'limda bit darajasidagi amallarning ilg'or qo'llanishlari ko'rib chiqiladi: dinamik
> dasturlash bilan bitlarni sanash, XOR'ning sehrli xossalari (single number turkumi, XOR
> prefiks, kodlangan massivlarni tiklash), Trie yordamida maksimal XOR, bitmask orqali
> kichik to'plamlar va bitmask DP (TSP, taqsimlash masalasi), Gosper's hack bilan k-elementli
> to'plamlarni sanash, hamda Gray kodi bilan ishlash. Bu usullar tezlik va xotira jihatidan
> juda samarali yechimlar beradi.

<a id="m847"></a>
### 847. Bitlarni sanash 0..n (counting bits, DP)
Har bir 0..n soni uchun ikkilik yozuvdagi birlar sonini O(n) da hisoblaydi: `dp[i] = dp[i >> 1] + (i & 1)`.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const countBits = (n) => {
  const dp = Array(n + 1).fill(0);
  for (let i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);
  return dp;
};
```
**PHP**
```php
function countBits(int $n): array {
    $dp = array_fill(0, $n + 1, 0);
    for ($i = 1; $i <= $n; $i++) $dp[$i] = $dp[$i >> 1] + ($i & 1);
    return $dp;
}
```
**Python**
```python
def count_bits(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

<a id="m848"></a>
### 848. Single number II (har biri 3 marta, biri 1 marta)
Massivda bitta sondan tashqari hamma 3 martadan takrorlanadi; har bir bit pozitsiyasidagi birlar sonini 3 ga bo'lib qoldiqni yig'amiz.
`⏱ O(32n) · 💾 O(1)`

**JS**
```js
const singleNumberII = (nums) => {
  let ones = 0, twos = 0;
  for (const x of nums) {
    ones = (ones ^ x) & ~twos;
    twos = (twos ^ x) & ~ones;
  }
  return ones;
};
```
**PHP**
```php
function singleNumberII(array $nums): int {
    $ones = 0; $twos = 0;
    foreach ($nums as $x) {
        $ones = ($ones ^ $x) & ~$twos;
        $twos = ($twos ^ $x) & ~$ones;
    }
    return $ones;
}
```
**Python**
```python
def single_number_ii(nums):
    ones = twos = 0
    for x in nums:
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
    return ones
```

<a id="m849"></a>
### 849. Single number III (ikkita noyob son)
Faqat ikki son bittadan, qolganlari juftlikda. Hammasini XOR qilamiz, eng past farqli bit bo'yicha ikki guruhga ajratamiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const singleNumberIII = (nums) => {
  let xorAll = 0;
  for (const x of nums) xorAll ^= x;
  const low = xorAll & -xorAll;
  let a = 0;
  for (const x of nums) if (x & low) a ^= x;
  return [a, xorAll ^ a];
};
```
**PHP**
```php
function singleNumberIII(array $nums): array {
    $xorAll = 0;
    foreach ($nums as $x) $xorAll ^= $x;
    $low = $xorAll & (-$xorAll);
    $a = 0;
    foreach ($nums as $x) if ($x & $low) $a ^= $x;
    return [$a, $xorAll ^ $a];
}
```
**Python**
```python
def single_number_iii(nums):
    xor_all = 0
    for x in nums:
        xor_all ^= x
    low = xor_all & -xor_all
    a = 0
    for x in nums:
        if x & low:
            a ^= x
    return [a, xor_all ^ a]
```

<a id="m850"></a>
### 850. Oraliqdagi sonlar bitli AND (bitwise AND of numbers range)
[left, right] oralig'idagi barcha sonlarni AND qiladi — bu ularning umumiy prefiksiga teng; tafovutli bitlarni o'ngga surib topamiz.
`⏱ O(log right) · 💾 O(1)`

**JS**
```js
const rangeBitwiseAnd = (left, right) => {
  let shift = 0;
  while (left < right) { left >>= 1; right >>= 1; shift++; }
  return left << shift;
};
```
**PHP**
```php
function rangeBitwiseAnd(int $left, int $right): int {
    $shift = 0;
    while ($left < $right) { $left >>= 1; $right >>= 1; $shift++; }
    return $left << $shift;
}
```
**Python**
```python
def range_bitwise_and(left, right):
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift
```

<a id="m851"></a>
### 851. Ikki sonning maksimal XOR'i (maximum XOR, Trie)
Massivdan ikki sonning eng katta XOR'ini bitli Trie yordamida topadi: har bir son uchun qarama-qarshi bitni ochko'zlik bilan tanlaymiz.
`⏱ O(32n) · 💾 O(32n)`

**JS**
```js
const findMaximumXOR = (nums) => {
  const HIGH = 30;
  const root = {};
  for (const x of nums) {
    let node = root;
    for (let i = HIGH; i >= 0; i--) {
      const b = (x >> i) & 1;
      node = node[b] ??= {};
    }
  }
  let best = 0;
  for (const x of nums) {
    let node = root, cur = 0;
    for (let i = HIGH; i >= 0; i--) {
      const b = (x >> i) & 1;
      if (node[b ^ 1]) { cur |= 1 << i; node = node[b ^ 1]; }
      else node = node[b];
    }
    best = Math.max(best, cur);
  }
  return best;
};
```
**PHP**
```php
function findMaximumXOR(array $nums): int {
    $HIGH = 30;
    $root = [];
    foreach ($nums as $x) {
        $node = &$root;
        for ($i = $HIGH; $i >= 0; $i--) {
            $b = ($x >> $i) & 1;
            if (!isset($node[$b])) $node[$b] = [];
            $node = &$node[$b];
        }
        unset($node);
    }
    $best = 0;
    foreach ($nums as $x) {
        $node = &$root; $cur = 0;
        for ($i = $HIGH; $i >= 0; $i--) {
            $b = ($x >> $i) & 1;
            if (isset($node[$b ^ 1])) { $cur |= 1 << $i; $node = &$node[$b ^ 1]; }
            else $node = &$node[$b];
        }
        unset($node);
        $best = max($best, $cur);
    }
    return $best;
}
```
**Python**
```python
def find_maximum_xor(nums):
    HIGH = 30
    root = {}
    for x in nums:
        node = root
        for i in range(HIGH, -1, -1):
            b = (x >> i) & 1
            node = node.setdefault(b, {})
    best = 0
    for x in nums:
        node, cur = root, 0
        for i in range(HIGH, -1, -1):
            b = (x >> i) & 1
            if (b ^ 1) in node:
                cur |= 1 << i
                node = node[b ^ 1]
            else:
                node = node[b]
        best = max(best, cur)
    return best
```

<a id="m852"></a>
### 852. Barcha kichik to'plamlar (subsets via bitmask)
n elementli massivning 2^n ta kichik to'plamini har bir bitmask 0..2^n-1 ni element tanlovi sifatida talqin qilib hosil qiladi.
`⏱ O(n × 2ⁿ) · 💾 O(n × 2ⁿ)`

**JS**
```js
const subsets = (nums) => {
  const n = nums.length, res = [];
  for (let mask = 0; mask < (1 << n); mask++) {
    const sub = [];
    for (let i = 0; i < n; i++) if (mask & (1 << i)) sub.push(nums[i]);
    res.push(sub);
  }
  return res;
};
```
**PHP**
```php
function subsets(array $nums): array {
    $n = count($nums); $res = [];
    for ($mask = 0; $mask < (1 << $n); $mask++) {
        $sub = [];
        for ($i = 0; $i < $n; $i++) if ($mask & (1 << $i)) $sub[] = $nums[$i];
        $res[] = $sub;
    }
    return $res;
}
```
**Python**
```python
def subsets(nums):
    n = len(nums)
    res = []
    for mask in range(1 << n):
        sub = [nums[i] for i in range(n) if mask & (1 << i)]
        res.append(sub)
    return res
```

<a id="m853"></a>
### 853. Hamming masofasi (Hamming distance)
Ikki sonning nechta bit pozitsiyasida farq qilishini hisoblaydi: XOR qilib, natijadagi birlarni sanaymiz.
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const hammingDistance = (x, y) => {
  let v = x ^ y, count = 0;
  while (v) { v &= v - 1; count++; }
  return count;
};
```
**PHP**
```php
function hammingDistance(int $x, int $y): int {
    $v = $x ^ $y; $count = 0;
    while ($v) { $v &= $v - 1; $count++; }
    return $count;
}
```
**Python**
```python
def hamming_distance(x, y):
    return bin(x ^ y).count("1")
```

<a id="m854"></a>
### 854. Umumiy Hamming masofasi (total Hamming distance)
Barcha juftliklar bo'yicha Hamming masofalari yig'indisi. Har bir bit pozitsiyasi uchun: (birlar soni) × (nollar soni).
`⏱ O(32n) · 💾 O(1)`

**JS**
```js
const totalHammingDistance = (nums) => {
  const n = nums.length;
  let total = 0;
  for (let i = 0; i < 32; i++) {
    let ones = 0;
    for (const x of nums) ones += (x >> i) & 1;
    total += ones * (n - ones);
  }
  return total;
};
```
**PHP**
```php
function totalHammingDistance(array $nums): int {
    $n = count($nums); $total = 0;
    for ($i = 0; $i < 32; $i++) {
        $ones = 0;
        foreach ($nums as $x) $ones += ($x >> $i) & 1;
        $total += $ones * ($n - $ones);
    }
    return $total;
}
```
**Python**
```python
def total_hamming_distance(nums):
    n = len(nums)
    total = 0
    for i in range(32):
        ones = sum((x >> i) & 1 for x in nums)
        total += ones * (n - ones)
    return total
```

<a id="m855"></a>
### 855. Sonning to'ldiruvchisi (number complement)
Sonning ikkilik yozuvidagi har bir bitni teskari qiladi (faqat ahamiyatli bitlar doirasida). Eng yuqori bitgacha bo'lgan maskani XOR qilamiz.
`⏱ O(log num) · 💾 O(1)`

**JS**
```js
const findComplement = (num) => {
  let mask = 1;
  while (mask < num) mask = (mask << 1) | 1;
  return num ^ mask;
};
```
**PHP**
```php
function findComplement(int $num): int {
    $mask = 1;
    while ($mask < $num) $mask = ($mask << 1) | 1;
    return $num ^ $mask;
}
```
**Python**
```python
def find_complement(num):
    mask = 1
    while mask < num:
        mask = (mask << 1) | 1
    return num ^ mask
```

<a id="m856"></a>
### 856. UTF-8 tekshiruvi (UTF-8 validation)
Bayt qiymatlari ro'yxati to'g'ri UTF-8 ketma-ketligi ekanligini tekshiradi: yetakchi bayt nechta davom baytini talab qilishini aniqlaymiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const validUtf8 = (data) => {
  let rest = 0;
  for (const byte of data) {
    const b = byte & 0xff;
    if (rest === 0) {
      if (b >> 5 === 0b110) rest = 1;
      else if (b >> 4 === 0b1110) rest = 2;
      else if (b >> 3 === 0b11110) rest = 3;
      else if (b >> 7 === 1) return false;
    } else {
      if (b >> 6 !== 0b10) return false;
      rest--;
    }
  }
  return rest === 0;
};
```
**PHP**
```php
function validUtf8(array $data): bool {
    $rest = 0;
    foreach ($data as $byte) {
        $b = $byte & 0xff;
        if ($rest === 0) {
            if ($b >> 5 === 0b110) $rest = 1;
            elseif ($b >> 4 === 0b1110) $rest = 2;
            elseif ($b >> 3 === 0b11110) $rest = 3;
            elseif ($b >> 7 === 1) return false;
        } else {
            if ($b >> 6 !== 0b10) return false;
            $rest--;
        }
    }
    return $rest === 0;
}
```
**Python**
```python
def valid_utf8(data):
    rest = 0
    for byte in data:
        b = byte & 0xff
        if rest == 0:
            if b >> 5 == 0b110:
                rest = 1
            elif b >> 4 == 0b1110:
                rest = 2
            elif b >> 3 == 0b11110:
                rest = 3
            elif b >> 7 == 1:
                return False
        else:
            if b >> 6 != 0b10:
                return False
            rest -= 1
    return rest == 0
```

<a id="m857"></a>
### 857. Toq va juft bitlarni almashtirish (swap odd and even bits)
Qo'shni bitlarni juftlab almashtiradi: juft pozitsiyalardagi bitlarni bir chapga, toqlarni bir o'ngga surib OR qilamiz (32-bitli son uchun).
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const swapOddEvenBits = (n) => {
  const even = (n & 0x55555555) << 1;
  const odd = (n & 0xaaaaaaaa) >>> 1;
  return (even | odd) >>> 0;
};
```
**PHP**
```php
function swapOddEvenBits(int $n): int {
    $even = ($n & 0x55555555) << 1;
    $odd = ($n & 0xaaaaaaaa) >> 1;
    return ($even | $odd) & 0xffffffff;
}
```
**Python**
```python
def swap_odd_even_bits(n):
    even = (n & 0x55555555) << 1
    odd = (n & 0xaaaaaaaa) >> 1
    return even | odd
```

<a id="m858"></a>
### 858. Bitlar navbatma-navbatligini tekshirish (alternating bits)
Sonning ikkilik yozuvida bitlar 0 va 1 ketma-ket almashinadimi? `n ^ (n >> 1)` ning hammasi 1 bo'lishini tekshiramiz.
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const hasAlternatingBits = (n) => {
  const x = n ^ (n >> 1);
  return (x & (x + 1)) === 0;
};
```
**PHP**
```php
function hasAlternatingBits(int $n): bool {
    $x = $n ^ ($n >> 1);
    return ($x & ($x + 1)) === 0;
}
```
**Python**
```python
def has_alternating_bits(n):
    x = n ^ (n >> 1)
    return x & (x + 1) == 0
```

<a id="m859"></a>
### 859. Birlarning eng uzun ketma-ketligi (longest run of 1s)
Sonning ikkilik yozuvidagi ketma-ket birlarning eng uzun zanjirini topadi: `n &= n << 1` har bir qadamda zanjirni qisqartiradi.
`⏱ O(k) · 💾 O(1)`

**JS**
```js
const longestRunOfOnes = (n) => {
  let count = 0;
  while (n) { n &= n << 1; count++; }
  return count;
};
```
**PHP**
```php
function longestRunOfOnes(int $n): int {
    $count = 0;
    while ($n) { $n &= $n << 1; $count++; }
    return $count;
}
```
**Python**
```python
def longest_run_of_ones(n):
    count = 0
    while n:
        n &= n << 1
        count += 1
    return count
```

<a id="m860"></a>
### 860. a OR b == c qilish uchun minimal flip (minimum flips)
a va b da nechta bitni o'zgartirsak `a | b == c` bo'ladi? Har bir bit pozitsiyasini ko'rib chiqamiz.
`⏱ O(32) · 💾 O(1)`

**JS**
```js
const minFlips = (a, b, c) => {
  let flips = 0;
  for (let i = 0; i < 32; i++) {
    const ai = (a >> i) & 1, bi = (b >> i) & 1, ci = (c >> i) & 1;
    if (ci === 0) flips += ai + bi;
    else if (ai === 0 && bi === 0) flips += 1;
  }
  return flips;
};
```
**PHP**
```php
function minFlips(int $a, int $b, int $c): int {
    $flips = 0;
    for ($i = 0; $i < 32; $i++) {
        $ai = ($a >> $i) & 1; $bi = ($b >> $i) & 1; $ci = ($c >> $i) & 1;
        if ($ci === 0) $flips += $ai + $bi;
        elseif ($ai === 0 && $bi === 0) $flips += 1;
    }
    return $flips;
}
```
**Python**
```python
def min_flips(a, b, c):
    flips = 0
    for i in range(32):
        ai, bi, ci = (a >> i) & 1, (b >> i) & 1, (c >> i) & 1
        if ci == 0:
            flips += ai + bi
        elif ai == 0 and bi == 0:
            flips += 1
    return flips
```

<a id="m861"></a>
### 861. Qism-massiv XOR so'rovlari (XOR queries, prefix XOR)
Bir nechta [l, r] so'rovi uchun arr[l..r] ning XOR'ini prefiks XOR yordamida O(1) da javob beradi: `pre[r+1] ^ pre[l]`.
`⏱ O(n + q) · 💾 O(n)`

**JS**
```js
const xorQueries = (arr, queries) => {
  const pre = [0];
  for (const x of arr) pre.push(pre[pre.length - 1] ^ x);
  return queries.map(([l, r]) => pre[r + 1] ^ pre[l]);
};
```
**PHP**
```php
function xorQueries(array $arr, array $queries): array {
    $pre = [0];
    foreach ($arr as $x) $pre[] = end($pre) ^ $x;
    $res = [];
    foreach ($queries as [$l, $r]) $res[] = $pre[$r + 1] ^ $pre[$l];
    return $res;
}
```
**Python**
```python
def xor_queries(arr, queries):
    pre = [0]
    for x in arr:
        pre.append(pre[-1] ^ x)
    return [pre[r + 1] ^ pre[l] for l, r in queries]
```

<a id="m862"></a>
### 862. XOR'langan massivni tiklash (decode XORed array)
encoded[i] = arr[i] ^ arr[i+1] va birinchi element berilgan; ketma-ket XOR bilan asl massivni tiklaymiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const decode = (encoded, first) => {
  const arr = [first];
  for (const e of encoded) arr.push(arr[arr.length - 1] ^ e);
  return arr;
};
```
**PHP**
```php
function decode(array $encoded, int $first): array {
    $arr = [$first];
    foreach ($encoded as $e) $arr[] = end($arr) ^ $e;
    return $arr;
}
```
**Python**
```python
def decode(encoded, first):
    arr = [first]
    for e in encoded:
        arr.append(arr[-1] ^ e)
    return arr
```

<a id="m863"></a>
### 863. XOR'langan o'rin almashtirishni tiklash (decode XORed permutation)
encoded[i] = perm[i] ^ perm[i+1], perm — toq n uchun 1..n ning o'rin almashtirishi. Total XOR va toq indeksli XOR orqali perm[0] ni topamiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const decodePermutation = (encoded) => {
  const n = encoded.length + 1;
  let total = 0;
  for (let i = 1; i <= n; i++) total ^= i;
  let odd = 0;
  for (let i = 1; i < n - 1; i += 2) odd ^= encoded[i];
  const perm = [total ^ odd];
  for (const e of encoded) perm.push(perm[perm.length - 1] ^ e);
  return perm;
};
```
**PHP**
```php
function decodePermutation(array $encoded): array {
    $n = count($encoded) + 1;
    $total = 0;
    for ($i = 1; $i <= $n; $i++) $total ^= $i;
    $odd = 0;
    for ($i = 1; $i < $n - 1; $i += 2) $odd ^= $encoded[$i];
    $perm = [$total ^ $odd];
    foreach ($encoded as $e) $perm[] = end($perm) ^ $e;
    return $perm;
}
```
**Python**
```python
def decode_permutation(encoded):
    n = len(encoded) + 1
    total = 0
    for i in range(1, n + 1):
        total ^= i
    odd = 0
    for i in range(1, n - 1, 2):
        odd ^= encoded[i]
    perm = [total ^ odd]
    for e in encoded:
        perm.append(perm[-1] ^ e)
    return perm
```

<a id="m864"></a>
### 864. Ikki sonni qo'shish (sum without +, bitwise)
`+` ishlatmasdan ikki butun sonni qo'shadi: XOR — qoldiqsiz yig'indi, AND << 1 — ko'chirish (carry).
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const getSum = (a, b) => {
  const MASK = 0xffffffff;
  while (b !== 0) {
    const carry = (a & b) << 1;
    a = (a ^ b) & MASK;
    b = carry & MASK;
  }
  return a > 0x7fffffff ? ~(a ^ MASK) : a;
};
```
**PHP**
```php
function getSum(int $a, int $b): int {
    while ($b != 0) {
        $carry = ($a & $b) << 1;
        $a = $a ^ $b;
        $b = $carry;
    }
    return $a;
}
```
**Python**
```python
def get_sum(a, b):
    mask = 0xffffffff
    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    a &= mask
    return a if a <= 0x7fffffff else ~(a ^ mask)
```

<a id="m865"></a>
### 865. Ikki sonni bo'lish (divide two integers, bit shift)
`*`, `/`, `%` ishlatmasdan butun bo'lish: bo'luvchini chap surish bilan ikki barobarlab eng katta bo'lakni ayiramiz.
`⏱ O(log² n) · 💾 O(1)`

**JS**
```js
const divide = (dividend, divisor) => {
  const INT_MAX = 2147483647;
  if (dividend === -2147483648 && divisor === -1) return INT_MAX;
  const neg = (dividend < 0) !== (divisor < 0);
  let a = Math.abs(dividend), b = Math.abs(divisor), res = 0;
  while (a >= b) {
    let temp = b, m = 1;
    while (a >= temp << 1) { temp <<= 1; m <<= 1; }
    a -= temp;
    res += m;
  }
  return neg ? -res : res;
};
```
**PHP**
```php
function divide(int $dividend, int $divisor): int {
    $INT_MAX = 2147483647;
    if ($dividend === -2147483648 && $divisor === -1) return $INT_MAX;
    $neg = ($dividend < 0) !== ($divisor < 0);
    $a = abs($dividend); $b = abs($divisor); $res = 0;
    while ($a >= $b) {
        $temp = $b; $m = 1;
        while ($a >= $temp << 1) { $temp <<= 1; $m <<= 1; }
        $a -= $temp;
        $res += $m;
    }
    return $neg ? -$res : $res;
}
```
**Python**
```python
def divide(dividend, divisor):
    INT_MAX = 2147483647
    if dividend == -2147483648 and divisor == -1:
        return INT_MAX
    neg = (dividend < 0) != (divisor < 0)
    a, b, res = abs(dividend), abs(divisor), 0
    while a >= b:
        temp, m = b, 1
        while a >= temp << 1:
            temp <<= 1
            m <<= 1
        a -= temp
        res += m
    return -res if neg else res
```

<a id="m866"></a>
### 866. Bitmask DP — sayohatchi (TSP, eng qisqa Hamilton yo'li)
n shaharni har birida bir marta bo'lib bosib o'tishning minimal narxi (Held-Karp). `dp[mask][i]` — `mask` to'plamdagi shaharlar bo'ylab i da tugagan eng arzon yo'l.
`⏱ O(2ⁿ × n²) · 💾 O(2ⁿ × n)`

**JS**
```js
const tsp = (dist) => {
  const n = dist.length, FULL = (1 << n) - 1, INF = Infinity;
  const dp = Array.from({ length: 1 << n }, () => Array(n).fill(INF));
  dp[1][0] = 0;
  for (let mask = 1; mask <= FULL; mask++) {
    for (let i = 0; i < n; i++) {
      if (dp[mask][i] === INF || !(mask & (1 << i))) continue;
      for (let j = 0; j < n; j++) {
        if (mask & (1 << j)) continue;
        const nm = mask | (1 << j);
        dp[nm][j] = Math.min(dp[nm][j], dp[mask][i] + dist[i][j]);
      }
    }
  }
  let best = INF;
  for (let i = 1; i < n; i++) best = Math.min(best, dp[FULL][i] + dist[i][0]);
  return best;
};
```
**PHP**
```php
function tsp(array $dist): float {
    $n = count($dist); $FULL = (1 << $n) - 1; $INF = INF;
    $dp = array_fill(0, 1 << $n, array_fill(0, $n, $INF));
    $dp[1][0] = 0;
    for ($mask = 1; $mask <= $FULL; $mask++) {
        for ($i = 0; $i < $n; $i++) {
            if ($dp[$mask][$i] === $INF || !($mask & (1 << $i))) continue;
            for ($j = 0; $j < $n; $j++) {
                if ($mask & (1 << $j)) continue;
                $nm = $mask | (1 << $j);
                $dp[$nm][$j] = min($dp[$nm][$j], $dp[$mask][$i] + $dist[$i][$j]);
            }
        }
    }
    $best = $INF;
    for ($i = 1; $i < $n; $i++) $best = min($best, $dp[$FULL][$i] + $dist[$i][0]);
    return $best;
}
```
**Python**
```python
def tsp(dist):
    n = len(dist)
    full = (1 << n) - 1
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1, full + 1):
        for i in range(n):
            if dp[mask][i] == INF or not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                nm = mask | (1 << j)
                dp[nm][j] = min(dp[nm][j], dp[mask][i] + dist[i][j])
    return min(dp[full][i] + dist[i][0] for i in range(1, n))
```

<a id="m867"></a>
### 867. Bitmask DP — taqsimlash masalasi (assignment problem)
n ishchini n ishga eng kam umumiy narxda biriktirish. `dp[mask]` — `mask` da belgilangan ishlar allaqachon biriktirilgan eng arzon holat.
`⏱ O(2ⁿ × n) · 💾 O(2ⁿ)`

**JS**
```js
const assignment = (cost) => {
  const n = cost.length, INF = Infinity;
  const dp = Array(1 << n).fill(INF);
  dp[0] = 0;
  for (let mask = 0; mask < (1 << n); mask++) {
    if (dp[mask] === INF) continue;
    let worker = 0, m = mask;
    while (m) { worker += m & 1; m >>= 1; }
    for (let job = 0; job < n; job++) {
      if (mask & (1 << job)) continue;
      const nm = mask | (1 << job);
      dp[nm] = Math.min(dp[nm], dp[mask] + cost[worker][job]);
    }
  }
  return dp[(1 << n) - 1];
};
```
**PHP**
```php
function assignment(array $cost): float {
    $n = count($cost); $INF = INF;
    $dp = array_fill(0, 1 << $n, $INF);
    $dp[0] = 0;
    for ($mask = 0; $mask < (1 << $n); $mask++) {
        if ($dp[$mask] === $INF) continue;
        $worker = 0; $m = $mask;
        while ($m) { $worker += $m & 1; $m >>= 1; }
        for ($job = 0; $job < $n; $job++) {
            if ($mask & (1 << $job)) continue;
            $nm = $mask | (1 << $job);
            $dp[$nm] = min($dp[$nm], $dp[$mask] + $cost[$worker][$job]);
        }
    }
    return $dp[(1 << $n) - 1];
}
```
**Python**
```python
def assignment(cost):
    n = len(cost)
    INF = float("inf")
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        worker = bin(mask).count("1")
        for job in range(n):
            if mask & (1 << job):
                continue
            nm = mask | (1 << job)
            dp[nm] = min(dp[nm], dp[mask] + cost[worker][job])
    return dp[(1 << n) - 1]
```

<a id="m868"></a>
### 868. Gosper's hack (k-elementli kichik to'plamlarni sanash)
n elementdan k tasini tanlovchi barcha bitmasklarni o'sish tartibida hosil qiladi — Gosper's hack keyingi maskani O(1) da topadi.
`⏱ O(C(n,k)) · 💾 O(1)`

**JS**
```js
const gosperSubsets = (n, k) => {
  const res = [];
  if (k === 0) return [0];
  let cur = (1 << k) - 1;
  const limit = 1 << n;
  while (cur < limit) {
    res.push(cur);
    const c = cur & -cur;
    const r = cur + c;
    cur = (((r ^ cur) >> 2) / c | 0) | r;
  }
  return res;
};
```
**PHP**
```php
function gosperSubsets(int $n, int $k): array {
    if ($k === 0) return [0];
    $res = [];
    $cur = (1 << $k) - 1;
    $limit = 1 << $n;
    while ($cur < $limit) {
        $res[] = $cur;
        $c = $cur & (-$cur);
        $r = $cur + $c;
        $cur = (intdiv(($r ^ $cur) >> 2, $c)) | $r;
    }
    return $res;
}
```
**Python**
```python
def gosper_subsets(n, k):
    if k == 0:
        return [0]
    res = []
    cur = (1 << k) - 1
    limit = 1 << n
    while cur < limit:
        res.append(cur)
        c = cur & -cur
        r = cur + c
        cur = (((r ^ cur) >> 2) // c) | r
    return res
```

<a id="m869"></a>
### 869. Juft/toq sonli bitli sonlar (even/odd set bits)
1..n oralig'idagi sonlarni set-bitlari soni juft yoki toqligiga ko'ra ikki ro'yxatga ajratadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const partitionByParity = (n) => {
  const even = [], odd = [];
  for (let x = 1; x <= n; x++) {
    let v = x, count = 0;
    while (v) { v &= v - 1; count++; }
    (count % 2 === 0 ? even : odd).push(x);
  }
  return { even, odd };
};
```
**PHP**
```php
function partitionByParity(int $n): array {
    $even = []; $odd = [];
    for ($x = 1; $x <= $n; $x++) {
        $v = $x; $count = 0;
        while ($v) { $v &= $v - 1; $count++; }
        if ($count % 2 === 0) $even[] = $x; else $odd[] = $x;
    }
    return ['even' => $even, 'odd' => $odd];
}
```
**Python**
```python
def partition_by_parity(n):
    even, odd = [], []
    for x in range(1, n + 1):
        count = bin(x).count("1")
        (even if count % 2 == 0 else odd).append(x)
    return {"even": even, "odd": odd}
```

<a id="m870"></a>
### 870. Gray kodi <-> ikkilik o'tkazish (gray code conversion)
Ikkilik sonni Gray kodiga (`g = n ^ (n >> 1)`) va Gray kodini ikkilikka (ketma-ket XOR) o'tkazadi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const toGray = (n) => n ^ (n >> 1);
const fromGray = (g) => {
  let n = 0;
  for (; g; g >>= 1) n ^= g;
  return n;
};
```
**PHP**
```php
function toGray(int $n): int {
    return $n ^ ($n >> 1);
}
function fromGray(int $g): int {
    $n = 0;
    for (; $g; $g >>= 1) $n ^= $g;
    return $n;
}
```
**Python**
```python
def to_gray(n):
    return n ^ (n >> 1)

def from_gray(g):
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n
```
