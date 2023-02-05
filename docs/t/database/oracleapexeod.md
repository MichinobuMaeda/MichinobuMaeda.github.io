# 簡単開発：Oracle APEX

Update: 2008-12-30

https://picasaweb.google.com/105998202054304028324/A?authkey=Gv1sRgCMT4w9mvnqfMfQ#5565386323851339106



仕事で Oracle社の APEX ( Application Express 、旧 HTML DB ) を使うことになったので、予習してみました。 APEX は Oracle DataBase 11g にセットで入っています。 HTML 版の Microsoft Access のようなものです。

## インストールは簡単ではない

まず、十分なスペックの PC を用意します。 Celeron のノートPCではまともに動きませんでした。 Intel Core 2 Duo くらいでないと CPU 能力が足りないと思います。私は AMD Athron 64 X2 Dual Core 5200+ の PC を使いました。メモリは、 OS が使う分を除いて 500MB 以上、できれば 1GB 以上欲しいです。



次に、 Oracle DataBase 11g をインストールします。今回は APEX の試用だけが目的なので、「基本インストール」の「初期データベース作成」有効でインストールしました。Oracleベースは `C:\app\oracle` としました。



!https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5WeV4l9I/AAAAAAAABqU/wCpNu98Wu-I/eodoracleapex_1_original.gif



初心者の場合、別のバージョンの Oracle がすでに入っている環境、もしくは、入っていた環境にトラブルなくインストールするのは困難です。1個のコンピュータに Oracle のシステムを複数インストールすることに慣れている人も、リスナーにサービスを動的に登録できる状態しておくといったことに気をつけてください。。。というような話がよくわからない場合は、とにかく、まっさらの PC にすべてデフォルトでインストールしてください。



Windows ファイアウォールやその他のセキュリティ製品によるポートの利用の制限が有効になっている場合は、穴あけてください。次のポートや `oracle.exe` を例外扱いにすればいいようです。

*   1521 : Net8
*   1158 : Enterprise Manager
*   8080 : XML DB

ポート番号はいずれもデフォルト値です。



GUI のインストーラによるインストールが終わって、普通に Oracle が動いていることを確認したら、 [4.5 Oracle Application Expressのインストール後の作業](http://otndnld.oracle.co.jp/document/products/oracle11g/111/windows/E05878-04/postcfg.htm#BCGICBCF) にしたがって APEX を設定します。 HTTP サーバは「埋込みPL/SQLゲートウェイ」を選択してください。次の項を見てください。

*   4.5.3.1 新規インストールまたはデータベースのアップグレード時の埋込みPL/SQLゲートウェイの構成
*   4.5.3.2 Oracle XML DB HTTPサーバーの無効化および有効化
*   4.5.6 Oracle Database 11gのネットワーク・サービスの有効化
*   4.5.7 その他の言語によるOracle Application Expressの実行について

「 Oracle HTTP Server 」のインストールはかなり面倒なので、こちらを選択することはおすすめできません。



「 4.5.7 」では、化けた文字が大量に画面に表示されますが、コマンドプロンプト上に UTF-8 で表示しているので、文字化けするのが正しいです。ここまでの作業が終わったら、コマンドプロンプトで次のコマンドを実行してください


```
lsnrctl status
```


次のようにポート 8080 が登録されていれば OK です。


```
リスニング・エンドポイントのサマリー...
 (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(PIPENAME=\\.\pipe\EXTPROC1521ipc)))
 (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=192.168.0.51)(PORT=1521)))
 (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=blueberry)(PORT=8080))(
Presentation=HTTP)(Session=RAW))
```


HOST パラメータの値が IPアドレスになっている行とホスト名になっている行が混じっているのですが、気にせず先に進みます。

## 使ってみる

管理者のログインはこの  `http://localhost:8080/apex/apex_admin` です。初めて開くときには時間がかかります。「 4.5.7 」で正しく日本語環境が設定されていれば、この画面は日本語で表示されます。ユーザ名「 ADMIN 」、パスワードは「 4.5.3.1 」で設定したパスワードです。

### 作業領域の作成

管理ホームでメニュー「作業領域の管理」－「作業領域の管理」－「作業領域の作成」を選びます。それから、画面の指示に従って、作業領域名、スキーマ名 ( Oracle のユーザ名 ) と領域割り当て制限のサイズなど入力して、新しい作業領域を作成します。

### 作業開始

実際に仕事で使う場合は、ここで開発者やユーザを登録することになるのですが、 `ADMIN` のまま作業を続けます。まず、ログアウトして、 `http://localhost:8080/apex` で作業領域を指定してログインしなおします。



ホームでメニュー「オブジェクト・ブラウザ」－「作成」－「表」を選択し、アプリケーションで使う表を作成します。ウィザード形式で、主キーの値を割り当てる順序を指定したりできます。



ホームでメニュー「アプリケーション・ビルダー」－「アプリケーションの作成」－「アプリケーションの作成」を選択します。ウィザード形式になっているので、画面の指示に従って進んでいくと、できました、数分で、こんなものが。「ページのタイプ」は「フォーム」を選択しました。





https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5XDEbeyI/AAAAAAAABqY/XHI_6_TFhrc/s1600/eodoracleapex_2_original.gif



とりあえず、ここで、データを２件ほど登録してみます。



ホームに戻ってメニュー「アプリケーション・ビルダー」－「アプリケーションの表示」を選択して、先ほど作成したアプリケーションを選択します。次に「ページの作成」ボタンを押します。「ページのタイプ」レポートを選択して、で、なんだかよくわからない設定項目はそのままにして、クエリ・ビルダで SQL を生成してウィザードのページをどんどん進んでいくとこんなのができました。今度は 1分くらいです。



https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5X_b55WI/AAAAAAAABqc/LalNrmvtbvk/s1600/eodoracleapex_3_original.gif



画面の上のほうのタブ、無しとか階層構造とか選べるようなのですが、まだ、その辺の決まりがよくわかりません。でも、まぁ、期待したとおりにできたからいいや。
