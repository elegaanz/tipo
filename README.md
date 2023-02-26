# Tipo

A tool to built an OTF file from hand drawn fonts.

## Usage

- Print `template.pdf` (at a 95% scale)
- Draw glyphs by hand on it (with black ink)
- Scan the two pages as PNG or JPG files (in portrait orientation)
- Run the Python script with the two images and a font name as arguments
- You now have a font file with what you drew

## Dependencies

- FontForge, `pacman -Sy fontforge`
- Pillow, `pip install pillow`
- potracer, `pip install potracer`
- Python 3
- Inkscape

## Licence

WTFPL