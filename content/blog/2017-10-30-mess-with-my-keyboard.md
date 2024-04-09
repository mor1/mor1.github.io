---
title: Spring Loading Karabiner in the Autumn
subtitle: Don't You Mess With My Keyboard
layout: post
category: blog
---

I recently took the plunge and upgraded my OS X. Not to vN of _Sierra_ as I'd
hoped, but to v0 _High Sierra_-- the perils of waiting too long...

Unfortunately, this toasted[^1] my carefully curated keyboard remappings as
[Karabiner][] used a kernel extension, for which everything changed. All was not
lost however, as the rewrite to support Sierra/High Sierra was well underway. Or
so I thought until I realised that the configuration file had changed from XML
to JSON. And so my configuration journey began. (But it all ends well, so that's
good.)

[Karabiner]: https://pqrs.org/osx/karabiner/
[^1]: To be honest, I suspect even the _Sierra_ upgrade would've done this.

## Controlling the config

The first thing was to get the new configuration matters under control. I did
this per the documentation, symlinking the config subdirectory from my
`rc-files` repo:

```bash
cd ~/.config/
mv karabiner/ ~/rc-files/
ln -s ~/rc-files/karabiner
```

## Internal Apple keyboard

In the interests of keeping all configuration in one place (but see below), I
decided to do this via a set of [complex modifications][keymap]. In summary this
meant:

  * swap `(caps_lock)` and `(control)`:

```json
    {
      "description": "mort: caps_lock -> ctrl",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "caps_lock",
            "modifiers": {"optional": ["any"]}
          },
          "to": [
            {
              "key_code": "left_control"
            }
          ]
        }
      ]
    },
```

  * swap `"` (glyph `S-'`) with `@` (glyph `S-2`):

```json
    {
      "description": "mort: S-' (\") <-> S-2 (@)",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "quote",
            "modifiers": {"mandatory": ["shift"]}
          },
          "to": [
            {
              "key_code": "2",
              "modifiers": ["shift"]}
          ]
        },
        {
          "type": "basic",
          "from": {
            "key_code": "2",
            "modifiers": {"mandatory": ["shift"]}
          },
          "to": [
            {
              "key_code": "quote",
              "modifiers": ["shift"]
            }
          ]
        }
      ]
    },
```

  * map `(backslash)` (glyph `\`) to `#`, and `S-\` (glyph `|`) to `~`:

```json
    {
      "description": "mort: \\ -> #; S-\\ (|) -> ~",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "backslash"
          },
          "to": [
            {
              "key_code": "3",
              "modifiers": ["option"]
            }
          ]
        },
        {
          "type": "basic",
          "from": {
            "key_code": "backslash",
            "modifiers": {"mandatory": ["shift"]}
          },
          "to": [
            {
              "key_code": "grave_accent_and_tilde",
              "modifiers": ["shift"]
            }
          ]
        },
...
    }
```

  * map `(non_us_backslash)` (glyph `§`) to `` ` `` and `S-(non_us_backslash)`
    (glyph `±`) to `€`, and then patch things up so that the usual window
    switching works (using `` (command)-` ``):

```json
    {
      "description": "mort: § -> `; ± (S-§) -> €",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "non_us_backslash"
          },
          "to": [
            {
              "key_code": "grave_accent_and_tilde"
            }
          ]
        },
        {
          "type": "basic",
          "from": {
            "key_code": "non_us_backslash",
            "modifiers": {"mandatory": ["shift"]}
          },
          "to": [
            {
              "key_code": "2",
              "modifiers": ["option"]
            }
          ]
        },
        {
          "type": "basic",
          "from": {
            "key_code": "non_us_backslash",
            "modifiers": {"mandatory": ["command"]}
          },
          "to": [
            {
              "key_code": "grave_accent_and_tilde",
              "modifiers": ["command"]
            }
          ]
        },
        {
          "type": "basic",
          "from": {
            "key_code": "non_us_backslash",
            "modifiers": {"mandatory": ["command", "shift"]}
          },
          "to": [
            {
              "key_code": "grave_accent_and_tilde",
              "modifiers": ["command", "shift"]
            }
          ]
        }
      ]
    },
```

  * finally, map `` ` `` to `\` and `` S-` `` to `|`

```json
    {
      "description": "mort: ` -> \\; S-` (~) -> |",
      "manipulators": [
        {
          "type": "basic",
          "from": {
            "key_code": "grave_accent_and_tilde"
          },
          "to": [
            {
              "key_code": "backslash"
            }
          ]
        },
        {
          "type": "basic",
          "from": {
            "key_code": "grave_accent_and_tilde",
            "modifiers": {"mandatory": ["shift"]}
          },
          "to": [
            {
              "key_code": "backslash",
              "modifiers": ["shift"]
            }
          ]
        }
      ]
    },
```

