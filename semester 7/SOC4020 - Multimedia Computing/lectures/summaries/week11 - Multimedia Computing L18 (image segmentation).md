# L18: Image Segmentation II: Thresholding, Otsu, Hierarchical Clustering, Mean Shift

**Multimedia Computing · Week 11 · 66 slides · Dr. Minhaz Uddin Ahmed**
Source: [week11 - Multimedia Computing L18 (image segmentation).pptx](../slides/week11%20-%20Multimedia%20Computing%20L18%20(image%20segmentation).pptx) *(4.5 MB)*
Practice: [L18 practice - detect_blob.png](../../resources/L18%20practice%20-%20detect_blob.png) ·
[L18 practice - tomatoes.jpg](../../resources/L18%20practice%20-%20tomatoes.jpg)

This continues **L17**. There is **no reference slide**. The thresholding half (slides 3–38) matches the
thresholding section of Gonzalez **chapter 10**, which L17 cites: basic global thresholding, Otsu, multiple
thresholds. It adds a few MATLAB demos
(`tools.bmp`, `boy.jpg`, `nodules1.tif`, `rice.tif`) and two Python ones (`detect_blob.png`, `sudoku.png`).
The clustering half covers **hierarchical clustering** (39–60) with a six-point worked example. **Mean
shift** (61–64) appears only as scikit-learn code, result pictures (slide 63 links Comaniciu & Meer's
results page) and a pros/cons list. The deck never explains how mean shift works, so there is a short
explanation below.

Pictures to open in the pptx: the binary-image tables (12), the code screenshots (13, 17), the Otsu
formulas (27–29), the linkage formulas (43, 45) and the worked distance tables (50–53). Their content is
copied below.

## The practice images

**`detect_blob.png`** is the image on slides 9, 13 and 14. Slide 13's script reads it in greyscale
(`cv2.imread('detect_blob.png', 0)`) and thresholds it at **85** with a double Python loop ("Slow Binary").
So the in-class exercise is: run it, see slide 14's binary image, then experiment with the threshold.

What to notice on slide 14: three things drop out because they are dark *in grey* even though they're
obvious in colour. They are the **dark-blue ellipse**, the **dark lower part of the red gradient bar**, and
the **shadowed edge of the shaded circle**. *(mine)* My run of the script gave the same picture, with 17
white blobs. Otsu (`cv2.THRESH_OTSU`) picked T = 80, which still loses the ellipse. Those two numbers are
from OpenCV 5.0; other libraries convert this PNG to grey slightly differently. The one-line version of the
loop is `_, binary = cv2.threshold(bw, 85, 255, cv2.THRESH_BINARY)`.

**`tomatoes.jpg`** is not named anywhere in the deck. It appears to be the colour-segmentation exercise:
pick out the red tomatoes. *(mine, from running it)* Greyscale thresholding fails here. Red tomatoes and
green leaves have similar grey levels (mean about 116 vs 141), so grey Otsu (T = 138) marks half the image
as foreground and catches only about 23% of the tomato pixels. A colour rule (red hue in HSV) or **k-means on
colour** (L17 slides 56–61) separates them: with k = 3, one cluster centre comes out orange-red. The unripe
green tomatoes will stay mixed with the leaves either way.

## Outline

