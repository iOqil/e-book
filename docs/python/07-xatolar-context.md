# 07 — Xatolarni boshqarish (`try` / `except`)

Dasturlarda xatolar muqarrar: foydalanuvchi raqam o'rniga matn kiritadi, fayl topilmaydi, nolga bo'lish sodir bo'ladi. Agar xatoni boshqarmasang, dastur **to'satdan to'xtaydi** (qulaydi). Bu modulda xatolarni ushlab, dasturni nazoratda saqlashni o'rganasan.

> **Bu modulda:** xato (exception) nima, `try`/`except`, aniq xato turlarini ushlash, `else`/`finally`, va o'zing xato chaqirish (`raise`).

---

## 7.1 Xato nima? Nega dastur "qulaydi"?

Xato yuz berganda, agar uni ushlamasang, dastur shu yerda to'xtaydi:

```python
yosh = int(input("Yoshing: "))     # foydalanuvchi "salom" yozsa...
print(yosh)
# ValueError: invalid literal for int() ... — dastur QULADI, keyingi kod ishlamaydi
```

Tez-tez uchraydigan xato turlari:

| Xato | Qachon | Misol |
|------|--------|-------|
| `ValueError` | qiymat noto'g'ri | `int("salom")` |
| `ZeroDivisionError` | nolga bo'lish | `10 / 0` |
| `TypeError` | tip mos kelmaydi | `"matn" + 5` |
| `KeyError` | lug'atda kalit yo'q | `lugat["yo'q"]` |
| `IndexError` | ro'yxatda indeks yo'q | `royxat[100]` |
| `FileNotFoundError` | fayl topilmadi | mavjud bo'lmagan faylni ochish |

---

## 7.2 `try` / `except` — xatoni ushlash

`try` blokiga "xato bo'lishi mumkin" kodni yozasan, `except` ga xato yuz berganda nima qilishni:

```python
try:
    yosh = int(input("Yoshing: "))
    print(f"Siz {yosh} yoshdasiz")
except:
    print("Iltimos, to'g'ri raqam kiriting")
```

Endi foydalanuvchi "salom" yozsa, dastur qulamaydi — `except` bloki ishlaydi va dastur davom etadi.

```python
try:
    natija = 10 / 0
except:
    print("Nolga bo'lib bo'lmaydi!")    # shu chiqadi, dastur tirik qoladi
```

---

## 7.3 Aniq xato turini ushlash

Har qanday xatoni emas, **aniq turini** ushlash yaxshiroq — shunda har xil xatoga har xil javob berasan:

```python
try:
    son = int(input("Son: "))
    natija = 100 / son
    print(natija)
except ValueError:
    print("Bu raqam emas!")
except ZeroDivisionError:
    print("Nolga bo'lib bo'lmaydi!")
```

> **Nega aniq tur?** "Hamma xatoni ushla" (`except:`) ba'zan haqiqiy muammoni yashiradi — masalan kodingdagi xatoni ham "yutib" yuboradi. Aniq turni ushlasang, faqat kutgan xatoga javob berasan, kutilmagani esa ko'rinadi (va sen tuzatasan).

Bir nechta turni birga ushlash:

```python
try:
    ...
except (ValueError, TypeError):
    print("Qiymat yoki tip xatosi")
```

Xato haqida ma'lumot olish (`as`):

```python
try:
    int("salom")
except ValueError as e:
    print(f"Xato yuz berdi: {e}")    # Xato yuz berdi: invalid literal for int()...
```

Xato turlari tasodifiy emas — ular vorislik daraxti (ierarxiya) bo'yicha tartibga solingan, va yuqori turni ushlasang uning ostidagi barcha turlar ham ushlanadi:

![Python exception ierarxiyasi: BaseException -> Exception -> ValueError, TypeError, ZeroDivisionError, KeyError, IndexError](rasmlar/py07-exception-ierarxiyasi.svg)

---

## 7.4 `else` va `finally`

**`else`** — xato **bo'lmaganda** ishlaydi:

```python
try:
    son = int(input("Son: "))
except ValueError:
    print("Noto'g'ri kiritish")
else:
    print(f"Rahmat! Siz {son} kiritdingiz")    # faqat xato bo'lmasa
```

**`finally`** — xato bo'ladimi-yo'qmi, **doim** ishlaydi (odatda tozalash uchun — faylni yopish va h.k.):

```python
try:
    fayl_ochish()
except FileNotFoundError:
    print("Fayl topilmadi")
finally:
    print("Bu har doim bajariladi")    # tozalash kodi shu yerga
```

Quyidagi diagramma to'rt blokning oqimini ko'rsatadi — xato bo'lganda va bo'lmaganda qaysi blok ishlashini:

