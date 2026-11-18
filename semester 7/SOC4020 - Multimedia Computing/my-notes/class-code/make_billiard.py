import cv2
import numpy as np

# The slide reads 'billiard.jpg' but we don't have the professor's file,
# so this draws a stand-in pool table of about the same size (~640x540).
W, H = 640, 540
img = np.zeros((H, W, 3), np.uint8)

# Wooden rail (BGR colours)
img[:] = (30, 45, 110)

# Green felt with a bright spot in the middle, like a lamp over the table
x0, y0, x1, y1 = 35, 35, W - 35, H - 35
yy, xx = np.mgrid[y0:y1, x0:x1]
d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
light = np.clip(1.0 - 0.55 * d, 0, 1)
img[y0:y1, x0:x1, 0] = (40 * light).astype(np.uint8)
img[y0:y1, x0:x1, 1] = (110 + 120 * light).astype(np.uint8)
img[y0:y1, x0:x1, 2] = (50 + 60 * light).astype(np.uint8)

# Six pockets
for px, py in [(x0, y0), (W // 2, y0 - 5), (x1, y0), (x0, y1), (W // 2, y1 + 5), (x1, y1)]:
    cv2.circle(img, (px, py), 18, (15, 15, 15), -1)

# Cue stick and cue ball on the left
cv2.line(img, (40, 270), (190, 270), (120, 190, 230), 6)
cv2.circle(img, (210, 270), 9, (245, 245, 245), -1)

# Fifteen balls racked in a triangle on the right
colours = [(0, 215, 255), (255, 80, 0), (0, 0, 220), (130, 0, 120), (0, 120, 255),
           (0, 140, 0), (20, 20, 140), (10, 10, 10), (0, 215, 255), (255, 80, 0),
           (0, 0, 220), (130, 0, 120), (0, 120, 255), (0, 140, 0), (20, 20, 140)]
k = 0
for col in range(5):
    for row in range(col + 1):
        cx = 440 + col * 17
        cy = 270 - col * 9 + row * 18
        cv2.circle(img, (cx, cy), 9, colours[k], -1)
        cv2.circle(img, (cx, cy), 9, (230, 230, 230), 1)
        k += 1

cv2.imwrite('billiard.jpg', img)
print('Saved billiard.jpg', img.shape)
