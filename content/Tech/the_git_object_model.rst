Gitのオブジェクトモデル(The Git Object Model翻訳)
==================================================

:date: 2015-08-5
:slug: the_git_object_model
:tags: git
:summary: Git Community Bookから、1章2節のThe Git Object Modelを翻訳。ライセンスは、GPLv2。多くのGit解説本と違い、まずGitの内部モデル解説から入るという、おもしろい構成の本です。人によっては、このほうがわかり易いかもしれません。Gitは差分データを管理していると誤解されることがたまにありますが、それは誤りであるということがこれを読めばわかります。

`Git Community Book <http://schacon.github.io/gitbook/index.html>`_ から、1章2節の `The Git Object Model <http://schacon.github.io/gitbook/1_the_git_object_model.html>`_ を翻訳。ライセンスは、 `GPLv2 <https://github.com/schacon/gitbook/blob/master/COPYING>`_ 。

多くのGit解説本と違い、まずGitの内部モデル解説から入るという、おもしろい構成の本です。人によっては、このほうがわかり易いかもしれません。Gitは差分データを管理していると誤解されることがたまにありますが、それは誤りであるということがこれを読めばわかります。

SHA
----

プロジェクトの履歴を表すのに必要な情報は、いずれも、40桁の「オブジェクト名」で参照されるファイルに格納されている。オブジェクト名は、このような形をしている:

::

  6ff87c4664981e4397625791c8ea3bbb5f2279a3

このような40文字の文字列は、Gitのあらゆる場面で見られる。どの場面で出てくるものであれ、その名前は、オブジェクトの内容のSHA1ハッシュを取ることで求められる。SHA1ハッシュは、暗号学的なハッシュ関数である。この意味は、異なるオブジェクトで、同じ名前を持つものを見付けるのは、ほぼ不可能ということである。これにはいくつもの利点がある。とくに重要なのは:

* Gitは2つのオブジェクトが同一かどうかをすばやく決定できる。たんに名前を比べるだけで。
* オブジェクトの名前は、すべてのリポジトリで、同一の方法で計算されるので、2つのリポジトリに格納されている同一のコンテンツは、常に同じ名前になる。
* Gitはオブジェクト読み込み時にエラーを検出できる。オブジェクト名がコンテンツのSHA1ハッシュになっているかをチェックすれば良い。

オブジェクト
-------------

どのオブジェクトも、3つのものから構成される。 **型** と **サイズ** と **コンテンツ** である。サイズは、たんにコンテンツのサイズで、コンテンツはオブジェクトの型が何であるかに依存し、そして、4つの異なるオブジェクトの型がある: 「ブロブ」、「ツリー」、「コミット」、そして「タグ」である。

* 「ブロブ」は、ファイルデータを格納するために使われる。一般的に、これはひとつのファイルである。
* 「ツリー」は、基本的にはディレクトリのようなものである。これは、他のツリーやブロブを束ねたものを参照している(例えば、ファイルやサブディレクトリのように)。
* 「コミット」は、単一のツリーを指して、特定の時点でのプロジェクトの見たままの形をマークする。これは、その時点についてのメタ情報を含む。例えば、タイムスタンプ、最後のコミットに変更を加えた人、直前のコミット(群)へのポインタなど。
* 「タグ」は、特定のコミットに特別な印をつける手段である。これは、通常、いくつかのコミットを、特定のリリース(あるいはそれと似たようなもの)としてタグ付けするために使われる。

Gitのすべては、この4つの異なるオブジェクト型からなる構造を操作することにあると言っても過言ではない。これは、ある種、小規模な独自のファイルシステムである。このファイルシステムは、マシンのファイルシステムそのものの上に構築される。

SVNとの違い
-----------

重要なのは、これが、読者の慣れ親しんでいるかもしれない、ほとんどのSCMとは異なるということである。Subversion、CVS、Perface、Mercurialのような差分ストレージを使うすべてのシステムが該当する。これらは、あるコミットと次のコミットとの間の差分を格納する。Gitでは、このようなことはしない。Gitは、プロジェクト内のすべてのファイルの見たままの形のスナップショットを、コミットをするたびに、上記のツリー構造に格納する。これは、とても重要な考えかたで、Gitを使うときには理解すべきことだ。

ブロブオブジェクト
-------------------

ブロブは、一般的にファイルの内容を格納する。

.. figure:: {filename}/images/object-blob.png
   :alt: Object blob

`git show <https://www.kernel.org/pub/software/scm/git/docs/git-show.html>`_ を使えば、ブロブの内容を確認できる。ブロブのSHAがあるとして、このようにすればコンテンツを確認できる。

