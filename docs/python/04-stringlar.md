# 04 — Stringlar (matn bilan ishlash)

Matn (string) — dasturlashda eng ko'p ishlatiladigan ma'lumot turlaridan biri: ismlar, xabarlar, fayl matni, foydalanuvchi kiritgan ma'lumot. Bu modulda matnni qanday tahlil qilish, o'zgartirish va formatlashni o'rganasan.

> **Bu modulda:** matn metodlari (katta/kichik harf, bo'sh joy tozalash, almashtirish), matnni bo'laklarga ajratish va birlashtirish, slicing, va matn ichidan qidirish.

---

## 4.1 Matn asoslari

Matn qo'shtirnoq `" "` yoki bittirnoq `' '` ichida yoziladi (farqi yo'q, lekin bittasini tanlab izchil ishlat):

```python
ism = "Aziz"
jumla = 'Bugun havo issiq'
```

Matn ichida qo'shtirnoq kerak bo'lsa, tashqarisiga bittirnoq ishlat (yoki teskari):

```python
gap = 'U "salom" dedi'
gap2 = "It's a book"
```

**Uzunligi** — `len()`:

```python
print(len("salom"))      # 5
```

**Matnni birlashtirish va takrorlash:**

```python
ism = "Aziz"
familiya = "Karimov"
print(ism + " " + familiya)    # Aziz Karimov   (+ birlashtiradi)
print("=" * 20)                # ====================   (* takrorlaydi)
```

> **Diqqat:** `+` faqat matnni matn bilan birlashtiradi. Matnga son qo'shmoqchi bo'lsang, avval sonni `str()` bilan matnga aylantir:
> ```python
> yosh = 25
> print("Yosh: " + str(yosh))    # Yosh: 25
> # yoki osonroq — f-string:
> print(f"Yosh: {yosh}")         # Yosh: 25
> ```

---

## 4.2 Matn metodlari

Matnga amal qiladigan ko'plab tayyor metodlar bor. `matn.metod()` ko'rinishida chaqiriladi:

```python
gap = "  Salom Dunyo  "

print(gap.upper())          # "  SALOM DUNYO  "   — katta harf
print(gap.lower())          # "  salom dunyo  "   — kichik harf
print(gap.strip())          # "Salom Dunyo"        — chetdagi bo'sh joylarni olib tashlaydi
print(gap.replace("Dunyo", "Olam"))   # "  Salom Olam  "  — almashtiradi
print(gap.title())          # "  Salom Dunyo  "   — har so'z bosh harf bilan
```

> **Muhim:** matn metodlari aslini **o'zgartirmaydi** — yangi matn qaytaradi. Natijani saqlash uchun o'zgaruvchiga ber:
> ```python
> gap = "  Salom  "
> gap = gap.strip()        # natijani qayta saqladik
> print(gap)               # "Salom"
> ```

Quyidagi diagramma matn **o'zgarmasligini** (immutable) ko'rsatadi: metod aslini tegmaydi, balki yangi obyekt yaratadi va u faqat o'zgaruvchiga qayta saqlasang qoladi.

