import fontforge
import sys
from PIL import Image
import potrace

BW_LIMIT = 100 # value limit between black and white pixels
COLS = 7 # number of columns on a template page
LINS = 4 # number of lines
ROTATE = True # should the scanned page be rotated
PAD = 10 # Percentage of each glyph box that should be cropped out
SCALE = 15 # Scale factor
BASELINE = 37 * SCALE # baseline offset

# check that all arguments are provided
if len(sys.argv) < 4:
    print("Error: please provide two pages and a font name")
    exit(1)

# parse arguments
page1 = Image.open(sys.argv[1])
page2 = Image.open(sys.argv[2])
fontname = sys.argv[3]
pages = [page1, page2]

# returns a list of all chars between two characters
def chars(start, end):
    return list(map(chr, range(ord(start), ord(end) + 1)))

# transforms a potrace Point to a tuple
# also does some coordinate adjustment
def p(pt):
    return (pt.x * SCALE, pt.y * SCALE - BASELINE)

# all glyphs that can be found in the template file
glyph_names = iter(chars('a', 'z') + chars('A', 'Z') + ['.', '!', ',', '?'])

# create an empty font!
font = fontforge.font()

for page in pages:
    # process a template page:

    # crop margins
    page = page.crop((30, 35, page.width - 5, page.height - 5))
    # make each pixel perfect black/white
    page = page.point(lambda x: 0 if x < BW_LIMIT else 255)
    # rotate the page if needed
    if ROTATE:
        page = page.rotate(90, expand=True)

    # compute dimensions of a glyph box
    box_width = page.width / COLS
    box_height = page.height / LINS
    pad_hori = box_width * PAD / 100
    pad_vert = box_height * PAD / 100

    # process each glyph :
    for lin_no in range(LINS):
        for col_no in range(COLS):
            # find its name
            glyph_name = next(glyph_names)
            
            # crop the bounding box
            box_left = box_width * col_no
            box_top = box_height * lin_no
            box = (
                box_left              + pad_hori,
                box_top               + pad_vert,
                box_left + box_width  - pad_hori,
                box_top  + box_height - pad_vert
            )
            bitmap = page.crop(box).transpose(Image.Transpose.FLIP_TOP_BOTTOM) # the transposition is needed because the Y axis are in reverse directions
            # trace the glyph contours, and write them to the font
            curves = potrace.Bitmap(bitmap).trace()
            pen = font.createChar(ord(glyph_name)).glyphPen()
            for path in curves:
                pen.moveTo(p(path.start_point))
                for segment in path:
                    if not segment.is_corner:
                        pen.curveTo(p(segment.c1), p(segment.c2), p(segment.end_point))
                    else:
                        pen.lineTo(p(segment.c))
                        pen.lineTo(p(segment.end_point))
                pen.closePath()

# adjust caracter spacing
font.selection.all()
font.autoWidth(SCALE)
# set the name of the font
font.fontname = fontname
font.fullname = fontname
font.familyname = fontname
# and export it!
font.save(fontname + ".sfd")
font.generate(fontname + ".ttf")