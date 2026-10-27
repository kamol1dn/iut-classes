# L4–L5 Compression: formula sheet and worked problems

Multimedia Computing midterm, Wed 2026-10-28. Covers **L4** (RLC, entropy, Shannon-Fano, Huffman, extended Huffman, LZW) and **L5** (arithmetic coding, quantization, audio data rate, MPEG audio bit allocation).

Part 2 of the exam is 8 problems × 10 points, so most of this file is problems to solve by hand. Try each one before you open the solution. Every number below was checked in Python.

The first problems use the professor's own slide examples (HELLO, LZW `ABABBABCABABBA`, arithmetic `CAEE$`). If one of those comes up, the slide's numbers are the expected answer.

---

## Formula and procedure sheet

### Numbers to remember

| | |
|---|---|
| log₂3 = 1.585 | log₂5 = 2.322 |
| log₂7 = 2.807 | log₂10 = 3.322 |
| log₂11 = 3.459 | log₂(1/p) = −log₂p |

Change of base with a basic calculator: **log₂x = ln x / ln 2 = log₁₀x / 0.3010**.

### Definitions

| Quantity | Formula | Note |
|---|---|---|
| Self-information of sᵢ | **log₂(1/pᵢ)** bits | the ideal code length for that symbol |
| Entropy | **η = Σ pᵢ log₂(1/pᵢ)** bits/symbol | the lower bound for any lossless code |
| Uniform source, n symbols | η = log₂n | 256 grey levels gives 8 bits |
| Average code length | **L̄ = Σ pᵢ·lᵢ** (or total bits ÷ number of symbols) | lᵢ = length of codeword i |
| Huffman bound | **η ≤ L̄ < η + 1** | slide 30, Eq. 7.6 |
| Extended Huffman, k symbols per group | η ≤ L̄ < η + 1/k bits per symbol | alphabet grows to nᵏ |
| Coding efficiency | η / L̄ (× 100%) | not on the slides, but a common follow-up question |
| Redundancy | L̄ − η | |
| Compression ratio | **B₀ / B₁** (bits before ÷ bits after) | should be ≫ 1 |
| Fixed-length code | ⌈log₂n⌉ bits per symbol | the baseline Huffman is compared against |
| Audio data rate | **sampling rate × bits per sample × channels** | CD: 44 100 × 16 × 2 = 1 411 200 bit/s |
| SNR per bit | about **6 dB per bit** (6.02N dB) | 16 bits ≈ 96 dB |
| MPEG bit allocation | **MNR = SNR − SMR** | give the next bit to the sub-band with the **lowest** MNR |

### Run-length coding (RLC)
Replace every run with **count + symbol**: `BBBBEEEEEEEECCCCDAAAAA → 4B8E4C1D5A`. It only helps when the data has long runs. On data with no runs it doubles the size.

### Shannon-Fano (top-down)
1. Sort the symbols by count.
2. Split the list into two groups whose total counts are **as equal as possible**. The left group gets 0 and the right group gets 1.
3. Repeat inside each group until every group has one symbol. The result is not unique, because different splits are allowed.

### Huffman (bottom-up)
1. List the symbols with their counts or probabilities.
2. Take the **two smallest**, make them children of a new parent whose count is **their sum**, and put the parent back in the list.
3. Repeat until one node is left (the root).
4. Label each branch 0/1 and read every code from the root down to the leaf.
5. Check: no code is a prefix of another, the two rarest symbols have equal length, and L̄ is within [η, η+1).

> **Ties:** when two counts are equal you may pick either. Different picks give **different codes and even different code lengths**, but **the same L̄**. Every such tree is optimal.

### LZW encoder (Algorithm 7.2)
```
s = first char
for each next char c:
    if s+c in dictionary: s = s+c
    else: output code(s); add s+c as new code; s = c
output code(s)
```
Table columns: **s | c | output | code | string**.

### LZW decoder (Algorithm 7.4, with the exception handler)
```
s = NIL
for each code k:
    entry = dict[k]
    if entry missing: entry = s + s[0]     ← exception (code was made in the step just before)
    output entry
    if s != NIL: add s + entry[0] as new code
    s = entry
```
Table columns: **s | k | entry/output | code | string**.

### Arithmetic coding
Give each symbol a range [Range_low, Range_high) of [0,1) with width equal to its probability.

**Encode:** start with low = 0, high = 1, range = 1. For each symbol:
```
high = low + range × Range_high(sym)     ← use the OLD low for both
low  = low + range × Range_low(sym)
range = high − low
```
(The slide 4 pseudocode updates `low` first. If you then compute `high` from the new `low`, you get the wrong answer. Always compute both from the old low.)

