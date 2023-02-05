# Google App Engine の BlobStore やメールなど

Update: 2012-01-22

※ 後でわかったことを追記しました ( 2012-01-22 )



昨年末、中学の同窓会の幹事さんから会員向けの写真置き場を何とかできないかとお願いされて Google App Engine で簡単なアプリを作ってみました。メールやバイナリデータの保存などいろいろな機能を使うことになったので、復習用に整理しておきます。作成したアプリのソースはそのままの形で公開できないので、興味のある人は以下の説明の中の断片をご参照ください。

## Google App Engine の概要を説明するとしたら

Google社が提供するアプリケーションの実行環境です。 PaaS の一種だという理解でいいと思います。ストレージ、CPU、ネットワークなどの使用量に応じて無料または有料で提供されています。ストレージについては 1GB のデータストアと 5GB のバイナリデータ専用のストア ( Blobstore ) が無料で利用できます。金出せばもっと使えます。 CPU とネットワークのクオータについては、今回はたいした量使わないことがわかっていたので見てません。



アプリケーションを呼び出すことができるのは HTTP Request だけです。定時実行のジョブのために Task Queue の API が提供されていますが、そこから例えば Python のスクリプトを直接呼び出すようなことはできません。 HTTP Request する必要があります。とはいえ、最初からそのつもりで設計すればさほど不便では無いと思います。



アプリケーションは負荷に応じて複数のサーバで実行されます。利用者はその辺意識しなくていいようです。ただし、利用されなければそのサーバの数はすぐ ( 数秒？ ) に 0個になってしまいます。 Java でフレームワークやライブラリをたくさん積むと、サーバ起動のために大きなオーバーヘッドがかかってしまうので注意が必要です。お金を出せば 0個にならない設定にもできるようです。



プロセス間で共有するデータは、データストアや memcache など提供された API を使って保存する必要があります。それ以外の手段でファイルなどを保存することはできません。とはいえ設定ファイルやテンプレートなど、アプリケーションの一部としてアップロードしたものを読むことはできます。例えば、 Java の Velocity などもだいじょうぶです。



データストアは RDB ではありません。 RDB も提供するというようなニュースを見たのですが、 2011年12月時点のドキュメントではまだ触れられていないようです（全部読んでないけど）。 Non SQL というとなにか新しい面倒なもののように思われるかもしれませんが、そこそこ親切な API が提供されているので苦労することは無いと思います。 Java 向けには JDO と JPA のインターフェースが提供されています。キーの扱いやエンティティ間の親子関係などが独特ですが、 RDB 使った開発でむやみやたらと複雑な SQL を書くのが好きな人でなければだいじょうぶ。



Blobstore はいまのところユーザがアップロードするもの専用です。プログラムで書き込む API は Java 用も Python 用も提供されていないようです（2011年12月の時点、全部読んでないけど）。根性で `multipart/form-data` を POST するプログラムを書けばなんとかなるかもしれません。Python の方のページには `from __future__ import ...` とかいうサンプルコードがあるけど、人柱になりそうなので見なかったことにします。



> 追記 2012-01-22  `from __future__ import with_statement` は python 2.5 で必要だけど、それ以降はいらなくて、ソースにこの記述が残っていたら無視される、とのことでした。サンプルコードは dev\_appserver 上で問題なく動きました。

## Python 2.7 の環境

現在 Experimental として提供されている Python 2.7 のランタイムの開発環境は、 SDK を入れただけではすべての機能を使うことができません。 "Using Python 2.7" のページをよく見てください。私の Mac OS X 10.7 の環境の場合 PIL がうまく動かなくてあきらめました。 Python 2.5 のランタイムを使っていた人は "What's New in Python 2.7" のページの自分に関係ありそうなところを見ておいた方がいいです。

## アップロードした画像のサムネイルを作成するには

Blobstore に格納した画像データのサムネイルを作成するために BlobKey を取得して `images.Image` のコンストラクタに渡して、とやってみたら、画像の縦横のサイズを取得する処理で「 BlobKey から生成した場合はできない」みたいなエラーが出てきます。作った人の気持ちは何となくわかります。代わりに `images.get_serving_url` で縮小画像を取得する URL を生成できます。それを使って URL Fetch して取得したものをそのまま使わせてもらうことにしました。


```
    url = images.get_serving_url(blob_key, size=240)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        entity.thumbnail = db.Blob(result.content)
        entity.put()
```



画像のヘッダだけ読み込んでそこから情報取得する方法もあるようです。今回は、あるサイズ以下の縮小画像ができさえすればよかったので、上記の簡単な処理で済ませました。



それから、アップロードしたファイルの名称が日本語の場合化けます。  `=?UTF-8?...` みたいに。管理機能の Blob Viewer では化けてません。 MIME デコードすればいいのかな？次のようにしてみましたが、完全には直りません。メールに添付した画像のファイル名はこの手順で対処できたのですが。



```
from email.header import decode_header

for decoded, enc in decode_header(filename):
    ...
```





