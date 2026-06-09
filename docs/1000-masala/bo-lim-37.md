<a id="b37"></a>
# 37-bo'lim: Greedy (qo'shimcha)

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Bu bo'lim oldingi greedy bo'limini to'ldiradi. Bu yerda ochko'z (greedy) yondashuvning
> turli ko'rinishlari yig'ilgan: saralashga asoslangan moslashtirishlar (assign cookies, boats,
> two city), interval optimallashtirishlari (non-overlapping, minimum arrows, meeting rooms,
> minimum platforms, maximum events), raqamlar ustidagi ochko'z qarorlar (remove k digits,
> monotone increasing digits, largest number), almashtirishga oid masalalar (advantage shuffle,
> minimum swaps) va klassik Huffman kodlash. Har bir masalada lokal-optimal tanlovning
> global-optimalga olib kelishini ko'rsatuvchi g'oya yotadi — odatda avval to'g'ri tartibda
> saralash yoki priority queue ishlatish hal qiluvchi qadam bo'ladi.

<a id="m822"></a>
### 822. Bolalarga pechene ulashish (assign cookies)
Har bola ochligi g[i], har pechene o'lchami s[j]. Maksimal qanoatlangan bolalar sonini top.
`⏱ O(n log n + m log m) · 💾 O(1)`

**JS**
```js
const findContentChildren = (g, s) => {
  g.sort((a, b) => a - b);
  s.sort((a, b) => a - b);
  let i = 0, j = 0;
  while (i < g.length && j < s.length) {
    if (s[j] >= g[i]) i++;
    j++;
  }
  return i;
};
```
**PHP**
```php
function findContentChildren(array $g, array $s): int {
    sort($g);
    sort($s);
    $i = 0; $j = 0;
    while ($i < count($g) && $j < count($s)) {
        if ($s[$j] >= $g[$i]) $i++;
        $j++;
    }
    return $i;
}
```
**Python**
```python
def find_content_children(g, s):
    g.sort()
    s.sort()
    i = j = 0
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:
            i += 1
        j += 1
    return i
```

<a id="m823"></a>
### 823. Limonad pulini qaytarish (lemonade change)
Har bir limonad 5$. Mijozlar 5/10/20$ beradi; qaytim bera olsang true.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const lemonadeChange = (bills) => {
  let five = 0, ten = 0;
  for (const b of bills) {
    if (b === 5) five++;
    else if (b === 10) { if (!five) return false; five--; ten++; }
    else {
      if (ten && five) { ten--; five--; }
      else if (five >= 3) five -= 3;
      else return false;
    }
  }
  return true;
};
```
**PHP**
```php
function lemonadeChange(array $bills): bool {
    $five = 0; $ten = 0;
    foreach ($bills as $b) {
        if ($b === 5) $five++;
        elseif ($b === 10) { if (!$five) return false; $five--; $ten++; }
        else {
            if ($ten && $five) { $ten--; $five--; }
            elseif ($five >= 3) $five -= 3;
            else return false;
        }
    }
    return true;
}
```
**Python**
```python
def lemonade_change(bills):
    five = ten = 0
    for b in bills:
        if b == 5:
            five += 1
        elif b == 10:
            if not five:
                return False
            five -= 1
            ten += 1
        else:
            if ten and five:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True
```

<a id="m824"></a>
### 824. Aksiyani sotib olish/sotish II (best time to buy and sell stock II)
Cheksiz tranzaksiya; har ko'tarilishdan foyda ol. Jami maksimal foydani top.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const maxProfit = (prices) => {
  let profit = 0;
  for (let i = 1; i < prices.length; i++)
    if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];
  return profit;
};
```
**PHP**
```php
function maxProfit(array $prices): int {
    $profit = 0;
    for ($i = 1; $i < count($prices); $i++)
        if ($prices[$i] > $prices[$i - 1]) $profit += $prices[$i] - $prices[$i - 1];
    return $profit;
}
```
**Python**
```python
def max_profit(prices):
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
```

