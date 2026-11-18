# 9.2: Lightweight Convolutional Neural Network

**Artificial Intelligence · Week 9 · 16 slides · Dr. Oybek Eraliev**
Source: `week09 - 9.2. Lightweight CNN.pptx`, 77 MB, not in the repo: download it from eClass (https://eclass.inha.ac.kr/mod/ubfile/view.php?id=73164)

> **Final-exam material.** The professor said in class (week 7) that the midterm covers weeks 1–6 and that
> everything from week 7 on goes to the final.

Companion material:
- [CNN.ipynb](../../resources/CNN.ipynb), cells 23–32 ("Lightweight CNN" and "Custom CNN Models"), builds the
  three layer types in PyTorch, counts their parameters and makes a separable LeNet-5. The bugs in that part
  are listed in the [9.1 summary](week09%20-%209.1.%20Deep%20Learning%20(CNN).md#the-notebook-cnnipynb).

Why the file is 77 MB: slides 3–11 are six **animated GIFs** of 10–16 MB each, from
[animatedai.github.io](https://animatedai.github.io) (the watermark on every one). Each animation slide carries
only a one-line caption with the settings. **Open the pptx in slideshow mode** to see them move. Everything else
(slides 13–14) is one text slide and one chart.

## Outline

| Slides | Topic |
|---|---|
| 2, 6, 9, 12 | Contents: standard conv → grouped conv → depthwise separable conv → BatchNorm → implementation in PyTorch |
| 3 | **Standard conv**: 3×3 filter, stride 1, padding 0 (animation) |
| 4 | Same with **stride 2** |
| 5 | Same with **padding 1** |
| 7 | **Grouped conv**, groups = 1. This is the standard conv again (same animation as slide 3) |
| 8 | Grouped conv, **groups = 2** |
| 10 | **Depthwise conv**: groups = 8, one filter per input channel |
| 11 | **Depthwise separable conv**: the depthwise step, then a 1×1 **pointwise** conv |
| 13 | **BatchNorm**: mini-batches, standardise, then scale and shift (text) |
| 14 | ImageNet (ILSVRC) **top-5 error** by year: 28% (2010) → 26% → **AlexNet 16.4%** (2012) → ZFNet 11.7% → GoogLeNet/VGG 6.7% (2014) → **human 5%** → **ResNet 3.6%** (2015) → 3.1% → 2.3% (2017) |
| 15–16 | Question slide, thank-you |

## What the animations show

My reading of the GIFs (counting cubes): the input is **7×7 with 8 channels**, and there are **8 filters**,
so 8 output channels.

| Slide | Setting | Each filter | Output |
|---|---|---|---|
| 3 | standard, S = 1, P = 0 | 3×3×8 (full depth) | (7 − 3)/1 + 1 = 5 → **5×5×8** |
| 4 | standard, S = 2 | 3×3×8 | (7 − 3)/2 + 1 = 3 → **3×3×8** |
| 5 | standard, P = 1 | 3×3×8 | (7 − 3 + 2)/1 + 1 = 7 → **7×7×8** |
| 8 | groups = 2 | 3×3×**4**: filters 1–4 see channels 1–4 only, filters 5–8 see channels 5–8 only | 5×5×8 |
| 10 | groups = 8 (depthwise) | 3×3×**1**: each filter sees one channel | 5×5×8 |
| 11 | depthwise, then pointwise | 3×3×1 each, then eight **1×1×8** filters that mix the channels | 8 channels |

Weights in that setting (biases left out):

| Layer | Weights per filter | Filters | Total |
|---|---|---|---|
| Standard | 3·3·8 = 72 | 8 | **576** |
| Grouped, g = 2 | 3·3·4 = 36 | 8 | **288** |
| Depthwise, g = 8 | 3·3·1 = 9 | 8 | **72** |
| Depthwise separable | 72 + 8·(1·1·8) | | 72 + 64 = **136** |

## The formulas (mine, the deck has none)

`F` = filter size, `C_in`/`C_out` = input/output channels, `g` = groups. Weights only, add `C_out` biases.

| Layer | Parameters | Note |
|---|---|---|
| Standard | `F²·C_in·C_out` | every filter spans all input channels |
| Grouped | `F²·(C_in/g)·C_out` | **g times fewer**. C_in and C_out must both divide by g. No mixing between groups |
| Depthwise (g = C_in) | `F²·C_in` | one F×F filter per channel, no channel mixing at all |
| Depthwise separable | `F²·C_in + C_in·C_out` | depthwise filters spatially, then a 1×1 conv mixes channels |

Depthwise separable ÷ standard = `1/C_out + 1/F²`. With 3×3 filters and many channels that is roughly **8–9×
fewer** parameters and multiply-adds. Multiply-adds are the same expressions × `H_out·W_out`.

The two steps split the two jobs a standard conv does at once: **spatial** filtering (depthwise) and
**channel** mixing (pointwise). Grouped and depthwise convs alone never mix information between groups, which is
why the pointwise 1×1 is needed.

*(Mine.)* Where these are used: **MobileNet** is built from depthwise separable convs; **ResNeXt** and
**ShuffleNet** use grouped convs. The deck names no architecture.

## Worked numbers from the notebook

Cell 25 (no saved output, numbers computed by me): input 32 channels on 28×28, output 64 channels, 3×3,
padding 1, so every output is 64×28×28.

| Layer | Parameters |
|---|---|
| Standard | 3·3·32·64 + 64 = **18,496** |
| Grouped, `groups=32` | 3·3·1·64 + 64 = **640** |
| Depthwise separable | (3·3·32 + 32) + (32·64 + 64) = 320 + 2,112 = **2,432** |

Separable is 7.6× smaller than standard here. `groups=32` is even smaller, but each output channel sees only one
input channel.

Cells 26–27 (computed by me): the separable LeNet-5 has **42,160** parameters against **42,890** for the
standard one in 9.1. The saving is tiny because **41,854** of those parameters sit in the fully connected layers.
Lightweight convs only pay off where the conv layers hold most of the weights.

## BatchNorm (slide 13)

The slide's steps:
1. Split the dataset at random into mini-batches (without replacement).
2. Standardise each batch: `(Xᵢ − X_mean) / X_std`.
3. Scale and shift: `γXᵢ + β`, so the network can undo the standardisation if that helps.

The full version *(mine)*, per channel, over a mini-batch B:

```
μ_B  = mean of x over the batch            (for conv layers: over N, H and W)
σ²_B = variance of x over the batch
x̂    = (x − μ_B) / √(σ²_B + ε)             ε avoids division by zero
y    = γ·x̂ + β                              γ, β are learned, 2 per channel
```

At test time there is no batch to average over, so it uses **running averages** of μ and σ² collected during
training. In PyTorch `model.eval()` switches to them, and `model.train()` switches back. Why bother:
training is more stable and faster, higher learning rates work, and there is a mild regularising effect.

```python
nn.Sequential(nn.Conv2d(32, 64, 3, padding=1, bias=False), nn.BatchNorm2d(64), nn.ReLU())
```

## Things that are wrong or loose in the deck

- **Slide 13 says BatchNorm comes "after activation".** The original paper (Ioffe & Szegedy, 2015) normalises
  **before** the non-linearity (conv → BN → ReLU), which is also the usual PyTorch pattern. Both orders are seen
  in practice, so don't state either as the only rule. *(Mine:)* a conv bias before BN is wasted, because BN
  subtracts the mean anyway.
- **Slide 13 leaves out** ε, that γ and β are learned, that it works per channel, and the train/test difference
  (running averages). The notebook has no BatchNorm layer, although the contents slides list it.
- **Slide 11's caption says "Padding = 0"**, but its animation shows a grey padded border like slide 5's
  (my reading of the GIF). Its "groups = 8" also only describes the depthwise step; the pointwise 1×1 is an
  ordinary conv (groups = 1).
- **The "Implementation of CNN using PyTorch Framework" item** on every contents slide has no slides. The
  notebook is that part.
- **Slide 14's 2017 bar has no label.** *(Mine:)* it's SENet, the last ILSVRC winner. The "human 5%" bar is one
  person's estimate (Andrej Karpathy's), not a measured average.
- The deck is titled "Lightweight CNN" but never names a lightweight network (MobileNet, ShuffleNet,
  EfficientNet). The building blocks are what you need to know.

## Exam checklist

- [ ] Parameter count of a standard, grouped, depthwise and depthwise separable layer for given F, C_in, C_out, g
- [ ] What `groups = 1`, `groups = 2` and `groups = C_in` mean for which channels each filter sees
- [ ] Why depthwise separable needs the 1×1 pointwise step (channel mixing)
- [ ] The ratio `1/C_out + 1/F²` and why it's about 8–9× for 3×3
- [ ] Output size with stride and padding (same formula as 9.1)
- [ ] BatchNorm: the steps, what γ and β do, training vs inference
- [ ] ImageNet top-5 milestones: AlexNet 16.4% (2012), human ~5%, ResNet 3.6% (2015)
