# GitHub Pages で Mermaid を使う

Update: 2022-06-04

GitHub が Markdown への Mermaid のダイアグラムの埋め込みに対応しました。
[Include diagrams in your Markdown files with Mermaid](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/)

しかしながら Jekyll の本体はそんなものには対応していなくてプラグインなどが必要になります。で、
Pages でプラグインが使えるのかというと、使えなくなはいけど、面倒なことになりそうな。。。プラグイン無しでなんとかする方法を探してみたらありました。

[Embed Mermaid in Jekyll without plugin](https://jackgruber.github.io/2021-05-09-Embed-Mermaid-in-Jekyll-without-plugin/)

コードをコピペしてみたら、動かない。。。
JavaScriptのコンソールのエラーは「`$` なんか知らん」ってそりゃここでは jQuery 使ってないもの。
jQuery を使わない方法に変えます。

`body` の `onload` で次の処理を呼びます。

```javascript
function initializeMermaid() {
   mermaid.initialize({
      startOnLoad:true,
      theme: "default",
   });
   window.mermaid.init(
      undefined,
      document.querySelectorAll('.language-mermaid'),
   );
}
```

記事と同じサンプルを試してみます。

<pre><code>```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```</code></pre>

ローカルで動きました。

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

highlight.js が「 `mermaid` なんて言語は知らん」と言ってますが、警告出してなにも処理しないということのようなのでこのままとします。

Tag: github mermaid
