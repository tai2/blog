Proton Mail 〜 おれが本物のプライバシーファーストなウェブメールを見せてやりますよ 〜
######################################################################################

:date: 2022-11-13
:slug: proton-mail
:summary: この記事では、Proton Mailの特徴や、技術的に興味深い点を紹介する。

はじめに
===========

    If you’re not paying for the product, you are the product itself.
    (製品にお金を払っていないということは、あなたが製品そのものということだ)

これまで、しっくりくるメール受信環境がなかなかみつからず、いろいろな変遷をたどってきた。

Gmailを長らく愛用していた時期もあったけど、あるとき、ふと開眼し、広告モデルのウェブメールをやめたいと思うようになった。
そこからは苦難の道だった。Mac標準のメールアプリは検索がときどきバグったり、フィルターがいまいちだったりした。
`OSSを使って快適なCLIメール環境の構築を試みもした <https://blog.tai2.net/mutt-and-notmuch.html>`_ けど、ときどきバグってメンテが大変だったりした。

けっきょくのところ、いまどきローカルにメールボックスを持つのは特定のマシンに縛られて不便だし、自前で環境が壊れないようにメンテするのもしんどい。
かといって、Gmailに戻るのも嫌だ。それなら、有料でウェブメールを提供しているサービスを探せばいいのではないかと思い立った。

探してみるといくつかの選択肢があったけど、 `Proton Mail <https://proton.me/mail>`_ というサービスが良さそうだったので使いはじめた。[ref]当時調べた中でmbox形式のインポートをサポートしていた唯一のメールサービスだったのも大きい[/ref]かれこれもう4年ほど経つ。

この記事では、Proton Mailの特徴や、技術的に興味深い点を紹介する。

.. contents:: 目次

Proton Mailとは
====================

Proton Mailは、プライバシーを主眼に置いて設計されたウェブメールサービスで、ウェブアプリ、iOS、Androidネイティブアプリが提供されている。

Proton Mailは有料の月額課金モデルで運営されている。[ref]無料で利用することも可能。無料ユーザーのコストは、有料ユーザーが支えている[/ref]だから、Gmailのように広告を見せられることはない。また、ユーザーのメールに含まれる情報を売って商売しているわけでもない。

このサービスのすごいところは、プライバシー保護をとことん突き詰めていることだ。
どこまで突き詰めているかというと、暗号化技術により、Proton Mail自身でさえもサーバーに保存されたメールが読めないようになっている。
だから、たとえデータ漏洩があっても第三者はメールの中身を読めないことが暗号技術によって保証されている。暗号を解除するための鍵はユーザー自身しか知らない。

Proton Mailの暗号化は、 `OpenPGP <https://www.openpgp.org/>`_ ベースのエンドツーエンド暗号化(E2EE)と、ゼロアクセス暗号化に分けられる。
暗号化を前提とした上で、どのようにスパムフィルタやメール検索を実装するのかというあたりも公式ブログで説明されていておもしろいので、順番に説明していく。

Proton Mailの特徴
--------------------

Proton Mail自身は、先進的なセキュリティー上の特徴として、 `以下を挙げている: <https://proton.me/blog/is-gmail-secure>`_


* あなただけが、あなたのメールを読めます: エンドツーエンド暗号化は、TLSよりさらに一歩踏み込みます。Protonでさえメールを読めません。
* データ漏洩に強いセキュリティー: ゼロアクセス暗号化とは、あなたのアカウントの全メールが暗号化されるということです。Proton以外のユーザーから受信したメールでさえも。
* すべての相手にエンドツーエンド暗号化を: パスワード保護されたメールをどんなメールアカウントにも無料で送信できます。
* 追跡しないし、ログも取りません: Googleが、フリーアカウント上のすべての行動を追跡する一方、Proton Mailはなにも記録しません。
* スイスのプライバシー: 米国を拠点とするGoogleと違い、Proton Mailはスイスのプライバシー法に統治されます。スイスのプライバシーは、世界でも最高レベルに厳格です。

公開鍵暗号おさらい
====================

Proton Mail自体の話に入る前に、Proton Mailのプライバシーの基礎になっている暗号システムの概要について、ざっと説明する。

共通鍵暗号とは、暗号化と復号に同じ鍵(パスフレーズなど)を使う暗号方式だ。

.. figure:: {static}/images/proton-mail/symmetric-key-encryption.png
   :alt: 共通鍵暗号は、同じ鍵で暗号化も復号もできる

   共通鍵暗号は、同じ鍵で暗号化も復号もできる

..
  stateDiagram-v2
      暗号化されたデータ --> 平文のデータ: 共通鍵で復号
      平文のデータ --> 暗号化されたデータ: 共通鍵で暗号化

共通鍵暗号だけでメッセージをやりとりしようと思うと、自分と相手双方が何らかの方法で共通鍵を事前に共有していなければならない。
メールのように不特定多数の相手とやりとりする場合、これは現実的ではない。

