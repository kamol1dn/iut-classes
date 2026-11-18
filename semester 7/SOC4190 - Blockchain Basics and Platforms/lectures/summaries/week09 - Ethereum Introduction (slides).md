# Week 9: Ethereum Introduction (slides)

**Blockchain · Week 9 · 13 pages · Dr. Jalolliddin Yusupov · dated 11/7/2026 · online, asynchronous**
Source: [week09 - Ethereum Introduction (slides).pdf](../slides/week09%20-%20Ethereum%20Introduction%20(slides).pdf) *(2.2 MB)*

The deck's own title is **"Ethereum: Where It Came From, and What It Is"**. It's the first lecture of the smart-contract
half, followed by the [Gas deck](week09%20-%20Ethereum%20-%20Gas,%20Wei,%20Fees%20(slides).md) and the
[Remix demo](week09%20-%20Demo%20-%20Remix%20(slides).md). Built from the rendered pages, since the text layer holds little
more than the titles. Notes marked *(my note)* are my own explanations and are not on the slides. It's a short, story-style
deck with no CALCULATE boxes; [Term Project I](../../homework/term-project-1/README.md) lists it as background reading.

## The question the lecture answers

The opener (p. 2, under the news headline *"Ethereum Postponed Its Next Upgrade"*): Bitcoin does one job and, after almost
eighteen years, still does it well: it moves coins from one person to another with nobody in the middle. **If thousands
of computers that don't trust each other can agree on who owns which coin, why stop at coins?** Could they agree on a bet?
A loan? A vote? Could they run any program, so that no company can switch it off and nobody can quietly change it? In 2013 a
19-year-old programmer asked exactly that, wrote his answer in a paper, and less than two years later it was running.

| Part | Stop | Answer |
|---|---|---|
| 1 · Where Ethereum came from | The person | Vitalik Buterin, 19 when he wrote the paper |
| | The paper | November 2013 |
| | The idea | Script is too weak for bigger agreements; build one blockchain that runs any program: a **smart contract** platform |
| | The first block | **30 July 2015** |
| 2 · What Ethereum is | Four things, one name | a network, its rules, the software, the coin |
| | Who does what | users, developers, nodes, validators |

## Part 1: where Ethereum came from (pp. 3–9)

**What we have built** (p. 3): block (Lecture 3), hash and keys (4), wallet (5), payment (6), mining (7), forks (8): one
machine where thousands of strangers keep the same record and nobody is in charge. It does **one job: move a coin from A to
B with nobody in the middle**. What else could such a network agree on? **A bet** (if X happens, pay A), **a loan** (pay back
or lose the deposit), **a vote** (count every member once), **a game** (rules nobody can bend). Bitcoin can do a little of
this with a lot of effort; its tools are few on purpose. *"Bitcoin answers one question: who owns which coin?"*

**Why build a new blockchain for every idea?** (p. 4). Think of 2005: your pocket held a phone, a camera, a music player and
a map; then one device did all of it. In 2013 each blockchain idea was its own device:

| Device | 2013 project | Job |
|---|---|---|
| calculator | **Bitcoin** | money |
| camera | **Namecoin** (2010): a blockchain only for registering names | names |
| music player | **colored coins**: bitcoins marked to stand for something else, like a share | assets |
| map | **Mastercoin**: new features added on top of Bitcoin | contracts |

A new idea meant a new coin, or a new layer on top of an old one. The idea: **one machine, any job**. Anyone adds a program,
nobody asks permission, no new coin is needed. *"Bitcoin was a very good calculator. Could a blockchain be a smartphone?"*

**What Bitcoin's Script cannot do** (p. 5). In Lecture 6 we ran a real lock on a stack (OP_DUP, OP_HASH160, OP_EQUALVERIFY,
OP_CHECKSIG). Script is small on purpose and asks one question: may this coin be spent? Ethereum's whitepaper doesn't say
Script is bad; it says Script is **too weak to carry bigger agreements**, and names exactly **four reasons**:

| Reason | What it means | Whitepaper's term |
|---|---|---|
| **No loops** | It can't repeat a step; long jobs are impossible | "Lack of Turing-completeness" |
| **Blind to amounts** | An output is spent whole; no "take out only 10 %" | "Value-blindness" |
| **No memory** | Spent or unspent: that's all it can remember | "Lack of state" |
| **Blind to the chain** | It can't read the block it lives in: no time, no nonce | "Blockchain-blindness" |

*"A lock only needs to open or stay shut. A program needs more."*

**New word: smart contract** (p. 6): a program that lives on a blockchain, holds money and follows its own rules; nobody has
to approve each step. **Two bad words:** it's not *smart* (it does only what is written, as the DAO showed in Lecture 8),
and it's not a legal *contract* (no court is involved). The name stayed anyway.

| A shop | A vending machine | A smart contract |
|---|---|---|
| A person takes your money. They may refuse, cheat, or close for lunch | Coin in, drink out, change back. The rules are built into it, but its owner can switch it off | The rules are a program on a blockchain. Thousands of nodes run it. No single person can switch them off |

`IF coins ≥ price THEN give drink and change ELSE give the coins back`. *"A vending machine is an old smart contract. It needs no shopkeeper."*

**Who wrote it? This time we know** (p. 7). Lecture 3 asked who Satoshi Nakamoto is, and nobody knows. Ethereum's author,
**Vitalik Buterin**, is a programmer you can watch on video. Timeline: **1994** born in Kolomna, Russia · **age 6** family moves
to Canada · **age 17** hears of Bitcoin from his father · **2011** co-founds *Bitcoin Magazine* · 2013 writes the whitepaper
(University of Waterloo, dropped out). **The lesson from a game:** he loved World of Warcraft, an online game run by one
company. One day the company changed his favourite spell for everybody; he writes that he cried himself to sleep and saw
"what horrors centralized services can bring". *"One company changed one rule for everyone. That is what a blockchain is built to prevent."*

