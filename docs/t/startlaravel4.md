# Laraval 5 による開発の手順 #4

Update: 2018-10-04


[Laraval 5 による開発の手順 #3](startlaravel3.html) の続きです。

## 所属するグループに基づく権限の管理

これから私が Larval 5 で作ろうとしているアプリには
LDAP のように組織を管理する機能が必要です。
利用者からヒアリングしたところでは概ね以下のような特別な権限があればよさそうです。
いずれの権限も、複数のメンバーが担当します。

- 全体を管理する権限
- システムの管理をする権限
- それぞれのグループを管理する権限

全体を管理する人は、権限とグループとユーザを追加、更新、削除します。

システムを管理する人は、全体を管理する人から委任されて、アプリのメンテナンスをします。

それぞれのグループを管理する人は、全体を管理する人から委任されて、担当するグループを更新し、グループに属するユーザーを更新します。

グループとユーザの新規作成と削除、所属するグループの変更は全体を管理する人にしかできません。ユーザ本人も、自分が所属するグループを変更することはできません。グループメンバーの変更（ユーザが所属するグループの変更）の権限を制限するのは、セキュリティ上の理由ですが、詳細は省きます。

## モデル

ユーザは Laravel 5 の User モデルをそのまま使います。ただし、後で、認証手段やプロファイルなどを追加します。

グループは３種類用意します。それぞれ、複数の管理者とメンバーを設定できます。

- Primary group
- System administrators
- その他

"Primary group" はすべてのグループとユーザが直接・間接に所属するトップレベルのグループです。
Role ( 役割 ) 名 "primary" で表します。

"System administrators" はシステム管理者が所属するグループです。
Role ( 役割 ) 名 "sysadmin" で表します。

それら以外に任意のグループを作ることができます。

"Primary group" の管理者は、全体を管理する権限を持ちます。
"Primary group" 以外のグループの管理者は、そのグループを管理する権限を持ちます。

アプリの初期構築時には、 "Primary group" と "System administrators" だけを作成します。
また、ユーザを一人だけ作成し、そのユーザは
"Primary group" の管理者と、 "System administrators" のメンバーになります。

"Primary group" が所属するグループはありません。

"Primary group" 以外のグループはいずれかのグループに所属する必要があります。
また、グループの所属の循環 ( グループ A がグループ B に所属し、グループ B がグループ A に所属する ) を避けて、
すべてのグループは "Primary group" の直接・間接の下位のグループにならなければなりません。

ユーザはいずれかのグループに所属しなければなりません。

"Primary group" 以外のグループとユーザは、複数のグループに所属することができます。

以上のような関係を、 User モデル、 Group モデル、 GroupRole モデルで表現します。

## リレーション

前項のモデルの関係は多対多ばかりになります（涙）。だから LDAP のような組織を管理するための専用のものがあるわけですね。多対多の関係は、オーソドックスな方式に従って関係テーブルで表現することにします。
以下のようなテーブルを作成します。

  * ``users`` : User モデル
  * ``groups`` : Group モデル
  * ``group_roles`` : GroupRole モデル、兼、GroupRole モデルとグループの関係
  * ``sub_groups`` : グループに対してグループが所属する関係
  * ``members`` : グループに対してユーザが所属する関係
  * ``group_manager`` : グループに対してユーザが管理者になる関係

``group_roles`` テーブルは Group の ID と Role 名 ( "primary", "sysadmin" ) だけの小さなテーブルです。
性能・負荷と将来の拡張性を考慮してこのような形にしています。

本来は GroupRole モデルと Group モデルの関係テーブルを置くのが概念的に正しいと思うのですが、
その通りにするとますます無用に複雑な実装になってしまうので、適当なところで妥協しました。

## 実装

データベースのテーブルは Laravel の migration を使って作成します。

```
php artisan make:migration CreateGroupTable
```

のようなコマンドで ``database/migrations`` の下に各テーブルの箱を作って、
自動で作成されている ``users`` や Laravel 5.7 のドキュメントの
https://laravel.com/docs/5.7/migrations
を参考に中身を作ります。

モデルも

```
php artisan make:model Group
```

のようなコマンドで箱を作ります。多対１、多対多の関係の表現については
Laravel 5.7 のドキュメントの
https://laravel.com/docs/5.7/eloquent-relationships
を見てください。

User モデルには、「全体を管理する権限があるか？」、「システムの管理をする権限があるか？」、「引数で渡したグループまたはユーザの管理をする権限があるか？」を取得するメソッドを追加しました。

これらのモデルのテストのために ``tests/Unit/ModelsTest.php``
を作成しましたが、後でモデルが増えることを考えるとこのファイル名はよくないかな。。。

初期データは Laravel 5 の Seeding 機能を使います。

```
php artisan make:seeder GroupsTableSeeder
```

のようなコマンドで User と Group の Seeder を作成して、
``database/seeds/DatabaseSeeder.php`` から呼び出します。

----

ここまで作ったものは https://github.com/MichinobuMaeda/tamuro.git
のタグ startlaravel4 です。チェックアウトの手順は
[Laraval 5 による開発の手順 #2](startlaravel2.html)
の末尾をご参照ください。チェックアウト済みであれば

```
git pull
git checkout tags/startlaravel4
```

としていただければいいです。

----

[Laraval 5 による開発の手順 #5](startlaravel5.html) に続く。

Tag: PHP Laravel
