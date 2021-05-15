Windows で netsh を簡単に使う
=====

Update: 2009-05-19



Windows のコマンドラインツール `netsh` を使うと、ネットワークの設定の変更などが自動化できます。かなり複雑な設定でもできます。便利なのですが、高機能な分、コマンドやパラメータなどの種類が多くてとっつきにくいです。IPアドレスを変えるだけといった簡単な操作を、簡単に実現する手順を説明します。

## 現状の設定を内容を表示する


`netsh` でネットワークカードの設定を表示・変更するコンテキストは `interface ip` です。そのコンテキストで `dump` コマンドを実行すると、私の PC の場合次のように表示されます。


```
C:\> netsh -c "interface ip"
netsh interface ip\>dump

# ----------------------------------
# インターフェイス IP 構成
# ----------------------------------
pushd interface ip

# "ローカル エリア接続" のインターフェイス IP 構成

set address name="ローカル エリア接続" source=dhcp
set dns name="ローカル エリア接続" source=dhcp register=PRIMARY
set wins name="ローカル エリア接続" source=dhcp

popd
# インターフェイス IP 構成の最後
```

## 元の設定に戻すスクリプトを作成する

上の出力例の先頭が `set` の行が設定内容です。この例の場合、すべて DHCP で設定していることがわかります。この先頭 `set` の行は `netsh` のコマンドの形式です。つまり、これらの行を保存しておいて、この PC の設定を変えた後、 `interface ip` コンテキストでそのまま実行すれば、元の設定に戻すことができます。



【注意】 上の例の “ローカル エリア接続” の部分は PC によって異なります。



そのためには、まず、次の内容のファイル `DHCPを使う.txt` を作成します。


```
set address name="ローカル エリア接続" source=dhcp
set dns name="ローカル エリア接続" source=dhcp register=PRIMARY
set wins name="ローカル エリア接続" source=dhcp
```

このファイルを使って次のオプションを指定して netsh を実行すれば、DHCP を使う設定に変更できます。


```
netsh -c "interface ip" -f DHCPを使う.txt
```

## いろいろな設定に変更するためのバッチを作成する

DHCP を使わない静的な IP アドレスを設定して `dump` コマンドを実行すると、私の PC の場合次のように表示されます。


```
C:\>netsh interface ip>dump

# ----------------------------------
# インターフェイス IP 構成
# ----------------------------------
pushd interface ip

# "ローカル エリア接続" のインターフェイス IP 構成

set address name="ローカル エリア接続" source=static addr=192.168.1.101 mask=255.255.255.0
set address name="ローカル エリア接続" gateway=192.168.1.1 gwmetric=0
set dns name="ローカル エリア接続" source=static addr=none register=PRIMARY
set wins name="ローカル エリア接続" source=static addr=none

popd
# インターフェイス IP 構成の最後
```

DHCP の例と同じように、次の内容のファイル `静的アドレスを使う.txt` を作成します。


```
set address name="ローカル エリア接続" source=static addr=192.168.1.101 mask=255.255.255.0
set address name="ローカル エリア接続" gateway=192.168.1.1 gwmetric=0
set dns name="ローカル エリア接続" source=static addr=none register=PRIMARY
set wins name="ローカル エリア接続" source=static addr=none
```

DHCP 設定用、静的アドレス用、それぞれのバッチファイルを作成します。



DHCPを使う.bat

```
netsh -c "interface ip" -f DHCPを使う.txt
ipconfig /ALL
```

静的アドレスを使う.bat


```
netsh -c "interface ip" -f 静的アドレスを使う.txt
ipconfig /ALL
```
