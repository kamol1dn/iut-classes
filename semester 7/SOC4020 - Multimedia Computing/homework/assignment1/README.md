# Multimedia Computing — Assignment 1 (15 points)

**Due: Sun 2026-10-25, 23:55 by the eClass clock.** The instructions doc says
23:59, but the eClass page says 23:55, and eClass's clock is the one that counts. Submit on
[eClass, assignment 72061](https://eclass.inha.ac.kr/mod/assign/view.php?id=72061).
Posted 2026-10-08/09 in the week-5 section.

Full instructions: [Google Doc](https://docs.google.com/document/d/1qP4UpMlIuY6bUvnH0P7vWDObn4jI52qf/edit)
(*Multimedia Computing – Assignment 1_2026.docx*). Everything below is taken from it.
Questions go to the TA, **Kamalova Khushnoza**, at xushnozakamalova@gmail.com.

Input files: [`provided/`](provided/), downloaded from the eClass page.

> **Plagiarism:** every submission goes through a plagiarism checker. **A single
> plagiarised task zeroes the whole assignment**, not just that task.

## What you hand in

Upload **7 loose files** to eClass. **No zip and no folders.** A wrong name zeroes that task.

```
1_audio_waveform.py
2_audio_compression.py
1_image_log_transform.py
2_image_sobel_edges.py
1_video_downscale.py
2_video_blur.py
requirements.txt          every dependency your scripts import
```

Don't submit the output images, audio or videos. The grader generates them by
running your scripts and **compares them against reference outputs**. That's why the
exact functions, constants and libraries matter more than "looks right".

## Allowed libraries — any other library zeroes the task

| Section | Only these |
|---|---|
| Audio | `numpy`, `matplotlib`, `scipy.io`. **Not** `librosa` or `wave` |
| Image | `PIL.Image` (Pillow), `numpy`, `cv2`. **Not** `scikit-image` or `imageio` |
| Video | `cv2` only |

## The six tasks

| # | Script → output | Points | Spec, exactly as given |
|---|---|---|---|
| A1 | `1_audio_waveform.py` → `1_audio_waveform.png` | 2 | Read `original_audio.wav`, extract the waveform, plot it with matplotlib. **Figure size (10, 4) inches.** |
| A2 | `2_audio_compression.py` → `2_audio_compression.wav` | 2 | Compress `original_audio.wav`: "apply a suitable compression technique and **reduce the sample rate twice**". It must reach **compressed size / original size < 0.7**. |
| I1 | `1_image_log_transform.py` → `1_image_log_transform.png` | 2 | Read `original_image.png` → **grayscale** → "do not forget to **normalize** it first" → `I_new = c · log(1 + I_old)` with **`c = 255 / log(1 + max(I_old))`**, where max is over the grayscale image. Save as PNG. |
| I2 | `2_image_sobel_edges.py` → `2_image_sobel_edges.png` | 3 | Read → grayscale → Sobel in x and y with `Gx = [[-1,0,1],[-2,0,2],[-1,0,1]]`, `Gy = [[-1,-2,-1],[0,0,0],[1,2,1]]` → magnitude **`G = √(Gx² + Gy²)`**. Save as PNG. |
| V1 | `1_video_downscale.py` → downscaled `.mp4` (see the naming clash below) | 3 | Resize each frame to **exactly 50 %** of the width and height (the original dimensions divided by 2) with **`cv2.resize(..., interpolation=cv2.INTER_LINEAR)`**. Keep the original **fps**. |
| V2 | `2_video_blur.py` → `2_video_blur.mp4` | 3 | **`cv2.GaussianBlur(frame, (15, 15), 0)`** on every frame. Keep the original fps, width and height. |

The grader compares the **width, height, fps** and the processed frames of each video.

## What the provided files actually are

Checked locally, so you don't have to guess:

| File | Properties |
|---|---|
| `original_audio.wav` | **stereo** (2 channels), 16-bit PCM, **44 100 Hz**, 12.09 s, 2.1 MB |
| `original_image.png` | 512 × 512, saved in **palette mode (`P`)**, not RGB as the doc says |
| `original_video.mp4` | H.264, **320 × 240**, **15 fps**, 205 frames, 13.7 s, with an AAC audio track |

Why these matter:
- **Stereo audio:** your waveform plot and your resampling both have to cope with two
  channels, not a 1-D array.
- **Palette-mode PNG:** `cv2.imread` hands you 3-channel BGR. With Pillow you
  have to `.convert(...)` before you get real pixel values. A palette image's raw
  array holds **palette indices, not intensities**, which is an easy silent bug.
- **Video audio:** OpenCV's `VideoWriter` writes video only. The audio track
  disappears, and that's expected, because only width/height/fps/frames are graded.

## The doc contradicts itself — read this before you start

The doc looks like last year's version with one video task (grayscale
conversion) cut. The leftovers explain most of the oddities:

1. **"Three tasks" / "three techniques" / "three videos"**: the video and image sections
   still say three, but only list two. **Do the six tasks in the table above.** The
   "What to Submit" list confirms six scripts.
2. **The downscaled video's filename disagrees.** Task V1 says save it as
   `2_video_downscale.mp4`, but the submission section says `1_video_downscale.mp4`.
   The grader runs your script and looks for a specific output name. **Ask the TA
   which one.**
3. **Points:** "each task is worth 2 points, total 15", but the table gives
   2 + 2 + 2 + 3 + 3 + 3 = 15. The table is the one that adds up.
4. **Late penalties don't match 15 points.** "30 % → −5, 50 % → −9, 70 % → −13"
   are 30/50/70 % of **18**, not 15. Either way: **up to 3 h late −30 %, 3–6 h −50 %,
   up to 24 h −70 %, after 24 h no submission.** The course deck said late
   homework is *never* accepted. This doc is more specific, but don't plan around it.

## Ask the TA before you write I1 and I2

Both are graded by matching a reference image pixel-for-pixel, and the doc leaves
choices open that change the pixels:

- **I1, "normalize it first":** normalising to `[0, 1]` and then using `c = 255 / log(1 + max)`
  gives a gentle curve. Leaving the values at `[0, 255]` gives a strongly compressive
  one. The two produce **visibly different images**, and only one matches the reference.
- **I2, the output scaling:** G can exceed 255. The doc doesn't say whether to
  clip it, normalise it to 0–255, or which depth (`CV_64F`?) to compute in.
- **A2, the resampler:** "reduce the sample rate twice" reads as *halve it*
  (44 100 → 22 050 Hz). The audio whitelist names only `scipy.io`, so check whether
  `scipy.signal` is allowed or whether plain NumPy decimation is expected.

One short email covering point 2 above and these three bullets saves you guessing on 10 of the 15 points.

The grayscale step is **not** a risk. Pillow's `convert('L')` and OpenCV's
`cvtColor(..., COLOR_BGR2GRAY)` give identical results on this image (all 262 144 pixels
match, checked 2026-10-09).

## Where the course covers this

| Task | Lecture material |
|---|---|
| A1, A2 | L2 (sampling, Nyquist): halving the rate halves the highest frequency you can keep. L5's **data rate = sampling rate × bits × channels** tells you what halving the rate does to the file size. |
| I1 | L6 covers point operations (negative, gamma, contrast stretch). The **log transform itself isn't in L1–L10**. Your own [`my-notes/intensity/transformation.py`](../../my-notes/intensity/transformation.py) already does the same normalise → curve → rescale-to-255 pattern for gamma. |
| I2 | **Not covered yet.** Sobel and spatial filtering aren't in L1–L10. L10's morphological gradient is the nearest relative. |
| V1, V2 | L6 mentions resampling/interpolation. L8 maps MATLAB blur to `cv2.blur`. The OpenCV video read/write loop is new. |

## Timing

Week 7 (17–23 Oct) has the Embedded Software and Deep Learning for CV midterms.
Week 8 (24 Oct onwards) has AI, Distinguished Lecture and probably this course's own midterm. This
assignment is due on the Sunday between them. Email the TA early, because the answers
decide how you write I1 and I2.

## Checklist

- [ ] Email the TA (V1 filename clash, I1 normalisation, I2 output scaling, A2 resampler)
- [ ] A1 `1_audio_waveform.py`
- [ ] A2 `2_audio_compression.py`, with the size ratio checked < 0.7
- [ ] I1 `1_image_log_transform.py`
- [ ] I2 `2_image_sobel_edges.py`
- [ ] V1 `1_video_downscale.py`, output 160 × 120 at 15 fps
- [ ] V2 `2_video_blur.py`, output 320 × 240 at 15 fps
- [ ] `requirements.txt`
- [ ] Run all six from a clean folder holding only the three originals, and check every output appears
- [ ] Upload the 7 loose files; confirm eClass shows "Submitted for grading"
