Google Sites で JavaScript
=====

Update: 2011-01-26



※ この記事の内容は Mac の Safari など限られた環境でしか確認してません。



このサイトを [DokuWiki](http://www.dwug-jp.org/) から Google Sites に引っ越すにあたってまず困ったのが [本気でパスワード](https://sites.google.com/site/michinobumaeda/programming/honkipass) のページです。エディタの HTML 編集機能を使って <script ... とか書いても拒否されます。で、何か方法は？と探し始めてすぐに見つかった記事が [How To Add JavaScript or Custom Contents to Google Sites with Gadget](http://www.mydigitallife.info/2010/02/03/how-to-add-javascript-or-custom-contents-to-google-sites-with-gadget/) です。



埋め込みたいソースは [honkipass.html](https://sites.google.com/site/michinobumaeda/programming/honkipass/honkipass.html?attredirects=0) です。これを



`<?xml version="1.0" encoding="UTF-8"?>`

`<Module>`

`<ModulePrefs title="Custom Gadget" />`

`<Content type="html"><![CDATA[`

`...`

`]]></Content>`

`</Module>`



の CDATA セクションの中にそのまま丸ごと入れて、拡張子 .xml で保存します。そのファイルをサイトのどこでもいいのでアタッチします。最後に、エディタのメニュー Insert - More gadgets... でアタッチした URL を指定して、縦横のサイズやタイトルなどの設定を調整するとできあがりです。



2011-01-27 追記



[Google Sites で Java Applet](https://sites.google.com/site/michinobumaeda/cms/googlesitesjavaapplet) で紹介した Code Wrapper もよさそうです。



* * *

<!-- google\_ad\_client="pub-7953317888125639"; google\_ad\_host="pub-6693688277674466"; google\_ad\_width=468; google\_ad\_height=60; google\_ad\_format="468x60\_as"; google\_ad\_type="text\_image"; google\_color\_border="FFFFFF"; google\_color\_bg="FFFFFF"; google\_color\_link="000000"; google\_color\_url="0033CC"; google\_color\_text="444444"; //-->
