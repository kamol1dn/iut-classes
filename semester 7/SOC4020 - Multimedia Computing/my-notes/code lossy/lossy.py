import cv2
import matplotlib.pyplot as plt

img = cv2.imread('bober.jpg')

# Step 2: Save the image with different JPEG quality levels
for quality in [90, 50, 10]:
    cv2.imwrite('compressed_image_' + str(quality) + '.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])

# Step 3: Read and display the compressed images
img_90 = cv2.imread('compressed_image_90.jpg')
img_50 = cv2.imread('compressed_image_50.jpg')
img_10 = cv2.imread('compressed_image_10.jpg')

images = [img, img_90, img_50, img_10]
titles = ['Original Image', 'JPEG Compressed 90% Quality', 'JPEG Compressed 50% Quality', 'JPEG Compressed 10% Quality']

plt.figure()
for i in range(4):
    plt.subplot(2, 2, i + 1)
    plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))  # OpenCV is BGR, matplotlib wants RGB
    plt.title(titles[i])
    plt.axis('off')
plt.show()

# Lower quality values result in more compression but also greater loss of image fidelity.
