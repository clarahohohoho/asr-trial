# MANUAL

## convert vtt to txt:
python vtt2txt.py vtt-path

## download video with subs
youtube-dl --write-auto-sub https://www.youtube.com/watch?v=KjXeAE6Qoa8

## extract WAV from MP4
ffmpeg -i input.mp4 -ac 1 -ar 8000 -acodec pcm_s16le output.wav