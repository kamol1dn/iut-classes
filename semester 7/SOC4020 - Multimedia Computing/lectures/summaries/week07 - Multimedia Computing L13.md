# L13: Image Compression

**Multimedia Computing · Week 7 · 44 slides · Dr. Minhaz Uddin Ahmed**
Source: [week07 - Multimedia Computing L13.pptx](../slides/week07%20-%20Multimedia%20Computing%20L13.pptx) *(3.1 MB)*

Gonzalez **chapter 8** (image compression). The redundancy material, Table 8.1, the run-length figure, the
IGS table and the TASO rating scale are Gonzalez's own figures and tables, pasted in. The rest is DCT/JPEG
background plus MATLAB demos (JPEG at three quality levels, PNG, run-length encoding, DCT truncation).
Several key slides are pictures only (9, 15, 24–26, 28, 36–37, 40–41), so **open the pptx for the DCT
formula (slide 9), the variable-length code table (24) and the compression model (41)**.

**This does not continue L12.** L12 was pattern classification (Gonzalez ch. 12). L13 starts a new block,
image compression, which is what the eClass syllabus schedules for weeks 7–9 (entropy coding → lossless →
lossy/JPEG). It does lean heavily on **L4** (compression ratio, run-length coding, variable-length codes,
Huffman) and **L5** (lossy compression, quantization), which *are* pre-midterm material. See the last
section for what that means for the midterm.

## Outline

| Slides | Topic |
|---|---|
| 3–6 | Goal: reduce the bytes needed to represent an image by removing redundancy. Used in fax, teleconferencing, etc. Review: lossless vs lossy |
| 7 | Compression model (source encoder → channel encoder → channel/store → decoders). Standards: **JPEG = DCT**, **JPEG 2000 = DWT** (wavelets), GIF |
| 8–9 | **DCT**: spatial domain → frequency domain, a sum of cosines. Energy concentrates in a few low-frequency coefficients, so high frequencies can be dropped. 2-D DCT formula on **8×8 blocks** |
| 10 | **JPEG-style pipeline**: split into 8×8 blocks → 2-D DCT → **quantize** (the lossy step) → **zigzag** scan → **entropy coding** (Huffman) |
| 11–12 | MATLAB: `blockproc` + `dct2` on 8×8 blocks, display `log(abs(DCT))` |
| 13–15, 20 | **Relative data redundancy** `R_D = 1 − 1/C_R`, **compression ratio** `C_R = n₁/n₂` |
| 16, 19 | MATLAB: save `peppers.png` as JPEG at quality 90 / 50 / 10, compare file sizes |
| 17–18 | PNG is **lossless**: same pixel values, smaller file |
| 21 | The **three redundancies**: coding, interpixel, psychovisual |
| 22–25 | **Coding redundancy**: give frequent gray levels short codes. `L_avg`. Table 8.1: fixed 3-bit code vs variable-length code |
| 26–27 | **Interpixel redundancy**: neighbouring pixels are correlated (spatial); successive video frames are correlated (**temporal / inter-frame**). Gonzalez's matchstick images with their autocorrelation plots |
| 28–33 | **Run-length coding**: Gonzalez's binary circuit-board example, then a MATLAB RLE of `cameraman.tif` |
| 34–38 | **Psychovisual redundancy**: the eye doesn't analyse every pixel, so some information can go unnoticed. IGS quantization table and figure. MATLAB: keep only the top-left 10% of DCT coefficients, inverse DCT |
| 39–40 | **Fidelity criteria**: subjective (TASO rating scale, 1 Excellent … 6 Unusable) vs objective (sum of absolute error, RMS error, SNR) |
| 41 | Gonzalez's compression system model (source encoder = mapper → quantizer → symbol encoder) |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Compression ratio | `C_R = n₁ / n₂` (original ÷ compressed) |
| Relative redundancy | `R_D = 1 − 1/C_R`. `C_R = 1` → `R_D = 0` (no redundancy). `C_R = 10` → `R_D = 0.9` (90% of D₁ redundant) |
| Slide 20's question: `n₁ ≪ n₂`? *(answer is mine, from Gonzalez)* | `C_R → 0`, `R_D → −∞`: the "compressed" set is *bigger* than the original. Slide 29 is exactly this case |
| Gray-level probability | `p_r(r_k) = n_k / n`, `k = 0 … L−1` |
| Average code length | `L_avg = Σ l(r_k)·p_r(r_k)`. An M×N image needs `M·N·L_avg` bits. A fixed 8-bit code gives `L_avg = 8` |
| Table 8.1 (slide 24) | Code 2: `L_avg = 2.7` bits vs 3 bits fixed. `C_R = 3/2.7 = 1.11`, `R_D ≈ 0.1` |
| Gonzalez RLE (slide 28) | `C_R = (1024·343) / (12166·11) ≈ 2.62`, `R_D ≈ 0.62`. 12,166 runs at 11 bits per run |
| 2-D DCT (slide 9) | `F(u,v) = ¼·α(u)α(v)·Σₓ Σᵧ f(x,y)·cos((2x+1)uπ/2N)·cos((2y+1)vπ/2N)`, `α(0) = 1/√2`, else 1 |
| JPEG pipeline | blocks → DCT → **quantize** → zigzag → entropy code. Only quantization loses information |

