<a id="b35"></a>
# 35-bo'lim: Ilg'or saralash va qidiruv

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Bu bo'limda klassik solishtiruvchi saralashlardan tashqari xususiy (non-comparison) saralash
> algoritmlari (radix, bucket, pigeonhole, counting g'oyalari), kam uchraydigan, lekin
> o'rganishga arzigulik saralashlar (cocktail, comb, gnome, cycle, pancake) hamda binary
> search'ning kuchli qo'llanishlari ko'rib chiqiladi. Eng muhim mavzu — "javob ustida binary
> search" (binary search on the answer): bunda biz qiymatlar massivi emas, balki javoblar
> oralig'ini ikkiga bo'lib qidiramiz. Bu uslub Koko, kemalar, sahifalar va boshqa ko'plab
> optimallashtirish masalalarini O(n log range) da yechishga imkon beradi.

<a id="m767"></a>
### 767. Radix sort (LSD, manfiy bo'lmagan butun sonlar)
Sonlarni raqamlari bo'yicha eng kichik xonadan boshlab counting sort bilan saralaydi.
`⏱ O(d × (n + b)) · 💾 O(n + b)`

**JS**
```js
const radixSort = (arr) => {
  if (arr.length === 0) return arr;
  const max = Math.max(...arr);
  for (let exp = 1; Math.floor(max / exp) > 0; exp *= 10) {
    const out = Array(arr.length);
    const cnt = Array(10).fill(0);
    for (const x of arr) cnt[Math.floor(x / exp) % 10]++;
    for (let i = 1; i < 10; i++) cnt[i] += cnt[i - 1];
    for (let i = arr.length - 1; i >= 0; i--) {
      const d = Math.floor(arr[i] / exp) % 10;
      out[--cnt[d]] = arr[i];
    }
    for (let i = 0; i < arr.length; i++) arr[i] = out[i];
  }
  return arr;
};
```
**PHP**
```php
function radixSort(array $arr): array {
    if (!$arr) return $arr;
    $max = max($arr);
    for ($exp = 1; intdiv($max, $exp) > 0; $exp *= 10) {
        $out = array_fill(0, count($arr), 0);
        $cnt = array_fill(0, 10, 0);
        foreach ($arr as $x) $cnt[intdiv($x, $exp) % 10]++;
        for ($i = 1; $i < 10; $i++) $cnt[$i] += $cnt[$i - 1];
        for ($i = count($arr) - 1; $i >= 0; $i--) {
            $d = intdiv($arr[$i], $exp) % 10;
            $out[--$cnt[$d]] = $arr[$i];
        }
        $arr = $out;
    }
    return $arr;
}
```
**Python**
```python
def radix_sort(arr):
    if not arr:
        return arr
    mx = max(arr)
    exp = 1
    while mx // exp > 0:
        out = [0] * len(arr)
        cnt = [0] * 10
        for x in arr:
            cnt[(x // exp) % 10] += 1
        for i in range(1, 10):
            cnt[i] += cnt[i - 1]
        for x in reversed(arr):
            d = (x // exp) % 10
            cnt[d] -= 1
            out[cnt[d]] = x
        arr = out
        exp *= 10
    return arr
```

<a id="m768"></a>
### 768. Bucket sort (taqsimot bo'yicha saralash)
[0, 1) oralig'idagi sonlarni teng "chelak"larga taqsimlab, har birini saralab birlashtiradi.
`⏱ O(n) o'rtacha · 💾 O(n)`

**JS**
```js
const bucketSort = (arr) => {
  const n = arr.length;
  if (n === 0) return arr;
  const buckets = Array.from({ length: n }, () => []);
  for (const x of arr) buckets[Math.min(n - 1, Math.floor(x * n))].push(x);
  const res = [];
  for (const b of buckets) {
    b.sort((a, c) => a - c);
    res.push(...b);
  }
  return res;
};
```
**Python**
```python
def bucket_sort(arr):
    n = len(arr)
    if n == 0:
        return arr
    buckets = [[] for _ in range(n)]
    for x in arr:
        buckets[min(n - 1, int(x * n))].append(x)
    res = []
    for b in buckets:
        b.sort()
        res.extend(b)
    return res
```

<a id="m769"></a>
### 769. Pigeonhole sort
Qiymatlar oralig'i kichik bo'lganda har bir qiymat uchun "katak" ajratib saralaydi.
`⏱ O(n + range) · 💾 O(range)`

**JS**
```js
const pigeonholeSort = (arr) => {
  if (arr.length === 0) return arr;
  const min = Math.min(...arr), max = Math.max(...arr);
  const holes = Array(max - min + 1).fill(0);
  for (const x of arr) holes[x - min]++;
  const res = [];
  for (let i = 0; i < holes.length; i++)
    while (holes[i]-- > 0) res.push(i + min);
  return res;
};
```
**PHP**
```php
function pigeonholeSort(array $arr): array {
    if (!$arr) return $arr;
    $min = min($arr); $max = max($arr);
    $holes = array_fill(0, $max - $min + 1, 0);
    foreach ($arr as $x) $holes[$x - $min]++;
    $res = [];
    foreach ($holes as $i => $c)
        while ($c-- > 0) $res[] = $i + $min;
    return $res;
}
```
**Python**
```python
def pigeonhole_sort(arr):
    if not arr:
        return arr
    lo, hi = min(arr), max(arr)
    holes = [0] * (hi - lo + 1)
    for x in arr:
        holes[x - lo] += 1
    res = []
    for i, c in enumerate(holes):
        res.extend([i + lo] * c)
    return res
```

<a id="m770"></a>
### 770. Cocktail shaker sort (ikki tomonlama bubble)
Bubble sort'ning ikki yo'nalishli varianti: har o'tishda chap va o'ng chegaralar qisqaradi.
`⏱ O(n²) · 💾 O(1)`

**JS**
```js
const cocktailSort = (arr) => {
  let lo = 0, hi = arr.length - 1, swapped = true;
  while (swapped) {
    swapped = false;
    for (let i = lo; i < hi; i++)
      if (arr[i] > arr[i + 1]) { [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]]; swapped = true; }
    hi--;
    for (let i = hi; i > lo; i--)
      if (arr[i - 1] > arr[i]) { [arr[i - 1], arr[i]] = [arr[i], arr[i - 1]]; swapped = true; }
    lo++;
  }
  return arr;
};
```
**Python**
```python
def cocktail_sort(arr):
    lo, hi, swapped = 0, len(arr) - 1, True
    while swapped:
        swapped = False
        for i in range(lo, hi):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        hi -= 1
        for i in range(hi, lo, -1):
            if arr[i - 1] > arr[i]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]
                swapped = True
        lo += 1
    return arr
```

<a id="m771"></a>
### 771. Comb sort
Bubble'ning yaxshilangan varianti: katta "tarama" oralig'idan boshlab uni 1.3 ga bo'lib kichraytiradi.
`⏱ O(n²) eng yomon, O(n log n) o'rtacha · 💾 O(1)`

**JS**
```js
const combSort = (arr) => {
  let gap = arr.length, swapped = true;
  while (gap > 1 || swapped) {
    gap = Math.max(1, Math.floor(gap / 1.3));
    swapped = false;
    for (let i = 0; i + gap < arr.length; i++)
      if (arr[i] > arr[i + gap]) {
        [arr[i], arr[i + gap]] = [arr[i + gap], arr[i]];
        swapped = true;
      }
  }
  return arr;
};
```
**Python**
```python
def comb_sort(arr):
    gap, swapped = len(arr), True
    while gap > 1 or swapped:
        gap = max(1, int(gap / 1.3))
        swapped = False
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
    return arr
```

<a id="m772"></a>
### 772. Gnome sort
Eng sodda saralash: noto'g'ri juftni topsa orqaga qadam tashlaydi, aks holda oldinga yuradi.
`⏱ O(n²) · 💾 O(1)`

**JS**
```js
const gnomeSort = (arr) => {
  let i = 0;
  while (i < arr.length) {
    if (i === 0 || arr[i] >= arr[i - 1]) i++;
    else { [arr[i], arr[i - 1]] = [arr[i - 1], arr[i]]; i--; }
  }
  return arr;
};
```
**PHP**
```php
function gnomeSort(array $arr): array {
    $i = 0; $n = count($arr);
    while ($i < $n) {
        if ($i === 0 || $arr[$i] >= $arr[$i - 1]) $i++;
        else { [$arr[$i], $arr[$i - 1]] = [$arr[$i - 1], $arr[$i]]; $i--; }
    }
    return $arr;
}
```
**Python**
```python
def gnome_sort(arr):
    i = 0
    while i < len(arr):
        if i == 0 or arr[i] >= arr[i - 1]:
            i += 1
        else:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            i -= 1
    return arr
```

<a id="m773"></a>
### 773. Cycle sort
Yozish amallari sonini minimal qiladi: har elementni to'g'ri o'rniga to'g'ridan-to'g'ri joylashtiradi.
`⏱ O(n²) · 💾 O(1)`

**JS**
```js
const cycleSort = (arr) => {
  const n = arr.length;
  for (let start = 0; start < n - 1; start++) {
    let item = arr[start];
    let pos = start;
    for (let i = start + 1; i < n; i++) if (arr[i] < item) pos++;
    if (pos === start) continue;
    while (item === arr[pos]) pos++;
    [arr[pos], item] = [item, arr[pos]];
    while (pos !== start) {
      pos = start;
      for (let i = start + 1; i < n; i++) if (arr[i] < item) pos++;
      while (item === arr[pos]) pos++;
      [arr[pos], item] = [item, arr[pos]];
    }
  }
  return arr;
};
```
**Python**
```python
def cycle_sort(arr):
    n = len(arr)
    for start in range(n - 1):
        item = arr[start]
        pos = start + sum(1 for i in range(start + 1, n) if arr[i] < item)
        if pos == start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        while pos != start:
            pos = start + sum(1 for i in range(start + 1, n) if arr[i] < item)
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
    return arr
```

<a id="m774"></a>
### 774. Pancake sort
Faqat "flip" (prefiksni ag'darish) amali bilan saralaydi — eng kattasini ketma-ket joyiga qo'yadi.
`⏱ O(n²) · 💾 O(1)`

**JS**
```js
const pancakeSort = (arr) => {
  const flip = (k) => {
    let i = 0;
    while (i < k) { [arr[i], arr[k]] = [arr[k], arr[i]]; i++; k--; }
  };
  for (let size = arr.length; size > 1; size--) {
    let mi = 0;
    for (let i = 1; i < size; i++) if (arr[i] > arr[mi]) mi = i;
    if (mi !== size - 1) {
      flip(mi);
      flip(size - 1);
    }
  }
  return arr;
};
```
**Python**
```python
def pancake_sort(arr):
    def flip(k):
        i = 0
        while i < k:
            arr[i], arr[k] = arr[k], arr[i]
            i += 1
            k -= 1
    for size in range(len(arr), 1, -1):
        mi = max(range(size), key=lambda i: arr[i])
        if mi != size - 1:
            flip(mi)
            flip(size - 1)
    return arr
```

<a id="m775"></a>
### 775. Quickselect — k-chi eng kichik element
Quicksort'ning bo'lish (partition) g'oyasi bilan saralamasdan k-chi elementni topadi.
`⏱ O(n) o'rtacha · 💾 O(1)`

**JS**
```js
const quickselect = (arr, k) => {
  let lo = 0, hi = arr.length - 1;
  while (lo < hi) {
    const pivot = arr[hi];
    let i = lo;
    for (let j = lo; j < hi; j++)
      if (arr[j] < pivot) { [arr[i], arr[j]] = [arr[j], arr[i]]; i++; }
    [arr[i], arr[hi]] = [arr[hi], arr[i]];
    if (i === k) return arr[i];
    if (i < k) lo = i + 1; else hi = i - 1;
  }
  return arr[lo];
};
```
**Python**
```python
def quickselect(arr, k):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        if i == k:
            return arr[i]
        if i < k:
            lo = i + 1
        else:
            hi = i - 1
    return arr[lo]
```

<a id="m776"></a>
### 776. Median of medians (kafolatlangan O(n) tanlash)
Pivotni "medianalar medianasi" sifatida tanlab, eng yomon holatda ham chiziqli vaqtni kafolatlaydi.
`⏱ O(n) eng yomon · 💾 O(n)`

**Python**
```python
def select(arr, k):
    if len(arr) <= 5:
        return sorted(arr)[k]
    groups = [sorted(arr[i:i + 5]) for i in range(0, len(arr), 5)]
    medians = [g[len(g) // 2] for g in groups]
    pivot = select(medians, len(medians) // 2)
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    eqs = len(arr) - len(lows) - len(highs)
    if k < len(lows):
        return select(lows, k)
    if k < len(lows) + eqs:
        return pivot
    return select(highs, k - len(lows) - eqs)
```
**JS**
```js
const select = (arr, k) => {
  if (arr.length <= 5) return [...arr].sort((a, b) => a - b)[k];
  const medians = [];
  for (let i = 0; i < arr.length; i += 5) {
    const g = arr.slice(i, i + 5).sort((a, b) => a - b);
    medians.push(g[g.length >> 1]);
  }
  const pivot = select(medians, medians.length >> 1);
  const lows = arr.filter((x) => x < pivot);
  const highs = arr.filter((x) => x > pivot);
  const eqs = arr.length - lows.length - highs.length;
  if (k < lows.length) return select(lows, k);
  if (k < lows.length + eqs) return pivot;
  return select(highs, k - lows.length - eqs);
};
```

<a id="m777"></a>
### 777. Dutch national flag (ranglarni saralash)
0, 1, 2 dan iborat massivni bitta o'tishda joyida saralaydi (uch yo'nalishli bo'lish).
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const sortColors = (arr) => {
  let lo = 0, mid = 0, hi = arr.length - 1;
  while (mid <= hi) {
    if (arr[mid] === 0) { [arr[lo], arr[mid]] = [arr[mid], arr[lo]]; lo++; mid++; }
    else if (arr[mid] === 2) { [arr[mid], arr[hi]] = [arr[hi], arr[mid]]; hi--; }
    else mid++;
  }
  return arr;
};
```
**PHP**
```php
function sortColors(array $arr): array {
    $lo = 0; $mid = 0; $hi = count($arr) - 1;
    while ($mid <= $hi) {
        if ($arr[$mid] === 0) { [$arr[$lo], $arr[$mid]] = [$arr[$mid], $arr[$lo]]; $lo++; $mid++; }
        elseif ($arr[$mid] === 2) { [$arr[$mid], $arr[$hi]] = [$arr[$hi], $arr[$mid]]; $hi--; }
        else $mid++;
    }
    return $arr;
}
```
**Python**
```python
def sort_colors(arr):
    lo, mid, hi = 0, 0, len(arr) - 1
    while mid <= hi:
        if arr[mid] == 0:
            arr[lo], arr[mid] = arr[mid], arr[lo]
            lo += 1
            mid += 1
        elif arr[mid] == 2:
            arr[mid], arr[hi] = arr[hi], arr[mid]
            hi -= 1
        else:
            mid += 1
    return arr
```

<a id="m778"></a>
### 778. Wiggle sort
Massivni `a[0] < a[1] > a[2] < a[3] ...` ko'rinishiga bitta o'tishda keltiradi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const wiggleSort = (arr) => {
  for (let i = 0; i < arr.length - 1; i++) {
    const wrong = i % 2 === 0 ? arr[i] > arr[i + 1] : arr[i] < arr[i + 1];
    if (wrong) [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]];
  }
  return arr;
};
```
**Python**
```python
def wiggle_sort(arr):
    for i in range(len(arr) - 1):
        wrong = arr[i] > arr[i + 1] if i % 2 == 0 else arr[i] < arr[i + 1]
        if wrong:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr
```

<a id="m779"></a>
### 779. Custom comparator sort (ko'p maydon bo'yicha)
Obyektlarni avval yosh (o'sish), so'ng ism (alifbo) bo'yicha saralash.

**JS**
```js
const sortPeople = (people) =>
  [...people].sort((a, b) => a.age - b.age || a.name.localeCompare(b.name));
// sortPeople([{name:"Bob",age:30},{name:"Ann",age:30},{name:"Cy",age:25}])
```
**PHP**
```php
function sortPeople(array $people): array {
    usort($people, fn($a, $b) =>
        $a['age'] <=> $b['age'] ?: strcmp($a['name'], $b['name']));
    return $people;
}
```
**Python**
```python
def sort_people(people):
    return sorted(people, key=lambda p: (p["age"], p["name"]))
```

<a id="m780"></a>
### 780. Search insert position
Saralangan massivda qiymat bo'lsa indeksini, bo'lmasa qo'yilishi kerak bo'lgan o'rnini qaytaradi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const searchInsert = (arr, target) => {
  let lo = 0, hi = arr.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] < target) lo = mid + 1;
    else hi = mid;
  }
  return lo;
};
```
**PHP**
```php
function searchInsert(array $arr, int $target): int {
    $lo = 0; $hi = count($arr);
    while ($lo < $hi) {
        $mid = intdiv($lo + $hi, 2);
        if ($arr[$mid] < $target) $lo = $mid + 1;
        else $hi = $mid;
    }
    return $lo;
}
```
**Python**
```python
def search_insert(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

<a id="m781"></a>
### 781. Find peak element
Qo'shnilaridan katta bo'lgan istalgan "cho'qqi" indeksini O(log n) da topadi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const findPeak = (arr) => {
  let lo = 0, hi = arr.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] < arr[mid + 1]) lo = mid + 1;
    else hi = mid;
  }
  return lo;
};
```
**Python**
```python
def find_peak(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

<a id="m782"></a>
### 782. Find minimum in rotated sorted array
Aylantirilgan (rotated) takrorlanmas saralangan massivdagi minimal elementni topadi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const findMin = (arr) => {
  let lo = 0, hi = arr.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] > arr[hi]) lo = mid + 1;
    else hi = mid;
  }
  return arr[lo];
};
```
**PHP**
```php
function findMin(array $arr): int {
    $lo = 0; $hi = count($arr) - 1;
    while ($lo < $hi) {
        $mid = intdiv($lo + $hi, 2);
        if ($arr[$mid] > $arr[$hi]) $lo = $mid + 1;
        else $hi = $mid;
    }
    return $arr[$lo];
}
```
**Python**
```python
def find_min(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] > arr[hi]:
            lo = mid + 1
        else:
            hi = mid
    return arr[lo]
