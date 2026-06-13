# 23 — Settings, env va xavfsizlik

[⬅️ Oldingi: 22 — Testlash](./22-testing.md) · [🏠 README](./README.md) · [Keyingi: 24 — Deployment (production) ➡️](./24-deployment.md)

---

> **Bu bobda:** ilovangizni production'ga chiqarishdan oldin uni **xavfsiz** qilishni o'rganamiz. Avval **settings'ni bo'lish**ni ko'ramiz: bitta katta `settings.py` o'rniga `base.py` (umumiy) + `dev.py` (ishlab chiqish) + `prod.py` (production) paketini tuzamiz va `DJANGO_SETTINGS_MODULE` qaysi birini yuklashini boshqaramiz. Keyin eng muhim qoidaga o'tamiz: **maxfiy ma'lumotlar (secrets) kod ichida saqlanmaydi** — `SECRET_KEY`, parollar, API kalitlar **muhit o'zgaruvchilari** (environment variables) va `.env` fayl orqali keladi (`django-environ` qanday ishlashini tushunamiz va xuddi shunday qiluvchi oddiy yordamchini o'zimiz yozamiz). So'ng production uchun uchta hayotiy-muhim sozlamani sozlaymiz: `SECRET_KEY` (uzun, tasodifiy, maxfiy), `DEBUG=False` (xato sahifasi sirlarni oshkor qilmasligi uchun), `ALLOWED_HOSTS` (Host header hujumiga qarshi). Keyin **xavfsizlik qatlamlarini** bosib o'tamiz: HTTPS/HSTS (`SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`), xavfsiz cookie'lar (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`), **XSS** (Django'ning avtomatik escape'i), **clickjacking** (`X-Frame-Options`), **CSRF** va **CORS** farqi. Hammasini yakuniy qurol — **`manage.py check --deploy`** bilan tekshiramiz, u sizning sozlamalaringizdagi xavfsizlik teshiklarini ro'yxatlab beradi. Oxirida **keng tarqalgan xatolar**ni — DEBUG'ni yoqib qoldirish, secret'ni git'ga tushirish, ALLOWED_HOSTS'ni `["*"]` qilish — ko'rib chiqamiz. Bu bob Python'ni bilishni nazarda tutadi ([Python qo'llanma](../python/README.md)); maxfiy ma'lumotlarni git'dan chetlatish [Git qo'llanma](../git-github/README.md) bilan bog'liq; baza secret'lari [SQL qo'llanma](../sql/README.md) bilan. Hamma kod Django 6.0.6 (Python 3.14) da haqiqatan ishga tushirib tekshirilgan (baza uchun SQLite; HTTPS/gunicorn/nginx talab qiladigan bloklar **illustrativ** deb belgilangan).

---

## Nega bu bob alohida ahamiyatga ega?

Avvalgi boblarda biz "ishlaydigan" kod yozdik. Bu bobda biz **xavfsiz** kod yozamiz. Farqi katta: noto'g'ri sozlangan Django ilovasi mukammal ishlaydi — toki birov uni buzguncha.

Eng achchiq haqiqat: production'dagi xavfsizlik buzilishlarining ko'pchiligi murakkab hujumlardan emas, balki **oddiy konfiguratsiya xatolaridan** kelib chiqadi:

- `DEBUG = True` qoldirilgan — xato sahifasi `SECRET_KEY`'ni, baza parolini, fayl yo'llarini ko'rsatadi.
- `SECRET_KEY` to'g'ridan-to'g'ri `settings.py` ichida — git tarixiga tushgan, GitHub'da hamma ko'rgan.
- `ALLOWED_HOSTS = ["*"]` — Host header hujumiga ochiq.
- HTTPS yo'q — parollar ochiq matnda uzatiladi.

Yaxshi xabar: Django bularning hammasini oldindan ko'zda tutgan va sizga **tayyor himoya qatlamlari** beradi. Sizning vazifangiz — ularni **to'g'ri yoqish**. Bu bob aynan shu haqida.

> **Oltin qoida:** Ishlab chiqishda qulaylik uchun yoqilgan narsalar (`DEBUG=True`, ochiq xato sahifasi) production'da xavfli. Shuning uchun ikki muhitni **alohida sozlash** kerak. Undan boshlaymiz.

---

## Settings'ni bo'lish: base / dev / prod

Yangi loyihada bitta `config/settings.py` bo'ladi. Muammo: ishlab chiqishda `DEBUG=True`, production'da `DEBUG=False` kerak. Agar bitta faylda `if`'lar bilan boshqarsak, fayl chalkashadi va xato qilish oson bo'ladi.

Yechim — `settings.py` faylini **paket**ga (papkaga) aylantirish va uchta faylga bo'lish:

![Settings bo'lish](rasmlar/dj23-settings-bolish.svg)

- **`base.py`** — ikkala muhit uchun **bir xil** narsalar: `INSTALLED_APPS`, `MIDDLEWARE`, `TEMPLATES`, `AUTH_PASSWORD_VALIDATORS`.
- **`dev.py`** — `from .base import *` qiladi, keyin faqat ishlab chiqishga xos narsalarni o'zgartiradi (`DEBUG=True`).
- **`prod.py`** — xuddi shunday, lekin xavfsizlikni yoqadi (`DEBUG=False`, `SECURE_*`).

Tuzilma quyidagicha:

```bash
config/
    settings/
        __init__.py
        base.py
        dev.py
        prod.py
    urls.py
    wsgi.py
    asgi.py
```

### base.py — umumiy poydevor

`base.py` ichida muhitga bog'liq bo'lmagan hamma narsa. E'tibor bering: `BASE_DIR` endi **uch** marta `.parent` qiladi, chunki fayl bir qavat chuqurroqda (`config/settings/base.py`):

```python
# config/settings/base.py
"""Umumiy (dev/prod uchun bir xil) sozlamalar."""
from pathlib import Path

# config/settings/base.py -> uch qavat yuqoriga = loyiha ildizi
BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### dev.py — ishlab chiqish

`dev.py` `base`'dan hamma narsani oladi, keyin faqat dev'ga xos sozlamalarni qo'shadi:

```python
# config/settings/dev.py
"""Ishlab chiqish (development) sozlamalari."""
from .base import *  # noqa: F401,F403

DEBUG = True
SECRET_KEY = "django-insecure-dev-faqat-mahalliy"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Email'ni jo'natmaymiz, konsolga chiqaramiz
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

`# noqa` — bu linter'ga "`import *` haqida ogohlantirma" deyish; bu yerda `import *` ataylab, chunki `base`'dagi hamma sozlamani olib kelyapmiz.

### prod.py — production

`prod.py` xavfsizlikni yoqadi. Maxfiy qiymatlar (`SECRET_KEY`) bu yerda **yozilmaydi** — keyingi bo'limda ko'radigan muhit o'zgaruvchilaridan keladi:

```python
# config/settings/prod.py
"""Production sozlamalari — xavfsizlik yoqilgan."""
from .base import *  # noqa: F401,F403

DEBUG = False

# HTTPS va xavfsizlik (keyingi bo'limlarda tushuntiriladi)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 yil
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Qaysi settings yuklanadi? — DJANGO_SETTINGS_MODULE

Django qaysi sozlama faylini ishlatishni `DJANGO_SETTINGS_MODULE` muhit o'zgaruvchisidan biladi. `manage.py`, `wsgi.py` va `asgi.py` uni o'rnatadi. Standartni `dev`'ga qo'yamiz:

```python
# manage.py (faqat o'zgargan qator)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
```

```python
# config/wsgi.py va config/asgi.py da ham xuddi shunday
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
```

`setdefault` — agar muhitda allaqachon o'rnatilgan bo'lsa, ustidan yozmaydi. Demak production serverda `DJANGO_SETTINGS_MODULE=config.settings.prod` qo'yib, kodga tegmasdan prod'ga o'tasiz:

```bash
# ishlab chiqish (default dev):
python manage.py runserver

# production sozlamalar bilan tekshirish:
# Linux/macOS:
DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py check

# Windows PowerShell:
$env:DJANGO_SETTINGS_MODULE="config.settings.prod"; python manage.py check
```

Yoki har safar yozmaslik uchun `--settings` flagidan foydalaning:

```bash
python manage.py check --settings=config.settings.prod
```

Bu tuzilma haqiqatan ishlaganini tasdiqlash uchun `check` ikkala muhitda ham ishlatildi: `dev`'da `System check identified no issues`, `prod`'da esa (kerakli muhit o'zgaruvchilari berilgach) yana `no issues`.

---

## Maxfiy ma'lumotlar: muhit o'zgaruvchilari va .env

Endi eng muhim qoida. **Maxfiy ma'lumotlar kod ichida bo'lmasligi kerak.** Buni nima deymiz: `SECRET_KEY`, baza paroli, API kalitlar, tashqi servis tokenlari.

Nega? Chunki kod **git**'ga tushadi. Agar secret kodda bo'lsa:

- U git **tarixiga** tushadi — keyin o'chirsangiz ham, eski commitlarda qoladi.
- Repozitoriy hamkasblar, CI serverlar, ehtimol GitHub'da hammaga ko'rinadi.
- Secret'ni almashtirish endi qiyin: butun jamoa, hamma deploy yangilanishi kerak.

Yechim — secret'lar **muhit o'zgaruvchilari**dan (environment variables) o'qiladi. Kod faqat "shu nomli o'zgaruvchini ber" deydi, qiymatning o'zi koddan tashqarida:

![Maxfiy ma'lumotlar oqimi](rasmlar/dj23-env-secrets.svg)

### .env fayl nima va django-environ qanday ishlaydi

Mahalliy ishlab chiqishda har safar muhit o'zgaruvchilarini qo'lda eksport qilish zerikarli. Shuning uchun ularni `.env` deb nomlangan oddiy faylga yozamiz:

```bash
# .env  — bu fayl GIT'GA TUSHMASLIGI kerak!
DJANGO_SECRET_KEY=fayldan-kelgan-juda-uzun-tasodifiy-maxfiy-kalit
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.com,api.example.com
DATABASE_URL=postgres://user:pass@localhost:5432/mydb
```

Mashhur `django-environ` kutubxonasi shu faylni o'qib, qiymatlarni `os.environ`'ga yuklaydi va qulay konvertorlar beradi (`env.bool`, `env.list`, `env.db`). Uning **tushunchasi** quyidagicha (haqiqiy `django-environ` kodi):

```python
# django-environ uslubi (ILLUSTRATIV - kutubxona o'rnatilishi kerak)
import environ

env = environ.Env(
    DEBUG=(bool, False),  # (tur, default)
)
environ.Env.read_env(BASE_DIR / ".env")  # .env ni o'qib os.environ'ga yuklaydi

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")  # avtomatik bool'ga aylantiriladi
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
```

### O'zimiz yozamiz: tashqi kutubxonasiz env o'qish

`django-environ` ichida sehr yo'q — u shunchaki `.env`'ni o'qib, satrlarni kerakli turga aylantiradi. Buni o'zimiz ham qila olamiz (hech narsa o'rnatmasdan). Quyidagi kod **haqiqatan ishlaydi** va `base.py` uchun mos:

```python
# config/settings/base.py (yuqoriga qo'shiladi)
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def load_env(path):
    """.env faylini o'qib, qiymatlarni os.environ'ga yuklaydi.

    Mavjud muhit o'zgaruvchisini ustidan yozmaydi (setdefault mantiqi).
    """
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def env(key, default=None):
    """Muhit o'zgaruvchisini satr sifatida o'qiydi."""
    return os.environ.get(key, default)


def env_bool(key, default=False):
    """'True'/'1'/'yes'/'on' -> True; aks holda False."""
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def env_list(key, default=None):
    """Vergul bilan ajratilgan satrni ro'yxatga aylantiradi."""
    val = os.environ.get(key)
    if not val:
        return default or []
    return [item.strip() for item in val.split(",") if item.strip()]


# .env faylni yuklaymiz (production'da fayl bo'lmasligi mumkin - muammo emas)
load_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-faqat-mahalliy-uchun-xavfsiz-emas")
DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", [])
```

Bu yordamchilar haqiqatan tekshirildi — `.env` faylidan `DJANGO_DEBUG=True`, `DJANGO_ALLOWED_HOSTS=example.com,api.example.com` va `DATABASE_URL=...` to'g'ri o'qildi (izoh qatorlari `#` va bo'sh satrlar e'tiborga olinmadi).

### Production'da .env yo'q

Muhim nuance: `.env` fayl faqat **mahalliy qulaylik** uchun. Production serverda ko'pincha `.env` fayl **bo'lmaydi** — server boshqaruv paneli (Heroku, Railway, systemd, Docker, CI/CD) muhit o'zgaruvchilarini **to'g'ridan-to'g'ri** beradi. Kodimiz ikkalasida ham ishlaydi, chunki u faqat `os.environ`'dan o'qiydi; `.env` shunchaki o'sha `os.environ`'ni to'ldirishning bir usuli.

### .env ni git'dan chetlatish

Bu hayotiy-muhim qadam. `.gitignore`'ga qo'shing:

```bash
# .gitignore
.env
*.env
db.sqlite3
__pycache__/
```

Va jamoaga namuna sifatida `.env.example` (maxfiy **qiymatlarsiz**) qoldiring — bu git'ga **tushadi**:

```bash
# .env.example  (bu git'ga tushadi - faqat tuzilma, qiymat yo'q)
DJANGO_SECRET_KEY=
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=
DATABASE_URL=
```

> Git'da secret'larni boshqarish bo'yicha batafsil: [Git va GitHub qo'llanma](../git-github/README.md).

---

## SECRET_KEY: uzun, tasodifiy, maxfiy

`SECRET_KEY` — Django'ning kriptografik imzolar uchun ishlatadigan asosiy kaliti. U bilan:

- Sessiya ma'lumotlari imzolanadi (cookie ichidagi `sessionid`).
- CSRF tokenlar yaratiladi.
- Parolni tiklash linklari imzolanadi.
- `signing` moduli (xavfsiz tokenlar) ishlaydi.

Agar hujumchi `SECRET_KEY`'ni bilsa, u soxta sessiya yarata oladi (boshqa foydalanuvchi sifatida kira oladi), CSRF himoyasini chetlab o'ta oladi. Shuning uchun u **uzun, tasodifiy va maxfiy** bo'lishi shart.

### Yangi kalit yaratish

Django'da tayyor funksiya bor — u 50 belgili tasodifiy kalit beradi:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Tekshirildi: bu buyruq aynan **50 belgili** kalit chiqaradi (masalan `=21+jen*5mc_3(8rn-0q...`). Bu qiymatni `.env` faylga (yoki server muhit o'zgaruvchisiga) yozasiz, **koddagi joyga emas**.

### Xato va to'g'ri yondashuv

```python
# config/settings/prod.py

# XATO - kalit kodda, git'ga tushadi, hammaga ko'rinadi
SECRET_KEY = "django-insecure-z(l4kt2$hi7g%oj2=4l$%8mxe2hq=ruj^02l_nbb6x4iew-4qc"  # noqa

# TO'G'RI - muhit o'zgaruvchisidan
SECRET_KEY = env("DJANGO_SECRET_KEY")
```

Production'da `SECRET_KEY` **majburiy** bo'lishi kerak — agar o'rnatilmagan bo'lsa, ilova umuman ishga tushmasligi kerak (jim turib default ishlatishdan ko'ra, baland ovozda yiqilgani yaxshi):

```python
# config/settings/prod.py
from django.core.exceptions import ImproperlyConfigured


def env_required(key):
    """Production'da majburiy o'zgaruvchi: yo'q bo'lsa darhol xato."""
    try:
        import os
        return os.environ[key]
    except KeyError:
        raise ImproperlyConfigured(f"Muhit o'zgaruvchisi o'rnatilmagan: {key}")


SECRET_KEY = env_required("DJANGO_SECRET_KEY")
```

Tekshirildi: `env_required("YOQ_OZGARUVCHI")` aniq `ImproperlyConfigured: Muhit o'zgaruvchisi o'rnatilmagan: YOQ_OZGARUVCHI` xatosini berdi; mavjud o'zgaruvchida esa qiymatni qaytardi.

> **Maslahat:** kalit oshkor bo'lib qolsa (masalan, xato bilan git'ga tushib ketdi) — uni **darhol almashtiring**. Eski kalit bilan imzolangan hamma sessiya va token bekor bo'ladi (foydalanuvchilar qayta kiradi), lekin bu xavfsizlik uchun arzon narx.

---

## DEBUG=False: production'da majburiy

`DEBUG=True` ishlab chiqishda ajoyib: xato yuz berganda Django to'liq batafsil sahifani ko'rsatadi — traceback, lokal o'zgaruvchilar, sozlamalar, SQL so'rovlar. Bu **debug** qilishni osonlashtiradi.

Aynan shu sabab production'da u **xavfli**. O'sha batafsil xato sahifasi quyidagilarni **hujumchiga ko'rsatadi**:

- `SECRET_KEY` (sozlamalar bo'limida).
- Baza ulanish ma'lumotlari (parol bundan mustasno emas).
- Fayl yo'llari, kutubxona versiyalari, server tuzilishi.
- Lokal o'zgaruvchilardagi maxfiy qiymatlar.

Shuning uchun production'da **doimo**:

```python
# config/settings/prod.py
DEBUG = False
```

`DEBUG=False` bo'lganda Django xato sahifasi o'rniga oddiy "Server Error (500)" sahifasini ko'rsatadi (siz uni `500.html` template bilan moslashtirishingiz mumkin). Batafsil xato esa logga yoziladi — foydalanuvchiga emas.

> **Muhim juftlik:** `DEBUG=False` qilganingizda, `ALLOWED_HOSTS` ham to'ldirilishi **shart** (keyingi bo'lim) — aks holda Django umuman so'rov qabul qilmaydi.

`DEBUG=False` bilan yana bir nuance: statik fayllar endi Django tomonidan xizmat qilinmaydi (`runserver` ham). Production'da `collectstatic` + nginx/WhiteNoise kerak — bu [keyingi bobning](./24-deployment.md) mavzusi.

---

## ALLOWED_HOSTS: Host header hujumiga qarshi

`ALLOWED_HOSTS` — sizning saytingiz **qaysi domen nomlari** orqali xizmat qilishini Django'ga aytadigan ro'yxat. Brauzer har so'rovda `Host:` headerini yuboradi (`Host: example.com`). Django kelgan `Host`'ni shu ro'yxat bilan solishtiradi:

- Ro'yxatdagi domen bo'lsa — so'rov qabul qilinadi.
- Notanish domen bo'lsa — **400 Bad Request** qaytaradi, view'ga umuman bormaydi.

Nega bu kerak? **Host header hujumi** uchun. Agar Django istalgan `Host`'ni qabul qilsa, hujumchi soxta `Host` yuborib, masalan parolni tiklash linkini o'z saytiga yo'naltira oladi (chunki Django ba'zi linklarni `request.get_host()`'dan quradi). Demak `ALLOWED_HOSTS` — bu "men faqat shu domenlar uchun ishlayman" degan kafolat.

```python
# config/settings/prod.py
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", [])
# .env: DJANGO_ALLOWED_HOSTS=example.com,www.example.com
```

Bu xulq haqiqatan tekshirildi. `ALLOWED_HOSTS=["example.com"]` va `DEBUG=False` bo'lganda:

```python
# tekshiruv natijasi (Django test Client orqali):
client.get("/", HTTP_HOST="yovuz-sayt.com")  # -> status 400 (rad etildi)
client.get("/", HTTP_HOST="example.com")     # -> status 200 (qabul qilindi)
```

### ❌ Eng tarqalgan xato: ALLOWED_HOSTS = ["*"]

```python
# ❌ XATO - hamma domenni qabul qiladi, Host header himoyasi o'chadi
ALLOWED_HOSTS = ["*"]
```

Bu "400 xatoni tezda yo'qotaman" deb qilinadi, lekin u himoyani **butunlay o'chiradi**. To'g'ri yo'l — aniq domenlarni sanab chiqish. Agar domen oldindan noma'lum bo'lsa (masalan, ko'p subdomenli SaaS), aniq subdomen naqshlarini yozing: `[".example.com"]` (boshidagi nuqta — barcha subdomenlar).

> **DEBUG=True nuance:** ishlab chiqishda `DEBUG=True` bo'lsa va `ALLOWED_HOSTS` bo'sh bo'lsa, Django avtomatik `localhost`, `127.0.0.1` va `[::1]`'ni qabul qiladi. Shuning uchun dev'da bu sozlama bilan kamdan-kam yuzma-yuz kelasiz — muammo aynan prod'da chiqadi.

---

## Xavfsizlik qatlamlari: HTTPS, HSTS va xavfsiz cookie'lar

Endi production xavfsizligining yuragi. Django'ning `SecurityMiddleware`'i bir nechta himoyani boshqaradi — siz faqat sozlamalarni yoqasiz.

![Xavfsizlik qatlamlari](rasmlar/dj23-xavfsizlik-qatlamlari.svg)

### HTTPS ga majburlash

HTTP — ochiq matn. Parol, cookie, hamma narsa tarmoqda o'qilishi mumkin. HTTPS (TLS) buni shifrlaydi. Production'da **doimo HTTPS** ishlatiladi.

```python
# config/settings/prod.py
# HTTP bilan kelgan so'rovni avtomatik HTTPS'ga (https://...) yo'naltiradi
SECURE_SSL_REDIRECT = True
```

Agar Django reverse-proxy (nginx) ortida tursa, proxy HTTPS'ni "tugatadi" va Django'ga HTTP yuboradi. Django HTTPS ekanini bilishi uchun proxy header'iga ishonadi:

```python
# config/settings/prod.py - ILLUSTRATIV: nginx/proxy shu headerni qo'yishi kerak
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

> Bu sozlamani faqat proxy haqiqatan `X-Forwarded-Proto`'ni o'rnatishiga **ishonchingiz komil bo'lsa** yoqing — aks holda hujumchi soxta header yuborib aldashi mumkin.

### HSTS: brauzerga "doimo HTTPS" deyish

HSTS (HTTP Strict Transport Security) — brauzerga "shu saytga endi faqat HTTPS bilan kel, hatto manzilni `http://` bilan tersam ham" deydigan header. Bu birinchi so'rovdagi "downgrade" hujumini oldini oladi.

```python
# config/settings/prod.py
SECURE_HSTS_SECONDS = 31536000          # 1 yil davomida eslab qol
SECURE_HSTS_INCLUDE_SUBDOMAINS = True   # subdomenlarga ham tatbiq et
SECURE_HSTS_PRELOAD = True              # brauzer preload ro'yxatiga kirish uchun
```

> **Ehtiyot bo'ling:** HSTS qaytarib bo'lmaydigan ta'sirga ega — agar `includeSubDomains` yoqib, keyin biror subdomen faqat HTTP bilan ishlasa, u brauzerlarda yetib bo'lmas holga keladi (HSTS muddati tugaguncha). Avval kichik `SECURE_HSTS_SECONDS` (masalan 3600) bilan sinab ko'ring, ishonch hosil qilgach oshiring.

### Xavfsiz cookie'lar

Sessiya va CSRF cookie'lari faqat HTTPS orqali yuborilishini ta'minlang — aks holda HTTP'da ular o'g'irlanishi mumkin:

```python
# config/settings/prod.py
SESSION_COOKIE_SECURE = True   # sessionid cookie faqat HTTPS'da
CSRF_COOKIE_SECURE = True      # csrftoken cookie faqat HTTPS'da
SECURE_CONTENT_TYPE_NOSNIFF = True  # X-Content-Type-Options: nosniff
```

`SECURE_CONTENT_TYPE_NOSNIFF=True` — brauzerga "Content-Type'ni o'zing taxmin qilma, men aytganini ishlat" deydi (MIME-sniffing hujumini oldini oladi). Tekshirildi: bu yoqilganda javobda `X-Content-Type-Options: nosniff` headeri paydo bo'ldi.

Hamma bularning to'g'riligi tasdiqlandi: `prod` sozlamalar bilan, kerakli muhit o'zgaruvchilari berilgach (`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_DEBUG=False`), `python manage.py check --deploy` aynan `System check identified no issues` natijasini berdi.

---

## XSS, clickjacking, CSRF va CORS

Bu to'rtta atama tez-tez chalkashtiriladi. Har birini ajratamiz — Django ko'pchiligini avtomatik himoya qiladi.

### XSS — Cross-Site Scripting

XSS — hujumchi sizning sahifangizga zararli JavaScript kiritishi (masalan, izoh maydoni orqali `<script>...</script>` yuborib). Django shablon tizimi buni **avtomatik** himoya qiladi: template'da chiqarilgan har qanday o'zgaruvchi **autoescape** qilinadi — `<`, `>`, `&`, `"`, `'` belgilari HTML-entity'ga aylanadi:

```html
<!-- template: foydalanuvchi izohi xavfsiz chiqariladi -->
<p>{{ izoh }}</p>
<!-- agar izoh = "<script>alert(1)</script>" bo'lsa, brauzer
     uni kod sifatida emas, MATN sifatida ko'rsatadi:
     &lt;script&gt;alert(1)&lt;/script&gt; -->
```

Autoescape'ni faqat ishonchli HTML uchun, ataylab `|safe` filtri bilan o'chirasiz — va bu yerda ehtiyot bo'ling:

```html
<!-- ❌ XAVFLI: agar matn foydalanuvchidan kelsa, XSS teshigi ochiladi -->
<p>{{ foydalanuvchi_matni|safe }}</p>
```

Autoescape mexanizmi avvalroq batafsil ko'rilgan ([04-bob, Template tizimi](./04-template-tizimi.md)).

### Clickjacking — X-Frame-Options

Clickjacking — hujumchi sizning saytingizni ko'rinmas `<iframe>` ichiga joylab, foydalanuvchini "boshqa narsani bosaman" deb aldab, aslida sizning saytingizdagi tugmani bostirishi. Django `XFrameOptionsMiddleware` bilan buni to'sadi — har javobga `X-Frame-Options: DENY` headerini qo'yadi (sahifa hech qanday frame ichida ko'rsatilmaydi):

```python
# base.py MIDDLEWARE ichida allaqachon bor:
# "django.middleware.clickjacking.XFrameOptionsMiddleware"
# Default: DENY. Agar o'z saytingiz frame'iga ruxsat kerak bo'lsa:
X_FRAME_OPTIONS = "SAMEORIGIN"
```

Tekshirildi: oddiy view'ga so'rov yuborilganda javobda `X-Frame-Options: DENY` headeri haqiqatan mavjud edi.

### CSRF — Cross-Site Request Forgery

CSRF — hujumchi boshqa saytdan foydalanuvchi nomidan sizning saytingizga **yashirin POST** yuborishi (masalan, "pul o'tkaz" formasini). Django `CsrfViewMiddleware` bilan himoya qiladi: har bir o'zgartiruvchi so'rov (POST/PUT/DELETE) yashirin **CSRF token** olib kelishi shart. Token yo'q bo'lsa — **403 Forbidden**:

```html
<!-- formada token shart -->
<form method="post">
    {% csrf_token %}
    <input name="nom">
    <button>Yuborish</button>
</form>
```

Tekshirildi (CSRF tekshiruvi yoqilgan test Client bilan):

```python
# POST token'siz -> 403 Forbidden
client.post("/forma/", {"nom": "Ali"})  # -> status 403
# GET xavfsiz, tekshirilmaydi -> 200
client.get("/forma/")                   # -> status 200
```

DRF API'larida JWT/Token auth ishlatilsa, CSRF odatda ta'sir qilmaydi (token header'da keladi, cookie'da emas) — bu [17-bobda](./17-drf-auth.md) ko'rilgan.

### CORS — Cross-Origin Resource Sharing

CORS — CSRF **emas**, ko'pincha shu bilan chalkashtiriladi. CORS — brauzerning qoidasi: boshqa **origin**dagi (boshqa domen/port) JavaScript sizning API'ngizga so'rov yubora oladimi yo'qmi. Buni server **ruxsat berish** uchun ishlatadi (masalan, `app.example.com` frontendi `api.example.com` backendiga murojaat qilishi uchun).

Django'da CORS o'rnatilgan **emas** — `django-cors-headers` kutubxonasi ishlatiladi:

```python
# ILLUSTRATIV: pip install django-cors-headers kerak
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE  # eng yuqorida

CORS_ALLOWED_ORIGINS = [
    "https://app.example.com",
]
```

Qisqacha farq:

- **CSRF** — *sizning* saytingizdan kelgan yashirin so'rovlarni soxtalashtirishdan himoya (server tomonida token).
- **CORS** — *boshqa* origin'dan kelgan brauzer-so'rovlariga **ruxsat berish** mexanizmi (server ruxsat headerini qo'yadi).
- **CSRF Trusted Origins** — bu uchinchisi: `DEBUG=False` va HTTPS'da, boshqa subdomendan POST qilinganda CSRF'ni qabul qilish uchun:

```python
# config/settings/prod.py
CSRF_TRUSTED_ORIGINS = ["https://www.example.com", "https://app.example.com"]
```

---

## manage.py check --deploy: yakuniy tekshiruv

Django'da production'ga chiqishdan oldin ishlatadigan tayyor xavfsizlik tekshiruvi bor:

```bash
python manage.py check --deploy
```

U sizning sozlamalaringizni skanerlaydi va **xavfsizlik ogohlantirishlari** ro'yxatini beradi. Har bir ogohlantirishning kodi (`security.W00X`) bor.

`dev` sozlamalar bilan ishga tushirsangiz (DEBUG=True, secret kodda), aynan quyidagi ogohlantirishlar chiqadi (haqiqiy natija):

```bash
System check identified some issues:

WARNINGS:
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting...
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True...
?: (security.W009) Your SECRET_KEY has less than 50 characters... or it's prefixed with 'django-insecure-'...
?: (security.W012) SESSION_COOKIE_SECURE is not set to True...
?: (security.W016) ... you have not set CSRF_COOKIE_SECURE to True...
?: (security.W018) You should not have DEBUG set to True in deployment.

System check identified 6 issues (0 silenced).
```

Bu ro'yxat aynan biz bu bobda yoqgan sozlamalarga mos keladi. Endi `prod` sozlamalar bilan, to'g'ri muhit o'zgaruvchilari berib ishlatamiz:

```bash
# Linux/macOS:
DJANGO_SETTINGS_MODULE=config.settings.prod \
DJANGO_SECRET_KEY="haqiqiy-uzun-tasodifiy-50-belgili-kalit-..." \
DJANGO_DEBUG=False \
DJANGO_ALLOWED_HOSTS="example.com,www.example.com" \
python manage.py check --deploy
```

```bash
# Windows PowerShell:
$env:DJANGO_SETTINGS_MODULE="config.settings.prod"
$env:DJANGO_SECRET_KEY="haqiqiy-uzun-tasodifiy-50-belgili-kalit-..."
$env:DJANGO_DEBUG="False"
$env:DJANGO_ALLOWED_HOSTS="example.com,www.example.com"
python manage.py check --deploy
```

Natija (tekshirildi):

```bash
System check identified no issues (0 silenced).
```

> **CI/CD'ga qo'shing:** `check --deploy`'ni deploy quvuringizning bir qadami qiling — agar yangi ogohlantirish chiqsa, deploy to'xtasin. Bu xavfsizlik regressiyalarini avtomatik ushlaydi. [Git/CI qo'llanma](../git-github/README.md).

---

## Keng tarqalgan xatolar

Yangi (va tajribali) dasturchilar tushadigan tuzoqlar — har birini ataylab xato (❌) va to'g'ri (✅) variant bilan ko'rsatamiz.

**1. DEBUG'ni production'da yoqib qoldirish.**

```python
# ❌ Eng xavfli xato - xato sahifasi SECRET_KEY va baza parolini ko'rsatadi
DEBUG = True

# ✅ Muhit o'zgaruvchisiga bog'lang, default False
DEBUG = env_bool("DJANGO_DEBUG", False)
```

**2. SECRET_KEY'ni kodga yozish.**

```python
# ❌ git tarixiga abadiy tushadi
SECRET_KEY = "django-insecure-..."

# ✅ muhitdan, production'da majburiy
SECRET_KEY = env_required("DJANGO_SECRET_KEY")
```

**3. ALLOWED_HOSTS = ["*"]** — Host header himoyasini o'chiradi (yuqorida ko'rilgan). Aniq domenlarni sanang.

**4. .env'ni git'ga qo'shib qo'yish.** Eng birinchi commitdan oldin `.gitignore`'ga `.env` qo'shing. Agar allaqachon tushib ketgan bo'lsa — secret'ni almashtiring (faqat git'dan o'chirish yetarli emas, tarixda qoladi).

**5. Settings'ni `import` bilan emas, nusxa bilan bo'lish.**

```python
# ❌ prod.py base.py ni nusxaladi - base o'zgarsa, prod eskirib qoladi
# (butun INSTALLED_APPS, MIDDLEWARE qayta yozilgan)

# ✅ from .base import * - bitta manba haqiqati
from .base import *  # noqa
```

**6. `CSRF_TRUSTED_ORIGINS`'siz subdomenlar aro POST.** `DEBUG=False`'da boshqa subdomendan forma yuborilsa CSRF 403 beradi — kerakli origin'larni `CSRF_TRUSTED_ORIGINS`'ga qo'shing.

**7. `SECURE_PROXY_SSL_HEADER`'ni proxy ishonchsiz holda yoqish** — agar proxy `X-Forwarded-Proto`'ni majburan o'rnatmasa, hujumchi soxta header bilan Django'ni "HTTPS" deb aldashi mumkin.

**8. `check --deploy`'ni unutish.** Deploy'dan oldin doimo ishlating — u yuqoridagi ko'p xatolarni avtomatik aytib beradi.

> **Solishtirma:** Node.js'da maxfiy ma'lumotlar odatda `dotenv` paketi va `process.env` orqali boshqariladi — Django'dagi `.env` + `os.environ` g'oyasi aynan o'sha ([Node.js qo'llanma](../nodejs/README.md)). Asosiy farq: Django sizga `check --deploy` kabi tayyor xavfsizlik auditi va `SECURE_*` sozlamalarini bir joyda beradi.

