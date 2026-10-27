# Midterm practice: L2 + L3 (audio)

Sound, sampling, aliasing, quantization, bit rate (L2) and SNR, SQNR, filtering,
data rate, MIDI, audio coding (L3). Every number below was checked in Python.

Attempt each problem before opening the solution. Problems 1-9 copy the
professor's own examples and tables; 10-16 combine them.

---

## Formula sheet

| What | Formula | Units / notes | Source |
|---|---|---|---|
| Period / frequency | **T = 1 / f** | T in s, f in Hz (cycles/s) | L2 S16, S21 |
| Wavelength | **λ = v · T = v / f** | λ in m, v in m/s (sound in air ≈ 340 m/s) | L2 S26 |
| Sampling | **x_s(n) = x(nT)**, f = 1/T | T = sampling period, f = sampling frequency | L2 S19 |
| Nyquist | **f_s > 2 · f_max** | 2·f_max is the "Nyquist sampling frequency" | L2 S47-48 |
| Quantization | **x_q(n) = Q[x_s(n)]**, Q = rounding | | L2 S29 |
| Levels | **N = 2^b** | b = bits per sample (here N means *levels*) | L2 S29 |
| Step size | **Δ = R / 2^b** | R = full range of the signal (e.g. volts) | L2 S29 |
| Max quantization error | **Δ / 2** | "at most half of the interval" | L3 S8 |
| Bit rate | **bit rate = sampling rate × bits per sample** (× channels) | bits/s; stereo doubles it | L2 S34, L3 S11 |
| File size | **size = bit rate × duration / 8** | bytes; 1 kB = 1000 B, 1 MB = 10^6 B on these slides | |
| SNR (voltages) | **SNR = 20 · log₁₀(V_signal / V_noise)** dB | power ∝ voltage², so 20 for voltage ... | L3 S6 |
| SNR (powers) | **SNR = 10 · log₁₀(P_signal / P_noise)** dB | ... and 10 for power | L3 S4 |
| bel | 1 bel = 10 dB | | L3 S4 |
| SQNR (derivation) | **20 · log₁₀(2^(N-1) / ½) = 20 · N · log₁₀2 = 6.02 N** dB | here **N = bits per sample** | L3 S9 |
| SQNR (sine input) | **SQNR = 6.02 N + 1.76** dB | "each bit adds about 6 dB"; 16 bits → 96 dB | L3 S9 |
| MIDI byte on the wire | 8 data bits + 0 start bit + stop bit = **10 bits** | | L3 S25, S31 |
| MIDI link | **31.25 kbps** = 31 250 bit/s, half-duplex | | L3 S31 |
| MIDI note message | 3 bytes = **30 bits** on the wire | time = bits / 31 250 | L3 S34 |
| MIDI status / data byte | status **128-255** (MSB = 1), data **0-127** (MSB = 0) | low 4 bits of status = channel 0-15 | L3 S25, S35 |
| Voice-message status bytes | Note off **8n**, Note on **9n**, Poly pressure An, Control change Bn, Program change Cn, Channel pressure Dn, Pitch bend En | n = channel (hex) | L3 S37 (Table 6.3) |

**Numbers to know by heart:** hearing 20 Hz-20 kHz · voice ≈ 4 kHz · audio sampled
8-48 kHz · music 16 bits, speech 8 bits · speech filter 50 Hz-10 kHz, music
20 Hz-20 kHz · 16 MIDI channels (0-15), channel 10 = drums · General MIDI: 128
patches, 47 percussion sounds, ≥ 24 voices · MIDI 3 min ≈ 3 kB vs WAV 1 min ≈ 10 MB.

**Professor's bit-rate table (L2 S35):**

| Signal | Sampling rate | Bits/sample | Bit rate |
|---|---|---|---|
| Speech | 8 kHz | 8 | 64 kbps |
| Audio CD | 44.1 kHz | 16 | 706 kbps mono, 1.4 Mbps stereo |
| Teleconferencing | 16 kHz | 16 | 256 kbps |
| AM radio | 11 kHz | 8 | 88 kbps |
| FM radio | 22 kHz | 16 | 352 kbps mono, 704 kbps stereo |

**Table 6.2 (L3 S11) is in kB/s, meaning bytes:** telephone 8 kB/s, AM 11.0 kB/s,
FM 88.2 kB/s, CD 176.4 kB/s, DVD audio up to 1200 kB/s.

---

## Part A: the professor's own examples

### Problem 1: Nyquist rate (L2 S48)

A signal's highest frequency component is 10 kHz.
(a) What is its Nyquist sampling frequency? (b) What is the largest sampling
period T that still avoids aliasing? (c) If it is sampled at 48 kHz instead,
what happens?

