整理中：Javascript の Object と Map

久しぶりに、JSON を扱うプログラムを書いてみようと思い立ったものの、すっかり Javascript のことを忘れています。最初、

`[{"code":"01","name":"北海道"},...]`

のような都道府県コードのデータを用意して、と考えました。

`<prefectures><prefecture><code>01</code><name>北海道</name></prefecture>...</prefectures>`

という XML を JSON に置き換えてみたわけです。しかしながらネットでやりとりするには少しでも小さい方がいいです。で、次に、

`{"01":"北海道",...}`

と縮めていじょうぶなのかと考えてみたわけです。 Javascript のプログラムの中で

`var test2 = {"01":"北海道","13":"東京都","47":"沖縄県"};`

document.write("<p>" + test2\["01"\] + "</p>");
document.write("<p>" + test2\["47"\] + "</p>");

と場合は問題ないのですが、オブジェクトのプロパティとして

`document.write("<p>" + test2.13 + "</p>");`

というように使うことはできないですね。少し変えてみます。

`{"p01":"北海道",...}`

これなら問題なさそうです。

var test2 = {"p01":"北海道","p13":"東京都","p47":"沖縄県"};

document.write("<p>" + test2\["p01"\] + "</p>");

document.write("<p>" + test2\["p02"\] + "</p>");

document.write("<p>" + test2.p13 + "</p>");

document.write("<p>" + test2.p14 + "</p>");

document.write("<p>" + test2\["p47"\] + "</p>");

for (code in test2) {

    document.write("<p>" + code + " : " + test2\[code\] + "</p>");

}

上のサンプルコードの出力結果は次の通り。

`北海道`

`undefined`

`東京都`

`undefined`

`沖縄県`

`p01 : 北海道`

`p13 : 東京都`

`p47 : 沖縄県`

これは次のサンプルコードと実質同等なわけですね。出力結果も全く同じです。

`var test2 = new Object();`

`test2.p01 = "北海道";`

`test2.p13 = "東京都";`

`test2.p47 = "沖縄県";`

`document.write("<p>" + test2["p01"] + "</p>");`

`document.write("<p>" + test2["p02"] + "</p>");`

`document.write("<p>" + test2.p13 + "</p>");`

`document.write("<p>" + test2.p14 + "</p>");`

`document.write("<p>" + test2["p47"] + "</p>");`

`for (code in test2) {`

 `document.write("<p>" + code + " : " + test2[code] + "</p>");`

`}`

余談ですが、ネットでこのあたりのサンプルコード調べていると、他の言語と同じように `.keys()` メソッドでキー値の一覧を取得できる形にするには、というようなものが出てましたが、処理量増えるだけだし `for ( in )` で取得できるのはキー値の方ということでいいんじゃないかな。
