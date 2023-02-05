# できるだけ金をかけずに Linux の勉強をする

Update: 2011-03-20

LPI Japan が [Linux標準教科書](http://www.lpi.or.jp/linuxtext/text.shtml) をタダで配布しています。 Linux も Unix も全く触ったことがないような人にもおすすめです。ほんっとーに基本的なことから勉強することができます。しかしながら、テキストだけで勉強して身につくかというと、まあ、無理です。自分の指を動かして、基本的なコマンドなら無意識で打てるくらいにならないと、仕事では使えません。



IT関係の仕事をしている人は個人でもPC持っていることが多いと思います。でも、買ったときから Windows が入っていてしかも１台しかないとなると、そこに Linux を入れるのは少々たいへんです。知識か度胸のどちらかが必要です。ま、私のように Mac 買えば Unix のコマンドが使えるし... という話はおいといて、ほとんど金をかけずに Windows の環境を壊すことなく Linux を動かす手順を紹介します。



Linux にもいろいろ種類があって、詳しいことは [Linux標準教科書](http://www.lpi.or.jp/linuxtext/text.shtml) など読んでいただくとして、中には Windows PC に CD や USB メモリを突っ込むだけでいい [Knoppix](http://www.knoppix.net/) というものもあります。でも、 [Linux標準教科書](http://www.lpi.or.jp/linuxtext/text.shtml) で使っている CentOS とは微妙に違うところがあります。初めての人は少し迷うことがあるかもしれません。以下の手順では CentOS を動かす環境を作ります。



私の環境は以下の通りです。



> MacBook Pro で BOOTCAMP を使用。つまり Mac と Windows のデュアルブート
>
> CPU: 2.4 Ghz Intel Core 2 Duo
>
> RAM: 4 GB 1067 MHz DDR3
>
> HDD: 77.92 GB -- 半分以上空き
>
> OS: Windows 7 Ultimate



あ、念のため、 Mac OS X じゃなくて Windows の方を起動して実際に試した手順です。 MacBook も Windows を起動してしまえば、普通の Windows PC と全く同じです。私の場合、ちょっとキーボードが US 仕様だったり......するけど気にしない気にしない。

## 1\. VMware Player のインストール

VMware の "VM" というのは、たぶん、いや、まちがいなく Virtual Machine の略です。「 "仮想" ってなんかいきなり難しそうなものを」という人もいると思いますが、使い方は簡単です。で、タダです。こちらから入手します。

[http://www.vmware.com/products/player/](http://www.vmware.com/products/player/)

私が使ったもの、この記事を書いている時点の最新版は "VMware Player 3.1.3 for 32-bit and 64-bit Windows" です。ここから先、「IPアドレス」、「ネットマスク」、「デフォルトゲートウェイ」など TCP/IP の言葉が出てきますが、ここでは説明しません。 [Linux標準教科書](http://www.lpi.or.jp/linuxtext/text.shtml) の「9章 ネットワークの設定と管理」などをご参照ください。



作業に入る前に VMware Player をインストールする前のネットワークの設定内容を確認しておきます。普段このあたりを触ったことない人にはわけわかんないかもしれませんが、何も知らないまま先に進むとますますわけわかんないことになるので、自分の PC の現状を確認してください。



まずコントロールパネルを開いて、「ネットワークとインターネット」を選択します。


![](https://lh5.googleusercontent.com/-fzX_1bC_FR4/TXI8G8xHhQI/AAAAAAAAB7Y/ORgv-JTX-PA/vmwareplayer01.png)


「ネットワークの状態とタスクの表示」を選択します。


![](https://lh4.googleusercontent.com/-OWgmZVhveI4/TXI8G7O20oI/AAAAAAAAB7g/KewoCDiOfu8/vmwareplayer02.png)


「アダプターの設定の変更」を選択します。


![](https://lh5.googleusercontent.com/-QyN93u8jRdg/TXI8G6o_xAI/AAAAAAAAB7o/1x3QeXm9H7w/vmwareplayer03.png)


そこに、どんなアイコンが並んでいるかだけ覚えておいてください。意味不明なことも書いていると思いますが、少なくとも何個アダプターがあることになっているかだけでも。



とりあえずこれだけを確認したら、 VMware Player をインストールします。 "仮想" みたいな名前の製品ですが、インストールの手順は普通のアプリケーションとかわりません。私がダウンロードしたものは `"VMware-player-3.1.3-324285.exe"` というファイル名でした。これを実行して、設定内容はすべてデフォルトでインストールします。



インストール後、ネットワークアダプターが 2個増えています。 VMnet1 と VMnet8 です。ネットワークカードを追加したりはしていません。ソフトウェアの力で、あたかもネットワークアダプターが増えたかのように装っているわけです。この 2枚の仮想のネットワークアダプターは、仮想マシン:  Virtual Machine とこの PC を接続する仮想の LAN に接続されています。そんなもの接続した覚えはないと思っても、できています。


![](https://lh5.googleusercontent.com/-6Ej_I1i9OzQ/TXI8Gwxb1OI/AAAAAAAAB78/lF1SvfJX2Pk/vmwareplayer05.png)


これらの、仮想のネットワークアダプターがどんな設定になっているのか見てみます。それぞれのアイコンをマウスで右クリックして、ポップアップメニューからプロパティを開いてください。


![](https://lh3.googleusercontent.com/-oBwrONRj2Xg/TXI8G86VISI/AAAAAAAAB8E/YHhpmtGXKsk/s400/vmwareplayer06.png)

"インターネット プロトコル バージョン 4 (TCP/IPv4)" を選択して、ボタン「プロパティ」をクリックします。ここに表示される内容は PC によって異なります。私の PC の場合と違っていても気にしないでください。 VMnet1 はこんな感じ。


![](https://lh4.googleusercontent.com/-dBruiN4ZRJU/TXI8G_jSRaI/AAAAAAAAB8M/ErOnYedQxmc/s400/vmwareplayer07.png)


VMnet8 はこんな感じ。なぜ、一方に静的な IPアドレスが設定され、もう一方が DHCP を使う設定になっているのは不明です。後述しますが、 DHCP を使う設定になっていても、必ず決まった IPアドレスが割り与えられるようになっています。


![](https://lh4.googleusercontent.com/-6ld08nY5Zgc/TXI8G3nSalI/AAAAAAAAB8U/0I7gU7tCnNI/s400/vmwareplayer08.png)


ここまでの設定内容は、コマンドプロンプト ( いわゆる "DOS窓" ) でも見ることができます。 `"ipconfig"` コマンドを実行してください。以下、私の PC の場合。関係ないアダプターの情報は省略。


```
C:\Users\michinobu>ipconfig
...
イーサネット アダプター VMware Network Adapter VMnet1:
 接続固有の DNS サフィックス . . . :
 リンクローカル IPv6 アドレス. . . . : fe80::b9a7:2483:6f5c:e36d%27
 IPv4 アドレス . . . . . . . . . . : 192.168.190.1
 サブネット マスク . . . . . . . . : 255.255.255.0
 デフォルト ゲートウェイ . . . . . :
イーサネット アダプター VMware Network Adapter VMnet8:
 接続固有の DNS サフィックス . . . :
 リンクローカル IPv6 アドレス. . . . : fe80::2159:3faf:d0ea:15bd%28
 IPv4 アドレス . . . . . . . . . . : 192.168.71.1
 サブネット マスク . . . . . . . . : 255.255.255.0
 デフォルト ゲートウェイ . . . . . :
...
```

DHCP を使う設定になっている VMnet8 の IPアドレスが 192.168.71.1 になっていることだけ頭に入れておきます。みなさんの PC では違う値になってるかもしれません。

## 2\. インストールメディアの入手

CentOS 5.x のインストールイメージの入手はこちらから。



[http://mirror.centos.org/centos/5/isos/](http://mirror.centos.org/centos/5/isos/)



自分の PC が 32bit だか 64bit だかよくわからない場合は 32bit の方を選択してください。


[http://isoredirect.centos.org/centos/5/isos/i386/](http://isoredirect.centos.org/centos/5/isos/i386/)



私が使ったのは `"CentOS-5.5-i386-bin-DVD.iso"` です。拡張子 `".iso"` というのは CD や DVD の ISO フォーマット（つまりようするに規格で決まったとおりのフォーマット）そのままのデータをファイルにしたもの、とう意味です。

## 3\. 仮想マシンの作成

VMware Player に Linux をインストールします。仮想マシンというものがどういうものなのか、よくわからなくても、動けば OK 、動かせばわかります。なにはともあれ VMware Player を起動します。



![](https://lh5.googleusercontent.com/-uSSbirN3kBI/TXI8GwsXFoI/AAAAAAAAB88/eZJdXU2UpTc/vmwareplayer17.png)



「新規仮想マシンの作成」を選択します。



![](https://lh5.googleusercontent.com/-w9LVzmIqsV4/TXI8G1nrGNI/AAAAAAAAB7M/fWS8SkVhiug/s400/vmwareplayer10.png)



長くなるので詳しい説明は省略しますが、学習に適した環境をつくるため、それから、 Linux のインストールに慣れるために、ここでは「後で OS をインストール」を選択してください。



![](https://lh3.googleusercontent.com/-SLJ4Aab9uC0/TXI8G2CBu2I/AAAAAAAAB7M/2-3WogthrdY/s400/vmwareplayer11.png)



ゲスト OS ( 仮想マシンにインストールする OS ) は "Linux" です。「バージョン」は "CentOS" を選択してください。



![](https://lh6.googleusercontent.com/-lMonyhjFPew/TXI8G68kniI/AAAAAAAAB7M/YZ4IjOdl8DE/s400/vmwareplayer12.png)



「仮想マシン名」はご自由に。ディスク容量が十分ある場合、格納場所はデフォルトでいいでしょう。



![](https://lh4.googleusercontent.com/-Vxx1EZk_kjI/TXI8G80uTNI/AAAAAAAAB7M/nS7nu5Rn3aw/s400/vmwareplayer13.png)



仮想マシンのハードディスクの実態は、Windows のファイルシステム上の大きなファイルです。興味のある人は、後でできあがったファイルの名前やサイズなど見てみるといいでしょう。ディスク最大サイズは大きめでもだいじょうぶです。 VMware Player は、実際にファイルなどを保存した領域に必要なだけのファイルを生成します。最大 20 GB の設定でも、実際に 2 GB しか使わなければ、 2 GB 程度のファイルが生成されるだけです。



仮想ディスクを単一のファイルとするか、複数のファイルに分割するかはお好みで。特にバックアップのことなど考えなくてよければ、デフォルトの単一のファイルでいいです。



設定を完了すると、左側、「ホーム」の下に仮想マシンが出現しますので、選択します。



![](https://lh5.googleusercontent.com/-uSSbirN3kBI/TXI8GwsXFoI/AAAAAAAAB88/eZJdXU2UpTc/vmwareplayer17.png)



ここでもう少し細かな設定を。「仮想マシン設定の編集」を選択します。



![](https://lh3.googleusercontent.com/-flCx4k4Stpw/TXI8GxmZZhI/AAAAAAAAB8k/1VptI3dwssw/vmwareplayer14.png)



メモリは、学習用途であれば 512 MB もあれば十分だと思います。



![](https://lh5.googleusercontent.com/-u-2hiBPP53k/TXI8G9MfuiI/AAAAAAAAB8s/6iS6DQ9LD5I/vmwareplayer15.png)



CD/DVD には CentOS の ISO イメージのファイルを指定してください。これで、あたかも本物の DVD が挿入されているかのように動作します。



![](https://lh5.googleusercontent.com/-rf_ehKx65Cc/TXI8G1ObVkI/AAAAAAAAB80/WWRGUQrhbTQ/vmwareplayer16.png)



ネットワークアダプタは NAT を選択してください。学習用途の場合この選択が無難です。



![](https://lh5.googleusercontent.com/-uSSbirN3kBI/TXI8GwsXFoI/AAAAAAAAB88/eZJdXU2UpTc/vmwareplayer17.png)



設定が終わったら、 "仮想マシンの再生" を選択します。すると、たぶん、次のようなダイアログが出てきます。



![](https://lh4.googleusercontent.com/-T9O0Hz2znIg/TXI8GywKs0I/AAAAAAAAB7M/HWVhRE65qEM/s400/vmwareplayer18.png)



読んだら \[ OK \] を押します。次のようなダイアログも出てきます。



![](https://lh4.googleusercontent.com/-b9BmwmD0u6g/TXI8G_VijMI/AAAAAAAAB7M/7HUMP8r6b34/vmwareplayer19.png)



詳しい説明は省略しますが、少なくともじゃまなものではないので \[ ダウンロードしてインストール \] しておいてください。



![](https://lh4.googleusercontent.com/-SaSkKTarABs/TXI8G17yhNI/AAAAAAAAB7M/qVqUWOl8oEU/s400/vmwareplayer20.png)



インストーラが起動しすると、まず、グラフィカルモードかテキストモードかの選択が迫られます。グラフィカルモードの方が少し楽なのですが、どちらでも大差有りません。環境によってはグラフィカルモードがうまく動いてくれないことがあるので、テキストモードを選択します。



![](https://lh6.googleusercontent.com/-QgTZ_7fDKec/TXI8G9PYstI/AAAAAAAAB7M/4A4U8bZfGg8/s400/vmwareplayer21.png)



インストールメディアのチェックは、やりたければ \[ OK \] 、やりたくなければ \[ Skip \] 、画面の一番下にあるように、\[Tab\] \[Space\] などのキーで移動して選択します。



![](https://lh3.googleusercontent.com/-iYCgrE2l3Io/TXI8G6m9S7I/AAAAAAAAB9E/zsRarHexoXk/vmwareplayer22.png)



インストーラの言語を選択しろとのことですが、 "Japanese" を選択しても「ごめん、英語じゃないとダメなんだ」と後で言われるだけなので、 "English" のまま \[ OK \] します。



![](https://lh6.googleusercontent.com/-j_D8RAJzg3k/TXI8Gyp4xhI/AAAAAAAAB9M/c1zqhDGAqyI/vmwareplayer23.png)



キーボードの選択。ほとんどの人は "jp106" だと思います。私は違うけど。



![](https://lh6.googleusercontent.com/-6d6FVOVzfC8/TXI8G1r4yAI/AAAAAAAAB9U/ROWkvrR4C7w/vmwareplayer24.png)



「ディスク全部消しちゃうぞ」は \[ OK \]



![](https://lh5.googleusercontent.com/-kBEYEg-ZyXg/TXI8G9KHYPI/AAAAAAAAB9c/I22UngetNos/s400/vmwareplayer25.png)



いろいろ書いてますが、デフォルトの "Remoce linux partitions ..." で \[ OK \]



![](https://lh5.googleusercontent.com/-wDX-yjiidMI/TXI8G_nXdhI/AAAAAAAAB9k/lthXTI94tfM/s400/vmwareplayer26.png)



再び「ディスク全部消しちゃうぞ」は \[ OK \]



![](https://lh4.googleusercontent.com/-uNzTvG7wi4I/TXI8G8BuUgI/AAAAAAAAB9s/7ih48N1QuP0/vmwareplayer27.png)



「パーティションのレイアウト見るか」？は \[ YES \]



![](https://lh6.googleusercontent.com/-gjbwpuzztjA/TXI8G1OEPZI/AAAAAAAAB9w/3_jGkjXtU10/s400/vmwareplayer28.png)



初めての人にはわけわかんないですが、見るだけ見ておいてください。



![](https://lh5.googleusercontent.com/-j3IGcTCl2CQ/TXI8G8wTaHI/AAAAAAAAB94/Sa7AnZSaKDs/s400/vmwareplayer29.png)



"Boot Loader" の設定はデフォルトのままで。



![](https://lh3.googleusercontent.com/-Asc-moAVQsk/TXI8G8odEaI/AAAAAAAAB-E/63VydQq3i5A/s400/vmwareplayer30.png)



これも "Boot Loader" の設定。デフォルトのままで。



![](https://lh3.googleusercontent.com/-QOmayIURw1Q/TXI8G7pZt9I/AAAAAAAAB-M/r_t2-jpOYko/s400/vmwareplayer31.png)



これも "Boot Loader" の設定。デフォルトのままで。



![](https://lh4.googleusercontent.com/-pg8pruNGqhA/TXI8GyDK6PI/AAAAAAAAB-U/SIFTdySPbNM/s400/vmwareplayer32.png)



これも "Boot Loader" の設定。デフォルトのままで。



![](https://lh3.googleusercontent.com/-cPrjuXT0i54/TXI8G08h0XI/AAAAAAAAB-c/X6TCiV574tE/s400/vmwareplayer33.png)



これも "Boot Loader" の設定。デフォルトのままで。



![](https://lh3.googleusercontent.com/-sq7Wf5efuBc/TXI8G6ZlN6I/AAAAAAAAB-k/FQuJ7iMVCjo/vmwareplayer34.png)



「ネットワークインターフェースの設定をするか？」は \[ Yes \]



![](https://lh5.googleusercontent.com/-TH4g0DFo2Ho/TXI8G3FrdYI/AAAAAAAAB-s/-HwITK6bI04/s400/vmwareplayer35.png)



"Activate on boot" ( 起動時に有効にする ) と、 "Enable IPv4 support" を "\*" にします。 "\*" は\[Space\] で切り替えできます。



![](https://lh3.googleusercontent.com/-wcb0elMbInI/TXI8G9NNw6I/AAAAAAAAB-0/3aVbI75wxhs/s400/vmwareplayer36.png)



「DHCP を使うか？自分で IPアドレスを設定するか？」は、とりあえず DHCP で。後で変更できます。詳しくはテキスト参照。



![](https://lh3.googleusercontent.com/-8P6zSDYe0_M/TXI8G5ENJoI/AAAAAAAAB-8/TvpBbSTp2Aw/s400/vmwareplayer37.png)



「ホスト名 ( Windows でいうところのコンピュータ名 ) を DHCP に決めてもらうか？」ですが、 VMware 環境ではたぶん無理なので、自分で決める "manually" を選択して、何か適当な名前を入れます。



![](https://lh5.googleusercontent.com/-EGOVcItnRdg/TXI8G0gzMOI/AAAAAAAAB_E/mbFYJF1ReDE/vmwareplayer38.png)



「システムクロックに UTC を使うか？」は、 Windows と同じ、使わない、にしておきます。タイムゾーンは自分がいるところ、日本国内であれば "Asia/Tokyo" です。



![](https://lh3.googleusercontent.com/-yhk0b-lUVWw/TXI8Gx4NAPI/AAAAAAAAB_I/qRZijhGY7xg/s400/vmwareplayer39.png)



root ユーザのパスワードは、何か設定してください。試してないですが、パスワード無しにはたぶんできないと思います。また、実際に Linux を使い始めると「 root ユーザのパスワードがないなんて想定外」というケースが多々あるだろうと思います。



![](https://lh6.googleusercontent.com/-D-rzod3xSgY/TXI8GzScjxI/AAAAAAAAB_Q/zIgoPQSfkC8/s400/vmwareplayer40.png)



インストールするパッケージについて、おおざっぱに決めることができます。学習用途の場合 "Server - GUI" が無難です。



![](https://lh4.googleusercontent.com/-awAQLmRECVQ/TXI8G6q6l9I/AAAAAAAAB_U/uvSAt65fp08/s400/vmwareplayer41.png)



ここで \[ OK \] すると、あとはインストーラがすべてやってくれます。 "/root/install.log" と書かれていることを覚えておいてください。



![](https://lh6.googleusercontent.com/-RUuO9QAbcyw/TXI8G7O8UGI/AAAAAAAAB_c/3gmqZcglLyM/s400/vmwareplayer44.png)



インストールが終わったら \[ Reboot \] します。再起動するとなにやら起動します。



![](https://lh3.googleusercontent.com/-p2_A2uNQ1Io/TXI8G3oB5PI/AAAAAAAAB_k/vhQkLv8Wj0w/s400/vmwareplayer45.png)



とりあえず \[ Exit \] でいいです。ここで設定することの大半は、テキストのお勉強の中でやることになります。で、ここからが本番。



![](https://lh5.googleusercontent.com/-DHGc_LFC7-A/TXI8GyfziSI/AAAAAAAAB7M/kE5G7dmeQEE/s400/vmwareplayer46.png)



Windows しか知らない人には、なんじゃこら？です。ユーザ名 root とパスワードを入力してログインしてください。ログインしても日付が表示されるだけです。愛想の無いことこの上ないです。当面、次の 2個のコマンドだけを覚えておいてください。それ以外は [Linux標準教科書](http://www.lpi.or.jp/linuxtext/text.shtml) 参照。



まず、ネットワークの設定を見るコマンド "ifconfig" です。



```
[foo@bar ~]# ifconfig
```

ここまでと同じ手順で CentOS をインストールした場合、ネットワークアダプターの名前は "eth0" ( Ethernet の 0番目 ) です。 "eth0" の設定だけを見たい場合は、その名前を指定します。



```
[foo@bar ~]# ifconfig eth0
```

このコマンドで、仮想マシンの IPアドレスを調べておいてください。私の場合 192.168.71.128 になっていました。後で、ネットワークの導通確認に使います。



次に、シャットダウン、または、リブートするコマンド "shutdown" です。



```
[foo@bar ~]# shutdown -h now
```

これが「今すぐ問答無用でシャットダウン」



```
[foo@bar ~]# shutdown -r now
```

これが「今すぐ問答無用で再起動」です。



この仮想マシンがおかしくなったからといって、 Windows の環境に影響を及ぼすことはありませんから、気軽にシャットダウンや再起動など試してみてください。

## 4\. ネットワークの導通の確認

TCP/IP のネットワークが通じているかどうかを確認する一番簡単な方法は "ping" コマンドを打ってみることです。しかしながら、たぶん Windows 7 のデフォルトの設定では外からの ping は受け付けないようになっています。とはいえ、ホスト名 ( コンピュータ名 ) ではなく IPアドレスを指定した "ping" で片方から通じ、もう片方からは通じないことはめったにないので、 Windows から Linux の仮想マシンに向けてだけ試してみることにします。



コマンドプロンプト ( いわゆる DOS窓 ) を開き、 Linux の仮想マシンの方で "ifconfig" を使って確認した IPアドレス宛に "ping" します。



```
C:\Users\michinobu> ping 192.168.71.128
```

これで、何か「反応返ってこないんですけどぉ」みないなメッセージが出なければ OK です。

## 5\. 仮想ネットワークの DHCP の設定について

DHCP について詳しいことは [Linux標準教科書](http://www.lpi.or.jp/linuxtext/text.shtml) には書いていません。 [Linuxサーバー構築標準教科書](http://www.lpi.or.jp/linuxtext/server.shtml) にもなさそう。設定ファイルの中身を見て、ここで必要な最小限のことを理解していただきましょう。

 Windows 7 の場合、次の場所に、仮想ネットワークの DHCP の設定ファイルがあります。



```
C:\ProgramData\VMware\vmnetdhcp.conf
```

Windows Vista もたぶん同じ場所、 Windows XP などの場合は `C:\Program Files\` の下じゃないかな。


```
allow unknown-clients;
default-lease-time 1800;                # default is 30 minutes
max-lease-time 7200;                    # default is 2 hours
```

ここから VMnet1



まず、ネットワークアドレスとネットマスク


```
# Virtual ethernet segment 1
# Added at 03/05/11 17:22:54
subnet 192.168.190.0 netmask 255.255.255.0 {
```

DHCPクライアントに割り当てる IPアドレスの範囲



```
range 192.168.190.128 192.168.190.254;            # default allows up to 125 VM's
```

その他の設定


```
option broadcast-address 192.168.190.255;
option domain-name-servers 192.168.190.1;
option domain-name "localdomain";
default-lease-time 1800;
max-lease-time 7200;
}
```

Windows のネットワークインターフェースの設定



必ず 192.168.190.1 を割り当てることになっている。


```
host VMnet1 {
 hardware ethernet 00:50:56:C0:00:01;
 fixed-address 192.168.190.1;
 option domain-name-servers 0.0.0.0;
 option domain-name "";
}
# End
```

ここから VMnet8



まず、ネットワークアドレスとネットマスク


```
# Virtual ethernet segment 8
# Added at 03/05/11 17:22:54
subnet 192.168.71.0 netmask 255.255.255.0 {
```

DHCPクライアントに割り当てる IPアドレスの範囲



```
range 192.168.71.128 192.168.71.254;            # default allows up to 125 VM's
```

その他の設定


```
option broadcast-address 192.168.71.255;
option domain-name-servers 192.168.71.2;
option domain-name "localdomain";
option netbios-name-servers 192.168.71.2;
option routers 192.168.71.2;
default-lease-time 1800;
max-lease-time 7200;
}
```

Windows のネットワークインターフェースの設定



必ず 192.168.71.1 を割り当てることになっている。


```
host VMnet8 {
 hardware ethernet 00:50:56:C0:00:08;
 fixed-address 192.168.71.1;
 option domain-name-servers 0.0.0.0;
 option domain-name "";
 option routers 0.0.0.0;
}
# End
```

## 6\. おまけ : コマンドプロンプトの設定

Linux のお勉強をしていると、 Windows でもコマンドプロンプト ( いわゆる DOS窓 ) を使う機会が増えます。例えば、ネットワークの設定の変更などのたびに "ping" することになります。



コマンドプロンプトのデフォルトの設定では、ウィンドウが小さくて、Cut ＆ Paste も面倒なので、私は次のように設定変更しています。



![](https://lh5.googleusercontent.com/-9NbZWAI43OE/TXI8G1yXZkI/AAAAAAAAB7M/HHEIA_zTQE4/s400/vmwareplayer43.png)



「簡易編集モード」と「挿入モード」にチェックを入れます。



![](https://lh6.googleusercontent.com/-u9QgWr4Z9iA/TXI8G9ecJSI/AAAAAAAAB7M/8COEv3BxLCE/s400/vmwareplayer42.png)



「画面のバッファーサイズ」と「ウィンドウのサイズ」それぞれの「幅」と「高さ」を増やします。
