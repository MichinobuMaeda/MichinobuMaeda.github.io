ubuntu 12.04 で resolv.conf が書き換えられる
=====

Update: 2012-08-25

まず最初に、 `resolve.conf` ではなく `resolv.conf` だそうです ^^;) bash の補完機能は便利ですねぇ ^^;;)

Ubuntu 10.04 のサーバを Ubuntu 12.04 server に置き換えるため、 OS インストールの後 `/etc/resolv.conf` の設定を書き換えました。そして、再起動すると、 resolv.conf の内容が書き換えられてしまいます。 Ubuntu 12.04 では `resolvconf` を使うので、 `/etc/resolvconf/resolv.conf.d/base` に書けばよいという話を聞いたの ( ソース不明 ) で Ubuntu 10.04 の旧サーバの `/etc/resolv.conf` の内容をそのままそこに書いて `sudo service resolvconf restart` としてみましたが、だめでした。旧サーバの `/etc/resolv.conf` の中の記述の順番に意味があるようなのですが、 resolvconf で書き換えたられた `/etc/resolv.conf` を見ると、順番が変わってしまっています。

そもそも resolvconf の正しい使い方はどうなの？ということで調べてみました。

まず、 Ubuntu がこのあたりの仕様を変えた理由はこちらです。

> Improvement to DNS resolving in Ubuntu
>
> [https://blueprints.launchpad.net/ubuntu/+spec/foundations-p-dns-resolving](https://blueprints.launchpad.net/ubuntu/+spec/foundations-p-dns-resolving)

いろいろなネットワークにつながっていて、利用する DNS も複数あるような場合に交通整理したい（超訳）ということのようです。 Desktop に関することは省略します。

Ubuntu のリリースノート [https://wiki.ubuntu.com/PrecisePangolin/ReleaseNotes/UbuntuServer](https://wiki.ubuntu.com/PrecisePangolin/ReleaseNotes/UbuntuServer) によると、この仕様変更についてはこちらを見ろとのことです。

> DNS in Ubuntu 12.04
>
> [http://www.stgraber.org/2012/02/24/dns-in-ubuntu-12-04/](http://www.stgraber.org/2012/02/24/dns-in-ubuntu-12-04/)

-   静的なIPの構成の場合は `/etc/network/interfaces` に "dns-nameservers", "dns-search", "dns-domain" を設定する。
-   /etc/resolvconf/resolv.conf.d/ の下のファイル `"base", "head", "tail"` に追加の設定を書くこともできる。
-   この仕組みを使いたくない場合は、シンボリックリンクになっている `/etc/resolv.conf` を普通のファイルにすることもできる。お勧めはしないけど。

というようなことを書いています。 Desktop に関することは省略します。

`/etc/network/interfaces` についてはこちらにサンプルがあります。

> Ubuntu Manpage: resolvconf - manage nameserver information
>
> [http://manpages.ubuntu.com/manpages/lucid/man8/resolvconf.8.html](http://manpages.ubuntu.com/manpages/lucid/man8/resolvconf.8.html)

それぞれのインターフェースに設定できるということのようです。うまく使えば不要な問い合わせを減らすことができるかもしれません。
