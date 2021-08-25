yarn の警告 "No license field" を止める
=====

Update: 2021-05-08


``package.json`` には間違いなく

```
  "license": "MIT",
```

と書いているのになぜか ``yarn`` を実行すると

```
warning ../package.json: No license field
```

と表示されます。気になって調べてたらわかりました。

<https://stackoverflow.com/questions/45690202/how-to-have-yarn-not-issue-a-warning-for-the-license-field>

によると上のディレクトリの ``package.json`` に ``license`` が無いからだそうです。確かにメッセージを見るとパスに ``../`` が付いてます。でも、そんなファイルを置いた覚えはないのだが、、、

```
$ cat ../package.json
{
  "dependencies": {}
}
```

有った（汗）。

たぶんそのディレクトリでまちがって npm か yarn を実行してしまったのでしょうね。
’’../package.json`` を消したら警告も表示されなくなりました。



Tag: nodejs



