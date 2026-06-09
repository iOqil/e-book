<a id="b40"></a>
# 40-bo'lim: Klassik intervyu masalalari

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Bu bo'lim ish suhbatlarida eng ko'p uchraydigan massiv, stek va bog'langan ro'yxat
> (linked list) klassiklarini jamlaydi. Ko'pchiligi LeetCode'ning mashhur "easy/medium"
> masalalari: takrorlarni topish, yo'qolgan sonlar, ko'pchilik elementi (Boyer-Moore),
> joyida ishlash (in-place), ikki ko'rsatkich (two pointer) va bog'langan ro'yxat
> manipulyatsiyalari. Linked list masalalarida tugun (Node) klassi qisqa ko'rsatiladi:
> har bir tugun `val` qiymatini va keyingi tugunga `next` ishorani saqlaydi.

<a id="m931"></a>
### 931. Takror bor-yo'qligi (contains duplicate)
Massivda kamida bitta element takrorlansa `true`, aks holda `false`.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const containsDuplicate = (nums) => new Set(nums).size !== nums.length;
// containsDuplicate([1,2,3,1]) // true
```
**PHP**
```php
function containsDuplicate(array $nums): bool {
    return count(array_unique($nums)) !== count($nums);
}
```
**Python**
```python
def contains_duplicate(nums):
    return len(set(nums)) != len(nums)
```

<a id="m932"></a>
### 932. Takror bor-yo'qligi II (contains duplicate II)
`nums[i] == nums[j]` va `|i - j| <= k` bo'ladigan juftlik bormi.
`⏱ O(n) · 💾 O(min(n, k))`

**JS**
```js
const containsNearbyDuplicate = (nums, k) => {
  const seen = new Map();
  for (let i = 0; i < nums.length; i++) {
    if (seen.has(nums[i]) && i - seen.get(nums[i]) <= k) return true;
    seen.set(nums[i], i);
  }
  return false;
};
// containsNearbyDuplicate([1,2,3,1], 3) // true
```
**PHP**
```php
function containsNearbyDuplicate(array $nums, int $k): bool {
    $seen = [];
    foreach ($nums as $i => $v) {
        if (isset($seen[$v]) && $i - $seen[$v] <= $k) return true;
        $seen[$v] = $i;
    }
    return false;
}
```
**Python**
```python
def contains_nearby_duplicate(nums, k):
    seen = {}
    for i, v in enumerate(nums):
        if v in seen and i - seen[v] <= k:
            return True
        seen[v] = i
    return False
```

<a id="m933"></a>
### 933. Eng katta ko'paytmali qism-massiv (maximum product subarray)
Uzluksiz qism-massivning eng katta ko'paytmasi; manfiylar sababli min va maxni birga kuzatamiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const maxProduct = (nums) => {
  let max = nums[0], min = nums[0], res = nums[0];
  for (let i = 1; i < nums.length; i++) {
    const n = nums[i];
    if (n < 0) [max, min] = [min, max];
    max = Math.max(n, max * n);
    min = Math.min(n, min * n);
    res = Math.max(res, max);
  }
  return res;
};
// maxProduct([2,3,-2,4]) // 6
```
**PHP**
```php
function maxProduct(array $nums): int {
    $max = $min = $res = $nums[0];
    for ($i = 1; $i < count($nums); $i++) {
        $n = $nums[$i];
        if ($n < 0) { $t = $max; $max = $min; $min = $t; }
        $max = max($n, $max * $n);
        $min = min($n, $min * $n);
        $res = max($res, $max);
    }
    return $res;
}
```
**Python**
```python
def max_product(nums):
    cur_max = cur_min = res = nums[0]
    for n in nums[1:]:
        if n < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(n, cur_max * n)
        cur_min = min(n, cur_min * n)
        res = max(res, cur_max)
    return res
```

<a id="m934"></a>
### 934. Massivdagi barcha takrorlarni topish (find all duplicates)
`1..n` oralig'idagi sonlar; har biri 1 yoki 2 marta. Ikki marta uchraganlarni joyida belgilash bilan topamiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const findDuplicates = (nums) => {
  const res = [];
  for (const x of nums) {
    const i = Math.abs(x) - 1;
    if (nums[i] < 0) res.push(i + 1);
    else nums[i] = -nums[i];
  }
  return res;
};
// findDuplicates([4,3,2,7,8,2,3,1]) // [2,3]
```
**PHP**
```php
function findDuplicates(array $nums): array {
    $res = [];
    foreach ($nums as $x) {
        $i = abs($x) - 1;
        if ($nums[$i] < 0) $res[] = $i + 1;
        else $nums[$i] = -$nums[$i];
    }
    return $res;
}
```
**Python**
```python
def find_duplicates(nums):
    res = []
    for x in nums:
        i = abs(x) - 1
        if nums[i] < 0:
            res.append(i + 1)
        else:
            nums[i] = -nums[i]
    return res
```

<a id="m935"></a>
### 935. Yo'qolgan sonlarni topish (find all disappeared numbers)
`1..n` oralig'idan massivda uchramaydigan sonlarni joyida belgilash bilan aniqlaymiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const findDisappeared = (nums) => {
  for (const x of nums) {
    const i = Math.abs(x) - 1;
    if (nums[i] > 0) nums[i] = -nums[i];
  }
  const res = [];
  for (let i = 0; i < nums.length; i++)
    if (nums[i] > 0) res.push(i + 1);
  return res;
};
// findDisappeared([4,3,2,7,8,2,3,1]) // [5,6]
```
**PHP**
```php
function findDisappeared(array $nums): array {
    foreach ($nums as $x) {
        $i = abs($x) - 1;
        if ($nums[$i] > 0) $nums[$i] = -$nums[$i];
    }
    $res = [];
    foreach ($nums as $i => $v)
        if ($v > 0) $res[] = $i + 1;
    return $res;
}
```
**Python**
```python
def find_disappeared(nums):
    for x in nums:
        i = abs(x) - 1
        if nums[i] > 0:
            nums[i] = -nums[i]
    return [i + 1 for i, v in enumerate(nums) if v > 0]
```

<a id="m936"></a>
### 936. Birinchi yo'qolgan musbat son (first missing positive)
Saralanmagan massivda uchramaydigan eng kichik musbat son; joyida o'z o'rniga qo'yish (cyclic sort).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const firstMissingPositive = (nums) => {
  const n = nums.length;
  for (let i = 0; i < n; i++) {
    while (nums[i] > 0 && nums[i] <= n && nums[nums[i] - 1] !== nums[i]) {
      const j = nums[i] - 1;
      [nums[i], nums[j]] = [nums[j], nums[i]];
    }
  }
  for (let i = 0; i < n; i++) if (nums[i] !== i + 1) return i + 1;
  return n + 1;
};
// firstMissingPositive([3,4,-1,1]) // 2
```
**PHP**
```php
function firstMissingPositive(array $nums): int {
    $n = count($nums);
    for ($i = 0; $i < $n; $i++) {
        while ($nums[$i] > 0 && $nums[$i] <= $n && $nums[$nums[$i] - 1] !== $nums[$i]) {
            $j = $nums[$i] - 1;
            $t = $nums[$i]; $nums[$i] = $nums[$j]; $nums[$j] = $t;
        }
    }
    for ($i = 0; $i < $n; $i++) if ($nums[$i] !== $i + 1) return $i + 1;
    return $n + 1;
}
```
**Python**
```python
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        while 0 < nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1
```

<a id="m937"></a>
### 937. Mos kelmaslik to'plami (set mismatch)
`1..n` to'plamida bitta son ikkilanib, bittasi yo'qolgan; takrorlangan va yo'qolgan sonni qaytar.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const findErrorNums = (nums) => {
  let dup = -1;
  for (const x of nums) {
    const i = Math.abs(x) - 1;
    if (nums[i] < 0) dup = i + 1;
    else nums[i] = -nums[i];
  }
  let missing = -1;
  for (let i = 0; i < nums.length; i++) if (nums[i] > 0) missing = i + 1;
  return [dup, missing];
};
// findErrorNums([1,2,2,4]) // [2,3]
```
**PHP**
```php
function findErrorNums(array $nums): array {
    $dup = -1;
    foreach ($nums as $x) {
        $i = abs($x) - 1;
        if ($nums[$i] < 0) $dup = $i + 1;
        else $nums[$i] = -$nums[$i];
    }
    $missing = -1;
    foreach ($nums as $i => $v) if ($v > 0) $missing = $i + 1;
    return [$dup, $missing];
}
```
**Python**
```python
def find_error_nums(nums):
    dup = -1
    for x in nums:
        i = abs(x) - 1
        if nums[i] < 0:
            dup = i + 1
        else:
            nums[i] = -nums[i]
    missing = next(i + 1 for i, v in enumerate(nums) if v > 0)
    return [dup, missing]
```

<a id="m938"></a>
### 938. Ko'pchilik elementi (majority element, Boyer-Moore)
Yarmidan ko'p uchraydigan element; Boyer-Moore ovoz berish algoritmi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const majorityElement = (nums) => {
  let count = 0, candidate = null;
  for (const n of nums) {
    if (count === 0) candidate = n;
    count += n === candidate ? 1 : -1;
  }
  return candidate;
};
// majorityElement([2,2,1,1,1,2,2]) // 2
```
**PHP**
```php
function majorityElement(array $nums): int {
    $count = 0; $candidate = null;
    foreach ($nums as $n) {
        if ($count === 0) $candidate = $n;
        $count += ($n === $candidate) ? 1 : -1;
    }
    return $candidate;
}
```
**Python**
```python
def majority_element(nums):
    count = 0
    candidate = None
    for n in nums:
        if count == 0:
            candidate = n
        count += 1 if n == candidate else -1
    return candidate
