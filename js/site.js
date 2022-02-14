function onBodyLoading() {
  filterByTag()
  setTagLink()
}

function filterByTag() {
  const tag = location.search.substring(1).split('&')
    .filter(item => item.startsWith('tag='))
    .reduce((ret, cur) => ret || cur.replace('tag=', ''), null)
  if (!tag) return
  const links = document.getElementsByTagName('a')
  for (i = 0; i < links.length; i++) {
    const tags = links[i].getAttribute('title') || ''
    const item = links[i].parentNode
    if ((item.nodeName || '').toUpperCase() !== 'LI') { continue; }
    item.style.display = (tag === 'ALL' || ` ${tags} `.includes(` ${tag} `)) ? 'list-item' : 'none'
  }
  if (document.getElementById('tag-cloud')) {
    const tags = document.getElementById('tag-cloud').children
    for (i = 0; i < tags.length; i++) {
      tags[i].style.borderBottom = tags[i].id === `tag-${tag}` ? 'solid 2px #0000ff' : 'none'
    }
    document.getElementById('tag-ALL').style.display = tag === 'ALL' ? 'none' : 'inline'
  }
}

function setTagLink() {
  const tags = Array.from(document.getElementsByTagName('p'))
    .reduce((ret, cur) => cur.textContent?.trim().startsWith('Tag:') ? cur : ret, null)
  console.log(tags)
  if (!tags) return
  tags.innerHTML = 'Tag: ' + tags.textContent.replace('Tag:', '')
    .trim().split(/\s/)
    .filter(item => item)
    .map(item => item.toLowerCase())
    .map(item => `<a href="/${location.pathname.replace(/^\//, '').replace(/\/.*/, '')}/?tag=${item}">${item}</>`)
    .join(' ')
}
