Google Sites で Java Applet
=====

Update: 2011-01-27



IE など NG です!! ( 2011-02-05 追記 )



本題の前に、 JavaScript と Java Applet はどう違うの？というような話は [http://detail.chiebukuro.yahoo.co.jp/qa/question\_detail/q136095388](http://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q136095388) などをどうぞ。



さて、 [Google Sites で JavaScript](https://sites.google.com/site/michinobumaeda/cms/googlesitesjs) や [Google Sites で Flash](https://sites.google.com/site/michinobumaeda/cms/googlesitesflash) と同じように、 DokuWiki から Google Sites に引っ越すにあたって少し苦労したお話の３個目です。 Google Sites の HTML エディタで <applet ... とか書いてもだめなので、世の中に私と同じ悩みを持っていた人はいないかと探してみました。最初に見つかったのはこの記事 J[ava applets in Google sites](http://www.google.com/support/forum/p/sites/thread?tid=4ca6167e3376dcc1) なのですが、 "Google Web Toolkit に移植してしまえ" というぶっとんだ回答なのでパス。



次に見つけたのは [Embed Java Applets in Google Sites](http://web.michaelchughes.com/how-to/embed-java-applets-in-google-sites) です。 [Code Wrapper gadget](https://sites.google.com/site/mori79/system/errors/NodeNotFound?suri=wuid://defaultdomain/mori79/gx:2f6d760e68f4b8) に [Java™ Rich Internet Applications Deployment Advice](http://java.sun.com/javase/6/docs/technotes/guides/jweb/deployment_advice.html) で紹介されている Deployment Toolkit Script を入れて使いなさいとのことです。



無事に引っ越しできたページは [たぶんはじめての Java](https://sites.google.com/site/michinobumaeda/programming/my1stjava) です。



まず、エディタのメニュー "Insert" - "More gadgets..." で "Code Wrapper" を検索します。 [Code Wrapper gadget](https://sites.google.com/site/mori79/system/errors/NodeNotFound?suri=wuid://defaultdomain/mori79/gx:2f6d760e68f4b8) が間違いなく出てくるので、それをページに埋め込みます。設定するコードは、 [Java™ Rich Internet Applications Deployment Advice](http://java.sun.com/javase/6/docs/technotes/guides/jweb/deployment_advice.html) のサンプルそのままならこんな感じ。

`<script src="http://www.java.com/js/deployJava.js"></script>
<script>
    var attributes = {codebase:'http://java.sun.com/products/plugin/1.5.0/demos/jfc/Java2D',
                      code:'java2d.Java2DemoApplet.class',
                      archive:'Java2Demo.jar',
                      width:710, height:540} ;
    var parameters = {fontSize:16} ;
    var version = '1.6' ;
    deployJava.runApplet(attributes, parameters, version);
</script>`

すると、派手な Java2D のデモが表示できます。
