Anaconda をインストールする
=====

Update: 2021-04-15


「Pythonによるプログラミング入門－東京大学教養学部テキスト－アルゴリズムと情報科学の基礎を学ぶ」ISBN: 978-4-13-062458-9 のための Python の環境として Anaconda をインストールしました。

Python は使ったことがあるのですが、このテキストをぱらぱらとめくってみると簡単なプログラムでグラフを描画しています。えーっと、これ、私たち、つまり、業務システムとか Web アプリとかつくっているエンジニアが知ってる Python の環境じゃないだろ？ 素の Python にどんだけパッケージ追加したらコマンドラインからいきなりグラフ描画できるのか見当つかないぞとテキストの最初のあたりを読んでみると Anaconda というのを使っていることがわかりました。そこにこのテキストで必要なものが一式入っているようです。最近の理系の学生さんはこういうのを使ってるのね。ということで、さっそく入れてみます。

## インストーラの入手と実行

私は普段 Mac を使っているのですが、他の人といっしょにやる都合で Windows でやってみます。

まず <https://www.anaconda.com/products/individual> のページの下の方から Windows の "64-Bit Graphical Installer" をダウンロードします。
``Anaconda3-2020.11-Windows-x86_64.exe`` という 457MB の（でかっ）インストーラがダウンロードできました。これを実行します。

まず、なにかインストールするときのお約束のセキュリティの警告は「実行」を選択します。

![](anaconda_001.png)

他のアプリを終了しろとの警告が出るので、指示に従って「Next」

![](anaconda_002.png)

License agreement は読みたければ読んで「Next」

![](anaconda_003.png)

Taylor Swift が Tiny desk concert で "Just me, no dancers." と言ってたのがかっこよかったのでデフォルトの「自分用」の選択のまま「Next」

![](anaconda_004.png)

必要なディスク容量 2.7GB （でかっ）について「足りない！」みたいな警告が出てなければ「Next」

![](anaconda_005.png)

私の場合、開発用の Python を別に入れる可能性があるので 2個目のチェックボックスは Off にしました。理系の学生・研究者でなければ Off でよさそうです。 PyCharm 等の IDE の設定はそれぞれの IDE でできるでしょうし。で、「Install」ボタンを押すと、、、

![](anaconda_006.png)

サイズが大きな分、インストールに時間がかかります。終わったら「Next」

![](anaconda_007.png)

PyCharm Pro を買ってほしそうですが、とりあえず無視して「Next」

![](anaconda_008.png)

Tutorial などは後で見たければ見るので、チェックボックスはすべて Off にして「Finish」

![](anaconda_009.png)

Windows のスタートメニューにこのような項目が表示されます。
Reset Spyder Settings 以外のものを一つずつ開いてみます。

![](anaconda_010.png)


## Anaconda Navigator

まず Anaconda Navigator です。ここからいろいろ起動できるようです。

![](anaconda_011.png)

Tutorial は、、、英語だ、、、

![](anaconda_012.png)


## Anaconda PowerShell Prompt

次に、 Anaconda PowerShell Prompt ですが、これは要するに PowerShell のコンソールで Python が起動できる、というそれだけのものです。

```
python3 --version[Enter]
```

を実行してみると、無い。 ``3`` は付かないんですね。

```
python --version[Enter]
```

で表示されたバージョンは 3.8.5 です。新しいバージョンが入っています。
``python[Enter]`` で ``1 + 1[Enter]`` が ``2`` になることを確認したら [Ctrl]+[D] ( Control キーを押しながら D を押す ) で Python を終了し、 ``exit[Enter]`` で PowerShell を終了します。 PowerShell の終了は右上の [X] でウィンドウを閉じるのでもいいです。

![](anaconda_013.png)


## Anaconda Prompt

Anaconda Prompt は PowerShell ではなくコマンドプロンプトが起動します。 PowerShell でない以外、できることは Anaconda PowerShell Prompt と同じです。

![](anaconda_014.png)


## Jupyter Notebook

Jupyter Notebook は、最初にコマンドプロンプトが表示されてしばらくすると「ブラウザか何かで開くか（意訳）？」と聞かれるので Edge でも Chrome でも好きなものを選択します。

![](anaconda_015.png)

するとフォルダの一覧が表示されます。これは ``C\:Users\ユーザ名`` の直下だな。

![](anaconda_016.png)

で、私はここでいきなり「New」の「Notebook」の「Python 3」を選択したのですが、この場所はよくないので、みなさんは後述する通り ``Documents`` の下の ``Python Scripts`` を開いて、そこから「New」の「Notebook」の「Python 3」を選択してください。
``Documents`` の下に ``Python Scripts`` が無い場合は ``Documents`` で 「New」の「Other」の「Folder」を選択して作成してください。

![](anaconda_017.png)

するとブラウザの新しいタブが開いてこんなものが表示されます。

![](anaconda_018.png)

``1 + 1[Enter]`` と入力してみると、改行された。。。いや、改行じゃなくて実行したいんだけど。

![](anaconda_019.png)

改行を消して Run ![](anaconda_020b.png) ボタンを押すと無事に実行できました。

![](anaconda_020.png)

改行できるということは、複数行まとめて実行できるということかな？ と 3行ほど入力して Run ![](anaconda_020b.png) ボタンを押して実行すると、期待通りに動きます。

![](anaconda_021.png)

変数 ``a`` の値は覚えてくれているようです。

![](anaconda_022.png)

フロッピーディスクのボタン ![](anaconda_022c.png) ( って若い人はフロッピーディスクは知らんだろ ) を押して保存してブラウザのタブを閉じると ''Untitled.ipynb'' というファイルが保存されています。

