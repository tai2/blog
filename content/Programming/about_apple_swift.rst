Appleの新言語Swiftが発表されました
###################################

:date: 2014-06-13
:slug: about-apple-swiftt
:tags: apple, swift, objective-c, ios
:summary: 先日のWWDC基調講演で、Appleの新言語 `Swift <https://developer.apple.com/swift/>`_ が発表されました。これは、いままでApple製品用のソフトウェアを開発するときに使われていたObjective-Cを置き換えるものです。発表と同時に言語のドキュメントも公開されて、開発者からも概ね好意的に受けとめられているようです。

.. image:: {filename}/images/swift_hello.png
   :align: center
   :alt: swift hello world code

先日のWWDC基調講演で、Appleの新言語 `Swift <https://developer.apple.com/swift/>`_ が発表されました。
これは、いままでApple製品用のソフトウェアを開発するときに使われていたObjective-Cを置き換えるものです。
発表と同時に言語のドキュメントも公開されて、開発者からも概ね好意的に受けとめられているようです。

おもしろいのは、Apple向けアプリの開発に関わらなさそうなプログラマたちからも、大きな注目を集めて、
みんなが言語仕様の分析などに熱中していることです。
Apple自身、この言語はCocoa[ref]Appleのアプリケーション開発用フレームワーク[/ref] 向けの言語であると言っているように、主としてiOSやMac OSX用のアプリケーションを書くために使われることになると思います。
もちろん、Objective-CをCocoaと切りはなして使えるように、Swiftをそれ単体で開発に使うこともできるでしょう。
しかし、多くの人は、実際に開発で使うかどうかという興味から離れたところで、Swiftに注目しているように見えます。

これは、Appleの影響力がそれほど大きいということももちろんありますが、
なによりも、Swiftが、注目を引くような現代的な機能をいろいろ詰め込んでおり、言語として興味深いからなのだと思います。

わたし自身は、Swiftのドキュメントは、まだほとんど読んでいません。
次にiOSアプリ開発案件が発生したら、そのときに覚えようと思っています。
幸い、iOS7アプリの開発にも使えるようですので、新規のプロジェクトにはどんどん使っていきましょう。
いまさらiOS6をサポートしても、`ほとんど意味はないでしょう <http://bylines.news.yahoo.co.jp/takayukifukatsu/20131031-00029328/>`_。

Swiftでアプリ開発がどう変わるか
===============================

Objective-Cよりあきらかに良い
-----------------------------

まず、パッと見ただけでも、スッキリしていて、明らかにSwiftはObjective-Cよりも開発しやすそうです。
ソースコードは、見た目が大事です。
じつのところ、Objective-Cには、一部 `熱狂的な信者 <http://love-motif.com/article/art_13.shtml>`_ がいたりしたようですが、言語それ自体は、
あまり評判のいい言語ではありませんでした。

Objective-Cの評判の悪そうな性質として、わたしが想像するのが、

1. 独自のメソッド呼び出しの記法(角括弧)が、Cの関数呼び出しと混在しているのが気持ち悪い
2. メソッド名にキーワードも含まれており、withやatなどの前置詞が名前に入るので、全般的に長すぎる
3. 型チェックもあるが、どちらかというと動的な性質が好まれていた(宣言していないメッセージの送信、id型へのメッセージ送信など)

といったあたりです。
すくなくとも、1,2は解消されていそうです。
3は、Objective-Cのように型[ref]型というのは、プログラミングの誤りを、プログラムを実行する前に発見するのに非常に有用な概念です。いずれ記事にするかもしれません。[/ref]を弱めるような使いかたが容易にできるのかどうか把握していないのですが、
ドキュメントをちょっと読むだけでも型安全という面を押し出しているようなので、開発者のマインドも
変わってくるのではないでしょうか。

ところで、基調講演では、Objective-C - C がSwiftとなんだと言ってましたが、むしろObjective-Cのエッセンスもあまり残ってないのでは。

Cとの互換性
-----------

ひとつ大きな変更点として、C言語との互換性を捨てたというのがあります。
Objective-Cでは、C言語の関数をそのまま呼び出すことができましたし、C関数をObjective-Cコード内で定義する
ことさえできました(Objective-Cは、Cにオブジェクト指向機能を足したものなので)。
これは、C言語で書かれたOSSなどのライブラリをそのまま使えるので、かなり大きな利点でした。
Swiftでは、Objective-Cとの互換性は保たれていますが、C関数をそのまま実行するのは、どうもできなさそうです。
`Cのデータ型自体はある <https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/BuildingCocoaApps/InteractingWithCAPIs.html#//apple_ref/doc/uid/TP40014216-CH8-XID_13>`_ ようなので、Cライブラリを使いたい場合は、Objective-Cでラップ必要があるのかなと想像しています。

いずれにしろ、Cライブラリを使うことが不可能になるということは有り得ないと思うので、ちょっとめんどうにはなるかもしれませんが、問題はないと思います。

**※追記** Cライブラリもインポートして使えるという `記述がありました <https://developer.apple.com/library/prerelease/ios/documentation/swift/conceptual/buildingcocoaapps/index.html>`_。*Any Objective-C framework (or C library) that’s accessible as a module can be imported directly into Swift. This includes all of the Objective-C system frameworks—such as Foundation, UIKit, and SpriteKit—as well as common C libraries supplied with the system.* この記述だけみると、ユーザー提供のCライブラリはインポートできないようにも読めますが、どうなんでしょうね。

劇的な工数削減はないかも
------------------------

心理的にも実際的にも、かなり開発し易くなることは確かですが、とは言え、それで開発工数が半分とか、十分の一になるかと言われると、そうはならない気がしています。そもそも、Objective-Cがそこまでよくはなかったとは言え、どうしようもなく悪いというわけでもありませんでした(C言語と比べれば)。また、わたしが普段やっているような小さい規模の案件だと、プログラミング言語やコーディング作業自体よりは、フレームワークの使いかたで悩んだりハマったりしてる割合が多いような気がします。もっと大きな案件になってくると、プログラミング言語自体の構造化能力が、より効いてくるというのはありそうですが。とはいえ、気持ち良くプログラミングできるのは良いことなので、やはりSwiftはiOS開発者にとって歓迎すべきものです。

