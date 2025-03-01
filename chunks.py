import ffmpeg
import os

def get_duration(input_file):
    """Получаем длительность видео в секундах"""
    try:
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"Ошибка при получении длительности: {e.stderr.decode()}")
        return None

def split_and_convert_to_3gp(input_file, output_file_part1, output_file_part2):
    """Разделяем видео на две части и конвертируем в 3gp"""
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Файл {input_file} не найден!")
        
        # Получаем длительность видео
        duration = get_duration(input_file)
        if duration is None:
            return
        
        # Делим видео на две равные части
        split_point = duration / 2

        # Первая часть: от начала до split_point
        stream1 = ffmpeg.input(input_file, t=split_point)  # Ограничиваем длительность
        stream1 = ffmpeg.output(stream1, output_file_part1, format='3gp', vcodec='h263', acodec='aac', s='176x144', vb='200k')
        ffmpeg.run(stream1, quiet=True)

        # Вторая часть: от split_point до конца
        stream2 = ffmpeg.input(input_file, ss=split_point)  # Начинаем с точки разделения
        stream2 = ffmpeg.output(stream2, output_file_part2, format='3gp', vcodec='h263', acodec='aac', s='176x144', vb='200k')
        ffmpeg.run(stream2, quiet=True)

        print(f"Успешно разделено и сконвертировано:")
        print(f"Часть 1: {output_file_part1}")
        print(f"Часть 2: {output_file_part2}")

    except ffmpeg.Error as e:
        print(f"Ошибка при разделении или конвертации: {e.stderr.decode()}")
    except Exception as e:
        print(f"Ошибка: {e}")

def get_files_from_folder(folder="files"):
    """Получаем список файлов из папки files"""
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Создана папка '{folder}'. Поместите в неё видео-файлы и перезапустите программу.")
        return []
    
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    return files

def ensure_output_folder(output_folder="output_chunks"):
    """Создаём папку output, если её нет"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Создана папка '{output_folder}' для выходных файлов.")

def choose_file(files):
    """Пользователь выбирает файл из списка"""
    if not files:
        print("В папке 'files' нет файлов для разделения.")
        return None
    
    print("\nДоступные файлы в папке 'files':")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input("\nВведите номер файла для разделения: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print(f"Пожалуйста, выберите число от 1 до {len(files)}.")
        except ValueError:
            print("Введите корректное число!")

if __name__ == "__main__":
    # Получаем список файлов из папки files
    files = get_files_from_folder("files")
    
    # Если файлов нет, завершаем программу
    if not files:
        exit()

    # Создаём или проверяем папку output
    ensure_output_folder("output_chunks")

    # Пользователь выбирает файл
    chosen_file = choose_file(files)
    if chosen_file:
        # Формируем пути
        input_file = os.path.join("files", chosen_file)
        base_name = os.path.splitext(chosen_file)[0]  # Имя файла без расширения
        output_file_part1 = os.path.join("output_chunks", f"{base_name}_part1.3gp")
        output_file_part2 = os.path.join("output_chunks", f"{base_name}_part2.3gp")
        
        # Разделяем и конвертируем
        split_and_convert_to_3gp(input_file, output_file_part1, output_file_part2)