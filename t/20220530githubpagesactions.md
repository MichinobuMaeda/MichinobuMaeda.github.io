# GitHub Pages で Actons を使う

Update: 2022-05-30

GitHub Pages に `push` する前に手元で目次ページを生成していたのを GitHub Actions で処理するようにしてみました。これで PC がなくても GitHub で直接ページを追加編集できるようになります。

```
name: Generate indexes
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Detect ruby version
      id: ruby-version
      run: echo "::set-output name=VERSION::$(cat .ruby-version)"
    - name: Setup ruby
      uses: ruby/setup-ruby@v1
      with:
        ruby-version: '${{ steps.ruby-version.outputs.VERSION }}'
    - name: Generate indexes
      run: ruby mkindex.rb
    - name: Commit generated indexes
      uses: EndBug/add-and-commit@v7
      with:
        default_author: github_actions
```

Ruby のバージョンの設定は
[GitHub Actions で言語のバージョンをファイルから読み出す](https://zenn.dev/rosylilly/articles/202202-github-actions-versions)
を参考にしましt。他の言語でもだいたい同様にできそうです。

Git の `add`, `commit`, `push` には
[Add & Commit](https://github.com/EndBug/add-and-commit)
を使いました。
`git` コマンドでもできるかなと思ったけれど、差分無しで空振りする場合の対応などが面倒ですね。便利なものを使わせていただくことにします。

Tag: github actions
