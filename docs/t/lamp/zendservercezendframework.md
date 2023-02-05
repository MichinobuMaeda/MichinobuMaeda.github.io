整理中：Zend Server CE / Zend Framework

##

<!-- google\_ad\_client="pub-7953317888125639"; google\_ad\_host="pub-6693688277674466"; google\_ad\_width=250; google\_ad\_height=250; google\_ad\_format="250x250\_as"; google\_ad\_type="text\_image"; google\_color\_border="999999"; google\_color\_bg="FFFFFF"; google\_color\_link="000000"; google\_color\_url="0033CC"; google\_color\_text="444444"; //-->

Windows, Linux, Mac にインストールする

2009-05-06



PHP の実行環境＋α の Zend Server Community Edition を Windows, Linux, Mac それぞれについて、どのくらい簡単にインストールできるか試してみました。

### Zend Server CE の入手

Zend Server Community Edition のページは http://www.zend.com/en/community/zend-server-ce です。このページのリンク Download Zend Server CE をクリックすると、各 OS のインストーラをダウンロードできるページに移動します。各 OS 向けのインストーラは、それぞれの OS の標準的な方式を採っています。特に Mac 版の、オプションの選択も何もなくすべてインストールして HTTP サーバも MySQL も自動で起動してしまう簡単さはには驚かされました。関連記事 ( [Mac で Web開発するのだ](mamp.html) / [Windows で PHP の開発](phponwin.html) / [Windows VistaでPHPの開発](vistaphp.html) ) を書いたときの苦労、というか、面倒くささはは何だったんだろうという感じです。



インストールの前提条件や注意事項など詳細は [Zend Server CE Installation Guide](http://files.zend.com/help/Zend-Server-Community-Edition/zend-server-community-edition.htm#installation_guide.htm) を見てください。そこに書いていることをここで繰り返すことはしません。私が気になった点などを記します。

### Windows XP

インストール時の Windows のユーザは Administorator 権限を持っていなければなりません。ダウンロードした `ZendServer-CE-4.0.1-Windows_x86.exe` を適当なフォルダに置いて、実行します。



“Setup Type” は “Full” を選択しました。



“Web Server” は Apache を選択しました。



インストールの途中で Windows ファイアウォールの警告が出ます。 “このプログラムをブロックし続けますか? Apache HTTP Server” というものですが、「ブロックを解除する」を選択しました。



それ以外はデフォルトの選択です。インストールが終わるとスタートメニューに次の項目が登録されています。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6Yx3Cp6I/AAAAAAAABtY/slkRrZZtza8/s1600/zendserverce_install_1.png)



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6aA7JJ3I/AAAAAAAABtc/tJ3HqpGsYjQ/s1600/zendserverce_install_2.png)



また、画面右下に “Zend Controller” と “Apache” のアイコンが表示されています。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6be2x5KI/AAAAAAAABtg/8FfqptfUhkI/zendserverce_install_3.png)![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6csRsmnI/AAAAAAAABtk/P4rryuQifBA/zendserverce_install_4.png)



MySQL の設定内容を確認・変更しました。「スタートメニュー」の



`Zend Server Community Edition`

 `- MySQL Server 5.0`

 `- MySQL Server Instance Config Wizard`



を起動します。設を定変更した箇所は以下の通りです。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6evsOCqI/AAAAAAAABto/26vgBhKWvFE/s1600/zendserverce_install_5.png)



InnoDB のフォルダを指定しました。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6h1FaajI/AAAAAAAABts/yWU9Xg8UQXo/s1600/zendserverce_install_6.png)



文字コード UTF-8 を選択しました。2番目の選択肢、(日本語) と書いてあるところです。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6kQ35WkI/AAAAAAAABtw/2wF5upqXSqE/s1600/zendserverce_install_7.png)



ユーザ root のパスワードを設定しました。

### Ubuntu Desktop 8.04 日本語版

