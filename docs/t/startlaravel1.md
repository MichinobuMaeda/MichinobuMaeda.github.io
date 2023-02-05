# Laraval 5 による開発の手順 #1

Update: 2018-09-22


追記 : Windows での各種開発ツールの導入については、後から書いた [Chocolatey を使ってみる](chocolatey.html) もご参照ください。

["What are the best full-stack PHP frameworks?"](https://www.slant.co/topics/2804/~best-full-stack-php-frameworks)
によると、 Larval 5 / Yii / Symfony / Phalcon / CodeIgniter の順で人気だそうです ( 2018年9月23日時点 ) 。 2番目の Yii については「初心者には難しいかも」と書いてる人がいます。 full-stack framework を利用する一般的なアプリの開発の場合はできる人ばかりでやるということはあまりないだろうと思うので、 1番目の Laravel 5 が無難でしょう。私が使ってみた感じ、 PHP の文法に郷愁を感じてしまうことを除いて Ruby on Rails より好きです。昔ながらの CGI や PHP モジュールを動かすタイプの共用型レンタルサーバに Node.js のフレームワークや Ruby on Rails を載せるのは不可能ですが、 Laravel ならできます ( [共用型レンタルサーバで Laravel](laravelonsharedserver.html) ) 。

full-stack はいらない、 API だけ作りたいという場合は Laravel をベースにした
[Lumen](https://lumen.laravel.com) というマイクロフレームワークもあります。
これは同種の PHP のフレームワーク Slim より少し速いそうです。

## PHP の開発環境を準備する

ひと昔前であれば PHP で開発するというと Apache / MySQL / PHP のセットを用意したものです。でも、特別な用途のシステムの開発でなければ Apache は不要です。例えば、Laravel のようにテスト環境まで用意したフレームワークを使わない場合でも

```
php -S localhost:8000
```

とすればテスト用の HTTP サーバを起動できます。ポート番号の 8000 のところは好きな値で。
``.htaccess`` でいろいろ設定する必要がある場合はダメですが、しかし、あんまり難しいことするのはやめましょうよ。

それから MySQL は本当に必要でしょうか？

SQLite の開発元のサイトは動的ページのデータの管理のために他の RDBMS 製品は使わず SQLite を使っています。
当然と言えば当然ですが。
それで毎日数10万のページビューを問題なく処理しているとのことです
( [Appropriate Uses For SQLite](https://www.sqlite.org/whentouse.html) ) 。
これは世間に名の知れたサイトならともかく、世の中に星の数ほどある Web サイトの大半には無縁なアクセス数だと思います。
また read 主体であれば数GBのデータ量で問題なく稼働している例もあるそうです。
write の並行が激しい場合は無理ですが、しかし、個人商店や1000人以下の企業がいまどきのコンピュータの性能で write の処理が追いつかなくなるほどの量の商品やサービスの注文をリアルの世界でさばけるわけがないですよね。
10年前か20年前までは電話とFAXで、その後も E-mail で受付してたりするわけでしょ？
ちなみに、 MySQL や Oracle を使っていていてもたかだか数万／日、ひどいのだと数千／日のアクセスで落ちるサイトがありましたが、それは作り方が悪いからなので悔い改めること。

そうはいっても「上の人」が MySQL や Oracle じゃないとダメとか言うことはあるでしょうけど、
full-stack framework について来る ORM を利用する場合はもちろん、
素の PHP でも PDO を使えば開発は SQLite 、本番は MySQL ということはできるはずです。
はい？「RDBMS 製品によって使える構文が違う」って？

だ〜か〜ら〜 むずかしいことをするのはやめましょう。

というわけで、ほとんどの場合は PHP と SQLite があれば十分だと思います。

Linux の場合 PHP と sqlite3 は yum や apt などのパッケージマネージャを使って入れてください。
Larval 5.7 の場合 PHP は 7.1.3 より新しいバージョンが必要です。
ディストリビューションによっては PHP の新しいバージョンが入らないかもしれません。
Debian 8 / Debian 9 の場合は [Debian 9 に PHP 7.1, 7.2 をインストールする](debian9php7_1.html) を参考にしてください。

Mac は Homebrew などを使って入れてください。
GUI の [DB Browser for SQLite](http://sqlitebrowser.org) も使いやすいです。
これは Windows 版もありますね。

Windows の場合は https://windows.php.net/download/ からコンパイル済みのセットをダウンロードして、
適当なフォルダに解凍して、そこに PATH を通してください。
``x64`` (64bit) か ``x86`` (32bit) かは自分のPCの OS に合せて。
それから ``Non Thread Safe`` と ``Thread Safe`` があるのですが、
Apache などを使わず PHP の HTTP サーバを建てる前提なので ``Thread Safe`` が無難です。
それから ``php.ini-development`` を ``php.ini`` にリネームするかコピーしてください。
そして ``php.ini`` のこのあたりのコメント（セミコロン）を外しておく必要があります。

```
;extension=mbstring
;extension=openssl
;extension=pdo_sqlite
```

でも、これ、コメントアウトを外すだけでいいんだっけ？
``extension=php_mbstring.dll`` みたいに書き換えたことがあったような。。。あ〜 忘れた orz

それから、 Windows で本家のコマンドライン版の sqlite3 が欲しい場合は
https://www.sqlite.org/download.html から
"Precompiled Binaries for Windows" の sqlite-tools を取得してください。
## IDE またはテキストエディタ

使い慣れたテキストエディタがあって、それが PHP の syntax hilighting に対応してくれているのであればそれでいいです。
私は昔は Eclipse PDT を使っていましたが、最近はまったく Java に関わっていなくて
Visual Studio Code に乗り換えました。自動インデントの仕様が若干気に入りませんが、それ以外は良いです。
NetBeans の PHP 対応も良いようです。

ブレークポイントを使ったデバッグは。。。設定めんどくさそうだし私は debug レベルのログ出力で済ませています。
behavior driven とか test first な ruby の開発をやってたような人達が
vi でブレークポイントを使ってたわけはないので、まあ、いいでしょう。

昔 UNIX で開発をしたときは gdb のコマンドを打ちながら「ああ VC++ はこれをあの画面上に表示しているのね」と感心したものですけど。

## composer の導入

PHP の composer は Ruby の bundler とか Node.js の npm のようなパッケージマネージャです。
Laravel 5 を使う場合は必要ですし、最近の PHP の開発ではよく使われるようになっているそうです。
Ruby や Node.js でこのようなパッケージマネージャ無しの開発をやるのはもはや想像できなくて、
PHP もようやくモダンになったということだと思います。

### Linux と Mac の場合

Linux と Mac は [Download Composer](https://getcomposer.org/download/)
の手順でインストールできます。
Windows もこれでだいじょうぶそうな気がするけど。。。
そのページに書かれている手順は「再配布するな（意訳：コピペして自分のサイトに貼るな）」ということになっていますので、
[Download Composer](https://getcomposer.org/download/)
に掲載されている最新の手順に従ってください。
ダウンロードしたファイルをチェックするためのハッシュ値がそこにベタ書きされているのですが、バージョンアップすると変わってしまうんだな。。。

どのディレクトリ（フォルダ）からでもコマンド ``composer`` が使えるようにするには、
[Getting Started](https://getcomposer.org/doc/00-intro.md)
の "Globally" に記載されているように、
インストールしたファイル ( デフォルトのファイル名は ``composer.phar`` ) を
``/usr/local/bin/composer`` などの PATH が通っているところに移動してください。
### Windows の場合

[Getting Started](https://getcomposer.org/doc/00-intro.md)
の "Installation - Windows" に記載されているように、
``Composer-Setup.exe`` をダウンロードして使ってください。
そして、その下に書かれている手順で ``composer.bat`` を作成してください。

----

[Laraval 5 による開発の手順 #2](startlaravel2.html) に続く。

Tag: PHP composer Laravel SQLite
