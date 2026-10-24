# 3.1 — Evaluating Learning Algorithms

**Artificial Intelligence · Week 3 · 29 slides · Dr. Oybek Eraliev**
Source: [week03 - 3.1. Evaluating Learning Algorithms.pdf](week03%20-%203.1.%20Evaluating%20Learning%20Algorithms.pdf)
Notebooks: [Evaluating_ML_Models.ipynb](../resources/Evaluating_ML_Models.ipynb) ·
[polynomial_regression_numpy.ipynb](../resources/polynomial_regression_numpy.ipynb)

**Contents:** why evaluate · regression metrics · classification metrics ·
implementation.

---

## 1. Why evaluate at all

The goal isn't low error on the training set. It's **low error on data the
model has never seen**. He gives five reasons to evaluate:

1. **Generalization.** Catches **overfitting** (good on train, bad on test) and
   **underfitting** (bad on both).
2. **Model selection.** You need a standard number to compare candidate models.
3. **Hyperparameter tuning.** Measure the effect of each setting.
4. **Strengths and weaknesses.** Where the model does well and where it struggles, e.g. noisy data.
5. **Benchmarking.** Compare against baselines and earlier models.

## 2. Which metric goes with which problem

| Supervised task | Example algorithms | Metrics |
|---|---|---|
| **Regression** | Linear regression, decision tree, SVM, ridge, stepwise | MSE · RMSE · MAE · R² |
| **Classification** | Logistic regression, decision tree, Naïve Bayes, KNN, SVM | Confusion matrix · accuracy · precision · recall · F1 |

## 3. Regression metrics

Notation is the course's usual one: `m` examples, prediction `h_θ(x⁽ⁱ⁾)`, true
value `y⁽ⁱ⁾`.

| Metric | Formula | What it tells you |
|---|---|---|
| **MSE** | `(1/m) Σ (h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾)²` | Average squared error. **Sensitive to large errors** because they get squared. |
| **RMSE** | `√MSE` | Same thing, but back **in the units of y**. |
| **MAE** | `(1/m) Σ |h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾|` | Average absolute error. **Less sensitive to outliers** than MSE. |
| **R²** | `1 − Σ(y⁽ⁱ⁾ − h_θ(x⁽ⁱ⁾))² / Σ(y⁽ⁱ⁾ − ȳ)²` | Share of the variance in y the model explains. **Close to 1 = good fit.** |

where `ȳ = (1/m) Σ y⁽ⁱ⁾`.

> ⚠️ **Slide 13 has the R² denominator wrong.** It writes
> `Σ(h_θ(x⁽ⁱ⁾) − ȳ)²`, i.e. predictions minus the mean. The correct total sum
> of squares is **`Σ(y⁽ⁱ⁾ − ȳ)²`**: *true values* minus the mean. His own
> notebook (`ss_total = np.sum((y - y_mean)**2)`) uses the correct version.
> Write the correct one in the exam.

Intuition for R²: the denominator is the error you'd get by always predicting
the mean. `R² = 0` means the model is no better than that. `R² < 0` is possible
and means the model is **worse** than predicting the mean.

## 4. Classification metrics

### The confusion matrix

Layout he uses (rows = predicted, columns = actual):

|  | **Actual +** | **Actual −** |
|---|---|---|
| **Predicted +** | True Positive (TP) | False Positive (FP) |
| **Predicted −** | False Negative (FN) | True Negative (TN) |

> Careful: sklearn's `confusion_matrix` and his notebook print it the other way
> round, `[[TN, FP], [FN, TP]]` with rows = actual. Always check which axis is
> which before reading off numbers.

### The worked example — bananas and apples

A classifier sees 10 fruit. **Banana = positive, apple = negative.**

|  | Actual banana | Actual apple |
|---|---|---|
| Predicted banana | **TP = 4** | **FP = 2** |
| Predicted apple | **FN = 1** | **TN = 3** |

| Metric | Formula | Example |
|---|---|---|
| **Accuracy** | `(TP + TN) / total` | (4 + 3) / 10 = **70%** |
| **Precision** | `TP / (TP + FP)` | 4 / 6 = **0.667** |
| **Recall** (sensitivity) | `TP / (TP + FN)` | 4 / 5 = **0.8** |
| **F1** | `2·P·R / (P + R)` | 2·0.667·0.8 / 1.467 = **0.73** |

All four numbers check out.

### Precision vs recall — when each matters

**Precision:** *"Of all the alarms the model raised, how many were real?"* It
only looks at predicted positives.
→ Prioritise it when a **false positive is costly**.
Example: **spam filtering**. Burying a real job offer in spam is worse than
letting one spam through.

**Recall:** *"Of all the real positives out there, how many did we catch?"* It
only looks at actual positives.
→ Prioritise it when a **false negative is costly**.
Examples: **cancer screening** (a missed cancer can be fatal, a false alarm
just means another test) · **airport weapon detection**.

**F1** is the harmonic mean. Use it when you need one number that punishes
being bad at *either*. The harmonic mean is dragged toward the smaller of the
two, so you can't hide poor recall behind great precision.

> Accuracy alone misleads on **imbalanced data**. If 99% of transactions are
> legitimate, a model that always says "legit" is 99% accurate and catches zero
> fraud. That's the reason precision and recall exist.

## 5. Implementation (slides 26–27 are code screenshots)

The code is in **`Evaluating_ML_Models.ipynb`**, and it's all NumPy, no
sklearn:

- **Regression:** `h_x = [11,19,28,35,48,60,66,78,91,99]` vs
  `y = [10,20,30,40,40,60,70,80,90,100]`. It computes MSE, RMSE, MAE and R²
  exactly as in the table above.
- **Classification:** 10 binary predictions. It counts TP/TN/FP/FN with
  boolean masks like `np.sum((h == 1) & (y == 1))`, then computes accuracy,
  precision, recall and F1, guarding against divide-by-zero.
  Here TP = 2, FP = 1, FN = 2, TN = 5, which gives accuracy 0.7,
  precision 0.667, recall 0.5 and F1 ≈ 0.571.

**`polynomial_regression_numpy.ipynb`** is the bigger one and ties this lecture back to
week 2:

- Hand-written `mse()` and `r2_score()` functions.
- Synthetic cubic data, `y = 0.5x³ − x² + 2x + 5 + noise`.
- `polynomial_features(x, d)` builds `[1, x, x², …, xᵈ]`. It's still *linear*
  regression, just on expanded features.
- It solves with the **normal equation** `w = (XᵀX)⁻¹Xᵀy` instead of gradient
  descent, using an 80/20 train/test split.
- It compares degrees 1, 2, 3, 5 and 9 by train and test R². Degree 3 fits
  well. Higher degrees push train R² up while test R² barely moves, and **the
  widening gap is overfitting**.
- It ends with a ⭐⭐ TODO to try other degrees, another data law and more
  noise. It's practice, not stated as graded.

## Exam checklist

- [ ] Define overfitting vs underfitting in terms of train/test error
- [ ] Write MSE, RMSE, MAE, R² (with the **correct** R² denominator)
- [ ] Explain why MSE punishes outliers more than MAE
- [ ] Draw a confusion matrix and compute accuracy, precision, recall and F1 from it
- [ ] Pick precision or recall for a scenario and justify it by which error costs more
- [ ] Explain why accuracy fails on imbalanced classes
