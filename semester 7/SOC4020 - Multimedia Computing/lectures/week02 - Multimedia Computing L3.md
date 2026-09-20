# L3 — SNR, Audio Filtering, MIDI & Audio Coding

**SOC4020 · Week 2 · 47 slides · Dr. Minhaz Uddin Ahmed**
Source: [week02 - Multimedia Computing L3.pptx](week02%20-%20Multimedia%20Computing%20L3.pptx)
Practice code: [practice code L3.rar](../resources/practice%20code%20L3.rar)
Reference: textbook **Chapter 6**

**Contents:** SNR · SQNR · audio filtering · audio quality vs data rate ·
synthetic sounds · MIDI · MIDI hardware · coding of audio · PCM.

Opens by re-showing the temporal aliasing slide from
[L2](week01%20-%20Multimedia%20Computing%20L2.md) — the wagon-wheel effect.

---

## 1. Signal-to-Noise Ratio (SNR)

In any analog system, **random fluctuations add noise** to the signal, so the
measured voltage is wrong.

> **SNR = the ratio of the power of the correct signal to the power of the
> noise.** It is a measure of signal quality.

Measured in **decibels (dB)**, defined via base-10 logarithms of squared values.

**Units:** a **bel** measures sound intensity and equals **10 decibels**, so
1 dB is one tenth of a bel.

**The key relationship:** signal **power is proportional to the square of the
voltage**. That's where the factor of 20 comes from:

```
if V_signal = 10 × V_noise    →    SNR = 20 · log₁₀(10) = 20 dB
```

**Worth knowing:** decibel figures for everyday sounds are quoted relative to a
**just-audible sound at 1 kHz** — i.e. as a ratio against the quietest sound a
human can hear.

## 2. Signal-to-Quantization-Noise Ratio (SQNR)

For *digital* signals there is a second error source beyond analog noise:
**only quantized values are stored**.

If voltages range 0–1 but you have only 8 bits, every continuous value is forced
into one of **256** possible values. That roundoff is **quantization error**,
usually called **quantization noise** — not really noise, but named so because
the errors occur essentially **randomly from sample to sample**.

> **Definition:** quantization noise is the difference between the analog signal
> value at the sampling instant and the nearest quantization interval value.
> **At most this error is half the interval.**

**The formula — memorise it:**

```
SQNR = 6.02·N + 1.76   (dB)        where N = bits per sample
```

**So each bit adds roughly 6 dB of resolution**, which gives:

| Bits | Max SQNR |
|---|---|
| 8 | ≈ 50 dB |
| **16** | **≈ 96 dB** |

The 16-bit → 96 dB figure is the one he states explicitly, and it's the obvious
exam question.

**The assumptions behind it:** the input signal is sinusoidal, the quantization
error is statistically independent, and its magnitude is uniformly distributed
between 0 and half the interval. Larger SQNR is better.

## 3. Audio filtering

Signals are filtered to remove unwanted frequencies; **which ones you keep
depends on the application**.

| Application | Range retained |
|---|---|
| **Speech** | 50 Hz – 10 kHz |
| **Music** | ~20 Hz – 20 kHz |

Done with a **bandpass filter** (also called a band-limiting filter), which
screens out both lower and higher frequencies.

**The subtlety worth understanding:** even though high frequencies were removed
at the encoder, they **reappear in the output** at the DA converter — a
consequence of sampling and quantization. So at the decoder a **low-pass
filter** is applied after the DA circuit, using **the same cutoff** as the
high-frequency end of the encoder's bandpass filter.

## 4. Audio quality vs data rate

- Uncompressed data rate **rises as more bits are used** for quantization.
- **Stereo doubles the bitrate** compared with mono.

**A terminology trap he flags:**

| Field | "Bandwidth" means |
|---|---|
| Analog devices | A **frequency range**, in Hertz (cycles per second) |
| Computer networking | A **data rate**, in bits per second |

