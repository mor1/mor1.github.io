---
title: Of Mice and Keyboards
description: El Capitan Upgrade and Microsoft Devices
layout: post
category: blog
---

A bit of a delay since the last post -- lots going on! But anyway: I
(relatively) recently upgraded my old skool Macbook Pro (look! built-in Ethernet
port! DVD drive!) to El Capitan. This was generally rather less faff that the
previous upgrade, though it did seem to take rather more reboots than might have
been assumed to be *strictly* necessary before it settled down, and I'd
remembered to fix up permissions for Homebrew with `sudo chown -R
$(whoami):admin /usr/local`. So that was ok.

![Macbook Pro UK Keyboard]({{ site.url }}/images/keyboard-small.png "Macbook Pro
UK Keyboard")

Except... I have a slightly odd keyboard and mouse setup. It's a UK Macbook
which means a slightly tweaked keyboard layout compared to the standard US
Macbook keyboard. At my desk, I also use a *Microsoft Digital Media Keyboard* --
nice action (for me!) plus some handy shortcut keys -- and a *Microsoft 5-Button
Mouse with IntelliEye*. Now, until El Capitan I'd happily been using the
Microsoft provided software to make use of the extra mouse buttons and shortcut
keys, coupled with a
[Ukelele-generated](http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=ukelele)
keymap to handle the oddities of the UK laptop keyboard (like, who in the world
really needs `§` at the top-left key, below `escape` rather than ``` ` ```; and
doesn't need an easily accessible `#`?).

This had never been entirely satisfactory -- I had to have a standard keymap
installed in addition to my modified one, and some apps (all of Microsoft
Office, I'm looking at you) liked to intermittently flip the keymap away from my
keymap to the standard issue on, including undoing my remapping of `caps lock`
to `ctrl`. This was annoying, but having it completely break was intolerable.

So I went hunting for alternatives and am now very happy with
[Karabiner.app][karabiner] for standard keyboard remappings, and fairly happy
with [USB Overdrive](http://www.usboverdrive.com) to handle the mouse and the
special Microsoft Digital Media Keyboard shortcut keys.

[karabiner]: https://pqrs.org/osx/karabiner/

### USB Overdrive

USB Overdrive seems to do the mouse mappings correctly, having detected the
device as a "Microsoft 5-Button Mouse with IntelliEye(tm), Any Application" --
`Button 4` and `Button 5` can be remapped to `forward` and `back`, just as I
like it.

![USB Overdrive]({{ site.url }}/images/usboverdrive.png "USB Overdrive Configuration")

It also allows me to repurpose some of the extra keys on my Microsoft keyboard
that [Karabiner][] doesn't seem able to see-- so I get one touch play/pause of
iTunes and other such delights.


### Karabiner.app

[Karabiner][] took a bit more setting up but does a very nice job. I needed to
remap certain keys differently on the two different keyboards to make both
consistent and to fix some of the weirder (to my mind!) decisions both Microsoft
and (particualrly) Apple have taken with their layouts. The result is an
[XML configuration file][karabiner.xml], symlinked by `~/Library/Application
Support/Karabiner/private.xml`. This applies two keymaps based on the detected
device, using product ID codes determined by the `EventViewer` app that comes
with [Karabiner][]:

[karabiner.xml]: https://github.com/mor1/rc-files/blob/master/karabiner.xml

```xml
<deviceproductdef>
  <productname>MACBOOK_PRO_UK_KEYBOARD</productname>
  <productid>0x0253</productid>
</deviceproductdef>

<deviceproductdef>
  <productname>DIGITAL_MEDIA_KEYBOARD</productname>
  <productid>0x00b4</productid>
</deviceproductdef>

<deviceproductdef>
  <productname>FIVE_BUTTON_MOUSE_WITH_INTELLIEYE</productname>
  <productid>0x0039</productid>
</deviceproductdef>
```

There are then two  `<item></item>` stanzas that configure the two different
keyboards, e.g.,

```xml
<item>
  <name>Keyboard mappings for Microsoft keyboard</name>
  <identifier>private.io.mort.microsoft_keyboard</identifier>
  <device_only>
    DeviceVendor::MICROSOFT,
    DeviceProduct::DIGITAL_MEDIA_KEYBOARD
  </device>
  ...
```

Each of these contains a number of `<autogen></autogen>` stanza mapping specific
keycodes for that keymap. For example, I want the top-left key on the main block
to be ``` ` ``` and, when shifted, to be `€`. This leads to the following on the
Microsoft keyboard:

```xml
<!-- shift-` to € -->
<autogen>
  __KeyToKey__
  KeyCode::BACKQUOTE, ModifierFlag::SHIFT_L | ModifierFlag::NONE,
  KeyCode::KEY_2, ModifierFlag::OPTION_R | ModifierFlag::SHIFT_R
</autogen>
<autogen>
  __KeyToKey__
  KeyCode::BACKQUOTE, ModifierFlag::SHIFT_R | ModifierFlag::NONE,
  KeyCode::KEY_2, ModifierFlag::OPTION_R | ModifierFlag::SHIFT_R
</autogen>
```

...but to the following on the Macbook built-in UK keyboard, to take account
first of the different keycode it generates but also to ensure that when used
with command and command-shift, the standard behaviour of cycling between
windows works:

```xml
<!-- top-left § to ` -->
<autogen>
  __KeyToKey__
  KeyCode::DANISH_DOLLAR, ModifierFlag::NONE,
  KeyCode::BACKQUOTE
</autogen>
<!-- ...with shift, to € -->
<autogen>
  __KeyToKey__
  KeyCode::DANISH_DOLLAR, ModifierFlag::SHIFT_L | ModifierFlag::NONE,
  KeyCode::KEY_2, ModifierFlag::OPTION_R | ModifierFlag::SHIFT_R
</autogen>
<autogen>
  __KeyToKey__
  KeyCode::DANISH_DOLLAR, ModifierFlag::SHIFT_R | ModifierFlag::NONE,
  KeyCode::KEY_2, ModifierFlag::OPTION_R | ModifierFlag::SHIFT_R
</autogen>
<!-- ...with COMMAND/SHIFT, so that cycle-window-{forward,back} work -->
<autogen>
  __KeyToKey__
  KeyCode::DANISH_DOLLAR, ModifierFlag::COMMAND_L | ModifierFlag::NONE,
  KeyCode::BACKQUOTE, ModifierFlag::COMMAND_R
</autogen>
<autogen>
  __KeyToKey__
  KeyCode::DANISH_DOLLAR, ModifierFlag::COMMAND_L | ModifierFlag::SHIFT_L | ModifierFlag::NONE,
  KeyCode::BACKQUOTE, ModifierFlag::COMMAND_R | ModifierFlag::SHIFT_R
</autogen>
```

There are a number of other mappings made in [karabiner.xml][]: `shift-'` is
`@`, `shift-2` is `"`, `shift-3` is `£`, and resolving general confusion among
`#`, `\`, `~`, and `|`.

### Emacs

That fixed things for the terminal and for most apps -- the only remaining
sticking point was Emacs. I don't pretend to understand the entire chain of
event processing but suffice it to say that Emacs was receiving `shift-@` and
`shift-3` without knowing what to do with them. Fortunately, when coupled with
[my hacks to enforce a `my-keys-minor-mode` to override everything](https://github.com/mor1/rc-files/blob/master/emacs.d/init.el#L929-L1019),
the fix was pretty straightforward:

```lisp
(define-key my-keys-minor-mode-map (kbd "s-@") "€")
(define-key my-keys-minor-mode-map (kbd "s-3")
  '(lambda () (interactive) (insert-char #x00A3))) ; £
```

### Result?

A **significant** decrease in the need I feel to curse because my keyboard has
changed in the middle of typing! It seems that keyboards remain, like time and
terminals, one of those *Really Hard* things for computers/manufacturers to
handle...

*Note: Thanks to <http://www.amp-what.com/unicode/search/> for an easy way to
hunt down some of the unicode symbols used above!*
