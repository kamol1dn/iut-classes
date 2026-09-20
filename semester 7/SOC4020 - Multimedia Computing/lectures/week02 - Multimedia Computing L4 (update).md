# L4 — Lossless Compression: Entropy, Huffman & LZW

**SOC4020 · Week 2 · 48 slides · Dr. Minhaz Uddin Ahmed**
Source: [week02 - Multimedia Computing L4 (update).pptx](week02%20-%20Multimedia%20Computing%20L4%20(update).pptx)
Reference: textbook **Chapter 7**

The most algorithm-heavy deck so far. Expect **worked problems**, not just
definitions — you will likely be asked to build a Huffman tree or trace LZW by
hand.

**Contents:** differential coding of audio · lossless predictive coding · DPCM ·
lossless compression · information theory · run-length coding · variable-length
coding · Shannon-Fano · Huffman · adaptive Huffman · LZW.

---

## 🟡 An exercise hidden in the speaker notes

Slide 26's notes contain a task that isn't on the visible slide:

> **Write your first name as a string, apply the Huffman coding algorithm, and
> draw the equivalent binary tree.**

Do it — it's the single best preparation for the exam version of this question,
and takes five minutes.

---

## 1. Modulation

**Definition:** varying one or more properties of a periodic waveform — the
**carrier signal** — using a separate **modulation signal** that carries the
information to be transmitted.

| Type | What varies |
|---|---|
| **AM** — amplitude modulation | The **height** of the carrier |
| **FM** — frequency modulation | The **frequency** of the carrier |
| **PM** — phase modulation | The **phase**; frequency stays unchanged. Similar to FM. |

**Modulation** encodes information into a transmitted signal;
**demodulation** extracts it back out.

## 2. PCM and the shape of compression

In a quantizer:

- The **coder mapping** is the set of input-interval boundaries that all map to the same output level.
- The **decoder mapping** is the set of representative output values.

### The three stages of every compression scheme

Repeated from [L3](week02%20-%20Multimedia%20Computing%20L3.md) — he clearly
considers it central:

| Stage | What happens |
|---|---|
| **1. Transformation** | Convert the input to a representation that compresses better. E.g. **predictive coding**: predict the next signal from previous ones, transmit only the **prediction error**. |
| **2. Loss** | **Quantization is the main lossy step** — fewer reconstruction levels than the original means information is necessarily lost. |
| **3. Coding** | Assign a **codeword** per output level/symbol, forming a bitstream. Fixed-length, or variable-length such as Huffman. |

## 3. Compression basics

> **Compression:** the process of coding that effectively **reduces the total
> number of bits** needed to represent certain information.
>
> **Lossless** if compression and decompression induce **no information loss**;
> otherwise **lossy**.

**Compression ratio:**

```
compression ratio = B₀ / B₁
```

where `B₀` is the bits needed **before** compression and `B₁` the bits
**after**. You want a ratio **much larger than 1.0** — the higher the better,
**so long as it stays computationally feasible**.

## 4. Information theory — entropy

For an information source with alphabet `S = {s₁, s₂, …, sₙ}` where `pᵢ` is the
probability of symbol `sᵢ`:

