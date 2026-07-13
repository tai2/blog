Why Utility-first CSS (Tailwind CSS) Makes Sense, and a Short History of UI Development with CSS
################################################################################################

:date: 2024-03-14
:slug: utility-first-css
:summary: Techniques for writing CSS have evolved to develop UI components while overcoming cascading, CSS's Achilles' heel. With Tailwind CSS, you can concentrate on implementing components without being bothered by extraneous chores like naming child elements.
:lang: en
:translation: true

.. contents:: Table of Contents

A Short History of CSS
======================

The techniques for implementing an app's UI with CSS have gone through several shifts over the years.

Long ago, when CSS was still young, physical tags like the FONT element were regarded as bad from the standpoint of separation of concerns, and people began to encourage keeping content (HTML) and style (CSS) cleanly separated.
There, HTML was strictly a document, and content and appearance were kept in separate worlds, connected only through the interface of the CSS class selector.
And at that point there was not yet any real concern about how to manage CSS in large-scale service development.

As time passed, HTML came to describe increasingly complex subjects. Once modularity and maintainability became the concerns of CSS coders,
"methodologies" typified by BEM were invented and developed.
These were an effort to overcome the "flaw" of cascading, and at the same time they opened the road to reusing styles.

Then, once tools like React were invented — ways of describing HTML as a tree of UI components using JavaScript —
a new idea called CSS in JS was born.
In a world where every class is automatically guaranteed to be unique, the problem of managing specificity, the perennial headache of markup engineers, was wiped away,
and CSS's greatest problem — the absence of scope — was solved perfectly.
By now the ideas of separating content from style, and of reusing style, had faded, and it came to be taken for granted that HTML and CSS are written together as a single unit.

Finally, when Adam Wathan pointed out the contradiction inherent in the notion of separation of concerns in HTML/CSS and invented Tailwind CSS,
it won a certain following among frontend engineers of the UI-component era and spread.
The reusability of CSS classes was maximized, the dependency between HTML and content was now completely severed, and classes became entities independent of content.

SUIT CSS — A Naming-Convention-Based CSS Methodology
====================================================

When you write CSS naively, `rule collisions against a particular element happen all too easily. <https://www.phase2technology.com/blog/used-and-abused-css>`_
What's supposed to make styles apply nicely even when rules collide is cascading — the very thing CSS is named after — together with
specificity-based rule resolution… but this is extremely hard to control and often produces unexpected output.

So our predecessors tried to solve the problem by naming classes according to a consistent set of rules, so that rule collisions wouldn't occur in the first place.
Under this naming convention, a rule's selector is basically a single class, so specificity stays at 0-1-0.
That way you can skip the complex, hard-to-control rule-resolution mechanism of cascading.

Writing a `media object <https://www.stubbornella.org/2010/06/25/the-media-object-saves-hundreds-of-lines-of-code/>`_ in SUIT CSS looks like this:

.. raw:: html

    <iframe width="100%" height="400px" src="https://stackblitz.com/edit/media-object-suit-css?embed=1&file=src%2FMedia.css&view=editor"></iframe>

`Media object - SUIT CSS <https://stackblitz.com/edit/media-object-suit-css?file=src%2FMedia.css>`_
(My CSS coding may be clumsy, so please bear with me…)

`SUIT CSS <https://github.com/suitcss/suit/blob/master/doc/naming-conventions.md>`_ is one derivative of the naming-convention-based CSS methodologies typified by BEM.
It has notation for expressing UI state and is designed to be used for UI components.
It was devised by `Nicolas Gallagher <https://nicolasgallagher.com/>`_, the author of react-native-web.
There are many CSS methodologies, but ever since the mentor who taught me CSS design recommended it, I still use it whenever I write CSS in a non-modern environment like plain (non-React) projects.

This certainly does ease the most painful problem of writing large-scale UI in CSS. But it has its own problems.
It isn't obvious how you should split classes to apply styles to child elements within a component, and you often get stuck deciding.
Even though CSS is ideally supposed to be thought out independently of HTML (without depending on HTML), in practice you frequently have to write CSS while thinking about the HTML structure.
It's even common to write the structure in HTML first, assign classes to it, and only then fill in the style bodies.
And as you can see from the sample code above, after expressing the component's structure in the CSS world, you then express the corresponding structure again in the HTML world.
It's extremely redundant. Whenever you think about or write a component, this double effort always arises.

