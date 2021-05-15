Macで "xcrun: error:" が出たら
=====

Update: 2021-02-26


私の MacBook で作業していると突然

```
xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
```

というエラーが出ることがあります。最近多いような気がするな。今回は Python と ``brew update`` で。ここで出られると作業がなんにもできません。どうもOSのアップデートが原因のようです。

Mac OS: xcrun: error: invalid active developer path, missing xcrun \\
https://ma.ttias.be/mac-os-xcrun-error-invalid-active-developer-path-missing-xcrun/

によると

```
$ xcode-select --install
```

しろと。やってみると何やらダイアログが表示されて Xcode のなんたら（よくわからないけど iOS 向けアプリを作っていない私には本体は必要ないけど一部が必要らしい）がインストールされます。

それがダメなら

```
$ sudo xcode-select --reset
```

それでもダメなら

Apple developer download section \\
https://developer.apple.com/download/more/

から Xcode を入手しろとのことですが、私は Apple Developer ID は持ってないぞ。
Xcode ならストアからインストールできるし、この記事を見る前はそれで巨大なやつを丸ごとインストールしてたけど。

Tag: macos xcode



