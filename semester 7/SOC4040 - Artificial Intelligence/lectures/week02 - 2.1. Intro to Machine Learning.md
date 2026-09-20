# 2.1 — Linear and Polynomial Regression

**SOC4040 · Week 2 · 50 slides · Dr. Oybek Eraliev**
Source: [week02 - 2.1. Intro to Machine Learning.pdf](week02%20-%202.1.%20Intro%20to%20Machine%20Learning.pdf)
Notebook: [linear_regression.ipynb](../resources/linear_regression.ipynb)

Picks up from [1.2](week01%20-%201.2.%20Intro%20to%20Machine%20Learning.md), which stopped
at single-variable regression.

**Contents:** multi-variable linear regression · polynomial regression ·
setting up environments · implementation.

---

## The big idea of this lecture

There are **two ways to solve a linear regression problem**, and knowing when
to use which is the examinable point:

| | **Gradient descent** | **Normal equation** |
|---|---|---|
| Learning rate α | **Must choose one** | **Not needed** |
| Iterations | Many required to reach the optimum | **None — one shot** |
| Many features | **Works well** | **Very slow** |
| Extra cost | — | Must compute `(Xᵀ·X)⁻¹` |

> Rule of thumb: few features → normal equation (exact, no tuning).
> Many features → gradient descent (matrix inversion becomes too expensive).

---

## 1. Linear regression with multiple variables

### From one feature to many

With several input features the hypothesis just gains terms:

```
h(x) = θ₀ + θ₁x₁ + θ₂x₂ + θ₃x₃
     = θ₀ + Σᵢ₌₁..ₙ θᵢxᵢ
```

where `n` is the number of features.

### The vectorisation trick

To write this as a single matrix product, **add a column `x₀` that is always
1**. Then θ₀ becomes just another weight:

```
h(x) = θ₀x₀ + θ₁x₁ + θ₂x₂ + θ₃x₃     (with x₀ = 1)
h(x) = Xθ
```

`X` is the **design matrix** — one row per training example, one column per
feature plus the leading column of ones. `θ` is the parameter column vector.
This is the form everything else uses, and the deck spends many slides walking
through the multiplication row by row.

### The worked example

He uses 5 training examples with 3 features (the Celsius column plus two
others), predicting Fahrenheit. The cost function is unchanged from 1.2, just
written for the vector θ:

```
J(θ) = (1 / 2m) · Σ ( h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾ )²
```

**Starting from θ = [0, 0, 0, 0]:** every prediction is 0, so the residuals
`h(x) − y` are just `−y` = −50, −59, −68, −77, −86. Squaring and summing gives
23,930, so

```
J(θ) = 23930 / (2 × 5) = 2393
```

**The vectorised update rule** — this is the form worth memorising, because it
replaces the per-parameter sums from 1.2 with one matrix expression:

```
θ := θ − α · (1/m) · Xᵀ · ( h(x) − y )
```

**One iteration with α = 0.001** moves θ from all zeros to roughly
`[1.45, 1.527, 0.369, 0.06]`. Re-predicting gives values around 34.7, 41.2,
65.3, 81.3, 93.1, so the residuals shrink from around −50…−86 down to roughly
−15 to +7, and `J` falls sharply from 2393.

He then tabulates the first few iterations to show `J` decreasing each time.

> **Likely exam task:** given a small `X`, `y` and a starting θ, compute `h(x)`,
> the residuals, `J`, and one gradient-descent step. Everything you need is the
> three boxed formulas above.

## 2. The normal equation

The closed-form alternative — solve for the optimum directly, no iteration, no
learning rate:

```
θ = (Xᵀ · X)⁻¹ · (Xᵀ · y)
```

The procedure he walks through: build `X` (with the ones column) and `y`,
transpose `X`, multiply, invert, multiply again.

Applied to the temperature data it returns **θ₁ = 1.8** with the other feature
weights coming out at around `10⁻¹⁴` — numerically zero. In other words it
recovers the true relationship exactly and correctly reports that the two extra
features carry no information. Compare that with gradient descent, which was
still climbing toward it after several iterations.

> Those tiny values like `2.8e-14` are **floating-point noise, not real
> weights**. Reading them as "almost zero" is the intended lesson.

## 3. Polynomial regression

**The core trick:** build new features out of the input — `x²`, `x³`, … — then
train an ordinary linear regression on the expanded feature set.

```
original feature:   x
extended:           x, x², x³
model:              w₁x + w₂x² + w₃x³ + b
```

> **The key point, and a very likely exam question:** the model is **still
> linear with respect to the parameters `w`**. The word "polynomial" describes
> the *shape of the features*, not the model. That's exactly why you can reuse
> linear regression machinery — nothing about the solver changes.

### In scikit-learn

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

poly_model = make_pipeline(
    PolynomialFeatures(degree=2),
    LinearRegression()
)
poly_model.fit(X_train, y_train)
y_pred = poly_model.predict(X_test)
```

- **`PolynomialFeatures`** generates `x²`, `x³`, … from `x`. For degree 2 it maps `x → [1, x, x²]`.
- **`make_pipeline`** chains the steps into one model — convenient and avoids mistakes.
- **`degree`** is the main hyperparameter, and he flags that it **must be chosen correctly**. (Too low underfits; too high overfits — the standard trade-off.)

---

## If you're revising this in 10 minutes

1. **Why add the `x₀ = 1` column** — it folds the intercept into the matrix form `h(x) = Xθ`.
2. **The vectorised update** `θ := θ − α·(1/m)·Xᵀ·(h(x) − y)`.
3. **The normal equation** `θ = (XᵀX)⁻¹Xᵀy`.
4. **The comparison table** — α, iterations, and behaviour with many features. This is the most exam-shaped thing in the deck.
5. **Polynomial regression is linear in the parameters** — only the features change.

The remaining slides are environment setup and Python code screenshots; the
runnable version is in
[linear_regression.ipynb](../resources/linear_regression.ipynb).
