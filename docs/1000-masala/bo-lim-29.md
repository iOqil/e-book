<a id="b29"></a>
# 29-bo'lim: Ilg'or stringlar

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Bu bo'limda stringlar (satrlar) bilan ishlashning ilg'or texnikalari yig'ilgan: siqish va
> dekodlash (RLE), qavslar to'g'riligini tekshirish va tuzatish, stek yordamida qo'shni
> takrorlarni o'chirish, sirpanuvchi oyna (sliding window) bilan eng uzun/kichik oyna topish,
> leksikografik tartiblash, hamda real hayotdagi formatlash masalalari (litsenziya kaliti, IP,
> email). Asosiy g'oyalar: stek, sirpanuvchi oyna, ochko'z (greedy) tanlov va hashmap. Asosiy
> satr amallari (teskari, palindrom, anagram, KMP, Trie) oldingi bo'limlarda ko'rilgan — bu yerda
> takrorlanmaydi.

<a id="m547"></a>
### 547. Satrni siqish — RLE (run-length encoding)
Ketma-ket takrorlangan belgilarni "belgi + son" ko'rinishida siqamiz: `aaabb` → `a3b2`.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const rleEncode = (s) => {
  let res = "", i = 0;
  while (i < s.length) {
    let j = i;
    while (j < s.length && s[j] === s[i]) j++;
    res += s[i] + (j - i);
    i = j;
  }
  return res;
};
```
**PHP**
```php
function rleEncode(string $s): string {
    $res = ""; $n = strlen($s); $i = 0;
    while ($i < $n) {
        $j = $i;
        while ($j < $n && $s[$j] === $s[$i]) $j++;
        $res .= $s[$i] . ($j - $i);
        $i = $j;
    }
    return $res;
}
```
**Python**
```python
def rle_encode(s):
    res, i, n = [], 0, len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        res.append(s[i] + str(j - i))
        i = j
    return "".join(res)
```

<a id="m548"></a>
### 548. RLE dekodlash (run-length decode)
`a3b2` kabi siqilgan satrni asliga qaytaramiz: `aaabb`. Son bir necha raqamli bo'lishi mumkin.
`⏱ O(natija) · 💾 O(natija)`

**JS**
```js
const rleDecode = (s) => {
  let res = "", i = 0;
  while (i < s.length) {
    const ch = s[i++];
    let num = "";
    while (i < s.length && s[i] >= "0" && s[i] <= "9") num += s[i++];
    res += ch.repeat(Number(num));
  }
  return res;
};
```
**PHP**
```php
function rleDecode(string $s): string {
    $res = ""; $n = strlen($s); $i = 0;
    while ($i < $n) {
        $ch = $s[$i++]; $num = "";
        while ($i < $n && ctype_digit($s[$i])) $num .= $s[$i++];
        $res .= str_repeat($ch, (int)$num);
    }
    return $res;
}
```
**Python**
```python
def rle_decode(s):
    res, i, n = [], 0, len(s)
    while i < n:
        ch = s[i]; i += 1
        num = ""
        while i < n and s[i].isdigit():
            num += s[i]; i += 1
        res.append(ch * int(num))
    return "".join(res)
```

<a id="m549"></a>
### 549. Siqilgan satrni ochish — k[encoded] (decode string)
`3[a]2[bc]` → `aaabcbc`. Ichma-ich qavslarni stek yordamida ochamiz.
`⏱ O(natija) · 💾 O(natija)`

**JS**
```js
const decodeString = (s) => {
  const numSt = [], strSt = [];
  let cur = "", num = 0;
  for (const ch of s) {
    if (ch >= "0" && ch <= "9") num = num * 10 + (+ch);
    else if (ch === "[") { numSt.push(num); strSt.push(cur); cur = ""; num = 0; }
    else if (ch === "]") { cur = strSt.pop() + cur.repeat(numSt.pop()); }
    else cur += ch;
  }
  return cur;
};
```
**PHP**
```php
function decodeString(string $s): string {
    $numSt = []; $strSt = []; $cur = ""; $num = 0;
    foreach (str_split($s) as $ch) {
        if (ctype_digit($ch)) $num = $num * 10 + (int)$ch;
        elseif ($ch === "[") { $numSt[] = $num; $strSt[] = $cur; $cur = ""; $num = 0; }
        elseif ($ch === "]") { $cur = array_pop($strSt) . str_repeat($cur, array_pop($numSt)); }
        else $cur .= $ch;
    }
    return $cur;
}
```
**Python**
```python
def decode_string(s):
    num_st, str_st, cur, num = [], [], "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            num_st.append(num); str_st.append(cur); cur = ""; num = 0
        elif ch == "]":
            cur = str_st.pop() + cur * num_st.pop()
        else:
            cur += ch
    return cur
```

<a id="m550"></a>
### 550. Yulduzli qavslar to'g'riligi (valid parenthesis string with *)
`*` belgi `(`, `)` yoki bo'sh bo'lishi mumkin. Ochilmagan qavslar oralig'ini ikki sanagich bilan kuzatamiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const checkValidString = (s) => {
  let lo = 0, hi = 0;
  for (const ch of s) {
    if (ch === "(") { lo++; hi++; }
    else if (ch === ")") { lo--; hi--; }
    else { lo--; hi++; }
    if (hi < 0) return false;
    if (lo < 0) lo = 0;
  }
  return lo === 0;
};
```
**PHP**
```php
function checkValidString(string $s): bool {
    $lo = 0; $hi = 0;
    foreach (str_split($s) as $ch) {
        if ($ch === "(") { $lo++; $hi++; }
        elseif ($ch === ")") { $lo--; $hi--; }
        else { $lo--; $hi++; }
        if ($hi < 0) return false;
        if ($lo < 0) $lo = 0;
    }
    return $lo === 0;
}
```
**Python**
```python
def check_valid_string(s):
    lo = hi = 0
    for ch in s:
        if ch == "(":
            lo += 1; hi += 1
        elif ch == ")":
            lo -= 1; hi -= 1
        else:
            lo -= 1; hi += 1
        if hi < 0:
            return False
        if lo < 0:
            lo = 0
    return lo == 0
```

