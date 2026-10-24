# L5 — Arithmetic Coding, Lossy Compression & MPEG Audio

**Multimedia Computing · Week 3 · 56 slides · Dr. Minhaz Uddin Ahmed**
Source: [week03 - Multimedia Computing L5.pptx](week03%20-%20Multimedia%20Computing%20L5.pptx)
Reference: textbook **Chapter 7** (arithmetic coding) and **Chapter 8** (lossy)

Two halves. The first finishes lossless coding with **arithmetic coding**, which
has a fully worked example you should be able to trace by hand. The second
starts **lossy compression** and spends most of its slides on **MPEG audio / MP3**.

**Contents:** arithmetic coding (encoder, codeword generation, decoder) · lossy
compression · rate-distortion · quantization · psychoacoustics and masking ·
MPEG-1 audio layers I/II/III · MP3 encoding pipeline · bit allocation · AAC /
MPEG-4 audio · MP4 container.

---

## 1. Arithmetic coding

Huffman gives every symbol a codeword with a **whole number of bits**.
Arithmetic coding encodes the **whole message as one number**, so it usually
compresses better than Huffman.

A message is an interval **[low, high)** inside [0, 1). Each symbol narrows the
interval in proportion to its probability. Longer messages give narrower
intervals, and a narrower interval needs more bits to pin down.

### Encoder (Algorithm 7.5)

```
low = 0.0; high = 1.0; range = 1.0
while symbol != terminator:
    get(symbol)
    high = low + range * Range_high(symbol)   # use the OLD low
    low  = low + range * Range_low(symbol)
    range = high - low
output a code with low <= code < high
```

> ⚠️ **The slide's pseudocode has the two lines in the wrong order.** It
> updates `low` first and then computes `high` from the *new* `low`, which gives
> the wrong answer. Both bounds must come from the old `low`. The worked table
> below is correct, so if you trace the slide's code literally it won't match.
> This is a known erratum in the textbook too.

### Worked example: encode `CAEE$`

| Symbol | Prob | Range |
|---|---|---|
| A | 0.2 | [0, 0.2) |
| B | 0.1 | [0.2, 0.3) |
| C | 0.2 | [0.3, 0.5) |
| D | 0.05 | [0.5, 0.55) |
| E | 0.3 | [0.55, 0.85) |
| F | 0.05 | [0.85, 0.9) |
| G / `$` | 0.1 | [0.9, 1.0) |

| After | Low | High | Range |
|---|---|---|---|
| start | 0 | 1.0 | 1.0 |
| C | 0.3 | 0.5 | 0.2 |
| A | 0.30 | 0.34 | 0.04 |
| E | 0.322 | 0.334 | 0.012 |
| E | 0.3286 | 0.3322 | 0.0036 |
| `$` | **0.33184** | **0.33220** | 0.00036 |

Speaker-note rule for each step: new bounds = `low + range × (symbol's lower
limit)` and `low + range × (symbol's upper limit)`.

### Picking the codeword (Procedure 7.2)

Build the **shortest binary fraction** that lands in [low, high): set the next
bit to 1; if the value is now above `high`, set it back to 0; stop as soon as
the value is at least `low`.

For `CAEE$` this gives **0.01010101₂ = 0.33203125**, so the message takes **8 bits**.

### Decoder (Algorithm 7.6)

Repeat until you reach the terminator: find the symbol whose range contains
`value`, output it, then rescale with `value = (value − low_s) / range_s`.

| Value | Symbol | Low | High | Range |
|---|---|---|---|---|
| 0.33203125 | C | 0.3 | 0.5 | 0.2 |
| 0.16015625 | A | 0.0 | 0.2 | 0.2 |
| 0.80078125 | E | 0.55 | 0.85 | 0.3 |
| 0.8359375 | E | 0.55 | 0.85 | 0.3 |
| 0.953125 | $ | 0.9 | 1.0 | 0.1 |

The contents slide also lists **scaling and incremental coding**, but the deck
has no slide on it. It covers how real coders output bits as they go so they
don't run out of floating-point precision. Read it in the textbook, Ch. 7.

---

## 2. Lossy compression

- The output is a **close approximation** of the original, not an exact copy.
- It gets a **much higher compression ratio** than lossless.
- **Rate-distortion theory** describes the trade-off: fewer bits means more
  distortion. That slide is a diagram only, so look at the pptx.

### Quantization, the main source of loss

It maps many input values to a much smaller set of output values.

- **Uniform:** the levels are evenly spaced.
- **Non-uniform:** the levels are unequal, usually spaced **logarithmically**
  (as in μ-law, from L3).

### Why audio needs compressing

**Data rate = sampling rate × bits per sample × channels** (+ control info)

CD audio is 44 100 Hz × 16 bit × 2 channels = **1.41 Mbit/s**.

> ⚠️ The slide says "1.4M per second, 84M per minute, 5G per hour" without units.
> Those numbers are **bits**. In bytes it is about **176 KB/s, 10.6 MB/min and
> 635 MB/hr**. If an exam asks for bytes, divide by 8.

### Audio formats

- An **audio coding format** is the representation, e.g. MP3, AAC, Vorbis,
  FLAC or Opus. A **codec** is a hardware or software implementation of one.
