# IUT Classes

Coursework for **Inha University in Tashkent**, CSE/ICE.

Each semester is mirrored from [eClass](https://eclass.inha.ac.kr/) into a
uniform folder structure so studying starts by opening this repo, not by hunting
across eClass, GitHub, Telegram and Discord.

| Semester | Term | Courses |
|---|---|---|
| [semester 7](semester%207/) | 2026 Fall (`202602`) | 6 — start at its [README](semester%207/README.md) |

## Layout

```
scripts/
├── pull_timetable.py      regenerates semester N/timetable.md from EduPage
└── pull_prof_material.py  snapshots Prof. Jeong Hong's GitHub repos + slides sites into course-repo/ and lectures/slides/

semester N/
├── README.md              dashboard: courses, timetable, grading weights
├── UPCOMING.md            deadlines, quiz windows, exams: the same for everyone
├── DEADLINES.md           (local only) my own status against those deadlines
├── timetable.md           generated — real clock times, rooms, teachers
├── _meta/                 (local only) sync manifest — eClass IDs behind every file
└── <CODE> - <Name>/
    ├── README.md          how this professor posts material, what is on hand
    ├── syllabus/          syllabus.md (readable) + original PDF
    ├── lectures/          decks and notes, prefixed "weekNN - "
    ├── labs/              cloned course repos live here (git-ignored)
    ├── homework/
    ├── resources/         notebooks, practice code, timetable images
    └── my-notes/
```

## Refreshing the timetable

```bash
python scripts/pull_timetable.py
```

Pulls the ICE23-1 timetable from <https://iut.edupage.org/timetable/> (public,
no login) and rewrites `semester 7/timetable.md`. Use `--check` to report drift
without writing, or `--all` to include subjects that were dropped.

## Notes

- `labs/` contents are **git-ignored**: they're working clones of upstream repos, where your own lab answers
  live. A read-only copy of each professor repo is in that course's `course-repo/` instead, refreshed with
  `python scripts/pull_prof_material.py`.
- `.vscode/settings.json` opens `.md` files in rendered preview by default.
  To edit one: right-click → *Open With…* → *Text Editor*.
- Lecture slides and PDFs here are the instructors' material, shared for classmates' study.
  The repo is public. Personal tracking (deadlines, attendance, submissions) is git-ignored and never committed.
