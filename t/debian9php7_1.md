Debian 9 に PHP 7.1, 7.2 をインストールする
=====

Update: 2018-07-03


共用タイプのレンタルサーバの PHP のバージョンを調べてみると、
今、この文章を書いている時点 ( 2018年7月 ) では
PHP 7.1 とか 7.2 の場合が多いです。

その環境で動くプログラムのテストのために自分のサーバの設定をしようとしたら、
Debian 9 は PHP 7.0 なんですね。

How to Install PHP 7.2, 7.1 and 5.6 on Debian 9 Stretch System\\
https://www.looklinux.com/how-to-install-php-7-2-7-1-and-5-6-on-debian-9-stretch-system/

に 7.0 以外のバージョンの PHP を Debian 9 に入れる方法が出ていました。

PPA: Personal Package Archives を追加します。

```
$ sudo apt install ca-certificates apt-transport-https 
$ wget -q https://packages.sury.org/php/apt.gpg -O- | sudo apt-key add -
$ sudo echo "deb https://packages.sury.org/php/ stretch main" | tee /etc/apt/sources.list.d/php.list
```

PHP 7.1 だったらこんな感じで。

```
$ sudo apt update
$ sudo apt install php7.1
```

Tag: Debian PHP
