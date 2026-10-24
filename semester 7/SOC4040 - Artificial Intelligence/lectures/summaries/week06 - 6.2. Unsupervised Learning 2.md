# 6.2 — Unsupervised Learning 2: Principal Component Analysis (PCA)

**Artificial Intelligence · Week 6 · 19 slides · Dr. Oybek Eraliev**
Source: [week06 - 6.2. Unsupervised Learning 2.pdf](../slides/week06%20-%206.2.%20Unsupervised%20Learning%202.pdf) *(0.8 MB)*

Companion material:
- [PCA.ipynb](../../resources/PCA.ipynb) works the slide-17 example in NumPy step by step (with a plot of PC1
  and the projections), wraps it in a from-scratch `PCA` class, then cuts an 800-feature synthetic
  dataset to 50 components. Linear SVM accuracy rises from 0.73 to 0.805, random forest from 0.745 to 0.785.

In scope for the midterm (Tue 10-27, weeks 1–6). The deck is short. The **hand calculation on slide 17**
is the obvious exam question, and its full working (which the slide skips) is below. The formulas on
slides 14–16 are images, so **open the PDF for those**.

## Outline

| Slides | Topic |
|---|---|
| 4–5 | PCA = **dimensionality reduction**: turn many variables into fewer that keep most of the information. Trade a little accuracy for simplicity |
| 6 | Principal components are **linear combinations** of the original variables, **uncorrelated**, with as much information as possible packed into the first ones. 10-D data → 10 PCs |
| 7 | Keep the high-information components and drop the rest. Bar chart of % explained variance per PC (a scree plot). PCs are **hard to interpret** |
| 8 | Geometrically, PCs are the **directions of maximum variance**. More variance = more spread = more information |
| 10–11 | PC1 is the line through the origin along which the projected points are **most spread out**, i.e. maximum variance |
| 12 | PC2: same, but **uncorrelated with (perpendicular to)** PC1, and it takes the next-highest variance. Continue until p PCs = number of variables |
| 14–16 | **The 5 steps**: mean → covariance matrix → eigenvalues → eigenvectors → project |
| 17 | Worked example: 4 points in 2-D → first principal component |

## The ones to memorise

| Thing | Rule |
|---|---|
| Goal | Reduce the number of variables while keeping as much **variance** (information) as possible |
| Principal component | A new axis: a linear combination of the original features. PCs are orthogonal and their scores are uncorrelated |
| PC1 | The direction of **maximum variance**. PC2 the next, perpendicular to PC1, and so on |
| How many | p features → p PCs. Keep the first k |
| Eigenvector of S | The **direction** of a PC |
| Eigenvalue λ | The **variance** along that PC. Sort descending: largest λ = PC1 |
| Explained variance ratio *(my addition)* | `λᵢ / Σλ` (the bars on slide 7). Keep enough PCs to reach e.g. 90–95% |
| Downside | PCs have no real-world meaning, so the model gets harder to interpret |

## The 5 steps (slides 14–16)

For m samples with p features (the slide uses m and n for the same count):

1. **Mean** of each feature: `x̄ = (Σᵢ xᵢ) / m`, then centre the data: `X_centered = X − x̄`.
2. **Covariance matrix** (p × p, symmetric):

       S = [ Cov(X₁,X₁)  Cov(X₁,X₂) ]        Cov(x, y) = 1/(n−1) · Σᵢ (xᵢ − x̄)(yᵢ − ȳ)
           [ Cov(X₂,X₁)  Cov(X₂,X₂) ]

   The diagonal holds the variances.
3. **Eigenvalues**: solve `det(S − λI) = 0`, where I is the identity matrix.
4. **Eigenvectors**: solve `(S − λI) U = 0` for each λ, with `U = [u₁, u₂]ᵀ`. Scale U to **unit length**.
5. **Project** the centred data onto the eigenvector of the largest λ: `PC1 = X_centered · u₁`
   (the slide writes `X_centeredᵀ · u₁`, see below). For k components, multiply by the p × k matrix
   of the top-k eigenvectors.

## Worked example (slide 17), full working

The slide gives only the data and the answer. These intermediate steps are mine, and they reproduce the
slide's answer and the notebook's output.

| Point | X₁ | X₂ |
|---|---|---|
| 1 | 4 | 11 |
| 2 | 8 | 4 |
| 3 | 13 | 5 |
| 4 | 7 | 14 |

**Step 1: means.** x̄₁ = (4 + 8 + 13 + 7)/4 = **8**, x̄₂ = (11 + 4 + 5 + 14)/4 = **8.5**.
Centred: (−4, 2.5), (0, −4.5), (5, −3.5), (−1, 5.5).

