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
  form.classList.add('js-form');

  function show(i, focus) {
    cur = i;
    steps.forEach(function (s, k) { s.classList.toggle('is-on', k === i); });
    bars.forEach(function (b, k) { b.classList.toggle('on', k <= i); });
    count.textContent = 'Step ' + (i + 1) + ' of ' + steps.length;
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
      finish('Preview only', 'The form is not connected yet, so nothing was sent. Once it is connected, this screen confirms the request and says when to expect a reply. Until then, email info@wormingbiohumuss.lv.');
      return;
    }
    send.disabled = true;
    fetch(endpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
      .then(function (r) { if (!r.ok) throw new Error(); finish('Request received', 'Thank you. We will reply by email with a delivered price and the specification sheet.'); })
      .catch(function () {
        send.disabled = false;
        count.textContent = 'Your request could not be sent. Check your connection and try again, or email info@wormingbiohumuss.lv.';
      });
  });
  show(0, false);
})();
