# Intro to Blockchain Technology, Part 2: Shared Ledgers, Blocks, Chains and Networks

**Blockchain · Week 3 · 51:05 · Dr. Jalolliddin Yusupov**
eClass: [VOD 71446](https://eclass.inha.ac.kr/mod/vod/view.php?id=71446) · slides are view-only ([71447](https://eclass.inha.ac.kr/mod/ubfile/view.php?id=71447))
Transcript: [.txt](week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%202).txt) · Subtitles: [.srt](week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%202).srt)
Follows [Part 1](week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%201).md).

---

## 🟡 Things he said that affect you

- **He watches who views what.** At recording time, 88 students had opened the
  syllabus and ~67 had watched the videos. **"If I don't like this, I might make
  watching the video compulsory."** Right now the VODs aren't
  progress-tracked (see [DEADLINES](../../../DEADLINES.md)), but that could change.
- **A quiz for this week is coming**, possibly with a demo. "Watch the videos,
  take your notes, and wait for the quiz." Quizzes are attendance.
- **Self-check at [20:17].** Pause, answer on paper and check against the slides.
  No answers are given. The questions are in the checklist at the bottom.
- **Term project preview:** you'll **pick a field in Uzbekistan and design a
  blockchain implementation for it**, "forget about the cryptocurrency".
- **"Print the terminology as a small sheet and keep it with you."** He'll give
  examples and ask whether they're centralized, decentralized or distributed.
- Consensus gets its own week, **week 6 or 7** ("these numbers are dynamic").

---

## 1. Who keeps the ledger? Everyone keeps a copy

The answer to Part 1's first question: **give every participant a copy.** Nobody can
quietly change it, and losing one copy doesn't matter.

| Card | Definition |
|---|---|
| **Shared ledger** | A ledger **many people keep together**, each holding a copy. |
| **Distributed ledger** | The technical name: the copies are **distributed over many computers**. |

Everyone owns it, so nobody owns it.

### The new problem: order

Suppose Malika pays shop A and shop B with the same coin milliseconds apart. Messages travel over
the internet at different speeds, e.g. to Tashkent vs. Khorasan. So **some copies
see A first and others see B first**, and a cheater can even show different
people different versions. Many copies are only useful if they **agree on one
order**.

> **Consensus:** the **agreement between all the copies about the order of
> records** in the ledger. The rules for reaching it are the **consensus rules**.
> His analogy: the class votes on the final timetable, then everyone copies
> that one.

## 2. Blocks — the pages of the notebook

- Nobody agrees on single transactions. Everyone agrees on **a whole page** at a time.
- **Block:** a **page in the shared ledger**, a group of transactions added
  together. The ledger grows **one block at a time**.
- Pages are **numbered strictly in sequence**, 41, 42, 43…

**Thought experiment.** Someone wants to slip a forged page 42 in between 41
and 43. Now there are two 42s, so he'd have to **renumber 43, 44 and every
page after it**. "The attacker has a very big problem," and the seal makes
this much worse (next section).

## 3. The seal and the chain

| Card | Definition |
|---|---|
| **Seal** | A short code **computed from the page's contents**. Think of laminating the page. **Change one letter and the seal comes out completely different.** Technically this is a **hash**, covered in week 4. |
| **Chain / link** | **Each block carries the seal of the block before it**, so blocks are linked in order. |

Sketch:

```
┌ Page 41 ──────────┐   ┌ Page 42 ──────────┐   ┌ Page 43 ──────────┐
│ prev: …           │   │ prev: seal(41)    │   │ prev: seal(42)    │
│ txs…              │ → │ txs…              │ → │ txs…              │
│ seal(41)          │   │ seal(42)          │   │ seal(43)          │
└───────────────────┘   └───────────────────┘   └───────────────────┘
```

Two protections come out of this:
1. **You can't change a page's contents**, because its seal changes.
2. **You can't swap in a forged page**, even if you somehow gave it a matching-looking seal:
   the *next* page stores the old seal (his example: `B09E`), and it won't match.
   That's why it's called a **block-chain**.

He compares it to a **linked list** with extras.

## 4. Blockchain ≠ cryptocurrency

**Blockchain** is the idea: a shared ledger, grouped into blocks, linked by seals.
Blocks can hold **anything**, not just payments. Blockchains fit **wherever many
parties must share one record that none of them control.**

| Field | Example he gave |
|---|---|
| Money | Cross-border payments with no bank |
| **Supply chain** | **Walmart traced a mango's origin in ~2 seconds** instead of 7 days |
| **Land registry** | Pilots in **Georgia** and **Sweden** |
| **Certificates** | Universities issuing diplomas on-chain, which are easy to verify |

