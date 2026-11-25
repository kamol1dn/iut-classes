"""Ear gender app: live webcam or an uploaded photo.

  python app.py

Buttons:
  Start camera   - live webcam. Turn your head sideways so the camera sees your ear.
  Upload image   - pick a photo; every ear found is labelled Male/Female ear.
  Guide box      - if the detector misses your ear, switch this on and hold
                   your ear inside the box: the box itself is classified.
  Close-up       - for uploads that are already a cropped ear photo.
  Save result    - save what is on screen.
"""
import tkinter as tk
from collections import deque
from tkinter import filedialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk

from ear import LABELS, EarGenderPipeline, crop, draw, read_image

VIEW_W, VIEW_H = 900, 600
SMOOTH_FRAMES = 10   # average the camera answer over this many frames
BG = "#1e1e1e"


class App:
    def __init__(self, root):
        self.root = root
        root.title("Ear Gender Detector - Multimedia Computing")
        root.configure(bg=BG)

        try:
            self.pipe = EarGenderPipeline()
        except FileNotFoundError as e:
            messagebox.showerror("Models missing", str(e))
            root.destroy()
            return

        bar = tk.Frame(root, bg=BG)
        bar.pack(fill="x", padx=10, pady=8)
        btn = dict(font=("Segoe UI", 11), padx=14, pady=4, relief="flat", bg="#3a3a3a",
                   fg="white", activebackground="#555", activeforeground="white")
        chk = dict(font=("Segoe UI", 10), bg=BG, fg="white", selectcolor="#333",
                   activebackground=BG, activeforeground="white")
        self.cam_btn = tk.Button(bar, text="Start camera", command=self.toggle_camera, **btn)
        self.cam_btn.pack(side="left", padx=4)
        tk.Button(bar, text="Upload image", command=self.upload, **btn).pack(side="left", padx=4)
        tk.Button(bar, text="Save result", command=self.save, **btn).pack(side="left", padx=4)
        self.guide = tk.BooleanVar(value=False)
        tk.Checkbutton(bar, text="Guide box (camera)", variable=self.guide,
                       command=self.history_reset, **chk).pack(side="left", padx=10)
        self.closeup = tk.BooleanVar(value=False)
        tk.Checkbutton(bar, text="Upload is an ear close-up", variable=self.closeup,
                       **chk).pack(side="left", padx=4)

        self.view = tk.Label(root, bg="black", width=VIEW_W, height=VIEW_H)
        self.view.pack(padx=10)
        self.status = tk.Label(root, text="Start the camera (turn sideways) or upload a photo of an ear.",
                               font=("Segoe UI", 14, "bold"), bg=BG, fg="white")
        self.status.pack(pady=10)

        self.cap = None
        self.current = None
        self.history = deque(maxlen=SMOOTH_FRAMES)   # recent P(female) of the main ear
        root.protocol("WM_DELETE_WINDOW", self.close)

    def history_reset(self):
        self.history.clear()

    # ---------------- camera ----------------
    def toggle_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = None
                messagebox.showerror("Camera", "Could not open the webcam.")
                return
            self.history.clear()
            self.cam_btn.config(text="Stop camera")
            self.camera_loop()
        else:
            self.stop_camera()

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.cam_btn.config(text="Start camera")

    def camera_loop(self):
        if self.cap is None:
            return
        ok, frame = self.cap.read()
        if ok:
            self.show_camera_frame(cv2.flip(frame, 1))   # mirror view
        self.root.after(15, self.camera_loop)

    def show_camera_frame(self, frame):
        out = frame.copy()
        h, w = frame.shape[:2]
        if self.guide.get():
            # Fixed box in the middle, ear-shaped (taller than wide).
            bh = int(h * 0.45); bw = int(bh * 0.65)
            boxes = [((w - bw) // 2, (h - bh) // 2, (w + bw) // 2, (h + bh) // 2)]
        else:
            boxes = self.pipe.detector.find_ears(frame)

        if not boxes:
            self.history.clear()
            self.set_status("No ear found - turn your head sideways, or tick Guide box", "#bbbbbb")
        else:
            boxes.sort(key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
            for i, box in enumerate(boxes):
                label, p = self.pipe.classifier.classify(crop(frame, box))
                if i == 0:
                    # Smooth the biggest ear's answer so the label does not flicker.
                    self.history.append(p if label == "Female" else 1 - p)
                    pf = float(np.mean(self.history))
                    label, p = ("Female", pf) if pf >= 0.5 else ("Male", 1 - pf)
                    self.announce(label, p, len(boxes))
                draw(out, box, label, p)
        self.display(out)

    # ---------------- upload ----------------
    def upload(self):
        path = filedialog.askopenfilename(
            title="Choose a photo",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All files", "*.*")])
        if not path:
            return
        self.stop_camera()
        img = read_image(path)
        if img is None:
            messagebox.showerror("Upload", "That file is not an image I can read.")
            return

        if self.closeup.get():
            label, p = self.pipe.classifier.classify(img)
            out = img.copy()
            draw(out, (0, 0, img.shape[1] - 1, img.shape[0] - 1), label, p)
            self.announce(label, p, 1)
            self.display(out)
            return

        out, results = self.pipe.analyse(img)
        if not results:
            self.set_status("No ear found. If the photo is already an ear, tick 'close-up' and upload again.",
                            "#ff6b6b")
        else:
            results.sort(key=lambda r: (r[2][2] - r[2][0]) * (r[2][3] - r[2][1]), reverse=True)
            label, p, _ = results[0]
            self.announce(label, p, len(results))
        self.display(out)

    # ---------------- helpers ----------------
    def announce(self, label, p, n):
        text = f"{label} ear  ({p * 100:.0f}% sure)"
        if n > 1:
            text += f"   ·   {n} ears, biggest shown here"
        self.set_status(text, "#40a0ff" if label == "Male" else "#ff50b4")

    def set_status(self, text, color):
        self.status.config(text=text, fg=color)

    def display(self, bgr):
        self.current = bgr
        h, w = bgr.shape[:2]
        s = min(VIEW_W / w, VIEW_H / h)
        rgb = cv2.cvtColor(cv2.resize(bgr, (max(1, int(w * s)), max(1, int(h * s)))),
                           cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(rgb))
        self.view.config(image=photo, width=VIEW_W, height=VIEW_H)
        self.view.image = photo   # keep a reference or Tk drops it

    def save(self):
        if self.current is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if path:
            ext = ".png" if path.lower().endswith(".png") else ".jpg"
            cv2.imencode(ext, self.current)[1].tofile(path)

    def close(self):
        self.stop_camera()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