公開鍵暗号を使えばこの欠点を克服できる。公開鍵暗号システムでは、秘密鍵と公開鍵という2つ組の鍵が使われる。
公開鍵は、メッセージを暗号化する際に使われ、暗号化されたメッセージは、対応する秘密鍵を持っていないと復号できない。
公開鍵は、その名の通り公にしても問題ないものなので、通信する二者が互いに公開鍵を交換しあえば、簡単かつ安全に通信できる。(メールアドレス自体と違って、名刺などに気軽に掲載して手入力できるような長さの文字列ではないので、最初にどう配布するかという問題はあると思う)

また、PGPでは、秘密鍵を使ってメッセージに電子署名をすることができる。これにより、受信者はメッセージがたしかに秘密鍵の所有者によって作成されたものであること(真性性)、またそのメッセージが改竄されていないこと(完全性)を、公開鍵を使って検証できる。

ちなみに、公開鍵暗号システムと言っても、メッセージそれ自体の暗号化は共通鍵暗号を使って行われ、暗号化に使われる共通鍵の交換だけが公開鍵暗号を使って行われる。

.. figure:: {static}/images/proton-mail/public-key-encryption.png
   :alt: 公開鍵暗号は、暗号と復号に異なる鍵を使う

   公開鍵暗号は、暗号と復号に異なる鍵を使う

..
  stateDiagram-v2
      暗号化された共通鍵 --> 平文の共通鍵: 秘密鍵で復号
      平文の共通鍵 --> 暗号化された共通鍵: 公開鍵で暗号化

近年、公開鍵暗号システムの実装で標準的に使われるようになった楕円曲線暗号(ECC)という公開鍵暗号方式[ref]Proton Mailでも現在はこれがデフォルト[/ref]では、メッセージの署名はできるが、暗号化機能自体ない。DH(Diffie-Hellman)鍵交換というアルゴリズムを使えば、機密性を担保できるが能動的攻撃による改竄の恐れがある。そこで、DH鍵交換と楕円曲線暗号を組み合わせることで、機密性と完全性を両方担保するという構成になっている(と、ぼくは理解している)。ECCでは、昔から使われてきたRSAよりもすくない計算資源で、効率良く暗号化を実現できる。

Proton Mailユーザー同士のメール交換 — エンドツーエンド暗号化
=============================================================

Proton Mailユーザー同士のやりとりでは、自動的にPGPによるエンドツーエンド暗号化が行われる。公開鍵のインポートなどの事前準備も必要なく、ふつうにメールを送るだけなのでなにも意識することはない。メールが暗号化されるかどうかは、送信先のアイコンで判別できる。

.. figure:: {static}/images/proton-mail/encrypted-icon.png
   :alt: アイコンによってメッセージが暗号化されることがわかる

   アイコンによってメッセージが暗号化されることがわかる

なお、PGPでのエンドツーエンド暗号化の範囲に、件名を含むメタデータは含まれない。暗号化で保護されるのは、あくまで本文のみだ。
誰が誰に、いつどのくらいメールを送ったかといったデータは、メールプロバイダーや、民間企業へデータを要求できる政府には、つつぬけと考えたほうがいいと思う。

Proton Mail外からのメール受信 — ゼロアクセス暗号化
=====================================================

非Proton MailユーザーがProton Mailユーザーにメッセージを送信するケースについて考える。
相手がPGPユーザーなら、もちろんエンドツーエンド暗号化が可能だ。こちらの公開鍵を何らかの方法で相手に伝えておけばいい。

しかし、相手がPGPユーザーでない場合は、どうしてもメッセージが平文で送られてくる[ref]通信路はTLSで保護されるけど、アプリケーションは平文で受け取る[/ref]。エンドツーエンド暗号化はできない。
この場合でも、Proton Mailは、ユーザーの公開鍵で暗号化を行ってから、受信したメールを保存する。Proton Mailは、この仕組みをゼロアクセス暗号化と呼んでいる。
だから、たとえProton Mailサーバーからのデータ漏洩があったとしても、メッセージ本文はユーザー以外読むことができない。

ただし、これにはいくつか穴がある。まず、メールを受信してから、ストレージに保存するまでの間であれば、Proton Mailは自由にメッセージを読むことができる。実際、Proton Mailは、メモリ上にロードされたメッセージデータを使ってスパムフィルタ処理などを行っている。つまり、エンドツーエンド暗号化と違って、平文を読まれないことが技術的に保証されているわけではない。

また、メッセージを送信してきた相手方のメールボックスには、平文のままのデータが残るし、やりとりの履歴が残る。いくらこちら側で万全の保護をしたとしても、相手方から情報が漏れてしまえばどうにもならない。

