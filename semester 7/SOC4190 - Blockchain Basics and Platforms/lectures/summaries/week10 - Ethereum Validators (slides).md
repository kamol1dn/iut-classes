# Week 10: Ethereum Validators (slides)

**Blockchain · Week 10 · 28 pages · Dr. Jalolliddin Yusupov · dated 11/14/2026 · online, asynchronous**
Source: [week10 - Ethereum Validators (slides).pdf](../slides/week10%20-%20Ethereum%20Validators%20(slides).pdf) *(4.5 MB, eClass slide 73658)*

The deck's own title is **"Ethereum: One Transaction, Three Questions"**; eClass lists it as *Ethereum Validators*. Built
from the rendered pages, since the text layer holds little more than the titles. Every number below was re-computed.
Notes marked *(my note)* are my own explanations and are not on the slides. It picks up from the
[Remix demo](week09%20-%20Demo%20-%20Remix%20(slides).md) and is followed by [Tokens](week10%20-%20Tokens%20-%20Money%20Made%20of%20Code%20(slides).md).

## The three questions the lecture answers

The opener (p. 2): in the Remix demo we pressed **Transact** and 42 was stored at once. Our own browser ran the code and
wrote the block, and nobody else was asked. On the real Ethereum your transaction goes to thousands of computers owned by
strangers. Somebody must run your code, somebody must write it into a block, and somebody, long ago, wrote the rules they
all follow. The deck follows one transaction, `store(42)`, through all three.

| # | Question | Answer (p. 27) |
|---|---|---|
| 1 | Who runs my code? | **Every node**, in the **EVM**; gas stops every program |
| 2 | Who writes the block? | A **validator** with 32 ETH, one per **12-second slot**; the others vote; **final ≈ 15 min** |
| 3 | Who changes the rules? | **EIPs**, bundled into **upgrades**, tested, then run by everyone |

*"And when it is final, not even the validators can take your 42 back."*

**Four words you've met, explained today** (p. 3):

| Word | Where you met it | Short meaning | Full story |
|---|---|---|---|
| validator | the tip goes to the validator (gas lecture: base fee, tip, burnt) | the one who writes a block | Question 2 |
| stake | new ETH is paid on the stake ("Is ETH shrinking or growing?") | money locked as a deposit | Question 2 |
| EIP | EIP-1559, the fee rule since August 2021 | a numbered proposal to change the rules | Question 3 |
| upgrade | 204,600 gas for a new account, on Sepolia only | a set of rule changes switched on together | Question 3 |

## Question 1: who runs my code? (pp. 4–8)

**Everybody.** Every full **node** receives your transaction and runs it itself; nobody trusts anybody else's answer.
The diagram sends `store(42)` to nodes in Tashkent, Berlin, São Paulo, Seoul and Toronto; each computes `number = 42`, and they all agree on the same new state.

| Word | Meaning |
|---|---|
| **EVM** (Ethereum Virtual Machine) | An imaginary computer described exactly on paper. Every node builds the same one in software. A **virtual** machine is a computer made of software that runs inside a real one. *Like the rules of chess: different boards in Tashkent and Seoul, same position + same move = same new position.* A laptop on Windows, a Linux server, a rented cloud machine, a small box at home: the hardware differs, the EVM inside is identical byte for byte |
| **Opcode** | One tiny instruction of the EVM, written as one byte: ADD, MUL, STOP… There are more than a hundred. A contract's **bytecode** is just a long list of opcodes |
| **Revert** | The EVM undoes every change the transaction made, as if it never ran. **Only the fee stays paid**: the nodes did the work |
| **Storage** | The contract's own data, kept in the state by every node, forever. In the demo, `number = 42` lives here |

**A real 7-byte program: add 2 and 3** (p. 6, CALCULATE):

| Bytes | Opcode | Does | Gas |
|---|---|---|---|
| `60 02` | PUSH 2 | put 2 on the pile | 3 |
| `60 03` | PUSH 3 | put 3 on the pile | 3 |
| `01` | ADD | take two numbers, put back their sum: 5 | 3 |
| `50` | POP | throw the top number away | 2 |
| `00` | STOP | the end | 0 |
| | | **total** | **11 gas** |