<a id="m551"></a>
### 551. Yaroqsiz qavslarni o'chirish (remove invalid parentheses)
Eng kam belgi o'chirib, barcha to'g'ri variantlarni topamiz. BFS bilan minimal o'chirishni qidiramiz.
`⏱ O(2ⁿ) · 💾 O(2ⁿ)`

**JS**
```js
const removeInvalidParentheses = (s) => {
  const isValid = (t) => {
    let c = 0;
    for (const ch of t) {
      if (ch === "(") c++;
      else if (ch === ")" && --c < 0) return false;
    }
    return c === 0;
  };
  let level = new Set([s]);
  while (level.size) {
    const valid = [...level].filter(isValid);
    if (valid.length) return valid;
    const next = new Set();
    for (const t of level)
      for (let i = 0; i < t.length; i++)
        if (t[i] === "(" || t[i] === ")")
          next.add(t.slice(0, i) + t.slice(i + 1));
    level = next;
  }
  return [""];
};
```
**Python**
```python
def remove_invalid_parentheses(s):
    def is_valid(t):
        c = 0
        for ch in t:
            if ch == "(":
                c += 1
            elif ch == ")":
                c -= 1
                if c < 0:
                    return False
        return c == 0

    level = {s}
    while level:
        valid = [t for t in level if is_valid(t)]
        if valid:
            return valid
        nxt = set()
        for t in level:
            for i, ch in enumerate(t):
                if ch in "()":
                    nxt.add(t[:i] + t[i + 1:])
        level = nxt
    return [""]
```

<a id="m552"></a>
### 552. Eng uzun to'g'ri qavslar ketma-ketligi (longest valid parentheses)
Eng uzun to'g'ri qavslangan qism-satr uzunligini topamiz. Stekda indekslar saqlanadi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const longestValidParentheses = (s) => {
  let best = 0;
  const st = [-1];
  for (let i = 0; i < s.length; i++) {
    if (s[i] === "(") st.push(i);
    else {
      st.pop();
      if (st.length === 0) st.push(i);
      else best = Math.max(best, i - st[st.length - 1]);
    }
  }
  return best;
};
```
**PHP**
```php
function longestValidParentheses(string $s): int {
    $best = 0; $st = [-1];
    for ($i = 0; $i < strlen($s); $i++) {
        if ($s[$i] === "(") $st[] = $i;
        else {
            array_pop($st);
            if (empty($st)) $st[] = $i;
            else $best = max($best, $i - end($st));
        }
    }
    return $best;
}
```
**Python**
```python
def longest_valid_parentheses(s):
    best = 0
    st = [-1]
    for i, ch in enumerate(s):
        if ch == "(":
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                best = max(best, i - st[-1])
    return best
```

<a id="m553"></a>
### 553. Qavslarni to'g'rilash uchun minimal o'chirish (minimum remove to make valid)
Faqat yaroqsiz qavslarni belgilab o'chiramiz, harflarni saqlaymiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const minRemoveToMakeValid = (s) => {
  const arr = s.split(""), st = [];
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === "(") st.push(i);
    else if (arr[i] === ")") {
      if (st.length) st.pop();
      else arr[i] = "";
    }
  }
  for (const i of st) arr[i] = "";
  return arr.join("");
};
```
**PHP**
```php
function minRemoveToMakeValid(string $s): string {
    $arr = str_split($s); $st = [];
    foreach ($arr as $i => $ch) {
        if ($ch === "(") $st[] = $i;
        elseif ($ch === ")") {
            if ($st) array_pop($st);
            else $arr[$i] = "";
        }
    }
    foreach ($st as $i) $arr[$i] = "";
    return implode("", $arr);
}
```
**Python**
```python
def min_remove_to_make_valid(s):
    arr = list(s)
    st = []
    for i, ch in enumerate(arr):
        if ch == "(":
            st.append(i)
        elif ch == ")":
            if st:
                st.pop()
            else:
                arr[i] = ""
    for i in st:
        arr[i] = ""
    return "".join(arr)
```

<a id="m554"></a>
### 554. Backspace bilan satr taqqoslash (backspace string compare)
`#` belgi oldingi belgini o'chiradi. Ikki satrni teskaridan yurib taqqoslaymiz.
`⏱ O(n + m) · 💾 O(1)`

**JS**
```js
const backspaceCompare = (s, t) => {
  const build = (str) => {
    const res = [];
    for (const ch of str) {
      if (ch === "#") res.pop();
      else res.push(ch);
    }
    return res.join("");
  };
  return build(s) === build(t);
};
```
**PHP**
```php
function backspaceCompare(string $s, string $t): bool {
    $build = function (string $str): string {
        $res = [];
        foreach (str_split($str) as $ch) {
            if ($ch === "#") array_pop($res);
            else $res[] = $ch;
        }
        return implode("", $res);
    };
    return $build($s) === $build($t);
}
```
**Python**
```python
def backspace_compare(s, t):
    def build(string):
        res = []
        for ch in string:
            if ch == "#":
                if res:
                    res.pop()
            else:
                res.append(ch)
        return "".join(res)

    return build(s) == build(t)
```

