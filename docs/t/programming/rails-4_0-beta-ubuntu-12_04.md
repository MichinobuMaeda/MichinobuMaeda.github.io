# Rails 4.0 beta を Ubuntu 12.04 に入れてみた

Update: 2012-12-16



Rails 未経験の私がひょんなことで Rails 4.0 beta を使ってみることになりました。職場の iMac に続いて自分の MacBook 中の VM で動いている Ubuntu に入れた記録です。MacBook にそのまま入れなかったのは、あまりきれいな環境ではなくて依存するものなど把握するにはよくない状態だからです。ベースにしたのは [CouchDBを始めてみようと思ったのですが。。。](https://sites.google.com/site/michinobumaeda/database/couchd-jpcommu) を入れた環境です。Ruby は入っていません。

- Create a Rails 4.0 Beta Project [http://www.drurly.com/blog/2012/09/08/create-a-rails-4-project](http://www.drurly.com/blog/2012/09/08/create-a-rails-4-project)
- Installing rails 4.0.0 beta [https://gist.github.com/2515536](https://gist.github.com/2515536)

を参考にしました。



まず RVM を。


```
$ curl -L https://get.rvm.io | bash -s stable
$ . .bashrc
$ rvm --version
$ rvm requirements
$ sudo apt-get install build-essential openssl libreadline6 libreadline6-dev curl git-core zlib1g zlib1g-dev ibssl-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt-dev autoconf libc6-dev ncurses-dev automake ibtool bison subversion pkg-config
$ sudo apt-get install nodejs
$ rvm install 1.9.3 --default
$ ruby --version
$ rvm gemset create rails-4.0-beta
$ bash --login
$ rvm 1.9.3@rails-4.0-beta
```

次に Rails の最新を github からとってきてお勉強用の blog アプリを作ろうとしましたが、いろいろ足りないと言われます。


```
$ mkdir github
$ cd github
$ git clone https://github.com/rails/rails.git
$ ruby rails/railties/bin/rails new blog --dev
```

足りないものを入れて、こんな入れ方でいいのかな？ 再実行。


```
$ gem install thread_safe
$ gem install i18n
$ gem install thor
$ ruby rails/railties/bin/rails new blog --dev
$ cd blog
$ vi Gemfile
```



結果おーらいということで、 Gemfile をこんな感じに。


```
source https://rubygems.org

gem 'rails', path: '/home/michinobu/github/rails'
gem 'journey', :git => 'git://github.com/rails/journey.git'
gem 'arel'
gem 'activerecord-deprecated_finders', git: 'git://github.com/rails/activerecord-deprecated_finders.git'

gem 'sqlite3'

# Gems used only for assets and not required
# in production environments by default.
group :assets do
  gem 'sprockets-rails'
  gem 'sass-rails', :git => 'git://github.com/rails/sass-rails.git'
  gem 'coffee-rails', :git => 'git://github.com/rails/coffee-rails.git'

  # See https://github.com/sstephenson/execjs#readme for more supported runtimes
  # gem 'therubyracer', platforms: :ruby

  gem 'uglifier', '1.0.3'
end

gem jquery-rails

# Turbolinks makes following links in your web application faster. Read more: https://github.com/rails/turbolinks
gem 'turbolinks'

# To use ActiveModel has_secure_password
# gem 'bcrypt-ruby', '~> 3.0.0'

# Build JSON APIs with ease. Read more: https://github.com/rails/jbuilder
# gem 'jbuilder'

# Use unicorn as the app server
# gem 'unicorn'

# Deploy with Capistrano
# gem 'capistrano', group: :development

# To use debugger
# gem 'debugger'
```

動かしてみます。


```
$ bundle install --binstubs
$ bin/rails -v
$ bin/rails s
```

ブラウザで表示してみます。

```
$ firefox http://127.0.0.1:3000/ &
```

ガイドの HTML を生成します。

```
$ cd ../rails/guides
$ rake guides:generate:html
```

またいろいろ足りないと言われるので、こんな入れ方でいいのかな？と思いつつ入れて、何はともあれできました。


```
$ gem install redcarpet
$ gem install nokogiri
$ gem install thread_safe
$ gem install i18n
$ gem install rack
$ gem install erubis
$ rake guides:generate:html
$ firefox output/index.html &
```



で、生成されたガイドの "Getting Started with Rails" なのですが、 http://guides.rubyonrails.org/getting\_started.html とは違うもので、 http://edgeguides.rubyonrails.org/getting\_started.html に近いもののようなのですが、どうも Strong Parameters 対応していないような。。。



## 追記：

新しいページを作るほどの内容ではないので、続きをここに。



この手順でインストールした場合、サーバは WEBrick になります。ところが、その WEBrick のログ出力でトラブって `*.css` や `*.js` の一部が読み込めないという困ったことになっていました。 WEBrick のソースを見ると確かにあまり凝った作りではないなあ。。。というわけで、職場で使っている Phusion Passenger を入れることにしました。



インストールはこの一行だけ。


```
$ gem install passenger
```

ガイドに従って次のように起動しようとすると、パスの通っているところにはいません。



```
$ sudo passenger start -p 80
```

探してみると `~/.rvm/gems/ruby-1.9.3-p327@rails-4.0-beta/bin/passenger` にいます。ポート 80 使う必要もないし、次のようにして起動しました。


```
$ ~/.rvm/gems/ruby-1.9.3-p327@rails-4.0-beta/bin/passenger start -p 3000
```

すると、なにやらいろいろダウンロードしてセットアップしている様子です。 nginx-1.2.4.tar.gz とかも入れようとしている模様。それらの処理が終わると、そのままサービスを始めました。


```
Processing by WelcomeController#index as HTML
Can't verify CSRF token authenticity
```

以外にはエラーは出ていないようです。
