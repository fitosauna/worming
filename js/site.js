/* Worming — site behaviour. No dependencies. */
(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Content binding: one editable data file ---------- */
  var LV = doc.lang === 'lv';
  fetch(LV ? '../content/site.lv.json' : 'content/site.json').then(function (r) { return r.json(); }).then(function (d) {
    document.querySelectorAll('[data-k]').forEach(function (el) {
      var v = el.getAttribute('data-k').split('.').reduce(function (o, k) { return o && o[k]; }, d);
      if (typeof v === 'string') {
        el.textContent = v;
        if (/^(to be confirmed|tiks precizēts)/i.test(v)) el.classList.add('tbc');
      }
    });
  }).catch(function () {});

  /* ---------- Mobile menu ---------- */
  var btn = document.querySelector('.menu-btn');
  var menu = document.getElementById('menu');
  function setMenu(open) {
    doc.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.querySelector('.menu-btn__t').textContent = open ? (LV ? 'Aizvērt' : 'Close') : (LV ? 'Izvēlne' : 'Menu');
    menu.inert = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (btn && menu) {
    menu.inert = true;
    btn.addEventListener('click', function () { setMenu(!doc.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && doc.classList.contains('menu-open')) { setMenu(false); btn.focus(); } });
  }

  /* ---------- Hero: the surface line ---------- */
  var hero = document.querySelector('.hero');
  var stage = document.querySelector('.hero__stage');
  var clip = document.getElementById('soil-clip-path');
  var line = document.getElementById('surface-line');
  var under = document.querySelector('.hero__under');
  var s0 = stage ? parseFloat(getComputedStyle(stage).getPropertyValue('--s0')) || 0.52 : 0.52;
  var surface = s0, pointer = 0, pointerT = 0, t0 = performance.now();

  function drawSurface(y, now) {
    var breathe = reduce ? 0 : Math.sin((now - t0) / 2600) * 0.004;
    var a = 0.022 + breathe, tilt = pointer * 0.012;
    var y0 = y + a * 0.6 - tilt, y1 = y - a * 0.9 + tilt;
    var c1 = y - a * 1.5 - tilt * 0.4, c2 = y + a * 1.7 + tilt * 0.4;
    var curve = 'M0,' + y0.toFixed(4) + ' C0.3,' + c1.toFixed(4) + ' 0.62,' + c2.toFixed(4) + ' 1,' + y1.toFixed(4);
    clip.setAttribute('d', curve + ' L1,1.2 L0,1.2 Z');
    line.setAttribute('d', curve);
  }

  /* ---------- Themes under header / gauge ---------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-theme]'));
  var gauge = document.querySelector('.gauge');
  var gaugeVal = document.querySelector('.gauge__val');
  function themeAt(y) {
    if (hero) {
      var hr = hero.getBoundingClientRect();
      if (hr.bottom > y) { var sr = stage.getBoundingClientRect(); return (y - sr.top) > surface * sr.height ? 'dark' : 'light'; }
    }
    for (var i = 0; i < sections.length; i++) {
      var r = sections[i].getBoundingClientRect();
      if (r.top <= y && r.bottom > y) return sections[i].getAttribute('data-theme');
    }
    return 'dark';
  }

  var lastY = 0, journey = document.getElementById('journey');
  function onScroll() {
    var vh = window.innerHeight, sy = window.scrollY;
    var pastHero = hero ? hero.getBoundingClientRect().bottom < 60 : (sy > 40 || doc.hasAttribute('data-solid'));
    doc.setAttribute('data-bar', pastHero ? 'solid' : 'clear');
    doc.setAttribute('data-hide', pastHero && sy > lastY + 2 ? '1' : (sy < lastY - 2 || !pastHero ? '0' : doc.getAttribute('data-hide') || '0'));
    lastY = sy;
    if (hero && !reduce) {
      var p = Math.min(1, Math.max(0, window.scrollY / (hero.offsetHeight - vh)));
      var e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      surface = s0 + (-0.08 - s0) * e;
      if (under) under.style.opacity = Math.max(0, (p - 0.55) / 0.3).toFixed(2);
    }
    doc.setAttribute('data-head', themeAt(34));
    doc.setAttribute('data-mid', themeAt(vh / 2));
    if (journey) { var jr = journey.getBoundingClientRect(); journey.style.setProperty('--jp', Math.min(1, Math.max(0, (vh * 0.6 - jr.top) / jr.height)).toFixed(3)); }
    var total = document.documentElement.scrollHeight - vh;
    var gp = total > 0 ? Math.min(1, window.scrollY / total) : 0;
    if (gauge) {
      gauge.style.setProperty('--p', gp.toFixed(3));
      gaugeVal.textContent = (gp === 0 ? '0' : '−' + Math.round(gp * 30)) + ' cm';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () {
    if (stage) s0 = parseFloat(getComputedStyle(stage).getPropertyValue('--s0')) || s0; onScroll();
  });
  window.addEventListener('pointermove', function (e) {
    if (e.pointerType === 'mouse') pointerT = (e.clientX / window.innerWidth) * 2 - 1;
  }, { passive: true });

  function frame(now) {
    pointer += (pointerT - pointer) * 0.05;
    if (stage && stage.getBoundingClientRect().bottom > 0) drawSurface(surface, now);
    if (!reduce) requestAnimationFrame(frame);
  }
  onScroll();
  if (stage) { drawSurface(surface, t0); if (!reduce) requestAnimationFrame(frame); }

  /* ---------- About: roots scene ---------- */
  var roots = document.querySelector('.roots');
  if (roots && !reduce && 'CSS' in window && CSS.supports('clip-path', 'url(#a)')) {
    roots.classList.add('roots--live');
    var rc1 = document.getElementById('rc1p'), rc2 = document.getElementById('rc2p');
    var plate = roots.querySelector('.roots__plate');
    var wave = function (el, t) {
      t = Math.min(1, Math.max(0, t)); var e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      var y = 1.12 - e * 1.24;
      el.setAttribute('d', 'M0,' + (y + 0.02).toFixed(4) + ' C0.3,' + (y - 0.035).toFixed(4) + ' 0.62,' + (y + 0.04).toFixed(4) + ' 1,' + (y - 0.02).toFixed(4) + ' L1,1.4 L0,1.4 Z');
    };
    var rootsScroll = function () {
      var p = (window.scrollY - roots.offsetTop) / (roots.offsetHeight - window.innerHeight);
      wave(rc1, (p - 0.1) / 0.34); wave(rc2, (p - 0.56) / 0.34);
      if (plate) { var o = Math.min(1, Math.max(0, 1 - (p - 0.03) / 0.09)); plate.style.opacity = o.toFixed(2); plate.style.visibility = o === 0 ? 'hidden' : 'visible'; }
    };
    window.addEventListener('scroll', rootsScroll, { passive: true });
    window.addEventListener('resize', rootsScroll);
    rootsScroll();
  }

  /* ---------- Applications explorer ---------- */
  var appItems = Array.prototype.slice.call(document.querySelectorAll('.apps li'));
  function activate(li) { appItems.forEach(function (x) { x.classList.toggle('is-active', x === li); }); }
  if (appItems.length && (reduce || !('IntersectionObserver' in window))) appItems.forEach(function (li) { li.classList.add('seen'); });
  if (appItems.length) {
    var wide = window.matchMedia('(min-width: 62rem)');
    appItems.forEach(function (li) {
      li.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') activate(li); });
      li.addEventListener('focusin', function () { activate(li); });
    });
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('seen'); io.unobserve(en.target); } });
      }, { rootMargin: '0px 0px -22% 0px', threshold: 0.35 });
      appItems.forEach(function (li) { io.observe(li); });
    }
  }

  /* ---------- Reveal ---------- */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var ro = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -12% 0px' });
    rv.forEach(function (el) { ro.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }
})();

