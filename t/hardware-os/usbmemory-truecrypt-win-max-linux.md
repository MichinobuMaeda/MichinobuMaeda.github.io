USBメモリを無料で暗号化
=====

Update: 2012-09-02

> 追記 2021-05-15: TrueCrypt はメンテナンスが止まっています。後継のツールとして
[VeraCrypt](https://veracrypt.fr/en/Home.html) などがあります。

おまけのついていない安い USBメモリを暗号化したい、 Windows でも Mac でも Linux でも使いたい、という私の贅沢な悩みを解決するツールを見つけました。 TrueCrypt [http://www.truecrypt.org/](http://www.truecrypt.org/) というフリーソフトです。 Vector 新着ソフトウェアレビュー [http://www.vector.co.jp/magazine/softnews/110831/n1108311\_reviewer.html](http://www.vector.co.jp/magazine/softnews/110831/n1108311_reviewer.html) でも紹介されていました。

さっそく Windows と Mac と Linux で試してみました。。。って PC 何台持っているのかって？ ここで使ったのは１台ですっ！！ で、ここで使わなかったのは何台かって？ いやそれは、まあ、それは置いといて (L- -)L Windows 版のインストールの手順と私の場合の使い方について説明します。

前提知識としては、暗号化しているしていないにかかわらず、USB メモリを PC からいきなり抜いたらダメということくらいかな。知らない場合は、周りの知ってそうな人にこっそり聞いてみてください。

ダウンロードは上記の Vector からでもいいし、配布元 [http://www.truecrypt.org/downloads](http://www.truecrypt.org/downloads) からでもいいです。ダウンロードした2012年9月1日現在の最新版 `TrueCrypt Setup 7.1a.exe` を実行します。

![](usbmemory-truecrypt-win-max-linux/8902b26a825eb02d49525b8344a1c54c.png)]

下の方の `I accept ...` のチェックを入れて、後はデフォルトの設定でどんどん進めてください。インストールが終わったら、Windows メニューの TruCriypt から起動してください。起動したら日本語化の設定をします。

![](usbmemory-truecrypt-win-max-linux/3f923b18ae3469454ab418b8a96fe1bc.png)

メニューの Settings の `Language...` を選択してください。

![](usbmemory-truecrypt-win-max-linux/680c9ad891763570a13f0c3b595ff2a2.png)

まだ English だけしかありません。下の方の `Download Language pack` をクリックしてください。ブラウザ ( インターネットエクスプローラとか、 FireFox とか ) でダウンロードページが表示されます。もしうまくいかないようなら [http://www.truecrypt.org/localizations](http://www.truecrypt.org/localizations) を開いてください。たくさんの言語が並んでいますが、その中から日本語のファイルをダウンロードしてください。 `langpack-ja-1.0.0-for-truecrypt-7.1a.zip` のようなファイル名です。ファイルを解凍すると、

*   `Language.ja.xml`
*   `Readme.txt`

というファイルが入っています。 Readme.txt の方に説明が書いてあります。英語で。要するに、 TrueCrypt をインストールしたフォルダ ( インストールの際に等に変更していなければ `C:\Program Files\TrueCrypt` ) に Language.ja.xml を入れろということだそうです。 TrueCrypt をいったん終了して、 Language.ja.xml を C:\\Program Files\\TrueCrypt にコピーして、 メニューの Settings の Language... をもう一度。


![](usbmemory-truecrypt-win-max-linux/4aed7e3dbf33c4ed591d54f7a89ed19d.png)]

「日本語」が出てきたので、マウスで「日本語」を選択して OK ボタンを押します。するとメニューなどが日本語になります。日本語訳担当は Ogoshi Masayuki さんだそうです。

![](usbmemory-truecrypt-win-max-linux/0eca6cd901428ddab7cf86e927f9a2b0.png)

ここまででインストールは完了です。次に、私が昨日買った安めの USB メモリを丸ごと暗号化してみます。 Mac と Linux でも使い方はほとんど同じです。

まずはその USB メモリを突っ込みます。その USB メモリは `F:` ドライブになりました。このあたりはみなさんの PC の状態によって違います。すると、先ほどまで TrueCrypt の一番上に表示されていた `F:` が消えました。

![](usbmemory-truecrypt-win-max-linux/0cb6c11d4438f42f317517fddbe72e4d.png)

「ボリュームの作成」ボタンを押します。

![](usbmemory-truecrypt-win-max-linux/2867f1bca50ae6f3a1b4c62ce8230c07.png)

今回は「非システムパーティション/ドライブを暗号化」を選びました。

![](usbmemory-truecrypt-win-max-linux/21bdfe139a72264ebf8d287bf6f6c052.png)
説明を見たところ「隠しボリューム」は使うのに少々手間がかかるようだし、命と引き替えにするほどの大事なデータを預かる予定はないので、「 TrueCrypt 標準ボリューム」を選びました。

![](usbmemory-truecrypt-win-max-linux/b869505749703c1bb82d5b2cb3a46c29.png)

「デバイスの選択」ボタンを押して、 F: ドライブの USB メモリを指定します。

![](usbmemory-truecrypt-win-max-linux/04c3bb9b87f767849a7416fb57b79688.png)

なんだか難しいことが書いてありますが、気にせず「次へ」。

![](usbmemory-truecrypt-win-max-linux/c6ee103d3b5734240661258e9e7d9f54.png)

USB メモリは空だったので、「暗号化ボリュームを作成してフォーマット」を選択しました。

![](usbmemory-truecrypt-win-max-linux/c96efc0a4a7d5373f4758db4173ce91d.png)

暗号化のアルゴリズムについては、特にこだわりは無いので、デフォルトのままにしました。

![](usbmemory-truecrypt-win-max-linux/e3b80cbc3339d7b031d51f15cd443b61.png)

サイズについては選択の余地はありません。とにかく丸ごと全部です。

![](usbmemory-truecrypt-win-max-linux/28c1a58bc9a407f8c4b0cdeb69e08449.png)

パスワードは長い方がいいです。キーファイルを併用するとさらにいいのですが、キーファイルを無くすと暗号化の解除のしようが無くなってしまうので、管理に自信がある場合だけにした方がいいです。

![](usbmemory-truecrypt-win-max-linux/54e4eefc0d6ed16658876f4ab638562e.png)

パスワードが短いとおこられます。

![](usbmemory-truecrypt-win-max-linux/bdc86fa2a4f86d1bb3b3b21c5e4a36e5.png)

4GB を超えるような巨大なファイルを扱うことはあり得ないので、「いいえ」を選択しました。「はい」を選択するのは、ファイルシステム等々について知識がある人だけにしてください。

![](usbmemory-truecrypt-win-max-linux/a222e7fc5cc7ddcaa3d46cf1d3b4a538.png)

ファイルシステムは FAT を選びました。 NTFS を選択するのは、そのあたりの知識がある人だけにしてください。それから、特に急いでいる場合は別にして、「クイックフォーマット」は選ばない方がいいようです。今回の場合フォーマットに 15分くらい時間がかかりました。

![](usbmemory-truecrypt-win-max-linux/39c5c237e2314c9a25c2e48125767d40.png)

これで USB メモリの暗号化が完了しました。

試す前に、 USB メモリを抜いて、差し込み直してみます。

![](usbmemory-truecrypt-win-max-linux/309d3bc1006312b4bfdd0ceec8e53554.png)

なるほど、これが出るから「暗号化されたファイルコンテナを作成」の方を初心者に勧めているわけですね。ここでフォーマットしてはいけません。「キャンセル」します。

![](usbmemory-truecrypt-win-max-linux/0cb6c11d4438f42f317517fddbe72e4d.png)

どれでもいいのですが、空いているドライブ、上記の例の場合 H: を選んで「マウント」ボタンを押します。

![](usbmemory-truecrypt-win-max-linux/a5dfb4f080c5ad2c60f618cbb5378feb.png)

パスワードを入力して、「キーファイル」ボタンを押してキーファイルを指定して、 OK します。

![](usbmemory-truecrypt-win-max-linux/1e5555bce8a36ac6e4e2fafad81250ab.png)

これで、暗号化した USB メモリが `H:` ドライブで使えるようになりました。 `F:` ドライブではありません。「マウント」ボタンの名前が「アンマウント」に変わっています。暗号化したドライブを使い終わったら、必ず「アンマウント」ボタンをして、さらに、 `F:` ドライブの接続も解除してから USB メモリを抜いてください。
