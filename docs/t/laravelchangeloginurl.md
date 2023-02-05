# Laravel のログインページの URL を変更する

Update: 2019-01-01


Laravel で作成中のサイトにログイン方法を選択するページを追加して、
そのページが最初に表示されるようにしようと思ったのですが、
そのあたりはフレームワークが提供する機能で設定されていて、
どこを変えたらいいのかよくわかりません。
とはいえ、同じことを考える人はいるだろうとぐぐってみたらいました。

[Laravel 5.4 change login url](https://laracasts.com/discuss/channels/laravel/laravel-54-change-login-url)

やり方としては２通りあります。どちらもこのページに出ています。

## Route を個別に定義する

フレームワークが用意しているルートは ``routes/web.php`` の ``Auth::routes();``
で一括で指定しているのですが、これを消して

```
Route::get('`myNewLoginPageYay/', 'Auth\LoginController@showLoginForm')->name('login');
```

のように個別に定義すればよいとのことです。

私が作成中ものはクローズドな会員向けのサイトなので、
``Auth::routes();`` だと不要なルートが設定されていますから、
ついでにいらないものを決しておくことにします。

```
Route::get(
  'login/password',
  'Auth\LoginController@showLoginForm'
)->name('login');
Route::post(
  'login/password',
  'Auth\LoginController@login'
);
Route::post(
  'logout',
  'Auth\LoginController@logout'
)->name('logout');
Route::get(
  'password/reset',
  'Auth\ForgotPasswordController@showLinkRequestForm'
)->name('password.request');
Route::post(
  'password/email',
  'Auth\ForgotPasswordController@sendResetLinkEmail'
)->name('password.email');
Route::get(
  'password/reset/{token}',
  'Auth\ResetPasswordController@showResetForm'
)->name('password.reset');
Route::post(
  'password/reset',
  'Auth\ResetPasswordController@reset'
)->name('password.update');
```

## 認証前のリダイレクト先を変える

``app/Exceptions/Handler.php`` に

```
    public function unauthenticated($request, AuthenticationException $exception)
    {
        return redirect()->guest(route('name'));
    }
```

のようなコードを追加すると ``AuthenticationException`` を拾ってくれるそうです。

Tag: Laravel
