AndroidアプリのSquare風MVP仕立て 〜Dagger 2をそえて〜
======================================================

:date: 2015-09-30
:slug: android_mvp
:tags: android,square,dagger,mvp,architecture
:summary: 本稿では、FlowとMortarにDIライブラリであるDagger 2を組み合わせて、Androidアプリを構築する方法について説明します。また、これらのライブラリがどのような仕組みで動いているのかも解説します。

Androidアプリプログラミングで、ある程度経験を積んだ開発者なら、Fragmentにまつわる操作で不意に発生するIllegalStateExceptionには、いくどとなく苦しめられたことがあるでしょう。
`Fragment <http://developer.android.com/intl/ja/guide/components/fragments.html>`_ は、スマートフォンのためのOSから、タブレットなどより幅広いスクリーンに対応できるマルチデバイスなOSに進化するために、Android 3.0で登場したコンポーネントです。
Fragmentを利用すれば、画面をいくつかの要素に分割して、それぞれをMVCで構築し再利用するという、 `Smalltalk-80のMVC的な方法論 <http://heim.ifi.uio.no/~trygver/themes/mvc/mvc-index.html>`_ が可能になります。
一方、いまでは広く認められていることですが、Fragmentのライフサイクルは `よく見てみると複雑 <https://github.com/xxv/android-lifecycle>`_ で、足をすくわれがちです。
そこで、 Fragmentに対するカウンターとして、 `Square <https://squareup.com/jp>`_ は、FlowとMortarという2つのライブラリを開発し、MVPアーキテクチャによるAndroidプログラミングを `提唱しました <https://corner.squareup.com/2014/10/advocating-against-android-fragments.html>`_ 。[ref]筆者自身、Fragmentを使わずともViewで十分なのではないかという `疑念を抱いていた <https://twitter.com/__tai2__/status/205235187116806144>`_ ので、この主張はスッと飲み込めるものでした。[/ref]

本稿では、FlowとMortarにDIライブラリであるDagger 2を組み合わせて、Androidアプリを構築する方法について説明します。
合わせて、FlowとMortarがどのような仕組みで動いているのかも学びます。

これから説明するMVPプログラミングは、ユニットテストをしやすくするために、オリジナルのSquareのやりかたから若干アレンジしています。
変更点については `ユニットテストの節 <#id29>`_ で詳しく述べます。

理解の助けとなるよう図をたくさん使いましたが、図中の線、形状、色の意味付けはかなりいい加減で一貫性もないので、逆に混乱させてしまったら申し訳ありません。
文章と合わせて適切に解釈してもらえると助かります。

また、この記事の主眼は、あくまでFlow/MortarとDagger 2を組み合わせて使うということであり、Dagger 2そのものの使い方には焦点を当てていないので、それについては他の文献を当たってください。

.. contents:: 目次

ライブラリのバージョン
------------------------

本稿の説明は、以下のバージョンのライブラリを前提とします。

* `Flow 0.12 <https://github.com/square/flow>`_
* `Mortar 0.19 <https://github.com/square/mortar>`_
* `Dagger 2.0.1 <https://github.com/google/dagger>`_

サンプルアプリ
----------------

Flow/Mortar/Dagger2を利用したアプリのサンプルとして、Todoアプリを用意しましたので、参考にしてください。

https://github.com/tai2/flowmortardagger2demo

このアプリは、Todoリスト画面、Todo追加画面、Todo編集画面という3つの画面からなります。各画面のユニットテストも実装してあります。

Square風MVPのメリット・デメリット
---------------------------------

Square風MVPでは、Androidの標準コンポーネントであるFragmentを完全に捨ててしまいます。それどころかActivityさえも基本的に使いません。
標準の開発者ガイドや参考書に書いてあるのとは、まったく違うやりかたでプログラミングをしますし、参考にできる情報も多くはありません。
そこまでして導入する価値のあるものなのかどうかという点が、気になっている方が多いと思いますので、まずはメリットとデメリットについて挙げます。
以下は、Square風MVPで、そこそこの規模の商用アプリを一本開発してみての感触です。

箇条書きで足りない部分は追加で補足します。

メリット
~~~~~~~~

1. 当然ながら、Fragment関連でのIllegalStateExceptionからは開放される。
2. Configuration Changesへの特別な対応が不要になる。
3. 画面遷移をするときに、(画面を表す)Pathのコンストラクタに必要な情報を渡せる。
4. Presenterは、Viewに直接依存しないのでテストし易い。
5. Daggerにより、オブジェクトの初期化を自動でできる(フィールドの宣言だけで済むのでコードがスッキリする)。
6. Daggerにより、「どこから」オブジェクトを取得するかと、「どの」オブジェクトを初期化するかを切り離すことができる。

2について。通常のActivityやFragmentは、画面の回転やConfiguration Changesと呼ばれるイベントが起きると、そのたびに破壊と再生成が繰り返されますので、
適切に状態を保存・復元する必要があります。一方、MVPでこれらに相当するPresenterは、シングルトンオブジェクトで、Activityよりも寿命が長いので、
Configuration Changesを気にする必要はありません。

3について。Fragmentでは、画面遷移をするときにFragmentオブジェクトをnewで生成して、FragmentTransactionに渡します。
一見すると普通のオブジェクトのように見えるので、コンストラクタのパラメータとして、そのクラスの依存するデータを定義したくなるのが人情ですが、
これは、Fragmentにあまり慣れていないプログラマーがよく陥る罠の一つです。Fragmentには、デフォルトコンストラクター以外のコンストラクターを定義してはいけません。
一方、Square風MPVで画面遷移時に用いるPathは、なにも特殊なことはないただのオブジェクトなので、気兼ねなくいろいろなコンストラクターを定義して、素直にオブジェクトを生成できます。

