共用型レンタルサーバで Laravel
=====

Update: 2018-07-17


[Laravel](https://laravel.com) を共用型のレンタルサーバで動かす例はあるのですが、
ssh を使ってインストールするものしか見つからなかったので、
ファイルをアップロードするだけで動くか試してみました。

ロリポップやさくらのライトプランのような ssh 無しの安いもののリソースで十分な場合は多いですから。

とりあえず、 Laravel のプロジェクトを作って ``welcome.blade.php`` に
[Foundation](https://foundation.zurb.com) のテンプレートを貼り付けて、
まず、自分の PC 上で ``php artisan serve`` して表示を確認。ソースはこちら。

https://github.com/MichinobuMaeda/larasample

DB が繋がらないとかはないだろうから、これれだけ作ったところでテスト用のサーバにアップロードしてみます。

外から見えないディレクトリにアップロードするのは、先頭に ``"."`` が付くものは ``.env`` だけ、
先頭に ``"."`` が付かないものは ``public`` 以外全てです。
200MB ほどあります。

ディレクトリ ``storage`` と ``bootstrap/cache`` は書き込みのパーミッションが必要です。

それから ``public/index.php`` の次の２箇所を実際のサーバのパスに合わせて書き換えます。

```
require __DIR__.'/../vendor/autoload.php';
$app = require_once __DIR__.'/../bootstrap/app.php';
```

今回は自分で立てた Nginx のサーバなので Rewrite の設定が別途必要でしたが、
たいていの共用型レンタルサーバで使われている Apache なら、
``public/.htaccess`` の設定そのままでだいじょうぶでしょう。
ただし、これをサイトのトップのディレクトリに置いてしまうと他のコンテンツに影響します。
Laravel で作ったアプリだけを置くサイトでなければ、サブディレクトリに置いた方がいいです。
``.htaccess`` の設定を変えてどうにかするのは少々面倒ですから。

最後に ``public`` を公開する場所にアップロードします。

https://michinobu.jp/larasamplepub/

さくらのライトプランあたりで実際に試してみたいのですが、それはまたの機会に。

追記：[共用型レンタルサーバで Laravelその２](laravelonsharedserver2.html)

Tag: PHP Laravel
