# Flutter の多言語化で JSON を使いたくない

Update: 2022-02-14

Flutter の[国際化のガイド](https://docs.flutter.dev/development/accessibility-and-localization/internationalization)
に ``*.arb`` という
JSON ベースの設定ファイルが出てくるのですけれど、あまり好きではないな。

Flutter の場合、その設定ファイルを変更した後にコード生成のための一手間が必要ですし、設定に何か間違いがあればコード生成の後でビルドエラーになってしまいます。生成されたコードを見ると設定ファイルに比べて可読性が悪いようにも思えませんし、それなら Dart で直接書けばいいと思ったわけです。そうすれば、何か変更した瞬間に IDE が他のプログラムと同じようにエラー検出してくれますから、その方がいいです。コーディングのペースを維持できます。

とはいえ、最初から全部書くのはたいへんなので、まず、上記のページの手順で一度コードを生成します。その際、サンプルとしてパラメータの埋め込みがあるようなデータも入れておきます。

生成したコードは ``.dart_tool/flutter_gen/gen_l10n`` に出力されるので、それを
``lib`` の下の自分の好きな場所にコピーします。ファイル名も変えたければ変えていいです。

そして、 ``import 'package:flutter_gen/gen_l10n/app_localizations.dart';``
をその場所に変更して、コード生成のために作成した
``*.arb`` ファイルや　``l10n.yaml`` や ``pubspec.yaml`` の ``generate: true``
の設定を消します。これでビルドが通れば OK.

Tag: flutter dart