---

## Mashqlar

### Oson

1. Yangi loyihada `config/settings.py` faylini `config/settings/` paketiga aylantiring: `__init__.py`, `base.py`, `dev.py`, `prod.py` yarating. `manage.py`'da `DJANGO_SETTINGS_MODULE`'ni `config.settings.dev` ga o'zgartiring.

2. `python -c` buyrug'i bilan yangi `SECRET_KEY` yarating va uning uzunligi 50 ekanini tasdiqlang.

3. `dev.py`'da `DEBUG=True`, `ALLOWED_HOSTS=["localhost", "127.0.0.1"]` qiling. `python manage.py check` ishlashini tekshiring.

4. `.gitignore` fayl yarating va unga `.env`, `db.sqlite3`, `__pycache__/` qatorlarini qo'shing.

5. `env_bool` funksiyasini yozing: `"True"`, `"1"`, `"yes"`, `"on"` (registrga befarq) uchun `True`, qolganlari uchun `False` qaytarsin. Uni `DJANGO_DEBUG` o'zgaruvchisida sinab ko'ring.

6. `dev` sozlamalar bilan `python manage.py check --deploy` ishlating va chiqqan ogohlantirishlar kodlarini (W004, W008, ...) sanang.

### O'rta

7. `env`, `env_bool`, `env_list` yordamchilarini `base.py`'da yozing. `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`'ni muhit o'zgaruvchilaridan o'qing (default'lar bilan).

8. `load_env(path)` funksiyasini yozing: `.env` faylini o'qib, izoh (`#`) va bo'sh qatorlarni o'tkazib yuborib, qolganlarini `os.environ`'ga `setdefault` bilan yuklasin.

9. `prod.py` yozing: `DEBUG=False`, hamma `SECURE_*` (SSL_REDIRECT, HSTS, cookie secure, nosniff) yoqilgan. To'g'ri muhit o'zgaruvchilari bilan `check --deploy` "no issues" berishini tasdiqlang.

10. `env_required(key)` yozing: o'zgaruvchi yo'q bo'lsa `ImproperlyConfigured` ko'tarsin. `prod.py`'da `SECRET_KEY = env_required("DJANGO_SECRET_KEY")` qiling va o'zgaruvchisiz ishga tushirib, xato chiqishini ko'ring.

11. `pytest-django` bilan test yozing: `ALLOWED_HOSTS=["example.com"]`, `DEBUG=False` da notanish `Host` bilan so'rov 400, tanish `Host` bilan 200 qaytarishini `@override_settings` orqali tekshiring.

12. Test yozing: `X-Frame-Options` headeri javobda `DENY` ekanini va `SECURE_CONTENT_TYPE_NOSNIFF=True`'da `X-Content-Type-Options: nosniff` paydo bo'lishini tasdiqlang.

### Qiyin

13. CSRF testini yozing: `Client(enforce_csrf_checks=True)` bilan `@csrf_protect` view'ga token'siz POST yuborib **403** olganingizni, GET'da esa **200** olganingizni tasdiqlang.

14. Uchta muhit qo'shing (`dev`, `staging`, `prod`) va `DJANGO_SETTINGS_MODULE`'ni `--settings` flagi orqali almashtirib, har birida `check` ishlashini ko'rsating. `staging`'da `DEBUG=False` lekin batafsilroq logging bo'lsin.

15. `prod.py`'ni shunday yozingki, `ALLOWED_HOSTS` bo'sh bo'lsa import vaqtidayoq `RuntimeError` ko'tarsin (jim ishlab ketmasin). Bo'sh va to'ldirilgan holatlarda xulqni tekshiring.

---

<details markdown="1"><summary>Yechimlar</summary>

**1.**
```bash
# settings.py o'rniga paket:
mkdir config/settings
# settings.py mazmunini base.py'ga ko'chiring, keyin o'chiring
# yangi fayllar: __init__.py (bo'sh), base.py, dev.py, prod.py
```
```python
# manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
# wsgi.py va asgi.py'da ham xuddi shunday
```

**2.**
```bash
python -c "from django.core.management.utils import get_random_secret_key; k=get_random_secret_key(); print(len(k), k)"
# Natija: 50 va tasodifiy kalit (masalan =21+jen*5mc_3...)
```

**3.**
```python
# config/settings/dev.py
from .base import *  # noqa

DEBUG = True
SECRET_KEY = "django-insecure-dev-faqat-mahalliy"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```
```bash
python manage.py check
# System check identified no issues (0 silenced).
```

**4.**
```bash
# .gitignore
.env
*.env
db.sqlite3
__pycache__/
*.pyc
staticfiles/
```

**5.**
```python
def env_bool(key, default=False):
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")

# sinov:
os.environ["DJANGO_DEBUG"] = "True"
assert env_bool("DJANGO_DEBUG") is True
os.environ["DJANGO_DEBUG"] = "0"
assert env_bool("DJANGO_DEBUG") is False
```

**6.**
```bash
python manage.py check --deploy
# WARNINGS: W004 (HSTS), W008 (SSL_REDIRECT), W009 (SECRET_KEY),
#           W012 (SESSION_COOKIE_SECURE), W016 (CSRF_COOKIE_SECURE), W018 (DEBUG)
# Jami: 6 issue
```

**7.**
```python
# config/settings/base.py
import os

def env(key, default=None):
    return os.environ.get(key, default)

def env_bool(key, default=False):
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")

def env_list(key, default=None):
    val = os.environ.get(key)
    if not val:
        return default or []
    return [x.strip() for x in val.split(",") if x.strip()]

SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-xavfsiz-emas")
DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", [])
```

**8.**
```python
from pathlib import Path

def load_env(path):
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())

load_env(BASE_DIR / ".env")
```

**9.**
```python
# config/settings/prod.py
from .base import *  # noqa

DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```
```bash
DJANGO_SETTINGS_MODULE=config.settings.prod \
DJANGO_SECRET_KEY="uzun-50-belgili-tasodifiy-kalit-..." \
DJANGO_ALLOWED_HOSTS="example.com" \
python manage.py check --deploy
# System check identified no issues (0 silenced).
```

**10.**
```python
import os
from django.core.exceptions import ImproperlyConfigured

def env_required(key):
    try:
        return os.environ[key]
    except KeyError:
        raise ImproperlyConfigured(f"Muhit o'zgaruvchisi o'rnatilmagan: {key}")

# prod.py:
SECRET_KEY = env_required("DJANGO_SECRET_KEY")
# o'zgaruvchisiz: ImproperlyConfigured: Muhit o'zgaruvchisi o'rnatilmagan: DJANGO_SECRET_KEY
```

**11.**
```python
# test_security.py
from django.test import override_settings

@override_settings(ALLOWED_HOSTS=["example.com"], DEBUG=False)
def test_allowed_hosts_blocks_unknown(client):
    r = client.get("/", HTTP_HOST="yovuz.com")
    assert r.status_code == 400

@override_settings(ALLOWED_HOSTS=["example.com"], DEBUG=False)
def test_allowed_hosts_accepts_known(client):
    r = client.get("/", HTTP_HOST="example.com")
    assert r.status_code == 200
```
```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.dev
python_files = test_*.py
```

**12.**
```python
def test_clickjacking_header(client):
    r = client.get("/", HTTP_HOST="localhost")
    assert r.status_code == 200
    assert r.headers["X-Frame-Options"] == "DENY"

@override_settings(SECURE_CONTENT_TYPE_NOSNIFF=True)
def test_nosniff_header(client):
    r = client.get("/", HTTP_HOST="localhost")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
```

**13.**
```python
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

@csrf_protect
def forma(request):
    if request.method == "POST":
        return HttpResponse("Qabul qilindi")
    return HttpResponse("Forma")

# test:
def test_csrf_blocks_post_without_token():
    from django.test import Client
    c = Client(enforce_csrf_checks=True)
    r = c.post("/forma/", {"nom": "Ali"}, HTTP_HOST="localhost")
    assert r.status_code == 403

def test_get_is_safe():
    from django.test import Client
    c = Client(enforce_csrf_checks=True)
    r = c.get("/forma/", HTTP_HOST="localhost")
    assert r.status_code == 200
```

**14.**
```python
# config/settings/staging.py
from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", ["staging.example.com"])
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "DEBUG"},  # batafsilroq
}
```
```bash
python manage.py check --settings=config.settings.dev
python manage.py check --settings=config.settings.staging
# prod.py SECRET_KEY ni env'dan majburiy oladi (env_required), shuning uchun
# DJANGO_SECRET_KEY ham beriladi — aks holda ImproperlyConfigured yiqiladi:
DJANGO_SECRET_KEY="uzun-50-belgili-tasodifiy-kalit-..." \
DJANGO_ALLOWED_HOSTS=example.com \
python manage.py check --settings=config.settings.prod
```

**15.**
```python
# config/settings/prod.py
from .base import *  # noqa

DEBUG = False
if not ALLOWED_HOSTS:
    raise RuntimeError("Production'da DJANGO_ALLOWED_HOSTS bo'sh bo'lmasligi kerak!")

# Tekshirildi:
# - bo'sh: RuntimeError ko'tariladi (import vaqtidayoq, ilova ishga tushmaydi)
# - DJANGO_ALLOWED_HOSTS="example.com": muammosiz yuklanadi
```

</details>

---

[⬅️ Oldingi: 22 — Testlash](./22-testing.md) · [🏠 README](./README.md) · [Keyingi: 24 — Deployment (production) ➡️](./24-deployment.md)
