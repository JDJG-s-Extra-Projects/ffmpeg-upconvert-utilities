import datetime
import pathlib
import sys
import datetime
import zoneinfo
import json
import subprocess


def get_media_created(path):
    proc = subprocess.Popen([
        "ffprobe",
        "-i",
        str(path),
        "-loglevel",
        "error",
        "-show_entries",
        "stream_tags:format_tags",
        "-of",
        "json"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, errors = proc.communicate()

    if proc.returncode != 0:  # when not successfull, print errors and exit
        print(errors.decode('utf-8', 'replace'), file=sys.stderr)
        sys.exit(1)
    data = json.loads(output)
    try:
        return datetime.datetime.fromisoformat(data['format']['tags']['creation_time'])
    except (ValueError, KeyError):
        return datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.UTC)

# Get the path to the current location of where the script is stored
current_directory = pathlib.Path(__file__).absolute().parent
files = list(current_directory.rglob("*.mp4"))
files.sort(key=lambda path: get_media_created(path))

count = 0
num = int(input("enter the video number:"))
# List all files in the current directory
for file in files:
    if file.is_file():
        name = file.name

        if file.suffix == ".mp4":
            stat = file.stat()
            ok = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%c")

            file.rename(f"video-{num}.mp4")
            print(f"renamed file to video-{num}.mp4")
            print(f"original name is {name}\nDate Creation:\n{ok}")
            print("-----------------------------------------------")

            count = count + 1
            num = num + 1

print(f"{count} files found")
