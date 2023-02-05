整理中：Windows VistaでPHPの開発

2009-06-05



> この記事を書いた後に [Zend Server](http://www.zend.com/en/products/server-ce/) や [XAMPP](http://www.apachefriends.org/jp/xampp.html) などを知りました。この記事のように個別に入れるよりこれらのパッケージを利用する方が楽です。 ( 参照 : [Zend Server CE / Zend Framework](zendservercezendframework.html) / [PHPのデバッグができる環境](phpdebugger.html) )



以前 Windows で PHP の開発 に Apache, MySQL, PHP のインストール手順を書いたのですが、 Vista でうまくいかないという話を聞いて自分でも試してみました。 今回は PHP のソースや MySQL の文字コードを EUC-JP にします。



手順の中で Webブラウザで確認するところがありますが、必ず表示を最新にしてください。 IE の場合 `[F5]` キー、 FireFox の場合 `[Ctrl]` を押しながら `[R]` です。

## Apache のインストール

[http://httpd.apache.org/download.cgi](http://httpd.apache.org/download.cgi) から Windows 用のインストーラ `apache_2.2.11-win32-x86-openssl-0.9.8i.msi` をダウンロードしました。インストーラの指示に従ってインストールすればいいのですが、設定をデフォルトから変えた箇所は次の通りです。



ドメイン、ホスト名、管理者パスワードに適当な値を入れます。本番環境ではないので、てきとーです。





![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5hXS5GkI/AAAAAAAABrA/cUBGe8Z-miU/s1600/phpvista_1.png)



インストール先を `C:¥site¥Apache2.2` にしました。 `C:¥Program Files` の下だと何かと面倒だからです。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5kJ9o3kI/AAAAAAAABrI/YWNFqHnhiU0/s1600/phpvista_2.png)



インストールが完了したら、 `http://localhost/` で “It works!” と表示されるのを確認します。また、画面の右下にサービスアイコンが表示されるので、サービスの停止や開始が正常にできることを確認します。 Apache の古いバージョンでは、 Visita でこのアイコンによるサービスの制御ができないことがありました。その場合は、「コントロールパネル」-「管理ツール」-「サービス」を使ってください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5lf6ftBI/AAAAAAAABrM/jewyNIjgKwc/phpvista_3.png)



## PHP のインストール

[http://www.php.net/downloads.php#v5](http://www.php.net/downloads.php#v5) の "Windows Binaries" から、 "PHP 5.2.9-2 installer" をダウンロードします。



インストール先は `C:¥site¥PHP` にしました。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5mVu9oQI/AAAAAAAABrQ/CAvLhPUxcRE/s1600/phpvista_4.png)



Web サーバは Apache2.2 を選択します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5nyWH2jI/AAAAAAAABrU/q8VY1f14BG8/s1600/phpvista_5.png)



Apache の設定ファイルのフォルダは `C:¥site¥Apache2.2¥conf` です。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5pKyrG8I/AAAAAAAABrY/332ooM1yyCk/s1600/phpvista_6.png)



すべてのオプションを選択します。選択肢が灰色ではな白になっていることをよく確認してください。マルチバイト文字列 ( mbstring ) 対応などをインストールしないと、日本人でなくても困ります。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5qSnWgMI/AAAAAAAABrc/ntxRG0jY91s/s1600/phpvista_7.png)



インストールが完了したらファイル `C:¥site¥Apache2.2¥conf¥httpd.conf` の



`#BEGIN PHP INSTALLER EDITS - REMOVE ONLY ON UNINSTALL`

`ScriptAlias /php/ "C:/site/PHP/"`

`Action application/x-httpd-php "C:/site/PHP/php-cgi.exe"`

`PHPIniDir "C:/site/PHP/"`

`LoadModule php5_module "C:/site/PHP/php5apache2_2.dll"`

`PHPIniDir "C:/site/PHP/"`

`LoadModule php5_module "C:/site/PHP/php5apache2.dll"`

`PHPIniDir "C:/site/PHP/"`

`LoadModule php5_module "C:/site/PHP/php5apache.dll"`

