# Laraval 5 による開発の手順 #2

Update: 2018-09-24


[Laraval 5 による開発の手順 #1](startlaravel1.html) の続きです。

## インストールする

2018年9月23日時点で最新の Laravel 5.7 のインストール手順は
https://laravel.com/docs/5.7 の "Installation" の通りです。

### PHP の Extension を確認する

上記のページの "Server Requirements" に必要な PHP のバージョンと
Extension について記載されています。

```
<?php phpinfo(); ?>
```

のようなファイルをどこかに置いて。

```
php -S localhost:8000
```

として表示してみるか、

```
php -r "phpinfo();"
```

としてみるかすれば調べられます。

``phpinfo()`` は昔 UTF-8 が一般的でなかった時代には
mbstring の設定を確認するのによく使っていましたが、最近は気にすることも少ないかと思います。
共用タイプのレンタルサーバだったらたいていのものが最初から入っていますし。
でも、一度くらいは見ておいてください。

足りないものがあったら Linux で yum や apt で PHP を導入している場合はパッケージを追加してください。
Mac の Homebrew で導入した場合はひととおり全部入っているんじゃないかな。
Windows の場合は ``php.ini`` の ``extension`` の行のコメントアウトを外してください。

### とりあえず動かす

上記のページに書いている通りなのですが、
以下のコマンドを実行すると最新版の Laravel がインストールされて、
Laravel のプロジェクト ( この例ではプロジェクト名 ``blog`` ) が作成されて、テスト用の HTTP サーバが起動します。

```
composer global require "laravel/installer"
composer create-project --prefer-dist laravel/laravel blog
php artisan serve
```

プロジェクトを作成するコマンドとして ``laravel new ...`` と ``composer create-project ...``
が併記されています。どちらでもいいのですが、
Windows の場合は ``laravel`` とコマンドを打っても動かないかもしれません。

## プロジェクトの設定を少し変える

プロジェクトの設定は ``.env`` と ``config`` の下の各ファイルです。
``.env`` は ``.gitignore`` に入っています。
開発用 ( local, staging ) と本番用 ( production ) をそれぞれ作成して使い分けてください。

### SQLite のデータファイルの場所を決める

SQLite のデータファイルの場所ですが、 ``public`` は絶対にダメです。
特別セキュリティに気を使うシステムでなければ、キャッシュやログなどが入っている
``storage`` でいいと思います。書き込み可のものはそこに全部集めるということで。
特別セキュリティに気を使うシステムの場合は、私からはなんとも言えないのでがんばって考えてください。

Linux や Mac の場合は

```
touch storage/blog.sqlite
```

のようにして空のファイルを置いてください。

Windows の場合は [DB Browser for SQLite](http://sqlitebrowser.org/) で新規作成するか、
sqlite3 のコマンドシェルで ``.open blog.sqlite`` とするか、
PowerShell で ``New-Item -ItemType File ...`` としてください。

データファイルの場所は ``config/database.php`` に次のように書いておけばよいです。

```
        'sqlite' => [
            'driver' => 'sqlite',
            'database' => env('DB_DATABASE', storage_path('blog.sqlite')),
            'prefix' => '',
        ],
```

この場合 ``.gitignore`` に ``/storage/blog.sqlite`` を追加しておいてください。

それから ``.env`` に sqlite を使う旨を記載してください。

```
DB_CONNECTION=sqlite
```

``.env`` を書き換えれば、他の RDBMS 製品に置き換えることもできます。
### 環境毎のログの形式を設定する

Laravel 5 は out-of-the-box で（最初から全部入ってる形で）単純なファイル、日毎のファイル、
Slack, Syslog などログの出力先の形を選べるようになっています。

local は single ( 単純なファイル ) 、 staging や production は日毎のファイル、というような設定にしておけばよいでしょう。

環境毎の出力先の選択は ``.env`` に以下のような形で、

```
LOG_CHANNEL=single
```

それぞれの出力先の詳細は ``config/logging.php`` と ``.env`` を組み合わせて設定してください。

## メアドとパスワードでログインできるようにする

Laravel 5.7 のドキュメントの [Authentication](https://laravel.com/docs/5.7/authentication)
に

```
php artisan make:auth
php artisan migrate
```

とすればとりあえず動くぞと書いてあります。その通りにすると、ログイン、サインアップ、登録、パスワードを忘れた場合のパスワードリセットの各機能とログイン後のページができて、データベーステーブルもできます。サインアップすれば誰でも使えるサービスを作るのであればこれでいいです。

プロジェクト作成時に生成された ``.env`` を見るとメールサーバは ``smtp.mailtrap.io`` になっています。
[Mailtrap.io](https://mailtrap.io) はテスト用のメールサーバのサービスですね。
アカウントを作って発行されたユーザ名とパスワードを ``.env`` に設定してやると、パスワードリセットのメールは
Mailtrap.io の Demo inbox に溜まるようになります。とても便利です。
自前のテスト用のメールサーバを建てようとすると、それ自体面倒ですし、
インターネットにつながっている場合はセキュリティの確保が必要ですし、
こういうものがあると助かります。

それから Laravel 5.7 のドキュメントの
[Encryption](https://laravel.com/docs/5.6/encryption)
に記載されている次のコマンドを実行すると ``.env`` の ``APP_KEY`` に値が設定されます。

```
php artisan key:generate
```
## ディクトリ構成

プロジェクトの初期構築の時点でできているディレクトリはこんな感じです。

```
app/
  Console/
  Exceptions/
  Http/
    Controllers/ <-- Controller
    Middleware/
  Providers/
  User.php  <-- Model は app の直下
bootstrap/
config/
database/
  factories/
  migrations/ <-- データベーステーブルの定義
    2014_10_12_000000_create_users_table.php
    2014_10_12_100000_create_password_resets_table.php
  seeds/      <-- データベースの初期データ
    DatabaseSeeder.php
public/
resources/
  js/
  lang/
    en/   <-- 英語のメッセージ
  sass/
  views/  <-- Blade のテンプレート
routes/
  web.php <-- Route の設定
storage/
  app/
  framework/
  logs/   <-- simple や daily のログ
tests/
vendor/
```

これに、処理ロジックやビューヘルパーなどを置く ``app/Services`` と、日本語メッセージを置く
``resources/lang/ja`` くらいを追加すればよいです。

ここまで作ったものは、以下の手順で入手して試していただくことができます。

```
git clone https://github.com/MichinobuMaeda/tamuro.git
cd tamuro
git checkout tags/startlaravel2
composer install
cp .env.local .env
vi .env
touch storage/tamuro.sqlite
php artisan migrate
php artisan serve
```

GUI版の Git ツールを使っている場合は
https://github.com/MichinobuMaeda/tamuro.git
のタグ ``startlaravel2`` をチェックアウトしてください。

``vi .env`` は vi でなくていいけど、パスワードリセットを試す場合はメールサーバの設定が必要です。

Windows で ``touch`` コマンドが使えない場合の代替手段は前述の通り。

----

[Laraval 5 による開発の手順 #3](startlaravel3.html) に続く。

Tag: PHP composer Laravel Mailtrap
