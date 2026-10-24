# L6 — Digital Image Fundamentals & Intensity Transformations

**Multimedia Computing · Week 3 · 67 slides · Dr. Minhaz Uddin Ahmed**
Source: [week03 - Multimedia Computing L6.pptx](week03%20-%20Multimedia%20Computing%20L6.pptx) *(10 MB)*
Reference: Gonzalez, *Digital Image Processing*, Ch. 2–3

The course moves from audio to **images**. The first half is mostly diagrams
taken from Gonzalez: the eye, lenses, the EM spectrum, sampling. Around **30 of
the 67 slides have no text**, so **open the pptx for slides 4–36**. The second
half covers **point operations** you can code in a few lines, and your gamma
experiment in [`my-notes/intensity/`](../my-notes/intensity/) already does one
of them.

**Contents:** human visual perception · brightness adaptation and
discrimination · image formation and lenses · light and the EM spectrum · image
acquisition · sampling and quantization · spatial and intensity resolution ·
pixel relationships · resampling · contrast stretching · thresholding ·
intensity transformations · gamma · histograms · histogram equalization.

---

## 1. Human visual perception

- **Scotopic vision** uses **rods** only. It works in dim light and shows no colour.
- **Photopic vision** uses **cones**. It works in bright light and gives colour.
- **Brightness adaptation:** the eye covers a huge range of light levels, but
  only a small part of that range at any one moment.
- **Brightness discrimination:** increase ΔI on a flash over a background of
  intensity I until it becomes just visible (the *just-noticeable difference*).
  **ΔI / I is the Weber ratio.** A small Weber ratio means good discrimination.
- **Perceived brightness isn't a simple function of actual intensity.** Two
  effects show this. **Mach bands** make edges look over- and undershot.
  **Simultaneous contrast** makes the same grey look darker on a bright background.

## 2. Image formation and acquisition

- The eye works like a camera: the lens focuses an image on the retina.
- **Focal length** sets the angle of view and the magnification. A **longer**
  focal length gives a **narrower** angle and **higher** magnification.
- **Visible light** runs from about **380 to 700 nm**. The relation is λ = c/ν
  and E = hν, so shorter wavelength means higher energy.
- **Airy pattern:** the smallest spot a perfect circular lens can focus.
  Diffraction limits its size.
- **Image formation model:** f(x,y) = i(x,y) · r(x,y), where i is illumination and r is reflectance.
- **Spatial-domain processing:** **g(x,y) = T[f(x,y)]**. T is an operator
  applied over a neighbourhood of (x,y), usually 3×3. If the neighbourhood is
  **1×1**, T is a *point operation*, which is what section 4 covers.

## 3. Sampling, quantization and resolution

- **Sampling** digitises the coordinates. **Quantization** digitises the amplitude.
- An M × N image with k bits per pixel needs **M · N · k bits** to store.
- **Spatial resolution** depends on the pixel count. Too few pixels gives a
  blocky image.
- **Intensity resolution** depends on the number of grey levels. Too few gives
  **false contouring**.
- **Isopreference curves** (speaker notes) show how perceived quality changes as
  you vary **N** (the number of pixels) and **k** (bits per pixel) independently.
  Images with **more detail** tolerate fewer grey levels.
- **Dynamic range** is the ratio between the brightest and darkest levels you can represent.
- **Pixel relationships:** 4-, 8- and m-adjacency. A region is represented as a
  **set of coordinates**, so set operations (∪, ∩, complement) apply to it.
- **Resampling / interpolation:** resizing or distorting an image. The usual
  methods are nearest-neighbour, bilinear and bicubic.

---

## 4. Intensity (point) transformations, the practical core

A point transformation maps each old pixel value to a new one with a fixed
function. It is usually implemented as a **look-up table (LUT)** with 256
entries, so it is very cheap to apply.

| Transform | Formula / idea | Use |
|---|---|---|
| **Null** | s = r | Baseline |
| **Negative** | **s = 255 − r** (slide: y = −x + 255) | Medical images, negative prints |
| **Gamma** | s = 255 · (r/255)^γ | Correcting for display response |
| **Contrast stretch** | Map [r_min, r_max] linearly onto [0, 255] | Low-contrast images |
| **Contrast compression** | The reverse of stretching | |
| **Threshold** | s = 255 if r ≥ T, else 0 (the slides show T = 100 and T = 128) | Segmentation |
| **Bounded threshold** | Threshold only inside a range; pass other pixels through unchanged | |
| **Posterize** | Reduce to n levels (the slide uses 8). With 2 levels this is a threshold. | |
| **Intensity-level slicing / range highlighting** | Boost one band of grey levels | Segment certain grey regions |
| **Bit clipping** | Keep the top k bits (the slide uses 2) | |
| **Iso-intensity contouring** | Mark pixels at chosen levels | Contour maps |
| **Solarize** | Invert above a threshold (the slide uses 150) | Artistic effect |
| **Parabola** | Quadratic curves | Artistic effect |

### Gamma correction

Cameras capture light **linearly**, but eyes and displays respond along a
**power curve**. Gamma correction stops images looking washed out or too dark
on different monitors.

- **γ < 1** (e.g. 0.45) **brightens**: it expands the dark tones.
- **γ > 1** (e.g. 2.2) **darkens**: it compresses the dark tones.
- The slides use **γ = 0.45 and 2.2**, and 0.45 ≈ 1/2.2. That's the standard
  display-gamma pair.

> Your `my-notes/intensity/transformation.py` runs γ ∈ {0.1, 0.5, 1.2, 2.2}
> with exactly this formula. One detail: the comment says *"Read the image in
> grayscale"*, but `cv2.imread('image.png')` loads it in **colour**, so gamma is
> applied to each BGR channel separately. Pass `cv2.IMREAD_GRAYSCALE` if you
> want grey.

---

## 5. Histograms

- A histogram is a bar chart with intensity on the x-axis and pixel count on the y-axis.
- It shows **contrast** and **overall brightness**. A narrow spread means low
  contrast, and a spread shifted left means a dark image.
- Scaling an image by ×1.2 or ÷1.2 **shifts and stretches** the histogram (slide 61).
- A **colour image** has one histogram per R, G and B channel. A greyscale image has one.

### Histogram equalization

**Goal:** make the output histogram as **uniform** as possible, which spreads
out the contrast.

1. Compute the histogram.
2. Compute the **normalised cumulative sum** (the CDF):
   **s_k = (L − 1) · Σ_{j=0..k} n_j / (M·N)**
3. Map every input level r_k to s_k.

In practice the result is only *approximately* flat. Because the levels are
discrete, peaks and valleys shift rather than disappear.

---

## If you're revising this in 10 minutes

1. **Rods = scotopic, no colour. Cones = photopic, colour.**
2. The **Weber ratio ΔI/I**. Perceived brightness ≠ intensity: **Mach bands** and **simultaneous contrast**.
3. **g(x,y) = T[f(x,y)]**. A 1×1 neighbourhood makes it a point operation.
4. **Sampling works on coordinates, quantization on amplitude.** Storage is **M·N·k bits**.
5. Know the **negative, threshold, contrast stretch and gamma** formulas.
6. **γ < 1 brightens, γ > 1 darkens.** The display pair is 0.45 and 2.2.
7. **Histogram equalization = map each level through its CDF**, scaled to L − 1.
8. Look through slides 4–36 in the pptx, because those diagrams aren't in this summary.
