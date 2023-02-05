# GitLab で Firebase の Functions のデプロイがうまくいかない

Update: 2020-07-11


GitLab で Firebase のデプロイをしていたら Functions でうまくいきません。
Scheduler をトリガーにする function がエラーになります。
HTTP 400 とか言われます。
権限の問題かなぁと調べましたがよくわかりません。
で、

Deploying a scheduler cloud function (function Failed to create function “function_name”— HTTP Error: 400, The request has errors) \\
https://stackoverflow.com/questions/57255101/deploying-a-scheduler-cloud-function-function-failed-to-create-function-functi

を見て Functions のデプロイの前に

```
 - npm install -g firebase-tools@latest
 - npm install -g firebase-functions@latest
```

を入れたらあっさり直りました。ベースになる Docker イメージが少し古かったんですね。
まあ、そういうことはありそうだなぁ。

追記： 自分用の Docker Image を作りました → [Firebase の CI/CD 用の Docker を作る](gitlabcicddockernodefirebase.html)


Tag: git firebase devops



