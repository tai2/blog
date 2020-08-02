Reduxアプリであれば、React Hot LoaderやLiveReactloadを使わずともライブリロードが可能
######################################################################################

:date: 2016-08-30
:slug: react-redux-reload
:tags: javascript, react, redux, browserify, livereload
:summary: SPAの開発において、効率良く作業を進めるためには、ライブリロードがなんとしても必要です。アプリの状態を保持したままコードの修正を反映できれば、効率的な開発が可能になります。

`SPA <https://en.wikipedia.org/wiki/Single-page_application>`_ の開発において、効率良く作業を進めるためには、ライブリロード[ref]ここでは、フルページロードではなく部分的なロード、また、アプリの状態を保持したままのロードとします[/ref]がなんとしても必要です。

たとえば、1.商品選択画面、2.注文画面、3.注文完了画面の3ステップからなるアプリを考えてみましょう。

素朴にReactを使って開発した場合、コードの修正したあと、結果を反映させるためにブラウザをリロードすると、状態がリセットされます。
そのため、最後の注文完了画面の調整をしたいときに、リロード後、毎回商品選択からはじめて、商品を選択し、送付先住所を入力した後、結果を確認しなければなりません。
仮に商品選択画面と注文画面での手動データ入力に1分かかるとすると、注文完了画面を100回修正して、そのたびに結果を確認すると、100分もの無駄な待機時間が発生してしまいます。

アプリの状態を保持したままコードの修正を反映できれば、効率的な開発が可能になります。

実現方法
=========

Reactアプリの開発で、ライブリロードを実現するための現在もっともメジャーな方法は、おそらく `Webpack <https://webpack.github.io/>`_ と `React Hot Loader <http://gaearon.github.io/react-hot-loader/>`_ プラグインを使うことです。

React Hot Loaderの中身を見ると、ソースコードを解析してReact Component自体を `proxyクラス <https://github.com/gaearon/react-proxy>`_ に `置き換える <https://github.com/gaearon/babel-plugin-react-transform>`_ など、 `非常に込み入った処理 <https://medium.com/@dan_abramov/hot-reloading-in-react-1140438583bf>`_ をしており、 `Webpackにはnpmとの互換性がない <http://blog.namangoel.com/browserify-vs-webpack-js-drama>`_ という問題もあります。BrowserifyとWebpackは目的は似ているものの、その思想がまったく異なり、筆者個人は、どちらかというとBrowserifyのほうが好みです。

BrowserifyでReactのライブリロードを実現するモジュールに、 `LiveReactload <https://github.com/milankinen/livereactload>`_ がありますが、これは現状、 `いくつかの問題 <https://github.com/gaearon/react-hot-boilerplate/pull/61>`_ を抱えているReact Hot Loader 2と同様のアーキテクチャを採用しています。軽く試してみた感じでは動いていたはいましたが、そもそもReact Hot Loader同様、仕組みが複雑なことに若干の不安があり、不安定なのではないかという疑念が拭えません。

しかしながら、ReduxやReact Hot Loaderの作者Dan Abramov氏も `言うように、 <https://medium.com/@dan_abramov/hot-reloading-in-react-1140438583bf#2727>`_ Reduxを使って、状態がすべてシングルツリーでStoreに格納されたアプリであれば、複雑な仕組みは不要です。
Storeを永続化してしまえば、例えフルページリロードを行っても、元の状態を復元できるからです。

`Redux DevTools <https://github.com/gaearon/redux-devtools>`_ では、開発用に状態をlocalStoregeに永続化する機能が提供されているのでこれを使います。
キーを指定することでセッションを区別する仕組みなので、様々なパターンをキーで区別して保存しておくことができる点が便利です。
あとは、 `browserify-hmr <https://github.com/AgentME/browserify-hmr>`_ [ref]BrowserifyでWebpackの `Hot Module Replacement <https://webpack.github.io/docs/hot-module-replacement.html>`_ を使えるようにするモジュール[/ref]を使ってトップレベルのコンポーネントで更新を検知して、以下のようにコンポーネントツリー全体を再描画すれば、状態を維持したまま更新が反映されます。

.. code-block:: javascript

    render(<App/>, document.getElementById('app'));

    if (module.hot) {
        module.hot.accept('app/components/app_dev.jsx', function() {
            const NextApp = require('app/components/app_dev.jsx');
            render(<NextApp/>, document.getElementById('app'));
        });
    }

この方法であれば、ルートコンポーネントをまるごと入れ替えるため、reducerやミドルウェアを含めたstoreのライブリロードにも自動的に対応できます。

ただし、筆者の環境では、Watchifyでの差分ビルドに2秒程度かかってしまいます。簡単に原因を調べたところ、Redux関連をはじめ、いろいろなモジュールをimportしていたら、いつのまにかビルドが遅くなっていました。[ref]なにか改善案があればぜひ教えてください[/ref]

CSSのリロードは、ふつうに `LiveReload <http://livereload.com/>`_ で行いました。できれば、 `sassify <https://github.com/davidguttman/sassify>`_ などですべてをBrowserify/Watchifyに統一したがったのですが、どうしても速度面でLiveReloadに敵わなかったため、このような形に落ち着きました。

サンプルコード
===============

サンプルコードをGitHubに置きました。

`react-redux-reload-sample <https://github.com/tai2/react-redux-reload-sample>`_

.. figure:: {static}/images/react-redux-reload/screenshot.png
   :alt: サンプルアプリのスクリーンショット

   サンプルアプリのスクリーンショット

1. 商品選択画面
2. 注文画面
3. 注文完了画面

これら3つの画面からなるECサービスで、1,2,3の順に遷移します。

React Router対応
=================

サンプルでは、クエリ文字列でセッションキーを渡すようにしてあります。 `React Router <https://github.com/reactjs/react-router>`_ を併用する場合は、なにもしないとルート遷移でクエリ文字列が消えてしまうので、以下のようにRouteのonChangeコールバックを利用して、セッションキーを引き回すなどの処理が必要になります。

.. code-block:: javascript

    function onChange(prevState, nextState, replace) {
        if (prevState.location.query.debug_session && !nextState.location.query.debug_session) {
            replace({
                pathname: nextState.location.pathname,
                query: Object.assign({}, nextState.location.query, {debug_session: prevState.location.query.debug_session}),
            });
        }
    }

