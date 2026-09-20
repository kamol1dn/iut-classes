# L2 — Sound, Digitization, Sampling & Aliasing

**SOC4020 · Week 1 · 58 slides · Dr. Minhaz Uddin Ahmed**
Source: [week01 - Multimedia Computing L2.pptx](week01%20-%20Multimedia%20Computing%20L2.pptx)

This is where the course gets technical. Unlike L1, nearly everything here is
examinable — definitions, formulas, and named results.

**Contents:** sound · analog-to-digital conversion (sampling, quantization, bit
rate) · signals and systems (LTI, useful signals, Fourier transform) · sampling
theorem and aliasing (spatial and temporal).

---

## 1. What sound is

A **wave phenomenon like light, but macroscopic** — air molecules being
compressed and expanded by some physical device. A speaker vibrates back and
forth, producing a **longitudinal pressure wave** we perceive as sound.

> **Without air there is no sound** — hence silence in space. Easy exam question.

Because it's a pressure wave it takes **continuous values**, as opposed to
digitized values with a finite range.

Although longitudinal, it still shows ordinary wave behaviours — **and this trio
is exam-shaped:**

| Behaviour | Meaning |
|---|---|
| **Reflection** | Bouncing off a surface |
| **Refraction** | Change of angle when entering a medium of different density |
| **Diffraction** | Bending around an obstacle |

These are what make **surround sound design possible**.

Sound is detected by measuring the pressure level at a point using a
**transducer**, which converts pressure into voltage.

## 2. Digital data acquisition

**Three major components of a multimedia system:**

1. Multimedia **content creation**
2. **Compression / storage** of the content
3. **Delivery / distribution** of the content

Digitizing happens in **1D** (audio — only one independent variable, time),
**2D** (images), and **3D** (video).

### Analog vs digital

| | Definition |
|---|---|
| **Analog** | Can be represented by a **continuous function** |
| **Digital** | A **discrete set of values** defined at specific (usually regular) instances of the input domain — time, space, or both |

Periodic analog signals are either **simple** — a sine wave, which cannot be
decomposed further — or **composite**, made of multiple sine waves.

### Why digital wins — five advantages

1. **Interactivity and editability.** Easy to access a single pixel, a region, or a section of a soundtrack, and apply operations to each — enhancing a region's quality, removing noise from audio.
2. **No degradation.** Stored digital signals don't decay over time or distance the way analog does. His example is **VHS ghosting**, where tapes lose image quality through repeated use.
3. **Efficient compression and transmission** over digital networks — live models like digital cable and video on demand, passive ones like DVD.
4. **Easy storage** on magnetic media (hard drives) or solid state (flash drives, memory cards), because everything is binary **regardless of data type**.
5. **Better quality and higher fidelity** overall.

## 3. Sine wave properties

The vocabulary the rest of the lecture depends on:

| Property | Symbol | Meaning | Unit |
|---|---|---|---|
| **Peak amplitude** | A | Maximum strength of the signal | volts |
| **Frequency** | f | Rate of change of the signal | Hertz (cycles/second) |
| **Period** | T | Time for one repetition | seconds |
| **Phase** | φ | Position of the waveform relative to time 0 | degrees/radians |
| **Wavelength** | λ | Distance occupied by one cycle | metres |

**Two formulas to memorise:**

```
T = 1 / f          (period and frequency are inverses)
λ = v · T          (v = signal velocity)
```

**The intuition he stresses:**

- Change over a **short** span of time → **high** frequency
- Change over a **long** span → **low** frequency
- A signal that **doesn't change at all** → frequency **zero**
- A signal that changes **instantaneously** → frequency **infinite**

### Time domain vs frequency domain

A complete sine wave in the time domain is **a single spike in the frequency
domain**. The frequency domain is more compact and much more useful once you
have several sine waves — three sine waves of different amplitude and frequency
become simply three spikes.

## 4. Analog-to-digital conversion

**Two processes: sampling and quantization.** The reverse — digital back to
analog — is **interpolation**.

The goal is that **no artifacts are created**, so that converting back gives
something indistinguishable from the original.

### Sampling

Taking measurements at **evenly spaced intervals**; the rate is the **sampling
frequency**.

With sampling interval `T`: `xs(1) = x(T)`, `xs(2) = x(2T)`, and so on.
**Reduce T (raise f) → more samples → more storage. Raise T (lower f) → fewer
samples → less storage.** `T` is the critical parameter.

Dimensions: **1D** (time, for sound) · **2D** (spatial x and y, for images) ·
**3D** (x, y, time for video, or x, y, z for 3D ranges). Practical sampling
involves **averaging**, in time or space.

**Numbers worth memorising:**

| Quantity | Value |
|---|---|
| Typical audio sampling rates | **8 kHz – 48 kHz** |
| Human hearing range | **~20 Hz – 20 kHz** (above that is ultrasound) |
| Human voice reaches | **~4 kHz** |

### Quantization

**Definition:** encoding the signal value at every sampled location with a
**predefined precision, defined by a number of levels**. The whole range `R` is
represented by a finite number of bits `b`, giving a **quantization step**.

