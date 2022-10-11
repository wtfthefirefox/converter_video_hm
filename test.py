from os import listdir
from os.path import isfile, join
import ffmpeg

import subprocess
import shlex
import json

def IsVideoFormated(pathToInputVideo):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    # run the ffprobe & convert stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)

    # find height and width
    height = ffprobeOutput['streams'][0]['height']
    width = ffprobeOutput['streams'][0]['width']

    if (width % 16 == 0 and width // 16 * 16 == width and height % 9 == 0 and height // 9 * 9 == height):
        return True
    else:
        return False

def find_nth(str, symbol, n):
    start = str.find(symbol)
    while (start >= 0 and n > 1):
        start = str.find(symbol, start+len(symbol))
        n -= 1
    return start

arr_of_files = [f for f in listdir("./samples") if (isfile(join("./samples", f)) and f.find('.DS_Store') == -1)] # get files from input
arr_of_files = map(lambda f: './samples/' + f, arr_of_files);

for file in arr_of_files:
    try:
        if (IsVideoFormated(file)):
            (ffmpeg
            .input(file)
            .output('./result/' + file[find_nth(file, '/', 2) + 1:file.rfind('.')] + '.mp4', acodec='copy', vcodec='copy')
            .run())
        else:
            (ffmpeg
            .input(file)
            .filter("pad", x="-1", y="-1", aspect="16/9", color="red")
            .output('./result/' + file[find_nth(file, '/', 2) + 1:file.rfind('.')] + '.mp4')
            .run())
    except Exception as e:
        print(f"Error at {file}")
        print(e)