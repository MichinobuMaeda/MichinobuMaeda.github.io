自分用 Checkstyle 5.0 暫定対応
=====

Update: 2010-01-04



以前 sun_checks.xml をカスタマイズしたもの ( [Checkstyle をチェックする](checkstyle4me.html) 参照 ) を、 Checkstyle 5.0 に対応できるように修正しました。

*   PackageHtml を JavadocPackage に変更しました。
*   FileLength と FileTabCharacter が Checker の直系の子どもになりました。

Checkstyle 5.0 ではこれら以外にたくさんのモジュールが変更されていますが、今回はとりあえずここまで。



```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE module PUBLIC
"-//Puppy Crawl//DTD Check Configuration 1.2//EN"
"http://www.puppycrawl.com/dtds/configuration_1_2.dtd">
<!--
 Checkstyle 4.1 の配布物に含まれる設定ファイル sun_checks.xml
 をカスタマイズしたものです。カスタマイズの内容の詳細は
 http://www.michinobu.jp/article.php/CheckCheckstyle
 をご参照ください。
 Checkstyle 5.0 に対応できるよう修正しました。
 http://www.michinobu.jp/article.php/CheckCheckstyle5.0
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
  <module name="JavadocPackage"/>
  <module name="Translation"/>
  <module name="FileLength"/>
  <module name="FileTabCharacter"/>
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
