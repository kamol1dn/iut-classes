# Ear Gender Detector — Multimedia Computing homework

Homework from the board (25 Nov 2026): **detect the ear, then say if it is a male ear or a female ear**.
The input is the webcam or an uploaded photo.

## Run it

```powershell
cd "semester 7\SOC4020 - Multimedia Computing\project\ear-gender"
py -3.12 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python download_models.py     # ~126 MB: detectors, MobileNetV2, EarVN1.0 dataset
.venv\Scripts\python train.py               # ~9 min, writes models/ear_gender.npz
.venv\Scripts\python app.py                 # the app
```

It uses **OpenCV 4.12** on purpose. OpenCV 5 removed the Haar `CascadeClassifier` from the main package.

Command line, without the app:

```powershell
.venv\Scripts\python ear.py side_photo.jpg          # find the ears, label them, save side_photo_result.jpg
.venv\Scripts\python ear.py ear_closeup.jpg --crop  # the photo is already just an ear
```

## In the app

| Control | What it does |
|---|---|
| Start camera | Live webcam. Turn your head **sideways** so the camera sees one ear |
| Upload image | Pick a photo; every ear found gets a box and "Male ear 87%" |
| Guide box (camera) | If the detector misses your ear, tick this and hold your ear in the box in the middle |
| Upload is an ear close-up | For photos that are already a cropped ear (like the dataset) |
| Save result | Save the labelled picture |

## How it works

```
image ──► 1. ear detector ──► 2. crop + resize 224×224 ──► 3. MobileNetV2 ──► 1280 numbers ──► 4. logistic regression ──► P(female)
          (Haar cascades,                                    (pretrained on                     (trained by train.py
           integral image)                                    ImageNet)                          on EarVN1.0)
```

1. **Ear detection: Viola–Jones Haar cascades.** These are OpenCV's `haarcascade_mcs_leftear.xml` and
   `..._rightear.xml`. A Haar feature is a difference between the sums of light and dark rectangles. With an
   **integral image**, the sum of any rectangle needs only 4 lookups, `D − B − C + A`, so thousands of
   features per window are cheap. That is the "integral image" example on the board. Both cascades run,
   and overlapping boxes are merged with non-maximum suppression.
2. **Crop** the ear with a 15% margin and resize it to 224×224.
3. **Feature extraction, which is transfer learning.** MobileNetV2 is a CNN that already learned edges,
   curves and textures from 1.2 million ImageNet photos. We cut off its last layer and keep the
   1280-number summary it computes for the ear.
4. **Classification.** Logistic regression on those 1280 numbers gives P(female). Above 0.5 means female.
   The ear is classified twice, once as-is and once mirrored, and the two answers are averaged. A mirrored
   left ear looks like a right ear, so the answer does not depend on which side is shown. On the camera,
   the answer is also averaged over the last 10 frames so it does not flicker.

## Dataset: EarVN1.0

28,412 ear photos of 164 Vietnamese public figures: 98 men (folders 001–098) and 66 women (099–164).
The photos were taken "in the wild", with different lighting, angles, earrings and hair.
Source: Hoang, *EarVN1.0: A new large-scale ear images dataset in the wild*, Data in Brief 27 (2019);
[Mendeley Data](https://data.mendeley.com/datasets/yws3v3mwx3). The dataset is for non-commercial use only, so
it is downloaded rather than stored in this repo.

## Results

This is 5-fold cross-validation **split by person**: each fold tests on about 33 people the model has never
seen. Full log: `data/train_log.txt`.

| Regularisation C | Accuracy per photo | Accuracy per person (majority vote of their photos) |
|---|---|---|
| 0.001 | 84.6% ± 1.3 | 98.2% |
| **0.01 (used)** | **84.8% ± 1.5** | **98.2%** (161 of 164) |
| 0.1 | 84.2% ± 1.4 | 98.2% |

Confusion matrix, all 28,412 photos, each predicted by the fold that never saw that person:

|  | predicted Male | predicted Female |
|---|---|---|
| **actually Male** (17,571) | 15,202 | 2,369 |
| **actually Female** (10,841) | 1,940 | 8,901 |

Male: precision 0.887, recall 0.865. Female: precision 0.790, recall 0.821. Training uses
`class_weight="balanced"` because there are 1.6× more male photos. Without it, the model would lean
towards "Male". For comparison, the paper *Deep Ear Biometrics for Gender Classification*
([arXiv 2308.08797](https://arxiv.org/abs/2308.08797)) reports 93% with a CNN trained end-to-end on this
dataset. Our model is much simpler: a frozen network plus logistic regression, trained in about 10 minutes
on a CPU.

**Why split by person?** Each person has about 170 photos. A random split by photo would put the same person
in both training and test. The model could then recognise *who* it is instead of judging the ear, and the
accuracy would look higher than it really is. Here every test person is someone the model has never seen.

## Limitations to mention

- The Haar ear detector is from 2010 and misses many ears. On 200 small, low-resolution dataset photos it
  found the ear in 42%. It works best on a clear side view with the ear not covered by hair. The guide box
  is the fallback.
- The dataset contains only Vietnamese adults, mostly celebrities. Results on other people may be worse.
- Long hair and earrings are strong hints in the photos, so the model may partly use them, not only the ear
  shape.
- The model gives a statistical guess about a photo. It says nothing about a person's gender identity.

## Files

| File | Purpose |
|---|---|
| `ear.py` | The pipeline: detector, feature extractor, classifier, drawing; also a command-line tool |
| `train.py` | Extracts features from EarVN1.0, runs person-wise 5-fold cross-validation, saves the model |
| `app.py` | Tkinter app: camera, upload, guide box, save |
| `download_models.py` | Downloads the cascades, MobileNetV2 and the dataset (checks the dataset's SHA-256) |
| `models/ear_gender.npz` | The trained classifier: scaler mean/std, 1280 weights and a bias (~15 KB) |