**Standard audio sampling frequencies**, supported by most sound cards, as
printed on the slide: **5.0125 kHz, 11.025 kHz, 22.05 kHz, 44.1 kHz**.
*(The usual low-end value in this series is 8 kHz — treat the first figure with
mild suspicion, but reproduce the slide's version if asked.)*

## 5. Synthetic sounds

Digitized sound must be converted back to analog before we can hear it. **Two
fundamentally different approaches** to handling stored sampled audio:

1. **FM — frequency modulation.** The audio signal is encoded on the carrier frequency. (FM broadcast stations operate in the **88–108 MHz** band.)
2. **Wave Table** (or just *Wave*) sound.

## 6. MIDI

**Musical Instrument Digital Interface**, dating from the **early 1980s**. A
protocol adopted by the electronic music industry so that computers,
synthesizers, keyboards and other musical devices can communicate.

> **The central idea:** MIDI is a **scripting language**. It codes *events* that
> stand for the production of sounds — a note's pitch, its volume, which
> instrument to play — rather than the sound itself. **That is why MIDI files
> are tiny.**

**The size comparison to memorise:**

| Format | Storage |
|---|---|
| **MIDI** | ~**3 minutes** of music in about **3 kB** |
| **WAV** (wave table) | **1 minute** of music in about **10 MB** |

**What it's good for:** inventing, editing and exchanging musical ideas
encapsulated as notes; music that can then be altered by the user; and music
education, since it ties closely to composition programs.

**Master–slave control.** One MIDI instrument can control others. His example:
a keyboard that *plays* like a traditional instrument but has a poor built-in
synthesizer can be **daisy-chained** to a better sound module. Because MIDI
carries a **built-in timecode**, the master's clock synchronises all the slaves.

A **sequencer-sampler** reorders and manipulates sets of digital-audio samples
and/or MIDI sequences. In a Digital Audio Workstation (e.g. ProTools),
multitrack recording is possible — sequential or concurrent, such as 8 vocal
tracks and 8 instrument tracks at once.

### MIDI concepts

- Music is organised into **tracks** in a sequencer; each can be switched on or off for recording or playback.
- An instrument is associated with a **MIDI channel**; channels separate messages.
- **There are 16 channels, numbered 0–15.** The channel occupies the **last four (least significant) bits** of the status byte.
- Conventionally channel 1 is piano and **channel 10 is drums** — but you can switch instruments midstream.
- **System messages** carry no channel number and address all instruments — e.g. a change in tuning or timing.
- An instrument simply **ignores any "play sound" message not on its channel**. If several messages arrive for its channel (simultaneous notes), it responds provided it is **multi-voice**.

### Terminology — this cluster is very exam-shaped

| Term | Meaning |
|---|---|
| **Synthesizer** | A stand-alone sound generator that can vary **pitch, loudness and tone colour**. Good ones have a microprocessor, keyboard, control panels and memory. |
| **Tone / sound module** | Any unit that generates sound |
| **Sequencer** | Originally hardware for storing and editing a sequence of musical events as MIDI data; now usually software |
| **MIDI keyboard** | **Produces no sound** — generates sequences of MIDI instructions (messages). May also contain a synthesizer. |
| **Timbre** | The **quality** of the sound — what instrument is being emulated, piano vs violin |
| **Multi-timbral** | Able to play **many different sounds** at once (piano, brass, drums) |
| **Voice** | In MIDI: every different **timbre *and* pitch** a tone module can produce simultaneously. Synths have 16, 32, 64, 256… |
| **Polyphony** | The **number of voices** producible at the same time |

His worked phrasing: a typical tone module might offer **"64 voices of
polyphony"** (64 notes at once) while being **"16-part multi-timbral"** (16
different instruments at once). Being able to explain that sentence is a very
likely exam question.

### MIDI specifics

- A **patch** is the set of control settings defining a particular timbre. Patches are organised into databases called **banks**.
- **General MIDI** is the standard mapping of patches to channels, so that patch 1 is always a piano. It defines **128 patches** for standard instruments, with **channel 10 reserved for percussion**, and a standard percussion map of **47 percussion sounds** — where the note sits on the score determines which element is struck.
- **A General MIDI device must:** support all 16 channels · be multi-timbral · be polyphonic · have a **minimum of 24 dynamically allocated voices**.

**Byte structure:**

| | Range |
|---|---|
| **Status byte** | 128 – 255 (MSB = 1) |
| **Data byte** | 0 – 127 (MSB = 0) |

Actual MIDI bytes are **8 bits plus a 0 start and a stop bit — 10-bit
"bytes"**.

