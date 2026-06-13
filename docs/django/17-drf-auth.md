# 17 — DRF autentifikatsiya (Token, JWT)

[⬅️ Oldingi: 16 — DRF ViewSets va routers](./16-drf-viewsets-routers.md) · [🏠 README](./README.md) · [Keyingi: 18 — DRF filtrlash, paginatsiya, nested ➡️](./18-drf-filtering-pagination.md)

---

> **Bu bobda:** API'ni qulflashni o'rganamiz. Avval ikkita asosiy savolni ajratamiz: **autentifikatsiya** ("sen kimsan?") va **avtorizatsiya / ruxsat** ("sen nima qila olasan?"). Brauzer cookie va session API uchun nega yaramasligini ko'rib, ikkita yondashuvni o'rganamiz: `TokenAuthentication` (DRF ichida, `rest_framework.authtoken`) va `JWT` (`djangorestframework-simplejwt` bilan `TokenObtainPairView` / `TokenRefreshView` / `TokenVerifyView`). Keyin ruxsatga o'tamiz: `permission_classes`, tayyor klasslar `IsAuthenticated`, `IsAdminUser`, `IsAuthenticatedOrReadOnly`; o'zimizning `BasePermission` klassimiz; va **obyekt darajasidagi ruxsat** (`has_object_permission`) — "bu maqolani faqat muallifi tahrirlaydi". Oxirida **throttling** (so'rov tezligini cheklash) bilan API'ni suiiste'moldan himoya qilamiz: `AnonRateThrottle`, `UserRateThrottle`, `ScopedRateThrottle`. 401 va 403 farqini ham aniq tushunamiz. Hamma kod Django 6.0.6, Python 3.14, djangorestframework 3.17, djangorestframework-simplejwt 5.5 da haqiqatan ishga tushirib tekshirilgan.

---

## Ikki xil savol: "kimsan?" va "nima qila olasan?"

API xavfsizligi ikkita alohida savoldan iborat va ularni aralashtirmaslik juda muhim:

- **Autentifikatsiya (authentication)** — "Sen **kimsan**?" So'rov egasini aniqlash. DRF buni o'qib `request.user` ni o'rnatadi. Agar hech kim tanilmasa, `request.user` — `AnonymousUser` bo'ladi.
- **Avtorizatsiya / ruxsat (permission)** — "Sen bu amalni **qila olasanmi**?" Allaqachon tanilgan foydalanuvchi shu konkret amalga (o'qish, yozish, o'chirish) huquqi bormi.

Bu farq HTTP javob kodlarida ham ko'rinadi:

- **401 Unauthorized** — "Men seni tanimadim". Token yo'q yoki noto'g'ri. Avtentifikatsiya muvaffaqiyatsiz.
- **403 Forbidden** — "Men seni tanidim, lekin senga bu mumkin emas". Tanilgan, ammo ruxsat yo'q.

DRF har so'rovni quvur (pipeline) orqali o'tkazadi: avval autentifikatsiya, keyin ruxsat, keyin throttle, va detail amallarda obyekt darajasidagi ruxsat. Mana shu oqim:

![DRF so'rov quvuri: authentication, permission, throttle bosqichlari](rasmlar/dj17-auth-pipeline.svg)

> **Eslatma.** Web sahifalar uchun (10-bobdagi formalar, `login_required`) Django **session + cookie** ishlatadi. Lekin mobil ilova, SPA (React/Vue) yoki boshqa server bizning API'ga murojaat qilganda cookie qulay emas: ular brauzer emas, cookie saqlamaydi, CSRF mexanizmi ham mos kelmaydi. Shu sababli API'lar odatda **token** asosida ishlaydi — har so'rovda `Authorization` sarlavhasida token yuboriladi.

---

## Tayyorgarlik: loyiha va model

Bu bobda kichik blog API'si bilan ishlaymiz. Avval kerakli paketlar `INSTALLED_APPS` ga qo'shiladi (`settings.py`):

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",        # TokenAuthentication uchun jadval
    "rest_framework_simplejwt",        # JWT uchun
    "blog",
]
```

`rest_framework.authtoken` — bu Django ilovasi, u tokenlarni saqlash uchun bitta jadval (`authtoken_token`) qo'shadi. Shuning uchun uni qo'shgach migratsiya kerak:

```bash
python manage.py migrate
```

Model — har maqolaning egasi (`muallif`) bor. Bu obyekt darajasidagi ruxsatda kerak bo'ladi (`blog/models.py`):

```python
from django.conf import settings
from django.db import models


class Maqola(models.Model):
    sarlavha = models.CharField(max_length=200)
    matn = models.TextField()
    muallif = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="maqolalar",
    )
    yaratilgan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sarlavha
