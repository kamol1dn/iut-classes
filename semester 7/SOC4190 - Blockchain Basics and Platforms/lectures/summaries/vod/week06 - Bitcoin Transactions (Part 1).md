# Bitcoin Transactions (Part 1)

**Blockchain · Week 6 · 50:06 · Jalolliddin Yusupov**
Transcript: [txt](../../vod/week06%20-%20Bitcoin%20Transactions%20(Part%201).txt) · Subtitles: [srt](../../vod/week06%20-%20Bitcoin%20Transactions%20(Part%201).srt)
Slides: [pdf](../../slides/week06%20-%20Bitcoin%20Transactions%20(slides).pdf) · Source files: [`resources/week06 - Bitcoin Transactions source/`](../../../resources/week06%20-%20Bitcoin%20Transactions%20source/README.md)

Last week he checked a payment's *signature*. This week he opens the payment up to see what was actually
agreed: where the coins are before and after, what the fee is and where it's written, what the 225 bytes
mean, and what a txid is. **Locks** (who can spend an output, addresses starting with `1`, and what went wrong in 2014) are
left for Part 2.

---

## 🥚 Hidden messages and small print

- **No easter egg** in this part.
- **Flagged as "I will definitely ask"** [12:50], at the project defence rather than the exam: **the transaction fee is not
  written anywhere in the transaction.** It's computed as Σ inputs − Σ outputs.
- **Flagged as likely question types:**
  - **sats ↔ BTC conversion** [04:20]: "sometimes I give you this kind of exercise". 0.01 BTC = 1,000,000 sats.
  - **little-endian decoding** [42:55]: "you can expect this kind of questions". You get a raw output amount and have to read the
    bytes backwards to get the number.
- **Homework count** [05:00]: about **21 of ~280** had submitted HW1 when he recorded this. "Homeworks will be quite hard… please speed up."

## 1. Banknotes and the satoshi [01:00]

- Analogy: you hold 50k + 20k sum notes and lunch costs 60k. You can't tear a note, so you hand over **both** and
  get **10k change**. Bitcoin works the same way: coins are spent **as whole notes** and change is created.
- **1 BTC = 100,000,000 satoshis (sats).** The ledger stores every amount as a **whole number of sats**, never a fraction.

## 2. Outputs, inputs, change [06:00]

| Term | Meaning |
|---|---|
| **Output** | A new "banknote" the transaction creates: an **amount in sats + a lock** (in practice an address) saying who may spend it. Numbered 0, 1, 2… |
| **Input** | A **pointer to an earlier transaction's output** (txid + output index). It spends that output **whole**. |
| **Change** | The output that sends the rest back to the payer. **Nothing marks it as change** on-chain. The wallet builds it, and you recognise it because it pays the sender's own address. Not writing a label saves space. |

## 3. The fee [12:00]

- In the lecture's example, inputs − outputs = **1,356 sats** "missing". That's the **transaction fee**, left for the **miner** who writes the block.
- **No field holds the fee.** Anyone can compute it, so writing it would waste block space (a recurring theme: **keep the chain small**).
- He contrasts this with bank fees (hidden, large). Bitcoin's fee has a clear incentive, covered in the mining lecture.
- **Fees follow size in bytes, not value** [26:40]. They rise when the network is busy and fall when it's quiet (evenings, weekends).

## 4. UTXO and the UTXO set [16:40]

- **UTXO = unspent transaction output.** Every bitcoin in existence sits in some UTXO.
- **The UTXO set** is the list of all of them, and **every node keeps it**.
- **There is no balance field.** Your wallet finds every UTXO locked to your addresses and adds them up (back to lecture 1: the balance is computed, not stored).
- **Every coin has a history**: trace inputs backwards through earlier transactions, like a banknote passing shop → market → salary → bank. At the root, coins are *created* (mining lecture).
- "Every output is **born in one payment and dies in another**."

## 5. Double spending, solved [22:40]

- **An output can be spent once.** A node rejects a payment whose input points to an output **not in its UTXO set** (already spent, or never existed).
- If two payments try to spend the same output, only one is accepted. *Which* one is decided by mining (later lecture).

## 6. Consolidation [24:30]

- Many small UTXOs (like a pocket of small notes) can be merged: **many inputs → one output to yourself**. You still pay a fee.
- Example on screen: one transaction with **30 inputs** → 1 output.
- Why bother: spending 30 UTXOs later means 30 inputs, a bigger transaction and a bigger fee. Do it **while fees are low**.

## 7. The $3 million fee [28:40]

- A user "with a faulty wallet" (or building the payment by hand) **forgot to add a change output**, so the whole unclaimed remainder became the
  **fee, about $3 M**. AntPool mined the block and offered to return it to anyone who could prove ownership with the private key. He believes it was returned.
- Compare the lecture example: **1,356 sats ≈ 13 sum**.
- Lessons: **whatever the outputs don't claim becomes fee, and it can't be undone.** Use reputable wallets, don't build payments
  by hand with real coins, and **keep the large-fee warning switched on**.

## 8. Inside the raw transaction: 225 bytes [35:00]

The **raw transaction** is the bytes exactly as nodes send and store them: 225 bytes = **450 hex characters**.

| Field | Size | In the example |
|---|---|---|
| version | 4 B | `02000000` → **2** |
| input count | 1 B | 1 |
| ↳ previous txid | 32 B | stored **reversed** |
| ↳ output index | 4 B | `01000000` → **1**, so it spends output #1 of that earlier tx |
| ↳ script length | 1 B | `6a` → **106** bytes follow |
| ↳ unlocking data | 106 B | 1 + ~71-byte **signature** + **public key**: the proof you may spend it |
| ↳ sequence | 4 B | `ffffffff` = default, nothing special |
| output count | 1 B | `02` → **2** |
| ↳ amount | 8 B | e.g. 1,000,000 sats |
| ↳ lock | — | contains the **20 bytes** behind the receiver's address (output 0), then the sender's (output 1 = change) |
| locktime | 4 B | earliest block it may enter. **0 = any time** |

- The chain stores **20 bytes, not the address text**. Explorers render the address for display.
- **No fee field anywhere.** That's the point of the walk-through.

## 9. Little-endian [40:40]

- Bitcoin writes multi-byte numbers **smallest byte first**, the way most CPUs hold them in RAM, so no conversion is needed
  (and arithmetic starts from the low byte). **To read a number, reverse the byte order**, then convert from hex.
- Example: version `02 00 00 00` → `0x00000002` = 2.

## 10. The txid [47:00]

- **txid = SHA-256(SHA-256(raw bytes)), written backwards** → 64 hex characters, the same way the block hash works.
- **Nobody assigns it.** Every node computes it. Inputs reference outputs **by txid + index**, so changing any byte changes the txid.
- Demo files: `txid.py` on `payment.hex` vs `payment_plus1.hex` (one hex digit changed) → completely different txids.

---

**Next (Part 2): locks.** How an output is locked and unlocked, `1…` addresses, and the 2014 problem.
