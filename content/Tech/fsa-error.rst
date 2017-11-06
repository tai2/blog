Flux Standard Actionで失敗したアクションを識別する場合は、カスタムエラーオブジェクトを作れば良い
##################################################################################################

:date: 2017-9-26
:slug: fsa-error
:tags: redux, flux, fsa
:summary: ReduxなどのFluxアプリケーションの実装では、アクションのフォーマットとして、Flux Standard Action(FSA) を採用しているプロジェクトも多いと思います。 FSAを使って非同期アクションの結果を表現しようとしているときに、以下のような疑問を抱いたことはないでしょうか?

問題
=====

ReduxなどのFluxアプリケーションの実装では、アクションのフォーマットとして、 `Flux Standard Action(FSA) <https://github.com/acdlite/flux-standard-action>`_ を採用しているプロジェクトも多いと思います。
FSAを使って非同期アクションの結果を表現しようとしているときに、以下のような疑問を抱いたことはないでしょうか?

たとえば、TODOアイテムの更新をするアクションとして、:code:`UPDATE_TODO:REQUESTED`, :code:`UPDATE_TODO:RECEIVED` という2つのアクションがあるとします。これらは、それぞれHTTPリクエストとレスポンスに対応します。

.. code-block:: javascript

    // リクエスト
    {
        type: 'UPDATE_TODO:REQUESTED',
        payload: {
            id: 100,
            text: 'Do something!'
        }
    }

    // レスポンス
    {
        type: 'ADD_TODO:RECEIVED',
        payload: {
            id: 100,
            text: 'Do something!'
        }
    }

リクエスト成功時は、これで問題ありません。

では、エラーレスポンスが返ってきたときはどうなるでしょうか?
FSAにおいては、:code:`error` プロパティーが :code:`true` の場合、:code:`payload` はエラーオブジェクトであるべきと定められています。
JavaScriptのエラーオブジェクトは、 `Errorコンストラクタ <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error>`_ で表現されます。


.. code-block:: javascript

    {
        type: 'ADD_TODO:RECEIVED',
        payload: error, // error instanceof Error === true
        error: true
    }

問題は、複数のTODOの更新操作が並行して走る場合です。リクエストエラー時には、ユーザーに対して操作が完了しなかったことを通知したいでしょう。複数の更新操作が同時に走るのであれば、どのアイテムに対する操作が失敗したのかも示したほうが親切かもしれません。

しかし、この場合、:code:`payload` は :code:`Error` オブジェクトに占有されてしまっています。エラー時に、複数の操作を識別するためには、どうすれば良いでしょうか?

解法: カスタムエラーオブジェクトを作成する
===========================================

ひとつの方法として、カスタムエラーオブジェクトを作成することが考えられます。

.. code-block:: javascript

    class IdentifiableError extends Error {
        constructor(id, ...args) {
            super(...args)
            this.name = 'IdentifiableError'
            this.targetId = id
        }
    }

このように専用のエラークラスを定義し、リクエストエラー時には、このオブジェクトを :code:`payload` に格納します。
エラーオブジェクトの :code:`targetId` プロパティーを参照すれば、どの項目についての操作が失敗したのかを識別できます。
また、静的型環境での型付けも問題ありません。

別の解法1: エラー時専用のアクションを用意する
=============================================

アクションとして、:code:`UPDATE_TODO:REQUESTED` 、:code:`UPDATE_TODO:RECEIVED` の2種類ではなく、:code:`UPDATE_TODO:REQUESTED` 、:code:`UPDATE_TODO:SUCCEEDED` , :code:`UPDATE_TODO:FAILED` の3種類にします。
そして、FAILEDの場合には、:code:`error !== true` の通常のアクションとして、:code:`payload` に非エラーオブジェクトを乗せます。

別の解法2: metaに情報を持たせる
===============================

FSAでは、:code:`type` 、 :code:`payload` 、 :code:`error` 以外の第4のフィールドとして、:code:`meta` プロパティーを持つことが許されています。
:code:`meta` プロパティーにも :code:`payload` と同様に任意のオブジェクトを乗せられるため、これを使って解決することも可能です。
ただ、いまここで乗せたい識別情報は、:code:`meta` に乗せるような情報なのかは、判断が難しいところです。
更新対象のIDというのは、どちらかというと、ペイロードそのもののようにも思えます。

ミドルウェアで、アクションごとのユニークなIDを発行して、それをmetaに乗せて、TODOアイテムと関連付けた上でリクエストの状態を管理するというような、よりシステマチックで大掛りな方法も考えられるかもしれません。

参考リンク
===========

* `What is the reason error property is boolean? #17 <https://github.com/acdlite/flux-standard-action/issues/17>`_ FSAのリポジトリでこの問題について議論されています。
* `Custom JavaScript Errors in ES6 <https://medium.com/@xjamundx/custom-javascript-errors-in-es6-aa891b173f87>`_ カスタムエラーオブジェクトの作成方法が解説されています。
