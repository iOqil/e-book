<a id="b32"></a>
# 32-bo'lim: Konkurensiya va async

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Konkurensiya (concurrency) — bir nechta vazifani "bir vaqtda" (aslida bir-biriga
> aralashtirib) bajarish san'ati. Bu bo'lim TILGA XOS: asosiy misollar JavaScript
> `Promise`/`async` modelida, hamda Python `asyncio` da beriladi. PHP — sinxron til,
> shuning uchun u faqat mos kelgan joylarda (`Fiber`, generator yoki tushuntirish bilan)
> qo'shilgan. Bu yerda "universal bo'lmasa ham mayli" qoidasi to'liq qo'llanadi: ko'p
> masala 2 tilda, ba'zilari 3 tilda. Maqsad — `Promise.all`, semaphore, mutex, async
> navbat, cancellation va deadlock kabi tushunchalarni amalda his qilish.

<a id="m667"></a>
### 667. Promise.all (qo'lda implement)
Barcha promise'lar bajarilishini parallel kutadi; tartibni saqlaydi, birortasi rad etilsa darhol reject bo'ladi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = new Array(promises.length);
    let done = 0;
    if (promises.length === 0) return resolve(results);
    promises.forEach((p, i) => {
      Promise.resolve(p).then(v => {
        results[i] = v;
        if (++done === promises.length) resolve(results);
      }, reject);
    });
  });
}
// promiseAll([1, Promise.resolve(2), 3]) -> [1, 2, 3]
```
**Python**
```python
import asyncio

async def gather_all(coros):
    results = [None] * len(coros)
    async def run(i, c):
        results[i] = await c
    await asyncio.gather(*(run(i, c) for i, c in enumerate(coros)))
    return results
```

<a id="m668"></a>
### 668. Promise.race
Birinchi bajarilgan (yoki rad etilgan) promise natijasini qaytaradi, qolganlarini e'tiborsiz qoldiradi.

**JS**
```js
function promiseRace(promises) {
  return new Promise((resolve, reject) => {
    for (const p of promises) Promise.resolve(p).then(resolve, reject);
  });
}
```
**Python**
```python
import asyncio

async def race(coros):
    tasks = [asyncio.ensure_future(c) for c in coros]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for p in pending:
        p.cancel()
    return done.pop().result()
```

<a id="m669"></a>
### 669. Promise.allSettled
Hamma promise tugaguncha kutadi va har biri uchun `{status, value|reason}` qaytaradi; hech qachon reject bo'lmaydi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
function allSettled(promises) {
  return Promise.all(
    promises.map(p =>
      Promise.resolve(p).then(
        value => ({ status: "fulfilled", value }),
        reason => ({ status: "rejected", reason })
      )
    )
  );
}
```
**Python**
```python
import asyncio

async def all_settled(coros):
    async def wrap(c):
        try:
            return {"status": "fulfilled", "value": await c}
        except Exception as e:
            return {"status": "rejected", "reason": e}
    return await asyncio.gather(*(wrap(c) for c in coros))
```

<a id="m670"></a>
### 670. Promise.any
Birinchi muvaffaqiyatli promise'ni qaytaradi; hammasi rad etilsa `AggregateError` tashlaydi.
`⏱ O(n) · 💾 O(n)`

**JS**
```js
function promiseAny(promises) {
  return new Promise((resolve, reject) => {
    const errors = new Array(promises.length);
    let rejected = 0;
    if (promises.length === 0)
      return reject(new AggregateError([], "All promises were rejected"));
    promises.forEach((p, i) => {
      Promise.resolve(p).then(resolve, err => {
        errors[i] = err;
        if (++rejected === promises.length)
          reject(new AggregateError(errors, "All promises were rejected"));
      });
    });
  });
}
```
**Python**
```python
import asyncio

async def any_ok(coros):
    tasks = [asyncio.ensure_future(c) for c in coros]
    errors = []
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for d in done:
            if d.exception() is None:
                for t in tasks:
                    t.cancel()
                return d.result()
            errors.append(d.exception())
        tasks = list(tasks)
    raise ExceptionGroup("All failed", errors)
```

