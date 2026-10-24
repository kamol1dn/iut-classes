# 5.2: Preparing Datasets for ML Model Training

**Artificial Intelligence · Week 5 · 39 pages · Dr. Oybek Eraliev**
Source: [week05 - 5.2. Data preparation for ML models.pdf](../slides/week05%20-%205.2.%20Data%20preparation%20for%20ML%20models.pdf) *(1.6 MB)*

Companion material:
- [titanic_data_preparation.ipynb](../../resources/titanic_data_preparation.ipynb) is this lecture applied to Titanic
- The **makeup video for the missed Week 4, Lecture 2** is this lecture on YouTube
  (eClass URL module 72382 in week 5: *Preparing Datasets for ML Model Training*, youtu.be/bFWPSe-kSyY)

Week 5 also brought two SVM notebooks for 4.2: [SVM.ipynb](../../resources/SVM.ipynb) and
[kernel_svm_from_scratch.ipynb](../../resources/kernel_svm_from_scratch.ipynb). There is no
"5.1" file on eClass. 4.2 SVM was presumably covered in its place.

This lecture is directly useful for **Home Assignment 1** (the Kaggle competition, due 10-25).

## Outline

| Pages | Topic |
|---|---|
| 3–6 | What data is. **Structured** (tables, SQL, time series) vs **unstructured** (text, images, audio) vs **semi-structured** (JSON/XML/logs). "Garbage in, garbage out": 60–70% of a data scientist's time goes on preparation |
| 7–8 | Pipeline: **collect → inspect → clean → transform → store → visualize**. Inspect first: `shape`, `dtypes`, `head()`, `describe()` |
| 9 | Six problems in every raw dataset: missing values, duplicates, wrong format, outliers, inconsistency, broken foreign keys |
| 10–11 | Missingness mechanisms (**MCAR / MAR / MNAR**). Imputation: drop, mean/median, mode, `KNNImputer`, `IterativeImputer` (MICE), GAIN |
| 12 | Duplicates: `drop_duplicates()`. Near-duplicates need record linkage (`recordlinkage`, `dedupe`) |
| 13–15 | Outliers: **IQR rule**, **Z-score**, then ML-based methods (Isolation Forest, LOF, autoencoders) |
| 16–17 | Six quality dimensions. Profiling tools (ydata-profiling, Great Expectations, Apache Griffin) |
| 18–20 | Scaling: **Min-Max**, **standardization**, **robust** |
| 21–22 | Encoding: **label** vs **one-hot**. Target encoding, entity embeddings |
| 23–25 | Big data's 5 Vs. **Class imbalance** (accuracy is misleading) → **SMOTE**, ADASYN, Borderline-SMOTE, class weights |
| 26–27 | Augmentation for images (flip/rotate/crop, Mixup, CutMix, diffusion) and audio (SpecAugment etc.) |
| 28–29 | Feature engineering (time features, log transform, ratios). Feature selection: **filter / wrapper / embedded** |
| 30–33 | Data-centric AI (Andrew Ng), synthetic data, foundation-model embeddings, validation and versioning tooling |
| 34 | **Golden rule: fit on train, transform on test** |
| 35–37 | Tool choice by data size, common mistakes, a readiness checklist |

## The ones to memorise

| Thing | Rule |
|---|---|
| MCAR | missingness is unrelated to anything (a sensor dropped out) |
| MAR | it depends on *other observed* columns (older people skip the income question) |
| MNAR | it depends on *the missing value itself* (high earners hide their income). The hardest case |
| IQR outlier | outside `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`, where `IQR = Q3 − Q1` |
| Z-score outlier | `|z| > 3`, with `z = (x − μ)/σ`. Assumes the data is roughly normal |
| Min-Max | `(x − min)/(max − min)` gives [0, 1]. The most outlier-sensitive. Good for NN, KNN, SVM |
| Standardize | `(x − μ)/σ` gives mean 0, sd 1. Good for linear/logistic regression and PCA |
| Robust | `(x − median)/IQR`. Resists outliers |
| Label encoding | only when the categories have a real order |
| One-hot | for nominal categories with few levels |
| Imbalance metrics | precision, recall, F1, PR-AUC. **Not accuracy** |
| SMOTE | pick a minority point, take its k nearest minority neighbours, interpolate between them. **Training set only** |
| Leakage | fit scalers, encoders, imputers and SMOTE on **train only**. Split time series chronologically |

## Things that are wrong or loose in the deck

- **Page 22's target-encoding code leaks.** It runs `te.fit_transform(df, df['salary'])` on the full
  dataset, which breaks the deck's own golden rule (p. 34). Fit the encoder on the training split
  only, ideally out-of-fold.
- **Page 29 lists Ridge (L2) as an embedded feature-selection method.** L2 shrinks coefficients but
  never makes them exactly zero, so it doesn't select anything. **LASSO (L1)** is the one that does.
- Page 13 calls the IQR rule best for "roughly symmetric" data. Its real advantage is that it doesn't
  assume normality and is robust to the outliers it is looking for. The Z-score is the one that
  needs a symmetric, normal-ish distribution.
