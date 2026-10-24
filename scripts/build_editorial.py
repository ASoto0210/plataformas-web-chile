"""Build the public site; editorial source and internal documents never ship."""
import argparse
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote
from xml.etree.ElementTree import Element, SubElement, tostring

DOMAIN = 'https://plataformasweb.cl'
CATEGORIES = ('Elegir', 'Operar', 'Proteger', 'Mejorar')


def validate(item):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['slug']):
        raise ValueError('Slug inválido: ' + item['slug'])
    for key in ('title', 'category', 'summary', 'status', 'sources'):
        if not item.get(key):
            raise ValueError('Falta ' + key)
    if item['category'] not in CATEGORIES:
        raise ValueError('Categoría inválida')
    for source in item['sources']:
        if not source['url'].startswith('https://'):
            raise ValueError('Fuente sin HTTPS')
    date.fromisoformat(item['publish_on'])
    date.fromisoformat(item['reviewed_on'])
    if item.get('published_on'):
        date.fromisoformat(item['published_on'])


def eligible(item, today):
    validate(item)
    reviewed = date.fromisoformat(item['reviewed_on'])
    return (item['status'] == 'ready'
            and date.fromisoformat(item['publish_on']) <= today
            and reviewed <= today
            and (today - reviewed).days <= item.get('review_days', 30))


def support_available(item, today):
    if not item.get('support_on') or date.fromisoformat(item['support_on']) > today:
        return False
    if item.get('support_published_on'):
        return date.fromisoformat(item['support_published_on']) <= today
    reviewed = date.fromisoformat(item.get('support_reviewed_on', item['reviewed_on']))
    return (item['status'] == 'ready' and reviewed <= today
            and (today - reviewed).days <= item.get('support_review_days', item.get('review_days', 30)))


def merge_history(items, previous):
    if not isinstance(previous, dict):
        raise ValueError('Historial inválido')
    by_slug = {item['slug']: item for item in items}
    missing = set(previous) - set(by_slug)
    if missing:
        raise ValueError('Retirada no autorizada de URLs publicadas: ' + ', '.join(sorted(missing)))
    for slug, entry in previous.items():
        item = by_slug[slug]
        if item['status'] != 'ready':
            raise ValueError('Una URL publicada no puede volver a borrador sin plan de retirada: ' + slug)
        entry = {'published_on': entry} if isinstance(entry, str) else entry
        if not isinstance(entry, dict) or not entry.get('published_on'):
            raise ValueError('Historial inválido para ' + slug)
        for field in ('published_on', 'support_published_on'):
            if entry.get(field):
                date.fromisoformat(entry[field])
                item[field] = entry[field]


def e(value):
    return html.escape(str(value), quote=True)


def document(title, description, path, content, schema, css_path):
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Plataformas Web Chile</title><meta name="description" content="{e(description)}">
<link rel="canonical" href="{DOMAIN}{path}"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fuentes/fuentes-v4.css"><link rel="stylesheet" href="{css_path}">
<meta name="theme-color" content="#100E0B"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}"><meta property="og:url" content="{DOMAIN}{path}">
<meta property="og:type" content="{'article' if schema['@type'] == 'Article' else 'website'}">
<meta property="og:image" content="{DOMAIN}/og-image.png"><meta property="og:image:alt" content="Plataformas Web Chile">
<meta property="og:site_name" content="Plataformas Web Chile"><meta property="og:locale" content="es_CL">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{DOMAIN}/og-image.png">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', chr(92) + 'u003c')}</script>
</head><body><a class="skip" href="#contenido">Ir al contenido</a>
<div class="shell"><header class="top"><a class="brand" href="/"><img src="/icono-color.svg" alt="" width="25" height="25">Plataformas Web Chile</a><nav aria-label="Navegación principal"><a href="/guias/">Guías</a><a href="/casos/stom/">Caso STOM</a><a href="/#contacto">Conversemos</a></nav></header>
<main id="contenido">{content}</main><footer class="foot"><span>Plataformas Web Chile · Santiago</span><a href="mailto:hola@plataformasweb.cl">hola@plataformasweb.cl</a><a href="/">Volver al inicio</a></footer></div>
<script src="/guias/editorial.js" defer></script></body></html>'''


def render_article(item, visible, today):
    path = '/guias/' + item['slug'] + '/'
    published = item.get('published_on', item['publish_on'])
    stale = (today - date.fromisoformat(item['reviewed_on'])).days > item.get('review_days', 30)
    notice = '<aside class="notice"><strong>Revisión pendiente.</strong> Esta guía conserva la fecha de su última comprobación. Consulta las fuentes oficiales antes de decidir sobre versiones, tarifas o requisitos actuales.</aside>' if stale else ''
    support = item.get('support', '') if support_available(item, today) else ''
    related = [a for a in visible if a['slug'] != item['slug']]
    related.sort(key=lambda a: a['category'] != item['category'])
    links = ''.join(f'<li><a href="/guias/{e(a["slug"])}/">{e(a["title"])}</a></li>' for a in related[:2])
    sources = ''.join(f'<li><a href="{e(s["url"])}">{e(s["title"])}</a></li>' for s in item['sources'])
    content = f'''<nav class="crumb" aria-label="Ruta de navegación"><a href="/">Inicio</a><span aria-hidden="true">/</span><a href="/guias/">Guías</a><span aria-hidden="true">/</span><span>{e(item['category'])}</span></nav>
