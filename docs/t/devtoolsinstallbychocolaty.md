# Chocolatey で Windows に開発ツールをインストールする

Update: 2020-07-14


Chocolatey ( https://chocolatey.org/ ) はたぶん主にシステム開発をやる人を主なターゲットとした
Windows にいろいろなものをインストールするツールとそのいろいろなもののリポジトリです。
オープンソースの製品を使って Windows でいまどきの Web の開発をするには必要でしょう。

とはいっても WSL ( [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) )
というものがあるので Linux というか bash や zsh などの UNIX系の Shell に抵抗ないのであれば
WSL を使うことをお勧めします。私はまだ WSL 2 は試していませんが、
WSL 1 でもそこから ``$ code`` で Visual Studio Code が起動できるしそれなら
ベースが Windows でも Mac でも Chrome OS でも Linux でもなんでもいいや、という感じです。

Chocolatey は non-administrative の手順
( https://chocolatey.org/docs/installation#non-administrative-install )
で入れてみました。
その後でいろいろ入れてみた感じ、 non-administrative ではない方がいいような気がします。

コマンドプロンプトではなく PowerShell を使ってください。
余談ですが、これから Windows でシステムの開発や運用の仕事をする人は PowerShell に慣れておきましょう。

```
PS> notepad ChocolateyInstallNonAdmin.ps1
PS> Set-ExecutionPolicy Bypass -Scope Process -Force;
PS> .\ChocolateyInstallNonAdmin.ps1
PS> choco
Chocolatey v0.10.15
Please run 'choco -?' or 'choco <command> -?' for help menu.
PS> choco -?
This is a listing of all of the different things you can pass to choco.

Commands

 * list - lists remote or local packages
 * find - searches remote or local packages (alias for search)
 * search - searches remote or local packages (alias for list)
 * info - retrieves package information. Shorthand for choco search pkgname --exact --verbose
 * install - installs packages from various sources
 * pin - suppress upgrades for a package
 * outdated - retrieves packages that are outdated. Similar to upgrade all --noop
 * upgrade - upgrades packages from various sources
 * uninstall - uninstalls a package
 * pack - packages up a nuspec to a compiled nupkg
 * push - pushes a compiled nupkg
 * new - generates files necessary for a chocolatey package from a template
 * sources - view and configure default sources (alias for source)
 * source - view and configure default sources
 * config - Retrieve and configure config file settings
 * feature - view and configure choco features
 * features - view and configure choco features (alias for feature)
 * setapikey - retrieves, saves or deletes an apikey for a particular source (alias for apikey)
 * apikey - retrieves, saves or deletes an apikey for a particular source
 * unpackself - have chocolatey set itself up
... ... ...

     --log-file=VALUE
     Log File to output to in addition to regular loggers. Available in 0.1-
       0.8+.
Chocolatey v0.10.15
```

RedHat系の yum や Debian の apt や Mac の brew 等々と同じようなコマンドが使えるようです。

まず git を入れます。

```
PS> choco install git -y
Chocolatey v0.10.15
Chocolatey detected you are not running from an elevated command shell
 (cmd/powershell).

 You may experience errors - many functions/packages
 require admin rights. Only advanced users should run choco w/out an
 elevated shell. When you open the command shell, you should ensure
 that you do so with "Run as Administrator" selected. If you are
 attempting to use Chocolatey in a non-administrator setting, you
 must select a different location other than the default install
 location. See
 https://chocolatey.org/install#non-administrative-install for details.


 Do you want to continue?([Y]es/[N]o): Y
```

なにやら警告が出ますが要するに Windows に何かインストールするときにたいてい出る確認のダイアログで「はい」押して、ということのようなのでそのまま進みます。

```
PS> git --version
git : 用語 'git' は、コマンドレット、関数、スクリプト ファイル、または操作可能なプログラムの名前として認識されません。
名前が正しく記述されていることを確認し、パスが含まれている場合はそのパスが正しいことを確認してから、再試行してください
。
発生場所 行:1 文字:1
+ git --version
+ ~~~
    + CategoryInfo          : ObjectNotFound: (git:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
```

git コマンドが見えてないようなので PowerShell を開き直してみます。

```
PS> git --version
git version 2.27.0.windows.1
PS> git config --global user.name "Michinobu Maeda"
PS> git config --global user.email "michinobumaeda@gmail.com"
```

正常にインストールできているようなので ``user.name`` と ``user.email`` を設定しておきます。
git を使う場合これらの設定は事実上必須です。
git の Windows 版には ``bash`` が付いてますが、それを使うくらいなら WSL でいいんじゃないかな。

次に Python 3 を入れます。これは PowerShell を管理者として起動して実行しなければうまくいきませんでした。

```
PS> choco install python3 -y

The recent package changes indicate a reboot is necessary.
 Please reboot at your earliest convenience.
```

リブートしろ、と Windows みたいなことを言われるので素直に従います。

```
PS> python3 --version
```

なにも表示されない。。。

```
PS> python -V
Python 3.8.3
```

Python 2 はいまさら使うなという前提かな。

次に Node.js を入れます。
Mac ならとりあえず最新 ( 14 とか 12 LTS とか ) を入れて
n でその都度必要なバージョンを指定するのが便利なのですが、
n は Windows に対応していません。私の場合、当面は 10 を使いたいのでバージョンを指定してインストールします。
npm も入るのですが、 npm が最新でない可能性もあります。
npm そのものを入れ直して、その他のグローバルでよく使うツールもついでに入れておきます。

```
PS> choco install nodejs-lts --version=10.16.0 -y
PS> node --version
v10.16.0
PS> npm ---version
6.9.0
PS> npm i -g npm yarn eslint jest firebase-tools @vue/cli
... ... ...

+ jest@26.1.0
+ @vue/cli@4.4.6
+ firebase-tools@8.4.3
+ eslint@7.4.0
+ npm@6.14.5
```

PHP を入れます。
Composer もいまどきの開発では必須ですから入れます。

```
PS> choco install php -y
PS> php --version
PHP 7.4.7 (cli) (built: Jun  9 2020 13:34:30) ( NTS Visual C++ 2017 x64 )
Copyright (c) The PHP Group
Zend Engine v3.4.0, Copyright (c) Zend Technologies

PS> choco install composer -y
PS> composer -V
Composer version 1.10.8 2020-06-24 21:23:30
```

Chocolatey で GUI のツールもインストールできます。
Visual Studio Code を入れてみます。

```
PS> choco install vscode -y
PS> code --version
1.46.1
cd9ea6488829f560dc949a8b2fb789f3cdc05f5d
x64
```

インストール後、私の環境では ``code`` で起動できました。ただし、この記事を書く前に普通に入れたものをアンインストールしています。もしかすると
PowerShell を起動し直すか OS 再起動するまでは ``code`` では起動できないかもしれません。

[パッケージのリポジトリ](https://chocolatey.org/packages)
を見ると他にも Gimp などいろいろあるようです。

で、結論として、 Linux というか bash や zsh が嫌いでなければ WSL を使うことをお勧めします。

Tag: Windows Chocolatey choco vscode powershell



