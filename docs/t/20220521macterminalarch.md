+++
title = "Mac の Zsh のプロンプトに CPU アーキテクチャを表示する"
date = 2022-05-21T00:00:00+09:00
categories = ["tech"]
tags = ["macos", "zsh"]
+++

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
