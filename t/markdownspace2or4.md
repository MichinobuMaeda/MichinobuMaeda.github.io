Markdown のインデントはスペース 2個なのか 4個なのか
=====

Update: 2020-07-11


## EditorConfig が効かない？

先日 JetBrains の開発ツールを買って有料のもののありがたさを感じているところなのですが、
どうも [EditorConfig](https://editorconfig.org/) の

```
indent_style = space
indent_size = 2
```

の設定が反映されないようです。
[Tab] キーでスペースが 4個入ります。
こんなところにバグが残っているわけないよな、もしかして、スペース 4個が正しいのかもと調べてみました。

「正しい」とは言っても GitHub に入れたソースの ``README.md``などはスペース 2個で問題なく表示されます。
さらに、私が Markdown でインデントを使うのはリストの入れ子くらいなので、
つまり、実用上は何を持って「正しい」とするのかをあまりこだわってもしょうがないさそうですが、でも気になるから。

## CommonMark

で、そもそもの正統な Markdown って何？ というところからよく知らなかったのですが、これ
[CommonMark](https://commonmark.org/)
のようですね。

[CommonMark Spec](https://spec.commonmark.org/) Version 0.29 (2019-04-06)
が最新の仕様なのかな。

まず、
[2.2Tabs](https://spec.commonmark.org/0.29/#tabs)
には

> tabs behave as if they were replaced by spaces with a tab stop of 4 characters.

と書かれています。
考え方としてはスペース 4個のようです。

で、かなり長文なので ``indent``
でざっと検索してみたところインデントでスペースを使う場合は 4個のようです。
2個でもいいというような記載はなさそうです。
また、出力結果に影響しないものとしてスペース 3個までのインデントを認めている箇所がいろいろあるので、
出力に影響がある（つまり意味がある）インデントはスペース 4個にしないと不都合があるかもしれません。

## GitHub Flavored Markdown

[GitHub Flavored Markdown](https://github.github.com/gfm/)
の仕様はどうなっているか調べてみたところ、
GitHub Flavored で追加された項目 ( テーブルとかタスクリストとか )
以外は CommonMark と同じもののようです。

GitHub のサイトの表示でスペース 2個を許容しているのは、
HTML みたいに仕様通りでなくても救っているということなのでしょう。

## 結論

JetBrains のツールの挙動に任せるのでいいや。


Tag: markdown
