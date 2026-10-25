# Midterm flashcards

> *If the residual doesn't shrink with more iterations, it's a geometry problem. Same goes for my grades.*

A terminal flashcard game for the Deep Learning for Computer Vision midterm ("Robot and AI", 33 MCQ, 60 min, no
calculator). It has **600 cards** covering weeks 0–6. There's no 33-question cap: it keeps going until you quit.

| Week | Topic | Cards |
|---|---|---|
| 0 | The five-layer robot stack | 61 |
| 1 | MuJoCo and MJCF | 86 |
| 2 | Transforms and forward kinematics | 93 |
| 2b | The robot as code | 50 |
| 3 | Inverse kinematics | 65 |
| 4 | Balance and LIPM walking | 83 |
| 5 | Actuation and PD control | 81 |
| 6 | Sensing and estimation | 81 |

About a quarter of the cards (153) are **hand calculations with fresh numbers**, the kind the exam asks without
a calculator. About a fifth (116) are built on the **traps** in the professor's study guide, which he says the
exam's wrong options come from.

```bash
python quiz.py
```

Or double-click `quiz.bat`.

## Keys

| On a question | |
|---|---|
| `a` `b` `c` `d` (or `1`–`4`) | answer, then see right/wrong plus the explanation |
| **Enter** | don't know, so show the answer and explanation |
| `q` | quit |

| After the answer | |
|---|---|
| **Enter** | next card |
| `k` | typo, I knew it: count it as right |
| `q` | quit |

In the Windows console, Windows Terminal or the VS Code terminal, one keypress is enough. In Git Bash,
type the key and press Enter.

## Picking what to drill

```bash
python quiz.py 4
```
Only week 4, walking. `2` gives weeks 2 and 2b together.

```bash
python quiz.py 5 6
```
Several weeks.

```bash
python quiz.py --missed
```
Only cards you got wrong and haven't fixed yet.

```bash
python quiz.py stats
```
Per-week progress and your weakest topics.

```bash
python quiz.py reset
```
Start over (asks first).

## How it decides what to ask

Progress is written to `progress.json` after **every** card, so `q`, Ctrl+C or closing the window loses
nothing. The file is git-ignored.

- **Right on the first try:** the card jumps to a high box and comes back only after ~60 other cards.
  Right again, and it's *mastered*: it shows up rarely, never zero.
- **Wrong, or Enter to reveal:** box 0. It comes back after ~4 cards, then climbs a box each time you
  get it right.
- **Topics you keep missing** (e.g. *Capture point*) get extra weight, so you see more cards on them.
- **Weeks come up in a guessed exam share** (week 2+2b 20%, weeks 1 and 4 15%, 5 and 6 14%, 3 12%, 0 10%).
  The professor gave no split, so this follows how much of his guide each week fills.
- **Answer order is shuffled every time**, so you learn the answer, not the letter.

## The questions

`questions/*.json` holds one file per week. They were written from the professor's
[study guide](../../course-repo/weeks/exam_midterm/overview.md) (the primary source: every idea, formula,
number and trap in it has a card) and, at lower density, from the week decks (`course-repo/weeks/*/slides.qmd`).
Every calculation was checked in Python. Where the slides and the guide differ, the cards follow the guide.
The guide's 19 practice questions are in here too, rephrased as multiple choice.
To add your own, append an object with the same fields; `choices[0]` is always the correct one.
