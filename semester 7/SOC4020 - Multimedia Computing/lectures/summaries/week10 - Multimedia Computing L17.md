# L17: Image Segmentation I: Discontinuities, Grouping, Background Subtraction, K-means

**Multimedia Computing · Week 10 · 65 slides · Dr. Minhaz Uddin Ahmed**
Source: [week10 - Multimedia Computing L17.pptx](../slides/week10%20-%20Multimedia%20Computing%20L17.pptx) *(4.2 MB)*

The reference slide (63) lists Gonzalez **chapter 10** (image segmentation) and Szeliski **chapter 5**
(segmentation, in the 1st edition whose cover is shown). The point/line/edge masks (slides 7–21) are
Gonzalez. The middle of the deck (tokens, Gestalt grouping, background subtraction, shot boundaries,
clustering: slides 11, 22–47) carries labels like "Figure 14.1", "figure 14.11" and "chp-9". Those don't
fit either listed book. They appear to come from Forsyth & Ponce, *Computer Vision: A Modern Approach*,
whose "segmentation by clustering" chapter is ch. 14 in the 1st edition and ch. 9 in the 2nd. The k-means
part (48–62) ends with an OpenCV practice script.

Segmentation is week 14 on the eClass syllabus and week 13 in his own plan. It arrived in week 10, and L18
continues it. Slides 7 and 12–17 repeat **L11**'s point/line/edge masks from the segmentation angle. Many
slides are pictures: the masks (12, 15), the formal conditions (10) and the k-means figures (54–60). The
masks and formulas are copied below.

## Outline

| Slides | Topic |
|---|---|
| 3–6 | **Segmentation** = partition an image into regions that match objects, and pull out the **region of interest (ROI)**. No single algorithm works for every image. Uses: summarizing video, finding people, finding buildings in satellite images, image search |
| 7, 12–14 | **Point detection**: slide a 3×3 mask, compute the response R, mark a point where `\|R\| ≥ T`. OpenCV `filter2D` demo |
| 8 | Taxonomy. **Discontinuity** (boundary approach): point, line, edge detection. **Similarity** (region approach): thresholding, region growing, region splitting and merging. Plus **clustering** |
| 9–10 | A segmentation splits R into regions R1…Rn, and the formal conditions (below) |
| 11 | **Tokens** = whatever we group (pixels, points, surface elements). **Top-down**: tokens belong together because they lie on the same object. **Bottom-up**: because they are locally coherent |
| 15–16 | **Line detection**: four masks (horizontal, +45°, vertical, −45°) and their results |
| 17–18 | Edge detection example (Sobel horizontal, vertical, combined). Using several masks together decides whether a pixel is a point, part of a line or an edge |
| 19–21 | **Edge linking**: noise and uneven lighting break the boundaries, so link nearby edge pixels whose gradient **strength** and **direction** are similar |
| 22–28 | **Segmentation by clustering**: get a compact representation and find components that belong together. Examples: super-pixels, fitting lines to edge points, fitting a fundamental matrix. Clustering by **partitioning** (split an image into coherent regions, a video into shots) vs **grouping** (collect tokens that form a line) |
| 29–33 | **Gestalt**: context changes perception. The Müller-Lyer illusion. Grouping factors: proximity, similarity, common fate, common region, parallelism, symmetry, continuity, closure. Occlusion as a grouping cue, and illusory contours |
| 34–36 | **Background subtraction**: if you know the background, foreground = pixels that differ a lot. Estimate the background with a moving average, subtract, threshold, clean up with morphology. Uses: office scenes, traffic, surveillance |
| 37–38 | **Shot boundary detection**: a cut gives a big difference between consecutive frames. Distances: frame, histogram, block or edge differences. Used to index video and pick a representative frame per shot |
| 39–46 | Background subtraction in detail: the per-frame algorithm, three background models, `createBackgroundSubtractorMOG2` demo, results at 80×60 and 160×120, and problems (dynamic backgrounds, shadows, gradual or sudden lighting changes, camera motion) |
| 47 | **Agglomerative** (start with every point alone, merge the closest pair) vs **divisive** (start with one cluster, split the most separated) |
| 48–53 | **K-means** / **Lloyd's algorithm**: objective, complexity, 1-D worked example |
| 54–60 | K-means on images: on grey levels (MATLAB one-liner; the result is "noisy"), on colour (11 segments), and on colour + position `(r, g, b, x, y)` (20 segments, spatially coherent) |
| 61–62 | Practice: `cv2.kmeans` on `billiard.jpg` with K = 4, each pixel painted with its cluster's centre colour |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Mask response (slide 7) | `R = w1·z1 + w2·z2 + … + w9·z9`. Detected where `\|R\| ≥ T` |
| Point mask (slide 12) | `[-1 -1 -1; -1 8 -1; -1 -1 -1]`. It sums to 0, so flat regions give R = 0 |
| Line masks (slide 15) | horizontal `[-1 -1 -1; 2 2 2; -1 -1 -1]` · +45° `[-1 -1 2; -1 2 -1; 2 -1 -1]` · vertical `[-1 2 -1; -1 2 -1; -1 2 -1]` · −45° `[2 -1 -1; -1 2 -1; -1 -1 2]` |
| Segmentation conditions (slide 10, corrected) | `∪ Ri = R` · each Ri is connected · `Ri ∩ Rj = ∅` for i ≠ j · `P(Ri) = TRUE` · `P(Ri ∪ Rj) = FALSE` for **adjacent** Ri, Rj |
| Edge linking (slide 21) | link (x, y) and a neighbour (x′, y′) if `\|∇f(x,y) − ∇f(x′,y′)\| ≤ T` and `\|α(x,y) − α(x′,y′)\| ≤ A`. Here ∇f means the gradient *magnitude* and α its angle |
| Background subtraction (slide 41) | `d(x,t) = \|I(x,t) − I0(x,t)\|`, `d_T = d > thresh`, then erode `d_T`. Objects are where `d_T ≠ 0` |
| Background models (slide 42) | **offline average** `I0 = (1/T)·Σ I(x,t)` · **adjacent frame difference** `I0(x,t) = I(x,t−1)` · **moving average** `I0 = (w_a·I(x,t) + Σᵢ wᵢ·I(x,t−i)) / w_c` |
| Shot boundary | distance(frame t, frame t−1) > threshold → cut |
| K-means objective (slide 50) | minimise the **within-cluster sum of squares** `Σᵢ Σ_{x∈Sᵢ} ‖x − μᵢ‖²` |
| Lloyd's algorithm (slide 52) | choose k → pick k starting centres → assign each point to its nearest centre → recompute each centre as the mean of its points → repeat until nothing moves |
| Complexity (slide 51) | NP-hard in general, so heuristics like Lloyd's are used. Exact in `O(n^(dk+1) log n)` for fixed k and d |

### Worked k-means, slide 53

Data (from the number line): **2 3 4 7 9 10 11 12 16 18 19 23 24 25 30**.

**Example 1, centres 3, 16, 25** (on the slide):

| Iteration | Clusters | New centres |
|---|---|---|
| 1 | {2, 3, 4, 7, 9} · {10, 11, 12, 16, 18, 19} · {23, 24, 25, 30} | 5 · 14.33 · 25.5 |
| 2 | same | same → converged |

**Example 2, centres 3, 12, 19** (left as an exercise on the slide; answer is mine, checked by script):

| Iteration | Clusters | New centres |
|---|---|---|
| 1 | {2, 3, 4, 7} · {9, 10, 11, 12} · {16, 18, 19, 23, 24, 25, 30} | 4 · 10.5 · 22.14 |
| 2 | {2, 3, 4, 7} · {9, 10, 11, 12, **16**} · {18, 19, 23, 24, 25, 30} | 4 · 11.6 · 23.17 |
| 3 | same | same → converged |

