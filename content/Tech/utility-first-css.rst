Utility-first CSS(Tailwind CSS)が合理的であることの説明と、CSSによるUI開発小史
##############################################################################

:date: 2024-03-14
:slug: utility-first-css
:summary: CSSを記述するための手法は、カスケーディングというCSSの難点を克服しつつ、UIコンポーネントを開発するために進化してきた。Tailwind CSSを使えば、子要素への名付けなど余計なことに煩わされずに、コンポーネント実装に集中できる。

.. contents:: 目次

CSS小史
========

CSSでアプリのUIを実装するための手法は、これまでいくかの変遷を辿ってきた。

はるか昔、CSSが生まれて間もないころには、関心の分離という文脈から、FONT要素などの物理タグはよくないものとされ、
コンテンツ(HTML)とスタイル(CSS)をきっちりと分離することが奨励されはじめた。
そこでは、HTMLはあくまで文書であり、CSSのクラスセレクタという接点でコンテンツと見た目が隔離されることで、それらは別世界のものとして管理されていた。
また、大規模サービス開発においていかにCSSを管理するかという問題意識はまだなかった。

時が経ち、HTMLは次第に複雑な対象を記述するようになった。モジュールやメンテナンス性といったことがCSSコーダーの関心時になると、
BEMに代表される「方法論」が発明され、発展してきた。
これは、カスケーディングというCSSの「欠点」を克服する努力であると共に、スタイルの再利用への道を開いた。

そして、Reactのような、JavaScriptを使ってHTMLをUIコンポーネントのツリーとして記述する手段が発明されると、
CSS in JSという新しい考えかたが生まれた。
すべてのクラスが自動的にユニークであることが保証される世界において、マークアップエンジニアの頭痛の種であった詳細度の管理という問題は一掃され、
スコープの不存在というCSS最大の問題は完璧に解決された。
いまや、コンテンツとスタイルの分離やスタイルの再利用という考え方は希薄になり、HTMLとCSSはひとまとまりに記述されるのが当たり前のこととして受け入れられた。

最後に、Adam Wathanが、HTML/CSSにおける関心の分離という概念に含まれる矛盾を指摘してTailwind CSSを発明すると、
UIコンポーネント時代のフロントエンドエンジニアから一定の支持を得て広まっていった。
CSSクラスの再利用性は最大化し、HTMLとコンテンツの依存性はいまや完全に断ち切られ、クラスはコンテンツから独立した存在となった。

SUIT CSS - 命名規約ベースのCSS方法論
=======================================

CSSで素朴にスタイルを記述すると、 `いとも簡単に特定の要素に対するルールの衝突が発生する。 <https://www.phase2technology.com/blog/used-and-abused-css>`_
ルールが衝突したときにも、いい感じにスタイルが当たるように用意されているのが、CSSの名前の所以たるカスケーディングと、
詳細度にもとづいたルールの解決…なのだけど、これは非常に制御しづらく、往々にして予期しない出力を生み出す。

そこで先人達は、そもそもルールの衝突が発生しないように、一貫した規則に基いてクラス名を名付けることで問題を解決しようとした。
この命名規則の下では、ルールのセレクタは基本的にクラス一個なので詳細度が0-1-0に保たれる。
これならば、カスケーディングによる複雑で制御の難しいルール解決メカニズムをスキップできる。

SUIT CSSで `media object <https://www.stubbornella.org/2010/06/25/the-media-object-saves-hundreds-of-lines-of-code/>`_ を記述すると、以下のようになる。

.. raw:: html
    
    <iframe width="100%" height="400px" src="https://stackblitz.com/edit/media-object-suit-css?embed=1&file=src%2FMedia.css&view=editor"></iframe>

`Media object - SUIT CSS <https://stackblitz.com/edit/media-object-suit-css?file=src%2FMedia.css>`_ 
(CSSコーディングが下手糞かもしれないけど、大目に見てください...。)

`SUIT CSS <https://github.com/suitcss/suit/blob/master/doc/naming-conventions.md>`_ は、BEMに代表される命名規則によるCSS方法論の派生型のひとつ。
UIの状態を表現するための記法があるなど、UIコンポーネントのために使うことを意図した設計になっている。
react-native-webの作者である `Nicolas Gallagher <https://nicolasgallagher.com/>`_ が考案した。
CSS方法論は数多くあるけど、ぼくがCSS設計を教わった師匠からおすすめされて以来、Reactなどのモダンでない環境でCSSを書くときには、いまでもこれを使ってる。

これでCSSで大規模UIを記述する際のもっともつらい問題はたしかに緩和される。だけど、問題もある。
コンポーネント内の子要素に対して、クラスをどのように区切ってスタイルを適用するのがいいのかが自明ではなく、しばしば迷いが生じる。
CSSはHTMLから独立して(HTMLに依存せずに)考えるのが理想とされるにも関わらず、実際には、しばしばHTMLの構造を考えながらCSSを記述しなければならない。
なんならHTMLで構造を書いて、そこにクラスを振ってから、スタイルの中身を書いていくということも普通だ。
また、上のサンプルコードを見ればわかるように、CSSの世界でコンポーネントの構造を表現した上で、さらにHTMLの世界でも再度対応する構造を
表現している。非常に冗長だ。コンポーネントについて考えたり書くときには、つねにこの二度手間が発生する。

ぼくは、CSS方法論による実装は、いまとなっては、どうしても必要でなければ避けたほうがいいと考えている。これは実体験にもとづく。
いままでいくつかのプロジェクトで、CSS方法論を導入してみてわかったのだけど、多くのプログラマ、とくにフロントエンド技術にあまり興味
のないバックエンドエンジニアには、これを正しく使いこなすのは難しいのだと思う。
ふつうのプログラマは、CSSのカスケーディングや詳細度の存在すら知らないし、なぜCSS方法論が必要なのかが、そもそもわからない。
そして、CSS方法論は、なにか強制力のあるメカニズムではなく、あくまでただのコーディング上の約束事に過ぎない。
だから、クラスの衝突を避け、詳細度を一定に保つという方法論の基本原則から、簡単に逸脱してしまう。

もちろん、時間をかけて、それらの意味について教えて理解してもらうことはできると思うけど、以下に説明するように、現代では、
CSS方法論を用いずに、もっと賢くカスケーディングの問題を解決する方法が、他にある。

styled-components - CSS in JS
===============================

CSS in JSは、ReactなどのJSを使ってUIコンポーネントを記述する仕組みを前提としている。
代表的なモジュールのひとつがstyled-componentsで、これは、テンプレートリテラル内に記述されたCSSから、
JSXコンポーネントと、そのコンポーネント専用のユニークなクラスを動的に生成する仕組みになっている。

styled-componentsで、先程のmedia objectを書き直すと以下のようになる。

.. raw:: html
    
    <iframe width="100%" height="400px" src="https://stackblitz.com/edit/media-object-styled-components?embed=1&file=src%2FMedia.tsx&view=editor"></iframe>

`Media object - styled-components <https://stackblitz.com/edit/media-object-styled-components?file=src%2FMedia.tsx>`_

CSS in JSの優れた点は、機械的にユニークなクラス名を生成するので、スタイルの衝突がけっして起きないことだ。
[ref]ただし、styled-componentsの記述内に自動生成でないふつうのクラスを入れ子にすることも許可しているので、この場合は衝突が発生し得る[/ref]
これはふつうに使っているだけでスタイルを曖昧さなく当てられるので、非常に大きな進歩だ。
もはやめんどうな方法論の規則を覚える必要はない。ただAPIの使いかたを知ればいいだけなので、だれでも無理なく使える。

ただし、styled-componentsのAPI設計には、一点だけどうしても気に食わない点がある。
ぼくは、styled-componentsもいくつかのプロジェクトで使ってきたけど、使えば使うほど不便と感じるようになってきた。
上記のサンプルコードを見ればわかるように、styled-componentsでは、スタイルを記述するために、
必ずひとつReactコンポーネントを作らなければならない。結果として、ほんとうに作りたいコンポーネントのまとまりひとつ(この場合
Mediaコンポーネント)に対して、いくつもの小さなコンポーネントを不必要に作らなければならないのだ。
もちろん、それぞれに対して命名するという作業も必要になる。これが相当わずらわしい。
ただスタイルを持つだけで、とくだん機能も論理的な意味もない無数の小さなコンポーネントが定義されているのはノイズだし、
スタイルとDOM構造が離れた場所に定義されているのも、どのような表示結果になるのかを一見して把握しづらくしている。

