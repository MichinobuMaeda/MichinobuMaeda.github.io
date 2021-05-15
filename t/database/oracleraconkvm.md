KVM で Oracle 10g RAC
=====

Update: 2009-12-23



以前作成した Oracle VM の環境をつぶして、 KVM を使った Oracle 10g RAC のお勉強用の環境を作ってみることにしました。なぜ KVM なのか？ それは、使ってみたかったからです。

## Host に Fedora 12 をインストール

マシンスペックは



- CPU: AMD Athlon™ 64 X2 Dual Core Processor 5200+
- RAM: 4GB
- HDD: SATA のものを数本



です。



Host OS には KVM や関連するツールの新しいバージョンが入っていそうな Fedora 12 を使うことにしました。デスクトップはほとんど使わず、リモートから（といっても同じ部屋の中ですが） MacBook でアクセスする予定です。したがって、インストールパッケージのセットは “Server” を基本に、ゲームなどのいらないものを消して、 “Virtualization” のパッケージを追加しただけの単純な構成にしました。

## Bridged network の追加

Guest OS を入れようと `virt-manager` を起動していろいろさわっていると、どうも、現状で Guest OS が使うことができるネットワークは NAT だけのようです。 Guest OS にも MacBook から ssh などでアクセスしたいので、 Bridged network を追加します。



