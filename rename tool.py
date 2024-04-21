import pathlib
import os
import datetime

# Get the path to the current directory
current_directory = pathlib.Path.cwd()
files = list(current_directory.rglob("*.mp4"))
files.sort(key=lambda x: os.path.getmtime(x))

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