ここ最近、Metaが内製のCSS in JSライブラリであるstylexを公開したことで、ゼロランタイムと言われるCSS in JSの別の一派が注目されているようだ。
これは、ビルド時にスタイル定義を解決することで、ランタイム処理を最小限にすることを狙っている。
また、Atomic CSSなので、CSSファイルのサイズも非常に小さくなる。
[ref]Atomic CSSは、ひとつのクラスに対して複数のルールを記述する旧来の方法よりファイルが小さくなることが `知られている。 <https://sebastienlorber.com/atomic-css-in-js>`_ [/ref]
stylexでは、1コンポーネント1スタイルという一対一関係こそ強制されないものの、ドキュメントで `述べられている通り、 <https://stylexjs.com/docs/learn/thinking-in-stylex/#readability--maintainability-over-terseness>`_ 
本質的にDOMとスタイルを切り離して、スタイルの塊に何らかの意味のある名前をつけるのを良しとしているという点で、
styled-componentsと本質的には変わらないと思う。これでは、ぼくがstyled-componentsに対して持っている不満点は解消されない。

Tailwind CSS - Utility-first CSS
===================================

CSSにおけるユーティリティークラスとは、単一の機能に特化したクラスのことで、そのほとんどは、プロパティーをひとつだけ持つ。
たとえば、さきほど紹介したSUIT CSSにも `ユーティリティークラス郡 <https://github.com/suitcss/suit/blob/master/packages/utils-flex/lib/flex.css>`_ が含まれている。以下はその一例。

.. code-block:: css

    .u-flex {
        display: flex !important;
    }

    .u-flexInline {
        display: inline-flex !important;
    }

    .u-flexRow {
        flex-direction: row !important;
    }

    .u-flexRowReverse {
        flex-direction: row-reverse !important;
    }



これらは、コンポーネントで表現し切れない部分、あるいはすべてをコンポーネント化して表現しようとすると無理が出てくる細かい部分を
補う目的で用意されている。
あるものの再利用性というものは、その責務が小さければ小さいほど高まる。ユーティリティークラスは、
単一責任に特化しているがゆえに、再利用性が最大化されているクラスだと言える。

これを推し進めて、ユーティリティークラスのみでスタイルを記述するという考えかたに発展させたのが、Utility-first CSSであり、
Utility-first CSSをサポートするCSSライブラリの中でも、現在最も支持を得ているのがTailwind CSSだ。
Tailwind CSSで、media objectを実装すると以下のようになる。


.. raw:: html
    
    <iframe width="100%" height="400px" src="https://stackblitz.com/edit/media-object-tailwind?embed=1&file=src%2FMedia.tsx&view=editor"></iframe>

`Media object - Tailwind CSS <https://stackblitz.com/edit/media-object-tailwind?file=src%2FMedia.tsx>`_

このファイルには、もはやわれわれがほんとうに作りたいMediaコンポーネント以外の、不要なものはなにもない。
内部にある各要素をどのようなコンセプトでくくって、どのような名前をつければいいかなどと考えなくていい。
欲しい見た目と機能を実装するために必要なこと、コンポーネント実装の本質に最短で取りかかって集中できる。
これこそ、まさにぼくがUtility-firstが合理的であると考える理由だ。

また、上記のflexユーティリティーの例を見ればわかるように、ユーティリティークラスの大半は、Atomicでもある。
したがって、CSSのサイズは自然とコンパクトになる。Tailwindなら、高速にコーディングできるし、高速にページがロードされる。
ランタイム時のオーバーヘッドももちろんゼロだ。

サイズに関して言うと、Tailwindは、アプリのコードをスキャンして、参照されているクラスのみを出力するという仕組みになっている。
この仕組みのシンプルさもまた、すばらしくクールで気に入っている点だ。バンドラーのような複雑な仕組みはまったく必要ない。
Reactなど特定のライブラリと結びついているわけではないので、やりたければRailsのサーバーサイドテンプレートと組み合わせて使うことだってできる。

もうひとつ注目してもらいたいのが、SUIT CSSの例では、 :code:`Media-button`, :code:`Media-date`, :code:`Media-separator` に個別に色を指定していたのに対して、
Tailwindの例では、親要素で一度色を指定して、子要素はそれを継承するだけで済んでいる点だ(styled-componentsの例も本質的に同じ)。
もちろん、SUIT CSSの例でも、親要素にクラスを付与して共通の色指定をすることは可能だ。
しかし、この例では、右側を複数の行(Meida-row)でまとめるという考え方で記述していた。1行目と2行目は色が違うので、Media-rowに直接
色を指定することはできない。では、Media-rowのモディファイアーを作るか。それともMedia-1stRow, Media-2ndRowというまとめかたをするか。
名付けが必要であるがゆえに、このように本質的でない悩みがいちいち発生する。
Tailwindなら、日付とボタンが同じ色だから、その親要素に色を指定するというシンプルな判断ができて、迷う余地はない。
なんと快適なことだろう。

