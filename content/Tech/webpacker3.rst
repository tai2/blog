Webpacker 3ではじめるRailsエンジニアのためのモダンフロントエンド入門 〜Sprocketsを使わないRailsプロジェクト試案〜
##################################################################################################################

:date: 2017-10-21
:slug: webpacker3
:tags: rails, webpacker, react
:summary: 本記事には2つの目的があります: RailsのAsset pipeline(Sprockets)をまったく使用しなくてもRails開発が可能であることを実証すること、モダンフロントエンド未体験のRailsエンジニアに向けて、実際のコードをまじえつつ、モダンフロントエンド開発の雰囲気を伝えること。また、Webpackerの概要を知りたいRailsエンジニアへの機能と使い方紹介にもなっています。


はじめに
========

  Webpack、ES6風味のJavaScript、そして他すべてのモダンなクライアント側開発体験の進歩をまだ試していないなら、Webpacker 3.0は、はじめるのに絶好の機会だ。

  -- DHH

`Rails 5.1 <http://weblog.rubyonrails.org/2017/4/27/Rails-5-1-final/>`_ で `Webpacker <https://github.com/rails/webpacker>`_ が導入され、Railsでもモダンなフロントエンド開発が簡単にできるようになりました。
Webpackerはリリースからどんどん進化しており、 `3.0でさらに使いやすくなりました。 <https://gist.github.com/tai2/9a72ed78a6227c9bbe046e08f72cdd95>`_

本記事には2つの目的があります:

* RailsのAsset pipeline(Sprockets)をまったく使用しなくてもRails開発が可能であることを実証すること
* モダンフロントエンド未体験のRailsエンジニアに向けて、実際のコードをまじえつつ、モダンフロントエンド開発の雰囲気を伝えること

また、Webpackerの概要を知りたいRailsエンジニアへの機能と使い方紹介にもなっています。

.. contents:: 目次

対象読者
========

Rails自体の基本的な使い方は習得済みのエンジニアのために書きました。
とは言え、Webpacker以外についての説明は、Railsとは無関係に独立して読めるので、たんにモダンフロントエンドに興味がある人にとっても参考になると思います。

サンプルコード
===============

本記事では、以下のサンプルコードを元に解説していきます。[ref]記事内で引用しているコードは、型アノテーションを省略するなど、適宜省略した形で抜粋しています。[/ref]

https://github.com/tai2/webpacker-react-example

Rails 5.1とWebpacker 3を使った簡単なTodoアプリです。
従来通りのRails MVC[ref]ほぼscaffoldingが生成したものそのままです[/ref]とReactの2通りの方法で、同じ機能を実装しているので、
Railsだけで書いていたコードをモダンフロントエンドで実装するとどのようになるのか、比較し易いと思います。

あくまでサンプルコードではありますが、筆者が実際の案件で使うための検証も兼ねており、ほぼこのままの形でプロダクションに投入する予定のコードでもあります。

このサンプルでは以下のことが実現されています:

* Sprocketsを使用せず、webpackerのみでアセットを管理する。
* Reactのクライアントアプリと通常のRails MVCを同一サービスで併用する(いわゆるSPAではない)。
* RailsのViewで使う小粒なJavaScript(いわゆるJS Sprinkles)もwebpackで管理する。
* サーバーAPIリクエストにCSRFプロテクションをかける。
* 静的ファイルのファイル名末尾にハッシュを付与する(いわゆるキャッシュバスター)。
* 通常のViewとReactアプリ両方でBootstrapを使う。
* Reactアプリのスタイル定義は、CSS Modulesで行う。
* JavaScriptは、すべてTypeScriptで記述し、静的型チェックを行う。
* クライアントアプリは、React ReduxによるFluxアーキテクチャで構成する。
* StorybookによるUIコンポーネントの開発。
* power-assertによるシンプルなアサーションAPIでテストを記述する。
* lodashを使うが、tree shakingにより実際に使用している関数のみバンドルする。
* babel-preset-envによる必要最低限のpolyfill。[ref]ただし、現状のUglifyJSでは、ES2015+をサポートしていないため実質的に無効化される。将来的にはUglifyJSが改善されて有効化される見込み。[/ref]

環境構築というのは、個々の要素間の相性などにより、得てして問題が発生し、正しく動作させるために試行錯誤が必要になります。
ですから、これらの要素をすべて詰め込んで、動作する組み合わせを選定し、実際に動作検証をしたというだけで、ひとつの成果と言って過言ではありません。

以降、上記の要素について個々に解説していきます。
ただし、ひとつの記事で、すべてを詳細に解説することは難しいので、できる限りコードを添えつつ簡単な概要と参考リンクを紹介するに留めます。あくまで、コードの雰囲気と便利なツールの紹介が目的です。
また、JavaScriptのエコシステムというのは非常に多用で選択肢が豊富であり、これが正解というのものはありません。
ここで紹介するものも、あくまでひとつの例に過ぎないことに注意してください。[ref]とは言え、紹介しているライブラリ・ツールはどれもJavaScript界で一定の評価を得ているポピュラーなものばかりです。[/ref]

この記事で扱わないもの
======================

昨今のシングルページアプリケーション(SPA)と呼ばれる、JavaScriptのみでUIが構成されるWebアプリでは、
しばしばサーバーサイドレンダリングを行います。
これは、JavaScriptが走る前に、あらかじめサーバー側でHTMLを生成してレスポンスに含めておくことで、
初期表示までの時間を短縮する技術です。
SPAでは、最終的なJavaScriptのサイズが数MB以上になることも珍しくないため、
シビアなパフォーマンスが要求されるサービスでは、このような施策が要求されます。
また、サーバーサイドレンダリングを行うとSEO上も有利になると言われています。
筆者はサーバーサイドレンダリングの経験がないため、この記事では扱いません。

また、アクセスされたURLに応じて、クライアント側で表示内容を変更する、
クライアントサイドルーティングも扱いません。[ref]筆者の案件では使わないため[/ref]

参考リンク
-----------

* `yahoo/fluxible による SPA + Server Rendering の概観 <https://havelog.ayumusato.com/develop/javascript/e675-spa_and_server_rendering_with_fluxible.html>`_
* `You Need to know SSR <https://speakerdeck.com/yosuke_furukawa/you-need-to-know-ssr>`_
* `TypeScript+webpack+Hypernova on RailsでSSRするときの設定ファイル <http://blog.bitjourney.com/entry/2017/09/29/183826>`_

