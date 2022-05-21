# Mac の Zsh のプロプトに CPU アーキテクチャを表示する

Update: 2022-05-21

M1 の Mac を使い始めてからしばらく「 Rosetta を使用して開く」を On にした Terminal を使って、 VS code や Homebrew も Intel の方を入れていました。でも、もうそろそろ Arm でいいかな、と、切り替えの作業を始めたところでさっそく「今、どっちの状態なのかわからん。 `arch` コマンドを打てばわかるけど、、、」と困ることになりました。 Oh My Zsh のカスタマイズでプロンプトに Git のブランチを表示できるんだから同じようにできるだろうと試してみてうまくいったのがこれです。

`.zshrc`

```
if [ "$(arch)" = "arm64" ]; then
    export PROMPT='A %~ ${vcs_info_msg_0_}$ '
else
    export PROMPT='I %~ ${vcs_info_msg_0_}$ '
fi
```

`arm64` なら `A ~ $ ` 、 `i368` なら `I ~ $ ` のように表示します。

Tag: macos zsh
