# 9.1: Deep Learning: Convolutional Neural Network

**Artificial Intelligence · Week 9 · 66 pages · Dr. Oybek Eraliev**
Source: [week09 - 9.1. Deep Learning (CNN).pdf](../slides/week09%20-%209.1.%20Deep%20Learning%20(CNN).pdf) *(25 MB)*

> **Final-exam material.** The professor said in class (week 7) that the midterm covers weeks 1–6 and that
> everything from week 7 on goes to the final. The calculable parts are on pages 38–64: output size,
> parameter count, a convolution by hand, and pooling by hand.

Companion material:
- [CNN.ipynb](../../resources/CNN.ipynb) is the deck's missing "Implementation of CNN using PyTorch" section.
  It checks `nn.Conv2d` shapes and parameter counts, then trains a LeNet-5-style network on Fashion-MNIST
  (86.7% test accuracy). Its second half covers the lightweight layers from
  [9.2](week09%20-%209.2.%20Lightweight%20CNN.md), a custom 4-conv CNN and AlexNet. Details and bugs are
  [below](#the-notebook-cnnipynb).

Most of the deck is pictures, many of them taken from Stanford CS231n. **Open the PDF for pages 3–8, 10–13,
20–37 and 61.** The text layer only carries titles and the worked numbers.

## Outline

| Pages | Topic |
|---|---|
| 2, 9, 60 | Contents: model representation → convolutional layer → pooling layer → implementation in PyTorch |
| 3 | **AlexNet** (Krizhevsky, Sutskever, Hinton, 2012) on ImageNet: the start of the CNN era |
| 4–7 | "ConvNets are everywhere": classification, retrieval, detection (Faster R-CNN), segmentation, image captioning, style transfer |
| 8 | A **LeNet-5** diagram (not named on the slide): 32×32 input → 6@28×28 → pool 6@14×14 → 16@10×10 → pool 16@5×5 → 120 → 84 → 10 |
| 10–13 | How an image is stored. **RGB** has 3 channels, each 0–255 (8 bit). **Grayscale** has 1 channel. Lena is 512×512×3 in colour and 512×512×1 in grey |
| 14–19 | A 7×7 binary "1" flattened into a 49-long vector for an ordinary network. The deck asks "How to train ANN on this kind of images?" |
| 20 | Recap of a fully connected layer: 32×32×3 is stretched to 3072×1, and `W` is 10×3072 |
| 21–24 | **Conv layer keeps the spatial structure.** A 5×5×3 filter always spans the **full depth** of the input. One output = a 75-dimensional dot product + bias, `wᵀx + b` |
| 25–30 | Sliding one filter over all positions gives one 28×28 **activation map**. A second filter gives a second map. 6 filters give 6×28×28 |
| 31–34 | One bias per filter (a 6-dim bias vector). Batches: N×C_in×H×W in, N×C_out×H′×W′ out, filters C_out×C_in×K_h×K_w |
| 35–37 | A ConvNet is a stack of conv layers with **ReLU** in between: 32×32×3 → (six 5×5×3) → 28×28×6 → (ten 5×5×6) → 24×24×10 |
| 38–46 | **Spatial size by hand**: 7×7 input, 3×3 filter. Stride 1 gives 5×5, stride 2 gives 3×3, stride 3 "doesn't fit" |
| 47–49 | **Zero padding** (P = 1, P = 2). 7×7, F = 3, S = 1, P = 1 gives 7×7. Padding `(F − 1)/2` keeps the size |
| 50–54 | **Worked convolution**: 7×7 input padded by 1, filter `[[1,2,1],[0,0,0],[1,2,1]]`, b = 0 → 7×7 output (page 54 has errors, see below) |
| 55–58 | **Examples**: 32×32×3 input, ten 5×5 filters, S = 1, P = 2 → 32×32×10, **760 parameters** |
| 59 | **Conv layer summary**: the four hyperparameters and the formulas below |
| 61 | **Pooling layer**: makes the representation smaller, works on each activation map separately. 224×224×64 → 112×112×64 |
| 62–63 | **Max pooling** and **average pooling**, 2×2 with stride 2, worked on a 4×4 slice |
| 64 | Pooling summary |
| 65–66 | Question slide, thank-you |

## The ones to memorise

| Thing | Rule |
|---|---|
| Conv hyperparameters | number of filters **K**, filter size **F**, stride **S**, zero padding **P** |
| Conv output size | `W₂ = (W₁ − F + 2P)/S + 1`, `H₂ = (H₁ − F + 2P)/S + 1`, depth = **K** |
| "Doesn't fit" | the formula must give a whole number. 7×7, F = 3, S = 3 gives 2.33, so it doesn't fit. *(Mine:)* PyTorch silently rounds down |
| Same-size padding | stride 1 and `P = (F − 1)/2`: F = 3 → P = 1, F = 5 → P = 2, F = 7 → P = 3 |
| Conv parameters | `F²·C·K` weights + `K` biases (C = input depth) |
| Filter depth | always equals the input depth: "filters always extend the full depth of the input volume" |
| Pooling hyperparameters | spatial extent **F**, stride **S** |
| Pooling output size | `W₂ = (W₁ − F)/S + 1`, `H₂ = (H₁ − F)/S + 1`, depth **unchanged** (C) |
| Pooling parameters | **0**. Nothing to learn |
| Max vs average pooling | max keeps the largest value in each window, average keeps the mean |

*(Mine.)* Why convolution beats a fully connected layer on images: a fully connected layer mapping 32×32×3 to
32×32×10 would need 3072 × 10240 ≈ **31.5 million** weights. The conv layer on pages 55–58 does it with
**760**, because each filter looks at a small patch (local connectivity) and the same filter is reused at every
position (weight sharing).

*(Mine.)* What a CNN calls "convolution" is really cross-correlation, because the filter is not flipped.
Page 50's filter is symmetric, so here it makes no difference.

## Worked examples

**Spatial size (pages 38–49)**, 7×7 input, 3×3 filter:

| Stride | Padding | Output |
|---|---|---|
| 1 | 0 | (7 − 3)/1 + 1 = **5** → 5×5 |
| 2 | 0 | (7 − 3)/2 + 1 = **3** → 3×3 |
| 3 | 0 | (7 − 3)/3 + 1 = 2.33 → doesn't fit |
| 1 | 1 | (7 − 3 + 2)/1 + 1 = **7** → 7×7 |

**Output volume and parameters (pages 55–58).** Input 32×32×3, ten 5×5 filters, stride 1, pad 2:
- Size: (32 + 2·2 − 5)/1 + 1 = 32, so the output is **32×32×10**.
- Parameters: each filter has 5·5·3 + 1 = 76, so 76 × 10 = **760**.

*(Mine, same type of question.)* AlexNet's first layer: 227×227×3 input, 96 filters of 11×11, stride 4, pad 0.
Output (227 − 11)/4 + 1 = **55**, so 55×55×96. Parameters 11·11·3·96 + 96 = **34,944**. A 3×3, stride-2 max pool
after it gives (55 − 3)/2 + 1 = **27**, so 27×27×96, with 0 parameters.

*(Mine.)* LeNet-5 on page 8, traced with the formulas: 32 → conv 5×5 → 28 → pool 2/2 → 14 → conv 5×5 → 10 →
pool 2/2 → 5, so 16·5·5 = 400 values go into the 120-unit layer.

**Convolution by hand (pages 50–54).** Input (before padding by 1) and filter, bias 0:

```
input 7×7               filter
2 1 1 2 4 2 1           1 2 1
3 2 3 2 3 1 1           0 0 0
1 1 2 2 2 3 3           1 2 1
1 2 1 3 1 2 1
2 2 2 2 2 0 2
3 2 3 1 3 2 1
2 3 2 3 1 2 1
```

The middle row of the filter is zero, so each output is just (row above · [1 2 1]) + (row below · [1 2 1]).
Page 51 does the top-left cell: 0·1 + 3·2 + 2·1 = **8** (the row above is padding). The correct full output, with
the cells the slide gets wrong in **bold**:

| | c1 | c2 | c3 | c4 | c5 | c6 | c7 |
|---|---|---|---|---|---|---|---|
| r1 | 8 | 10 | 10 | 10 | 9 | 6 | 3 |
| r2 | **8** | **10** | 12 | 17 | 21 | 20 | 13 |
| r3 | **12** | 16 | 17 | **18** | 16 | 12 | 7 |
| r4 | **9** | 13 | 15 | 16 | 15 | 15 | 13 |
| r5 | 12 | 16 | 16 | 16 | 16 | 14 | 8 |
| r6 | 13 | 18 | **18** | 17 | 13 | **10** | 8 |
| r7 | 8 | 10 | 9 | 8 | 9 | 8 | 4 |

| Row, col | Correct | Page 54 |
|---|---|---|
| 2, 1 | **8** | 6 |
| 2, 2 | **10** | 12 |
| 3, 1 | **12** | 11 |
| 3, 4 | **18** | 17 |
| 4, 1 | **9** | 7 |
| 6, 3 | **18** | 20 |
| 6, 6 | **10** | 11 |

Check row 2, col 1: the window is `[0 2 1 / 0 3 2 / 0 1 1]`, so (0 + 4 + 1) + (0 + 2 + 1) = 8. The other 42 cells
on page 54 are right (checked in NumPy).

**Pooling (pages 62–63)**, single 4×4 depth slice, 2×2 windows, stride 2:

```
1 1 | 2 4        max:  6 8        average:  3.25 5.25
5 6 | 7 8              3 4                  2    2
----+----
3 2 | 1 0
1 2 | 3 4
```

Average of the top-left window: (1 + 1 + 5 + 6)/4 = 3.25. Both slides are correct.

## Things that are wrong or loose in the deck

- **Page 54's output grid has seven wrong cells** (table above). Pages 51–53 build the first three cells
  (8, 10, 10) correctly. The rest of the grid appears all at once, and that is where the mistakes are.
- **Page 13's grey scale is labelled backwards.** It puts **255 under black** and **0 under white**. In 8-bit
  grayscale, 0 is black and 255 is white.
- **Pages 14–19 call a 0/1 image "2 bit color format".** Two levels need only **1 bit** per pixel. 2 bits
  would give 4 grey levels.
- **Page 64's pooling summary says "Conv layer needs 2 hyperparameters".** It's the pooling layer. The text was
  copied from page 59.
- **Page 9's contents slide says "Implementation of CNN in TensorFlow Framework".** Pages 2 and 60 say
  PyTorch, and the notebook is PyTorch. There are no implementation slides at all; the notebook is that part.
- **Pages 62–63, "Introduces spatial invariance"**, is loose. *(Mine:)* pooling gives a little **translation**
  invariance: a feature that moves by a pixel inside the pooling window gives the same output. It does nothing
  for rotation or scale, and larger shifts still change the output.

## The notebook (CNN.ipynb)

| Cells | What it does |
|---|---|
| 2–5 | `nn.Conv2d` from 3 to 64 channels with "same" padding, so the size is kept (32×32, and 64×64 in cell 5): 3×3/P1 → **1,792** params, 5×5/P2 → **4,864**, 7×7/P3 → **9,472**. Each is `F²·3·64 + 64`, the page-59 formula |
| 6–7 | `DoubleConvLayer`: a 3×3 and a 7×7 branch added together, then 2×2 max pool → 64×16×16, 11,264 params (1,792 + 9,472) |
| 8–14 | **Fashion-MNIST**: 60,000 train and 10,000 test images, 1×28×28, 10 clothing classes. `DataLoader` with batch 64 |
| 15–22 | A LeNet-5-style model (**42,890** params) trained for 10 epochs: cross-entropy, SGD with lr 0.01 and momentum 0.9. Test accuracy **86.7%**, then 9 sample predictions |
| 23–27 | 9.2's layers: standard, grouped and depthwise separable conv, and a separable LeNet-5. See the [9.2 summary](week09%20-%209.2.%20Lightweight%20CNN.md) |
| 28–32 | A custom 4-conv CNN (32 → 64 → 128 → 256 channels, two max pools, then 12,544 → 50 → 10), in a standard and a "depthwise separable" version |
| 33–36 | AlexNet and a 5-epoch training loop (never run, see below) |

The training loop is the pattern to copy for any PyTorch project: `model.train()`, then for each batch
`zero_grad → forward → loss → backward → step`, then `model.eval()` with `torch.no_grad()` for evaluation.

Problems in the notebook:
- **Its `LeNet5` isn't textbook LeNet-5.** `pool1` is an average pool with kernel **5**, stride 2 (textbook:
  2×2), and `conv2` is 3×3 (textbook: 5×5). It still ends at 16×4×4 on 28×28 input, so it runs. The `SepLeNet5`
  in cell 26 uses the textbook layout, so comparing the two is not like-for-like.