```

<a id="m939"></a>
### 939. Ko'pchilik elementi II (majority element II, n/3)
`n/3` martadan ko'p uchraydigan elementlar (ko'pi bilan 2 ta); kengaytirilgan Boyer-Moore.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const majorityElementII = (nums) => {
  let c1 = null, c2 = null, n1 = 0, n2 = 0;
  for (const n of nums) {
    if (n === c1) n1++;
    else if (n === c2) n2++;
    else if (n1 === 0) { c1 = n; n1 = 1; }
    else if (n2 === 0) { c2 = n; n2 = 1; }
    else { n1--; n2--; }
  }
  return [c1, c2].filter(c => nums.filter(x => x === c).length > nums.length / 3);
};
// majorityElementII([3,2,3]) // [3]
```
**PHP**
```php
function majorityElementII(array $nums): array {
    $c1 = $c2 = null; $n1 = $n2 = 0;
    foreach ($nums as $n) {
        if ($n === $c1) $n1++;
        elseif ($n === $c2) $n2++;
        elseif ($n1 === 0) { $c1 = $n; $n1 = 1; }
        elseif ($n2 === 0) { $c2 = $n; $n2 = 1; }
        else { $n1--; $n2--; }
    }
    $res = [];
    foreach ([$c1, $c2] as $c) {
        if ($c !== null && count(array_filter($nums, fn($x) => $x === $c)) > count($nums) / 3)
            $res[] = $c;
    }
    return $res;
}
```
**Python**
```python
def majority_element_ii(nums):
    c1 = c2 = None
    n1 = n2 = 0
    for n in nums:
        if n == c1:
            n1 += 1
        elif n == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = n, 1
        elif n2 == 0:
            c2, n2 = n, 1
        else:
            n1 -= 1
            n2 -= 1
    return [c for c in (c1, c2) if c is not None and nums.count(c) > len(nums) // 3]
```

<a id="m940"></a>
### 940. Nollarni ohirga surish (move zeroes)
Barcha nollarni massiv oxiriga sur, nolmaslar tartibini saqlagan holda, joyida.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const moveZeroes = (nums) => {
  let j = 0;
  for (let i = 0; i < nums.length; i++)
    if (nums[i] !== 0) [nums[j++], nums[i]] = [nums[i], nums[j]];
  return nums;
};
// moveZeroes([0,1,0,3,12]) // [1,3,12,0,0]
```
**PHP**
```php
function moveZeroes(array $nums): array {
    $j = 0;
    for ($i = 0; $i < count($nums); $i++) {
        if ($nums[$i] !== 0) {
            $t = $nums[$j]; $nums[$j] = $nums[$i]; $nums[$i] = $t;
            $j++;
        }
    }
    return $nums;
}
```
**Python**
```python
def move_zeroes(nums):
    j = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[j], nums[i] = nums[i], nums[j]
            j += 1
    return nums
```

<a id="m941"></a>
### 941. Birga oshirish (plus one)
Raqamlar massivi bilan ifodalangan songa 1 qo'sh; ko'tarilishni (carry) hisobga ol.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const plusOne = (digits) => {
  for (let i = digits.length - 1; i >= 0; i--) {
    if (digits[i] < 9) { digits[i]++; return digits; }
    digits[i] = 0;
  }
  return [1, ...digits];
};
// plusOne([1,2,9]) // [1,3,0]
```
**PHP**
```php
function plusOne(array $digits): array {
    for ($i = count($digits) - 1; $i >= 0; $i--) {
        if ($digits[$i] < 9) { $digits[$i]++; return $digits; }
        $digits[$i] = 0;
    }
    return array_merge([1], $digits);
}
```
**Python**
```python
def plus_one(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits
```

<a id="m942"></a>
### 942. Paskal uchburchagi (Pascal's triangle)
Birinchi `numRows` qatorni qur; har element ustidagi ikki sonning yig'indisi.
`⏱ O(n²) · 💾 O(n²)`

**JS**
```js
const generate = (numRows) => {
  const tri = [];
  for (let r = 0; r < numRows; r++) {
    const row = Array(r + 1).fill(1);
    for (let c = 1; c < r; c++) row[c] = tri[r - 1][c - 1] + tri[r - 1][c];
    tri.push(row);
  }
  return tri;
};
// generate(4) // [[1],[1,1],[1,2,1],[1,3,3,1]]
```
**PHP**
```php
function generate(int $numRows): array {
    $tri = [];
    for ($r = 0; $r < $numRows; $r++) {
        $row = array_fill(0, $r + 1, 1);
        for ($c = 1; $c < $r; $c++) $row[$c] = $tri[$r - 1][$c - 1] + $tri[$r - 1][$c];
        $tri[] = $row;
    }
    return $tri;
}
```
**Python**
```python
def generate(num_rows):
    tri = []
    for r in range(num_rows):
        row = [1] * (r + 1)
        for c in range(1, r):
            row[c] = tri[r - 1][c - 1] + tri[r - 1][c]
        tri.append(row)
    return tri
```

<a id="m943"></a>
### 943. Paskal uchburchagi II (Pascal's triangle II)
Faqat `n`-qatorni O(n) qo'shimcha xotira bilan qaytar; qatorni o'ngdan chapga yangilaymiz.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const getRow = (rowIndex) => {
  const row = Array(rowIndex + 1).fill(1);
  for (let r = 1; r <= rowIndex; r++)
    for (let c = r - 1; c > 0; c--) row[c] += row[c - 1];
  return row;
};
// getRow(3) // [1,3,3,1]
```
**PHP**
```php
function getRow(int $rowIndex): array {
    $row = array_fill(0, $rowIndex + 1, 1);
    for ($r = 1; $r <= $rowIndex; $r++)
        for ($c = $r - 1; $c > 0; $c--) $row[$c] += $row[$c - 1];
    return $row;
}
```
**Python**
```python
def get_row(row_index):
    row = [1] * (row_index + 1)
    for r in range(1, row_index + 1):
        for c in range(r - 1, 0, -1):
            row[c] += row[c - 1]
    return row
```

<a id="m944"></a>
### 944. Eng katta tafovut (maximum gap)
Saralangan ketma-ketlikdagi qo'shni sonlar orasidagi eng katta farq; chiqindi (bucket) usuli, saralashsiz O(n).
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const maximumGap = (nums) => {
  const n = nums.length;
  if (n < 2) return 0;
  const lo = Math.min(...nums), hi = Math.max(...nums);
  if (lo === hi) return 0;
  const size = Math.max(1, Math.floor((hi - lo) / (n - 1)));
  const count = Math.floor((hi - lo) / size) + 1;
  const mins = Array(count).fill(Infinity), maxs = Array(count).fill(-Infinity);
  for (const x of nums) {
    const b = Math.floor((x - lo) / size);
    mins[b] = Math.min(mins[b], x);
    maxs[b] = Math.max(maxs[b], x);
  }
  let gap = 0, prev = lo;
  for (let i = 0; i < count; i++) {
    if (mins[i] === Infinity) continue;
    gap = Math.max(gap, mins[i] - prev);
    prev = maxs[i];
  }
  return gap;
};
// maximumGap([3,6,9,1]) // 3
```
**PHP**
```php
function maximumGap(array $nums): int {
    $n = count($nums);
    if ($n < 2) return 0;
    $lo = min($nums); $hi = max($nums);
    if ($lo === $hi) return 0;
    $size = max(1, intdiv($hi - $lo, $n - 1));
    $count = intdiv($hi - $lo, $size) + 1;
    $mins = array_fill(0, $count, PHP_INT_MAX);
    $maxs = array_fill(0, $count, PHP_INT_MIN);
    foreach ($nums as $x) {
        $b = intdiv($x - $lo, $size);
        $mins[$b] = min($mins[$b], $x);
        $maxs[$b] = max($maxs[$b], $x);
    }
    $gap = 0; $prev = $lo;
    for ($i = 0; $i < $count; $i++) {
        if ($mins[$i] === PHP_INT_MAX) continue;
        $gap = max($gap, $mins[$i] - $prev);
        $prev = $maxs[$i];
    }
    return $gap;
}
```
**Python**
```python
def maximum_gap(nums):
    n = len(nums)
    if n < 2:
        return 0
    lo, hi = min(nums), max(nums)
    if lo == hi:
        return 0
    size = max(1, (hi - lo) // (n - 1))
    count = (hi - lo) // size + 1
    mins = [float("inf")] * count
    maxs = [float("-inf")] * count
    for x in nums:
        b = (x - lo) // size
        mins[b] = min(mins[b], x)
        maxs[b] = max(maxs[b], x)
    gap, prev = 0, lo
    for i in range(count):
        if mins[i] == float("inf"):
            continue
        gap = max(gap, mins[i] - prev)
        prev = maxs[i]
    return gap
```

<a id="m945"></a>
### 945. Oraliqlar xulosasi (summary ranges)
Saralangan massivni uzluksiz oraliqlarga ("a->b" yoki "a") jamla.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const summaryRanges = (nums) => {
  const res = [];
  for (let i = 0; i < nums.length; i++) {
    const start = nums[i];
    while (i + 1 < nums.length && nums[i + 1] === nums[i] + 1) i++;
    res.push(start === nums[i] ? `${start}` : `${start}->${nums[i]}`);
  }
  return res;
};
// summaryRanges([0,1,2,4,5,7]) // ["0->2","4->5","7"]
```
**PHP**
```php
function summaryRanges(array $nums): array {
    $res = [];
    for ($i = 0; $i < count($nums); $i++) {
        $start = $nums[$i];
        while ($i + 1 < count($nums) && $nums[$i + 1] === $nums[$i] + 1) $i++;
        $res[] = ($start === $nums[$i]) ? "$start" : "$start->{$nums[$i]}";
    }
    return $res;
}
```
**Python**
```python
def summary_ranges(nums):
    res = []
    i = 0
    while i < len(nums):
        start = nums[i]
        while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
            i += 1
        res.append(str(start) if start == nums[i] else f"{start}->{nums[i]}")
        i += 1
    return res
```

<a id="m946"></a>
### 946. Ikki massiv kesishmasi (intersection of two arrays)
Ikki massivda ham uchraydigan noyob elementlar to'plami.
`⏱ O(n + m) · 💾 O(n)`

**JS**
```js
const intersection = (a, b) => {
  const setB = new Set(b);
  return [...new Set(a)].filter(x => setB.has(x));
};
// intersection([1,2,2,1], [2,2]) // [2]
```
**PHP**
```php
function intersection(array $a, array $b): array {
    return array_values(array_unique(array_intersect($a, $b)));
}
```
**Python**
```python
def intersection(a, b):
    return list(set(a) & set(b))
```

<a id="m947"></a>
### 947. Ikki massiv kesishmasi II (intersection of two arrays II)
Takrorlarni ham hisobga olib kesishmani topish (min chastotagacha).
`⏱ O(n + m) · 💾 O(n)`

**JS**
```js
const intersect = (a, b) => {
  const count = new Map();
  for (const x of a) count.set(x, (count.get(x) || 0) + 1);
  const res = [];
  for (const x of b) {
    if (count.get(x) > 0) { res.push(x); count.set(x, count.get(x) - 1); }
  }
  return res;
};
// intersect([1,2,2,1], [2,2]) // [2,2]
```
**PHP**
```php
function intersect(array $a, array $b): array {
    $count = array_count_values($a);
    $res = [];
    foreach ($b as $x) {
        if (($count[$x] ?? 0) > 0) { $res[] = $x; $count[$x]--; }
    }
    return $res;
}
```
**Python**
```python
from collections import Counter

