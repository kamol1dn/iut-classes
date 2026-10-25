# Multimedia Computing

**Instructor:** Minhaz Uddin Ahmed · **Room:** B-101 · **Mode:** Offline
**Schedule:** Tue **09:30–11:00** · Wed **13:00–14:30**
**eClass course id:** `2622`

---

## How this course distributes material

Straight **eClass file posts** — PowerPoint decks numbered `L1`, `L2`, `L3` …
placed under the week they were posted, plus occasional `.rar` archives of
practice code. No external GitHub, Telegram or Discord for this one.

Note the lecture numbering runs ahead of the week numbering: L1 **and** L2 were
both posted in week 1, and L3, L3-practice-code and L4 all in week 2.

## Grading — the week-1 deck adds an item eClass omits

> *My GPA after this course: lossy compression.*

| Item | Weight |
|---|---|
| Mid-term | 30% |
| Final | 30% |
| Assignment | 15% |
| **Quiz** | **20%** |
| Attendance | 5% |
| **+ class activity** | **10%** |

**Quizzes are 20%** — by far the heaviest quiz weight of the six courses, and
they are announced in class. **Late homework will not be accepted**, says the
deck. Assignment 1's doc softens that to a sliding penalty for up to 24 h; see its brief.

> The deck's list sums to **110%**, so the class-activity 10% is presumably
> bonus. eClass lists the same first five items totalling 100% and no
> class-activity line. Either way, **speaking up in class is worth marks here**,
> which is not true of your other courses.

**Assignments are Python programming** — stated explicitly on slide 3.

> ⚠️ **Exam weeks disagree.** His deck puts the **midterm in week 8**, the
> **final in week 15**, and a **review class in week 16**. eClass puts the final
> in week 16. His plan also swaps most of the post-midterm compression material
> for **computer graphics and ray tracing** in weeks 9-10. Full comparison in
> [the L1 summary](lectures/summaries/week01%20-%20Multimedia%20Computing%20L1.md).

Per the syllabus, homework falls in **weeks 2, 9, 10 and 12**. In practice the
first one arrived on eClass in week 5:

> 📝 **[Assignment 1](homework/assignment1/) is due Sun 2026-10-25 23:55** (15 points).
> It's six Python scripts (audio waveform + compression, log transform + Sobel, video
> downscale + blur) plus `requirements.txt`, auto-graded against reference
> outputs with a strict library whitelist. The doc contradicts itself in a few
> places, so read the brief and email the TA before writing the image tasks.

## Materials on hand

Each deck has a full summary beside it — read the `.md`, open the `.pptx` only
for the diagrams.

