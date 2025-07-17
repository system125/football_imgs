import cv2
import numpy as np

# Load image
img = cv2.imread('img.png')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, threshold1=200,threshold2=255)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a blank white image
outline = np.ones_like(img) * 255  # white background

# Draw contours (black lines)
cv2.drawContours(outline, contours, -1, (0, 0, 0), thickness=1)

# Save the result
cv2.imwrite('logo_outline.png', outline)
