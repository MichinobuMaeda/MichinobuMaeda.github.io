# Load ave. って結局何？

Update: 2011-11-04



Unix / Linux のサーバの CPU の負荷を表す指標として Load ave. というのがあります。 CPU 使用率だけじゃダメなんです。 CPU 使用率が短いスパンで見ても 10% 以下に収まっているようなときにはどちらも気にしなくていいのですが、負荷が上がった場合、それが継続する場合、気にしないわけにはいきません。「CPU 使用率が 100% だとしても、 Load ave. が 3 なのか 6 なのかでは違う」 ( [http://en.wikipedia.org/wiki/Load\_(computing)](http://en.wikipedia.org/wiki/Load_(computing)) ) ということなのですが、詳しい説明は省きます。

Load ave. の考え方は日本の情報処理試験に出てくる待ち行列に似ています。どこが違うかというと、 Unix / Linux は ( Windows も NT 以降は ) マルチタスクです。先に処理開始したプロセスが完了しなくても、次のプロセスの処理を開始できます。その上、最近はマルチコアが当たり前です。待ち行列の M/M/1 の公式を当てはめることはできません。 M/M/n は。。。すみません、私には理解できませんが、 Load ave. に雰囲気近い値を出すことができるかもしれません。たぶん、誤差は数倍とか数桁くらいでしょう。

しかしながら Load ave. のモデルはさほど複雑なものではありません。デフォルト 10 ミリ秒の単位で空いている CPU に仕事を割り当てます。発生した仕事が "Load" です。 ( "Examining Load Average" Dec 01, 2006 By Ray Walker [http://www.linuxjournal.com/article/9001?page=0,0](http://www.linuxjournal.com/article/9001?page=0,0) ) 。この数字に I/O 等の待ちの時間は含みません。CPU のコアやスレッドの数が多ければそれだけたくさんの仕事ができますから、マルチコア・マルチスレッドの 1個あたりの負荷を考えるには割り算しなければなりません。

文系の私にはこれを計算式の形にすることはできませんが、単純化してシミュレートするのは難しくありません。 10 ミリ秒単位時間軸の上でランダムにプロセスを発生させて、空いている CPU に割り当てて、それぞれのプロセスの残時間や経過時間や CPU 利用時間をひたすら足し算引き算しつづけたらいいのです。以下の前提でプログラム書いてみました。

*   割り当てられたプロセス無しでも、 I/O 待ちでも、とにかく空いている CPU は使います。
*   各CPUコアはメモリを共有してます。従って、空いているどの CPU を使ってもかまいません。
*   プロセスを処理している CPU コアが処理の途中で変わってしまった場合の細かなオーバーヘッド等は無視します。
*   I/O等の待ちについては、各プロセスの処理時間に占める率だけがわかるということにします。つまり、いつ発生するかまでは予測できないということにします。乱数使って適当に処理します。

計算には10数秒～数分かかります。乱数の素との関係で、同じ設定値でも実行するたびに結果が変わります。

```
<script language="javascript">

var quantum = 10; // Linux のタイムスライスの間隔 ( msec. )
var tcka = 1000 * 60 / quantum;   // タイムスライス数で表した 1分
var tckb = 5000 * 60 / quantum;   // タイムスライス数で表した 5分
var tckc = 15000 * 60 / quantum;  // タイムスライス数で表した 15分
var cpu;    // 設定値: CPU数 ( 個 )
var siz;    // 設定値: プロセスの処理時間 ( quantum )
var ior;    // 設定値: I/O等の待ち時間の割合
var frq;    // 設定値: プロセスの発生頻度 ( 回 / quantum )
var len;    // 設定値: シミュレートする時間 ( quantum )
var jiffy;  // 処理開始以降のタイムスライス数
var q;// 割り当て待ちのプロセス
var p;// 処理済みのプロセスの情報
var ccnt;   // CPU使用回数
var l;// Load値のリスト

/** シミュレートする。 */
function runsim() {

  // 表示を初期化する。
  document.getElementById("time").value = '-';
  document.getElementById("ocnt").value = '-';
  document.getElementById("rate").value = '-';
  document.getElementById("tmax").value = '-';
  document.getElementById("tave").value = '-';
  document.getElementById("lmax").value = '-';
  document.getElementById("lave").value = '-';
  document.getElementById("lava").value = '-';
  document.getElementById("lavb").value = '-';
  document.getElementById("lavc").value = '-';

  // 設定値を取得する。
  cpu = document.getElementById("cpu").value;
  if ((cpu < 1) || (cpu != Math.round(cpu))) {
    alert("CPU数には 1 以上の整数を記入してください。");
    return;
  }
  siz = document.getElementById("siz").value * 1000 / quantum;
  if (siz <= 0) {
    alert("プロセスの処理時間には正の数を記入してください。");
    return;
  }
  ior = document.getElementById("ior").value / 100;
  if (ior < 0) {
    alert("I/O等の待ち時間には 0% 以上の値を記入してください。");
    return;
  }
  if (1 <= ior) {
    alert("I/O等の待ち時間には 100% 未満の値を記入してください。");
    return;
  }
  if ((document.getElementById("frqc").value <= 0) ||
(document.getElementById("frqt").value <= 0)) {
    alert("プロセスの発生頻度には正の値を記入してください。");
    return;
  }
  frq = document.getElementById("frqc").value / document.getElementById("frqt").value * quantum / 1000;
  len = document.getElementById("len").value * 1000 / quantum;
  if (len < 1) {
    alert("シミュレートする時間には 0.01 秒以上の値を記入してください。");
    return;
  }

  // 計算結果を初期化する。
  jiffy = 0;
  q = [];
  p = [];
  l = [];
  ccnt = 0;
  tave = 0;
  tmax = 0;

  // シミュレートする。
  while (jiffy < len) {

    utilized = 0; // CPUの処理数
    load = 0;     // Load数

    // 設定値に基づく頻度でプロセスを発生させる。
    for (i = 0; i < 10; ++i) {
if (Math.random() < (frq / 10)) { q.push([siz, 0]); }
    }

    // 各プロセスを処理する。
    for (i = 0; i < q.length; ++i) {

// 処理済みのプロセスは対象外。
if (q[i][0] == 0) { continue; }

// スループットをカウントアップする。
++q[i][1];

// I/O等待ちの場合はCPUの処理無し。
if (Math.random() <= ior) {
  --q[i][0];
  continue;
}

// Load数をカウントする。
++load;

// CPU数だけ処理する。
if (utilized < cpu) {
  ++utilized;
  --q[i][0];
}
    }

    while ((q.length > 0) && (q[0][0] == 0)) {
p.push(q.shift());
    }

    // CPU処理数を加算する。
    ccnt += utilized;

    // Load値をリストに追加する。
    l.push(load);

    // 時間を進める。
    ++jiffy;
  }

  // 結果を表示する。
  document.getElementById("time").innerHTML = jiffy * quantum / 1000;
  document.getElementById("ocnt").innerHTML = p.length;
  document.getElementById("rate").innerHTML = Math.round(ccnt / jiffy / cpu * 10000) / 100;
  ttl = 0;
  for (i = 0; i < p.length; ++i) {
    ttl += p[i][1];
    if (tmax < p[i][1]) {
tmax = p[i][1];
    }
  }
  document.getElementById("tave").innerHTML = Math.round(ttl / p.length * quantum) / 1000;
  document.getElementById("tmax").innerHTML = Math.round(tmax * quantum) / 1000;
  ttl = 0;
  lmax = 0;
  wava = 0;
  wavb = 0;
  wavc = 0;
  lava = 0;
  lavb = 0;
  lavc = 0;
  for (i = 0; i < l.length; ++i) {
    ttl += l[i];
    if (lmax < l[i]) { lmax = l[i]; }
    wava += l[i];
    if (0 <= (i - tcka)) { wava -= l[i - tcka]; }
    if (lava < wava) { lava = wava; }
    wavb += l[i];
    if (0 <= (i - tckb)) { wavb -= l[i - tckb]; }
    if (lavb < wavb) { lavb = wavb; }
    wavc += l[i];
    if (0 <= (i - tckc)) { wavc -= l[i - tckc]; }
    if (lavc < wavc) { lavc = wavc; }
  }
  document.getElementById("lave").innerHTML = Math.round(ttl / jiffy * 100) / 100;
  document.getElementById("lmax").innerHTML = lmax;
  if (tcka < l.length) {
    document.getElementById("lava").innerHTML = Math.round(lava * 100 / tcka) / 100;
  }
  if (tckb < l.length) {
    document.getElementById("lavb").innerHTML = Math.round(lavb * 100 / tckb) / 100;
  }
  if (tckc < l.length) {
    document.getElementById("lavc").innerHTML = Math.round(lavc * 100 / tckc) / 100;
  }
}
</script>
<style>
body, div, p, form, h1, h2, h3, h4, h5, h6, input {
  font-size: 100%;
  font-family: Verdana, Geneva, sans-serif;
  margin: 0;
  padding: 0;
  line-height: 1.5em;
  text-align: left;
  font-weight: normal;
}
body {
  background-color: #eee;
}
#header, #footer {
  background-color: #666;
  color: #eee;
  padding: .5em 1em .5em 1em;
}
#header a, #footer a {
  color: #eee;
}
form, #lanes {
  margin: .5em 1em .5em 1em;
}
.ttl {
  display: inline-block;
  width: 12em;
}
input {
  line-height: 1em;
  padding: .1em .25em .1em .25em;
  margin: .1em .1em .1em .1em;
}
.num {
  display: inline-block;
  width: 6em;
  text-align: right;
}
#go {
  line-height: 1em;
  padding: .25em .25em .25em .25em;
  font-size: 150%;
  margin-left: 14em;
}
    </style>
<form onsubmit="return false;">
  <div>
    <span class="ttl">CPU数:</span>
    <input type="text" id="cpu" class="num" value="2"> 個
  </div>
  <div>
    <span class="ttl">プロセスの処理時間:</span>
    <input type="text" id="siz" class="num" value="0.1"> 秒
  </div>
  <div>
    <span class="ttl">I/O等の待ち時間の割合:</span>
    <input type="text" id="ior" class="num" value="80"> %
  </div>
  <div>
    <span class="ttl">プロセスの発生頻度:</span>
    <input type="text" id="frqc" class="num" value="1000"> 回 /
    <input type="text" id="frqt" class="num" value="3600"> 秒
  </div>
  <div>
    <span class="ttl">シミュレートする時間:</span>
    <input type="text" id="len" class="num" value="100000"> 秒
  </div>
  <button id="go" onclick="runsim()">実行</button>
</form>
<div id="lanes">
  <div>
    <span class="ttl">経過時間:</span>
    <span id="time" class="num">-</span> 秒
  </div>
  <div>
    <span class="ttl">処理プロセス数:</span>
    <span id="ocnt" class="num">-</span> 個
  </div>
  <div>
    <span class="ttl">CPU使用率:</span>
    <span id="rate" class="num">-</span> %
  </div>
  <div>
    <span class="ttl">スループット最大:</span>
    <span id="tmax" class="num">-</span> 秒
  </div>
  <div>
    <span class="ttl">スループット平均:</span>
    <span id="tave" class="num">-</span> 秒
  </div>
  <div>
    <span class="ttl">Load最大:</span>
    <span id="lmax" class="num">-</span>
  </div>
  <div>
    <span class="ttl">Load平均:</span>
    <span id="lave" class="num">-</span>
  </div>
  <div>Load ave.</div>
  <div>
    <span class="ttl"> - 1分間平均の最大:</span>
    <span id="lava" class="num">-</span>
  </div>
  <div>
    <span class="ttl"> - 5分間平均の最大:</span>
    <span id="lavb" class="num">-</span>
  </div>
  <div>
    <span class="ttl"> - 15分間平均の最大:</span>
    <span id="lavc" class="num">-</span>
  </div>
  <br>
</div>
```