Webpackとは
============

ごくごく最近まで、ブラウザ上のJavaScriptには、モジュール分割のための機能がありませんでした。
そのため、ランタイムに頼らずにモジュール化を行うための手法がいくつも発明されてきました。
その中のひとつが、トランスパイルとバンドル化という手法です。

この手法では、CommonJSやESModuleなどの本来はブラウザ上で使えない(あるいは使えなかった)
仕様を解釈しつつ、それをブラウザが解釈できるソースコードに変換(トランスパイル)します。
また、モジュール機能のないブラウザ上で実行するために、変換したソースコードはすべて
結合してひとつのソースコードにします(バンドル化)。

.. figure:: {filename}/images/webpacker3/webpack.png
   :alt: Webpack

   WebpackはJSアプリのアセットをひとまとめにする

JavaScriptのバンドルツールとしては、 `Rollup <https://rollupjs.org/>`_ や `Fusebox <http://fuse-box.org/>`_ など、いくつものプログラムがありますが、現在もっともポピュラーなのが `Webpack <https://webpack.js.org/>`_ です。

また、バンドル化するときには、同時に、ECMAScript 2017(ES2017)などの最新のJavaScript仕様から、
より広範囲のブラウザで実行できるECMAScript 5(ES5)などにトランスパイルします。
これにより、現在のフロントエンドプログラミングでは、最新の便利な言語機能を使って、以前よりも快適に開発ができます。

Webpackはあくまでバンドル化だけを行うツールであり、トランスパイルは別のツールが行います。
JavaScriptのトランスパイラでもっともポピュラーなのが `Babel <https://babeljs.io/>`_ です。
WebpackとBabel、およびそれらのプラグインを組み合わせることで、単にトランスパイル&バンドル化を行うだけでなく、さまざまなことが行えます。

トランスパイラとしてもうひとつメジャーなのが、 `TypeScript <https://www.typescriptlang.org/index.html>`_ です。こちらは、名前からも分かる通り、静的型チェックの機能を備えつつ、ECMAScriptとほぼ互換性のある文法を持ったべつの言語になっています。

参考リンク
----------

* `最新版で学ぶwebpack 3入門 – JavaScript開発で人気のバンドルツール <https://ics.media/entry/12140>`_

Webpackerとは
=============

`Webpacker <https://github.com/rails/webpacker>`_ は、RailsとWebpackを統合するためのgemおよび、Nodeモジュールです。
これには、以下のような機能が含まれます。

* WebpackでビルドしたアセットをRailsのViewから使用するためのヘルパー
* Webpackのデフォルト設定
* オンデマンドビルド(Railsへのリクエスト時にWebpackを起動)
* React,Vue,Angular,Elmの雛型ジェネレータ

なぜSprocketsを避けるのか
-------------------------

Railsには、もともとSprocketsという、CoffeeScriptやSASSのトランスパイルができる機能が含まれています。
Railsとしては、JavaScriptのコンパイルのみをWebpackerで行い、スタイルシートやその他アセットは従来通りSprockets
から利用するというのが当面の方針のようです。

しかしながら、筆者の見るところ、実はWebpackerにはSprocketsがなくてもそれだけで完結できる十分な機能が備わっています。
[ref]以前であれば、Sprocketsを使わずにWebpackのみでアセットを管理するためには、 `ヘルパなどを自前で実装する必要がありましたが、 <http://engineer.crowdworks.jp/entry/2016/05/24/174511>`_ いまではWebpackerのみで事足ります。[/ref]

だとすると、同一機能を持ったものが2つ存在しているのはDRYではありません。

また、Rails 5.1では、 `Sprockets経由でES2015+の構文を使用することが可能であり、 <https://qiita.com/ryohashimoto/items/aa2a7065abc6a4dcedd1>`_ [ref]ECMAScriptの仕様は、2015以降毎年更新されています。それらを総称して2015+と呼んだりもします。また、2015以前の仕様であるES5と対比する意味で、ES6,ES7,ES8などと呼ばれたりもします。[/ref]npm[ref]Node.jsのパッケージ管理ツール、及びその中央リポジトリ。Rubyで言うところのRubyGems。JavaScriptのエコシステムはnpmを要として発展しています。[/ref]からインストールしたモジュールを使用することさえも可能です。しかし、Sprocketsでは、現状、ESModuleのimportステートメントやCommonJSのrequire関数を解釈することができないため、実際には、利用できるNodeモジュールがかなり制限されています。

ですから、Nodeエコシステムの恩恵をフルに受けられるWebpacker一本でいくほうが良いと判断し、それを実証するためにこの記事を書きました。

デメリットとして、Sprocketsが前提になっているようなgem(Mountable Engineなど)は、利用できなくなると思われます。

ディレクトリ構成
-----------------

Webpackerのデフォルトでは、

* :code:`app/javascript/packs/` 変換元のファイル
* :code:`public/packs/` 変換後のファイル

というディレクトリ構成になっています。
:code:`app/javascript/packs` 内に置かれたすべてのファイルは、自動的に、Webpackのエントリポイントとして扱われます。
つまり、このディレクトリ内にあるファイルはすべて、:code:`public/packs/` に変換後のファイルが出力されるということです。
Webpackerでは、この個々のエントリーポイントをpackと呼びます。

同時に、従来の :code:`app/assets/javascripts` はそのまま残されています。[ref]Webpackerのディレクトリが :code:`app/javascript/` であることには、`明確な意図 <https://github.com/rails/webpacker/pull/2#issuecomment-265611291>`_ が込められているようです。[/ref]
Railsのデフォルトでは、 :code:`app/assets` はアセットパイプラインの管轄であり、ここに置かれているJavaScriptはSprocketsによってビルドされます。

RailsとWebpackerを併用するRailsのデフォルトであれば、この設定で適切なのですが、
我々は、いまSprocketsを捨ててすべてのアセット管理をWebpackerにまかせようとしています。
JavaScript以外のスタイルシート、画像ファイルといったアセット一般をそこに置くとなった場合に、
:code:`app/javascript/` というパスは不適切に思えます。
幸い、この部分は設定ファイルの :code:`source_path` で変更できるため、:code:`app/assets/` に変更します。
pack用のディレクトリは、 :code:`app/assets/packs` で、それ以外は従来のRailsと同じ形になります。
アセットパイプラインの責務をWebpackerに置き換えるので、これがしっくり来ます。