<a id="m555"></a>
### 555. Litsenziya kalitini formatlash (license key formatting)
Tirelarni olib tashlab, belgilarni `k` tadan guruhlab, bosh harfga keltiramiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const licenseKeyFormatting = (s, k) => {
  const clean = s.replace(/-/g, "").toUpperCase();
  const groups = [];
  for (let i = clean.length; i > 0; i -= k)
    groups.unshift(clean.slice(Math.max(0, i - k), i));
  return groups.join("-");
};
```
**PHP**
```php
function licenseKeyFormatting(string $s, int $k): string {
    $clean = strtoupper(str_replace("-", "", $s));
    $groups = [];
    for ($i = strlen($clean); $i > 0; $i -= $k)
        array_unshift($groups, substr($clean, max(0, $i - $k), min($k, $i)));
    return implode("-", $groups);
}
```
**Python**
```python
def license_key_formatting(s, k):
    clean = s.replace("-", "").upper()
    groups = []
    i = len(clean)
    while i > 0:
        groups.append(clean[max(0, i - k):i])
        i -= k
    return "-".join(reversed(groups))
```

<a id="m556"></a>
### 556. Log fayllarni qayta tartiblash (reorder data in log files)
Harfli loglar mazmun bo'yicha (teng bo'lsa identifikator bo'yicha), raqamli loglar esa o'z tartibida ortda.
`⏱ O(n log n · L) · 💾 O(n)`

**JS**
```js
const reorderLogFiles = (logs) => {
  const letters = [], digits = [];
  for (const log of logs) {
    const rest = log.slice(log.indexOf(" ") + 1);
    if (rest[0] >= "0" && rest[0] <= "9") digits.push(log);
    else letters.push(log);
  }
  letters.sort((a, b) => {
    const ia = a.indexOf(" "), ib = b.indexOf(" ");
    const ca = a.slice(ia + 1), cb = b.slice(ib + 1);
    if (ca !== cb) return ca < cb ? -1 : 1;
    return a.slice(0, ia) < b.slice(0, ib) ? -1 : 1;
  });
  return [...letters, ...digits];
};
```
**Python**
```python
def reorder_log_files(logs):
    def key(log):
        ident, rest = log.split(" ", 1)
        if rest[0].isdigit():
            return (1,)
        return (0, rest, ident)

    return sorted(logs, key=key)
```

<a id="m557"></a>
### 557. Maxsus tartibda satr (custom sort string)
`order` belgilar tartibini belgilaydi; `s` ni shu tartibda joylashtramiz, qolganlari oxirida.
`⏱ O(n + m) · 💾 O(1)`

**JS**
```js
const customSortString = (order, s) => {
  const cnt = {};
  for (const ch of s) cnt[ch] = (cnt[ch] || 0) + 1;
  let res = "";
  for (const ch of order)
    if (cnt[ch]) { res += ch.repeat(cnt[ch]); cnt[ch] = 0; }
  for (const ch in cnt)
    if (cnt[ch]) res += ch.repeat(cnt[ch]);
  return res;
};
```
**PHP**
```php
function customSortString(string $order, string $s): string {
    $cnt = array_count_values(str_split($s));
    $res = "";
    foreach (str_split($order) as $ch)
        if (!empty($cnt[$ch])) { $res .= str_repeat($ch, $cnt[$ch]); $cnt[$ch] = 0; }
    foreach ($cnt as $ch => $c)
        if ($c) $res .= str_repeat($ch, $c);
    return $res;
}
```
**Python**
```python
from collections import Counter

def custom_sort_string(order, s):
    cnt = Counter(s)
    res = []
    for ch in order:
        if cnt[ch]:
            res.append(ch * cnt[ch]); cnt[ch] = 0
    for ch, c in cnt.items():
        if c:
            res.append(ch * c)
    return "".join(res)
```

<a id="m558"></a>
### 558. Eng qisqa to'ldiruvchi so'z (shortest completing word)
`licensePlate` dagi harflar (raqam/probelsiz) to'liq mavjud bo'lgan eng qisqa so'zni topamiz.
`⏱ O(n · L) · 💾 O(1)`

**JS**
```js
const shortestCompletingWord = (plate, words) => {
  const need = {};
  for (const ch of plate.toLowerCase())
    if (ch >= "a" && ch <= "z") need[ch] = (need[ch] || 0) + 1;
  const covers = (w) => {
    const c = {};
    for (const ch of w) c[ch] = (c[ch] || 0) + 1;
    return Object.keys(need).every((k) => (c[k] || 0) >= need[k]);
  };
  let best = null;
  for (const w of words)
    if (covers(w) && (best === null || w.length < best.length)) best = w;
  return best;
};
```
**Python**
```python
from collections import Counter

def shortest_completing_word(plate, words):
    need = Counter(ch for ch in plate.lower() if ch.isalpha())
    best = None
    for w in words:
        c = Counter(w)
        if all(c[k] >= v for k, v in need.items()):
            if best is None or len(w) < len(best):
                best = w
    return best
```

<a id="m559"></a>
### 559. Tovlamachi xati (ransom note)
`note` ni `magazine` harflaridan (har biri bir marta) tuzish mumkinligini tekshiramiz.
`⏱ O(n + m) · 💾 O(1)`

**JS**
```js
const canConstruct = (note, magazine) => {
  const cnt = {};
  for (const ch of magazine) cnt[ch] = (cnt[ch] || 0) + 1;
  for (const ch of note) {
    if (!cnt[ch]) return false;
    cnt[ch]--;
  }
  return true;
};
```
**PHP**
```php
function canConstruct(string $note, string $magazine): bool {
    $cnt = array_count_values(str_split($magazine));
    foreach (str_split($note) as $ch) {
        if (empty($cnt[$ch])) return false;
        $cnt[$ch]--;
    }
    return true;
}
```
**Python**
```python
from collections import Counter

def can_construct(note, magazine):
    cnt = Counter(magazine)
    for ch in note:
        if cnt[ch] <= 0:
            return False
        cnt[ch] -= 1
    return True
