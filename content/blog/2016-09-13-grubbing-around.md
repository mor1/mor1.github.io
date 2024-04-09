---
title: Grubbing Around
subtitle: Some commands I found useful
layout: post
category: blog
---

Nothing earth-shattering here: I recently had the "pleasure" of setting up an
ARM64 server. After considerable support, several firmware upgrades, corruption
of the main HDD, reinstallation of CentOS7 (recommended, somewhat to my
surprise), all that remained was to get an up-to-date Linux built and installed
with 32 bit binary support. This took a bit of `make config` fiddling, but got
there after a few tries.

And then I had to relearn how `grub`/`grub2` works in this brave new (to me)
UEFI CentOS7 world. Herewith some brief commands I found useful while doing
so...

{% highlight bash %}
sudo grep "^menu entry" /boot/efi/EFI/centos/grub.cfg \
     | tr -s " " | cut -f 2 -d "'" | cat -n
{% endhighlight %}

Edit `/etc/default/grub` to set `GRUB_DEFAULT=N` for desired value of `N`

Temporarily set the default for the next reboot:

{% highlight bash %}
sudo grub2-reboot 1 # based on output of above
{% endhighlight %}

Regenerate the grub2 configuration:

{% highlight bash %}
sudo grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
{% endhighlight %}
