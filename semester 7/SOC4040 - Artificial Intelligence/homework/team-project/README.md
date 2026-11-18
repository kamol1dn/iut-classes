# Team Project: an end-to-end AI application

**Artificial Intelligence · Team project (20% of the course) · presentation + live demo, graded out of 100**

- Guidelines: [Team-Project-Guidelines_IUT-AI-Fall-2026_final-version.pdf](Team-Project-Guidelines_IUT-AI-Fall-2026_final-version.pdf)
  (6 pages), posted on eClass as [assignment 73304](https://eclass.inha.ac.kr/mod/assign/view.php?id=73304) in the
  week-10 section. The eClass page says the guidelines were written with AI (claude.ai).
- Professor: Dr. Oybek Eraliev. Education Assistant (EA): Jasurbek Mamurov.
- **Follow the course Discord for all announcements, templates and deadlines.** That's the PDF's closing line.
  The invite link is in the [course README](../../README.md).

## Deadlines

**The guidelines PDF gives no dates at all.** Every deadline below is **announced on Discord**.

| Deliverable | Where | When |
|---|---|---|
| Project brief | your team's **private space** on the course Discord server. The PDF says to check regularly whether it has been created for your team | announced on Discord |
| Code | **GitHub** (a GitHub Organization). "Repository details will be shared later" | announced on Discord |
| Project report (PDF) | **eClass**, in a submission slot announced later | announced on Discord |
| Presentation + live demo | **in person**, to the course team, with the demo running on **your own laptop** | announced on Discord |

The lecture slides gave earlier week numbers. 10.1 slide 70 (week 10) says: "Choose a project topic (free topic,
should be not the same with other teams), (Week 9)" and "Make a project proposal (Week 10)". The week-1 deck had
week 5 for the topic, week 6 for the proposal and week 14 (possibly 16) for the presentation. The topic and
proposal weeks have already passed. The presentation week is still ahead but unconfirmed, and the guidelines PDF
repeats none of these, so go by Discord.

## Team size

**The guidelines PDF doesn't say.** 10.1 slide 70 says "Make a team (4~6 students in a team)", and the week-1
deck's grading table says teams of 4–6. Topics must not duplicate another team's (slide 70), so the first team to
claim a topic gets it.

## What's required

**Topic:** open. Any project that uses AI to solve a **real problem**, which your team understands, cares about
and can realistically build.

**End to end:** data → a trained model → a working application that someone can actually use.

What they expect, from the PDF's table:

| Area | Expected |
|---|---|
| Dataset | Collected or created by the team |
| Cleaning & preparation | A full pipeline built by the team: cleaning, labelling and formatting the data for your own model |
| Model | Designed, built and trained **from scratch** by the team |
| Evaluation | Several experiments, compared and explained |
| Deployment | The model served through a user interface the team built: web, app or Telegram bot |

An existing dataset or model is **allowed**, but own data and a from-scratch model **earn more credit**. Keep
reuse to a minimum, and **state every piece of it**.

**Signs of effort they look for:**
- Data the team collected, labelled or significantly extended
- Documented cleaning and preprocessing, with **before-and-after examples**
- Model code written and trained by the team, not only called from a library
- Several approaches tried and compared, with the best chosen for a clear reason
- A working application with a user interface that shows the model in action
- A **GitHub history that shows steady work from every team member**
- Honest disclosure of every reused dataset, model, piece of code or tool

### Experiments and model selection

The final model should come out of a **comparison**, not be the first thing that worked. Things to compare:
- **Models**: a simple baseline against two or three stronger approaches
- **Settings**: hyperparameters such as learning rate, number of layers, tree depth
- **Data preparation**: different cleaning, feature or augmentation choices
- **Data versions**: e.g. results before and after adding the data you collected

Keep a simple log while you work and show the key rows as a table. Use **the same metric and the same test data
in every row**, so the comparison is fair. The PDF's example (format only):

