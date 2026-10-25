# Blockchain — Homework 2 (5%)

**Due: Mon 2026-11-09, 23:55 by the eClass clock.** The PDF says 23:59, but the eClass page says 23:55, and
the LMS clock is the one that counts. Submit on [eClass, assignment 72938](https://eclass.inha.ac.kr/mod/assign/view.php?id=72938).
Posted 2026-10-25. Individual work, 100 points.

Files: [SOC4190 Homework 2 v1.0.pdf](SOC4190%20Homework%202%20v1.0.pdf) (the handout, 8 pages) ·
[SOC4190 Homework 2 Template.docx](SOC4190%20Homework%202%20Template.docx) (write the report in this).
The `[SOURCE FILES] Mining` posted with it is the week-7 lecture code, filed under
[`resources/week07 - Mining source/`](../../resources/week07%20-%20Mining%20source/README.md).

> **His rules, from the handout:** a screenshot or a sheet that doesn't show your student ID or your own
> address is worth **zero** ("It could have come from anyone"). Exercises marked ✍ must be **handwritten**,
> with your name and ID on every sheet: typed tables and calculations score zero, and he marks the steps.
> If you used an AI tool, say which one and for what **in the first line of the report**.
> **Never** show a Secret Recovery Phrase or a private key: that screenshot scores zero.

## What you hand in

```
SOC4190_HW2_<StudentID>_<Surname>.zip
├── report.pdf        answers + screenshots + photos of handwriting, numbered 1.1, 2.3 … as in the handout
└── src/
    └── txid.py       Part 2, exercise 2.4, typed by you (not pasted)
```

## Your own numbers (from your student ID)

Write these at the top of the report. Almost every task uses them.

| Name | Rule | Example (ID U2310123) |
|---|---|---|
| Block height **H2** | 840,000 + the last five digits of your ID | 10123 → **850,123** |
| Data string **D** | your surname in CAPITALS, exactly as on eClass | YUSUPOV |
| Transaction **T** | the **second** transaction in block H2 on mempool.space (the first is the coinbase) | look it up |
| Variant | last digit of your ID: 0–3 → **A**, 4–6 → **B**, 7–9 → **C** | 3 → A |
| Account 1 address | your MetaMask Account 1 | your own |

Course address (from the faucet lecture): `0x02B75C782186B7615730A246D0b366d54Fa38772`

## The tasks

| # | Points | Type | What to do |
|---|---|---|---|
| **Part 1** | **30** | | **Your first transaction on Sepolia** (lecture 5) |
| 1.1 | 8 | 💻 | Faucet Sepolia ETH. Send **0.001** to the course address and **0.002** to a new Account 2. Fill From / To / Value / Block / Status for both from sepolia.etherscan.io; screenshots with the address bar visible, plus one of MetaMask showing the sender |
| 1.2 | 5 | 💻 | Screenshot of Account 1 and 2 together (nothing secret). Two sentences: why does one seed give many addresses, and what is lost if the phrase is lost? |
| 1.3 | 5 | 💻 | Restore test: import the wallet in a **second browser profile**, check that the same Account 1 appears, then delete only that new profile. One sentence: where does the account actually live? |
| 1.4 | 6 | 💻 | Change one middle character of the course address. Paste it into MetaMask "Send to" and open it on Etherscan. Write what each did (refused, warned, or showed an empty page). **Send nothing.** One sentence on why all-lowercase would have let the typo through (checksum capitals) |
| 1.5 | 6 | 💻 | Look up the private-key-1 addresses (given in the handout) on mempool.space and **mainnet** etherscan.io: balance, number of txs, date of the latest. Two sentences: why does money sent there vanish in seconds, and who takes it? |
| **Part 2** | **40** | | **Reading Bitcoin transactions** (lecture 6). Put T's full txid at the top of the report |
| 2.1 | 7 | ✍ | Fee = inputs − outputs, all in **satoshi** (1 BTC = 100,000,000 sat). Compare with the explorer's fee. Who gets the difference? (More than 8 inputs/outputs: add the first 8 by hand, take the rest from the explorer's total and say so) |
| 2.2 | 4 | 💻 | Which outputs of T are still unspent (date and time it). Two sentences: what is the UTXO set, and how does it catch a double spend? |
| 2.3 | 10 | ✍ | Take the raw legacy tx for **your variant** from the handout (A/B: 191 bytes, 1 output; C: 226 bytes, 2 outputs). On a printout, bracket and label every field: version, input count, previous txid (reversed), output index, script length, unlocking script, sequence, output count, value, script length, locking script, locktime. Convert each value from little-endian to decimal satoshi and compare with the explorer |
| 2.4 | 10 | 💻 | **Type in** the 5-line `txid.py` from the handout (it's double SHA-256, reversed). Run it on your variant's hex: the byte count and a txid equal to the explorer's. Change one hex digit in a copy and screenshot the new txid next to the old. Two sentences on malleability. Run `echo <your ID>` in the same terminal first so it shows in the screenshot. Optional: try it on your own T (SegWit: it won't match; say why) |
| 2.5 | 6 | ✍ | In block H2 find one **legacy** tx (inputs from `1…`/`3…` addresses) and one **SegWit** tx (`bc1q…`), each with 1–2 inputs and 1–2 outputs. Copy size, vsize, weight and fee; check weight ≈ 4 × vsize; fee rate = fee ÷ vsize. One sentence on why SegWit is cheaper |
| 2.6 | 3 | 💻 | mempool.space front page **three times on one day** (morning, afternoon, late evening), with the computer clock visible. Table of low/medium/high sat/vB and blocks waiting. **Plan for this: it needs a whole day** |
| **Part 3** | **30** | | **Mining by hand** (lecture 7) on andersbrownworth.com/blockchain/block |
| 3.1 | 5 | 💻 | Block = 1, Data = **D**, start at nonce 1, count up by hand until the hash starts with `0` (ignore the red colour, which wants four zeros) |
| 3.2 | 8 | 💻 ✍ | Keep counting until it starts with `00`. Don't change D. By hand: expected attempts 16 and 256, and why; lucky or unlucky? |
| 3.3 | 3 | 💻 | Check a classmate's 3.2 result in one try (no classmate: D = INHA). Two sentences on why "hard to find, easy to check" makes proof of work usable |
| 3.4 | 8 | ✍ | Coinbase of H2: halving count = H2 ÷ 210,000 (whole part), subsidy 3.125 BTC = 312,500,000 sat, total paid = sum of outputs, fees = total − subsidy. Compare with the block page, and name the pool |
| 3.5 | 6 | 💻 ✍ | Etherscan confirmations of your 1.1 tx, **two looks at least 30 min apart**, clock visible. Seconds per block = (minutes × 60) ÷ new blocks. Compare with Bitcoin's 10 min |

If a site is down, use another explorer (blockstream.info, any Sepolia explorer) and say which one.

## Checklist (from the handout)

- ZIP named `SOC4190_HW2_<StudentID>_<Surname>.zip`, with `report.pdf` that opens and `src/txid.py` that runs.
- H2, D, T's txid, your variant and your Account 1 address are written at the top of the report.
- Every screenshot shows your own address, H2, D or student ID. No seed phrase or private key anywhere.
- Every ✍ exercise is a photo of handwriting with your name and ID on the sheet.
- First line of the report: which AI tool you used, if any, and for what.
