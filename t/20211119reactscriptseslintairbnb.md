react-scripts に Airbnb Style を入れる
======

Update: 2021-11-19

私はソースコードのスタイルをどうするか考えるのは面倒なのですが、かといってスタイルが揃ってないのも嫌なので、厳し目のルールを
IDE などで自動で強制してくれるのが好みです。
VS code で Flutter のコーディングをやるような環境は最高ですね。で、
``create-react-app`` で作ったプロジェクトに ``eslint`` の ``airebnb`` 拡張を入れようとすると、少しハマりました。

まず ``eslint`` の最新の v8.x.x はうまくいかないようなので v7.x.x を入れます。

```
$ yarn -D add eslint@^7.32.0 eslint-config-airbnb
```

``package.json`` に設定を追加します。

```
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest",
      "airbnb"
    ]
  },
```

この状態ではなぜか動かないので、

```
$ rm -rf node_modules
$ yarn install
```

とやってみたのですが NG で、

```
$ yarn upgrade
```

したら OK でした。

```
$ yarn lint
```

で大量のエラーと警告を表示してくれます。
VS Code を起動し直すとエディタは真っ赤になります（笑



Tag: nodejs react eslint
