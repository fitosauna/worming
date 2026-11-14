import glob, json, re
from bs4 import BeautifulSoup, NavigableString, Comment
ATTRS = ['alt', 'aria-label', 'placeholder', 'content', 'title']
def strings(html):
    soup = BeautifulSoup(html, 'html.parser'); out = []
    for t in soup.find_all(string=True):
        if isinstance(t, Comment) or t.parent.name in ('script', 'style'): continue
        s = re.sub(r'\s+', ' ', str(t)).strip()
        if s: out.append(s)
    for el in soup.find_all(True):
        for a in ATTRS:
            if el.has_attr(a) and el[a].strip():
                if a == 'content' and el.get('name') != 'description': continue
                out.append(re.sub(r'\s+', ' ', el[a]).strip())
    return out
if __name__ == '__main__':
    seen = []
    for f in ['index.html','product.html','applications.html','quality.html','about.html','quote.html','privacy.html','company.html']:
        for s in strings(open(f).read()):
            if s not in seen: seen.append(s)
    json.dump(seen, open('/tmp/strings.json','w'), ensure_ascii=False, indent=0)
    print(len(seen), sum(len(s) for s in seen))
