# L19: Segmentation III and Object Detection: Mean Shift, Spectral Clustering, Skin Tone, Contours, Face Detection

**Multimedia Computing · Week 11 · 55 slides · Dr. Minhaz Uddin Ahmed**
Source: [week11 - Multimedia Computing L19 (segmentation 3, object and face detection).pptx](../slides/week11%20-%20Multimedia%20Computing%20L19%20(segmentation%203,%20object%20and%20face%20detection).pptx) *(6.0 MB)*
Practice: [L19 practice - faces.jpeg](../../resources/L19%20practice%20-%20faces.jpeg) ·
[L19 practice - fuzzy.png](../../resources/L19%20practice%20-%20fuzzy.png)

This continues **L18**. The eClass file is called "image segmentation 2", but L18 was already the second
segmentation deck, so this is really part three, and its second half is **object and face detection**.
Slide 2 cites Gonzalez **chapter 10** and Szeliski **chapter 5** (Segmentation, in the first edition shown on
slide 53). The deck has five parts:

- **Mean shift** (3–8): this time with an explanation (3–4). The code and pictures repeat L18 slides 61–64.
- **Spectral clustering** (9–14), then a three-slide summary comparing k-means, agglomerative and spectral
  clustering (15–17).
- **Skin tone detection** in HSV on `faces.jpeg` (18–22).
- **Contours and object detection** (23–42): a MATLAB pocket-watch example, then OpenCV `findContours` on
  L18's `detect_blob.png`, a ripe-tomato detector on L18's `tomatoes.jpg`, and the `fuzzy.png` exercise.
- **Face detection** (43–52): detection vs recognition, the sliding-window classifier, 19×19 features and a
  ROC chart. These slides are borrowed from a course called "Pattern Recognition for Vision" (the
  footer). There is no face-detection code.

Pictures to open in the pptx: the mean shift and spectral results (6, 7, 14), the HSV channel images
(18–19), the pocket-watch images (23–26), the tomato pipeline (34–36), the feature diagram (51) and the ROC
chart (52). Their content is described below.

## The practice images

Both are run with the deck's own code. *(mine)* All numbers below come from running that code with OpenCV
5.0 and scikit-learn 1.9.

**`faces.jpeg`** is a 5 × 5 grid of portrait photos (750 × 750) with very different skin tones. Slides
21–22 split it into H, S and V and keep pixels with **saturation > 40 AND hue ≤ 15**:

```python
ret, min_sat = cv2.threshold(s, 40, 255, cv2.THRESH_BINARY)      # S > 40   -> 255
ret, max_hue = cv2.threshold(h, 15, 255, cv2.THRESH_BINARY_INV)  # H <= 15  -> 255
final = cv2.bitwise_and(min_sat, max_hue)
```

The point (slides 18, 20) is that no single threshold works for every skin tone, so you combine two
("composite filtering"). The saturation filter removes grey backgrounds, white shirts, teeth and eye whites.
The hue filter keeps reds and oranges. *(mine)* My run kept 38% of the image. The faces come out white,
but so does most of the blond and brown **hair** and some of the beige backgrounds, because they are
the same warm hue. Hue alone cannot tell skin from hair. In OpenCV, H runs 0–179 (degrees ÷ 2), so 15
means about 30°. Red **wraps around**: pinkish-red pixels have H near 170–179, and this rule drops them.
That matters for lips and red clothes here (about 2% of the image), not for most skin.

