# SOC3050 — Embedded Software & Design

**Instructor:** Jeong Hong · **Rooms:** B101 (Wed), B202 (Fri) · **Mode:** Offline
**Schedule:** Wed **15:00–16:30** (B101) · Fri **14:00–15:30** (**B202**)
⚠️ eClass registers Friday as `18~20` in B-101 — that is wrong; see [timetable.md](../timetable.md).
**eClass course id:** `2615`

---

## ⚠️ Read this first — most material is NOT on eClass

Same setup as SOC4180 (same professor): eClass carries the syllabus, a timetable
image and one intro deck. **The working material is on GitHub and Telegram.**

| Where | What | Link |
|---|---|---|
| **GitHub** | Course code, labs, examples | https://github.com/gnoejh/soc3050code |
| **Telegram** | Announcements, day-to-day comms | https://t.me/+EcqPs3qT0oZjYTI6 |
| eClass | Syllabus, timetable, week-1 deck | [course page](https://eclass.inha.ac.kr/course/view.php?id=2615) |

**Suggested:**

```bash
git clone https://github.com/gnoejh/soc3050code "labs/soc3050code"
```

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
| Introduction to Computing | 1 | 📄 [summary](lectures/week01%20-%200_IntroductionToComputing.md) · [.pps](lectures/week01%20-%200_IntroductionToComputing.pps) |

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
lectures/    decks posted on eClass, prefixed by week
labs/        clone the GitHub repo here
homework/    assignments as they are set
resources/   timetable image, misc
my-notes/    your own notes
```
