#!/usr/bin/env python3
"""Builds the inner pages from shared header/footer taken from index.html.
Run: python3 build.py   (index.html is hand-written and is the source of the shared parts)"""
import re, pathlib
root = pathlib.Path(__file__).parent
idx = (root / 'index.html').read_text()
chrome = idx[idx.index('<a class="skip"'):idx.index('<main id="main">')]
footer = idx[idx.index('<footer'):idx.index('</footer>') + 9]
P = 'images/placeholder/'

def pic(name, alt='', mq='(min-aspect-ratio:1/1)', small='tall', big='wide', lazy=True):
    return (f'<picture><source media="{mq}" srcset="{P}{name}-{big}.jpg">'
            f'<img src="{P}{name}-{small}.jpg" alt="{alt}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""}></picture>')

CLOSE_TPL = '\n<section class="sec sec--earth close" data-theme="dark" style="--prev:var(--__PREV__)">\n  <div class="close__top">__PIC__\n  <svg class="close__line" viewBox="0 0 1 1" preserveAspectRatio="none" aria-hidden="true"><path class="fill" d="M0,0.6 C0.3,0.1 0.62,0.95 1,0.35 L1,1.1 L0,1.1 Z"/><path d="M0,0.6 C0.3,0.1 0.62,0.95 1,0.35"/></svg></div>\n  <svg class="close__waves" viewBox="0 0 1440 320" preserveAspectRatio="none" aria-hidden="true"><path class="w1" d="M0,140 C300,60 600,220 900,150 C1150,95 1300,120 1440,90 L1440,320 L0,320 Z"/><path class="w2" d="M0,200 C260,260 520,120 820,190 C1100,255 1280,170 1440,210 L1440,320 L0,320 Z"/><path class="w3" d="M0,262 C240,300 520,318 760,300 C1040,280 1250,235 1440,250 L1440,320 L0,320 Z"/></svg>\n  <div class="wrap">\n    <div class="close__head">\n      <h2 class="h2">__TITLE__</h2>\n      <svg class="close__orn" viewBox="0 0 300 24" aria-hidden="true"><path d="M4,18 C6,8 14,5 22,7 C20,15 13,19 4,18 Z M26,18 C24,10 30,4 40,3 C41,12 35,18 26,18 Z"/><line x1="56" y1="14" x2="296" y2="14"/></svg>\n    </div>\n    <div class="close__grid">\n      <div class="contact">\n        <a href="tel:+37120252517"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg><span data-k="company.phone">+371 20252517</span></a>\n        <a href="mailto:tomsupenieks@gmail.com"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3 7l9 6 9-6"/></svg><span data-k="company.email">tomsupenieks@gmail.com</span></a>\n      </div>\n      <a class="btn btn--solid-light" href="quote.html"><span>__BTN__<svg class="arr" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg></span></a>\n    </div>\n  </div>\n</section>'

def close(title, btn='Request a quote', prev='sand'):
    return CLOSE_TPL.replace('__PREV__', prev).replace('__PIC__', pic('landscape-latvia', 'Farmland in morning mist')).replace('__TITLE__', title).replace('__BTN__', btn)

PASSPORT = idx[idx.index('<div class="passport"'):idx.index('</section>', idx.index('<div class="passport"'))].rsplit('</div>', 1)[0]

def page(fn, title, desc, body, head_theme='dark', extra_js='', solid=False):
    c = chrome.replace('<a href="index.html" aria-current="true" lang="en"', '<a href="@@SELF@@" aria-current="true" lang="en"').replace('href="lv/index.html" lang="lv"', f'href="lv/{fn}" lang="lv"')
    c = c.replace(f'href="{fn}"', f'href="{fn}" aria-current="page"').replace('@@SELF@@', fn)
    html = f'''<!DOCTYPE html>
<html lang="en" class="no-js" data-head="{head_theme}" data-mid="{head_theme}"{' data-solid' if solid else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Worming</title>
<meta name="description" content="{desc}">
<link rel="preload" href="fonts/literata-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/onest-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="alternate" hreflang="lv" href="lv/{fn}">
<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/pages.css">
<link rel="icon" href="images/logo/symbol-colour.png">
</head>
<body>
{c}<main id="main">
{body}
</main>

{footer}

<script src="js/site.js"></script>
{extra_js}
</body>
</html>
'''
    (root / fn).write_text(html)
    print('built', fn)

