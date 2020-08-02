(L)GPLとApp StoreとVLC for iOS
###############################

:date: 2014-06-29
:slug: lgpl_and_appstore
:tags: apple, ios, gpl, lgpl, license, fsf, vlc, oss
:summary: 主に仕事で、ffmpegやVLCのような(L)GPLのもとに配布されているプログラムを利用することが、ちょくちょくあるのですが、GPLプログラムはApp Storeで配布できないという話をツイッターでみかけたのをきっかけに、そのあたりどうなっているのか調べてみました。

.. image:: {static}/images/lgpl.png
   :align: center
   :alt: LGPL logo

.. contents:: 目次

主に仕事で、ffmpegやVLCのような(L)GPLのもとに配布されているプログラムを利用することが、
ちょくちょくあるのですが、GPLプログラムはApp Storeで配布できないという話をツイッターで
みかけたのをきっかけに、そのあたりどうなっているのか調べてみました。

以下の話の大前提として、(L)GPLは、著作権に基くライセンスであることに注意する必要があります。
つまり、ライセンスに違反するような形での頒布を行ったとしても、
著作権者がその行為を容認するならば、問題とはならない可能性があるということです。
また、当然ながら、わたしは法律の専門家ではありませんし、そうであろうとなかろうと、
法的なリスクを伴う判断は法律家に相談した上で行ってください。

ことの発端、GNU GoがApp Storeから消えた
=======================================

2010年5月、FSFは、GPLv2の元に配布されている `GNU Go <http://www.gnu.org/software/gnugo/gnugo.html>`_ という囲碁ソフトをiPhone向けに
移植したプログラムがApp Storeを通じて頒布されている状況は、ライセンス違反であるという `声明を出しました <http://www.fsf.org/news/2010-05-app-store-compliance>`_ 。
[ref]iPhone版の作者自身もGPLに違反していたようですが、FSFの記事はAppleにフォーカスを当てており、作者自身によるGPL違反の詳細については触れられていません。[/ref]
その主張によれば、 iTunes Storeのサービス規約には、GPLv2 第6節に違反するような内容が含まれています。
[ref]iTunes Storeサービス規約は、2010年当時から現在にかけて、幾度となく改訂を繰り返しており、その中には、
「オープンソースコンポーネントの使用に関する使用許諾条件」について言及している文が追加されていたり、
5個のデバイスまでしかアプリをインストールできないという部分が削除されるなど、興味深い部分も含まれて
いますが、制限があるという基本的な状況は現在でも同じものと思われます。[/ref]
FSFは、App Storeのサービス規約修正を要求したようですが、Appleはそれに答えるかわりに、GNU Goをストアから削除しました。

`FSFがとくに問題にしている <http://www.fsf.org/blogs/licensing/more-about-the-app-store-gpl-enforcement>`_ 第6節は、次の通りです。

  6. Each time you redistribute the Program (or any work based on the Program), the recipient automatically receives a license from the original licensor to copy, distribute or modify the Program subject to these terms and conditions. You may not impose any further restrictions on the recipients' exercise of the rights granted herein. You are not responsible for enforcing compliance by third parties to this License.

  6. あなたが『プログラム』(または『プログラム』を基にした著作物全般)を再頒 布するたびに、その受領者は元々のライセンス許可者から、この契約書で指定 された条件と制約の下で『プログラム』を複製や頒布、あるいは改変する許可 を自動的に得るものとする。あなたは、受領者がここで認められた権利を行使 することに関してこれ以上他のいかなる制限も課してはならない。あなたには、 第三者がこの契約書に従うことを強制する責任はない。

いまの文脈では、「あなた」をApple、「受領者」をApple Storeのユーザーと読み替えて解釈すればいいでしょう。

一方、iTunes Storeのサービス規約には以下のような文が含まれています。

  (i) Your use of the Products is conditioned upon your prior acceptance of the terms of this Agreement.
  (ii) You shall be authorized to use the Products only for personal, noncommercial use.
  (iii) You shall be authorized to use the Products on five Apple-authorized devices at any time, except in the case of Movie Rentals, as described below.

  (当時のサービス規約の日本語版が入手できなかったので英文のみ)

このように、アプリを使うにあたって、iTunesのサービス規約に同意しなければならないことや、個人使用に限ること、5個のデバイスまででしか使用を許可されないという、GPLで規定された以上の制限を加えています。さらに、Apple Storeでは、サードパーティーとユーザーが個別のEULAを結ぶことも許していますが、これらの条件は、サードパーティーとユーザー間の契約に追加される形で作用することも明記されていました。
[ref]このあたりも現在の規約では微妙に変わってたりしますが、Appleの利用ルールがユーザーに強制されることは変わっていないと思われます。[/ref]
したがって、App Storeを通じてGPLプログラムをユーザーに配布することは、GPLに違反しているということになるわけです。

