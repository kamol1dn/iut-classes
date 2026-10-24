# Blockchain — Homework 1 (5%)

**Due: Sun 2026-10-18, 23:55 by the eClass clock.** The PDF says 23:59, but the
eClass page says 23:55, and he said in lecture that the LMS clock is the only one
that counts. Submit on [eClass, assignment 71837](https://eclass.inha.ac.kr/mod/assign/view.php?id=71837).

Files: [SOC4190 Homework 1.pdf](SOC4190%20Homework%201.pdf) (the handout, 6 pages) ·
[SOC4190 Homework 1 Template.docx](SOC4190%20Homework%201%20Template.docx) (write the report in this)

> **His rules, from the eClass page:** don't copy. If a submission looks
> suspicious, he calls you in to explain your code out loud, and that
> conversation decides the mark. If you can't do a task, **skip it**: an honest
> gap costs a few points, while a copied answer costs the whole assignment. Use
> only what the course has taught.

## What you hand in

```
SOC4190_HW1_<StudentID>_<Surname>.zip
├── report.pdf        answers + screenshots + photos of handwriting
└── src/
    ├── blockhash.py  Part 3.3, typed by you (not pasted)
    └── header.hex    Part 3.3, the header of your block
```

## Your own numbers (from your student ID)

Write these at the top of the report. Every task uses them.

| Name | Rule |
|---|---|
| Block height **H** | last five digits |
| Leaves **L1 L2 L3 L4** | last four digits, each + 10 |
| Key **K** | last digit + 3 |
| Amount **A** | second-to-last digit × 5 + 10 |

Check these against the handout's table before relying on them. A wrong H
makes every screenshot in Part 2 worthless.

## Ground rules that cost marks

- **Screenshots:** your student ID must be visible in the command, or the block height
  must be your H. Show the whole window, including the browser address bar on
  the explorer. Use the screenshot tool, **never a phone photo of the screen**.
- **✍ exercises are handwritten on paper**, with your name and ID on every sheet,
  then photographed or scanned. **Typed versions score zero.** Show every
  step of the arithmetic.
- Number the answers exactly as the handout does (1.1, 2.3 …).

## Checklist

| Part | Points | Needs | Lecture |
|---|---|---|---|
| **1** The ledger: 1.1 ✍ balances table, 1.2 double spend, 1.3 centralised/distributed table | 15 | paper | Intro Parts 1–2 (week 3, summarised in `lectures/vod/`) |
| **2** Your block on mempool.space: 2.1 header fields, 2.2 ✍ Unix time → date, 2.3 ✍ draw H−1, H, H+1, 2.4 block timing | 20 | browser + paper | "Bitcoin: Where It Came From, and What a Block Is" (week 4) |
| **3** SHA-256: 3.1 one-character change, 3.2 output size, 3.3 **compute your block's hash in Python**, 3.4 ✍ toy hash | 25 | terminal + Python + paper | "Cryptography for Blockchains" (week 4) |
| **4** ✍ Merkle trees with T(a,b) = (31a + b) mod 97: build, change a leaf, proof, 5 leaves, proof length | 25 | paper only | Cryptography (week 4) |
| **5** Keys: 5.1 ✍ Caesar, 5.2 private/public table, 5.3 three short answers | 15 | paper + typing | Cryptography (week 4) |

That's about a dozen handwritten exercises, so budget an evening for Part 4 alone.

## Tooling on this machine

- **Terminal for Part 3:** Git Bash works. The handout writes `shasum -a 256`.
  If Git Bash doesn't have `shasum`, use `sha256sum`, which the handout allows.
  Use `printf`, **not** `echo`, because echo adds a newline and changes the hash.
- **Python:** `python` here (the handout writes `python3`). Either is fine,
  as long as the screenshot shows the command you actually ran.
- mempool.space and its `/api/block/<hash>` endpoint are public, so no login is needed.

## Lecture material

The handout's "Lecture 3" and "Lecture 4" are the two week-4 videos, both now summarised.
Each summary marks which homework question each section feeds:

- [Bitcoin: Where It Came From, and What a Block Is](../../lectures/summaries/vod/week04%20-%20Bitcoin%20-%20Where%20It%20Came%20From,%20and%20What%20a%20Block%20Is.md): Part 2
  (header fields, Unix time by hand, drawing the chain, block rhythm)
- [Cryptography for Blockchains](../../lectures/summaries/vod/week04%20-%20Cryptography%20for%20Blockchains.md): Parts 3–5
  (the hash-function promises by name, double SHA-256, Merkle trees and proofs, Caesar, keys)
- Part 1 comes from the two week-3 intro lectures in the same folder.
