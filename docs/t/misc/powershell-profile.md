# PowerShell の Profile

Update: 2016-09-18

PowerShell に Linux の Shell の .profile みたいなものはないものかと思ってたらありました ( [Windows PowerShell プロファイル](https://technet.microsoft.com/ja-jp/scriptcenter/powershell_owner06.aspx) ) 。たまには真面目に Microsoft 社のドキュメントも読んでみるものです。このページより詳しいのは [Understanding the Six PowerShell Profiles](https://blogs.technet.microsoft.com/heyscriptingguy/2012/05/21/understanding-the-six-powershell-profiles/) ですが、日常使うのは次の２個で足りるでしょう。

- PowerShell のコンソールで `$profile` が指しているパス。
- PowerShell ISE のコンソールで `$profile` が指しているパス。

それぞれ異なるファイル名です。私の場合、そのファイルに `cd` など書いています。
