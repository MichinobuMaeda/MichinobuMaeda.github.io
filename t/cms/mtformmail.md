Movable Type で問い合わせページ
=====
Update: 2009-08-25

お問い合わせページを追加したのは http://www.zippyzip.jp/ ( 閉鎖 ) です。拡張子 .php のテンプレートを追加するという少し変な方法を使っています。

## 入力ページ

まず、デザインの元になる適当なテンプレートを複製して mail.php を作成しました。こんな感じ。プログラムは簡単なので説明は無し。

```
<?php
$errormessage = $_POST['errormessage'];
$name = $_POST['name'];
$from = $_POST['from'];
$body = $_POST['body'];
$ts = date('Ymdhis');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" id="sixapart-standard">
<head>
 <$mt:Include module="HTMLヘッダー"$>
 <title>お問い合わせ - <$mt:BlogName encode_html="1"$></title>
</head>
<body id="<$mt:BlogTemplateSetID$>" class="mt-entry-archive <$mt:Var name="page_layout"$>">
 <div id="container">
 <div id="container-inner">
 <$mt:Include module="バナーヘッダー"$>
 <div id="content">
 <div id="content-inner">
 <div id="alpha">
 <div id="alpha-inner">
<div class="entry-asset asset hentry">
 <div class="asset-header">
 <h1 id="page-title" class="asset-name entry-title">お問い合わせ</h1>
 </div>
 <div class="asset-content entry-content">
 <div class="asset-body">
<form action="sendmail.php" method="post">
 <p>
 <span class="sendmail_title">お名前</span>
 <input type="input" id="sendmail_name" name="name"
 value="<?php echo htmlspecialchars($name); ?>" />
 </p>
 <p>
 <span class="sendmail_title">メールアドレス</span>
 <input type="input" id="sendmail_from" name="from"
 value="<?php echo htmlspecialchars($from); ?>" />
 </p>
 <p><textarea id="sendmail_body" name="body" rows="16" cols="64"
 ><?php echo htmlspecialchars($body); ?></textarea></p>
 <p><input id="sendmail_submit" type="submit" value="OK" /></p>
 <input type="hidden" name="ts" value="<?php echo $ts; ?>" />
</form>
 </div>
 </div>
 <div class="asset-footer">
 </div>
</div>
 </div>
 </div>
 <$mt:Include module="サイドバー"$>
 </div>
 </div>
 <$mt:Include module="バナーフッター"$>
 </div>
 </div>
</body>
</html>
```

## 入力値チェックと受付完了のページ

このテンプレートを複製して少し書き換えて sendmail.php を作成しました。
*   入力値をチェックし、エラーがあれば入力ページに戻るボタンを表示します。
*   受け付けた内容を、サイト管理者とお問い合わせした人の両方にメールします。また、そのメールの内容は、所定のディレクトリに 1件 1ファイルで保存します。このディレクトリは必ず非公開の場所に作成してください。
*   受け付けた結果を表示します。
データを保存するファイル名は、入力内容を MD5 ハッシュしたファイル名にしています。入力内容が全く同じ場合、つまり、同じファイルを生成しようとした場合は、ボタンの２度押しなどによる重複と判断します。

