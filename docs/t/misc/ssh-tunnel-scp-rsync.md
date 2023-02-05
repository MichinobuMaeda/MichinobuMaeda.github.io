# ssh tunnel で scp と rsync

Update: 2016-07-29

local ( Mac ) -- remote1 -- remote2 で scp と rsync する手順、Stack Overflow で見つけました。



まず、簡単な方、 rsync は



rsync through ssh tunnel

[http://stackoverflow.com/questions/16654751/rsync-through-ssh-tunnel](http://stackoverflow.com/questions/16654751/rsync-through-ssh-tunnel)



の 20 がよいです。



```
rsync -av -e "ssh -A user1@remote1 ssh" ./src user2@remote2:/dst
```



scp については



How to scp with a second remote host

[http://stackoverflow.com/questions/9139417/how-to-scp-with-a-second-remote-host](http://stackoverflow.com/questions/9139417/how-to-scp-with-a-second-remote-host)



に一般的な ssh tunnel の手順も載っているのですが、よく使う経路の場合 17 のオプションの設定を `~/.ssh/config` に入れておくのが楽です。以下のような感じで。

```
Host remote2
    User user2
    ProxyCommand ssh user1@remote1 nc %h %p
```



remote1 に nc が入ってなければ入れてください。ところで、これは ssh tunnel とは違うものになるのかな？ ま、動けばいいです ^^;
