# L9 — Point Processing: LUTs, Histograms, Arithmetic & Logic

**Multimedia Computing · Week 5 · 62 slides · Dr. Minhaz Uddin Ahmed**
Source: [week05 - Multimedia Computing L9.pptx](../slides/week05%20-%20Multimedia%20Computing%20L9.pptx) *(9.7 MB, posted as "L9_up")*

Point (1×1) operations: each output pixel depends **only on the same input
pixel's value**, so every one of them can be written as a look-up table. Many
slides are figures from Gonzalez ch. 3, and their text didn't extract, so
**open the pptx for the worked tables (slides 29–31, 44)**.

## Outline

| Slides | Topic |
|---|---|
| 3–6 | Image types: binary, grayscale, colour. RGB = 3 × 8 bit = **24 bit/pixel**. Data types |
| 7–8 | Spatial-domain model **g(x,y) = T[f(x,y)]**, with T over a neighbourhood of (x,y) |
| 9–12 | **Look-up tables**: the pixel value is an *index*, and the output is `LUT[value]`. A colourmap is an LUT, so an 8-bit index can address 24-bit colours |
| 13 | Point processing = 1×1 neighbourhood, **s = T(r)**. Contrast stretching vs binarisation (threshold) |
| 14–19 | Histogram: x = intensity, y = count. Shows contrast and brightness. ×1.2 and ÷1.2 stretch or squeeze it |
| 20–39 | **Histogram equalisation** |
| 40–45 | **Histogram specification (matching)** |
| 46–53 | Arithmetic ops: ± → brightness; ×, ÷ → contrast; overflow → **clamp** to [0,255]; subtraction → change/motion detection |
| 54–59 | Logic ops: NOT = `255 − p`, XOR, AND, OR (bitwise) |

## Histogram equalisation, the part to know cold

Goal: spread the grey levels so the output histogram is roughly uniform.

1. Compute the histogram h(r).
2. Compute the **normalised cumulative sum** (the CDF):
   `s_k = (L−1) · Σ_{j≤k} h(j) / N` where N = number of pixels.
3. Round, then use `s_k` as an LUT: replace every r_k with s_k.

Why it works (slides 23–24): if `s = T(r) = ∫₀ʳ p_r(w) dw` (the CDF), then
`p_s(s) = p_r(r)·|dr/ds| = 1`, which is uniform. T must be single-valued and
monotonically increasing so that it's invertible and keeps the order of grey levels.

Effects (slide 26): contrast **expands** near histogram peaks and is
**compressed** near valleys. The discrete result is **not flat**, because
levels can only merge, never split.

> The slide-30 example uses a 16-pixel, 8-level image, so the scale is
> (L−1)/N = 7/16 (for example, cumulative count 1 → 0.44, 3 → 1.31). The slide writes
> 0.43 because it truncates. Either way it rounds to 0.

## Histogram specification

Map the image so that its histogram matches a *chosen* one:

1. Equalise the input: `s = T(r)` (its CDF).
2. Equalise the target histogram: `v = G(z)` (the target CDF).
3. For each r, find the z with `G(z) ≈ T(r)`, i.e. `z = G⁻¹(T(r))`.

In short: input CDF → inverse target CDF.

## Quick facts likely to be asked

- Addition and subtraction shift the histogram, so they change **brightness, not contrast**.
- Multiplication and division scale the histogram, so they change **contrast**.
- Overflow and underflow are fixed by **clamping** (saturating) to 0/255.
- XOR with a constant flips selected bits. It's used to find pixels of one value
  and to draw cursors, because XOR-ing twice restores the original.

## How this connects

- **L6 already introduced histogram equalisation and gamma.** L9 is the full
  treatment (derivation, worked LUT, specification), so read them together.
- L7 covered connectivity and L8 covered tools (Octave `imhist`, `histeq`).
  The gamma (power-law) curves in `my-notes/intensity/` are the
  other family of intensity transforms in Gonzalez 3.2.
- OpenCV equivalents: `cv2.equalizeHist`, `cv2.LUT`, `cv2.add` (saturating),
  `cv2.bitwise_xor`.