<article class="article"><header class="intro"><p class="eyebrow">{e(item['category'])} · Guía práctica</p><h1>{e(item['title'])}</h1><p class="lead">{e(item['summary'])}</p><p class="meta">Por Plataformas Web Chile · Publicado <time datetime="{e(published)}">{e(published)}</time><br>Fuentes revisadas <time datetime="{e(item['reviewed_on'])}">{e(item['reviewed_on'])}</time></p><button class="button secondary" type="button" data-print>Imprimir o guardar PDF</button></header>
{notice}<div class="prose">{item['body']}{support}</div>
<section class="sources" aria-labelledby="fuentes"><h2 id="fuentes">Fuentes y alcance</h2><p>Las funciones y condiciones de un proveedor pueden cambiar. Separamos las referencias de nuestras recomendaciones operativas.</p><ul>{sources}</ul></section>
<aside class="cta"><p class="eyebrow">Tu siguiente paso</p><h2>{e(item.get('cta', 'Revisemos tu caso antes de decidir.'))}</h2><p>Cuéntanos tu catálogo, plataforma actual y el problema que necesitas resolver. No envíes contraseñas ni datos de clientes.</p><a class="button" data-contact href="mailto:hola@plataformasweb.cl?subject={quote('Consulta sobre ' + item['title'])}">Conversar sobre mi plataforma</a></aside>
{'<section class="related"><h2>Para seguir revisando</h2><ul>' + links + '</ul></section>' if links else ''}</article>'''
    schema = {'@context': 'https://schema.org', '@type': 'Article', 'headline': item['title'],
              'description': item['summary'], 'datePublished': published, 'dateModified': item['reviewed_on'],
              'inLanguage': 'es-CL', 'mainEntityOfPage': DOMAIN + path,
              'author': {'@type': 'Organization', 'name': 'Plataformas Web Chile', 'url': DOMAIN + '/'},
              'image': DOMAIN + '/og-image.png'}
    return document(item['title'], item['summary'], path, content, schema, '/guias/editorial.css')


def render_index(items):
    rows = ''
    for category in CATEGORIES:
        group = [a for a in items if a['category'] == category]
        if not group:
            continue
        group.sort(key=lambda a: a.get('published_on', a['publish_on']), reverse=True)
        entries = ''.join(f'''<li><a class="entry" href="/guias/{e(a['slug'])}/"><div><p class="meta">{e(a.get('published_on', a['publish_on']))}</p><h3>{e(a['title'])}</h3><p>{e(a['summary'])}</p></div><span class="arrow" aria-hidden="true">↗</span></a></li>''' for a in group)
        rows += f'<section class="group"><h2>{e(category)}</h2><ul class="entries">{entries}</ul></section>'
    content = f'''<div class="hub-intro"><p class="eyebrow">La plataforma, entendida</p><h1>Decide mejor.<br>Opera con confianza.</h1><p class="lead">Guías para elegir, mantener y mejorar una tienda online. Pasos concretos, fuentes a la vista y ejemplos para negocios chilenos.</p><p class="meta">Por Plataformas Web Chile · Catálogos complejos, decisiones claras.</p></div>
{rows or '<p>Estamos preparando las primeras guías.</p>'}
<section class="cta"><h2>Tu catálogo tiene sus propias reglas.</h2><p>Si buscas por vehículo, medida o compatibilidad, revisemos cómo llega tu cliente al producto correcto.</p><a class="button" href="/#contacto">Cuéntanos tu caso</a><a class="text-link" href="/casos/stom/">Ver el caso STOM →</a></section>'''
    schema = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Guías de Plataformas Web Chile',
              'url': DOMAIN + '/guias/', 'hasPart': [{'@type': 'Article', 'headline': a['title'], 'url': DOMAIN + '/guias/' + a['slug'] + '/'} for a in items]}
    return document('Guías para elegir y cuidar tu plataforma', 'Decisiones, costos, seguridad y operación de tiendas online: guías con fuentes para PyMEs chilenas.', '/guias/', content, schema, '/guias/editorial.css')


def build(root, out, today, articles):
    root, out = Path(root).resolve(), Path(out).resolve()
    if out == root or root.is_relative_to(out):
        raise ValueError('El destino no puede contener el repositorio')
    if out.exists() and any(out.iterdir()):
        raise ValueError('El destino debe estar vacío; no se borran archivos existentes')
    out.mkdir(parents=True, exist_ok=True)
    for name in ('fuentes', 'casos', 'glosario', 'email'):
        if (root / name).is_dir():
            shutil.copytree(root / name, out / name)
    for source in root.iterdir():
        if source.is_file() and (source.name in ('index.html', 'CNAME') or source.suffix in ('.svg', '.png', '.ico')):
            shutil.copy2(source, out / source.name)
    signature = root / 'docs' / 'firma-correo.html'
    if signature.exists():
        (out / 'docs').mkdir()
        shutil.copy2(signature, out / 'docs' / signature.name)
    guias = out / 'guias'
    guias.mkdir()
    for name in ('editorial.css', 'editorial.js'):
        if (root / 'guias' / name).exists():
            shutil.copy2(root / 'guias' / name, guias / name)
    visible, report, slugs = [], [], set()
    for item in articles:
        validate(item)
        if item['slug'] in slugs:
            raise ValueError('Slug duplicado')
        slugs.add(item['slug'])
        was_published = (item.get('published_on') and date.fromisoformat(item['published_on']) <= today)
        if eligible(item, today) or (was_published and item['status'] == 'ready'):
            item = dict(item)
            item.setdefault('published_on', today.isoformat())
            visible.append(item)
        else:
            report.append(item['slug'] + ': pendiente de fecha o revisión')
    for item in visible:
        if support_available(item, today):
            item.setdefault('support_published_on', today.isoformat())
        destination = guias / item['slug']
        destination.mkdir()
        if item.get('existing'):
            text = (root / 'guias' / item['slug'] / 'index.html').read_text(encoding='utf-8')
            if (today - date.fromisoformat(item['reviewed_on'])).days > item.get('review_days', 30):
                text = text.replace('<article>', '<article><aside class="aviso"><p><strong>Revisión pendiente.</strong> Las fuentes se comprobaron por última vez el ' + e(item['reviewed_on']) + '. Consulta los avisos oficiales antes de aplicar versiones o medidas actuales.</p></aside>', 1)
            if support_available(item, today):
                text = text.replace('</article>', item.get('support', '') + '</article>', 1)
            (destination / 'index.html').write_text(text, encoding='utf-8')
        else:
            (destination / 'index.html').write_text(render_article(item, visible, today), encoding='utf-8')
    (guias / 'index.html').write_text(render_index(visible), encoding='utf-8')
    published = {a['slug']: {k: a[k] for k in ('published_on', 'support_published_on') if a.get(k)} for a in visible}
    (guias / 'publicadas.json').write_text(json.dumps(published, indent=2), encoding='utf-8')
    xml = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    urls = ['/', '/guias/', '/casos/stom/', '/glosario/']
    urls = [u for u in urls if (out / u.strip('/') / 'index.html').exists()]
    urls += ['/guias/' + a['slug'] + '/' for a in visible]
    for url in urls:
        SubElement(SubElement(xml, 'url'), 'loc').text = DOMAIN + url
    (out / 'sitemap.xml').write_bytes(tostring(xml, encoding='utf-8', xml_declaration=True))
    (out / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + DOMAIN + '/sitemap.xml\n', encoding='utf-8')
    (out / '.nojekyll').touch()
    return visible, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', help='Fecha de prueba, YYYY-MM-DD; omitir en producción')
    parser.add_argument('--output', default='_site')
    parser.add_argument('--previous', help='Registro del despliegue anterior, para conservar URLs')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    today = date.fromisoformat(args.date) if args.date else date.today()
    items = json.loads((root / '_editorial' / 'catalog.json').read_text(encoding='utf-8'))
    previous = json.loads(Path(args.previous).read_text(encoding='utf-8')) if args.previous else {}
    merge_history(items, previous)
    for item in items:
        for field, target in [('body_file', 'body'), ('support_file', 'support')]:
            if item.get(field):
                body_path = (root / '_editorial' / item[field]).resolve()
                if not body_path.is_relative_to(root / '_editorial'):
                    raise ValueError('Contenido fuera de _editorial')
                item[target] = body_path.read_text(encoding='utf-8')
    visible, report = build(root, root / args.output, today, items)
    print(f'{len(visible)} guías disponibles en {args.output}')
    print('\n'.join(report))


if __name__ == '__main__':
    main()
