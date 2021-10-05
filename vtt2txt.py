import webvtt
import re
import sys

def main():
    vtt_filename = sys.argv[1]
    vtt = webvtt.read(vtt_filename)
    transcript = ""

    lines = []
    for line in vtt:
        lines.extend(line.text.strip().splitlines())

    previous = None
    for line in lines:
        if line == previous:
            continue
        transcript += " " + line
        previous = line

    txt_filename =  re.sub(r'.vtt$', '_GT.txt', vtt_filename)

    #open text file
    text_file = open(txt_filename, "w")
    #write string to file
    text_file.write(transcript)
    #close file
    text_file.close()

if __name__ == "__main__":
    main()