The close calls: 7 goes to 3, not 12 (distance 4 vs 5). In iteration 2, 16 moves because
`|16 − 10.5| = 5.5 < |16 − 22.14| = 6.14`. **Different starting centres give a different answer**: the
within-cluster sum of squares is 136.3 for Example 1 and 138.0 for Example 2. K-means only finds a *local*
minimum, which is why `cv2.kmeans` takes an `attempts` argument (10 on slide 61) and keeps the best run.

### Using k-means on an image (slides 55–62)

Each pixel becomes a point in feature space: grey level (1-D), colour `(R, G, B)` (3-D), or colour plus
position `(r, g, b, x, y)` (5-D). Cluster, then paint each pixel with its cluster's mean. Clustering on
colour alone is really vector quantization: clusters needn't be spatially connected, so the result looks
speckled ("noisy"). Adding x, y makes segments spatially coherent. Scale the features before mixing colour
and position (slide 49's "careful about scaling").

## Things that are wrong or loose in the deck

- **Slide 10 writes `Ri ∩ R1 = ∅ (for all i and j): i ≠ j`.** It should be `Ri ∩ Rj`. The last condition
  also needs "**adjacent**": two separate dark objects can both be "dark", and their union still satisfies
  P. The condition is only meant to stop *neighbouring* regions that should have been one region.
- **Slide 14's point-detection code doesn't do point detection.** There is no `|R| > T` step, so it shows
  the raw filter response. That is why the result lights up the whole line as well as the dots: the mask
  responds to lines too, and only a threshold would separate them. Also, `cv2.filter2D(image, -1, kernel)`
  keeps the uint8 type, so responses are clipped to 0–255. Negative responses become 0, so you get
  `max(R, 0)`, not `|R|`, and large ones saturate at 255 (I checked on a synthetic image). A fix:
  `R = cv2.filter2D(image.astype(np.float32), -1, kernel)`, then `points = np.abs(R) >= T`.
- **Slide 36 is not background subtraction.** The `cvtColor` line is commented out, so the "grey" image is
  still 3-channel. The "background" is a constant grey of 128, so the code just thresholds `|I − 128| > 30`
  per colour channel. The mask is 3-channel, which is why the "Foreground Mask" output is magenta and green
  (matplotlib ignores `cmap` for colour images). Real background subtraction needs a background *image*:
  an empty-table frame, or a model like slide 40's MOG2.
- **Slide 40 mixes Colab and desktop OpenCV.** `cv2_imshow` (Colab's replacement for `cv2.imshow`) prints
  two images per frame into the notebook output. The `waitKey` / press-`q` exit is meant for a desktop
  OpenCV window, which Colab doesn't open. On a desktop use `cv2.imshow`. In Colab, process a fixed number
  of frames instead.
- **Slide 51 lost a superscript.** "O(ndk+1 log n)" means `O(n^(dk+1) log n)`.
- **Slide 53's note says "Lloyd's algorithm is a special case of the K-means algorithm."** Read it the
  other way round. *k-means* is the problem (minimise the WCSS). *Lloyd's algorithm* is the usual heuristic
  for solving it, the procedure slides 48–52 describe.
- Slide 2 lists **Interactive Segmentation**, but no slide covers it.
- Slides 37 and 45 are garbled in places ("much shorter subsequences within the same object", "average
  exceeds an somewhat smaller thresold"). The meaning: a video is made of shots, and slide 45 compares two
  threshold levels.

## Links to other lectures

- **L10**: morphology. The erosion step on slide 41 and the "clean up with morphological operations" trick
  on slide 34.
- **L11**: point and line masks, Sobel, edges. Slides 7 and 12–17 here are that material reused.
- **L12**: pattern classification. K-means is the *unsupervised* counterpart of nearest-class-mean: same
  "nearest mean" rule, but the means are learned without labels.
- **L14**: video. Shot boundaries and background subtraction run on its frames.
- **L18**: continues with thresholding, hierarchical clustering and mean shift.
