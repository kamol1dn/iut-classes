# Week 10: Tokens: Money Made of Code (slides)

**Blockchain · Week 10 · 26 pages · Dr. Jalolliddin Yusupov · dated 11/15/2026 · online, asynchronous**
Source: [week10 - Tokens - Money Made of Code (slides).pdf](../slides/week10%20-%20Tokens%20-%20Money%20Made%20of%20Code%20(slides).pdf) *(4.6 MB, eClass slide 73706)*

Built from the rendered pages: the text layer holds little more than the titles. Every number below was re-computed.
Notes marked *(my note)* are my own explanations and are not on the slides. The deck is the second half of week 10,
after [Ethereum Validators](week10%20-%20Ethereum%20Validators%20(slides).md), and keeps using the Remix VM accounts
from the [Remix demo](week09%20-%20Demo%20-%20Remix%20(slides).md). The next lecture is announced as **security**: how
such programs get robbed, and how to defend them.

## The five questions the lecture answers

The opener (p. 2): one mainnet block "from this afternoon" holds **222** plain ETH payments and **404** transfers of
something else: dollars, gold, shares of a fund, even names. None of them is ETH, and the rules of Ethereum created none
of them. Each is a small program somebody deployed, exactly as you deployed Storage.

| # | Question | Answer (p. 25) |
|---|---|---|
| 1 | What is a token? | A table of balances in one contract |
| 2 | Why the same words? | ERC-20: nine names every wallet knows |
| 3 | Who else may spend? | `approve`, then `transferFrom`: read what you sign |
| 4 | Can it be a dollar? | Yes, if you trust the issuer |
| 5 | One of a kind? | ERC-721: a number, and its owner |

**Timeline (p. 3):** Nov 2013 whitepaper (its first listed application: "token systems") · 30 Jul 2015 first block,
anyone can deploy a contract · **19 Nov 2015** ERC-20 proposed · **24 Jan 2018** ERC-721, for things that are one of a kind ·
15 Nov 2026: **84.3 billion** dollar coins of one issuer live on Ethereum. Before 2015 people tried to put extra coins on
top of Bitcoin, which was hard because Script can't keep a table of owners.

The whitepaper's definition: a token system is *"a database with one operation"*: take X from A and give X to B, on two
conditions: **A must have at least X**, and **A must agree** to the transaction. The deck writes both conditions in code.

## Part 1: a token is a table (pp. 4–11)

**Token:** a coin that is *not* built into the chain. It exists only as a table of balances inside one contract, and
whoever deploys the contract decides its rules.

| | ETH | A token |
|---|---|---|
| Where the balance lives | in every account (the Remix accounts hold ≈ 100 ETH each) | one table inside one contract: `0x5B38…ddC4` 750, `0xAb84…5cb2` 250, `0x4B20…02db` 0 |
| The accounts | hold their own balance field | hold nothing; the contract keeps the book |

**`mapping(address => uint256)`** (p. 5): a lookup table in storage, a row for every address. `balanceOf[x]` = "the row
of x". **A row never written answers 0, not an error.** You've used one already: Term Project I's **Guestbook** keeps
your number in a mapping row under your address. *("Like the lockers at school: your student ID opens your own locker.")*

**ClassCoin, a whole coin in 10 lines** (p. 6):

```solidity
contract ClassCoin {
    mapping(address => uint256) public balanceOf;
    constructor() {
        balanceOf[msg.sender] = 1000;
    }
    function transfer(address to, uint256 amount) public {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
    }
}
```

| Word | Meaning |
|---|---|
| **`msg.sender`** | The address that sent this transaction. Solidity fills it in, and nobody can fake it because the transaction is signed. It is the whitepaper's "**A agrees**": only A's own signature can move A's row |
| **constructor** | Runs once, at deploy. The deployer's row gets all **1,000** coins |
| **`transfer(to, amount)`** | My row goes down (`-=`), the receiver's goes up (`+=`): the whitepaper's one operation. **No ETH moves**: two numbers inside one contract change |