.. code-block:: bash

  $ git show 6ff87c4664
  
   Note that the only valid version of the GPL as far as this project
   is concerned is _this_ particular version of the license (ie v2, not
   v2.2 or v3.x or whatever), unless explicitly otherwise stated.
  ...


「ブロブ」オブジェクトは、バイナリデータのチャンク以外のなにものでもない。それ以外のものにはなにも言及しておらず、どんな属性も持っていない(ファイル名さえも)。

ブロブは、完全にデータによって定義されるので、ディレクトリツリーの中に、同一の内容を持つ2つのファイルがあれば(あるいはリポジトリの異なるバージョンでもいい)、それらは同じブロブオブジェクトを共有する。ブロブオブジェクトは、ディレクトリツリー内の位置とはまったく関係がなく、ファイル名を変更したとしても、ファイルが関連付けられたオブジェクトは変わらない。

ツリーオブジェクト
-------------------

ツリーは、シンプルなオブジェクトで、ブロブや他のツリーへのポインタを束ねたものだ。一般的に、ディレクトリやサブディレクトリの内容を表している。


.. figure:: {filename}/images/object-tree.png
   :alt: Tree Object

非常に多彩な機能を持つ `git show <https://www.kernel.org/pub/software/scm/git/docs/git-show.html>`_ を使って、ツリーオブジェクトの内容を確認することももちろんできるが、 `git ls-tree <http://www.kernel.org/pub/software/scm/git/docs/git-ls-tree.html>`_ ならもっと詳しいことがわかる。ツリーのSHAがあるとすると、このように内容を確認できる:

.. code-block:: bash

  $ git ls-tree fb3a8bdd0ce
  100644 blob 63c918c667fa005ff12ad89437f2fdc80926e21c    .gitignore
  100644 blob 5529b198e8d14decbe4ad99db3f7fb632de0439d    .mailmap
  100644 blob 6ff87c4664981e4397625791c8ea3bbb5f2279a3    COPYING
  040000 tree 2fb783e477100ce076f6bf57e4a6f026013dc745    Documentation
  100755 blob 3c0032cec592a765692234f1cba47dfdcc3a9200    GIT-VERSION-GEN
  100644 blob 289b046a443c0647624607d471289b2c7dcd470b    INSTALL
  100644 blob 4eb463797adc693dc168b926b6932ff53f17d0b1    Makefile
  100644 blob 548142c327a6790ff8821d67c2ee1eff7a656b52    README
  ...

見てわかるように、ツリーオブジェクトは、エントリーのリストを含んでおり、それぞれにモード、オブジェクト型、SHA1名、ファイル名があって、ファイル名でソートされている。これは、ひとつのディレクトリツリーの内容を表している。

ツリーから参照されるオブジェクトは、ブロブ(ファイルの内容を表す)か、または他のツリー(サブディレクトリの内容を表す)かもしれない。ツリーとブロブは、他のすべてのオブジェクトと同様に、それらの内容のSHA1ハッシュで参照される。2つのツリーが(再帰的にすべてのサブディレクトリについても)同一の内容を持つならば、かつその場合に限り、それらは同じSHA1名を持つ。これにより、Gitは、関連した2つのツリーオブジェクトの間の違いをすばやく判定することができる。オブジェクト名が同一のエントリーは無視できるためだ。

(注意: サブモジュールが存在する場合には、ツリーには、コミットもエントリーとして含まれるかもれない。 **サブモジュール** の節を見よ。)

すべてのファイルは、644か755のモードとなることに注意: Gitは、実際には、実行ビットしか見ない。

コミットオブジェクト
---------------------

「コミット」オブジェクトは、ツリーの物理的な状態と、そこにどうやって辿りつくのかの記述、及びその理由を結びつける。

.. figure:: {filename}/images/object-commit.png
   :alt: Commit Object

--pretty=rawオプションを `git show <https://www.kernel.org/pub/software/scm/git/docs/git-show.html>`_ または `git log <https://www.kernel.org/pub/software/scm/git/docs/git-log.html>`_ に与えて、好きなコミットの内容を見ることができる。

.. code-block:: bash

  $ git show -s --pretty=raw 2be7fcb476
  commit 2be7fcb4764f2dbcee52635b91fedb1b3dcf7ab4
  tree fb3a8bdd0ceddd019615af4d57a53f43d8cee2bf
  parent 257a84d9d02e90447b149af58b271c19405edb6a
  author Dave Watson <dwatson@mimvista.com> 1187576872 -0400
  committer Junio C Hamano <gitster@pobox.com> 1187591163 -0700
  
      Fix misspelling of 'suppress' in docs
  
      Signed-off-by: Junio C Hamano <gitster@pobox.com>