| Week | Deck | Topic | Summary | Slides |
|---|---|---|---|---|
| 1 | L1 | Intro to multimedia, image processing, CV survey | [md](lectures/summaries/week01%20-%20Multimedia%20Computing%20L1.md) | [pptx](lectures/slides/week01%20-%20Multimedia%20Computing%20L1.pptx) *(25 MB)* |
| 1 | L2 | Sound, A/D conversion, sampling, **Nyquist & aliasing** | [md](lectures/summaries/week01%20-%20Multimedia%20Computing%20L2.md) | [pptx](lectures/slides/week01%20-%20Multimedia%20Computing%20L2.pptx) |
| 2 | L3 | SNR, SQNR, audio filtering, **MIDI**, PCM | [md](lectures/summaries/week02%20-%20Multimedia%20Computing%20L3.md) | [pptx](lectures/slides/week02%20-%20Multimedia%20Computing%20L3.pptx) |
| 2 | L4 | **Entropy, RLC, Shannon-Fano, Huffman, LZW** | [md](lectures/summaries/week02%20-%20Multimedia%20Computing%20L4%20(update).md) | [pptx](lectures/slides/week02%20-%20Multimedia%20Computing%20L4%20(update).pptx) |
| 3 | L5 | **Arithmetic coding**, lossy compression, psychoacoustics, **MP3 / AAC** | [md](lectures/summaries/week03%20-%20Multimedia%20Computing%20L5.md) | [pptx](lectures/slides/week03%20-%20Multimedia%20Computing%20L5.pptx) |
| 3 | L6 | Image fundamentals, **intensity transforms, gamma, histogram equalization** | [md](lectures/summaries/week03%20-%20Multimedia%20Computing%20L6.md) | [pptx](lectures/slides/week03%20-%20Multimedia%20Computing%20L6.pptx) *(10 MB, diagram-heavy)* |
| 4 | L7 | **Pixel neighbours, connectivity, distance metrics**, radiometry vs photometry, **CIE XYZ & chromaticity** | [md](lectures/summaries/week04%20-%20Multimedia%20Computing%20L7.md) | [pptx](lectures/slides/week04%20-%20Multimedia%20Computing%20L7.pptx) |
| 4 | L8 | MATLAB / Octave / Colab for image processing (tooling) | [md](lectures/summaries/week04%20-%20Multimedia%20Computing%20L8%20(Matlab-Octave).md) | [pptx](lectures/slides/week04%20-%20Multimedia%20Computing%20L8%20(Matlab-Octave).pptx) *(code screenshots)* |
| 5 | L9 | Point processing: **LUTs, histogram equalization & specification**, arithmetic/logic ops (deepens L6) | [md](lectures/summaries/week05%20-%20Multimedia%20Computing%20L9.md) | [pptx](lectures/slides/week05%20-%20Multimedia%20Computing%20L9.pptx) |
| 5 | L10 | **Morphology**: structuring elements, dilation/erosion, opening/closing, hit-or-miss, boundary, skeletons, top-hat | [md](lectures/summaries/week05%20-%20Multimedia%20Computing%20L10.md) | [pptx](lectures/slides/week05%20-%20Multimedia%20Computing%20L10.pptx) |
| 6 | L11 | **Spatial filtering & edges**: convolution, borders, blur/Gaussian, sharpen/unsharp/high-boost, Roberts/Prewitt/Sobel, compass, Laplacian + zero crossings, LoG/DoG, colour edges, median/min/max | [md](lectures/summaries/week06%20-%20Multimedia%20Computing%20L11.md) | [pptx](lectures/slides/week06%20-%20Multimedia%20Computing%20L11.pptx) |
| 7 | L12 | **Pattern classification**: features and pattern classes, sea bass vs salmon, decision boundaries and cost, generalization, PR design cycle, nearest class mean (σ-scaled), nearest neighbour / k-NN, **Bayes rule** | [md](lectures/summaries/week07%20-%20Multimedia%20Computing%20L12.md) | [pptx](lectures/slides/week07%20-%20Multimedia%20Computing%20L12.pptx) |
| 7 | L13 | **Image compression** (Gonzalez ch. 8): compression ratio and redundancy, the three redundancies, run-length coding, DCT and the JPEG steps, quality measures. New topic, not a continuation of L12. ⚠️ The run-length demo computes the ratio upside down | [md](lectures/summaries/week07%20-%20Multimedia%20Computing%20L13.md) | [pptx](lectures/slides/week07%20-%20Multimedia%20Computing%20L13.pptx) |

Plus [practice code L3.rar](resources/practice%20code%20L3.rar) — extract before use.
Week 4 practice: [Lecture7.ipynb](resources/Lecture7.ipynb) (sRGB → XYZ),
[practice code L8 - experiment.txt](resources/practice%20code%20L8%20-%20experiment.txt) (MATLAB snippets) with
[300cat.jpeg](resources/300cat.jpeg) / [300dog.jpeg](resources/300dog.jpeg).

**L2 and L4 are the exam-dense ones.** L1 is a survey; L3 and L4 carry the
formulas and algorithms you will be asked to reproduce.

> 🟡 **An exercise buried in L4's speaker notes:** write your first name as a
> string, apply Huffman coding, and draw the binary tree. It is the best
> preparation for the likely exam question and takes five minutes.

> ⚠️ **L7 slide 22 defines 8-connectivity with N4(p).** It should be **N8(p)**.
> L8's image-add snippet also has a broken size check. Both are explained in the summaries.

> ⚠️ **L5's arithmetic-encoder pseudocode is buggy.** It computes `high` from the
> already-updated `low`. Trust the worked `CAEE$` table instead; the L5
> summary spells out the correct order.

## Textbooks

- Gonzalez, *Digital Image Processing* (Pearson, 2012)
- Ze-Nian Li, *Fundamentals of Multimedia* (Springer, 2006)
- Szeliski, *Computer Vision* (Springer, 2015)

## Links

- [eClass course page](https://eclass.inha.ac.kr/course/view.php?id=2622)
- [Class announcements](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=70064)
- [Class Q&A board](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=70065)
- [Full syllabus](syllabus/syllabus.md)

## Folders

```
syllabus/    syllabus.md
lectures/    slides/ = PPTX decks, prefixed by the week posted · summaries/ = .md notes
homework/    assignments as they are set (assignment1/ = Assignment 1)
resources/   practice code archives
my-notes/    your own notes
```
