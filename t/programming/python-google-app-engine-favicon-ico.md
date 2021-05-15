Python の Google App Engine で favicon.ico
=====

Update: unknown

Google App Engine の管理コンソールにたくさん出てくる favicon.ico 。。。じゃまです。



でも、 Python の場合どうやって置くのかがよくわかりません。 `app.yaml` で静的なコンテンツを置くディレクトリを指定することはできるのですが、トップにこうやって `/favicon.ico` 置くにはどうしたらいいの？

なかったので調べてみました。



How do you generate the list of URIs showing the most errors in my application's admin console?

https://developers.google.com/appengine/kb/general#erroruris



Static File Handlers

https://developers.google.com/appengine/docs/python/config/appconfig#Static_File_Handlers



ようするに `app.yaml` にこんな感じで設定しろということです。


```
- url: /favicon\.ico
  static_files: static/favicon.ico
  upload: static/favicon\.ico
```


`static_files` とは別に upload を指定していますが、 Google さんのサンプルを見た限りではありがたみを感じませんでした。


```
  static_files: archives/\2/items/\1
```


のような形があるので、この値を正規表現として使ってファイルを特定することはできないということのようです。作った人の気持ちはなんとなくわかります。