I've come to believe that, these days, implementation via a CSS methodology is best avoided unless it's absolutely necessary. This is based on real experience.
Having introduced a CSS methodology in several projects, I've found that for many programmers — especially backend engineers who aren't very interested in frontend technology —
using it correctly is difficult.
Ordinary programmers don't even know that cascading or specificity exist, and they simply don't understand why a CSS methodology is needed in the first place.
And a CSS methodology isn't some enforcing mechanism; it's nothing more than a coding convention.
So people easily stray from the methodology's basic principles of avoiding class collisions and keeping specificity constant.

Of course, I think you could take the time to teach people what these things mean and get them to understand. But as I'll explain below, these days
there's another way to solve the cascading problem more cleverly, without using a CSS methodology.

styled-components — CSS in JS
=============================

CSS in JS presupposes a mechanism for describing UI components with JS, such as React.
One of the representative modules is styled-components, which dynamically generates a JSX component and a unique class dedicated to that component
from CSS written inside a template literal.

Rewriting the earlier media object in styled-components looks like this:

.. raw:: html

    <iframe width="100%" height="400px" src="https://stackblitz.com/edit/media-object-styled-components?embed=1&file=src%2FMedia.tsx&view=editor"></iframe>

`Media object - styled-components <https://stackblitz.com/edit/media-object-styled-components?file=src%2FMedia.tsx>`_

The great thing about CSS in JS is that it generates unique class names mechanically, so style collisions never happen.
[ref]However, since styled-components also allows you to nest ordinary, non-auto-generated classes inside its declarations, collisions can occur in that case.[/ref]
This lets you apply styles unambiguously just by using it normally, which is a very big advance.
You no longer need to memorize the tedious rules of a methodology. You just need to know how to use the API, so anyone can use it without strain.

That said, there's one point about styled-components' API design that I really can't stand.
I've used styled-components in several projects too, but the more I use it, the more inconvenient I find it.
As you can see from the sample code above, in styled-components you must always create one React component in order to write a style.
As a result, for the single unit of component you actually want to build (here, the Media component),
you're forced to create many small components unnecessarily.
Of course, you also have to name each of them. This is quite a nuisance.
Having countless tiny components defined that merely carry a style but have no particular function or logical meaning is noise, and
having the style and the DOM structure defined in separate places also makes it hard to grasp at a glance what the rendered result will be.

Recently, with Meta releasing stylex, its in-house CSS in JS library, another school of CSS in JS — the so-called zero-runtime kind — seems to be getting attention.
It aims to minimize runtime processing by resolving style definitions at build time.
And because it's Atomic CSS, the CSS file size becomes very small too.
[ref]Atomic CSS is `known <https://sebastienlorber.com/atomic-css-in-js>`_ to produce smaller files than the traditional approach of writing multiple rules for a single class.[/ref]
In stylex, the one-to-one relationship of one component per style isn't enforced, but as the documentation `states, <https://stylexjs.com/docs/learn/thinking-in-stylex/#readability--maintainability-over-terseness>`_
it essentially decouples the DOM from styles and favors giving a chunk of style some meaningful name — so in that sense
I don't think it's fundamentally different from styled-components. This doesn't resolve the complaint I have about styled-components.

Tailwind CSS — Utility-first CSS
================================

A utility class in CSS is a class specialized to a single function; most of them have just one property.
For example, the SUIT CSS I introduced earlier also contains a `set of utility classes <https://github.com/suitcss/suit/blob/master/packages/utils-flex/lib/flex.css>`_. Here's one example.

.. code-block:: css

    .u-flex {
        display: flex !important;
    }

    .u-flexInline {
        display: inline-flex !important;
    }

    .u-flexRow {
        flex-direction: row !important;
    }

    .u-flexRowReverse {
        flex-direction: row-reverse !important;
    }



These are provided to supplement the parts that can't be fully expressed by components — or the fine details where forcing everything into components would be a stretch.
The reusability of something increases the smaller its responsibility is. A utility class, being specialized to a single responsibility,
can be said to be a class whose reusability is maximized.

Pushing this idea further, developing it into the notion of writing styles using only utility classes, is Utility-first CSS. And
among the CSS libraries that support Utility-first CSS, the one that currently enjoys the most support is Tailwind CSS.
Implementing the media object in Tailwind CSS looks like this:


.. raw:: html

    <iframe width="100%" height="400px" src="https://stackblitz.com/edit/media-object-tailwind?embed=1&file=src%2FMedia.tsx&view=editor"></iframe>

`Media object - Tailwind CSS <https://stackblitz.com/edit/media-object-tailwind?file=src%2FMedia.tsx>`_

This file contains nothing unnecessary beyond the Media component we actually want to build.
You don't have to think about what concept to group each inner element under, or what to name it.
You can get straight to and focus on what's needed to implement the appearance and behavior you want — the essence of implementing the component.
This is exactly why I consider Utility-first to be reasonable.

