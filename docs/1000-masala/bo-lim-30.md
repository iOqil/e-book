<a id="b30"></a>
# 30-bo'lim: Dizayn patternlar (OOP)

<sub>[↑ Mundarijaga qaytish](README.md#mundarija)</sub>

> Dizayn patternlar (design patterns) — bu obyektga yo'naltirilgan dasturlashda tez-tez uchraydigan
> muammolarga sinalgan, qayta ishlatiladigan yechim shablonlari. Ular GoF (Gang of Four) kitobida
> uchta guruhga ajratilgan: yaratuvchi (creational), strukturaviy (structural) va xulq-atvor
> (behavioral) patternlar. Bu bo'limda 35 ta klassik (va bir nechta amaliy) pattern JS, PHP va Python
> klasslari yordamida qisqa, idiomatik misollarda ko'rsatiladi. Maqsad — algoritm tezligi emas,
> balki strukturani tushunish, shuning uchun Big-O qatori bu yerda ko'pincha tashlab ketiladi.

<a id="m587"></a>
### 587. Singleton
Klassdan butun dastur davomida faqat bitta nusxa (instance) bo'lishini ta'minlaydi.

**JS**
```js
class Database {
  static #instance = null;
  constructor() { this.connections = 0; }
  static getInstance() {
    if (!Database.#instance) Database.#instance = new Database();
    return Database.#instance;
  }
}
// Database.getInstance() === Database.getInstance() // true
```
**PHP**
```php
class Database {
    private static ?Database $instance = null;
    public int $connections = 0;
    private function __construct() {}
    public static function getInstance(): Database {
        return self::$instance ??= new Database();
    }
}
// Database::getInstance() === Database::getInstance() // true
```
**Python**
```python
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connections = 0
        return cls._instance
# Database() is Database()  # True
```

<a id="m588"></a>
### 588. Factory Method
Obyekt yaratishni alohida metodga topshiradi; qaysi konkret klass yaratilishini quyi klasslar hal qiladi.

**JS**
```js
class Dog { speak() { return "Woof"; } }
class Cat { speak() { return "Meow"; } }
class AnimalFactory {
  create(kind) {
    if (kind === "dog") return new Dog();
    if (kind === "cat") return new Cat();
    throw new Error("noma'lum: " + kind);
  }
}
// new AnimalFactory().create("dog").speak() // "Woof"
```
**PHP**
```php
interface Animal { public function speak(): string; }
class Dog implements Animal { public function speak(): string { return "Woof"; } }
class Cat implements Animal { public function speak(): string { return "Meow"; } }
class AnimalFactory {
    public function create(string $kind): Animal {
        return match ($kind) {
            "dog" => new Dog(),
            "cat" => new Cat(),
            default => throw new InvalidArgumentException("noma'lum: $kind"),
        };
    }
}
```
**Python**
```python
class Dog:
    def speak(self): return "Woof"

class Cat:
    def speak(self): return "Meow"

class AnimalFactory:
    def create(self, kind):
        match kind:
            case "dog": return Dog()
            case "cat": return Cat()
            case _: raise ValueError(f"noma'lum: {kind}")
# AnimalFactory().create("cat").speak()  # "Meow"
```

<a id="m589"></a>
### 589. Abstract Factory
O'zaro bog'liq obyektlar oilasini (masalan, bir uslubdagi tugma va checkbox) yaratuvchi interfeys.

**JS**
```js
class LightButton { render() { return "[light btn]"; } }
class DarkButton { render() { return "[dark btn]"; } }
class LightTheme { createButton() { return new LightButton(); } }
class DarkTheme { createButton() { return new DarkButton(); } }
function renderUI(factory) { return factory.createButton().render(); }
// renderUI(new DarkTheme()) // "[dark btn]"
```
**PHP**
```php
interface Button { public function render(): string; }
class LightButton implements Button { public function render(): string { return "[light btn]"; } }
class DarkButton implements Button { public function render(): string { return "[dark btn]"; } }
interface Theme { public function createButton(): Button; }
class LightTheme implements Theme { public function createButton(): Button { return new LightButton(); } }
class DarkTheme implements Theme { public function createButton(): Button { return new DarkButton(); } }
function renderUI(Theme $factory): string { return $factory->createButton()->render(); }
```
**Python**
```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self): ...

class LightButton(Button):
    def render(self): return "[light btn]"

class DarkButton(Button):
    def render(self): return "[dark btn]"

class Theme(ABC):
    @abstractmethod
    def create_button(self): ...

class LightTheme(Theme):
    def create_button(self): return LightButton()

class DarkTheme(Theme):
    def create_button(self): return DarkButton()

def render_ui(factory): return factory.create_button().render()
# render_ui(DarkTheme())  # "[dark btn]"
```

<a id="m590"></a>
### 590. Builder
Murakkab obyektni bosqichma-bosqich, o'qiladigan tarzda quradi.

**JS**
```js
class Burger {
  constructor() { this.parts = []; }
}
class BurgerBuilder {
  constructor() { this.burger = new Burger(); }
  add(part) { this.burger.parts.push(part); return this; }
  build() { return this.burger; }
}
// new BurgerBuilder().add("bun").add("patty").add("bun").build().parts
// ["bun","patty","bun"]
```
**PHP**
```php
class Burger {
    public array $parts = [];
}
class BurgerBuilder {
    private Burger $burger;
    public function __construct() { $this->burger = new Burger(); }
    public function add(string $part): static { $this->burger->parts[] = $part; return $this; }
    public function build(): Burger { return $this->burger; }
}
// (new BurgerBuilder())->add("bun")->add("patty")->build()->parts
```
**Python**
```python
class Burger:
    def __init__(self):
        self.parts = []

class BurgerBuilder:
    def __init__(self):
        self.burger = Burger()

    def add(self, part):
        self.burger.parts.append(part)
        return self

    def build(self):
        return self.burger
# BurgerBuilder().add("bun").add("patty").add("bun").build().parts
```

<a id="m591"></a>
### 591. Prototype
Mavjud obyektni nusxalash (clone) orqali yangi obyekt yaratadi.

**JS**
```js
class Shape {
  constructor(color, size) { this.color = color; this.size = size; }
  clone() { return new Shape(this.color, this.size); }
}
// const a = new Shape("red", 5); const b = a.clone(); b.color = "blue";
// a.color // "red"
```
**PHP**
```php
class Shape {
    public function __construct(public string $color, public int $size) {}
    public function cloneSelf(): static { return clone $this; }
}
// $a = new Shape("red", 5); $b = $a->cloneSelf(); $b->color = "blue";
```
**Python**
```python
import copy

class Shape:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def clone(self):
        return copy.deepcopy(self)
# a = Shape("red", 5); b = a.clone(); b.color = "blue"; a.color == "red"
```

<a id="m592"></a>
### 592. Adapter
Mos kelmaydigan interfeysni mijoz kutgan interfeysga moslashtiradi.

**JS**
```js
class CelsiusSensor { read() { return 25; } }          // °C qaytaradi
class FahrenheitAdapter {
  constructor(sensor) { this.sensor = sensor; }
  readF() { return this.sensor.read() * 9 / 5 + 32; }  // °F
}
// new FahrenheitAdapter(new CelsiusSensor()).readF() // 77
```
**PHP**
```php
class CelsiusSensor { public function read(): float { return 25; } }
class FahrenheitAdapter {
    public function __construct(private CelsiusSensor $sensor) {}
    public function readF(): float { return $this->sensor->read() * 9 / 5 + 32; }
}
// (new FahrenheitAdapter(new CelsiusSensor()))->readF() // 77
```
**Python**
```python
class CelsiusSensor:
    def read(self): return 25  # °C

class FahrenheitAdapter:
    def __init__(self, sensor):
        self.sensor = sensor

    def read_f(self):
        return self.sensor.read() * 9 / 5 + 32  # °F
# FahrenheitAdapter(CelsiusSensor()).read_f()  # 77.0
```

<a id="m593"></a>
### 593. Bridge
Abstraksiya (shakl) va realizatsiyani (chizish usuli) bir-biridan ajratib, ularni mustaqil kengaytiradi.

**JS**
```js
class Vector { render(shape) { return `<svg:${shape}>`; } }
class Raster { render(shape) { return `[pixels:${shape}]`; } }
class Circle {
  constructor(renderer) { this.renderer = renderer; }
  draw() { return this.renderer.render("circle"); }
}
// new Circle(new Vector()).draw() // "<svg:circle>"
```
**PHP**
```php
interface Renderer { public function render(string $shape): string; }
class Vector implements Renderer { public function render(string $s): string { return "<svg:$s>"; } }
class Raster implements Renderer { public function render(string $s): string { return "[pixels:$s]"; } }
class Circle {
    public function __construct(private Renderer $renderer) {}
    public function draw(): string { return $this->renderer->render("circle"); }
}
```
**Python**
```python
class Vector:
    def render(self, shape): return f"<svg:{shape}>"

class Raster:
    def render(self, shape): return f"[pixels:{shape}]"

class Circle:
    def __init__(self, renderer):
        self.renderer = renderer

    def draw(self):
        return self.renderer.render("circle")
# Circle(Vector()).draw()  # "<svg:circle>"
```

<a id="m594"></a>
### 594. Composite
Yagona obyekt va obyektlar guruhini bir xil interfeys orqali daraxt ko'rinishida ishlatadi.

**JS**
```js
class File {
  constructor(size) { this.size = size; }
  total() { return this.size; }
}
class Folder {
  constructor() { this.children = []; }
  add(node) { this.children.push(node); return this; }
  total() { return this.children.reduce((s, c) => s + c.total(), 0); }
}
// new Folder().add(new File(3)).add(new File(7)).total() // 10
```
**PHP**
```php
interface Node { public function total(): int; }
class FileNode implements Node {
    public function __construct(private int $size) {}
    public function total(): int { return $this->size; }
}
class Folder implements Node {
    private array $children = [];
    public function add(Node $n): static { $this->children[] = $n; return $this; }
    public function total(): int {
        return array_sum(array_map(fn(Node $c) => $c->total(), $this->children));
    }
}
```
**Python**
```python
class File:
    def __init__(self, size):
        self.size = size

    def total(self):
        return self.size

class Folder:
    def __init__(self):
        self.children = []

    def add(self, node):
        self.children.append(node)
        return self

    def total(self):
        return sum(c.total() for c in self.children)
# Folder().add(File(3)).add(File(7)).total()  # 10
```

<a id="m595"></a>
### 595. Decorator
Obyektni o'rab olib, asl interfeysni o'zgartirmasdan unga yangi xulq qo'shadi.

**JS**
```js
class Coffee { cost() { return 2; } }
class MilkDecorator {
  constructor(coffee) { this.coffee = coffee; }
  cost() { return this.coffee.cost() + 0.5; }
}
class SugarDecorator {
  constructor(coffee) { this.coffee = coffee; }
  cost() { return this.coffee.cost() + 0.25; }
}
// new SugarDecorator(new MilkDecorator(new Coffee())).cost() // 2.75
```
**PHP**
```php
interface Drink { public function cost(): float; }
class Coffee implements Drink { public function cost(): float { return 2; } }
class MilkDecorator implements Drink {
    public function __construct(private Drink $d) {}
    public function cost(): float { return $this->d->cost() + 0.5; }
}
class SugarDecorator implements Drink {
    public function __construct(private Drink $d) {}
    public function cost(): float { return $this->d->cost() + 0.25; }
}
```
**Python**
```python
class Coffee:
    def cost(self): return 2

class MilkDecorator:
    def __init__(self, drink):
        self.drink = drink

    def cost(self):
        return self.drink.cost() + 0.5

class SugarDecorator:
    def __init__(self, drink):
        self.drink = drink

    def cost(self):
        return self.drink.cost() + 0.25
# SugarDecorator(MilkDecorator(Coffee())).cost()  # 2.75
```

<a id="m596"></a>
### 596. Facade
Murakkab quyi tizimlarga sodda, yagona kirish nuqtasini taqdim etadi.

**JS**
```js
class CPU { boot() { return "cpu"; } }
class Memory { load() { return "mem"; } }
class Disk { read() { return "disk"; } }
class Computer {
  constructor() { this.cpu = new CPU(); this.mem = new Memory(); this.disk = new Disk(); }
  start() { return [this.cpu.boot(), this.mem.load(), this.disk.read()].join("+"); }
}
// new Computer().start() // "cpu+mem+disk"
```
**PHP**
```php
class CPU { public function boot(): string { return "cpu"; } }
class Memory { public function load(): string { return "mem"; } }
class Disk { public function read(): string { return "disk"; } }
class Computer {
    private CPU $cpu; private Memory $mem; private Disk $disk;
    public function __construct() { $this->cpu = new CPU(); $this->mem = new Memory(); $this->disk = new Disk(); }
    public function start(): string {
        return implode("+", [$this->cpu->boot(), $this->mem->load(), $this->disk->read()]);
    }
}
```
**Python**
```python
class CPU:
    def boot(self): return "cpu"

class Memory:
    def load(self): return "mem"

class Disk:
    def read(self): return "disk"

class Computer:
    def __init__(self):
        self.cpu, self.mem, self.disk = CPU(), Memory(), Disk()

    def start(self):
        return "+".join([self.cpu.boot(), self.mem.load(), self.disk.read()])
# Computer().start()  # "cpu+mem+disk"
```

<a id="m597"></a>
### 597. Flyweight
Ko'p takrorlanadigan o'zgarmas holatni ulashib, xotirani tejaydi.

**JS**
```js
class TreeTypeFactory {
  constructor() { this.types = new Map(); }
  get(name) {
    if (!this.types.has(name)) this.types.set(name, { name });
    return this.types.get(name);   // bir xil nom — bir xil obyekt
  }
}
// const f = new TreeTypeFactory(); f.get("oak") === f.get("oak") // true
```
**PHP**
```php
class TreeTypeFactory {
    private array $types = [];
    public function get(string $name): object {
        return $this->types[$name] ??= (object)["name" => $name];
    }
}
// $f = new TreeTypeFactory(); $f->get("oak") === $f->get("oak") // true
```
**Python**
```python
class TreeTypeFactory:
    def __init__(self):
        self._types = {}

    def get(self, name):
        if name not in self._types:
            self._types[name] = {"name": name}
        return self._types[name]
# f = TreeTypeFactory(); f.get("oak") is f.get("oak")  # True
```

<a id="m598"></a>
### 598. Proxy
Asl obyektga kirishni nazorat qiluvchi o'rinbosar (masalan, lazy yuklash yoki keshlash).

**JS**
```js
class HeavyImage {
  constructor(file) { this.file = file; /* og'ir yuklash */ }
  display() { return `image:${this.file}`; }
}
class ImageProxy {
  constructor(file) { this.file = file; this.real = null; }
  display() {                       // faqat kerak bo'lganda yaratiladi
    if (!this.real) this.real = new HeavyImage(this.file);
    return this.real.display();
  }
}
// new ImageProxy("a.png").display() // "image:a.png"
```
**PHP**
```php
class HeavyImage {
    public function __construct(private string $file) {}
    public function display(): string { return "image:{$this->file}"; }
}
class ImageProxy {
    private ?HeavyImage $real = null;
    public function __construct(private string $file) {}
    public function display(): string {
        $this->real ??= new HeavyImage($this->file);
        return $this->real->display();
    }
}
```
**Python**
```python
class HeavyImage:
    def __init__(self, file):
        self.file = file  # og'ir yuklash

    def display(self):
        return f"image:{self.file}"

class ImageProxy:
    def __init__(self, file):
        self.file = file
        self._real = None

    def display(self):
        if self._real is None:
            self._real = HeavyImage(self.file)
        return self._real.display()
# ImageProxy("a.png").display()  # "image:a.png"
```

<a id="m599"></a>
### 599. Chain of Responsibility
So'rovni ishlovchilar zanjiri bo'ylab uzatadi; biri uddalay olmasa, keyingisiga o'tadi.

**JS**
```js
class Handler {
  constructor(level) { this.level = level; this.next = null; }
  setNext(h) { this.next = h; return h; }
  handle(amount) {
    if (amount <= this.level) return `${this.level} to'ladi`;
    return this.next ? this.next.handle(amount) : "rad etildi";
  }
}
// const a = new Handler(100); a.setNext(new Handler(1000));
// a.handle(500) // "1000 to'ladi"
```
**PHP**
```php
class Handler {
    private ?Handler $next = null;
    public function __construct(private int $level) {}
    public function setNext(Handler $h): Handler { $this->next = $h; return $h; }
    public function handle(int $amount): string {
        if ($amount <= $this->level) return "{$this->level} to'ladi";
        return $this->next ? $this->next->handle($amount) : "rad etildi";
    }
}
```
**Python**
```python
class Handler:
    def __init__(self, level):
        self.level = level
        self.next = None

    def set_next(self, h):
        self.next = h
        return h

    def handle(self, amount):
        if amount <= self.level:
            return f"{self.level} to'ladi"
        return self.next.handle(amount) if self.next else "rad etildi"
