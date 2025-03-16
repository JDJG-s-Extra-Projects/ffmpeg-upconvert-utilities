import asyncio
import datetime
import pathlib

# Get the path to the current directory
current_directory = pathlib.Path(__file__).absolute().parent
files = list(current_directory.rglob("*.mp4"))
files.sort(key=lambda path: path.stat().st_mtime)


async def ffmpeg_shengians():
    # List all files in the current directory
    for file in files:
        if file.is_file():
            name = file.name

            if file.suffix == ".mp4":
                stat = file.stat()
                ok = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%c")
                # unused ok variable may use it for prints or something else I don't know yet.

                source_file = str(file)
                base_file = file.with_stem(f"{file.stem} upgraded")
                quality_file = file.with_stem(f"{file.stem} quality")

                proc = await asyncio.create_subprocess_exec(
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
                )
                await proc.wait()

                proc = await asyncio.create_subprocess_exec(
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
                )

                await proc.wait()


asyncio.run(ffmpeg_shengians())
print("done")
