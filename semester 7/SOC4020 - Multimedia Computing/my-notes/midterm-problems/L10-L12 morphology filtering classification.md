# Midterm practice: L10 + L11 + L12 (morphology, spatial filtering, classification)

Morphology (L10), spatial filtering and edge detection (L11), pattern
classification (L12). Every number below was checked in Python (numpy/scipy).

Attempt each problem before opening the solution. Problems marked **(deck)**
copy the professor's own figure or worked example; the others are built in
the same style with arrays small enough to do by hand.

Conventions used throughout (state them on the exam too, it costs one line):

- Binary images: **1 = object (white), 0 = background**. Pixels outside the image count as **0**.
- Structuring element (SE) and masks are 3×3 with the **origin at the centre**.
- Rows and columns are counted from 0 at the top-left. `(r, c)` = (row, column).
- "Apply the mask" = slide 14's recipe: lay the mask on the pixel, multiply
  overlapping entries, add. That is **correlation**. True convolution rotates
  the mask 180° first. They differ only for non-symmetric masks (Problem 9).

---

## Formula and procedure sheet

### L10: morphology

| What | Formula | In words / by hand | Source |
|---|---|---|---|
| Reflection | B̂ = { w : w = −b, b ∈ B } | rotate the SE 180° about its origin | L10 S8 |
| Dilation | **A ⊕ B = { z : (B̂)_z ∩ A ≠ ∅ }** | output 1 if the (reflected) SE **hits** at least one 1. Grey: local **max** | L10 S12-13, S20 |
| Erosion | **A ⊖ B = { z : (B)_z ⊆ A }** | output 1 only if the SE **fits**: every 1 of the SE lands on a 1. Grey: local **min** | L10 S18, S23 |
| Opening | **A ∘ B = (A ⊖ B) ⊕ B** | erode then dilate. Removes small bright specks, thin protrusions, breaks narrow isthmuses | L10 S26, S29 |
| Closing | **A • B = (A ⊕ B) ⊖ B** | dilate then erode. Fills small holes, fuses narrow breaks and long thin gulfs | L10 S28-29 |
| Opening properties | A∘B ⊆ A; C ⊆ D ⇒ C∘B ⊆ D∘B; (A∘B)∘B = A∘B | anti-extensive, increasing, idempotent | L10 S34 |
| Closing properties | A ⊆ A•B; C ⊆ D ⇒ C•B ⊆ D•B; (A•B)•B = A•B | extensive, increasing, idempotent | L10 S34 |
| Hit-or-miss | **A ⊛ B = (A ⊖ X) ∩ [Aᶜ ⊖ (W − X)]** | X must fit the object AND the local background W−X must fit the background | L10 S36-37 |
| Boundary | **β(A) = A − (A ⊖ B)** | object minus its eroded self (3×3 square SE) | L10 S38-39 |
| Region filling | **X_k = (X_{k−1} ⊕ B) ∩ Aᶜ**, X₀ = p; stop when X_k = X_{k−1}; answer **X_k ∪ A** | B = 3×3 **cross**; p is a seed inside the hole | L10 S40-42 |
| Connected components | **X_k = (X_{k−1} ⊕ B) ∩ A** | same loop, intersect with A instead of Aᶜ; B = 3×3 square | L10 S43-44 |
| Morph. gradient | (A ⊕ B) − (A ⊖ B) | dilation minus erosion → edges | L10 S55 |
| White / black top-hat | A − (A∘B) / (A•B) − A | small bright details / small dark details | L10 S56 |
| Size rule (square SE, side s) | dilation adds s/2 on every side (+s per dimension); erosion removes s/2 (−s per dimension) | d×d square, d/4 SE: dilation → 5d/4, erosion → 3d/4 | L10 S21, S24 |

### L11: spatial filtering and edges

| What | Formula / mask | Notes | Source |
|---|---|---|---|
| Discrete convolution | y(m,n) = Σ Σ h(m−m′, n−n′) x(m′,n′) | flip the mask; correlation does not flip | L11 S11 |
| Border handling | zero-pad; skip borders (start at (1,1)); duplicate edges; wrap around | output shrinks if you skip borders | L11 S15 |
| Box (average) blur | all 1/9 (3×3), all 1/25 (5×5) | bigger mask = more blur | L11 S16 |
| Gaussian (weighted) | ¹⁄₁₆ [1 2 1; 2 4 2; 1 2 1] | σ controls spread | L11 S19 |
| Sharpening masks | [0 −1 0; −1 5 −1; 0 −1 0], [−1 −1 −1; −1 9 −1; −1 −1 −1] | weights sum to **1** → flat areas unchanged | L11 S20 |
| High-pass | ¹⁄₉ [−1 −1 −1; −1 8 −1; −1 −1 −1] | weights sum to **0** → flat areas → 0 | L11 S21 |
| Unsharp masking | **original − lowpass** | = high-pass | L11 S21 |
| High-boost | **A·original − lowpass**; mask centre **(9A−1)/9**, others −1/9 | A = 1 → high-pass; A > 1 keeps background, image gets lighter | L11 S21, S24 |
| Point detection | R = Σ wᵢzᵢ with [−1 −1 −1; −1 8 −1; −1 −1 −1]; point if **\|R\| > T** | | L11 S27-28 |
| Line masks | horizontal [−1 −1 −1; 2 2 2; −1 −1 −1], vertical, ±45° (the 2s along the line) | largest response wins | L11 S28 |
| Homogeneity operator | max \|centre − each of 8 neighbours\| | 8 subtractions | L11 S33-34 |
| Difference operator | max of 4 \|opposite-pair differences\| | 4 subtractions, faster | L11 S33-34 |
| Roberts (deck) | [0 0 −1; 0 1 0; 0 0 0], [−1 0 0; 0 1 0; 0 0 0] | smallest support, most noise-prone | L11 S37-38 |
| Prewitt | [1 0 −1]×3 rows, and [−1 −1 −1; 0 0 0; 1 1 1] | "more sensitive to horizontal/vertical edges" | L11 S37-38 |
| Sobel | [1 0 −1; 2 0 −2; 1 0 −1], [−1 −2 −1; 0 0 0; 1 2 1] | "more sensitive to diagonal edges"; thick edges, noisy | L11 S37, S43-44 |
| Frei-Chen | Sobel with √2 instead of 2 | | L11 S37 |
| Gradient magnitude | **√(Gx² + Gy²)** or **\|Gx\| + \|Gy\|** | | L11 S37 |
| Gradient direction | **θ = tan⁻¹(Hc / Hr)** | ratio of the two mask responses | L11 S37 |
| Laplacian | [0 −1 0; −1 4 −1; 0 −1 0] or [−1 −1 −1; −1 8 −1; −1 −1 −1] | sums to 0; edges = **zero crossings**; noisy, double edges, no direction | L11 S45 |
| Laplacian sharpening | **g = f + (deck Laplacian response)** = the 5-centre / 9-centre masks | because the deck's Laplacian has a **positive** centre | L11 S20, S45 |
| LoG / DoG | DoG ≈ LoG when σ₂/σ₁ ≈ 1.6 (σ₁ = 1.0, σ₂ = 1.6 on the slide) | bigger mask (9×9 vs 7×7) → wider edges | L11 S48-49 |
| Median | sort the window, take the middle (5th of 9) | best for salt-and-pepper, keeps edges | L11 S53-57 |
| Vector (colour) median | pick the xᵢ with the smallest Σⱼ ‖xᵢ − xⱼ‖ (L1 over R, G, B) | per-channel median breaks colour correlation | L11 S58-59 |
| Min / max filter | min removes **white** (salt) spikes, darkens; max removes **black** (pepper) spikes, brightens | each fails on mixed noise; cascade them | L11 S60 |