def intersect(a, b):
    count = Counter(a)
    res = []
    for x in b:
        if count[x] > 0:
            res.append(x)
            count[x] -= 1
    return res
```

<a id="m948"></a>
### 948. Saralangan massivlarni birlashtirish (merge sorted array)
`nums1` (oxirida bo'sh joy bor) ichiga `nums2` ni joyida, orqadan boshlab birlashtir.
`⏱ O(m + n) · 💾 O(1)`

**JS**
```js
const merge = (nums1, m, nums2, n) => {
  let i = m - 1, j = n - 1, k = m + n - 1;
  while (j >= 0) {
    if (i >= 0 && nums1[i] > nums2[j]) nums1[k--] = nums1[i--];
    else nums1[k--] = nums2[j--];
  }
  return nums1;
};
// merge([1,2,3,0,0,0], 3, [2,5,6], 3) // [1,2,2,3,5,6]
```
**PHP**
```php
function merge(array &$nums1, int $m, array $nums2, int $n): void {
    $i = $m - 1; $j = $n - 1; $k = $m + $n - 1;
    while ($j >= 0) {
        if ($i >= 0 && $nums1[$i] > $nums2[$j]) $nums1[$k--] = $nums1[$i--];
        else $nums1[$k--] = $nums2[$j--];
    }
}
```
**Python**
```python
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    return nums1
```

<a id="m949"></a>
### 949. To'liq kvadrat tekshiruvi (valid perfect square)
`sqrt` ishlatmasdan sonning to'liq kvadrat ekanligini binary search bilan tekshir.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const isPerfectSquare = (num) => {
  let lo = 1, hi = num;
  while (lo <= hi) {
    const mid = Math.floor((lo + hi) / 2);
    const sq = mid * mid;
    if (sq === num) return true;
    if (sq < num) lo = mid + 1;
    else hi = mid - 1;
  }
  return false;
};
// isPerfectSquare(16) // true
```
**PHP**
```php
function isPerfectSquare(int $num): bool {
    $lo = 1; $hi = $num;
    while ($lo <= $hi) {
        $mid = intdiv($lo + $hi, 2);
        $sq = $mid * $mid;
        if ($sq === $num) return true;
        if ($sq < $num) $lo = $mid + 1;
        else $hi = $mid - 1;
    }
    return false;
}
```
**Python**
```python
def is_perfect_square(num):
    lo, hi = 1, num
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

<a id="m950"></a>
### 950. Raqamlar yig'indisi (add digits, digital root)
Bir xonali songa qolguncha raqamlarni qo'sh; matematik formula bilan O(1).
`⏱ O(1) · 💾 O(1)`

**JS**
```js
const addDigits = (num) => (num === 0 ? 0 : 1 + (num - 1) % 9);
// addDigits(38) // 2
```
**PHP**
```php
function addDigits(int $num): int {
    return $num === 0 ? 0 : 1 + ($num - 1) % 9;
}
```
**Python**
```python
def add_digits(num):
    return 0 if num == 0 else 1 + (num - 1) % 9
```

<a id="m951"></a>
### 951. Palindrom bog'langan ro'yxat (palindrome linked list)
Ro'yxat palindrom ekanligini ikkinchi yarmini ag'darib O(1) xotira bilan tekshir.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const isPalindrome = (head) => {
  let slow = head, fast = head;
  while (fast && fast.next) { slow = slow.next; fast = fast.next.next; }
  let prev = null;
  while (slow) { [slow.next, prev, slow] = [prev, slow, slow.next]; }
  let a = head, b = prev;
  while (b) { if (a.val !== b.val) return false; a = a.next; b = b.next; }
  return true;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function isPalindrome(?Node $head): bool {
    $slow = $head; $fast = $head;
    while ($fast !== null && $fast->next !== null) { $slow = $slow->next; $fast = $fast->next->next; }
    $prev = null;
    while ($slow !== null) { $nx = $slow->next; $slow->next = $prev; $prev = $slow; $slow = $nx; }
    $a = $head; $b = $prev;
    while ($b !== null) { if ($a->val !== $b->val) return false; $a = $a->next; $b = $b->next; }
    return true;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def is_palindrome(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    prev = None
    while slow:
        slow.next, prev, slow = prev, slow, slow.next
    a, b = head, prev
    while b:
        if a.val != b.val:
            return False
        a, b = a.next, b.next
    return True
```

<a id="m952"></a>
### 952. Ikki ro'yxat kesishmasi (intersection of two linked lists)
Ikki bog'langan ro'yxat birlashadigan tugunni ikki ko'rsatkichni almashtirib top.
`⏱ O(n + m) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const getIntersectionNode = (headA, headB) => {
  let a = headA, b = headB;
  while (a !== b) {
    a = a ? a.next : headB;
    b = b ? b.next : headA;
  }
  return a;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function getIntersectionNode(?Node $headA, ?Node $headB): ?Node {
    $a = $headA; $b = $headB;
    while ($a !== $b) {
        $a = $a !== null ? $a->next : $headB;
        $b = $b !== null ? $b->next : $headA;
    }
    return $a;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def get_intersection_node(head_a, head_b):
    a, b = head_a, head_b
    while a is not b:
        a = a.next if a else head_b
        b = b.next if b else head_a
    return a
```

