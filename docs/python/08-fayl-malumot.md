# 08 — Fayllar, JSON va CSV

Hozirgacha ma'lumot faqat dastur ishlab turganda xotirada saqlangan — dastur tugagach yo'qolgan. **Fayllar** ma'lumotni doimiy saqlash imkonini beradi: matn yozish, o'qish, sozlamalarni saqlash. Bu modulda fayllar bilan ishlash, hamda ma'lumotni JSON va CSV formatlarida saqlashni o'rganasan.

> **Bu modulda:** fayl o'qish va yozish (`open`, `with`), `utf-8` kodlash, `pathlib`, JSON bilan ma'lumot saqlash/yuklash, va CSV jadvallar.

---

## 8.1 Faylga yozish

Faylni `open()` bilan ochasan. Eng to'g'ri usul — `with` bilan (u faylni avtomatik yopadi):

```python
with open("salom.txt", "w", encoding="utf-8") as f:
    f.write("Salom, dunyo!\n")
    f.write("Ikkinchi qator\n")
# blok tugaganda fayl avtomatik yopiladi
```

`open()` ning ikkinchi parametri — **rejim**:

| Rejim | Ma'nosi |
|-------|---------|
| `"w"` | yozish (mavjud faylni **o'chirib** qaytadan yozadi) |
| `"a"` | qo'shish (mavjud faylning **oxiriga** qo'shadi) |
| `"r"` | o'qish (standart) |

> **`encoding="utf-8"` — juda muhim!** O'zbekcha (yoki har qanday o'zbek kirill/lotin) matn bilan ishlaganda doim `encoding="utf-8"` yoz. Aks holda ba'zi tizimlarda harflar buzilib chiqishi mumkin. Buni odat qil.

---

## 8.2 Fayldan o'qish

```python
# Butun faylni bir matn sifatida o'qish:
with open("salom.txt", "r", encoding="utf-8") as f:
    matn = f.read()
print(matn)

# Qator-qator o'qish (katta fayllar uchun eng yaxshi yo'l):
with open("salom.txt", "r", encoding="utf-8") as f:
    for qator in f:
        print(qator.strip())     # strip() — qator oxiridagi \n ni olib tashlaydi

# Barcha qatorlarni ro'yxatga olish:
with open("salom.txt", "r", encoding="utf-8") as f:
    qatorlar = f.readlines()     # ['Salom...\n', 'Ikkinchi...\n']
```

> **Nega `with`?** `with` bloki tugaganda fayl avtomatik va ishonchli yopiladi — xato bo'lsa ham. `with`siz `f.close()` ni o'zing yozishing kerak bo'lardi va unutish oson. Doim `with` ishlat.

Quyidagi diagramma `with` blokining ichki mexanizmini ko'rsatadi: blokka kirganda fayl ochiladi, chiqqanda esa (xato bo'lsa ham) avtomatik yopiladi.

![with bloki faylni ochib avtomatik yopishi](rasmlar/py08-with-context-manager.svg)

---

## 8.3 `pathlib` — fayl yo'llari bilan ishlash

`pathlib` — fayl va papka yo'llari bilan ishlashning zamonaviy usuli:

```python
from pathlib import Path

yol = Path("hujjatlar/salom.txt")

print(yol.name)        # salom.txt    — fayl nomi
print(yol.stem)        # salom        — kengaytmasiz nom
print(yol.suffix)      # .txt         — kengaytma
print(yol.exists())    # True/False   — fayl mavjudmi?

# Yo'llarni / bilan birlashtirish (qulay!):
papka = Path("hujjatlar")
fayl = papka / "yangi.txt"     # hujjatlar/yangi.txt

# pathlib bilan o'qish/yozish — qisqaroq:
Path("salom.txt").write_text("Salom!", encoding="utf-8")
matn = Path("salom.txt").read_text(encoding="utf-8")
```

---

## 8.4 JSON — ma'lumotni saqlash va yuklash

JSON — ma'lumotni matn ko'rinishida saqlash formati. Python lug'at/ro'yxatlarini faylga saqlab, keyin qayta yuklash uchun ideal (masalan, dastur sozlamalari yoki foydalanuvchi ma'lumotlari).

```python
import json

malumot = {
    "ism": "Aziz",
    "yosh": 20,
    "tillar": ["o'zbek", "ingliz"],
}

# Faylga saqlash:
with open("malumot.json", "w", encoding="utf-8") as f:
    json.dump(malumot, f, ensure_ascii=False, indent=2)

# Fayldan yuklash:
with open("malumot.json", "r", encoding="utf-8") as f:
    yuklangan = json.load(f)

print(yuklangan["ism"])    # Aziz
```

> **`ensure_ascii=False`** — o'zbekcha harflar to'g'ri (o'qiladigan) ko'rinishda saqlanishi uchun. Busiz harflar `\u...` kodlariga aylanib ketadi. **`indent=2`** — faylni chiroyli, o'qish oson qilib formatlaydi.

