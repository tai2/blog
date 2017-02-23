React Redux Real World Examples 〜先人から学ぶReact Reduxの知恵〜
===================================================================

:date: 2017-2-22
:slug: real-world-redux
:tags: javascript,react,redux
:summary: この記事は、実際のReact Reduxプロダクトのソースコードを調査することで、筆者がふだんReact Reduxで開発をしていて感じる疑問への答えを探る試みです。

React Reduxを使ってプロダクトを作りはじめて、かれこれ半年くらい経ちます。
しかし、どうもうまく書けていない気がすることがときどきあり、悩んでいたところ、ツイッターで次のような助言をもらいました。

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="en-gb"><p lang="ja" dir="ltr"><a href="https://twitter.com/__tai2__">@__tai2__</a> 達人かどうかは微妙なところがありますが、ある程度の規模のコードはここにリンク集あります <a href="https://t.co/B79B5s1DTe">https://t.co/B79B5s1DTe</a></p>&mdash; Yuki Kodama (@kuy) <a href="https://twitter.com/kuy/status/806651108793851904">8 December 2016</a></blockquote>
    <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

この記事は、上記のリンク集でまとめられている実際のReact Reduxプロダクトのソースコードを調査することで、筆者がふだんReact Reduxで開発をしていて感じる疑問への答えを探る試みです。

筆者が答えを得たいと思っている疑問は次の4つです
[ref]いろいろわかった今から見れば、単に筆者の無知から来る疑問だったものもあります。実際のところ、これらの疑問の多くは `公式ドキュメント <http://redux.js.org/>`_ を隅から隅まで読めば、答えやヒントが言及されています)。ちなみに、副作用については、筆者の中では現状 `redux-saga <https://github.com/redux-saga/redux-saga>`_ で対応するという答えで決着しており、とくに疑問に思う部分もないため扱いません。[/ref]

* Storeはどんな具合に階層化すべきか
* Store初期化(hydration)用データの定義はどうすべきか
* Componentはどう整理すべきか
* データフェッチはどう実装すべきか

.. contents:: 目次

事例
----

冒頭で上げたReact Reduxアプリリンク集には、実に32個ものサンプルがありました(2016年12月時点)。
ひととおり手元にダウンロードして動かしてみたり、コードがどのように書かれているかを簡単に確認しましたが、ここですべてに触れることはもちろんできません。本記事では、もっとも典型的なコードの書き方のお手本と考えて良いであろう、公式のRedux Real World Exampleに加えて、規模の大きさやコードの綺麗さなどから、参考になりそうな2つのアプリをとくに詳しく見ます。

Redux Real World Example
~~~~~~~~~~~~~~~~~~~~~~~~~

https://github.com/reactjs/redux/tree/master/examples/real-world

.. figure:: {filename}/images/real-world-redux/redux-real-world.png
   :alt: Redux Real World Example

   Redux Real World Exampleのスクリーンショット

GitHubのAPIから取得したデータを表示するサンプルです。
非常に小規模なコードですが、URLルーティングや非同期API通信など最低限の要素を備えています。[ref]componentDidMountではなく、 `componentWillMount <https://facebook.github.io/react/docs/react-component.html#componentwillmount>`_ でデータフェッチをしている点がちょっと気になるところではあります。[/ref]
`react-router <https://github.com/ReactTraining/react-router>`_ を使用しており、指定されたユーザーがスターを付けたプロジェクトを一覧する画面と、指定されたプロジェクトのコントリビューター一覧を表示する2つの画面から成ります。また、 `normalizr <https://github.com/paularmstrong/normalizr>`_ を使ってAPIからのレスポンスを正規化しているのも特徴です。

Project Tofino
~~~~~~~~~~~~~~~

https://github.com/mozilla/tofino

.. figure:: {filename}/images/real-world-redux/tofino.png
   :alt: Project Tofino

   Tofinoのスクリーンショット

MozillaによるブラウザUI実験用のElectronアプリで、UI部分がReact Reduxで実装されています。
小〜中規模プロダクトでありそうなコード量(UI部分だけで12000行程度)であることと、Reducerのコードが非常に読みやすく整理されているため取り上げることにします。Immutable.js使用。

redux部分は、 `/app/ui/にまとまっています。 <https://github.com/mozilla/tofino/tree/7fd8ff0f9a17159893ea4edd613bb90fbc791a29/app/ui>`_ 

wp-calypso
~~~~~~~~~~~

https://github.com/Automattic/wp-calypso

