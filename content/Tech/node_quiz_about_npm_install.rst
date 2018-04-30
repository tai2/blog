Node.jsクイズ第58問 ./node_modules直下にはどのパッケージが入る?
################################################################

:date: 2018-5-1
:slug: node-quiz-about-npm-install

.. contents:: 目次

バッケージの集合をまとめるためのパッケージを作りたい
=====================================================

アプリに必要なプラグイン群への依存を別パッケージにまとめて記述しておいて、アプリはそのパッケージに依存するようにすれば便利ではないでしょうか?

.. figure:: {filename}/images/node_quiz_about_npm_install/meta-package.png
   :alt: Meta package

   npmでこのようなメタパッケージを実現したい

パッケージの依存関係をまとめるだけの、メタパッケージのようなものです。
そうすれば、アプリ自体のpackage.jsonは短くなるし、メタパッケージに必要なプラグインの選定を `オマカセ <http://david.heinemeierhansson.com/2012/rails-is-omakase.html>`_ できます。

しかし、Node.jsのパッケージシステム(npmとyarn)で、このようなことをやろうとすべきではありません。
このことは、以下の問題を考えることで理解できます。

問題
======

以下のようなパッケージの依存関係があるとします。

.. figure:: {filename}/images/node_quiz_about_npm_install/dependencies.png
   :alt: Package dependencies

   パッケージの依存関係

モジュールA, B, C, D\@1.0, D\@2.0があり、

* A -> B (devDependencies)
* B -> D\@2.0 (dependencies)
* A -> C (dependencies)
* C -> D\@1.0 (dependencies)

という依存関係です。

このとき、 Aのpackage.jsonがあるディレクトリで :code:`npm install` を実行すると、ローカルのnode_modules直下にはどのパッケージが配置されるでしょうか。
また、 :code:`npm install --production` ではどうでしょうか?
(ただし、Aへのモジュール追加操作は、まずBを追加して、次にCの追加が行われるものとします。)

これを知るためには、Nodo.jsのモジュール検索アルゴリズムと、npm(yarn)のインストールアルゴリズムを理解する必要があります。

Nodeモジュールの検索アルゴリズム
=================================

/Users/tai2/my-node-app/node_modules/some-node-module/foo.js から :code:`require('bar')` したときには、
以下のような順番で対象モジュールの検索が行われます

1. /Users/tai2/my-node-app/node_modules/some-node-module/node_modules/bar
2. /Users/tai2/my-node-app/node_modules/bar
3. /Users/tai2/node_modules/bar
4. /Users/node_modules/bar
5. /node_modules/bar

.. figure:: {filename}/images/node_quiz_about_npm_install/require-algorithm.png
   :alt: Node's module search algorithm

   Node.jsのモジュール検索アルゴリズム

このように、requireしているファイルのあるディレクトリから、ルートディレクトリまで順番に駆け上がっていく形で、node_modules内にあるモジュールを探します。ただし、ディレクトリ名がnode_modulesの場合は、その下のnode_modules(つまりnode_modules/node_modules)は検索対象になりません。

参考: `Loading from node_modules Folders <https://nodejs.org/api/modules.html#modules_loading_from_node_modules_folders>`_

npm installのアルゴリズム
===========================

npm installでnode_modulesにパッケージを配置するときのアルゴリズムは、上記の検索アルゴリズムが前提になっています。
node_modules下の依存パッケージ内に、さらにnode_modulesディレクトリが配置され、その中に依存の依存が配置され、
さらにその下にもnode_modulesと依存の依存の依存が配置され・・・というようなツリー構造になります。

ただし、それを素朴にやると重複するパッケージが配置されてディスク容量が無駄なってしまうため、基本的には、なるべく上の階層にパッケージを配置します。
さきほど説明したように、requireの検索アルゴリズムは、ルートに向かって駆け上がってくれるので、上の階層に置くことで自然と共通化できます。

依存パッケージのインストール時に、すでに同名のパッケージの別バージョンがnode_modules内にある場合には、その下の階層のnode_modulesにインストールします。
その下の階層にもインストールできない場合にはさらに下というふうに、最終的には、依存パッケージ自身のプライベートなnode_modulesまで下る可能性があります。

参考: `npm-install <https://docs.npmjs.com/cli/install#algorithm>`_ , `npm-folders <https://docs.npmjs.com/files/folders#cycles-conflicts-and-folder-parsimony>`_

yarnとnpmはinstallアルゴリズムが異なる
========================================