![](anaconda_023.png)

「Running」を選択してみると、このファイル名の行に「Shutdown」ボタンがあります。何か動いているようです。

![](anaconda_024.png)

「Shutdown」ボタンを押して「Files」に戻ると表示が変わりました。

![](anaconda_025.png)

前述の通りファイルを保存する場所がよくなかったので、
``Documents`` の下の ``Python Scripts`` からやり直します。
``Documents`` の下に ``Python Scripts`` が無い場合は ``Documents`` で 「New」の「Other」の「Folder」で作成してください。「New」の「Notebook」の「Python 3」を選択して新しいノートブック（と呼ぶのかな？）を作成して、

![](anaconda_026.png)

「File」の「Rename」でファイル名を変更します。ファイル名には日付やテキストの章の番号などを付けるといいと思います。

![](anaconda_027.png)

先ほどと同じことをやって、フロッピーディスクのボタン ![](anaconda_022c.png) で保存してブラウザのタブを閉じます。

![](anaconda_028.png)

「Rename」で付けたファイル名で保存されています。これをクリックすると元通りの状態で表示されるんだろうな。そうでない場合を試してみたいので、

![](anaconda_029.png)

「Running」で「Shutdown」してみます。

![](anaconda_030.png)

表示が変わりました。これをクリックして開いてみます。

![](anaconda_031.png)

先ほどと見た目は同じものが表示されたので、変数 ``a`` を覚えてくれているか試してみます。 ``a`` を入力して Run

![](anaconda_020b.png) ボタンで実行するとエラーになります。覚えていません。

![](anaconda_032.png)

ブラウザを閉じて、何やら呪文がたくさん表示されているコマンドプロンプトを右上の [X] で閉じて、 Jupyter Notebook を開き直すと、 Shutdown された状態でした。

Jupyter Notebook 例えば学生の場合、授業１回分を１個のノートブックにするという使い方が良さそうです。
Python を開発の作業で使うようなコンソールで実行するとコンソールを閉じたらすべて消えてしまいます。こんな感じでやったことを丸ごと残しておくことができるのは、学習用にとても便利です。

![](anaconda_033.png)


## Spyder

最後に Spyder を試してみます。 Spyder を起動すると「アップデートするか？」と聞かれるます。今回はとりあえず無視します。

![](anaconda_034.png)

次に Kite というツールを入れるかどうか聞かれます。詳しい説明は省略しますが、これも今回のお勉強の範囲であればどうしても欲しい感じではないので無視します。今後、本格的に仕事や研究で Python を使う場合は用途に合ったものを入れてください。 Visual Studio Code や PyCharm であれば一般的なものが最初から入っているか、入っていなくても案内が表示されるか、どちらかだと思います。

![](anaconda_035.png)

Spyder の見た目は Visual Studio Code のような IDE と同じような感じですね。左側にプログラムを書くエディタ、右側に実行結果等を表示するコンソールがあります。左側に

```
a = 0
a = a + 1
print(a)
```

と書いて、フロッピーディクスのボタンで（これ作ったやつ絶対おやじだ）保存して、右向き三角のボタン ![](anaconda_037b.png) で実行します。

![](anaconda_037.png)

すると「実行結果をどこに表示する？」と聞かれるので、デフォルトの設定のまま「Run」ボタンを押します。

![](anaconda_036.png)

右側に ``1`` と表示されました。 Visual Studio Code のような IDE より手軽ですね。まとまった量のプログラムを書く場合は Jupyter Notebook ではなくこちらを使うことになります。


## 追記: Mac にインストールする

Mac でも試してみたのですが、 Anaconda Navigator, Jupyter Notebook, Spyder は Windows と見た目がほとんど同じです。

まず <https://www.anaconda.com/products/individual> のページの下の方から MacOS の "64-Bit Command Line Installer" をダウンロードして、コンソールで実行します。

```
$ cd ~/Downloads/
$ sh Anaconda3-2020.11-MacOSX-x86_64.sh
```

``~/anaconda3`` に一式がインストールされます。そのディレクトリの直下に ``Anaconda-Navigator`` というアプリがあるのでそれを実行すると Anaconda Navigator が起動します。 Jupyter Notebook と Spyder は Anaconda Navigator から起動できるのですが、単独で起動したいのだけど、、、

Jupyter Notebook を起動したコンソールの表示を見たところ ``~/anaconda3/bin`` の下の ``jupyter_mac.command`` を起動しているだけのようです。その ``jupyter_mac.command`` は同じディレクトリの ``jupyter-notebook`` を起動しているだけです。コンソールから

```
$ ~/anaconda3/bin/jupyter-notebook
```

で起動できました。

Spyder は

```
$ ~/anaconda3/bin/spyder
```

で起動できました。

アンインストールは ``~/anaconda3`` を消すだけでよさそうです。

### 追記: Mac の PATH の変更


Mac の場合インストーラが ``.bash_profile`` に Anaconda の PATH などの設定を追加します。

```
(base) ~$ which python
/Users/michinobu/anaconda3/bin/python
(base) ~$ which python3
/Users/michinobu/anaconda3/bin/python3
(base) ~$ which python --version
/Users/michinobu/anaconda3/bin/python
(base) ~$ python --version
Python 3.8.5
(base) ~$ python3 --version
Python 3.8.5
```

これが都合悪い場合は ``.bash_profile`` の

```
# >>> conda initialize >>>
```

から

```
# <<< conda initialize <<<
```

までを消してください。私の場合、これを残した  ``.bash_profile_anaconda3`` と消した ``.bash_profile`` を使い分けるようにしています。

Tag: python