ゼロアクセス暗号化の効果は限定的なものに留まると思う。

Proton Mail外へのメール送信 — パスワード保護付きメール
=========================================================

Proton Mail外へのメール送信は、相手がPGPユーザーであれば、Proton Mailユーザーのように通常のエンドツーエンド暗号化が可能だが、そうでない大多数のユーザーとは、暗号化した状態でメールをやりとりすることができない。
そこで代替手段として、パスワード保護付きメッセージという手段が用意されている。
これは、パスワードによる保護をかけた状態でメッセージをProton Mailサーバー上に保存した上で、メール本文には、メッセージへのリンクを記載し、Proton Mailサーバー上でメッセージのやりとりをするというものだ。パスワードは共通鍵なので、なんらかの方法でプライベートに共有しておく必要がある。
この場合もメッセージはエンドツーエンド暗号化される。

メール検索
=============

Proton Mailでは、メールの検索機能も提供されている。サーバーサイドでメール本文にアクセスできない状況で、どうやってメール検索を実装するのか。
これについては、Proton Mailから `解説記事が公開されている。 <https://proton.me/blog/engineering-message-content-search>`_

世の中には、 `検索可能暗号(Searchable Encryption) <https://atmarkit.itmedia.co.jp/ait/articles/1509/29/news003.html>`_ という技術が存在しており、それを使えば、暗号化されたデータに対して直接検索をかけられる可能性があるらしい。
が、Proton Mailでは、これらの技術は、まだ研究途上であり、実用段階にはいたっていないと判断し、導入しなかった。

結論として、Proton Mailは、単純にクライアントサイド(Web版ならブラウザ内)で、検索を行っている。

Proton Mail(Web版)は、ブラウザ内のIndexedDBに検索用インデックスを構築する。メッセージはOpenPGPで暗号化されているので、まずは復号する必要がある。そして、タグの除去など、メッセージを検索しやすいように整形した上で、メタデータと共に `WebCrypt API <https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API>`_ でAES-GCMで暗号化して、検索用インデックスに格納される。Proton Mailは、メッセージIDをキーとするフォーワードインデックスを採用している。なお、検索時に毎回復号しているわけではなく、平文のインデックスがキャッシュされる。

スパムフィルタ
================

暗号化を前提とする環境で、Proton Mailは、スパムフィルタをどのように実現しているのだろうか。
スパムフィルタについても、エンドツーエンド暗号化がされているケースと、そうでないケース(ゼロアクセス暗号化)で対応が違ってくる。

ゼロアクセス暗号時のスパム対応については、 `公式ブログに解説がある。 <https://protonmail.com/blog/encrypted-email-spam-filtering/>`_

Proton Mailの解説によると、非暗号化メール受信時には、送信元IPアドレスのチェック、ベイジアンフィルタ、メッセージチェックサムとスパムデータベースの照合、DMARC等による真性性の検査、ユーザー定義のスパムフィルタ、といった処理を暗号化する前にメモリ上で行っているようだ。

エンドツーエンド暗号化環境でのスパム処理については、ドキュメントはないものの、その性質上、重要な処理は必ずブラウザ内で起きているはずなので、論理的には、ソースコードを読めばどのように対処しているのかわかるはずだ。だれかコードを読んで教えてください。

メールのインポート
====================

メールは重要なデータベースなので、メールサービスを新しく使いはじめるのであれば、いままで受信したメールデータも移行したい。
ぼくの場合は、Maildir形式でローカルディスクにメールを保持していたので、それをインポートできるかどうかが、サービス選定にあたって重要なポイントのひとつだった。

Proton Mailでは、 `専用のアプリ <https://proton.me/support/export-emails-import-export-app>`_ で Mbox形式のインポートをサポートしていたので、PythonでMaildirからMboxに変換して、専用アプリでMboxをインポートすることで、無事全メールをProton Mailに移行することができた。当時、Mboxのインポートをサポートしていたのは、候補に上がったサービスの中ではProton Mailだけだった。

ちなみに、Gmailや他のプロバイダーからのデータ移行も `もちろんサポートしている。 <https://proton.me/support/easy-switch>`_

データ漏洩 — 国家はデータを監視している
=========================================

`プライバシーは人間にとって本質的に大事なものだ。 <https://www.ted.com/talks/glenn_greenwald_why_privacy_matters>`_ 自分が明かしたいと思った相手以外に、私的なやりとりを勝手に覗き見されたくはない。

なぜ、PGPによるエンドツーエンドの暗号化(やゼロアクセス暗号化)が必要なのだろうか。TLSで、通信路が暗号化されているなら、それで十分ではないのか。
理由はいくつか考えられる。たとえば、Yahoo Mailは、 `2013年に30億アカウントのデータ漏洩を起こした。 <https://proton.me/blog/protonmail-security-advisory-regarding-yahoo-hack>`_ Proton Mailでも同様の事故が今後起きることは十分考えられる。しかし、エンドツーエンド暗号化されていれば、たとえサーバーからデータが漏洩したとしても、他人に中身を読まれることはない。

