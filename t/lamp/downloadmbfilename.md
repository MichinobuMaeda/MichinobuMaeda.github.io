Webから日本語ファイル名でダウンロード
=====

Update: 2009-07-13



「Webから日本語ファイル名でダウンロードさせたいんだけどどうすればいい？」と [eubun さん](http://eibun.com/) から質問が。こんなかんじでいいようです。


```
<?php
// ブラウザの種類がIEかどうかを判別する。
$isIE = (preg_match('/IE/', $_SERVER['HTTP_USER_AGENT']) == 0) ? FALSE : TRUE;
// GETパラメータでファイルのサーバ上のパス名とユーザから見えるファイル名を受け取る。
$path = $_GET["path"];
$name = $_GET["name"];
// ファイルの拡張子から、Content-typeを確定する。
if (preg_match('/.pdf$/i', $name) == 1) {
 $type = "application/pdf";
} elseif (preg_match('/.doc$/i', $name) == 1) {
 $type = "application/vnd.ms-word";
} elseif (preg_match('/.xls$/i', $name) == 1) {
 $type = "application/vnd.ms-exce";
} elseif (preg_match('/.ppt$/i', $name) == 1) {
 $type = "application/vnd.ms-powerpoint";
} else {
 $type = "application/binary";
}
// HTTPレスポンスヘッダを出力する。
header("Content-Transfer-Encoding: binary");
header("Content-Type: ".$type);
header("Content-Length: " . filesize($path));
if ($isIE) {
 header("Content-Disposition: inline; filename=".$name);
 header("Pragma: public");
 header("Cache-Control: must-revalidate, post-check=0, pre-check=0");
} else {
 header('Content-Disposition: attachment; filename="' . $name . '"');
 header("Pragma: no-cache");
}
// ファイルを返す。
readfile($path);
?>
```
