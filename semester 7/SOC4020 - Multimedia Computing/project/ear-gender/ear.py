"""Ear detection + male/female ear classification.

Pipeline for one image (BGR, as OpenCV loads it):
  1. Ear detector: Viola-Jones Haar cascades (left ear + right ear). They are
     evaluated fast with an integral image, the same idea as the board example.
  2. Each ear is cropped and resized to 224x224.
  3. MobileNetV2 (pretrained on ImageNet) turns the crop into 1280 numbers
     (a "feature vector") that describe its shape and texture.
  4. Logistic regression, trained by train.py on EarVN1.0, turns those 1280
     numbers into P(female). Above 0.5 -> Female, otherwise Male.

Command line:
  python ear.py photo.jpg          -> detect ears, print result, save photo_result.jpg
  python ear.py ear_crop.jpg --crop -> the photo is already a cropped ear, just classify it
"""
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).parent
MODELS = HERE / "models"

LABELS = ["Male", "Female"]
COLORS = {"Male": (255, 160, 40), "Female": (180, 80, 255)}  # BGR

# ImageNet normalisation that MobileNetV2 was trained with (RGB order).
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
FEATURE_LAYER = None  # filled in on load: the global-average-pool output (1280 values)


# ---------------------------------------------------------------- features
class FeatureExtractor:
    """MobileNetV2 without its last layer: image -> 1280-d feature vector."""

    def __init__(self):
        self.net = cv2.dnn.readNetFromONNX(str(MODELS / "mobilenetv2-12.onnx"))
        # The network ends GlobalAveragePool -> Reshape -> Gemm (1000 ImageNet
        # classes). We stop at the pooled 1280-d vector before the classifier:
        # OpenCV 4 asks for it by layer name, OpenCV 5 by tensor name ("464" in this
        # file, checked with the onnx package), so try both once.
        dummy = np.zeros((1, 3, 224, 224), np.float32)
        for name in ("onnx_node!GlobalAveragePool_97", "464"):
            try:
                self.net.setInput(dummy)
                self.net.forward(name)
                self.layer = name
                break
            except cv2.error:
                continue
        else:
            raise RuntimeError("Could not find MobileNetV2's pooling layer")

    @staticmethod
    def preprocess(bgr_images):
        batch = []
        for img in bgr_images:
            rgb = cv2.cvtColor(cv2.resize(img, (224, 224)), cv2.COLOR_BGR2RGB)
            x = (rgb.astype(np.float32) / 255.0 - IMAGENET_MEAN) / IMAGENET_STD
            batch.append(x.transpose(2, 0, 1))      # HWC -> CHW
        return np.stack(batch)                       # N x 3 x 224 x 224

    def __call__(self, bgr_images):
        # One image per forward pass: OpenCV 4's ONNX loader fixes the batch
        # size at 1 inside this model's Reshape node.
        feats = []
        for x in self.preprocess(bgr_images):
            self.net.setInput(x[None])
            feats.append(self.net.forward(self.layer).reshape(-1))
        return np.stack(feats)                       # N x 1280


# ---------------------------------------------------------------- classifier
class EarGenderClassifier:
    """Logistic regression stored as plain numbers in models/ear_gender.npz."""

    def __init__(self):
        path = MODELS / "ear_gender.npz"
        if not path.exists():
            raise FileNotFoundError("models/ear_gender.npz missing. Run: python train.py")
        w = np.load(path)
        self.mean, self.std = w["mean"], w["std"]
        self.coef, self.bias = w["coef"], float(w["bias"])
        self.features = FeatureExtractor()

    def p_female(self, bgr_crops):
        f = (self.features(bgr_crops) - self.mean) / self.std
        z = f @ self.coef + self.bias
        return 1.0 / (1.0 + np.exp(-z))

    def classify(self, bgr_crop):
        """Return (label, confidence) for one ear crop."""
        # Average the crop and its mirror image: a left ear flipped looks like a
        # right ear, so this makes the answer the same for either side.
        p = float(np.mean(self.p_female([bgr_crop, cv2.flip(bgr_crop, 1)])))
        return ("Female", p) if p >= 0.5 else ("Male", 1 - p)


