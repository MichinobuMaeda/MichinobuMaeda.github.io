# Movable Type に Twitter 投稿リンクを追加

Update: 2010-09-28

みちのぶのねぐら B面 に Twitter で感想など投稿してもらうためのリンクを追加しました。やることは簡単。「ブログ記事」に次のコードを追加しただけ。

```html
<div><a href="javascript:location.href='http://twitter.com/home?status='+`encodeURIComponent(document.title)+'%20'+encodeURIComponent(location.href);">ご感想を Twitter で</a></div>`
```

ん？ もしかして、こっちにも同じように入れたらいい？ ということで、ここで使っているテンプレートはフッタの編集ができるので、ページの一番下に入れました。

追記 : 2011-01-24

引っ越し先のA面、B面、C面ではこのリンクはやめました。

Tag: html twitter
