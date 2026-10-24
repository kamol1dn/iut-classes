# Week 7: Mining: Who Writes the Block (slides)

**Blockchain · Week 7 · 28 pages · Dr. Jalolliddin Yusupov · dated 10/23/2026 · online, asynchronous**
Source: [week07 - Mining - Who Writes the Block (slides).pdf](../slides/week07%20-%20Mining%20-%20Who%20Writes%20the%20Block%20(slides).pdf) *(4.5 MB)*

Many pages are diagrams and screenshots with little extractable text, so this summary was built from the
text layer **and the rendered pages**. Every number below was re-computed. Notes marked *(my note)*
are my own explanations and are not on the slides. **Weekly quizzes need a calculator.** The
**CALCULATE** boxes (pp. 10, 12, 17, 18, 20, 25, 27) are the likely quiz material.

Video: the matching two-part lecture VODs are on eClass but **not transcribed yet**.

## The six questions the lecture answers

Same block as last week: **block 968,391** (24 Sep 2026, 11:49 UTC, 4,117 transactions), the one holding
week 6's 225-byte payment (#451, fee 1,356 sat). It was mined by **SpiderPool**.

| Stop | Question | Answer |
|---|---|---|
| The writer | Who gets to write the next block? | The first miner to find a nonce that makes the block hash small enough: **proof of work** |
| The nonce | What is the nonce, exactly? | The **4-byte counter** in the header that the miner changes until the hash is below the target |
| The bits | What do the bits say? | The **target**, packed into 4 bytes. **Difficulty** = how much smaller it is than the first target |
| The pay | What does the miner get, and where do new coins come from? | The **coinbase transaction**: subsidy (new coins) + all fees. The subsidy **halves** every 210,000 blocks |
| The rhythm | Why about one block every ten minutes? | **Difficulty adjustment** every 2,016 blocks |
| The danger | Two winners at once, or one miner too strong? | **Orphan blocks**, most-work chain rule, **confirmations**, **51 % attack** |

Recap from earlier lectures (p. 2): the 80-byte header has six fields: version (4 B), previous block
hash (32), Merkle root (32), timestamp (4), **bits (4)**, **nonce (4)**. Block hash = SHA-256 twice.

## Part 1: who writes the next block (pp. 4–8)

- **The story** (p. 4): 300 students share one notebook with thousands of copies. Someone has to write the next
  page, choosing which payments go in and in what order. If the wrong person writes it, they can write their own payment twice.
- **Role of a miner** (p. 5): validating accountant, security guard, currency issuer (the "mint") and
  "governance body". The miner's pursuit of profit is what secures the network. Miners give **decentralization,
  security, consensus**.
- **Live demo** (p. 6, andersbrownworth.com/blockchain/block): press "Mine" until the hash starts with
  zeros. Even empty data has a hash (the demo found nonce 72,608 → `0000f727…`).
- **Mining** (p. 7) = build a block and try nonce after nonce until the hash is small enough. The loop is
  **1 collect** (mempool) → **2 build** (tx #0 pays me, Merkle root, header) → **3 try a nonce** (SHA-256 twice
  of the 80 bytes) → **4 small enough?** If not, change the nonce and go back to 3 → **5 send it** (every node checks with one hash).
  *"Mining is the loop; proof of work is the small hash it leaves behind."*
- **Proof of work** = a block hash small enough to show that a great many tries were made. It can't be faked, and anyone can check it with one hash.
- **Hard to find, easy to check** (p. 8):

  | | The miner | Every other node |
  |---|---|---|
  | Job | find a nonce that makes the hash small enough | check that it does |
  | Work | about **5.7 × 10²³** hashes (block 968,391) | **one** hash |
  | If someone cheats | a block with a big hash is thrown away | caught at once |

  To change an old payment, a cheater must redo the puzzle for that block **and every block after it**,
  faster than everyone else. *"That asymmetry is the security."*

