mutt + notmuch でコマンドラインメール送受信環境を構築する(Mac OS X編)
######################################################################

:date: 2016-2-12
:slug: mutt-and-notmuch
:tags: mail, mutt, notmuch
:summary: この記事では、muttというコマンドラインのメールクアイアントにnotmuchというメール検索プログラムを組み合わせて、Mac OS X上で、メール送受信環境を構築する方法を説明します。

..

    「メールクライアントはどれだってひどい。このメールクライアントは、ひどさがマシってだけ」
    
     -- mutt作者

この記事では、muttというコマンドラインのメールクアイアントにnotmuchというメール検索プログラムを組み合わせて、Mac OS X上で、メール送受信環境を構築する方法を説明します。不明点があればコメントでどうぞ。

.. contents:: 目次

メールの基礎知識
=================

環境構築の説明に入る前に、メール関連の基礎知識を簡単に説明しておきます。

MxA
~~~~

メールシステムに関わるサブシステムとして、以下のようなものがあります。どれも(Mail|Message) * Agentという名前なので、総称してMxAと呼ばれたりします。
必ずしも、それぞれが、ひとつのプログラムに対応しているとは限らず、あるサブシステムの役割に相当するプログラムを同時に複数使うこともありますし、単一のプログラムが、複数のサブシステムの役割を担うこともあります。

.. figure:: {filename}/images/mutt_and_notmuch/MxA.png
   :alt: メールシステム

   メールに関わるサブシステムの図 `General overview of the mail processing chain <http://dev.mutt.org/trac/wiki/MailConcept/Layout>`_ から転載

* MTA(Message Transfer Agent): メールを転送するためのシステム。
* MUA(Mail User Agent): いわゆるメーラー。人間がメールを読み書きするためのシステム。
* MRA(Mail Retrieval Agent): メールを受信するためのシステム。
* MDA(Mail Delivery Agent): メールを処理して振り分けるためのシステム。
* MSA(Mail Submission Agent): ざっくり言うと認証機能付きのMTA。

関連するプロトコル
~~~~~~~~~~~~~~~~~~

メールに関連するプロトコルとして、以下の3つがあります。

* SMTP: メールの転送をするための基本プロトコル。MTA間での転送や、MUA -> MTA間の転送で使われる。
* POP3: リモートにあるメールボックスからローカルにメールをダウンロードするためのプロトコル。
* IMAP: リモートにあるメールボックスをローカルから閲覧・操作するためのプロトコル。自宅のデスクトップと会社のノートPCなど、複数の環境からメールボックスにアクセスするときに便利。

メールボックス
~~~~~~~~~~~~~~~

メールボックス(メールを格納するためのデータ構造)には、いくつかの普及しているフォーマットがあります。
大きくわけて、mbox系のすべてのメールを1ファイルに格納するフォーマットと、Maildir系の1メール1ファイルで格納するフォーマットの2種類です。
1メール1ファイルで格納する形式のほうが、スクリプトで処理する場合などになにかと扱いやすく便利なので、Maildirに格納することにします。

筆者のメール環境
=================

このブログもそうですが、自分のサイトのホスティング先として、さくらインターネットの `レンタルサーバー <http://www.sakura.ne.jp/>`_ を利用しています。
プランは、スタンダードプランです。
このプランでは、無制限のメールアドレスを利用できて、メールボックスには、POP3とIMAPでアクセスできます。
また、sshでリモートホストにログインして作業することができます。

本題からは逸れますが、実際にリモートにログインすると、メールは、Maildir形式のメールボックスに保存されているようです。
また、sendmailもセットアップ済みで、コマンドラインからメールを送信できます(実際にメールの送信手段として利用します)。

やりたいことは、レンタルサーバー上のメールボックスから、定期的にPOP3でメールを受信して、閲覧できる環境を構築することです。
サーバーで利用できる容量が限られており、受信したメールはサーバー上から削除したいので、IMAPは使いません。

筆者は、さくらサーバー上で、用途に応じた3つのメールボックスを運用しています。
それから、パートナー企業から発行された別のサーバー上のもの(POP3)も加えて、計4つのメールボックスを日常的に使用します。

動機
====

筆者は、これまでいくつかのメール環境を試してきました。

