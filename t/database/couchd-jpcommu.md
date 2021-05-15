CouchDBを始めてみようと思ったのですが。。。
=====

Update: 2012-12-13

[Apache CouchDB](http://couchdb.apache.org/) を始めてみようと思ったのですが、[日本のコミュニティのメーリングリスト](https://groups.google.com/group/couchdb-jp/topics?hl=ja) は今年の１月あたりが最後の投稿になっているような。。。周回遅れだったかな。。。とりあえず登録はしました。

CouchDB は JSON 形式でデータを格納する Document-oriented な NoSQL です。

*   HTTP による単純なインターフェース ( REST API )
*   いつでも電源OFFしてOKな感じの耐障害性
*   Optimistic locking
*   MapReduce による view

といった特徴が気に入りました。これができるなら、ディスクを余分に使うことになっても、性能面で劣るとしても、 Mongo DB よりおもしろそうだと思ったのです。アプリケーションの処理の複雑さによっては CouchDB の方が性能が出る場合もあるかもしれません。 Mongo DB との比較は [Comparing Mongo DB and Couch DB](http://www.mongodb.org/display/DOCS/Comparing+Mongo+DB+and+Couch+DB) をご覧ください。 CouchDB のストレージの概要については [The Power of B-trees](http://guide.couchdb.org/draft/btree.html) を。まだ斜め読んだだけですが、確かにこの仕組みなら SSD が長持ちしそうです。

まず、なにはともあれ動かしてみます。

現時点 ( 2012-12-13 ) の最新の 1.2.0 を使います。 Mac OS X では後述する "Test Suite" が通りませんでした。 Ubuntu 12.04 で `aptitude show couchdb` してみると、 `Version: 1.0.1-0ubuntu18` 。。。 [ソースからインストール](http://guide.couchdb.org/draft/source.html) することにします。まず、 OS のグループとユーザが必要です。こんな感じでいいのではないかと。

/etc/group

```
couchdb:x:114:
```

/etc/passwd

```
couchdb:x:114:114::/opt/couchdb1.2.0:/bin/sh
```

/etc/shadow

```
couchdb:*:15680:0:99999:7:::
```

以下、実行したコマンドです。 `/opt/coucdb1.2.0` にインストールしたのは後で消しやすいようにということです。

```
$ sudo apt-get install build-essential erlang libicu-dev libmozjs-dev libcurl4-openssl-dev
$ sudo mkdir /opt/couchdb1.2.0
$ wget http://ftp.kddilabs.jp/infosystems/apache/couchdb/releases/1.2.0/apache-couchdb-1.2.0.tar.gz
$ tar xzvf apache-couchdb-1.2.0.tar.gz
$ cd apache-couchdb-1.2.0/
$ ./configure --prefix=`/opt/couchdb1.2.0
$ make && sudo make install
$ sudo chown -R couchdb.couchdb /opt/couchdb1.2.0/etc/couchdb/
$ sudo chown -R couchdb.couchdb /opt/couchdb1.2.0/var/lib/couchdb/
$ sudo chown -R couchdb.couchdb /opt/couchdb1.2.0/var/log/couchdb/
$ sudo chown -R couchdb.couchdb /opt/couchdb1.2.0/var/run/couchdb/`
```

管理者のユーザ名とパスワードをこのファイルに

```
$ sudo vi /opt/couchdb1.2.0/etc/couchdb/local.ini
```

こんな感じで書いておくと、

```
 ... ... ...
[admins]
admin = secret
```

初回起動時にパスワードを暗号化してくれるという妙な仕様になっています。だから /etc/couchdb の所有者を設定するのか、なるほど。セットアップが終わったら、起動して、ログ見て、トップページ ( と言うのかな？ ) を見てみます。

```
$ sudo /opt/``couchdb1.2.0``/etc/init.d/couchdb start
$ cat /opt/``couchdb1.2.0``/var/log/couchdb/couch.log
$ curl http://127.0.0.1:5984/`
```

こんなものも JSON で出力するこだわりがなんとも。基本的な使い方は [Getting Started](http://guide.couchdb.org/draft/tour.html) をご覧ください。

```
{"couchdb":"Welcome","version":"1.2.0"}
```

デフォルトでは 127.0.0.1 しか Listen していません。外からもアクセスしたい場合は

/opt/couchdb1.2.0/etc/couchdb/local.ini

```
bind_address = 0.0.0.0
```

とすればいいそうです ( [Why can't I access my CouchDB instance externally on Ubuntu 9.04 server?](http://serverfault.com/questions/79453/why-cant-i-access-my-couchdb-instance-externally-on-ubuntu-9-04-server) ) 。ただし、この後の "Test Suite" はどうも http://127.0.0.1:5984/ でないとうまくいかないようです。 http://localhost:5984/ でもだめというような記述もありました。そんなわけで Firefox を入れて `ssh -X` で外から起動して、管理ツール Futon を開いて "Test Suite" をやってみます。 "Test Suite" 実行中は Firefox が固まったようになってしまって不安なので、ログを表示しておきます。

```
$ sudo apt-get install firefox
$ firefox http://127.0.0.1:5984/_utils/ &
$ tail -f /opt/couchdb1.2.0/var/log/couchdb/couch.log`
```

Firefox で表示した Futon のページの右下の Login をクリックしてログインします。

ページの右側のメニュー "Verify Installation" を選択して "Verify Your Installation" を実行します。正常にインストールできていれば "√ Your installation looks fine. Time to Relax." となります。

ページの右側のメニュー "Test Suite" を選択して "Run All" を実行します。すると、 「このテストは Admin Party mode で実行するから "Remove Admins" をクリックしてね（抄訳）」とのたまうのでしょうがないからその通りにします。するとターミナルの方ではびゅんびゅんとログが流れ始めて Futon の方も Status に "success", "success", "success"... と出始めて待つこと10分くらい、 "rev\_stemming" でエラーが出ました。メッセージ見てもわからないなあ。

> 追記: まっさらの OS にインストールしてやり直したら、すべて "success" になりました。

```
1. Assertion failed: db.open("bar", {revs:true})._revisions.ids.length == newLimit + 1
2. Assertion failed: docB2._conflicts[0] == docB1._rev) // We having already updated bar before setting the limit, so it's still got // a long rev history. compact to stem the revs. T(db.open("bar", {revs:true})._revisions.ids.length == newLimit + 1
```

上の方にある "Share Test Reports" を押して報告しておきました。

ページの右側のメニュー "Overview" を選択します。するとテスト用のデータベースがたくさん残っています。掃除しておこうかな。。。

まず、データベースの一覧を取得します。

```
$ curl -X GET http://127.0.0.1:5984/_all_dbs
```

JSON 形式で出てきます。実物は１行ですが、見やすいように改行入れます。

```
[
    "_replicator",
    "_users",
    "test_suite_db",
    "test_suite_db/with_slashes",
    "test_suite_db_a",
    "test_suite_db_b",
    "test_suite_db_c",
    "test_suite_foobar",
    "test_suite_reports"
]
```

削除します。データベースの名称の `"/"` は `"%2F"` に置き換えるといいようです。

```
$ curl -X DELETE http://admin:password@127.0.0.1:5984/test_suite_db
$ curl -X DELETE http://`admin:password@127.0.0.1:5984/test\_suite\_db%2Fwith\_slashes
$ curl -X DELETE http://`admin:password@127.0.0.1:5984/test\_suite\_db\_a
$ curl -X DELETE http://`admin:password@127.0.0.1:5984/test\_suite\_db\_b
$ curl -X DELETE http://`admin:password@127.0.0.1:5984/test\_suite\_db\_c
$ curl -X DELETE http://`admin:password@127.0.0.1:5984/test\_suite\_foobar
$ curl -X DELETE http://`admin:password@127.0.0.1:5984/test\_suite\_reports
```

正常に処理すると `{"ok":true}` と出力されます。

最後に、couchdb を停止して、管理者のユーザ名とパスワードを設定し直して、再起動して終わりです。
