# Firebase で Cloud Tasks

Update: 2022-08-21

Firebase functions で定時実行するジョブの実行の有無を、ジョブの結果で決めたいんだけど、ジョブ・キューみたいなことができるとうれしいんだけどとドキュメントを眺めていたら、いつの間にか
[Enqueue functions with Cloud Tasks](https://firebase.google.com/docs/functions/task-functions)
というのができているのに気がつきました。
SDK for Cloud Functions v3.20.1 / Admin SDK v10.2.0 からということなので最近ですね。

使い方は簡単で、 Functions を使ったことがある人でしたらドキュメントに掲載されているサンプル・コードを見ればだいたいわかるでしょう。

Cloud Tasks ではジョブをキューに登録するときにデータを引数で渡すこともできます。私の場合、 Functions の時間制限を超えるかもしれないジョブを分割する用がありまして、引数に分割した処理対象範囲を設定したものをまとめて全部登録して非同期で並行に実行させてうまく行きました。処理の開始から終了までの時間は短くなりました。処理対象範囲の指定が簡単になったので、処理量もわずかながら減っているはずです。

```
const functions = require("firebase-functions");
const {getFunctions} = require("firebase-admin/functions");

const region = "...";

exports.job1 = functions.region(region)
    .pubsub.schedule(...).timeZone(...)
    .onRun(async () => {
         ... ...
        await Promise.all(
            Array.from(Array(10).keys())
                .map((index) => getFunctions().taskQueue(
                    `locations/${region}/functions/job2`,
                ).enqueue({index}),
            ),
        );
    });

exports.job2 = functions.region(region)
    .runWith({...})
    .tasks.taskQueue({...})
    .onDispatch(async ({index}) => {...});
```

Tag: firebase
