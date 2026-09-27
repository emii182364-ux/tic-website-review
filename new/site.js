// Language switch (English by default, Traditional Chinese as an option), mobile menu and group filters.
(function () {
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem('tic-lang'); } catch (e) {}
  var fromUrl = /[?&]lang=zh\b/.test(location.search) ? 'zh' : null;
  setLang(fromUrl || saved || 'en');

  function setLang(lang) {
    root.dataset.lang = lang;
    root.lang = lang === 'zh' ? 'zh-Hant' : 'en';
    document.querySelectorAll('.lang').forEach(function (b) {
      b.textContent = lang === 'zh' ? 'English' : '中文';
      b.setAttribute('aria-label', lang === 'zh' ? 'Switch to English' : '切換為中文');
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.lang');
    if (b) {
      var next = root.dataset.lang === 'zh' ? 'en' : 'zh';
      setLang(next);
      try { localStorage.setItem('tic-lang', next); } catch (err) {}
    }
    var m = e.target.closest('.menu-btn');
    if (m) {
      var nav = document.getElementById('nav');
      var open = nav.classList.toggle('open');
      m.setAttribute('aria-expanded', open);
    }
    var c = e.target.closest('.chip');
    if (c) {
      document.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', x === c); });
      var f = c.dataset.f;
      document.querySelectorAll('[data-t]').forEach(function (g) {
        g.hidden = f !== 'all' && g.dataset.t.split(' ').indexOf(f) < 0;
      });
    }
    var cp = e.target.closest('[data-copy]');
    if (cp) {
      var text = document.getElementById(cp.dataset.copy).textContent.trim();
      var done = function (ok) {
        var old = cp.innerHTML;
        cp.textContent = ok ? '✓' : text;
        setTimeout(function () { cp.innerHTML = old; }, 1600);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
      else done(false);
    }
  });
  // Entrance effect for the five photo strips: starts when the strips scroll into view.
  document.addEventListener('DOMContentLoaded', function () {
    var st = document.querySelector('.strips');
    if (!st) return;
    function check() {
      var r = st.getBoundingClientRect();
      if (r.top < innerHeight * 0.9 && r.bottom > 0) {
        st.classList.add('in');
        removeEventListener('scroll', check);
        removeEventListener('resize', check);
      }
    }
    addEventListener('scroll', check, { passive: true });
    addEventListener('resize', check);
    check();
  });
  // Re-apply after the page is parsed so buttons get the right label.
  document.addEventListener('DOMContentLoaded', function () { setLang(root.dataset.lang); });
})();
