Google Firebase のプロジェクトの設定
=====

Update: 2020-07-11


[Firebase](https://firebase.google.com/) というのは Google 社が2014年に買い取ったモバイルアプリ、Webアプリ向けのデータ ＆ 認証の
BaaS ( backend-as-a-service ) です。
データベースは NoSQL のドキュメント型で、認証と連携したアクセス権の設定が細かくできます。
認証はメアドとパスワードの他、メールでログイン用のリンクを取得する手順、OAuth ( 「○○でログイン」 ) などが用意されています。
アプリの案内や、 SPA （ Single-page application ） や PWA ( Progressive web application )
のアプリを置くための Webホスティングもできます。
単純なアプリでしたらサーバ側のプログラムは無しでもいけます。
ストレージや IoT などの [Google Cloud](https://cloud.google.com/) の他のサービスとの連携もできます。

以下、この Firebase の新規プロジェクトの作成手順です。

## アカウントと支払い

Firebase のプロジェクトは Google Cloud のプロジェクトなので、
Google Cloud のアカウントが無ければ作成してください。
使用料の支払いも Google Cloud のプロジェクトとしての請求になるので、
Google Cloud のコンソールで支払い方法の設定をしてください。

手順は Google Cloud のページの案内の通りなので説明は省略します。

なお、基本機能だけを試用する場合は、支払いの設定は無しでだいじょうぶです。

## Node.js

後述の Firebase CLI のために必要です。 8.x 以降であればよいと思います ( 2020年 4月 時点 )。

Linux の場合、 Windows 10 で [WSL ( Windows Subsystem for Linux )](https://docs.microsoft.com/ja-jp/windows/wsl/install-win10)
を利用する場合は ``yum`` とか ``apt`` で入れてください。
Mac は [Homebrew](https://brew.sh/) 、
Windows で WSL を使わない場合は [Chocolatey](https://chocolatey.org/) が無難です。

## プロジェクトの設定

特に独自ドメイン名の設定などしない限り、プロジェクト名は Webホスティングのサブドメイン名になります。

  * https://project-name.firebaseapp.com/
  * https://project-name.web.app/

テスト用にプロジェクト名に "-test" を追加した名称のプロジェクトも作っておくとよいです。

プロジェクト名が既に使われている場合は、数字をてきと〜に追加した名称を自動生成してくれます。

  - [コンソール](https://console.firebase.google.com/) にログインする。
  - "+ Add project"
    - "Project name" にプロジェクト名を入力して、もし、数字付きの名称が自動生成されたらそれでいいかどうか考える。いやならがんばって別の名称を考える。
    - Google Analytics を使うか？ と聞かれるので要不要を選択する。
    - "Create project"
  - プロジェクトのページの左側メニュー "Settings"
    - "Project settings"
      - "Google Cloud Platform (GCP) resource location" を選択する。 ( やり直し不可!! )
        * asia-northeast1 : 東京
        * asia-northeast2 : 大阪
        * asia-northeast2 : ソウル
      - "Public-facing name" はプロジェクト名と同じでいいんじゃないかな。
      - "Support email" はとりあえず自分のメアド。
      - "Select a platform to get started" で今回は SPA にするので Web （</>） を選択する。
        - "App nickname" はプロジェクト名と同じでいいんじゃないかな。
        - "Also set up Firebase Hosting for ..." は On にする。
        - "Register App"
        - HTMLの <head> に記載するコード・スニペットが表示されるが、後でも出てくるのでとりあえず先に進む。
        - "Next"
        - ``firebase-tools`` のインストール手順が表示されるので、まだなら実行する。 Node.js が必要。
        - "Next"
        - "Deploy to Firebase Hosting" の手順は後ほど。
        - "Continue to console"
        - "Firebase SDK snippet" に数種類表示されますが、必要なものを選んで使ってください。なお ``apiKey`` をソースにそのまま入れて GitHub の Public プロジェクトに Push すると「危ないことするな」とおこられます。
      - "Users and permissions" にプロジェクトメンバーを追加する。
  - プロジェクトのページの左側メニュー "Authentication"
    - "Sign-in method" で必要なものを有効にする。
    - "Templates"
      - "Template language" : Japanese
  - プロジェクトのページの左側メニュー "Database"
    - "Go to Cloud Platform"
      - Firebase のリアルタイム更新機能を使う場合は "SWITCH TO NATIVE MODE" ( やり直し不可!! )
      - Go to Cloud Platform のページを閉じて Firebase の Database のページを更新すると "Data", "Rules" などのメニューが表示される。設定はアプリの作成の中で。
  - プロジェクトのページの左側メニュー "Storage" は必要であれば "Get started" で有効化する。
  - プロジェクトのページの左側メニュー "Hosting" は特に設定は上記の "Settings" で設定済み。あとはコンテンツ作成後にデプロイすればよい。
  - プロジェクトのページの左側メニュー "Storage" は必要であれば "Get started" で有効化する。

## プロジェクトの作成

[Quasar Framework](https://quasar.dev/) の場合

```
$ quasar create project-name
$ cd project-name
$ firebase login
$ firebase init
$ firebase use project-name
$ firebase projects:list
```

Tag:



