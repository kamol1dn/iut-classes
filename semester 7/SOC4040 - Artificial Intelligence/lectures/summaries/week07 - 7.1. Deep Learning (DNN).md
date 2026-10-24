# 7.1: Deep Learning: Deep Neural Network (Part 1)

**Artificial Intelligence · Week 7 · 30 pages · Dr. Oybek Eraliev**
Source: [week07 - 7.1. Deep Learning (DNN).pdf](../slides/week07%20-%207.1.%20Deep%20Learning%20(DNN).pdf) *(1.3 MB)*

> **Final-exam material, not midterm.** The professor said in class (week 7) that the midterm covers
> up to the week-6 lectures and that week 7's topics go to the final.

Companion material:
- [Neural_Network.ipynb](../../resources/Neural_Network.ipynb) builds the deck's exact 2-2-1 network by
  hand (same names `w_11 … w_14`, `w_21`, `w_22`, `b_11`, `b_12`, `b_2`), first with no activation, then with
  ReLU, then vectorised in NumPy and in PyTorch. It then does classification (ReLU hidden layer, sigmoid output,
  BCE loss, 91% test accuracy) and a 3-hidden-layer PyTorch DNN mixing ReLU, Tanh and SELU. This is the
  deck's missing "Implementation of DNN" section. The last cells read a `Bin_packing.csv` that isn't shipped.

The deck is titled "Part – 1", so expect a 7.2 / Part 2. Much of the maths is typeset as images, so the
PDF's text layer is garbled. **Open the PDF for pages 3–9 and 16–23.** Pages 10 and 25–27 are pictures
only (the DNN diagram and the activation-function plots).

## Outline

| Pages | Topic |
|---|---|
| 2, 11, 14, 24, 28 | Contents: model representation → loss functions → backpropagation → activation functions → implementation |
| 3–4 | **Perceptron forward pass**: inputs × weights → sum → non-linearity. `ŷ = g(w₀ + Σᵢ xᵢwᵢ)`, with `g` the sigmoid `1/(1+e⁻ᶻ)` |
| 5 | Simplified perceptron: `z = w₀ + Σ xⱼwⱼ`, `y = g(z)` |
| 6 | **Multi-output perceptron**: one `zᵢ` per output, `yᵢ = g(zᵢ)` |
| 7–9 | **"Single layer" neural network** = one hidden layer (3 inputs → 4 hidden → 2 outputs). Weight matrices `W⁽¹⁾`, `W⁽²⁾`. Pages 8–9 expand `a₂` term by term |
| 10 | Picture of a deep network: 3 hidden layers |
| 12 | **Binary cross-entropy** loss, for outputs that are a probability in (0, 1) |
| 13 | **Mean squared error** loss, for regression outputs |
| 15 | **Gradient descent**: random init → loop {gradient, update} → return weights |
| 16–18 | Worked network: **2 inputs → 2 hidden (a₁, a₂) → 1 output**, nine parameters. Forward pass |
| 19–23 | **Backprop on that network** with per-sample MSE: loss → `∂L/∂ŷ` → output-weight gradients → input-weight gradients (chain rule) → update all nine |
| 25–27 | Activation functions (plots only): **sigmoid, tanh, ReLU, Leaky ReLU, ELU, SELU** |
| 29–30 | Question slide, thank-you |

## The worked network (pages 16–18)

Weight naming from the diagram (the notebook uses the same):

| Weight | Connects |
|---|---|
| `w11` | x₁ → a₁ |
| `w12` | x₁ → a₂ |
| `w13` | x₂ → a₁ |
| `w14` | x₂ → a₂ |
| `w21`, `w22` | a₁ → ŷ, a₂ → ŷ |
| `b11`, `b12`, `b2` | biases of a₁, a₂, ŷ |

Forward pass:

```
a1 = g(x1·w11 + x2·w13 + b11)
a2 = g(x1·w12 + x2·w14 + b12)      ← the deck prints x2·w12 here, see errors below
ŷ  = g(a1·w21 + a2·w22 + b2)
```

Backprop (pages 19–23), as the deck gives it:

```
Loss = (ŷ − y)²                       ∂Loss/∂ŷ = 2(ŷ − y)
∂Loss/∂w21 = ∂Loss/∂ŷ · ∂ŷ/∂w21       (same shape for w22, b2)
∂Loss/∂w11 = ∂Loss/∂ŷ · ∂ŷ/∂a1 · ∂a1/∂w11   (same shape for w13, b11)
w := w − α · ∂Loss/∂w                  for all nine parameters
```

*(Mine, not in the deck.)* The deck stops at the chain-rule shape and never evaluates the factors.
Write `z1, z2, zo` for the sums inside each `g(·)`. Then, with `δ = ∂Loss/∂zo = 2(ŷ − y)·g′(zo)`:

| Parameter | Gradient |
|---|---|
| `w21`, `w22`, `b2` | `δ·a1`, `δ·a2`, `δ` |
| `w11`, `w13`, `b11` | `δ·w21·g′(z1)·x1`, `δ·w21·g′(z1)·x2`, `δ·w21·g′(z1)` |
| `w12`, `w14`, `b12` | `δ·w22·g′(z2)·x1`, `δ·w22·g′(z2)·x2`, `δ·w22·g′(z2)` |