Tailwindには、他にも特筆すべき点がある。それは、色やサイズなどすべてにおいて、指定できる値が限定されているということだ。
この使用可能な値の集合は、設定ファイルで指定できる。これは、実質的に、Tailwindを使えば自動的にデザイントークンが導入されて、
一貫したトーン&マナーのUIになるということだ。もちろん、他のどの方法でもデザイントークンに基いた実装をすることはできるけど、
Tailwindなら、なにも考えなくても強制的にそうなる。

以上見てきたように、Tailwindは独自のクラス名体系があって学習曲線が多少高かったり、デザイントークンが勝手に導入されるなど、
SUIT CSSやstyled-componentなどと比べて、かなり主張の強めな選択肢であることは否めないかもしれない。
また、Tailwindでは、カスケーディングによるクラス名衝突の問題は、実はあまり解決されていない。
クラス名にプレフィックスを付与する設定はあるので、ある程度緩和はできるけど、CSS in JSのように衝突を避けるメカニズムがあるわけではないからだ。
だから、既存プロジェクトに段階的に導入するなど、実際にクラス名の衝突が危惧される状況では注意が必要だ。
しかし、最初からTailwindですべて記述すると決めて始めたプロジェクトであれば、衝突の心配はないだろう。

ともかく、一度ハマってしまえば、そのシンプルさから来る開発体験の快適さは、クセになること請け合いだ。

なぜインラインスタイルではダメなのか
-----------------------------------------

もしかすると、Tailwindでスタイルを記述するくらいなら、style属性にスタイルを直接記述すればいいと思われるかもしれない。
しかし、style属性には、機能的な制限がある。メディアクエリーや、疑似クラス、アニメーションといったことが記述できないのだ。
最近は、style属性を拡張して疑似クラスなどを記述できるようにする `CSS Hooks <https://css-hooks.com/>`_ のようなライブラリも
あるようだけど、それでも拡張できる範囲は限られている。
もし今後、style属性からCSSの全機能にアクセスできる技術が出てくれば、そのときはstyle属性で済ませてもいいのかもしれない。

まとめ
===========

* CSSを記述するための手法は、カスケーディングというCSSの難点を克服しつつ、UIコンポーネントを開発するために進化してきた。
* Tailwind CSSを使えば、子要素への名付けなど余計なことに煩わされずに、コンポーネント実装に集中できる。
* Tailwindおすすめ。

タイムライン
=============

+-----------------------+----------------------------------------------------------------------------------------+
| 1996/12/17            | `CSS 1 <https://www.w3.org/TR/2008/REC-CSS1-20080411/>`_                               |
+-----------------------+----------------------------------------------------------------------------------------+
| 1998/5/12             | `CSS 2 <https://www.w3.org/TR/2008/REC-CSS2-20080411/>`_                               |
+-----------------------+----------------------------------------------------------------------------------------+
| 2009/5/20             | `less 0.7.0 <https://rubygems.org/gems/less/versions/0.7.0>`_                          |
+-----------------------+----------------------------------------------------------------------------------------+
| 2010/9/22             | `sass 3.1.0.alpha.2 <https://rubygems.org/gems/sass/versions/3.1.0.alpha.2>`_          |
+-----------------------+----------------------------------------------------------------------------------------+
| 2013/7/18             | `Bootstrap 1.0.0 <https://github.com/twbs/bootstrap/releases/tag/v1.0.0>`_             |
+-----------------------+----------------------------------------------------------------------------------------+
| 2013/7/3              | `React 0.3.0 <https://github.com/facebook/react/releases/tag/v0.3.0>`_                 |
+-----------------------+----------------------------------------------------------------------------------------+
| 2013/10/16            | `BEM CORE 1.0.0 <https://github.com/bem/bem-core/releases/tag/v1.0.0>`_                |
+-----------------------+----------------------------------------------------------------------------------------+
| 2014/3/23             | `SUIT CSS 0.3.0 <https://www.npmjs.com/package/suitcss/v/0.3.0>`_                      |
+-----------------------+----------------------------------------------------------------------------------------+
| 2014/10/30            | `jss 0.2.0 <https://www.npmjs.com/package/jss/v/0.2.0>`_                               |
+-----------------------+----------------------------------------------------------------------------------------+
| 2015/2/12             | `atomizer 0.2.0 <https://www.npmjs.com/package/atomizer/v/0.2.0>`_                     |
+-----------------------+----------------------------------------------------------------------------------------+
| 2015/3/7              | `tachyons CSS 1.1.0 <https://www.npmjs.com/package/tachyons/v/1.1.0>`_                 |
+-----------------------+----------------------------------------------------------------------------------------+
| 2016/10/13            | `styled-components 1.0.0 <https://www.npmjs.com/package/styled-components/v/1.0.0>`_   |
+-----------------------+----------------------------------------------------------------------------------------+
| 2017/11/2             | `tailwindcss 0.1.0 <https://github.com/tailwindlabs/tailwindcss/releases/tag/v0.1.0>`_ |
+-----------------------+----------------------------------------------------------------------------------------+


