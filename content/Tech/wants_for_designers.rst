プログラマーからデザイナーへの要望(主にアプリ開発について)
###########################################################

:date: 2015-07-27
:slug: wants_for_designers
:tags: workflow, design
:summary: アプリ開発においてのフローは、まずデザイナーがデザイン指示書を作成し、プログラマーが、なるべく忠実にそれを再現するように実装していくという順序になることがよくあります。これまでの経験を踏まえて、今後案件をはじめる前にデザイナー、あるいは、プロジェクトマネージャーやディレクターに読んでもらうための資料を作成することにしました。本稿では、開発過程で、プログラマーとデザイナーとのやりとりにおいて発生するいくつかの問題について説明し、より良いコラボレーションのありかたを模索します。

.. contents:: 目次

アプリ開発においてのフローは、まずデザイナーがデザイン指示書を作成し、プログラマーが、なるべく忠実にそれを再現するように実装していくという順序になることがよくあります。自然で現実的な発想ではあるのですが、実際の開発の過程では、この流れが思っていたほどスムーズにいかないこともあります。そこで、これまでの経験を踏まえて、今後案件をはじめる前にデザイナー、あるいは、プロジェクトマネージャーやディレクターに読んでもらうための資料を作成することにしました。本稿では、開発過程で、プログラマーとデザイナーとのやりとりにおいて発生するいくつかの問題について説明し、より良いコラボレーションのありかたを模索します。

問題の根っ子
=============

問題の核心を一言で言うと、「どんなプラットフォームにも技術的な制約がある」ということです。[ref]技術的な制約を越えて、あるいは縮小して、アイデアを実現するのがプログラマーの仕事だというようなことを言う人がいることは承知してます[/ref]アプリケーションあるいはシステムを具現化する役割であるところのプログラマーは、当然、取り組んでいるプラットフォームの技術的な制約を一番よく理解しています。理解しなければ具現化のしようがありません。一方、デザイナーはというと、UI上の視覚効果、ユーザビリティー、ユーザー心理などについてはよく理解していますが、その土台となっている技術的な詳細や制約については、あまり把握していない場合が多いでしょう。

最近は、どのプラットフォームも、たいていデザインガイドラインを用意しています。Appleであれば、 `Human Interface Guidlines <https://developer.apple.com/library/ios/documentation/UserExperience/Conceptual/MobileHIG/>`_ 、Androidであれば、 `Material Design <https://developer.android.com/design/index.html>`_ などです。これらを熟読して、そのプラットフォームの標準では、どういったUI要素をどのように使うことが可能なのかを把握しておいてもらえれば、話は早いです。[ref]プラットフォームの都合で標準のガイドラインがいきなり変わって、最新のガイドラインが、現在市場でメインターゲットとなる機種でサポートされていないため、役に絶たないという場合もありますが…[/ref] しかしながら、これまで仕事をしてきて、こういったガイドラインの内容をきちんと把握しているデザイナーにはあまり出会ったことがありません。また、たとえデザインガイドラインレベルで把握していたとしても、実装で生じ得るデザイン起因の問題を完璧に把握することは難しいでしょう。けっきょく、実装の問題は、実装をしなければわかりません。

.. figure:: {static}/images/concerns-of-programmers-and-designers.png
   :alt: Concerns of programmers and designers

   プログラマーとデザイナーの関心領域の違い

ガイドラインを読んで把握していなくても、市場に出回っている本物のアプリをたくさん調査して、アプリのUI的な構造がどうなっているのか具体的に把握するというやりかたをしている人はけっこういると思います。これは非常に効果的なやりかたで、どんどんやるべきだと思いますが、完璧ではありません。実際のアプリで実装されているからといって、それが必ずしも標準的なUIなのかはわかりませんし、簡単に実現できるものだとも限らないからです。ユーザー目線で魅力的に写る、ちょっと小粋なユーザーインターフェイスは、実は、ベンダーががんばって独自に実装した結果である可能性があるのです。[ref]たとえば、コンテンツをピンチイン・アウトで拡大縮小するという機能は、iOSでは標準のコンポーネントのみで実装できますが、Androidでは、標準では用意されていないので、自力で実装しようとすると(iOSに比べれば)めんどうだったりします[/ref]

もちろん、なんであれ技術的に可能なことは、実現することができます。しかし、プロジェクトの予算は常に限られていますので、なるべく効率的に配分する必要があります。非標準的な実装をするために工数が跳ね上がってしまうのであれば、標準的なUIをちょっとカスタマイズするぐらいにしておこう、という判断もあり得るかもしれません。もっともこれは、デザイナーやプログラマーの一存で決めることではないでしょうが。すくなくとも、その実装コストを判断するのにもっとも適しているのは、プログラマーです。

