# Blockchain Basics and Platforms

**Instructor:** Jalolliddin Yusupov (j.yusupov@inha.uz) · **Mode:** online, asynchronous
**eClass course id:** `2635`

---

## Material by week

Every week's VODs and slides are summarised in `lectures/`. The `.mp4` files are git-ignored; the
transcripts (`.txt`/`.srt`) and summaries (`.md`) are tracked. The course has **no progress-tracked
activities**, so VOD windows don't affect attendance. The **weekly quiz** does.

### Week 11: security · Homework 3 (10%) · Term Project II teams

The robbery lecture the Tokens deck promised: **ClassBank** emptied by a **Thief** contract in one transaction
(reentrancy), then repaired by moving one line. **[Homework 3](homework/hw3/README.md)** (posted 11-22, due
**Sun 11-29 23:55**) is built on this deck (Part B) and the week-10 Tokens deck (Part A: deploy your own ERC-20 on Sepolia).

| Item | Length | Notes |
|---|---|---|
| [SLIDE] Security: How Contracts Get Robbed (ubfile 73944) | 24 pp | Lecture 14. **Downloadable**: [pdf](lectures/slides/week11%20-%20Security%20-%20How%20Contracts%20Get%20Robbed%20(slides).pdf) · [summary](lectures/summaries/week11%20-%20Security%20-%20How%20Contracts%20Get%20Robbed%20(slides).md). ClassBank robbed by the Thief call by call (reentrancy), the DAO hack (2016), the check → write → pay fix; overflow, Panic 0x11 and the BeautyChain hack (2018); five defences; the Bybit hack (2025): send vs approve vs sign/permit, six wallet habits; proxies (USDC's admin can change its code). ⚠️ p. 2 still has the Tokens deck's title; p. 15 calls 250 − 1,000 an "overflow" (strictly an underflow) and BEC's bug was a multiplication |
| [CODE] Security (ubfile 73974) | 3 files | [`resources/week11 - Security source/`](resources/week11%20-%20Security%20source/): `L14_1_ClassBank.sol`, `L14_2_ClassBankFixed.sol`, `L14_3_Thief.sol` |
| [VIDEO] Security: How Contracts Get Robbed (VOD 73981) | 1:09:59 | Not mirrored or transcribed yet. The handout points to it for the B.1 screenshot and the B.4 drawing format |
| [HOMEWORK] Assignment 3 (assign 73929) | 10% | 🆕 Brief: [homework/hw3](homework/hw3/README.md). Part A needs **≥ 0.02 Sepolia ETH**, so check the faucet early. B.4 is handwritten |
| [Term Project II] Team Formation Poll (choice 73942) | — | 🆕 **Pick a team by Sun 12-06.** Teams of **6–8**; 36 slots. No team by the deadline = random assignment, and teams under 6 get random members added. Changeable until then. Guidelines "soon". Linked from the top of the page as *Team Poll URL* (73982); *Homework 3 URL* (73930) links the assignment |
| Chat for Team Discussions (ubchat 73975) | — | Top of the page, "For testing" |

The week-10 **[CODE] Tokens** file (ubfile 73973, posted with this week's material) is the lecture's ClassCoin →
ClassToken series: [`resources/week10 - Tokens source/`](resources/week10%20-%20Tokens%20source/) (`L11_1` … `L11_7`).
Two old top-of-page links were removed: the *Term Project I* URL (73311) and the week-7 games file (72944,
still mirrored in `resources/week07 - games`).

### Week 10: validators and tokens

Two decks, each with its own video. The Tokens deck ends by announcing **the security lecture** next: how token
contracts get robbed, and how to defend them.

| Item | Length | Notes |
|---|---|---|
| [SLIDE] Ethereum Validators (ubfile 73658) | 28 pp | Deck dated 11-14; its title page reads "One Transaction, Three Questions". **Downloadable**: [pdf](lectures/slides/week10%20-%20Ethereum%20Validators%20(slides).pdf) · [summary](lectures/summaries/week10%20-%20Ethereum%20Validators%20(slides).md). EVM, opcodes, gas as the alarm clock, memory vs storage; stake, validators, 12 s slots, epochs, votes, slashing, finality, the Merge; EIPs, clients, upgrades (London, Paris, Shanghai, Osaka, Glamsterdam) |
| [VIDEO] Ethereum Validators (VOD 73659) | — | Not mirrored or transcribed yet |
| [SLIDE] Tokens: Money Made of Code (ubfile 73706) | 26 pp | Deck dated 11-15. **Downloadable**: [pdf](lectures/slides/week10%20-%20Tokens%20-%20Money%20Made%20of%20Code%20(slides).pdf) · [summary](lectures/summaries/week10%20-%20Tokens%20-%20Money%20Made%20of%20Code%20(slides).md). A token is a mapping in one contract (ClassCoin), `require`, events and log topics, ERC-20's nine names, decimals, OpenZeppelin, `approve`/`transferFrom` and unlimited approvals, stablecoins (USDT, USDC, DAI, UST), what USDT's owner can freeze, real-world assets, ERC-721 and ENS |
| [VIDEO] Tokens: Money Made of Code (VOD 73709) | — | Not mirrored or transcribed yet |

### Week 9: Ethereum, gas and the Remix demo · Term Project I (25%)

The start of the smart-contract half. **[Term Project I](homework/term-project-1/README.md)** (posted 11-09, due
**Wed 11-18 23:55**) is built on these three decks: the Gas deck for Part B, the Remix deck for Parts A and C. The Gas and
Remix summaries point out the pages the project cites.

| Item | Length | Notes |
|---|---|---|
| [SLIDE] Ethereum Introduction (ubfile 73239) | 13 pp | Deck dated 11-07; title page "Where It Came From, and What It Is". **Downloadable**: [pdf](lectures/slides/week09%20-%20Ethereum%20Introduction%20(slides).pdf) · [summary](lectures/summaries/week09%20-%20Ethereum%20Introduction%20(slides).md). Why stop at coins, Script's four limits, smart contracts, Vitalik Buterin, block 0 (30 Jul 2015), four things called Ethereum, Bitcoin vs Ethereum |
| [SLIDE] Ethereum: Gas, Wei, Fees (ubfile 73262) | 25 pp | Deck dated 11-08; title page "Ethereum, Part 2" (Term Project I calls it Lecture 10). **Downloadable**: [pdf](lectures/slides/week09%20-%20Ethereum%20-%20Gas,%20Wei,%20Fees%20(slides).pdf) · [summary](lectures/summaries/week09%20-%20Ethereum%20-%20Gas,%20Wei,%20Fees%20(slides).md). State and accounts (120 bytes), state root and trie, EOA vs contract, the account nonce, stuck transactions, gas, wei and gwei, the 21,000 vs 204,600 puzzle (EIP-8037 on Sepolia), gas limit, base fee, tip, burnt, savings, EIP-1559, issuance |
| [SLIDE] Demo: Remix (ubfile 73302) | 14 pp | Deck dated 11-08; title page "Ethereum, Part 2: Remix DEMO" (Term Project I's Lecture 11). **Downloadable**: [pdf](lectures/slides/week09%20-%20Demo%20-%20Remix%20(slides).pdf) · [summary](lectures/summaries/week09%20-%20Demo%20-%20Remix%20(slides).md). `Storage.sol` written, compiled, deployed, `store(42)` (a transaction, 43,718 gas) and `retrieve` (a call, free); Remix VM vs Sepolia |
| [VIDEO] *Ethereum Introduction (PART 1)* (VOD 73240) · *Ethereum: Gas, Wei, Fees (PART 2)* (VOD 73265) · *Remix DEMO* (VOD 73303) | — | Not mirrored or transcribed yet |

### Week 8: wallets, forks and types of blockchain

The last lecture of the Bitcoin half: smart contracts are weeks 9–11. There's no quiz in this section so far, and
**Term Project I hasn't been posted** (the syllabus says it's announced in week 8; eClass has only its grade item).
*(It was posted on 11-09; see week 9.)*

| Item | Length | Notes |
|---|---|---|
| [SLIDE] Wallets, Forks and Types of Blockchain v2.0 (ubfile 72984) | 28 pp | 🆕 10-31. **Downloadable**: [pdf](lectures/slides/week08%20-%20Wallets,%20Forks%20and%20Types%20of%20Blockchain%20(slides).pdf) · [summary](lectures/summaries/week08%20-%20Wallets,%20Forks%20and%20Types%20of%20Blockchain%20(slides).md). Hot/cold, custodial, multisig, soft and hard forks, Bitcoin Cash, the DAO, replay attacks and chain ID, public/private/permissioned, proof of stake, finality. Demo: [sandbox.eth.build](https://sandbox.eth.build) |
| [VIDEO] Wallets, Forks and Types of Blockchain, Parts 1 and 2 (VOD 72985, 72990) | 1:00:05 + 36:21 | 🆕 10-31. Not transcribed yet |

### Week 7: mining, plus four practice games · Homework 2 (5%)

| Item | Length | Notes |
|---|---|---|
| [SLIDE] Mining: Who Writes the Block (ubfile 72902) | 28 pp | **Downloadable**: [pdf](lectures/slides/week07%20-%20Mining%20-%20Who%20Writes%20the%20Block%20(slides).pdf) · [summary](lectures/summaries/week07%20-%20Mining%20-%20Who%20Writes%20the%20Block%20(slides).md). Proof of work, target and bits, nonce, difficulty, hashrate, coinbase, subsidy and halving, difficulty adjustment, pools, orphans, confirmations, 51% attack |
| [VIDEO] Mining: Who Writes the Block, Parts 1 and 2 (VOD 72903, 72908) | — | Not mirrored or transcribed yet |
| [SOURCE FILES] Mining (ubfile 72937) | 1 KB | 🆕 10-25. [`resources/week07 - Mining source/`](resources/week07%20-%20Mining%20source/README.md): `pow.py` (find a nonce by brute force) and `blockhash.py` on a real header |
| [HOMEWORK] Assignment 2 (assign 72938) | 5% | 🆕 10-25, **due Mon 11-09 23:55**. Brief: [homework/hw2](homework/hw2/README.md). Sepolia transactions, reading and hand-decoding Bitcoin transactions, mining by hand. **Task 2.6 needs screenshots at three times of one day, and 3.5 needs two looks 30 min apart**, so start those early |

The **HTML practice games** he promised in the week-6 Part 2 video. Each is an eClass page with the game embedded
inline; saved here, they run offline in any browser. There's no score submission, so they're **practice, not
graded**, and good quiz prep. All use the real payment `d9f91d3f…6dd6` from Slide 6.

| Mod | Game | Local file | What you do |
|---|---|---|---|
| 72664 | Lock & Key | [game1](resources/week07%20-%20games/game1-lock-and-key.html) | Step a P2PKH lock on the stack, one opcode at a time (also wrong keys and a 2-of-3 P2SH) |
| 72665 | The Byte Detective | [game2](resources/week07%20-%20games/game2-byte-detective.html) | Read the 225-byte payment field by field (little-endian), then compute its txid |
| 72666 | The Shapeshifter | [game3](resources/week07%20-%20games/game3-shapeshifter.html) | Transaction malleability, Mt. Gox, and how SegWit fixes it |
| 72667 | The Block Packer | [game4](resources/week07%20-%20games/game4-block-packer.html) | Weight units, vbytes, fee rate, mempool, picking a fee for the next block |

### Week 6: Bitcoin transactions · Quiz 2 (2%)

| Item | Length | Notes |
|---|---|---|
| [VIDEO] Bitcoin Transactions, Part 1 | 50:06 | UTXO, change, fee (not written anywhere), the 225-byte layout, little-endian, txid · [summary](lectures/summaries/vod/week06%20-%20Bitcoin%20Transactions%20(Part%201).md) |
| [VIDEO] Bitcoin Transactions, Part 2 (VOD 72467) | 57:22 | Locks: Script, P2PKH, P2SH, malleability/Mt. Gox, SegWit, vbytes and fee rate · [summary](lectures/summaries/vod/week06%20-%20Bitcoin%20Transactions%20(Part%202).md) |
| [SLIDE] Bitcoin Transactions | — | **Downloadable**: [pdf](lectures/slides/week06%20-%20Bitcoin%20Transactions%20(slides).pdf) · [summary](lectures/summaries/week06%20-%20Bitcoin%20Transactions%20(slides).md) |
| [SOURCE FILES] Bitcoin Transactions (ubfile 72468) | 1 KB | [`resources/week06 - Bitcoin Transactions source/`](resources/week06%20-%20Bitcoin%20Transactions%20source/README.md): two raw tx hex files + `txid.py`, which shows that one changed byte gives an unrelated txid |
| [QUIZ] 2 Week 6 | 1 h | [Quiz 72454](https://eclass.inha.ac.kr/mod/quiz/view.php?id=72454), open 10-18 → **10-25 23:59**, 1 attempt, timer starts when you begin. **Have a calculator ready.** It's week 6's attendance |

### Week 5: wallets and addresses

| Item | Length | Notes |
|---|---|---|
| [VIDEO] Wallets, Addresses and the First Transaction, Part 1 | 55:56 | Slides 72103 are **view-only**. The wallet onboarding the syllabus promised for week 3 |
| [VIDEO] Wallets, Addresses and the First Transaction, Part 2 | 27:58 | The section also has a "Demo Session" label |

### Week 4: Bitcoin blocks and cryptography · Homework 1 (5%)

| Lecture | Length | Summary | HW 1 parts |
|---|---|---|---|
| Bitcoin: Where It Came From, and What a Block Is | 1:04:15 | [md](lectures/summaries/vod/week04%20-%20Bitcoin%20-%20Where%20It%20Came%20From,%20and%20What%20a%20Block%20Is.md) | Part 2 |
| Cryptography for Blockchains | 59:32 | [md](lectures/summaries/vod/week04%20-%20Cryptography%20for%20Blockchains.md) | Parts 3, 4, 5 |

[Homework 1](homework/hw1/README.md) (5%) was due 2026-10-18 23:55: five parts, mostly handwritten, plus
screenshots of your own Bitcoin block and a small Python script.

- **He hides messages in his material.** The week-4 *Cryptography* video had an easter-egg question at 17:34
  ("Why do Lubuntu ISO files come with SHA-256 hashes?"), worth 1 bonus point to the first student to message
  him. It has been claimed. His note: *"Keep an eye out for more hidden treasures in upcoming documents."* So
  read the handouts and slides closely and report anything odd quickly, since only the first finder is rewarded.
- He also said that **hard quiz and homework questions rely on small notes in his slides that he mentions only
  once out loud.** The Merkle odd-leaf rule was one of them, and HW 4.4 uses it.

### Week 3: the big picture

The first modules landed in the **week 3** section on 09-24 and 09-25. Their slides are view-only on eClass,
so the videos were mirrored and transcribed instead.

| Lecture | Length | Summary | Transcript |
|---|---|---|---|
| Intro to Blockchain Technology, Part 1: ledgers, trust, intermediaries, Lehman 2008, double spending | 44:14 | [md](lectures/summaries/vod/week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%201).md) | [txt](lectures/vod/week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%201).txt) |
| Intro to Blockchain Technology, Part 2: shared ledger, consensus, blocks, seals and chains, (de)centralized vs distributed, P2P, gossip, DLT, Bitcoin vs Ethereum, block explorers | 51:05 | [md](lectures/summaries/vod/week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%202).md) | [txt](lectures/vod/week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%202).txt) |

