from svgpathtools import parse_path
import xml.etree.ElementTree as ET
import os

SVG_FILE = "numbers.svg"
OUTPUT_DIR = "numbersvg"
os.makedirs(OUTPUT_DIR, exist_ok=True)

tree = ET.parse(SVG_FILE)
root = tree.getroot()
SVG_NS = {'svg': 'http://www.w3.org/2000/svg'}

viewBox = root.attrib.get('viewBox')
if viewBox:
    min_x, min_y, width, height = map(float, viewBox.split())
else:
    width = float(root.attrib['width'])
    height = float(root.attrib['height'])
    min_x = min_y = 0

glyph_count = 10  # For digits 0-9
glyph_width = width / glyph_count
digits = [1,2,3,4,5,6,7,8,9,0]  # Output order: 1-9,0

# Helper: get bounding box of a path
def path_bbox(d):
    path = parse_path(d)
    try:
        xmin, xmax, ymin, ymax = path.bbox()
        return xmin, ymin, xmax, ymax
    except Exception as e:
        print(f"Error parsing path: {e}")
        return None

# Find all <path> elements (recursively)
all_paths = []
for elem in root.iter():
    if elem.tag.endswith('path'):
        d = elem.attrib.get('d')
        if d:
            bbox = path_bbox(d)
            all_paths.append((elem, bbox))

print(f"Found {len(all_paths)} path elements.")

for i, digit in enumerate(digits):
    x0 = min_x + i * glyph_width
    x1 = x0 + glyph_width
    digit_paths = []
    for elem, bbox in all_paths:
        if bbox is None:
            continue
        bx0, by0, bx1, by1 = bbox
        # If the path's bbox overlaps this digit's slice, include it
        if bx1 > x0 and bx0 < x1:
            digit_paths.append(elem)
    if not digit_paths:
        print(f"No paths found for digit {digit} (slice x={x0}-{x1})")
        continue
    # Build SVG
    digit_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {min_y} {glyph_width} {height}">
{''.join(ET.tostring(e, encoding='unicode') for e in digit_paths)}
</svg>'''
    with open(os.path.join(OUTPUT_DIR, f"{digit}.svg"), "w", encoding="utf-8") as f:
        f.write(digit_svg)
    print(f"Wrote {digit}.svg with {len(digit_paths)} paths.")