コマンドライン上の作業になります。各コマンドで `sudo` を使うか、 "`# sudo bash"` で `root` ユーザになるか、どちらかで作業します。後者はいい方法ではありません。セキュリティに配慮した `sudo` の機能が実質無効になってしまいます。



Zend Server CE Installation Guide の “DEB Installation” の手順に従って

*   `/etc/apt/sources.list` にリポジトリを追加し、
*   リポジトリの公開キーを取得し、
*   `aptitude update` でリポジトリの情報を取得し、
*   `aptitude install zend-ce` で本体をインストール

しました。さらに以下のコマンドでオプションをインストールします。



`aptitude install php5-extra-extensions-zend-ce`

`aptitude install php-source-zend-ce`

`aptitude install php-dev-zend-ce`

`aptitude install java-bridge-zend-ce`

`aptitude install php-loader-zend-ce`

`aptitude install phpmyadmin-zend-ce`

`...`

`以下の新規パッケージがインストールされます:`

 `exim4 exim4-base exim4-config exim4-daemon-light libdbd-mysql-perl`

 `libdbi-perl libhtml-template-perl libnet-daemon-perl libplrpc-perl mailx`

 `mysql-client-5.0 mysql-server mysql-server-5.0 phpmyadmin`

 `phpmyadmin-zend-ce`

`...`

`aptitude install zend-framework-dojo-ce`

`aptitude install zend-framework-extras-ce`

`aptitude install php-ibmdb2-zend-ce`

`...`

`以下のパッケージには満たされていない依存関係があります:`

 `php-ibmdb2-zend-ce: 依存: db2exc これは仮想パッケージです。`

`Resolving dependencies...`

`依存関係を解決できません! 諦めています...`

`中断。`

`...`

`aptitude install php-pdo-ibm-zend-ce`

`...`

`以下のパッケージには満たされていない依存関係があります:`

 `php-pdo-ibm-zend-ce: 依存: db2exc これは仮想パッケージです。`

`Resolving dependencies...`

`依存関係を解決できません! 諦めています...`

`中断`



MySQL と phpMyAdmin は `phpmyadmin-zend-ce` が依存するパッケージとしてインストールされます。また、MySQL のインストールの途中で root ユーザの入力が求められます。ディレクトリ `/etc/apache2/conf.d/` を見るとファイル `phpmyadmin.conf` ができています。その内容を見ると、 phpMyAdmin のインストール先や、 URL が `http://localhost/phpmyadmin/` になっていることなどがわかります。phpMyAdmin には `root` ユーザでログインしてください。 DB インスタンスの文字コードは UTF-8 になっていました。



IMB DB2 関連のオプションはインストールできませんでした。当面使う予定はないのでこのままとします。



最後に “DEB Installation” に従って環境変数 `PATH` を変更します

### Fedora 9 x86\_64

Fedora のインストール時の構成は、 xen を追加してゲームなどを外した以外すべてデフォルトです。 64bit 版で仮想マシンを使う構成にしたのは別の用途のためです。 Zend Server のインストールには特に影響しないはずです。



Zend Server CE Installation Guide の “RPM Installation” の手順に従ってインストールすればいいのですが、私が引っかかったところは次の通り。

#### SELinux 対応

SELinux による規制を解除しないと Zend Server が正常に起動できません。手順によると "`# setenforce permissive"` を実行すればよいとのことですが、それでいいのか？ まあ、いいや。

#### リポジトリの設定

`/etc/yum.repos.d/zend.repo` の設定は手順の記述通りではうまくいきませんでした。 `baseurl` の値の末尾に `”/”` が必要です。私が設定した内容は以下の通りです。



`[Zend]`

`name=Zend CE $releasever - $basearch - Released Updates`

`baseurl=http://repos.zend.com/rpm/ce/$basearch/`

`enabled=1`

`gpgcheck=0`

`[Zendce-noarch]`

`name=Zend CE - noarch`

`baseurl=http://repos.zend.com/rpm/ce/noarch/`

`enabled=1`

`gpgcheck=0`

