import pathlib
import os
import datetime
import subprocess


# Get the path to the current directory
current_directory = pathlib.Path.cwd()
files = list(current_directory.rglob("*.mp4"))
files.sort(key=lambda x: os.path.getmtime(x))


# List all files in the current directory
for file in files:
    if file.is_file():
        name = file.name

        if file.suffix == ".mp4":
            stat = file.stat()
            ok = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%c")

            source_file = str(file.name)
            base_file = f"{file.stem} upgraded.mp4"
            quality_file = f"{file.stem} quality.mp4"

            subprocess.check_call(
                [
                    "ffmpeg",
                    "-i",
                    source_file,
                    "-c:v",
                    "hevc_nvenc",
                    "-qp",
                    "17",
                    "-vf",
                    "scale=1920x1080:flags=lanczos",
                    base_file,
                ]
            )
            subprocess.check_call(
                [
                    "ffmpeg",
                    "-i",
                    source_file,
                    "-i",
                    base_file,
                    "-c:v",
                    "hevc_nvenc",
                    "-qp",
                    "17",
                    "-filter_complex",
                    "[0]pad=iw:1080:0:(1080-ih)/2,hstack",
                    quality_file,
                ]
            )


print("done")
