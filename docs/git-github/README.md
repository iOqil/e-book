# Git va GitHub — Noldan boshlovchilar uchun amaliy kitob

Bu kitob **hech qachon versiya nazorati ishlatmagan** odam ham tushunadigan tilda yozilgan. Git'ni terminal qora oynasidan qo'rqmasdan, GitHub'ni esa "tugmalar o'rmoni"dek emas, mantiqan tushunib o'rganasiz. Har bobda: sodda nazariya -> tayyor, sinab tekshirilgan buyruqlar -> **20 ta mashq** (o'zingiz bajarasiz). Jami 24 bob, 480 mashq.

> 🎨 Har bob **SVG diagrammalar** bilan boyitilgan — uch zona, branch, merge va rebase, remote/push/pull, PR oqimi kabi tushunchalar ko'z bilan ko'rib o'rganiladi.

> **Qoida:** Git o'qib o'rganilmaydi — **YOZIB** o'rganiladi. Har bir buyruqni kompyuterda o'zingiz tering. Xato chiqsa — bu yaxshi, xatodan o'rganasiz (bu kitob xatodan qaytishni ham o'rgatadi).

---

## Qanday o'qish kerak

1. Boblarni **tartib bilan** o'qing (01 -> 02 -> ...). Har biri oldingisiga tayanadi.
2. 2-bobda Git'ni o'rnatib, o'zingizni tanishtiring (`user.name`, `user.email`) — keyingi hamma bob shunga asoslangan.
3. Har bob oxiridagi **20 ta mashqni** o'zingiz bajaring — buyruqlarni ko'chirib qo'yish bilan Git o'rganilmaydi.
4. Diagrammalar tushunchani tezroq singdiradi — ularga e'tibor bering.

## Talab

