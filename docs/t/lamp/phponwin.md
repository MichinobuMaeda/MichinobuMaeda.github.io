# 整理中：Windows で PHP の開発

Update: 2008-06-30



> この記事を書いた後に [Zend Server](http://www.zend.com/en/products/server-ce/) や [XAMPP](http://www.apachefriends.org/jp/xampp.html) などを知りました。この記事のように個別に入れるよりこれらのパッケージを利用する方が楽です。 ( 参照 : [Zend Server CE / Zend Framework](zendservercezendframework.html) / [PHPのデバッグができる環境](phpdebugger.html) )



システムの仕事をしている人の場合自宅に Windows PCが 1台あることが多いです。でも、そこに LAMP ( Linux, Apache, MySQL, PHP : 仕事で使える特に優れたオープンソース製品 ) 一式入れて本格的な環境を作るとなるとたいへんです。 OS は Windows のまま、 Web 開発のための最小限の環境を短時間で作る手順を紹介します。



それから、このページに表示されているバックスラッシュ「\\」は、半角「￥」と置き換えて読んでください。

## 1. はじめに

### 1.1. 対象となる読者

Windows を普通に使えるエンジニアで、PHP 未経験の人を対象にします。



「Virtual Machine 使えば？」という人はスキルが高すぎるので対象外です。



「PHP を Windows 上で動かしてだいじょうぶなの？」と思う人もいるかもしれませんが、 Xoops など動かしてみた限りでは問題ありませんでした。 Micorsoft社が Zend社と提携したというニュースも流れていましたので将来は IIS 上で PHP なんてことが普通になるかもしれません。



HTML や CSS の基本はここでは扱いません。



セッションの管理やオブジェクト指向など PHP のより高度な機能についてもここでは扱いません。



PHP から MySQL に接続する API には 2種類ありますが、古い方 ( 性能が落ちるかもしれないけど簡単な方 ) を使います。

### 1.2. 必要なもの

Windows PC 1台、低いスペックでも OK です。この記事の内容の検証には Windows Vista を使っています。 Windows XP もだいじょうぶ、 Windows 2000 でも問題ないと思います。



資材を入手するためにインターネットに接続する環境が必要です。



tar.gz 形式の圧縮ファイルを解凍できるツールが必要です。 PHP のドキュメントなど tar.gz 形式で配布されているものがあります。



> 例) [Lhaca デラックス版](http://www.vector.co.jp/soft/win95/util/se166893.html)



PHP のソースの編集のためにテキストエディタがあるといいのですが、「メモ帳」でもだいじょうぶです。

### 1.3. 各製品の簡単な説明

#### Apache

Apache は広く使われている Webサーバ ( HTTPサーバ ) です。フリーソフトですが品質性能とも非常に高く、仕事でも安心して利用できます。 Microsoft社の IIS 以外の商用製品が売れない原因になっているような。。。

#### PHP

PHP は Apache や IIS などの Webサーバで動的なページを作成するための言語です。 C, Java, C# 等に似た文法で習得しやすく、「とりあえず手間かけずに動かしたい」場合も 「しっかりモジュール化してきちんとしたシステムを作りたい」場合にも使えます。 大規模システムの採用の例としては楽天市場があります。

#### MySQL

MySQL はフリーと商用の両方のライセンスで配布されている RDBMS ( Relational Database Management System ) です。性能や品質はきわめて高く、特に性能面では Oracle 以外の商用の製品にも負けません。機能は少なめですが、普通のシステムを作るには十分です。 商用ライセンス買っても安いので、仕事で使う場合はサポート付けることをお勧めします。

### 1.4. 文字コードについて

ほとんどデフォルトの設定のままインストールしますが、文字コードだけは最初に設定しておいた方がいいです。ここでは文字コードに UTF-8 を使う設定で説明します。



Windows では Shift\_JIS と UNICODE ( UTF-16 ) がよく使われます。 UNIX / Linux ではこれまで EUC-JP が使われていましたが、最近 UTF-8 も使われるようになりました。 Apache と MySQL はどれでもだいじょうぶです。 PHP は Shift\_JIS と UNICODE ( UTF-16 ) が苦手です。今回は開発の最中に文字コードについては考えなくて済むように UTF-8 を使います。 Windows XP の「メモ帳」も UTF-8 に対応しています。 PC用の Webブラウザで UTF-8 に対応していないものは見たことがありません。携帯電話も古い機種 ( i-mode がこの世に登場したばかりの頃とか ) でなければ UTF-8 に対応しています。

## 2. Apache のインストール

### 2.1. インストーラの入手

2008年 5月 2日現在の最新版とその入手先です。



The Apache Software Foundation [http://www.apache.org/](http://www.apache.org/)



 `- Apache Projects`

 `- HTTP Server`

 `- Download!`

 `- from a mirror`

 `- Win32 Binary including OpenSSL 0.9.8g (MSI Installer):`

 `apache_2.2.8-win32-x86-openssl-0.9.8g.msi`



### 2.2. インストール

Apache のインストーラ `apache_2.2.8-win32-x86-openssl-0.9.8g.msi` を実行します。 PC によって次の「 Server Information 」の画面の各項目にデフォルト値が入っている場合と空欄の場合があります。空欄の場合は適当な値、例えば `localdomain`, `localhost.localdomain`, `admin@localhost.localdomain` といった感じの値を入れてください。それ以外はすべてデフォルトの設定のままでインストールします。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5OmlywqI/AAAAAAAABp8/AbWQDaLayKY/s1600/amponwin02_1_original.gif)



インストールが終わったら Webブラウザで `http://localhost/` を表示してください。「 It works! 」と表示されたら OK です。



こんな感じのフォルダ構成になっています。



`C:\PROGRAM FILES`

 `\APACHE SOFTWARE FOUNDATION`

 `\APACHE2.2`

 `\bin`

 `\cgi-bin`

 `\conf`

 `httpd.conf -- 設定ファイル`

 `\error`

 `\htdocs`

 `index.html -- 「 It works! 」`

 `\icons`

 `\logs`

 `\manual`

 `\modules`



設定ファイル `httpd.conf` はこの後何度か使うので、この場所を覚えておいてください。

### 2.3. DocumentRoot の移動

表示するコンテンツを置く `htdocs` の場所がここでは使いにくいので、新しいフォルダ C:\\MySite\\html を作ってそちらに移動します。まず、 `httpd.conf` の次の行を変更してください。 行の先頭「 `＃` 」はコメント行で変更前の内容です。



`#DocumentRoot "C:/Program Files/Apache Software Foundation/Apache2.2/htdocs"`

`DocumentRoot "C:/MySite/html"`



もう１カ所変更します。



`#<Directory "C:/Program Files/Apache Software Foundation/Apache2.2/htdocs">`

`<Directory "C:/MySite/html">`



ファイル `C:\MySite\html\index.html` を作成して、テキストエディタかメモ帳で次の内容の HTML ソースを書きます。



`<html>`

 `<head>`

 `<title>My Page</title>`

 `</head>`

 `<body>`

 `<h1>My Page</h1>`

 `</body>`

`</html>`



Apache を再起動します。 Windows XP の場合は画面右下の ![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5PcXCmnI/AAAAAAAABqA/C0VbWJdAgLw/amponwin02_2.gif) をマウス左ボタンでクリックして「 Stop 」を選択、次に「 Start 」を選択してください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5PzR5b5I/AAAAAAAABqE/_WqhqEAnKVg/amponwin02_3_original.gif)