はるか昔には、GMail一本でやっていた時期がありました。快適な環境ではありましたが、宗教上の理由により、あるときから、クラウドでのメール環境の使用をやめました。
また、仕事上、パートナー企業のメールアカウントを使う必要があるため、どちらにしろローカルでのメール受信が必要となるのですが、ローカルでひとつの環境に統一できれば、スッキリします(統一するだけなら、GMailのメールボックスにPOP3やIMAPでアクセスすれば可能ではありますが)。

Mac OS Xを使い始めてからしばらくは、標準のMail.appを使用していました。しかし、これはメールボックスが複数になり、メールの件数が増えてくるにつれ、次第に動作が遅くなり、使うのが苦痛になってきました。
メールボックスの切り替えに異常に時間がかかったり、突発的に固まったりするのです。

Mail.appの代わりになる、軽量なメールクライアントはないか探した結果、Sparrowを見付けました。なんとなく見た目がスッキリしていて良さそうだったので、しばらく使っていましたが、Gmailのフロントエンドとして使うことが前提の設計になっているためスパムフィルターがない、しばしばメールが文字化けする、開発終了してしまった、などの問題があり、他のソフトを探しはじめました。

また、個人的に、コマンドラインでできることは、できる限りコマンドラインで済ませたい人間なので、CLIのプログラムであることを条件としました。
メールの読み書きは、本質的にテキストのみで成立するはずだからです。

使用するプログラム
===================

メール送受信システムを構築するために利用するプログラムのリストは、細かいものも含めると、以下のようになります。

* `mutt <http://www.mutt.org/>`_
* `notmuch <https://notmuchmail.org/>`_ 
* `getmail <http://pyropus.ca/software/getmail/>`_
* `spamassassin <http://spamassassin.apache.org/index.html>`_
* `Razor2 <http://razor.sourceforge.net/>`_
* `terminal-notifier <https://github.com/julienXX/terminal-notifier>`_
* launchd
* ssh + sendmail

ずいぶん数が多いと思われるかもしれませんが、これは、muttやnotmuchが、単機能のプログラムを組み合わせて使うという `UNIX哲学 <https://ja.wikipedia.org/wiki/UNIX%E5%93%B2%E5%AD%A6>`_ に従った設計になっているためです。
ここに挙げたプログラムすべてを使うことが必須というわけではなく、気に食わないものがあれば、部分的に別のプログラムに変えることもできます。
また、ちょっとしたスクリプトを書いて、自分好みにカスタマイズすることも容易にできるのです。

ほとんどのプログラムは、Homebrewでパッケージ化されているので、 :code:`brew install` でインストールできます。SpamAssassinとRazor2だけは、Homebrewにはないため、CPANからインストールします。

mutt
~~~~

.. figure:: {filename}/images/mutt_and_notmuch/mutt.png
   :alt: muttのインデックス画面

   muttのインデックス画面

コマンドラインで使えるスクリーン指向のMUAです。
Linuxカーネル開発者の中にもmuttを使用している人は `多いようです。 <http://cpplover.blogspot.jp/2013/06/linux.html>`_ 
軽量で、マクロによってある程度柔軟に拡張できます。
また、サイドバー表示など本体への拡張機能もいろいろ開発されていますが、パッチを当てて自分でビルドしなければならないのは、すこしめんどうです。
むかしながらのフリーソフトウェアなのでしょうがないですね。
mutt自体は、あくまでMUAであり、ローカルのメールボックスからメールを読み込んで表示したり、メールを書くためだけのソフトウェアなのですが、
いちおうオマケ機能として、POP3やIMAPでメールを受信したり、SMTPでメールを送信するための機能も付いているので、これ単体でもクライアント環境として成立します。

muttには、日本語化パッチがありますが、最新のバージョンに追随していなかったりするため、Homebrewにあるバージョンをそのまま使っています。メール一覧で、件名が長い場合などにときどき表示崩れが起きたりすることがありますが、ウィンドウを十分に長くすれば問題は起きないので、筆者はあまり気にしていません。

実のところ、キーバインディングに統一性がない部分など、UI的にあまり良いとは思っていないのですが、OS X環境で他に手軽に使えるものが他になかったため、これを使っています。

notmuch
~~~~~~~

Maildirに格納されているメールのインデックスを作成し、高速に検索するためのプログラムです。
似たようなプログラムに `mu <http://www.djcbsoftware.nl/code/mu/>`_ というのもあって、これも良さそうだったのですが、残念ながら `日本語の扱いに問題があった <https://github.com/djcb/mu/issues/544>`_ ため、使えませんでした。
notmuchはCJK環境でも問題なく使えます。

notmuchは、ただのメール検索プログラムに留まりません。
メールへのタグ付けと高速なタグ検索機能、そしてマッチしたメールのパス一覧を取得する機能を備えています。
これにより、メール処理の中心となるミドルウェア、あるいは糊付けプログラムとして機能するポテンシャルを秘めているのです。

例えば、新着メールにスパムチェックをかけたいとします(あくまで説明のための例です)。

1. notmuchでは、新着メールに付与するタグを指定できるので、spam-check-requiredというタグをつけることにします。
2. 次に、spam-check-requiredタグのついたメールを検索し、それらのパスを取得してスパムチェックをかけ、スコアを記録するためのヘッダを追加します。
3. 再度、spam-check-requiredタグのついたメールを検索し、spam-check-requiredタグを除去します。

このようにして、新着メールに一度だけ処理をかけることができます。

また、notmuchにはemacs用のフロントエンドも付属しています。これは、notmuchのタグ機能をフルに活かしたMUA環境になっているようですが、筆者はvim使いなので残念ながら使えません。emacs使いの方は、これを利用するのも良いかもしれません。

getmail
~~~~~~~~

POP3やIMAPで、メールを受信するためのプログラム(MRA)です。
muttのメール受信機能では、OS Xのキーチェーンにアクセスすることはできないため、設定ファイルにパスワードを直接記述しなければなりません。
これはあまり好ましくないため、メールの受信はgetmailにさせます。

SpamAssassin
~~~~~~~~~~~~~

スパムフィルタです。パイプでメールファイルを渡すと、スパム判定のスコアを示したX-Spam-Statusというヘッダを挿入してくれます。
このプログラム自体、単純ベイズによるスパム判定機能を搭載していますが、それ以外にも、実にさまざまなスパムフィルタプログラムを統合するファサード的なプログラムとして機能します。複雑なプログラムで、非常に動作が重いです。

Razor2
~~~~~~

協調フィルタリングによるスパムフィルタプログラムです。SpamAssassinと連携させて使います。
類似のプログラムとして、PyzorやDCCなどがあります。これら3つすべてを同時にSpamAssassinと組み合わせて使うことも可能です。
どんどん重くなりそうな気がするので、筆者はひとつに留めています。

terminal-notifier
~~~~~~~~~~~~~~~~~~

好み次第ですが、新着メール受信時にデスクトップに通知が届くと便利です。
terminal-notifierを使えば、コマンドラインからデスクトップに通知を送ることができます。
副作用として、通知センターから、フォルダをまたがった新着メール一覧を確認できるようになります。
[ref]muttでフォルダをまたがって新着を一覧する方法がないものか考えましたが、いまのところ良い術を思い付いていません。[/ref]
結果として、新着メールを確認するために、常にmuttを立ち上げておく必要がなくなります。

Homebrewからインストールできるバージョンンでも実用上問題ありませんが、アイコンを変更できない点が不満だったため、
筆者は、アイコンを差し替えて自分でビルドしたバージョンを使用しています。

launchd
~~~~~~~~

launchdは、OS X組込のジョブ管理プログラムです。cronの代替として使えます。cron自体はOS Xでも使えますが、バックグラウンドでのキーチェーンへのアクセスがうまくいかなかったため[ref]深くは追ってません[/ref]、こちらにしました。
リモートメールボックスのポーリングをするために使います。

ssh + sendmail
~~~~~~~~~~~~~~~

muttには、実は、オマケ機能としてSMTPでメールを送信する機能もついているので、muttからレンタルサーバーへSMTPを通じてメールを送信することもできます。
しかし、残念ながら、OS Xのキーチェーンと連携する機能はないため、パスワードを直接設定ファイルに記述しなければなりません。