Viewヘルパー
------------

Webpackerでは3つのViewヘルパーが追加されます。

.. code-block:: erb

  <%= javascript_pack_tag 'todos' %>

:code:`javascript_pack_tag` で、packでバンドルされたJavaScriptファイルを出力できます。

.. code-block:: erb

  <%= stylesheet_pack_tag 'todos' %>

:code:`stylesheet_pack_tag` で、packでバンドルされたCSSファイルを出力できます。
スタイルシートのバンドルについては後程説明します。

.. code-block:: erb

  <img class="logo" src="<%= asset_pack_path 'images/rails.svg' %>" />

:code:`asset_pack_path` で、packに含まれるすべてのアセットへのパスを出力できます。
packに画像などのファイルを含める方法については後程説明します。

これらのヘルパーを使用すると、プロダクション環境では、ファイル名に自動的にダイジェストが付加されます。

デフォルトWebpack設定とそのカスタマイズ
---------------------------------------

Webpackの設定ファイルは、それ自身がJavaScriptモジュールであり、設定が記述されたオブジェクトをエクスポートしています。
そしてWebpackerのnpmモジュールは、ReactやSCSSなどの変換が使えるように設定されたWebpackの設定を提供するオブジェクトです。
ただし、厳密にはWebpack設定そのものではなく、カスタマイズがしやすいインターフェイスを備えた独自のオブジェクトになっています。

.. code-block:: javascript

  // Webpackerの設定オブジェクトをインポートする
  const { environment } = require('@rails/webpacker')

  // ここで設定をカスタマイズする

  // Webpackerの独自オブジェクトからWebpack設定オブジェクトに変換しエクスポートする
  module.exports = environment.toWebpackConfig()

Webpackerのオブジェクトで設定できるのは、ローダーとプラグインのみに制限されています。
ローダーは、拡張子ごとの変換を定義し、プラグインは、それ以外の一般的な拡張、たとえばminifyや(トランスパイル対象のコードへの)環境変数の注入などです。この範囲に収まらないカスタマイズがどうしても必要な場合は、 :code:`toWebpackConfig()` した後の生のWebpack設定オブジェクトをいじる必要があります。

ジェネレータ
-------------

Rails 5.1以降では、プロジェクト生成時にReact、Vue.js、Angular、Elmのどれかを選択して雛型を生成することができます。
Reactの場合は以下のようにします。

.. code-block:: bash

  rails new myapp --webpack=react

あるいは、既存のプロジェクト(5.1にアップグレード済みかつwebpacker gem追加済みとする)にwebpacker関連の設定を追加するには、
以下のようにします。

.. code-block:: bash

  ./bin/rails webpacker:install
  ./bin/rails webpacker:install=react

ちなみに、この記事のサンプルプロジェクトは以下のコマンドで生成しました。

.. code-block:: bash

  rails new webpacker-react-example --webpack=react --skip-turbolinks --skip-coffee --skip-sprockets

Webpackerでアセットを管理する
------------------------------

Webpackでは、JavaScript以外の一般のアセット、たとえばPNGやSVGなどのファイルをバンドルに入れるこのが可能です。
そのためには、JavaScriptのソースから、アセットをモジュールとしてインポートする必要があります。

.. code-block:: javascript

  // react.svgをバンドルに追加する
  import reactIcon from 'images/react.svg'

このようにすると :code:`images/react.svg` が最終的な生成物に含まれることになります。
:code:`reactIcon` には、デプロイ後の環境で画像を参照するためのパスが入ります。
:code:`import` の構文自体はES2015+のものですが、画像ファイルなどを対象としてインポートできる機能は、Webpackの独自拡張になります。
こうして、バンドルが依存しているアセットをコードで明示的に表現するのがWebpack流のやりかたです。

本記事では、Railsアプリで使用するすべてのアセットをWebpackerで管理するため、通常のViewから参照する画像などについても、JavaScriptで依存関係を表明しておく必要があります。RailsのViewから使用するすべての画像について個別にインポートするのは現実的ではないので、Webpackの :code:`require.context` という関数を使います。

.. code-block:: javascript

  require.context('images', true, /\.(png|jpg|jpeg|svg)$/)

本サンプルプログラムでは、Webpackerの :code:`source_path` を :code:`app/assets` に変更しているため、このディレクトリにあるファイルは相対パスを使わないで参照ができます。2番目の引数は再帰的に検索することを意味します。従って、上記のコードで、:code:`app/assets/images` 以下のすべての画像ファイルをpackに追加することを意味します。

参考リンク
----------

* `Webpacker 2 → Webpacker 3 移行ログ <https://gist.github.com/tai2/bf284bd00039eabf405049ad42275bd1>`_

rails-ujs
==========

以前jquery-ujsと呼ばれていたものが、いまではjQuery依存を取り除かれ、 `rails-ujs <https://github.com/rails/rails/tree/master/actionview/app/assets/javascripts>`_ になりました。
Sprocketsを使用する場合はとくになにも設定しなくても有効化されていますが、本記事では、アセットパイプラインを使用しないため、JavaScriptのエントリポイントから明示的に :code:`import` する必要があります。

.. code-block:: javascript

  import Rails from 'rails-ujs'

  Rails.start()

これでフォーム処理中のsubmitボタン自動無効化などが有効になります。

CSRFトークンの取得
-------------------

JavaScriptのCSRF保護機能を使うには、rails-ujsでCSRFトークンを取得して、リクエストヘッダに設定します。

.. code-block:: javascript

  import { csrfToken } from 'rails-ujs'

  request
    .post('/todos.json')
    .set('X-CSRF-Token', csrfToken())

上記コードでは、XHR APIをラップした `superagent <https://github.com/visionmedia/superagent>`_ を使っています。

なお、RailsのViewに :code:`csrf_meta_tags` を挿入しておく必要があります。

.. code-block:: erb

  <%= csrf_meta_tags %>

React
=====

