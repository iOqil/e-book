# 16 — Muntazam ifodalar (regex, `re` moduli)

Tasavvur qil: foydalanuvchi formaga email kiritdi — `aziz@mail` deb. Bu to'g'ri emailmi? Yoki minglab qatorli log faylidan faqat xato (`ERROR`) qatorlarini, ulardagi sana va IP manzilni ajratib olish kerak. Bularni oddiy `in`, `.split()`, `.find()` bilan qilish mumkin, lekin tezda halokatga aylanadi — chunki bunday tekshiruvlar **naqsh** (pattern) ustida ishlaydi: "bir nechta harf, keyin `@`, keyin domen, keyin nuqta...". Mana shu naqshlarni qisqa, kuchli tilda yozish vositasi — **muntazam ifodalar** (regular expressions, qisqacha **regex**), Python'da esa `re` moduli orqali.

Regex avvaliga "begona alifbo" kabi ko'rinadi (`r"^\d{3}-\d{2}$"` nimaga o'xshaydi?), lekin u aslida juda mantiqiy. Bu bobda har bir belgini noldan, analogiya bilan tushuntiramiz va har birini real misolda — email, O'zbekiston telefoni, parol, sana, IP, log — ishlatib ko'ramiz.

> **Bu modulda:** `re` modulining barcha asosiy funksiyalari (`search`, `match`, `fullmatch`, `findall`, `finditer`, `sub`, `split`), raw string `r"..."` nega zarurligi, naqsh sintaksisi to'liq (`. \d \w \s`, belgi sinflari, anchorlar, miqdorlar, guruhlar, nomli guruhlar, tanlov, ekranlash), bayroqlar (`IGNORECASE`, `MULTILINE`, `DOTALL`), `re.compile`, Match obyekti, hamda real validatsiya va parsing misollari.

---

## 16.1 Birinchi regex: naqsh bormi yoki yo'qmi?

Regex bilan ishlash uchun avval `re` modulini import qilamiz. Eng oddiy savol: **"shu matnda shu naqsh bormi?"** Buni `re.search()` hal qiladi — u matnni boshidan oxirigacha qidiradi va **birinchi** moslikni topadi.

```python
import re

matn = "Mening yoshim 25 da"
natija = re.search(r"\d+", matn)    # \d+ — bir yoki ko'p raqam

print(natija)            # <re.Match object; span=(14, 16), match='25'>
print(natija.group())    # 25  — topilgan qism
```

`re.search()` ikkita narsa qaytaradi:
- agar moslik **topilsa** — `Match` obyekti (uni `if` da `True` deb hisoblaydi);
- agar **topilmasa** — `None`.

Shuning uchun natijani odatda `if` bilan tekshiramiz:

```python
import re

def raqam_bormi(matn: str) -> bool:
    return re.search(r"\d", matn) is not None

print(raqam_bormi("salom123"))   # True
print(raqam_bormi("salom"))      # False
```

Bu yerda `\d` — "bitta raqam" degani. Naqsh nimani anglatishini keyingi bo'limlarda batafsil ko'ramiz; hozir asosiy oqimni tushunib ol: **naqsh + matn → Match yoki None**.

---

## 16.2 Raw string `r"..."` — nega regex'da shart?

Yuqorida naqshni `r"\d+"` deb yozdik — boshida `r` harfi bilan. Bu **raw string** (xom satr). Nega kerak?

Muammo shundaki, Python'ning oddiy satrida `\` (teskari chiziq) maxsus ma'noga ega: `\n` — yangi qator, `\t` — tabulyatsiya, `\b` — backspace. Lekin regex'ning o'zi ham `\` dan keng foydalanadi (`\d`, `\w`, `\b`). Natijada chalkashlik chiqadi:

```python
print("\d")     # Python ogohlantiradi: \d maxsus emas, lekin xavfli
print("\n")     # bu — yangi qator (bo'sh satr chiqadi)
print(r"\n")    # bu — ikki belgi: \ va n
```

Raw string `r"..."` ichida `\` **oddiy belgi** sifatida qoladi, hech narsa "tarjima" qilinmaydi. Demak `r"\d"` — aynan `\` va `d` ikki belgisi, va regex buni "raqam" deb to'g'ri o'qiydi.

```python
import re

# r SIZ — \b ni Python "backspace" deb tarjima qiladi, regex buziladi
print(re.findall("\bsom", "1000 som"))    # []  — ishlamaydi

# r BILAN — \b regex'ga "so'z chegarasi" bo'lib yetadi
print(re.findall(r"\bsom", "1000 som"))   # ['som']  — to'g'ri
```

> **Qoida:** regex naqshini **doim** `r"..."` bilan yoz. Bu odat seni ko'p tushunarsiz xatolardan qutqaradi.

---

## 16.3 `search`, `match`, `fullmatch` — uchta turli savol

Uchala funksiya ham naqshni qidiradi, lekin **qayerdan** qidirishi va **qancha** qismni talab qilishi bilan farq qiladi. Bu farqni tushunish juda muhim.

- **`re.search`** — naqsh matnning **istalgan joyida** bormi?
- **`re.match`** — naqsh matnning **boshidan** boshlanadimi? (oxirigacha shart emas)
- **`re.fullmatch`** — naqsh **butun matnga** to'liq mos keladimi? (boshidan oxirigacha)

```python
import re

matn = "abc123"

print(re.search(r"\d+", matn))      # match='123'  — istalgan joyda topdi
print(re.match(r"\d+", matn))       # None         — bosh '1' emas, 'a'
print(re.match(r"[a-z]+", matn))    # match='abc'  — bosh harflar bilan boshlandi
print(re.fullmatch(r"[a-z]+", matn))  # None       — butun matn faqat harf emas
print(re.fullmatch(r"[a-z]+\d+", matn))  # match='abc123'  — to'liq mos
```

Buni shunday eslab qol:
- **search** — "ichidan top" (lupa bilan qidiradi),
- **match** — "boshidan boshlanadimi",
- **fullmatch** — "aynan shumi" (validatsiya uchun eng qulayi).

Email yoki telefonni **tekshirishda** odatda `re.fullmatch` ishlatamiz — chunki bizga "matn **butunlay** to'g'ri formatdami" kerak, "ichida bormi" emas.

---

## 16.4 Pattern asoslari: literal va `.` (har qanday belgi)

Naqshning eng oddiy turi — **literal**, ya'ni belgilarning o'zi. `r"som"` naqshi matndagi aynan `som` ketma-ketligini qidiradi.

```python
import re
print(re.search(r"som", "1000 som").group())   # som
```

Maxsus belgi `.` (nuqta) — **istalgan bitta belgini** anglatadi (yangi qatordan tashqari):

```python
import re