Fedora のドキュメントにいいのがありました。 Fedora 12 の “Virtualization Guide” の [8.2. Bridged networking with libvirt](http://docs.fedoraproject.org/virtualization-guide/f12/en-US/html/sect-Virtualization_Guide-Network_Configuration-Bridged_networking_with_libvirt.html) に書いているとおりに設定します。 iptables のファイアウォールの設定が OS インストール完了時より甘くなってしまった気がするのですが、今回は深く考えないことにします。



以下、参考書も見ずに、いきなり `virt-manager` を使ってゲスト OS を入れてみます。

## Guest OS のインストール

Guest OS には RedHat EL や Oracle EL とほぼ同じ構成の CentOS を使います。 5.x だと RAW デバイス周りの設定手順などが Oracle 10g のドキュメントが前提としているものに比べて新しすぎるようなので、 4.8 にしました。で、早速、 MacBook から `“ssh -X -l root ホスト名”` で Host に接続して `virt-manager` を起動してインストールを始めたのですが、 Guest マシンに送られるキーがでたらめ……. `[R]` が `[Tab]` 、 `[*]` が `[Enter]` になっているところまでは解明しましたが、無理、 `root` のパスワードとか入れられない、ということで、あきらめて、 Host マシンのディスプレイで作業しました。



デフォルトの Storage Pool の場所が都合悪かったので新しい Storage Pool を追加しましたが、それ以外は virt-manager の指示の通り、 CentOS のインストーラの指示の通りです。



Guest のインストールが終わって起動したところで MacBook から接続をテストしましたが、問題なしです。 Oracle のインストールなどこの後の作業は Host の画面を使わなくてもできそうです。

## Guest の Clone

`virt-manager` から Guest の Clone ができます。たぶん GUI から入力させたパラメータをそのまま `virt-clone` に渡しているだけなんだろうと思います。新しい Guest とそのストレージファイルの名称が「 元の名前-clone 」になるので修正します。 NIC の MAC Address は自動で生成してくれます。



Clone が終わって新しい Guest を起動すると「 NIC が変わっている。古い方の設定を削除するか？新しい方の設定を追加するか？」と Guest の画面に出てきます。これは、先に述べた事情で MacBook からは操作困難なので Host の `virt-manager` から開いた Guest の画面で操作します。 Guest が無事起動したらその `/etc/sysconfig/network` の `hostname` を変更します。その後 Guest を再起動して、 IPアドレス、 Host名などが適切に設定されていること、その前に、そもそも正常に再起動できることを確認します。



Guest は合計 4個にしました。








| 項目 | 1   | 2   | 3   | 4   |
| --- | --- | --- | --- | --- |
| hostname    | centos4a              | centos4b                  | centos4c      | centos4d |
| IP Address  | 192.168.0.71          | 192.168.0.72              | 192.168.0.73  | 192.168.0.74 |
| RAM         | 1.5GB                 | 1.5GB                     | 1.5GB         | 1.5GB |
| Storage     | 20GB                  | 20GB                      | 20GB          | 20GB |
| Note        | 手をつけずにそのまま残す。 | RAC じゃない Oracle を入れる。 | RAC を入れる。  | RAC を入れる。 |





















## NAT の DHCP の設定の変更

RAC のインターコネクト用のネットワークとして、 Guest OS インストール時には使わなかった NAT が使えそうです。設定を見ると DHCP のリース範囲が `2 - 254` になっています。固定 IP Address も使いたいのでこれでは困ります。 `/etc/libvirt/qemu/networks/default.xml` にこの DHCP の設定が記述されいるようです。


```
 <dhcp>
 <range start="192.168.122.2" end="192.168.122.254" />
 </dhcp>
```


を


```
 <dhcp>
 <range start="192.168.122.224" end="192.168.122.254" />
 </dhcp>
```


と書き直して `/etc/init.d/libvirtd restart` したところ、期待どおりの設定になりました。

## Guest に NIC を追加する

Guest に NIC を追加するのは、 `virt-manager` から簡単にできますね。



Guest を起動すると、また起動時に「新しい NIC を設定するか？」画面が出てきます。これも、また、私の MacBook からはうまく操作できないので、 Host のディスプレイを使って設定しました。再起動完了後、 Guest 相互の導通を ping で確認します。次のような構成になりました。

| 項目 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| hostname    | centos4a              | centos4b                  | centos4c      | centos4d |
| IP Address  | 192.168.0.71          | 192.168.0.72              | 192.168.0.73 / 192.168.122.73  | 192.168.0.74 / 192.168.122.74 |
| RAM         | 1.5GB                 | 1.5GB                     | 1.5GB         | 1.5GB |
| Storage     | 20GB                  | 20GB                      | 20GB          | 20GB |
| Note        | 手をつけずにそのまま残す。 | RAC じゃない Oracle を入れる。 | RAC を入れる。  | RAC を入れる。 |




## Guest に共有ストレージを追加する

Guest に共有するストレージとして 1GB 3個と 10GB 2個を作成します。 `allocation` の値はめいっぱいにしておきます（なんとなく）。 OracleVM と違って、「共有付加」「共有可」のようなパラメータが見あたらないので、本当に共有できるかどうか不安です。まず、試しに、1GB のものを 1個、片方の Guest に追加します。 I/F はデフォルトの IDE ではなく SCSI としました（なんとなく）。この Guest をシャットダウンしてディスクを追加して、起動した後、正常にそのデバイスを認識していることを確認します。


```
[root@centos4c ~]# fdisk -l

Disk /dev/hda: 20.9 GB, 20971520000 bytes
255 heads, 63 sectors/track, 2549 cylinders
Units = シリンダ数 of 16065 * 512 = 8225280 bytes

デバイス Boot      Start         End      Blocks   Id  System
/dev/hda1   *           1          13      104391   83  Linux
/dev/hda2              14        2549    20370420   8e  Linux LVM

Disk /dev/sda: 1073 MB, 1073741824 bytes
34 heads, 61 sectors/track, 1011 cylinders
Units = シリンダ数 of 2074 * 512 = 1061888 bytes

ディスク /dev/sda は正常な領域テーブルを含んでいません
```


`virt-manager` でもう一方の Guest に追加します。「別のゲストが使っているぞ、本当に追加するか？」との警告が出ますが、無視して追加します。で、起動して、つまり、両方の Guest が起動している状態で、両方の Guest で上記の確認をすると、どちらも認識しています。試しに、片方の Guest を再起動して確認、またもう片方を再起動して確認、としてみましたが、ディスクの認識についての問題は出ませんでした。

## RAW デバイスを設定する

まずは `fdisk` で 256MB のパーティションを 2個作成します。詳しくは「Oracle Database 2日でReal Application Clustersガイド」「2 クラスタの準備」「RAW記憶域デバイスとRAWパーティションの構成」を見てください。片方の Guest でパーティションを作成して、もう片方の Guest で見てみると、作成した結果が認識できています。


```
[root@centos4c ~]# fdisk -l

Disk /dev/hda: 20.9 GB, 20971520000 bytes
255 heads, 63 sectors/track, 2549 cylinders
Units = シリンダ数 of 16065 * 512 = 8225280 bytes

デバイス Boot      Start         End      Blocks   Id  System
/dev/hda1   *           1          13      104391   83  Linux
/dev/hda2              14        2549    20370420   8e  Linux LVM

Disk /dev/sda: 1073 MB, 1073741824 bytes
34 heads, 61 sectors/track, 1011 cylinders
Units = シリンダ数 of 2074 * 512 = 1061888 bytes

デバイス Boot      Start         End      Blocks   Id  System
/dev/sda1               1         242      250923+  83  Linux
/dev/sda2             243         484      250954   83  Linux
```


ガイドの残りの手順をやってみましたが、 RAW デバイスの認識も問題ないようです。お勉強用の環境としては使えるものになったのかなぁ？



残りのディスクも追加します。同じディスクが異なるデバイス名になるのはいやなので、一つずつ確認しながら追加します。

## OS の設定

「Oracle Database インストレーション・ガイド 10gリリース2（10.2）for Linux x86」の「2 インストール前の作業」の手順で、 OS ユーザ・グループの作成、 ORACLE\_BASE ディレクトリの作成、カーネルパラメータの調整などします。 RAC ではない Oracle を入れる予定の Guest も併せて同じ内容を設定します。



再起動して、カーネルパラメータを再確認したら、予行演習として RAC ではない Oracle を入れる予定の Guest に Database software をインストールしてみます。インストーラを起動したら化け化けです。とりあえず LANG=C で英語表示にして回避します。このインストールについては特に問題なさそうです。



横道にそれますが、これらの 3個の Guest をすべて起動すると Host のメモリが足りなくなります。 Guest のメモリは 1.5GB から 1.2GB に減らすことにしました。



次に「Oracle Database 2日でReal Application Clustersガイド 10g リリース2（10.2）」「2 クラスタの準備」の手順で ssh などの設定をします。で、念のため OS を再起動してみて気がついたのですが、 raw パーティションの所有者が `root` に戻っています。 `/etc/udev/permissions.d/50-udev.permissions` というファイルが既に存在するのですが、 `/etc/udev/permissions.d/oracle.permissions` を `/etc/udev/permissions.d/49-oracle.permissions` にリネームして OS を再起動してみるとうまくいきました。



追加でインストールが必要だったパッケージは libaio だけでした。

## ソフトウェアとインスタンスのインストール

「Oracle Database 2日でReal Application Clustersガイド 10g リリース2（10.2）」の手順で Database のインストールまでやってみます。私の不注意で ASM 用の ORACLE\_HOME が `/u01/app/oracle/oracle/product/10.2.0/asm` ( “oracle” が二回出てくる) になったこと以外、特に問題ありませんでした。このスペックのマシンだと、あまり待たされずに作業できます。



この環境で引き続き dbca を使った手順など試してみたいので、最後に ASM と Listner と Database を削除します。 srvctl で ASM と Database を停止して、削除して、 Listner も停止して、各ノードで `crs_unregister` を使って Lisner を削除しました。これらのツールの使い方は「Oracle Database Oracle ClusterwareおよびOracle Real Application Clusters管理およびデプロイメント・ガイド 10g リリース2（10.2）」の「B 高可用性Oracle Clusterwareのコマンドライン・リファレンスおよびC API」と「E サーバー制御ユーティリティのリファレンス」に出ています。



ここまで確認できた Guest の環境は、 VM のイメージ丸ごとバックアップしておくことにします。



以上、終わり。
