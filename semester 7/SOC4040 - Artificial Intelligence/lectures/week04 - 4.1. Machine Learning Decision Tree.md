# 4.1 — Decision Tree and Random Forest

**Artificial Intelligence · Week 4 · 53 slides · Dr. Oybek Eraliev**
Source: [week04 - 4.1. Machine Learning Decision Tree.pdf](week04%20-%204.1.%20Machine%20Learning%20Decision%20Tree.pdf) *(1.7 MB)*

Posted to the **week 4** section, but it appeared on eClass after 10-05, so it is
being taught in week 5. The tables and trees are images: **open the PDF for slides 26–27 and 32–34
(the Play-Tennis worked example) and 41–46 (the forest example)**.

## Outline

| Slides | Topic |
|---|---|
| 2 | Warm-up recap: a Naïve Bayes question on the "Buy" table (Day, Discount, Free Delivery) |
| 5–8 | What a decision tree is: non-parametric, supervised, does classification *and* regression. **ID3** (entropy), **C4.5** (handles continuous and missing values), **CART** (Gini, binary splits, regression too) |
| 10–13 | Terms: root, decision node, leaf (terminal), sub-tree / branch, pruning, parent and child |
| 15–20 | How it's built: start at the root, pick the "best question", split, recurse until the nodes are pure. A list of "assumptions" |
| 22–29 | **Entropy** as impurity |
| 31–34 | **Information gain** plus the worked example |
| 36–46 | **Random forest**: bootstrap samples, random feature subsets, majority vote |
| 48–50 | RF key features and assumptions |
| 52–53 | Implementation (code screenshots) |

## Formulas

**Entropy** (log base 2, which the slide doesn't state):

    E(S) = − p₊ log₂ p₊ − p₋ log₂ p₋

It is 0 for a pure node and 1 for a 50/50 node.

**Information gain** for splitting S on attribute a:

    IG(S, a) = E(S) − Σ_v (|S_v| / |S|) · E(S_v)

Pick the attribute with the **largest IG**, which is the biggest drop in entropy.

**Gini** (CART, named but not worked through): `G = 1 − Σ pᵢ²`.

## The worked example (slides 32–34): Play Tennis, 14 days

- Root: 9 Yes / 5 No, so E(S) = −(9/14)log₂(9/14) − (5/14)log₂(5/14) ≈ **0.940**.
- **Outlook** has the highest IG (≈ 0.247), so it becomes the root:
  - Overcast → 4 Y / 0 N → **leaf Yes**
  - Sunny → 2 Y / 3 N → split on **Humidity**: High 0/3 → No, Normal 2/0 → Yes
  - Rain → 3 Y / 2 N → split on **Wind**: Strong 0/2 → No, Weak 3/0 → Yes
- Slide 34 asks you to classify `{Outlook = Sunny, Humidity = High, Temp = Hot, Wind = Weak}`.
  Work it through the tree yourself. Note that Temp never gets used.

Practise the IG arithmetic by hand. Computing Gain(Humidity) ≈ 0.151 and
Gain(Wind) ≈ 0.048 at the root is a standard exam question.

## Random forest in 4 lines

1. Draw B **bootstrap** samples (sampling rows with replacement).
2. Grow one tree per sample, and at each split consider only a **random subset of features**.
3. Each tree predicts.
4. **Majority vote** for classification, **average** for regression.

Bagging lowers variance, and random features de-correlate the trees, so the forest
overfits far less than one deep tree. Slide 46 example: all 3 trees say No → **No**.

## Where the slides are loose

- **Slide 16 "binary splits"** vs. the worked example: Outlook splits three ways.
  ID3 and C4.5 do multi-way splits, while CART (and sklearn) does binary splits only.
- **Slide 17 "feature independence"** is the *Naïve Bayes* assumption. Trees
  don't assume it. They model feature interactions naturally.
- **Slide 20 "equal importance … unless feature scaling"**: trees are
  **invariant to feature scaling**. A threshold split doesn't care about units.
- **Slide 48 "handles missing data"**: true for C4.5-style trees. Classic
  sklearn `RandomForestClassifier` needed imputation until v1.4.

## Try it

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
dt = DecisionTreeClassifier(criterion="entropy", max_depth=3).fit(X, y)
rf = RandomForestClassifier(n_estimators=100, max_features="sqrt").fit(X, y)
rf.feature_importances_
```
