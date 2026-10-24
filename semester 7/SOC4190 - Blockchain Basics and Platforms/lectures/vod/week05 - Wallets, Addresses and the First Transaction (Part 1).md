# Wallets, Addresses and the First Transaction (Part 1)

**Blockchain · Week 5 · 55:56 · Jalolliddin Yusupov**
Transcript: [txt](week05%20-%20Wallets,%20Addresses%20and%20the%20First%20Transaction%20(Part%201).txt) · Subtitles: [srt](week05%20-%20Wallets,%20Addresses%20and%20the%20First%20Transaction%20(Part%201).srt)
Slides: view-only on eClass (module 72103)

This is the **wallet onboarding** the syllabus promised for week 3. Part 2 is the hands-on MetaMask demo,
so **have your laptop ready** for it [52:55]. He asks you to **pause and use pen and paper**.

Prerequisites he won't repeat: private vs public key, SHA-256 and hash functions, transactions, block explorers, nodes (week 4).

---

## 🥚 Hidden messages and small print

- **No explicit easter egg** in this part. The only pause-and-think question [22:30] is *why do addresses derived from
  private key = 1 always have a zero balance?* He answers it straight away (section 4).
- **Small facts he mentions once**, the kind he says hard quiz questions use:
  - a private key is **256 bits = 64 hex characters**. There are about **10⁷⁷** possible keys
  - a public key is **33 bytes** in Bitcoin's (compressed) form: 32 bytes plus one prefix byte for *y*. He also says 64 bytes (x‖y) when hashing for Ethereum
  - Ethereum address = **last 20 bytes of Keccak-256(64-byte public key)**, written as `0x` + 40 hex = **42 characters**
  - the seed-phrase list has **2048 words** (2¹¹). **12 words** for MetaMask, **24** for his Trezor. **The last word is partly a checksum** over the others
- **At the end [53:10]**: he can see view counts on eClass. Only **about 30 people watched the Cryptography video**. At the
  project defence he will ask questions, and if you can't answer, you're likely to fail. He also mentions **a bug in the quiz**:
  if it was his mistake, grades update automatically and you don't need to do anything.

## 1. What a private key is [02:50]

- **A random number** your computer picks, like **256 coin tosses**. Written as **64 hex characters** (0–9, a–f).
- Nobody issues or registers it. **You must save it**, since no one can memorise it.
- **Guessing is "almost impossible"**: even if all 8 billion people each guessed a billion keys per second since the
  Big Bang, they wouldn't have tried a meaningful fraction of the **≈10⁷⁷** keys [06:40].

## 2. Private key → public key: elliptic curves [08:50]

- `public key = k × G`, meaning the generator point **G added to itself k times** on an **elliptic curve** (two points add to give a third), with shortcuts that make it fast.
- **Forward is easy. Backward (finding k) is infeasible.** It's *not* ordinary multiplication, so you can't just divide.
- The curve maths is not examinable here ("there's a 1-minute video if you want").

## 3. Public key → address [12:25]

- An **address is the fingerprint (hash) of the public key**: your public ID on the chain, where people send money.
- **Ethereum**: take the 64-byte public key (x, y) → **Keccak-256** (SHA-256's "cousin", with the same five
  hash-function properties) → 32-byte hash → **keep only the last 20 bytes** → prefix `0x`.
- **Deterministic**: the same key gives the same address on every computer. Change one bit and everything changes.
- It **can't be reversed** into the public or private key.
- ⚠️ **Read the whole address.** Apps show only the first and last few characters, and an attacker can craft an address
  with the same ends but a different middle [16:30].
- **Bitcoin addresses** look different (`1…`, `3…`, `bc1…`). The old format drops look-alike characters (**0, O, I, l**). Newer
  formats use **all lowercase**, and wallets can detect typos and altered addresses [19:00].
- There's no address registry. Collisions are possible in theory, but the odds are negligible.

## 4. Why key = 1 is a disaster [21:30]

- k = 1 is a *valid* key with a real Bitcoin and Ethereum address. People have sent money there (**199 transactions**), and the **balance is always 0**.
- **Why**: everyone can compute the key for "1", so bots watch the address day and night and **sweep anything that arrives**.
- **Lesson**: the key must come from **real randomness**, never from you (birthday, a book quote, "clever" numbers). *A key anyone can guess is a key everyone owns.*

## 5. What a wallet is [25:15]

- An **app or hardware device** (his is a **Trezor**) that **generates and stores the private key, shows your address and balance, and signs transactions** when you press Send.
- 🔴 **The wallet holds keys, not coins.** Coins are just **entries in the ledger** on thousands of nodes. *"Aziz sent 100 BTC to Botir"* is a row in the ledger, not something in a pocket.
- **Delete the app or burn the device and the money is not gone**, as long as you still have the key.
- Spending works by proving you hold the key: you sign, nodes verify against your public key and address, and the new transfer is written to the ledger.
- Wallet types: the **Telegram wallet** (recently rebranded, fine for small amounts, "some conspiracies behind it"), **MetaMask** (used in this course), and hardware wallets (the safest, covered in a later lecture).

## 6. The seed phrase [33:00]

- **12 ordinary English words** from a fixed list of **2048**. The wallet turns them into **every private key it will ever use**.
  MetaMask calls it the **Secret Recovery Phrase**.
- **Lose the device, keep the words, and you lose nothing**: reinstall and restore. People in the news who "lost Bitcoin on a hard disk" really lost
  their **seed words**.
- **Brute force**: 2048¹² ≈ 2¹³² phrases. At a billion guesses a second that's still astronomically long.
- **One seed, many accounts** [39:40]: account 1, 2, 3… are derived by counting from the same seed. **One backup covers them all.**
- ⚠️ **Published phrases are owned by everyone**: `test test … test junk` (a Hardhat/Foundry default) and `abandon abandon … about` (the BIP-39 example). One
  of these accounts has **11,000+ transactions and a zero balance** [49:40]. **Never use words you've seen anywhere.**

### Rules for your 12 words [42:56]

1. Write them **on paper, in order, numbered 1–12**, and check twice.
2. **Keep the paper at home.**
3. **Never photograph them**: cloud sync (iCloud, Google Photos), and photos can be recovered from a phone after a reset and resale.
4. Never put them in the cloud, notes or a screenshot folder, and never type them into a website.
5. **Nobody needs them**: not MetaMask, not the TA, not the professor, not your teammates. **Whoever asks is a thief.** To receive coins, people need only your **address**.
6. The course uses test coins, so a leak costs nothing, but **practise the habit now**.

### Password vs seed phrase [45:40]

| | **Password** | **Seed phrase** |
|---|---|---|
| Protects | the app on *this* computer, from someone sitting at it | the **wallet itself**: every key and address |
| Forgotten? | reinstall and restore with the 12 words. **Nothing lost** | **everything lost forever** |
| Stolen? | useless without your computer | **they own your whole wallet** |
| Changeable? | any time | **never**. A different phrase means different addresses |

> *"The password locks the door to your house. The seed phrase is your house."*

## Things that are loose in the lecture

- He calls Bitcoin's old address alphabet **"base 56"**. It's **Base58**: Base64 minus `0 O I l + /`.
- "Keccak-256 is much safer than SHA-256" isn't established. They're different designs (Keccak is the sponge
  construction behind SHA-3), and both are considered secure.
- At [28:37] he says *"wallet does not store the key"*. That's a slip: the rest of the lecture (and his slide) says the wallet **stores the key, not the coins**.
