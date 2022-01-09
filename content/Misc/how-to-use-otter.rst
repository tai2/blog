Automatic note taking on Otter.ai
==================================

:date: 2022-1-9
:slug: how-to-use-otter
:summary: Otter.ai is a note-taking service, which generates text of speaking conversations through your audio devices in real-time.There are some ways to record meetings on Otter.ai. Some give you the best quality, and others require no extra cost depending on your facilities. I suggest three ways in this article.
:lang: en

Otter.ai is a note-taking service, which generates text of speaking conversations through your audio devices in real-time.

It greatly helps English learners like me to understand what others speak. You can read recorded text back to check what you missed during meetings. Of course, it's valuable enough to only take notes automatically as meeting logs.

Zoom's `live transcription <https://support.zoom.us/hc/en-us/articles/207279736-Managing-closed-captioning-and-live-transcription>`_ gives you a similar benefit, but you have to ask admins to enable it. On the other hand, you can use Otter.ai by yourself.

You can combine it with video conferencing tools like Zoom, Huddle, etc. I select Zoom as an example because I have recently used it. However, using other apps is not so different from Zoom.

There are some ways to record meetings on Otter.ai. Some give you the best quality, and others require no extra cost depending on your facilities. I suggest three ways in this article:

* Use no extra tools or devices
* Use Loopback and BlackHole on a single computer(macOS)
* Use another computer

Use no extra tools or devices
-------------------------------

.. figure:: {static}/images/how-to-use-otter/simplest-form.jpg
   :alt: The simplest form to record meetings on Otter.ai

   The simplest form to record meetings on Otter.ai

This is the fair simplest and maybe somewhat capable aproach than you think.

You use your standard microphone and speakers.
The speaking voices sounded from your speaker, including yours and other ones, come into your microphone, then they are put into Otter.ai. You don't use headphones to pick up all attendees' speaking.

.. figure:: {static}/images/how-to-use-otter/speakers-and-mic-on-zoom.png
   :alt: Just use your usual microphone and speakers.

   Just use your usual mic and speakers. I use the mic of my USB cam due to its quality.

.. figure:: {static}/images/how-to-use-otter/mic-for-browsers.png
   :alt: Set the same microphone to the system default

   Set the same microphone to the system default so your browser can use it.

This method often works well, maybe because of `the echo cancellation <https://support.zoom.us/hc/en-us/articles/115003279466-Using-and-preserving-original-sound-in-a-meeting>`_ of Zoom. Still, sometimes you are possibly bothered with echo.

If you would like to completely get rid of echo issues, you can use the other ways below.

Use Loopback and BlackHole on a single computer(macOS)
-------------------------------------------------------

.. figure:: {static}/images/how-to-use-otter/loopback-and-blackhole.jpg
   :alt: Internal routing using Loopback and BlackHole to record on Otter.ai

   Internal routing using Loopback and BlackHole to record on Otter.ai

You can route and mix any of your audio output streams into an audio input stream with the combination of Loopback and BlackHole. These two apps are provided only on macOS. You have to find similar software if you use other operating systems.

`BlackHole <https://github.com/ExistentialAudio/BlackHole>`_ is a virtual audio device that converts audio output into audio input. BlackHole redirect sounds an app plays on BlackHole to another app using BlackHole as input.

.. figure:: {static}/images/how-to-use-otter/blackhole-for-input.png
   :alt: Set BlackHole to the system default so your browser can process all required audio.

   Set BlackHole to the system default so your browser can process all required audio.

`Loopback <https://rogueamoeba.com/loopback/>`_ is an audio routing software that can take multiple audio output streams, mix them, and split them into multiple output streams. It works as a virtual audio device as well as BlackHole.

.. figure:: {static}/images/how-to-use-otter/loopback-config.png
   :alt: Send your mic and Zoom output to BlackHole and monitor only Zoom with your headphones.

   Send your mic and Zoom output to BlackHole and monitor only Zoom with your headphones.

Your voice flows to both Zoom and Loopback. Then the latter one is mixed with the output of Zoom on Loopback and ends up flowing to Otter.ai through BlackHole. The output of Zoom is also routed to your headphone for monitoring.

.. figure:: {static}/images/how-to-use-otter/specify-loopback-on-zoom.png
   :alt: Send the output of Zoom to Loopback. Your microphone is directly routed to Zoom.

   Send the output of Zoom to Loopback. Your microphone is directly routed to Zoom.

You can accordingly record your voice from your mic and others' voices from Zoom on Otter.ai without bothering about echo. Otter.ai converts those sounds into text.

This is the way I currently use to take meeting notes.

Use another computer and BlackHole
------------------------------------

.. figure:: {static}/images/how-to-use-otter/multiple-computers.jpg
   :alt: Use another computer to record meetings on Otter.ai

   Use another computer to record meetings on Otter.ai

Using two computers is an option if you have another computer and can use another account on remote meeting services. You join a meeting with one computer while taking a meeting note on Otter.ai with another computer.

It simply and perfectly works regardless of whether recording your voice or not. All you need are to send the output of Zoom to Otter.ai through BlackHole and hear sound with headphones to avoid echo. A pitfall of this is it requires extra physical space on your desk.

I haven't tried this method myself, but I believe it would work.
