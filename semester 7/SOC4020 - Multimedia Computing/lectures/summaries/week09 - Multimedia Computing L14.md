# L14: Video Fundamentals (Analog and Digital Video)

**Multimedia Computing · Week 9 · 40 slides · Dr. Minhaz Uddin Ahmed**
Source: [week09 - Multimedia Computing L14.pptx](../slides/week09%20-%20Multimedia%20Computing%20L14.pptx) *(2.5 MB)*

Li, Drew & Liu, *Fundamentals of Multimedia* (2nd ed.), **chapter 5** (fundamental concepts in video). The
cover is on slide 38. Slides 13–14 are two gamma figures borrowed from chapter 4. On top of the book there
are newer slides: the YCbCr maths, the composite-signal equation, the J:a:b subsampling notation, Rec. 601,
compression, SDI/HDMI and an OpenCV webcam loop. Nine slides are textbook pages pasted in as pictures
(19, 24, 26–28, 30–33). Their numbers are copied into the tables below, so you only need the pptx
for the figures: the interlaced raster (slide 16), the helicopter (18) and the subsampling grids (25).

His week-1 plan had video in week 6, and the eClass syllabus has digital video in week 10. It arrived in
week 9, as the first deck after the midterm week. It leans on **L2** (sampling and quantization), **L6**
(gamma) and **L13** (DCT, and temporal redundancy between frames).

## Outline

| Slides | Topic |
|---|---|
| 2 | Contents. It lists "3D video", which the deck never reaches |
| 3–5 | **Analog video**: a continuous voltage. A CRT's electron gun sweeps line by line (**horizontal retrace**) and frame by frame (**vertical retrace**). Blanking intervals carry the sync pulses. Weaknesses: noise, attenuation, tapes wear out |
| 6–7 | **Component video**: three separate signals (R, G, B or Y, Pb, Pr). Best colour and no crosstalk, but needs the most bandwidth and good sync. YPbPr is analog, YCbCr digital. Luma gets more bandwidth than the colour differences because the eye resolves grey detail better than colour |
| 8–10 | **Composite video**: luma and chroma share one carrier on one wire. Chroma (I, Q in NTSC or U, V in PAL) is modulated onto a colour **subcarrier** at the top of the luma band, and the receiver separates them again. The overlap causes **dot crawl** and **cross-colour**. Slide 10 is a photo of a plaid shirt with a paragraph about herringbone fabric (see the last section) |
| 11 | **S-Video**: two wires, one for luma and one for composite chroma. Less crosstalk than composite. Colour can be sent at lower resolution because we only see "fairly large blobs" of colour |
| 12–14 | Received brightness is a monotonic but non-linear function of voltage, hence **gamma correction** (Li Fig. 4.6 and 4.7, the same idea as L6) |
| 15–18 | **Progressive** scanning draws every line of a frame in order. **Interlaced** scanning draws the odd lines (odd field), then the even lines (even field). Two fields make one frame. Fig. 5.1 labels the retraces (Q→R horizontal, T→U and V→P vertical). Interlace blurs fast motion: the helicopter in Fig. 5.2 |
| 19 | **De-interlacing**: drop one field and repeat the other's lines (loses half the information), or combine both fields. Sync uses a "blacker-than-black" level to mark the start of a line |
| 20 | **ADC**: sample and quantize to PCM. **Rec. 601** samples standard-definition luma at **13.5 MHz** |
| 21–25 | **Chroma subsampling**, J:a:b notation, and the 4:4:4 / 4:2:2 / 4:1:1 / 4:2:0 schemes (pixel grids on slide 25). Speaker note: 4:2:0 is the scheme JPEG and MPEG use |
| 26–27 | **NTSC**: the voltage of one scan line (Fig. 5.3) and the basic numbers (table below) |
| 28 | **PAL**: YUV, 8 MHz channel. The chroma sign alternates on successive lines (hence "Phase Alternating Line"), so a comb filter at the receiver can average neighbouring lines to separate Y from C |
| 29 | **SECAM**: also 625 lines and 25 fps. U and V are sent on alternate lines, only one per line |
| 30 | Comparison table of the three analog systems |
| 31 | **Digital video** advantages: store and process it (noise removal, cut and paste), direct access makes non-linear editing easy, re-recording doesn't degrade it, and it is easy to encrypt and more tolerant of channel noise |
| 32–33 | **HDTV**: the aim is a *wider* picture (**16:9** instead of 4:3), not more detail per unit area. It moves to **progressive** scan. MPEG-2 video and AC-3 (5.1) audio. SDTV, then **EDTV** (≥ 480 active lines), then **HDTV** (≥ 720 active lines) |
| 34 | Compression: **intra-frame** (spatial: DCT or wavelets plus quantization, e.g. JPEG and MPEG-2 I-frames) vs **inter-frame** (temporal: motion estimation and compensation on macroblocks, **I, P and B frames**) |
| 35 | Interfaces: **SDI** (coax with BNC connectors, uncompressed, broadcast studios) and HDMI / DisplayPort (one cable for video, audio and control data) |
| 36–37 | OpenCV webcam capture: `cv2.VideoCapture(0)`, loop on `cap.read()`, `cv2.imshow`, quit on `q` with `cv2.waitKey(1)`, then `cap.release()` and `cv2.destroyAllWindows()` |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Luma (slide 7) | `Y = 0.299R + 0.587G + 0.114B` |
| Colour differences (slide 7) | Pb/Cb from `B − Y`, Pr/Cr from `R − Y` (scaled in practice, see the last section) |
| Composite signal (slide 9) | `V(t) = Y(t) + U(t)·sin(ω_sc·t) + V(t)·cos(ω_sc·t) + S(t)`. `S(t)` = sync pulses |
| Colour subcarrier | ≈ **3.58 MHz** NTSC, ≈ **4.43 MHz** PAL |
| Interlace | 2 fields = 1 frame. NTSC has **262.5 lines per field** |
| NTSC scan line (slide 26) | white 0.714 V, black 0.055 V, blank 0 V, sync −0.286 V. **10.9 µs** horizontal retrace + **52.7 µs** active line |
| Check *(mine)* | `1 / (525 × 29.97) = 63.6 µs` per line, and `10.9 + 52.7 = 63.6` ✓ |
| NTSC blanking (slide 27) | 20 lines per field for vertical retrace and control data. About 1/6 of each line is blanked for horizontal retrace |
| NTSC visible lines (slide 27) | pixels fall between scan lines, so only about **70%** of active lines show (progressive), as low as **50%** interlaced |
| Rec. 601 | 13.5 MHz luma sampling for SD |

