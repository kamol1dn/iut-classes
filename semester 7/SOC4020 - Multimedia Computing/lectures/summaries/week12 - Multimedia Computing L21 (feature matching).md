# L21: Feature Matching: Template Matching, Harris Corners, Blobs and Scale, SIFT

**Multimedia Computing · Week 12 · 78 slides · Dr. Minhaz Uddin Ahmed**
Source: [week12 - Multimedia Computing L21 (feature matching).pptx](../slides/week12%20-%20Multimedia%20Computing%20L21%20(feature%20matching).pptx) *(9.5 MB)*
Practice: [L21 practice - player.jpg](../../resources/L21%20practice%20-%20player.jpg) ·
[L21 practice - templ.jpg](../../resources/L21%20practice%20-%20templ.jpg) (template) ·
[L21 practice - som.jpg](../../resources/L21%20practice%20-%20som.jpg)

The question of this lecture: how do you find **the same thing in two different pictures**? Slide 2 cites
Szeliski **chapter 4** ("Feature detection and matching", first edition). The deck has four parts:

- **Template matching** (3–8): slide a small picture over a big one and score every position. Simple, but it
  breaks as soon as the object is bigger, smaller or rotated (6).
- **Why features** (9–20): build a panorama by finding matching points in two photos. Three problems:
  find the same points again, describe them so they can be told apart, and survive wrong matches.
- **Corners and blobs** (21–49): the **Harris corner detector** with its eigenvalue maths (21–33), what it is
  and isn't invariant to (34–38), then **blobs and automatic scale selection** with the Laplacian (39–48).
- **SIFT** (50–74): the Scale-Invariant Feature Transform. Its four steps (56–62), OpenCV's API (63–66) and
  two code slides (67, 72) with output pictures (68–73). The exercise (74) is SIFT matching on a video.

Most of the maths (23–26, 45, 49) is pasted as pictures, so the text extractor misses it. The formulas below
were read off the rendered slides. Pictures to open in the pptx: the flat/edge/corner diagram (22), the cow
example of every Harris step (29–33), the blob and scale plots (41–47), the SIFT descriptor diagrams (52–53)
and the pyramid of Gaussians and DoGs (57).

## The practice images

All numbers below come from running the deck's own code with OpenCV 5.0. *(mine)*

**`player.jpg`** (544 × 363) is a youth football match: a goalkeeper in red, three players, and a **white**
ball on the grass in the lower left. **`templ.jpg`** (56 × 48) is the template: a close-up of a
**yellow** ball with dark patches. It is a different ball from the one in the photo. Slide 8 shows the same
pair. The deck's code (slide 7) reads them as `players.jpg` and `template.jpg`, so rename the files or
fix the names first (see the errors section).

Slide 7 runs `cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)` on the greyscale images and takes
the **maximum** of the result map. *(mine)* It does find the ball: the best score is **0.466** at
(132, 243), and a 56 × 48 box from there covers the white ball. But it only just wins. The next peaks are
0.437 (beside the goalkeeper's legs) and 0.433 (a patch of fence above a parked car). A score of 0.47 out of 1 is a weak match,
because the template is a different ball with different colours. It works only because both are round with
dark patches. The other methods do worse: `TM_CCORR`, `TM_CCORR_NORMED`, `TM_SQDIFF` and
`TM_SQDIFF_NORMED` all pick bright background patches near the top left, not the ball. Resizing the template
(0.5× to 1.25×) never pushes the score above 0.54. **SIFT finds 0 good matches** between the template and
the photo. The template gives only 50 keypoints, and none of them describe the white ball.

Slide 67 runs SIFT on `players.jpg`. *(mine)* It finds **1,364 keypoints**, each with a 128-number
descriptor. For comparison, Harris (`cv2.cornerHarris(img, 2, 3, 0.04)`, R > 1% of the max, local maxima
only) finds 224 corners.

**`som.jpg`** (728 × 512) is a photo of part of a **5,000 so'm banknote**: a pink plate and pot, the
large "5000", and green and yellow patterned panels. **The deck never mentions it.** It is a good image
for the slide 74 idea (find the same object again after it moves). *(mine)* I rotated it 30°, shrank it
to 0.6×, and changed the brightness (0.8 × I + 20). Then SIFT + the ratio test (slide 62):

| Step | Result |
|---|---|
| Keypoints | 1,831 in the original, 393 in the shrunk copy |
| Nearest neighbour only (no ratio test) | 1,831 matches, only **236 correct** (13%) |
| Ratio test, distance ratio < 0.8 | **277** matches kept, **227 correct** (82%) |
| What the ratio test threw away | 1,554 matches, of which 1,545 were wrong. It lost only 9 correct ones (about 4%) |
| RANSAC homography on the 277 | 228 inliers. The recovered matrix is `[[0.52, 0.30], [−0.30, 0.52]]`, which is exactly 0.6 × (cos 30°, sin 30°) |

That last row is slide 18's "problem 3" solved: even with some wrong matches you can recover the exact
transformation. The ratio test numbers match Lowe's claim on slide 62 (90% of false matches removed,
under 5% of correct ones lost).

