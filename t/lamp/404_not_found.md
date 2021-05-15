404 Not Found
=====

Update: 2011-05-12

ある日の、ある Web サーバのログです。

悪いことしようとする人が、それらしいパスを指定してアクセスを試みています。

ご丁寧に２回ずつ。

なるほど、こういうところを狙うと。

phpMyAdmin を設置するときは、パス名変えた方がよさそう。


```
 Requests with error response codes
 404 Not Found
 /admin/phpmyadmin/scripts/setup.php: 2 Time(s)
 /admin/pma/scripts/setup.php: 2 Time(s)
 /admin/scripts/setup.php: 2 Time(s)
 /db/scripts/setup.php: 2 Time(s)
 /dbadmin/scripts/setup.php: 2 Time(s)
 /images/logo_elastix.png: 2 Time(s)
 /myadmin/scripts/setup.php: 1 Time(s)
 /mysql/scripts/setup.php: 2 Time(s)
 /mysqladmin/scripts/setup.php: 2 Time(s)
 /phpMyAdmin/scripts/setup.php: 2 Time(s)
 /phpadmin/scripts/setup.php: 2 Time(s)
 /phpmyadmin/scripts/setup.php: 2 Time(s)
 /pma/scripts/setup.php: 2 Time(s)
 /scripts/setup.php: 2 Time(s)
 /sqlweb/scripts/setup.php: 2 Time(s)
 /web/phpMyAdmin/scripts/setup.php: 2 Time(s)
 /web/phpmyadmin/scripts/setup.php: 2 Time(s)
 /web/scripts/setup.php: 2 Time(s)
 /webadmin/scripts/setup.php: 2 Time(s)
 /webdb/scripts/setup.php: 2 Time(s)
 /websql/scripts/setup.php: 2 Time(s)
```
