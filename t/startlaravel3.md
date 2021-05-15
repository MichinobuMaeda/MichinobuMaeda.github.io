Laraval 5 による開発の手順 #3
=====

Update: 2018-09-25


[Laraval 5 による開発の手順 #2](startlaravel2.html) の続きです。

## PHPUnit をインストールする

[Laraval 5 による開発の手順 #1](startlaravel1.html) に書いておけばよかったのですが、 unit test のために PHPUnit を使います。
Java の JUnit と同じようなものです。

私は Mac に Homebrew でインストールしました。
Windows にも Chocolatey というものがあるのですね。私は使ったことがありません。
オーソドックスなインストール手順は配布元の
[1. PHPUnit のインストール](https://phpunit.readthedocs.io/ja/latest/installation.html)
を見てください。

## メッセージを日本語化する

表示する言語を動的に変更して国際化するのであれば、
HTTP Request のヘッダやユーザが選んだ設定などをみる必要がありますが、
日本語だけに対応すればよいのであれば簡単です。

まず ``config/app.php`` の以下の値を ``ja`` に変更してください。
``JP`` ではありません。 ``JP`` は国、言語は ``ja`` で、 ``JA`` は農協です。
日本の場合、アイヌ語の言語コード ``ain``
が実際のところ使われていなくて知られていなくて（私も今知った）国と言語の区別が気になることはあまりないですが、
例えばカナダの場合、国は ``CA`` で言語は英語 ``en`` とフランス語 ``fr`` です。

```
    'locale' => 'ja',
    'fallback_locale' => 'ja',
```

プロジェクト作成直後の ``resources/views/welcome.blade.php`` は

```
<html lang="{%raw%}{{ app()->getLocale() }}{%endraw%}">
```

となっていますが、

```
<html lang="ja">
```

でいいです。

``resource/lang/en`` をコピーするか移動するかして ``resource/lang/ja`` を作ってください。
そして ``resource/lang/ja`` と ``resources/views``
の下の各ファイルをかんばって翻訳すると日本語で表示されるようなります。ただ、
``resource/lang/ja`` の下の量がすごくて。。。
テスト中に英語が出てきたら都度翻訳するこということでご勘弁を。

追記： ``resource/lang/ja`` の他に ``resource/lang/ja.json`` ファイルも必要です。
## 日時の表示を日本語化する

前回作ったところまでのサンプルにユーザを登録してデータベースに格納された値を見てみると、
テーブル ``users`` の ``created_at`` と ``updated_at`` がどう見ても JST ではありません。
``config/app.php`` は次のようになっています。

```
    'timezone' => 'UTC',
```

ドメスティックなお仕事をカネもらってやってるならこれを

```
    'timezone' => 'Asia/Tokyo',
```

に変更して「できました〜！」と済ませるところですが、
趣味やボランティアで真剣にやる場合はそういうわけにはいきません。
東京オリンピックのために夏時間を導入するとかいう話がありますし、
私がこれから作ろうとしているアプリは海外在住の人も使うんですよね。

システムが内部に保持するデータは UTC のまま、
表示だけ任意のタイムゾーンにすることにします。
言語の国際化はしない日本語のみの対応の予定なので、
フォーマットは日本式だけの対応ですませます。
各ユーザが自分用に選択したタイムゾーンで表示するようにします。

タイムゾーンはテーブル ``users`` のカラム ``timezone`` に格納します。
Laravel 5 の migration の仕組みでは後からカラムを追加することもできるのですが、
まだリリースしていないアプリなので ``database/migrations`` の ``CreateUsersTable`` を直接編集します。

```
            $table->string('password');
            $table->string('timezone')->nullable();
            $table->rememberToken();
            $table->timestamps();
```

``.env`` に以下のような設定を追加します。これらの設定は ``env()`` で取得できます。

```
APP_DEFAULT_TIMEZONE=Asia/Tokyo
APP_DATE_FORMAT=Y年n月j日
APP_TIME_FORMAT=G:i
APP_DATE_TIME_FORMAT='Y年n月j日 G:i'
APP_TIMESTAMP_FORMAT='Y-m-d H:i:s'
```

日時の値の格納には ``DateTime`` オブジェクトを使います。
Laravel 5 の Model はデフォルトの動作では timestamp 型のカラムの値を ``DateTime`` で返してくれないので、
それぞれの Model について以下のように timestamp 型のカラム名を指定しておいてください。

```
    /**
     * Get the attributes that should be converted to dates.
     *
     * @return array
     */
    public function getDates()
    {
        return array(
            'birthday',
            'created_at',
            'updated_at'
        );
    }
```

ビューヘルパーとして ``app/Services/ViewHelperService.php``
を作成し、その unit test のために
``tests/Unit/Services/ViewHelperServiceTest.php``
を作成します。

このビューヘルパーは Blade テンプレートの中で、例えば

```
@inject('vh', 'App\Services\ViewHelperService')
```

のように宣言してやると ``$vh`` として利用できます。

unit test は ``phpunit`` コマンドを実行すればよいです。
カバレッジを取得したい場合は、例えば

```
phpunit --coverage-html coverage
```

のようにすると ``coverage`` の下に HTML 形式のレポートが出力されます。この場合は
``.gitignore`` に ``/coverage`` を追加しておいてください。

----

ここまで作ったものは https://github.com/MichinobuMaeda/tamuro.git
のタグ ``startlaravel3`` です。チェックアウトの手順は
[Laraval 5 による開発の手順 #2](startlaravel2.html) の末尾をご参照ください。
``startlaravel2`` をチェックアウト済みであれば

```
git pull
git checkout tags/startlaravel3
```

としていただければいいです。

----

[Laraval 5 による開発の手順 #4](startlaravel4.html) に続く。

Tag: PHP Laravel localization
