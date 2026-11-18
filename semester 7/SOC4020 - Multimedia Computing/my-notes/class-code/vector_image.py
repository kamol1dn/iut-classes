import svgwrite

# Create an SVG drawing object
svg = svgwrite.Drawing("vector_image.svg", size=("400px", "400px"))

# Add a rectangle (x, y, width, height)
svg.add(svg.rect(insert=(50, 50), size=("200px", "100px"),
                 fill="blue", stroke="black", stroke_width=3))

# Add a circle (center x, center y, radius)
svg.add(svg.circle(center=(300, 150), r=50, fill="red",
                   stroke="black", stroke_width=2))

# Add a line (start x, start y, end x, end y)
svg.add(svg.line(start=(50, 300), end=(350, 300), stroke="green",
                 stroke_width=4))

# Add some text
svg.add(svg.text("Vector Image Example", insert=(100, 380),
                 fill="black", font_size="20px"))

# Save the drawing to a file
svg.save()

print("Vector image saved as vector_image.svg")