たとえば一例として、元々GPLプログラムは、個人利用だろうが商用だろうが、関係なく頒布することができるわけですが、
上記のuseという言葉に頒布という意味が含まれていると解釈すると、App Storeを通じて頒布された時点で、
個人利用での頒布しかできなくなってしまう、といったことが問題になってくるのだと思います。
(アーキテクチャ的にデバイス間での自由なアプリのコピーが可能だったとして)。

ただ、個人的には、GPLが、複製、頒布、改変についてのみ規定しているのに対して、Appleの規約には、頒布、配布といった
言葉は、ライセンスアプリケーション・エンドユーザ使用許諾契約[ref]これは、現在の規約では、サードパーティーライセンスで置き換え可能[/ref]を除いて出てこず、利用ルール(Usage rules)の利用(Usage)という言葉に頒布・配布といった意味が含まれないとすると、お互いに衝突する部分はないという解釈もありえるのではないか、という印象を持ちました。

vlc-develでの問題提起、App Storeからの削除
==========================================

GNU Goの一件から5ヶ月後の2010年10月、VLCの開発者メーリングリストで、主要開発者
`Rémi Denis-Courmon <https://mailman.videolan.org/pipermail/vlc-devel/2010-October/076868.html>`_
[ref]実際には、この投稿より前から、開発者間での議論があり、その過程でどうもいざこざがあったらしく、Denis-CourmonのRSS feedがVideoLanのサイトからはずされるという出来事がありました。もはや当事者間で話しあってもどうにもならないと思ったのか、メーリングリストに自分の主張を展開するという手に出たようです。[/ref]
の問題提起に端を発する議論が行われていました。

`VLC <http://www.videolan.org/vlc/index.html>`_ は、Linux,Windows,Mac等各種プラットフォームで使うことのできる、動画プレイヤーです。
VLCの開発プロジェクトは、VideoLanというNPOによって運営されており、デスクトップ版は、GNU GPLライセンスの元に配布されています。
また、このプロジェクトの特徴として、開発者が著作権をVideoLANに移譲するということはせず、各自がそのまま保持し続ける形で運営されていることが挙げられます(これと対照的に、GNUのリリースしているソフトウェアでは、著作権はFSFに移譲されます)。

さて、このVLCのiOS版が、2010年の9月にリリースされました。リリースしたのは、VideoLANとは無関係なApplidiumという会社ですが、開発に際してはVLCコミュニティの協力もあったようで、VLC開発者たちからは認知されていたようです。GNU Goの件があった後でしたので、iOS版に協力していた、べつの主要開発者であるJean-Baptiste Kempfにも、iOS版がグレーゾーンであるという認識はあったようです。

iOS版のリリース後、Denis-Courmontは、VLCの著作権者の一人としての権限を行使して、Applidiumによる著作権侵害をAppleに訴えました。
この裏には,自由ソフトウェア主義的な思想を持っているDenis-Courmontと、自由ソフトウェア的な考えかたにあまり拘らない他の開発者の対立という構図があったようです。彼のこの行動は、 `FSFからも支持されました <http://www.fsf.org/blogs/licensing/vlc-enforcement>`_ 。
ほどなくして、VLC for iOSは、いったん `App Storeから姿を消しました <http://applidium.com/en/news/apple_pulled_vlc_off_the_appstore/>`_ 。

LGPLへのリライセンス、App Storeへの復活
=======================================

その後、どういう議論があってそうなったのかは不明ですが、Kempの主導で、エンジン部分であるlibVLCを含む主要なコードのライセンスをLGPLに変更するという方向に動きはじめました。
GNUプロジェクトのようにひとつの組織に著作権が移譲されているのであれば、プロジェクトのライセンスを変更するのは、やろうと思えば可能かもしれません。しかし、VLCの著作権は、100人を越える開発者に分散されているので、一筋縄ではいきません。すべての著作権者からライセンス変更の許諾を得る必要があるからです。その難行を `Kempはやりとげました <http://lwn.net/Articles/525718/>`_ 。リライセンスに `反対の立場 <https://mailman.videolan.org/pipermail/vlc-devel/2011-January/078156.html>`_ だったDenis-Courmontも、最終的には認める方向で落ち着いたようです。リライセンスが完了すると、いま現在でもApp Storeに見られるように、見事VLC for iOSは、App Storeへの復活を果たしました。