<a id="m671"></a>
### 671. Ketma-ket vs parallel bajarish
Bir xil vazifalarni navbatma-navbat (`await` ichida sikl) yoki bir vaqtda (`Promise.all`/`gather`) bajarish — vaqt farqi katta.

**JS**
```js
async function sequential(tasks) {
  const out = [];
  for (const t of tasks) out.push(await t()); // navbatma-navbat
  return out;
}
async function parallel(tasks) {
  return Promise.all(tasks.map(t => t()));     // bir vaqtda
}
```
**Python**
```python
import asyncio

async def sequential(tasks):
    return [await t() for t in tasks]

async def parallel(tasks):
    return await asyncio.gather(*(t() for t in tasks))
```
**PHP**
```php
// PHP sinxron: faqat ketma-ket (real parallel uchun curl_multi/Fiber kerak)
function sequentialPhp(array $tasks): array {
    $out = [];
    foreach ($tasks as $t) $out[] = $t();
    return $out;
}
```

<a id="m672"></a>
### 672. async map (concurrency limit bilan)
Elementlarni asinxron almashtiradi, lekin bir vaqtda ko'pi bilan `limit` ta ishlov ketadi; tartib saqlanadi.

**JS**
```js
async function mapLimit(items, limit, fn) {
  const results = new Array(items.length);
  let i = 0;
  async function worker() {
    while (i < items.length) {
      const idx = i++;
      results[idx] = await fn(items[idx], idx);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
```
**Python**
```python
import asyncio

async def map_limit(items, limit, fn):
    sem = asyncio.Semaphore(limit)
    async def bound(i, x):
        async with sem:
            return i, await fn(x)
    pairs = await asyncio.gather(*(bound(i, x) for i, x in enumerate(items)))
    out = [None] * len(items)
    for i, v in pairs:
        out[i] = v
    return out
```

<a id="m673"></a>
### 673. async pool
`Promise.race` orqali bajarilayotgan vazifalar to'plamini cheklab turadi: yangi vazifa qo'shilishidan oldin bittasi tugashini kutadi.

**JS**
```js
async function asyncPool(poolSize, items, iteratorFn) {
  const ret = [];
  const executing = new Set();
  for (const item of items) {
    const p = Promise.resolve().then(() => iteratorFn(item));
    ret.push(p);
    executing.add(p);
    const clean = () => executing.delete(p);
    p.then(clean, clean);
    if (executing.size >= poolSize) await Promise.race(executing);
  }
  return Promise.all(ret);
}
```
**Python**
```python
import asyncio

async def async_pool(pool_size, items, fn):
    sem = asyncio.Semaphore(pool_size)
    async def worker(x):
        async with sem:
            return await fn(x)
    return await asyncio.gather(*(worker(x) for x in items))
```

<a id="m674"></a>
### 674. sleep/delay (Promise)
Berilgan vaqtga "uxlovchi" (bloklamasdan) promise; ixtiyoriy qiymat bilan resolve bo'ladi.

**JS**
```js
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
// await sleep(100);
```
**Python**
```python
import asyncio

async def delay(seconds, value=None):
    await asyncio.sleep(seconds)
    return value
```
**PHP**
```php
function delayPhp(float $seconds): void {
    usleep((int)($seconds * 1_000_000)); // bloklaydi (PHP sinxron)
}
```

<a id="m675"></a>
### 675. timeout wrapper (Promise.race)
Promise'ni vaqt chegarasi bilan o'raydi: kechiksa "timeout" xatosi bilan rad etadi.

**JS**
```js
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("timeout")), ms)
  );
  return Promise.race([promise, timeout]);
}
```
**Python**
```python
import asyncio

async def with_timeout(coro, seconds):
    return await asyncio.wait_for(coro, timeout=seconds)  # TimeoutError tashlaydi
```