```

> **Nega `settings.AUTH_USER_MODEL`, `User` emas?** `settings.AUTH_USER_MODEL` — bu Django'da foydalanuvchi modeliga ishora qilishning to'g'ri usuli. Kelajakda custom User modeliga o'tsangiz, kod sinmaydi. Bu Django 6.0 idiomasi.

Serializer (`blog/serializers.py`) — `muallif` ni `ReadOnlyField` qilamiz, chunki egasini foydalanuvchi tanlamaydi, biz uni avtomatik so'rovni yuborgan foydalanuvchi qilib qo'yamiz:

```python
from rest_framework import serializers

from .models import Maqola


class MaqolaSerializer(serializers.ModelSerializer):
    muallif = serializers.ReadOnlyField(source="muallif.username")

    class Meta:
        model = Maqola
        fields = ["id", "sarlavha", "matn", "muallif", "yaratilgan"]
```

---

## TokenAuthentication: eng sodda token

Eng sodda token mexanizmi — DRF ichidagi `TokenAuthentication`. Mantiq oddiy:

1. Foydalanuvchi username + parol yuboradi.
2. Server tekshiradi va unga **bitta tasodifiy token** beradi, uni bazaga yozadi.
3. Keyingi har bir so'rovda klient shu tokenni `Authorization: Token <token>` sarlavhasida yuboradi.
4. Server bazadan tokenni topib, qaysi foydalanuvchiga tegishli ekanini aniqlaydi.

Buni yoqish uchun `settings.py` da DRF'ga aytamiz:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

`DEFAULT_AUTHENTICATION_CLASSES` — DRF har so'rovda shu klasslarni navbat bilan sinaydi: birortasi foydalanuvchini topsa, qolganini sinab o'tirmaydi. `SessionAuthentication` ni ham qoldirsak, brauzerli DRF interfeysi (browsable API) ishlashda davom etadi.

### Tokenni qanday olish

DRF tayyor view beradi — `obtain_auth_token`. URL'ga ulaymiz (`core/urls.py`):

```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # ...
    path("api/token-auth/", obtain_auth_token),
]
```

Endi foydalanuvchi username + parol yuborsa, token qaytadi:

```bash
# Komandalar qatorida (illustrativ - server ishlab turgan deb faraz qiladi):
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
     -d "username=ali&password=parol12345"
# Javob:  {"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
```

> Yuqoridagi `curl` bloki **illustrativ** — u haqiqiy ishlab turgan serverni talab qiladi, shu sababli bu bobning test muhitida `curl` orqali emas, balki DRF'ning test klienti orqali tekshirilgan (pastdagi testlarga qarang).

Tokenni qabul qilgach, har so'rovda shunday yuboriladi:

```bash
curl http://127.0.0.1:8000/api/me/ \
     -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

`Token` so'zi va token o'rtasida **bitta probel** bo'lishi shart. Bu DRF `TokenAuthentication` kutadigan format.

### Server tomonida test klienti bilan

DRF'ning `APIClient` ni ishlatib, tokenli kirishni real HTTP'siz tekshiramiz. `credentials()` metodi har so'rovga sarlavha qo'shadi:

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase


class TokenAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ali", password="parol12345")

    def test_token_olish(self):
        # Tayyor obtain_auth_token view: username+parol -> token
        r = self.client.post(
            "/api/token-auth/", {"username": "ali", "password": "parol12345"}
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("token", r.data)

    def test_token_bilan_kirish(self):
        token = Token.objects.create(user=self.user)
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        r = c.get("/api/me/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "ali")

    def test_tokensiz_401(self):
        # Token yubormasak -> 401 (kim ekaning aniqlanmadi)
        r = self.client.get("/api/me/")
        self.assertEqual(r.status_code, 401)
```

Yuqorida `/api/me/` — joriy foydalanuvchini qaytaradigan oddiy view (`blog/views.py`):

```python
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class MeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username, "id": request.user.id})
```

Boshqaruv buyrug'i orqali ham token yaratish mumkin (foydali, masalan admin uchun):

```bash
python manage.py drf_create_token ali
# 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## JWT: stateless token (simplejwt)

`TokenAuthentication` da server har so'rovda bazadan tokenni **qidiradi**. JWT (JSON Web Token) boshqacha: token o'z ichida foydalanuvchi ma'lumotini (`user_id`, muddati `exp`) saqlaydi va u serverning maxfiy kaliti bilan **imzolangan**. Server faqat imzoni tekshiradi — bazaga qaramaydi. Buni **stateless** deyiladi.

Ikkala yondashuvning farqi:

![TokenAuthentication va JWT ikkala oqim solishtirilgan](rasmlar/dj17-token-vs-jwt.svg)

