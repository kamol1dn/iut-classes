# L1 — Introduction to Multimedia Computing

**SOC4020 · Week 1 · 69 slides · Dr. Minhaz Uddin Ahmed**
Source: [week01 - Multimedia Computing L1.pptx](week01%20-%20Multimedia%20Computing%20L1.pptx)

A survey lecture — very broad, light on depth. The examinable content is the
**definitions and the taxonomies**; most of the middle is application
screenshots with no text.

---

## 🔴 Course admin — differs from eClass

### Grading, as given on slide 3

| Item | Weight |
|---|---|
| Mid-term exam | 30% |
| Final exam | 30% |
| Assignment | 15% |
| **Quiz** | **20%** |
| Attendance | 5% |
| **+ class activity** | **10%** |

> Note that sums to **110%**, so the 10% class activity is presumably bonus on
> top of a 100% base — eClass lists the same first five items totalling 100%
> and no class-activity line. Worth confirming, but either way **participating
> in class is worth marks here**, which is unusual among your courses.

**Assignments are Python programming.** Stated explicitly on the same slide.

### His weekly plan vs eClass

The two diverge sharply after the midterm — his version drops most of the
compression material and adds **computer graphics and ray tracing**:

| Week | His deck | eClass syllabus |
|---|---|---|
| 1 | Introduction to multimedia computing | same |
| 2 | Audio: nature of sound, waveform, digitization | same |
| 3 | Audio: processing, compression, perceptual compression | same |
| 4 | Image data representation, physics of imaging, intensity transformation | same |
| 5 | Colour, feature extraction, **XYZ→RGB transform** | Colour, linear filter, geometric transformation |
| 6 | **Video: NTSC vs PAL, 3D camera model, video compression** | Gradient, non-linear filtering, frequency domain |
| 7 | **Image pattern classification** | Image compression: entropy coding |
| 8 | **Mid-Term Exam** | Image compression: lossless |
| 9 | **Computer graphics: raster images & devices** | Image compression: lossy, JPEG |
| 10 | **Computer graphics: ray tracing, ray-object intersection** | Video compression, MPEG |
| 11 | CV: applications, topics, recent research | same |
| 12 | CV: Canny, Harris, feature matching | same |
| 13 | CV: stereo, model fitting, segmentation | same |
| 14 | CV: recognition, classification, **generative AI in CV** | same |
| 15 | **Final Exam** | CV: recognition, probabilistic, generative AI |
| 16 | **Review class** | **Final Exam** |

⚠️ **The midterm is week 8 in his plan**, and the **final is week 15 with a
review class in week 16** — eClass puts the final in week 16. If you plan
around eClass you will be a week late. Ask in class which is right.

---

## 1. What multimedia is

**Definition:** media and content that uses a **combination of different content
forms**.

**The six components** — memorise this list:

1. **Text**
2. **Audio**
3. **Still images**
4. **Animation**
5. **Video**
6. **Interactivity**

**Everyday examples he gives:** a PowerPoint presentation (all media types, plus
interactive tools) · playing a video game (inherently interactive) · describing
a picture to a friend · reading a newspaper · videoconferencing · watching TV
or listening to radio — with TV being audio + video, where **channel surfing is
the interactivity**.

**History:** Edison's **phonograph, 1877** — the first device able to record
*and* reproduce sound.

## 2. The elements, one by one

**Text** — the most widely used and flexible means of presenting information on
screen. His point: like every design element, text can **either direct the
reader's attention or divert it**.

**Hypermedia** — introduced by **Ted Nelson**. Goes beyond text-only to include
graphics, images and especially the *continuous* media (sound and video), and
**links them together**. The **World Wide Web is the best example** of a
hypermedia application.

> Two names/dates likely to be asked: **Edison, 1877, phonograph** and
> **Ted Nelson, hypermedia**.

**Audio** — sound files, music tracks. Players: VLC, RealPlayer.

**Images** — a two-dimensional screen display, but also three-dimensional
things like a statue or hologram. Includes graphs, pie charts, paintings.
Formats: `.jpg`, `.png`, `.gif`.

**Video** — unedited material as originally filmed or recorded. Its advantage
is the capacity to **convey a great deal of information in the least amount of
time**, plus a personal element other media lack.

## 3. Digital image processing

**Why it's needed — three reasons:**

1. **Improvement of pictorial information for human perception**
2. **Image processing for autonomous machine application**
3. **Efficient storage and transmission**

**Three levels of processing** — this structure recurs all term:

| Level | Task | Example |
|---|---|---|
| **Low** | Signal cleanup | Noise removal, image sharpening |
| **Mid** | Finding structure | Object segmentation |
| **High** | Meaning | Scene understanding |

**Techniques for human perception:** noise filtering · content enhancement ·
contrast enhancement · deblurring · remote sensing. Illustrated with image
enhancement, **thresholding** and **edge detection**.

**Histograms** characterise an image's content and can be used to detect
specific objects or textures.

### Application domains he surveys

Astronomy (nebulae in visible vs infrared) · **ultrasound / sonography** —
high-frequency sound waves producing dynamic images of organs, tissue and blood
flow, based on **sonar** · industrial inspection, on the argument that human
operators are *expensive, slow and unreliable* · medical X-ray · law
enforcement (fingerprints, number plates) · **PCB inspection** — checking all
components are present and solder joints acceptable, using both conventional
and X-ray imaging · special effects and composites · remote sensing from
satellites.

## 4. Motion detection

**Definition:** sensing physical movement in a given area. Detected by
measuring **change in speed or vector** of an object.

**Goals:** identify moving objects · detect unusual activity patterns · compute
trajectories of moving objects.

**Applications:** indoor/outdoor security · real-time crime detection · traffic
monitoring. Many intelligent video analysis systems are built on it.

**Two approaches — likely exam question:**

| | **Change detection** | **Optical flow** |
|---|---|---|
| Method | Detect objects within a scene, track them across frames | Compute motion within a region, or the frame as a whole |
| Granularity | Object-level | Pixel/region-level |

## 5. Computer vision

**Definition:** the field of computer science that enables computers to **see,
identify and process images in the same way human vision does**, and then
provide appropriate output.

### Facial expression recognition

**Applications:** human-computer interaction · identity confirmation · emotion
recognition · access control.

**Challenges:** variation in **pose** · **age** · **lighting conditions** ·
**occlusion** · **face motion**.

### Human Action Recognition (HAR)

**What it is:** human physical body movement (running, walking, reading), and
interaction with the environment or objects for a purpose (using a computer,
taking a photograph).

**Applications:** security surveillance in airports and bus stations ·
content-based browsing, e.g. fast-forwarding to the next goal-scoring scene ·
assisting elderly or disabled people in hospitals · **video recycling** —
filtering harmful video content away from children.

**Challenges:** variation in pose · complex background · object scale ·
occlusion · camera motion · large amounts of unlabelled data · actions easily
misinterpreted.

### Traditional vs deep learning — the comparison to know

| **Traditional (hand-crafted features)** | **Deep learning** |
|---|---|
| Relies on human domain knowledge more than on data | Makes better use of large data |
| Feature design is **separate** from training the classifier | **Jointly learns** features and classifier, so their integration is optimal |
| Hand-crafted features with many parameters are hard to tune manually | Learns huge numbers of parameters automatically |
| Developing effective features for a new application is slow | Much faster to obtain representations for new applications |

His note on the slide adds that a shallow or linear classifier operating on raw
pixels simply cannot distinguish the classes — which is the argument for
learned representations.

### Other CV applications surveyed

Self-driving cars · robotic surgery and medical diagnosis · robots navigating
cluttered environments (chefs, farmers, assistants) · intelligent surveillance
and drones · indoor navigation · creation of art · social apps such as
Instagram filters · **3D reconstruction**, including real-time indoor scene
reconstruction · **augmented reality**.

## 6. Graph machine learning

The last third of the deck (slides 56–66) shifts to **graph ML**, organised by
the *level* the prediction happens at. Worth knowing as a taxonomy:

| Level | Example task |
|---|---|
| **Node-level** | Protein folding |
| **Edge-level** | Recommender systems · drug side-effect prediction · bio-medical link prediction |
| **Sub-graph level** | Traffic prediction — **road network as a graph**, where nodes are road segments, edges are connectivity, and the prediction is **estimated time of arrival**. Done with a GNN. |
| **Graph-level** | Drug discovery — antibiotics as small molecular graphs, with **nodes = atoms** and **edges = chemical bonds** |

This section is not in either syllabus version, so it's likely context rather
than examinable core — but the four levels with one example each is a cheap
thing to remember in case it appears.

---

## If you're revising this in 10 minutes

The **six components of multimedia** · **Edison 1877** and **Ted Nelson /
hypermedia / WWW** · the **three reasons for digital image processing** · the
**low/mid/high level** split with an example each · the **two motion-detection
approaches** · the **definition of computer vision** · and the
**traditional-vs-deep-learning table**. Everything else is illustration.
