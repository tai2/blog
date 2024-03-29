人月の神話
############

:date: 2022-2-28
:slug: the-mythical-man-month
:summary: 人月の神話をひさしぶりに読んでみた

`人月の神話 <https://www.amazon.co.jp/dp/4894716658/>`_ をひさしぶりに読んでみた。

人月の神話は、フレデリック・ブルックスの超有名古典的エッセイ集で、ソフトウェアエンジニアリングに関する多岐にわたるトピック取り扱っている。その中でもとくに有名で、よく世間で言及されるのは、表題にもなってる「人月の神話」と「銀の弾などない」、それから「セカンドシステム症候群」あたりだろうか。

はじめて読んだのは20年くらい前。社会人になったばかりのころ、満員電車にゆられながら、「へー人を増やしても開発ってうまくいかないのねー」などとわかったような顔をしながら読んでいたのを覚えている。当時は職業プログラマとしての経験を積む前で、本を読んでも鵜呑みにすることしかできなかった。でも、熟練のプログラマとして経験を積んだいま読んだら、またなにか違った洞察を得られたりするかもしれない。読み返してみた動機はそんな感じ。

.. contents:: 目次

現代のプログラマにとって有益か
==================================

改めて読んでみて、とくべつすごい感動したとかはなかったんだけど、人月の神話とセカンドシステム症候群あたりは、いまでも危険な兆候を察知したり、当てはまりそうな状況のときに自説を補強する材料として使ってみてもいいのかもしれない。人数を増やせば単純に生産性があがるという直感から来る思い込みは根強いし、人月にまつわるコミュニケーションの諸問題が広く常識として定着することは永遠になさそう。

この本をまだ読んでいない人に薦めるかと言われれば、さすがに同様のトピックを扱っていてもっと現代的な書籍はぜったいあるはずなので、違う本を読んだ方がいい、気がする。ただ、具体的にどれと言われると知らない。ぼくが読んだことある本だと、 `実践ソフトウェアエンジニアリング <https://www.ohmsha.co.jp/book/9784274227943/>`_ とか、たぶんほとんどのトピックを扱ってそうだけど、いかんせん...すごく退屈で読んでもぜんぜんおもしろくない本なので、あんまりおすすめできない...。おすすめがあれば教えてください。

やっぱり本質と偶有がわからない
===============================

    「技術においても管理手法においても、それだけで十年間に生産性や信頼性と容易性での飛躍的な改善を一つでも約束できるような開発は一つとしてない」

この業界の人間なら聞いたことくらいはあるであろう銀の弾丸の議論、その元ネタがこの本に載っているエッセイのひとつ「銀の弾などない」です。このエッセイでは、ソフトウェア構築を「複雑な概念構造体を作り上げる」本質的作業と「抽象的な実在をプログラミング言語で表現」する偶有的作業に分ける。その上で、これまでのソフトウェア開発は、主に偶有的な作業にまつわる困難を取り除くことで進歩してきた、しかし、これ以上偶有的な困難を取り除いても「大きな収穫」は得られないとする(ブルックスの主張では、偶有的困難の占める割合は全体の半分以下)。さらに、今後10年(1986年〜1996年)に本質的な困難を飛躍的に改善する技術はひとつも現れないとブルックスは断言する。では飛躍的な改善とはいったいどれくらいなのか。これは「生産性で十倍の改善」であれば十分らしい。(ちなみに、現代に置いても偶有的作業の占める割合のほうが圧倒的に大きいぞコノヤローっていう `反論 <https://danluu.com/essential-complexity/>`_ もある)

この本質的と偶有的という議論の核となる区別、考えれば考えるほどわからなくなってくる。

「難しさの本質とはソフトウェアの性質に固有な困難のこと」で、「偶有的難しさとは実現するとき派生するが本来備わっているものではない困難」なのだそうだ。そして、1986年までに偶有的困難を解決することで飛躍的な改善をもたらしてきた技術として「高水準言語」「タイムシェアリング」「UNIX」を挙げている。

