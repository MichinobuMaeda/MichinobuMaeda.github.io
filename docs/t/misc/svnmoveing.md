# Subversion のお引っ越し

Update: 2009-08-21



かんたん、かんたん。



Subversion のリポジトリを家庭内サーバ ( OpenBlockS ) から外のサーバに移動しました。自分一人で使っているこのリポジトリを公開したいわけではないのですが（ディレクトリ構成が変だし）、たまに、外出先から見たくなることがあるからです。



引っ越し先のリポジトリの初期化が済んだところで、まず、元のリポジトリの内容をダンプ出力します



```
svnadmin dump /home/svn/repo/ |gzip - > svndump-20090820.gz
```



出力したファイルを引っ越し先のサーバに送り込んだら、ロードします。



```
gzip -d svndump-20090820.gz
svnadmin load /var/svn/repos < svndump-20090820
```



以上終わり。
