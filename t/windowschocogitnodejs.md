Chocolaty で Git や Node.js を入れる
=====

Update: 2021-05-05


[Tamuro デモ用ソース](https://github.com/MichinobuMaeda/tamurodemo) を Linux や Bash に慣れていない人に試してもらうための Chocolaty で Git や Node.js を入れる手順です。

Linux で Bash などのシェルを使ったことある人は WSL2 https://docs.microsoft.com/ja-jp/windows/wsl/install-win10 を利用してください。その方が楽です。
WSL2 に GUI を入れてなくてもコンソールから code コマンドで Visual Studio Code を起動できますし、
Visual Studio Code の中のターミナルで WSL2 の Bash を使うこともできます。

以下の作業中に Windows ファイアウォールが Java や Node.js によるネットワークアクセスの許可を求める表示を出したら許可してください。

## Chocolatey

いろいろなツールを導入するために Chocolatey を使います。

Chocolatey を PowerShell のコマンドでインストールするのですが、 Windows 10 のデフォルトの設定はセキュリティが厳しすぎるので ``Restricted`` から ``RemoteSigned`` に変更します。

スタートメニューで Windows PowerShell をマウス右クリック > その他 > 管理者として実行

```
PS C:\WINDOWS\system32> Get-ExecutionPolicy
Restricted

PS C:\WINDOWS\system32> Set-ExecutionPolicy RemoteSigned

Execution Policy Change
... ... ...
[Y] Yes ... ... .. : Y

PS C:\WINDOWS\system32> Get-ExecutionPolicy
RemoteSigned
```

https://chocolatey.org/install に書いてある呪文をコピペして実行します。

```
PS C:\WINDOWS\system32> Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

PS C:\WINDOWS\system32> choco --version
0.10.15
```

## Git

PowerShell を閉じて管理者として起動しなおします。

```
PS C:\WINDOWS\system32> choco install git
 ... ... ...
Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint): A

PS C:\WINDOWS\system32> git --version
git version 2.31.1.windows.1
```

Git といっしょに Git Bash というものも入っています。
Linux と同じ感じのコンソールです。

## OpenJDK

Firebase emulator を動かすのに Java が必要なので OpenJDK を入れます。 
``"openjdk"`` で検索してみると 16 という新しいものが用意されているのでそれを入れます。

```
PS C:\WINDOWS\system32> choco search openjdk
Chocolatey v0.10.15
openjdk 16.0.1 [Approved] Downloads cached for licensed users
 ... ... ...

PS C:\WINDOWS\system32> choco install openjdk
 ... ... ...
Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint): A
```

表示されたメッセージにしたがい、PowerShell を閉じて管理者として起動しなおします。

```
PS C:\WINDOWS\system32> java --version
openjdk 16.0.1 2021-04-20
OpenJDK Runtime Environment (build 16.0.1+9-24)
OpenJDK 64-Bit Server VM (build 16.0.1+9-24, mixed mode, sharing)
```

## Node.js

私は Mac では n というパッケージで Node.js のバージョンを切り替えて作業していたのですが、
n は Windows には対応していないので NVM を入れます。

```
PS C:\WINDOWS\system32> choco install nvm
 ... ... ...
Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint): A
```

表示されたメッセージにしたがい、PowerShell を閉じて管理者として起動しなおします。

```
PS C:\WINDOWS\system32> nvm --verison

Running version 1.1.7.

PS C:\WINDOWS\system32> nvm install 12.22.1
PS C:\WINDOWS\system32> nvm use 12.22.1
PS C:\WINDOWS\system32> node --version
v12.22.1
```

## Visual Studio Code

choco コマンドでもインストールできると思うのですが、私は
https://code.visualstudio.com/Download
からインストーラをダウンロードしてインストールしました。 
OS を再起動すると PowerShell からでも Git Bash からでも code で起動できるようになります。

Windows 版のターミナルのデフォルトは PowerShell です。私は Bash を使い慣れているので Git Bash に設定変更しようかな、、、と思ったのですがその前に、公開しているソースなのに Bash でないと動かないものを作ってしまったような気がするのでしばらくは PowerShell のまま点検します。

## SSH

GitHub の接続に SSH を使用します。
ssh コマンドを実行してみて存在しない場合は、 Windows 10 のオプション機能を有効にします。

Windows のスタートメニュー > 設定 > アプリ > オプション機能 > 機能の追加 > OpenSSHクライアント

```
PS C:\WINDOWS\system32> ssh -V
OpenSSH_for_Windows_8.1p1, LibreSSL 3.0.2

PS C:\WINDOWS\system32> scp
usage: scp [-346BCpqrTv] [-c cipher] [-F ssh_config] [-i identity_file]
            [-J destination] [-l limit] [-o ssh_option] [-P port]
            [-S program] source ... target
```

## SSH 公開鍵の作成

ここから後は管理者権限は不要です。

Git で使用する自分の名前とメールアドレスを登録します。ここで設定したものがソースのコミット時に記録されます。 GitHub 等のサービスのアカウントとは別です（たぶん）。

```
PS C:\Users\michinobu> git config --global user.name "Your Name"
PS C:\Users\michinobu> git config --global user.email you@example.com
```

SSH の鍵を作成します。
SSHの鍵のファイルを置く場所は、特に複数のものを使い分ける用がなければ（普通ないです）デフォルトの場所のままにしてください。パスフレーズは文章のような長いものでもだいじょうぶです。

```
PS C:\Users\michinobu> ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (C:\Users\michinobu/.ssh/id_rsa):
Created directory 'C:\Users\michinobu/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:\Users\michinobu/.ssh/id_rsa.
Your public key has been saved in C:\Users\michinobu/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256: ... ... ...
```

生成された２ファイルのうち ``id_rsa.pub`` が公開キーです。これを GitHub などに登録して使います。秘密キー ``id_rsa`` は何があっても他人に渡したらダメです。

パスフレーズを忘れたり、秘密キーが漏洩した場合は鍵を作り直して、他の接続手段を使うか誰か他の人に頼むかして設定しなおしましょう。ほとんどの場合はそれで運用は何とかなります。私の場合、複数の端末からそれぞれ異なるキーで接続できるようにしています。

作業中に毎回パスフレーズを入力しなくて済むように ssh-agent という仕組みを使うことができるのですが、

```
PS C:\Users\michinobu> ssh-add
Error connecting to agent: No such file or directory
```

ssh-agent サービスが動いていない。。。

タスクマネージャ > 詳細 > サービス  > サービス管理ツールを開く > OpenSSH Authenticate Agent をマウスダブルクリック > スタートアップの種類：自動 > 適用 > 開始

```
PS C:\Users\michinobu> ssh-add
Enter passphrase for C:\Users\michinobu/.ssh/id_rsa:
Identity added: C:\Users\michinobu/.ssh/id_rsa (michinobu@MICHINOBUMA635A)
```

Windows の場合は eval `ssh-agent` とかしなくていいみたいだな。

デモ用ソースを clone しようとすると、、、

```
PS C:\Users\michinobu> git clone git@github.com:MichinobuMaeda/tamurodemo.git
Cloning into 'tamurodemo'...
 ... ... ...
Enter passphrase for key '/c/Users/michinobu/.ssh/id_rsa':
```

git が ssh-add した情報を認識してくれない。。。

https://snowdrift.tech/cli/ssh/git/tutorials/2019/01/31/using-ssh-agent-git-windows.html#:~:text=The ssh-agent that is included with git%2C while,is available for use. Enabling and starting ssh-agent
によると、まず、 git コマンドより ssh コマンドの PATH を先にしろと、、、

```
PS C:\Users\michinobu> Get-Command git | Select-Object Source

Source
------
C:\Program Files (x86)\Git\cmd\git.exe

PS C:\Users\michinobu> Get-Command ssh | Select-Object Source

Source
------
C:\WINDOWS\System32\OpenSSH\ssh.exe

PS C:\Users\michinobu> $env:PATH
C:\Python39\Scripts\;C:\Python39\;C:\Program Files\Parallels\Parallels Tools\Applications;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\ProgramData\chocolatey\bin;C:\Program Files (x86)\Git\cmd;C:\Program Files\OpenJDK\jdk-16.0.1\bin;C:\ProgramData\nvm;C:\Program Files\nodejs;C:\Users\michinobu\AppData\Local\Microsoft\WindowsApps;;C:\Users\michinobu\AppData\Local\Programs\Microsoft VS Code\bin
```

、、、なってます。そうなってなければ Windows のスタートメニュー > システム > バージョン情報 > システムの詳細設定 > 詳細設定 > 環境変数 でがんばって直します。

それから環境変数 GIT_SSH を設定します。

```
PS C:\Users\michinobu> [Environment]::SetEnvironmentVariable("GIT_SSH", "$((Get-Command ssh).Source)", [System.EnvironmentVariableTarget]::User)
```

新しい PowerShell のコンソールを開いてデモ用ソースを clone するとうまくいきました。

```
PS C:\Users\michinobu> git clone git@github.com:MichinobuMaeda/tamurodemo.git
Cloning into 'tamurodemo'...
remote: Enumerating objects: 6950, done.
remote: Counting objects: 100% (6950/6950), done.
remote: Compressing objects: 100% (2076/2076), done.
Receiving objects: 100% (6950/6950), 4.86 MiB | 409.00 KiB/s, done.
remote: Total 6950 (delta 4554), reused 6903 (delta 4510), pack-reused 0
Resolving deltas: 100% (4554/4554), done.
```

## Node.js のパッケージのインストール

https://github.com/MichinobuMaeda/tamurodemo/blob/master/docs/prerequisites.md
については n ではなく NVM を使うので、少し手順が変わります。次の 1行だけ実行してください。

```
PS C:\Users\michinobu> npm -g install yarn firebase-tools eslint jest @vue/cli
 ... ... ...
+ yarn@1.22.10
+ firebase-tools@9.10.0
+ eslint@7.25.0
+ jest@26.6.3
+ @vue/cli@4.5.12
added 2227 packages from 811 contributors in 196.005s
```

## 開発環境のセットアップ

先ほどの手順でコマンドを入れたので、念のための新しい PowerShell を開きなおします。

https://github.com/MichinobuMaeda/tamurodemo/blob/master/docs/dev.md
は PowerShell でも同様に動きます。

```
PS C:\Users\michinobu> cd tamurodemo
PS C:\Users\michinobu\tamurodemo> cd functions
PS C:\Users\michinobu\tamurodemo\functions> yarn
PS C:\Users\michinobu\tamurodemo\functions> cd ..
PS C:\Users\michinobu\tamurodemo> yarn
PS C:\Users\michinobu\tamurodemo> yarn test:unit
 ... ... ...
Test Suites: 26 passed, 26 total
Tests:       135 passed, 135 total
Snapshots:   0 total
Time:        106.881s
 ... ... ...
Done in 143.10s.

PS C:\Users\michinobu\tamurodemo> tools/testOnly.bat tests/unit/auth/admin.spec.js
 ... ... ...
Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   0 total
Time:        5.658s
Ran all test suites matching /tests\\unit\\auth\\admin.spec.js/i.
 ... ... ...

PS C:\Users\michinobu\tamurodemo> yarn serve
```

ローカルサーバを実行するとコンパイル完了後に自動でブラウザが開きます。エラー等が表示されないのにブラウザが起動しない場合や、デフォルト以外のブラウザで表示したい場合は http://localhost:8000/ を開いてください。

ローカルサーバは ``[Ctrl]+[C]`` で終了します。

Visual Studio Code を起動して

```
PS C:\Users\michinobu\tamurodemo> cd ..
PS C:\Users\michinobu> code tamurodemo
```

``[Ctrl]+[Shift]+[`]`` でターミナルを起動できます。デフォルトは PowerShell です。 PowerShell が苦手ない人は CMD や Git Bash に変えてもいいですが、今後 Windows のサーバサイドの仕事をする人は慣れておいた方がいいです。

Tag: windows chocolaty nodejs ssh



