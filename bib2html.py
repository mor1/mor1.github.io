#!/usr/bin/env python3

import json
import logging
import os
from typing import Optional

import bibtexparser
import click
from bibtexparser import middlewares as mw
from rich.console import Console
from rich.logging import RichHandler
from yattag import Doc, indent

errcon = Console(stderr=True)
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=errcon, rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HOMEPAGES = {}


def authors(doc, bib):
    authors = bib.get("author").value
    with doc.tag("span", klass="authors"):
        for i, author in enumerate(authors):
            if i == 0:
                pass
            elif i + 1 == len(authors):
                doc.text(" and ")
            else:
                doc.text(", ")

            klass = "author"
            key = f"{author.first[0]} {author.last[0]}"
            homepage = HOMEPAGES.get(key)

            if (author.first[0], author.last[0]) == ("Richard", "Mortier"):
                klass += " highlight"

            author.first = [f"{author.first[0][0].strip()}."]
            with doc.tag("span", klass=klass):
                if homepage:
                    with doc.tag("a", href=homepage):
                        doc.text(f"{author.merge_last_name_first}")
                else:
                    doc.text(f"{author.merge_last_name_first}")


def parse_date(bib):
    date = bib.get("issue_date")
    if date:
        date = date.value
        month, year = date.split(" ")

    else:
        date = bib.get("date")
        if date:
            date = date.value
            year, month, day = date.split("-")
        else:
            year = bib.get("year").value
            month = bib.get("month").value if bib.get("month") else ""
            month, *day = month.split("#")
            day = " ".join(day if day else "").strip()

        month = {
            "": "",
            "01": "January",
            "jan": "January",
            "02": "Feburary",
            "feb": "February",
            "03": "March",
            "mar": "March",
            "04": "April",
            "apr": "April",
            "05": "May",
            "may": "May",
            "06": "June",
            "jun": "June",
            "07": "July",
            "jul": "July",
            "08": "August",
            "aug": "August",
            "09": "September",
            "sep": "September",
            "10": "October",
            "oct": "October",
            "11": "November",
            "nov": "November",
            "12": "December",
            "dec": "December",
        }[month.strip()]

        if month:
            date = f"{day} {month}, {year}"
        else:
            date = year

    return date, year, month


def year(doc, year):
    with doc.tag("span", klass="year"):
        doc.text(f" ({year}) ")


def title(doc, bib):
    title = bib.get("title").value
    with doc.tag("span", klass="title"):
        doc.asis(f"&ldquo;{title}&rdquo;. ")


def publisher(doc, bib):
    publisher = bib.get("publisher")
    if publisher:
        with doc.tag("span", klass="publisher"):
            doc.text(f" {publisher.value.strip()} ")


def venue(doc, bib):
    addendum = ""
    match bib.entry_type:
        case "inproceedings":
            doc.text("In ")
            venue = bib["booktitle"]

            address = bib.get("address")
            if address:
                addendum += f". {address.value}"

            pages = bib.get("pages")
            if pages:
                addendum += f". pp.&nbsp;{pages.value}"

        case "article":
            doc.text("In ")
            venue = bib.get("journaltitle")
            if not venue:
                venue = bib.get("journal")
            venue = venue.value

            volume = bib.get("volume")
            if volume:
                addendum += f"&nbsp;{volume.value}"

            number = bib.get("number")
            if number:
                addendum += f"({number.value})"

            pages = bib.get("pages")
            if pages:
                addendum += f":{pages.value}"

        case "patent":
            venue = "Patent"

        case "online" | "report" | "misc":
            doc.text("In ")
            venue = bib.get("eprinttype")
            if not venue:
                venue = bib.get("institution")
            if not venue:
                venue = bib.get("publisher")
            venue = venue.value

        case "inbook":
            doc.text("In ")
            venue = bib.get("volume")
            if not venue:
                venue = bib.get("booktitle")
            venue = venue.value

        case "unpublished":
            venue = ""

        case _:
            venue = "UNKNOWN VENUE"

    with doc.tag("span", klass="venue"):
        doc.asis(f"{venue.strip()}")

    if len(addendum) > 0:
        doc.asis(f"{addendum}. ")


