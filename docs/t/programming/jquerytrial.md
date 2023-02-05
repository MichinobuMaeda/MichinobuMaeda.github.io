# 整理中：jQuery 日記

Update: 2011-01-24

## 2010-07-03 ちょいと試す

参考にした本は「JavaScript + jQuery ベーシックマスター」 ISBN978-4-7678-0956-4 です。何はともあれ [http://jquery.com/](http://jquery.com/) から jquery-1.4.2.min.js をダウンロードして試してみます。練習の課題にするのは、以前 prototype.js で作った 郵便番号データを利用する機能 と同じようなもの。要素のイベントを設定したり、受信した JSON データで選択リストを作ってみたりします。とりあえず、都道府県のリストだけ生成する簡単なプログラムを。素の機能の使い勝手を比べてみたかんじ prototype.js より簡単そうです。



今日のところはとりあえずこんな感じ。



`<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"`

 `"http://www.w3.org/TR/html4/loose.dtd">`

`<html>`

 `<head>`

 `<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">`

 `<title>郵便番号JSON細切れデータを jQury で利用するサンプル</title>`

 `<link rel="stylesheet" type="text/css" href="jquery-json.css" />`

 `<script type="text/javascript" charset="UTF-8" src="jqueryui/js/jquery-1.4.2.min.js"></script>`

 `<script type="text/javascript" charset="UTF-8" src="jquery-json.js"></script>`

 `</head>`

 `<body>`

 `<div id="content">`

 `<div id="header">`

 `<h1></h1>`

 `<div id="breadcrumb"><a href="/">Top</a> » <a href="./">サンプル</a></div>`

 `</div>`

 `<div id="body">`

 `<form id="main">`

 `<div>`

 `<span class="title">郵便番号</span>`

 `<input type="text" id="zip1" name="zip1" value="" maxlength="3" />`

 `-`

 `<input type="text" id="zip2" name="zip2" value="" maxlength="4" />`

 `</div>`

 `<div>`

 `<span class="title">都道府県</span>`

 `<input type="text" id="pref" name="pref" value="" />`

 `</div>`

 `<div>`

 `<span class="title">市区町村</span>`

 `<input type="text" id="city" name="city" value="" />`

 `</div>`

 `<div>`

 `<span class="title">住所１</span>`

 `<input type="text" id="add1" name="add1" value="" />`

 `</div>`

 `<div>`

 `<span class="title">住所２</span>`

 `<input type="text" id="add2" name="add2" value="" />`

 `</div>`

 `<div>`

 `<span class="title">事業所</span>`

 `<input type="text" id="corp" name="corp" value="" />`

 `</div>`

 `<div>`

 `<span class="title">&nbsp;</span>`

 `<input type="reset" id="reset" name="reset" value="リセット" />`

 `</div>`

 `</form>`

 `</div>`

 `<div id="footer">`

 `<div id="copyright">Copyright <span id="crYear"></span> Michinobu Maeda.</div>`

 `</div>`

 `</div>`

 `</body>`

`</html>`



`$(function () {`

 `// h1 には title と同じ内容を設定する。`

 `$('h1').append($('title').text());`

 `// Copyright の年を計算して設定する。`

 `var crYear = 2010;`

 `var crNow = new Date().getYear() + 1900;`

 `if (crYear == (crNow - 1)) {`

 `crYear += ',' + crNow;`

 `} else if (crYear < crNow) {`

 `crYear += '-' + crNow;`

 `}`

 `$('#crYear').append(crYear);`

 `// 都道府県の選択リストを作成する。`

 `$.ajax ({`

 `url: '/data/json/pref/prefs.json',`

 `success: function(data) {`

 `$('#pref').replaceWith(`

 `'<select id="pref" name="pref">' +`

 `'<option value="-" selected>-- 選択してください --</option>' +`

 `'</select>');`

 `for (i = 0; i < data.length; ++i) {`

 `$('#pref').append(`

 `'<option value="' + data[i].x0401 + '">' + data[i].name + '</option>');`

 `}`

 `}`

 `});`

`});`

## 2010-07-05 jQuery UI を入れてみる

あうちっ！ お勉強中の JavaScript のソース消しちゃったよ。でもあわてない、こんなときのために自分一人のために立てた Subversion のリポジトリ（汗）から復旧！ Eclipse のローカルヒストリーからさらに最新に復旧！ 安心安心。



さてと、まず [http://jqueryui.com/](http://jqueryui.com/) から一式ダウンロードします。なにやらいろいろオプションが選べるようなのですが、デフォルトのままダウンロード。自分の作業環境の適当なところにおいて、参考書に書いてある順番で CSS と JavaScript を読み込むよう HTML のソースを変更します。



すると、自分が作ったページがいきなりかっこよくなるのか？と思ったけど、全く変わりません。既存の CSS の設定には影響しないようになっているようです。



development-bundle ディレクトリは、、、よくわからないけどとりあえず消しておこう。

## 2010-07-07 先頭のテキストボックスにフォーカスをあてる

[Set Focus to the First TextBox on a Page using jQuery](http://www.devcurry.com/2009/09/set-focus-to-first-textbox-on-page.html) によると

 `// 先頭のテキストボックスにフォーカスをあてる。`

 `$("input[type='text']:enabled:first").focus();`



だそうな。こりゃいいや。

## 2010-07-07 フォーカス On/Off で背景色を変える

まとめて複数の要素を指定できるのがうれしい。



 `$('#zip1, #zip2, #pref, #city, #add1, #add2, #corp').focus(function() {`

 `$(this).css('background', '#ffa');`

 `});`

 `$('#zip1, #zip2, #pref, #city, #add1, #add2, #corp').blur(function() {`

 `$(this).css('background', '#fff');`

 `});`

## 2010-07-11 IE でうまくいかないことが

この部分が IE ではうまく動いてくれませんでした。どうしても JavaScript にさせたい処理ではないので削除しました。



`// h1 には title と同じ内容を設定する。`

`$('h1').append($('title').text());`



それから、次のような処理もエラーになりました。



`$('#addListDialog').dialog('option', 'width', window.innerWidth * 0.9);`



Safari, FireFox, Opera, Chrome すべてだいじょうぶなんだけどなぁ。



あと、キーイベントの処理で微妙な違いが。これは後で解決できたとしても、文章にするのは難しいかもしれないなぁ。

## 2010-07-11 最初のサンプル公開

郵便番号を 7桁全部入力したら、その候補を探しに行って、あれば選択リストを表示する、というサンプルを公開しました。



http://www.zippyzip.jp/sample/jquery-json.html ( 閉鎖 )



使用しているデータについては http://www.zippyzip.jp/ ( 閉鎖 ) の説明を見てください。私が趣味で作成している独自のものです。日本郵便が配布しているデータを基に、毎月自動で更新しています。

### 2011-01-24 追記

サンプルはこちらに移動しました。

[http://code.google.com/p/zippyzipjp/](http://code.google.com/p/zippyzipjp/)