| # | Approach | What changed | Accuracy | Selected |
|---|---|---|---|---|
| 1 | Baseline (most frequent class) | — | 0.41 | |
| 2 | Logistic regression | Basic cleaning | 0.68 | |
| 3 | Neural network (own) | 2 hidden layers | 0.74 | |
| 4 | Neural network (own) | 3 layers + collected data | 0.81 | ✔ |

Be ready to answer **"why this one?"**: name the result that decided it and any trade-off you accepted (speed,
model size).

### Deployment: the minimum

- **Deployed locally**, on your own laptop, and run there during the presentation. Online hosting is not required.
- **Has a user interface**: a simple website, a desktop or mobile app, or a Telegram bot.
- **Works live**: a user gives input (text, image, numbers…) and the model answers in real time.
- **Uses your trained model**: save it after training and load it in the app. **Do not retrain during the demo.**
- **Can be run by others**: a few lines in the GitHub README on how to install and start the demo.

Test the demo on the presentation laptop **before** the day. Keep a short screen recording as a backup, but it
does **not** replace the live demo.

For a PyTorch model, saving and loading is a few lines:

```python
torch.save(model.state_dict(), "model.pt")        # after training
model = MyModel(); model.load_state_dict(torch.load("model.pt")); model.eval()   # in the app
```

### Submission contents

- **Project brief**: written in your team's private Discord space.
- **Code (GitHub)**: training code, the **source of the deployed demo app** (required), and a short README on how to
  run it. Upload source code; no installer needed.
- **Report**: on eClass. 10.1 slide 70 lists its contents: the role of each team member and their contribution,
  objective, definition, block diagrams of the application, and a demo video shown during the presentation.
  The guidelines PDF says nothing about the report's contents.
- **Presentation + live demo**: in person.

## Presentation structure (follow it)

Effort should show throughout, especially in Methodology, Experiments and the Live Demo.

| Slide | Content |
|---|---|
| 1. Title | project title; team members and student IDs; one-sentence problem summary |
| 2. Problem definition | what problem, why it matters, how it connects to AI. Keep it short |
| 3. Proposed solution | what the project is, what it does, what makes the approach useful |
| 4. Methodology | tools, models, libraries, datasets; key AI techniques; one architecture/workflow diagram; **mark clearly what you built and what you reused** |
| 5. Challenges | 2–3 major issues, how you solved them, what you learned |
| 6. Experiments & results | where the data came from and how you collected, cleaned and prepared it; metrics; the **comparison table** and why the final model won; main results. Key numbers only |
| 7. Live demo | switch to the running app; real input, live output; how the model connects to the interface |
| 8. Conclusion | what you achieved, why it matters, a one-sentence takeaway |

Title slide format: `<Project title>` · `<Full name> (<StudentID>)` for each member · one-sentence summary.

## Grading (out of 100)

"Your presentation is your evidence": they grade by listening and asking questions. **If you don't tell them
about your effort, they can't give you credit for it.**

| Criterion | Max | What they look at |
|---|---|---|
| Problem Definition and Relevance | 10 | a clear problem statement; relevance to AI; why the problem matters; a scope the team can actually build |
| Methodology and Implementation | 25 | a clear, appropriate method; AI techniques applied; **how much of the model and pipeline the team built** (from scratch valued most); evidence that alternatives were tried; complete and correct; a clear split between built and reused |
| Dataset, Experimental Design and Results | 25 | how the data was obtained (**collected or created by the team valued most**); cleaning, labelling and preparation; suitable metrics and experiments; analysis of results; comparisons made and a clear reason for the final choice |
| Deployment and Live Demo | 10 | runs locally and works live; a UI for input and output; loaded from saved files, not retrained; a README explaining how to install and run; usability and stability, including sensible handling of unexpected input |
| Creativity and Critical Thinking | 10 | originality; how you dealt with challenges and limitations; future improvements or applications |
| Q&A, **individual** | 20 | **4 questions to each member**, scored individually: about the project **and the AI course**; each member explains their own part; justifying the team's decisions |
| **Total** | **100** | |

