# Mac OS X の Python に PIL を入れる

Update: 2012-01-07

> 追記 ( 2012-01-07 ) : 下記の手順でエラーは消えましたが、GAE の BlobStore 周りなどはまだ正常に動いていないようです。



Mac OS X 10.7 で Google App Engine の Python 2.7 の開発環境を準備している最中のこと、 PIL など追加のライブラリを入れて 
`dev_appserver.py` を起動するとこんな警告が出るのです。


```
WARNING  2011-12-24 01:27:51,762 dev_appserver.py:3344] Could not initialize images API; you are likely missing the Python "PIL" module. ImportError: dlopen(/Library/Python/2.7/site-packages/PIL/_imaging.so, 2): Symbol not found: _jpeg_resync_to_restart

    Referenced from: /Library/Python/2.7/site-packages/PIL/_imaging.so
    Expected in: flat namespace
    in /Library/Python/2.7/site-packages/PIL/_imaging.so
```



依存関係のどこかがうまくいっていません。世の中に同じ悩みを持つ人が世の中にいないかと探してみると、いました。

http://stackoverflow.com/questions/1518573/snow-leopard-python-2-6-problems-getting-pil-to-work


試してみたところ shacker さんの回答が当たりで、 Lennart Regebro さんが紹介している

http://jetfar.com/libjpeg-and-python-imaging-pil-on-snow-leopard/

と併せてインストールをやり直しました。 jpeg のソースからインストールした作業ディレクトリが残っている状態から

```
$ sudo rm /opt/local/lib/*jpeg*
$ cd /tmp/jpeg-8
$ sudo make clea
$ cp /usr/share/ibtool/config/config.sub .
$ cp /usr/share/libtool/config/config.gues .
$ ./configure --enable-shared --enable-stati
$ mak
$ sud make install
$ sudo pip uninstal PIL
$ sudo pip install http//effbot.org/downloads/Imaging-1.1.7.tar.gz
```


として、 dev\_appserver.py を再起動すると、警告消えました。
