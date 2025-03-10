import asyncio
import pathlib

async def ffmpeg_process_file(file_path):
    """Processes a single video file using ffmpeg with specific options."""
    output_file = file_path.with_stem(f"{file_path.stem}-30fps")

    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-y",
        "-stats",
        "-noautorotate",
        "-i",
        str(file_path),
        "-v",
        "error",
        "-sn",
        "-dn",
        "-map",
        "0",
        "-f",
        "mp4",
        "-vsync",
        "0",
        "-codec:v",
        "h264_nvenc",
        "-vb",
        "0",
        "-rc",
        "cbr",
        "-g",
        "2",
        "-bf",
        "0",
        "-codec:a",
        "aac",
        "-ab",
        "256k",
        "-filter:v",
        "fps=fps=30/1",
        str(output_file),
    )
    await proc.wait()
    if proc.returncode != 0:
        print(f"ffmpeg processing failed for {file_path}")

async def process_mp4_files(directory):
    """Processes all .mp4 files in the given directory recursively, processing sequentially."""
    files = list(directory.rglob("*.mp4"))
    for file in files:
        if file.is_file():
            await ffmpeg_process_file(file)

async def main():
    """Main function to start the file processing."""
    current_directory = pathlib.Path(__file__).absolute().parent
    await process_mp4_files(current_directory)
    print("done")

if __name__ == "__main__":
    asyncio.run(main())