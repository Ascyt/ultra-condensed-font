import os
import svgutils.transform as sg
from string import ascii_lowercase, ascii_uppercase

SVG_DIR = "lettersvg"
UPPERCASE_SYMBOL = "uppercase-symbol.svg"  # This file is in root
OUTPUT_DIR = os.path.join(SVG_DIR, "uppercase")

def parse_length(val_str):
    if not val_str:
        return 0.0
    val_str = val_str.strip().lower()
    if val_str.endswith("px"):
        return float(val_str.replace("px", ""))
    if val_str.endswith("mm"):
        return float(val_str.replace("mm", "")) * (96/25.4)
    try:
        return float(val_str)
    except Exception:
        return 0.0

def get_svg_viewbox(svg_element):
    vb_str = svg_element.root.get("viewBox")
    if vb_str:
        try:
            parts = vb_str.strip().split()
            if len(parts) == 4:
                minx, miny, w, h = map(float, parts)
                return minx, miny, w, h
        except Exception:
            pass
    # Fallback: use width and height and assume minx/miny are 0
    w = parse_length(svg_element.width)
    h = parse_length(svg_element.height)
    return 0, 0, w, h

def combine_svgs(symbol_path, letter_path, output_path):
    try:
        # Load files
        symbol_svg = sg.fromfile(symbol_path)
        letter_svg = sg.fromfile(letter_path)
        
        # Get viewBox info: (minx, miny, width, height)
        symbol_minx, symbol_miny, symbol_w, symbol_h = get_svg_viewbox(symbol_svg)
        letter_minx, letter_miny, letter_w, letter_h = get_svg_viewbox(letter_svg)
        
        gap = 0  # No additional gap
        
        # The effective dimensions are the viewBox widths/heights.
        total_width = symbol_w + gap + letter_w
        total_height = max(symbol_h, letter_h)
        
        # Create a new SVG figure with combined dimensions.
        fig = sg.SVGFigure(f"{total_width}px", f"{total_height}px")
        fig.root.set("viewBox", f"0 0 {total_width} {total_height}")
        
        # Adjust symbol: shift it so its content starts at (0,0)
        symbol_root = symbol_svg.getroot()
        symbol_root.moveto(-symbol_minx, -symbol_miny)
        
        # Adjust letter: shift it so its content starts at (symbol_w + gap, 0)
        letter_root = letter_svg.getroot()
        letter_root.moveto(symbol_w + gap - letter_minx, -letter_miny)
        
        # Append both adjusted roots
        fig.append(symbol_root)
        fig.append(letter_root)
        
        fig.save(output_path)
        print(f"Created {output_path} (Symbol viewBox: {symbol_minx},{symbol_miny},{symbol_w},{symbol_h}; Letter viewBox: {letter_minx},{letter_miny},{letter_w},{letter_h}; Total: {total_width}x{total_height})")
    except Exception as e:
        print(f"Error combining {symbol_path} and {letter_path}: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for lc, uc in zip(ascii_lowercase, ascii_uppercase):
        letter_svg_path = os.path.join(SVG_DIR, f"{lc}.svg")
        symbol_path = os.path.join(SVG_DIR, UPPERCASE_SYMBOL)
        if not os.path.exists(symbol_path):
            print(f"Missing uppercase symbol in {SVG_DIR}. Using file from root: {UPPERCASE_SYMBOL}")
            if os.path.exists(UPPERCASE_SYMBOL):
                symbol_path = UPPERCASE_SYMBOL
            else:
                print(f"Also not found at: {UPPERCASE_SYMBOL}")
                continue
        output_svg_path = os.path.join(OUTPUT_DIR, f"{uc}.svg")
        if not os.path.exists(letter_svg_path):
            print(f"Missing letter SVG: {letter_svg_path}")
            continue
        combine_svgs(symbol_path, letter_svg_path, output_svg_path)

if __name__ == "__main__":
    main()
