from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import os

"""
читает папку шрифтов и создает папки с svg каждого символа

"""


def extract_and_save_glyphs_as_svg(font_file, fonts_path, output_dir):
    font_path = os.path.join(fonts_path, font_file)
    font = TTFont(font_path)
    print('======================================\n', font_file, '\n======================================')
    glyph_set = font.getGlyphSet()
    unitsPerEm = font['head'].unitsPerEm
    shift = unitsPerEm - abs(font['hhea'].descender)  # из высоты вычитаю величину базовой линии
    cmap = font.getBestCmap()

    for unicode_val, glyph_name in cmap.items():
        if not unicode_val in all_codes:
            continue
        svg_pen = SVGPathPen(glyph_set)
        glyph = glyph_set[glyph_name]
        glyph.draw(svg_pen)
        svg_path_data = svg_pen.getCommands()
        transform = f"scale(1, -1) translate(0, -{shift})"
        if svg_path_data:
            svg_filename = os.path.join(output_dir, f"{font_file.replace('.ttf', '')}_{unicode_val}.svg")
            print(glyph_name, unicode_val, chr(unicode_val))
            with open(svg_filename, 'w', encoding='utf-8') as svg_file:
                svg_file.write(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {glyph.width} {unitsPerEm}'><path transform='{transform}' d='{svg_path_data}'/></svg>")


symbols = {'!': 33, '"': 34, '#': 35, '$': 36, '%': 37, '&': 38, "'": 39, '(': 40, ')': 41, '*': 42, '+': 43, ',': 44, '-': 45, '.': 46, '/': 47, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57, ':': 58, ';': 59, '<': 60, '=': 61, '>': 62, '?': 63, '@': 64, '[': 91, '\\': 92, ']': 93, '^': 94, '_': 95, '{': 123, '|': 124, '}': 125, '§': 167, '©': 169, '«': 171, '»': 187, 'Ё': 1025, 'І': 1030, 'А': 1040, 'Б': 1041, 'В': 1042, 'Г': 1043, 'Д': 1044, 'Е': 1045, 'Ж': 1046, 'З': 1047, 'И': 1048, 'Й': 1049, 'К': 1050, 'Л': 1051, 'М': 1052, 'Н': 1053, 'О': 1054, 'П': 1055, 'Р': 1056, 'С': 1057, 'Т': 1058, 'У': 1059, 'Ф': 1060, 'Х': 1061, 'Ц': 1062, 'Ч': 1063, 'Ш': 1064, 'Щ': 1065, 'Ъ': 1066, 'Ы': 1067, 'Ь': 1068, 'Э': 1069, 'Ю': 1070, 'Я': 1071, 'а': 1072, 'б': 1073, 'в': 1074, 'г': 1075, 'д': 1076, 'е': 1077, 'ж': 1078, 'з': 1079, 'и': 1080, 'й': 1081, 'к': 1082, 'л': 1083, 'м': 1084, 'н': 1085, 'о': 1086, 'п': 1087, 'р': 1088, 'с': 1089, 'т': 1090, 'у': 1091, 'ф': 1092, 'х': 1093, 'ц': 1094, 'ч': 1095, 'ш': 1096, 'щ': 1097, 'ъ': 1098, 'ы': 1099, 'ь': 1100, 'э': 1101, 'ю': 1102, 'я': 1103, 'ё': 1105, 'і': 1110, 'Ғ': 1170, 'ғ': 1171, 'Қ': 1178, 'қ': 1179, 'Ң': 1186, 'ң': 1187, 'Ү': 1198, 'ү': 1199, 'Ұ': 1200, 'ұ': 1201, 'Һ': 1210, 'һ': 1211, 'Ә': 1240, 'ә': 1241, 'Ө': 1256, 'ө': 1257, '‐': 8208, '‑': 8209, '–': 8211, '—': 8212, '‘': 8216, '’': 8217, '“': 8220, '”': 8221, '…': 8230, '‰': 8240, '€': 8364, 'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90, 'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109, 'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122}
all_codes = symbols.values()
path_to_fonts = 'arh_all_fonts'
output_dir = 'svg_symbols'

fonts = [(os.path.join(path_to_fonts, font), font.split('.')[-2]) for font in os.listdir(path_to_fonts)]
for font_path, font_name in fonts:
    print('======================================\n', font_name, '\n======================================')
    target_folder = os.path.join(output_dir, font_path).replace('.ttf', '')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(font_path)
        extract_and_save_glyphs_as_svg(font_path, path_to_fonts, target_folder)
