---
title: Platforms, Packaging, Progress— Addendum
subtitle: Fixing OPAM Release Metadata Errors
layout: post
category: blog
---

This is a short addendum to
my
[post of a couple of days ago](http://mort.io/blog/2017/08/28/past-present-future/) caused
by my carelessness in writing
the
[OPAM file](https://github.com/mor1/ocal/blob/13a9a7f5b8f2e0be4c2b55941a00a885df202cf8/ocal.opam#L16-L22).
Careful readers will observe the lack of any dependency on [notty]. Read on for
what happened next...

[notty]: https://github.com/pqwy/notty/

The result of this carelessness was that everything worked just fine locally,
but
[my PR to the OPAM package repository](https://github.com/ocaml/opam-repository/pull/10176) failed.
Cue much wailing and gnashing of teeth.

However, thanks to a moment's assistance
from [Daniel Bünzli](http://erratique.ch/contact.en), this was easy to fix:

```bash
$ git checkout 0.2.0       # checkout the relevant release version tag
$ topkg opam pkg           # create the release metadata
$ e _build/ocal.0.2.0/opam # invoke editor so I can add the missing dep
$ topkg opam submit        # submit the updated OPAM metadata, updating the PR
Submitting _build/ocal.0.2.0
[ocal-0.2.0.tbz] http://github.com/mor1/ocal/releases/download/0.2.0/ocal-0.2.0.tbz downloaded
Updating existing pull-request #10176
Pull-requested: https://github.com/ocaml/opam-repository/pull/10176
```

For me, the main thing to note here is that the OPAM metadata in the repo at the
commit ref tagged for release doesn't match that which OPAM uses to install the
release. But as [Sebastien Mondet](http://seb.mondet.org/) pointed out to me,
this is neither relevant nor (in the long term) likely, as (e.g.) version
constraints on dependencies may need to be added to old versions of dependent
packages to keep them working. (Though I did add and commit the dependency to
`master`, naturally.)

So, all-in-all, an easy fix to a common problem. Which is the way it should
be...
