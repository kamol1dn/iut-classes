# L15: Computer Graphics: Areas, Pipeline and Raster Images

**Multimedia Computing · Week 9 · 54 slides · Dr. Minhaz Uddin Ahmed**
Source: [week09 - Multimedia Computing L15 (graphics).pptx](../slides/week09%20-%20Multimedia%20Computing%20L15%20(graphics).pptx) *(3.7 MB)*

Marschner & Shirley, *Fundamentals of Computer Graphics* (4th ed.), **chapter 1** (introduction) and
**chapter 3** (raster images). The cover is on slide 52. This book is not one of the three textbooks in the
course README. The history slides (4–7, 12, 14–15) come from a standard intro-to-graphics lecture ("slide
ideas … courtesy Marc Levoy"). The deck ends with two Python practice snippets: a vector image with
`svgwrite` and a raster image with Pillow. Nearly everything is text, so the pptx only adds the history
pictures and the LED/LCD and compositing figures (slides 37, 39, 46).

This is exactly his week-1 plan for week 9 ("computer graphics: raster images & devices"). The eClass
syllabus has JPEG here instead. His plan put **ray tracing** in week 10, but the week-10 decks (L16, L17)
are geometric processing and segmentation, so no deck has covered ray tracing yet.

## Outline

| Slides | Topic |
|---|---|
| 3 | **Computer graphics** = any use of computers to create and manipulate images. 2D or 3D, fully synthetic or made from photographs |
| 4–7 | History: the term was coined by William Fetter (Boeing, 1960). First graphics system: SAGE radar displays (MIT, mid-1950s). **Sketchpad** (Sutherland, MIT 1963) was the first interactive system, with pop-up menus, constraint-based drawing and hierarchical modelling. SuperPaint (Shoup and Smith, PARC 1973–79). Image processing for TV sports overlays |
| 8–9 | The three main areas. **Modeling**: a mathematical description of shape and appearance (a mug as 3D points, an interpolation rule and a reflection model). **Rendering**: making shaded images from 3D models. **Animation**: the illusion of motion through a sequence of images. Slide 9 chains them as a "3D graphics pipeline" |
| 10–11 | Modeling: spline curves and surfaces (70s–80s), the Utah teapot, triangle meshes scanned from real objects |
| 12–15 | Rendering history. **Visibility** (1960s): Roberts, Appel (hidden lines), Warnock, Watkins (hidden surfaces), "visibility = sorting". **Lighting** (1970s): Gouraud (diffuse), Phong (specular), Blinn (curved surfaces, texture), Catmull (**z-buffer**). **Global illumination** (1980s): Whitted 1980 **ray tracing**, Goral/Torrance 1984 **radiosity**, Kajiya 1986 the **rendering equation** |
| 16 | **CGI** covers still and moving images. **Computer animation** means moving images only |
| 17–18 | Other areas: user interaction, virtual reality (stereo plus head tracking, ideally sound and force feedback), visualization, image processing, 3D scanning, computational photography |
| 19 | Why study it: the maths of projections, curves and surfaces, the physics of lighting, and graphics software and hardware |
| 20–22 | Applications: games, cartoons, visual effects (compositing), animated films, **CAD/CAM**, simulation (flight simulators), medical imaging (a CT scan is a 3D array of densities), information visualization |
| 23 | **Graphics APIs**: every program needs a graphics API (output) and a user-interface API (input). Two styles: integrated in the language (Java), or a library such as **OpenGL / Direct3D** with a separate UI toolkit |
| 24–25 | The **graphics pipeline** in every desktop: maps 3D triangle vertices to 2D screen positions and shades them. Visibility is now solved by brute force with the **z-buffer**. The geometry runs in **4D homogeneous coordinates** |
| 26–27 | Numerical issues: the **IEEE floating-point** standard and its special values `+∞`, `−∞`, `NaN` |
| 28–29 | Efficiency: memory access patterns matter more than operation counts. Order: write it plainly, compile optimized, profile, improve data locality, and only then read the assembly |
| 30–32 | Class design: `vector2`, `vector3`, `hvector` (4 components), `rgb`, `transform` (4×4 matrix), `image`. Float vs double: float saves memory, double avoids numerical trouble |
| 33–35 | **Raster image** (a 2D array of pixel values) vs **vector image** (shape descriptions, resolution independent) |
| 36 | Raster devices: displays (**transmissive** LCD, **emissive** LED), hardcopy (binary ink-jet, continuous-tone dye sublimation), input (2D sensor: camera, 1D sensor: flatbed scanner) |
| 37–40 | Displays: each pixel has red, green and blue **subpixels**. LED pixels emit light. An LCD pixel sits between two polarizers, and the liquid crystal rotates the light's polarization by an amount set by the voltage |
| 41–44 | **Rasterization**: converting vector shapes into pixels. Bitmapped (raster) graphics and the usual paint programs (Photoshop, GIMP, …) |
| 45–46 | **Alpha compositing** (formula below) |
| 47 | Storage: **JPEG** (lossy, for natural images), **TIFF** (binary images or lossless 8/16-bit RGB), **PPM** (simple, lossless, uncompressed), **PNG** (lossless) |
| 48–51 | Practice: `svgwrite` writes `vector_image.svg` (rectangle, circle, line, text). Pillow `ImageDraw` writes `raster_image.png` with similar shapes |

## Formulas to know

| Thing | Formula / fact |
|---|---|
| Alpha compositing, "over" (slide 46, Eq. 3.2) | `c = α·c_f + (1 − α)·c_b`. α = the fraction of the pixel covered by the foreground. α = 1 replaces the background, α = 0 leaves it |
| Why it is safe (slide 46) | the weights sum to 1, so if foreground and background have the same colour, the result doesn't change |
| Worked example *(mine)* | α = 0.25, red `(255,0,0)` over blue `(0,0,255)` gives `(63.75, 0, 191.25)` |
| IEEE division rules (slide 27), a > 0 | `+a/(+∞) = +0`, `−a/(+∞) = −0`, `+a/(−∞) = −0`, `−a/(−∞) = +0`. `0/0 = NaN` |
| Also IEEE *(mine)* | `+a/(+0) = +∞`, `−a/(+0) = −∞`. Any arithmetic with NaN gives NaN |
| Raster size *(mine)* | 8-bit RGB needs `W × H × 3` bytes. 1920 × 1080 → 6,220,800 bytes ≈ 6.2 MB |
| Homogeneous point | `(x, y, z, 1)`, transformed by a 4×4 matrix (more in L16) |

### Raster vs vector (slides 33–35, 41–43)

| | Raster (bitmap) | Vector |
|---|---|---|
| Stores | a colour value for every pixel on a grid | descriptions of shapes: the instructions, not the pixels |
| Enlarging | gets blocky or blurry | stays sharp (resolution independent) |
| Display | drives the screen pixels directly | must be **rasterized** first |
| Typical use | photographs | logos, diagrams, text |
| Practice code | Pillow `ImageDraw` → PNG | `svgwrite` → SVG |

### Emissive vs transmissive

**Emissive** pixels make their own light (LED, OLED). **Transmissive** pixels filter a backlight (LCD).
Exam bait: an LCD needs a backlight and two polarizers, and the liquid crystal only *rotates* polarization.
It does not emit light.

## Things that are wrong or loose in the deck

- **Slide 21: "CAD/CAM stands design and manufacturing."** Words are missing: it stands for
  **computer-aided design / computer-aided manufacturing**.
- **"Pipeline" means two different things.** Slide 9's "3D graphics pipeline" is the *production workflow*
  (modeling → animation → rendering). Slides 24–25's "graphics pipeline" is the *hardware rendering
  pipeline* (vertices → screen positions → shaded, depth-tested pixels). Don't mix them in an answer.
- **Slide 33 has a margin note pasted into a sentence:** "A common Pixel is short for 'picture element.'
  example is a flat-panel computer display…". Read it as two sentences: a pixel is a "picture element", and
  a common example of a raster display is a flat-panel screen.
- **The two practice drawings are not the same picture.** The SVG rectangle is 200 px wide (x 50–250),
  the Pillow one 150 px (x 50–200), and Pillow's default font is much smaller than the SVG's 20 px text.
  So don't read slides 49 and 51 as the same image in two formats.

## Links to other lectures

- **L6**: an image as a sampled 2D array. Slide 33's raster image is the same object.
- **L13**: JPEG vs PNG (slide 47 here).
- **L14**: displays and CRT scanning. Slides 36–40 are the modern flat-panel side.
- **L16**: geometric transformations. Slides 25 and 30–31 (homogeneous coordinates, the 4×4 `transform`
  class) are what L16 uses for translation and rotation.
