整理中：テスト用転送無しメールサーバ

2005-09-23



メール送信などのテストで使うためにローカルに置くメールサーバを Apache James でつくってみました。送信を受け付けたメールを他のサーバに全く転送しません。



James は毎分 2,000通を超えるメールを処理できるそうで、 スパム拒否の機能などもデフォルトで入っていてかなり高機能です。 設定の変更だけでいろいろできそうですが、 Servlet と同じようにフィルタや機能を自分で実装することが可能で、使い道はかなり広いようです。



今回はほとんどインストールしたまま、設定の変更は 1箇所だけで済ませました。

## 情報源

Javaメールアプリケーションプラットフォーム Apache Jakarta:JAMES詳解 ISBN: 4775303171

## 用意したもの

*   Java2 SDK 1.4.2 – JDK または JRE 1.3 以降で動作すると思います。
*   Apache James – 現時点の最新版 2.2.0 を使いました。

## インストールと設定

`james-2.2.0.zip` を適当なディレクトリに解凍します。 `C:\opt\james-2.2.0` に置きました。



`C:\opt\james-2.2.0\bin\run.bat` を起動します ( Windows の場合 ) 。するとこんな感じで起動します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5Zbm-CWI/AAAAAAAABqk/dLerZUShDvA/s1600/james_1.png)



`C:\opt\james-2.2.0\apps\james.sar` というのが Servlet なら WAR に相当するライブラリのようです。起動時に `C:\opt\james-2.2.0\apps\james` の下に次のようなディレクトリ構成が作成されます。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5aotGSDI/AAAAAAAABqo/5OOI-e_vDDM/s1600/james_2.png)



`telnet localhost 4555` で管理コンソールにログインします。管理アカウントはデフォルトで `root/root` です。 `help` コマンドで次のようなコマンドの一覧が表示されます。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5but4tgI/AAAAAAAABqs/3BjX4opOVT8/s1600/james_3.png)



ユーザ `test1` を追加しました。



`adduser test1 password`



`C:\opt\james-2.2.0\apps\james\SAR-INF\config.xml` を1箇所だけ変更しデフォルトの動作を「転送拒否」にします。



 `<!-- Send remaining mails to the transport processor`

 `for either local or remote delivery -->`

 `<mailet match="All" class="ToProcessor">`

 `<!-- <processor> transport </processor> -->`

 `<processor> relay-denied </processor>`

 `</mailet>`

 `</processor>`



最後に管理コンソールから `shutdown` して再起動して設定完了です。

## 動作の確認

メールクライアントに、ユーザ名 `test1` サーバは smtp, pop とも `localhost` のアカウントを設定します。そして、自分宛 ( `To: test1@localhost` ) のメールを送信して、受信してみます。すると受信できません。ローカルのユーザの場合の設定などが何もないので `relay-denied` として処理されているからです。 `C:\opt\james-2.2.0\apps\james\var\mail\relay-denied` を見ると、次のような 2つのファイルができています。



`4D61696C313132373437323636363735372D30.Repository.FileObjectStore`

`4D61696C313132373437323636363735372D30.Repository.FileStreamStore`



これらのうち `*.FileStreamStore` のほうは次のような ASCII 形式のデータです。



`Return-Path: <test1@localhost>`

`Received: from 127.0.0.1 ([127.0.0.1])`

 `by orange (JAMES SMTP Server 2.2.0) with SMTP ID 62`

 `for <test1@localhost>;`

 `Fri, 23 Sep 2005 19:51:06 +0900 (JST)`

`To: test1@localhost`

`Subject: =?iso-2022-jp?B?GyRCPCtKLDA4JWEhPCVrGyhC?=`

`From: "Test User #1 at Localhost" <test1@localhost>`

`Organization: localhost`

`Content-Type: text/plain; format=flowed; delsp=yes; charset=iso-2022-jp`

`MIME-Version: 1.0`

`Content-Transfer-Encoding: 8bit`

`Date: Fri, 23 Sep 2005 19:50:55 +0900`

`Message-ID: <op.sxjxq5i8pxtr8j@orange>`

`User-Agent: Opera M2/8.5 (Win32, build 7702)`

## 自分宛メール

Windows の場合このファイルの拡張子を `*.eml` にしてシステムのデフォルトのメールソフトで開くと次のように表示されます。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5cYp69NI/AAAAAAAABqw/PtSO81HV6Lo/s1600/james_4.png)



これらの 2つのファイルを Inbox のユーザアカウントのサブディレクトリ `C:\opt\james-2.2.0\apps\james\var\mail\inboxes\test1` に移動すると、メールクライアントから受信できるようになります。



次にメールクライアントに `test2@dummy.com` というアカウントを作成し、メールサーバは `localhost` とします。



このアカウントから実在するメールサーバ宛てにメールを送信すると、それも `relay-denied` の対象となり、 `C:\opt\james-2.2.0\apps\james\var\mail\relay-denied` にデータが残ります。



`Return-Path: <test2@dummy.com>`

`Received: from 127.0.0.1 ([127.0.0.1])`

 `by orange (JAMES SMTP Server 2.2.0) with SMTP ID 413`

 `for <test3@mmichi.com>;`

 `Fri, 23 Sep 2005 20:10:39 +0900 (JST)`

`To: test3@mmichi.com`

`Subject: =?iso-2022-jp?B?GyRCPEI6XyQ5JGslYSE8JWslNSE8JVAkS0F3Py4bKEI=?=`

`From: "Test User #1 at Localhost" <test2@dummy.com>`

`Organization: localhost`

`Content-Type: text/plain; format=flowed; delsp=yes; charset=iso-2022-jp`

`MIME-Version: 1.0`

`Content-Transfer-Encoding: 8bit`

`Date: Fri, 23 Sep 2005 20:10:33 +0900`

`Message-ID: <op.sxjynvjmllssr8@orange>`

`User-Agent: Opera M2/8.5 (Win32, build 7702)`



## 実在するメールサーバに送信

できました ↓



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5dCX4zLI/AAAAAAAABq0/H80zMYZNNug/s1600/james_5.png)