ブルックスは言語を本質からは独立したものとして考えているようなふしがある。しかし、言語とそのランタイムは切り離して考えられないと思う。そして、言語で何が実現できるかという「本質的」なことにおいては、言語そのものよりもライブラリや動作モデルなど含めたランタイムがより重要な気がする。たとえば、サーバーにRubyを使うかNode.jsを使うかでは、ランタイムの動作モデルが根本的に違うので、どちらを使うかでシステムの設計・構成そのものが部分的にせよ変わる、ということはあり得ると思う(もっとも最近はRubyでもFiberが浸透してきてるのでNode.js的な非同期ベースなノリの設計ができるのかもしれないけど)。あるいは、マイクロサービスのコンポーネントをPHPで実装することもできはするだろうけど、現実的には多くの企業が、たぶんそのランタイムの利便性から、マイクロサービスの実装言語としてGolangとかを選択したりしているんじゃないだろうか。つまり、言語の選択というのは偶有的ではなく本質的なことに思える。

なにが偶有的作業で、なにが本質的作業なのか。よくわからないなりに云々うなりながら考えていたら、ひとつ使えそうな切り口を思い付いた。対象のプロダクトによって変わる作業、domain specificな作業というのが本質的で、開発対象によらず一定の作業、general purposeな作業というのが偶有的。こう考えるとうまく分類できるのではないか。この切り口で考えると、開発ツールが扱う問題は偶有的な問題ということになる。つまり、プログラミング言語、テキストエディタ、LSP、Coreutilsのような汎用性のあるユーティリティーなどは、すべて偶有的な解決策。ブルックスが「高水準言語」「タイムシェアリング」「UNIX」を挙げたのも当てはまる。逆に本質的な解決策というのは、特定の問題にしか役立たないもの。たとえば、音声を認識してテキストを抽出するという問題とか、インターネット上で人々が議論できる空間を実現するという問題とか、家計を管理するという問題とか。開発者ではなくエンドユーザーに価値を提供する解決策とも言ってもいいかもしれない。つまり、開発ツールがいくら進化しても、エンドユーザーに直接価値を届ける上で汎用的な解決策は存在しないよってこと? お、なんかそれっぽいかも? でもブルックスの言う本質的作業と偶有的作業からはすこし離れてしまったような気もする。やっぱりよくわからない。

それから、本質的攻略と新技術の違い。そして、生産性というのが何を意味しているのか。このあたりもよくわからない。ブルックスがIBMで開発をしていた時代から、いまに至るまで、新技術が途切れることはなかっただろうし、ソフトウェア領域での新技術が現れないなどとは考えていなかっただろうから、きっと新技術とブルックスの言う本質的攻略は別ものなんだろう。新技術は、これまでできなかったことをできるようにしたりするから、生産性やら信頼性やら容易性やらを飛躍的に向上させると思う。たとえば、OpenCVというライブラリが現れたことで手軽に画像認識アプリケーションを開発できるようになったし、Unityのような汎用ゲームエンジンの登場で3Dゲームの開発の生産性が飛躍的上がったり、Google Mapsによって地図ベースのアプリケーションが開発できるようになったりした。ブルックスが予言した時代の範疇で言えば、デスクトップとGUIライブラリによってユーザーにとっての使い勝手が飛躍的によくなったり。つまり、新しい技術で新しい価値が提供できるようになることは、飛躍的な生産性の向上とは言わない? 「生産」とはいったい。しかしまあ、こういった新技術がどの時代でもどんどん出てくるのはあたり前なので、そこから考えると本質的な攻略は、個別の特定分野を対象とした新技術ではなく、広範囲に適用できる技術でなければならないんだろう、きっと。

と、ここまで考えてきて、ブルックスが人月の神話の95年版を書いた後に、本質的な解決、銀の弾丸に限りなく近いものが登場したことに思い当たる。それは、インターネットの普及、そしてそれに付随して登場した、オープンソース、パッケージマネージャ、クラウドサービスあたりの台頭だ。単一ではなく複合的だという理由でつっぱねられる可能性はなきにしもあらずだけど、これらの組み合わせが、現在我々が生産できるソフトウェアのレベルを飛躍的に引き上げているのは事実だろう。実際、ブルックス自身、本質への有望な攻略のひとつとしてソフトウェア製品を挙げていて、これはその延長線上にあるものだと思う。

