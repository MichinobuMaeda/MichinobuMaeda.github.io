Debian 9 から 10 にアップデート
=====

Update: 2020-07-11


このサーバで Debian 9 を使っていたのですが、
Debian 10 が出てからしばらく経つのでアップデートすることにします。

参考にしたのはこちら https://phoenixnap.com/kb/how-to-upgrade-debian-9-stretch-to-debian-10-buster

まず設定をバックアップ

```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

次に ``/etc/apt/sources.list`` の中の ``stretch`` をすべて ``buster`` に変えます。

このサーバに追加した参照先 ( ``/etc/apt/sources.list.d/`` の下 ) も同様に変更します。

  * ``deb <nowiki>https://deb.nodesource.com/node_10.x</nowiki> stretch main``
  * ``deb <nowiki>https://packages.sury.org/php/ stretch</nowiki> main``

で、次に ``sudo apt ...``  っていやまてこのページの編集しながらではダメだろ。。。というわけでいったん保存。

念のためデータや ``/etc`` を手元の PC にバックアップして、

```
sudo apt update
sudo apt upgrade
```

とやってる最中に ``arno-iptables-firewall`` が何やらエラーを表示。
で、いやな予感の通り ``ssh`` のセッションが切れてしまったと思ったらネットワークが全くつながらない。
サーバ屋さんが用意してくれている Web のコンソールから入り直して、
とりあえず ``arno-iptables-firewall`` をアンインストールして ``iptables`` をリセット。

https://kerneltalks.com/virtualization/how-to-reset-iptables-to-default-settings/

```
sudo apt remove arno-iptables-firewall
sudo iptables -P INPUT ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -F
```

で、 ``ssh`` がつながるようになったので残りを実行。

```
sudo apt dist-update
sudo shutdown -r now
```

``arno-iptables-firewall`` は再インストール。
アンインストールする前の [設定ファイル](arnoiptablesfirewall.html) は残っていたので再設定は不要でした。


Tag: debian iptables arno-iptables-firewall



