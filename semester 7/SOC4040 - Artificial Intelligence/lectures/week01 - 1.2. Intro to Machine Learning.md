# 1.2 — Intro to Machine Learning: Linear Regression

**SOC4040 · Week 1 · 34 slides · Dr. Oybek Eraliev**
Source: [week01 - 1.2. Intro to Machine Learning.pdf](week01%20-%201.2.%20Intro%20to%20Machine%20Learning.pdf)
Notebook: [linear_regression.ipynb](../resources/linear_regression.ipynb)

> The deck follows Andrew Ng's ML course closely (he credits it on slide 23), so
> the notation here — `h`, `θ`, `J`, `α` — is Ng's. If you get stuck, his course
> covers the identical derivation.

---

## Definitions

**Machine learning**, two definitions he gives:

- The use and development of computer systems able to **learn and adapt without following explicit instructions**, using algorithms and statistical models to analyse and draw inferences from patterns in data.
- **Arthur Samuel (1959):** the field of study that gives computers the ability to learn without being explicitly programmed. *(Memorise the name and year — classic exam fodder.)*

**Nesting:** AI ⊃ Machine Learning ⊃ Deep Learning.

**Branches of ML:** supervised · unsupervised · reinforcement · recommender systems.

## The taxonomy — worth memorising as a table

| | Sub-type | Algorithms | Example applications |
|---|---|---|---|
| **Supervised** | **Classification** | Logistic Regression · Decision Tree · Naive Bayes · K-Nearest Neighbour · SVM | Email spam detection · speech recognition |
| | **Regression** | Linear Regression · Ridge Regression · Stepwise Regression | Stock market prediction · rainfall prediction |
| **Unsupervised** | **Clustering** | K-Means · MeanShift | — |
| | **Dimensionality reduction** | PCA · LDA · Autoencoders | — |

The distinction he draws with pictures: **classification** outputs a *category*
(apple / banana), **regression** outputs a *continuous number* (45 °C → 113 °F).

---

## Linear regression with one variable

### The running example

He uses Celsius → Fahrenheit, where the true relationship is known:

```
F = 32 + 1.8 · t
```

That's deliberate — you already know the right answer, so you can watch the
algorithm discover it. The second example is house size (ft²) → price.

### Notation — get this straight, everything else builds on it

| Symbol | Meaning |
|---|---|
| `m` | number of training examples |
| `x` | input variable / **feature** |
| `y` | output variable / **target** |
| `(x, y)` | one training example |
| `(x⁽ⁱ⁾, y⁽ⁱ⁾)` | the **i-th** training example |
| `h` | the **hypothesis** — the function the learning algorithm produces |

The pipeline: **training set → learning algorithm → h**, and then `h` maps a new
input to a prediction.

### The hypothesis

```
h_θ(x) = θ₀ + θ₁x
```

Equivalently `y = b + wx` — `θ₀` is the intercept (bias), `θ₁` the slope
(weight). For the temperature data the correct answer is **θ₀ = 32, θ₁ = 1.8**.

Changing the two parameters just moves and tilts the line — he shows three
cases (`θ₀=1.5, θ₁=0` gives a flat line; `θ₀=0, θ₁=0.5` a line through the
origin; `θ₀=1, θ₁=0.5` both).

### The cost function

The whole problem is: **pick θ₀ and θ₁ so h_θ(x) is close to y across the
training examples.** "Close" is made precise by the **squared error function**:

```
J(θ₀, θ₁) = (1 / 2m) · Σᵢ₌₁..ₘ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ )²
```

and the goal is

```
minimise over θ₀, θ₁ of J(θ₀, θ₁)
```

> Two things examiners like to ask: the `2` in `2m` is there to cancel when you
> differentiate the square, and the error is **squared** so positive and
> negative errors don't cancel out.

### The worked example — know how to reproduce this

