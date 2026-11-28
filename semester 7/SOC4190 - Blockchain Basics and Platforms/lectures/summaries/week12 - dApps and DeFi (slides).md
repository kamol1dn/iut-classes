# Week 12: dApps and DeFi: A Market With No Shopkeeper (slides)

**Blockchain · Week 12 · 29 pages · Dr. Jalolliddin Yusupov · dated 11/27/2026 · online, asynchronous**
Source: [week12 - dApps and DeFi (slides).pdf](../slides/week12%20-%20dApps%20and%20DeFi%20(slides).pdf) *(5.3 MB, eClass slide 74307)*

Built from the rendered pages, since the text layer holds little more than the titles. Every number below was
re-computed. Notes marked *(my note)* are my own explanations and are not on the slides. The file behind the PDF is
"Slide 15 defi dapss": this is **Lecture 15**, right after
[Security: How Contracts Get Robbed](week11%20-%20Security%20-%20How%20Contracts%20Get%20Robbed%20(slides).md)
(Lecture 14), which announced it as "contracts that trade with each other". It reuses ClassToken (CLS) and ERC-721 from
[Tokens](week10%20-%20Tokens%20-%20Money%20Made%20of%20Code%20(slides).md), 32 ETH from
[Ethereum Validators](week10%20-%20Ethereum%20Validators%20(slides).md), and the check → write → pay order from the
security deck. No code file was posted this week: the three contracts below are copied from the slide images. Page 29
is an empty closing picture. The next lecture is announced as **scaling**: *"sixty million gas per block for the whole
world. How can that be enough?"*

## The five questions the lecture answers

The opener (p. 2): a market with no shopkeeper, a loan with no bank, a dollar no company issues, a vote nobody can
quietly recount, a ticket that cannot be forged. Most of it is a few hundred lines of code, and the class writes three
small ones itself and runs them.

| # | Question | Teaser (p. 2) | Answer (p. 28) |
|---|---|---|---|
| 1 | What is a dApp? | a door and a machine | a website in front of a contract |
| 2 | What does DeFi do? | trade, lend, stable money, stake | a bank's counters, rebuilt as contracts |
| 3 | What else can a dApp do? | own, decide, fund, sell | anything with rules, money and a list |
| 4 | What can go wrong? | prices, order, off switches | ask who can stop each part |
| 5 | What could you build? | one contract, one real need | say what the chain cannot prove |

*"A dApp is rules, money and a list, written as a contract, with a website in front."*

## Where it came from: an exchange with no company inside (p. 3)

**Custodial:** the company holds the coins; the customers hold only a promise. Mt. Gox and FTX were custodial, and both
promises failed. So people asked: can a contract keep the promise instead?

| Date | Event |
|---|---|
| 2014 | **Mt. Gox**, a company, loses its customers' coins |
| 18 Dec 2017 | **DAI** goes live: a dollar that no company issues |
| 2 Nov 2018 | **Uniswap** goes live: an exchange that is only contracts |
| June 2020 | a lending app pays users in its own token; copies follow |
| 2022 | **FTX**, a company, fails the same way as Mt. Gox |
| 27 Nov 2026 | 9,127 projects in 104 categories, listed by one site |

**Built by small teams:** Uniswap was written by Hayden Adams, a former mechanical engineer at Siemens, after a blog post
by Vitalik Buterin. Many of today's examples began as one person's side project. *(my note: the June 2020 app is
Compound, which started handing out its COMP token to its users. That started the rush called "DeFi summer".)*

*"Companies failed; contracts were tried in their place."*

## New word: DeFi (p. 4)

**DeFi (decentralised finance):** money services (exchanging, lending, borrowing) provided by **contracts on a public
blockchain**, not by a company's staff. Nothing in it is new to you: a token, `approve` and `transferFrom`, a contract
that holds ETH, a `require` that says no.

| At a bank or an exchange | Who does it there | In DeFi | Today's example |
|---|---|---|---|
| changes one money into another | a clerk, or the company's list of buyers and sellers | a contract that holds two piles of tokens | Uniswap |
| lends against a deposit | a loan officer, a paper contract, a court | a contract that holds deposits and counts debts | Aave |
| issues a dollar | a company with a bank account | a contract that creates dollars against locked crypto | DAI |
| pays interest on savings | the bank, from its loans | a contract that stakes your ETH for you | Lido |
| knows today's price | the company's own screen | a contract into which somebody writes the price | Chainlink |

*"The counter stays; the clerk is replaced by a contract."*

## Part 1: what a dApp is (pp. 5–7)

### New word: dApp, a website in front of a contract (p. 5)

**dApp (decentralised application):** a website that shows the buttons, plus contracts on a blockchain that do the work.
**The website is only the door. The contracts are the application.** You have used one already: in Term Project I, Remix
was the website, MetaMask the wallet, a node carried your transaction to Sepolia, and Storage was the contract.