Also, as you can see from the flex utility example above, the majority of utility classes are Atomic as well.
Consequently, the CSS size naturally becomes compact. With Tailwind you can code fast, and pages load fast.
And of course there's zero runtime overhead.

As for size, Tailwind works by scanning the app's code and outputting only the classes that are referenced.
The simplicity of this mechanism is another thing I find wonderfully cool. You don't need any complex machinery like a bundler at all.
Since it isn't tied to any particular library such as React, you can even combine it with server-side templates in Rails if you want to.

One more thing I'd like you to note: in the SUIT CSS example, colors were specified individually on :code:`Media-button`, :code:`Media-date`, and :code:`Media-separator`, whereas
in the Tailwind example the color is specified once on the parent element and the child elements simply inherit it (the styled-components example is essentially the same).
Of course, in the SUIT CSS example too you could apply a class to the parent element and specify a common color there.
But in this example, the right side was described using the idea of grouping it into multiple rows (Media-row). Since the first and second rows have different colors, you can't
specify the color directly on Media-row. So do you make a modifier for Media-row? Or do you group them as Media-1stRow and Media-2ndRow?
Because naming is required, these non-essential dilemmas keep cropping up.
With Tailwind, since the date and the button are the same color, you can make the simple decision to specify the color on their parent element — there's no room for hesitation.
How comfortable that is.

Tailwind has other noteworthy points. One is that the values you can specify — for colors, sizes, and everything else — are limited.
This set of usable values can be specified in a config file. In effect, this means that using Tailwind automatically introduces design tokens,
resulting in a UI with a consistent tone and manner. Of course you can implement based on design tokens with any other method too, but
with Tailwind it happens forcibly, without you having to think about it.

As we've seen, Tailwind has its own class-naming system, so the learning curve is somewhat steep, and design tokens get introduced whether you like it or not —
so it can't be denied that, compared with SUIT CSS or styled-components, it's a fairly opinionated choice.
Also, in Tailwind the problem of class-name collisions from cascading actually isn't very well solved.
There is a setting to add a prefix to class names, so it can be mitigated to some extent, but unlike CSS in JS there's no mechanism that avoids collisions.
So caution is needed in situations where class-name collisions are a real concern, such as introducing it incrementally into an existing project.
But if it's a project you decided from the start to write entirely in Tailwind, there should be no worry about collisions.

In any case, once you're hooked, the comfort of the development experience that comes from its simplicity is guaranteed to become addictive.

Why Not Just Use Inline Styles?
-------------------------------

You might think that if you're going to write styles in Tailwind, you might as well write the styles directly in the style attribute.
But the style attribute has functional limitations. You can't write things like media queries, pseudo-classes, or animations.
Recently there seem to be libraries like `CSS Hooks <https://css-hooks.com/>`_ that extend the style attribute so you can write pseudo-classes and such,
but even so the range that can be extended is limited.
If a technology emerges in the future that gives the style attribute access to the full feature set of CSS, then at that point it might be fine to just use the style attribute.

Summary
=======

* Techniques for writing CSS have evolved to develop UI components while overcoming cascading, CSS's Achilles' heel.
* With Tailwind CSS, you can concentrate on implementing components without being bothered by extraneous chores like naming child elements.
* Tailwind recommended.

Timeline
========

