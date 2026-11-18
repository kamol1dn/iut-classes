# Week 9: Ethereum: Gas, Wei, Fees (slides)

**Blockchain · Week 9 · 25 pages · Dr. Jalolliddin Yusupov · dated 11/8/2026 · online, asynchronous**
Source: [week09 - Ethereum - Gas, Wei, Fees (slides).pdf](../slides/week09%20-%20Ethereum%20-%20Gas,%20Wei,%20Fees%20(slides).pdf) *(4.3 MB)*

The deck's title page reads **"Ethereum, Part 2"**; [Term Project I](../../homework/term-project-1/README.md) calls it
**Lecture 10** (gas). Built from the rendered pages, since the text layer holds only the titles. Every number below was
re-computed. Notes marked *(my note)* are my own explanations and are not on the slides. **Weekly quizzes need a calculator**,
and the **CALCULATE** boxes (pp. 15, 21, 22) are the likely quiz material. Term Project I's Part B (B.2–B.4) is built
on pp. 8, 14–17, 20 and 24. It comes between the [Ethereum Introduction](week09%20-%20Ethereum%20Introduction%20(slides).md)
and the [Remix demo](week09%20-%20Demo%20-%20Remix%20(slides).md).

## The object of the lecture: your own transaction page

**Homework 2, Task 1** told you: *"Ignore every other field on that page; we have not learned them yet."* By 7 Nov,
**41 of you** had sent your 0.001 ETH to the course address. That Etherscan page is Ethereum, and the lecture reads every
line of it. You knew 5 lines (status, block, from, to, value). By p. 24 every ❓ becomes ✅ except **Input Data** and **Logs**,
which belong to "the machine" (the next lectures).

A real student's page (Sepolia block **12,067,762**, 5 Nov 2026, address left out here):

| Row | Value | Explained on |
|---|---|---|
| Status · Block · From · To · Value | Success · 12,067,762 · (the student) · `0x02B7…8772` (the course address) · 0.001 ETH | known |
| Transaction Fee | 0.000031500000399 ETH | p. 15 |
| Gas Price | 1.500000019 Gwei | pp. 14, 20 |
| Gas Limit & Usage by Txn | 31,500 \| 21,000 (66.67 %) | p. 16 |
| Gas Fees | Base 19 wei · Max 1.500000026 · Priority 1.5 Gwei | p. 20 |
| Burnt & Txn Savings | Burnt 399,000 wei · Savings 147,000 wei | p. 20 |
| Other Attributes | Txn Type 2 · **Nonce 0** · Position 0 | p. 8 |
| Input Data · Logs | `0x` · 1 | not yet |

| Part | Question | Answer |
|---|---|---|
| The account (pp. 3–11) | What does Ethereum keep instead of Bitcoin's unspent outputs? | A **book of balances**: one 120-byte line per account, locked by one **state root**. A **nonce** counts each account's transactions |
| Gas (pp. 12–18) | Why did one student's second payment cost 9.7× the first? | Fees are **gas used × gas price**. Paying a **brand-new address** on Sepolia costs 204,600 gas instead of 21,000 |
| The price (pp. 19–23) | Who sets the gas price? | Since Aug 2021, **EIP-1559**: the network sets a **base fee** (burnt) from the traffic; you add a **tip** for the validator |

## Part 1: the account (pp. 3–11)

**State:** the full list of accounts and what each one holds, right now. Every node keeps a copy, and every block changes a few lines of it.

| Bitcoin: notes in your pocket | Ethereum: one line in a book |
|---|---|
| unspent outputs of 0.50, 0.30 and 0.02 BTC (illustrative). No balance is written anywhere; your wallet adds them up (0.82 BTC). To pay, you spend whole notes and get change (Lecture 6) | the student 0.05 → **0.0489685 ETH**, the course address 5.30675 → **5.30775 ETH**. A payment doesn't move notes: one line goes down, one goes up, and the fee is paid |

