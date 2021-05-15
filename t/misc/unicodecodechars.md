Unicode 内のそれぞれの文字種の範囲
=====

Update: 2009-11-23



[郵便番号データを利用するサンプル](http://code.google.com/p/zippyzipjp/) を作っている最中に気になって、ひらがな、カタカナなどの文字種の Unicode の文字コードの範囲を調べました。



資料として [http://www.unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/SHIFTJIS.TXT](http://www.unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/SHIFTJIS.TXT) を使います。 “OBSOLETE” となっていますが参考にはなります。これを表計算のシートに貼り付けて Unicode 順に並べ替えるとわかりやすいです。以下の説明には unicode.org の対応する “Code Charts” の URL も記しておきましたので、個別の字面とコード値の確認のためにご参照ください。



unicode.org の文書に頻出する “CJK” は “Chinese Japanese Korean” の略です。

## ASCIIコード

Code Charts: [C0 Controls and Basic Latin / Range: 0000–007F](http://www.unicode.org/charts/PDF/U0000.pdf)



基本的には `0x0020 - 0x007D` がASCIIコードに対応するのですが、 Shift\_JIS 等の日本の文字コードでこれ以外に関係するのは半角の円マークとバックスラッシュです。バックスラッシュは `0x005C` 半角の円マークは `0x00A5` （次項参照）になります。

## 全角記号

全角記号は Unicode の広い範囲に分散しています。 Shift\_JIS に対応づけられる文字はその中の一部です。



Code Charts: [C1 Controls and Latin-1 Supplement / Range: 0080–00FF](http://www.unicode.org/charts/PDF/U0080.pdf)

Code Charts: [Greek and Coptic / Range: 0370–03FF](http://www.unicode.org/charts/PDF/U0370.pdf)

Code Charts: [Cyrillic / Range: 0400–04FF](http://www.unicode.org/charts/PDF/U0400.pdf)

Code Charts: [General Punctuation / Range: 2000–206F](http://www.unicode.org/charts/PDF/U2000.pdf)

Code Charts: [Letterlike Symbols / Range: 2100–214F](http://www.unicode.org/charts/PDF/U2100.pdf)

Code Charts: [Arrows / Range: 2190–21FF](http://www.unicode.org/charts/PDF/U2190.pdf)

Code Charts: [Mathematical Operators / Range: 2200–22FF](http://www.unicode.org/charts/PDF/U2200.pdf)

Code Charts: [Miscellaneous Technical / Range: 2300–23FF](http://www.unicode.org/charts/PDF/U2300.pdf)

Code Charts: [Box Drawing / Range: 2500–257F](http://www.unicode.org/charts/PDF/U2500.pdf)

Code Charts: [Geometric Shapes / Range: 25A0–25FF](http://www.unicode.org/charts/PDF/U25A0.pdf)

Code Charts: [Miscellaneous Symbols / Range: 2600–26FF](http://www.unicode.org/charts/PDF/U2600.pdf)


```
0x00A2 - 0x00F7 Latin-1 に含まれる各種記号
0x0391 - 0x03C9 ギリシャ文字
0x0401 - 0x0451 キリル文字
0x2010 - 0x2312 矢印、科学技術記号など
0x2500 - 0x254B 罫線
0x25A0 - 0x266F 図形など
```


SHIFTJIS.TXT に収められている文字はこれだけなのですが、 Windows の機種依存文字としてラテン数字がありますね。次のものが対応するのかな？



Code Charts: [Number Forms / Range: 2150–218F](http://www.unicode.org/charts/PDF/U2150.pdf)



丸付き数字については調査見送り。

## 全角かな

Code Charts: [CJK Symbols and Punctuation / Range: 3000–303F](http://www.unicode.org/charts/PDF/U3000.pdf)

Code Charts: [Hiragana / Range: 3040–309F](http://www.unicode.org/charts/PDF/U3040.pdf)

Code Charts: [Katakana / Range: 30A0–30FF](http://www.unicode.org/charts/PDF/U30A0.pdf)



“Code Charts” を見ると「そんな文字使えるの？」というものもありますね。 SHIFTJIS.TXT に収められているものは次のようになります。


```
0x3000 - 0x301C 全角スペース、句読点など
0x3041 - 0x3093 ひらがな
0x309B          濁点
0x309C          半濁点
0x309D          「ゝ」
0x309E          「ゞ」
0x30A1 - 0x30F6 カタカナ
0x30FB          中黒点「・」
0x30FC           長音「ー」
0x30FD          「ヽ」
0x30FE          「ヾ」
```

## 漢字

Code Charts: [CJK Unified Ideographs / Range: 4E00–9FCF](http://www.unicode.org/charts/PDF/U4E00.pdf)



SHIFTJIS.TXT に収められている範囲は `0x4E00 - 0x9FA0` です。すべて上記のリストの範囲内です。 Windows で使える文字が最近拡張されているのが気になるのですが、今回はここまで。 JIS 第三、第四水準の漢字とオーバーラップすると思われる CJK Extension-A 〜 C もざっと見てみましたが、地名等にはあるかもしれないけど、とても日本人が日常使いこなせるとは思えない文字ばかりでした。

## 全角英数字、半角カナなど

英数字は ASCIIコードにあるもの、つまり、日本人が言うところの「半角」のものが基本で「全角」は特殊なもの、ひらがな・カタカナは「全角」が基本で「半角」が特殊なものという考え方なのだろうと思います。



Code Charts: [Halfwidth and Fullwidth Forms / Range: FF00–FFEF](http://www.unicode.org/charts/PDF/UFF00.pdf)



全角英数字と全角のカンマ、ピリオドなどの基本的な記号は `0xFF01 - 0xFF5D` になります。



全角記号「￣」が `0xFFE3` 全角円マークが `0x818F` と、上記の全角記号より少し離れた場所にあります。



Shift\_JIS の `0xA1 - 0xDF` の範囲にある半角カナなどは、 `0xFF61 - 0xFF9F` になります。