昨今のフロントエンド開発では、Virtual DOMなどの仕組みに基いた、宣言的にHTMLを記述できるViewライブラリ群が隆盛を極めています。
その中でもとりわけ人気があるのがfacebookの開発している `React <https://reactjs.org/>`_ です。React自体はただのViewライブラリであり、APIも非常にシンプルでなにも難しいことはありません。

以下に、サンプルコードから、Reactのコンポーネント[ref]ReactではViewの構成単位をコンポーネントと呼びます。[/ref]定義の一例を挙げます。

.. code-block:: jsx

  import TodoItem from '../TodoItem'

  function TodoList(props) {
    return (
      <table className="table">
        <thead>
          <tr>
            <th>Content</th>
            <th>Due date</th>
            <th />
          </tr>
        </thead>
        <tbody>{props.todos.map(id => <TodoItem key={id} id={id} />)}</tbody>
      </table>
    )
  }

Reactのコンポーネント描画関数では、Propsと呼ばれる入力パラメータを表すオブジェクトを外部から受け取って、JSXというXMLライクな記法で記述される要素を返します。上記では、todosという配列を受け取って、その各要素を別のコンポーネントに変換しています。
JSXは、HTMLとほぼ互換性があるので、HTMLの知識がそのまま流用できます。[ref]例にもある用に、一部、 :code:`class` のようなJavaScriptの予約語は使えないため、 :code:`className` のように別のキーワードに置き換えられています。[/ref]
与えられるPropsが変化すれば、それに応じて表示内容も変化します。

上記のコンポーネントでは、 :code:`<TodoItem>` という大文字で始まる見慣れないタグが使われています。[ref]DOM標準以外のコンポーネントは大文字で始まる必要があります。[/ref]これは、アプリケーションで独自に定義したコンポーネントです。HTML標準以外のファイル外部で定義されたタグは、必ずJavaScriptモジュールとして :code:`import` する必要があります。Reactプログラミングでは、こうして独自に定義したコンポーネントを組み合わせてViewツリーを構築していきます。
また、見ての通りただのJavaScriptの関数なので、:code:`if` や :code:`for` などすべてのJavaScript構文を使えます。

エントリポイントは、以下のようになります。

.. code-block:: jsx

  // #todo-appの要素を検索し、その子要素としてAppコンポーネントをレンダリングする
  ReactDOM.render(
    <App />,
    document.getElementById('todo-app')
  )

これだけ見ると、どこからもPropsを注入していないし、Propsが与えられたとしても変化する余地がないのでインタラクティブなアプリを作れないと思われるかもしれません。どのように状態を扱うかについては、次節で説明します。

乱暴に言ってしまえば、Reactはただのテンプレートです。ただし、Virtual DOMのおかげで、複雑なViewをリアルタイムに書き換えても高速に描画されます。これとよく比較されるものとして、jQueryのようなユーティリティーでDOMの部分部分を手続き的に書き換える旧来の手法があります。
Reactベースのアプリ開発では、宣言的な言語で平易に記述できることや、モジュールシステムのおかげで依存関係が明確化されることで、格段にメンテナンス性が高まります。

参考リンク
-----------

* `Reactアハ体験 <https://qiita.com/ossan-engineer/items/66feec268f9c4e582bb6>`_ Reactへの理解を深められます

FluxアーキテクチャとRedux
==========================

前節では紹介しませんでしたが、Reactにも状態を扱う機能はあります。これを使って、クリックなどのイベントに応じてなどインタラクティブに状態を変化させることも可能です。しかし、コンポーネント間でのデータの受け渡し方法は(基本的には)Propsしかないため、アプリの複雑な状態管理をこれだけで行うのは、不可能とは言わないまでも少々心許無いところです。

Reactの世界では、状態を管理するための手法として、 `Flux <https://facebook.github.io/flux/docs/overview.html>`_ というアーキテクチャが発展してきました。
Fluxライブラリにおいても、例によって激しい競争が行われましたが、これを生き残って今現在一強状態にあるのが `Redux <http://redux.js.org/>`_ です。

Reduxでは、アプリのほぼすべての状態[ref]コンポーネント自身が状態を管理することもあるが、基本はストアに格納する[/ref]をストアに格納します。
ストアは、言わば巨大なグローバル変数であり、それは基本的にはJSONシリアライズ可能なJavaScriptのオブジェクトです。[ref]実際にはJSONシリアライズできないオブジェクトを格納することも可能で、それが必要な場合もあるが(FileやBlobなど)、そうするといくつかのReduxの恩恵を受けられなくなる[/ref]
Reduxでのデータの流れは次の図のようになります。

.. figure:: {filename}/images/webpacker3/redux.png
   :alt: Redux

   Reduxにおけるデータの流れ

アプリ内でのユーザーの操作は、アクションと呼ばれるプレーンなJavaScriptオブジェクトで表現されます。
アクションがコンポーネントから送出されると、Reducerと呼ばれる関数が呼ばれます。
これは、現在のストア状態とアクションを受けて、次のストア状態を返す関数です。
ストアの状態変更は、必ずこのReducerを経由します。
ストアと接続されたコンポーネントはその状態を監視しているので、Reducerによって変更された状態は、コンポーネントに通知されます。
このように、データの流れが一方向に循環することから、Fluxは、一方向データフローであると言われます。

.. code-block:: javascript

  // Reducerは、受け取ったアクションに応じて、新しいストア状態を返す。
  // これによりストアが更新される。
  function appReducer(state, action) {
    switch (action.type) {
      case actions.SELECT_ORDER:
	return {
	  ...state,
	  sortBy: action.payload.sortBy,
	  sortOrder: action.payload.sortOrder,
	}
      case actions.TOGGLE_DONE_FILTER:
        return {
          ...state,
          doneFilter: !state.doneFilter,
        }
      // ... 中略
      default
        return state
    }
  }

  // react-reduxのconnect関数によって、コンポーネントとストアが接続される。
  connect(
    // 1番目の引数でコンポーネントにストアの状態を渡し、
    (state) => ({
      sortBy: state.app.sortBy,
      sortOrder: state.app.sortOrder,
      doneFilter: state.app.doneFilter,
    }),

    // 2番目の引数でコンポーネントのコールバックを定義し、そこでアクションを送出する
    (dispatch) => ({
      onOrderChange(ev) {
        const [prop, order] = ev.currentTarget.value.split('-')
        dispatch({ type: SELECT_ORDER, payload: { sortBy, sortOrder } })
      },
      onDoneFilterChange() {
        dispatch({ type: TOGGLE_DONE_FILTER })
      },
    })
  )(TodoConditions)

Reduxを使用することで次のようなメリットが得られます。

* 状態を必要とするコンポーネントがストアと接続されることで、

  * コンポーネント自身が状態を持つ必要がなくなり、
  * Propsのバケツリレーも不要になる。

* react-reduxの提供する最適化機能により、不要なレンダリングを回避できる(パフォーマンス向上)

また、アプリ内で起きたイベントが、Actionのシーケンスとして表現されるため、DX向上にも活用できます。
たとえば、 `Chrome拡張 <https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=en>`_ を導入すれば、次のスクリーンショットのようにアクションのログをブラウザ内で見ることができます。

.. figure:: {filename}/images/webpacker3/redux-devtools.png
   :alt: redux-devtools-extention

   Chrome拡張でアクションログが確認できる


非同期の扱い
-------------

Reducerもコンポーネントもなんらかの値を受け取って、即時に値を返すただの関数であるため、
実は、前節までに紹介した枠組みのままでは、HTTPリクエストのような非同期な処理を実行する余地がありません。

Reduxでは、ミドルウェアと呼ばれる拡張機構が用意されており、非同期な処理はここで取り扱います。
非同期処理を扱うミドルウェアは、 `redux-thunk <https://github.com/gaearon/redux-thunk>`_ 、 `redux-promise <https://github.com/acdlite/redux-promise>`_ 、 `redux-api-middleware <https://github.com/agraboso/redux-api-middleware>`_ などさまざまな
ものがあり、しばしば論争の種になったりもしますが、筆者は `redux-saga <https://redux-saga.js.org/>`_ というライブラリを使用しています。

.. figure:: {filename}/images/webpacker3/redux-with-async.png
   :alt: Redux with async

   Reduxにおけるデータの流れ(非同期版)

redux-sagaでは、sagaと呼ばれる、reduxの通常の枠組みとは別の一種の外部環境を設け、
その中でアプリに関するすべての非同期な処理を扱います。
これは、Actionを受け取り、非同期処理を実行した結果として別のActionを送出する、
Aciton-Action変換として解釈できます。

Reduxの通常の枠組みをそのまま残しつつ、[ref]redux-thunkやredux-promiseでは、アクションの定義を拡張します。これらを使った場合、Actionはもはや、ただのオブジェクトではありません。[/ref]自然に非同期を取り入れることができるというのが、
筆者がredux-sagaを採用する理由です。
redux-sagaに非常に高機能な非同期処理のためのユーティリティー群が含まれますが、典型的なユースケースではその中のごく一部があれば十分です。

.. code-block:: javascript

  // Todo項目追加時のsaga
  // ADD_TODO_REQUESTEDアクションを受け取り、APiを呼び出して、
  // ADD_TODO_RECEIVEDアクションを送出する
  function* addTodoRequested(action: actions.AddTodoRequested) {
    try {
      const { requestId, item: { content, dueDate } } = action.payload
      const item = yield call(webApi.addTodo, content, dueDate, false)
      yield put(actions.addTodoReceived({ requestId, item }))
    } catch (error) {
      yield put(
        actions.addTodoReceived(
          new IdentifiableError(SINGLETON_ID, error.message)
        )
      )
    }
  }

sagaはジェネレータ関数で定義されるため非同期処理を逐次処理のように記述できます。
これもsagaの大きな魅力です。

RailsからReduxへのデータ受け渡し
--------------------------------

RailsからReact Reduxアプリにデータを受け渡すには、Viewの中でデータ格納用の要素を用意し、属性としてJSON化した文字列を格納します。

.. code-block:: erb

  <%= content_tag :div,
    id: 'todos-data',
    data: {
      todos: @todos
    }.to_json do %>
  <% end %>

クライアント側からは、この文字列を取り出してパースした上で使用します。
Reduxの `ストア作成関数 <http://redux.js.org/docs/api/createStore.html>`_ には、2番目の引数として初期値を指定できるため、これで、
アプリの初期状態をサーバー側から制御できます。

.. code-block:: javascript

  function getPreloadedState() {
    const node = document.getElementById('todos-data')!
    return convert(JSON.parse(node.getAttribute('data')))
  }

  document.addEventListener('DOMContentLoaded', () => {
    // createAppStoreは、ストア作成用にアプリ内で定義しているヘルパー
    store = createAppStore(getPreloadedState())
    render(App)
  })

参考リンク
-----------

* `Microsoft/TypeScript-React-Starter <https://github.com/Microsoft/TypeScript-React-Starter>`_ TypeScriptでReact Reduxを型付けをしているサンプルコード
* `Typesafe Container Components with React-Redux’s Connect and TypeScript <https://spin.atomicobject.com/2017/04/20/typesafe-container-components/>`_ TypeScriptでReact Reduxを型付けするやりかた
* `Redux & Typescript typed Actions with less keystrokes <https://medium.com/@martin_hotell/redux-typescript-typed-actions-with-less-keystrokes-d984063901d>`_ ReduxのアクションをTypeScriptでスマートに型付けする方法
* `redux-sagaで非同期処理と戦う <https://qiita.com/kuy/items/716affc808ebb3e1e8ac>`_ redux-sagaの日本一詳しい説明
* `Using Redux DevTools in production <https://medium.com/@zalmoxis/using-redux-devtools-in-production-4c5b56c5600f>`_ Redux DevToolsをプロダクション環境で使うことのメリット

CSS Modules
============

コンポーネント指向の昨今のフロントエンドアプリ開発においては、CSSにも変革が起きています。
そのひとつが、 `CSS Modules <https://github.com/css-modules/css-modules>`_ です。
CSSでは、しばしばセレクタの詳細度が問題になり、
スタイル設計において問題を起こさないための技法として、 `BEM <http://getbem.com/>`_ のような技法が発展してきました。

CSS Modulesでは、コンポーネントごとに専用のCSSファイルを定義します。
そこでは、ファイル(モジュール)が固有の名前空間を持つため、クラス名の衝突が原理的に発生しません。
そのため、BEMのような技法を使わずとも自然と詳細度が1になります。

