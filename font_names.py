from fontTools.ttLib import TTFont
import os

def get_font_names(directory):
    font_names = {}

    for filename in os.listdir(directory):
        if '(' in filename:
            os.remove(os.path.join(directory, filename))

    for filename in os.listdir(directory):
        if filename.endswith('.ttf') or filename.endswith('.otf'):  # Проверка на расширение файла шрифта
            try:
                font_path = os.path.join(directory, filename)
                if not '(' in font_path:
                    font = TTFont(font_path)
                    name = ""
                    for record in font['name'].names:
                        if record.nameID == 4 and not name:  # nameID 4 - это полное название шрифта
                            if b'\000' in record.string:
                                name = record.string.decode('utf-16-be')
                            else:
                                name = record.string.decode('latin-1')
                            font_names[filename] = name
                            break
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")
    return font_names


path_to_fonts = 'arh_all_fonts'
font_names = get_font_names(path_to_fonts)
print("Количество:", len(font_names))
print("Имена шрифтов:", font_names)
font_names_str = "\n".join(font_names)

with open('font_names.txt', 'w', encoding='utf-8') as file:
    file.write(font_names_str)