4について。一般論として、 `MVPはPresenterのユニットテストが容易にできる <https://en.wikipedia.org/wiki/Presenter_First>`_ とされていますが、そのメリットをそのまま受けられます。
ただし、Squareのサンプルコードでは、Presenterが具象Viewと密結合する形となっているので、若干のアレンジが必要です(より.NETのMVPに近い形にします)。

6について。これは、たとえば、開発版とリリース版で使用するオブジェクトを切り替えたり、テスト版では使用するオブジェクトをすべてモックに切り替えるといったことを、一行の変更で行えるようになるということです。

デメリット
~~~~~~~~~~~

1. 学習コストが高い。ドキュメントがほとんどなく、使い方を調べるためにライブラリのソースコードを読む必要がある。[ref]Flowに関しては、サンプルアプリが削除され、今後はドキュメントの拡充に集中する方針のようです。[/ref]
2. ボイラープレートが多くなる。1画面ごとに、Path,Presenter,View,Componentすべてを記述する必要がある。
3. APIの互換性についての保証はない。
4. ライフサイクルの種類はたしかに少ないが、十分な機能を提供していない。
5. Activityの機能に直接アクセスできないことが不便なときがある。

1は、この記事を読めば、多少ハードルが下がるのではないかと思います。

3について。Android SDKは、基本的にAPIの後方互換性を保つ形でバージョンアップされていきますが、FlowとMortarはサードパーティーであるSquareが、自社アプリのためのライブラリとして開発したものをOSSとして公開しているに過ぎないので、そのような保証はありません。
実際、バージョン0.9で、 `APIの破壊的変更が行われました <https://github.com/square/flow/blob/master/CHANGELOG.md>`_ 。
このため、これまでFlowとMortarについて書かれた記事の多く[ref]といってもそもそもそんなに多くないのですが...[/ref]やコードは、そのままでは使えなくなってしまっています。

4について、たしかにFragmentのライフサイクルよりは、MortarのPresenterのライフサイクルのほうがシンプルだとは思うのですが、実際のアプリを作るのに十分な機能を提供できていない場合があります。
たとえば、基本的にはポートレイト固定で、特定の画面のみ回転可能にしたいといった要求はよくあると思いますが、そのようなケースで実装に試行錯誤が必要になることがあります。[ref]実際、試行錯誤が必要になりました。[/ref] また、例えば、スクリーンオフになったときに、動画の再生を停止するといった単純なことも、それをやるのに相応しいライフサイクルメソッドは用意されていないため、Viewのメソッドを駆使してがんばる必要があります。

5は、4とも関連しますが、けっきょくのところ実際のアプリ開発では、Activityの機能にアクセスしたくなることがあります。
たとえばアクションバーのタイトルを変更するためには、Activityへのアクセスが必要です。
しかし、Flowでは、Activityに直接アクセスする手段は用意されていないため、一工夫が必要になります。

Dagger 1 vs Dagger 2
----------------------

FlowとMortarを使ったMVPアーキテクチャでは、 `Dagger 1 <http://square.github.io/dagger/>`_ または `Dagger 2 <http://google.github.io/dagger/>`_ を併用します。Presenterのシングルトン化に、これらのライブラリの提供する機能が必要だからです。

オリジナルのDagger 1は、Squareが開発したもので、Squareの提唱するMVPでもDagger 1を前提としていました。
その後、GoogleがDaggerの後継ライブラリとして、 `Dagger 2を提案しました <https://github.com/square/dagger/issues/366>`_ 。

どちらも用途としては同じで、アノテーションによってDependency Injectionを実現するためのものであり、javax.inject(JSR-330)の一実装です。
Dagger 2の最大の特徴は、それが **完全な** オブジェクトグラフの構成と検証をコンパイル時に行うということです。そのため、生成されるコードは簡潔で、素早いものになります。
一方で、Dagger 1は、オブジェクトグラフの構成(リンク)をランタイムに行います。また、オブジェクトグラフを動的に拡張することが可能です。つまり、コンパイル時のオブジェクトグラフ検証を完全には行いません。

いま現在Squareが内部的にどちらを使ってるのかはさだかではないのですが、 `2015年1月時点ではDagger 1を使っており <https://github.com/JakeWharton/u2020/issues/158>`_ 、すぐに移行する予定もなかったようです。
ただし、Dagger 1は、今年の5月で更新が止まっています。

いまでこそ、Mortarは、Dagger 2とも併用可能なように再設計が行われましたが、もともとDagger 1と併用する前提で開発されたものなので、どちらかというとDagger 1とのほうが相性はいいのかもしれません。
すくなくとも、現時点では、Dagger 1と併用するパターンのほうが情報が多く使い方が確立されていると思います。

一方で、Dagger 2とFlow/Mortarを併用したMVPアプリ開発は、Square社員でMortarの開発にも参加している `Pierre-Yves Ricau <https://github.com/pyricau>`_ を含め、何人かがやりかたを提案してはいるのですが、
確立された方法はないという状況です。そのため、Dagger 2と併用する場合には、導入までの努力が多く必要になると思います。
また、MVPアプリで使う場合には、画面ごとに異なるオブジェクトグラフを作成したいのですが、それをスマートにやろうとすると、けっきょくランタイムのリフレクションが必要になり、
それであれば、ランタイムに柔軟なオブジェクトグラフの構成ができるDagger 1のほうが向いているかもしれません。[ref]Dagger 2がやっているのと同様に、アノテーションを見て、足りない部分を自力でソースコード生成して補うというところまでやれば、Dagger 2の長所を活かせると思いますが、そこまでやる気力はありませんでした。[/ref]

