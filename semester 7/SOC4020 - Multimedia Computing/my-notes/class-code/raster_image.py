from PIL import Image, ImageDraw

# Create a blank white image (width, height) with RGB mode
width, height = 400, 400
image = Image.new("RGB", (width, height), "white")

# Create a draw object
draw = ImageDraw.Draw(image)

# Draw a rectangle (top left corner, bottom right corner)
draw.rectangle([(50, 50), (200, 150)], outline="black", fill="blue", width=3)

# Draw an ellipse (bounding box for the ellipse)
draw.ellipse([(250, 100), (350, 200)], outline="black", fill="red", width=3)

# Draw a line (start point, end point)
draw.line([(50, 300), (350, 300)], fill="green", width=4)

# Draw text on the image
draw.text((100, 350), "Raster Image Example", fill="black")

# Save the image as a PNG file
image.save("raster_image.png")

print("Raster image saved as raster_image.png")
