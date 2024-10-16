import asyncio
import datetime
import json
import pathlib
import sys


async def get_media_created(path):
    proc = await asyncio.create_subprocess_exec(
        "ffprobe",
        "-i",
        str(path),
        "-loglevel",
        "error",
        "-show_entries",
        "stream_tags:format_tags",
        "-of",
        "json",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    output, errors = await proc.communicate()
    if proc.returncode != 0:
        print(errors.decode('utf-8', 'replace'), file=sys.stderr)
        sys.exit(1)
    data = json.loads(output.decode('utf-8'))
    try:
        return datetime.datetime.fromisoformat(data['format']['tags']['creation_time'])
    except (ValueError, KeyError):
        return datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.UTC)

async def process_file(file, num):
    if file.is_file() and file.suffix == ".mp4":
        stat = file.stat()
        ok = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%c")
        new_name = f"video-{num}.mp4"
        file.rename(file.with_name(new_name))
        print(f"renamed file to {new_name}")
        print(f"original name is {file.name}\nDate Creation:\n{ok}")
        print("-" * 50)
        return 1
    return 0

async def main():
    current_directory = pathlib.Path(__file__).absolute().parent
    files = list(current_directory.rglob("*.mp4"))

    sorted_files = await asyncio.gather(*[get_media_created(path) for path in files])
    files = [file for _, file in sorted(zip(sorted_files, files))]

    num = int(input("Enter the video number: "))

    tasks = [process_file(file, num + i) for i, file in enumerate(files)]
    results = await asyncio.gather(*tasks)

    count = sum(results)
    print(f"{count} files found")

if __name__ == "__main__":
    asyncio.run(main())