*"A contract is a list of tiny steps, and every step has a price in gas."*

**What if a program never stops?** (p. 7). Without a meter, a program loops forever, every node runs it forever, and the
whole network freezes. With gas, each step spends gas, the gas limit runs out, and the EVM stops and undoes everything.
**Gas has a second job: it's the alarm clock.** A real failed call, block **26,361,276**: it used **49,570 gas**, was undone,
and still paid **0.0000624 ETH**. *(my note: fee = gas used × gas price, so that price was 0.0000624 ETH ÷ 49,570 ≈ 1.26 gwei.)*

**Where does the 42 live? Two places** (p. 8):

| | Memory: scrap paper | Storage: the book |
|---|---|---|
| Lifetime | used while the code runs, wiped when the transaction ends | the contract's own page in the state, kept forever by every node |
| Price | **1 KB costs about 107 gas** | **one new number costs 22,106 gas** |

Storing one number costs about **2,000 times** more than adding two numbers *(my note: 22,106 ÷ 11 ≈ 2,010, the 11-gas
program above)*. *"Thinking is cheap; remembering forever is expensive, because every node must remember."*

## Question 2: who writes the block? (pp. 9–20)

Thousands of nodes hold the same result, but a block needs **one author** to choose which waiting transactions go in and in
what order. If everybody wrote their own block there would be thousands of chains.

**The first answer, 2015–2022: a race, like Bitcoin** (p. 10). Ethereum began with **proof of work** (Lecture 7): miners
raced to find a lucky hash, and the winner wrote the block. The last 2,000 mined blocks: average **14.86 s**, shortest
**1 s**, longest **175 s**; nobody knew who was next. *"Mining worked, but the clock was a lottery."*

**Why stop racing?** (p. 11). In proof of work cheating is expensive because writing is expensive, and the cost is paid every
day by honest miners too: **electricity** (all but one guess is wasted), **an arms race** (faster machines win, so mining
gathers in big farms), **a lottery clock** (a block after 1 second or after 3 minutes). After Ethereum stopped mining its
electricity use fell by **more than 99.9 %**.

| Word | Meaning |
|---|---|
| **Stake** | ETH you lock as a deposit to earn the right to write and check blocks. Rules followed: you're paid. Rules broken: part of the deposit is destroyed. Writing by stake is **proof of stake** (Lecture 8). *Like renting a flat: deposit first, back if you leave it clean, lost if you break the furniture.* For Ethereum blocks: **32 ETH** |
| **Validator** | A participant who has locked at least 32 ETH and runs software with its own key that does two jobs: **propose** a block when chosen, and **vote** on blocks written by others, all the time. The tip from your fee is the proposer's reward for including it |
| **Slot** | A **12-second** turn. In each slot one validator is picked to propose a block |
| **Epoch** | **32 slots** in a row, **6.4 minutes** |
| **Vote (attestation)** | A signed message from a validator: "I checked this block; it follows the rules." Every validator sends one vote in each epoch. Votes are what make a block trusted |
| **Slashing** | The punishment for signing two different things for the same moment. Part of the stake is destroyed and the validator is removed; whoever reports it is rewarded |
| **Finality** | The moment after which a block can't be undone without destroying a huge amount of stake. On Ethereum it comes after two epochs of votes: **about 15 minutes** |
| **The Merge** | The hard fork of **15 September 2022** that joined the mined chain and the staking chain. From that block on, validators write Ethereum's blocks; balances and contracts stayed exactly the same |

*"Honest work costs almost nothing. Only cheating is expensive."*

**Ethereum on 7 Nov 2026** (p. 13): **813,444** active validators, **44.3 million ETH** locked as stake, shown as
**78.359.000.000 $** (that is $78.359 billion, written with dots).

**A lottery with a timetable** (p. 14): mining was a race and nobody knew who would win. Now everybody knows the schedule a
few minutes ahead: the pick is random, but the clock is fixed. Picked fairly: **more stake, more chances**. **With 32 ETH,
your turn comes about once every 192 days.**

