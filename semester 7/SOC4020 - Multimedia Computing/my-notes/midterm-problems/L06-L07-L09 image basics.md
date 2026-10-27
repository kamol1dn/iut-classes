# Midterm practice: L6 + L7 + L9 (image basics, pixel relationships, point processing)

Human vision, sampling and quantization, storage, intensity transforms (L6);
neighbours, adjacency, paths, distances, arithmetic/logic, colour (L7); LUTs,
histogram equalisation, histogram specification, point arithmetic and logic (L9).
Every number below was checked in Python (numpy).

Attempt each problem before opening the solution. Problems marked **[slide]**
copy the professor's own example. The rest use the same method on small numbers
you can do by hand.

**Conventions used here (say them in the exam too):**
- Pixel coordinates are (row, column), origin at the top-left.
- Rounding is to the **nearest** integer. The professor rounds 2.18 → 2 and 4.81 → 5 (L9 S30-31).
- 8-bit means values 0-255, so L − 1 = 255. 3-bit means 0-7, so L − 1 = 7.

---

## Formula sheet

| What | Formula | Notes | Source |
|---|---|---|---|
| Spatial-domain model | **g(x,y) = T[f(x,y)]** | 1×1 neighbourhood = point op, **s = T(r)** | L6 S22, L9 S8, S13 |
| Image formation | **f(x,y) = i(x,y) · r(x,y)**, 0 < f < ∞ | i = illumination, r = reflectance | L6 S23, L7 S18-19 |
| Grey levels | **L = 2^k** | values 0 … L − 1 | L7 S20 |
| Storage | **b = M × N × k** bits | ÷ 8 for bytes; RGB = 3 × 8 = **24 bit/pixel** | L6 S28, L7 S20, L9 S5 |
| Row-major index | **y·W + x** (row y, column x) | C, NumPy | L7 S4 |
| Column-major index | **x·H + y** | MATLAB, Fortran | L7 S4 |
| Weber ratio | **ΔI / I** | small = good discrimination | L6 S6 |
| Negative | **s = (L − 1) − r** = 255 − r | slide: y = −x + 255; also "NOT" | L6 S45, L9 S55 |
| Threshold | **s = 255 if r ≥ T, else 0** | slides use T = 100 and 128 | L6 S42-43 |
| Contrast stretch (low/high) | **s = 255 · (r − low)/(high − low)**, 0 below low, 255 above high | | L6 S37 |
| Contrast stretch (min/max) | **y = (2^B − 1)/(x_max − x_min) · (x − x_min)** | B = bits | L6 S38 |
| Log | **s = c · log(1 + r)**, c = (L − 1)/log(L) | any log base, c absorbs it | Gonzalez 3.2 (not on slides) |
| Gamma (power law) | **s = (L − 1) · (r/(L − 1))^γ** | **γ < 1 brightens, γ > 1 darkens**; slides: 0.45 and 2.2 | L6 S47-48, S53 |
| Bit plane k | **(r >> k) & 1** | plane 7 = MSB = threshold at 128 | L6 S55 |
| Bit clipping (top 2 bits) | **r AND 11000000₂** = r AND 192 | | L6 S55 |
| LUT | **out = LUT[in]** | pixel value is the index | L9 S9-11 |
| Histogram | h(r_k) = n_k, p(r_k) = n_k / MN | | L9 S14 |
| **Histogram equalisation** | **s_k = (L − 1) · Σ_{j≤k} n_j / MN**, then round | = (L−1)·CDF | L9 S20-31 |
| Histogram specification | s = T(r), v = G(z), **z = G⁻¹(T(r))** | match each s to the closest G(z) | L9 S40-44 |
| N4(p) | (x±1, y), (x, y±1) | 4 pixels | L7 S21 |
| ND(p) | (x±1, y±1) | 4 diagonals | L7 S21 |
| N8(p) | N4 ∪ ND | 8 pixels | L7 S21 |
| m-adjacent | q ∈ N4(p), **or** q ∈ ND(p) **and N4(p) ∩ N4(q) has no pixel in V** | removes double paths | L7 S23-24, L6 S35 |
| Euclidean | **D_E = √((x−s)² + (y−t)²)** | disc | L7 S31 |
| City-block | **D4 = \|x−s\| + \|y−t\|** | diamond | L7 S32 |
| Chessboard | **D8 = max(\|x−s\|, \|y−t\|)** | square | L7 S33 |
| Metric | D ≥ 0 (= 0 iff p = q); D(p,q) = D(q,p); D(p,z) ≤ D(p,q) + D(q,z) | | L7 S30 |
| Add / subtract | **I'(x,y) = I(x,y) + a** | **brightness**, not contrast | L9 S46, S48 |
| Multiply / divide | I · a, I / a | **contrast** | L9 S50 |
| Overflow | **clamp** to [0, 255] | | L9 S52 |
| NOT | **255 − p** | | L9 S55 |
| Chromaticity | **x = X/(X+Y+Z), y = Y/(X+Y+Z)**, z = 1 − x − y | Y = luminance | L7 S47, S54 |
| CMY | **C = 1 − R, M = 1 − G, Y = 1 − B** (normalised) or 255 − R … | Gonzalez Ch. 6 | not on slides |
| Grey from RGB | (R+G+B)/3 (HSI intensity) or 0.299R + 0.587G + 0.114B | Lecture7.ipynb uses 0.2126/0.7152/0.0722 | L7 S37 |