<a id="m825"></a>
### 825. Bolalarga konfet ulashish (candy)
Har bolaga ≥1 konfet; baholi qo'shnidan ko'ra ko'p oladi. Minimal jami konfet.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const candy = (ratings) => {
  const n = ratings.length;
  const c = Array(n).fill(1);
  for (let i = 1; i < n; i++)
    if (ratings[i] > ratings[i - 1]) c[i] = c[i - 1] + 1;
  for (let i = n - 2; i >= 0; i--)
    if (ratings[i] > ratings[i + 1]) c[i] = Math.max(c[i], c[i + 1] + 1);
  return c.reduce((a, b) => a + b, 0);
};
```
**PHP**
```php
function candy(array $ratings): int {
    $n = count($ratings);
    $c = array_fill(0, $n, 1);
    for ($i = 1; $i < $n; $i++)
        if ($ratings[$i] > $ratings[$i - 1]) $c[$i] = $c[$i - 1] + 1;
    for ($i = $n - 2; $i >= 0; $i--)
        if ($ratings[$i] > $ratings[$i + 1]) $c[$i] = max($c[$i], $c[$i + 1] + 1);
    return array_sum($c);
}
```
**Python**
```python
def candy(ratings):
    n = len(ratings)
    c = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)
```

<a id="m826"></a>
### 826. Kesishmaydigan intervallar — minimal o'chirish (non-overlapping intervals)
Intervallarni kesishmaydigan qilish uchun minimal nechta o'chirish kerak.
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const eraseOverlapIntervals = (intervals) => {
  intervals.sort((a, b) => a[1] - b[1]);
  let count = 0, end = -Infinity;
  for (const [s, e] of intervals) {
    if (s >= end) end = e;
    else count++;
  }
  return count;
};
```
**PHP**
```php
function eraseOverlapIntervals(array $intervals): int {
    usort($intervals, fn($a, $b) => $a[1] <=> $b[1]);
    $count = 0; $end = PHP_INT_MIN;
    foreach ($intervals as [$s, $e]) {
        if ($s >= $end) $end = $e;
        else $count++;
    }
    return $count;
}
```
**Python**
```python
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    count = 0
    end = float("-inf")
    for s, e in intervals:
        if s >= end:
            end = e
        else:
            count += 1
    return count
```

<a id="m827"></a>
### 827. Sharlarni yorish uchun minimal o'qlar (minimum arrows to burst balloons)
Har shar [start, end] oraliqda. Vertikal o'q kesishgan barchasini yoradi. Minimal o'q soni.
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const findMinArrowShots = (points) => {
  if (!points.length) return 0;
  points.sort((a, b) => a[1] - b[1]);
  let arrows = 1, end = points[0][1];
  for (const [s, e] of points) {
    if (s > end) { arrows++; end = e; }
  }
  return arrows;
};
```
**PHP**
```php
function findMinArrowShots(array $points): int {
    if (!$points) return 0;
    usort($points, fn($a, $b) => $a[1] <=> $b[1]);
    $arrows = 1; $end = $points[0][1];
    foreach ($points as [$s, $e]) {
        if ($s > $end) { $arrows++; $end = $e; }
    }
    return $arrows;
}
```
**Python**
```python
def find_min_arrow_shots(points):
    if not points:
        return 0
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    for s, e in points:
        if s > end:
            arrows += 1
            end = e
    return arrows
```

<a id="m828"></a>
### 828. Barcha uchrashuvlarga ulgurish mumkinmi (can attend meetings)
Intervallar berilgan; hech biri kesishmasa true (bir vaqtda bitta uchrashuv).
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const canAttendMeetings = (intervals) => {
  intervals.sort((a, b) => a[0] - b[0]);
  for (let i = 1; i < intervals.length; i++)
    if (intervals[i][0] < intervals[i - 1][1]) return false;
  return true;
};
```
**PHP**
```php
function canAttendMeetings(array $intervals): bool {
    usort($intervals, fn($a, $b) => $a[0] <=> $b[0]);
    for ($i = 1; $i < count($intervals); $i++)
        if ($intervals[$i][0] < $intervals[$i - 1][1]) return false;
    return true;
}
```
**Python**
```python
def can_attend_meetings(intervals):
    intervals.sort()
    return all(intervals[i][0] >= intervals[i - 1][1] for i in range(1, len(intervals)))
```

