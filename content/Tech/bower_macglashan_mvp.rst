BowerとMacGlashanのMVP論文要約
###############################

:date: 2015-07-6
:slug: bower-and-macglashan-mvp-architecture
:tags: mvp, mvc, architecture
:summary: BowerとMacGlashanによるMVPを提唱した論文の要約です。最近MVPモデルのフレームワークでプログラミングをしているのですが、ビューとプレゼンターの境界が曖昧になって、どちらにコードを置くべきか迷う場面が出てきたので、根本的な理解を求めて読んでみました。

BowerとMacGlashanによるMVPを提唱した論文の要約です。最近MVPモデルのフレームワークでプログラミングをしているのですが、ビューとプレゼンターの境界が曖昧になって、どちらにコードを置くべきか迷う場面が出てきたので、根本的な理解を求めて読んでみました。 `PotelのMVP <{filename}/Tech/potel_mvp.rst>`_ に比べると、自分が理解しているMVPの姿とほぼ同じだったこともあり参考になりました。ただ、現在モバイル開発やウェブ開発でよく言われているMVCと、この論文で言及されているMVC[ref]VisualWorksの開発したMVCモデル[/ref]はだいぶかけはなれているので、昨今の典型的なMVC(MVPとかなり似ている)とMVPの微妙な違いは、これを読んでもよくわかりませんでした。

TWISTING THE TRIAD The evolution of the Dolphin Smalltalk MVP application framework.
=====================================================================================

Andy Bower, Blair McGlashan Object Arts Ltd.(2000)

http://www.object-arts.com/downloads/papers/TwistingTheTriad.PDF [ref]こちらには図は入れていないので、元のPDFと並べて読んだほうがいいと思います。[/ref]

導入
----

* この論文では、Model-View-Presenterフレームワークに辿りつくまでの過程を説明する。Object ArtsのMVPは、Dolphin Smalltalkのためのユーザーインターフェイスモデルとして作られた。

ウィジェット
-------------

* Dolphinの設計は、当初Visual Basicのようなクライアントプログラミング環境を真のオブジェクト指向で置き換えるものだった。それはウィジェットベースと呼ばれるものだった。
* ウィジェットベースでは、ユーザーインターフェイスをレイアウトしてから、その要素にコードを貼り付けて、アプリケーションロジックを構築した。
* Visual Basicでは、コンポーネントベースのアプローチができなかった(新しいウィジェットを作って再利用することはできなかった)が、Dolphinでは、コンポーネントを階層的に組み合わせて、それ自身をさらに再利用できるようにしたかった。
* ウィジェットベースのシステムは、ドメインロジックとインターフェイスロジックが密結合してしまいやすいので、満足な結果は得られなかった。

モデル・ビュー・コントローラー
-------------------------------

* 1995年にウィジェットベースのフレームワークをやめて、MVC実装に置き換え始めた。2ヶ月程でほぼ完了したが、満足な結果は得られなかった。
* MVCでは、ビューが、モデルの保持するデータを表示する責務を負う。コントローラーは、低レベルなユーザーのジェスチャをモデルにとって意味のあるアクションに変換する。
* 一般的に、ビューとコントローラーは互いに直接リンクしている(互いを指すインスタンス変数を保持し合っている)。
* ビュー・コントローラーのペアは、モデルとオブザーバー関係になっており間接的にリンクしている。ビュー・コントローラーはモデルを知っているが、逆は成り立たない。
* これにより、複数のビュー・コントローラーが、ひとつのモデルを共有できる(ビュー・コントローラーの差し替えができる)。
* MVCでは、ほとんどの機能はアプリケーションモデルというモデルクラスに組み込まれる。アプリケーションモデルは、ほんとうのモデルと、ビュー・コントローラーの媒介になる。
* ほとんどすべてのアプリケーションロジックが、アプリケーションモデルの中に入る(メニューコマンドやボタンアクションの実行、バリデーションなど)。
* アプリケーションモデルは、その性質上、ユーザーインターフェイスに直接アクセスしたくなることが多いが、それはオブザーバー関係に違反する。
* しかしながら、オブザーバー関係を厳密に守ろうとすると、簡単なことをやるにも遠回りなイベント通知が必要になるので、現実的ではない。
* しかしながら、そうしなければ、モデルが、接続されているビューを知ることになってしまう。それではモデルを共有できなくなってしまう。
* また、コントローラーという概念は、Microsoft WindowsのようなGUI開発環境にはうまくフィットしない。Windowsの提供するウィジェットは、単なるビューではなくそれ自体がコントローラーとしての機能を有している(形を合わせるためだけにMVCのコントローラーを作って、OS標準ウィジェットに機能を委譲するとかおかしなことになる)。

3つ組をねじる: モデル・ビュー・プレゼンター
--------------------------------------------

* MVCのオブザーバーとしての点とコンポーネントを差し替えられる柔軟性は良かったが、アプリケーションモデルとビューが間接的にリンクしている点は間違っていた。また、Windows環境では、コントローラーは不要なように思われた。
* MVCでいきづまっていたときに、同僚の１人が教えてくれたTaligentのMVPに感銘を受けた。それは、MVCの3つ組を60°回転させてMVPとすることで問題を解決するものだった。

モデル
~~~~~~

* ユーザーインターフェイスについての知識を一切持たないドメインオブジェクト(MVCではアプリケーションモデルは、ユーザーインターフェイス的な側面も持っていた点が異なる)。

ビュー
~~~~~~

* MVPでのビューの振舞いは、MVCのそれと同様。モデルの内容を表示するのはビューの責任。モデルは、データの変更をビューに通知する(オブザーバーパターン)。
* MVCとの重要な違いは、コントローラーを取り除いたこと。その代わりに、ビュー自身が生のユーザーインターフェイスイベントを解釈して意味のあるイベントに変換する。
* ほとんどの場合、ユーザー入力イベントは、プレゼンターを介して、モデルに作用する。

プレゼンター
~~~~~~~~~~~~

* ユーザーインターフェイスによって、モデルがどのように操作・変更されるかを管理する。アプリケーションの振舞いの心臓部。
* MVPのプレゼンターは、MVCのアプリケーションモデルに相当するが、プレゼンターは、ビューと直接結びついて、密に連携することでユーザーインターフェイスを提供する点が異なる。

MVPの利点
---------

* プレゼンターがビューに直接アクセスできるので便利。
* コントローラーを排除したので、Windows OSにもよく馴染む。
* ウィジェットベースと比べてユーザーインターフェイスの表示と、ユーザーインターフェイスのロジックがよく分離できている。
* プレゼンターに対してビューを複数用意して、「スキン」を変更するとかも簡単。

将来の可能性
------------

回路図
~~~~~~~

* 当時の特定のツールに依存した話なので省略。回路図みたいなものでアプリケーションのロジックを記述して、クラスを自動生成させよう、みたいな話。

ポータブルなMVP
~~~~~~~~~~~~~~~

* 異なるGUI環境に移植するときにも、MVPなら、MとPはOS非依存なので、Viewさえ対応させれば残りはほぼそのまま使える可能性が微レ存。

結論
-----

* 数年間MVPで開発してみたけど、良さそうだよ。
* VBとかAWTみたいなウィジェットベースのアプローチよりも柔軟。
* MVCと似てるけど、より一貫性があって、プログラミングも気持ち良くできる。

