OpenLDAP でミラーリング
=====

Update: 2012-12-29



OpenLDAP でミラーリングしました。双方向、つまり master-master のレプリケーションです。会社でやったことの復習です。 OS は Ubuntu 12.04 Server です。レプリケーションの通信は TLS で保護します。内容は、記事 [OpenLDAP を Ubuntu 12.04 にインストール](https://sites.google.com/site/michinobumaeda/misc/openldap-ubuntu-12_04-install) と一部重複します。



OpenLDAP Software 2.4 Administrator's Guide [5\. Configuring slapd](http://www.openldap.org/doc/admin24/slapdconf2.html) によると `slapd.conf` は deprecated だということなので、 `ldapadd` や `ldapmodify` などのコマンドを使って動的に設定します。しかしながら [18\. Replication](http://www.openldap.org/doc/admin24/replication.html) の設定例には `slapd.conf` のものが残っています。パッケージのインストールや TLS の設定などについては Ubuntu Server Guide » Network Authentication » [OpenLDAP Server](https://help.ubuntu.com/12.04/serverguide/openldap-server.html) を参考にしました。こちらには Delta-syncrepl の少々たいへんな例が出ていますが、当面私が大規模なディレクトリに関わる予定はないので、 Delta-syncrepl は無しにします。



ホストは 3個です。 u1204s1.michinobu.jp と u1204s2.michinobu.jp をミラーリングします。 u1204s3.michinobu.jp は普通のコンシューマです。

## u1204s1, 2, 3 共通の設定

Ubuntu の slapd のパッケージは、インストール時にホストのドメイン名に従って Base DN を決めます。それで都合が悪い場合は、 slapd のインストール時だけホストのドメイン名を変えるか、 slapd をソースインストールするかしてください。まず、パッケージをインストールして、内容を確認します。


```
$ sudo apt-get install slapd ldap-utils
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

$ ldapsearch -x -LLL -H ldap:/// -b dc=michinobu,dc=jp dn
dn: dc=michinobu,dc=jp

dn: cn=admin,dc=michinobu,dc=jp
```

`cn=admin,dc=michinobu,dc=jp` のパスワードは `test` にしています。この後の操作やレプリケーションの設定で必要になります。



次に、使うかもしれないスキーマ `misc.ldif` を追加します。



```
$ sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/misc.ldif
```


ログ出力のレベルを設定します。後の TLS の動作の確認で必要になります。ただし、このままにしておくと膨大なログを出力してしまうので、本番環境などでは元に戻しておいてください。


```
$ vi logging.ldif
dn: cn=config
changetype: modify
add: olcLogLevel
olcLogLevel: stats

$ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f logging.ldif
```

どんな構成になるとしてもまちがいなく必要になるインデックスを追加します。


```
$ vi uid_index.ldif
dn: olcDatabase={1}hdb,cn=config
add: olcDbIndex
olcDbIndex: uid eq,pres,sub

$ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f uid_index.ldif

$ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config '(olcDatabase={1}hdb)' olcDbIndex
dn: olcDatabase={1}hdb,cn=config
olcDbIndex: objectClass eq
olcDbIndex: uid eq,pres,sub
```

## u1204s1 にテスト用のデータを登録

まず、お約束の `ou=People` と `ou=Groups` を追加します。


```
$ vi base.ldif
dn: ou=People,dc=michinobu,dc=jp
objectClass: organizationalUnit
ou: People

dn: ou=Groups,dc=michinobu,dc=jp
objectClass: organizationalUnit
ou: Groups

$ ldapadd -x -D cn=admin,dc=michinobu,dc=jp -W -f base.ldif
```

テスト用のユーザ test1, test2, test3 を追加します。


```
$ vi users.ldif
dn: uid=test1,ou=People,dc=michinobu,dc=jp
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: test1
sn: Myouji
givenName: Test1
cn: Test1 Myouji
displayName: Test1 Myouji
uidNumber: 1000
gidNumber: 100
userPassword: test1
loginShell: /bin/bash
homeDirectory: /home/test1
mail: test1@michinobu.jp

dn: uid=test2,ou=People,dc=michinobu,dc=jp
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: test2
sn: Myouji
givenName: test2
cn: Test2 Myouji
displayName: Test2 Myouji
uidNumber: 1001
gidNumber: 100
userPassword: test2
loginShell: /bin/bash
homeDirectory: /home/test2
mail: test2@michinobu.jp

dn: uid=test3,ou=People,dc=michinobu,dc=jp
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: test3
sn: Myouji
givenName: test3
cn: Test3 Myouji
displayName: Test3 Myouji
uidNumber: 1002
gidNumber: 100
userPassword: test3
loginShell: /bin/bash
homeDirectory: /home/test3
mail: test3@michinobu.jp

$ ldapadd -x -D cn=admin,dc=michinobu,dc=jp -W -f users.ldif
```

## u1204s1 にミラーリングの設定

[18\. Replication](http://www.openldap.org/doc/admin24/replication.html) の `slapd.conf` 向けの設定例を書き直すと、こうなるようです。 Ntp による時刻の同期は必須のようです。レプリケーションのタイプは `refreshAndPersist` にしています。 `refreshOnly` が可能かどうかはよくわかりません。可能だとしてもタイムスタンプ比較で「後の人が勝ち」しかできないだろうと思います。 `binddn` に `cn=admin,dc=michinobu,dc=jp` を使っていますが、本番環境ではセキュリティのために、レプリケーションのためのユーザを作った方がいいと思います。


```
$ vi mirror1.ldif
dn: cn=config
changetype: modify
replace: olcServerID
olcServerID: 1

dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: syncprov

dn: olcDatabase={1}hdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: entryCSN eq
-
add: olcDbIndex
olcDbIndex: entryUUID eq
-
add: olcSyncRepl
olcSyncRepl: rid=001 provider=ldap://u1204s2.michinobu.jp
  bindmethod=simple binddn="cn=admin,dc=michinobu,dc=jp" credentials=test
  searchbase="dc=michinobu,dc=jp" schemachecking=on
  type=refreshAndPersist retry="60 +"
-
add: olcMirrorMode
olcMirrorMode: TRUE

dn: olcOverlay=syncprov,olcDatabase={1}hdb,cn=config
changetype: add
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: syncprov

$ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f mirror1.ldif
```

## u1204s2 にミラーリングの設定

u1204s1 とは `olcServerID` や `provider` が異なります。 `rid` は同じです。


```
$ vi mirror2.ldif
dn: cn=config
changetype: modify
replace: olcServerID
olcServerID: 2

dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: syncprov

dn: olcDatabase={1}hdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: entryCSN eq
-
add: olcDbIndex
olcDbIndex: entryUUID eq
-
add: olcSyncRepl
olcSyncRepl: rid=001 provider=ldap://u1204s1.michinobu.jp
  bindmethod=simple binddn="cn=admin,dc=michinobu,dc=jp" credentials=test
  searchbase="dc=michinobu,dc=jp" schemachecking=on
  type=refreshAndPersist retry="60 +"
-
add: olcMirrorMode
olcMirrorMode: TRUE

dn: olcOverlay=syncprov,olcDatabase={1}hdb,cn=config
changetype: add
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: syncprov

$ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f mirror2.ldif
```

## ミラーリングの動作確認

[OpenLDAP Server](https://help.ubuntu.com/12.04/serverguide/openldap-server.html) では



```
$ ldapsearch -z1 -LLLQY EXTERNAL -H ldapi:/// -s base contextCSN
```


で `contextCSN` を参照しているのですがうまくいきません。



```
$ ldapsearch -z1 -LLLQY EXTERNAL -H ldapi:/// -b dc=michinobu,dc=jp contextCSN
```

で u1204s1 の `contextCSN` を確認します。まだ空です。 `uid=test3` の `displayName` を変更してミラーリングの動作を確認します。現在の内容を確認します。


```
$ ldapsearch -x -LLL -b dc=michinobu,dc=jp 'uid=test3' cn displayName
dn: uid=test3,ou=People,dc=michinobu,dc=jp
cn: Test3 Myouji
displayName: Test3 Myouji
```

u1204s1 で値を変更します。


```
$ vi mirror_test_1.ldif
dn: uid=test3,ou=People,dc=michinobu,dc=jp
changetype: modify
replace: displayName
displayName: test3 Myouji

$ ldapmodify -x -D cn=admin,dc=michinobu,dc=jp -W -f mirror_test_1.ldif
```

`contextCSN` と `displayName` を確認します。


```
$ ldapsearch -z1 -LLLQY EXTERNAL -H ldapi:/// -b dc=michinobu,dc=jp contextCSN
contextCSN: 20121228155627.848349Z#000000#001#000000
...
$ ldapsearch -x -LLL -b dc=michinobu,dc=jp 'uid=test3' cn displayName
…
displayName: test3 Myouji
```

u1204s2 で確認します。


```
$ ldapsearch -z1 -LLLQY EXTERNAL -H ldapi:/// -b dc=michinobu,dc=jp contextCSN
contextCSN: 20121228155627.848349Z#000000#001#000000
...
$ ldapsearch -x -LLL -b dc=michinobu,dc=jp 'uid=test3' cn displayName
...
displayName: test3 Myouji
```

u1204s2 で値を変更します。


```
$ vi mirror_test_2.ldif
dn: uid=test3,ou=People,dc=michinobu,dc=jp
changetype: modify
replace: displayName
displayName: Test3 Myouji
$ ldapmodify -x -D cn=admin,dc=michinobu,dc=jp -W -f mirror_test_2.ldif
```

`contextCSN` と `displayName` を確認します。 `contextCSN` は 2行になります。


```
$ ldapsearch -z1 -LLLQY EXTERNAL -H ldapi:/// -b dc=michinobu,dc=jp contextCSN
contextCSN: 20121228155627.848349Z#000000#001#000000
contextCSN: 20121228155704.214920Z#000000#002#000000
...
$ ldapsearch -x -LLL -b dc=michinobu,dc=jp 'uid=test3' cn displayName
...
displayName: Test3 Myouji
```

u1204s1 で確認します。


```
$ ldapsearch -z1 -LLLQY EXTERNAL -H ldapi:/// -b dc=michinobu,dc=jp contextCSN
contextCSN: 20121228155627.848349Z#000000#001#000000
contextCSN: 20121228155704.214920Z#000000#002#000000
...
$ ldapsearch -x -LLL -b dc=michinobu,dc=jp 'uid=test3' cn displayName
...
displayName: Test3 Myouji
```

## ミラーの TLS の設定

[OpenLDAP Server](https://help.ubuntu.com/12.04/serverguide/openldap-server.html) の "TLS" の内容そのままです。



u1204s1

```
$ sudo apt-get install gnutls-bin ssl-cert
$ sudo sh -c "certtool --generate-privkey > /etc/ssl/private/cakey.pem"
$ sudo vi /etc/ssl/ca.info
cn = michinobu.jp at Home
ca
cert_signing_key

$ sudo certtool --generate-self-signed \
--load-privkey /etc/ssl/private/cakey.pem \
--template /etc/ssl/ca.info \
--outfile /etc/ssl/certs/cacert.pem

$ sudo certtool --generate-privkey \
--bits 1024 \
--outfile /etc/ssl/private/u1204s1_slapd_key.pem

$ sudo vi /etc/ssl/u1204s1.info
organization = michinobu.jp at Home
cn = u1204s1.michinobu.jp
tls_www_server
encryption_key
signing_key
expiration_days = 3650

$ sudo certtool --generate-certificate \
--load-privkey /etc/ssl/private/u1204s1_slapd_key.pem \
--load-ca-certificate /etc/ssl/certs/cacert.pem \
--load-ca-privkey /etc/ssl/private/cakey.pem \
--template /etc/ssl/u1204s1.info \
--outfile /etc/ssl/certs/u1204s1_slapd_cert.pem


$ sudo vi /etc/ssl/certinfo.ldif
dn: cn=config
add: olcTLSCACertificateFile
olcTLSCACertificateFile: /etc/ssl/certs/cacert.pem
-
add: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ssl/certs/u1204s1_slapd_cert.pem
-
add: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ssl/private/u1204s1_slapd_key.pem
$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f /etc/ssl/certinfo.ldif
$ sudo adduser openldap ssl-cert
$ sudo chgrp ssl-cert /etc/ssl/private/u1204s1_slapd_key.pem
$ sudo chmod g+r /etc/ssl/private/u1204s1_slapd_key.pem
$ sudo chmod o-r /etc/ssl/private/u1204s1_slapd_key.pem
$ sudo service slapd restart

$ mkdir u1204s2-ssl
$ cd u1204s2-ssl
$ sudo certtool --generate-privkey \
--bits 1024 \
--outfile u1204s2_slapd_key.pem

$ vi u1204s2.info
organization = michinobu.jp at Home
cn = u1204s2.michinobu.jp
tls_www_server
encryption_key
signing_key
expiration_days = 3650

$ sudo certtool --generate-certificate \
--load-privkey u1204s2_slapd_key.pem \
--load-ca-certificate /etc/ssl/certs/cacert.pem \
--load-ca-privkey /etc/ssl/private/cakey.pem \
--template u1204s2.info \
--outfile u1204s2_slapd_cert.pem

$ cp /etc/ssl/certs/cacert.pem .
$ cd ..
$ sudo tar czvf u1204s2-ssl.tar.gz u1204s2-ssl
$ scp u1204s2-ssl.tar.gz u1204s2.michinobu.jp:~/
```

u1204s2

```
$ sudo apt-get install gnutls-bin ssl-cert
$ tar xzvf u1204s2-ssl.tar.gz
$ cd u1204s2-ssl
$ sudo adduser openldap ssl-cert
$ sudo cp u1204s2_slapd_cert.pem cacert.pem /etc/ssl/certs
$ sudo cp u1204s2_slapd_key.pem /etc/ssl/private
$ sudo chgrp ssl-cert /etc/ssl/private/u1204s2_slapd_key.pem
$ sudo chmod g+r /etc/ssl/private/u1204s2_slapd_key.pem
$ sudo chmod o-r /etc/ssl/private/u1204s2_slapd_key.pem
$ sudo vi /etc/ssl/certinfo.ldif
dn: cn=config
add: olcTLSCACertificateFile
olcTLSCACertificateFile: /etc/ssl/certs/cacert.pem
-
add: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ssl/certs/u1204s2_slapd_cert.pem
-
add: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ssl/private/u1204s2_slapd_key.pem

$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f /etc/ssl/certinfo.ldif
```

u1204s1

```
$ vi mirror1_tls.ldif
dn: olcDatabase={1}hdb,cn=config
changetype: modify
replace: olcSyncRepl
olcSyncRepl: rid=001 provider=ldap://u1204s2.michinobu.jp
  bindmethod=simple binddn="cn=admin,dc=michinobu,dc=jp" credentials=test
  searchbase="dc=michinobu,dc=jp" schemachecking=on
  type=refreshAndPersist retry="60 +"
  starttls=critical tls_reqcert=demand

$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f mirror1_tls.ldif
$ sudo service slapd restart
```

u1204s2

```
$ vi mirror2_tls.ldif
dn: olcDatabase={1}hdb,cn=config
changetype: modify
replace: olcSyncRepl
olcSyncRepl: rid=001 provider=ldap://u1204s1.michinobu.jp
  bindmethod=simple binddn="cn=admin,dc=michinobu,dc=jp" credentials=test
  searchbase="dc=michinobu,dc=jp" schemachecking=on
  type=refreshAndPersist retry="60 +"
  starttls=critical tls_reqcert=demand

$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f mirror2_tls.ldif
$ sudo service slapd restart
```

ミラーリングの動作確認と同様に u1204s1 と u1204s2 の両方で値を変更し、ログに `STARTTLS` が出ていることを確認します。


```
$ sudo tail -100 /var/log/syslog
…
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 fd=13 ACCEPT from IP=192.168.93.102:54158 (IP=0.0.0.0:389)
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 op=0 EXT oid=1.3.6.1.4.1.1466.20037
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 op=0 STARTTLS
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 op=0 RESULT oid= err=0 text=
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 fd=13 TLS established tls_ssf=128 ssf=128
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 op=1 BIND dn="cn=admin,dc=michinobu,dc=jp" method=128
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 op=1 BIND dn="cn=admin,dc=michinobu,dc=jp" mech=SIMPLE ssf=0
Dec 29 01:13:15 u1204s1 slapd[6012]: conn=1000 op=1 RESULT tag=97 err=0 text=
…
```

## コンシューマの設定

u1204s3 を u1204s2 のコンシューマにします。テストが楽なのでレプリケーションのタイプは `refreshAndPersist` にしますが、本番環境では要件に合うものを選択した方がいいです。小規模なディレクトリであれば日毎や時間毎の更新でも十分でしょう。


```
$ vi consumer.ldif
dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: syncprov

dn: olcDatabase={1}hdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: entryCSN eq
-
add: olcDbIndex
olcDbIndex: entryUUID eq
-
add: olcSyncRepl
olcSyncRepl: rid=003 provider=ldap://u1204s2.michinobu.jp
  bindmethod=simple binddn="cn=admin,dc=michinobu,dc=jp" credentials=test
  searchbase="dc=michinobu,dc=jp" filter="(objectClass=*)" scope=sub
  type=refreshAndPersist retry="60 +"

$ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f consumer.ldif
```

設定すると、すぐにレプリケーションされます。


```
$ ldapsearch -x -LLL -b dc=michinobu,dc=jp dn
dn: dc=michinobu,dc=jp
dn: cn=admin,dc=michinobu,dc=jp
dn: ou=People,dc=michinobu,dc=jp
dn: ou=Groups,dc=michinobu,dc=jp
dn: uid=test1,ou=People,dc=michinobu,dc=jp
dn: uid=test2,ou=People,dc=michinobu,dc=jp
dn: uid=test3,ou=People,dc=michinobu,dc=jp
```

u1204s1 で値を変更します。



```
$ ldapmodify -x -D cn=admin,dc=michinobu,dc=jp -W -f mirror_test_1.ldif
```

直ちに変更内容が u1204s2 経由で u1204s3 に到達するはずです。



```
$ ldapsearch -x -LLL -b dc=michinobu,dc=jp 'uid=test3' cn displayName
```

## コンシューマの TLS の設定

ミラーの TLS の設定と同様です。



u1204s1

```
$ mkdir u1204s3-ssl
$ cd u1204s3-ssl
$ sudo certtool --generate-privkey \
--bits 1024 \
--outfile u1204s3_slapd_key.pem

$ vi u1204s3.info
organization = michinobu.jp at Home
cn = u1204s3.michinobu.jp
tls_www_server
encryption_key
signing_key
expiration_days = 3650

$ sudo certtool --generate-certificate \
--load-privkey u1204s3_slapd_key.pem \
--load-ca-certificate /etc/ssl/certs/cacert.pem \
--load-ca-privkey /etc/ssl/private/cakey.pem \
--template u1204s3.info \
--outfile u1204s3_slapd_cert.pem

$ cp /etc/ssl/certs/cacert.pem .
$ cd ..
$ sudo tar czvf u1204s3-ssl.tar.gz u1204s3-ssl
$ scp u1204s3-ssl.tar.gz u1204s3.michinobu.jp:~/
```

u1204s3

```
$ sudo apt-get install gnutls-bin ssl-cert
$ tar xzvf u1204s3-ssl.tar.gz
$ cd u1204s3-ssl
$ sudo adduser openldap ssl-cert
$ sudo cp u1204s3_slapd_cert.pem cacert.pem /etc/ssl/certs
$ sudo cp u1204s3_slapd_key.pem /etc/ssl/private
$ sudo chgrp ssl-cert /etc/ssl/private/u1204s3_slapd_key.pem
$ sudo chmod g+r /etc/ssl/private/u1204s3_slapd_key.pem
$ sudo chmod o-r /etc/ssl/private/u1204s3_slapd_key.pem
$ sudo vi /etc/ssl/certinfo.ldif
dn: cn=config
add: olcTLSCACertificateFile
olcTLSCACertificateFile: /etc/ssl/certs/cacert.pem
-
add: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ssl/certs/u1204s3_slapd_cert.pem
-
add: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ssl/private/u1204s3_slapd_key.pem

$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f /etc/ssl/certinfo.ldif
$ vi mirror3_tls.ldif
dn: olcDatabase={1}hdb,cn=config
changetype: modify
replace: olcSyncRepl
olcSyncRepl: rid=003 provider=ldap://u1204s2.michinobu.jp
  indmethod=simple binddn="cn=admin,dc=michinobu,dc=jp" credentials=test
  earchbase="dc=michinobu,dc=jp" filter="(objectClass=*)" scope=sub
  ype=refreshAndPersist retry="60 +"
  tarttls=critical tls_reqcert=demand

$ sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f mirror3_tls.ldif
$ sudo service slapd restart
```

u1204s3 でログに `STARTTLS` が出力されていることを確認します。


```
$ sudo tail -100f /var/log/syslog
...
Dec 29 15:49:08 u1204s2 slapd[1111]: conn=1002 op=0 EXT oid=1.3.6.1.4.1.1466.20037
Dec 29 15:49:08 u1204s2 slapd[1111]: conn=1002 op=0 STARTTLS
Dec 29 15:49:08 u1204s2 slapd[1111]: conn=1002 op=0 RESULT oid= err=0 text=
Dec 29 15:49:08 u1204s2 slapd[1111]: conn=1002 fd=18 ACCEPT from IP=192.168.93.103:47820 (IP=0.0.0.0:389)
Dec 29 15:49:08 u1204s2 slapd[1111]: conn=1002 fd=18 TLS established tls_ssf=128 ssf=128
...
```
