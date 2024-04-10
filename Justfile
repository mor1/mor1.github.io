_default:
    @just --list

flags  := env_var_or_default('DOCKER_FLAGS', '')
docker := "docker run -u $(id -u) -v $(pwd -P):/cwd -w /cwd $flags"
bibs   := "~/u/me/publications"

# check internal and external links
@check:
  @zola check --drafts

# bring up the server, showing drafts as well
@test: build
  @zola serve --drafts

# build the site, minimally
@build: papers jss
  @zola build

# build papers data for site
@papers:
  #!/usr/bin/env bash
  python3 ./bib2json.py \
    -s {{bibs}}/strings.bib {{bibs}}/rmm-[cjptwu]*.bib \
  | tr '\r\n' '\n' >| research/papers/papers.json

# build JS for site
@jss:
  #!/usr/bin/env bash
  {{docker}} mor1/coffeescript -c -o static/js papers.coffee

# # Publish `master` to the drafts site
# draft:
#   @git push origin master:drafts

# # Publish `master` to the production site
# publish:
#   @git push origin master:publish

@clean:
  rm -rf public
