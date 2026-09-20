# SOC4180 — Deep Learning for Computer Vision

> Official syllabus, 2026 Fall Semester. Mirrored from eClass on 2026-09-20.
> Source: `https://eclass.inha.ac.kr/local/ubion/setting/syllabus.php?id=2634`
> Original PDF: [soc4180.pdf](soc4180.pdf)

| | |
|---|---|
| **Course No.** | SOC4180 — Class 001 |
| **Semester** | 2026 Fall (202602) |
| **Instructor** | Jeong Hong |
| **Room** | B-101 |
| **Schedule** | Mon `14~16` · Thu `9~11` (as registered — see note below) |
| **Credits** | 3.0 |
| **Grading** | Relative evaluation |
| **Mode** | Offline |

## Grading breakdown

| Mid-term | Final | Attendance | Assignments | Quiz | Discussion | Etc. |
|---|---|---|---|---|---|---|
| 30% | 30% | 5% | 30% | 0% | 0% | 5% |

## ⚠️ Note: the official syllabus is internally inconsistent

The **objectives / description** sections describe a *robotics and robot learning*
course built around the MuJoCo simulator and the Unitree G1 humanoid. The
**weekly plan** below describes a *deep learning fundamentals* course
(neurons → transformers → generative models → agents). Both are reproduced
verbatim. Confirm with Prof. Jeong Hong which one the course actually follows —
the lecture slides at `gnoejh.github.io/soc4180` are the best live signal.

## Course objectives *(as registered)*

Introduces robotics and robot learning from first principles, from the basic
anatomy of a robot to autonomous locomotion policies. Students build, control
and analyze a full-scale humanoid — the Unitree G1 — entirely within the MuJoCo
physics simulator: reading a robot model, computing kinematics, designing
controllers, and ultimately training policies that replace those controllers.

*First half (classical):* rigid-body transforms and coordinate frames, forward
and inverse kinematics, contact and ground reaction, support polygon and Zero
Moment Point criterion, and the Linear Inverted Pendulum Model. By week 4
students make a 29-DOF humanoid walk using only geometry, a linear differential
equation and inverse kinematics — no learning at all. Actuation, PD control,
oscillator-based gaits and state estimation complete the classical foundation.

*Second half (learning):* locomotion as a Markov decision process, policy
gradients and PPO, reward shaping and its failure modes, and training locomotion
policies with GPU-parallel simulation. Domain randomization, robustness
evaluation and the sim-to-real gap are treated directly; vision-based perception
and imitation learning extend the work toward current practice.

Conducted **entirely in simulation — no physical hardware required**. Each week
pairs a structured lecture with a lab notebook that runs in Google Colab with
zero installation.

## Course description *(as registered)*

**Core components** — the five-layer robot stack (physics, model, middleware,
control, autonomy); robot description formats (MJCF, URDF) and the body tree as
a kinematic chain; degrees of freedom, floating-base systems, actuators and
sensors; control timescales from 500 Hz physics to sub-hertz task decisions.

**Kinematics and geometry** — rigid-body transforms, rotation matrices,
quaternions, axis-angle; forward kinematics validated against a physics engine;
Jacobians and differential kinematics; inverse kinematics (closed-form and
damped least squares); singularities, joint limits, workspace analysis.

**Dynamics, contact and balance** — contact modeling, friction, ground reaction
forces; center of mass, center of pressure, support polygon; Zero Moment Point
criterion; underactuation.

**Classical control and analytic locomotion** — PD and position control, gain
tuning, torque saturation; Linear Inverted Pendulum Model and its closed-form
solution; footstep planning and boundary value problems; swing-foot trajectories
and double-support phases; central pattern generators.

**Sensing and state estimation** — gyroscopes, accelerometers, gravity as a tilt
reference; complementary filtering; observation design.

**Reinforcement learning** — MDPs, policies, value functions, returns; policy
gradients, actor-critic, PPO; Gymnasium API and residual action
parameterization; reward shaping, reward hacking, diagnosing failed runs;
GPU-parallel simulation.

**Robustness and sim-to-real** — domain randomization over mass, friction and
actuation; actuator lag, latency, backlash, sensor noise; quantifying the
reality gap; policy export and onboard deployment.

**Perception and imitation** — rendering RGB and depth from onboard cameras;
terrain-aware locomotion and height maps; motion tracking and imitation.

**Tools** — MuJoCo and MuJoCo Menagerie; Unitree G1; Gymnasium, PyTorch,
Stable-Baselines3, JAX/MJX; pinned, reproducible Colab environments.

## Weekly plan *(as registered)*

| Week | Theme | Details |
|---|---|---|
| 1 | Artificial Neurons | Neurons, activation functions (ReLU, GELU), weight initialization (Xavier, He) |
| 2 | Optimization & Loss | Loss functions (MSE, cross-entropy), gradient descent variants, backpropagation |
| 3 | Neural Components | Softmax, residual connections, dropout, normalization (BatchNorm, LayerNorm) |
| 4 | Embedding & Representation | Tokenization, word embeddings (Word2Vec, GloVe), dense vector spaces, semantic encoding |
| 5 | Positional Encoding & Attention | Positional encoding (sinusoidal, learned), scaled dot-product attention, multi-head attention |
| 6 | Reinforcement Learning | MDPs, policy gradients, Q-learning, RL in agentic systems |
| 7 | **Midterm Exam** | |
| 8 | Classical Architectures | MLPs, CNNs, pooling layers, ResNet-style residual networks |
| 9 | Sequence Models | RNNs, LSTMs, GRUs, temporal dependencies |
| 10 | Transformer Architecture | Self-attention, encoder-decoder, BERT, GPT, scalability |
| 11 | Generative Models I | Autoencoders, VAEs, GANs — latent space modeling and adversarial training |
| 12 | Generative Models II | Diffusion models, DDPM, image synthesis via denoising |
| 13 | Multimodal Models | CLIP, BLIP, vision-language fusion, cross-modal embeddings |
| 14 | Agentic Frameworks | MCP, A2A, Toolformer, ReAct, multimodal agent orchestration |
| 15 | **Final Exam** | |
| 16 | Makeup | |

## ⚠️ Failure conditions

Any of the following results in failure:

- **Attendance:** 1/4 of classes absent (8 times), unless permitted beforehand by
  the instructor (not by AA).
- No Lab, No Project, No Midterm exam, or No Final exam.

Course contents may be changed without notification during the semester.

---

## Note on the schedule numbers

The `Schedule` row reproduces the eClass syllabus field verbatim. eClass is
ambiguous about whether those numbers are clock hours or period (교시) indices:
the upcoming-events calendar labels the same classes with different period
numbers (e.g. a Monday DLCV class appears as `4교시` while the syllabus says
`14~16`). Treat the numbers as the registered values, and confirm actual
start times against the timetable image in `resources/` or with the instructor.
