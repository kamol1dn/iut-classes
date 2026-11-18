# L16: Geometric Processing: Interpolation, Scaling, Rotation, Translation, Mirroring

**Multimedia Computing · Week 10 · 54 slides · Dr. Minhaz Uddin Ahmed**
Source: [week10 - Multimedia Computing L16 (geometric processing).pptx](../slides/week10%20-%20Multimedia%20Computing%20L16%20(geometric%20processing).pptx) *(3.7 MB)*

The reference slide (52) shows the cover of Gonzalez & Woods, 4th edition, with "Chapter 4". In that book
chapter 4 is frequency-domain filtering. Gonzalez's interpolation and geometric-transformation material sits
in the early "digital image fundamentals" chapter instead. Most slides come from other, older texts: C-style
pseudocode with `X_dest`/`X_source`, `LENA256.RAW` screenshots, and a hard-coded `+128` centre for 256×256
images. Slide 23 labels its kernel "Fig. 4.7", so "Chapter 4" probably refers to that other source book. Five Python practice snippets use OpenCV and Pillow. They read
`pepper.png`, which isn't in `resources/`, so any image will do.

The eClass syllabus lists "geometric transformation" in week 5. It arrived here instead. The key formulas
(slides 15, 19, 20, 23, 28, 43) and all the result images are pictures. The formulas are transcribed below,
so open the pptx only for the figures.

## Outline

| Slides | Topic |
|---|---|
| 3–5 | **Interpolation** = estimating unknown values from known ones. **Geometric processes** move pixels around and ideally don't change their values. The basic three are **scaling, rotation and translation** |
| 6–8 | **Forward mapping** (for each source pixel, compute where it lands) leaves **holes** (destination pixels nobody maps to) and **overlaps** (two sources land on one destination). **Reverse (inverse) mapping** walks the *destination* pixels and asks which source position each comes from, so it has neither problem |
| 9–10 | Interpolation fills in values at addresses *between* pixels. Better quality costs more time. For a 2× zoom, `x_src = x_dest / 2`, so `dest[1][1]` needs `source[0.5][0.5]`. Zooming = create the new pixel locations, then assign them grey levels |
| 11–14 | **Nearest neighbour**: round the fractional source address to the closest pixel. Fast, but blocky, and worse the more output pixels share one input pixel. Its kernel is a box |
| 15–17 | **Bilinear**: use the 2×2 neighbours. Interpolate horizontally (top and bottom pairs), then vertically. Smoother, but slower than NN. Slide 15 also gives the backward-mapping matrix for scale + rotation + translation |
| 18–20 | Interpolation as **convolution** with a continuous kernel: NN = box, linear = triangle. 1-D comparison plots |
| 21–24 | **Higher order**: **cubic convolution** needs 4 samples in 1-D (16 in 2-D). Its kernel has negative lobes, so results are **clipped** to the valid pixel range. Example: a small image scaled up to 256×256 |
| 25–26 | **Bicubic**: the 4×4 = 16 nearest pixels and a cubic polynomial `a0 + a1x + a2x² + a3x³`. Smoother than bilinear, but slower and uses more memory |
| 27–29 | **Spline / B-spline**: a piecewise cubic. The **smoothest** of all, works like a low-pass filter, and **never needs clipping** |
| 30–31 | Practice: `cv2.resize(…, (600, 600))` with `INTER_NEAREST`, `INTER_LINEAR`, `INTER_CUBIC` side by side |
| 32 | Scaling vocabulary: magnification / up-sampling / zooming vs minification / decimation / down-sampling. Two rules: you can **never** add real resolution, and every operation degrades the image |
| 33–36 | **Minification**: replace each n×n block by its **median** or its **average**. Pillow demo: a 6×6 ramp shrunk to 3×3 with bilinear |
| 37–42 | **Rotation** by inverse mapping, about (0,0) or about the image centre. Multiples of 90° are a simple row/column rearrangement. Pillow `rotate(45, expand=True)` (expand keeps the corners) |
| 43–47 | **Translation**: move all or part of the image. The homogeneous 4×4 translation matrix. Double buffering for a partial translation. **Order matters**: translate-then-rotate ≠ rotate-then-translate (slide 46). Pillow `ImageChops.offset` |
| 48–51 | **Mirroring**: flip about the y-axis (horizontal mirror) or the x-axis (vertical mirror). Pillow `transpose(FLIP_LEFT_RIGHT / FLIP_TOP_BOTTOM)` |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Nearest neighbour (slides 11, 19) | `u0 = round(x) = ⌊x + 0.5⌋`, `ĝ(x) = g(u0)` |
| 1-D linear (slide 19) | `ĝ(x) = g(u0)·(1 − (x − u0)) + g(u0 + 1)·(x − u0)` with `u0 = ⌊x⌋` |
| Bilinear (slide 15) | `p = (1−dx)(1−dy)·p00 + dx(1−dy)·p10 + (1−dx)dy·p01 + dx·dy·p11`. dx, dy = the fractional offset from p00. p10 is to the right, p01 below |
| Bilinear as code (slide 17) | `top = NW + dx·(NE − NW)`, `bottom = SW + dx·(SE − SW)`, `p = top + dy·(bottom − top)` |
| Worked example *(mine)* | p00 = 10, p10 = 20, p01 = 30, p11 = 40, dx = 0.25, dy = 0.5: top = 12.5, bottom = 32.5, **p = 22.5** |
| Interpolation as convolution (slide 20) | `ĝ(x0) = Σᵤ w(x0 − u)·g(u)` |
| Neighbours used | NN **1**, bilinear **4** (2×2), cubic / bicubic / B-spline **16** (4×4) |
| Backward mapping (slide 15) | `[x, y]ᵀ = (1/S)·[[cos θ, sin θ], [−sin θ, cos θ]]·[x′ − Tx, y′ − Ty]ᵀ` |
| Rotation about (0,0), inverse (slide 37) | `x_src = x_d·cos θ + y_d·sin θ`, `y_src = y_d·cos θ − x_d·sin θ` |
| Rotation about the centre *(mine, consistent with the line above)* | `x_src = (x_d − cx)cos θ + (y_d − cy)sin θ + cx`, `y_src = −(x_d − cx)sin θ + (y_d − cy)cos θ + cy` |
| Translation (slide 43) | `[X*, Y*, Z*, 1]ᵀ = [[1,0,0,X0],[0,1,0,Y0],[0,0,1,Z0],[0,0,0,1]]·[X, Y, Z, 1]ᵀ`, i.e. `v* = T·v` |
| Mirroring (slide 50) | horizontal: `(x, y) → (W − 1 − x, y)`. Vertical *(mine, by symmetry)*: `(x, y) → (x, H − 1 − y)` |
| Minification (slides 33–34) | block `{13, 4, 8, 2, 9, 6, 7, 25, 16}`: **median = 8**, **average = 90/9 = 10** |

