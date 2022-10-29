# Firebase, Flutter, Google Cloud Workstations

Update: 2022-11-26

## A. 概要

### Firebase

<https://firebase.google.com/>

GCP: Google Cloud Platform のサービスで、以下のようなものがセットになった Serverless のシステム基盤です。

- Authentication: 認証基盤
- Firestore: NoSQL でトランザクションをサポートしたデータベース
- Cloud Storage: 画像や文書などのファイルを格納するストレージ
- Cloud Functions: プロセスの常駐は不可で単発の処理だけができるサーバ側実行環境
- Hosting: 静的なファイルだけを置くことができる Webサーバ
- その他、メッセージ配信、メール送信（メールサーバは別途必要）、アクセス解析など

Firestore と Cloud Stroage は Authentication と組み合わせたアクセス制御が可能です。
Firestore はデータの内容に基づく動的な制御が可能で、アカウントやアカウントの権限・グループ等に紐付ける形で、読み書きのアクセス権を定義できます。

Firestore の RDBとの違いは、

- スキーマの定義が不要
- 更新データのプッシュ配信が可能

で、チャットなどのアプリが容易に構築できます。

### Flutter

<https://flutter.dev/>

Google が作ったモバイルアプリ用のフレームワークです。
JavaScript に似た Dart という言語を使います。 JavaScript と違って型の定義が必要なので Java にも似ています。
Flutter は一つのコードから以下の OS向けの実行モジュールを生成できます。

- Android
- iOS/iPadOS
- Web ( SPA: Single-Page Application / PWA: Progressiv Web Apps )
- Windows
- Mac OS
- Linux

見た目の雰囲気は、以下のどちらかを選択できます。

- Material ( Android 風 )
- Cupertino ( iOS 風 )

Flutter は OS やブラウザの UI部品を使わず、すべて自前で描画するので、
異なる OS でもほとんど同じ見た目になります。

サンプル: <https://pages.michinobu.jp/honkipass/>

#### 参考: React Native との違い

Facebook ( Meta ) の React Native は OS の UI部品を使います。
対応する OS は Android と iOS/iPadOS だけで、デスクトップ OS には対応していません。
Web向けの React とロジックは共有できますが、プレゼンテーション層は完全には共有できないようです。

### Google Cloud Workstations

<https://cloud.google.com/workstations>

クラウド上の開発環境で、 Debian Linux の仮想マシンと Web版エディタなどがセットになっています。
Visual Studio Code とほぼ同じ仕様の Code OSS が Web上で利用できます。

- 非力なPCやChromebookで開発したい場合。
- 自分のPCで複数のバージョンの言語やライブラリを管理するのが煩わしい場合。

後述する gcloud CLI が不要であれば iPad や Android タブレットでも利用可能かもしれない。

## B. 環境の準備

以下の順番で環境を作成する。

1. GCP のアカウントの作成（無い場合）
2. Firebase プロジェクトの作成（他人と重複しないプロジェクト名が必要）
3. gcloud CLI のインストール
4. Workstation の作成
5. 必要なパッケージのインストール
6. Flutter のプロジェクトの作成
7. GitHub のアカウントの作成（無い場合）
8. GitHub のリポジトリの作成
9. Firebase の設定の追加

### 1. GCP のアカウントの作成

- Gmail のアドレスが無ければ作成する。
    - Android スマホ購入時に作成したものでもよいが、仕事で使う場合は 2要素認証の設定がお勧め。
- https://cloud.google.com/ からアカウントを登録する。
- 支配の設定をする。
    - 手順: [支払い方法の追加、削除、更新](https://cloud.google.com/billing/docs/how-to/payment-methods)
    - 各プロジェクトの支払いの有無と支払いを担当するアカウントは後から変更が可能。

### 2. Firebase プロジェクトの作成

Firebase　のプロジェクトを作成すると自動で同じIDの GCP のプロジェクトができる。
プロジェクトID を Flutter のパッケージ名と同じにする場合は、英小文字と数字だけにしておくとよい。
テスト用のプロジェクトを作る場合は「プロジェクトID-test」のようなIDのプロジェクトを追加で作成するとよい。
Webを利用する場合はプロジェクトIDがそのままURLの一部になるので、ランダムな文字列などのてきとーなIDは後悔することになる。

### 3. gcloud CLI のインストール

手順: [Google Cloud Workstations を使ってみる](https://pages.michinobu.jp/t/googlecloudworkstations.html) 前半

### 4. Workstation の作成

手順: [Google Cloud Workstations を使ってみる](https://pages.michinobu.jp/t/googlecloudworkstations.html) 後半

### 5. 必要なパッケージのインストール

どうも Workstation を再起動すると `apt` でインストールしたものが消えているようなので
[Homebrew](https://brew.sh/) を使いました。
Homebrew は Mac OS でよく使われているパッケージマネージャです。
`yum` や 'apt' などの Linux の標準のパッケージマネージャと違って、インストールする言語のバージョンの設定ができるのが便利です。

Flutter はバージョンアップが速いので、 FVM: Flutter Version Management を使います。

Firebase Tools のために Node.js が必要です。また、 Firebase Emulator のために Java が必要です。

### 6. Flutter のプロジェクトの作成

### 7. GitHub のアカウントの作成

私の場合は [MichinobuMaeda](http://github.com/MichinobuMaeda/>)

### 8. GitHub のリポジトリの作成

Firebase のプロジェクト名や Flutter のパッケージ名と同じにしておくといいです。
リポジトリのURLは `http://github.com/アカウント名/リポジトリ名` です。

### 9. Firebase の設定の追加

Tag: firebase flutter github
