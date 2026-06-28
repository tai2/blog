I built aco (Appium Command-line Operator), a tool for operating Appium from the CLI
====================================================================================

:date: 2026-6-28
:slug: aco-appium-command-line-operator
:summary: Page source in mobile automation is fundamentally different from web page source, and it comes with various difficulties
:lang: en

While building a mobile test execution system (Appium-based) at work, I frequently want to experiment with and verify the behavior of Appium or the AUT (application under test). `Exploring how to swipe in order to achieve a stable amount of scrolling <https://github.com/tai2/appium-meetup-tokyo-2-swipe-experiment>`_, investigating the differences in startup time across simulator versions, checking what accessibility IDs are available on a particular screen, and so on and so forth.

Appium is a client-server architecture system, so to use it you first have to start up the server. To do that, you also need to `install Appium and the necessary drivers <https://appium.io/docs/en/latest/quickstart/install/>`_ (and, going further, Node.js as a prerequisite, as well as setting up Xcode and Android Studio). Well, that's fine. Next is the client side, where you typically write a script in some language to connect to the server and implement the automation steps. This becomes one hurdle. To establish an Appium session, you have to specify a group of parameters called capabilities, and if you can't write these correctly, you can't even get started in the first place. There's also a GUI client called `Appium Inspector <https://github.com/appium/appium-inspector>`_, but since it's just a simple wrapper around the protocol, it doesn't reduce the knowledge required to use it. You have to specify all of the capabilities by hand. These can, of course, be reused once you've got them established, but when all you want to do is run a tap or swipe on the app, having to start up the server and prepare a throwaway script every single time is still a pain.

So I built a command-line tool to make Appium as easy to use as humanly possible. Its name is aco (Appium Command-line Operator).

https://www.npmjs.com/package/@tai2/aco

How easy? You only have to specify the platform and the build file, and you can already start a session.

.. code-block:: bash

   aco session start --platform ios --app /tmp/MyApp.app

The key point is that it starts the server in the background and builds the capabilities appropriately for you, so you can get things running without knowing the exact format. And once the session has started, you can already send commands.

.. code-block:: bash

   aco tap --x 100 --y 200

Here's the second point. Session information is saved to a file, so you don't need to specify a session ID or anything like that. The most recently started session is automatically selected (if there are multiple sessions, you can also specify one via a parameter).

Since the main purpose is to try out various Appium features, I designed the commands comprehensively so that all of Appium's features can be accessed via the CLI, and I also provided an escape hatch to make that coverage complete. All of the extension commands specific to XCUITestDriver and UIAutomator2Driver can be accessed under the :code:`aco io` and :code:`aco android` subcommands as well. On top of that, I prepared several features that are convenient for operating the app from the CLI. For example, using :code:`aco elements`, you can list all of the labeled elements currently on the screen along with the selectors for accessing those elements.

.. code-block:: bash

   $ aco elements
   #0  android.widget.TextView  "VoicePost"
         selector: -android uiautomator:new UiSelector().text("VoicePost")
         rect: 32,101 183x54
   #1  android.view.ViewGroup  "Open settings"
         selector: accessibility id:Open settings
         rect: 1000,102 48x51
   #2  android.widget.TextView  ""
         selector: -android uiautomator:new UiSelector().text("")
         rect: 1000,102 48x51
   #3  android.view.ViewGroup  "Start recording"
         selector: accessibility id:Start recording
         rect: 350,378 380x380
   #4  android.widget.TextView  ""
         selector: -android uiautomator:new UiSelector().text("")
         rect: 431,455 218x225
   #5  android.widget.TextView  "00:00"
         selector: -android uiautomator:new UiSelector().text("00:00")
         rect: 473,880 121x64
   #6  android.view.ViewGroup  "Start recording"
         selector: accessibility id:Start recording
         rect: 331,984 419x120
   #7  android.widget.TextView  "Start recording"
         selector: -android uiautomator:new UiSelector().text("Start recording")
         rect: 435,1016 267x56

You can just pass the displayed selector directly to the :code:`--selector` parameter.

.. code-block:: bash

   aco tap --selector 'accessibility id:Start recording'

Also, by using the :code:`--xpath` parameter of the :code:`aco source` command, you can filter the page source with xpath.

.. code-block:: bash

   aco source --xpath '//XCUIElementTypeButton[@name="Login"]' 

I also built a plugin for Claude Code, so you can do mobile automation using Claude Code too. Once you install the plugin, you should be able to just describe in natural language what you want to automate, and it'll do it for you (probably… maybe…).

.. code-block:: bash

   claude plugin marketplace add tai2/aco
   claude plugin install aco@aco

I designed it on the assumption that the Appium server itself is installed in the user's own environment, and that aco simply makes use of it. Somehow it felt like people doing mobile automation might want to use what's already in their own environment as-is, and bundling the entire Appium server and driver set into aco and distributing them together seemed like it would be too big — but in terms of making setup even easier, it might be fine to include those as well (it's a few hundred MB, though…).

As you can tell from the commit log, I built the whole thing with Claude Code. If I'd had to write all of it from scratch myself, there's a chance I wouldn't have acted on the idea even after coming up with it, so being able to quickly turn an idea into something real — I think we've come into a good era.