TBC = '<span class="tbc">To be confirmed</span>'

# ---------------------------------------------------------------- PRODUCT
product = f'''
<section class="ph ph--image" data-theme="dark">
  <div class="ph__bg">{pic('material-macro', '', lazy=False)}</div>
  <div class="wrap ph__in">
    <h1 class="h1">Worm humus, screened and tested.</h1>
    <p class="ph__plate"><span data-k="product.name">Biohumus (vermicompost)</span><br><span class="muted" data-k="product.type">Processed organic soil improver</span></p>
  </div>
</section>

<section class="sec sec--linen" data-theme="light">
  <div class="wrap material">
    <h2 class="h2" style="color:var(--forest)">The material.</h2>
    <div class="material__cols">
      <div class="material__text">
        <h3>Feedstock</h3>
        <p>Organic matter: manure, vegetable matter and leaves.</p>
        <h3>Worms</h3>
        <p>Californian red worms eat through the feedstock. What they leave behind is the product.</p>
        <h3>Result</h3>
        <p>A dark material that looks like black earth and has no smell. It contains plant nutrients and humic substances.</p>
      </div>
      <figure class="material__img">{pic('hand-material', 'A gloved hand holding loose worm humus above an open big bag', mq='(min-width:62rem)', small='wide', big='tall')}</figure>
    </div>
  </div>
</section>

<section class="sec sec--sand" data-theme="light">
  <div class="wrap">
    <h2 class="h2">How it differs from compost.</h2>
    <div class="cmp" role="table" aria-label="Compost compared with worm humus">
      <div class="cmp__row cmp__head" role="row"><span role="columnheader"></span><span role="columnheader">Compost</span><span role="columnheader">Worm humus</span></div>
      <div class="cmp__row" role="row"><span role="rowheader">Made by</span><span role="cell">Microbes, in a heap that heats up</span><span role="cell">Worms, at ambient temperature</span></div>
      <div class="cmp__row" role="row"><span role="rowheader">Texture</span><span role="cell">Varies with the source material</span><span role="cell">Fine and earth-like</span></div>
      <div class="cmp__row" role="row"><span role="rowheader">Used as</span><span role="cell">Bulk organic matter, by the tonne</span><span role="cell">A small share of a mix or planting hole</span></div>
    </div>
    <p class="lede" style="margin-top:2rem">They do different jobs. Most growers who use worm humus keep using compost too.</p>
  </div>
</section>

<section class="sec sec--earth" data-theme="dark" id="specifications">
  <div class="wrap">
    <h2 class="h2">Specifications.</h2>
    <p class="lede muted" style="margin-top:1.25rem">Values from our current product data sheet.</p>
    <dl class="figs">
      <div><dd class="num" data-k="product.ph">7.3</dd><dt>pH (KCl)</dt></div>
      <div><dd class="num" data-k="product.organicMatter">min. 20.1%</dd><dt>Organic matter</dt></div>
      <div><dd class="num" data-k="product.n">0.9%</dd><dt>Total nitrogen (N)</dt></div>
      <div><dd class="num" data-k="product.p2o5">0.9%</dd><dt>Phosphorus (P₂O₅)</dt></div>
      <div><dd class="num" data-k="product.k2o">0.7%</dd><dt>Potassium (K₂O)</dt></div>
      <div><dd class="tbc" data-k="product.moisture">To be confirmed</dd><dt>Moisture</dt></div>
    </dl>
    <div class="read">
      <div>
        <h3 class="read__t">How to read a batch passport</h3>
        <p class="muted">The passport is a one-page summary of the material. It lists the values above, the screen size and the storage conditions, so your agronomist or QA team can check them against your recipe.</p>
      </div>
      {PASSPORT}
  </div>
</section>

<section class="sec sec--linen" data-theme="light">
  <div class="wrap formats">
    <figure class="formats__img">{pic('supply-bigbags', 'Filled big bags on pallets in a warehouse', mq='(min-width:62rem)', small='wide', big='tall')}</figure>
    <div>
      <h2 class="h2" style="color:var(--forest)">Formats.</h2>
      <ul class="rows">
        <li><h3>Sacks</h3><p>For trials, nurseries and smaller sites. Size: {TBC}</p></li>
        <li><h3>Big bags</h3><p>On pallets, for forklift handling. Size: {TBC}</p></li>
        <li><h3>Bulk</h3><p>For substrate producers and larger volumes. {TBC}</p></li>
      </ul>
      <h2 class="h2" style="color:var(--forest);font-size:var(--step2);margin-top:4rem">Handling and storage.</h2>
      <ul class="rows">
        <li><h3>Temperature</h3><p>Store between <span data-k="product.storage">−30 °C to +40 °C</span>.</p></li>
        <li><h3>Cover</h3><p data-k="product.storageNote">Protect from rain and direct sun.</p></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--sand" data-theme="light">
  <div class="wrap docs">
    <h2 class="h2" style="font-size:var(--step2)">Documents.</h2>
    <ul class="rows rows--earth">
      <li><h3>Product specification sheet</h3><p>Sent with your quote.</p></li>
      <li><h3>Example batch report</h3><p>On request.</p></li>
      <li><h3>Organic suitability statement</h3><p>On request, for your certifier.</p></li>
    </ul>
  </div>
</section>
{close('Request a sample or a quote.')}
'''
page('product.html', 'Product and specifications', 'Solid biohumus (vermicompost) from Californian red worms: material, specifications, formats and storage.', product)

