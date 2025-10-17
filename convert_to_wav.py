import ffmpeg

input_file = r"C:\Users\monic\Downloads\audio-visualizer\DammyDee-Uk-Drill-type-freebeat (1).mp3"
output_file = r"C:\Users\monic\Downloads\audio-visualizer\DammyDee-Uk-Drill-type-freebeat.wav"

ffmpeg.input(input_file).output(output_file).run()

print("✅ Conversion complete: MP3 → WAV")
