# Embedded Software & Design

**Instructor:** Jeong Hong · **Rooms:** B101 (Wed), B202 (Fri) · **Mode:** Offline
**Schedule:** Wed **15:00–16:30** (B101) · Fri **14:00–15:30** (**B202**)
⚠️ eClass registers Friday as `18~20` in B-101 — that is wrong; see [timetable.md](../timetable.md).
**eClass course id:** `2615`

---

## ⚠️ Read this first — most material is NOT on eClass

Same setup as Deep Learning for CV: eClass carries the syllabus, a timetable
image and one intro deck. **The working material is on GitHub and Telegram.**

| Where | What | Link |
|---|---|---|
| **GitHub** | Course code, labs, examples | https://github.com/gnoejh/soc3050code |
| **Slides site** | Lecture decks, published live (eClass URL 71731, added week 4) | https://gnoejh.github.io/soc3050code/ |
| **Telegram** | Announcements, day-to-day comms | https://t.me/+EcqPs3qT0oZjYTI6 |
| eClass | Syllabus, timetable, week-1 deck | [course page](https://eclass.inha.ac.kr/course/view.php?id=2615) |

### 📦 Already in this repo (no clone needed)

| What | Where | Notes |
|---|---|---|
| **All lecture decks**, lessons 00–19 + board pin map | [`lectures/slides/`](lectures/slides/) | Downloaded from the live slides site (rendered from the lesson sources on every push, so newer than the repo's committed `_slides/`). Download a file and open it in a browser |
| **The course repo** (ARM + AVR projects, docs, shared libs, midterm guide) | [`course-repo/`](course-repo/) | A read-only snapshot of `gnoejh/soc3050code` at commit `7906b2f` (2026-10-24), refreshed every sync. **`tools/` is left out**: it's ~1 GB of bundled compilers and simulators. Clone the real repo to build and simulate |

To build, flash or simulate, clone it: `git clone https://github.com/gnoejh/soc3050code labs/soc3050code`,
then `git -C labs/soc3050code pull` to refresh.
The course has moved to an **ARM edition** (`projects2026_arm/`). On 09-30, VS Code
build, simulate and F5 debugging switched to it. **Week 4 is GPIO, polling and
interrupts**, which is ARM lesson 05: debouncing and EXTI, with notes on reaching
those code paths under GDB (updated 10-02).

## 📝 Midterm (30%, week 8, 26–30 Oct)

> *Closed book, no calculator. The only interrupt allowed is a nervous breakdown.*

Study guide added to the repo on 2026-10-18:
[`projects2026_arm/exam_midterm/overview.md`](course-repo/projects2026_arm/exam_midterm/overview.md).

- **60 min, 33 multiple-choice questions** (A–D, 1 mark each), with no penalty for wrong answers, so answer every question.
- **Closed book.** No notes, no calculator, no devices. Use a blue or black non-erasable pen.
  Write your name, ID and **section number on every page** (a wrong section number is penalised).
  Only the answer sheet on the cover is marked.
- **Scope: lessons 00–08** (programmer's model up to UART). Each lesson gives 2–5 questions.
- Expect to predict behaviour (silent failures), do hand calculations (bit masks, hex,
  little-endian, vector addresses, timer `PSC`/`ARR`, `BRR`), pick the correct line of
  code, and name concepts. You won't write any code.
- The guide has lesson-by-lesson notes, a formula sheet, a glossary and practice problems with answers.

**10-19 repo update, inside exam scope:** lesson **08 (UART and Python host)** got `keys.c`/`keys.h`. An arrow key
arrives over UART as three bytes (`ESC [ D`), so recognising one is a small framing problem. A **50 ms silence** separates
a lone Esc from the start of a sequence. The shell now echoes typed characters and handles Backspace, but never echoes a
`$` frame (otherwise `host.py` would read its own command back). The lab now says to use the Wokwi VS Code serial terminal.

The date isn't published yet. Midterm week is **26–30 Oct** (the syllabus said week 7). Check Telegram for the exact day.

---

## Grading

| Mid-term | Final | Attendance | Assignments | Quiz | Etc. |
|---|---|---|---|---|---|
| 30% | 30% | 5% | 30% | 0% | 5% |

## ⚠️ Failure conditions — unusually strict

Any **one** of these fails the course:

- 8 absences (1/4 of classes), unless cleared with the professor **beforehand** (not via AA)
- No Labs · No Project · No Midterm · No Final
- Cheating in labs, homework, projects or exams
- **The classroom door closes 5 minutes after the start of class**

No class changes allowed.

## What is on eClass right now

| Item | Week | Filed as |
|---|---|---|
| Syllabus (PDF) | — | [syllabus/soc3050.pdf](syllabus/soc3050.pdf) |
| Timetable image, posted 09-18 | — | [resources/timetable - Class0918.png](resources/timetable%20-%20Class0918.png) |
| Introduction to Computing | 1 | 📄 [summary](lectures/summaries/week01%20-%200_IntroductionToComputing.md) · [.pps](lectures/slides/week01%20-%200_IntroductionToComputing.pps) |

Weeks 2–3 have nothing on eClass — check GitHub and Telegram for those.

The week-1 deck is **Chapter 0** of the Naimi AVR textbook: memory types, the
three buses, address decoding, fetch–decode–execute, and **Von Neumann vs
Harvard** (the AVR is Harvard). Full summary linked above.

> The `.pps` is the **legacy binary PowerPoint format**. To open or re-extract:
> `soffice --headless --convert-to pptx "<file>"`, then
> `python scripts/extract_slides.py "<converted>.pptx"`.

## Tooling you will need

SimulIDE (hardware emulation) · ATmega development boards · AVR assembly ·
C/C++ toolchain. The syllabus also promises TinyML deployment later in the term.

## Folders

```
syllabus/    syllabus.md (readable) + soc3050.pdf (original)
lectures/    slides/ = the eClass intro deck + every deck from the slides site · summaries/ = .md notes
course-repo/ snapshot of github.com/gnoejh/soc3050code without tools/ (read-only, refreshed each sync)
labs/        clone the GitHub repo here to build and simulate (git-ignored)
homework/    assignments as they are set
resources/   timetable image, misc
my-notes/    your own notes
```
