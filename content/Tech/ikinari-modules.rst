ikinari-modules: package.json不要でunpkg等からimportしてバンドルできるCLI
###########################################################################

:date: 2020-12-20
:slug: ikinari-modules

この記事は `Node.js Advent Calendar 2020 <https://qiita.com/advent-calendar/2020/nodejs>`_ の20日目の記事です。

先日、

.. code-block:: bash

        echo "import stringLength from 'https://unpkg.com/string-length'; \
        console.log(stringLength('🐴'))" \
        | somethingUsefulCommand

みたいな感じで、 `unpkg <https://unpkg.com/>`_ からのstatic importを解決してバンドル化した上で標準出力してくれるツールがあればいいのに、と思うことがあった。

調べたところ、そのような機能を持った既存コマンドは見つけられなかったのでこれを作成した。

https://github.com/tai2/ikinari-modules

これを使えば、以下のようにpackage.jsonを作らずともバンドル化されたJSファイルを得られる

.. code-block:: bash

        echo "import stringLength from 'https://unpkg.com/string-length'; \
        console.log(stringLength('🐴'))" \
        | ikinari -i -

作るまでの過程で、非常にふわっとした理解しか持っていなかったES modulesについても調べて理解したので、そのあたりのことや、既存ツールの状況などについて、この記事でまとめる。

どのバンドラーをベースにするか
================================

既存でぴったりマッチするツールがなくても、webpackなどモジュールバンドラーのAPIを使うなりなんなりすれば、たぶんサクッと作れるだろうという直感はあった。ただ、URLを直接importするということが、最近のブラウザでできるのは知っていたものの、各種バンドラーがその機能を持っているのかはまったく知らなかったので調べた。

* `webpack <https://webpack.js.org/>`_ : webpack 5で、 `httpsからフェッチするプラグイン <https://webpack.js.org/blog/2020-10-10-webpack-5-release/#uris>`_ が追加されたらしい 。ただし、現状まだexperimental。
* `rollup <https://rollupjs.org/>`_ : いくつかプラグインがあるが、 `rollup-plugin-url-resolve <https://github.com/mjackson/rollup-plugin-url-resolve>`_  を使えば動作することが確認できた。
* `parcel <https://parceljs.org/>`_ : コミュニティープラグインを含めて探したが、それらしいものは見つけられなかった。
* `snowpack <https://www.snowpack.dev/>`_ : 今回調べるまで知らなかったが、snowpack自体にはモジュールのバンドリング機能はないらしい。あくまで開発時のビルド体験高速化が目的のツール。なので対象外。

今回、個人的な趣味で、入力ファイルは標準入力からも受け付けられるようにしたかった。webpack cliは標準入力を取れず、rollupのcliは取れる。なので、webpackにしようかrollupにしようかすこし迷ったものの、rollup cliをラップすることにした。

skypackとunpkg
===============

npmのモジュールを配布しているCDN自体、いくつもある。

rollup-plugin-url-resolveを動かして試した結果、skypackからのimportなら成功するが、unpkgからではできないものがあることがわかった。

skypackとunpkgには、前者がパッケージにある変換をかけて配布しているのに対して、unpkgはnpmに上がっているものをそのまま配布しているだけという違いがある。(実はunpkgにも?moduleをいうパラメータを付ければ変換済みの結果にアクセスできる機能があるが、不完全であり、一部のパッケージでしか動作しないことを確認した) skypackがなにをやっているかというと、まずCommonJSのファイルをES Moduleに変換している。それから、package.jsonを見て依存関係を解決した上でimport指定(specifier)を変換している。つまり、import指定に@v4.0.1みたいなバージョン指定を付与している。

だから、skypackならブラウザから直接importできる。

rollupでunpkgからのimportができないのは、skypackがやっている処理の一部分しかできないからだ。つまり、 `@rollup/plugin-commonjs <https://github.com/rollup/plugins/tree/master/packages/commonjs/#readme>`_ プラグインなどでCommonJS → ES変換はできるものの、rollup-plugin-url-resolveは単純なフェッチ機能のみで、依存関係解決機能がない。

