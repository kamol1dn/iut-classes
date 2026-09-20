#!/usr/bin/env python3
"""Pull the ICE23-1 class timetable from iut.edupage.org and write it as markdown.

The EduPage timetable is public — no login, no token. Two POST endpoints:

    /timetable/server/ttviewer.js?__func=getTTViewerData   -> which timetables exist
    /timetable/server/regulartt.js?__func=regularttGetData -> the full dataset

The second returns every table for the whole university (82 classes, 681 cards);
we filter down to one class. Both accept ``__gsh: "00000000"`` as the security
hash, which is what the public page itself sends.

Usage:
    python scripts/pull_timetable.py                 # write the markdown
    python scripts/pull_timetable.py --check         # report drift, write nothing
    python scripts/pull_timetable.py --class ICE23-2 # a different group
    python scripts/pull_timetable.py --json out.json # also dump raw lessons
    python scripts/pull_timetable.py --all           # include dropped subjects
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import requests

BASE = "https://iut.edupage.org"
DEFAULT_CLASS = "ICE23-1"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "semester 7" / "timetable.md"

# Subject short code -> the eClass course it corresponds to. Courses that are
# taught online have no room slot and never appear in the timetable at all.
COURSE_MAP = {
    "AI": "SOC4040 — Artificial Intelligence",
    "DLCV": "SOC4180 — Deep Learning for Computer Vision",
    "MC": "SOC4020 — Multimedia Computing",
    "ES&D": "SOC3050 — Embedded Software & Design",
}

# EduPage publishes the timetable per *group*, not per student, so it lists
# everything ICE23-1 takes. Drop the subjects this student is not enrolled in.
# Pass --all to render the full group timetable regardless.
DROPPED = {
    "BDA": "Big Data Analytics — dropped 2026-09",
}


def open_session() -> requests.Session:
    """A plain GET on /timetable/ first — the RPC endpoints need its PHPSESSID."""
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": f"{BASE}/timetable/",
        }
    )
    s.get(f"{BASE}/timetable/", timeout=45).raise_for_status()
    return s


def post(session: requests.Session, path: str, args: list) -> dict:
    """POST to an EduPage RPC endpoint and return the unwrapped ``r`` payload.

    Both endpoints want exactly two positional args and reject a bare ``[None]``
    with an opaque ``{"e": "Error: ..."}``. ``__gsh`` is the security hash; the
    public page sends all zeros, and so do we.
    """
    resp = session.post(
        f"{BASE}{path}",
        json={"__args": args, "__gsh": "00000000"},
        headers={"Content-Type": "application/json"},
        timeout=60,
    )
    resp.raise_for_status()
    body = resp.json()
    if "r" not in body:
        raise RuntimeError(
            f"{path} rejected args {args!r}: {body.get('e') or body}"
        )
    return body["r"]


def current_timetable(session: requests.Session, year: str | None = None) -> tuple[str, str]:
    """Return (tt_num, label) for the timetable to pull.

    The second RPC argument is the school year. Passing the right one makes
    EduPage fill in ``default_num``; passing anything else still returns the
    full list but leaves it blank. So: try the year if we were given one, and
    otherwise fall back to the newest non-hidden timetable in the list. That
    keeps working when the year rolls over without hardcoding it.
    """
    regular = post(
        session,
        "/timetable/server/ttviewer.js?__func=getTTViewerData",
        [None, year or {}],
    )["regular"]

    available = [t for t in regular.get("timetables", []) if not t.get("hidden")]
    if not available:
        raise RuntimeError("EduPage listed no visible timetables")

    num = regular.get("default_num") or ""
    if not any(t["tt_num"] == num for t in available):
        newest = max(
            available,
            key=lambda t: (t.get("year") or 0, int(t["tt_num"]) if t["tt_num"].isdigit() else 0),
        )
        num = newest["tt_num"]

    label = next((t["text"] for t in available if t["tt_num"] == num), f"timetable {num}")
    return num, label


def fetch_tables(session: requests.Session, tt_num: str) -> dict[str, list]:
    res = post(
        session, "/timetable/server/regulartt.js?__func=regularttGetData", [None, tt_num]
    )
    tables = res.get("dbiAccessorRes", {}).get("tables")
    if not tables:
        raise RuntimeError(f"no tables returned for timetable {tt_num!r}")
    return {t["id"]: t.get("data_rows", []) for t in tables}


def build(tables: dict[str, list], class_name: str, keep_dropped: bool = False) -> list[dict]:
    """Flatten lessons+cards into one row per scheduled block, sorted by day/time."""
    by_id = lambda rows: {r["id"]: r for r in rows}  # noqa: E731
    subjects = by_id(tables["subjects"])
    teachers = by_id(tables["teachers"])
    rooms = by_id(tables["classrooms"])
    lessons = by_id(tables["lessons"])
    periods = {p["period"]: p for p in tables["periods"]}

    klass = next((c for c in tables["classes"] if c["name"] == class_name), None)
    if klass is None:
        names = sorted(c["name"] for c in tables["classes"])
        raise SystemExit(
            f"class {class_name!r} not found. Available: {', '.join(names)}"
        )

    mine = {lid for lid, l in lessons.items() if klass["id"] in l.get("classids", [])}

    entries = []
    for card in tables["cards"]:
        lesson = lessons.get(card["lessonid"])
        if lesson is None or card["lessonid"] not in mine:
            continue

        # Unplaced cards carry an empty period/days — EduPage keeps them around
        # for lessons the scheduler has not assigned a slot to. Skip them.
        period_raw = str(card.get("period") or "").strip()
        if not period_raw.isdigit() or "1" not in str(card.get("days") or ""):
            continue

        start_no = int(period_raw)
        span = int(lesson.get("durationperiods") or 1)
        end_no = start_no + span - 1
        start = periods.get(str(start_no))
        end = periods.get(str(end_no))
        if not start or not end:
            continue

        subject = subjects.get(lesson["subjectid"], {})
        if not keep_dropped and subject.get("short") in DROPPED:
            continue

        for idx, flag in enumerate(card["days"]):
            if flag != "1" or idx >= len(DAYS):
                continue
            entries.append(
                {
                    "day_index": idx,
                    "day": DAYS[idx],
                    "period_start": start_no,
                    "period_end": end_no,
                    "start": start["starttime"],
                    "end": end["endtime"],
                    "subject": subject.get("name", "?"),
                    "subject_short": subject.get("short", "?"),
                    "room": ", ".join(
                        rooms.get(r, {}).get("short", r) for r in card.get("classroomids", [])
                    ),
                    "teachers": ", ".join(
                        teachers.get(t, {}).get("short", t) for t in lesson.get("teacherids", [])
                    ),
                    "course": COURSE_MAP.get(subject.get("short", "")),
                }
            )

    entries.sort(key=lambda e: (e["day_index"], e["period_start"]))
    return entries


def render(entries: list[dict], class_name: str, label: str, tt_num: str,
           keep_dropped: bool = False) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [
        f"# Timetable — {class_name}",
        "",
        f"> {label} · EduPage timetable `{tt_num}`",
        f"> Pulled from <{BASE}/timetable/> on **{now}**.",
        "> Generated by `scripts/pull_timetable.py` — do not edit by hand.",
        "",
        "Periods are **30-minute slots starting at 08:00**, so period *n* begins at",
        "`07:30 + 0:30n`. The period numbers registered on eClass syllabi use this",
        "same scheme.",
        "",
    ]

    for idx, day in enumerate(DAYS):
        rows = [e for e in entries if e["day_index"] == idx]
        out.append(f"## {day}")
        out.append("")
        if not rows:
            out += ["*No classes.*", ""]
            continue
        out.append("| Time | Periods | Subject | Room | Teacher | eClass course |")
        out.append("|---|---|---|---|---|---|")
        for e in rows:
            course = e["course"] or "—"
            out.append(
                f"| **{e['start']}–{e['end']}** | {e['period_start']}~{e['period_end']} "
                f"| {e['subject']} | {e['room']} | {e['teachers']} | {course} |"
            )
        out.append("")

    unmapped = sorted({e["subject"] for e in entries if not e["course"]})
    if unmapped:
        out += [
            "## On the timetable but not on eClass",
            "",
            "Attended in person, with no eClass course page to mirror:",
            "",
        ]
        out += [f"- **{name}**" for name in unmapped]
        out.append("")

    if DROPPED and not keep_dropped:
        out += [
            "## Excluded",
            "",
            "EduPage publishes the timetable for the whole ICE23-1 group, so it also",
            "lists subjects not being taken. These are filtered out above — run the",
            "script with `--all` to see the full group timetable:",
            "",
        ]
        out += [f"- **{short}** — {why}" for short, why in sorted(DROPPED.items())]
        out.append("")

    out += [
        "## Online courses",
        "",
        "NTS4070 (Distinguished Lecture) and SOC4190 (Blockchain) are online and",
        "have no room slot, so they never appear here. Their weekly VOD windows are",
        "tracked in [DEADLINES.md](DEADLINES.md).",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--class", dest="class_name", default=DEFAULT_CLASS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    ap.add_argument("--json", type=Path, help="also dump the flattened entries as JSON")
    ap.add_argument("--year", help="school year, e.g. 2026 (usually auto-detected)")
    ap.add_argument("--all", action="store_true",
                    help="include dropped subjects (full ICE23-1 group timetable)")
    args = ap.parse_args()

    session = open_session()
    tt_num, label = current_timetable(session, args.year)
    print(f"timetable {tt_num}: {label}", file=sys.stderr)

    entries = build(fetch_tables(session, tt_num), args.class_name, keep_dropped=args.all)
    print(f"{len(entries)} scheduled blocks for {args.class_name}", file=sys.stderr)

    if args.json:
        args.json.write_text(json.dumps(entries, indent=2), encoding="utf-8")

    text = render(entries, args.class_name, label, tt_num, keep_dropped=args.all)
    old = args.out.read_text(encoding="utf-8") if args.out.exists() else ""

    # Ignore the "Pulled ... on" line so a re-run with no real change is a no-op.
    strip = lambda s: "\n".join(  # noqa: E731
        l for l in s.splitlines() if not l.startswith("> Pulled from")
    )
    changed = strip(old) != strip(text)

    if args.check:
        print("CHANGED" if changed else "unchanged")
        return 1 if changed else 0

    if changed:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}" if old else f"created {args.out}")
    else:
        print("unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
