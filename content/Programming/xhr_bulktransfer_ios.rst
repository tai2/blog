XMLHttpRequestによるネイティブアプリ-WebView間でのストリーミングデータ送信実験
##############################################################################

:date: 2014-06-17
:slug: xhr-bulktransfer-ios
:tags: ios, xmlhttprequest, webkit, experiment
:summary: モバイルアプリ開発で、ネイティブコードから、WebView内のJavaScriptに大量のデータを高速に流し込めると、いろいろとうれしいことが考えられます(たとえば、ネイティブアプリで生成した映像を、非圧縮動画としてWebViewに転送して表示したりできるかもしれません)。これを実現できないか模索してみます。まずは、XMLHttpRequestでのデータ転送を検証してみました。
          
モバイルアプリ開発で、ネイティブコードから、WebView内のJavaScriptに大量のデータを高速に流し込めると、いろいろとうれしい
ことが考えられます(たとえば、ネイティブアプリで生成した映像を、非圧縮動画としてWebViewに転送して表示したりできるかもしれません)。

これを実現できないか模索してみます。まずは、XMLHttpRequestでのデータ転送を検証してみました。

WebViewとの通信手段
===================

モバイルアプリで、ネイティブコードとWebView内のJavaScriptが通信する方法には、以下のような仕組みなどがあります。

1. XMLHttpRequest
2. WebSocket
3. `Server-sent event <http://www.html5rocks.com/en/tutorials/eventsource/basics/>`_
4. `stringByEvaluatingJavaScriptFromString <https://developer.apple.com/library/ios/documentation/UIKit/Reference/UIWebView_Class/Reference/Reference.html>`_ (iOS)
5. `addJavascriptInterface <http://developer.android.com/reference/android/webkit/WebView.html>`_ (Android)

以下、簡単に各手法の特徴を述べます。

1は、HTTPで通信して、文字列の他にバイナリデータの転送もできます。アプリ内にWebサーバーを立てる必要があります。

2は、WebSocketプロトコルで通信します。ヘッダが小さく、リクエスト・レスポンスという制約もないので、HTTPよりも高速な通信が期待できます。任意の形式のデータ転送が可能です。アプリ内にWebSocketサーバーを立てる必要があります。

3は、HTTPで小さいデータをストリーミング配信できますが、データは文字列のみです。高速データ転送には向かないでしょう。

4は、iOSのWebView用APIで、ネイティブ側から、文字列を渡して、JavaScriptコードとして評価させることができます。毎回JavaScirptを評価させるので、データ転送には向かない気がします(試してはいません)。

5は、ネイティブ(Java)で実装したコードをWebViewにエクスポートするメカニズムですが、致命的な脆弱性があるため、Android 4.1以前を対象にしたアプリでは使えません。Android 4.2以降でよければ、もっともお手軽にデータ転送を実現できる仕組みだと思います。ただし、文字列型のデータしか受け渡せません。

単純に映像の転送という意味では、`HLS <http://en.wikipedia.org/wiki/HTTP_Live_Streaming>`_ を使って、videoタグで配信することも可能ですが、
H264でのエンコードをアプリ内で行う必要があるため、処理負荷的に、モバイルでリアルタイムで行うのは厳しい気がします。

XMLHttpRequestでのストリーミング転送
====================================

iOSで、アプリ内にWebサーバーを立てて、XMLHttpRequestでの転送を行って、どの程度速度が出るか実験してみました。
コードは、githubに置いてあります: `XHRBulkTransferDemo_iOS <https://github.com/tai2/XHRBulkTransferDemo_iOS>`_

.. image:: images/xhr.png
   :align: center
   :alt: In-app web server to webview

XMLHttpRequestでのストリーミング転送を行うにあたっては、いくつか考慮すべき点があります。

まず、1回のリクエストでデータ転送を行うと、メモリ上にすべてのデータを蓄積しなければならないため、ストリーミングには向きません。
したがって、データをチャンク化して、複数回のリクエストに分割して転送を行う必要があります。[ref]Gecko(Firefoxのエンジン)では、"moz-chunked-arraybuffer"などの拡張機能を使うことで、1回の転送を分割受信することもできるようなのですが、残念ながらWebKitには、同様の機能がいまのところはないようです。[/ref]

複数回のリクエストに分割した場合、これらを複数のTCPコネクションに分割してしまうと、TCPはスロースタート戦略で転送を行うことや、3-Wayハンドシェイクのオーバーヘッドがあるので、十分な速度がでないと考えられます。幸い、HTTP 1.1にはpersistent connection機能があるので、1つのコネクションに複数のリクエストを詰め込むことができます。XMLHttpRequestでpersistent connectionを使うには、ひとつのXHRインスタンスを使い回せばOKです。サーバーからのレスポンスには、Connection: keep-aliveヘッダを付加する必要があるようです。HTTP 1.1はデフォルトでpersistent connectionだと思っていたのですが、このヘッダを付加しないと毎回接続しなおしになってしまいました。persistent connectionを使うと使わないでは、2倍程度速度に差が出ました。

また、HTTP 1.1では、pipeliningという、レスポンスを待たずにリクエストをいくつも流し込める機能があります。数個から数十個程度まで、レスポンスを待たずにリクエストするということをやってみましたが、転送速度にはあまり差はありませんでした(これについては、正しいやりかたができてたのか、あまり自信がありません)。

結果
=====

さて、結果ですが、以下のようなことがわかりました。

* チャンクサイズを大きくするほど、転送速度が早くなる
* 第一世代iPad mini実機で、160Mbps程度(チャンクサイズ1MB)。
* **レスポンスのメモリが開放されずにアプリが落ちてしまう**
   
VGA 30fps生RGBで221Mbps必要であることを考えると、もうすこしで実用可能な速度に届きそうなのですが、いろいろ試しているうちに、レスポンスが開放されないという致命的な問題に気付きました。Instrumentsで見ると、レスポンスに使っているArrayBufferオブジェクトが開放されずにそのまま蓄積されていっています。
WebKitのコードを見ると、XMLHttpRequest::openしたときに開放処理(参照カウントのデクリメント)をしているのですが、メモリ上に残っているということは、他の部分からも参照されていて参照カウントが残っているのだと思います。

速度的には、チューニングをすれば、もう少し上げられそうな気がしていますが、この手法は使えなさそうなので、これ以上追求するのはやめました。
もしかすると、Androidでは、また違った結果になるかもしれません。

次は、`WebSocketで同様の実験 <{filename}websocket_bulktransfer_ios.rst>`_ をしてみようと思っています。
