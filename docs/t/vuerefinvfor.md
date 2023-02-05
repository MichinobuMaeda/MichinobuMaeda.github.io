# Vue の v-for の中の要素に ref を設定する

Update: 2020-06-24


Vue の v-for でループしている要素に ref を設定する必要があって、

```
<div v-for="item in list" :key="item.id">
  <div :ref="'element' + item.id">...</div>
  ... $refs['element' + item.id] を参照する処理 ...
</div>
```

のように動的に設定してみたのですが、うまくいきません。エラーなどは出ないのですが、明らかに参照できていません。

ループしてないところであればたいてい静的な値を設定すればいいのですが、ループの中はそれではダメだろう。
でも、こんなこと、誰でも普通に必要になるよね？ と解決策を探してみたらありました。解決策というか、何もしなくても勝手に配列になってくれるそうな。
たぶん、私が Vue のお勉強で基本的なことを端折って勝手にハマっただけです。

[How to add dynamic ref in vue.js?](https://stackoverflow.com/questions/45563329/how-to-add-dynamic-ref-in-vue-js)

Answer 9. You have dynamic refs and have multiple elements. To target any single node just pass the index within method params

```
<div v-for="(item, index) in list" :key="item.id">
  <div ref="element">...</div>
  ... $refs.element[index] を参照する処理 ...
</div>
```


Tag: vue



