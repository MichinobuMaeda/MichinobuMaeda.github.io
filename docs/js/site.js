function onBodyLoading() {
  filterByTag();
  setTagLink();
  showUpdates(5);
}

function filterByTag() {
  const tag = location.search.substring(1).split('&')
    .filter(item => item.startsWith('tag='))
    .reduce((ret, cur) => ret || cur.replace('tag=', ''), null);

  const tagAll = document.getElementById('tag-ALL')
  if (tagAll) {
    tagAll.style.display = tag ? 'block' : 'none';
  }

  if (!tag) return;

  const links = document.getElementById('toc').getElementsByTagName('a');

  for (i = 0; i < links.length; i++) {
    const tags = links[i].getAttribute('title') || '';
    const item = links[i].parentNode;

    if ((item.nodeName || '').toUpperCase() !== 'LI') continue;

    item.style.display = (tag === 'ALL' || ` ${tags} `.includes(` ${tag} `)) ? 'list-item' : 'none';
  }

  if (document.getElementById('tag-cloud')) {
    const tags = document.getElementById('tag-cloud').children;

    for (i = 0; i < tags.length; i++) {
      tags[i].style.backgroundColor = tags[i].id === `tag-${tag}` ? '#ffdddd' : 'none';
    }
  }
}

function setTagLink() {
  const tags = Array.from(document.getElementsByTagName('p'))
    .reduce((ret, cur) => cur.textContent?.trim().startsWith('Tag:') ? cur : ret, null);

  if (!tags) return;

  tags.innerHTML = 'Tag: ' + tags.textContent.replace('Tag:', '')
    .trim().split(/\s/)
    .filter(item => item)
    .map(item => item.toLowerCase())
    .map(item => `<a href="/${location.pathname.replace(/^\//, '').replace(/\/.*/, '')}/?tag=${item}">${item}</a>`)
    .join(' ');
}

function showUpdates(count) {
  const http = new XMLHttpRequest();
  http.overrideMimeType("application/json");
  http.open("GET", '/meta.json', true);
  http.onreadystatechange = () => {
    if (http.readyState === 4 && http.status == "200") {
      meta = JSON.parse(http.responseText);
      pages = meta.pages.filter(page => page.updated_at.match(/^2/));
      pages.sort((a, b) => a.updated_at === b.updated_at ? 0 : a.updated_at < b.updated_at ? 1 : -1);
      li = '';
      for (i = 0; i < count && i < pages.length; ++i) {
        li += '<li>' + pages[i].updated_at + '<br><a href="/' + pages[i].path + '">' + pages[i].title + '</a></li>'
      }
      document.getElementById('updates').innerHTML = li;
    }
  }
  http.send(null);
}
