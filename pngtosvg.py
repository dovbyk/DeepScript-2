#creates ttf file from svg file

import fontforge
import os
import psMat

# Paths
input_directory = "svg_output"
output_font_path = "CustomFont3.ttf"

# Character Mapping
glyph_map = {
    "A": "A.svg", "B": "B.svg", "C": "C.svg", "D": "D.svg",
    "E": "E.svg", "F": "F.svg", "G": "G.svg", "H": "H.svg",
    "I": "I.svg", "J": "J.svg", "K": "K.svg", "L": "L.svg",
    "M": "M.svg", "N": "N.svg", "O": "O.svg", "P": "P.svg",
    "Q": "Q.svg", "R": "R.svg", "S": "S.svg", "T": "T.svg",
    "U": "U.svg", "V": "V.svg", "W": "W.svg", "X": "X.svg",
    "Y": "Y.svg", "Z": "Z.svg",
    "a": "a.svg", "b": "b.svg", "c": "c.svg", "d": "d.svg",
    "e": "e.svg", "f": "f.svg", "g": "g.svg", "h": "h.svg",
    "i": "i.svg", "j": "j.svg", "k": "k.svg", "l": "l.svg",
    "m": "m.svg", "n": "n.svg", "o": "o.svg", "p": "p.svg",
    "q": "q.svg", "r": "r.svg", "s": "s.svg", "t": "t.svg",
    "u": "u.svg", "v": "v.svg", "w": "w.svg", "x": "x.svg",
    "y": "y.svg", "z": "z.svg"
}

# Define character sets
uppercase_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ascender_chars = set('bdfhklt')
descender_chars = set('gpqy')
regular_lowercase = set('aceimnorsuvwxz')

# Create a new font
font = fontforge.font()
font.familyname = "CustomFont"
font.fullname = "CustomFont Regular"
font.fontname = "CustomFont-Regular"

# Set font metrics
font.em = 1000
font.ascent = 800
font.descent = 200

def get_scale_factors(char, glyph_height, glyph_width):
    """Calculate appropriate scale factors based on character type."""
    if char in uppercase_chars or char in ascender_chars:
        height_target = 700
        width_target = 600
    elif char in descender_chars:
        # For descenders, we want the main body at x-height
        # but allow extra space below baseline
        height_target = 500  # This will be for the main body
        width_target = 500
    else:  # regular lowercase
        height_target = 500
        width_target = 500
    
    height_scale = height_target / glyph_height if glyph_height > 0 else 1
    width_scale = width_target / glyph_width if glyph_width > 0 else 1
    
    return min(height_scale, width_scale)

def position_glyph(glyph, char):
    """Position the glyph correctly relative to the baseline."""
    bbox = glyph.boundingBox()
    
    if char in descender_chars:
        # Calculate the main body height (assuming it's the top 2/3 of the glyph)
        main_body_height = (bbox[3] - bbox[1]) * 2/3
        
        # Position so the main body aligns with x-height and descender extends below
        baseline_shift = 200 - main_body_height  # 200: increase the value the descenders move upwards
    else:
        baseline_shift = 0
    
    matrix = psMat.translate(0, baseline_shift)
    glyph.transform(matrix)

# Add glyphs
for char, svg_file in glyph_map.items():
    svg_path = os.path.join(input_directory, svg_file)
    if not os.path.exists(svg_path):
        print(f"SVG file not found: {svg_path}. Skipping {char}.")
        continue

    # Create a glyph for the character
    glyph = font.createChar(ord(char), char)
    glyph.importOutlines(svg_path)

    # Get original dimensions
    bbox = glyph.boundingBox()
    glyph_width = bbox[2] - bbox[0]
    glyph_height = bbox[3] - bbox[1]

    # Calculate and apply appropriate scaling
    scale_factor = get_scale_factors(char, glyph_height, glyph_width)
    
    if char in descender_chars:
        # For descenders, apply a larger scale to allow for the descender
        scale_factor *= 1.5  # Adjust this value to control descender length
    
    glyph.transform(psMat.scale(scale_factor))

    # Position the glyph correctly
    position_glyph(glyph, char)

    # Set appropriate glyph width
    new_bbox = glyph.boundingBox()
    new_width = new_bbox[2] - new_bbox[0]
    glyph.width = int(new_width + 100)

# Set font-wide metrics
font.hhea_ascent = font.ascent
font.hhea_descent = -font.descent
font.os2_typoascent = font.ascent
font.os2_typodescent = -font.descent
font.os2_winascent = font.ascent
font.os2_windescent = font.descent
font.os2_xheight = 500

# Generate the font
font.generate(output_font_path)
print(f"Font saved as {output_font_path}")