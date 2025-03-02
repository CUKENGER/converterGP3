import ffmpeg

def convert_mp4_to_mp3(input_file, output_file):
    try:
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, format='mp3', acodec='mp3', audio_bitrate='192k')
        ffmpeg.run(stream)
        print(f"Конвертация завершена: {output_file}")
    except ffmpeg.Error as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
input_file = "files/wg.mp4"
output_file = "mp3/wg.mp3"
convert_mp4_to_mp3(input_file, output_file)