- **Lossless** formats (FLAC, Apple Lossless) give bigger files.
- **Lossy** formats (MP3, AAC) are the most widely used. Both are built on the
  **MDCT** (modified discrete cosine transform) and **perceptual coding**. They
  lose data permanently, so they aren't suitable for music production.

---

## 3. Psychoacoustics, the basis of MP3

- Humans hear **20 Hz – 20 kHz** and are most sensitive at **500 Hz – 5 kHz**,
  because the basilar membrane responds most to middle frequencies.
- The **threshold of hearing** is the quietest level you can hear at each
  frequency. It is lowest in the middle of the range.
- **Masking** means one sound makes another harder to hear:
  - **Frequency masking:** a loud tone hides quieter tones at nearby frequencies.
  - **Temporal masking:** a loud sound hides quieter ones just before and after it.
- **Key insight (slide 41):** each extra bit adds about **6 dB** of SNR. Masking
  lets you **raise the noise floor** near a loud sound without anyone hearing
  it. A higher noise floor means fewer bits, which is compression.

---

## 4. MPEG-1 audio

| | |
|---|---|
| Standardised | MPEG-1 Audio **1992**, MPEG-2 Audio **1994** |
| Precision | 16 bit |
| Sampling rates | 32, 44.1, 48 kHz |

| Layer | Bit-rate range | Target | Notes |
|---|---|---|---|
| **I** | 32–448 kbps | 192 kbps | Simplest |
| **II (MP2)** | 32–384 kbps | 128 kbps | Sub-band coder in the time domain, based on MUSICAM. Standard for DAB radio and DVB TV. |
| **III (MP3)** | 32–320 kbps | 64 kbps (goal 128) | Most complex, best compression, used on the internet |

The layers are **backwards-compatible**: a Layer III decoder also plays I and
II. MP3 is an **open standard** that no single company owns, which helped it
spread.

History: the first psychoacoustic masking codec came from **AT&T Bell Labs in
1979**. MP3 grew out of **OCF** and **PXFM**. MPEG-1 Layer III was released
publicly in **1993**. Then mp3.com launched in **1997** and Napster in **1999**,
which raised copyright problems.

### The encoding pipeline

1. A **filter bank** splits the input into **32 equal frequency sub-bands**.
2. A **psychoacoustic model** works out which parts are masked and can be dropped.
3. **Bit allocation** gives each sub-band only as many bits as its audible
   noise allows.
4. The result is packed into the **bitstream**.

### Bit allocation algorithm (slide 37), likely exam material

**MNR = SNR − SMR**. MNR is the mask-to-noise ratio and SMR the signal-to-mask ratio.

1. Compute MNR for every sub-band. The SNR estimates come from tables in the standard.
2. Find the sub-band with the **lowest MNR**.
3. Give that sub-band more code bits.
4. Look up the new SNR estimate for it and repeat until the bits run out.

### Quality problems

- **Too low a bit-rate** causes artifacts: **ringing** and **pre-echo**. Pre-echo
  is sound heard *before* it happens. It comes from transform coding and is most
  audible on percussion such as cymbals.
- **CBR vs VBR:** constant versus variable bit-rate encoding.

---

## 5. MPEG-4 audio and AAC

- **AAC** (Advanced Audio Coding) replaced MP3. It was introduced in **1997** as
  MPEG-2 Part 7 and folded into MPEG-4 in **1999**. It is the default on
  iPhone, Android, PlayStation and others.
- It improves on MP3 with **8–96 kHz** sampling, arbitrary bit-rates, variable
  frame length, **up to 48 channels**, and a simpler filter bank using **pure MDCT**.
- MPEG-4 audio covers **2–64 kbps** with three families of coders:

| Coder | Bit-rate | Sampling |
|---|---|---|
| Parametric | 2–6 kbps | 8 kHz |
| **CELP** (code-excited linear prediction, for speech) | 6–24 kbps | 8 / 16 kHz |
| Time-frequency | ≥ 16 kbps | > 7 kHz |

- **MPEG-4 Part 3** covers speech coding (CELP), general audio (AAC), lossless
  audio, text-to-speech and structured audio (MIDI).
- **MPEG-4 Part 14 = MP4** (`.mp4`). It is a **container format**, not a codec:
  a wrapper that holds video and audio streams plus metadata.

### Criteria for a good standard

It achieves the outcome, is understandable, can be implemented efficiently,
supports competition, has benchmarks, is backed by industry and is good for
users. There are two models: **implement first, then standardise**, or
**standardise first, then implement**.

---

## If you're revising this in 10 minutes

1. **Trace arithmetic coding of `CAEE$`** → [0.33184, 0.33220), codeword
   **0.01010101₂** (8 bits). Then decode it back.
2. Know that the **slide's encoder pseudocode is buggy**: compute `high` from the old `low`.
3. Arithmetic coding beats Huffman because it isn't limited to **whole bits per symbol**.
4. **Uniform vs non-uniform quantization**. Quantization is where the loss happens.
5. **CD data rate = 1.41 Mbit/s**. Watch bits versus bytes.
6. **Frequency vs temporal masking**, and the **6 dB per bit** argument.
7. MP3 pipeline: **32 sub-bands → psychoacoustic model → bit allocation**, with **MNR = SNR − SMR**.
8. **Layer I/II/III** bit-rates, and MP2 for broadcast.
9. **AAC vs MP3**, **CELP** for speech, and **MP4 is a container**.
