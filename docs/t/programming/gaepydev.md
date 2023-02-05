# Eclipse で Python

Update: unknown

Google App Engine の Python の方、やってみようと思って、 Mac で使えるPython のエディタを探してみました。



[http://wiki.python.org/moin/PythonEditors](http://wiki.python.org/moin/PythonEditors)



いろいろあるものです。結局、使い慣れた Eclipse で、プラグイン PyDev を使うことにしました。



プラグインはお約束の方法で入れれば OK 。 Mac OS X 用の Google App Engine SDK も入れます。 MacBook のターミナルで `python --version` とやってみると微妙に新しいバージョンだったので、 PyDev も SDK も `/usr/bin/python2.5` を使うように設定します。



GoogleAppEngineLauncher で新しいアプリケーションを作成すると、あっさりできてしましました。実行すると "Hello World!" 表示します。こんなに簡単でいいのかなってくらい簡単です。 PyDev が入った Eclipse では、プロジェクトの新規作成で "PyDev Google App Engine Project" を選択できるので、試してみます。できあがったプロジェクトは空っぽです。 GoogleAppEngineLauncher で生成されたファイルを移動して、ディレクトリの位置を入れ替えて、 Eclipse のプロジェクトの位置と、 GoogleAppEngineLauncher が認識するアプリケーションの位置が同じになるようにします。



GoogleAppEngineLauncher で、管理用のコンソールを開いたり、デプロイしたりできるようです。これだけあれば、普通の開発で困ることはなさそうです。



で、気になるのが、プロジェクト作成時に自動生成された `src` サブフォルダ。これはどう使うんだろう？ Python の開発の全体像を理解していないのでよくわかりません。



なにはともあれ設定など確認してみようと `app.yaml` を開くとシステムのデフォルトのエディタが起動してしまいました。これはあまり好みではないので、 YEdit というプラグインを追加しました。機能としては、色つけてくれるくらいなのかなぁ。その色を好みの感じに変えました。