<a id="m829"></a>
### 829. Bo'y bo'yicha navbatni qayta tiklash (queue reconstruction by height)
Har odam [h, k]: oldida bo'yi ≥h bo'lgan aniq k kishi. Navbatni tikla.
`⏱ O(n²) · 💾 O(n)`

**JS**
```js
const reconstructQueue = (people) => {
  people.sort((a, b) => b[0] - a[0] || a[1] - b[1]);
  const res = [];
  for (const p of people) res.splice(p[1], 0, p);
  return res;
};
```
**PHP**
```php
function reconstructQueue(array $people): array {
    usort($people, fn($a, $b) => $b[0] <=> $a[0] ?: $a[1] <=> $b[1]);
    $res = [];
    foreach ($people as $p) array_splice($res, $p[1], 0, [$p]);
    return $res;
}
```
**Python**
```python
def reconstruct_queue(people):
    people.sort(key=lambda p: (-p[0], p[1]))
    res = []
    for p in people:
        res.insert(p[1], p)
    return res
```

<a id="m830"></a>
### 830. Odamlarni qutqarish uchun qayiqlar (boats to save people)
Har qayiq ≤2 kishi va og'irligi ≤limit. Minimal qayiq sonini top.
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const numRescueBoats = (people, limit) => {
  people.sort((a, b) => a - b);
  let i = 0, j = people.length - 1, boats = 0;
  while (i <= j) {
    if (people[i] + people[j] <= limit) i++;
    j--;
    boats++;
  }
  return boats;
};
```
**PHP**
```php
function numRescueBoats(array $people, int $limit): int {
    sort($people);
    $i = 0; $j = count($people) - 1; $boats = 0;
    while ($i <= $j) {
        if ($people[$i] + $people[$j] <= $limit) $i++;
        $j--;
        $boats++;
    }
    return $boats;
}
```
**Python**
```python
def num_rescue_boats(people, limit):
    people.sort()
    i, j, boats = 0, len(people) - 1, 0
    while i <= j:
        if people[i] + people[j] <= limit:
            i += 1
        j -= 1
        boats += 1
    return boats
```

<a id="m831"></a>
### 831. Ikki shaharga jo'natish (two city scheduling)
2n odam; costs[i]=[aCity, bCity]. Yarmi A, yarmi B shaharga. Minimal jami narx.
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const twoCitySchedCost = (costs) => {
  costs.sort((x, y) => (x[0] - x[1]) - (y[0] - y[1]));
  const n = costs.length / 2;
  let total = 0;
  for (let i = 0; i < costs.length; i++)
    total += i < n ? costs[i][0] : costs[i][1];
  return total;
};
```
**PHP**
```php
function twoCitySchedCost(array $costs): int {
    usort($costs, fn($x, $y) => ($x[0] - $x[1]) <=> ($y[0] - $y[1]));
    $n = count($costs) / 2;
    $total = 0;
    foreach ($costs as $i => $c)
        $total += $i < $n ? $c[0] : $c[1];
    return $total;
}
```
**Python**
```python
def two_city_sched_cost(costs):
    costs.sort(key=lambda c: c[0] - c[1])
    n = len(costs) // 2
    return sum(c[0] for c in costs[:n]) + sum(c[1] for c in costs[n:])
```