```
YOU                 THE WEBSITE          YOUR WALLET          A NODE               THE CONTRACT
press "Exchange" →  prepares the      →  shows it to you;  →  passes it on      →  runs it,
on a web page       transaction          you sign             to the network       inside a block
|<-------- ordinary computers: each one belongs to somebody -------->|          |<- on the blockchain ->|
```

Only the last box is on the chain. Everything before it can be replaced by another, and anything before it can fail.

### Using a dApp: five steps, two signatures (p. 6)

**Connect wallet:** the button on every dApp website. The wallet tells the site **which address** you use, so it can
show your balances. It does not give away your key, and it moves nothing.

| Step | What happens | Signature? |
|---|---|---|
| 1 · **Open** | the website, typed or bookmarked | no |
| 2 · **Connect** | the site learns your address only | **no** |
| 3 · **Approve** | only for tokens: a spending limit | yes |
| 4 · **Confirm** | the action itself: a transaction, with gas | yes |
| 5 · **Check** | on Etherscan: status, amounts | no |

**A website that asks you to sign at step 2 wants more than your address.** Step 3 is the approval from the Tokens
lecture (approve what you need, not "unlimited"); step 4 is where you read the amount before you press. The same five
steps work for every dApp in this lecture; only the words on the buttons change.

### The map: 9,127 projects in 104 categories (p. 7)

One public website, **DefiLlama**, lists such projects and counts the money inside each (on 27 Nov 2026: 9,127 projects,
104 categories). **Not everything listed is DeFi:** the biggest category is **companies' exchanges** (78 of them, 215.7
billion USD), where a company holds the keys. One category is honestly named **Ponzi**: 11 projects.

| Category | What it does, in plain words | Projects | Money inside (USD) | The largest |
|---|---|---|---|---|
| Lending | borrow against a deposit | 486 | 45.1 billion | Aave V3 |
| Liquid Staking | stake ETH, keep a tradable token | 250 | 39.9 billion | Lido |
| Exchanges | exchange tokens, no company | 1,677 | 10.8 billion | Uniswap V3 |
| Stablecoins from locked crypto | create dollars against locked crypto | 184 | 4.5 billion | Sky Lending |
| Real-world assets | tokens for things outside the chain | 92 | 2.9 billion | Re |
| Prediction Market | bets on real-world events | 76 | 340 million | Polymarket International |
| Insurance | pay if something goes wrong | 25 | 139 million | Nexus Mutual Insurance |
| Payments | salaries and payments over time | 23 | 207 million | Lightning Network |
| NFT Marketplace | buy and sell NFTs | 29 | 13 million | Blur Bids |

*"Lending, staking and exchanging hold most of the money."* *(my note: DefiLlama counts every chain, not only Ethereum.
Lightning Network, the top "Payments" entry, runs on Bitcoin. Sky is the new name of MakerDAO, the project behind DAI.)*

## Part 2: DeFi, apps for money (pp. 8–15)

### Example 1: Uniswap, pool number 1 (p. 8)

| Word | Meaning |
|---|---|
| **DEX** (decentralised exchange) | a contract holding two piles of tokens |
| **pool** | that pair of piles |
| **reserve** | one pile |
| **swap** | add to one pile and take from the other. Anyone may do it |
| **factory** | Uniswap's contract that makes a new pool for any two tokens |
| **WETH** (wrapped ether) | an ERC-20 token that one contract hands out 1 for 1 for the ETH you deposit. Pools speak ERC-20, and ETH itself is not an ERC-20. That contract holds **2,272,024.89 ETH** and has issued exactly as many WETH |

**Asked of the chain at block 26,500,825 (26 Nov 2026, 17:20:11 UTC):**

| Question | Answer |
|---|---|
| How many pools has the factory created? | **528,739** |
| Which was the first? | `0xb4e1…c9dc`, created in block 10,008,355 on 5 May 2020 |
| What does pool number 1 hold? | **8,355,669.11 USDC** and **4,947.26 WETH** |
| So its list price is | 8,355,669.11 ÷ 4,947.26 = **1,688.95 USDC for 1 WETH** ✓ |
| Who can stop or change it? | **Nobody**: its 11,293 bytes contain no `pause()`, no `owner()`, no blacklist, no upgrade function |
| Is it the newest? (*whitepaper vs mainnet*) | No: versions 3 (2021) and 4 (2025) exist. **Version 2 runs on, because nobody can switch it off** |

*"No seller, no clerk: two piles and a contract."* *(my note: "pool number 1" is the first pool of Uniswap **version
2**, the USDC/WETH pair. Version 1 from 2018 had older pools with a different factory.)*

### How a pool sets its price: x · y = k (p. 9)

