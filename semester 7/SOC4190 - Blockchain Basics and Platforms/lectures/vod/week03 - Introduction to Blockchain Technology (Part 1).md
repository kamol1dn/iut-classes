# Intro to Blockchain Technology, Part 1: Ledgers, Trust and Double-Spending

**Blockchain · Week 3 · 44:14 · Dr. Jalolliddin Yusupov**
eClass: [VOD 71402](https://eclass.inha.ac.kr/mod/vod/view.php?id=71402) · slides are view-only ([71403](https://eclass.inha.ac.kr/mod/ubfile/view.php?id=71403))
Transcript: [.txt](week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%201).txt) · Subtitles: [.srt](week03%20-%20Introduction%20to%20Blockchain%20Technology%20(Part%201).srt)

The first ~16 minutes are about him and how the course runs. The lecture proper
starts at **[16:23]**.

---

## 🟡 How the course runs, as he explained it

This is more concrete than the syllabus in places.

- **Weekly rhythm:**
  - **Friday:** the week's module opens on eClass, with **two ~40-minute recordings** plus the slides.
  - **Saturday 10:00–11:00:** online office hours. "This one is fixed." The link will be shared, via Zoom or maybe a Telegram stream. With 300 students, people may be taken one at a time.
  - **Sunday:** a quiz opens, and it **closes the following Sunday**. "Deadlines are always on Sundays."
- **The eClass clock is the only clock that counts.** Deadlines are strict. He
  runs eClass for about 10 other universities through his own company, so
  expect the platform's features to be used fully, including a live gradebook.
- **Being behind is being handled.** The course started about two weeks late, and he'll run
  **make-up classes**, with extra videos during the midterm period. He repeated that there
  is **no exam**.
- **Grading, restated:**

  | Item | Weight |
  |---|---|
  | Attendance | 10% |
  | Quizzes | 15% |
  | Home assignments | 25% |
  | Term Project I | 25% |
  | Term Project II | 25% |

  - Attendance is computed from the weekly quizzes: **do the quiz, get the attendance point.** "Please don't skip the quizzes."
  - Home assignments are practical work on a **test network** plus **handwritten parts**, scanned and uploaded to eClass.
  - Term Project I is individual and replaces the midterm. Term Project II is a team project.