/* Compare: with / without, split by a living surface line */
(function () {
  var st = document.getElementById('compare'); if (!st) return;
  var top = st.querySelector('.cmp__top'), path = st.querySelector('.cmp__line path'), knob = st.querySelector('.cmp__knob'), range = st.querySelector('.cmp__range');
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pos = 50, touched = false, N = 28;
  function draw() {
    var pts = [], d = '', mid = pos, r = st.getBoundingClientRect(), amp = calm ? 0 : Math.min(1.5, 900 / Math.max(r.width, 1) * 1.1);
    for (var i = 0; i <= N; i++) {
      var y = i / N * 100, x = pos + amp * Math.sin(y / 100 * Math.PI * 2.6 + pos * 0.16) + amp * 0.4 * Math.sin(y / 100 * Math.PI * 6 - pos * 0.1);
      if (i === N / 2) mid = x;
      pts.push(x.toFixed(2) + '% ' + y.toFixed(2) + '%'); d += (i ? 'L' : 'M') + x.toFixed(2) + ' ' + y.toFixed(2);
    }
    top.style.clipPath = 'polygon(0 0,' + pts.join(',') + ',0 100%)';
    path.setAttribute('d', d); knob.style.left = mid + '%';
    st.style.setProperty('--a', Math.max(0, Math.min(1, (pos - 12) / 14)));
    st.style.setProperty('--b', Math.max(0, Math.min(1, (88 - pos) / 14)));
  }
  function set(v) { pos = Math.max(4, Math.min(96, v)); range.value = Math.round(pos); draw(); }
  function fromEvent(e) { var r = st.getBoundingClientRect(); set((e.clientX - r.left) / r.width * 100); }
  var drag = false;
  st.addEventListener('pointerdown', function (e) { if (e.button) return; drag = true; touched = true; st.classList.add('is-drag'); try { st.setPointerCapture(e.pointerId); } catch (x) {} fromEvent(e); });
  st.addEventListener('pointermove', function (e) { if (drag) fromEvent(e); });
  ['pointerup', 'pointercancel'].forEach(function (n) { st.addEventListener(n, function () { drag = false; st.classList.remove('is-drag'); }); });
  range.addEventListener('input', function () { touched = true; pos = +range.value; draw(); });
  window.addEventListener('resize', draw);
  draw();
  if (!calm && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var t0 = null, keys = [50, 70, 34, 50];
      function ease(t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
      function step(ts) {
        if (touched) return; if (!t0) t0 = ts;
        var t = Math.min((ts - t0) / 2100, 1) * 3, i = Math.min(Math.floor(t), 2);
        set(keys[i] + (keys[i + 1] - keys[i]) * ease(t - i));
        if (t < 3) requestAnimationFrame(step);
      }
      setTimeout(function () { requestAnimationFrame(step); }, 350);
    }, { threshold: .55 });
    io.observe(st);
  }
})();