<a id="m832"></a>
### 832. Tebranuvchi ketma-ketlik (wiggle subsequence)
Eng uzun ketma-ketlik uzunligi: ayirmalari navbatma-navbat musbat/manfiy.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const wiggleMaxLength = (nums) => {
  if (nums.length < 2) return nums.length;
  let up = 1, down = 1;
  for (let i = 1; i < nums.length; i++) {
    if (nums[i] > nums[i - 1]) up = down + 1;
    else if (nums[i] < nums[i - 1]) down = up + 1;
  }
  return Math.max(up, down);
};
```
**PHP**
```php
function wiggleMaxLength(array $nums): int {
    if (count($nums) < 2) return count($nums);
    $up = 1; $down = 1;
    for ($i = 1; $i < count($nums); $i++) {
        if ($nums[$i] > $nums[$i - 1]) $up = $down + 1;
        elseif ($nums[$i] < $nums[$i - 1]) $down = $up + 1;
    }
    return max($up, $down);
}
```
**Python**
```python
def wiggle_max_length(nums):
    if len(nums) < 2:
        return len(nums)
    up = down = 1
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1
    return max(up, down)
```

<a id="m833"></a>
### 833. Monoton o'suvchi raqamlar (monotone increasing digits)
n dan ≤ va raqamlari kamaymaydigan eng katta sonni top.
`⏱ O(d) · 💾 O(d)`

**JS**
```js
const monotoneIncreasingDigits = (n) => {
  const d = String(n).split("").map(Number);
  let mark = d.length;
  for (let i = d.length - 1; i > 0; i--) {
    if (d[i - 1] > d[i]) { d[i - 1]--; mark = i; }
  }
  for (let i = mark; i < d.length; i++) d[i] = 9;
  return Number(d.join(""));
};
```
**PHP**
```php
function monotoneIncreasingDigits(int $n): int {
    $d = str_split((string)$n);
    $mark = count($d);
    for ($i = count($d) - 1; $i > 0; $i--) {
        if ($d[$i - 1] > $d[$i]) { $d[$i - 1]--; $mark = $i; }
    }
    for ($i = $mark; $i < count($d); $i++) $d[$i] = '9';
    return (int)implode('', $d);
}
```
**Python**
```python
def monotone_increasing_digits(n):
    d = list(str(n))
    mark = len(d)
    for i in range(len(d) - 1, 0, -1):
        if d[i - 1] > d[i]:
            d[i - 1] = str(int(d[i - 1]) - 1)
            mark = i
    for i in range(mark, len(d)):
        d[i] = "9"
    return int("".join(d))
```

<a id="m834"></a>
### 834. K ta raqamni o'chirib eng kichik son (remove k digits)
num satridan k ta raqam o'chirib eng kichik sonni hosil qil (yetakchi nollarsiz).
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const removeKdigits = (num, k) => {
  const stack = [];
  for (const c of num) {
    while (k && stack.length && stack[stack.length - 1] > c) { stack.pop(); k--; }
    stack.push(c);
  }
  while (k--) stack.pop();
  return stack.join("").replace(/^0+/, "") || "0";
};
```
**PHP**
```php
function removeKdigits(string $num, int $k): string {
    $stack = [];
    foreach (str_split($num) as $c) {
        while ($k && $stack && end($stack) > $c) { array_pop($stack); $k--; }
        $stack[] = $c;
    }
    while ($k-- > 0) array_pop($stack);
    $res = ltrim(implode('', $stack), '0');
    return $res === '' ? '0' : $res;
}
```
**Python**
```python
def remove_k_digits(num, k):
    stack = []
    for c in num:
        while k and stack and stack[-1] > c:
            stack.pop()
            k -= 1
        stack.append(c)
    stack = stack[:len(stack) - k] if k else stack
    return "".join(stack).lstrip("0") or "0"
```

<a id="m835"></a>
### 835. Yuk mashinasidagi maksimal qutilar (maximum units on a truck)
boxTypes[i]=[soni, birlik]; truck sig'imi truckSize. Maksimal birlik yig'.
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const maximumUnits = (boxTypes, truckSize) => {
  boxTypes.sort((a, b) => b[1] - a[1]);
  let units = 0;
  for (const [cnt, u] of boxTypes) {
    const take = Math.min(cnt, truckSize);
    units += take * u;
    truckSize -= take;
    if (!truckSize) break;
  }
  return units;
};
```
**PHP**
```php
function maximumUnits(array $boxTypes, int $truckSize): int {
    usort($boxTypes, fn($a, $b) => $b[1] <=> $a[1]);
    $units = 0;
    foreach ($boxTypes as [$cnt, $u]) {
        $take = min($cnt, $truckSize);
        $units += $take * $u;
        $truckSize -= $take;
        if (!$truckSize) break;
    }
    return $units;
}
```
**Python**
```python
def maximum_units(box_types, truck_size):
    box_types.sort(key=lambda b: -b[1])
    units = 0
    for cnt, u in box_types:
        take = min(cnt, truck_size)
        units += take * u
        truck_size -= take
        if not truck_size:
            break
    return units