そう考えると、けっきょくのところ、Android MVPをやるには、現時点では、Dagger 1のほうがいい選択なのかもしれません。
筆者がプロジェクトをはじめる前には、いまほど深い理解もなく、どちらのほうが良い選択なのかも判断が難しかったので、新しい方のDagger 2を採用しました。

Model-View-Presenter
----------------------

Model-View-Presenterパターンは、Model-View-Controllerを改変したGUI用のアーキテクチャです。 
MVPの世界では、すべてをドメインモデルとユーザーインターフェイスという2つに綺麗に分割し、Controllerのようなどちらにもまたがる半端者はいなくなる、というのが筆者の解釈です。
`BowerとMacGlashanのMVP論文要約 <http://blog.tai2.net/bower-and-macglashan-mvp-architecture.html>`_ も参考にしてください。

また、 `マイクロソフトの提唱するMVP <http://blogs.msdn.com/b/jowardel/archive/2008/09/09/using-the-model-view-presenter-mvp-design-pattern-to-enable-presentational-interoperability-and-increased-testability.aspx>`_ では、PresenterとViewはインターフェイスによって分離されるため、UI(Presenter)の自動テストが容易になります。Viewの表現自体はテストできませんが、ユーザーアクション=Presenterのメソッドとなるため、アプリ動作のシナリオを、通常のユニットテストの枠組みで検証できるようになります。

コンポーネントの責務
----------------------

この節では、利用する各コンポーネント[ref]この記事では、Dagger 2の提供するComponentというクラスと、いわゆる一般的なコンポーネント(機能のまとまり)が両方出てくるためまぎらわしいかもしれません。Dagger 2のほうは、英語でComponentと書くことにします。[/ref]の責務について簡単に説明します。また、それを利用するアプリがすべきこととしては、なにが残るのかについても触れます。

Flowの責務
~~~~~~~~~~

Flowは、View単位での画面遷移の仕組みを提供します。
これを使うことによって、カスタムビューをベースとしたアプリの構築ができるようになります。

Flowは、独自にバックスタック(History)を管理し、バックスタックに対する操作を定義します。
また、Activityのライフサイクルメソッドの処理を肩代りする、FlowDelegateというクラスも提供します。

Mortarの責務
~~~~~~~~~~~~

Mortarは、階層化されたスコープ(MortarScope)を提供します。
これにより、Contextを階層化したり、階層毎に異なるサービス[ref]ここで言うサービスとは、Context#getSystemService()で取得できるオブジェクトのこと。[/ref]を定義することが可能となります。
また、スコープに応じて適切にリソースを破棄します。

Mortarは、Flowの管理するバックスタックをBundleに保存・復元します。

Dagger 2の責務
~~~~~~~~~~~~~~~

Dagger 2は、アプリの定義したオブジェクトグラフ[ref]どのオブジェクトがどのオブジェクトに依存しているかという依存関係のこと。[/ref]から、Componentクラスを生成します。
Componentクラスは、オブジェクトを生成してフィールドに注入します。また、シングルトンとして指定されたオブジェクトを保持します。
なお、この場合のシングルトンとは、static変数ということではなく、何度injectしても同じインスタンスが再利用される、という意味です。
したがって、Componentインスタンスが変われば、シングルトンとして指定されているインスタンスでも同一とは限りません。

Dagger 2 Componentは、MortarのPresenterインスタンスをシングルトンとして保持します。

アプリの責務
~~~~~~~~~~~~~

アプリは、Activityのライフサイクルメソッドを、FlowDelegateやBundleServiceRunnerに委譲します。
アプリは、コンテナビューを定義し、 `画面遷移の際の細々とした処理 <#pathcontainerview>`_ も実装します。
また、バックスタックの状態をParcelableにシリアライズするための方法も定義します。 
追加のサービスをApplicationやActivityに埋め込むのもアプリの責務です。
ただし、これらはFlowやMortarのサンプルコードに必要なクラスやコード片が用意されているので、基本的にはそれを使えば済みます。

当然ながら、アプリは、画面毎に、Presenter、Viewのレイアウト、Viewクラス、Dagger 2 Componentを実装し、それらの間の遷移やビジネスロジックを実装します。

Square風MVP詳解
----------------

基本的な構成
~~~~~~~~~~~~~

Flow/Mortar/Dagger 2を使用したMVPアプリの構成では、ひとつの画面は、

* Path
* Presenter
* Dagger 2 Component(必要に応じてModule)
* カスタムView(とそのレイアウトファイル)

の4つから構成されます。

.. figure:: {filename}/images/android_mvp/structure.png
   :alt: Squrea Stack Structure

   Squareスタックにおける基本的な構成

Pathは、画面を特定するアドレスのようなもので、画面遷移時に使われます。
Dagger 2 Componentは、各画面のオブジェクトグラフを定義します。
カスタムViewは、画面の視覚的な表現です。
そして、Presenterは、Viewに保持されるインスタンスで、Viewの初期化時にDagger 2 Componentによってinjectされます。

サンプルTodoアプリのTodo追加画面の実装は、以下のようになっています。