**Numbers to know by heart:** visible light 380-700 nm · photopic peak **555 nm**
(half at 510 and 610) · scotopic peak **507 nm** · rods = scotopic (no colour),
cones = photopic (colour) · NTSC 525 lines, PAL 625 lines · CIE RGB primaries
435.8, 546.1, 700 nm · protanopia peak ≈ 540 nm, deuteranopia ≈ 560 nm.

---

## Part A: storage, LUTs and point transforms

### Problem 1: Storage size (L6 S28, L7 S20) [slide]

(a) How many bits and bytes does a 1024 × 1024 image with 256 grey levels need?
(b) The professor circled the bottom-right cell of Table 2.1: N = 8192, k = 8. Give it in bits and in MB.
(c) A 640 × 480 RGB image at 24 bits/pixel: how many bytes?

<details><summary>Solution</summary>

256 levels → k = log₂ 256 = 8 bits.

| Part | M × N × k | Bits | Bytes |
|---|---|---|---|
| (a) | 1024 × 1024 × 8 | 8,388,608 | 1,048,576 = **1 MB** |
| (b) | 8192 × 8192 × 8 | **536,870,912** | 67,108,864 = **64 MB** |
| (c) | 640 × 480 × 24 | 7,372,800 | **921,600 bytes** (≈ 900 KB) |

Final: **(a) 8,388,608 bits = 1 MB, (b) 536,870,912 bits = 64 MB, (c) 921,600 bytes.**

*Trap:* the formula uses k (bits), not L (levels). 256 × 1024 × 1024 is wrong. Divide by 8 for bytes.
</details>

### Problem 2: Working backwards to grey levels; indexed colour (L7 S20, L9 S5, S9)

(a) A 256 × 256 grayscale image occupies exactly 49,152 bytes. How many grey levels does it have?
(b) A 256 × 256 colour image is stored as 8-bit indices into a 256-entry RGB colormap (LUT). Compare its size with a true 24-bit image.

<details><summary>Solution</summary>

(a) bits = 49,152 × 8 = 393,216. k = 393,216 / (256 × 256) = 393,216 / 65,536 = **6 bits → L = 2⁶ = 64 levels** (0-63).

(b)

| Item | Calculation | Bytes |
|---|---|---|
| Index image | 256 × 256 × 1 byte | 65,536 |
| Colormap | 256 entries × 3 bytes | 768 |
| **Indexed total** | | **66,304** |
| True colour | 256 × 256 × 3 bytes | **196,608** |

The indexed image is about **3× smaller**, but it can show only 256 different colours at once.

*Trap:* don't forget the LUT itself (768 bytes). The professor's point (L9 S9): "an 8-bit index number can be used to look up a 24-bit RGB colour".
</details>

### Problem 3: Flattening, row-major vs column-major (L7 S4)

An image is W = 5 columns wide and H = 4 rows high. Pixel at row y = 2, column x = 3. What is its 1-D index (starting at 0) in row-major order and in column-major order?

<details><summary>Solution</summary>

| Order | Formula | Value |
|---|---|---|
| Row-major (C, NumPy) | y·W + x = 2·5 + 3 | **13** |
| Column-major (MATLAB) | x·H + y = 3·4 + 2 | **14** |

*Trap:* row-major multiplies by the **width**, column-major by the **height**. Mixing them gives 2·4 + 3 = 11 or 3·5 + 2 = 17.
</details>

### Problem 4: Apply a look-up table (L9 S11) [slide]

The professor's 3-bit LUT is `LUT = [0, 0, 1, 1, 2, 3, 4, 5]` (index 0 … 7). Apply it to the 5 × 5 input image:

```
7 7 5 4 2
7 6 4 3 0
7 6 4 3 1
6 6 4 2 0
5 5 3 1 0
```

