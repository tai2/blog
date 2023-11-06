DenoでCLIを作るのはとても快適
###############################

:date: 2023-11-05
:slug: deno-cli
:summary: 最近ちょっと必要があって、DenoでCLIコマンドを作ってみた。いままでこういったCLIコマンドはNodeやPythonで作ることが多かったのだけど、Denoの使い心地が知りたくて作ってみたら、思いのほかすごく快適だったので紹介する。

最近ちょっと必要があって、DenoでCLIコマンドを作ってみた。
いままでこういったCLIコマンドはNodeやPythonで作ることが多かったのだけど、Denoの使いごこちが知りたくて作ってみたら、
思いのほかすごく快適だったので紹介する。

作ったのは、 `decor <https://github.com/tai2/decor>`_ というマークダウン変換ツールだけど、なにを作ったかよりも、
どう作ったかが重要なので、この記事では深掘りしない。

.. contents:: 目次

Denoとは
=========

Denoは、Node.jsのクリエイターである
`Ryan Dahl <https://tinyclouds.org/>`_ が、
`Node.jsでの反省点 <https://yosuke-furukawa.hatenablog.com/entry/2018/06/07/080335>`_
を盛り込んで作り直したJavaScriptランタイム。セキュリティーを念頭に置いて設計されている。詳しくは検索してください。

Deno気持ちいい
================

まずなにがいいって、TypeScriptがファーストクラスの言語として組み込まれていて、わずらわしい設定なしに、すぐTypeScript
でプログラムを書きはじめられる。tsconfigを読み込ませることも可能ではあるけど、設定を変更するのは推奨されていない。
それでいい。

そしてそれだけでなく、フォーマッター、リンター、テストランナーなども組み込みコマンドとして付いてくる。いまどきの言語環境
らしく必要なもの全部入り。なんだかんだでJavaScript(TypeScript)が最も手に馴染んだ言語のひとつであるぼくのような
プログラマーにとっては、とにかくお手軽にTypeScriptでプログラムを作れるdenoという環境が、ものすごくありがたい。

Denoはセキュリティーを念頭に置いて設計された環境でもある。具体的には、ファイルの読み込み、書き込み、
ネットワークアクセス、環境変数アクセスなど、どれも明示的な許可が必要になる。権限は、コマンドライン引数で指定するか、
または、ユーザーが都度インタラクティブに与えることもできる。なんとも先進的でクールだ。

パッケージについては、Nodeのnpmのように中央集権的なリポジトリがあるわけではない。基本的には、GitHubのリポジトリがその
ままパッケージという形になる。https://deno.land/x というDenoのパッケージを一覧できるサイトもあるけど、本質的には
GitHubリポジトリにアクセスするためのCDNに過ぎない。 :code:`package.json` でパッケージを管理する必要はなく、

.. code-block:: javascript

    import { DOMParser } from 'https://deno.land/x/deno_dom@v0.1.42/deno-dom-wasm.ts';

こういうふうにURLから直接インポートする。

ただし、npmもサポートしていて、 `Node互換API <https://docs.deno.com/runtime/manual/node/compatibility>`_ 
も完全にではないにしろ用意されてはいるので、Node.js向けに公開されているパッケージもある程度利用できる。

感覚としては、npmの `そこそこ複雑なモジュール解決の仕組み <https://blog.tai2.net/node-quiz-about-npm-install.html>`_
がガッツリないことで、ブラックボックス部分が少なく、シンプルに使えるという感覚がある。モジュール解決に柔軟性を持たせる
仕組みとして、JS標準の `Import Maps <https://docs.deno.com/runtime/manual/basics/import_maps>`_ も
サポートしている。

プログラムの配布
==================

CLIコマンドを書いたら配布したくなる。Denoで書いたプログラムを配布するのはとても簡単だ。ユーザーシステムにdenoがすでに
インストールされている前提であれば、

.. code-block:: bash

    deno install --allow-write --allow-read https://deno.land/x/decor/src/decor.ts