*"Bitcoin asks: which notes are unspent? Ethereum asks: what is written on your line?"* This one design choice explains the nonce and the price of a new account.

**Why a book?** (p. 4). A payment happens once; a **program** has to live somewhere: the same address, the same money, the
same data, call after call. If a program kept its money in one 40-coin note, two customers spending it at once would clash:
one fails and must start again, and every sale needs a brand-new note. On a line, 40 → 41 → 42: A pays, then B pays, both
succeed. **Notes keep one advantage:** payments that spend different notes can't clash, so a node can check them at the
same moment; in a book the order matters, so transactions run one after another. *"Notes suit payments. A book suits programs."*

**Account (Ethereum)** (p. 5): one line of the state, an address with four things under it.

| Field | Size | Meaning | A real student's account |
|---|---|---|---|
| address key | 32 bytes | who this line belongs to | (left out) |
| **nonce** | 8 bytes | transactions sent so far | 2 |
| **balance** | 16 bytes | the ETH it holds | 0.04666 ETH |
| **code hash** | 32 bytes | hash of its program; empty = Keccak-256 of nothing | `c5d24601…85a470` |
| **storage root** | 32 bytes | hash of its saved data; empty = the root of an empty tree | `56e81f17…63b421` |

**32 + 8 + 16 + 32 + 32 = 120 bytes for one account**, and every node keeps them. Even "nothing" has a hash (Lecture 4).

**State root and trie** (p. 6). The **state root** is one hash that stands for the whole state; change one balance and it
changes. Every block carries it in its header. A **trie** is a Merkle tree (Lecture 4) you can search like the tabs of a
phone book: the hash of your address gives 64 hex digits, and each digit picks the next tab. The lecture walked from block
**12,082,126**'s state root (`0xa85fbe…98ac`) down **8 pages** (six of 532 bytes, one of 308, a final one of 112: **3,612
bytes**, every hash matched) to the course address's line: nonce 0, balance 5.376 ETH. *"One hash locks the whole book,
and a few pages can prove any line of it."*

**Two kinds of account** (p. 7):

| | EOA (externally owned account) | Contract account |
|---|---|---|
| Controlled by | a private key: whoever holds it signs, and the account acts. Your MetaMask Accounts 1 and 2 are EOAs | its **code**; no private key exists |
| Starts a transaction? | yes | never: it runs only when a transaction calls it |
| Example | a student's account: nonce 2, 0.04666 ETH, 0 bytes of code | the deposit contract `0x0000…05Fa`: nonce 1 (a contract starts at 1, then adds the contracts it creates), **93,096,702 ETH**, 6,358 bytes of code |

**Whitepaper vs mainnet:** the 2013 whitepaper had two kinds, no mixing. **Since May 2025** an EOA may also point at code
(**EIP-7702**): the Sepolia example `0xAc68…4D00` holds 23 bytes, `0xef0100` plus an address. No student address does this.
Smart accounts are a later lecture. *"One kind of account signs. The other kind runs code."*

### New word: nonce, the Ethereum one (p. 8) — Term Project I A.5 (c)

**Nonce (of an account):** a counter of how many transactions this account has sent. Your first transaction carries
**nonce 0**, your second nonce 1. It may not skip: nonce 5 waits until nonce 4 is in a block. *Same word, different job:*
in Lecture 7 the nonce was the number a miner keeps changing in a block header. Both are numbers used once; don't mix them up.

- One student: nonce 0 in block 12,067,762 (06:41 UTC), nonce 1 in block 12,067,772 (06:43 UTC), **counter now 2**.
- A thief copies your signed payment (nonce 0) and sends it again. The signature is still valid, but it's **rejected**:
  the book says this account is past nonce 0.
- **Why Bitcoin has no such counter:** a spent output is gone (Lecture 6), so a copy finds nothing to spend. A balance is
  not gone after a payment, so a copy could spend it again unless the book counts.
