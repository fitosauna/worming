"""Internal: builds font-lab.html (EN) and lv/font-lab.html to compare display fonts on the real homepage."""
import pathlib, re
root = pathlib.Path(__file__).parent
UR  = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2212,U+2215'
URX = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+1E00-1E9F,U+20A0-20AB'
def face(name, base, weight, pre):
    return (f'@font-face{{font-family:"{name}";font-weight:{weight};font-display:swap;src:url({pre}fonts/lab/{base.replace("LATIN","latin")}) format("woff2");unicode-range:{UR}}}\n'
            f'@font-face{{font-family:"{name}";font-weight:{weight};font-display:swap;src:url({pre}fonts/lab/{base.replace("LATIN","latin-ext")}) format("woff2");unicode-range:{URX}}}\n')
def scale(sel, m, d):
    return (f'html[data-font="{sel}"] .hero__stage{{--fs:min({22.5*m:.2f}vw,{13.2*m:.2f}svh)}}\n'
            f'@media (min-aspect-ratio:1/1){{html[data-font="{sel}"] .hero__stage{{--fs:min({11.4*d:.2f}vw,{31*d:.2f}svh)}}}}\n')
SER = ':is(.serif,.h1,.h2,.hero__title,.menu__links a,h1,h2,h3,dd,.passport *,.close *)'
def css(pre):
    return ('<style id="font-lab">\n'
      + face('Besley', 'besley-LATIN-wght-normal.woff2', '400 900', pre)
      + face('Bricolage Grotesque', 'bricolage-grotesque-LATIN-standard-normal.woff2', '200 800', pre)
      + face('Gloock', 'gloock-LATIN-400-normal.woff2', '400', pre)
      + 'html[data-font="besley"]{--serif:"Besley",Georgia,serif}\n'
      + f'html[data-font="besley"] {SER}{{letter-spacing:-.02em}}\n'
      + 'html[data-font="besley"] .hero__title{font-weight:700;letter-spacing:-.04em}\n'
      + scale('besley', .86, .86)
      + 'html[data-font="bricolage"]{--serif:"Bricolage Grotesque",system-ui,sans-serif}\n'
      + f'html[data-font="bricolage"] {SER}{{font-variation-settings:"opsz" 96,"wdth" 88;letter-spacing:-.03em}}\n'
      + 'html[data-font="bricolage"] .hero__title{font-weight:700;font-variation-settings:"opsz" 96,"wdth" 86;letter-spacing:-.03em}\n'
      + scale('bricolage', 1.04, 1.04)
      + 'html[data-font="bricolage"] dd{font-variation-settings:"opsz" 24,"wdth" 100;font-weight:500;letter-spacing:-.01em}\n'
      + 'html[data-font="gloock"]{--serif:"Gloock",Georgia,serif}\n'
      + 'html[data-font="gloock"] *{font-synthesis:none}\n'
      + f'html[data-font="gloock"] {SER}{{letter-spacing:-.01em}}\n'
      + 'html[data-font="gloock"] .hero__title{letter-spacing:-.02em}\n'
      + scale('gloock', .97, .97)
      + '.flab{position:fixed;left:50%;bottom:.75rem;transform:translateX(-50%);z-index:9999;display:flex;gap:2px;background:#2A1D14;padding:3px;box-shadow:0 8px 30px rgba(0,0,0,.35);max-width:calc(100vw - 1rem)}\n'
      + '.flab a{font:500 .8rem/1 "Onest",system-ui,sans-serif;color:#F4F5F1;text-decoration:none;padding:.7rem .7rem;white-space:nowrap}\n'
      + '.flab a[aria-current]{background:#F4F5F1;color:#1E3B2C}\n'
      + '</style>\n<meta name="robots" content="noindex">\n'
      + '<script>(function(){var f=new URLSearchParams(location.search).get("font")||"literata";document.documentElement.setAttribute("data-font",f)})()</script>\n')
BAR = ('<nav class="flab" aria-label="Font options">'
       '<a href="?font=literata" data-f="literata">Current</a><a href="?font=besley" data-f="besley">A · Besley</a>'
       '<a href="?font=bricolage" data-f="bricolage">B · Bricolage</a><a href="?font=gloock" data-f="gloock">C · Gloock</a>'
       '<a href="OTHER" data-other>LANG</a></nav>\n'
       '<script>(function(){var f=document.documentElement.getAttribute("data-font");document.querySelectorAll(".flab a").forEach(function(a){'
       'if(a.dataset.f===f)a.setAttribute("aria-current","true");if(a.hasAttribute("data-other"))a.href+="?font="+f;});})()</script>\n')
for src, out, pre, other, lang in (('index.html', 'font-lab.html', '', 'lv/font-lab.html', 'LV'), ('lv/index.html', 'lv/font-lab.html', '../', '../font-lab.html', 'EN')):
    s = (root / src).read_text()
    s = s.replace('</head>', css(pre) + '</head>', 1).replace('</body>', BAR.replace('OTHER', other).replace('LANG', lang) + '</body>', 1)
    (root / out).write_text(s)
    print('built', out)
