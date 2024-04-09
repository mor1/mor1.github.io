---
title: Evolving the Unikernel Revolution
subtitle: From revolution to evolution!
layout: post
category: blog
---

I've had the pleasure of giving a couple of talks at some fun venues recently,
extolling both the virtues of [unikernels][] and talking a bit about where we
currently see them as usefully being deployed.

[unikernels]: http://unikernel.org/

Specifically, [Operability.io 2016][oio] a couple of weeks ago was enlightening
about some of the problems faced in operating production systems. Some great
audience questions and follow-ups after the talk, including some who were even
wondering when we'll see unikernels as ready for the desktop! Of course, with
the release of the [Docker for Mac][d4m] and [Docker for Windows][dfw] products,
it's arguable that we've beaten Linux to that accolade, as both products make
extensive use of [MirageOS][] unikernel libraries. Having said that, I was
pleased to be told that the message about unikernels having a range of
deployment scenarios, and particularly partial deployments into micro-service
environments made sense to many who came to speak to me afterwards.

[d4m]: https://docker.com/...
[d4w]: https://docker.com/...
[mirageos]: https://mirage.io
[oio]: https://operability.io/

This was followed by a slightly expanded version of that talk earlier today at
the [Devox Belgium][devoxx] conference. [Devoxx][] is primarily a Java community
so I was interested to see how the talk would go down given that [MirageOS][] is
staunchly OCaml-centric, and the [unikernels][] movement in general is language
specific and (at least until now) somewhat weighted toward functional
programming, our good friends at [IncludeOS][] notwithstanding. In the end it
seemed to go pretty well, based on what little I could see through the bright
lights-- maybe one day I'll get used to that when being videoed! Certainly some
good questions again, on the specific utility of unikernels to IoT, the
relationship between unikernels and Docker, and more besides.

[devoxx]: https://devoxx.be/
[includeos]: http://www.includeos.org/

Anyway, I hope anyone who came to either talk enjoyed it and found it
interesting. Happy to respond to comments or questions via email or
on [Twitter](https://twitter.com/mort___)!
