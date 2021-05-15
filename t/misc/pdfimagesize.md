画像を埋め込んでもサイズが大きくならないPDF生成
=====

Update: 2013-02-16

PDFに画像埋め込んだら、どうも元のデータサイズに比べてできあがったPDFの方がかなり大きいような。。。ということはよくあります。PDFである限り避けられないようなことではなかろうと思ったので、久しぶりに Apache FOP で試してみました。７年ぶりくらいかな？まだ Apache FOP ってあるのかな？と少し心配だったのですが、ありました --> [http://xmlgraphics.apache.org/fop/](http://xmlgraphics.apache.org/fop/)



fop-1.1 をダウンロードして、解凍して、動作確認を "Quick Start Guide" にあるとおり



```
./fop -fo examples/fo/basic/readme.fo -awt
```



とすると、エラーです - -;)



まあ、Mac OS X だからと気を取り直して ( GUI関係はOS依存になってる可能性高いです )



```
./fop -fo examples/fo/basic/readme.fo -pdf readme.pdf
```



とすると、無事 PDF ができました。



A4いっぱいのサイズ ( 297mm x 210mm ) の画像を 4個用意してこんなソースを書いてマージンもなんにもなしの 4ページを生成してみます。画像ファイルは相対パスでおいとけば OK。



image-test.fo

```
fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"
 fo:layout-master-set
 fo:simple-page-master margin-right="0cm" margin-left="0cm" margin-bottom="0cm" margin-top="0cm" page-width="21cm" page-height="29.7cm" master-name="fp"
 fo:region-body/
 /fo:simple-page-master
 /fo:layout-master-set
 fo:page-sequence id="P1" master-reference="fp"
 fo:flow flow-name="xsl-region-body"
 fo:block
 fo:external-graphic width="21cm" height="29.7cm" content-width="21cm" content-height="29.7cm" src="sample1.jpg"/
 /fo:block
 /fo:flow
 /fo:page-sequence
 fo:page-sequence id="P2" master-reference="fp"
 fo:flow flow-name="xsl-region-body"
 fo:block
 fo:external-graphic width="21cm" height="29.7cm" content-width="21cm" content-height="29.7cm" src="sample2.jpg"/
 /fo:block
 /fo:flow
 /fo:page-sequence
 fo:page-sequence id="P3" master-reference="fp"
 fo:flow flow-name="xsl-region-body"
 fo:block
 fo:external-graphic width="21cm" height="29.7cm" content-width="21cm" content-height="29.7cm" src="sample3.jpg"/
 /fo:block
 /fo:flow
 /fo:page-sequence
 fo:page-sequence id="P4" master-reference="fp"
 fo:flow flow-name="xsl-region-body"
 fo:block
 fo:external-graphic width="21cm" height="29.7cm" content-width="21cm" content-height="29.7cm" src="sample4.jpg"/
 /fo:block
 /fo:flow
 /fo:page-sequence
/fo:root
```

このようなコマンドを実行すると



```
./fop -fo image-test.fo -pdf image-test.pdf
```



できましたよ。 Mac の Preview で見ると 1ドットくらい、 Adobe Reader だと 2ドットくらい上端が白いのがちょっと気になります。 [Google Docs のビュアー](https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxtaWNoaW5vYnVtYWVkYXxneDo0ZTUxN2JmNWVhNzJiMTg5) でも出るなあ。



画像サイズは 343,781 + 428,372 + 256,668 + 610,965 = 1,639,786 バイト、PDFのサイズは 1,634,738 バイトで小さくなっているような。。。なんで ^^)?