<a id="m676"></a>
### 676. retry (backoff bilan)
Vazifa muvaffaqiyatsiz bo'lsa, har urinishda kutish vaqtini ikki barobar oshirib (exponential backoff) qayta uradi.

**JS**
```js
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function retry(fn, { retries = 3, base = 100 } = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (attempt < retries) await sleep(base * 2 ** attempt);
    }
  }
  throw lastErr;
}
```
**Python**
```python
import asyncio

async def retry(fn, retries=3, base=0.01):
    last = None
    for attempt in range(retries + 1):
        try:
            return await fn()
        except Exception as e:
            last = e
            if attempt < retries:
                await asyncio.sleep(base * 2 ** attempt)
    raise last
```
**PHP**
```php
function retryPhp(callable $fn, int $retries = 3, int $baseMs = 10): mixed {
    $last = null;
    for ($attempt = 0; $attempt <= $retries; $attempt++) {
        try {
            return $fn();
        } catch (Throwable $e) {
            $last = $e;
            if ($attempt < $retries) usleep($baseMs * (2 ** $attempt) * 1000);
        }
    }
    throw $last;
}
```

<a id="m677"></a>
### 677. debounce (async)
Tez-tez chaqirishlarni "bosadi": faqat oxirgi chaqiruv `delay` jimlikdan keyin ishlaydi va promise qaytaradi.

**JS**
```js
function debounce(fn, delay) {
  let timer = null;
  let pending = null;
  return (...args) => {
    if (timer) clearTimeout(timer);
    if (!pending) {
      pending = {};
      pending.promise = new Promise((res, rej) => {
        pending.resolve = res;
        pending.reject = rej;
      });
    }
    const cur = pending;
    timer = setTimeout(() => {
      pending = null;
      Promise.resolve(fn(...args)).then(cur.resolve, cur.reject);
    }, delay);
    return cur.promise;
  };
}
```
**Python**
```python
import asyncio

def debounce(fn, delay_s):
    handle = None
    future = None
    loop = asyncio.get_event_loop()
    def debounced(*args):
        nonlocal handle, future
        if handle:
            handle.cancel()
        if future is None or future.done():
            future = loop.create_future()
        cur = future
        handle = loop.call_later(delay_s, lambda: asyncio.ensure_future(_call(cur, *args)))
        return cur
    async def _call(fut, *args):
        try:
            fut.set_result(await fn(*args))
        except Exception as e:
            fut.set_exception(e)
    return debounced
```

<a id="m678"></a>
### 678. throttle (async)
Funksiyani har `interval` da ko'pi bilan bir marta chaqiradi; oraliqdagi chaqiruvlar oxirgi natijani qaytaradi.

**JS**
```js
function throttle(fn, interval) {
  let last = 0;
  let lastResult;
  return async (...args) => {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      lastResult = await fn(...args);
    }
    return lastResult;
  };
}
```
**Python**
```python
import time

def throttle(fn, interval):
    state = {"last": 0.0, "result": None}
    async def throttled(*args):
        now = time.monotonic()
        if now - state["last"] >= interval:
            state["last"] = now
            state["result"] = await fn(*args)
        return state["result"]
    return throttled
```
**PHP**
```php
function throttlePhp(callable $fn, float $interval): callable {
    $last = 0.0; $result = null;
    return function (...$args) use (&$last, &$result, $fn, $interval) {
        $now = microtime(true);
        if ($now - $last >= $interval) {
            $last = $now;
            $result = $fn(...$args);
        }
        return $result;
    };
}
```

<a id="m679"></a>
### 679. async queue (navbat)
Vazifalarni navbatga qo'yadi va bir vaqtda ko'pi bilan `concurrency` tasini bajaradi; har biri uchun promise qaytaradi.