<details><summary>Solution</summary>

(a) f_s > 2 × f_max = 2 × 10 kHz → **Nyquist sampling frequency = 20 kHz**; the signal must be sampled at more than 20 kHz.

(b) T = 1 / f_s = 1 / 20 000 Hz = 0.00005 s → **T must be less than 50 µs**.

(c) 48 kHz > 20 kHz is **oversampling: nothing special happens**. The signal is reproduced correctly, but you store and transmit **more data than necessary** (48/20 = 2.4 times the minimum).

**Trap:** the theorem says *greater than* twice f_max, not "at least". Also, 20 kHz is the Nyquist *sampling frequency*, not the signal's maximum frequency.
</details>

### Problem 2: Period and wavelength (L2 S21, S26)

A 500 Hz tone travels through air at v = 340 m/s. Find its period and wavelength.

<details><summary>Solution</summary>

T = 1 / f = 1 / 500 = **0.002 s = 2 ms**

λ = v · T = 340 × 0.002 = **0.68 m**

**Trap:** λ = v·T (multiply by the period), equivalently v / f. Students often write v·f = 170 000 m, which is absurd for a sound wave.
</details>

### Problem 3: Bit rates from the professor's table (L2 S34-S35)

Compute the bit rate of: (a) telephone speech, 8 kHz, 8 bits, mono; (b) audio CD,
44.1 kHz, 16 bits, mono and stereo; (c) teleconferencing, 16 kHz, 16 bits;
(d) AM radio, 11 kHz, 8 bits.

<details><summary>Solution</summary>

Bit rate = sampling rate × bits per sample × channels.

(a) 8000 × 8 = **64 000 bit/s = 64 kbps**

(b) mono: 44 100 × 16 = **705 600 bit/s ≈ 706 kbps**; stereo: × 2 = **1 411 200 bit/s ≈ 1.4 Mbps**

(c) 16 000 × 16 = **256 000 bit/s = 256 kbps**

(d) 11 000 × 8 = **88 000 bit/s = 88 kbps**

**Trap:** forgetting × 2 for stereo. The slides say "stereo doubles the bitrate".
</details>

### Problem 4: Quantization levels and step size (L2 S29-S31)

An audio signal spans a range R = 2 V (from -1 V to +1 V).
(a) How many levels, and what step Δ, with b = 8, 4 and 3 bits?
(b) What is the maximum quantization error with b = 3?
(c) With b = 3 and rounding to the nearest multiple of Δ, what is stored for a
sample of 0.30 V, and what is the error?

<details><summary>Solution</summary>

N = 2^b and Δ = R / 2^b.

(a)
| b | Levels N = 2^b | Δ = 2 V / N |
|---|---|---|
| 8 | 256 | 0.0078125 V ≈ 7.8 mV |
| 4 | 16 | 0.125 V |
| 3 | 8 | **0.25 V** |

(b) Max error = Δ / 2 = 0.25 / 2 = **0.125 V**

(c) The nearest multiples of 0.25 V are 0.25 and 0.50; 0.30 is closer to 0.25. Stored **0.25 V**, error **0.05 V** (below the 0.125 V bound).

**Trap:** every extra bit *halves* Δ; it does not reduce Δ by a fixed amount. And quantization *always* introduces some error (L2 S31).
</details>

### Problem 5: SNR in decibels (L3 S6)

(a) The signal voltage is 10 times the noise voltage. What is the SNR?
(b) V_signal = 5 V and V_noise = 0.05 V. SNR?
(c) A system has an SNR of 60 dB. What are the voltage ratio and the power ratio?

<details><summary>Solution</summary>

Power ∝ V², so SNR = 10·log₁₀(P_s/P_n) = 20·log₁₀(V_s/V_n).

