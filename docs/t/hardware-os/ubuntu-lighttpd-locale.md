# Ubuntu で lighttpd 再起動すると locale が設定されてないと...

Update: 2012-01-26



Ubuntu に Lighttpd をインストールしたのですが、再起動するとこんなメッセージが出てきました。


```
$ sudo service lighttpd restart
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
LANGUAGE = (unset),
LC_ALL = (unset),
LANG = "ja_JP.UTF-8"
 are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
perl: warning: Setting locale failed.
...
```

再起動はできているのでほっとこうかと思ったのですが警告など出ないに越したことはないので、調べてみました。掲示板の投稿を見つけましたが [perl: warning: Setting locale failed.](http://ubuntuforums.org/showthread.php?t=1346581) 英語環境でも出るのですね。私のところではこんな感じで


```
$ sudo locale-gen ja_JP ja_JP.UTF-8
Generating locales...
 ja_JP.UTF-8... done
Generation complete.
$ sudo dpkg-reconfigure locales
Generating locales...
 en_AG.UTF-8... done
 en_AU.UTF-8... done
 en_BW.UTF-8... done
 en_CA.UTF-8... done
 en_DK.UTF-8... done
 en_GB.UTF-8... done
 en_HK.UTF-8... done
 en_IE.UTF-8... done
 en_IN.UTF-8... done
 en_NG.UTF-8... done
 en_NZ.UTF-8... done
 en_PH.UTF-8... done
 en_SG.UTF-8... done
 en_US.UTF-8... done
 en_ZA.UTF-8... done
 en_ZM.UTF-8... done
 en_ZW.UTF-8... done
 ja_JP.UTF-8... up-to-date
Generation complete.
```

この後 lighttpd を再起動してみると、警告は出なくなっていました。
