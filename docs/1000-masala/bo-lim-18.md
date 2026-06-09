<a id="b18"></a>
# 18-bo'lim: Sana / vaqt

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> 📅 Bu yerda asosiy gap — har tilning sana kutubxonasidan to'g'ri foydalanish (murakkablik deyarli har doim O(1)). Eng katta tuzoq: **JS Date'da oylar 0-dan boshlanadi**, hamda `getDay()` (JS) / `weekday()` (Python) haftani **turli kundan** boshlaydi. PHP `DateTime`, Python `datetime`, JS `Date`.

<a id="m194"></a>
### 194. Joriy vaqt va Unix timestamp
`⏱ O(1)`
JS `Date.now()` millisoniya, PHP/Python `time()` soniya qaytaradi.

**JS**
```js
const now = new Date();
const timestamp = Math.floor(Date.now() / 1000); // soniyalarda
```
**PHP**
```php
$now = new DateTime();
$timestamp = time(); // soniyalarda
```
**Python**
```python
from datetime import datetime
import time

now = datetime.now()
timestamp = int(time.time())  # soniyalarda
```

<a id="m195"></a>
### 195. Sanani formatlash (YYYY-MM-DD HH:MM:SS)
`⏱ O(1)`
JS'da oylar 0-dan (`getMonth() + 1` zarur) — klassik xato manbai. PHP/Python format satrlari bu muammodan xoli.

**JS**
```js
const formatDate = d => {
  const pad = n => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ` +
         `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
};
```
**PHP**
```php
function formatDate(DateTime $d): string {
    return $d->format('Y-m-d H:i:s');
}
```
**Python**
```python
def format_date(d):
    return d.strftime("%Y-%m-%d %H:%M:%S")
```

<a id="m196"></a>
### 196. Satrdan sanani parse qilish
`⏱ O(1)`
JS faqat ISO formatni ishonchli parse qiladi; aniq format uchun PHP `createFromFormat`, Python `strptime` ishonchliroq.

**JS**
```js
const date = new Date("2026-06-09T14:30:00");
```
**PHP**
```php
$date = new DateTime("2026-06-09 14:30:00");
// aniq format: DateTime::createFromFormat('d/m/Y', '09/06/2026')
```
**Python**
```python
from datetime import datetime

date = datetime.strptime("2026-06-09 14:30:00", "%Y-%m-%d %H:%M:%S")
```

<a id="m197"></a>
### 197. Ikki sana orasidagi kunlar farqi
`⏱ O(1)`
JS — millisoniya farqini kunga bo'lish; PHP `diff()` `DateInterval` qaytaradi; Python sanalarni ayirsa `timedelta` chiqadi.

**JS**
```js
const daysBetween = (a, b) => {
  const ms = Math.abs(b - a);
  return Math.floor(ms / (1000 * 60 * 60 * 24));
};
```
**PHP**
```php
function daysBetween(DateTime $a, DateTime $b): int {
    return $a->diff($b)->days;
}
```
**Python**
```python
def days_between(a, b):
    return abs((b - a).days)
```

<a id="m198"></a>
### 198. Sanaga kun qo'shish
`⏱ O(1)`
JS `setDate` oy/yil chegarasini avtomatik to'g'rilaydi; PHP `modify`; Python `timedelta`.

**JS**
```js
const addDays = (d, days) => {
  const r = new Date(d);
  r.setDate(r.getDate() + days);
  return r;
};
```
**PHP**
```php
function addDays(DateTime $d, int $days): DateTime {
    $r = clone $d;
    $r->modify("+$days days");
    return $r;
}
```
**Python**
```python
from datetime import timedelta

def add_days(d, days):
    return d + timedelta(days=days)
```

<a id="m199"></a>
### 199. Hafta kuni (nomi)
`⏱ O(1)`
⚠️ JS `getDay()` va PHP `'w'` — 0 = Yakshanba; Python `weekday()` — 0 = Dushanba (boshqacha!). Indekslashda ehtiyot bo'ling.

**JS**
```js
const weekday = d =>
  ["Yakshanba", "Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"][d.getDay()];
```
**PHP**
```php
function weekday(DateTime $d): string {
    $days = ["Yakshanba", "Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"];
    return $days[(int) $d->format('w')];
}
```
**Python**
```python
def weekday(d):
    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    return days[d.weekday()]
```

<a id="m200"></a>
### 200. Oydagi kunlar soni
`⏱ O(1)`
JS hiyla — keyingi oyning "0-kuni" joriy oyning oxirgi kuni; PHP `date('t')`; Python `calendar.monthrange`.

**JS**
```js
const daysInMonth = (year, month) => new Date(year, month, 0).getDate();
// month: 1-12
```
**PHP**
```php
function daysInMonth(int $year, int $month): int {
    return (int) date('t', mktime(0, 0, 0, $month, 1, $year));
}
```
**Python**
```python
import calendar

def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]
```

<a id="m201"></a>
### 201. Yosh hisoblash (tug'ilgan sanadan)
`⏱ O(1)`
Tug'ilgan kun shu yili hali o'tmagan bo'lsa, 1 yil ayiriladi. PHP `diff()->y` buni avtomatik qiladi.

**JS**
```js
const age = birth => {
  const today = new Date();
  let years = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) years--;
  return years;
};
```
**PHP**
```php
function age(DateTime $birth): int {
    return (new DateTime())->diff($birth)->y;
}
```
**Python**
```python
from datetime import date

def age(birth):
    today = date.today()
    years = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        years -= 1
    return years
```

---