Web制作の場合 ー インブラウザデザイン(Designing in the Browser)
================================================================

静的なHTMLの制作では、アプリ開発とはすこし事情が違います。ある意味では、Web制作のほうがアプリ開発よりも一歩先を言っていると言ってもいいかもしれません。

Web制作においては、従来、大雑把な工程として、デザインとコーディングという2工程に分けて作業が進められてきました。前者は、Fireworks,Photoshop,Illustratorといったツールを使用して行い、それが完成してから、テキストエディタを使用してマークアップを記述するという流れがふつうだったようです。この場合も、先程論じたのと同様に、実装の段階で、技術的な制約が出てきて、デザイン通りに実装することが難しかったり、あるいは前工程に戻っての修正が必要になるといったことがあり得ます。

これは、デザインの工程が、2次元のビットマップあるいはベクタ画像を成果物としており、実質的に無制約であるのに対して、コーディングは、ブラウザ上に動的にレイアウトする作業であるため、より制約が強いからです。

.. figure:: {static}/images/html-constraint.png
   :alt: Constraint of HTML/CSS

   単なるビットマップ・ベクトル画像よりもHTML/CSSのほうが制約が強い

ところで、Web制作においては、デザイナー自身が、実装言語であるところのHTML/CSS(と多少のJavaScript)を習得しており、設計(デザイン)と実装(コーディング)を同じ人が担当する場合もすくなくはないでしょう。そこで、実装時に(ある意味で)無駄な苦労するぐらいであれば、最初から制約の強い環境でデザイン自体をしてしまおうという、インブラウザデザイン(Designing in the Browser)と呼ばれる流れが出てきました。この考えかたで作業を行えば、実質的に設計と実装の不一致はなくなります。最近のウェブでは、モバイルの台頭によりレスポンシブウェブデザインがふつうに求められるようになってきており、画角を固定した静的なレイアウトではなく、より動的なレイアウトが必要になってきていることが、こういった流れの背景にあるようです。

Webアプリ開発の場合
====================

静的なHTMLではなく、従来的なWebアプリケーション[ref]SPAの場合は若干事情が異なる可能性があります。わたしはSPAでのウェブアプリケーション開発は経験がまだないので、よくわかりません[/ref]の場合でも、ネイティブアプリ開発よりは状況が良いように見えます。Webアプリケーションでは、ビューやテンプレートと言われるファイル自体は、HTML+αの記述で書けるようになっている場合が多く、また、ネイティブアプリに比べて、ビジネスロジックとプレゼンテーション(ビュー)の、より明確な分離ができている傾向にあるように思います。ですから、デザインに加えて、ビューの実装自体を完全にデザイナーに任せるという役割分担も実現し易いのではないでしょうか。そうでなくても、デザイナーがHTML/CSSレベルまで落とし込んでくれれば、それをビュー実装に変換するのは容易なので、デザイナーの成果物=HTML/CSSという形で、プログラマーとデザイナーがうまく協業できているプロジェクトも多いでしょう。

.. figure:: {static}/images/roles-of-programmers-and-designers.png
   :alt: Roles of programmers and designers

   プログラマーとデザイナーの綺麗な役割分担

このように、デザイナーがプレゼンテーションの実装まで責任を負ってくれるのであれば、プログラマーはビジネスロジックに集中できます。非常にわかり易くて綺麗な役割分担です。

ネイティブアプリの場合
======================

ところが、(iOSでもAndroidでも)ネイティブアプリ開発では、ウェブのような綺麗は役割分担は難しいです。要因はいくつかあります。

まず、冒頭でも述べたように、デザイナーが、ネイティブアプリのアーキテクチャに不慣れなケースが多いように見受けられることです。ウェブブラウザについてはよく理解しているデザイナーが多いのですが、ネイティブアプリとなると、どのようなコントロールが使えるのかといったことや、基本的なアプリのナビゲーションなど、ガイドラインレベルの知識を持っていないデザイナーが多く見られます。また、アプリの実装となると、Webのようにブラウザとテキストエディタでは成立せず、XcodeやAndroid StudioといったIDEを使用してビルドすることが必要になるので、単に実行環境を作るだけでも、ハードルが高いようです。

