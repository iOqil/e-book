# 15 — Avtomatik deploy

[⬅️ Oldingi: 14 — Docker image CI va GHCR](./14-docker-ci-ghcr.md) · [🏠 README](./README.md) · [Keyingi: 16 — Nginx asoslari ➡️](./16-nginx-asoslari.md)

> **Bu bobda:** CI/CD zanjirini oxirigacha yopamiz — [14-bobda](./14-docker-ci-ghcr.md) image GHCR'ga push bo'lgan edi, endi uni serverga **avtomatik deploy** qilamiz. Asosiy usul — **push-based SSH deploy**: GitHub Actions job serverga `ssh` bilan kiradi va `docker compose pull && docker compose up -d` qiladi (SSH kalit, host, user `secrets`'da). Buni ikki yo'l bilan ko'rsatamiz: tayyor `appleboy/ssh-action@v1.2.5` va sof `ssh` + `known_hosts`. So'ng **`environments`** (staging va production) bilan deployni boshqaramiz: `push main`'da staging avtomatik, production esa **qo'lda APPROVAL** (protection rules, required reviewers, environment secrets) ortida; triggerlar — `on push`, `on release`/tag, `workflow_dispatch`. **Rollback**'ni o'rganamiz — oldingi immutable tag'ga (`sha`/semver) qaytib qayta `up`; **zero-downtime** kirish (`up -d` yangi konteyner ko'taradi, healthcheck o'tgach eskisini o'chiradi); **pull-based** alternativa (Watchtower / GitOps — 24-bobga ishora) va deploy **xavfsizligi** (alohida cheklangan SSH user, secrets'ni logda ko'rsatmaslik).

---

## Muammo: image tayyor, lekin serverda hali eski versiya

[14-bobda](./14-docker-ci-ghcr.md) chiroyli ish qildik: har `git push`da GitHub Actions namuna ilovamizning (`vazifalar-api`) Docker image'ini quradi va `ghcr.io/foydalanuvchi/vazifalar-api` ga push qiladi. Registry'da `:latest`, `:main`, `:sha-abc1234` teglari yaltirab turibdi.

Lekin... serverda nima o'zgardi? **Hech nima.** Server hali ham eski image bilan ishlayapti. Yangi versiyani ko'rsatish uchun kimdir hali ham `ssh` qilib kirib, `docker compose pull` va `docker compose up -d` qilishi kerak. Ya'ni [5-bobdagi](./05-qolda-deploy.md) **5-og'riq** — "har yangilashda yana qo'lda" — to'liq yo'qolmadi: biz faqat *build*'ni avtomatlashtirib, *deploy*'ni qo'lda qoldirdik.