# a = Handler(100); a.set_next(Handler(1000)); a.handle(500)  # "1000 to'ladi"
```

<a id="m600"></a>
### 600. Command
So'rovni alohida obyekt sifatida qadoqlaydi; bu uni navbatga qo'yish va undo qilishni osonlashtiradi.

**JS**
```js
class Light { constructor() { this.on = false; } }
class TurnOn {
  constructor(light) { this.light = light; }
  execute() { this.light.on = true; }
  undo() { this.light.on = false; }
}
// const l = new Light(); const cmd = new TurnOn(l);
// cmd.execute(); l.on // true ; cmd.undo(); l.on // false
```
**PHP**
```php
class Light { public bool $on = false; }
interface Command { public function execute(): void; public function undo(): void; }
class TurnOn implements Command {
    public function __construct(private Light $light) {}
    public function execute(): void { $this->light->on = true; }
    public function undo(): void { $this->light->on = false; }
}
```
**Python**
```python
class Light:
    def __init__(self):
        self.on = False

class TurnOn:
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on = True

    def undo(self):
        self.light.on = False
# l = Light(); cmd = TurnOn(l); cmd.execute(); l.on  # True
```

<a id="m601"></a>
### 601. Iterator
Kolleksiya ichki tuzilishini ochmasdan, elementlar bo'ylab ketma-ket yurish imkonini beradi.

**JS**
```js
class Range {
  constructor(start, end) { this.start = start; this.end = end; }
  *[Symbol.iterator]() {
    for (let i = this.start; i < this.end; i++) yield i;
  }
}
// [...new Range(1, 4)] // [1, 2, 3]
```
**PHP**
```php
class RangeColl implements IteratorAggregate {
    public function __construct(private int $start, private int $end) {}
    public function getIterator(): Generator {
        for ($i = $this->start; $i < $this->end; $i++) yield $i;
    }
}
// iterator_to_array(new RangeColl(1, 4)) // [1, 2, 3]
```
**Python**
```python
class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        i = self.start
        while i < self.end:
            yield i
            i += 1