# ---------------------------------------------------------------- APPLICATIONS
def seg(id, cls, theme, img, alt, title, intro, uses, rates, check):
    return f'''
<section class="seg {cls}" data-theme="{theme}" id="{id}">
  <figure class="seg__img">{pic(img, alt)}</figure>
  <div class="seg__body">
    <h2 class="h2">{title}</h2>
    <p class="lede">{intro}</p>
    <div class="seg__blocks">
      <div><h3>Typical uses</h3>{uses}</div>
      <div><h3>Starting rates</h3>{rates}</div>
      <div><h3>What to check</h3>{check}</div>
      <div><h3>Evidence</h3><p class="tbc">Trial results coming soon.</p></div>
    </div>
  </div>
</section>'''

apps = f'''
<section class="ph ph--plain sec--linen" data-theme="light">
  <div class="wrap">
    <h1 class="h1" style="color:var(--forest)">Where it fits in your operation.</h1>
    <div class="ph__row">
      <p class="lede">Rates below are starting points, not prescriptions. Crops and systems differ, so confirm each one with a small trial.</p>
      <nav class="seg-nav" aria-label="Applications">
        <a href="#substrate">Substrate producers</a>
        <a href="#greenhouse">Greenhouses and young plants</a>
        <a href="#orchards">Orchards and vineyards</a>
        <a href="#vegetables">Organic vegetable growers</a>
      </nav>
    </div>
  </div>
</section>
{seg('substrate', 'seg--split seg--sand', 'light', 'app-substrate', 'Dark growing media on a conveyor in a production hall', 'Substrate and growing-media producers',
 'An organic component for potting and propagation mixes, including peat-reduced recipes.',
 '<p>Blended into finished growing media as one part of the recipe.</p>',
 '<p>Start test batches at about 10% by volume and work up. Our own guidance for raising seedlings is 1 part worm humus to 3 parts peat or soil.</p>',
 '<p>EC, pH and air capacity of the final blend. Our data sheet pH (KCl) is 7.3.</p>')}
{seg('greenhouse', 'seg--top seg--linen', 'light', 'app-greenhouse', 'Seedling trays on greenhouse benches', 'Greenhouses and young plants',
 'For propagation, potting on and planting out under glass or plastic.',
 '<p>Sowing and pricking-out mixes for cucumbers, tomatoes, peppers and brassicas. In the planting hole at transplanting.</p>',
 '<p>Seedling mixes: up to 1 part to 3 parts peat or soil. Tomatoes and cucumbers: about 100 g in each planting hole, then water.</p>',
 '<p>High mix rates can raise EC. Check salinity, and trial first on sub-irrigated benches.</p>')}
{seg('orchards', 'seg--split seg--rev seg--forest', 'dark', 'app-orchard', 'Gloved hands planting a young vine', 'Orchards and vineyards',
 'Mixed into the planting hole for new trees, vines and berry crops.',
 '<p>New plantings of fruit trees and berry bushes. Monthly top-dressing around established plants in the growing season.</p>',
 '<p>Apple, pear, cherry and plum: 1.5 to 2 kg per planting hole. Currants and gooseberries: 1 to 1.5 kg. Strawberries: 150 to 200 g per plant. For vines, ask us and plan a trial row.</p>',
 '<p>Mix it with the soil in the hole instead of leaving it in a layer, and water after planting.</p>')}
{seg('vegetables', 'seg--top seg--earth', 'dark', 'app-vegetables', 'Rows of lettuce in a polytunnel', 'Organic vegetable growers',
 'Bed preparation, transplanting and feeding through the season, in tunnels and in the field.',
 '<p>Worked into beds before sowing or planting. Placed under transplants. Top-dressed during growth.</p>',
 '<p>Onions, carrots and beets: 0.5 kg per m². Salad, dill and parsley: 1 L per m² of row. Potatoes: about 50 g under each plant. In season: about 1 L per m² once a month, worked in and watered.</p>',
 '<p>Vermicompost is authorised for EU organic production (Regulation (EU) 2021/1165, Annex II). Confirm with your certifier.</p>')}

<section class="sec sec--sand" data-theme="light">
  <div class="wrap trial">
    <div>
      <h2 class="h2">Run a trial before you order.</h2>
      <p class="muted" style="margin-top:1.25rem;max-width:28rem">The rates on this page follow the recommendations of the Latvian Biohumus Producers' Association. Your own side-by-side trial tells you more than any table.</p>
    </div>
    <ol class="supply-list">
      <li><h3>Pick a small area</h3><p>One bay, a few rows or one substrate batch.</p></li>
      <li><h3>Keep a control</h3><p>Leave an untreated strip right next to it.</p></li>
      <li><h3>Measure</h3><p>Record rooting, growth and EC for four to six weeks.</p></li>
      <li><h3>Decide</h3><p>Send us the results and we'll talk through a rate for your system.</p></li>
    </ol>
  </div>
</section>
{close('Talk to us about your crop.')}
'''
page('applications.html', 'Applications', 'How substrate producers, greenhouses, orchards, vineyards and organic vegetable growers use worm humus, with starting rates.', apps, head_theme='light')

