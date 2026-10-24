# Cryptography for Blockchains

**Blockchain · Week 4 · 59:32 · Jalolliddin Yusupov**
Transcript: [txt](week04%20-%20Cryptography%20for%20Blockchains.txt) · Subtitles: [srt](week04%20-%20Cryptography%20for%20Blockchains.srt)
Slides: view-only on eClass (module 71795)

**This is "Lecture 4" in [Homework 1](../../homework/hw1/README.md). It covers Parts 3, 4 and 5.**

---

## 🥚 The hidden message: [17:34–18:25]

Mid-way through the hash-function section he stops and says he's leaving an
**easter egg**:

> **"Why do Lubuntu ISO files come with SHA-256 hash values?"** The first person
> to message him the answer gets 1 point.

**That point is gone.** The eClass note says another student was first,
and two others also answered. The answer is in section 3 below.

**The second easter egg, which matters more [34:46]:** for hard quiz, homework and
project questions he hides **small notes in his slides, "in very short letters
and without any example"**, and mentions them only once, out loud. His example is
the **odd-number-of-leaves rule for Merkle trees** (section 5). It appears in
**HW 4.4**, which even says *"Use Bitcoin's rule (told you so xD)"*. Expect more of these.
**Read the small print on his slides, and listen for "I told you this in the lecture".**

---

## 1. Finishing the header [00:00]

- **Merkle root:** a 32-byte fingerprint of *every* transaction in the body. It is
  the **only link between the header and the body**. Add, remove or change any
  transaction and the root changes, so the header changes, so the block hash changes.
- **Bits and nonce** concern **making** the block (mining), not payments. They
  are the reason block hashes start with zeros. Covered later, around week 6.
- **All headers of all of Bitcoin:** ~969,000 × 80 bytes ≈ **77–78 MB**. Small
  enough for a phone to keep the whole "skeleton" of the chain and check that it isn't broken.

## 2. Cryptography and Caesar [04:09] → HW 5.1

- *Kryptos* means hidden and *graphein* means to write.
- **Caesar cipher:** shift every letter forward by the **key**. With key 3,
  `INHA` → `LQKD`. Decrypt by shifting **back** by the same key.
- **Symmetric:** sender and receiver use the **same key**. The weakness is that
  they must share it first, e.g. Caesar meeting Cleopatra in person to tell her "3".
- His slide has a line encrypted with key +7 for you to decrypt by hand. That's **HW 5.1(b)**.
- **In blockchain, cryptography doesn't hide anything. Everything is public.** It is used to **prove** two things:
  1. **The data is exactly what was written.** This uses **hash functions**.
  2. **The payer really owns the coins.** This uses **digital signatures**.

## 3. Hash functions and SHA-256 [10:15] → HW 3.1, 3.2

A hash function is a black box: **any data in, a short fixed-size fingerprint
out**. Bitcoin uses **SHA-256**: 256 bits, which is 32 bytes or **64 hex characters**.

Terminal demo:

```bash
printf "Inha University in Tashkent" | shasum -a 256   # Linux: sha256sum
```

**Use `printf`, not `echo`.** `echo` silently adds a newline, so you get a
different hash. He tripped over this live.

**The promises a good hash function makes.** HW 3.2 and 3.3 ask you to *name* one, so know them by name:

| # | Promise | Meaning |
|---|---|---|
| 1 | **Deterministic** | The same input gives the same hash, today, tomorrow and on any computer |
| 2 | **Fixed size** | Any input size gives the same output size. **Even empty input has a hash.** A 1-byte letter and a 40 GB movie both give 64 hex characters |
| 3 | **Avalanche effect** | A tiny change in the input changes **about half** of the output. In his demo, only **7 of 64** characters stayed the same |
| 4 | **One-way (preimage resistance)** | You can't get the input back from the hash, any more than you can un-blend a smoothie. The only attack is guessing |
| 5 | **No twins (collision resistance)** | Two different inputs with the same hash are **practically impossible** to find |
| + | **Fast** | Millions of hashes per second on a laptop |

All five must hold for the fingerprint to be useful. This is **not** the
data-structures hash table, which only spreads keys evenly.

**The Lubuntu answer:** big downloads publish their SHA-256 so you can **hash the
file you downloaded and compare**. A match means the file is **exactly** the one
published, with no corruption or tampering (promises 1, 3 and 5).