| Bits | Levels |
|---|---|
| 8 | 256 |
| 4 | 16 |
| 3 | 8 |

> **Key point:** because each sample uses a finite number of bits, the quantized
> value **always differs from the true value** — quantization **always
> introduces error**.

**How many bits?** Depends on the signal and its use:

- **Music / audio → 16 bits**
- **Speech → 8 bits**

The range is divided into **fixed, uniformly separated intervals**. That works
well when all values in the range are **equally likely**, so the error is evenly
distributed. When they aren't, **non-linear quantization** — e.g. a
**logarithmic** interval scale — does better.

For images the same applies per pixel: an 8-bit-per-pixel image quantized down
toward 1 bit per pixel visibly degrades.

### Bit rate

The **number of bits produced per second**, measured in bits/second. Critical
for storage and for transmission across networks of high, low or varying
bandwidth.

> The target: **just enough bit rate to convey the necessary information with
> minimal perceptual distortion, while minimising storage.**

## 5. Signals and systems

**Signal properties** that appear in combination: smooth · unsmooth ·
continuous · discontinuous · finite support · periodic.

**A system is any operation that transforms a signal.**

### Linear Time Invariant (LTI) systems

Understanding LTI systems is what lets you characterise how any practical system
performs sampling and digitization.

**Convolution** (`f * g`) — the result of taking the integral of the first
signal multiplied by the second signal **reversed and shifted**.

**The central result, stated two ways:**

| View | Characterised by | Relationship |
|---|---|---|
| **Time domain** | The **impulse response** | Output = input **convolved with** the impulse response |
| **Frequency domain** | The **transfer function** | Transfer function = **Fourier transform of the impulse response** |

Any LTI system is **fully characterised** by its impulse response. This
equivalence is a very likely exam question.

### Useful signals

Specific functions that recur in sampling, filtering and convolution:
**Delta · comb · step · box · sinc**.

**The Dirac Delta function**, introduced by the theoretical physicist **Paul
Dirac**: a sharp peak bounding **unit area** — zero everywhere except at
`x = 0`, where it is infinite, with an integral of **1**.

### The Fourier transform

Due to **Joseph Fourier (1768–1830)**, who published his initial results in
**1807**.

**The claim:** any periodic, continuous signal can be represented as a **sum of
individual sinusoids** — a *Fourier series expansion*. Equivalently, every
periodic continuous signal is a **weighted combination of sine and cosine
waves**.

The weights used to combine them are the **Fourier series coefficients**, also
called **spectral components**.

## 6. Sampling theorem and aliasing

### The core result

How many samples you need rises with the **frequency content** of the signal. A
signal that doesn't change (zero frequency) needs one sample; the next needs
two; a high-frequency one needs many.

**The Nyquist–Shannon sampling theorem** — established in the **late 1920s by
Henry Nyquist**, formalised by **Claude Shannon in 1950**:

> **A signal must be sampled at a frequency greater than twice the maximum
> frequency present in the signal.**

**Worked example:** a signal with a maximum frequency of **10 kHz** must be
sampled above **20 kHz**. That 20 kHz is the **Nyquist sampling frequency** for
this signal.

### Sampling too fast, and too slow

| | What happens |
|---|---|
| **Above Nyquist** (oversampling) | Nothing special — the signal reproduces correctly. But you generate **more data than necessary**, increasing storage and transmission overhead. |
| **Below Nyquist** (undersampling) | Frequency content is **not captured**. Converted back, the signal **does not match the original**. This is **aliasing**. |

> **Definition to memorise:** *aliasing* is the loss of information during
> digitization caused by sampling below the Nyquist rate.

### Spatial aliasing

Occurs in all dimensions. His 2D example starts from an image of **750 × 620
samples** and progressively reduces the sampling resolution in both directions —
as the number of spatial samples drops, the original frequencies are no longer
properly captured and the reconstruction degrades.

### Temporal aliasing — the wagon-wheel effect

The classic example, from western films: as a stagecoach starts moving its
wheels rotate forward as expected, but **as it speeds up the wheels appear to
rotate backwards**.

**Why:** the movie camera has **undersampled** the wheels' motion — the rotation
frequency exceeded half the frame rate, so the reconstructed motion is wrong.

---

## If you're revising this in 10 minutes

1. **Reflection / refraction / diffraction**, and that sound needs a medium.
2. **T = 1/f** and **λ = vT**, plus the five sine-wave properties.
3. **Sampling + quantization = A/D; interpolation = D/A.**
4. **Quantization always introduces error**; music 16 bits, speech 8 bits.
5. **Human hearing 20 Hz – 20 kHz**, audio sampled 8–48 kHz.
6. **Nyquist: sample at more than 2× the maximum frequency.** Know the 10 kHz → 20 kHz example, and what happens above and below.
7. **Aliasing** defined, plus one spatial and one temporal example (the wagon wheel).
8. **LTI systems**: impulse response ↔ transfer function via the Fourier transform.
9. **Fourier 1807**; **Nyquist late 1920s**; **Shannon 1950**; **Dirac delta**.
