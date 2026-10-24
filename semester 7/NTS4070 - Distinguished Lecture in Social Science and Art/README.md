# Distinguished Lecture in Social Science and Art

**Instructor:** Bobir Muratov, DSc · **Mode:** ONLINE · **Credits:** 2
**eClass course id:** `2592`

---

## Attendance

Attendance here is **20% of the grade** and is earned *only* by watching the
weekly VODs inside their open window. Videos cannot be mirrored into this
folder — they must be watched on eClass so the platform records the view.

---

## How this course distributes material

A weekly rhythm on eClass: one **slide deck** (`.pptx`), one or two **VODs**
(which carry attendance), and a **quiz**. Nothing lives outside eClass.

## Grading — no final exam

| Attendance | Quiz | Midterm | Debate | Total |
|---|---|---|---|---|
| 20% | 20% | 30% | 30% | 100% |

- **Midterm (week 8, offline)** covers the *Critical Thinking* chapters, weeks 1–7. **30 MCQ, 1% each, 1 hour**;
  ~30% fallacies (ch.5), ~60% ch.1/6/10/12, ~10% ch.2/4/11. Date not announced yet. See the
  [Midterm info summary](lectures/vod/week07%20-%20Midterm%20info.md).
  **Drill it with the flashcard game:** `python my-notes/midterm-quiz/quiz.py` (696 cards, all chapters,
  saves progress). See its [README](my-notes/midterm-quiz/README.md).
- **Debate (weeks 12–14, offline, on Saturdays)** is a group project worth 30%. Details to follow.
- Week 15 is a final week with **no exam**.

## Main textbook

Boss, J. A. *Think: Critical Thinking and Logic Skills for Everyday Life.*
McGraw-Hill. Chapters 1, 2, 4, 5, 6, 11 and 12 are the examinable set for the
midterm. Supplementary readings are listed in [syllabus/syllabus.md](syllabus/syllabus.md).

## Slide decks on hand

| Week | Topic | File |
|---|---|---|
| 1 | Introduction + Ch.1 Critical Thinking | [week01 - DLSSA 1](lectures/week01%20-%20DLSSA%201%20(class%20intro%20+%20lecture%201).pptx) |
| 2 | Ch.2 Reason & Emotion | [week02 - DLSSA 2](lectures/week02%20-%20DLSSA%202.pptx) |
| 3 | Ch.4 Knowledge, Evidence & Errors in Thinking | [week03 - DLSSA 3](lectures/week03%20-%20DLSSA%203.pptx) |
| 4 | Ch.5 Informal Fallacies | [week04 - DLSSA 4](lectures/week04%20-%20DLSSA%204.pptx) |
| 5 | Ch.6 Recognizing, Analyzing & Constructing Arguments | [week05 - DLSSA 5](lectures/week05%20-%20DLSSA%205.pptx) |
| 6 | Ch.10 Marketing & Advertising | [week06 - DLSSA 6.1](lectures/week06%20-%20DLSSA%206.1.pptx) |
| 6 | Ch.11 Mass Media | [week06 - DLSSA 6.2](lectures/week06%20-%20DLSSA%206.2.pptx) |
| 7 | Ch.12 Science | [week07 - DLSSA 7](lectures/week07%20-%20DLSSA%207.pptx) |

Slide-text summary of weeks 6–7 (and the debate-survey admin): [week06-07 slides md](lectures/week06-07%20-%20DLSSA%206.1,%206.2,%207%20(slides).md).

## Lecture videos, transcripts & summaries

All twelve VODs are mirrored to `lectures/vod/`. The **videos are git-ignored**;
the transcripts and summaries are tracked, so they survive a fresh clone and can
be searched or asked about without the media.

| Week | Lecture | Length | Chapter | Summary |
|---|---|---|---|---|
| 1 | Class intro | 18:09 | — (admin only) | [md](lectures/vod/week01%20-%20Class%20intro.md) |
| 1 | Lecture 1 | 44:35 | Ch.1 Critical Thinking | [md](lectures/vod/week01%20-%20Lecture%201.md) |
| 2 | Lecture 2 | 1:00:34 | Ch.2 Reason & Emotion | [md](lectures/vod/week02%20-%20Lecture%202.md) |
| 3 | Lecture 2-1 | 38:22 | Ch.4 Knowledge & Evidence (pt 1) | [md](lectures/vod/week03%20-%20Lecture%202-1.md) |
| 3 | Lecture 3-2 | 25:35 | Ch.4 Knowledge & Evidence (pt 2) | [md](lectures/vod/week03%20-%20Lecture%203-2.md) |
| 4 | Lecture 4 | 52:26 | Ch.5 Informal Fallacies | [md](lectures/vod/week04%20-%20Lecture%204.md) |
| 5 | Lecture 5 | 47:34 | Ch.6 Arguments: recognise, analyse, construct | [md](lectures/vod/week05%20-%20Lecture%205.md) |
| 6 | Debate survey | 8:11 | — (debate admin: survey due 10-23 12:00, prepare both sides) | [md](lectures/vod/week06%20-%20Debate%20survey.md) |
| 6 | Lecture 6-1 | 29:06 | Ch.10 Marketing & Advertising (**task: find a local ad with a fallacy**) | [md](lectures/vod/week06%20-%20Lecture%206-1.md) |
| 6 | Lecture 6-2 | 26:43 | Ch.11 Mass Media (**task: media-analyse a piece of local news**) | [md](lectures/vod/week06%20-%20Lecture%206-2.md) |
| 7 | Video 7 | 55:33 | Ch.12 Science (last lecture before the midterm) | [md](lectures/vod/week07%20-%20Video%207.md) |
| 7 | Midterm info | 3:19 | — (**midterm format and question split**; attendance-tracked, closes 10-25) | [md](lectures/vod/week07%20-%20Midterm%20info.md) |