# ---------------------------------------------------------------- QUALITY
quality = f'''
<section class="ph ph--image ph--forest" data-theme="dark">
  <div class="ph__bg">{pic('production-beds', '', lazy=False)}</div>
  <div class="wrap ph__in">
    <h1 class="h1">One site. Every batch on record.</h1>
    <p class="ph__plate">Production, quality and supply<br><span class="muted">Vītiņu pagasts, Latvia</span></p>
  </div>
</section>

<section class="sec sec--forest" data-theme="dark">
  <div class="wrap">
    <h2 class="h2">Production, step by step.</h2>
    <div class="journey" id="journey"><span class="journey__fill" aria-hidden="true"></span><ol>
      <li><h3>Feedstock</h3><p>Manure, vegetable matter and leaves come in and are prepared for the beds.</p></li>
      <li><h3>Worm beds</h3><p>Californian red worms work through the material.</p><figure>{pic('production-beds', 'Long indoor beds of dark organic material', small='wide')}</figure></li>
      <li><h3>Maturation</h3><p>The humus rests before it is harvested.</p></li>
      <li><h3>Screening</h3><p>It is sieved to an even, fine crumb.</p><figure>{pic('production-screening', 'A rotary screen sieving dark humus', small='wide')}</figure></li>
      <li><h3>Testing</h3><p>The material is checked against the specification.</p></li>
      <li><h3>Packing</h3><p>It is filled, labelled and stored under cover until dispatch.</p><figure>{pic('supply-bigbags', 'Filled big bags on pallets', small='wide')}</figure></li>
    </ol></div>
  </div>
</section>

<section class="sec sec--sand" data-theme="light">
  <div class="wrap batch">
    <div>
      <h2 class="h2">Traceability.</h2>
      <p class="lede" style="margin-top:1.5rem">From batch number to data sheet. You know what you received, and so does your QA team.</p>
      <h3 class="q-sub">What we test</h3>
      <ul class="taglist"><li>pH</li><li>Organic matter</li><li>Nitrogen</li><li>Phosphorus</li><li>Potassium</li><li>Moisture</li></ul>
      <p class="small muted" style="margin-top:1rem">Testing frequency: {TBC}</p>
    </div>
    {PASSPORT}
  </div>
</section>

<section class="sec sec--linen" data-theme="light">
  <div class="wrap supplygrid">
    <h2 class="h2" style="color:var(--forest)">Supply.</h2>
    <div class="supplygrid__cols">
      <div><h3>Documents for certifiers and QA teams</h3><p>Specification sheet, batch report and an organic suitability statement, on request.</p></div>
      <div><h3>Formats and packaging</h3><p>Sacks, big bags on pallets, and bulk. Sizes: {TBC}</p></div>
      <div><h3>Capacity and contract supply</h3><p>Tell us your yearly volume and timing. We'll confirm what we can reserve for your season.</p></div>
      <div><h3>Delivery across the EU</h3><p>Shipped from Latvia. Freight is included in each quote and lead time is confirmed with it.</p></div>
    </div>
  </div>
</section>
{close('Request a quote.', prev='linen')}
'''
page('quality.html', 'Quality and supply', 'How Worming produces, checks, packs and delivers worm humus across the EU.', quality)