# list(Range(1, 4))  # [1, 2, 3]
```

<a id="m602"></a>
### 602. Mediator
Obyektlar bir-biri bilan to'g'ridan-to'g'ri emas, markaziy vositachi (mediator) orqali muloqot qiladi.

**JS**
```js
class ChatRoom {
  constructor() { this.users = []; this.log = []; }
  register(user) { user.room = this; this.users.push(user); }
  send(from, msg) { this.log.push(`${from}: ${msg}`); }
}
class User {
  constructor(name) { this.name = name; this.room = null; }
  say(msg) { this.room.send(this.name, msg); }
}
// const r = new ChatRoom(); const u = new User("Ali"); r.register(u);
// u.say("salom"); r.log // ["Ali: salom"]
```
**PHP**
```php
class ChatRoom {
    public array $users = [];
    public array $log = [];
    public function register(User $u): void { $u->room = $this; $this->users[] = $u; }
    public function send(string $from, string $msg): void { $this->log[] = "$from: $msg"; }
}
class User {
    public ?ChatRoom $room = null;
    public function __construct(public string $name) {}
    public function say(string $msg): void { $this->room->send($this->name, $msg); }
}
```
**Python**
```python
class ChatRoom:
    def __init__(self):
        self.users = []
        self.log = []

    def register(self, user):
        user.room = self
        self.users.append(user)

    def send(self, sender, msg):
        self.log.append(f"{sender}: {msg}")