Each summary carries a timestamp index, so you can jump from a claim back to the
exact passage in the `.txt`. Re-fetch or extend with:

```bash
python scripts/pull_vods.py && python scripts/transcribe_vods.py
```

> **Chapter 3 (language and communication) is skipped.** The sequence is
> 1 -> 2 -> 4. He kept one point from it as self-study: how language is used to
> manipulate.

## 🔴 Things stated only in the videos

None of these appear in the syllabus PDF or anywhere on eClass:

- **The 4th missed lecture is an automatic F.** You may miss at most **3** all semester. No excuses accepted — not illness, not travel.
- **Pass mark is 40%.**
- **Quizzes are effectively free marks.** Not multiple-choice, not findable online; they ask for your own opinions and experience. No right or wrong answers — he checks only that it is in your own words. ~5-10 minutes each, for 20% of the grade.
- **One quiz question was never posted to eClass at all** — he read it aloud at the end of Lecture 3-2 specifically so it could not be pasted into an AI. See that summary.
- **Do not contact him on Telegram or LinkedIn.** He refuses both. eClass message, email, or the TA.
- Debates are **on Saturdays**; topics and group format announced after the drop period.

**Check the last few minutes of every VOD** — that is where he puts the tasks.

## Quizzes and VODs (eClass only)

| Item | Week | Window | Link |
|---|---|---|---|
| Class intro VOD — 18m 09s | 1 | 09-05 → 09-13 | [open](https://eclass.inha.ac.kr/mod/vod/view.php?id=70109) |
| Lecture 1 VOD — 44m 35s | 1 | 09-05 → 09-13 | [open](https://eclass.inha.ac.kr/mod/vod/view.php?id=70112) |
| Quiz 1 | 1 | closed 09-14 | [open](https://eclass.inha.ac.kr/mod/quiz/view.php?id=70117) |
| Lecture 2 VOD — 1h 00m 34s | 2 | 09-12 → 09-20 | [open](https://eclass.inha.ac.kr/mod/vod/view.php?id=70704) |
| Lecture 2-1 VOD — 38m 22s | 3 | 09-19 → 09-27 | [open](https://eclass.inha.ac.kr/mod/vod/view.php?id=71123) |
| Lecture 3-2 VOD — 25m 35s | 3 | 09-19 → 09-27 | [open](https://eclass.inha.ac.kr/mod/vod/view.php?id=71124) |
| Quiz 2 | 3 | opened 09-20 18:27 | [open](https://eclass.inha.ac.kr/mod/quiz/view.php?id=71122) |
| Lecture 4 VOD | 4 | → 10-04 | [open](https://eclass.inha.ac.kr/mod/vod/view.php?id=71475) |
| Lecture 5 VOD · Quiz 3 | 5 | quiz → 10-11 23:59 | [VOD](https://eclass.inha.ac.kr/mod/vod/view.php?id=71777) · [quiz](https://eclass.inha.ac.kr/mod/quiz/view.php?id=71773) |
| Debate survey 8:11 · Lecture 6-1 29:06 · Lecture 6-2 26:43 · Quiz 4 | 6 | VODs 10-10 → 10-18 · quiz → 10-19 23:59 | [6-1](https://eclass.inha.ac.kr/mod/vod/view.php?id=72217) · [6-2](https://eclass.inha.ac.kr/mod/vod/view.php?id=72220) · [quiz](https://eclass.inha.ac.kr/mod/quiz/view.php?id=72222) |
| Video 7 55:33 · Midterm info 3:19 | 7 | 10-17 → **10-25 23:59** | [Video 7](https://eclass.inha.ac.kr/mod/vod/view.php?id=72441) · [Midterm info](https://eclass.inha.ac.kr/mod/vod/view.php?id=72743) |

Every VOD here is progress-tracked: watching it inside its window is that week's attendance.
Quizzes are 20% of this course, with one attempt each.

## Links

- [eClass course page](https://eclass.inha.ac.kr/course/view.php?id=2592)
- [Class announcements](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=69948) *(empty)*
- [Class Q&A board](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=69949)

## Folders

```
syllabus/    syllabus.md (transcribed) + the original PDF
lectures/    PPTX decks, prefixed by week
homework/    (no written homework in this course — debates and quizzes instead)
resources/   misc
my-notes/    your own notes
```
