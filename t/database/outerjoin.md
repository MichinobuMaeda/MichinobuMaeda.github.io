外部結合の結果をイメージするのは難しい
=====

Update: 2013-05-08



今、私が基盤の担当として関わっているシステムでは、外部結合 ( Outer Join ) を使った SQL を多用しています。でも、それらの内容をよく見ると、外部結合を使わなくていいものがあるような。。。最近は Java でも Rails でも ORM ( Object-relational Mapping ) が当たり前のように使われています。若いエンジニアさんたちは SQL を直接扱うことが少なくなりました。でも RDB の側は SQL で処理しています。ですから基本的なことは理解しておいてもらった方がいいだろうと考えて、以下のようのなクイズを作ってみました。難しいだろうと思うのですが、実際にシステムの中で使われている SQL に比べればずいぶん単純なものです。



問題：a. 〜 z. の `SELECT`文について、同じ結果を返す組み合わせをすべて挙げてください。 `ORDER BY` を付けていないのですが、結果の行の順番は考慮しなくてかまいません。

テーブルの定義：

```
CREATE TABLE T1 (PK INT NOT NULL, C1 INT, PRIMARY KEY (PK));
CREATE TABLE T2 (PK INT NOT NULL, C2 INT, PRIMARY KEY (PK));
```

SELECT文：

```
a. SELECT C1, C2 FROM T1 NATURAL JOIN     T2;
b. SELECT C1, C2 FROM T1 JOIN             T2 ON T1.PK = T2.PK;
c. SELECT C1, C2 FROM T1 INNER JOIN       T2 ON T1.PK = T2.PK;
d. SELECT C1, C2 FROM T1 LEFT JOIN        T2 ON T1.PK = T2.PK;
e. SELECT C1, C2 FROM T1 RIGHT JOIN       T2 ON T1.PK = T2.PK;
f. SELECT C1, C2 FROM T1 FULL JOIN        T2 ON T1.PK = T2.PK;
g. SELECT C1, C2 FROM T1 LEFT OUTER JOIN  T2 ON T1.PK = T2.PK;
h. SELECT C1, C2 FROM T1 RIGHT OUTER JOIN T2 ON T1.PK = T2.PK;
i. SELECT C1, C2 FROM T1 FULL OUTER JOIN  T2 ON T1.PK = T2.PK;
j. SELECT C1, C2 FROM T2 NATURAL JOIN     T1;
k. SELECT C1, C2 FROM T2 JOIN T1 ON       T1.PK = T2.PK;
l. SELECT C1, C2 FROM T2 INNER JOIN       T1 ON T1.PK = T2.PK;
m. SELECT C1, C2 FROM T2 LEFT JOIN        T1 ON T1.PK = T2.PK;
n. SELECT C1, C2 FROM T2 RIGHT JOIN       T1 ON T1.PK = T2.PK;
o. SELECT C1, C2 FROM T2 FULL JOIN        T1 ON T1.PK = T2.PK;
p. SELECT C1, C2 FROM T2 LEFT OUTER JOIN  T1 ON T1.PK = T2.PK;
q. SELECT C1, C2 FROM T2 RIGHT OUTER JOIN T1 ON T1.PK = T2.PK;
r. SELECT C1, C2 FROM T2 FULL OUTER JOIN  T1 ON T1.PK = T2.PK;
s. SELECT C1, C2 FROM T1 INNER JOIN       T2 ON T1.PK = T2.PK WHERE C2 = 1;
t. SELECT C1, C2 FROM T1 LEFT JOIN        T2 ON T1.PK = T2.PK WHERE C2 = 1;
u. SELECT C1, C2 FROM T1 RIGHT JOIN       T2 ON T1.PK = T2.PK WHERE C2 = 1;
v. SELECT C1, C2 FROM T1 FULL JOIN        T2 ON T1.PK = T2.PK WHERE C2 = 1;
w. SELECT C1, C2 FROM T1 INNER JOIN       T2 ON T1.PK = T2.PK WHERE C2 IS NULL;
x. SELECT C1, C2 FROM T1 LEFT JOIN        T2 ON T1.PK = T2.PK WHERE C2 IS NULL;
y. SELECT C1, C2 FROM T1 RIGHT JOIN       T2 ON T1.PK = T2.PK WHERE C2 IS NULL;
z. SELECT C1, C2 FROM T1 FULL JOIN        T2 ON T1.PK = T2.PK WHERE C2 IS NULL;
```

回答としてありうる組み合わせは天文学的な数になるので、適当に選んで正解になった人は、人生の残りの運をすべて使い果たすことになります。「データによって違う」と思った人は、正しいですが、情報処理試験のDBになかなか合格できないタイプです。

> 追記: 「天文学的」は間違い。そんなに多くない。でも、人生の残りの運を使い果たすには十分。

具体例で考えたい場合は、どのようなデータがあり得るか自分で考えてください。とはいえ、考え方のポイントを理解していないと、条件を網羅するデータをつくることはできないと思います。実際に RDB 上で動かしてみてもかまいませんが、世の中の RDB 製品は必ずしも SQL の規格を満たしていません。例えば、今、みなさんが使っている MySQL は `FULL` をサポートしていません。私はつい先ほど知りました。 PostgreSQL は基本的に規格通りにつくっているそうです。

まず、最初の `NATURAL JOIN` は、見たことない人が多いと思います。 SQL の理論と規格を作った人たちは、これこそが自然な結合の形であると考えたようなのですが、なぜか実務で使われることが少ないです。 Rails の場合も `ActiveRecord` の命名の方式との関係でうまく使えません。そのような次第で `NATURAL JOIN` についての説明は省略するので詳細についてはぐぐってください。