Windows Vista はこれではうまくいかないようです。 画面右下の ![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5PcXCmnI/AAAAAAAABqA/C0VbWJdAgLw/amponwin02_2.gif)  をマウス右ボタンでクリックして「 Open Services 」を選択して表示される Windows の「サービス」画面を使ってください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5QkBSMII/AAAAAAAABqI/JXJJpbjoVv0/amponwin02_4_original.gif)



もう一度Webブラウザで `http://localhost/` を表示し直してください。「 My Page 」と表示されたら OK です。

## 3. PHP のインストール

### 3.1. ドキュメントと Windows 版の入手

PHP の Windows 用のインストーラというものもあるのですが、あまり出来が良くなくて、 Apache や MySQL のように「全部デフォルトでインストールすればとりあえず動く」ようなものではありません。マニュアル ( 手動 ) インストールでもたいして手間はかからないのでそちらを使います。



2008年 5月 2日現在の最新版のドキュメントと Windows 版は次のところからダウンロードしてください。



PHP: Hypertext Preprocessor [http://www.php.net/](http://www.php.net/)



 `- Documentation`

 `- Downloads`

 `- documentation downloads Page`

 `- Japanese`



 `- downloas`

 `- Windows Binaries`

 `- PHP 5.2.6 zip package`



### 3.2. ドキュメントと実行環境のコピー

先にドキュメントを用意します。 フォルダ `C:\MySite\html\documents\php` を新規に作成してください。 `php_manual_ja.tar.gz` を解凍して、 サブフォルダ `html` の中のファイルを作成したフォルダにすべてコピーしてください。



「 2. 」でインストールした Apache により `http://localhost/documents/php/` で表示できます。　Internet Explorer の場合一部のページが正常に表示できないことがあります。 UTF-8 の文字コードの自動認識がうまくいかないようです。「エンコード」の設定が「日本語(自動選択)」とか「日本語(シフトJIS)」になっている場合は「自動選択」に変更してみてください。



インストールに関係のあるページは次の通りです。



 `- インストールと設定`

 `- Windows システムへのインストール`

 `- マニュアルインストール`

 `- Apache 2.0.x （Microsoft Windows 用）`



PHP の動作モードには次の 3種類があるのですが、詳しい説明は省きます。

*   CGI 実行ファイル
*   CLI 実行ファイル
*   サーバモジュール

ここでは「サバーバモジュール」を使います。



マニュアルと同じフォルダ `C:\PHP` を作成して `php-5.2.6-Win32.zip` の中身を解凍してください。次のようなフォルダ構成になります。



`C:\PHP`

 `\dev`

 `\ext`

 `\extras`

 `\PEAR`



`C:\PHP` の直下のファイル `php.ini-recommended` をコピーして同じフォルダにファイル `php.ini` を作ります。

### 3.3. PHP の設定の変更

`php.ini` の中にたくさんの設定が入っていますが、そのほとんどは行の先頭「 `;` 」でコメントアウトされています。次の項目について、コメントアウトされていれば「 `;` 」を消して有効にして「 `=` 」の右側の値を変更してください。



`extension_dir = "./ext"`



`extension=php_mbstring.dll`

`extension=php_mcrypt.dll`

`extension=php_mysql.dll`



`[mbstring]`

`mbstring.language = Japanese`

`mbstring.internal_encoding = UTF-8`

`mbstring.encoding_translation = Off`

`mbstring.substitute_character = none;`

`mbstring.func_overload = 0`



### 3.4. Apache の設定の変更

Apache の `httpd.conf` の末尾に次の設定を追加してください。



`LoadModule php5_module "c:/php/php5apache2_2.dll"`

`AddType application/x-httpd-php .php`

`PHPIniDir "C:/php"`



Apache の `httpd.conf` の `<IfModule dir_module>` という箇所を探して設定を変更してください。 URL の指定でファイル名を省略した場合に表示する候補となるファイルの名称を追加します。



`<IfModule dir_module>`

 `DirectoryIndex index.php index.html`

`</IfModule>`



Apache の `httpd.conf` の次の行が「 `#` 」でコメントアウトされているので「 `#` 」を削除して有効にしてください。



`Include conf/extra/httpd-manual.conf`



### 3.5. 動作の確認

表示の確認のためのページを `C:\MySite\html` の下に作成します。まず `index.php` を作成します。



`<html>`

 `<head>`

 `<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />`

 `<title>Hello PHP!!</title>`

 `</head>`

 `<body>`

 `<h1>Hello PHP!!</h1>`

 `<h2>マニュアル</h2>`

 `<ul>`

 `<li><a href="manual/">Apache 2.2</a></li>`

 `<li><a href="documents/php">PHP 5.2</a></li>`

 `<li><a href="documents/mysql">MySQL 5.1</a></li>`

 `</ul>`

 `<h2>その他</h2>`

 `<ul>`

 `<li><a href="phpinfo.php">phpinfo</a></li>`

 `<li><a href="phpMyAdmin">phpMyAdmin</a></li>`

 `</ul>`

 `</body>`

`</html>`



次に `phpinfo.php` も同じフォルダ `C:\MySite\html` に作成します。このファイルで PHP の動作環境の設定内容の一覧を表示することができます。



`<?php phpinfo(); ?>`



Apache を再起動して `http://localhost/` を表示し直してください。「 Hello PHP!! 」と表示されたら OK です。

### 3.6. 設定ファイル

修正済みの設定ファイルです。修正箇所は「 `2008/05/05` 」で検索してください。



*   [httpd.conf](https://sites.google.com/site/michinobumaeda/lamp/phponwin/httpd_conf.zip?attredirects=0)
*   [php.ini](https://sites.google.com/site/michinobumaeda/lamp/phponwin/php_ini.zip?attredirects=0)

## 4. MySQL のインストール

### 4.1. インストーラとドキュメントの入手

2008年 5月 2日現在の最新版とその入手先です。



MySQL [http://www.mysql.com/](http://www.mysql.com/)



 `- Developer Zone`

 `- Downloads`

 `- MySQL Community Server / Download`

 `- Windows downloads`

 `- Windows ZIP/Setup.EXE (x86)`

 `- Pick a mirror`



“New Users” でアカウント登録するか、 “No thanks, just take me to the downloads!” を選択するかしてください。



ドキュメントは、仕様の詳細から導入・保守まで網羅した完成度の高いものです。



 `- Developer Zone`

 `- Documentation`

 `- Japanese v5.1`



### 4.2. インストール

`mysql-5.0.51b-win32.zip` を解凍してインストーラを実行してください。 MySQL のシステムのインストールが終わると自動でデータベース・インスタンスのインストーラも起動します。前半のシステムの方はすべてデフォルトの設定です。データベース・インスタンスのインストールで「 Please select the default character set. 」画面が出てきたら「 Best Support For Multilingualizm 」 ( 要するに　UTF-8 ) を選択してください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5SqoaMSI/AAAAAAAABqM/47-WeM_CfMA/s1600/amponwin04_1_original.gif)



「 Please set the security options. 」画面が出てきたら、管理者 `root` ユーザのパスワードを入力してください。このパスワードは忘れないでください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5UHfgjBI/AAAAAAAABqQ/kRo_-RDuvO0/s1600/amponwin04_2_original.gif)



開発環境とはいえできるだけセキュリテリは守りたいですから、特に必要なければ「 Enable root access from remote machines 」は有効にしないでください。今回構築しようとしている環境も、 Apache と MySQL が同じ PC に同居しているのでリモートアクセスは不要です。

### 4.3. ドキュメントのコピー

フォルダ `C:\MySite\html\documents\mysql` を新規に作成してください。 `refman-5.1-ja.html-chapter.zip` を解凍して、中のファイルを作成したフォルダにすべてコピーしてください。「 3.5. 動作の確認 」で作成したページ `http://localhost/` のリンク「 MySQL 5.1 」から参照できるようになります。

### 4.3. phpMyAdmin の入手

phpMyAdmin は Web 版の MySQL の管理ツールです。



phpMyAdmin : [http://www.phpmyadmin.net/](http://www.phpmyadmin.net/)



 `- DOWNLOADS`

 `- all-languages.zip`



### 4.4. phpMyAdmin のインストール

フォルダ `C:\MySite\html\phpMyAdmin` を新規に作成してください。 `phpMyAdmin-2.11.6-all-languages.zip` を解凍して、中のファイルを作成したフォルダにすべてコピーしてください。「 3.5. 動作の確認 」で作成したページ `http://localhost/` のリンク「 phpMyAdmin 」から参照できるようになります。



初めて表示したときはメッセージ 「 設定ファイルが作成されていないものと思われます。セットアップスクリプト を利用して設定ファイルを作成してください 」 が表示されます。このツールの作者はこの「 セットアップスクリプト 」を使うと簡単に設定できると主張していますが、今回使いたい範囲の機能の実現のためには全然簡単ではないので、次の手順で設定してください。



ファイル `C:\MySite\html\phpMyAdmin\config.sample.inc.php` をコピーしてファイル `C:\MySite\html\phpMyAdmin\config.inc.php` を作成してください。そのファイルの次の項目に適当な値を設定してください。次の例のように本当にてきとうーな値でいいです



`$cfg['blowfish_secret'] = 'lkasdjfkladgkahskdfla';`



もう一度 `http://localhost/phpMyAdmin/` を表示します。今度はエラーなど無しにログイン画面が表示されます。「 言語 」は「 日本語 - Japanese (utf-8) 」を選択して、ユーザ root でログインしてください。

## 5. テスト用 DB の作成

### 5.1. ユーザとデータベースを作成する

「インスタンス」とか「データベース」とか「ユーザ」とか「スキーマ」という言葉が出てきますが RDBMS 製品によってこのあたりの関係が違っていて困ります。でも、きっとどうにもならないのであきらめましょう。



先ほど作成した MySQL のインスタンスにユーザとデータベース ( ツールによっては「スキーマ」 )を作成するのですが、 MySQL の場合次のルールにしておくと管理が楽です。

*   一人のユーザが一つのデータベースを使用する
*   そのユーザとデータベースの名前は同じ

そのようなわけで、 `phpsite` ユーザと `phpsite` データベースを作成します。



前項でセットアップした phpMyAdmin に `root` ユーザでログインすると、最初の画面の真ん中より下の方「 特権 」というすごい名前のリンクがあるのでクリックします。



次の画面の真ん中あたりに「 新しいユーザを追加する 」リンクがあるのでクリックします。



「ログイン情報」の各欄に値を入力します。



 ユーザ名

 phpsite

 ホスト

 localhost

 パスワード

 この値はお任せします。





パスワードを複雑な値にしたければ、記入欄の下の「パスワードを生成する」機能を使うといいでしょう。



その下の「ユーザ専用データベース」は「同名のデータベースを作成してすべての特権を与える」を選択します。



さらにその下の「グローバル特権」は設定不要です。



画面の一番下の \[ 実行する \] ボタンを押して出来上がりです。



では、ここで一度ログアウトして今度はユーザ `phpsite` でログインしてみましょう。ログアウトのボタンはとてもわかりにくいです。画面左上 phoMyAdmin の下の５個並んだアイコンの左から２番目「 Exit 」とほとんど読めないくらい小さな字で無理矢理書いたアイコンです。 ログインするときは念のため「 言語 」で「 日本語 - Japanese (utf-8) 」を選択していることを確認してください。ユーザ名 phpsite と先ほど設定したパスワードで無事ログインできれば OK です。

### 5.2. テーブルを作成する

phpMyAdmin にユーザ `phpsite` でログインすると、画面左側にデータベース名が２個「 `information_schema` 」と「 `phpsite` 」が並んでいますので「 `phpsite` 」の方を選択します。すると「 データベース phpsite に新しいテーブルを作成する 」という今まさにやりたいことがそのまま書かれていますので、名前に「 `HATSUYUME` 」フィールド数に「 2 」を入力して右の方の \[ 実行する \] ボタンを押します。全部半角です。 MySQL が日本語のテーブル名カラム名に対応しているかどうかは未確認です。誰か試してみてください。



最初のフィールドは次の設定です。



 フィールド

 NO

 種別

 INT

 長さ/値

 ※設定無し

 照合順序

 ※設定無し

 属性

 ※設定無し

 ヌル(NULL)

 not null

 デフォルト値

 ※設定無し

 その他

 auto\_incriment

 インデックスの設定

 主キー　( 鍵のマークを選択 )

 全文検索の設定

 ※設定無し



２番目のフィールドは次の設定です。



 フィールド

 NAME

 種別

 VARCHAR

 長さ/値

 100

 照合順序

 ※設定無し

 属性

 ※設定無し

 ヌル(NULL)

 not null

 デフォルト値

 ※設定無し

 その他

 ※設定無し

 インデックスの設定

 ※設定無し ( — を選択 )

 全文検索の設定

 ※設定無し



画面下の方に「ストレージエンジン」という選択欄がありますが、これはとりあえずデフォルトの InnoDB でいいです。最後に、その下の \[ 保存する \] ボタンを押してください。

### 5.3. データを入れる

引き続き phpMyAdmin 上の作業です。「 サーバ: `localhost` データベース: `phpsite` テーブル: `HATSUYUME` 」のまま作業を続けます。この画面の上の方のタブ「 挿入 」を選択してください。



入力する値は次の通りです。一度に最大２行しか入力できないので、操作を繰り返してください。



 NO

 NAME

 1

 富士

 2

 鷹

 3

 茄



画面上のタブ「 表示 」で結果を確認してください。

## 6. DB の内容をWebで表示する

### 6.1. PHP の MySQL に関する機能

PHP の MySQL に関する機能はマニュアルのこの目次をたどってください。各関数について、使用例を挙げて詳しく説明しています。



 `- 関数リファレンス`

 `- データベース関連`

 `- ベンダー固有のモジュール`

 `- MySQL`



### 6.2. サンプルページ

ファイル `C:\MySite\html\hatsuyume.php` を新規で作成してください。内容は次の通りです。ファイルを保存するときに文字コードを UTF-8 にしてください。



`<html>`

 `<head>`

 `<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />`

 `<title>初夢</title>`

 `</head>`

 `<body>`

`<?php`

`// MySQL に接続する。`

`$link = mysql_connect("localhost:3306", "phpsite", "phpsite");`

`if (!$link) {`

`?>`

 `<p>Error: MySQL に接続できませんでした。</p>`

`<?php`

`// クライアント側の文字コードの設定`

`} elseif (!mysql_set_charset("utf8")) {`

`?>`

 `<p>Error: MySQL のクライアント側の文字コードの設定ができませんでした。</p>`

`<?php`

`// データベース phpsite を選択`

`} elseif (!mysql_select_db("phpsite")) {`

`?>`

 `<p>Error: MySQL のデータベース phpsite を選択できませんでした。</p>`

`<?php`

`} else {`

 `// 問い合わせの実行`

 `$result = mysql_query("SELECT NO, NAME FROM HATSUYUME");`

 `// 問い合わせの結果のチェック`

 `if (!$result) {`

`?>`

 `<p>Error: MySQL の問い合わせでエラー <?php echo mysql_error(); ?> が発生しました。</p>`

`<?php`

 `} else {`

 `// 結果を表示`

`?>`

 `<table>`

 `<tr>`

 `<th>No.</th>`

 `<th>Name</th>`

 `</tr>`

`<?php`

 `while ($row = mysql_fetch_assoc($result)) {`

`?>`

 `<tr>`

 `<td><?php echo htmlspecialchars($row["NO"], ENT_COMPAT, "utf8"); ?></td>`

 `<td><?php echo htmlspecialchars($row["NAME"], ENT_COMPAT, "utf8"); ?></td>`

 `</tr>`

`<?php`

 `}`

`?>`

 `</table>`

`<?php`

 `}`

 `// MySQL の接続を閉じる。`

 `mysql_close($link);`

`}`

`?>`

 `</body>`

`</html>`



`http://localhost/hatsuyume.php` で表示を確認してください。正常なら次のように表示されます。何かエラーがあればできるだけ画面上に表示するプログラムにしてありますのでメッセージを確認してください。



`No.` `Name`

`1` `富士`

`2` `鷹`

`3` `茄`



## 番外編 osCommerce

なぜ番外編なのかというと、 osCommerce は、古いバージョンの PHP や MySQL を前提にしていて、日本語版の文字コードも EUC-JP だからです。 ソースに手を入れることによる PHP5 対応や UTF-8 対応 も可能なのですが、少々面倒です。それから、自分の作業環境の都合で Windows XP で動作確認しています。

### 1. 作業のためのツール

tar.gz 形式の圧縮ファイルの解凍、文字コード ECU-JP のファイルの編集など Windows ではなじみの薄い作業のために私が使っているフリーのツールです。他のものでもかまいません。

#### 1.1. +Lhaca デラックス版

*   Lhaca123.EXE

対応している形式の多い Windows 用の圧縮解凍ツールです。入手先 URL はこちらです。[http://park8.wakwak.com/~app/Lhaca/lhacadx.html](http://park8.wakwak.com/~app/Lhaca/lhacadx.html)

#### 1.2. TeraPad

*   tpad093.zip

ごく普通のテキストエディタです。入手先 URL はこちらです。 [http://www5f.biglobe.ne.jp/~t-susumu/library/tpad.html](http://www5f.biglobe.ne.jp/~t-susumu/library/tpad.html)



よく、秀丸エディタを未登録のまま使っている人がいますが、使うんなら金払う、金払わないんなら使わない、私は秀丸のライセンス買ってますが、微妙な挙動の好みの問題で他の製品を使っています。

### 2. Apache

*   apache\_2.0.63-win32-x86-openssl-0.9.7m.msi

バージョンは 2.2 ではなく 2.0 ですが、インストールの手順は 2. Apache のインストール と同じです。デフォルトのインストール先は `C:\Program Files\Apache Group\Apache2` です。 `C:\Program Files\Apache Group\Apache2\conf\httpd.conf` の設定内容を追加・変更した箇所は次の通り。 `default.php` は osCommerce で使われていたので追加しました。 Web のコンテンツを置く場所は本編と同じ `C:\MySite\html` としています。 PHP をインストールする場所も本編と同じ `C:\php` としています。



`... 変更 ...`

`DocumentRoot "C:/MySite/html"`

`... 変更 ...`

`<Directory "C:/MySite/html">`

`... 変更 ...`

`DirectoryIndex index.php default.php index.html index.html.var`

`... 追加 ...`

`LoadModule php4_module "c:/php/php4apache2.dll"`

`AddType application/x-httpd-php .php`

`PHPIniDir "C:/php"`



### 3. PHP

*   php-4.4.8-Win32.zip
*   libmcrypt.dll
*   php\_manual\_ja.tar.gz

本編の PHP5 より PHP4 の方が手順が少々増えます。



まず、 phpMyAdmin が使用する mcrypt で必要となる `libmcrypt.dll` が Windows バイナリパッケージに含まれていません。次の URL から入手して、 C:\\php にコピーしてください。



[http://files.edin.dk/php/win32/mcrypt/](http://files.edin.dk/php/win32/mcrypt/)



ドキュメントの Windows でのインストールの手順に書いているように、 `C:\php\dlls` と `C:\php\sapi` の下のファイルをすべて `C:\php` の下に移動してください。



`php.ini` の設定も少し異なります。 まず、 PHP5 と違って `php_mysql.dll` というのはありません。デフォルトで MySQL への接続に対応しています。それから、 `extension_dir` の値は相対パス指定ではうまく動かないようです。次の例のようにフルパス指定してください。



`extension_dir = "c:/php/extensions"`

`...`

`extension=php_mbstring.dll`

`...`

`extension=php_mcrypt.dll`



osCommerce のための追加の設定が必要です。 osCommerce 日本語版 ( 「 6. osCommerce 」参照 ) の INSTALL\_japanese.txt の中の「 2.2 PHPの設定 」の記述に従って設定してください。



環境変数 `PATH` に `C:\php` を追加したら念のため OS を再起動してください。

### 4. MySQL

*   mysql-essential-4.1.22-win32.msi
*   refman-4.1-ja.html-chapter.zip

MySQL も古いバージョンになります。インストールの手順は、文字コードに「 UTF-8」ではなく「 ujis 」 ( EUC-JP のこと ) を選択する以外「 4. MySQL 」のインストール と同じです。PHP に含まれる MySQL のクライアントのバージョンが古いようで、インストール完了後に次の設定が必要です。



`Windows 「スタート」メニュー`

 `→ すべてのプログラム`

 `→ MySQL`

 `→ MySQL Server 4.1`

 `→ MySQL Command Line Client`



を選択し、インストール時に設定した `root` のパスワードを入力して次のコマンドを実行してください。「 '\*\*\*\*' 」には root のパスワードを入れてください。 MySQL にユーザを追加したとき、および、 MySQL のユーザのパスワードを変更したときは毎回この操作が必要です。



`mysql> SET PASSWORD FOR root@localhost = OLD_PASSWORD('****');`



### 5. phpMyAdmin

*   phpMyAdmin-2.11.7-all-languages.zip

「4. MySQL のインストール 」の「 4.3. phpMyAdmin の入手 」「 4.4. phpMyAdmin のインストール 」と同じです。ログイン時の「 言語 」は UTF-8 でも euc でもどちらでもいいです。データベースと同じ euc の方が文字化け等の心配が少ないかもしれません。

### 6. osCommerce

*   oscommerce-2.2ms1j-R8.tar.gz

php.ini に「 3. PHP 」の設定が間違いなくできていることを確認したら、念のため Apache を再起動してください。 osCommerce のインストール時のエラーの表示はあまり親切ではないようなので、事前に設定をよく確認してください。



phpMyAdmin を使って、 MySQL に osCommerce 用のユーザとデータベースを作成します。 5. テスト用 DB の作成 と同じ要領でユーザ osc とデータベース osc を作成します。違う名称でもいいですが、その場合は以下の説明の「 `osc` 」を読み替えてください。



`oscommerce-2.2ms1j-R8.tar.gz` は Lhaca などを使って解凍してください。解凍すると一番上のディレクトリにファイル `INSTALL_japanese.txt` があります。ここに記述された手順に従ってインストールします。



まず、 `oscommerce-2.2ms1j-R8.tar.gz` の中のサブフォルダ `admin` と `catalog` をフォルダごと `C:\MySite\html` の下にコピーします。たくさんのディレクトリとファイルがありますが、この後使う主なものは次のようになります。



`C:`

`+---MySite`

 `+---html`

 `+---admin`

 `|   +----includes`

 `|           configure.php`

 `+---catalog`

 `+----includes`

 `|       configure.php`

 `+----install`



次に、設定ファイルに Windows の全てのユーザとグループに設定ファイルの書き込み権限を与えます。本当は全部のユーザ・グループでなくていいのですが、みなさんの PC の環境によって対象が異なりますし、どっちみちインストール完了後に元に戻すので、とりあえず全部でいいです。エクスプローラで各ファイルを選択してマウス右クリックし、ポップアップメニューの「プロパティ」を選択し、タブ「全般」の「読み取り専用」のチェックが Off になっていることを確認します。さらに、タブ「セキュリティ」が表示されている場合は ( PC の環境によっては表示されないこともあります ) 、その一覧に表示されている全てのユーザとグループに「フルアクセス」権限を与えてください。設定ファイルは次の２個です。

*   `admin\includes\configure.php`
*   `catalog\includes\configure.php`

インストーラは Web ブラウザから実行します。 `http://localhost/catalog/install` を表示してください。



PHP などの設定に問題なければ次の画面が表示されます。



`ようこそ osCommerce へ!`

`インストール方法を選択して、インストールを開始してください:`



ボタン \[ New Install \] をクリックしてください。次の画面でデータベースの情報を入力します。



`新規インストール`

`1. インストールのためのオプションを設定してください:`

 `[v] カタログ・データベースのインポート`

 `[v] 自動設定`

`2. ウェブ・サーバに関する情報を入力してください:`

 `ウェブ・サーバのルート・ディレクトリ : C:/MySite/html`

 `カタログ・ディレクトリ : /catalog/`

 `管理ツール・ディレクトリ : /admin/`

 `WWW カタログ・ディレクトリ : /catalog/`

 `WWW 管理ツール・ディレクトリ : /admin/`

`3. データベース・サーバに関する情報を入力してください:`

 `データベース・サーバ : localhost`

 `ユーザ名 : osc`

 `パスワード : ***`

 `データベース : osc`



入力が終わったらボタン \[ Continue \] をクリックしてください。次の画面「 Step 1: データベース・インポート 」もボタン \[ Continue \] をクリックしてください。その次の画面「 Step 2: osCommerce の設定 」はほとんどデフォルトのままでいいのですが、最後の項目は「 セッション情報をファイルに保存する 」ではなく「 セッション情報をデータベースに保存する 」を選択してください。性能に影響があるのですが、開発・テストの環境の場合は後で手間のかからない方を選びます。



入力が終わったらボタン \[ Continue \] をクリックしてください。最後の画面で次の 2個のボタンが表示されます。

*   \[ Catalog \]
*   \[ Administration Tool \]

それぞれのボタンを押して、新しい画面が正常に表示されることを確認します。



\[ Catalog \] の方で画面の上の方に警告のメッセージが表示されます。次の作業をして、この画面を更新してください。これらのメッセージが消えるはず、だと思うのですが、 PC の環境によっては他にも何か対処が必要かもしれません。



*   ディレクトリ `C:\MySite\html\catalog\install` を削除する。
*   設定ファイル：それぞれのアクセス権限を元に戻し、「プロパティ」のタブ「全般」の「読み取り専用」のチェックを On にする。

*   `admin\includes\configure.php`
*   `catalog\includes\configure.php`

\[ Administration Tool \] の方は管理機能のログイン画面が表示されます。ユーザは `admin` 、初期パスワードは `admin` です。
