ffmpegをビジネスで利用したときに特許侵害になる可能性
####################################################

:date: 2014-07-2
:slug: mpegla_and_ffmpeg
:tags: ffmpeg, mpeg-la, patent
:summary: 主に仕事で、ffmpegやVLCのようなOSSを利用して、動画をデコードしたりエンコードすることがちょくちょくあるのですが、そういうのを使ったときにMEPG-LAの保有している特許プールに突っ込むことにならないのか、気になったのでこの際ハッキリさせておくことにしました。

.. image:: {filename}/images/ffmpeg-logo.png
   :align: center
   :alt: ffmpeg logo

主に仕事で、ffmpegやVLCのようなOSSを利用して、動画をデコードしたりエンコードすることがちょくちょくあるのですが、
そういうのを使ったときにMEPG-LAの保有している特許プールに突っ込むことにならないのか、気になったのでこの際ハッキリさせておくことにしました。

ffmpegの見解
=============

`MPEG-LA <http://www.mpegla.com/main/default.aspx>`_ は、Apple、Microsoft、Fujitsu、Sony等等等といった名立たる企業が名を連ねたLLCで、MPEG2コーデック、MPEG2-Systems、H264/AVC等、動画にまつわる多数の特許を保持しています。
当然、ffmpeg等を利用して動画をデコード・エンコードできる能力を備えたソフトウェアを提供するときにも、これらの特許が問題になってくる可能性があります。

ffmpeg自体はボランティアで開発されており、MPEG-LAにライセンス料を支払う収入源があるとは思えないにも関わらず、どうして活動を続けられているのか、よくよく考えてみると不思議です。
ffmpegは、特許に関して、次のような立場であることを `表明しています <https://www.ffmpeg.org/legal.html>`_ 。

 Q: Does FFmpeg use patented algorithms?

 A: We do not know, we are not lawyers so we are not qualified to answer this. 
 Also we have never read patents to implement any part of FFmpeg, so even if we were qualified we could not answer it as we do not know what is patented. 

つまり、具体的な特許の内容を把握していないので、特許侵害しているのかどうかは知らないという立場のようです。
実際、H264/AVCに関連する特許だけでも、`膨大な数 <http://www.mpegla.com/main/programs/avc/Documents/avc-att1.pdf>`_ になるので、ひとつひとつ精査するだけでもとんでもない労力がかかるだろうと思います。

 Q: Is it perfectly alright to incorporate the whole FFmpeg core into my own commercial product?

 A: You might have a problem here. There have been cases where companies have used FFmpeg in their products. These companies found out that once you start trying to make money from patented technologies, the owners of the patents will come after their licensing fees. Notably, MPEG LA is vigilant and diligent about collecting for MPEG-related technologies.

商業製品にffmpegを利用した場合、問題になる可能性があることを指摘しています。
また、過去にそういうケースがあったことをほのめかしてもいますが、具体的にどういう問題があったのかまでは、軽く調べた限り見付けられませんでした。

ffmpegのような非商業活動をしているところに対して特許権を主張しても、お金を取れないので放置されているということなんでしょうかね。ソースコードの頒布自体は特許の侵害にならないという議論もありますが、そのあたりは国によって状況が違うようです。例えソースコードの頒布が問題にならなかったとしても、ffmpegをバイナリとして配布している各種のディストリビューションはどうなるんだ、とか考えると、やはり潜在的な問題は深そうです。

商業製品で動画を扱いたい場合はどうするべきか
=============================================

いくつか考えられますが、H264をエンコード・デコードできればいいだけなら、OSの提供するAPIを利用すればいいでしょう。
この場合は、OSのベンダーがライセンス料をすでに払ってくれているので問題ないという認識です。
モバイルでは、iOSならAVFoundation、Androidは、4.1以降であればMediaCodecクラスが使えます。

あるいは、 `MainConcept <http://www.mainconcept.com/jp/products/sdks.html>`_ のようなMPEG-LAへのライセンス済みの商用ライブラリを使うという手もあります。これであれば、ffmpegでH264エンコードしようとした場合に発生するx264のGPL問題も回避することができます(詳しい値段は知りませんが、噂によるとけっこうお高いようです)。

もちろん、ffmpeg等を使用した上で、MPEG-LAとライセンスを結べば、そもそも問題は発生しません。
いろいろな契約形態があるようですので、くわしくはMPEG-LAに直接問い合わせるのがいいと思います。

あとは、研究開発・実証実験といった内部向けのデモでしか使わないようなソフトウェアであれば、そもそもこういったことは問題にはならないかもしれません。

参考記事
========

* `Think H.264 is Now Royalty-Free? Think Again – and the “Open Source” Defense is No Defense to MPEG <http://blog.sorensonmedia.com/2010/09/think-h-264-is-now-royalty-free-think-again-and-the-open-source-defense-is-no-defense-to-mpeg-la/>`_
* `Frequently Asked Questions about software patents <https://www.ffii.org/Frequently%20Asked%20Questions%20ab
  out%20software%20patents>`_

----

.. raw:: html

  <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br />この記事のライセンスは、<a href="http://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>とします。

