# Week 9: Demo: Remix (slides)

**Blockchain · Week 9 · 14 pages · Dr. Jalolliddin Yusupov · dated 11/8/2026 · online, asynchronous**
Source: [week09 - Demo - Remix (slides).pdf](../slides/week09%20-%20Demo%20-%20Remix%20(slides).pdf) *(2.3 MB)*

The deck's title page reads **"Ethereum, Part 2: Remix DEMO"**. Built from the rendered pages, since the text layer holds
only the titles. Every number below was re-computed. Notes marked *(my note)* are my own explanations and are not on the
slides. **This is the deck [Term Project I](../../homework/term-project-1/README.md) leans on** (the handout calls it
Lecture 11): its Part A is this demo, redone on Sepolia with your own N. Page numbers below are the ones the project README cites.

## The five steps of the demo (p. 2)

*"Enough reading. Let us build one."* After the account book and the gas meter (the
[Gas deck](week09%20-%20Ethereum%20-%20Gas,%20Wei,%20Fees%20(slides).md)), we write a tiny contract that remembers one
number, put it on a blockchain, and talk to it. That is enough to see every moving part.

| Step | What happens | Page |
|---|---|---|
| 1 · Write | `Storage.sol`, a few lines | p. 6 |
| 2 · Compile | words become bytes | p. 7 |
| 3 · Deploy | a new contract account is born | p. 8 |
| 4 · Store 42 | a **transaction**: signed, paid, in a block | p. 9 |
| 5 · Retrieve | a **call**: free, no block | p. 10 |

Remix runs all five steps in one browser tab: no installation, no real money. *"Write, compile, deploy, store, retrieve:
the whole life of a contract in five clicks."*

## New words: Remix and Solidity (p. 3)

| Word | Meaning |
|---|---|
| **Remix** | A free website for writing contracts. It holds an editor, a compiler, test wallets and a practice blockchain, all inside your browser |
| **Solidity** | The main language for writing Ethereum contracts. It looks a little like Java or C. Files end in `.sol` |

One browser tab, **app.remix.live**: **editor** (you type Solidity, `1_Storage.sol`) → **compiler** (turns it into bytes,
version 0.8.34) → **test wallet** (Account 1, 100 ETH, `0x5B38…ddC4`) → **Remix VM** (a small blockchain and its node).
*"Toy money, toy chain, real rules: the same code later runs on Sepolia or mainnet."*

## The big picture: who talks to whom? (p. 4)

**Three players.** **You** act through an **EOA** (externally owned account: an account controlled by a private key). A
**node** receives your message and runs the contract. The **contract account** answers. The **blockchain** keeps the history.

**Two kinds of message:**

| Message | What it is |
|---|---|
| **Transaction** | Signed, paid in gas, written into a block. It **changes the state** |
| **Call** | A question to a node. No signature, no fee, no block |

The diagram: you, in Remix (EOA Account 1 `0x5B38…ddC4` holds the private key and signs what you send; you click a button
and Remix builds the message) → ① `store(42)` → the node (EOA `0x5B38…ddC4`: balance 99.999 ETH, nonce 2; contract
account `0xd914…9138`: code 297 bytes, **storage: number = 42**) → ② receipt. Then ③ `retrieve()` → ④ 42, which **adds no
block**. The blockchain holds block 0 (the start), block 1 (deploy Storage), block 2 (`store(42)`): the history that built
the state. The node keeps the **world state: one line per account**; a contract's **storage** is its own saved data.

*"You speak through an EOA. The contract account answers. The node does the work. The blockchain remembers."*

## Two accounts on one screen (p. 5)

Both are 20-byte addresses, and both are lines in the same book. The difference is **who controls the line**: a private key, or the code stored inside it.

| | EOA: Account 1 | Contract account: Storage |
|---|---|---|
| Address in Remix | `0x5B38Da6a701c568545dCfcB03FcB875f56beddC4` | `0xd9145CCE52D386f254917e481eB44e9943F39138` |
| Who controls it | whoever holds its private key | nobody: only its own code |
| Has code | no | yes, 297 bytes |
| Has storage | no | yes: the variable `number` |
| Can start a transaction | **yes**: it signs | **no**: it only answers when called |
| Where Remix shows it | the Account box at the top | the list *Deployed Contracts* |

*"An EOA acts. A contract account reacts."*

## Step 1 · Write: `Storage.sol`, line by line (p. 6)

