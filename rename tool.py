import pathlib
import datetime

# Get the path to the current location of where the script is stored
current_directory = pathlib.Path(__file__).absolute().parent
files = list(current_directory.rglob("*.mp4"))
files.sort(key=lambda path: path.stat().st_mtime)

count = 0
num = int(input("enter the video number:"))
# List all files in the current directory
for file in files:
    if file.is_file():
        name = file.name

        if file.suffix == ".mp4":
            stat = file.stat()
            ok = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%c")
            # ok not used

            file.rename(f"video-{num}.mp4")
            print(f"renamed file to video-{num}.mp4")
            print(f"original name is {name}\nDate Creation:\n{ok}")
            print("-----------------------------------------------")

            count = count + 1
            num = num + 1

print(f"{count} files found")