- **Two locks, two jobs:** the **chain ID** stops a copy on *another* chain (Lecture 8); the **nonce** stops a copy on the *same* chain.

*"Bitcoin: a spent output is gone. Ethereum: a used nonce is gone."*

**A stuck transaction** (p. 9): fee too low? You can't take it back: it sits in the mempool of many nodes you don't control.
The way out is the nonce: sign a **new transaction with the same nonce and a higher fee**; only one of the two can ever
enter a block. Wallets call this **Speed Up**, or **Cancel** when the new one sends 0 ETH to yourself. Example: nonce 7 in a
block, nonce 8 waiting (fee too low), 9 and 10 stuck behind it → new nonce 8 goes first, the old one is dropped, 9 and 10
go through. *"A nonce is a queue: one stuck transaction holds back every later one."*

**Inside a transaction: where is "From"?** (p. 10). **Transaction hash** = Keccak-256 of its signed bytes, Ethereum's
transaction ID (Bitcoin, Lecture 6, used SHA-256 twice). This one is 119 bytes; hashing them gave the same hash as the page.
The signed bytes hold: **chain ID 11,155,111** (Sepolia), **nonce 0**, **to** `0x02B7…8772`, **value** 0.001 ETH, **data** empty
(no program called), **3 fee numbers**, and the **signature**. **"From" isn't in the bytes you signed.** Nobody writes it,
because nobody has to: signature + signed bytes → recover the public key → Keccak-256, keep the last 20 bytes → From ✓.
*"Your signature is your 'From'. Change one byte and a different address comes out."*

**The life of your transaction** (p. 11), seven steps: **sign** (your wallet, your private key) → **wait** (in the mempool,
Lecture 6) → **pay** (a price is set for the work) → **run** (every node runs it and gets one result) → **write** (somebody
writes the block) → **vote** (others check and vote) → **final** (past undoing, Lecture 8). About **12 s** to be in a block,
about **15 min** to be final. The first two you knew; the rest are the next lectures.

## Part 2: gas (pp. 12–18)

**The puzzle** (p. 12): the same student, two minutes apart:

| | Sent | Fee |
|---|---|---|
| Payment 1, to the course address, 06:41 UTC | 0.001 ETH | **0.0000315 ETH** |
| Payment 2, to a brand-new Account 2, 06:43 UTC | 0.002 ETH | **0.0003069 ETH** |

**9.7 times the fee for 2 times the money.** It isn't the amount (the fee isn't a percentage) and it isn't the traffic
(the two are 10 blocks apart). Every first payment to a brand-new address checked so far shows the same jump, **43 times out of 43**.

**Why a meter?** (p. 13). Every node must run every program, so one endless loop would freeze all of them, for free, for
ever. And **you cannot check first**: a Turing-complete machine can loop forever, and Turing proved in 1936 that no program
can always predict that. **Bitcoin's answer: no loops** (Lecture 6: Script always ends; safe and small). **Ethereum's answer:
a meter**, like a taxi: don't guess the trip, count every step as it happens and charge the passenger. The money runs out: the program stops.

### New words: gas, wei and gwei (p. 14)

| Word | Meaning |
|---|---|
| **Gas** | Measures **work**. Every step a transaction asks the network to do costs some gas. **A plain transfer is 21,000 gas.** You pay **gas used × gas price** |
| **Wei** | The smallest piece of ETH (as the satoshi is for Bitcoin) |
| **Gwei** | One billion wei. Gas prices are quoted in gwei |

**1 ETH = 1,000,000,000 gwei = 1,000,000,000,000,000,000 wei** (10⁹ and 10¹⁸).

| | | | |
|---|---|---|---|
| A car | litres used | × price per litre | = what you pay |
| Bitcoin (Lecture 6) | size in vB | × sat per vB | = transaction fee |
| Ethereum | **21,000 gas** | × **1.5 gwei per gas** | = **31,500 gwei** |

*"Bitcoin charges for space. Ethereum charges for work."*

