Debain 9 で Dovecot の SSL/TLS を設定する
=====

Update: 2017-12-02


久しぶりにメールサーバのセットアップをしています。

まず、 Debian 9 にはデフォルトで入っているけど使い慣れない exim4 を削除して、
Postfix や Dovecot のパッケージはこのくらい入れたらいいだろう、たぶん。

```
# apt-get remove exim4-base exim4-config exim4-daemon-light
# apt autoremove
# apt-get install postfix dovecot-imapd libsasl2-modules sasl2-bin
```

ローカルから SSL/TLS 無しでログインしてみます。

```
# telnet host.domain 143
Trying 100.200.300.400...
Connected to host.domain.
Escape character is '^]'.
* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID \
  ENABLE IDLE STARTTLS AUTH=PLAIN] Dovecot ready.
a login "user id" "password"
a OK [CAPABILITY IMAP4rev1 ... ] Logged in
b logout
* BYE Logging out
b OK Logout completed (0.000 + 0.000 secs).
Connection closed by foreign host.
```

OSユーザでログインできてしまいました。
PAM の設定とかしなくていいのですね。

で Dovecot の SSL/TLS が利用できるようにしようとドキュメントを見たのですが、こんだけでいいの ^^)?

https://wiki2.dovecot.org/SSL/CertificateCreation

https://wiki2.dovecot.org/SSL/DovecotConfiguration

昔のことは全然覚えていないけど、簡単になってないかな ^^)?

とはいえドキュメントに記載されている
doc ディレクトリは見当たらないので、それらしい場所を探して、
SSL証明書を作ります。

```
# cd /usr/share/dovecot/
# ./mkcert.sh 
```

``/etc/dovecot/conf.d/10-ssl.conf`` は以下のように。

```
ssl = yes
ssl_cert = </etc/dovecot/dovecot.pem
ssl_key = </etc/dovecot/private/dovecot.pem
```

サービスをリスタートします。

```
# service dovecot restart
```

リモートから SSL/TLS 無しでログインしてみます。

```
# telnet host.domain 143
 ... ...
a login "user id" "password"
* BAD [ALERT] Plaintext authentication not allowed without SSL/TLS, \
  but your client did it anyway. If anyone was listening, 
  the password was exposed. 
  a NO [PRIVACYREQUIRED] Plaintext authentication disallowed 
  on non-secure (SSL/TLS) connections.
```

ダメだって言われました。

ローカルから SSL 接続を試してみます。

```
# openssl s_client -connect host.domain:imaps
CONNECTED(00000003)
 ... ...
* OK [CAPABILITY IMAP4rev1 ... ] Dovecot ready.
a login "user id" "password"
a OK [CAPABILITY IMAP4rev1 ... ] Logged in
b logout
* BYE Logging out
b OK Logout completed (0.000 + 0.000 secs).
Connection closed by foreign host.
```

リモートから SSL 接続するとつながりません。。。
あ、ポート開けてなかったわ。使わないつもりだからそのままで。

STARTTLS を試してみます。

```
# telnet host.domain 143
 ... ...
a STARTTLS
a OK Begin TLS negotiation now.
b bye
Connection closed by foreign host.
```

できてるよ。いいのかこれで ^^)?

短いドキュメントを読み直してみた感じ、
Self-signed の証明書でよければこんなものみたいです。

Tag: debian dovecot imap ssl tls STARTTLS