# Mort's Web Pages

In the past this was faintly experimental using [Mirage](https://mirage.io/),
[Docker](https://docker.com/), [Travis CI](https://travis-ci.org/) and all sorts
to avoid the need to install dependencies including
[Coffeescript](http://coffeescript.org/), [Jekyll](http://jekyllrb.com/),
[Python](http://python.org/). 

Time has passed and so this is now a fairly plain site, built using
[Zola](https://www.getzola.org/), [Just](https://github.com/casey/just), and a
script reliant on [BibTexParser](https://bibtexparser.readthedocs.io/), and
hosted via [GitHub Pages](https://pages.github.com/).

## Targets

`just` lists available tagets:  `clean` and `build` are hopefully obvious;
`test` builds and runs the site locally; and `papers` runs the scripts that
generates the HTML version of my publication list for inclusion when the site is
built. `publish` and `review` push the built content to the live and draft sites respectively.

# TODO

+ Return pages with headers permitting caching
+ Add hcard/vcard markup per <http://indiewebcamp.com/Getting_Started>
+ Add rel=me links to github, twitter per
  <http://indiewebcamp.com/Getting_Started>
+ Fix PDF hosting, per
  http://webapps.stackexchange.com/questions/48061/can-i-trick-github-into-displaying-the-pdf-in-the-browser-instead-of-downloading