.. code-block:: css

  /* styles.scss */
  .logo {
    width: 100px;
  }

.. code-block:: jsx

  import styles from './styles.scss'

  function App({ todos }) {
    return (
      <div>
        <img className={styles.logo} src={reactIcon} alt="react icon" />
        <TodoConditions />
        <TodoList todos={todos} />
        <TodoAddForm />
      </div>
    )
  }

スタイルシートがコンポーネントに属すことは :code:`import` によってコードで明示
されます。
例えば、上記コードの :code:`.logo` クラスは、CSS Modulesでなければ、:code:`.App .logo` のように入れ子のセレクタになっていたかもしれません。
しかし、これでは詳細度が2に上がってしまい柔軟性が下がります。BEMライクであれば、 :code:`.App__logo` のようになるのでしょうが、やや煩雑です。
我々にはCSS Modulesがあるので、いまやクラス名は、安全なままに、短く明確です。

なお、CSS Modulesとは別に、 `CSSinJS <http://cssinjs.org/>`_ という、スタイルをJavaScriptのコードで直接記述するアプローチもあります。

グローバルなクラスとBootstrap
------------------------------

一方で、通常のRailsのViewからCSS Modulesを利用することはできません。
そのためReactコンポーネントと一対一で定義するスタイルシート以外に、グローバルなスタイルシートが必要になります。

サンプルコードでは、Rails View用のpackをひとつ用意し、そこからグローバルに使用するスタイルシートを取り込んでいます。

.. code-block:: css

  @import '~bootstrap/dist/css/bootstrap';
  @import '~bootstrap/dist/css/bootstrap-theme';
  @import '~stylesheets/scaffold';
  @import '~stylesheets/react-datetime';

  .check {
    width: 1em;
  }

  .logo {
    width: 100px;
  }

このようなスタイルシートを含むpackをレイアウトファイルで取り込んでいます。
Bootstrapもインポートしているため、アプリケーション全体で利用できます。

.. code-block:: erb

  <!DOCTYPE html>
  <html>
    <head>
      <title>WebpakcerReactExampl</title>
      <%= csrf_meta_tags %>

      <%# 'app'は グローバルアセットのためのpack %>
      <%= javascript_pack_tag 'app' %>
      <%= stylesheet_pack_tag 'app' %>
      <%= yield :head %>
    </head>

    <body>
      <div class="container">
        <%= yield %>
      </div>
    </body>
  </html>

グローバルなアセットはクライアントアプリとも共有されるため、
Reactアプリからも同様にBootstrapのクラスを利用できます。

.. code-block:: jsx

  function EditButton({ className = '', disabled = false, onClick }) {
    return (
      <button
        type="button"
        className={classNames('btn btn-default btn-xs', className)}
        disabled={disabled}
        aria-label="Edit"
        onClick={onClick}
      >
        <span className="glyphicon glyphicon-edit" aria-hidden="true" />
      </button>
    )
  }

CSS ModulesとグローバルCSSを両立するためのWebpack設定
-----------------------------------------------------

Webpackerの提供するデフォルトの設定では、CSS Modulesは有効にはなっていません。
`ドキュメント <https://github.com/rails/webpacker/blob/master/docs/webpack.md#overriding-loader-options-in-webpack-3-for-css-modules-etc>`_ でCSS Modulesを有効化する方法は紹介されていますが、:code:`.scss` 拡張子に対するローダーは1つしかなく、その設定を変更してしまっているため、今度はグローバルなCSSが使えなくなります。

本記事のサンプルアプリでは、スタイルシート用のローダを2つ用意した上で、:code:`node_modules` と :code:`app/assets/stylesheets` に置かれているスタイルシートはグローバル、それ以外はCSS Modulesとして、ディレクトリによって設定を分けています。

.. code-block:: javascript

  const globalStylePaths = [
    resolve('app/assets/stylesheets'),
    resolve('node_modules')
  ]

  function enableCssModules(cssLoader) {
    const cssModuleOptions = {
      modules: true,
      sourceMap: true,
      localIdentName: '[name]__[local]___[hash:base64:5]'
    }
    cssLoader.options = merge(cssLoader.options, cssModuleOptions)
  }

  // デフォルトのstyleローダーは、app/assets/stylesheetsとnode_modulesに限定
  const styleLoader = environment.loaders.get('style')
  styleLoader.include = globalStylePaths

  // styleローダーをコピーしつつ、上記で限定された以外のパスは、CSS Modulesを有効化
  delete require.cache[require.resolve('@rails/webpacker/package/loaders/style')]
  const moduleStyleLoader = require('@rails/webpacker/package/loaders/style')
  moduleStyleLoader.exclude = globalStylePaths
  enableCssModules(moduleStyleLoader.use.find(el => el.loader === 'css-loader'))
  environment.loaders.set('moduleStyle', moduleStyleLoader)

参考リンク
----------

* `CSSモジュール ― 明るい未来へようこそ <http://postd.cc/css-modules/>`_ CSS Modulesの魅力がわかりやすく書いてある記事

TypeScript
==========

近年のJavaScript界では、静的型チェックの実施がますます普通のことになってきています。
取り得る選択肢は2つ、TypeScriptと `flowtype <https://flow.org/>`_ です。
どちらも素のJavaScriptとほぼ機能的な互換を保ちつつ、静的型付けのために文法を拡張しています。
型システム自体もかかなり似ており、どちらも構造的部分型がベースになっています。

TypeScriptは、ES5などの下位バージョンへのトランスパイラも兼ねていますが、
flowtypeは、純粋に型付けのためのツールという立ち位置になっています。
また、どちらも第三者が作った型付けされていないモジュールに、後付けで型を定義できる仕組みを持っており、
そのための中央リポジトリを持っている点も同じです。

TypeScriptとflowtypeどちらにするかは、非常に悩ましい選択なのですが、
redux-sagaなどの依存しているライブラリが、公式に型定義を提供しているという理由から、
TypeScriptを選択しました。[ref]redux-sagaの型定義も中央リポジトリにあるにはあるのですが、バージョンアップに追随できていないのが現状です。また、redux-sagaとflowtypeについての筆者の理解度が低いために、自分で型定義を書くことはあきらめました。[/ref]

