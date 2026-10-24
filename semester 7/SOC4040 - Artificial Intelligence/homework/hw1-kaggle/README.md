# Home Assignment 1: Kaggle "SOC4040HW1"

**Artificial Intelligence · Homework 1 (10% of the course) · due Sun 2026-10-25 23:59 Tashkent · no late submissions**

- Competition: https://www.kaggle.com/competitions/soc-4040-hw-1 (private; invite link is in
  [eClass announcement 7701](https://eclass.inha.ac.kr/mod/ubboard/article.php?id=69586&bwid=7701))
- Tabs: [Data](https://www.kaggle.com/competitions/soc-4040-hw-1/data) ·
  [Rules](https://www.kaggle.com/competitions/soc-4040-hw-1/rules) ·
  [Leaderboard](https://www.kaggle.com/competitions/soc-4040-hw-1/leaderboard)
- Host: Oybek Eraliev (the lecturer). Questions go to the EA, Jasurbek Mamurov, on Discord.

Read from the competition pages on 2026-10-20.

## The task

Predict a person's **cancer type** from 18 anonymised risk-factor features. This is a **5-class classification** problem.

| label | class |
|---|---|
| 0 | Breast |
| 1 | Colon |
| 2 | Lung |
| 3 | Prostate |
| 4 | Skin |

| File | What it is |
|---|---|
| `train.csv` | 1,200 rows: `id`, `f01`..`f18`, `label` |
| `test.csv` | 800 rows: `id`, `f01`..`f18`. Predict `label` for each |
| `sample_submission.csv` | the format: two columns, `id,label` |
| `data_dictionary.csv` | what each `f01`..`f18` is |

The features are age, gender, BMI, exposure and diet indices (0–10 scale), family history,
genetic and infection flags, and a composite risk score. `id` is random and **carries no
information**, so drop it before training. BMI and the risk score were "lightly perturbed"
(noise was added).

**Metric: macro-averaged F1.** Compute F1 for each of the 5 classes separately, then take
the plain average. Every class counts equally, so a model that ignores a rare class gets punished.
Lecture 3.1 covers F1 for a single class. Macro-F1 is the average of five of those.

**Leaderboard split:** the public score uses about 30% of the test set. The **hidden 70% decides the
final ranking**. Trust your own cross-validation more than the public number.

## Grading (Rules §9)

| Part | Weight |
|---|---|
| Leaderboard score **band** | **80%** |
| Notebook quality and reproducibility | 10% |
| Written report | 10% |

"Grades depend on score bands, not on exact rank." The band cut-offs are not published.
**No reproducible notebook = no leaderboard credit at all** (§6). So the notebook is really what
unlocks the 80%, not just its own 10%.

## Rules that matter

1. **One Kaggle account, real full name, individual.** No teams.
2. **No external data.** Don't look for the original public dataset this may be derived from, and
   don't try to match test rows to outside sources.
3. **No pretrained models and no AutoML.** scikit-learn, XGBoost, LightGBM and PyTorch are allowed.
4. **No sharing** of code, predictions or scores with classmates before the deadline. Discussing
   general ideas is fine.
5. **5 submissions a day.** **Select 2 final submissions** before the deadline. If you don't,
   Kaggle picks by public score, which may not be your best private score.
6. **Share the final notebook with the instructor.** It must run top to bottom and reproduce the
   final submission.
7. **Short written report**: what you tried, what worked, what didn't, and why.
8. He may ask you to **explain your solution** in person. A score you can't explain gets disqualified.

## ⚠️ Three things the rules page leaves open

1. **AI-assistant rule (§4).** The page shows **both** options from a template:
   *Option A (allowed)*: AI can help with code and explanations, but you must be able to explain
   every part and must list the tools you used in the report.
   *Option B (not allowed)*: no AI for writing code or text.
   He forgot to delete one of them. ✅ **Resolved 2026-10-20: AI help is allowed (Option A).**
   So: **list Claude in the report**, and make sure you can explain every line (§7).
2. **Report format.** §6 says "a short written report ()". The format in the brackets is blank,
   and the announcement says report instructions "will be given". Nothing more on eClass as of 10-20.
3. **Starter notebook.** The Overview says there is one in the Code tab. Before joining, the Code
   tab showed none. It may only appear after you join.

Discord message to the EA (edit as you like):

> Hi, about SOC4040 HW1 on Kaggle: what format should the written report be in, and where
> should it be submitted? Thank you.

## Where things stand (public leaderboard, 2026-10-20)

22 students have submitted, 94 submissions in total. Public macro-F1 ranges from **0.716 to 0.796**,
with about half above 0.775. Expect a decent model to land around **0.75–0.80**. Above about 0.78 puts
you in the top third of the public board.

## Plan, step by step

Each step names the lecture it comes from. Steps 1–4 are what to aim for today and tomorrow, so
you have a baseline score early (the 5-a-day cap rewards starting soon).

| # | Step | You'll need | Lecture |
|---|---|---|---|
| 0 | Click **Join Competition**, accept the rules. **Verify your phone** in Kaggle Settings | — | — |
| 1 | New notebook in the Code tab. Load `train.csv`, `test.csv`, `data_dictionary.csv`. Look at shape, dtypes, missing values, and how many rows each class has | `pandas` | 5.2 |
| 2 | Decide what each feature is (number, 0/1 flag, category) using the data dictionary. Plan imputation and scaling | — | 5.2 |
| 3 | **Baseline**: one simple model (e.g. logistic regression) inside a `Pipeline` with scaling. Score it with **5-fold stratified cross-validation, macro-F1** | `sklearn` | 2.2, 3.1 |
| 4 | Fit on all of train, predict test, write `submission.csv` (`id,label`), **submit**. Compare the public score with your CV score | — | — |
| 5 | Try other models from class under the **same CV**: KNN, Naive Bayes, decision tree, random forest, SVM. Then gradient boosting if you like | `sklearn` | 3.2, 4.1, 4.2 |
| 6 | Improve the best one or two: tune a few hyperparameters, try `class_weight="balanced"`, maybe drop useless features | — | 5.2 |
| 7 | Submit your top 2–3 candidates over the next days. **Select 2 finals**: your best CV score, and one safer or different model | — | — |
| 8 | Clean the notebook. **Restart and Run All** on Kaggle so it reproduces the final file. Share it with the instructor | — | — |
| 9 | Write the report (half a page to a page): data findings, models tried with CV and public scores, what worked and why, final choice. List any AI tools if Option A applies | — | — |

### Getting near the top

The public top is 0.796, and the gap between 1st and 10th is only 0.02. On a 240-row public split
that gap is mostly noise. The grade is a **band**, not a rank. So aim for a model that scores well
in **your own CV**, and the private board usually follows. These levers matter most, roughly in order:

1. **Honest CV first.** Use repeated stratified 5-fold (e.g. 3 repeats) and report the mean ± std.
   Every decision below is judged on that number, not on the public board.
2. **Think about what each feature means.** The data dictionary says which column is gender, which are
   exposures, and so on. Some classes are almost decided by one feature (prostate needs a male, breast
   is overwhelmingly female). Others line up with an exposure (lung with smoking/air, skin with sun,
   colon with diet/BMI). Plot each class against those features. Encode categories properly and
   leave 0/1 flags as they are.
3. **Tree ensembles.** Random forest (4.1) and gradient boosting (`HistGradientBoostingClassifier`,
   LightGBM, XGBoost) usually beat linear models on tabular data like this. Tune only a few settings
   (depth, number of trees, learning rate, min samples per leaf) with a small grid. Don't search hundreds.
4. **Class balance for macro-F1.** If one class is rarer, try `class_weight="balanced"`. Look at the
   per-class F1 from `classification_report`. The weakest class is where the points are.
5. **Ensemble.** Average the predicted probabilities of 2–3 different good models (soft voting),
   e.g. boosting + random forest + logistic regression. That's often a steady +0.005 to +0.01.
6. **Don't over-engineer.** With 1,200 rows, piling on features or tuning overfits fast. If a change
   doesn't beat the CV standard deviation, it isn't real.

### Pitfalls

- **Fit scalers and imputers inside the CV folds**, using a `Pipeline`. Fitting them on all of train
  first leaks information into validation (5.2's "data leakage").
- **Use `StratifiedKFold`** so each fold has every class in the same proportion. It matters with
  5 classes and only 1,200 rows.
- **Use `scoring="f1_macro"`.** Accuracy can look good while a small class is getting zero F1.
- **Set `random_state`** everywhere, or the notebook won't reproduce the same file.
- **Don't chase the public board.** It's only 240 rows, so a +0.01 jump there is often noise.
- Keep a small table as you go (model, settings, CV macro-F1, public score). It *is* the report.

## Timeline (fits around the midterms)

| Day | Kaggle work |
|---|---|
| Tue 10-20 | Steps 0–1. Send the Discord question |
| Wed 10-21 | Steps 2–4: baseline submitted |
| Thu 10-22 | Step 5: compare the class models |
| Fri 10-23 | Step 6: tune, submit 2–3 |
| Sat 10-24 | Steps 7–9: pick finals, share the notebook, report |
| Sun 10-25 | Buffer. Nothing after 23:59 |

## Submission checklist

- [ ] Joined with real full name, phone verified
- [ ] At least one submission scored on the leaderboard
- [ ] **2 final submissions selected** (Submissions page → tick "Use for Final Score")
- [ ] Notebook runs top to bottom with Restart and Run All and reproduces the final file
- [ ] Notebook shared with the instructor
- [ ] Notebook + report (PDF) zipped together and uploaded to the eClass [submission space](https://eclass.inha.ac.kr/mod/assign/view.php?id=72915) (opened 10-24)