.. figure:: {filename}/images/real-world-redux/wp-calypso.png
   :alt: wp-calypso

   wp-calypsoのスクリーンショット

Automatic社による、React Reduxを(部分的に)使ったWordPress.comの新しい実装です。
それなりの規模があるコードベース(クライアントサイド35万行以上)で、どのようにコードを整理しているのかの実例として、取り上げます。
Node.jsによるSSR込みの本格的なUniversal JavaScriptの実例でもあります。
DucksというReduxの状態を関心ごとに分離するパターンに近い形で構成されています。

かなり大規模で、すでにある程度の歴史を経ている(Initial commitは2015年11月)だけあって、
createClassとextends Componentが同居してたり、fluxとreduxが同居してたり、Object.assignとImmutable.jsが同居してたりする、という意味でもリアルです。

----------

[コラム]Ducksパターン
----------------------

`Ducks <https://github.com/erikras/ducks-modular-redux>`_ は、Action Type、Action Creator、Reducerを関心ごとにひとまとめにしてパッケージ化するためのパターンです。
本来、ActionはReducerとは直交する概念であり、任意のReducerが任意のAction Typeを扱うことができます。
しかし、実際のアプリでは、ReducerとAction Typeの間に偏りがあり、あるActionは、特定のReducerによってしか処理されないことが多いです。
たとえば、:code:`CREATE_USER` , :code:`UPDATE_USER` , :code:`DELETE_USER` というAction Typeは、:code:`user` Reducerにしか影響しない、といった具合です。

Ducskの提案では、どのようなルールでパッケージを定義するかというところを厳密に定義していますが、大事なのは関心ごとにこれらをまとめることで、アプリをサブシステムに分解することができ、管理がしやすくなるということです。たとえば、上記に加えて `Selectorもパッケージに含めてもいいと思います。 <https://twitter.com/dan_abramov/status/664581975764766721>`_
wp-calypsoでは、Ducsk風の関心の分離を行うことで、分割統治を行っています。大規模になるほど、このパターンの有効性は増してくると思われます。

----------

Storeはどんな具合に構成すべきか
---------------------------------

Storeの形(Shape)は、Reducerの返すデータによって規定されます。言いかたを変えると、ReducerはStoreがそうあるべき形状に合致したデータを返さなければなりません。Storeをどのように構成するかによって、Reducerの可読性が決まるといっても過言ではないでしょう。

Reducerは、 :code:`(state, action) -> state` とい形式の純粋関数です。
純粋関数という制約を持つがゆえに、書くときにじゃっかん特殊なテクニックが要求されます。

あるとき、筆者はReducerのあるケース節がとんでもなく可読性の低いコードになっていることに気付きました。
階層化されたデータを直接変更することなく新しい値を得るために、無数のmap、アロー関数、スプレッド記法、Object.assignなどが詰め込まれた、解読に時間を要するようなコードです。このようなコードの例として、例えば、 `JSchematic <https://github.com/nicksenger/JSchematic>`_ というアプリの `Reducerの一部 <https://github.com/nicksenger/JSchematic/blob/29b841e7ec94c0730f0af277a6aa51554390ad14/src/js/reducers/reducerManageElements.js#L12>`_ はかなり読みづらいと思います。

また、こんなこともありました。Reducerの実装では、Redux標準のcombineReducersという高階関数を利用することで、複数のスライス(サブツリー)に分割して、関心の分離を実現できます。
これはReduxアプリでの基本テクニックですが、スライスされたReducerから、別のスライスに分離されたサブツリーを参照したくなりました。
combineReducersによる分離では、各スライスが、あたかも独立したツリーであるかのようになり、お互いに見えなくなります。

.. code-block:: javascript

    function a(state, action) {
       // スライスaを変更する処理
    }

    function b(state, action) {
       // スライスbを変更する処理
    }

    function c(state, action) {
       // スライスcを変更する処理
    }

    export default combineReducers({a, b, c});
    // combineReducersで状態を分割した場合、お互いの状態を知らない「スライス」となる。
    // スライスcからスライスa,bの値が欲しくなっても参照することはできない。

どうすればいいかしばらく悩んだあげく、しかたがないので欲しい値を計算する処理を、見える範囲にもうひとつ書いてしのぎました。つまり、重複する値の計算処理をスライスごとに1個ずつ書いたのです。たしかに、これで動きはしましたが、正しいことをしている感覚はありませんでした。

そこで、次のような疑問が浮かびます:

* combineReducersの勘所はどのようなものか。
* Reducerの可読性を高めるStoreの構成法はどんなものか。
* ツリーは、どの程度深くなるか、あるいは深くすべきではないか。
* スライス間で共有したいデータがある場合、どうすべきか。

Store構成についての見解
~~~~~~~~~~~~~~~~~~~~~~~~

Reducerの構成方法については、実は `公式のStructuring Reducersというドキュメント <http://redux.js.org/docs/recipes/StructuringReducers.html>`_ にかなり丁寧に書いてあって、これを読めばだいたい勘所が掴めます。この中では、

* ルートReducer: 大本のReducer
* スライスReducer: combineReducersで分割されたReducer
* ケース関数: Reducerの中のひとつのcase節に相等する関数
* 高階Reducer: Reducerを受け取って別のReducerを返す関数

といった概念を導入し、それに沿ってReducerを読み易くするための工夫を説明しています。 
とくに、この `リファクタリングの例 <http://redux.js.org/docs/recipes/reducers/RefactoringReducersExample.html>`_ などは参考になると思います。適切に関数を分割して、ユーティリティー関数を導入することで、可読性が向上していく様が見て取れるからです。

TofinoのReducerは、redux-ecosystem-linksに載っているアプリの中でも、とくに見易い印象を受けました。
たとえば、 `pagesというReducer <https://github.com/mozilla/tofino/blob/7fd8ff0f9a17159893ea4edd613bb90fbc791a29/app/ui/browser-modern/reducers/pages.js>`_ は、Tofinoの中でももっとも複雑なスライスReducerですが、それでも十分な読み易さを保っていると思います。
ポイントは、case節内の具体的な処理をすべてケース関数に抜き出しているところです。筆者の経験では、一定以上の長さのReducerでは、これをするだけで、ずいぶん見通しが良くなって印象が変わります。

個々のケース関数に関しては、Immutable.jsの恩恵によって可読性が向上している面があります。Immutable.jsでは、withMutationsを使えばデータ構造への変更を破壊的に記述することができます。よって、ふつうの手続き型プログラミングと変わらない感覚でReducerが記述できます。

例えば、ページを新規追加するときのケース関数は以下のようになっています。

.. code-block:: javascript

    function createPage(state, id, location = UIConstants.HOME_PAGE, options = {
        selected: true,
        index: null,
    }) {
        return state.withMutations(mut => {
            const page = new Page({ id, location });
            const pageIndex = options.index != null ? options.index : state.displayOrder.size;

            mut.update('displayOrder', l => l.insert(pageIndex, page.id));
            mut.update('ids', s => s.add(page.id));
            mut.update('map', m => m.set(page.id, page));

            if (options.selected) {
                mut.set('selectedId', page.id);
            }
        });
    }

ためしに、これをImmutable.jsを使わずに `Immutable Update Patterns <http://redux.js.org/docs/recipes/reducers/ImmutableUpdatePatterns.html>`_ にならってES2015+の記法のみで書くと、おそらくこのような形になるでしょう。

.. code-block:: javascript

    function createPage(state, id, location = UIConstants.HOME_PAGE, options = {
        selected: true,
        index: null,
    }) {
        const page = new Page({ id, location });
        const pageIndex = options.index != null ? options.index : state.displayOrder.size;
        const displayOrder = [
            ...state.displayOrder.slice(0, pageIndex),
            page.id,
            ...state.displayOrder.slice(pageIndex),
        ];
        const ids = [...state.ids, page.id];
        const newPage = { [page.id]: page };
        const map = { ...state.map, ...newPage };

        const newState = {
            ...state,
            displayOrder,
            ids,
            map,
        };

        if (options.selected) {
            newState.selectedId = page.id;
        }

        return newState;
    }

Immutable.jsを使うのと使わないのでは、コードを完全に理解するために要する時間がまったく違います。
ただ、筆者の所感としては、Immutable.jsは絶対に必要というわけではなく、適宜定型的な処理をユーティリティー関数として抽出したり、場合によっては、 `dot-prop-immutable <https://github.com/debitoor/dot-prop-immutable>`_ のようなモジュールを利用して補うことで、十分に可読性を保てると思っています。

