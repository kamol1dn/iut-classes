# L20: Face Detection: ROC Evaluation, Boosting, Haar Features, Integral Image, Cascade Classifier

**Multimedia Computing · Week 12 · 69 slides · Dr. Minhaz Uddin Ahmed**
Source: [week12 - Multimedia Computing L20 (face detection).pptx](../slides/week12%20-%20Multimedia%20Computing%20L20%20(face%20detection).pptx) *(13.2 MB)*
Practice: [L20 practice - haarcascade_frontalface_default.xml](../../resources/L20%20practice%20-%20haarcascade_frontalface_default.xml)
(the trained face detector) · the code also reads L19's [faces.jpeg](../../resources/L19%20practice%20-%20faces.jpeg)

L19 ended with the idea of face detection (slide a window, classify each patch) but no code. This lecture
gives the method everyone uses in OpenCV: the **Viola–Jones Haar cascade**. Most text comes from Szeliski
chapters 4 and 14 (first edition, slide 66), plus slides borrowed from S. Seitz and from OpenCV's docs. The
deck has six parts:

- **The Haar cascade in one picture, and code** (4–9): what a cascade is, then 15 lines of Python that draw
  a box round every face in `faces.jpeg`.
- **Evaluating a detector** (10–16): true and false positives, the **ROC curve**, and the four rates (TPR,
  FPR, PPV, accuracy) with a worked confusion table.
- **A tour of recognition** (17–35): classification vs detection, older face detectors (Rowley, Sung and
  Poggio), **boosting** and the **AdaBoost** algorithm (23–26), a timeline, pedestrian detection with HOG,
  parts-based and bag-of-words models. Mostly survey, little you can compute.
- **How Viola–Jones works** (36–48): Haar-like features, the **integral image** with three numeric examples
  (43–47), AdaBoost in plain words.
- **OpenCV's API and C++ code** (49–53, 60–64): `detectMultiScale` and its parameters, a webcam face-and-eye
  detector.
- **Training your own cascade** (54–59), then an exercise: **detect an ear** (65).

A lot of the deck is pictures. The extractor gets no text from slides 4–7, 9, 15–18, 26, 31, 43–47, 51–53,
55–56 and 61–64. Everything below was read off the rendered slides. Pictures worth opening in the pptx: the
cascade diagram (5), the confusion table and formulas (15–16), the AdaBoost algorithm (26), the
integral-image grids (43–47), the C++ code (51–52) and the training command screenshots (55–56).

## The practice file

**`haarcascade_frontalface_default.xml`** is a detector that someone already trained. You do not train
anything in this lecture. You load the file and use it. *(mine, from reading the file)* It is OpenCV's
standard frontal-face cascade by Rainer Lienhart. It works on a **24 × 24** window and has **25 stages**
holding **2,913 weak classifiers** in total. Stage 1 has only 9, the last stage has 200. That shape is the
whole point of a cascade: cheap stages first, expensive ones only for windows that look like faces.

**Running slide 8's code** on L19's `faces.jpeg` (750 × 750, a 5 × 5 grid of portraits):

```python
img = cv2.imread("faces.jpeg", 1)                       # 1 = load in colour (BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)            # Haar features use brightness only
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.10, minNeighbors=5, minSize=(40, 40))
print(len(faces))                                       # number of boxes found
for (x, y, w, h) in faces:                              # each box: top-left corner, width, height
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)   # green, 2 px thick
```

*(mine)* It prints **24**. That is 23 real faces plus one false box (a second, lower box on the face in row 1,
column 2). Two faces are **missed**: the boy in row 3, column 5 (head tilted, hand behind his head) and the
woman in row 4, column 3. Changing the settings:

| Setting | Boxes | What happens |
|---|---|---|
| `minNeighbors=0` | 1,076 | every raw window that passed all 25 stages, no grouping |
| `minNeighbors=1` | 31 | many duplicates and false boxes |
| `minNeighbors=3` | 27 | **all 25 faces found**, plus 2 false boxes |
| `minNeighbors=5` (slide 8) | 24 | 23 faces, 1 false box, 2 missed |
| `minNeighbors=12` | 21 | fewer false boxes, more missed faces |
| `scaleFactor=1.05 / 1.2 / 1.5` | 27 / 21 / 17 | finer steps find more, bigger steps miss faces |

