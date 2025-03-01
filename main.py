import ffmpeg
import os

def convert_to_3gp(input_file, output_file):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Файл {input_file} не найден!")
        
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, format='3gp', vcodec='h263', acodec='aac', s='176x144', vb='200k')
        ffmpeg.run(stream, quiet=True)
        print(f"Сконвертировано в {output_file}")

    except ffmpeg.Error as e:
        print(f"Ошибка конвертации: {e.stderr.decode()}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    input_file = input("Введите путь к видео: ")
    output_file = input("Введите имя выходного файла (например, output.3gp): ")
    convert_to_3gp(input_file, output_file)