**`fuzzy.png`** is the "Identify objects" exercise (slides 40–42): three coloured squares (red, green, blue)
on a background of bright colour noise (400 × 300). The task is to segment every object, draw each in its
own random colour on a black image, **print each one's area and perimeter**, and keep only objects larger
than 1,000 px². The slides' solution is: grey → `GaussianBlur` 5×5 → `adaptiveThreshold(…,
THRESH_BINARY_INV, 205, 1)` → `findContours` → drop contours with area < 1000 → `drawContours(…, -1)`
filled. *(mine)* It works. It finds 933 contours (almost all noise specks) and keeps exactly **3**: areas
29,908 (green), 17,281 (red) and 4,942 (blue). Their perimeters, which the code forgets to print (see the
errors section), are 755, 566 and 297 from `cv2.arcLength(c, True)`. The blur is what makes it work. The
squares are darker on average than the bright noise, so the inverted threshold turns them white.

The deck also reuses **L18's two practice images**. `detect_blob.png` gets contours drawn round every
shape (29–31). *(mine)* That gives 27 contours, one of them the thin frame round the picture.
`tomatoes.jpg` is the ripe-fruit example (32–36). *(mine)* It keeps 10 contours of area ≥ 300. They
are the red and orange tomatoes, plus a couple of orange blurs in the background and a yellow-brown leaf patch. The
green tomatoes are ignored, which is the intent.

## Outline

| Slides | Topic |
|---|---|
| 1–2 | Title. Contents: Gonzalez ch. 10 and Szeliski ch. 5; mean shift, spectral clustering, skin tone, contour-based and segmentation-based object detection, face detection, face detection evaluation |
| 3 | **Mean shift** idea: estimate the data density with a kernel (**KDE**), e.g. a Gaussian kernel. **Bandwidth h** = the kernel's radius of influence. Points are shifted toward the densest region (a **mode**) until the shift is negligible |
| 4 | Steps: every point starts as its own seed. Find the neighbours within radius h. The **mean shift vector** points from the current position to their mean. Move there and repeat until the move is below a tolerance (a local density maximum) |
| 5–6 | `MeanShift(bandwidth=2)` on three blobs centred at (2,2), (5,5), (8,8): finds 3 clusters (same code as L18 slide 61) |
| 7–8 | Segmentation results (Comaniciu & Meer). Pros: general purpose, any number and shape of regions, robust to outliers. Cons: choose the kernel size in advance, poor in high dimensions. Use for over-segmentation, multiple segmentations, tracking, clustering, filtering |
| 9 | **Spectral clustering** groups points by their *similarity* to each other. It maps the data into a new space using the eigenvectors of a graph built from the data. Good for **non-convex** shapes, where k-means fails |
| 10 | Step 1, the **similarity graph**: nodes are points, edge weights are similarities, e.g. the Gaussian kernel `S(i,j) = exp(−‖xᵢ − xⱼ‖² / 2σ²)`. Close points have high similarity |
| 11 | Step 2, the **Laplacian** `L = D − S`, where D is the diagonal **degree matrix** (row sums of S) |
| 12 | Step 3: eigendecompose L and keep the eigenvectors of the **k smallest eigenvalues**. Step 4: treat each row of that n × k matrix as a point and run k-means. Step 5: each original point gets its row's cluster |
| 13–14 | `SpectralClustering(n_clusters=2, affinity='rbf', gamma=10)` on two concentric circles (`make_circles`). Slide 14 shows the result (see the errors section: it splits left/right, not inner/outer) |
| 15 | Summary, **k-means**: aims to preserve the data's variance, and a new point is easy to assign. Uses: quantisation for histograms (bag of words) and summarising 20,000 photos of Rome with "greedy k-means" (Canonical Views) |
| 16 | Summary, **agglomerative**: flexible distance measures (e.g. based on boundary prediction), adapts to the data, the hierarchy is useful. Example: a polar-bear photo turned into a hierarchy of regions at λ = 0.1, 0.3, 0.7 and a boundary map (Arbeláez's UCM) |
| 17 | When to use which: k-means for summarisation, patch dictionaries and general clustering. Agglomerative for segmentation and general clustering. Spectral for relevance, summarisation and segmentation |
| 18–20 | **Skin tone detection**: skin varies too much for one threshold, so combine several. Split `faces.jpeg` into HSV channels (the slide images show single channels in grey) |
| 21–22 | Code: `S > 40` AND `H ≤ 15`, combined with `bitwise_and`. Slide 21 is the local `cv2.imshow` version; slide 22 is the Colab version with `cv2_imshow` |
| 23 | **Contour-based detection** (MATLAB, pocket-watch picture): threshold first to erase the noise specks inside the object |
| 24 | Edge finding: `img_edge = edge(x);` turns the filled silhouette into a one-pixel outline |
| 25–26 | **Contour tracing** needs a starting point, a rule for which direction to move, and must not loop forever. Slide 26 plots the traced boundary as a curve with pixel axes |
| 27–28 | **Contours** (OpenCV): a tight, closed perimeter around each object in a binary image. Any pixel above 0 is foreground, and connected pixels belong to the same object. The result is a list of contours, each a list of boundary points. Contours lead from segmentation (often thresholding) to detection |
| 29–31 | `detect_blob.png`: `adaptiveThreshold(gray, 255, GAUSSIAN_C, THRESH_BINARY, 115, 1)` → `findContours(thresh, RETR_TREE, CHAIN_APPROX_SIMPLE)` → `drawContours(img2, contours, -1, (255,0,255), 4)`, so every outline is drawn in magenta |
| 32–36 | **Ripe tomato detection** on `tomatoes.jpg` (titled "Edge detection"). (a) Keep hue ≤ 25 (red/orange). (b) Canny edges (100, 200), inverted and eroded so the borders get thicker. (c) AND the two masks, so touching tomatoes are cut apart along their edges. (d) Find contours, skip area < 300, draw each and mark its **centroid** from the moments. Slides 35–36 show the threshold, Canny and final images |
| 37 | Toolbox: value thresholding, adaptive thresholding, edge detection, Gaussian blur against noise, dilation/erosion against speckles |
| 38–39 | More: histogram-based segmentation, other colour spaces, **watershed**, prior-knowledge methods. Use what you know: expected size and orientation, a known black background |
| 40–42 | `fuzzy.png` exercise and solution (above) |
| 43–44 | A **feature** is any image part or property that helps the task. Good features are invariant to lighting and scale. **Detection** (is there a face, where) usually comes before **recognition** (whose face). The same feature, e.g. the distance between the eyes, can serve both |
| 45 | Object recognition splits into **detection** ("Is there a face? Where is Jane?") and **identification** ("Who is it? Jane or Erik?") |
| 46 | Recognition must be invariant to **external** parameters (pose, illumination) and, for detection, **internal** ones (identity, expression). It applies to many classes (signs, cars) |
| 47–48 | **Object detection**: find whether objects of a class are in the image and where. It is hard because the classifier must cover every member of the class, the negative class is "everything else", and the false-positive rate must be tiny |
| 49 | **Face detection basic scheme**: train a classifier offline on face and non-face examples. Then slide a window over the image at **every location and several resolutions**, extract a feature vector (x₁ … xₙ) from each window and classify it |
| 50 | Train on a training set. Test on a **labelled** test set and count correct detections and false positives |
| 51 | **Features** from a 19×19 window. **Gray**: histogram-equalise, mask the corners → 283 values in [0, 1]. **Gradient**: equalise, x–y Sobel → 17×17. **Haar wavelets**: transform, normalise → 1,740 values |
| 52 | **ROC** on the CMU test set 1 (127 images, 479 faces, 56.8 million windows). x = false positives per inspected window, y = fraction of faces found. Grey and grey + gradient features are best; Haar is worst at low false-positive rates |
| 53–55 | References: Gonzalez & Woods *Digital Image Processing* 4e, Szeliski *Computer Vision: Algorithms and Applications*. Questions. Thank you |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Mean shift step *(mine; slides 3–4 in words)* | `m(x) = Σᵢ K(xᵢ − x)·xᵢ / Σᵢ K(xᵢ − x)`. Move x to m(x), repeat. The **mean shift vector** is `m(x) − x`. With a flat kernel, K = 1 inside radius h and 0 outside, so m(x) is the plain mean of the neighbours |
| Bandwidth *(mine, by running slide 5)* | on slide 5's blobs: h = 0.5 → 45 clusters, 1 → 5, **2 → 3** (centres ≈ (1.9, 2.0), (4.9, 4.9), (8.1, 8.0)), 4 → 2, 6 → 1. Too small over-segments, too large merges |
| Gaussian similarity (slide 10) | `S(i,j) = exp(−‖xᵢ − xⱼ‖² / 2σ²)`. In scikit-learn, `affinity='rbf'` uses `exp(−γ‖xᵢ − xⱼ‖²)`, so **γ = 1 / 2σ²**. γ = 10 means σ ≈ 0.22 |
| Degree, Laplacian (slide 11) | `Dᵢᵢ = Σⱼ S(i,j)` · `L = D − S`. The smallest eigenvalue is always 0, with the constant vector (1, 1, …, 1) |
| HSV in OpenCV | H 0–179 (degrees ÷ 2), S and V 0–255. Skin rule (slide 22): S > 40 and H ≤ 15. Ripe rule (slide 32): H ≤ 25 |
| `THRESH_BINARY` vs `_INV` | BINARY: `> T → 255`, else 0. BINARY_INV is the opposite, so `≤ T → 255` |
| `adaptiveThreshold(…, block, C)` | per pixel: T = Gaussian-weighted mean of the block × block neighbourhood − C. Block must be odd (115, 205 here) |
| Contour properties | area `cv2.contourArea(c)` · perimeter `cv2.arcLength(c, True)` · centroid `cx = m10/m00`, `cy = m01/m00` from `cv2.moments(c)` (m00 is the area) |
| `findContours` flags | `RETR_TREE` keeps the nesting (holes inside objects). `CHAIN_APPROX_SIMPLE` stores only the corner points of straight runs. Index −1 in `drawContours` draws all contours; thickness −1 fills them |

### Worked spectral clustering *(mine, checked by script)*

Four points in two pairs. Strong similarity inside each pair (1), weak between the pairs (0.1, between
points 2 and 3):

```
S = | 0    1    0    0 |     D = diag(1, 1.1, 1.1, 1)     L = D − S = |  1    −1     0     0  |
    | 1    0    0.1  0 |                                              | −1    1.1  −0.1   0  |
    | 0    0.1  0    1 |                                              |  0   −0.1   1.1  −1  |
    | 0    0    1    0 |                                              |  0    0    −1     1  |
