---
title: ARMing LinuxKit
subtitle: ARM64 support for LinuxKit on <code>packet.net</code>
layout: post
category: blog
---

As some may know, following the [Unikernel Systems][uniks] acquisition, I
currently do contract work for [Docker Inc.][docker] in addition to my day job
here at the [Cambridge University Computer Laboratory][cucl]. Recently this has
centred on [LinuxKit][], "_A toolkit for building secure, portable and lean
operating systems for containers_" and, specifically, enabling ARM64 support.
I'm pleased to say that a basic proof-of-concept is now complete, and we're
working towards getting support merged upstream.

[packet.net]: https://packet.net
[`packet.net`]: https://packet.net
[docker]: https://docker.com
[uniks]: https://unikernels.com
[linuxkit]: https://github.com/linuxkit/linuxkit
[cucl]: https://www.cl.cam.ac.uk

The proof-of-concept was developed using the great ARM64 support provided
by [`packet.net`][], on one of their `type 2A` boxes.

If you fancy trying it out, then hopefully the following instructions will be of
use -- or just bug me on the [`packet.net` Slack][slack]!

[slack]: https://slack.packet.net/

## Building

Start by getting an ARM64 box setup. If you have one to hand, great! If not, you
could head over to [packet.net] and create type 2A Ubuntu box to use as a build
environment.

Then clone the source, either `git
clone` [my dev branch](https://github.com/mor1/linuxkit/tree/project-arm64), or
see <https://github.com/linuxkit/linuxkit/pull/1654> for the open PR which may
be a bit more stable.

The essence of it then is to build the containers based off `aarch64/alpine`,
along with an ARM64 version of the [`moby` CLI][moby] if needed. Specifying the
container images you just built in your `moby.yml` file will then cause `moby`
to assemble things that should boot on ARM64.

The output should be a gzipped kernel, currently slightly misleadingly named
`bzImage` as well as a suitable `initrd`.

[moby]: https://github.com/moby/moby

## Booting

Setup another ARM64 box on which to boot the results. You could setup a
type 2A [packet.net] box once more, but this  time set it to _custom OS_ and
_iPXE boot_. For the iPXE boot URL, give a URL pointing to a suitable boot
file. I use:

```
#!ipxe
set base-url URL-TO-DIRECTORY-HOLDING-IMAGES
set kernel-params ip=dhcp nomodeset ro serial console=ttyAMA0,115200 earlycon earlyprintk=serial,keep initrd=arm64-initrd.img
initrd ${base-url}/arm64-initrd.img
imgstat
boot ${base-url}/arm64-bzImage ${kernel-params}
```

Note that, currently at least, the [packet.net] iPXE boot only occurs on the
first boot as it is assumed that the iPXE boot will install a working image to
the local disk. Thus, if it doesn't work first time, get an SOS console and
break in by hitting `^B` at the appropriate moment, before issuing `chain URL`
where `URL` points to your iPXE boot file.


## Conclusion

This just does the barest minimum for now -- I did say it was a
proof-of-concept... :) Work is currently ongoing to upstream this rather than
developing this PoC further, but if anyone has a particular interest or would
like to provide patches to, e.g., support network devices on [packet.net],
please [get in touch](mailto:mort@cantab.net), file an issue or send a pull
request!
