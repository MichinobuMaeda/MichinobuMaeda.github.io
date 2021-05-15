arno-iptables-firewall
=====

Update: 2017-11-26


リモートで管理する debian 9 のサーバで簡単にファイアウォールの設定ができないものか、
必要なポートを開けるだけでいいのだけどと探してみたところ、いいのがありました。

パッケージをインストールする際に設定内容を聞かれるるので、
インストールする前にネットワーク・インターフェイスの名前を調べておきます。
``/etc/network/interfaces`` などを見ればよいです。
debian 9 はデフォルトで ``ens33`` のような名前になります。

```
# apt-get install arno-iptables-firewall
```

ssh のポート 22 など最小限必要な設定はしておいてください。

一般的な Web サーバのために 22, 80, 443 を開けた場合、
``/etc/arno-iptables-firewall/conf.d/00debconf.conf``
は以下のようになります。

```
EXT_IF="ens33"
EXT_IF_DHCP_IP=1
OPEN_TCP="22 80 443"
OPEN_UDP=""
INT_IF=""
NAT=0
INTERNAL_NET=""
NAT_INTERNAL_NET=""
OPEN_ICMP=0
```

次に、サービスが起動しているかどうかを調べて、必要なら（必要です）起動の設定をします。

```
# service --status-all
# update-rc.d arno-iptables-firewall enable
# service arno-iptables-firewall start
```

Tag: debian firewall arno-iptables-firewall