- **Cell 31's "depthwise" conv is missing `groups=in_channel`.** As written it's an ordinary 3×3 conv followed by
  a 1×1, not depthwise separable. Computed by me (the cell has no saved output): the conv layers have
  **237,290** parameters as written and **45,770** with `groups` added, against **387,840** for the standard
  version. Cell 32 also prints "myStdCNN" for the separable model. In both models `fc1` (12,544 → 50) holds
  **627,250** parameters, more than all the convs together.
- **Cell 33's AlexNet assigns `self.conv4` twice**, so the second one (384 → 256) overwrites the first, and
  AlexNet's fifth conv layer is missing. It also can't run on 1×28×28 Fashion-MNIST. By the size formula, conv1
  (11×11, stride 4, pad 2) gives 6×6, pool1 (3×3, stride 2) gives 2×2, and pool2's 3×3 window no longer fits.
  `view(-1, 256*6*6)` expects an input of about 224×224, so resize first (`transforms.Resize(224)`). Cells 34–36
  have no saved output.
- **Cell 20 plots training and validation loss** but labels the y-axis "Accuracy %".
- **The test set doubles as the validation set**, so cell 21's "test accuracy" is the same 0.8668 as epoch 10's
  "val accuracy". Fine for a demo. For a project, keep a separate validation split and touch the test set once.

To run it: `pip install torch torchvision matplotlib`. Fashion-MNIST downloads itself (`download=True`). The
notebook picks `cuda`, then Apple `mps`, then `cpu`.

## Exam checklist

- [ ] Why a fully connected layer is a poor fit for images (parameter count, lost spatial structure)
- [ ] Filter depth = input depth; one filter → one activation map; K filters → depth K
- [ ] Output size `(W − F + 2P)/S + 1` for any stride and padding, and spot when it "doesn't fit"
- [ ] Padding that keeps the size: `(F − 1)/2`
- [ ] Parameter count `F²·C·K + K` (the 760 example)
- [ ] A 3×3 convolution by hand on a small padded input
- [ ] Max and average pooling by hand; pooling output size; why pooling has 0 parameters
- [ ] Shape trace of LeNet-5 (page 8)
- [ ] RGB vs grayscale: channels and the 0–255 range (0 = black)
