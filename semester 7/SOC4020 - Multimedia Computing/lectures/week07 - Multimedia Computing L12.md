# L12: Pattern Classification

**Multimedia Computing · Week 7 · 51 slides · Dr. Minhaz Uddin Ahmed**
Source: [week07 - Multimedia Computing L12.pptx](week07%20-%20Multimedia%20Computing%20L12.pptx) *(3.8 MB)*

Gonzalez **chapter 12** plus Duda, Hart & Stork, *Pattern Classification*, **chapter 1**. The
whole "sea bass vs salmon" thread is Duda's opening example, almost slide for slide. This is a short,
concept-heavy deck. About a third of the slides (7, 10, 13, 16, 18, 21, 33–35, 43–48) are pictures
only, so **open the pptx for the fish histograms and the template-matching formula on slide 35**.

This is the first lecture after the filtering/edges block. It moves from processing images to
*recognising* what is in them, and it overlaps heavily with Artificial Intelligence weeks 2–3
(KNN, Naïve Bayes, evaluation).

## Outline

| Slides | Topic |
|---|---|
| 3 | Vocabulary: a **pattern** is an arrangement of descriptors; a descriptor is also called a **feature**; a **pattern class** is a family of patterns sharing common properties |
| 4–7 | Running example: sort **sea bass vs salmon** on a conveyor with a camera. Candidate features: length, lightness, width, number/shape of fins, mouth position. Pipeline: **segment** each fish → **feature extractor** → **classifier** |
| 8–11 | **Length alone is a poor feature.** Lightness separates better. Moving the threshold trades one error for the other, so pick it by **cost** (here: fewer sea bass sold as salmon). That trade-off is the job of **decision theory** |
| 12–14 | Use two features, `xᵀ = [x₁, x₂]` = (lightness, width), and the boundary becomes a line in 2-D. Adding more features helps only if they aren't **noisy/redundant** |
| 14–16 | A boundary that wraps every training fish perfectly is the "best" on training data, but the real goal is **novel input**: the issue of **generalization** (i.e. overfitting) |
| 17–19 | Stages of a PR system: **sensing** (transducer), **segmentation & grouping**, **feature extraction** (discriminative, invariant to translation/rotation/scale), **classification**, **post-processing** (use context) |
| 20–27 | **Design cycle**: data collection → feature choice → model choice → training → evaluation, with computational complexity as the constraint throughout |
| 28 | **Supervised** (a teacher gives a label or cost per training pattern) vs **unsupervised** learning (the system finds clusters / natural groupings) |
| 29–30 | **Statistical** PR (data → vectors of numbers → statistics) vs **structural** PR (data → grammar or graph → parsing, graph matching) |
| 31–32, 36 | Definitions: class, **feature extractor**, **classifier**, the **reject class**. Feature vector `X = [x₁ … xₙ]`, e.g. `[#holes, #strokes, moments, …]` for characters |
| 33–35 | Character recognition: candidate features, then **template matching** (formula is an image on slide 35) |
| 37 | **Discriminant functions** `f(x, K)`: compute a score per class from the feature vector plus knowledge K, then pick a class |
| 38–40 | **Nearest class mean** with Euclidean distance; reject if not close enough. Fails when a class is **multi-modal** (fix: one mean per mode). **Scale by each class's σ** per dimension |
| 41 | **Nearest neighbour**: keep all training samples, give the class of the closest one; extends to **k-NN** |
| 42 | **Bayesian decision-making** (formulas below) |
| 43–48 | Examples as pictures: Iris flowers, Bayes classification of multispectral image data, noisy objects, object recognition |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Nearest class mean | choose the class `c` minimising `‖x − x_c‖`; reject if the smallest distance is still too large |
| Scaled Euclidean distance (slide 40) | `‖x − x_c‖ = √( Σᵢ ((x[i] − x_c[i]) / σᵢ)² )` where `σᵢ` is class *c*'s spread along dimension *i* |
| What the three distributions are (slide 42) | **class-conditional** `p(x\|ωᵢ)`, **prior** `P(ωᵢ)`, **unconditional (evidence)** `p(x)` |
| Bayes rule (slide 42) | `P(ωᵢ\|x) = p(x\|ωᵢ)·P(ωᵢ) / p(x) = p(x\|ωᵢ)·P(ωᵢ) / Σⱼ p(x\|ωⱼ)·P(ωⱼ)` |
| Bayes decision | pick the class with the largest **posterior** `P(ωᵢ\|x)`. `p(x)` is the same for every class, so comparing `p(x\|ωᵢ)·P(ωᵢ)` is enough |

Why scaling matters (slide 40's own example): a point near the top of a widely spread Class 3 can be
nearer Class 2's mean in plain distance, but nearer Class 3's mean once each axis is divided by that
class's σ.

## Things that are wrong or loose in the deck

- **Slide 14's wording is muddled.** It says to add features "that are not correlated with the ones
  we already have", then warns against "such noisy features", as if the uncorrelated ones were the
  noisy ones. The intended point: a new feature should bring *new* information (so, uncorrelated), but
  a feature that is mostly noise can make the classifier worse.
- Slide 17 says segmented patterns "should not overlap". That's the goal, not a guarantee.
  Segmentation is one of the hardest steps precisely because real objects touch and overlap.
- Slide 42 says to use Bayes' rule "if all of the classes ωᵢ are disjoint". The real conditions are
  that the classes are **mutually exclusive and exhaustive**, which is what lets `p(x)` expand into
  the sum in the denominator.
- Slides 14–16 never use the word *overfitting*, but that's what "Issue of generalization!" is about.
  Expect either term on an exam.

## Links to other courses

- **Artificial Intelligence 3.2** covers Naïve Bayes and KNN with worked numbers. If slide 41–42
  feel thin, read those decks.
- **Artificial Intelligence 3.1**: evaluation metrics, which is the "Evaluation" step of the design cycle here.