| Slides | Topic |
|---|---|
| 3 | Segmentation is usually the **first step** of image analysis: split the image into meaningful, non-overlapping regions. Autonomous segmentation is one of the hardest problems in image processing. Example: threshold a hand photo, then count the fingers |
| 4 | **Pixel-based** methods. **Thresholding**: pixels above (or below) a level form the segment, giving a binary image. **Slicing**: keep a range between a lower and an upper bound. Several ranges can each get their own label |
| 5–8 | Choose the level from the **intensity histogram**. If it is bimodal, threshold at the **valley** (minimum). Valleys are hard to find because of noise. Trick: boundary pixels have in-between values and high gradient, so remove them (Sobel or Canny), then recompute a cleaner histogram |
| 9–14 | Basic idea (above T → region 1, below → region 2). Pros: simple, good when peaks are well separated. Cons: noise, and **intensity inhomogeneity** (uneven lighting). Binary-image tables with T = 128 and T = 64. Python practice on `detect_blob.png` |
| 15–16 | Segmentation assumes intensities differ *between* regions and are similar *within* them. `tools.bmp` at two thresholds. A sudoku photo where one global threshold fails in the shadowed corner |
| 17–18 | **Adaptive thresholding** for uneven lighting: different thresholds in different parts of the image. `cv2.adaptiveThreshold(…, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, …)` cleans up the sudoku |
| 19–20 | **Fixed (global)** threshold form. Overlapping histogram peaks. The mean intensity as a simple threshold |
| 21–23, 32 | **Iterative (basic global) thresholding** (algorithm below). MATLAB demo calls `opthr` |
| 24–26 | **Optimal thresholding**: when peaks overlap, some pixels will be misclassified whatever you do, so define a criterion function and maximise it |
| 27–31 | **Otsu's method** (formulas below). MATLAB `graythresh` + `im2bw` on `nodules1.tif` (level 0.5804) and `rice.tif` |
| 33 | Bimodal example: rice on a black background |
| 34–38 | **Multimodal** histograms need **multiple thresholds**. One method: **Discrete Curve Evolution** treats the histogram as a polyline and simplifies it until a few vertices remain (256 → 15 for Lena). The local-minimum vertices become the thresholds |
| 39–42 | **Hierarchical clustering**. Flat methods (k-means) need k up front. Hierarchical methods build partitions P1 (one cluster) … Pn (every point alone) and let you choose. **Agglomerative** (bottom-up, merge the closest pair) vs **divisive** (top-down, split recursively). Each needs a rule: a cluster distance for merging, a split criterion for dividing |
| 43 | Distances between clusters: **single, average, complete linkage**, **centroid**, **Ward** |
| 44–45 | Divisive versions. Single linkage = build the **minimum spanning tree**, then cut its longest edge, recursively. Agglomerative and divisive single linkage give the same result. Divisive Ward = split to minimise the two halves' total squared error, which needs approximations for large clusters |
| 46–48 | **Dendrograms**: root = all data, leaves = observations, height = merge distance. To get k clusters, cut the tree where it has k subtrees |
| 49–58 | Agglomerative worked example on 18, 22, 25, 27, 42, 43, then a picture-by-picture animation of merging 2-D points |
| 59–60 | Cluster similarity (min, max or average distance, distance between means or medoids). How many clusters (cut by count or by merge distance). Pros: simple, adaptive cluster shapes, gives a hierarchy. Cons: unbalanced clusters, you still choose k or a threshold |
| 61–64 | **Mean shift**: `sklearn.cluster.MeanShift(bandwidth=2)` on three synthetic blobs finds 3 clusters. Segmentation results. Pros: general purpose, any number and shape of regions, robust to outliers. Cons: must choose the kernel size (bandwidth), poor in high dimensions |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Fixed threshold (slide 19) | `g(x,y) = 1` if `f(x,y) ≥ T`, else 0 |
| Multilevel (slide 34) | class A if `T1 < f(x,y) ≤ T2`, class B if `f(x,y) > T2`, background if `f(x,y) ≤ T1` |
| Iterative threshold (slides 23, 32) | 1. start with T (e.g. the mean, or 128). 2. split into G1 (> T) and G2 (≤ T). 3. means m1, m2. 4. `T = (m1 + m2) / 2`. 5. repeat 2–4 until T changes by less than T0 |
| Otsu, class sizes (slide 27) | `P(i) = nᵢ / N` · `ω0 = Σ_{i=0..T} P(i)` · `ω1 = 1 − ω0` |
| Otsu, class means | `μ0 = Σ_{i=0..T} i·P(i) / ω0` · `μ1 = Σ_{i=T+1..L−1} i·P(i) / ω1` · global mean `μt = ω0·μ0 + ω1·μ1` |
| Between-class variance (slide 28) | `σb² = ω0(μ0 − μt)² + ω1(μ1 − μt)² = ω0·ω1·(μ1 − μ0)²` |
| Total variance (corrected) | `σt² = Σ_{i=0..L−1} (i − μt)²·P(i)`. It is the same for every threshold T |
| Otsu criterion (slide 29) | `η = σb² / σt²`. Try every T and keep the one that **maximises** η. Since σt² is fixed, that is the same as maximising σb², or minimising the within-class variance (slide 26) |
| `graythresh` (slide 30) | returns a level in [0, 1]. Multiply by 255 for 8-bit: 0.5804 → 148 |
| Linkage (slide 43) | single `min d(x,y)` · average `mean d(x,y)` · complete `max d(x,y)` · centroid `‖x̄P − x̄Q‖` · Ward `2·\|P\|\|Q\| / (\|P\| + \|Q\|) · ‖x̄P − x̄Q‖²` |
| Divisive Ward (slide 45) | split R into P, Q minimising `RSS = Σ_{i∈P} ‖xᵢ − x̄P‖² + Σ_{j∈Q} ‖xⱼ − x̄Q‖²` |

### Worked Otsu *(mine, checked by script)*

A 3-bit image (levels 0–7) with histogram `n = [2, 6, 4, 1, 1, 3, 7, 2]`, so N = 26 and μt = 92/26 = 3.54.
Class 0 is levels 0…T.