**JS**
```js
class AsyncQueue {
  constructor(concurrency = 1) {
    this.concurrency = concurrency;
    this.running = 0;
    this.queue = [];
  }
  push(task) {
    return new Promise((resolve, reject) => {
      this.queue.push({ task, resolve, reject });
      this._next();
    });
  }
  _next() {
    while (this.running < this.concurrency && this.queue.length) {
      const { task, resolve, reject } = this.queue.shift();
      this.running++;
      Promise.resolve()
        .then(task)
        .then(resolve, reject)
        .finally(() => {
          this.running--;
          this._next();
        });
    }
  }
}
```
**Python**
```python
import asyncio

class AsyncQueue:
    def __init__(self, concurrency=1):
        self.queue = asyncio.Queue()
        self.concurrency = concurrency
        self._workers = []

    async def push(self, coro_fn):
        fut = asyncio.get_event_loop().create_future()
        await self.queue.put((coro_fn, fut))
        return await fut

    async def _worker(self):
        while True:
            coro_fn, fut = await self.queue.get()
            try:
                fut.set_result(await coro_fn())
            except Exception as e:
                fut.set_exception(e)
            self.queue.task_done()

    def start(self):
        self._workers = [asyncio.ensure_future(self._worker())
                         for _ in range(self.concurrency)]
```

<a id="m680"></a>
### 680. semaphore
Bir vaqtda kira oladiganlar sonini `max` bilan cheklaydi: `acquire` da joy bo'lmasa kutadi, `release` da navbatdagini uyg'otadi.

**JS**
```js
class Semaphore {
  constructor(max) {
    this.max = max;
    this.count = 0;
    this.waiters = [];
  }
  async acquire() {
    if (this.count < this.max) { this.count++; return; }
    await new Promise(resolve => this.waiters.push(resolve));
    this.count++;
  }
  release() {
    this.count--;
    const next = this.waiters.shift();
    if (next) next();
  }
}
```
**Python**
```python
# asyncio.Semaphore tayyor bor; o'rganish uchun qo'lda:
import asyncio

class Semaphore:
    def __init__(self, max_count):
        self.max = max_count
        self.count = 0
        self.waiters = []

    async def acquire(self):
        if self.count < self.max:
            self.count += 1
            return
        fut = asyncio.get_event_loop().create_future()
        self.waiters.append(fut)
        await fut
        self.count += 1

    def release(self):
        self.count -= 1
        if self.waiters:
            self.waiters.pop(0).set_result(None)
```
**PHP**
```php
// PHP sinxronida "bir vaqtda" yo'q — semaphore faqat sanagich sifatida:
class SemaphorePhp {
    private int $count = 0;
    public function __construct(private int $max) {}
    public function tryAcquire(): bool {
        if ($this->count < $this->max) { $this->count++; return true; }
        return false;
    }
    public function release(): void { $this->count--; }
}
```

<a id="m681"></a>
### 681. mutex/lock
`max=1` bo'lgan semaphore — bir vaqtda faqat bitta vazifa kritik bo'limga kiradi. `runExclusive` bilan xavfsiz o'raladi.

**JS**
```js
class Mutex {
  constructor() {
    this._locked = false;
    this._waiters = [];
  }
  acquire() {
    return new Promise(resolve => {
      if (!this._locked) { this._locked = true; resolve(); }
      else this._waiters.push(resolve);
    });
  }
  release() {
    const next = this._waiters.shift();
    if (next) next();
    else this._locked = false;
  }
  async runExclusive(fn) {
    await this.acquire();
    try { return await fn(); }
    finally { this.release(); }
  }
}
```
**Python**
```python
import asyncio

class Mutex:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def run_exclusive(self, coro_fn):
        async with self._lock:
            return await coro_fn()
```

<a id="m682"></a>
### 682. producer-consumer
Ishlab chiqaruvchi navbatga element qo'yadi, iste'molchi undan oladi; navbat bo'sh bo'lsa iste'molchi kutadi.

**JS**
```js
class Channel {
  constructor() {
    this.buffer = [];
    this.takers = [];
  }
  put(item) {
    const taker = this.takers.shift();
    if (taker) taker(item);
    else this.buffer.push(item);
  }
  take() {
    if (this.buffer.length) return Promise.resolve(this.buffer.shift());
    return new Promise(resolve => this.takers.push(resolve));
  }
}
```
**Python**
```python
import asyncio

async def producer_consumer(n):
    queue = asyncio.Queue(maxsize=3)
    consumed = []
    async def producer():
        for i in range(n):
            await queue.put(i)
        await queue.put(None)         # tugadi belgisi
    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                break
            consumed.append(item)
    await asyncio.gather(producer(), consumer())
    return consumed
```