class User:
    def __init__(self, name):
        self.name = name
        self.room = None

    def say(self, msg):
        self.room.send(self.name, msg)
# r = ChatRoom(); u = User("Ali"); r.register(u); u.say("salom"); r.log
```

<a id="m603"></a>
### 603. Memento
Obyektning ichki holatini inkapsulyatsiyani buzmasdan saqlaydi va keyin tiklaydi (undo).

**JS**
```js
class Editor {
  constructor() { this.text = ""; }
  save() { return { text: this.text }; }       // memento
  restore(m) { this.text = m.text; }
}
// const e = new Editor(); e.text = "v1"; const m = e.save();
// e.text = "v2"; e.restore(m); e.text // "v1"
```
**PHP**
```php
class Editor {
    public string $text = "";
    public function save(): array { return ["text" => $this->text]; }
    public function restore(array $m): void { $this->text = $m["text"]; }
}
// $e = new Editor(); $e->text = "v1"; $m = $e->save();
// $e->text = "v2"; $e->restore($m); $e->text // "v1"
```
**Python**
```python
class Editor:
    def __init__(self):
        self.text = ""

    def save(self):
        return {"text": self.text}  # memento

    def restore(self, m):
        self.text = m["text"]
# e = Editor(); e.text = "v1"; m = e.save(); e.text = "v2"; e.restore(m); e.text
```

<a id="m604"></a>
### 604. Observer
Subyekt holati o'zgarganda unga obuna bo'lgan barcha kuzatuvchilarni avtomatik xabardor qiladi.

**JS**
```js
class Subject {
  constructor() { this.observers = []; }
  subscribe(fn) { this.observers.push(fn); }
  notify(data) { this.observers.forEach(fn => fn(data)); }
}
// const s = new Subject(); const got = [];
// s.subscribe(x => got.push(x)); s.notify(7); got // [7]
```
**PHP**
```php
class Subject {
    private array $observers = [];
    public function subscribe(callable $fn): void { $this->observers[] = $fn; }
    public function notify($data): void {
        foreach ($this->observers as $fn) $fn($data);
    }
}
```
**Python**
```python
class Subject:
    def __init__(self):
        self.observers = []

    def subscribe(self, fn):
        self.observers.append(fn)

    def notify(self, data):
        for fn in self.observers:
            fn(data)