JWT token uchta qismdan iborat, nuqta bilan ajralgan: `header.payload.signature`. Diqqat: payload **shifrlanmaydi**, faqat base64 bilan kodlanadi — shuning uchun **maxfiy ma'lumotni JWT ichiga qo'ymang** (masalan parolni).

simplejwt ikkita token beradi:

- **access** — qisqa umrli (masalan 5 daqiqa). Har API so'rovida ishlatiladi.
- **refresh** — uzun umrli (masalan 1 kun). Faqat yangi access olish uchun.

![JWT access va refresh tokenlar hayot sikli](rasmlar/dj17-jwt-lifecycle.svg)

### Sozlash

`settings.py` da autentifikatsiya klassiga JWT'ni qo'shamiz va token umrini belgilaymiz:

```python
from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

### URL'lar

simplejwt uchta tayyor view beradi (`core/urls.py`):

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,   # username+parol -> access+refresh
    TokenRefreshView,      # refresh -> yangi access
    TokenVerifyView,       # token yaroqlimi?
)

urlpatterns = [
    # ...
    path("api/jwt/create/", TokenObtainPairView.as_view()),
    path("api/jwt/refresh/", TokenRefreshView.as_view()),
    path("api/jwt/verify/", TokenVerifyView.as_view()),
]
```

### To'liq oqimni test klienti bilan tekshirish

```python
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase


class JWTTest(APITestCase):
    def setUp(self):
        User.objects.create_user("ali", password="parol12345")

    def test_jwt_create_refresh_verify(self):
        # 1. login -> access + refresh
        r = self.client.post(
            "/api/jwt/create/", {"username": "ali", "password": "parol12345"}
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)
        access = r.data["access"]
        refresh = r.data["refresh"]

        # 2. access bilan API'ga kirish - "Bearer" sxemasi (Token emas!)
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        me = c.get("/api/me/")
        self.assertEqual(me.status_code, 200)

        # 3. refresh -> yangi access
        rr = self.client.post("/api/jwt/refresh/", {"refresh": refresh})
        self.assertEqual(rr.status_code, 200)
        self.assertIn("access", rr.data)

        # 4. verify -> token yaroqli (200, javob bo'sh)
        v = self.client.post("/api/jwt/verify/", {"token": access})
        self.assertEqual(v.status_code, 200)

    def test_jwt_xato_parol(self):
        r = self.client.post(
            "/api/jwt/create/", {"username": "ali", "password": "notogri"}
        )
        self.assertEqual(r.status_code, 401)
```

> **Eng ko'p uchraydigan xato.** JWT'da sarlavha `Authorization: Bearer <token>` (so'z **Bearer**), `TokenAuthentication` da esa `Authorization: Token <token>`. Ikkalasini aralashtirsangiz 401 olasiz.

### JWT'ga qo'shimcha ma'lumot (custom claim)

Ba'zan token ichiga foydalanuvchi nomi yoki `is_staff` kabi ma'lumotni qo'shish kerak — frontend uni token'dan o'qiydi (qayta so'rov yubormasdan). Buning uchun `TokenObtainPairSerializer` ni meros olamiz:

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MeningTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username   # custom claim
        token["is_staff"] = user.is_staff
        return token


class MeningTokenView(TokenObtainPairView):
    serializer_class = MeningTokenSerializer
```

URL'da `TokenObtainPairView` o'rniga `MeningTokenView` ni ulaysiz. Endi access token payload'ida `username` va `is_staff` ham bo'ladi (biz buni tekshirib ko'rdik — payload kalitlari: `exp, iat, is_staff, jti, token_type, user_id, username`).

---

## permission_classes: kim nima qila oladi

Autentifikatsiya bilan "kimligini" aniqladik. Endi **ruxsat** — kim nima qila olishi. DRF'da har view'ning `permission_classes` ro'yxati bor; so'rov o'tishi uchun **barcha** ruxsat klasslari `True` qaytarishi kerak (mantiqiy VA).

### Tayyor ruxsat klasslari

| Klass | Ma'nosi |
|-------|---------|
| `AllowAny` | Hammaga ochiq (autentifikatsiya talab qilinmaydi) |
| `IsAuthenticated` | Faqat tanilgan (login qilgan) foydalanuvchilar |
| `IsAdminUser` | Faqat `is_staff=True` bo'lganlar |
| `IsAuthenticatedOrReadOnly` | O'qish (GET/HEAD/OPTIONS) hammaga; yozish faqat tanilganlarga |

### IsAuthenticated

Bitta view'ga ruxsat qo'yish — `permission_classes` atributi orqali. Bu global `DEFAULT_PERMISSION_CLASSES` ni shu view uchun bekor qiladi:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def maxfiy(request):
    return Response({"xabar": f"Salom, {request.user.username}!"})
```

Tanilmagan foydalanuvchi `/api/maxfiy/` ga kirsa — 401. Tanilgan bo'lsa — 200.