yarnとnpmではアルゴリズムが微妙に異なります。
npmでは、 :code:`npm install <package-name>` を実行した時点でのnode_modulesツリーの状態を見て、インストール先を決定します。
つまり、 :code:`npm install <package-name>` を実行する順番によってレイアウトが変わるのです!

yarnでは、現在のディレクトリツリーに関係なく常に同じレイアウトになります。パッケージを追加する順序に依存しません。
言いかえると、yarnでは、 :code:`yarn add` を実行するごとに、node_modules内でサブツリーが上位階層に移動したり、別のサブツリーに付け替えられたりします。

参考: `Yarn: A new package manager for JavaScript <https://code.facebook.com/posts/1840075619545360>`_

解答
=====

以上を踏まえると、 :code:`npm install` を実行したときのA/node_modules内のレイアウトは以下のようになります。

.. code-block:: text

    $ tree node_modules/
    node_modules/
    ├── B
    │   └── package.json
    ├── C
    │   ├── node_modules
    │   │   └── D
    │   │       └── package.json
    │   └── package.json
    └── D
        └── package.json

Dのバージョン違いが2つあり、CのサブディレクトリにあるほうがD\@1.0、上位にあるほうがD\@2.0です。
これは、まずAにBを追加して、その結果A/node_modules/DにD\@2.0が配置され、次にAにCが追加されるときには、
すでにDのバージョン違いがあるため、Cのプライベートなnode_modulesにD\@1.0が配置されるためです。
ちなみに、yarnを使った場合は、これとは逆の順番になるようです。

プロダクション環境用に :code:`npm install --production` でインストールした場合は、devDependencies(B)が無視されるため、以下のようになります。

.. code-block:: text

    $ tree node_modules/
    node_modules/
    └── C
        ├── node_modules
        │   └── D
        │       └── package.json
        └── package.json

A/node_modulesからDが消えました。つまり、Aパッケージからrequireを実行してDに到達することはできなくなりました。

参考までに、これを実験したときのモジュールを `GitHub <https://github.com/tai2/node_modules_layout_experiment>`_ に上げておきます。
このような実験を行うときには、ローカル環境にnpmレジストリを立てられる `sinopia <https://github.com/rlidwka/sinopia>`_ が便利です。

元々やりたかったのは、プラグイン(パッケージ)群への依存をまとめたメタパッケージのようなものを実現したいということでした。
ここまで見てきた事実で、なぜこのようなことをしてはいけないのかがわかります。
A,B,C,Dを具体的な例に置き換えてみます。

* A: アプリ
* B: メタパッケージ
* C: Bとは無関係にプラグインに依存したパッケージ
* D: プラグイン

開発時には、アプリからプラグインが使えていたのに、プロダクション環境では、プラグインが使えなくなってしまうという状況になってしまっています。
これは、アプリが、明示的に依存関係を指定していない(つまりpackage.jsonに記述していない)パッケージを、直接利用しようとしたことから生じています。

このようなバカなことを実際にするわけがないと思われるかもしれませんが、実際にこれをやっているwebpackerというパッケージがあります。
筆者は、これが原因でトラブルに見舞われました。A,B,C,Dを実在のパッケージに置き換えて依存関係を表すと以下の通りです。

* App -> Storybook (devDependencies)
* Storybook -> file-loader\@1.1 (dependencies)
* App -> Webpacker (dependencies)
* Webpacker -> file-loader\@0.11 (dependencies)

このときは、Appのpackage.jsonにfile-loader\@1.1への依存を追加することで問題を回避しました。
[ref]最新のWebpacker 4では、file-loaderへの依存が(たまたま)Storybookと同じ1.1になっているため、この問題は起きないと思います[/ref]
webpackベースで似たような機能を提供する、create-react-app(react-scripts)やpoiではどうなっているか調べたところ、
これらは、アプリからプラグインを直接利用させるような設計にはなっていないため、問題なさそうでした。
webpackerは、ビルド機能そのものを提供するのではなくwebpackの設定ファイルのみを提供する(ビルドそのものはアプリ側で行う)、というコンセプトの違いが問題の根底にありそうです。

参考: `What's the difference between dependencies, devDependencies and peerDependencies in npm package.json file? <https://stackoverflow.com/questions/18875674/whats-the-difference-between-dependencies-devdependencies-and-peerdependencies>`_

まとめ
======

* 複数のパッケージをまとめるメタパッケージのようなことをnpmの仕組みでやろうとするのは、やめたほうがいい
* package.jsonで指定していないパッケージを直接利用すべきではない