He was candid that **many pilots died** (like Facebook's metaverse) because
"an ordinary database is enough." The end of the course covers which projects worked,
which failed, and what's happening in Uzbekistan.

### Formal definitions

| Card | Definition |
|---|---|
| **Blockchain** | A shared ledger **kept by many computers**, with transactions **grouped into blocks** that are **linked in order**. In one line: "a record many people keep together with **no single owner**." |
| **Cryptocurrency** | **Digital money whose ledger is a blockchain instead of a bank.** Its units are **coins**. The first coin appeared in **2009** (Satoshi Nakamoto). Today there are thousands. |
| **"Crypto"** | From **cryptography**, the science of secret codes and proofs. The seal is cryptography. Later, it will *prove* who owns a coin. |

### How blockchain answers Part 1's three questions

| Question | Answer |
|---|---|
| Who keeps the ledger? | **Many computers** |
| Who decides the order? | **Consensus** |
| Who stops cheating? | **The chain** makes cheating impossible, or at least visible, down to who did it |

## 5. Centralized vs decentralized vs distributed ⚠️ he'll test this

| Term | The question it answers | Meaning |
|---|---|---|
| **Centralized** | Who controls it? | **One party** controls the system and all records, e.g. a bank like NBU. Everyone connects to the centre. |
| **Decentralized** | Who controls it? | Control is **shared by many independent parties**. No one is in charge, and it keeps working if some leave. |
| **Distributed** | Where are the copies? | Copies are **spread across many computers**. |

> ⚠️ **He mis-speaks twice here [28:30–30:31]; the table above is the
> correct version.** He says "if it's many independent parties we call it
> *distributed*" (that's decentralized) and "banks are decentralized" (he
> immediately corrects himself). His actual point is **the trap:** a bank with
> servers in Tashkent, Bukhara and Samarkand is **distributed but still
> centralized**, because one party controls everything.

**Blockchain aims to be both:** *distributed* (many copies) **and** *decentralized*
(many owners). It depends on the type of blockchain.

## 6. The network — nodes, peer-to-peer, gossip

| Card | Definition |
|---|---|
| **Node** | A computer that **runs the blockchain program and keeps a full copy** of the ledger. |
| **Peer-to-peer (P2P)** | Computers connect **directly to each other as equals**. There's **no central server**. Compare BitTorrent. |
| **Gossip** | How news spreads. A transaction reaches one node, which **checks it against the rules** (e.g. is the money there?) and passes it to a **few** neighbours, not everyone. They check it and pass it on. Within seconds every node has it. |

**Nobody is believed. Everything is checked.** A node never accepts news just
because a neighbour sent it. Even if a liar recruits 100 accomplices, the first
honest node outside that group checks the message and rejects it.

## 7. DLT, immutability, and where trust comes from

- **DLT (distributed ledger technology):** the umbrella term for any ledger shared
  across many computers.
- **Every blockchain is a DLT, but not every DLT is a blockchain.** A blockchain adds
  blocks linked by seals.
- **Immutable / tamper-resistant:** history is very hard to change, and any change is
  **visible to every node**. Changing page 41 breaks the link stored in page 42.
  There are exceptions, covered later. The transcript garbles this as "temporary system"; he means tamper-resistant.

**With a bank you trust a company. With a blockchain you trust four things:**

1. **Many copies.** Thousands of nodes each hold the full ledger, and no single copy matters.
2. **Everyone checks.** Every node checks every transaction and block against public rules.
3. **The chain shows changes.** Each block carries the previous seal.
4. **Cheating costs more than it earns.** Rewriting a block is expensive, explained in coming weeks.

"We trust the mathematics, not the person."

## 8. Bitcoin and Ethereum — the course's two focus networks

| | Bitcoin | Ethereum |
|---|---|---|
| Started | First block **January 2009** | Covered from week 8 |
| Purpose | Digital money with no intermediary | A blockchain that **runs programs** (smart contracts), so it's **programmable** |
| Price when recorded | ~$85,000 | ~$2,500 |

- The network name and the coin name can differ. His example is Telegram's TON.
- **Most other blockchains copy ideas from these two.** Understand them and you
  can understand almost any chain.
- He personally prefers Ethereum. Expect a lot of **coding** later.

## 9. Block explorers — see it yourself

- **[mempool.space](https://mempool.space)** is a Bitcoin **block explorer**, a
  website that shows **every block and every transaction** of a public blockchain,
  for anyone to read. It works in Uzbekistan. Some other explorers, e.g. bitcoin.com, have
  been blocked there.
- **Block height** = the block's page number, i.e. **how many blocks came before
  it**, counting from **0** (the first block ever). He looked at one around 900,000.
- An explorer shows each block's **hash** (the seal), the **previous block's hash**,
  timestamp, size, and things coming later: weight, sat/vB, subsidy, fees, mining.
- You can see amounts moving between addresses, but **not who owns them**. Privacy
  is covered later.

---

## Self-check questions from [20:17]

Answer in your own words, on paper, as he asks:

1. What is a ledger, and what two things about it matter?
2. Why does digital money have a double-spending problem?
3. How does a bank stop it?
4. If everyone keeps a copy of the ledger, why do they also need consensus?
5. Someone secretly changes one line on page 41. What happens to page 42?

## Terminology sheet (his list, for the quiz)

- [ ] Shared / distributed ledger · consensus · consensus rules
- [ ] Block · seal (hash) · chain / link
- [ ] Blockchain · cryptocurrency · coin · why "crypto"
- [ ] **Centralized vs decentralized vs distributed**, including the bank trap
- [ ] Node · peer-to-peer · gossip
- [ ] DLT (blockchain ⊂ DLT) · immutability / tamper resistance
- [ ] The four sources of trust
- [ ] Bitcoin vs Ethereum · smart contracts (named only)
- [ ] Block explorer · block height · block hash
