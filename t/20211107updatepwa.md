PWA のアップデート
======

Update: 2021-11-07

PWA のアプリをアップデートする単純で確実な仕組みがなかなか見つからなくて困っていました。
以前 [Quasar](https://quasar.dev/) で作ったアプリはキャッシュを削除してリロードするのでよかったようなのですが、
``@vue/cli-plugin-pwa`` で作ったものは Android の場合アプリやブラウザを終了して再起動するまでUIが更新されない場合があるようです。

```
$ npx create-react-app my-app --template cra-template-pwa
```

で作ったアプリも同様です。

[How to clear cache of service worker?](https://stackoverflow.com/questions/45467842/how-to-clear-cache-of-service-worker)
で ``registration.unregister()`` している例は試したことがないので

上記の React の ``cra-template-pwa`` で作成した ``App.js`` を

```
import React from 'react';
import './App.css';

const updateApp = () => navigator.serviceWorker.ready
  .then((registration) => registration.unregister())
  .then(() => { window.location.reload(); });

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Ver.5</p>
        <p><button onClick={updateApp}>Update</button></p>
      </header>
    </div>
  );
}

export default App;
```

としたものを Firebase hosting に置いて試してみました。

Android はこれでよさそうです。

Tag: pwa nodejs react
