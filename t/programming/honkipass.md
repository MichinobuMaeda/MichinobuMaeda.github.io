本気でパスワード
=====

Update: 2006-04-30

追記: 2021-05-23 最新版はこちら https://pages.michinobu.jp/t/20210522honkipass.html

ランダムにパスワードを生成するツールです。 JavaScript のお勉強を兼ねて作成しました。

Windows の場合ダウンロードして、適当なフォルダに拡張子 .hta で保存してください。

それ以外の OS の場合は、拡張子 .html で保存してください。

- [honkipass.html](honkipass/honkipass.html)


ソース


```
<!--
/*
 * $Id: honkipass.hta 131 2006-04-30 15:23:12Z michinobu $
 *
 * Copyright 2006 Michinobu Maeda.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
-->
<html>
  <head>
    <meta http-equiv="Content-type" content="text/html; charset=UTF-8"/>
    <style type="text/css">
    body {
        margin: 0px;
        padding: 12px;
        background: #F0F0E0;
    }
    h1 {
        text-align: center;
        font-size: 150%;
        font-family: sans-serif;
        font-weight: 400;
        line-height: 150%;
        margin: 12px 0px;
        border-top: solid 2px black0;
        border-bottom: solid 2px black;
    }
    p, div, input {
        font-size: 100%;
        font-family: sans-serif;
        line-height: 120%;
        margin: 2px 0px;
        padding: 2px 0px;
    }
    div {
        margin: 0px;
        padding: 0px;
    }
    form {
        margin: 0px;
    }
    #ver {
        font-size: 67%;
        font-family: sans-serif;
    }
    #rst, #btn {
        margin-left: 24pt;
    }
    #btn {
        padding-left: 8pt;
        padding-right: 8pt;
    }
    #len, #chr, #pwd {
        padding: 1px 8px;
        font-family: monospace;
        line-height: 100%;
    }
    #chr, #pwd {
        width: 50%;
    }
    #len {
        text-align: right;
    }
    #cr {
        text-align: center;
        border-top: solid 2px black;
    }
    </style>
    <script language="JavaScript">

    var limit = 1000;   // 計算回数の限界
    var type = "";      // 一般／数値4桁
    var gen = null;     // ラジオボタン「一般」
    var n4c = null;     // ラジオボタン「数値4桁」
    var rst = null;     // ボタン「リセット」
    var prm = null;     // 一般パラメータ領域
    var num = null;     // チェックボックス「数字」
    var lwc = null;     // チェックボックス「小文字」
    var upc = null;     // チェックボックス「大文字」
    var sin = null;     // チェックボックス「記号」
    var chr = null;     // テキストボックス「記号として使用する文字」
    var mix = null;     // チェックボックス「すべての文字種を使用」
    var ndc = null;     // チェックボックス「同一文字使用禁止」
    var len = null;     // テキストボックス「文字数」
    var btn = null;     // ボタン「作詞」
    var pwd = null;     // テキストボックス「パスワード」

    /* ウィンドウサイズを設定する. */
    if (location.protocol.toString().match(/file/)) {
        window.resizeTo(620, 460);
        window.moveTo(
            (screen.availWidth - 620) / 2,
            (screen.availHeight - 480) / 2);
    }

    /* ウィンドウ初期化時のイベントハンドラを登録する. */
    regEvent(window, "load", false, function () {
        gen = document.getElementById("gen");
        n4c = document.getElementById("n4c");
        rst = document.getElementById("rst");
        prm = document.getElementById("prm");
        num = document.getElementById("num");
        lwc = document.getElementById("lwc");
        upc = document.getElementById("upc");
        sin = document.getElementById("sin");
        chr = document.getElementById("chr");
        mix = document.getElementById("mix");
        ndc = document.getElementById("ndc");
        len = document.getElementById("len");
        btn = document.getElementById("btn");
        pwd = document.getElementById("pwd");

        setDefault ();

        regEvent(gen, "click", false, function () {
            onTypeSelected("gen");
        });

        regEvent(n4c, "click", false, function () {
            onTypeSelected("n4c");
        });

        regEvent(rst, "click", false, setDefault);

        regEvent(btn, "click", true, function () {
            btn.disabled = true;
            createPassword();
            btn.disabled = false;
        });
    });

    /**
     * 要素にイベントを登録する.
     * @param element 要素
     * @param name イベント名
     * @param flg イベント伝播の方向
     * @param handle ハンドラ
     */
    function regEvent(element, name, flg, handle) {
        if (element.addEventListener) {
            element.addEventListener(name, handle, flg);
        } else if (element.attachEvent) {
            element.attachEvent("on" + name, handle);
        }
    }

    /**
     * 一般／数値4桁選択変更時の処理.
     * @param sel 選択内容
     */
    function onTypeSelected(sel) {
        if (sel == type) { return; }
        pwd.value = "";
        type = sel;
        if (type == "gen") {
            gen.checked = true;
            n4c.checked = false;
            prm.style.display = "block";
        } else {
            gen.checked = false;
            n4c.checked = true;
            prm.style.display = "none";
        }
    }

    /** デフォルト値を設定する. */
    function setDefault() {
        onTypeSelected ("gen");
        num.checked = true;
        lwc.checked = true;
        upc.checked = true;
        mix.checked = true;
        ndc.checked = true;
        sin.checked = false;
        chr.value = "@#$%^&*-_=+";
        len.value = "8";
        pwd.value = "";
    }

    /** パスワードを作成する. */
    function createPassword() {
        var vals = (n4c.checked ? "0123456789"
            : (num.checked ? "0123456789" : "")
            + (lwc.checked ? "abcdefghijklmnopqrstuvwxyz" : "")
            + (upc.checked ? "ABCDEFGHIJKLMNOPQRSTUVWXYZ" : "")
            + (sin.checked ? chr.value : ""));
        var cnt = n4c.checked ? 4 : new Number(len.value);
        var tcnt = (num.checked ? 1 : 0)
            + (lwc.checked ? 1 : 0)
            + (upc.checked ? 1 : 0)
            + (sin.checked ? 1 : 0);
        var isNum = true;           // 数字を使用する
        var isLwc = true;           // 小文字を使用する
        var isUpc = true;           // 大文字を使用する
        var isSin = true;           // 記号を使用する
        var n = 0;                  // 計算回数
        var ret = "";               // 計算結果

        if (isNaN(cnt)) {
            alert("文字数には半角で数値を設定してください。");
            return;
        }

        if (cnt < 1) {
            alert("文字数には正の数値を設定してください。");
            return;
        }

        if(mix.checked && (cnt < tcnt)) {
            alert("すべての文字数を使用するには " + tcnt + " 文字以上必要です。");
            return;
        }

        if (tcnt < 1) {
            alert("1個以上の文字種を選択してください。");
            return;
        }

        if (sin.checked) {
            if (chr.value.length == 0) {
                alert("使用する記号を指定してください。");
                return;
            }

            for (i = 0; i < chr.value.length; ++i) {
                var c = chr.value.charAt(i);
                if (c == " ") {
                    alert("記号にスペースは指定できません。");
                    return;
                }
            }
        }

        for (; n < limit; ++n) {

            ret = "";

            if(mix.checked) {
                isNum = !num.checked;
                isLwc = !lwc.checked;
                isUpc = !upc.checked;
                isSin = !sin.checked;
            }

            for (i = 0; i < cnt; ++i) {

                var c = vals.charAt(Math.floor(Math.random() * vals.length));

                if (ndc.checked) {
                    if (ret.indexOf(c) >= 0) { break; }
                }

                if (c.match(/[0-9]/)) {
                    isNum = true;
                } else if (c.match(/[a-z]/)) {
                    isLwc = true;
                } else if (c.match(/[A-Z]/)) {
                    isUpc = true;
                } else {
                    isSin = true;
                }

                ret = ret + c;
            }

            if (ret.length == cnt) {
                if (n4c.checked) { break; }
                if (isNum && isLwc && isUpc && isSin) { break; }
            }
        }

        if (n >= limit) {
            alert("計算回数が " + limit + " を超えました。条件を満たすパスワードを作成するのは困難です。");
            return;
        }
        pwd.value = ret;
        return false;
    }
    </script>
    <title>本気でパスワード Ver. 1.0</title>
  </head>
  <body>
    <h1>本気でパスワード <span id="ver">Ver. 1.0</span></h1>
    <form action="javascript:return false;">
      <p>
        <input type="text" id="pwd" readonly/>
        <button id="btn">パスワード作成</button>
      </p>
      <p>
        <input type="radio" id="gen" name="type"/> 一般用
        <input type="radio" id="n4c" name="type"/> 数字4桁
        <button id="rst">設定をすべて初期値に戻す</button>
      </p>
      <div id="prm">
        <p>
          <input type="checkbox" id="num"/> 数字を使う。
        </p>
        <p>
          <input type="checkbox" id="lwc"/> アルファベット小文字を使う。
        </p>
        <p>
          <input type="checkbox" id="upc"/> アルファベット大文字を使う。
        </p>
        <p>
          <input type="checkbox" id="sin"/> 右の欄の記号を使用する。
          <input type="text" id="chr"/>
        </p>
        <p>
          <input type="checkbox" id="mix"/> それぞれの文字種を1文字以上使う。
        </p>
        <p>文字数
          <input type="text" id="len" size="3"/>
          ← 半角数字で 1以上の値を記入してください。
        </p>
        <p>パスワードは 6文字以上で3種類以上の文字種を使用することをおすすめします。</p>
      </div>
      <p>
        <input type="checkbox" id="ndc"/> 同じ文字を2回以上使用しない。
      </p>
    </form>
    <p id="cr">Copyright 2006 Michinobu Maeda.</p>
  </body>
</html>
```