それから、運営者がデータを利用または悪用することもできない。エンドツーエンド暗号化でなければ、運営者が勝手に自分のメールを他人に渡したり、広告など個人を追跡するために使ったりしないという保証はない。すくなくとも技術的には。

`エドワード・スノーデンの告発 <https://www.theguardian.com/world/interactive/2013/nov/01/snowden-nsa-files-surveillance-revelations-decoded>`_ であきらかになったとおり、国家権力は、インターネット技術を利用して国民を監視している。スノーデン以降、国家による直接の大量監視に制限はかかったものの、現在でも、 `民間企業のデータを通じて間接的な監視は行われているようだ。 <https://www.wsj.com/articles/federal-agencies-use-cellphone-location-data-for-immigration-enforcement-11581078600>`_ また、国家は、必要であれば裁判所を通じて、インターネット企業にデータの提出を要求できる。しかも、民間企業はそれらのデータを提出した事実を `秘匿しなければならないこともある。 <https://en.wikipedia.org/wiki/Gag_order>`_ そういったケースは、 `企業が公表している透明性データ <https://transparency.fb.com/data/government-data-requests/?source=https%3A%2F%2Ftransparency.facebook.com%2Fgovernment-data-requests>`_ などにも表れてこない。 国家による監視がどこまで行われているのかについては、 `「超監視社会: 私たちのデータはどこまで見られているのか? 」 <https://www.amazon.co.jp/dp/4794222378/>`_ という本に詳しく書かれている。こういった標的を定めない大量監視の効果は、エンドツーエンド暗号化が使われていれば、かなり弱めることができる。

ただし、 `Proton Mail自身が勧告している <https://protonmail.com/blog/protonmail-threat-model/>`_ ことだけど、国家が本気になって個人を標的にした場合、エンドツーエンド暗号化をもってしても秘密を守りきれない可能性が高い。だから、たとえばスノーデンのように国家には歯向かって秘密を暴露しようとしている人などには、Eメールの使用自体おすすめできない。


ところで、Gmailはユーザーのメールを売り物にしてるの?
======================================================

Proton Mailのブログを読んでいると、しきりに、Gmailの利用にはプライバシー上の懸念があるという主張がなされている。
これは、ほんとうだろうか。

まず、事実として、Gmailは2004年のリリースから長らく、 `ユーザーのメールボックスをスキャンして <https://privacyrights.org/resources/privacy-and-civil-liberties-organizations-urge-google-suspend-gmail>`_ 物品の購買情報等個人情報を把握し、それを元にユーザーに合わせた広告を表示してきた。

しかし、2014年ごろから、エンタープライズユーザーの拡大と顧客企業からの懸念を背景に、段々とメールボックスのスキャンをやめてきた。
そして、2017年には、広告を目的としたメールボックスのスキャンを `完全に停止した。 <https://www.nytimes.com/2017/06/23/technology/gmail-ads.html>`_ Googleは、現在、広告のためにGmailのメッセージをスキャンしないし、個人情報を売ることはないと `表明している。 <https://support.google.com/mail/answer/6603>`_

現在、Gmailについて指摘されているプライバシー上の問題には、以下のようなものがある:

* Gmailはメールの自動返信や予定のカレンダーへの自動登録など、ユーザーの利便性を理由とするメールボックスのスキャンは、 `今でも行っている。 <https://proton.me/blog/is-gmail-secure>`_
* Gmailにはアドオンと呼ばれるサードパーティーによる拡張機能とそのためのAPIがある。ユーザーが許可をすればサードパーティーは自由にメールボックスにアクセスできる。いくつかのアドオンは、ユーザーの意図しない形でメールにアクセスしていた。

Return Pathというマーケティングツールの事例が `WSJによって報道された。 <https://www.wsj.com/articles/techs-dirty-secret-the-app-developers-sifting-through-your-gmail-1530544442>`_ Return Pathは多くのアドオンベンダーと提携しており、Return Path提携企業の提供する数多くのアドオンが流通している。Earny社による商品価格自動比較アドオンもその一つだった。これをインストールしたユーザーは、知らぬ間に、自身のメールをReturn Pathのマーケティングツールのためのデータとして提供することになる。

ただ、サードパーティーへのアクセスを許可する際には、必ず読取権限を明示的に要求されるので、たとえその利用方法が(Earnyのケースのように)想定外だったしても、ユーザーは許可をしていることにはなる。
Google自体は、現在ではプライバシーに配慮したメールボックスの取り扱いをしているかもしれないが、サードパーティーはその限りではない。アドオンに権限を渡す際には注意が必要だろう。
この記事を書くにあたって色々調べてみて、個人的には、Gmailは、もはや以前ほど不健全ではないのかもしれないという感触を持った。

