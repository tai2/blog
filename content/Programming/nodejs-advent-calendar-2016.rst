おすすめNodeSchool Workshopper 8選
####################################

:date: 2016-12-13
:slug: nodejs-advent-calendar-2016
:tags: programming, nodejs, nodeschool
:summary: 数あるワークショッパーの中から、おすすめのものを8つ紹介します。

この記事は、 `Node.js Advent Calendar 2016 <http://qiita.com/advent-calendar/2016/nodejs>`_ の13日目の記事です。

`数あるワークショッパー <https://nodeschool.io/#workshopper-list>`_ の中から、おすすめのものを8つ紹介します。

NodeSchool Workshopperとは
===============================

`公式サイトの説明 <https://nodeschool.io/ja/about.html>`_ を見てください。

NodeSchoolは、国内でも大阪・東京・福井などの都市で有志により開催されています。
開催情報は、 `東京Node学園のconnpass <https://nodejs.connpass.com/>`_ をチェックしてください。
今週末の12月17日には、 `NodeSchool Fukui <https://nodejs.connpass.com/event/46884/>`_ が、永和システムマネジメントで、来年1月29日に、 `NodeSchool Tokyo <https://nodejs.connpass.com/event/45720/>`_ がヒカリエで開催されるので、ぜひご参加を。

learnyounode
=============

NodeSchoolでもとくに人気のあるワークショッパーのひとつです。Node.jsの基本が学べます。
筆者自身もこれでNode.js入門しました。

* 日本語: あり
* 学べる内容:

  * コンソール出力
  * コマンドライン引数
  * ファイルI/O(同期・非同期)
  * ディレクトリ読み込み
  * モジュール(CommonJS)
  * HTTPクライアント
  * ストリーム
  * HTTPサーバー

javascripting
==============

JavaScriptの基本を学べます。
他の言語での経験はあるがJavaScriptはやったことがないという人や、プログラミング入門者向け。

* 日本語: あり
* 学べる内容:

  * 変数
  * 文字列
  * 数値
  * 条件分岐
  * ループ
  * 配列
  * オブジェクト
  * 関数

expressworks
=============

Node.jsでもっともポピュラーなWebアプリケーションフレームワークである、Expressの使い方を学べます。

* 日本語: あり
* 学べる内容:

  * Hello World
  * 静的ファイルの配信
  * Jadeによるテンプレートのレンダリング
  * Form値の取得
  * Stylusによる簡潔なスタイルシート
  * URLパラメータの使い方
  * クエリ文字列の使い方
  * JSONレスポンスの返しかた

how-to-npm
===========

npmで実際に自分のパッケージを公開してみるところまでを、順を追って学べます。

* 日本語: あり( `別パッケージ <https://github.com/nodeschool-ja/how-to-npm-jp>`_ [ref]watildeさんが本家に `プルリクエスト <https://github.com/nodeschool-ja/how-to-npm-jp/issues/21>`_ を出してくれてるので、いずれは統一されると思います[/ref])
* 学べる内容:

  * アカウント作成
  * プロジェクト初期化
  * モジュールの追加
  * 依存モジュールの表示
  * タスクランナー
  * 公開
  * バージョン(semver)
  * 配布タグ
  * 古くなったモジュールの確認と更新
  * モジュールの削除

git-it
=======

gitでのコミットのしかたから、実際にプルリクエストを出してマージされるまでを順を追って学べます。
マージされると、 `GitHubのリポジトリに <http://jlord.us/patchwork/>`_ 名前が載ります。

* 日本語: あり(ただし `Electron版 <https://github.com/jlord/git-it-electron>`_ のみ)
* 学べる内容:

  * 初期設定
  * コミット・状態確認・差分確認
  * GitHubアカウントの作成
  * リモートへのアップロード
  * フォーク
  * ブランチ
  * プルリクエスト
  * マージ

tower-of-babel
===============

babelを使って、ES6で導入されたJavaScriptの新しい機能について学べます。
会長ことyosuke_furukawaさんが作ったやつです。

* 日本語: あり
* 学べる内容:

  * クラス
  * 継承
  * モジュールの定義方法
  * ブロックスコープ
  * computed property(オブジェクトリテラルで動的にキーを定義する)
  * イテレーター
  * ジェネレーター
  * 分割代入
  * アロー関数
  * rest and spread

stream-adventure
=================

streamは、Node.jsでのデータ入出力を扱うための基本的なAPIで、まるでUNIXのパイプのように繋げて使うことができる便利なものです。
streamの基本的な使いかたや、さまざまな便利なライブラリについて学べます。

* 日本語: なし
* 学べる内容:

  * streamの繋げかた
  * through2(ストリームの変換)
  * split(改行での分割)
  * concat-stream(stream結合して一個の文字列に)
  * HTTPサーバーの実装
  * HTTPクライアントの実装
  * websocket-stream(WebSocket接続)
  * trumpet(HTMLのパース)
  * duplexer2(入力と出力をまとめて一つのstreamにする)
  * through2とduplexer2の応用
  * stream-combiner(複数のstreamの結合)
  * crypto(暗号化)
  * zlib(圧縮)

bug-clinic
===========

Node.jsでアプリ開発をする際のさまざまなデバッグツールの使い方を学べます。

* 日本語: なし
* 学べる内容:

  * consoleオブジェクト
  * jshintとeslint
  * bunyan(ロガー)
  * long stacktrace(非同期APIをまたがったスタックトレース)
  * tape(自動テスト)
  * NODE_DEBUG環境変数
  * jstrace(DTrace)
  * replpad/replify(動作中のアプリにREPLを仕込む)
  * debuggerステートメント(コード内にブレイクポイントを仕込む)
  * node-inspector(ChromeのDeveloper ToolsベースのNode用開発ツール)
  * heapdump(メモリ使用状況をダンプする)
  * gdb/lldb(C++レイヤーでのデバッグ)

----

.. raw:: html

  <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />この記事のライセンスは、<a href="http://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>とします。