<a id="m953"></a>
### 953. Ro'yxat elementlarini o'chirish (remove linked list elements)
Berilgan `val` qiymatga teng barcha tugunlarni o'chir; sentinel (qo'riqchi) tugun bilan oson.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const removeElements = (head, val) => {
  const dummy = new Node(0, head);
  let cur = dummy;
  while (cur.next) {
    if (cur.next.val === val) cur.next = cur.next.next;
    else cur = cur.next;
  }
  return dummy.next;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function removeElements(?Node $head, mixed $val): ?Node {
    $dummy = new Node(0, $head);
    $cur = $dummy;
    while ($cur->next !== null) {
        if ($cur->next->val === $val) $cur->next = $cur->next->next;
        else $cur = $cur->next;
    }
    return $dummy->next;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def remove_elements(head, val):
    dummy = Node(0, head)
    cur = dummy
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return dummy.next
```

<a id="m954"></a>
### 954. Toq-juft bog'langan ro'yxat (odd-even linked list)
Toq indeksli tugunlarni oldinga, juftlarni keyinga guruhla, nisbiy tartibni saqlab.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const oddEvenList = (head) => {
  if (!head) return head;
  let odd = head, even = head.next, evenHead = even;
  while (even && even.next) {
    odd.next = even.next; odd = odd.next;
    even.next = odd.next; even = even.next;
  }
  odd.next = evenHead;
  return head;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function oddEvenList(?Node $head): ?Node {
    if ($head === null) return $head;
    $odd = $head; $even = $head->next; $evenHead = $even;
    while ($even !== null && $even->next !== null) {
        $odd->next = $even->next; $odd = $odd->next;
        $even->next = $odd->next; $even = $even->next;
    }
    $odd->next = $evenHead;
    return $head;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def odd_even_list(head):
    if not head:
        return head
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head
```

<a id="m955"></a>
### 955. Ikki sonni qo'shish (add two numbers, linked list)
Raqamlar teskari tartibda saqlangan ikki sonni qo'shib, natijani yangi ro'yxatda qaytar.
`⏱ O(max(n, m)) · 💾 O(max(n, m))`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const addTwoNumbers = (l1, l2) => {
  const dummy = new Node(0);
  let cur = dummy, carry = 0;
  while (l1 || l2 || carry) {
    const sum = (l1 ? l1.val : 0) + (l2 ? l2.val : 0) + carry;
    carry = Math.floor(sum / 10);
    cur.next = new Node(sum % 10);
    cur = cur.next;
    if (l1) l1 = l1.next;
    if (l2) l2 = l2.next;
  }
  return dummy.next;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function addTwoNumbers(?Node $l1, ?Node $l2): ?Node {
    $dummy = new Node(0);
    $cur = $dummy; $carry = 0;
    while ($l1 !== null || $l2 !== null || $carry) {
        $sum = ($l1 ? $l1->val : 0) + ($l2 ? $l2->val : 0) + $carry;
        $carry = intdiv($sum, 10);
        $cur->next = new Node($sum % 10);
        $cur = $cur->next;
        if ($l1) $l1 = $l1->next;
        if ($l2) $l2 = $l2->next;
    }
    return $dummy->next;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def add_two_numbers(l1, l2):
    dummy = Node(0)
    cur, carry = dummy, 0
    while l1 or l2 or carry:
        total = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
        carry, digit = divmod(total, 10)
        cur.next = Node(digit)
        cur = cur.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next
```

<a id="m956"></a>
### 956. Ro'yxatni qayta tartiblash (reorder list)
`L0->L1->...->Ln` ni `L0->Ln->L1->Ln-1->...` ko'rinishiga keltir; o'rtani topish, teskarilash, qo'shish.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const reorderList = (head) => {
  if (!head || !head.next) return head;
  let slow = head, fast = head;
  while (fast.next && fast.next.next) { slow = slow.next; fast = fast.next.next; }
  let second = slow.next, prev = null;
  slow.next = null;
  while (second) { const nx = second.next; second.next = prev; prev = second; second = nx; }
  let first = head;
  while (prev) {
    const t1 = first.next, t2 = prev.next;
    first.next = prev; prev.next = t1;
    first = t1; prev = t2;
  }
  return head;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function reorderList(?Node $head): ?Node {
    if ($head === null || $head->next === null) return $head;
    $slow = $head; $fast = $head;
    while ($fast->next !== null && $fast->next->next !== null) { $slow = $slow->next; $fast = $fast->next->next; }
    $second = $slow->next; $prev = null; $slow->next = null;
    while ($second !== null) { $nx = $second->next; $second->next = $prev; $prev = $second; $second = $nx; }
    $first = $head;
    while ($prev !== null) {
        $t1 = $first->next; $t2 = $prev->next;
        $first->next = $prev; $prev->next = $t1;
        $first = $t1; $prev = $t2;
    }
    return $head;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def reorder_list(head):
    if not head or not head.next:
        return head
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    second, prev = slow.next, None
    slow.next = None
    while second:
        nx = second.next
        second.next = prev
        prev = second
        second = nx
    first = head
    while prev:
        t1, t2 = first.next, prev.next
        first.next = prev
        prev.next = t1
        first, prev = t1, t2
    return head
```

<a id="m957"></a>
### 957. Tasodifiy ko'rsatkichli ro'yxat nusxasi (copy list with random pointer)
Har tuguni `next` va `random` ishoraga ega ro'yxatning chuqur nusxasini O(1) xotira bilan ol (tugunlarni qatorlash usuli).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node {
  constructor(val, next = null, random = null) { this.val = val; this.next = next; this.random = random; }
}
const copyRandomList = (head) => {
  if (!head) return null;
  for (let cur = head; cur; cur = cur.next.next) {
    cur.next = new Node(cur.val, cur.next);
  }
  for (let cur = head; cur; cur = cur.next.next) {
    if (cur.random) cur.next.random = cur.random.next;
  }
  const newHead = head.next;
  for (let cur = head; cur; cur = cur.next) {
    const copy = cur.next;
    cur.next = copy.next;
    if (copy.next) copy.next = copy.next.next;
  }
  return newHead;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public ?Node $random = null;
    public function __construct(public mixed $val, ?Node $next = null, ?Node $random = null) {
        $this->next = $next; $this->random = $random;
    }
}
function copyRandomList(?Node $head): ?Node {
    if ($head === null) return null;
    for ($cur = $head; $cur !== null; $cur = $cur->next->next) {
        $cur->next = new Node($cur->val, $cur->next);
    }
    for ($cur = $head; $cur !== null; $cur = $cur->next->next) {
        if ($cur->random !== null) $cur->next->random = $cur->random->next;
    }
    $newHead = $head->next;
    for ($cur = $head; $cur !== null; $cur = $cur->next) {
        $copy = $cur->next;
        $cur->next = $copy->next;
        if ($copy->next !== null) $copy->next = $copy->next->next;
    }
    return $newHead;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None, random=None):
        self.val = val
        self.next = nxt
        self.random = random

def copy_random_list(head):
    if not head:
        return None
    cur = head
    while cur:
        cur.next = Node(cur.val, cur.next)
        cur = cur.next.next
    cur = head
    while cur:
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    new_head = head.next
    cur = head
    while cur:
        copy = cur.next
        cur.next = copy.next
        if copy.next:
            copy.next = copy.next.next
        cur = cur.next
    return new_head
```

<a id="m958"></a>
### 958. Ro'yxatni aylantirish (rotate list)
Ro'yxatni o'ngga `k` pozitsiyaga aylantir; uzunlikni topib, halqaga ulab, kerakli joyda uz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const rotateRight = (head, k) => {
  if (!head || !head.next || k === 0) return head;
  let len = 1, tail = head;
  while (tail.next) { tail = tail.next; len++; }
  k %= len;
  if (k === 0) return head;
  tail.next = head;
  let steps = len - k, newTail = head;
  for (let i = 1; i < steps; i++) newTail = newTail.next;
  const newHead = newTail.next;
  newTail.next = null;
  return newHead;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function rotateRight(?Node $head, int $k): ?Node {
    if ($head === null || $head->next === null || $k === 0) return $head;
    $len = 1; $tail = $head;
    while ($tail->next !== null) { $tail = $tail->next; $len++; }
    $k %= $len;
    if ($k === 0) return $head;
    $tail->next = $head;
    $steps = $len - $k; $newTail = $head;
    for ($i = 1; $i < $steps; $i++) $newTail = $newTail->next;
    $newHead = $newTail->next;
    $newTail->next = null;
    return $newHead;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def rotate_right(head, k):
    if not head or not head.next or k == 0:
        return head
    length, tail = 1, head
    while tail.next:
        tail = tail.next
        length += 1
    k %= length
    if k == 0:
        return head
    tail.next = head
    steps = length - k
    new_tail = head
    for _ in range(steps - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head
```

<a id="m959"></a>
### 959. Ro'yxatni bo'lish (partition list)
`x` dan kichik tugunlarni oldinga, qolganlarini keyinga sur; ikki yordamchi ro'yxat bilan.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const partition = (head, x) => {
  const lessDummy = new Node(0), geDummy = new Node(0);
  let less = lessDummy, ge = geDummy;
  for (let cur = head; cur; cur = cur.next) {
    if (cur.val < x) { less.next = cur; less = cur; }
    else { ge.next = cur; ge = cur; }
  }
  ge.next = null;
  less.next = geDummy.next;
  return lessDummy.next;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function partition(?Node $head, int $x): ?Node {
    $lessDummy = new Node(0); $geDummy = new Node(0);
    $less = $lessDummy; $ge = $geDummy;
    for ($cur = $head; $cur !== null; $cur = $cur->next) {
        if ($cur->val < $x) { $less->next = $cur; $less = $cur; }
        else { $ge->next = $cur; $ge = $cur; }
    }
    $ge->next = null;
    $less->next = $geDummy->next;
    return $lessDummy->next;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def partition(head, x):
    less_dummy, ge_dummy = Node(0), Node(0)
    less, ge = less_dummy, ge_dummy
    cur = head
    while cur:
        if cur.val < x:
            less.next = cur
            less = cur
        else:
            ge.next = cur
            ge = cur
        cur = cur.next
    ge.next = None
    less.next = ge_dummy.next
    return less_dummy.next
```

<a id="m960"></a>
### 960. Ro'yxatni saralash (sort list, merge sort)
Bog'langan ro'yxatni O(n log n) vaqtda merge sort bilan sara.
`⏱ O(n log n) · 💾 O(log n)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const sortList = (head) => {
  if (!head || !head.next) return head;
  let slow = head, fast = head.next;
  while (fast && fast.next) { slow = slow.next; fast = fast.next.next; }
  const mid = slow.next;
  slow.next = null;
  const left = sortList(head), right = sortList(mid);
  const dummy = new Node(0);
  let cur = dummy, a = left, b = right;
  while (a && b) {
    if (a.val <= b.val) { cur.next = a; a = a.next; }
    else { cur.next = b; b = b.next; }
    cur = cur.next;
  }
  cur.next = a || b;
  return dummy.next;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function sortList(?Node $head): ?Node {
    if ($head === null || $head->next === null) return $head;
    $slow = $head; $fast = $head->next;
    while ($fast !== null && $fast->next !== null) { $slow = $slow->next; $fast = $fast->next->next; }
    $mid = $slow->next; $slow->next = null;
    $left = sortList($head); $right = sortList($mid);
    $dummy = new Node(0); $cur = $dummy; $a = $left; $b = $right;
    while ($a !== null && $b !== null) {
        if ($a->val <= $b->val) { $cur->next = $a; $a = $a->next; }
        else { $cur->next = $b; $b = $b->next; }
        $cur = $cur->next;
    }
    $cur->next = $a ?? $b;
    return $dummy->next;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def sort_list(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    left, right = sort_list(head), sort_list(mid)
    dummy = Node(0)
    cur, a, b = dummy, left, right
    while a and b:
        if a.val <= b.val:
            cur.next, a = a, a.next
        else:
            cur.next, b = b, b.next
        cur = cur.next
    cur.next = a or b
    return dummy.next
```

<a id="m961"></a>
### 961. k-li guruhlarda teskarilash (reverse nodes in k-group)
Ro'yxatni `k` tadan guruhlab teskarila; oxirgi to'liqsiz guruh o'z holicha qoladi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const reverseKGroup = (head, k) => {
  let node = head, count = 0;
  while (node && count < k) { node = node.next; count++; }
  if (count < k) return head;
  let prev = reverseKGroup(node, k), cur = head;
  for (let i = 0; i < k; i++) {
    const nx = cur.next;
    cur.next = prev;
    prev = cur;
    cur = nx;
  }
  return prev;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function reverseKGroup(?Node $head, int $k): ?Node {
    $node = $head; $count = 0;
    while ($node !== null && $count < $k) { $node = $node->next; $count++; }
    if ($count < $k) return $head;
    $prev = reverseKGroup($node, $k); $cur = $head;
    for ($i = 0; $i < $k; $i++) {
        $nx = $cur->next;
        $cur->next = $prev;
        $prev = $cur;
        $cur = $nx;
    }
    return $prev;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def reverse_k_group(head, k):
    node, count = head, 0
    while node and count < k:
        node = node.next
        count += 1
    if count < k:
        return head
    prev = reverse_k_group(node, k)
    cur = head
    for _ in range(k):
        nx = cur.next
        cur.next = prev
        prev = cur
        cur = nx
    return prev
```

<a id="m962"></a>
### 962. Juftlab almashtirish (swap nodes in pairs)
Qo'shni tugunlarni juft-juft qilib joyini almashtir; rekursiv yechim qisqa.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
class Node { constructor(val, next = null) { this.val = val; this.next = next; } }
const swapPairs = (head) => {
  if (!head || !head.next) return head;
  const second = head.next;
  head.next = swapPairs(second.next);
  second.next = head;
  return second;
};
```
**PHP**
```php
class Node {
    public ?Node $next = null;
    public function __construct(public mixed $val, ?Node $next = null) { $this->next = $next; }
}
function swapPairs(?Node $head): ?Node {
    if ($head === null || $head->next === null) return $head;
    $second = $head->next;
    $head->next = swapPairs($second->next);
    $second->next = $head;
    return $second;
}
```
**Python**
```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def swap_pairs(head):
    if not head or not head.next:
        return head
    second = head.next
    head.next = swap_pairs(second.next)
    second.next = head
    return second
```

<a id="m963"></a>
### 963. Keyingi katta element II (next greater element II, aylanma)
Aylanma massivda har element uchun keyingi kattaroqni top; monoton stek va ikki marta aylanish.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const nextGreaterElements = (nums) => {
  const n = nums.length, res = Array(n).fill(-1), stack = [];
  for (let i = 0; i < 2 * n; i++) {
    const cur = nums[i % n];
    while (stack.length && nums[stack[stack.length - 1]] < cur)
      res[stack.pop()] = cur;
    if (i < n) stack.push(i);
  }
  return res;
};
// nextGreaterElements([1,2,1]) // [2,-1,2]
```
**PHP**
```php
function nextGreaterElements(array $nums): array {
    $n = count($nums); $res = array_fill(0, $n, -1); $stack = [];
    for ($i = 0; $i < 2 * $n; $i++) {
        $cur = $nums[$i % $n];
        while (!empty($stack) && $nums[end($stack)] < $cur)
            $res[array_pop($stack)] = $cur;
        if ($i < $n) $stack[] = $i;
    }
    return $res;
}
```
**Python**
```python
def next_greater_elements(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        cur = nums[i % n]
        while stack and nums[stack[-1]] < cur:
            res[stack.pop()] = cur
        if i < n:
            stack.append(i)
    return res
```

<a id="m964"></a>
### 964. Yomg'ir suvini yig'ish (trapping rain water)
Balandliklar orasida tutilib qolgan suv hajmini ikki ko'rsatkich bilan O(1) xotirada hisobla.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const trap = (height) => {
  let l = 0, r = height.length - 1, leftMax = 0, rightMax = 0, water = 0;
  while (l < r) {
    if (height[l] < height[r]) {
      leftMax = Math.max(leftMax, height[l]);
      water += leftMax - height[l++];
    } else {
      rightMax = Math.max(rightMax, height[r]);
      water += rightMax - height[r--];
    }
  }
  return water;
};
// trap([0,1,0,2,1,0,1,3,2,1,2,1]) // 6
```
**PHP**
```php
function trap(array $height): int {
    $l = 0; $r = count($height) - 1; $leftMax = 0; $rightMax = 0; $water = 0;
    while ($l < $r) {
        if ($height[$l] < $height[$r]) {
            $leftMax = max($leftMax, $height[$l]);
            $water += $leftMax - $height[$l++];
        } else {
            $rightMax = max($rightMax, $height[$r]);
            $water += $rightMax - $height[$r--];
        }
    }
    return $water;
}
```
**Python**
```python
def trap(height):
    l, r = 0, len(height) - 1
    left_max = right_max = water = 0
    while l < r:
        if height[l] < height[r]:
            left_max = max(left_max, height[l])
            water += left_max - height[l]
            l += 1
        else:
            right_max = max(right_max, height[r])
            water += right_max - height[r]
            r -= 1
    return water
```

<a id="m965"></a>
### 965. O'zidan boshqa hammasining ko'paytmasi (product of array except self)
Bo'lishsiz har bir pozitsiya uchun qolgan elementlar ko'paytmasini prefiks va suffiks bilan top.
`⏱ O(n) · 💾 O(1) (chiqishdan tashqari)`

**JS**
```js
const productExceptSelf = (nums) => {
  const n = nums.length, res = Array(n).fill(1);
  let prefix = 1;
  for (let i = 0; i < n; i++) { res[i] = prefix; prefix *= nums[i]; }
  let suffix = 1;
  for (let i = n - 1; i >= 0; i--) { res[i] *= suffix; suffix *= nums[i]; }
  return res;
};
// productExceptSelf([1,2,3,4]) // [24,12,8,6]
```
**PHP**
```php
function productExceptSelf(array $nums): array {
    $n = count($nums); $res = array_fill(0, $n, 1);
    $prefix = 1;
    for ($i = 0; $i < $n; $i++) { $res[$i] = $prefix; $prefix *= $nums[$i]; }
    $suffix = 1;
    for ($i = $n - 1; $i >= 0; $i--) { $res[$i] *= $suffix; $suffix *= $nums[$i]; }
    return $res;
}
```
**Python**
```python
def product_except_self(nums):
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res
```

> Daraxt (binary tree) klassikalari — kitobning yakuniy masalalari. Quyida ishlatiladigan
> standart tugun klassi (uni har masalada qayta yozmaymiz):
>
> ```python
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val
>         self.left = left
>         self.right = right
> ```
> JS'da `class TreeNode { constructor(val=0, left=null, right=null){ this.val=val; this.left=left; this.right=right; } }`,
> PHP'da esa `class TreeNode { public function __construct(public $val=0, public $left=null, public $right=null){} }`.

<a id="m966"></a>
### 966. Simmetrik daraxt (symmetric tree)
Daraxt o'z markaziy o'qiga nisbatan oyna kabi simmetrikmi — chap va o'ng pastdaraxtlarni juftlab solishtiramiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const isSymmetric = (root) => {
  const mirror = (a, b) => {
    if (!a && !b) return true;
    if (!a || !b || a.val !== b.val) return false;
    return mirror(a.left, b.right) && mirror(a.right, b.left);
  };
  return !root || mirror(root.left, root.right);
};
```
**PHP**
```php
function isSymmetric($root): bool {
    $mirror = function ($a, $b) use (&$mirror) {
        if (!$a && !$b) return true;
        if (!$a || !$b || $a->val !== $b->val) return false;
        return $mirror($a->left, $b->right) && $mirror($a->right, $b->left);
    };
    return !$root || $mirror($root->left, $root->right);
}
```
**Python**
```python
def is_symmetric(root):
    def mirror(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return mirror(a.left, b.right) and mirror(a.right, b.left)
    return not root or mirror(root.left, root.right)
```

<a id="m967"></a>
### 967. Yo'l yig'indisi (path sum)
Ildizdan bargga boruvchi qiymatlar yig'indisi `target`'ga teng yo'l bormi?
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const hasPathSum = (root, target) => {
  if (!root) return false;
  if (!root.left && !root.right) return root.val === target;
  const rest = target - root.val;
  return hasPathSum(root.left, rest) || hasPathSum(root.right, rest);
};
```
**PHP**
```php
function hasPathSum($root, $target): bool {
    if (!$root) return false;
    if (!$root->left && !$root->right) return $root->val === $target;
    $rest = $target - $root->val;
    return hasPathSum($root->left, $rest) || hasPathSum($root->right, $rest);
}
```
**Python**
```python
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    rest = target - root.val
    return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)
```

<a id="m968"></a>
### 968. Yo'l yig'indisi II — barcha yo'llar (path sum II)
Ildizdan bargga `target`'ga teng bo'lgan barcha yo'llarni qaytaramiz (backtracking bilan).
`⏱ O(n²) · 💾 O(h)`

**JS**
```js
const pathSum = (root, target) => {
  const res = [], path = [];
  const dfs = (node, rem) => {
    if (!node) return;
    path.push(node.val);
    rem -= node.val;
    if (!node.left && !node.right && rem === 0) res.push([...path]);
    else { dfs(node.left, rem); dfs(node.right, rem); }
    path.pop();
  };
  dfs(root, target);
  return res;
};
```
**PHP**
```php
function pathSum($root, $target): array {
    $res = []; $path = [];
    $dfs = function ($node, $rem) use (&$dfs, &$res, &$path) {
        if (!$node) return;
        $path[] = $node->val;
        $rem -= $node->val;
        if (!$node->left && !$node->right && $rem === 0) $res[] = $path;
        else { $dfs($node->left, $rem); $dfs($node->right, $rem); }
        array_pop($path);
    };
    $dfs($root, $target);
    return $res;
}
```
**Python**
```python
def path_sum(root, target):
    res, path = [], []
    def dfs(node, rem):
        if not node:
            return
        path.append(node.val)
        rem -= node.val
        if not node.left and not node.right and rem == 0:
            res.append(path[:])
        else:
            dfs(node.left, rem)
            dfs(node.right, rem)
        path.pop()
    dfs(root, target)
    return res
```

<a id="m969"></a>
### 969. Ildizdan bargga sonlar yig'indisi (sum root to leaf numbers)
Har bir ildiz-barg yo'li raqamlar ketma-ketligini hosil qiladi (masalan 1->2->3 = 123); shularning yig'indisini topamiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const sumNumbers = (root) => {
  const dfs = (node, cur) => {
    if (!node) return 0;
    cur = cur * 10 + node.val;
    if (!node.left && !node.right) return cur;
    return dfs(node.left, cur) + dfs(node.right, cur);
  };
  return dfs(root, 0);
};
```
**PHP**
```php
function sumNumbers($root): int {
    $dfs = function ($node, $cur) use (&$dfs) {
        if (!$node) return 0;
        $cur = $cur * 10 + $node->val;
        if (!$node->left && !$node->right) return $cur;
        return $dfs($node->left, $cur) + $dfs($node->right, $cur);
    };
    return $dfs($root, 0);
}
```
**Python**
```python
def sum_numbers(root):
    def dfs(node, cur):
        if not node:
            return 0
        cur = cur * 10 + node.val
        if not node.left and not node.right:
            return cur
        return dfs(node.left, cur) + dfs(node.right, cur)
    return dfs(root, 0)
```

<a id="m970"></a>
### 970. Daraxtning o'ng tomondan ko'rinishi (binary tree right side view)
O'ngdan qaraganda har sathda eng oxirgi (eng o'ngdagi) tugun ko'rinadi; BFS bilan har sathning oxirini olamiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const rightSideView = (root) => {
  if (!root) return [];
  const res = [];
  let level = [root];
  while (level.length) {
    res.push(level[level.length - 1].val);
    const next = [];
    for (const node of level) {
      if (node.left) next.push(node.left);
      if (node.right) next.push(node.right);
    }
    level = next;
  }
  return res;
};
```
**PHP**
```php
function rightSideView($root): array {
    if (!$root) return [];
    $res = []; $level = [$root];
    while ($level) {
        $res[] = end($level)->val;
        $next = [];
        foreach ($level as $node) {
            if ($node->left) $next[] = $node->left;
            if ($node->right) $next[] = $node->right;
        }
        $level = $next;
    }
    return $res;
}
```
**Python**
```python
def right_side_view(root):
    if not root:
        return []
    res, level = [], [root]
    while level:
        res.append(level[-1].val)
        nxt = []
        for node in level:
            if node.left:
                nxt.append(node.left)
            if node.right:
                nxt.append(node.right)
        level = nxt
    return res
```

<a id="m971"></a>
### 971. Eng yaqin umumiy ajdod (lowest common ancestor — oddiy binary tree)
BST emas; ikki tugunni har ikki pastdaraxtda izlaymiz — agar bir tugun ikkala tomonda topilsa, u LCA.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const lowestCommonAncestor = (root, p, q) => {
  if (!root || root === p || root === q) return root;
  const left = lowestCommonAncestor(root.left, p, q);
  const right = lowestCommonAncestor(root.right, p, q);
  if (left && right) return root;
  return left || right;
};
```
**PHP**
```php
function lowestCommonAncestor($root, $p, $q) {
    if (!$root || $root === $p || $root === $q) return $root;
    $left = lowestCommonAncestor($root->left, $p, $q);
    $right = lowestCommonAncestor($root->right, $p, $q);
    if ($left && $right) return $root;
    return $left ?: $right;
}
```
**Python**
```python
def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```

<a id="m972"></a>
### 972. Daraxt diametri (diameter of binary tree)
Ixtiyoriy ikki barg orasidagi eng uzun yo'l (qirralar soni); har tugunda balandliklar yig'indisini hisoblaymiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const diameterOfBinaryTree = (root) => {
  let best = 0;
  const depth = (node) => {
    if (!node) return 0;
    const l = depth(node.left), r = depth(node.right);
    best = Math.max(best, l + r);
    return 1 + Math.max(l, r);
  };
  depth(root);
  return best;
};
```
**PHP**
```php
function diameterOfBinaryTree($root): int {
    $best = 0;
    $depth = function ($node) use (&$depth, &$best) {
        if (!$node) return 0;
        $l = $depth($node->left); $r = $depth($node->right);
        $best = max($best, $l + $r);
        return 1 + max($l, $r);
    };
    $depth($root);
    return $best;
}
```
**Python**
```python
def diameter_of_binary_tree(root):
    best = 0
    def depth(node):
        nonlocal best
        if not node:
            return 0
        l = depth(node.left)
        r = depth(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    depth(root)
    return best
```

<a id="m973"></a>
### 973. Balanslangan daraxtmi (balanced binary tree)
Har tugunda chap va o'ng pastdaraxt balandliklari farqi 1 dan oshmasligi kerak; -1 "balanssiz" signali.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const isBalanced = (root) => {
  const check = (node) => {
    if (!node) return 0;
    const l = check(node.left);
    if (l === -1) return -1;
    const r = check(node.right);
    if (r === -1 || Math.abs(l - r) > 1) return -1;
    return 1 + Math.max(l, r);
  };
  return check(root) !== -1;
};
```
**PHP**
```php
function isBalanced($root): bool {
    $check = function ($node) use (&$check) {
        if (!$node) return 0;
        $l = $check($node->left);
        if ($l === -1) return -1;
        $r = $check($node->right);
        if ($r === -1 || abs($l - $r) > 1) return -1;
        return 1 + max($l, $r);
    };
    return $check($root) !== -1;
}
```
**Python**
```python
def is_balanced(root):
    def check(node):
        if not node:
            return 0
        l = check(node.left)
        if l == -1:
            return -1
        r = check(node.right)
        if r == -1 or abs(l - r) > 1:
            return -1
        return 1 + max(l, r)
    return check(root) != -1
```

<a id="m974"></a>
### 974. Minimal chuqurlik (minimum depth)
Ildizdan eng yaqin bargagacha bo'lgan tugunlar soni; bitta bola yo'q bo'lsa, mavjud tomon bo'yicha boramiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const minDepth = (root) => {
  if (!root) return 0;
  if (!root.left) return 1 + minDepth(root.right);
  if (!root.right) return 1 + minDepth(root.left);
  return 1 + Math.min(minDepth(root.left), minDepth(root.right));
};
```
**PHP**
```php
function minDepth($root): int {
    if (!$root) return 0;
    if (!$root->left) return 1 + minDepth($root->right);
    if (!$root->right) return 1 + minDepth($root->left);
    return 1 + min(minDepth($root->left), minDepth($root->right));
}
```
**Python**
```python
def min_depth(root):
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))
```

<a id="m975"></a>
### 975. Daraxtni bog'langan ro'yxatga yoyish (flatten binary tree to linked list)
Daraxtni preorder tartibida faqat o'ng ko'rsatkichlardan iborat "ro'yxat"ga aylantiramiz (joyida).
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const flatten = (root) => {
  let prev = null;
  const dfs = (node) => {
    if (!node) return;
    dfs(node.right);
    dfs(node.left);
    node.right = prev;
    node.left = null;
    prev = node;
  };
  dfs(root);
  return root;
};
```
**PHP**
```php
function flatten($root) {
    $prev = null;
    $dfs = function ($node) use (&$dfs, &$prev) {
        if (!$node) return;
        $dfs($node->right);
        $dfs($node->left);
        $node->right = $prev;
        $node->left = null;
        $prev = $node;
    };
    $dfs($root);
    return $root;
}
```
**Python**
```python
def flatten(root):
    prev = None
    def dfs(node):
        nonlocal prev
        if not node:
            return
        dfs(node.right)
        dfs(node.left)
        node.right = prev
        node.left = None
        prev = node
    dfs(root)
    return root
```

<a id="m976"></a>
### 976. Keyingi o'ng ko'rsatkichlarni to'ldirish (populating next right pointers)
Har tugunda `next` maydoni o'sha sathdagi o'ngdagi qo'shni tugunga ishora qiladi; mukammal (perfect) daraxt uchun O(1) qo'shimcha xotira.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
class Node {
  constructor(val = 0, left = null, right = null, next = null) {
    this.val = val; this.left = left; this.right = right; this.next = next;
  }
}
const connect = (root) => {
  let leftmost = root;
  while (leftmost && leftmost.left) {
    let head = leftmost;
    while (head) {
      head.left.next = head.right;
      if (head.next) head.right.next = head.next.left;
      head = head.next;
    }
    leftmost = leftmost.left;
  }
  return root;
};
```
**Python**
```python
class Node:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

def connect(root):
    leftmost = root
    while leftmost and leftmost.left:
        head = leftmost
        while head:
            head.left.next = head.right
            if head.next:
                head.right.next = head.next.left
            head = head.next
        leftmost = leftmost.left
    return root
```

<a id="m977"></a>
### 977. Preorder va inorder'dan daraxt qurish (construct from preorder + inorder)
Preorder birinchi element — ildiz; inorder'da uning o'rni chap/o'ng qismlarni ajratadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const buildTree = (preorder, inorder) => {
  const idx = new Map(inorder.map((v, i) => [v, i]));
  let pre = 0;
  const build = (lo, hi) => {
    if (lo > hi) return null;
    const val = preorder[pre++];
    const node = new TreeNode(val);
    const mid = idx.get(val);
    node.left = build(lo, mid - 1);
    node.right = build(mid + 1, hi);
    return node;
  };
  return build(0, inorder.length - 1);
};
```
**Python**
```python
def build_tree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    pre = 0
    def build(lo, hi):
        nonlocal pre
        if lo > hi:
            return None
        val = preorder[pre]
        pre += 1
        node = TreeNode(val)
        mid = idx[val]
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(inorder) - 1)
```

<a id="m978"></a>
### 978. Inorder va postorder'dan daraxt qurish (construct from inorder + postorder)
Postorder oxirgi element — ildiz; postorder'ni teskari o'qib avval o'ng, keyin chap pastdaraxtni quramiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const buildTreePost = (inorder, postorder) => {
  const idx = new Map(inorder.map((v, i) => [v, i]));
  let post = postorder.length - 1;
  const build = (lo, hi) => {
    if (lo > hi) return null;
    const val = postorder[post--];
    const node = new TreeNode(val);
    const mid = idx.get(val);
    node.right = build(mid + 1, hi);
    node.left = build(lo, mid - 1);
    return node;
  };
  return build(0, inorder.length - 1);
};
```
**Python**
```python
def build_tree_post(inorder, postorder):
    idx = {v: i for i, v in enumerate(inorder)}
    post = len(postorder) - 1
    def build(lo, hi):
        nonlocal post
        if lo > hi:
            return None
        val = postorder[post]
        post -= 1
        node = TreeNode(val)
        mid = idx[val]
        node.right = build(mid + 1, hi)
        node.left = build(lo, mid - 1)
        return node
    return build(0, len(inorder) - 1)
```

<a id="m979"></a>
### 979. Daraxtni serializatsiya va deserializatsiya qilish (serialize / deserialize)
Daraxtni preorder satr ko'rinishiga aylantirib, keyin yana qayta tiklaymiz (`#` — bo'sh tugun).
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const serialize = (root) => {
  const out = [];
  const dfs = (node) => {
    if (!node) { out.push('#'); return; }
    out.push(node.val);
    dfs(node.left);
    dfs(node.right);
  };
  dfs(root);
  return out.join(',');
};
const deserialize = (data) => {
  const vals = data.split(',');
  let i = 0;
  const build = () => {
    const v = vals[i++];
    if (v === '#') return null;
    const node = new TreeNode(Number(v));
    node.left = build();
    node.right = build();
    return node;
  };
  return build();
};
```
**Python**
```python
def serialize(root):
    out = []
    def dfs(node):
        if not node:
            out.append("#")
            return
        out.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return ",".join(out)

def deserialize(data):
    vals = iter(data.split(","))
    def build():
        v = next(vals)
        if v == "#":
            return None
        node = TreeNode(int(v))
        node.left = build()
        node.right = build()
        return node
    return build()
```

<a id="m980"></a>
### 980. BST'dagi k-chi eng kichik element (kth smallest in BST)
BST'ning inorder aylanishi o'sish tartibida bo'ladi; k-chi tashrif buyurilgan tugunni qaytaramiz.
`⏱ O(h + k) · 💾 O(h)`

**JS**
```js
const kthSmallest = (root, k) => {
  const stack = [];
  let node = root;
  while (node || stack.length) {
    while (node) { stack.push(node); node = node.left; }
    node = stack.pop();
    if (--k === 0) return node.val;
    node = node.right;
  }
  return -1;
};
```
**PHP**
```php
function kthSmallest($root, int $k): int {
    $stack = []; $node = $root;
    while ($node || $stack) {
        while ($node) { $stack[] = $node; $node = $node->left; }
        $node = array_pop($stack);
        if (--$k === 0) return $node->val;
        $node = $node->right;
    }
    return -1;
}
```
**Python**
```python
def kth_smallest(root, k):
    stack, node = [], root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return -1
```

<a id="m981"></a>
### 981. BST iterator (klass)
Inorder ketma-ketlikni dangasa (lazy) hosil qiluvchi iterator: `next()` keyingi eng kichikni, `hasNext()` qolgan bor-yo'qligini beradi.
`⏱ O(1) amortizatsiya · 💾 O(h)`

**JS**
```js
class BSTIterator {
  constructor(root) {
    this.stack = [];
    this._push(root);
  }
  _push(node) {
    while (node) { this.stack.push(node); node = node.left; }
  }
  next() {
    const node = this.stack.pop();
    this._push(node.right);
    return node.val;
  }
  hasNext() {
    return this.stack.length > 0;
  }
}
```
**Python**
```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push(root)

    def _push(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()
        self._push(node.right)
        return node.val

    def has_next(self):
        return len(self.stack) > 0
```

<a id="m982"></a>
### 982. BST'dan tugunni o'chirish (delete node in BST)
Topilgan tugunni o'chiramiz: barg/bitta bola oddiy; ikki bola bo'lsa, o'ng pastdaraxtning eng kichigi bilan almashtiramiz.
`⏱ O(h) · 💾 O(h)`

**JS**
```js
const deleteNode = (root, key) => {
  if (!root) return null;
  if (key < root.val) root.left = deleteNode(root.left, key);
  else if (key > root.val) root.right = deleteNode(root.right, key);
  else {
    if (!root.left) return root.right;
    if (!root.right) return root.left;
    let succ = root.right;
    while (succ.left) succ = succ.left;
    root.val = succ.val;
    root.right = deleteNode(root.right, succ.val);
  }
  return root;
};
```
**Python**
```python
def delete_node(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)
    return root
```

<a id="m983"></a>
### 983. Saralangan massivdan balanslangan BST (convert sorted array to BST)
O'rta elementni ildiz qilib olamiz va ikki yarmidan rekursiv quramiz — balandligi minimal daraxt.
`⏱ O(n) · 💾 O(log n)`

**JS**
```js
const sortedArrayToBST = (nums) => {
  const build = (lo, hi) => {
    if (lo > hi) return null;
    const mid = (lo + hi) >> 1;
    const node = new TreeNode(nums[mid]);
    node.left = build(lo, mid - 1);
    node.right = build(mid + 1, hi);
    return node;
  };
  return build(0, nums.length - 1);
};
```
**Python**
```python
def sorted_array_to_bst(nums):
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(nums[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(nums) - 1)
```

<a id="m984"></a>
### 984. BST'ni tiklash (recover BST — ikki tugun almashgan)
Aniq ikki tugun joyi adashgan; inorder'da tartib buzilgan ikki nuqtani topib qiymatlarini almashtiramiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const recoverTree = (root) => {
  let first = null, second = null, prev = null;
  const dfs = (node) => {
    if (!node) return;
    dfs(node.left);
    if (prev && prev.val > node.val) {
      if (!first) first = prev;
      second = node;
    }
    prev = node;
    dfs(node.right);
  };
  dfs(root);
  [first.val, second.val] = [second.val, first.val];
  return root;
};
```
**Python**
```python
def recover_tree(root):
    first = second = prev = None
    def dfs(node):
        nonlocal first, second, prev
        if not node:
            return
        dfs(node.left)
        if prev and prev.val > node.val:
            if not first:
                first = prev
            second = node
        prev = node
        dfs(node.right)
    dfs(root)
    first.val, second.val = second.val, first.val
    return root
```

<a id="m985"></a>
### 985. Daraxtdagi maksimal yo'l yig'indisi (binary tree maximum path sum)
Yo'l ixtiyoriy tugundan boshlanib ixtiyoriy tugunda tugashi mumkin; har tugunda chap+o'ng manfiymas hissalarni birlashtiramiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const maxPathSum = (root) => {
  let best = -Infinity;
  const gain = (node) => {
    if (!node) return 0;
    const l = Math.max(gain(node.left), 0);
    const r = Math.max(gain(node.right), 0);
    best = Math.max(best, node.val + l + r);
    return node.val + Math.max(l, r);
  };
  gain(root);
  return best;
};
```
**PHP**
```php
function maxPathSum($root): int {
    $best = PHP_INT_MIN;
    $gain = function ($node) use (&$gain, &$best) {
        if (!$node) return 0;
        $l = max($gain($node->left), 0);
        $r = max($gain($node->right), 0);
        $best = max($best, $node->val + $l + $r);
        return $node->val + max($l, $r);
    };
    $gain($root);
    return $best;
}
```
**Python**
```python
def max_path_sum(root):
    best = float("-inf")
    def gain(node):
        nonlocal best
        if not node:
            return 0
        l = max(gain(node.left), 0)
        r = max(gain(node.right), 0)
        best = max(best, node.val + l + r)
        return node.val + max(l, r)
    gain(root)
    return best
```

<a id="m986"></a>
### 986. Zigzag sath tartibida aylanish (zigzag level order traversal)
Sathlar bo'yicha BFS, lekin har juft sathni teskari yo'nalishda yozamiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const zigzagLevelOrder = (root) => {
  if (!root) return [];
  const res = [];
  let level = [root], leftToRight = true;
  while (level.length) {
    const vals = level.map((n) => n.val);
    res.push(leftToRight ? vals : vals.reverse());
    const next = [];
    for (const node of level) {
      if (node.left) next.push(node.left);
      if (node.right) next.push(node.right);
    }
    level = next;
    leftToRight = !leftToRight;
  }
  return res;
};
```
**Python**
```python
def zigzag_level_order(root):
    if not root:
        return []
    res, level, left_to_right = [], [root], True
    while level:
        vals = [n.val for n in level]
        res.append(vals if left_to_right else vals[::-1])
        nxt = []
        for node in level:
            if node.left:
                nxt.append(node.left)
            if node.right:
                nxt.append(node.right)
        level = nxt
        left_to_right = not left_to_right
    return res
```

<a id="m987"></a>
### 987. BST'dagi modani topish (find mode in BST)
Eng ko'p uchragan qiymat(lar); inorder'da tartiblangan ketma-ketlik bo'lgani uchun ketma-ket teng qiymatlarni sanaymiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const findMode = (root) => {
  let res = [], cur = null, count = 0, best = 0;
  const dfs = (node) => {
    if (!node) return;
    dfs(node.left);
    count = node.val === cur ? count + 1 : 1;
    cur = node.val;
    if (count > best) { best = count; res = [cur]; }
    else if (count === best) res.push(cur);
    dfs(node.right);
  };
  dfs(root);
  return res;
};
```
**Python**
```python
def find_mode(root):
    res, cur, count, best = [], None, 0, 0
    def dfs(node):
        nonlocal cur, count, best, res
        if not node:
            return
        dfs(node.left)
        count = count + 1 if node.val == cur else 1
        cur = node.val
        if count > best:
            best = count
            res = [cur]
        elif count == best:
            res.append(cur)
        dfs(node.right)
    dfs(root)
    return res
```

<a id="m988"></a>
### 988. BST oraliq yig'indisi (range sum of BST)
`[low, high]` oralig'idagi barcha qiymatlar yig'indisi; BST xususiyatidan foydalanib keraksiz shoxlarni kesamiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const rangeSumBST = (root, low, high) => {
  if (!root) return 0;
  if (root.val < low) return rangeSumBST(root.right, low, high);
  if (root.val > high) return rangeSumBST(root.left, low, high);
  return root.val + rangeSumBST(root.left, low, high) + rangeSumBST(root.right, low, high);
};
```
**PHP**
```php
function rangeSumBST($root, int $low, int $high): int {
    if (!$root) return 0;
    if ($root->val < $low) return rangeSumBST($root->right, $low, $high);
    if ($root->val > $high) return rangeSumBST($root->left, $low, $high);
    return $root->val + rangeSumBST($root->left, $low, $high) + rangeSumBST($root->right, $low, $high);
}
```
**Python**
```python
def range_sum_bst(root, low, high):
    if not root:
        return 0
    if root.val < low:
        return range_sum_bst(root.right, low, high)
    if root.val > high:
        return range_sum_bst(root.left, low, high)
    return root.val + range_sum_bst(root.left, low, high) + range_sum_bst(root.right, low, high)
```

<a id="m989"></a>
### 989. BST'ni kesish (trim a BST — low..high)
`[low, high]` oralig'idan tashqaridagi tugunlarni olib tashlab, BST tuzilishini saqlaymiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const trimBST = (root, low, high) => {
  if (!root) return null;
  if (root.val < low) return trimBST(root.right, low, high);
  if (root.val > high) return trimBST(root.left, low, high);
  root.left = trimBST(root.left, low, high);
  root.right = trimBST(root.right, low, high);
  return root;
};
```
**PHP**
```php
function trimBST($root, int $low, int $high) {
    if (!$root) return null;
    if ($root->val < $low) return trimBST($root->right, $low, $high);
    if ($root->val > $high) return trimBST($root->left, $low, $high);
    $root->left = trimBST($root->left, $low, $high);
    $root->right = trimBST($root->right, $low, $high);
    return $root;
}
```
**Python**
```python
def trim_bst(root, low, high):
    if not root:
        return None
    if root.val < low:
        return trim_bst(root.right, low, high)
    if root.val > high:
        return trim_bst(root.left, low, high)
    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root
```

<a id="m990"></a>
### 990. Berilgan tugundan k masofadagi barcha tugunlar (all nodes distance k)
Maqsadli tugundan aynan k qadam uzoqdagi qiymatlar; avval ota-ona xaritasini quramiz, keyin BFS bilan tarqaymiz.
`⏱ O(n) · 💾 O(n)`

**Python**
```python
from collections import deque

def distance_k(root, target, k):
    parent = {}
    def link(node, par):
        if not node:
            return
        parent[node] = par
        link(node.left, node)
        link(node.right, node)
    link(root, None)
    seen = {target}
    q = deque([(target, 0)])
    res = []
    while q:
        node, d = q.popleft()
        if d == k:
            res.append(node.val)
            continue
        for nb in (node.left, node.right, parent[node]):
            if nb and nb not in seen:
                seen.add(nb)
                q.append((nb, d + 1))
    return res
```
**JS**
```js
const distanceK = (root, target, k) => {
  const parent = new Map();
  const link = (node, par) => {
    if (!node) return;
    parent.set(node, par);
    link(node.left, node);
    link(node.right, node);
  };
  link(root, null);
  const seen = new Set([target]);
  let queue = [[target, 0]];
  const res = [];
  while (queue.length) {
    const next = [];
    for (const [node, d] of queue) {
      if (d === k) { res.push(node.val); continue; }
      for (const nb of [node.left, node.right, parent.get(node)]) {
        if (nb && !seen.has(nb)) { seen.add(nb); next.push([nb, d + 1]); }
      }
    }
    queue = next;
  }
  return res;
};
```

<a id="m991"></a>
### 991. Yaxshi tugunlarni sanash (count good nodes)
Tugun "yaxshi" — agar ildizdan unga boruvchi yo'lda undan katta qiymat bo'lmasa; yo'l bo'yicha maksimumni uzatamiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const goodNodes = (root) => {
  const dfs = (node, mx) => {
    if (!node) return 0;
    const good = node.val >= mx ? 1 : 0;
    const nm = Math.max(mx, node.val);
    return good + dfs(node.left, nm) + dfs(node.right, nm);
  };
  return dfs(root, -Infinity);
};
```
**PHP**
```php
function goodNodes($root): int {
    $dfs = function ($node, $mx) use (&$dfs) {
        if (!$node) return 0;
        $good = $node->val >= $mx ? 1 : 0;
        $nm = max($mx, $node->val);
        return $good + $dfs($node->left, $nm) + $dfs($node->right, $nm);
    };
    return $dfs($root, PHP_INT_MIN);
}
```
**Python**
```python
def good_nodes(root):
    def dfs(node, mx):
        if not node:
            return 0
        good = 1 if node.val >= mx else 0
        nm = max(mx, node.val)
        return good + dfs(node.left, nm) + dfs(node.right, nm)
    return dfs(root, float("-inf"))
```

<a id="m992"></a>
### 992. Uy o'g'risi III (house robber III — daraxt DP)
Qo'shni (ota-bola) tugunlarni birga "talon-taroj" qilib bo'lmaydi; har tugunda (olingan, olinmagan) juftligini qaytaramiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const rob = (root) => {
  const dfs = (node) => {
    if (!node) return [0, 0];
    const [lTake, lSkip] = dfs(node.left);
    const [rTake, rSkip] = dfs(node.right);
    const take = node.val + lSkip + rSkip;
    const skip = Math.max(lTake, lSkip) + Math.max(rTake, rSkip);
    return [take, skip];
  };
  return Math.max(...dfs(root));
};
```
**Python**
```python
def rob(root):
    def dfs(node):
        if not node:
            return (0, 0)
        l_take, l_skip = dfs(node.left)
        r_take, r_skip = dfs(node.right)
        take = node.val + l_skip + r_skip
        skip = max(l_take, l_skip) + max(r_take, r_skip)
        return (take, skip)
    return max(dfs(root))
```

<a id="m993"></a>
### 993. Boshqa daraxtning pastdaraxti (subtree of another tree)
`sub` daraxti `root`'ning biror tuguni ostida aynan takrorlanadimi — har tugunda tenglikni tekshiramiz.
`⏱ O(m × n) · 💾 O(h)`

**JS**
```js
const isSubtree = (root, sub) => {
  const same = (a, b) => {
    if (!a && !b) return true;
    if (!a || !b || a.val !== b.val) return false;
    return same(a.left, b.left) && same(a.right, b.right);
  };
  if (!root) return false;
  return same(root, sub) || isSubtree(root.left, sub) || isSubtree(root.right, sub);
};
```
**PHP**
```php
function isSubtree($root, $sub): bool {
    $same = function ($a, $b) use (&$same) {
        if (!$a && !$b) return true;
        if (!$a || !$b || $a->val !== $b->val) return false;
        return $same($a->left, $b->left) && $same($a->right, $b->right);
    };
    if (!$root) return false;
    return $same($root, $sub) || isSubtree($root->left, $sub) || isSubtree($root->right, $sub);
}
```
**Python**
```python
def is_subtree(root, sub):
    def same(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return same(a.left, b.left) and same(a.right, b.right)
    if not root:
        return False
    return same(root, sub) or is_subtree(root.left, sub) or is_subtree(root.right, sub)
```

<a id="m994"></a>
### 994. Ikki daraxtni birlashtirish (merge two binary trees)
Mos tugunlarni qo'shamiz; bittasi bo'sh bo'lsa ikkinchisini olamiz.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const mergeTrees = (t1, t2) => {
  if (!t1) return t2;
  if (!t2) return t1;
  const node = new TreeNode(t1.val + t2.val);
  node.left = mergeTrees(t1.left, t2.left);
  node.right = mergeTrees(t1.right, t2.right);
  return node;
};
```
**Python**
```python
def merge_trees(t1, t2):
    if not t1:
        return t2
    if not t2:
        return t1
    node = TreeNode(t1.val + t2.val)
    node.left = merge_trees(t1.left, t2.left)
    node.right = merge_trees(t1.right, t2.right)
    return node
```

<a id="m995"></a>
### 995. Sathlar o'rtacha qiymati (average of levels)
Har bir sathdagi qiymatlarning o'rtacha arifmetigini topamiz (BFS).
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const averageOfLevels = (root) => {
  const res = [];
  let level = root ? [root] : [];
  while (level.length) {
    const sum = level.reduce((s, n) => s + n.val, 0);
    res.push(sum / level.length);
    const next = [];
    for (const node of level) {
      if (node.left) next.push(node.left);
      if (node.right) next.push(node.right);
    }
    level = next;
  }
  return res;
};
```
**Python**
```python
def average_of_levels(root):
    res = []
    level = [root] if root else []
    while level:
        res.append(sum(n.val for n in level) / len(level))
        nxt = []
        for node in level:
            if node.left:
                nxt.append(node.left)
            if node.right:
                nxt.append(node.right)
        level = nxt
    return res
```

<a id="m996"></a>
### 996. Chap barglar yig'indisi (sum of left leaves)
Faqat chap bola bo'lib turgan barglarning qiymatlari yig'indisi.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const sumOfLeftLeaves = (root) => {
  if (!root) return 0;
  let sum = 0;
  if (root.left && !root.left.left && !root.left.right) sum += root.left.val;
  else sum += sumOfLeftLeaves(root.left);
  sum += sumOfLeftLeaves(root.right);
  return sum;
};
```
**PHP**
```php
function sumOfLeftLeaves($root): int {
    if (!$root) return 0;
    $sum = 0;
    if ($root->left && !$root->left->left && !$root->left->right) $sum += $root->left->val;
    else $sum += sumOfLeftLeaves($root->left);
    $sum += sumOfLeftLeaves($root->right);
    return $sum;
}
```
**Python**
```python
def sum_of_left_leaves(root):
    if not root:
        return 0
    total = 0
    if root.left and not root.left.left and not root.left.right:
        total += root.left.val
    else:
        total += sum_of_left_leaves(root.left)
    total += sum_of_left_leaves(root.right)
    return total
```

<a id="m997"></a>
### 997. Eng pastki chap qiymat (find bottom left value)
Eng chuqur sathning eng chap tugunining qiymati; o'ngdan chapga BFS qilsak, oxirgi ko'rilgan tugun shu bo'ladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const findBottomLeftValue = (root) => {
  let queue = [root], val = root.val;
  while (queue.length) {
    const next = [];
    val = queue[0].val;
    for (const node of queue) {
      if (node.left) next.push(node.left);
      if (node.right) next.push(node.right);
    }
    queue = next;
  }
  return val;
};
```
**Python**
```python
from collections import deque

def find_bottom_left_value(root):
    q = deque([root])
    val = root.val
    while q:
        val = q[0].val
        for _ in range(len(q)):
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return val
```

<a id="m998"></a>
### 998. Daraxtning maksimal kengligi (maximum width of binary tree)
Eng keng sathdagi chetki tugunlar orasidagi masofa (bo'sh joylar ham hisobga olinadi); tugunlarni indekslab boramiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const widthOfBinaryTree = (root) => {
  if (!root) return 0;
  let best = 0;
  let level = [[root, 0]];
  while (level.length) {
    const base = level[0][1];
    best = Math.max(best, level[level.length - 1][1] - base + 1);
    const next = [];
    for (const [node, idx] of level) {
      const pos = idx - base;
      if (node.left) next.push([node.left, 2 * pos]);
      if (node.right) next.push([node.right, 2 * pos + 1]);
    }
    level = next;
  }
  return best;
};
```
**Python**
```python
def width_of_binary_tree(root):
    if not root:
        return 0
    best = 0
    level = [(root, 0)]
    while level:
        base = level[0][1]
        best = max(best, level[-1][1] - base + 1)
        nxt = []
        for node, idx in level:
            pos = idx - base
            if node.left:
                nxt.append((node.left, 2 * pos))
            if node.right:
                nxt.append((node.right, 2 * pos + 1))
        level = nxt
    return best
```

<a id="m999"></a>
### 999. Vertikal tartibda aylanish (vertical order traversal)
Tugunlarni (ustun, qator) bo'yicha guruhlaymiz; bir xil pozitsiyada qiymat bo'yicha saralaymiz.
`⏱ O(n log n) · 💾 O(n)`

**Python**
```python
from collections import defaultdict

def vertical_traversal(root):
    cols = defaultdict(list)
    def dfs(node, r, c):
        if not node:
            return
        cols[c].append((r, node.val))
        dfs(node.left, r + 1, c - 1)
        dfs(node.right, r + 1, c + 1)
    dfs(root, 0, 0)
    res = []
    for c in sorted(cols):
        res.append([v for _, v in sorted(cols[c])])
    return res
```
**JS**
```js
const verticalTraversal = (root) => {
  const cols = new Map();
  const dfs = (node, r, c) => {
    if (!node) return;
    if (!cols.has(c)) cols.set(c, []);
    cols.get(c).push([r, node.val]);
    dfs(node.left, r + 1, c - 1);
    dfs(node.right, r + 1, c + 1);
  };
  dfs(root, 0, 0);
  return [...cols.keys()].sort((a, b) => a - b).map((c) =>
    cols.get(c).sort((a, b) => a[0] - b[0] || a[1] - b[1]).map((x) => x[1])
  );
};
```

<a id="m1000"></a>
### 1000. Daraxt yo'llari — satr ko'rinishida (binary tree paths)
Ildizdan har bir bargga boruvchi yo'lni `"a->b->c"` ko'rinishidagi satr qilib qaytaramiz. Kitobimizning yakuniy masalasi.
`⏱ O(n) · 💾 O(h)`

**JS**
```js
const binaryTreePaths = (root) => {
  const res = [];
  const dfs = (node, path) => {
    if (!node) return;
    path = path ? `${path}->${node.val}` : `${node.val}`;
    if (!node.left && !node.right) { res.push(path); return; }
    dfs(node.left, path);
    dfs(node.right, path);
  };
  dfs(root, "");
  return res;
};
```
**PHP**
```php
function binaryTreePaths($root): array {
    $res = [];
    $dfs = function ($node, $path) use (&$dfs, &$res) {
        if (!$node) return;
        $path = $path === "" ? (string)$node->val : "$path->$node->val";
        if (!$node->left && !$node->right) { $res[] = $path; return; }
        $dfs($node->left, $path);
        $dfs($node->right, $path);
    };
    $dfs($root, "");
    return $res;
}
```
**Python**
```python
def binary_tree_paths(root):
    res = []
    def dfs(node, path):
        if not node:
            return
        path = f"{path}->{node.val}" if path else str(node.val)
        if not node.left and not node.right:
            res.append(path)
            return
        dfs(node.left, path)
        dfs(node.right, path)
    dfs(root, "")
    return res
```

---
