Windows 7 x64 でイベントログをコマンドラインで参照
=====

Update: 2009-12-17



仕事で Windows のイベントログを監視するスクリプトを作ることになって、「たしか `eventlogquery` というコマンドがあったよなぁ」と自宅の Windows 7 x64 で試してみようとしたところ、ありません。おかしいなぁ。。。



64bit OS だとなにかあったり、無かったり、するのでしょうか。VBScript で実装されたツールだから、自前でも何とかなるかなと調べていたら、ベースになりそうなものがありました。 [WMI スクリプト入門](http://msdn.microsoft.com/ja-jp/library/ms974579.aspx) : 第 1 部 の「リスト 3. Windows イベント ログ レコードを読み取る」です。



この WMI は ActivePerl などからでも呼び出せるそうです。今回はシステムのエラーをメール配信しようとしているのですが、メール送信は ActivePerl でつくったスクリプトが既にいい感じで動いています。それと組み合わせて使うことにしよう、と調べ始めたら今度は Win32::EventLog というのを見つけました。一覧を表示するにはとりあえずこんな感じかな？


```
use strict;
use Win32::EventLog;
my $handle=Win32::EventLog->new("Application");
my $recs;
my $base;
my $hashRef;
my $x = 0;
$handle->GetNumber($recs);
$handle->GetOldest($base);
print "base: $base recs: $recs\n";
while ($x < $recs) {
 print "\n";
 $handle->Read(EVENTLOG_FORWARDS_READ|EVENTLOG_SEEK_READ, $base + $x, $hashRef);
 Win32::EventLog::GetMessageText($hashRef);
 foreach my $key (keys(%$hashRef)) {
 next if ($key eq "Message");
 print "$key:\t$hashRef->{$key}\n";
 }
 print "Message:\n$hashRef->{Message}\n";
 $x++;
}
```
