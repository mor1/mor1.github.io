---
title: Begin, Again!
subtitle: The Turtle Moves!
layout: post
category: blog
---

Specifically, I've left [Horizon](http://www.horizon.ac.uk) and the
[School of Computer Science](http://www.cs.nott.ac.uk) at the
[University of Nottingham](http://www.nottingham.ac.uk) to (re-)join the
[Cambridge University](http://www.cam.ac.uk)
[Computer Laboratory](http://www.cl.cam.ac.uk). In celebration, and frankly
because it was long overdue anyway, I've reworked my website. What do you think?

For the curious, or the technically inclined, the site now uses
[ZURB Foundation][foundation] 5.5.0 (the current downloadable release as of
yesterday), with some slightly customised CSS. The site itself is largely
written in [Markdown][markdown] and currently generated using
[Jekyll][] to be hosted on [Github](http://github.com).

It's actually gone through an interim phase where it was parsed by the OCaml
[OMD][omd] parser before being crunched into a [Mirage KV_RO][mirage-types]
filesystem which is then compiled into a type-safe, self-contained web appliance
that serves these pages and no other using the OCaml [Cowabloga][], [COW][] and
[CoHTTP][] libraries. This could either be run as a [POSIX binary][mirage-unix]
or a self-contained [Xen VM][mirage-xen] depending on what I felt like. Neat eh?
(And for the sceptical among you, yes, a thing _can_ be neat and yet appear
curiously over-engineered at the same time... :)

For the time being however, I'm using it as an excuse to think about what I
might do to better support site generation like this in [Cowabloga][] so that I
can more seamlessly switch between [Jekyll][] and [Mirage][].

[foundation]: http://foundation.zurb.com/
[markdown]: http://daringfireball.net/projects/markdown/
[jekyll]: http://jekyllrb.com/

[omd]: https://github.com/pw347/omd
[cow]: https://github.com/mirage/ocaml-cow
[cowabloga]: https://github.com/mirage/cowabloga
[cohttp]: https://github.com/mirage/ocaml-cohttp

[mirage]: http://openmirage.org/
[mirage-types]: https://github.com/mirage/mirage-types
[mirage-unix]: https://github.com/mirage/mirage-platform/tree/master/unix
[mirage-xen]: https://github.com/mirage/mirage-platform/tree/master/xen