#### yum コマンドの実行順

“RPM Installation” では



`1.Run the command:`

`# yum install zend-ce`

`2. To clean your packages cache and ensure retrieval of updates from the web, run:`

`yum clean all`



となっているのですが、

1.  yum clean all
2.  yum install zend-ce

の順ですよね？



それ以外は Ubuntu の場合と同様に MySQL など依存するものを含めて問題なくインストールできました。



Ubuntu の場合と違って MySQL のインストール中に root のパスワードの入力を求められなかったので、後で手動で設定します。



`# mysql -u root`

`mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('********');`

`mysql> quit`



`"# mysql -u root -p"` で設定したパスワードで接続できることを確認します。



phpMyAdmin は Basic 認証を使う設定になっていましたが、これは私の好みでログインページを表示するように変更しました。 `/usr/share/phpMyAdmin/config.inc.php` の 次の行を変更します。



`$cfg['Servers'][$i]['auth_type']     = 'cookie';`



最後に “RPM Installation” に従って環境変数 PATH を変更します。

### Mac OS X

`ZendServer-CE-4.0.2-1.dmg` をダウンロードして、中に入っている ZendServer.pkg を開いて、後は画面の指示に従って進めばインストール完了です。



Zend Server そのものは `http://localhost:10088/` です。インストールした状態そのままであれば “Zend Server Test Page” が表示されます。



Zend Server の管理画面は `http://localhost:10081/` です。初回はパスワードの設定が求められます。ログインしたページにリンク “Open phpMyAdmin” ( `http://localhost:10081/phpmyadmin/` ) があります。 phpMyAdmin を開いて root ( 初期状態ではパスワード無し ) でログインすると “The configuration file now needs a secret passphrase (blowfish\_secret).” と警告が出ているので `/usr/local/zend/share/phpmyadmin/config.inc.php` の該当箇所に暗号化の種になる適当な ( 本当にてきとーな ) 値を記入します。そういえば、他の OS 版のインストールの後で、この設定をしていなかったような。。。



MySQL の `root` ユーザにパスワードを設定しようと思ってコマンドをたたくとパスが通っていなかったので、 `/etc/profile` に次の設定を追加しました。



`PATH=$PATH:/usr/local/zend/bin:/usr/local/zend/mysql/bin`

`LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/zend/lib`



次のコマンドで、現在の環境に設定を反映します。



`# source /etc/profile`



このあたり、「なんのことやら？」という人は Mac 、というより UNIX の基本的な使い方をお勉強してください。 Linux も同様です。



MySQL の `root` ユーザのパスワードの設定は次の通り。



`# mysql -u root`

`mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('********');`

`mysql> quit`



さらにもう 1行、次のコマンドをたたいて設定したパスワードでログインできることを確認します。



`# mysql -u root -p`



## Zend Framework を試してみる

2009-07-08



Zend Framework を使ってアプリケーションを作ってみます。今回作るのは、母上が時々送ってくる写メを取り込んで、Blogのような体裁にするツールです。

### 実行環境

Zend Server に実行環境一式入っています。個別にインストールする場合は次のものが必要です。

*   Apache 2.2
*   PHP 5.2
*   Zend Framework 1.8.4
*   MySQL 5.1 またはその他のRDBMS

MySQL は古いバージョンでもたいていだいじょうぶですが、PHP は5.2.4 以降が必要になります。共用形式のレンタルサーバの場合、PHP のバージョンの確認が必要です。



Zend Framework は `/usr/local/ZendFramework-1.8.4` に置きました。PHP の設定は次のように変更しました。

*   Core

*   include\_path = .:/usr/local/ZendFramework-1.8.4/library

*   mbstring

*   mbstring.language = Japanese
*   mbstring.internal\_encoding = UTF-8
*   mbstring.http\_output = UTF-8
*   mbstring.encoding\_translation = Off

私は `php.ini` で設定しましたが、共用タイプのレンタルサーバなど `php.ini` を直接編集できない環境の場合は `.htaccess` で設定変更したのでいいと思います。こんな感じ。