wp-calypsoでは、Ducksライクに `状態を関心ごとに分離しています。 <https://github.com/Automattic/wp-calypso/tree/6153f05db236cfadad8bc166edf99088974b493f/client/state>`_ 各ディレクトリごとにREADMEが配置されていて、設計論のようなものが記述されていたりするのがおもしろいです。Storeの階層はそれなりに深くなっています。扱う状態が深くなるほど、Reducerの可読性は低くなる傾向にあるように思いますが、combineReducersによって適切に状態をスライスすることで、個々のReducerはそれほど読みづらくはなっていない印象です。[ref]もちろん、全Reducerに目を通したわけではありませんが…[/ref]。スライスのスライスのスライスのような、3重にcombineRecucersされたReducerも見られることからも、このwp-calypsoの大規模さがうかがえます。

こうした例から、Storeの構成法、ツリーの深さといったこちについて筆者の得た結論は、こうです。
基本的には、 `正規化 <http://redux.js.org/docs/recipes/reducers/NormalizingStateShape.html>`_ を適切に施せば、そもそもツリーはそれほど深くならないはずだが、大規模アプリなど、管理の都合上どうしてもツリーが深くってしまう場合であっても、combineReducersによって適切にツリーをスライスすることで、Reducerの可読性を保つことができる。

さて、combineReducersによって状態をスライスしたときに、そのメリットのコインの裏返しとして現れてくるのが、前述した、他のスライスが見えなくなるという問題です。これも基本的には、 `公式のBeyond combineReducersというドキュメント <http://redux.js.org/docs/recipes/reducers/BeyondCombineReducers.html#sharing-data-between-slice-reducers>`_ で解決策がいくつか提示されてますが、ここでは、そのひとつとして、 `reduce-reducers <https://github.com/acdlite/reduce-reducers>`_ を取り上げます。reduce-reducersを使うと、Reducerの過程を2パス(あるいはそれ以上)に分割することができます。つまり、reduce-reducersを利用して、1パス目で、他のスライスに依存しない通常のReducerを実行。その後、2パス目で、他のスライスに依存するReducerを改めて実行、というふうにするのです。例えば、次のコードを見てください。

.. code-block:: javascript

    function a(state = 1, action) {
        switch (action.type) {
        case 'FOO':
            return state + 1;
        default:
            return state;
        }
    }


    function b(state = 1, action) {
        switch (action.type) {
        case 'FOO':
            return state * 2;
        default:
            return state;
        }
    }

    // assuming state.a and state.b already exists
    function c(state, action) {
        switch (action.type) {
        case 'FOO':
            return {
                ...state,
                c: state.a + state.b,
            };
        default:
            return state;
        }
    }

    export default reduceReducers(combineReducers({a, b}), c);

a,bは通常のスライスで、cはa,bの計算結果に依存します。このようにreduce-reducersを利用することで、適切な分割を保ちつつ、スライス間でデータを共有できない問題が解消できます。

Store初期化(hydration)用データの定義はどうすべきか
----------------------------------------------------

Reduxでは、Store作成時に初期化(hydration)用のデータを与えることができます。

.. code-block:: javascript

    createStore(reducers, {x: 1, y: [3,4], z: 'foo'});

ここで与えるデータの形は、Reducerによって規定されるデータの形と一致している必要があります。
つまり、Storeの形状があらかじめ定められており、初期値を与える側と、Reducer側が協調して動作する必要があります。
上の例で言うと、reducerの返す状態は、xという数値、yという配列、zという文字列をプロパティとして持っているという暗黙の知識が前提になっています。
しかし、ある程度の規模のアプリでStoreが複雑になってきたときに、初期値として与えているデータと、Reducerの期待するデータの形状が一致していると、どうすれば確信できるでしょうか?なにかひとつの対象を二重管理しているような気がして、若干の不安を感じます。

Store初期化用のデータについての見解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

これには、いくつかの緩和、あるいは解決策があります。

まず、 `combineReducersの動作 <http://redux.js.org/docs/recipes/reducers/InitializingState.html#combined-reducers>`_ を知ることで、これはそれほど問題にはならないことがわかります。なぜなら、combineReducersによってスライスすることで、初期化時にすべてのデータを与える必要はなくなるからです。アプリの実装において、ルートReducerは、combineReducersによって分離されたスライスの集合になっている場合が多いと思います。

.. code-block:: javascript

    const rootReducer = combineReducer({x, y, z});

このようにしたときに、createStoreに与えるデータは、x,y,zそれぞれを個別に指定できます。undefinedのプロパティが存在した場合、そのプロパティは、スライスごとに定義された初期値(通常、Reducerの第一引数のデフォルト値)が使われます。Storeの形について必要な知識も部分的になるため、問題が緩和されたと言えるでしょう。