print(re.findall(r"k.t", "kot kit kut kt kart"))
# ['kot', 'kit', 'kut']
# k.t = k, istalgan bitta belgi, t
# 'kt' mos kelmadi (o'rtada belgi yo'q), 'kart' ham (ikki belgi)
```

Agar haqiqiy nuqtani qidirmoqchi bo'lsang (masalan `3.14` dagi nuqta), uni **ekranlash** kerak — `\.` deb yozasan. Bu haqda 16.13 da batafsil.

```python
import re
print(re.findall(r"\.", "3.14 va 2.71"))   # ['.', '.']  — faqat nuqtalar
```

---

## 16.5 `\d \w \s` va ularning teskarilari

Regex'da eng ko'p ishlatiladigan **maxsus belgi sinflari** — bular qisqa yozuvlar:

| Belgi | Ma'nosi | Misol |
|-------|---------|-------|
| `\d` | raqam (digit) `0-9` | `7`, `0` |
| `\w` | "so'z belgisi": harf, raqam, `_` | `a`, `5`, `_` |
| `\s` | bo'sh joy (space, tab, yangi qator) | ` `, `\t` |
| `\D` | raqam **emas** | `a`, `@` |
| `\W` | so'z belgisi **emas** | `@`, ` `, `.` |
| `\S` | bo'sh joy **emas** | `a`, `5` |

Katta harfli variant — kichik harflining **teskarisi**. Ular juda foydali:

```python
import re

matn = "Buyurtma #42 narxi 1500 som"

print(re.findall(r"\d", matn))    # ['4', '2', '1', '5', '0', '0']  — har bir raqam
print(re.findall(r"\d+", matn))   # ['42', '1500']  — raqamlar guruhi
print(re.findall(r"\w+", matn))   # ['Buyurtma', '42', 'narxi', '1500', 'som']
print(re.findall(r"\S+", matn))   # ['Buyurtma', '#42', 'narxi', '1500', 'som']
```

`\d` bilan `\d+` farqiga e'tibor ber: `\d` — bitta raqam, `\d+` — ketma-ket bir yoki ko'p raqam (miqdorlar haqida 16.8 da).

---

## 16.6 Belgi sinflari `[...]` va inkor `[^...]`

Kvadrat qavs `[...]` — "shu belgilardan **biri**" degani. Bu o'zingning maxsus sinfingni yaratish usuli.

```python
import re

# [aiu] — a, i yoki u harflaridan biri
print(re.findall(r"k[aiu]t", "kat kit kut ket kot"))
# ['kat', 'kit', 'kut']  — ket va kot mos emas (e, o yo'q)
```

Qavs ichida **diapazon** (`-`) yozish mumkin:
- `[a-z]` — kichik lotin harflari,
- `[A-Z]` — katta harflar,
- `[0-9]` — raqamlar (`\d` bilan bir xil),
- `[a-zA-Z0-9]` — harf yoki raqam.

```python
import re

print(re.findall(r"[a-z]+", "Salom Dunyo 2026"))   # ['alom', 'unyo']  — faqat kichik
print(re.findall(r"[A-Za-z]+", "Salom Dunyo 2026")) # ['Salom', 'Dunyo']
print(re.findall(r"[0-9]+", "Salom Dunyo 2026"))    # ['2026']
```

`^` belgisi qavs **ichida** va **boshida** — **inkor** ("bulardan tashqari hammasi"):

```python
import re

# [^0-9] — raqam BO'LMAGAN har qanday belgi
print(re.sub(r"[^0-9]", "", "Tel: +998-90-123-45-67"))
# 998901234567  — faqat raqamlar qoldi
```

> **Diqqat:** qavs ichida ko'p maxsus belgilar (`.`, `+`, `*`) oddiy belgiga aylanadi. `[.+]` — aynan nuqta yoki plyus belgisi, miqdor emas.

---

## 16.7 Anchorlar: `^`, `$`, `\b`

Anchorlar (langar) belgilar — ular hech narsaga "mos kelmaydi", balki **pozitsiyani** ko'rsatadi:

- `^` — matn (yoki qator) **boshi**,
- `$` — matn (yoki qator) **oxiri**,
- `\b` — **so'z chegarasi** (so'z boshi yoki oxiri).

```python
import re

print(re.search(r"^Salom", "Salom dunyo"))     # topadi — boshida 'Salom'
print(re.search(r"^Salom", "Hey, Salom"))      # None — boshida emas
print(re.search(r"dunyo$", "Salom dunyo"))     # topadi — oxirida 'dunyo'
```

`^...$` birgalikda **butun matn** shu naqshga to'liq mos kelishini talab qiladi — bu `fullmatch` ga juda o'xshaydi va validatsiyada ko'p ishlatiladi:

```python
import re

def faqat_raqamlardanmi(s: str) -> bool:
    return re.search(r"^\d+$", s) is not None

print(faqat_raqamlardanmi("12345"))    # True
print(faqat_raqamlardanmi("123a5"))    # False — o'rtada harf bor
```

`\b` (so'z chegarasi) — so'zni "yopishgan" matndan ajratib oladi. Masalan `som` so'zini topish, lekin `kosmos` ichidagisini emas:

```python
import re

print(re.findall(r"\bsom\b", "som va kosmos somon"))
# ['som']  — faqat alohida 'som' so'zi (kosmos, somon ichidagisi emas)
```

---

## 16.8 Miqdorlar: `* + ? {n} {n,m}`

Miqdorlar — naqshning bir qismi **necha marta** takrorlanishini ko'rsatadi. Bular o'zidan **oldingi** elementga tegishli.

| Miqdor | Ma'nosi |
|--------|---------|
| `*` | 0 yoki ko'p marta |
| `+` | 1 yoki ko'p marta (kamida bitta) |
| `?` | 0 yoki 1 marta (ixtiyoriy) |
| `{n}` | aniq `n` marta |
| `{n,m}` | `n` dan `m` gacha |
| `{n,}` | `n` yoki ko'p marta |

```python
import re

print(re.findall(r"go*l", "gl gol goool"))   # ['gl', 'gol', 'goool']  — 'o' 0+ marta
print(re.findall(r"go+l", "gl gol goool"))   # ['gol', 'goool']         — 'o' 1+ marta
print(re.findall(r"go?l", "gl gol gool"))    # ['gl', 'gol']            — 'o' 0 yoki 1
```

`{n}` va `{n,m}` aniq sonni belgilaydi — masalan, telefon kodi yoki pochta indeksi uchun ideal:

```python
import re