+-----------------------+----------------------------------------------------------------------------------------+
| 1996/12/17            | `CSS 1 <https://www.w3.org/TR/2008/REC-CSS1-20080411/>`_                               |
+-----------------------+----------------------------------------------------------------------------------------+
| 1998/5/12             | `CSS 2 <https://www.w3.org/TR/2008/REC-CSS2-20080411/>`_                               |
+-----------------------+----------------------------------------------------------------------------------------+
| 2009/5/20             | `less 0.7.0 <https://rubygems.org/gems/less/versions/0.7.0>`_                          |
+-----------------------+----------------------------------------------------------------------------------------+
| 2010/9/22             | `sass 3.1.0.alpha.2 <https://rubygems.org/gems/sass/versions/3.1.0.alpha.2>`_          |
+-----------------------+----------------------------------------------------------------------------------------+
| 2013/7/18             | `Bootstrap 1.0.0 <https://github.com/twbs/bootstrap/releases/tag/v1.0.0>`_             |
+-----------------------+----------------------------------------------------------------------------------------+
| 2013/7/3              | `React 0.3.0 <https://github.com/facebook/react/releases/tag/v0.3.0>`_                 |
+-----------------------+----------------------------------------------------------------------------------------+
| 2013/10/16            | `BEM CORE 1.0.0 <https://github.com/bem/bem-core/releases/tag/v1.0.0>`_                |
+-----------------------+----------------------------------------------------------------------------------------+
| 2014/3/23             | `SUIT CSS 0.3.0 <https://www.npmjs.com/package/suitcss/v/0.3.0>`_                      |
+-----------------------+----------------------------------------------------------------------------------------+
| 2014/10/30            | `jss 0.2.0 <https://www.npmjs.com/package/jss/v/0.2.0>`_                               |
+-----------------------+----------------------------------------------------------------------------------------+
| 2015/2/12             | `atomizer 0.2.0 <https://www.npmjs.com/package/atomizer/v/0.2.0>`_                     |
+-----------------------+----------------------------------------------------------------------------------------+
| 2015/3/7              | `tachyons CSS 1.1.0 <https://www.npmjs.com/package/tachyons/v/1.1.0>`_                 |
+-----------------------+----------------------------------------------------------------------------------------+
| 2016/10/13            | `styled-components 1.0.0 <https://www.npmjs.com/package/styled-components/v/1.0.0>`_   |
+-----------------------+----------------------------------------------------------------------------------------+
| 2017/11/2             | `tailwindcss 0.1.0 <https://github.com/tailwindlabs/tailwindcss/releases/tag/v0.1.0>`_ |
+-----------------------+----------------------------------------------------------------------------------------+


Reference Links
===============

* `‘Why BEM?’ in a nutshell <https://blog.decaf.de/2015/06/24/why-bem-in-a-nutshell/>`_ Why you should use BEM. An explanation of the specificity problem.
* `MindBEMding – getting your head ’round BEM syntax <https://csswizardry.com/2013/01/mindbemding-getting-your-head-round-bem-syntax/>`_ Why you should use BEM. An explanation of BEM's readability.
* `About HTML semantics and front-end architecture <https://nicolasgallagher.com/about-html-semantics-front-end-architecture/>`_ SUIT CSS author Nicolas Gallagher's reflection on the role of classes in frontend development. Class names should not be named based on content, but should have names based on design patterns.
* `Challenging CSS Best Practices <https://www.smashingmagazine.com/2013/10/challenging-css-best-practices-atomic-approach/>`_ Describes the benefits of Atomic CSS as used at Yahoo!. A comparison with traditional semantic class naming.
* `Frequently Asked Questions | Atomizer <https://acss.io/frequently-asked-questions.html>`_ An FAQ on Atomic CSS. About the problems it solves — no specificity problems, smaller size, and so on. Much of it applies to Utility-first CSS too.
* `CSS Utility Classes and "Separation of Concerns" <https://adamwathan.me/css-utility-classes-and-separation-of-concerns/>`_ Unpacks the instability of describing components with a CSS methodology like BEM. If you push reusability to its limit, many of the classes named based on meaning end up vanishing before you know it. Explains the ideological background of Tailwind.
* `Building the New Facebook with React and Relay | Frank Yan <https://www.youtube.com/watch?v=9JZHodNR184>`_ Touches on the CSS weight reduction Facebook achieved by moving to Atomic CSS with Stylex. From 413KB to 74KB.
* `Cascade, specificity, and inheritance <https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_and_inheritance>`_ Explains, with concrete examples, how cascading, specificity, and inheritance combine to form the actual appearance. If you use the methods explained in this article (the one you're reading), of these you'll barely have to be conscious of cascading and specificity.
* `Introducing the CSS Cascade <https://developer.mozilla.org/en-US/docs/Web/CSS/Cascade>`_ A detailed explanation of cascading.
* `Used and Abused – CSS Inheritance and Our Misuse of the Cascade <https://www.phase2technology.com/blog/used-and-abused-css>`_ An explanation of the concrete harm that cascading brings. Once multiple specificities are mixed together, when you touch a rule you can no longer predict where and what will happen.
* `HTML Standard <https://html.spec.whatwg.org/multipage/dom.html#classes>`_ The HTML standard encourages describing the nature of the content, not the appearance, with class names.
* `The media object saves hundreds of lines of code <https://www.stubbornella.org/2010/06/25/the-media-object-saves-hundreds-of-lines-of-code/>`_ The media object. A famous example demonstrating the effectiveness of class design that doesn't refer to the meaning of specific content.
* `CSS Zen Garden: The Beauty of CSS Design <https://csszengarden.com/>`_ An attempt to produce a variety of designs by changing only the stylesheet while keeping the HTML structure and CSS classes fixed. An intriguing example of using class names that carry meaning based on content. You can't do this with CSS in JS or Utility-first CSS.