**x · y = k** and **AMM:** call the two reserves **x** and **y**. A swap may change both, but the product **x · y must
not get smaller**. That one rule is the whole price list. A contract that prices this way is an **automated market
maker (AMM)**. Nobody types the price in: **the price is the ratio of the piles**.

**Our own small pool:** 10 ETH and 1,000 ClassToken (CLS), so k = 10 × 1,000 = **10,000**. The list price is
1,000 ÷ 10 = **100 CLS per ETH**.

**Worked by hand: you pay in 1 ETH.**
1. x goes from 10 to **11**.
2. k must stay 10,000, so y must fall to 10,000 ÷ 11 = **909.091**.
3. You receive 1,000 − 909.091 = **90.909 CLS**, not 100.
4. The new list price is 909.091 ÷ 11 = **82.645 CLS per ETH**: your swap made ETH cheaper in CLS for the next person.

| You pay in | x after | y after = 10,000 ÷ x | You receive | CLS for each ETH you paid | List price afterwards (y ÷ x) |
|---|---|---|---|---|---|
| 1 ETH | 11 | 909.091 | **90.909 CLS** | 90.909 | 82.645 |
| 2 ETH | 12 | 833.333 | **166.667 CLS** | 83.333 | 69.444 |
| 5 ETH | 15 | 666.667 | **333.333 CLS** | 66.667 | 44.444 |
| 10 ETH | 20 | 500.000 | **500.000 CLS** | 50.000 | 25.000 |

All four rows check out. **The bigger the bite, the worse the price:** doubling the pile of ETH (10 → 20) buys only
half the CLS. The curve on the slide is y = 10,000 ÷ x; every point on it multiplies to 10,000, and the pile you take
from can never reach 0. *(my note: real Uniswap version 2 also keeps a 0.3% fee from every swap and leaves it in the
pool, so k grows a little each time. That is why the rule says "must not get smaller" and not "must stay equal".)*

### Example 2: Aave, a loan with no bank (p. 10)

**Collateral:** what you lock in the contract as a guarantee. A contract cannot take an address to court, so it lends
**less than the collateral is worth**. The loan is **over-collateralised**. Why borrow less than you own? To have dollars
today without selling the ETH. The ETH stays yours as long as the debt stays well below its value.

**Aave's rule for WETH, read from the contract, with 10 WETH locked:**

| Rule | With 10 WETH |
|---|---|
| the collateral, at the price the contract uses | 10 × 1,692.94 = **16,929.35 USD** (see ⚠️ 1) |
| you may borrow up to **81%** of its value | 0.81 × 16,929.35 = **13,712.78 USD** of a dollar token ✓ |
| the loan is in danger above **84%** | 0.84 × 16,929.35 = **14,220.66 USD** ✓ |
| the bonus for whoever then ends it: **5%** | paid out of your collateral |

Example: a debt of **13,000 USD** is 13,000 ÷ 16,929.35 = **76.8%** of the collateral ✓. **The debt does not move. The
collateral's value shrinks when the price falls.** *"Lock more than you borrow, and nobody needs to know your name."*

### New word: oracle, who tells a contract the price? (pp. 11–12)

**Oracle:** a contract into which somebody outside writes a fact, by transaction, so that other contracts can read it. A
contract cannot open a website. A **price feed** is an oracle for one price.

**Why not simply ask a pool?** Because one big bite moves a pool's price (the table above). DeFi platforms have been
robbed with **flash loans**: huge loans taken and paid back **inside one transaction**, used to bend a pool's price for a
moment.

**The flash-loan attack in five pictures (p. 11):**
1. The attacker borrows a huge amount of token A with a flash loan.
2. They swap A for B in a DEX. Now the pool says A is cheap and B is expensive.
3. They deposit B into a lending contract that reads its price **from that DEX**, and borrow A against it. B looks
   expensive, so they can borrow far more A than B is really worth.
4. They pay back the flash loan.
5. They keep the extra A. The pool's price drifts back, and the lending contract is left holding B worth much less than
   the A it lent.

*(my note: all five steps are in one transaction, so the attacker needs almost no money of their own. If any step fails,
the whole transaction is undone, so the flash loan itself carries no risk for the lender.)*

**One question, three contracts, the same block 26,500,825: how many dollars is 1 ETH? (p. 12)**

| Source | Answer | Notes |
|---|---|---|
| the price feed "ETH / USD" | **1,692.9444** | stored as `169294440000` with 8 decimals (169,294,440,000 ÷ 10⁸ ✓); written 30 min 36 s before the block |
| Aave's own oracle contract | **1,692.9352** | what the lending contract believes (`0x5458…a0c2`) |
| pool number 1: nobody asks it | **1,688.95** | 8,355,669.11 USDC ÷ 4,947.26 WETH; (1,692.9444 − 1,688.95) ÷ 1,692.9444 = **0.24%** lower than the feed ✓ |

