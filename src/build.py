import os
import re
import shutil
from pathlib import Path
import datetime
import json
import math
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pytz
import markdown
from mdx_gfm import PartialGithubFlavoredMarkdownExtension


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class MdData:
    def __init__(self, path):
        self.path = path
        self.src = open(self.path, encoding='utf8').read()
        self.title = ''
        self.updated_at = ''
        self.tags = []

        first_line = ''
        second_line = ''

        for line in self.src.split('\n'):
            if first_line == '':
                first_line = line
            elif second_line == '':
                second_line = line

            # Get first '# '
            if self.title == '':
                ret = re.match(r"^#\s+(?P<text>.+)\s*$", line, re.IGNORECASE)
                if ret and ret.group('text'):
                    self.title = ret.group('text')

            # Get first 'Update: '
            if self.updated_at == '':
                ret = re.match(r"^Update:\s*(?P<text>.+)\s*$",
                               line, re.IGNORECASE)
                if ret and ret.group('text'):
                    self.updated_at = ret.group('text')

            # Get last 'Tag: '
            ret = re.match(r"^Tag:\s*(?P<text>.+)\s*$", line, re.IGNORECASE)
            if ret:
                self.tags = ret.group('text').lower().split()

        if self.title == '' and re.match(r"^=+$", second_line):
            self.title = first_line


def render_markdown(md):
    return markdown.markdown(
        md,
        extensions=[PartialGithubFlavoredMarkdownExtension()]
    ).replace(
        'class="language-mermaid"',
        'class="mermaid nohighlight"'
    )


def get_dest_path(dest, docs, md_path):
    return re.sub(
        r"\.md$",
        '.html',
        os.path.join(dest, os.path.relpath(md_path, docs)),
        flags=re.IGNORECASE,
    )


def save_html(path, html):
    open(path, 'w', encoding='utf-8').write(html)


def save_meta(dest, meta):
    with open(os.path.join(dest, 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)


def sort_key_updated_at(el):
    ret = re.match(r"^2.*$", el['updated_at'])
    ts = ret.group(0) if ret else ''
    path = el['path']
    return f'{ts} {path}'


def generate_tag_cloud_data(pages, cat):
    cloud = {}
    for page in pages:
        if page['cat'] == cat.id:
            tags = page['tags']
            for tag in tags:
                if tag in cloud:
                    cloud[tag] += 1
                else:
                    cloud[tag] = 1
    tag_names = list(cloud.keys())
    tag_names.sort()

    ret = []
    for name in tag_names:
        ret.append({
            'name': name,
            'size': min(math.ceil(math.log(cloud[name], 2)) + 1, 9),
        })

    return ret


if __name__ == '__main__':
    src = os.path.dirname(__file__)
    docs = os.path.join(src, '..', 'docs')
    dest = os.path.join(src, '..', '_site')
    year = str(datetime.datetime.now(pytz.timezone('Asia/Tokyo')).year)
    categories = [
        Category('t', '工作室'),
        Category('l', '厚生部'),
        Category('p', '政治局'),
    ]
    meta = {'pages': []}

    jinja = Environment(
        loader=FileSystemLoader(src),
        autoescape=select_autoescape()
    )
    layout = jinja.get_template('template_layout.html')
    cat_index = jinja.get_template('template_cat_index.html')

    if not os.path.exists(dest):
        Path(dest).mkdir(parents=True, exist_ok=True)

    md = MdData(os.path.join(src, 'sample.md'))
    save_html(
        get_dest_path(dest, docs, md.path),
        layout.render({
            'categories': categories,
            'year': year,
            'root': '../docs/',
            'title': md.title,
            'content': render_markdown(md.src),
        })
    )

    md = MdData(os.path.join(docs, 'index.md'))
    save_html(
        get_dest_path(dest, docs, md.path),
        layout.render({
            'categories': categories,
            'year': year,
            'root': '/',
            'title': md.title,
            'content': render_markdown(md.src),
        })
    )

    if not os.path.exists(dest):
        Path(dest).mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(docs):
        cat = os.path.relpath(root, docs).split(os.path.sep)[0]
        trg = os.path.join(dest, os.path.relpath(root, docs))
        if not os.path.exists(trg):
            Path(trg).mkdir(parents=True, exist_ok=True)
        for file in files:
            if re.match(r".*\.md$", file, flags=re.IGNORECASE):
                md = MdData(os.path.join(root, file))
                save_html(
                    get_dest_path(dest, docs, md.path),
                    layout.render({
                        'categories': categories,
                        'year': year,
                        'root': '/',
                        'title': md.title,
                        'content': render_markdown(md.src),
                    })
                )
                if cat != '.':
                    meta['pages'].append({
                        'cat': cat,
                        'path': os.path.relpath(
                            get_dest_path(dest, docs, md.path), dest
                        ).replace('\\', '/'),
                        'title': md.title,
                        'updated_at': md.updated_at,
                        'tags': md.tags,
                    })
            else:
                shutil.copyfile(
                    os.path.join(root, file),
                    get_dest_path(dest, docs, os.path.join(root, file)),
                )

    meta['pages'].sort(key=sort_key_updated_at, reverse=True)

    for cat in categories:
        save_html(
            os.path.join(dest, cat.id, 'index.html'),
            layout.render({
                'categories': categories,
                'year': year,
                'root': '/',
                'title': cat.name,
                'content': cat_index.render({
                    'title': cat.name,
                    'cat': cat.id,
                    'tag_cloud': generate_tag_cloud_data(meta['pages'], cat),
                    'pages': [page for page in meta['pages'] if page['cat'] == cat.id],
                }),
            })
        )

    save_meta(dest, meta)
