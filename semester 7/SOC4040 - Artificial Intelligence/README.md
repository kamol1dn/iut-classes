# SOC4040 — Artificial Intelligence

**Instructor:** Eraliev Oybek · **Room:** B-101 · **Mode:** Offline
**Schedule:** Mon **13:00–14:30** · Thu **14:00–15:30**
**eClass course id:** `2626`

---

## How this course distributes material

Everything comes through **eClass file posts**, organised by week: numbered PDF
decks (`1.1.`, `1.2.`, `2.1.` …) plus Jupyter notebooks for the hands-on parts.
This is the most self-contained of the six courses — eClass is enough.

**Plus a Discord server** (posted by the Education Assistant, Mamurov Jasurbek,
on 2026-09-17):

> https://discord.gg/tWQUXMpM7
> Requirement: set your **per-server nickname** to *Full name, Student ID*.

## Grading — per the week-1 deck, which overrides eClass

| Item | Weight | Detail |
|---|---|---|
| Attendance | 10% | **Medical certificates are not accepted.** 8+ absences = automatic F |
| Mid-term | 25% | Week 8 |
| Final | 25% | Week 15 |
| Homework | 20% | **Two assignments, 10% each** |
| Term project | 20% | Teams of 4-6 |
| **Extra points** | optional | up to **10 points** |

Exams are only 50% here — the lowest of any course this semester.

> 🔴 **"Taking note — checking before mid exam and final exam."** He inspects
> your notes before each exam. Keeping a written notebook is a requirement, not
> a suggestion.

## 🔴 Term project — dates that are not on eClass

- **Teams of 4-6 students**, end-to-end AI project.
- **Week 5 (3-9 Oct)** — choose a topic. Free choice but **must not duplicate another team's**. Fields: computer vision, NLP, generative AI.
- **Week 6 (10-16 Oct)** — submit the proposal.
- Prepare a report.
- **Week 14 (5-11 Dec)** — presentation, possibly moved to week 16.

Topic uniqueness is first-come, so forming a team early matters more than it looks.

**Office hours: Tuesday & Thursday, 14:00-15:30.** EA: Jasurbek Mamurov.

> ⚠️ His weekly plan in the deck **differs from the eClass syllabus** from week 4
> onward — he goes Clustering → Deep Learning → CNNs → Advanced CV, then NLP,
> Transformers, Generative Models, RL and Deep RL. SVM and object detection are
> not in his version. Full comparison in
> [the 1.1 summary](lectures/week01%20-%201.1.%20Intro%20to%20AI.md).

## Materials on hand

Each deck has a full summary beside it — read the `.md`, open the `.pdf` only
for the diagrams.

| Week | Lecture | Topic | Summary | Slides |
|---|---|---|---|---|
| 1 | 1.1 | Intro to AI - foundations, paradigms, LLMs, ethics | [md](lectures/week01%20-%201.1.%20Intro%20to%20AI.md) | [pdf](lectures/week01%20-%201.1.%20Intro%20to%20AI.pdf) |
| 1 | 1.2 | Linear regression, cost function, gradient descent | [md](lectures/week01%20-%201.2.%20Intro%20to%20Machine%20Learning.md) | [pdf](lectures/week01%20-%201.2.%20Intro%20to%20Machine%20Learning.pdf) |
| 2 | 2.1 | Multi-variable + polynomial regression, normal equation | [md](lectures/week02%20-%202.1.%20Intro%20to%20Machine%20Learning.md) | [pdf](lectures/week02%20-%202.1.%20Intro%20to%20Machine%20Learning.pdf) |
| 2 | 2.2 | Logistic regression, multi-class, regularization | [md](lectures/week02%20-%202.2.%20Logistic%20Regression.md) | [pdf](lectures/week02%20-%202.2.%20Logistic%20Regression.pdf) |
- [linear_regression.ipynb](resources/linear_regression.ipynb)
- [logistic_regression.ipynb](resources/logistic_regression.ipynb)

To run the notebooks:

```bash
pip install numpy pandas matplotlib scikit-learn jupyter
```

## Textbooks

- Russell & Norvig, *Artificial Intelligence: A Modern Approach* (Pearson, 2017)
- Géron, *Hands-On Machine Learning with Scikit-Learn and TensorFlow* (O'Reilly, 2023)
- Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* (CUP, 2021)

## Links

- [eClass course page](https://eclass.inha.ac.kr/course/view.php?id=2626)
- [Class announcements](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=69586)
- [Class Q&A board](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=69587)
- [Full syllabus](syllabus/syllabus.md)

## Folders

```
syllabus/    syllabus.md
lectures/    PDF decks, prefixed by week
homework/    assignments as they are set
resources/   practice notebooks
my-notes/    your own notes
```