sshを利用すれば、リモートサーバー上のコマンドをローカルにあるかのように実行することができるため、これでレンタルサーバー上のsendmailコマンドを実行します。
こうすれば、(SSHの公開鍵設定がしてあれば)パスワードは不要になります。ちなみに、sendmailは、よく使われているメジャーなMTAのひとつです。

ローカルでsendmailコマンドが使えるように設定するという選択肢もありましたが、外向けのポート25は `ISPで制限されている場合が多い <https://ja.wikipedia.org/wiki/Outbound_Port_25_Blocking>`_ という問題があることや、ほとんど設定をせずに済む一番楽な方法がssh + sendmailだったことから、こうしました。

メール受信のシーケンス
=======================

スパムと判定されたメールは、spamフォルダに振り分けます。
ただし、false positiveの可能性があるため、本来のフォルダに戻せるようにしておく必要があります。
そのため、タグに受信メールボックスを記録しておきます。
false negativeの場合は、マニュアルでspamフォルダに移動します(それ用のmuttマクロで行います)。

1. POP3でメール受信
~~~~~~~~~~~~~~~~~~~~

まずは、getmailでメールを受信します。

2. スパム判定
~~~~~~~~~~~~~~

getmailには、受信したメールを外部プログラムに渡してフィルターをかける機能があるので、SpamAssassinに渡します。
データの受け渡しはパイプによって標準入出力で行われます。
これにより、メールにX-Spam-Status等のヘッダが挿入されます。

筆者の環境では、1通あたり3秒くらいかかります。

3. 一時フォルダにメールファイルを保存
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

受信したメールを直接メールボックスに入れてしまうと、この次のスパム報告処理に時間がかかるため、spamフォルダに振り分けられることになるメールが、しばらくmutt上に表示されてしまいます。
これを避けるため、メールファイルは、いったんmuttから見えない一時フォルダに保存しておきます。

4. スパム報告&学習
~~~~~~~~~~~~~~~~~~~

スパム判定の結果に基いて、Razor2のサーバーにレポートを送り、ベイズフィルターの分類器に学習をさせます。
スパムの場合は、X-Spam-StatusヘッダにYesという値が入るため、これをgrepで判定します。
結果に応じて、 :code:`spamassassin` コマンドにメールファイルを与えて、処理を行います。

筆者の環境では、1通毎に2秒ほどかかります。

5. メールファイルをメールボックスに移動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

この後は、もう処理時間のかかる工程はないのと、インデックスを作成するため、メールボックスにメールを移します。

6. 検索インデックス作成
~~~~~~~~~~~~~~~~~~~~~~~

新規受信したメールのインデックスを作成します。新規のメールは、notmuchが自動的に認識します。
また、この後の工程のために、新規のメールには、自動的に :code:`new` タグを付与するよう設定しておきます。

7. 配信先フォルダタグ付与
~~~~~~~~~~~~~~~~~~~~~~~~~

スパム判定でfalse positiveが出てしまった場合に、後で元のメールボックスに戻せるように、 :code:`delivered-to-メールボックス名` というタグを付与しておきます。spamフォルダから元のフォルダに戻すときには、タグを見て移動先を判断します。

処理対象のメールは、 :code:`new` タグ付与されたすべてのメールです。

8. spamフォルダへ移動
~~~~~~~~~~~~~~~~~~~~~

X-Spam-Status: Yesの含まれるメールをspamフォルダに移動します。

処理対象のメールは、 :code:`new` タグ付与されたすべてのメールです。

9. newタグを除去
~~~~~~~~~~~~~~~~

最後に、:code:`new` タグのついたすべてのメールから、:code:`new` タグを除去します。
これでメールの受信処理がすべて完了となります。


各種の設定
===========

すでに筆者の環境では、4つのメールアドレスを使い分けています。
メールアドレスは、仮に、ryu@example.com, ken@example.com, guile@example.com, zangief@example.com としておきます。

メールアドレス毎に、ryu,ken,guile,zangiefという4つのフォルダと、スパムメール用にspamというフォルダを作ります。

mutt
~~~~

詳しくは、muttの `マニュアル <http://www.mutt.org/doc/devel/manual.html>`_ を参照してください。

~/.mutt/muttrc

