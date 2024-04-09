---
title: Rescuing a Shattered Nexus 4
subtitle: Help! I Lost My Photos!
layout: post
category: blog
---

A little while ago, before I'd done the smart thing and got myself a case for my
Nexus 4, I dropped it a couple of inches onto a hard surface at the wrong angle.
The screen promptly shattered -- and this was bad because without the touch
screen, I couldn't interact with it, I had some photos on it from son#1 birthday
party that hadn't been copied off, and I hadn't got round to enabling USB access
to the filesystem or any of the debug/developer options.

So what to do? I *really* didn't want to lose those photos. A couple of hours
searching the Interwebs and a little bit of experimentation later, and I managed
it. Basically, download and apply the clockwork mod bootloader, and this turns
on the developer options that allow access to the filesystem via the Android SDK
tools. To find out the details, read on...

First, download the recovery image:
```bash
$ wget http://download2.clockworkmod.com/recoveries/recovery-clockwork-touch-6.0.3.1-mako.img
```

Next, install the Android SDK -- I'm on OSX using [Homebrew][] so I do:
```bash
$ brew install android-sdk
```

Now, power off and disconnect the phone! Then boot it into fastboot mode by
holding down `power` and `volume-down`. Once it boots you should be in the
fastboot list -- the volume keys will cycle you through the list. You should now
also be able to see the device once connected to USB, and you can then OEM
unlock it:

```bash
$ sudo fastboot devices -l
04f02d4bdcd3b6e2       fastboot usb:FD123000
$ sudo fastboot oem unlock
...
OKAY [ 17.937s]
finished. total time: 17.937s
```

Having unlocked it, you can now install the clockwork recovery bootloader you
downloaded (assuming it's in the local directory):

```bash
$ sudo fastboot flash recovery recovery-clockwork-touch-6.0.3.1-mako.img
sending 'recovery' (7560 KB)...
OKAY [  0.526s]
writing 'recovery'...
OKAY [  0.448s]
finished. total time: 0.975s
```

When you now use the volume keys to cycle through the list, you should now see
__recovery mode__ as an option -- select it, and you should be able to see the
device listed in the usual way via `adb`:


```bash
: mort@greyjay:phone$; sudo adb devices -l
List of devices attached
04f02d4bdcd3b6e2       recovery usb:FD123000 product:occam model:Nexus_4 device:mako
```

Finally, pull all the contents off the sdcard:

```bash
$ adb pull /sdcard/0 ./sdcard/
$ adb pull /data/ ./data/
$ adb pull /system/ ./system/
```

...and that's it -- you should now have a local copy of everything off the
phone, and you can send it away for repair (or whatever you feel like
otherwise), possibly while sobbing quietly.
