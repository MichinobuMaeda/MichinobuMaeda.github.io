# Linux と VMware で Oracle の Cluster

Update: 2008-02-10

## 低スペックマシンじゃ無理だぁ

日本Orale社から VMware 使ってお勉強などに使うための RAC ( Real Applicatin Cluster ) を構築するガイドが出ているので試してみました。ガイドでは Windows 上で VMware Server を使うことになっているのですが、自分がライセンス持っている Linux をホストにした VMware Workstation を使ってやってみたわけです。それ自体は大きな問題にはならないんですけどねぇ。 ガイドのものを大きく下回ったマシンのスペックで、なんとかインストール完了した Clusterware はすべてのアプリケーションが起動する前に何かがタイムアウトしてしまうようでとても不安定です。以下、それをなんとかした記録です。

## ホストが Linux の場合の console

ホストが Linux の場合、ガイドに出てくる console マシンはゲストではなくホストを使ったのでいいです。それだけでかなり負荷が下がります。



ホストが Fedora などの場合はたぶん追加の設定は不要です。 ssh の設定などをガイドの通りにすればだいじょうぶだと思います。



私は最近流行の Ubuntu のデスクトップ用途の構成を使ったのですが、この場合は SSH のインストールと X の設定の変更が必要でした。 Ubuntu は追加のパッケージのインストールは簡単だから SSH のインストールの説明はいらないですね。 X については私もよくわからないので、エラーメッセージの内容で google 検索してみてください。日本語ページの検索は目的の場所にたどり着かないかもしれません。

## VMware Workstation の場合の仮想ネットワークの設定

VMware Workstation はインストール後仮想ネットワークの設定を変更したりはできません。たぶん。私が理解している限りでは。



まず、日本Oracle社のガイドの最初の部分をよく読んで、どんな設定にする必要があるのか理解しましょう。で、ネットワークアドレスなどはできるだけガイドのものに合わせましょう。そうしないとその後の作業できっと混乱します。



VMware Workstation をインストールの際、「仮想ネットワークのためのウィザードを起動するか?」と聞かれますが、起動せず、マニュアルで設定するといいです。

## Clusterware のインストーラが Public インターファエイスを認識しない

さっき画面で指定したつもりなんだけどなぁ、何でこんなエラーメッセージが出るの、と、最初につまずいたのがこれです。



「指定のインタフェース”eth0”はパブリックではありません。パブリック・インタフェースを使用して仮想IPを構成する必要があります。」



詳しい話は端折りますが、このエラーが出たら次のコマンドで仮想IPの設定画面を起動して設定して、 Clusterware のインストールを続けると、たぶん、うまくいきます。


```
[root@oracle02 ~]# cd /home/oracle/oracle/product/10.2.0/crs/bin/`
[root@oracle02 bin]# ./vipca
```


Clusterware のインストールや Oracle のインスタンスの構築が終わったら次のコマンドで正常に起動終了するか確認しましょう。


```
[root@oracle01 ~]# cd /home/oracle/oracle/product/10.2.0/crs/bin/
[root@oracle02 bin]# ./crsctl stop crs
[root@oracle02 bin]# ./crsctl start crs
[root@oracle01 bin]# ./crs_stat -t
```


## Oracle のインストールのリモートの側でエラー

何が原因かよくわからないのですが Oracle のインストールのリモートの側でエラーになって、ログなどみると次のコマンドを実行しろというようなことが書いてあったので、その通りにしたら正常にインストール完了となりました。画面表示の都合で複数行に分けて書いていますが1行のコマンドです。


```
/home/oracle/oracle/product/10.2.0/db/oui/bin/runInstaller -attachHome \
-noClusterEnabled ORACLE_HOME=/home/oracle/oracle/product/10.2.0/db \
ORACLE_HOME_NAME=OraDb10g_home1 \
CLUSTER_NODES=oracle01,oracle02 \
"INVENTORY_LOCATION=/home/oracle/oracle/oraInventory" \
LOCAL_NODE=oracle02`
```


## Enterprise Manager がおそおぉぉぉぉぉぉい

インスタンスの構築までたどり着いて、最後に Enterprise Manager 入れたんですが、遅すぎてログイン画面もなかなか出てきません。これはもうどうしようもないので CPU をもう少し早いのにかえることに決めました。でも AMD の SocketA の CPU ってもう普通には売ってないんですよねぇ。中古品見つけたので次の週末にでも試してみることにします。