`php_value include_path ".:/usr/local/ZendFramework-1.8.4/library"`



`public/index.php` の先頭に次の1行を追加したのでもだいじょうぶでした。



`ini_set("include_path", ".:/usr/local/ZendFramework-1.8.4/library");`



Zend Framework を置く場所は、できれば公開されていないディレクトリにしましょう。

### 開発環境

Eclipse PHP Development Tools から Eclipse PDT All-in-one をダウンロードして使いました。ワークスペースのパスは `/Users/michinobu/workspace-pdt` としました。`/home/…` じゃなくて `/Users/…` なのは Mac OS X だからです。

### ドキュメント

次のようなドキュメントをダウンロードしていつでも見ることができるようにしておくといいでしょう。

*   MySQL 5.1 リファレンスマニュアル
*   PHP マニュアル
*   Zend Framework プログラマ向けリファレンスガイド
*   Zend Framework API Documentation

「Zend Framework プログラマ向けリファレンスガイド」は、日本語訳されず、英語のままのページがたくさんあるようです。

### プロジェクトの作成

プロジェクト名は dormouse としました。



Eclipse でプロジェクトを作成します。

*   メニュー Window - Open Perspective - PHP を選択します。
*   メニュー File - New - PHP Project を選択します。
*   プロジェクト名として dormouse と入力し Finish ボタンを押します。

Zend Framework でプロジェクトを作成します。「リファレンスガイド」の「4.2. Zend\_Application Quick Start」の手順に従い次のコマンドを実行します。



`/usr/local/ZendFramework-1.8.4/bin/zf.sh  create project dormouse`



Windows の場合は zf.bat を使えばいいようです。できあがったプロジェクトのサブディレクトリを Eclipse のプロジェクトの下にコピーします。



`cd dormouse/`

`cp -rf * /Users/michinobu/workspace-pdt/dormouse/`



Eclipse で `[F5]` キーを押すと、追加されたサブディレクトリが表示されます。サブディレクトリ public が `http://ホスト名/dormouse/` で表示されるように Apache の `httpd.conf` に設定を追加して Apache を再起動します。



`Alias /dormouse /Users/michinobu/workspace-pdt/dormouse/public`



`<Directory "/Users/michinobu/workspace-pdt/dormouse/public">`

 `Options Indexes FollowSymLinks`

 `AllowOverride All`

 `Order allow,deny`

 `Allow from all`

`</Directory>`



ブラウザで `http://ホスト名/dormouse/` が正常に表示できることを確認します。「Welcome to the Zend Framework!」と表示されました。



Eclipse からは参照できませんが、サブディレクトリ `public` の下には `.htaccess` が作られています。次のように修正しました。



`RewriteEngine On`

`RewriteCond %{REQUEST_FILENAME} -s [OR]`

`RewriteCond %{REQUEST_FILENAME} -l [OR]`

`RewriteCond %{REQUEST_FILENAME} -d`

`RewriteBase /dormouse/`

`RewriteRule ^.*$ - [NC,L]`

`RewriteRule ^.*$ index.php [NC,L]`



このアプリケーションの URL の一番上のレベルが `/` ではなく `/dormouse/` なので `RewriteBase` を追加しています。



`public/index.php` の中で定数 `APPLICATION_PATH` を定義しています。実環境のディレクトリ構成が開発環境と異なる場合は、この定数の値を変更すればいいようです。



次に、「4.2.3. Adding and creating resources」の記述に素直に従って、いくつか設定を追加します。



`application/configs/application.ini` のセクション `[production]` に次の 2行を追加します。



`resources.layout.layout = "layout"`

`resources.layout.layoutPath = APPLICATION_PATH "/layouts/scripts"`



フォルダ `application/layouts/scripts` を追加します。



ファイル `application/layouts/scripts/layout.phtml` を作成します。



`<?php echo $this->doctype() ?>`

`<html>`

