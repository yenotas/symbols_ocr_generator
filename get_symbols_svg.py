import io
import cairosvg
from fontTools.ttLib import TTFont
from PIL import Image
from fontTools.pens.svgPathPen import SVGPathPen
import os
from symbols import symbols


"""
читает папку шрифтов и создает папки с svg каждого символа
"""


def getImageFromSVG(svg_code, size):
    png_bytes = cairosvg.svg2png(bytestring=svg_code.encode('utf-8'), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png_bytes))


def extractVariousGlyphs(font_file, unicode_val):
    font = TTFont(font_file)
    glyph_set = font.getGlyphSet()
    unitsPerEm = font['head'].unitsPerEm
    adding_size = abs(font['hhea'].descender)
    shift = unitsPerEm  # вычисляю величину базовой линии
    cmap = font.getBestCmap()
    glyph_name = cmap[unicode_val]
    svg_pen = SVGPathPen(glyph_set)
    glyph = glyph_set[glyph_name]
    glyph.draw(svg_pen)  # есть аттрибуты glyph.width
    square = unitsPerEm + adding_size
    print('shift', shift, 'glyph.width', glyph.width)
    svg_path_data = svg_pen.getCommands()
    transform = f"scale(1, -1) translate(0, {-shift})"
    if svg_path_data:
        return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {glyph.width} {square}'><path transform='{transform}' d='{svg_path_data}'/></svg>",
                f"<path transform='{transform}' d='{svg_path_data}'/></svg>")


def saveGlyphSVG(unicode, output_folder, fonts):
    """
    Сохранить глифы в формате SVG для кода {unicode} для всех шрифтов словаря {fonts}
    в папке {output_folder} под именем /{unicode}/{font_name}_{unicode}_.svg
    :param unicode: int
    :param output_folder: str
    :param fonts: [(font_path, font_name),..]
    :return:
    """
    target_folder = os.path.join(output_folder, str(unicode))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for font_path, font_name in fonts:
        print('======================================\n', font_name, '\n======================================')
        svg, _ = extractVariousGlyphs(font_path, unicode)
        svg_filename = os.path.join(target_folder, f"{font_name}_{unicode}.svg")
        with open(svg_filename, 'w', encoding='utf-8') as svg_file:
            svg_file.write(svg)


all_codes = list(symbols.values())
path_to_fonts = 'arh_all_fonts'
output_dir = 'svg_symbols'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

font_files = [(os.path.join(path_to_fonts, font), font.split('.')[-2]) for font in os.listdir(path_to_fonts)]
# for code in all_codes:
# saveGlyphSVG(code, output_dir, font_files)

font_path, font_name = font_files[100]
print('======================================\n', font_name, '\n======================================')
for code in [1025]:
    target_folder = os.path.join(output_dir, str(code))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    svg, _ = extractVariousGlyphs(font_path, code)
    img = getImageFromSVG(svg, 28)
    img.show()
    svg_filename = os.path.join(target_folder, f"{font_name}_{code}.svg")
    with open(svg_filename, 'w', encoding='utf-8') as svg_file:
        svg_file.write(svg)