# aniq 5 ta raqam (pochta indeksi)
print(re.fullmatch(r"\d{5}", "10000"))    # match='10000'
print(re.fullmatch(r"\d{5}", "1000"))     # None — 4 ta raqam

# 2 dan 4 gacha raqam
print(re.findall(r"\d{2,4}", "1 22 333 44444"))   # ['22', '333', '4444']
```

### Dangasa (lazy) miqdor `*?` va `+?`

Odatda miqdorlar **ochko'z** (greedy) — imkon qadar **ko'proq** belgi yutadi. Ba'zan bu xato natija beradi:

```python
import re

matn = "<b>qalin</b> matn"

# ochko'z: birinchi < dan oxirgi > gacha hammasini oladi
print(re.findall(r"<.*>", matn))    # ['<b>qalin</b>']

# dangasa (*?): imkon qadar KAM oladi — har bir tegni alohida
print(re.findall(r"<.*?>", matn))   # ['<b>', '</b>']
```

`?` ni miqdordan keyin qo'ysang (`*?`, `+?`, `{n,m}?`), u **dangasa** bo'ladi — minimal mos kelishni oladi. HTML teglari, qo'shtirnoq ichidagi matnni ajratishda juda foydali.

---

## 16.9 `findall` va `finditer` — barcha mosliklar

`re.search` faqat **birinchi** moslikni topadi. Barchasini olish uchun ikki yo'l bor.

**`re.findall`** — barcha mosliklarni **ro'yxat (list)** sifatida qaytaradi (matn ko'rinishida):

```python
import re

matn = "Narxlar: 1500, 23000 va 450 som"
print(re.findall(r"\d+", matn))   # ['1500', '23000', '450']
```

**`re.finditer`** — barcha mosliklarni **Match obyektlari** ko'rinishida, birma-bir (iterator) qaytaradi. Bu pozitsiya (`.start()`, `.end()`) ham kerak bo'lganda ishlatiladi:

```python
import re

matn = "Narxlar: 1500, 23000 va 450 som"
for m in re.finditer(r"\d+", matn):
    print(f"{m.group()} → pozitsiya {m.start()}-{m.end()}")
# 1500 → pozitsiya 9-13
# 23000 → pozitsiya 15-20
# 450 → pozitsiya 24-27
```

> **Qaysi birini tanlash?** Faqat topilgan matnlar kerak bo'lsa — `findall` (oddiy). Pozitsiya yoki guruhlar bilan murakkab ishlov kerak bo'lsa — `finditer`.

`findall` ning bir o'ziga xosligi: agar naqshda **guruh** (`(...)`) bo'lsa, u butun moslik o'rniga faqat guruhlarni qaytaradi (bu haqda 16.10 da).

---

## 16.10 Guruhlar `(...)` — qismni ajratib olish

Qavs `(...)` naqshning bir qismini **guruhga** oladi — keyin o'sha qismni alohida ajratib olish mumkin. Bu regex'ning eng kuchli imkoniyatlaridan biri.

```python
import re

matn = "Sana: 2026-06-11"
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", matn)

print(m.group())     # 2026-06-11  — butun moslik (group 0)
print(m.group(1))    # 2026        — birinchi guruh
print(m.group(2))    # 06          — ikkinchi guruh
print(m.group(3))    # 11          — uchinchi guruh
print(m.groups())    # ('2026', '06', '11')  — barcha guruhlar tuple
```

`group(0)` (yoki shunchaki `group()`) — butun moslik. `group(1)`, `group(2)` ... — qavslar tartibida. `groups()` — barchasini birdan tuple qilib qaytaradi.

Guruhlarni `findall` bilan ishlatganda, u faqat guruhlarni qaytaradi:

```python
import re

matn = "Aziz: 25, Malika: 30, Bobur: 19"
print(re.findall(r"(\w+): (\d+)", matn))
# [('Aziz', '25'), ('Malika', '30'), ('Bobur', '19')]
# har bir moslik uchun (ism, yosh) jufti
```

---

## 16.11 Nomli guruhlar `(?P<ism>...)`

Guruhlarni raqam (`group(1)`) bilan emas, **nom** bilan chaqirish ancha o'qiladigan kod beradi — ayniqsa guruh ko'p bo'lsa. Sintaksis: `(?P<ism>...)`.

```python
import re

matn = "2026-06-11"
m = re.search(r"(?P<yil>\d{4})-(?P<oy>\d{2})-(?P<kun>\d{2})", matn)

print(m.group("yil"))    # 2026
print(m.group("oy"))     # 06
print(m.group("kun"))    # 11
print(m.groupdict())     # {'yil': '2026', 'oy': '06', 'kun': '11'}
```

`m.groupdict()` — barcha nomli guruhlarni **lug'at (dict)** qilib qaytaradi. Bu juda qulay: natijani to'g'ridan-to'g'ri o'zgaruvchilarga yoki strukturaga solish mumkin.

```python
import re

def sanani_ajrat(s: str) -> dict[str, int] | None:
    m = re.fullmatch(r"(?P<kun>\d{2})\.(?P<oy>\d{2})\.(?P<yil>\d{4})", s)
    if m is None:
        return None
    return {k: int(v) for k, v in m.groupdict().items()}

print(sanani_ajrat("11.06.2026"))   # {'kun': 11, 'oy': 6, 'yil': 2026}
print(sanani_ajrat("xato"))         # None
```

---

## 16.12 Tanlov `|` — "yoki"

Vertikal chiziq `|` — "yoki" degani: bir nechta variantdan birini tanlaydi.

```python
import re

# 'olma' yoki 'anor' yoki 'uzum'
print(re.findall(r"olma|anor|uzum", "olma anor banan uzum"))
# ['olma', 'anor', 'uzum']
```

Tanlovni guruh bilan birlashtirib, qismga qo'llash mumkin:

```python
import re

# fayl kengaytmasi: jpg, png yoki gif
matn = "rasm.jpg hujjat.pdf logo.png ikon.gif"
print(re.findall(r"\w+\.(jpg|png|gif)", matn))
# ['jpg', 'png', 'gif']  — faqat mos kengaytmalar (qavs guruh bo'lgani uchun)
```

Yana bir misol — salomlashishning turli shakllarini topish:

```python
import re

matn = "Salom! Assalomu alaykum. Hayrli kun."
print(re.findall(r"Salom|Assalomu|Hayrli", matn))
# ['Salom', 'Assalomu', 'Hayrli']
```

---

## 16.13 Ekranlash `\` — maxsus belgini oddiy qilish

`. + * ? ( ) [ ] { } | ^ $ \` — bular regex'da **maxsus** ma'noga ega. Agar shu belgilarning **o'zini** qidirmoqchi bo'lsak, oldiga `\` qo'yib **ekranlash** (escape) kerak.

```python
import re