Matn va Python obyekti orasida aylantirish (faylsiz):

```python
import json
matn = json.dumps({"a": 1})    # obyekt → JSON matn:  '{"a": 1}'
obyekt = json.loads('{"a": 1}')  # JSON matn → obyekt: {'a': 1}
```

Quyidagi diagramma JSON matn va Python obyekti orasidagi ikki tomonlama moslikni ko'rsatadi.

![JSON matn va Python dict orasidagi moslik](rasmlar/py08-json-dict.svg)

---

## 8.5 CSV — jadval ma'lumotlari

CSV — jadval ko'rinishidagi ma'lumot (Excel kabi: qatorlar va ustunlar). Har qator vergul bilan ajratilgan qiymatlar:

```python
import csv

# Yozish:
with open("talabalar.csv", "w", newline="", encoding="utf-8") as f:
    yozuvchi = csv.writer(f)
    yozuvchi.writerow(["ism", "yosh", "ball"])     # sarlavha qatori
    yozuvchi.writerow(["Aziz", 20, 85])
    yozuvchi.writerow(["Malika", 22, 90])

# O'qish:
with open("talabalar.csv", "r", encoding="utf-8") as f:
    oquvchi = csv.reader(f)
    for qator in oquvchi:
        print(qator)        # ['ism', 'yosh', 'ball'], keyin ['Aziz', '20', '85'], ...
```

Kalit bilan o'qish (`DictReader`) — har qatorni lug'at sifatida:

```python
import csv
with open("talabalar.csv", "r", encoding="utf-8") as f:
    oquvchi = csv.DictReader(f)
    for qator in oquvchi:
        print(qator["ism"], qator["ball"])    # Aziz 85, Malika 90
```

> **`newline=""`** — CSV yozishda bu parametrni qo'sh (ba'zi tizimlarda qo'shimcha bo'sh qatorlar paydo bo'lmasligi uchun). CSV'dan o'qilgan sonlar **matn** ko'rinishida keladi (`"20"`), kerak bo'lsa `int()` bilan aylantir.

Quyidagi diagramma CSV jadval va Python qatorlari orasidagi moslikni ko'rsatadi (`DictReader` har qatorni lug'atga aylantirishi bilan).

![CSV jadval va Python qatorlari orasidagi moslik](rasmlar/py08-csv-qatorlar.svg)

---

## ✍️ Masalalar (20 ta)

> Bu masalalar fayllar bilan ishlaydi — har birini ishga tushirib, yaratilgan fayllarni tekshir.

**Oson (1–7):**

1. `salom.txt` fayliga "Salom, dunyo!" deb yoz (`with open`, `"w"`, `utf-8`).
2. Shu faylni o'qib, mazmunini ekranga chiqar.
3. Faylga uchta qator yoz (har biri yangi qatorda, `\n` bilan).
4. Faylni qator-qator o'qib, har qatorni `strip()` bilan chiqar.
5. `"a"` rejimida faylga yana bir qator **qo'sh** (eskisi o'chmasin).
6. `pathlib.Path` bilan `salom.txt` faylining nomini, kengaytmasini va mavjudligini chiqar.
7. `Path.write_text` bilan faylga matn yozib, `read_text` bilan qayta o'qi.

**O'rta (8–14):**

8. Bir lug'atni (`ism`, `yosh`) `json.dump` bilan faylga saqla (`ensure_ascii=False`, `indent=2`).
9. Shu JSON faylni `json.load` bilan o'qib, qiymatlarini chiqar.
10. Ro'yxatdagi sonlarni faylga yoz (har biri alohida qatorda), keyin o'qib yig'indisini hisobla.
11. Foydalanuvchidan bir nechta ism so'rab (sikl bilan), ularni faylga yoz.
12. CSV faylga 3 ta talaba (ism, yosh, ball) yoz (`csv.writer`).
13. Shu CSV faylni `csv.DictReader` bilan o'qib, har talabaning ism va ballini chiqar.
14. JSON faylga sonlar ro'yxatini saqla, keyin o'qib eng kattasini top.

**Murakkab (15–20):**

