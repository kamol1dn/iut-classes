#!/usr/bin/env python3
"""Mirror Prof. Jeong Hong's off-eClass material into the shared repo.

Embedded Software and Deep Learning for CV keep almost nothing on eClass. Their
real material is a public GitHub repo per course plus a GitHub Pages slides
site. This script brings both into the course folders, where classmates
browsing the shared repo can see them:

    <course>/course-repo/      read-only snapshot of the professor's repo
    <course>/lectures/slides/  every deck from the slides site, one HTML each

The snapshot is taken with ``git archive origin/main`` from the clone in
``labs/``, never from the working tree. So your own edits to graded lab files
(``moves.py`` and friends) stay local: the snapshot always holds the blanks
exactly as the professor published them.

Usage:
    python scripts/pull_prof_material.py            # pull, snapshot, download
    python scripts/pull_prof_material.py --no-slides
    python scripts/pull_prof_material.py --check    # report what changed, write nothing
"""

from __future__ import annotations

import argparse
import io
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from urllib.parse import urljoin

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
SEMESTER = REPO_ROOT / "semester 7"
# eClass's and GitHub's bot filters both reject the default python UA.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"

COURSES = [
    {
        "folder": "SOC3050 - Embedded Software and Design",
        "clone": "labs/soc3050code",
        "url": "https://github.com/gnoejh/soc3050code",
        # ~1 GB of bundled compilers and simulators. Clone the real repo to build.
        "exclude": ["tools"],
        "site": "https://gnoejh.github.io/soc3050code/",
        # The site is flat: every deck is <name>.html next to index.html.
        "deck_re": r'href="([0-9A-Za-z_-]+\.html)"',
        "deck_name": lambda href: href,
    },
    {
        "folder": "SOC4180 - Deep Learning for Computer Vision",
        "clone": "labs/soc4180",
        "url": "https://github.com/gnoejh/soc4180",
        # Encrypted instructor material; useless to anyone without the key.
        "exclude": ["instructor.tar.gz.gpg"],
        "site": "https://gnoejh.github.io/soc4180/",
        # One deck per week: <NN-topic>/slides.html, saved as "weekNN - topic.html".
        "deck_re": r'href="([0-9]+[a-z]?-[a-z0-9-]+/slides\.html)"',
        "deck_name": lambda href: "week{} - {}.html".format(*href.split("/")[0].split("-", 1)),
    },
]


def git(clone: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(clone), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def snapshot(course: dict, check: bool) -> str:
    folder = SEMESTER / course["folder"]
    clone = folder / course["clone"]
    if not clone.exists():
        subprocess.run(["git", "clone", "--quiet", course["url"], str(clone)], check=True)
    git(clone, "fetch", "--quiet", "origin")
    if not git(clone, "status", "--porcelain"):
        git(clone, "merge", "--ff-only", "--quiet", "origin/main")
    head = git(clone, "rev-parse", "--short", "origin/main")

    out = folder / "course-repo"
    marker = out / ".snapshot"
    old = marker.read_text().strip() if marker.exists() else "none"
    if old == head:
        return f"{head} (unchanged)"
    if check:
        return f"{old} -> {head} (would refresh)"

    spec = ["--", "."] + [f":(exclude){p}" for p in course["exclude"]]
    tar_bytes = subprocess.run(["git", "-C", str(clone), "archive", "origin/main", *spec],
                               check=True, capture_output=True).stdout
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tar:
        tar.extractall(out, filter="data")
    marker.write_text(head + "\n")
    return f"{old} -> {head}"


def slides(course: dict, check: bool) -> str:
    out = SEMESTER / course["folder"] / "lectures" / "slides"
    session = requests.Session()
    session.headers["User-Agent"] = UA
    index = session.get(course["site"], timeout=60)
    index.raise_for_status()
    hrefs = sorted(set(re.findall(course["deck_re"], index.text)))
    if check:
        missing = [h for h in hrefs if not (out / course["deck_name"](h)).exists()]
        return f"{len(hrefs)} decks online, {len(missing)} not on disk"

    out.mkdir(parents=True, exist_ok=True)
    changed = 0
    for href in hrefs:
        r = session.get(urljoin(course["site"], href), timeout=300)
        r.raise_for_status()
        dest = out / course["deck_name"](href)
        if not dest.exists() or dest.read_bytes() != r.content:
            dest.write_bytes(r.content)
            changed += 1
    return f"{len(hrefs)} decks, {changed} new or changed"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report what would change, write nothing")
    ap.add_argument("--no-slides", action="store_true", help="skip the slides sites")
    args = ap.parse_args()

    for course in COURSES:
        print(course["folder"])
        print("  repo:  ", snapshot(course, args.check))
        if not args.no_slides:
            print("  slides:", slides(course, args.check))
    return 0


if __name__ == "__main__":
    sys.exit(main())
