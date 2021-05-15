HTTP で Redirect しよう
=====

Update: 2011-01-29

こちらの記事 ["How To Redirect A Web Page, The Smart Way"](http://www.stevenhargrove.com/redirect-web-pages/) によると、 Web サイトの引っ越しをする場合、 HTML で `<meta http-equiv="refresh" ...` とかしてリダイレクトしちゃだめなのだそうです。この方法は SPAM のために使われてきたので、サーチエンジンに嫌われるとのこと。 HTML ファイルに直接書かず JavaScript でどうにかしたとしても、そのくらいのものはサーチエンジンが容易に検出してしまうのでダメ。そのかわりに、 HTTP のステータス 301 でリダイレクトしましょうとのことです。



Apache の場合についてはこちらのページ [http://httpd.apache.org/docs/2.0/mod/mod\_alias.html](http://httpd.apache.org/docs/2.0/mod/mod_alias.html) に `http.conf` や `.htaccess` に記述する構文と例が出ています。 `"Redirect"` ディレクティブです。 `"``Redirect"` ディレクティブのデフォルトはステータス 302  ( 一時的な移動という意味 ) になるので、引数 `"permanent"` を設定するか、 `"RedirectPermanent"` ディレクティブを使うかどちらかにします。日本語 ( というか UTF-8 ) のパス名もでだいじょうぶなようです。



それ以外の様々な環境や言語の場合の例が ["How To Redirect A Web Page, The Smart Way"](http://www.stevenhargrove.com/redirect-web-pages/) に載っています。



それから、 [Canonical Link](http://www.mattcutts.com/blog/canonical-link-tag/) についても記しています。これは、サブドメイン間で使うことはできるのですが、異なるドメインの間では使えないとのことです。