| Kerak | Daraja |
|---|---|
| Kompyuter (Windows / macOS / Linux) | Shart |
| Git (2-bobda o'rnatamiz) | Shart |
| GitHub akkaunti (10-bobda ochamiz, bepul) | Shart |
| Oldingi dasturlash tajribasi | **Shart emas** |

---

## I qism — Git asoslari

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 01 | [Versiya nazorati nima?](./01-versiya-nazorati-nima.md) | Fayllarni `loyiha_final_v2.zip` deb saqlash og'rig'idan boshlab, versiya nazorati (loyiha uchun "vaqt mashinasi") nima ekanini, snapshot modelini, markazlashgan va taqsimlangan tizimlar farqini, eng muhimi — ko'pchilik chalkashtiradigan **Git va GitHub** farqini aniq ajratamiz. |
| 02 | [Git'ni o'rnatish va sozlash](./02-git-ornatish-sozlash.md) | Git'ni har uch tizimga o'rnatamiz, terminaldan qo'rqmaslikni va kerakli buyruqlarni (`pwd`, `cd`, `ls`) o'rganamiz, Git'ga o'zimizni tanishtiramiz (`user.name`, `user.email`), config'ning uch darajasini (system/global/local), default branch'ni `main` qilishni va alias yasashni ko'rib chiqamiz. |
| 03 | [Birinchi repozitoriy va uch zona](./03-birinchi-repozitoriy.md) | Oddiy papkani `git init` bilan repozitoriyga aylantirishni, yashirin `.git` katalogini, butun kitobning eng muhim modeli — **uch zona**ni (Working Directory, Staging Area, Repository), faylning hayot siklini (untracked -> staged -> committed -> modified) va `git status`ni o'qishni o'rganamiz. |
| 04 | [O'zgarishlarni saqlash: add va commit](./04-add-commit.md) | O'zgarishlarni tarixga muhrlashning ikki qadamini — `git add` (staging'ga qo'yish) va `git commit` (surat olish)ni, nega ikki bosqich kerakligini, yaxshi commit xabarini, `.gitignore` bilan keraksiz fayllarni chetlatishni hamda `git rm`, `git mv`, `git diff --staged`ni o'rganamiz. |
| 05 | [Tarixni o'qish: log, diff, show](./05-tarix-log-diff.md) | Commit tarixini o'qishni: `git log` variantlari (`--oneline`, `--graph`, `--stat`, `--author`), bitta commit nimadan tuzilganini (hash, parent, tree, muallif), `HEAD` ko'rsatkichini, `git show`ni va `git diff`ning uch turini bir-biridan ajratishni o'rganamiz. |
| 06 | [Orqaga qaytish: restore, reset, revert](./06-orqaga-qaytish.md) | Xato qilganda orqaga qaytishni: `git restore` (working zonani tozalash), `git restore --staged`, `git reset`ning uch turi (`--soft`/`--mixed`/`--hard`) va ularning uch zonaga ta'siri, ulashilgan tarixni xavfsiz bekor qiluvchi `git revert` va `git commit --amend`ni o'rganamiz. |

## II qism — Branch va birlashtirish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 07 | [Branch — shoxlar](./07-branch.md) | Asosiy kodni buzmasdan yangi xususiyat sinash uchun branch (shox)ni: branch aslida arzon ko'rsatkich ekanini, `git branch`, `git switch`/`git switch -c`, HEAD nima ekanini, shoxlar ajralib ketishini (divergence), `-d/-D/-m` bilan o'chirish/nomlashni va "detached HEAD" holatini o'rganamiz. |
| 08 | [Merge va konfliktlar](./08-merge-konflikt.md) | Tayyor ishni asosiy shoxga qaytadan qo'shishni — merge'ni: fast-forward va 3-way merge farqini, `--no-ff` bayrog'ini, KONFLIKT hodisasini, konflikt markerlarini o'qib qo'lda hal qilishni va `git merge --abort` bilan ortga qaytishni qadam-baqadam o'rganamiz. |
| 09 | [Rebase va interaktiv rebase](./09-rebase.md) | Chigal tarixni toza chiziqli tarixga aylantiradigan `git rebase`ni: commitlarni "qayta o'ynashni", merge bilan farqini, **OLTIN QOIDA** (ulashilgan commitni rebase qilmaslik)ni, `git rebase -i` bilan squash/reword/drop'ni, konfliktni `--continue`/`--abort` bilan boshqarishni va `git pull --rebase`ni o'rganamiz. |

## III qism — GitHub bilan ishlash

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 10 | [GitHub bilan tanishuv](./10-github-tanishuv.md) | Lokal repo nega yetarli emasligini, GitHub aslida nimaligini, bepul akkaunt ochish va profilni to'ldirishni, birinchi repozitoriy yaratishni (public/private, README/gitignore/license), "remote" va `origin` tushunchasini, repo sahifasi anatomiyasini, README "loyiha yuzi" ekanini, Star/Fork/Watch'ni va GitHub/GitLab/Bitbucket farqini o'rganamiz. |
| 11 | [Remote: clone, push, fetch, pull](./11-remote-push-pull.md) | Lokal Git'ni GitHub repozitoriysi bilan bog'lashni: `git clone`, `git remote add origin`, `git push`, `git fetch` (xavfsiz olish) va `git pull` (fetch+merge)ni, eng muhimi **fetch va pull farqi** hamda **push rad etilganda** nima qilishni, `origin/main` tracking branch va HTTPS/SSH url farqini o'rganamiz. |
| 12 | [Autentifikatsiya: SSH va token](./12-autentifikatsiya-ssh.md) | GitHub sizdan kimligingizni qanday so'rashini va nega oddiy parol ishlamasligini: HTTPS + Personal Access Token (PAT) va SSH kalit yo'llarini, `ssh-keygen`, ochiq kalitni qo'yish, `ssh -T` bilan tekshirish, credential helper, `git remote set-url` va 2FA hamda sirni hech qachon commit qilmaslikni o'rganamiz. |
| 13 | [Pull Request va code review](./13-pull-request.md) | Nega to'g'ridan-to'g'ri `main`'ga push xavfli ekanini va yechimi — Pull Request'ni: o'z repoda PR oqimini (branch -> push -> PR -> merge) va begona loyiha uchun fork modelini, reviewer/izoh/Approve jarayonini, uch xil merge usuli farqini, Draft PR va branch protection'ni o'rganamiz. |
| 14 | [Hamkorlik oqimlari: Git Flow, GitHub Flow](./14-hamkorlik-oqimlari.md) | Branch va PR'ni jamoa uchun bitta tartibga — oqimga bog'lashni: GitHub Flow, Git Flow va trunk-based oqimlarini, qaysi birini qachon tanlashni, branch nomlash (`feature/login`), Conventional Commits (`feat:`, `fix:`), main'ni himoyalash va hotfix ssenariysini o'rganamiz. |

## IV qism — Kuchli vositalar

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 15 | [Stash, tag va cherry-pick](./15-stash-tag-cherry-pick.md) | Uchta "qutqaruvchi" buyruqni: `git stash` (yarim ishni vaqtincha javonga qo'yish), `git tag` (relizni `v1.0.0` bilan belgilash, lightweight/annotated farqi, semantik versiyalash, GitHub Releases) va `git cherry-pick` (bittagina commitni boshqa branchga ko'chirish)ni o'rganamiz. |
| 16 | [Tarixni tozalash va reflog](./16-tarixni-tozalash-reflog.md) | Tarixni chiroyli qilish va "hammasini yo'qotdim!" holatidan qutqarishni: `git commit --amend`, interaktiv rebase bilan squash/reword/reorder/drop, `git push --force-with-lease` xavfsiz majburlashni, `git reflog` bilan o'chgan commit/branch'ni tiklashni, `git fsck`ni va **tozalashning oltin qoidasi**ni o'rganamiz. |
| 17 | [Xatoni qidirish: bisect, blame, grep](./17-bisect-blame.md) | "Ilgari ishlardi, endi buzilgan — qaysi commit buzdi?" savoliga javob topishni: `git bisect` (ikkilik qidiruv) va `bisect run`, `git blame` (har satrni kim/qachon yozgani), `git log -S`/`-G` (pickaxe) va `git log --grep` bilan aybdor commitni topishni o'rganamiz. |
| 18 | [Submodule, Git LFS va monorepo](./18-submodule-lfs.md) | Loyiha o'sgani sayin uchraydigan uchta muammoni: boshqa repoga bog'liqlik (submodule, `.gitmodules`), katta binar fayllar (Git LFS, `.gitattributes`) va bitta repoda ko'p loyiha (monorepo/polyrepo, `git subtree`)ni — hammasi alohida sinov papkasida tekshirilgan — o'rganamiz. |

## V qism — Jamoa va avtomatlashtirish

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 19 | [GitHub vositalari: Issues, Projects](./19-github-issues-projects.md) | Jamoa ishini boshqarishni: Issues (xato/vazifa kartochkalari) va hayot sikli, label/milestone/assignee, commit/PR orqali issue'ni avtomatik yopish (`Closes #12`), GitHub Projects kanban doskasi, `.github/` shablonlari va `gh` (GitHub CLI) bilan ishlashni o'rganamiz. |
| 20 | [GitHub Actions — CI/CD](./20-github-actions.md) | Qo'lda test/deploy zerikarli ekanidan boshlab CI/CD nimaligini, GitHub Actions ishlashini — `.github/workflows` yaml anatomiyasini (`on`, `jobs`, `steps`, `uses`, `run`, `runs-on`), Node/Python testlarini matrix bilan avtomatlashtirishni, secret, status badge, deploy va cache'ni o'rganamiz. |
| 21 | [Open source'ga hissa qo'shish](./21-open-source.md) | Ochiq kod dunyosini: sog'lom repozitoriy fayllarini (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT), litsenziyalar farqini (MIT/Apache/GPL), birinchi hissa oqimini (good first issue -> fork -> branch -> PR -> merge), upstream bilan sinxron tutishni, maintainer odobi va semver/CHANGELOG'ni o'rganamiz. |
| 22 | [GitHub Pages va portfolio](./22-github-pages-portfolio.md) | Kodingizni dunyoga ko'rsatishni: GitHub Pages bilan bepul jonli sayt (ikki turi — `username.github.io` va loyiha sayti), saytni yoqish, URL tuzilishi, custom domen, Jekyll va Actions orqali deploy, hamda profil README, badge'lar va pin qilingan repolar bilan portfolio yasashni o'rganamiz. |

## VI qism — Xavfsizlik va yakun

| # | Bob | Nima o'rganasiz |
|---|---|---|
| 23 | [Xavfsizlik va eng yaxshi amaliyotlar](./23-xavfsizlik-amaliyot.md) | Git/GitHub'ni xavfsiz ishlatishni: sirni (parol, `.env`) hech qachon commit qilmaslik (va tushib qolsa rotate qilish), imzolangan commit va **Verified** belgisi (SSH/GPG), 2FA, branch protection, GitHub xavfsizlik vositalari (Dependabot, secret scanning, CodeQL), minimal ruxsat va `--force-with-lease`ni o'rganamiz. |
| 24 | [Yakuniy loyiha va shpargalka](./24-yakuniy-loyiha.md) | O'rgangan hamma narsani bitta loyihada birlashtirib jamoa ishini boshidan oxirigacha simulyatsiya qilamiz (init -> commit -> push -> branch -> PR -> review -> merge -> tag -> Pages deploy), vahimali vaziyatlarni tinch hal qilamiz, to'liq buyruq shpargalkasini bitta jadvalda yig'amiz va keyingi yo'lni belgilaymiz. |

---

## Muallif

**Oqil Imomnazarov** — [ioqil.uz](https://ioqil.uz) · [Telegram](https://t.me/i_oqil) · [YouTube](https://www.youtube.com/@I_Oqil)

Kitob bepul tarqatiladi (CC BY-NC-SA 4.0). Savdo qilish taqiqlanadi.