### The two cubic kernels (slides 23 and 28, with the slide typos fixed)

```
Cubic convolution (parameter a):
  f(x) = (a+2)|x|³ − (a+3)|x|² + 1        for 0 ≤ |x| < 1
       = a|x|³ − 5a|x|² + 8a|x| − 4a       for 1 ≤ |x| < 2
       = 0                                 for |x| ≥ 2

Cubic B-spline:
  f(x) = ½|x|³ − |x|² + 2/3                for 0 ≤ |x| < 1
       = −⅙|x|³ + |x|² − 2|x| + 4/3        for 1 ≤ |x| < 2
       = 0                                 for |x| ≥ 2
```

The deck never gives a value for `a`. Common choices are −0.5 and −0.75 *(mine)*. OpenCV's `INTER_CUBIC`
uses −0.75: resizing a single bright pixel ×2 gives exactly the a = −0.75 kernel values (0.879, 0.262,
−0.105, −0.035), which I checked on OpenCV 5.0.

**Why one needs clipping and the other doesn't** *(mine)*. Cubic convolution has `f(0) = 1` and
`f(±1) = f(±2) = 0`, so it passes exactly through the original samples. It is a true interpolator. But for
`a < 0` it dips negative between 1 and 2, so near a sharp edge it overshoots and the result must be clipped
(slide 23). The B-spline has `f(0) = 2/3` and `f(±1) = 1/6`, and it is never negative. Every output is a
weighted average of its neighbours, so it can't overshoot and needs no clipping (slide 28). The same fact
means it doesn't reproduce the original pixels: it smooths them, hence "greatest smoothing" and "low-pass
filter".

