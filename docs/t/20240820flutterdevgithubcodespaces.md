# GitHub Codespaces で Firebase & Flutter の開発

Update: 2024-08-20

## やりたかったこと

バックエンドが Firebase でフロントエンドが Flutter (Web) の開発を趣味でほそぼそとやっているのですけれど、これを
GitHub Codespaces でできないかなと思いついたのはずいぶん前のことです。なぜすぐに実行に移さなかったのかというと、まず
Emulator の設定がたいへんそうだからです。クラウド側で Web サーバーを起動してその上の
SPA をローカルのブラウザで表示するところまではたぶん簡単なのですが、
SPA が利用する Firebase Emulator の各サービスのポートをすべて Forward しなければなりません。

それから Functions の言語として Python
を選んでしまったこともあり、たくさんの言語の環境をインストールする必要があります。なぜ
Python にしたのかというと、使ってみたかったから。

でも、半日ほど気合を入れて試してみるとできました。以下、その手順です。

## 使用した環境

M2 MabBook 上の Chrome で試しました。後述の
`gh` コマンドが使える環境なら Windows や Linux はもちろん Chromebook や
Termius を入れた Android タブレットでもなんとかなると思います。

## コンテナの設定

コンテナのベースは ruby にしました。
Ruby を使っていないのになぜそうしたのかというと Homebrew を入れるためです。
Homebrew を入れる理由は Linux 上でもこれが楽だから。実際、下記の `Dockerfile`
の最終行のように実質 1 or 2行で済みます。

`.devcontainer/Dockerfile`

```Dockerfile
FROM ruby

RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
RUN (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /root/.bashrc
RUN eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" && brew tap leoafarias/fvm && brew install fvm nvm pyenv openjdk ruff
```

Homebrew のインストール手順は <https://docs.brew.sh/Installation> で最新の内容を確認してください。

現在は Flutter SDK のアップデートが激しいので fvm を使っています。

## ポートの設定（コンテナ側）

Emulator UI のポートはデフォルト可変なので、下記のように指定します。

`firebase.json`

```JSON
    "ui": {
      "enabled": true,
      "port": 4040
    },
```

ポートの穴あけは `devcontainer.json` に記載します。
`firebase.json` の設定内容に合わせてとにかく全部設定します。
VS Code で使っている拡張もここですべて設定しておくといいです。
`"name"` をサンプルをコピーしたまま `"Flutter"` としてしまったのにいまごろになって気がついたのですが、とりたてて不都合はなさそうです。

ポート 3000 については後述します。

`.devcontainer/devcontainer.json`

```JSON
{
  "build": {
    "dockerfile": "Dockerfile"
  },
  "forwardPorts": [
    3000,
    4040,
    9099,
    5001,
    8080,
    8085,
    9199
  ],
  "name": "Flutter",
  "customizations": {
    "vscode": {
      "extensions": [
        "bierner.markdown-mermaid",
        "charliermarsh.ruff",
        "dart-code.dart-code",
        "dart-code.flutter",
        "davidanson.vscode-markdownlint",
        "dbaeumer.vscode-eslint",
        "donjayamanne.python-environment-manager",
        "donjayamanne.python-extension-pack",
        "editorconfig.editorconfig",
        "gaetschwartz.build-runner",
        "google.arb-editor",
        "ms-ceintl.vscode-language-pack-ja",
        "ms-python.debugpy",
        "ms-python.python",
        "ms-python.vscode-pylance",
        "redhat.vscode-yaml",
        "robert-brunhage.flutter-riverpod-snippets",
        "streetsidesoftware.code-spell-checker"
      ]
    }
  }
}
```

## コンテナ起動後の最初の設定

上記の2ファイルをリポジトリの `main` に push して Codespaces の Web版 VS Code
を開くとコンテナの構築が始まります。構築中のコンソール出力を参照できるので、エラーがないか確認します。構築後にログを参照することもできます。

このあたりの操作は Web版 VS Code の下端などを見ているとなんとなくわかるかと思います。不明な場合は Codespaces のドキュメントをご参照ください。

`.bashrc` に設定の追加が必要です。正確な設定内容はコンテナ構築のログや
`pyenv init` の出力内容を参照してください。

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "/home/linuxbrew/.linuxbrew/opt/nvm/nvm.sh" ] && \. "/home/linuxbrew/.linuxbrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/home/linuxbrew/.linuxbrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/home/linuxbrew/.linuxbrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

これらの設定をしたら、ターミナルを開き直してください。

それぞれの言語やパッケージをせっせと入れます。私の場合こんな感じ ...

```bash
nvm install
fvm use
pyenv install
pyenv init
npm i
fvm flutter pub get
cd functions
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

入れたはずのコマンド等が動いてくれない場合は、ターミナルを開き直すとうまくいくかもしれません。

ここまででコンテナの初期構築は完了です。

Flutter SDK のバージョンアップなどの対応は、ここまでできる人はわかりますよね。ローカルで開発する場合と同じです。

## ローカルの設定

`gh` を使ったことない人は <https://cli.github.com/> から入手してください。最初にログインが必要です。

`gh` コマンドでまずコンテナの名称を取得します。

```bash
$ gh cs list
NAME                             DISPLAY NAME    ...
nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn  ddddddddddddddd ...
```

その名称を使って、必要なポートをすべて `localhost` につなぎます。

```bash
export CODESPACE_NAME=nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
gh cs ports forward 3000:3000 -c $CODESPACE_NAME &
gh cs ports forward 4040:4040 -c $CODESPACE_NAME &
gh cs ports forward 5001:5001 -c $CODESPACE_NAME &
gh cs ports forward 8080:8080 -c $CODESPACE_NAME &
gh cs ports forward 8085:8085 -c $CODESPACE_NAME &
gh cs ports forward 9099:9099 -c $CODESPACE_NAME &
gh cs ports forward 9199:9199 -c $CODESPACE_NAME &
```

## flutter run コマンドのデバイスID

Codespaces のコンテナから Chrome の起動はできないので、デバイスIDは
`web-server` を使います。また、ポートは上記の設定に合わせます。

```bash
fvm flutter run -d web-server --web-port=3000
```

## アプリと Emulator UI の参照

アプリ: <http://localhost:3000>

エミュレータ: <http://localhost:4040>

## 結論

何をやるにしてもドキュメントは真面目に読まなければなりません。

## おまけ

Codespaces での作業が終わったら、不要な課金をされないよう必ず忘れずに停止しましょう。

Tag: github codespaces flutter firebase
