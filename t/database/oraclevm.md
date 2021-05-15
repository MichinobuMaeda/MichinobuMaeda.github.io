Oracle VM
=====

Update: 2009-07-17

## 自宅のPCにインストール


OTN Software Kit が時々送られてくるのですが（なぜなら高い金出して買ったから）その中に入っている Oracle VM が気になるわけですね。まずはインストールしてみることにします。

### ハードウェア

PCは2台使います。Oracle VM Server 用と Oracle VM Manager 用です。Oracle VM Server 用は AMD の 64bit のCPUと 4GB のメモリを積んでいます。 Oracle VM Manager 用は、古い ThinkPad にメモリ 2GB 積んだもので、Oracle VM Manager の推奨スペックに比べて CPU 能力が少々足りません。

### Oracle VM Server のインストール

ふつーの Linux のインストール手順とあまりかわりません。VM Agent のパスワードを入力する手順が追加になっているくらいでしょうか。詳しくは「Oracle VM Server インストレーション・ガイド リリース2.1.2 B51695-01」の「2 CD-ROM からのOracle VM Server のインストール」見てください。あっけないくらい簡単にできてしまいます。

ssh はデフォルトで有効になっていました。

### Oracle VM Manager のための OS のインストール

対応するOSについては「Oracle VM Manager インストレーション・ガイド リリース2.1.2 B51696-01」を見てください。私は OTN Software Kit に入っていた Enterprise Linux Release 5 Update 1 を使いました。こちらも、インストールの手順は、他の RedHat系ディストリビューションと同じです。

### Oracle VM Manager のインストール

CD 入れて、マウントして、`runInstaller.sh` を実行します。途中で「Oracle Database 10g Express Edition 入れるか？」というようなことを聞かれるので素直にそれに従います。あとは、パスワードの記入を何度か求められます。

### port を空ける

Oracle VM Manager のインストールの最中に次のように表示されます。これらのポートを空けてやる必要がありそうです。


```
Specify the HTTP port that will be used for Oracle Application Express [8080]:
Specify a port that will be used for the database listener [1521]:`
  ...
To access the Oracle VM Manager home page go to:
 http://carbon.home.michinobu.jp:8888/OVS`
To access the Oracle VM Manager help page go to:
 http://carbon.home.michinobu.jp:8888/help/help
```



`“carbon.home.michinobu.jp”` というのは Oracle VM Manager をインストールしたPCのホスト名です。GUI画面のメニュー「システム」「管理」「セキュリティレベルとファイヤーウォールの設定」を選択して、「その他のポート」に追加します。



他のPCから（はい、これで、私のPCは何台目でしょう？） `http://carbon.home.michinobu.jp:8080/` と `http://carbon.home.michinobu.jp:8888/OVS` を表示してみます。また、 ssh でログインしてみます。いずれも OK でした、これでリモートから作業できます（全部部屋の中だけど）。



Oracle VM Manager は、ユーザ admin とインストール時に設定したパスワードでログインできます。

### 補足

「Oracle VM Managerインストレーション・ガイド リリース2.1.2 B51696-01」を見ながら、少し追加の作業です。



*   ポート 8889 を空けました。何に使うんだろう？
*   TightVNC-Javaアプレットをインストールしました。

## テンプレートを使ってみる

2009-07-20



実際に VM を作ってみます。 VM のテンプレートを使う一番簡単な方法を試してみました。



以下、参照したドキュメントはすべて「Oracle VM Managerユーザーズ・ガイド リリース2.1.2 部品番号: B51698-01」です。

### 作業環境

私が作業した環境は次のようになります。 Oracle VM Server をインストールしたマシンにも、 Oracle VM Manager をインストールしたマシンにも、直接手を触れることはありません。 MacBook から、Webブラウザや ssh を通して操作しました。