このようにソースコード(エントリポイント)を指定してinstallコマンドを実行するだけでいい。この際、指定した権限がインスト
ールされるスクリプトに付与されるので、ユーザーが毎回権限を指定する必要はない。

また、ユーザーにdenoランタイムのインストールを要求したくない場合は、Typescriptのソースコードをネイティブバイナリ
ファイルにコンパイルすることもできる。

.. code-block:: bash

    deno compile --target x86_64-unknown-linux-gnu --allow-write --allow-read src/decor.ts

WindowsやmacOSなど各種環境へのクロスビルドが可能。便利。この機能を使って、リリースごとに `CIで各種プラットフォーム向けの
バイナリをビルドし、アセットとして添付するようにした。 <https://github.com/tai2/decor/blob/main/.github/workflows/build.yml>`_
denoで作ったプログラムを配布するのがいかに簡単かについては、HomebrewのクリエイターであるMax Howeellも
`詳しく紹介している。 <https://deno.com/blog/tea-simplifies-distributing-software>`_

また、ぼくはふだんmacOSを使っているので、コマンドはなるべく `Homebrew <https://brew.sh/>`_ で管理したい。
なので、Homebrew用の `Formula <https://github.com/tai2/homebrew-brew/blob/main/Formula/decor.rb>`_ 
も用意した。Denoプログラム用には、 `Node.jsのように便利なユーティリティー関数 <https://github.com/Homebrew/brew/blob/ff404fe5ab7491b074568b3e20ef001b5ca39595/Library/Homebrew/language/node.rb>`_
もいまのところ用意されていないものの、denoの仕組み自体シンプルなので素直に実装できた。

.. code-block:: ruby

    def install
        prefix.install "src"
        system "deno", "install", "--allow-read", "--allow-write", "--root", ".", "#{prefix}/src/decor.ts"
        bin.install "bin/decor"
    end

このように必要なコード一式をインストールしてから、 :code:`deno instal` を実行して、ラッパースクリプトを生成する。
そして、最後に生成されたラッパースクリプトをインストールすればいい。

ソースコード以外のアセットを配布する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nodeであれば、パッケージに内包されるファイルは、 :code:`npm install` 時に、配布先システムのnode_modules内に
配置される。しかし、denoにはパッケージをインストールするという概念がないし、バンドラーのように任意のファイルをimport
することもできない。つまり、denoでは、任意のアセットをパッケージの一部として、手軽に配布する機能がない。

今回作成したプログラムでは、マークダウンファイルやHTMLをプログラムの一部として配布、というかプログラムから参照して使いた
かった。もちろんソースコード内部に文字列として定義することもできるが、できれば別ファイルに分離してアセットとして管理
したい。調べたところ、Denoでは、以下のようにJSONファイルへの依存関係をimportで記述できることがわかった。

.. code-block:: javascript

    import assets from './assets.json' assert { type: 'json' }

そこで、必要なアセットを `JSONに変換しておくことで <https://github.com/tai2/decor/blob/main/src/build_assets.ts>`_ 
プログラムの一部としてアセットを配布できるようにするという方法を考えた。バイナリファイルなども、BASE64エンコードすれば
JSONに入れておくことができるだろう。

依存関係の自動更新
======================

Nodeであれば、dependabotやrenovateといったツールで依存関係の自動更新ができるが、どちらのツールも現在のところDenoを
サポートしていない。

Denoでは、 `udd <https://github.com/hayd/deno-udd>`_ というツールで依存ファイルの更新検出とアップデートができる
ので、これを `スケジュールジョブで回して <https://github.com/tai2/decor/blob/main/.github/workflows/udd.yml>`_
依存ライブラリの更新をするようにした。

ただし、更新してくれるのは直接依存しているファイルのみで、依存の依存までは見てくれないため、依存ライブラリが依存している
ライブラリに脆弱性が発見されたときに、部分的に依存を更新するといったケースは、この仕組みでは対応できない
(Nodeであれば、 :code:`package-lock.json` や :code:`yarn.lock` の更新で対応できるケース)。