しかしながら、LGPLv2.1の文面とAppleの規約を見比べてみても、果たしてLGPLになったことによって、元々の問題が解消されたのかどうか、あまりはっきりしません。実際、VideoLAN自身、これによってApp Storeで利用可能になるのか `不明である <http://www.videolan.org/press/lgpl-modules.html>`_ と言っていますし、AGPL著者であるBradley M. Kuhnなどは、LGPLであっても `Apple規約との非互換性は残っている <http://ebb.org/bkuhn/blog/2012/11/22/vlc-lgpl.html>`_ と述べています。私見では、LGPLになったことによって問題が解消されてApp Storeに復帰できたというよりは、開発者間でのコンセンサスが取れて、だれもApplidiumに対して著作権を行使する人間がいなくなったので、表面上問題が解消されたように見えているというのが、ほんとうのところに近いのではないかと思っています。冒頭に述べたように、著作権者が問題にしなければ、(L)GPLに違反していようがしていまいが、関係ないのです。

その他の疑問
=============

iOSアプリでLGPLライセンスのライブラリを使用した場合、アプリのライセンスもLGPLになる?
-------------------------------------------------------------------------------------

iOSアプリにはダイナミックリンクの仕組みがなく、静的リンクするしかないので、リンクしたアプリ本体もLGPLで
配布しなければならないのではないかという疑問です。今回ちゃんと調べるまで知らなかったのですが、静的リンクでも、
再リンクが可能なようにオブジェクトファイル一式を配布すれば、問題ありません。

Sparrow for iOSはLGPLに違反していないのか
-----------------------------------------

前述のテクニックを使用して、App Storeで、LGPLライブラリを使用しつつ、アプリ自体はクローズドソースのまま配布しているのが、
`Sparrow <http://www.sparrowmailapp.com/lgpl.php>`_ です。
ただし、前述の議論から、LGPLであってもAppleの規約と互換性があるのかは不明ですので、違反しているのか、していないのか、
わたしにはわかりません。この手法については、AppleのDeveloper Programに入会して、
年会費を払わないと実機でアプリを実行できない点が問題になるのではないかという指摘もあります。

LGPLライブラリを使用しているプログラムは、リバースエンジニアリングを許可しなければならないのでは?
-------------------------------------------------------------------------------------------------

Appleの規約で、製品のリバースエンジニアリングを禁止しているならば、LGPLと競合するのではないかという疑問です。
VLCの問題が出てしばらくした後のライセンス更新で、

  お客様は、ライセンスアプリケーション、そのアップグレード、またはそれらの一部について、複製 （本使用許諾および本利用ルールで明示的に認められている場合を除きます）、逆コンパイル、リバースエンジニアリング、逆アセンブル、ソースコードの解明 の試み、改変、または二次的著作物の創作を行うことはできません（但し、上記の制約が、適用法令により禁止される場合、または、**ライセンスアプリケーショ ンに含まれるオープンソースコンポーネントの使用に関する使用許諾条件により許容される場合にはこの限りではありません**）。

の強調部分が追加されたりしているので、すくなくともこの部分については問題にならないのではないかと思います。

VLCはffmpegを使用しているのではないのか
-----------------------------------------

VLCは、一部GPLライセンスで配布されているffmpegから派生したコードも使用しているのですが、
よくプロジェクト外部の広範囲の人にまで許可を取ることができたなあという部分が、個人的には気になってます。
VLCの開発者コミュニティとffmpegの開発者コミュニティって仲良しだったりするんでしょうかね。
VLC for iOSに含まれる x264.cとかみると、先頭部分のライセンス表記はGPLのままだったりするんすが、
これは単なる修正漏れですかね(x264自体はVideoLANの管理課にあるプロジェクトのようなので、問題ないと思いますが)。

結論
====

で、けっきょくのところ、(L)GPLのコードは、iOSで使えるのか、使えないのかというところですが、
LGPLについては、SparrowというLGPLライブラリを使用しながら、クローズドのまま公開され続けている実例があります。
また、すくなくともVLCKitについては、VideoLANとしてApple Storeで頒布しても問題ないという立場でリリースしている
もののはずなので、互換性がないと言って文句を言ってきたりはしないんじゃないでしょうか
(とはいえ、著作権がVideoLANにないのは、前述の通りです)。

しかしながら、いまのところはっきりとした結論が出ているとは言えない状況なので、著作権者に
文句を言われた場合には、アプリを取り下げざるを得なくなるかもしれません。

リンク
======

ライセンス関連
--------------

