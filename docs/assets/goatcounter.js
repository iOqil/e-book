/* ======================================================================
   GoatCounter — sahifa ko'rishlari statistikasi
   ----------------------------------------------------------------------
   • Bepul, maxfiylikka do'st (cookie yo'q, rozilik banneri SHART EMAS).
   • MkDocs Material "navigation.instant" bilan ishlaydi: har sahifa
     o'tishida qo'lda sanaydi (aks holda faqat birinchi sahifa sanaladi).
   • Footerga jonli hisoblagich qo'yadi: ko'rish + tashrifchi soni.

   >>> SOZLASH (faqat 1 qadam):
   1. https://www.goatcounter.com da bepul ro'yxatdan o'ting va "code"
      tanlang (masalan: oqil-ebooks  ->  oqil-ebooks.goatcounter.com).
   2. Pastdagi GC qatorini o'z kodingiz bilan almashtiring.
   3. GoatCounter sozlamalarida (Settings) "Allow adding visitor counts
      to other websites" (visitor counter) ni YOQING — footer raqami
      shu orqali olinadi.
   ====================================================================== */

(function () {
  // ====== O'Z GOATCOUNTER MANZILINGIZNI shu yerga yozing ======
  var GC = "https://oqil-e-book.goatcounter.com";
  // ============================================================

  // Avtomatik sanashni o'chiramiz — SPA navigatsiya uchun qo'lda chaqiramiz.
  window.goatcounter = window.goatcounter || {};
  window.goatcounter.no_onload = true;

  // count.js skriptini data-goatcounter atributi bilan yuklaymiz.
  if (!document.querySelector("script[data-goatcounter]")) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "//gc.zgo.at/count.js";
    s.setAttribute("data-goatcounter", GC + "/count");
    document.head.appendChild(s);
  }

  // Bitta sahifa ko'rishini sanash. count.js hali yuklanmagan bo'lsa kutadi.
  function countView(path) {
    path = path || location.pathname + location.search + location.hash;
    if (window.goatcounter && typeof window.goatcounter.count === "function") {
      window.goatcounter.count({ path: path });
    } else {
      setTimeout(function () { countView(path); }, 400);
    }
  }

  // Sonni "1 234 567" ko'rinishida formatlash.
  function fmt(n) {
    return (Number(n) || 0).toLocaleString("en-US").replace(/,/g, " ");
  }

  // Footerga umumiy ko'rish/tashrifchi sonini qo'yish.
  function showFooter() {
    var holder = document.querySelector(".md-copyright");
    if (!holder) return;
    fetch(GC + "/counter/TOTAL.json")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d) return;
        var el = holder.querySelector(".gc-views");
        if (!el) {
          el = document.createElement("span");
          el.className = "gc-views";
          holder.appendChild(el);
        }
        var views = "👁 " + fmt(d.count) + " ko'rish";
        var uniq = d.count_unique ? " · " + fmt(d.count_unique) + " tashrifchi" : "";
        el.textContent = views + uniq;
        el.title = "Jami sahifa ko'rishlari va noyob tashrifchilar · GoatCounter";
      })
      .catch(function () { /* statistika yuklanmasa — jim qolamiz */ });
  }

  function run() {
    countView();
    showFooter();
  }

  // Material instant navigation: document$ har sahifa o'tishida signal beradi.
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else if (document.readyState !== "loading") {
    run();
  } else {
    document.addEventListener("DOMContentLoaded", run);
  }
})();
