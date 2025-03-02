import ffmpeg
import os

def split_mp3(input_file, split_time, output1, output2):
    """
    Разделяет MP3 файл на две части в указанной точке времени
    
    Args:
        input_file (str): Путь к входному MP3 файлу
        split_time (str): Время разделения в формате "HH:MM:SS" или секунды "300"
        output1 (str): Путь к первому выходному файлу
        output2 (str): Путь ко второму выходному файлу
    """
    try:
        # Получаем длительность файла
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        
        # Первая часть: от начала до split_time
        stream1 = ffmpeg.input(input_file)
        stream1 = ffmpeg.output(
            stream1, 
            output1,
            t=split_time,  # длительность первой части
            acodec='copy', # копируем аудиокодек без перекодирования
            format='mp3'
        )
        
        # Вторая часть: от split_time до конца
        stream2 = ffmpeg.input(input_file, ss=split_time)  # ss - начальная точка
        stream2 = ffmpeg.output(
            stream2,
            output2,
            acodec='copy',
            format='mp3'
        )
        
        # Выполняем команды
        ffmpeg.run(stream1)
        ffmpeg.run(stream2)
        
        print(f"Файл успешно разделен:")
        print(f"Часть 1: {output1}")
        print(f"Часть 2: {output2}")
        
    except ffmpeg.Error as e:
        print(f"Произошла ошибка: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

# Пример использования
def main():
    input_file = "mp3/wg.mp3"
    split_time = "00:15:30"  # Разделить на 2 минуты 30 секунд
    output1 = "output/part1.mp3"
    output2 = "output/part2.mp3"
    
    if not os.path.exists(input_file):
        print("Входной файл не найден!")
        return
    
    split_mp3(input_file, split_time, output1, output2)

if __name__ == "__main__":
    main()