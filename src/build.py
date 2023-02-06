import os
import re
import datetime
import json
import math
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
        self.md = open(self.path, encoding='utf8').read()
        self.title = ''
        self.updated_at = ''
        self.tags = []

        first_line = ''
        second_line = ''
        for line in self.md.split('\n'):
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

    def get_html(self):
        return markdown.markdown(
            self.md,
            extensions=[PartialGithubFlavoredMarkdownExtension()]
        ).replace(
            'class="language-mermaid"',
            'class="mermaid nohighlight"'
        )

    def get_html_path(self):
        return re.sub(r"\.md$", '.html', self.path, flags=re.IGNORECASE)


def save_html_from_md(tmpl, md, sample=False):
    save_html(
        tmpl,
        md.get_html_path(),
        md.get_html(),
        md.title,
        sample
    )


def save_html(tmpl, path, content, title, sample=False):
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


def sort_key_updated_at(el):
    ret = re.match(r"^2.*$", el['updated_at'])
    ts = ret.group(0) if ret else ''
    path = el['path']
    return f'{ts} {path}'


def generate_tag_cloud_data(pages, cat):
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

    ret = []
    for name in tag_names:
       ret.append({
            'name': name,
            'size': min(math.ceil(math.log(cloud[name], 2)) + 1, 9),
        })
    return ret


def generate_cat_index(pages, cat, title):
    html = f'<h1>{title}</h1>\n'

    tag_cloud = generate_tag_cloud_data(pages, cat)

    if tag_cloud:
        html = f'{html}<ul id="tag-cloud">\n'
        for tag in tag_cloud:
            name = tag['name']
            size = tag['size']
            html = f'{html}<li id="tag-{name}"><a href="/{cat}/?tag={name}" class="tag-{size}">{name}</a></li>'
        html = f'{html}</ul>\n'
        html = f'{html}<p id="tag-ALL"><a href="/{cat}/">フィルタ解除</a></p>\n'

    html = f'{html}<ul id="toc">\n'
    for page in pages:
        if page['cat'] == cat:
            updated_at = page['updated_at'] if page['updated_at'] else 'unknown'
            title = page['title']
            path = page['path']
            tags = ' '.join(page['tags'])
            html = f'{html}<li>{updated_at} <a href="/{path}" title="{tags}">{title}</a></li>\n'
    html = f'{html}</ul>\n'
    return html


if __name__ == '__main__':
    src = os.path.dirname(__file__)
    docs = os.path.join(src, '..', 'docs')
    meta_path = os.path.join(docs, 'meta.json')
    ts = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).isoformat()

    categories = [
        Category('t', '工作室'),
        Category('l', '厚生部'),
        Category('p', '政治局'),
    ]

    tmpl = open(
        os.path.join(src, 'template.html'),
        encoding='utf8'
    ).read().replace(
        '%%copyright_year%%',
        ts[0:4]
    )

    pages = []

    save_html_from_md(
        tmpl,
        MdData(os.path.join(src, 'sample.md')),
        sample=True
    )

    save_html_from_md(
        tmpl,
        MdData(os.path.join(docs, 'index.md')),
    )

    for cat in categories:
        for root, dirs, files in os.walk(os.path.join(docs, cat.id)):
            for file in files:
                if re.match(r".*\.md$", file, flags=re.IGNORECASE):
                    md = MdData(os.path.join(root, file))
                    save_html_from_md(tmpl, md)
                    pages.append({
                        'cat': cat.id,
                        'path': os.path.relpath(md.get_html_path(), docs).replace('\\', '/'),
                        'title': md.title,
                        'updated_at': md.updated_at,
                        'tags': md.tags,
                    })

    pages.sort(key=sort_key_updated_at, reverse=True)

    for cat in categories:
        save_html(
            tmpl,
            os.path.join(docs, cat.id, 'index.html'),
            generate_cat_index(pages, cat.id, cat.name),
            cat.name
        )

    # pages.sort(key=sort_key_path)
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump({'pages': pages}, f, ensure_ascii=False, indent=4)
