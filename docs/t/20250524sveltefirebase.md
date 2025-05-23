# Svelte と Firebase で複数ソーシャルメディア同時予約投稿

Update: 2025-05-24

コンピュータ・ユニオン関西 IT 支部の技術交流会の発表資料です。いっしょに作る人、売ってくれる人を募集中です。

ソース: <https://github.com/MichinobuMaeda/black-bream>

## A. 機能

### A-1. 実現した機能

-   複数のソーシャルメディアに日時指定で記事を投稿する。
-   対応しているソーシャルメディアサービス
    -   X
    -   Mastodon
    -   Misskey
    -   Bluesky
    -   Threads
    -   Instagram
    -   Tumblr
-   画像は 1 枚だけ可。
-   画像のファイルサイズを 1MB 未満に縮小する。 ※一部のソーシャルメディアサービスで必要
-   リンクのカードを生成してくれないソーシャルメディアについては、こちらで生成する。
-   文面のテンプレートを複数作成できる。
-   日時指定のためによく使う曜日・時刻を複数登録できる。

### A-2. 作成中の機能

-   WordPress の RSS を日次で取得し、登録済みのテンプレートと曜日・時刻に更新のお知らせを投稿する。

### A-3. 検討している機能

-   WordPress の更新のお知らせで AI による記事の要約を作成する。

### A-4. 欠点

-   Bluesky 以外のサービスについてはそれぞれ開発者アカウントでアプリの登録が必要です。これが面倒です。

## B. 利用した製品・サービス

### B-1. Svelte

JavaScript を使う Web フレームワーク。今回は PWA ( Progressive Web Apps ) の形のものを作成した。

React や Flutter と同様に変数の値が変わると表示が変わる仕組みなので、少ないプログラムで機能が実現できる。
React との違いは以下の通り。

-   State Management の仕組みが最初から入っている。
-   ほぼ普通の HTML を使う。

### B-2. Firebase

Google Cloud のサービスで、主にモバイルアプリで使われる機能をセットにしたもの。

### B-2-1. Cloud Functions

単発の処理を登録するサーバレスの機能。
AWS の Lambda と同様のもの。
Firebase 版は JavaScript と Python で利用可能。
CRON と同様の書式で定時のジョブを設定することが可能。

### B-2-2. Firestore

NoSQL のスキーマレスのデータベースで、アプリに対して Push 配信が可能。
Firebase の認証の機能と組み合わせて細かなアクセス制限を設定することができるため、小規模なアプリであれば次項の
Cloud Functions 等との組み合わせでサーバレスの環境を実現できる。
Cloud Functions をトリガーとして利用可能。

### B-2-3. Cloud Storage

AWS の S3 と同様のオブジェクトストアー。今回は画像の保管に利用した。
Cloud Functions をトリガーとして利用可能。

### B-2-4. Cloud Tasks

Cloud Functions に登録した処理を起動する Task queue を作成できる。
起動のパラメータの指定が可能。
即時または日時指定による実行が可能。

## B-3. 自家製 UI パーツ

Google の Material Design 3 におおむね準拠したもの。 Svelte 専用。テーマカラー生成機能付き。

<https://github.com/MichinobuMaeda/coarse-paper>

## B-4. Tailwind

上記の UI パーツの作成で利用した CSS フレームワーク。パーツの作成の他、レスポンシブなレイアウトの実現も可能。

## B-5. GitHub Actions

ソースの更新をトリガーに自動で以下の処理を実行し、複数のサイトにそれぞれ異なる設定でデプロイする。

-   自動テストプログラムの実行 ※テスト不合格の場合は後続の処理を中止
-   自動テストのカバレッジの結果を後述の Codecov にアップロード
-   サイト毎の設定を適用してビルド
-   各サイトにデプロイ
-   各サイトで Cloud Functions に登録されたデータ移行のための処理を実行

現在、デプロイ先のサイトは以下の２箇所。アプリ名とテーマカラーが異なる。

-   ソフトウェアセクション用
-   個人用

## B-6. Codecov

-   自動テストのカバレッジの集計と表示

<https://app.codecov.io/gh/MichinobuMaeda/black-bream>

Tag: svelte firebase CI Tailwind