.. code-block:: txt

    set realname = "Taiju Muto"
    set use_from = yes
    set signature = ~/.mutt/signature
    set sleep_time = 0 # フォルダの切り替えが速くなります。
    unset record # 送信メールの保存は、BCCで自分宛てに送るのでOFFにしてます。
    set postponed = +postponed
    set sort_aux = reverse-date
    set assumed_charset="iso-2022-jp:euc-jp:shift_jis:utf-8" # 文字コード指定がなかったりする場合のために優先順位を設定しておきます
    set index_format = "%4C %Z %{%b %d} %-15.15L %H%s(%?l?%4l&%4c?)" # デフォルトに加えて、スパムのスコアが表示されるようにしてます。
    set sendmail = "ssh tai2@tai2.net sendmail -oem -oi" # メールの送信はレンタルサーバー上のsendmailで。
    set header_cache = ~/.mutt/cache/ # ヘッダーキャッシュをしておくとフォルダの切り替えがだいぶ良くなります。
    spam "X-Spam-Status: Yes, score=([^ \t]+)" "(Spam %1)" # スパムヘッダの定義

    # 色付けは、muttのソースコードに同梱されているcolors.defaultを使っています。
    source ~/.mutt/colors.default

    # HTMLメールを自動で見易くするための設定です。.mailcapも参照。
    auto_view text/html
    alternative_order text/plain text/enriched text/html

    # メールボックス設定
    # mailboxesに追加しておくと、対象フォルダをポーリングして、muttのステータス行で通知してくれます
    set folder = ~/Dropbox/Mail/
    set spoolfile = +ryu
    mailboxes +ryu +ken +guile +zangief
    folder-hook +ryu source ~/.mutt/rc-ryu
    folder-hook +ken source ~/.mutt/rc-ken
    folder-hook +guile source ~/.mutt/rc-guile
    folder-hook +zangief source ~/.mutt/rc-zangief
    folder-hook +spam source ~/.mutt/rc-spam

    # マクロのための設定
    set pipe_split = yes
    set my_wait_key=$wait_key

    # スパム報告用のマクロ。スパム報告してから、spamフォルダにメールを移動します。
    macro index S "\
    <enter-command>set wait_key=no<enter>\
    <pipe-message>report_spam.py $folder<enter><enter-command>\
    set wait_key=$my_wait_key<enter>\
    <first-entry>\
    " "report a spam message"

    # スパム解除用のマクロ。false-positiveが起きたときに使います。
    # スパム否定報告をしてから、本来の受信メールボックスに戻します。
    macro index X "\
    <enter-command>set wait_key=no<enter>\
    <pipe-message>revoke_spam.py $folder<enter><enter-command>\
    set wait_key=$my_wait_key<enter>\
    <first-entry>\
    " "revoke a spam message"

    # notmuchで条件指定して検索した一覧を表示します。
    macro index <F8> \
    "<enter-command>set my_old_pipe_decode=\$pipe_decode my_old_wait_key=\$wait_key nopipe_decode nowait_key<enter>\
    <shell-escape>notmuch-mutt -r --prompt search<enter>\
    <change-folder-readonly>`echo ${XDG_CACHE_HOME:-$HOME/.cache}/notmuch/mutt/results`<enter>\
    <enter-command>set pipe_decode=\$my_old_pipe_decode wait_key=\$my_old_wait_key<enter>" \
        "notmuch: search mail"

    # カーソル上のメールの関連したスレッドを表示します。
    macro index <F9> \
    "<enter-command>set my_old_pipe_decode=\$pipe_decode my_old_wait_key=\$wait_key nopipe_decode nowait_key<enter>\
    <pipe-message>notmuch-mutt -r thread<enter>\
    <change-folder-readonly>`echo ${XDG_CACHE_HOME:-$HOME/.cache}/notmuch/mutt/results`<enter>\
    <enter-command>set pipe_decode=\$my_old_pipe_decode wait_key=\$my_old_wait_key<enter>" \
        "notmuch: reconstruct thread"

マクロで利用しているreport_spam.pyとrevoke_spam.pyは、 `gist <https://gist.github.com/tai2/d186222bc9755c943e6f>`_ に置いておきます。

~/.mutt/rc-ryu

