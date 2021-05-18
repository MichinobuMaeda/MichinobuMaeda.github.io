function filterByTag(tag) {
  const links = document.getElementsByTagName('a')
  for (i = 0; i < links.length; i++) {
    const tags = links[i].getAttribute('title') || ''
    const item = links[i].parentNode
    if ((item.nodeName || '').toUpperCase() !== 'LI') { continue; }
    item.style.display = (tag === 'ALL' || ` ${tags} `.includes(` ${tag} `)) ? 'list-item' : 'none'
  }
  const tags = document.getElementById('tag-cloud').children
  for (i = 0; i < tags.length; i++) {
    tags[i].style.borderBottom = tags[i].id === `tag-${tag}` ? 'solid 2px #0000ff' : 'none'
  }
  document.getElementById('tag-ALL').style.display = tag === 'ALL' ? 'none' : 'inline'
}