# ---------------------------------------------------------------- QUOTE
EU = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czechia','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','Other']
opts = lambda xs: '<option value="">Select</option>' + ''.join(f'<option>{x}</option>' for x in xs)
quote = f'''
<section class="quote" data-theme="dark">
  <div class="quote__side">
    <div class="quote__bg">{pic('hero-below', '', lazy=False)}</div>
    <div class="quote__side-in">
      <h1 class="h1">Request a quote</h1>
      <p class="lede">Four short steps. We reply with a price delivered to your site.</p>
      <h2 class="q-sub">What happens next</h2>
      <ol class="next">
        <li>We read your request and check format and volume.</li>
        <li>You receive a delivered price and the specification sheet.</li>
        <li>If you asked for one, we send a sample.</li>
      </ol>
      <h2 class="q-sub">Prefer to talk?</h2>
      <p class="contact"><a href="tel:+37120252517" data-k="company.phone">+371 20252517</a><a href="mailto:tomsupenieks@gmail.com" data-k="company.email">tomsupenieks@gmail.com</a></p>
    </div>
  </div>

  <div class="quote__main">
    <!-- Set data-endpoint to your form service URL (for example a Formspree endpoint) to enable sending. -->
    <form id="quote-form" class="qf" method="post" action="#" data-endpoint="" novalidate>
      <div class="qf__progress" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <p class="qf__count small" aria-live="polite"></p>

      <fieldset class="qf__step">
        <legend>Your business</legend>
        <div class="f"><label for="company">Company</label><input id="company" name="company" type="text" autocomplete="organization" required><p class="err" hidden>Enter your company name.</p></div>
        <div class="f"><label for="operation">Type of operation</label><select id="operation" name="operation" required>{opts(['Substrate or growing-media producer','Greenhouse or young-plant grower','Orchard or vineyard','Organic vegetable grower','Nursery','Distributor','Other'])}</select><p class="err" hidden>Choose the closest match.</p></div>
        <div class="f"><label for="country">Delivery country</label><select id="country" name="country" autocomplete="country-name" required>{opts(EU)}</select><p class="err" hidden>Choose a country.</p></div>
      </fieldset>

      <fieldset class="qf__step">
        <legend>What you need</legend>
        <div class="f"><label for="application">Intended application</label><input id="application" name="application" type="text" placeholder="Tomato propagation mix"></div>
        <div class="f"><label for="format">Format</label><select id="format" name="format">{opts(['Big bags','Sacks','Bulk','Not sure yet'])}</select></div>
        <div class="f"><label for="quantity">Estimated quantity per year</label><input id="quantity" name="quantity" type="text" placeholder="20 big bags"></div>
        <div class="f"><label for="timing">When do you need it?</label><input id="timing" name="timing" type="text" placeholder="March 2027"></div>
        <label class="check"><input type="checkbox" name="sample" value="yes"><span>Send me a sample first</span></label>
      </fieldset>

      <fieldset class="qf__step">
        <legend>Delivery</legend>
        <div class="f"><label for="postcode">Delivery postcode or region</label><input id="postcode" name="postcode" type="text" autocomplete="postal-code"></div>
        <div class="f"><span class="f__label" id="unload-l">Unloading on site</span>
          <div class="radios" role="radiogroup" aria-labelledby="unload-l">
            <label class="check"><input type="radio" name="unloading" value="Forklift available"><span>Forklift available</span></label>
            <label class="check"><input type="radio" name="unloading" value="Tail-lift needed"><span>Tail-lift needed</span></label>
            <label class="check"><input type="radio" name="unloading" value="Not sure"><span>Not sure</span></label>
          </div>
        </div>
      </fieldset>

      <fieldset class="qf__step">
        <legend>Your contact details</legend>
        <div class="f"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required><p class="err" hidden>Enter your name.</p></div>
        <div class="f"><label for="email">Work email</label><input id="email" name="email" type="email" autocomplete="email" required><p class="err" hidden>Enter an email address like name@company.com.</p></div>
        <div class="f"><label for="phone">Phone (optional)</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="f"><label for="notes">Notes (optional)</label><textarea id="notes" name="notes" rows="3"></textarea></div>
        <div class="f"><label class="check"><input type="checkbox" id="consent" name="consent" required><span>I agree that Worming uses these details to answer my request. See the <a href="privacy.html">privacy policy</a>.</span></label><p class="err" hidden>Tick the box so we can reply.</p></div>
      </fieldset>

      <div class="qf__nav">
        <button type="button" class="btn btn--ghost-dark qf__back" hidden><span>Back</span></button>
        <button type="button" class="btn btn--solid-dark qf__next"><span>Next</span></button>
        <button type="submit" class="btn btn--solid-dark qf__send"><span>Send request</span></button>
      </div>
    </form>
    <div class="qf__done" id="quote-done" hidden tabindex="-1">
      <h2 class="h2" style="font-size:var(--step2);color:var(--forest)"></h2>
      <p class="lede" style="margin-top:1rem"></p>
    </div>
  </div>
</section>
'''
page('quote.html', 'Request a quote', 'Request a delivered price for worm humus anywhere in the EU.', quote, extra_js='<script src="js/quote.js"></script>', solid=True)

