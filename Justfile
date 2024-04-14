_default:
    @just --list

bibdir := "/home/mort/u/me/publications"
papers := "publications.html"

# check internal and external links
@check:
  @zola check --drafts

# bring up the server, showing drafts as well
@test: build
  @zola serve --drafts

# build the site, minimally
@build: papers
  @zola build

# build papers data for site
@papers:
  #!/usr/bin/env bash
  cd ./templates/shortcodes
  ./render_publications.py '{{bibdir}}/rmm-[cjptwu]*.bib' >| {{papers}}

# # Publish `master` to the drafts site
# draft:
#   @git push origin master:drafts

# # Publish `master` to the production site
# publish:
#   @git push origin master:publish

@clean:
  rm -rf public