<a id="m683"></a>
### 683. async generator (oqim)
Cheksiz oqimdan (`async`/`yield`) faqat birinchi `n` elementni oladi — lazy, talab bo'yicha.

**JS**
```js
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function* counter() {
  let i = 0;
  while (true) { await sleep(0); yield i++; }
}
async function* take(asyncIterable, n) {
  let count = 0;
  for await (const item of asyncIterable) {
    if (count++ >= n) break;
    yield item;
  }
}
```
**Python**
```python
import asyncio

async def counter():
    i = 0
    while True:
        await asyncio.sleep(0)
        yield i
        i += 1

async def take(agen, n):
    out = []
    async for item in agen:
        if len(out) >= n:
            break
        out.append(item)
    return out
```
**PHP**
```php
// PHP generatori sinxron, lekin lazy oqim g'oyasi bir xil:
function counterGen(): Generator {
    $i = 0;
    while (true) yield $i++;
}
function takeGen(Generator $gen, int $n): array {
    $out = [];
    foreach ($gen as $item) {
        if (count($out) >= $n) break;
        $out[] = $item;
    }
    return $out;
}
```

<a id="m684"></a>
### 684. chunked async processing
Katta ro'yxatni `size` o'lchamli bo'laklarga bo'lib, har bo'lakni parallel ishlab, keyingisiga o'tadi (xotira/yuklamani cheklash uchun).

**JS**
```js
async function processInChunks(items, size, fn) {
  const results = [];
  for (let i = 0; i < items.length; i += size) {
    const chunk = items.slice(i, i + size);
    results.push(...await Promise.all(chunk.map(fn)));
  }
  return results;
}
```
**Python**
```python
import asyncio

async def process_in_chunks(items, size, fn):
    results = []
    for i in range(0, len(items), size):
        chunk = items[i:i + size]
        results.extend(await asyncio.gather(*(fn(x) for x in chunk)))
    return results
```
**PHP**
```php
function processInChunksPhp(array $items, int $size, callable $fn): array {
    $results = [];
    foreach (array_chunk($items, $size) as $chunk) {
        foreach ($chunk as $x) $results[] = $fn($x);
    }
    return $results;
}
```

<a id="m685"></a>
### 685. cancellation (AbortController/flag)
Uzoq vazifani tashqaridan bekor qilish: JS da `AbortController.signal`, Python da `asyncio.Event` yoki task `cancel()`.

**JS**
```js
function cancellableDelay(ms, signal) {
  return new Promise((resolve, reject) => {
    if (signal.aborted) return reject(new Error("aborted"));
    const id = setTimeout(resolve, ms);
    signal.addEventListener("abort", () => {
      clearTimeout(id);
      reject(new Error("aborted"));
    }, { once: true });
  });
}
// const ac = new AbortController(); ac.abort();
```
**Python**
```python
import asyncio

async def cancellable_work(event):
    try:
        while not event.is_set():
            await asyncio.sleep(0.001)
        return "cancelled"
    except asyncio.CancelledError:
        return "cancelled"
```

<a id="m686"></a>
### 686. promisify (callback -> Promise)
Eski "error-first callback" uslubidagi funksiyani Promise/awaitable qaytaradigan funksiyaga o'raydi.

**JS**
```js
function promisify(fn) {
  return (...args) =>
    new Promise((resolve, reject) => {
      fn(...args, (err, result) => (err ? reject(err) : resolve(result)));
    });
}
// const readAsync = promisify(fs.readFile);
```
**Python**
```python
import asyncio

def promisify(fn):
    async def wrapper(*args):
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        def callback(err, result):
            if err:
                fut.set_exception(err if isinstance(err, Exception) else Exception(err))
            else:
                fut.set_result(result)
        fn(*args, callback)
        return await fut
    return wrapper
```