ここから、コミットの定義がわかる:

* **ツリー**: ツリーオブジェクトのSHA1名(以下で定義)。特定の時点でのディレクトリの内容を表す。
* **親(1つ以上)**: いくつかのコミットのSHA1名。これらは、プロジェクト履歴における直前のステップ(1つ以上)を表す。上の例は1つの親を持つ。マージコミットは、1つ以上の親を持つかもしれない。親のないコミットは、「ルート」コミットと呼ばれ、プロジェクトの最初のリビジョンを表す。どのプロジェクトも、すくなくとも1つのルートを持たなければならない。プロジェクトが複数のルートを持つこともあるが、これは普通ではない(し、良いアイデアとも言えない)。
* **著者**: この変更についての責任を持つ人の名前。日付もいっしょに。
* **コミッター**: 実際にコミットを作成した人の名前。作成された日付もいっしょに。これは著者とは違うかもしれない。例えば、著者はパッチを書き、メールでそれを他の人に送り、その人がパッチを使ってコミットをするといったことが考えられる。
* **コメント**: コミットについての説明。

コミット自体は、実際になにが変更されたのかについての情報をまったく含んでいないことに注意。すべての変更は、コミットから参照されるツリーの内容と親に関連付けられたツリーを比較することで計算される。とくに、Gitは、ファイル名の変更を明示的には記録しない。にも関わらず、同じファイルデータのパス変更があるときにはそれを検出して、リネームを提案する。(例えば、 `git diff <https://www.kernel.org/pub/software/scm/git/docs/git-diff.html>`_ の-Mオプションを見よ)

コミットは、通常、 `git commit <https://www.kernel.org/pub/software/scm/git/docs/git-commit.html>`_ によって作られる。これは、通常、現在のHEADを親とするコミットを作成し、そのツリーは、現在インデックスに格納されている内容から取得される。

オブジェクトモデル
-------------------

これまで3つの主要なオブジェクト型を見てきた(ブロブ、ツリー、コミット)ので、これらがどのようにまとめられるのか簡単に見てみよう。

次のようなディレクトリ構造を持つシンプルなプロジェクトがあるとする。

.. code-block:: bash

  $>tree
  .
  |-- README
  `-- lib
      |-- inc
      |   `-- tricks.rb
      `-- mylib.rb
  
  2 directories, 3 files

そして、これをGitリポジトリにコミットしたとすると、このように表される。

.. figure:: {filename}/images/objects-example.png
   :alt: Objects structure

(ルートを含めて)ディレクトリー毎に **ツリー** オブジェクトが、ファイル毎に **ブロブ** オブジェクトができたことがわかる。それから、 ルートを指している **コミット** オブジェクトがあるので、コミットされた時点でのプロジェクトのあるがままの形を追跡することができる。

タグオブジェクト
-----------------

.. figure:: {filename}/images/object-tag.png
   :alt: Tag Object

タグオブジェクトは、オブジェクトの名前(単に「オブジェクト」と呼ばれる)、オブジェクトの型、タグ名、タグを作成した人の名前(タガー)、そしてメッセージが含まれる。メッセージにはシグネチャが含まれることもある。これは `git cat-file <https://www.kernel.org/pub/software/scm/git/docs/git-cat-file.html>`_ を使えば見られる:

.. code-block:: bash

  $ git cat-file tag v1.5.0
  object 437b1b20df4b356c9342dac8d38849f24ef44f27
  type commit
  tag v1.5.0
  tagger Junio C Hamano <junkio@cox.net> 1171411200 +0000
  
  GIT 1.5.0
  -----BEGIN PGP SIGNATURE-----
  Version: GnuPG v1.4.6 (GNU/Linux)
  
  iD8DBQBF0lGqwMbZpPMRm5oRAuRiAJ9ohBLd7s2kqjkKlq1qqC57SbnmzQCdG4ui
  nLE/L9aUXdWeTFPron96DLA=
  =2E+0
  -----END PGP SIGNATURE-----


`git tag <https://www.kernel.org/pub/software/scm/git/docs/git-tag.html>`_ コマンドを見て、タグオブジェクトの作成と検証方法を学ぶこと。(`git tag <https://www.kernel.org/pub/software/scm/git/docs/git-tag.html>`_ は、「軽量タグ」を作成するためにも使われることに注意。これはタグオブジェクトとはぜんぜん違うもので、たんに"refs/tags/"ではじまる名前のものを参照するだけだ。)

