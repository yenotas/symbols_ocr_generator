from fontTools.ttLib import TTFont
import numpy as np
from PIL import Image as PilImage, ImageFont, ImageDraw
import os


def drawSymbolImage(code, font_path, size, k=0.2):
    """
    Отрисовка символа в квадрате стороной size
    :param code: int, код символа в unicode
    :param font_path: str, полный путь к файлу
    :param size: int, размер фона
    :param k: коэффициент базовой линии
    :return: кортеж с именем файла и изображением

    """
    symbol = chr(code)
    font_size = size - 2
    font = ImageFont.truetype(font_path, size=font_size)
    symbol_img = PilImage.new('L', (size, size), color=0)
    imgDraw = ImageDraw.Draw(symbol_img)
    symbol_w, text_height = imgDraw.textbbox((0, 0), symbol, font=font)[2:4]

    # symbol_w, min_h, max_h, symbol_img = drawText(symbol, font_path, size)
    symbols_arr = []
    for dx in range(-3, 4):
        for dy in range(-3, 4):

            canvas = PilImage.new('L', (size, size), color=0)

            x = (size - symbol_w) // 2 + dx
            y = (size - text_height) // 2 + dy  # + size * k
            imgDraw = ImageDraw.Draw(canvas)
            imgDraw.text((x, y), symbol, fill=255, font=font)
            # canvas.paste(symbol_img, (x, dy), symbol_img)

            img_array = np.array(canvas)
            is_empty = np.all(img_array == 0)
            if is_empty:
                continue

            filename_without_extension = os.path.splitext(os.path.basename(font_path))[0]
            filename = f"{filename_without_extension}_{str(code)}_{dx}_{dy}.png"
            symbols_arr.append((filename, canvas))

    return symbols_arr


def drawText(s, font_path, size):
    font = ImageFont.truetype(font_path, size=size)
    bg = PilImage.new('L', (size+4, size+4), color=255)
    imgDraw = ImageDraw.Draw(bg)
    imgDraw.text((0, 0), s, fill=0, font=font)
    # Преобразование изображения в массив NumPy
    np_img = np.array(bg)
    # Определение границ текста на холсте
    rows = np.any(np_img < 235, axis=1)
    cols = np.any(np_img < 235, axis=0)

    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    # Обрезка холста по границам текста слева и справа
    trimmed_img = np_img[0:size, min_col:max_col + 1]
    h, w = trimmed_img.shape
    # Преобразование обрезанного изображения в целочисленный тип, затем в PIL Image
    trimmed_img = trimmed_img.astype(np.uint8)
    img = PilImage.fromarray(trimmed_img, mode='L')

    return w, min_row, max_row, img


def extractFontGlyphs(path, size):
    font = TTFont(path)
    unitsPerEm = font['head'].unitsPerEm
    ratio = abs(font['hhea'].descender) / unitsPerEm  # относительный коэффициент для базовой линии
    cmap = font.getBestCmap()
    glyphs = []
    for unicode_val, glyph_name in cmap.items():
        if unicode_val not in all_codes:
            continue
        glyphs.append(drawSymbolImage(unicode_val, path, size, ratio))
    return glyphs


def getFontNamesAndPaths(directory):
    font_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.ttf') or filename.endswith('.otf'):  # Проверка на расширение файла шрифта
            font_path = os.path.join(directory, filename)
            font = TTFont(font_path)
            name = ""
            for record in font['name'].names:
                if record.nameID == 4 and not name:  # nameID 4 - это полное название шрифта
                    if b'\000' in record.string:
                        name = record.string.decode('utf-16-be')
                    else:
                        name = record.string.decode('latin-1')
                    font_names.append((name, font_path))
                    break
    return font_names


symbols = {'!': 33, '"': 34, '#': 35, '$': 36, '%': 37, '&': 38, "'": 39, '(': 40, ')': 41, '*': 42, '+': 43,
           ',': 44, '-': 45, '.': 46, '/': 47, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54,
           '7': 55, '8': 56, '9': 57, ':': 58, ';': 59, '<': 60, '=': 61, '>': 62, '?': 63, '@': 64, '[': 91,
           '\\': 92, ']': 93, '^': 94, '_': 95, '{': 123, '|': 124, '}': 125, '§': 167, '©': 169, '«': 171,
           '»': 187, 'Ё': 1025, 'І': 1030, 'А': 1040, 'Б': 1041, 'В': 1042, 'Г': 1043, 'Д': 1044, 'Е': 1045,
           'Ж': 1046, 'З': 1047, 'И': 1048, 'Й': 1049, 'К': 1050, 'Л': 1051, 'М': 1052, 'Н': 1053, 'О': 1054,
           'П': 1055, 'Р': 1056, 'С': 1057, 'Т': 1058, 'У': 1059, 'Ф': 1060, 'Х': 1061, 'Ц': 1062, 'Ч': 1063,
           'Ш': 1064, 'Щ': 1065, 'Ъ': 1066, 'Ы': 1067, 'Ь': 1068, 'Э': 1069, 'Ю': 1070, 'Я': 1071, 'а': 1072,
           'б': 1073, 'в': 1074, 'г': 1075, 'д': 1076, 'е': 1077, 'ж': 1078, 'з': 1079, 'и': 1080, 'й': 1081,
           'к': 1082, 'л': 1083, 'м': 1084, 'н': 1085, 'о': 1086, 'п': 1087, 'р': 1088, 'с': 1089, 'т': 1090,
           'у': 1091, 'ф': 1092, 'х': 1093, 'ц': 1094, 'ч': 1095, 'ш': 1096, 'щ': 1097, 'ъ': 1098, 'ы': 1099,
           'ь': 1100, 'э': 1101, 'ю': 1102, 'я': 1103, 'ё': 1105, 'і': 1110, 'Ғ': 1170, 'ғ': 1171, 'Қ': 1178,
           'қ': 1179, 'Ң': 1186, 'ң': 1187, 'Ү': 1198, 'ү': 1199, 'Ұ': 1200, 'ұ': 1201, 'Һ': 1210, 'һ': 1211,
           'Ә': 1240, 'ә': 1241, 'Ө': 1256, 'ө': 1257, '‐': 8208, '‑': 8209, '–': 8211, '—': 8212, '‘': 8216,
           '’': 8217, '“': 8220, '”': 8221, '…': 8230, '‰': 8240, '€': 8364, 'A': 65, 'B': 66, 'C': 67, 'D': 68,
           'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79,
           'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90,
           'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105, 'j': 106,
           'k': 107, 'l': 108, 'm': 109, 'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116,
           'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122}
all_codes = symbols.values()
cover_size = 32
path_to_fonts = 'test_font'
output_dir = 'png_symbols'

fonts = [(os.path.join(path_to_fonts, font), font.split('.')[-2]) for font in os.listdir(path_to_fonts)]
for font_path, font_name in fonts:
    print('======================================\n', font_name, '\n======================================')
    target_folder = os.path.join(output_dir, font_name)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for code in symbols.values():
        for (file_name, glyph_img) in drawSymbolImage(code, font_path, cover_size):
            png_filename = os.path.join(target_folder, file_name)
            glyph_img.save(png_filename)


# fonts = [(os.path.join(path_to_fonts, font), font.split('.')[-2]) for font in os.listdir(path_to_fonts)]
# for symbol, symbol_num in symbols.items():
#     target_folder = os.path.join(output_dir, symbol_num)
#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)
#     print('======================================\n', symbol_num, '\n======================================')
#     for font_path, font_name in fonts:
