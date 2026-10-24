# Bitcoin: Where It Came From, and What a Block Is

**Blockchain · Week 4 · 1:04:15 · Jalolliddin Yusupov**
Transcript: [txt](week04%20-%20Bitcoin%20-%20Where%20It%20Came%20From,%20and%20What%20a%20Block%20Is.txt) · Subtitles: [srt](week04%20-%20Bitcoin%20-%20Where%20It%20Came%20From,%20and%20What%20a%20Block%20Is.srt)
Slides: view-only on eClass (module 71743)

**This is "Lecture 3" in [Homework 1](../../homework/hw1/README.md). It is the whole basis of Part 2**
(your block on mempool.space). The hidden-message easter egg was in the *other*
week-4 video, [Cryptography](week04%20-%20Cryptography%20for%20Blockchains.md).

---

## 1. Where Bitcoin came from [02:01]

- **2008-09-15:** Lehman Brothers fails (from last week).
- **2008-10-31**, six weeks later: a **9-page paper**, *Bitcoin: A Peer-to-Peer
  Electronic Cash System*, is posted to a cryptography mailing list. It names no
  company, university or funding. The idea in its first line: send electronic cash
  **directly from one person to another without a financial institution**.
- A **white paper** is a short document that describes a system and how it works.
  (bitcoin.org is blocked in Uzbekistan, but the PDF is easy to find.)
- The author is **Satoshi Nakamoto**, a **pseudonym**. Nobody knows who it is, or whether it was one person or a group.
- 2009–10 he improves the software with volunteers on GitHub. **2011: he goes silent.**
  He holds a large number of coins and is presumably a billionaire.
- **Why it matters:** Bitcoin has run for about 17 years **without its
  inventor**. The community maintains it. This is "no single owner" in practice.

## 2. Satoshi combined old ideas [14:13]

He invented very little. He **combined about six existing ideas**:

| Idea | Year |
|---|---|
| Merkle trees | 1980 |
| Digital time-stamping | 1991 |
| b-money (a shared ledger with no bank) | 1998 |
| Hashcash (proof of work) | 2002 |
| Public-key crypto and digital signatures | 1970s |
| Peer-to-peer networks | ~2000 |

His aside: when you use someone's idea, **cite it**. That is "our main rule for this project".

## 3. The genesis block and early history [16:15]

- **Genesis block** = the first block of any blockchain, **height 0**. Every other
  block links back to it. Its **previous-block-hash is all zeros**.
- Bitcoin's genesis block: **3 Jan 2009**, **285 bytes**, **one transaction**
  that created (minted) **50 BTC**.
- **The hidden message:** inside that first transaction Satoshi embedded
  *"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"*.
  Two usual readings:
  1. It **proves the block wasn't made before that date**, since you can't predict a newspaper headline.
  2. It is a silent statement of **why** the system was built.
  Try it yourself: type `0` into mempool.space.
- **12 Jan 2009, block 170:** Satoshi sends **10 BTC to Hal Finney**, the first
  person-to-person transaction. (The transcript says "107", but it is block 170.)
- **We know Hal's address only because he posted it on a forum.** Addresses are
  pseudonymous, so **don't share yours**.
- **22 May 2010, Bitcoin Pizza Day:** László Hanyecz pays **10,000 BTC for two
  pizzas**. At today's prices that is hundreds of millions of dollars.
- **Rhythm:** about 18 years from block 0 to block ~969,432 works out to **about
  577 s per block**, i.e. roughly 10 minutes, nonstop, with no weekends or maintenance windows. → **HW 2.4(c)** uses the
  same method: `(timestamp − 1,231,006,505) ÷ H`.

## 4. Why does it have a price? [30:31]

His "jaydara" (street-level) explanation uses pencils. They are worth nothing
until people believe they will be worth something later. Then they sell for
1 cent, then 10 cents to someone with **FOMO** (*fear of missing out*), and so
on. "Bitcoin has no value" in itself. **The price is trust plus speculation.**
He promises a more academic treatment later.

## 5. What "Bitcoin" means [36:36]

The word means four things, and all are correct:
- **network**: thousands of nodes connected as equals;
- **ledger**: the blockchain;
- **coin**: BTC, the unit;
- **protocol**: the rules.

The rules live in open software, and a computer running that software is a **node**. By habit,
**Bitcoin** with a capital B means the system and **bitcoin** in lowercase means the coin.

**Three roles** (one computer can play several):
- **Users** create transactions.
- **Nodes** check everything and keep the full ledger.
- **Miners** pack waiting transactions into blocks.

A miner **cannot force a bad block** on anyone, because every node re-checks every block.

## 6. Anatomy of a block [38:36] → HW Part 2

A block is a **header** (small, **fixed 80 bytes**) plus a **body** (the list of transactions).

- **Body:** the lines of the ledger. His example block has **6,816
  transactions and about 1 MB**. Each transaction has an ID. **The first
  transaction in every block creates the new coins** (the coinbase).
- **Header: six fields, 80 bytes.**

| Field | Bytes | Meaning |
|---|---|---|
| **Version** | 4 | Which set of rules the block follows (like a Python version). Rises as features are added. |
| **Previous block hash** | 32 | Fingerprint of the parent block. **This one field *is* the chain.** |
| **Merkle root** | 32 | One fingerprint for all transactions in the body (next lecture) |
| **Timestamp** | 4 | When the block was made, in **Unix time** |
| **Bits** | 4 | How hard the block was to make (the target) |
| **Nonce** | 4 | A counter the miner keeps changing (mining, later) |

4 + 32 + 32 + 4 + 4 + 4 = **80**. He asks you to check this.

## 7. Timestamps and Unix time [48:48] → HW 2.2

- A timestamp is **seconds since 1 Jan 1970 00:00 UTC**.
- It is set by the **miner's own clock**, so it's approximate. Hours or minutes
  off is tolerated, days are not.
- **Converting by hand** (slide "When was block 0 made?"):
  1. Divide the seconds by 86,400 to get whole days plus a remainder.
  2. Count the days year by year from 1970, **remembering leap years**, to land on the date.
  3. Divide the remainder by 3,600 for hours, then by 60 for minutes, and the rest is seconds (UTC).
- Genesis timestamp is **1231006505**. Check with `date -d @1231006505` on Linux.

## 8. Block hash and the chain [54:58] → HW 2.3, 3.3

- **Block hash** = the real name for the "seal". It's a 32-byte fingerprint of the
  **80-byte header**, written as 64 hex characters.
- **It is not stored in the block's own header.** Anyone can recompute it from the header.
- **Real hashes start with many zeros. That's not an accident** (mining, later).
- Demo: Anders Brownworth's blockchain demo (andersbrownworth.com/blockchain).
  Change one transaction and that block's hash changes. The next block's
  "previous hash" no longer matches, and **every later block breaks**.
- **Drawing exercise from the slides:** three consecutive blocks side by side,
  each with its own hash and its previous hash, plus arrows. The parent's hash
  must equal the child's "previous block hash". That's exactly **HW 2.3**.
- **10 minutes is an average, not a timetable.** Neighbouring blocks can be
  seconds apart, or much longer. → **HW 2.4(d)**.

## Asides

- Long tangent on research careers: papers, citations and h-index. He says Prof.
  Farrukh Otamuratov at Inha is among the top researchers in Uzbekistan, and that
  "PhD is the best part of your life".
- He pauses the recording often, so his clothes sometimes change mid-video.
  He recommends watching at your own pace and pausing to digest.
- Questions go in the **Q&A section**, not email or direct messages.
