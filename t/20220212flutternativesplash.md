# Flutter アプリの起動時にロゴなど表示する

Update: 2022-02-12

Flutter のアプリを起動した後しばらく真っ白の状態になるのはなんとかできないものかと思っていたのですが、簡単に解決できますね。少し真面目探したらすぐに
[flutter_native_splash](https://pub.dev/packages/flutter_native_splash)
を見つけることができました。

導入は簡単です。

```
$ flutter pub add flutter_native_splash
$ flutter pub get
```

として ``pubspec.yaml`` に以下のような内容を追加します。
``color`` または ``background_image``
のどちらか一方を設定するのが最小限必須のようです。

```
flutter_native_splash:
  color: "#795548"
  image: images/logo.png
```

ダークモードに別の色やイメージを表示することもできるようです。

その後、

```
$ flutter pub run flutter_native_splash:create
```

を実行すると、 web の場合 ``web/splash`` というフォルダができます。これでできあがりです。

Tag: flutter
