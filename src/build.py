import os
import re
import datetime
import json
import pytz
import markdown
from mdx_gfm import PartialGithubFlavoredMarkdownExtension


def get_title(html):
    ret = re.findall(
        r"<h1(\s[^>]*)*>\s*(.*)\s*</h1>",
        html,
        flags=re.IGNORECASE
    )
    return ret[0][-1] if len(ret) else ''


def get_updaed_at(html):
    ret = re.findall(
        r"<p(\s[^>]*)*>Update:\s*(.*)\s*</p>",
        html,
        flags=re.IGNORECASE
    )
    return ret[0][-1] if len(ret) else 'unknown'


def get_tags(html):
    ret = re.findall(
        r"(<p(\s[^>]*)*>Tag:\s*(.*)\s*</p>)",
        html,
        flags=re.IGNORECASE
    )
    return ret[-1][-1].lower().split() if len(ret) else []


def set_tag_links(html, cat, tags):
    el = '<p>Tag:'
    for tag in tags:
        el = f'{el} <a href="/{cat}/?tag={tag}">{tag}</a>'
    el = f'{el}</p>\n'

    ret = re.findall(
        r"(<p(\s[^>]*)*>Tag:\s*(.*)\s*</p>)",
        html,
        flags=re.IGNORECASE
    )
    return html.replace(ret[-1][0], el) if len(ret) else html

def save_html(tmpl, cat, md_path, sample=False):
    content = markdown.markdown(
        open(
            md_path,
            encoding='utf8'
        ).read(),
        extensions=[PartialGithubFlavoredMarkdownExtension()]
    ).replace(
        'class="language-mermaid"',
        'class="mermaid nohighlight"'
    )

    title = get_title(content)
    updated_at = get_updaed_at(content)
    tags = get_tags(content)
    content = set_tag_links(content, cat, tags)

    open(
        re.sub(r"\.md$", '.html', md_path, flags=re.IGNORECASE),
        'w',
        encoding='utf-8'
    ).write(
        tmpl.replace(
            '%%root%%',
            '../docs/' if sample else '/'
        ).replace(
            '%%title%%',
            f'{title} - ' if title else ''
        ).replace(
            '%%content%%',
            content
        )
    )

    return [title, updated_at, tags]


def sort_key_path(el):
    return el['path']

if __name__ == '__main__':
    src = os.path.dirname(__file__)
    docs = os.path.join(src, '..', 'docs')
    categories = ['l', 'p', 't']
    meta_path = os.path.join(docs, 'meta.json')
    ts = datetime.datetime.now(
        pytz.timezone('Asia/Tokyo')
    ).isoformat()

    tmpl = open(
        os.path.join(src, 'template.html'),
        encoding='utf8'
    ).read().replace(
        '%%copyright_year%%',
        ts[0:4]
    )

    pages = []

    save_html(
        tmpl,
        't',
        os.path.join(src, 'sample.md'),
        sample=True
    )

    for cat in categories:
        for root, dirs, files in os.walk(os.path.join(docs, cat)):
            for file in files:
                if re.match(r".*\.md$", file, flags=re.IGNORECASE):
                    dir = os.path.relpath(root, docs).replace('\\', '/')
                    path = f'{dir}/{file}'
                    pages.append({
                        'cat': cat,
                        'path': path,
                        'title': '',
                        'updated_at': 'unkown',
                        'tags': [],
                    })

    pages.sort(key=sort_key_path)
    meta = {
        'pages': pages
    }
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)