# . ni ekranlamasdan — har qanday belgini bildiradi (xato)
print(re.findall(r"3.14", "3.14 va 3X14"))   # ['3.14', '3X14']  — ikkalasi ham!

# \. bilan — faqat haqiqiy nuqta
print(re.findall(r"3\.14", "3.14 va 3X14"))  # ['3.14']  — to'g'ri
```

Boshqa maxsus belgilarni ekranlash misoli — narx va qavs:

```python
import re

matn = "Narx: $5 (chegirma) va $10"
print(re.findall(r"\$\d+", matn))      # ['$5', '$10']  — \$ haqiqiy dollar belgisi
print(re.findall(r"\(\w+\)", matn))    # ['(chegirma)']  — \( va \) qavslar
```

Agar ko'p belgini ekranlash kerak bo'lsa, `re.escape()` foydalaniladi — u matndagi barcha maxsus belgilarni avtomatik ekranlaydi:

```python
import re

foydalanuvchi_kiritdi = "narx (3.5$)"
xavfsiz = re.escape(foydalanuvchi_kiritdi)
print(xavfsiz)    # narx\ \(3\.5\$\)
# endi bu naqshni xavfsiz ishlatish mumkin
print(re.search(xavfsiz, "Yangi narx (3.5$) bugun").group())   # narx (3.5$)
```

---

## 16.14 `re.sub` — almashtirish (topib, o'zgartirish)

`re.sub(naqsh, almashtiruvchi, matn)` — naqshga mos kelgan **barcha** qismlarni boshqa matnga almashtiradi. Bu "topib-almashtirish" ning juda kuchli varianti.

```python
import re

# Barcha raqamlarni # bilan yashirish
print(re.sub(r"\d", "#", "Karta: 1234 5678"))   # Karta: #### ####

# Ortiqcha bo'shliqlarni bittaga keltirish
print(re.sub(r"\s+", " ", "Salom    dunyo\t\tbugun"))   # Salom dunyo bugun
```

Almashtiruvchi matnda **guruhga** murojaat qilish mumkin — `\1`, `\2` yoki nomli guruh `\g<ism>`. Bu format o'zgartirishda zo'r ishlaydi:

```python
import re

# Sanani YYYY-MM-DD dan DD.MM.YYYY ga aylantirish
matn = "Bugun 2026-06-11"
natija = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3.\2.\1", matn)
print(natija)   # Bugun 11.06.2026
```

Almashtiruvchi sifatida **funksiya** ham berish mumkin — har bir moslik shu funksiyaga Match obyekti bo'lib uzatiladi:

```python
import re

# Har bir sonni ikki barobar oshirish
def ikki_barobar(m: re.Match) -> str:
    return str(int(m.group()) * 2)

print(re.sub(r"\d+", ikki_barobar, "5 olma, 10 nok"))   # 10 olma, 20 nok
```

> **`re.subn`** — `sub` bilan bir xil, lekin `(natija, nechta_almashtirildi)` tuplini qaytaradi. Nechta o'zgarish bo'lganini bilish kerak bo'lsa foydali.

---

## 16.15 `re.split` — naqsh bo'yicha bo'lish

Oddiy `str.split()` faqat bitta ajratuvchi bilan ishlaydi. `re.split()` esa **naqsh** bo'yicha bo'ladi — bir nechta turli ajratuvchini birato'la qo'llash mumkin.

```python
import re

# Vergul, nuqta-vergul yoki bo'shliq bilan ajratilgan
matn = "olma, anor; uzum  banan"
print(re.split(r"[,;\s]+", matn))   # ['olma', 'anor', 'uzum', 'banan']
```

`[,;\s]+` naqshi — "bir yoki ko'p vergul, nuqta-vergul yoki bo'sh joy" — ketma-ket ajratuvchilarni ham to'g'ri yutadi. Yana bir misol:

```python
import re

# Matnni gaplarga bo'lish (. ! ? bo'yicha)
matn = "Salom! Qalaysan? Yaxshi. Rahmat."
gaplar = re.split(r"[.!?]\s*", matn)
print([g for g in gaplar if g])   # ['Salom', 'Qalaysan', 'Yaxshi', 'Rahmat']
```

---

## 16.16 Bayroqlar (flags): `IGNORECASE`, `MULTILINE`, `DOTALL`

Bayroqlar regex'ning xatti-harakatini o'zgartiradi. Ular funksiyaga `flags=` argumenti orqali beriladi.

**`re.IGNORECASE`** (qisqa: `re.I`) — katta-kichik harfni e'tiborsiz qoldiradi:

```python
import re

print(re.findall(r"salom", "Salom SALOM salom", flags=re.IGNORECASE))
# ['Salom', 'SALOM', 'salom']
```

**`re.MULTILINE`** (`re.M`) — `^` va `$` ni har bir **qatorning** boshi/oxiriga moslaydi (butun matnniki emas):

```python
import re

matn = """1-qator
2-qator
3-qator"""

# MULTILINE'siz: faqat butun matnning boshi
print(re.findall(r"^\d", matn))                      # ['1']
# MULTILINE bilan: har qatorning boshi
print(re.findall(r"^\d", matn, flags=re.MULTILINE))  # ['1', '2', '3']
```

**`re.DOTALL`** (`re.S`) — `.` belgisi yangi qatorni (`\n`) **ham** moslaydi (odatda moslamaydi):

```python
import re

matn = "boshi\noxiri"
print(re.findall(r"boshi.oxiri", matn))                 # []  — . qatorni o'tmaydi
print(re.findall(r"boshi.oxiri", matn, flags=re.DOTALL)) # ['boshi\noxiri']
```

Bir nechta bayroqni birlashtirish uchun `|` (OR) ishlatiladi: `flags=re.IGNORECASE | re.MULTILINE`.

---

## 16.17 `re.compile` — naqshni qayta ishlatish

Agar bitta naqshni **ko'p marta** ishlatsang (masalan, siklda har qatorni tekshirish), uni har safar qaytadan "tarjima qilish" samarasiz. `re.compile()` naqshni bir marta **tayyor obyektga** aylantiradi, keyin uni qayta-qayta ishlatasan.

```python
import re

# Naqshni bir marta tayyorlash
email_naqsh = re.compile(r"[\w.]+@[\w.]+\.\w+")

