# Bitcoin Transactions (Part 2)

**Blockchain · Week 6 · 57:22 · Jalolliddin Yusupov**
Transcript: [txt](../../vod/week06%20-%20Bitcoin%20Transactions%20(Part%202).txt) · Subtitles: [srt](../../vod/week06%20-%20Bitcoin%20Transactions%20(Part%202).srt)
Slides: [pdf](../../slides/week06%20-%20Bitcoin%20Transactions%20(slides).pdf) · Part 1: [md](week06%20-%20Bitcoin%20Transactions%20(Part%201).md) · Source files: [`resources/week06 - Bitcoin Transactions source/`](../../../resources/week06%20-%20Bitcoin%20Transactions%20source/README.md)

**Locks and keys**: how an output is locked and unlocked (Script, P2PKH, P2SH), how a `1…` address is
built, transaction malleability and Mt. Gox (2014), the SegWit fix, and **weight / vbytes / fee rate**.

---

## 🥚 Hidden messages and small print

- **No easter egg** in this part.
- **Promised practice material** [46:50, 56:55]: he'll put **"a lot of HTML games"** on eClass to practise
  on (a raw-tx decoder, a vbyte calculator), plus **lab sessions** on Script. Watch for new eClass items.
- **"You have to remember this"** [18:17]: **Base58Check**, which drops look-alike characters (0/O, I/l) and adds a 4-byte checksum.
- His numbers in the fee example don't quite line up on screen. The consistent reading is
  **1,356 sats / 225 vB ≈ 6.03 sat/vB** (legacy) vs **980 sats / 141 vB ≈ 6.95 sat/vB** (SegWit).

## 1. Demo: txid.py [00:00]

`python txid.py payment.hex` → `d9f91d3f…`. Running `payment_plus1.hex` (one hex digit changed) gives a completely
different txid. **Any change to the bytes changes the ID**, so nothing can be altered unnoticed.

## 2. Locks and keys [02:40]

- **Locking script** (scriptPubKey) sits in every **output**: a tiny program saying what must be shown to spend it.
- **Unlocking script** (scriptSig) sits in every **input**: the data that satisfies the lock, here the **signature (~71 B) + public key**.
- **Every node runs key + lock** before accepting the payment. There's no central authority, because public-key crypto is the barrier.
- A wallet doesn't hold money. It holds **keys**.

## 3. Script [06:00]

- Bitcoin's own **stack-based scripting language**: **no loops, no files, no network, on purpose**, so any device can run it without installing an interpreter.
- A glimpse of programmable money (escrow, multisig). **Ethereum takes this much further.**

## 4. P2PKH, pay-to-public-key-hash [08:00]

The classic **25-byte** lock: *"show the public key that hashes to these 20 bytes, and a signature made with it."*

```
76        OP_DUP          copy the top item
a9        OP_HASH160      hash it → 20 bytes
14        push 0x14 = 20 bytes of data follow (there are no separators in raw hex)
<20 B>    receiver's public-key hash
88        OP_EQUALVERIFY  top two equal? else fail
ac        OP_CHECKSIG     signature valid for this pubkey + payment? → TRUE
```

**Stack evaluation** [18:30], unlocking data first:

1. push **sig**, push **pubkey**
2. `OP_DUP` → sig, pubkey, pubkey
3. `OP_HASH160` → sig, pubkey, hash(pubkey)
4. lock pushes **expected 20 B**
5. `OP_EQUALVERIFY` → the two hashes must match, or fail
6. `OP_CHECKSIG` → **TRUE** left on the stack, so the coins move

## 5. Building a `1…` address [16:20]

**public key → SHA-256 → RIPEMD-160 (20 B) → Base58Check** (version byte `0x00` gives the leading **1**, plus a **4-byte checksum**,
and **no 0/O/I/l**). The same 20 bytes sit inside the P2PKH lock.

## 6. P2SH, pay-to-script-hash [26:40]

- Locks coins to the **HASH160 of a whole script** instead of a single key. Addresses start with **`3`**.
- Example: a **105-byte 2-of-3 multisig** script (any 2 of 3 listed keys must sign). Use case: company funds.
- **The sender pays nothing extra**: they just send to a short `3…` address. **The spender reveals the full script** plus the signatures, and pays for that size.

## 7. Transaction malleability and Mt. Gox [32:30]

- **The signature can't sign itself**, yet it was inside the bytes hashed into the **txid**.
- So a third party could **re-encode the signature** (e.g. tweak its *s* value; still valid, now 72 B) → **same payment, different txid**.
  Anyone tracking the payment by its ID thinks it vanished.
- **Mt. Gox** (Tokyo, the largest exchange): halted withdrawals on **7 Feb 2014**, blamed malleability on **10 Feb**, went bankrupt,
  reportedly losing **~850,000 BTC**. Later research watching the network found only **~386 BTC** actually taken this way. The flaw was real, but probably not the main cause.
- Lessons: **don't track payments by txid alone; check the evidence.** Coins held by an intermediary are only as safe as the intermediary (hardware wallets come later).

## 8. SegWit: the fix (2017) [40:30]

- **Segregated Witness** moves the signature + public key into a separate **witness** section that is **not hashed into the txid**. It's still sent and checked by every node.
- Our payment as SegWit: **113 B** of core data (version, inputs, outputs, locktime) + **2 B** marker/flag + **108 B** witness = **223 B**.
- SegWit addresses start with **`bc1`** and use **Bech32** (lowercase + digits, stronger typo check).

## 9. Weight, vbytes, fee rate [43:00]

- **Weight** = non-witness bytes × **4** + witness bytes × **1**. A block holds **4,000,000 weight units**.
- **Virtual bytes (vB)** = weight ÷ 4.
  - Legacy 225 B → 900 WU → **225 vB**
  - SegWit (113 + 2 core, 108 witness) → **≈ 141 vB**, about **63% of the room**
- **Fee rate = sats per vB.** Miners fill the limited block space with the **highest fee rates** first (mining lecture).
- **You pay for space, not for value**: moving $1 M or $10 can cost the same. A 30-input payment costs more than a 1-input one.
- Example: legacy **1,356 sats / 225 vB ≈ 6.03 sat/vB** vs SegWit **980 sats / 141 vB ≈ 6.95 sat/vB**. SegWit pays **less in total** but a **higher rate**, so the miner picks it first.
- Mempool snapshot [55:00]: a quiet network ≈ **8 sat/vB (~$0.76)**, medium priority ≈ **11 sat/vB**.

---

**Next: mining.** Who picks which payment, where new coins come from, and fee competition.
