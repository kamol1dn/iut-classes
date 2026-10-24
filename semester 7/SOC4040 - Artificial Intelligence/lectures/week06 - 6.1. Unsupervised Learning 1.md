# 6.1 — Unsupervised Learning 1: K-Means Clustering

**Artificial Intelligence · Week 6 · 38 slides · Dr. Oybek Eraliev**
Source: [week06 - 6.1. Unsupervised Learning 1.pdf](week06%20-%206.1.%20Unsupervised%20Learning%201.pdf) *(1.2 MB)*

Companion material:
- [K-Means.ipynb](../resources/K-Means.ipynb) is the deck's missing "Python Implementation" section: K-Means
  from scratch in NumPy on 3 blobs (compared with sklearn's `KMeans`), then K-Means++ initialisation from
  scratch, then an elbow plot of SSE vs K on a harder 5-blob dataset.

In scope for the midterm (Tue 10-27, weeks 1–6). Several slides are pictures only (13–15, 24–25,
29–35), so **open the PDF for those**. The contents slide lists "Python Implementation", but the deck
has no slides for it (37 is a question mark, 38 is "Thank you"). The notebook covers it.

## Outline

| Slides | Topic |
|---|---|
| 3 | **Clustering** = grouping similar objects. K-Means splits into a *predefined* K clusters; **hierarchical** clustering builds a tree instead (mentioned once, not covered) |
| 4–5 | K-Means is **centroid-based / distance-based**. Goal: minimise the (squared) distance from each point to its cluster's centroid |
| 7–9 | **The algorithm**: initialise → assign → update → repeat → output |
| 10 | Objective restated: points similar within a group, dissimilar across groups |
| 12 | Challenge 1: choosing **K**. Too small → under-clustering, too large → over-clustering |
| 13–16 | Challenge 2: clusters of **different sizes and densities**. K = 3 splits the big loose cluster and merges tight ones |
| 17 | Choosing K with the **elbow method** |
| 18 | Challenge 3: **outliers** pull centroids. Remove/transform them or use a robust variant |
| 19 | "Solutions": use a larger K (e.g. 10); random initialisation gives different results each run → **K-Means++** |
| 21–23 | **K-Means++** steps and a worked example on 5 points |
| 24–26 | K-Means++ in pictures. Costlier to initialise, but K-Means then converges faster and to better clusters |
| 28–30 | **Elbow curve**: x = number of clusters, y = inertia. Slide 30 circles the bend around K ≈ 6–10 |
| 31–35 | Picture walk-through of K-Means with K = 3: random centroids, assign, move, repeat until stable |

## The algorithm (slides 7–9)

1. **Initialisation**: pick K points from the data at random as the starting centroids.
2. **Assignment**: for every point, compute the distance to each of the K centroids and assign it to the
   **nearest** one.
3. **Update**: move each centroid to the **mean** of the points assigned to it.
4. **Repeat** 2–3 until **convergence**: centroids stop changing (significantly) or a maximum number
   of iterations is reached.
5. **Result**: final centroids plus the cluster label of every point.

The objective it minimises (written out on no slide; slides 3 and 5 describe it in words) is the
**within-cluster sum of squares**, which sklearn calls **inertia**:

    J = Σₖ Σ_{x ∈ Cₖ} ‖x − μₖ‖²          μₖ = mean of the points in cluster k

Not on the slides: each step can only lower J, so K-Means always converges, but only to a **local**
minimum that depends on the starting centroids. The notebook shows this directly. Random start with
seed 11 converges in 3 iterations at cost ≈ 611.6. Seed 42 gets stuck at ≈ 8980, a poor local
minimum. K-Means++ reaches ≈ 611.6 again.

## K-Means++ (slides 21–23)

The fix for random initialisation. Only the **first** centroid is uniformly random:

1. Pick the first centroid uniformly at random from the data.
2. For every point x compute **D(x)**, its distance to the **nearest** centroid chosen so far.
3. Pick the next centroid at random with probability **proportional to D(x)²**:
   `P(x) = D(x)² / Σ D(x)²`.
4. Repeat 2–3 until K centroids are chosen, then run normal K-Means.

### Worked example (slides 22–23), squared Euclidean distance

Points: A(1, 2), B(2, 1), C(5, 4), D(6, 5), E(9, 8). Suppose the first pick is **C₁ = A(1, 2)**.

| Point | D² to C₁ | P(chosen next) |
|---|---|---|
| A | 0 | 0 |
| B | (2−1)² + (1−2)² = 2 | 2/156 = 0.013 |
| C | (5−1)² + (4−2)² = 20 | 20/156 = 0.128 |
| D | (6−1)² + (5−2)² = 34 | 34/156 = 0.218 |
| E | (9−1)² + (8−2)² = 100 | 100/156 = **0.641** |

Sum = 156. E is the most likely, and the slide takes **C₂ = E(9, 8)**. Now D(x) is the distance to the
**nearer** of the two:

| Point | D² to C₁ | D² to C₂ (corrected, see below) | min | P(chosen 3rd) *(my numbers)* |
|---|---|---|---|---|
| A | 0 | 100 | 0 | 0 |
| B | 2 | **98** (slide: 85) | 2 | 2/40 = 0.05 |
| C | 20 | **32** (slide: 25) | 20 | 20/40 = **0.50** |
| D | 34 | 18 | 18 | 18/40 = **0.45** |
| E | 100 | 0 | 0 | 0 |

The slide's conclusion: **the third centroid will likely be C(5, 4) or D(6, 5)**. Points already chosen
have D = 0 and can never be picked again.

### My own practice: finish the job with K = 2

Not in the deck. Start K-Means from A and E:
- Assign: A, B, C are nearer A (C: 20 vs 32); D is nearer E (18 vs 34). Clusters {A, B, C}, {D, E}.
- Update: μ₁ = (8/3, 7/3) ≈ (2.67, 2.33), μ₂ = (7.5, 6.5).
- Re-assign: C → μ₁ (8.22 vs 12.5), D → μ₂ (4.5 vs 18.2). Nothing changes, so it has **converged**.
- Inertia = 13.33 + 9.00 = **22.33** (it was 40 with the initial centroids).

## Choosing K: the elbow method (slides 17, 28–30)

Run K-Means for K = 1, 2, 3, … and plot **inertia (sum of squared distances to the centroid)** against K.
Inertia always falls as K grows (K = n gives 0), so don't pick the minimum. Pick the **elbow**, where the
curve starts to level off and an extra cluster stops buying much. The notebook's 5-blob example picks K = 5.

## Challenges (slides 12–19)

| Challenge | What happens | Remedy given in the deck |
|---|---|---|
| Choosing K | Too small under-clusters, too large over-clusters | Elbow method |
| Different cluster sizes / densities | Tight groups get merged, a big loose group gets split | "Use a higher K" (see below) |
| Outliers | Means are pulled toward extreme values | Remove or transform them, or a robust variant |
| Random initialisation | Different clusters on every run | **K-Means++** |

Not on the slides but useful: K-Means uses Euclidean distance, so **scale the features** first
(see 5.2), and it assumes roughly round, similar-sized clusters. The robust variant the deck alludes to
is typically **K-Medoids** / **K-Medians**, which use a real data point or the median instead of the mean.

## Where the slides are loose

- **Slide 23's "dist² to C₂" column has two wrong values.** B(2, 1) to E(9, 8) is 7² + 7² = **98**, not 85.
  C(5, 4) to E(9, 8) is 4² + 4² = **32**, not 25. The `min` column and the conclusion (C or D next) are
  unaffected, because both distances to A are smaller anyway.
- **Slide 21, step 2** says distance "from the cluster center that has already been chosen", singular.
  Once there is more than one centroid it is the distance to the **nearest** chosen centroid, which is
  exactly what slide 23's `min` column does.
- **Slides 24–25** draw the next centroid as simply the farthest point. K-Means++ *samples* with
  probability ∝ D²: the farthest point is the most likely, not guaranteed. Likewise slide 23's choice of
  E is one random outcome (64% likely).
- **Slides 5 and 10** say "minimise the sum of distances". The objective is the sum of **squared**
  distances (slides 3 and 5 say so themselves). With plain distances the mean would not be the optimal
  centre.
- **Slide 19, "use a higher number of clusters, perhaps k = 10"**: loose. A bigger K always lowers
  inertia, but it chops the big cluster into pieces rather than recovering the real groups of different
  size or density. My note: the standard answers are a different algorithm, such as a Gaussian mixture
  model (unequal sizes/spreads) or DBSCAN (density-based).
- **Slide 17** sits under the "Solutions" heading but describes another challenge (finding K).
- **Slides 29–30**: the elbow plot's y-axis is not linear (1000, 500, 300, 200, 100, 50 are evenly
  spaced), so the curve looks flatter than the real drop.

## Try it

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
Xs = StandardScaler().fit_transform(X)
inertias = [KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=0).fit(Xs).inertia_
            for k in range(1, 11)]          # plot vs k and look for the elbow
km = KMeans(n_clusters=3, init="k-means++", n_init=10).fit(Xs)
km.labels_, km.cluster_centers_
```

`init="k-means++"` is sklearn's default. `n_init=10` reruns from 10 starts and keeps the lowest inertia,
another answer to the local-minimum problem.

## Exam checklist

- [ ] Define clustering; K-Means vs hierarchical in one line each
- [ ] The 5 steps of K-Means, including both stopping criteria
- [ ] Write the objective (sum of squared distances to the centroid / inertia)
- [ ] Run an assignment + update iteration by hand
- [ ] The 4 K-Means++ steps; compute D² and the selection probabilities for a small set
- [ ] Why K-Means++ beats random initialisation (and its cost)
- [ ] The elbow method: what is on each axis, and why not just take the lowest inertia
- [ ] Challenges: choosing K, unequal sizes/densities, outliers, random initialisation