(a) 20 × log₁₀(10) = 20 × 1 = **20 dB** (the professor's own example)

(b) V_s/V_n = 5 / 0.05 = 100 → 20 × log₁₀(100) = 20 × 2 = **40 dB**

(c) 60 = 20·log₁₀(V ratio) → log₁₀ = 3 → **voltage ratio = 1000**; 60 = 10·log₁₀(P ratio) → **power ratio = 10^6**

**Trap:** using 10·log for a voltage ratio. Voltages (and amplitudes, pressures) use **20**, powers (and intensities) use **10**.
</details>

### Problem 6: SQNR and the 6 dB-per-bit rule (L3 S9)

(a) Using SQNR = 20·log₁₀(2^(N-1) / ½), show that SQNR ≈ 6.02 N dB.
(b) Compute the maximum SQNR for 8-bit and 16-bit audio with 6.02 N, and with
6.02 N + 1.76.

<details><summary>Solution</summary>

(a) 2^(N-1) / ½ = 2^(N-1) × 2 = 2^N, so SQNR = 20·log₁₀(2^N) = 20 · N · log₁₀2 = 20 × 0.30103 × N = **6.02 N dB**.

(b)
| N | 6.02 N | 6.02 N + 1.76 |
|---|---|---|
| 8 | **48.16 dB** | **49.92 dB** (≈ 50 dB) |
| 16 | **96.32 dB** (the slide's "96 dB") | **98.08 dB** |

**Trap:** in this formula N is the number of *bits*, while on L2 S29 N = 2^b is the number of *levels*. Do not plug 256 into 6.02 N.
</details>

### Problem 7: The MIDI chord (L3 S34)

MIDI runs at 31.25 kbps; each byte is sent as 10 bits; a Note On message is 3 bytes.
(a) How long does a ten-finger chord take to start?
(b) How long per note?
(c) How long until all ten notes have been both started and stopped?

<details><summary>Solution</summary>

One message = 3 bytes × 10 bits = 30 bits. Ten notes = 300 bits.

(a) 300 / 31 250 = **0.0096 s ≈ 0.01 s**

(b) 30 / 31 250 = **0.00096 s ≈ 0.001 s (about 1 ms)**

(c) Ten Note On + ten Note Off = 600 bits → 600 / 31 250 = **0.0192 s ≈ 0.02 s**

**Trap:** using 8 bits per byte (gives 240 bits, 7.68 ms). On the MIDI wire a byte is **10 bits** (0 start bit + 8 data + stop bit).
</details>

### Problem 8: MIDI vs WAV storage (L3 S21)

The slide says 3 minutes of MIDI ≈ 3 kB and 1 minute of WAV ≈ 10 MB.
(a) Check the 10 MB figure for CD-quality WAV (44.1 kHz, 16 bits, stereo).
(b) How many times larger is a 3-minute CD-quality WAV than the 3 kB MIDI file?

<details><summary>Solution</summary>

(a) 44 100 × 16 × 2 = 1 411 200 bit/s; × 60 s = 84 672 000 bits; ÷ 8 = **10 584 000 bytes ≈ 10.6 MB**. That matches "about 10 MB".

(b) 3 minutes = 3 × 10 584 000 = 31 752 000 bytes; ÷ 3000 = **10 584 times larger** (about 10 000×).

**Trap:** MIDI is small because it stores *events* (note, volume, instrument), not samples. Its size does not depend on sampling rate at all.
</details>

### Problem 9: Decoding a MIDI message (L3 S25, S35, Table 6.3)

A MIDI device receives the bytes `93 3C 64` (hex).
(a) Which is the status byte and how do you know?
(b) What message is it, and on which channel?
(c) What do the two data bytes mean (in decimal)?

<details><summary>Solution</summary>

(a) 0x93 = 147, in 128-255 and its MSB is 1 (1001 0011), so **0x93 is the status byte**. 0x3C = 60 and 0x64 = 100 are in 0-127 (MSB 0), so they are data bytes.

(b) The high nibble 9 = **Note On**; the low 4 bits 0011 = **channel n = 3** (channel number 3 on the 0-15 scale, i.e. the 4th channel).

(c) Data byte 1 = key number **60**, data byte 2 = Note On velocity **100**.

**Trap:** "channel 10 = drums" counts channels from 1; in the status byte the drums are n = 9 (0x99 for Note On). Also, a byte of 0x80 or more is never data.
</details>

---

## Part B: combined and harder problems

### Problem 10: Which components survive sampling?

x(t) = sin(2π·1000 t) + sin(2π·3500 t) is sampled at 5 kHz.
(a) What is the Nyquist sampling frequency for x(t)?
(b) Is the signal aliased? What frequencies appear after reconstruction?

<details><summary>Solution</summary>

(a) f_max = 3500 Hz → Nyquist = 2 × 3500 = **7 kHz**; sample above 7 kHz.

(b) 5 kHz < 7 kHz → **aliased**. Only frequencies up to f_s/2 = 2.5 kHz can be represented. 1000 Hz is fine. 3500 Hz folds back to |3500 - 5000| = **1500 Hz**. Reconstruction contains **1000 Hz and 1500 Hz**, which does not match the original.

**Trap:** the alias rule f_alias = |f - k·f_s| (k chosen so the result is ≤ f_s/2) is standard, not on the slides; the slide only demands the definition (loss of information from sampling below Nyquist), so state that too.
</details>

### Problem 11: Aliased frequency of a single tone

Find the frequency heard after reconstruction for: (a) 7 kHz sampled at 10 kHz;
(b) 9 kHz sampled at 8 kHz; (c) 25 kHz sampled at 44.1 kHz.

<details><summary>Solution</summary>

Folding frequency = f_s / 2. f_alias = |f - k·f_s|, nearest multiple k.

(a) 7 > 5 → |7 - 10| = **3 kHz**

(b) 9 > 4 → |9 - 8| = **1 kHz**

(c) 25 > 22.05 → |25 - 44.1| = **19.1 kHz** (still audible, which is why music is band-limited to 20 kHz *before* sampling)

**Trap:** students subtract f_s/2 instead of f_s (7 - 5 = 2 kHz is wrong).
</details>

### Problem 12: Bits needed for a given step size

A sensor outputs 0-5 V. You need Δ ≤ 1 mV. Minimum number of bits? Actual Δ?
Maximum quantization error?

<details><summary>Solution</summary>

Δ = R / 2^b ≤ 0.001 → 2^b ≥ 5 / 0.001 = 5000. 2^12 = 4096 (too small), 2^13 = 8192.

**b = 13 bits**, Δ = 5 / 8192 = **0.61 mV**, max error = Δ/2 ≈ **0.31 mV**.

**Trap:** log₂(5000) = 12.29 must be rounded *up*; 12 bits gives Δ = 1.22 mV, which fails.
</details>

### Problem 13: File size and storage

(a) Size in bytes and MB of a 3-minute CD-quality stereo song (44.1 kHz, 16 bits)?
(b) How many minutes of this audio fit on a 700 MB disc (1 MB = 10^6 bytes)?
(c) How large is 1 hour of telephone-quality audio (8 kHz, 8 bits, mono)?

<details><summary>Solution</summary>

(a) 1 411 200 bit/s × 180 s = 254 016 000 bits ÷ 8 = **31 752 000 bytes ≈ 31.75 MB** (≈ 30.3 MiB if 1 MB = 2^20).

(b) Bytes per second = 1 411 200 / 8 = 176 400 B/s (Table 6.2's 176.4 kB/s). 700 × 10^6 / 176 400 = 3968 s = **≈ 66.1 minutes**.

(c) 64 000 bit/s = 8000 B/s; × 3600 s = **28 800 000 bytes = 28.8 MB**.

**Trap:** bits vs bytes. Table 6.2 lists **kB/s (bytes)** while L2's table lists **kbps (bits)**: CD = 176.4 kB/s = 1411.2 kbps. Divide by 8 once, not twice.
</details>

### Problem 14: Choosing bits from an SQNR target

A recording system must reach SQNR ≥ 75 dB.
(a) Minimum bits per sample with 6.02 N? With 6.02 N + 1.76?
(b) How many dB do you gain by going from 8 to 12 bits?

<details><summary>Solution</summary>

(a) 6.02 N ≥ 75 → N ≥ 12.46 → **N = 13** (78.26 dB).
6.02 N + 1.76 ≥ 75 → N ≥ 12.17 → **N = 13** (80.02 dB). Both give 13 bits.

(b) 4 extra bits × 6.02 = **24.08 dB** (48.16 → 72.24 dB).

**Trap:** always round bits *up*, and each bit adds ~6 dB (not 3 dB, which is doubling *power*).
</details>

### Problem 15: Design a digital music recorder

Music occupies 20 Hz-20 kHz and must have SQNR ≥ 75 dB (6.02 N rule), stereo.
(a) Minimum sampling frequency? Which standard rate would you pick?
(b) Bits per sample (from Problem 14)?
(c) Bit rate at the chosen rate, and storage for 10 minutes?
(d) Which filters go before the ADC and after the DAC?

<details><summary>Solution</summary>

(a) f_s > 2 × 20 kHz = **40 kHz**. Pick the standard **44.1 kHz** (L3 S12 list).

(b) **13 bits** (6.02 × 13 = 78.26 dB ≥ 75).

(c) 44 100 × 13 × 2 = **1 146 600 bit/s ≈ 1.15 Mbps**; × 600 s ÷ 8 = **85 995 000 bytes ≈ 86 MB**.

(d) Before the ADC: a **band-pass (band-limiting) filter** keeping 20 Hz-20 kHz. After the DAC: a **low-pass filter with the same 20 kHz cutoff**, because high frequencies reappear through sampling and quantization (L3 S10).

**Trap:** forgetting the 2 channels, or using the music range (20 kHz) as the sampling rate instead of doubling it.
</details>

### Problem 16: Sound levels and decibel arithmetic (L3 S5)

Using the slide's table (conversation 60 dB, loud radio 80 dB, threshold of pain 140 dB):
(a) How many times more intense (power) is a loud radio than conversation? Pressure (amplitude) ratio?
(b) What happens to the dB value if the signal voltage doubles? If power doubles?

<details><summary>Solution</summary>

(a) Difference 20 dB. Power: 10^(20/10) = **100×**. Pressure/voltage: 10^(20/20) = **10×**.

(b) Voltage ×2: 20·log₁₀2 = **+6.02 dB**. Power ×2: 10·log₁₀2 = **+3.01 dB**.

**Trap:** decibels are relative to a just-audible 1 kHz sound (0 dB), not to silence; 0 dB does not mean "no sound".
</details>

### Problem 17: MIDI bandwidth limits

(a) What is the maximum number of 3-byte MIDI messages per second on a 31.25 kbps link?
(b) A pianist plays a 6-note chord and releases it. How long does it take to send all messages?
(c) Write the status byte for "Program change on channel n = 5" and for "Note On on the drum channel (channel 10 counting from 1)".

<details><summary>Solution</summary>

(a) 31 250 / 30 = 1041.7 → **1041 complete messages per second**.

(b) 6 Note On + 6 Note Off = 12 × 30 = 360 bits → 360 / 31 250 = **0.01152 s ≈ 11.5 ms**.

(c) Program change = Cn → **0xC5** (= 197). Drum channel = n 9 → Note On **0x99** (= 153).

**Trap:** pitch-bend and modulation wheels add many more messages (L3 S34), so the real limit is lower.
</details>

### Problem 18: Wagon wheel (temporal aliasing, L2 S55)

A film camera runs at 24 frames/s. A stagecoach wheel has 6 identical spokes
and turns at 3.5 rev/s. What does the audience see?

<details><summary>Solution</summary>

The pattern repeats every spoke, so the pattern frequency = 6 × 3.5 = 21 Hz.
Nyquist limit of the camera = 24 / 2 = 12 Hz. 21 > 12 → **undersampled**.

Apparent frequency = 21 - 24 = **-3 Hz**: the spoke pattern appears to move *backwards* at 3 spoke-steps per second = 3 / 6 = **0.5 rev/s backwards**.

**Trap:** using the rotation rate (3.5 Hz, well below 12) instead of the spoke rate. The professor's explanation: "the movie camera has under sampled the wheels' motion".
</details>

---

## Part C: short explain/compare questions

**C1. What happens when you sample above vs below the Nyquist frequency?**
Above: nothing special, the signal is reproduced exactly, but you produce more
data than needed, raising storage and transmission overhead. Below: not all
frequency content is captured, so the reconstructed signal differs from the
original. That loss of information is called aliasing (spatial example: reducing
a 750 × 620 image; temporal example: the wagon wheel turning backwards).

**C2. How is an LTI system characterised in the time and frequency domains?**
Any LTI system is fully characterised by its impulse response. In the time
domain the output is the input convolved with the impulse response. In the
frequency domain it is described by the transfer function, which is the Fourier
transform of the impulse response.

**C3. Explain "64 voices of polyphony, 16-part multi-timbral". Why are MIDI files small?**
Polyphony is the number of voices (notes of any timbre and pitch) played at the
same time, so 64 notes at once. Multi-timbral means playing different instrument
sounds simultaneously, so 16 instruments at once. MIDI files are small because
MIDI is a scripting language: it stores events (pitch, volume, instrument), not
sampled audio, so 3 min ≈ 3 kB versus 1 min of WAV ≈ 10 MB.

**C4. Why is a low-pass filter used after the DAC, and what are the three stages of a compression scheme?**
High frequencies removed by the encoder's band-pass filter reappear at the DAC
output because of sampling and quantization, so a low-pass filter with the same
cutoff as the encoder's upper band edge removes them. Compression stages:
(1) transformation (e.g. predictive coding sends the prediction error), (2) loss
(quantization is the main lossy step), (3) coding (fixed-length or variable-length
codewords such as Huffman).

---

## Most likely on the exam

1. **Bit rate and file size** (sampling rate × bits × channels, then ÷ 8): his table is on the slides and is the easiest thing to turn into a 10-point problem.
2. **SNR / SQNR in dB**: 20·log₁₀ of a voltage ratio (his 20 dB example) and 6.02 N (+1.76), including "how many bits for X dB".
3. **Nyquist / aliasing**: minimum sampling rate for a given f_max, plus what happens above and below; possibly an aliased-frequency calculation.

Also worth a look: the MIDI 31.25 kbps chord timing (Problem 7) and quantization
levels and step size (Problem 4).
