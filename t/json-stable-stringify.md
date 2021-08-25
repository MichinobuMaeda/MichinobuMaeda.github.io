JSONを名前順にソートして出力する
=====

Update: 2018-07-01


JavaScript の JSON.stringify() は便利なのですが、
オブジェクトのプロパティが出力される順番は実装依存です。

名前順に並んでくれるとうれしいんだけどなぁ、と探してみたところ
``json-stable-stringify`` というのがありました。

<https://github.com/substack/json-stable-stringify>

使い方は簡単で、

```
npm install json-stable-stringify
```

とか

```
yarn add json-stable-stringify
```

のようにインストールして、

```
var stringify = require('json-stable-stringify');
var obj = { c: 8, b: [{z:6, y:5, x:4}, 7], a: 3 };
console.log(stringify(obj, {space: '  '}));
```

とすると、

```
{
  "a": 3,
  "b": [
    {
      "x": 4,
      "y": 5,
      "z": 6
    },
    7
  ],
  "c": 8
}
```

と出力されます。

Tag: Node JavaScript JSON