![try/except/else/finally oqimi: xato bo'lganda except, bo'lmaganda else, finally esa har doim](rasmlar/py07-try-except-else-finally.svg)

---

## 7.5 `raise` — o'zing xato chaqirish

Ba'zan o'zing xato "chaqirishing" kerak — masalan, noto'g'ri qiymat berilganda dasturni to'xtatish uchun:

```python
def yosh_tekshir(yosh):
    if yosh < 0:
        raise ValueError("Yosh manfiy bo'lishi mumkin emas")
    return yosh

try:
    yosh_tekshir(-5)
except ValueError as e:
    print(e)        # Yosh manfiy bo'lishi mumkin emas
```

> **Qachon `raise`?** Funksiyangga noto'g'ri ma'lumot kelganda, uni jimgina qabul qilish o'rniga xato chaqir. Shunda muammo erta ko'rinadi va chaqiruvchi kod uni ushlab, to'g'ri javob beradi.

Quyidagi diagramma `raise` qilingan xato funksiyadan chaqiruvchi tomonga qanday uzatilishini va u yerda `except` bilan ushlanishini ko'rsatadi:

![raise bilan xato ko'tarish: funksiya xatoni ko'taradi, chaqiruvchi uni except bilan ushlaydi](rasmlar/py07-raise-oqimi.svg)

---

## 7.6 Amaliy namuna: ishonchli kiritish

Xato boshqarishning eng keng tarqalgan ishlatilishi — foydalanuvchi to'g'ri ma'lumot kiritguncha qayta-qayta so'rash:

```python
while True:
    try:
        yosh = int(input("Yoshingiz: "))
        break                          # to'g'ri raqam — sikldan chiqamiz
    except ValueError:
        print("Iltimos, butun son kiriting")

print(f"Yoshingiz: {yosh}")
```

> Bu naqsh (`while True` + `try/except` + `break`) juda foydali — foydalanuvchi xato qilsa, dastur qulamaydi, balki muloyim qayta so'raydi.

---

## ✍️ Masalalar (20 ta)

> Bu masalalar 1–7 modullar mavzulariga asoslangan.

**Oson (1–7):**

1. Foydalanuvchidan son so'ra. `try/except` bilan: raqam bo'lmasa "Bu raqam emas" deb chiqar.
2. `10 / 0` ni `try/except` ichida yozib, `ZeroDivisionError` ni ushla.
3. Foydalanuvchidan ikki son so'rab, birinchisini ikkinchisiga bo'l. Nolga bo'lishni ushlab, xabar chiqar.
4. Ro'yxat `[1,2,3]` ning 10-indeksiga murojaat qilib, `IndexError` ni ushla.
5. Lug'atdan mavjud bo'lmagan kalitni so'rab, `KeyError` ni ushla.
6. `int("salom")` ni `try/except ValueError` bilan ushlab, xato xabarini (`as e`) chiqar.
7. `try/except/else` ishlat: son to'g'ri kiritilsa `else` da "rahmat" deb yoz.

**O'rta (8–14):**

8. `while True` + `try/except` bilan: foydalanuvchi to'g'ri butun son kiritguncha qayta so'ra.
9. Bir funksiya yoz: ikki sonni bo'lsin, lekin nolga bo'lishni `try/except` bilan ushlab, `None` qaytarsin.
10. Ikki xil xatoni alohida ushla (`ValueError` va `ZeroDivisionError`), har biriga boshqa xabar ber.
11. `finally` ishlat: xato bo'ladimi-yo'qmi, oxirida "Tugadi" deb chiqaruvchi kod yoz.
12. `raise` ishlat: `yosh < 0` bo'lsa `ValueError` chaqiradigan funksiya yoz.
13. Foydalanuvchidan ro'yxat indeksini so'rab, shu indeksdagi elementni chiqar. Noto'g'ri indeks bo'lsa "Bunday element yo'q" deb yoz.
14. Bir funksiya yoz: matnni songa aylantirsin, agar aylantirib bo'lmasa 0 qaytarsin (xatoni ushlab).

**Murakkab (15–20):**