次に `INNER JOIN` と `JOIN` ですが、これらは同じものです。 `JOIN` は `INNER` を省略した表現です。 `ON` の右側に書いた条件に合う行を結合します。


```
T1         T2
----+----  ----+----
 C1 | C2    C3 | C4
----+----  ----+----
  1 | A      1 | X
  2 | B      3 | Y
  3 | C      4 | Z

SELECT C1, C2, C3, C4 FROM T1 INNER JOIN T2 ON T1.C1 = T2.C3;
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  1 | A  |  1 | X
  3 | C  |  3 | Y
```


`LEFT OUTER JOIN` と `LEFT JOIN` は同じものです。 `LEFT JOIN` は `OUTER` を省略した表現です。 `LEFT OUTER JOIN` の右側のテーブルに条件に合う行が無くても、左側のテーブルの行だけ返します。


```
T1         T2
----+----  ----+----
 C1 | C2    C3 | C4
----+----  ----+----
  1 | A      1 | X
  2 | B      3 | Y
  3 | C      4 | Z

SELECT C1, C2, C3, C4 FROM T1 LEFT OUTER JOIN T2 ON T1.C1 = T2.C3;
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  1 | A  |  1 | X
  2 | B  |NULL|NULL
  3 | C  |  3 | Y
```


`RIGHT OUTER JOIN` と "RIGHT JOIN" は同じものです。 `RIGHT JOIN` は `OUTER` を省略した表現です。 "RIGHT OUTER JOIN" の左側のテーブルに条件に合う行が無くても、右側のテーブルの行だけ返します。

```
T1         T2
----+----  ----+----
 C1 | C2    C3 | C4
----+----  ----+----
  1 | A      1 | X
  2 | B      3 | Y
  3 | C      4 | Z

SELECT C1, C2, C3, C4 FROM T1 RIGHT OUTER JOIN T2 ON T1.C1 = T2.C3;
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  1 | A  |  1 | X
  3 | C  |  3 | Y
NULL|NULL|  4 | Z
```

`RIGHT OUTER JOIN` の上記の例の `T1` と `T2` を入れ替えた場合、 `LEFT OUTER JOIN` と同じ結果になります。

```
T1         T2
----+----  ----+----
 C1 | C2    C3 | C4
----+----  ----+----
  1 | A      1 | X
  2 | B      3 | Y
  3 | C      4 | Z

SELECT C1, C2, C3, C4 FROM T2 RIGHT OUTER JOIN T1 ON T1.C1 = T2.C3;
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  1 | A  |  1 | X
  2 | B  |NULL|NULL
  3 | C  |  3 | Y
```

`FULL OUTER JOIN` と "FULL JOIN" は同じものです。 "FULL JOIN" は "OUTER" を省略した表現です。 "FULL OUTER JOIN" の左右のどちらかのテーブルに行があれば、とにかく全部返します。

```
T1         T2
----+----  ----+----
 C1 | C2    C3 | C4
----+----  ----+----
  1 | A      1 | X
  2 | B      3 | Y
  3 | C      4 | Z

SELECT C1, C2, C3, C4 FROM T1 FULL OUTER JOIN T2 ON T1.C1 = T2.C3;
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  1 | A  |  1 | X
  2 | B  |NULL|NULL
  3 | C  |  3 | Y
NULL|NULL|  4 | Z
```

では、以下のような

1.  結合に使う列 `(` `C1``,` `C3 )`の値が他方のテーブルに存在する / 存在しない。
2.  絞り込み条件に使う列 `(` `C4` `)`の値が `NULL` でない / NULL である。

という条件を網羅するデータを `JOIN` して `WHERE` 条件で絞り込んだ結果について考えてみることにします。考える上で面倒なのは、外部結合した場合、もとのテーブルに該当する行がない場合も、該当する行があって値が `NULL` の場合も、結合した結果は `NULL` になるということです。

```
T1         T2
----+----  ----+----
 C1 | C2    C3 | C4
----+----  ----+----
  1 | A      1 | X
  2 | A      2 |NULL
  3 | A      4 | X
             5 |NULL
```

`"FULL OUTER JOIN"` の場合、 `WHERE` 条件無しなら次のようになります。

```
SELECT C1, C2, C3, C4 FROM T1 FULL OUTER JOIN T2 ON T1.C1 = T2.C3;
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  1 | A  |  1 | X
  2 | A  |  2 |NULL
  3 | A  |NULL|NULL
NULL|NULL|  4 | X
NULL|NULL|  5 |NULL
```

`WHERE C4 = 'X'` を追加すると次のようになります。

```
SELECT C1, C2, C3, C4 FROM T1 FULL OUTER JOIN T2 ON T1.C1 = T2.C3 WHERE C4 = 'X';
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  1 | A  |  1 | X
NULL|NULL|  4 | X
```

上の例の `FULL OUTER JOIN` を `INNER JOIN` / `LEFT OUTER JOIN` / `RIGHT OUTER JOIN` に置き換えるとどうなるかについても考えてみてください。

`WHERE C4 IS NULL` なら次のようになります。

```
SELECT C1, C2, C3, C4 FROM T1 FULL OUTER JOIN T2 ON T1.C1 = T2.C3 WHERE C4 IS NULL;
----+----+----+----
 C1 | C2 | C3 | C4
----+----+----+----
  2 | A  |  2 |NULL
  3 | A  |NULL|NULL
NULL|NULL|  5 |NULL
```

上の例の `FULL OUTER JOIN` を `INNER JOIN` / `LEFT OUTER JOIN` / `RIGHT OUTER JOIN` に置き換えるとどうなるかについても考えてみてください。

さて、このあたりで外部結合のことは嫌いになっていただけたでしょうか？
