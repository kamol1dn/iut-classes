# Artificial Intelligence midterm: open questions and hand calculations

Tue 2026-10-27, 14:00. Weeks 1–6 (1.1 → 6.2). Week 7 (DNN) is for the final.

The group chat says there are **open questions worth ~6 points**. Each answer below is short enough to
copy into your notebook (he checks it before the exam) and to write from memory in 3–5 minutes.
The full working is in the [lecture summaries](../lectures/summaries/).

---

## Part 1. Likely open questions

### 1. K-Means vs K-Means++ (the one classmates named)

- **They differ only in how the first K centroids are chosen.** After that, both run the same loop:
  assign each point to the nearest centroid, move each centroid to the mean of its points, and repeat
  until nothing changes.
- **K-Means** picks all K starting centroids **at random**. Different runs give different clusters, and a
  bad start can leave it stuck in a poor **local minimum**.
- **K-Means++** picks only the **first** centroid at random. For every point it computes D(x), the
  distance to the **nearest** centroid chosen so far, and picks the next centroid with probability
  **D(x)² / Σ D(x)²**. It repeats this until there are K centroids.
- **Effect:** the starting centroids are spread out, so K-Means converges **faster, to better clusters,
  and more consistently**. **Cost:** a slower initialisation, because every point's distance is
  recomputed for each new centroid.
- A chosen point has D = 0, so it can't be picked twice. The farthest point is only the **most likely**
  pick, not a guaranteed one.

### 2. How a decision tree is built (decision trees are "for sure" on the exam)

- Start with all the data at the root. For each attribute compute the **information gain**
  `IG(S, a) = E(S) − Σ (|Sᵥ|/|S|)·E(Sᵥ)`, where `E = −Σ p log₂ p`.
- Split on the attribute with the **largest IG**, which is the biggest drop in impurity. Repeat on each
  child until the nodes are pure, or until a stopping rule (max depth, min samples) kicks in.
- Entropy is 0 for a pure node and 1 for a 50/50 node. **Gini** `1 − Σ p²` is the CART alternative.
- ID3 uses entropy with multi-way splits. C4.5 adds continuous and missing values. CART uses Gini and
  binary splits, and does regression too.
- Deep trees **overfit**. Fix it by **pruning** or limiting the depth, or use a random forest.

### 3. Decision tree vs random forest

- A **random forest** is many trees. Each tree is trained on a **bootstrap sample** (rows drawn with
  replacement), and each split considers only a **random subset of features**.
- Prediction is a **majority vote** for classification and the **average** for regression.
- **Why it's better:** bagging lowers variance, and random features de-correlate the trees, so the
  forest overfits much less than one deep tree. **Cost:** slower, and harder to interpret.

### 4. PCA: what it is and its 5 steps

- **What:** dimensionality reduction. Replace p correlated features with fewer **uncorrelated** principal
  components that keep most of the **variance** (information).
- **Steps:** (1) centre each feature on its mean (standardise if the units differ) → (2) covariance
  matrix S, using 1/(n−1) → (3) eigenvalues from `det(S − λI) = 0` → (4) unit eigenvectors from
  `(S − λI)u = 0` → (5) sort λ in descending order, keep the top k, and project:
  `Z = X_centered · [u₁ … u_k]`.
- **Eigenvector = direction** of a PC, **eigenvalue = variance** along it. PC2 is perpendicular to PC1.
  Explained variance ratio = `λᵢ / Σλ`.
- **Cons:** PCs have no real-world meaning, and some information is lost. PCA is unsupervised, so it
  ignores y.

### 5. Choosing K: the elbow method

- Run K-Means for K = 1, 2, 3, … and plot **inertia** (the sum of squared distances to the cluster
  centroid) against K.
- Inertia always falls as K grows (K = n gives 0), so the minimum is useless. Pick the **elbow**, where
  adding another cluster stops reducing inertia by much.

### 6. K-Means challenges

- Choosing **K** (use the elbow method). Clusters of **different sizes and densities** get merged or
  split. **Outliers** pull the means (remove them, or use K-Medoids). **Random initialisation** gives
  different results on every run (use K-Means++). Always **scale the features** first, because K-Means
  uses Euclidean distance.

### 7. SVM: hard vs soft margin, C, and the kernel trick

- An SVM finds the hyperplane `w·x + b = 0` with the **maximum margin** `2/‖w‖`. Only the **support
  vectors** (the closest points) define it.
- **Hard margin:** minimise `½‖w‖²` subject to `yᵢ(w·xᵢ + b) ≥ 1`. This only works when the data is
  perfectly linearly separable, and it is very sensitive to outliers.
- **Soft margin:** add the hinge loss: `½‖w‖² + C·Σ max(0, 1 − yᵢ(w·xᵢ + b))`. A **large C** gives a
  narrow margin, few training errors, and a risk of overfitting. A **small C** gives a wide margin and a
  smoother boundary.
- **Kernel trick:** compute `K(x, x') = φ(x)·φ(x')` (polynomial, RBF, sigmoid) so the SVM separates
  non-linear data in a higher dimension without ever computing φ.
