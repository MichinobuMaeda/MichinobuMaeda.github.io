import os
import re
import datetime
import json
import math
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


def render_markdown(path):
    return markdown.markdown(
        open(
            path,
            encoding='utf8'
        ).read(),
        extensions=[PartialGithubFlavoredMarkdownExtension()]
    ).replace(
        'class="language-mermaid"',
        'class="mermaid nohighlight"'
    )


def save_html(tmpl, cat, path, content, sample=False):
    title = get_title(content)
    updated_at = get_updaed_at(content)
    tags = get_tags(content)

    open(
        path,
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

    return (title, updated_at, tags)


def sort_key_path(el):
    return el['path']


def sort_key_updated_at(el):
    ts = el['updated_at']
    path = el['path']
    return ts if re.match(r"2.*", ts) else f' {path}'


def generate_cat_index(pages, cat, title):
    pages.sort(key=sort_key_updated_at, reverse=True)

    html = f'<h1>{title}</h1>\n'

    html = f'{html}<ul id="tag-cloud">\n'
    cloud = {}
    for page in pages:
        if page['cat'] == cat:
            tags = page['tags']
            for tag in tags:
                if tag in cloud:
                    cloud[tag] += 1
                else:
                    cloud[tag] = 1
    tag_names = list(cloud.keys())
    tag_names.sort()
    for name in tag_names:
        size = min(math.ceil(math.log(cloud[name], 2)) + 1, 9)
        html = f'{html}<li id="tag-{name}"><a href="/{cat}/?tag={name}" class="tag-{size}">{name}</a></li>'
    html = f'{html}</ul>\n'

    if len(tag_names):
        html = f'{html}<p id="tag-ALL"><a href="/{cat}/">フィルタ解除</a></p>\n'

    html = f'{html}<ul id="toc">\n'
    for page in pages:
        if page['cat'] == cat:
            updated_at = page['updated_at']
            title = page['title']
            path = page['path']
            tags = ' '.join(page['tags'])
            html = f'{html}<li>{updated_at} <a href="/{path}" title="{tags}">{title}</a></li>\n'
    html = f'{html}</ul>\n'
    return html


if __name__ == '__main__':
    src = os.path.dirname(__file__)
    docs = os.path.join(src, '..', 'docs')
    categories = {
        'l': '厚生部',
        'p': '政治局',
        't': '工作室',
    }
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

    md_path = os.path.join(src, 'sample.md')
    save_html(
        tmpl,
        't',
        re.sub(r"\.md$", '.html', md_path, flags=re.IGNORECASE),
        render_markdown(md_path),
        sample=True
    )

    md_path = os.path.join(docs, 'index.md')
    save_html(
        tmpl,
        None,
        re.sub(r"\.md$", '.html', md_path, flags=re.IGNORECASE),
        render_markdown(md_path),
    )

    for cat in categories.keys():
        for root, dirs, files in os.walk(os.path.join(docs, cat)):
            for file in files:
                if re.match(r".*\.md$", file, flags=re.IGNORECASE):
                    md_path = os.path.join(root, file)
                    (title, updated_at, tags) = save_html(
                        tmpl,
                        't',
                        re.sub(r"\.md$", '.html', md_path,
                               flags=re.IGNORECASE),
                        render_markdown(md_path),
                    )

                    dir = os.path.relpath(root, docs).replace('\\', '/')
                    pages.append({
                        'cat': cat,
                        'path': re.sub(r"\.md$", '.html', f'{dir}/{file}', flags=re.IGNORECASE),
                        'title': title if title else 'unknown',
                        'updated_at': updated_at,
                        'tags': tags,
                    })

    for cat in categories.keys():
        save_html(
            tmpl,
            't',
            os.path.join(docs, cat, 'index.html'),
            generate_cat_index(pages, cat, categories[cat]),
        )

    pages.sort(key=sort_key_path)
    meta = {
        'pages': pages
    }
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)