```
<?php
// sendmail のパスとオプション
define("SENDMAIL", '/usr/sbin/sendmail -t');
// メールアドレスの書式の正規表現
define("EMAIL_FORMAT",
 '/^[0-9A-Za-z._%+-]+@([0-9A-Za-z][0-9A-Za-z-]*\.)+[A-Za-z]{2}[A-Za-z]*$/');
// メッセージを保存するディレクトリ
define("MESSAGE_DIR", '/var/www/mt-static/mail');
// サイト名
define("SITE_NAME", "Open Source で医療システム");
// URL
define("SITE_URL", "http://www.os-medico.jp/");
$errormessage = FALSE;
$name = preg_replace('/^\s/', '', preg_replace('/\s$/', '', $_POST['name']));
$from = preg_replace('/^\s/', '', preg_replace('/\s$/', '', $_POST['from']));
$body = preg_replace('/^\s/', '', preg_replace('/\s$/', '', $_POST['body']));
$ts = $_POST['ts'];
// 受付メールの配信先
$to = 'maed@michinobu.jp';
// 受付メールの From:
$sender = 'maed@michinobu.jp';
// サイト名
$site_name = "os-medico.jp";
if (!strlen($name)) {
 $errormessage .= "お名前を記入してください。\n";
}
if (!strlen($from)) {
 $errormessage .= "メールアドレスを記入してください。\n";
} elseif (0 == preg_match(EMAIL_FORMAT, $from)) {
 $errormessage .= "正しい書式でメールアドレスを入力してください。\n";
}
if (!strlen($body)) {
 $errormessage .= "本文を記入してください。\n";
}
if (!isset($ts)) {
 $errormessage .= "システムエラーです。 ".$to." にご連絡ください。\n";
} elseif (!strlen($ts)) {
 $errormessage .= "システムエラーです。 ".$to." にご連絡ください。\n";
} elseif (0 < preg_match('/[^0-9]/', $ts)) {
 $errormessage .= "システムエラーです。 ".$to." にご連絡ください。\n";
}
$file = MESSAGE_DIR.'/'.$ts.'-'.md5($name.$from.$body).'.txt';
if (file_exists($file)) {
 $errormessage .= "このお問い合わせは受付済みです。\n";
}
if ($errormessage === FALSE) {
 // 問い合わせした人に送信
 send_mail($file, $sender, $name, $from, $from, $body, $site_name);
 // 設定した配信先に送信
 send_mail($file, $sender, $name, $from, $to, $body, $site_name);
}
function send_mail($file, $sender, $name, $from, $to, $body, $site_name)
{
 $enc = mb_internal_encoding();
 mb_internal_encoding('iso-2022-jp');
 $handle = fopen($file, 'w');
 fwrite($handle,
 "From: ".$sender."\n"
 . "To: ".$to."\n"
 . "Subject: ".mb_encode_mimeheader(mb_convert_encoding(
 $site_name . " お問い合わせ受け付け", 'iso-2022-jp', 'UTF-8'), 'iso-2022-jp')."\n"
 . "Mime-Version: 1.0\n"
 . "Content-Type: text/plain; charset=ISO-2022-JP\n"
 . "\n"
 . mb_convert_encoding(
 "自動送信: \n"
 . "\n"
 . $site_name . " お問い合わせ受け付け\n"
 . "\n"
 . "次のお問い合わせを受け付けました。\n"
 . "\n"
 . "----------------------------------------------------------------\n"
 . "お名前        : ".$name."\n"
 . "メールアドレス: ".$from."\n"
 . "受付日時      : ".date(DATE_RFC822)."\n"
 . "----------------------------------------------------------------\n"
 . preg_replace('/(\r\n|\r|\n)\./', "\n .", $body)."\n"
 . "----------------------------------------------------------------\n"
 . "\n"
 . "--\n"
 . SITE_NAME."\n"
 . SITE_URL."\n"
 . $sender."\n"
 . ".\n"
 , "JIS"
 , "UTF-8")
 );
 fclose($handle);
 system('cat '.$file.' |' . SENDMAIL);
 mb_internal_encoding($enc);
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" id="sixapart-standard">
<head>
 <$mt:Include module="HTMLヘッダー"$>
<?php if ($errormessage === FALSE) { ?>
 <title>お問い合わせ受付完了 - <$mt:BlogName encode_html="1"$></title>
<?php } else { ?>
 <title>お問い合わせ受付エラー - <$mt:BlogName encode_html="1"$></title>
<?php } ?>
</head>
<body id="<$mt:BlogTemplateSetID$>" class="mt-entry-archive <$mt:Var name="page_layout"$>">
 <div id="container">
 <div id="container-inner">
 <$mt:Include module="バナーヘッダー"$>
 <div id="content">
 <div id="content-inner">
 <div id="alpha">
 <div id="alpha-inner">
 <div class="entry-asset asset hentry">
 <div class="asset-header">
<?php if ($errormessage === FALSE) { ?>
 <h1 id="page-title" class="asset-name entry-title">お問い合わせ受付完了</h1>
<?php } else { ?>
 <h1 id="page-title" class="asset-name entry-title">お問い合わせ受付エラー</h1>
<?php } ?>
 <p><a href="/">トップページに戻る</a></p>
 </div>
 <div class="asset-content entry-content">
 <div class="asset-body">
<?php if ($errormessage === FALSE) { ?>
 <p id="sendmail_message">お問い合わせの受付を完了いたしました。</p>
<?php } else { ?>
 <div id="sendmail_errormessage">
 <p><?php echo nl2br(htmlspecialchars($errormessage)); ?></p>
 <form action="mail.php" method="post">
 <input type="hidden" name="name" value="<?php echo htmlspecialchars($name); ?>" />
 <input type="hidden" name="from" value="<?php echo htmlspecialchars($from); ?>" />
 <input type="hidden" name="body" value="<?php echo htmlspecialchars($body); ?>" />
 <input id="sendmail_submit" type="submit" value="戻る" />
 </form>
 </div>
<?php } ?>
<hr class="sendmail_part" />
<div><?php echo htmlspecialchars($name); ?> 様</div>
<div><?php echo htmlspecialchars($from); ?></div>
<hr class="sendmail_part" />
<pre><?php echo htmlspecialchars($body); ?></pre>
 </div>
 </div>
 <div class="asset-footer">
 </div>
 </div>
 </div>
 </div>
 <$mt:Include module="サイドバー"$>
 </div>
 </div>
 <$mt:Include module="バナーフッター"$>
 </div>
 </div>
</body>
</html>
スタイルシートに次のような内容を追加しました。

.sendmail_title{
 display: inline-block;
 width: 8em;
}
#sendmail_name, #sendmail_from {
 width: 24em;
}
#sendmail_body {
 width: 36em;
 font-family: monospace;
}
.sendmail_part {
 margin: 1em 0;
 border: solid 1px #339999;
}
```
