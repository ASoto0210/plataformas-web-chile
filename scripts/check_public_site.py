"""Check public HTML, internal destinations and metadata without network calls."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs, self.ids, self.schemas = [], set(), []
        self.h1 = 0
        self.canonical = None
        self.json_script = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a['href']
        for key in ('href', 'src'):
            if a.get(key):
                self.refs.append(a[key])
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.json_script = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.json_script = False

    def handle_data(self, data):
        if self.json_script and data.strip():
            self.schemas.append(json.loads(data))


def check(root):
    root = Path(root).resolve()
    errors = []
    pages = {p: Page(p.read_text(encoding='utf-8')) for p in root.rglob('*.html')}
    for path, page in pages.items():
        rel = path.relative_to(root).as_posix()
        public_path = '/' + rel
        for ref in page.refs:
            url = urlsplit(urljoin('https://plataformasweb.cl' + public_path, ref))
            if url.scheme not in ('http', 'https') or url.netloc not in ('plataformasweb.cl', 'www.plataformasweb.cl'):
                continue
            target = (root / unquote(url.path).lstrip('/')).resolve()
            if not target.is_relative_to(root):
                errors.append(rel + ': ruta fuera del sitio')
                continue
            if target.is_dir():
                target /= 'index.html'
            if not target.exists():
                errors.append(rel + ': destino inexistente ' + ref)
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(rel + ': ancla inexistente ' + ref)
        if rel.startswith('guias/') and path.name == 'index.html':
            if page.h1 != 1 or not page.canonical or not page.schemas:
                errors.append(rel + ': falta H1 único, canonical o JSON-LD')
            expected = 'https://plataformasweb.cl/' + rel.removesuffix('index.html')
            if page.canonical != expected:
                errors.append(rel + ': canonical incorrecto')
    for name in ('_editorial', 'scripts', 'tests', '.git', 'docs/estrategia-editorial-2026-10-23.md'):
        if (root / name).exists():
            errors.append('Archivo interno publicado: ' + name)
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'OK: {len(pages)} páginas, destinos internos y metadatos de guías.')


if __name__ == '__main__':
    check(sys.argv[1] if len(sys.argv) > 1 else '_site')