# Endi obyektning o'z metodlari bor (re. emas, naqsh.)
print(email_naqsh.search("aloqa: aziz@mail.uz").group())   # aziz@mail.uz
print(email_naqsh.findall("a@b.uz va c@d.com"))            # ['a@b.uz', 'c@d.com']
```

Compiled obyektda `.search()`, `.match()`, `.fullmatch()`, `.findall()`, `.finditer()`, `.sub()`, `.split()` — barcha metodlar mavjud, faqat naqshni qayta yozish shart emas. Bayroqni ham compile vaqtida berish mumkin:

```python
import re

naqsh = re.compile(r"xato", flags=re.IGNORECASE)
print(naqsh.findall("XATO va Xato va xato"))   # ['XATO', 'Xato', 'xato']
```

> **Qoida:** naqshni faqat bir-ikki marta ishlatsang — to'g'ridan-to'g'ri `re.search(...)` yetarli. Ko'p marta (siklda, funksiyada) ishlatsang — `re.compile` bilan tayyorla. Bu tezroq va o'qiladigan.

---

## 16.18 Match obyekti to'liq: `.group`, `.start`, `.end`, `.span`

Har bir muvaffaqiyatli moslik — `Match` obyekti. Uning foydali metodlari:

- `.group()` / `.group(0)` — butun moslik,
- `.group(n)` — `n`-guruh,
- `.groups()` — barcha guruhlar (tuple),
- `.groupdict()` — nomli guruhlar (dict),
- `.start()`, `.end()` — moslik boshlanish/tugash indeksi,
- `.span()` — `(start, end)` tuple.

```python
import re

matn = "Mahsulot kodi: AB-1234 tayyor"
m = re.search(r"(?P<harf>[A-Z]{2})-(?P<son>\d{4})", matn)

print(m.group())          # AB-1234       — butun moslik
print(m.group("harf"))    # AB            — nomli guruh
print(m.group("son"))     # 1234
print(m.groups())         # ('AB', '1234')
print(m.groupdict())      # {'harf': 'AB', 'son': '1234'}
print(m.start(), m.end()) # 15 22
print(m.span())           # (15, 22)
print(matn[m.start():m.end()])   # AB-1234  — span orqali kesib olish
```

Bu metodlar, ayniqsa `finditer` bilan birga, matndagi mosliklarni aniq joylashuvi bilan qayta ishlashda zarur bo'ladi.

---

## 16.19 REAL: email validatsiyasi

Endi o'rganganlarni birlashtirib, amaliy validatorlar yozamiz. Email uchun soddalashtirilgan, lekin amalda ishlaydigan naqsh:

```python
import re

EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

def email_togrimi(s: str) -> bool:
    return EMAIL.fullmatch(s) is not None

for e in ["aziz@mail.uz", "a.b+test@gmail.com", "xato@", "@yoq.uz", "oddiy matn"]:
    print(f"{e:20} → {email_togrimi(e)}")
# aziz@mail.uz         → True
# a.b+test@gmail.com   → True
# xato@                → False
# @yoq.uz              → False
# oddiy matn           → False
```

Naqshni qism-qismga ajratamiz:
- `^[\w.+-]+` — boshida bir yoki ko'p so'z belgisi, nuqta, plyus yoki tire (foydalanuvchi nomi),
- `@` — majburiy "kuchukcha",
- `[\w-]+` — domen nomi,
- `\.` — haqiqiy nuqta (ekranlangan),
- `[\w.-]+$` — domen kengaytmasi (`uz`, `com`, `co.uk`), oxirigacha.

> **Eslatma:** "100% to'g'ri" email regex'i juda murakkab (RFC standarti). Amalda yuqoridagi kabi soddalashtirilgan naqsh aksar holatlarda yetarli. Mukammal tekshiruv kerak bo'lsa, `email-validator` kabi kutubxonadan foydalaniladi.

---

## 16.20 REAL: O'zbekiston telefon raqami (+998)

O'zbekiston raqami: `+998` mamlakat kodi, keyin 2 raqamli operator kodi, keyin 7 raqam. Odamlar uni turlicha yozadi (`+998 90 123-45-67`, `998901234567`). Avval tozalaymiz, keyin tekshiramiz.

```python
import re

def telefon_normalla(s: str) -> str | None:
    # Faqat raqamlarni qoldiramiz (bo'shliq, tire, qavs, + ni olib tashlaymiz)
    raqamlar = re.sub(r"\D", "", s)
    # 998 bilan boshlanishi va jami 12 raqam bo'lishi kerak
    if re.fullmatch(r"998\d{9}", raqamlar):
        return "+" + raqamlar
    return None

for t in ["+998 90 123 45 67", "998901234567", "90-123-45-67", "+1 555 0100"]:
    print(f"{t:20} → {telefon_normalla(t)}")
# +998 90 123 45 67    → +998901234567
# 998901234567         → +998901234567
# 90-123-45-67         → None   (mamlakat kodi yo'q)
# +1 555 0100          → None   (998 emas)
```

Bu yondashuv kuchli: avval `re.sub(r"\D", "", s)` bilan **barcha** ajratuvchilarni tozalaymiz, keyin toza raqamni `fullmatch` bilan tekshiramiz. Foydalanuvchi qanday yozishidan qat'i nazar ishlaydi.

Operator kodini ajratib olmoqchi bo'lsak, nomli guruh ishlatamiz:

```python
import re

m = re.fullmatch(r"998(?P<operator>\d{2})(?P<raqam>\d{7})", "998901234567")
print(m.group("operator"))   # 90
print(m.group("raqam"))      # 1234567
```

---

## 16.21 REAL: parol mustahkamligini tekshirish

Yaxshi parol qoidasi: kamida 8 belgi, ichida katta harf, kichik harf, raqam va maxsus belgi bo'lsin. Buni bitta ulkan regex bilan yozish qiyin va o'qilmaydi — shuning uchun **har shartni alohida** kichik regex bilan tekshiramiz:

```python
import re

def parol_tekshir(p: str) -> list[str]:
    xatolar = []
    if len(p) < 8:
        xatolar.append("kamida 8 belgi bo'lishi kerak")
    if not re.search(r"[A-Z]", p):
        xatolar.append("katta harf bo'lishi kerak")
    if not re.search(r"[a-z]", p):
        xatolar.append("kichik harf bo'lishi kerak")
    if not re.search(r"\d", p):
        xatolar.append("raqam bo'lishi kerak")
    if not re.search(r"[!@#$%^&*]", p):
        xatolar.append("maxsus belgi (!@#$...) bo'lishi kerak")
    return xatolar