- The **self-information** of `sᵢ` (Shannon's term) is the **number of bits needed to encode `sᵢ`**.
- The **entropy η** is the average of that over the alphabet.

**Entropy encoding** is therefore a lossless technique that assigns **shorter
codes to more frequent symbols** and longer codes to rarer ones.

### The two worked examples — know both

| Image | Distribution | Entropy |
|---|---|---|
| **Uniform** grey levels | every `pᵢ = 1/256` | **log₂256 = 8** bits |
| **Two-value** image | two possible values | **0.92** bits |

The point: entropy tells you the **theoretical floor** for lossless coding. A
uniform 256-level image genuinely needs 8 bits/pixel; a nearly-binary one needs
under 1.

## 5. Run-Length Coding (RLC)

**First, a definition you need:**

> A **memoryless source** is one that is independently distributed — the value
> of the current symbol **does not depend** on the symbols before it.

**RLC does the opposite: it exploits the memory present in the source.**

**Rationale:** if symbols tend to form **continuous groups**, encode the symbol
plus the **length of the group**.

**Worked examples:**

```
aaaaa                    →  5a
BBBBEEEEEEEECCCCDAAAAA   →  4B8E4C1D5A
```

### Two relatives

**Repetition suppression** — reserve a specific **flag symbol** for a commonly
occurring pattern, and substitute it for long runs.

**Pattern substitution** — build groups of individual symbols into **strings**,
give each string a **code or index**, and use that index every time the string
appears. Its advantage: **no pre-analysis is needed** to build a dictionary —
the strings are created as the message is scanned. (This is the idea LZW
develops.)

## 6. Variable-Length Coding — Shannon-Fano

**A top-down approach:**

1. **Sort** the symbols by frequency count.
2. **Recursively divide** the symbols into two parts, each with approximately the same total count, until every part holds a single symbol.

### The "HELLO" example

Frequency counts: **H=1, E=1, L=2, O=1**.

**First tree:**

| Symbol | Count | log₂(1/p) | Code | Bits used |
|---|---|---|---|---|
| L | 2 | 1.32 | `0` | 1 |
| H | 1 | 2.32 | `10` | 2 |
| E | 1 | 2.32 | `110` | 3 |
| O | 1 | 2.32 | `111` | 3 |
| | | | **Total** | **10** |

**Second tree — a different valid split:**

| Symbol | Count | log₂(1/p) | Code | Bits used |
|---|---|---|---|---|
| L | 2 | 1.32 | `00` | 4 |
| H | 1 | 2.32 | `01` | 2 |
| E | 1 | 2.32 | `10` | 2 |
| O | 1 | 2.32 | `11` | 2 |
| | | | **Total** | **10** |

> **Why he shows two trees:** Shannon-Fano's result is **not unique** — the
> recursive split can be made differently and both are legal. Here both happen
> to total 10 bits. This non-uniqueness is exactly the weakness Huffman fixes.

## 7. Huffman coding

**The motivation:** when data is first sampled, every sample gets the same
number of bits — `log₂n`, where `n` is the number of distinct samples or
quantization intervals. Equal-length codes are **inefficient when some symbols
are far more common than others**.

**A bottom-up approach** (contrast with Shannon-Fano's top-down):

1. Associate the **leaves** of a binary tree with the list of probabilities. Sorting them is optional.
2. Take the **two smallest probabilities** and make them siblings under a new parent whose probability is **the sum** of the two.
3. **Repeat** — each time combining the two lowest-probability nodes, whether leaves or parents — until only one node remains. That is the **root**.
4. **Label the branches** 0 and 1, from the root down to every intermediary node.
5. **Traverse root → leaf**, collecting branch labels, to read off each symbol's code.

### The "HELLO" trace

With parent nodes named P1, P2, P3, the list evolves:

```
After initialisation:   L   H   E   O
After iteration (a):    L   P1  H
After iteration (b):    L   P2
After iteration (c):    P3
```

### Two properties — both exam-shaped

**1. Unique Prefix Property.** No Huffman code is a **prefix** of any other.
This is what **precludes ambiguity in decoding** — you always know where one
codeword ends.

**2. Optimality.** It is a **minimum-redundancy code**, proven optimal for a
given accurate probability distribution. Three consequences worth quoting:

- The **two least frequent symbols** have codes of the **same length**, differing only in the **last bit**.
- **More frequent symbols get shorter codes** than less frequent ones.
- The **average code length is strictly less than η + 1** — i.e. within one bit of the entropy bound.

## 8. Extended Huffman

**The motivation:** all Huffman codewords have **integer** bit lengths. That's
wasteful when a symbol's probability `pᵢ` is very large, since its ideal code
length is close to 0 bits but it must still be given at least 1.

**The fix:** group several symbols together and assign **one codeword to the
whole group**. Grouping `k` symbols from an alphabet of size `n` gives an
extended alphabet of size **nᵏ**.

**The verdict he gives:** it does improve the average bits per symbol, **but not
by much** — and there's a hard practical limit. For `k ≥ 3` with `n ≫ 1`, `nᵏ`
means a **huge symbol table**, which is impractical.

## 9. Adaptive Huffman

**The idea:** statistics are **gathered and updated dynamically as the data
stream arrives** — no prior pass over the data.

```
ENCODER                    DECODER
initial_code();            initial_code();
while not EOF {            while not EOF {
    get(c);                    decode(c);
    encode(c);                 output(c);
    update_tree(c);            update_tree(c);
}                          }
```

- **`initial_code`** assigns some initially agreed-upon codes, with **no prior knowledge** of frequency counts.
- **`update_tree`** does two things: **(a)** increments frequency counts for symbols, including any newly seen ones, and **(b)** updates the configuration of the tree.

> **Critical constraint:** the encoder and decoder must use **exactly the same**
> `initial_code` and `update_tree` routines — otherwise their trees diverge and
> decoding fails.

### Tree updating rules

- Nodes are numbered **left to right, bottom to top**.
- The tree must always maintain the **sibling property**: all nodes, internal and leaf, are arranged in **order of increasing counts**.
- If the sibling property is about to be violated, a **swap** rearranges the nodes.
- **The swap rule:** the **farthest node with count N** is swapped with the node whose count has just been incremented to **N + 1**.

## 10. LZW — dictionary-based coding

**Lempel–Ziv–Welch.** Uses **fixed-length codewords to represent
variable-length strings** of symbols that commonly occur together — words in
English text, for instance.

**The key mechanism:** the encoder and decoder **build up the same dictionary
dynamically** as the data flows. Longer and longer repeated entries go into the
dictionary, and once an element is in it, LZW emits **the code** rather than the
string.

### Advantages over Huffman

- **No prior knowledge** of the input data stream is required.
- **60–70% compression ratio** on some text files.
- Performs better on files with a lot of **repetitive data**.
- Compresses in a **single pass**.

### The compression algorithm

```
s = next input character;
while not EOF {
    c = next input character;
    if s + c exists in the dictionary
        s = s + c;
    else {
        output the code for s;
        add string s + c to the dictionary with a new code;
        s = c;
    }
}
output the code for s;
```

### The worked example — learn to trace this

Input `ABABBABCABABBA`, with an initial dictionary of just `1=A, 2=B, 3=C`.

**Output codes: `1 2 4 5 2 3 4 6 1`**

**Dictionary built along the way:**

| Code | String | | Code | String |
|---|---|---|---|---|
| 4 | AB | | 8 | BC |
| 5 | BA | | 9 | CA |
| 6 | ABB | | 10 | ABA |
| 7 | BAB | | 11 | ABBA |

**The result:** instead of sending 14 characters, only **9 codes** are sent —
a **compression ratio of 14/9 ≈ 1.56**.

### Decompression, and the exception case

The simple decoder mirrors the encoder, rebuilding the identical dictionary and
recovering `ABABBABCABABBA` exactly — **a truly lossless result**.

But there is a **modified version with an exception handler**:

```
entry = dictionary entry for k;
if (entry == NULL)          /* exception handler */
    entry = s + s[0];
```

> **Why this is needed, and why it gets asked:** the decoder runs **one step
> behind** the encoder in building the dictionary. If the encoder emits a code
> it has only *just* created, the decoder hasn't added it yet and the lookup
> returns nothing. The reconstruction `s + s[0]` is provably the right answer in
> that case.

### Practical dictionary management

Code length `l` is kept within a range `[l₀, lmax]`. The dictionary starts at
size `2^l₀`; when it fills, the code length **increases by 1**, repeating until
`l = lmax`. Once `lmax` is reached and the dictionary fills again, it must be
**flushed** (as in Unix `compress`) or have its **least recently used (LRU)**
entries removed.

---

## If you're revising this in 10 minutes

1. **Compression ratio = B₀/B₁**; lossless vs lossy.
2. **Entropy**: uniform 256-level image → **8 bits**; two-value image → **0.92**.
3. **RLC** and the `4B8E4C1D5A` example; **memoryless source** defined.
4. **Shannon-Fano is top-down and non-unique; Huffman is bottom-up and optimal.**
5. **Build a Huffman tree by hand** — do the first-name exercise.
6. **Unique prefix property** and the **η + 1** bound.
7. **Adaptive Huffman**: sibling property and the swap rule.
8. **Trace LZW** on `ABABBABCABABBA` → `1 2 4 5 2 3 4 6 1`, ratio 1.56 — and be able to say **why the decoder needs the exception handler**.
