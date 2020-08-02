title: Node.jsで文芸的プログラミング
date: 2017-12-19
slug: literate-programming

この記事は [Node.js 2 Advent Calender](https://qiita.com/advent-calendar/2017/nodejs2) の 19日目の記事です。

みなさんは[文芸的プログラミング](https://en.wikipedia.org/wiki/Literate_programming)というものをご存知でしょうか。
筆者はよく知らないのですが、プログラミングの神様ドナルド・クヌース先生が編み出したプログラミング技法で、
文芸的プログラミングで書かれた[TeX](https://www.amazon.co.jp/gp/product/020113439X/)のソースコードが出版されたりもしています。

いろいろなプログラマのエッセイなどを読むと、しばしば文芸的プログラミングに言及していたりするので、
いったいどんなものなのか以前から興味を持ってはいました。
そんな折、いつものように開発中のプログラムに必要な機能を満たしてくれるJavaScriptのライブラリをGoogleで検索していると、偶然、Node.jsで文芸的プログラミングをするためのプログラムにいき当たったのです。
いい機会なので、文芸的プログラミングというやつを、実際に体験してやろう。
そうして筆を取ったのが、この記事というわけです。

実は、はじめはNode.jsで作られた文芸的プログラミングの処理系を使ってみるという記事にする
予定だったのですが、調べてみると、文芸的プログラミングの処理系というのは、
各言語で[星の数ほど](https://github.com/search?utf8=%E2%9C%93&q=literate+programming&type=)作られていることが
わかってきました。考えてもみると、マークダウンをベースとした実装であれば、簡単なものなら自分でも作れそうです。

そこで、この記事では、Node.jsで文芸的プログラミングの簡単な処理系を実装します。
おもちゃの実装なので、[toylit](https://github.com/tai2/toylit)という名前にします。

なお、[この記事自体](https://github.com/tai2/blog/blob/master/content/Tech/literate-programming.md)が、toylitで処理できるソースコードになっています。
ですから、以下のように、このブログ記事をコンパイルすることで、「このブログ記事をコンパイルできるプログラム」を生成することができます。

```sh
$ wget https://raw.githubusercontent.com/tai2/blog/master/content/Tech/literate-programming.md
$ toylit literate-programming.md -o output1.js # このブログ記事をコンパイル
$ npm install yargs marked # 依存モジュールのインストール
$ node output1.js literate-programming. -o output2.js # このブログ記事をコンパイルした結果のプログラムに、このブログ記事を与える
$ diff output1.js output2.js && echo 'results are same'
results are same
```

## 仕様

プログラム言語の理屈に合わせてコードを記述するのでなく、
人間の思考に合わせてプログラムを記述できるというのが、文芸的プログラミングのエッセンスです。
文芸的プログラミングでは、人間にとって重要な高レベルな抽象の記述に集中し、
低レベルな詳細の記述を後回しにできます。

クヌースの実装した[CWEB](https://en.wikipedia.org/wiki/CWEB)という処理系では、
マクロと呼ばれる自然言語で表現された概念の下に、プログラムコードのチャンクを付随させます。
マクロの定義は、文中で後から追加していくことができます。
ソースコードからマクロを抽出・展開すると、プログラミング言語になります。

この記事では、ともかく最低限文芸的プログラミングと呼べなくもない何かができることを目標とするので、
高度な機能は実装しません。
文書をマークダウンとして記述し、見出しをマクロとした上で、見出しに付随するコードブロックを連結することで、
ソースコードを生成することにします。

* & ではじまる見出しをマクロとする
* &* ではじまる見出しをルートマクロ(プログラムのエントリポイントとする)
* ルートマクロは改行区切りでマクロを記述し、プログラムの構成順序を定義する
* マクロから、次のマクロ、またはファイル末尾までに現れるコードブロックをマクロに付随するコードチャンクとする
* マクロは文書中に複数回に渡って定義できる(記述順に結合される)

以上がこのプログラムの仕様です。
記号は、マークダウンの記法と衝突しないものを適当に選びました。

## &* 構成

プログラム全体は、以下のように構成されます。

```javascript
& モジュールのインポート
& 文字列ストリームクラス
& Streamから文字列への変換
& 入力の切り替え
& パーサー
& コマンドライン引数
& メイン関数
```

## コンパイルの流れ

Node.jsには、[marked](https://github.com/chjj/marked)という優れたマークダウンパーサーがあるので、
マークダウンの処理にはこれを利用します。
markd自体は、内部的にASTを持っておらず、パースをすると一気にHTMLに変換されますが、
マークダウンという形式は、階層のないフラットな形式なので、トークン列が得られれば十分です。

### & パーサー

```javascript
function compile (text) {
  const tokens = marked.lexer(text)
  const chunks = collectCode(tokens)
  return concatCode(chunks)
}
```

`compile`関数は、マークダウンテキストを受け取って、JavaScriptソースコードを返します。
まず、`marked`でトークン列に変換します。

    # Heading

    Sample text.

    ```javascript
    console.log('Hello World!')
    ```

このようなマークダウン文書をmarkedの`lexer`にかけると、

```json
[ { type: 'heading', depth: 1, text: 'Heading' },
  { type: 'paragraph', text: 'Sample text.' },
  { type: 'code',
    lang: 'javascript',
    text: 'console.log(\'Hello World!\')' },
  links: {} ]
```

このような配列が得られます。
`cllectCode`関数でこのJSONからプログラムコードの断片を抽出し、`concatCode`でそれらを結合します。

## コード断片の抽出

それでは、コードの抽出部分から実装していきましょう。
仕様に書いたように、特殊な記法で書かれた見出しをマクロとみなして、
マクロとマクロの間にあるコードブロックをすべて集めます。

### & パーサー

`collectCode`は、markedのlexerが解析したトークン列を受け取る関数です。

```javascript
function collectCode (tokens) {
```

まずは、収集したコード断片を格納するためのテーブルを用意します。

```javascript
  const chunks = {
    root: [],
    codeTable: {}
  }
```

`root`は、ルートマクロ専用で、`codeTable`は、見出しをキーに持つテーブルです。
ひとつのマクロに対応するコード断片が複数あっても良いので、要素は配列になります。

収集処理は、トークンを最初から順番に取り出しながら処理する状態機械で良さそうです。
状態は、3つ考えられます。開始直後の初期状態、ルートマクロを収集している状態、
その他のマクロを収集している状態です。

```javascript
  const STATE_INIT = 0
  const STATE_IN_ROOT = 1
  const STATE_IN_MACRO = 2
```

これらの状態を格納する変数を用意しましょう。

```javascript
  let state = STATE_INIT
```

また、現在収集中のマクロ名を保持しておくための変数も用意します。
`chunks.codeTable`のキーとして使います。

```javascript
  let subject = ''
```

変数の準備ができたので、状態機械のループを実装します。

見出しトークンが来た場合は、`isRootMacro`、 `isMacro`を使って、それらがマクロかどうかを判定した上で、状態を変化させます。
非ルートマクロの場合は、初回の出現時のみ`codeTable`のエントリを空配列で初期化します。

```javascript
  for (const token of tokens) {
    if (token.type === 'heading') {
      if (isRootMacro(token.text)) {
        state = STATE_IN_ROOT
      } else if (isMacro(token.text)) {
        state = STATE_IN_MACRO
        subject = extractSubject(token.text)
        if (!chunks.codeTable[subject]) {
          chunks.codeTable[subject] = []
        }
      }
```

コードブロックトークンの場合は、ルートマクロ走査中なら`chunks.root`に、
非ルートマクロ処理中なら`chunks.codeTable`にコード断片を追加します。

また、この処理系で扱うのはJavaScriptのソースコードのみとします。

```javascript
    } else if (token.type === 'code' && token.lang === 'javascript') {
      if (state === STATE_IN_ROOT) {
        chunks.root.push(token.text)
      } else if (state === STATE_IN_MACRO) {
        chunks.codeTable[subject].push(token.text)
      }
    }
  }
```

ループが終了すると、chunksには必要なコード断片が詰め込まれているので、返値として返します。

```javascript
  return chunks
}
```

見出しがマクロかどうかの判定、およびマクロから記号を取り除いたテキストの抽出は、簡単な正規表現で行えます。

```javascript
function isRootMacro (text) {
  return /^&\*.+$/.test(text)
}

function isMacro (text) {
  return /^&[^*]+$/.test(text)
}

function extractSubject (text) {
  return /^&([^*]+)$/.exec(text)[1].trim()
}
```

## コード断片の結合

ここまででコード断片の抽出ができたので、次はそれらを結合します。

### & パーサー

ルートマクロには特殊なチャンクが含まれます。
このチャンクは、改行区切りのフォーマットで、各行にはマクロが含まれています。
プログラムチャンクは、ルートマクロに書かれている順序で結合されます。

`parseRootChunk`では、ルートマクロの内容を受け取って、
記号を取り除いた見出し文字列の配列を返します。

```javascript
function parseRootChunk (text) {
  return text
    .split('\n')
    .filter(isMacro)
    .map(extractSubject)
}
```

`concatCode`は、`collectCode`で収集した`chunk`オブジェクトを受け取って、
ソースコード文字列を返します。
上で定義した`parseRootChunk`でまずはルートマクロを解析し、
そこで得られた順序に従って、マクロのコードチャンクを結合していきます。

```javascript
function concatCode (chunks) {
  const subjects = parseRootChunk(chunks.root.join('\n'))

  return subjects.reduce((acc, subject) => {
    const code = chunks.codeTable[subject].join('\n')
    return acc + code + '\n'
  }, '')
}
```

## CLIの実装

ここまでで本質的な処理は実装できました。
あとは、これを使ってCLIのプログラムを仕立てるだけです。

### 仕様の検討

このプログラムは、本質的にテキストからテキストへの変換なので、
典型的なUNIXのフィルタプログラムとして使えるようにしたいです。

そのため、最低限、標準入力からデータを受け取って、標準出力に書き出せる必要があります。

また、入力ファイル名が指定された場合は、標準入力ではなくファイルを入力とします。
入力ファイルは複数指定可能で、catのように指定された順番で結合して出力されます。

同様に、`--output`で出力ファイル名が指定された場合は、ファイルを出力先とします。

おまけとして、`--exec`が指定された場合は、コードを書き出すのではなく、その場で実行します。
この機能は、単に、筆者が「実行可能なマークダウン」というパワーワードを使いたかっただけです。

ブログ記事のためのおもちゃプログラムにしては過度な機能に聞こえるかもしれませんが、
Node.jsで、これらの異なる入出力を一般化して簡潔に書くことができるかやってみたかった
だけなので、これで良いのです。

### & メイン関数

プログラムのエントリーポイントを以下で定義していきます。

main関数は、`async`関数とします。

```javascript
async function main () {
```

なぜかと言えば、Node.jsでは、標準入力とファイル入力を統一的に扱うには
[Stream API](https://nodejs.org/dist/latest-v9.x/docs/api/stream.html)を使う他なく、
Stream APIはコールバックベースのインターフェースであるため、
逐次的に読み易く書くには、`Promise`でラップした上で[async](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)/[await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)を使うしかないからです。

出力先は、コマンドライン引数に応じて変化させます。詳細は後述。

```javascript
  const argv = getArgv()

  const output = getOutput(argv)
```

そして、ファイル名が与えられたか否かに応じて入力を切り替えてコンパイルを実行します。

```javascript
  if (argv._.length === 0) {
    await runCompile(process.stdin, output)
  } else {
    for (const static of argv._) {
      const input = fs.createReadStream(static)
      await runCompile(input, output)
    }
  }
```

標準入力とファイル入力を統一的に扱うことで`runCompile`の分岐を無くす(後の枝のみに統一)ことも考えましたが、
その場合、単純にやると全入力ファイルを一気にオープンする形になってしまいます。
開くファイルは一度にひとつとしたかったため、分岐は許容することにしました。

もちろん、ファイルのオープンを遅延評価にすれば、要件を満たしつつ統一することも可能ですが、
そこまでがんばる気分にはなりませんでした。

最後に、`exec`フラグが立っている場合は、抽出されたソースコードを`eval`で実行します。
`exec`の場合の`output`の出力先は文字列になっています。

```javascript
  if (argv.exec) {
    eval(output.toString()) // eslint-disable-line no-eval
  }
}
```

`runCompile`関数は、[Readable Stream](https://nodejs.org/dist/latest-v9.x/docs/api/stream.html#stream_readable_streams)
と[Writable Stream](https://nodejs.org/dist/latest-v9.x/docs/api/stream.html#stream_writable_streams)を引数に
取り、入力を変換した上で出力に流し込む関数です。

`readInput`が`Promise`を返すことによって、処理の流れが分断せずに読み易くなります。

```javascript
async function runCompile (input, output) {
  const text = await readInput(input)
  const code = compile(text)
  output.write(code)
}
```

メイン関数が定義できたので、それを実行します。

```javascript
main()
```

### & Streamから文字列への変換

Streamのデータを蓄積して文字列に変換する`readInput`を定義します。
やることは、受け取ったデータを配列に溜めておいて、`Buffer.concat`で結合するだけです。
`Promise`で包むことによって、使いやすいAPIになります。

```javascript
function readInput (stream) {
  return new Promise((resolve, reject) => {
    const chunks = []
    stream.on('data', chunk => chunks.push(chunk))
    stream.on('end', () => {
      resolve(Buffer.concat(chunks).toString('utf8'))
    })
    stream.on('error', err => {
      reject(err)
    })
  })
}
```

### & 入力の切り替え

与えられたコマンドライン引数に応じて、出力先を切り替えます。
`--exec`が与えられた場合は、後述する`StringWritable`によって、
いったんメモリ内にコード文字列を蓄積します。

```javascript
function getOutput (argv) {
  if (argv.exec) {
    return new StringWritable()
  } else if (argv.output) {
    return fs.createWriteStream(argv.output)
  } else {
    return process.stdout
  }
}
```

### & 文字列ストリームクラス

各入力ファイルに対応するプログラムコードを蓄積した上で`eval`にかけたいので、
そのための場所として`StringWritable`クラスを定義します。
`Writable`を実装することで、ファイル出力や標準出力との統一的な扱いを実現しています。

```javascript
class StringWritable extends Writable {
  constructor () {
    super()
    this.output = ''
  }
  _write (chunk, encoding, callback) {
    const str = encoding === 'buffer' ? chunk.toString('utf8') : chunk
    this.output += str
    callback()
  }
  toString () {
    return this.output
  }
}
```

### & コマンドライン引数

コマンドライン引数は、yargsを使ってオブジェクトに変換しています。
使えるフラグは、`--output`と`--exec`の2つのみです。
フラグなしのパラメータは、入力ファイルとして扱われます。

```javascript
function getArgv () {
  return require('yargs')
    .usage('Usage: $0 [-i static] [-o static]')
    .option('output', {
      alias: 'o',
      describe: 'output path. standard output when omitted.'
    })
    .option('exec', {
      alias: 'e',
      boolean: true,
      describe: 'execute program.'
    }).argv
}
```

## & モジュールのインポート

このプログラムでは、以下のモジュールを使用しています。

```javascript
const fs = require('fs')
const { Writable } = require('stream')
const marked = require('marked')
```

## 感想

* 自然と饒舌になる。
* 処理系の能力不足で書き味が制限される面があった。本格的にやるのであれば、マクロをもっと高機能にする必要がある。
* 文芸的プログラミングめんどくさい。