```

<a id="m560"></a>
### 560. Takrorlanuvchi qism-satr namunasi (repeated substring pattern)
Satr o'zining bir qism-satrini bir necha bor takrorlash bilan hosil bo'lganmi? `(s+s)` ichidan izlaymiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const repeatedSubstringPattern = (s) =>
  (s + s).slice(1, -1).includes(s);
```
**PHP**
```php
function repeatedSubstringPattern(string $s): bool {
    $doubled = substr($s . $s, 1, -1);
    return strpos($doubled, $s) !== false;
}
```
**Python**
```python
def repeated_substring_pattern(s):
    return s in (s + s)[1:-1]
```

<a id="m561"></a>
### 561. Ikkilik qism-satrlarni sanash (count binary substrings)
Bir xil sondagi `0` va `1` lar guruhlangan qism-satrlar soni. Qo'shni guruhlar uzunligi minimumi.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const countBinarySubstrings = (s) => {
  let prev = 0, cur = 1, res = 0;
  for (let i = 1; i < s.length; i++) {
    if (s[i] === s[i - 1]) cur++;
    else { res += Math.min(prev, cur); prev = cur; cur = 1; }
  }
  return res + Math.min(prev, cur);
};
```
**PHP**
```php
function countBinarySubstrings(string $s): int {
    $prev = 0; $cur = 1; $res = 0;
    for ($i = 1; $i < strlen($s); $i++) {
        if ($s[$i] === $s[$i - 1]) $cur++;
        else { $res += min($prev, $cur); $prev = $cur; $cur = 1; }
    }
    return $res + min($prev, $cur);
}
```
**Python**
```python
def count_binary_substrings(s):
    prev, cur, res = 0, 1, 0
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cur += 1
        else:
            res += min(prev, cur); prev = cur; cur = 1
    return res + min(prev, cur)
```

<a id="m562"></a>
### 562. Eng uzun baxtli satr (longest happy string)
`a`, `b`, `c` larni berilgan miqdorda ishlatib, uchta bir xil belgi ketma-ket kelmaydigan eng uzun satr.
`⏱ O(n log 3) · 💾 O(1)`

**JS**
```js
const longestDiverseString = (a, b, c) => {
  const heap = [["a", a], ["b", b], ["c", c]];
  let res = "";
  while (true) {
    heap.sort((x, y) => y[1] - x[1]);
    let placed = false;
    for (const item of heap) {
      const [ch, cnt] = item;
      if (cnt === 0) break;
      const n = res.length;
      if (n >= 2 && res[n - 1] === ch && res[n - 2] === ch) continue;
      res += ch; item[1]--; placed = true; break;
    }
    if (!placed) break;
  }
  return res;
};
```
**Python**
```python
def longest_diverse_string(a, b, c):
    heap = [["a", a], ["b", b], ["c", c]]
    res = []
    while True:
        heap.sort(key=lambda x: -x[1])
        placed = False
        for item in heap:
            ch, cnt = item
            if cnt == 0:
                break
            if len(res) >= 2 and res[-1] == ch and res[-2] == ch:
                continue
            res.append(ch); item[1] -= 1; placed = True
            break
        if not placed:
            break
    return "".join(res)
```

<a id="m563"></a>
### 563. Takror harflarni o'chirish — eng kichik leksikografik (remove duplicate letters)
Har bir harf bir martadan qoladigan, leksikografik eng kichik natija. Ochko'z stek + oxirgi indeks.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const removeDuplicateLetters = (s) => {
  const last = {};
  for (let i = 0; i < s.length; i++) last[s[i]] = i;
  const st = [], inStack = new Set();
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (inStack.has(ch)) continue;
    while (st.length && st[st.length - 1] > ch && last[st[st.length - 1]] > i)
      inStack.delete(st.pop());
    st.push(ch); inStack.add(ch);
  }
  return st.join("");
};
```
**PHP**
```php
function removeDuplicateLetters(string $s): string {
    $last = [];
    for ($i = 0; $i < strlen($s); $i++) $last[$s[$i]] = $i;
    $st = []; $inStack = [];
    for ($i = 0; $i < strlen($s); $i++) {
        $ch = $s[$i];
        if (isset($inStack[$ch])) continue;
        while ($st && end($st) > $ch && $last[end($st)] > $i) {
            $rem = array_pop($st); unset($inStack[$rem]);
        }
        $st[] = $ch; $inStack[$ch] = true;
    }
    return implode("", $st);
}
```
**Python**
```python
def remove_duplicate_letters(s):
    last = {ch: i for i, ch in enumerate(s)}
    st, in_stack = [], set()
    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while st and st[-1] > ch and last[st[-1]] > i:
            in_stack.discard(st.pop())
        st.append(ch); in_stack.add(ch)
    return "".join(st)
```

<a id="m564"></a>
### 564. Bo'laklarga ajratish (partition labels)
Har bir harf faqat bitta bo'lakda bo'ladigan qilib satrni maksimal bo'laklarga bo'lamiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const partitionLabels = (s) => {
  const last = {};
  for (let i = 0; i < s.length; i++) last[s[i]] = i;
  const res = [];
  let start = 0, end = 0;
  for (let i = 0; i < s.length; i++) {
    end = Math.max(end, last[s[i]]);
    if (i === end) { res.push(end - start + 1); start = i + 1; }
  }
  return res;
};
```
**PHP**
```php
function partitionLabels(string $s): array {
    $last = [];
    for ($i = 0; $i < strlen($s); $i++) $last[$s[$i]] = $i;
    $res = []; $start = 0; $end = 0;
    for ($i = 0; $i < strlen($s); $i++) {
        $end = max($end, $last[$s[$i]]);
        if ($i === $end) { $res[] = $end - $start + 1; $start = $i + 1; }
    }
    return $res;
}
```
**Python**
```python
def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}
    res = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res
