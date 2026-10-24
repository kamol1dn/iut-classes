# L10 — Morphological Image Processing

**Multimedia Computing · Week 5 · 61 slides · Dr. Minhaz Uddin Ahmed**
Source: [week05 - Multimedia Computing L10.pptx](../slides/week05%20-%20Multimedia%20Computing%20L10.pptx) *(4.3 MB)*

Gonzalez **chapter 9**. Most equations and worked grids are images, so **open the
pptx for slides 20–25 and 30–47**. L8's Octave `strel` / `imerode` demo
was a preview of this lecture.

## Outline

| Slides | Topic |
|---|---|
| 3–6 | Morphology is a set of non-linear, shape-based operations. **Structuring element (SE)**: a small 0/1 matrix, usually odd-sized with its origin at the centre. It plays the role a kernel plays in convolution. An SE **fits** the image if every 1 lands on a 1, and **hits** it if at least one does |
| 7–9 | Set theory: translation, **reflection B̂**, logic ops on binary images |
| 10–11 | Morphology depends only on pixel *ordering*, so it suits binary images. Uses: denoising, separating and joining objects, finding bumps and holes |
| 12–14 | **Dilation** = local **max** under the SE. Bright regions grow |
| 15–19 | **Erosion** = local **min**. Bright regions shrink and holes grow |
| 20–25 | Set definitions plus worked examples |
| 26–35 | **Opening** and **closing**, with their properties |
| 36–37 | Hit-or-miss transform |
| 38–47 | Algorithms: boundary extraction, region filling, connected components, thinning, skeletons |
| 48–51 | Summary table (Gonzalez Table 9.1) |
| 52–54 | Grey-scale extension |
| 55–58 | Morphological gradient, top-hat, skeletonisation, pruning |

## The definitions to memorise

| Op | Set form | Pixel intuition | Effect |
|---|---|---|---|
| Dilation | `A ⊕ B = { z : (B̂)_z ∩ A ≠ ∅ }` | max | grows objects, fills small holes and gaps |
| Erosion | `A ⊖ B = { z : (B)_z ⊆ A }` | min | shrinks objects, removes small specks |
| Opening | `A ∘ B = (A ⊖ B) ⊕ B` | erode → dilate | removes small **bright** specks and thin protrusions, breaks narrow isthmuses |
| Closing | `A • B = (A ⊕ B) ⊖ B` | dilate → erode | removes small **dark** holes, fuses narrow breaks, fills gaps |

Properties (slide 34): opening is **anti-extensive**, `A∘B ⊆ A`. Closing is
**extensive**, `A ⊆ A•B`. Both are **increasing**: if C ⊆ D, then C∘B ⊆ D∘B.
Both are **idempotent**: applying them twice changes nothing more.

Duality: erosion of the foreground = dilation of the background, and
opening ↔ closing under complement.

## Derived operations

- **Boundary**: `β(A) = A − (A ⊖ B)`, the object minus its eroded self.
- **Region filling**: `X_k = (X_{k−1} ⊕ B) ∩ Aᶜ`, starting from a seed point p
  inside the hole. Repeat until X stops changing.
- **Connected components**: the same iteration, but intersect with A instead of Aᶜ.
- **Morphological gradient**: `(A ⊕ B) − (A ⊖ B)`, which highlights edges.
- **Top-hat**: white = `A − (A ∘ B)`, which keeps small bright details. Black =
  `(A • B) − A`, which keeps small dark details. Good for uneven illumination.
- **Skeleton**: erode repeatedly, and keep at each step whatever opening would remove.
  **Pruning** then trims the spurs.

## Small slide issues

- Slide 12 says dilation is *"convoluting"* the image with a kernel. It
  isn't a convolution: it's a max over the SE, which is non-linear. The kernel only
  supplies the neighbourhood shape.
- Slide 29: "long thing gulfs" should read "long **thin** gulfs".

## Try it

```python
import cv2, numpy as np
k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
er  = cv2.erode(img, k);  di = cv2.dilate(img, k)
op  = cv2.morphologyEx(img, cv2.MORPH_OPEN,  k)
cl  = cv2.morphologyEx(img, cv2.MORPH_CLOSE, k)
grd = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, k)
th  = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, k)
```