```

<a id="m836"></a>
### 836. Ustunlik aralashtirish (advantage shuffle)
A ni shunday qayta tartibla: A[i] > B[i] bo'lgan pozitsiyalar soni maksimal bo'lsin.
`⏱ O(n log n) · 💾 O(n)`

**JS**
```js
const advantageCount = (A, B) => {
  A.sort((a, b) => a - b);
  const idx = B.map((v, i) => i).sort((a, b) => B[a] - B[b]);
  const res = Array(A.length);
  let lo = 0, hi = A.length - 1;
  for (let i = A.length - 1; i >= 0; i--) {
    if (A[hi] > B[idx[i]]) res[idx[i]] = A[hi--];
    else res[idx[i]] = A[lo++];
  }
  return res;
};
```
**PHP**
```php
function advantageCount(array $A, array $B): array {
    sort($A);
    $idx = range(0, count($B) - 1);
    usort($idx, fn($a, $b) => $B[$a] <=> $B[$b]);
    $res = array_fill(0, count($A), 0);
    $lo = 0; $hi = count($A) - 1;
    for ($i = count($A) - 1; $i >= 0; $i--) {
        if ($A[$hi] > $B[$idx[$i]]) $res[$idx[$i]] = $A[$hi--];
        else $res[$idx[$i]] = $A[$lo++];
    }
    return $res;
}
```
**Python**
```python
def advantage_count(A, B):
    A.sort()
    idx = sorted(range(len(B)), key=lambda i: B[i])
    res = [0] * len(A)
    lo, hi = 0, len(A) - 1
    for i in range(len(A) - 1, -1, -1):
        if A[hi] > B[idx[i]]:
            res[idx[i]] = A[hi]
            hi -= 1
        else:
            res[idx[i]] = A[lo]
            lo += 1
    return res
```

<a id="m837"></a>
### 837. Chastotalarni noyob qilish uchun minimal o'chirish (minimum deletions to make frequencies unique)
Belgilar chastotalari hammasi turlicha bo'lishi uchun minimal o'chirishlar soni.
`⏱ O(n + k log k) · 💾 O(k)`

**JS**
```js
const minDeletions = (s) => {
  const freq = {};
  for (const c of s) freq[c] = (freq[c] || 0) + 1;
  const used = new Set();
  let deletions = 0;
  for (let f of Object.values(freq)) {
    while (f > 0 && used.has(f)) { f--; deletions++; }
    if (f > 0) used.add(f);
  }
  return deletions;
};
```
**PHP**
```php
function minDeletions(string $s): int {
    $freq = array_count_values(str_split($s));
    $used = [];
    $deletions = 0;
    foreach ($freq as $f) {
        while ($f > 0 && isset($used[$f])) { $f--; $deletions++; }
        if ($f > 0) $used[$f] = true;
    }
    return $deletions;
}
```
**Python**
```python
from collections import Counter

def min_deletions(s):
    used = set()
    deletions = 0
    for f in Counter(s).values():
        while f > 0 and f in used:
            f -= 1
            deletions += 1
        if f > 0:
            used.add(f)
    return deletions
