# DevOps — 0 dan Expertgacha (o'zbek tilida)

Bu kitob **bitta ilova yozishni biladigan** dasturchini (frontend yoki backend — farqi yo'q) shu ilovani **ishonchli, avtomatik va qayta-qayta** serverga chiqarib, kuzatib va boshqarib turadigan darajaga olib chiqadi. Linux serverdan boshlab — **Docker** konteynerlar, **GitHub Actions** bilan CI/CD, **Nginx** reverse proxy va HTTPS, **systemd**, **Kubernetes** orkestratsiyasi, **Prometheus + Grafana** monitoringi, **Ansible/Terraform** (Infrastructure as Code) orqali — yakuniy to'liq **DevOps platforma** kapstonigacha.

> 🛠️ **Zamonaviy stek (2026).** Kitob faqat **joriy** idiomdan foydalanadi: Docker Compose **v2** (`docker compose`, `compose.yaml` — eski `docker-compose` va `version:` kaliti emas), GitHub Actions **v6** action'lari (`actions/checkout@v6`), Ubuntu **26.04 LTS**, Kubernetes **1.3x**, Prometheus **3.x**, Grafana **12.x**. Internetdagi eski qo'llanmalardagi `docker-compose up`, `version: "3"`, `checkout@v2` kabilar **eskirgan** — kitobda ular faqat ❌ "eski usul" sifatida ko'rsatiladi.

> ⚠️ **HALOL eslatma.** Kitobdagi **konfiguratsiya va kod** — Dockerfile'lar, `compose.yaml` fayllari, GitHub Actions workflow'lari, Nginx config'lari, Bash skriptlari va Kubernetes manifestlari — **lokal mashinada haqiqatan ishga tushirib tekshirilgan**: Dockerfile'lar `docker build` + `docker run` bilan qurilgan, compose fayllari `docker compose config` bilan, Nginx config'lari `nginx -t` bilan, Bash `bash -n` bilan, YAML `yamllint` bilan tasdiqlangan. Ammo **jonli infratuzilma** — real VPS'da `apt`/`ufw`/`systemctl`, Certbot bilan haqiqiy domenga sertifikat, SSH orqali deploy, jonli Kubernetes klaster, cloud resurslari va Grafana dashboard'lari — **server, domen yoki cloud hisobi** talab qiladi; bu bloklar to'g'ri, lekin matnda **"illustrativ"** deb belgilangan. Ularni o'z serveringizda ishga tushiring.

> ℹ️ Bu kitob siz **bitta dasturlash tilida ilova yoza olasiz** (Node.js, Python/Django, PHP/Laravel — bari mos) va **terminal** hamda **Git** bilan tanish deb hisoblaydi. Git yangi bo'lsa, avval [Git & GitHub — 0 dan Expertgacha](../git-github/README.md) kitobini o'qing (CI/CD qismi shunga tayanadi).

---

## Bu kitob nimaga o'rgatadi?

Tasavvur qiling: ilovangiz lokalda zo'r ishlaydi, lekin serverga chiqarish — har safar qo'rqinchli marosim. Qo'lda fayl ko'chirish, "menda ishlaydi-ku" muammosi, tushib qolgan sayt, yo'qolgan ma'lumot. **DevOps** — aynan shu og'riqni yo'qotadi: ishlab chiqish (Dev) va ishlatish (Ops) o'rtasidagi devorni buzib, hamma narsani **avtomatik, takrorlanadigan va kuzatiladigan** qiladi.

Kitob oxirida siz: ilovani **konteynerga** joylaysiz, har `git push`'da **avtomatik test+build+deploy** qilasiz, uni **Nginx + HTTPS** ortida ishlatasiz, **Kubernetes**'da masshtablaysiz, **Prometheus/Grafana** bilan kuzatasiz va **Ansible/Terraform** bilan butun serverni koddan tiklaysiz.

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 → 02 → ...). Har biri oldingisiga tayanadi.
2. Har bir buyruq va konfiguratsiyani **o'zingiz tering va ishga tushiring** — DevOps faqat amaliyot bilan o'rganiladi.
3. Bitta **arzon VPS** (yoki lokal virtual mashina) oling — kitobning yarmidan ko'pi real serverda mashq qilishni talab qiladi. Cloud provayderlar yangi hisob uchun bepul kredit beradi.
4. Docker'ni lokal kompyuteringizga o'rnating ([Docker Desktop](https://www.docker.com/products/docker-desktop/) yoki Linux'da Docker Engine) — 06-bobdan boshlab kerak bo'ladi.

## Talab

| Kerak | Daraja |
|---|---|
| Bitta tilda ilova yoza olish (Node/Python/PHP) | **Shart** |
| Terminal va Git bilan tanishlik | **Shart** |
| Linux asoslari (fayl, papka, buyruq) | Foydali (02-bobda qaytariladi) |
| Arzon VPS yoki lokal virtual mashina | Amaliyot uchun shart |
| Cloud hisobi (kapston/IaC uchun) | Foydali |

---

## Mundarija

### I qism — DevOps va Linux poydevori

| # | Bob | Mavzu |
|---|---|---|
| 01 | [DevOps nima va nega kerak](./01-devops-nima.md) | Dev↔Ops devori, DevOps madaniyati, CALMS, CI/CD/IaC/monitoring tushunchalari, SRE, kitob xaritasi. |
| 02 | [Linux server asoslari](./02-linux-server-asoslari.md) | SSH bilan ulanish, fayl tizimi, foydalanuvchi/guruh, ruxsatlar (`chmod`/`chown`), paketlar (`apt`), `systemctl` asos. |
| 03 | [Bash skripting va avtomatlashtirish](./03-bash-skripting.md) | O'zgaruvchi/shart/sikl/funksiya, argument, exit code, quvur (pipe), `cron` bilan rejalashtirilgan vazifa. |
| 04 | [Tarmoq va server xavfsizligi](./04-tarmoq-xavfsizlik.md) | IP/port/DNS/HTTP(S), `ufw` firewall, SSH kalit autentifikatsiya, root'ni o'chirish, `fail2ban`, server hardening. |
| 05 | [Ilovani qo'lda serverga joylash](./05-qolda-deploy.md) | Real ilovani VPS'da qo'lda ishga tushirish — va nega bu yo'l og'riqli (keyingi boblar uchun motivatsiya). |

### II qism — Konteynerlar: Docker

| # | Bob | Mavzu |
|---|---|---|
| 06 | [Docker nima: konteynerlar](./06-docker-nima.md) | Konteyner vs virtual mashina, image/container/registry, "menda ishlaydi" muammosini Docker qanday yechadi. |
| 07 | [Konteyner bilan ishlash](./07-konteyner-ishlash.md) | `docker run`/`ps`/`logs`/`exec`/`stop`/`rm`, port chiqarish (`-p`), environment (`-e`), interaktiv rejim. |
| 08 | [Dockerfile: o'z image'ingiz](./08-dockerfile.md) | `FROM`/`RUN`/`COPY`/`WORKDIR`/`CMD`/`ENTRYPOINT`, qatlamlar (layers), `.dockerignore`, build kesh. |
| 09 | [Image optimizatsiya va registry](./09-image-optimizatsiya.md) | Multi-stage build, kichik base (alpine/distroless), kesh tartibi, tag, Docker Hub va GHCR'ga `push`. |
| 10 | [Volume va Docker tarmog'i](./10-volume-network.md) | Persistent ma'lumot (named volume / bind mount), `docker network`, konteynerlararo DNS bilan aloqa. |
| 11 | [Docker Compose](./11-docker-compose.md) | Ko'p-servisli ilova (`web`+`db`+`cache`) bitta `compose.yaml`'da, `.env`, `depends_on`, `healthcheck`, profillar. |

### III qism — CI/CD: avtomatlashtirish

| # | Bob | Mavzu |
|---|---|---|
| 12 | [CI/CD va GitHub Actions asoslari](./12-cicd-github-actions.md) | CI/CD nima, workflow anatomiyasi (`on`/`jobs`/`steps`/`uses`/`run`), runner, birinchi pipeline. |
| 13 | [Test va build pipeline](./13-pipeline-test-build.md) | Lint+test avtomatlashtirish, `matrix` (ko'p versiya), kesh (`actions/cache@v5`), artifact, status badge, branch himoyasi. |
| 14 | [Docker image CI va GHCR](./14-docker-ci-ghcr.md) | Image'ni Actions'da qurib GHCR'ga `push`, `secrets`, `docker/build-push-action@v7`, tag strategiyasi (sha/semver), Trivy bilan zaiflik skani. |
| 15 | [Avtomatik deploy](./15-avtomatik-deploy.md) | SSH orqali serverga avtomatik deploy, `environments`, qo'lda tasdiq (approval), rollback, deploy-on-tag. |

### IV qism — Nginx, HTTPS va deploy

| # | Bob | Mavzu |
|---|---|---|
| 16 | [Nginx asoslari](./16-nginx-asoslari.md) | O'rnatish, server block, static fayl, `location`, log, konfiguratsiya tuzilishi, `nginx -t` va reload. |
| 17 | [Reverse proxy va load balancing](./17-reverse-proxy-load-balancing.md) | `proxy_pass`, `upstream`, ilova oldida Nginx, `gzip`, kesh, WebSocket, bir nechta instansga yuk taqsimlash. |
| 18 | [HTTPS, domen va Let's Encrypt](./18-https-domen.md) | DNS yo'naltirish, Let's Encrypt/Certbot bilan bepul sertifikat, TLS sozlash, HTTP→HTTPS, avtomatik yangilash. |
| 19 | [systemd va process boshqaruvi](./19-systemd-process.md) | `systemd` service unit, `restart` siyosati, `journald` log, ilovani demonlashtirish, konteynersiz xizmat. |
| 20 | [To'liq production deploy](./20-toliq-deploy.md) | Compose + Nginx reverse proxy + HTTPS + domen — real ilovani noldan production'ga chiqarish, zero-downtime asoslari. |

### V qism — Kubernetes va orkestratsiya

| # | Bob | Mavzu |
|---|---|---|
| 21 | [Nega Kubernetes: arxitektura va lokal klaster](./21-kubernetes-nima.md) | Orkestratsiya muammosi, K8s arxitekturasi (control plane, node, kubelet, etcd), `kubectl`, `minikube`/`kind` bilan lokal klaster. |
| 22 | [Pod, Deployment, Service](./22-pod-deployment-service.md) | Pod, ReplicaSet, Deployment, Service (ClusterIP/NodePort/LoadBalancer), YAML manifest, `ConfigMap`/`Secret`, label/selector. |
| 23 | [Production Kubernetes](./23-production-k8s.md) | Rolling update va rollback, liveness/readiness probe, resource requests/limits, namespace, horizontal autoscaling (HPA). |
| 24 | [Ingress, storage, Helm va GitOps](./24-ingress-helm-gitops.md) | Ingress controller (nginx) + TLS, persistent storage (PV/PVC, StatefulSet kirish), Helm chart, GitOps (Argo CD kirish), managed K8s (cloud). |

### VI qism — Monitoring, IaC va kapston

| # | Bob | Mavzu |
|---|---|---|
| 25 | [Monitoring: Prometheus va Grafana](./25-monitoring-prometheus-grafana.md) | Metrika turlari, Prometheus + `node_exporter` + cAdvisor, PromQL asoslari, Grafana dashboard, Compose bilan monitoring stek. |
| 26 | [Logging, alerting, backup va ishonchlilik](./26-logging-alerting-backup.md) | Markazlashtirilgan log (journald/Loki/`logrotate`), Alertmanager, healthcheck/uptime, SLI/SLO/error budget, DB va volume backup + restore. |
| 27 | [Infrastructure as Code: Ansible va Terraform](./27-iac-ansible-terraform.md) | IaC nima, Ansible bilan server tayyorlash (idempotentlik, playbook), Terraform bilan cloud resurs (`plan`/`apply`/state), immutable infratuzilma. |
| 28 | [Yakuniy kapston: to'liq DevOps platforma](./28-kapston.md) | Boshidan oxirigacha: kod → GitHub Actions CI → image → GHCR → Kubernetes deploy → Ingress+HTTPS → Prometheus/Grafana → backup; runbook va post-mortem. Yo'l yakuni. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
