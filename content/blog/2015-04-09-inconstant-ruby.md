---
title: Diamonds are a Chap's Best Friend
subtitle: ...while Rubies are inconstant at best
layout: post
category: blog
---

As [noted previously](/blog/2015/01/15/begin-again/), this site is basically a
[Github][]-hosted [Jekyll][] site at present, though one that can be built as a
[Mirage][] unikernel. Part of the [Mirage][] workflow to publish a new post
involves using [Travis CI][travis] to build and then commit back a new unikernel
image. Thus it is currently necessary to run [Jekyll][] in the [Travis][] build
scripts, and the dynamism of the Ruby environment meant that this broke (again)
recently as one of the `github-pages` gem's dependencies now depends on `Ruby >=
2.0` while the default Rubies on the [Travis][] Ubuntu image for `C` language
builds is `1.8` (via Ubuntu packaging) or, if you remove that one, `1.9` (via
[rvm][]). Read on to find out how to fix this...

[github]: https://github.com/
[jekyll]: http://jekyllrb.com/
[mirage]: http://openmirage.org/
[travis]: https://travis-ci.org/

The fix that currently works for me turns out to be relatively simple: remove
all the rubies installed as Ubuntu packages, and then invoke [rvm][] to set the
default ruby to something reasonable -- in this case, 2.1.

[rvm]: https://rvm.io/

{% highlight bash %}
## remove old ubuntu rubies
sudo apt-get -y remove ruby ruby1.8
sudo apt-get -y autoremove

## use rvm and a modern-ish ruby
source ~/.rvm/scripts/rvm
rvm --default use 2.1

## check that all worked...
which ruby
ruby --version

## install jekyll and github-pages
gem install jekyll
gem install github-pages --no-rdoc --no-ri
jekyll -v
{% endhighlight %}

And that's all there is to it -- you should now be able to call `jekyll` in your
[Travis][] environment as you'd expect...
