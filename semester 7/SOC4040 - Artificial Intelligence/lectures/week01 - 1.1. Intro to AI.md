# 1.1 — Introduction to Artificial Intelligence

**SOC4040 · Week 1 · 48 slides · Dr. Oybek Eraliev**
Source: [week01 - 1.1. Intro to AI.pdf](week01%20-%201.1.%20Intro%20to%20AI.pdf)

---

## 🔴 Course admin — this deck overrides eClass

Slides 6–10 restate the course rules, and they **do not match the eClass
syllabus**. Treat the deck as authoritative; it's what he presented in class.

### Grading

| Item | Weight | Note |
|---|---|---|
| Attendance | 10% | **Medical certificates are not accepted.** 8+ absences = automatic F |
| Mid-term exam | 25% | Week 8 |
| Final exam | 25% | Week 15 |
| Homework assignments | 20% | **Two assignments, 10% each** |
| Term project | 20% | Week 14 (possibly 16) |
| **Extra points** | optional | up to **10 points** |

> **"Taking note — checking before mid exam and final exam."** He checks your
> notes before each exam. Whatever that's worth, it means **keeping a written
> notebook is an actual requirement**, not a suggestion. Cheapest marks in the
> course after attendance.

### Term project — the dates you need

- **Teams of 4–6 students.**
- An **end-to-end AI project**.
- **Week 5** (3–9 Oct): choose a topic. Free choice, but it **must not duplicate another team's**. Fields: computer vision, NLP, generative AI, etc.
- **Week 6** (10–16 Oct): submit a project proposal.
- Prepare a report.
- **Week 14** (5–11 Dec): presentation, possibly pushed to week 16.

Topic choice is in **three weeks** and is first-come on uniqueness, so forming
a team early is worth more than it looks.

### Contact

- **Office hours: Tuesday & Thursday, 14:00–15:30**
- Educational Assistant: Jasurbek Mamurov (also posted the Discord link)
- Email: `oybekeraliev7@gmail.com`

### His weekly plan (differs from eClass)

| Week | Deck | eClass syllabus |
|---|---|---|
| 1 | Introduction to AI | same |
| 2 | Core ML Algorithms | Intro to ML |
| 3 | ML for Classification | same |
| 4 | **ML for Clustering** | Non-parametric models (KNN, trees) |
| 5 | **Intro to Deep Learning** | SVM |
| 6 | **CNNs** | Unsupervised learning |
| 7 | **Advanced CV Models** | Deep Neural Networks |
| 8 | Mid-Term Exam | same |
| 9 | **NLP** | CNNs |
| 10 | **NLP with Transformers** | Object detection |
| 11 | **Generative Models** | Sequence models |
| 12 | **Reinforcement Learning** | Intro to NLP |
| 13 | **Deep RL** | Transformers & LLMs |
| 14 | Term project presentation | same |
| 15 | Final exam | same |

The deck's version is more compressed and pushes further (RL and deep RL are in;
SVM and object detection are out). **For exam prep, follow the deck.**

---

## Content

The lecture is organised in four parts: foundations, how machines learn, modern
systems, and responsible AI.

### Part 1 — Foundations

**What AI is.** He builds the definition from the two words — *artificial*
(made by humans rather than occurring naturally) and *intelligence* (the ability
to acquire and apply knowledge and skills) — then gives the working definition:

> **AI is the field of building systems that perform tasks normally requiring
> human intelligence.**

Four capabilities, each with an example — a likely exam question:

| Capability | Meaning | Example |
|---|---|---|
| **Perceive** | Interpret images, sound, text | Recognising a face in a photo |
| **Reason** | Draw conclusions, solve problems | Diagnosing a fault from symptoms |
| **Learn** | Improve from experience | A spam filter sharpening over time |
| **Act** | Take actions in the world | A self-driving car steering and braking |

**The six disciplines that make up most of AI:** natural language processing ·
knowledge representation · automated reasoning · machine learning · computer
vision and speech recognition · robotics.

**AI vs ML vs DL** — nested, and a classic exam question:

- **AI** — the broadest goal: systems that behave intelligently, *by any means*, including hand-coded rules.
- **Machine learning** — a subset: systems that learn patterns from data instead of following hand-written rules.
- **Deep learning** — a subset of ML: multi-layer neural networks learning increasingly abstract representations.

**Timeline — worth memorising, it's exam-shaped:**

| Year | Event |
|---|---|
| 1950 | Turing proposes the "Imitation Game" |
| 1956 | Dartmouth Workshop coins the term "Artificial Intelligence" |
| 1970s–80s | Two **AI winters** as funding and hype collapse |
| 1997 | Deep Blue defeats Kasparov at chess |
| 2012 | **AlexNet** ignites the deep learning boom |
| 2016 | AlphaGo defeats Lee Sedol at Go |
| 2022 | ChatGPT brings generative AI mainstream |

### Part 2 — How machines learn

