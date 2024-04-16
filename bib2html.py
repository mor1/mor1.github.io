#!/usr/bin/env python3

import json
import logging
import os
from typing import Optional

import bibtexparser
from bibtexparser import middlewares as mw
from rich.console import Console
from rich.logging import RichHandler
from yattag import Doc, indent

HOMEPAGES = {}

errcon = Console(stderr=True)
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=errcon, rich_tracebacks=True)],
)
log = logging.getLogger(__name__)


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

            # compute date

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

                date = f"{day} {month}, {year}"

            # insert year
            with doc.tag("span", klass="year"):
                doc.text(f" ({year}) ")

            # insert title
            title = bib.get("title").value
            with doc.tag("span", klass="title"):
                doc.asis(f"&ldquo;{title}&rdquo;. ")

            # insert venue
            doc.text("In ")
            addendum = ""
            match bib.entry_type:
                case "inproceedings":
                    venue = bib["booktitle"]

                    address = bib.get("address")
                    if address:
                        addendum += f". {address.value}"

                    pages = bib.get("pages")
                    if pages:
                        addendum += f". pp.&nbsp;{pages.value}"

                case "article":
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
                    venue = "PATENT"

                case _:
                    venue = "UNKNOWN VENUE"

            with doc.tag("span", klass="venue"):
                doc.asis(f"{venue.strip()}")

            doc.asis(f"{addendum}. ")

            # insert date
            with doc.tag("span", klass="date"):
                doc.text(f"{date}. ")

            # insert note
            with doc.tag("span", klass="note"):
                note = bib.get("note")
                if note:
                    doc.text(f"{note.value}. ".replace("..", "."))

            # insert DOI
            with doc.tag("span", klass="doi"):
                doi = bib.get("doi")
                if doi:
                    with doc.tag("a", href=doi.value):
                        doc.asis(f"doi:{doi.value} ")

            # insert URL
            with doc.tag("span", klass="url"):
                url = bib.get("url")
                if url:
                    with doc.tag("a", href=url.value):
                        doc.asis(f"{url.value}")

        except Exception:
            log.exception(f"ENTRY : {bib}")
            raise
            # errcon.print_exception(show_locals=True)

    elif isinstance(bib, bibtexparser.library.Library):
        html(bib.entries, doc)
        return doc

    else:
        assert False


if __name__ == "__main__":
    bibfiles = {
        "Peer-reviewed journal papers": ["rmm-journal.bib"],
        "Peer-reviewed conference papers": ["rmm-conference.bib"],
        "Peer-reviewed workshop papers": ["rmm-workshop.bib"],
        "Technical reports, editorials, book chapters, patents, etc.": [
            "rmm-techreport.bib",
            "rmm-patent.bib",
            "rmm-unpublished.bib",
        ],
    }

    with open(r"./authors.json") as f:
        HOMEPAGES = json.load(f)

    with open(r"/home/mort/u/me/publications/strings.bib") as f:
        strings = f.read()

    print("{{dummy}}")

    for section, filenames in bibfiles.items():
        content = ""
        for filename in filenames:
            with open(os.path.join("/home/mort/u/me/publications", filename)) as f:
                content += f.read()

        library = bibtexparser.parse_string(
            strings + content,
            parse_stack=[
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
        log.info(f"STATS: f{stats=}")

        if len(library.failed_blocks) > 0:
            for failure in library.failed_blocks:
                print(f"{failure.start_line}({failure.duplicate_keys}) {failure.raw}")

        doc = Doc()
        with doc.tag("section", klass="papers"):
            doc.text(section)
        with doc.tag("ol", klass="papers"):
            html(library, doc)

        print(indent(doc.getvalue()))
