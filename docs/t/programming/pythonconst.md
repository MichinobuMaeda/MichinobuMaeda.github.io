# Python で定数のようなものを使う

Update: 2010-12-25

プログラム言語 Python には、定数がありません。でも、定数みたいなものが使いたいなと思って探していたらありました。

<http://code.activestate.com/recipes/65207/>

```python
class _const:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value
import sys
sys.modules[__name__]=_const()`
```


一度メンバーに値を設定すると、それ以降、値を変えることができないクラスです。こんな感じで使うのですが、

```python
import const
const.test = "Test1"
const.test = "Test2"
```

この例の場合、最後の行で例外が発生します。エラーの検知は実行時で、コンパイルの時点の違反の検出はできませんが、それでも十分使う価値があるものだと思います。

Tag: python
