# このサイトを GitHub Pages に引っ越し

Update: 2021-05-18

レンタルサーバ上の DokuWiki と Blogger 2個と Google Sites にバラバラにページを置いていたのが面倒になったので集約しました。

Markdown が使えるといいんだけど、あと、静的なページでいいんだけどと
[Usage statistics of content management systems](https://w3techs.com/technologies/overview/content_management)
を見ていたら GitHub Pages が上の方にいます。上の方といっても WordPress が圧倒的なので 10位より下は 1.0% 未満です。
WordPress がいいものだとは思わないんだけどな。まあ、他人のことはいいです。

GitHub Pages なら GitHub のオンラインの編集機能も利用できます。

## サブディレクトリ無しにするためのお約束

GitHub にリポジトリを作れば Markdown でも HTML でもとにかく Pages で公開できることは知っていました。 `https://username.github.io/repositoryname` の形になります。でも、そのリポジトリ名のサブディレクトリは無しにしたいんだけどと調べてみたらリポジトリ名を `username.github.io` にしろとのこと。そうするとサブディレクトリ無しの `https://username.github.io/` で公開してくれます。

## 独自ドメインの利用

独自ドメインでも無料でSSL設定できますね。

手順は
[GitHub Pages サイトのカスタムドメインを設定する](https://docs.github.com/ja/pages/configuring-a-custom-domain-for-your-github-pages-site)
に詳しく載っています。

設定にはDNSのレコードの管理についての基本的な知識が必要です。例えば `CNAME` の値の末尾に `.` が必要だとか。その前に「CNAMEって何？」とか。設定が終わるとリポジトリのトップに `CNAME` というファイルが自動でコミットされます。ファイルの中身はドメイン名だけです。

## テーマの選択

自分で Markdown を HTML に変換してアップロードすればどんな形にでもできるのですが、あらかじめ用意してあるテーマがよさそうなので、少しだけカスタマイズして利用することにします。
GitHub Pages に用意されているテーマは [Jekyll](https://jekyllrb.com/) を使っています。 GitHub の設定ページでテーマを選択すると `_config.yaml` に自動で記載されます。ローカルで記入して `push` してもいいです。今回は [Minimal](https://github.com/pages-themes/minimal) を選択しました。

## テーマのカスタマイズ

テーマをカスタマイズしてローカルでプレビューなどするには Ruby が必要です。そんなわけでずいぶん久しぶりに Ruby の環境を用意します。

Ruby は複数のバージョンを入れられるようにします。昔は RVM を使った記憶があります。使ったという記憶だけで、使い方は忘れてしまいました。今回は [rbenv](computer-union.jp) を使ってみます。 Mac の場合、インストールは簡単です。

```
$ brew install rbenv
```

次に

```
$ rbenv init
```

とすると `.profile` か `.bash_profile` に以下のものを入れておけとメッセージが出るので素直にそれに従います。

```
eval "$(rbenv init -)"
```

それから OpenSSL についての警告が出るので以下の行も入れておきました。これは無くてもとりあえず動くと思います。

```
export RUBY_CONFIGURE_OPTS="--with-openssl-dir=$(brew --prefix openssl@1.1)"
```

利用可能なステーブル・バージョンを調べてどれかをインストールします。

```
$ rbenv install -l
2.6.7
2.7.3
3.0.1
jruby-9.2.17.0
 ... ... ...

$ rbenv install 2.7.3
```

`.ruby-version` ファイルを作成して Ruby のバージョンを書きます。

余談ですが JRuby まだあるんだ。 JRuby は Java VM の上で動く Ruby です。メンテナンス大変だろうな。

`Gemfile` は以下のように。

```
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
```

必要なパッケージをインストールしてプレビューするには以下のように。

```
$ bundle install
$ bundle exec jekyll serve
```

http://127.0.0.1:4000 でプレビューを参照できます。 出力先の `_site` ディレクトリは `.gitignore` に追加しておきます。

カスタマイズで利用したファイルは以下のようになります。

```
+---_layouts
|       default.html
+---_sass
|       custom.scss
+---assets
    +---css
            style.scss
    _config.yaml
```

詳細は [Minimal](https://github.com/pages-themes/minimal) か [私のサイトの設定](https://github.com/MichinobuMaeda/MichinobuMaeda.github.io) を見てください。

Tag: github ruby jekyll
