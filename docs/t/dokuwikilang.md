# DokuWikiの「サイドバー」を変更

Update: 2021-01-02


dokuwikimyuserstyle に追加で以下のようなカスタマイズをしました。

## スマホ表示の「サイドバー」を「メニュー」に変更

スマホではサイドバーが折り畳まれて「サイドバー」というボタンになります。
これを「メニュー」に変更します。
``conf/lang/ja/lang.php`` が無ければ（たぶん無い）追加して以下のように。

```php
<?php
$lang['sidebar']               = 'メニュー';
```

## 外部リンクのアイコンを削除

[How to "completely" remove external link icons?](https://forum.dokuwiki.org/d/17349-solved-how-to-completely-remove-external-link-icons)
より、 ``conf/userstyle.css`` に設定を追加します。

```css
.dokuwiki a.urlextern,
.dokuwiki a.interwiki,
.dokuwiki a.windows,
.dokuwiki a.mail {
    background-image: none !important;
    padding-left: 0 !important;
}
```

Tag: dokuwiki
