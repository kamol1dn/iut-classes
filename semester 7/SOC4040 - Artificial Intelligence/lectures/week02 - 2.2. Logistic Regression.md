# 2.2 — Classification: Logistic Regression

**SOC4040 · Week 2 · 49 slides · Dr. Oybek Eraliev**
Source: [week02 - 2.2. Logistic Regression.pdf](week02%20-%202.2.%20Logistic%20Regression.pdf)
Notebook: [logistic_regression.ipynb](../resources/logistic_regression.ipynb)

**Contents:** logistic regression · multi-class classification · regularization ·
implementation.

---

## 1. Classification

**Examples he uses throughout:** email spam / not spam · online transaction
fraud (yes / no) · brain tumour benign / malignant.

| Type | Labels |
|---|---|
| **Binary** | `y ∈ {0, 1}` |
| **Multi-class** | `y ∈ {0, 1, 2, 3, …}` |

Convention: **0 = "negative class"** (benign tumour), **1 = "positive class"**
(malignant).

### Why linear regression doesn't work here

The obvious idea is to fit `h_θ(x) = Xθ` and threshold it at 0.5 — predict
`y=1` if `h_θ(x) ≥ 0.5`, else `y=0`. He shows this on the tumour-size data, and
it appears to work.

Then he adds a data point further along the axis. The fitted line tilts, the
0.5 crossing moves, and examples that were classified correctly now aren't.
**One outlier breaks the classifier.**

There's a second problem: `h_θ(x) = Xθ` can return values **above 1 or below
0**, which is meaningless if you want to read the output as a probability.

> **What we want:** `0 ≤ h_θ(x) ≤ 1`. That is exactly what logistic regression
> gives.

## 2. The hypothesis — the sigmoid

```
h_θ(x) = g(Xθ)        where      g(z) = 1 / (1 + e⁻ᶻ)

so     h_θ(x) = 1 / (1 + e^(−Xθ))
```

`g` is the **logistic / sigmoid function**. It's an S-curve that squashes any
real number into (0, 1), crossing 0.5 at `z = 0`.

### Interpreting the output

`h_θ(x)` is the **estimated probability that y = 1** given input `x`:

```
h_θ(x) = P(y = 1 | X ; θ)
```

His example: with `x = [1, tumorSize]`, an output of `h_θ(x) = 0.7` means you
tell the patient there is a **70% chance the tumour is malignant**.

Because there are only two outcomes:

```
P(y=0 | X;θ) + P(y=1 | X;θ) = 1
P(y=0 | X;θ) = 1 − P(y=1 | X;θ)
```

### Threshold, restated

Predict `y=1` when `h_θ(x) ≥ 0.5`, else `y=0`. And since the sigmoid crosses
0.5 exactly at zero:

```
g(z) ≥ 0.5  ⟺  z ≥ 0
g(z) < 0.5  ⟺  z < 0
```

**So you can skip the sigmoid entirely and just check the sign of `Xθ`.**
Predict 1 when `Xθ ≥ 0`. This is what makes the decision boundary a clean
geometric object.

## 3. Decision boundary

Take `h_θ(x) = g(θ₀ + θ₁x₁ + θ₂x₂)` with **θ = [−3, 1, 1]**:

```
predict y=1   when   −3 + x₁ + x₂ ≥ 0   →   x₁ + x₂ ≥ 3
predict y=0   when                          x₁ + x₂ < 3
```

The **decision boundary** is the line `x₁ + x₂ = 3` — precisely where
`h_θ(x) = 0.5`.

> **Very likely exam question:** given a θ vector, write down and sketch the
> decision boundary. Set `Xθ = 0` and solve.

## 4. Cost function

Squared error is not used here. Instead, **log loss**, defined piecewise:

```
Cost(h_θ(x), y) =  −log( h_θ(x) )        if y = 1
                   −log( 1 − h_θ(x) )    if y = 0
```

The intuition: if `y=1` and you predict close to 1, `−log(1) = 0`, no penalty.
Predict close to 0 and the cost shoots to infinity. Confident and wrong is
punished hardest.

**Collapsed into one line** — this works because one of the two terms always
multiplies by zero:

```
Cost(h_θ(x), y) = −y·log(h_θ(x)) − (1−y)·log(1 − h_θ(x))
```

**Averaged over the training set:**

```
J(θ) = −(1/m) · Σᵢ [ y⁽ⁱ⁾·log(h_θ(x⁽ⁱ⁾)) + (1−y⁽ⁱ⁾)·log(1 − h_θ(x⁽ⁱ⁾)) ]
```

## 5. Gradient descent

```
repeat {
    θⱼ := θⱼ − α · (1/m) · Σᵢ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) · xⱼ⁽ⁱ⁾
}
```

vectorised as

```
θ := θ − α · (1/m) · Xᵀ · ( h(x) − y )
```

