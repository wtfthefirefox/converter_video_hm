from os import listdir
from os.path import isfile, join
import ffmpeg

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
        (ffmpeg
        .input(file)
        .filter('setdar', '16/9') # add black line
        .output('./result/' + file[find_nth(file, '/', 2) + 1:file.rfind('.')] + '.mp4')
        .run())
    except Exception as e:
        print(f"Error at {file}")
        print(e)