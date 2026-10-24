# L11: Spatial Filtering and Edge Detection

**Multimedia Computing · Week 6 · 63 slides · Dr. Minhaz Uddin Ahmed**
Source: [week06 - Multimedia Computing L11.pptx](week06%20-%20Multimedia%20Computing%20L11.pptx) *(11.2 MB)*

Gonzalez **chapter 3** (spatial filtering). Most of the figures, the masks and the formulas are images,
so **open the pptx for the masks on slides 16, 20–21, 28, 37–43 and 49**. This is the
material for Assignment 1's filtering/edge tasks, so it's worth reading before you start the image part.

## Outline

| Slides | Topic |
|---|---|
| 3–5 | A **mask** is a filter. Spatial filtering means convolving a mask with the image. Uses: blur and denoise, or sharpen and find edges |
| 6–8 | **Edges** are horizontal, vertical or diagonal. Edge operators come in two families: **gradient** (1st derivative: Roberts, Prewitt, Sobel) and **Gaussian-based** (2nd derivative: LoG, and the deck also lists Canny here) |
| 9–10 | Histogram statistics: mean, *n*th moment, variance. **Global** vs **local** enhancement |
| 11–14 | **Convolution** is a weighted sum of the neighbourhood, with weights taken from the kernel. 1-D first, then 2-D |
| 15 | **Borders**: zero-pad, skip the edge (start at (1,1) for a 3×3), duplicate the edge rows/cols, or wrap around |
| 16–19 | **Blurring** (low-pass): box masks with all entries 1/9 (3×3) or 1/25 (5×5). A bigger mask blurs more. **Gaussian** smoothing, where σ sets the spread. Interactive demo: setosa.io/ev/image-kernels |
| 20–26 | **Sharpening** (high-pass), **unsharp masking**, **high-boost** |
| 27–28 | Discontinuities: **point** detection (`|R| > T`) and **line** masks |
| 29–36 | Edge types (step, ramp, roof, line). **Homogeneity operator** (max of 8 differences) vs **difference operator** (4 subtractions, faster) |
| 37–40 | First-derivative masks: **Roberts, Sobel, Prewitt** |
| 41–42 | **Compass** operators (8 orientations): Prewitt, Kirsch, Robinson 3- and 5-level |
| 43–44 | **Sobel**: two 3×3 kernels (Gx, Gy). Cheap to compute, but noisy and gives thick edges |
| 45–47 | **Laplacian** (2nd derivative): edges show up as **zero crossings**. It's very noise-sensitive, gives double edges and no direction. ZC code, plus a ZC test with a threshold |
| 48–50 | **LoG** (Gaussian, then Laplacian) and **DoG**, a cheaper approximation of LoG (σ ratio ≈ 1.6). A bigger DoG mask finds wider edges |
| 51–52 | **Colour edges**: luminance only, per RGB channel, or per channel then summed |
| 53–59 | **Median** filter: removes impulse (salt-and-pepper) noise and keeps edges, which low-pass can't do. Colour median: per channel (breaks colour correlation) vs the **vector median** (pick the xᵢ with the smallest summed distance) |
| 60 | **Min / max** filters, and cascading them |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Discrete 2-D convolution | `g(x,y) = Σₛ Σₜ w(s,t) · f(x−s, y−t)` |
| Box blur | every weight = `1/(n²)` |
| Unsharp mask | `sharp = original − lowpass` |
| High-boost | `HB = A·original − lowpass`. A = 1 gives a plain high-pass. A > 1 keeps more background and looks lighter |
| Point detection | `R = Σ wᵢ zᵢ`, a point where `|R| > T` |
| Gradient magnitude | `|∇f| ≈ √(Gx² + Gy²)`, often `|Gx| + |Gy|` |
| Laplacian | `∇²f = ∂²f/∂x² + ∂²f/∂y²` → zero crossings mark edges |
| DoG ≈ LoG | `σ₂/σ₁ ≈ 1.6` |

Sensitivity claims as the deck states them (from Umbaugh, so expect them on an exam):
**Roberts** has the smallest support and is the most noise-prone. **Sobel** is "more sensitive to
diagonal edges". **Prewitt** is "more sensitive to horizontal/vertical edges".

## Things that are wrong or loose in the deck

- **Slide 60 swaps opening and closing.** It says *closing = min → max, opening = max → min*.
  L10 (and Gonzalez) define **opening = erosion (min) then dilation (max)** and
  **closing = max then min**. Go with L10.
- **Slide 8 files Canny under "second-order, Gaussian-based".** Canny actually works on the
  **first-derivative** gradient of a Gaussian-smoothed image, followed by non-max suppression and
  hysteresis. Only LoG belongs in the second-order group.
- Slide 51 says "HSU space". It means HSI/HSV.
- Slide 4 contrasts "linear/smoothing filters" with "frequency domain filters", which isn't a real
  split. Spatial vs frequency domain is about *where* you filter. Linear vs non-linear (median, min/max)
  is about *what* the filter does.