Worked check for Table 8.1 *(mine)*: `0.19·2 + 0.25·2 + 0.21·2 + 0.16·3 + 0.08·4 + 0.06·5 + 0.03·6 + 0.02·6 = 2.70`.

### Where each redundancy is attacked *(mine, from Gonzalez's model on slide 41)*

| Redundancy | Encoder stage | Example | Reversible? |
|---|---|---|---|
| Interpixel | **mapper** | run-length, pixel differences / prediction, DCT | yes |
| Psychovisual | **quantizer** | dropping high-frequency DCT coefficients, IGS | **no**, which is why the decoder has no "inverse quantizer" |
| Coding | **symbol encoder** | Huffman, variable-length codes | yes |

### IGS quantization (slide 36 table, no explanation on the slide) *(mine)*

Improved Gray-Scale quantization to 4 bits: add the low 4 bits of the previous *sum* to the current
8-bit pixel (skip the add if the pixel's high 4 bits are already 1111), and keep the high 4 bits of the
result as the code. The pseudo-random carry breaks up the false contours that plain 16-level quantization
causes (compare the vase pictures on slide 34).

### The peppers file sizes (slide 19) *(ratios are mine)*

Assuming MATLAB's standard 384×512 RGB `peppers.png` (589,824 bytes of raw pixels):

| File | Bytes (slide) | `C_R` vs raw pixels |
|---|---|---|
| JPEG quality 90 | 41,327 | ≈ 14 |
| JPEG quality 50 | 15,671 | ≈ 38 |
| JPEG quality 10 | 6,619 | ≈ 89 |
| PNG (lossless) | 287,589 | ≈ 2 |

Lossless can only remove coding and interpixel redundancy. JPEG also throws away psychovisual
redundancy, hence the order-of-magnitude gap.

## Things that are wrong or loose in the deck

- **Slide 29/32's run-length demo actually made the image bigger.** It reports "Original Size: 65536,
  Compressed Size: 112224, Compression Ratio: 1.71". The code computes `compressed_size / original_size`,
  which is the **inverse** of the deck's own `C_R = n₁/n₂`. The real `C_R` is 65536/112224 ≈ **0.58**
  (`R_D` ≈ −0.71): 56,112 runs for 65,536 pixels, so almost every pixel is its own run. RLE suits
  binary or flat images (slide 28). It does not suit a noisy natural photo like `cameraman.tif`. The
  "bytes" labels are also really element counts.
- **Slide 13 says "Image compression is an irreversible process."** Only lossy compression is. The deck
  itself shows lossless PNG (slides 17–18), and slide 8's speaker note says "lossless" for the DCT.
  The DCT itself is invertible. The loss happens at quantization (slide 10, step 3).
- **Slide 9 calls the formula "the general form" but the ¼ only holds for N = 8.** The general scale is
  `2/N`. That gives ¼ for JPEG's 8×8 blocks.
- **Slide 35 says psychovisual removal is "usually irreversible".** It is always irreversible: it is
  quantization. Its last sentence is garbled ("It's elimination is real visual information is possible
  only because…"). The intended meaning: removing it is possible only because that information isn't
  essential to normal vision.
- **Slide 19's output is missing the original size.** It also re-saves a file that was already a PNG as
  PNG. So the "lossless" demo doesn't really show compression against the original.
- **Slide 38 applies one DCT to the whole image**, not 8×8 blocks as in slides 9–10. That's why the
  result on slide 37 is a uniformly blurred image with ringing, rather than JPEG's blocky artifacts.
- Small numeric slips: slide 24's `R_D = 0.099` is exactly **0.1** (`1 − 2.7/3`), and slide 28's
  `C_R = 2.63` computes to **2.62**. Slide 10 also skips steps a real JPEG has (level shift by 128, colour
  conversion and chroma subsampling, run-length coding of the zero coefficients before Huffman).
- Slide 12 displays `log(abs(DCT_image))`. Any exactly-zero coefficient gives `−Inf`. The usual form is
  `log(1 + abs(…))`.

## Is this midterm material?

The midterm is **Wed 2026-10-28**, and the scope so far has been understood as L1–L12. L13 is a **new topic**,
not a continuation of L12, and it is the first deck of the post-midterm compression block on the eClass
syllabus. My read: it is probably **not core midterm material**. But that depends on whether it was
lectured before the exam, which this repo doesn't record. If in doubt, ask in class.

The cheap insurance is the part that overlaps L4: `C_R`, `R_D = 1 − 1/C_R`, `L_avg`, the three
redundancies and run-length coding. That's half an hour of work and examinable via L4 anyway. Leave the DCT formula,
IGS and the fidelity criteria for after the midterm.

## Links to other lectures

- **L4**: compression ratio `B₀/B₁`, run-length coding, Huffman. Slides 22–25 here are the image version
  of L4's variable-length coding.
- **L5**: lossy compression and quantization. MP3's MDCT is a cousin of the DCT here.
- **L11** (blur / smoothing filters): keeping only low-frequency DCT coefficients (slide 38) is a
  low-pass filter, which is why the result looks blurred.