### CALCULATE: the two fees (p. 15) — Term Project I B.3

**fee = gas used × gas price**, done by hand in wei; then **wei → ETH: move the point 18 places to the left**.

| | Payment 1, to the course address | Payment 2, to a brand-new address |
|---|---|---|
| Gas used | 21,000 | **204,600** |
| Gas price | 1,500,000,019 wei | 1,500,000,020 wei |
| Fee | **31,500,000,399,000 wei** | **306,900,004,092,000 wei** |
| Fee in ETH | 0.000031500000399 | 0.000306900004092 |
| Balance check | 0.05 − 0.001 − 0.000031500000399 = **0.048968499999601** ✓ | 0.048968499999601 − 0.002 − 0.000306900004092 = **0.046661599995509** ✓ |

The whole class by 7 Nov *(my note: p. 2 says 41 of you had paid, and p. 15 counts 42 payments to the course address;
the slides don't explain the gap of one)*: to the course address **42 of 42** at 21,000 gas; to a brand-new address **43 of 43** at 204,600;
to another address that already existed, **3** at 21,000. *"The price barely moved. The gas went from 21,000 to 204,600. The puzzle is about gas."*

### Gas limit (p. 16) — Term Project I B.2

**Gas limit:** the most gas you allow a transaction to use. Your wallet proposes it and you sign it. **Unused gas isn't
charged.** If the work needs more than the limit, the transaction stops, **fails, and the gas is still paid**. *A fuel tank:*
Payment 1 had a tank of 31,500 and the trip used 21,000, so you paid for 21,000 (the page's "66.67 %").

**War story: 9 Oct 2026, the day the course address was born.** 10:46 UTC: a faucet sends 0.15425 ETH with a limit of
30,000; it uses 30,000 of 30,000: **out of gas**, nothing arrived, **0.00006 ETH fee still paid**. 10:48 UTC: a faucet sends
0.05 ETH, uses **204,600 of a 630,000 limit**: success, the account was created. Every later payment to the same address:
21,000. *"Out of gas: the work was done, so the fee is paid, and nothing moves."*

### Why 204,600? A new line in the book (p. 17) — Term Project I B.4

Payment 2's extra work was **storage, forever**: Account 2 had no line in the state, so every node had to add 120 bytes and keep them.

```
120 bytes × 1,530 gas per byte = 183,600 gas   (a new line in the book)
 21,000 + 183,600              = 204,600 gas ✓  (the transfer + the new line)
```

The course address already had a line, so paying it costs 21,000.

- **Whitepaper vs mainnet:** on **Sepolia since 6 Oct 2026**, a new account costs 204,600 gas (**EIP-8037**, part of the
  **Glamsterdam** upgrade). **Mainnet today: still 21,000** (checked: a plain transfer to a never-used address in block 26,350,296 used exactly 21,000).
  *"Your testnet is ahead of mainnet. You have already paid a price the real Ethereum has not charged yet."*
- **The news story:** the faucet's 30,000 limit always worked while a transfer cost 21,000. On 9 Oct, three days after the
  new rule, it ran out of gas. The Ethereum Foundation's list of old assumptions (6 Nov) includes "A fixed gas amount is enough for the job".
- **War story, Homework 2 Task 1.4:** the homework said not to send to your broken address. **4 of you did.** Nobody holds
  those keys, yet the network made 4 new lines at 204,600 gas each, and those coins are stuck for good.

### Block gas limit (p. 18)

**Block gas limit:** the most gas all the transactions in one block may use together. **Today 60,000,000**, so one block
fits at most **2,857** plain transfers (60,000,000 ÷ 21,000). Validators set it, **by small steps**: each block may move the
limit by less than 1/1024 (on 7 Nov 2026 the biggest step in 100 blocks was 58,592; 60,000,000 ÷ 1,024 = 58,594). One
exception: **London, 2021**, doubled it at once (≈ 15 M → 30 M), and the target stayed near 15 million. The chart's
steps: 14.8 M → **30 M** (2021) → 36 M → 45 M (2025) → **60 M**. *"More gas means more room, and heavier work for every node. That is the argument of every year."*

## Part 3: who sets the price? (pp. 19–23)

**Before August 2021: an auction** (p. 19), the same answer as Bitcoin (Lecture 6): you name a price and block writers take
the highest bids. **Why it hurt:** nobody knows the right price; bid low and you wait, bid high and you pay for nothing.

| Block | What a plain transfer paid, gwei per gas |
|---|---|
| **12,964,999**, the last auction | lowest 27.0 · middle 31.0 · highest 58.2: the same 21,000 gas of work cost some people twice as much as others |
| 26,361,381, today, a quiet day | from 0.04 to 2.74, nearly all of it a voluntary extra |

Since August 2021 the network itself names the price of entry, so a wallet no longer has to guess. *"An auction makes everyone guess, and it charges them for guessing wrong."*

### New words: base fee, tip and burnt (p. 20) — Term Project I B.2, B.3

| Word | Meaning |
|---|---|
| **Base fee** | The lowest gas price a block accepts. **The network sets it, not you.** It is **burnt**: destroyed, so it's on nobody's line any more |
| **Tip** (priority fee) | What you add on top of the base fee, per gas. It goes to the **validator** who puts your transaction in a block |
| **Max fee** | The ceiling your wallet signed, per gas |
| **Txn savings** | (max fee − the price actually charged) × gas used: it stays with you |

**gas price = base fee + tip.** A real mainnet transfer (block 26,350,266), gas price 1,608,496,482 wei × 21,000 gas:

```
base fee  608,496,482 wei × 21,000 = 12,778,426,122,000 wei   burnt: gone for everyone
tip     1,000,000,000 wei × 21,000 = 21,000,000,000,000 wei   paid to the validator
```

The whole block 26,350,266: 168 transactions, **burnt 0.00759 ETH, tips 0.00679 ETH**.

**A student's page on Sepolia:** base fee **19 wei** (yes, 19 wei: a testnet is empty), tip 1.5 gwei, so almost the whole fee
was tip. The wallet's max fee was 1,500,000,026 wei per gas; the network charged 1,500,000,019; **the gap × 21,000 gas =
147,000 wei** stays with you: that's "Txn Savings".

*(my note, the four formulas Term Project I B.3 asks for, checked on that page:
gas price = 19 + 1,500,000,000 = **1,500,000,019 wei** ·
fee = 21,000 × 1,500,000,019 = **31,500,000,399,000 wei = 0.000031500000399 ETH** ·
burnt = base × gas used = 19 × 21,000 = **399,000 wei** ·
savings = (1,500,000,026 − 1,500,000,019) × 21,000 = 7 × 21,000 = **147,000 wei** ✓.)*

*"Bitcoin pays the whole fee to the miner. Ethereum burns the base fee and pays only the tip."*

### CALCULATE: EIP-1559, the next base fee (p. 21)

**EIP-1559**, the fee rule since August 2021: each block aims to use **half of its gas limit**, the **target**. A block above
target pushes the next base fee up; below target pushes it down; **never by more than one eighth**.

**next = base ± base × |used − target| ÷ target ÷ 8**

```
block 26,350,266: base 608,496,482 wei, used 12,473,253, target 30,000,000
used < target, so down:  608,496,482 − 608,496,482 × 17,526,747 ÷ 30,000,000 ÷ 8
next = 564,059,133 wei ✓ (as on the chain)
```

The chart (blocks …260 to …272) shows the same thing in million wei: 40.3 M used → 585 rises to 610; 24.7 M → 610 falls to
597; 12.5 M → 608 falls to 564. *"Nobody sets this price. Every block sets it from the block before."*

### A storm: one night, one sale (p. 22)

**War story, 1 May 2022:** a company sold **55,000 plots of digital land** at one fixed price, all at 01:00 UTC. The price
couldn't rise, so buyers bid with gas instead. Reports put the night's gas bill at about **$160–180 million**; failed buyers
paid too, until the seller refunded them. The base fee went from **97 gwei** (00:40 UTC) to a peak of **8,629 gwei** in block **14,688,911**.

**CALCULATE:** a full block adds one eighth; **six in a row: 1.125⁶ ≈ 2**, so the price can **double in 72 seconds** (6 × 12 s).
33 nearly full blocks came in a row before the peak. *"The base fee cannot stop a storm. It makes everyone in the storm pay more, block by block."*

### Is ETH shrinking or growing? (p. 23)

Burning destroys ETH; validators receive new ETH. Bitcoin has a fixed timetable (Lecture 7); Ethereum has no fixed limit
(Lecture 9), so the answer changes with traffic. **Issuance:** new ETH created for validators as pay. It follows a rule,
not a timetable: more stake means more ETH in total, and less for each validator.

| One day of ETH (7 Nov 2026) | |
|---|---|
| New ETH, the most the rule allows | **3,032 ETH** |
| Burnt ETH, measured over 7,200 blocks | **34 ETH** |

Stake 44,320,876 ETH; rule: **64 ÷ √(stake in gwei) per ETH, each 6.4 minutes** (one epoch).

*(my note, CALCULATE: stake in gwei = 4.432 × 10¹⁶, √ = 2.105 × 10⁸, so 64 ÷ 2.105 × 10⁸ = 3.04 × 10⁻⁷ ETH per staked ETH
per epoch × 44,320,876 ETH = 13.47 ETH per epoch × 225 epochs a day (24 h ÷ 6.4 min) = **3,032 ETH** ✓. 7,200 blocks = one
day of 12-second slots.)*

**Whitepaper vs mainnet:** the popular slogan says burning makes ETH "ultrasound money", always shrinking. On 7 Nov 2026
mainnet burnt 34 ETH a day against up to 3,032 new. Busy days burn more; **a quiet network grows**. Why so little burnt? The
mean base fee that day was **0.157 gwei** (the May 2022 storm peaked at 8,629). Burn follows the base fee. *"Bitcoin's supply is a timetable. Ethereum's supply is a result."*

## Half time: what we can read now (p. 24) — Term Project I B.2

| Row on your page | It means |
|---|---|
| **Nonce** | your counter (p. 8) |
| **Transaction hash** | Keccak-256 of the signed bytes (p. 10) |
| **Gas limit and usage** | the tank and the trip (p. 16) |
| **Gas price** | base fee + tip (p. 20) |
| **Burnt** | the base-fee part (p. 20) |
| **Savings** | your ceiling minus the price (p. 20) |
| Input Data · Logs | still ❓: they belong to the machine behind the page (next lectures) |

*"Everything about money on your page is now ✅. Next: the machine."*

## Slide errors and loose claims

No errors: every fee, balance, base-fee, block-limit and issuance figure above re-computes exactly. Two things on p. 22 to
read carefully if a quiz asks:

1. **"33 nearly full blocks in a row before the peak"** can't start from the chart's 97 gwei label. At the maximum +12.5 % per
   block, 97 × 1.125³³ ≈ 4,700 gwei; going all the way from 97 to 8,629 needs at least 38 full blocks (1.125^38.1 ≈ 89).
   The 33-block run fits if it started near 8,629 ÷ 1.125³³ ≈ **177 gwei**, and the chart's line does sit above 97 just
   before the climb. *(my note)*
2. **"Double in 72 seconds"** uses today's 12-second slots. In May 2022 Ethereum was still mined, with blocks about 14.9 s
   apart on average (Validators deck p. 10), so six blocks then took about 90 s. For a quiz, use the slide's 1.125⁶ ≈ 2 and 72 s.

Video: the matching lecture is on eClass (one of the week-9 VODs 73240, 73265, 73303), not mirrored or transcribed yet.
