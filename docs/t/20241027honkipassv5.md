# 本気でパスワード v5

Update: 2024-10-27

追記 2025-11-29: React による実装に変更 <https://pages.michinobu.jp/honkipass5>

[Svelte 用の Material 3 風のコンポーネント](20241025md3components.html) を使って「本気でパスワード v5」を作りました。
Flutter で作った [v4](https://github.com/MichinobuMaeda/honkipass) は起動が遅く、単機能に対してさすがに不釣り合いでした。

バックエンドは無しで、サーバ等との通信は UI のアップデートの有無の確認だけです。スマホでは PWA となるはずですが iOS ではテストしていません。

ソース: <https://github.com/MichinobuMaeda/honkipass5>

~~実物: <https://honkipass.michinobu.jp/>~~

<img src="20241027honkipassv5.png" alt="本気でパスワード v5" style="width:320px;"/>

Tag: tailwind material
