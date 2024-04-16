_default:
    @just --list

bibdir := "/home/mort/u/me/publications"
papers := "./templates/shortcodes/publications.html"
output := "./docs"

# check internal and external links
@check:
  @zola check --drafts

# bring up the server, showing drafts as well
@test: papers
  @zola serve --drafts

# build the site, minimally
@build: papers
  @zola build --force --output-dir {{output}}

# build papers data for site
@papers:
  ./bib2html.py bibinputs.json >| {{papers}}

# remove built site
@clean:
  rm -rf {{output}}