.. code-block:: java

  // Path
  @Layout(R.layout.todo_add) @WithComponent(TodoAddPath.Component.class) public class TodoAddPath
      extends Path {
  
      // Component
      @dagger.Component(dependencies = MyApplication.Component.class) @PerScreen
      public interface Component {
          void inject(TodoAddView v);
      }
  
      // Presenter
      @PerScreen public static class Presenter extends ViewPresenter<View> {
  
          @Inject Presenter() {
          }
  
          ...
      }
  }

  // View
  public class TodoAddView extends RelativeLayout implements ActionBarModifier, TodoAddPath.View {
  
      @Inject TodoAddPath.Presenter presenter;
  
      public TodoAddView(Context context, AttributeSet attrs) {
          super(context, attrs);
          DaggerService.<TodoAddPath.Component>getDaggerComponent(context).inject(this);
      }

      ...
  }

Activityは、アプリケーションでひとつしか存在しません。Square風MVPアプリにおいて、Activityは、Applicationと同様にシングルトン的な存在です。
ただし、Configuration ChangesでActivityは破棄されるので、常に同一のインスタンスであることを期待してはいけません。

また、各画面ごとのViewを格納するためのコンテナビュー(PahtContainerView)が、Activityに対してひとつあります。
スマホ用の1画面レイアウトと、 タブレット用の `マスター・ディテール <https://developer.android.com/intl/ja/tools/projects/templates.html#master-detail-activity>`_ のように異なるレイアウトを出し分けする場合には、コンテナビューもその分用意します。

サービスの追加
~~~~~~~~~~~~~~~~

Androidにおいて、Contextは、システムにアクセスするための重要な手段です。
ApplicationやActivity自身もContextの一種であり、通常、いつでもどこからでもアクセスすることが可能です。

Flow/Mortarでは、 `getSystemService() <http://developer.android.com/reference/android/content/Context.html#getSystemService(java.lang.String)>`_
をオーバーライドして、独自のサービスをContextに追加することで、システムを拡張するという方法を多用します。
たとえば、ApplicationやActivityのgetSystemServiceには、 `階層化されたスコープ <#mortarscope>`_ を提供するためのMortarScopeインスタンスや、
Activityのライフサイクルメソッドを肩代わりするためのFlowDelegateインスタンスを埋め込みます。

サンプルアプリでは、ApplicationのgetSystemServiceは以下のようになっています。

.. code-block:: java

  @Override public Object getSystemService(String name) {                                                                                        
      if (rootScope == null) {                                                                                                                     
          Component component = DaggerService.createComponent(Component.class, new Module(this));                                                    
          rootScope = MortarScope.buildRootScope()                                                                                                   
              .withService(DaggerService.SERVICE_NAME, component)                                                                                    
              .build("Root");                                                                                                                        
      }                                                                                                                                            
      return rootScope.hasService(name) ? rootScope.getService(name) : super.getSystemService(name);                                               
  }

また、これら以外にも `ContextWrapper <http://developer.android.com/intl/ja/reference/android/content/ContextWrapper.html>`_ 
を使用して、独自のContext定義し、機能を拡張するという手法も使います。
ContextWrapperは、Contextインスタンスを包んで追加の機能やフィールドを持たせるためのプロキシークラスです。
ContextWrapperの派生クラスを見ると、このクラスがAndroid SDK内でも多用されていることがわかります。

.. figure:: {filename}/images/android_mvp/context_wrapper.png
   :alt: ContextWrappers wrap Context

   ContextWapperはContextに機能を追加する

ContextをContextWrapperで何重にも包んでサービスを追加していくので、操作しているContextがどのContext
なのかをただしく認識するのが、コードを理解する鍵になってきます。それによって利用できるサービスが異なるからです。

追加されるサービス一覧
~~~~~~~~~~~~~~~~~~~~~~~~~

Flow/Mortarアプリで独自に定義される(非標準の)サービスとしては、以下のようなものがあります。
ただし、純粋に内部的なもので、アプリから直接は利用しないものも含まれます。

* Flow.FLOW_SERVICE(Flow): Flowインスタンスを提供する。
* LocalPathWrapper.LOCAL_WRAPPER_SERVICE(Flow): Contextに付随するPathを提供する。
* PathContext.SERVICE_NAME(Flow): Path固有のContextを提供する。
* MortarScope.MORTAR_SERVICE(Mortar): Contextに付随するMortarScopeを提供する。
* BundleServiceRunner.SERVICE_NAME(Mortar): Contextに付随するBundleServiceRunnerを提供する。
* DaggerService.SERVICE_NAME(アプリ): Contextに付随するDagger Componentを提供する。

MortarScope
~~~~~~~~~~~~

スコープ(MortarScope)は、Mortarの提供する主たる機能のひとつで、サービスの辞書を保持するオブジェクトです。また、スコープは、それ自身ツリー構造を成します。
実際のアプリでは、次の図のように、Rootスコープ(Applicationスコープ)、Activityスコープ、Pathスコープという3階層までになります。
なお、Pathスコープが2ノードになるのは、マスター・ディテールなど複数画面構成の場合のみで、1画面構成のアプリの場合は、常に1ノードです。

.. figure:: {filename}/images/android_mvp/scopes.png
   :alt: MortarScope consists tree structure

   MortarScopeのツリー構造