`<head>`

 `<?php echo $this->headTitle() ?>`

 `<?php echo $this->headLink() ?>`

 `<?php echo $this->headStyle() ?>`

 `<?php echo $this->headScript() ?>`

`</head>`

`<body>`

 `<?php echo $this->layout()->content ?>`

`</body>`

`</html>`



`application/Bootstrap.php` に次のメソッドを追加します。



 `protected function _initView()`

 `{`

 `// Initialize view`

 `$view = new Zend_View();`

 `$view->doctype('XHTML1_STRICT');`

 `$view->headTitle('My First Zend Framework Application');`



 `// Add it to the ViewRenderer`

 `$viewRenderer = Zend_Controller_Action_HelperBroker::getStaticHelper(`

 `'ViewRenderer'`

 `);`

 `$viewRenderer->setView($view);`



 `// Return it, so that it can be stored by the bootstrap`

 `return $view;`

 `}`



もう一度ブラウザで `http://ホスト名/dormouse/` を表示します。先ほどのものと何が違うのかというと、 `<head> 〜 </head>` などがソースに含まれています。見た目はほとんど変わりません。つまり、アプリケーションを作る際には `<body> 〜 </body>` の中だけ考えたらいいということのようです。

### DBの接続を定義する

`application/configs/application.ini` のセクション `[production]` にこんな設定をしておくと、



`resources.db.adapter = "pdo_mysql"`

`resources.db.params.host = "localhost"`

`resources.db.params.username = "dormouse"`

`resources.db.params.password = "**********"`

`resources.db.params.dbname = "dormouse"`

`resources.db.isDefaultTableAdapter = true`



こんな感じでDB接続アダプターを取得できるそうです。



`$resource = $bootstrap->getPluginResource('db');`

`$db = $resource->getDbAdapter();`



なにもしなくても、上記の通り `application/configs/application.ini` に



`resources.db.isDefaultTableAdapter = true`



と設定しているので、 `Zend_Db_Table_Abstract` のサブクラスがこのDB接続アダプターを勝手に使ってくれます。単純な処理は `model` として `Zend_Db_Table_Abstract` のサブクラスを使うことにします。