print(parol_tekshir("Aziz123!"))   # []  — kuchli parol
print(parol_tekshir("aziz"))
# ['kamida 8 belgi...', 'katta harf...', 'raqam...', 'maxsus belgi...']
```

Bu usul — bitta murakkab naqshdan ko'ra ancha tushunarli va foydalanuvchiga **aniq** nima yetishmayotganini aytadi. Regex'ni qachon **bo'lish** kerakligiga yaxshi misol.

---

## 16.22 REAL: sana va IP manzil validatsiyasi

**Sana** (`DD.MM.YYYY`) ni ajratib, qism-qismlari mantiqan to'g'ri ekanini ham tekshiramiz:

```python
import re

def sana_ajrat(s: str) -> tuple[int, int, int] | None:
    m = re.fullmatch(r"(?P<kun>\d{1,2})\.(?P<oy>\d{1,2})\.(?P<yil>\d{4})", s)
    if m is None:
        return None
    kun, oy, yil = int(m["kun"]), int(m["oy"]), int(m["yil"])
    if not (1 <= kun <= 31 and 1 <= oy <= 12):
        return None
    return kun, oy, yil

print(sana_ajrat("11.06.2026"))   # (11, 6, 2026)
print(sana_ajrat("45.13.2026"))   # None  — format to'g'ri, lekin qiymat noto'g'ri
print(sana_ajrat("2026/06/11"))   # None  — format noto'g'ri
```

Diqqat: `m["kun"]` — `m.group("kun")` ning qisqa shakli (Match obyektini lug'at kabi indekslash mumkin).

**IP manzil** (`192.168.1.1`) — to'rtta 0-255 oraliqdagi son, nuqta bilan ajratilgan:

```python
import re

# Har bir oktet 0-255: 25[0-5] | 2[0-4]\d | 1\d\d | [1-9]?\d
OKTET = r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
IP = re.compile(rf"^{OKTET}\.{OKTET}\.{OKTET}\.{OKTET}$")

def ip_togrimi(s: str) -> bool:
    return IP.fullmatch(s) is not None

print(ip_togrimi("192.168.1.1"))     # True
print(ip_togrimi("255.255.255.0"))   # True
print(ip_togrimi("256.1.1.1"))       # False  — 256 > 255
print(ip_togrimi("1.2.3"))           # False  — 4 ta bo'lak emas
```

Bu yerda `rf"..."` — raw va f-string birga (naqsh ichida `{OKTET}` o'zgaruvchisini qo'yamiz). Murakkab naqshni kichik bo'laklardan qurish — professional usul.

---

## 16.23 REAL: log faylini tahlil qilish

Eng kuchli real misol — log parsing. Quyidagi formatdagi loglardan sana, daraja (level) va xabarni ajratib olamiz:

```python
import re

log = """2026-06-11 09:15:23 INFO Server ishga tushdi
2026-06-11 09:16:01 ERROR Bazaga ulanib bo'lmadi
2026-06-11 09:16:05 WARNING Xotira kam qoldi
2026-06-11 09:17:30 ERROR Timeout: 30s"""

NAQSH = re.compile(
    r"(?P<sana>\d{4}-\d{2}-\d{2}) "
    r"(?P<vaqt>\d{2}:\d{2}:\d{2}) "
    r"(?P<level>\w+) "
    r"(?P<xabar>.+)"
)

# Faqat ERROR qatorlarini ajratamiz
for m in NAQSH.finditer(log):
    if m["level"] == "ERROR":
        print(f"[{m['vaqt']}] {m['xabar']}")
# [09:16:01] Bazaga ulanib bo'lmadi
# [09:17:30] Timeout: 30s
```

Naqsh bir nechta string sifatida yozilgan — Python ularni avtomatik birlashtiradi (qulay, har qism alohida o'qiladi). Nomli guruhlar har qatorni strukturaga aylantiradi: shu tarzda minglab qatorli logni soniyalarda tahlil qilish mumkin.

---

## 16.24 REAL: matndan hashtag, son va boshqa naqshlar

Ijtimoiy tarmoq matnidan **hashtag** larni ajratish:

```python
import re

post = "Bugun #Python o'rgandim! #dasturlash #code2026 zo'r ekan"
print(re.findall(r"#\w+", post))
# ['#Python', '#dasturlash', '#code2026']
```

Matndan barcha **sonlarni** (butun va kasr) topish:

```python
import re

matn = "Narx 1500.50 som, chegirma 10%, jami 1350.45"
print(re.findall(r"\d+\.?\d*", matn))   # ['1500.50', '10', '1350.45']
# \d+ butun qism, \.? ixtiyoriy nuqta, \d* kasr qism
```

**URL** havolalarni ajratish:

```python
import re

matn = "Sayt https://ioqil.uz va https://github.com/iOqil yaxshi"
print(re.findall(r"https?://[\w./-]+", matn))
# ['https://ioqil.uz', 'https://github.com/iOqil']
# https? — 's' ixtiyoriy (http yoki https)
```

Bu uchala misol regex'ning kundalik ishdagi eng tez-tez uchraydigan vazifalarini ko'rsatadi: matndan kerakli naqshni **toping va ajratib oling**.

---

## 16.25 Ushlamaydigan guruh `(?:...)` va lookahead

Ba'zan guruh kerak (`|` yoki miqdor uchun), lekin uni **ushlab qolish** (capture) shart emas. `(?:...)` — ushlamaydigan guruh: guruhlaydi, lekin natijaga qo'shmaydi:

```python
import re

matn = "2024-yil, 2025-yil"
print(re.findall(r"(\d{4})(?:-yil)", matn))   # ['2024', '2025'] — faqat yil
print(re.findall(r"(\d{4})(-yil)", matn))     # [('2024', '-yil'), ('2025', '-yil')] — ortiqcha
```

**Lookahead** — "oldinda nima borligini" guruhga olmasdan tekshirish. `(?=...)` ijobiy, `(?!...)` salbiy, `(?<=...)`/`(?<!...)` lookbehind:

```python
import re

# Oldida "so'm" bo'lgan son ("so'm" natijaga kirmaydi):
print(re.findall(r"\d+(?= so'm)", "Olma 5000 so'm, Non 3000 so'm"))   # ['5000', '3000']
# Oldida "$" bo'lgan son (lookbehind):
print(re.findall(r"(?<=\$)\d+", "narx $100 va 200"))                 # ['100']
```

📌 Lookahead/lookbehind naqshga **shart** qo'yadi, lekin o'sha qismni natijaga olmaydi. Kuchli parol qoidasida qulay: `(?=.*\d)` — "ichida raqam bo'lsin".

## 16.26 Orqa havola `` — takrorlangan qismni topish

Naqsh ichida ilgari ushlangan guruhga ``, `` bilan murojaat qilish — "xuddi shu" qismni qayta talab qiladi:

```python
import re

