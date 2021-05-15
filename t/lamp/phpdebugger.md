PHPのデバッグができる環境
=====

Update: 2010-05-16

## 今回の制約

開発をしている人の場合、今でもまだ Windows XP を使い続けている人が多いと思いますが、私の MacBook に入っている Windows 7 をそのまま使いました。 Zend Debugger をセットアップするには Zend Server を入れるのが一番手っ取り早いのですが Windows 7 にはうまく入りませんでした ( 注：この記事を書いた時点のバージョンの話です ) 。それで、 XAMPP を使うことにしました。



それから、単体の Zend Debugger の PHP 5.3 用のものが入手できませんでした。したがって、 XAMPP は最新ではなく、 PHP 5.2 が入っている 1.6x を使うことにしました。



以下の文章でバックスラッシュ "\\"  ( ← 表示されていないかも？ ) が表示されているところは、半角の円マーク "￥" ( ← 表示されていないかも？ ) に読み替えてください。

## XAMPP のインストール

[http://sourceforge.net/projects/xampp/files/](http://sourceforge.net/projects/xampp/files/) から `xampp-win32-1.6.8.exe` をダウンロードします。このファイルは自己解凍圧縮ファイルになっていて、実行するとフォルダ xampp ができます。そのフォルダを `C:\` の直下に移動しました。



次に `c:\xampp\setup_xampp.bat` を実行します。数秒で完了します。



サーバの起動は `c:\xampp\xampp_start.exe` 終了は `c:\xampp\xampp_stop.exe` です。



サーバを起動すると、初回起動時は次のようなダイアログが表示されるので、 「 アクセスを許可する 」 を選択してください。





![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5zK7VD3I/AAAAAAAABrw/CgClkw_VIE0/s1600/zend-debugger-000.png)





![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw506ukVnI/AAAAAAAABr0/wiFSxxmZqw8/s1600/zend-debugger-001.png)



サーバを起動したら、ブラウザで `http://localhost/` を表示します。表示したら「日本語」を選択します。管理メニューが表示されるので、

*   phpinfo()
*   phpMyAdmin

などが正常に表示できることを確認します。

## Zend Debugger の設定（サーバ側）

[http://www.zend.com/community/pdt](http://www.zend.com/community/pdt) のページのリンク “download the Zend Debugger extension binaries” をクリックして [http://downloads.zend.com/pdt/server-debugger/](http://downloads.zend.com/pdt/server-debugger/) を開きます。そこから `ZendDebugger-5.2.15-cygwin_nt-i386.zip` をダウンロードして解凍します。



インストールの手順は `ZendDebugger-5.2.15RC1-cygwin_nt-i386\README.txt` に書いてあります。



まず `ZendDebugger-5.2.15RC1-cygwin_nt-i386\5_2_x_comp\ZendDebugger.dll` を `C:\xampp\php\ext\ZendDebugger.dll` にコピーします。



次に `ZendDebugger-5.2.15RC1-cygwin_nt-i386\dummy.php` を `C:\xampp\htdocs\dummy.php` にコピーします。



設定ファイル `C:\xampp\apache\bin\php.ini` ＜注意＞`C:\xampp\php\php.ini` ではない＜／注意＞ に



```
[Zend]
zend_extension_ts = "C:\xampp\php\zendOptimizer\lib\ZendExtensionManager.dll"
zend_extension_manager.optimizer_ts = "C:\xampp\php\zendOptimizer\lib\Optimizer"
zend_optimizer.enable_loader = 0
zend_optimizer.optimization_level=15
;zend_optimizer.license_path =
```



という記述があるのですが、これを次のように修正します。セクションの先頭の行はセミコロン 「 ;　」 でコメントアウトしてください。



```
[Zend]
;zend_extension_ts = "C:\xampp\php\zendOptimizer\lib\ZendExtensionManager.dll"
zend_extension_ts= "C:\xampp\php\ext\ZendDebugger.dll"
zend_debugger.allow_hosts=127.0.0.1
zend_debugger.expose_remotely=always
zend_extension_manager.optimizer_ts = "C:\xampp\php\zendOptimizer\lib\Optimizer"
zend_optimizer.enable_loader = 0
zend_optimizer.optimization_level=15
;zend_optimizer.license_path =
```



ファイルを保存して閉じたら、 `c:\xampp\xampp_restart.exe` でサーバをリスタートします。その後、管理メニューの phpinfo() を再表示してください。セクション “Zend Debugger” が表示されていれば OK です。





![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw52e5_shI/AAAAAAAABr4/K9e67K-7BPU/s1600/zend-debugger-002.png)



## Eclipse のインストール

Eclipse は Java で動きます。まず最初に、 PC に Java が入ってるかどうかを確認してください。コマンドプロンプトで次のようになれば OK です。



```
C:\Users\michinobu>java -version
java version "1.6.0_20"
Java(TM) SE Runtime Environment (build 1.6.0_20-b02)
Java HotSpot(TM) Client VM (build 16.3-b01, mixed mode, sharing)`
```


Java が入っていない場合、および、上記のバージョンより古い場合は [http://www.java.com/ja/](http://www.java.com/ja/) からダウンロードしてインストールしてください。



今回は、 [http://www.eclipse.org/](http://www.eclipse.org/) から配布されているものではなく、日本語化されていて、 PHP のためのプラグインも入っているものを利用します。



[http://mergedoc.sourceforge.jp/](http://mergedoc.sourceforge.jp/) から 「 Eclipse 3.5.2 Galileo Windows 32bit ベース 」 を選択します。 Java などは関係ないので、 「 Pleiades All in One PHP 」 の 「 Standard All in One 」 をダウンロードします。ファイル名は `pleiades-e3.5-php_20100226.zip` でした。



これを解凍すると中にたくさんのファイルが入ったフォルダ `eclipse` ができます。そのフォルダを `C:\` の直下に移動しました。 `C:\eclipse\eclipse.exe` を実行すると Eclipse が起動します。ショートカットなど作っておくといいでしょう。



起動時に 「 ワークスペース 」 の場所を聞かれます。 PHP の開発のためだけに使うので、 `C:\xampp\htdocs` にしました。こうしておくと、編集したファイルをすぐそのままブラウザで確認できますし、デバッガの設定も楽です。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw53a3POjI/AAAAAAAABr8/m4iGcmlWpCw/s1600/zend-debugger-003.png)



また、次のようなダイアログが表示されるので、 「 アクセスを許可する 」 を選択してください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw54xZQYLI/AAAAAAAABsA/n9AuMPF3xUY/s1600/zend-debugger-004.png)



初回起動時には “Welcome” 画面が表示されますが、じゃまなだけなのでとりあえず消してください。

## Eclipse の設定

Eclipse の基本的な設定はメニュー 「 ウィンドウ 」 「 設定 」 を使います。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw56DvYWUI/AAAAAAAABsE/ROXcmAGd-Kc/zend-debugger-005.png)



私の場合次のような個所をカスタマイズします。



*   一般のファイルのエンコード

![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw57sbrdAI/AAAAAAAABsI/RqBrzTkDvqQ/zend-debugger-006.png)

*   HTML ファイルのエンコード

![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw58uqCJSI/AAAAAAAABsM/Qwryti30yxs/s400/zend-debugger-007.png)

*   HTML のタブとインデント

![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5-l3GZ6I/AAAAAAAABsQ/riWaZMS0fSs/zend-debugger-008.png)

*   PHP のタブとインデント

![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5_YcW_4I/AAAAAAAABsU/sacLF3WIME4/zend-debugger-009.png)



Eclipse のデフォルトの設定は一般的によくつかわれるものになっているので、これ以上細かくは変更せずに使っています。

## デバッガの実行

テスト用のファイル `C:\xampp\htdocs\test\index.php` を以下の手順で作成します。



まず、プロジェクト test を新規で作成します。メニュー 「 ファイル 」 「 新規 」 「 PHP プロジェクト 」 を選択します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6AZn_qFI/AAAAAAAABsY/L6n4zvb1pHI/s400/zend-debugger-010.png)



プロジェクト名に `test` と入力します。それから、同じダイアログの下の方 「 JavaScript サポート 」 を使用可能にします。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6B3MboII/AAAAAAAABsc/c6nCjDpRlHM/s1600/zend-debugger-012.png)



次に、ファイル index.php を新規で作成します。プロジェクト `test` を選択して、マウス右クリックします。ポップアップメニュー 「 新規 」 「 PHP ファイル 」 を選択します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6DSpmzZI/AAAAAAAABsg/FgzWTpum4xI/s1600/zend-debugger-013.png)



ファイル名に `index.php` を入力します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6EQQk1jI/AAAAAAAABsk/ce9cEmyLAHw/zend-debugger-014.png)



index.php のソースは次の通りです。



```
<?php
 $a = 1 + 1;
 $b = $a + 1;
?>
<html>
 <head>
 <meta http-equiv="Content-Type" content="text /html; charset=UTF-8" />
 <title>Test</title>
 </head>
 <body>
 <h1>Test</h1>
 <p>計算結果: <?php echo $b; ?></p>
 </body>
</html>
```


ブラウザで `http://localhost/test/index.php` が表示できることを確認してください。



デバッグ実行のためのブレークポイントを設定します。 Visual Basic などを使ったことがあれば、それとほとんど同じです。今回はソースの 2行目にブレークポイントを設定します。 2行目の行番号の左側をマウスでダブルクリックしてください。青い小さな丸印が付きます。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6FbvUjSI/AAAAAAAABso/qqINg4sw-No/zend-debugger-015.png)



ツールバーの虫の形のボタン 「 デバッグ 」 をクリックします。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6GY0XTEI/AAAAAAAABss/oij1ZP46w_k/zend-debugger-016.png)



