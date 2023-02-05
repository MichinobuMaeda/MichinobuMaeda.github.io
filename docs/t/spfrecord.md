# SPFレコードの設定

Update: 2017-12-03


新設したメールサーバのテストのために Gmail 宛にメールを送ったら迷惑メールにされてしまいました。
DNSの逆引き設定はしてるし他になんかあったっけ？
と、過去を振り返ること数分。ああ、なんだか呪文をDNSに追加してたわ、これだ。

送信ドメイン認証SPFレコードについて au

https://www.au.com/mobile/service/mail/attention/spf-record/

日本語の説明としては、この au のページが分かりやすいです。

SPFポークではありません。
「このドメインのメールは、このIPアドレスからしか送信されないはずです」というようなことの宣言です。
この条件に合わないメールが来たら怪しいということになります。

SPFレコード追加後に受信したメールのヘッダを見ると以下のような行があって、
Gmail さんがチェックしてくれているのがわかります。

```
Received-SPF: pass (google.com: domain of user@domain
  designates 123.45.67.89 as permitted sender)
  client-ip=123.45.67.89;
```

Tag: SPF spam email DNS


