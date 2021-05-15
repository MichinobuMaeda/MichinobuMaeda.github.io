VPS でメモリを節約する
=====

Update: 2009-09-26



このサーバ ( 記事を書いた当初のサーバ ) は VPS ( Virtual Private Server ) を利用しているのですが、ある一つのメモリのパラメータだけが不足気味でした。それを、各プロセスの設定の変更でかなり改善できました。



この VPS は Parallels の製品を使っています。最初はプロバイダが提供する最小単位を使っていたのですが、メールサーバ、DBサーバ、LDAPサーバなどを入れた後、 `yum install` で複数のパッケージをインストールするだけでハングするようになってしまいました。それで今は 2個分に拡張しています。それでもまだときどき `privvmpages` についてアラートが出ていました。それを本気出してチューニングしてみようと思ったわけです。ちなみに、チューニングの前も後もあまり変わらない全体の状況は…



```
# free
 total       used       free     shared    buffers     cached
Mem:        368640      77668     290972          0          0          0
-/+ buffers/cache:      77668     290972
Swap:            0          0          0
```

物理メモリはかなり余っています。 Swap が無いですが、それは VPS だから。

## httpd の調整はあまり効果無し

`ps -ef` してみるとたくさん表示されるのが `httpd` と `saslauthd` です。`saslauthd` のメモリの消費量は少ないようなので、 `httpd` のプロセスの数を減らしたり、不要なモジュールを読み込まないようにしたのですが、あまり効果がありません。 DSO ( Dynamic Shared Object ) によるメモリの節約が効いているのかな？

## 本当にメモリを浪費しているプロセスは?

次に `ps aux` とか `grep Vm /proc/*/status` とかやってみます。 `privvmpages` に関係あるのは `VmData` かなぁ。 `grep VmData /proc/*/status` で大食いのプロセスを探します。どうも MySQL と OpenLDAP のようです。

## OpenLDAP のデータキャッシュを減らす

OpenLDAP のバックエンドには BDB を使っています。「そういえば `/var/lib/ldap/DB_CONFIG` はインストールした後デフォルトのまま放置していたなぁ」と見てみると、大きなキャッシュサイズを設定しています。LDAP のエントリの数は両手で足りるくらいしかないので、これをおもいっきり小さくして、 `slapd` を再起動します。 Parallels の管理画面の Resources - Memory - Secondary System Parameters - privvmpages を見ると効果有りです。

## MySQL は MyISAM しか使っていないので...

MySQL のメモリ使用量は起動オプションで調整できます。つまり、 `/etc/init.d/mysqld` を編集すればいいわけです。



このサイトの場合 `–key_buffer_size` と `–sort_buffer_size` は小さな値でだじょうぶです。それぞれの意味については MySQL のドキュメントの “7.5.3. Tuning Server Parameters” などを見てください。これらを変更して再起動するとばっちり効果有りです。



他に何か無いかなぁと探していると [Reducing MySQL Memory Usage for Low End Boxes](http://www.lowendbox.com/blog/reducing-mysql-memory-usage-for-low-end-boxes/) という記事を見つけました。このサーバでは MyISAMしか使っていません。起動オプションに `–skip-bdb` と `–skip-innodb` を追加して再起動します。めちゃめちゃ効果有りです。



ここまでやった結果は次の通り。 LDAP がなければ VPS １部屋分の最小単位でもだいじょうぶかな。



```
Parameter   Current Use Soft Limit Hard Limit Units
privvmpages      52,466    125,000    150,000 4KB pages
```