The feed is written by a group of independent computers that sign one report together, so **one liar among them is
outvoted**. *"A contract knows only what somebody writes into the chain."*

### New word: liquidation, when the price falls (p. 13)

**Liquidation:** when a debt rises above the allowed share of its collateral's value, **anyone** may repay part of it and
take that much collateral, plus the bonus. No letter, no judge, no second chance: one transaction.

**Worked by hand: when is our 10 WETH loan in danger?** Debt 13,000 USD. Danger when 13,000 > 0.84 × 10 × price, so when
the price < 13,000 ÷ 8.4 = **1,547.62 USD** ✓. That is (1,692.94 − 1,547.62) ÷ 1,692.94 = **8.6%** below today's price ✓.
A fall of under a tenth ends the loan.

**Real liquidations, 25 Nov 2026** (`LiquidationCall` logs of Aave's contract `0x8787…a4e2`):

| Block · time (UTC) | Debt repaid by a stranger | WETH taken from the borrower | Worth, at the feed's price | More than repaid |
|---|---|---|---|---|
| 26,492,826 · 14:34:47 | 2,947,875.85 USDT | 1,893.954 WETH | 3,078,090.92 USD at 1,625.22 | 4.4% |
| 26,492,827 · 14:34:59 | 7,638.71 USDC | 4.912 WETH | 7,983.65 USD at 1,625.22 | 4.5% |
| 26,492,879 · 14:45:23 | 1,672.50 USDC | 1.081 WETH | 1,737.77 USD at 1,607.19 | 3.9% |

The price fell from 1,625 to 1,607 dollars in those minutes (about 1.1%). Rule read from the contract: a bonus of 5%, of
which **Aave keeps one fifth**. Each row was somebody's deposit. Percentages re-checked: 3,078,090.92 ÷ 2,947,875.85 =
1.044, 7,983.65 ÷ 7,638.71 = 1.045, 1,737.77 ÷ 1,672.50 = 1.039 ✓. *(my note: in the first row a stranger repaid about
2.95 million and walked away with about **130,215 USD** more than they paid. A 5% bonus minus Aave's fifth leaves about
4% for the stranger. The rows land between 3.9% and 4.5% because the WETH is valued at the feed's last stored price,
and the price was moving within these minutes; the slide notes the third round was written in the same second.)*

*"The limit is a cliff, not a target: borrow far below it."*

### Example 3: DAI, a dollar no company issues (p. 14)

**CDP (collateralised debt position):** lock crypto in a contract; it **creates new dollar tokens** for you, up to a
limit; give them back to unlock your crypto. In the Tokens lecture's table of stablecoins (backed by dollars, backed by
crypto, backed by an algorithm only), this is how the **second kind** works.

**The story on the slide:**
1. You have $1,500 of ETH and don't want to sell it, because you think it will rise.
2. But you need cash to buy a car.
3. You lock the $1,500 of ETH in the DAI contract.
4. It gives you **1,000 brand-new DAI** (each worth $1).
5. You spend the 1,000 DAI.
6. To get your ETH back, you return 1,000 DAI plus a small fee, and the contract unlocks your ETH.

*(my note: 1,500 locked for 1,000 created means 150% collateral, so you borrowed two thirds of the value. Compare Aave's
81% limit above. The returned DAI is destroyed, which is how DAI leaves circulation again.)*

| Asked of the chain, or of the record | The answer |
|---|---|
| the DAI contract, its name and symbol | "Dai Stablecoin", "DAI" |
| how many DAI exist | **4,336,627,108.72** |
| its successor, the same question | "USDS Stablecoin", "USDS": **3,123,212,600.86** exist |
| what the project says USDS is | "the upgraded version of DAI" (its own description on DefiLlama) |
| when DAI started | 18 December 2017, on the main Ethereum network |
| the risk | if the locked crypto falls fast, it is sold: a **liquidation, at the scale of a whole currency** |

*"A dollar can be a contract's promise instead of a bank's."*

### Example 4: Lido, staking for everyone (p. 15)

**The problem it solves:** from the proof-of-stake lecture, a validator needs **32 ETH**, a computer that never sleeps,
and stake that stays locked. Most people have none of the three.

**Liquid staking:** give any amount of ETH to a contract that stakes it with validators for you. In return you get a
token, **stETH**, that stands for your ETH plus its rewards, and that you can sell or use at any time. *(The slide's
picture is a cloakroom: you hand in your coat and get a numbered tag you can carry around.)*

| Asked of the chain, or of the list | The answer |
|---|---|
| the stETH contract, its name and symbol | "Liquid staked Ether 2.0", "stETH" |
| how much ETH it says it manages | **9,709,710.44 ETH**, the same as the number of stETH |
| how much ETH sits in the contract itself | **14,213.46 ETH**: 14,213.46 ÷ 9,709,710.44 = **0.15%** ✓. The rest works as stake, with validators |
| its place in the list of all projects | the largest by money inside: **16.7 billion USD** |
| what you trust instead of a bank | the contract, the validators it chooses, and the people who can change its rules |

