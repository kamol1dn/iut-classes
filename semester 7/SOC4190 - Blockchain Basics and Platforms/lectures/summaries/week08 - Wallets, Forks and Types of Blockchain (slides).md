# Week 8: Wallets, Forks and Types of Blockchain (slides)

**Blockchain · Week 8 · 28 pages · Dr. Jalolliddin Yusupov · dated 10/31/2026 · online, asynchronous**
Source: [week08 - Wallets, Forks and Types of Blockchain (slides).pdf](../slides/week08%20-%20Wallets,%20Forks%20and%20Types%20of%20Blockchain%20(slides).pdf) *(3.5 MB, "v2.0" on eClass)*

Built from the rendered pages. Every number below was re-computed. Notes marked *(my note)* are my own
explanations and are not on the slides. **Weekly quizzes need a calculator**, and the two **CALCULATE** boxes
(pp. 9, 17) are the likely quiz material. The deck calls itself **the last lecture of the Bitcoin half**: smart
contracts are weeks 9–11.

## The six questions the lecture answers

A blockchain has no boss, so who controls the key, the rules and the membership?

| Stop | Question | Answer |
|---|---|---|
| The place | Where should a key live? | Hot or cold; with you (non-custodial) or with a company (custodial). A hardware wallet signs inside itself |
| The keys | Can one key be too few? | **Multisig**: any m of n keys must sign |
| The rules | How do the rules of a blockchain change? | A **soft fork** makes them stricter and old nodes still follow. A **hard fork** loosens them and old nodes split off |
| The split | What happens to my coins when a chain splits? | They exist on both chains. A **chain ID** in every signature stops a payment being copied across |
| The members | Who may read, write and join? | **Public** (anyone), **private** (one owner), **permissioned** (a known group) |
| The agreement | Can a network agree without mining? | Yes: **proof of stake**, with validators and finality |

News opener (p. 2): the deck shows a Binance hack of an estimated **$6.3bn**, the largest on its chart, ahead of Bybit
$1.5bn, Poly Network $0.61bn, Ronin $0.54bn, Coincheck $0.53bn and Mt. Gox $0.5bn; $3.0bn frozen on-chain.

## Part 1: where your key lives (pp. 4–9)

The story: savings in your pocket, in a safe at home, or in a bank. Each place trades **convenience** against
**safety**, and the bank adds a third thing, **trust in someone else**.

| Word | Meaning |
|---|---|
| **Hot wallet** | The key sits on an internet-connected device (browser extension, phone app). Quick to use; open to anything that reaches the device. Your course wallet is one |
| **Cold wallet** | The key is where the internet can't reach it: on paper, or on a device that stays offline. Slow; safe from remote thieves |
| **Hardware wallet** | A small device that keeps the key and signs. The computer sends the payment, the device shows it on its own screen, you press its button, and only the **signature** goes back |
| **Custodial** | A company holds the key. You hold a login. If the company fails, your coins are only a promise in its books |
| **Non-custodial** | You hold the key and the 12 words. If you forget your password, restore from the words. If a company fails, nothing changes |
| **Multisig** | A lock that needs signatures from several keys, any m of n. Lecture 6's P2SH "any 2 of 3" is one |

- *Hot for spending, cold for saving.* Keep large savings cold and a small spending amount hot.
- A hardware wallet **protects the key, not your judgement**: it signs whatever you approve. Read the device's
  screen, not the laptop's.
- **"Not your keys, not your coins."** A custodian is an intermediary, the thing blockchains were built to remove.
- **FTX, November 2022:** reports that its money was mixed with a sister company's, a rush to withdraw, withdrawals
  stopped, bankruptcy. The founder got 25 years for fraud; about $10bn was taken. **The chain did not fail; the custodian did.**
- Lecture 6's real 2-of-3 address `3CTkLec3…NDfJLG` has been used in 4,134 transactions, most likely a company
  treasury or a service.

### CALCULATE: how many keys can you lose? (p. 9)

For an **m-of-n** lock: **keys you may lose = n − m**, and **keys a thief must steal = m**.

| Lock | May lose | Thief needs |
|---|---|---|
| 1 of 1 (a normal wallet) | 0 | 1 |
| 2 of 2 | 0 | 2 |
| **2 of 3** (the classic) | 1 | 2 |
| 3 of 5 | 2 | 3 |

**Your turn on the slide:** a family keeps savings in a 3-of-5 lock with three keys at home. The house burns down, can
they still spend? A burglar takes the three home keys, can they spend?
*(my note: the fire leaves 2 keys and 3 are needed, so **no**. The burglar holds exactly 3, so **yes**. Keeping m keys
in one place defeats the lock.)*

## Part 2: when the rules change (pp. 10–14)

**Fork:** a change of a blockchain's rules, which every node must choose to accept or not. Nobody can force a node to
update: the rules are whatever the nodes run. Volunteers usually write the changes as numbered proposals (BIP for
Bitcoin, EIP for Ethereum) and argue for them in public.

The football analogy: "no more than 5 substitutes" instead of 7 is still legal to an old referee; "goals from your own
half count double" isn't.

| | Soft fork | Hard fork |
|---|---|---|
| The change | Only makes the rules **stricter** | **Loosens** them or changes them outright |
| New blocks under the old rules | Still valid | **Invalid** |
| Nodes that didn't update | Stay on the same chain | Split off, unless everyone updates |
| Result | One chain | One upgrade if everyone follows; otherwise two chains with one shared past |
| Example | **SegWit**, block 481,824, 24 Aug 2017 | **Bitcoin Cash**, 1 Aug 2017; Ethereum's upgrades |