# ---------------------------------------------------------------- LEGAL
privacy = '''
<section class="ph ph--plain sec--linen legal" data-theme="light">
  <div class="wrap legal__in">
    <h1 class="h1" style="color:var(--forest);font-size:var(--step3)">Privacy policy</h1>
    <p class="small muted">Draft for legal review. Last updated 14 November 2026.</p>

    <h2>Who we are</h2>
    <p><span data-k="company.legalName">SIA "Worming"</span>, registration number <span data-k="company.regNo">48503018418</span>, <span data-k="company.address">"Līči", Vītiņu pagasts, Auces novads, LV-3721, Latvia</span>, is the controller of personal data collected through this website. Contact: <a href="mailto:tomsupenieks@gmail.com">tomsupenieks@gmail.com</a>, <span data-k="company.phone">+371 20252517</span>.</p>

    <h2>What we collect</h2>
    <p>When you send a quote request we receive what you enter in the form: company, type of operation, country, delivery postcode or region, the product details you ask about, your name, work email, phone number if you give one, and your notes. If you email or call us, we keep that correspondence.</p>

    <h2>Why we use it, and on what legal basis</h2>
    <ul>
      <li>To prepare a quote and answer your request: steps taken at your request before entering into a contract (GDPR Article 6(1)(b)).</li>
      <li>To deliver orders and keep accounting records: performance of a contract and legal obligations (Article 6(1)(b) and (c)).</li>
      <li>To follow up on a business enquiry: our legitimate interest in running our business (Article 6(1)(f)). You can object at any time.</li>
    </ul>
    <p>We don't send marketing emails unless you ask for them.</p>

    <h2>Who receives it</h2>
    <p>Our email and form service providers, who process data for us, and carriers when we deliver an order. We don't sell personal data.</p>

    <h2>How long we keep it</h2>
    <p>Quote requests that don't lead to an order: up to two years after our last contact. Orders and invoices: as long as Latvian accounting law requires.</p>

    <h2>Cookies</h2>
    <p>This website sets no advertising or tracking cookies and loads no third-party analytics. Fonts are served from our own site.</p>

    <h2>Your rights</h2>
    <p>You can ask us for access to your data, to correct or delete it, to restrict or object to its use, and to receive it in a portable format. Write to <a href="mailto:tomsupenieks@gmail.com">tomsupenieks@gmail.com</a>. You can also complain to the Latvian Data State Inspectorate (Datu valsts inspekcija, dvi.gov.lv).</p>

    <h2>Changes</h2>
    <p>We'll publish any changes on this page with a new date.</p>
  </div>
</section>
'''
page('privacy.html', 'Privacy policy', 'How SIA Worming handles personal data from quote requests.', privacy, head_theme='light')

