# JavaScriptでスワイプ操作の検出

Update: 2021-03-13


マウスの操作でHTML上の要素を移動するプログラムを書いてみたんだけど、スマホでは反応しない、、、スワイプってそのものの名称のイベントはないようだけどどうするの？ と調べたらすぐ見つかりました。

Detecting a swipe (left, right, top or down) using touch \
<http://www.javascriptkit.com/javatutors/touchevents2.shtml>

なるほど、マルチタッチは無視して ``e.changedTouches[0]`` だけ見るわけですね。それから ``touchmove`` は ``e.preventDefault()`` で素通りしてしまうのが幸せになれるポイントのようです。

ほとんどこの記事の通りのコードを書いて要素の移動はうまくいったのですが、その要素はボタンで、クリックが効かなくなりました。なるよな〜〜 ``e.preventDefault()`` してるんだから。そこは ``touchstart`` から ``touchend`` まで 100msec. 以内ならクリック時の処理をする、としてみたところ、そこそこいい感じです。 100msec. 以内でスワイプしたつもりみたいなことができる超人は無視です。

で、ここまでできたところで私が今回使っている Vuetify のドキュメントをよく見たら ``v-touch`` というのがありました（涙

まあ、このやり方でマウスの操作と共通の処理にできたし、後でタイミングや移動距離などの感度を細かく調整できるから、これはこれでいいや。

Tag: javascript vue