まあしかし、けっきょく銀の弾丸ってただの未来予測で、それが当たってたからと言って、だからなんなのという話ではある。本質と偶有に分けて考えることが、我々一介のプログラマになにか有用な示唆を与えてくれる気もあまりしないし。けっきょく我々がやることは、いま使える技術でシステムを作るだけなんだから、銀の弾丸はないと宣言されたところで、はいそうですかって話でしかないんだよな。

自分の経験と照らし合わせての感想
===================================

自分のプログラマとしての経験照らし合わせて、人月の神話の各トピックごとに語ってみる(とくに言いたいことがないトピックは省略)。

タールの沼
-----------

システムの開発コストは、コンポーネントの足し算ではない…と言われても、そんなでかいシステム関わったことないから、よくわからない。システムのでかさのせいでコストが異常に増大してるパターン…うーん、あったかな。多くの場合、各コンポーネントができて、それを組み合わせれば、わりと素直に動いてた気がする。もちろん組み合わせる時に多少の想定外とかはあるけど、ちゃちゃっと修正して、問題洗い出すだけでふつうに対応できてた。システムの規模がさらに大きくなって何階層にもなってたら、組み合わせた時の問題が大きくなるというのは、なんとなくなら想像できる。
ただ、そんなに巨大なシステム(数十人から数百人のプログラマがかかわるシステム)ってなんなんだろうというのは、経験してこなかったし、たぶんこれからも経験しないで終わるのかもしれない。

そもそも現在においては、巨大なシステムを部分ごと分けて作って、それから一気にくっつけてテストするという作り方をすることは、たぶんあまり普通じゃないし、それをやる必要もない。現代では、最初から動くものを作って統合した状態で少しずつ育てていくというのがあたりまえなはず。

ブルックス本の時代と現代における大きな違いのひとつは「出荷」というものに対するスタンスの違いだと思う。ブルックスの作っていたのは、ハードウェア専用に作られた、ハードウェアと一緒に出荷することが前提のOSとかコンパイラその他といったものだ。ハードウェアとソフトウェア込みでのシステム一式として納品する先とかも決まったりしていて、スケジュールを通りに出荷することがものすごく大事だったんじゃないだろうか。

ぼくが普段扱っているような、すでに稼動しているウェブシステムだと、納期という概念があまりない。もちろん、いついつまでにこれこれをリリースするみたいなことをセールスに約束してたり、新規プロダクト立ち上げのときにビジネス状の都合で奮闘するといったこともまったくないことはないけど、基本的には動いているシステムを少しずつ改善していくという作業が主になる。すると、 `見積もりというものの重要性が相対的に薄れてくる。 <https://messagepassing.github.io/018-deadline/>`_

ただ、一方で確かにタールの沼に足を取られるような経験をしたことも何度かはある。そのようなプロジェクトでは、ビジネス上の希望と、おそらく未熟な見積もりスキルの両方から決められたデッドラインがあり、チームは寄せ集めで未成熟、アーキテクトの不在、単純な技術力不足といったいくつもの要因が重なっていたように思う。単一の要因が欠けていただけで派手に転んだプロジェクトというのは見たことがない。どんなプロジェクトでもなにかしら足りないものというのはあるものだけど、ひとつやふたつなら、みんなのアイデアとか誰かのがんばりでどうにかカバーできる。ただ、破綻したプロジェクトでは、それらの数が多すぎたように思う。ひとつやふたつの問題を工夫やがんばりで解消したところで焼石に水。つまり、後から呼ばれた外野から見ると、それらは最初から成功する見込みがまったくなかったように見える。

にも関わらず、なぜそれらのプロジェクトは走り出してしまったのか。走り出す時点で、とても成功する見込みのないひどい状態にあることに気づけなかったのか。あるいは気づいていたのに止まることができなかった？これらプロジェクトの失敗理由をブルックスの理論で説明できるだろうか。ちょっと試してみよう。(ここでは、失敗=出荷までこぎつけられなかったプロジェクトという意味で使っています)

人月の神話
-----------

