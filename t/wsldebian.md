Windows Subsystem for Linux の Debian で Web 開発の環境を作る
=====

Update: 2020-07-11


Windows Subsystem for Linux の有効化の手順は
<https://docs.microsoft.com/ja-jp/windows/wsl/install-win10>
を見てください。私は組み込み用途で使われることが多い Debian を選択しました。

2019年6月時点では Debian 9 "stretch" が入ります。 Debian 10 "buster" はまだリリースされたばかりです。
私の好みで neovim を入れました。

```
$ cat /etc/issue
Debian GNU/Linux 9 \n \l

$ sudo apt update
$ sudo apt upgrade
$ sudo apt install neovim
$ nvim --version
NVIM 0.1.7

```

標準のパッケージとして ssh クライアントと git と python3 を入れます。

```
$ sudo apt install openssh-client
$ sudo apt install git
$ git --version
git version 2.11.0

$ git config --global user.name "Firstname Lastname"
$ git config --global user.email "michinobumaeda@gmail.com"

$ sudo apt install python3
$ python3 --version
Python 3.5.3

$ sudo apt install python3-pip
$ pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.5)

$ pip3 install virtualenv
$ virtualenv --version
16.6.1

```

<https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-debian-9>
を参考に Node.js 10 を入れます。

```
$ sudo apt install curl
$ curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh
$ sudo bash nodesource_setup.sh
$ sudo apt install nodejs
$ node --version
v10.16.0

$ npm --version
6.9.0

$ sudo npm install yarn -g
$ yarn --version
1.16.0

```

<https://computingforgeeks.com/how-to-install-php-7-3-on-debian-9-debian-8/>
を参考に PHP 7.3 を入れます。

```
$ sudo apt -y install lsb-release apt-transport-https ca-certificates
$ sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
$ echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php7.3.list
deb https://packages.sury.org/php/ stretch main

$ sudo apt update
$ sudo apt -y install php7.3
$ php --version
PHP 7.3.6-1+0~20190531112735.39+stretch~1.gbp6131b7 (cli) (built: May 31 2019 11:27:35) ( NTS )

$ echo test > index.html
$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 ...

```

Webブラウザで URL <http://localhost:8000/> が表示できるれば OK です。

Windows の notepad を起動することもできます。拡張し ``.exe`` を付けてください。
ちなみに ``ping.exe`` で Windows版の ping が、
``ping`` で Debian の ping が起動できます。

```
$ notepad.exe index.html
```

``ls /mnt/c/`` で Windows の C: ドライブも参照できます。

Windows のエクスプローラやコマンドプロンプトから ``\\wsl$\Debian`` Debian のファイルシステムが参照できます。

WSL 環境からのインターネット接続がうまくいかない場合は、
``ipconfig.exe /all`` で DNS サーバの IPアドレスを調べて、
``/etc/resolv.conf`` に ``nameserver IPアドレス`` と設定してやると取り敢えずなんとかなるようです。
私自身、モバイル環境でトラブったのですが、正しい手順はよくわかりません。

ssh クライアントは Linux とまったく同じように利用できます。

```
$ mksir ~/.ssh
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):

$ eval `ssh-agent`
$ ssh-add

```

Visual Studio Code をインストール済みであれば、コマンド ``code`` で起動できるようです。

```
$ git clone gtit@gitlab.com:UserName/project-name.git
$ code project-name
```

[Ctrl]+[Shift]+P で ``Terminal: Select Default Shell`` を入力するとターミナルのデフォルトのシェルの選択肢が出てきますので、
``WSL Bash C:\Windows\System32\wsl.exe`` を選択します。

ターミナルはメニューの ``Terminal`` -- ``New Terminal`` で表示できます。
OSによってショートカットキーが異なるかもしれないので、メニューに表示されるものを使ってください。

Python の場合、プロジェクトごとの環境設定は以下のようにするとよいです。

```
$ virtualenv venv
$ . venv/bin/activate
$ python --version
Python 3.5.3

$ which python
project-directory/venv/bin/python

$ which pip
project-directory/venv/bin/pip

```

プロジェクトに ``requirements.txt`` がある場合は以下のコマンドで必要なパッケージが導入できます。
パッケージはグローバルではなく、プロジェクトのディレクトリの ``venv`` サブディレクトリの下に入ります。

```
$ pip install -r requirements.txt
$ ls venv/lib/python3.5/
```

一度設定すると、次回からは

```
$ . venv/bin/activate
```

だけでだいじょうぶです。

virtualenv で python のバージョンをプロジェクト毎に設定することも可能です。
Node.js や PHP などの他の言語にも Python の virtualenv に似た仕組みがあります。

Tag: Windows WSL Debian python pip virtualenv git