company = '''
<section class="ph ph--plain sec--linen legal" data-theme="light">
  <div class="wrap legal__in">
    <h1 class="h1" style="color:var(--forest);font-size:var(--step3)">Company details</h1>
    <dl class="cdl">
      <div><dt>Legal name</dt><dd data-k="company.legalName">SIA "Worming"</dd></div>
      <div><dt>Registration number</dt><dd class="num" data-k="company.regNo">48503018418</dd></div>
      <div><dt>Registered address</dt><dd data-k="company.address">"Līči", Vītiņu pagasts, Auces novads, LV-3721, Latvia</dd></div>
      <div><dt>Phone</dt><dd><a href="tel:+37120252517" data-k="company.phone">+371 20252517</a></dd></div>
      <div><dt>Email</dt><dd><a href="mailto:tomsupenieks@gmail.com" data-k="company.email">tomsupenieks@gmail.com</a></dd></div>
    </dl>
    <p style="margin-top:2.5rem"><a class="btn btn--solid-dark" href="quote.html"><span>Request a quote</span></a></p>
  </div>
</section>
'''
page('company.html', 'Company details', 'Legal and contact details of SIA Worming, Latvia.', company, head_theme='light')

# ---------------------------------------------------------------- ABOUT
def img1(name, alt=''):
    return f'<img src="{P}{name}.jpg" alt="{alt}" loading="lazy">'

