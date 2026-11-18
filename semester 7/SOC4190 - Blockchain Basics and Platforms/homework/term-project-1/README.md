# Blockchain — Term Project I (25%, replaces the midterm)

**Due: Wed 2026-11-18, 23:55 by the eClass clock.** The PDF says 23:59, but eClass closes at 23:55, and the
LMS is the one that counts. Submit on [eClass, assignment 73309](https://eclass.inha.ac.kr/mod/assign/view.php?id=73309).
Posted 2026-11-09. Individual work, 100 points. Resubmission is unlimited until the close, so upload early and replace.

Files: [Term Project I.pdf](Term%20Project%20I.pdf) (the handout, 9 pages) ·
[SOC4190 Term Project 1 Template.docx](SOC4190%20Term%20Project%201%20Template.docx) (the official template.
**It stops after A.1 with "etc…"**, so you build the rest yourself; keep his numbering) ·
[Guestbook.sol](Guestbook.sol) (the Part C contract, identical to the one printed in the handout).

Put your own working files (draft report, screenshots, the photo, the zip) in `work/`. It is git-ignored.

> **His rules, from the handout:**
> - A screenshot that doesn't show **your own address** is worth zero. On Etherscan the **address bar** and **From**
>   must be visible. In Remix the **Account** box of "Deploy & run transactions" must be visible. Use the computer's
>   screenshot tool, not a phone photo. Don't crop the result.
> - **Every** transaction must come from your **registered address** (MetaMask Account 1). Account 2 is ungraded.
> - B.3 ✍ is **handwritten**, with your name and ID on the sheet. Show the steps; typed arithmetic scores zero.
> - **Never** show a Secret Recovery Phrase or a private key anywhere. Nothing in this project needs them.
> - The grader **reads the chain**: your Storage contract must return **N+1** at grading time, it must have been
>   created by your address, and the guestbook must hold **N** for your address.
> - The syllabus asks for **one line disclosing AI use** in every submission. This handout doesn't repeat it, but
>   put it at the top of the report anyway.

## What you hand in

```
SOC4190_TP1_<StudentID>_<Surname>.zip
└── report.pdf      the filled template, exported to PDF; answers numbered A.1, B.3, C.2 … as in the handout
```

At the top of the report: **N**, **N+1**, your registered address, your Storage contract address and the guestbook
address `0x683da2EF81ea1a9a68506033c21575F254A73B54`.

## Your numbers

| Name | Rule | Example (ID U2310123) |
|---|---|---|
| **N** | the last five digits of your student ID, as a number (00000 → 1) | 10123 |
| **N+1** | N plus one | 10124 |
| Registered address | your MetaMask **Account 1**, on Sepolia | 0x… |
| Course address | the address paid in Homework 2 | `0x02B75C782186B7615730A246D0b366d54Fa38772` |
| Guestbook | the instructor's class contract | `0x683da2EF81ea1a9a68506033c21575F254A73B54` |

## The run-sheet: six transactions, in this order

Have **at least 0.01 Sepolia ETH** on Account 1 first (any Sepolia faucet; Google Cloud's Web3 faucet is the one
the lecture showed). Then do the on-chain part in one sitting, from Account 1, sending nothing else in between.
The nonce answer in A.5 is cleanest that way.

| # | Task | Kind | What you do | Capture **before moving on** |
|---|---|---|---|---|
| 0 | A.0 | setup | remix.ethereum.org → open `contracts/1_Storage.sol` → **Compile** → Deploy & run → Environment **Browser Extension → MetaMask** → connect **only Account 1**. Check: Sepolia, chain ID 11155111, your address, balance > 0 | 📸 **A.1 Remix**: Environment (Browser Extension, Sepolia) + Account box |
| 1 | A.1 | **tx** | **Deploy** (Value 0, gas auto) → Confirm in MetaMask | Contract address (copy icon) · deploy tx hash · 📸 Etherscan deploy page: From = you, "Contract … Created" visible |
| 2 | A.2 | **tx** | `store(N)` → **Transact** → Confirm | tx hash · 📸 Etherscan: From = you, To = your Storage, Success |
| 3 | A.3 | call | **Call** `retrieve` | 📸 **A.3 Remix**: `0: uint256: N` + Account box + contract address. **Take it now: step 4 overwrites N** |
| 4 | A.4 | **tx** | `store(N+1)` → Transact → Confirm → **Call** `retrieve` | tx hash · 📸 Etherscan page · 📸 Remix showing N+1 |
| 5 | B.1 | **tx** | MetaMask only: send **0.001** Sepolia ETH to the course address | tx hash · 📸 Etherscan: From = you, To = course address |
| 6 | C.1–C.2 | **tx** | New file `contracts/Guestbook.sol` (paste [Guestbook.sol](Guestbook.sol)) → Compile → Deployed Contracts → **Add Contract** (older Remix: "At Address") with the guestbook address. **Do not press Deploy.** Call `hasSigned(your address)`: it must be `false`. Type **N** carefully → `sign` → Transact → Confirm | tx hash · 📸 Etherscan: From = you, To = guestbook, Success |
| 7 | C.3 | call ×2 | `numberOf(your address)` → Call; `count` → Call | 📸 **one** Remix screenshot with both results + Account box; type both values into the report |

**On every Etherscan page:** click **"Click to show more"** before the screenshot, so Gas Limit, Gas Fees, Burnt and
Nonce are visible. Those five screenshots are the proof for the B.2 table, and no new ones are asked for. Zoom
the browser out (Ctrl −) until the address bar and the whole result fit.

**One-way doors:**
- The guestbook accepts **one** signature per address, forever. A wrong N can't be fixed. If MetaMask or Remix
  warns that the transaction will fail, **Reject**: you've already signed.
- After A.4, **don't store anything else** in your Storage contract. The grader expects `retrieve` = N+1.
- Pressing **Deploy** on the guestbook makes a private copy nobody grades, and it costs a lot of gas.

## Then the writing

| # | Points | Type | What to hand in | Read first |
|---|---|---|---|---|
| A.1 | 8 | 💻 | contract address, deploy hash, 2 screenshots | Remix deck p.8 (deploy = tx with no receiver; address from sender + nonce) |
| A.2 | 6 | 💻 | hash + Etherscan screenshot | Remix deck p.9 |
| A.3 | 5 | 💻 | Remix screenshot showing N | Remix deck p.10 (call vs transaction table) |
| A.4 | 8 | 💻 | hash + Etherscan + Remix showing N+1 | Remix deck p.13, step 7 |
| A.5 | 8 | ✏️ | (a) table: the 5 actions → "transaction" / "call"; (b) 2 sentences: why `retrieve` was free and isn't on Etherscan; (c) nonce **before** deploy (= Nonce on the deploy page) and **after** the 2nd store (= its Nonce + 1), plus why it grew by that much; (d) 1 sentence: why a deploy one tx later gives a different address | Remix deck p.4, p.8, p.10 · Gas deck p.8 (nonce) |
| B.1 | 3 | 💻 | hash + Etherscan screenshot | — |
| B.2 | 12 | 📋 | 10 rows × 5 transactions, **copied exactly with units** | Gas deck p.20 (base fee, tip, burnt, savings) and p.24 (what each row means) |
| B.3 | 14 | ✍ | for the **transfer** and **store N**: wei conversions; gas price = base + tip; fee = gas used × gas price; fee → ETH; burnt = base × gas used; savings = (max − price) × gas used. Compare each with Etherscan | Gas deck p.14 (wei, gwei), p.15 (two fees worked by hand), p.20 (the 147,000-wei savings example). If something doesn't match, write why: that scores *better* than a copied match |
| B.4 | 6 | ✏️ | 3 × 2 sentences: (a) which tx used the most gas and why; (b) why store N and store N+1 differ; (c) why the transfer is exactly 21,000 | Gas deck p.14 (21,000 for a plain transfer), p.16–17 (a **new line in the book** costs extra on Sepolia since 6 Oct, EIP-8037). Remix deck p.9 splits a store's gas. The handout's hint for (b): "before A.2 your number was 0, an empty place" |
| C.2 | 12 | 💻 | hash + Etherscan screenshot | handout p.7–8 |
| C.3 | 10 | 💻 | Remix screenshot: `numberOf` = N and `count`, Account box; both values typed | — |
| C.4 | 8 | ✏️ | 4 sentences: (a) whose account your N lives in now, and how 300 numbers stay apart; (b) who paid to deploy the guestbook, who paid for your line, who pays when the grader reads with calls | handout p.8 (mapping, msg.sender) · Remix deck p.10 (calls are free) |

The handout calls these Lecture 10 (gas) and Lecture 11 (Remix demo). Locally:
[gas deck](../../lectures/slides/week09%20-%20Ethereum%20-%20Gas,%20Wei,%20Fees%20(slides).pdf) ·
[Remix deck](../../lectures/slides/week09%20-%20Demo%20-%20Remix%20(slides).pdf) ·
[Ethereum intro](../../lectures/slides/week09%20-%20Ethereum%20Introduction%20(slides).pdf).
The VODs are on eClass (73240, 73265, 73303) and haven't been mirrored.

## Checklist (from the handout)

- [ ] ZIP named `SOC4190_TP1_<StudentID>_<Surname>.zip`, containing only `report.pdf`.
- [ ] N, N+1, registered address, Storage address and guestbook address at the top.
- [ ] All five transactions (deploy, store N, store N+1, sign N, transfer) from the registered address, with hashes in the report.
- [ ] `retrieve` on your Storage returns **N+1** right now.
- [ ] Guestbook `numberOf(your address)` returns **N**.
- [ ] Every Etherscan screenshot shows the address bar and your address in From; every Remix one shows the Account box.
- [ ] B.2 complete, with units; B.3 is a photo of handwriting with your name and ID.
- [ ] No seed phrase or private key anywhere.
- [ ] First line: AI disclosure (tool + what for), or "no AI used".

> **Possible easter egg:** page 6 has a gold italic note ("I know this is computationally intensive…") styled unlike
> anything else in the handout. He has hidden bonus questions in material before, and the first finder wins. It may
> just be a note, but it's worth a second look.