<details><summary>Solution</summary>

| r | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| LUT[r] | 0 | 0 | 1 | 1 | 2 | 3 | 4 | 5 |

Replace each pixel by LUT[pixel]:

```
5 5 3 2 1
5 4 2 1 0
5 4 2 1 0
4 4 2 1 0
3 3 1 0 0
```

The slide's first row **5 5 3 2 1** matches. **Output above.** The LUT darkens the image and compresses 8 levels into 6 (0-5).

*Trap:* the pixel value is the **index**, not a position in the image. LUT[7] = 5 (the 8th entry), not 7.
</details>

### Problem 5: Image negative (L6 S44-45, L9 S55)

(a) 8-bit image `[[0, 50, 100], [150, 200, 255], [30, 128, 77]]`. Find the negative.
(b) 3-bit image `[[0, 3], [5, 7]]`. Find the negative.

<details><summary>Solution</summary>

(a) s = 255 − r:

| r | 0 | 50 | 100 | 150 | 200 | 255 | 30 | 128 | 77 |
|---|---|---|---|---|---|---|---|---|---|
| s | 255 | 205 | 155 | 105 | 55 | 0 | 225 | 127 | 178 |

**[[255, 205, 155], [105, 55, 0], [225, 127, 178]]**

(b) L = 8, so s = 7 − r: **[[7, 4], [2, 0]]**.

*Trap:* the negative uses L − 1, not L. For 3-bit it is 7 − r, not 8 − r and not 255 − r.
</details>

### Problem 6: Threshold and contrast stretching (L6 S37, S42-43, L9 S13)

Image (8-bit):

```
 90 100 110
120 130 140
151 160 105
```

(a) Threshold with T = 128 (s = 255 if r ≥ T, else 0).
(b) Contrast-stretch with low = 100, high = 151 using the slide-37 formula.

<details><summary>Solution</summary>

(a) Only 130, 140, 151, 160 are ≥ 128:

```
  0   0   0
  0 255 255
255 255   0
```

(b) 255 / (151 − 100) = 255 / 51 = **5**, so s = 5 · (r − 100), clamped:

| r | 90 | 100 | 110 | 120 | 130 | 140 | 151 | 160 | 105 |
|---|---|---|---|---|---|---|---|---|---|
| rule | ≤ low → 0 | 0 | 5·10 | 5·20 | 5·30 | 5·40 | 5·51 | ≥ high → 255 | 5·5 |
| s | 0 | 0 | 50 | 100 | 150 | 200 | 255 | 255 | 25 |

**Stretched: [[0, 0, 50], [100, 150, 200], [255, 255, 25]]**

*Trap:* values outside [low, high] are clipped to 0 or 255. Plugging 160 into the formula gives 295, which is out of range.
</details>

### Problem 7: Contrast stretching, min/max form (L6 S38)

A 4-bit image (B = 4, values 0-15) only uses 4 … 9:

```
4 5 6
7 8 9
5 6 7
```

Stretch it to the full range with y = (2^B − 1)/(x_max − x_min) · (x − x_min).

<details><summary>Solution</summary>

x_min = 4, x_max = 9, 2⁴ − 1 = 15, factor = 15 / 5 = **3**. So y = 3(x − 4).

| x | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|
| y | 0 | 3 | 6 | 9 | 12 | 15 |

**[[0, 3, 6], [9, 12, 15], [3, 6, 9]]**. The used range goes from 4-9 (width 5) to 0-15 (width 15).

*Trap:* use 2^B − 1 = 15, not 2^B = 16; with 16 the maximum would come out as 16, which does not fit in 4 bits.
</details>

### Problem 8: Log transform (Gonzalez 3.2, in the brief, not on the slides)

Apply s = c · log₁₀(1 + r) to an 8-bit image with pixels 0, 9, 99, 255, choosing c so that 255 maps to 255.

<details><summary>Solution</summary>

c = 255 / log₁₀(256) = 255 / 2.408 = **105.89**.

| r | 1 + r | log₁₀(1 + r) | s = 105.89 · log | rounded |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | **0** |
| 9 | 10 | 1 | 105.89 | **106** |
| 99 | 100 | 2 | 211.77 | **212** |
| 255 | 256 | 2.408 | 255 | **255** |

**0 → 0, 9 → 106, 99 → 212, 255 → 255.** Dark values are spread out a lot: 0-9 becomes 0-106.

*Trap:* the "+1" stops log(0) = −∞. With natural log, c = 255/ln 256 = 45.99 and you get the same s values.
</details>

### Problem 9: Gamma correction (L6 S47-48, S53; your transformation.py)