### IsAdminUser

`is_staff=True` bo'lganlargina kira oladi. Boshqalar (oddiy tanilgan foydalanuvchi ham) 403 oladi:

```python
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


class AdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"ok": True})
```

Biz buni `APIRequestFactory` bilan tekshirdik: oddiy foydalanuvchi (`is_staff=False`) → **403**, staff foydalanuvchi (`is_staff=True`) → **200**.

### IsAuthenticatedOrReadOnly

Eng ko'p ishlatiladigan naqsh: ro'yxat va o'qish hammaga ochiq, lekin yaratish/tahrirlash uchun login kerak. Buni ViewSet'da ko'ramiz:

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Maqola
from .serializers import MaqolaSerializer


class MaqolaViewSet(viewsets.ModelViewSet):
    queryset = Maqola.objects.all()
    serializer_class = MaqolaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Yangi maqola muallifini avtomatik so'rov egasi qilamiz
        serializer.save(muallif=self.request.user)
```

`perform_create` — ViewSet yangi obyekt saqlashdan oldin chaqiradigan ilgak (hook). `muallif` serializerda `ReadOnlyField` bo'lgani uchun foydalanuvchi uni yubora olmaydi; biz uni shu yerda majburan `request.user` qilib qo'yamiz. Bu — xavfsizlik uchun muhim naqsh: egasini hech qachon klient yuborgan ma'lumotdan olmang.

---

## Custom BasePermission yozish

Tayyor klasslar yetmasa, o'zimiznikini yozamiz. `BasePermission` dan meros olib, ikki metodning birini (yoki ikkalasini) ustun qoplaymiz:

- `has_permission(self, request, view)` — **view darajasi**. Har so'rovda, har doim chaqiriladi. "Bu foydalanuvchi umuman bu view'ga kira oladimi?"
- `has_object_permission(self, request, view, obj)` — **obyekt darajasi**. Faqat konkret obyekt bilan ishlanganda (detail: retrieve/update/destroy) chaqiriladi. "Bu foydalanuvchi **shu konkret obyekt** bilan bu amalni qila oladimi?"

### View darajasidagi custom permission

Misol: yozishga faqat ish kunlari ruxsat berish (o'qish doim ochiq). `SAFE_METHODS` — bu DRF'dagi tayyor to'plam: `("GET", "HEAD", "OPTIONS")`.

```python
import datetime

from rest_framework import permissions


class IshKunidaYoziladi(permissions.BasePermission):
    message = "Yozish faqat ish kunlari mumkin."

    def has_permission(self, request, view):
        # Xavfsiz (o'qish) metodlar - doim ruxsat
        if request.method in permissions.SAFE_METHODS:
            return True
        # 0=Dushanba ... 6=Yakshanba; faqat dush-juma yozish mumkin
        return datetime.datetime.now().weekday() < 5
```

`message` atributi — ruxsat rad etilganda 403 javobida ko'rsatiladigan matn. Biz `has_permission` ni GET so'rov uchun tekshirdik — `True` qaytdi.

### Obyekt darajasidagi custom permission

Bu eng muhim naqsh: **"bu maqolani faqat muallifi tahrirlay oladi"**. O'qish hammaga, lekin o'zgartirish faqat egasiga (`blog/permissions.py`):

```python
from rest_framework import permissions


class FaqatMuallifTahrirlaydi(permissions.BasePermission):
    """O'qish hammaga; yozish faqat obyekt muallifiga."""

    message = "Bu maqolani faqat muallifi tahrirlay oladi."

    def has_object_permission(self, request, view, obj):
        # GET/HEAD/OPTIONS - xavfsiz metodlar, hammaga ruxsat
        if request.method in permissions.SAFE_METHODS:
            return True
        # PATCH/PUT/DELETE - faqat muallif
        return obj.muallif == request.user
```

Uni ViewSet'ga qo'shamiz. Diqqat: ikkita ruxsat klassi bor — birinchisi (`IsAuthenticatedOrReadOnly`) view darajasida "umuman login qilganmi" ni tekshiradi, ikkinchisi (`FaqatMuallifTahrirlaydi`) obyekt darajasida "egasimisan" ni:

```python
class MaqolaViewSet(viewsets.ModelViewSet):
    queryset = Maqola.objects.all()
    serializer_class = MaqolaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, FaqatMuallifTahrirlaydi]

    def perform_create(self, serializer):
        serializer.save(muallif=self.request.user)
```

> **Muhim nozik nuqta.** `has_object_permission` **avtomatik** faqat `get_object()` chaqirilganda ishlaydi — ya'ni detail amallari (`/maqolalar/5/`) uchun. Ro'yxat (`list`) va `create` da u **chaqirilmaydi**. Shuning uchun "boshqa foydalanuvchining maqolasini ro'yxatdan yashirish" kerak bo'lsa, buni `get_queryset()` da filtrlash bilan qiling, permission bilan emas.

Buni to'liq test bilan tasdiqlaymiz:

```python
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Maqola


