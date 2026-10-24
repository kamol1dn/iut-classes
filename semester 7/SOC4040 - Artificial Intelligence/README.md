# Artificial Intelligence

**Instructor:** Eraliev Oybek · **Room:** B-101 · **Mode:** Offline
**Schedule:** Mon **13:00–14:30** · Thu **14:00–15:30**
**eClass course id:** `2626`

---

## How this course distributes material

Everything comes through **eClass file posts**, organised by week: numbered PDF
decks (`1.1.`, `1.2.`, `2.1.` …) plus Jupyter notebooks for the hands-on parts.
This is the most self-contained of the six courses — eClass is enough.

**Plus a Discord server** (posted by the Education Assistant, Mamurov Jasurbek,
on 2026-09-17):

> https://discord.gg/tWQUXMpM7
> Requirement: set your **per-server nickname** to *Full name, Student ID*.

## Grading — per the week-1 deck, which overrides eClass

| Item | Weight | Detail |
|---|---|---|
| Attendance | 10% | **Medical certificates are not accepted.** 8+ absences = automatic F |
| Mid-term | 25% | Week 8 (Tue 10-27 14:00). **Covers weeks 1–6 only** |
| Final | 25% | Week 15 |
| Homework | 20% | **Two assignments, 10% each** |
| Term project | 20% | Teams of 4-6 |
| **Extra points** | optional | up to **10 points** |

Exams are only 50% here — the lowest of any course this semester.

> 🔴 **"Taking note — checking before mid exam and final exam."** He inspects
> your notes before each exam. Keeping a written notebook is a requirement, not
> a suggestion.

## 📝 Mid-term scope: weeks 1–6

The professor said in class on **Thu 2026-10-22** (week 7): the midterm covers material **up to week 7**,
and **this week's (week 7) topics go to the final**. So study lectures 1.1 through the week-6 lecture, and
skip anything from the 10-19 and 10-22 classes.

**The week-6 decks are now up (posted 10-23/24):** [6.1](lectures/summaries/week06%20-%206.1.%20Unsupervised%20Learning%201.md)
and [6.2](lectures/summaries/week06%20-%206.2.%20Unsupervised%20Learning%202.md) *Unsupervised Learning*, with
`PCA.ipynb` and `K-Means.ipynb`. They're on the midterm, so the PCA rumour (10-15) was right.
Classmates also say there are **open questions worth ~6 points**, e.g. *"the difference between k-means and
k-means++"*, and that decision trees will come up. The week-7 deck (7.1 DNN) is for the final.

## 🔴 Home Assignment 1: a Kaggle competition, due Sun 2026-10-25 23:59 (Tashkent)

Posted on the announcements board on 2026-10-14 by EA Jasurbek Mamurov (eClass board 69586, post 7701).
This is the first of the two 10% homeworks.

- **Join through the invitation link in that eClass announcement**, with your own Kaggle account under
  your **real full name**. One account per student.
- **Verify your phone number** in Kaggle settings, because notebooks need it.
- Read the competition's **Rules** page: **no external data**, and no sharing of code or results before the deadline.
- **Individual work.** Up to **5 submissions a day**. **Select 2 final submissions** before the deadline.
- Submit **your notebook plus a short written report**. The eClass
  [submission space](https://eclass.inha.ac.kr/mod/assign/view.php?id=72915) opened on 10-24 (week-8
  section, announcement post 7725): **one ZIP containing the Kaggle notebook and the report as a PDF**.
  eClass shows the due time as 10-26 00:00; the post says 10-25 11:59 PM.
