# Chocolatey を使ってみる

Update: 2018-09-25


職場の Windows マシンはセキュリティ上の理由で入れられるものが制限されているので、
[Laraval 5 による開発の手順 #1](startlaravel1.html) を書いたときにはまだ Chocolatey のことを知りませんでした。

Chocolatey は Mac の Homebrew のようなものです、と、
Mac を使ってない人に言ってもわかるわけないですね。
Chocolatey は Windows 向けのパッケージマネージャーで、
2018年9月現在で 6,000 を超えるアプリ、ツールに対応しています ( https://chocolatey.org/packages ) 。

GUI のツールもあるようなのですが、開発に使うコマンドラインのツールを
Linux の ``yum`` や ``apt`` のような感じでインストールできます。
ざっと見たところ、
``git``, ``nodejs``, ``python2``, ``python3``, ``php``, ``composer``,
``sqlite``, ``openssh``, ``make``, ``mingw`` ( ``gcc`` などを含む ), ``gcc-arm``, ``7zip``
といったものがありました。
``tar`` が見つけられなかったけど、、、 ``tartool`` でいいのかな。。。

Chocolatey そのもののインストール方法は簡単で、
コマンドプロンプトか PowerShell のコンソールを管理者権限で開いて、
https://chocolatey.org/install
に記載されている呪文を実行するだけです。
PowerShell の場合は先にセキュリティの設定を見ておいてください。

```
Get-ExecutionPolicy
```

で一番厳しい ``Restricted`` だったら

```
Set-ExecutionPolicy AllSigned
```

としてください。

Chocolatey をインストールしたらコンソールを開き直してください。

全体のヘルプは、

```
choco -?
```

コマンドのヘルプは、例えば ``install`` コマンドの場合

```
choco install -?
```

です。

```
choco search git
```

で欲しいパッケージを探して、

```
choco info git
```

でパッケージについての情報を見ることができます。

パッケージのインストールは

```
choco install git -y
```

です。 ``-y`` はコマンド実行中の問い合わせをすべて ``Yes`` とするオプションです。

パッケージをインストールする際にたいてい ``PATH`` の設定をしていますので、
インストール後はコンソールを開き直してください。

インストールしたものの実行は、管理者権限不要です。

``vim`` もありました。漢字を入力しても化けないようです。

```
choco upgrade all
```

ですべてのパッケージを最新にします。

``php`` は ``C:¥tools¥php72`` のようなフォルダに置かれます。
``php.ini`` の ``extensions`` がすべてコメントアウトされているので、
全く使いそうにないもの以外はコメントアウトを外してください。

