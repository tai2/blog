AppiumをCLIから操作するためのツールaco (Appium Command-line Operator)を作った
===============================================================================

:date: 2026-6-28
:slug: aco-appium-command-line-operator
:summary: モバイル自動化におけるページソースは、ウェブのページソースと本質的に違り、さまざまな困難を伴う
:lang: ja

業務でモバイルテスト実行システム(Appiumベース)を作っていると、AppiumやAUT(テスト対象アプリ)の挙動を実験して確認したいことが頻繁にある。 `安定したスクロール量を実現するためのスワイプのしかたを模索したり <https://github.com/tai2/appium-meetup-tokyo-2-swipe-experiment>`_ 、シミュレーターのバージョンごとの起動時間の違いを調べたり、特定の画面でどのようなアクセシビリティーIDが利用可能なのか調べたり、等等等。

Appiumはクライアント・サーバーアーキテクチャのシステムなので、使うためにはまずサーバーを立ち上げる必要がある。そのために、 `Appiumと必要なドライバーをインストールする必要もある <https://appium.io/docs/en/latest/quickstart/install/>`_ (もっと言うと前提としてNode.jsもだし、XcodeやAndroid Studioの設定も)。まあ、それはいい。次にクライアント側だけど、これは通常何らかの言語でサーバーに接続するためのスクリプトを書いて、自動化手順を実装する。ここが一つのハードルになる。Appiumのセッションを確立するためには、capabilitiesと呼ばれるパラメータ群を指定する必要があるのだけど、これが正しく記述できないとそもそも使いはじめることができない。 `Appium Inspector <https://github.com/appium/appium-inspector>`_ というGUIのクライアントもあるけど、これは単純なプロトコルのラッパーなので、使うのに必要な知識が減るわけではない。capabilitiesは全部手書きで指定しなければならない。これらは、まあ一度確立できれば使いまわせることではあるけれど、単にtapやswipeをアプリ上で実行したいだけなのに、いちいちサーバーを起動して、書き捨てのスクリプトを用意してとやらなければならないのは、依然としてめんどくさい。

そこで、Appiumを極限まで簡単に使えるようにするためのコマンドラインツールを作った。名前はaco (Appium Command-line Operator)。

https://www.npmjs.com/package/@tai2/aco

どのように簡単かというと、プラットフォームとビルドファイルだけ指定すれば、もうセッションが開始できる。

.. code-block:: bash

   aco session start --platform ios --app /tmp/MyApp.app.zip

肝は、サーバーも裏側で起動した上で、capabilitiesも適切に構築してくれるので、正確なフォーマットを知らなくてもとりあえず動かせるということ。そして、セッションが開始できたら、もうコマンドを送信できる。

.. code-block:: bash

   aco tap --x 100 --y 200

ここで第2のポイント。セッション情報はファイルに保存されているので、セッションIDなどを指定する必要はない。最後に起動したセッションが自動的に選択される(複数セッションがある場合は、パラメータで指定することもできる)。

主な目的はAppiumの機能をいろいろ試すことなので、Appiumのすべての機能にCLI経由でアクセスできるように網羅的にコマンドをデザインし、網羅性を完全にするために脱出口も用意した。XCUITestDriverとUIAutomator2Driver固有の拡張コマンドもすべて、:code:`aco io` と :code:`aco android` サブコマンド以下からアクセスできる。さらに、CLIからアプリを操作するために便利な機能もいくつか用意した。たとえば、:code:`aco elements` を使うと、現在スクリーン上にあるうちでラベルを付与されたすべての要素と、その要素にアクセスするためのセレクターを一覧できる。

.. code-block:: bash

   $ aco elements
   #0  android.widget.TextView  "VoicePost"
         selector: -android uiautomator:new UiSelector().text("VoicePost")
         rect: 32,101 183x54
   #1  android.view.ViewGroup  "Open settings"
         selector: accessibility id:Open settings
         rect: 1000,102 48x51
   #2  android.widget.TextView  ""
         selector: -android uiautomator:new UiSelector().text("")
         rect: 1000,102 48x51
   #3  android.view.ViewGroup  "Start recording"
         selector: accessibility id:Start recording
         rect: 350,378 380x380
   #4  android.widget.TextView  ""
         selector: -android uiautomator:new UiSelector().text("")
         rect: 431,455 218x225
   #5  android.widget.TextView  "00:00"
         selector: -android uiautomator:new UiSelector().text("00:00")
         rect: 473,880 121x64
   #6  android.view.ViewGroup  "Start recording"
         selector: accessibility id:Start recording
         rect: 331,984 419x120
   #7  android.widget.TextView  "Start recording"
         selector: -android uiautomator:new UiSelector().text("Start recording")
         rect: 435,1016 267x56

ここに表示されているセレクタをそのまま :code:`--selector` パラメータに渡せば良い。

.. code-block:: bash

   aco tap --selector 'accessibility id:Start recording'

また、 :code:`aco source` コマンドの :code:`--xpath` パラメータを使えばページソースに対してxpathでフィルターをかけられる。

.. code-block:: bash

   aco source --xpath '//XCUIElementTypeButton[@name="Login"]' 

Claude Code用のプラグインも作ったので、Claude Codeを使ってモバイルのオートメーションをすることもできる。プラグインをインストールしたら、自然言語でオートメーションしたい内容を指示すれば、やってくれるようになる(はず、かもしれない…)。

.. code-block:: bash

   claude plugin marketplace add tai2/aco
   claude plugin install aco@aco

Appiumサーバー自体は、ユーザー自身の環境にインストールされているという前提で、それを利用する設計にした。なんとなく、モバイル自動化をやっている人なら、自分の環境にあるものをそのまま使いたいかもしれないし、Appiumサーバーとドライバー一式までacoに入れていっしょに配布すると大きすぎるような気がしたからだけど、セットアップをさらに簡単にするという意味では、それらも含めてしまってもいいかもしれない(数百MBあるけど…)。

コミットログを見ればわかるように、Claude Codeですべて作った。たぶん自分で一からぜんぶ書くとなったら、アイデア思いついても実行に移さなかった可能性もあるので、思いついたアイデアをすぐ形にできるのは、いい時代になったなあと思う。