Tofinoで興味深いのは、Immutable.jsの `Record <https://facebook.github.io/immutable-js/docs/#/Record>`_ を利用して、 `Storeの形状を型として表現している <https://github.com/mozilla/tofino/blob/7fd8ff0f9a17159893ea4edd613bb90fbc791a29/app/ui/browser-modern/model/index.js>`_ ことです。Tofinoでは、 `model/ディレクトリ <https://github.com/mozilla/tofino/tree/7fd8ff0f9a17159893ea4edd613bb90fbc791a29/app/ui/browser-modern/model>`_ にデータ構造が型としてまとめられています。これによって、Storeの形がコードで明示されることになるため、だいぶ安心できます。ただし、Recordの挙動は、プリミティブレベルまで含めたデータ型を定義して厳密なチェックを行うわけではなく、キーが存在しない場合はデフォルト値で初期化、型に定義されていないキーがコンストラクタに渡された場合は無視、存在しないキーに後からsetした場合ランタイムエラーというものなので、バリデーション用途で使うには、心許無いかもしれません。

データ型の定義という点において、wp-calypsoではまた違ったアプローチを取っています。このアプリでは、 `is-my-json-valid <https://github.com/mafintosh/is-my-json-valid>`_ というJSONバリデータを使って定義したスキーマによって、動的に型チェックを行います。
このスキーマ定義は、初期化時にローカル保存しておいたStoreの状態が、動作しているプログラムが期待するデータ構造と一致するかをチェックすることを目的としたものです。wp-calypsoでは、SERIALIZEアクションによって構築される永続化用の状態を、 `定期的にローカル保存します。 <https://github.com/Automattic/wp-calypso/blob/f8ea145698153ffcc69579362b264d945483d030/client/state/initial-state.js#L70>`_ アプリのバージョンが異なれば永続化されるデータ構造も異なる可能性があるため、このようなバリデーションが必要になってくるのです。

あるいは、 `flowtype <https://flowtype.org/>`_ を使ってStoreの状態全体の型を定義すれば、Storeの形状は暗黙の知識ではなくコードで明示されたものになるため、問題を完全に解消できます。ただし、flowtypeによるチェックはあくまで静的なものであるため、ローカルに保存しておいたデータをStoreに流し込んだときに、動的にデータの整合性をチェックするような使い方はできません。[ref] `flow-runtime <https://codemix.github.io/flow-runtime/#/>`_ を利用することで、解決するかもしれません。[/ref] 今回調査したアプリの中には、このようなflowtypeの使いかたを参考になるレベルでしているものは残念ながらありませんでした。[ref]jenkins blueocean-pluginというアプリが `flowtypeを使っていました <https://github.com/jenkinsci/blueocean-plugin/blob/ac60b900a90122cd42a96ca08e2b85c90746df8f/blueocean-web/src/main/js/redux/router.js#L55>`_ が、コード規模が小さくてあまり参考にならないため、取り上げませんでした。[/ref]

余談ですが、Server Side Renderingを行う際のRedux Storeへのデータの受け渡し・初期化方法についても、 `Server Rendering <http://redux.js.org/docs/recipes/ServerRendering.html>`_ というドキュメントが用意されています。 `Relax <https://github.com/relax/relax>`_ というCMSが、このドキュメント `ほぼそのままのやりかた <https://github.com/relax/relax/blob/cf18abcd28fbabd593bdccfc61721c9b64935750/lib/server/shared/helpers/render-html.js>`_ で実装しており、ReduxでSSRをやるときには参考になると思います。

Componentはどう整理すべきか
-----------------------------

JSXによって再利用性の高いComponentを宣言的に記述できることが、Reactの特徴のひとつです。
Componentは実際のところただのJavaScriptの関数もしくはクラスなので、容易に括り出して共通化などができます。
このComponentを細分化する粒度について、なにか指針はあるでしょうか?

Reduxでは、 `connect関数 <https://github.com/reactjs/react-redux/blob/master/docs/api.md#connectmapstatetoprops-mapdispatchtoprops-mergeprops-options>`_ を用いてStoreとComponentを接続します。
接続されたComponentはStoreに変更があると自動的にプロパティが更新されます。
Reduxでは、接続されたComponentを `Container component <https://medium.com/@learnreact/container-components-c0e67432e005#.e5fgnyfic>`_ 、接続されていないComponentをPresentational componentなどと言って区別します。
Container componentは、Componentツリーのルートに限らず、どのノードに差し込んでもかまいません。
Container componentを挿入する位置について、なにか指針はあるでしょうか?