**Programmability:** filters to change bass and treble response, and to change
the **envelope** describing how a sound's amplitude varies over time.

**Sequencer techniques for getting more music from less:** looping over a few
bars · **time-varying amplitude modulation** (volume shaped over time) · and
**time compression or expansion with no pitch change**.

**Multisampling** — shifting a sampled instrument's pitch sounds bad over large
key changes, so a sound is recorded through **several bandpass filters** and the
recordings assigned to different keyboard keys. Less shift per note, better
result.

**MIDI Machine Control (MMC)** — a subset of the spec for controlling recording
equipment such as multitrack recorders; most commonly used to remotely press
"Play". More broadly, MIDI can synchronise instruments and recording equipment
and even **control theatre lighting**.

### Message structure — two types

**1. Channel messages.** Up to 3 bytes. The first is the **status byte** with
its most significant bit set to **1**; the four low-order bits identify the
channel and the remaining three hold the message. Data bytes have MSB **0**.

**2. Voice messages.** A channel message that controls a voice — which note to
play or turn off, and key pressure. Also used for controller effects:
**sustain, vibrato, tremolo, pitch wheel**.

### Hardware

- **31.25 kbps serial connection**, with 10-bit bytes (0 start and stop bit).
- MIDI units are usually **either input or output devices, not both**.
- **Communication is half-duplex.**
- Physical ports are **5-pin connectors labelled IN and OUT**, plus optionally **THRU**, which simply copies the data entering IN.
  - **IN** — receives all MIDI data
  - **OUT** — transmits data the device generates itself
  - **THRU** — passes IN through unchanged, for daisy-chaining
- On a traditional synthesizer, the **modulation wheel adds vibrato** and **pitch bend alters frequency**, like bending a guitar string.

**Typical setup:** keyboard OUT → synthesizer IN → **THRU** → each additional
sound module. Recording: the keyboard sends messages to the sequencer.
Playback: the sequencer sends to all sound modules and the synthesizer.

### Why 31.25 kbps is restrictive — the worked example

Playing one note takes a **3-byte message**. A ten-finger chord is ten notes at
**30 bits each = 300 bits**. At 31.25 kbps that takes about **0.01 seconds**
(~0.001 s per note) — **and that's before the ten note-off messages**. Pitch
bend and modulation wheels generate many more messages on top.

### MIDI-to-WAV conversion

Some software (he cites early Adobe Premiere) refuses MIDI and requires WAV.
Shareware converters use large lookup files substituting predefined or shifted
WAV output for MIDI messages, **with inconsistent success**.

## 7. Coding of audio

**Quantization and transformation of data are together known as *coding*.**

For audio, the **µ-law technique for companding** is usually combined with a
simple algorithm exploiting the **temporal redundancy** present in audio
signals.

### The three stages of every compression scheme

This is the most exam-shaped item in the deck, and it recurs in the compression
lectures later in the course:

| Stage | What happens |
|---|---|
| **1. Transformation** | Input data is converted to a representation that is easier or more efficient to compress. Example: **predictive coding** — predict the next signal from previous ones and transmit only the **prediction error**. |
| **2. Loss** | Information may be discarded. **Quantization is the main lossy step** — using fewer reconstruction levels than the original necessarily loses information. |
| **3. Coding** | Assign a **codeword** to each output level or symbol, forming a binary bitstream. Either fixed-length, or variable-length such as **Huffman coding**. |

---

## If you're revising this in 10 minutes

1. **SNR** definition and the `20·log₁₀` example (power ∝ voltage²).
2. **SQNR = 6.02N + 1.76 dB**, ~6 dB per bit, **16 bits → 96 dB**, and that quantization error is at most half an interval.
3. **Speech 50 Hz–10 kHz, music 20 Hz–20 kHz**, bandpass at the encoder, low-pass at the decoder with the same cutoff.
4. **MIDI is events, not audio** — hence 3 kB vs 10 MB.
5. **16 channels, channel 10 = percussion, 128 General MIDI patches, minimum 24 voices.**
6. **Timbre / multi-timbral / voice / polyphony** — be able to explain "64 voices of polyphony, 16-part multi-timbral".
7. **IN / OUT / THRU**, half-duplex, 31.25 kbps, and the 300-bit chord example.
8. **The three stages of any compression scheme.**