- He said he **may make watching compulsory** if view counts stay low.
- Per Part 1, quizzes **open on Sunday and close the following Sunday**.
- The content covers the syllabus's week 1–2 topics, so the course runs about two weeks behind. He promised
  make-up classes.
- **Contact him through eClass messages or the Q&A board, not email.** "I really don't like emails." Office
  hours are **Saturday 10:00–11:00 online**. The link gets shared, via Zoom or maybe a Telegram stream.

## How this course works, and what can fail you

> *No midterm here. He just mines your free time with proof of work instead.*

- **A new module each Friday evening** on eClass. The first one should
  arrive around **Fri 2026-09-25**.
- **Attendance = submitting that week's quiz.** Missing more than **25% of weeks**
  (about 4) is an **automatic F**. It's the same trap as Distinguished Lecture's VODs.
  Weeks 1–3 had no quizzes, so they shouldn't count against you, but it's
  worth confirming once a TA is named.
- **No exams.** 10% attendance · 15% quizzes · 25% home assignments ·
  25% Term Project I (individual, announced in week 8) · 25% Term Project II (team, due week 16).
- **Hard LMS deadlines**, with unlimited resubmission before the close. You get
  **two 48-hour late passes**, which you request by emailing the TA **at least
  24 hours before** the deadline.
- **Evidence must come from your registered course address** (set up in the
  week-3 onboarding module), **plus handwritten pages**. If either is missing,
  the work is graded as not done. **Keep one wallet for the whole course and
  never lose its seed phrase.**
- **Disclose AI use** in one line per submission.

## Links

- [eClass course page](https://eclass.inha.ac.kr/course/view.php?id=2635)
- [Syllabus viewer](https://eclass.inha.ac.kr/mod/ubfile/view.php?id=71301) (view-only; transcribed in [syllabus/syllabus.md](syllabus/syllabus.md))
- [Class Q&A board](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=70115)
- The announcements board (`70114`) has **disappeared** from the course page.
  News arrives as labels on the week sections instead.

## Folders

```
syllabus/    syllabus.md (transcribed v1)
lectures/    slides/ = downloadable decks · vod/ = recordings (.mp4 local only) + transcripts · summaries/ = .md notes
homework/    home assignments; keep tx hashes and screenshots here
resources/   textbooks and tools
my-notes/    your own notes; keep a record of your course wallet address here (never the seed)
```
