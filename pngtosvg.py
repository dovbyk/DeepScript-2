#converts png to bmp and bmp to svgs

import os
from PIL import Image
import subprocess

# Directories
input_directory = "segmented_chars"  # Directory containing the PNG files
bmp_directory = "bmp_output"  # Directory to save intermediate BMP files
svg_directory = "svg_output"  # Directory to save the SVG files

# Create output directories if they don't exist
os.makedirs(bmp_directory, exist_ok=True)
os.makedirs(svg_directory, exist_ok=True)

# Function to convert PNG to BMP
def convert_png_to_bmp(input_path, output_path):
    # Open the PNG image
    img = Image.open(input_path).convert("L")  # Convert to grayscale
    img = img.point(lambda p: 255 if p > 128 else 0)  # Binarize (black and white)
    img.save(output_path, format="BMP")
    print(f"Converted to BMP: {output_path}")

# Function to convert BMP to SVG using Potrace
def convert_bmp_to_svg(bmp_path, svg_path):
    command = ["potrace", bmp_path, "-s", "-o", svg_path]
    subprocess.run(command, check=True)
    print(f"Converted to SVG: {svg_path}")

# Process each PNG file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".png"):
        png_path = os.path.join(input_directory, file_name)
        
        # Convert PNG to BMP
        bmp_file_name = os.path.splitext(file_name)[0] + ".bmp"
        bmp_path = os.path.join(bmp_directory, bmp_file_name)
        convert_png_to_bmp(png_path, bmp_path)
        
        # Convert BMP to SVG using Potrace
        svg_file_name = os.path.splitext(file_name)[0] + ".svg"
        svg_path = os.path.join(svg_directory, svg_file_name)
        convert_bmp_to_svg(bmp_path, svg_path)