*(my note, CALCULATE: chance per slot = your stake ÷ all stake = 32 ÷ 44,300,000. Expected wait = 44,300,000 ÷ 32 =
1,384,375 slots × 12 s ≈ 16.6 million s ≈ **192 days** ✓. Dividing by the number of validators instead (813,444 × 12 s)
gives about 113 days. The two differ because the average validator now holds about 54 ETH, not 32, so the slide's
stake-based figure is the right one.)*

**Every validator votes** (p. 15): one block by one proposer; the others check it and sign. In epoch **487,523**,
**811,029 of 813,444** validators voted: **99.7 %** turnout ✓. *"One writes, almost everyone checks."*

**Slashing war story** (p. 16): on **4 Feb 2021**, **75 validators** run by the company **Staked** were slashed. After a
restart their software signed a second vote that clashed with the first. Lesson: **a validator key must never run in two
places.** The cheat is "vote A, slot 100" and "vote B, slot 100": same key, same moment, two answers, and anyone can show both signatures.

**Finality** (p. 17): epochs 1–3 final, 4–6 still voting, your block final after **about 15 min**. Two-thirds of all stake
has voted for it, twice. To undo it attackers would lose at least one third of all stake: **about 14.8 million ETH**,
destroyed by the rules themselves *(my note: 44.3 M ÷ 3 = 14.77 M ✓)*. Bitcoin has no such moment: each new block only makes undoing harder (Lecture 8).

**The Merge** (pp. 18–19). *Like a plane changing engines in flight*: the new engine ran beside the plane for almost two
years, tested but not connected, then the old one was switched off and passengers kept their seats.

| | Block | Time (15 Sep 2022) |
|---|---|---|
| Last mined block | **15,537,393** | 06:42:42 UTC |
| First staked block | **15,537,394** | 06:42:59 UTC |

The staking chain had run beside it for **653 days**, with no transactions, only validators voting. Then, **17 seconds** apart,
the writer of Ethereum changed. *(my note: the staking chain started on 1 Dec 2020; to 15 Sep 2022 is 653 days ✓.)*

**The Merge, seen in the clock** (p. 19): subtract each block's timestamp from the next, 2,000 times on each side.

| Mined: a lottery | Staked: a timetable |
|---|---|
| **14.86 s** on average, anything from 1 s to 175 s; 459 of 2,000 gaps under 5 s | **1,971 of 2,000** gaps exactly 12 s; the rest 24 s: a slot with no block (the proposer missed its turn) |

**The two answers Ethereum has given** (p. 20): both make cheating expensive; they differ in **who pays**. In mining every
honest miner pays every day; in staking mainly the cheater pays.

| | Mining (2015–2022) | Staking (since 15 Sep 2022) |
|---|---|---|
| Who writes the block | the miner who finds a lucky hash first | a validator picked at random, by stake |
| What it costs to take part | machines and electricity | 32 ETH locked as a deposit |
| What stops a cheater | the electricity he wasted | slashing: part of his deposit is destroyed |
| The clock | a lottery: 14.86 s on average | a timetable: one slot every 12 s |
| When is a block final | never completely | after about 15 minutes |
| Electricity | very high | more than 99.9 % less |

## Question 3: who changes the rules? (pp. 21–26)

Ethereum has no company, no CEO and no vote of ETH holders, yet the fee rule changed in 2021 and the block writers changed in
2022, with every node switching at the same block. Somebody wrote the change down, and everybody agreed to run it.

| Word | Meaning |
|---|---|
| **EIP** (Ethereum Improvement Proposal) | A public document that describes one change to Ethereum, exactly enough to program it. Each gets a number. Anyone may write one |
| **Client** | A program that runs an Ethereum node, such as **Geth** or **Nethermind**. Several teams write different clients for the same rules; if one has a bug, the others keep going |
| **Upgrade** | A bundle of EIPs that every node switches on at the same block: a hard fork that everyone follows. Each gets a name |

**Three EIPs we've already met** (p. 22):