- Classmates say the **TA may ask you to explain your code**, so understand every line you submit.
- Questions go to the EA on Discord.
- **Full brief, rules, grading and step plan: [homework/hw1-kaggle](homework/hw1-kaggle/README.md)** ([competition](https://www.kaggle.com/competitions/soc-4040-hw-1)). Task: 5-class cancer type from 18 features, scored by **macro-F1**. Grading: **80% leaderboard band**, 10% notebook, 10% report. AI help is allowed (Option A), so list the tools in the report.
- Relevant material: [5.2 Data preparation](lectures/summaries/week05%20-%205.2.%20Data%20preparation%20for%20ML%20models.md)
  and [titanic_data_preparation.ipynb](resources/titanic_data_preparation.ipynb).

## 🔴 Term project — dates that are not on eClass

- **Teams of 4-6 students**, end-to-end AI project.
- **Week 5 (3-9 Oct)** — choose a topic. Free choice but **must not duplicate another team's**. Fields: computer vision, NLP, generative AI.
- **Week 6 (10-16 Oct)** — submit the proposal.
- Prepare a report.
- **Week 14 (5-11 Dec)** — presentation, possibly moved to week 16.

Topic uniqueness is first-come, so forming a team early matters more than it looks.

**Office hours: Tuesday & Thursday, 14:00-15:30.** EA: Jasurbek Mamurov.

> ⚠️ His weekly plan in the deck **differs from the eClass syllabus** from week 4
> onward — he goes Clustering → Deep Learning → CNNs → Advanced CV, then NLP,
> Transformers, Generative Models, RL and Deep RL. SVM and object detection are
> not in his version. Full comparison in
> [the 1.1 summary](lectures/summaries/week01%20-%201.1.%20Intro%20to%20AI.md).

## Materials on hand

Each deck has a full summary beside it — read the `.md`, open the `.pdf` only
for the diagrams.

| Week | Lecture | Topic | Summary | Slides |
|---|---|---|---|---|
| 1 | 1.1 | Intro to AI - foundations, paradigms, LLMs, ethics | [md](lectures/summaries/week01%20-%201.1.%20Intro%20to%20AI.md) | [pdf](lectures/slides/week01%20-%201.1.%20Intro%20to%20AI.pdf) |
| 1 | 1.2 | Linear regression, cost function, gradient descent | [md](lectures/summaries/week01%20-%201.2.%20Intro%20to%20Machine%20Learning.md) | [pdf](lectures/slides/week01%20-%201.2.%20Intro%20to%20Machine%20Learning.pdf) |
| 2 | 2.1 | Multi-variable + polynomial regression, normal equation | [md](lectures/summaries/week02%20-%202.1.%20Intro%20to%20Machine%20Learning.md) | [pdf](lectures/slides/week02%20-%202.1.%20Intro%20to%20Machine%20Learning.pdf) |
| 2 | 2.2 | Logistic regression, multi-class, regularization | [md](lectures/summaries/week02%20-%202.2.%20Logistic%20Regression.md) | [pdf](lectures/slides/week02%20-%202.2.%20Logistic%20Regression.pdf) |
| 3 | 3.1 | Evaluation: MSE/RMSE/MAE/R², confusion matrix, precision/recall/F1 | [md](lectures/summaries/week03%20-%203.1.%20Evaluating%20Learning%20Algorithms.md) | [pdf](lectures/slides/week03%20-%203.1.%20Evaluating%20Learning%20Algorithms.pdf) |
| 3 | 3.2 | Naïve Bayes (Bayes' theorem, shopping example) + KNN | [md](lectures/summaries/week03%20-%203.2.%20Naive%20Bayes%20and%20KNN.md) | [pdf](lectures/slides/week03%20-%203.2.%20Naive%20Bayes%20and%20KNN.pdf) |
| 4 | 4.1 | **Decision tree** (entropy, information gain, Play-Tennis example) + **random forest** | [md](lectures/summaries/week04%20-%204.1.%20Machine%20Learning%20Decision%20Tree.md) | [pdf](lectures/slides/week04%20-%204.1.%20Machine%20Learning%20Decision%20Tree.pdf) |
| 4 | 4.2 | **SVM**: max margin, hard/soft margin + hinge loss, C, kernels | [md](lectures/summaries/week04%20-%204.2.%20Machine%20Learning%20Support%20Vector%20Machine.md) | [pdf](lectures/slides/week04%20-%204.2.%20Machine%20Learning%20Support%20Vector%20Machine.pdf) |
| 5 | 5.2 | **Data preparation**: MCAR/MAR/MNAR + imputation, IQR/Z-score outliers, scaling, encoding, SMOTE, feature selection, leakage. Makeup video for week 4 L2 = YouTube link in week 5 | [md](lectures/summaries/week05%20-%205.2.%20Data%20preparation%20for%20ML%20models.md) | [pdf](lectures/slides/week05%20-%205.2.%20Data%20preparation%20for%20ML%20models.pdf) |
| 6 | 6.1 | **K-Means**: steps, sum-of-squared-distances objective, **K-Means++** (5-point worked example), elbow method, pitfalls | [md](lectures/summaries/week06%20-%206.1.%20Unsupervised%20Learning%201.md) | [pdf](lectures/slides/week06%20-%206.1.%20Unsupervised%20Learning%201.pdf) |
| 6 | 6.2 | **PCA**: definitions, the 5 steps, covariance → eigenvectors → projection, slide-17 example worked in full | [md](lectures/summaries/week06%20-%206.2.%20Unsupervised%20Learning%202.md) | [pdf](lectures/slides/week06%20-%206.2.%20Unsupervised%20Learning%202.pdf) |
| 7 | 7.1 | **Deep learning (DNN)**: perceptron, losses, gradient descent, backprop by hand on a 2-2-1 net, activations. **Final, not midterm** | [md](lectures/summaries/week07%20-%207.1.%20Deep%20Learning%20(DNN).md) | [pdf](lectures/slides/week07%20-%207.1.%20Deep%20Learning%20(DNN).pdf) |

> ⚠️ **6.1 slide 23 has two wrong distances** in the K-Means++ example: B→E is 98 (not 85) and C→E is 32
> (not 25). The conclusion (C or D next) still holds.

> ⚠️ **3.1 slide 13 has the R² formula wrong**: the denominator should be
> `Σ(y − ȳ)²`, not `Σ(h(x) − ȳ)²`. The notebook uses the correct one.

The 1.2 deck was also re-posted as an editable
[pptx](lectures/slides/week01%20-%201.2.%20Intro%20to%20Machine%20Learning.pptx). Same content as the PDF.

Notebooks:

- [K-Means.ipynb](resources/K-Means.ipynb) (week 6, for 6.1): from-scratch K-Means, K-Means++ and an elbow plot
- [PCA.ipynb](resources/PCA.ipynb) (week 6, for 6.2): the slide example in NumPy, then 800 → 50 features before an SVM
- [Neural_Network.ipynb](resources/Neural_Network.ipynb) (week 7, for 7.1): the 2-2-1 network by hand, then PyTorch
- [SVM.ipynb](resources/SVM.ipynb), [kernel_svm_from_scratch.ipynb](resources/kernel_svm_from_scratch.ipynb) (week 5, for 4.2)
- [titanic_data_preparation.ipynb](resources/titanic_data_preparation.ipynb) (week 5, for 5.2)
- [linear_regression.ipynb](resources/linear_regression.ipynb) (week 2)
- [logistic_regression.ipynb](resources/logistic_regression.ipynb) (week 2)
- [polynomial_regression_numpy.ipynb](resources/polynomial_regression_numpy.ipynb) (week 3): from-scratch polynomial regression with the normal equation, and under/overfitting across degrees
- [Evaluating_ML_Models.ipynb](resources/Evaluating_ML_Models.ipynb) (week 3): regression and classification metrics in plain NumPy

To run the notebooks:

```bash
pip install numpy pandas matplotlib scikit-learn jupyter
```

## 🎥 3Blue1Brown (recommended in class)

The professor recommended **3Blue1Brown** out loud in class; it isn't written in any deck or on eClass, so
the exact videos weren't named. The series below are the ones that line up with this course, and each lecture
summary has its own **Watch** section with the matching videos.

| Series | Videos | Best for |
|---|---|---|
| [**Neural networks**](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) | 10 | **The main one.** Ch.1–4 are 7.1 almost scene for scene (network → gradient descent → backprop → backprop calculus) |
| [Essence of linear algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) | 16 | Matrices for 2.1, dot products for 4.2, **eigenvectors for PCA (6.2)** |
| [Essence of calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) | 12 | Derivatives for gradient descent (1.2), the chain rule behind backprop (7.1) |

| Lecture | Watch |
|---|---|
| 1.2 Linear regression, gradient descent | [Gradient descent, how neural networks learn](https://youtu.be/IHZwWFHWa-w) · [The paradox of the derivative](https://youtu.be/9vKqVkMQHKk) |
| 2.1 Multi-variable regression, normal equation | [Linear transformations and matrices](https://youtu.be/kYB8IZa5AuE) · [Inverse matrices](https://youtu.be/uQhTuRlWMxw) |
| 2.2 Logistic regression | [But what is cross-entropy?](https://youtu.be/GlYgs6v2YfU) (the log-loss) |
| 3.2 Naïve Bayes | [Bayes theorem, the geometry of changing beliefs](https://youtu.be/HZGCoVF3YvM) · [The medical test paradox](https://youtu.be/lG4VkPoG3ko) |
| 4.1 Decision tree | [Reinventing Entropy](https://youtu.be/l6DKRf-fAAM) (entropy and information gain) |
| 4.2 SVM | [Dot products and duality](https://youtu.be/LyGKycYT2v0) |
| **6.2 PCA** (midterm) | [Eigenvectors and eigenvalues](https://youtu.be/PFDu9oVAE-g) · [A quick trick for computing eigenvalues](https://youtu.be/e50Bj7jn9IQ) (2×2, like slide 17) · [Change of basis](https://youtu.be/P2LTAUO1TdA) |
| **7.1 Deep learning (DNN)** (final) | Neural networks ch.1–4: [1](https://youtu.be/aircAruvnKk) · [2](https://youtu.be/IHZwWFHWa-w) · [3](https://youtu.be/Ilg3gGewQ5U) · [4](https://youtu.be/tIeHLnjs5U8) · [cross-entropy](https://youtu.be/GlYgs6v2YfU) · [chain rule](https://youtu.be/YG15m2VwSjA) |

3.1, 5.2 and 6.1 (K-Means) have no matching 3Blue1Brown video.

For the later weeks of his plan (NLP, Transformers, generative models), the same playlist continues:
[Large Language Models explained briefly](https://youtu.be/LPZh9BOjkQs) ·
[Transformers (ch.5)](https://youtu.be/wjZofJX0v4M) · [Attention (ch.6)](https://youtu.be/eMlx5fFNoYc) ·
[How might LLMs store facts (ch.7)](https://youtu.be/9-Jl0dxWQs8) ·
[How AI images and videos work](https://youtu.be/iv-5mZ_9CPY) (guest video by Welch Labs).

## Textbooks

- Russell & Norvig, *Artificial Intelligence: A Modern Approach* (Pearson, 2017)
- Géron, *Hands-On Machine Learning with Scikit-Learn and TensorFlow* (O'Reilly, 2023)
- Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* (CUP, 2021)

## Links

- [eClass course page](https://eclass.inha.ac.kr/course/view.php?id=2626)
- [Class announcements](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=69586)
- [Class Q&A board](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=69587)
- [Full syllabus](syllabus/syllabus.md)

## Folders

```
syllabus/    syllabus.md
lectures/    slides/ = PDF (and a few PPTX) decks, prefixed by week · summaries/ = .md notes
homework/    assignments as they are set
resources/   practice notebooks
my-notes/    your own notes
```