## iTerm2

Unfortunately for me, iTerm2 then gets a bit confused as it wants to leave
`(command)` alone, only allowing mapping of `(option)` to `(meta)` (or, in fact,
`(esc+)`). In the past I swapped `(left_command)` and `(left_option)` to make
the usual shell (`bash`) CLI editing combinations (roughly, `emacs`) work.  That
wasn't ideal though as I then had to fix up the window cycling commands
(``(command)-` `` and so on). Fortunately, the fix this time seems easier: just
configure the two tricky mappings (involving generating a keypress modified with
`(option)`) to be interpreted by iTerm2 to just send the appropriate text
through. Again, I did this in the UI (Preferences > Profiles > Keys) but the
resulting configuration change is also straightforward:

```xml
			<key>Keyboard Map</key>
			<dict>
...
				<key>0x32-0x80000</key>
				<dict>
					<key>Action</key>
					<integer>12</integer>
					<key>Text</key>
					<string>€</string>
				</dict>
...
				<key>0x33-0x80000</key>
				<dict>
					<key>Action</key>
					<integer>12</integer>
					<key>Text</key>
					<string>#</string>
				</dict>
...
			</dict>
```

## Microsoft Digital Media keyboard

Examining the key codes using the Karabiner Event-Viewer, it seemed that the
first thing to do was to swap `(grave_accent_and_tilde)` (glyph `` ` ``) and
`(non_us_backslash)` (slightly confusingly, glyph `\` on my keyboard). I started
out trying to do this as a complex modification so that all the remappings were
in [one file][keymap], but couldn't: I couldn't figure out how to control the
application order of mappings in that file. However, simple modifications are
applied before complex modifications, and this _is_ a simple modification as
it's a direct swap, so I just used the UI and did it there. For the sake of
completeness, the resulting modification to [`karabiner.json`][config] is:

[keymap]: https://github.com/mor1/rc-karabiner/blob/master/assets/complex_modifications/mort-keymap.json
[config]: https://github.com/mor1/rc-karabiner/blob/master/karabiner.json

```json
{
...
    "profiles": [
        {
...
            "devices": [
                {
                    "disable_built_in_keyboard_if_exists": false,
                    "fn_function_keys": [],
                    "identifiers": {
                        "is_keyboard": true,
                        "is_pointing_device": false,
                        "product_id": 180,
                        "vendor_id": 1118
                    },
                    "ignore": false,
                    "simple_modifications": [
                        {
                            "from": {
                                "key_code": "grave_accent_and_tilde"
                            },
                            "to": {
                                "key_code": "non_us_backslash"
                            }
                        },
                        {
                            "from": {
                                "key_code": "non_us_backslash"
                            },
                            "to": {
                                "key_code": "grave_accent_and_tilde"
                            }
                        }
                    ]
                }
            ],
...
        }
    ]
}
```

The next step was to patch up the complex modifications. Once I realised that
the event viewer was claiming that the key with glyph `#` was emitting
`(backslash)` while it was, in fact, emitting `(non_us_pound)`, this was fairly
straightforward:
  * swap `(command)` (glyph `Alt`) and `(option)` (glyph `Start`):

```json
        {
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [{"vendor_id": 1118, "product_id": 180}]
            }
          ],
          "type": "basic",
          "from": {
            "key_code": "left_option",
            "modifiers": {"optional": ["any"]}
          },
          "to": [
            {
              "key_code": "left_command"
            }
          ]
        },
        {
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [{"vendor_id": 1118, "product_id": 180}]
            }
          ],
          "type": "basic",
          "from": {
            "key_code": "left_command",
            "modifiers": {"optional": ["any"]}
          },
          "to": [
            {
              "key_code": "left_option"
            }
          ]
        }
      ]
    },
```

  * add coverage of `(non_us_pound)` to the rule that remaps `\` to `#`:
```json
        {
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [{"vendor_id": 1118, "product_id": 180}]
            }
          ],
          "type": "basic",
          "from": {
            "key_code": "non_us_pound"
          },
          "to": [
            {
              "key_code": "3",
              "modifiers": ["option"]
            }
          ]
        },
        {
          "conditions": [
            {
              "type": "device_if",
              "identifiers": [{"vendor_id": 1118, "product_id": 180}]
            }
          ],
          "type": "basic",
          "from": {
            "key_code": "non_us_pound",
            "modifiers": {"mandatory": ["shift"]}
          },
          "to": [
            {
              "key_code": "grave_accent_and_tilde",
              "modifiers": ["shift"]
            }
          ]
        }
```

...and that's it. My keyboard is, once again, my castle.
