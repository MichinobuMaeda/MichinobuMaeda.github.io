Laraval 5 による開発の手順 #5
=====

Update: 2018-10-14


[Laraval 5 による開発の手順 #4](startlaravel4.html) の続きです。

## 誰でもユーザ登録できる機能を削除する

私が作りたいものは、管理者が設定した会員だけが利用するシステムです。

[Laraval 5 による開発の手順 #4](startlaravel4.html) までに作成したものには "Register" メニューがあるので、それを削除します。
UI の見た目だけなくて、コントローラも削除します。

それから、ログインしていないときに表示するページはログインページでいいです。
welcome ページからログインページへの遷移はなくしたいです。
welcome ページは削除します。

まず、以下のファイルを削除します。

```
app/
  Http/
    Controllers/
      Auth/
        RegisterController.php
        VerificationController
resources/
  views/
    auth/
      register.blade.php
      verify.blade.php
      welcome.blade.php
```

トップページ ``/`` は welcome ページではなく、ログイン後に表示される home ページにします。
そのため、まず ``web.php`` の

```
Route::get('/', function () {
    return view('welcome');
});
```

を削除して、

```
Route::get('/home', 'HomeController@index')->name('home');
```

を

```
Route::get('/', 'HomeController@index')->name('home');
```

に変更します。

それから ``LoginController.php`` と ``ResetPasswordController.php`` の

```
    protected $redirectTo = '/home';
```

を

```
    protected $redirectTo = '/';
```

に変更します。

//追記(2018/10/07)：ここから//

また、 /app/Http/Middleware/RedirectIfAuthenticated.php の

```
        if (Auth::guard($guard)->check()) {
            return redirect('/home');
        }
```

を

```
        if (Auth::guard($guard)->check()) {
            return redirect('/');
        }
```

に変更します。

//追記(2018/10/07)：ここまで//

"Register" メニューのリンクは ``app.blade.php`` にあるので、

```
      <li class="nav-item">
          <a class="nav-link" href="{%raw%}{{ route('register') }}{%endraw%}">{%raw%}{{ __('Register') }}{%endraw%}</a>
      </li>
```

を削除します。

これで、誰でもユーザ登録できる機能が（たぶん）完全に無くなります。
もともと "Register" メニューに設定されていた URL を直接指定してもエラーになります。
## テスト用のユーザを追加する

まだ管理者がユーザを登録する機能を作っていないので、
Laravel 5 の Seeding 機能を利用して local の環境に限りテスト用のユーザを追加できるよにします。

```
php artisan make:seeder LocalSeeder
```

で local 環境用の ``LocalSeeder.php`` を作成し、
``DatabaseSeeder.php`` から以下のように呼び出します。

```
        // for local test.
        if (App::environment('local')) {
            $this->call(LocalSeeder::class);
        }
```

``.env`` に ``APP_ENV=local`` が設定されている場合、次のコマンドでデータベースを初期化して
local 用のテストデータを入れてテスト用サーバを起動することができます。

```
php artisan migrate:refresh --seed
php artisan serve
```

``APP_ENV=staging`` や ``APP_ENV=production`` の場合は
``LocalSeeder.php`` は無視されます。


## 日本語化する

ログインやパスワード変更に関係するページの日本語化は以下の２ファイルでできます。

```
resources/
  lang/
    ja/
      passwords.php
    ja.json
```

``resources/lang/ja.json`` のことは
[Laraval 5 による開発の手順 #3](startlaravel3.html) に書き忘れていたので追記しておきました。

パスワードリセットのために送信するメールのカスタマイズについては
[Modify Password Reset Email Text In Laravel](https://thewebtier.com/laravel/modify-password-reset-email-text-laravel/)
を参考にしました。

まず、次のコマンドでカスタマイズのためのクラスを追加します。

```
php artisan make:notification MailResetPasswordNotification
```

パスワードリセットのメールのテンプレート
``/vendor/laravel/framework/src/Illuminate/Notifications/resources/views/email.blade.php``
を見ながら
``MailResetPasswordNotification.php`` の
``public function toMail($notifiable)`` と
``resources/lang/ja.json`` に
メールの件名と本文のカスタマイズ内容を記載します。

メールの送信元は ``.env`` に以下の２行を追加すると変更できます。

```
MAIL_FROM_ADDRESS=info@abc.def
MAIL_FROM_NAME=Tamuro
```

そして、 パスワードリセット時に
``MailResetPasswordNotification`` を使ように
``app/User.php`` のスーパークラスのメソッドをオーバーライドする処理を追加します。

```
    public function sendPasswordResetNotification($token)
    {
        $this->notify(new MailResetPasswordNotification($token));
    }
```

[Laraval 5 による開発の手順 #2](startlaravel2.html)
[Mailtrap.io](https://mailtrap.io/) のアカウントを設定し、
テスト用サーバを起動して「パスワードを忘れた場合...」 からパスワードリセットメールを送信すると、
Demo inbox で HTML と Text それぞれの送信内容を確認できます。

今回カスタマイズしたメールの文面は後ほど作成する管理者からの招待メールも兼ねる予定なので、
パスワードの「再設定」ではなく「設定」という表現にしました。

----

ここまで作ったものは https://github.com/MichinobuMaeda/tamuro.git
のタグ ``startlaravel5`` です。チェックアウトの手順は
[Laraval 5 による開発の手順 #2](startlaravel2.html) の末尾をご参照ください。
チェックアウト済みであれば

```
git pull
git checkout tags/startlaravel5
```

としていただければいいです。

----

[Laraval 5 による開発の手順 #6](startlaravel6.html) に続く。

Tag: PHP Laravel Mailtrap