Bu bobda zanjirning oxirgi bo'g'inini ulaymiz: **push qildingiz -> sekundlar ichida server yangi versiyada**. Odam aralashuvisiz (production'da — bitta tasdiq tugmasi bilan).

> 📌 Bu bobning ilovasi — kitob bo'ylab kelayotgan o'sha `vazifalar-api`. Serverda u allaqachon `compose.yaml` bilan ishlamoqda ([11-bob](./11-docker-compose.md)) va image GHCR'da ([14-bob](./14-docker-ci-ghcr.md)). Bizga faqat "yangi image'ni tortib qo'yadigan" deploy bosqichi qoldi.

---

## Deploy oqimi: build'dan serverga

Avtomatik deployning to'liq manzarasi quyidagicha. Build job image quradi va GHCR'ga push qiladi; deploy job esa serverga `ssh` bilan kirib, o'sha yangi image'ni tortib oladi va konteynerni qayta ko'taradi.

![CI/CD avtomatik deploy oqimi: git push GitHub Actions ni ishga tushiradi, build job Docker image quradi va GHCR ga push qiladi, deploy job serverga ssh bilan kirib docker compose pull va up qiladi, ilova yangi versiyada ishlaydi](rasmlar/dvo15-deploy-oqim.svg)

E'tibor bering: deploy job **build job tugagach** ishlaydi (`needs: build`), chunki tortib oladigan image avval registry'da paydo bo'lishi kerak. Server tomonida hech qanday build yo'q — server faqat tayyor image'ni `pull` qiladi. Bu push-based deployning go'zalligi: server "ohist" qoladi, og'ir build ishi CI'da bo'ladi.

> 💡 "Push-based" nomi shundan: **CI server tomon itaradi** (push qiladi). Buning aksi — "pull-based": server o'zi registry/Git'ni kuzatib, o'zgarishni tortib oladi (bob oxirida Watchtower/GitOps). Boshlash uchun push-based soddaroq va tushunarliroq.

---

## Server tomoni: deploy nima qiladi

Avval serverda nima sodir bo'lishini aniq tushunaylik — workflow shunchaki shu buyruqlarni masofadan chaqiradi. Serverda loyiha papkasida (masalan `/srv/vazifalar-api`) `compose.yaml` turadi va u image'ni GHCR'dan oladi:

```yaml
services:
  api:
    image: ghcr.io/foydalanuvchi/vazifalar-api:latest
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:3000"
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://localhost:3000/tasks').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 5s
```

> ℹ️ `127.0.0.1:3000:3000` — port faqat serverning o'ziga ochiq (tashqariga emas); oldida Nginx turadi (16-17-boblar). `healthcheck` — Docker ilova "tirik"ligini tekshiradi; zero-downtime uchun keyin asqotadi.

Deploy paytida serverda bajariladigan skript — `deploy.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /srv/vazifalar-api

# Yangi image'ni GHCR'dan tortib olish
docker compose pull

# Yangi konteynerni ko'tarish, eskisini almashtirish, yetim konteynerlarni tozalash
docker compose up -d --remove-orphans

# Ishlatilmayotgan eski image'larni tozalash (disk to'lib qolmasin)
docker image prune -f
```

Bu skriptdagi har bir buyruq aniq vazifa bajaradi:

- `docker compose pull` — `compose.yaml`'dagi `image:` tegiga mos yangi image'ni registry'dan tortadi. Agar registry private bo'lsa, oldin `docker login ghcr.io` qilingan bo'lishi kerak (pastda).
- `docker compose up -d --remove-orphans` — o'zgargan servislar uchun **yangi konteyner** yaratadi, eskisini to'xtatib o'rniga qo'yadi (`-d` — fonda). `--remove-orphans` — `compose.yaml`'dan olib tashlangan servislarning eski konteynerlarini tozalaydi.
- `docker image prune -f` — endi hech qaysi konteyner ishlatmaydigan "osilib qolgan" (dangling) image'larni o'chiradi; aks holda har deployda disk to'lib boradi.

> ⚠️ Bu server qadamlari **illustrativ** — ular **haqiqiy VPS**da bajariladi. Lokal mashinada bu skriptning sintaksisini tekshirish mumkin (`bash -n deploy.sh`), lekin `docker compose pull` real serverda, GHCR'ga ulanish bilan ishlaydi. Buyruqlar to'g'ri yozilgan — o'z serveringizda sinab ko'ring.

---

## Push-based deploy: GitHub Actions serverga SSH bilan kiradi

Endi workflow yozamiz. G'oya oddiy: build job image'ni push qilgach, deploy job serverga `ssh` orqali kirib yuqoridagi buyruqlarni bajaradi. Buning uchun GitHub'ga serverga kirish ma'lumotlari kerak — ularni **hech qachon kodga yozmaymiz**, balki **repository secrets**'da saqlaymiz.

Kerakli secrets (repo `Settings -> Secrets and variables -> Actions`):

| Secret | Nima | Misol |
|---|---|---|
| `DEPLOY_HOST` | server IP yoki domen | `203.0.113.10` |
| `DEPLOY_USER` | deploy uchun SSH user | `deploy` |
| `DEPLOY_SSH_KEY` | **maxfiy** SSH kalit (private key) | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_PORT` | SSH port (ixtiyoriy) | `22` |

> 📌 `DEPLOY_SSH_KEY` — bu serverga kiruvchi **maxfiy** kalitning (private key) to'liq matni. Uni alohida, faqat deploy uchun yaratilgan kalit juftligidan oling (pastda "Xavfsizlik" bo'limi). Hech qachon shaxsiy kalitingizni ishlatmang.

### Variant A: `appleboy/ssh-action` (soddaroq)

Eng keng tarqalgan yo'l — tayyor `appleboy/ssh-action`. U SSH ulanishini, kalit va `known_hosts` bilan bog'liq mayda-chuydani o'zi hal qiladi; siz faqat serverda bajariladigan `script`'ni berasiz.

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6
      - uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest,ghcr.io/${{ github.repository }}:sha-${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Serverga SSH bilan deploy
        uses: appleboy/ssh-action@v1.2.5
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          port: ${{ secrets.DEPLOY_PORT }}
          script: |
            set -e
            cd /srv/vazifalar-api
            echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
            docker compose pull
            docker compose up -d --remove-orphans
            docker image prune -f
```

Bu yerda muhim joylar:

- `needs: build` — deploy faqat build muvaffaqiyatli tugagach ishlaydi. Image yo'q bo'lsa, deploy qilishdan ma'no yo'q.
- `appleboy/ssh-action@v1.2.5` — versiyani **aniq qotirdik** (tasdiqlangan: bu actionning joriy barqaror relizi). `@v1` kabi "harakatlanuvchi" teg ham bor, lekin qotirilgan versiya — takrorlanadigan (reproducible) deploy.
- `set -e` (script birinchi qatori) — `script` ichidagi biror buyruq xato qaytarsa, qolganlari bajarilmaydi va job qulaydi. Buni **albatta** qo'ying, aks holda `pull` muvaffaqiyatsiz bo'lsa ham `up` ishlab, yarim-buzuq deploy chiqadi. (Eslatma: `appleboy/ssh-action` ning eski `script_stop` inputi v1.2.5 da olib tashlangan — uning o'rniga skript boshiga `set -e` qo'yiladi.)
- `docker login ... --password-stdin` — image private bo'lsa kerak. `GITHUB_TOKEN` faqat shu workflow ishlayotgan paytda amal qiladi (vaqtinchalik), shuning uchun serverda doimiy parol qoldirmaydi.

> 💡 `--password-stdin` parolni argument sifatida bermaydi (process ro'yxatida ko'rinmaydi), `stdin` orqali uzatadi. Parolni `docker login -p PAROL` bilan to'g'ridan-to'g'ri yozish — yomon odat.

### Variant B: sof `ssh` + `known_hosts`

Tashqi action'ga bog'lanmaslik istasangiz (yoki uning ichida nima ketayotganini to'liq nazorat qilmoqchi bo'lsangiz), sof `ssh` bilan ham bo'ladi. Bu yerda muhim narsa — **`known_hosts`**: server kalitini oldindan ishonchli ro'yxatga qo'shmasak, `ssh` interaktiv "yes/no" so'raydi va job qotib qoladi.

```yaml
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: SSH kalit va known_hosts ni tayyorlash
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan -H "${{ secrets.DEPLOY_HOST }}" >> ~/.ssh/known_hosts

      - name: Serverga deploy
        run: |
          ssh -i ~/.ssh/id_ed25519 \
            "${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }}" \
            'cd /srv/vazifalar-api && docker compose pull && docker compose up -d --remove-orphans && docker image prune -f'
```

> ⚠️ `ssh-keyscan` serverning kalitini avtomatik oladi — bu qulay, lekin "ishonish-birinchi-ulanishda" (TOFU) prinsipiga tayanadi: agar deploy paytida o'rtada hujum (MITM) bo'lsa, soxta kalit yozilishi mumkin. Yuqori xavfsizlik kerak bo'lsa, server kalitini bir marta o'zingiz olib, `secrets.DEPLOY_KNOWN_HOSTS`'ga qo'ying va `ssh-keyscan` o'rniga uni yozing.

Ikkala variant bir xil natija beradi. Boshlash uchun **Variant A** soddaroq; **Variant B** esa nima sodir bo'layotganini ochiq ko'rsatadi va keraksiz bog'liqlikni yo'qotadi.

---

## Environments: staging va production, qo'lda tasdiq bilan

To'g'ridan-to'g'ri production'ga deploy qilish — qo'rqinchli. Agar yangi versiya buzuq bo'lsa-chi? Shuning uchun jiddiy loyihalar **ikki muhit** ishlatadi:

- **staging** — production'ning nusxasi; bu yerga **avtomatik** deploy bo'ladi, sinab ko'rasiz.
- **production** — haqiqiy foydalanuvchilar; bu yerga deploy **qo'lda tasdiq** (approval) ortida.

GitHub'da buni **Environments** mexanizmi bilan qilamiz. Har bir environment'ning o'z **secrets**'i (har muhit o'z serveri), o'z **protection rules**'i (kim/qachon deploy qila oladi) bo'ladi.

![Ikki muhitli deploy oqimi: git push main staging muhitiga avtomatik deploy boladi, sungra production muhiti oldida required reviewers tasdiq darvozasi turadi, tasdiqlangach production ga deploy boladi](rasmlar/dvo15-environments.svg)

Avval GitHub'da environment yaratasiz: repo `Settings -> Environments -> New environment`. `production` uchun **Required reviewers** yoqib, o'zingizni (yoki jamoa a'zosini) qo'shasiz — endi shu environment'ga tegadigan job **tasdiqsiz ishlamaydi**.

Workflow'da `environment:` kalitini job'ga qo'shamiz:

```yaml
name: Deploy

on:
  push:
    branches: [main]
  release:
    types: [published]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6
      - uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:sha-${{ github.sha }}

  deploy-staging:
    needs: build
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.vazifalar.uz
    steps:
      - uses: appleboy/ssh-action@v1.2.5
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          envs: IMAGE_TAG
          script: |
            set -e
            cd /srv/vazifalar-api
            export IMAGE_TAG=sha-${{ github.sha }}
            docker compose pull
            docker compose up -d --remove-orphans

  deploy-production:
    needs: build
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://vazifalar.uz
    steps:
      - uses: appleboy/ssh-action@v1.2.5
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            set -e
            cd /srv/vazifalar-api
            docker compose pull
            docker compose up -d --remove-orphans
```

Diqqat qiling:

- **Triggerlar uchta:** `push: main` (staging avto), `release: published` (production), `workflow_dispatch` (qo'lda "Run workflow" tugmasi — favqulodda holatda).
- `deploy-staging` faqat `push`'da (`if: github.event_name == 'push'`), `deploy-production` faqat `release`'da ishlaydi.
- `environment: name: production` job'ga **protection rules**'ni bog'laydi. GitHub'da `production` uchun required reviewer qo'yilgani uchun, bu job **"Waiting for approval"** holatida kutib turadi — kimdir tasdiqlamaguncha SSH ham qilmaydi. `url:` esa Actions UI'da "View deployment" havolasini ko'rsatadi.
- Secrets `${{ secrets.DEPLOY_HOST }}` — agar `production` va `staging` environment'larida bir xil nomli **environment secret** belgilangan bo'lsa, har job o'z muhitining qiymatini oladi (har muhit — boshqa server). Bu environment secrets'ning asosiy foydasi.

> 📌 `environment` darvozasi — **CD'dagi eng muhim xavfsizlik chizig'i**. U "bitta noto'g'ri push butun production'ni yiqitishi"ni to'xtatadi: production'ga har deploy ongli, qo'lda tasdiqlangan harakat bo'ladi.

> 💡 `release` trigger semantik versiyalash bilan tabiiy yuradi: GitHub'da `v1.4.0` teg bilan release chiqarasiz -> production deploy ishga tushadi -> reviewer tasdiqlaydi -> server o'sha versiyaga o'tadi. Tag — deployning "manzili".

---

## Zero-downtime: foydalanuvchi uzilishni sezmaydi

`docker compose up -d` aytilganda Docker o'zgargan servis uchun **yangi konteyner** yaratadi, u tayyor bo'lgach **eskisini to'xtatadi**. Ya'ni qisqa vaqt ichida ikkala konteyner ham yashashi mumkin — bu zero-downtime deployning poydevori. Lekin sodda holatda baribir kichik uzilish bo'ladi: eski konteyner o'lib, yangisi hali so'rovga tayyor bo'lmagan oniy.

Bu yerda **`healthcheck`** asqotadi. Agar `compose.yaml`'da healthcheck bo'lsa, Docker yangi konteyner *sog'lom* (healthy) bo'lgunicha kutadi. Oldida Nginx/reverse-proxy turgan to'liq production'da (20-bobda chuqur ko'ramiz) bu — foydalanuvchi hech narsani sezmaydigan, silliq almashinuvga aylanadi: proxy faqat sog'lom konteynerga trafik yuboradi.

Hozircha shuni bilish kifoya: **healthcheck'siz "deploy bo'ldi" yolg'on bo'lishi mumkin** — konteyner ko'tarilgan, lekin ilova ichida xato bilan qulagan. Healthcheck bilan Docker "haqiqatan tayyor"ligini biladi. To'liq zero-downtime strategiyasi (blue-green, rolling) — 20 va 22-boblarda.

> 📌 Deploy job "yashil" bo'lishi — ilova ishlayapti degani EMAS. Har deploydan keyin **healthcheck** yoki kichik `curl` "smoke test" bilan haqiqatan javob berayotganini tasdiqlang. Aks holda buzuq versiya jimgina production'da turadi.

---

## Rollback: oldingi versiyaga qaytish

Deploy qildingiz — va sayt qulab tushdi. Birinchi qoida: **panika qilma, orqaga qayt.** Buni "fixni topib, yangi deploy qilaman" emas, balki avval **rollback** (oldingi ishlaydigan versiyaga qaytish) qilib, keyin sokin holatda fixni o'ylash kerak.

![Rollback jarayoni: v2 versiya production ga deploy boladi va qulaydi, server compose faylida image teg v2 dan oldingi sog'lom v1 ga o'zgartiriladi, docker compose up bilan v1 qayta ko'tariladi va ilova tiklanadi](rasmlar/dvo15-rollback.svg)

Rollback shuning uchun ham oson bo'ladiki, biz **immutable** (o'zgarmas) teglardan foydalanamiz. `sha-abc1234` yoki `v1.4.0` kabi teg har doim **aynan bitta** image'ni bildiradi va u hech qachon o'zgarmaydi. Demak "oldingi versiya"ga qaytish — shunchaki oldingi tegni qayta ishga tushirish:

```bash
# Serverda: hozir qaysi image ishlayotganini ko'rish
docker compose ps

# compose.yaml'da image tegini oldingi sog'lom versiyaga o'zgartirish
# image: ghcr.io/foydalanuvchi/vazifalar-api:sha-abc1234  (eski, ishlaydigan)

# yoki teg'ni muhit o'zgaruvchisi bilan boshqarsangiz:
IMAGE_TAG=sha-abc1234 docker compose up -d
```

> ⚠️ **Nega `:latest` rollback uchun yomon.** Agar serverda har doim `:latest` ishlatilsa, "oldingi versiya" degan tushuncha yo'qoladi — `latest` doim eng yangini bildiradi. `docker compose pull` baribir buzuq versiyani tortadi. Shuning uchun production'da **immutable teg** (sha yoki semver) ishlating, `latest`'ni faqat qulaylik uchun qo'shimcha teg sifatida qoldiring.

Eng toza yo'l — `compose.yaml`'da image tegini muhit o'zgaruvchisidan olish:

```yaml
services:
  api:
    image: ghcr.io/foydalanuvchi/vazifalar-api:${IMAGE_TAG:-latest}
```

Endi deploy `IMAGE_TAG=sha-<yangi> docker compose up -d`, rollback esa `IMAGE_TAG=sha-<eski> docker compose up -d` — bitta o'zgaruvchi. Hatto rollbackni ham `workflow_dispatch` input'i bilan tugma orqali qilish mumkin (mashqlar bo'limida).

> 💡 Rollback strategiyasi — image-versiyalash strategiyangizning bevosita natijasi ([9-bob](./09-image-optimizatsiya.md), teglash). Immutable teglar -> bir soniyalik rollback. `latest`-only -> rollback uchun qayta build kutish. Shuning uchun "har deployga `sha` tegi" — bekorga emas.

---

## Pull-based alternativa: Watchtower va GitOps (qisqacha)

Biz ko'rgan usul — **push-based**: CI server tomon "itaradi". Muqobil falsafa — **pull-based**: server (yoki klaster) o'zi registry/Git'ni kuzatib turadi va o'zgarishni o'zi tortib oladi. Ikki keng tarqalgan yo'l:

- **Watchtower** — serverda ishlaydigan kichik konteyner; registry'dagi image yangilanganini sezsa, sizning konteyneringizni avtomatik yangilaydi. Kichik loyihalar uchun juda qulay: CI faqat push qiladi, qolganini Watchtower hal qiladi. Kamchiligi — yangilanish ustidan aniq nazorat va approval kamayadi.
- **GitOps (Argo CD / Flux)** — "haqiqat manbai" — Git repozitoriy. Siz Git'da kerakli holatni (qaysi versiya ishlashi kerakligini) yozasiz, klasterdagi agent doimo Git'ni real holat bilan solishtirib, farqni o'zi to'g'rilaydi. Bu — Kubernetes dunyosining standart deploy yondashuvi.

> ℹ️ GitOps'ni Kubernetes kontekstida [24-bobda](./24-ingress-helm-gitops.md) batafsil ko'ramiz. Hozir shuni bilish kifoya: push-based — boshlash uchun eng sodda va ko'rinarli; ko'lam o'sgani sayin pull-based/GitOps ishonchliroq va auditga qulayroq bo'ladi.

---

## Xavfsizlik: deploy kalitini ehtiyot qiling

Avtomatik deploy serverga **doimiy kalit** beradi — bu qulaylik, lekin xavf ham. Bir nechta qat'iy qoida:

- **Alohida, cheklangan deploy user.** Serverda faqat deploy uchun maxsus user (masalan `deploy`) yarating; unga `root` bermang. U faqat loyiha papkasiga va `docker` buyrug'iga ega bo'lsin. Eng yaxshisi — bu user faqat kerakli `docker compose` buyruqlarini bajara olsin.
- **Alohida SSH kalit juftligi.** Deploy uchun shaxsiy kalitingizni emas, faqat shu maqsadda yaratilgan kalitni ishlating:

```bash
# Lokal mashinada deploy uchun kalit juftligi yaratish
ssh-keygen -t ed25519 -C "deploy-vazifalar-api" -f ./deploy_key

# Ochiq kalitni (public) serverdagi deploy user authorized_keys ga qo'shing:
#   cat deploy_key.pub >> /home/deploy/.ssh/authorized_keys
# Maxfiy kalitni (private) deploy_key faylidan oling va GitHub secret DEPLOY_SSH_KEY ga joylang.
```

- **Secrets — faqat secrets'da.** Host, user, kalit — hech qachon workflow YAML'iga, kodga yoki commit'ga yozilmaydi. GitHub `secrets` qiymatlarni loglarda avtomatik **maskalaydi** (`***` bilan yashiradi), lekin siz ham ularni `echo` qilmang.
- **Kalit chiqib ketsa — darhol bekor qiling.** Serverdagi `authorized_keys`'dan o'sha ochiq kalitni o'chiring va GitHub secret'ni yangilang. Immutable, alohida kalit shuning uchun ham yaxshi: bittasini bekor qilish boshqalariga ta'sir qilmaydi.

> ⚠️ Deploy job loglarini commit/PR ochiq bo'lsa hamma ko'radi. `set -x` (bash debug) yoqib, kalit yoki tokenni echo qilib qo'ymang — bir marta loglarga tushgan maxfiy ma'lumot "chiqib ketgan" hisoblanadi. Shubha bo'lsa — kalitni almashtiring.

> 📌 Production'ga deploy uchun ideal: alohida `deploy` user + alohida SSH kalit + `environment: production` approval darvozasi + immutable teg. Bu to'rt qatlam birgalikda "tasodifan yoki yomon niyatda production'ni buzish"ni juda qiyinlashtiradi.

---

## Yakun: zanjir yopildi

Endi to'liq CI/CD zanjiri ishlaydi: **kod yozasiz -> `git push` -> test ([13-bob](./13-pipeline-test-build.md)) -> image build + GHCR push ([14-bob](./14-docker-ci-ghcr.md)) -> staging'ga avto-deploy -> tag/release bilan production'ga tasdiqli deploy (shu bob).** [5-bobdagi](./05-qolda-deploy.md) 5-og'riq — "har yangilash qo'lda + downtime" — nihoyat yo'qoldi.

Hali serverda ilova `:3000` portda, oldida hech nima yo'q — foydalanuvchiga `http://203.0.113.10:3000` deb aytib bo'lmaydi. Keyingi bo'lim (16-18-boblar) shuni hal qiladi: **Nginx** reverse proxy, domen va HTTPS. 20-bob esa hamma narsani — Docker, CI/CD, Nginx, HTTPS, zero-downtime — bitta to'liq production deploy'ga birlashtiradi.

---

## 15-bob mashqlari

### Oson

1. Avtomatik deployda **build** va **deploy** j'oblari nega alohida bo'lib, deploy `needs: build` bilan bog'lanadi? Agar `needs`'ni olib tashlasangiz qanday muammo bo'lishi mumkin?
2. Quyidagi to'rt secret'ning har biri nima uchun kerak: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_PORT`. Qaysi biri eng maxfiy va nega?
3. Deploy triggeri sifatida `push: main`, `release: published`, `workflow_dispatch` — har birining vazifasini bir jumlada ayting.
4. `docker compose up -d --remove-orphans` buyrug'idagi `-d` va `--remove-orphans` nima qiladi? `-d`siz deploy job'da nima bo'lardi?
5. Nega production deploy uchun `:latest` emas, `:sha-...` yoki `:v1.4.0` kabi immutable teg afzal? Bitta jumlada javob bering.

### O'rta

6. `appleboy/ssh-action` (Variant A) va sof `ssh` + `known_hosts` (Variant B) ni solishtiring: har birining bittadan afzalligi va bittadan kamchiligini ayting. Variant B'da `known_hosts` nega kerak?
7. GitHub Environments'da `production` uchun **Required reviewers** qo'yilgan. Reviewer tasdiqlamaguncha `environment: production` bo'lgan job qaysi holatda turadi va SSH qiladi-mi? Tushuntiring.
8. Deploy job "yashil" (muvaffaqiyatli) bo'lsa-yu, ilova ichida xato bilan qulagan bo'lsa — buni qanday aniqlaysiz? `healthcheck` va "smoke test" rollarini ayting.
9. `set -e` (script boshida) nima uchun deploy skriptida muhim? `docker compose pull` xato bersa, usiz nima sodir bo'lishini izohlang.
10. Pull-based deploy (Watchtower/GitOps) push-based'dan nimasi bilan farq qiladi? Har biri qaysi holatda afzalroq?

### Qiyin

11. To'liq `Deploy` workflow yozing: `build` job image'ni `ghcr.io/.../vazifalar-api:sha-<sha>` tegi bilan push qilsin; `deploy-staging` faqat `push: main`'da, `deploy-production` faqat `release`'da ishlasin; production `environment: production` ortida bo'lsin. SSH uchun `appleboy/ssh-action@v1.2.5` ishlating.
12. Serverda bajariladigan `deploy.sh` skript yozing: loyiha papkasiga o'tsin, `docker compose pull`, `docker compose up -d --remove-orphans`, so'ng `docker image prune -f` qilsin; xato bo'lsa darhol to'xtasin. `bash -n` bilan sintaksisini tekshiring.
13. `compose.yaml`'da image tegini muhit o'zgaruvchisidan oladigan qilib yozing (`${IMAGE_TAG:-latest}`) va shu asosda **rollback** ssenariysini tasvirlang: v2 qulasa, v1'ga qanday qaytasiz (aniq buyruqlar bilan)?
14. `workflow_dispatch` input bilan **qo'lda rollback** workflow'i loyihalashtiring: foydalanuvchi qaytmoqchi bo'lgan teg (`image_tag`) ni kiritsin, job serverga SSH qilib o'sha teg bilan `up -d` qilsin. Bu nega "ehtiyot tugmasi" sifatida foydali?
15. Deploy xavfsizligi bo'yicha alohida `deploy` user va alohida SSH kalit yaratish qadamlarini yozing (`ssh-keygen`, `authorized_keys`, GitHub secret). Nega shaxsiy kalitingizni emas, alohida kalit ishlatish kerak?

<details markdown="1"><summary>Yechim — 11</summary>

```yaml
name: Deploy

on:
  push:
    branches: [main]
  release:
    types: [published]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6
      - uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:sha-${{ github.sha }}

  deploy-staging:
    needs: build
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.vazifalar.uz
    steps:
      - uses: appleboy/ssh-action@v1.2.5
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            set -e
            cd /srv/vazifalar-api
            docker compose pull
            docker compose up -d --remove-orphans

  deploy-production:
    needs: build
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://vazifalar.uz
    steps:
      - uses: appleboy/ssh-action@v1.2.5
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            set -e
            cd /srv/vazifalar-api
            docker compose pull
            docker compose up -d --remove-orphans
```

`production` uchun GitHub'da (`Settings -> Environments -> production`) Required reviewers yoqilgan bo'lishi shart — shunda `deploy-production` job tasdiq kutib turadi. Build bir marta ishlaydi, ikkala deploy ham o'sha `sha-<sha>` tegidan foydalanadi (immutable, takrorlanadigan).
</details>

<details markdown="1"><summary>Yechim — 12</summary>

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /srv/vazifalar-api

echo "1/3 Yangi image'ni tortish..."
docker compose pull

echo "2/3 Konteynerni qayta ko'tarish..."
docker compose up -d --remove-orphans

echo "3/3 Eski image'larni tozalash..."
docker image prune -f

echo "Deploy tugadi."
```

`set -euo pipefail` — xato (`-e`), e'lon qilinmagan o'zgaruvchi (`-u`) yoki pipe ichidagi xato (`pipefail`) bo'lsa skript darhol to'xtaydi; demak `pull` muvaffaqiyatsiz bo'lsa `up` umuman ishlamaydi. Sintaksis tekshiruvi: `bash -n deploy.sh` — xato bo'lmasa hech narsa chiqmaydi (toza chiqish = to'g'ri sintaksis).
</details>

<details markdown="1"><summary>Yechim — 13</summary>

`compose.yaml`:

```yaml
services:
  api:
    image: ghcr.io/foydalanuvchi/vazifalar-api:${IMAGE_TAG:-latest}
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:3000"
```

`${IMAGE_TAG:-latest}` — `IMAGE_TAG` muhit o'zgaruvchisi berilsa o'sha, aks holda `latest`.

**Rollback ssenariysi:** v2 (`sha-bbb2222`) deploy qildingiz, sayt qulaydi. Oldingi sog'lom versiya — v1 (`sha-aaa1111`). Serverda:

```bash
cd /srv/vazifalar-api
IMAGE_TAG=sha-aaa1111 docker compose pull
IMAGE_TAG=sha-aaa1111 docker compose up -d
```

Konteyner v1 image bilan qayta ko'tariladi, ilova tiklanadi. Bu bir necha soniyada bo'ladi, chunki `sha-aaa1111` image hali serverning lokal keshida (yoki registry'da o'zgarmasdan) turibdi — qayta build kutilmaydi. Keyin sokin holatda v2'dagi xatoni topib tuzatasiz.
</details>

<details markdown="1"><summary>Yechim — 14</summary>

```yaml
name: Rollback

on:
  workflow_dispatch:
    inputs:
      image_tag:
        description: "Qaytariladigan image teg (masalan sha-aaa1111 yoki v1.3.0)"
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - uses: appleboy/ssh-action@v1.2.5
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          envs: TAG
          script: |
            set -e
            cd /srv/vazifalar-api
            export TAG="${{ github.event.inputs.image_tag }}"
            IMAGE_TAG="$TAG" docker compose pull
            IMAGE_TAG="$TAG" docker compose up -d --remove-orphans
```

Foydalanuvchi Actions UI'da "Run workflow" bosib, qaytmoqchi bo'lgan tegni kiritadi. `environment: production` tufayli bu ham approval ortida bo'lishi mumkin. Bu — "ehtyot tugmasi": yangi build yoki kod o'zgartirmasdan, ma'lum, ishlaydigan versiyaga bir necha bosishda qaytaradi. Immutable teglar tufayli har bir eski versiya hali ham aniq, o'zgarmas image bo'lib registry'da turadi.
</details>

<details markdown="1"><summary>Yechim — 15</summary>

**1. Serverda alohida deploy user yaratish (root sifatida, bir marta):**

```bash
sudo adduser --disabled-password --gecos "" deploy
sudo usermod -aG docker deploy        # docker buyrug'iga ruxsat
sudo mkdir -p /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
```

**2. Lokal mashinada alohida kalit juftligi:**

```bash
ssh-keygen -t ed25519 -C "deploy-vazifalar-api" -f ./deploy_key
# Ikki fayl: deploy_key (maxfiy) va deploy_key.pub (ochiq)
```

**3. Ochiq kalitni serverga qo'shish:**

```bash
# deploy_key.pub matnini serverdagi /home/deploy/.ssh/authorized_keys ga qo'shing
sudo tee -a /home/deploy/.ssh/authorized_keys < deploy_key.pub
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys
```

**4. Maxfiy kalitni GitHub secret'ga:** `deploy_key` faylining to'liq matnini `DEPLOY_SSH_KEY` secret'iga joylang, `deploy_key` faylini lokaldan xavfsiz o'chiring.

**Nega shaxsiy kalit emas:** shaxsiy kalitingiz barcha serverlaringizga, GitHub'ga, boshqa joylarga kirish beradi — uni GitHub secret'iga qo'yish "hamma tuxumni bitta savatga" solishdir. Agar secret chiqib ketsa yoki workflow buzilsa, butun hayotingiz xavf ostida. Alohida deploy kalit esa **faqat bitta serverdagi cheklangan user**ga kirish beradi; chiqib ketsa, faqat o'shani bekor qilasiz, boshqa hech narsaga ta'sir qilmaydi (zarar chegaralanadi).
</details>

---

[⬅️ Oldingi: 14 — Docker image CI va GHCR](./14-docker-ci-ghcr.md) · [🏠 README](./README.md) · [Keyingi: 16 — Nginx asoslari ➡️](./16-nginx-asoslari.md)