He simplifies to `θ₀ = 0`, so `h_θ(x) = θ₁x` and the cost `J(θ₁)` can be drawn
on one axis. With the three points (1,1), (2,2), (3,3):

| θ₁ | Computation | J(θ₁) |
|---|---|---|
| **1** | ((1−1)² + (2−2)² + (3−3)²) / (2·3) = 0 / 6 | **0** |
| **0.5** | ((0.5−1)² + (1−2)² + (1.5−3)²) / (2·3) = 3.5 / 6 | **0.58** |
| **0** | ((0−1)² + (0−2)² + (0−3)²) / (2·3) = 14 / 6 | **2.33** |

Plotting these gives a **parabola** (bowl shape) with its minimum at θ₁ = 1 —
which is exactly the right answer. With both parameters free, `J(θ₀, θ₁)`
becomes a 3-D bowl surface.

**This is a very likely exam question:** given three or four points and a value
of θ, compute J by hand. Practise it.

---

## Gradient descent

The algorithm for finding the minimum without trying every value.

**Outline:** start with some `(θ₀, θ₁)` — typically `(0, 0)` — then keep changing
them to reduce `J` until you reach a minimum.

```
repeat until convergence {
    θⱼ := θⱼ − α · ∂/∂θⱼ J(θ₀, θ₁)        for j = 0 and j = 1
}
```

Two pieces: **α** is the **learning rate**, and the rest is the **derivative
(slope) term**.

### Why the sign works out

| Situation | Derivative | Effect |
|---|---|---|
| Positive slope | ≥ 0 | θ₁ − α·(positive) → **θ₁ decreases** |
| Negative slope | ≤ 0 | θ₁ − α·(negative) → **θ₁ increases** |
| At a local optimum | slope = 0 | θ₁ − α·0 → **θ₁ unchanged** |

Either way you move *downhill*, and you stop automatically at the bottom.

### Choosing α

- **Too small** → gradient descent is slow, taking tiny steps.
- **Too large** → it can **overshoot** the minimum, and may fail to converge or even **diverge**.

> A point he makes explicitly and that gets asked: **you don't need to decrease
> α over time.** As you approach a minimum the derivative shrinks, so the steps
> get smaller on their own. Gradient descent converges to a local minimum with α
> held fixed.

### The derivatives, worked out

Substituting `h_θ(x) = θ₀ + θ₁x` into `J` and differentiating:

```
∂J/∂θ₀ = (1/m) · Σ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ )
∂J/∂θ₁ = (1/m) · Σ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) · x⁽ⁱ⁾
```

The only difference is the trailing `· x⁽ⁱ⁾` on the θ₁ term. Giving the final
update rules:

```
repeat until convergence {
    θ₀ := θ₀ − α · (1/m) · Σ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ )
    θ₁ := θ₁ − α · (1/m) · Σ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) · x⁽ⁱ⁾
}
```

> **Both must be updated simultaneously** — compute both new values from the
> *old* θ's, then assign. Updating θ₀ first and using it in the θ₁ computation is
> the classic mistake.

### The payoff

Running this on the temperature data with **α = 0.01**, starting from
`θ₀ = 0, θ₁ = 0`, the parameters converge over iterations to **θ₀ = 32,
θ₁ = 1.8** — rediscovering the Celsius-to-Fahrenheit formula from data alone.
The cost `J` drops toward the bottom of the bowl as it goes.

---

## Still to come

The deck's contents list promises **linear regression with multiple variables**,
but the slides stop before it. That's picked up in
[2.1](week02%20-%202.1.%20Intro%20to%20Machine%20Learning.md).

## If you're revising this in 10 minutes

Be able to (1) write the hypothesis, (2) write the squared-error cost function
and say why it has `2m` and a square, (3) **compute J by hand for given points
and θ**, (4) write the gradient descent update rule and explain α being too
small vs too large, and (5) say why α need not decrease over time. Run
[linear_regression.ipynb](../resources/linear_regression.ipynb) once to see it move.
