SSH の基本的な使い方
=====

Update: 2020-12-30


この間あちこちで説明していることをまとめました。

最近は Linux と Mac だけでなく Windows でも WSL に ``ssh`` や ``scp`` などのコマンドが入っているのでエンジニアさんはそれらを使っていただきたいです。
Git などもそうなのですが GUI のツールは製品によっていちいち手順が違うのが困ります。一つの会社の中でみなさん同じツールを使うことになっているのならともかく、そうでないところで使い方がわからんからと聞かれても、、、私は Mac だから。

それから、ネットやシステムの仕事をしているのに公開キー認証を使うことができるところで公開キーを使っていない場合、その会社とか周りの人とかがよくわかってないようでしたらセキュリティやばいので、とりあえず自分だけでも理解しておいてください。以下、公開キー認証だけを使ってパスワード認証を無効にする手順です。
## 自分のキーを作成する

以下の手順では ``~/.ssh`` の下に秘密鍵 ``id_rsa`` と公開鍵 ``id_rsa.pub`` のペアを作成します。
まずコマンド ``ssh-keygen`` を実行します。

既存のキーがある場合は、以下のように警告が出ますので、既存のキーをどけるか、別の名前で作成するかしてください。

```
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):
/home/username/.ssh/id_rsa already exists.
Overwrite (y/n)?
```

既存のキーがない場合は以下のようになりますので ２個目と 3個目の問合せでパスフレーズを入力してください。文章のような長いものでもだいじょうぶです。

それからひとつ大事なことを。このパスフレーズは接続するサーバの側のユーザのパスワードとは全く関係ありません。別のものを設定してだいじょうぶです、というか、セキュリティを強くするには同じでない方がよいです。

```
$ ssh-keygen
Enter file in which to save the key (/home/username/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:97vKT53OzM3v8mBuRu+pbnPKgqPfBp79ILyRhnmp/SI username@hostname
The key's randomart image is:
+---[RSA 2048]----+
|                 |
|                 |
|                 |
|                 |
|        S .      |
|        +oo. ... |
|       o.O=.o.=. |
|       E=B==o@+=o|
|       o++B=OX@*O|
+----[SHA256]-----+
```

公開キーとして以下のようなものが出力されます。

```
$ cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAA...途中略...iwYNMY+bvvvjBqWvJlxeAraqfIIh username@hostname</code>

秘密キーは秘密です。


===== サーバ側に公開キーを置く =====

まず、どうにかしてサーバに公開キーを送り込みます。次のような手段を使うことができると思います。

  * たぶんデフォルトで有効になっている SSH のパスワード認証を使う
  * FTPを使う

SSH のパスワード認証を利用できる場合は SCP コマンドを使います。

<code>
$ scp ~/.ssh/id_rsa.pub username@servername:~/
```

SSH か telnet や VNC 等でサーバのターミナルを開いて ``~/.ssh`` ディレクトリがなければ作成します。

```
$ mkdir .ssh
$ chown go-rwx .ssh
```

``~/.ssh/authorized_keys`` に公開キーを追加します。

```
$ cat id_rsa.pub >> .ssh/authorized_keys
$ rm id_rsa.pub
```

これで公開キー認証による接続がきるようになります。たぶん。サーバで公開キー認証が無効になっていなければ。普通は有効です。

複数のキーを登録すること可能です。私の場合 Mac と Android でそれぞれ別のキーを作成して使っています。
機器の故障等のことを考えると、複数ある方が安心です。

公開キー認証が使える場合は、先ほど作成したキーのパスフレーズを要求され、サーバ側のユーザのパスワードは聞かれません。先ほど作成したキーのファイル名がデフォルトの ``id_rsa`` と ``id_rsa.pub`` の場合はキーのファイル名の指定は無しでだいじょうぶです。

```
$ ssh username@servername
Enter passphrase for key '/home/username/.ssh/id_rsa':
```

キーのファイル名がデフォルトの ``id_rsa`` と ``id_rsa.pub`` ではない場合は ``-i`` オプションで公開キーのファイル名を指定します。

```
$ ssh -i ~/.ssh/id_rsa_2.pub username@servername
Enter passphrase for key '/home/username/.ssh/id_rsa':
```


## パスフレーズの入力を減らすには

パスワード認証の場合は接続するたびに毎回パスワードを要求されますが、
SSHの公開キー認証の場合は手元のターミナルにパスフレーズを覚えさせることができます。この仕組みでパスフレーズの入力の回数を減らすことができます。また、あるサーバを踏み台に別のサーバに接続する場合に認証情報を引き継ぐ（つまりパスフレーズの入力が不要とする）ことができます。

この仕組みでは認証情報をメモリ中で管理していますので、漏洩することはありません。

Linux の場合 ``ssh-agent`` と ``ssh-add`` を使います。
``ssh-agent`` は下記のように変な使い方をしますが、説明は省略します。
これらを実行したターミナルの中で有効です。

```
$ eval `ssh-agent`
$ ssh-add
Enter passphrase for /home/username/.ssh/id_rsa:
Identity added: /home/username/.ssh/id_rsa (/home/username/.ssh/id_rsa)
```

``eval `ssh-agent`; ssh-add`` を alias に登録しておくといいかもしれません。

Mac の場合は ``ssh-add`` だけです。そのコマンドの実行したターミナルだけでなく他でも有効になるようなのですが、仕組みや仕様はよくわかりません。
``ssh-add`` の実行が必要になるのはマシンの再起動の後くらいかなぁ。。。


## パスワード認証を無効にする

サーバ側の sshd の設定変更が可能でしたら、公開鍵認証で接続できることが確認できたらパスワード認証を無効にしてしまいましょう。これで総当たり攻撃などによる不正アクセスを防止することができます。なお、「 sshd って何？」とあなたかあなたが設定を依頼するシステム管理者がいう場合は設定変更可能ではありません。詳しくは
[sshでパスワード認証を禁止するには](https://www.atmarkit.co.jp/flinux/rensai/linuxtips/430dnypsswdacces.html)
などをご参照ください。手短に言うと

  * ``/etc/ssh/sshd_config`` に ``PasswordAuthentication no`` を設定する。
  * sshd を再起動する。

です。最近の Linux の Debian 系のディストリビューションの場合、 sshd の再起動は

```
$ sudo systemctl restart sshd
```

です。

## クライアント側の設定

私の場合、以下のような設定をしています。

```
$ cat .ssh/config
Host *
        ServerAliveInterval 60
Host www
        User username2
        Hostname www.example.com
        ForwardAgent yes
```

``ServerAliveInterval 60`` : サーバからタイムアウトで切断されるのを防ぐため、６０秒毎に空のデータを送信する。

``Host www`` / ``Hostname`` : ``Hostname`` で指定したサーバに ``www`` で接続する。

``User username2`` : このホストに接続する際に ``username2`` を使用する。

``ForwardAgent yes`` : このサーバを踏み台にて別のサーバに接続する際に ``ssh-add`` で作成した認証情報を再利用する。

上記のように ``Hostname`` と ``User`` を設定しておくと、

```
$ ssh username2@www.example.com
```

の代わりに

```
$ ssh www
```

で接続できます。これらのパラメータ以外に ``Port`` や ``IdentityFile`` なども設定できます。


Tag: ssh
