# L7 — Pixel Relationships, Light Measurement & Colour Spaces

**Multimedia Computing · Week 4 · 71 slides · Dr. Minhaz Uddin Ahmed**
Source: [week04 - Multimedia Computing L7.pptx](week04%20-%20Multimedia%20Computing%20L7.pptx) *(7 MB)*
Practice code: [Lecture7.ipynb](../resources/Lecture7.ipynb) (sRGB → CIE XYZ → chromaticity)
Reference: Gonzalez, *Digital Image Processing*, Ch. 2 and 6

The deck has two halves. The first half (slides 3–36) finishes Gonzalez Ch. 2:
how light is measured, how pixels relate to each other, and how far apart two
pixels are. The second half (slides 37–68) introduces **colour**: the HSI
model, Munsell, and especially **CIE XYZ** and the chromaticity diagram.
**Slides 42–45, 48–58 and 60–66 are figures or equations with almost no text**,
so open the pptx for the colour-matching curves and the chromaticity horseshoe.

**Contents:** coordinate convention · row- vs column-major storage ·
radiometry vs photometry · scotopic/photopic sensitivity · achromatic light ·
radiance, luminance, brightness · image formation f = i·r · resolution and
bit depth · N4 / ND / N8 neighbours · 4-, 8- and m-connectivity · paths,
adjacency, boundaries · Euclidean, city-block and chessboard distance ·
arithmetic and logical image operations · HSI, Munsell · CIE XYZ, CIE RGB,
chromaticity diagram · gamut, PAL/NTSC · colour stimuli.

---

## 1. Storing an image

- **Coordinate convention:** pixel (x, y), with the origin top-left. You can
  treat an image element by element (each pixel on its own) or as one matrix
  (for spatial transforms).
- **Flattening.** Embedded code stores the image as a 1-D array.
  - **Row-major** (C, NumPy): index = `y·W + x`.
  - **Column-major** (MATLAB, Fortran): index = `x·H + y`.
  This matters in L8: MATLAB `A(:)` walks down the **columns**.

## 2. Measuring light

| Term | Means | Unit given in the deck |
|---|---|---|
| **Radiometry** | Measuring radiation across the *whole* optical spectrum | watt (W) |
| **Photometry** | Measuring only the *visible* part, **weighted by the eye's response** | — |
| **Radiance** | Total energy flowing from the source | W |
| **Luminance** | Energy the **observer perceives** from the source | lumen (lm) |
| **Brightness** | A subjective impression. **Practically impossible to measure** | — |

- The frequency of light **f = c/λ** and the photon energy **E = hf** stay the
  same in any medium. Speed and wavelength change with the refractive index n.
- **Eye sensitivity:**
  - **Photopic** (cones, bright light): peak at **555 nm** (yellow-green). Sensitivity halves at 510 and 610 nm.
  - **Scotopic** (rods, dim light): peak at **507 nm** (blue-green).
- **Achromatic (monochromatic) light** has only one attribute, **intensity**.
  That is a grayscale image.
- **Image formation model** (repeated from L6): **f(x,y) = i(x,y) · r(x,y)**,
  with 0 < f < ∞. Here i is illumination and r is reflectance.
- **Storage:** **b = M × N × k** bits for an M×N image with 2ᵏ grey levels.

> The units in the table are Gonzalez's simplified definitions, and that is what
> to write in the exam. Strictly, radiance is W·sr⁻¹·m⁻² and luminance is
> cd/m², while **lumen is luminous *flux***.

## 3. Neighbours, connectivity, adjacency

For pixel p at (x, y):

- **N4(p)** are the 4 horizontal and vertical neighbours: (x±1, y) and (x, y±1).
- **ND(p)** are the 4 diagonal neighbours: (x±1, y±1).
- **N8(p) = N4 ∪ ND** gives 8 neighbours.

Let **V** be the set of values that count as "foreground", e.g. V = {1}.

- **4-connected:** p, q ∈ V and q ∈ N4(p).
- **8-connected:** p, q ∈ V and q ∈ **N8**(p).
- **m-connected (mixed):** q ∈ N4(p), **or** q ∈ ND(p) **and** N4(p) ∩ N4(q)
  contains no pixel from V.
  **Why m-connectivity exists:** 8-connectivity can create *two* paths between
  the same pixels, one diagonal and one around the corner. m-connectivity
  removes the ambiguity by using the diagonal only when no 4-path exists.

> ⚠️ **Slide 22 has a typo.** It defines 8-connectivity as "q is in the set
> **N4**(p)", which is the 4-connectivity definition. It should say **N8(p)**.

- **Path** from p to q: a sequence of distinct pixels, each adjacent to the
  next. Its **length n** is the number of steps.
