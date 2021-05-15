玄箱Proのリカバリ
=====

Update: 2009-08-03



同じ構成の玄箱Pro 2台をファイルサーバにして `rsync` で毎晩同期して使っていたのですが、片方が動かなくなってしまいました。数日前から、ときどき「パキンパキンパキン」という、やぁな音がしていたのですが、うんともすんともいわなくなってしまいました。 HDD が壊れています。とっかえなけれればならないのですが、PCのように「 CD つっこんで OS 再インストール」というわけにはいきません。CD-ROM もディスプレイもついていないですからね。 CD-ROM もディスプレイも無い代わりに、自作したシリアルのレベル変換器をつないでターミナルから接続することができます。フラッシュメモリは問題ないようで、何かしら起動します。こんな表示が



```
Hit any key to stop autoboot: 2
```



出たところでキーを押すと、こんな



```
Marvell>>
```



プロンプトになります。その話の前に、キーを押さずに放置した場合は TFTP 経由でブートイメージを読み込もうとしているらしい表示が出てきます。そうではなくてフラッシュメモリに出荷時から入っているイメージでブートしたいわけですが、 [フラッシュメモリからブートするには](http://www.yamasita.jp/linkstation/kuro-box_pro/tips/uboot/post_5.html) にしたがって次のコマンドを入力します。



```
Marvell>> setenv bootargs_root root=/dev/mtdblock2 rw panic=5
Marvell>> setenv bootcmd 'nboot $(default_kernel_addr) 0 ↓
 $(nand_uImage_offset);bootm $(default_kernel_addr)'
Marvell>> setenv nand_boot yes
Marvell>> setenv bootargs $(bootargs_base) $(bootargs_root) $(buffalo_ver)
Marvell>> boot`
```


待つこと数十秒、爆笑なアスキーアートを表示しつつ起動が完了します。



DHCP で固定の IP アドレスを割り当てているので IP アドレスは同じ、 Samba も OK ということで「玄箱Proで遊ぼう!!」ISBN978-4-89977-202-6 の「\[第3部\] 応用編 2 Debian のインストール」の手順に従って OS を再インストールします。



あとは諸々のパッケージを入れて、データを生きていた片方からコピーして、終わり。
