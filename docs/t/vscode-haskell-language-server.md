# VSCode Haskell Language Server の設定

Update: 2020-07-11


Haskell のお勉強のために普段使っている VSCode に
Haskell Language Server を入れました。

[本気で Haskell したい人向けの Stack チュートリアル](https://qiita.com/waddlaw/items/49874f4cf9b680e4b015)
など見たところ、パッケージの管理には stack を使うと良いようです。
というか、それ以外は私には無理そうです。
Nix は MacBook にうまく入れられませんでした。
stack は

```
% curl -sSL https://get.haskellstack.org/ | sh
```

で入れます。バイナリは ``/usr/local/bin/stack`` に入ります。
stack を使って導入するコマンドは ``~/.local/bin`` に入るので、
そこにパスを通しておきます。私の場合 ``.zshrc`` に以下のように追加しました。

```
export PATH=/Users/<user>/.local/bin:$PATH
```

で、 ``stack update`` を実行すると ``~/.stack`` のしたになにやらいろいろできるので、
``~/.stack/config.yaml`` の以下の行を編集します。

```
templates:
  params:
    author-name: Michinobu Maeda
    author-email: michinobumaeda@gmail.com
#    copyright:
    github-username: MichinobuMaeda
```

それから haskell-ide-engine ですが、 私の MacBook の場合
Haskell Language Server 拡張の説明通りには入りません。

```
% git clone https://github.com/haskell/haskell-ide-engine --recursive
% stack ./install.hs hie
% stack ./install.hs hie
```

で入りました。
``install.hs`` はなぜか途中で一度止まります。
もう一度実行すると complete します。
２時間かかりました（汗

stack のコマンドの一覧は ``stack --help`` です。

```
% stack new <プロジェクト名>
```

でプロジェクトを作成してそのディレクトリを VSCode で開きます。

VSCode の拡張は Haskell Syntax Highlighting と Haskell Language Server を入れます。

VSCode のターミナルで REPL を開くとなんだかたくさんメッセージが出てきて、、、

```
% stack repl
  ... たくさんメッセージ ...
*Main Lib> 1 + 2
3
*Main Lib>
```

プロンプトは ``Prelude>`` じゃないんだ？

``stack build`` するととりあえずエラーは出ないようです。

``stack run`` でプロジェクト作成時のサンプルコードに入っている文字列が出力されます。
試しにその文字列を数値 ``0`` に変えるとエラーになりますね。こういう言語は久しぶりです。

Tag: haskell vscode
