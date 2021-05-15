dokuwiki on Nginx
=====

Update: 2017-11-26


久しぶりにサイトリニューアルしてみようかと思い立って、 Nginx に dokuwiki を載せてみました。
サイト全体ではなくサブディレクトリに dokuwiki を置きます。
OS は Debian 9 です。

必要なパッケージは ``nginx`` ``php-fpm`` ``php-xml`` です。
インストール後に ``service --status-all`` で ``nginx`` と ``php7.0-fpm`` が動いているのを確認します。
dokuwiki は Debian のパッケージは使わずに手動で導入しました。コピーするだけだし。
FPM や URL Rewrite は
https://www.dokuwiki.org/install:nginx
を参考に以下のような感じで。
仕事では Nginx をリバースプロキシに使ったことしかなくて
FastCGI の設定は初めてなので、不要な設定があるかもしれません。

```
  index index.html index.htm doku.php;
  
  location / {
    try_files $uri $uri/ =404;
  }

  location /tec/ { try_files $uri $uri/ @tec; }
  location @tec {
    rewrite ^/tec/_media/(.*) /tec/lib/exe/fetch.php?media=$1 last;
    rewrite ^/tec/_detail/(.*) /tec/lib/exe/detail.php?media=$1 last;
    rewrite ^/tec/_export/([^/]+)/(.*) /tec/doku.php?do=export_$1&id=$2 last;
    rewrite ^/tec/(.*) /tec/doku.php?id=$1&$args last;
  }
  location ~ ^/tec/(data/|conf/|bin/|inc/|install.php) { deny all; }
  location ~ ^/tec/.*\.php$ {
    try_files $uri $uri/ /tec/doku.php;

    #include snippets/fastcgi-php.conf;
    fastcgi_split_path_info ^(.+\.php)(/.+)$;
    #try_files $fastcgi_script_name =404;
    set $path_info $fastcgi_path_info;
    fastcgi_param PATH_INFO $path_info;
    fastcgi_index index.php;
    include fastcgi.conf;

    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param REDIRECT_STATUS 200;
    fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
  }
```

``snippets/fastcgi-php.conf`` は設定 ``try_files`` の競合が起きたので、それ以外の内容をコピーしました。
dokuwiki のドキュメントには image medeia が云々と書かれていますが、最新版では何もしなくてだいじょうぶそうです。

あとは、同様の設定を別のサブフォルダに入れて動くかどうかですね。

Tag: nginx dokuwiki php fpm fastcgi debian rewrite