### The three analog systems (slide 30)

| System | Frame rate | Scan lines | Channel width | Y | I or U | Q or V |
|---|---|---|---|---|---|---|
| NTSC | 29.97 | 525 | 6.0 MHz | 4.2 | 1.6 | 0.6 |
| PAL | 25 | 625 | 8.0 MHz | 5.5 | 1.8 | 1.8 |
| SECAM | 25 | 625 | 8.0 MHz | 6.0 | 2.0 | 2.0 |

All three are 4:3 and interlaced. NTSC is North America and Japan. PAL is Western Europe, China, India and
many other countries.

### Chroma subsampling, J:a:b (slides 21–25)

Think of a block **J pixels wide and 2 rows tall** (J is almost always 4). **a** = chroma samples in the
first row. **b** = chroma samples that *change* in the second row (b = 0 means row 2 reuses row 1's colour).
So each chroma channel gets `a + b` samples per 8 pixels.

*(cost columns are mine)*

| Scheme | What is subsampled | Y : Cb : Cr per 4×2 block | Bits/pixel at 8-bit | vs 4:4:4 |
|---|---|---|---|---|
| 4:4:4 | nothing | 8 : 8 : 8 | 24 | 100% |
| 4:2:2 | chroma halved horizontally | 8 : 4 : 4 | 16 | 67% |
| 4:1:1 | chroma quartered horizontally | 8 : 2 : 2 | 12 | 50% |
| 4:2:0 | chroma halved horizontally *and* vertically | 8 : 2 : 2 | 12 | 50% |

4:1:1 and 4:2:0 cost the same. 4:1:1 keeps full vertical colour resolution, while 4:2:0 spreads the loss
over both directions. Slide 24 gives the 4:2:2 sample order: `(Cb0,Y0)(Cr0,Y1)(Cb2,Y2)(Cr2,Y3)(Cb4,Y4)…`.

## Things that are wrong or loose in the deck

- **Slide 29 garbles the SECAM subcarriers.** "SECAM and PAL … differ slightly in their color subcarriers
  at 4.25MHz and 4.41 MHz respectively" reads as SECAM = 4.25 and PAL = 4.41. That contradicts the deck
  itself: PAL's subcarrier is **4.43 MHz** (slides 9 and 28). The two numbers belong to **SECAM alone**,
  which uses two subcarriers, about 4.25 MHz and 4.41 MHz, one for each colour-difference signal.
- **Slides 21 and 23 explain J:a:b two different ways.** Slide 23 says the numbers give "how many pixel
  values, per four original pixels, are actually sent". That reading works for 4:4:4, 4:2:2 and 4:1:1, but
  for 4:2:0 it would mean no Cr at all. Use slide 21's row-based definition (the table above).
- **Slide 22 labels 4:4:4 "Uncompressed".** 4:4:4 only means *no chroma subsampling*. A 4:4:4 stream can
  still be compressed, and 4:2:2 video can travel uncompressed (over SDI, for example).
- **Slide 7 writes Cb = B − Y and Cr = R − Y.** In BT.601 they are scaled to the range ±0.5. With slide 7's
  luma, `B − Y` spans ±0.886 and `R − Y` spans ±0.701, so `Cb = 0.5/0.886·(B − Y) = 0.564(B − Y)` and
  `Cr = 0.5/0.701·(R − Y) = 0.713(R − Y)`. 8-bit digital video then adds an offset of 128.
- **Slide 35 puts DisplayPort under "TMDS / FRL".** Those are HDMI's signalling schemes. DisplayPort has its
  own packet-based link.
- **Slide 10 never says why the shirt is there.** The point *(mine)*: a fine luma pattern like herringbone
  has frequencies inside the chroma band. A composite decoder reads it as colour, so the shirt shimmers with
  false colour. That is the **cross-colour** artefact from slide 9.
- Slide 2 lists **"3D video"**, but no slide covers it.
- Slide 33 is dated book text: analog broadcasting is "planned to be replaced by the year 2009", and it
  refers to a "Table 5.4" that isn't in the deck.

## Links to other lectures

- **L2**: sampling and quantization. Slide 20's ADC is the same idea applied to a video signal.
- **L6**: gamma. Slides 12–14 are the display-side reason gamma correction exists.
- **L13**: the DCT and JPEG. Slide 34's intra-frame coding *is* JPEG-style coding, and inter-frame coding
  exploits the temporal redundancy L13 slides 26–27 describe. JPEG also uses 4:2:0 subsampling.
- **L17**: shot boundary detection and background subtraction work on video frames.