マークダウンパーサー
==========================

decorはマークダウンを扱うツールなので、マークダウンパーサーが必要だった。TypeScriptで使えるマークダウンパーサーには
いくつか選択肢があるが、機能とAPIを検討した結果、今回は、 `marked <https://github.com/markedjs/marked>`_ を
使うことにした。型情報が後付けではなく、最初からTypeScriptで開発されているのも、高評価ポイントのひとつ。

ただし、markedをDenoから使うにもいくつか方法がある:

1. npmモジュールとして利用する方法: :code:`import { marked } from 'npm:marked';`
2. deno.landで `配布されているバージョン <https://deno.land/x/marked@1.0.2>`_ を利用する方法
3. GitHubから直接参照する方法

方法1の場合は、元々TSで書かれたものが、JSにコンパイルされて型情報と分離された状態で配布される形になる。Denoは、Nodeで
TypeScriptを使ったときと違って、:code:`d.ts` から自動的に型情報を見つけてはくれない。型情報の定義先も
`別途明示的に記述する必要がある。 <https://docs.deno.com/runtime/manual/advanced/typescript/types#providing-types-when-importing>`_
何だか面倒なのでもっといい方法があるなら、そちらを選択したい。

2は、どこかの誰かが、markedをdenoから利用しやすいようにdeno.landな形にして登録したものらしい。試してみたところ、本来
得られて欲しい型情報がanyになっていたりして、いまいちだった。中身がどうなっているのか見てみると… `単にnpm specifierで
importしているだけだった。 <https://github.com/prettykool/marked-deno/blob/main/mod.ts>`_

よくよく考えると、さきほども書いたようにmarkedのコードはそもそもTSで記述されている。そして、Denoはリモートのソース
コードを直接参照できるので、GitHubから直接importすればいいだけなのではないか。つまり、こうなる。

.. code-block:: javascript

    export { marked } from 'https://raw.githubusercontent.com/markedjs/marked/v9.1.4/src/marked.ts'

TypeScriptのソースコードをそのままなので、型情報も完璧。Denoでは、このようにリポジトリから直接importできるので、
TypeScriptで書かれたライブラリを選択するモチベーションがより高くなると思う。

DOMパーサー
============

decorではHTMLのパーサーも必要だったので、いくつか選択肢を検討した。

Denoのサイトでも紹介されているように、DenoでHTMLをパースするときには、いくつかの選択肢がある。主なものは:

* `js-dom <https://docs.deno.com/runtime/manual/advanced/jsx_dom/jsdom>`_
* `deno-dom <https://docs.deno.com/runtime/manual/advanced/jsx_dom/deno_dom>`_
* `LinkeDOM <https://docs.deno.com/runtime/manual/advanced/jsx_dom/linkedom>`_

どれも型情報は提供されている。deno-domは唯一Deno向けにTypeScript(+Rust)で書かれたものなので、せっかくだから
deno-domを使ってみることにした。途中、うまく動かない箇所があり、バグ報告しつつLinkeDOMのほうも試してみたら、こちらは
こちらで型情報が間違っていて、目的が達成できないなどのトラブルがあった。そうこうしているうちに、deno-domのバグが修正
してもらえたので、けっきょくdeno-domで実装することができた。deno-domは報告したらけっこうサクッと問題修正してもらえ
たので、安心感がある。

いずれもHTMLのDOM APIに寄せて作られているので、乗り換えはそこまで大変ではないと思う。

まとめ
======

* Denoは設定ファイルほとんど不要ですぐに開発環境が整うので快適
* TypeScriptまわりのあれこれについてもopinionatedにこうすると決めてくれているので、なにも考えずついていけばいいだけなのは楽
* TSコードを単独で動作するネイティブバイナリにコンパイルできるので配布も楽
* npmを参照したり、GitHubからTypeScriptソースコードを直接importできるので、サクッとアプリを作りやすい環境も整っている