```

<a id="m838"></a>
### 838. Qatnashilgan maksimal tadbirlar (maximum events attended)
events[i]=[start, end]. Har kuni bitta tadbir. Maksimal nechta tadbirga ulgurasan.
`⏱ O(n log n) · 💾 O(n)`

**JS**
```js
const maxEvents = (events) => {
  events.sort((a, b) => a[0] - b[0]);
  const heap = []; // min-heap of end days (oddiy massiv + sort)
  let day = 0, i = 0, count = 0;
  const maxDay = Math.max(...events.map(e => e[1]));
  for (day = 1; day <= maxDay; day++) {
    while (i < events.length && events[i][0] === day) heap.push(events[i++][1]);
    heap.sort((a, b) => a - b);
    while (heap.length && heap[0] < day) heap.shift();
    if (heap.length) { heap.shift(); count++; }
  }
  return count;
};
```
**PHP**
```php
function maxEvents(array $events): int {
    usort($events, fn($a, $b) => $a[0] <=> $b[0]);
    $heap = new SplMinHeap();
    $day = 0; $i = 0; $count = 0;
    $maxDay = max(array_column($events, 1));
    for ($day = 1; $day <= $maxDay; $day++) {
        while ($i < count($events) && $events[$i][0] === $day) $heap->insert($events[$i++][1]);
        while (!$heap->isEmpty() && $heap->top() < $day) $heap->extract();
        if (!$heap->isEmpty()) { $heap->extract(); $count++; }
    }
    return $count;
}
```
**Python**
```python
import heapq

def max_events(events):
    events.sort()
    heap = []
    i = count = 0
    max_day = max(e[1] for e in events)
    for day in range(1, max_day + 1):
        while i < len(events) and events[i][0] == day:
            heapq.heappush(heap, events[i][1])
            i += 1
        while heap and heap[0] < day:
            heapq.heappop(heap)
        if heap:
            heapq.heappop(heap)
            count += 1
    return count
```

<a id="m839"></a>
### 839. Eng katta son (largest number)
Manfiy bo'lmagan sonlardan ulanishida eng katta sonni hosil qil (maxsus saralash).
`⏱ O(n log n × L) · 💾 O(n)`

**JS**
```js
const largestNumber = (nums) => {
  const arr = nums.map(String).sort((a, b) => (b + a).localeCompare(a + b));
  return arr[0] === "0" ? "0" : arr.join("");
};
```
**PHP**
```php
function largestNumber(array $nums): string {
    $arr = array_map('strval', $nums);
    usort($arr, fn($a, $b) => strcmp($b . $a, $a . $b));
    return $arr[0] === '0' ? '0' : implode('', $arr);
}
```
**Python**
```python
from functools import cmp_to_key

def largest_number(nums):
    arr = sorted(map(str, nums), key=cmp_to_key(lambda a, b: (a + b < b + a) - (a + b > b + a)))
    return "0" if arr[0] == "0" else "".join(arr)
```

<a id="m840"></a>
### 840. Minimal platformalar (minimum platforms)
Poyezdlarning kelish/ketish vaqtlari berilgan. Bir vaqtda kerak bo'ladigan minimal platforma soni.
`⏱ O(n log n) · 💾 O(n)`

**JS**
```js
const minPlatforms = (arr, dep) => {
  arr.sort((a, b) => a - b);
  dep.sort((a, b) => a - b);
  let plat = 0, maxPlat = 0, i = 0, j = 0;
  while (i < arr.length) {
    if (arr[i] <= dep[j]) { plat++; i++; maxPlat = Math.max(maxPlat, plat); }
    else { plat--; j++; }
  }
  return maxPlat;
};
```
**PHP**
```php
function minPlatforms(array $arr, array $dep): int {
    sort($arr);
    sort($dep);
    $plat = 0; $maxPlat = 0; $i = 0; $j = 0;
    while ($i < count($arr)) {
        if ($arr[$i] <= $dep[$j]) { $plat++; $i++; $maxPlat = max($maxPlat, $plat); }
        else { $plat--; $j++; }
    }
    return $maxPlat;
}
```
**Python**
```python
def min_platforms(arr, dep):
    arr.sort()
    dep.sort()
    plat = max_plat = i = j = 0
    while i < len(arr):
        if arr[i] <= dep[j]:
            plat += 1
            i += 1
            max_plat = max(max_plat, plat)
        else:
            plat -= 1
            j += 1
    return max_plat