- **Adjacent regions:** R1 and R2 are adjacent if some pixel of R1 is adjacent
  to some pixel of R2. The kind of adjacency (4, 8 or m) must be stated.
- **Boundary subtlety (slides 28–29):** a pixel can count as boundary under
  8-adjacency but not under 4-adjacency. Also, the *inner* boundary of a region
  need not be a closed path, though the *outer* one always is.

## 4. Distance measures

A function D is a **metric** if it is non-negative (and zero only for p = q),
symmetric, and satisfies the triangle inequality.

For p = (x, y), q = (s, t):

| Name | Formula | Shape of "distance ≤ r" | p=(0,0), q=(4,4) |
|---|---|---|---|
| **Euclidean D_E** | √((x−s)² + (y−t)²) | disc | √32 ≈ **5.66** |
| **City-block D4** | \|x−s\| + \|y−t\| | **diamond** | **8** |
| **Chessboard D8** | max(\|x−s\|, \|y−t\|) | **square** | **4** |
| **D_m** | length of the shortest m-path | depends on pixel values | — |

The worked values come from the speaker notes, which round D_E to 5.65.
**D4 and D8 depend only on coordinates. D_m depends on the pixel values along
the way.** That is the point of slide 34's exercise ("find the m-distance from
p to p4").

## 5. Image arithmetic and logic

- Arithmetic (+ − × ÷) is element-wise and **needs images of the same size**.
  [practice code L8](../resources/practice%20code%20L8%20-%20experiment.txt)
  adds the cat and dog images.
- Logical operations (AND, OR, NOT, XOR) act on **binary** images, with white = 1 and black = 0.

## 6. Colour

- **RGB** stores one channel per primary. **HSI** separates the colour (hue, saturation) from **intensity**.
- **Munsell (1915)** describes colour by **hue** (which colour), **value**
  (light or dark) and **chroma/saturation** (how vivid). A colour *solid* adds
  saturation as the third axis of a 2-D colour wheel.
- Other spaces named: **HSL, HSV, LUV, CIE L\*a\*b\***. In Lab, L\* is
  lightness, a\* is the red–green axis and b\* is the yellow–blue axis.
- **CIE XYZ (1931):**
  - **Y = luminance**, matched to the eye's brightness sensitivity.
  - **X** is a red-ish mix chosen so every value stays positive.
  - **Z** roughly corresponds to the blue response.
- **Chromaticity** is colour without brightness:
  **x = X/(X+Y+Z), y = Y/(X+Y+Z)**, with z = 1 − x − y.
  The **chromaticity diagram** is the horseshoe of all visible colours in the
  (x, y) plane. In polar form around the white point, the angle is **hue** and the
  radius is **saturation**. See slides 61–65.
- **Colour blindness** shifts the luminous-efficiency peak. Protanopia moves it
  to about 540 nm (nothing above 670 nm is seen). Deuteranopia moves it to about 560 nm.
- **Gamut** is the subset of colours a device or colour space can reproduce. On
  the diagram it is a triangle whose corners are the device's three primaries.
  Analogue TV standards: **NTSC 525 lines, PAL 625 lines**.
- **Colour stimuli:**
  - **monochromatic** has one wavelength (a laser);
  - **achromatic** has equal energy at all wavelengths (daylight comes close);
  - **polychromatic** has unequal amounts, which covers most real light.
- A **colorimeter** measures absorbance and transmittance through a sample
  under a fixed illuminant, e.g. for blood, water or soil analysis.

## Practice code: [Lecture7.ipynb](../resources/Lecture7.ipynb)

Python, no libraries. `srgb_to_xyz(r, g, b)`:

1. Scale 0–255 values to 0–1.
2. **Undo the sRGB gamma:** c/12.92 if c ≤ 0.04045, else ((c+0.055)/1.055)^2.4.
   This is the inverse of L6's gamma curve.
3. Multiply by the **sRGB→XYZ matrix (D65 white)**. The Y row,
   **0.2126 R + 0.7152 G + 0.0722 B**, is the standard luminance formula.
4. Compute chromaticity x, y. Pure black falls back to the D65 white point (0.3127, 0.3290).

Try the commented-out Yellow and Cyan. They should land between their two
primaries on the chromaticity diagram.

## Likely exam material

- Define N4, ND, N8 and 4-, 8- and m-connectivity, and explain *why* m-connectivity exists.
- Compute D_E, D4 and D8 between two pixels, and sketch the diamond and square.
- Radiometry vs photometry, and radiance vs luminance vs brightness.
- Photopic vs scotopic peaks: 555 nm vs 507 nm.
- Convert XYZ to chromaticity (x, y), and say what Y represents.
