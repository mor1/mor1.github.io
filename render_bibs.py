#!/usr/bin/env python3

import glob
import logging
import sys
from typing import Optional

import bibtexparser
from bibtexparser import middlewares as mw
from rich.console import Console
from rich.logging import RichHandler
from yattag import Doc, indent

STRINGS = r"/home/mort/u/me/publications/strings.bib"

errcon = Console(stderr=True)
logging.basicConfig(
    level="INFO",
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
            authors = bib.get("author").value
            with doc.tag("span", klass="authors"):
                for i, author in enumerate(authors):
                    if i + 1 == len(authors):
                        doc.text(" and ")

                    klass = "author"
                    if (author.first[0], author.last[0]) == ("Richard", "Mortier"):
                        klass += " highlight"
                    author.first = [f"{author.first[0][0].strip()}."]
                    with doc.tag("span", klass=klass):
                        doc.text(f"{author.merge_last_name_first}")
                    if i + 1 < len(authors):
                        doc.text(", ")

            doc.stag("br")

            title = bib.get("title").value
            with doc.tag("span", klass="title"):
                doc.text(f"{title}")

            doc.stag("br")

            date = bib.get("issue_date")
            if date:
                date = date.value
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
                        "jan": "January",
                        "feb": "February",
                        "mar": "March",
                        "apr": "April",
                        "may": "May",
                        "jun": "June",
                        "jul": "July",
                        "aug": "August",
                        "sep": "September",
                        "oct": "October",
                        "nov": "November",
                        "dec": "December",
                    }[month.strip()]

                date = " ".join([day, month, year])
            with doc.tag("span", klass="date"):
                doc.text(f"{date.strip()}")

        except Exception:
            log.exception(f"ENTRY : {bib}")
            raise
            # errcon.print_exception(show_locals=True)

    elif isinstance(bib, bibtexparser.library.Library):
        with doc.tag("ul"):
            html(bib.entries, doc)
        return doc

    else:
        assert False


if __name__ == "__main__":
    INPUT = sys.argv[1]

    bibfiles = glob.glob(INPUT)

    with open(STRINGS) as f:
        strings = f.read()

    content = ""

    for filename in bibfiles:
        with open(filename) as f:
            content += f.read()

    library = bibtexparser.parse_string(
        strings + content,
        append_middleware=[
            mw.LatexDecodingMiddleware(),
            # mw.MonthIntMiddleware(),
            mw.SeparateCoAuthors(),
            mw.SplitNameParts(),
            mw.SortBlocksByTypeAndKeyMiddleware(),
            # mw.AddEnclosingMiddleware(),
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

    doc = html(library)
    print(indent(doc.getvalue()))