**Step 2: covariance** (divide by n − 1 = 3):
- Cov(X₁,X₁) = (16 + 0 + 25 + 1)/3 = **14**
- Cov(X₂,X₂) = (6.25 + 20.25 + 12.25 + 30.25)/3 = **23**
- Cov(X₁,X₂) = (−10 + 0 − 17.5 − 5.5)/3 = **−11**

       S = [  14  −11 ]
           [ −11   23 ]

**Step 3: eigenvalues.** `(14 − λ)(23 − λ) − 121 = 0` → `λ² − 37λ + 201 = 0` →
`λ = (37 ± √565)/2` → **λ₁ = 30.3849**, λ₂ = 6.6151.
Check: λ₁ + λ₂ = 37 = trace(S), and λ₁λ₂ = 201 = det(S).

**Step 4: eigenvector for λ₁.** First row of `(S − λ₁I)U = 0`: `(14 − 30.3849)u₁ − 11u₂ = 0` →
`u₂ = −1.4895 u₁`. Take (11, −16.3849), whose length is 19.735, and normalise:
**u₁ = (0.5574, −0.8303)**.

**Step 5: project.** `PC1 = 0.5574·(x₁ − 8) − 0.8303·(x₂ − 8.5)`:

| Point | Centred | PC1 |
|---|---|---|
| 1 | (−4, 2.5) | −2.2296 − 2.0757 = **−4.3052** |
| 2 | (0, −4.5) | 0 + 3.7361 = **3.7361** |
| 3 | (5, −3.5) | 2.7870 + 2.9058 = **5.6928** |
| 4 | (−1, 5.5) | −0.5574 − 4.5664 = **−5.1238** |

This matches the slide. *My addition:* PC1 explains 30.385 / 37 = **82.1%** of the variance, so
going from 2-D to 1-D keeps most of the information.

**Sign does not matter.** The notebook gets u₁ = (−0.5574, 0.8303) and therefore +4.3052, −3.7361,
−5.6928, +5.1238. An eigenvector times −1 is still an eigenvector, so both answers are correct.

## Where the slides are loose

- **Slide 16's formula, `X_centeredᵀ · u₁`, has the transpose in the wrong place** for data stored as one
  row per sample, which is how slide 17 and the notebook store it. X_centered is 4 × 2 and u₁ is 2 × 1, so
  the projection is `X_centered · u₁` (4 × 1). The transposed form only works as `u₁ᵀ · X_centeredᵀ`, or if
  X is stored one column per sample.
- **Step 4 never says to normalise the eigenvector** to unit length. Without that the projections are
  scaled by an arbitrary factor. Slide 17's numbers need the unit vector.
- **The steps skip "sort eigenvalues in descending order and keep the top k"**, which is the step that
  actually reduces the dimension. The notebook does it (`argsort(...)[::-1]`).
- **Step 1 only centres the data.** Not on the slides: when features are in different units, also
  **standardise** them (z-score) first, or the largest-scale feature dominates PC1. That is why 5.2
  recommends standardisation before PCA.
- **Slide 14 mixes notation**: the mean divides by m and the covariance by n − 1, but both are the number
  of samples. Use n − 1 (sample covariance): it is what gives the slide's answer and what `np.cov` does.
- **Slide 5, "reducing the number of variables naturally comes at the expense of accuracy"**: loose. It
  loses *information* (variance), but model accuracy can go up when the dropped dimensions are noise. The
  course's own notebook shows exactly that (SVM 0.73 → 0.805).
- **Slide 11, "goes through the origin" / variance = average squared distance to the origin**: true only
  because the data has been centred, so the origin is the mean.

## Try it

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
pca = make_pipeline(StandardScaler(), PCA(n_components=0.95))   # keep 95% of the variance
Z_train = pca.fit_transform(X_train)                            # fit on train only (5.2's golden rule)
Z_test  = pca.transform(X_test)
pca[-1].explained_variance_ratio_                               # the slide-7 bar chart
```

PCA is **unsupervised**: it never looks at y. It finds high-variance directions, which are not
necessarily the ones that separate the classes.

## Exam checklist

- [ ] Define PCA and a principal component in one sentence each
- [ ] Why variance = information; what PC1 and PC2 are geometrically (max variance, perpendicular)
- [ ] How many PCs p-dimensional data has, and how you choose how many to keep
- [ ] The 5 steps, with the covariance formula (n − 1) and `det(S − λI) = 0`
- [ ] Eigenvalue = variance along a PC, eigenvector = its direction
- [ ] Do the 2-D example by hand: mean, S, λ, unit u₁, projections
- [ ] Explained variance ratio from the eigenvalues
- [ ] Pros (fewer variables, faster, easier to visualise) and cons (PCs are not interpretable, some information is lost)