GNU General Public License, version 2
  http://www.gnu.org/licenses/gpl-2.0.html
GNU 一般公衆利用許諾契約書
  http://www.opensource.jp/gpl/gpl.ja.html
GNU Lesser General Public License, version 2.1
  https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
GNU 劣等一般公衆利許諾契約書
  http://www.opensource.gr.jp/lesser/lgpl.ja.html
iTUNES STORE - TERMS AND CONDITIONS
  http://www.apple.com/legal/internet-services/itunes/us/terms.html
iTUNES STORE - サービス規約
  http://www.apple.com/legal/internet-services/itunes/jp/terms.html

参考記事(時系列)
----------------

Which open source licenses are compatible with the Apple's iPhone and its official App Store ? [closed] (2009/01/20)
  http://stackoverflow.com/questions/459833/which-open-source-licenses-are-compatible-with-the-apples-iphone-and-its-offici
Compatibility between the iPhone App Store and the LGPL (2009/08/24)
  http://multinc.com/2009/08/24/compatibility-between-the-iphone-app-store-and-the-lgpl/
GPL Enforcement in Apple's App Store (2010/05/25)
  http://www.fsf.org/news/2010-05-app-store-compliance
More about the App Store GPL Enforcement (2010/05/26)
  http://www.fsf.org/blogs/licensing/more-about-the-app-store-gpl-enforcement
[vlc-devel] Apple AppStore infringing VLC media player license (2010/10/26)
  https://mailman.videolan.org/pipermail/vlc-devel/2010-October/076868.html
VLC developer takes a stand against DRM enforcement in Apple's App Store (2010/10/29)
  http://www.fsf.org/blogs/licensing/vlc-enforcement
The VLC-iOS license dispute and how it could spread to Android (2010/11/02)
  http://arstechnica.com/apple/2010/11/the-vlc-ios-license-dispute-and-how-it-could-spread-to-android/
[vlc-devel] FSF position on GPLv2 & current App Store terms (2010/11/02)
  https://mailman.videolan.org/pipermail/vlc-devel/2010-November/077027.html
VLC for iOS likely be pulled from App Store because of incompatibility with source code GPL (2010/11/02)
  http://www.geek.com/apple/vlc-for-ios-likely-be-pulled-from-app-store-because-of-incompatibility-with-source-code-gpl-1292666/
Apple pulled VLC off the AppStore (2011のどこか)
  http://applidium.com/en/news/apple_pulled_vlc_off_the_appstore/
No GPL Apps for Apple's App Store (2011/01/08)
  http://www.zdnet.com/blog/open-source/no-gpl-apps-for-apples-app-store/8046
[vlc-devel] update on AppStore situation please (2011/01/10)
  https://mailman.videolan.org/pipermail/vlc-devel/2011-January/078046.html
The GPL, the App Store, and you (2011/09/01)
  http://www.tuaw.com/2011/01/09/the-gpl-the-app-store-and-you/
Changing the VLC engine license to LGPL (2011/09/07)
  http://www.videolan.org/press/lgpl.html
[vlc-devel] LGPL and VLC (2011/10/04)
  https://mailman.videolan.org/pipermail/vlc-devel/2011-October/081869.html
Why (not) to relicense VLC under LGPL? (2012のどこか)
  http://www.remlab.net/op/vlc-lgpl.shtml
Apple don't allow any GPL software on iOS. (2012/01/21)
  https://news.ycombinator.com/item?id=3488833
VLC playback modules relicensed to LGPL (2012/11/20)
  http://www.videolan.org/press/lgpl-modules.html
Relicensing VLC from GPL to LGPL (2012/11/21)
  http://lwn.net/Articles/525718/
LGPL is not compatible with IOS (2012/04/18)
  https://trac.ffmpeg.org/ticket/1229
How to properly(?) relicense a large open source project - part 1 (2012/11/07)
  http://www.jbkempf.com/blog/post/2012/How-to-properly-relicense-a-large-open-source-project
VLC re-licensed as LGPL, ready to head back to the App Store (2012/11/15)
  http://www.geek.com/apple/vlc-re-licensed-as-lgpl-ready-to-head-back-to-the-app-store-1528626/
Left Wondering Why VideoLan Relicensed Some Code to LGPL (2012/11/22)
  http://ebb.org/bkuhn/blog/2012/11/22/vlc-lgpl.html
The Problem with Using LGPL v2.1 Code in an iOS App (2013/07/23)
  http://roadfiresoftware.com/2013/08/the-problem-with-using-lgpl-v2-1-code-in-an-ios-app/