`#END PHP INSTALLER EDITS - REMOVE ONLY ON UNINSTALL`



を、次のように変更します。



`#BEGIN PHP INSTALLER EDITS - REMOVE ONLY ON UNINSTALL`

`PHPIniDir "C:/site/PHP/"`

`LoadModule php5_module "C:/site/PHP/php5apache2_2.dll"`

`#END PHP INSTALLER EDITS - REMOVE ONLY ON UNINSTALL`



このように変更して余計な設定を削除しないと、 Apache 再起動時にエラーが発生して起動できなくなります。



次に、ファイル名無しの URL 指定で `index.php` を表示するよう設定変更します 。`C:¥site¥Apache2.2¥htdocs¥index.html` のファイル名を `C:¥site¥Apache2.2¥htdocs¥index.php` に変えます。その後 `http://localhost/` を表示します。設定変更前は次のように表示されるか、エラーになるかどちらかです。



`Index of /`

`index.php`



ファイル `C:¥site¥Apache2.2¥conf¥httpd.conf` の



`<IfModule dir_module>`

 `DirectoryIndex index.html`

`</IfModule>`



を、次のように変更します。



`<IfModule dir_module>`

 `DirectoryIndex index.php index.html`

`</IfModule>`



Apache を再起動したら、 `http://localhost/` で “It works!” と表示されるのを確認します。



最後に、PHPで文字コード EUC-JP を使うための設定をします。 `C:¥site¥PHP¥php.ini` の `[mbstring]` の設定内容を次のようにしてください。インストールしたままの状態では、たぶん、これらの行はコメントアウトされていると思います。



`mbstring.language = Japanese`

`mbstring.internal_encoding = EUC-JP`

`mbstring.http_input = auto`

`mbstring.http_output = EUC-JP`

`mbstring.encoding_translation = Off`

`mbstring.detect_order = auto`

`mbstring.substitute_character = none`

## MySQL のインストール

[http://dev.mysql.com/downloads/](http://dev.mysql.com/downloads/) の "MySQL Community Server | Download » " から Windows MSI Installer (x86) をダウンロードしました。 MySQL のプログラムのインストールの完了時に次の画面が出ます。チェックを On にしたまま Finish ボタンを押すと、データベースを設定するウィザードが起動します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5smClE2I/AAAAAAAABrg/qEFthMhb-jM/s1600/phpvista_8.png)



文字コードは ujis を選択してください。これが EUC-JP です。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5uOVqkGI/AAAAAAAABrk/sRzPVHskV_A/s1600/phpvista_9.png)



ユーザ `root` のパスワードを設定してください。本番環境では強いパスワードにしてください。開発環境でも、「パスワード無しはあり得ない」という前提で作られたツールがあると思うので、必ず設定してください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5jKhd5gI/AAAAAAAABrE/RDVwfPY63dk/s1600/phpvista_10.png)



## phpMyAdmin のインストール

[http://www.phpmyadmin.net/home\_page/downloads.php](http://www.phpmyadmin.net/home_page/downloads.php) から `phpMyAdmin-3.1.5-all-languages.zip` をダウンロードしました。それを解凍して `C:¥site¥Apache2.2¥htdocs¥phpMyAdmin` に置きました。



設定ファイルのサンプルは `C:¥site¥Apache2.2¥htdocs¥phpMyAdmin¥config.sample.inc.php` です。これをコピーして `C:¥site¥Apache2.2¥htdocs¥phpMyAdmin¥config.sample.inc.php` を作ります。



設定ファイルの次の値に適当な、本当にてきとーな値を入れます。



`$cfg['blowfish_secret'] = 'slkfak2ok0lajsdfnwidlv';`



サーバの名称は通常 `localhost` でいいのですが、レンタルサーバ等の場合、違う名称にしなければならないことがあります。そのときは次の値を変更してください。



`$cfg['Servers'][$i]['host'] = 'localhost';`



`http://localhost/phpMyAdmin/` を表示して、ユーザ `root` で正常にログインできれば確認完了です。パスワードは MySQL のインストール時に設定したパスワードです。