しかし、企業である以上、政府から要求されればデータは提供するしかない。そして、エンドツーエンド暗号化でない以上、メールのコンテンツに第三者でもアクセスできてしまう。その意味で、究極的には、Gmailに対するプライバシー上の懸念は永遠に払拭されることはない、というのはそうなのだろうと思う。

クライアントのソースコード
===============================

Proton Mailはクライアントサイドのコードをオープンソースソフトウェアとして、GitHub上で公開している。
メインの `ウェブクライアント <https://github.com/ProtonMail/WebClients>`_ はもちろん、iOSやAndroidその他各種ライブラリも含め積極的に `公開している。 <https://github.com/ProtonMail>`_

ちなみに、Proton Mailのクアイアントは元々AngularJSで実装されていたけど、何年か前にReactに移行した。

ソースコードが公開されているのは、エンドツーエンド 暗号化を売りにしているProton Mailにとって意味のあることだ。
エンドツーエンド暗号化において、重要なことはすべてクライアントサイドで起こる。だから、われわれユーザーは、理論的には、ソースコードを精査することによって、情報が漏れることも改竄されることもなく相手に伝わると確証できる。

公開されているのはクライアントサイドのみで、サーバーサイドのソースコードは公開されていない。だから、非暗号化メールを受信したときの、スパムフィルタやゼロアクセス暗号化など、サーバーサイドで起こる部分については、なにが行われているのか、ほんとうにはわからない。もっとも、サーバーサイドでどんなコードが動いているのかは、本質的に不透明なので、たとえソースコードが公開されていてもあまり意味はないかもしれない。

認証から秘密鍵取得までの過程
-------------------------------

Proton Mailでは、一度もログインしたことのない端末からでも、アカウント名とパスワードさえ入力すれば、自分のメールを読むことができる。
つまり、ログイン時に秘密鍵が暗号化された状態でダウンロードされて、それを復号するという処理がブラウザ内で起きているはずだ。
そのあたりの処理がどうなっているのか気になったので、ソースコードから調べてみた。

まず、ブラウザ内でパスワードを入力するUIはわかっているので、そこを起点にブラウザのInspectorを使って調べていく。すると、input要素の属性などから、 `LoginForm <https://github.com/ProtonMail/WebClients/blob/0631583898f1a9019969e0defe09b5253e1d4523/applications/account/src/app/login/LoginForm.tsx>`_ というコンポーネントに辿りつき、 `loginActions <https://github.com/ProtonMail/WebClients/blob/0631583898f1a9019969e0defe09b5253e1d4523/packages/components/containers/login/loginActions.ts>`_ というファイルがログインまわりの処理をしていることがわかった。

認証時の処理については、 `ブログに詳しい解説がある。 <https://proton.me/blog/encrypted-email-authentication>`_ Proton Mailでは、 `SRP(Secure Remote Password)による認証を行っている。 <https://github.com/ProtonMail/WebClients/blob/1215e18025ca1d39af95a08a0930b1e116f57d21/packages/shared/lib/authentication/loginWithFallback.ts#L38-L44>`_ ログインパスワードがそのまま秘密鍵を得るための鍵になるので、パスワードはブラウザの外に出してはいけない。SRPは、DH鍵交換に似た仕組みで、これによりパスワードをProton Mailに送信せずに、認証を行える。
SRPの結果として、 `ユーザーIDやアクセストークン <https://github.com/ProtonMail/WebClients/blob/1215e18025ca1d39af95a08a0930b1e116f57d21/packages/shared/lib/authentication/interface.ts#L16-L30>`_ が得られる。

処理を追っていくと、どうやら認証後にサーバーから `ユーザー情報 <https://github.com/ProtonMail/WebClients/blob/0631583898f1a9019969e0defe09b5253e1d4523/packages/shared/lib/interfaces/User.ts#L19-L42>`_ を取得し  、 そこには `秘密鍵 <https://github.com/ProtonMail/WebClients/blob/0631583898f1a9019969e0defe09b5253e1d4523/packages/shared/lib/interfaces/Key.ts#L20>`_ が暗号化された状態で入っていることがわかった。

次に、ログインパスワードとソルトから、 `秘密鍵復号用のキーを生成する。 <https://github.com/ProtonMail/WebClients/blob/1215e18025ca1d39af95a08a0930b1e116f57d21/packages/srp/lib/keys.ts#L10-L18>`_ それを用いて、 `秘密鍵を復号する。 <https://github.com/ProtonMail/WebClients/blob/1215e18025ca1d39af95a08a0930b1e116f57d21/packages/components/containers/login/loginHelper.ts#L21-L33>`_
なお、秘密鍵用のキーは、セッション情報の一部として、ローカルストレージにキャッシュされる。

