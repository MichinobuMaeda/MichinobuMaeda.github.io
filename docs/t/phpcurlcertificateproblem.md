# Windows で PHP の curl が証明書のエラーを出したら

Update: 2019-01-04


Windows で PHP のテストをしていたら

> SSL certificate problem: unable to get local issuer certificate ...

のようなエラーが出ました。どうも curl
が出しているようなのですが、「なんか足りてない？」と調べてみたら確かに私の環境には設定されてなかったですよ。。。

[SSL certificate problem: unable to get local issuer certificate](https://github.com/rollbar/rollbar-php/issues/334)
によると、まず https://curl.haxx.se/ca/cacert.pem
から curl 用の証明書をダウンロードして、どこかに置きます。
``C:\php\extras\ssl`` あたりがいいかな。

次に、その場所を php.ini に記載します。

```
[curl]
; A default value for the CURLOPT_CAINFO option. This is required to be an
; absolute path.
curl.cainfo = C:\php\extras\ssl\cacert.pem
```

これで OK

Tag: PHP curl SSL