参考リンク
===========

* `‘Why BEM?’ in a nutshell <https://blog.decaf.de/2015/06/24/why-bem-in-a-nutshell/>`_ なぜBEMを使うべきか。詳細度の問題についての解説。
* `MindBEMding – getting your head ’round BEM syntax <https://csswizardry.com/2013/01/mindbemding-getting-your-head-round-bem-syntax/>`_ なぜBEMを使うべきか。BEMの可読性についての解説。
* `About HTML semantics and front-end architecture <https://nicolasgallagher.com/about-html-semantics-front-end-architecture/>`_ SUIT CSS作者Nicolas Gallagherによる、フロンエンド開発におけるクラスの役割についての考察。クラス名は、コンテンツにもとづいて命名されるべきではなく、デザインのパターンに基いた名前を持つべき。
* `Challenging CSS Best Practices <https://www.smashingmagazine.com/2013/10/challenging-css-best-practices-atomic-approach/>`_ Yahoo!で使われているAtomic CSSのメリットについて述べている。従来的なセマンティックなクラス命名との比較。
* `Frequently Asked Questions | Atomizer <https://acss.io/frequently-asked-questions.html>`_ Atomic CSSのFAQ。それが解決する問題について。詳細度の問題が起きない、サイズが小さくなるなど。多くは、Utility-first CSSにも当てはまる。
* `CSS Utility Classes and "Separation of Concerns" <https://adamwathan.me/css-utility-classes-and-separation-of-concerns/>`_ BEMのようなCSS方法論でコンポーネントを記述することの不安定さを解いている。再利用性を付きつめていくと、意味に基いて命名されたクラスの多くはいつのまにかなくなってしまう。Tailwindの思想的な背景を説明している。
* `Building the New Facebook with React and Relay | Frank Yan <https://www.youtube.com/watch?v=9JZHodNR184>`_ StylexによるAtomic CSS化でfacebookが達成したCSSの軽量化について触れている。413KBから74KBに。
* `Cascade, specificity, and inheritance <https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_and_inheritance>`_ カスケーディング、詳細度、継承がどのように組み合わさって、実際の見た目を形成するかを具体例に基いて解説している。(あなたが読んでいる)この記事で解説している方法を使えば、これらのうちカスケーディングと詳細度はほとんど意識しなくてよくなる。
* `Introducing the CSS Cascade <https://developer.mozilla.org/en-US/docs/Web/CSS/Cascade>`_ カスケーディングの詳細な説明。
* `Used and Abused – CSS Inheritance and Our Misuse of the Cascade <https://www.phase2technology.com/blog/used-and-abused-css>`_ カスケーディングがもたらす具体的な害の解説。複数の詳細度がまぜこぜになると、あるルールをいじったときに、どこでなにが起きるか予測できなくなる。
* `HTML Standard <https://html.spec.whatwg.org/multipage/dom.html#classes>`_ HTML標準では、クラス名で見た目ではなくコンテンツの性質を記述することが奨励されている。
* `The media object saves hundreds of lines of code <https://www.stubbornella.org/2010/06/25/the-media-object-saves-hundreds-of-lines-of-code/>`_ media object 具体的なコンテンツの意味に言及しないクラス設計の有効性を示した有名な例
* `CSS Zen Garden: The Beauty of CSS Design <https://csszengarden.com/>`_ HTML構造とCSSクラスを固定したまま、スタイルシートの変更だけでさまざまなデザインをする試み。コンテンツにもとづいた意味を持つクラス名の興味深い活用例。CSS in JSやUtility-first CSSでは、こういうことはできない。
