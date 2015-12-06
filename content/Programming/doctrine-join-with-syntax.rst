DQLのJOIN WITH構文を使えば、無用な関係を定義せずにテーブルの結合ができる
##########################################################################

:date: 2015-12-07
:slug: doctrine-join-with-syntax
:tags: php, symfony, doctrine, dql
:summary: DQLでクエリを書く際に、JOIN WITH構文を使用することで、@OneToManyアノテーションなどで関係するプロパティを定義せずとも、関係するエンティティを結合して絞り込みをかけることができる。

`Symfony Advent Calendar 2015 <http://qiita.com/advent-calendar/2015/symfony>`_ 7日目。

要約
=====

Doctrine 2.4以降では:

* DQLでクエリを書く際に、
* JOIN WITH構文を使用することで、
* @OneToManyアノテーションなどで関係するプロパティを定義せずとも、
* 関係するエンティティを結合して絞り込みをかけることができる。

前提
=====

JOINをしたいが、エンティティ間の関係を定義するほどではない。あるいは、プロジェクトのポリシーで、所与のもの以外には、@OneToManyなどの対多関係を追加しないということになっている。

例題
=====

以下の、ブログポストへのタグ付けを意図した多対多の関係を考える。

postテーブル

================================== ==================================
id                                 title
================================== ==================================
1                                  Symfonyのルーティング
2                                  Symfonyで知っておくと便利なconfig
================================== ==================================

tagテーブル

======== ========
id       name   
======== ========
1        symfony
2        routing
======== ========

post_tagテーブル

======== ========
post_id  tag_id 
======== ========
1        1
1        2
2        1
======== ========

ここで、

1. 「symfony」タグが付与された全ポストを取得したい。あるいは、
2. 「Symfonyのルーティング」に付随する全タグを取得したい。

通常のJOIN構文
===============

Doctrineにおける一般的な方法では、以下のように、@OneToMay,@ManyToOneという関係を定義するための機能を利用する。

.. code-block:: php

    <?php
    /**
     * @ORM\Entity
     */
    class Post
    {
        /**
         + @ORM\Column(type="integer")
         + @ORM\Id
         + @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;

        /**
         + @ORM\OneToMany(targetEntity="PostTag", mappedBy="post")
         */
        protected $post_tags;

        public function __construct() {
            $this->post_tags = new ArrayCollection();
        }

        ...
    }

    /**
     * @ORM\Entity
     */
    class Tag
    {
        /**
         + @ORM\Column(type="integer")
         + @ORM\Id
         + @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;

        /**
         + @ORM\OneToMany(targetEntity="PostTag", mappedBy="tag")
         */
        protected $post_tags;

        public function __construct() {
            $this->post_tags = new ArrayCollection();
        }

        ...
    }

    /**
     * @ORM\Entity
     * @ORM\Table(
     * indexes={
     *     @ORM\Index(name="post_idx", columns={"post_id"}),
     *     @ORM\Index(name="tag_idx", columns={"tag_id"})
     * },
     * )
     */
    class PostTag
    {
        /**
         * @ORM\Column(type="integer")
         * @ORM\Id
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;

        /**
         * @ORM\ManyToOne(targetEntity="Post", inversedBy="post_tags")
         */
        protected $post;

        /**
         * @ORM\ManyToOne(targetEntity="Tag", inversedBy="post_tags")
         */
        protected $tag;

        ...
    }

すると、以下のようにDQLのJOIN機能を使用してエンティティを取得できる。

.. code-block:: php

    <?php
    $em = $this->getContainer()->get('doctrine')->getManager();

    $posts = $em->createQuery(
        'SELECT p FROM AppBundle:Post p ' .
        'JOIN p.post_tags pt ' .
        'JOIN pt.tag t ' .
        'WHERE t.id = :tag_id')
        ->setParameter('tag_id', 1)
        ->getResult();

    $tags = $em->createQuery(
        'SELECT t FROM AppBundle:Tag t ' .
        'JOIN t.post_tags pt ' .
        'JOIN pt.post p ' .
        'WHERE p.id = :post_id')
        ->setParameter('post_id', 1)
        ->getResult();