## Part 2: bits and nonce (pp. 9–15)

**Target** (p. 9): a 256-bit number set by the rules of the moment. A block is valid only if its hash, read as
a number, is **below** the target.

```
hash   000000000000000000006a6ecfff40e7f73228dd2302732b917e38769c398da3   (20 leading zeros)
target 000000000000000000021ec50000000000000000000000000000000000000000   (19 leading zeros, then 2)
```
Compare them like prices, left to right. The first 19 digits are equal, then the hash has **0** where the target has **2**, so the hash is smaller ✓.

**Bits → target** (p. 10, CALCULATE). Block 968,391's header stores `c5 1e 02 17` (little-endian):

| Step | Value |
|---|---|
| backwards | `17 02 1e c5` = **0x17021ec5** |
| first byte (exponent) | 0x17 = **23** → the target is 23 bytes long |
| other three (coefficient) | `021ec5` = the first digits |
| target | `021ec5` followed by **40 hex zeros** (20 bytes), padded to 64 hex digits |

Formula *(my note, same thing written as maths)*: `target = coefficient × 256^(exponent − 3)` =
0x021ec5 × 256²⁰ = 0x021ec5 × 2¹⁶⁰. 23 bytes = 46 hex digits, so there are 64 − 46 = **18** leading zeros
before `021ec5` (which gives 19 zeros before the `2`). The slide's second diagram works a different
example, bits `1705dd01` → `05dd01` + 40 zeros. **Lower target = fewer good hashes = harder work.**

