# Semester 7 — 2026 Fall (202602)

Inha University in Tashkent · 6 courses · 17 credits
Mirrored from [eClass](https://eclass.inha.ac.kr/) on **2026-09-20** (week 3).

---

## Status — 2026-09-20 11:33

**Attendance is clean.** NTS4070 now reads **3 attendance · 0 absence · 0 late**
— weeks 2 and 3 were both marked absent earlier today and have since cleared.
Nothing is currently at risk.

| Next up | When |
|---|---|
| **NTS4070 Quiz 2** — *opens* today at 18:27, no close time published | ⏰ tonight → [open quiz](https://eclass.inha.ac.kr/mod/quiz/view.php?id=71122) |
| Classes resume | Tomorrow, Mon 2026-09-21 — SOC4040, then SOC4180 |
| Week 4 begins | Sat 2026-09-26 |

Full list in [DEADLINES.md](DEADLINES.md).

---

## Courses

| Code | Course | Instructor | Mode | Where material actually lives |
|---|---|---|---|---|
| [NTS4070](NTS4070%20-%20Distinguished%20Lecture%20in%20Social%20Science%20and%20Art/) | Distinguished Lecture in Social Science and Art | Bobir Muratov | ONLINE | eClass — weekly deck + VOD + quiz |
| [SOC3050](SOC3050%20-%20Embedded%20Software%20and%20Design/) | Embedded Software & Design | Jeong Hong | Offline | **GitHub + Telegram** (eClass nearly empty) |
| [SOC4020](SOC4020%20-%20Multimedia%20Computing/) | Multimedia Computing | Minhaz Uddin Ahmed | Offline | eClass — PPTX decks + practice code |
| [SOC4040](SOC4040%20-%20Artificial%20Intelligence/) | Artificial Intelligence | Eraliev Oybek | Offline | eClass — PDF decks + notebooks, **+ Discord** |
| [SOC4180](SOC4180%20-%20Deep%20Learning%20for%20Computer%20Vision/) | Deep Learning for Computer Vision | Jeong Hong | Offline | **GitHub + slides site + Telegram** |
| [SOC4190](SOC4190%20-%20Blockchain%20Basics%20and%20Platforms/) | Blockchain Basics and Platforms | Yusupov Jalolliddin | ONLINE | ⚠️ nothing published yet |

### The three distribution styles

1. **eClass-native** (NTS4070, SOC4020, SOC4040) — everything is posted as files
   under weekly sections. This folder mirrors them; ask me to re-sync.
2. **Off-platform** (SOC3050, SOC4180, both Prof. Jeong Hong) — eClass has only
   the syllabus and a timetable. Real material is on GitHub, a slides site and
   Telegram. Clone the repos into each course's `labs/` and `git pull`.
3. **Not started** (SOC4190) — empty page three weeks in.

---

## Weekly schedule

Schedule values are reproduced exactly as registered on eClass. **eClass is
ambiguous about whether they are clock hours or period (교시) indices** — the
calendar labels the same classes with different period numbers. Confirm against
the timetable images in `SOC3050 .../resources/` and `SOC4180 .../resources/`.

| Day | Course | Registered slot |
|---|---|---|
| Mon | SOC4040 Artificial Intelligence | `11~13` |
| Mon | SOC4180 Deep Learning for CV | `14~16` |
| Tue | SOC4020 Multimedia Computing | `4~6` |
| Wed | SOC4020 Multimedia Computing | `11~13` |
| Wed | SOC3050 Embedded Software & Design | `15~17` |
| Thu | SOC4180 Deep Learning for CV | `9~11` |
| Thu | SOC4040 Artificial Intelligence | `13~15` |
| Fri | SOC3050 Embedded Software & Design | `18~20` |
| — | NTS4070, SOC4190 | online, self-paced within weekly windows |

All offline classes are in **room B-101**.

---

## Grading weights at a glance

| Course | Mid | Final | Attend. | Assign. | Quiz | Other |
|---|---|---|---|---|---|---|
| NTS4070 | 30% | — | 20% | — | 20% | Debate 30% |
| SOC3050 | 30% | 30% | 5% | 30% | — | 5% |
| SOC4020 | 30% | 30% | 5% | 15% | **20%** | — |
| SOC4040 | 25% | 25% | 10% | 20% | — | **Term project 20%** |
| SOC4180 | 30% | 30% | 5% | 30% | — | 5% |
| SOC4190 | *no syllabus registered* | | | | | |

**Things that fail you outright** (SOC3050 and SOC4180, Prof. Jeong Hong):
8 absences · skipping any lab, project, midterm or final · cheating.
SOC3050 also closes the classroom door **5 minutes after** class starts.

**Heaviest non-exam load:** SOC4040's term project (20%, presented week 14) and
SOC4020's quizzes (20%, where late homework is never accepted).

---

## Folder layout

Every course follows the same shape:

```
<COURSE CODE> - <Name>/
├── README.md      course dashboard: how material is posted, what is on hand, links
├── syllabus/      syllabus.md (readable) + the original PDF where one exists
├── lectures/      slide decks and notes, prefixed "weekNN - "
├── labs/          (Jeong Hong's courses) clone the GitHub repo here
├── homework/      assignments as they are set
├── resources/     notebooks, practice code, timetable images
└── my-notes/      yours
```

`_meta/` holds the sync manifest — the eClass IDs behind every file here, so
re-checking for updates is a lookup rather than a re-crawl.

---

## Keeping this up to date

Just ask, in plain words:

- *"check eClass for updates"* — re-crawl all six courses, download anything new, update the READMEs
- *"what is due this week?"* — re-read the calendar and refresh [DEADLINES.md](DEADLINES.md)
- *"update SOC4020"* — one course only
- *"pull the GitHub repos"* — refresh Prof. Jeong Hong's material

Last full sync: **2026-09-20 11:33**.
