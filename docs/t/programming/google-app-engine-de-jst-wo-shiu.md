# Google App Engine で JST を使う ( python )

Update: unknown

Google App Engine の python の DateTimeProperty は、タイムゾーン情報を持ちません。 datetime.datetime.now() を代入すると、 UTC の日時になります。これを日本標準時 JST に直すこと自体は簡単で、こちら http://teraapi.blogspot.jp/2008/05/google-app-enginejst.html で紹介されているとおり。 [DateConvModule.py](http://dateconv4gae.googlecode.com/svn/trunk/DateConvModule.py) でほとんどの場合十分だと思います。

では、 DateTimeProperty にタイムゾーン有りの値を代入したらどうなるか？ 試してみました。

下のサンプルコードは [Local Unit Testing for Python](http://developers.google.com/appengine/docs/python/tools/localunittesting) の最後に載っている testrunner を使った Python unittest2 の [テストコード](https://github.com/MichinobuMaeda/moleutils/blob/master/test/testtz.py) の一部です。


```
    utc = UtcTzinfo()
    jst = JstTzinfo()

    m1 = TestModel(key_name='m1', dt=datetime(2001, 2, 3, 4, 5, 6))
    self.assertEquals(m1.dt, datetime(2001, 2, 3, 4, 5, 6))

    m1.dt = datetime(2001, 2, 3, 4, 5, 6, tzinfo=utc)
    m1.put()
    with self.assertRaises(TypeError):
    dmy = (m1.dt == datetime(2001, 2, 3, 4, 5, 6))

    m2 = TestModel.get_by_key_name(key_names='m1')
    self.assertEquals(m2.dt, datetime(2001, 2, 3, 4, 5, 6))

    m1.dt = datetime(2001, 2, 3, 13, 5, 6, tzinfo=jst)
    m1.put()
    with self.assertRaises(TypeError):
    dmy = (m1.dt == datetime(2001, 2, 3, 4, 5, 6))

    m3 = TestModel.get_by_key_name(key_names='m1')
    self.assertEquals(m3.dt, datetime(2001, 2, 3, 4, 5, 6))
```


タイムゾーン情報 UTC 付きの値を代入した変数をそのまま参照すると、タイムゾーン情報付きの値のままです。 native な値にはなっていません。 native な値 `datetime(2001, 2, 3, 4, 5, 6)` と比較しようとすると `TypeError` になります。

保存した値を読み込んで参照すると、タイムゾーン無しの native な値になっています。

タイムゾーン情報 JST 付きの値を代入した変数をそのまま参照したばあいも、タイムゾーン情報付きのままです。

保存した値を読み込んで参照すると、タイムゾーン無しの native な値になっています。ただし、単純にタイムゾーンを無視するのではなくて、 9時間前の値になっています。代入した値に付いているタイムゾーン情報は認識しています。

親切な仕様だと思いますが、よく知らずに使うとはまるだろうなぁ。