とりあえず、skypack限定っていう形なら目標が実現できることは、この時点で確定した。実用的にはこれでも十分なんだけど、それだけだとつまらないので、もうちょっと深堀してunpkgからのimportをあらためてゴールに設定した。たぶん、rollup-plugin-url-resolveをちょこっと修正するなり、補完するプラグインを作るなりすればイケるだろう。

依存解決の問題
================

そもそもブラウザでのimportとNodeでのimport、CommonJSのrequireとの間にはどのような違いがあるのか、なにが問題なのかを見定めるために、このあたりをきっちり理解しておく必要がある。

まず、ブラウザでのimportだけど、これは現状、与えられたURLを単純にそのままフェッチするだけで、依存関係の解決機能はブラウザには一切ない。これがNodeとの大きな違いだと思う。それから、ブラウザでは、bare specifierと呼ばれる指定ができない。これは、Nodeでいちばん普通のユースケースである、パッケージ名だけの指定。 :code:`import 'string-length'` みたいなやつ。bare specifier自体は、 `import-maps <https://github.com/WICG/import-maps>`_ という機能  が実装されれば利用できるようになる模様。パッケージ名をどのように解決するかをJSONファイルで補う仕様のようだ。これができると、npmで依存を解決してnode_modulesにパッケージをまとめた上で、それをそのままブラウザから使うことができるようになる。つまり、ブラウザとnpmが直接コラボできるようになるということと理解した。

一方、Nodeでの依存解決はどうなっているのか。以前 `別の記事 <https://blog.tai2.net/node-quiz-about-npm-install.html>`_ にまとめたけど、Nodeの依存解決というのは、実は2フェーズから成り立っている。npm installとrequire/importだ。npm installが、package.jsonを見て依存パッケージとバージョンを把握した上で、node_modulesフォルダを適切に構成する。そして、require/importが、その中から `規定されたアルゴリズム <https://nodejs.org/api/modules.html#modules_loading_from_node_modules_folders>`_ に従って、実際のパッケージを検索する。この2つが合わさって、最終的に取り込むモジュールが確定される。

Nodeでのrequireとimportについては、細かい挙動の違いはあるものの、 `検索アルゴリズム <https://nodejs.org/api/esm.html#esm_resolver_algorithm_specification>`_ 自体は同じものだと思っている。けど違ったら教えてください。

リモートimportで依存解決を実装する
===================================

上記で見たように、Nodeでは、import実行時に1から依存解決をするわけではない。npm installで、パッケージのフェッチを含む大半の依存解決が住んでいることが前提のアルゴリズムになっている。今回やりたいことは、パッケージがまったく手元にないことが前提になるので、通常のブラウザやNodeのimportとはまったく違うやりかたをしなければならない。

具体的には、importer(importを実行している元ファイル)がリモートURLであった場合には、自分自信も同一のリモートサイトに置かれていると見なして、まずpackage.jsonを読んだ上で実際の依存バージョンを特定し、その上でフェッチする。幸い、upnkgには、package.json準拠の `バージョン表記 <https://docs.npmjs.com/about-semantic-versioning#using-semantic-versioning-to-specify-update-types-your-package-can-accept>`_ を理解した上で、適切なバージョンにリダイレクトしてくれたり、bear specifierから、インポートすべきモジュールにリダイレクトしてくれたりする機能はあるので、そのあたりはすこし楽をできる。

ということで、上記を実現するために不足している機能をrollup-plugin-url-resolveに追加した。

https://github.com/mjackson/rollup-plugin-url-resolve/pull/9

これで、当初の目標が実現できた。

参考文献
=========

* JavaScript modules https://hacks.mozilla.org/2018/03/es-modules-a-cartoon-deep-dive/ ES Modulesについて一歩踏み込んだ理解ができるので、おすすめ。
* JavaScript modules https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
* JavaScript modules https://v8.dev/features/modules
* Modules: ECMAScript modules https://nodejs.org/api/esm.html
* WICG/import-maps https://github.com/WICG/import-maps

