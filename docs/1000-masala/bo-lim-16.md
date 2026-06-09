<a id="b16"></a>
# 16-bo'lim: Greedy (ochko'z algoritmlar)

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> 🤑 Greedy — har qadamda lokal optimal tanlovni qilib, global optimalga yetishga harakat. **Har doim ham ishlamaydi**: greedy to'g'riligi isbotlanishi kerak (mas. tugash vaqti bo'yicha tanlash, kasrli knapsack). Aks holda DP kerak bo'ladi.

<a id="m177"></a>
### 177. Tanga maydalash — greedy (kanonik tizim)
`⏱ O(n log n + amount) · 💾 O(1)`
⚠️ Greedy faqat **kanonik** tizimlarda to'g'ri (mas. [1,5,10,25]). [1,3,4] uchun summa 6 → greedy 4+1+1=3 ta beradi, optimal esa 3+3=2 ta. Bunday holatda DP (157-masala) kerak.

**JS**
```js
const coinChangeGreedy = (coins, amount) => {
  const sorted = [...coins].sort((a, b) => b - a);
  let count = 0;
  for (const c of sorted) {
    while (amount >= c) { amount -= c; count++; }
  }
  return amount === 0 ? count : -1;
};
```
**PHP**
```php
function coinChangeGreedy($coins, $amount): int {
    $sorted = $coins;
    rsort($sorted);
    $count = 0;
    foreach ($sorted as $c) {
        while ($amount >= $c) { $amount -= $c; $count++; }
    }
    return $amount === 0 ? $count : -1;
}
```
**Python**
```python
def coin_change_greedy(coins, amount):
    count = 0
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c
            count += 1
    return count if amount == 0 else -1
```

<a id="m178"></a>
### 178. Activity selection (intervallarni rejalashtirish)
`⏱ O(n log n) · 💾 O(1)`
Tugash vaqti bo'yicha saralab, eng erta tugaydiganni tanlash — keyingilarga eng ko'p joy qoldiradi (greedy choice). Kirish: `[[start, end], ...]`.

**JS**
```js
const activitySelection = intervals => {
  const sorted = [...intervals].sort((a, b) => a[1] - b[1]);
  let count = 0, lastEnd = -Infinity;
  for (const [start, end] of sorted) {
    if (start >= lastEnd) { count++; lastEnd = end; }
  }
  return count;
};
```
**PHP**
```php
function activitySelection($intervals): int {
    $sorted = $intervals;
    usort($sorted, fn($a, $b) => $a[1] <=> $b[1]);
    $count = 0;
    $lastEnd = -INF;
    foreach ($sorted as [$start, $end]) {
        if ($start >= $lastEnd) { $count++; $lastEnd = $end; }
    }
    return $count;
}
```
**Python**
```python
def activity_selection(intervals):
    count = 0
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda x: x[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count
```

<a id="m179"></a>
### 179. Fractional knapsack (kasrli ryukzak)
`⏱ O(n log n) · 💾 O(n)`
0/1 knapsack (159) DP talab qiladi, lekin **kasrli** versiyada greedy optimal — eng yuqori qiymat/og'irlik nisbatidan boshlash.

**JS**
```js
const fractionalKnapsack = (weights, values, cap) => {
  const items = weights.map((w, i) => ({ w, r: values[i] / w }));
  items.sort((a, b) => b.r - a.r);
  let total = 0;
  for (const item of items) {
    if (cap <= 0) break;
    const take = Math.min(item.w, cap);
    total += take * item.r;
    cap -= take;
  }
  return total;
};
```
**PHP**
```php
function fractionalKnapsack($weights, $values, $cap): float {
    $items = [];
    foreach ($weights as $i => $w) {
        $items[] = ['w' => $w, 'r' => $values[$i] / $w];
    }
    usort($items, fn($a, $b) => $b['r'] <=> $a['r']);
    $total = 0;
    foreach ($items as $item) {
        if ($cap <= 0) break;
        $take = min($item['w'], $cap);
        $total += $take * $item['r'];
        $cap -= $take;
    }
    return $total;
}
```
**Python**
```python
def fractional_knapsack(weights, values, cap):
    items = sorted(
        ((values[i] / w, w) for i, w in enumerate(weights)),
        reverse=True,
    )
    total = 0.0
    for ratio, w in items:
        if cap <= 0:
            break
        take = min(w, cap)
        total += take * ratio
        cap -= take
    return total
```

<a id="m180"></a>
### 180. Jump game (oxiriga yetib bo'ladimi)
`⏱ O(n) · 💾 O(1)`
nums[i] — i'dan maksimal sakrash. Eng uzoq yetib boriladigan pozitsiyani kuzatamiz; joriy indeks undan oshsa — to'siq.

**JS**
```js
const canJump = nums => {
  let reach = 0;
  for (let i = 0; i < nums.length; i++) {
    if (i > reach) return false;
    reach = Math.max(reach, i + nums[i]);
  }
  return true;
};
```
**PHP**
```php
function canJump($nums): bool {
    $reach = 0;
    for ($i = 0; $i < count($nums); $i++) {
        if ($i > $reach) return false;
        $reach = max($reach, $i + $nums[$i]);
    }
    return true;
}
```
**Python**
```python
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True
```

<a id="m181"></a>
### 181. Merge intervals (intervallarni birlashtirish)
`⏱ O(n log n) · 💾 O(n)`
Boshlanish bo'yicha saralab — keyingi interval oxirgisining oxiri bilan kesishsa, birlashtirib uzaytiramiz.

**JS**
```js
const mergeIntervals = intervals => {
  if (intervals.length === 0) return [];
  const sorted = [...intervals].sort((a, b) => a[0] - b[0]);
  const res = [sorted[0]];
  for (let i = 1; i < sorted.length; i++) {
    const last = res[res.length - 1];
    const [start, end] = sorted[i];
    if (start <= last[1]) last[1] = Math.max(last[1], end);
    else res.push([start, end]);
  }
  return res;
};
```
**PHP**
```php
function mergeIntervals($intervals): array {
    if (count($intervals) === 0) return [];
    $sorted = $intervals;
    usort($sorted, fn($a, $b) => $a[0] <=> $b[0]);
    $res = [$sorted[0]];
    for ($i = 1; $i < count($sorted); $i++) {
        [$start, $end] = $sorted[$i];
        $j = count($res) - 1;
        if ($start <= $res[$j][1]) {
            $res[$j][1] = max($res[$j][1], $end);
        } else {
            $res[] = [$start, $end];
        }
    }
    return $res;
}
```
**Python**
```python
def merge_intervals(intervals):
    if not intervals:
        return []
    res = []
    for start, end in sorted(intervals, key=lambda x: x[0]):
        if res and start <= res[-1][1]:
            res[-1][1] = max(res[-1][1], end)
        else:
            res.append([start, end])
    return res
```

<a id="m182"></a>
### 182. Gas station (aylana bo'ylab boshlanish nuqtasi)
`⏱ O(n) · 💾 O(1)`
Umumiy gaz ≥ umumiy xarajat bo'lsa, yechim bor; bak manfiyga tushgan joydan keyingi stansiya yagona nomzod boshlanish nuqtasi.

**JS**
```js
const canCompleteCircuit = (gas, cost) => {
  let total = 0, tank = 0, start = 0;
  for (let i = 0; i < gas.length; i++) {
    const diff = gas[i] - cost[i];
    total += diff;
    tank += diff;
    if (tank < 0) { start = i + 1; tank = 0; }
  }
  return total >= 0 ? start : -1;
};
```
**PHP**
```php
function canCompleteCircuit($gas, $cost): int {
    $total = 0; $tank = 0; $start = 0;
    for ($i = 0; $i < count($gas); $i++) {
        $diff = $gas[$i] - $cost[$i];
        $total += $diff;
        $tank += $diff;
        if ($tank < 0) { $start = $i + 1; $tank = 0; }
    }
    return $total >= 0 ? $start : -1;
}
```
**Python**
```python
def can_complete_circuit(gas, cost):
    total = tank = start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff
        tank += diff
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1
```

---
