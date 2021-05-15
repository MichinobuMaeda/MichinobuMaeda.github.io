Oracle のロールバック表領域でブロックに障害が出たら
=====

Update: 2011-05-16

★ Undo を使っていない古いバージョンのお話です ★



Oracle のデータ・ブロック障害の対処方法について、それが普通の表領域ではなくてロールバック表領域の場合の手順をまとめたものはあまり見かけないので、ざっと書いてみました。新しいシステムでは、ロールバックセグメントではなく UNDOセグメントを使っていると思いますが、その場合はこれとは手順が異なります。RAC ( Real Application Clusters ) を使っている場合も手順が異なりますが、その規模のシステムなら専任のDBAさんがいますね。


```
ORA-01578 ファイル番号 string, ブロック番号 string でOracle データ・ブロックに障害が発生しました。
```


というようなエラーが出てそれがロールバックセグメントだった場合の応急処置は次のような感じです。Oracle のバージョンによってデータディクショナリの定義が違うことがありますが、だいたいこれでだいじょうぶでしょう。



エラーリファレンスに書いてあるとおり次のコマンドでセグメント名を求めます。


```
SELECT SEGMENT_TYPE,OWNER||'.'||SEGMENT_NAME FROM DBA_EXTENTS
WHERE ファイル番号 = FILE_ID AND ブロック番号 BETWEEN BLOCK_ID AND BLOCK_ID+BLOCKS -1;
```


ロールバックセグメントだとわかっている場合は次のようにセグメント名だけでもいいです。


```
SELECT SEGMENT_NAME FROM DBA_EXTENTS
WHERE ファイル番号 = FILE_ID AND ブロック番号 BETWEEN BLOCK_ID AND BLOCK_ID+BLOCKS -1;
```


ロールバックセグメントは普通複数あるので、とりあえずエラーが出たセグメントをオフラインにします。そのセグメントを今使っているトランザクションがなければすぐオフラインになります。


```
ALTER ROLLBACK SEGMENT セグメント名 OFFLINE;
```


この処理の結果は次のSQLで確認できます。


```
SELECT SEGMENT_NAME, STATUS FROM DBA_ROLLBACK_SEGS;
```


セグメントが減って、ロールバック領域の不足が少し心配になるので、次のSQL文ですべてのロールバックセグメントのサイズを最適化します。一部のセグメントがどーんと大きな領域を占有している場合、それを開放してくれます。


```
ALTER ROLLBACK SEGMENT セグメント名 SHRINK;
```


で、根本解決ですが、失敗するとOracleが動かなくなってしまうので、テスト環境で試してからにしましょう。



エラーになったファイルは捨てて、新しいファイルに乗り換えたいですね。まず、表領域名を調べます。


```
SELECT TABLESPACE_NAME FROM DBA_DATA_FILES
WHERE FILE_ID = ファイル番号;
```


次にファイルの設定を調べます。


```
SELECT FILE_NAME, FILE_ID, BYTES/1024,
AUTOEXTENSIBLE, MAXBYTES/1024, INCREMENT_BY
FROM DBA_DATA_FILES WHERE TABLESPACE_NAME = 表領域名;
```


これで、ファイル名、ファイル番号、サイズ(KB)、自動拡張の有無、自動拡張Onの場合の最大サイズ(KB)、自動拡張Onの場合の増分ブロック数が取得できます。



増分はサイズではなくブロック数しか取得できません。ブロックサイズ 4KB の場合 ブロック数×4 (KB) となります。



同じサイズの表領域を作成するには、自動拡張Offの場合、


```
CREATE TABLESPACE 新しい表領域名
DATAFILE '新しいファイル名' SIZE サイズK
AUTOEXTEND OFF;
```


自動拡張Onの場合、


```
CREATE TABLESPACE 新しい表領域名
DATAFILE '新しいファイル名' SIZE サイズK
AUTOEXTEND ON NEXT 増分K MAXSIZE 最大サイズK;
```


このSQLを実行する前にディスクの空き容量が十分あるか確認してください。



次に現状のロールバックセグメントの設定を調べます。


```
SELECT SEGMENT_NAME,
INITIAL_EXTENT/1024, NEXT_EXTENT/1024,
MIN_EXTENTS, MAX_EXTENTS, PCT_INCREASE
FROM DBA_ROLLBACK_SEGS WHERE TABLESPACE_NAME = 表領域名;
```

これで、各セグメントのセグメント名、初期サイズ(KB)、増分サイズ(KB)、最少エクステント数、最大エクステント数、増分の増加の割合(%)が取得できます。で、ここで一つ問題が… 最適サイズが取得できません。上記の `"ALTER ROLLBACK SEGMENT セグメント名 SHRINK;"` の後の実サイズを取得することにします。


```
SELECT SEGMENT_NAME, BYTES/1024
FROM DBA_SEGMENTS WHERE TABLESPACE_NAME = 表領域名;
```


で、新しい表領域に、現状と同じ数・設定の新しいロールバックセグメントを作ります。


```
CREATE ROLLBACK SEGMENT 新しいセグメント名
TABLESPACE 新しい表領域名
STORAGE (INITIAL 初期サイズK NEXT 増分サイズK
MINEXTENTS 最少エクステント数 MAXEXTENTS 最大エクステント数
PCTINCREASE 増分の増加の割合 OPTIMAL 最適サイズK);
```


新しい方のロールバックセグメントを使うように切り替えるには、初期設定ファイル `init<SID>.ora` の `ROLLBACK_SEGMENTS` の値を変更して再起動するわけですが、再起動無しでできないかな…
