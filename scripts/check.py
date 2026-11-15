"""Validate generated HTML, bilingual structure, local links and no tracking assets."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from build import ROOT, render


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links = set(), []
        self.headings = 0
        self.language = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        assert tag not in ('script', 'iframe', 'form'), f'Unexpected {tag}'
        assert not any(key.startswith('on') for key in data), 'Inline script handler'
        if tag == 'html': self.language = data.get('lang')
        if tag == 'h2': self.headings += 1
        if 'id' in data:
            assert data['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(data['id'])
        for attr in ('href','src'):
            if attr in data: self.links.append(data[attr])
        if tag == 'link' and data.get('rel') == 'stylesheet':
            assert data.get('href') == 'style.css', 'No external stylesheet'


pages = {}
for filename, expected in render().items():
    data = (ROOT/filename).read_text()
    assert data == expected, f'Regenerate {filename}'
    page = Page()
    page.feed(data)
    assert page.language == ('en' if filename == 'en.html' else 'zh-CN')
    if filename != 'index.html':
        policy = json.loads((ROOT/'policies'/filename.replace('.html','.json')).read_text())
        assert page.headings == len(policy['sections']) == 12
    pages[filename] = page
for filename, page in pages.items():
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme:
            assert parsed.scheme in ('https','mailto'), f'Unsafe link {link}'
            continue
        target = parsed.path or filename
        assert (ROOT/target).is_file(), f'Missing target {target}'
        if parsed.fragment:
            assert parsed.fragment in pages[target].ids, f'Missing anchor {link}'
assert (ROOT/'.nojekyll').is_file()
print('PASS: bilingual sections, generated HTML, anchors, local assets and no script/form embeds')