..
  sequenceDiagram
      participant Client
      participant SRP module
      participant Server
      Client->>SRP module: ユーザー名、パスワード
      SRP module->>Server: SRP認証
      Server->>SRP module: ユーザーID、アクセストークン
      SRP module->>Client: ユーザーID、アクセストークン
      Client->>Server: User API
      Server-->>Client: Userモデル(暗号化された秘密鍵付き)
      Client->>Server: Salt API
      Server-->>Client: ソルト
      Client->>SRP module: パスワード、ソルト
      SRP module->>Client: 秘密鍵用パスワード

.. figure:: {static}/images/proton-mail/authentication-with-srp.png
   :alt: SRPによる認証、暗号化された秘密鍵取得、秘密鍵用の共通鍵生成

   SRPによる認証、暗号化された秘密鍵取得、秘密鍵用の共通鍵生成(パスワードはサーバーに送信されない)

では、秘密鍵はどういうアルゴリズムで暗号化されているのだろうか。

どうやらWorkerの `importPrivateKey <https://github.com/ProtonMail/WebClients/blob/0631583898f1a9019969e0defe09b5253e1d4523/packages/crypto/lib/worker/api.ts#L294-L320>`_ というメソッドが秘密鍵の復号を行っているようだ。名前からわかるとおり、鍵の処理はワーカースレッドで行われるらしい。

その中身を追っていくと、 `openpgp.js <https://openpgpjs.org/>`_ (これ自体Proton Mailによってメンテナンスされている)の `decrypt <https://github.com/openpgpjs/openpgpjs/blob/2f8a8c1c9af37685e9f2c7af9c37324881935b48/src/packet/secret_key.js#L309-L368>`_ というメソッドにいきつく。

はじめて聞いたけど、 `S2K(String-to-Key) <https://www.rfc-editor.org/rfc/rfc4880#section-3.7>`_ という文字列を鍵に変換するための枠組みが規定されていて、どうやらそれに則った処理になっているようだ。
そこから、 `AEAD <https://developers.google.com/tink/aead>`_ 、またはAESのCFBモードに分岐しているらしいが、どういう条件なのかはよくわからない。

いずれにせよ、秘密鍵は、ユーザーが指定したパスワードとサーバーから取得されたソルトからハッシュ関数で生成されたパスワードで、AES(対象鍵暗号化の標準)で暗号化されていることがわかった。

..
  sequenceDiagram
      Client->>OpenPGP: 秘密鍵用パスワードと暗号化された秘密鍵
      OpenPGP-->>Client: 平文の秘密鍵

.. figure:: {static}/images/proton-mail/decryption-with-openpgp.png
   :alt: OpenPGPによる秘密鍵の暗号化解除

   OpenPGPによる秘密鍵の暗号化解除


もちろん、これはあくまで1ケースで、実際には2FAが入るパターンなど色々な分岐がある。

Proton Mail所感
======================

世の中Gmailが支配的で、PGPもあんまり普及してないらしい。そして、Proton Mailユーザー同士やPGPユーザー相手じゃないとエンドツーエンド暗号化は機能しない。だとすると、けっきょくProton Mailを使ってたとしても、実質的にエンドツーエンド暗号化ではないじゃんとは思った。
そこは、Proton Mailについて調べるとまず第一に気になったことだ。「エンドツーエンド暗号化であらゆるコミュニケーションがプライベートであることが、 **技術的に** 保証されています」、だったら、どれだけ話がわかりやすかったことか…。

ただ、それでも、現状のウェブシステムでは、電子メールはまだまだ必要不可欠なツールなので、どうしても使っていく必要がある。
その上で、Proton Mailは選択肢として悪くないし、Proton Mailの月額課金ビジネスモデルは健全だと思うので、今後とも使っていきたい。

純粋に対人でのコミュニケーションで、エンドツーエンドの暗号化を期待するのであれば、他の選択肢もある。たとえば、`Signal <https://signal.org/en/>`_ [ref]ちなみにぼくはSignalユーザーでもある。ただし、いまのところSignalは、妻専用アプリと化していて、他の人とのやりとりでは、くやしながらLineを使っている。[/ref] やTelegramなどのメールではないメッセージングアプリのほうが、アプリとしての使い勝手など、優れている面があるではないかと思う。これらならば、すべてのやりとりでエンドツーエンド暗号化が保証されるので、話としてもわかりやすい。ただ、けっきょく、PGPも含め、ツールを使えるかは相手ありきで、自分だけではどうにもならないのが、歯痒いところだ。

Proton Mail自体のメーラーとしての使い勝は、悪くない。数年間使ってみて、スパムフィルタや検索なども問題なく、ふつうに使えている。
特定のサービスからのメールがどうしても届かないということが1、2回あったけど[ref]ためしにGmailで登録してみたら届いた[/ref]、まあ支障はない。
たぶん、Gmailには、もっと便利な自動分類機能や、他のサービスとの連携機能などが提供されているのだろうけど(ユーザーじゃないので、くわしくは知らない)、メールにそこまで高度な機能は求めてないので、とくに問題ない。

