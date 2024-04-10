+++
title = "codes"
tags = ["top", "mirage", "dataware", "homework", "karaka", "pyrt"]
date = "1970-01-01"
[extra]
hidden = true
+++

Most of the code I write is available via my [Github][] account -- pull requests
always welcome! -- but I thought I'd collate links to some of the larger
codebases I've been involved with as well as some of the Github organisations
I'm involved in.

[github]: https://github.com/mor1

<h2 data-magellan-destination="mirage" id="mirage">
  <a href="http://openmirage.org">Mirage</a> <small>2010&ndash;date</small>
</h2>

MirageOS is a framework for creating _unikernels_ that revisits of library OS
work from the 1990s joined with the application of functional programming
techniques (specifically, the [OCaml][] language) and the of the [Xen][]
hypervisor. Compact, efficient, lightweight, self-contained, MirageOS unikernels
can be generated from a single codebase to target anything from [the cloud][aws]
to [small form-factor ARM devices][cubieboard]. Our current focus is on support
for the Internet-of-Things and the use of MirageOS to produce infrastructure
that can be deployed by non-expert users as part of the [HDI][] agenda.

[ocaml]: http://ocaml.org/
[xen]: http://xen.org/
[aws]: http://aws.amazon.com/
[cubieboard]: http://cubieboard.org/tag/cubieboard2/
[hdi]: http://hdiresearch.org/

<h2 data-magellan-destination="dataware" id="dataware">
  <a href="http://github.com/dataware">Dataware</a>
  <small>2011&ndash;2014</small>
</h2>

Developed through [Horizon Digital Economy Research][horizon], Dataware
represents a set of prototype services enabling control over access to personal
data. Presents data via web services, and controls access via a personal
catalogue. Third-parties access personal data by requesting permission via the
catalogue, allowing accesses to be audited and managed.

[horizon]: http://www.horizon.ac.uk/

<h2 data-magellan-destination="homework" id="homework">
  <a href="https://github.com/homework/">Homework</a>
  <small>2010&ndash;2013</small>
</h2>

Developed during the [Homework][] project, the Homework router reconstructs the
home router informed by ethnographic study of home networks 'in the wild'. Uses
OpenFlow (Open vSwitch and NOX/POX) to provide novel interrogation, control and
policy interfaces to a home router.

[homework]: http://homenetworks.ac.uk/

<h2 data-magellan-destination="karaka" id="karaka">
  <a href="http://github.com/mor1/karaka/">Karaka</a>
  <small>2007&ndash;2009</small>
</h2>

Developed at Vipadia Limited, this is a scalable software system implementing a
distributed Skype-XMPP gateway released under the GPLv2. Copyright was acquired
by [Voxeo Corp.][voxeo] in January 2010.

[voxeo]: http://voxeo.com/

<h2 data-magellan-destination="pyrt" id="pyrt">
  <a href="http://github.com/mor1/pyrt">PyRT</a>
  <small>2001&ndash;2002</small>
</h2>

I developed the Python Routeing Toolkit while at Sprint ATL, who released it
under the GPLv2. It comprises code for collecting and analysing routeing data.
This package currently collects BGPv4 and ISIS, and dumps and parses MRTD files
including MRTD `TABLE_DUMP` files (as available from, e.g., [RouteViews][] and
[RIPE/RIS][ripe-ris]). A number of utilities for manipulating these dumps are
also provided. Since the code on [Sprint's website][pyrt] appears to be
orphaned, I have created a [github repository here][pyrt-git] for it. I have
also subsequently written an [OCaml][ocaml-mrt] MRT dump parser as a learning
exercise.

[mirage]: http://openmirage.org/
[pyrt]: https://research.sprintlabs.com/pyrt/
[routeviews]: http://www.routeviews.org/
[ripe-ris]: http://www.ripe.net/data-tools/stats/ris/ris-raw-data
[ocaml-mrt]: https://github.com/mor1/ocaml-mrt
[pyrt-git]: https://github.com/mor1/pyrt/