15. Oddiy "eslatmalar" dasturi: foydalanuvchi yozgan eslatmalarni faylga qo'shib boradi (`"a"` rejimi), har safar yangi qator.
16. Lug'atlar ro'yxatini (talabalar) JSON faylga saqla, qayta yuklab, ballari 80 dan yuqorilarni chiqar.
17. CSV faylni o'qib, barcha ballarning o'rtachasini hisobla (sonlarni `int` ga aylantirishni unutma).
18. Oddiy "telefon kitobchasi": ma'lumotni JSON faylda saqla. Dastur ishga tushganda yuklasin, yangi kontakt qo'shilganda saqlasin (qo'shish/ko'rish menyusi bilan).
19. Bir matn faylini o'qib, undagi qatorlar sonini, so'zlar sonini va belgilar sonini hisobla.
20. Ma'lumotni CSV'dan o'qib, JSON formatiga o'tkazib saqlovchi dastur yoz (har CSV qatori — JSON'da bitta lug'at bo'lsin).

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
with open("salom.txt", "w", encoding="utf-8") as f:
    f.write("Salom, dunyo!")

# 2
with open("salom.txt", "r", encoding="utf-8") as f:
    print(f.read())

# 3
with open("uch.txt", "w", encoding="utf-8") as f:
    f.write("Birinchi\n")
    f.write("Ikkinchi\n")
    f.write("Uchinchi\n")

# 4
with open("uch.txt", "r", encoding="utf-8") as f:
    for qator in f:
        print(qator.strip())

# 5
with open("uch.txt", "a", encoding="utf-8") as f:
    f.write("Qo'shilgan qator\n")

# 6
from pathlib import Path
yol = Path("salom.txt")
print(yol.name, yol.suffix, yol.exists())   # salom.txt .txt True

# 7
from pathlib import Path
Path("test.txt").write_text("Salom!", encoding="utf-8")
print(Path("test.txt").read_text(encoding="utf-8"))   # Salom!

# 8
import json
malumot = {"ism": "Aziz", "yosh": 20}
with open("m.json", "w", encoding="utf-8") as f:
    json.dump(malumot, f, ensure_ascii=False, indent=2)

# 9
import json
with open("m.json", "r", encoding="utf-8") as f:
    d = json.load(f)
print(d["ism"], d["yosh"])    # Aziz 20

# 10
sonlar = [10, 20, 30]
with open("sonlar.txt", "w", encoding="utf-8") as f:
    for s in sonlar:
        f.write(f"{s}\n")
with open("sonlar.txt", "r", encoding="utf-8") as f:
    jami = sum(int(q) for q in f)
print(jami)                   # 60

# 11
with open("ismlar.txt", "w", encoding="utf-8") as f:
    for _ in range(3):
        ism = input("Ism: ")
        f.write(ism + "\n")

# 12
import csv
with open("talabalar.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ism", "yosh", "ball"])
    w.writerow(["Aziz", 20, 85])
    w.writerow(["Malika", 22, 90])
    w.writerow(["Bobur", 21, 78])

# 13
import csv
with open("talabalar.csv", "r", encoding="utf-8") as f:
    for q in csv.DictReader(f):
        print(q["ism"], q["ball"])

# 14
import json
with open("nums.json", "w", encoding="utf-8") as f:
    json.dump([5, 12, 8, 20, 3], f)
with open("nums.json", "r", encoding="utf-8") as f:
    nums = json.load(f)
print(max(nums))              # 20

# 15
while True:
    eslatma = input("Eslatma ('stop' to'xtatadi): ")
    if eslatma == "stop":
        break
    with open("eslatmalar.txt", "a", encoding="utf-8") as f:
        f.write(eslatma + "\n")

# 16
import json
talabalar = [
    {"ism": "Aziz", "ball": 85},
    {"ism": "Malika", "ball": 92},
    {"ism": "Bobur", "ball": 70},
]
with open("t.json", "w", encoding="utf-8") as f:
    json.dump(talabalar, f, ensure_ascii=False, indent=2)
with open("t.json", "r", encoding="utf-8") as f:
    yuklangan = json.load(f)
for t in yuklangan:
    if t["ball"] > 80:
        print(t["ism"])       # Aziz, Malika

# 17
import csv
ballar = []
with open("talabalar.csv", "r", encoding="utf-8") as f:
    for q in csv.DictReader(f):
        ballar.append(int(q["ball"]))
print(sum(ballar) / len(ballar))

# 18
import json
from pathlib import Path
FAYL = "kontaktlar.json"
def yukla():
    if Path(FAYL).exists():
        return json.loads(Path(FAYL).read_text(encoding="utf-8"))
    return {}
def saqla(k):
    Path(FAYL).write_text(json.dumps(k, ensure_ascii=False, indent=2), encoding="utf-8")
kontaktlar = yukla()
while True:
    amal = input("qosh / korish / chiqish: ")
    if amal == "chiqish":
        break
    elif amal == "qosh":
        ism = input("Ism: ")
        kontaktlar[ism] = input("Raqam: ")
        saqla(kontaktlar)
    elif amal == "korish":
        print(kontaktlar)

# 19
with open("uch.txt", "r", encoding="utf-8") as f:
    matn = f.read()
print("Qatorlar:", len(matn.splitlines()))
print("So'zlar:", len(matn.split()))
print("Belgilar:", len(matn))

# 20
import csv, json
qatorlar = []
with open("talabalar.csv", "r", encoding="utf-8") as f:
    for q in csv.DictReader(f):
        qatorlar.append(q)
with open("talabalar.json", "w", encoding="utf-8") as f:
    json.dump(qatorlar, f, ensure_ascii=False, indent=2)
print("CSV → JSON tayyor")
```

</details>

---

[← Xatolarni boshqarish](./07-xatolar-context.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Generator va dekoratorlar →](./09-iterator-generator-decorator.md)