また、Componentの作りかたに関連して、以下のような疑問もあります。

* componentの純粋さにどこまでこだわるべきか。
* :code:`containers/` と :code:`components/` は分けるべきか。
* 階層が深くなったときに、:code:`propName={propsName}` のような、プロパティを上から下に流すだけで記述が冗長になる問題には、どう対処すべきか。

Componentについての見解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Componentの整理方法については、redux-ecosystem-linksに載っているアプリを見た限り、実に様々です。

Componentの純粋さにどこまでこだわるべきか、UIに関する状態をStoreに掃き出すか否かに関する切り分けはどうするか、といったことに関して、
無理なく記述できるのであれば、Componentにはstateを持たせず純粋関数にしておいたほうが良い、という一般論以上の指針は得られませんでした。 `公式のBasic Reducer Structure and State Shape <http://redux.js.org/docs/recipes/reducers/BasicReducerStructure.html>`_ というドキュメントでは、アプリケーションの処理・表示対象となるドメインデータ、現在選択中のアイテムなどを示すアプリ状態、それからUIの状態という3つに分類しています。このうちドメインデータとアプリ状態については、Storeに格納すれば良いと迷いなく判断できるのですが、UI状態については、わざわざStoreに格納する意味が薄くComponentに状態を持たせたほうが合理的な気がして、判断に悩む部分があります。ケースバイケースで判断するしかないかもしれません。

Reduxに含まれるサンプルプログラムをはじめとして、多くのアプリでは、 :code:`containers/` と :code:`components/` という形で `ディレクトリを分けています。 <https://github.com/reactjs/redux/tree/master/examples/real-world/src>`_
しかし、このディレクトリ構成にどれほど意味があるのか筆者は疑問を感じています。
主な理由としては、PresentationalとContainerの区別というのは、実際には `それほど明確ではなく、 <https://medium.com/@dan_abramov/smart-and-dumb-components-7ca2f9a7c7d0#.7smj0zmty>`_ しばしばPresentational ComponentであったものがContainer Componentに昇格したりしますし、Presentationalの世界にContainerはいっさい現れることなく閉じているのであればともかく、PresentationalとContainerと入り乱れてビューツリーを構築します。 また、しばらくこのやりかたで開発をしてみて、大きなメリットを感じたこともありません。むしろ、ディレクトリおよびクラスが明確に分かれていることに煩雑さを感じます。それなりに実際的なコードであるTofinoでもwp-calypsoでも、ディレクトリを分けて明確に区別することはしていませんし、国内における大規模なReact Reduxの適用事例のひとつであるアメブロでも、やはり `区別はしていない <https://developers.cyberagent.co.jp/blog/archives/636/>`_ ようです。

かわりに筆者が使っているディレクトリ構成は次のようなものです。

* Presentational,Containerの区別なく、Componentはすべて :code:`components/` ディレクトリに格納する。
* すべてのComponentは、各々ディレクトリと :code:`index.jsx` と :code:`styles.pcss` を持つ(CSS Modulesが前提)。
* Container componentは、 :code:`compoennts/` 直下に置く。
* あるContainer component専用のComponentは、そのContainer componentのディレクトリ配下に置く。
* 複数のComponentから利用される再利用可能なPresentational Componentは、:code:`components/shared` に置く。

言葉だけではわかりづらいので、この構成の例を次に挙げます。

.. code-block:: txt

    components
    ├── ContainerA
    │   ├── Sub1
    │   │   ├── index.jsx
    │   │   └── styles.pcss
    │   ├── Sub2
    │   │   ├── index.jsx
    │   │   └── styles.pcss
    │   ├── index.jsx
    │   └── styles.pcss
    ├── ContainerB
    │   ├── index.jsx
    │   └── styles.pcss
    └── shared
	└── Button
	    ├── index.jsx
	    └── styles.pcss

さて、次に :code:`propName={propName}` のような、プロパティの受け渡しが増殖して煩雑になってしまう問題です。
実例として、Relaxというアプリの `LinkingというComponent <https://github.com/relax/relax/blob/cf18abcd28fbabd593bdccfc61721c9b64935750/lib/shared/screens/admin/shared/components/page-builder-menu/tabs/link/linking.jsx#L94>`_ を見てみます。このComponentではいくつかのプロパティを受け取っていますが、ほとんどは、そのまま次の :code:`Property` Componentに流しているだけです。
Reactアプリを開発していて、このような状況に遭遇したことのある方も多いのではないでしょうか。

