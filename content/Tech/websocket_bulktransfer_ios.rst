WebSocketによるネイティブアプリ-WebView間でのストリーミングデータ送信実験
##########################################################################

:date: 2014-07-05
:slug: websocket-bulktransfer-ios
:tags: ios, websocket, webkit, experiment
:summary: モバイルネイティブアプリ側からWebViewへの動画(無圧縮RGB)データ転送の可能性を模索して、 XMLHttpRequestによる実験 を行いました。 XHRを用いた手法は、期待する速度が出ないことと、メモリが蓄積されていってアプリがクラッシュしてしまうことから 実用性がないことがわかったため、今度はWebSocketで同様の実験を行ってみました。

モバイルネイティブアプリ側からWebViewへの動画(無圧縮RGB)データ転送の可能性を模索して、
`XMLHttpRequestによる実験 <{filename}/Tech/xhr_bulktransfer_ios.rst>`_ を行いました。
XHRを用いた手法は、期待する速度が出ないことと、メモリが蓄積されていってアプリがクラッシュしてしまうことから
実用性がないことがわかったため、今度はWebSocketで同様の実験を行ってみました。

WebSocketでのストリーミング転送
====================================

iOSで、アプリ内にWebSocketサーバーを立てて、WebView内のWebSocketオブジェクトへの転送を行い、どの程度速度が出るか実験してみました。
コードは、githubに置いてあります: `WebSocketBulkTransferDemo_iOS <https://github.com/tai2/WebSocketBulkTransferDemo_iOS>`_

.. image:: {static}/images/websocket.png
   :align: center
   :alt: In-app web server to webview

条件は以下のような感じです。

* サーバーは、非ブロッキングソケット + イベント通知モデルで実装。
* WebSocketペイロードのサイズは1MB。
* ペイロードは、ArrayBufferとして受けとる。
* ソケット送信バッファサイズも1MB(XHRのときと同様)。
* ユーザーランドの送信バッファは10MB。
* 0.1秒間隔のコールバック内で、ユーザーランド送信バッファを適当なデータで一杯まで埋める。
* 送信可能イベント通知を利用して、ユーザーランド送信バッファからソケット送信バッファへデータ転送。

結果
=====

以下のようなことがわかりました。

* 第一世代iPad mini実機で、110Mbps程度。
* **メッセージのメモリが開放されずにアプリが落ちてしまう**

期待とは裏腹に、XHRよりも速度が出ませんでした(転送のしかたが悪い?)。
また、XHRのときと同様に、実機で実行するとWebView内で受信したデータが蓄積されていってしまい、最終的にアプリがクラッシュします。
jsコード内からのデータへの参照は、即座に解除されているはずなのですが、どうも実際の開放までに時間差があるようで、
開放される速度よりも受信する速度が上回った結果クラッシュしてしまっているような感じがします。

HTTPやWebSocketでモバイルWebViewに大量のストリーミングデータ転送を行うという手法は、現実的ではないようですね(すくなくとも現状のiOSでは)。

余談ですが、データ送信完了までその場で待ってくれる同期I/Oと比べると、送信可能なデータ量が未確定な非ブロッキングソケットは、プログラミングしづらいなと、改めて思いました。もちろん、イベントモデルにはレースコンディションを考えなくていいという素晴しい利点もあるのですが…。一長一短ですね。

