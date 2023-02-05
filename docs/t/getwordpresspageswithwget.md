# wget で Wordpress のサイトを丸ごとコピーする

Update: 2020-09-05


Wordpress で作られたサイトは特に手を加えなければ URL の末尾に ``?p=82`` みたいなものが付きます。これは Wordpress に限った話ではなくて Blog や Wiki 等であればたいていそうなっています。で、そんなサイトを一つ閉じることになって、その前に掲示している内容をコピーしようとしたのですが、そのサイトのアカウント情報がよくわかんなくなっていたので ``wget`` でコピーしておこうかと思ったのですが、 ``wget -m`` とすると ``?p=82`` みたいファイル名で保存されてしまいます。これではローカルで参照するのが面倒です。

いつものように「同じことで困った人はいるはず」と探してみるといました。

[Mirroring a wordpress website with wget](https://superuser.com/questions/721854/mirroring-a-wordpress-website-with-wget)

```
wget \
      --recursive \
      --no-clobber \
      --page-requisites \
      --html-extension \
      --convert-links \
      --restrict-file-names=windows $url-of-site
```

だそうです。なるほど ``--html-extension`` ですか。そんなオプションあったっけ？
と ``wget --help`` やってみたのですが、無いような。。。なぜ？
手もとにあるバージョンの wget で本当に動くのかな？
と心配になりつつ ``$url-of-site`` に URL 入れてやってみたらバッチリできましたよ。

というわけで、私が再度 ``wget --help`` やってもわからないし思い出せないことなので、ここにメモしておきます。

Tag: wget wordpress



