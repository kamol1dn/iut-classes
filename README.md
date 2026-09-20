# IUT Classes

Coursework for **Inha University in Tashkent**, CSE/ICE.

Each semester is mirrored from [eClass](https://eclass.inha.ac.kr/) into a
uniform folder structure so studying starts by opening this repo, not by hunting
across eClass, GitHub, Telegram and Discord.

| Semester | Term | Courses |
|---|---|---|
| [semester 7](semester%207/) | 2026 Fall (`202602`) | 6 — start at its [README](semester%207/README.md) and [DEADLINES](semester%207/DEADLINES.md) |

## Layout

```
semester N/
├── README.md              dashboard: courses, timetable, grading weights
├── DEADLINES.md           what is closing now + dated milestones
├── _meta/                 sync manifest — eClass IDs behind every file
└── <CODE> - <Name>/
    ├── README.md          how this professor posts material, what is on hand
    ├── syllabus/          syllabus.md (readable) + original PDF
    ├── lectures/          decks and notes, prefixed "weekNN - "
    ├── labs/              cloned course repos live here (git-ignored)
    ├── homework/
    ├── resources/         notebooks, practice code, timetable images
    └── my-notes/
```

## Notes

- `labs/` contents are **git-ignored** — those are separate upstream repos. Each
  course README has its clone command.
- `.vscode/settings.json` opens `.md` files in rendered preview by default.
  To edit one: right-click → *Open With…* → *Text Editor*.
- Lecture slides and PDFs here are the instructors' material, kept for personal
  study. This repo is private and should stay that way.
