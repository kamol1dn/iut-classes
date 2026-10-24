# Deep Learning for Computer Vision

**Instructor:** Jeong Hong · **Room:** B-101 · **Mode:** Offline
**Schedule:** Mon **14:30–16:00** · Thu **12:00–13:30**
**eClass course id:** `2634`

---

## ⚠️ Read this first — most material is NOT on eClass

This is one of **Prof. Jeong Hong's two courses** (the other is Embedded Software), and he
runs both the same way: eClass holds only the syllabus and a timetable image.
**Everything you actually study lives outside eClass.**

| Where | What | Link |
|---|---|---|
| **GitHub** | Course code, labs, notebooks | https://github.com/gnoejh/soc4180 |
| **Slides site** | Lecture slides, published live | https://gnoejh.github.io/soc4180/ |
| **Telegram** | Announcements, day-to-day comms | https://t.me/+UHxHay2_c3kyMGQy |
| eClass | Syllabus PDF + timetable only | [course page](https://eclass.inha.ac.kr/course/view.php?id=2634) |

**Suggested:** clone the repo into `labs/` so lectures, labs and your work sit
together:

```bash
git clone https://github.com/gnoejh/soc4180 "labs/soc4180"
```

Then `git pull` there instead of re-downloading anything.

**Repo state at 2026-10-02:** all 15 weeks are now in `labs/soc4180/weeks/`
(weeks 11–15 were added on 09-27). On 09-28 every deck got a "maths pass" with
derivations and drawings. The current week is **04-walking**, and
**05-actuation** (PD control, gain windows, CPG rhythm) starts 10-03. Neither
README marks its lab as a graded game, unlike week 3's `moves.py`. Ask in class
or check Telegram before assuming they're ungraded.

---

## 📝 Midterm (30%, week 8, 26–30 Oct): study guide posted 10-19

The professor pushed a **student study guide** at 00:03 on 10-19:
[`labs/soc4180/weeks/exam_midterm/overview.md`](labs/soc4180/weeks/exam_midterm/overview.md) (1,148 lines).

- **33 MCQ, 60 min.** No notes, **no calculator**, no laptop. Every calculation is meant to be done by hand in under a minute.
- **Scope: weeks 0–6**: the five-layer stack, MuJoCo/MJCF, transforms and forward kinematics, the robot as code (2b),
  inverse kinematics, LIPM walking, actuation and PD control, sensing and state estimation.
- Each week has four parts: *ideas*, *maths*, *numbers worth knowing* (measured on the G1) and **traps**.
  The guide says the distractors are built from the traps.
- At the end there's a formula sheet ("memorise these"), a glossary and practice questions with answers.
- Same format as the Embedded Software guide. The exam paper and key are gitignored in the repo.

Also new on 10-19: **week 16, the cerebellum in a walking robot** (HTML deck in `weeks/16-cerebellum/`), linked from eClass
as URL 72641 *Cerebellum Robot*. That's after the midterm, so it isn't exam material.

---

## Grading

| Mid-term | Final | Attendance | Assignments | Quiz | Etc. |
|---|---|---|---|---|---|
| 30% | 30% | 5% | 30% | 0% | 5% |

**Assignments are 30%** — the labs are not optional. Per the syllabus, *no lab,
no project, no midterm or no final each individually mean failure*, as does
missing 8 classes.

## ⚠️ The registered syllabus contradicts itself

The objectives/description describe a **robotics course** (MuJoCo, Unitree G1
humanoid, locomotion policies). The weekly plan describes a **deep learning
fundamentals course** (neurons → transformers → diffusion → agents). Both are
reproduced in [syllabus/syllabus.md](syllabus/syllabus.md). The slides site is
the most reliable signal for what is actually being taught — check it before
relying on either reading.

## What is on eClass right now

| Item | Filed as |
|---|---|
| Syllabus (PDF) | [syllabus/soc4180.pdf](syllabus/soc4180.pdf) |
| Timetable image, posted 09-18 | [resources/timetable - Class0918.png](resources/timetable%20-%20Class0918.png) |

No lecture files, no assignments, no announcements posted on eClass as of
2026-09-20.

## Folders

```
syllabus/    syllabus.md (readable) + soc4180.pdf (original)
lectures/    (empty — slides live at gnoejh.github.io/soc4180)
labs/        clone the GitHub repo here
homework/    assignments as they are set
resources/   timetable image, misc
my-notes/    your own notes
```