![Matn o'zgarmas: metod yangi obyekt yaratadi](rasmlar/py04-string-immutability.svg)

Tekshiruv metodlari (`True`/`False` qaytaradi):

```python
"salom".startswith("sal")    # True   — "sal" bilan boshlanadimi?
"rasm.jpg".endswith(".jpg")  # True   — ".jpg" bilan tugaydimi?
"12345".isdigit()            # True   — faqat raqamlardan iboratmi?
"salom".isalpha()            # True   — faqat harflardanmi?
"Salom" in "Salom Dunyo"     # True   — ichida bormi?
```

---

## 4.3 Matnni bo'laklarga ajratish va birlashtirish

**`split()`** — matnni bo'laklarga ajratib, ro'yxat qaytaradi:

```python
gap = "olma banan uzum"
sozlar = gap.split()          # bo'sh joy bo'yicha ajratadi
print(sozlar)                 # ['olma', 'banan', 'uzum']

sana = "2026-06-09"
qismlar = sana.split("-")     # "-" bo'yicha ajratadi
print(qismlar)                # ['2026', '06', '09']
```

**`join()`** — ro'yxatni matnga birlashtiradi (`split` ning teskarisi):

```python
sozlar = ["olma", "banan", "uzum"]
print(", ".join(sozlar))      # "olma, banan, uzum"   — vergul bilan birlashtirdi
print(" ".join(sozlar))       # "olma banan uzum"
```

> **Eslab qol:** `ajratuvchi.join(royxat)` — ajratuvchi belgi matnga ulanib turadi. Bu yangi boshlovchilarni chalkashtiradi: `join` ro'yxatning emas, **ajratuvchi matnning** metodi.

---

## 4.4 Slicing — matnning bir qismini olish

Matn ham xuddi ro'yxatdek indekslanadi (0 dan boshlab) va slicing bilan kesib olinadi:

```python
gap = "Python"

print(gap[0])        # P       (birinchi harf)
print(gap[-1])       # n       (oxirgi harf)
print(gap[0:3])      # Pyt     (0 dan 3 gacha, 3 kirmaydi)
print(gap[2:])       # thon    (2-indeksdan oxirigacha)
print(gap[:3])       # Pyt     (boshidan 3 gacha)
print(gap[::-1])     # nohtyP  (teskari — matnni teskari aylantirish hiylasi!)
```

Quyidagi chizg'ich indekslar qanday ishlashini ko'rsatadi: musbat indeks boshidan (0 dan), manfiy indeks oxiridan (-1 dan) sanaladi, qadam (step) esa yo'nalish va sakrashni belgilaydi.

![String slicing chizg'ichi: musbat va manfiy indeks hamda qadam](rasmlar/py04-string-slicing.svg)

Matn bo'ylab aylanish:

```python
for harf in "abc":
    print(harf)          # a, b, c
```

---

## 4.5 f-string bilan formatlash (kengaytirilgan)

1-modulda f-string'ni ko'rgan edik. Eng muhim formatlash variantlarini takrorlaymiz:

```python
ism = "Aziz"
narx = 1234567.5
foiz = 0.85

f"Salom, {ism}!"             # Salom, Aziz!
f"{narx:,.2f}"               # 1,234,567.50   — minglik ajratgich + 2 kasr
f"{foiz:.1%}"                # 85.0%          — foiz
f"{ism:>10}"                 # "      Aziz"   — o'ngga tekislash, 10 belgi kenglikda
f"{ism:<10}"                 # "Aziz      "   — chapga tekislash
f"{ism:^10}"                 # "   Aziz   "   — markazga
```

Tekislash jadval ko'rinishidagi chiqarish uchun foydali:

```python
mahsulotlar = [("Olma", 12000), ("Non", 4000), ("Go'sht", 90000)]
for nom, narx in mahsulotlar:
    print(f"{nom:<10} {narx:>10,} so'm")
# Olma            12,000 so'm
# Non              4,000 so'm
# Go'sht          90,000 so'm
```

---

## 4.6 Matn ichidan qidirish (boshlang'ich)

Oddiy qidiruv uchun yuqoridagi metodlar (`in`, `startswith`, `find`) yetadi:

```python
gap = "Salom Dunyo"
print("Dunyo" in gap)        # True
print(gap.find("Dunyo"))     # 6      — qaysi indeksdan boshlanishini qaytaradi
print(gap.find("yo'q"))      # -1     — topilmasa -1
print(gap.count("o"))        # 2      — necha marta uchraydi
```

> **Ilg'or qidiruv:** murakkab namunalar (masalan "har qanday telefon raqamini top") uchun Python'da `re` (regular expressions) moduli bor. U kuchli, lekin boshlovchi uchun erta — keyingi modullarda ko'rib chiqamiz. Hozircha yuqoridagi oddiy metodlar ko'p ishni hal qiladi.

---

## 4.7 Escape ketma-ketliklar (maxsus belgilar)

Ba'zi belgilarni matn ichida to'g'ridan-to'g'ri yozib bo'lmaydi. Masalan, yangi qatorni klaviaturadan "yozolmaysan" — uning o'rniga **escape ketma-ketligi** ishlatiladi: teskari chiziq `\` va undan keyingi belgi. Bu boshlovchilar uchun juda muhim — `\n`ni bilmasdan turib chiroyli chiqarish qiyin.

```python
print("Birinchi qator\nIkkinchi qator")
# Birinchi qator
# Ikkinchi qator

print("Ism:\tAziz")          # Ism:    Aziz   (\t — tabulyatsiya, ustun tekislash)
```

Eng ko'p ishlatiladigan escape'lar:

| Escape | Ma'nosi | Misol natijasi |
|--------|---------|----------------|
| `\n` | yangi qator (newline) | qatorni sindiradi |
| `\t` | tabulyatsiya (tab) | ustun bo'shlig'i |
| `\\` | teskari chiziqning o'zi | `\` |
| `\'` | bittirnoq | `'` |
| `\"` | qo'shtirnoq | `"` |
| `★` | Unicode belgi (4 hex raqam) | `★` |
| `\xNN` | belgi (2 hex raqam) | `\x41` → `A` |
| `\0` | nol bayt (null) | ko'rinmaydi |

```python
print("C:\\Users\\Aziz")     # C:\Users\Aziz   — har bir \ ni \\ deb yozdik
print('It\'s a book')        # It's a book     — bittirnoq ichida bittirnoq
print("U \"salom\" dedi")    # U "salom" dedi  — qo'shtirnoq ichida qo'shtirnoq
print("Yulduz: ★")      # Yulduz: ★       — Unicode kod orqali belgi
print("Tab kodi: \x41")      # Tab kodi: A     — A harfining 16-lik kodi 0x41
```

> **Nega `\\` kerak?** Python `\` ni "keyingi belgi maxsus" signali deb biladi. Agar matnda haqiqiy `\` kerak bo'lsa (masalan Windows yo'llarida), uni ikki marta yozasan: `\\`. Aks holda `\U`, `\n` kabi narsalar noto'g'ri talqin qilinadi.

Escape'larni birlashtirib, formatlangan chiqarish yasash mumkin:

```python
narx = 1234
print(f"Narx:\t{narx}\nValyuta:\tso'm")
# Narx:    1234
# Valyuta: so'm
```

---

## 4.8 Raw string va ko'p qatorli matn

**Raw string (`r"..."`)** — teskari chiziqni "oddiy belgi" deb qaraydi, hech qanday escape qilmaydi. Bu Windows yo'llari va regex namunalari uchun juda qulay:

```python
yol = r"C:\Users\Aziz\rasmlar\yangi.png"
print(yol)                   # C:\Users\Aziz\rasmlar\yangi.png  — \n, \r buzmadi!

print(len("\n"))             # 1   — bitta newline belgisi
print(len(r"\n"))            # 2   — \ va n, ikkita oddiy belgi
```

Raw string'siz xuddi shu yo'lni yozish uchun har bir `\` ni ikkilashga to'g'ri kelardi (`"C:\\Users\\Aziz"`). Regex (16-modul) deyarli doim raw string bilan yoziladi:

```python
naqsh = r"\d+\.\d+"          # raqam.raqam namunasi — \ lar buzilmaydi
print(naqsh)                 # \d+\.\d+
```

**Ko'p qatorli matn (triple quote `"""..."""` yoki `'''...'''`)** — bir necha qatorni `\n`siz, ko'rinishidagidek yozish imkonini beradi:

```python
xat = """Hurmatli Aziz,

Sizning buyurtmangiz qabul qilindi.
Rahmat!"""
print(xat)
# Hurmatli Aziz,
#
# Sizning buyurtmangiz qabul qilindi.
# Rahmat!
```

Triple quote SQL so'rovlari, HTML shablonlari, uzun matnlar uchun ideal:

```python
sql = """
SELECT ism, yosh
FROM foydalanuvchilar
WHERE yosh > 18
"""
print(sql)
```

> **Birlashtirish:** `r"""..."""` ham bo'ladi — raw va ko'p qatorli birga. Triple quote shuningdek funksiya/klass ichidagi **docstring** (hujjat matni) sifatida ishlatiladi (6-modulda ko'ramiz).

---

## 4.9 Bytes va kodlash (encode / decode)

Hozirgacha biz `str` (matn) bilan ishladik — bu **belgilar** ketma-ketligi. Lekin fayllar, tarmoq, internet **baytlar** (`bytes`) bilan ishlaydi — 0–255 oralig'idagi sonlar. Matnni faylga yozish yoki tarmoqqa yuborish uchun avval uni baytlarga aylantirish kerak. Bu mavzu boshlovchi qo'llanmalarda ko'pincha tushirib qoldiriladi, lekin fayl va web bilan ishlaganda darhol kerak bo'ladi.

```python
b = b"salom"                 # b prefiksi — bu bytes, str emas
print(b)                     # b'salom'
print(type(b))               # <class 'bytes'>
print(b[0])                  # 115   — 's' harfining ASCII kodi
```

**`encode()`** — `str` → `bytes` (matnni baytlarga). **`decode()`** — `bytes` → `str` (orqaga). Standart kodlash — **UTF-8** (butun internet shuni ishlatadi):

```python
matn = "salom"
baytlar = matn.encode("utf-8")
print(baytlar)               # b'salom'

qayta = baytlar.decode("utf-8")
print(qayta)                 # salom
```

**Muhim:** lotin harflari 1 baytdan, lekin maxsus belgilar (`é`, kirill, emoji) bir necha baytdan iborat. Shuning uchun **belgilar soni ≠ baytlar soni**:

```python
print("café".encode("utf-8"))      # b'caf\xc3\xa9'  — é ikki bayt
print(len("café"))                 # 4   — belgilar
print(len("café".encode("utf-8"))) # 5   — baytlar
```

**`bytearray`** — bu `bytes`ning o'zgaruvchan (mutable) versiyasi: alohida baytni o'zgartirish mumkin:

```python
ba = bytearray(b"abc")
ba[0] = 65                   # 65 — 'A' harfining kodi
print(ba)                    # bytearray(b'Abc')
print(ba.decode())           # Abc   (utf-8 standart)
```

Amaliy misol — matnni baytlarga aylantirib, raqamlarini ko'rish:

```python
data = "Hello".encode("utf-8")
print(list(data))            # [72, 101, 108, 108, 111]
```

> **Eslab qol:** faylni `"rb"` (read binary) yoki `"wb"` (write binary) rejimda ochsang, `str` emas, `bytes` qaytadi/kutiladi (8-modulda ko'ramiz). Matnli rejimda esa Python o'zi encode/decode qiladi.

---

## 4.10 Qolgan foydali metodlar

4.2-bo'limdagi metodlarga qo'shimcha — kunlik ishda ko'p asqotadigan yana bir qancha metod:

**Bir tomonlama tozalash — `lstrip` / `rstrip`:**

```python
gap = "  Salom Dunyo  "
print(repr(gap.lstrip()))    # 'Salom Dunyo  '   — faqat chap chetdan
print(repr(gap.rstrip()))    # '  Salom Dunyo'   — faqat o'ng chetdan
print(repr("xxxAziz".lstrip("x")))   # 'Aziz'    — berilgan belgilarni olib tashlaydi
```

**Qatorlarga ajratish — `splitlines`:**

```python
matn = "bir\nikki\nuch"
print(matn.splitlines())     # ['bir', 'ikki', 'uch']   — \n bo'yicha, lekin oxirgi bo'sh element qoldirmaydi
```

**Bir marta ajratish — `partition` / `rpartition`** (uch qismli kortej qaytaradi: chap, ajratuvchi, o'ng):

```python
epost = "aziz@example.com"
print(epost.partition("@"))   # ('aziz', '@', 'example.com')
print("a.b.c".rpartition(".")) # ('a.b', '.', 'c')   — oxirgi nuqta bo'yicha
print("salom".partition("@"))  # ('salom', '', '')   — topilmasa hammasi chapda
```

**Tekislash va to'ldirish — `center` / `ljust` / `rjust` / `zfill`:**

```python
print(repr("Aziz".center(12, "*")))   # '****Aziz****'
print(repr("Aziz".ljust(10, ".")))    # 'Aziz......'
print(repr("Aziz".rjust(10)))         # '      Aziz'

print("42".zfill(5))         # 00042   — nollar bilan to'ldiradi
print("-7".zfill(5))         # -0007   — ishorani saqlaydi
```

**Registr metodlari — `casefold` / `swapcase` / `capitalize`:**

```python
print("Salom Dunyo".swapcase())      # sALOM dUNYO   — katta<->kichik almashtiradi
print("salom dunyo".capitalize())    # Salom dunyo   — faqat birinchi harf katta
print("STRASSE".casefold())          # strasse       — lower'ning kuchliroq versiyasi
print("ß".casefold())                # ss            — taqqoslash uchun ishonchli
```

> **`casefold` vs `lower`:** taqqoslashda (`a.casefold() == b.casefold()`) `casefold` ishlatish xavfsizroq, chunki u nemis `ß` kabi maxsus holatlarni ham to'g'ri qayta ishlaydi. Oddiy chiqarish uchun `lower` yetadi.

**Tekshiruv metodlari — `isnumeric` / `isspace`:**

```python
print("123".isnumeric())     # True
print("²³".isnumeric())      # True   — daraja belgilari ham raqam sanaladi
print("   ".isspace())       # True   — faqat bo'sh joydanmi?
print("abc".isspace())       # False
```

---

## 4.11 f-string format-spec to'liq grammatikasi

4.5-bo'limda f-stringning asoslarini ko'rdik. Endi to'liq grammatikasini o'rganamiz. Ikki nuqtadan keyingi format spetsifikatori shu tartibda yoziladi:

```
{qiymat:[[to'ldiruvchi]tekislash][ishora][#][0][kenglik][guruh][.aniqlik][tur]}
```

Hammasi ixtiyoriy — kerakligini qoldirasan. Quyida har bir qismni ko'rib chiqamiz.

**To'ldiruvchi (fill) + tekislash (align):** `<` chap, `>` o'ng, `^` markaz, `=` raqamlarda ishorani chetda qoldiradi:

```python
print(f"{'Aziz':*^12}")      # ****Aziz****   — * bilan markazga
print(f"{'Aziz':.<12}")      # Aziz........   — . bilan chapga
print(f"{42:>8}")            # "      42"     — o'ngga
print(f"{-42:=8}")           # "-     42"     — ishora chapda, bo'shliq o'rtada
```

**Ishora (sign): `+` `-` `(probel)`:**

```python
print(f"{42:+}")             # +42   — musbatga ham + qo'yadi
print(f"{42:-}")             # 42    — faqat manfiyga - (standart)
print(f"{42: }")             # " 42" — musbat oldida bo'shliq (jadval tekislash uchun)
print(f"{-42:+}")            # -42
```

**`#` — alternativ shakl** (asoslar uchun prefiks qo'shadi):

```python
print(f"{255:#x}")           # 0xff    — 16-lik
print(f"{255:#o}")           # 0o377   — 8-lik
print(f"{8:#b}")             # 0b1000  — 2-lik
```

**`0` va kenglik — nol bilan to'ldirish:**

```python
print(f"{42:08}")            # 00000042
print(f"{3.14:08.2f}")       # 00003.14
```

**Guruh ajratgich: `,` va `_`:**

```python
print(f"{1234567:,}")        # 1,234,567   — minglik vergul
print(f"{1234567:_}")        # 1_234_567   — minglik pastki chiziq
print(f"{1234567.5:,.2f}")   # 1,234,567.50
```

**`.aniqlik` (precision):** sonlarda kasr xonalari, matnda esa **kesish** uzunligi:

```python
print(f"{3.14159:.2f}")      # 3.14
print(f"{'salomlashamiz':.5}")  # salom   — matnni 5 belgiga kesdi
```

**Tur (type):** `d` butun, `f` kasr, `e` ilmiy, `%` foiz, `x`/`X` 16-lik, `b` 2-lik, `o` 8-lik:

```python
print(f"{0.85:.1%}")         # 85.0%
print(f"{12345.678:e}")      # 1.234568e+04
print(f"{255:x}")            # ff
print(f"{255:X}")            # FF
```

**Konversiya `!r` `!s` `!a`** — qiymatni avval `repr()` / `str()` / `ascii()` orqali o'tkazadi. `!r` xatolarni qidirishda (debug) juda qulay, chunki tirnoqlarni ko'rsatadi:

```python
ism = "Aziz"
print(f"{ism!r}")            # 'Aziz'   — repr: tirnoq bilan
print(f"{ism!s}")            # Aziz     — str (standart)
```

**Ichma-ich (nested) format** — kenglik yoki aniqlikni o'zgaruvchidan olish mumkin:

```python
kenglik = 10
print(f"{'salom':>{kenglik}}")   # "     salom"   — kenglik o'zgaruvchidan
```

**Debug `=` (3.8+)** — ifoda va qiymatini birga chiqaradi, tez tekshirish uchun ajoyib:

```python
x = 42
print(f"{x = }")             # x = 42
print(f"{x * 2 = }")         # x * 2 = 84
```

Endi bularni birlashtirib chiroyli jadval yasash mumkin:

```python
mahsulotlar = [("Olma", 12000), ("Non", 4000), ("Go'sht", 90000)]
print(f"{'Mahsulot':.<12}{'Narx':.>10}")
for nom, narx in mahsulotlar:
    print(f"{nom:.<12}{narx:>10,}")
# Mahsulot..........Narx
# Olma........    12,000
# Non.........     4,000
# Go'sht......    90,000
```

---

## ✍️ Masalalar (26 ta)

> Bu masalalar 1–4 modullar mavzulariga asoslangan.

**Oson (1–7):**

1. Foydalanuvchidan ism va familiyani alohida so'rab, ularni bo'sh joy bilan birlashtirib chiqar.
2. Bir matnni `upper()` va `lower()` bilan katta va kichik harfda chiqar.
3. `"  salom  "` matnidan chetdagi bo'sh joylarni `strip()` bilan olib tashlab chiqar.
4. Bir matnning uzunligini (`len`) chiqar.
5. `"="` belgisini 30 marta chiqar (`*` ishlat).
6. `"Python dasturlash"` matnini `split()` bilan so'zlarga ajratib chiqar.
7. `["a", "b", "c"]` ro'yxatini `"-"` bilan birlashtirib chiqar (`a-b-c`).

**O'rta (8–14):**

8. Foydalanuvchidan email so'ra. Agar ichida `"@"` bo'lsa "to'g'ri", aks holda "noto'g'ri" deb chiqar.
9. Bir so'zni slicing bilan teskari aylantir (`"salom"` → `"molas"`).
10. Foydalanuvchidan jumla so'rab, undagi so'zlar sonini chiqar (`split()` + `len`).
11. Bir matndagi biror harf (masalan `"a"`) necha marta uchrashini sana (`count`).
12. Fayl nomini (masalan `"rasm.jpg"`) tekshir: `.jpg` bilan tugasa "rasm", `.txt` bilan tugasa "matn", aks holda "boshqa" deb chiqar.
13. Foydalanuvchidan to'liq ismni (`"Aziz Karimov"`) so'rab, faqat ismini (birinchi so'z) chiqar (`split` + indeks).
14. Bir jumladagi har bir so'zni alohida qatorda chiqar (`split` + `for`).

**Murakkab (15–20):**

15. Foydalanuvchidan jumla so'rab, undagi har so'zning bosh harfini katta qil (`title()` ishlatmasdan, `split` + `for` + slicing bilan qilib ko'r).
16. Palindrom tekshir: foydalanuvchidan so'z so'rab, u teskarisiga ham bir xil o'qiladimi tekshir (`"radar"` → palindrom). Bo'sh joy va katta-kichik harfni hisobga olma.
17. Foydalanuvchidan jumla so'rab, undagi unli harflar (`a, e, i, o, u`) sonini sana.
18. Bir matndagi barcha bo'sh joylarni `"_"` ga almashtir (`replace`) va natijani chiqar.
19. Sana matnini (`"2026-06-09"`) `split("-")` bilan ajratib, `"9-iyun, 2026-yil"` ko'rinishida chiqar (oylar nomini lug'atdan ol).
20. Oddiy "shifrlash": foydalanuvchidan so'z so'rab, har bir harfni keyingi harfga almashtir (`"abc"` → `"bcd"`). Maslahat: `ord()` harfni songa, `chr()` sonni harfga aylantiradi.

**Yangi mavzular (21–26) — escape, raw, bytes, metodlar, f-string:**

21. `\n` va `\t` ishlatib, ikkita mahsulot nomi va narxini ustun ko'rinishida bir `print` da chiqar (har bir qator `\n` bilan, nom va narx orasida `\t`).
22. Raw string yordamida Windows yo'li yasaydigan `windows_yol(papka, fayl)` funksiyasini yoz: `windows_yol("Aziz", "rasm.png")` → `C:\Users\Aziz\rasm.png`. Ichida `\n`, `\r` buzilmasligi kerak.
23. `encode("utf-8")` bilan matnning **bayt hajmini** qaytaruvchi `hajm_baytlarda(matn)` funksiyasini yoz. `"salom"` → 5, `"café"` → 5 ekanini tekshir (`é` ikki bayt).
24. `zfill` bilan butun sonlar ro'yxatini (`[7, 42, 1234]`) 6 xonali, oldida nollar bilan chiqar (`000007`, `000042`, `001234`).
25. `partition("@")` yordamida email manzilni foydalanuvchi nomi va domenga ajratuvchi funksiya yoz. `"aziz@example.com"` → `("aziz", "example.com")`. `@` bo'lmasa `("", "")` qaytar.
26. `bytearray` bilan oddiy Sezar shifri: `shifrla(matn, siljish)` har bir baytga `siljish` qo'shib `bytes` qaytarsin, `shifrsizla(data, siljish)` esa orqaga ochsin. `shifrsizla(shifrla("salom", 3), 3)` → `"salom"`. Maslahat: `(bayt + siljish) % 256`.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Ko'rsatish uchun ochish</summary>

```python
# 1
ism = input("Ism: ")
familiya = input("Familiya: ")
print(ism + " " + familiya)

# 2
gap = "Salom"
print(gap.upper())        # SALOM
print(gap.lower())        # salom

# 3
print("  salom  ".strip())    # "salom"

# 4
print(len("Python"))      # 6

# 5
print("=" * 30)

# 6
print("Python dasturlash".split())    # ['Python', 'dasturlash']

# 7
print("-".join(["a", "b", "c"]))       # a-b-c

# 8
email = input("Email: ")
if "@" in email:
    print("to'g'ri")
else:
    print("noto'g'ri")

# 9
soz = "salom"
print(soz[::-1])          # molas

# 10
jumla = input("Jumla: ")
print(len(jumla.split()))

# 11
gap = "banana"
print(gap.count("a"))     # 3

# 12
fayl = "rasm.jpg"
if fayl.endswith(".jpg"):
    print("rasm")
elif fayl.endswith(".txt"):
    print("matn")
else:
    print("boshqa")

# 13
toliq = input("To'liq ism: ")
print(toliq.split()[0])   # birinchi so'z

# 14
jumla = input("Jumla: ")
for soz in jumla.split():
    print(soz)

# 15
jumla = input("Jumla: ")
natija = []
for soz in jumla.split():
    natija.append(soz[0].upper() + soz[1:])
print(" ".join(natija))

# 16
soz = input("So'z: ").lower().replace(" ", "")
if soz == soz[::-1]:
    print("palindrom")
else:
    print("palindrom emas")

# 17
jumla = input("Jumla: ").lower()
hisob = 0
for harf in jumla:
    if harf in "aeiou":
        hisob += 1
print("Unlilar soni:", hisob)

# 18
gap = input("Matn: ")
print(gap.replace(" ", "_"))

# 19
sana = "2026-06-09"
yil, oy, kun = sana.split("-")
oylar = {
    "01": "yanvar", "02": "fevral", "03": "mart", "04": "aprel",
    "05": "may", "06": "iyun", "07": "iyul", "08": "avgust",
    "09": "sentabr", "10": "oktabr", "11": "noyabr", "12": "dekabr",
}
print(f"{int(kun)}-{oylar[oy]}, {yil}-yil")    # 9-iyun, 2026-yil

# 20
soz = input("So'z: ")
natija = ""
for harf in soz:
    natija += chr(ord(harf) + 1)
print(natija)             # "abc" -> "bcd"
```

</details>

<details markdown="1">
<summary>Masala 21</summary>

```python
qatorlar = [("Olma", 12000), ("Non", 4000)]
chiqish = ""
for nom, narx in qatorlar:
    chiqish += f"{nom}\t{narx}\n"
print(chiqish, end="")
# Olma    12000
# Non     4000
```

</details>

<details markdown="1">
<summary>Masala 22</summary>

```python
def windows_yol(papka: str, fayl: str) -> str:
    return r"C:\Users" + "\\" + papka + "\\" + fayl

print(windows_yol("Aziz", "rasm.png"))   # C:\Users\Aziz\rasm.png
```

</details>

<details markdown="1">
<summary>Masala 23</summary>

```python
def hajm_baytlarda(matn: str) -> int:
    return len(matn.encode("utf-8"))

print(hajm_baytlarda("salom"))   # 5
print(hajm_baytlarda("café"))    # 5  (é ikki bayt, lekin c-a-f bir baytdan)
```

</details>

<details markdown="1">
<summary>Masala 24</summary>

```python
sonlar = [7, 42, 1234]
for n in sonlar:
    print(str(n).zfill(6))
# 000007
# 000042
# 001234
```

</details>

<details markdown="1">
<summary>Masala 25</summary>

```python
def email_ajrat(email: str) -> tuple[str, str]:
    nom, belgi, domen = email.partition("@")
    if belgi == "":          # "@" topilmadi
        return ("", "")
    return (nom, domen)

print(email_ajrat("aziz@example.com"))   # ('aziz', 'example.com')
print(email_ajrat("notog'ri"))           # ('', '')
```

</details>

<details markdown="1">
<summary>Masala 26</summary>

```python
def shifrla(matn: str, siljish: int) -> bytes:
    ba = bytearray(matn.encode("utf-8"))
    for i in range(len(ba)):
        ba[i] = (ba[i] + siljish) % 256
    return bytes(ba)

def shifrsizla(data: bytes, siljish: int) -> str:
    ba = bytearray(data)
    for i in range(len(ba)):
        ba[i] = (ba[i] - siljish) % 256
    return ba.decode("utf-8")

shifr = shifrla("salom", 3)
print(shifr)                      # b'vdorp'
print(shifrsizla(shifr, 3))       # salom
```

</details>

---

[← Ma'lumot tuzilmalari](./03-malumot-tuzilmalari.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: OOP (klasslar) →](./05-oop.md)