```

<a id="m565"></a>
### 565. Bitta tahrir masofasi (one edit distance)
Ikki satr orasida aynan bitta tahrir (qo'shish, o'chirish yoki almashtirish) borligini tekshiramiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const isOneEditDistance = (s, t) => {
  if (Math.abs(s.length - t.length) > 1) return false;
  if (s.length > t.length) [s, t] = [t, s];
  for (let i = 0; i < s.length; i++) {
    if (s[i] !== t[i]) {
      if (s.length === t.length) return s.slice(i + 1) === t.slice(i + 1);
      return s.slice(i) === t.slice(i + 1);
    }
  }
  return s.length + 1 === t.length;
};
```
**Python**
```python
def is_one_edit_distance(s, t):
    if abs(len(s) - len(t)) > 1:
        return False
    if len(s) > len(t):
        s, t = t, s
    for i in range(len(s)):
        if s[i] != t[i]:
            if len(s) == len(t):
                return s[i + 1:] == t[i + 1:]
            return s[i:] == t[i + 1:]
    return len(s) + 1 == len(t)
```

<a id="m566"></a>
### 566. Palindromni bittasini o'chirib tekshirish (valid palindrome II)
Ko'pi bilan bitta belgini o'chirib palindrom hosil qilish mumkinligini aniqlaymiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const validPalindrome = (s) => {
  const isPal = (l, r) => {
    while (l < r) { if (s[l] !== s[r]) return false; l++; r--; }
    return true;
  };
  let l = 0, r = s.length - 1;
  while (l < r) {
    if (s[l] !== s[r]) return isPal(l + 1, r) || isPal(l, r - 1);
    l++; r--;
  }
  return true;
};
```
**PHP**
```php
function validPalindrome(string $s): bool {
    $isPal = function (int $l, int $r) use ($s): bool {
        while ($l < $r) { if ($s[$l] !== $s[$r]) return false; $l++; $r--; }
        return true;
    };
    $l = 0; $r = strlen($s) - 1;
    while ($l < $r) {
        if ($s[$l] !== $s[$r]) return $isPal($l + 1, $r) || $isPal($l, $r - 1);
        $l++; $r--;
    }
    return true;
}
```
**Python**
```python
def valid_palindrome(s):
    def is_pal(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1; r -= 1
        return True

    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return is_pal(l + 1, r) or is_pal(l, r - 1)
        l += 1; r -= 1
    return True
```

<a id="m567"></a>
### 567. Palindromni buzish (break a palindrome)
Palindromni leksikografik eng kichik NOPALINDROM qilish uchun bitta belgini o'zgartiramiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const breakPalindrome = (s) => {
  const n = s.length;
  if (n < 2) return "";
  const arr = s.split("");
  for (let i = 0; i < Math.floor(n / 2); i++)
    if (arr[i] !== "a") { arr[i] = "a"; return arr.join(""); }
  arr[n - 1] = "b";
  return arr.join("");
};
```
**PHP**
```php
function breakPalindrome(string $s): string {
    $n = strlen($s);
    if ($n < 2) return "";
    $arr = str_split($s);
    for ($i = 0; $i < intdiv($n, 2); $i++)
        if ($arr[$i] !== "a") { $arr[$i] = "a"; return implode("", $arr); }
    $arr[$n - 1] = "b";
    return implode("", $arr);
}
```
**Python**
```python
def break_palindrome(s):
    n = len(s)
    if n < 2:
        return ""
    arr = list(s)
    for i in range(n // 2):
        if arr[i] != "a":
            arr[i] = "a"
            return "".join(arr)
    arr[-1] = "b"
    return "".join(arr)
```

<a id="m568"></a>
### 568. Namunani topish va almashtirish (find and replace pattern)
`pattern` ga ikki tomonlama mos (bijection) keladigan so'zlarni qaytaramiz.
`⏱ O(n · L) · 💾 O(L)`

**JS**
```js
const findAndReplacePattern = (words, pattern) => {
  const norm = (w) => {
    const m = {}; let res = "", next = 0;
    for (const ch of w) {
      if (!(ch in m)) m[ch] = next++;
      res += m[ch] + ",";
    }
    return res;
  };
  const p = norm(pattern);
  return words.filter((w) => norm(w) === p);
};
```
**Python**
```python
def find_and_replace_pattern(words, pattern):
    def norm(w):
        m, res, nxt = {}, [], 0
        for ch in w:
            if ch not in m:
                m[ch] = nxt; nxt += 1
            res.append(m[ch])
        return tuple(res)

    p = norm(pattern)
    return [w for w in words if norm(w) == p]
```

<a id="m569"></a>
### 569. Siljitilgan satrlarni guruhlash (group shifted strings)
`abc` → `bcd` kabi bir xil siljish naqshiga ega satrlarni guruhlaymiz. Kalit — qo'shni farqlar ketma-ketligi.
`⏱ O(n · L) · 💾 O(n · L)`

**JS**
```js
const groupStrings = (strings) => {
  const groups = {};
  for (const s of strings) {
    let key = "";
    for (let i = 1; i < s.length; i++)
      key += ((s.charCodeAt(i) - s.charCodeAt(i - 1) + 26) % 26) + ",";
    (groups[key] ||= []).push(s);
  }
  return Object.values(groups);
};
```
**Python**
```python
def group_strings(strings):
    groups = {}
    for s in strings:
        key = tuple((ord(s[i]) - ord(s[i - 1])) % 26 for i in range(1, len(s)))
        groups.setdefault(key, []).append(s)
    return list(groups.values())
```

<a id="m570"></a>
### 570. Satrlarni kodlash/dekodlash — uzunlik prefiksi (encode and decode strings)
Har bir satr oldiga `uzunlik#` qo'shamiz; dekodda shu prefiks bo'yicha kesib olamiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const encode = (strs) =>
  strs.map((s) => s.length + "#" + s).join("");

const decode = (s) => {
  const res = [];
  let i = 0;
  while (i < s.length) {
    let j = i;
    while (s[j] !== "#") j++;
    const len = Number(s.slice(i, j));
    res.push(s.slice(j + 1, j + 1 + len));
    i = j + 1 + len;
  }
  return res;
};
```
**Python**
```python
def encode(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)

def decode(s):
    res, i = [], 0
    while i < len(s):
        j = i
        while s[j] != "#":
            j += 1
        length = int(s[i:j])
        res.append(s[j + 1:j + 1 + length])
        i = j + 1 + length
    return res
```

<a id="m571"></a>
### 571. Noyob email manzillar (unique email addresses)
`.` e'tiborsiz, `+` dan keyingi qism tashlanadi (local qism). Noyob manzillar sonini sanaymiz.
`⏱ O(n · L) · 💾 O(n)`

**JS**
```js
const numUniqueEmails = (emails) => {
  const set = new Set();
  for (const e of emails) {
    let [local, domain] = e.split("@");
    local = local.split("+")[0].replaceAll(".", "");
    set.add(local + "@" + domain);
  }
  return set.size;
};
```
**PHP**
```php
function numUniqueEmails(array $emails): int {
    $set = [];
    foreach ($emails as $e) {
        [$local, $domain] = explode("@", $e);
        $local = str_replace(".", "", explode("+", $local)[0]);
        $set[$local . "@" . $domain] = true;
    }
    return count($set);
}
```
**Python**
```python
def num_unique_emails(emails):
    seen = set()
    for e in emails:
        local, domain = e.split("@")
        local = local.split("+")[0].replace(".", "")
        seen.add(local + "@" + domain)
    return len(seen)
```

<a id="m572"></a>
### 572. IP manzilni zararsizlantirish (defanging an IP address)
Har bir `.` ni `[.]` ga almashtramiz: `1.1.1.1` → `1[.]1[.]1[.]1`.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const defangIPaddr = (address) => address.replaceAll(".", "[.]");
```
**PHP**
```php
function defangIPaddr(string $address): string {
    return str_replace(".", "[.]", $address);
}
```
**Python**
```python
def defang_ip_addr(address):
    return address.replace(".", "[.]")
```

<a id="m573"></a>
### 573. Satrni aylantirish (rotate string)
`s` ni bir necha pozitsiyaga aylantirib `goal` hosil bo'lishini tekshiramiz: `(s+s)` ichidan izlaymiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const rotateString = (s, goal) =>
  s.length === goal.length && (s + s).includes(goal);
```
**PHP**
```php
function rotateString(string $s, string $goal): bool {
    return strlen($s) === strlen($goal) && strpos($s . $s, $goal) !== false;
}
```
**Python**
```python
def rotate_string(s, goal):
    return len(s) == len(goal) and goal in (s + s)
```

<a id="m574"></a>
### 574. Takrorlanuvchi DNA ketma-ketliklari (repeated DNA sequences)
Bir necha bor uchraydigan 10 belgili qism-satrlarni topamiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const findRepeatedDnaSequences = (s) => {
  const seen = new Set(), res = new Set();
  for (let i = 0; i + 10 <= s.length; i++) {
    const sub = s.slice(i, i + 10);
    if (seen.has(sub)) res.add(sub);
    else seen.add(sub);
  }
  return [...res];
};
```
**PHP**
```php
function findRepeatedDnaSequences(string $s): array {
    $seen = []; $res = [];
    for ($i = 0; $i + 10 <= strlen($s); $i++) {
        $sub = substr($s, $i, 10);
        if (isset($seen[$sub])) $res[$sub] = true;
        else $seen[$sub] = true;
    }
    return array_keys($res);
}
```
**Python**
```python
def find_repeated_dna_sequences(s):
    seen, res = set(), set()
    for i in range(len(s) - 9):
        sub = s[i:i + 10]
        if sub in seen:
            res.add(sub)
        else:
            seen.add(sub)
    return list(res)
```

<a id="m575"></a>
### 575. Bitta almashtirish bilan tenglashtirish (buddy strings)
Aynan bitta juft belgini almashtirib ikki satrni teng qilish mumkinligini tekshiramiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const buddyStrings = (s, goal) => {
  if (s.length !== goal.length) return false;
  if (s === goal) return new Set(s).size < s.length;
  const diff = [];
  for (let i = 0; i < s.length; i++)
    if (s[i] !== goal[i]) diff.push(i);
  return diff.length === 2 &&
    s[diff[0]] === goal[diff[1]] && s[diff[1]] === goal[diff[0]];
};
```
**Python**
```python
def buddy_strings(s, goal):
    if len(s) != len(goal):
        return False
    if s == goal:
        return len(set(s)) < len(s)
    diff = [i for i in range(len(s)) if s[i] != goal[i]]
    return (len(diff) == 2 and
            s[diff[0]] == goal[diff[1]] and s[diff[1]] == goal[diff[0]])
```

<a id="m576"></a>
### 576. Qavslarning maksimal ichma-ichlik chuqurligi (maximum nesting depth)
Faqat qavslarni hisobga olib, eng katta joriy chuqurlikni topamiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const maxDepth = (s) => {
  let depth = 0, best = 0;
  for (const ch of s) {
    if (ch === "(") best = Math.max(best, ++depth);
    else if (ch === ")") depth--;
  }
  return best;
};
```
**PHP**
```php
function maxDepth(string $s): int {
    $depth = 0; $best = 0;
    foreach (str_split($s) as $ch) {
        if ($ch === "(") $best = max($best, ++$depth);
        elseif ($ch === ")") $depth--;
    }
    return $best;
}
```
**Python**
```python
def max_depth(s):
    depth = best = 0
    for ch in s:
        if ch == "(":
            depth += 1
            best = max(best, depth)
        elif ch == ")":
            depth -= 1
    return best
```

<a id="m577"></a>
### 577. Satrni balansli bo'laklarga ajratish (split balanced strings)
`L` va `R` lar teng bo'lgan maksimal sondagi balansli bo'laklar sonini sanaymiz.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const balancedStringSplit = (s) => {
  let bal = 0, count = 0;
  for (const ch of s) {
    bal += ch === "L" ? 1 : -1;
    if (bal === 0) count++;
  }
  return count;
};
```
**PHP**
```php
function balancedStringSplit(string $s): int {
    $bal = 0; $count = 0;
    foreach (str_split($s) as $ch) {
        $bal += $ch === "L" ? 1 : -1;
        if ($bal === 0) $count++;
    }
    return $count;
}
```
**Python**
```python
def balanced_string_split(s):
    bal = count = 0
    for ch in s:
        bal += 1 if ch == "L" else -1
        if bal == 0:
            count += 1
    return count
```

<a id="m578"></a>
### 578. Ko'pi bilan K xil belgili eng uzun qism-satr (longest substring with at most K distinct)
Sirpanuvchi oyna va hashmap bilan ko'pi bilan `k` xil belgi saqlovchi eng uzun oynani topamiz.
`⏱ O(n) · 💾 O(k)`

**JS**
```js
const lengthOfLongestSubstringKDistinct = (s, k) => {
  const cnt = new Map();
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    cnt.set(s[right], (cnt.get(s[right]) || 0) + 1);
    while (cnt.size > k) {
      const c = s[left++];
      cnt.set(c, cnt.get(c) - 1);
      if (cnt.get(c) === 0) cnt.delete(c);
    }
    best = Math.max(best, right - left + 1);
  }
  return best;
};
```
**Python**
```python
def length_of_longest_substring_k_distinct(s, k):
    cnt = {}
    left = best = 0
    for right, ch in enumerate(s):
        cnt[ch] = cnt.get(ch, 0) + 1
        while len(cnt) > k:
            c = s[left]; left += 1
            cnt[c] -= 1
            if cnt[c] == 0:
                del cnt[c]
        best = max(best, right - left + 1)
    return best