```

<a id="m841"></a>
### 841. Huffman kodlash (huffman coding)
Belgilar chastotalaridan optimal prefiksli kodlar daraxtini quradi; har belgi kod uzunligini qaytaradi.
`⏱ O(n log n) · 💾 O(n)`

**JS**
```js
const huffmanCodes = (freq) => {
  const nodes = Object.entries(freq).map(([ch, f]) => ({ ch, f, l: null, r: null }));
  while (nodes.length > 1) {
    nodes.sort((a, b) => a.f - b.f);
    const a = nodes.shift(), b = nodes.shift();
    nodes.push({ ch: null, f: a.f + b.f, l: a, r: b });
  }
  const codes = {};
  const walk = (node, code) => {
    if (node.ch !== null) { codes[node.ch] = code || "0"; return; }
    walk(node.l, code + "0");
    walk(node.r, code + "1");
  };
  if (nodes.length) walk(nodes[0], "");
  return codes;
};
```
**Python**
```python
import heapq
from itertools import count

def huffman_codes(freq):
    tie = count()
    heap = [[f, next(tie), ch, "", ""] for ch, f in freq.items()]
    heapq.heapify(heap)
    nodes = {ch: ["", None, None] for ch in freq}
    while len(heap) > 1:
        f1, _, c1, _, _ = heapq.heappop(heap)
        f2, _, c2, _, _ = heapq.heappop(heap)
        heapq.heappush(heap, [f1 + f2, next(tie), (c1, c2), "", ""])
    codes = {}

    def walk(node, code):
        if isinstance(node, tuple):
            walk(node[0], code + "0")
            walk(node[1], code + "1")
        else:
            codes[node] = code or "0"

    if heap:
        walk(heap[0][2], "")
    return codes
```

<a id="m842"></a>
### 842. K ta inkordan keyin maksimal yig'indi (maximize sum after k negations)
Massivda aniq k marta biror elementning ishorasini o'zgartirib, yig'indini maksimal qil.
`⏱ O(n log n) · 💾 O(1)`

**JS**
```js
const largestSumAfterKNegations = (nums, k) => {
  nums.sort((a, b) => a - b);
  for (let i = 0; i < nums.length && k > 0 && nums[i] < 0; i++) {
    nums[i] = -nums[i];
    k--;
  }
  const sum = nums.reduce((a, b) => a + b, 0);
  if (k % 2 === 1) return sum - 2 * Math.min(...nums);
  return sum;
};
```
**PHP**
```php
function largestSumAfterKNegations(array $nums, int $k): int {
    sort($nums);
    for ($i = 0; $i < count($nums) && $k > 0 && $nums[$i] < 0; $i++) {
        $nums[$i] = -$nums[$i];
        $k--;
    }
    $sum = array_sum($nums);
    if ($k % 2 === 1) return $sum - 2 * min($nums);
    return $sum;
}
```
**Python**
```python
def largest_sum_after_k_negations(nums, k):
    nums.sort()
    for i in range(len(nums)):
        if k > 0 and nums[i] < 0:
            nums[i] = -nums[i]
            k -= 1
        else:
            break
    total = sum(nums)
    if k % 2 == 1:
        return total - 2 * min(nums)
    return total
```

<a id="m843"></a>
### 843. Satrni balanslash uchun minimal almashtirishlar (minimum swaps to make string balanced)
Faqat '[' va ']' belgili satr. Har almashtirish ikki belgini joyini almashtiradi. Minimal almashtirish.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const minSwaps = (s) => {
  let balance = 0, maxNeg = 0;
  for (const c of s) {
    balance += c === "[" ? 1 : -1;
    maxNeg = Math.min(maxNeg, balance);
  }
  return Math.ceil(-maxNeg / 2);
};
```
**PHP**
```php
function minSwaps(string $s): int {
    $balance = 0; $maxNeg = 0;
    foreach (str_split($s) as $c) {
        $balance += $c === '[' ? 1 : -1;
        $maxNeg = min($maxNeg, $balance);
    }
    return (int)ceil(-$maxNeg / 2);
}
```
**Python**
```python
import math

def min_swaps(s):
    balance = 0
    max_neg = 0
    for c in s:
        balance += 1 if c == "[" else -1
        max_neg = min(max_neg, balance)
    return math.ceil(-max_neg / 2)
```

