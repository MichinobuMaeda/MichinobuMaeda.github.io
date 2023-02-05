# PukiWiki で普通のサイトを作る

Update: 2008-12-30



[PukiWiki](http://pukiwiki.sourceforge.jp/) で Wiki じゃない普通のサイトを作りました [IT業界の法令遵守をすすめよう!!](http://www.union-net.or.jp/compliance/) 。簡単です。 Wiki らしい機能を画面上から隠して、編集済みのページを凍結するだけです。



PukiWiki のインストール手順は [PukiWikiのインストール](http://pukiwiki.sourceforge.jp/?PukiWiki%2FInstall) を見てください。その他 PukiWiki の一般的な情報は [はじめてのPukiWiki](http://pukiwiki.sourceforge.jp/?%E3%81%AF%E3%81%98%E3%82%81%E3%81%A6%E3%81%AEPukiWiki) や [FAQ](http://pukiwiki.sourceforge.jp/?FAQ) などを見てください。



PukiWiki の見た目をカスタマイズするには、次の 3個のファイルを編集します。



- `pukiwiki.ini.php`
- `skin/pukiwiki.skin.php`
- `skin/pukiwiki.css.php`



これらのファイルの内容と、実際の表示を見比べながらの地道な作業になります。でも、掲示板や Blog の形式の CMS に比べて仕組みが単純なので、かなり大胆に変更してもだいじょうぶです。その他、画像なども必要に応じて追加変更します。



私自身は HTML を直接書くのは苦にならなくて、いま、この記事も HTML モードで書いているのですが、そんな私でも Wiki の編集画面の方が楽だと感じます。文章は普通に書けばいいです。 `[[ ]]` の使い方を覚えれば、新しいページとそのページへのリンクができます。その他、画像の貼り付け方、番号有・無のリスト、見出し、表組みなどの書き方が理解できれば十分です。 PukiWiki をインストールすると、ヘルプと練習ページもついてくるので有効活用してください。私は入門書など無しで済ませました。



デザイナーなどがカスタマイズしてサイトを準備して、サイトのオーナーが自分で内容を更新するといった使い方ができると思います。



Wiki パッケージとしては WikiPedia に使われている [MediaWiki](http://www.mediawiki.org/wiki/MediaWiki/ja) もあります。こちらの方が高機能なようです。試してはいないのですが、カスタマイズして使う場合、高機能な方が手間がかかると思います。変更が影響を及ぼす範囲の確認の作業が増えるからです。 Wiki の本来の用途のために使う場合は好きな方でいいと思います。また、組織内の情報蓄積・整理の用途に特化した Enterprise Wiki というものもあります。フリーの [TWiki](http://twiki.org/) などが有名です。。。とはいっても私も使ったことがないし、 Enterprise Wiki を知っている人の中では有名ということです。