ネイティブアプリでは、実際に、プレゼンテーションの実装がウェブよりもヘヴィーな作業であるように思います。iOSでは、Storyboardという優れたUIデザインツールが標準で用意されているので、ある程度状況が良いのですが、これ自体使うのに立ち入った知識が必要ですし、込み入ったレイアウトを実装するには、どうしてもプログラミングが必要になってきます。プレゼンテーションを実装するのに(大量の)XMLとJavaの必要なAndroidは、言うに及びません。さらに言うと、最近のアプリ開発では必須と言えるアニメーションの実装ともなれば、プログラミングをしながらの試行錯誤は必須です。つまり、これらのプラットフォームでは、プレゼンテーションの実装からプログラミング言語を完全に分離することができず、また、Webで学んだHTML/CSSの知識はまったく役に立たないのです。

こういった状況があるのは、ある意味でプログラマーの責任ではあります。つまり、プレゼンテーションの実装と、それ以外の実装が、ワークフローを意識して明確に分離をされていない環境を作ったのもまた、プログラマーだからです。理想論を言えば、プレゼンテーションの実装は、Webのようにビジネスロジックとは明確に分離されており[ref]できればHTML/CSSのようにプレゼンテーション単体で確認可能なのが望ましい[/ref]、また、デザイナーの理解できる言語で記述できるようになっているべきだし、そういう方向を目指すべきだと、わたしは思います。

イニシアチブの所在
===================

これまで、設計(デザイン)と実装(コーディング)の乖離から生じる問題について見てきました。また、ウェブ制作では、設計工程と実装工程の分離をやめることで、問題を解消するアプローチがあることを見ました。

ネイティブアプリ制作のワークフローとしてよくあるのは、冒頭で挙げたような、デザイン指示書作成(デザイナー) → 実装(プログラマー)という流れです。この流れだと、アプリUIの設計に関してイニチアチブを握っているのはデザイナーです。画面に入る要素の種類や配置を考えるのもデザイナーですし、ナビゲーション(画面遷移)を決めるのもデザイナーです。

けれども、この流れは本当に正しいのでしょうか。ネイティブアプリでは、ナビゲーションの種類や意味、バーの配置やそこに入れることのできる要素の制限など、UIのレギュレーションがウェブよりもはるかに厳しく定められています。デザイナーがガイドラインレベルの知識を持たないのであれば、それらの制約を正しく理解しているのはプログラマーだけです。逆説的ですが、それを理解しているが故に、(技術的な実現可能性を踏まえた上で)その枠から出る発想をできるのもプログラマーだという考えかたもできます。

そうだとすれば、デザイナーがプラットフォームの制約を理解せずに野放図に作成したデザインを実現するために、無闇に工数をかけるよりも、制約を理解したプログラマーがイニチアチブを握って、最初から無理のない設計をするほうが良いのではないでしょうか。プログラマーが骨組となる絵を描いて、その上で、細かい肉付けだけをデザイナーがする、という考え方です。

このように言えば、デザイナーは、プログラマーのように視覚表現の発想力がなく、デザイン原則を考えない人間に、そんな重要なことを任せられるかと怒ると思いますし、そうあって欲しいと思います。であれば、デザイナーには、プラットフォームについて、せめてガイドラインレベルでは理解しておいてもらいたいものです。それに、ソフトウェア開発の現場では、プログラマーの作業比重が(デザイナーと比べて)重くなりすぎているというのが現実なので、できるだけ負担を分けあいたいのです。それは、ソフトウェア開発市場におけるデザイナーの職域拡大にも結び付くことだと思います。[ref]開発現場で、プログラマーが偏重されているというデザイナーからの意見が、しばしば耳に入ってきます[/ref]

.. figure:: {static}/images/weight-of-programmers-and-designers.png
   :alt: Weight of programmers and designers

   アプリ開発では、デザイナーよりプログラマーのほうが負担が大きい

そうは言っても、現実には、やはり旧来通りのデザイン指示書→実装という流れになることが考えられます。そもそもワークフローそれ自体はデザイナーやプログラマーの一存では決められないことが多いですし、現状では、インブラウザデザインのようなフローをアプリ開発で実践するのは技術的に難しいからです。ですから、できる限りプラットフォームについて勉強しつつ、実装するプログラマーと相談しながら、柔軟に作業を進めていって欲しいと思います。わからないことがあったらプログラマーに聞くべきです。モバイルプラットフォームが未経験であれば、作業に入る前に、プログラマーに時間を取ってもらって、モバイルプラットフォームのアーキテクチャーについて、ひととおりレクチャーを受けるといいかもしれません。

プログラマーへの指示の出しかた
===============================

とりあえず、現実的なやりかたに従って、あらかじめデザイナーがレイアウト・デザインをして、それをもとにプログラマーが実装をするというよくあるフローで開発を進めるとします。これは、組版で例えると、アートディレクターとデザイナー、あるいはデザイナーとDTPオペレーターの関係に相当します。こういったやりかたをする場合に、指示を受けるプログラマーの側からすれば、このように指示を出してもらうとありがたいという具体的なポイントがいくつかありますので、説明します。目標は、無駄なコミュニケーションの削減による時間短縮です。