# Ketma-ket takrorlangan so'zni top:
print(re.findall(r"(\w+)\s+", "salom salom, xayr dunyo dunyo"))   # ['salom', 'dunyo']
# Nomli guruhga orqa havola (?P=ism):
print(bool(re.fullmatch(r"(?P<x>\w)(?P=x)", "aa")))   # True (ikki bir xil harf)
```

## 16.27 `re.VERBOSE` — o'qiladigan murakkab naqsh

Uzun naqsh tushunarsiz bo'ladi. `re.VERBOSE` (yoki `re.X`) naqsh ichida **bo'sh joy va izoh** yozishga ruxsat beradi:

```python
import re

telefon = re.compile(r"""
    \+998        # davlat kodi
    \s?          # ixtiyoriy bo'sh joy
    \d{2}        # operator kodi
    \s?
    \d{7}        # raqam
""", re.VERBOSE)

print(bool(telefon.fullmatch("+998 90 1234567")))   # True
```

📌 `re.VERBOSE`da haqiqiy bo'sh joyni `\ ` (ekranlangan) yoki `[ ]` bilan yozing — oddiy bo'sh joy e'tibordan qoladi.

## 16.28 Amaliy maslahatlar va keng tarqalgan xatolar

Bobni yakunlab, regex bilan ishlashda esda tutadigan asosiy qoidalar:

1. **Doim `r"..."` ishlat** — raw string regex naqshlari uchun standart.
2. **Validatsiyada `fullmatch` yoki `^...$`** — "ichida bormi" emas, "to'liq to'g'rimi" kerak bo'lganda.
3. **Murakkab naqshni bo'lib tashla** — parol kabi ko'p shartli tekshiruvni alohida kichik regex'larga ajrat. O'qiladigan va xatosi oson topiladigan bo'ladi.
4. **`re.compile` ni ko'p ishlatiladigan naqshlar uchun** — siklda yoki funksiyada qayta-qayta chaqirilsa.
5. **Nomli guruh `(?P<ism>...)` afzal** — raqamli guruhdan ko'ra o'qiladigan.
6. **Ochko'z/dangasa farqini eslab tur** — HTML/teg ajratganda `*?` (dangasa) kerak bo'ladi.
7. **Regex har narsani yechmaydi** — to'liq HTML/JSON parsing uchun maxsus kutubxona (`html.parser`, `json`) ishlat, regex emas.

> **Mashq qilish maslahati:** [regex101.com](https://regex101.com) — naqshni real vaqtda sinab ko'rish, har bir belgini izohlash uchun ajoyib vosita. Yangi regex yozayotganda undan foydalan.

Regex — boshda murakkab, lekin amaliyot bilan kuchli qurolingga aylanadi. Endi matndagi istalgan naqshni topish, tekshirish va o'zgartirishni bilasan.

---

## ✍️ Masalalar (20 ta)

> Bu masalalar shu modul (regex) mavzulariga asoslangan. `import re` ni unutma.

**Oson (1–7):**

1. `re.search` bilan tekshir: berilgan matnda kamida bitta raqam bormi? `True`/`False` qaytaruvchi `raqam_bormi(matn)` funksiyasini yoz.
2. `re.findall` bilan matndan barcha raqam guruhlarini (`\d+`) ro'yxat sifatida chiqar. Sinov: `"uy 12, xona 305"` → `['12', '305']`.
3. Matnda `Python` so'zi (katta-kichik harfga qaramay) bormi? `re.IGNORECASE` ishlatib tekshir.
4. `re.sub` bilan matndagi barcha raqamlarni `*` belgisiga almashtir. Sinov: `"PIN 1234"` → `"PIN ****"`.
5. Berilgan satr **faqat** harflardan iboratmi? `^[a-zA-Z]+$` bilan tekshiruvchi funksiya yoz.
6. `re.findall` bilan matndan barcha hashtag (`#soz`) larni ajrat.
7. `re.split` bilan vergul yoki nuqta-vergul bo'yicha matnni bo'laklarga ajrat. Sinov: `"a,b;c,d"` → `['a', 'b', 'c', 'd']`.

**O'rta (8–14):**

8. Email validatori yoz: `^[\w.+-]+@[\w-]+\.[\w.-]+$` naqshi bilan `fullmatch` qilib `True`/`False` qaytar.
9. O'zbekiston telefon raqamini tekshir: avval `re.sub(r"\D", "", s)` bilan tozalab, keyin `998\d{9}` ga mosligini tekshir.
10. `re.sub` bilan matndagi ortiqcha bo'shliqlarni (ketma-ket) bitta probelga keltir (`\s+` → `" "`).
11. Matndan barcha email manzillarni `re.findall` bilan ro'yxat qilib ajrat.
12. `re.findall` bilan matndagi barcha sonlarni (butun va kasr, masalan `3.14`) top.
13. Berilgan parolda kamida bitta katta harf, bitta raqam va uzunligi ≥8 ekanini tekshir (uchta alohida `re.search`).
14. `re.sub` va guruh bilan sanani `YYYY-MM-DD` dan `DD.MM.YYYY` ga aylantir.

**Murakkab (15–20):**

15. Nomli guruh `(?P<...>)` bilan `DD.MM.YYYY` sanasini ajratib, `groupdict()` orqali lug'at qaytar.
16. Log qatoridan (`2026-06-11 09:15 ERROR xabar`) nomli guruhlar bilan sana, daraja va xabarni ajrat.
17. IP manzil validatori yoz: har bir oktet 0-255 oralig'ida bo'lsin (`192.168.1.1` → `True`, `256.1.1.1` → `False`).
18. Berilgan loglar ro'yxatidan faqat `ERROR` darajali qatorlarni filtrlab chiqar (`finditer` + nomli guruh).
19. `re.sub` ga **funksiya** berib, matndagi har bir sonni 10% oshirib qaytar (`100` → `110`).
20. To'liq parol qoidasi: kamida 8 belgi, katta harf, kichik harf, raqam, maxsus belgi (`!@#$%^&*`). Yetishmagan shartlar ro'yxatini qaytar.

---

## ✅ Yechimlar

<details markdown="1">
<summary>Masala 1</summary>

```python
import re

def raqam_bormi(matn: str) -> bool:
    return re.search(r"\d", matn) is not None

print(raqam_bormi("salom123"))   # True
print(raqam_bormi("salom"))      # False
```

</details>

<details markdown="1">
<summary>Masala 2</summary>

```python
import re

print(re.findall(r"\d+", "uy 12, xona 305"))   # ['12', '305']
```

</details>

<details markdown="1">
<summary>Masala 3</summary>

