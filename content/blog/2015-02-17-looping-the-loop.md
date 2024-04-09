---
title: Looping the Loop
subtitle: Uncaching 301 Redirect in Chrome
layout: post
category: blog
---

In a fit of blogging mania, here's another one literally barely days after the
previous one. Maybe I'll crack this yet.

Anyway, this is just a short one with what verges on a Technical Contribution.
To whit: I recently sorted out [this domain](http://mort.io/) and was having
some issues getting some consistency between what `dig`, Chrome and my
[domain provider](http://gandi.net) believed to be the correct state. In
particular, I was switching over to make the domain properly live rather than
simply a `301 Moved Permanently` redirect to my old pages at Nottingham.

It turns out this was probably mostly Chrome being confused. It seems that it
caches `301 Moved Permanently` redirects fairly aggressively and the cached
entries are __not__ discarded when you go through the standard mechanisms to
clear caches.

After a bit of experimentation and browsing, it seems that one way to clear this
is to `view-source` on the page but pass a spurious parameter to defeat the
cache. So, to force the browser to fetch <http://mort.io> properly, all I had to
do was `view-source:mort.io?spurious=parameter`. And lo! All was well.