この状況を解消する手段はいくつか考えられます。

まず、connectをしてStoreと直接繋ぐことで、プロパティの受け渡しをなくすことです。
Redux作者のdan_abramovも、プロパティを使わずに次のComponentに送っていることに気付いたら、新しいContainer Componentを導入する良いタイミングであると `述べています。 <https://medium.com/@dan_abramov/smart-and-dumb-components-7ca2f9a7c7d0#.a4ezrej5l>`_

それから、多くのプロパティを次に委譲しているだけであれば、Reactの `spread演算子 <https://zhenyong.github.io/react/docs/jsx-spread.html>`_ を使うことで、コードを大幅に短縮することもできます。
例えば、wp-calypsoの `Card <https://github.com/Automattic/wp-calypso/blob/7475c744b951cbe4b44525c2aa93d2708adaeae0/client/components/card/index.jsx>`_ というComponentは、共通のプロパティであるバリエーションである、 `CompactCard <https://github.com/Automattic/wp-calypso/blob/7475c744b951cbe4b44525c2aa93d2708adaeae0/client/components/card/compact.jsx>`_ というComponentを持っています。これはReactにおけるspread演算子の典型的な利用例です。

Tofinoにもspread演算子に関するおもしろいテクニックが見られます。
PropTypesを定義する際に、子Componentに渡したくないプロパティを別に分けておき、lodashの :code:`omit` と :code:`Object.keys` を利用することで、プロパティの **消費** を `賢く表現しています。 <https://github.com/mozilla/tofino/blob/7fd8ff0f9a17159893ea4edd613bb90fbc791a29/app/ui/shared/widgets/dropdown-menu-btn.jsx#L132>`_ ただし、このテクニックは、Componentのプロパティ定義をflowtypeで行っている場合には残念ながら使えません。flowtypeの型情報は実行時には除去されてしまうためです。

もう一つ考えられるのは、renderが大きくなってきてコードを整理する際に、別Componentに分けるのではなく、別メソッドにrenderFooのようなメソッドを設けて分離することです。同じクラス内のメソッドであれば、Componentのプロパティには :code:`this` 経由でどこからでもアクセスできるため、そもそもプロパティの受け渡しは不要です。

データフェッチはどう実装すべきか
---------------------------------

あるComponentがマウントされてたときに表示に必要なデータフェッチのトリガーは、どこからどのような形で行うべきでしょうか?
筆者がまず思い付いたやりかたは、onDidMountのような名前のデータフェッチのトリガーとなるメソッドをmapDispatchToPropsで定義して、componentDidMountからそれを呼ぶという方法です。

.. code-block:: javascript

    class Foo extends Component {
	componentDidMount {
            this.props.onDidMount();
	}
    }

    function mapStateToProps(state) {
        return {};
    }

    function mapDispatchToProps(dispatch) {
	return {
	    onDidMount() {
		dispatch(fetchData());
	    }
	}
    }

    export default connect(mapStateToProps, mapDispatchtoProps)(Foo); 

しかし、これはあまりしっくり来てはいません。もっといい方法はないでしょうか?

また、react-routerを使うと、あるURLにアクセスしたときに、それに対応するComponentがマウントされます。
たとえば、 :code:`/page/:id/` のようなURLにアクセスしたときには、ページの最新情報をアクセスしたタイミングで取得したい場合が多いでしょう。このとき、実装方法がまずいと、まずStoreに残っている古いデータが表示され、最新情報のフェッチが完了した後に、はじめて最新の情報が表示されるということが起きます。アプリの性質にもよりますが、多くの場合、これはあまり望ましい挙動ではないでしょう。

このような挙動を防ぐためには、フェッチ開始時にデータをクリアする、あるいはフェッチ中はローディング表示するなどして、フェッチ完了語に最新のデータを表示する必要があります。もっともスマートな方法は、どのような方法になるでしょうか。

