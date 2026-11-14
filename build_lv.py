"""Generates the Latvian site in /lv from the built English pages and i18n/lv.json."""
import json, re, pathlib
from bs4 import BeautifulSoup, Comment
root = pathlib.Path(__file__).parent
PAGES = ['index.html','product.html','applications.html','quality.html','about.html','quote.html','privacy.html','company.html']
ATTRS = ['alt', 'aria-label', 'placeholder', 'title']
ASSET = re.compile(r'^(css|js|fonts|images|content)/')
KEEP = re.compile(r'^[\W\d_]*$|^(html|EN|LV|pH|pH \(KCl\)|Worming|Toms Upenieks|Malta|\+371.*|.*@gmail\.com|0 cm|48503018418)$')

def run():
    tr = json.load(open(root / 'i18n' / 'lv.json'))
    missing = set()
    def t(s):
        key = re.sub(r'\s+', ' ', s).strip()
        if not key: return s
        if key in tr:
            lead = s[:len(s) - len(s.lstrip())]; tail = s[len(s.rstrip()):]
            return lead + tr[key] + tail
        if not KEEP.match(key): missing.add(key)
        return s
    (root / 'lv').mkdir(exist_ok=True)
    for fn in PAGES:
        soup = BeautifulSoup((root / fn).read_text(), 'html.parser')
        soup.html['lang'] = 'lv'
        for node in soup.find_all(string=True):
            if isinstance(node, Comment) or node.parent.name in ('script', 'style'): continue
            new = t(str(node))
            if new != str(node): node.replace_with(new)
        for el in soup.find_all(True):
            for a in ATTRS:
                if el.has_attr(a) and el[a].strip(): el[a] = t(el[a])
            if el.name == 'meta' and el.get('name') == 'description': el['content'] = t(el['content'])
            for a in ('href', 'src'):
                if el.has_attr(a) and ASSET.match(el[a]): el[a] = '../' + el[a]
            if el.has_attr('srcset') and ASSET.match(el['srcset']): el['srcset'] = '../' + el['srcset']
        for l in soup.select('link[rel=alternate]'):
            l['hreflang'] = 'en'; l['href'] = '../' + fn
        en, lv = soup.select('.lang a')
        en['href'] = '../' + fn; del en['aria-current']
        lv['href'] = fn; lv['aria-current'] = 'true'
        (root / 'lv' / fn).write_text(str(soup))
    print('built lv/ (%d pages)' % len(PAGES))
    if missing:
        print('UNTRANSLATED:'); [print('  ', m) for m in sorted(missing)]

if __name__ == '__main__':
    run()