*"A token can stand for locked money and still move freely."* *(my note: stETH balances grow by themselves each day as
rewards arrive, which is why the stETH count equals the ETH count. Check: 9,709,710 ETH × 1,692.94 ≈ 16.4 billion USD,
close to DefiLlama's 16.7 billion, which was probably counted at a slightly different moment or price.)*

## Part 3: beyond money (pp. 16–23)

### Example 5: NFTs and a marketplace (p. 16)

**Marketplace:** a contract that swaps an NFT for a payment **in one transaction** (the slide labels it an *atomic
swap*): either both move, or neither does. The seller never has to trust the buyer, and nobody holds the goods in between.

**Website and contract, again:** OpenSea is a company with a website. **Seaport** is its contract, and the contract does
the trading. Any other website may call the same contract.

| Asked of the chain, or of the list | The answer |
|---|---|
| a famous collection, its name and size | "BoredApeYachtClub": **10,000** tokens, one picture each; `ownerOf(0)` = `0xf780…b66a` |
| OpenSea's contract, its name | "Seaport", **23,981 bytes** of code |
| sales it completed in 50 blocks, about 10 minutes | **7** (its "order fulfilled" announcements). 50 × 12 s = 600 s = 10 min ✓ |
| names you can own | ENS: `vitalik.eth` is an ERC-721 token (Tokens lecture) |
| games | Axie Infinity: "a digital game that fuses NFT collectibles and blockchain" (its own description) |

The picture beside the table is a tweet: someone "saved" a Bored Ape image for free. *(my note: the joke is that
copying the picture copies nothing that matters. Ownership is the `ownerOf` row in the contract, and only the owner's key
can move it.)* *"If it is one of a kind and has an owner, it can be a token."*

### Example 6: deciding together, a DAO (pp. 17–18)

**DAO (decentralised autonomous organisation):** a group whose rules and money live in contracts, and which decides by
**vote of its token holders**. The result is carried out by the contract itself.

| Part | In a DAO |
|---|---|
| the rules and the money | live inside smart contracts, not in a bank account and a rulebook |
| the decisions | everyone who holds the DAO's token may vote |
| the execution | when the vote ends, the contract carries out the result by itself. If the vote says "pay someone $10,000", the code sends it (see ⚠️ 3) |

**One token, one vote.** Not one person, one vote: a holder with a million tokens outvotes a thousand holders with one
each. A class vote would need a different rule: one **address** per student.

**Uniswap's governor contract, asked (p. 18):**

| Question | Answer |
|---|---|
| its name | "Uniswap Governor Bravo" |
| how many proposals so far | **102** |
| the votes you need behind you to make a proposal | **1,000,000 UNI** |
| the "for" votes a proposal needs to pass | **40,000,000 UNI**: 40 M ÷ 1,000 M = **4%** of all 1,000,000,000 UNI ✓ |
| one decision it made | **December 2025**: part of every swap's fee now goes to the protocol |

*"A DAO is a vote whose result no one can ignore."* *(my note: "The DAO" robbed in 2016, from the security lecture, was
one early DAO.)*

### Build it: ClassVote, a vote in 15 lines (p. 19)

```solidity
contract ClassVote {
    string public question;
    uint256 public yes;
    uint256 public no;
    mapping(address => bool) public voted;

    constructor(string memory q) {
        question = q;
    }

    function vote(bool agree) public {
        require(!voted[msg.sender], "ClassVote: already voted");
        voted[msg.sender] = true;
        if (agree) yes += 1;
        else no += 1;
    }
}
```

| Piece | What it means |
|---|---|
| `string` | text |
| `memory` | the text exists only while the constructor runs; then it is copied into storage |
| `!` | "not": `!voted[msg.sender]` means "this address has not voted yet" |
| `voted` | a mapping of addresses to true/false, like Term Project I's Guestbook one-entry rule |

**Run it:** Accounts 1 and 3 vote yes, Account 2 votes no: **yes 2, no 1**. Account 1 tries again: **failed**, "ClassVote:
already voted". **Gas:** deploy 471,527; first vote 66,448; the refused one 24,123.

**Its weak point:** one student with three addresses votes three times. **The chain cannot see people, only addresses.**
*(my note: the 15 lines count every non-empty line. Note the order: the `require` checks, then `voted` is written, then
the count changes. Nothing is paid, so there is nothing to rob.)*

### Build it: ClassFund, a fundraiser with refunds (p. 20)

**The rules, in plain words:** anyone may `give` until the goal is reached. Before that, anyone may take their own money
back. After it, only the organiser may `collect`, and only everything at once. (The slide's logo: Kickstarter, the
company version of the same idea.)

```solidity
contract ClassFund {
    address public organiser;
    uint256 public goal;
    uint256 public raised;
    mapping(address => uint256) public given;

    constructor(uint256 goalWei) {
        organiser = msg.sender;
        goal = goalWei;
    }

    function give() public payable {
        require(raised < goal, "ClassFund: goal already reached");
        given[msg.sender] += msg.value;
        raised += msg.value;
    }

    function refund() public {
        require(raised < goal, "ClassFund: goal reached, no refunds");
        uint256 amount = given[msg.sender];
        require(amount > 0, "ClassFund: nothing to refund");
        given[msg.sender] = 0;
        raised -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "ClassFund: payment failed");
    }

    function collect() public {
        require(msg.sender == organiser, "ClassFund: only the organiser");
        require(raised >= goal, "ClassFund: goal not reached");
        (bool ok, ) = organiser.call{value: raised}("");
        require(ok, "ClassFund: payment failed");
    }
}
```

**The order from the security lecture:** in `refund`: check, **write** (`given = 0`), then pay. The robbery of ClassBank
cannot happen here: a second `refund` call from inside the payment finds `given` already 0.

### Run it: goal 5 ETH, three accounts, nine steps (p. 21)

Account 1 deploys ClassFund with a goal of 5 ETH, then:

| # | Who and what | Result | In the fund (ETH) | Gas |
|---|---|---|---|---|
| 1 | Account 2 gives 3 ETH | done | 3 | 68,135 |
| 2 | Account 3 gives 1 ETH | done | 4 | 51,035 |
| 3 | Account 3 changes its mind: refund | done | 3 | 36,210 |
| 4 | Account 1 collects too early | **failed**: "ClassFund: goal not reached" | 3 | 27,929 |
| 5 | Account 3 gives 2 ETH | done | **5** | 51,035 |
| 6 | Account 2 asks for a refund | **failed**: "ClassFund: goal reached, no refunds" | 5 | 25,777 |
| 7 | Account 2 gives 1 ETH more | **failed**: "ClassFund: goal already reached" | 5 | 25,712 |
| 8 | Account 3 tries to collect | **failed**: "ClassFund: only the organiser" | 5 | 23,703 |
| 9 | Account 1 collects | done | 0 | 34,983 |

**Every "failed" is a `require` doing its job: nobody had to be trusted.** Real ones exist: Juicebox calls itself "light
enough for a group of friends"; its first version holds 9 million USD.

The slide asks which step a **dishonest organiser** would most like to do. *(my note: step 4, collecting before the goal
is reached, and so before the givers have lost their right to a refund. The second `require` of `collect` refuses it.)*

*(my note, on the gas: step 1 costs 17,100 more than step 2 because it writes `raised` for the first time (from 0 to a
number), which is the expensive kind of storage write. Step 5 costs the same as step 2: Account 3's `given` row was set
back to 0 by its refund, so it is a "first write" again, and `raised` was already non-zero.)*

*"Goal reached, money released; goal missed, money returned."* (see ⚠️ 4)

### Build it: ClassTicket, concert tickets as NFTs (p. 22)

```solidity
import "@openzeppelin/contracts@5.6.1/token/ERC721/ERC721.sol";

contract ClassTicket is ERC721 {
    uint256 public price = 0.01 ether;
    uint256 public seats = 100;
    uint256 public sold;

    constructor() ERC721("INHA Spring Concert", "TKT") {}

    function buy() public payable {
        require(msg.value == price, "ClassTicket: wrong price");
        require(sold < seats, "ClassTicket: sold out");
        sold += 1;
        _mint(msg.sender, sold);
    }
}
```

| Piece | What it means |
|---|---|
| `is ERC721` | the contract gets all the ERC-721 rules (owners, `ownerOf`, `transferFrom`) from the OpenZeppelin library, already written |
| `msg.value == price` | you must pay **exactly** 0.01 ETH, not more, not less |
| `sold < seats` | at most 100 tickets |
| `sold += 1; _mint(msg.sender, sold)` | the ticket number is the count after this sale, so tickets are numbered 1 to 100 |

**Run it:** Account 2 pays 0.01 ETH: ticket 1. Account 3 pays 0.005: **failed**, "ClassTicket: wrong price". It pays
0.01: ticket 2. Account 2 gives ticket 1 to Account 3 with `transferFrom`: `ownerOf(1)` is now Account 3. **Gas:** deploy
1,944,418 (the ERC-721 rules come with it); first ticket 94,899, the next 77,799 (again 17,100 apart: `sold` goes from 0
to 1 the first time).

**At the door:** the guard asks the chain "who owns ticket 2?". A copy of a screenshot proves nothing; only the owner's
signature does.

**What is missing?** The **0.02 ETH** of the two tickets stays in the contract. Nothing lets anyone take it out. Add a
`collect` like ClassFund's. *"A ticket is an NFT with a price and a seat count."*

### More examples, one line each (p. 23)

**Look for the pattern:** each one is a list, some money, and rules about who may move it when. That is also the recipe
for your own.

| Kind | Example | What the contract does |
|---|---|---|
| prediction market | Polymarket (317 million USD inside), on Polygon, another chain | holds bets on an event; pays the winners when an oracle reports the result |
| payment over time | Sablier: "pay at a constant rate" (its own words) | releases a salary second by second; the worker takes what is earned so far |
| insurance | Nexus Mutual Insurance (76 million USD inside) | members put money in a common pot; claims are paid out by a vote of members |
| real-world asset | gold and fund tokens (Tokens lecture) | keeps the list of owners; the gold itself is kept by a company |
| bug bounty | 2 projects in the list | holds a reward that is paid automatically to whoever proves a bug |
| game | 29 projects in the list | items and characters as NFTs, so a player owns them outside the game company |

"Money inside" is DefiLlama's count, called **total value locked (TVL)**. The slide asks which of these would be useful
at INHA. *"Rules, money and a list: everything else is design."*

## Part 4: what can go wrong (pp. 24–25)

### Wrong 1: somebody goes first, the sandwich (p. 24)

**Front-running:** your transaction waits in public for some seconds before it enters a block. A **bot** (a program that
trades by itself) can see it and get **in front of it**. **Sandwich:** the bot buys just before you, so you buy at a
worse price, then it sells just after.

Our pool again: 10 ETH, 1,000 CLS, x · y = 10,000.

| Order in the block | Who | Transact | Result | Pool: ETH | Pool: CLS |
|---|---|---|---|---|---|
| | | the pool before | | 10 | 1,000 |
| 1 · front | Account 3, the bot | `buy`, Value 2 ETH | receives 166.667 CLS | 12 | 833.333 |
| 2 · victim | Account 2 | `buy`, Value 1 ETH | receives **64.103 CLS**, not 90.909 | 13 | 769.231 |
| 3 · back | Account 3, the bot | `sell(166.667 CLS)` | receives **2.315 ETH** for its 2 ETH | 10.685 | 935.897 |

**Worked by hand** (all ✓):
1. Bot: x = 12, y = 10,000 ÷ 12 = 833.333, so it gets 1,000 − 833.333 = 166.667 CLS (the 2 ETH row of p. 9).
2. Victim: x = 13, y = 10,000 ÷ 13 = 769.231, so it gets 833.333 − 769.231 = **64.103 CLS**. Alone, it would have got
   90.909.
3. Bot sells: y = 769.231 + 166.667 = 935.897, x = 10,000 ÷ 935.897 = 10.685, so it gets 13 − 10.685 = **2.315 ETH**.

*(my note: the bot made 0.315 ETH in one block; the victim got 26.806 CLS less, about 29% less. The pool still
multiplies to 10,000 at the end.)* **Nothing was hacked: three allowed calls, in a chosen order.**

**The defence: a minimum.** Send with your swap the **least you accept**. In the run, a minimum of **90 CLS** turned the
robbery into a failed transaction: "ClassPool: price moved". Websites call this setting **slippage**. *(my note: 90 out
of the expected 90.909 is a 1% slippage setting. The victim's swap fails instead of being robbed, and the bot is left
holding CLS it must sell back at no profit.)*

### Wrong 2: who can switch it off? (p. 25)

**"Decentralised" is not a yes or a no.** Ask it of each part separately. The contract may be unstoppable while the
website, the dollar inside it and the price it reads each have an owner.

| The part | Who runs it | Can it be stopped or changed? | Seen today |
|---|---|---|---|
| the website | one company or team | yes; the contract still answers, from Remix or Etherscan | OpenSea's website, Seaport's contract |
| the node behind the wallet | usually a company | it can refuse you; another node will answer | step 4 of using a dApp |
| the contract | nobody, or its admin | only if it has a pause, an owner or a proxy | pool number 1: none of the three |
| the tokens inside | their issuers | USDT can pause and freeze; USDC can replace its program | the Tokens and Security lectures |
| the price | the oracle's signers | they decide what "the price" is | a loan ended the second it changed |
| the order in a block | whoever assembles the block | they choose the order; they cannot break your minimum | the sandwich |
| the rules | token holders, by vote | a vote can change fees and rules | Uniswap's fee, December 2025 |

The slide asks which row could stop **you** from using a dApp tomorrow. *(my note: the website and the node can be
walked around, since the contract still answers through another door. A token issuer freezing your address, or a vote
changing the rules, cannot be walked around.)* *"Before you trust a dApp, walk down this column."*

## Part 5: your own dApp (pp. 26–27)

### Before you build: six questions for any dApp (p. 26)

A good project answers all six in one sentence each. **The last row is the one most ideas forget.**

| Question | ClassVote | ClassFund | ClassTicket |
|---|---|---|---|
| what lives in the contract? | the question, the counts, who voted | the goal, who gave how much | who owns which seat |
| what stays off the chain? | the discussion, the website | the plan for the money | the concert itself |
| who holds the money? | nobody: there is none | the contract, until the goal | the contract, for ever (the bug) |
| who pays the gas? | each voter | each giver, and the organiser | each buyer |
| who can stop or change it? | nobody | nobody | nobody, not even to take the money |
| what can the chain not prove? | that one address is one student | that the money is spent well | that the concert happens |

The slide asks which row is hardest for the ticket shop. *(my note: the last one. No contract can prove the concert
takes place.)* *"Code settles who may do what; people still settle whether it was worth doing."*

### Ideas you could build from today's bricks (p. 27)

Every idea is one of today's examples, changed a little for a real need at INHA. The project rules come separately.

| Idea | Built from | The hard part |
|---|---|---|
| a club vote, one address per member | ClassVote + a list of members | who may add members to the list |
| a fundraiser for a student event, with refunds | ClassFund | proving afterwards how the money was spent |
| event tickets that cannot be forged | ClassTicket + a collect function | checking ownership at the door |
| certificates of attendance or of a course | ClassTicket without a price | who may issue them, and stopping resale |
| a class coin and its market | ClassToken + a pool | why anyone would want the coin |
| a team wallet that needs two signatures | multisig, from the lecture on wallets | what happens if one member disappears |
| a safe deal between two students: pay now, release on delivery | ClassFund's pattern, two accounts | who decides when the two disagree |

*"A small dApp that solves one real problem beats a big one that solves none."*

**What you can do now** (p. 28): name the kind of any dApp, find its contract on Etherscan, say who can stop each part,
and sketch a contract of your own from today's three. The last question: which of today's examples surprised you most,
and why?

## Real events the deck uses

| When | What | Where in the deck |
|---|---|---|
| 2014 | Mt. Gox, a company exchange, loses its customers' coins | p. 3 |
| 2022 | FTX fails the same way | p. 3 |
| 5 May 2020 | Uniswap version 2's first pool (USDC/WETH) is created, block 10,008,355 | p. 8 |
| December 2025 | Uniswap's token holders vote that part of every swap's fee goes to the protocol | pp. 18, 25 |
| 25 Nov 2026 | three Aave liquidations while ETH fell from 1,625 to 1,607 dollars, one of them nearly 3 million USDT | p. 13 |
| (general) | DeFi platforms robbed with flash loans that bend a pool's price | p. 11 |

## Slide errors and loose claims

The AMM table (p. 9), the sandwich (p. 24), the loan limits, the liquidation price and percentages, the oracle 0.24%,
Lido's 0.15%, Uniswap's 4% quorum and the ClassFund run all check out. One rounding slip and three loose claims:

1. **p. 10, "10 × 1,692.94 = 16,929.35".** As written it multiplies to **16,929.40**. The 16,929.35 comes from Aave's
   unrounded price, 1,692.9352 (p. 12), × 10. Every later number (13,712.78, 14,220.66, 76.8%) uses 16,929.35, so only
   the displayed product is off by 5 cents.
2. **p. 9, "k is a magic number that must never change".** The same slide's other box says the product "must not get
   smaller", which is the correct rule. With a swap fee (real Uniswap version 2 keeps 0.3%), k grows a little with every
   swap *(my note)*. "Never changes" is only true for the fee-free classroom pool.
3. **p. 17, "No human can stop it, change it, or embezzle the funds".** Too strong, and the deck itself says otherwise on
   p. 25: a contract with an admin, pause or proxy can be stopped or changed, and a vote can change the rules. A
   majority of tokens can also vote the money to itself *(my note: in the Beanstalk attack of April 2022, an attacker
   borrowed enough voting tokens with a flash loan to pass their own proposal and drained about 182 million dollars)*.
4. **p. 21, "goal missed, money returned".** ClassFund has **no deadline** and nothing returns money by itself. If the
   goal is never reached, each giver must call `refund` themselves; whatever they don't claim stays locked for ever,
   because `collect` needs the goal. "Money can be taken back" is the accurate version.

*(my note, not counted as errors: p. 14 says behind each DAI "is locked crypto, not a bank account". That was the 2017
design. For years since, a large part of DAI's backing has been USDC, a company's dollar, plus tokenised government
debt, so the line describes the idea more than today's mix. Also, ClassFund's `collect` never sets `raised` to 0; this
is harmless here, since a second `collect` finds no ETH and fails with "payment failed".)*

Video: the matching lecture is on eClass as VOD 74308 (1:10:13), not mirrored or transcribed yet.
