"""Train the male/female ear classifier on EarVN1.0.

  python train.py

Steps:
  1. Read every ear photo in data/EarVN1.0 dataset/Images/. Folders 001-098 are
     the 98 men, 099-164 the 66 women (as in the dataset paper).
  2. MobileNetV2 turns each photo into a 1280-d feature vector (cached in
     data/features.npz, so the slow part runs once).
  3. Split by PERSON, not by photo: 20% of the people are never seen in
     training. Otherwise the model could "recognise" a person it has seen
     instead of judging the ear, and the accuracy would be inflated.
  4. Logistic regression on the features; report accuracy on the unseen people.
  5. Retrain on everyone and save models/ear_gender.npz for the app.
"""
import time
from pathlib import Path

import cv2
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler

from ear import MODELS, FeatureExtractor, read_image

HERE = Path(__file__).parent
IMAGES = HERE / "data" / "EarVN1.0 dataset" / "Images"
CACHE = HERE / "data" / "features.npz"
LAST_MALE = 98


def load_features():
    if CACHE.exists():
        d = np.load(CACHE)
        return d["X"], d["y"], d["groups"]

    files, y, groups = [], [], []
    for folder in sorted(IMAGES.iterdir()):
        person = int(folder.name.split(".")[0])
        for f in sorted(folder.glob("*.jpg")):
            files.append(f)
            y.append(0 if person <= LAST_MALE else 1)   # 0 = male, 1 = female
            groups.append(person)
    print(f"{len(files)} images, {len(set(groups))} people "
          f"({y.count(0)} male images, {y.count(1)} female images)")

    fx = FeatureExtractor()
    X = np.zeros((len(files), 1280), dtype=np.float32)
    t0, B = time.time(), 64
    for i in range(0, len(files), B):
        imgs = [read_image(f) for f in files[i:i + B]]
        X[i:i + len(imgs)] = fx(imgs)
        if (i // B) % 40 == 0:
            print(f"  features {i + len(imgs)}/{len(files)}  ({time.time() - t0:.0f}s)")
    y, groups = np.array(y), np.array(groups)
    np.savez_compressed(CACHE, X=X, y=y, groups=groups)
    return X, y, groups


def fit(X, y, C):
    scaler = StandardScaler().fit(X)
    clf = LogisticRegression(C=C, class_weight="balanced", max_iter=3000)
    clf.fit(scaler.transform(X), y)
    return scaler, clf


def main():
    X, y, groups = load_features()

    # 5-fold cross-validation, split by person. Each fold holds out ~33 people.
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
    best = None
    for C in (0.001, 0.01, 0.1):
        accs, people_accs = [], []
        all_true, all_pred = [], []
        for tr, te in cv.split(X, y, groups):
            scaler, clf = fit(X[tr], y[tr], C)
            pred = clf.predict(scaler.transform(X[te]))
            accs.append(np.mean(pred == y[te]))
            all_true += list(y[te]); all_pred += list(pred)
            # Per person: majority vote over all their ear photos.
            for g in np.unique(groups[te]):
                m = groups[te] == g
                people_accs.append(round(pred[m].mean()) == y[te][m][0])
        acc = np.mean(accs)
        print(f"C={C:<6} per-photo accuracy {acc * 100:.1f}% (+/- {np.std(accs) * 100:.1f}),"
              f" per-person (majority vote) {np.mean(people_accs) * 100:.1f}%")
        if best is None or acc > best[0]:
            best = (acc, C, all_true, all_pred)

    acc, C, t, p = best
    print(f"\nBest C={C}. Results on people the model never saw:")
    print(confusion_matrix(t, p))
    print(classification_report(t, p, target_names=["Male", "Female"], digits=3))

    scaler, clf = fit(X, y, C)
    np.savez(MODELS / "ear_gender.npz", mean=scaler.mean_.astype(np.float32),
             std=scaler.scale_.astype(np.float32), coef=clf.coef_[0].astype(np.float32),
             bias=np.float32(clf.intercept_[0]))
    print(f"saved {MODELS / 'ear_gender.npz'}")


if __name__ == "__main__":
    main()
