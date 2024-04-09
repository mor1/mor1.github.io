---
title: Building Up Your ARMs
subtitle: Creating boot images for Cubieboards
layout: post
category: blog
---

Due to the impending finish of the EU FP7 funded [User Centric
Networking][ucn][^1] I recently had cause to revisit the excellent work that
[Thomas Leonard][talex5] did for the project in getting Xen/ARM running on the
[Cubieboard2][cb2] and [Cubietruck][cb3] (aka [Cubieboard3][cb3]).

The resulting repo, [mirage/xen-arm-builder][xab], had languished for several
months and the past SD card images had some problems and had been allowed to
drop off the 'Net as a result. However, sterling work by [Ian Campbell][ijc] at
a recent Mirage [hackathon][] had started to resurrect this work based on
the [Alpine Linux][alpine] distribution. This seemed a promising place to start,
so I did :)

## Building an Image

The end result was an enormous [pull request][pr] that splatted a Brave New
World on top of [Thomas'][talex5] work.
The [`README`](https://github.com/mirage/xen-arm-builder/blob/master/README.md)
is hopefully reasonably self-explanatory but in summary,

1. Clone the repo:

   ```bash
   git clone https://github.com/mor1/arm-image-builder.git
   cd arm-image-builder
   ```

2. Use the `make` targets:

   ```bash
   make all       # runs `make prepare build image`
   # make prepare # clones repos, pulls tarballs
   # make build   # use Docker to build the `linux/` and `u-boot/` trees
   # make image   # finally, create the on-disk `sdcard.img`
   ```

This clones the necessary repos (Linux, u-boot), builds them, and then puts
together the image file `sdcard.img` in the current directory. If on OSX, `make
sdcard` will then attempt to write that to a blank, mounted SD card. This does a
rather hacky auto-discovery of where the SD card might be mounted; if in doubt,
and in any case, always safer to simply

```bash
MNT=the-correct-mount-point make sdcard
```

...or simply use your favourite tools to write the `sdcard.img` file to your SD
card.

## Using the Image

The end result should be an SD card that you can use to boot your device into
[Alpine Linux v3.4][alpine]. At present, completing installation requires then:

  * [resetting the environment](https://github.com/mirage/xen-arm-builder#first-boot--re-initialisation),
  * [completing Alpine setup](https://github.com/mirage/xen-arm-builder#base-install) via
    the `setup-alpine` script,
  * (if desired) installing Xen via the
    `/media/mmcblk0p1/alpine-dom0-install.sh` script created as part of building
    the SD card image,
  * (if desired) finally,
    building [Alpine](https://github.com/mirage/xen-arm-builder#alpine)
    and/or [Debian](https://github.com/mirage/xen-arm-builder#debian) `domU`s
    via the `/media/mmcblk0p1/alpine-domU-install.sh` and
    `/media/mmcblk0p1/debian-domU-install.sh` scripts, also created as part of
    building the image.

Hopefully the net result is you end up with a Cubieboard2/3 running Xen with an
Alpine Linux `dom0` and some `domU` images available.

As
ever, [comments, patches, pull requests welcome][mort]!

[ucn]: https://usercentricnetworking.eu
[^1]: Grant No. 611001 for those who care.
[talex5]: https://github.com/talex5
[cb2]: http://cubieboard.org/model/cb2/
[cb3]: http://cubieboard.org/model/cb3/
[xab]: https://github.com/mirage/xen-arm-builder
[ijc]: https://github.com/ijc25
[hackathon]: https://mirage.io/blog/2016-summer-hackathon-roundup
[alpine]: https://alpinelinux.org/
[pr]: https://github.com/mirage/xen-arm-builder/pull/71
[mort]: https://twitter.com/mort___
