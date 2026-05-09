+++
title = "MUI の DataGrid の \"Rows per page\" をローカライズする"
date = 2021-11-23T00:00:00+09:00
categories = ["tech"]
tags = ["nodejs", "react", "mui"]
+++

[MUI](https://mui.com/) の ``DataGrid`` のフッタに表示される "Rows per page" を日本語にしようとしたのですが、
<https://github.com/mui-org/material-ui-x/blob/HEAD/packages/grid/_modules_/grid/constants/localeTextConstants.ts>
には無いようです。

[とりあえずの回避策](https://github.com/mui-org/material-ui-x/issues/1854#issuecomment-856885588)
はうまくいきました。

私の場合、こんな感じで。
``t('Rows per page')`` のところはローカライズの仕組みに合わせて。

```
<DataGrid
  componentsProps={ {
    pagination: {
      labelRowsPerPage: t('Rows per page')
    }
  }}
/>
```
