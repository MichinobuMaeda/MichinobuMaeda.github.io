Checkstyle をチェックする
=====

Update: 2006-01-06



あまり真剣に読まないように。



> 関連記事 : [自分用 Checkstyle 5.0 暫定対応](checkstyle5forme.html)



自分でスタイルを決めてJava のコーディングをする場合は、できるだけ Sun ( 現在は Oracle : 2011-01-24 追記 ) [“Java Code Conventions”](http://www.oracle.com/technetwork/java/codeconv-138413.html) に従っているつもりでした。そのために Eclipse の機能や Checkstyle などのツールを使っているわけですが、ときどき「本当にこれは Sun “Java Code Conventions” のルールなの？」と疑問に思うことがあり、 久しぶりに原典を読み直してツールの機能を確認してみようと思ったわけです。



このページはきわめて趣味的なものなので、まじめに最後まで読もうとか思わないでください。特に C言語のコメントがどうのとか、”Double-Checked Locking” とかは 99.9% の Java エンジニアには無関係な話です。



カスタマイズした結果は次の通りです。

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE module PUBLIC
	"-//Puppy Crawl//DTD Check Configuration 1.2//EN"
	"http://www.puppycrawl.com/dtds/configuration_1_2.dtd">
<!--
  $Id: reduced_sun_checks.xml 36 2005-12-20 05:38:38Z michinobu $

  Checkstyle 4.1 の配布物に含まれる設定ファイル sun_checks.xml
  をカスタマイズしたものです。カスタマイズの内容の詳細は
  http://www.mmichi,com/checkstyle/ をご参照ください。

  Checkstyle については http://checkstyle.sf.net/ を
  ご参照ください。

  Checkstyle は GNU LESSER GENERAL PUBLIC LICENSE ( LGPL ) Version 2.1
  により配布されています。 sun_checks.xml については個別に
  ライセンスについて記述されていませんが、LGPL が適用されると
  思われます。このファイルについてもそのライセンスを引き継ぎます。
  LGPL についての詳細は http://www.gnu.org/copyleft/lesser.html を
  ご参照ください。
 -->
<module name="Checker">
  <module name="PackageHtml"/>
  <module name="Translation"/>
  <module name="TreeWalker">
    <module name="JavadocMethod"/>
    <module name="JavadocType"/>
    <module name="JavadocVariable"/>
    <module name="JavadocStyle">
      <property name="checkFirstSentence" value="false"/>
    </module>
    <module name="ConstantName"/>
    <module name="LocalFinalVariableName"/>
    <module name="LocalVariableName"/>
    <module name="MemberName"/>
    <module name="MethodName"/>
    <module name="PackageName"/>
    <module name="ParameterName"/>
    <module name="StaticVariableName"/>
    <module name="TypeName"/>
    <module name="AvoidStarImport">
      <property name="excludes" value="java.io,java.util"/>
    </module>
    <module name="IllegalImport"/>
    <module name="RedundantImport"/>
    <module name="UnusedImports"/>
    <module name="FileLength"/>
    <module name="LineLength"/>
    <module name="MethodLength"/>
    <module name="ParameterNumber"/>
    <module name="EmptyForIteratorPad"/>
    <module name="MethodParamPad"/>
    <module name="NoWhitespaceAfter"/>
    <module name="NoWhitespaceBefore"/>
    <module name="OperatorWrap"/>
    <module name="ParenPad"/>
    <module name="TypecastParenPad"/>
    <module name="TabCharacter"/>
    <module name="WhitespaceAfter"/>
    <module name="WhitespaceAround">
      <property name="allowEmptyMethods" value="true"/>
    </module>
    <module name="ModifierOrder"/>
    <module name="RedundantModifier"/>
    <module name="AvoidNestedBlocks"/>
    <module name="EmptyBlock"/>
    <module name="LeftCurly"/>
    <module name="NeedBraces"/>
    <module name="RightCurly"/>
    <module name="DoubleCheckedLocking"/>
    <module name="EmptyStatement"/>
    <module name="EqualsHashCode"/>
    <module name="HiddenField">
      <property name="ignoreSetter" value="true"/>
    </module>
    <module name="IllegalInstantiation"/>
    <module name="InnerAssignment"/>
    <module name="MagicNumber">
      <property name="ignoreNumbers" value="-1, 0, 1"/>
    </module>
    <module name="MissingSwitchDefault"/>
    <module name="RedundantThrows"/>
    <module name="SimplifyBooleanExpression"/>
    <module name="SimplifyBooleanReturn"/>
    <module name="FinalClass"/>
    <module name="HideUtilityClassConstructor"/>
    <module name="InterfaceIsType"/>
    <module name="VisibilityModifier"/>
    <module name="ArrayTypeStyle"/>
    <module name="FinalParameters"/>
    <module name="TodoComment">
      <property name="format" value="(TODO|XXX|FIXME)"/>
    </module>
    <module name="UpperEll"/>
  </module>
</module>
```

Eclipse プラグインに設定ファイルとして読み込んだり、 Maven の checkstyle:checkstyle ゴールの propertiesFile パラメタに設定できたりします、が、現状の Maven 2 用のプラグインは国際化対応とクラスローダの 問題があってうまく動きません。リソースバンドルの不足については jira に登録したら早速 「SVN のソースでは直っているよ」とコメントがつきました。でも、サイトに掲示されている SVN の URL が間違っているという別の報告済みの問題があって、これはまだ直っていないです。 クラスローダの件もすでに他の人が登録していたのでそのうち直るでしょう。



以下の文章で ”\[ 変更 \]” ”\[ 不可 \]” としている事項が、私が Checkstlye をカスタマイズした箇所です。

## Sun "Java Code Conventions" の復習

なぜ Sun “Java Code Conventions” なのかというと、世の中に広く受け入れられているからです。 それは、規定の内容そのものの優劣より重要なことだと思います。



配布元 URL は http://java.sun.com/docs/codeconv/index.html です ( 現在は [http://www.oracle.com/technetwork/java/codeconv-138413.html](http://www.oracle.com/technetwork/java/codeconv-138413.html) : 2011-01-24 追記 ) 。1997 年に作成されてそれ以降改訂されていないようで、バージョン番号などは記されていません。

### ファイル名、クラス名など

議論の対象になることはほとんどなさそうなので略します。 クラス名に数字のコード値を割り当てるような仕事なら私はさっさと逃げます。 そのような会社があると噂には聞いていたのですが、この目で見たときには絶句しました。



ときどきインターフェイスの名称の先頭に “I” をつけているものを見ますが、いい方法ではないと思います。 そのインターフェイスを使う側にはそれがインターフェイスなのかどうかを意識させない方がオブジェクト指向のプログラムとして自然な姿だと思うからです。 Java より先に「インターフェイス」という言葉を世の中に広めた Microsoft の COM を例に挙げると、 VB の部品や Office の公開インターフェイスにすべていちいち “I” がついていたりはしません。

### ファイルの先頭のコメント

```
/*
 * Classname
 *
 * Version info
 *
 * Copyright notice
 */
```


… だそうです。 “11 - Code Examples” の場合、 “Classname” と “Version info” に相当すると思われる行は次のようになっています。


```
/*
 * %W% %E% Firstname Lastname
 *
````



CVS や Subversion であれば $Id$ など入れておけばよさそうです。 Eclipse 3.1 の場合このブロックコメントを折りたたんでもこの 1行だけは表示されるのでいい感じです。

### import

”.\*” を使ったものが例示されています。 ”.\*” を原則使わないという流儀もあって私も従っているのですが、 Eclipse などインテリジェントな環境で作業するのでなければ、java.\* の下のパッケージは ”.\*” を使ってインポートしてもいいと思います。 依存関係のチェックの対象とする必要はないからです。

### メンバの記述の順番

メンバの記述の順番は次のようになります。

1.  クラス ( static ) 変数
2.  インスタンス変数
3.  コンストラクタ
4.  メソッド

### インデントとタブ

少しわかりにくい書き方になっているのですが、私が読み取った内容は次のようになります。



Sun “Java Code Conventions” が決めていることは次の通りです。

*   インデントは4桁である。
*   タブは8桁である。

Sun “Java Code Conventions” が決めていないことは次の通りです。

*   インデントを記述するのにスペースだけを使うかタブも使うか。

Eclipse などいくつかのツールのデフォルトの動作ではタブを4桁として表示してしまいますので、 スペースだけを使うのが無難だと思います。

### 1行の長さ

80桁を超える行は避けるように、とのことです。



多くのツールやターミナルによってうまく処理できるように、という趣旨なので、日本語の場合は 80文字ではなくいわゆる半角で 80桁以内にということになりますし、 改行の表示のことを考えるとたぶん 79桁以内の方がいいのだろうと思います。

### 処理行の途中の改行

次のような原則が示されれています。

*   カンマの後で改行する。
*   演算子の前で改行する。
*   できるだけ高いレベルで ( 演算の優先順位を指していると思われる ) 改行する。
*   同じレベルの改行は先頭をそろえる。
*   インデントする場合は 8桁。

いくつかの例が挙げられていますが、厳密に次の例の通りに書かれたソースはいまだかつて見たことがありません。


```
    if ((condition1 && condition2)
            || (condition3 && condition4)
            ||!(condition5 && condition6)) {
        doSomethingAboutIt();
    }
```


”!” の前後にスペースは入れないのですね。 “10.5.1 Parentheses” の考え方に従うなら !(…) は (!(…)) とする方がいいように思います。

### コメント

省略しますが次の点だけ。



“\*” などで箱を描かないように、とのことです。 C言語でよく使いますね。私も使っていましたが、 100桁を超えるような幅の箱は環境によっては困ったことになります。

"//" で連続する複数行をコメントアウトするのはいいが、 連続する複数行の文章の記述には使わないように、とのことです。

はっきりと記述されているわけではないのですが、次のように解釈していいようです。



*   `/*…*/` をコメントアウトに使わない。
*   `/*…*/` は次のフォーマットで。


```
    /*
     * 1行目
     * 2行目
     * 3行目
     */
```



少し話がそれますが、次のような形のコメントアウトの記述ミスで痛い目に遭った C言語プログラマはたくさんいらっしゃるでしょう。



```
/*
    ここから
     ...
    ここまでコメントアウト
*/
```



で、「C言語でも "//" 使えばいい」という人もいるのですが、 それ、きっと、たぶん ANSI C じゃないです。少し格好悪いですが、次のように書くことが可能です。 コメントアウトの途中に /\*…\*/ が入っていてもだいたいうまくいきます。


```
/*
*//*    ここから
*//*    ...
*//*    ここまでコメントアウト
*/`
````


変数の宣言



次のようなことが書かれています。

*   1行に 1個の変数を宣言する。で、次のようにコメントをつけるのが望ましい。

```
    int level; // indentation level
    int size; // size of table
```

*   型と変数の間のスペースは次のどちらかにする。
*   スペース1個。
*   タブを使って変数の先頭をそろえる。
*   ブロック ( {…} で囲まれたブロック ) の先頭で宣言する。 for 文のインデックスだけは例外。
*   ローカル変数はできるだけ宣言した場所で初期化する。

私の場合 C++ を書き始めたときにブロックの途中でローカル変数が宣言時に初期化できるのがうれしくて Java になってからも多用していたのですが、そもそもメソッドのサイズを小さくするなどして避けるようにします。

### クラスとインターフェイスの宣言

例の通りなので省略。



{...}



“7.2 Compound Statements” に、きっとたぶん日本語に訳してもなお晦渋 ( 怪獣 ) であろうと思われる書き方で定義していますが、 その後の各節の例を見れば誤解なく理解できるだろうと思います。



重要な事項としては次のようなことがあります。

*   if, if-else 文は必ず {…} を使う。
*   switch 文で break; を省略する場合は /\* falls through \*/ といったコメントを break; が ( 省略せずに入れるとすれば ) 入ることになる場所に記述する。
*   switch 文には default: を記述する。
*   switch 文の default: にも break; を記述する。

switch 文の体裁は C/C++ でも様々な流儀があったので例を引用しておきます。


```
    switch (condition) {
    case ABC:
        statements;
        /* falls through */
    case DEF:
        statements;
        break;
    case XYZ:
        statements;
        break;
    default:
        statements;
        break;
    }
```


「使わないはずの default: には assert を入れておけばよい」と言う人もいます。そういえば私は Java の assert は活用できていないなぁ。



C/C++ でも少数派だとは思いますが、「if 文の else を必ず」といった記述はありませんでした。

### 空行

細かくいろいろ決まっています。

*   2行入れるべき箇所
*   ソースファイルの “sections” の間
*   クラスもしくはインターフェイスの宣言の間
*   1行入れるべき箇所
*   メソッドの間
*   メソッドの中のローカル変数と最初のステートメントの間
*   コメントの前
*   その他メソッドの中のロジカルな “sections” の間で可読性を向上できる場合

間に 2行入れるべき “sections” というのは “11.1 Java Source File Example” を見てもよくわかりません。 import とクラスの宣言の間は対象になりそうです。

### スペース

スペースを入れるべき箇所も細かく記述されています。

*   キーワードと ”(” の間に入れる。メソッド名と ”(” の間に入れない。
*   引数のリストのカンマの後
*   ”.” 以外の二項演算子とそのオペランドの間。 ”++” ”–” とそのオペランドの間には入れない。
*   “for” 文の条件説の間
*   キャストの後

### 命名規則

省略。

### プログラムの記述

*   インスタンス変数は public にしない。ただし、振る舞いを全く含まないデータ構造を表すクラスはその限りではない。
*   クラス変数とクラスメソッドを参照する場合は、オブジェクト名ではなくクラス名を使う。
*   \-1 と 0, 1 以外の数値を直書きしない。
*   1行で複数の変数に値を代入したり、評価と代入をいっぺんにやったり、とにかく難しいことをしない。

### その他

*   演算子の優先順位で混乱しないよう丸括弧は明示的につけたほうがいい。
*   プログラムの構造を明確にするために、 if…else の途中などでの return は避ける。
*   3項演算子 ?: の ”?” の前で演算する場合は丸括弧を付与する。
*   特別なコメント
*   XXX 「正しくないがとりあえず動いてはいる。
*   FIXME 「正しくない、動いていない、修正が必要。」

Eclipse 3.1 の場合 “Task Tags” として XXX, FIXME, TODO が登録されています。

## Checkstyle 4.1 の sun\_checks.xml の検討

Checkstyle 4.1 に添付されている sun\_checks.xml を詳しく見てみることにします。これまで使ってみた感じでは、 Sun “Java Code Conventions” そのものの内容の他に “some best practices” として追加された事項がたくさんあり、中にはあまり品質には影響しそうにないもの、 環境によっては作業効率を落とす可能性の高いもの、そもそも不合理なものが含まれているように思います。



以下、各モジュールについての意見です。



\[ 可 \] : Sun “Java Code Conventions” のとおり。

\[ 追加 \] : “Java Code Conventions” には含まれないが、使いたい事項。

\[ 変更 \] : プロパティの追加など変更を加えて使いたい事項。

\[ 不可 \] : 使いたくない事項。

### Module: PackageHtml

\[ 追加 \]



package.html の有無をチェックします。

### Module: NewlineAtEndOfFile

\[ 不可 \]



ファイルの末尾が改行文字かどうかをチェックします。



改行文字の種類もチェックしているため、たとえば Windows 上で LF のみとした場合にエラーとなってしまいます。 NetBeans で作業しているときにこの問題が発生しました。 あまり重要な事項ではないし、環境が変わるたびに設定を変更するのは面倒なので不可とします。

### Module: Translation

\[ 追加 \]



国際化対応のためのプロパティファイルが同じキーを重複なく一つだけ含むかどうかをチェックします。

### Module: JavadocMethod

\[ 可 \]



コンストラクタおよびメソッドの JavaDoc コメントをチェックします。



scope のデフォルトは private ですが、 クラスの外からどのような形でも参照されないわけで、 package くらいでもいいと思ったのですが、とりあえずこのままで。



継承したメソッドについては Eclipse が自動で付与してくれる



 `/* (non-Javadoc)`

 `* @see com.mmichi.o2X.analysis.Analyser#getDocument()`

 `*/`



を認識してくれなくて不満だったのですが、ドキュメントをよく読むと



 `/** {@inheritDoc} */`



を使えと書いています。 Eclipse の設定を変えてしまうことにします。

### Module: JavadocType

\[ 可 \]



クラスまたはインターフェイスの JavaDoc コメントをチェックします。



scope については JavadocMethod と同様です。

### Module: JavadocVariable

\[ 可 \]



変数の JavaDoc コメントをチェックします。



scope については JavadocMethod と同様です。

### Module: JavadocStyle

\[ 変更 \]



JavaDoc の体裁をチェックします。



先頭行がピリオド等で終わることのチェックは、国際化対応していなくて日本語の「。」は認識しません。 またプロパティなどで追加することもできないようです。 少し惜しい気がしますが checkFirstSentence プロパティは false で使うことにします。

### Module: ConstantName

\[ 可 \]



static final の定数の名称をチェックします。

### Module: LocalFinalVariableName, LocalVariableName, MemberName, MethodName, PackageName, ParameterName, StaticVariableName, TypeName

\[ 可 \]



命名規則のチェックです。



Checkstyle のモジュールのうち AbstractClassName は含みません。

### Module: AvoidStarImport

\[ 変更 \]



.\* によるインポートをチェックします。



デフォルトではすべて禁止ですが、プロパティ excludes に次のものを追加して使うことにします。



1.  `java.io`
2.  `java.util`

### Module: IllegalImport

\[ 追加 \]



デフォルトで `sun.*` のインポートをチェックします。理由は 100% Pure Java でないからだそうです。

### Module: RedundantImport

\[ 追加 \]



冗長なインポートの記述をチェックします。

### Module: UnusedImports

\[ 追加 \]



使用されないインポートをチェックします。

### Module: FileLength

\[ 可 \]



ファイルの行数をチェックします。デフォルトで 2,000行です。

### Module: LineLength

\[ 可 \]



行の文字数をチェックします。デフォルトで 80文字です。タブは 8文字として計算します。

### Module: MethodLength

\[ 追加 \]



メソッドの行数をチェックします。デフォルトで 150行です。

### Module: ParameterNumber

\[ 追加 \]



コンストラクタとメソッドのパラメタの数をチェックします。デフォルトで 7個です。



なぜ 7個なのか不明ですが、まぁ妥当な数だと思うのでそのままとします。

### Module: EmptyForIteratorPad

\[ 追加 \]



要するに次のような場合の第3項目 ;) のスペースの有無をチェックします。 デフォルトでは「スペース無し」です。



`for (Iterator it = set.iterator(); it.hasNext();) {`



「スペース有り」の設定にもできます。どっちでもいいような気もするのですが、 “pad policy” に `method(a, b);` と `method( a, b );` という例が挙げられていて、それならやはり「スペース無し」かなと思うのでデフォルトに従います。

### Module: MethodParamPad

\[ 可 \]



メソッドの宣言 ( ドキュメントには “definition” と書いていますが “declaration” ではないかな？ ) のスペースの有無をチェックします。



デフォルトではプロパティ allowLineBreaks が false です。 Sun “Java Code Conventions” の “4.2 Wrapping Lines” を厳格に解釈するとそうなります。

### Module: NoWhitespaceAfter

\[ 追加 \]



プロパティ “tokens” に設定された文字列の後の空白が無いことをチェックします。 次のものが設定されています。

*   ARRAY\_INIT : 配列を初期化する {
*   BNOT : ~
*   DEC : オペランドの前に付く –
*   DOT : .
*   INC : オペランドの前に付く ++
*   LNOT : !
*   UNARY\_MINUS : 負の数値を表す +
*   UNARY\_PLUS : 正の数値を表す -

デフォルトでは改行は認めます。 ARRAY\_INIT 以外は認めたくないけどそのままとします。

### Module: NoWhitespaceBefore

\[ 追加 \]



プロパティ “tokens” に設定された文字列の前の空白が無いことをチェックします。 次のものが設定されています。

*   SEMI : ;
*   POST\_DEC : オペランドの後に付く –
*   POST\_INC : オペランドの後に付く ++

デフォルトでは改行も認めません。



セミコロン ; については Sun “Java Code Conventions” に明記していないように思うのですが、当然だと思うのでデフォルトの設定に従います。

### Module: OperatorWrap

\[ 可 \]



演算子に関する改行のポリシーをチェックします。

### Module: ParenPad

\[ 可 \]



丸括弧に関する空白のポリシーをチェックします。

### Module: TypecastParenPad

\[ 可 \]



キャストに関する空白のポリシーをチェックします。

### Module: TabCharacter

\[ 追加 \] !! Sun “Java Code Conventions” とは異なる設定です。



タブ '\\t' が使われていないことをチェックします。



これはタブの使用の可否を決めていないことを明記している Sun “Java Code Conventions” に反しますが、これまで私自身タブ '\\t' で困ったし、ドキュメントで挙げられている理由も理解できるので、 あえて「追加」とします。

### Module: WhitespaceAfter

\[ 追加 \]



プロパティ “tokens” に設定された文字列の後に空白があることをチェックします。 次のものが設定されています。

*   COMMA : ,
*   SEMI : ;
*   TYPECAST : キャスト (…)

セミコロン ; については Sun “Java Code Conventions” に明記していないように思うのですが、当然だと思うのでデフォルトの設定に従います。 for (Iterator …; …;) は別途設定しているとおり例外となります。

### Module: WhitespaceAround

\[ 変更 \]



プロパティ “tokens” に設定された文字列の前後に空白があることをチェックします。 “tokens” にはデフォルトでたくさんのものが設定されています。



プロパティ allowEmptyMethods は true にして 空のコンストラクタとメソッドについては `method (){}` とすることを許可します。

### Module: ModifierOrder

\[ 可 \]



次の順番になっていることをチェックします。

*   public
*   protected
*   private
*   abstract
*   static
*   final
*   transient
*   volatile
*   synchronized
*   native
*   strictfp

### Module: RedundantModifier

\[ 追加 \]



冗長な修飾子をチェックします。例えばインターフェイスのメソッドに public abstract を付けるのはエラーとなります。



ドキュメントに書いている理由では納得できなかったのですが、 『プログラミング言語 Java 第 3版』の該当箇所と思われる項に「慣習として…省略」 する旨記述されていたので従うことにします。

### Module: AvoidNestedBlocks

\[ 追加 \]



`{…}` だけの、つまり if 文などを伴わないブロックの無いことをチェックします。 `switch` 文について、ローカル変数を宣言するために case: 全体を、 break; も含めて `{…}` で囲むことは許可します。

### Module: EmptyBlock

\[ 追加 \]



空のブロックがないことをチェックします。



空の catch など通過することがあり得ない場合は assert false など入れておくとして、それ以外に空のブロックが発生することはほとんどなさそうなので従います。

### Module: LeftCurly

\[ 可 \]



ブロック開始の { の位置をチェックします。デフォルトでは行末です。

### Module: NeedBraces

\[ 可 \]



ブロックが {…} で囲まれていることをチェックします。

### Module: RightCurly

\[ 可 \]



else, try, catch ブロック終了の } とそれに続く文の位置をチェックします。

### Module: AvoidInlineConditionals

\[ 不可 \]



ドキュメントには対象となる範囲を詳しく書いていないのですが、 例として 3項演算子 ?: が挙げられています。 事実上これを禁止するもののようです。



Sun “Java Code Conventions” では、不適切な例を書き換えた適切なものの例としてこの 3項演算子を使ったものを挙げている箇所があります。それをさらに if-else で書き換える ( もちろん適切な形で ) ことも可能ですが、判断がつかないので「不可」とします。



ドキュメントでは「禁止している会社もある」という書き方をしていますが、周囲の意見や習慣が判断の基準になると思います。

### Module: DoubleCheckedLocking

\[ 追加 \]



アプリケーションの実装で使うことはないだろうと思いますが、この問題の詳細は "Double-Checked Locking is Broken" Declaration を参照してください。



synchronized の使用は確かに減らしたいですが、そのような背景を知らずに初めて DOL の例を見たときは何したい処理なのか意味わかりませんでした。 そこまでしたいのなら他の言語を使った方がいいのではないでしょうか。 アセンブラならきっと間違いなくできます。

### Module: EmptyStatement

\[ 追加 \]



`;` だけの行がないかチェックします。

### Module: EqualsHashCode

\[ 追加 \]



`equals()` をオーバライドした場合 `hashCode()` もオーバーライドしていることをチェックします。

### Module: HiddenField

\[ 変更 \]



ローカル変数や引数がそのクラスのメンバ変数と同じ名前になっていないかチェックします。



プロパティ ignoreSetter を true にして Setter は例外とします。

### Module: IllegalInstantiation

\[ 追加 \]



ファクトリメソッドを使用すべき箇所をチェックします。

### Module: InnerAssignment

\[ 追加 \]



次の例のようなものをチェックします。


```
    String s = Integer.toString(i = 2);
```

### Module: MagicNumber

\[ 変更 \]



マジックナンバーを禁止します。デフォルトでは -1, 0, 1 の他に 2 を許可していますが、 Sun “Java Code Conventions” の通り禁止とします。

### Module: MissingSwitchDefault

\[ 可 \]



switch 文の default: があることをチェックします。

### Module: RedundantThrows

\[ 追加 \]



`throws` の冗長な例外の定義をチェックします。

### Module: SimplifyBooleanExpression

\[ 追加 \]



- `if (b == true)`
- `b || true`
- `!false`

のようなものがないかチェックします。

### Module: SimplifyBooleanReturn

\[ 追加 \]



`boolean` 値の `return` について必要以上に複雑な書き方になっていないかチェックします。

### Module: DesignForExtension

\[ 不可 \]



static でも private でも無いメソッドについて、 次のいずれかとなっていることをチェックします。

*   abstract
*   final
*   空の実装

何かのまちがいでしょう。

### Module: FinalClass

\[ 追加 \]



プライベートなコンストラクタだけを持っているクラスが final であることをチェックします。

### Module: HideUtilityClassConstructor

\[ 追加 \]



スタティックメソッドだけを持っているクラスが public コンストラクタを持たないことをチェックします。デフォルトコンストラクタは次のようにします。


```
    protected StringUtils() {
        throw new UnsupportedOperationException(); // prevents calls from subclass
    }
```

### Module: InterfaceIsType

\[ 追加 \]



インターフェイスが 1個以上のメソッドを持つことをチェックします。



典拠は “Effective Java” ですね。たぶん。

### Module: VisibilityModifier

\[ 可 \]



`static final` のメンバ変数だけが `public` であることをチェックします。デフォルトではそれ以外のメンバ変数が `private` であることをチェックします。

### Module: ArrayTypeStyle

\[ 追加 \]



配列の定義について、C言語のように `[]` を変数の後に付けないスタイルとなっていることをチェックする。



プロパティを変更して C言語のようなスタイルにするようチェックすることも可能です。

### Module: FinalParameters

\[ 追加 \]



`abstract` でないメソッドとコンストラクタについて、パラメタが `final` であることをチェックします。



プロパティの設定により `catch` もチェックすることが可能です。

### Module: GenericIllegalRegexp

\[ 不可 \]



次のようなプロパティが設定されています。


```
    <property name="format" value="\s+$"/>
    <property name="message" value="Line has trailing spaces."/>
```



行末のスペースは無いに越したことはないのですが、 インテリジェントな開発環境が自動的に削除してくれるならともかく手作業で消すのは大変で、 品質上のメリットと釣り合うとは思えません。

### Module: TodoComment

\[ 変更 \]



コメントに TODO: が残っていないかチェックします。



これは便利な機能です。せっかくなので `":"` は外して次の文字列をチェックするようにします。

*   TODO
*   XXX
*   FIXME

### Module: UpperEll

\[ 追加 \]



`long` の定数 ( リテラル？ ) に、小文字の `l` ではなく `L` が付与されていることをチェックする。
