# SOC4040 — Artificial Intelligence

> Official syllabus, 2026 Fall Semester. Mirrored from eClass on 2026-09-20.
> Source: `https://eclass.inha.ac.kr/local/ubion/setting/syllabus.php?id=2626`

| | |
|---|---|
| **Course No.** | SOC4040 — Class 001 |
| **Semester** | 2026 Fall (202602) |
| **Instructor** | Eraliev Oybek |
| **Room** | B-101 |
| **Schedule** | Mon **13:00–14:30** · Thu **14:00–15:30** (B101) |
| **Credits** | 3.0 |
| **Grading** | Relative evaluation |
| **Mode** | Offline |

## Grading breakdown

| Mid-term | Final | Attendance | Assignments | Quiz | Discussion | Etc. (term project) |
|---|---|---|---|---|---|---|
| 25% | 25% | 10% | 20% | 0% | 0% | 20% |

> Note the **20% "Etc."** — per the class structure this is the **term project**,
> presented in week 14. Combined with assignments that is 40% of the grade
> outside exams.

## Course objectives

By the end of the course students will be able to:

1. Explain foundational AI concepts — history, key paradigms, real-world applications *(week 1)*.
2. Describe and implement core ML algorithms — supervised classification and unsupervised clustering — and evaluate them on real datasets *(weeks 2–4)*.
3. Understand deep learning principles — architectures, forward/backward propagation, optimization *(week 5)*.
4. Design and apply CNNs and advanced computer vision models to classification, detection and segmentation *(weeks 6–7)*.
5. Apply core NLP techniques and transformer architectures (attention, BERT/GPT-style models) *(weeks 9–10)*.
6. Understand generative modeling (GANs, VAEs, diffusion) *(week 11)*.
7. Formulate and solve sequential decision problems with RL and deep RL *(weeks 12–13)*.
8. Integrate multiple AI/ML techniques into an original **term project** *(week 14)*.
9. Critically evaluate AI/ML models — assumptions, limitations, ethics, appropriate use *(week 15)*.

## Course description

A comprehensive introduction to Artificial Intelligence and Machine Learning
covering theoretical foundations and practical applications: core ML algorithms
for classification and clustering, deep learning fundamentals, CNNs and advanced
computer vision, NLP including transformer architectures, generative models and
reinforcement learning. Hands-on exercises plus a term project give practical
experience designing, implementing and evaluating AI/ML solutions.

## Textbooks

| Title | Author | Publisher | Year |
|---|---|---|---|
| Artificial Intelligence: A Modern Approach | Stuart Russell, Peter Norvig | Pearson | 2017 |
| Hands-On Machine Learning with Scikit-Learn and TensorFlow | Aurélien Géron | O'Reilly | 2023 |
| Mathematics for Machine Learning | Deisenroth, Faisal, Ong | Cambridge University Press | 2021 |

## Class structure

PPT lecture presentations · Assignments · Term project

## Weekly plan

| Week | Theme | Details |
|---|---|---|
| 1 | Introduction to AI | Foundations of AI; risks and benefits; supervised, unsupervised and reinforcement learning |
| 2 | Intro to Machine Learning | Linear regression (one variable and multivariable); implementation in Python |
| 3 | ML for Classification | Logistic regression, regularization, binary and multi-class classification; evaluation — accuracy, F1, recall, precision, MSE, RMSE, R²; Python implementation |
| 4 | Non-parametric ML models | Naive Bayes, KNN, Decision Tree, Random Forest |
| 5 | Support Vector Machines | SVM types, mathematical intuition, margin, optimization function and constraints, kernels |
| 6 | Unsupervised Learning | K-Means and K-Means++, PCA for dimensionality reduction, Python implementation |
| 7 | Deep Neural Networks | Perceptron & MLP, forward/backward propagation; optimization — SGD, Adam, loss functions, regularization |
| 8 | **Mid-Exam** | |
| 9 | Convolutional Neural Networks | CNN model representation, convolutional layer, lightweight techniques (depthwise separable, grouped CNN), PyTorch implementation |
| 10 | Object Detection | YOLO, non-max suppression, anchor boxes, R-CNN, Fast R-CNN; YOLO implementation |
| 11 | Sequence Models | RNN, LSTM, GRU; implementation |
| 12 | Intro to NLP | Text preprocessing and embeddings (tokenization, one-hot, bag of words, TF-IDF, Word2Vec, GloVe); sentiment analysis |
| 13 | Transformers and LLMs | Motivation for transformers, attention mechanisms, encoder-decoder; text classification with transformers; training GPT-2 from scratch |
| 14 | **Term Project Presentation** | |
| 15 | **Final Exam** | |
| 16 | — | |

---

## Note on the schedule numbers

**Resolved.** The eClass syllabus numbers are **period indices**, and periods are
30-minute slots starting at 08:00 — so period *n* begins at `07:30 + 0:30n`, and
a `a~b` range runs from the start of period *a* to the end of period *b*.

Verified against the official EduPage timetable for ICE23-1, which agrees with
eClass on 7 of the 8 registered slots. The clock times in the table above are
the authoritative ones, taken from [../../timetable.md](../../timetable.md) —
regenerate it with `python scripts/pull_timetable.py`.