それから、[\[#ZF-1541\]](http://framework.zend.com/issues/browse/ZF-1541) によると、 `Charcter set` の設定をうまくやる手段がまだないようです。それぞれの Action Controller の `init()` に次のような処理を追加して問題を回避しました。



 `public function init()`

 `{`

 `....`

 `$db = $bootstrap->getPluginResource('db')->getDbAdapter();`

 `$db->getConnection()->exec("SET NAMES 'utf8'");`

 `}`



### ログを出力できるようにする

`Zend_Log` クラスは、 Java の log4j に似た機能を持っています。`Bootstrap` クラスに `Zend_Log` のインスタンスを作成する処理を追加して、使ってみます。まず、 `application/configs/application.ini` のセクション `[production]` に次の 2行を追加します。



`log.level = 7`

`log.path = /var/log/dormouse/dormouse.log`



`application/Bootstrap.php` クラスに 次のメソッドを追加します。



 `protected function _initLog()`

 `{`

 `$opt = $this->getApplication()->getOptions();`

 `$writer = new Zend_Log_Writer_Stream($opt['log']['path']);`

 `$logger = new Zend_Log($writer);`

 `$filter = new Zend_Log_Filter_Priority(intval($opt['log']['level']));`

 `$writer->addFilter($filter);`

 `$logger->debug('Bootstrap->_initLog()');`

 `return $logger;`

 `}`



`application/controllers/IndexController.php` を次のように修正します。



c

`lass IndexController extends Zend_Controller_Action`

`{`



 `protected $logger;`

 `public function init()`

 `{`

 `$bootstrap = $this->getInvokeArg('bootstrap');`

 `$this->logger = $bootstrap->getResource('log');`

 `$this->logger->debug('IndexController->init()');`

 `}`



 `public function indexAction()`

 `{`

 `$this->logger->debug('IndexController->indexAction()');`

 `}`

`}`



ログ出力先のディレクトリ `/var/log/dormouse` を作成して、必要な書き込み権限を設定しておきます。ここまでで準備完了です。 `http://ホスト名/dormouse/` を再表示（更新）します。すると、次のようにログ出力されます。



`2009-07-08T16:29:15+09:00 DEBUG (7): Bootstrap->_initLog()`

`2009-07-08T16:29:15+09:00 DEBUG (7): IndexController->init()`

`2009-07-08T16:29:15+09:00 DEBUG (7): IndexController->indexAction()`



`application/configs/application.ini` の `log.level` を 4 ( WARN ) や 3 ( ERR ) などに変更すると、これらの DEBUG レベルのログは出力されなくなります。

### 認証

今回は、メールサーバを認証に使うことにしました。メールサーバのアカウントを持っている人が、このツールを使う権限を持っている人ということでいいからです。Zend Framework には、認証情報の格納先として DB などを使うアダプタクラスがいくつか用意されています。でも、メールサーバを使うものはないので自作することにします。



認証のアダプタは `Zend_Auth_Adapter_Interface` を実装したクラスとして作成します。実装するメソッドは `authenticate()` だけです。このメソッドから、認証の結果を格納した `Zend_Auth_Result` オブジェクトを返します。認証の処理中にシステムエラーが発生した場合は例外 `Zend_Auth_Adapter_Exception` を投げます。



実装したアダプタは次のように使います。こうすると、自動で、セッションにユーザIDを格納してくれます。単純なアプリケーションなら、明示的にセッションを使わずに済ませることができるでしょう。



`$auth = Zend_Auth::getInstance();`

`$result = $auth->authenticate(new ImapAuthAdapter(...));`



ログアウトなどの際に認証を取り消すには次のようにします。



`Zend_Auth::getInstance()->clearIdentity();`



余談ですが、私のメールサーバの認証には LDAP を使っていたので、 LDAP 用のアダプタを使えばよかったようです。もう、作ってしまったから、このままでいいや。

### サンプル

サンプルはこちら。

*   [dormouse-1\_50.zip](https://sites.google.com/site/michinobumaeda/lamp/zendservercezendframework/dormouse-1_50.zip?attredirects=0)

*   [dormouse-1\_35.zip](https://sites.google.com/site/michinobumaeda/lamp/zendservercezendframework/dormouse-1_35.zip?attredirects=0)
*   [dormouse-1\_32.zip](https://sites.google.com/site/michinobumaeda/lamp/zendservercezendframework/dormouse-1_32.zip?attredirects=0)
*   [dormouse-1\_20.zip](https://sites.google.com/site/michinobumaeda/lamp/zendservercezendframework/dormouse-1_20.zip?attredirects=0)
*   [dormouse-1\_10.zip](https://sites.google.com/site/michinobumaeda/lamp/zendservercezendframework/dormouse-1_10.zip?attredirects=0)
*   [dormouse-1\_00.zip](https://sites.google.com/site/michinobumaeda/lamp/zendservercezendframework/dormouse-1_00.zip?attredirects=0)

*   http://www.michinobu.jp/keiko/ ( 閉鎖 )

何つくろうとしたかは README.txt 見てください。



1.50 で、 MySQL から Sqlite に変更してみました。DBの接続先と、日付の書式の変更だけで済みました。また、この 1.50 から開発環境に ZendFramework 1.95 を使用しています。

## Zend Server の Zend Framework をアップデート

2009-11-23



私の MacBook とレンタルサーバの Zend Server の Zend Framework をアップデートしてみました。



手順は簡単です。

*   php –version で PHP のバージョンが 5.2.4 以上なのを確認します。
*   現時点で最新の Zend Framework 1.9.5 をダウンロードして解凍する。
*   `/usr/local/zend/share/ZendFramework/` の下のものを入れ替える。
*   念のため httpd を reload または restart する。

後は、自分が使っているアプリケーションなどの動作確認をします。