**Toy hash [22:27] → HW 3.4:** add the digits and keep the last digit. It has only 10
possible outputs, so **twins are trivial to find**. SHA-256 has 2²⁵⁶ outputs.
Twins must exist mathematically, since there are more inputs than outputs, but
nobody has ever found one.
**Quantum computers** are a looming threat to today's cryptography. "Not for this course."

**A better toy, used in the homework:** `T(a, b) = (31·a + b) mod 97`.

## 4. Computing a real block hash [28:37] → HW 3.3

- **Block hash = SHA-256( SHA-256( 80-byte header ) )**, i.e. hashed **twice**,
  then shown with the bytes **reversed**. That's the `[::-1]` in `blockhash.py`.
- Take "Block Header Hex" from mempool.space (160 hex characters = 80 bytes) and run
  the script. The result equals the explorer's hash, **zeros at the start and all**.
  You've just done what every node does.
- Change **one** character of the header and the hash is completely different,
  and the leading zeros are gone. This is the avalanche effect (promise 3).

## 5. Merkle trees [30:38] → HW Part 4

- **Why not hash the whole body at once?** It would protect everything, but to check
  **one** payment a phone would need the whole ~1.5 MB body.
- **Merkle tree:** hash each transaction, hash the hashes **in pairs**, and repeat
  until one value is left. That value is the **Merkle root**. Named after
  **Ralph Merkle (1980)**.
- **⚠️ The hidden rule:** if a level has an **odd** number of values, **pair the
  last one with a copy of itself**. This is the exact rule HW 4.4 relies on.
- **Worked example** with T and leaves **65, 66, 67, 68**: T(65,66) = **44** and
  the right pair gives **11**. The transcript loses which pair is which, so check the
  slide. The root is **17**. Change leaf 66 to **88** and the left pair becomes
  **66** and the root becomes **20**.
  **A change at one leaf climbs all the way to the root.**
  (Check: 31·65 + 66 = 2081 = 21·97 + 44 ✓, matching the handout's example.)
- He verified a real 2010 block with exactly 4 transactions in Python, and it matches mempool.space.
- **Merkle proof:** to prove one transaction is in the block, you only need the
  **sibling hash at each level** on the way up. Recompute up to the root and
  compare it with the root in the header.
  - Proof length = **number of levels = ⌈log₂ n⌉** hashes, each 32 bytes.
  - 4 transactions → 2 levels; 8 → 3; about 1,000 → 10.
  - **6,000 (his 6,816-transaction block) → 13 hashes = 416 bytes**, instead of about 1.5 MB.
  - **The proof grows with the number of levels, not the number of payments.**
  - Practice from the slide: work out the proof size for 3,000 transactions and for 1,000,000. → **HW 4.5**

## 6. Keys and digital signatures [42:52] → HW 5.2, 5.3

- **The problem:** the ledger is public, so anyone could *write* "Aziz pays me $5".
  A pasted image of a signature proves nothing on a computer.
- **What a signature needs:**
  - only the owner can make it;
  - **everyone can check it** without learning the owner's secret;
  - it fits **only that one message**, so it can't be copied onto another.
- **Public-key (asymmetric) cryptography, 1976:**
  - The **private key** is secret and only the owner has it. It is used to **sign**.
  - The **public key** is computed from the private key and shared openly. It is used to **verify**.
  - (Caesar, by contrast, is **symmetric**: one shared key.)
- **Sign:** `signature = f(message, private key)`. In practice the
  message is hashed first and the 32-byte hash is signed.
- **Verify:** anyone with the **message, the signature and the public key** gets yes or no. They never need the private key.
- **What a signature proves:** **who** agreed (only the private-key holder could
  have signed), that the message is **unchanged** since signing, and that the
  signer **can't deny it**.
- **What it does *not* do:** **it doesn't hide or encrypt the message.**
  Everyone can still read "Aziz → Timur · 5".
- Every node checks every signature. **A transaction without a valid signature is never put into a block.**
  Timur can write "Aziz → Timur" but **can't produce Aziz's signature** for it.
- **Where keys come from:**
  - **private key** = a random 256-bit number;
  - **public key** = computed from it, easy one way and **infeasible to reverse**;
  - **address** = **hash of the public key**.
  So private key → public key → address, each step one-way.
- **Lose the private key and you lose the coins.** There is no bank to reset
  it, because there is no middleman, and people have lost millions this way.
  Securing keys will be covered with wallets.

## His "at home" list (now Homework 1)

At [57:08] he lists what became the homework:
- SHA-256 of your student ID;
- run `blockhash.py` on your block's header;
- draw a Merkle tree by hand and change a leaf;
- decrypt the Caesar message by hand.