> **The point he is making, and it's exam-shaped:** this is *identical in form*
> to linear regression's update from [2.1](week02%20-%202.1.%20Intro%20to%20Machine%20Learning.md).
> The only thing that changed is that `h_θ` is now the sigmoid rather than `Xθ`.

### The worked example

Five training examples with two features plus the `x₀ = 1` column, labels
`y = [1, 0, 0, 1, 1]`, starting `θ = [0, 0, 0]` and `α = 0.1`.

| Step | Result |
|---|---|
| `Z = Xθ` | all zeros |
| `h_θ(x) = 1/(1+e⁰)` | **0.5 for every example** |
| `J(θ)` | **0.693** |
| `h(x) − y` | ±0.5 for each row |
| θ after iteration 1 | ≈ `[−0.03, 0.07, …]` |

Then the iteration table: **J = 0.693 → 0.638 → 0.595**, decreasing as expected.

> **Useful sanity check:** 0.693 is `ln 2`. When every prediction is 0.5, every
> term is `−log(0.5) = 0.693`, so the average is 0.693. If you start a logistic
> model from all-zero weights and your first cost isn't ≈0.693, something is wrong.

## 6. Multi-class classification

**Examples:** email foldering (Work / Friends / Family / Hobby) · medical
diagnosis (Not ill / Cold / Flu) · weather (Sunny / Cloudy / Rain / Snow).

**The method — one-vs-all** (also called one-vs-rest):

1. For each class `i`, train a **separate** logistic regression classifier `h⁽ⁱ⁾_θ(x)` that predicts `P(y = i | x; θ)` — that class against everything else combined.
2. For a new input `x`, run **all** the classifiers and **pick the class `i` that maximises `h⁽ⁱ⁾_θ(x)`**.

So three classes means three binary classifiers, each drawing its own boundary.

## 7. Regularization

### The problem of overfitting

Shown first on linear regression (housing prices):

| Model | Behaviour | Diagnosis |
|---|---|---|
| `θ₀ + θ₁x` | Too simple to follow the data | **Underfit → high bias** |
| `θ₀ + θ₁x + θ₂x²` | Fits well | Just right |
| `θ₀ + θ₁x + θ₂x² + θ₃x³ + θ₄x⁴` | Wiggles through every point | **Overfit → high variance** |

**Definition:** with too many features, the hypothesis may fit the training set
almost perfectly (`J(θ) ≈ 0`) yet **fail to generalise to new examples**.

The same picture is repeated for logistic regression, where the decision
boundary goes from a straight line, to a sensible curve, to a contorted shape
wrapping individual points.

### Two ways to address it

1. **Reduce the number of features** — select manually which to keep, or use a model-selection algorithm (covered later in the course).
2. **Regularization** — keep all the features but **shrink the magnitude of the parameters θⱼ**. Works well when you have many features each contributing a little to predicting `y`.

**Definition:** regularization prevents overfitting by **penalising complex
models** — adding a penalty term to the cost function that forces the weights to
stay small, improving generalisation to unseen test data.

### L2 regularization — the formulas

**Linear regression with L2 → this is Ridge Regression:**

```
J(θ) = (1/2m) · [ Σᵢ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ )²  +  λ · Σⱼ₌₁..ₙ θⱼ² ]
```

**Logistic regression with L2:**

```
J(θ) = −(1/m)·Σᵢ [ y⁽ⁱ⁾log(h_θ(x⁽ⁱ⁾)) + (1−y⁽ⁱ⁾)log(1−h_θ(x⁽ⁱ⁾)) ]
       + (λ/2m)·Σⱼ₌₁..ₙ θⱼ²
```

`λ` is the **regularization parameter**.

**Gradient descent, both cases** — note θ₀ is handled separately:

```
θ₀ := θ₀ − α·(1/m)·Σ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ )·x₀⁽ⁱ⁾

θⱼ := θⱼ − α·(1/m)·[ Σ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ )·xⱼ⁽ⁱ⁾ + (λ/m)·θⱼ ]
```

> **The detail most often asked about:** the penalty sum runs from **j = 1**,
> not j = 0. **θ₀ (the bias) is never regularized** — which is why it gets its
> own update line. Shrinking the intercept would just bias every prediction
> toward zero for no benefit.

---

## If you're revising this in 10 minutes

1. **Why not linear regression** — outliers move the threshold, and output escapes [0,1].
2. **The sigmoid** `g(z) = 1/(1+e⁻ᶻ)` and that `h_θ(x) = P(y=1|x;θ)`.
3. **Predict 1 when `Xθ ≥ 0`** — and be able to derive the decision boundary from a given θ.
4. **Log loss**, both the piecewise and combined forms, and why confident-and-wrong costs infinity.
5. **The update rule is the same shape as linear regression** — only `h_θ` changed.
6. **One-vs-all**: one classifier per class, take the max.
7. **Bias vs variance**, and **L2 regularization excludes θ₀**.
