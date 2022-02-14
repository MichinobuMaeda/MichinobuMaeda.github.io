# Flutter の色の設定で楽をする

Update: 2022-02-14

Flutter の色の設定は

```
  Widget build(BuildContext context) => MaterialApp(
      theme: ThemeData(primarySwatch: Colors.teal),
      ...
  );
```

のようにすればとりあえずできます。でも、セカンダリ・カラーとかダーク・モードとかどうすればいいのかとなると、私はデザイナーではないので「どうやって設定するか」の前に「どのような色にすればいいか」がわかりません。そんな私が細かな設定を考えるのは時間の無駄なので
``flex_color_scheme`` を使ってみました。

フォントやボタンのサイズなども一括で設定したいので、次のような感じに。
``NotoSansJP`` は ``asset`` に入れてあります。

```
  Widget build(BuildContext context) => MaterialApp(
      theme: FlexColorScheme.light(
        scheme: FlexScheme.amber,
        fontFamily: 'NotoSansJP',
        textTheme: TextTheme(...),
      ).toTheme.copyWith(
            elevatedButtonTheme: ElevatedButtonThemeData(...),
            outlinedButtonTheme: OutlinedButtonThemeData(...),
            snackBarTheme: SnackBarThemeData(...),
          ),
      darkTheme: FlexColorScheme.dark(
        ... light と同じ内容 ...
          ),
        ...
  );
```

Tag: flutter dart
