+++
title = "pip-upgrader"
date = 2023-05-04T00:00:00+09:00
categories = ["tech"]
tags = ["python"]
+++

Python で `requirements.txt` に入っているパッケージを全部まとめて更新したいけど、
`pip` にはそれらしいコマンドがありません。
`pip install --upgrade` はパッケージ名の指定が必要です。何かいいものはないかなと探していたら
[pip-upgrader](https://github.com/simion/pip-upgrader)
というのがありました。

使い方は簡単で、

```bash
pip install pip-upgrader
```

で入れて、

```bash
pip-upgrade
```

とするだけです。プロンプト無しですべて自動で実行するには

```bash
pip-upgrade -p all
```

とします。