- **How to contact him:**
  - **Don't email.** "I really don't like emails." Send an **eClass message**, or come to office hours.
  - Put questions about course content on the **Q&A board** ([70115](https://eclass.inha.ac.kr/mod/ubboard/view.php?id=70115)), so everyone can see the answer.
  - The syllabus PDF also lists an email address. In practice, eClass is preferred.
- **Definition cards.** Every new term gets a definition "card" on the slides.
  "Your job is to remember them," and the quizzes will test them.
- **The slides change every year** because the field moves fast. He'll announce any
  mid-term changes.

He also offered to talk in office hours about master's and PhD paths and
recommendation letters.

---

## 1. The friends' notebook — what a ledger is

Five friends in Tashkent keep lending each other money: Aziz → Elnoza, Elnoza
→ Begzod 30,000, Begzod → Aziz 20,000. After a month nobody remembers, so they
start writing it down in a notebook.

| Term (a "card") | Definition |
|---|---|
| **Ledger** | An **ordered list of records of who gave what to whom**, one line after another. Examples: the friends' notebook, a bank's payment list, a shop's sales book, a university's tuition list. "A ledger is just memory." |
| **Record** | One row in the ledger's table. |
| **Transaction** | **One record in a ledger: one transfer of value from one person to another.** |
| **Balance** | **How much someone has now, found by going through all their transactions.** It's computed from the history, not stored as a separate secret number. It's what Click or Payme shows you. |

**Key point:** anyone holding the ledger can compute anyone's balance.

## 2. Who holds the notebook? — trust

There's one notebook, and **Timur keeps it in his bag**. Four things can go wrong:

1. Timur **quietly adds** "Aziz gave Timur 40,000".
2. Timur **loses the bag**.
3. Timur **refuses to show** it to someone, e.g. Malika.
4. Two friends **disagree about what a line says**: "I never got that 40,000."

**Whoever holds the only ledger has power over everyone in it.** Everyone
else just hopes the holder is honest and careful.

> **Trust:** believing someone will act honestly **even when you cannot check
> what they do**. You trust a bus driver to drive safely, and a bank to record your salary
> correctly. You don't audit the bank's ledger.

### The two choices, which frame the whole course

| | |
|---|---|
| **Choice A** | Pick **one party everyone trusts** to keep the ledger. |
| **Choice B** | Make the ledger **checkable by everyone**, so **no one needs to be trusted**. |

He said the arc of the course is to start with trust and end with **"don't trust"**, i.e.
choice B.

## 3. Choice A today — banks as intermediaries

When you send 50,000 via Click or Payme, **no banknote moves**. The bank's
**database, which is its ledger,** changes two lines: your balance goes down and
the recipient's goes up. **Your money is a line in the bank's ledger.**

> **Intermediary** (middleman): someone in the middle who **keeps the ledger for
> everybody and makes the transfers happen**. Banks, Click, Payme, card companies.

**Why intermediaries exist.** They do real work:
- keep the ledger safe and backed up
- check who you are
- put payments in order
- stop you spending money you don't have
- fix mistakes and handle complaints

Result: nothing is lost, nobody else can spend your money, balances stay correct,
and there's someone to call.

**What intermediaries cost:**

| Cost | His example |
|---|---|
| **Fees** | Low in Uzbekistan's fintech. "Crazy" in Italy, the US and Japan, especially cross-border. |
| **Timing** | Banks close on weekends and holidays. You can't wire $10,000 to the US on a Saturday. |
| **Permission** | They can refuse you or **freeze your account**, by accident or on purpose. |
| **Privacy** | They see everything you do. |
| **Single point of failure** | If the bank, backups included, goes offline, gets hacked or fails, **everyone stops at once**. He said this phrase will recur throughout the course. |

Until Satoshi Nakamoto there was no real alternative, so the costs were worth paying.

## 4. When the intermediary fails — Lehman Brothers, 2008

- **Lehman Brothers**, founded **1850**, one of the largest US banks, went
  **bankrupt on 15 September 2008**. That's a 158-year-old record keeper that everyone trusted.
- Fear spread through the whole financial system. Governments **bailed out**
  other banks with public money to stop a chain of failures. He'll explain the
  contagion later.
- **Lesson:** even the biggest intermediaries can fail, and in a single weekend.
- After 2008 people began asking: **can we keep records without trusting one
  company?**

> He says "2018" at one point [30:39]; it's **2008**, as he says correctly right after.

## 5. Digital money and the double-spending problem

**Digital money:** money that exists **only as a record in a computer**, a line in
a ledger, not paper or metal. Most payments today are already like this, e.g.
metro and supermarket payments, and in China many places accept only app payments.

**The danger: data can be copied for free.** You can send a photo to 100 friends and still
have it. Now suppose a coin is just a file, `coin #001`, owned by whoever has
the file. You send it to **shop A** and to **shop B**, and both see a valid coin. Paper
cash can't do that. The banknote in shop A's drawer isn't also in shop B's.

> **Double spending:** spending the **same digital money twice** by sending it
> to two people at almost the same moment. **The biggest problem digital money
> must solve.**

**How a bank solves it.** Every payment goes through **one ledger**. At time `t`
the bank checks your balance and accepts the payment, and your balance hits zero. The second attempt
is checked again and **refused**. It works because **one keeper sees everything and
puts every payment in order**. So for years, safe digital money **required a
middleman to decide the order**.

## 6. The cliffhanger — three questions without a middleman

Can a group of **strangers anywhere in the world** share digital money with
**no one in the middle**? Then you must answer, all at once:

1. **Who keeps the ledger?** If nobody owns it, where does it live?
2. **Who decides the order** of transactions? Otherwise double spending returns.
3. **Who stops cheating**, e.g. someone rewriting the past?

These are answered in Part 2.

---

## Cards to memorise (quiz material)

- [ ] Ledger · record · transaction · balance
- [ ] Trust, and the four notebook failure modes
- [ ] Choice A vs Choice B
- [ ] Intermediary: what it does, and its five costs
- [ ] Single point of failure
- [ ] Lehman Brothers (founded 1850, bankrupt 15 Sep 2008) and bail-out
- [ ] Digital money · double spending · how a bank prevents it
- [ ] The three questions a middleman-free system must answer
