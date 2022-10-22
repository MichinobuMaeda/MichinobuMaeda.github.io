Google Cloud Workstations を使ってみる
=====

Update: 2022-10-22

Google が Cloud Workstations というサービスをはじめました。まだ Preview です。 Docker コンテナに Web版の Code OSS などのエディタやポートフォワーディングの機能が付いています。類似のものは GitHub など他からもでているのですが、私の用途に微妙に合わないところがあって使っていませんでした。これが使えると自分のPCの性能はどうでもよくなります。複数の環境の同居の仕組みで悩む必要もなくなります。

サービスの仕様をざっと見た感じ iPad は難しいかな。でも Chrome Book は問題なさそうです。一度 Linux 環境を入れてみたもののそれっきりになっていた非力な Chrome Book で試してみます。

Chrome Book 上の古い Debian は削除して、入れ直してみました。

```
michinobu@penguin:~$ sudo apt update
michinobu@penguin:~$ sudo apt upgrade
michinobu@penguin:~$ cat /etc/debian_version
11.5
michinobu@penguin:~$ lscpu
Architecture:                    x86_64
 ... ... ...
michinobu@penguin:~$ python3 --version
Python 3.9.2
```

ポートフォワーディングやSSH接続を使う場合は gcloud CLI を入れておきます。

Google Cloud のプロジェクトが無い場合は作成して、
Billing と Cloud Workstations API を有効にしてください。

メニューから Cloud Workstations を開くと、メニュー項目として

- Workstations
- Configurations
- Clusters

が並んでいます。下から順番に作成します。

最初に Cluster を作成します。
デフォルトは Public で、単純な構成ならデフォルトのままで良いと思います。
Public とはいっても SSH tunnel を使うしか無い環境ですので、通常の用途でしたらセキュリティはそれでだいじょうぶでしょう。
Cluster の作成には20分くらいかかります。

次に Configuration を作成します。
"Quick start workstations" はカネかかりそうなので無効にしました。
今回は Apache + PHP の単純な Webサイトのテスト環境にしたいだけなので、
"Machine type" は一番小さなものにしています。
エディタなどもここで選択できます。私は普段 VS Code を使っているので、デフォルトのまま Code OSS としました。
設定を保存すると Configuration はすぐにできます。

最後に Workstation を作成します。
名称を決めて Configuration を選択するだけですぐにできます。

一覧の中の Workstation を "Start" すると 2分40秒くらいで起動しまして
"START" が "LAUNCH" に変わります。
"LAUNCH" をクリックすると Code OSS が表示されます。ブラウザを全画面表示にすると、デスクトップ版の VS Code とほとんど同じですね。

Code OSS でターミナルを開くとこんな感じです。

```
 user@workstation-test:~$ pwd
/home/user
user@workstation-test:~$ echo $SHELL
/bin/bash
user@workstation-test:~$ cat /etc/debian_version
11.5
user@workstation-test:~$ python3 --version
Python 3.10.7
user@workstation-test:~$ git --version
git version 2.30.2
```

"LAUNCH" の右の ▼ をクリックすると Port forwarding や SSH 接続の手順が表示されます。

![LAUNCH](googlecloudworkstations01.png)

Webサーバ等を動かす場合、ポート 80 は既に使われているので他のポートにしてください。

```
user@workstation-php74:~$ curl localhost:80
<!-- Copyright (C) Microsoft Corporation. All rights reserved. -->
<!DOCTYPE html>
<html>
 ... ... ...
```

Tag: cloud