判断材料を提供する
-------------------

どんなものにもバグは入り込みます。たとえそれがデザインであったとしても、指定の詳細度が増せば増すほど、一貫性がない部分、指定の漏れなどミスが入り込む余地は増えてきます。最終的な成果物となるアプリでは、工数をかけてひとつひとつ機能を検証し、バグを潰していきますが、中間成果物であるデザイン指示書では、通常そこまでの検証は行いません。結果として、プログラマーの元には、多分に曖昧さや誤りの含まれた資料が届きます。これはデザイナーの努力不足とかではなく、ワークフローに含まれる構造的な問題なので、しかたのないことです。

このようなデザイン資料に含まれるバグは存在するという前提に立って、どういう資料作りをしてもらえるのがいいかを考えると、方針が見えてきます。

1. 記載する情報は必要最低限にする
2. 不足している情報を実装者が補うための判断材料を提供する

という2点がポイントになります。

一般的に言って、情報の量が多ければ多いほど、そこにミスの入り込む余地は増えます。すべてのUI要素のサイズやマージンなどを個別に手動で指定していたら、必ず、何箇所かは一貫性の無い部分や記述漏れが入り込むでしょう。そういったケアレスミスを防ぐために、情報を整理し、カテゴリーや階層化などの手段を用いて重複をなくし、資料のページ数や、余分な情報をできるだけ減らすのです。

そのためには、情報構造になんらかの意味を与えるという作業が必要になってくると思います。例えば、フォントに関する情報でも、見出し、メニュー、リストなどの整理をして、それにスタイルを紐付けるといった整理が考えられます。なにも難しいことはありません。HTML/CSSでやっていることと同じ考えかたをすればいいだけです。こういった考えかたに基いて資料が作成されていれば、実装をする際にも要素の意味を実装者が判断して足りない情報を補えるので、部分部分に事細かに指示が書き込まれていなくても、悩まずに作業が進められます。

あるいは、別のアプローチとして、PhotoshopやIllustratorなどから、直接レイアウト情報を網羅的に出力できる `Specctr <https://www.specctr.com/>`_ のようなツールもあります。こういったツールを使用することで、人の手によるミスを無くすという方向性もあり得ますので、検討する価値はあると思います。

検索性の高い資料
-----------------

デザイン資料の作成方法は、個々のデザイナーによりさまざまで、PDFにテキストで色々指示を書き込んで渡してくれる人もいれば、1画面のPNGを何枚も渡してくる人もいますし、あるいは、PSDファイルをそのまま渡してくる人もいます。

PSDでそのまま渡すというやりかたは、レイヤー構造自体が整理されて注釈が適切に付加されており、資料としてそのまま利用できるレベルになっているのというのであれば、あり得るのかもしれません。ただ、個人的にはあまりPhotoshopというツール自体使い慣れていないので、PSDそのままで渡されるとちょっと辛いです。

資料を作る際に考慮して欲しいことは、プログラマーは、それを何度も何度も繰り返し参照しながら、実装に落し込んでいくということです。ですから、その資料自体の検索性[ref]この場合の検索というのは、キーワード検索に限りません。見たい内容にすぐに辿り付けるように整理されているか、ということです。[/ref]が低いと、作業効率に直に響いてきます。個人的には、1冊のPDFかなにかにすべてまとまっていて、スクロールさせたり、キーワード検索をかければ、即座に必要な項目に辿りつけるという作りがいいと思っていますが、それに限らずとも、資料自体の使い方とセットで提示してもらえれば、なんでもかまいません。

カラースキーム
---------------

アプリケーションで使われる色の指定を効率良く伝達するには、カラースキームの作成が役立ちます。このときひとつやってもらいたいのが、色に名前を付けるということです。

デザインドキュメントに、逐一数値だけで記述されていると、見る側からすれば、どこで使われている色と共通する色なのか、パッと見て識別できません。とくにそれが微妙な色の違いの場合には、ミスにも繋がりかねません。

.. figure:: {static}/images/design-document-1.png
   :alt: Color scheme 1

   数値で色が指定してあるデザイン指示書

また、プログラムのソースコード内では、多くの場合数値には名前を付けて管理するので、最初から色に名前がついていれば、自分で考える手間が省けて助かります。色の命名方法は、これ自体色々やりかたが考えられますが、いくつか使用する色をピックアップして、その彩度違いのバージョンを末尾に数値を付けて表す、などが考えられます。それをさらにUI的な情報構造と関連付けて整理するというのも有効だと思います。