**Codeword (Procedure 7.2):** write binary fraction bits 0.b₁b₂b₃… one at a time. Set the next bit to 1. If the value is now **> high**, change the bit back to 0. Stop as soon as the value is **≥ low**.

**Decode (Algorithm 7.6):** find the symbol s with Range_low(s) ≤ value < Range_high(s) and output it. Then set **value = (value − Range_low(s)) / (Range_high(s) − Range_low(s))**. Stop when you output the terminator `$`.

---

## Problems (easy → hard)

### Problem 1: Entropy basics (10 pts)
(a) An 8-bit grey image has all 256 grey levels equally likely. What is its entropy?
(b) A two-level image has one level with probability 1/3 and the other with 2/3. What is its entropy? (This is the "0.92" image on slide 13.)
(c) A source emits a, b, c, d with probabilities 1/2, 1/4, 1/8, 1/8. What is its entropy?

<details><summary>Solution</summary>

(a) pᵢ = 1/256 for every level, so η = Σ (1/256)·log₂256 = log₂256 = **8 bits/pixel**.

(b) η = (1/3)·log₂3 + (2/3)·log₂(3/2)
= (1/3)(1.585) + (2/3)(1.585 − 1)
= 0.528 + 0.390 = **0.918 ≈ 0.92 bits/pixel**

(c)

| Symbol | p | log₂(1/p) | p·log₂(1/p) |
|---|---|---|---|
| a | 1/2 | 1 | 0.5 |
| b | 1/4 | 2 | 0.5 |
| c | 1/8 | 3 | 0.375 |
| d | 1/8 | 3 | 0.375 |
| | | **η** | **1.75** |

**η = 1.75 bits/symbol**

*Trap:* entropy is never more than log₂n, and it reaches log₂n only for a uniform source. A two-value image needs at most 1 bit, never 2.
</details>

---

### Problem 2: Entropy of a string, and the bound (10 pts)
For the string `HELLO`:
(a) give the probability and self-information of each symbol,
(b) compute the entropy,
(c) give the minimum total number of bits any lossless code needs for this string, and the number of bits a fixed-length code needs.

<details><summary>Solution</summary>

Counts: H=1, E=1, L=2, O=1, so n = 5.

| Symbol | Count | p | log₂(1/p) | p·log₂(1/p) |
|---|---|---|---|---|
| L | 2 | 0.4 | log₂2.5 = 1.322 | 0.529 |
| H | 1 | 0.2 | log₂5 = 2.322 | 0.464 |
| E | 1 | 0.2 | 2.322 | 0.464 |
| O | 1 | 0.2 | 2.322 | 0.464 |
| | | | **η** | **1.922** |

(b) **η ≈ 1.922 bits/symbol**
(c) Lower bound = 5 × 1.922 ≈ **9.61 bits**, so a real code needs at least **10 bits**. A fixed-length code needs ⌈log₂4⌉ = 2 bits per symbol, so 5 × 2 = **10 bits**.

*Trap:* "log₂(1/p)" in the slide tables (1.32, 2.32) is self-information. It is not the code length you actually get, because real codes use whole bits.
</details>

---

### Problem 3: Run-length coding (10 pts)
(a) RLC-encode `BBBBEEEEEEEECCCCDAAAAA` and give the compression ratio in characters.
(b) A fax scan line is 12 W, 1 B, 12 W, 3 B, 24 W, 1 B, 14 W. Encode it and give the ratio.
(c) Encode `ABCABC`. What happens?

<details><summary>Solution</summary>

(a) Runs: 4 B, 8 E, 4 C, 1 D, 5 A → **`4B8E4C1D5A`**. That is 22 characters → 10 characters, so **ratio = 22/10 = 2.2**.

(b) **`12W1B12W3B24W1B14W`**: 67 characters → 18 characters, so **ratio = 67/18 ≈ 3.72**.

(c) `1A1B1C1A1B1C`: 6 → 12 characters, so **ratio = 0.5. The output is twice as long.**

*Trap:* RLC exploits the **memory** in a source (runs). On a memoryless source, or data without runs, it makes the data bigger.
</details>

---

### Problem 4: Audio data rate, compression ratio, quantization (10 pts)
(a) Find the data rate of CD audio (44.1 kHz, 16 bits, stereo) in bit/s and in bytes/s, and the storage needed for one minute and for one hour.
(b) An MP3 encoder outputs 128 kbit/s. What is the compression ratio?
(c) Using "about 6 dB per bit", what SNR do 16-bit samples give?
(d) A 3-bit uniform quantizer covers [−4, 4). Find the step size, and quantize x = 2.3 (index and reconstruction value, using the midpoint of the interval). What is the error, and what is the maximum error?

<details><summary>Solution</summary>

