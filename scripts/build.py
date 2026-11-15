"""Build static policy pages with the Python standard library. Use --check in reviews."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://bitlap.org/sf-app-privacy/'
LANGUAGES = {'zh-CN': '简体中文', 'en': 'English'}


def frame(lang, title, content, filename):
    items = []
    for code, label in LANGUAGES.items():
        current = ' aria-current="page"' if code == lang else ''
        items.append(f'<a href="{code}.html" hreflang="{code}"{current}>{label}</a>')
    links = ''.join(items)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="幻兔 / SnapFlow 隐私政策 · Privacy Policy">
  <title>{html.escape(title)}</title>
  <link rel="canonical" href="{BASE}{filename}">
  <link rel="alternate" hreflang="zh-CN" href="{BASE}zh-CN.html">
  <link rel="alternate" hreflang="en" href="{BASE}en.html">
  <link rel="alternate" hreflang="x-default" href="{BASE}">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip" href="#policy">跳至正文 / Skip to content</a>
  <header><a class="brand" href="index.html">幻兔 <span>SnapFlow</span></a>
    <nav aria-label="语言 / Language">{links}</nav>
  </header>
  <main id="policy">{content}</main>
  <footer><a href="mailto:dreamylost@outlook.com">dreamylost@outlook.com</a>
    <span>幻兔 / SnapFlow · Privacy</span></footer>
</body>
</html>
'''


def render():
    policies = {code: json.loads((ROOT/'policies'/f'{code}.json').read_text()) for code in LANGUAGES}
    baseline = [(s['id'], len(s['paragraphs'])) for s in policies['zh-CN']['sections']]
    outputs = {}
    for code, policy in policies.items():
        assert policy['language'] == code and policy['updated'] == '2026-11-15'
        assert [(s['id'], len(s['paragraphs'])) for s in policy['sections']] == baseline
        assert len({s['id'] for s in policy['sections']}) == len(baseline)
        title = '幻兔隐私政策' if code == 'zh-CN' else 'SnapFlow Privacy Policy'
        date = '更新及生效日期：2026年11月15日' if code == 'zh-CN' else 'Updated and effective: November 15, 2026'
        toc = ''.join(f'<li><a href="#{s["id"]}">{html.escape(s["title"])}</a></li>' for s in policy['sections'])
        sections = ''.join(f'<section aria-labelledby="{s["id"]}"><h2 id="{s["id"]}">{html.escape(s["title"])}</h2>'
                           + ''.join(f'<p>{p}</p>' for p in s['paragraphs']) + '</section>' for s in policy['sections'])
        content = f'<h1>{title}</h1><p class="date">{date}</p><details><summary>{"目录" if code == "zh-CN" else "Contents"}</summary><ul>{toc}</ul></details>{sections}'
        outputs[f'{code}.html'] = frame(code, title, content, f'{code}.html')
    outputs['index.html'] = frame('zh-CN', '幻兔 / SnapFlow · 隐私政策 / Privacy Policy', '''
    <h1>隐私政策<br><span lang="en">Privacy Policy</span></h1>
    <p>了解幻兔如何处理账号、照片与云端内容、推荐记录、消息及系统通知，以及如何联系我们提出数据请求。</p>
    <p lang="en">Learn how SnapFlow handles accounts, photos and cloud content, recommendations, messages and notifications, and how to contact us about your data.</p>
    <div class="choices"><a href="zh-CN.html" lang="zh-CN">阅读简体中文版 <span>→</span></a><a href="en.html" lang="en">Read in English <span>→</span></a></div>
    <p class="date">2026年11月15日 · <span lang="en">November 15, 2026</span></p>''', '')
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for filename, content in render().items():
        target = ROOT/filename
        if args.check:
            assert target.exists() and target.read_text() == content, f'Regenerate {filename}'
        else:
            target.write_text(content)
    print('Policy pages are current' if args.check else 'Built three static policy pages')
