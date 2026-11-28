# Homework 2: a CNN from scratch on Tiny ImageNet

**Artificial Intelligence · Homework 2 (10% of the course) · eClass closes Tue 2026-12-01 00:00** (end of Mon 11-30)

- Submit on eClass: [Homework-2. Submission space](https://eclass.inha.ac.kr/mod/assign/view.php?id=74277) (week 12)
- Guidelines: [Homework-2_Guidelines_AI-IUT-Fall-2026-version-3.docx.pdf](Homework-2_Guidelines_AI-IUT-Fall-2026-version-3.docx.pdf)
  (also posted on Discord), reminder in [announcement 7783](https://eclass.inha.ac.kr/mod/ubboard/article.php?id=69586&bwid=7783) (11-27)
- Questions go to the EA, Jasurbek Mamurov, on Discord.

> ⚠️ **The deadline is ambiguous.** The PDF and the announcement say *"Nov 30, 12 AM (the whole Sunday is the
> last day)"*, but in 2026 Sunday is **11-29** and 11-30 is a Monday. The eClass form closes at **12-01 00:00**,
> i.e. the end of Monday. Aim for **Sunday 11-29** and treat Monday as a buffer.

Read from the guidelines PDF on 2026-11-28.

## The task

Build a deep learning model (mainly a CNN), **train it from scratch**, and classify images into **200 classes**.

| | |
|---|---|
| Dataset | Tiny ImageNet: 64 × 64 RGB, 100,000 train (500 per class), 10,000 validation (50 per class) |
| Grading | **Accuracy 50 + macro F1 50**, both on the 10,000-image validation set |
| Platform | Anything; free GPUs on Kaggle Notebooks or Google Colab are fine |

### Loading the data

```python
!pip install -q datasets
from datasets import load_dataset
ds = load_dataset("zh-plus/tiny-imagenet")
train_data = ds["train"]   # 100,000 images
eval_data  = ds["valid"]   # 10,000 images: the evaluation set
```

Alternative: `http://cs231n.stanford.edu/tiny-imagenet-200.zip` (about 240 MB). A few images are grayscale,
so call `image.convert("RGB")` on everything. On Kaggle, switch **Internet on** in the notebook settings
(needs a phone-verified account).

## Rules that zero the homework

**Data leakage scores 0.** The evaluation set (`ds["valid"]`) must never reach training in any form:

- Train only on the training set. Split your own validation set **off the training set** (for example 90 / 10).
- Compute normalisation mean and std **from training images only**.
- Don't pick epochs, settings or models by their evaluation-set score. Use the evaluation set **once**, in the last cell.
- No augmented copies of evaluation images, no merging and re-splitting.

**Pretrained models are not accepted:**

- No pretrained weights, no fine-tuning or transfer learning.
- **No ready-made constructors, even with random weights**: no `torchvision.models.resnet18()`, no `keras.applications`.
  Write the layers yourself. A VGG- or ResNet-*style* network you write is fine.
- Allowed: any framework, conv / pool / norm / dropout / activation layers, augmentation, regularisation, LR schedules.

## What the notebook must show

Run it top to bottom and keep **every output**. They grade only what the outputs show.

1. Data loading and preparation: RGB conversion, train/val split, normalisation, augmentation.
2. Model definition plus a **model summary with the parameter count**.
3. Training loop with **per-epoch loss and accuracy** on train and on your own validation split.
4. **Training curves**: loss and accuracy over epochs.
5. Final predictions on the evaluation set, ending with **exactly this cell**:

```python
from sklearn.metrics import accuracy_score, f1_score
acc = accuracy_score(y_true, y_pred)
f1  = f1_score(y_true, y_pred, average="macro")
print(f"Evaluation accuracy: {acc:.4f}")
print(f"Evaluation macro F1:  {f1:.4f}")
```

## Submission

Two files, named exactly like this, or **20% of your score is deducted**:

| File | Content |
|---|---|
| `<StudentID>_HW2.ipynb` | The notebook with all outputs saved |
| `<StudentID>_HW2.pdf` | The same notebook exported to PDF, outputs visible |

## Time plan

Training takes hours, not minutes, so start the GPU run first and write around it.

1. Kaggle notebook, GPU on, Internet on. Load the data and make the 90/10 split from `train`.
2. A small ResNet-style net you write yourself (for example 4 stages, 64 → 512 channels, BatchNorm, ReLU),
   random crop + horizontal flip, label smoothing, AdamW or SGD with a cosine / OneCycle schedule, 20–40 epochs.
3. While it trains, write the markdown explanations. Plot the curves, then run the evaluation cell **once**.
4. *Save & Run All* (commit) on Kaggle so the outputs are kept, download the `.ipynb`, export the PDF, rename both, upload.