**The nonce, checked** (p. 11, live demo with week 4's `blockhash.py`): with nonce **3,682,494,035** the
hash starts with 20 zeros (below target ✓). With nonce + 1 the hash is `483cd7a0…` and has no leading zeros at all ✗.
*"The nonce is the winning ticket."*

**Four billion tries are not enough** (p. 12, CALCULATE):

| | |
|---|---|
| possible nonces | 2³² = **4,294,967,296** ≈ 4.29 × 10⁹ |
| tries needed (block 968,391) | ≈ **5.7 × 10²³** |
| nonce runs out | 5.7 × 10²³ ÷ 4.29 × 10⁹ ≈ **1.3 × 10¹⁴ times** |

So when all 2³² nonces fail, the miner changes a few free bytes in **its own transaction #0**. That changes
the Merkle root, so the header is new and 4 billion fresh nonces are ready. The time field also moves forward.

**Difficulty** (p. 13) = how many times harder today's target is than the first one of 2009 =
**first target ÷ today's target**.

```
first target   00000000ffff0000…   (bits 0x1d00ffff)
block 968,391  000000000000000000021e…   (bits 0x17021ec5)
difficulty = first ÷ today's = 132,757,073,449,488  ≈ 1.3 × 10¹⁴
```
- Block 968,391 needed about 1.3 × 10¹⁴ times more tries than the first blocks, **about 5.7 × 10²³ in all**.
- Today's difficulty, after the last adjustment: **140,577,680,051,920**.
- *(my note)* The formulas that connect the numbers:
  - **expected tries = difficulty × 2³²**. Check: 1.3276 × 10¹⁴ × 4.295 × 10⁹ = **5.70 × 10²³** ✓.
  - The "nonce runs out 1.3 × 10¹⁴ times" on p. 12 is therefore **just the difficulty again**.
  - Difficulty from bits: (0xffff ÷ 0x021ec5) × 2⁴⁸ = (65,535 ÷ 138,949) × 2.815 × 10¹⁴ ≈ 1.3276 × 10¹⁴ ✓.

**Hashrate** (p. 14) = hashes per second, of one machine or of the whole network.

| | rate | time for block 968,391's 5.7 × 10²³ tries |
|---|---|---|
| this laptop | 1,530,978 ≈ 1.5 × 10⁶ H/s | 5.7 × 10²³ ÷ 1.5 × 10⁶ ≈ **11.8 billion years** |
| the network | **1.0 × 10²¹** H/s | ≈ **9 minutes** (see errors below: it's 9.5) |

For comparison, the universe is about 13.8 billion years old. Real mining runs in halls of ASICs
(slide shows an Antminer S19 Pro: 104 TH/s, 3,400 W). *(my note)* Formula: **time = tries ÷ hashrate**.
The years figure uses 1 year ≈ 3.156 × 10⁷ s.

## Part 3: the miner's pay (pp. 16–21)

**Coinbase transaction** (p. 16) = the **first transaction (#0) of every block**, written by the miner. Its
input points to no earlier output (`0000…0000`), so its coins are new. It pays the miner. It has nothing to do with the
company called Coinbase. In block 968,391 (tx `6921665a…74ea`): one output of **318,883,485 sat** to
SpiderPool's address `1BM1sAcr…C2Qc`, plus **5 notes worth 0 sat** that other systems read.

**Subsidy vs reward** (p. 17):
- **Block subsidy** = the new coins a block may create, fixed by the rules: **3.125 BTC** today.
- **Block reward** = subsidy + every fee in the block. This is what the coinbase may pay out, **and not one satoshi more**.

```
subsidy                      312,500,000 sat
+ fees of 4,116 payments       6,383,485 sat
= block reward               318,883,485 sat ✓  = 3.18883485 BTC
```
Week 6's 1,356 sat fee is one of those 4,116 fees (4,117 transactions minus the coinbase). Every node checks
this sum, and a coinbase that pays more is rejected.

**Read the coinbase** (p. 18, CALCULATE). Transaction #0's input has no signature to carry, so the miner fills that space with:

| Bytes | Meaning |
|---|---|
| `03` | "3 bytes follow" |
| `c7 c6 0e` | backwards `0ec6c7` = **968,391**, the block height ✓ |
| readable text | `SpiderPool/1376/` |

*(my note)* Check: 0x0ec6c7 = 14 × 65,536 + 0xc6c7 (50,887) = 917,504 + 50,887 = 968,391. Block 0 did the same
(week 3: Satoshi's newspaper headline sat in exactly this spot). Miners still sign their blocks this way.

**Halving** (p. 19): every **210,000 blocks** (about every four years) the subsidy is cut in half. This has been fixed in the rules since 2009.

| From block | Date | Subsidy |
|---|---|---|
| 0 | 2009-01-03 | 50 BTC |
| 210,000 | 2012-11-28 | 25 |
| 420,000 | 2016-07-09 | 12.5 |
| 630,000 | 2020-05-11 | 6.25 |
| 840,000 | 2024-04-20 | **3.125** ← block 968,391 is here |
| 1,050,000 | 2028 (estimate) | 1.5625 |

- Measured: block 839,999 created 6.25 new BTC. Block 840,000, four minutes later, created only 3.125.
- The next halving is at block 1,050,000, **78,129 blocks from now**. *(my note: "now" = block 971,871, the same tip
  used on p. 25. At 10 min/block that is about 1.5 years away.)*
- *(my note)* Formula: **subsidy = 50 BTC ÷ 2^⌊height ÷ 210,000⌋**. For 968,391: ⌊968,391 / 210,000⌋ = 4 → 50/16 = 3.125 ✓.
- Side note on the slide: **HODL** = slang for holding coins through crashes instead of selling.

**Why 21 million** (p. 20, CALCULATE):
```
210,000 × (50 + 25 + 12.5 + …) = 210,000 × 100 = 21,000,000 BTC   (almost)
in satoshis, rounded down at each halving:
  = 2,099,999,997,690,000 sat = 20,999,999.9769 BTC
```
- The subsidy is a whole number of satoshis. **After 33 halvings it rounds down to zero**, and only fees remain.
- *(my note)* 50 + 25 + 12.5 + … is a geometric series = 50 ÷ (1 − ½) = **100**.
- The money supply is decided by a rule that every node checks in every coinbase, not by a bank or a vote.
- **Genesis block's coins**: block 0's 50 BTC went to `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`. They can never be spent,
  because the first program never added that coinbase to its UTXO set. People still send small amounts as a tribute: 66,961 payments,
  57.66531918 BTC received in total, **0 ever spent**. (*(my note)* So about 7.67 BTC of it are tributes.)

**Difficulty adjustment** (p. 21): every **2,016 blocks** (about two weeks) every node recomputes the target
from how fast the last 2,016 blocks came. If they came **too fast**, the target goes **down** (harder). If **too slow**, it goes **up** (easier).
That is why Bitcoin averages about 10 minutes per block however many machines join (week 3 measured 9.6 min).

| | |
|---|---|
| Last adjustment | block 971,712, 16 Oct 2026: difficulty **+5.92 %** |
| This period so far | 7.9 % done, average gap **579 s** |
| Next adjustment | block 973,728, about 30 Oct 2026; estimate **+2.0 %** |

*(my note)* Formulas:
- **new difficulty ≈ old × (2,016 × 600 s) ÷ (actual time for 2,016 blocks)** = old × 600 ÷ (average gap).
- The change is capped at ×4 or ÷4 per adjustment.
- 2,016 blocks × 10 min = 20,160 min = **14 days**.
- Check: 971,712 = 482 × 2,016 and 973,728 = 971,712 + 2,016 ✓.

## Part 4: races and attacks (pp. 22–27)

**Mining pool** (p. 22) = a group of miners who search together and share each reward by the work each one
did. They get a steady small income instead of a rare big win. Blocks in the last 7 days (measured 17 Oct 2026, **1,095 blocks**):

| Pool | Blocks | Share |
|---|---|---|
| Foundry USA | 263 | 24 % |
| AntPool | 243 | 22 % |
| F2Pool | 196 | 18 % |
| ViaBTC | 105 | 10 % |
| MARA Pool | 62 | 6 % |
| SpiderPool | 51 | 5 % |
| all others | 175 | 16 % |

**Whitepaper vs mainnet**: the 2008 whitepaper says "Proof-of-work is essentially one-CPU-one-vote". Last week,
**three pools wrote 64 %** of all blocks ((263 + 243 + 196) / 1,095 = 702 / 1,095 = 64.1 % ✓). But each pool is many
independent miners who can leave.

*(my note)* 1,095 blocks in 7 days instead of the expected 7 × 144 = 1,008. That is about 552 s per block, i.e. faster than 10
min, which fits the +5.92 % adjustment.

**Orphan block** (pp. 23–24) = a valid block that loses the race because another block at the same height was built on
instead. Its transactions go back to the mempool unless the winner holds them too, and **its miner gets nothing**. Causes:
network latency, propagation delay, many miners racing at once.
- Real case, **2026-10-14**: two blocks at height **971,345** were found at about the same time. One was F2Pool's (`…b1d2ff3e`,
  03:33:06 UTC). The other came from another miner (`…2cda3ee5`, valid, 19 leading zeros). Nodes split until **AntPool** built
  971,346 on F2Pool's at 03:47:02 (about 14 min later), and every node followed.
- *"When two blocks tie, the next block decides; the loser is orphaned."*

**Confirmation** (p. 25): a payment has one confirmation when it is in a block, plus one for every block on top.
**Rule every node follows: when there is a choice, take the chain with the most work in it.**

```
newest block   971,871
our block    − 968,391
             +       1
confirmations = 3,481        (week 6's payment)
```
*(my note)* Formula: **confirmations = tip height − block height + 1**.

**51 % attack** (pp. 25–26): one miner or group controls more than half of all hashing. It can build a **secret
chain** faster than everyone else (block 2′ pays itself instead of the shop), publish it once it is longer, and so
replace recent blocks, which undoes its own payments (**double spending**). What it **still cannot** do:
- spend anybody else's coins (there is no signature, week 4)
- create coins beyond the rules (every node checks every coinbase)
- rewrite old history cheaply (every block on top must be redone)

*"More than half of the work can rewrite recent blocks — never someone else's signature."*

**Why wait for six blocks?** (p. 27, CALCULATE). A miner with share *q* wins a given block with chance *q*, so it wins six in a row with chance **q⁶**:

| q | 1 block | 6 in a row: q⁶ |
|---|---|---|
| 10 % | 0.1 | 0.000001 (1 in 1,000,000) |
| 30 % | 0.3 | 0.00073 (1 in 1,372) |
| 45 % | 0.45 | 0.0083 (1 in 120) |

So services wait for about **six confirmations (about one hour)** before treating a large payment as final.
*"Each confirmation multiplies the attacker's odds by q."* (This is a simplification: see the errors section below.)

**War story: Bitcoin Gold, May 2018**: Bitcoin Gold is a separate, much smaller network that copied Bitcoin's design.
Someone rented enough machines to control more than half of its mining. They deposited coins at exchanges, traded them and
withdrew, then replaced the blocks that held the deposits. The reported loss was **over 18 million US dollars**, borne by the exchanges.
*"Security is the cost of the work: little work, little security."*

## Slide errors and loose claims

1. **p. 14, "the whole network ≈ 9 minutes"**: 5.70 × 10²³ ÷ 1.0 × 10²¹ = 570 s = **9.5 min**. If a quiz asks,
   compute it yourself. The laptop's 11.8 billion years is right only with the exact numbers (1,530,978 H/s). The
   rounded line "÷ 1.5 × 10⁶" actually gives about 12.0 billion years.
2. **p. 27, q⁶ is not the attacker's real success chance.** q⁶ is the chance of mining six blocks *in a row*. But
   an attacker doesn't need a streak: it only needs its secret chain to *eventually* overtake. Nakamoto's
   whitepaper (§11) gives for z = 6: q = 10 % → **0.00024**, q = 30 % → **0.13**, q = 45 % → **0.77** (my
   computation from his formula). q⁶ hugely understates the risk, especially at 45 %. Use the slide's q⁶ for quiz
   answers, but know it is the simplified model.
3. **p. 16, coinbase screenshot**: the explorer screenshot shows a coinbase of **3.17052829 BTC** with a "Foundry USA Pool" tag. That is a
   *different block*, not 968,391 (SpiderPool, 3.18883485 BTC). Use the numbers in the diagram, not the screenshot.
4. **p. 19, "the block reward gets smaller than 1 satoshi"**: it is the **subsidy** that shrinks to zero. The reward still
   includes fees. The slide's own definitions on p. 17 make this distinction.
5. **p. 20, "the bug is that Satoshi never programmed the genesis coinbase into the UTXO set"**: the fact is right, but
   calling it a *bug* is an interpretation. Nobody knows whether it was deliberate.
6. **p. 21, "estimate +2.0 %"**: from the slide's own average gap of 579 s, the naive estimate is 600 ÷ 579 − 1 ≈
   **+3.6 %**. The +2.0 % probably comes from a tracker using a different window. Don't try to reproduce it from 579 s.
7. **p. 5, miners as "governance body"**: this is debatable. Miners can signal for upgrades, but every full node enforces the
   rules, and a miner who breaks them has its blocks rejected (as p. 17 itself says about the coinbase).
8. **p. 6, "millions of tries"**: the demo's 4-zero puzzle needs about 16⁴ = 65,536 tries (it found nonce 72,608).
   "Millions" is true of real Bitcoin, not of this demo.
9. **pp. 23–24, "orphan block"**: *(my note)* strictly, a block that lost the race is a **stale** block. "Orphan" originally meant
   a block whose parent is unknown. The slides (like most textbooks) use "orphan", so use that word on the quiz.