s = 255 · (r/255)^γ.
(a) Normalised inputs r/255 = 0.25 and 0.5: compute the output for γ = 0.5 and γ = 2.
(b) r = 100: compute s for the slide values γ = 0.45 and γ = 2.2.

<details><summary>Solution</summary>

(a)

| r/255 | γ = 0.5 | γ = 2 |
|---|---|---|
| 0.25 | √0.25 = **0.5** | 0.25² = **0.0625** |
| 0.5 | √0.5 = **0.707** | 0.5² = **0.25** |

(b) r/255 = 0.392.

| γ | 0.392^γ | s = 255 · … | rounded |
|---|---|---|---|
| 0.45 | 0.656 | 167.3 | **167** (brighter) |
| 2.2 | 0.1275 | 32.5 | **33** (darker) |

Final: **γ = 0.45 → 167, γ = 2.2 → 33.**

*Trap:* normalise first. 100^0.45 = 7.9 is nonsense. 0 and 255 never move for any γ.
</details>

### Problem 10: Bit-plane slicing and bit clipping (L6 S55)

(a) Write 173 in binary and list all 8 bit planes.
(b) Apply 2-bit bit clipping (keep the top 2 bits) to 173.
(c) Give bit plane 7 and bit plane 0 of `[[200, 100, 173], [64, 255, 127]]`.

<details><summary>Solution</summary>

(a) 173 = 128 + 32 + 8 + 4 + 1 = **10101101₂**.

| Plane | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|
| Bit | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |

(b) 173 AND 11000000₂ = 10000000₂ = **128**.

(c) Plane 7 = (r ≥ 128): **[[1, 0, 1], [0, 1, 0]]**. Plane 0 = odd/even: **[[0, 0, 1], [0, 1, 1]]**.

*Trap:* plane 7 is the **most** significant bit and looks like a threshold at 128. Plane 0 looks like noise.
</details>

---

## Part B: histograms

### Problem 11: Histogram equalisation, the professor's example (L9 S29-31) [slide]

3-bit image (L = 8), 4 × 4 = 16 pixels:

```
4 4 3 3
4 4 3 3
4 1 2 3
0 1 2 3
```

Equalise it. Give the full table and the output image.

<details><summary>Solution</summary>

MN = 16, L − 1 = 7, so s_k = 7 · cum_k / 16.

| r_k | n_k | p_k = n_k/16 | cum n | CDF | 7·CDF | s_k |
|---|---|---|---|---|---|---|
| 0 | 1 | 0.0625 | 1 | 0.0625 | 0.44 | **0** |
| 1 | 2 | 0.125 | 3 | 0.1875 | 1.31 | **1** |
| 2 | 2 | 0.125 | 5 | 0.3125 | 2.19 | **2** |
| 3 | 6 | 0.375 | 11 | 0.6875 | 4.81 | **5** |
| 4 | 5 | 0.3125 | 16 | 1.0 | 7.00 | **7** |
| 5 | 0 | 0 | 16 | 1.0 | 7.00 | 7 |
| 6 | 0 | 0 | 16 | 1.0 | 7.00 | 7 |
| 7 | 0 | 0 | 16 | 1.0 | 7.00 | 7 |

Output (the slide-31 result):

```
7 7 5 5
7 7 5 5
7 1 2 5
0 1 2 5
```

**LUT 0→0, 1→1, 2→2, 3→5, 4→7.** The output histogram is n(0)=1, n(1)=2, n(2)=2, n(5)=6, n(7)=5. The tall bars are pushed apart (gap at 3, 4 and 6), and it is **not** flat.

*Trap:* the slide writes 1 × 7/16 = **0.43**. That is truncated; the exact value is 0.4375. It rounds to 0 either way.
</details>

### Problem 12: Histogram equalisation of a dark 5 × 5 image

3-bit image (L = 8), 25 pixels:

```
0 0 1 1 2
0 1 1 2 3
0 1 1 2 4
0 1 2 3 5
0 1 2 3 4
```

<details><summary>Solution</summary>

Count first: n = [6, 8, 5, 3, 2, 1, 0, 0] (sum 25). s_k = 7 · cum / 25.

| r_k | n_k | p_k | cum n | CDF | 7·CDF | s_k |
|---|---|---|---|---|---|---|
| 0 | 6 | 0.24 | 6 | 0.24 | 1.68 | **2** |
| 1 | 8 | 0.32 | 14 | 0.56 | 3.92 | **4** |
| 2 | 5 | 0.20 | 19 | 0.76 | 5.32 | **5** |
| 3 | 3 | 0.12 | 22 | 0.88 | 6.16 | **6** |
| 4 | 2 | 0.08 | 24 | 0.96 | 6.72 | **7** |
| 5 | 1 | 0.04 | 25 | 1.00 | 7.00 | **7** |
| 6 | 0 | 0 | 25 | 1.00 | 7.00 | 7 |
| 7 | 0 | 0 | 25 | 1.00 | 7.00 | 7 |

