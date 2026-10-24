# Syllabus (v1): Blockchain Basics and Platforms

Transcribed from `Syllabus Blockchain Basics.pdf` (eClass mod **71301**, posted
under week 1, first seen 2026-09-23). eClass shows it only in its **view-only document
viewer**, so there's no local PDF; this file is the local copy. The instructor
calls it **v1** and says topics may change slightly, with notice.

| | |
|---|---|
| Course | Blockchain Basics and Platforms · SOC4190 · 2026 Fall |
| Instructor | **Jalolliddin Yusupov**, D.Sc., Professor of CSE |
| Email | j.yusupov@inha.uz |
| Room | A406/4 |
| Office hours | **Saturday 10:00–11:00, online** (link on eClass) |
| TA | To be announced |
| Mode | **Online and asynchronous.** Weekly modules are released on eClass on **Friday evening**, with some live lectures. |
| Grading | Relative |

## Grading

| Component | Weight |
|---|---|
| Attendance (linked to the weekly quizzes) | **10%** |
| Weekly online quizzes | **15%** |
| Home assignments | **25%** |
| Term Project I, individual, replaces the midterm | **25%** |
| Term Project II, team, replaces the final | **25%** |
| Midterm / final exam | **none** |

Grades: A+, A0, B+, B0, C+, C0, D+, D0, F.

## Policies that matter

- **Attendance is the weekly quiz.** Submitting a week's quiz counts as
  attendance for that week. **If you miss more than 25% of weeks without a valid
  reason (under 75% attendance), you get an F.** Over 16 weeks that is about **4 weeks**.
- **Deadlines are hard.** The LMS accepts nothing after the close time.
  **Resubmission is unlimited** before the deadline, so submit early and update later.
- **Two 48-hour late passes per semester.** To use one, email the TA **at least
  24 hours before** the deadline and they open an extension for you. Otherwise a
  missed deadline scores 0.
- **AI use is allowed, but you must disclose every use** in one line per
  submission: which tool, and what for.
- **Submissions are checked against your own evidence:** on-chain values from
  **your registered course address**, plus **handwritten pages**. If the evidence
  comes from a different address or the handwritten pages are missing, the work
  is graded as not done.
- **Assignments are "deliberately large"**, and every part is graded separately.
  They combine test-network tasks (transaction hashes, contract addresses,
  balances, with screenshots showing the registered address) with handwritten
  work (hash and Merkle computations, decoding transactions, fee arithmetic),
  photographed or scanned.
- **Integrity:** copying, or using evidence from another student's address,
  scores **0** on that part of the course.

## Tools

These are all free: a browser with **MetaMask**, **Remix IDE**, a public Ethereum
test network and its explorer (announced in the onboarding module), a Bitcoin
explorer (**mempool.space**), and Python 3 or a Linux command line. You don't
need any real cryptocurrency.

Prerequisites: at least one high-level language, plus Linux and the command line.

## Textbooks

- **Required (free):** Narayanan et al., *Bitcoin and Cryptocurrency
  Technologies*, Princeton 2016, free draft at bitcoinbook.cs.princeton.edu.
- **Required (free):** Antonopoulos & Wood, *Mastering Ethereum*, O'Reilly 2018,
  at github.com/ethereumbook/ethereumbook.
- **Recommended:** Antonopoulos & Harding, *Mastering Bitcoin*, 3rd ed., O'Reilly
  2023, at github.com/bitcoinbook/bitcoinbook.
- **References:** the Bitcoin whitepaper (bitcoin.org/bitcoin.pdf), the Ethereum
  whitepaper, EIP-1559/4844/20/721, the Solidity docs, Roughgarden's
  *Foundations of Blockchains* (timroughgarden.github.io/fob), and napp.uz for
  Uzbekistan's crypto-asset regulations.

Each weekly module lists the chapters to read.

## Weekly plan

| Wk | Dates | Topic | Notes |
|---|---|---|---|
| 1 | 5–11 Sep | Introduction: the trust problem, double-spending, ledgers, blocks and chains | |
| 2 | 12–18 Sep | Blockchain, Bitcoin and Ethereum: centralised vs decentralised, P2P, DLT, first look at a block explorer | |
| 3 | 19–25 Sep | **Onboarding:** create a wallet, protect the seed phrase, **register the course address**, send a first testnet transaction | |
| 4 | 26 Sep–2 Oct | Hashing (SHA-256, Keccak-256), Merkle trees and proofs, keys, ECC, signatures, HD wallets | |
| 5 | 3–9 Oct | Bitcoin transactions: UTXO, raw transaction byte by byte, Script, P2PKH/P2SH, SegWit, vbytes | |
| 6 | 10–16 Oct | Bitcoin blocks and mining: header fields, PoW, halving, coinbase, orphans, 51% attack | |
| 7 | 17–23 Oct | Wallets, forks and blockchain types: multisig, hard/soft forks, DAO/ETC, PoS, BFT | |
| 8 | 24 Oct–1 Nov | Ethereum: accounts, gas, EIP-1559, EVM, the Merge | **No midterm. Term Project I announced.** |
| 9 | 31 Oct–6 Nov | Smart contracts I: Solidity and Remix, deploying and verifying, ABI | |
| 10 | 7–13 Nov | Smart contracts II: ERC-20, ERC-721, ERC-1155, OpenZeppelin, stablecoins | |
| 11 | 14–20 Nov | Smart-contract security: reentrancy, access control, MEV, oracles, flash loans, CTF exercise | |
| 12 | 21–27 Nov | DApps and DeFi: AMMs, lending, oracles, DAOs, NFT marketplaces | |
| 13 | 28 Nov–4 Dec | Scaling: L2 rollups, ZK proofs, bridges, account abstraction, Lightning | |
| 14 | 5–11 Dec | Platforms: Hyperledger Fabric, IPFS, use cases that worked and those that didn't | |
| 15 | 12–18 Dec | Blockchain in Uzbekistan: NAPP, licensing, mining, the Central Bank stablecoin pilot | Term Project II work |
| 16 | 21–25 Dec | Final assessment week. **No final exam.** | **Term Project II due** on eClass |

## Course learning objectives

1. Explain how Bitcoin and Ethereum work (hashing, signatures, transactions,
   blocks, PoW/PoS) and check the mechanics by hand and on an explorer.
2. Create and manage wallets and keys safely on a testnet, and read any
   transaction, block or contract on a public explorer.
3. Design, implement, test and deploy Solidity contracts, including standard
   tokens, on a public Ethereum testnet.
4. Recognise the main classes of smart-contract vulnerability and apply the defensive patterns.
5. Explain DApps, DeFi, scaling and permissioned platforms, and judge when a
   blockchain is the wrong tool.
6. Describe the legal and infrastructure situation for blockchain in Uzbekistan and the region.