```

<a id="m579"></a>
### 579. Ko'pi bilan 2 xil belgili eng uzun qism-satr (at most two distinct)
Avvalgi masalaning `k = 2` xususiy holi — meva terish (fruit into baskets) sifatida ham mashhur.
`⏱ O(n) · 💾 O(1)`

**JS**
```js
const lengthOfLongestSubstringTwoDistinct = (s) => {
  const cnt = new Map();
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    cnt.set(s[right], (cnt.get(s[right]) || 0) + 1);
    while (cnt.size > 2) {
      const c = s[left++];
      cnt.set(c, cnt.get(c) - 1);
      if (cnt.get(c) === 0) cnt.delete(c);
    }
    best = Math.max(best, right - left + 1);
  }
  return best;
};
```
**Python**
```python
def length_of_longest_substring_two_distinct(s):
    cnt = {}
    left = best = 0
    for right, ch in enumerate(s):
        cnt[ch] = cnt.get(ch, 0) + 1
        while len(cnt) > 2:
            c = s[left]; left += 1
            cnt[c] -= 1
            if cnt[c] == 0:
                del cnt[c]
        best = max(best, right - left + 1)
    return best
```

<a id="m580"></a>
### 580. Minimal qoplovchi oyna (minimum window substring)
`t` dagi barcha belgilarni qamrab oluvchi eng qisqa qism-satrni topamiz. Sirpanuvchi oyna + sanagich.
`⏱ O(n + m) · 💾 O(m)`

**JS**
```js
const minWindow = (s, t) => {
  const need = new Map();
  for (const ch of t) need.set(ch, (need.get(ch) || 0) + 1);
  let required = need.size, formed = 0;
  const win = new Map();
  let left = 0, best = [Infinity, 0, 0];
  for (let right = 0; right < s.length; right++) {
    const c = s[right];
    win.set(c, (win.get(c) || 0) + 1);
    if (need.has(c) && win.get(c) === need.get(c)) formed++;
    while (formed === required) {
      if (right - left + 1 < best[0]) best = [right - left + 1, left, right];
      const lc = s[left++];
      win.set(lc, win.get(lc) - 1);
      if (need.has(lc) && win.get(lc) < need.get(lc)) formed--;
    }
  }
  return best[0] === Infinity ? "" : s.slice(best[1], best[2] + 1);
};
```
**Python**
```python
from collections import Counter