**Turing-complete:** a machine is Turing-complete if it can run any program a computer can run, loops included (named after
Alan Turing, who described such a machine in 1936). Bitcoin's Script is not; Ethereum was built to be. *"Bitcoin's paper said:
here is cash without a bank. Ethereum's said: here is a computer without an owner."*

**Old ideas, one new combination** (p. 8). Almost nothing in Bitcoin's whitepaper was new (Lecture 3), and the same is true here:

| Year | Idea | What it gave |
|---|---|---|
| 1936 | Alan Turing | one machine can run any program |
| 1996 | Nick Szabo | rules enforced by a machine, not a court |
| 2008 | Satoshi Nakamoto | strangers agree with nobody in the middle |
| 2009 | Bitcoin Script | small programs inside a transaction |
| 2010–13 | Namecoin, Mastercoin | people want a chain to do more than pay |

**Ethereum's contribution** was putting them together: a blockchain with **one machine built in**, so the record holds
programs as well as who owns what, and all nodes run them the same way. The team called the dream a **"world computer"**.
*"Bitcoin combined old ideas to make money. Ethereum combined old ideas to make a computer."*

**30 July 2015: the first block** (p. 9). **Ether (ETH):** the coin of Ethereum, used to pay for transactions and programs.
Ether is to Ethereum what bitcoin is to Bitcoin; you've been spending it, in Sepolia form, since Lecture 5.

| Ethereum block 0, read from a node | Value | Meaning |
|---|---|---|
| timestamp | 0 | 1 January 1970 in Unix time (Lecture 3) |
| transactions | 0 | the sale's balances were written in directly |
| limit of work | 5,000 | too small for one payment |
| block hash | `0xd4e56740…cb8fa3` | |
| extra data | `0x11bbe8db…1b82fa` | a hash: of **testnet block 1,028,201** |

Bitcoin's block 0 held a newspaper headline of its day, proving it wasn't made before that day (Lecture 3). Ethereum's block 0
holds the hash of testnet block 1,028,201, which nobody could predict before that block was made: the same trick, with a hash
in place of a headline. **Why 1,028,201?** It reads the same in both directions and it's a prime number; the team chose it
for fun, and said so. *(my note: both checked ✓. Also, "too small for one payment" is because a plain transfer needs 21,000 gas,
which you meet in the Gas deck.)* *"Bitcoin's first block quotes a newspaper. Ethereum's first block quotes a hash."*

## Part 2: what Ethereum is (pp. 10–12)

**Four things with one name** (p. 10). People say "Ethereum" and mean four different things, all correct, exactly as we found for Bitcoin in Lecture 3:

| A network | The rules | The software | The coin |
|---|---|---|---|
| thousands of computers, called **nodes**, all over the world | a **protocol**: what counts as valid, written in the **Yellow Paper** and **EIPs** | free programs anyone may run: **Geth**, **Nethermind** and others | **ether, or ETH**: what you pay with, and what validators lock up |

By habit, **Ethereum** with a capital E is the system; **ether, or ETH**, is the coin. **One difference matters:** Bitcoin has
one main program; Ethereum has several, written by separate teams, so one bug doesn't stop everybody. **EIP** = Ethereum
Improvement Proposal, the numbered public proposal from Lecture 8. *"A network, its rules, the software, and a coin: that is all a blockchain ever is."*

**Who does what** (p. 11). Mostly the same cast as Bitcoin (Lecture 3: users, nodes, miners). Ethereum keeps users and nodes,
**replaced miners in 2022**, and adds one new role: people who write programs for the chain.

| Users | Developers | Nodes | Validators |
|---|---|---|---|
| hold keys in a wallet, send transactions, pay fees: **you** | write smart contracts and put them on the chain for others to use: **you, in a few weeks** | keep a full copy, check every block, refuse what breaks the rules: **anyone with a computer** | lock ETH as a guarantee, propose and vote on blocks, earn rewards: **812,322 on 5 Nov 2026** |

*"On Bitcoin you send money. On Ethereum you can also send a program."*

**Bitcoin and Ethereum, side by side** (p. 12). Most of what you learned still holds: hashes, keys, signatures, blocks, forks.

| | Bitcoin | Ethereum |
|---|---|---|
| First block | 3 January 2009 | 30 July 2015 |
| Author | Satoshi Nakamoto: nobody knows who | Vitalik Buterin, then a team |
| Built for | electronic cash | programs, and money as one of them |
| Programs | Script: small, no loops (Lecture 6) | a full programming machine |
| A block comes | about every 10 minutes | every 12 seconds |
| Agreement | proof of work | proof of stake, since 2022 |
| Hash used for addresses | SHA-256 and RIPEMD-160 | Keccak-256 |
| Total coins | limited to 21 million | no fixed limit |

*"Same foundations. A different ambition."*

## Slide errors and loose claims

No errors in what the pages say. Two gaps:

1. **p. 2's outline promises stops that have no page:** "the team and the ether sale" and "your page: you are already here".
   Neither has a slide in this PDF; they're presumably covered in the video. (The Gas deck opens with "your page", the
   Homework 2 Etherscan page, so that stop may simply have moved there.)
2. **p. 2's headline, "Ethereum Postponed Its Next Upgrade"**, isn't explained on the slide. The Validators deck (week 10,
   p. 23) gives the story: the Glamsterdam rehearsal on the Hoodi testnet was postponed on 22 Oct 2026.

Video: the matching lecture is on eClass (one of the week-9 VODs 73240, 73265, 73303), not mirrored or transcribed yet.
