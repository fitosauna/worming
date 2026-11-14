/* Quote form: progressive steps, inline validation, configurable endpoint. */
(function () {
  var form = document.getElementById('quote-form');
  if (!form) return;
  var steps = Array.prototype.slice.call(form.querySelectorAll('.qf__step'));
  var bars = form.querySelectorAll('.qf__progress i');
  var count = form.querySelector('.qf__count');
  var back = form.querySelector('.qf__back'), next = form.querySelector('.qf__next'), send = form.querySelector('.qf__send');
  var done = document.getElementById('quote-done');
  var cur = 0;
  var LV = document.documentElement.lang === 'lv';
  var T = LV ? {
    step: function (i, n) { return i + '. solis no ' + n; },
    previewT: 'Tikai priekšskatījums', previewP: 'Veidlapa vēl nav pieslēgta, tāpēc nekas netika nosūtīts. Kad tā būs pieslēgta, šeit redzēsiet apstiprinājumu un to, kad gaidīt atbildi. Līdz tam rakstiet uz tomsupenieks@gmail.com.',
    okT: 'Pieprasījums saņemts', okP: 'Paldies! Atbildēsim e-pastā ar cenu, kurā iekļauta piegāde, un specifikācijas lapu.',
    fail: 'Pieprasījumu neizdevās nosūtīt. Pārbaudiet interneta savienojumu un mēģiniet vēlreiz vai rakstiet uz tomsupenieks@gmail.com.'
  } : {
    step: function (i, n) { return 'Step ' + i + ' of ' + n; },
    previewT: 'Preview only', previewP: 'The form is not connected yet, so nothing was sent. Once it is connected, this screen confirms the request and says when to expect a reply. Until then, email tomsupenieks@gmail.com.',
    okT: 'Request received', okP: 'Thank you. We will reply by email with a delivered price and the specification sheet.',
    fail: 'Your request could not be sent. Check your connection and try again, or email tomsupenieks@gmail.com.'
  };
  form.classList.add('js-form');

  function show(i, focus) {
    cur = i;
    steps.forEach(function (s, k) { s.classList.toggle('is-on', k === i); });
    bars.forEach(function (b, k) { b.classList.toggle('on', k <= i); });
    count.textContent = T.step(i + 1, steps.length);
    back.hidden = i === 0;
    next.hidden = i === steps.length - 1;
    send.hidden = i !== steps.length - 1;
    if (focus) { var f = steps[i].querySelector('input,select,textarea'); if (f) f.focus(); }
  }
  function check(field) {
    var ok = field.checkValidity();
    var wrap = field.closest('.f'); var err = wrap && wrap.querySelector('.err');
    field.setAttribute('aria-invalid', ok ? 'false' : 'true');
    if (err) err.hidden = ok;
    return ok;
  }
  function validStep(i) {
    var first = null;
    steps[i].querySelectorAll('[required]').forEach(function (f) { if (!check(f) && !first) first = f; });
    if (first) first.focus();
    return !first;
  }
  form.addEventListener('input', function (e) { if (e.target.getAttribute('aria-invalid') === 'true') check(e.target); });
  form.addEventListener('change', function (e) { if (e.target.getAttribute('aria-invalid') === 'true') check(e.target); });
  next.addEventListener('click', function () { if (validStep(cur)) show(cur + 1, true); });
  back.addEventListener('click', function () { show(cur - 1, true); });
  form.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA' && e.target.type !== 'submit' && cur < steps.length - 1) { e.preventDefault(); next.click(); }
  });

  function finish(title, text) {
    form.hidden = true; done.hidden = false;
    done.querySelector('h2').textContent = title;
    done.querySelector('p').textContent = text;
    done.focus();
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!validStep(cur)) return;
    var endpoint = form.getAttribute('data-endpoint');
    if (!endpoint) {
      finish(T.previewT, T.previewP);
      return;
    }
    send.disabled = true;
    fetch(endpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
      .then(function (r) { if (!r.ok) throw new Error(); finish(T.okT, T.okP); })
      .catch(function () {
        send.disabled = false;
        count.textContent = T.fail;
      });
  });
  show(0, false);
})();
