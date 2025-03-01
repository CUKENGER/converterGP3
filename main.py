import ffmpeg
import os

def convert_to_3gp(input_file, output_file):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Файл {input_file} не найден!")
        
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, format='3gp', vcodec='h263', acodec='aac', s='176x144', vb='200k')
        ffmpeg.run(stream, quiet=True)
        print(f"Успешно сконвертировано в {output_file}")

    except ffmpeg.Error as e:
        print(f"Ошибка конвертации: {e.stderr.decode()}")
    except Exception as e:
        print(f"Ошибка: {e}")

def get_files_from_folder(folder="files"):
    # Проверяем, существует ли папка files
    if not os.path.exists(folder):
        os.makedirs(folder)  # Создаём папку, если её нет
        print(f"Создана папка '{folder}'. Поместите в неё видео-файлы и перезапустите программу.")
        return []
    
    # Получаем список всех файлов в папке files
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    return files

def ensure_output_folder(output_folder="output"):
    # Создаём папку output, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Создана папка '{output_folder}' для выходных файлов.")

def choose_file(files):
    if not files:
        print("В папке 'files' нет файлов для конвертации.")
        return None
    
    # Выводим список файлов с номерами
    print("\nДоступные файлы в папке 'files':")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    # Запрашиваем выбор пользователя
    while True:
        try:
            choice = int(input("\nВведите номер файла для конвертации: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]  # Возвращаем имя выбранного файла
            else:
                print(f"Пожалуйста, выберите число от 1 до {len(files)}.")
        except ValueError:
            print("Введите корректное число!")

if __name__ == "__main__":
    # Получаем список файлов из папки files
    files = get_files_from_folder("files")
    
    # Если файлов нет, программа завершается
    if not files:
        exit()

    # Убеждаемся, что папка output существует
    ensure_output_folder("output")

    # Пользователь выбирает файл
    chosen_file = choose_file(files)
    if chosen_file:
        # Формируем пути
        input_file = os.path.join("files", chosen_file)  # Путь к входному файлу
        output_file = os.path.join("output", os.path.splitext(chosen_file)[0] + ".3gp")  # Выходной файл в папке output
        
        # Запускаем конвертацию
        convert_to_3gp(input_file, output_file)