In Remix: **File explorer → contracts → 1_Storage.sol** (Remix puts it in its default workspace).

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract Storage {
    uint256 number;

    function store(uint256 num) public {
        number = num;
    }

    function retrieve() public view returns (uint256) {
        return number;
    }
}
```

| Piece | Meaning |
|---|---|
| `pragma solidity` | Which compiler versions may build this file: 0.8.2 or newer, below 0.9.0 |
| `contract Storage` | Like a class: code plus its own saved data. Deployed, it becomes a contract account |
| `function store(uint256 num)` | A **function** is a named piece of code that can be run. `store` takes one input, `num`, and saves it |
| `uint256 number` | A whole number, 0 or more, 256 bits wide, kept in the contract's **storage**: data that stays on the chain |
| `public` · `view` | `public`: anyone may call it. `view`: it only reads and changes nothing |

## Step 2 · Compile: from words to bytes (p. 7)

| Word | Meaning |
|---|---|
| **Compile** | Translate a program from words people read into bytes a machine runs. The program that does it is a **compiler**; for Solidity it's **solc** (the demo used solc 0.8.34) |
| **Bytecode** | The bytes the machine runs. Storage's is **297 bytes**, `0x6080604052…0033`, and it's what the chain stores |
| **ABI** (Application Binary Interface) | The list of functions and their inputs, so a wallet knows how to call them: the menu Remix turns into buttons. `store(uint256)` writes and needs a transaction; `retrieve() → uint256` reads, a call |

**The chain never sees our Solidity. It stores and runs only the bytes.** *"Compile once: bytes for the chain, a menu for the people."*

## Step 3 · Deploy: a new account is born (p. 8)

- **Deploy = a transaction with no receiver.** Account 1 signs a transaction whose **data** is the bytecode and whose **to**
  field is empty. The node runs the **constructor** (code that runs only once, at birth) and opens a new line in the book: the contract account.
- **The address is computed, not random.** It comes from the **sender's address and its nonce**, which was 0. On a fresh
  Remix VM, Account 1 is the same for everyone, so your first contract also gets `0xd914…9138`.

```
[vm] from: 0x5B3...eddC4 to: Storage.(constructor) value: 0 wei data: 0x608...20033 logs: 0
status             1 Transaction mined and execution completed
transaction hash   0x95ddbdbdfba78b24835b8dd339e262f82bc0052c171cbf83369b2ba801344684
block number       1
contract address   0xd9145CCE52D386f254917e481eB44e9943F39138
from               0x5B38Da6a701c568545dCfcB03FcB875f56beddC4
transaction cost   117683 gas
execution cost     59509 gas
```

**Transaction cost** (117,683 gas) = everything this transaction paid for. **Execution cost** (59,509 gas) = the part spent running the code.

*(my note: most of the execution cost is the price of storing the code itself, **200 gas per byte**: 297 × 200 = 59,400.
The other 58,174 is the 21,000 every transaction pays, plus 32,000 for creating a contract, plus the bytes of data sent.)*

## Step 4 · Store 42: a transaction (p. 9)

We type 42 next to **store** and press the orange **Transact** button. Remix builds a transaction from Account 1 to the
contract, signs it and sends it to the node. The node runs `store`, writes 42 into storage, and puts the transaction into **block 2**.

The data sent: **`6057361d`** (4 bytes: which function, `store(uint256)`) + **`000…02a`** (32 bytes: 42 in hex is `2a`, padded to 32 bytes).

### CALCULATE: where did 43,718 gas go? (p. 9)

```
  21,000   for any transaction
