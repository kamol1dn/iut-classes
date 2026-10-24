# L8 — MATLAB / Octave for Image Processing

**Multimedia Computing · Week 4 · 47 slides · Dr. Minhaz Uddin Ahmed**
Source: [week04 - Multimedia Computing L8 (Matlab-Octave).pptx](../slides/week04%20-%20Multimedia%20Computing%20L8%20(Matlab-Octave).pptx) *(5 MB)*
Practice: [practice code L8 - experiment.txt](../../resources/practice%20code%20L8%20-%20experiment.txt) ·
[300cat.jpeg](../../resources/300cat.jpeg) · [300dog.jpeg](../../resources/300dog.jpeg)

A tooling lecture. **Almost every slide is a screenshot of code with only a
title as text**, so this summary can only give the outline. **Open the pptx to
see the actual commands.** Treat it as a lab handout. The free route is
**GNU Octave**, which runs almost all of this code unchanged, or Google Colab
for the Python equivalents.

## Outline

| Slides | Topic |
|---|---|
| 3–4 | MATLAB desktop: command window, workspace, editor |
| 5–11 | Variables, scalars, vectors, matrices |
| 12–14 | Matrix indexing. **1-based, column-major**, `A(r,c)`, `A(:)`, `end` |
| 15–20 | Matrix operations: `*` vs element-wise `.*` `./` `.^`, transpose, concatenation `[A B]`, `[A; B]` |
| 21–22 | Strings, cell arrays `{}`, structs |
| 23–24 | Operators, `if` / `for` / `while` |
| 25–27 | Script `.m` files, functions, debugging |
| 28 | Plotting |
| 29–32 | **Images:** data type (`uint8` vs `double`), `imread` / `imshow` / `imwrite`, `rgb2gray`, `im2double`, arithmetic |
| 33–35 | **Filtering / convolution:** `fspecial`, `imfilter` |
| 36–39 | **Morphology:** `strel`, `imerode`, dilation |
| 40–41 | Octave: load data, `image(X)`, `colormap(map)`, down-sample `X(1:2:200,:)` |
| 42–44 | Google Colab / Jupyter |

Reference tutorial (slide 45): Cambridge's Octave tutorial, `octavetut.pdf`.

## Morphology example from slide 36

```matlab
A = [0 0 0 0 0 0; 0 0 1 1 0 0; 0 1 1 1 1 0; 0 0 1 1 0 0; 0 0 0 0 0 0];
B = strel([1;1;1]);          % vertical 3x1 line
A_eroded_By_B = imerode(A, B)
```

On the slide, each row of A is written run together, as `000000`. MATLAB would
read that as the single number 0, so space the digits out as above. Eroding by a vertical 3-line
keeps a pixel only if the pixels above and below it are also 1. Only the
**two centre pixels of the middle row** survive.

## The practice script

[experiment.txt](../../resources/practice%20code%20L8%20-%20experiment.txt) is
four snippets, pasted from a MATLAB session:

1. **Add two images.** It uses the cat and dog images, which are both
   1024×1024 RGB. Both are converted with `im2double` and summed.
2. **Logical OR** of two binarised images (`imbinarize(rgb2gray(...))`).
3. **Logical NOT** of each image.
4. **Blur** with a 5×5 averaging filter: `fspecial('average',[5 5])` + `imfilter`.

To run it: drop the `>>` prompts, run from the `resources/` folder so
`imread` finds the jpegs, and point snippets 2–4 at `300cat.jpeg` /
`300dog.jpeg` instead of `image1.jpg`. `imbinarize` needs the Image
Processing Toolbox (`pkg load image` in Octave).

> ⚠️ **Two things in snippet 1 don't work as written.**
> - `if size(image1) ~= size(image2)` compares two vectors. MATLAB's `if` is
>   true only when *every* element is non-zero, so this raises an error only if
>   **all** dimensions differ. Use `if ~isequal(size(image1), size(image2))`.
> - `imshow(result_image)` runs **before** the normalising step. The sum goes
>   up to 2.0, and anything above 1 shows as white. Divide by
>   `max(result_image(:))` first, then display.

## Python equivalents (for Colab)

| MATLAB | Python |
|---|---|
| `imread` / `imshow` | `cv2.imread` / `plt.imshow` (OpenCV loads **BGR**) |
| `im2double` | `img.astype(float) / 255` |
| `rgb2gray` | `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` |
| `imbinarize` | `cv2.threshold(g, 0, 255, cv2.THRESH_OTSU)` |
| `fspecial('average',[5 5])` + `imfilter` | `cv2.blur(img, (5,5))` |
| `imerode(A, strel(...))` | `cv2.erode(A, kernel)` |