def date(doc, date):
    with doc.tag("span", klass="date"):
        doc.text(f"{date}. ")


def note(doc, bib):
    with doc.tag("span", klass="note"):
        note = bib.get("note")
        if note:
            doc.text(f"{note.value.strip()}. ".replace("..", "."))


def doi(doc, bib):
    with doc.tag("span", klass="doi"):
        doi = bib.get("doi")
        if doi:
            with doc.tag("a", href=doi.value):
                doc.asis(f"doi:{doi.value} ")


def url(doc, bib):
    with doc.tag("span", klass="url"):
        url = bib.get("url")
        if url:
            with doc.tag("a", href=url.value):
                doc.asis(f"{url.value}")


def html(bib, doc: Optional[Doc] = None) -> Doc:
    if doc is None:
        doc = Doc()
    assert doc is not None

    if isinstance(bib, list):
        for entry in bib:
            klass = ["paper"]
            match entry.entry_type:
                case "article":
                    klass += ["journal"]
                case "inproceedings":
                    klass += ["conference"]
                case _:
                    klass += [entry.entry_type]

            with doc.tag("li", id=entry.key, klass=" ".join(klass)):
                html(entry, doc)

    elif isinstance(bib, bibtexparser.model.Entry):
        try:
            log.debug(f"{bib=}")
            d, y, _ = parse_date(bib)

            authors(doc, bib)
            year(doc, y)
            title(doc, bib)
            venue(doc, bib)
            publisher(doc, bib)
            date(doc, d)
            note(doc, bib)
            doi(doc, bib)
            url(doc, bib)

        except Exception:
            log.exception(f"ENTRY : {bib}")
            raise

    elif isinstance(bib, bibtexparser.library.Library):
        html(bib.entries, doc)
        return doc

    else:
        assert False


@click.command()
@click.argument("config", type=click.File("r"))
@click.option("--debug", default=False, is_flag=True)
def main(
    config,
    debug,
):
    if debug:
        log.setLevel(logging.DEBUG)

    config = json.load(config)
    log.debug(f"{config=}")

    global HOMEPAGES

    homepages = config.get("homepages")
    if homepages:
        with open(homepages) as f:
            HOMEPAGES = json.load(f)
    log.debug(f"{HOMEPAGES=}")

    strings = config.get("strings", "")
    if len(strings) > 0:
        with open(strings) as f:
            strings = f.read()
    log.debug(f"{strings=}")

    bibdir = config.get("bibdir", ".")
    log.debug(f"{bibdir=}")

    print("{{dummy}}")

    for section, filenames in config["sections"].items():
        log.info(f"{section=} {filenames=}")
        content = ""
        for filename in filenames:
            with open(os.path.join(bibdir, filename)) as f:
                content += f.read()

        library = bibtexparser.parse_string(
            strings + content,
            append_middleware=[
                mw.LatexDecodingMiddleware(),
                mw.SeparateCoAuthors(),
                mw.SplitNameParts(),
                mw.SortFieldsCustomMiddleware(order=("year", "authors")),
            ],
        )

        stats = {
            "blocks": len(library.blocks),
            "entries": len(library.entries),
            "comments": len(library.comments),
            "strings": len(library.strings),
            "preamble": len(library.preambles),
            "failures": len(library.failed_blocks),
        }
        log.info(f"{stats=}")

        if len(library.failed_blocks) > 0:
            for failure in library.failed_blocks:
                log.error(
                    f"{failure.start_line}({failure.duplicate_keys}) {failure.raw}"
                )

        doc = Doc()
        with doc.tag("section", klass="papers"):
            doc.text(section)
        with doc.tag("ol", klass="papers"):
            html(library, doc)

        print(indent(doc.getvalue()))


if __name__ == "__main__":
    main()  # pyright: ignore