<a id="m687"></a>
### 687. async reduce (ketma-ket)
Ro'yxatni asinxron yig'indiga keltiradi, lekin har qadam oldingisini kutadi (tartib va akkumulyator muhim bo'lganda).

**JS**
```js
async function reduceAsync(items, fn, initial) {
  let acc = initial;
  for (const item of items) acc = await fn(acc, item);
  return acc;
}
```
**Python**
```python
async def reduce_async(items, fn, initial):
    acc = initial
    for item in items:
        acc = await fn(acc, item)
    return acc
```
**PHP**
```php
function reduceAsyncPhp(array $items, callable $fn, mixed $initial): mixed {
    $acc = $initial;
    foreach ($items as $item) $acc = $fn($acc, $item);
    return $acc;
}
```

<a id="m688"></a>
### 688. parallel with limit
Tayyor vazifalar ro'yxatini cheklangan ishchilar bilan parallel bajaradi; natija tartibini saqlaydi (672-masalaning "task'lar" varianti).

**JS**
```js
async function parallelLimit(tasks, limit) {
  const results = new Array(tasks.length);
  let i = 0;
  const workers = Array.from({ length: Math.min(limit, tasks.length) }, async () => {
    while (i < tasks.length) {
      const idx = i++;
      results[idx] = await tasks[idx]();
    }
  });
  await Promise.all(workers);
  return results;
}
```
**Python**
```python
import asyncio

async def parallel_limit(tasks, limit):
    sem = asyncio.Semaphore(limit)
    async def bound(i, t):
        async with sem:
            return i, await t()
    pairs = await asyncio.gather(*(bound(i, t) for i, t in enumerate(tasks)))
    out = [None] * len(tasks)
    for i, v in pairs:
        out[i] = v
    return out
```

<a id="m689"></a>
### 689. batch processor
Kelayotgan elementlarni to'plab, hajm chegarasiga (`maxSize`) yoki vaqt chegarasiga (`maxWait`) yetganda bitta partiya sifatida yuboradi.

**JS**
```js
class BatchProcessor {
  constructor(flushFn, { maxSize = 10, maxWait = 50 } = {}) {
    this.flushFn = flushFn;
    this.maxSize = maxSize;
    this.maxWait = maxWait;
    this.batch = [];
    this.timer = null;
  }
  add(item) {
    this.batch.push(item);
    if (this.batch.length >= this.maxSize) this.flush();
    else if (!this.timer) this.timer = setTimeout(() => this.flush(), this.maxWait);
  }
  flush() {
    if (this.timer) { clearTimeout(this.timer); this.timer = null; }
    if (this.batch.length === 0) return;
    const items = this.batch;
    this.batch = [];
    this.flushFn(items);
  }
}
```
**Python**
```python
import asyncio

class BatchProcessor:
    def __init__(self, flush_fn, max_size=10, max_wait=0.05):
        self.flush_fn = flush_fn
        self.max_size = max_size
        self.max_wait = max_wait
        self.batch = []
        self.handle = None

    def add(self, item):
        self.batch.append(item)
        if len(self.batch) >= self.max_size:
            self.flush()
        elif self.handle is None:
            self.handle = asyncio.get_event_loop().call_later(self.max_wait, self.flush)

    def flush(self):
        if self.handle:
            self.handle.cancel()
            self.handle = None
        if not self.batch:
            return
        items, self.batch = self.batch, []
        self.flush_fn(items)
```
**PHP**
```php
class BatchProcessorPhp {
    private array $batch = [];
    public function __construct(private $flushFn, private int $maxSize = 3) {}
    public function add(mixed $item): void {
        $this->batch[] = $item;
        if (count($this->batch) >= $this->maxSize) $this->flush();
    }
    public function flush(): void {
        if (!$this->batch) return;
        ($this->flushFn)($this->batch);
        $this->batch = [];
    }
}
```

<a id="m690"></a>
### 690. rate-limited async ishlov
Token bucket: har `intervalMs` da `maxPerInterval` ta token tiklanadi; token bo'lmasa chaqiruv navbatga turadi.

**JS**
```js
function rateLimiter(maxPerInterval, intervalMs) {
  let tokens = maxPerInterval;
  const queue = [];
  setInterval(() => {
    tokens = maxPerInterval;
    while (tokens > 0 && queue.length) { tokens--; queue.shift()(); }
  }, intervalMs).unref?.();
  return () =>
    new Promise(resolve => {
      if (tokens > 0) { tokens--; resolve(); }
      else queue.push(resolve);
    });
}
```
**Python**
```python
import asyncio, time

class RateLimiter:
    def __init__(self, max_per_interval, interval):
        self.max = max_per_interval
        self.interval = interval
        self.tokens = max_per_interval
        self.last = time.monotonic()

    async def acquire(self):
        now = time.monotonic()
        if now - self.last >= self.interval:
            self.tokens = self.max
            self.last = now
        while self.tokens <= 0:
            await asyncio.sleep(self.interval)
            self.tokens = self.max
            self.last = time.monotonic()
        self.tokens -= 1
```

<a id="m691"></a>
### 691. microtask vs macrotask (demo)
`Promise.then` — microtask (joriy ish tugagach darhol), `setTimeout` — macrotask (keyingi "tick"da). Demo sinxron kod birinchi tugashini ko'rsatadi.

**JS**
```js
function demoOrder() {
  const order = [];
  order.push("sync-start");
  setTimeout(() => order.push("macrotask"), 0);          // eng oxirida
  Promise.resolve().then(() => order.push("microtask")); // sync'dan keyin
  order.push("sync-end");
  return order; // hozircha: ["sync-start", "sync-end"]
}
// To'liq tartib: sync-start, sync-end, microtask, macrotask
```
**Python**
```python
import asyncio

async def demo_order():
    order = []
    loop = asyncio.get_event_loop()
    order.append("sync-start")
    loop.call_later(0, lambda: order.append("later"))  # macrotask kabi
    loop.call_soon(lambda: order.append("soon"))        # microtask kabi
    order.append("sync-end")
    await asyncio.sleep(0.01)
    return order  # ["sync-start", "sync-end", "soon", "later"]
```

<a id="m692"></a>
### 692. async memoize (in-flight dedup)
Bir xil kalit uchun bir vaqtda kelgan chaqiruvlarni birlashtiradi: natija o'rniga promise'ni keshlaydi, shuning uchun ish faqat bir marta bajariladi.

**JS**
```js
function memoizeAsync(fn) {
  const cache = new Map();
  return (key, ...args) => {
    if (cache.has(key)) return cache.get(key);
    const promise = Promise.resolve(fn(key, ...args)).catch(err => {
      cache.delete(key); // xato bo'lsa keshni tozalaymiz
      throw err;
    });
    cache.set(key, promise);
    return promise;
  };
}
```
**Python**
```python
import asyncio

def memoize_async(fn):
    cache = {}
    def wrapper(key, *args):
        if key in cache:
            return cache[key]
        async def run():
            try:
                return await fn(key, *args)
            except Exception:
                cache.pop(key, None)
                raise
        task = asyncio.ensure_future(run())
        cache[key] = task
        return task
    return wrapper
```
**PHP**
```php
// PHP sinxron: "in-flight" tushunchasi yo'q, oddiy keshlash:
function memoizePhp(callable $fn): callable {
    $cache = [];
    return function (string $key, ...$args) use (&$cache, $fn) {
        return $cache[$key] ??= $fn($key, ...$args);
    };
}
```

<a id="m693"></a>
### 693. fan-out/fan-in
Bir kirishni ko'p ishchiga tarqatadi (fan-out), keyin natijalarni bitta qiymatga yig'adi (fan-in).

**JS**
```js
async function fanOutFanIn(input, workers) {
  const partial = await Promise.all(workers.map(w => w(input))); // fan-out
  return partial.reduce((a, b) => a + b, 0);                      // fan-in
}
```
**Python**
```python
import asyncio

async def fan_out_fan_in(value, workers):
    partial = await asyncio.gather(*(w(value) for w in workers))  # fan-out
    return sum(partial)                                            # fan-in
```

<a id="m694"></a>
### 694. waitGroup (barcha tugaguncha)
Go uslubidagi `WaitGroup`: bir nechta vazifa ishga tushiriladi, `wait()` ularning hammasi tugaguncha bloklaydi.

**JS**
```js
class WaitGroup {
  constructor() {
    this.count = 0;
    this.resolvers = [];
  }
  add(n = 1) { this.count += n; }
  done() {
    this.count--;
    if (this.count === 0) {
      this.resolvers.forEach(r => r());
      this.resolvers = [];
    }
  }
  wait() {
    if (this.count === 0) return Promise.resolve();
    return new Promise(resolve => this.resolvers.push(resolve));
  }
}
```
**Python**
```python
import asyncio

async def wait_group(coro_fns):
    async with asyncio.TaskGroup() as tg:        # Python 3.11+
        tasks = [tg.create_task(fn()) for fn in coro_fns]
    return [t.result() for t in tasks]            # blok tugaganda hammasi tayyor
```

<a id="m695"></a>
### 695. debounce + leading/trailing
Debounce'ning ikki rejimi: `leading` — birinchi chaqiruvda darhol; `trailing` — jimlikdan keyin oxirgi chaqiruvda.

**JS**
```js
function debounceLT(fn, delay, { leading = false, trailing = true } = {}) {
  let timer = null;
  return (...args) => {
    const callNow = leading && !timer;
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      if (trailing && !callNow) fn(...args);
    }, delay);
    if (callNow) fn(...args);
  };
}
```
**Python**
```python
import asyncio

def debounce_lt(fn, delay_s, leading=False, trailing=True):
    state = {"handle": None}
    loop = asyncio.get_event_loop()
    def debounced(*args):
        call_now = leading and state["handle"] is None
        if state["handle"]:
            state["handle"].cancel()
        def fire():
            state["handle"] = None
            if trailing and not call_now:
                fn(*args)
        state["handle"] = loop.call_later(delay_s, fire)
        if call_now:
            fn(*args)
    return debounced
```

<a id="m696"></a>
### 696. deadlock'dan qochish (lock tartibi)
Ikki lock kerak bo'lsa, ularni doim bir xil tartibda (masalan `id` bo'yicha) olish — bu o'zaro kutishni (deadlock) yo'q qiladi.