def min_window(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    required = len(need)
    win = {}
    formed = 0
    left = 0
    best = (float("inf"), 0, 0)
    for right, c in enumerate(s):
        win[c] = win.get(c, 0) + 1
        if c in need and win[c] == need[c]:
            formed += 1
        while formed == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            lc = s[left]; left += 1
            win[lc] -= 1
            if lc in need and win[lc] < need[lc]:
                formed -= 1
    return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]
```

<a id="m581"></a>
### 581. 3 ta bir xil ketma-ket belgisiz satr (string without 3 identical consecutive)
Belgilarni qo'shamiz, lekin oxirgi ikkitasi bir xil bo'lsa, joriy belgini tashlab ketamiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const removeThreeConsecutive = (s) => {
  const res = [];
  for (const ch of s) {
    const n = res.length;
    if (n >= 2 && res[n - 1] === ch && res[n - 2] === ch) continue;
    res.push(ch);
  }
  return res.join("");
};
```
**PHP**
```php
function removeThreeConsecutive(string $s): string {
    $res = [];
    foreach (str_split($s) as $ch) {
        $n = count($res);
        if ($n >= 2 && $res[$n - 1] === $ch && $res[$n - 2] === $ch) continue;
        $res[] = $ch;
    }
    return implode("", $res);
}
```
**Python**
```python
def remove_three_consecutive(s):
    res = []
    for ch in s:
        if len(res) >= 2 and res[-1] == ch and res[-2] == ch:
            continue
        res.append(ch)
    return "".join(res)
```

