# Firebase の API Key は隠さなくていいよね？

Update: 2020-07-11


とあるイベントの申し込み受付を Firebase と Vue で作っていたのですが、
GutHub にソースをコミットすると
"Warning: GitGuardian detected an API key from Google"
というメールが来ました。確かに入れてます。

でもこれ、クライアントサイドに配置してしまうつもりなんだけどな。
暗号化もせずに ^^)
仮に暗号化しようとしたとしても、その暗号化のキーはどこに置くの？
みたいなことになって、まあ、無理です。
特にクローズドでないサービスの場合は。

キーの発行時に Admin 向けのキーは「ちゃんとしまっとけ」と注意されたけど、
こちらは何も言われていません。
Firebase は主に不特定多数向けのクライアントサイドのアプリを想定しているわけで、
そんな、隠さなければ困るようなものを
Google さんが開発者に何も言わずに渡すわけないじゃないと調べてみました。

stackoverflow ではこれですが、要するに必要ないしできない、ということのようです。

"Is it safe to expose Firebase apiKey to the public?"
https://stackoverflow.com/questions/37482366/is-it-safe-to-expose-firebase-apikey-to-the-public

Google Groups などのやりとりを見てみましたが同様で、
上記のページへのリンクを貼ってある記事もあります。

Firebase のデータベースやストレージの場合、
普通のサーバーサイドのアプリケーションが使う RDBMS 等と違って、
個々のユーザに紐づく形で細かくアクセス権を設定できますから。
いいんじゃないかな。

がんばって CIツールに仕掛けを入れてデプロイ前に。。。
みたいなことはできるかもしれませんが、
世間の皆さんがやらないことをやって変な穴を開けてしまっても困るし。

> 追記： 結局 CI / CD の仕組みを使って動的に設定することにしました。

Tag: Firebase GitHub