Only the Q&A is stated as individual: those 20 points are **per person**. The questions can cover the course
material too, so revise the lectures.

## What costs points

The PDF lists **no fixed deductions**. What it does say:
- **Presenting reused work as your own "will be treated seriously."** Reuse is fine only when you say so. Keep
  a list of every reused dataset, model, code snippet and tool from day one.
- **Reuse earns less.** Existing datasets, pretrained models, or a model that is only a library call score below
  your own data and from-scratch code (criteria 2 and 3).
- **Only one model**, with no baseline and no comparison, loses the experiments part of criteria 2 and 3.
- **Unfair comparisons**: rows with different metrics or different test data.
- **No live demo, or retraining during it.** A screen recording is only a backup. No README on how to run it
  also costs points under criterion 4, as does an interface that breaks on unexpected input.
- **Effort you don't mention** in the presentation isn't credited.
- **A member who can't explain their part** loses their own Q&A points. The PDF also notes that "preparing
  presentation slides is not that much of considerable effort", so don't make slides someone's whole job.
- **Uneven GitHub history**: they look for steady commits from **every** member.
- **Duplicate topic**: slide 70 says topics must not be the same as another team's.

## IUT AI Laboratory

Teams may use the lab's resources (section 08 of the PDF).
- **Request access early** through the EA, and read the lab's essential documents (the link is in section 08 of
  the PDF).
- Resources are shared and scheduled in order of request and availability. Late requests may not be met in time.

## Course material that helps

- [3.1 Evaluation](../../lectures/summaries/week03%20-%203.1.%20Evaluating%20Learning%20Algorithms.md): metrics for the comparison table
- [5.2 Data preparation](../../lectures/summaries/week05%20-%205.2.%20Data%20preparation%20for%20ML%20models.md): cleaning, encoding, scaling, leakage
- [7.1 DNN](../../lectures/summaries/week07%20-%207.1.%20Deep%20Learning%20(DNN).md) and [Neural_Network.ipynb](../../resources/Neural_Network.ipynb): a network written by hand
- [9.1 CNN](../../lectures/summaries/week09%20-%209.1.%20Deep%20Learning%20(CNN).md), [9.2 Lightweight CNN](../../lectures/summaries/week09%20-%209.2.%20Lightweight%20CNN.md) and [CNN.ipynb](../../resources/CNN.ipynb): a PyTorch training loop for image models
- [10.1 Object detection](../../lectures/summaries/week10%20-%2010.1.%20Object%20Detection.md) and [object_detection.ipynb](../../resources/object_detection.ipynb): fine-tuning YOLO (counts as reuse)
- [HW1](../hw1-kaggle/README.md): a baseline-then-compare workflow with cross-validation

## Checklist

- [ ] Team of 4–6 formed; Discord nicknames set to "Full name, Student ID"
- [ ] Check Discord for your team's private space; write the **project brief** there
- [ ] Topic: a real problem solved with AI, realistic scope, not taken by another team
- [ ] Data collected, created or extended by the team; source written down
- [ ] Cleaning/labelling pipeline, with before-and-after examples
- [ ] Baseline + 2–3 approaches, logged; one comparison table with the same metric and test set
- [ ] Final model written and trained by the team; reason for choosing it; saved to a file
- [ ] App with a UI (web, app or Telegram bot) that loads the saved model and handles bad input
- [ ] GitHub repo (once details are shared): training code, app source, README with install/run steps, commits from every member
- [ ] Reuse list: every dataset, model, code snippet and tool that isn't yours
- [ ] Report PDF on eClass when the slot opens: roles and contributions, objective, definition, block diagram
- [ ] 8-slide presentation in the required order; title slide with `<Full name> (<StudentID>)` for each member
- [ ] Demo rehearsed on the presentation laptop; backup screen recording
- [ ] Every member can explain their own part, and has revised the course for the 4 Q&A questions
- [ ] Lab access requested early through the EA, if needed
