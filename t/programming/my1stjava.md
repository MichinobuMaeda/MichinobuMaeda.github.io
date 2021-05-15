たぶんはじめての Java
=====

Update: unknown

たぶん私が初めて書いた Java プログラムです。並んでいるアプレットは同じものでパラメータだけ変えています。JDK1.0.6 だったと思います。もう、ソースは残っていません。 Java 2D が Sun からリリースされるのもこの後のことです。

[flowersong.jar](my1stjava/flowersong.jar)



[Deployment Toolkit Script](http://download.oracle.com/javase/6/docs/technotes/guides/jweb/deployment_advice.html) は次の通り。

```
<script src="http://www.java.com/js/deployJava.js"></script>
<script>
  var attributes = {codebase:'http://sites.google.com/site/michinobumaeda/programming/my1stjava/',
  code:'FlowerSong.class',
  archive:'flowersong.jar',
  width:240, height:240} ;
  var parameters = {``} ;
  var version = '1.0' ;
  deployJava.runApplet(attributes, parameters, version);
</script>

<script src="http://www.java.com/js/deployJava.js"></script>
<script>
  var attributes = {codebase:'http://sites.google.com/site/michinobumaeda/programming/my1stjava/',
  code:'FlowerSong.class',
  archive:'flowersong.jar',
  width:240, height:240} ;
  var parameters = {
    backGround:'#000000',
    dotColor:'#00FFFF',
    dotChangeColor:'#FF8888',
    tailCount:'5',
    initSpeed:'10',
    petalCount:'8',
    petalInterval:'5000',
    dotSize:'16',
    interval:'12'
  } ;
  var version = '1.0' ;
  deployJava.runApplet(attributes, parameters, version);
</script>
```
