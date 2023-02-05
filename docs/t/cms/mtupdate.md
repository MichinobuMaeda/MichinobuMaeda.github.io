# Movable Type のアップグレード 4.32-ja → 5.02-ja

Update: 2010-07-18



`http://www.zippyzip.jp/` ( 閉鎖 ) の Movable Type をアップグレードします。元のバージョンは 4.32-ja で、新しいバージョンは 5.02-ja です。Movable Type の日本語版は本家サイトからダウンロードできますが、リンクが見あたりません。ダウンロードボタンのリンクのURLの en を ja に書き換えて [http://www.movabletype.org/downloads/stable/MTOS-5.02-ja.zip](http://www.movabletype.org/downloads/stable/MTOS-5.02-ja.zip) をダウンロードします。



アップグレードのガイドは [http://www.movabletype.org/documentation/installation/upgrade-movable-type.html](http://www.movabletype.org/documentation/installation/upgrade-movable-type.html) です。



まず、事前のチェックですが、同じサーバの別のドメイン名で既に新しいバージョンの Movable Type が動いているし、プラグインは全く入れてないし、無問題です。



このサイトでは SQLite を使っているので、関係するディレクトリをすべてまとめてファイルとしてバックアップします。 MySQL や PostgreSQL を使っている場合は、ダンプなどをとっておけばいいでしょう。



ここから先は手作業で CGI やら `mt-static` やらを総取っ替えすることになるのですが、このサイトは静的なページしか公開していないので、昼間っから堂々と実行することにします。



`mt-static` は `mt-static.org` に改名して、新しい `mt-static` をコピーして、サブディレクトリ `support` の中身を移動します。 `mt-static` の下はそれだけでいいのかな？ それ以外に私が触ったところはなさそうだな。



```
mv mt-static.old/support/* mt-static/support/
```



`mt` ディレクトリ ( CGI などが入ってるディレクトリ ) も同様に入れ替えます。



念のため `mt` ディレクトリにある `mt-check.cgi` を実行します。特に問題なし。このスクリプトはもう使わないので、改名してしまいます。



このくらいチェックしておけば、もうだいじょうぶでしょう。 `mt.cgi` を実行します。古いバージョンがある場合は、自動でそれを認識してデータベースのアップグレードをしてくれます。移行完了後、ダッシュボードは正常に表示されているようです。



さて、最後に、全てのファイル再構築!! … 特に問題なさそう。サイトの見た目は全く変わりませんが、テンプレートを変えてないから当然か。。。



以上、完了。





追記



終わってから見つけたのだけど、日本語のガイドがありました。 [http://www.movabletype.jp/documentation/mt5/upgrade/index.html](http://www.movabletype.jp/documentation/mt5/upgrade/index.html)