しかし、JOINを利用するためだけに@OneToManyによる関係プロパティを追加するのは、過剰な場合がある。

Native SQL
===========

Native SQLを使用すれば、SQLのクエリ結果のカラムをエンティティにマップすることができる。

.. code-block:: php

    <?php
    /**
     * @ORM\Entity
     */
    class Post
    {
        /**
         * @ORM\Column(type="integer")
         * @ORM\Id
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;

        ...
    }

    /**
     * @ORM\Entity
     */
    class Tag
    {
        /**
         * @ORM\Column(type="integer")
         * @ORM\Id
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;

        ...
    }

    /**
     * @ORM\Entity
     * @ORM\Table(
     * indexes={
     *     @ORM\Index(name="post_idx", columns={"post_id"}),
     *     @ORM\Index(name="tag_idx", columns={"tag_id"})
     * },
     * )
     */
    class PostTag
    {
        /**
         * @ORM\Column(type="integer")
         * @ORM\Id
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;

        /**
         * @ORM\Column(type="integer")
         */
        protected $post_id;

        /**
         * @ORM\Column(type="integer")
         */
        protected $tag_id;

        ...
    }

このように@OneToMany等による関係プロパティのないエンティティ定義でも、Native SQLを使用することで、SQLの結果を直接エンティティにマッピングできる。

.. code-block:: php

    <?php
    $em = $this->getContainer()->get('doctrine')->getManager();

    $rsm = new ResultSetMappingBuilder($em);
    $rsm->addRootEntityFromClassMetadata('AppBundle:Post', 'p');
    $posts = $em->createNativeQuery(
        'SELECT p.id, p.title FROM post AS p ' .
        'JOIN post_tag AS pt ON pt.post_id = p.id ' .
        'JOIN tag AS t ON t.id = pt.tag_id ' .
        'WHERE t.id = :tag_id', $rsm)
        ->setParameter('tag_id', 1)
        ->getResult();

    $rsm = new ResultSetMappingBuilder($em);
    $rsm->addRootEntityFromClassMetadata('AppBundle:Tag', 't');
    $tags = $em->createNativeQuery(
        'SELECT t.id, t.name FROM tag AS t ' .
        'JOIN post_tag AS pt ON pt.tag_id = t.id ' .
        'JOIN post AS p ON p.id = pt.post_id ' .
        'WHERE p.id = :post_id', $rsm)
        ->setParameter('post_id', 1)
        ->getResult();

SQLを直接使えるため強力ではあるが、低級な部分が剥き出しになるため、やや醜い。

JOIN WITH構文
===============

上記と同様のエンティティ定義でも、JOIN WITH構文を使用すれば、Native SQLを使わずに同様のクエリを実現できる。

.. code-block:: php

    <?php
    $em = $this->getContainer()->get('doctrine')->getManager();

    $posts = $em->createQuery(
        'SELECT p FROM AppBundle:Post p ' .
        'JOIN AppBundle:PostTag pt WITH pt.post_id = p.id ' .
        'JOIN AppBundle:Tag t WITH t.id = pt.tag_id ' .
        'WHERE t.id = :tag_id')
        ->setParameter('tag_id', 1)
        ->getResult();

    $tags = $em->createQuery(
        'SELECT t FROM AppBundle:Tag t ' .
        'JOIN AppBundle:PostTag pt WITH pt.tag_id = t.id ' .
        'JOIN AppBundle:Post p WITH p.id = pt.post_id ' .
        'WHERE p.id = :post_id')
        ->setParameter('post_id', 1)
        ->getResult();

ただし、@OneToManyで関係を定義した場合には、外部キー制約が付与されるのに対して、
Native SQLの説明で用いたEntity定義では、外部キー制約がないため、厳密に同一ではない。
筆者の調べた限り、Doctrineで、@OneToMany等での関係プロパティ定義をせずに外部キー制約をつける方法はなさそうだ。