参考リンク
=====================

* `Is Privacy Under Attack? <https://protonmail.com/blog/privacy-under-attack/>`_ 監視資本主義を脱却して、サブスクリプションモデルに移行しよう。これこそウェブサービスのあるべき姿だ。
* `Why privacy matters <https://www.ted.com/talks/glenn_greenwald_why_privacy_matters>`_ プライバシーは人間にとって本質的に重要なものだ。
* `The ProtonMail Threat Model <https://protonmail.com/blog/protonmail-threat-model/>`_ Proton Mailの脅威モデル。Proton Mailは、どういうユーザーに向いていて、どういうユーザーには向かないか。
* `How encrypted email works <https://proton.me/blog/encrypted-email>`_ Proton Mailで使われている暗号技術の概要。
* `What is end-to-end encryption and how does it work? <https://protonmail.com/blog/what-is-end-to-end-encryption/>`_ Proton Mailによるエンドツーエンド暗号化の解説。
* `What is zero-access encryption and why it is important for security <https://protonmail.com/blog/zero-access-encryption/>`_ ゼロアクセス暗号化の解説。エンドツーエンド暗号化との違い。ゼロアクセス暗号化がデータ漏洩に効果的であること。
* `What is PGP encryption and how does it work? <https://protonmail.com/blog/what-is-pgp-encryption/>`_ Proton MailによるPGPの解説。
* `Improved Authentication for Email Encryption and Security <https://proton.me/blog/encrypted-email-authentication>`_ Proton MailによるSRP認証の解説。
* `Behind the scenes of Proton Mail’s message content search <https://proton.me/blog/engineering-message-content-search>`_ Proton Mailのメッセージ検索解説。
* `Effective Spam Filtering with Encrypted Email <https://protonmail.com/blog/encrypted-email-spam-filtering/>`_ Proton Mailのスパムフィルタ解説(外部からメッセージが到達したときの処理のみ)。
* `Encrypt Message for Non-ProtonMail Recipients <https://protonmail.com/support/knowledge-base/encrypt-for-outside-users/>`_ Proton Mailのパスワード保護メールの使いかた。
* `How to use PGP with Proton Mail <https://proton.me/support/how-to-use-pgp>`_ Proton MailでのPGPの使い方。公開鍵の送付、アップロード、信用など。
* `Why Switzerland? An Analysis of Swiss Privacy Laws <https://protonmail.com/blog/switzerland/>`_ スイスの法律は、他国に比べてプライバシー保護が強いという主張。
* `Impact of Swiss surveillance laws on secure email <https://protonmail.com/blog/swiss-surveillance-law/>`_ スイスで新設された大量監視法の影響についての分析。スイスの諜報機関は国内の案件にしか興味がないので、NSAなど諸外国に情報をオープンにすることはない。法律では、保存されたデータを提出させることはできるが、ユーザーを監視させることはできない。保存されたデータは、エンドツーエンド暗号化されているので安全である。(2015年)
* `Why Proton Mail Is More Secure Than Gmail <https://protonmail.com/blog/protonmail-vs-gmail-security/>`_ なぜProton Mailは、Gmailよりセキュアなのか。エンドツーエンド暗号化、SRP、スイスの法律、追跡やログがないこと、など。アプリの種類が少ないから攻撃面がすくないことも挙げているけど、MailとVPNしかなかった当時と比べて、いまではProtonもいろんなアプリを提供しているので、もう妥当とは言えない。
* `Privacy isn’t free. Here’s why that’s a good thing. <https://protonmail.com/blog/ad-free-business-model/>`_ Proton Mailがどうやって金銭を得て、それをどんなことに使っているのか。サービスの運営に加え、法的な活動、セキュリティー活動、OSS活動など。
* `Google Says It Doesn’t 'Sell' Your Data. Here’s How the Company Shares, Monetizes, and Exploits It. <https://www.eff.org/deeplinks/2020/03/google-says-it-doesnt-sell-your-data-heres-how-company-shares-monetizes-and>`_ GoogleはRTBと呼ばれる広告オークションの仕組みを通じて、実質的にユーザー情報を売っている。(2020年)
* `How Gmail ads work <https://support.google.com/mail/answer/6603>`_ Gmailの広告についての説明。Google自身はメールボックスのスキャンはしないと言っている。
* `Google Will No Longer Scan Gmail for Ad Targeting <https://www.nytimes.com/2017/06/23/technology/gmail-ads.html>`_ Googleは、今後広告のためのメールボックススキャンを止める。(2017年)
* `Google Will Keep Reading Your Emails, Just Not for Ads <https://variety.com/2017/digital/news/google-gmail-ads-emails-1202477321/>`_ Googleは、広告目的のスキャンをやめただけで、すくなくともユーザーの利便性のためにメールボックスをスキャンし、サーバーにデータを送信し続ける。(2017年)
* `Tech’s ‘Dirty Secret’: The App Developers Sifting Through Your Gmail <https://www.wsj.com/articles/techs-dirty-secret-the-app-developers-sifting-through-your-gmail-1530544442>`_ Googleは「アドオン」と称してサードパーティーへのメールボックスアクセスを許可している。そこからデータが漏洩している(2018年)。
* `Google、「サードパーティ開発者がGmailの内容を読んでいる」報道について説明 <https://www.itmedia.co.jp/news/articles/1807/04/news055.html>`_ WSJのReturn Path報道に対する補足(2018年)。
* `As G Suite gains traction in the enterprise, G Suite’s Gmail and consumer Gmail to more closely align <https://blog.google/products/gmail/g-suite-gains-traction-in-the-enterprise-g-suites-gmail-and-consumer-gmail-to-more-closely-align/>`_ G Suiteユーザーと同様、今後は一般向けGmailユーザーのメッセージも、広告用のデータとしては使わない。
* `What Yahoo’s NSA Surveillance Means for Email Privacy <https://protonmail.com/blog/yahoo-us-intelligence/>`_ Yahooは、NSAとFBAからの要求で、ユーザーを監視するソフトウェアの設置を強制されていた。
* `Edward Snowden's Email Provider Shuts Down Amid Secret Court Battle <https://www.wired.com/2013/08/lavabit-snowden/>`_ スノーデンの使っていた米国のプライバシーファーストなメールプロバイダーLavabitは、おそらく、当局からの圧力の結果、10年間続いたサービスの幕を閉じた。
* `Don’t be fooled by Google’s fake privacy <https://protonmail.com/blog/google-fake-online-privacy/>`_ Goolgeは、世間がプライバシーを気にするようになってきたのに合わせて、気にしているようなそぶりを見せはしているが、以前として広告で儲けている企業である以上、真に受けてはいけない。
* `The real problem with encryption backdoors <https://protonmail.com/blog/encryption-backdoor/>`_ 当局は、数十年にわたって、暗号化へのバックドアを仕掛けようとしてきた。暗号化へのバックドアとは、意図的に暗号に弱点を作り込み、政府がアクセスできるようにすることだ。しかし、良い物だけが使えるバックドアなどというものは存在しないのだから、暗号化のへのバックドアは本質的に危険なものだ。
* `Why we created ProtonCA <https://proton.me/blog/why-we-created-protonca>`_ Proton Mailがなぜ独自CAを運営しているのか。Proton Mail自身がCAを持つことで、third-party signaturesを通じて、全Proton Mailユーザーの鍵の真性性を簡単に証明できるから。
* `email is bad <https://emailisbad.com/>`_ Eメールにはダメなところもたくさんあるけど、おおむね他のものよりはいいよという話。
* `Why you should stop using SMS <https://proton.me/blog/stop-using-sms>`_ SNSは、暗号化による保護がまったくないし、いくつかの弱点が知られているので、使うのをやめたほうがいい。認証には2FA認証アプリを使う。メッセージングには、iMessage, RCS, Signal, Telegram, WhatsApp, Meta Messangerなどを使う。
* `Government Requests for User Data <https://transparency.fb.com/data/government-data-requests/?source=https%3A%2F%2Ftransparency.facebook.com%2Fgovernment-data-requests>`_ Metaの公開している、政府からのデータ要求件数。おそらくGAGオーダーは含まれていない。しかし、 `以前は含まれていた…? <https://www.digitaltrends.com/social-media/facebook-government-requests-gag-order/>`_
* `Here's an actual Top Secret document published in 2014 showing an example of NSA's "sorry, can't decrypt PGP" message. Cryptography works: <https://twitter.com/Snowden/status/878686842631139334>`_ PGPによる暗号化がNSAの盗聴を防いだ例。
* `Google Will Keep Reading Your Emails, Just Not for Ads <https://variety.com/2017/digital/news/google-gmail-ads-emails-1202477321/>`_ Googleは、広告目的には使わないというだけで、ユーザーのメールを読むこと自体は続ける。
* `Massive corporate databases become government tools of surveillance <https://proton.me/blog/privacy-user-data-requests>`_ 民間企業のデータが、政府の監視ツールとなりつつある。政府が民間企業にデータを要求する件数は年々増えている。
* `Federal Agencies Use Cellphone Location Data for Immigration Enforcement <https://www.wsj.com/articles/federal-agencies-use-cellphone-location-data-for-immigration-enforcement-11581078600>`_ 米政府は、民間企業から、ユーザーの位置データを購入し、移民の監視に利用している。(2020年)

