# Week 6: Bitcoin Transactions (slides)

**Blockchain · Week 6 · 34 pages · Dr. Jalolliddin Yusupov**
Source: [week06 - Bitcoin Transactions (slides).pdf](../slides/week06%20-%20Bitcoin%20Transactions%20(slides).pdf) *(5.7 MB)*

**Unlike every earlier deck, this one is downloadable** (eClass module 72453, a real PDF). Most
pages are diagrams with little extractable text, so this summary is built from the text layer plus
the page titles. **Read the PDF itself for the byte maps on pp. 16–19 and 23.** He has said hard
quiz questions come from small notes on the slides.

Video: *Bitcoin Transactions (PART 1)*, 50:06, is on eClass. A second part is still "being rendered".
**[QUIZ] 2 Week 6 (2%) opens 10-18 09:54 and closes 10-25 23:59** (1 attempt, 1 h). It counts
as this week's attendance.

## The six questions the lecture answers

He works through **one real 225-byte payment** from block **968,391** (the one whose signature
was checked in week 4's lecture):

| Stop | Question | Answer |
|---|---|---|
| The coins | Where are the coins before and after? | In **outputs**: new "banknotes", each locked to an address and **spent whole** (UTXOs) |
| The cost | Who pays the fee, and where is it written? | `fee = Σinputs − Σoutputs` = **1,356 sat**. It is **written nowhere** |
| The bytes | What do its 225 bytes say? | version · 1 input · 2 outputs · locktime (last 4 bytes). **TXID = SHA-256 applied twice** |
| The lock | What stops anyone else spending? | A **locking script**: P2PKH, a public-key hash that only a matching signature opens |
| The address | How is a `1…` address made? | **SHA-256 → RIPEMD-160 (= HASH160) → Base58Check** |
| The size | What went wrong in 2014, and what does block space cost? | **Malleability** (Mt. Gox), fixed by **SegWit**. Fee = size (vB) × fee rate |

## Part 1: coins as banknotes (pp. 3–14)

- New words: **satoshi**, **output**, **input**, **change**, **transaction fee**, **UTXO**.
- **Change** is not marked anywhere on chain. The wallet adds it automatically, and you only spot it
  because it goes back to the sender.
- **No balance is stored.** Your wallet finds every UTXO locked to your addresses and adds them up.
- **Double spend caught**: each output can be spent once. Every node keeps the UTXO set. An input
  pointing to an output not in the set is rejected. If two payments race, the first one written into a block wins.
- *Every coin has a history*: on 24 Sep 11:49 UTC the payment spent one old output and made two new
  ones. Both were spent again by 14:55 the same day.
- **War story: the 83 BTC fee** (≈ $3.15 M). The transaction was about half the size of ours and paid
  6 million times more. The cause was a faulty wallet. On 30 Nov 2023 Antpool offered a refund if the owner proved ownership
  by signing a message with the private key.

## Part 2: the payment byte by byte (pp. 15–20)

- **Raw transaction**: 225 bytes = 450 hex characters, exactly as nodes relay it and blocks store it.
- **Little-endian**: amounts are stored with the least significant byte first.
  *Exercise on p. 17: output #1's amount is `2c 2c 0c 00 00 00 00 00`. Which number is it?*
- **TXID**: nodes compute it from the bytes, and nobody assigns it. Change the amount by 1 sat and only 3 of 64
  hex characters still match (week 4's avalanche effect). Inputs reference outputs by
  **(TXID, output index)**, so changing one byte orphans every later spend.

## Part 3: locks and keys (pp. 21–27)

- **Script / opcodes.** The P2PKH lock uses four opcodes:

  | Byte | Opcode | Does |
  |---|---|---|
  | `76` | OP_DUP | copy the top item |
  | `a9` | OP_HASH160 | replace the top item with its 20-byte hash |
  | `88` | OP_EQUALVERIFY | the two top items must be equal, or stop with FALSE |
  | `ac` | OP_CHECKSIG | does the signature fit this public key *and this payment*? |

  So the locking script is `OP_DUP OP_HASH160 <20-byte pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG`.
  The spender supplies `<sig> <pubKey>`. **p. 25 is a DRAW slide** ("Running P2PKH, step by step"):
  practise drawing the stack, since it's very likely on a quiz or homework.
- The address's 20 bytes are the same ones that sit inside the lock of the coin it spent.
- **P2SH** (addresses starting with `3`): the lock holds only the HASH160 of a longer script (e.g.
  2-of-3 multisig). The spender reveals the script and pays for it.

## Part 4: a bug, its fix, and the price of space (pp. 28–33)

- **Transaction malleability**: replacing the signature's `s` with `n − s` still verifies, but the
  signature grows from 71 to 72 bytes and the **TXID changes**, because the signature is part of the bytes that get hashed.
- **Mt. Gox, Feb 2014**: withdrawals stopped on 7 Feb. On 10 Feb it blamed malleability, saying it had been "tricked into
  paying twice". It closed at the end of February with about 850,000 BTC missing. **Decker and Wattenhofer (ETH Zürich,
  arXiv:1403.6676)** watched for a year and found that at most about **386 BTC** could have been taken that way.
- **SegWit**, activated at **block 481,824 on 2017-08-24**, moves signatures into a separate *witness*. Example
  payment: 223 bytes = 113 + 2 + 108 witness.
- **Weight and virtual bytes**: a SegWit payment of about the same raw size (223 vs 225) takes up **63 %** of the room.
- **Fee rate and mempool**: what you pay is **size × the fee rate at that moment**, not a share of the
  amount. So a 30-input payment costs more than a 1-input one regardless of value.