| EIP | What | Live |
|---|---|---|
| **EIP-1559** | the base fee, burnt | mainnet, since 5 Aug 2021 (gas lecture) |
| **EIP-3675** | proof of stake replaces mining | mainnet, since 15 Sep 2022 (Question 2) |
| **EIP-8037** | a new account costs 204,600 gas | **Sepolia only**, since 6 Oct 2026 (gas lecture) |

**The road of an EIP** (p. 23): **written** (drafted in public) → **discussed** (weekly public calls of client developers) →
**packed** (chosen EIPs bundled together) → **testnets** (Sepolia, Hoodi: practice first) → **mainnet** (every node updates
for one moment). **Nobody can force an update**: every node operator decides to install the new client; if almost all do,
the change becomes the rule, a hard fork that everyone follows (Lecture 8). **Glamsterdam today:** on Sepolia since
**6 Oct 2026** (block **11,856,337**); the Hoodi rehearsal was postponed on 22 Oct. Mainnet comes only after every testnet has run it cleanly.

**Why the strange names?** (p. 24): the EVM side is named after cities of Ethereum conferences: Berlin, London, Shanghai,
Cancun, Prague, Osaka, next Amsterdam. The validators' side uses star names. The two are glued together: **Fulu + Osaka =
Fusaka**, switched on at block **23,935,694** on **3 Dec 2025** (it bundled EIP-7594, EIP-7825 and more). Osaka was the rule set of our Remix demo.

**Eleven years, seven upgrades that matter to us** (p. 25). Mainnet has had **17 upgrades** since the first day; most fixed small things. These seven changed the fee you pay, who writes the block, and what a new account costs:

| Year | Upgrade | What changed | Block |
|---|---|---|---|
| 2015 | Frontier | Ethereum starts | 1 |
| 2016 | DAO fork | the hacked money moved to a refund program (Lecture 8) | 1,920,000 |
| 2021 | London | EIP-1559: the base fee is burnt | 12,965,000 |
| 2022 | Paris | the Merge: validators replace miners | 15,537,394 |
| 2023 | Shanghai | validators can take their stake out | 17,034,870 |
| 2025 | Osaka | one transaction may use at most **16,777,216** gas | 23,935,694 |
| next | Glamsterdam | on Sepolia: a new account costs 204,600 gas | not on mainnet yet |

*(my note: 16,777,216 = 2²⁴.)*

**Upgrades leave fingerprints in every block** (p. 26): each upgrade that needed new information added a field to the block,
so a block's fields tell you which rules it was written under. **A block written before London has no base-fee field at all.**

| Upgrade | Added the field | For |
|---|---|---|
| London (2021) | `baseFeePerGas` | the base fee of EIP-1559 |
| Shanghai (2023) | `withdrawals` | stake taken out by validators |
| Prague (2025) | `requestsHash` | deposits and exits of validators |
| Glamsterdam (Sepolia) | `slotNumber` | the 12-second slot of the block |

*"Ethereum: a shared machine, written by validators, ruled by public proposals."*

## Slide errors and loose claims

No errors in the content. Two leftover titles, then three points to read carefully:

1. **Two copied titles.** p. 2 reads "Live Demo: Our First Smart Contract, in Remix", copied from the Remix deck's p. 2;
   the page is really this lecture's opener (one transaction, three questions). p. 20 repeats p. 19's "The Merge, Seen
   in the Clock"; it is really the mining-vs-staking table ("The two answers Ethereum has given"). Only the titles are stale.
2. **p. 17, "two epochs … about 15 minutes"**: two epochs are 2 × 6.4 = 12.8 min. The ~15 min (and week 8's "about 14
   minutes") includes waiting for the epoch you're in to finish. For a quiz, use the slide's 15 min.
3. **p. 14, "once every 192 days"** is correct, but only with stake weighting (see the note there). Don't divide by 813,444 validators.
4. **p. 13, 813,444 validators and 44.3 million ETH**: 813,444 × 32 is only about 26 million ETH. It isn't a contradiction:
   32 ETH is the *minimum* per validator, and many hold more *(my note)*.

Video: the matching lecture is on eClass as VOD 73659, not mirrored or transcribed yet.
