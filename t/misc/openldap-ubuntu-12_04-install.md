OpenLDAP を Ubuntu 12.04 にインストール
=====

Update: 2012-12-23



OpenLDAP を Ubuntu 12.04 にインストールしました。

*   できるだけデフォルトのまま手をかけずにセットアップする。
*   ディレクトリは公開しない。
*   管理者は複数いて、管理用のアカウントは共有しなくて済むようにする。

ということで、以下、その手順です。私自身は `uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp` になります。内容は [OpenLDAP でミラーリング](misc/openldap-mirror.html) と一部重複します。

日本語の入門書としては [『入門LDAP/OpenLDAP―ディレクトリサービス導入・運用ガイド』](http://www.amazon.co.jp/%E5%85%A5%E9%96%80LDAP-OpenLDAP%E2%80%95%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E5%B0%8E%E5%85%A5%E3%83%BB%E9%81%8B%E7%94%A8%E3%82%AC%E3%82%A4%E3%83%89-%E3%83%87%E3%83%BC%E3%82%B8%E3%83%BC%E3%83%8D%E3%83%83%E3%83%88/dp/4798033499/ref=pd_sim_sbs_b_1) がありますが、私は旧版しか読んでいません。 [http://www.openldap.org/doc/admin24/slapdconfig.html](http://www.openldap.org/doc/admin24/slapdconfig.html) によると `slapd.conf` は deprecated になってしまったということで旧版の手順はそのまま使えなかったのですが、概念の理解と応用については十分参考になります。

## OSの設定

Ubuntu の slapd のパッケージは、インストール時にホスト名を基に初期データベースをセットアップしてくれます。そのまま使うことができるととても楽なのですが、そうでない場合はかなり面倒です。初期データベースの設定が予定と違う場合、どう直したらいいのか私にはわかりませんでした。データベースを追加することはできるのですが、消すことができないとゴミが残ります。私のテスト環境の場合、インストール開始前に以下のようにしました。

`/etc/hostname`

```
u1204s2.home.michinobu.jp
```

`/etc/hosts`

```
127.0.0.1    localhost
127.0.1.1    u1204s2.home.michinobu.jp    u1204s2
```

「127.0.1.1 てなんやねん？」という人は [127.0.1.1 って？](https://sites.google.com/site/michinobumaeda/hardware-os/whats127-0-1-1) をご参照ください。で、「そのやり方はどないやねん」という人は Ubuntu コミュニティに突っ込んであげてください ( 英語で ) 。たぶんきれいに解決する方法はありません。

## パッケージのインストール

参考にしたのは [https://help.ubuntu.com/10.04/serverguide/openldap-server.html](https://help.ubuntu.com/10.04/serverguide/openldap-server.html) です。インストールするものはこれだけです。


```
$ sudo apt-get install slapd ldap-utils
```

インストールした結果を見てみます。 `dc=home,dc=michinobu,dc=jp` の箱になる `olcDatabase={1}hdb,cn=config` が既にできあがっています。アクセス権を定義した `olcDatabase={1}hdb,cn=config` の `olcAccess` の 3行は後で修正します。

```
$ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config dn
dn: cn=config

dn: cn=module{0},cn=config

dn: cn=schema,cn=config

dn: cn={0}core,cn=schema,cn=config

dn: cn={1}cosine,cn=schema,cn=config

dn: cn={2}nis,cn=schema,cn=config

dn: cn={3}inetorgperson,cn=schema,cn=config

dn: olcBackend={0}hdb,cn=config

dn: olcDatabase={-1}frontend,cn=config

dn: olcDatabase={0}config,cn=config

dn: olcDatabase={1}hdb,cn=config

$ sudo slapcat -n 0
dn: cn=config
objectClass: olcGlobal
cn: config
olcArgsFile: /var/run/slapd/slapd.args
olcLogLevel: none
olcPidFile: /var/run/slapd/slapd.pid
olcToolThreads: 1
...
dn: olcDatabase={1}hdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcHdbConfig
olcDatabase: {1}hdb
olcDbDirectory: /var/lib/ldap
olcSuffix: dc=home,dc=michinobu,dc=jp
olcAccess: {0}to attrs=userPassword,shadowLastChange by self write by anonymou
 s auth by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write by * none
olcAccess: {1}to dn.base="" by * read
olcAccess: {2}to * by self write by dn="cn=admin,dc=home,dc=michinobu,dc=jp" w
 rite by * read
olcLastMod: TRUE
olcRootDN: cn=admin,dc=home,dc=michinobu,dc=jp
olcRootPW:: ...
...

$ sudo slapcat -n 1
dn: dc=home,dc=michinobu,dc=jp
objectClass: top
objectClass: dcObject
objectClass: organization
o: home.michinobu.jp
dc: home
structuralObjectClass: organization
...
dn: cn=admin,dc=home,dc=michinobu,dc=jp
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator
userPassword:: ...
structuralObjectClass: organizationalRole
...

$ ldapsearch -x -LLL -H ldap:/// -b dc=home,dc=michinobu,dc=jp dn
dn: dc=home,dc=michinobu,dc=jp

dn: cn=admin,dc=home,dc=michinobu,dc=jp

$ ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=admin,dc=home,dc=michinobu,dc=jp
dn: cn=admin,dc=home,dc=michinobu,dc=jp
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator
```

## スキーマ定義の追加

後で使うかもしれない `misc.ldif` を追加します。

```
$ sudo ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/misc.ldif

$ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config dn
dn: cn=config

dn: cn=module{0},cn=config

dn: cn=schema,cn=config

dn: cn={0}core,cn=schema,cn=config

dn: cn={1}cosine,cn=schema,cn=config

dn: cn={2}nis,cn=schema,cn=config

dn: cn={3}inetorgperson,cn=schema,cn=config

dn: cn={4}misc,cn=schema,cn=config

dn: olcBackend={0}hdb,cn=config

dn: olcDatabase={-1}frontend,cn=config

dn: olcDatabase={0}config,cn=config

dn: olcDatabase={1}hdb,cn=config
```

LDIF 形式ではないスキーマ定義を追加する場合は、少々面倒ですが [https://help.ubuntu.com/10.04/serverguide/openldap-server.html](https://help.ubuntu.com/10.04/serverguide/openldap-server.html) の "Further Configuration" の手順を参考にしてください。

## 基本構造の作成

お約束の `People` と `Groups` を追加します。


```
$ vi base.ldif
dn: ou=People,dc=home,dc=michinobu,dc=jp
objectClass: organizationalUnit
ou: People

dn: ou=Groups,dc=home,dc=michinobu,dc=jp
objectClass: organizationalUnit
ou: Groups

$ ldapadd -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -f base.ldif
Enter LDAP Password:
adding new entry "ou=People,dc=home,dc=michinobu,dc=jp"

adding new entry "ou=Groups,dc=home,dc=michinobu,dc=jp"

$ ldapsearch -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -LLL -b dc=home,dc=michinobu,dc=jp dn
dn: dc=home,dc=michinobu,dc=jp

dn: cn=admin,dc=home,dc=michinobu,dc=jp

dn: ou=People,dc=home,dc=michinobu,dc=jp

dn: ou=Groups,dc=home,dc=michinobu,dc=jp
```

## ユーザの追加

私自身のエントリを追加して結果を見ます。パスワードは後で `ldappasswd` コマンドで設定します。

```
$ vi michinobu.ldif
dn: uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
objectClass: inetOrgPerson
objectClass: posixAccount
uid: michinobu
sn: Maeda
givenName: Michinobu
cn: Michinobu Maeda
displayName: Michinobu Maeda
uidNumber: 1000
gidNumber: 100
loginShell: /bin/bash
homeDirectory: /home/michinobu

$ ldapadd -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -f michinobu.ldif

$ ldapsearch -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -LLL -b uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
Enter LDAP Password:
dn: uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
objectClass: inetOrgPerson
objectClass: posixAccount
uid: michinobu
sn: Maeda
givenName: Michinobu
cn: Michinobu Maeda
displayName: Michinobu Maeda
uidNumber: 1001
gidNumber: 100
loginShell: /bin/bash
homeDirectory: /home/michinobu
userPassword:: ...

$ ldappasswd -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -S uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
```

テスト用のユーザを追加します。

```
$ vi test.ldif
dn: uid=test,ou=People,dc=home,dc=michinobu,dc=jp
objectClass: inetOrgPerson
objectClass: posixAccount
uid: test
sn: Maeda
givenName: Test
cn: Test Maeda
displayName: Test Maeda
uidNumber: 1002
gidNumber: 100
loginShell: /bin/bash
homeDirectory: /home/test

$ ldapadd -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -f test.ldif
```

## アクセス権の変更

各ユーザがどのユーザのパスワードを変更できるか試してみます。

```
$ ldappasswd -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -S uid=test,ou=People,dc=home,dc=michinobu,dc=jp

  --> OK

$ ldappasswd -x -D uid=test,ou=People,dc=home,dc=michinobu,dc=jp -W -S uid=test,ou=People,dc=home,dc=michinobu,dc=jp

  --> OK

$ ldappasswd -x -D uid=test,ou=People,dc=home,dc=michinobu,dc=jp -W -S uid= michinobu,ou=People,dc=home,dc=michinobu,dc=jp

  --> NG
```

Ubuntu のパッケージのデフォルトで、一般的に使える設定になっています。

*   admin は test のパスワードを変更できます。
*   test は test 自身のパスワードを変更できます。
*   test は michinobu のパスワードを変更できません。

前述の `sudo slapcat -n 0` の出力の、アクセス制御の部分を読みやすく改行すると以下のようになります。

```
olcAccess: {0}to attrs=userPassword,shadowLastChange
 by self write
 by anonymous auth
 by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write
 by * none
olcAccess: {1}to dn.base=""
 by * read
olcAccess: {2}to *
 by self write
 by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write
 by * read
```

先ほど試したパスワードが変更する権限があるかどうかなどのことはここで定義されているのですが、参照権限がどうなっているか、実際に動かして試してみます。

```
$ ldapsearch -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -LLL -b uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
...
homeDirectory: /home/michinobu
userPassword:: ...

$ ldapsearch -x -D uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp -W -LLL -b uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
...
homeDirectory: /home/michinobu
userPassword:: ...

$ ldapsearch -x -D uid=test,ou=People,dc=home,dc=michinobu,dc=jp -W -LLL -b uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
...
homeDirectory: /home/michinobu

$ ldapsearch -x -LLL -b uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
...
homeDirectory: /home/michinobu
```

*   admin と自分自身は、パスワードを含めて全て参照することができます。
*   他のユーザはパスワード以外の情報を参照することができます。
*   匿名ユーザはパスワード以外の情報を参照することができます。

[http://www.openldap.org/doc/admin24/access-control.html](http://www.openldap.org/doc/admin24/access-control.html) の "8.3.5. Access Control Examples" を参考に、このアクセス制御の設定を変更します。

まず、匿名ユーザによる参照権限を削除します。

```
$ vi olcAccess.ldif
dn: olcDatabase={1}hdb,cn=config
changetype: modify
delete: olcAccess
-
add: olcAccess
olcAccess: {0}to attrs=userPassword,shadowLastChange by self write by anonymous auth by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write by * none
-
add: olcAccess
olcAccess: {1}to dn.base="" by * read
-
add: olcAccess
olcAccess: {2}to * by self write by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write by anonymous auth by * read

$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f olcAccess.ldif

$ sudo ldapsearch -Y EXTERNAL -H ldapi:/// -LLL -b olcDatabase={1}hdb,cn=config olcAccess
dn: olcDatabase={1}hdb,cn=config
olcAccess: {0}to attrs=userPassword,shadowLastChange by self write by anonymou
 s auth by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write by * none
olcAccess: {1}to dn.base="" by * read
olcAccess: {2}to * by self write by dn="cn=admin,dc=home,dc=michinobu,dc=jp" w
 rite by anonymous auth by * read
```

追加したのは `olcAccess: {2}to * ...` の行の `by anonymous auth` だけです。これで、匿名ユーザは認証を試みることができるけれど、認証に成功しなければ何も参照できない、という設定になります。

次に、 admin 以外のユーザに管理者の権限を与えます。 [http://www.openldap.org/doc/admin24/access-control.html](http://www.openldap.org/doc/admin24/access-control.html) の "8.4.4. Managing access with Groups" で紹介されている手順のうち、直感的にわかりやすい `groupOfNames` による実現方法を使います。

まず `useradmin` グループを作成し、私をメンバーにします。

```
$ vi useradmin.ldif
dn: cn=useradmin,ou=Groups,dc=home,dc=michinobu,dc=jp
cn: Administrators of user accounts
objectclass: groupOfNames
member: uid=michinobu,ou=People,dc=home,dc=michinobu,dc=jp
member: ...

$ ldapadd -x -D cn=admin,dc=home,dc=michinobu,dc=jp -W -f useradmin.ldif
```

次に、`useradmin` グループに任意のユーザのパスワードを変更する権限と、任意のオブジェクトの変更の権限を与えます。

```
$ vi olcAccess.ldif
dn: olcDatabase={1}hdb,cn=config
changetype: modify
delete: olcAccess
-
add: olcAccess
olcAccess: {0}to attrs=userPassword,shadowLastChange by self write by anonymous auth by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write by group.exact="cn=useradmin,ou=Groups,dc=home,dc=michinobu,dc=jp" write by * none
-
add: olcAccess
olcAccess: {1}to dn.base="" by * read
-
add: olcAccess
olcAccess: {2}to * by self write by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write by group.exact="cn=useradmin,ou=Groups,dc=home,dc=michinobu,dc=jp" write by anonymous auth by * read

$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f olcAccess.ldif

$ sudo ldapsearch -Y EXTERNAL -H ldapi:/// -LLL -b olcDatabase={1}hdb,cn=config olcAccess
dn: olcDatabase={1}hdb,cn=config
olcAccess: {0}to attrs=userPassword,shadowLastChange by self write by anonymou
 s auth by dn="cn=admin,dc=home,dc=michinobu,dc=jp" write by group.exact="cn=u
 seradmin,ou=Groups,dc=home,dc=michinobu,dc=jp" write by * none
olcAccess: {1}to dn.base="" by * read
olcAccess: {2}to * by self write by dn="cn=admin,dc=home,dc=michinobu,dc=jp" w
 rite by group.exact="cn=useradmin,ou=Groups,dc=home,dc=michinobu,dc=jp" write
  by anonymous auth by * read
```

これで、私が `test` ユーザのパスワードを変更したり、 `test` ユーザを削除したり、新しいユーザを作成したりできるようになります。

## OSのユーザ認証の設定

次に [https://help.ubuntu.com/community/LDAPClientAuthentication](https://help.ubuntu.com/community/LDAPClientAuthentication) を参考に、LDAP で OS のユーザを認証するよう設定します。

インストールするものはこれだけです。途中でパラメータの入力を求められますが、ドメイン名や管理者以外はデフォルトを受け入れます。

```
$ sudo apt-get install libnss-ldap
```

設定を間違えてやり直す場合は以下のコマンドで。

```
$ sudo dpkg-reconfigure ldap-auth-config
```

LDAPによる認証を有効にします。

```
$ sudo auth-client-config -t nss -p lac_ldap
$ sudo pam-auth-update
```

途中で以下の入力を求められますが、 LDAPが止まると全員ログインできなくなる事態を避けるために、 "Unix authentication" のチェックは外さないでください。

```
[*] Unix authentication
[*] LDAP Authentication
```

たまたま私自身の `gid` が `/etc/passwd` の設定で `1000` になっていたので、ログインし直して `gid` が変わるかどうか確かめてみます。 `/etc/passwd` の設定が優先なので、`gid` は LDAP の設定の `100` にならず `1000` のままです。また、デーモン `slapd` を止めてもログインできます。

test ユーザは LDAP の設定通りにログインできます。

> 追記 : 2012-12-27
>
>
>
> OS の認証をする場合は nscd も入れた方がいいそうです。 [https://help.ubuntu.com/community/LDAPClientAuthentication](https://help.ubuntu.com/community/LDAPClientAuthentication) などご参照ください。
>
> ユーザのホームディレクトリを自動作成するには以下のように。

```
$ sudo vi /usr/share/pam-configs/my_mkhomedir
Name: activate mkhomedir
Default: yes
Priority: 900
Session-Type: Additional
Session:
        required                        pam_mkhomedir.so umask=0022 skel=/etc/skel
$ sudo pam-auth-update
$ sudo /etc/init.d/nscd restart
```