<a id="m582"></a>
### 582. DI satr mosligi (DI string match)
`I` (increasing) va `D` (decreasing) ga mos 0..n permutatsiyasini ikki ko'rsatkich bilan tuzamiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const diStringMatch = (s) => {
  let lo = 0, hi = s.length;
  const res = [];
  for (const ch of s)
    res.push(ch === "I" ? lo++ : hi--);
  res.push(lo);
  return res;
};
```
**PHP**
```php
function diStringMatch(string $s): array {
    $lo = 0; $hi = strlen($s); $res = [];
    foreach (str_split($s) as $ch)
        $res[] = $ch === "I" ? $lo++ : $hi--;
    $res[] = $lo;
    return $res;
}
```
**Python**
```python
def di_string_match(s):
    lo, hi = 0, len(s)
    res = []
    for ch in s:
        if ch == "I":
            res.append(lo); lo += 1
        else:
            res.append(hi); hi -= 1
    res.append(lo)
    return res
```

<a id="m583"></a>
### 583. Qavslar bahosi (score of parentheses)
`()` = 1, `AB` = A+B, `(A)` = 2·A. Stek yordamida joriy darajaning bahosini yig'amiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const scoreOfParentheses = (s) => {
  const st = [0];
  for (const ch of s) {
    if (ch === "(") st.push(0);
    else {
      const v = st.pop();
      st[st.length - 1] += Math.max(2 * v, 1);
    }
  }
  return st[0];
};
```
**PHP**
```php
function scoreOfParentheses(string $s): int {
    $st = [0];
    foreach (str_split($s) as $ch) {
        if ($ch === "(") $st[] = 0;
        else {
            $v = array_pop($st);
            $st[count($st) - 1] += max(2 * $v, 1);
        }
    }
    return $st[0];
}
```
**Python**
```python
def score_of_parentheses(s):
    st = [0]
    for ch in s:
        if ch == "(":
            st.append(0)
        else:
            v = st.pop()
            st[-1] += max(2 * v, 1)
    return st[0]
```

<a id="m584"></a>
### 584. Barcha qo'shni takrorlarni o'chirish (remove all adjacent duplicates)
Stekka belgilarni joylaymiz; cho'qqi joriy belgiga teng bo'lsa, juftlikni o'chiramiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const removeAdjacentDuplicates = (s) => {
  const st = [];
  for (const ch of s) {
    if (st.length && st[st.length - 1] === ch) st.pop();
    else st.push(ch);
  }
  return st.join("");
};
```
**PHP**
```php
function removeAdjacentDuplicates(string $s): string {
    $st = [];
    foreach (str_split($s) as $ch) {
        if ($st && end($st) === $ch) array_pop($st);
        else $st[] = $ch;
    }
    return implode("", $st);
}
```
**Python**
```python
def remove_adjacent_duplicates(s):
    st = []
    for ch in s:
        if st and st[-1] == ch:
            st.pop()
        else:
            st.append(ch)
    return "".join(st)
```

<a id="m585"></a>
### 585. K ta qo'shni takrorni o'chirish (remove adjacent duplicates II)
Stekda `[belgi, son]` saqlaymiz; son `k` ga yetganda guruhni olib tashlaymiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const removeDuplicatesK = (s, k) => {
  const st = [];
  for (const ch of s) {
    if (st.length && st[st.length - 1][0] === ch) {
      if (++st[st.length - 1][1] === k) st.pop();
    } else st.push([ch, 1]);
  }
  return st.map(([ch, c]) => ch.repeat(c)).join("");
};
```
**PHP**
```php
function removeDuplicatesK(string $s, int $k): string {
    $st = [];
    foreach (str_split($s) as $ch) {
        $n = count($st);
        if ($n && $st[$n - 1][0] === $ch) {
            if (++$st[$n - 1][1] === $k) array_pop($st);
        } else $st[] = [$ch, 1];
    }
    $res = "";
    foreach ($st as [$ch, $c]) $res .= str_repeat($ch, $c);
    return $res;
}
```
**Python**
```python
def remove_duplicates_k(s, k):
    st = []
    for ch in s:
        if st and st[-1][0] == ch:
            st[-1][1] += 1
            if st[-1][1] == k:
                st.pop()
        else:
            st.append([ch, 1])
    return "".join(ch * c for ch, c in st)
```

<a id="m586"></a>
### 586. Satrni "yaxshi" qilish (make string great)
Yonma-yon kelgan bir harfning katta/kichik juftini (`aA`/`Aa`) stek bilan o'chiramiz.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
const makeGood = (s) => {
  const st = [];
  for (const ch of s) {
    const top = st[st.length - 1];
    if (top && top !== ch && top.toLowerCase() === ch.toLowerCase()) st.pop();
    else st.push(ch);
  }
  return st.join("");
};
```
**PHP**
```php
function makeGood(string $s): string {
    $st = [];
    foreach (str_split($s) as $ch) {
        $top = end($st);
        if ($top !== false && $top !== $ch && strtolower($top) === strtolower($ch))
            array_pop($st);
        else $st[] = $ch;
    }
    return implode("", $st);
}
```
**Python**
```python
def make_good(s):
    st = []
    for ch in s:
        if st and st[-1] != ch and st[-1].lower() == ch.lower():
            st.pop()
        else:
            st.append(ch)
    return "".join(st)
```