まず、スケジュールを立てることの難しさを述べている「人月の神話」の話はたしかに当てはまる。事実として、それらの失敗プロジェクトにおいて、開始時に立てたスケジュールは、完全に間違っていた。ただ、付け加えるならスケジュールにさえ十分な余裕があれば問題なく完成していたかと言われると、ちょっと疑わしい。そもそもコミュニケーションはうまくいっておらず、コードと製品の品質は著しく低かった。もちろんタイトなスケジュールのために品質が下がったということもあるだろうけど、それ以前の根本的な問題があった気がしてならない。

貴族政治、民主政治、そしてシステムデザイン
-------------------------------------------

    「コンセプトの完全性こそ、システムデザインにおいてもっとも重要な考慮点である」

この主張は、プロジェクトの失敗についてなにか重要なことを言っている気がする。失敗したプロジェクトのいくつかでは、たしかにコンセプトの完全性がなかった。それは既存のなにかの焼き直しであり、継ぎはぎ細工であった。そういえば、すでに完成されたものの焼き直しで、ソースコードも流用できるから簡単だろうと下方に難易度が見積もられていたことも共通している。

    「コンセプトの完全性を得るには、デザインが一人ないしは互いに意見が同じ少人数の頭脳グループで考え出されなければならない」

これが実践できていれば、そして、その1人ないし少人数が十分に経験を詰んだプログラマであれば、プロジェクト成功の確率はかなり上がるんじゃないだろうか。継ぎはぎで成長して一貫性もくそもないシステムを１から刷新しようとしたことが、そもそも間違いだったようにも思える。それをわかっていれば、これは難易度がものすごく高いプロジェクトであることを着手前に認識できた...のかもしれない。

セカンドシステム症候群
--------------------------

さきほど言ったように、いくつかのプロジェクトは、既存システムの焼き直しだった。これらは「セカンドシステム症候群」であった可能性がある。というのも、どちらも、既存システムにある機能すべてを持つことを最初から前提としてしまったからだ。最初に核となる最小の動くシステムとして作成し、そこからイテレーションを経て育てていくというのが現代のソフトウェア開発における成功パターンだと思う。ところが、失敗プロジェクトでは、既存システムで実現している盛りだくさんの機能をすべて実現することを前提としてしまった。それらは一度は実現した、はっきりと形の決まっている機能であるため、再構築は容易であると見立てた。そして短いスケジュールを組んだ。ただし、再構築を行うのはオリジナルのチームとはまったく無関係どころか、別の会社だった。1度目のシステム構築を行った開発者との連絡はまともに取れず、心もとないドキュメントとソースコードだけも頼りに再実装を行う。最初から多数の機能を急いで実現しようとしているため、一個一個のコンポーネントの仕上がりもろくに検証されず、線表にしたがって最低限の動作確認だけして表面上動いているように見えたら、できていることにされて、生煮えのまま次の機能に取りかかる。もちろんろくに検証されていないので実際には一個一個の機能やコンポーネントが多数の不具合を抱えている。隠れた、あるいは見なかったことにされた不具合はどんどん蓄積していきやがて...。焼き直しだから、既存のコードがあるから簡単にできる。これらの言葉が聞こえてきたら、警戒した方がいいかもしれない。きっと、2度目だろうが何度目だろうが、システムの作り方は変えるべきじゃないのだ。いつも最小限だが完璧に動作するシステムからはじめて、成長させていくのが１番の正攻法なんだと思う。ブルックスの言うセカンドシステム症候群は、2度目のシステムで1度目以上に機能を盛り込んでしまうことへの警句だったけど、ぼくの経験からすると、1度目と同等を最初から目指している時点で危険なんだと思う。

命令を伝える
---------------

この章は、いかにしてコンセプトの完全性を達成するかについて述べている。失敗プロジェクトでは、ドキュメントがないことはなかったが、とても十分なドキュメントとは言えなかった。そしてドキュメントを書いた人とのコミュニケーションも困難だった。さらに、既存システムのコードがドキュメントの代替になると考えていた節がある。システム構築においてコードはドキュメントの代替にはならないと思う。ひとつには、コードに設計が内包されているのは事実だけど、コードは設計を伝えるには非効率的なんだと思う。コードの質が低い場合にはとくにそうだ。それから、コードを読む能力というのも人によってまちまちなのだから、ある程度の人海戦術的な局面を想定するのであれば、コード＝ドキュメントという考えはますます成り立たないだろう。まともなドキュメントなしに多人数で開発するのは、スケールしないし、精度も効率も悪すぎる。