**The ML pipeline**, five stages, and note it's a **loop** — production models
are monitored and retrained continuously:

1. Collect data → 2. Train a model → 3. Evaluate on unseen data → 4. Deploy & predict → 5. Monitor & retrain

**The three paradigms** — the core of this lecture:

| | Supervised | Unsupervised | Reinforcement |
|---|---|---|---|
| **Learns from** | Labelled examples — input paired with correct answer | Unlabelled data; no correct answer given | Rewards and penalties from acting in an environment |
| **Mechanism** | Learns the mapping from many (input, output) pairs | Groups or compresses data by similarity | Observe state → act → get reward → update strategy |
| **Examples** | Spam detection · house price prediction · diagnosis from X-rays | Customer segmentation · anomaly detection · topic discovery | Game agents (AlphaGo, Atari) · robot walking/grasping · data-centre cooling |

**Why deep learning took off when it did** — three things converging around
2012, given the theory dates from the 1980s:

1. **Data** — an explosion of digital images, text and sensor data
2. **Compute** — GPUs and TPUs making large networks practical
3. **Algorithms** — better architectures (CNNs, transformers) and training techniques

### Part 3 — Modern systems & applications

**Computer vision** — interpreting images and video. Applications: facial
recognition, medical imaging (tumours, fractures), self-driving perception
(pedestrians, lanes, signs), manufacturing quality inspection.

**NLP** — understanding, interpreting and generating human language.
Applications: machine translation, sentiment analysis, voice assistants,
chatbots.

**Generative AI and LLMs** — creating new content (text, images, audio, code)
rather than just classifying. Applications: text generation, image generation
via diffusion, code generation, summarisation.

**How LLMs work, in four steps:**

1. **Tokenize** — text is broken into tokens, the word-pieces the model processes
2. **Predict the next token** — trained to predict what follows, given everything before
3. **Learn from scale** — grammar, facts and patterns emerge from enormous corpora
4. **Generate** — produce text one token at a time, sampling from predicted probabilities

> **The caveat he flags explicitly:** LLMs predict *plausible* text — they don't
> "know" facts the way a database does. That's why they state falsehoods
> confidently. The failure mode is called **hallucination**. Expect this on an exam.

**State of the art — concrete examples he cites:** Waymo passing 10 million
public-road miles by 2018 with human takeover only about once every 6,000 miles ·
Atlas walking uneven terrain, jumping onto boxes and doing backflips ·
route planning at scale by ride-hailing and mapping services · machine
translation covering 100+ languages, reaching the native languages of over 99%
of people · speech assistants including Google Duplex making phone
reservations · recommendation systems at Amazon, Netflix, Spotify, YouTube ·
medical diagnosis matching or exceeding expert doctors on image-based
conditions (Alzheimer's, metastatic cancer, ophthalmic and skin disease) ·
and a local example, **wakil.ai** by HumblebeeAI, in law.

He also notes the hardware question — CPU, GPU, TPU, quantum computing — as a
computer-engineering foundation of AI.

### Part 4 — Responsible AI & the future

**Four limitations of today's AI** — clean list, very exam-shaped:

1. **Hallucination** — confident, fluent, false statements
2. **Lack of true understanding** — pattern matching, not comprehension or reasoning
3. **Brittleness** — small unexpected input changes cause large errors
4. **Data dependency** — models inherit the biases, gaps and blind spots of their training data

**Bias and fairness.** AI can learn and *amplify* unfair patterns already in the
data. His two cases: facial recognition historically showing higher error rates
for women and people with darker skin, driven by underrepresentation in training
sets; and hiring tools trained on historical CVs downgrading candidates on
gender-correlated signals. **The takeaway:** fairness needs diverse data,
testing across subgroups, and continued auditing after deployment.

**Trends to watch:** multimodal AI (text + image + audio + video in one system) ·
autonomous agents planning and executing multi-step tasks · smaller efficient
models running locally on devices · growing regulation such as the EU AI Act.

**Careers:** ML engineer · data scientist · AI/ML researcher · AI ethicist or
policy analyst · AI product and prompt roles. Skills he names: Python,
statistics and linear algebra, and critical thinking about when to apply AI at all.

### His five key takeaways

1. AI is the broad goal; ML and DL are the tools used to reach it today.
2. Machines learn through supervised, unsupervised and reinforcement paradigms.
3. Transformers plus large-scale data and compute unlocked the generative AI boom.
4. AI creates enormous value — and real risks around bias, privacy and misuse.
5. Responsible use means understanding both what AI can do and where it falls short.

---

## If you're revising this in 10 minutes

Know the **AI/ML/DL nesting**, the **three learning paradigms with one example
each**, the **four capabilities** (perceive/reason/learn/act), the **five-stage
pipeline**, the **four limitations**, and the **timeline dates** (1950, 1956,
1997, 2012, 2016, 2022). That's the examinable skeleton; everything else is
illustration.
