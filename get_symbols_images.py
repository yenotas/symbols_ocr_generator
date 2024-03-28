import sys
sys.path.append('/content/symbols_ocr_generator')

import random

from fontTools.ttLib import TTFont
import numpy as np
from PIL import Image as PilImage, ImageFont, ImageDraw
from symbols import symbols
import os
from config import path_to_fonts, output_dir, cover_size

all_codes = symbols.values()
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

fonts = [(os.path.join(path_to_fonts, font), font.split('.')[-2]) for font in os.listdir(path_to_fonts)]


def generateOneSymbolImage(code):
    """
    Отрисовка случайно сдвинутого, масштабированного, повернутого, символа
    в квадрате стороной size со случайным шумом
    :param code: int, код символа в unicode
    :return: Image
    """
    symbol = chr(code)

    angle = -random.randint(0,50)/10
    noise_power = random.randint(0,50)
    font_path, _ = random.choice(fonts)
    print(font_path)
    is_empty = True
    while is_empty:
        dx = random.randint(-4, 4)
        dy = random.randint(-4, 4)
        font_size = cover_size - random.randint(0, 4)
        font = ImageFont.truetype(font_path, size=font_size)
        symbol_img = PilImage.new('L', (cover_size, cover_size), color=0)
        imgDraw = ImageDraw.Draw(symbol_img)
        symbol_w, text_height = imgDraw.textbbox((0, 0), symbol, font=font)[2:4]

        canvas = PilImage.new('L', (cover_size, cover_size), color=0)

        x = (cover_size - symbol_w) // 2 + dx
        y = (cover_size - text_height) // 2 + dy
        imgDraw = ImageDraw.Draw(canvas)
        imgDraw.text((x, y), symbol, fill=255, font=font)

        img_array = np.array(canvas)
        is_empty = np.all(img_array == 0)
        if not is_empty:
            return canvas


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

    symbols_arr = []
    for dx in range(-3, 4):
        for dy in range(-3, 4):

            canvas = PilImage.new('L', (size, size), color=0)

            x = (size - symbol_w) // 2 + dx
            y = (size - text_height) // 2 + dy  # + size * k
            imgDraw = ImageDraw.Draw(canvas)
            imgDraw.text((x, y), symbol, fill=255, font=font)

            img_array = np.array(canvas)
            is_empty = np.all(img_array == 0)
            if is_empty:
                continue

            filename = os.path.splitext(os.path.basename(font_path))[0]
            filename = f"{filename}_{str(code)}_{dx}_{dy}.png"
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


def ciclicGenerateClearSymbolImages():
    for symbol, code in symbols.items():
        target_folder = os.path.join(output_dir, str(code))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        print('======================================\n', code, '\n======================================')
        for font_path, font_name in fonts:
            for file_name, glyph_img in drawSymbolImage(code, font_path, cover_size):
                png_filename = os.path.join(target_folder, file_name)
                glyph_img.save(png_filename)