.. figure:: {static}/images/design-document-2.png
   :alt: Color scheme 2

   名前で色が指定してあるデザイン指示書

.. figure:: {static}/images/design-document-3.png
   :alt: Color scheme 3

   情報構造と関連付けて色が指定してあるデザイン指示書

レスポンシブ対応
-----------------

最近では、iOSでもAndroidともに、特定の画面サイズを想定して、固定サイズのキャンバスにデザインすることはできなくなりました。320x480のサイズ固定で考えれば良かった古き良き時代のやりかたは、もう通用しないのです。Webのようにインブラウザデザイン的な方法論を取ることもできません。

しかたがないので、心眼でレスポンシブなデザインをするしかないのですが、タブレットとスマートフォンで、大幅に見せかたを変えるようなことまでするとなれば、プログラマーとの密接な連携なしには実現できません。大中小など想定サイズをいくつかに分類して、そのパターンだけレイアウトを作成するというやりかたもありますが、まあ大変だと思います。

とりあえず、プラットフォーム毎に、レイアウトの実装をどのように行っているのか、どのような指定ができるのかというところまで把握した上で、デザインドキュメントを作成してもらえれば、やりとりがスムーズになると思います。そうしないのであれば、おおざっぱなイメージだけ作成して、細かい部分はプログラマーにまかせるしかありません。ともかく、これに関しては、わたし自身、デザイナーとどう連携するべきなのか、いまだに頭を抱えています。

インタラクション
-----------------

アプリは、紙とは違って、ユーザーが操作したら反応するものです。ボタンであれば、押したときに必ずなにかしら変化がありますので、通常の色だけでなく、押下時の色についても指定する必要があります。アプリのデザインでは、ユーザーが操作したときに、その要素にどのような変化が起きるのかについても、必ず考えてください。また、これはプラットフォームによって、どのような変化が起きるのかや、どのように指定するのかなど細部が異なるので、プラットフォーム個別の知識が必要になってきます。

プラットフォームごとに異なる自然な表現
---------------------------------------

iOSには、1次元または2次元の整列されたデータを表示するのに便利なテーブルビューというビューがあります。あるいは、データの一覧だけでなく、静的なレイアウトのためにも使うことができたりして、非常に便利です。これはiOSでは非常に一般的なものなので、デザイナーのみなさんも、このコンセプトをベースにデザインされることが多いようです。

一方、Androidにも、似たようなものとして、リストビューという標準のビューがありますが、これは、iOSのテーブルビューに比べるとだいぶ貧弱で、2次元のデータは扱えませんし、静的なレイアウトをするのにも向いていません。iOSのコンセプトに慣れている人が、Androidでもテーブルビュー的な考えかたを持ち込んでしまうと、プログラマーは苦労する場合があります。もちろん、iOS的な表現を実装すること自体は可能なのですが、iOSで実装するよりも工数がかかるかもしれないということです。UI的にどうしてもその表現が必要なのであれば、苦労してでも実装すべきですが、なんとなくiOSでそうなってるから合わせてみたというだけであれば、その決定は、無駄に工数を増やしているだけかもしれません。

また、ナビゲーションの概念も、iOSとAndroidで微妙に異なります。iOSでは、アプリのモードを瞬時に切り替えるタブビュー、ナビゲーションバーと関連付けられたナビゲーションビュー、その中に入るコンテンツというように、厳密に画面の階層構造が整理されています。一方、Androidでは、画面のナビゲーションはもっと自由です。Androidでは、画面下部にバックボタンがあることが前提になるため、基本的には左上の「戻る」ボタンは不要ですし、画面上部にアクションバーという多彩な機能を持ったバーがあり、これがUI的に色々な役割を果たします。

この他、iOSとAndroidで異なる部分を挙げればきりがありません。ともかく、同じモバイルでも、プラットフォームごとに自然なUIは異なるということを念頭に置いてデザインをしてください。プラットフォームのガイドラインを読んで自然なUIについて学び、なにが自然なのかわからなければ、プログラマーと相談してください。

まとめ
=======

* どんなプラットフォームにも技術的な制約がある
* ネイティブアプリ開発では、Webのような綺麗な作業分担が難しい
* わからないことはプログラマーに聞いて欲しい
* デザイン資料は検索性の良さを意識して作成して欲しい
* カラースキームを作るときは、色に名前を付けて欲しい
* レスポンシブ対応は難しいけど協力してがんばろう
* UI操作時のインタラクションまで考えて欲しい
* プラットフォームごとの特性について学んだ上でデザインして欲しい

