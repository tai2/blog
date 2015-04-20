NodeSchool TokyoイベントレポートとNodeSchoolコミュニティの紹介
##############################################################

:date: 2015-04-18
:slug: nodeschool_tokyo_report
:tags: nodeschool, nodejs
:summary: PythonJSというPythonからJavaScriptへのトランスレーターで変換されたコードが、元のCPythonコードよりも高速になったという 記事が出ました。ちょっと興味が湧いたので、PythonJSについて調べてみました(この記事はプログラマ向けです)。

.. contents:: 目次

.. image:: {filename}/images/nodeschool-tokyo-logo.png
   :align: center
   :alt: NodeSchool Tokyo logo

去る4月12日、渋谷のサイバーエージェントセミナールームで行われた `NodeSchool Tokyo(東京Node学園 入学式) <http://nodejs.connpass.com/event/13182/>`_ に、メンターの１人として参加してきました。
本稿では、NodeSchoolとは何かを説明し、イベント当日の雰囲気をお伝えします。

ワークショッパーについて
========================

NodeSchoolについて話すためには、まずワークショッパーについて説明しなければいけません。
ワークショッパーは、Node.jsで実装されたターミナル向けのアプリケーションで、これを使えばNode.jsの基本や、JavaScriptなど、さまざまな技術をクイズ形式で学べます。プログラミングに詳しい人には、ユニットテストのテストスイートがあって、それにパスする実装を書いて提出するようなイメージと言えば伝わり易いかもしれません。

クイズ形式とはどういうことか簡単に説明しましょう。
たとえば、JavaScriptの入門向けワークショッパーであるjavascriptingは、
次のコマンドでインストールできます。[ref]ワークショッパーは、Node.jsのパッケージリポジトリであるnpm上で公開されています。[/ref]

.. code-block:: none

   npm install -g javascripting-jp

javascriptingを起動すると次のようなメニューが表示されます。

.. image:: {filename}/images/javascripting-menu.png
   :align: center
   :alt: javascripting menu

覚えたい項目を選択すると次のように問題文が表示されます。

.. image:: {filename}/images/javascripting-problem.png
   :align: center
   :alt: javascripting problem

出題された条件を満たすプログラムを書けたら、次のコマンドを実行すれば答え合わせができます。

.. code-block:: none

   javascripting-jp verify strings.js

間違っていたら、どこが間違っているのか丁寧に教えてくれます。

.. image:: {filename}/images/javascripting-fail.png
   :align: center
   :alt: javascripting fail

正解すると褒めてもらえます:)

.. image:: {filename}/images/javascripting-succeeded.png
   :align: center
   :alt: javascripting succeeded

NodeSchoolとは
===============

`NodeSchool <http://nodeschool.io/>`_ はワークショッパーをベースにして繋がるコミュニティです。
ワークショッパー自体を作成したり、それを利用した学習イベントを世界中で開催していて、
やる気さえあれば、だれでもローカルなコミュニティイベントを開催できます。

NodeSchoolコミュニティで活発に活動している `マーティンさん(大阪在住) <https://github.com/martinheidegger>`_ から聞いた話では、
NodeSchoolは元々は、Node.jsを使ってプログラムを作ったり、知識を教え合うような場だったのだそうです。
それがGitHubとワークショッパーを通じて、南極大陸を除くすべての大陸でコミュニティイベントが開催されるほどに広がりました。

当日の雰囲気
=============

今回のイベントは、日本語化されているワークショッパーのうち、以下の4つを使って行われました。

* `learnyounode <https://www.npmjs.com/package/learnyounode>`_ Node.js入門
* `javascripting-jp <https://www.npmjs.com/package/javascripting-jp>`_ JavaScript入門
* `how-to-npm-jp <https://www.npmjs.com/package/how-to-npm-jp>`_ npm入門
* `tower-of-babel <https://www.npmjs.com/package/tower-of-babel>`_ ES6入門

参加者は、満員の150名程度。メンターも正確には把握していませんが最終的に20名程度集まったようです。

.. image:: {filename}/images/nodeschool-tokyo-picture.jpg
   :align: center
   :alt: NodeSchool Tokyo picture

まずは、Node.jsの環境自体のセットアップができている人と、できてない人に分かれてもらって、
セットアップがまだの人にはメンターが手伝いながらインストールをしてもらいました。

環境構築ができたら、さっそくワークショッパーをインストールしてはじめてもらいます。
大規模イベントの常ではありますが、多人数が同時にダウンロードをしたため、
帯域が足りなくなり、なかなか進まない状況が生まれました。
しかし、多少時間はかかったものの、全員セットアップが完了して、それぞれの課題に入ることができました。

