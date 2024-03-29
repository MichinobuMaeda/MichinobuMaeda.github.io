# インデックスの有無と INSERT の所要時間 ( MySQL )

Update: 2013-02-06

昔、仕事で Oracle の INSERT の所要時間をインデックスの有り無しで比べてみたことがありました。かなりはっきり出ます。  MySQL でも同じように差が出るはずだと思うのですが、具体的にどんな値になるのか知りたくて試してみました。



マシンは MacBook Pro でディスクは 5,400 rpm です。遅いです。遅い方が結果がはっきり出ていいのです、ということにしておきます。



インデックス無し

```
CREATE TABLE t1 (
 pk INT
, c1 INT
, c2 INT
, c3 INT
, c4 CHAR(10)
, c5 CHAR(10)
, c6 VARCHAR(2000)
, PRIMARY KEY ( pk )
);
```

インデックス有り

```
CREATE TABLE t2 (
 pk INT
, c1 INT
, c2 INT
, c3 INT
, c4 CHAR(10)
, c5 CHAR(10)
, c6 VARCHAR(2000)
, PRIMARY KEY ( pk )
, INDEX ( c2 )
, INDEX ( c4 )
);
```

これらのテーブルに 1,000,000行ずつ INSERT して時間を計りました。以下のようなデータです。 c6 列は 1,000 文字です。まともに 1,000,000回 INSET すると時間がかかりそうなので、 15,625回 1行ずつ INSET した後、 INSERT...SELECT... を 5回繰り返して 64倍にしました。


```
+----+------+------+------+------------+------------+----------------
| pk | c1   | c2   | c3   | c4         | c5         | c6
+----+------+------+------+------------+------------+----------------
|  0 | NULL | NULL | NULL | 0123456789 | 0123456789 | 012345678901...
|  1 |    1 |    1 |    1 | 1234567890 | 1234567890 | 012345678901...
|  2 |    2 |    2 |    2 | 2345678901 | 2345678901 | 012345678901...
|  3 |    3 |    3 |    3 | 3456789012 | 3456789012 | 012345678901...
|  4 |    4 |    4 |    4 | 4567890123 | 4567890123 | 012345678901...
|  5 |    5 |    5 |    5 | 5678901234 | 5678901234 | 012345678901...
|  6 |    6 |    6 |    6 | 6789012345 | 6789012345 | 012345678901...
|  7 |    7 |    7 |    7 | 7890123456 | 7890123456 | 012345678901...
|  8 |    8 |    8 |    8 | 8901234567 | 8901234567 | 012345678901...
|  9 |    9 |    9 |    9 | 9012345678 | 9012345678 | 012345678901...
| 10 |   10 | NULL | NULL | 0123456789 | 0123456789 | 012345678901...
| 11 |   11 |    1 |    1 | 1234567890 | 1234567890 | 012345678901...
| 12 |   12 |    2 |    2 | 2345678901 | 2345678901 | 012345678901...
| 13 |   13 |    3 |    3 | 3456789012 | 3456789012 | 012345678901...
| 14 |   14 |    4 |    4 | 4567890123 | 4567890123 | 012345678901...
...
```

交互にそれぞれ 4回繰り返した結果は以下の通りです。


```
インデックス   無し      有り
--------+----------+-----------
             89 秒      140 秒
             78 秒      144 秒
            105 秒      137 秒
             86 秒      136 秒
--------+----------+-----------
 平均       89.5 秒   139.25 秒
```

インデックス無しに比べてインデックス有りは 156% かかるという結果になりました。


インデックスが付いているカラムの値を UPDATE する場合についても気が向いたら計ってみたいと思いますが、 DELETE して INSERT するくらいの影響だろうと思います。B-Tree の操作の詳しいことはわかりませんが、昔、 Oracle 使って計測したときはそんな感じの値でした。



> 以下、あまりこのような数字を見たことがない人のために念のための追加の説明です。



Web を含む OLTP 系のアプリケーションの場合、この結果から「インデックスを付けると遅くなる」という一般論を導き出すのはとんでもない間違いです。 INSERT は他の処理に比べて早くて、私の遅い MacBook Pro でも上記の結果を 1,000,000 で割ると 1行あたり 0.1ミリ秒くらいにしかなりません。その 56% ということなのですが、上記の例ではインデックスを 2個追加していますから、単純に割ってインデックス 1個あたり 0.025 ミリ秒にしかなりません。



インデックスが効いていなくて性能が落ちている SELECT, UPDATE, DELETE は、小さな場合でも 0.01秒、つまり 10ミリ秒くらいは損してますよね？ それどころか、100ミリ秒とか秒の単位の時間になってしまうこともありますよね？ そのような時間に比べて 0.025 ミリ秒というのは存在しないも同然の値です。



バッチ処理等で大量の INSERT をする場合は、インデックスを無効にしておいて処理が終わった後でインデックスを再生成するなど、それぞれの製品に合った回避手段があるだろうと思います。とはいえ、私の遅い MacBook Pro の 1,000,000 行で 100秒前後しかかかっていませんから、本当に心配する必要が出てくるのは 10,000,000行くらいからではないかと思います。
