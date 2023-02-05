# 最近のWebアプリはアイコンがたくさん必要で

Update: 2020-07-11


ホームページやスマホのアプリのアイコンはみなさん日常目にするもので、それがわかりにくいと困るわけです。私も Slack とか Google Maps のアイコンがいきなり変わってしまったときには「ど〜こ〜だ〜よ〜あったはずだよな〜」とむかつきながら探しました。昔は小さなサイズの画像を ICO というマイクロソフト社が決めた ( たぶん ) フォーマットで置いとけばよかったのですが、今は PC もスマホもディスプレイが高解像度になって、ずいぶん大きなサイズのきれいな画像をアイコンとして使うことができます。そこに小さなサイズの画像を無理やり拡大したガタガタのアイコンを表示したくはないですよね。でも、昔からある fabvicon.ico など小さなサイズも相変わらず必要です。そのため、何か作るたびにせっせと GIMP でそれぞれのサイズの画像を作っていたのですが、「少し色合いが気に入らないから修正」とかなると全部やり直しです。

そんなアイコンの中に ``safari-pinned-tab.svg`` というのがあります。 SVG だから解像度は関係なくきれいにレンダリングできるベクター形式です。これだけ Illustrator みたいなツールで作ってそれ以外を自動生成すればいいよね？

ちなみに余談ですが私は Adobe に毎年数万円払うほどのことはやってないし、かといって Adobe の単体プランでは足りないし、で、 [GIMP](https://www.gimp.org/) と Illustrator より少し安い Affinity Designer で済ませています。

普段よく使う言語は Node.js なので、まず、PNG 形式の画像ファイルは [sharp](https://sharp.pixelplumbing.com/) を使いました。処理が速いので、アプリの処理で画像の加工などをする場合も使っていいと思います。ほとんどデフォルトの設定でだいじょうぶなのですが SVG の場合は入力データのオプションの ''density'' にデフォルトの 96 より大な値を設定する方がいいかもしれません。 SVG に設定されている表示サイズかまたは DPI が小さい場合、出力される PNG も荒くなってしまいます。元のデータが十分大きければ ( 例えば 1024 x 1024 ) 設定無しでもだいじょぶです。

次に ICO 形式なのですが、 sharp は対応していないようで [icon-gen](https://github.com/akabekobeko/npm-icon-gen) を使いました。 icon-gen で PNG も出力できるのですが、 sharp の方が処理が速いしファイル名、切り抜き、フィルタ ( kernel ) など細かな設定もできるので icon-gen を使うのは ICO だけにします。

icon-gen の仕様は「作った人自身が使いやすいように作ったな」という感じでいっぺんにいろいろなものを出力するようになっています。で、私が作りたいのは ``favicon.ico`` だけなんだけど ``favicon`` オプションはどう設定しても PNG がいっしょに出力されてしまいます。私がドキュメントを読み間違えているかな。。。そのようなわけで ``ico`` オプションで出力ファイル名に ``favicon.ico`` を指定することにしました。

コードは以下の通り。入出力先は Vue CLI で Vuetify + PWA のプロジェクトを作った場合の形です。他でも似たような感じでしょう。出来上がった ICO を GIMP で開いてみると 16px, 32px, 48px それぞれの画像が入っていましたので問題なさそうです。

```
const path = require('path')
const sharp = require('sharp')
const icongen = require('icon-gen')

// Vue + Vuetify + PWA の場合
const iconsPath = path.join(__dirname, '..', 'public', 'img', 'icons')
const faviconPath = path.join(__dirname, '..', 'public')
// 入力に safari-pinned-tab.svg 以外のファイルを利用する場合は変更する。
const inputPath = path.join(iconsPath, 'safari-pinned-tab.svg')

// Vue + Vuetify + PWA の場合
const targets = [
  {
    source: inputPath,
    size: 192,
    name: 'android-chrome-192x192.png'
  },
  {
    source: inputPath,
    size: 512,
    name: 'android-chrome-512x512.png'
  },
  {
    source: inputPath,
    size: 192,
    name: 'android-chrome-maskable-192x192.png'
  },
  {
    source: inputPath,
    size: 512,
    name: 'android-chrome-maskable-512x512.png'
  },
  {
    source: inputPath,
    size: 180,
    name: 'apple-touch-icon.png'
  },
  {
    source: inputPath,
    size: 60,
    name: 'apple-touch-icon-60x60.png'
  },
  {
    source: inputPath,
    size: 76,
    name: 'apple-touch-icon-76x76.png'
  },
  {
    source: inputPath,
    size: 120,
    name: 'apple-touch-icon-120x120.png'
  },
  {
    source: inputPath,
    size: 152,
    name: 'apple-touch-icon-152x152.png'
  },
  {
    source: inputPath,
    size: 180,
    name: 'apple-touch-icon-180x180.png'
  },
  {
    source: inputPath,
    size: 16,
    name: 'favicon-16x16.png'
  },
  {
    source: inputPath,
    size: 32,
    name: 'favicon-32x32.png'
  },
  {
    source: inputPath,
    size: 144,
    name: 'msapplication-icon-144x144.png'
  },
  {
    source: inputPath,
    size: 150,
    name: 'mstile-150x150.png'
  }
]

targets.forEach(target => {
  // 入力がSVGで出力の解像度が低い場合は density を大きな値に変更する。
  const inputImage = sharp(target.source, { density: 96 })
  inputImage.metadata().then(metaData => {
    inputImage
      // トリミングが必要な場合は設定する。
      .extract({
        left: 0,
        top: 0,
        width: metaData.width - 0 * 2,
        height: metaData.height - 0 * 2
      })
      // kernel は通常 lanczos3 (default) でよい。
      .resize(
        target.size,
        target.size,
        {
          kernel: sharp.kernel.lanczos3
        }
      )
      .toFile(path.join(iconsPath, target.name))
  })
})

icongen(inputPath, faviconPath, {
  report: true,
  ico: {
    name: 'favicon',
    sizes: [16, 32, 48]
  }
}).then((results) => {
    console.log(results)
  })
  .catch((err) => {
    console.error(err)
  })
```

Tag: nodejs gimp icon-gen



