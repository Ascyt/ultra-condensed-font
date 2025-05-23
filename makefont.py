import fontforge
import os
import psMat
from string import ascii_uppercase, ascii_lowercase

FONT_NAME = "MySVGFont"
OUTPUT_FONT = "output_font.ttf"
SVG_DIR = "lettersvg"
MARGIN = 20 # Adjust for more/less spacing

font = fontforge.font()
font.fontname = FONT_NAME
font.familyname = FONT_NAME
font.fullname = FONT_NAME
font.em = 1000

for i, letter in enumerate(ascii_uppercase):
    svg_path = os.path.join(SVG_DIR, f"{letter}.svg")
    if not os.path.exists(svg_path):
        print(f"Missing {svg_path}")
        continue
    glyph = font.createChar(ord(letter))
    glyph.importOutlines(svg_path)
    bbox = glyph.boundingBox()
    glyph_left = bbox[0]
    glyph_right = bbox[2]
    glyph_width = glyph_right - glyph_left
    advance_width = glyph_width + 2 * MARGIN
    shift = (advance_width / 2) - ((glyph_left + glyph_right) / 2)
    glyph.transform(psMat.translate(shift, 0))
    glyph.width = int(advance_width)

for i, letter in enumerate(ascii_uppercase):
    lower = ascii_lowercase[i]
    lower_glyph = font.createChar(ord(lower))
    lower_glyph.addReference(letter)
    lower_glyph.width = font[letter].width  # <-- Fix: set width

# Add space glyph to prevent fallback in Word
space = font.createChar(ord(' '))
space.width = int(font['A'].width)  # Or set to your preferred width

font.generate(OUTPUT_FONT)
print(f"Font saved as {OUTPUT_FONT}")