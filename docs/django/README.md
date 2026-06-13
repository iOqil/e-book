# Django — 0 dan Expertgacha

Bu kitob **Python asoslarini biladigan** o'quvchini Django bo'yicha noldan ishonchli full-stack veb-dasturchi darajasiga olib chiqadi. Birinchi `urls.py`/`views.py` dan boshlab — template tizimi, modellar va ORM, admin panel, formalar, class-based views, autentifikatsiya, **Django REST Framework (DRF)** bilan to'liq REST API, signallar, keshlash, async va Celery, testlash, xavfsizlik va production deploy orqali — yakuniy kapston loyihaga qadar. Har bir mavzu sodda tushuntirish, **Django 6.0.6 da haqiqiy ishga tushirib tekshirilgan** kod va amaliy loyihalar bilan ochib beriladi.

> Django 6.0 — full-stack: bir tomondan server tomonida HTML render qiluvchi **templates** (an'anaviy veb-ilovalar), ikkinchi tomondan **DRF** orqali zamonaviy SPA/mobil mijozlar uchun REST API. Bu kitobda ikkala qatlam ham qamraladi.

> **Qoida:** Django o'qib emas — **YOZIB** o'rganiladi. Har bir misolni o'zingiz tering, `python manage.py runserver` bilan ishga tushiring va brauzer/`curl` orqali sinab ko'ring. Xato chiqsa — aynan shu yerda haqiqiy o'rganish boshlanadi.

> Bu kitob siz Python asoslarini (o'zgaruvchi, funksiya, sinf, dekorator, virtual muhit, `pip`) bilasiz deb hisoblaydi. Python yangi bo'lsa, avval [Python — 0 dan Expertgacha](../python/README.md) kitobini o'qing.

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 -> 02 -> ...). Har biri oldingisiga tayanadi, sakramang.
2. 02-bobda virtual muhit yaratib, Django'ni o'rnatib, har bir misolni o'z kompyuteringizda ishga tushiring.
3. Amaliy loyihalarni o'zingiz qaytadan yozing — ko'chirib qo'yish bilan Django o'rganilmaydi.
4. ORM va DRF kabi mavzular amaliyotsiz mavhum tuyuladi — har bir `QuerySet` va endpointni o'zingiz sinang.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter (Windows / macOS / Linux) | Shart |
| Python 3.12+ (Django 6.0 uchun) | Shart |
| Python asoslari | **Shart** |
| Terminal va virtual muhit bilan tanishlik | Foydali |
| HTML/CSS asoslari | Foydali |
| Oldingi veb tajribasi | Shart emas |

---

## Mundarija

### I qism — Tanishuv

| # | Bob | Mavzu |
|---|---|---|
| 01 | [Django bilan tanishuv](./01-django-tanishuv.md) | Django nima, "batteries included" falsafasi, MVT arxitekturasi, qaerda ishlatiladi va nega tanlanadi. |
| 02 | [O'rnatish va birinchi loyiha](./02-ornatish-loyiha.md) | Virtual muhit, `pip install django`, `django-admin startproject`, `manage.py`, `startapp`, loyiha tuzilmasi va birinchi `runserver`. |
| 03 | [View va URL marshrutlash](./03-view-url.md) | Function-based views, `HttpRequest`/`HttpResponse`, `urls.py`, URL parametrlari va `path` konverterlari, `include`, nomlangan URL va `reverse`. |
| 04 | [Template tizimi (DTL)](./04-template-tizimi.md) | Django Template Language: o'zgaruvchilar, teglar, filtrlar, `{% extends %}`/`{% block %}` meros, `{% include %}`, kontekst va template render. |

### II qism — Modellar va ORM

| # | Bob | Mavzu |
|---|---|---|
| 05 | [Modellar va migratsiya](./05-modellar-migratsiya.md) | Modellar va maydon turlari, `makemigrations`/`migrate`, migratsiyalar qanday ishlaydi, baza sxemasi va modeldan jadvalga. |
| 06 | [ORM va QuerySet so'rovlar](./06-orm-queryset.md) | `objects` manager, `filter`/`exclude`/`get`, lookuplar, `order_by`, lazy QuerySet, `Q` va `F` obyektlari, agregatsiya. |
| 07 | [Model munosabatlari](./07-munosabatlar.md) | `ForeignKey`, `OneToOneField`, `ManyToManyField`, teskari munosabatlar (`related_name`), munosabatlar bo'ylab so'rov. |
| 08 | [Admin panel](./08-admin-panel.md) | Django admin'ni yoqish, model ro'yxatdan o'tkazish, `ModelAdmin` sozlamalari (`list_display`, `search_fields`, `inlines`), maxsuslashtirish. |
| 09 | [Ilg'or ORM va optimizatsiya](./09-ilgor-orm.md) | N+1 muammosi, `select_related`/`prefetch_related`, `annotate`, `values`/`only`/`defer`, transaction va so'rovlarni profillash. |

### III qism — Veb qatlam

| # | Bob | Mavzu |
|---|---|---|
| 10 | [Formalar va validatsiya](./10-formalar.md) | `forms.Form` va `ModelForm`, maydon validatsiyasi, `clean` metodlar, formani render qilish va CSRF himoyasi. |
| 11 | [Class-based views (CBV)](./11-class-based-views.md) | FBV vs CBV, generic views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`), mixinlar va metodlarni override qilish. |
| 12 | [Static, media va to'liq layout](./12-static-media-layout.md) | `staticfiles`, `STATIC_URL`/`STATICFILES_DIRS`, `collectstatic`, foydalanuvchi yuklagan media fayllar va to'liq sayt layouti. |
| 13 | [Autentifikatsiya va ruxsatlar](./13-auth-tizimi.md) | `User` modeli, login/logout/register, `login_required`, permissions va guruhlar, parol boshqaruvi. |
| 14 | [Sessiyalar, messages va middleware](./14-sessions-middleware.md) | Session framework, `messages` tizimi, middleware qanday ishlaydi va o'z middleware'ingizni yozish. |

### IV qism — REST API (DRF)

| # | Bob | Mavzu |
|---|---|---|
| 15 | [DRF kirish va serializers](./15-drf-serializers.md) | Django REST Framework o'rnatish, `Serializer` va `ModelSerializer`, validatsiya, `APIView` bilan birinchi endpoint. |
| 16 | [DRF ViewSets va routers](./16-drf-viewsets-routers.md) | `ViewSet`/`ModelViewSet`, `DefaultRouter` bilan avtomatik URL, kamroq kod bilan to'liq CRUD API. |
| 17 | [DRF autentifikatsiya (Token, JWT)](./17-drf-auth.md) | API autentifikatsiya: TokenAuthentication, JWT (`simplejwt`), permission classes va himoyalangan endpointlar. |
| 18 | [DRF filtrlash, paginatsiya, nested](./18-drf-filtering-pagination.md) | `django-filter`, qidiruv va saralash, paginatsiya stillari, nested serializers va munosabatlarni API'da ko'rsatish. |

### V qism — Ilg'or mavzular

| # | Bob | Mavzu |
|---|---|---|
| 19 | [Signallar va custom mantiq](./19-signals-custom.md) | `pre_save`/`post_save` va boshqa signallar, `receiver`, custom manager va QuerySet, model metodlari bilan biznes mantiq. |
| 20 | [Keshlash va performance](./20-caching-performance.md) | Cache framework, per-view va low-level kesh, Redis backend, `cached_property`, performance o'lchash va tezlashtirish. |
| 21 | [Async va fon vazifalari](./21-async-celery.md) | Django async views va ORM, ASGI, **Celery** bilan fon vazifalari, broker (Redis) va vaqt talab qiladigan ishlarni navbatga qo'yish. |

### VI qism — Production va kapston

| # | Bob | Mavzu |
|---|---|---|
| 22 | [Testlash](./22-testing.md) | `TestCase`, test client, model/view/API testlari, fixtures va factory, coverage va TDD yondashuvi. |
| 23 | [Settings, env va xavfsizlik](./23-settings-xavfsizlik.md) | `settings.py` ni muhitlarga bo'lish, `.env` va maxfiy kalitlar, `DEBUG`/`ALLOWED_HOSTS`, OWASP va Django xavfsizlik sozlamalari. |
| 24 | [Deployment (production)](./24-deployment.md) | Gunicorn/Uvicorn, Nginx, `collectstatic`, PostgreSQL, environment, **Docker** va production'ga chiqarish. |
| 25 | [Yakuniy kapston loyiha](./25-kapston.md) | Butun kitobni bog'laydigan production-darajali to'liq loyiha: modellar + DRF API + auth + testlar + deploy. "0 dan expertgacha" yo'lining yakuni. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
