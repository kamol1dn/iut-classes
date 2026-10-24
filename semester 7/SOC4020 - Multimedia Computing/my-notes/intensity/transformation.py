import cv2
import numpy as np
img = cv2.imread('image.png')  # Read the image in grayscale

for gamma in [0.1, 0.5, 1.2, 2.2]:

    gamma_corrected = np.array(255*(img/255)**gamma, dtype = 'uint8')

    cv2.imwrite ('gamma_transformed'+str(gamma)+ '.jpg', gamma_corrected)