```python
import re

def python_bormi(matn: str) -> bool:
    return re.search(r"python", matn, flags=re.IGNORECASE) is not None

print(python_bormi("men PYTHON yaxshi ko'raman"))   # True
print(python_bormi("java haqida"))                   # False
```

</details>

<details markdown="1">
<summary>Masala 4</summary>

```python
import re

print(re.sub(r"\d", "*", "PIN 1234"))   # PIN ****
```

</details>

<details markdown="1">
<summary>Masala 5</summary>

```python
import re

def faqat_harfmi(s: str) -> bool:
    return re.fullmatch(r"[a-zA-Z]+", s) is not None

print(faqat_harfmi("Salom"))    # True
print(faqat_harfmi("Salom1"))   # False
```

</details>

<details markdown="1">
<summary>Masala 6</summary>

```python
import re

post = "#Python va #code2026 zo'r"
print(re.findall(r"#\w+", post))   # ['#Python', '#code2026']
```

</details>

<details markdown="1">
<summary>Masala 7</summary>

```python
import re

print(re.split(r"[,;]", "a,b;c,d"))   # ['a', 'b', 'c', 'd']
```

</details>

<details markdown="1">
<summary>Masala 8</summary>

```python
import re

EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

def email_togrimi(s: str) -> bool:
    return EMAIL.fullmatch(s) is not None

print(email_togrimi("aziz@mail.uz"))   # True
print(email_togrimi("xato@"))          # False
```

</details>

<details markdown="1">
<summary>Masala 9</summary>

```python
import re

def telefon_togrimi(s: str) -> bool:
    raqamlar = re.sub(r"\D", "", s)
    return re.fullmatch(r"998\d{9}", raqamlar) is not None

print(telefon_togrimi("+998 90 123 45 67"))   # True
print(telefon_togrimi("90-123-45-67"))        # False
```

</details>

<details markdown="1">
<summary>Masala 10</summary>

```python
import re

print(re.sub(r"\s+", " ", "Salom    dunyo\t\tbugun"))   # Salom dunyo bugun
```

</details>

<details markdown="1">
<summary>Masala 11</summary>

```python
import re

matn = "Aloqa: aziz@mail.uz yoki admin@site.com"
print(re.findall(r"[\w.+-]+@[\w.-]+\.\w+", matn))
# ['aziz@mail.uz', 'admin@site.com']
```

</details>

<details markdown="1">
<summary>Masala 12</summary>

```python
import re

matn = "Narx 1500.50, soni 3, jami 4501.50"
print(re.findall(r"\d+\.?\d*", matn))   # ['1500.50', '3', '4501.50']
```

</details>

<details markdown="1">
<summary>Masala 13</summary>

```python
import re

def parol_oddiy_tekshir(p: str) -> bool:
    return (
        len(p) >= 8
        and re.search(r"[A-Z]", p) is not None
        and re.search(r"\d", p) is not None
    )

print(parol_oddiy_tekshir("Parol123"))   # True
print(parol_oddiy_tekshir("parol"))      # False
```

</details>

<details markdown="1">
<summary>Masala 14</summary>

```python
import re

matn = "Sana 2026-06-11"
print(re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3.\2.\1", matn))
# Sana 11.06.2026
```

</details>

<details markdown="1">
<summary>Masala 15</summary>

```python
import re

def sana_dict(s: str) -> dict[str, str] | None:
    m = re.fullmatch(r"(?P<kun>\d{2})\.(?P<oy>\d{2})\.(?P<yil>\d{4})", s)
    return m.groupdict() if m else None

print(sana_dict("11.06.2026"))   # {'kun': '11', 'oy': '06', 'yil': '2026'}
print(sana_dict("xato"))         # None
```

</details>

<details markdown="1">
<summary>Masala 16</summary>

```python
import re

qator = "2026-06-11 09:15 ERROR Bazaga ulanib bo'lmadi"
m = re.search(
    r"(?P<sana>\d{4}-\d{2}-\d{2}) (?P<vaqt>\d{2}:\d{2}) "
    r"(?P<level>\w+) (?P<xabar>.+)",
    qator,
)
print(m["sana"], m["level"], "→", m["xabar"])
# 2026-06-11 ERROR → Bazaga ulanib bo'lmadi
```

</details>

<details markdown="1">
<summary>Masala 17</summary>

```python
import re

OKTET = r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
IP = re.compile(rf"^{OKTET}\.{OKTET}\.{OKTET}\.{OKTET}$")

def ip_togrimi(s: str) -> bool:
    return IP.fullmatch(s) is not None

print(ip_togrimi("192.168.1.1"))   # True
print(ip_togrimi("256.1.1.1"))     # False
```

</details>

<details markdown="1">
<summary>Masala 18</summary>

```python
import re

log = """2026-06-11 09:15 INFO Boshlandi
2026-06-11 09:16 ERROR Xato 1
2026-06-11 09:17 WARNING Ogohlantirish
2026-06-11 09:18 ERROR Xato 2"""

NAQSH = re.compile(r"(?P<vaqt>\d{2}:\d{2}) (?P<level>\w+) (?P<xabar>.+)")
for m in NAQSH.finditer(log):
    if m["level"] == "ERROR":
        print(f"[{m['vaqt']}] {m['xabar']}")
# [09:16] Xato 1
# [09:18] Xato 2
```

</details>

<details markdown="1">
<summary>Masala 19</summary>

```python
import re

def oshir(m: re.Match) -> str:
    return str(int(int(m.group()) * 1.1))

print(re.sub(r"\d+", oshir, "narx 100 va 200"))   # narx 110 va 220
```

</details>

<details markdown="1">
<summary>Masala 20</summary>

```python
import re

def parol_tekshir(p: str) -> list[str]:
    xatolar = []
    if len(p) < 8:
        xatolar.append("kamida 8 belgi")
    if not re.search(r"[A-Z]", p):
        xatolar.append("katta harf")
    if not re.search(r"[a-z]", p):
        xatolar.append("kichik harf")
    if not re.search(r"\d", p):
        xatolar.append("raqam")
    if not re.search(r"[!@#$%^&*]", p):
        xatolar.append("maxsus belgi")
    return xatolar

print(parol_tekshir("Aziz123!"))   # []
print(parol_tekshir("aziz"))
# ['kamida 8 belgi', 'katta harf', 'raqam', 'maxsus belgi']
```

</details>

---

[← Ma'lumotlar bazasi va SQL](./15-malumotlar-bazasi.md) | [Boshlovchilar README ↑](./README.md) | [Keyingi: OOP — ilg'or →](./17-oop-ilgor.md)