型チェックから受けられる恩恵は非常に大きなもので、コードが満たすべき性質を記述することで、かなりのプログラミングエラーを未然に防いでくれます。個人的に、型チェックなしの環境でプログラミングしていると、Reducerでのプログラミングエラーがしばしば発生し、デバッグに時間を取られていたのですが、これがかなり改善されたと思います。以下は型付けされたReducerの抜粋です。

.. code-block:: javascript

  interface TodoMap {
    readonly [id: number]: Readonly<Todo>
  }

  interface TodosState {
    readonly byId: TodoMap
    readonly ids: number[]
  }

  function addTodoReceived(state: TodosState, action: actions.AddTodoReceived) {
    if (action.payload instanceof Error) {
      return state
    }

    const newTodo = action.payload.item

    return {
      ...state,
      byId: {
        ...state.byId,
        [newTodo.id]: newTodo,
      },
      ids: [...state.ids, newTodo.id],
    }
  }

  function todosReducer(
    state: TodosState = initialTodosState,
    action: actions.Action
  ): TodosState {
    switch (action.type) {
      case actions.ADD_TODO_RECEIVED:
        return addTodoReceived(state, action)
      // ... 中略
      default:
        return state
    }
  }

引数に型指定(:code:`:` の右側)が付いている点に注意してください。
これにより、たとえば :code:`state` に存在しないプロパティーを参照しようとすると、コンパイルエラーになります。

また、:code:`TodoState` でストアの形が型で定義されているため、
あらかじめ定義されたストアの形状と異なる状態を作ってしまうことが原理的に発生しなくなります。

ReduxのReducerは純粋関数である必要があります。もし、新しい状態オブジェクトを返すのではなく、:code:`state` 引数を直接書き換えて返してしまうと、コンポーネントの描画が更新されないという不具合が起きます。
上記定義では、ストアのプロパティーに :code:`readonly` 修飾子が付いているため、そもそも書き換えることができません。

小粒なJavaScript(Sprinkles)
----------------------------

現状、JavaScriptをSprocketsでビルドする場合、Webpackを通らないため、:code:`import` ステートメントは使えませんし、TypeScriptを使うこともできません。
本記事の方式であれば、すべてのJavaScriptはWebpackを通るため、Viewの中で使用するいわゆる小粒なJavaScriptでさえも、モダン環境の恩恵をフルに受けられます。以下はその例です。TypeScriptで記述され、:code:`import` ステートメントを使用しています。

.. code-block:: typescript

  // セレクトボックスの状態に応じてページURLを変更する小粒なJavaScript
  import * as queryString from 'query-string'

  function prepereSelectElems(): void {
    const doms = document.querySelectorAll(
      'select[data-change-query]'
    ) as NodeListOf<HTMLSelectElement>
    const query = queryString.parse(location.search)

    for (const select of doms) {
      if (query.sort_by) {
        select.value = query.sort_by
      }
      select.addEventListener('change', () => {
        query.sort_by = select.value
        location.search = `?${queryString.stringify(query)}`
      })
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    prepereSelectElems()
  })

参考リンク
----------

* `Revised Revised 型の国のTypeScript <http://typescript.ninja/typescript-in-definitelyland/>`_ 日本語で書かれたTypeScriptの解説書。
* `TypeScript(Webpack公式ページ) <https://webpack.js.org/guides/typescript/>`_ TypeScriptのためのWebpack設定。アセット用の型定義についても言及されている。
* `Tree-shaking example with Typescript and Webpack <https://github.com/blacksonic/typescript-webpack-tree-shaking>`_ TypeScript + WebpackでのTree-shakingのサンプル。
* `Tree shake Lodash with Webpack, Jest and Typescript <https://medium.com/@martin_hotell/tree-shake-lodash-with-webpack-jest-and-typescript-2734fa13b5cd>`_ TypeScript + Webpackでlodashをtree shakingする方法

BabelとES2015+
===============

ES5へのトランスパイルにTypeScriptを使用しない場合の選択肢が、Babelを使ったトランスパイルです。
こちらはプラグイン形式になっており、TypeScriptよりも幅広いカスタマイズが可能です。

筆者は、TypeScriptをES5へのトランスパイラとしては使わず単なる型チェッカーとして使っています。
そのため、TypeScriptにはECMAScriptの最新仕様でコードを出力させ、そこからさらにBabelでのトランスパイルを行います。

構成の複雑さが増すというデメリットがある一方、このようにすることで、次のようなメリットが受けられます:

* `babel-preset-env <https://github.com/babel/babel-preset-env>`_ によって、現在のブラウザの実装状況に応じて必要最低限のpolyfill[ref]ブラウザ実装の足りない部分を補うために、その実装を自分のコードに含めること[/ref]と変換を行うことができる。
* Webpackのtree shaking[ref]未使用のコードを除去してバンドルサイズを縮小すること[/ref]で、classも除去できる(Babelを通さない場合、classはそのまま残る)
* `babel-plugin-lodash <https://github.com/lodash/babel-plugin-lodash>`_ [ref]lodashは、JavaScript使いに人気のあるユーティリティーライブラリです。すべての関数をバンドルに入れると、かなりのサイズになります。[/ref]で、めんどうな手続きなしに、最低限の `lodash <https://lodash.com/>`_ 関数だけをバンドルに入れることができる。[ref]ただし、Webpack 4からはtree shakingが強化されてTypeScriptでも同様の効果を得られる模様[/ref]
* React Componentの `Hot Loading <https://github.com/gaearon/react-hot-loader>`_ が、Babelを使わない場合よりもすこし機能アップする。

Babelを通すかどうかについては、非常に迷ったのですが、将来的にもBabelを通したほうが多くのメリットを得られるであろうと考え、こちらに賭けることにしました。ただし、実際には設定の変更だけでソースコードはそのままでいいはずなので、後でBabelをはずすのは、おそらく簡単なはずです。

なお、Webpackerのデフォルト設定では、 `babel-polyfillが組込まれていない <import "babel-polyfill">`_ ため、エントリーポイントで、

.. code-block:: javascript

  import 'babel-polyfill'

する必要があります。

参考リンク
----------