For sigmoid, `g′(z) = g(z)(1 − g(z))`. With a linear output (as the notebook does for regression),
`g′(zo) = 1` and `δ` is just `2(ŷ − y)`, which is the notebook's `dL_dy`. The pattern to remember: a
weight's gradient = (error signal arriving at its neuron) × (the input that weight multiplies).

## The ones to memorise

| Thing | Rule |
|---|---|
| Neuron | `ŷ = g(w₀ + Σ xᵢwᵢ)`: weighted sum plus bias, then a non-linearity `g` |
| Why `g` must be non-linear *(mine)* | without it, stacked layers collapse into one linear map. The notebook's first, activation-free network is just linear regression |
| BCE | `J(W) = −(1/m) Σ [ y⁽ⁱ⁾ log ŷ⁽ⁱ⁾ + (1 − y⁽ⁱ⁾) log(1 − ŷ⁽ⁱ⁾) ]`. Pair with a **sigmoid output** (classification) |
| MSE | `J(W) = (1/m) Σ (ŷ⁽ⁱ⁾ − y⁽ⁱ⁾)²`. Pair with a **linear output** (regression) |
| Gradient descent | `W := W − α · ∂J(W)/∂W`, `α` = learning rate |
| Backpropagation | the chain rule, applied from the output back towards the input |
| Sigmoid | `1/(1+e⁻ᶻ)`, range (0, 1). *(Mine:)* `g′ = g(1−g)`, at most 0.25, so gradients vanish in deep stacks |
| Tanh | `(eᶻ − e⁻ᶻ)/(eᶻ + e⁻ᶻ)`, range (−1, 1). *(Mine:)* zero-centred, still saturates |
| ReLU | `max(0, z)`. *(Mine:)* gradient 1 or 0, cheap, no saturation for z > 0, but units can "die" |
| Leaky ReLU | `max(0.1·z, z)` on the slide's plot. *(Mine:)* small negative slope keeps a gradient; PyTorch's default slope is 0.01, which the notebook prints |
| ELU | `z` for z > 0, `α(eᶻ − 1)` for z ≤ 0 |
| SELU | `λ` × ELU with fixed `α ≈ 1.6733`, `λ ≈ 1.0507` |

## Things that are wrong or loose in the deck

- **Page 18's forward pass has a wrong weight.** It prints `a₂ = g(x₁w₁₂ + x₂w₁₂ + b₁₂)`. By the diagram,
  x₂ reaches a₂ through **w₁₄**: `a₂ = g(x₁w₁₂ + x₂w₁₄ + b₁₂)`. The same page calls the activations
  "h₁₁ and h₁₂" and then names them a₁, a₂.
- **Page 6 applies the activation twice.** It defines `zᵢ = g(w₀,ᵢ + Σ xⱼwⱼ,ᵢ)` and then `yᵢ = g(zᵢ)`.
  `zᵢ` is the pre-activation and has no `g`, as page 7 correctly writes it.
- **Page 9 drops the `g`.** It reads `a₂ = g(w₀,₂ + Σ …) = w₀,₂ + x₁w₁,₂ + x₂w₂,₂ + x₃w₃,₂`. The
  right-hand side is `z₂`, not `a₂`. Page 8 is the same slide done correctly (with the bias written `b⁽¹⁾`
  instead of `w₀,₂`).
- **Page 7's output formula has the wrong sum.** `ŷᵢ = g(w₀,ᵢ⁽²⁾ + Σᵢ₌₁ᵐ g(zⱼ)wⱼ,ᵢ⁽²⁾)` sums over `i`
  up to `m` (the number of inputs). It should sum over the hidden units, `j = 1 … 4`.
- **Page 12's BCE is missing its brackets.** As typeset, the `−1/m Σ` only covers the first term.
  Both terms belong inside the sum (formula above).
- **Pages 19–23 call it a regression network but keep `ŷ = g(…)`.** With the deck's sigmoid `g`, the
  output can never leave (0, 1), which is wrong for regression. The output layer should be linear.
  The notebook does this correctly ("Output layer (no activation, linear regression)").
- **Page 21's and 22's headings are shifted.** "Step 3: Hidden Layer weights" is actually the
  hidden→output weights (w₂₁, w₂₂, b₂), and "Step 4: Input Layer weights" is the input→hidden ones.
  Step 4 also only shows a₁'s three parameters. w₁₂, w₁₄ and b₁₂ go through a₂ and w₂₂ (table above).
- **Page 25 labels tanh as `σ(z)` and sigmoid as `φ(z)`.** `σ` normally means the sigmoid. Don't mix
  them up on an exam.
- **Page 27 prints the α and λ constants under both ELU and SELU.** They are SELU's fixed values.
  ELU's α is a free hyperparameter (commonly 1).
- **The contents slides disagree.** Pages 14, 24 and 28 list "History and Intro to Deep Learning", which
  pages 2 and 11 don't, and no such slides exist. "Implementation of DNN" (p. 28) is followed only by the
  question slide. The implementation is the notebook.
- The worked "DNN" has a single hidden layer. That is a shallow network. "Deep" means several hidden
  layers, as in page 10's picture and the notebook's last model.

## Links to other courses

- **Artificial Intelligence 2.2 (logistic regression)** is a single sigmoid neuron with BCE loss
  ("log loss") and the same gradient-descent update. This deck stacks those neurons.
- **Deep Learning for Computer Vision** builds on exactly this forward/backward pass.
