+++
title = "smtp_tls_security_level"
date = 2017-12-07T00:00:00+09:00
categories = ["tech"]
tags = ["SMTP", "STARTTLS", "TLS", "Postfix"]
+++

久しぶりに立てたメールサーバから Gmail 宛に送信すると、なんだか赤いマークが付いてます ^^;

![](notlsmail.png)

暗号化されてないからよくないと。。。

昔は当たり前ではなかったSMTPサーバ間の暗号化が求められているのでしょうか？

少し調べてみると、 2009年の Postfix 2.3 で
``smtp_tls_security_level``
というパラメータが追加になっています。
Change log によると、いろいろパラメータがあってごちゃごちゃしてたのを整理したのだそうです。

```
smtp_tls_security_level = may
```

で Gmail さんには文句言われなくなりました。
