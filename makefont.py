# "C:\Program Files (x86)\FontForgeBuilds\fontforge.bat" -script makefont.py

import fontforge
import os
import psMat
from string import ascii_uppercase, ascii_lowercase, digits

FONT_NAME = "MySVGFont"
OUTPUT_FONT = "output_font.ttf"
SVG_DIR = "lettersvg"
UPPERCASE_DIR = "lettersvg/uppercase"
NUMBER_DIR = "numbersvg"
MARGIN = 20 # Adjust for more/less spacing

font = fontforge.font()
font.fontname = FONT_NAME
font.familyname = FONT_NAME
font.fullname = FONT_NAME
font.em = 1000

# Uppercase: import from UPPERCASE_DIR
for i, letter in enumerate(ascii_uppercase):
    svg_path = os.path.join(UPPERCASE_DIR, f"{letter}.svg")
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

# Lowercase: import from SVG_DIR
for i, letter in enumerate(ascii_lowercase):
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

# Numbers: import from NUMBER_DIR
for i, digit in enumerate(digits):
    svg_path = os.path.join(NUMBER_DIR, f"{digit}.svg")
    if not os.path.exists(svg_path):
        print(f"Missing {svg_path}")
        continue
    glyph = font.createChar(ord(digit))
    glyph.importOutlines(svg_path)
    bbox = glyph.boundingBox()
    glyph_left = bbox[0]
    glyph_right = bbox[2]
    glyph_width = glyph_right - glyph_left
    advance_width = glyph_width + 2 * MARGIN
    shift = (advance_width / 2) - ((glyph_left + glyph_right) / 2)
    glyph.transform(psMat.translate(shift, 0))
    glyph.width = int(advance_width)

# Add space glyph to prevent fallback in Word
space = font.createChar(ord(' '))
if 'a' in font:
    space.width = int(font['a'].width)
else:
    space.width = 500

font.generate(OUTPUT_FONT)
print(f"Font saved as {OUTPUT_FONT}")