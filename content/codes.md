+++
title = "codes"
template = "pages.html"
date = "1970-01-01"
[extra]
hidden = true
+++

Most of the code I write is available via my [Github][] account -- pull requests
always welcome! -- but I thought I'd collate links to some of the larger
codebases I've been involved with as well as some of the Github organisations I
participate in.

[github]: https://github.com/mor1

## [Mirage](https://mirage.io/) <small>2010---date</small>

MirageOS is a framework for creating _unikernels_ that revisits of library OS
work from the 1990s joined with the application of functional programming
techniques (specifically, the [OCaml][] language) and the of the [Xen][]
hypervisor. Compact, efficient, lightweight, self-contained, MirageOS unikernels
can be generated from a single codebase to target anything from [the cloud][aws]
to [small form-factor ARM devices][cubieboard]. 

[ocaml]: https://ocaml.org/
[xen]: https://xen.org/
[aws]: https://aws.amazon.com/
[cubieboard]: https://cubieboard.org/tag/cubieboard2/
[hdi]: https://hdiresearch.org/

## [Dataware](https://github.com/dataware) <small>2011---2014</small>

Developed through [Horizon Digital Economy Research][horizon], Dataware
represents a set of prototype services enabling control over access to personal
data. Presents data via web services, and controls access via a personal
catalogue. Third-parties access personal data by requesting permission via the
catalogue, allowing accesses to be audited and managed.

[horizon]: https://www.horizon.ac.uk/

## [Homework](https://github.com/homework/) <small>2010---2013</small>

Developed during the [Homework][] project, the Homework router reconstructs the
home router informed by ethnographic study of home networks 'in the wild'. Uses
OpenFlow (Open vSwitch and NOX/POX) to provide novel interrogation, control and
policy interfaces to a home router.

[homework]: https://homenetworks.ac.uk/

## [Karaka](https://github.com/mor1/karaka/) <small>2007---2009</small>

Developed at Vipadia Limited, this is a scalable software system implementing a
distributed Skype-XMPP gateway released under the GPLv2. Copyright was acquired
by [Voxeo Corp.][voxeo] in January 2010.

[voxeo]: https://voxeo.com/

## [PyRT](https://github.com/mor1/pyrt/) <small>2001---2002</small>

I developed the Python Routeing Toolkit while at Sprint ATL, who released it
under the GPLv2. It comprises code for collecting and analysing routeing data.
This package currently collects BGPv4 and ISIS, and dumps and parses MRTD files
including MRTD `TABLE_DUMP` files (as available from, e.g., [RouteViews][] and
[RIPE/RIS][ripe-ris]). A number of utilities for manipulating these dumps are
also provided. Since the code on [Sprint's website][pyrt] appears to be
orphaned, I have created a [GitHub repository here][pyrt-git] for it. I have
also subsequently written an [OCaml][ocaml-mrt] MRT dump parser as a learning
exercise.

[mirage]: https://openmirage.org/
[pyrt]: https://research.sprintlabs.com/pyrt/
[routeviews]: https://www.routeviews.org/
[ripe-ris]: https://www.ripe.net/data-tools/stats/ris/ris-raw-data
[ocaml-mrt]: https://github.com/mor1/ocaml-mrt/
[pyrt-git]: https://github.com/mor1/pyrt/