## Outline

| Slides | Topic |
|---|---|
| 1–2 | Title. Contents: Szeliski ch. 4, template matching, Harris corners, blobs, descriptors, SIFT, SIFT in OpenCV, examples |
| 3–4 | **Template matching**: slide the template over the image. At each position compare the pixels and write a score into a result map. A slight overlap gives a grey value, a perfect overlap a white one |
| 5 | Inputs (frame, template "scaled" to the object's size), the six OpenCV methods (`TM_CCOEFF`, `TM_CCOEFF_NORMED`, `TM_CCORR`, `TM_CCORR_NORMED`, `TM_SQDIFF`, `TM_SQDIFF_NORMED`), output map. "Brightest spot = best matching x,y" (true for 4 of the 6, see errors) |
| 6 | **Limitations**: not scale invariant, not rotation invariant, needs a well-formed template. The picture: a bigger triangle ≠, a rotated triangle ≠, only an identical one = |
| 7–8 | Code: `matchTemplate(…, TM_CCOEFF_NORMED)` → `minMaxLoc` → print the best score and position → draw a circle there on the result map |
| 9–10 | **Kinds of features**: **keypoints / interest points** (corners, peaks, doorways), regions, **edges** (matched by orientation and profile; mark object boundaries) and straight lines (give vanishing points, so camera parameters) |
| 11–15 | Motivation: a **panorama** (Brown & Lowe 2003). Detect feature points in both images, find corresponding pairs, use the pairs to align the images |
| 16–18 | The three problems: (1) detect the same point independently in both images, so you need a **repeatable detector**; (2) recognise which point corresponds to which, so you need a **reliable, distinctive descriptor**; (3) estimate the transformation despite some wrong pairs |
| 19 | Good features: **repeatability** (found again after geometric and lighting changes), **saliency** (distinctive), **compactness** (far fewer features than pixels), **locality** (small area, so robust to clutter and occlusion) |
| 20 | Uses: motion tracking, alignment, 3D reconstruction, object recognition, image search, robot navigation |
| 21–22 | **Corners**: around a corner the gradient has two or more dominant directions. Look through a small window: **flat** = no change when you shift it in any direction; **edge** = no change along the edge; **corner** = big change in every direction |
| 23 | Shift the window W by (u, v) and sum the squared differences: the SSD "error" E(u, v) |
| 24 | E(u, v) rewritten as `[u v] H [u v]ᵀ`, with H built from Ix², IxIy, Iy². Which shift directions give the largest and smallest E? The eigenvectors of H |
| 25 | Eigenvalue review: `Ax = λx`, solve `det(A − λI) = 0`. For a 2 × 2 matrix the solution is the λ± formula below |
| 26 | **x₊** = direction of largest increase in E, **λ₊** = how much. **x₋** = direction of smallest increase, **λ₋** = how much. On a vertical edge, x₊ points across the edge and x₋ along it |
| 27 | Recipe: gradient at each pixel → H → eigenvalues → keep points with **λ₋ > threshold** → keep only local maxima. A checkerboard shows I, λ₊ (bright on all edges) and λ₋ (bright only at the corners) |
| 28 | **Harris steps**: (1) Gaussian derivatives at each pixel, (2) second moment matrix H in a Gaussian window, (3) corner response **R**, (4) threshold R, (5) **non-maximum suppression** (keep local maxima) |
| 29–33 | The steps on two photos of a toy cow, taken at different angles: R as a heat map (30), R > threshold as white blobs (31), local maxima as single dots (32), the corners drawn back on both photos (33). Many of the same corners appear in both |
| 34 | **Invariance**: the image changes and the feature value stays the same. **Covariance**: the image changes and the detected location moves with it. Want invariance to lighting, covariance to geometry |
| 35 | Transformations: geometric (rotation, scale, affine: valid for an orthographic camera and locally flat objects) and photometric (affine intensity change I → aI + b) |
| 36 | **Rotation**: the ellipse of H turns but keeps its shape (same eigenvalues). R is **invariant**, the corner location is **covariant** |
| 37 | **Scaling**: zoom in on a corner and each small window sees only a gently curving edge, so every point is classified as an edge. **Not invariant** to scale |
| 38 | **Intensity**: only derivatives are used, so I → I + b changes nothing. I → aI scales R, so points near the threshold can drop in or out. **Partially invariant** |
| 39 | Edges and corners describe boundaries. What about the texture inside an object (a leopard's spots)? Blobs |
| 41 | **Scale covariance**: detect matching regions in two zoomed versions of a picture independently. Plots: the same building at two zoom levels. The response-vs-scale curves peak at 10.1 and 3.89, a ratio of about 2.6, the zoom factor between the photos |
| 40, 42 | **Blobs**. An edge is one "ripple"; a blob is two ripples close together. The Laplacian response is largest at the centre of the blob **when the Laplacian's scale matches the blob's size** |
| 43–44 | Convolve with Laplacians at several σ and look for the peak. Problem: the plain response shrinks as σ grows. Fix: **scale normalisation**. Multiply a first derivative of Gaussian by σ, the Laplacian (second derivative) by **σ²** |
| 45 | The best match is when the Laplacian's zero ring lies on the blob's edge: `1 − (x² + y²)/2σ² = 0`, so **σ = r/√2** for a circle of radius r |
| 46–47 | **Characteristic scale** (Lindeberg 1998) = the σ that gives the peak normalised Laplacian at the blob centre. Example: sunflowers (40) and a butterfly (47) with circles of the detected sizes |
| 48 | **Affine adaptation**: the window should fit the region's shape. Start with a circle, compute H, reshape the window into the ellipse H describes, recompute, iterate |
| 49 | Harris response depends only on the eigenvalues of `M = Σ w(x,y) [[Ix², IxIy], [IxIy, Iy²]]` (the same matrix as H, now with Gaussian weights w), so it does not change with rotation |
| 50–51 | **SIFT** (David Lowe). Object recognition with SIFT: store keypoints from reference images in a database; match each new keypoint to its **nearest neighbour by Euclidean distance**; group matches that agree on position, scale and rotation with a **Hough transform**; clusters of 3 or more go to a detailed check, and the outliers are removed |
| 52 | Descriptor idea: a 16 × 16 window, the edge orientation of each pixel, drop weak gradients, build an orientation histogram |
| 53 | **4 × 4 cells × 8 orientation bins = 128 numbers**. Gaussian weighting from the centre. Normalised to length 1 |
| 54 | Why it is robust: cells tolerate small shifts, orientation is normalised, unit length removes contrast changes, histograms tolerate small deformations |
| 55–56 | A corner stops being a corner when you zoom in (same picture as 37). SIFT's steps: (1) scale-space extrema, (2) keypoint localisation, (3) orientation assignment, (4) descriptor; then matching |
| 57–58 | **Step 1**: blur the image with increasing σ, subtract neighbouring blurred images (**DoG**, a cheap approximation of LoG), repeat on a half-size image for the next **octave**. Small σ responds to small blobs, large σ to large ones |
| 59 | **Step 2**: refine each extremum's position with a Taylor expansion. Reject it if its contrast is below **0.03** (Lowe's paper). In OpenCV this is `contrastThreshold` |
| 60 | **Step 3**: around the keypoint, a **36-bin** histogram of gradient directions (10° each). The highest peak gives the orientation. Every other peak above **80%** of it creates an extra keypoint at the same place with that orientation |
| 61 | **Step 4**: 16 × 16 neighbourhood → 16 blocks of 4 × 4 → an 8-bin histogram each → **128 values** |
| 62 | **Matching**: nearest neighbour. If the closest / second-closest distance ratio is **> 0.8**, reject. This removes about 90% of false matches and only about 5% of correct ones |
| 63–66 | OpenCV 2.x C++ API: `SIFT(nfeatures=0, nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10, sigma=1.6)` and `operator()(img, mask, keypoints, descriptors, useProvidedKeypoints)`. The parameters are explained below |
| 67–68 | Python: `cv2.SIFT_create()` → `detectAndCompute(image, None)` → `drawKeypoints(…, DRAW_RICH_KEYPOINTS)` → matplotlib. Output: a toy monster (Sulley) with small keypoint marks |
| 69–71 | A hummingbird and a rotated copy (69), its keypoints as circles with a radius line for size and orientation (70), and the matches between the two copies as coloured lines (71) |
| 72–73 | The OpenCV tutorial code on `home.jpg`: `detect` → `drawKeypoints` → `imwrite`, then `detectAndCompute`. Slide 73: matches between two views of the toy |
| 74 | **Exercise**: apply SIFT keypoint matching to a video (.avi) file |
| 75–78 | References (OpenCV docs; Szeliski's book cover), questions, thank you |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Template result map size | for an image W × H and template w × h: **(W − w + 1) × (H − h + 1)**. Each entry is the score of the template placed with its **top-left corner** there. *(mine)* 544 × 363 and 56 × 48 give 489 × 316 |
| `TM_SQDIFF` | `Σ (T − I)²`. 0 = perfect. **Best = minimum** |
| `TM_CCORR` | `Σ T · I`. Bigger = better, but bright areas score high whatever they look like |
| `TM_CCOEFF` | the same with each patch's mean subtracted first: `Σ T′ · I′` |
| `_NORMED` versions | divide by `√(Σ T′² · Σ I′²)`. `TM_CCOEFF_NORMED` is the **correlation coefficient**, from −1 to 1, and does not care about brightness or contrast. 1 = perfect |
| SSD of a shift (slide 23) | `E(u,v) = Σ₍ₓ,ᵧ₎∈W [I(x+u, y+v) − I(x,y)]²` |
| Taylor step (skipped in the deck) | `I(x+u, y+v) ≈ I(x,y) + Ix·u + Iy·v`, so `E(u,v) ≈ Σ (Ix·u + Iy·v)² = [u v] H [u v]ᵀ` |
| Second moment matrix (24, 49) | `H = M = Σ w(x,y) [[Ix², IxIy], [IxIy, Iy²]]`. Ix, Iy are the x and y gradients (e.g. Sobel). w = 1 in the window (slide 24) or a Gaussian (slides 28, 49) |
| Eigenvalues of a 2 × 2 (slide 25) | `λ± = ½ [ (h₁₁ + h₂₂) ± √(4 h₁₂ h₂₁ + (h₁₁ − h₂₂)²) ]` |
| What λ₊, λ₋ say | both small → **flat**. λ₊ big, λ₋ small → **edge**. Both big → **corner** |
| Harris response *(mine; used but not given in the deck)* | `R = det(H) − k·(trace H)² = λ₊λ₋ − k(λ₊ + λ₋)²`, k ≈ 0.04–0.06. R ≫ 0 corner, R < 0 edge, \|R\| small flat. It avoids computing square roots |
| Shi–Tomasi *(mine; this is slide 27's rule)* | keep points with `min(λ₊, λ₋) = λ₋ > threshold`. OpenCV: `cv2.goodFeaturesToTrack` |
| Scale-normalised Laplacian (44) | `σ² (Gxx + Gyy)`. First derivatives × σ, second derivatives × σ² |
| Best scale for a disc (45) | `σ = r / √2` (in 2-D) |
| DoG ≈ LoG *(mine)* | `G(kσ) − G(σ) ≈ (k − 1) σ² ∇²G`. The DoG is already scale-normalised, up to the constant (k − 1) |
| SIFT octave *(mine)* | `k = 2^(1/s)` with s = `nOctaveLayers` = 3. Base blur σ = 1.6. Each octave needs s + 3 blurred images, giving s + 2 DoG images |
| Extremum test *(mine)* | a DoG pixel is a candidate if it is bigger (or smaller) than all **26 neighbours**: 8 in its own image, 9 in the scale above, 9 below |
| Edge rejection *(mine; `edgeThreshold`)* | with the 2 × 2 Hessian of the DoG, keep only if `trace² / det < (r + 1)² / r`, r = 10. Edges have one big and one small curvature and fail this test |
| SIFT descriptor (53, 61) | 4 × 4 cells × 8 bins = **128** dimensions, normalised to unit length |
| Orientation (60) | 36 bins × 10° = 360°. Extra orientation for every peak ≥ 80% of the highest |
| Ratio test (62) | accept if `d₁ / d₂ < 0.8` (nearest / second-nearest distance) |
| OpenCV defaults (63) | `nfeatures=0` (keep all), `nOctaveLayers=3`, `contrastThreshold=0.04`, `edgeThreshold=10`, `sigma=1.6`. Bigger `contrastThreshold` → **fewer** features. Bigger `edgeThreshold` → **more** features (less is filtered) |

### Worked Harris example *(mine, checked by script)*

Say the summed gradients in one window give `H = [[5, 2], [2, 2]]`. Slide 25's formula:
trace = 7, (h₁₁ − h₂₂)² = 9, 4h₁₂h₂₁ = 16, √25 = 5, so **λ₊ = (7 + 5)/2 = 6** and **λ₋ = (7 − 5)/2 = 1**.
Both are clearly above zero, so this is a corner (a weak one, since λ₋ is small). Harris with k = 0.04:
`R = det − k·trace² = (10 − 4) − 0.04 × 49 = 6 − 1.96 = 4.04 > 0`, a corner.

Compare an edge: `H = [[10, 0], [0, 0]]` (only x gradients). λ₊ = 10, λ₋ = 0, and
`R = 0 − 0.04 × 100 = −4 < 0`, an edge. A flat patch has H ≈ 0, so R ≈ 0.

### Why template matching fails and SIFT doesn't

Template matching compares **raw pixels** at one fixed size and angle. Make the object 20% bigger or turn it
by 20° and the pixels no longer line up, so the score collapses (slide 6). SIFT answers each failure:

- **Scale**: it searches all sizes (the DoG pyramid, 57–58) and picks each blob's own characteristic scale (46).
- **Rotation**: it measures each keypoint's dominant direction (60) and describes the patch relative to it.
- **Lighting**: gradients ignore added brightness, and the unit-length descriptor ignores contrast (54).
- **Small shape changes and clutter**: histograms over 4 × 4 cells don't care about exact pixel positions,
  and each keypoint is local, so a hidden part of the object kills only some matches (19, 54).

### SIFT matching code *(mine; the deck shows match pictures on 71 and 73 but no code for them)*

```python
import cv2, numpy as np
a = cv2.imread('som.jpg', cv2.IMREAD_GRAYSCALE)
b = cv2.imread('som_rotated.jpg', cv2.IMREAD_GRAYSCALE)
sift = cv2.SIFT_create()
ka, da = sift.detectAndCompute(a, None)          # keypoints + 128-D descriptors
kb, db = sift.detectAndCompute(b, None)
pairs = cv2.BFMatcher(cv2.NORM_L2).knnMatch(da, db, k=2)   # 2 nearest neighbours each
good = [m for m, n in pairs if m.distance < 0.8 * n.distance]   # ratio test, slide 62
src = np.float32([ka[m.queryIdx].pt for m in good])
dst = np.float32([kb[m.trainIdx].pt for m in good])
H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)   # problem 3: ignore the wrong pairs
out = cv2.drawMatches(a, ka, b, kb, good, None, flags=2)
```

For the slide 74 exercise, put the same matching inside the `cap.read()` loop from L14: keep the first
frame's keypoints and match every new frame against them.

## What to know for the exam

- Template matching: how it works, the size of the result map, which methods want the **max** and which the
  **min** (SQDIFF), and its limits (not scale or rotation invariant).
- The three matching problems (detector, descriptor, robust transformation) and the four properties of good
  features (repeatability, saliency, compactness, locality).
- Flat / edge / corner by shifting a window, and by the eigenvalues of H. Which eigenvalue means what.
- The five Harris steps, including **non-maximum suppression**.
- **Invariant vs covariant**, and Harris's answers: rotation yes, intensity partly, **scale no**.
- Scale selection: normalise the Laplacian by σ², characteristic scale, σ = r/√2.
- SIFT's four steps and the numbers: DoG instead of LoG, contrast threshold 0.03 (0.04 in OpenCV),
  36-bin orientation and the 80% rule, 16 × 16 → 4 × 4 × 8 = **128**, ratio test **0.8**.
- What makes SIFT invariant to each of scale, rotation and lighting.

## ⚠️ Things that are wrong or loose in the deck

- **Slide 26 has a wrong subscript.** The last bullet reads "λ₋ = amount of increase in direction **x₊**".
  It should be **x₋**. λ₋ is the eigenvalue of x₋, the direction of the *smallest* increase (the equation
  `H x₋ = λ₋ x₋` on the same slide says so). It looks like a copy-paste of the λ₊ line.
- **Slide 5 says "Brightest spot = best matching x,y" right under all six methods.** For `TM_SQDIFF` and
  `TM_SQDIFF_NORMED` the best match is the **darkest** spot (smallest difference). Using `max_loc` with
  them finds the worst match. *(mine, by running)* On `player.jpg`, `max_loc` of `TM_SQDIFF` is
  (346, 189), the place that looks *least* like the template.
- **The Harris response R is never defined.** Slides 28–32 compute, threshold and maximise R, and slide
  49 says it "depends only on the eigenvalues", but no slide gives the formula. It is
  `R = det(M) − k·(trace M)²` (see the table above).
- **Slide 27's rule is not Harris's.** "Find points with large response (λ₋ > threshold)" is the
  **Shi–Tomasi** criterion (min eigenvalue). Slide 28 then switches to Harris's R. Both work, but the deck
  presents them as one method.
- **Slide 24 writes "=" where it is only an approximation.** The quadratic form `[u v] H [u v]ᵀ` comes from
  a first-order Taylor expansion of I(x+u, y+v), so it holds only for small shifts. The deck skips that
  step, so the jump from slide 23 to 24 cannot be followed.
- **Slide 49 is titled "Descriptors Invariant to Rotation", but it shows the Harris detector.** Harris finds
  *where* features are (a detector). It does not describe them (a descriptor). The same slide also renames
  the matrix from H to **M** and adds weights w(x, y) without comment.
- **Slides 63–66 document an API that no longer exists.** `SIFT::SIFT(...)` and `SIFT::operator()` are
  the OpenCV 2.x C++ interface from the old "nonfree" module (slide 75's links point there too). Since
  OpenCV 4.4, SIFT is in the main library and you call `cv2.SIFT_create(...)` and
  `sift.detectAndCompute(img, mask)`, which is what slides 67 and 72 do.
- **The code uses file names that don't match the shipped images.** Slides 7 and 67 read `players.jpg` and
  `template.jpg`, but the files are `player.jpg` and `templ.jpg`. `cv2.imread` does not raise an error for
  a missing file. It returns `None`, and the program then crashes later inside `imshow` or
  `matchTemplate` with an assertion error. *(mine, checked)*
- **No slide shows how to match.** Slides 71 and 73 show matched keypoint pairs, and slide 62 explains the
  ratio test, but the code stops at `detectAndCompute`. There is no `BFMatcher`, `knnMatch` or ratio test
  anywhere. The code above fills the gap.
- **Slide 55 says Lowe came up with SIFT "in 2004".** It was first published in **1999** (ICCV). The 2004
  paper (IJCV, cited on slide 52) is the full journal version.
- **Slide 56 says "4 steps" and lists five.** Keypoint matching is not part of SIFT itself. SIFT detects
  and describes. Matching is a separate step that uses the descriptors.
- **Slide 58 says a Gaussian kernel with low σ "gives high value for small corner".** The LoG/DoG responds
  to **blobs**, not corners (slide 58's own first sentence calls it a blob detector).
- **Slide 59 skips half of step 2.** Besides low-contrast points, SIFT also rejects points lying on
  **edges** (the `edgeThreshold` test above). Slide 64 lists `edgeThreshold` without the deck ever saying
  what it does.
- **Slide 67 shows a BGR image with `cmap='gray'`.** `drawKeypoints` returns a 3-channel BGR image, so
  `cmap` is ignored and matplotlib shows the keypoint colours with red and blue swapped. Harmless here
  (the colours are random), but `cv2.cvtColor(…, cv2.COLOR_BGR2RGB)` is the correct habit.
- **Slide 72 writes `sift_keypoints.jpg` twice**, so the first picture (plain keypoints) is overwritten by
  the second (rich keypoints). It also creates a second SIFT object it doesn't need. It is copied
  from the OpenCV tutorial, which does the same.

## Links to other lectures

- **L11**: Gaussian blur, Sobel gradients (Ix, Iy), the Laplacian, **LoG and DoG**. All of Harris and SIFT
  is built from these.
- **L12**: nearest-neighbour classification. SIFT matching is nearest neighbour on 128-D descriptors,
  with Euclidean distance.
- **L14**: reading video frames with OpenCV, needed for the slide 74 exercise.
- **L16**: rotation, resizing and interpolation. These are the "geometric transformations" that
  features should be covariant to (slide 35), and they make test images like the rotated banknote.
- **L19**: what a "feature" is, and sliding a window over the image at every position and size (face
  detection), the same idea as template matching.
- **L20**: Haar-cascade face detection, another feature-based detector.
