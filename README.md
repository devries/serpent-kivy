Serpent Kivy Controller
=======================

This is a quick project to build a serpent controller using the Nexus 10
tablet. Kivy was chosen as a platform because it is device independent, and
yields rapid results, however it has shortcomings in that it can be a slow
driver for the Serpent. In the future an approach which makes use of the
BeagleBoard or is written in java may be a better fit.

Installation
------------
To install on any computer, follow the [Kivy installation
instructions](http://kivy.org/#download). Then run the `main.py` application
using the `kivy` command. 

Android Installation
--------------------
To create an android apk download the [Kivy Python for
Android](https://docs.google.com/uc?export=download&confirm=no_antivirus&id=0B1WO07-OL50_bTR0SElrLTZGWEU)
virual machine. You can run this virtual linux instance using
[VirtualBox](https://www.virtualbox.org/). 

You will need to install mercurial in the virtual machine, and clone the code
into the home directory. 

    $ sudo apt-get install mercurial
    $ hg clone https://bitbucket.org/devries/serpent-kivy

Next you will need to create a build environment:

    $ cd ~/android/python-for-android
    $ ./distribute.sh -m "openssl pil kivy"

Then create the apk from within the build environment:

    $ cd dist/default
    $ ./build.py --package com.idolstarastronomer.serpent --name serpent \
    --version 0.2 --dir ~/serpent-kivy --permission INTERNET debug

The apk is now in the `bin` subdirectory with the name
`serpent-0.2-debug.apk`. You can install this into an android device using the
command

    $ adb install bin/serpent-0.2-debug.apk

Alternative Android Installation
--------------------------------
You can avoid the build process, by installing the [Kivy Android
Launcher](https://market.android.com/details?id=org.kivy.pygame) from the play
store. Then you will have to copy the source directory to `/sdcard/kivy` on
the android device.

I have not yet tested this method.
