# 4.2 — Support Vector Machine

**Artificial Intelligence · Week 4 · 51 slides · Dr. Oybek Eraliev**
Source: [week04 - 4.2. Machine Learning Support Vector Machine.pdf](../slides/week04%20-%204.2.%20Machine%20Learning%20Support%20Vector%20Machine.pdf) *(2.1 MB)*

Posted in the week-4 section, and it appeared after 10-05. Several derivation steps (slides 25,
33–35) and the kernel formulas (46–48) are images, so **open the PDF for those**.

## Outline

| Slides | Topic |
|---|---|
| 3–5 | What an SVM is. **Logistic regression = probabilistic, SVM = geometric / max-margin**. Rule of thumb: try LR first, then a linear SVM, then kernels |
| 7 | Linear vs non-linear SVM |
| 9 | Terms: **support vectors** (the points closest to the boundary), **margin**, hard vs soft |
| 11–13 | Only the support vectors define the boundary. LR uses every point |
| 15–22 | Dot-product intuition: project x onto the normal **w**. `w·x > c` → positive, `< c` → negative |
| 24–26 | Hyperplane `w·x + b = 0`, margin lines `w·x + b = ±1` |
| 28–36 | Constraints and the **hard-margin** objective |
| 37–42 | **Soft margin**: hinge loss and C |
| 44–48 | **Kernel trick**: polynomial, sigmoid (RBF only appears in the figure) |
| 49 | Pros and cons |

## The derivation in 5 lines

1. Decision rule: predict +1 if `w·x + b ≥ 0`, otherwise −1.
2. Require every point to sit outside the margin: `yᵢ (w·xᵢ + b) ≥ 1`.
3. Take support vectors x₊, x₋ on the lines `w·x + b = ±1`. The margin is their
   difference projected onto the unit normal: `d = (x₊ − x₋)·w/‖w‖ = 2/‖w‖`.
4. Maximising `2/‖w‖` is the same as **minimising `½‖w‖²`** subject to (2).
   This is the **hard-margin SVM**, and it is feasible only if the data is linearly separable.
5. **Soft margin**: allow violations ξᵢ and pay C for each:

       J(w, b) = ½‖w‖² + C Σᵢ max(0, 1 − yᵢ(wᵀxᵢ + b))

   The `max(0, ·)` term is the **hinge loss**, and ξᵢ ("zeta") is exactly that term.

**C trade-off (slide 41):** large C punishes violations, giving a narrow margin, fewer
training errors and a risk of overfitting. Small C gives a wide margin, more violations
and a smoother boundary.

## Kernels

Map x to a higher-dimensional φ(x) where the data is linearly separable, but compute
only `K(x, x') = φ(x)·φ(x')`, never φ itself.

| Kernel | K(x, x') | Hyperparameters |
|---|---|---|
| Linear | `x·x'` | C |
| Polynomial | `(γ x·x' + r)^d` | C, d, (γ, r) |
| RBF / Gaussian | `exp(−γ ‖x − x'‖²)` | C, **γ** |
| Sigmoid | `tanh(γ x·x' + r)` | C, γ, r |

Kernels and their hyperparameters are chosen by tuning, for example `GridSearchCV` over C and γ.

## Where the slides are loose

- **Slide 34** prints `yᵢ*(2.x+b)=1`. It should be `yᵢ(w·x + b) = 1`.
- **Slide 36** says "the equation which we have to *maximize*" and then shows
  `minimize ½‖w‖²`. Both describe the same problem, since maximising the margin
  2/‖w‖ means minimising ‖w‖.
- **Slide 48**: the sigmoid kernel is `tanh`, which ranges over **(−1, 1)**,
  not (0, 1).
- **Slide 49, "SVM is not sensitive to outliers"**: only partly true. A
  hard-margin SVM is *very* sensitive, because one outlier can become the support vector or
  make the problem infeasible. Soft margin with moderate C is more robust.
- **Slide 49, "works better when the data is linear"**: the
  kernel trick on the same slide exists precisely for non-linear data.

## Try it

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
clf = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma="scale")).fit(X, y)
clf[-1].support_vectors_     # the points that define the boundary
```

Unlike trees (4.1), SVMs **need feature scaling**, because the margin is a distance.