スコープインスタンスに対して、サービスの検索を要求すると、まず自分の持つ辞書に該当するサービスがあるかを検索し、なければ親に遡って検索していきます。
また、スコープに登録されるサービスがScopedインターフェイスを実装している場合には、スコープへの登録時にonEnterScope()が、スコープの破棄時に、onEnterScope()が呼ばれます。

.. code-block:: java

  public interface Scoped {                                                                                                                        
      void onEnterScope(MortarScope scope);                                                                                                          
      void onExitScope();                                                                                                                            
  }      

これらのメソッドで、前処理と後処理をすることで、スコープの寿命と同期したリソースの初期化と回収が実現できます。
たとえば、onEnterScopeで、そのスコープ内で有効なRealmインスタンスを取得し、onExitScopeでreleaseするRealmServiceのようなものを実装して、
サービスとしてスコープにに登録することも可能です。

スコープと、それに紐付けられたサービスは、Configuration Changesを生き残ります。Rootスコープは、Applicationによって保持されるインスタンスだからです。

Presenterのライフサイクル
~~~~~~~~~~~~~~~~~~~~~~~~~

Presenterには、次の4つのライフサイクルメソッドが用意されています。

* void onEnterScope(MortarScope scope): PresenterがScopeに登録されたとき(画面遷移時)に一度だけ実行される。
* void onLoad(Bundle savedInstanceState): Presenterのロード時に呼び出される。
* void onSave(Bundle outState): Presenterの中断時に呼び出される。
* void onExitScope(): PresenterがScopeから登録解除されたとき(画面遷移時)に一度だけ実行される。

.. figure:: {filename}/images/android_mvp/presenter_lifecycle.png
   :alt: Lifecyle of Presenter

   Presenterのライフサイクル

onEnterScopeは、Configuration Changeのたびに呼びだされることはありません。Configuration ChangeのたびにViewインスナンスは再構築されるので、Viewに依存した初期化などはここで実行することはできません。
onLoadのタイミングでは、実際のViewが生成されInflateも完了しているので、初期化処理はこの中でやるのが適切です。

onLoadは、ActivityのonCreateかViewの表示時(takeView)のタイミングで呼ばれます。onSaveは、ActivityのonSaveInstanceStateがトリガーになります。
onEnterScopeとonExitScopeのタイミングは、アプリの実装に依存しますが、通常は画面遷移時です。

Presenterには、ActivityのonStaret,onResume,onSuspend,onStopに相当するようなライフサイクルメソッドが存在しないため、実際のアプリ実装では若干機能が足りないことがあります。
たとえば、スクリーンオフになったときに、動画やオーディオの再生を停止したいといったケースには、上記のメソッドだけでは対応できません。
そういったケースでは、ViewのonDetachedFromWindowや、onWindowFocusChangedといったメソッドを駆使して対応します。

PathとPathContext
~~~~~~~~~~~~~~~~~

Flowでは、Viewが画面遷移の単位になります。
Viewと一対一で対応付けて、そのViewを識別するために用いられるのがPathです。

Flowでの画面遷移は、次のようなコードで実行されます。

.. code-block:: java

    public void onItemClick(int position) {
        Flow.get(getContext()).set(new TodoEditPath(todoItems.get(position).getId()));
    }

サンプルアプリでは、次のコードのように、@Layoutというアノテーションを使って、Pathとレイアウトファイルを関連付けています。
@WithComponentについては `後述 <http://localhost:8000/android_mvp.html#pathscoper>`_ します。