# s = Subject(); got = []; s.subscribe(got.append); s.notify(7); got  # [7]
```

<a id="m605"></a>
### 605. State
Obyekt ichki holatiga qarab o'z xulqini o'zgartiradi; har bir holat alohida klassda.

**JS**
```js
class RedLight { next() { return new GreenLight(); } name() { return "red"; } }
class GreenLight { next() { return new YellowLight(); } name() { return "green"; } }
class YellowLight { next() { return new RedLight(); } name() { return "yellow"; } }
class TrafficLight {
  constructor() { this.state = new RedLight(); }
  change() { this.state = this.state.next(); return this.state.name(); }
}
// const t = new TrafficLight(); t.change() // "green"
```
**PHP**
```php
interface LightState { public function next(): LightState; public function name(): string; }
class RedLight implements LightState { public function next(): LightState { return new GreenLight(); } public function name(): string { return "red"; } }
class GreenLight implements LightState { public function next(): LightState { return new YellowLight(); } public function name(): string { return "green"; } }
class YellowLight implements LightState { public function next(): LightState { return new RedLight(); } public function name(): string { return "yellow"; } }
class TrafficLight {
    private LightState $state;
    public function __construct() { $this->state = new RedLight(); }
    public function change(): string { $this->state = $this->state->next(); return $this->state->name(); }
}
```
**Python**
```python
class RedLight:
    def next(self): return GreenLight()
    def name(self): return "red"

class GreenLight:
    def next(self): return YellowLight()
    def name(self): return "green"

class YellowLight:
    def next(self): return RedLight()
    def name(self): return "yellow"

class TrafficLight:
    def __init__(self):
        self.state = RedLight()

    def change(self):
        self.state = self.state.next()
        return self.state.name()
# TrafficLight().change()  # "green"
```

<a id="m606"></a>
### 606. Strategy
Almashtiriladigan algoritmlar oilasini inkapsulyatsiya qiladi va ularni ish vaqtida tanlaydi.

**JS**
```js
const asc = (a, b) => a - b;
const desc = (a, b) => b - a;
class Sorter {
  constructor(strategy) { this.strategy = strategy; }
  sort(arr) { return [...arr].sort(this.strategy); }
}
// new Sorter(desc).sort([1, 3, 2]) // [3, 2, 1]
```
**PHP**
```php
class Sorter {
    public function __construct(private $strategy) {}
    public function sort(array $arr): array { usort($arr, $this->strategy); return $arr; }
}
$asc = fn($a, $b) => $a - $b;
$desc = fn($a, $b) => $b - $a;
// (new Sorter($desc))->sort([1, 3, 2]) // [3, 2, 1]
```
**Python**
```python
class Sorter:
    def __init__(self, strategy):
        self.strategy = strategy

    def sort(self, arr):
        return sorted(arr, key=self.strategy)
# Sorter(lambda x: -x).sort([1, 3, 2])  # [3, 2, 1]
```

<a id="m607"></a>
### 607. Template Method
Algoritm skeletini bazaviy klassda belgilaydi, ayrim qadamlarni quyi klasslarga qoldiradi.

**JS**
```js
class Report {
  generate() { return [this.header(), this.body(), "--end--"].join("\n"); }
  header() { return "=== Report ==="; }
  body() { throw new Error("body() ni amalga oshiring"); }
}
class SalesReport extends Report {
  body() { return "savdo: 100"; }
}
// new SalesReport().generate().includes("savdo: 100") // true
```
**PHP**
```php
abstract class Report {
    public function generate(): string { return implode("\n", [$this->header(), $this->body(), "--end--"]); }
    protected function header(): string { return "=== Report ==="; }
    abstract protected function body(): string;
}
class SalesReport extends Report {
    protected function body(): string { return "savdo: 100"; }
}
```
**Python**
```python
from abc import ABC, abstractmethod

class Report(ABC):
    def generate(self):
        return "\n".join([self.header(), self.body(), "--end--"])

    def header(self):
        return "=== Report ==="

    @abstractmethod
    def body(self): ...

class SalesReport(Report):
    def body(self):
        return "savdo: 100"