| T | ω0 | μ0 | μ1 | σb² |
|---|---|---|---|---|
| 1 | 0.308 | 0.75 | 4.78 | 3.46 |
| 2 | 0.462 | 1.17 | 5.57 | 4.82 |
| **3** | **0.500** | **1.31** | **5.77** | **4.98** |
| 4 | 0.538 | 1.50 | 5.92 | 4.85 |
| 5 | 0.654 | 2.12 | 6.22 | 3.81 |

Otsu picks **T = 3** (levels 0–3 vs 4–7). σt² = 5.63, so η = 0.88. The iterative method agrees in one step:
start at the mean 3.54, get m1 = 1.31 and m2 = 5.77, and the new T is again 3.54.

### Worked agglomerative clustering, slides 50–53 (single linkage)

Points 18, 22, 25, 27, 42, 43. The slides never name the linkage, but the updated tables use the
**minimum**, so it is single linkage. For example, after merging 42 and 43 the new row is 24, 20, 17, 15.
Complete linkage would give 25, 21, 18, 16.

| Step | Merge | Distance |
|---|---|---|
| 1 | 42 + 43 | 1 |
| 2 | 25 + 27 | 2 |
| 3 | 22 + {25, 27} | 3 |
| 4 | 18 + {22, 25, 27} | 4 |
| 5 | {18, 22, 25, 27} + {42, 43} | 15 |

Dendrogram (slide 53): `((42, 43), (((25, 27), 22), 18))`. Cutting it at k = 2 gives {18, 22, 25, 27} and
{42, 43}. *(mine)* With **complete** linkage the tree changes: 42+43 (1), 25+27 (2), 18+22 (4),
{18, 22}+{25, 27} (9), all (25). Single linkage builds a chain, complete linkage builds compact pairs. The
two-cluster cut is the same either way.

### How mean shift works *(mine; the deck only runs it)*

Put a window of radius = **bandwidth** on a data point. Move the window to the **mean** of the points inside
it, and repeat until it stops moving. It ends on a peak of the data density, a **mode**. Points whose
windows end on the same mode form one cluster. So the number of clusters comes out of the data: you choose
the bandwidth, not k. For image segmentation each pixel is a point in colour space or colour + position
space, as with L17's k-means.

## Things that are wrong or loose in the deck

- **Slide 21 has steps 2 and 3 in the wrong order.** It computes the means of R1 and R2 *before*
  partitioning the image into R1 and R2. Partition first, then take the means. Slides 23 and 32 give the
  right order.
- **Slide 27 says Otsu is "based on selecting the lowest point between two classes (peaks)".** It isn't.
  Otsu maximises the between-class variance. On a clean bimodal histogram that often lands near the
  valley, but Otsu never searches for a valley, and it works even when there isn't a visible one.
- **Slide 27's total variance sums only up to T.** It must run over all levels, 0 to L−1, around the global
  mean μt (corrected above). As written, it is part of class 0's variance. The symbol is also a ∂
  (partial-derivative sign) where σ is meant. ω and μ on that slide are class 0's only, and class 1 is
  everything above T.
- **Slide 31's MATLAB won't run.** `graythresh;` and `imshow;` have lost their arguments, and `tr` is never
  assigned. It should read `tr = graythresh(r); subplot(211); imshow(r); subplot(212); imshow(im2bw(r, tr))`.
- **Slide 22 calls `opthr(I)`.** That isn't built into MATLAB. It is a user-contributed function from
  MATLAB Central File Exchange, and the deck never says so. Without it the snippet fails. Write the
  iterative algorithm yourself, or use the built-in `graythresh` (Otsu).
- **Slide 15's labels don't match its code.** The second image is labelled "Threshold = 75", but the code
  thresholds at `> 80`.
- **Slide 34 drops the `f`**: "if T1 < (x,y) <= T2" should be `T1 < f(x,y) ≤ T2`.
- **Slides 17 and 18 describe two different "adaptive" methods.** Slide 18's text splits the image into
  sub-images and thresholds each one (Gonzalez's approach). Slide 17's `cv2.adaptiveThreshold` instead
  computes a threshold for *every pixel* from a Gaussian-weighted mean of its neighbourhood minus a constant.
- **Slides 51 → 52 skip two merges** (22 at distance 3, then 18 at 4). The table above fills them in.
- "Dendogram" (slides 46–48) is a misspelling of **dendrogram**, which slide 59 gets right.

## Links to other lectures

- **L6 / L9**: histograms. Everything in slides 5–8 and 20–38 reads the histogram.
- **L10**: morphology, for cleaning up a thresholded mask (opening removes specks, closing fills holes).
- **L11**: Sobel and Canny. Slide 8 uses them to strip boundary pixels before re-histogramming.
- **L17**: segmentation part one. K-means is the *flat* clustering that slide 39 contrasts with
  hierarchical clustering, and its colour clustering is the tool for `tomatoes.jpg`.
