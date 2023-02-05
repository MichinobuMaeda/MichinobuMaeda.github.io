# Chrome OS の Debian を 10 にアップグレードする

Update: 2020-07-25


Linux が普通に動くタブレットかそれに近いものが欲しくて Chrome OS のノートPCを買ってみました。
Ubuntu Touch は開発が止まってしまって自分で同様のものをつくるのはかなりたいへんです、というか、無理です。
タッチスクリーンの古いノートPCに 32 bit の Debian を入れてみたものはあるのですが、
ディスプレイを指で押しても反応しません。
とはいえ Android や iPad で ``bash`` や ``ssh`` を使うのはなにかと窮屈ですから。

Chrome OS のノートPC は Mac は言うに及ばず Windows のものより安めです。
CPU やディスプレイが同レベルでもディスクが小さいからでしょうね。
私が各社の製品を一通り見たところ（たいした数ではない）、
ほとんどディスプレイがくるっと 360度回転するタイプのようです。

Chrome OS に搭載されている Chrome ブラウザは Android のものではなく Windows や Mac の PC のものと同様の UI で、
Android が大きくなっただけではない感じです。
Microsoft Office などは Android 版を使うことになりますが、どっちかというと PC に近いものかな。

で、この Chrome OS には Debian が付いてます。

[Chromebook で Linux（ベータ版）をセットアップする](https://support.google.com/chromebook/answer/9145439?hl=ja)

付いているのですが、初期状態では Debian 9 で少し古いです。
ふつうに ``apt install`` すると PHP や Node.js はずいぶん古いバージョンが入ってしまいます。
パッケージのリポジトリを追加して、とかやってもいいのですが、
Debian 10 に上げられるのなら上げたいです。

Debian 9 から Debian 10 へのアップグレードは自分の Web サーバでやったことがあるのですが、
同じやり方で Chrome OS の本体に影響しないのか不安なので調べてみたら、
やはり Chrome OS 独自の手順でした。

[Upgrading Crostini to Debian Buster (10)](https://kmyers.me/blog/chromeos/upgrading-crostini-to-debian-buster-10/)

まず Chrome OS 本体をアップデートします。
Chrome OS の Settings （日本語だと「設定」かな？）の
"About Chrome OS" （日本語だと「Chrome OS について」かな？）にアップデート確認のボタンがあるので押します。
上記の記事では 81.X 以降でなきゃダメとのことですが、自分のはアップデートすると 83.0 になりました。

次に Debian を開いて

```
$ cd /opt/google/cros-containers/bin/
$ sudo ./upgrade_container
```

を実行します。私の場合は途中でなにやらメッセーが出て止まって
``sudo apt --fix-broken install`` を実行して修復しろとのことでしたので素直にそのとおりにやって、
途中で止まったコマンドを再度実行します。

コマンドが正常に終了したら OS 再起動します。

```
$ sudo shutdown -r now
```

再起動されるのは Debian だけです。再起動開始でターミナルが消えるので、再度開きます。

```
$ cat /etc/issue
Debian GNU/Linux 10 \n \l
```

無事にアップグレードできました。

記事では 2時間30分くらいかかるかもとのことでしたが、回線状態が良かったからなのか 30分くらいでできました。


Tag: debian ChromeOS Chromebook