```

The eigenvalues are **0, 0.095, 2, 2.105**. The eigenvector for 0 is constant (all 0.5), so it can't split
anything. The next one (the **Fiedler vector**) is (0.52, 0.47, −0.47, −0.52). Its signs split the points
into {1, 2} and {3, 4}, cutting the weak 0.1 edge. For k = 2 you take both eigenvectors, so each point
becomes a 2-D row, and k-means on those rows gives the same split. A small second eigenvalue means a cheap
cut, so the graph almost falls apart into two pieces.

### Why the tomato pipeline ANDs edges with the colour mask *(mine)*

The hue mask alone (slide 35) merges the touching tomatoes into one white blob, so `findContours` would
return one object. The Canny edges trace the outline of each tomato. Invert them (edges = 0) and erode
(thicker black lines), then AND with the mask: the black lines cut the blob into separate tomatoes. The
area ≥ 300 filter then drops the specks the cutting leaves behind.

### MATLAB contour tracing *(mine; slides 23–26 give no code)*

`bw = imbinarize(rgb2gray(I)); bw = bwareaopen(bw, 50); e = edge(bw); B = bwboundaries(bw);
plot(B{1}(:,2), B{1}(:,1))`. `bwboundaries` does slide 25's tracing (start point, direction, stop on
return) for every object, and the plot is slide 26's picture. Note the column/row swap when plotting.

## Things that are wrong or loose in the deck

- **Slide 14's own result is a failure.** The colours split the picture into a **left half and a right
  half** of both circles, not inner ring vs outer ring. That is exactly what k-means would do, and the
  opposite of slide 9's claim. *(mine, by running slide 13)* With `gamma=10` the inner and outer circles
  are never separated (adjusted Rand index 0 on 8 random datasets). `gamma=25` works on 7 of the 8 and
  `gamma=30` or more works on all 8, as does `affinity='nearest_neighbors'`. Spectral clustering
  only works when σ is small compared with the gap between the rings. That is the bandwidth problem again.
- **Slides 27–28 describe the wrong algorithm.** An "iterative energy reduction algorithm … an elastic
  film that … squeezes in around all the objects" is an **active contour (snake)**. OpenCV's
  `findContours`, which the code uses, does no energy minimisation. It is **border following** (Suzuki &
  Abe): scan the binary image, and when it hits a foreground pixel, walk round its boundary until it
  returns to the start (slide 25's description). It finishes because each border is finite, not because
  something "converges". Slide 27's last sentence is also cut off ("…part of the same").
- **Slide 40 asks you to print each object's perimeter; slide 42's code never does.** It prints only the
  area. Add `print(cv2.arcLength(c, True))`.
- **Slide 22 (Colab) never shows the answer.** `#cv2_imshow(final)` is commented out, so you see only the
  HSV split and the two intermediate masks. `cv2.waitKey(0)` and `cv2.destroyAllWindows()` do nothing in
  Colab. Slide 21's local version shows "Final" correctly.