# "savdo: 100" in SalesReport().generate()  # True
```

<a id="m608"></a>
### 608. Visitor
Obyektlar strukturasini o'zgartirmasdan, ularga yangi operatsiyalar qo'shadi.

**JS**
```js
class Circle { constructor(r) { this.r = r; } accept(v) { return v.visitCircle(this); } }
class Square { constructor(s) { this.s = s; } accept(v) { return v.visitSquare(this); } }
class AreaVisitor {
  visitCircle(c) { return Math.PI * c.r * c.r; }
  visitSquare(s) { return s.s * s.s; }
}
// new Square(3).accept(new AreaVisitor()) // 9
```
**PHP**
```php
interface Shape { public function accept(Visitor $v): float; }
class Circle implements Shape {
    public function __construct(public float $r) {}
    public function accept(Visitor $v): float { return $v->visitCircle($this); }
}
class Square implements Shape {
    public function __construct(public float $s) {}
    public function accept(Visitor $v): float { return $v->visitSquare($this); }
}
interface Visitor { public function visitCircle(Circle $c): float; public function visitSquare(Square $s): float; }
class AreaVisitor implements Visitor {
    public function visitCircle(Circle $c): float { return M_PI * $c->r ** 2; }
    public function visitSquare(Square $s): float { return $s->s ** 2; }
}
```
**Python**
```python
import math

class Circle:
    def __init__(self, r):
        self.r = r

    def accept(self, v):
        return v.visit_circle(self)

class Square:
    def __init__(self, s):
        self.s = s

    def accept(self, v):
        return v.visit_square(self)

class AreaVisitor:
    def visit_circle(self, c):
        return math.pi * c.r ** 2

    def visit_square(self, s):
        return s.s ** 2
# Square(3).accept(AreaVisitor())  # 9
```

<a id="m609"></a>
### 609. Null Object
`null` o'rniga "hech narsa qilmaydigan" obyekt qaytarib, doimiy `null` tekshiruvlardan qutqaradi.

**JS**
```js
class RealLogger { log(msg) { return `LOG: ${msg}`; } }
class NullLogger { log() { return ""; } }   // hech narsa qilmaydi
function getLogger(enabled) { return enabled ? new RealLogger() : new NullLogger(); }
// getLogger(false).log("x") // "" — null tekshiruvi shart emas
```
**PHP**
```php
interface Logger { public function log(string $msg): string; }
class RealLogger implements Logger { public function log(string $msg): string { return "LOG: $msg"; } }
class NullLogger implements Logger { public function log(string $msg): string { return ""; } }
function getLogger(bool $enabled): Logger { return $enabled ? new RealLogger() : new NullLogger(); }
```
**Python**
```python
class RealLogger:
    def log(self, msg): return f"LOG: {msg}"

class NullLogger:
    def log(self, msg): return ""  # hech narsa qilmaydi

def get_logger(enabled):
    return RealLogger() if enabled else NullLogger()
# get_logger(False).log("x")  # "" — None tekshiruvi shart emas
```

<a id="m610"></a>
### 610. Object Pool
Qimmat yaratiladigan obyektlarni qayta ishlatish uchun zaxirada saqlaydi.

**JS**
```js
class ConnectionPool {
  constructor() { this.free = []; this.used = 0; }
  acquire() { this.used++; return this.free.pop() ?? { id: this.used }; }
  release(conn) { this.free.push(conn); }
}
// const p = new ConnectionPool(); const c = p.acquire();
// p.release(c); p.acquire() === c // true
```
**PHP**
```php
class ConnectionPool {
    private array $free = [];
    private int $used = 0;
    public function acquire(): object { $this->used++; return array_pop($this->free) ?? (object)["id" => $this->used]; }
    public function release(object $conn): void { $this->free[] = $conn; }
}
```
**Python**
```python
class ConnectionPool:
    def __init__(self):
        self.free = []
        self.used = 0

    def acquire(self):
        if self.free:
            return self.free.pop()
        self.used += 1
        return {"id": self.used}

    def release(self, conn):
        self.free.append(conn)
# p = ConnectionPool(); c = p.acquire(); p.release(c); p.acquire() is c  # True
```

<a id="m611"></a>
### 611. Dependency Injection
Obyekt o'z bog'liqliklarini ichida yaratmasdan, tashqaridan (konstruktor orqali) oladi.

**JS**
```js
class ConsoleMailer { send(to) { return `mail->${to}`; } }
class UserService {
  constructor(mailer) { this.mailer = mailer; }   // tashqaridan beriladi
  register(name) { return this.mailer.send(name); }
}
// new UserService(new ConsoleMailer()).register("Ali") // "mail->Ali"
```
**PHP**
```php
interface Mailer { public function send(string $to): string; }
class ConsoleMailer implements Mailer { public function send(string $to): string { return "mail->$to"; } }
class UserService {
    public function __construct(private Mailer $mailer) {}
    public function register(string $name): string { return $this->mailer->send($name); }
}
```
**Python**
```python
class ConsoleMailer:
    def send(self, to): return f"mail->{to}"

class UserService:
    def __init__(self, mailer):  # tashqaridan beriladi
        self.mailer = mailer

    def register(self, name):
        return self.mailer.send(name)
# UserService(ConsoleMailer()).register("Ali")  # "mail->Ali"
```

<a id="m612"></a>
### 612. Repository pattern
Ma'lumotlarga kirish mantig'ini biznes mantig'idan ajratuvchi kolleksiyaga o'xshash abstraksiya.

**JS**
```js
class UserRepository {
  constructor() { this.store = new Map(); }
  add(user) { this.store.set(user.id, user); }
  findById(id) { return this.store.get(id) ?? null; }
  all() { return [...this.store.values()]; }
}
// const r = new UserRepository(); r.add({ id: 1, name: "Ali" });
// r.findById(1).name // "Ali"
```
**PHP**
```php
class UserRepository {
    private array $store = [];
    public function add(array $user): void { $this->store[$user["id"]] = $user; }
    public function findById(int $id): ?array { return $this->store[$id] ?? null; }
    public function all(): array { return array_values($this->store); }
}
```
**Python**
```python
class UserRepository:
    def __init__(self):
        self._store = {}

    def add(self, user):
        self._store[user["id"]] = user

    def find_by_id(self, id):
        return self._store.get(id)

    def all(self):
        return list(self._store.values())
