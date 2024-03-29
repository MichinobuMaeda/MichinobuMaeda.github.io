# Google App Engine に大きなデータを入れる

Update: 2010-10-10



> 追記 : 2012-12-23 今は無料コースでも BlogStore が使えるので、こんな面倒なことはしなくてだいじょうぶです。



郵便番号データを加工するプログラムを Google App Engine 上で構築しようとしているのですが、無料でどうにかするためには一つ大きな問題があります。日本郵便が配布しているデータをどうやって保存するか。 LZH ファイルのサイズは全県データが 2MB 弱、事業所データが 1MB 弱です。 LZH 形式のアーカイブファイルをそのまま BLOB として保存できれば簡単なのですが、１日当たり 1$ 以上の有料コースとなるようです。 byte 型の配列で保存することはできません。 500を超えるサイズは拒否されます。 16進や base64 にして String で保存することもできません。これも 500 文字を超えるデータは拒否されます。そもそも１オブジェクト当たり 1MB の制限がありますから文字列に変換すると確実にオーバーしてしまいます。



苦肉の策として、解凍て取り出した CSV ファイルを行毎にバラバラにして LinkedList にして保存することにしました。まず CSV ファイルを適当な行数で分割します。試しに、確実にサイズオーバーしそうにない 2,000行毎に１オブジェクトにして保存すると OK でした。分割したものには共通の識別と順序を付与しておけばいいです。



JDO によるデータ取り扱いはめちゃめちゃ簡単です。 Using the Datastore with JDO に書いてあるとおりです。私が少しはまったのは PersistenceManagerFactory の取り扱いをこのページに書いてあるとおりにしなかったことだけ。なんで、 Spring Framework で Singleton 指定したインスタンスの変数の初期化が２回実行されたような現象が出るかなぁ。。。よくわからないけど、とにかくこのページに書いてあるとおりクラス変数にすると正常に動きました。



2010-10-16 追記



LZH を解凍してテキストファイルを取り出して入れる方法でも CPU 使用の制限に引っかかってしまいました。また、過去のデータまで全部入れようとするとディスク容量が足りなくなる可能性があります。



そこで、 [http://iharder.net/base64](http://iharder.net/base64) が配布しているクラス（ファイル１個だけ配布している）を使って LZH を base64 エンコードして保存することにしました。 base64 encoder / decoder のライブラリとしては Apache Commons codec も試してみましたが、こちらのファイル１個だけの方が使い勝手がいいです。



元のデータを 320byte ずつエンコードします。エンコード後のサイズはその 4/3 倍、つまり 480byte になるはずです。 これを String で保存すると 500文字の制限をクリアできます。



訂正： 480byte の 3/4 は 360byte でした。既に本番環境に 320byte ごとに分割したデータを保存してしまったので、そのまま運用しています。



1MB の制限についてですが、 Google App Engine のデータストアの内部の文字コードがなんなのかがよくわかりません。ローカルのテスト環境の WEB-INF/appengine-generated/local\_db.bin をみたところ、アルファベットは ASCII と同じコード値で保存されているようです。 UTF-8 を使っているのかな？ いずれにしても、 base64 エンコード後の String は、単純に文字数と同じバイト数になるようです。であれば、 2048件は保存できそうです。



これを LinkedList<String> にして保存してみたところ、テスト環境も本番環境も問題ありませんでした。