```
---------
Oracle VM
 Server
---------
    |
---------
Oracle VM
 Manager
---------
    |
---------
 MacBook
---------
````


### サーバー・プールの作成

「3.2 サーバー・プールの作成」の手順に従って、最初でたぶん最後のサーバー・プールを作成します。マシンの台数の制約により、必然的に All-in-One構成の HA 無しになります。

### テンプレートのインポート

「5.1 仮想マシン・テンプレートのインポート」の案内に従ってテンプレートを入手してインポートします。テンプレートには HVM というのと PV というのがあるようなのですが、 HVM が Hardware Virtualized Machine PV が Paravirtualized ですね。PV の方を使います。メモリサイズは 1024MB にしました。



インポートの最中は、いったい何をやっているのか、Oracle VM Server を入れたマシンのディスクガリガリ言っています。数分でインポートが完了するので、「 Approve 」するとテンプレートが有効になります。

### VMの作成

ドキュメントの「6.3.1 仮想マシン・テンプレートに基づいた新しい仮想マシンの作成」とウィザードの指示に従って作成すればいいのですが、少しだけカスタマイズしたところがあります。あとで Oracle Database の RAC を試してみたいいので、ネットワークインターフェイスを 3個にしました。「 Virtual Network Interface Name 」の下のボタン「 Add Row 」を 2回押します。最初から表示されている VIF0 の下に VIF1 と VIF2 ができます。



ウィザードが完了すると、またもやディスクがガリガリ。終わったところで「 Power On 」して「 Console 」ボタンが有効になるまで何度か「 Refresh 」ボタンを押して、「 Console 」を押すとなにやら Java Applet を使ったポップアップが表示されます。パスワードを入れろと言うのですが、なぜかキーを受け付けないので、テキストエディタに書いたパスワードをコピペしてみるとログインできました。ログインすると、おなじみの Linux の起動時の表示が出てきます。Java Applet の表示領域をクリックするとキー入力できる仕組みになっています。よくできています。



テンプレートの root のパスワードはドキュメントの「5.1 仮想マシン・テンプレートのインポート」に書いてあります。root のパスワードを変更して、各ネットワークインターフェイスに別々のサブネットの静的なアドレスを設定しました。ping で自宅の LAN 環境に正常に接続できることを確認して、基本的な設定は完了です。 ssh で MacBook からこの VM に接続することもできました。



同じ手順で VM をもう一つインストールします。同じ名前のインターフェイスに同じサブネットのIPアドレスを設定します。ネットワークの設定まで終わったら、 ping で VM 間の疎通を確認します。


```
----------------------------
サブネット 192.168.0.0
----------------------------
192.168.0.32    MacBook
192.168.0.51    Oracle VM Server
192.168.0.52    Oracle VM Manager
192.168.0.211   VM1 eth0
192.168.0.212   VM2 eth0
----------------------------
サブネット 192.168.10.0
----------------------------
192.168.10.211  VM1 eth1
192.168.10.212  VM2 eth1
----------------------------
サブネット 192.168.100.0
----------------------------
192.168.100.211 VM1 eth2
192.168.100.212 VM2 eth2
```



### 仮想ディスクを追加する

Oracle VM Manager では、共有不可と共有の２種類の仮想ディスクを作成できます。どちらも、ホストマシン上のファイルを使います。お勉強やテストのためには便利なのですが、たぶん、本番運用の環境では SAN、NAS、iSCSI などを使うことになるのでしょう。この後 Oracle Database 11g RAC をインストールするために、共有不可 10GB 1個（システム用）、共有 10GB 2個（データ用）、共有 1GB 3個（OCR 用および投票ディスク用）を作成しました。



共有仮想ディスクの作成と追加で少し戸惑った点があります。

#### 共有仮想ディスクの VM が正常に追加できないことがある

> 共有仮想ディスクを追加した別の VM が起動しているとうまくいかないようです。他の VM をシャットダウンしてから追加することで回避しました。

#### 共有仮想ディスクの VM からの削除の手順がわかりにくい

> 「 Add Shared Virtual Disk 」ボタンで「 Manage Sharable Disks 」ページを開いて、そこで操作します。ボタンの名前、間違ってると思うけどなぁ。



共有仮想ディスクについては、同じ仮想ディスクを同じデバイス名で追加したかったので、１個追加する毎に fdisk -l コマンドで確認しました。

### ネットワークの設定についての補足

ここまで終わったところで、「共有仮想ディスク使うんだったら、ネットワーク・インターフェイスは２個ずつでいいや」と気がつき、それぞれの VM の VIF2 は削除しました。



作業の途中で、NFS がファイアウォールをうまく超えてくれないという問題につきあたりました。 HTTP 等々のように該当するポートを空けるだけではダメで、少々面倒でした。まず、ファイル `/etc/sysconfig/nfs` があれば、次の行のコメントを外します。なければ追加します。


```
LOCKD_TCPPORT=32803
LOCKD_UDPPORT=32769
MOUNTD_PORT=892
STATD_PORT=662
```


次に、ファイル `/etc/sysconfig/iptables` に次の行を追加します。もしくは、何らかのツールでファイアウォールに穴を空けます。


```
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 111 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp --dport 111 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 662 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp --dport 662 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 892 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp --dport 892 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 2049 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp --dport 2049 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 32803 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp --dport 32803 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 32769 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp --dport 32769 -j ACCEPT
```


次のコマンドを実行します。


```
/etc/init.d/iptables restart
/etc/init.d/nfs restart
/etc/init.d/nfslock restart
```


## 11g RAC のインストール

2009-08-05



今回主に参照したドキュメントは「Oracle Database 2日でReal Application Clustersガイド 11gリリース1（11.1） 部品番号: E05737-03」です。細かな内容については「Oracle Clusterwareインストレーション・ガイド 11gリリース1（11.1）for Linux E05831-06」なども見る必要があります。

### OS の環境の設定

仮想マシンの OS には Oracle Enterprise Linux 5.3 を使ったので、ユーザ `oracle` やグループ `oinstall, dba` は最初からあります。



`/etc/hosts` は次のようにしました。 `rac1, rac2` がホスト名、 `home.michinobu.jp` がドメイン名、 `rac1-priv, rac2-pri`v はプライベートネットワーク上の名称です。


```
127.0.0.1       localhost.localdomain   localhost
::1     localhost6.localdomain6 localhost6
192.168.0.211   rac1.home.michinobu.jp rac1
192.168.0.212   rac2.home.michinobu.jp rac2
192.168.0.231   rac1-vip.home.michinobu.jp rac1-vip
192.168.0.232   rac2-vip.home.michinobu.jp rac2-vip
192.168.10.211  rac1-priv.home.michinobu.jp rac1-priv
192.168.10.212  rac2-priv.home.michinobu.jp rac2-priv
```


次に ssh ですが、次の導通をすべて確認しました。すべてのノードで同じ確認をします。つまり、自分自身への導通も確認します。


```
ssh rac1
ssh rac2
ssh rac1.home.michinobu.jp
ssh rac2.home.michinobu.jp
ssh rac1-priv
ssh rac2-priv
ssh rac1-priv.home.michinobu.jp
ssh rac2-priv.home.michinobu.jp
```

SELinux は… テンプレートから作成した Enterprise Linux の場合動いてませんね。 `/etc/sysconfig/selinux` ファイルを探したのですが、ありませんでした。



iptables は無効にします。無効にしなくても、細かく設定すればいいのだろうと思うのですが、今回は手抜きします。



インストール先のディレクトリを作成します。


```
mkdir /u01/app
mkdir /u01/app/oracle
mkdir /u01/app/crs
chown -R oracle:oinstall /u01/app
```


ISO イメージのファイルは、次のようにマウントすればいいんですね。知らなかった。。。


```
mount -o loop,ro ISOイメージのパス マウントポイント
```


ブロックデバイスのパーミッションの設定ですが、ドキュメントには `/etc/udev/permissions.d` に設定ファイルを置けと書いてあるのですが、 Enterprise Linux 5.3 の場合そんなディレクトリはありません。以下のような内容のファイル `/etc/udev/rules.d/65-permissions.rules` を作成して OS を再起動します。


```
KERNEL=="xvde1", OWNER="root", GROUP="oinstall", MODE="640"
KERNEL=="xvdf1", OWNER="root", GROUP="oinstall", MODE="640"
KERNEL=="xvdg1", OWNER="root", GROUP="oinstall", MODE="640"
KERNEL=="xvde2", OWNER="oracle", GROUP="oinstall", MODE="640"
KERNEL=="xvdf2", OWNER="oracle", GROUP="oinstall", MODE="640"
KERNEL=="xvdg2", OWNER="oracle", GROUP="oinstall", MODE="640"
KERNEL=="xvdc", OWNER="oracle", GROUP="dba", MODE="660"
KERNEL=="xvdd", OWNER="oracle", GROUP="dba", MODE="660"
```


`xvde1` 〜 `xvdg2` は OCR ディスクと投票ディスクに使うパーティション、 `xvdc` と `xvdd` はデータ用のデバイスです。

### Clusterware の要件の検証

OS の設定が終わったら、クラスタ検証ユーティリティで環境を確認します。 CD-ROM など読み取り専用のメディアから起動する場合、カレントディレクトリをマウントポイントに移動してから実行するとエラーになります。それ以外のディレクトリからフルパス指定で起動します。



結果を見ると `glibc-2.5-12` で NG 出ているのですが、より新しいバージョンが入っているのでよしとします。

### Clusterware のインストール

Mac OS X の場合、次のコマンドで X を起動できます。



```
ssh -X -l  ユーザ名 ホスト名
```



パスワードを入れて、しばらくすると、ドックに X のアイコンが出現します。試しにターミナルで xclock と入力してみると、無事、時計が表示されました。ターミナルを閉じても X は自動で終了してくれないので手で終了してください。



インストールの手順はドキュメントに書いてある通り、ただし、インストーラの起動は、マウントポイントに移動してからではなく、外のディレクトリからフルパス指定で。 OS の設定に間違いがなければ、失敗することはないでしょう。

### ASM のインストール

ドキュメントに書いてある通りです。

### Database のインストール

ドキュメントに書いてある通りにやったんですが、起動にすごい時間がかかるなぁ。各ノードに Enterprise Manager が入っていますね。ブラウザで開いてみると、いつまでたってもページが表示されません。 ASM をインストールした直後のバックアップに戻して、シンプルな構成で入れ直してみようと思います。