- **Slides 29–30 use `cv2.COLOR_RGB2GRAY` on an image from `cv2.imread`, which is BGR.** It should be
  `COLOR_BGR2GRAY`. As written, the red and blue weights are swapped. Here it doesn't change the result (27
  contours either way), but on colour-critical images it would. Slide 41 gets it right.
- **Slide 12, "smallest k eigenvalues (other than 0)", is loose.** The standard algorithm takes the first k
  eigenvectors, including eigenvalue 0. Only the plain two-way cut uses just the second one. If the
  graph is already split into k separate pieces, there are k zero eigenvalues, and those are exactly the
  vectors you want, so skipping "the zeros" would throw away the answer.
- **Slide 3 says the kernel is typically Gaussian; slide 4 uses a hard "hypersphere of radius h"** (a flat
  kernel). Both are valid mean shift kernels. scikit-learn's `MeanShift`, used on slide 5, is the flat one.
- **Slides 32–33 are titled "Edge detection"**, but they are the whole ripe-tomato detector (colour
  threshold + Canny + contours + centroids). The rule H ≤ 25 also keeps orange and some yellow-brown
  areas, not only ripe red.
- **Slide 52 is labelled "ROC" without saying what was classified.** The legend's "poly2" and "lin" are
  **SVM kernels** (2nd-degree polynomial and linear). The deck never mentions SVMs. The x-axis is false
  positives *per inspected window* (around 10⁻⁵), not the false-positive rate of a textbook ROC.
- **Slide 19's arrow** points from the dark HSV channel to a greyscale picture under the caption "Split to
  HSV", which reads backwards. The split goes from colour to channels.
- **Slide 2 promises "segmentation based object detection"** but has no slide of that name. It is slides
  37–42.

## Links to other lectures

- **L7**: colour spaces. HSV is the basis of the skin and tomato rules.
- **L6 / L9**: histograms. Histogram equalisation is the first step of every face feature on slide 51.
- **L10**: morphology. Slide 32 erodes the edge map, and slide 37 lists dilation/erosion against
  speckles.
- **L11**: Gaussian blur, Sobel and Canny (slides 32, 41, 51).
- **L17**: k-means, which slides 12, 15 and 17 build on, and which fails on the circles.
- **L18**: thresholding, adaptive thresholding, hierarchical clustering and the first mean shift slides.
  Both L18 practice images are used here (`detect_blob.png` on 29–31, `tomatoes.jpg` on 32–36), which
  answers L18's open question of what `tomatoes.jpg` was for.
