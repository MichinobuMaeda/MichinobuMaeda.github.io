# gollum をローカルで動かしてみた

Update: 2012/04/23

GitHub の Wiki をオフラインでも編集したくて、 gollum を MacBook にインストールしてみました。書き始めた Wiki は https://github.com/MichinobuMaeda/jpzipcode/wiki です。編集モードのデフォルトだった Markdown を使っています。まず http://github.com/github/gollum の案内の通り


```
sudo gem install gollum
sudo gem install github-markdown
```


として、ローカルのリポジトリに `cd` して `gollum` を起動してみましたが、 localhost:4567 を表示するとエラーが出ます。


```
NoMethodError - undefined method `new' for Redcarpet:Module:
 /Library/Ruby/Gems/1.8/gems/gollum-1.3.1/lib/gollum/markup.rb:463:in `render'
 ... ...
```


世の中に同じことで困っている人はいないかと、このエラーメッセージで検索すると [http://stackoverflow.com/questions/8395347/gollum-wiki-undefined-method-new-for-redcarpetmodule](http://stackoverflow.com/questions/8395347/gollum-wiki-undefined-method-new-for-redcarpetmodule) にいました。


```
sudo gem uninstall redcarpet
sudo gem install redcarpet --version=1.17.2
```



としろと。なるほど。詳しいことはよくわからないけど Redcarpet さんのバージョンによる違いの影響ですね。再度 `gollum` を動かすと表示できましたが、あれ ^^)? 微妙に違う。箇条書きとその前の行の間の改行の有無の解釈が本番環境と違っていました。いや、まあ、改行無しで本番環境で正常に表示できていた方がむしろ「えー、いいのかな？」だったので、改行入れることにします。修正前が



```
略語
* GAE: Google App Engine
```


修正後が



```
略語

* GAE: Google App Engine
```

です。日本語のファイル名でもだいじょうぶだし ( UTF-8 じゃない Windows はだめかも ) 、編集を保存するとローカルのリポジトリにコミットできているし、なかなか快適な環境です。