### Slide 36's minification numbers *(mine)*

I ran the slide's code (Pillow 12.3). It prints exactly the slide's `[[21 39 57] [30 48 66] [38 56 74]]`.
The plain 2×2 block averages would be `[[17.5 37.5 57.5] [27.5 47.5 67.5] [37.5 57.5 77.5]]`. The centre
pixel agrees (47.5 rounds to 48), but the border pixels don't. When Pillow *shrinks*, it widens its bilinear
filter by the scale factor (to avoid aliasing). Each output pixel then averages about 4 source pixels per
direction, and at the border the window is cut off and leans inward. If an exam asks you to minify by hand
with averaging, give the block averages.

## Things that are wrong or loose in the deck

- **Slide 15 describes the bilinear weights backwards.** It says "each weight is directly proportional to
  the distance from each existing pixel". It is the reverse: the *closer* neighbour gets the *larger*
  weight, `(1 − dx)(1 − dy)` for p00. The slide's own formula shows that.
- **Slide 23's second interval reads `0 ≤ |x| < 2`.** It should be `1 ≤ |x| < 2`.
- **Slide 28's B-spline has the same interval slip and a wrong constant: `+3/4` should be `+4/3`.** Check:
  at `|x| = 1` the first branch gives 1/6. With 4/3 the second branch also gives 1/6, and it reaches 0 at
  `|x| = 2`. With 3/4 it would jump to −5/12. The plotted curve on the slide is the correct one.
- **Slide 37's "rotation about image center" formulas have three slips.** The `Y_source` line uses
  `X_dest − center_y` where it means `center_x`. The `+128` is the centre of a 256×256 image, so it should
  be `+center_x` / `+center_y`. The sign of the sin term is flipped relative to the (0,0) version, so the two
  formulas rotate in **opposite directions**. I checked at 90°: one sends source (1, 0) to destination
  (0, 1), the other to (0, −1). Use the consistent version in the table above.
- **Slide 37: rotating by 90° is not "a simple transposition".** A transpose mirrors the image about its
  diagonal. A 90° rotation is a transpose *plus* a flip of the rows or the columns.
- **Slide 17's code won't compile as written.** `(char)EWtop + NSweight*(EWbottom − EWtop)` casts only
  `EWtop`, so it should be `(char)(EWtop + …)`. `Ewbottom` and `EWbottom` are different names in C.
  `floatx − floor(x)` should be `floatx − floor(floatx)`. Slide 11 also mixes `floatx` and `floatX`.
- **Slide 45's `ImageChops.offset` is not a plain translation.** It **wraps around**: pixels pushed off the
  right or bottom edge reappear on the left or top. I checked this on a 4×4 array. Its comment "Create a
  new blank image" is wrong, since no blank image is made. For a translation with a black fill, use
  `image.transform(image.size, Image.AFFINE, (1, 0, -100, 0, 1, -50))` (shift right 100, down 50).
- **Slide 24's sizes don't match.** It says "128×125 original" scaled up to "256×256". Doubling 128×125
  gives 256×250, so "128×125" is probably a typo for 128×128.
- **Cubic convolution (slides 22–24) and bicubic (25–26) are the same method shown twice.** In 2-D, cubic
  convolution with a 4×4 neighbourhood *is* bicubic interpolation. Slide 26's "solve for a0…a3" and slide
  23's kernel are two ways of writing it.
- The reference slide's "Chapter 4" doesn't match the Gonzalez cover it shows (see the top).

## Links to other lectures

- **L7**: pixel neighbours. Bilinear uses the 2×2 block, bicubic the 4×4.
- **L11**: convolution and box/Gaussian blurs. Slide 20's "interpolation = convolution with a kernel" is
  the same operation, and the B-spline acting as a low-pass filter is why it blurs.
- **L15**: homogeneous coordinates and the 4×4 `transform` class. Slide 43's translation matrix is that.
- **L13 / L14**: down-sampling chroma (4:2:0) is minification of the colour channels.