So the parameters trade **missed faces** against **false boxes**. That is exactly the ROC trade-off of
slides 11–14. Note on versions: with OpenCV 5.0 the plain `opencv-python` package has **no
`CascadeClassifier`** (my run fails with `AttributeError`). You need `opencv-contrib-python`. With OpenCV 4.x
the plain package works.

## Outline

| Slides | Topic |
|---|---|
| 1–2 | Title. Contents: feature detection, evaluating results, ROC, face detection methods, object detection, Haar features, cascade classifier |
| 3 | **Feature detection** (Szeliski fig. 4.1): point-like interest points, region-like features, edges, straight lines |
| 4, 7 | **Haar cascade method**: feature-based machine learning, trained on labelled positive (face) and negative (non-face) images, runs thousands of classifiers in a **cascade**, output = bounding boxes |
| 5 | **Cascading** diagram. Each region of interest (ROI) goes through classifier 1, 2, 3. Early ones are "fast but general", later ones "slow but precise". Pass all → "ROI is a face". Fail any one → rejected at once |
| 6 | Training data → face detector → results with a **false positive** (box on a non-face) and **false negatives** (missed faces) circled |
| 8–9 | The Python code above, and its result on `faces.jpeg` (see the errors section: slide 9 is not slide 8's output) |
| 10 | Two kinds of features: **keypoints / interest points** (corners, peaks, doorways) and **edges** (good for object boundaries) |
| 11–12 | Matching features between two photos of the Trevi fountain. Each match has a **feature distance** (50, 75, 200). A threshold on the distance decides what counts as a match. **True positive** = a detected match that is correct. **False positive** = a detected match that is wrong (the 200 one) |
| 13–14 | **ROC curve**: x = false positive rate, y = true positive rate, one point per threshold. Example point: TPR 0.7 at FPR 0.1. The diagonal is random guessing. A good matcher bends toward the top-left. Compare methods by the **area under the curve (AUC)** |
| 15–16 | Szeliski table 4.1: a **confusion matrix** with TP 18, FN 2, FP 4, TN 76, and the formulas for TPR, FPR, PPV and accuracy (worked below) |
| 17–18 | **Classification** ("does this picture contain people?") vs **detection** ("where are the people?", circles drawn on them) |
| 19 | Szeliski fig. 14.1: many kinds of recognition (pictorial structures, eigenfaces, Viola–Jones real-time detection, instance recognition, location recognition, context) |
| 20 | Rowley, Baluja and Kanade's detector run on a group photo. Run a recognizer on **every sub-window** |
| 21 | Every pixel and every scale is too slow. Rowley's training prep: mirror, rotate, scale and shift face images for variety; cut non-face patches from images with no faces (a tree); subtract a best-fit linear brightness ramp and **histogram-equalise** each patch |
| 22 | **Sung and Poggio** (1998): 19 × 19 face and non-face patches, each group clustered into **six** clusters with k-means, then analysed with PCA. The cluster centres are shown |
| 23 | **Boosting** (Viola and Jones): train a series of increasingly strict simple classifiers and blend their outputs |
| 24 | Boosting picture: after each weak classifier (a **decision stump**, i.e. one threshold on one feature), the points it got wrong get **heavier weights**. The final classifier is a weighted sum of the weak ones |
| 25 | Boosting picks one feature to threshold each round. With an O(N) pre-computation (the integral image), a feature of r rectangles costs about 4r additions/subtractions, r ∈ {2, 3, 4} |
| 26 | **Algorithm 14.1, AdaBoost training** (image only; formulas below) |
| 27 | Timeline: alignment (1965–1980s), appearance methods (early 90s), **sliding windows** (mid 90s), features, parts-and-shape, bags of features and **HOG** (2003–2010), **deep learning** (2012 on) |
| 28 | **Pedestrian detection** (Dalal and Triggs 2005) with **HOG**, histograms of oriented gradients, and an SVM |
| 29–30 | **Parts and structure**: an object is a set of parts (headlights, windscreen) plus where they sit relative to each other. The face drawn as eyes, nose, mouth joined by springs |
| 31 | **Bag of words**: describe an object as an unordered bag of small patches, ignoring where they are |
| 32–34 | Three issues: **representation**, **learning** (learn the difference from data instead of writing rules) and **recognition** (use the classifier on new images). Invariances needed: viewpoint, lighting, occlusion, scale, deformation, clutter |
| 35 | Applications: licence plates, zip codes, cheques, fingerprints, face detection in cameras |
| 36–37 | **Viola and Jones (2001)**. Train a cascade of boosted classifiers on a few hundred positive views of one object, scaled to one size (say 20 × 20), and on negative images of the same size |
| 38 | The trained classifier outputs **1** (object) or **0** for one window. Slide the window over the whole image. The extended feature set: **edge**, **line** and **centre-surround** features, some rotated 45° |
| 39 | Four ingredients: **Haar features**, the **integral image**, **AdaBoost**, the **cascade**. A Haar feature is a pair (or more) of adjacent light and dark rectangles |
| 40 | Feature value = (light region) − (dark region). Above a learned threshold → the feature is "present". Viola–Jones fig. 2: the integral image, and the sum inside rectangle D = 4 + 1 − (2 + 3) |
| 41–42 | Summing many rectangles at many scales is too slow, so use the **integral image**. Slide 42's formula: rectangle ABCD = AC − (AB + AD − AA) |
| 43 | Small example: 3 × 3 image → its integral image (numbers below) |
| 44 | 7 × 6 example: the integral value at one cell (988) is the sum of the 3 × 3 block above-left of it |
| 45 | Sum of a 4 × 3 block = `II_P − II_Q − II_S + II_R = 3490 − 1137 − 1249 + 417 = 1521`. "Computation cost only three addition" |
| 46 | A two-rectangle **Haar response**: white block − black block = 1246 − 1182 = **64**, "only 7 additions" |
| 47 | Computing the integral image in one **raster scan** (row by row). Shows pixel A with neighbours B (above), C (left), D (above-left). The formula itself is not on the slide (given below) |
| 48 | **AdaBoost** in plain words: a weak classifier is only a bit better than guessing. Many of them, each with a weight, add up to a strong classifier. AdaBoost picks the features and sets the thresholds |
| 49–50 | `CascadeClassifier::detectMultiScale(image, objects, scaleFactor=1.1, minNeighbors=3, flags=0, minSize, maxSize)` and what each parameter means (table below) |
| 51–52 | **C++ webcam code**: load face and eye cascades, read frames, find faces, then search for eyes inside each face box and circle them (see the errors section) |
| 53 | The `haarcascades` folder in an OpenCV install, and the first features the frontal-face cascade picked (eyes darker than cheeks, nose bridge lighter than eyes) |
| 54–56 | Training your own: OpenCV's training tutorial. Use `dir /b > positive.dat` and `dir /b > neg.dat` to list image files. Folder screenshots of positive (face) and negative images |
| 57–58 | `opencv_haartraining` options: `data`, `vec`, `bg`, `nstages`, `nsplits`, `minhitrate`, `maxfalsealarm`, `npos`, `nneg`, `w`, `h`, `mem`, `mode` (BASIC = upright features only, ALL = also 45° rotated) |
| 59 | The two commands, `opencv_createsamples` then `opencv_haartraining` (see the errors section: they don't work as typed) |
| 60–61 | The training produces an XML like `haarcascade_frontalface_alt.xml`. Slide 61 shows its inside: stages, trees, rectangles, thresholds |
| 62–64 | Output pictures: one face with a blue box and red eye circles (62); a group photo with every face found (63–64) |
| 65 | **Exercise: use a Haar cascade to detect an ear** |
| 66–69 | References: Szeliski *Computer Vision: Algorithms and Applications*, Howse et al. *OpenCV: Computer Vision Projects with Python*, OpenCV 2.4 cascade docs, Wikipedia on ROC. Questions. Thank you |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Confusion counts (slide 16) | **TP** correct detections · **FN** real ones missed · **FP** detections that are wrong · **TN** non-objects correctly ignored. P = TP + FN (real positives), N = FP + TN (real negatives) |
| Rates (slide 16) | `TPR = TP/(TP+FN) = TP/P` (also called recall) · `FPR = FP/(FP+TN) = FP/N` · `PPV = TP/(TP+FP)` (precision) · `ACC = (TP+TN)/(P+N)` |
| Slide 15's numbers | TP 18, FN 2, FP 4, TN 76 → TPR 18/20 = **0.90**, FPR 4/80 = **0.05**, PPV 18/22 = **0.82**, ACC 94/100 = **0.94**. All four check out |
| ROC curve | plot (FPR, TPR) for every threshold. Lower threshold → both go up. AUC 1 = perfect, 0.5 = guessing |
| Integral image | `II(x, y)` = sum of all pixels above and to the left, including (x, y) itself |
| Building it (slide 47, formula *mine*) | `II_A = I_A + II_B + II_C − II_D`, B above, C left, D above-left. One pass over the image. Check on slide 44: 124 + 658 + 623 − 417 = **988** |
| Any rectangle sum (slides 40, 45) | `sum = II(bottom-right) − II(just above top-right) − II(just left of bottom-left) + II(just above-left of top-left)`. Four look-ups, 3 additions/subtractions, **whatever the rectangle size** |
| Haar response (slides 40, 46) | `V = Σ(white) − Σ(black)`. A 2-rectangle feature: 8 look-ups and 7 operations (only 6 distinct look-ups, since the two rectangles share an edge) |
| AdaBoost error (slide 26) | `e_j = Σᵢ wᵢ,ⱼ · eᵢ,ⱼ`, where `eᵢ,ⱼ` = 1 if example i is misclassified by classifier j, 0 if correct |
| AdaBoost weights (slide 26) | `β_j = e_j / (1 − e_j)`, classifier weight `α_j = −log β_j = log((1 − e_j)/e_j)`. Update `wᵢ ← wᵢ · β_j^(1 − eᵢ,ⱼ)`: correct examples are multiplied by β (< 1), wrong ones unchanged, then renormalise |
| Final strong classifier (slide 26) | `h(x) = sign(Σ_j α_j h_j(x))`, labels +1 (face) and −1 (non-face). A more accurate weak classifier gets a bigger α |
| `scaleFactor` | each step shrinks the image by this factor (1.1 = 10%). Smaller = more scales = slower but finds more |
| `minNeighbors` | how many overlapping raw detections a box needs to be kept. Higher = fewer false boxes, more misses. C++ default 3 |
| `minSize` / `maxSize` | ignore objects smaller / larger than this |

### Worked integral image *(slide 43, checked)*

```
Input I          Integral II
1  5  2          1   6   8          row 1: running sums 1, 1+5, 1+5+2
2  4  1          3  12  15          II(2,2) = 1+5+2+4 = 12
2  1  1          5  15  19          II(3,3) = sum of everything = 19
```

Sum of the bottom-right 2 × 2 block (4, 1, 1, 1 = 7) from the table: `19 − 8 − 5 + 1 = 7`. Four look-ups,
three operations. For a 100 × 100 block it is still four look-ups. That is why Viola–Jones can test
thousands of features per window in real time.

*(mine, checked by script)* All 42 numbers in slide 44's 7 × 6 integral image are correct, and so are both
results: the 4 × 3 block on slide 45 really sums to 1521, and on slide 46 the white block sums to 1246 and
the black one to 1182.

### Worked AdaBoost round *(mine)*

Five training examples, all weights 0.2. The best stump gets one of them wrong.

- Error `e = 0.2`. So `β = 0.2/0.8 = 0.25` and `α = log 4 ≈ 1.39`.
- The four correct examples: 0.2 × 0.25 = 0.05 each. The wrong one stays at 0.2. Total 0.4.
- Renormalise: correct ones become **0.125**, the wrong one becomes **0.5**.

The one hard example now carries half of all the weight, so the next stump is pushed to get it right. Note
that the old stump's weighted error is now exactly 0.5, no better than guessing on the new weights. That is
why the next round must pick a different feature.

### Why a cascade is fast *(mine)*

In a typical image almost every window is **not** a face. If stage 1 (9 features here) throws away half of
those windows, stage 2 sees half as many, and so on. OpenCV's training defaults ask each stage for a hit
rate of 0.995 and a false-alarm rate of 0.5. Over 20 stages that gives

- detection rate `0.995^20 ≈ 0.90`
- false-positive rate `0.5^20 ≈ 0.00000095` (about 1 in a million windows)

Each stage only needs to be "weak", but the chain is very strict. And most windows cost just a few
features. A window counts as a face only if it passes **every** stage.

### detectMultiScale, step by step *(mine)*

1. Build an image pyramid: the image, then 1/1.1 of it, then 1/1.1² ... until it is smaller than the 24 × 24
   window. For `faces.jpeg` with `minSize=(40,40)` that is about **31 scales**.
2. At each scale slide the 24 × 24 window across all positions and run the cascade.
3. Every window that passes all 25 stages is a raw hit. A real face gives many hits at nearby positions and
   scales (1,076 raw hits on `faces.jpeg`).
4. Group overlapping hits. Keep a group only if it has at least `minNeighbors` members. Return one box per
   group.

### Ear exercise (slide 65) *(mine)*

OpenCV's current cascade set has no ear detector. The old OpenCV 2.4 set had
`haarcascade_mcs_leftear.xml` and `haarcascade_mcs_rightear.xml` (from the same "mcs" family as the eye-pair
files in slide 53's folder). The code is slide 8's with the file name changed. Ears are seen from the side,
so a **profile** photo like slide 65's works and a frontal one will not. If you can't find those files, you
must train your own cascade (slides 54–59).

## What to know for the exam

- The four Viola–Jones ingredients and what each one buys: Haar features (simple), integral image (fast
  sums), AdaBoost (picks the useful features), cascade (rejects non-faces early).
- Compute an integral image by hand, and a rectangle sum from four corner values. Know which corners are
  inside and which are one step outside.
- A Haar response = white sum − black sum.
- TP, FP, FN, TN; TPR, FPR, PPV, accuracy from a confusion table; what an ROC curve plots and why a bigger
  AUC is better.
- AdaBoost: weak vs strong classifier, misclassified examples get heavier, the final answer is a weighted
  vote, `α = log((1 − e)/e)`.
- Classification vs detection vs recognition.
- `detectMultiScale` parameters, especially what raising `minNeighbors` or `scaleFactor` does.
- Convert to grey first. Haar cascades use brightness patterns, not colour.

## ⚠️ Things that are wrong or loose in the deck

- **Slide 59's training commands do not work as typed.** (1) `opencv_createsamples -info neg.dat -vec
  neg.vec` packs the **negatives** into a `.vec` file. A `.vec` file is for **positives**. Negatives are
  only listed in a text file and passed with `-bg`. (2) The second command then reads `-vec F:\prog\pos.vec`,
  a file the first command never made. (3) The options are mangled: `-nstages14` and `–nneg20` have no
  space, `-npos 20 -npos` repeats an option with no value, `–num` and `–nneg` use an en dash instead of a
  hyphen, and the curly quotes (“ ”) are not valid in a Windows command line. The folder is also spelled
  "Poistive".
- **Slide 55's `dir /b > positive.dat` makes the wrong file for positives.** It lists only file names.
  `opencv_createsamples -info` needs each line as `file count x y w h` (where the object is in the image).
  A bare file list is fine only for the negative `bg` file.
- **Slides 57–59 teach `opencv_haartraining`, which was removed in OpenCV 3.0.** Slide 54 links the newer
  `opencv_traincascade` tutorial, whose options have different names (`-numStages`, `-numPos`, `-numNeg`,
  `-minHitRate`, `-maxFalseAlarmRate`, `-featureType`). The slides and the link don't match.
- **Slide 51's C++ program does not compile as shown.** It includes only `opencv2/imgproc/imgproc.hpp`, but
  uses `CascadeClassifier` (objdetect module), `VideoCapture` (videoio), `imshow` and `waitKey` (highgui), and
  `assert` (`<cassert>`). Include `<opencv2/opencv.hpp>` instead. It also uses the old C names
  `CV_BGR2GRAY` and `CV_HAAR_SCALE_IMAGE`. On OpenCV 4 use `cv::COLOR_BGR2GRAY` and
  `cv::CASCADE_SCALE_IMAGE`. There is no check that `v.read(frame)` got a frame, so it crashes when the
  camera stops.
- **Slide 52's eye search is loose.** It looks for eyes over the whole face box with `minNeighbors=2`, so
  the mouth and nostrils also get hits. Slide 62's output shows several small red marks on the forehead,
  nose and mouth that look like such false eye detections. Searching only the top half of the face box and
  raising `minNeighbors` fixes most of it.
- **Slide 9 is not the output of slide 8's code.** *(mine, by running)* With slide 8's settings
  (`minNeighbors=5`) you get 24 boxes and two faces are missed. Slide 9 shows all 25 faces plus two extra
  boxes. My run reproduces slide 9 exactly with `minNeighbors=3`, the default.
- **Slide 22's caption says "192-long vectors", but its own figure says ℜ²⁸³.** A 19 × 19 patch has 361
  pixels. Masking the corners leaves **283** (the same number as L19 slide 51). 192 is wrong.
- **Slide 42 calls the rectangle sum an "Area".** It is the **sum of pixel values** in the rectangle, not
  its area. The slide also uses "A" for two things: the image's top-left point (in "AP") and a corner of
  the rectangle. Read "AC" as "sum from the image's top-left corner to C". Slide 45 shows the same idea
  more clearly.
- **Slide 14 writes "Receiver Operator Characteristic".** The name is Receiver **Operating**
  Characteristic (the slide's own Wikipedia link says so). The same slide says "# current/incorrect
  matches", meaning **correct**/incorrect.
- **Slide 50 mixes two APIs.** It describes `detectMultiScale` from the C++ class, but its `cascade` line
  is from the old C function `cvHaarDetectObjects` (`cvReleaseHaarClassifierCascade`, `Load()`), which is
  not a parameter of the C++ method at all.
- **Slide 26's indices don't line up.** Stages run `j = 1 … M`, but the final sum runs `j = 0 … m−1` and
  the example sum `i = 0 … N−1`. It is copied from Szeliski as is. Also `sign(...)` with labels ±1 needs each
  weak classifier to output ±1 too. Viola and Jones's own version uses 0/1 outputs and a threshold of half
  the total α instead.
- **Slide 36's figure is not a Viola–Jones picture.** Its caption (Szeliski fig. 4.26) says these are Haar
  wavelets used to hash the MOPS descriptor, a feature-matching method. The patterns look the same, but the
  use is different.
- **Slides 23 and 36 give different years (2004 and 2001).** Both are right. The detector was presented in
  2001 (CVPR) and published in full in 2004 (IJCV).
- **Slide 37 says "say, 20x20" and slide 61 shows a 20 × 20 cascade (`_alt`).** The file shipped with this
  lecture (`_default`) uses **24 × 24**, the size in the original Viola–Jones paper. Not an error, but don't
  mix them up.
- **Slide 8 imports `cv2_imshow` in a comment but calls `cv2.imshow`.** Fine on your own computer, but in
  Colab `cv2.imshow` doesn't work. Uncomment the import and use `cv2_imshow(img)` there.

## Links to other lectures

- **L19**: the sliding-window face detection idea, the 19 × 19 features (283 values, the same as slide 22
  here) and an ROC chart. `faces.jpeg` was used there for skin-tone detection and is reused here.
- **L12**: pattern classification. AdaBoost and the cascade are classifiers, and TP/FP/ROC measure them.
- **L6 / L9**: histograms and histogram equalisation (slide 21's patch preprocessing).
- **L11**: gradients and edges, the basis of HOG (slide 28).
- **L17**: k-means, used by Sung and Poggio (slide 22).
- **L21**: feature detection and matching in depth (Harris corners, SIFT). Slides 3 and 10–14 here are a
  preview of it.