# r = UserRepository(); r.add({"id": 1, "name": "Ali"}); r.find_by_id(1)["name"]
```

<a id="m613"></a>
### 613. Event Emitter (Pub/Sub)
Nomli hodisalarga obuna bo'lish va ularni chiqarish (emit) orqali bo'shashtirilgan aloqani ta'minlaydi.

**JS**
```js
class EventEmitter {
  constructor() { this.handlers = {}; }
  on(event, fn) { (this.handlers[event] ??= []).push(fn); }
  emit(event, data) { (this.handlers[event] ?? []).forEach(fn => fn(data)); }
}
// const e = new EventEmitter(); const got = [];
// e.on("hi", x => got.push(x)); e.emit("hi", 5); got // [5]
```
**PHP**
```php
class EventEmitter {
    private array $handlers = [];
    public function on(string $event, callable $fn): void { $this->handlers[$event][] = $fn; }
    public function emit(string $event, $data): void {
        foreach ($this->handlers[$event] ?? [] as $fn) $fn($data);
    }
}
```
**Python**
```python
from collections import defaultdict

class EventEmitter:
    def __init__(self):
        self.handlers = defaultdict(list)

    def on(self, event, fn):
        self.handlers[event].append(fn)

    def emit(self, event, data):
        for fn in self.handlers[event]:
            fn(data)
# e = EventEmitter(); got = []; e.on("hi", got.append); e.emit("hi", 5); got  # [5]
```

<a id="m614"></a>
### 614. Lazy initialization
Qimmat resursni faqat birinchi marta so'ralganda yaratadi va keyin keshlaydi.

**JS**
```js
class Config {
  get settings() {                 // birinchi murojaatda hisoblanadi
    if (!this._settings) this._settings = { loaded: true, ts: Date.now() };
    return this._settings;
  }
}
// const c = new Config(); c.settings === c.settings // true (bir xil obyekt)
```
**PHP**
```php
class Config {
    private ?array $settings = null;
    public function getSettings(): array {
        return $this->settings ??= ["loaded" => true];
    }
}
// $c = new Config(); $c->getSettings() === $c->getSettings() // true
```
**Python**
```python
from functools import cached_property

class Config:
    @cached_property
    def settings(self):  # birinchi murojaatda hisoblanadi
        return {"loaded": True}
# c = Config(); c.settings is c.settings  # True (bir xil obyekt)
```

<a id="m615"></a>
### 615. Multiton
Singleton'ning kalit bo'yicha varianti: har bir kalit uchun aniq bitta nusxa.

**JS**
```js
class Logger {
  static #instances = new Map();
  constructor(name) { this.name = name; }
  static get(name) {
    if (!Logger.#instances.has(name)) Logger.#instances.set(name, new Logger(name));
    return Logger.#instances.get(name);
  }
}
// Logger.get("db") === Logger.get("db") // true
// Logger.get("db") === Logger.get("api") // false
```
**PHP**
```php
class Logger {
    private static array $instances = [];
    private function __construct(public string $name) {}
    public static function get(string $name): Logger {
        return self::$instances[$name] ??= new Logger($name);
    }
}
```
**Python**
```python
class Logger:
    _instances = {}

    def __init__(self, name):
        self.name = name