```

<a id="m783"></a>
### 783. Search in rotated sorted array II (dublikatlar bilan)
Aylantirilgan, dublikatli massivda qiymat borligini topadi; teng qiymatlarda chegaralarni qisqartiradi.
`⏱ O(log n) o'rtacha, O(n) eng yomon · 💾 O(1)`

**JS**
```js
const searchRotatedII = (arr, target) => {
  let lo = 0, hi = arr.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] === target) return true;
    if (arr[lo] === arr[mid] && arr[mid] === arr[hi]) { lo++; hi--; }
    else if (arr[lo] <= arr[mid]) {
      if (arr[lo] <= target && target < arr[mid]) hi = mid - 1;
      else lo = mid + 1;
    } else {
      if (arr[mid] < target && target <= arr[hi]) lo = mid + 1;
      else hi = mid - 1;
    }
  }
  return false;
};
```
**Python**
```python
def search_rotated_ii(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return True
        if arr[lo] == arr[mid] == arr[hi]:
            lo += 1
            hi -= 1
        elif arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

<a id="m784"></a>
### 784. Nth root (javob ustida binary search)
n-darajali ildizni butun aniqlikda qidiradi; mid^n ni m bilan solishtiradi.
`⏱ O(log m × n) · 💾 O(1)`

**JS**
```js
const nthRoot = (n, m) => {
  let lo = 1, hi = m;
  const pow = (x) => {
    let r = 1;
    for (let i = 0; i < n; i++) { r *= x; if (r > m) return Infinity; }
    return r;
  };
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const p = pow(mid);
    if (p === m) return mid;
    if (p < m) lo = mid + 1; else hi = mid - 1;
  }
  return -1;
};
```
**Python**
```python
def nth_root(n, m):
    def power(x):
        r = 1
        for _ in range(n):
            r *= x
            if r > m:
                return float("inf")
        return r
    lo, hi = 1, m
    while lo <= hi:
        mid = (lo + hi) // 2
        p = power(mid)
        if p == m:
            return mid
        if p < m:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