.. code-block:: txt

    # スレッド表示にします。
    set sort = threads
    # メールボックスごとにfromを変えます。
    set from="ryu@example.com"
    # 送信メールの保存用途と、ツリーで完全な会話が見られるようにBccとして自分を入れておきます。
    my_hdr Bcc: ryu@example.com

~/.mutt/rc-spam

.. code-block:: txt

    # スパムメールについてはスレッド表示せず、単純に日付の降順で表示します。
    set sort = reverse-date

~/.mailcap

.. code-block:: txt

    # HTMLメールはw3mで整形して見易く表示されるようにします。
    # see. http://jasonwryan.com/blog/2012/05/12/mutt/
    text/html; w3m -I %{charset} -T text/html; copiousoutput;

notmuch
~~~~~~~~

ほぼデフォルトで生成される設定で使ってますが、新着の記事に :code:`new` というタグを付与するようにしてます。
それから、草稿用のメールボックスと.DS_Storeはインデックス対象から除外するようにしています。

~/.notmuch-configから抜粋。

.. code-block:: txt

    [new]
    tags=unread;inbox;new;
    ignore=postponed;.DS_Store;

`Approaches to initial tagging of messages <https://notmuchmail.org/initial_tagging/>`_ という記事を参考にしました。

notmuchでは、インデックスの前後にフックを仕込めるようになっているため、それを利用しています。

インデックス前処理

.. code-block:: bash

    #!/bin/sh
    status=`ifconfig en0 | sed -n 's/^.*status: \(.*\)/\1/p'`
    if [ $status = 'active' ];
    then
        # getmailでメール受信
        for folder in $MAIL_FOLDERS
        do
            getmail_opt="$getmail_opt --rcfile rc-$folder"
        done
        /usr/local/bin/getmail $getmail_opt

        # スパム報告
        for new_file in `find ~/.getmail/tmp -type f`
        do
            if grep --max-count=1 '^X-Spam-Status: Yes' $new_file > /dev/null
            then
                /usr/local/bin/spamassassin --report $new_file
            else
                /usr/local/bin/spamassassin --revoke $new_file
            fi
        done

        # 一時フォルダからメールボックスに移動
        for dir in $MAIL_FOLDERS
        do
            src=~/.getmail/tmp/$dir/new/
            for file in `ls $src`
            do
                mv $src/$file ~/Dropbox/Mail/$dir/new/
            done
        done
    fi

インデックス後処理

.. code-block:: bash

    #!/bin/sh

    # メールボックス毎のタグを付与
    for folder in $MAIL_FOLDERS
    do
        /usr/local/bin/notmuch tag +delivered-to-$folder -- tag:new folder:$folder
    done

    # スパムメールをspamフォルダに移動
    for new_file in `/usr/local/bin/notmuch search --output=files tag:new`
    do
        if grep --max-count=1 '^X-Spam-Status: Yes' $new_file > /dev/null
        then
            p1=`dirname $new_file`
            p2=`dirname $p1`
            dest_dir=`dirname $p2`/spam/new
            mv $new_file $dest_dir
        else
            /Users/tai2/bin/notify-message.py $new_file
        fi
    done

    # newタグを除去
    /usr/local/bin/notmuch tag -new -- tag:new

`notify-message.py <https://gist.github.com/tai2/16b8acf511a92638da46>`_ は、メールをパースして、terminal-notifierに送信者と件名を渡して起動するためのスクリプトです。

getmail
~~~~~~~~


ほとんど同内容の設定ファイルが4つあるのは、DRY原則に反していてアレですが、筆者の運用環境ではメールアカウントの個数が変動することはほとんどないことなので、許容しています。

~/.getmail/rc-ryu

.. code-block:: txt

    [retriever]
    type = SimplePOP3SSLRetriever
    server = pop3.example.com
    username = ryu@example.com

    # SpamAssassinでのスパム判定を行います。
    [filter]
    type = Filter_external
    path = /usr/local/bin/spamassassin

    # 一時的な保存先として、~/.getmail/tmp/下に置いておくようにしています。
    [destination]
    type = Maildir
    path = ~/.getmail/tmp/ryu/

    # リモートのメールは取得後すぐ消す設定にしてます。
    # SpamAssassinでのエラーの可能性を考えると、数日間残す設定のほうが良いのかもしれません。
    [options]
    delete = True
    message_log = ~/.getmail/log

