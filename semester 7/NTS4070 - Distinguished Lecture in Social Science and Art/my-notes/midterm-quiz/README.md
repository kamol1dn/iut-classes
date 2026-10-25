# Midterm flashcards

> *Ad hominem: attacking the person instead of the argument. Example: "whoever wrote this exam hates us."*

A terminal flashcard game for the Distinguished Lecture midterm (30 MCQ, 1 hour). It has **696 cards**
covering every examinable chapter. There's no 30-question cap: it keeps going until you quit.

| Exam share | Chapters | Cards |
|---|---|---|
| ~30% | Ch.5 Informal Fallacies | 220 |
| ~60% | Ch.1 Critical Thinking 68 · Ch.6 Arguments 67 · Ch.10 Marketing & Advertising 59 · Ch.12 Science 81 | 275 |
| ~10% | Ch.2 Reason & Emotion 73 · Ch.4 Knowledge & Evidence 86 · Ch.11 Mass Media 42 | 201 |

About 43% of the cards (299) are "spot it in a sentence" application questions, the kind the professor said
the fallacy questions will be.

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
python quiz.py 5
```
Only Chapter 5, the fallacies (~30% of the exam).

```bash
python quiz.py 1 6 10 12
```
Only the ~60% block.

```bash
python quiz.py --missed
```
Only cards you got wrong and haven't fixed yet.

```bash
python quiz.py stats
```
Per-chapter progress and your weakest topics.

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
- **Topics you keep missing** (e.g. *Red herring*) get extra weight, so you see more cards on them.
- **Chapters come up in their exam share** (30 / 60 / 10), however many cards each has. When one
  group runs out of new cards the others fill in, so all 696 get covered. To drill a low-share group
  on purpose, run `python quiz.py 2 4 11`.
- **Answer order is shuffled every time**, so you learn the answer, not the letter.

## The questions

`questions/*.json` holds one file per chapter group, each card linked to the lecture timestamp it comes
from. They were written from the slide decks, the VOD transcripts and their summaries. The lecture
wins where it differs from the textbook (e.g. his definition of *sound*); the explanation says so.
Where a lecture only listed a term, the textbook definition is used, marked `Textbook` in the source.
To add your own, append an object with the same fields; `choices[0]` is always the correct one.
