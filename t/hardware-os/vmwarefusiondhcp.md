VMware Fusion の DHCP の設定
=====

Update: 2011-02-20

私の MacBook の VMware Fusion 3 に Ubuntu 10.10 Server を複数インストールしました。 ssh 使っていろいろしたくて IPアドレスは固定にしたかったのですが、 NAT や Host Only の仮想ネットワークで効いている DHCP の設定はどうなっていたっけ？とりあえずリース範囲外のアドレスを使いたいんだけど、と設定ファイルを探したのですが、見つかりません。



とはいえ、世の中には物好きな ( 失礼 ) 人がいるもので、こんな資料 [How to modify Fusion network settings whitepaper](http://communities.vmware.com/thread/97712) がありました。 PDF の資料はこちら [VMware Fusion Network Settings – Part1](http://communities.vmware.com/servlet/JiveServlet/download/718890-1931/VMware%20Fusion%20Network%20Settings%20-%20Part%201.pdf) です。



DHCP の設定ファイルはこんな奥まったところにあります。Mac OS X だからなぁ。。。



```
/Library/Application Support/VMware Fusion/vmnet1/dhcpd.conf
/Library/Application Support/VMware Fusion/vmnet8/dhcpd.conf
```



この周辺に、他の設定ファイルもいろいろあるようです。
