RAID規格の概要
=====

Update: 2009-03-27



私が所属する組合 ( [コンピュータ・ユニオン](http://www.union-net.or.jp/densanro/) ) のミーティングで RAID についての話になったのですが、私が覚えているのと違う定義があるようです。パリティが１個のディスクに書き込まれるのは私の記憶だと RAID 3 、別の人が言うにはそれは RAID 2 だとのことでした。よく使われる 0, 1, 5 で認識のずれがなければ困ることはないのですが、気になって調べてみました。私が覚えていたつもりの RAID 2, 4 のことなどもうすっかり忘れていましたし。



もともと RAID は厳格ではない規格です。世の中の製品のバラエティが増えるにつれて RAID 0 などが追加されてきました。４、５年以上前なら「 正式な RAID の Level は 1 〜 5 だけ」みたいな記述も見られましたが、今ではそんな堅いことを言う人はいません。

## RAID は何の略？

もともとは Redundant Array of Inexpensive Disks の略でした。でも、 “Inexpensive” の印象がよくないということで Redundant Array of Independent Disks の略とされることが多くなっています。

## 歴史的文書から

Wikipedia の [RAID](http://en.wikipedia.org/wiki/Redundant_array_of_independent_disks) の参照文献 [1 A Case for Redundant Arrays of Inexpensive Disks (RAID)](http://www.cs.cmu.edu/~garth/RAIDpaper/Patterson88.pdf) ( David A. Patterson, Garth A. Gibson and Randy Katz ) ではこうなっています。

- First Level RAID: Mirrored Disk
- Second Level RAID: Hamming Code For ECC
- Third Level RAID: Single Check Disk Per Group
- Fourth Level RAID: Independent Reads/Writes
- Fifth Level RAID: No Single Check Disk


私が覚えていた 1, 3, 5 はこの定義です。ただし、今までよくわかっていなかった RAID 4 の意味がわかりました。RAID 3, 4, 5 の順番に並んでいる理由がわかりました。bit 単位でデータを取り扱う RAID 3 に対してRAID 4 はセクタ単位になり、詳細は省略して（論文を全文翻訳することになりそうなので）その結果、 Independent Reads/Writes になります。で、そのセクタ単位のチェック情報を１個のディスクに集中させずに全ディスクに分散させたのが RAID 5 なのだそうです。



で、 Wikipedia の記事に戻ると、 RAID 3 は “dedicated parity or bit interleaved parity or byte level parity” で RAID 4 は “Block level parity” となっていて、なんか微妙に違うなぁ。 MSDN の RAID Levels and SQL Server でも RAID 3 に対して RAID 4 は “striped data in much larger blocks or segments” を使うと記されています。 1987年に上記の論文が発表された後、いろいろな製品が出てきたということでしょう。

## その他のレベル、ベンダによる定義

Wikipedia のこの記事で挙げられているその他の Level には次のようなものがあります。



- RAID 0: striped disks : パリティ無しです。
- RAID 6: striped disks with dual parity : 2個のディスクの故障まで耐えられます。
- RAID 10 (or 1+0): uses both striping and mirroring : ミラー構成セットを使ってストライピングする 1+0 と、ストライピングセットをミラー構成にする 0+1 に区分することがあります。
- RAID 53: Merges the features of RAID level 0 and RAID level 3



MSDN の [RAID Levels and SQL Server](http://msdn.microsoft.com/en-us/library/ms190764.aspx) に Level 10 (1+0) についても記されているのですが、ストライピングセットをミラー構成にしたものだそうで、 Wikipedia の説明では 0+1 とされているものになります。



EMC の [EMC CLARiXの高可用性（HA）構成のベストプラクティス](http://japan.emc.com/microsites/japan/techcommunity/pra/bpi/clarix-ha-2.htm) には RAID 0, 1, 1/0, 3, 5, 6 について簡単に説明しています。1/0 が Wikipedia の説明の 0+1 なのか 1+0 なのかはわかりません。この記事は全体としてわかりやすくていいですね。



日立の [RAID](http://www.hitachi.co.jp/products/it/storage-solutions/techsupport/basicknowledge/raid.html) にも RAID 0, 1, 0+1, 3, 5, 6 についての簡単な説明が掲載されています。ここに掲載されている RAID 0+1 は、図を見る限り Wikipedia RAID の 0+1 と同じです。



HP の [RAID 6 with HP Advanced Data Guarding technology: a cost-effective, fault-tolerant solution](http://h50146.www5.hp.com/products/storage/whitepaper/pdfs/c00386950.pdf) には RAID 0, 1, 1+0, 5, 6 についての説明が掲載されています。この RAID 1+0 は “implemented as a striped array of mirrored drives” ということで Wikipedia RAID の 1+0 と同じ、かな？



さらに Wikipedia の [Non-standard RAID levels](http://en.wikipedia.org/wiki/Non-standard_RAID_levels) には、1.5 とか 7 とかいろいろ載っています。

## RAID 1 は何個か？

ミーティングのとき「RAID 1 は普通２個だよね」「３個は効果が薄いという検討結果になったことがあった」「通常２個、あったとしても偶数個のはず」と話をしていたのですが、リンクをたどるとありました。奇数で構成できるミラーリング製品。 IBM 社が RAID 1E というのを出していて奇数個可、つまり、ディスクを１個ずつ追加可、なのだそうです。 Wikipedia の [Non-standard RAID levels](http://en.wikipedia.org/wiki/Non-standard_RAID_levels) の図 [RAID\_1E.png](http://en.wikipedia.org/wiki/File:RAID_1E.png) がわかりやすいのですが、奇数個でも 1/2台分の容量になります。で、普通は、つまり “E” が付かなければ偶数個ということになります。