class PermissionTest(APITestCase):
    def setUp(self):
        self.ali = User.objects.create_user("ali", password="x")
        self.vali = User.objects.create_user("vali", password="x")
        self.maqola = Maqola.objects.create(
            sarlavha="Salom", matn="matn", muallif=self.ali
        )

    def test_oqish_anonim(self):
        # IsAuthenticatedOrReadOnly: GET hammaga
        r = self.client.get("/api/maqolalar/")
        self.assertEqual(r.status_code, 200)

    def test_yozish_anonim_401(self):
        # Tanilmagan + yozish -> 401
        r = self.client.post("/api/maqolalar/", {"sarlavha": "a", "matn": "b"})
        self.assertEqual(r.status_code, 401)

    def test_muallif_tahrirlaydi(self):
        self.client.force_authenticate(self.ali)   # haqiqiy muallif
        r = self.client.patch(
            f"/api/maqolalar/{self.maqola.id}/", {"sarlavha": "Yangi"}
        )
        self.assertEqual(r.status_code, 200)

    def test_begona_tahrirlay_olmaydi(self):
        self.client.force_authenticate(self.vali)   # begona, tanilgan
        r = self.client.patch(
            f"/api/maqolalar/{self.maqola.id}/", {"sarlavha": "Buzaman"}
        )
        self.assertEqual(r.status_code, 403)   # tanilgan, lekin egasi emas

    def test_create_muallif_avtomatik(self):
        self.client.force_authenticate(self.vali)
        r = self.client.post("/api/maqolalar/", {"sarlavha": "Yangi", "matn": "matn"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["muallif"], "vali")  # perform_create ishladi
```

`force_authenticate` — test klientining qulayligi: token/parolsiz to'g'ridan-to'g'ri foydalanuvchini "kirgan" qilib belgilaydi. Bu yerda 401 va 403 farqi yaqqol ko'rinadi: anonim yozsa **401**, begona tanilgan yozsa **403**.

---

## Throttling: so'rov tezligini cheklash

Throttling — bu foydalanuvchi (yoki anonim IP) ma'lum vaqtda nechta so'rov yubora olishini cheklash. Bu API'ni suiiste'mol va DoS hujumlardan himoya qiladi. Limit oshsa, DRF **429 Too Many Requests** qaytaradi.

Tayyor throttle klasslari:

- `AnonRateThrottle` — anonim (tanilmagan) so'rovlarni IP bo'yicha cheklaydi.
- `UserRateThrottle` — tanilgan foydalanuvchini ID bo'yicha cheklaydi.
- `ScopedRateThrottle` — har view'ga alohida nom (scope) berib, alohida limit qo'yish.

### Global throttle

`settings.py` da tezliklarni belgilaymiz. Format: `son/davr`, davr `s` (sekund), `min`, `hour`, `day` bo'lishi mumkin:

```python
REST_FRAMEWORK = {
    # ... (autentifikatsiya, ruxsat)
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",
        "user": "100/min",
    },
}
```

Endi har anonim IP daqiqasiga 10 ta, har tanilgan foydalanuvchi daqiqasiga 100 ta so'rov yubora oladi.

### View darajasidagi maxsus throttle

Ba'zan bitta og'ir endpointga (masalan parol tiklash, SMS yuborish) qattiqroq limit kerak. `UserRateThrottle` dan meros olib `scope` beramiz:

```python
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle


class SekinThrottle(UserRateThrottle):
    scope = "sekin"


@api_view(["POST"])
@throttle_classes([SekinThrottle])
def yubor(request):
    return Response({"holat": "qabul qilindi"})
```

Va `settings.py` da shu `scope` uchun tezlik:

```python
REST_FRAMEWORK = {
    # ...
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",
        "user": "100/min",
        "sekin": "3/min",     # bu endpoint daqiqasiga atigi 3 marta
    },
}
```

Buni test bilan tasdiqlaymiz — 3 tadan keyin 429 keladi:

```python
from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APITestCase


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
        ],
        "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.UserRateThrottle"],
        "DEFAULT_THROTTLE_RATES": {"user": "100/min", "sekin": "3/min"},
    }
)
class ThrottleTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ali", password="x")

    def test_throttle_429(self):
        self.client.force_authenticate(self.user)
        kodlar = [self.client.post("/api/yubor/").status_code for _ in range(5)]
        # 3/min: dastlabki 3 ta OK, 4-chi 429
        self.assertEqual(kodlar[:3], [200, 200, 200])
        self.assertEqual(kodlar[3], 429)