about = f"""
<section class="roots" data-theme="dark" aria-label="Why Worming exists">
  <div class="roots__stage">
    <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
      <clipPath id="rc1" clipPathUnits="objectBoundingBox"><path id="rc1p" d="M0,1.2 L1,1.2 L1,1.3 L0,1.3 Z"/></clipPath>
      <clipPath id="rc2" clipPathUnits="objectBoundingBox"><path id="rc2p" d="M0,1.2 L1,1.2 L1,1.3 L0,1.3 Z"/></clipPath>
    </defs></svg>
    <div class="roots__layer roots__layer--1">
      <picture><source media="(min-aspect-ratio:1/1)" srcset="{P}about-table-wide.jpg"><img src="{P}about-table-tall.jpg" alt="Freshly harvested vegetables on a wooden table" fetchpriority="high"></picture>
      <p class="roots__say">Good health starts with good food.</p>
    </div>
    <div class="roots__layer roots__layer--2">
      <img src="{P}about-roots-tall.jpg" alt="A young plant lifted from the soil, roots showing">
      <p class="roots__say">Good food starts with healthy soil.</p>
    </div>
    <div class="roots__layer roots__layer--3">
      <picture><source media="(min-aspect-ratio:1/1)" srcset="{P}hero-below-wide.jpg"><img src="{P}hero-below-tall.jpg" alt=""></picture>
      <p class="roots__say">Healthy soil starts here.</p>
    </div>
    <h1 class="roots__plate">About Worming<br><span>Founded 2023 in Auce, Latvia</span></h1>
  </div>
</section>

<section class="sec sec--linen" data-theme="light">
  <div class="wrap why">
    <div class="why__text">
      <h2 class="h2" style="color:var(--forest)">Why we started.</h2>
      <p class="why__lede">Worming was founded in 2023 on a simple belief: good health starts with good food, and good food starts with healthy soil.</p>
      <p>We care about nutrition, wellbeing and sustainable agriculture. Making worm humus is how we support the growers who produce high-quality organic food.</p>
    </div>
    <figure class="why__fig"><div class="why__img">{img1('about-founder-tall', 'Toms Upenieks at the farm in Auce')}</div><figcaption><strong>Toms Upenieks</strong><span>Founder</span></figcaption></figure>
  </div>
</section>

<section class="sec sec--forest gen" data-theme="dark">
  <figure class="gen__img">{img1('about-generations-wide', 'Two generations of the family beside a bed of worm humus')}</figure>
  <div class="wrap">
    <h2 class="h2 gen__title">Two generations of family farming.</h2>
    <p class="lede muted" style="margin-top:1.5rem;max-width:38ch">Worming is built on practical farming knowledge passed from one generation to the next, combined with a modern approach to sustainable production and international business.</p>
  </div>
</section>

<section class="sec sec--sand" data-theme="light">
  <div class="wrap place">
    <div>
      <h2 class="h2">Made in Auce. Supplied to 15 countries.</h2>
      <p class="lede" style="margin-top:1.5rem;max-width:36ch">Our production site is in Auce, Latvia. We manage the whole biohumus process there, from raw materials to finished product.</p>
      <dl class="place__figs">
        <div><dd class="num">2023</dd><dt>Founded</dt></div>
        <div><dd class="num">15</dd><dt>Countries supplied</dt></div>
        <div><dd class="num">1</dd><dt>Product</dt></div>
      </dl>
    </div>
    <div class="place__imgs">
      <figure>{img1('about-farm-wide', 'The production building in the Latvian countryside')}</figure>
      <figure>{img1('about-loading-wide', 'Big bags being loaded onto a truck by forklift')}</figure>
    </div>
  </div>
</section>

<section class="sec sec--linen" data-theme="light">
  <div class="wrap how">
    <div>
      <h2 class="h2" style="color:var(--forest)">How we work.</h2>
      <p class="muted" style="margin-top:1.25rem;max-width:28rem">We believe good business starts with honest communication, and we want long-term relationships with the growers we supply.</p>
    </div>
    <ul class="rows">
      <li><h3>Direct from the manufacturer</h3><p>Competitive pricing, with no middlemen between you and the producer.</p></li>
      <li><h3>Personal, responsive service</h3><p>You deal with the people who make the product.</p></li>
      <li><h3>Flexible bulk supply</h3><p>Volumes to suit your operation and season.</p></li>
      <li><h3>Simple purchasing</h3><p>A clear quote, clear terms and no surprises.</p></li>
      <li><h3>Who we supply</h3><p>Substrate manufacturers, commercial greenhouses, nurseries, orchards, vineyards and organic vegetable growers.</p></li>
    </ul>
  </div>
</section>
{close('Let&rsquo;s talk about your crop.', prev='linen')}
"""
page('about.html', 'About', 'Worming is a family business in Auce, Latvia, making worm humus for professional growers in 15 countries.', about)


import build_lv
build_lv.run()
