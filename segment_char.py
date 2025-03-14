import cv2
import os
import numpy as np

# Paths
input_image_path = "img4.jpeg"  # Path to your scanned input image
output_directory = "segmented_chars"  # Directory to save your segmented characters
output_image_with_boxes = "image_with_boxes.jpg"  # Optional file, you can keep it as it is

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Read the image
image = cv2.imread(input_image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocess the image
_, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

# Noise removal using morphological operations
kernel = np.ones((3, 3), np.uint8)
binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)  # Remove small noise
binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)  # Fill small gaps

# Find contours on the cleaned binary image
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extract bounding boxes from contours
bounding_boxes = [cv2.boundingRect(c) for c in contours]

# Function to merge close bounding boxes
def merge_close_boxes(boxes, proximity_threshold=20):
    merged_boxes = []
    for box in boxes:
        x, y, w, h = box
        merged = False
        for i in range(len(merged_boxes)):
            mx, my, mw, mh = merged_boxes[i]
            # Check if the boxes are close
            if not (x > mx + mw + proximity_threshold or mx > x + w + proximity_threshold or
                    y > my + mh + proximity_threshold or my > y + h + proximity_threshold):
                # Merge the boxes
                nx = min(x, mx)
                ny = min(y, my)
                nw = max(x + w, mx + mw) - nx
                nh = max(y + h, my + mh) - ny
                merged_boxes[i] = (nx, ny, nw, nh)
                merged = True
                break
        if not merged:
            merged_boxes.append(box)
    return merged_boxes

# Merge bounding boxes that are close to each other
merged_boxes = merge_close_boxes(bounding_boxes)

# Sort the merged bounding boxes top-to-bottom, left-to-right
sorted_boxes = sorted(merged_boxes, key=lambda b: (b[1], b[0]))

# Copy the input image to draw bounding boxes
image_with_boxes = image.copy()

# Process and save each character
for i, (x, y, w, h) in enumerate(sorted_boxes):
    # Filter out noise by setting a size threshold
    if w > 10 and h > 10:
        # Extract the character from the binary image
        char_image = binary_image[y:y + h, x:x + w]

        # Resize and pad the character to 28x28
        aspect_ratio = w / h
        if aspect_ratio > 1:  # Wider than tall
            new_width = 20
            new_height = int(20 / aspect_ratio)
        else:  # Taller than wide
            new_height = 20
            new_width = int(20 * aspect_ratio)
        
        resized_char = cv2.resize(char_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        padded_char = cv2.copyMakeBorder(
            resized_char,
            top=(28 - new_height) // 2,
            bottom=(28 - new_height) - (28 - new_height) // 2,
            left=(28 - new_width) // 2,
            right=(28 - new_width) - (28 - new_width) // 2,
            borderType=cv2.BORDER_CONSTANT,
            value=0
        )

        # Normalize the image to range [0, 1]
        normalized_char = padded_char / 255.0

        # Save the character as an individual image
        output_path = os.path.join(output_directory, f"character_{i}.png")
        cv2.imwrite(output_path, (normalized_char * 255).astype(np.uint8))  # Convert back to uint8
        print(f"Saved: {output_path}")

        # Draw bounding box on the image
        cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Save the image with bounding boxes
cv2.imwrite(output_image_with_boxes, image_with_boxes)
print(f"Image with bounding boxes saved to '{output_image_with_boxes}'.")