<a id="m785"></a>
### 785. Koko eating bananas (javob ustida binary search)
H soatda hamma uyumlarni yeyish uchun minimal yeyish tezligi k ni topadi.
`⏱ O(n log max) · 💾 O(1)`

**JS**
```js
const minEatingSpeed = (piles, h) => {
  const hours = (k) => piles.reduce((s, p) => s + Math.ceil(p / k), 0);
  let lo = 1, hi = Math.max(...piles);
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (hours(mid) <= h) hi = mid;
    else lo = mid + 1;
  }
  return lo;
};
```
**PHP**
```php
function minEatingSpeed(array $piles, int $h): int {
    $hours = fn($k) => array_sum(array_map(fn($p) => intdiv($p + $k - 1, $k), $piles));
    $lo = 1; $hi = max($piles);
    while ($lo < $hi) {
        $mid = intdiv($lo + $hi, 2);
        if ($hours($mid) <= $h) $hi = $mid;
        else $lo = $mid + 1;
    }
    return $lo;
}
```
**Python**
```python
from math import ceil

def min_eating_speed(piles, h):
    def hours(k):
        return sum(ceil(p / k) for p in piles)
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

<a id="m786"></a>
### 786. Capacity to ship packages in D days (BS)
D kunda hamma yuklarni jo'natish uchun kemaning minimal sig'imini topadi.
`⏱ O(n log sum) · 💾 O(1)`

**JS**
```js
const shipWithinDays = (weights, days) => {
  const need = (cap) => {
    let d = 1, cur = 0;
    for (const w of weights) {
      if (cur + w > cap) { d++; cur = 0; }
      cur += w;
    }
    return d;
  };
  let lo = Math.max(...weights), hi = weights.reduce((a, b) => a + b, 0);
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (need(mid) <= days) hi = mid;
    else lo = mid + 1;
  }
  return lo;
};
```
**Python**
```python
def ship_within_days(weights, days):
    def need(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = 0
            cur += w
        return d
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

<a id="m787"></a>
### 787. Split array largest sum (BS)
Massivni m bo'lakka bo'lganda bo'laklar yig'indilarining maksimumini minimallashtiradi.
`⏱ O(n log sum) · 💾 O(1)`

**JS**
```js
const splitArray = (nums, m) => {
  const parts = (cap) => {
    let cnt = 1, cur = 0;
    for (const x of nums) {
      if (cur + x > cap) { cnt++; cur = 0; }
      cur += x;
    }
    return cnt;
  };
  let lo = Math.max(...nums), hi = nums.reduce((a, b) => a + b, 0);
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (parts(mid) <= m) hi = mid;
    else lo = mid + 1;
  }
  return lo;
};
```
**Python**
```python
def split_array(nums, m):
    def parts(cap):
        cnt, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                cnt += 1
                cur = 0
            cur += x
        return cnt
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if parts(mid) <= m:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

<a id="m788"></a>
### 788. Minimum days to make m bouquets (BS)
Har biri k qo'shni guldan iborat m ta guldasta yig'ish uchun minimal kunlar sonini topadi.
`⏱ O(n log max) · 💾 O(1)`

**JS**
```js
const minDays = (bloom, m, k) => {
  if (m * k > bloom.length) return -1;
  const canMake = (day) => {
    let made = 0, run = 0;
    for (const b of bloom) {
      if (b <= day) { run++; if (run === k) { made++; run = 0; } }
      else run = 0;
    }
    return made >= m;
  };
  let lo = Math.min(...bloom), hi = Math.max(...bloom);
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (canMake(mid)) hi = mid;
    else lo = mid + 1;
  }
  return lo;
};
```
**Python**
```python
def min_days(bloom, m, k):
    if m * k > len(bloom):
        return -1
    def can_make(day):
        made = run = 0
        for b in bloom:
            if b <= day:
                run += 1
                if run == k:
                    made += 1
                    run = 0
            else:
                run = 0
        return made >= m
    lo, hi = min(bloom), max(bloom)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_make(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

<a id="m789"></a>
### 789. Kth smallest pair distance (BS)
Barcha juftliklar orasidagi |a[i]-a[j]| masofalar ichidan k-chi eng kichigini topadi.
`⏱ O(n log n + n log max) · 💾 O(1)`

**JS**
```js
const smallestDistancePair = (nums, k) => {
  nums.sort((a, b) => a - b);
  const count = (d) => {
    let c = 0, lo = 0;
    for (let hi = 0; hi < nums.length; hi++) {
      while (nums[hi] - nums[lo] > d) lo++;
      c += hi - lo;
    }
    return c;
  };
  let lo = 0, hi = nums[nums.length - 1] - nums[0];
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (count(mid) >= k) hi = mid;
    else lo = mid + 1;
  }
  return lo;
};
```
**Python**
```python
def smallest_distance_pair(nums, k):
    nums.sort()
    def count(d):
        c = lo = 0
        for hi in range(len(nums)):
            while nums[hi] - nums[lo] > d:
                lo += 1
            c += hi - lo
        return c
    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

<a id="m790"></a>
### 790. Median of two sorted arrays (BS)
Ikki saralangan massivning umumiy medianasini O(log(min(m,n))) da bo'lish nuqtasini qidirib topadi.
`⏱ O(log(min(m, n))) · 💾 O(1)`

**Python**
```python
def find_median_sorted(a, b):
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = (m + n + 1) // 2 - i
        al = a[i - 1] if i > 0 else float("-inf")
        ar = a[i] if i < m else float("inf")
        bl = b[j - 1] if j > 0 else float("-inf")
        br = b[j] if j < n else float("inf")
        if al <= br and bl <= ar:
            if (m + n) % 2:
                return float(max(al, bl))
            return (max(al, bl) + min(ar, br)) / 2
        if al > br:
            hi = i - 1
        else:
            lo = i + 1
    return 0.0
```
**JS**
```js
const findMedianSorted = (a, b) => {
  if (a.length > b.length) [a, b] = [b, a];
  const m = a.length, n = b.length;
  let lo = 0, hi = m;
  while (lo <= hi) {
    const i = (lo + hi) >> 1;
    const j = ((m + n + 1) >> 1) - i;
    const al = i > 0 ? a[i - 1] : -Infinity;
    const ar = i < m ? a[i] : Infinity;
    const bl = j > 0 ? b[j - 1] : -Infinity;
    const br = j < n ? b[j] : Infinity;
    if (al <= br && bl <= ar)
      return (m + n) % 2 ? Math.max(al, bl) : (Math.max(al, bl) + Math.min(ar, br)) / 2;
    if (al > br) hi = i - 1;
    else lo = i + 1;
  }
  return 0;
};
```

<a id="m791"></a>
### 791. Aggressive cows / minimaks masofa (BS)
c ta sigirni oxirlarga shunday joylashtirish kerakki, eng yaqin ikki sigir orasidagi masofa maksimal bo'lsin.
`⏱ O(n log n + n log range) · 💾 O(1)`

**JS**
```js
const aggressiveCows = (stalls, cows) => {
  stalls.sort((a, b) => a - b);
  const canPlace = (dist) => {
    let count = 1, last = stalls[0];
    for (const s of stalls)
      if (s - last >= dist) { count++; last = s; }
    return count >= cows;
  };
  let lo = 0, hi = stalls[stalls.length - 1] - stalls[0], ans = 0;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (canPlace(mid)) { ans = mid; lo = mid + 1; }
    else hi = mid - 1;
  }
  return ans;
};
```
**Python**
```python
def aggressive_cows(stalls, cows):
    stalls.sort()
    def can_place(dist):
        count, last = 1, stalls[0]
        for s in stalls:
            if s - last >= dist:
                count += 1
                last = s
        return count >= cows
    lo, hi, ans = 0, stalls[-1] - stalls[0], 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_place(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans
```

<a id="m792"></a>
### 792. Allocate minimum pages (BS)
Kitoblarni m talabaga bo'lganda eng ko'p sahifa olgan talabaning yukini minimallashtiradi.
`⏱ O(n log sum) · 💾 O(1)`

**JS**
```js
const allocateBooks = (books, students) => {
  if (students > books.length) return -1;
  const need = (limit) => {
    let cnt = 1, cur = 0;
    for (const b of books) {
      if (cur + b > limit) { cnt++; cur = 0; }
      cur += b;
    }
    return cnt;
  };
  let lo = Math.max(...books), hi = books.reduce((a, b) => a + b, 0);
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (need(mid) <= students) hi = mid;
    else lo = mid + 1;
  }
  return lo;
};
```
**Python**
```python
def allocate_books(books, students):
    if students > len(books):
        return -1
    def need(limit):
        cnt, cur = 1, 0
        for b in books:
            if cur + b > limit:
                cnt += 1
                cur = 0
            cur += b
        return cnt
    lo, hi = max(books), sum(books)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= students:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

