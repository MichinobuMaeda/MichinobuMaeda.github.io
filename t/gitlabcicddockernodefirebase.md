Firebase の CI/CD 用の Docker を作る
=====

Update: 2020-07-11


先日買った Chromebook の Debian に
[Docker Engine](https://docs.docker.com/engine/)
を入れてみたら普通に動きました。

久しぶりに Docker でなにか作ってみようかと、
Firebase のアプリを GitLab の CI / CD するコンテナを作りました。

これまでは GitLab の公式のガイドに載っていた
rambabusaravanan/firebase
を使っていたのですが、アップデートの頻度がもひとつなので自分でメンテできるようにします。

作ったものは
https://hub.docker.com/repository/docker/michinobumaeda/firebase-tools
に置いてます。

Dockerfile は 3行しかありません。

```
FROM node
RUN npm i -g n && n 10
RUN npm i -g eslint firebase-tools jest
```

1行目: Node.js の公式イメージをベースにします。

2行目: 公式イメージは最新のバージョンで Firebase のデプロイで使うには新しすぎるので、
n で node 10 にします。ベースイメージのバージョンを指定するよりこっちのほうが楽だし後で変えるのも簡単。

3行目: 必要なツールを追加します。

これを最新にするにはイメージをキャッシュ無しで再ビルドすればいいはず。
後日 firebase-tools のアップデートが出たらやってみます。

Tag: docker firebase gitlab node n