- **Logistic regression vs SVM:** LR is probabilistic and uses every point. SVM is geometric and uses
  only the support vectors.

### 8. KNN vs K-Means (easy to mix up)

- **KNN** is **supervised** classification: a new point takes the majority label of its k nearest
  labelled neighbours. It has no training step. Use an odd k for two classes, and scale the features.
- **K-Means** is **unsupervised** clustering: it groups unlabelled points into K clusters around
  centroids.
- The only thing they share is the letter K and the use of distance.

### 9. Naïve Bayes

- `P(class | x) ∝ P(class) · Π P(xᵢ | class)`. It is "naïve" because it assumes the features are
  **independent given the class**.
- Compute the score for each class, then normalise so they sum to 1, and pick the largest.
- **Zero-frequency problem:** a value never seen with a class gives P = 0, which wipes out the whole
  product. Fix it with **Laplace smoothing** (add 1 to every count).

### 10. Precision vs recall (and why accuracy misleads)

- `Precision = TP/(TP+FP)`: of the cases predicted positive, how many really are.
  `Recall = TP/(TP+FN)`: of the real positives, how many were caught. `F1 = 2PR/(P+R)`.
- When **false negatives are costly** (cancer screening) you want high recall. When **false positives are
  costly** (spam filtering) you want high precision.
- On **imbalanced** data accuracy is misleading: always predicting "no" on a 99/1 dataset scores 99%
  accuracy and 0 recall.

### 11. Missing data: MCAR / MAR / MNAR

- **MCAR:** missing for reasons unrelated to anything (a sensor drop-out).
- **MAR:** depends on **other observed** columns (older people skip the income question).
- **MNAR:** depends on **the missing value itself** (high earners hide their income). This is the hardest
  case.
- Fixes: drop rows, mean or median (median if skewed), mode for categories, KNNImputer, or
  IterativeImputer (MICE).

### 12. Data leakage and the golden rule

- **Fit on train, transform on test.** Scalers, imputers, encoders, PCA and SMOTE learn their parameters
  from the **training split only**. Split time series chronologically.

---

## Part 2. Hand calculations with check numbers

**Entropy and information gain (Play Tennis, 9 Yes / 5 No):**
E(S) = −(9/14)log₂(9/14) − (5/14)log₂(5/14) = **0.940**.
The gains: Outlook **0.247** (so it becomes the root), Humidity 0.151, Wind 0.048.
Under Outlook: Overcast 4/0 → Yes; Sunny 2/3 → split on Humidity; Rain 3/2 → split on Wind.
Slide 34's day {Sunny, High humidity, Hot, Weak wind} → Sunny → High → **No**.
Useful values: log₂(1/2) = −1, so E(1:1) = 1. E(4:0) = 0. E(2:3) = E(3:2) = 0.971 (slide 27 prints 0.966). E(5:2) = 0.863 (slide 26 prints 0.85).

**K-Means++ (points A(1,2) B(2,1) C(5,4) D(6,5) E(9,8), first centroid A):**
D² values = 0, 2, 20, 34, 100, which sum to 156, so P(E) = 100/156 = **0.641**.
With centroids A and E, the minimum D² values are 0, 2, 20, 18, 0, which sum to 40.
So P(C) = 0.50 and P(D) = 0.45: the third centroid is **C or D**. (Slide 23's 85 and 25 are typos for 98
and 32.)

**One K-Means iteration:** assign each point to its nearest centroid, then make each new centroid the
**mean** of its points. Example: {A, B, C} → (8/3, 7/3), {D, E} → (7.5, 6.5).

**PCA (slide 17; points (4,11) (8,4) (13,5) (7,14)):**
Means (8, 8.5). Covariance S = [[14, −11], [−11, 23]].
λ² − 37λ + 201 = 0 → λ₁ = **30.385**, λ₂ = 6.615. Check: λ₁ + λ₂ = trace = 37, λ₁·λ₂ = det = 201.
u₁ = (0.5574, −0.8303). PC1 = −4.305, 3.736, 5.693, −5.124. Explained variance = 30.385/37 = **82%**.
A sign flip of u₁ is also correct.

**Metrics:** with TP = 40, FP = 10, FN = 20: precision = 0.8, recall = 0.667, F1 = 0.727.
⚠️ The fruit confusion matrix in 3.1 (slides 17–25) mixes up its axes. The slides' official answers are
precision **0.667**, recall **0.8**, accuracy **70%**, F1 **0.73**. If the exam reuses it, check which axis
is "predicted" before you read off FP and FN.
R² = 1 − SS_res/SS_tot, where SS_tot = Σ(y − ȳ)². The R² formula on 3.1 slide 13 is wrong.

**Outliers and scaling:** IQR fences are Q1 − 1.5·IQR and Q3 + 1.5·IQR. z = (x − μ)/σ, and |z| > 3 is an
outlier. Min-max scaling is (x − min)/(max − min).

**SVM:** the margin is 2/‖w‖. For w = (3, 4), ‖w‖ = 5, so the margin is 0.4.
