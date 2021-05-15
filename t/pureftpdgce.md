Pure-FTPd の Google Compute Engine 向けの設定
=====

Update: 2019-03-16


クラウドで FTP サーバを動かす用があって、
Google Compute Engine に Pure-FTPd を入れてみました。

なぜ Pure-FTPd を選んだのかというと、
ProFTPD や vsftpd よりセキュアだとされていて
( [Evaluating FTP Servers: ProFTPd vs PureFTPd vs vsftpd | systemBash](https://systembash.com/evaluating-ftp-servers-proftpd-vs-pureftpd-vs-vsftpd/) ) 、
chroot した仮想ユーザの設定が楽だからです。
インストールの基本的な手順は
[Setup Pure-FTPd With TLS on Debian 9](https://www.vultr.com/docs/setup-pure-ftpd-with-tls-on-debian-9)
を参考にしました。

Google Cloud や AWS などのクラウド環境の場合、以下の追加の設定が必要です。
## Firewall のポートの穴あけ

Port 21 の他、 PassivePortRange に設定したポートの穴を開ける必要があります。
Passive ではないモードも使うのなら 20 も必要かな。
詳しくは、それぞれのクラウドサービスのマニュアルを見てください。

## External IP

Google Compute Engine の場合、
``sudo ifconfig`` とかしたときに表示される Internal IP と、
外から接続するときに使う External IP が異なります。
Passive 接続する FTP クライアントにその External IP
を明示的に教えてあげないとダメな場合があります。
そのあたりの動作は FTP クライアントによって違うようで、
明示的に教えてあげなくても、最初に接続した External IP を使うクライアントもあります。
そうでない場合、どうも Internal IP に接続しようとしてしまうようです。

設定は簡単で、
``/etc/pure-ftpd/conf/ForcePassiveIP``
というファイルを無ければ追加して External IP を記載すればいいです。
設定の反映のために ``sudo service pure-ftpd restart`` してください。
( [Enable passive mode for Pure-ftpd on AWS](http://getasysadmin.com/2012/12/enable-passive-mode-for-pure-ftpd-on-aws/) )

Tag: Pure-FTPd Cloud