<a id="m793"></a>
### 793. Peak index in mountain array
"Tog'" massivida (avval o'sib, keyin kamayuvchi) cho'qqi indeksini O(log n) da topadi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const peakIndexInMountain = (arr) => {
  let lo = 1, hi = arr.length - 2;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] < arr[mid + 1]) lo = mid + 1;
    else hi = mid;
  }
  return lo;
};
```
**Python**
```python
def peak_index_in_mountain(arr):
    lo, hi = 1, len(arr) - 2
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

<a id="m794"></a>
### 794. Single element in a sorted array (BS)
Har element ikki marta uchraydigan saralangan massivda yagona toq elementni O(log n) da topadi.
`⏱ O(log n) · 💾 O(1)`

**JS**
```js
const singleNonDuplicate = (arr) => {
  let lo = 0, hi = arr.length - 1;
  while (lo < hi) {
    let mid = (lo + hi) >> 1;
    if (mid % 2 === 1) mid--;
    if (arr[mid] === arr[mid + 1]) lo = mid + 2;
    else hi = mid;
  }
  return arr[lo];
};
```
**PHP**
```php
function singleNonDuplicate(array $arr): int {
    $lo = 0; $hi = count($arr) - 1;
    while ($lo < $hi) {
        $mid = intdiv($lo + $hi, 2);
        if ($mid % 2 === 1) $mid--;
        if ($arr[$mid] === $arr[$mid + 1]) $lo = $mid + 2;
        else $hi = $mid;
    }
    return $arr[$lo];
}
```
**Python**
```python
def single_non_duplicate(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2 == 1:
            mid -= 1
        if arr[mid] == arr[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return arr[lo]
```

