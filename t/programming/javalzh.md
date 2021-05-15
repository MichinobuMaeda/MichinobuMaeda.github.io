Java で LZH 形式のファイルを解凍する
=====

Update: 2010-10-02



郵便番号データを加工するプログラム http://www.zippyzip.jp/ ( 閉鎖 ) を Google App Engine に移植してみたいなと思い立ったのですが、最大の問題はデータが LHA で圧縮されて配布されていること。 Google App Engine で使うことができるプログラム言語はPython と Java なのですが、どちらも Zip 形式みたいに標準の API で OK なんてことは全くありません。



まず、機会があれば使ってみたかった Python の方。ぐぐってみたところ、みなさんネイティブなものを呼び出してどうにかされているようです。これはやりたくないんだな Google App Engine では。



Java の方は、２種類見つけました。

*   [Lha Library for Java](http://homepage1.nifty.com/dangan/Content/Program/Java/jLHA/LhaLibrary.html)
*   [JHLHA](http://www.vector.co.jp/soft/other/java/se192202.html)

どちらでもいいのですが、 java.util.zip に似たインターフェイスにしているという [Lha Library for Java](http://homepage1.nifty.com/dangan/Content/Program/Java/jLHA/LhaLibrary.html) の方を試してみることにします。



まず、ソースとドキュメントをダウンロード。私が使ったのはこのバージョン。

*   [jlhasrc\_20050504.tar.gz](https://sites.google.com/site/michinobumaeda/programming/javalzh/jlhasrc_20050504.tar.gz?attredirects=0)
*   [jlhadoc\_20050504.tar.gz](https://sites.google.com/site/michinobumaeda/programming/javalzh/jlhadoc_20050504.tar.gz?attredirects=0)

ソースの中には compile.xml というファイルが入っています。これは Ant 用だな。この設定は好みではないので、


```
    <property name="javac.compiler" value="modern"/>
    <property name="javac.target"   value="1.1"/>
    <property name="src.dir"        value="."/>
    <property name="dest.dir"       value="."/>
```


こんな感じに修正します。


````
    <property name="javac.compiler" value="modern"/>
    <property name="javac.target"   value="1.6"/>
    <property name="src.dir"        value="."/>
    <property name="dest.dir"       value="./dest">
````

で、ビルドすると、


```
$ mkdir dest
$ ant -f compile.xml -l compile.log compileRelease
```


「非推奨」の警告が出るけど、気にしない。それを JAR ファイルにします。


```
$ cd dest
$ jar cvf jlha.jar *
```


これで jlha.jar ができました。郵便番号データの場合、書庫の中のファイルは１個だけなので、その前提のテスト用のプログラムを書いてみます。エラー処理などは入っていません。


```
import java.io.FileInputStream;
import java.io.FileOutputStream;
import jp.gr.java_conf.dangan.util.lha.LhaInputStream;
import jp.gr.java_conf.dangan.util.lha.LhaHeader;
public class JlhaTest {

    public static void main(String[] args) {
        try {
            LhaInputStream is = new LhaInputStream(new FileInputStream(args[0]));
            LhaHeader header = is.getNextEntry();
            System.out.println("Entry : " + header.getPath());
            System.out.println("Size  : " + header.getOriginalSize());
            String outPath = args[0].replaceAll("lzh", "csv");
            System.out.println("Target: " + outPath);
            FileOutputStream os = new FileOutputStream(outPath);
            long sz = 0;
            int buff = is.read();

            while (0 <= buff) {
                os.write(buff);
                buff = is.read();
                ++ sz;
            }
            os.flush();

            os.close();
            is.close();
            System.out.println("Output: " + sz);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```



これをコンパイルして実行すると、


```
$ javac -cp jlha.jar JlhaTest.java
$ java -cp jlha.jar -cp . JlhaTest lzh/20050201000000_jigyosyo.lz
Entry : jigyosyo.cs
Size  : 292443
Target: csv/20050201000000_jigyosyo.cs
Output: 292443`
```


いいんじゃないかな。