今回のワークショッパーの中では、やはり、javascriptingとlearnyounodeの人気が高かったようです。
tower-of-babelも先端的な機能に触れられるということで人気があったと思います。
作りたてホヤホヤのプログラムということもあり、いくつかトラブルも発生していましたが、
作成者自身が会場にいたため、問題はスムーズに解決されていました。
how-to-npmはモジュールを公開するチュートリアルという若干地味な内容ですが、何人かは取り組んでいた方がいたようです。

参加者のバックグラウンドは多岐に渡りましたが、メンターの数も十分だったので滞りなく進んでいた印象で、
時間内にワークショッパーをクリアできた参加者もチラホラいたようです。

イベントの終わりには、LTがいくつか行われ、その後はそのまま会場で懇親会が行われました。
懇親会は、さまざまなプログラマーと交流することができ、とてもたのしいひとときでした。

NodeSchool Tokyoの活動
======================

NodeSchoolの `東京コミュニティ <http://nodeschool.io/tokyo/>`_ は、 `Sota Yamashtia <https://github.com/sotayamashita>`_ さんの
`声掛け <https://github.com/nodeschool/tokyo/issues/2>`_ で、
今年の1月ごろから徐々に人が集まり始めて、この度ついにイベントを開催することができました。
ちなみに、今回のイベントは、「東京Node学園 入学式」と銘打たれていることからもわかる通り、
`東京Node学園 <http://nodefest.jp/>`_ という有名な日本のNode.jsコミュニティイベントに協賛してもらう形で行われました。
150人もの大人数が集ったのは、東京Node学園の場を借りられたことが大きかったと思います。

NodeSchoolの日本のコミュニティでは、英語で作成されたワークショッパーの翻訳や、
ワークショッパーの作成なども行っています。といっても、いまのところ日本発のものは、
`古川さん <https://github.com/yosuke-furukawa>`_ の作成されたtower-of-babelだけですが。tower-of-babelは、英語や韓国語への翻訳が進行中です。

まだまだ日本語化されていないワークショッパーもたくさんあるので、英語が得意な方は、
翻訳をすると喜ばれると思います。ぼく自身もちょこちょこと翻訳作業をしています。

ちなみに、ワークショッパーを作成するためのモジュールは複数あるのですが、i18n対応などを考える
と新規の作成には、 `workshopper <https://www.npmjs.com/package/workshopper>`_ というモジュールを使うといいようです。

東京以外のコミュニティ
======================

`大阪 <http://nodeschool.io/osaka/>`_ は、いまのところ、おそらく日本で一番活発にNodeSchoolのコミュニティイベントが `開催されている <https://nodeschool.doorkeeper.jp/>`_ 地域です。
月一回くらいの頻度で活発に開催しているようです。それから、過去には、神奈川県の `藤沢 <http://nodeschoolfujisawa.connpass.com/>`_ でも開催されたことがある模様です。
自分の地域でも開催したいという方は、 `チャット <https://gitter.im/nodeschool/nodeschool-japan>`_ などで相談するとコミュニティーの人が話を聞いてくれるのではないかと思います。

NodeSchool International Day
=============================

今度の5月23日には、 `International Day <http://nodeschool.io/international-day/>`_ と題して、世界同時開催のコミュニティイベントが開催されることが決まっています。
詳しい内容は決まっていませんが、きっとたのしいイベントになると思います。

NodeSchool Tokyoについての他の記事
==================================

以下は、先日のイベントについてレポートしている記事です。

* `nodeschool tokyo (東京Node学園 入学式) <http://togetter.com/li/807537>`_
* `東京Node学園 入学式に参加してきました:-) <http://ba-kgr.hatenablog.com/entry/2015/04/12/231154>`_
* `NodeSchoolに参加しました <http://blog.livedoor.jp/kaidouji85/archives/5004079.html>`_
* `nodeschool tokyo 東京Node学園　入学式行ってきました！ <http://k2lab.hateblo.jp/entry/2015/04/12/233921>`_

他にもレポートしている記事などがあればぜひ教えてください。

おわりに
========

ぼくは、普段新しい環境に入るときには、公式のチュートリアルを一通りやって使い方を覚えるようにしています。
仕事でNode.jsをやることになり、使い方を覚えようと思って公式サイトのチュートリアルをやってみようと思ったところ、
Node.js自体にはチュートリアルがなく、代わりにリンクされていたのがNodeSchoolでした。

ビギナー向けのワークショッパーをいくつかやってみたところ、Node.jsという環境自体の楽さもあるとは思いますが、非常にお手軽に入門できました。
個人的には、ユニットテストのような枠組みを発想の転換で、学習教材にしてしまおうという試みがおもしろいなと思っています。
また、ただの学習教材では終わらず、それをベースにして、分散的にローカルコミュニティを構築できる、
フレームワークのようなものを提供しようとしているのもすばらしいです。他の言語や環境でも、このやり方は真似できそうな気がしています。

コミュニティの活動はオープンに行われていて誰でも参加できます。興味を持たれた方は覗いてみてください。