# ---------------------------------------------------------------- detector
class EarDetector:
    def __init__(self):
        self.cascades = []
        for name in ("haarcascade_mcs_leftear.xml", "haarcascade_mcs_rightear.xml"):
            c = cv2.CascadeClassifier(str(MODELS / name))
            if c.empty():
                raise FileNotFoundError(f"models/{name} missing. Run: python download_models.py")
            self.cascades.append(c)

    def find_ears(self, bgr, min_size=40):
        gray = cv2.equalizeHist(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY))
        boxes, scores = [], []
        for c in self.cascades:
            found, _, weights = c.detectMultiScale3(
                gray, scaleFactor=1.05, minNeighbors=4, minSize=(min_size // 2, min_size),
                outputRejectLevels=True)
            for (x, y, w, h), s in zip(found, np.ravel(weights) if len(found) else []):
                boxes.append([int(x), int(y), int(w), int(h)])
                scores.append(float(s))
        if not boxes:
            return []
        # The two cascades often fire on the same ear: keep the strongest box.
        # (Cascade weights can be negative; NMSBoxes wants scores >= 0, so shift them.)
        low = min(scores)
        scores = [s - low + 1e-3 for s in scores]
        keep = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=0.0, nms_threshold=0.3)
        out = []
        for i in np.ravel(keep):
            x, y, w, h = boxes[i]
            out.append((x, y, x + w, y + h))
        return out


def crop(img, box, margin=0.15):
    h, w = img.shape[:2]
    x1, y1, x2, y2 = box
    mx, my = int((x2 - x1) * margin), int((y2 - y1) * margin)
    return img[max(0, y1 - my):min(h, y2 + my), max(0, x1 - mx):min(w, x2 + mx)]


def draw(img, box, label, p):
    x1, y1, x2, y2 = box
    color = COLORS[label]
    thickness = max(2, img.shape[1] // 400)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    text = f"{label} ear {p * 100:.0f}%"
    scale = max(0.5, (x2 - x1) / 160)
    (tw, th), base = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
    ty = y1 - 8 if y1 - th - 12 > 0 else y2 + th + 8
    cv2.rectangle(img, (x1, ty - th - 6), (x1 + tw + 8, ty + base), color, -1)
    cv2.putText(img, text, (x1 + 4, ty - 2), cv2.FONT_HERSHEY_SIMPLEX, scale,
                (255, 255, 255), 2, cv2.LINE_AA)


class EarGenderPipeline:
    def __init__(self):
        self.detector = EarDetector()
        self.classifier = EarGenderClassifier()

    def analyse(self, img):
        """Detect and classify every ear. Returns (annotated_copy, [(label, p, box)])."""
        out = img.copy()
        results = []
        for box in self.detector.find_ears(img):
            label, p = self.classifier.classify(crop(img, box))
            results.append((label, p, box))
            draw(out, box, label, p)
        return out, results


def read_image(path):
    # imdecode handles non-ASCII Windows paths, unlike imread.
    return cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return
    path = Path(args[0])
    img = read_image(path)
    if img is None:
        sys.exit(f"Could not read {path}")
    if "--crop" in sys.argv:
        label, p = EarGenderClassifier().classify(img)
        print(f"{label} ear ({p * 100:.1f}%)")
        return
    out, results = EarGenderPipeline().analyse(img)
    if not results:
        print("No ear found. Try a side (profile) photo, or --crop if it is already an ear.")
    for i, (label, p, box) in enumerate(results, 1):
        print(f"ear {i}: {label} ({p * 100:.1f}%) at {box}")
    save = path.with_name(path.stem + "_result.jpg")
    cv2.imencode(".jpg", out)[1].tofile(str(save))
    print(f"saved {save}")


if __name__ == "__main__":
    main()
