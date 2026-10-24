# 3.2 — Naïve Bayes and K-Nearest Neighbour

**Artificial Intelligence · Week 3 · 57 slides · Dr. Oybek Eraliev**
Source: [week03 - 3.2. Naive Bayes and KNN.pdf](../slides/week03%20-%203.2.%20Naive%20Bayes%20and%20KNN.pdf)

**Contents:** Bayes' theorem · the Naïve Bayes classifier (shopping example) ·
pros/cons · KNN · distance measures · choosing k · pros/cons.

The implementation slides (30–31, 55–57) are code screenshots with no text,
and no matching notebook was posted this week.

---

# Part A — Naïve Bayes

## 🎥 Watch: 3Blue1Brown

The professor recommended 3Blue1Brown in class. These are the videos that match this lecture ([full list](../../README.md#-3blue1brown-recommended-in-class)).

| Video | Length | Why it helps here |
|---|---|---|
| [Bayes theorem, the geometry of changing beliefs](https://youtu.be/HZGCoVF3YvM) | 15:11 | Bayes' theorem as areas, the picture behind section 1 |
| [The medical test paradox, and redesigning Bayes' rule](https://youtu.be/lG4VkPoG3ko) | 21:14 | priors and base rates, the trap in every Bayes question |

## 1. Bayes' theorem

```
P(A | B) = P(B | A) · P(A) / P(B)
```

| Term | Name |
|---|---|
| `P(A|B)` | **posterior**: probability of A given B happened |
| `P(B|A)` | **likelihood** |
| `P(A)` | **prior** |
| `P(B)` | **evidence** |

### Coin warm-up

Toss two coins, so the sample space is `{HH, HT, TH, TT}`.

- P(two heads) = 1/4 · P(at least one tail) = 3/4
- P(2nd = H | 1st = T) = 1/2 · P(two heads | 1st = H) = 1/2

With **A = second coin is heads** and **B = first coin is tails**:

```
P(A|B) = P(B|A)·P(A) / P(B) = (0.5 · 0.5) / 0.5 = 0.5
```

The coins are independent, so knowing B changes nothing. That's the point of
the example.

Where it sits: **supervised learning → classification → Naïve Bayes**.

## 2. The shopping example

**Task:** predict whether a customer **buys** from three features: **Day**
(weekday / weekend / holiday), **Discount** (yes/no) and **Free delivery**
(yes/no). There are 15 records: **10 buy, 5 don't**.

### Frequency → likelihood tables

| Day | Buy = Yes | Buy = No | Total |
|---|---|---|---|
| Weekday | 4 | 1 | 5 |
| Weekend | 2 | 2 | 4 |
| Holiday | 4 | 2 | 6 |
| **Total** | **10** | **5** | **15** |

| Discount | Yes | No | | Free delivery | Yes | No |
|---|---|---|---|---|---|---|
| Yes | 8 | 2 | | Yes | 9 | 2 |
| No | 2 | 3 | | No | 1 | 3 |

(Columns are Buy = Yes / Buy = No. Discount totals are 10 yes and 5 no.
Free-delivery totals are 11 yes and 4 no.)

Divide each cell by its column total to get likelihoods, e.g.
`P(Weekday | No) = 1/5`, `P(Discount = Yes | Yes) = 8/10`.

### One-feature calculation (slide 18)

```
P(No Buy | Weekday) = P(Weekday | No) · P(No) / P(Weekday)
                    = (1/5 · 5/15) / (5/15) = 0.20
```

Below 0.5, so a weekday customer most likely **buys**.

> ⚠️ **Slide 19's wording is muddled.** It calls 5/15 "the probability of
> purchasing on a weekday" and says "out of the **30** people … **10** of those
> purchases were made on weekdays." In the tables, 5/15 is simply
> **P(Weekday)**, there are **15** records, and **4** of the 10 purchases were
> on weekdays. The final 0.20 is right. Ignore the narrative on that slide.

### The full Naïve Bayes prediction

Query: **Day = Holiday, Discount = Yes, Free delivery = Yes.**

The "naïve" step: assume the features are **independent given the class**, so
the joint likelihood is a product:

```
P(No | B)  ∝ P(Disc=Y|No) · P(FD=Y|No) · P(Holiday|No) · P(No)
           = (2/5)(2/5)(2/5)(5/15)          = 0.0213

P(Yes | B) ∝ P(Disc=Y|Yes) · P(FD=Y|Yes) · P(Holiday|Yes) · P(Yes)
           = (8/10)(9/10)(4/10)(10/15)      = 0.192
```

The slides also divide both by `P(Disc=Y)·P(FD=Y)·P(Holiday) =
(10/15)(11/15)(6/15) = 0.1956`, giving **0.109** and **0.982**. Those two sum
to 1.09, not 1, because that denominator is itself computed under the
independence assumption. So he **normalises**:

```
P(Buy)    = 0.982 / 1.09 ≈ 90%
P(No Buy) = 0.109 / 1.09 ≈ 10%    → predict BUY
```

> **Exam shortcut:** the denominator is the same for every class, so you can
> skip it. Compare the two numerators (0.192 vs 0.0213) and normalise:
> 0.192 / 0.2133 = 90%. Same answer, less arithmetic.

All of his numbers check out.

## 3. Pros and cons

| Advantages | Disadvantages |
|---|---|
| Simple, easy to implement | **Independence assumption** rarely true in real data |
| Needs little training data | **Zero-frequency problem**: an unseen category gets P = 0 and wipes out the whole product. Fix it with **Laplace smoothing** |
| Handles continuous and discrete data | **Poorly calibrated probabilities**: good for ranking/classifying, not as true confidence |
| Scales well with features and data points | **Biased toward the majority class** on imbalanced data |
| Fast, OK for real-time prediction | |
| Not sensitive to irrelevant features | |

---

# Part B — K-Nearest Neighbour (KNN)

## 4. The idea

Predict a new point from the **k most similar training points**. Similar
things sit close together.

- **Non-parametric.** It learns no weights and just **memorises the training
  set**.
- **"Lazy" algorithm.** There's no training step. All the work, computing
  distances, happens at prediction time.
- **Classification:** majority vote of the k neighbours.
  **Regression:** average of their values.

## 5. Distance measures

| Distance | Formula | Use when |
|---|---|---|
| **Euclidean** | `√Σ(xᵢ − yᵢ)²` | Continuous features (height, weight, salary). **The default.** |
| **Manhattan** | `Σ|xᵢ − yᵢ|` | Grid-like movement, integer-valued features |
| **Minkowski** | `(Σ|xᵢ − yᵢ|ᵖ)^(1/p)` | The generalisation: **p = 1 → Manhattan, p = 2 → Euclidean** |

## 6. Worked example — iris by sepal size

Classify a new flower at **(sepal length 5.2, sepal width 3.1)** against 12
labelled flowers.

**Step 1: distances** (Euclidean). The first one:
`√((5.2−5.3)² + (3.1−3.7)²) = √0.37 = 0.608`.

**Step 2: rank them.** **Step 3: take the k nearest.** With **k = 3**:

| Rank | Sepal L | Sepal W | Species | Distance |
|---|---|---|---|---|
| 1 | 5.1 | 3.3 | Setosa | 0.22 |
| 2 | 5.4 | 3.4 | Setosa | 0.36 |
| 3 | 5.3 | 3.7 | Setosa | 0.608 |

3 of 3 are Setosa, so **the prediction is Setosa**. I re-computed all 12 distances and
ranks and they're correct. (The slides spell it "Vercicolor"; it's
*Versicolor*.)

## 7. Choosing k

- `k = 1` looks only at the single nearest point. `k = N` always predicts the
  dataset's majority class.
- **Small k overfits**: noisy, jagged boundary. **Large k smooths** and
  eventually underfits.
- His illustration: the same point is class **B at k = 3** but class **A at
  k = 6**.
- **How to pick it:** split train/test, plot error rate vs k, and take the
  **elbow point**, where raising k stops reducing error much. In his plot the
  error flattens after **k ≈ 5**.
- Tip that's not on the slide: for binary classification use an **odd k** so
  votes can't tie.

## 8. Pros and cons

| Advantages | Challenges |
|---|---|
| **Simple**, often the first classifier people learn | **Hard to scale**: stores all the data, and every prediction computes distances to everything |
| **Adaptable**: add training samples and predictions update immediately | **Curse of dimensionality**: in high dimensions distances become less meaningful, so accuracy drops |
| **Few hyperparameters**: just k and the distance metric | **Overfitting** when k is too low |

Not on the slides but it matters: **scale your features** before KNN. If one
feature is in thousands and another in fractions, the big one dominates every
distance.

## Exam checklist

- [ ] State Bayes' theorem and name prior / likelihood / evidence / posterior
- [ ] Explain what's "naïve" about Naïve Bayes
- [ ] Build a likelihood table from a frequency table
- [ ] Run the full shopping-style calculation and normalise
- [ ] Explain the zero-frequency problem and Laplace smoothing
- [ ] Why KNN is "lazy" and "non-parametric"
- [ ] Euclidean vs Manhattan vs Minkowski (which p gives which)
- [ ] Classify a point by hand with KNN for a given k
- [ ] Effect of small vs large k; the elbow method
- [ ] Curse of dimensionality