**JS**
```js
async function transfer(from, to, amount) {
  const [first, second] = from.id < to.id ? [from, to] : [to, from]; // doimiy tartib
  await first.lock.acquire();
  try {
    await second.lock.acquire();
    try {
      from.balance -= amount;
      to.balance += amount;
    } finally { second.lock.release(); }
  } finally { first.lock.release(); }
}
```
**Python**
```python
import asyncio

async def transfer(frm, to, amount):
    first, second = (frm, to) if frm["id"] < to["id"] else (to, frm)  # doimiy tartib
    async with first["lock"]:
        async with second["lock"]:
            frm["balance"] -= amount
            to["balance"] += amount
```
**PHP**
```php
// PHP da Fiber bilan kooperativ navbat: lock tartibini ko'rsatish o'rniga,
// Fiber'lar suspend/resume orqali oldindan belgilangan tartibda davom etadi.
function fiberDemo(): array {
    $log = [];
    $fibers = [];
    foreach ([3, 1, 2] as $id) {
        $fibers[] = new Fiber(function () use ($id, &$log) {
            Fiber::suspend();          // boshqalarga navbat beradi
            $log[] = $id;
        });
    }
    foreach ($fibers as $f) $f->start();   // hammasi suspend bo'ladi
    foreach ($fibers as $f) $f->resume();  // belgilangan tartibda davom etadi
    return $log; // [3, 1, 2]
}
```