<a id="m795"></a>
### 795. Find the duplicate number (Floyd tsikl usuli)
1..n oralig'idagi n+1 sondan iborat massivdagi yagona takrorlanuvchini massivni o'zgartirmasdan topadi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const findDuplicate = (nums) => {
  let slow = nums[0], fast = nums[0];
  do { slow = nums[slow]; fast = nums[nums[fast]]; } while (slow !== fast);
  slow = nums[0];
  while (slow !== fast) { slow = nums[slow]; fast = nums[fast]; }
  return slow;
};
```
**Python**
```python
def find_duplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

<a id="m796"></a>
### 796. H-index (saralash)
Tadqiqotchining h-indeksini topadi: h ta maqola kamida h martadan iqtibos qilingan.
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const hIndex = (citations) => {
  citations.sort((a, b) => b - a);
  let h = 0;
  while (h < citations.length && citations[h] > h) h++;
  return h;
};
```
**PHP**
```php
function hIndex(array $citations): int {
    rsort($citations);
    $h = 0;
    while ($h < count($citations) && $citations[$h] > $h) $h++;
    return $h;
}
```
**Python**
```python
def h_index(citations):
    citations.sort(reverse=True)
    h = 0
    while h < len(citations) and citations[h] > h:
        h += 1
    return h
```
