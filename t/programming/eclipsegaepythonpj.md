Eclipse Pydev で Google App Engine
=====

Update: unknown

[](https://code.google.com/p/sangiin-votes/)

参議院の押しボタン投票を集計する Google App Engine のアプリ [http://code.google.com/p/sangiin-votes/](http://code.google.com/p/sangiin-votes/) を作り始めました。そのための Eclipse のプロジェクトの作成の手順です。使用している Eclipse のプラグインなどについては [Eclipse で Python](https://sites.google.com/site/michinobumaeda/programming/gaepydev) を見てください。


アプリケーションの ID は `sangiin-votes` です。

新しいプロジェクトを作成します。"Pydev Google App Engine Project" を選択します。


![](https://lh3.googleusercontent.com/-b_ImD0FlXi4/TfRi9XHpKjI/AAAAAAAACDg/4zpd9VUJlv8/s1600/sv001.png)



プロジェクト名と Python のバージョン、パスを設定します。プロジェクト名はアプリケーション ID と同じにしました。私の MacBook の場合、`/usr/bin/python` は 2.6.1 なので、 `/usr/bin/python2.5` を指定しました。



![](https://lh4.googleusercontent.com/-33XNMU6edVo/TfRi9zj4FvI/AAAAAAAACDk/r6TayR-gO5A/s1600/sv002.png)



Google App Engine SDK のパスを設定します。 Mac OS X の場合は



`/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/`



のようなわかりにくい場所になります。



![](https://lh3.googleusercontent.com/-euNQNIB84uY/TfRjBKM-IJI/AAAAAAAACD0/vHICD_NGPbI/s1600/sv004.png)



アプリケーション ID と、サンプルコードの有無を指定します。



![](https://lh4.googleusercontent.com/-emsZhPBUaY4/TfRi_LEvRVI/AAAAAAAACDo/tWmiy6Nvsy0/s1600/sv005.png)



`app.yaml` と `helloworld.py` のサンプルが生成されました。

![](https://lh5.googleusercontent.com/-OiyX_ZFxvao/TfRjAwahNNI/AAAAAAAACDw/W4MqarIX1fU/sv006.png)



アプリケーションをデプロイするスクリプト、開発用の実行環境を起動するスクリプト（データストアをクリアするものとしないもの）を作成します。

sangiin-votes_deploy.sh

```
/usr/bin/python2.5 ¥
 /Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/appcfg.py ¥
 --email=xxxxxxxxxxxxxxxxxxxx@gmail.com ¥
 update ¥
 /Users/michinobu/workspace/sangiin-votes/src
```

sangiin-votes_start_cleare.sh

```
/usr/bin/python2.5 ¥
    /Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/dev_appserver.py ¥
    --admin_console_server= ¥
    --port=8080 ¥
    --use_sqlite ¥
    --clear_datastore ¥
    /Users/michinobu/workspace/sangiin-votes/src
```

sangiin-votes_start.sh

```
/usr/bin/python2.5 ¥
    /Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/dev_appserver.py ¥
    --admin_console_server= ¥
    --port=8080 ¥
    --use_sqlite ¥
    /Users/michinobu/workspace/sangiin-votes/src
```


`sangiin-votes_start_cleare.sh` を実行して、ブラウザで確認します。

アプリケーション `http://localhost:8080/`

![](https://lh4.googleusercontent.com/-lqgH5wQTXYs/TfRjAtg965I/AAAAAAAACDs/H2gJfmygLS8/sv007.png)


管理機能 `http://localhost:8080/_ah/admin/`

 ![](https://lh6.googleusercontent.com/-m8mF3wLjIX0/TfRjBvLfzPI/AAAAAAAACD4/YouosB3r1hg/s1600/sv008.png)


とりあえず `helloworld.py` のファイル名を `index.py` に変更し、 `app.yaml` の該当箇所も書き換えて、リポジトリに登録します。リポジトリの場所は [http://sangiin-votes.googlecode.com/svn/trunk/](http://sangiin-votes.googlecode.com/svn/trunk/) です。Google Project Hosting の場合、http が読み取り専用、 https が読み書き可能です。パースペクティブを "SVN Repository Exploring perspective" に変更し、新しいリポジトリ・ロケーションを追加します。



![](https://lh6.googleusercontent.com/-wsmSFYndmJQ/TfSNX2MS8GI/AAAAAAAACEI/a6MnhOqAOYk/s1600/sv009.png)



Pydev のパースペクティブに戻り、プロジェクトを共有します。



![](https://lh5.googleusercontent.com/-jfUf0ZDWrVo/TfSNX2TVgtI/AAAAAAAACEM/as820SaeRkQ/s1600/sv010.png)



リポジトリの種類は SVN を選択します。



![](https://lh6.googleusercontent.com/-Be7gfHCuYlg/TfSNX9MiD1I/AAAAAAAACEE/dXk3ZWuuq6Y/s1600/sv011.png)



登録済みのロケーションを選択します。


![](https://lh5.googleusercontent.com/-5KdzI8LLzgg/TfSNYIwA2II/AAAAAAAACEQ/wUyPAKaKxsM/s1600/sv012.png)



プロジェクトのロケーションが [https://sangiin-votes.googlecode.com/svn/trunk/sangiin-votes](https://sangiin-votes.googlecode.com/svn/trunk/sangiin-votes) になるように設定します。



![](https://lh4.googleusercontent.com/-Cn4kMNfHqJg/TfSNYP0XK7I/AAAAAAAACEc/GhhWblDLjMw/s1600/sv013.png)



コメントは適当に。自動生成されたものでいいと思います。



![](https://lh3.googleusercontent.com/-6ZQWf2ZFSBY/TfSNYOM-bvI/AAAAAAAACEU/T24QhW1ntsk/s1600/sv014.png)



リソースのコミットのコメントは適当に。



![](https://lh4.googleusercontent.com/--FlQF6O1aws/TfSNYalmknI/AAAAAAAACEY/wFwDoOepMfE/s1600/sv015.png)



"SVN Repository Exploring perspective" に戻って、表示を更新すると、登録した結果を見ることができます。 



![](https://lh6.googleusercontent.com/-IKQIN-0mw7c/TfSNYao4MpI/AAAAAAAACEg/eVhfSCvG8-g/sv016.png)