### L12: pattern classification

| What | Formula | Notes | Source |
|---|---|---|---|
| Feature vector | **x = [x₁, …, xₙ]ᵀ** | e.g. fish: (lightness, width); characters: [#holes, #strokes, …] | L12 S12, S32 |
| Nearest class mean | assign x to the class with the smallest **‖x − m_j‖**; reject if still too far | Euclidean distance | L12 S38 |
| Equivalent decision function | **d_j(x) = xᵀm_j − ½ m_jᵀm_j**; pick the **largest** d_j | (Gonzalez 12.2) same answer as smallest distance | Gonzalez ch.12 |
| Boundary between i and j | **d_ij(x) = d_i(x) − d_j(x) = (m_i − m_j)ᵀx − ½(m_iᵀm_i − m_jᵀm_j) = 0** | perpendicular bisector of the segment m_i m_j | Gonzalez ch.12 |
| Scaled Euclidean | **‖x − x_c‖ = √Σᵢ ((x[i] − x_c[i]) / σᵢ)²** | divide each axis by that class's σ | L12 S40 |
| Nearest neighbour / k-NN | keep all training samples; class of the nearest one / majority of the k nearest | odd k avoids 2-class ties | L12 S41 |
| Bayes rule | **P(ωᵢ\|x) = p(x\|ωᵢ)P(ωᵢ) / Σⱼ p(x\|ωⱼ)P(ωⱼ)** | class-conditional × prior / evidence; pick the largest posterior | L12 S42 |
| Error rate | wrong / total; accuracy = 1 − error rate | "Evaluation" step of the design cycle | L12 S26 |

### Where the deck is loose (and what to write)

- **L11 S60 swaps opening and closing** ("closing filter: min → max, opening filter: max → min").
  L10 and Gonzalez: **opening = min (erosion) then max (dilation)**, closing = max then min. If an MCQ
  quotes S60 word for word, the deck's own wording may be the "expected" answer; in a written answer,
  use the L10 definition and add one line noting the slide.
- **L11 S8 lists Canny under "second-order, Gaussian-based".** Canny uses the first derivative of a
  Gaussian-smoothed image. An MCQ copied from S8 may still expect "Gaussian-based: Canny, LoG".
- **L11 S14 calls the multiply-and-add recipe "convolution"** but does not flip the mask. That is
  correlation. Same result for symmetric masks (box, Gaussian, Laplacian); different for Sobel/Prewitt
  (sign flips) and any lopsided mask.
- **L11 S20, third sharpening mask** prints as [1 −2 1; −1 5 −2; 1 −2 1], whose weights sum to 2. The
  intended mask is [1 −2 1; −2 5 −2; 1 −2 1] (sum 1).
- **L11 S49 writes σ₁/σ₂ = 1.6** with σ₁ = 1.0, σ₂ = 1.6. The ratio is really σ₂/σ₁ = 1.6.
- **L10 S12 says dilation is "convoluting"** the image with a kernel. It is a max, not a weighted sum.
- **L12 S42: "use Bayes rule if all classes are disjoint"** means mutually exclusive and exhaustive.
- **L12 S14-16 "issue of generalization"** = overfitting. Expect either word.

---

## Part A: L10 morphology

### Problem 1: Erosion and dilation with a cross SE (10 pts)

Image A (7×7) and the 3×3 cross SE B (origin = centre):

```
A                    B
0 0 0 0 0 0 0        0 1 0
0 1 1 1 0 0 0        1 1 1
0 1 1 1 1 0 0        0 1 0
0 1 1 1 1 0 0
0 0 1 1 1 0 0
0 0 0 0 0 1 0
0 0 0 0 0 0 0
```

(a) Compute A ⊖ B. (b) Compute A ⊕ B. (c) How many 1-pixels does A, A ⊖ B and A ⊕ B have?
(d) What happens to the isolated pixel at (5,5) in each case?

<details><summary>Solution</summary>

**Erosion rule:** put the cross on each pixel; output 1 only if the centre and its 4 neighbours (up,
down, left, right) are all 1.

Check the candidates. (2,2): itself 1, up (1,2)=1, down (3,2)=1, left (2,1)=1, right (2,3)=1 → 1.
(2,3): up (1,3)=1, down 1, left 1, right (2,4)=1 → 1. (3,2), (3,3): same → 1.
(1,2): up (0,2)=0 → 0. (2,4): right (2,5)=0 → 0. (4,3): down (5,3)=0 → 0. Everything else fails.

```
A ⊖ B
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 1 1 0 0 0
0 0 1 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Dilation rule:** output 1 if the cross centred there touches any 1 (the cross is symmetric, so
B̂ = B). Equivalently: every 1 of A "stamps" a cross.

```
A ⊕ B
0 1 1 1 0 0 0
1 1 1 1 1 0 0
1 1 1 1 1 1 0
1 1 1 1 1 1 0
0 1 1 1 1 1 0
0 0 1 1 1 1 1
0 0 0 0 0 1 0
```

**(c) |A| = 15, |A ⊖ B| = 4, |A ⊕ B| = 31.**

(d) The isolated pixel **disappears under erosion** (its neighbours are 0) and **grows into a cross
under dilation**, where it merges with the dilated blob at (4,4)/(5,4).

Trap: corners of the 3×3 cross are 0, so diagonal neighbours do not matter. With a 3×3 **square** SE
the erosion keeps only (2,2) and (3,3), a different answer.
</details>

### Problem 2: Opening removes specks and protrusions (10 pts)

A (6×9), B = 3×3 square of 1s.

```
0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0
0 1 1 1 1 1 1 1 0
0 1 1 1 1 0 0 0 0
0 1 1 1 1 0 0 1 0
0 0 0 0 0 0 0 0 0
```

(a) Compute A ⊖ B. (b) Compute A ∘ B. (c) What did the opening remove? (d) Compute the white top-hat
A − (A ∘ B).

<details><summary>Solution</summary>

(a) Erosion with a 3×3 square: a pixel survives only if its whole 3×3 neighbourhood is 1. Inside the
4×4 block (rows 1-4, cols 1-4) only the 2×2 core (rows 2-3, cols 2-3) qualifies. The protrusion is one
pixel thick and the speck is one pixel, so they vanish.

```
A ⊖ B
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0
0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

(b) Dilate that 2×2 core by the 3×3 square: it grows by 1 on every side and gives back the 4×4 block.

```
A ∘ B
0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0
0 1 1 1 1 0 0 0 0
0 1 1 1 1 0 0 0 0
0 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0
```

(c) **The thin protrusion (2,5)-(2,7) and the isolated speck (4,7) are removed; the 4×4 block is
restored exactly.** 20 pixels → 16 pixels, and A ∘ B ⊆ A (anti-extensive).

(d)
```
A − (A ∘ B)
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0
```

Trap: opening is **not** "erosion undone". Anything the erosion deleted completely never comes back.
</details>

### Problem 3: Closing fills a hole and a gulf (10 pts)

C (6×8), B = 3×3 square.

```
0 0 0 0 0 0 0 0
0 1 1 1 0 1 1 0
0 1 0 1 0 1 1 0
0 1 1 1 0 1 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```

(a) Compute C ⊕ B. (b) Compute C • B. (c) Compute the black top-hat (C • B) − C. (d) What would
opening with the same B do to this image?

<details><summary>Solution</summary>

(a) Every 1 stamps a 3×3 square. The object spans rows 1-4, cols 1-6, so the dilation covers rows 0-5,
cols 0-7: **the whole 6×8 image becomes 1.**

(b) Erode that all-ones image (outside = 0). A pixel survives if its 3×3 neighbourhood is inside the
image, i.e. rows 1-4, cols 1-6.

```
C • B
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```

(c) Pixels added by closing:
```
(C • B) − C
0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0
0 0 1 0 1 0 0 0
0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
**The 1-pixel hole at (2,2) is filled and the 1-pixel-wide gulf in column 4 is fused.** C ⊆ C • B
(extensive).

(d) No 3×3 square fits anywhere in C (the hole and the gulf break every 3×3 window), so the erosion is
empty and **the opening deletes the whole object**.

Trap: closing = dilate **first**. Getting the order backwards turns this into (d).
</details>

### Problem 4 (deck): Boundary extraction, Gonzalez Fig. 9.13 (10 pts)

A (5×10), B = 3×3 square, pixels outside A count as background.

```
A
1 1 1 0 1 1 1 1 1 0
1 1 1 0 1 1 1 1 1 0
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
```

Compute A ⊖ B and β(A) = A − (A ⊖ B).

<details><summary>Solution</summary>

Erosion keeps a pixel only if all 9 pixels of its 3×3 window are 1. The whole outer frame (row 0, row
4, col 0, col 9) fails because part of its window lies outside. Pixels next to the two notches
(column 3, rows 0-1, and column 9, rows 0-1) also fail.

```
A ⊖ B
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 1 1 1 0 0
0 1 0 0 0 1 1 1 0 0
0 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0
```

Subtract from A:

```
β(A)
1 1 1 0 1 1 1 1 1 0
1 0 1 0 1 0 0 0 1 0
1 0 1 1 1 0 0 0 1 1
1 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1
```

**The boundary has 30 pixels** and is one pixel thick (it matches the figure on L10 S38).

Trap: a 3×3 square gives an 8-connected-thick boundary of width 1; a bigger SE gives a thicker boundary.
Using a cross gives a thinner, 4-connected-style boundary.
</details>

### Problem 5 (deck): Region filling, Gonzalez Fig. 9.15 (10 pts)

A is the 10×7 outline below, B is the 3×3 cross, the seed is p = (2,2).

```
A
0 0 0 0 0 0 0
0 0 1 1 0 0 0
0 1 0 0 1 0 0
0 1 0 0 1 0 0
0 0 1 0 1 0 0
0 0 1 0 1 0 0
0 1 0 0 0 1 0
0 1 0 0 0 1 0
0 1 1 1 1 0 0
0 0 0 0 0 0 0
```

Use X_k = (X_{k−1} ⊕ B) ∩ Aᶜ. Give X₁, X₂, X₃, the iteration at which it converges, and the filled
region X_k ∪ A.

<details><summary>Solution</summary>

Each step: grow the current set by one pixel up/down/left/right, then delete anything that lands on
the boundary A (∩ Aᶜ).

```
X0 = p     X1         X2         X3          (only rows 2-4, cols 1-4 shown; the rest is 0)
. 1 . .    . 1 1 .    . 1 1 .    . 1 1 .     row 2
. . . .    . 1 . .    . 1 1 .    . 1 1 .     row 3
. . . .    . . . .    . . . .    . . 1 .     row 4
```

X₁: the seed (2,2) grows to (1,2), (3,2), (2,1), (2,3); (1,2) and (2,1) are on A, so they are removed.

In full, X₃ = {(2,2),(2,3),(3,2),(3,3),(4,3)}. It keeps flowing down the 1-pixel channel at column 3,
then spreads into rows 6-7. **X₇ is final (X₈ = X₇)**:

```
X7                 X7 ∪ A
0 0 0 0 0 0 0      0 0 0 0 0 0 0
0 0 0 0 0 0 0      0 0 1 1 0 0 0
0 0 1 1 0 0 0      0 1 1 1 1 0 0
0 0 1 1 0 0 0      0 1 1 1 1 0 0
0 0 0 1 0 0 0      0 0 1 1 1 0 0
0 0 0 1 0 0 0      0 0 1 1 1 0 0
0 0 1 1 1 0 0      0 1 1 1 1 1 0
0 0 1 1 1 0 0      0 1 1 1 1 1 0
0 0 0 0 0 0 0      0 1 1 1 1 0 0
0 0 0 0 0 0 0      0 0 0 0 0 0 0
```

Trap: B must be the **cross**. A 3×3 square would leak through the diagonal gaps in the 8-connected
boundary (e.g. between (1,3) and (2,4)) and flood the background.
</details>

### Problem 6 (deck): Size rules, Gonzalez Figs. 9.4, 9.6, 9.7 (10 pts)

A is a d × d square.

(a) B is a d/4 × d/4 square (origin at centre). Give the size of A ⊕ B and A ⊖ B.
(b) B is d/4 wide and d tall. Give the size of A ⊕ B and A ⊖ B.
(c) An image holds squares of side 1, 3, 5, 7, 9 and 15. It is eroded with a 13×13 square of 1s and
then dilated with the same SE. What is left after each step?

<details><summary>Solution</summary>

Rule: with a centred SE of width w, dilation adds w/2 on each side (+w total); erosion removes w/2
on each side (−w total). Same for height.

(a) w = h = d/4. **Dilation: (d + d/4) = 5d/4 square (d/8 added on each side). Erosion: 3d/4 square.**

(b) Width d/4, height d. **Dilation: 5d/4 wide × 2d tall** (d/2 added top and bottom).
**Erosion: 3d/4 wide × 0 tall, i.e. a horizontal line segment of length 3d/4** through the centre.

(c) Erosion by 13×13 kills every square smaller than 13. **Only the 15×15 squares survive, each
shrunk to 3×3** (15 − 12 = 3). Dilating with 13×13 grows each 3×3 back to **15×15**. The net effect is
an opening that **keeps only the large squares**.

Trap: the change per side is half the SE size, not the full SE size.
</details>

### Problem 7: Hit-or-miss, finding isolated points (10 pts)

Find every isolated single pixel in A with the hit-or-miss transform A ⊛ B = (A ⊖ X) ∩ [Aᶜ ⊖ (W − X)],
where X = the single centre pixel and W − X = its 8-neighbour ring.

```
A                 X        W − X
0 0 0 0 0 0       0 0 0    1 1 1
0 1 0 0 0 0       0 1 0    1 0 1
0 0 0 1 1 0       0 0 0    1 1 1
0 0 0 1 1 0
0 1 0 0 0 0
0 0 0 0 0 0
```

<details><summary>Solution</summary>

**A ⊖ X** = A itself (X is one pixel at the origin), so every 1 is a candidate: (1,1), (2,3), (2,4),
(3,3), (3,4), (4,1).

**Aᶜ ⊖ (W − X)**: a pixel survives if all 8 neighbours are background. True for (1,1) and (4,1);
false for each pixel of the 2×2 block (they have 1-neighbours). (Background pixels can also pass,
but the intersection removes them since they fail A ⊖ X.)

Intersection: **A ⊛ B = {(1,1), (4,1)}**, the two isolated pixels; the 2×2 block is rejected.

Trap: erosion alone (A ⊖ X) cannot tell an isolated pixel from part of a blob; the second term
checks the **background** around it. That is the whole point of hit-or-miss.
</details>

### Problem 8: Grey-scale morphology on a 1-D signal (10 pts)

f = [3, 3, 9, 3, 3, 7, 7, 7, 1, 1], flat SE of length 3 (centred). At the ends, use only the
samples that exist.

Compute the dilation, erosion, morphological gradient, opening, closing, white top-hat f − (f∘B) and
black top-hat (f•B) − f.

<details><summary>Solution</summary>

Dilation = max of each 3-window, erosion = min.

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| f | 3 | 3 | 9 | 3 | 3 | 7 | 7 | 7 | 1 | 1 |
| f ⊕ B (max) | 3 | 9 | 9 | 9 | 7 | 7 | 7 | 7 | 7 | 1 |
| f ⊖ B (min) | 3 | 3 | 3 | 3 | 3 | 3 | 7 | 1 | 1 | 1 |
| gradient (max − min) | 0 | 6 | 6 | 6 | 4 | 4 | 0 | 6 | 6 | 0 |
| opening = max of the min row | 3 | 3 | 3 | 3 | 3 | 7 | 7 | 7 | 1 | 1 |
| closing = min of the max row | 3 | 3 | 9 | 7 | 7 | 7 | 7 | 7 | 1 | 1 |
| white top-hat f − open | 0 | 0 | **6** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| black top-hat close − f | 0 | 0 | 0 | **4** | **4** | 0 | 0 | 0 | 0 | 0 |

**Opening cuts off the narrow bright spike (9 → 3); the white top-hat isolates it (height 6).
Closing fills the narrow dark valley between 9 and 7 (3,3 → 7,7); the black top-hat isolates it (depth
4).** The 3-wide plateau of 7s is untouched by both.

Trap: opening is a min followed by a max (L10), not "max → min" as L11 S60 prints.
</details>

---

## Part B: L11 spatial filtering and edges

### Problem 9 (deck): Mean, Gaussian, median, min, max on one window (10 pts)

The median example from L11 S55: the 3×3 window

```
13  4  8
 2  9  6
 7 25 16
```

Give the output at the centre for (a) the 3×3 box filter, (b) the Gaussian mask ¹⁄₁₆[1 2 1; 2 4 2; 1 2 1],
(c) the median, (d) min and max filters.

<details><summary>Solution</summary>

(a) Sum = 13+4+8+2+9+6+7+25+16 = 90. **Mean = 90/9 = 10.**

(b) Corners ×1: 13+8+7+16 = 44. Edges ×2: (4+2+6+25)·2 = 74. Centre ×4: 36.
Total 154 / 16 = **9.625**.

(c) Sorted: 2, 4, 6, 7, **8**, 9, 13, 16, 25. **Median = 8** (5th of 9), exactly as on the slide.

(d) **Min = 2, max = 25.**

Trap: the median is the middle of the **sorted** list, not the original centre value (9).
</details>

### Problem 10: Box vs median on salt-and-pepper, zero padding (10 pts)

```
I
10  10  10  10
10 200  10  10
10  10   0  10
10  10  10  10
```

(200 is salt, 0 is pepper.) Use zero padding.

(a) Apply the 3×3 box filter at (0,0), (1,1), (1,2), (2,1), (2,2).
(b) Apply the 3×3 median filter to the whole image.
(c) Repeat the median at (0,0) with edge duplication instead.

<details><summary>Solution</summary>

(a) Window sums:
- (0,0): 5 padding zeros + 10, 10, 10, 200 = 230 → **25.56**
- (1,1): 7 tens + 200 + 0 = 270 → **30**
- (1,2), (2,1), (2,2): each window again contains 200, 0 and seven 10s = 270 → **30**

The salt spike is smeared over its whole neighbourhood (10 → 30), and the corners are darkened or
brightened by the padding.

(b) Median, zero padding:
- Corner (0,0): {0,0,0,0,0,10,10,10,200} → 0. Same for every corner.
- Edge (0,1): {0,0,0,10,10,10,10,10,200} → 10.
- Interior: e.g. (1,1): {0,10,10,10,10,10,10,10,200} → 10.

```
median (zero pad)
 0 10 10  0
10 10 10 10
10 10 10 10
 0 10 10  0
```

**Both impulses are gone**, but the four corners turn black because 5 of their 9 values are padding.

(c) With duplicated edges the corner window is {10,10,10,10,10,10,10,10,200} → **10**. Duplication
gives an all-10 output.

Trap: the box filter "removes" noise only by spreading it; the median deletes it. Zero padding biases
corner and edge results (mean toward 0, median to 0 at corners).
</details>

### Problem 11: Correlation vs convolution with a non-symmetric mask (10 pts)

```
I                  w
1 2 3 0            1 2  0
4 5 6 1            0 1  0
7 8 9 2            0 0 −1
0 1 2 3
```

(a) Compute the correlation output at the four interior pixels (1,1), (1,2), (2,1), (2,2).
(b) Compute the convolution output at the same pixels.
(c) What do correlation and convolution give for a unit impulse with w = [1 2 3; 4 5 6; 7 8 9]?

<details><summary>Solution</summary>

(a) **Correlation:** overlay w directly.

(1,1): window [1 2 3; 4 5 6; 7 8 9] → 1·1 + 2·2 + 5·1 + 9·(−1) = 1 + 4 + 5 − 9 = **1**
(1,2): window [2 3 0; 5 6 1; 8 9 2] → 2 + 6 + 6 − 2 = **12**
(2,1): window [4 5 6; 7 8 9; 0 1 2] → 4 + 10 + 8 − 2 = **20**
(2,2): window [5 6 1; 8 9 2; 1 2 3] → 5 + 12 + 9 − 3 = **23**

(b) **Convolution:** rotate w by 180° first: w_rot = [−1 0 0; 0 1 0; 0 2 1].

(1,1): −1·1 + 5 + 2·8 + 9 = **29**
(1,2): −2 + 6 + 18 + 2 = **24**
(2,1): −4 + 8 + 2 + 2 = **8**
(2,2): −5 + 9 + 4 + 3 = **11**

```
correlation   convolution
  1 12          29 24
 20 23           8 11
```

(c) Correlating an impulse gives **w rotated 180°** ([9 8 7; 6 5 4; 3 2 1]); convolving an impulse
gives **w itself** ([1 2 3; 4 5 6; 7 8 9]). That is why convolution is defined with the flip.

Trap: slide 14's "multiply and add" is correlation. For box, Gaussian and Laplacian masks (symmetric)
both give the same answer, so nobody notices until a lopsided mask appears.
</details>

### Problem 12 (deck): 1-D convolution of two rectangles, L11 S13 (10 pts)

f(x) = 1 on [0, 1], g(x) = ½ on [0, 1], both 0 elsewhere. Find f ∗ g. Then compute the discrete
convolution of f = [0, 1, 2, 3, 2, 1, 0] with w = [1, 2, 3] (full length).

<details><summary>Solution</summary>

Flip g, slide it by x, integrate the overlap (shaded area on the slide):
- 0 ≤ x ≤ 1: overlap length x, height 1·½ → **x/2**
- 1 ≤ x ≤ 2: overlap length 2 − x → (2 − x)/2 = **1 − x/2**
- elsewhere **0**

**A triangle from 0 to 2 with peak ½ at x = 1.**

Discrete: (f ∗ w)[n] = Σ f[k] w[n − k]. Full output (length 7 + 3 − 1 = 9):

**[0, 1, 4, 10, 14, 14, 8, 3, 0]**

(e.g. n = 3: f[1]w[2] + f[2]w[1] + f[3]w[0] = 1·3 + 2·2 + 3·1 = 10.)

Trap: full convolution length is N + M − 1. Two boxes convolve to a triangle, not a box.
</details>

### Problem 13: Laplacian and sharpening (10 pts)

```
p (centre = 30)
10 10 40
10 30 40
10 20 40
```

(a) Laplacian response with the 4-neighbour mask [0 −1 0; −1 4 −1; 0 −1 0] and the 8-neighbour mask.
(b) Output of the two sharpening masks [0 −1 0; −1 5 −1; 0 −1 0] and [−1 −1 −1; −1 9 −1; −1 −1 −1].
(c) For a flat 3×3 patch of 50s with centre 80 (an isolated bright point), give the 4- and
8-neighbour Laplacian.

<details><summary>Solution</summary>

(a) L4 = 4·30 − (10 + 10 + 40 + 20) = 120 − 80 = **40**.
L8 = 8·30 − (10+10+40+10+40+10+20+40) = 240 − 180 = **60**.

(b) The sharpening masks are "identity + Laplacian" (centre 4+1 = 5, 8+1 = 9):
**[0 −1 0; −1 5 −1; 0 −1 0] → 30 + 40 = 70. [−1 −1 −1; −1 9 −1; −1 −1 −1] → 30 + 60 = 90.**

(c) L4 = 4·80 − 4·50 = **120**; L8 = 8·80 − 8·50 = **240**. Sharpened: 200 and 320, so the point
is boosted strongly.

Trap: with the deck's positive-centre Laplacian you **add** it to sharpen. Gonzalez's book uses a
negative-centre Laplacian and **subtracts** it. Same final mask either way; the masks summing to 1
leave flat regions unchanged.
</details>

### Problem 14: High-pass, unsharp masking, high-boost (10 pts)

```
q (centre 40)
20 20 20
20 40 20
20 20 60
```

(a) Lowpass (3×3 mean) at the centre. (b) High-pass = original − lowpass. (c) High-boost
A·original − lowpass for A = 1.2 and A = 1.7. (d) Write the 3×3 high-boost mask for A = 1.2.

<details><summary>Solution</summary>

(a) Sum = 7·20 + 40 + 60 = 240 → lowpass **= 26.67**.

(b) HP = 40 − 26.67 = **13.33**. (Same as the mask ¹⁄₉[−1 −1 −1; −1 8 −1; −1 −1 −1]: (8·40 − 200)/9 =
120/9 = 13.33.)

(c) A = 1.2: 48 − 26.67 = **21.33**. A = 1.7: 68 − 26.67 = **41.33**.

(d) ω = 9A − 1 = 9.8, so the centre is **9.8/9 ≈ 1.089** and the other eight entries are **−1/9**.
Check: (9.8·40 − 200)/9 = 192/9 = 21.33.

Trap: A = 1 is plain high-pass (dark image, edges only). As A grows, more of the original is kept and
the image gets lighter (L11 S24).
</details>

### Problem 15: Sobel, Prewitt, Roberts at one pixel (10 pts)

```
P
20 30  60
20 40  90
30 60 100
```

Use Gx = [−1 0 1; −2 0 2; −1 0 1] (right minus left) and Gy = [−1 −2 −1; 0 0 0; 1 2 1] (bottom minus top).

(a) Sobel Gx, Gy, |Gx| + |Gy|, √(Gx² + Gy²), and the direction θ = tan⁻¹(Gy/Gx).
(b) Same with Prewitt (1s instead of 2s).
(c) The deck's Roberts masks [0 0 −1; 0 1 0; 0 0 0] and [−1 0 0; 0 1 0; 0 0 0].
(d) The deck prints the Sobel x-mask as [1 0 −1; 2 0 −2; 1 0 −1]. What changes?

<details><summary>Solution</summary>

(a) Sobel Gx = (60 + 2·90 + 100) − (20 + 2·20 + 30) = 340 − 90 = **250**.
Gy = (30 + 2·60 + 100) − (20 + 2·30 + 60) = 250 − 140 = **110**.
**|Gx| + |Gy| = 360. √(250² + 110²) = 273.1. θ = tan⁻¹(110/250) = 23.7°.**

(b) Prewitt Gx = (60 + 90 + 100) − (20 + 20 + 30) = **180**; Gy = (30 + 60 + 100) − (20 + 30 + 60) =
**80**. **|·|+|·| = 260, √ = 197.0, θ = 24.0°.**

(c) Roberts (deck): z5 − z3 = 40 − 60 = **−20**; z5 − z1 = 40 − 20 = **20**. Magnitude
√(400 + 400) = **28.3** (or 40 with the |·|+|·| form). Tiny 2-pixel support, so it sees much less of
the edge than Sobel.

(d) [1 0 −1; 2 0 −2; 1 0 −1] is left minus right, so it gives **Gx = −250**. **The magnitude is
unchanged; the direction flips by 180°.** (Convolution instead of correlation does the same thing.)

Trap: |Gx| + |Gy| is always ≥ √(Gx² + Gy²); it is the cheap approximation, not the same number.
</details>

### Problem 16 (deck): Homogeneity and difference operators, L11 S34 (10 pts)

```
window 1         window 2
11 13 15         20 22 40
16 11 11         18 25 45
16 12 11         19 21 50
```

Give the homogeneity and difference operator outputs for both.

<details><summary>Solution</summary>

**Homogeneity** = max |centre − neighbour| over the 8 neighbours.
Window 1: |11−11|, |11−13|, |11−15|, |11−16|, |11−11|, |11−16|, |11−12|, |11−11| = 0, 2, 4, 5, 0, 5,
1, 0 → **5** (slide's answer).
Window 2: |25 − 20|, …, |25 − 50| → **25**.

**Difference** = max of the 4 opposite-pair differences: |TL − BR|, |T − B|, |TR − BL|, |R − L|.
Window 1: |11−11| = 0, |13−12| = 1, |15−16| = 1, |11−16| = 5 → **5** (slide's answer).
Window 2: |20−50| = 30, |22−21| = 1, |40−19| = 21, |45−18| = 27 → **30**.

Trap: the difference operator never uses the centre pixel; 4 subtractions instead of 8 is why it is
faster.
</details>

### Problem 17: Point and line detection; first vs second derivative in 1-D (10 pts)

(a) With the point mask [−1 −1 −1; −1 8 −1; −1 −1 −1] and T = 100, decide for
[10 10 10; 10 90 10; 10 10 12] and [30 32 31; 29 30 33; 30 31 30].
(b) Which line mask (horizontal, +45°, vertical, −45°) responds most to [0 0 9; 0 9 0; 9 0 0]?
(c) For the ramp f = [10, 10, 10, 10, 20, 30, 40, 40, 40, 40] compute the first difference f[x+1] −
f[x] and the second difference f[x+1] − 2f[x] + f[x−1]. Where is the edge?

<details><summary>Solution</summary>

(a) R₁ = 8·90 − (7·10 + 12) = 720 − 82 = **638 → |R| > 100, point detected.**
R₂: the 8 neighbours are 30, 32, 31, 29, 33, 30, 31, 30 (sum 246), so R₂ = 8·30 − 246 = **−6 →
|R| < 100, not a point.**

(b) The 9s run from bottom-left to top-right: that is the **+45° mask** [−1 −1 2; −1 2 −1; 2 −1 −1],
response 3·2·9 = **54**. Horizontal, vertical and −45° each give **0**.

(c) First difference: **[0, 0, 0, 10, 10, 10, 0, 0, 0]**, non-zero along the whole ramp (a thick
edge). Second difference: **[0, 0, 10, 0, 0, −10, 0, 0]**, a +10 at the start of the ramp and −10 at
its end: a **double edge**, and the **zero crossing** between them marks the edge centre.

Trap: the 2nd derivative is zero along the ramp itself; the edge is located where it **changes sign**,
not where it is zero.
</details>

---

## Part C: L12 pattern classification

### Problem 18 (Gonzalez's Iris example): Minimum-distance classifier, two classes (10 pts)

Class means: m₁ = (4.3, 1.3) (Iris versicolor), m₂ = (1.5, 0.3) (Iris setosa), features (petal length,
petal width).

(a) Write d₁(x) and d₂(x). (b) Find the decision boundary d₁₂(x) = 0. (c) Classify x = (3, 1) using
both distances and decision functions.

<details><summary>Solution</summary>

(a) d_j(x) = xᵀm_j − ½‖m_j‖².
‖m₁‖² = 4.3² + 1.3² = 18.49 + 1.69 = 20.18 → **d₁(x) = 4.3x₁ + 1.3x₂ − 10.09**.
‖m₂‖² = 2.25 + 0.09 = 2.34 → **d₂(x) = 1.5x₁ + 0.3x₂ − 1.17**.

(b) d₁₂ = d₁ − d₂ = **2.8x₁ + 1.0x₂ − 8.92 = 0** (Gonzalez rounds to −8.9). It is the perpendicular
bisector of m₁m₂ and passes through the midpoint (2.9, 0.8).

(c) Distances: ‖x − m₁‖ = √(1.3² + 0.3²) = **1.334**; ‖x − m₂‖ = √(1.5² + 0.7²) = **1.655** →
class 1. Decision functions: d₁ = 12.9 + 1.3 − 10.09 = **4.11**; d₂ = 4.5 + 0.3 − 1.17 = **3.63**;
d₁₂ = 8.4 + 1 − 8.92 = **0.48 > 0** → **class 1 (versicolor)**.

Trap: with distances pick the **smallest**; with d_j pick the **largest**. Sign of d₁₂ > 0 means class 1.
</details>

### Problem 19: Minimum distance, three classes, plus reject (10 pts)

m₁ = (1, 2), m₂ = (6, 1), m₃ = (3, 6). Classify x = (4, 3). Write all three pairwise boundaries. If
the classifier rejects any x whose nearest mean is farther than 2.5, what happens to x?

<details><summary>Solution</summary>

Squared distances: to m₁: 3² + 1² = **10**; to m₂: 2² + 2² = **8**; to m₃: 1² + 3² = **10**.
Distances 3.162, **2.828**, 3.162 → **class 2**.

Decision functions d_j = xᵀm_j − ½‖m_j‖²: d₁ = 4 + 6 − 2.5 = 7.5; d₂ = 24 + 3 − 18.5 = **8.5**;
d₃ = 12 + 18 − 22.5 = 7.5. Largest is d₂ → class 2 (agrees).

Boundaries (m_i − m_j)ᵀx − ½(‖m_i‖² − ‖m_j‖²) = 0:
- **d₁₂: −5x₁ + x₂ + 16 = 0** (passes through the midpoint (3.5, 1.5))
- **d₁₃: −2x₁ − 4x₂ + 20 = 0** (i.e. x₁ + 2x₂ = 10)
- **d₂₃: 3x₁ − 5x₂ + 4 = 0**

Reject threshold 2.5: the nearest distance 2.828 > 2.5, so **x goes to the reject class**.

Trap: comparing squared distances is fine for picking the winner, but compare the real distance (not
the square) with a reject threshold.
</details>

### Problem 20 (deck idea, L12 S40): Scaled Euclidean distance changes the answer (10 pts)

Class 2: mean (2, 6), σ = (1, 1). Class 3: mean (7, 2), σ = (1, 4) (spread out vertically).
Classify x = (5, 5) with plain and with scaled Euclidean distance.

<details><summary>Solution</summary>

Plain: to class 2 √(3² + 1²) = √10 = **3.162**; to class 3 √(2² + 3²) = √13 = **3.606** → class 2.

Scaled: class 2 √((3/1)² + (1/1)²) = **3.162**; class 3 √((−2/1)² + (3/4)²) = √(4 + 0.5625) = **2.136**
→ **class 3**.

**Plain distance says class 2, scaled distance says class 3**, exactly the situation on S40 (a point at
the top of the widely spread class 3).

Trap: each class uses **its own** σ per dimension; you do not scale x once for all classes.
</details>

### Problem 21: k-nearest neighbours (10 pts)

| Point | (x₁, x₂) | Class |
|---|---|---|
| P1 | (3, 4) | R |
| P2 | (4, 4) | B |
| P3 | (5, 3) | B |
| P4 | (1, 4) | R |
| P5 | (1, 1) | R |
| P6 | (6, 3) | B |
| P7 | (6, 6) | B |
| P8 | (0, 1) | R |

Classify q = (3, 3) with 1-NN, 3-NN and 5-NN (Euclidean distance).

<details><summary>Solution</summary>

Squared distances to (3,3): P1 0+1 = **1**, P2 1+1 = **2**, P3 4+0 = **4**, P4 4+1 = **5**,
P5 4+4 = **8**, P6 9+0 = **9**, P8 9+4 = **13**, P7 9+9 = **18**.

Sorted: P1 (R, 1), P2 (B, 1.41), P3 (B, 2), P4 (R, 2.24), P5 (R, 2.83), P6 (B, 3), …

- **1-NN: P1 → R**
- **3-NN: R, B, B → B (2 : 1)**
- **5-NN: R, B, B, R, R → R (3 : 2)**

Trap: the answer depends on k. Use odd k with 2 classes, and sort by distance before voting (squared
distances keep the same order, so no square roots are needed).
</details>

### Problem 22: Bayes decision (10 pts)

(a) Fish: P(salmon) = 0.6, P(sea bass) = 0.4. A fish is measured as "bright". p(bright | salmon) = 0.2,
p(bright | sea bass) = 0.7. Find the evidence p(bright) and both posteriors. Decide.
(b) Three classes with priors 0.5, 0.3, 0.2 and likelihoods p(x|ωᵢ) = 0.1, 0.4, 0.6. Find the
posteriors. Which class would a "largest prior only" rule pick, and which does Bayes pick?
(c) The classifier is tested on 50 salmon (45 correct) and 50 sea bass (40 correct). Error rate?

<details><summary>Solution</summary>

(a) p(bright) = 0.2·0.6 + 0.7·0.4 = 0.12 + 0.28 = **0.40**.
P(salmon | bright) = 0.12/0.40 = **0.30**; P(sea bass | bright) = 0.28/0.40 = **0.70** →
**sea bass**, even though salmon has the larger prior.

(b) Products: 0.05, 0.12, 0.12; evidence 0.29. Posteriors **0.172, 0.414, 0.414**. Prior-only picks
ω₁; **Bayes gives a tie between ω₂ and ω₃** (a reject/tie-break case), and ω₁ is the least likely.

(c) Errors = 5 + 10 = 15 of 100 → **error rate 15 %, accuracy 85 %**.

Trap: comparing p(x|ω)·P(ω) is enough; dividing by p(x) does not change which class wins. Do not
compare likelihoods alone (that ignores the prior).
</details>

### Problem 23: Template matching (10 pts)

Find where the 2×2 template T best matches image I, using the sum of absolute differences (SAD).

```
I              T
0 1 1 0        1 1
1 1 0 0        1 0
0 1 1 1
```

<details><summary>Solution</summary>

Slide T over all 2 × 3 = 6 positions (top-left corner (r, c)):

| (r,c) | window | SAD |
|---|---|---|
| (0,0) | 0 1 / 1 1 | 2 |
| (0,1) | 1 1 / 1 0 | **0** |
| (0,2) | 1 0 / 0 0 | 2 |
| (1,0) | 1 1 / 0 1 | 2 |
| (1,1) | 1 0 / 1 1 | 2 |
| (1,2) | 0 0 / 1 1 | 3 |

**Best match at top-left (0,1), SAD = 0 (exact match).** With the plain correlation Σ w·f the score
there is 3, the maximum.

Trap: minimise SAD/SSD but **maximise** correlation. Raw correlation favours bright regions, which is
why Gonzalez (the source of S35's Fig. 12.8) normalises it into a correlation coefficient in [−1, 1].
For an m×n template the image needs (m−1)/2 rows and (n−1)/2 columns of padding so the template
centre can reach every border pixel (S35).
</details>

---

## Part D: short "explain / compare" model answers

**Opening vs closing (L10 S26-34).** Opening = erosion then dilation; it removes small bright objects,
thin protrusions and narrow bridges ("isthmuses"), and smooths contours from the inside. Closing =
dilation then erosion; it fills small holes and narrow dark gaps, fuses narrow breaks and long thin
gulfs, smoothing contours from the outside. Opening is anti-extensive (A∘B ⊆ A), closing is extensive
(A ⊆ A•B); both are increasing and idempotent. They are duals: closing A equals the complement of
opening Aᶜ (with the reflected SE).

**Median vs mean on salt-and-pepper noise (L11 S53-57).** An impulse is an extreme value. The mean
adds it into the average, so the spike is spread over the whole window (a 200 among 10s becomes a 30
blob) and edges blur. The median sorts the window and takes the middle value, so a few extreme values
are simply ignored, and a step edge is preserved because the middle value still belongs to one side of
it. Low-pass is better for Gaussian noise; median is better for impulse noise and for keeping edges.
Larger median windows remove more noise but erase fine detail (S57).

**First vs second derivative edge detection (L11 S37-47).** First-derivative operators (Roberts,
Prewitt, Sobel) give a magnitude that is large along the whole ramp of an edge (thick edges), plus a
direction θ = tan⁻¹(Gy/Gx); they need a threshold. Second-derivative operators (Laplacian) respond only
at the start and end of the ramp with opposite signs (a double edge); the edge is at the zero
crossing, which gives better localisation but no direction and very high noise sensitivity. LoG (and
its cheap approximation DoG, σ ratio 1.6) smooths with a Gaussian first to tame the noise.

**Nearest class mean vs nearest neighbour (L12 S38-41).** Nearest mean stores one prototype per class
and gives straight-line boundaries (perpendicular bisectors), which is cheap but fails for multi-modal
classes (S39; fix: one mean per mode) and for classes with very different spreads (fix: scale by σ,
S40). Nearest neighbour stores every training sample and can draw any boundary shape, but costs more
memory and time and is sensitive to noisy samples; using k > 1 neighbours with a majority vote makes it
more robust.

**Why not add every feature? (L12 S12-16).** A new feature helps only if it carries information the
existing ones do not (uncorrelated with them). A noisy feature adds variance and can reduce
performance. A boundary that fits every training sample perfectly may fail on new fish: the goal is
generalisation to novel input, not zero training error (overfitting).

---

## The problem types most likely on the exam

1. **Erosion / dilation / opening / closing of a small 0/1 grid** with a given SE (Problems 1-4), and
   boundary extraction A − (A ⊖ B). The deck spends 30+ slides here and the grids are exam-sized.
2. **A 3×3 mask at one pixel**: mean / weighted / median (Problem 9 uses the deck's own numbers), and
   **Sobel/Prewitt Gx, Gy, magnitude and direction** (Problem 15), Laplacian sharpening (Problem 13).
3. **Minimum-distance classifier** with given class means: distances, d_j(x), the boundary equation
   (Problems 18-19), with k-NN (Problem 21) as the other likely L12 calculation.
