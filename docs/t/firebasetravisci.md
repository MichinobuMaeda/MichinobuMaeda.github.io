# Travis CI で Firebase にデプロイする

Update: 2018-07-01


Firebase の hosting と functions を Travis CI でデプロイしてみました。
設定ファイルはこんな感じです。

```
language: node_js
node_js:
  - "8"
before_deploy: "yarn build"
deploy:
  provider: firebase
  skip_cleanup: true
  token:
    secure: xxxxxxxxxxxxxxxxxx
```

私の好みで ``npm`` ではなく ``yarn`` を使っているのですが、
node_js のバージョンがデフォルトではうまくいきません。
``"6"`` より新しければだいじょうぶかな。。。

hosting の対象は Vuetify で作成した SPA ( Single-page application )
で、ビルドが必要です。
そのため ``deploy.skip_cleanup: true`` の設定を追加し、
``before_deploy: "yarn build"`` でデプロイの前にビルドします。

``npm`` の場合は ``yarn`` を ``npm`` に置き換えてください。

Firebase にデプロイするための設定はこちら。
https://docs.travis-ci.com/user/deployment/firebase/

トークンを暗号化するために travis ツールが必要ですね。
まず、 Ruby がなければインストールして、 gem コマンドで入れてやります。

https://github.com/travis-ci/travis.rb#installation

```
$ gem install travis -v 1.8.8 --no-rdoc --no-ri
```

``travis encrypt`` コマンドを実行すると ``.travis.yml``
に環境変数の設定らしきものが追加されるのですが、
そっちではなく上記の ``deploy.token.secure`` にコピペします。

でき上がった ``.travis.yml`` を ``git push`` すると
Travis が自動でビルドとデプロイをして、、、、あ、エラー、、、

エラーメッセージに従って ``firebase-functions`` と ``firebase-admin``
を ``package.json`` に入れてやるとうまくいきました。

```
$ yarn add firebase-functions -D
$ yarn add firebase-admin -D
```

``npm`` の場合は ``npm install -D`` です。

Tag: Node JavaScript TravisCI Firebase