+    204   for the 36 bytes of data
+ 22,514   for running store
= 43,718   as Remix reports (transaction cost; execution cost 22,514)
```

*(my note: the 204 is the calldata price, **16 gas per non-zero byte, 4 per zero byte**. Non-zero: the 4 selector bytes +
`2a` = 5 × 16 = 80. Zero: 31 × 4 = 124. 80 + 124 = 204 ✓. Most of the 22,514 is writing a number into an empty storage
slot. That's why Term Project I's first `store(N)` costs more than the second one, `store(N+1)`, which only overwrites.)*

*"Writing costs gas, needs a signature, and waits for a block."*

## Step 5 · Retrieve: a call, not a transaction (p. 10)

We press the blue **Call** button next to **retrieve**. Remix asks the node: "run `retrieve` and tell me the result". The
node reads storage and answers 42. **Nothing is signed, nothing is paid, no block is made.**

```
CALL [call] from: 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4 to: Storage.retrieve()
execution cost   2409 gas (Cost only applies when called by a contract)
input            0x2e6...4cec1
decoded output   { "0": "uint256: 42" }
```

| | Transaction (`store`) | Call (`retrieve`) |
|---|---|---|
| Signed by your key | yes | no |
| Costs a fee | yes, 43,718 gas | no (the gas is only counted) |
| Goes into a block | yes, block 2 | no |
| Changes the state | yes: `number` becomes 42 | no: it only reads |

The slide's question: *if reading is free, why does Remix still print a gas number?* (Answer in the terminal line: the
2,409 would be charged only if **another contract** called `retrieve` inside a transaction.) *"Reading is free and instant.
Writing is paid and waits for a block."*

## Where is the blockchain in all this? (p. 11)

In the **Remix VM** the blockchain is real but tiny, and it lives in your browser; every transaction got its own block at once.

```
BLOCK 0 (the start) → BLOCK 1: deploy Storage (0x683e…e385) → BLOCK 2: store(42) (0xf99e…da64)      retrieve(): no block, a call
```

Each block points back to the one before it by hash *(my note: those two short hashes are **block** hashes; the long ones on
pp. 8–9 are **transaction** hashes)*. **The state after block 2**, what the book says now:

| Account | State |
|---|---|
| EOA `0x5B38…ddC4` | balance about 99.999 ETH · **nonce 2** (two transactions sent) |
| Contract `0xd914…9138` | code 297 bytes · storage: `number = 42` (`retrieve()` reads this line) |

**Chain and state, again:** the **chain** is the list of blocks, what happened. The **state** is the book, what is true now.
A call reads the state and never touches the chain. *"Two transactions, two blocks. One question, no block."*

## Toy chain or real chain? (p. 12)

| | Remix VM | Browser Extension (MetaMask) → Sepolia |
|---|---|---|
| Accounts | test accounts, 100 ETH each | your own key and faucet ETH |
| Blocks | made at once, one per transaction | about every 12 seconds |
| Who can see it | only you | anyone, on a block explorer |
| Where it runs | your browser tab: Remix + wallet + node + chain, all in one place | thousands of computers, worldwide |

**Same file, same buttons. Only the Environment menu changes.** *"Practise on the toy chain. When it works, change one menu
and the same contract goes on Sepolia."* (That one menu change is Term Project I's step A.0.)

## DEMO: the whole run, step by step (p. 13)

**Before you start:** open **remix.ethereum.org** (it forwards to app.remix.live). In **Deploy & run transactions** check:
Environment **Remix VM**, rules **Osaka** (the newest Ethereum rules, live on mainnet since 3 Dec 2025). *"Do it with me,
then do it again alone."*

| # | Do this in Remix | Point at this |
|---|---|---|
| 1 | File explorer → contracts → **1_Storage.sol** | one variable, two functions |
| 2 | Press **Compile** (or Ctrl + S) | a green tick; gas hints appear next to each function |
| 3 | Deploy & run → **Deploy** | terminal: block 1, contract address `0xd914…9138` |
| 4 | Open **Deployed Contracts** → Storage | orange **store** (Transact), blue **retrieve** (Call) |
| 5 | Type 42, press **Transact** | block 2, 43,718 gas; the ETH balance drops a little |
| 6 | Press **Call** next to retrieve | `0: uint256: 42`; no block, no fee |
| 7 | **Store 7, then call retrieve again** | the old 42 is gone: storage keeps only the latest value |

*"Every number you see in Remix has a place in the big picture."*

## How Term Project I maps onto this deck

| Term Project I | Demo step | Page |
|---|---|---|
| A.0 connect MetaMask, Sepolia | the Environment menu | p. 12 |
| A.1 deploy | Step 3 (no receiver; address from sender + nonce) | p. 8 |
| A.2 `store(N)` | Step 4 | p. 9 |
| A.3 call `retrieve` | Step 5 | p. 10 |
| A.4 `store(N+1)`, retrieve again | demo row 7 | p. 13 |
| A.5 (a) transaction or call; (c) nonce; (d) new address | transaction vs call; nonce 2 after two transactions; address from sender + nonce | pp. 4, 10, 11, 8 |
| B.4 (b) why the two stores differ | the 43,718 split | p. 9 |
| C.4 who pays when the grader reads | calls are free | p. 10 |

## Slide errors and loose claims

No errors found: every gas sum adds up (21,000 + 204 + 22,514 = 43,718), and the two function IDs are right
(`store(uint256)` = `6057361d`, `retrieve()` = `2e64cec1`). Two things to keep straight:

1. **Remix VM accounts are the same for everyone** (`0x5B38…ddC4`, 100 ETH). That's why everyone's first contract lands at
   `0xd914…9138`. For Term Project I none of these count: every transaction must come from your own MetaMask Account 1 on Sepolia.
2. **p. 10's 2,409 gas** for `retrieve` is not paid by you. Remix prints it because a *contract* calling `retrieve` inside a
   transaction would pay it. A call from your wallet costs nothing and leaves no trace on Etherscan (Term Project I, A.5 b).

Video: the matching demo is on eClass (one of the week-9 VODs 73240, 73265, 73303), not mirrored or transcribed yet.