<a id="m844"></a>
### 844. Minimal o'suvchi ketma-ketliklarga ajratish (partition into minimum increasing subsequences)
Massivni qatorga keladigan eng kam sondagi qat'iy o'suvchi ketma-ketliklarga ajrat. Bu son — eng katta takror chastota (patience-ga teskari g'oya: eng ko'p takrorlangan qiymat).
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const minIncreasingPartitions = (nums) => {
  const freq = new Map();
  let maxFreq = 0;
  for (const x of nums) {
    const f = (freq.get(x) || 0) + 1;
    freq.set(x, f);
    maxFreq = Math.max(maxFreq, f);
  }
  return maxFreq;
};
```
**PHP**
```php
function minIncreasingPartitions(array $nums): int {
    $freq = [];
    $maxFreq = 0;
    foreach ($nums as $x) {
        $freq[$x] = ($freq[$x] ?? 0) + 1;
        $maxFreq = max($maxFreq, $freq[$x]);
    }
    return $maxFreq;
}
```
**Python**
```python
from collections import Counter

def min_increasing_partitions(nums):
    return max(Counter(nums).values(), default=0)
```

<a id="m845"></a>
### 845. Chiplarni ko'chirishning minimal narxi (minimum cost to move chips)
Pozitsiyalar berilgan. 2 ga siljish bepul, 1 ga siljish narxi 1. Hamma chipni bir joyga yig'.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const minCostToMoveChips = (position) => {
  let odd = 0, even = 0;
  for (const p of position) {
    if (p % 2 === 0) even++;
    else odd++;
  }
  return Math.min(odd, even);
};
```
**PHP**
```php
function minCostToMoveChips(array $position): int {
    $odd = 0; $even = 0;
    foreach ($position as $p) {
        if ($p % 2 === 0) $even++;
        else $odd++;
    }
    return min($odd, $even);
}
```
**Python**
```python
def min_cost_to_move_chips(position):
    odd = sum(p % 2 for p in position)
    return min(odd, len(position) - odd)
```

<a id="m846"></a>
### 846. Matritsani ag'darishdan keyingi maksimal ball (score after flipping matrix)
Binar matritsada qatorlar/ustunlarni teskarilab (0↔1), har qatorni ikkilik son sifatida o'qib, jami ballni maksimal qil.
`⏱ O(m × n) · 💾 O(1)`

**JS**
```js
const matrixScore = (grid) => {
  const m = grid.length, n = grid[0].length;
  let score = m * (1 << (n - 1));
  for (let j = 1; j < n; j++) {
    let ones = 0;
    for (let i = 0; i < m; i++)
      ones += grid[i][j] === grid[i][0] ? 1 : 0;
    score += Math.max(ones, m - ones) * (1 << (n - 1 - j));
  }
  return score;
};
```
**PHP**
```php
function matrixScore(array $grid): int {
    $m = count($grid); $n = count($grid[0]);
    $score = $m * (1 << ($n - 1));
    for ($j = 1; $j < $n; $j++) {
        $ones = 0;
        for ($i = 0; $i < $m; $i++)
            $ones += $grid[$i][$j] === $grid[$i][0] ? 1 : 0;
        $score += max($ones, $m - $ones) * (1 << ($n - 1 - $j));
    }
    return $score;
}
```
**Python**
```python
def matrix_score(grid):
    m, n = len(grid), len(grid[0])
    score = m * (1 << (n - 1))
    for j in range(1, n):
        ones = sum(1 for i in range(m) if grid[i][j] == grid[i][0])
        score += max(ones, m - ones) * (1 << (n - 1 - j))
    return score
```