Output:

```
2 2 4 4 5
2 4 4 5 6
2 4 4 5 7
2 4 5 6 7
2 4 5 6 7
```

**LUT 0→2, 1→4, 2→5, 3→6, 4→7, 5→7.** New histogram: n(2)=6, n(4)=8, n(5)=5, n(6)=3, n(7)=3. The dark image now uses 2-7 and is brighter. Levels 4 and 5 **merged** into 7.

*Trap:* the darkest level does **not** stay 0. s_0 = 7 · 6/25 = 1.68 → 2, because 6 pixels already sit there.
</details>

### Problem 13: Histogram equalisation from a histogram only (Gonzalez Ex. 3.5)

A 64 × 64 3-bit image has n_k = 790, 1023, 850, 656, 329, 245, 122, 81 for r = 0 … 7. Find s_k and the equalised histogram.

<details><summary>Solution</summary>

MN = 4096.

| r_k | n_k | p_k | cum n | 7·CDF | s_k |
|---|---|---|---|---|---|
| 0 | 790 | 0.19 | 790 | 1.35 | **1** |
| 1 | 1023 | 0.25 | 1813 | 3.10 | **3** |
| 2 | 850 | 0.21 | 2663 | 4.55 | **5** |
| 3 | 656 | 0.16 | 3319 | 5.67 | **6** |
| 4 | 329 | 0.08 | 3648 | 6.23 | **6** |
| 5 | 245 | 0.06 | 3893 | 6.65 | **7** |
| 6 | 122 | 0.03 | 4015 | 6.86 | **7** |
| 7 | 81 | 0.02 | 4096 | 7.00 | **7** |

Equalised histogram (add the counts that land on the same s):

| s | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| n | 0 | 790 | 0 | 1023 | 0 | 850 | 656 + 329 = **985** | 245 + 122 + 81 = **448** |

**s = [1, 3, 5, 6, 6, 7, 7, 7].** Only 5 distinct levels are left out of 8.

*Trap:* when two r map to the same s, **add** their counts. Don't list 6 twice.
</details>

### Problem 14: Histogram specification (L9 S29, S44) [slide]

Use the slide-29 image from Problem 11. The desired histogram (slide 44) puts all 16 pixels at the bright end: n_z = 0, 0, 0, 0, 0, **6, 5, 5** for z = 0 … 7. Find the mapping r → z and the output image.

<details><summary>Solution</summary>

**Step 1, equalise the input** (from Problem 11): T(r) = 0.44, 1.31, 2.19, 4.81, 7, … → s = 0, 1, 2, 5, 7.

**Step 2, equalise the target:** G(z) = 7 · cum(n_z) / 16.

| z | n_z | cum | G(z) |
|---|---|---|---|
| 0-4 | 0 | 0 | 0.0 |
| 5 | 6 | 6 | 2.6 |
| 6 | 5 | 11 | 4.8 |
| 7 | 5 | 16 | 7.0 |

