# Geeklog

Update: 2008-01-22

このサイトを以前 Geeklog で構築したときの記録です。

## 使用開始



なんでいろいろある中で Geeklog をってところから説明しますね。



昨日から Geeklog というフリーの CMS ( Content Management System ) を使ってこの Webサイトを作り直しております。以前だいたい同じ範囲の機能を持つ Xoops を使ってみたことがあるのですが、なんでやめたかというと面倒だから。高度にモジュール化されて高機能で細かく管理できるのですが、仕事モードならともかくプライベート・モードの私にはそれを理解するのはたいへんです。このサイトから Xoops を撤去した後も Web Computer Union (既に閉鎖) 用にPC/携帯対応モジュールなど作ってみたりしたのですが、まるごと携帯対応は私の力ではとても無理、そして Xoops の日本の(?)分家 Cube はなんとなく多難な前途を抱えているような気がするし（ほんとうに「なんとなくです」関係者のみなさんごめんなさい、と謝るくらいなら書くなという内容ですが）で、他のものを探しているうちに日本語版で携帯主要３事業者対応やってしまっている Geeklog にたどりついたわけです。



いまのところ極力避けたいと考えているのですが、もし、カスタマイズなどやるとして、ソースは Geeklog の方がきれいですね、というか、 Xoops のがきたないですね。これについては謝る気はありません。だって本当にすごいコードだから。

## テーマ入れ替え

2008-05-18



CMS の使用をやめて静的なページにした時期もあったのですが、テーマを入れ替えて Geeklog の利用を再開しました。



Geeklog のテーマの入れ替えの作業は Xoops と同じくらい簡単です。テーマエディタのリストに追加したテーマが出てこないのは… `geeklog/plugins/themedit/config.php` に設定追加すると選択できるようになりました。



CSS 、テンプレート、コンフィギュレーションなどを変更しましたが、今のところ Hack は無しです。 [カスタム関数](http://wiki.geeklog.jp/index.php/Lib_custom) という仕組みもあるのですがこれもまだ使っていません。カスタマイズの手段は Xoops より細かく用意されているようです。私の場合ついついソースから追っかけてしまうのですが、ソースは見たくない人、英語は苦手でない人は先に本家サイト英語版 [Documentation](http://www.geeklog.net/docs/) を見ておくといいでしょう。



この文章を書いている最中に気がついたのですが、アドバンストエディタで Webブラウザ上のリンクをコピペすると自動でリンクになります。この機能は Mac の Firefox のページから Firefox へのコピーでは有効、 Safari から Firefox ではうまくいかずテキストとして貼付けられました。

## サイトマップ・プラグイン導入

2009-05-06



[Geeklog 日本公式サイト](http://www.geeklog.jp/) で使われているのと同じものです。



[Geeklog増殖計画](http://mystral-kk.net/) から入手しました。 [サイトマッププラグイン(Sitemap plugin)](http://mystral-kk.net/filemgmt/index.php?id=18) の説明のページに書かれているように、このプラグインを導入する前に [Dataproxyプラグイン(Dataproxy plugin)](http://mystral-kk.net/filemgmt/index.php?id=17) を導入する必要があります。インストールの手順は、それぞれのパッケージの `/admin/install_ja.html` に書いてあるとおりです。



あわせて、このページの上のメニューバーの 過去記事 ( 閉鎖 ) を サイトマップ ( 閉鎖 ) に変更しました。あまり手をかけずに設置できて、機能も十分で、いいかんじです。