「 PHP Web ページ 」 を選択します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6HhHMNCI/AAAAAAAABsw/AeXzeVHLiwY/zend-debugger-017.png)



URL はそのままで合っているはずです。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6IiuJ4VI/AAAAAAAABs0/Rdhre1OQ20w/s1600/zend-debugger-018.png)



「 パースペクティブ 」 というのは、その時の作業内容に応じた画面の構成のことです。 「 常にこの設定を使用する 」 のチェックを有効にしてください。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6J9z_XAI/AAAAAAAABs4/lg6oASopVsY/s1600/zend-debugger-019.png)



パースペクティブを手動で切り替えたい場合は、ウィンドウの右上のアイコンを使用してください 「 PHP デバッグ 」 と 「 PHP 」 が選択できます。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6RLWKdbI/AAAAAAAABtA/wrSFGKhmF38/zend-debugger-021.png)



PHP のデバッグ用のパースペクティブは次のような構成です。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6QDezcZI/AAAAAAAABs8/pgsHuuiCw4M/zend-debugger-020.png)



デバッグ実行直後、 2行目のブレークポイントで停止している状態です。左端の矢印が停止している行を示します。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6ST12IEI/AAAAAAAABtE/wZvZWv7tfcQ/zend-debugger-022.png)



ツールバーの2段目の 「 ステップオーバー 」 をクリックします。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6TZIk1rI/AAAAAAAABtI/oTZ_0hwB2CU/zend-debugger-023.png)



停止位置が 1行進んで 3行目になります。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6UQwUNeI/AAAAAAAABtM/gnRgV1dWwUk/zend-debugger-024.png)



中央上に変数の値の一覧があるのですが、変数 $a に、値 2 が入っていることがわかります。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6VgR9P2I/AAAAAAAABtQ/UrfoXuLnu7U/zend-debugger-025.png)



変数の値を無理やり変更することも可能です。



![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw6XQAEzSI/AAAAAAAABtU/P1OIB5XWZmY/zend-debugger-026.png)

## 詳しい使い方は書籍で

この記事には Zend Debugger の使い方のほんのさわりしか書いていません。詳しい使い方は次の書籍などを参考にしてください。

*   「 PHP 統合開発環境 PDT2 入門 」 岸本忠士 ISBN978-4-7980-2257-4