**Step 3, inverse LUT:** for each s, pick the z whose G(z) is closest (this is the slide's "inverse value" column).

| s | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| closest G | 0.0 | 0.0 | 2.6 | 2.6 | 4.8 | 4.8 | 7.0 | 7.0 |
| G⁻¹(s) | 0 | 0 | 5 | 5 | 6 | 6 | 7 | 7 |

**Step 4, chain them:** z = G⁻¹(T(r)).

| r | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| s = T(r) | 0 | 1 | 2 | 5 | 7 |
| z | **0** | **0** | **5** | **6** | **7** |

Output:

```
7 7 6 6
7 7 6 6
7 0 5 6
0 0 5 6
```

Output histogram: n(0)=3, n(5)=2, n(6)=6, n(7)=5. The bright end (5-7) matches the target 6/5/5 roughly, but the 3 darkest pixels cannot be moved up.

*Trap:* use the **closest** G(z), as the slide does. Picking "the first z with G(z) ≥ s" would send s = 1 to 5 instead of 0. State which rule you use.
</details>

---

## Part C: neighbours, paths and distances

### Problem 15: Neighbours and distances (L7 S21, S31-33) [slide]

(a) List N4, ND, N8 of p = (3, 5).
(b) The professor's example: p = (0, 0), q = (4, 4). Find D_E, D4, D8.
(c) p = (2, 3), q = (7, 5). Find D_E, D4, D8.
(d) How many pixels have D4 ≤ 2 from a centre pixel? How many have D8 ≤ 2?

<details><summary>Solution</summary>

(a) N4 = {(4,5), (2,5), (3,6), (3,4)}. ND = {(4,6), (4,4), (2,6), (2,4)}. N8 = all 8 of them.

(b) and (c), with dx = |x − s|, dy = |y − t|:

| Pair | dx, dy | D_E = √(dx² + dy²) | D4 = dx + dy | D8 = max |
|---|---|---|---|---|
| (0,0)-(4,4) | 4, 4 | √32 = **5.66** | **8** | **4** |
| (2,3)-(7,5) | 5, 2 | √29 = **5.39** | **7** | **5** |

(d) D4 ≤ r is a diamond with 2r² + 2r + 1 pixels; for r = 2 that is **13**. D8 ≤ r is a (2r + 1) × (2r + 1) square: **25**.

Always **D8 ≤ D_E ≤ D4**.

*Trap:* the speaker notes write 5.65 for √32. The correct value is 5.657 → 5.66. Write √32 to be safe.
</details>

### Problem 16: m-distance (L7 S34) [slide]

V = {1}. Find the m-distance between p (bottom-left) and p4 (top-right) for each arrangement (blank = 0):

```
layout          case 1      case 2      case 3
.  p3 p4        .  0  1     .  1  1     .  1  1
p1 p2 .         0  1  .     0  1  .     1  1  .
p  .  .         1  .  .     1  .  .     1  .  .
```

<details><summary>Solution</summary>

A diagonal step p → q is allowed under m only if the two 4-neighbours they share are both **not** in V.

| Case | Diagonal p→p2 OK? (shared: p1, (2,1)) | Diagonal p2→p4 OK? (shared: p3, (1,2)) | Shortest m-path | D_m |
|---|---|---|---|---|
| 1 (p1=0, p3=0) | yes | yes | p, p2, p4 | **2** |
| 2 (p1=0, p3=1) | yes | **no** (p3 = 1) | p, p2, p3, p4 | **3** |
| 3 (p1=1, p3=1) | **no** (p1 = 1) | no | p, p1, p2, p3, p4 | **4** |

**D = 2, 3, 4** (as on the slide). D8 would be 2 in all three cases; D4 and D8 don't depend on pixel values, D_m does.

*Trap:* path length n counts **steps**, not pixels. p, p2, p4 is 3 pixels but length 2.
</details>

### Problem 17: Shortest 4-, 8- and m-paths (Gonzalez Prob. 2.15)

p is the bottom-left pixel (3, 0) and q is the top-right pixel (0, 3):

```
       c0 c1 c2 c3
r0      3  1  2  1   <- q
r1      2  2  0  2
r2      1  2  1  1
r3 p->  1  0  1  2
```

Find the shortest 4-, 8- and m-path lengths for (a) V = {0, 1} and (b) V = {1, 2}.

<details><summary>Solution</summary>

**(a) V = {0, 1}.** Mark the allowed pixels (V = 1/0 values):

```
.  1  .  1
.  .  0  .
1  .  1  1
1  0  1  .
```

| Type | Path | Length |
|---|---|---|
| 4 | From p you reach (2,0), (3,1), (3,2), (2,2), (1,2), (2,3), but every 4-neighbour of q is 2 | **no 4-path** |
| 8 | (3,0) → (3,1) → (2,2) → (1,2) → (0,3) | **4** |
| m | (3,0) → (3,1) → (3,2) → (2,2) → (1,2) → (0,3) | **5** |

The 8-step (3,1) → (2,2) is diagonal, but the shared 4-neighbour (3,2) = 1 is in V, so m forbids it and goes round. The last step (1,2) → (0,3) is fine under m because its shared neighbours (0,2) = 2 and (1,3) = 2 are not in V.

**(b) V = {1, 2}:**

| Type | Path | Length |
|---|---|---|
| 4 | (3,0) → (2,0) → (1,0) → (1,1) → (0,1) → (0,2) → (0,3) | **6** |
| 8 | (3,0) → (2,0) → (1,1) → (0,2) → (0,3) | **4** |
| m | same as the 4-path | **6** |

Final: **(a) D4: none, D8 = 4, Dm = 5. (b) D4 = 6, D8 = 4, Dm = 6.**

*Trap:* "no path exists" is a valid answer. Also, the m-path is never shorter than the 8-path and never longer than the 4-path.
</details>

### Problem 18: 8-adjacency ambiguity (L6 S35) [slide]

V = {1}:

```
0 1 1
0 1 0
0 0 1
```

How many 8-paths are there from the centre (1,1) to the top-right pixel (0,2)? How many m-paths? Is (2,2) m-adjacent to (1,1)?

<details><summary>Solution</summary>

| Adjacency | Paths centre → (0,2) | Count |
|---|---|---|
| 8 | direct diagonal (1,1) → (0,2); and (1,1) → (0,1) → (0,2) | **2** (ambiguous) |
| m | diagonal forbidden, because the shared 4-neighbour (0,1) = 1 ∈ V; only (1,1) → (0,1) → (0,2) | **1** |

(2,2) and (1,1) are diagonal neighbours. Their shared 4-neighbours (1,2) = 0 and (2,1) = 0 are not in V, so **yes, they are m-adjacent**.

**8: 2 paths, m: 1 path, (2,2) is m-adjacent.**

*Trap:* m-adjacency does not ban all diagonals, only the ones that duplicate an existing 4-connection.
</details>

---

## Part D: arithmetic, logic and colour

### Problem 19: Image arithmetic with clamping (L9 S46-53)

A = `[[100, 200, 50], [250, 10, 128]]`, B = `[[100, 100, 100], [20, 30, 128]]` (8-bit). Compute A + B, A − B, |A − B|, 1.2·A and A/1.2 (clamp to [0, 255], round).

<details><summary>Solution</summary>

| Op | Row 1 | Row 2 |
|---|---|---|
| A + B (raw) | 200, 300, 150 | 270, 40, 256 |
| **A + B (clamped)** | **200, 255, 150** | **255, 40, 255** |
| A − B (raw) | 0, 100, −50 | 230, −20, 0 |
| **A − B (clamped)** | **0, 100, 0** | **230, 0, 0** |
| **\|A − B\|** (change detection) | **0, 100, 50** | **230, 20, 0** |
| 1.2·A | 120, 240, 60 | 300 → **255**, 12, 153.6 → **154** |
| A / 1.2 | 83.3 → **83**, 166.7 → **167**, 41.7 → **42** | 208.3 → **208**, 8.3 → **8**, 106.7 → **107** |

Adding/subtracting changes **brightness**, multiplying/dividing changes **contrast** (L9 S48, S50).

*Trap:* uint8 arithmetic without clamping **wraps around**: 250 + 20 = 270 becomes 14, which is why the slides clamp.
</details>

### Problem 20: Logic operations (L9 S54-59)

Same A and B. Compute NOT A, A AND B, A OR B, A XOR B and A XOR 128 (bitwise, 8 bits). Show the binary for the pair 200 and 100.

<details><summary>Solution</summary>

200 = 11001000, 100 = 01100100:

| Op | Binary | Decimal |
|---|---|---|
| AND | 01000000 | 64 |
| OR | 11101100 | 236 |
| XOR | 10101100 | 172 |
| NOT 200 | 00110111 | 55 |

All pixels:

| Op | Row 1 | Row 2 |
|---|---|---|
| NOT A = 255 − A | **155, 55, 205** | **5, 245, 127** |
| A AND B | **100, 64, 32** | **16, 10, 128** |
| A OR B | **100, 236, 118** | **254, 30, 128** |
| A XOR B | **0, 172, 86** | **238, 20, 0** |
| A XOR 128 | **228, 72, 178** | **122, 138, 0** |

XOR gives 0 where A = B (100 ⊕ 100, 128 ⊕ 128), which is how "XOR finds all pixels of a certain value" (L9 S56). A XOR 128 flips only the MSB. Doing it twice restores A, which is why XOR is used to draw a mouse cursor.

*Trap:* NOT on an 8-bit image is 255 − p (all 8 bits flipped), not 1 − p.
</details>

### Problem 21: Colour conversions (L7 S37, S47-49, S54; Lecture7.ipynb)

(a) Convert RGB (200, 100, 50) to CMY (8-bit and normalised).
(b) Convert the same pixel to grey with the average (HSI intensity) and with 0.299R + 0.587G + 0.114B.
(c) A colour has X = 20, Y = 30, Z = 50. Find its chromaticity (x, y, z).
(d) Using the slide-49 CIE-RGB → XYZ matrix, show that R = G = B = 1 lands on the white point.

<details><summary>Solution</summary>

(a) C = 255 − R etc.: **CMY = (55, 155, 205)**. Normalised: C = 1 − 200/255 = 0.216, M = 0.608, Y = 0.804.

(b)

| Method | Calculation | Grey |
|---|---|---|
| Average I = (R+G+B)/3 | 350 / 3 | 116.7 → **117** |
| 0.299R + 0.587G + 0.114B | 59.8 + 58.7 + 5.7 | **124.2** |
| (notebook) 0.2126R + 0.7152G + 0.0722B | 42.5 + 71.5 + 3.6 | 117.6 |

(c) X + Y + Z = 100. **x = 0.2, y = 0.3, z = 0.5**.

(d) The matrix is (1/0.17697) · [[0.49, 0.31, 0.20], [0.17697, 0.81240, 0.01063], [0.00, 0.01, 0.99]]. Each row sums to 1.00 (0.49+0.31+0.20; 0.17697+0.81240+0.01063; 0+0.01+0.99), so X = Y = Z = 1/0.17697 = 5.65 and **x = y = z = 1/3** (equal-energy white). This is CIE criterion 2, "equal amounts of the primaries produce white" (L7 S45).

*Trap:* chromaticity throws away brightness: (20, 30, 50) and (40, 60, 100) have the same (x, y). CMY is subtractive, so yellow (255, 255, 0) becomes C = 0, M = 0, Y = 255.
</details>

### Problem 22: Quick L6 facts with numbers (L6 S6, S17-18; L7 S9)

(a) A background has I = 50 and the flash just becomes visible at ΔI = 5. Weber ratio? Is discrimination better here or at I = 100, ΔI = 2?
(b) A display goes from 8-bit to 4-bit. How many grey levels are lost, and what artefact appears?

<details><summary>Solution</summary>

(a) 5/50 = **0.10** vs 2/100 = **0.02**. The smaller ratio is better, so discrimination is **better at I = 100** (bright).

(b) 256 → 16 levels, so **240 levels lost**. Smooth areas show **false contouring** (banding) (L6 S30).

*Trap:* a **small** Weber ratio means **good** discrimination: a small relative change is already visible.
</details>

---

## Part E: "explain" model answers

**E1. Why do we need m-adjacency? (L7 S24, L6 S35)**
With 8-adjacency, two pixels can be joined by two paths at once: the direct
diagonal and the route through a shared 4-neighbour (see Problem 18). Paths,
boundaries and connected components then become ambiguous. m-adjacency keeps
4-neighbours, and allows a diagonal neighbour only when N4(p) ∩ N4(q) contains no
pixel from V. That removes the duplicate diagonal, so there is exactly one path
and no loss of connectivity.

**E2. Why is an equalised histogram not flat, and what does equalisation do to contrast? (L9 S20, S26)**
The derivation p_s(s) = p_r(r)·|dr/ds| = 1 gives a uniform histogram only for
continuous intensities. With discrete levels, every pixel of one input level
maps to a single output level, so bins can only move or **merge**, never split.
The result is spread out but not flat. Contrast is **stretched** near histogram
peaks (many pixels → large steps in s) and **compressed** near valleys. T(r) must be
single-valued and monotonically increasing so grey-level order is kept.

**E3. What is gamma correction and why is it needed? (L6 S47-48)**
s = (L−1)(r/(L−1))^γ. Cameras record light linearly, but displays and the eye
respond along a power curve, so uncorrected images look bleached or too dark on
different monitors. γ < 1 (e.g. 0.45) lifts dark tones and brightens; γ > 1 (e.g.
2.2) darkens. 0.45 ≈ 1/2.2, so the two cancel. Endpoints 0 and L−1 never move.

**E4. Sampling vs quantization, and what goes wrong when each is too low? (L6 S24-31)**
Sampling digitises the **coordinates** (how many pixels, M × N). Too few
pixels gives a blocky, checkerboard image (low spatial resolution). Quantization digitises
the **amplitude** (how many grey levels, L = 2^k). Too few levels gives **false
contouring**. Isopreference curves show that images with more detail tolerate
fewer grey levels. Storage grows as M · N · k bits.

**E5. Radiance vs luminance vs brightness (L7 S13-15)**
Radiance is the total energy flowing from the source (W). Luminance is the energy
an observer **perceives** (lumens, lm); it is weighted by the eye. Brightness is a
subjective impression that is practically impossible to measure. Radiometry
covers the whole optical spectrum; photometry covers only the visible part weighted
by the eye's response.

---

## The three problem types most likely on the exam

1. **Histogram equalisation table** (Problems 11-13): n_k → p_k → cumulative → (L−1)·CDF → round → output image.
2. **Distances and paths** (Problems 15-17): D_E/D4/D8 between two points, and shortest 4/8/m path for a given V.
3. **Point transform on a small array** (Problems 4-10, 19-20): LUT, negative, threshold, contrast stretch, gamma, clamped arithmetic, bitwise logic.
