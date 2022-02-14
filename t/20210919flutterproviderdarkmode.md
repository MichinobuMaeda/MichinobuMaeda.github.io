Flutter の Provider で動的にダークモード設定する
======

Update: 2021-09-19

追記: 2022-02-14 -- Provider より BLoC の方が楽でした。

Flutter のダークモードはこのような感じで設定するのですが、
``light``, ``dark``, ``system`` をここで設定するとその後は変更できないようなんです。で、
[dynamic_theme](https://pub.dev/packages/dynamic_theme)
のようなプラグインもあります。あまりプラグインの数を増やしたくないので provider を使ってやってみました。きれいに簡単にできます。

```
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My app title',
      theme: theme,
      darkTheme: darkTheme,
      themeMode: ThemeMode.dark,
      home: const MyHomePage(title: 'My app title'),
    );
  },
```

まず、こんな ``ChangeNotifier`` を作ります。保持するデータはモードだけです。

```

class ThemeModeModel extends ChangeNotifier {
  ThemeMode _mode = ThemeMode.system;

  set mode(ThemeMode mode) {
    _mode = mode;
    notifyListeners();
  }

  ThemeMode get mode => _mode;
}
```

それをアプリに渡します。

```
void main() {
  runApp(MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (context) => ThemeModeModel()),
      ... ...
    ],
    child: const App(),
  ));
}
```

変更の通知は一番上で受け取ります。モードが変更されるとすべて描き変えられる重い処理になりますが、しょうがないですよね。

```
  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeModeModel>(
      builder: (context, themeMode, child) {
        return MaterialApp(
          title: appTitle,
          theme: theme,
          darkTheme: darkTheme,
          themeMode: themeMode.mode,
          home: const MyHomePage(title: appTitle),
        );
      },
    );
  }
```

アプリのどこかにモードを選択する Widget を置きます。例えばこんな感じ。
[Material icons](https://fonts.google.com/icons) に ``light_mode`` と ``dark_mode`` があるんだけど「システムの設定に合わせる」を表すいい感じのものがないなあ。

```
  @override
  Widget build(BuildContext context) {
    ThemeModeModel themeModeModel = Provider.of<ThemeModeModel>(context);
     ... ...
      DropdownButton<ThemeMode>(
        value: themeModeModel.mode,
        onChanged: (ThemeMode? value) {
          themeModeModel.mode = value ?? ThemeMode.light;
        },
        items: const [
          DropdownMenuItem<ThemeMode>(
            value: ThemeMode.light,
            child: Text('ライト'),
          ),
          DropdownMenuItem<ThemeMode>(
            value: ThemeMode.dark,
            child: Text('ダーク'),
          ),
          DropdownMenuItem<ThemeMode>(
            value: ThemeMode.system,
            child: Text('自動'),
          ),
        ],
      ),
```

Tag: flutter dart material
