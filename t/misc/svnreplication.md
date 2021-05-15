Subversion のレプリケート
=====

Update: 2010-12-05



Google Code に置いた Subversion のリポジトリを他のサーバに複製することはできないかな？と思ってやってみました。複製先は自宅の Linux 機です。



資料はこちら [Version Control with Subversion (for Subversion 1.5) - Repository Replication](http://svnbook.red-bean.com/en/1.5/svn.reposadmin.maint.html#svn.reposadmin.maint.replication)



複製先のリポジトリを作ります。



```
# svnadmin create /home/backup/zippyzipjp/mirror
```


hook script を作ります。



```
$ cat mirror/hooks/pre-revprop-change
#!/bin/sh

USER="$3"

if [ "$USER" = "syncuser" ]; then exit 0; fi

echo "Only the syncuser user may change revision properties" >&2
exit 1
$ chmod +x mirror/hooks/pre-revprop-change

$ cat mirror/hooks/start-commit
#!/bin/sh`

USER="$2"

if [ "$USER" = "syncuser" ]; then exit 0; fi


echo "Only the syncuser user may commit new revisions" >&2
exit 1
$ chmod +x mirror/hooks/start-commit`
```

svnsync で初期化します。


```
svnsync initialize file:///home/backup/zippyzipjp/mirror \
 http://****.googlecode.com/svn/ \
 --sync-username syncuser --sync-password ******
```

複製を実行します。



```
svnsync synchronize file:///home/backup/zippyzipjp/mirror
```


以上