(a) 44 100 × 16 × 2 = **1 411 200 bit/s ≈ 1.41 Mbit/s** = 176 400 bytes/s.
1 minute: 1 411 200 × 60 / 8 = **10.58 MB**. 1 hour: **635 MB** (the slide's "84M per minute, 5G per hour" are in **bits**).

(b) B₀/B₁ = 1 411 200 / 128 000 = **11.025 ≈ 11 : 1**

(c) 16 × 6 ≈ **96 dB** (6.02 × 16 = 96.3 dB).

(d) Δ = (4 − (−4)) / 2³ = 8/8 = **1**. The intervals are [−4,−3), …, [2,3), [3,4) with indices 0…7.
x = 2.3 falls in [2, 3) → **index 6** (binary 110) → reconstruction **2.5**. Error = 0.2. Maximum error = Δ/2 = **0.5**.

*Trap:* bits vs bytes. Divide by 8 whenever the question says "bytes" or "MB". kbit/s here means 1000, not 1024.
</details>

---

### Problem 5: Shannon-Fano on HELLO, both trees (slides 19–23) (10 pts)
Apply Shannon-Fano to `HELLO`. Give two different valid trees, the code table for each, and the total number of bits.

<details><summary>Solution</summary>

Sorted: L(2), H(1), E(1), O(1). Total = 5.

**Tree 1:** split {L}=2 | {H,E,O}=3. Then {H}=1 | {E,O}=2. Then {E} | {O}.

| Symbol | Count | log₂(1/p) | Code | Bits used |
|---|---|---|---|---|
| L | 2 | 1.32 | 0 | 2 × 1 = 2 |
| H | 1 | 2.32 | 10 | 2 |
| E | 1 | 2.32 | 110 | 3 |
| O | 1 | 2.32 | 111 | 3 |
| | | | **Total** | **10** |

**Tree 2:** split {L,H}=3 | {E,O}=2. Then L|H and E|O.

| Symbol | Count | Code | Bits used |
|---|---|---|---|
| L | 2 | 00 | 4 |
| H | 1 | 01 | 2 |
| E | 1 | 10 | 2 |
| O | 1 | 11 | 2 |
| | | **Total** | **10** |

**Both trees use 10 bits, so L̄ = 10/5 = 2 bits/symbol** (η = 1.922).

*Trap:* the two splits 2|3 and 3|2 are equally balanced, so both are legal. Shannon-Fano is **not unique** and in general **not optimal**.
</details>

---

### Problem 6: Huffman on HELLO, the professor's tree (slides 28–29) (10 pts)
Build the Huffman tree for `HELLO` following the list on slide 29 (P1, P2, P3). Give the codes, the total bits, L̄ and the efficiency.

<details><summary>Solution</summary>

| Step | Merge | New node | List afterwards |
|---|---|---|---|
| init | | | L(2) H(1) E(1) O(1) |
| (a) | E(1) + O(1) | P1(2) | L(2) P1(2) H(1) |
| (b) | H(1) + P1(2) | P2(3) | L(2) P2(3) |
| (c) | L(2) + P2(3) | P3(5) = root | P3 |

Tree: root P3 → 0: L, 1: P2. P2 → 0: H, 1: P1. P1 → 0: E, 1: O.

| Symbol | Count | Code | Bits |
|---|---|---|---|
| L | 2 | 0 | 2 |
| H | 1 | 10 | 2 |
| E | 1 | 110 | 3 |
| O | 1 | 111 | 3 |
| | | **Total** | **10** |

**L̄ = 10/5 = 2.0 bits/symbol**, η = 1.922, so **efficiency = 1.922/2 = 96.1%**. The bound 1.922 ≤ 2.0 < 2.922 holds.

*Trap:* at step (b), H(1) has to merge with one of two nodes of count 2 (L or P1). The slide picks P1. Picking L gives L=00, H=01, E=10, O=11. That is a different tree with **the same 10 bits**. Both are correct.
</details>

---

### Problem 7: "Huffman your own name" (speaker-notes exercise, slide 26) (10 pts)
The notes say to write your first name as a string, apply Huffman coding and draw the tree. Do it for **`SHAHZODA`**, then repeat with your own name. Give the codes, the total bits, L̄, η and the efficiency, and compare with a fixed-length code.

<details><summary>Solution</summary>

Counts: H=2, A=2, S=1, Z=1, O=1, D=1 (8 letters).

| Step | Merge | New node |
|---|---|---|
| 1 | S(1) + Z(1) | P1(2) |
| 2 | O(1) + D(1) | P2(2) |
| 3 | H(2) + A(2) | P3(4) |
| 4 | P1(2) + P2(2) | P4(4) |
| 5 | P3(4) + P4(4) | root(8) |

Root → 0: P3 {H,A}, 1: P4 {S,Z,O,D}.

| Symbol | Count | p | Code | Bits |
|---|---|---|---|---|
| H | 2 | 1/4 | 00 | 4 |
| A | 2 | 1/4 | 01 | 4 |
| S | 1 | 1/8 | 100 | 3 |
| Z | 1 | 1/8 | 101 | 3 |
| O | 1 | 1/8 | 110 | 3 |
| D | 1 | 1/8 | 111 | 3 |
| | | | **Total** | **20** |

**L̄ = 20/8 = 2.5 bits/letter.** η = 2·(1/4)(2) + 4·(1/8)(3) = 1 + 1.5 = **2.5**, so **efficiency = 100%**.
Fixed-length: 6 symbols need ⌈log₂6⌉ = 3 bits, so 8 × 3 = 24 bits. **Huffman saves 4 bits (ratio 24/20 = 1.2).**

*Trap:* Huffman reaches the entropy exactly only when every p is a power of 1/2, as here. For your own name expect L̄ slightly above η. Ties between equal counts can change individual codes, but never the total.
</details>

---

### Problem 8: MISSISSIPPI, Shannon-Fano vs Huffman (10 pts)
For `MISSISSIPPI`, compute η, then build the Shannon-Fano and the Huffman code. Compare the total bits with η and with a 2-bit fixed code.

<details><summary>Solution</summary>

Counts: I=4, S=4, P=2, M=1, n = 11.

η = 2·(4/11)·log₂(11/4) + (2/11)·log₂(11/2) + (1/11)·log₂11
= 2(0.364)(1.459) + (0.182)(2.459) + (0.0909)(3.459) = 1.061 + 0.447 + 0.314 = **1.823 bits/symbol** (≈ 20.05 bits in total)

**Shannon-Fano:** {I}=4 | {S,P,M}=7 (difference 3 beats {I,S}=8 | {P,M}=3, difference 5). Then {S}=4 | {P,M}=3, then P | M.

**Huffman:** M(1)+P(2) → 3. Then 3 + I(4) → 7 (S or I, a tie). Then S(4) + 7 → 11.

| Symbol | Count | Shannon-Fano | Huffman | Bits |
|---|---|---|---|---|
| I | 4 | 0 | 00 | SF 4 / H 8 |
| S | 4 | 10 | 1 | SF 8 / H 4 |
| P | 2 | 110 | 010 | 6 / 6 |
| M | 1 | 111 | 011 | 3 / 3 |
| | | | **Total** | **21 / 21** |

**Both give 21 bits, L̄ = 21/11 = 1.909 bits/symbol.** Efficiency = 1.823/1.909 = **95.5%**. Fixed 2-bit code = 22 bits.

*Trap:* the codes look different (I and S swap lengths) because of the I/S tie. The totals are the same.
</details>

---

### Problem 9: Huffman with ties gives different lengths (10 pts)
Source: A 0.4, B 0.2, C 0.2, D 0.1, E 0.1. Build two different Huffman codes and show that both are optimal. Find η and the efficiency.

<details><summary>Solution</summary>

**Tree 1 (merge the new node last when tied):**
D+E = 0.2 → {B 0.2, C 0.2, DE 0.2, A 0.4} → B+C = 0.4 → {DE 0.2, BC 0.4, A 0.4} → DE+A = 0.6 → BC+ADE = 1.0

| Sym | p | Code | Len |
|---|---|---|---|
| A | 0.4 | 00 | 2 |
| B | 0.2 | 10 | 2 |
| C | 0.2 | 11 | 2 |
| D | 0.1 | 010 | 3 |
| E | 0.1 | 011 | 3 |

L̄ = 0.4·2 + 0.2·2 + 0.2·2 + 0.1·3 + 0.1·3 = **2.2**

**Tree 2 (merge the new node first when tied):**
D+E = 0.2 → DE+C = 0.4 → that 0.4 + B = 0.6 → A + 0.6 = 1.0. Lengths: A 1, B 2, C 3, D 4, E 4.
Codes: A=0, B=10, C=110, D=1110, E=1111.
L̄ = 0.4·1 + 0.2·2 + 0.2·3 + 0.1·4 + 0.1·4 = **2.2**

η = 0.4·log₂2.5 + 2·0.2·log₂5 + 2·0.1·log₂10 = 0.529 + 0.929 + 0.664 = **2.122**. **Efficiency = 2.122/2.2 = 96.4%.**

*Trap:* the two trees have **different code lengths but the same L̄ = 2.2**. Both are correct. Tree 1 has smaller variance (better for buffering), but either one gets full marks.
</details>

---

### Problem 10: Shannon-Fano is not always optimal (10 pts)
Counts: A 15, B 7, C 6, D 6, E 5 (39 symbols). Build Shannon-Fano and Huffman codes and compare the total bits.

<details><summary>Solution</summary>

**Shannon-Fano:** {A,B}=22 | {C,D,E}=17 (difference 5 beats 15|24, difference 9). A|B. {C}=6 | {D,E}=11 (difference 5 beats 12|5, difference 7). D|E.
Codes: A=00, B=01, C=10, D=110, E=111.
Bits = 15·2 + 7·2 + 6·2 + 6·3 + 5·3 = 30 + 14 + 12 + 18 + 15 = **89**

**Huffman:** E5+C6 = 11 (C/D tie) → D6+B7 = 13 → 11+13 = 24 → A15+24 = 39.
Codes: A=0 and B, C, D, E all 3 bits (e.g. B=111, C=101, D=110, E=100).
Bits = 15·1 + 24·3 = **87**

η = 2.186 bits/symbol (85.3 bits in total). **Shannon-Fano: 89 bits (2.282 b/s). Huffman: 87 bits (2.231 b/s).** Huffman wins.

*Trap:* Shannon-Fano decides top-down and can get stuck with a poor first split. Huffman (bottom-up) is **guaranteed optimal** among prefix codes.
</details>

---

### Problem 11: Prefix property and decoding (10 pts)
(a) With the code a=1, b=01, c=001, d=000, decode `1001011000`.
(b) Why can't the code a=0, b=01, c=10 be decoded reliably? Show it with `010`.

<details><summary>Solution</summary>

(a) Read greedily. Each codeword is recognised as soon as it is complete, because no codeword is a prefix of another:
`1 | 001 | 01 | 1 | 000` → **a c b a d**

(b) `0` (a) is a prefix of `01` (b). So `010` can be read as `0|10` = **ac** or as `01|0` = **ba**. That is ambiguous.

*Trap:* Huffman codes always have the unique prefix property, because every symbol is a **leaf** and no codeword ends at an internal node. That is why no separators are needed.
</details>

---

### Problem 12: Extended Huffman (slides 31–32) (10 pts)
A binary source has p(A) = 0.9 and p(B) = 0.1. (a) What is η? (b) What L̄ does plain Huffman give? (c) Group the symbols in pairs (k = 2) and Huffman-code the 4 pairs. How many bits per original symbol do you get now?

<details><summary>Solution</summary>

(a) η = 0.9·log₂(1/0.9) + 0.1·log₂10 = 0.137 + 0.332 = **0.469 bits/symbol**

(b) Two symbols means each code is at least 1 bit, so **L̄ = 1 bit/symbol** (efficiency 47%).

(c) Pairs: AA 0.81, AB 0.09, BA 0.09, BB 0.01.
BB+AB = 0.10 → BA+0.10 = 0.19 → AA+0.19 = 1.0

| Pair | p | Code | Len |
|---|---|---|---|
| AA | 0.81 | 0 | 1 |
| BA | 0.09 | 11 | 2 |
| AB | 0.09 | 100 | 3 |
| BB | 0.01 | 101 | 3 |

L̄ per pair = 0.81 + 0.18 + 0.27 + 0.03 = 1.29, so **per symbol = 1.29/2 = 0.645 bits**. That is down from 1 and closer to 0.469.

*Trap:* the alphabet size grows as nᵏ. For k ≥ 3 with a big n the table becomes impractical, and the gain is "an improvement, but not much".
</details>

---

### Problem 13: LZW encoding, slide example (slides 40–41) (10 pts)
Dictionary: 1=A, 2=B, 3=C. Encode `ABABBABCABABBA`. Give the full table, the output codes and the compression ratio.

<details><summary>Solution</summary>

| s | c | Output | Code | String |
|---|---|---|---|---|
| | | | 1 | A |
| | | | 2 | B |
| | | | 3 | C |
| A | B | 1 | 4 | AB |
| B | A | 2 | 5 | BA |
| A | B | | | |
| AB | B | 4 | 6 | ABB |
| B | A | | | |
| BA | B | 5 | 7 | BAB |
| B | C | 2 | 8 | BC |
| C | A | 3 | 9 | CA |
| A | B | | | |
| AB | A | 4 | 10 | ABA |
| A | B | | | |
| AB | B | | | |
| ABB | A | 6 | 11 | ABBA |
| A | EOF | 1 | | |

**Output: 1 2 4 5 2 3 4 6 1** (9 codes for 14 characters). **Compression ratio = 14/9 = 1.56.**

*Trap:* when s+c is already in the dictionary, there is **no output and no new entry**. You only extend s. Don't forget to output the last s at EOF.
</details>

---

### Problem 14: LZW decoding, slide example (slides 42–43) (10 pts)
Decode `1 2 4 5 2 3 4 6 1` with the initial dictionary 1=A, 2=B, 3=C, and rebuild the dictionary.

<details><summary>Solution</summary>

| s | k | Entry/output | Code | String (s + entry[0]) |
|---|---|---|---|---|
| NIL | 1 | A | | |
| A | 2 | B | 4 | AB |
| B | 4 | AB | 5 | BA |
| AB | 5 | BA | 6 | ABB |
| BA | 2 | B | 7 | BAB |
| B | 3 | C | 8 | BC |
| C | 4 | AB | 9 | CA |
| AB | 6 | ABB | 10 | ABA |
| ABB | 1 | A | 11 | ABBA |

Output: A·B·AB·BA·B·C·AB·ABB·A = **ABABBABCABABBA**. The dictionary is identical to the encoder's, so the result is lossless.

*Trap:* the decoder adds an entry **one step later** than the encoder, using s + **first letter** of the current entry (not the whole entry).
</details>

---

### Problem 15: LZW with the exception case (slide 44) (10 pts)
Dictionary 1=A, 2=B.
(a) Encode `BABAABAAA`.
(b) Decode your output and show where the exception handler is needed.
(c) Decode `1 2 3 5`.

<details><summary>Solution</summary>

(a) Encoding:

| s | c | Output | Code | String |
|---|---|---|---|---|
| B | A | 2 | 3 | BA |
| A | B | 1 | 4 | AB |
| B | A | | | |
| BA | A | 3 | 5 | BAA |
| A | B | | | |
| AB | A | 4 | 6 | ABA |
| A | A | 1 | 7 | AA |
| A | A | | | |
| AA | EOF | 7 | | |

**Output: 2 1 3 4 1 7** (9 characters → 6 codes, ratio 1.5)

(b) Decoding:

| s | k | Entry/output | Code | String |
|---|---|---|---|---|
| NIL | 2 | B | | |
| B | 1 | A | 3 | BA |
| A | 3 | BA | 4 | AB |
| BA | 4 | AB | 5 | BAA |
| AB | 1 | A | 6 | ABA |
| A | 7 | **7 missing → s + s[0] = A + A = AA** | 7 | AA |

Output **BABAABAAA**. The exception happens at code 7, because the encoder used code 7 immediately after creating it.

(c) `1 2 3 5`: A. Then B (add 3=AB). Then AB (add 4=BA). Then 5 is missing, so entry = AB + A = ABA (add 5=ABA). **→ ABABABA**

*Trap:* the exception only happens with the pattern cScSc (here A·A·A, or AB·AB·A). The simple decoder (Alg. 7.3) would crash on it.
</details>

---

### Problem 16: Arithmetic encoding of CAEE$ (slides 5–8) (10 pts)
Use the table below. Encode `CAEE$`, show low/high/range after each symbol, and generate the binary codeword.

| Sym | A | B | C | D | E | F | $ |
|---|---|---|---|---|---|---|---|
| p | 0.2 | 0.1 | 0.2 | 0.05 | 0.3 | 0.05 | 0.1 |
| Range | [0,0.2) | [0.2,0.3) | [0.3,0.5) | [0.5,0.55) | [0.55,0.85) | [0.85,0.9) | [0.9,1.0) |

<details><summary>Solution</summary>

| Sym | Computation (old low, old range) | Low | High | Range |
|---|---|---|---|---|
| start | | 0 | 1.0 | 1.0 |
| C | 0 + 1·0.3, 0 + 1·0.5 | 0.3 | 0.5 | 0.2 |
| A | 0.3 + 0.2·0, 0.3 + 0.2·0.2 | 0.30 | 0.34 | 0.04 |
| E | 0.3 + 0.04·0.55, 0.3 + 0.04·0.85 | 0.322 | 0.334 | 0.012 |
| E | 0.322 + 0.012·0.55, 0.322 + 0.012·0.85 | 0.3286 | 0.3322 | 0.0036 |
| $ | 0.3286 + 0.0036·0.9, 0.3286 + 0.0036·1.0 | **0.33184** | **0.33220** | 0.00036 |

Check: final range = product of the probabilities = 0.2·0.2·0.3·0.3·0.1 = 0.00036 ✓

Codeword (low 0.33184, high 0.3322):

| k | Try bit 1 → value | > high? | Keep | Value | ≥ low? |
|---|---|---|---|---|---|
| 1 | 0.5 | yes | 0 | 0 | no |
| 2 | 0.25 | no | 1 | 0.25 | no |
| 3 | 0.375 | yes | 0 | 0.25 | no |
| 4 | 0.3125 | no | 1 | 0.3125 | no |
| 5 | 0.34375 | yes | 0 | 0.3125 | no |
| 6 | 0.328125 | no | 1 | 0.328125 | no |
| 7 | 0.3359375 | yes | 0 | 0.328125 | no |
| 8 | 0.33203125 | no | 1 | 0.33203125 | **yes → stop** |

**Interval [0.33184, 0.3322). Codeword 0.01010101₂ = 0.33203125, 8 bits.**

*Trap:* compute high **before** overwriting low (the slide 4 pseudocode has the order backwards). The final range is always the product of the symbol probabilities, which is a quick way to check your work.
</details>

---

### Problem 17: Arithmetic decoding of 0.33203125 (slides 9–10) (10 pts)
Decode the value 0.33203125 with the same table.

<details><summary>Solution</summary>

| Value | Symbol | Low | High | Range | Next value = (value − low)/range |
|---|---|---|---|---|---|
| 0.33203125 | C | 0.3 | 0.5 | 0.2 | 0.03203125/0.2 = 0.16015625 |
| 0.16015625 | A | 0.0 | 0.2 | 0.2 | 0.16015625/0.2 = 0.80078125 |
| 0.80078125 | E | 0.55 | 0.85 | 0.3 | 0.25078125/0.3 = 0.8359375 |
| 0.8359375 | E | 0.55 | 0.85 | 0.3 | 0.2859375/0.3 = 0.953125 |
| 0.953125 | $ | 0.9 | 1.0 | 0.1 | stop |

**Decoded: CAEE$**

*Trap:* divide by the **symbol's** range (its probability), not by the running interval width from the encoder.
</details>

---

### Problem 18: Arithmetic coding, new table (10 pts)
A [0, 0.4), B [0.4, 0.7), C [0.7, 0.9), $ [0.9, 1.0).
(a) Encode `CAB$` and give the shortest binary codeword.
(b) Decode the value **0.7545** with the same table.

<details><summary>Solution</summary>

(a)

| Sym | Low | High | Range |
|---|---|---|---|
| start | 0 | 1 | 1 |
| C | 0.7 | 0.9 | 0.2 |
| A | 0.7 + 0.2·0 = 0.7 | 0.7 + 0.2·0.4 = 0.78 | 0.08 |
| B | 0.7 + 0.08·0.4 = 0.732 | 0.7 + 0.08·0.7 = 0.756 | 0.024 |
| $ | 0.732 + 0.024·0.9 = **0.7536** | 0.732 + 0.024·1 = **0.756** | 0.0024 |

Check: 0.2·0.4·0.3·0.1 = 0.0024 ✓

Codeword: 1 (0.5, keep) → 1 (0.75, keep, still < 0.7536) → then 0.875, 0.8125, 0.78125, 0.765625 and 0.7578125 are all > 0.756, so bits 3–7 = 0 → bit 8: 0.75390625 is ≤ high and ≥ low, so stop.
**Codeword 0.11000001₂ = 0.75390625, 8 bits.** (Rule of thumb: about ⌈−log₂ range⌉ = ⌈8.7⌉ bits.)

(b)

| Value | Symbol | Next value |
|---|---|---|
| 0.7545 | C [0.7,0.9) | (0.7545−0.7)/0.2 = 0.2725 |
| 0.2725 | A [0,0.4) | 0.2725/0.4 = 0.68125 |
| 0.68125 | B [0.4,0.7) | (0.68125−0.4)/0.3 = 0.9375 |
| 0.9375 | $ | stop |

**Decoded: CAB$** (0.7545 lies inside [0.7536, 0.756), as it should).

*Trap:* any number inside [low, high) decodes to the same message. The codeword is just the shortest binary one.
</details>

---

### Problem 19: MPEG audio bit allocation (slide 37) (10 pts)
Four sub-bands have SMR = 12, 3, 20, 8 dB. Assume each code bit adds 6 dB of SNR, and every band starts at 0 bits (SNR = 0). There are 7 bits to allocate, one at a time, using MNR = SNR − SMR. Show each step and the final allocation.

<details><summary>Solution</summary>

| Step | MNR (b1, b2, b3, b4) | Lowest MNR → gets 1 bit |
|---|---|---|
| 1 | −12, −3, **−20**, −8 | band 3 |
| 2 | −12, −3, **−14**, −8 | band 3 |
| 3 | **−12**, −3, −8, −8 | band 1 |
| 4 | −6, −3, **−8**, −8 | band 3 (tie with band 4 at −8, the lower index wins) |
| 5 | −6, −3, −2, **−8** | band 4 |
| 6 | **−6**, −3, −2, −2 | band 1 |
| 7 | 0, **−3**, −2, −2 | band 2 |

**Final bits: band 1 = 2, band 2 = 1, band 3 = 3, band 4 = 1** (total 7). Final MNR = 0, 3, −2, −2 dB.

*Trap:* the bit goes to the **lowest** MNR (the band where the noise is most audible), not the highest SMR alone. After every allocation, recompute that band's SNR.
</details>

---

### Problem 20: Full comparison on one string (10 pts)
For `BBBBEEEEEEEECCCCDAAAAA` (22 symbols): compute η, build a Huffman code, and compare total bits for 8-bit ASCII, a fixed 3-bit code, Huffman and RLC (count as 4 bits + symbol as 3 bits per run).

<details><summary>Solution</summary>

Counts: E 8, A 5, B 4, C 4, D 1.
η = (8/22)log₂(22/8) + (5/22)log₂(22/5) + 2(4/22)log₂(22/4) + (1/22)log₂22 = **2.113 bits/symbol** (46.5 bits in total).

Huffman, one valid tree: D1+C4 = 5 (B/C tie) → B4 + 5 = 9 (tie between A5 and the new 5) → A5 + E8 = 13 → 9 + 13 = 22. Other tie choices give other codes, but always 49 bits.

| Sym | Count | Code | Bits |
|---|---|---|---|
| E | 8 | 11 | 16 |
| A | 5 | 10 | 10 |
| B | 4 | 00 | 8 |
| C | 4 | 011 | 12 |
| D | 1 | 010 | 3 |
| | | **Total** | **49** |

L̄ = 49/22 = 2.227 bits/symbol (efficiency 94.9%).

| Method | Bits | Ratio vs ASCII |
|---|---|---|
| ASCII 8 bit | 22 × 8 = 176 | 1 |
| Fixed 3 bit | 66 | 2.67 |
| **Huffman** | **49** | **3.59** |
| RLC (5 runs × 7 bits) | 35 | 5.03 |

*Trap:* RLC beats Huffman here only because the string is made of long runs. Huffman ignores order and only looks at frequencies.
</details>

---

## Explain and compare: model answers

**Q1. Lossless vs lossy compression.**
Lossless: decompression gives back **exactly** the original (RLC, Huffman, LZW, arithmetic). Use it for text, programs and medical data. Ratios are modest (about 2–3:1). Lossy: the output is only a **close approximation**. Information is thrown away, mainly by **quantization**, so it reaches much higher ratios (MP3 about 11:1). Use it for audio, images and video, where the eye or ear does not notice the loss. Rate-distortion theory describes the trade-off: fewer bits means more distortion.

**Q2. Why is a Huffman code prefix-free, and why does that matter?**
Every symbol sits at a **leaf** of the binary tree, and a codeword is the path from the root to its leaf. One leaf's path can never pass through another leaf, so no codeword is a prefix of another. The decoder can therefore read bits and output a symbol the moment it reaches a leaf. It needs no separators, and decoding is never ambiguous.

**Q3. Huffman vs arithmetic coding.**
Huffman gives each symbol a codeword with a **whole number of bits**, so it can waste up to almost 1 bit/symbol. This is especially bad when one p is close to 1 (ideally about 0 bits, but Huffman must give at least 1). Arithmetic coding encodes the **whole message as one number** in [low, high). The message costs about −log₂(Π pᵢ) bits, so a symbol effectively costs a **fraction of a bit** and the result gets closer to the entropy. The costs: floating-point precision (which needs scaling and incremental output), more computation, and an error in one bit corrupts everything after it.

**Q4. Shannon-Fano vs Huffman, and LZW vs Huffman.**
Shannon-Fano is **top-down** (split into halves of equal weight) and is not unique or always optimal. Huffman is **bottom-up** (merge the two smallest) and is optimal, with η ≤ L̄ < η+1. Both need the symbol statistics first. **LZW** needs **no prior knowledge**, works in a **single pass**, and builds the same dictionary in the encoder and the decoder, so the dictionary is never sent. It uses fixed-length codes for variable-length strings and is best on repetitive data (60–70% on some text).

**Q5 (bonus). Why can masking be used for compression?**
Every extra bit gives about 6 dB of SNR, so quantization noise is set by the number of bits. A loud tone masks nearby frequencies (frequency masking) and nearby moments (temporal masking). So the noise floor in those sub-bands can be **raised without anyone hearing it**. A higher noise floor means fewer bits, and fewer bits is compression. MPEG allocates bits by **MNR = SNR − SMR**.

---

## Most likely on the exam
1. **Huffman tree + code table + L̄ vs η** (HELLO or your own name). Show the merge list and the bound.
2. **LZW encode and/or decode with a full dictionary table** (`ABABBABCABABBA`, maybe one that needs the exception handler).
3. **Arithmetic encode (low/high/range table) + codeword, or decode** (`CAEE$`-style).
