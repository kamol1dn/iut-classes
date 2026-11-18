# Practice code from the Multimedia Computing slide (segmentation lecture),
# copied as shown. Run make_billiard.py first if you don't have billiard.jpg.
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('billiard.jpg')
# Convert the image to grayscale
gray_image = image #cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Assume the background is a blank image or create a mask for background
# Create a static background for subtraction
# (Here, we'll use a blank gray background of the same size)
background = np.full_like(gray_image, 128)  # A gray background

# Perform background subtraction by taking the absolute difference
foreground = cv2.absdiff(gray_image, background)

# Threshold the foreground to get binary image (foreground mask)
_, foreground_mask = cv2.threshold(foreground, 30, 255, cv2.THRESH_BINARY)
# Display the original image, background, and foreground mask
plt.figure(figsize=(15,5))
plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.subplot(1, 3, 2)
plt.title('Background )')
plt.imshow(background, cmap='gray')

plt.subplot(1, 3, 3)
plt.title('Foreground Mask')
plt.imshow(foreground_mask, cmap='gray')
plt.savefig('background_subtraction_result.png')  # added so the result is kept
plt.show()