.. code-block:: java

  @Layout(R.layout.todo_list) @WithComponent(TodoListPath.Component.class)
  public class TodoListPath extends Path {
      ...

これ自体はFlowに用意されている仕組みではありません。Pathとレイアウトファイルを関連付けて、レイアウトファイルをinflateするといったあたりは、アプリ側コードになります(SimplePathContainer)。
ただし、定型処理なので、サンプルにあるものをそのまま使えば事足ります。

PathContextは、Pathインスタンスと対になるContextで、Path固有のサービスを提供します。
画面遷移の際には、直前のPathから親Contextを引き継いで、新しいPathContextを作成します。
そして、 `cloneInContext <http://developer.android.com/intl/ja/reference/android/view/LayoutInflater.html#cloneInContext(android.content.Context)>`_ で、
新しいContextを指定したLayoutInflaterによって、レイアウトファイルをinflateすることで、そのContextに紐付くViewインスタンスを生成します。
同時に、前の画面のPathContextは破棄します。
ちなみに、PathContextの親Contextは、Activityです。

.. figure:: {filename}/images/android_mvp/pathcontext.png
   :alt: PathContext

   PathContextは、遷移時に生成・破棄される

こうして、PathContextのサービスを利用可能なViewのセットアップ、および、そのクリーンアップがされます。

Flow
~~~~~

Flowクラスは、Flowを使うときの窓口になるクラス(いわゆる `Facade <http://c2.com/cgi/wiki?FacadePattern>`_ )です。
内部にHistoryインスタンスと、Dispatcherインスタンスをひとつづつ保持しています。
このクラスを通してバックスタック(History)を操作することで、画面遷移を行います。

Flowインスタンスは、FlowDelegateインスタンスの中に保持されます。
FlowDelegateインスタンス自体は、Activityに持たせますので、実質的に、Flowインスタンスはシングルトンのようなものです。

.. figure:: {filename}/images/android_mvp/flowdelegate.png
   :alt: FlowDelegate

   ActivityはライフサイクルメソッドをFlowDelegateに委譲する

また、FlowDelegateインスタンスは、上図のようにActivityのライフサイクルメソッドの委譲先となります。
これにより、適切にActivityのライフサイクルがハンドリングされ、アプリ側ではActivityのことを気にせずにすみます。

Historyのエントリーには、View階層の状態と、対応するPathオブジェクト自身が含まれます。

.. figure:: {filename}/images/android_mvp/history.png
   :alt: History

   Historyは、PathとViewの状態を保持する

Configuration Changesなど状態保存が必要なときには、Historyまるごと、Bundleの中にシリアライズされます。
View階層の状態は、 `saveHierarchyState()`__ で保存、 `restoreHierarchyState()`__ で復元されます。

.. _saveHierarchyState: http://developer.android.com/intl/ja/reference/android/view/View.html#saveHierarchyState(android.util.SparseArray<android.os.Parcelable>)

__ saveHierarchyState_

.. _restoreHierarchyState: http://developer.android.com/intl/ja/reference/android/view/View.html#restoreHierarchyState(android.util.SparseArray<android.os.Parcelable>)

__ restoreHierarchyState_

また、Pathは、アプリ定義のシリアライザー(StateParceler)で、シリザライズ・デシリアライズされるのですが、サンプル実装では、GsonParcelarというGsonを使った実装になっています。
したがって、PathはGsonでシリアライズ可能なオブジェクトでなければなりません。

PathContainerView
~~~~~~~~~~~~~~~~~~

Viewは、PathContainerViewの子ViewとしてViewツリーに追加されます。それらは、PathContainerに管理されます。
そして、PathContainerViewは、Activityによって表示されます。PathContainerViewは、マスター・ディテールなどの場合に複数になることがあります。

.. figure:: {filename}/images/android_mvp/pathcontainer.png
   :alt: PathContainer manages child views

   PathContainerは子Viewを管理する

FlowDelegateは、コンストラクターでDispatcherインスタンスを引数に取ります。
画面遷移が起きたときには、Dispatcher#dispatchが呼ばれて、そこから最終的には、PathContainer#performTraversalが呼ばれます(呼ばれるようにアプリコードを構成します)。
このperformTraversalの中で、Viewの入れ替えや、アニメーションの実行、PathContextの生成・破棄といった処理を行います。
これらの処理は、Flowの外側の部分なのでアプリの責務の範囲ですが、Flowのサンプル実装で提供されているSimplePathContainerをそのまま使えば、十分です。

状態の保存と復元メカニズム
~~~~~~~~~~~~~~~~~~~~~~~~~~~

History(バックスタック)や、View固有の状態(onSaveで保存されるもの)などは、すべてBundleに保存されます。

Bundleへの状態保存とBundleからの復元は、BundleServiceRunnerが行います。
このインスタンスは、Activityのスコープにサービスとして登録されるので、アプリから見れば、実質的にシングルトンです。
また、このオブジェクトは、保存の大本になるルートBundleを保持します。
BundleServiceRunnerは、ActivityのonCreate/onSaveInstanceStateをトリガーとして、保存と復元を行います。

.. figure:: {filename}/images/android_mvp/bundle_tree.png
   :alt: Bundle Tree

   Bundleはツリー構造を成す

ルートBundleの下には、スコープのパスをキーとして、スコープごとのBundleが格納されます。
そして、スコープごとのBundleの下には、Bundlerインスタンス毎にBundleがぶら下がります。
Bundlerは、Scope毎にリソースを管理するためのインターフェイスです。

.. code-block:: java

  public interface Bundler {                                                                                                                       
      String getMortarBundleKey();                                                                                                                   
      void onEnterScope(MortarScope scope);                                                                                                          
      void onLoad(Bundle savedInstanceState);                                                                                                        
      void onSave(Bundle outState);                                                                                                                  
      void onExitScope();                                                                                                                            
  } 

PresenterもBundlerを内部に保持しており、同名のライフサイクルメソッドも、これに準じたタイミングで実行されます。
Presenter用のBundlerでは、クラス名が保存用のキーになります。

Componentのスコープと階層化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Presenterインスタンスは、Configuration Changesを生き残るためにシングルトンである必要があります。
これを実現するために、Dagger 2のScopedインスタンスの機能を使います。

Scopedインスタンスとは、インスタンスのプロバイダーに@Singletonのようなアノテーションを付けておくと、
そのインスタンスが、Componentの寿命の範囲内で使い回される、というDagger 2の機能です。

たとえば、サンプルアプリでは、次のようなDagger 2モジュールが定義されています。

.. code-block:: java

  @dagger.Module public static class Module {
      @Provides @Singleton RealmConfiguration provideRealmConfiguration() {
          return new RealmConfiguration.Builder(context).build();
      }
  }

  @Singleton @dagger.Component(modules = Module.class) public interface Component {
      RealmConfiguration provideRealmConfiguration();
  }

RealmConfigurationには@Singletonアノテーションがついているため、同一のComponentインスタンスを使用する限り、何度injectしても、同一のインスタンスが使い回されます。

Dagger 2では、オブジェクトグラフに含まれるインスタンスは、Componentインスタンスを通して取得できます。
そして、Component自体を他のComponentに依存させることで、オブジェクトグラフを階層化することができます。

階層化されたオブジェクトグラフにおいて、他のComponentに依存するComponentは、依存されるComponentとは異なるスコープを持つ必要があります(依存するComponentのほうが寿命が短かくなります)。
そのことを表現するために、必要に応じて、@Scopeアノテーションを定義する必要があります。
異なるComponent階層に対して、同じ@Scopeアノテーション(例えば@Singleton)をつけようとしても、ビルドエラーになってしまいます。
なお、ここで言うスコープは、Mortarのスコープとは異なるもので、直接の関係はないので注意してください。

.. figure:: {filename}/images/android_mvp/components.png
   :alt: Component Hierarchy

   Componentの階層化

筆者の提案するMVP構成では、Rootスコープと、Pathスコープという2種類のスコープを定義します。
Rootスコープ用には、標準の@Singletonをそのまま使い、Pathスコープ用には、画面毎のスコープという意味で、@PerScreenスコープを新設します。

Rootスコープには、アプリケーション全体を通じて有効なオブジェクトを置き、Pathスコープには、画面毎に必要に応じたオブジェクトを置きます。
PathスコープのComponentインスタンスは、次節の仕組みにより、画面を去るときにいっしょに破棄されます。

PathScoper
~~~~~~~~~~~

サンプルアプリでは、他の人のやりかたを参考にして、@WithComponentというアノテーションを導入しました。
これをPathに付与することで、PathとComponentを対応付けます。

.. code-block:: java

  @Layout(R.layout.todo_list) @WithComponent(TodoListPath.Component.class) public class TodoListPath
        extends Path {
  
    @dagger.Component(dependencies = MyApplication.Component.class) @PerScreen
    public interface Component {
        void inject(TodoListView v);
    }

    ...

そして、Pathへの遷移時に、リフレクションでComponentクラスを検索して、Componentインスタンスを生成し、PathレベルのMortarScopeに紐付けます(MortarContextFactory)。
これをやるためのヘルパーとして、PathScoperというクラスを作成しました。
Androidのリフレクションは重いということなので、一度検索したComponentとModuleコンストラクタはキャッシュするようになっています。

Componentインスタンスは、PathレベルのMortarScopeの管理下にあるため、画面遷移時にきちんと破棄されます。
また、Rootスコープ(Applicationレベル)のオブジェクトグラフは破棄されずに残ります。

PathScoperでは、ApplicationスコープとPathスコープの2階層構成を前提としており、PathレベルComponentの生成時に必要なApplicationレベルのComponentは、
ハードコーディングになっています。構成がこれ以上変更になることはないと思うので、これでも十分な気はしますが、さらなる柔軟性を追求する余地が残っています。

縦横での切り替え
~~~~~~~~~~~~~~~~~

Flowでは、ポートレイトとランドスケープで実装を切り替えることも容易です。

.. code-block:: xml

  <net.tai2.flowmortardagger2demo.view.TodoListView
      xmlns:android="http://schemas.android.com/apk/res/android"
      android:layout_width="match_parent"
      android:layout_height="match_parent"
      android:orientation="vertical"
      android:paddingLeft="10dp"
      android:paddingRight="10dp"
      >
    ...

画面を定義するViewのレイアウトファイルには、このように対象のカスタムViewクラスが埋め込まれる形となるので、
通常のリソース切り替えのメカニズムを使って、ポートレイト用とランドスケープ用のレイアウトファイルを切り替えることで、実装ごと切り替えることができます。
この方法には、カスタムViewもPresenterもまったく別実装にする、カスタムViewは切り替えるがPresenterは共有する、どちらも共通にするがレイアウトのだけ変化させるなど、
いくつかバリエーションが考えられます。

レスポンシブ対応
~~~~~~~~~~~~~~~~~

縦横の切り替えと同じ要領で、ルートのレイアウトファイルをスマートフォンとタブレットで分けることで、実装を変えるという方法があります。
Flowのサンプルアプリが、その方法でレスポンシブ対応をしているので、そちらを見ると良いと思います。
ただし、直近の変更でサンプルコードが削除されてしまったので、0.12以前をチェックアウトしてください。

ユニットテスト
---------------

MVPでは、ユニットテストがしやすくなるとよく言われますが、それは、主に、Presenterと具象Viewが、インターフェイスによって分離されているためです。
ところが、SquareのMVP実装では、画面の実装に利用するViewPresenterは次のようになっています。

.. code-block:: java

  public class ViewPresenter<V extends View> extends Presenter<V> {
      @Override protected final BundleService extractBundleService(V view) {
        return BundleService.getBundleService(view.getContext());
      }
  }

ここで、Viewは、android.view.Viewです。これでは、Presenterが具象Viewと直接結びついてしまうため、モックを使ってテストを実装するのがやりにくくなります。

幸い、基底クラスのPresenterはジェネリックになっており、付随するオブジェクトの型を変更できるので、以下のようにします。

.. code-block:: java

  public interface ContextHolder {
      Context getContext();
  }
  
  public class ViewPresenter<V extends ContextHolder> extends Presenter<V> {
      @Override protected final BundleService extractBundleService(V view) {
        return BundleService.getBundleService(view.getContext());
      }
  
      public final Context getContext() {
        return getView().getContext();
      }
  }

より具体的なViewのインターフェイスは、画面ごとにContextHolderを拡張して定義します。
これで、PresenterとViewの結びつきを間接化できます。
モックViewの定義も容易になり、以下のような感じでテストコードが書けます。

.. code-block:: java

  @UiThreadTest public void testAddClick() {

      presenter.onAddClick();

      getInstrumentation().waitForIdle(new Runnable() {
        @Override public void run() {
          Todo todo = realm.where(Todo.class).findFirst();
          assertNotNull(todo);
          assertEquals(mockView.getContent(), todo.getContent());
          assertEquals(TodoListPath.class, Flow.get(getActivity()).getHistory().top().getClass());
        }
      });
  }

もちろん、AndroidにはEspressoがあるので、このようなアプローチを用いる必要はないかもしれません。
実際、Espressoでは具象Viewをそのままテストできるので、カバーできている範囲はこのアプローチよりも広いです。

ただ、今回はMVPがテーマですので、よりMVPのメリットを活かせるユニットテストのアプローチを模索してみました。
両者を比較して、どのようなメリットとデメリットがあるのかは興味深い話題ですが、この記事の範囲外です。

Proguard設定
-------------

Proguard要らずが本来のDagger 2の売りのひとつではありますが、
本稿の手法では、Dagger 2の自動生成するクラスをリフレクションで検索するので、それに関連したクラスをProguardから除外します。

.. code-block:: txt

  -keep @dagger.Component public class *
  -keep @dagger.Module public class * { *; }
  -keep class net.tai2.flowmortardagger2demo.**Dagger** { *; }

まとめと展望
-------------

この記事では、Flow/Mortar/Dagger 2を使用したMVPアーキテクチャによるAndroid実装のメリット・デメリットを分析し、その後、ライブラリの詳しい使い方と内部のメカニズムを見ました。

メリットは、Fragmentを使用しないことなどによる安定化や、MVCとは違ったアプローチの自動テストが可能になることでした。
一方、デメリットは、標準的な方法を外れることによる、高い学習コストや、機能の不足、またボイラープレートの増加などです。

Flow/Mortar/Dagger 2とアプリ自身、それぞれの受け持つ責務の振り分けについて学び、各画面の基本的な構成が、View,Path,Presenter,Componentの4つから成ることを学びました。
Flow/MortarがContextWrapperによる機能拡張を多用することを見て、MortarScopeを軸としてツリー構造を形成しつつ、
Flow,History,PathContext,Presenter,Bundler,Componentといった要素が連携してアプリを構成することを学びました。
また、SquareのオリジナルMVPに変更を加えて、Presenterを直接テストするための方法を学びました。

現状で、Flow/MortarとDagger 2を組み合わせたアプローチは、まだ決定的なやりかたが確立されておらず、Flow/Mortarの進化と共に変わっていくと思います。
Flow/Mortarを利用することで、かえってボイラープレートが増加し、煩雑になってしまっている部分があるのが、大きな欠点です。
それらの欠点については、Dagger 2自身のアプローチと同様、アノテーションとコード生成あるいはリフレクションを活用することで、改善の余地があります。
実際、 `lukaspili/Auto-Mortar <https://github.com/lukaspili/Auto-Mortar>`_ や、 `lukaspili/Auto-Dagger2 <https://github.com/lukaspili/Auto-Dagger2>`_
といった試みが出てきているので、これらを活用することで、記述量を減らせるかもしれません。

参考文献
----------

* `Simpler Android apps with Flow and Mortar <https://corner.squareup.com/2014/01/mortar-and-flow.html>`_ Flow/Mortarのメイン開発者の１人であるRay Ryanによる紹介記事。ただしAPIが古い。
* `Advocating Against Android Fragments <https://corner.squareup.com/2014/10/advocating-against-android-fragments.html>`_ SquareがFragmentをやめてMVPに移行した理由の説明。
* `【翻訳】Android Fragmentへの反対声明) <http://ninjinkun.hatenablog.com/entry/2014/10/16/234611>`_ 上記の翻訳。
* `An Investigation into Flow and Mortar <https://www.bignerdranch.com/blog/an-investigation-into-flow-and-mortar/>`_ Flow/Mortarの解説。ただしAPIが古い。
* `Fragments vs. CustomViews に一つの結論を出してみた <http://qiita.com/KeithYokoma/items/9e049f12ca38d942e4fd>`_ Fragmentとカスタムビューベースの設計の比較。
* `Snorkeling with Dagger 2 <https://github.com/konmik/konmik.github.io/wiki/Snorkeling-with-Dagger-2>`_ Dagger 2の解説記事。おすすめ。
* `Dagger 2 - The redaggering - Google Slides <https://docs.google.com/presentation/d/1fby5VeGU9CN8zjw4lAb2QPPsKRxx6mSwCe9q7ECNSJQ/pub?start=false&loop=false&delayms=3000>`_ DIライブラリの進化の歴史。
* `BowerとMacGlashanのMVP論文要約 <http://blog.tai2.net/bower-and-macglashan-mvp-architecture.html>`_ 現在普及しているMVPの原型を提案した論文の要約。
* `pyricau/dagger2-mortar-flow-experiment <https://github.com/pyricau/dagger2-mortar-flow-experiment>`_ Square社員のPierre-Yves RicauによるFlow/Mortar/Dagger 2の試案。
* `lukaspili/Mortar-Flow-Dagger2-demo <https://github.com/lukaspili/Mortar-Flow-Dagger2-demo>`_ Flow/Mortar/Dagger 2のデモ実装。
* `JakeWharton/u2020 <https://github.com/JakeWharton/u2020>`_ Jake WhartonがSquare製ライブラリてんこ盛りで作ったサンプルアプリ。Flow/Mortarは使っていないが、Dagger 1は使っている。
* `EligijusStarinskas/U2020-mortar-flow <https://github.com/EligijusStarinskas/U2020-mortar-flow>`_ 上記のアプリをFlow/Mortar/Dagger 2でリメイクしたもの。

----

.. raw:: html

  <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br />この記事のライセンスは、<a href="http://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>とします。

