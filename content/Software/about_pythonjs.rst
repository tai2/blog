CPythonよりも(制約付きで)速いPythonJS
######################################

:date: 2014-07-09
:slug: about_pythonjs
:tags: python, javascript, v8, altjs
:summary: PythonJSというPythonからJavaScriptへのトランスレーターで変換されたコードが、元のCPythonコードよりも高速になったという 記事が出ました。ちょっと興味が湧いたので、PythonJSについて調べてみました(この記事はプログラマ向けです)。

.. image:: {filename}/images/python-logo.png
   :align: center
   :alt: Python logo

PythonJSというPythonからJavaScriptへのトランスレーターで変換されたコードが、元のCPythonコード[ref]Pythonと一口にいっても、オリジナルのCで実装されたCPython、Javaで実装されたJython、.NET上で動くIronPython、RPythonというPythonのサブセットで実装されたPyPyなど、いくつもの実装があります。[/ref]よりも高速になったという `記事が出ました <http://pythonjs.blogspot.jp/2014/05/pythonjs-now-faster-than-cpython.html>`_ 。ちょっと興味が湧いたので、PythonJSについて調べてみました(この記事はプログラマ向けです)。

PythonJSとは
============

`PythonJS <https://github.com/PythonJS/PythonJS>`_ は、正確に言うと、Pythonから、JavaScriptを含む各種プログラミング言語(現状、JavaScript,Dart,Lua,CoffeScript)へのトランスレーターです。
このトランスレーター自体はPythonで書かれていますが、`empythoned <https://github.com/replit/empythoned>`_ を使ってNode.jsから実行することもできます(empythoned自体もPythonJSに同梱されてます)。Node.js用のライブラリとしてのインターフェイスもありますので、Node.jsアプリケーションから、Pythonコードを動的に変換して使用するといった(若干変態的な)荒技も可能です。

.. image:: {filename}/images/pythonjs_flow.png
   :align: center
   :alt: PythonJS conversion flow

変換処理は2パスになっており、まずはPythonコードをpythonjsと呼ばれる中間コードに変換します。
この中間コード自体もPythonで、`同期処理が非同期処理に変換されたり <http://pythonjs.blogspot.jp/2014/06/automatic-synchronous-to-async-transform.html>`_ 、import文がホスト先言語の対応するモジュールに変換されたりします(importは、PythonJSのインライン記法
[ref]JS('var sin = Math.sin')のようにJS関数に文字列を渡すことで、ホスト先言語のコードをPython内にインラインで記述できます。[/ref]
を用いてホスト先言語の対応する機能に変換する文として出力されます)。
次に、pythonjsから、ホスト先のコードに変換されます。

Pythonコードは、標準の `astモジュール <https://docs.python.org/2/library/ast.html>`_ でパースされ、AST[ref]抽象構文木=コードをプログラムから扱い易いツリー構造に変換したもの[/ref]に変換されます。中間コード自体も構文的にPythonコンパイラで受理される表現になっているので、astモジュールでパースできるのがミソです。最近の言語ではあたりまえなのかもしれませんが、標準でこういうライブラリが用意されていると、開発ツールを作るときとかに非常にありがたいですね。

関数のタイプ
=============

PythonJSでは、関数の変換のしかたに3つのモードがあります。

通常モードでは、引数の受け渡し方法を含めて、通常のPythonとの互換性が最大限に維持されます。
このモードでは、メソッドをそのままJavaScriptのコールバックとして渡したりすることもできます(selfと結合した形で関数にしてくれます)。
しかしながら、このモードはかなり遅いです。

fastdefモードは、通常モードより速いコードを生成できますが、可変長引数が使えなくなり、JavaScriptから関数を呼び出すときに、引数を配列やオブジェクトに格納してから渡さなければなりません。関数を@fastdefデコレータで修飾するか、with fastdef:という特別なブロックの中で関数を定義するとfastdefモードになります。

javascriptモードは、最速のモードです。こちらも可変長引数を使えないことに加えて、JavaScriptから関数を呼び出すときには、キーワード引数が使えなります。関数を@javascriptデコレータで修飾する、with javascript:という特別なブロックの中で関数を定義する、pythonjs.configure(javascript=True)でグローバルなスイッチをONにする、のいずれかの方法で、javascriptモードの関数を定義できます。

なお、公式ブログでCPythonよりも速くなったと言っているのは、すべての関数をjavascriptモードで変換した場合の話です。

静的型付け用拡張構文
====================

PythonJSでおもしろいのは、静的型付けができるように `構文を拡張している <http://pythonjs.blogspot.jp/2014/06/optional-static-typing.html>`_ ことです。

.. code-block:: python

    def f(arr, x):
      list arr
      int x
      int y = somefunction()
      arr.append( x+y )

上記のようにC風の書き方で型付けができます。文法を拡張しているのにastモジュールでそのままパースできるのが不思議なところですが、パース前に型付けされている文をプリプロセスするというハックで `実現している <https://github.com/PythonJS/PythonJS/issues/104>`_ ようです。

静的型付けをすると、listのメソッド呼び出しなどが劇的に高速化されるようです。

ベンチマークを走らせてみた
==========================

せっかくなので公式ブログに出ているベンチマークを動かしてみようと悪銭苦闘してみたのですが、けっきょくテストスイートが動かせませんでした(グラフ出力のためのgnuplotコードが構文エラーになってしまったところで挫折)。テストコードは、いまのところLinuxのみサポートしているようです。付属のnbodyベンチマークを単体で走らせてみましたが、たしかにCPythonよりも断然速いようです。

せっかくなので、グラフィクス野郎にはおなじみの `aobench <https://code.google.com/p/aobench/>`_ の `Python版 <http://leonardo-m.livejournal.com/79346.html>`_ を動かしてみたところ、PyPyとほぼ同じくらいのタイムでした(PyPyのほうがほんのすこし速い)。

* PyPy 5秒後半
* PythonJS(javascript=True) 6秒弱
* CPython 1分半くらい
* PythonJS(normal) 4分くらい

(Node.js v0.10.28, PyPy 2.3.1、Core i5で計測)

評価
=====

若干の制約はありますが、言語コアの機能自体は、ほぼほぼ動くようです。
また、V8[ref]Node.jsやChromiumのVM[/ref]はCPythonのVMよりもはるかに高速なので、たしかに速くなります。

ただ、現状だと標準ライブラリが、`ほとんど使えない <https://github.com/PythonJS/PythonJS/blob/59aecdbaa895bc653dd6c74d88a20bd43aa45ddb/pythonjs/ministdlib.py>`_ ので、既存のコードベースはほぼ動かないと思われます(ホスト先に対応する関数があれば、追加すること自体はできますが、上手いことマッピングするのはそれなりにめんどくさそうな気がします)。必然的に、AltJSとして、JavaScriptとミックスして使う形になりそうです。

実際のところ、こんなややこしいことをしてまでPythonコードをV8で動かしたいかと言われると、
あまり実用したいとは思わず、素直にJavaScriptか、あるいはもうちょっとJavaScriptとなじみやすいAltJSで書いたほうがいいかなという気がします。わたし自身はPythonに速さは求めていないのですが、どうしても速さが必要な場合は、PyPyを使ったほうがいいでしょう。

----

.. raw:: html

  <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br />この記事のライセンスは、<a href="http://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>とします。