```

> **Eslatma kesh haqida.** Throttle hisoblarini DRF Django **kesh**ida saqlaydi (standart `LocMemCache`). Ishlab chiqarishda (production) ko'p server bo'lsa, hisob umumiy bo'lishi uchun **Redis** kabi markaziy kesh kerak. Redis serveri bu bobda ishga tushirilmagan — bu joy faqat sozlama ko'rsatkichi. Bu bobning testlari `LocMemCache` (Django standarti) bilan ishladi.

---

## To'liq rasm: hammasi birga

Yakuniy ViewSet (`blog/views.py`) autentifikatsiya, ruxsat va avtomatik muallifni birlashtiradi. Autentifikatsiya esa global `settings.py` da (JWT + Token + Session). Bu uchlik — ko'pchilik real API'larning poydevori:

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Maqola
from .permissions import FaqatMuallifTahrirlaydi
from .serializers import MaqolaSerializer


class MaqolaViewSet(viewsets.ModelViewSet):
    queryset = Maqola.objects.all()
    serializer_class = MaqolaSerializer
    # 1) login qilganmi (yozish uchun) 2) egasimi (tahrir uchun)
    permission_classes = [IsAuthenticatedOrReadOnly, FaqatMuallifTahrirlaydi]

    def perform_create(self, serializer):
        serializer.save(muallif=self.request.user)   # egasi = so'rov egasi
```

Bu kichik loyiha 11 ta avtomat test bilan to'liq tekshirilgan: token olish/ishlatish/401, JWT create-refresh-verify va xato parol, anonim o'qish, anonim yozish 401, muallif tahriri 200, begona tahriri 403, avtomatik muallif, va throttle 429.

> **Keyingi qadam.** Kelajakda PostgreSQL (`../sql/README.md`) va Redis bilan ishlab chiqarishga deploy qilganda, JWT kalitini muhit o'zgaruvchisidan o'qing va `ACCESS_TOKEN_LIFETIME` ni qisqa tuting. CI/CD orqali avtomatik testlarni ishga tushirish uchun `../git-github/README.md` ga qarang. Python asoslari kerak bo'lsa `../python/README.md`.

---

## Mashqlar

### Oson

1. `settings.py` da `DEFAULT_PERMISSION_CLASSES` ni `IsAuthenticated` qiling. Endi `/api/maqolalar/` ga anonim GET so'rov yuborilsa qaysi status kod keladi? Nega?
2. 401 va 403 status kodlari o'rtasidagi farqni o'z so'zlaringiz bilan tushuntiring. Qaysi biri "autentifikatsiya", qaysi biri "ruxsat" bilan bog'liq?
3. `TokenAuthentication` da `Authorization` sarlavhasi qanday ko'rinadi? JWT'da-chi? Ikkita format farqini yozing.
4. `AllowAny` permission klassi nima qiladi? Uni qaysi vaziyatda ishlatasiz (masalan ro'yxatdan o'tish endpoint'i)?
5. `SAFE_METHODS` to'plamida qaysi HTTP metodlar bor? Nega ular "xavfsiz" deyiladi?
6. JWT'da access va refresh tokenlar muddatini (masalan access 10 daqiqa, refresh 7 kun) qilib `SIMPLE_JWT` sozlamasini yozing.

### O'rta

1. `IzohViewSet` (Izoh modeli: `matn`, `muallif`, `maqola`) yarating. `perform_create` da `muallif` ni avtomatik `request.user` qilib qo'ying va `IsAuthenticatedOrReadOnly` ruxsatini bering.
2. `FaqatEgasiKoradi` nomli custom permission yozing: foydalanuvchi faqat **o'zining** obyektlarini (GET ham) ko'ra olsin. (Eslatma: bu ro'yxatda ishlamaydi — `get_queryset()` da ham filtrlash kerakligini izohlang.)
3. `obtain_auth_token` view'iga POST so'rov yuborib token olishni, keyin shu token bilan himoyalangan endpointga kirishni `APITestCase` da test qiling.
4. JWT custom claim qo'shing: token ichida foydalanuvchining `email` maydoni ham bo'lsin. `TokenObtainPairSerializer` ni meros oling.
5. `IsAdminUser` ruxsatli view yozing va ikkita test yozing: oddiy foydalanuvchi 403 oladi, staff foydalanuvchi 200 oladi (`APIRequestFactory` yoki `force_authenticate` bilan).
6. `ScopedRateThrottle` bilan ikki xil endpointga ikki xil limit qo'ying (masalan `qidiruv: 20/min`, `yuklash: 5/min`). `throttle_scope` atributini ishlating.

### Qiyin

1. To'liq autentifikatsiya oqimini yozing: foydalanuvchi `/api/jwt/create/` dan access oladi, u bilan maqola yaratadi (201), keyin access muddati o'tib ketgan deb faraz qilib `/api/jwt/refresh/` dan yangi access oladi va u bilan ham ishlay olishini test qiling.
2. `has_object_permission` ro'yxat (`list`) amalida chaqirilmasligini test bilan isbotlang: begona foydalanuvchi boshqa birovning maqolasini ro'yxatda ko'ra oladi (chunki obyekt ruxsati `list` da ishlamaydi), lekin `PATCH` qilolmaydi (403). Keyin `get_queryset()` ni filtrlab, ro'yxatdan ham yashiring.
3. `IsOwnerOrReadOnly` va `IsAdminUser` ni birlashtiruvchi mantiq yozing: obyektni egasi **yoki** admin tahrirlay olsin, boshqalar faqat o'qisin. Buni bitta custom `BasePermission` klassida `has_object_permission` bilan amalga oshiring va uchta holat uchun test yozing (egasi 200, admin 200, begona 403).

---

<details markdown="1">
<summary>Yechimlar</summary>

### Oson

**1.** `IsAuthenticated` da anonim GET ham rad etiladi — chunki bu klass o'qish/yozishni ajratmaydi, faqat "login qilganmi" ni tekshiradi. Status kod **401** (token yo'q, autentifikatsiya muvaffaqiyatsiz). Agar o'qishni ochiq qoldirmoqchi bo'lsangiz, `IsAuthenticatedOrReadOnly` ishlatish kerak.

**2.** **401 Unauthorized** — "seni tanimadim", autentifikatsiya muammosi (token yo'q yoki noto'g'ri). **403 Forbidden** — "seni tanidim, lekin senga ruxsat yo'q", avtorizatsiya/ruxsat muammosi. Ya'ni: anonim foydalanuvchi himoyalangan resursga kirsa 401; tanilgan, lekin egasi bo'lmagan foydalanuvchi tahrirlamoqchi bo'lsa 403.

**3.** `TokenAuthentication`: `Authorization: Token 9944b091...`. JWT: `Authorization: Bearer eyJhbGc...`. Farq — sxema so'zi: `Token` va `Bearer`. Aralashtirsangiz 401 olasiz.

**4.** `AllowAny` — hech qanday cheklov qo'ymaydi, hatto anonim foydalanuvchiga ham ruxsat beradi. Ro'yxatdan o'tish (`register`), login, yoki ochiq ma'lumot (blog ro'yxati) endpointlarida ishlatiladi — ya'ni foydalanuvchi hali token olmagan paytdagi endpointlar.

**5.** `SAFE_METHODS = ("GET", "HEAD", "OPTIONS")`. Ular "xavfsiz" deyiladi, chunki faqat **o'qiydi**, server holatini **o'zgartirmaydi** (ma'lumot yaratmaydi/o'chirmaydi).

**6.**
```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
```

### O'rta

**1.**
```python
# models.py
class Izoh(models.Model):
    matn = models.TextField()
    muallif = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    maqola = models.ForeignKey(Maqola, on_delete=models.CASCADE, related_name="izohlar")

# serializers.py
class IzohSerializer(serializers.ModelSerializer):
    muallif = serializers.ReadOnlyField(source="muallif.username")
    class Meta:
        model = Izoh
        fields = ["id", "matn", "muallif", "maqola"]

# views.py
class IzohViewSet(viewsets.ModelViewSet):
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(muallif=self.request.user)
```

**2.**
```python
class FaqatEgasiKoradi(permissions.BasePermission):
    message = "Faqat o'z obyektlaringizni ko'ra olasiz."

    def has_object_permission(self, request, view, obj):
        return obj.muallif == request.user
```
Bu obyekt darajasida ishlaydi, lekin `list` (ro'yxat) amalida `has_object_permission` chaqirilmaydi. Shuning uchun ro'yxatdan ham boshqalarning obyektlarini yashirish uchun ViewSet'da `get_queryset` ni filtrlash shart:
```python
    def get_queryset(self):
        return Maqola.objects.filter(muallif=self.request.user)
```

**3.**
```python
class TokenFlowTest(APITestCase):
    def setUp(self):
        User.objects.create_user("ali", password="parol12345")

    def test_token_olib_kirish(self):
        r = self.client.post(
            "/api/token-auth/", {"username": "ali", "password": "parol12345"}
        )
        self.assertEqual(r.status_code, 200)
        token = r.data["token"]

        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        me = c.get("/api/me/")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data["username"], "ali")
```

**4.**
```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EmailliTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token

class EmailliTokenView(TokenObtainPairView):
    serializer_class = EmailliTokenSerializer
```

**5.**
```python
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.views import APIView

class OnlyAdmin(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return Response({"ok": True})

class AdminTest(APITestCase):
    def test_oddiy_403(self):
        u = User.objects.create_user("oddiy", password="x", is_staff=False)
        self.client.force_authenticate(u)
        # OnlyAdmin URL'ga ulangan deb faraz: /api/onlyadmin/
        factory = APIRequestFactory()
        req = factory.get("/x/"); force_authenticate(req, user=u)
        self.assertEqual(OnlyAdmin.as_view()(req).status_code, 403)

    def test_staff_200(self):
        a = User.objects.create_user("admin", password="x", is_staff=True)
        factory = APIRequestFactory()
        req = factory.get("/x/"); force_authenticate(req, user=a)
        self.assertEqual(OnlyAdmin.as_view()(req).status_code, 200)
```

**6.**
```python
# views.py
from rest_framework.throttling import ScopedRateThrottle

class QidiruvView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "qidiruv"
    def get(self, request):
        return Response({"natija": []})

class YuklashView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "yuklash"
    def post(self, request):
        return Response({"ok": True})

# settings.py
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.ScopedRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"qidiruv": "20/min", "yuklash": "5/min"},
}
```

### Qiyin

**1.**
```python
class FullFlowTest(APITestCase):
    def setUp(self):
        User.objects.create_user("ali", password="parol12345")

    def test_jwt_toliq_oqim(self):
        # 1. login
        r = self.client.post(
            "/api/jwt/create/", {"username": "ali", "password": "parol12345"}
        )
        access, refresh = r.data["access"], r.data["refresh"]

        # 2. access bilan maqola yaratish
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        m = c.post("/api/maqolalar/", {"sarlavha": "S", "matn": "M"})
        self.assertEqual(m.status_code, 201)

        # 3. refresh -> yangi access
        rr = self.client.post("/api/jwt/refresh/", {"refresh": refresh})
        yangi_access = rr.data["access"]

        # 4. yangi access bilan ham ishlaydi
        c2 = APIClient()
        c2.credentials(HTTP_AUTHORIZATION=f"Bearer {yangi_access}")
        self.assertEqual(c2.get("/api/maqolalar/").status_code, 200)
```

**2.**
```python
class ListVsObjectTest(APITestCase):
    def setUp(self):
        self.ali = User.objects.create_user("ali", password="x")
        self.vali = User.objects.create_user("vali", password="x")
        self.maqola = Maqola.objects.create(sarlavha="S", matn="M", muallif=self.ali)

    def test_begona_royxatda_koradi_lekin_tahrir_yoq(self):
        self.client.force_authenticate(self.vali)
        # list: obyekt ruxsati chaqirilmaydi -> begona ham ko'radi
        lst = self.client.get("/api/maqolalar/")
        self.assertEqual(lst.status_code, 200)
        self.assertEqual(len(lst.data), 1)
        # detail PATCH: obyekt ruxsati ishlaydi -> 403
        patch = self.client.patch(
            f"/api/maqolalar/{self.maqola.id}/", {"sarlavha": "X"}
        )
        self.assertEqual(patch.status_code, 403)
```
Ro'yxatdan ham yashirish uchun ViewSet'ga:
```python
    def get_queryset(self):
        # Anonimga hammasi, tanilganga faqat o'ziniki - vaziyatga qarab
        return Maqola.objects.filter(muallif=self.request.user)
```
Endi `len(lst.data) == 0` bo'ladi, chunki ro'yxat queryset darajasida filtrlangan.

**3.**
```python
class IsOwnerOrAdmin(permissions.BasePermission):
    message = "Faqat egasi yoki admin tahrirlaydi."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # egasi YOKI admin (is_staff)
        return obj.muallif == request.user or request.user.is_staff


# Test
class OwnerOrAdminTest(APITestCase):
    def setUp(self):
        self.ali = User.objects.create_user("ali", password="x")
        self.vali = User.objects.create_user("vali", password="x")
        self.admin = User.objects.create_user("admin", password="x", is_staff=True)
        self.maqola = Maqola.objects.create(sarlavha="S", matn="M", muallif=self.ali)
        # ViewSet permission_classes = [IsAuthenticated, IsOwnerOrAdmin] deb faraz

    def _patch(self, user):
        self.client.force_authenticate(user)
        return self.client.patch(
            f"/api/maqolalar/{self.maqola.id}/", {"sarlavha": "Y"}
        ).status_code

    def test_egasi_200(self):
        self.assertEqual(self._patch(self.ali), 200)

    def test_admin_200(self):
        self.assertEqual(self._patch(self.admin), 200)

    def test_begona_403(self):
        self.assertEqual(self._patch(self.vali), 403)
```

</details>

---

[⬅️ Oldingi: 16 — DRF ViewSets va routers](./16-drf-viewsets-routers.md) · [🏠 README](./README.md) · [Keyingi: 18 — DRF filtrlash, paginatsiya, nested ➡️](./18-drf-filtering-pagination.md)