**Bitcoin Cash, 1 Aug 2017.** Both sides built on block **478,558** (13:16 UTC). Bitcoin Cash's block 478,559 was
**1,915,175 bytes**, illegal for Bitcoin's 1,000,000-byte limit, while Bitcoin's own was 272,502 bytes (13:23 UTC). The
first new-chain block came about **5 hours** after the last shared one (18:12 UTC), because few miners had followed and
blocks stayed as hard to make as before.

## Part 3: one chain becomes two (pp. 15–18)

At the split, every unspent output exists on **both** chains, and whoever held a key for 1 BTC now also held 1 BCH.

| Your coins were… | After the split |
|---|---|
| In a non-custodial wallet | You hold both: the same key opens the same outputs on each chain |
| At an exchange | You get the new coins only if the exchange decides to give them to you |

**The DAO, June 2016.** An investment fund that was a program on Ethereum. On 17 Jun an attacker used a bug to drain
about **3.6 million ETH**. The debate: "Fix the theft: the rules exist to serve people" against "Code is law: if the rules
can be changed after a loss, nothing is certain." On 20 Jul most of the community hard-forked at **block 1,920,000**,
moving the funds to a refund program. Both sides kept their chain: **Ethereum** and **Ethereum Classic**.

- Both blocks 1,920,000 build on the shared block 1,919,999. The forking miners wrote `dao-hard-fork` into the extra data:
  the hex starts `6461 6f2d`, ASCII for `dao-`.
- Today: Ethereum (chain ID 1) has a block every 12 s like a clock and difficulty **0**. Ethereum Classic (chain ID 61) has
  random gaps (16, 8, 5, 41, 6, 7 s) and is still mined, difficulty 2.2 × 10¹⁵.

**Replay attack:** copying a payment signed for one chain and sending it on the other, where the same signature is valid
too. People lost coins this way after the 2016 split. **The fix** (Nov 2016, Ethereum block 2,675,000): every signature now
includes the chain ID, so a payment signed for chain 1 is invalid on chain 61.

### CALCULATE: the chain ID in the signature (p. 17)

**v = 35 + 2 × chain ID + (0 or 1)**

| Chain | v | Working |
|---|---|---|
| Ethereum | 38 | 35 + 2 × 1 + 1 |
| Ethereum Classic | 157 | 35 + 2 × 61 + 0 |

*(my note: to go backwards, chain ID = (v − 35) ÷ 2, rounded down.)*

## Part 4: who may join, and how they agree (pp. 19–22)

| | Public | Private |
|---|---|---|
| Who may write | Anyone who follows the rules | Only computers the owner approves |
| Who may read | Everyone, on any explorer | Whoever the owner allows |
| Who can change the rules | Whoever the nodes follow (forks) | The owner |
| Trust | In the rules and the work | In the owner: an intermediary again |

**Permissioned** sits between them: a known group of organisations (several banks, shipping firms), admitted by name, each
running nodes, none in charge. They know each other, so they need a way to vote rather than mining. It makes sense when
organisations that don't fully trust each other must keep one shared record the public mustn't see. *Brochure vs reality:*
many such projects were announced and fewer survived; when a simple shared database would do, it usually wins.

| | Proof of work (Lecture 7) | Proof of stake |
|---|---|---|
| The cost of writing | Electricity, spent guessing hashes | Coins locked as a deposit (the **stake**) |
| Who writes next | Whoever guesses first | A **validator** picked at random, weighted by stake |
| Punishment for cheating | Wasted electricity | Part of the deposit is destroyed |

**The day Ethereum stopped mining, 15 Sep 2022.** Blocks 15,537,393 (06:42:42 UTC, difficulty 11,055,787,484,078,698, the
last miner) and 15,537,394 (06:42:59, difficulty **0**, nonce all zeros, the first validator) are **17 seconds** apart. A hard
fork that everyone followed, so no split.

**Finality:** the point after which a block can no longer be undone under the rules. Blockchains are *tamper-resistant*, not
"immutable".

| | Bitcoin (PoW) | Ethereum (PoS) |
|---|---|---|
| When is a block final? | Never completely: every block on top makes undoing harder | After a two-thirds vote of validators on a checkpoint, about **14 minutes** behind the newest block when measured |
| Undoing it would need | More work than the rest of the world, block after block | Breaking a two-thirds vote, which destroys the voters' deposits |

## Wallet solutions and demo (pp. 23–27)

The deck lists ZenGo (software, free, "#1 best overall"), Crypto.com (hot, free), Binance (hot, free, 1000+ coins), Ledger
Nano X (cold, $149), Trezor (cold, $79, open source) and Pionex (listed as cold, free). The Ledger setup is a PIN, then a
**24-word** seed phrase. Local example: **Asterium**, shown as Uzbekistan's largest crypto exchange, with Visa and HUMO
crypto cards (a gazeta.uz story).

*(my note: p. 23 lists Pionex as a cold wallet, but it's an exchange, so treat that entry with care. Part of p. 25's Trezor text
is hidden behind a photo.)*

**Demo:** [sandbox.eth.build](https://sandbox.eth.build), drag-and-drop blocks that generate a key pair, sign "Salom
hammaga" and recover the same address from the signature.

Video: the matching two-part lecture on eClass, VODs 72985 and 72990.