また、securityコマンドを使用して、キーチェーンにパスワードを設定しておく必要があります。

.. code-block:: txt

    security -i -p 'enter password' add-internet-password -a 'ryu@example.com' -s 'pop3.example.com' -r 'pop3'

SpamAssassin & Razor2
~~~~~~~~~~~~~~~~~~~~~~

デフォルトだと、SpamAssassinは、positive判定をした場合にメールの本文を改変してしまいます。
これはgetmailにとって `よろしくない <http://comments.gmane.org/gmane.mail.getmail.user/1204>`_ 挙動のため、report_safeを0に設定して、ヘッダを挿入するだけにします。また、SUBJ_ILLEGAL_CHARSで8bitヘッダを許容するようにします。

また、 /etc/mail/spamassassin/local.cf を編集してRazor2を使用するようにします。

SpamAssassinのインストールと設定は、ソースコードに含まれるINSTALLや `wikiのインストールガイド <http://wiki.apache.org/spamassassin/SingleUserUnixInstall>`_ などを熟読しつつ設定します。 `Razor2の設定ガイド <https://wiki.apache.org/spamassassin/RazorSiteWide>`_ もあります。ちょっとめんどうですが、マニュアルをしっかり読めばできるはずです。-Dオプションをつけるとデバッグログが出力されるので、適宜挙動を確認しながら進めていくと良いと思います。

スパムの閾値は、デフォルトの5のまま運用していますが、ときどきスパムが4.xとスコアリングされてfalse negativeが生じます。頻度は低いので問題視していません。

launchd
~~~~~~~~

launchdを利用して、notmuch newコマンドを定期的に実行します。メールの受信や、その他の前後処理は、notmuchのフック機能を介して実行されます。

launchdからコマンドを実行するときには、bash_profileで設定している項目は反映されないため、注意が必要です。
必要な環境変数は、plistの中で定義しましょう。

notmuchの全文検索エンジンであるxapianに日本語を正しく処理させるために、XAPIAN_CJK_NGRAMを設定する必要があります。
これをしないと日本語の検索ができないので注意しましょう。

MAIL_SOUNDとMAIL_FOLDERSは、自作スクリプトのための環境変数です。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>EnvironmentVariables</key>
        <dict>
            <key>XAPIAN_CJK_NGRAM</key>
            <string>1</string>
            <key>TERMINAL_NOTIFIER</key>
            <string>/Users/tai2/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier</string>
            <key>MAIL_SOUND</key>
            <string>Hero</string>
            <key>MAIL_FOLDERS</key>
            <string>ryu ken guile zangief</string>
        </dict>
        <key>Label</key>
        <string>net.tai2.notmuch</string>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/local/bin/notmuch</string>
            <string>new</string>
        </array>
        <key>StartInterval</key>
        <integer>180</integer>
    </dict>
    </plist>

データ移行
===========

Mail.appからエクスポートしたmboxファイルがあったため、Maildir形式に変更する必要がありました。
検索すると、mb2mdというような名前でいくつかのプログラムが出てくるのですが、なぜかどれも手元では動作しません。
しかたがないので、 `Pythonでスクリプトを書いて <https://gist.github.com/tai2/0d4e8ea30dc7a97850bf>`_ データ移行しました。

Sparrowは、データをエクスポートするための機能を備えていません。
ドラッグ&ドロップでファイル化できるので、手作業ですべて選択してファイル化し、Maildirにつっこみました。[ref]実際には、ファイル名の規則が他と違ってしまい、なにか気持ち悪いので、Maildirの命名規則に合わせてリネームするスクリプトを書きました。そのままでも実用上は問題ないと思います。[/ref]

今後の改善
============

muttの操作性を改善するためにパッチを当ててみたり、あるいは別のMUAも検討してみたいと考えています。その場合にも、UNIX哲学のメリットを活かして、MUAのみ差し替えて残りはなるべくそのままの構成でできればなと、ぼんやり考えています。

また、SpamAssassinが重いので、代替のスパムフィルターに変更することも検討しています。いまのところの候補は、 `POPFile <http://getpopfile.org/>`_ です。

当面は、このまま運用して様子を見ます。