    @classmethod
    def get(cls, name):
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]
# Logger.get("db") is Logger.get("db")  # True
```

<a id="m616"></a>
### 616. Registry
Obyektlarni nom bo'yicha ro'yxatga olib, global tarzda topib beruvchi markaziy reestr.

**JS**
```js
class Registry {
  static #items = new Map();
  static set(key, value) { Registry.#items.set(key, value); }
  static get(key) { return Registry.#items.get(key); }
}
// Registry.set("pi", 3.14); Registry.get("pi") // 3.14
```
**PHP**
```php
class Registry {
    private static array $items = [];
    public static function set(string $key, $value): void { self::$items[$key] = $value; }
    public static function get(string $key) { return self::$items[$key] ?? null; }
}
// Registry::set("pi", 3.14); Registry::get("pi") // 3.14
```
**Python**
```python
class Registry:
    _items = {}

    @classmethod
    def set(cls, key, value):
        cls._items[key] = value

    @classmethod
    def get(cls, key):
        return cls._items.get(key)
# Registry.set("pi", 3.14); Registry.get("pi")  # 3.14
```

<a id="m617"></a>
### 617. Fluent interface (method chaining)
Har bir metod `this`/`self` ni qaytaradi, shu sababli chaqiruvlarni zanjir qilib yozish mumkin.

**JS**
```js
class Query {
  constructor() { this.parts = []; }
  select(c) { this.parts.push(`SELECT ${c}`); return this; }
  from(t) { this.parts.push(`FROM ${t}`); return this; }
  where(w) { this.parts.push(`WHERE ${w}`); return this; }
  build() { return this.parts.join(" "); }
}
// new Query().select("*").from("users").where("id=1").build()
// "SELECT * FROM users WHERE id=1"
```
**PHP**
```php
class Query {
    private array $parts = [];
    public function select(string $c): static { $this->parts[] = "SELECT $c"; return $this; }
    public function from(string $t): static { $this->parts[] = "FROM $t"; return $this; }
    public function where(string $w): static { $this->parts[] = "WHERE $w"; return $this; }
    public function build(): string { return implode(" ", $this->parts); }
}
```
**Python**
```python
class Query:
    def __init__(self):
        self.parts = []

    def select(self, c):
        self.parts.append(f"SELECT {c}")
        return self

    def from_(self, t):
        self.parts.append(f"FROM {t}")
        return self

    def where(self, w):
        self.parts.append(f"WHERE {w}")
        return self

    def build(self):
        return " ".join(self.parts)
# Query().select("*").from_("users").where("id=1").build()
```

<a id="m618"></a>
### 618. Specification pattern
Biznes qoidalarni qayta ishlatiladigan, birlashtiriladigan (and/or) shartlar sifatida ifodalaydi.

**JS**
```js
class Spec {
  constructor(test) { this.test = test; }
  and(other) { return new Spec(x => this.test(x) && other.test(x)); }
  or(other) { return new Spec(x => this.test(x) || other.test(x)); }
  isSatisfiedBy(x) { return this.test(x); }
}
// const adult = new Spec(u => u.age >= 18);
// const active = new Spec(u => u.active);
// adult.and(active).isSatisfiedBy({ age: 20, active: true }) // true
```
**PHP**
```php
class Spec {
    public function __construct(public $test) {}
    public function and(Spec $o): Spec { return new Spec(fn($x) => ($this->test)($x) && ($o->test)($x)); }
    public function or(Spec $o): Spec { return new Spec(fn($x) => ($this->test)($x) || ($o->test)($x)); }
    public function isSatisfiedBy($x): bool { return ($this->test)($x); }
}
```
**Python**
```python
class Spec:
    def __init__(self, test):
        self.test = test

    def and_(self, other):
        return Spec(lambda x: self.test(x) and other.test(x))

    def or_(self, other):
        return Spec(lambda x: self.test(x) or other.test(x))

    def is_satisfied_by(self, x):
        return self.test(x)
# adult = Spec(lambda u: u["age"] >= 18)
# active = Spec(lambda u: u["active"])
# adult.and_(active).is_satisfied_by({"age": 20, "active": True})  # True
```

<a id="m619"></a>
### 619. Service Locator
Servislarni markaziy registratordan nom bo'yicha topib beradi (DI ning muqobili).

**JS**
```js
class ServiceLocator {
  constructor() { this.services = new Map(); }
  register(name, service) { this.services.set(name, service); }
  resolve(name) {
    if (!this.services.has(name)) throw new Error(`topilmadi: ${name}`);
    return this.services.get(name);
  }
}
// const sl = new ServiceLocator(); sl.register("db", { ok: true });
// sl.resolve("db").ok // true
```
**PHP**
```php
class ServiceLocator {
    private array $services = [];
    public function register(string $name, $service): void { $this->services[$name] = $service; }
    public function resolve(string $name) {
        if (!isset($this->services[$name])) throw new RuntimeException("topilmadi: $name");
        return $this->services[$name];
    }
}
```
**Python**
```python
class ServiceLocator:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def resolve(self, name):
        if name not in self._services:
            raise KeyError(f"topilmadi: {name}")
        return self._services[name]
# sl = ServiceLocator(); sl.register("db", {"ok": True}); sl.resolve("db")["ok"]
```

<a id="m620"></a>
### 620. Data Mapper
Domen obyektlari bilan ma'lumotlar bazasi qatorlari o'rtasida ikki tomonlama o'tkazma qiladi.

**JS**
```js
class User {
  constructor(id, name) { this.id = id; this.name = name; }
}
class UserMapper {
  toDomain(row) { return new User(row.user_id, row.full_name); }
  toRow(user) { return { user_id: user.id, full_name: user.name }; }
}
// const m = new UserMapper();
// m.toDomain({ user_id: 1, full_name: "Ali" }).name // "Ali"
```
**PHP**
```php
class User {
    public function __construct(public int $id, public string $name) {}
}
class UserMapper {
    public function toDomain(array $row): User { return new User($row["user_id"], $row["full_name"]); }
    public function toRow(User $u): array { return ["user_id" => $u->id, "full_name" => $u->name]; }
}
```
**Python**
```python
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class UserMapper:
    def to_domain(self, row):
        return User(row["user_id"], row["full_name"])

    def to_row(self, user):
        return {"user_id": user.id, "full_name": user.name}
# UserMapper().to_domain({"user_id": 1, "full_name": "Ali"}).name  # "Ali"
```

<a id="m621"></a>
### 621. Value Object
O'zgarmas (immutable) va faqat qiymati bilan tenglashtiriladigan kichik obyekt (masalan, pul).

**JS**
```js
class Money {
  constructor(amount, currency) {
    this.amount = amount; this.currency = currency;
    Object.freeze(this);                 // o'zgarmas
  }
  equals(o) { return this.amount === o.amount && this.currency === o.currency; }
}
// new Money(5, "USD").equals(new Money(5, "USD")) // true
```
**PHP**
```php
final class Money {
    public function __construct(public readonly int $amount, public readonly string $currency) {}
    public function equals(Money $o): bool {
        return $this->amount === $o->amount && $this->currency === $o->currency;
    }
}
// (new Money(5, "USD"))->equals(new Money(5, "USD")) // true
```
**Python**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: int
    currency: str
# Money(5, "USD") == Money(5, "USD")  # True — qiymat bo'yicha tenglik
```
