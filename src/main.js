(function () {
  "use strict";
  var io = "IntersectionObserver" in window;

  // 1. Forward traffic-source params (src, sck, utm_*) to every checkout link.
  var params = new URLSearchParams(location.search);
  var keep = ["src", "sck", "utm_source", "utm_medium", "utm_campaign", "utm_content"];
  document.querySelectorAll("a[data-checkout]").forEach(function (a) {
    try {
      var url = new URL(a.href);
      keep.forEach(function (k) { if (params.get(k)) url.searchParams.set(k, params.get(k)); });
      if (!url.searchParams.get("src")) url.searchParams.set("src", "salespage");
      a.href = url.toString();
    } catch (e) {}
    a.addEventListener("click", function () {
      if (window.fbq) window.fbq("track", "InitiateCheckout");
      if (window.gtag) window.gtag("event", "begin_checkout", { location: a.getAttribute("data-checkout") });
    });
  });

  // 2. Carousel: counter + arrows on top of native scroll-snap.
  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var track = root.querySelector(".track");
    var slides = track.children;
    var prev = root.querySelector("[data-prev]");
    var next = root.querySelector("[data-next]");
    var count = root.querySelector("[data-count]");
    var current = 0;
    function update() {
      var mid = track.scrollLeft + track.clientWidth / 2, best = 0, dist = Infinity;
      for (var i = 0; i < slides.length; i++) {
        var c = slides[i].offsetLeft + slides[i].offsetWidth / 2;
        if (Math.abs(c - mid) < dist) { dist = Math.abs(c - mid); best = i; }
      }
      current = best;
      count.textContent = (best + 1) + " / " + slides.length;
      prev.disabled = best === 0;
      next.disabled = best === slides.length - 1;
    }
    function go(i) {
      var s = slides[Math.max(0, Math.min(slides.length - 1, i))];
      track.scrollTo({ left: s.offsetLeft - (track.clientWidth - s.offsetWidth) / 2, behavior: "smooth" });
    }
    prev.addEventListener("click", function () { go(current - 1); });
    next.addEventListener("click", function () { go(current + 1); });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(current + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(current - 1); }
    });
    var t;
    track.addEventListener("scroll", function () { clearTimeout(t); t = setTimeout(update, 60); }, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  // 3. Jude × Enoch: draw the shared-word highlights when the block scrolls in.
  var col = document.querySelector(".collation");
  if (col) {
    if (!io) col.classList.add("in");
    else new IntersectionObserver(function (es, ob) {
      es.forEach(function (e) { if (e.isIntersecting) { col.classList.add("in"); ob.disconnect(); } });
    }, { threshold: 0.45 }).observe(col);
  }

  // 4. Sticky buy bar: show after the hero button leaves view, hide over the offer/final CTA.
  var bar = document.querySelector(".buybar");
  var heroCta = document.querySelector("[data-hero-cta]");
  if (bar && heroCta && io) {
    var heroGone = false, blockers = new Set();
    function paint() { bar.classList.toggle("show", heroGone && blockers.size === 0); bar.setAttribute("aria-hidden", bar.classList.contains("show") ? "false" : "true"); }
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { heroGone = !e.isIntersecting && e.boundingClientRect.top < 0; });
      paint();
    }).observe(heroCta);
    var hideObs = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) blockers.add(e.target); else blockers.delete(e.target); });
      paint();
    }, { rootMargin: "0px 0px -80px 0px" });
    document.querySelectorAll("[data-hide-bar]").forEach(function (el) { hideObs.observe(el); });
  }

  // 5. Email capture: post to the configured email tool without leaving the page.
  var form = document.querySelector("[data-lead-form]");
  if (form) {
    var status = form.querySelector(".status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var action = form.getAttribute("data-action");
      var btn = form.querySelector("button");
      status.className = "status"; status.textContent = "";
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (!action) {
        status.className = "status err";
        status.textContent = form.getAttribute("data-msg-unconfigured");
        return;
      }
      btn.disabled = true;
      var payload = {};
      new FormData(form).forEach(function (v, k) { payload[k] = v; });
      fetch(action, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          status.className = "status ok";
          status.textContent = form.getAttribute("data-msg-ok");
          form.querySelector("input[type=email]").value = "";
          if (window.fbq) window.fbq("track", "Lead");
          if (window.gtag) window.gtag("event", "generate_lead");
        })
        .catch(function () {
          status.className = "status err";
          status.textContent = form.getAttribute("data-msg-err");
        })
        .then(function () { btn.disabled = false; });
    });
  }
})();