15. Oddiy kalkulyator: ikki son va amal so'ra. Noto'g'ri son yoki nolga bo'lishni `try/except` bilan boshqarib, foydalanuvchini qulatmagin.
16. `raise` ishlat: bank hisobidan balansdan ko'p yechishga urinilsa `ValueError("mablag' yetarli emas")` chaqiruvchi funksiya yoz, uni `try/except` bilan sina.
17. Foydalanuvchidan bir nechta son so'rab (sikl bilan), faqat to'g'ri kiritilganlarini ro'yxatga qo'sh, xato kiritilganlarni o'tkazib yubor.
18. Lug'atdan xavfsiz qiymat oluvchi funksiya yoz: kalit bo'lsa qiymatni, bo'lmasa "topilmadi" qaytarsin (`try/except KeyError` bilan, keyin `get` bilan ham qilib taqqosla).
19. O'z funksiyangda kirish tekshiruvi: `bolish(a, b)` funksiyasi `b == 0` bo'lsa o'zi xato chaqirsin (`raise`), chaqiruvchi tomon esa ushlasin.
20. "Ishonchli son kiritish" funksiyasini yoz: parametr sifatida savol matnini olsin, foydalanuvchi to'g'ri butun son kiritguncha so'rasin, va sonni qaytarsin. Bir nechta joyda qayta ishlatib ko'r.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
try:
    son = int(input("Son: "))
    print(son)
except ValueError:
    print("Bu raqam emas")

# 2
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Nolga bo'lib bo'lmaydi")

# 3
try:
    a = int(input("a: "))
    b = int(input("b: "))
    print(a / b)
except ZeroDivisionError:
    print("Nolga bo'lib bo'lmaydi")

# 4
try:
    print([1, 2, 3][10])
except IndexError:
    print("Bunday indeks yo'q")

# 5
lugat = {"ism": "Aziz"}
try:
    print(lugat["yosh"])
except KeyError:
    print("Bunday kalit yo'q")

# 6
try:
    int("salom")
except ValueError as e:
    print(f"Xato: {e}")

# 7
try:
    son = int(input("Son: "))
except ValueError:
    print("Noto'g'ri")
else:
    print("rahmat")

# 8
while True:
    try:
        son = int(input("Butun son: "))
        break
    except ValueError:
        print("Iltimos, butun son kiriting")
print("Kiritildi:", son)

# 9
def bol(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
print(bol(10, 2), bol(10, 0))    # 5.0 None

# 10
try:
    son = int(input("Son: "))
    print(100 / son)
except ValueError:
    print("Raqam emas")
except ZeroDivisionError:
    print("Nolga bo'lib bo'lmaydi")

# 11
try:
    print("ishlayapti")
except Exception:
    print("xato")
finally:
    print("Tugadi")

# 12
def yosh_tekshir(yosh):
    if yosh < 0:
        raise ValueError("Yosh manfiy bo'lmaydi")
    return yosh
try:
    yosh_tekshir(-3)
except ValueError as e:
    print(e)

# 13
royxat = [10, 20, 30]
try:
    i = int(input("Indeks: "))
    print(royxat[i])
except (IndexError, ValueError):
    print("Bunday element yo'q")

# 14
def songa(matn):
    try:
        return int(matn)
    except ValueError:
        return 0
print(songa("42"), songa("salom"))   # 42 0

# 15
try:
    a = float(input("1-son: "))
    b = float(input("2-son: "))
    amal = input("Amal (+ - * /): ")
    if amal == "+":
        print(a + b)
    elif amal == "-":
        print(a - b)
    elif amal == "*":
        print(a * b)
    elif amal == "/":
        print(a / b)
except ValueError:
    print("Noto'g'ri son")
except ZeroDivisionError:
    print("Nolga bo'lib bo'lmaydi")

# 16
def yech(balans, summa):
    if summa > balans:
        raise ValueError("mablag' yetarli emas")
    return balans - summa
try:
    print(yech(500, 1000))
except ValueError as e:
    print(e)

# 17
sonlar = []
for _ in range(5):
    qiymat = input("Son: ")
    try:
        sonlar.append(int(qiymat))
    except ValueError:
        print(f"'{qiymat}' o'tkazib yuborildi")
print(sonlar)

# 18
lugat = {"ism": "Aziz", "yosh": 20}
def olish(kalit):
    try:
        return lugat[kalit]
    except KeyError:
        return "topilmadi"
print(olish("ism"), olish("email"))    # Aziz topilmadi
# get bilan ham:
print(lugat.get("email", "topilmadi"))  # topilmadi

# 19
def bolish(a, b):
    if b == 0:
        raise ValueError("nolga bo'lish mumkin emas")
    return a / b
try:
    print(bolish(10, 0))
except ValueError as e:
    print(e)

# 20
def son_sora(savol):
    while True:
        try:
            return int(input(savol))
        except ValueError:
            print("Iltimos, butun son kiriting")
yosh = son_sora("Yoshingiz: ")
miqdor = son_sora("Miqdor: ")
print(yosh, miqdor)
```

</details>

---

[← Modullar va muhit](./06-modullar-muhit.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: Fayllar, JSON, CSV →](./08-fayl-malumot.md)