データフェッチについての見解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Redux Real World Exampleでは、やはりContainer Componentの `マウント時 <https://github.com/reactjs/redux/blob/79e81bffcc41aad4a55c5533915047fe09bebabd/examples/real-world/src/containers/RepoPage.js#L26>`_ にmapDispatchToPropsで渡されたコールバックを呼び出して、フェッチアクションをdispatchしています。筆者の考えた素朴な方法と同様です。
また、古いキャッシュされたデータへの対処については、API用の特殊なMiddlewareを用意して、そこでリクエスト開始・完了に対応した `アクションを発行しています。 <https://github.com/reactjs/redux/blob/79e81bffcc41aad4a55c5533915047fe09bebabd/examples/real-world/src/middleware/api.js#L113>`_ これらのアクションに応じて、isFetchingという状態がON/OFFされるので、そのフラグに応じて表示制御を行っています。独自のMiddlewareを用意している点はじゃっかん風変りですが、 `公式のAsync Actionsというドキュメント <http://redux.js.org/docs/advanced/AsyncActions.html>`_ で紹介されている基本的な方法の変形と考えていいでしょう。

wp-calypsoでも、ほぼ同等の `redux-thunk <https://github.com/gaearon/redux-thunk>`_ を使用した方法を取っている部分がある他、 `非同期通信用のMiddleware <https://github.com/Automattic/wp-calypso/tree/7475c744b951cbe4b44525c2aa93d2708adaeae0/client/state/data-layer>`_ も用意されているようです。

tofinoはブラウザなので若干特殊で、Componentから通常のDOMイベントを監視して、アクションをdispatchしたりしているようで、あまりウェブアプリの参考にはならなさそうです。

redux-ecosystem-linksに載っているアプリではあまり使われていなかったのですが、URLルーティングと同時にデータフェッチするケースをサポートしてくれるライブラリとして、 `redux-async-connect <https://github.com/Rezonans/redux-async-connect>`_ 、 `redux-async-loader <https://github.com/recruit-tech/redux-async-loader>`_ `redux-saga-router <https://github.com/jfairbank/redux-saga-router>`_ 、 `redux-tower <https://github.com/kuy/redux-tower>`_ といったものがあります。redux-async-loaderでは、 `モバイルでページ遷移をしたときに生じる微妙な問題 <https://speakerdeck.com/yoshidan/nodefest2016?slide=17>`_ も適切にハンドリングしてくれるようなので、こういった問題に対処したい場合には必須かもしれません。このライブラリであれば、ライフサイクルイベントの発生をデータフェッチ完了まで遅延させてくれるようなので、ローディング中かどうかの制御も不要になるのかもしれません。

また、詳しくはないのですが、GraphQLを使っている場合は、 `Relay.js <https://facebook.github.io/relay/>`_ のようなライブラリを使うと、サーバーとの接続まで含めてData Componentがケアしてくれるようです。

まとめ
--------

この記事では、Redux Real World Example、Project Tofino、wp-calypsoといった実際のアプリのソースコードを参考に、React Redux開発において生じる疑問へのヒントを探りました。

Storeの構成は、概ね公式ドキュメントの通りにやれば可読性を担保でき、大規模な場合にはDucksパターンを使う、スライス間での状態共有が必要な場合にはreduce-reducersを使う、といったことを見ました。

Storeの初期化データ定義については、Immutable.jsのRecordを利用する方法があることや、ローカルに保存された状態を動的にバリデーションする必要がある場合があることを見ました。また、flowtypeを利用することで問題が解消することについても触れました。

また、Componentの整理について、多数のReact Reduxアプリを見た中で行き着いたファイル構成のスタイルを提案し、プロパティの受け渡しが冗長になってしまう場合の対策をいくつか紹介しました。

最後に、データフェッチについては今回調査した範囲では公式ドキュメントの非同期プラクティスより大きく優れたものは見つからず、かわりにデータフェッチを簡単にしてくれるライブラリをいくつか紹介しました。

参考リンク
-----------

* `Applications and Examples <https://github.com/markerikson/redux-ecosystem-links/blob/master/apps-and-examples.md#applications>`_
* `Container Components <https://medium.com/@learnreact/container-components-c0e67432e005#.lo4csvl0g>`_
* `Presentational and Container Components <https://medium.com/@dan_abramov/smart-and-dumb-components-7ca2f9a7c7d0#.wot8t890i>`_
* `Ducks: Redux Reducer Bundles <https://github.com/erikras/ducks-modular-redux>`_
* `Real World Redux <https://speakerdeck.com/chrisui/real-world-redux>`_
* `React + Reduxを使った大規模商用サービスの開発 <https://www.youtube.com/watch?v=rtmiiNATv84>`_
* `アメブロ2016 ~ React/ReduxでつくるIsomorphic web app ~ <https://developers.cyberagent.co.jp/blog/archives/636/>`_

----

.. raw:: html

  <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />この記事のライセンスは、<a href="http://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>とします。

