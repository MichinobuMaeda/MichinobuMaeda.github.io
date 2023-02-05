# Mac で Web開発するのだ

Update: 2008-01-27



> この記事を書いた後に [Zend Server](http://www.zend.com/en/products/server-ce/) や [XAMPP](http://www.apachefriends.org/jp/xampp.html) などを知りました。この記事のように個別に入れるよりこれらのパッケージを利用する方が楽です。 ( 参照 : [Zend Server CE / Zend Framework](https://sites.google.com/site/michinobumaeda/lamp/zendservercezendframework) / [PHPのデバッグができる環境](https://sites.google.com/site/michinobumaeda/lamp/phpdebugger) )



いまどきの Mac は “Photoshop がうごく BSD Unix” ですからね。 Apache などいれてみます。



Mac というか BSD のお約束がよくわからないので、こちらのページ [http://blog.phpdoc.info/archives/83-php-5.2.5-on-Leopard.html](http://blog.phpdoc.info/archives/83-php-5.2.5-on-Leopard.html) のおせわになることにします。



まず Xcode をインストールします。 OS の DVD におまけで入ってます。



Macports をダウンロードして入れます。で、次のコマンドを実行。


```
sudo port selfupdate
sudo port sync
```

MySQL は MySQL のサイトからコミュニティ版 Mac OS X 10.4 用のものをダウンロードしてインストールします。私の Mac は OS X 10.5 だけど問題なく動きます。試しに OS 再起動してみましたが、 MySQL は自動で起動してくれました。この辺に設定が入っているようですね。


```
/Library/StartupItems/MySQLCOM
```

root@localhost` のパスワードは次のようにして設定します。


```
sudo mysql
mysql> set password for 'root'@'localhost = PASSWORD('パスワード');
```

設定したパスワードで接続できることを確認します。


```
mysql -u root -pパスワード
```

MySQL GUI Tools も Mac 用が出ているのでダウンロードしてインストールしました。



PHP のため、今後のコンソール上での作業のために次のような設定をします。


```
sudo ln -s /usr/local/mysql/lib /usr/local/mysql/lib/mysql
sudo mkdir /usr/local/bin
sudo ln -s /usr/local/mysql/bin/my* /usr/local/bin
```

次のコマンドを2回実行して `f(^^` Apache をインストールします。


```
port install apache2
```

で、次のような設定を。


```
sudo w /Library/LaunchDaemons/org.macports.apache2.plist
sudo cp /opt/local/apache2/conf/httpd.conf.sample /opt/local/apache2/conf/httpd.conf
sudo mv /usr/sbin/apachectl /usr/sbin/apachectl-leopard
sudo ln -s /opt/local/apache2/bin/apachectl /usr/local/bin/apachectl
```

それから `/opt/local/apache2/conf/httpd.conf` の次の行をコメントアウト。


```
LoadModule ssl_module modules/mod_ssl.so
```

次のコマンドで Apache が起動して動いていることを確認します。


```
sudo apachectl start
```

PHP が依存するものをたくさんインストール。


```
port install jpeg
port install libpng
port install freetype
port install libmcrypt
port install tidy
```

`/tmp` あたりに PHP のソースを解凍してコンパイルしてインストールします。


```
'./configure' \
'--prefix=/Users/sean/php' \
'--with-apxs2=/opt/local/apache2/bin/apxs' \
'--with-xsl=/usr' \
'--with-tidy=/opt/local' \
'--enable-mbstring' \
'--with-gd' \
'--with-jpeg-dir=/opt/local' \
'--with-png-dir=/opt/local' \
'--with-zlib-dir' \
'--enable-sockets' \
'--enable-exif' \
'--with-mcrypt=/opt/local' \
'--enable-soap' \
'--with-mysql=/usr/local/mysql' \
'--with-pdo-mysql=/usr/local/mysql/bin/mysql_config' \
'--with-mysql-sock=/tmp/mysql.sock' \
'--with-freetype-dir=/opt/local' \
'--with-openssl=/opt/local' \
'--without-iconv' \
'--enable-cli'
make
sudo make install
```

`/opt/local/apache2/conf/httpd.conf` に次の設定を追加して、


```
AddHandler application/x-httpd-php .php
AddHandler application/x-httpd-php-source .phps
```

Apache をリスタートして、


```
<?php phpinfo(); ?>
```

と書いたページを表示して PHP が確かに動いていることを確認して終わりです。