### Run it: Account 1 sends 250 coins (p. 7)

After deploy: Account 1 = 1,000, Account 2 = 0. After `transfer(Account 2, 250)`: **750 and 250**. The transaction's
data is **68 bytes**:

| Bytes | Part |
|---|---|
| 4 | `a9059cbb`: which function, `transfer(address,uint256)` |
| 32 | `to`: Account 2's address, padded to 32 bytes |
| 32 | `amount`: 250 = `0xfa`, padded to 32 bytes |

**21,000** for any transaction + **572** for these 68 bytes + **28,314** for running `transfer` = **49,886 gas**.

*(my note: the 572 is the calldata price, **16 gas per non-zero byte and 4 per zero byte**. Non-zero: 4 (selector) + 20
(the address) + 1 (`fa`) = 25 × 16 = 400. Zero: 12 (address padding) + 31 (amount padding) = 43 × 4 = 172. 400 + 172 =
572 ✓. The same rule gives the Remix demo's 204 for `store(42)`.)*

### A rule and an announcement (pp. 8–10)

ClassCoin gets two more lines: `require(balanceOf[msg.sender] >= amount, "ClassCoin: not enough coins");` before the
move, and `emit Transfer(msg.sender, to, amount);` after it, with `event Transfer(address indexed from, address indexed to, uint256 amount);`.

| Word | Meaning |
|---|---|
| **`require(check, "message")`** | If the check is false: stop, **revert** everything, return the message. The whitepaper's "A must have X". *Like a cashier who checks your balance first and tells you why the payment failed* |
| **event / emit** | `event` is the shape of an announcement; `emit` sends one. It goes into the transaction's **log**, where wallets look, not into storage. *Like the bank's SMS: your balance is in the book, the SMS is a separate, cheap message* |
| **`indexed`** | Puts the field on the log's label, so a wallet can search "every transfer **to** me" |
| **topic** | One searchable label of a log. **Topic 0** is the hash of the event's name and types (its fingerprint); the other topics are the indexed fields |

| | Good transfer (Account 1 sends 250) | Bad transfer (Account 2, owning 250, sends 1,000) |
|---|---|---|
| status | 1: done | **0: failed**, reverted |
| what comes back | nothing | `"ClassCoin: not enough coins"` |
| gas used | **52,053** | **24,695** |
| balances afterwards | 750 · 250 · 0 | 750 · 250 · 0, unchanged |
| what the world sees | one announcement in the log | no announcement |

**A failure is not free:** nothing changed, but on Sepolia or mainnet the 24,695 gas is really paid. A good wallet warns you before you send.

**The log of the 250-coin transfer** (p. 10): `address` = the contract (`0xd9145CCE…F39138`) · **topic 0** =
`0xddf252ad1be2c89b…f523b3ef` = keccak256(`"Transfer(address,address,uint256)"`) · **topic 1** = from (Account 1) ·
**topic 2** = to (Account 2) · **data** = `0x…fa` = 250 (not indexed). The announcement cost **1,955 gas**: 52,053 with
it, 50,098 without. Cheap, because nothing is written into storage. A wallet searches topic 2 for its own address and finds its coins.

*(my note: the three gas figures are three versions of the contract. 49,886 is the 10-line ClassCoin; 50,098 adds the
`require` (+212); 52,053 adds the `emit` (+1,955). The contract address is the same `0xd9145…9138` as Storage in the
Remix demo because it's again Account 1's first deploy on a fresh Remix VM, at nonce 0.)*

### The same fingerprint on mainnet (p. 11)

Mainnet block **26,420,616** holds **443 transactions**. **404 logs** in it carry topic 0 = `0xddf252ad…`, from **70**
different contracts. Topic 0 and the 4-byte function ID are hashes of the **name and types only**, so the same words give the same bytes.

| | ClassCoin (Remix VM) | Tether USD (USDT), mainnet |
|---|---|---|
| size | 1,000 coins, three accounts | 84,296,691,994 tokens |
| function called | `transfer(address,uint256)`: `a9059cbb` | `a9059cbb`, the same 4 bytes |
| topic 0 of its log | `0xddf252ad…` | `0xddf252ad…`, the same event |
| amount in data | 250 | 90,000,000 (it counts in millionths: **90 USDT**) |
| gas used | 52,053 | 46,109 |

*(my note: 222 ETH payments + 404 token transfers is more than the block's 443 transactions. That isn't a mistake,
because one transaction can emit several Transfer logs.)*

## Part 2: one standard for all (pp. 12–15)

Nothing forces the names. ClassCoin could have said `send` or `pay`, but then MetaMask, Etherscan and every exchange
would need special code for it. *Like the plug and the socket: nobody owns the shape, and everything fits.*

**ERC-20** (p. 13): an **ERC** (Ethereum Request for Comments) is an EIP about how **contracts** should look, not about
the chain's rules. Number 20, proposed on **19 Nov 2015**, fixes the names a token must have. **"ERC-20 is a promise
about names, not a program."**

| Name | 4-byte ID | What it answers or does | ClassCoin |
|---|---|---|---|
| `name` · `symbol` · `decimals` | `06fdde03` · `95d89b41` · `313ce567` | what the token is called, its short name, where its decimal point goes | — |
| `totalSupply` | `18160ddd` | how many tokens exist | — |
| `balanceOf(owner)` | `70a08231` | how many this address owns | ✓ |
| `transfer(to, amount)` | `a9059cbb` | move my own tokens | ✓ |
| `approve` · `allowance` · `transferFrom` | `095ea7b3` · `dd62ed3e` · `23b872dd` | let somebody else spend my tokens, up to a limit (Part 3) | — |
| event `Transfer` · event `Approval` | `0xddf252ad…` · `0x8c5be1e5…` | the two announcements | ✓ · — |

ClassCoin already has three of the names with exactly the same bytes; ready-made code gives the others.

**decimals** (p. 14): a token has no decimal point. The contract counts whole units of its smallest piece, and
`decimals` says where to put the point when showing it. ETH does the same with wei: **18**. These four use **6**:

| symbol | name | decimals | totalSupply, as the contract answers | with the point in place | What the issuer says it is |
|---|---|---|---|---|---|
| USDT | "Tether USD" | 6 | 84,296,691,994,493,958 | **84,296,691,994.49** | 1 token = 1 US dollar |
| USDC | "USD Coin" | 6 | 44,428,039,898,455,098 | **44,428,039,898.45** | 1 token = 1 US dollar |
| XAUt | "Tether Gold" | 6 | 827,417,630,000 | **827,417.63** | 1 token = 1 troy ounce of gold |
| BUIDL | "BlackRock USD Institutional Digital Liquidity Fund" | 6 | 170,275,395,777,549 | **170,275,395.77** | 1 token = 1 dollar share of a fund |

*(my note: **shown value = raw number ÷ 10^decimals**. The slide cuts off after two decimal places instead of rounding,
so BUIDL's 170,275,395.777549 shows as .77, not .78.)*

**Whitepaper vs mainnet:** ERC-20 says `transfer` must answer **true**. USDC does; **USDT answers nothing at all**, so every
wallet and exchange had to learn to accept both. *(my note: our ClassCoin's `transfer` also returns nothing. The ID
`a9059cbb` still matches, because the return type isn't part of the hash.)*

**OpenZeppelin** (p. 15): a free, public **library** of contract code, read and tested by thousands. Nobody writes a token by hand:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts@5.6.1/token/ERC20/ERC20.sol";
contract ClassToken is ERC20 {
    constructor() ERC20("ClassToken", "CLS") {
        _mint(msg.sender, 1000 * 10 ** 18);
    }
}
```

- `is ERC20`: ClassToken gets all nine names, the rule and the announcements, already written.
- `_mint(msg.sender, 1000 * 10 ** 18)`: create 1,000 tokens for the deployer; with 18 decimals that is 1,000 × 10¹⁸ smallest pieces.
- What we got: **3,554 bytes** of program from 8 lines; name ClassToken, symbol CLS, decimals 18. Measured: deploy
  **939,798 gas**; a transfer of 250: **52,189 gas** (ClassCoin: 52,053).

## Part 3: permission to spend (pp. 16–18)

`transfer` moves only the caller's **own** tokens. A shop or exchange contract can't press your button, so you give
permission first and it collects later. *Like a direct debit with a limit.*

| Word | Meaning |
|---|---|
| **`approve(spender, amount)`** | I let this address spend up to `amount` of my tokens |
| **`allowance`** | How much is still allowed |
| **`transferFrom(from, to, amount)`** | The spender moves them |

The contract keeps **two tables**: balances and allowances (who may spend whose). Diagram (p. 16): you own 1,000, sign
`approve(shop, 100)`; the shop signs `transferFrom(you, shop, 60)`. Balances you 1,000 → 940, shop 0 → 60; allowance
100 → 40. **You signed nothing in step 2.**

**Run it with three accounts** (p. 17). Account 1 owns the tokens, Account 2 spends, Account 3 only receives:

| # | Who signs | Transact | Result | Gas |
|---|---|---|---|---|
| 1 | Account 1 (owner) | `approve(Account 2, 100)` | allowance of Account 2 = 100; one Approval announcement | 46,940 |
| 2 | Account 2 (spender) | `transferFrom(Account 1, Account 3, 60)` | Account 1: 690 · Account 3: 60 · allowance left: **40** | 58,426 |
| 3 | Account 2 (spender) | `transferFrom(Account 1, Account 3, 50)` | **failed**: 50 is more than the 40 left; nothing changes | 25,799 |
| 4 | Account 3 (no permission) | `transferFrom(Account 1, Account 3, 1)` | **failed**: no allowance at all | 25,787 |

*(my note: Account 1 starts at 750 from Part 1, so 750 − 60 = 690.)* In steps 2 and 3 the owner signed nothing: the permission was enough.

**The danger: a permission with no limit** (p. 18). Many apps ask you to approve **the largest possible number**,
`0xffff…ffff` = **2²⁵⁶ − 1** (the largest number a uint256 can hold), so they never have to ask again. Of **739** Approval
announcements in **25 blocks** (about five minutes of mainnet): **107 unlimited**, 470 with some other limit, 162 set to 0.
**War story that repeats every week:** a fake site asks for one signature, the wallet shows `approve`, nothing leaves, the
victim relaxes. Later the spender calls `transferFrom` and takes everything. The thief never needed the key.

- **Read what you sign**: "approve" is not "send", and it is not harmless.
- **Approve what you need**: a limit of 100 can lose at most 100.
- **Take it back**: `approve(spender, 0)` cancels a permission.

*"An approval is a signed blank cheque if it has no limit."*

## Part 4: real money on a chain (pp. 19–21)

**Stablecoin:** a token built to keep one price, usually **1 US dollar**. The simplest kind: a company takes a real dollar
and creates one token; it gives the dollar back and destroys the token. On Ethereum alone: **84,296,691,994 USDT** and
**44,428,039,898 USDC** (from `totalSupply` and `decimals`).

| Kind | What stands behind 1 token | Example | What can go wrong |
|---|---|---|---|
| backed by dollars | dollars and US government debt, held by a company off the chain | USDT (Tether), USDC (Circle) | you must trust the company's reserves and its bank |
| backed by crypto | more than 1 dollar of ETH or other tokens, locked in a contract on the chain | DAI | the locked crypto can fall faster than the contract can react |
| backed by an algorithm only | nothing: code creates and destroys tokens to push the price | TerraUSD (UST) | **May 2022**: UST fell far below 1 dollar and never came back; holders lost their savings |

**A decentralised chain, a centralised token** (p. 20, *whitepaper vs mainnet*): nobody can freeze your ETH or bitcoin,
but a token obeys **its contract**, and the contract obeys its **owner**. Read the code, not the advertisement. Found in
USDT's bytecode:

| Function | What it lets the owner do |
|---|---|
| `issue(uint256)` | create new tokens (when new dollars arrive, the company says) |
| `pause()` | stop **every** transfer of the token |
| `addBlackList(address)` | freeze one address: its tokens can no longer move |
| `isBlackListed(address)` | anyone may ask whether an address is frozen |
| `owner()` | answers `0xc6cd…a828`, the one address allowed to call the first three |

**Real-world asset (RWA)** (p. 21): a token that stands for something **outside** the chain: gold, a share of a fund, a
building. The thing stays where it is; only the list of owners moves to the chain. XAUt: 827,417.63 tokens, each one troy
ounce (about 31 g) of gold. BUIDL: 170,275,395.77 tokens, shares of a BlackRock fund holding cash and US government debt.

| The chain proves | The chain cannot prove |
|---|---|
| how many tokens exist (827,417.63 XAUt) | that the gold is really in the vault |
| who holds each one, right now | that nobody else has a claim on it |
| every transfer since the first | that you can get it out tomorrow |
| what the owner is able to do | → for these: an auditor, a contract, the law |

*"The token is perfect bookkeeping for an imperfect promise."*

## Part 5: one of a kind (pp. 22–23)

**Fungible:** every unit is equal to every other. One 10,000 so'm note pays like any other; dollars, gold and ERC-20 tokens
are fungible. A concert ticket, a diploma, a house are **not**.

**ERC-721 / NFT** (non-fungible token), 24 Jan 2018: each token has a number, its **tokenId**, and `ownerOf(tokenId)` answers with one address.

| | ERC-20 | ERC-721 |
|---|---|---|
| The table asks | how many do you own? | who owns number N? |
| Shape | `address → amount` | `number → owner's address` |

**A real ERC-721 that isn't a picture: ENS** (p. 23). The Ethereum Name Service registers readable names ending in `.eth`,
so you can send to a name instead of 42 hex characters. Each name is one ERC-721 token that can be held, sent and sold:
`vitalik.eth` → tokenId = keccak256("vitalik") = `0xaf2caa1c2c…a67c7103cc` (77 digits long in decimal) → `ownerOf` →
`0x2208…3a9d`, registered until 2048. An ERC-721 contract also emits `Transfer`, but with the tokenId as a **fourth**
topic: in the block above, **8 of the 404** Transfer logs had four topics. The same shape fits a ticket, a diploma, a land record, a game item, and a picture.

## Three kinds of value, side by side (p. 24)

| | ETH | an ERC-20 token | an ERC-721 token |
|---|---|---|---|
| Where the balance lives | in every account | in one contract: address → amount | in one contract: tokenId → owner |
| Who wrote the rules | the Ethereum rules, changed by upgrades | whoever deployed the contract | whoever deployed the contract |
| The question you ask | the account's balance | `balanceOf(address)` | `ownerOf(tokenId)` |
| To let another spend it | not possible: only your signature | `approve`, then `transferFrom` | the same idea, per token |
| Can somebody freeze it? | **no** | only if the contract has such a function (USDT has) | only if the contract has such a function |
| Measured today | 222 plain payments in block 26,420,616 | 396 transfers in the same block | 8 transfers in the same block |

Only the first column is part of Ethereum itself (396 + 8 = 404 ✓). **What you can do now** (p. 25): open any token on
Etherscan, choose **Read Contract**, and ask it name, symbol, decimals, totalSupply, the balance of an address, the
allowance you gave. No permission, no account.

## Slide errors and loose claims

No real errors found; every number above checks out. Two things to read carefully:

1. **p. 7, the caption** "When Account 1 clicks 'send,' the wallet turns that action into raw computer code" sits on top of the
   `a9059cbb` row. The 68 bytes are the transaction's **data** (which function, then its two inputs), not code; in Remix
   the button is **transact**.
2. **p. 14, rounding**: the "with the point in place" column cuts off after two decimals (BUIDL .777549 → .77). If a quiz
   asks you to convert, divide by 10⁶ and say whether you rounded.

Video: the matching lecture is on eClass as VOD 73709, not mirrored or transcribed yet.
