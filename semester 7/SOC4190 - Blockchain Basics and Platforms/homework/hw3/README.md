# Blockchain — Homework 3 (10%): my own token · a bank robbery and its repair

**Due: Sun 2026-11-29, 23:55 by the eClass clock.** The PDF says 23:59, but the eClass page says 23:55, and
the LMS clock is the one that counts. Submit on [eClass, assignment 73929](https://eclass.inha.ac.kr/mod/assign/view.php?id=73929).
Posted 2026-11-22 (the handout says "assigned 23.11"). Individual work, 100 points, scaled to 10%.

Files: [SOC4190 Homework 3 v1.0.pdf](SOC4190%20Homework%203%20v1.0.pdf) (the handout, 9 pages) ·
[SOC4190 Homework 3 Template.docx](SOC4190%20Homework%203%20Template.docx) (write the report in this) ·
[MyToken.sol](MyToken.sol) · [ClassBank.sol](ClassBank.sol) · [Thief.sol](Thief.sol).
Lectures it is built on: week 10 *Tokens* ([summary](../../lectures/summaries/week10%20-%20Tokens%20-%20Money%20Made%20of%20Code%20(slides).md),
[code](../../resources/week10%20-%20Tokens%20source/)) for Part A, week 11 *Security: How Contracts Get Robbed*
([summary](../../lectures/summaries/week11%20-%20Security%20-%20How%20Contracts%20Get%20Robbed%20(slides).md),
[code](../../resources/week11%20-%20Security%20source/)) for Part B.

> **His rules, from the handout:** a screenshot or sheet without your student ID, your own address or your own
> numbers is worth **zero**. Etherscan screenshots need the **address bar** visible and **From = your registered
> address**; Part B (Remix VM) screenshots need the **editor tab whose file name starts with your ID**. No cropped
> corners, no phone photos of the monitor. **B.4 is handwritten** (paper, or a tablet with a stylus), with name and
> ID at the top. If you used an AI tool, say which and for what in **one line at the top** of the report.
> **Never** show a Secret Recovery Phrase or private key: the report scores zero.

## What you hand in

```
SOC4190_HW3_<StudentID>_<Surname>.zip
├── report.pdf                    the template, filled in, exported to PDF; answers numbered A.1, B.4 …
└── src/
    ├── MyToken.sol               Part A, with your own name, symbol and supply
    ├── <StudentID>_ClassBank.sol Part B, the bank AFTER the repair (B.5)
    └── <StudentID>_Thief.sol     Part B
```

## Your own numbers (from your student ID)

Write all of these at the top of the report. "Remainder" = what is left after the division.

| Name | Rule | Example (ID U2310123) |
|---|---|---|
| **N** | last five digits of your ID as a number (00000 → 1) | 10123 |
| Supply **S** | 100,000 + N | 110,123 |
| Payment **P** | (N mod 100) + 1, tokens you pay the course | 24 |
| Deposit **D1** | (N mod 7) + 2, ETH Account 1 puts in the bank | 3 |
| Deposit **D2** | (N mod 5) + 1, ETH Account 2 puts in the bank | 4 |
| Vault **V** | D1 + D2 | 7 |
| Token name · symbol | surname + " Coin" · first three letters of the surname in capitals (Latin, as on eClass) | Yusupov Coin · YUS |
| Registered address | your MetaMask Account 1, the one from Homework 2 / Term Project I | your own |

One line of Python does all of it: `N=10123; print(100000+N, N%100+1, N%7+2, N%5+1, N%7+2+N%5+1)`.

Course address: `0x02B75C782186B7615730A246D0b366d54Fa38772`.
**Token amounts take 18 extra zeros**: P = 24 tokens is typed as `24000000000000000000`.

## Before you start

- **At least 0.02 Sepolia ETH in Account 1.** The token deploy alone is about 6.2 M gas ≈ 0.01 Sepolia ETH.
  Low? Use Google's Sepolia faucet (from the lecture) or any other.
- Remix as of 22 Nov (2.6.15): *Deploy & run transactions* has three tabs (Deploy · Deployed Contracts ·
  Transaction History). A function's **Value** box is at the **bottom of the contract's card**; the Deploy tab's
  Value box counts only for the deploy.
- **Remix never clears Value.** Set it back to **0** after every deposit and before every deploy, or the next
  call fails with *"The called function should be payable if you send value"*.
- Compiler **0.8.34** for every file.

## Part A: your token on Sepolia (50 pts)

| Step | Do | Hand in |
|---|---|---|
| A.0 | MetaMask: Account 1, Sepolia. Remix → `contracts/MyToken.sol`, type the file, change **only** the name, symbol and `110123` → your S. Compile 0.8.34 (first compile downloads OpenZeppelin). Environment → *Browser Extension (MetaMask)*: chain 11155111, your address, ≥ 0.02 ETH. Selector = **MyToken**, Value 0, Deploy, Confirm | — |
| A.1 | Wait for the block, copy the contract address and the tx hash, open it on sepolia.etherscan.io | contract address, deploy hash, Remix screenshot (Environment + Account), Etherscan screenshot (From = you, created contract visible) |
| A.2 | Call `name`, `symbol`, `decimals`, `totalSupply` (free calls, no MetaMask) | one screenshot with all four; typed (a) totalSupply as given, (b) with the decimal point, (c) its digit count and why |
| A.3 | `transfer(course address, P + 18 zeros)` → Transact → read MetaMask before confirming. Then `balanceOf` for the course and for yourself | tx hash, Etherscan screenshot (To = your token, Success), Remix screenshot showing P and S − P (with 18 zeros each) |
| A.4 | Etherscan → the transfer → **Logs** tab: copy Address, Topic 0, Topic 1, Topic 2, Data into the table; decode the Data (`int("0x…", 16)`) | screenshot of Logs + the table + four short answers (a)–(d) |
| A.5 | Think | (a) where the course's P tokens are stored and which function reads it; (b) deploy gas vs transfer gas from Etherscan, one sentence why |

Part A is graded from the chain itself: the token must report S with 18 decimals, be created by your
registered address, and the course address must hold P of it.

## Part B: rob your own bank, then repair it (50 pts) · all on Remix VM

| Step | Do | Hand in |
|---|---|---|
| B.0 | Environment → **Remix VM**. Create `<StudentID>_ClassBank.sol` and `<StudentID>_Thief.sol`; change Thief's import to `import "./<StudentID>_ClassBank.sol";`. Compile both. **Keep one of these tabs open in every screenshot** | — |
| B.1 | Account 1: deploy ClassBank (Value 0). Value = D1 ether → `deposit`. Account 2: Value = D2 → `deposit`. Value → 0. `balanceOf` for Accounts 1 and 2 | screenshot: card Balance = V ETH + a balanceOf answer + ID tab; typed: both balanceOf answers in wei |
| B.2 | Copy the bank address. **Account 3**: deploy Thief with `bankAddress` = the bank, Value 0. Thief card: Value = **1 ether** → `attack`. Value → 0. Read both cards' Balance | screenshot(s) of both Balances + ID tab; the before/after table (vault, Thief ETH, book for Accounts 1 and 2); number of payments as a formula in V **and** as your number |
| B.3 | Account 1, Value 0 → `withdraw`. Read the red terminal text | the sentence after *"Reason provided by the contract:"* exactly, a screenshot, one sentence on why the bank can't pay although the book says D1 |
| B.4 ✍ | **By hand**: the robbery as nested boxes ("The Robbery, Call by Call" slide) with your V: `Thief.attack()` (1 ETH) → `deposit` (vault + Thief's book row) → first three `withdraw` calls and the last, each with what check ① reads and the vault before/after payment ②; the Thief function between them and its condition; where line ③ finally runs and how many times; total payments and the Thief's final ETH | photo/scan with name + ID at the top |
| B.5 | Move **one line** of `withdraw` so the order is check → write → pay (add nothing, delete nothing). Compile. **Reset** the Environment (Yes, Reset). Repeat B.1 + B.2 with the repaired bank | the repaired `withdraw` typed with ① check ② write ③ pay marked; screenshot of the failed attack (red text + bank Balance = V + ID tab); the *Reason provided* sentence exactly; the file in `src/` |
| B.6 | Think | (a) what the broken bank hadn't done yet when the Thief asked again; (b) what check ① reads now in the repaired bank, and what happens to the Thief's 1 ETH and the whole transaction |

## Checklist (from page 9)

- ZIP named `SOC4190_HW3_<StudentID>_<Surname>.zip`; `report.pdf` opens; `src/` has three files.
- N, S, P, D1, D2, V, token name and symbol, registered address and token address at the top of the report.
- Both Part A transactions sent from your registered address, both hashes in the report.
- `totalSupply` = S + 18 zeros; `balanceOf(course)` = P + 18 zeros.
- Every Etherscan screenshot shows the address bar; every Part B screenshot shows the ID tab.
- No Secret Recovery Phrase or private key anywhere.
