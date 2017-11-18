Puppeteerで記事タイトルからog:imageを生成する
#############################################

:date: 2017-11-18
:slug: puppeteer-ogimage

最近話題の `dev.to <https://dev.to>`_ で、og:imageを記事タイトルから生成しているのが良かったので、
このブログでも `記事タイトルからog:imageを生成するようにしました <https://github.com/tai2/blog/commit/3a433584b62598878e5b17d552675b5369eea9aa>`_ 。

dev.toのog:imageは、 `Cloudinary <https://cloudinary.com/features#manipulation>`_ という、
URLのクエリ文字列で画像処理をできるSaaSを使って動的に生成していますが、本記事ではこれとは別のアプローチを取ります。
`Pupeteer <https://github.com/GoogleChrome/puppeteer>`_ を使って自前で生成するというやりかたです。

Puppeteerとは
==============

`Headless Chrome <https://developers.google.com/web/updates/2017/04/headless-chrome>`_ を操作するためのNode.js用ライブラリです。`Selenium WebDriver <http://www.seleniumhq.org/>`_ と同じようなものですが、Chromeに特化していて、シンプルなAPIを持っているのが特徴です。npm installするだけでChromium[ref]Chromeのオープンソース版[/ref]もいっしょにダウンロードしてくれるので、お手軽に使いはじめられます。

方法
====

`og:image用に組んだHTML <https://github.com/tai2/blog/blob/d1cef7ddd6c8b1bfee089e207393b183fb5fcac2/ogimage.html>`_ をPuppeteerでレンダリングして、画像として保存します。

og:imageの生成とキャプチャは、以下のような非常に短かい関数で実現できます。
`exposeFunction` でChrome側に関数をエクスポートできるので、これを使って、HTML側に記事タイトルを注入します。

.. code-block:: javascript

    async function capture(article) {
        const viewport = {
            width: 1000,
            height: 500,
        }
        const injectedProps = {
            title: article.title,
        }
        const basename = path.basename(article.path, '.rst')

        const browser = await puppeteer.launch()
        const page = await browser.newPage()
        page.setViewport(viewport)

        // getInjectedPropsという関数を注入してプロパティーをHTMLに引き渡す
        await page.exposeFunction('getInjectedProps', () => injectedProps)

        await page.goto('file://' + path.resolve('ogimage.html'))
        await page.screenshot({path: `content/images/og/${basename}.png`})
        await browser.close()
    }

HTML側では、レンダリング結果が画像サイズをはみ出ないように、1ピクセルずつ小さくしながら最適なフォントサイズを探索します。

.. code-block:: javascript

    let fontSize = 100 // px dimension
    for (;;) {
        title.style.fontSize = fontSize + 'px'

        // レンダリング結果の高さがwindow.innerHeight(viewportの高さ)をはみ出さなければ探索停止
        if (document.body.clientHeight <= window.innerHeight) {
            break
        }

        fontSize -= 1
    }

なお、実装は、いったんPuppeteerとは切り離して単体のHTMLとしてデザインを完成させた上で、
あとからPuppeteerを組込むという工程で進めました。

評価
====

HTMLとCSSでレイアウトができるため、とても柔軟な表現が可能です。
Cloudinaryについては詳しくありませんが、おそらくは、それに勝る表現の柔軟性があるのではないでしょうか。

一方、処理時間については、 筆者の環境(MacBook Pro Core i7 3.1GHz)で画像1枚生成するのに、Nodeプロセスの起動から終了までで2秒程度かかります。
Puppeteerの起動から完了まででも1.5秒、スクリーンショットの保存だけで0.5秒といった感じです。

このブログは、 `Pelican <https://blog.getpelican.com/>`_ という静的サイトジェネレータで管理しています。
このツールでは、記事変換時に、常に全記事一気に変換されるため、記事変換にog:imageの生成を付随させると、
publishにかかる時間がかなり長くなってしまいます。
そのため、自動的なog:imageの生成は断念して、新規記事追加ごとに手動で画像生成する運用でいくことにしました。

実際のサービスなどに応用することを考えると、生成のタイミングは工夫する必要があるかもしれません。