* `ECMAScript 6 — New Features: Overview & Comparison <http://es6-features.org/>`_ ES6の新機能が短いコード例で紹介されており、短時間でキャッチアップできます。
* `Modern JavaScript Cheatsheet <https://github.com/mbeaudru/modern-js-cheatsheet>`_

Storybook
==========

`Storybook <https://storybook.js.org/>`_ は、プロトタイピング、ビジュアルTDD、デザイナーとの協業など、さまざまな可能性を秘めたツールです。
これをを使うと、Reactコンポーネントを状態ごとにカタログとして一覧表示できます。

.. figure:: {filename}/images/webpacker3/storybook.png
   :alt: Storybook

   Storybookによるコンポーネントの表示

Storybookでは、コンポーネントごとにstoriesと呼ばれる一連の状態定義を行います。
これは、以下のようにさながらユニットテストのような見た目をした[ref]入力値のパターンを列挙しつつ対象コードを実行するという意味で[/ref]コードになっています。

.. code-block:: jsx

  storiesOf('TodoAddForm', module)
    .add('typical', () => (
      <TodoAddForm
        addTodoRequest={succeededRequest}
        onAddTodo={action('added')}
      />
    ))
    .add('while adding', () => (
      <TodoAddForm addTodoRequest={loadingRequest} onAddTodo={action('added')} />
    ))
    .add('adding error', () => (
      <TodoAddForm addTodoRequest={errorRequest} onAddTodo={action('added')} />
    ))

ユニットテスト
===============

JavaScriptでのテストフレームワークは、`Mocha <https://mochajs.org/>`_ 、`Jasmine <https://jasmine.github.io/>`_ 、`Ava <https://github.com/avajs/ava-docs/blob/master/ja_JP/readme.md>`_ 、`Jest <http://facebook.github.io/jest/ja/>`_ などの選択肢があります。
[ref]筆者もあまり詳しいわけではないので、たぶん他にもいろいろあると思います。[/ref]

個人的には、アーキテクチャが洗練されていて並列実行に対応していたり、後述のpower-assertベース
でアサーションAPIが簡単なAvaを使いたかったのですが、
残念ながら現段階では `トランスパイラのサポートがまだ弱く、 <https://github.com/avajs/ava/blob/master/docs/specs/001%20-%20Improving%20language%20support.md#typescript-projects>`_ TypeScriptのコードをテストするのは厳しそうだっったため、
Mochaを選択しました。

power-assert
------------

`power-assert <https://github.com/power-assert-js/power-assert>`_ を使うと、Node.jsの標準アサーションAPIを使いつつ、テスト失敗時に結果をわかりやすく表示できます。
アサーションAPIは厳選されており、多数の細分化されたアサーションAPIの使い分けに頭を悩ますことなく、テスト対象という本質にフォーカスできます。

.. figure:: {filename}/images/webpacker3/power-assert.png
   :alt: power-assert

   power-assertを使えば式のどこが期待と異なるのか一目瞭然

サンプルコードでは、Mocha上でTypeScriptのコードをテストするために、 `espower-typescript <https://github.com/power-assert-js/espower-typescript>`_ を使いました。
これを使うと、テスト時にテストコードとテスト対象両方の自動的なトランスパイルが可能になります。
なお、ブラウザ向けビルドと異なり、テストコード自体は、Babelを通さずに直接実行されるため、
TypeScriptの設定ファイルをターゲットに応じて分けています。

Enzyme
-------

Reactコンポーネントのユニットテストには `Enzyme <http://airbnb.io/enzyme/>`_ を使用します。

.. code-block:: jsx

  describe('<TodoAddForm />', () => {
    describe('display errors', () => {
      context('when request failed', () => {
        it('should render error message', () => {
          const request = { requesting: false, error: new Error('error') }
          const wrapper = enzyme.shallow(
            <TodoAddForm addTodoRequest={request} onAddTodo={_.noop} />
          )
          assert(wrapper.find('.error').exists())
        })
      })
    })
  })

このようにテスト内にJSXでコンポーネントを直接記述する形になります。
Viewのテストは壊れやすくなりがちで難しい面がありますが、ReactでTDDを実践したい人などには
便利かもしれません。

参考リンク
----------

* `Unit testing node applications with TypeScript — using mocha and chai <https://journal.artfuldev.com/unit-testing-node-applications-with-typescript-using-mocha-and-chai-384ef05f32b2>`_ TypeScriptのコードをMochaでテストする方法。

Prettier
========

`Prettier <https://github.com/prettier/prettier>`_ はコードの自動フォーマッタです。TypeScriptやSCSSにも対応しています。
自動的にコーディングにある程度の一貫性が得られるのでたいへんありがたいです。

TSLint
======

`TSLint <https://palantir.github.io/tslint/>`_ は、TypeScript用の静的解析ツールです。
Prettierと重複する部分がありますが、こちらはコーディングスタイル以外にもコーディングエラーを発見してくれたりします。
TypeScriptとPretteirを導入している環境だと相対的な重要度は低いと言えますが、コストゼロでメリットが得られるので導入しています。

webpack-bundle-analyzer
========================

冒頭でも書きましたが、webpackを通してバンドル化すると、ちょっとしたアプリでもすぐにJavaScriptが数MBを越えます。
ファイルサイズは、アプリのロード時間に直結するため重要です。
`webpacker-bundle-analyzer <https://github.com/webpack-contrib/webpack-bundle-analyzer>`_ というプラグインを使えば、
以下の画像のようにバンドルサイズの内訳をグラフィカルに表示できるので、最適化のための方針が立てやすくなります。

.. figure:: {filename}/images/webpacker3/webpacker-bundle-analyzer.png
   :alt: webpacker-bundle-analyzer

   webpacker-bundle-analyzerによる解析結果

まとめ
======

この記事では、まず、Webpacker 3を使って構築したサンプルアプリを元にしつつ、Webpackerの基本的な機能と使い方を説明しました。
同時に、Sprocketsを使用しなくともRailsアプリが成立することを説明し、そのための設定を紹介しました。

後半では、React Reduxをはじめとして、モダンフロントエンド開発で使用されている便利なライブラリやツールを簡単に紹介しました。
また、CSS Modulesの組込についてはとくに注意が必要なため、設定方法を紹介しました。Babelの節では、TypeScriptとBabelを併用することで得られるささいなメリットについても説明しました。