バベルの塔は、なぜ失敗に終わったか
------------------------------------

コミュニケーションの問題は、間違いなくあった。失敗プロジェクトにおいても、ブルックスの推奨するような進捗や問題共有のための定例会議や、日常的なチャットベースでのコミュニケーションはあった。それにも関わらず十分なコミュニケーションが行われてはいなかったように思われる。一つには、開発は会社をまたがって行われ、発注と受注という主従関係で分断されていた。互いの組織内では活発なコミュニケーションが行われていたかもしれないが、組織を横断してのコミュニケーションは限定される。また、開発側は、問題を認識していてもそれをそのまま共有する動機はなくギリギリまで組織内部で対処しようとするため、別の組織からはなかなか中で起きている問題が見えてこない。ブルックスも指摘するように、組織におけるコミュニケーションの構造は、(組織の権限構造が木構造であるのとは裏腹に)ネットワーク構造なのだけど、このネットワークのノードを繋ぐ「点線」が十分でなかったとは言えるのかもしれない。

この事例だけ見ると、複数の会社が分担して開発することがそもそもよくないとも取られかねないけど、実際には、複数の外注会社が協力して開発して、それでもきちんとシステムを作り上げられたプロジェクトももちろんある。だから、これは唯一の原因ではなく、あくまでプロジェクトが抱えていたたくさんの問題のうちのひとつなんだろうと思う。体験的には、正常にまわっていたプロジェクトでは、組織間の壁が薄く、カジュアルにやりとりが行われていたような気がする。それから、アーキテクトがきちんと全体的なタスクの状況と問題を把握できていることも重要に思える。

一つは捨て石にするつもりで
-----------------------------

変化に備えることの重要性を述べている。失敗プロジェクトでは、実現すべき仕様は最初から変化していないため、この章の内容はあたらない。変化が要求されなくともプロジェクトは失敗する。

破局を生み出すこと
--------------------

この章は、まさになにがプロジェクトの破綻を生み出すのか、どう回避すべきなのかについて説明している。失敗プロジェクトを振り返るのになにか重要な知見を与えてくれるはずだ。ブルックスはマイルストーンを持つことが必要だと言っている。もちろん失敗プロジェクトにおいてもマイルストーンは存在した。だけど、それはブルックスの言う「ナイフの刃のような鋭さをもって定義」されてはいなかった。明確なマイルストーンとは、「コーティングは90%完了した」というような感覚的なものではなく、誰でも測定できる事実であるべきということだ。だから、それはチェックリストとして、例えば「ユーザーはウェブとスマホの両方から複数の商品を出品・取消できる」とか「何万件のデータに対して1秒以内に検索が完了する」というような形で定義されるものの羅列になるんだと思う。明確でないと、遅れに気づくこともできず、マイルストーンが意味をなさなくなってしまう。また、ブルックスはクリティカル法を用いてスケジュール管理することを推奨している。失敗プロジェクトには、「ナイフのような」マイルストーンも、クリティカルパス図も存在しなかった。それらが存在していれば、スケジュールの遅延はきっともっと早くにあぶり出されていた………ん？いやいやいやそんなものは無くてもスケジュールの遅れは明明白白だった。これらの管理ツールはきちんと使えれば有効なものではあるだろうが、それだけでプロジェクトの破綻を防げたとは到底思えない。

まとめ
========

* ブルックスの本は話が古くてわかりづらいので、現代のプログラマにはもっと適した本がきっとある
* システム開発の本質と偶有を区別しても、そんなにメリットなさそう
* 失敗プロジェクトは、複数の原因が重なって失敗した
* セカンドシステムは実際危険
* ブルックスの言っていることは、どれもたぶん大事なことだけど、失敗プロジェクトは、なにかもっとはじまる前の段階で、すでに失敗がはじまっていた気がしてならない