`"abc 日本語のファイル名 def.jpg"` でアップロードしたものが `"abc 日本語のファ"` で切れてしまいます。おかしいです。さらに、テストプログラムを書いて、該当するデータの `BlobInfo` を取得して `filename` プロパティを見ると `"abc 日本語のファイル名 def.jpg"` です。なんだかとても変です。ファイルアップロードは `BlobstoreUploadHandler` を使って処理しているのですが、それを疑ってみます。ログ出力を追加してテストしてみると、そのハンドラの中で取得できている filename は `"=?ISO-2022-JP?B?YWJjIBskQkZ8S1w4bCROJVUlIRsoQg==?="` です。コマンドラインで python を起動してデコードしてみます。


```
>>> from email.header import decode_header
>>> decode_header('=?ISO-2022-JP?B?YWJjIBskQkZ8S1w4bCROJVUlIRsoQg==?=')
[('abc \x1b$BF|K\\8l$N%U%!\x1b(B', 'iso-2022-jp')]
```



短すぎます。そもそも `UTF-8` しか使っていないアプリなのになんで `ISO-2022-JP` が出てくるのか、さっぱりわかりません。 phthon 2.7 のランタイムの環境で、ここだけ `webapp2` ではなく `webapp` のライブラリを使うことになってるのが何となく不安だったのですが、深入りせず、別の方法で回避することにします。アップロードの処理が終わった後、最初にこの記事を表示する処理で `BlobInfo` を取得し直して、その filename プロパティを使うようにしました。



[http://code.google.com/p/googleappengine/issues/detail?id=2749](http://code.google.com/p/googleappengine/issues/detail?id=2749) にはファイル名以外のこともいろいろと。 JIS 2004 か、、、かかわりたくないなぁ。。。

## マルチパートのメールの処理

メールの送受信の基本的なところは "Mail Python API Overview" を見てください。受信したメールは HTTP リクエストに変換される仕組みになっています。基本的に英語のことしか考えていない作りになっているので、日本語のメールを送信したい場合は Python Standard Liblary の email package あたりを使って何とかしてください。今回は、写メとして送られてきた画像を登録する必要がありました。デコメとか絵文字とか面倒なものは非対応ということにしましたが、メール本文になにか書いてくれていたら説明として載せたいので、平文に限り取得することにしました。

```
    for content_type, body in msg.bodies('text/plain'):
         ...
        text = body.decode()
```


という感じで。日本語は特に問題なしでした。ただ、その、テストに使った日本語のメールが、 UTF-8 だったのか ISO-2022-JP だったのかはよくわかりません。添付された画像ファイルについては、ほとんどの携帯はこれでなんとかなるでしょう。


```
    for filename, data in msg.attachments:
        if filename.endswith('jpg') or filename.endswith('JPG'):
             ...
```

## タイムスタンプ

画像を登録した日時などを記録するために、JST のタイムスタンプが欲しかったのですが、 Python のタイムゾーンの扱いがよくわからなかったので、以下のような反則で済ませてしまいました。



```
datetime.datetime.utcnow() + datetime.timedelta(hours=9)
```



> 追記 2012-01-22 : 次のような datetime.tzinfo のサブクラスを作るといいようです。 [http://timezones.appspot.com/](http://timezones.appspot.com/) 参照。

```
    class UtcTzinfo(datetime.tzinfo):
        def utcoffset(self, dt):`
            return datetime.timedelta(0)`
        def dst(self, dt):`
            return datetime.timedelta(0)`
        def tzname(self, dt):`
            return 'UTC'`
        def olsen_name(self):`
            return 'UTC'`

    class JstTzinfo(datetime.tzinfo):`
        def utcoffset(self, dt):`
            return datetime.timedelta(hours=9)`
        def dst(self, dt):`
            return datetime.timedelta(0)`
        def tzname(self, dt):`
            return 'JST'`
        def olsen_name(self):`
            return 'Asia/Tokyo'`
```

> タイムゾーン無しの datetime.datetime オブジェクトを JST に変換しようとすると "native はダメ" みたいなメッセージが出てくるので、こんなふうにやってみたらうまくいきました。

```
native.replace(tzinfo=UtcTzinfo()).astimezone(JstTzinfo())
```


## 永続データの使用量を見る

データストアの使用量は `stats.GlobalStat.all().get()` で統計情報のエンティティを取得して `bytes` プロパティの値を見ます。開発環境では統計情報のエンティティが取得できなかったのですが、本番環境ではうまくいきました。もしかすると、本番環境でも、アプリケーションを登録した直後などは統計情報のエンティティを取得できないかもしれません。



> 追記 2012-01-22 : dev\_appserver の管理画面に "Datastore Stats Generator" というものがありました。



Blobstore に格納したデータのサイズの合計を見るのは簡単です。


```
    blob_size = 0
    for blob_info in blobstore.BlobInfo.all():
        blob_size = blob_size + blob_info.size
```



ただし、データ本体以外にメタデータなどのオーバーヘッドがあると思います。

Blobsotre の統計情報を取得する API は見つけられませんでした（あまりまじめに探していないのですが）。
