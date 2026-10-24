import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('editorial', ROOT / 'scripts' / 'build_editorial.py')
editorial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editorial)


def article(**changes):
    value = dict(slug='ejemplo', title='Ejemplo', category='Elegir', summary='Una guía.',
                 publish_on='2026-11-02', reviewed_on='2026-10-24', review_days=30,
                 status='ready', body='<h2>Decidir</h2><p>Contenido verificado.</p>',
                 sources=[{'title': 'Fuente', 'url': 'https://example.org/'}])
    value.update(changes)
    return value


class EditorialTests(unittest.TestCase):
    def test_date_gate_and_review_expiry(self):
        item = article()
        self.assertFalse(editorial.eligible(item, date(2026, 11, 1)))
        self.assertTrue(editorial.eligible(item, date(2026, 11, 2)))
        self.assertFalse(editorial.eligible(item, date(2026, 11, 25)))

    def test_legal_or_draft_never_publishes(self):
        for status in ['draft', 'legal-review']:
            self.assertFalse(editorial.eligible(article(status=status), date(2026, 11, 2)))

    def test_rejects_paths_and_future_review(self):
        for slug in ['../index', '/index', 'uno/dos', '']:
            with self.assertRaises(ValueError):
                editorial.validate(article(slug=slug))
        self.assertFalse(editorial.eligible(article(reviewed_on='2027-01-01'), date(2026, 11, 2)))

    def test_build_excludes_sources_and_future_urls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'source'
            root.mkdir()
            (root / 'index.html').write_text('<html><body>Inicio</body></html>', encoding='utf-8')
            (root / 'docs').mkdir()
            (root / 'docs' / 'private.md').write_text('INTERNAL', encoding='utf-8')
            out = Path(tmp) / 'site'
            editorial.build(root, out, date(2026, 11, 2), [article(), article(slug='futura', publish_on='2026-12-01')])
            self.assertTrue((out / 'guias' / 'ejemplo' / 'index.html').exists())
            self.assertFalse((out / 'guias' / 'futura').exists())
            self.assertFalse((out / 'docs').exists())
            sitemap = (out / 'sitemap.xml').read_text(encoding='utf-8')
            self.assertIn('/guias/ejemplo/', sitemap)
            self.assertNotIn('futura', sitemap)
            index = (out / 'guias' / 'index.html').read_text(encoding='utf-8')
            self.assertIn('ejemplo/', index)
            self.assertNotIn('futura/', index)

    def test_preserves_previously_published_but_marks_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'source'
            root.mkdir()
            (root / 'index.html').write_text('Inicio', encoding='utf-8')
            out = Path(tmp) / 'site'
            editorial.build(root, out, date(2026, 12, 1), [article(published_on='2026-11-02')])
            page = (out / 'guias' / 'ejemplo' / 'index.html').read_text(encoding='utf-8')
            self.assertIn('Revisión pendiente', page)

    def test_support_has_its_own_release_date(self):
        item = article(support_on='2026-11-05', support='<section>APOYO DEL JUEVES</section>')
        before = editorial.render_article(item, [item], date(2026, 11, 2))
        after = editorial.render_article(item, [item], date(2026, 11, 5))
        self.assertNotIn('APOYO DEL JUEVES', before)
        self.assertIn('APOYO DEL JUEVES', after)

    def test_new_support_does_not_bypass_expired_review(self):
        item = article(published_on='2026-11-02', review_days=1,
                       support_on='2026-11-05', support='APOYO NUEVO')
        self.assertNotIn('APOYO NUEVO', editorial.render_article(item, [item], date(2026, 11, 5)))
        item['support_published_on'] = '2026-11-05'
        self.assertIn('APOYO NUEVO', editorial.render_article(item, [item], date(2026, 12, 1)))

    def test_history_rejects_removal_and_hidden_status(self):
        with self.assertRaises(ValueError):
            editorial.merge_history([article()], {'retirada': '2026-11-02'})
        with self.assertRaises(ValueError):
            editorial.merge_history([article(status='draft')], {'ejemplo': '2026-11-02'})
        items = [article()]
        editorial.merge_history(items, {'ejemplo': {'published_on': '2026-11-02', 'support_published_on': '2026-11-05'}})
        self.assertEqual(items[0]['support_published_on'], '2026-11-05')


if __name__ == '__main__':
    unittest.main()
