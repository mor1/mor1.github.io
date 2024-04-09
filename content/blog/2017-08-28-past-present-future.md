---
title: Platforms, Packaging, Progress
subtitle: Modernising a small OCaml package
layout: post
category: blog
---

I recently decided to refresh and update my [ocal] package,[^1] primarily to
port it to use the excellent [notty] before adding support for indicating
week-of-year. At the same time, I took the opportunity to update the build
infrastructure now that the OCaml world has some shiny new packaging and build
tools to go with [OPAM], namely [`topkg`] and [`jbuilder`]. So, starting
from [Dave Scott's][djs55] [wiki entry] about how to package [Mirage] libraries,
here's what I had to do...

[^1]: A somewhat over-featured replacement for the standard UNIX `cal` utility,
    because I got irritated by its American-centricity and my
    initial [Python replacement][py-cal] was just too slow...

[ocal]: https://github.com/mor1/ocal/
[OPAM]: https://github.com/ocaml/opam/
[`topkg`]: https://github.com/dbuenzli/topkg/
[`jbuilder`]: https://github.com/janestreet/jbuilder/
[topkg]: https://github.com/dbuenzli/topkg/
[jbuilder]: https://github.com/janestreet/jbuilder/
[djs55]: http://github.com/djs55/
[wiki entry]: https://mirage.io/wiki/packaging
[notty]: https://github.com/pqwy/notty/
[Mirage]: https://mirage.io/
[py-cal]: https://github.com/mor1/python-scripts/blob/master/cal.py


### Remove Oasis remnants

```bash
git rm _oasis setup.ml Makefile* _tags myocamlbuild.ml .merlin
mv ocal.opam/opam o && git rm -rf ocal.opam && mv o ocal.opam && git add ocal.opam
cat >| .gitignore <<_EOF
_build
*.merlin
*.install
_EOF
```

Although we're removing the `ocal.opam/descr` file, we're not going to lose the
content: we're going to let `topkg opam pkg` use its default `--readme` option
to extract the relevant info from the first marked up section of the
[`README.md`]:

```markdown
# ocal — An improved Unix `cal` utility

%%VERSION%%

A replacement for the standard Unix `cal` utility. Partly because I could,
partly because I'd become too irritated with its command line interface.
```

[`README.md`]: https://github.com/mor1/ocal/blob/0.2.0/README.md

We also remove but don't lose the functionality of the `.merlin` and OPAM
`ocal.install` files, as [jbuilder] will generate them for us.

### Create `src/jbuild` file

```bash
cat >| src/jbuild <<_EOF
(jbuild_version 1)

(executable
 ((public_name ocal)
  (package     ocal)
  (name        main)

  (libraries
   (
    astring
    calendar
    cmdliner
    notty
    notty.unix
    ))
  (flags (:standard -w "A-44-48-52" -safe-string))
  ))
_EOF
```

This corresponds to the [0.2.0](https://github.com/mor1/ocal/releases/tag/0.2.0)
release of [ocal]. Note that the `name` parameter refers to the module that
contains the entrypoint for the executable, and that we turn on all warnings
(`A`) except for three that we wish to ignore:

  * `44`: Open statement shadows an already defined identifier.
  * `48`: Implicit elimination of optional arguments.
  * `52`: (see 8.5.1) Fragile constant pattern.

After I did some tidying up of the code to deal with the newly imposed warnings,
`make` and `make install` satisfactorily (and quickly!) used [jbuilder] to
build and install the executable as `~/.opam/system/bin/ocal` (thanks to the
`public_name` stanza in the `src/jbuild` file, above). `make uninstall` then
caused [jbuilder] to remove it, before I `opam` pinned it and then reinstall
through `opam` to check that workflow worked as well:

```bash
opam remove ocal
opam pin add -yn --dev-repo ocal .
opam install ocal
```

### Create the `topkg` skeletons

Having refreshed the basic build infrastructure, next it's time to update the
packaging workflow. For a simple library we could use the automatic
[jbuilder]/[topkg] plugin per the [wiki entry]:

```bash
mkdir pkg
cat >| pkg/pkg.ml <<_EOF
#!/usr/bin/env ocaml
#use "topfind"
#require "topkg-jbuilder.auto"
_EOF
```

However, this isn't a library so we don't have documentation to build so we
don't bother with the `odoc` skeleton. As a result we also need to customise
[`pkg/pkg.ml`] so as to stop `topkg publish` failing when it can't build docs:

```ocaml
#!/usr/bin/env ocaml
#use "topfind"
#require "topkg-jbuilder"

open Topkg

let publish =
  Pkg.publish ~artefacts:[`Distrib] ()

let () =
  Topkg_jbuilder.describe ~publish ()
```

[`pkg/pkg.ml`]: https://github.com/mor1/ocal/blob/0.2.0/pkg/pkg.ml

### Prepare a release

Finally, we follow the standard [topkg] workflow to prepare a release. First,
add an entry to [`CHANGES.md`] with the correct formatting and commit the
result, and then:

```make
distrib:
	[ -x $$(opam config var root)/plugins/opam-publish/repos/ocal ] || \
	  opam-publish repo add ocal mor1/ocal
	topkg tag
	topkg distrib
```

...which creates tokens for accessing the GitHub repo for this project (if they
don't already exist), creates a release tag based on entries in [`CHANGES.md`],
and then creates the release tarballs (without the edits to [`pkg/pkg.ml`] this
would also build the docs, but we have none).

### Publish a release

Finally, we publish the release to GitHub and issue a pull request to
the [OPAM repository][opam] to add the new release into OPAM after linting and
tests have passed.

```make
publish:
	topkg publish
	topkg opam pkg
	topkg opam submit
```

[opam]: https://github.com/ocaml/opam-repository/
[`CHANGES.md`]: https://github.com/mor1/ocal/blob/0.2.0/CHANGES.md

Given that this repo has only a single package, we could in fact simply issue

```
topkg tag && topkg bistro
```

Also, as an alternative to customising the [`pkg/pkg.ml`] as indicated above, we
could simply remember to indicate the appropriate customisation on the command
line:

```
topkg publish distrib
```

...but `topkg bistro` wouldn't then work.

### Conclusion

So that's it: a simple executable distribution taken from old-school [Oasis] and
[OCamlBuild] infrastructure to shiny new modern [jbuilder] and [topkg]. The new
scheme seems to me to be an improvement: faster build times, simpler (to my
eyes) metadata, autogeneration of more of the repeated metadata (`.merlin` etc),
and a reasonably simple [`Makefile`] that I actually think I understand.
Definitely progress :)

[Oasis]: http://oasis.forge.ocamlcore.org/
[OCamlBuild]: https://ocaml.org/learn/tutorials/ocamlbuild/
[`Makefile`]: https://github.com/mor1/ocal/blob/0.2.0/Makefile
